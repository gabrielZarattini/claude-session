# SOP: Collective Efficiency Ledger — instrumentar a eficiência do coletivo de agentes (`collective-efficiency-ledger`)

**Status:** ACTIVE · v1.0 · 2026-06-26
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrito **ANTES** de qualquer código do Collective Efficiency Ledger (a VIEW `collective_efficiency_ledger` + o RPC `collective_efficiency_rollup` + os emits de overhead). Abre o gate **OTD-AG-001** (flagship da doutrina `docs/architecture/agentic-vision.md` §4). Cobre **FR-AG-001..005**.
**Canonical directive:** `docs/architecture/agentic-vision.md` (doutrina AGI→ASI · Via 4) · `.claude/rules/survival.md > Law 1 (Materiality)` · `docs/bok/agentic-governance/{04-frd,05-sdd,06-data-model}.md` (SSOT) · `CLAUDE.md > Security model` (RLS default-deny + `infra_health_logs` no-PII).
**Sibling SOPs:** `autopilot-cron-identity.md` (de onde vem a verdade financeira `autopilot_cycles`) · `schema-drift-audit.md` (todo hotfix vira migration) · `edge-jwt-identity-verification.md`.

---

## Context

O paper *From AGI to ASI* (DeepMind) aponta como **aberto** justamente o que o MCORCH ainda não faz: respondemos as perguntas de coletivo de agentes (Via 4) **por doutrina, mas não *medimos* nenhuma** — valor marginal por agente (V4-2), custo por resultado (V4-4), overhead de coordenação (V4-5). Crescemos o coletivo **no escuro**. O Ledger fecha isso **derivando** a métrica da verdade financeira que já existe — sem novo write-path, sem auto-report.

Dois riscos materiais nascem da instrumentação:

1. **Vazamento cross-tenant (FM-AG-001 / SEC-AG-CRIT-01).** A VIEW une `pipeline_runs` + `autopilot_cycles`, ambas com dados financeiros por tenant. Uma VIEW **sem** `security_invoker = on` roda com os privilégios do *dono* da VIEW (postgres) e **ignora a RLS das bases** → qualquer `authenticated` leria o ledger de **todos** os tenants (eficiência + gasto da concorrência). A regra é inviolável: `security_invoker = on`, herdando a RLS `SELECT-own` das bases; e o rollup **cross-tenant** (que existe para a decisão de escala do Sovereign) é **service-role-only** (`REVOKE` de `anon`/`authenticated`), nunca exposto ao tenant.

2. **PII / Goodhart na telemetria de overhead (FM-AG-003 / FM-AG-002).** Os emits `collective_hop`/`collective_retry` vão para `infra_health_logs`, que é **global-read** (`authenticated` lê tudo, para o HUD). O contrato da tabela proíbe PII/segredo no `metadata` — então o emit carrega **apenas** `{ run_id, collective_type }`, nunca topic/conteúdo/user-identificável. E a métrica jamais é escrita *para* o ledger (seria gameável — alerta explícito do paper): ela é **derivada** de `mcoin`/`cycles` (verdade que ninguém infla para "parecer eficiente").

**Regra-mãe:** o Ledger **lê e deriva**, nunca escreve um número de eficiência. Per-tenant herda RLS via `security_invoker`; cross-tenant é service-role-only; telemetria de overhead é allowlist sem PII; e **V4-2 (valor marginal/agente) fica deferido a um experimento real** — não se fabrica um proxy gameável só para ter o número.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (autoria da migration da VIEW/RPC + os 2 emits) + Postgres (executa a VIEW por query, sob a identidade do caller via `security_invoker`).
- **Reviewer:** Sovereign (Gabriel) — aprova a migration + `/security-review` independente (mandato `CLAUDE.md` FMEA-011) + valida a prova material de `count cross-tenant = 0`.
- **Owner:** Sovereign — blast radius = **exposição de gasto/eficiência entre tenants** (se a RLS herdada falhar) + **decisão de escala errada** (se a métrica medir a coisa errada / for gameável).

---

## Operator (equivalente manual — material)

A automação substitui o ritual que o Sovereign executaria **hoje, à mão**, para responder "o coletivo está ficando mais eficiente, ou só mais caro?":

| # | Passo manual | Critério de sucesso material |
|---|--------------|------------------------------|
| 1 | Abrir o DB e listar os runs do coletivo (`pipeline_runs` + `autopilot_cycles`) de uma janela | Lista de runs com `mco` e `status` visível |
| 2 | Para cada run: calcular o custo **real** (autopilot: `spend_mco − refunded_mco`; orchestrate: `mco_cost`) | `mco_actual` por run conhecido |
| 3 | Contar os resultados **entregues** por run (autopilot: linhas em `creative_metrics` do ciclo; orchestrate: `status='done'`) | `n_results` por run conhecido |
| 4 | Dividir: `mco_actual ÷ n_results` por tipo de coletivo | `mco_per_result` por `collective_type` (V4-4) |
| 5 | Anotar overhead: nº de steps + nº de retries por run | `coordination_overhead` por run (V4-5) |
| 6 | Comparar a tendência entre janelas → **decidir escala** (mais agentes onde mco/resultado cai; cortar onde overhead sobe) | Decisão fundada, não "no escuro" |

O passo 6 **continua sendo do humano** (HITL — Survival/ORO). A VIEW + rollup automatizam os passos 1–5. **O gate Lei 2 existe porque automatizar o passo 1–4 com uma VIEW que vaza cross-tenant expõe o gasto de um tenant a outro, e medir o passo 4 com um número auto-reportado (Goodhart) leva o passo 6 a uma decisão de escala errada.**

---

## Sequence (passos numerados, cada um com gate material)

1. **Migration da VIEW** `public.collective_efficiency_ledger` `WITH (security_invoker = on)` — UNION de `pipeline_runs` + `autopilot_cycles` (colunas em `docs/bok/agentic-governance/06-data-model.md`). **Gate G1:** o DDL contém literal `security_invoker = on`.
2. **RPC `collective_efficiency_rollup()`** — `SECURITY DEFINER · SET search_path = '' · REVOKE ALL FROM PUBLIC, anon, authenticated · GRANT EXECUTE TO service_role`. Agrega cross-tenant (AVG mco_actual, AVG wall_clock_ms, retry-rate) por `collective_type`. **Gate G2:** `grep` confirma os 4 elementos (DEFINER · search_path='' · REVOKE · GRANT service_role).
3. **`/security-review`** na migration **antes do commit**. **Gate G3:** veredito SAFE (sem cross-tenant leak, sem search_path mutável).
4. **Emits de overhead** — `collective_hop` em `orchestrate-content` (1 por kick de `async_orchestrate_step`) + `collective_retry` em `orchestrate-step` (branch de erro existente), `metadata = { run_id, collective_type }`. **Gate G4:** `grep` confirma que nenhum emit carrega topic/body/user-PII.
5. **Aplicar a migration** (`supabase db push` ou bridge). **Gate G5:** `db push` retorna sucesso material (output literal).
6. **Prova material per-tenant** — com um JWT de usuário real, `SELECT count(*) FROM collective_efficiency_ledger WHERE user_id <> auth.uid()` = **0**. **Gate G6 (o gate-mãe):** zero linha de outro tenant visível.
7. **Prova material da métrica** — um run real (orchestrate-content ou ciclo autopilot) aparece como linha com `mco_actual` e `wall_clock_ms` corretos vs a base. **Gate G7:** valores batem com `pipeline_runs`/`autopilot_cycles`.
8. **tsc + lint** limpos (se o hook de surfacing for tocado). **Gate G8:** `npx tsc --noEmit` = 0.

---

## Verification gates (resumo)

| Gate | Comando / critério | Esperado |
|------|--------------------|----------|
| G1 | `grep -c 'security_invoker = on' <migration>` | ≥ 1 |
| G2 | `grep -E "SECURITY DEFINER\|search_path = ''\|GRANT EXECUTE.*service_role" <migration>` | os 3 presentes + REVOKE |
| G3 | `/security-review` | SAFE |
| G4 | `grep` nos 2 emits | metadata só `{run_id, collective_type}` |
| G5 | `supabase db push` | output de sucesso |
| **G6** | `SELECT count(*) ... WHERE user_id <> auth.uid()` (JWT real) | **0** |
| G7 | comparar 1 linha da VIEW vs base | valores idênticos |
| G8 | `npx tsc --noEmit` | 0 |

---

## Recovery path (falha por gate)

- **G1/G2 falha (DDL incompleto):** corrigir o DDL ANTES de aplicar — nunca aplicar uma VIEW sem `security_invoker` (seria leak imediato). Rollback = `DROP VIEW` + reescrever.
- **G3 `/security-review` aponta leak:** não commitar. O achado mais provável é `security_invoker` ausente OU o rollup acessível a `authenticated` — aplicar a correção e re-rodar.
- **G6 falha (linha cross-tenant visível):** **HALT IMEDIATO + `DROP VIEW`** — é a primitiva de vazamento. Causa quase certa: `security_invoker` não pegou (Postgres < 15 OU sintaxe). Validar versão; reaplicar. Não há "tentar de novo" — provar `count = 0` de novo.
- **G7 falha (métrica diverge):** a expressão de `mco_actual`/`wall_clock_ms` está errada (ex.: status divergente 'done' vs 'completed', ou EXTRACT errado). Corrigir a VIEW; reaplicar; re-provar.
- **Drift:** se algo for hotfixado direto em prod, **vira migration na MESMA sessão** (`schema-drift-audit.md`).

---

## Success signal (materialmente observável)

O flow está completo quando, **com um JWT de usuário real**:
1. `SELECT * FROM collective_efficiency_ledger LIMIT 5` retorna runs reais do tenant (UUIDs reais).
2. `... WHERE user_id <> auth.uid()` retorna **0** (G6 — prova de isolamento).
3. Uma linha da VIEW bate coluna-a-coluna com a base (`pipeline_runs`/`autopilot_cycles`).
4. `collective_efficiency_rollup()` é **negado** a `authenticated` (`permission denied`) e **permitido** a `service_role`.
5. `/security-review` = SAFE; `tsc` = 0.

Só então o Sovereign pode ler o rollup e **decidir escala com dado, não no escuro** — o objetivo da Via 4 instrumentada.

---

_Generated by MCORCH Master Execution Agent — SOP Lei 2 antes do código (OTD-AG-001)._

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

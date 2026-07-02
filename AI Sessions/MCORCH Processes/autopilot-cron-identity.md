# SOP: Viral Autopilot — Cron Identity + Pre-Debit/Refund Atomicity (`autopilot-cron-identity`)

**Status:** ACTIVE · v1.0 · 2026-06-20
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrito **ANTES** de qualquer código da fatia de cadência/custo do Viral Autopilot (R2 recorrência + R3 loop). Abre o gate **OTD-VA-008** (`docs/bok/viral-autopilot/05-sdd.md:425` — *"Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer código"*) e cobre o pré-débito/refund atômico de **FR-VA-007** + o cap diário de **FR-VA-021**.
**Canonical directive:** `CLAUDE.md > "API Tenancy Model — Per-User Credentials"` · `.claude/rules/survival.md > Law 1 (Materiality) / Law 2 (Anticipated Process)` · `docs/bok/viral-autopilot/{04-frd,05-sdd,06-data-model}.md`
**Sibling SOPs:** `edge-jwt-identity-verification.md` (camada-3 service-role gate, base deste) · `orchestrate-async-pipeline.md` (mandato `verify_jwt=false` + pg_net + contrato de param-name dos RPCs).

---

## Context

A fatia de cadência do Viral Autopilot introduz **automação financeira autônoma**: um `pg_cron` dispara a geração+publicação de criativos a cada N dias, **sem mão humana no loop**, gastando `mco_balance` do tenant. Dois riscos materiais nascem disso:

1. **Identidade do caminho cron (SEC-VA-CRIT-01 / OTD-VA-008).** As funções `autopilot-*` rodam com `verify_jwt = false` em `supabase/config.toml` — o gateway Kong **não** valida JWT (mesmo motivo de todo o ecossistema: a sessão do usuário é ES256, o gateway está configurado para o segredo HS256 legado; ver `edge-jwt-identity-verification.md`). O cron **não possui** um JWT de usuário para repassar. A tentação fatal é confiar num header `x-autopilot-user-id` vindo do request — o que deixaria **qualquer** chamador drenar a carteira de **qualquer** vítima (`POST autopilot-run` com `x-autopilot-user-id: <victim>` → débito + publicação na conta da vítima). A validação adversarial da BoK (Fase 6, rodada R1) marcou exatamente este vetor como **blocker**.

2. **Atomicidade do pré-débito/refund (FR-VA-007 / TOCTOU SEC-VA-04).** Um ciclo gera `N_runs = |produtos| × |redes| × ab_variants` sub-runs, cada um um bundle flat de 10 mcoCoins (`billing.ts:16-21` — imagem **já incluída**). Se cada sub-run se auto-cobrar, uma falha no meio deixa o tenant cobrado por trabalho não-entregue; se o cap diário for checado com um `SELECT` separado do `deduct`, dois ciclos concorrentes passam o cap juntos (TOCTOU). A rodada R2 da validação pegou um **anti-mint** que eu mesmo introduzi: refund implementado como `deduct` de valor negativo viola o guard `p_amount <= 0` de `deduct_mco_coins` (`migration 20260603220000:45`) — refund **tem** que ser crédito positivo.

**Regra-mãe:** confiar num `user_id` no caminho cron só é permitido depois de **provar posse da `SB_SECRET_KEY` in-function** E de derivar o `user_id` de uma **linha confiável do banco** (`autopilot_plans.user_id` / `autopilot_cycles.user_id`), **nunca do corpo/header do request**. Todo movimento de saldo passa por **um** RPC `SECURITY DEFINER` service-role-only, com cap + débito na **mesma transação sob advisory lock**, e refund como **crédito positivo idempotente**.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (autoria das migrations/funções) + `pg_cron` apresentando a Vault key (execução por tick) + Edge runtime Deno (gate por request).
- **Reviewer:** Sovereign (Gabriel) — aprova as migrations + valida os smokes zero-cost e o exploit test pós-deploy · `/security-review` independente em **cada** migration (mandato `CLAUDE.md`).
- **Owner:** Sovereign — blast radius = **carteira do tenant gasta autonomamente** (mint/drain cross-tenant se a identidade falhar; sangria silenciosa se o cap/refund falhar).

---

## Operator (equivalente manual — material)

A automação substitui o seguinte ritual humano que o Sovereign executaria **hoje, à mão**, a cada janela de cadência, para cada plano ativo:

| # | Passo manual | Critério de sucesso material |
|---|--------------|------------------------------|
| 1 | Abrir a UI do Autopilot e listar os planos cujo `next_run_at` venceu | Lista de `plan_id` vencidos visível |
| 2 | Para cada plano: conferir o `mco_balance` **e** quanto já gastou hoje (não estourar o cap diário) | `balance` e `gasto_hoje` lidos antes de qualquer clique |
| 3 | Calcular `N_runs = produtos × redes × variants` e `projetado = N_runs×10 + 2` | Número conferido contra o cap do plano |
| 4 | Clicar "gerar agora" **uma vez** por plano (dispara os sub-runs) | 1 débito de `projetado`, depois os sub-runs publicam |
| 5 | Aguardar os sub-runs; anotar quantos **de fato** publicaram | `actual` real conhecido |
| 6 | Reconciliar: devolver ao saldo os coins dos runs que **não** entregaram | `balance` final = inicial − `actual` |
| 7 | Reagendar o plano para a próxima janela (`next_run_at += interval_days`) | Plano re-armado |

O `pg_cron` automatiza os passos 1–7. **O gate Lei 2 existe porque automatizar o passo 2 (cap) e o passo 6 (refund) errado = sangria silenciosa de carteira.** O precedente vivo desta topologia é **`nurture-cron` → `nurture-dispatch`** (`supabase/functions/nurture-cron/index.ts`): driver service-role que varre `next_run_at` vencidos e faz fan-out com cap `MAX_PER_RUN` + `CONCURRENCY`, cada linha carregando seu próprio `user_id` confiável.

---

## Topologia (alvo)

```
pg_cron  ──Bearer SB_SECRET_KEY──▶  autopilot-cadence-cron   (driver service-role)
  (Vault key)                          │  SELECT plan_id,user_id FROM autopilot_plans
                                       │  WHERE status='active' AND next_run_at <= now()
                                       │  (user_id = SERVER-TRUSTED da linha)
                                       ▼  fan-out (cap MAX_PER_RUN + CONCURRENCY)
            ──Bearer SB_SECRET_KEY──▶  autopilot-run          (executor por plano)
            + x-autopilot-user-id        │  ① prova service-role in-function
                                         │  ② begin_autopilot_cycle (cap + pré-débito atômico, advisory lock)
                                         │  ③ fan-out sub-runs
                                         ▼
            ──Bearer SB_SECRET_KEY──▶  orchestrate-content    (prepaid=true → NÃO self-bill)
            + x-autopilot-user-id        │  geração product-aware + monetize (Fatia 1)
                                         ▼
                                       finalize_autopilot_cycle (refund crédito-positivo idempotente)
                                         │
                                         ▼  inline pós-ciclo
                                       autopilot-analyze       (R3 loop; tenant de previous_cycle_id)
```

---

## Identity resolution order (canonical — funções `autopilot-*`, `verify_jwt=false`)

| # | Camada | Fonte | Permitido em |
|---|--------|-------|--------------|
| 1 | **Service-role gate (caminho cron — PRIMÁRIO aqui)** | `req.headers.get("Authorization") === \`Bearer ${SB_SECRET_KEY}\`` → **403** se não. Padrão literal vivo: `nurture-cron/index.ts` (self-check) + `orchestrate-step/index.ts:110` (`SB_SECRET_KEY ?? SUPABASE_SERVICE_ROLE_KEY`). | `autopilot-cadence-cron`, `autopilot-run` (tick), `autopilot-analyze`, `autopilot-collect` |
| 2 | **`user_id` server-trusted** | Derivar de uma **linha do banco**: `autopilot_plans.user_id` (cadence-cron) · `autopilot_cycles.user_id` via `previous_cycle_id` (analyze) · `scheduled_posts`/`autopilot_cycles` (collect). O header `x-autopilot-user-id` é só um **espelho** desse valor para logging/propagação — **nunca a fonte de verdade**. | Idem (sempre, após camada 1) |
| 3 | **User JWT ("gerar agora")** | Caminho user-facing: `getUser()` / JWKS verify (sibling SOP) → **asserir `user.id === plan.user_id`** (IDOR gate). | `autopilot-run` (botão UI) |
| 4 | **Hard failure** | — | **403** `{ error: "Forbidden" }` (cron) / **401** `{ error: "Token inválido" }` (user). **Fail-closed.** |

**Regra de ouro (herdada de `edge-jwt-identity-verification.md`, estendida):** no caminho cron, confiar num `user_id` exige **(a)** posse provada da `SB_SECRET_KEY` **E** **(b)** o `user_id` ter vindo de uma linha do banco — não do request. As duas condições, sempre, e nessa ordem.

---

## Sequence (o tick → ciclo → finalize)

1. **`pg_cron` dispara `autopilot-cadence-cron`** via pg_net, header `Authorization: Bearer <SB_SECRET_KEY>` (Vault). Sucesso material: linha `infra_health_logs service='autopilot-cadence-cron'`.
2. **`autopilot-cadence-cron` prova service-role** (camada 1) → 403 se ausente. Varre `autopilot_plans WHERE status='active' AND next_run_at <= now()` (índice parcial, espelha `idx_enroll_due`). Sucesso: lista de `{plan_id, user_id}` (user_id **da linha**).
3. **Fan-out** para `autopilot-run` (cap `MAX_PER_RUN`, `CONCURRENCY`), cada POST com `Bearer SB_SECRET_KEY` + `x-autopilot-user-id` = `plan.user_id`. **Sem fan-out ilimitado silencioso** (logar se o cap for atingido — padrão `nurture-cron`).
4. **`autopilot-run` prova service-role** (camada 1) **OU** valida JWT+IDOR (camada 3). Resolve `user_id` server-trusted. Calcula `N_runs` e `projetado = N_runs×10 + ANALYZE_COST(2)`.
5. **`begin_autopilot_cycle(p_user_id, p_plan_id, p_projected_mco, p_daily_cap_mco, p_budget_cap_mco)`** — RPC `SECURITY DEFINER`, service-role-only, **`pg_advisory_xact_lock(hashtext(user_id::text))`**:
   - **Cap diário (FR-VA-021):** `SUM(spend_mco)` dos `autopilot_cycles` do tenant no dia (UTC). Se `acumulado + projetado > daily_cap_mco` → `RAISE` `aborted_daily_cap` (**sem deduzir**).
   - **Cap por plano + saldo (FR-VA-007):** `projetado > budget_cap_mco` → `aborted_budget`; `balance < projetado` → `insufficient_balance`. Ambos `RAISE` **sem deduzir** + pausam o plano.
   - **OK:** `INSERT autopilot_cycles (state='open', debited_at=now(), spend_mco=projetado)` **+** `deduct_mco_coins(user_id, projetado)` na **mesma transação** → `RETURN cycle_id`. **Um** débito por ciclo. O advisory lock serializa ciclos concorrentes do mesmo tenant → mata o TOCTOU.
6. **Fan-out dos sub-runs** → `orchestrate-content` com `prepaid=true` + service-role + `x-autopilot-user-id` (FR-VA-016). **`prepaid` ⇒ NÃO chama `deduct_mco_coins`** (já pré-debitado no passo 5). Sucesso: `pipeline_runs` por sub-run; `affiliate_links.content_id` NON-NULL (herdado da Fatia 1).
7. **`finalize_autopilot_cycle(p_cycle_id, p_actual_mco)`** — RPC `SECURITY DEFINER`, service-role-only, **espelha `finalize_vision_job` (`20260615160000`):**
   - Claim-once: `UPDATE autopilot_cycles SET state='closed', actual_mco=p_actual, refunded_at=now() WHERE id=p_cycle_id AND state='open' RETURNING user_id`. Se `NULL` → já terminal → **no-op** (sem refund duplo).
   - `refund = projetado − actual`; se `refund > 0` → **`add_mco_coins(user_id, refund)`** (crédito **positivo** ledgered) na **mesma transação**. **NUNCA `deduct` negativo.**
8. **`autopilot-analyze` inline** (não cron próprio) — tenant de `previous_cycle_id` (camada 2). 2 mco **só se `has_real_data`** (senão 0, log `analyze_empty`).
9. **Reagendar:** `next_run_at += interval_days` (catch-up de janela perdida — FR-VA-005). Sucesso: `next_run_at` futuro.

---

## Cost & atomicity contract (resumo executável)

| Invariante | Como é garantido | Âncora |
|------------|------------------|--------|
| **Um débito por ciclo** | `begin_autopilot_cycle` faz o `deduct` único; sub-runs `prepaid` | FR-VA-007 · FR-VA-016 |
| **Cap + débito atômicos (anti-TOCTOU)** | tudo dentro de `begin_autopilot_cycle` sob `pg_advisory_xact_lock` | FR-VA-007 / SEC-VA-04 |
| **Refund = crédito positivo** | `add_mco_coins(user, refund)`; `deduct_mco_coins` rejeita `p_amount<=0` | `20260603220000:45` |
| **Refund idempotente (sem duplo)** | claim-once `WHERE state='open' RETURNING user_id` | espelha `finalize_vision_job` |
| **Abort não cobra** | caps fazem `RAISE` antes do `deduct` | FR-VA-007 / FR-VA-021 |
| **RPCs blindados** | `REVOKE ... FROM PUBLIC, anon, authenticated; GRANT ... TO service_role` | padrão ledger `20260603220000` |
| **`user_id` nunca do body** | derivado de `autopilot_plans/_cycles` (linha confiável) | OTD-VA-008 (Decisão B) |

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| **G1 — Cron identity (exploit, prod)** | `curl -X POST <autopilot-run-url>` com `x-autopilot-user-id: <victim>` **sem** `Bearer SB_SECRET_KEY` (apikey anon) | **403** — nenhum débito, nenhum ciclo criado (sem o gate: processaria como vítima) |
| **G2 — IDOR no caminho user** | JWT do user A com `plan_id` do user B | **401/403** — `user.id !== plan.user_id` rejeitado |
| **G3 — Pré-débito atômico (smoke zero-cost)** | `scripts/qa/smoke-autopilot-budget.ts`: `begin_autopilot_cycle` com `projetado > balance` | `insufficient_balance`, `mco_balance` **intacto** (SELECT antes/depois) |
| **G4 — Cap diário (smoke zero-cost)** | acumular `spend_mco` fictício > `daily_cap`, chamar `begin_*` | `aborted_daily_cap`, **sem deduct** |
| **G5 — Refund idempotente** | `finalize_autopilot_cycle` chamado **2×** no mesmo `cycle_id` | 1º credita `refund`; 2º `finalized=false` (no-op) — saldo creditado **uma** vez |
| **G6 — Refund nunca-negativo** | `finalize_*` com `actual > projetado` (refund negativo) | `refund` clampado a 0 (nunca chama `deduct`); CHECK `actual_mco <= spend_mco` no DDL |
| **G7 — `prepaid` não self-cobra** | sub-run `orchestrate-content` com `prepaid=true` | nenhuma linha `mcoin_transactions` do sub-run; só o débito único do `begin_*` |
| **G8 — RPC grants** | `\df+ begin_autopilot_cycle finalize_autopilot_cycle` (ou Management API) | EXECUTE **só** `service_role`; revogado de `public/anon/authenticated` |
| **G9 — `/security-review`** | cada migration nova | **SAFE** (0 findings ≥ High) antes do commit |
| **G10 — Advisory lock real** | 2 `begin_*` concorrentes do mesmo user (teste de stress) | serializados; soma nunca passa o cap |

G1/G3/G4/G5 são **zero-cost** (usam `dry_run`/usuários descartáveis/RPC isolado) — provam o gate **sem** gastar mcoCoins reais. O 1º ciclo pago real (E2E) é **gated em GO Sovereign** (mesma disciplina das fatias anteriores).

---

## Recovery path

- **Cron dispara mas a fn rejeita (403):** verificar que o `pg_cron` job injeta a Vault key correta no header (`SB_SECRET_KEY`, **não** a legada `SUPABASE_SERVICE_ROLE_KEY` revogada — ver memória `reference_supabase_keys_migrated`). Recriar o job com `Authorization: Bearer <SB_SECRET_KEY>`.
- **Débito feito mas fan-out falha (crash entre passo 5 e 6):** o ciclo fica `state='open'` com `debited_at` setado e `actual=0`. Um **sweep de reconciliação** (cron diário ou poll, espelha o self-heal de órfão do `deepsearch.poll`) chama `finalize_autopilot_cycle(cycle_id, actual_real)` → credita o não-usado. O claim-once garante idempotência mesmo se o sweep e o caminho normal colidirem.
- **Refund parece não creditar:** confirmar materialmente via `SELECT mco_balance` antes/depois + a linha `mcoin_transactions action='autopilot_refund'`. NUNCA "tente de novo" cego — `finalize_*` é idempotente, re-chamar é seguro e diagnóstico.
- **Cap diário travando ciclos legítimos:** ajustar `daily_cap_mco` no plano (config do tenant), nunca remover a checagem. O cap é a feature, não o bug.
- **Rollback de migration:** as migrations são aditivas (novas tabelas/RPCs). Rollback = `DROP FUNCTION begin_autopilot_cycle / finalize_autopilot_cycle` + `DROP TABLE autopilot_cycles / autopilot_plans` (ordem FK). Confirmar via Management API.

---

## Success signal

- **G1 verde:** `403` literal no exploit test contra produção (cron sem `Bearer` → rejeitado), colado no handoff (Lei 1).
- **G3/G4 verdes:** smokes zero-cost com `mco_balance` **byte-idêntico** antes/depois de um abort (SELECT real).
- **G5 verde:** refund creditado **exatamente uma** vez sob dupla-finalização.
- **G8 verde:** `service_role`-only nos dois RPCs (output literal do `\df+` / Management API).
- **G9 verde:** `/security-review` SAFE em cada migration.
- **1º ciclo pago real (gated):** `autopilot_cycles` `state='closed'`, `deduct` = `projetado`, `refund` = `projetado − actual`, `mco_balance` final = inicial − `actual` (delta material exato).

---

## Anti-patterns proibidos

- ❌ Confiar em `x-autopilot-user-id` (ou qualquer `user_id` do body/header) **sem** provar `SB_SECRET_KEY` in-function E sem derivar de linha do banco.
- ❌ `deduct_mco_coins(user, -refund)` para "estornar" — viola o guard anti-mint (`20260603220000:45`). Refund é **`add_mco_coins` positivo**.
- ❌ Checar o cap com um `SELECT` e depois `deduct` em chamadas separadas (TOCTOU). Cap + débito vão **juntos** no `begin_autopilot_cycle` sob advisory lock.
- ❌ Sub-run `orchestrate-content` self-cobrando no caminho cron (duplo débito). `prepaid=true` ⇒ sem `deduct`.
- ❌ `finalize_*` sem claim-once → refund duplo a cada retry/sweep.
- ❌ Fan-out ilimitado sem cap por tick (`MAX_PER_RUN`) — drift de custo silencioso.
- ❌ `GRANT EXECUTE` dos RPCs de ciclo a `authenticated`/`anon` (qualquer um cunharia/estornaria). **Service-role-only.**
- ❌ `verify_jwt=true` no gateway para as `autopilot-*` (quebraria o caminho cron **e** o user ES256).
- ❌ Setar `daily_cap`/`budget_cap` como opcional/ausente — o cron **não** roda sem teto (kill-switch obrigatório, FMEA-VA-001 RPN 128).

---

## Sibling reference

- **Camada-3 service-role gate (base):** `docs/processes/edge-jwt-identity-verification.md` + `supabase/functions/nurture-cron/index.ts` (precedente vivo idêntico de cron→dispatch).
- **`verify_jwt=false` + pg_net + param-name contract:** `docs/processes/orchestrate-async-pipeline.md`.
- **Anti-mint ledger RPCs:** `supabase/migrations/20260603220000_secure_ledger_rpcs.sql` (`deduct_mco_coins` sign+own-tenant guards; `award_mco_coins`/`add_user_score` edge-only).
- **Atomic terminal+refund (molde):** `supabase/migrations/20260615160000_vision_mcp_jobs.sql` (`finalize_vision_job` claim-once + `add_mco_coins` positivo).
- **Sealed contract:** `docs/bok/viral-autopilot/04-frd.md` (FR-VA-002/007/008/010/016/021) · `05-sdd.md:425-427` (OTD-VA-008 + nota do gate Lei 2).

---

## Amendment 2026-07-02 — Fan-out hygiene (plataformas sem step não fanam)

`orchestrate-content` só tem steps reais p/ `wordpress`/`linkedin`/`twitter` (stepsOrder; `knowledge_mesh` é fallback universal — `orchestrate-content:244-246`). Um sub-run de `youtube`/`tiktok`/`pinterest`/`instagram` cairia direto no `knowledge_mesh` e AINDA contaria `ORCH_COST` (10) no actual — charge-com-valor-mínimo. A distribuição p/ essas redes é responsabilidade do **reshaper** (FR-CP-003) sobre o master 9:16 do pilar wordpress (provado no DB: `channel_variants` `reused_master` p/ tiktok/youtube/pinterest/instagram no ciclo `77e02fca`) — não do fan-out.

**Guard (`autopilot-run`):** `FAN_OUT_PLATFORMS = {wordpress, linkedin, twitter}`; plataformas do plano fora do set são filtradas ANTES do `nRuns`/`projected` (não pré-debitam, não fanam) + telemetria `event='fanout_platform_skipped'` em `infra_health_logs`. Plano só com plataformas não-suportadas → `422 plan_has_no_targets`.

## Amendment 2026-07-02 (b) — B4 EWMA multi-ciclo no analyze

`autopilot-analyze` agora agrega o reward sobre a janela dos **últimos M=5 ciclos do plano** (ancorada no ciclo analisado), peso `0.5^idade` — FRD v0.3 "fixes embarcados" (FR-VA-010/011) + SDD §fluxo ("EWMA M ciclos"). **Semântica documentada:** ciclo zerado sob plano COM histórico ainda emite policy (a janela lembra — anti-thrash); só plano com janela toda vazia retorna `has_real_data=false` (nunca inventa do nada). Auditoria em `reward_vector.ewma {m, decay, cycles_used}`. M/decay = constantes de código até a coluna config-as-data `reward_weights` existir (NFR-VA-010, deferida junto com os pesos do reward). Gate: smoke `smoke-autopilot-loop.ts` L7 (evidência acumulada vence vencedor fraco recente).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

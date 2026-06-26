# Session agent-aeae6da7e8d1cdbe8
**Date:** 2026-06-26 | **Session ID:** `agent-aeae6da7e8d1cdbe8`

---

## 👤 User *(23:15:31)*

Você é um arquiteto de sistemas agênticos desenhando o MENOR loop de Learning & Adaptation que realmente COMPÕE (fica mensuravelmente melhor a cada ciclo) para o MCORCH. Read-only.

CONTEXTO: a doutrina docs/architecture/agentic-vision.md marca Learning & Adaptation como o único padrão FRACO (OTD-AG-002, P0). O paper Gulli (cap 9) diz: o mecanismo é RL/online-learning/A-B/auditoria, e o PITFALL é reward de métrica única → gaming, não objetivo real → usar reward MULTI-MÉTRICA. Acabamos de construir o Collective Efficiency Ledger (mede mco/resultado — eficiência, não valor de desfecho).

SURVEY (leia/cite):
- O mandato Obstáculo→Síntese (CLAUDE.md §5) — é aprendizado do PROCESSO de dev, mas manual. 
- OpenClaw Dreaming (.claude/skills/openclaw-dreaming/SKILL.md) — promoção de memória é um loop de aprendizado? de quê?
- ab_variants no viral-autopilot (docs/bok/viral-autopilot/) — existe infra de A/B? é usada para aprender?
- creative_metrics + o Collective Efficiency Ledger novo (supabase/migrations/20260626120000) — que sinais já temos.

PROJETE (concreto):
1. Qual é o NORTH-STAR reward multi-métrica que evita Goodhart? (ex: combinação ponderada de receita_atribuída + alcance/reach + engajamento + sinal de marca — proponha a fórmula e de onde vem cada termo). Conecte à virada brand-persona (hoje o objetivo é MARCA + alcance, não só receita de afiliado).
2. Qual é o MENOR loop genuinamente fechado e multi-métrica que poderíamos shippar para COMPOR — e que seja honesto (anti-Goodhart, anti-proxy-gameável)? Descreva: o que mede, onde guarda o reward, como o próximo ciclo MUDA de comportamento por causa dele, e como provamos materialmente que melhorou.
3. O que é o gargalo REAL: falta de loop, ou falta de DADO de desfecho (dependência da frente B)? Seja honesto sobre o que destrava o quê.
~800 palavras, concreto, cite arquivos.

## 🤖 Claude *(23:15:32)*

I'll start by reading the key files cited in the survey to ground my design materially.

## 🤖 Claude *(23:15:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat docs/architecture/agentic-vision.md 2>/dev/null | head -200; echo \"=== END agentic-vision ===\"; ls docs/bok/viral-autopilot/ 2>/dev/null",
  "description": "Read agentic-vision doctrine and list viral-autopilot BoK"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # MCORCH — Agentic Vision (Doutrina AGI→ASI · lente vinculante de desenvolvimento)
> 
> > **Documento canônico load-bearing.** Toda SDD de módulo novo declara conformidade contra os **21 padrões agênticos** desta doutrina (ver CLAUDE.md §1 — *Pattern Conformance Declaration*). Este documento **substitui** `docs/architecture/system_architecture.md` como referência arquitetural viva.
> 
> | Campo | Valor |
> |---|---|
> | **Status** | Vivo (v1) · selado na malha como `documentation_suite` |
> | **Fontes** | `docs/Agentic-Design-Patterns.pdf` (Gulli, 482 pg — 21 padrões) · `docs/From AGI to ASI - 2606.12683.pdf` (DeepMind arXiv:2606.12683, 57 pg — 4 vias) |
> | **Síntese pai** | `.claude/context/agi-asi-via4-design-checklist.md` (nó malha `a576216e`) |
> | **ORO** | Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign |
> | **Criado** | 2026-06-26 |
> 
> ---
> 
> ## 1. Tese — onde estamos e para onde encaminhamos
> 
> O paper *From AGI to ASI* mapeia o avanço **pós-AGI** por **quatro vias não-exclusivas** (compõem, não só somam):
> 
> 1. **Via 1 — Escala** (compute + modelos + dados).
> 2. **Via 2 — Saltos de paradigma** (quebra algorítmica/arquitetural).
> 3. **Via 3 — Auto-aperfeiçoamento recursivo** (IA melhorando IA — o caminho "Singularidade").
> 4. **Via 4 — Formação de coletivo de agentes** (coordenação de muitos agentes especializados, governança central ou de mercado).
> 
> **O MCORCH é a Via 4 instanciada na camada de produto** — um coletivo de agentes especializados (Pantheon/Departmental Army + Knowledge Mesh + orquestração) **com o humano no comando** (ORO/HITL) — **e roda a Via 3 no micro**: o mandato **Obstáculo→Síntese** (CLAUDE.md §5) é *auto-aperfeiçoamento recursivo aplicado ao próprio processo de desenvolvimento* — todo obstáculo resolvido vira SOP+skill+agent, e o sistema melhora o próprio tooling.
> 
> **Calibração honesta (Lei 1):** o paper opera em escopo de **laboratório de fronteira** (treinar modelos, compute, energia). O MCORCH não é isso — é uma instanciação **fiel, em camada de produto**, dos padrões de desenho da Via 4 + Via 3-micro. Força declarada, não pretensão.
> 
> ### O gap estrutural (o que "antecipar o mercado" realmente significa)
> 
> O paper aponta como **aberto** justamente o que o MCORCH ainda não faz: respondemos as perguntas de coletivo de agentes **por doutrina, mas não *medimos* nenhuma** —
> 
> - valor marginal por agente adicionado ao fan-out (multi-agent scaling, V4-2);
> - custo (mco) por resultado, atribuído a "mais agentes" vs "modelo maior" (V4-4);
> - overhead de coordenação — hops/handoffs/retries por resultado (V4-5).
> 
> **Crescemos o coletivo no escuro.** Instrumentar isso é o fosso. A iniciativa flagship desta doutrina é o **Collective Efficiency Ledger** (§4 abaixo).
> 
> ---
> 
> ## 2. Pattern Maturity Ledger (21 padrões canônicos × MCORCH)
> 
> Maturidade: ✅ **Forte/Excelente** (doutrina sólida + artefato em produção) · 🟡 **Moderado/Parcial** (existe mas não-canônico/ad-hoc) · 🔴 **Fraco** (gap real).
> 
> | # | Padrão | Maturidade | Artefato MCORCH que o encarna | Gap aberto (→ OTD §3) |
> |---|--------|:--:|---|---|
> | 1 | **Prompt Chaining** | ✅ | `orchestrate-content`/`orchestrate-step` (pg_net), Workflow `pipeline()` | Sem validação JSON Schema entre steps (coerção manual de tipo) |
> | 2 | **Routing** | 🟡 | `llm-cascading-fallback` (provider Claude→GPT→Gemini), Vision-QA gate | Sem routing semântico por embedding para dispatch de agente |
> | 3 | **Parallelization** | ✅ | Workflow `parallel()` fan-out concorrente; `openrouter-swarm` | Sem timeout/circuit-break em straggler; sem backpressure |
> | 4 | **Reflection** | 🟡 | Vision-QA (`vision-qa.ts`), `mcorch-qa-healing` (verify adversarial) | Hard-coded por caso; sem framework Generator-Critic genérico |
> | 5 | **Tool Use** | ✅ | Vision MCP (`packages/vision-mcp-core/`), edge functions tipadas | Schemas autorados à mão; sem telemetria de tool (sucesso/latência) |
> | 6 | **Planning** | 🟡 | BoK suite (MRD→SDD), `deepsearch-blueprint`, `intent-plan-execution` | Plano pré-gerado; sem re-planejamento dinâmico na divergência |
> | 7 | **Multi-Agent** | ✅ | **Pantheon** (L1 Heads + L2 + main + guardian), OpenClaw squad | Sem protocolo inter-agente formal; sem debate de consenso |
> | 8 | **Memory Management** | ✅ | **Knowledge Mesh GraphRAG** (`mcorch_nodes/edges`, HNSW 768d, FSRS-6) | Short-term (janela) e long-term (grafo) sem estratégia de recall unificada |
> | 9 | **Learning & Adaptation** | 🔴 | Obstáculo→Síntese (manual), autopilot `optimization_policy` | **Sem loop de feedback fechado/RL formal; risco de reward de métrica única** |
> | 10 | **Model Context Protocol** | ✅ | Vision MCP (spec Anthropic, Streamable HTTP), `McpConnectorsCard` | Sem middleware de normalização de output; sem auto-schema de REST |
> | 11 | **Goal Setting & Monitoring** | 🟡 | `infra_health_logs` + watchdog, `sprint-priorities` (SMART) | Sem camada formal de spec de goal; loop monitor→feedback→replan ad-hoc |
> | 12 | **Exception Handling & Recovery** | ✅ | `infra_health_logs`, `rescue-video`, refund RPCs, watchdog, retry idempotente | Sem máquinas de estado de recovery explícitas (rollback DAGs) |
> | 13 | **Human-in-the-Loop** | ✅ | **ORO triplet** (`survival.md`), AskUserQuestion, GO Sovereign | Sem tracking de SLA de escalação; sem tag de expertise do reviewer |
> | 14 | **Knowledge Retrieval (RAG)** | ✅ | Knowledge Mesh (`match_mcorch_nodes`, `search-constellation`), MCP `mesh.search` | Resolução de contradição/reconciliação de fonte não-automatizada |
> | 15 | **Inter-Agent Comm. (A2A)** | 🟡 | Mesh bridge (`bridge-mesh-to-openclaw`/`distribute-mesh-to-agents`), Telegram, edges | Sem schema de Agent Card / protocolo de discovery formal |
> | 16 | **Resource-Aware Optimization** | ✅ | **mcoCoins** (`deduct_mco_coins` atômico), calibração 4×-floor, caps Vision MCP | Sem reserva preditiva de recurso / gestão proativa de quota |
> | 17 | **Reasoning Techniques** | 🟡 | deepsearch (Gemini grounding), `analyze-node`, Workflow judge-panel/loop-until-dry | Sem Graph-of-Thought formal / framework de agente de reflexão |
> | 18 | **Guardrails / Safety** | ✅ | **Survival Laws**, **Cyber-Sentinel** (`_shared/sentinel.ts` pt-BR+EN), RLS default-deny, BoK Gate, ES256 JWT | Sem suíte de eval adversarial / regressão de jailbreak no CI |
> | 19 | **Evaluation & Monitoring** | 🟡 | `mcorch-qa-healing` (Fase 5c), Vision QA, `audit-schema-drift`, e2e-user-zero | Sem rubricas de avaliação padronizadas / dashboard contínuo de métricas |
> | 20 | **Prioritization** | 🟡 | `sprint-priorities`, ledger OTD/RPN (FMEA), gates de recusa Survival | Sem álgebra de priorização formal / scheduler (risco de starvation) |
> | 21 | **Exploration & Discovery** | 🟡 | `fetch-trends`/`vm_trends` (autopilot angle), `deepsearch-blueprint`, OpenClaw Dreaming | Sem torneio de ranking (Elo) / loop de debate multi-agente; exploração reativa, não generativa |
> 
> > **Apêndice F (Reasoning Engines)** — presente (Vision MCP multimodal, streaming Workflow); gap: SLA de latência + semântica de rollback de output streamado não formalizados. Não conta como padrão numerado.
> 
> **Placar:** ✅ **11 fortes** · 🟡 **9 moderados** · 🔴 **1 fraco**. A fundação (Guardrails + Memory + Multi-Agent + Resource-Aware + Tool/MCP + HITL) é robusta; os gaps são majoritariamente de **canonização** (formalizar o que já fazemos ad-hoc) e **instrumentação** (medir), não de arquitetura ausente. A exceção real é **Learning & Adaptation** — o elo recursivo (Via 3) ainda é manual.
> 
> ---
> 
> ## 3. Backlog priorizado de canonização (gaps → OTDs nomeados)
> 
> Os gaps **não viram código já** — viram dívida técnica rastreável (OTD). Prioridade pela tese: o que destrava medir o coletivo primeiro.
> 
> | OTD | Padrão | Iniciativa | Prioridade |
> |---|---|---|---|
> | **OTD-AG-001** | 9·11·16 | **Collective Efficiency Ledger** — instrumentar valor marginal/agente, mco/resultado, overhead de coordenação (V4-2/4/5). **Flagship desta doutrina** (§4). | 🔴 P0 |
> | OTD-AG-002 | 9 | Fechar o loop **Learning & Adaptation** — feedback estruturado autopilot→policy com reward **multi-métrica** (anti-Goodhart) | 🔴 P0 |
> | OTD-AG-003 | 4 | Framework **Generator-Critic** genérico (reflexão reutilizável, crítico de persona distinta) | 🟡 P1 |
> | OTD-AG-004 | 19 | **Rubricas de avaliação** padronizadas + dashboard contínuo (LLM-judge + amostra humana) | 🟡 P1 |
> | OTD-AG-005 | 6·11 | **Re-planejamento dinâmico** — plano revisado na divergência de execução (monitor→replan) | 🟡 P1 |
> | OTD-AG-006 | 15 | **Agent Card** formal + protocolo de discovery (A2A schema-ado) | 🟡 P2 |
> | OTD-AG-007 | 2 | **Routing semântico** por embedding para dispatch de agente/modelo | 🟡 P2 |
> | OTD-AG-008 | 21 | **Torneio de exploração** (Elo) — hipótese→crítico→ranqueador→evolução | 🟢 P3 |
> | OTD-AG-009 | 18 | Regressão de **jailbreak adversarial** no CI (Cyber-Sentinel) | 🟢 P3 |
> | OTD-AG-010 | 12 | Máquinas de estado de **recovery** explícitas (rollback DAG) | 🟢 P3 |
> 
> ---
> 
> ## 4. Iniciativa flagship — Collective Efficiency Ledger (OTD-AG-001)
> 
> A resposta material ao gap estrutural. **Design VIEW-sobre-verdade-financeira** (resiste a Goodhart — ninguém escreve *para* o ledger; é derivado do que já é cobrado/refundado). Mede o **coletivo in-system** (pipelines edge + ciclos autopilot + crons Pantheon) onde mco-cost e nós da malha já existem.
> 
> - **Primeira métrica computável já (V4-4):** mco actual ÷ criativos entregues (`autopilot_cycles.spend_mco − refunded_mco`).
> - **Parcial (V4-5):** overhead via `pipeline_runs.steps` + emits `collective_retry`/`collective_hop` em `infra_health_logs`.
> - **Deferido a experimento real (V4-2):** valor marginal/agente — **não fabricar proxy gameável** (alerta do próprio paper). Só mede quando houver A/B real de largura de fan-out.
> 
> Detalhe de implementação em `docs/bok/agentic-governance/` (SSOT) + SOP `docs/processes/collective-efficiency-ledger.md`.
> 
> ---
> 
> ## 5. Princípios de design (todo módulo novo segue)
> 
> 1. **Material-proof na avaliação** — sucesso ancorado em artefato físico (Lei 1); avaliação não-declarada (Vision QA / mcorch-qa-healing).
> 2. **Defense-in-depth de guardrails** — Survival Laws + Sentinel + RLS default-deny + BoK Gate; nunca camada única.
> 3. **Loop de feedback fechado** — toda automação que produz resultado deve poder medir se o resultado melhorou (anti-Via-3-cega).
> 4. **Reuso do chokepoint de telemetria** — emitir em `infra_health_logs` (sem PII/segredos), não criar write-sites paralelos.
> 5. **Multi-tenant-correto desde o dia 1** — `security_invoker` VIEW sobre bases SELECT-own; agregado cross-tenant = service-role-only.
> 6. **Anti-Goodhart** — métrica derivada de verdade financeira, não auto-reportada; deferir o que só medível por experimento.
> 7. **Humano no comando em velocidade supra-humana** — quando o coletivo produz mais artefatos do que o Sovereign consome, exigir digest em camadas (Guardian briefing) + bounded autonomy por domínio (Pantheon decision scope).
> 
> ---
> 
> ## 6. Conexão com a governança existente
> 
> | Protocolo | Papel na visão |
> |---|---|
> | **MCORCH Master Execution Protocol** (CLAUDE.md) | BoK Gate + Obstáculo→Síntese = Via 3-micro (recursão do processo). Agora carrega o **Pattern Conformance Gate**. |
> | **Survival Laws** (`survival.md`) | Materialidade + ORO = a oversight scalable que o paper aponta como faltante. Anti-alucinação universal (humano e agente). |
> | **Pantheon Role Matrix** | Via 4 instanciada — escopo bounded por BoK lens; escalação explícita a main/Sovereign. |
> | **API Tenancy (per-user)** | Segregação de credencial/quota = segurança governance-grade para coletivo multi-tenant. |
> 
> ---
> 
> *"MATE A POESIA. ENTREGUE ENGENHARIA." — a doutrina existe para que o coletivo cresça medido, não no escuro.*
> === END agentic-vision ===
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> ```

## 🤖 Claude *(23:15:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat supabase/migrations/20260626120000* 2>/dev/null; echo \"=== END ledger migration ===\"",
  "description": "Read Collective Efficiency Ledger migration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -- Migration: Collective Efficiency Ledger — VIEW + cross-tenant rollup RPC (FR-AG-001/002).
> -- BoK SSOT: docs/bok/agentic-governance/05-sdd.md §7 (migration stub) + 06-data-model.md.
> -- SOP (Lei 2): docs/processes/collective-efficiency-ledger.md. Doctrine: docs/architecture/agentic-vision.md §4.
> --
> -- WHY: the "From AGI to ASI" paper flags the multi-agent-collective questions (V4-2/4/5) as OPEN. MCORCH answers
> -- them by doctrine but does NOT MEASURE any. This instruments the IN-SYSTEM collective (orchestrate-content runs +
> -- autopilot cycles) by DERIVING efficiency from financial truth that already exists — zero new write-path, no
> -- self-reported number (anti-Goodhart, DD-AG-001/004).
> --
> -- SECURITY (the two material risks — FM-AG-001 / FM-AG-007):
> --   * VIEW is `security_invoker = on` → the underlying RLS (pipeline_runs/autopilot_cycles are SELECT-own) is
> --     evaluated AS THE CALLER. An `authenticated` user sees ONLY their own rows (G6: count cross-tenant = 0).
> --   * The cross-tenant rollup is for the Sovereign's SCALE decision (DD-AG-006) → SECURITY DEFINER + search_path=''
> --     + REVOKE PUBLIC/anon/authenticated + GRANT service_role (mirrors 20260603220000_secure_ledger_rpcs.sql).
> -- Additive + read-only (VIEW/RPC, no table, no write-path) ⇒ ZERO impact on existing writers. No PII introduced.
> -- Passes /security-review before commit (NFR-AG-004 / FMEA-011).
> 
> -- ── VIEW per-tenant (RLS herdada via security_invoker — DD-AG-002 / FR-AG-001) ──────────────────────────────────
> CREATE OR REPLACE VIEW public.collective_efficiency_ledger
>   WITH (security_invoker = on) AS
>   SELECT pr.id                                                        AS run_id,
>          'orchestrate-content'::text                                  AS collective_type,
>          pr.user_id                                                   AS user_id,
>          COALESCE(jsonb_array_length(pr.steps), 0)                    AS n_units,
>          pr.mco_cost                                                  AS mco_projected,
>          pr.mco_cost                                                  AS mco_actual,
>          pr.status                                                    AS result_status,
>          (pr.status IN ('done'))                                      AS succeeded,
>          (EXTRACT(EPOCH FROM (pr.completed_at - pr.started_at)) * 1000)::bigint AS wall_clock_ms,
>          pr.started_at                                                AS started_at
>   FROM public.pipeline_runs pr
>   UNION ALL
>   SELECT ac.id,
>          'autopilot-cycle'::text,
>          ac.user_id,
>          ac.planned_units,
>          ac.spend_mco,
>          (ac.spend_mco - ac.refunded_mco),
>          ac.status,
>          (ac.status IN ('completed')),
>          (EXTRACT(EPOCH FROM (ac.completed_at - ac.started_at)) * 1000)::bigint,
>          ac.started_at
>   FROM public.autopilot_cycles ac;
> 
> COMMENT ON VIEW public.collective_efficiency_ledger IS
>   'Collective Efficiency Ledger (agentic-governance FR-AG-001). Per-tenant DERIVED view (security_invoker=on → '
>   'inherits SELECT-own RLS of pipeline_runs/autopilot_cycles). One row per collective run: n_units, mco_projected, '
>   'mco_actual (spend-refund for cycles), succeeded, wall_clock_ms. Anti-Goodhart: derived from financial truth, '
>   'never written to. SOP docs/processes/collective-efficiency-ledger.md.';
> 
> -- ── RPC agregado cross-tenant (service-role-only — DD-AG-006 / FR-AG-002 / FM-AG-007) ───────────────────────────
> -- The Sovereign's scale decision needs the WHOLE collective, across tenants. SECURITY DEFINER runs as the function
> -- owner (RLS-bypassing) so it sees all tenants; access is hard-revoked from anon/authenticated and granted ONLY to
> -- service_role. retry_rate joins the agentic-governance 'collective_retry' overhead events (FR-AG-003).
> CREATE OR REPLACE FUNCTION public.collective_efficiency_rollup()
>   RETURNS TABLE (
>     collective_type    text,
>     runs               bigint,
>     avg_mco_actual     numeric,
>     avg_wall_clock_ms  numeric,
>     retry_rate         numeric
>   )
>   LANGUAGE sql
>   STABLE
>   SECURITY DEFINER
>   SET search_path = ''
> AS $$
>   WITH retries AS (
>     SELECT (metadata->>'run_id')::uuid AS run_id
>     FROM public.infra_health_logs
>     WHERE service = 'agentic-governance' AND event = 'collective_retry'
>     GROUP BY 1
>   )
>   SELECT l.collective_type,
>          count(*)                                                                       AS runs,
>          avg(l.mco_actual)::numeric                                                      AS avg_mco_actual,
>          avg(l.wall_clock_ms)::numeric                                                   AS avg_wall_clock_ms,
>          (count(*) FILTER (WHERE r.run_id IS NOT NULL))::numeric / NULLIF(count(*), 0)   AS retry_rate
>   FROM public.collective_efficiency_ledger l
>   LEFT JOIN retries r ON r.run_id = l.run_id
>   GROUP BY l.collective_type;
> $$;
> 
> REVOKE ALL    ON FUNCTION public.collective_efficiency_rollup() FROM PUBLIC, anon, authenticated;
> GRANT  EXECUTE ON FUNCTION public.collective_efficiency_rollup() TO service_role;
> 
> COMMENT ON FUNCTION public.collective_efficiency_rollup() IS
>   'Cross-tenant aggregate of the Collective Efficiency Ledger (FR-AG-002). SECURITY DEFINER service-role-only — the '
>   'scale decision is the Sovereign''s, not the tenant''s (DD-AG-006). Returns avg mco_actual / wall_clock_ms / '
>   'retry_rate per collective_type, ALL tenants. Never reachable by anon/authenticated (FM-AG-007).';
> === END ledger migration ===
> ```

## 🤖 Claude *(23:15:39)*

Now let me read the survey artifacts: the Obstacle→Synthesis mandate context, OpenClaw Dreaming, ab_variants in viral-autopilot BoK, and creative_metrics schema.

## 🤖 Claude *(23:15:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/skills/openclaw-dreaming/SKILL.md 2>/dev/null | head -120; echo \"=== END dreaming SKILL ===\"",
  "description": "Read OpenClaw Dreaming skill"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---
> name: openclaw-dreaming
> description: Diagnosticar, ajustar e RECUPERAR o subsistema de Dreaming/memória do OpenClaw — promoção para MEMORY.md, dream diary (DREAMS.md), Memory Palace + Imported Insights (wiki). Use quando o painel claw.gcrux.com/dreaming mostrar "0 promovido", Palace/Insights congelados/desatualizados, ou ao tunar gates de promoção e o provider de embedding da memória. Doc oficial: https://docs.openclaw.ai/pt-BR/concepts/dreaming. Sibling: openclaw-gateway-ops (gateway/modelos).
> ---
> 
> # Skill: openclaw-dreaming — Memória, Promoção & Recovery do Dreaming
> 
> Playbook operacional do Dreaming do OpenClaw. Domínio distinto do gateway:
> aqui é **consolidação de memória de longo prazo**, não processo/porta.
> Doc autoritativa: https://docs.openclaw.ai/pt-BR/concepts/dreaming.
> 
> ## ⚠️ Modelo mental (correções que custaram caro)
> 
> **1. Dreaming = UMA varredura, NÃO 3 jobs separados.** `frequency` (cron, default `0 3 * * *`) dispara 1 sweep com 3 fases INTERNAS sequenciais (light→REM→deep). O schema `dreaming.phases.{light,deep,rem}` tem `enabled`/`limit`/gates, **NÃO** `cron`/`time` por fase → impossível distribuir tipo sono humano nativamente.
> - **"LEVE/PROFUNDO/REM 3:00" na UI = horário do CLOCK da próxima varredura (03:00), NÃO countdown de 3 min.**
> - A distribuição real (Light 03 / Deep 05 / REM 07 BRT) são os **mcorch circadian crons** (`nightly-stage1/2/3` no crontab SO) — OUTRO sistema, separado do dreaming nativo.
> 
> **2. As 3 fases (só Deep promove):**
> | Fase | Faz | Escreve MEMORY.md? |
> |------|-----|--------------------|
> | Light | ingere recall recente, dedup, prepara candidatos | ❌ |
> | Deep | rankeia candidatos + gates → promove | ✅ (única) |
> | REM | padrões/temas → DREAMS.md (dream diary) | ❌ |
> 
> **3. DOIS subsistemas distintos** (não confundir):
> - **memory-core** → dreaming, MEMORY.md (promoção), DREAMS.md (diário). CLI `memory *`.
> - **memory-wiki** → Memory Palace (syntheses) + Imported Insights (clusters). É o que a UI `/dreaming` mostra como Palace/Insights. **Clustering depende de embeddings.**
> 
> ## 🔑 Dependência crítica: EMBEDDINGS
> 
> Tudo (clustering do Palace/Insights + scoring de promoção) depende de embeddings funcionais.
> - ✅ **Atual: `gemini-embedding-001`** (`memorySearch.provider=gemini`, 768d via outputDimensionality). Funciona com a key Google.
> - ❌ Default era OpenAI `text-embedding-3-small` → **403 "project access revoked"** → Palace/Insights congelam (ingest copia arquivo OK, mas síntese/cluster falha) + promoção degrada.
> - Embedding LOCAL (`embeddinggemma-300m`) existe mas precisa `node-llama-cpp` (ausente).
> 
> ## Deep phase — ranking ponderado + gates
> 
> Pesos (doc): Relevance **0.30** · Frequency 0.24 · QueryDiversity 0.15 · Recency 0.15 · Consolidation 0.10 · Conceptual 0.06.
> Gates (`dreaming.phases.deep`): `minScore` · `minRecallCount` · `minUniqueQueries` (TODOS devem passar).
> **Atual:** `minScore=0.5 · minRecallCount=0 · minUniqueQueries=1` (afrouxado p/ recovery). Diary/report NÃO promovem (só grounded memory snippets).
> 
> ## Fase 1 — Diagnóstico (read-only)
> 
> ```bash
> OC="node /home/ubuntu/openclaw/openclaw.mjs"
> $OC memory status --agent=main      # Provider, chunks, Dirty, Dreaming gates, Recall store (N promoted), Batch failures
> $OC memory status --deep            # thresholds de gating
> $OC memory promote                  # preview do ranking de candidatos (não escreve)
> $OC memory promote-explain "topico" # por que um candidato falhou no score
> $OC memory rem-harness --agent=main # dry-run: reflections + deep candidates (não escreve)
> ```
> **Sinais saudáveis:** Provider=gemini · Batch failures 0/N (não 403) · Recall store com `promoted > 0` crescendo · Dirty: no.
> 
> ## Fase 2 — "0 promovido" / Palace congelado: causa-raiz
> 
> 1. **Embeddings 403?** → `memory status` mostra Batch failures + log gateway `embeddings failed: 403`. **Fix:** `memorySearch.provider=gemini` (Fase 3).
> 2. **Gates inalcançáveis?** → `rem-harness` mostra maxScore < minScore, ou recallCount=0 vs minRecallCount≥1. **Chicken-and-egg:** recall só registra com search funcionando; se embeddings estavam quebrados, o backlog tem `recalls=0` permanente.
> 3. **Palace/Insights (wiki) só atualiza no compile cycle** — regenera no sweep/bridge quando embeddings funcionam. Dados brutos preservados em `~/.openclaw/wiki/main/sources/` (mesmo durante freeze).
> 4. **"blocked" na UI** (≠ "ativo")? → Heartbeat do agente default deve estar enabled + destination ≠ `none`.
> 
> ## Fase 3 — Recovery (config patch validado)
> 
> ```bash
> OC="node /home/ubuntu/openclaw/openclaw.mjs"
> # Backup + patch SEMPRE validado contra schema (dry-run primeiro):
> cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%s)
> $OC config patch --file <patch.json5> --dry-run   # depois sem --dry-run
> systemctl --user restart openclaw-gateway.service  # config só relê no boot (NUNCA pm2/openclaw gateway restart — ver openclaw-gateway-ops)
> ```
> 
> | Sintoma | Patch / Ação |
> |---------|--------------|
> | Embeddings 403 | `agents.defaults.memorySearch = {provider:"gemini", model:"gemini-embedding-001", outputDimensionality:768}` → restart → `memory index --agent=<id>` ×6 agentes |
> | Gates muito altos | `plugins.entries.memory-core.config.dreaming.phases.deep = {minScore:0.5, minRecallCount:0, minUniqueQueries:1}` |
> | Backlog (período congelado, recalls=0) | **Canônico:** `memory rem-backfill --stage-short-term --path <dir>` (stage candidates, reversível `--rollback`). **OU** minRecallCount=0 + rodar promoção: `$OC cron run cb6df4a5-9678-4c9b-a388-24b97e4bf463` (várias vezes; promove top-N por score/ciclo) |
> | Sweep no horário errado | `dreaming.timezone="America/Sao_Paulo"` (servidor já é BRT, mas explícito é higiene) |
> | Diário UI vazio | `memory rem-backfill --path <dir>` (escreve REM summaries grounded no DREAMS.md) |
> 
> ## Fase 4 — Materialidade (Lei 1)
> 
> Toda claim de "recuperado/promovendo" exige:
> - `memory status` mostrando Provider=gemini + Batch failures 0 + `promoted` count **delta** (ex: 3→8)
> - `cron run <id>` → run jsonl com `status=ok model=...`
> - Palace/Insights na UI: confirmação VISUAL no `claw.gcrux.com/dreaming` (regenera no sweep 03:00 BRT — não dá pra forçar via comando único)
> - NUNCA afirmar "promovido N" sem o count real do `memory status`.
> 
> ## Config reference — `plugins.entries.memory-core.config.dreaming`
> 
> `enabled` (bool) · `frequency` (cron, `0 3 * * *`) · `timezone` · `model` (Dream Diary subagent override; default runtime = qwen3-235b) · `phases.light` (lookbackDays/limit/dedupeSimilarity) · `phases.deep` (limit/minScore/minRecallCount/minUniqueQueries/recencyHalfLifeDays/maxAgeDays) · `phases.rem` (lookbackDays/limit/minPatternStrength) · `storage.mode` (inline/separate/both).
> 
> Cron nativo `Memory Dreaming Promotion` (id `cb6df4a5-...` em `~/.openclaw/cron/jobs.json`) reflete os gates do deep na sua descrição.
> 
> ## Ver também
> - **openclaw-gateway-ops** — gateway/supervisor/modelos/fallback (sibling)
> - Memória `project_openclaw_ollama_integration.md` — fatos cross-conversation
> - Doc oficial: https://docs.openclaw.ai/pt-BR/concepts/dreaming
> === END dreaming SKILL ===
> ```

## 🤖 Claude *(23:15:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"ab_variant\\|ab_test\\|A/B\\|variant\\|reward\\|optimization_policy\\|FR-VA-010\\|FR-VA-018\" docs/bok/viral-autopilot/04-frd.md docs/bok/viral-autopilot/06-data-model.md 2>/dev/null | head -60; echo \"=== END frd/datamodel grep ===\"",
  "description": "Grep ab_variants and reward/policy refs in viral-autopilot BoK"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> docs/bok/viral-autopilot/04-frd.md:14:**In scope (MVP+v1.0):** entidade de plano de cadência; cron de disparo recorrente por-tenant; geração product-aware monetizada em todo formato (texto+imagem); coletor de desempenho unificado (cliques+orgânico+receita); analisador de ciclo + reinjeção de aprendizado; guarda de custo (teto + kill-switch); dashboard de ROI por criativo; seleção de produto por comissão+trend; ângulo informado por trends; geração A/B de variantes; gate HITL opcional.
> docs/bok/viral-autopilot/04-frd.md:31:| FR-VA-002 | Cycle dispatcher | Edge fn `autopilot-run`: valida plano, aplica gate de custo (FR-VA-007/021), seleciona produto(s), abre `autopilot_cycles`, e faz fan-out product-aware para `orchestrate-content` (**1 dispatch por produto×rede×variante** — `N_runs = produtos × redes × ab_variants`, casando com o pré-débito FR-VA-007). Reusa o padrão de `campaign-run`. | Critical | PR-VA-002, PR-VA-001 | EdgeFunction | AT-VA-002 |
> docs/bok/viral-autopilot/04-frd.md:33:| FR-VA-004 | Monetize all formats | `monetizeContent` (`_shared/affiliate.ts`) roda em artigo **+ LinkedIn + Twitter**, embutindo link ML per-user por criativo (não só no artigo, não por regex de 3 SKUs). **`content_variant_id` = o `id` da linha de `content_library` daquele criativo**; grava `affiliate_links.content_id = content_variant_id` (hoje gravado `null`) e embute o `content_variant_id` no link rastreável → habilita atribuição por peça (FR-VA-017). | Critical | PR-VA-002 | Lib | AT-VA-004 |
> docs/bok/viral-autopilot/04-frd.md:36:| FR-VA-007 | Cost guardrail (kill-switch, atômico) | Custo projetado = **`N_runs × ORCHESTRATION_RUN(10) + ANALYZE_COST(2)`**, onde **`N_runs = |target_product_ids| × |platforms| × ab_variants`** (cada `orchestrate-content` é bundle flat de 10 que **já inclui imagem** — `billing.ts:16-21`; `ab_variants` default 1). Se `projetado > budget_cap_mco` OU `saldo < projetado/min_balance` → aborta (`aborted_budget` 409 / `insufficient_balance` 402), pausa o plano, notifica — **sem deduzir**. Atomicidade: `autopilot-run` faz **UM `deduct_mco_coins(user_id, projetado)` ANTES do fan-out** (pré-pago, `debited_at`); sub-runs em modo `prepaid` (sem self-bill); ao fechar, **`finalize_autopilot_cycle(cycle_id, actual)`** (RPC SECURITY DEFINER service-role-only, idempotente por `refunded_at IS NULL`) **credita o não-usado** `(projetado − actual)` no `mco_balance` na MESMA transação (espelha `finalize_vision_job`). **Refund é crédito positivo — NUNCA `deduct` negativo** (`deduct_mco_coins` rejeita `p_amount<=0`, migration `20260603220000:45`). Resolve TOCTOU. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |
> docs/bok/viral-autopilot/04-frd.md:38:| FR-VA-009 | Unified creative metrics | Tabela `creative_metrics` keyed por `content_variant_id`: affiliate_clicks, impressions, engagements, revenue_cents, source, collected_at. Unifica os 3 sinais (Decisão 3). | High | PR-VA-004 | DB | AT-VA-009 |
> docs/bok/viral-autopilot/04-frd.md:39:| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role): deriva o tenant de `previous_cycle_id` (`SELECT user_id FROM autopilot_cycles` — **nunca do body**); lê `creative_metrics` do ciclo anterior; se vazio, usa baseline (`has_real_data=false`, NÃO inventa) e **não cobra** (log `analyze_empty`); se há dado, produz `optimization_policy` estruturado (top hook/produto/horário/formato) e cobra **2 mco** (`ANALYZE_COST`, 4×-floor — SOP `mcoin-cost-calibration`). **Encadeado pós-ciclo pelo `autopilot-cadence-cron`** (inline, sem cron próprio). | High | PR-VA-005 | EdgeFunction | AT-VA-010 |
> docs/bok/viral-autopilot/04-frd.md:40:| FR-VA-011 | Feedback injection | A geração (`orchestrate-step`/`autopilot-run`) LÊ o `optimization_policy` mais recente do tenant e injeta as features no system prompt do próximo ciclo. Fecha a quebra "saída sem consumo". | Critical | PR-VA-005 | Lib/EdgeFunction | AT-VA-011 |
> docs/bok/viral-autopilot/04-frd.md:46:| FR-VA-017 | Revenue attribution per creative | `handle-ml-postback` credita `revenue_cents` na `affiliate_links` cujo `content_id = content_variant_id` (FR-VA-004); o coletor (FR-VA-008) reflete em `creative_metrics` por `content_variant_id`. Caminho: postback → `order_id`/`click_id` → `affiliate_links.content_id` → criativo. Depende de OTD-VA-007 (secret per-user). | High | PR-VA-004, PR-VA-007 | EdgeFunction | AT-VA-017 |
> docs/bok/viral-autopilot/04-frd.md:47:| FR-VA-018 | Trend-informed angle | `autopilot-run` lê `vm_trends` (de `fetch-trends`) para pautar o ângulo viral do ciclo (reconecta a ilha de trends). Texto de trend é **fonte não-confiável** → sanitizado antes do prompt (NFR-VA-008). | High | PR-VA-011 | EdgeFunction | AT-VA-018 |
> docs/bok/viral-autopilot/04-frd.md:48:| FR-VA-019 | A/B variant generation | Gera N variantes por criativo por ciclo (config no plano); a vencedora é escolhida pelo desempenho do ciclo anterior (`creative_metrics`) e promovida no próximo. Reusa a geração; sob o mesmo teto de custo (FR-VA-007). | Should (v1.0) | PR-VA-012 | EdgeFunction | AT-VA-019 |
> docs/bok/viral-autopilot/04-frd.md:61:| FR-VA-023 | Product-aware 9:16 composition | Em `orchestrate-step`, quando `video_enabled`, monta uma **composição HTML 1080×1920** a partir do produto-alvo (imagem do produto — reusa o asset de FR-VA-013 — + gancho viral + caption + CTA + branding) usando um **template de short determinístico**. As 3 fontes não-confiáveis (nome/desc de produto, texto de trend FR-VA-018, `optimization_policy` FR-VA-011) são **sanitizadas/escapadas** antes de entrar no HTML (NFR-VA-008 + Cyber-Sentinel fail-closed, espelha `orchestrate-content:92`). | High | PR-VA-020 | Lib/EdgeFunction | AT-VA-023 |
> docs/bok/viral-autopilot/04-frd.md:63:| FR-VA-025 | Async asset reconciliation + attach | Render é assíncrono e **pode chegar depois** do `finalize_autopilot_cycle`. Reconciliação **event-driven no próprio worker** (OTD-VA-014 — sem cron novo): no `done`, se a render carrega `composition.autopilot`, o worker lê `storage_key` (asset ≥ 100KB) e **anexa** o vídeo: `content_library` linha `type='video'` (`media_url` = path durável no bucket privado `video-studio-assets`) + 1 linha `creative_metrics` (`source='organic'`, keyed pelo `content_variant_id` = id da nova linha, FR-VA-009). Falha de render = **fail-open `skipped`** + `finalize_video_render(failed, refund=VIDEO_COST)` (espelha Fatia 1b). Renders genéricos (editor) sem `autopilot` não anexam. | High | PR-VA-020 | Worker/EdgeFunction | AT-VA-025 |
> docs/bok/viral-autopilot/04-frd.md:80:| NFR-VA-007 | Auditability | Todo post autônomo rastreável a `cycle_id`+`plan_id`+`product`+`content_variant_id` | 100% | SELECT join `scheduled_posts`↔`autopilot_cycles` |
> docs/bok/viral-autopilot/04-frd.md:138:**Response (200):** `{ status: "ok", optimization_policy_id: string, has_real_data: boolean, top_features: {...} }`  
> docs/bok/viral-autopilot/04-frd.md:152:| `creative_metrics.content_variant_id` | `uuid` | NOT NULL | **= `content_library.id`** do criativo (**referência lógica — sem FK física**, p/ retenção independente: métricas vivem 18m mesmo se o conteúdo for podado, §7); nasce na geração (1 linha de `content_library` por criativo) e é propagado a `affiliate_links.content_id` (FR-VA-004) e ao link rastreável | — |
> docs/bok/viral-autopilot/04-frd.md:165:| FR-VA-004 | ✅ | ✅ | ✅ | link ML + `content_variant_id` em TODO formato |
> docs/bok/viral-autopilot/04-frd.md:170:| FR-VA-009 | ✅ | — | — | unicidade por `content_variant_id`+`source` |
> docs/bok/viral-autopilot/04-frd.md:171:| FR-VA-010 | ✅ | ✅ | — | baseline quando vazio (`has_real_data=false`) |
> docs/bok/viral-autopilot/04-frd.md:178:| FR-VA-017 | ✅ | ✅ | — | atribuição por `content_variant_id` (gated em OTD-VA-007) |
> docs/bok/viral-autopilot/04-frd.md:179:| FR-VA-018 | ✅ | ✅ | — | ângulo lê `vm_trends`; sanitização de fonte externa |
> docs/bok/viral-autopilot/04-frd.md:180:| FR-VA-019 | ✅ | ✅ | — | N variantes; seleção por desempenho; custo × ab_variants |
> docs/bok/viral-autopilot/04-frd.md:199:| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |
> docs/bok/viral-autopilot/04-frd.md:204:| PR-VA-011 | FR-VA-018 | — |
> docs/bok/viral-autopilot/06-data-model.md:15:       │ (references)               │ (cycle_id on)                │ (content_variant_id)
> docs/bok/viral-autopilot/06-data-model.md:27:- **creative_metrics:** desempenho por criativo (`content_variant_id`), unificando cliques de afiliado + engajamento orgânico + receita de postback (Decisão 3).
> docs/bok/viral-autopilot/06-data-model.md:30:- **affiliate_links / optimization_policy / content_library / mcorch_nodes (reuse):** receita, política de melhoria, conteúdo, memória.
> docs/bok/viral-autopilot/06-data-model.md:52:| `ab_variants` | `int` | NOT NULL | `1` | — | Nº de variantes A/B por criativo (FR-VA-019); 1 = sem A/B |
> docs/bok/viral-autopilot/06-data-model.md:84:| `content_variant_id` | `uuid` | NOT NULL | — | ref. lógica → `content_library.id` (sem FK física) | Criativo medido (= a linha de `content_library`; sem FK p/ retenção independente §7; propagado a `affiliate_links.content_id`) |
> docs/bok/viral-autopilot/06-data-model.md:93:| — | — | — | — | — | **UNIQUE (content_variant_id, source)** |
> docs/bok/viral-autopilot/06-data-model.md:134:CREATE INDEX creative_metrics_variant_idx ON public.creative_metrics (content_variant_id);
> docs/bok/viral-autopilot/06-data-model.md:204:| `creative_metrics` | `(content_variant_id, source)` | UNIQUE (upsert por fonte) | — |
> === END frd/datamodel grep ===
> ```

## 🤖 Claude *(23:15:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rln \"ab_variant\\|creative_metrics\\|optimization_policy\\|reward\" supabase/migrations/ 2>/dev/null | head; echo \"=== files ===\"; echo \"--- creative_metrics schema ---\"; grep -rn \"creative_metrics\\|optimization_policy\\|ab_variant\" supabase/migrations/*viral_autopilot* supabase/migrations/*creative* 2>/dev/null | head -40",
  "description": "Find creative_metrics and ab_variants schema in migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql
> supabase/migrations/20260620120100_viral_autopilot_cycles.sql
> supabase/migrations/20260620120000_viral_autopilot_plans.sql
> supabase/migrations/20260624140000_autopilot_video_enqueue_refund.sql
> supabase/migrations/20260622040000_video_studio_renders_and_assets.sql
> supabase/migrations/20260414150946_850633b4-d676-428c-b2c1-8d0aa8fca4d0.sql
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql
> === files ===
> --- creative_metrics schema ---
> supabase/migrations/20260620120100_viral_autopilot_cycles.sql:13:-- UNIQUE(id,user_id) anchors the composite FK from creative_metrics (closed at the end of this file).
> supabase/migrations/20260620120100_viral_autopilot_cycles.sql:55:-- ── Close the deferred composite FK from creative_metrics (Fatia 1 left cycle_id NULL-able, NO FK) ──────────────
> supabase/migrations/20260620120100_viral_autopilot_cycles.sql:63:    SELECT 1 FROM pg_constraint WHERE conname = 'creative_metrics_cycle_fk'
> supabase/migrations/20260620120100_viral_autopilot_cycles.sql:65:    ALTER TABLE public.creative_metrics
> supabase/migrations/20260620120100_viral_autopilot_cycles.sql:66:      ADD CONSTRAINT creative_metrics_cycle_fk FOREIGN KEY (cycle_id, user_id)
> supabase/migrations/20260620120000_viral_autopilot_plans.sql:15:--     floor [1 run 10 + analyze 2], ab_variants 1-5) materialize the §6 Data Quality rules at the DB layer.
> supabase/migrations/20260620120000_viral_autopilot_plans.sql:32:  ab_variants        int         NOT NULL DEFAULT 1   CHECK (ab_variants BETWEEN 1 AND 5),
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:1:-- Migration: viral-autopilot creative_metrics — canonical per-creative performance ledger (FR-VA-009).
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:2:-- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md (creative_metrics) + 04-frd.md (FR-VA-009 unified
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:23:CREATE TABLE IF NOT EXISTS public.creative_metrics (
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:42:  CONSTRAINT creative_metrics_variant_source_uniq UNIQUE (content_variant_id, source)
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:45:ALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:49:CREATE POLICY "creative_metrics_select_own" ON public.creative_metrics
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:54:CREATE POLICY "creative_metrics_no_client_delete" ON public.creative_metrics
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:57:CREATE INDEX IF NOT EXISTS creative_metrics_variant_idx  ON public.creative_metrics (content_variant_id);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:58:CREATE INDEX IF NOT EXISTS creative_metrics_user_idx     ON public.creative_metrics (user_id, collected_at DESC);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:59:CREATE INDEX IF NOT EXISTS creative_metrics_cycle_idx    ON public.creative_metrics (cycle_id);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:60:CREATE INDEX IF NOT EXISTS creative_metrics_product_idx  ON public.creative_metrics (product_id);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:62:COMMENT ON TABLE public.creative_metrics IS
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:1:-- Migration: viral-autopilot creative_metrics — canonical per-creative performance ledger (FR-VA-009).
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:2:-- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md (creative_metrics) + 04-frd.md (FR-VA-009 unified
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:23:CREATE TABLE IF NOT EXISTS public.creative_metrics (
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:42:  CONSTRAINT creative_metrics_variant_source_uniq UNIQUE (content_variant_id, source)
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:45:ALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:49:CREATE POLICY "creative_metrics_select_own" ON public.creative_metrics
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:54:CREATE POLICY "creative_metrics_no_client_delete" ON public.creative_metrics
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:57:CREATE INDEX IF NOT EXISTS creative_metrics_variant_idx  ON public.creative_metrics (content_variant_id);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:58:CREATE INDEX IF NOT EXISTS creative_metrics_user_idx     ON public.creative_metrics (user_id, collected_at DESC);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:59:CREATE INDEX IF NOT EXISTS creative_metrics_cycle_idx    ON public.creative_metrics (cycle_id);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:60:CREATE INDEX IF NOT EXISTS creative_metrics_product_idx  ON public.creative_metrics (product_id);
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:62:COMMENT ON TABLE public.creative_metrics IS
> ```

## 🤖 Claude *(23:15:46)*

Let me read the creative_metrics table columns exactly, the optimization_policy structure, and the FR-VA-010 analyzer to ground the loop precisely.

## 🤖 Claude *(23:15:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '20,65p' supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql; echo \"=== END creative_metrics cols ===\"",
  "description": "Read creative_metrics column definitions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -- can never forge a metric for another tenant nor fabricate revenue. Financial table → RESTRICTIVE no-delete
> -- (clients cannot erase the ledger). Passes /security-review (FMEA-011 / FMEA-VA-001 cross-tenant family).
> 
> CREATE TABLE IF NOT EXISTS public.creative_metrics (
>   id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id            uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   cycle_id           uuid,                          -- reserved for the cadence Fatia (autopilot_cycles); NO FK yet
>   content_variant_id uuid        NOT NULL,          -- logical ref to content_library.id; NO physical FK (independent
>                                                     -- 18-month retention per Data Model §7 — content can be pruned
>                                                     -- while its performance history is retained for the loop)
>   product_id         text,                          -- = vm_affiliate_products.external_id (the featured product)
>   platform           text,                          -- wordpress | linkedin | twitter
>   source             text        NOT NULL DEFAULT 'organic'
>                        CHECK (source IN ('affiliate_click','organic','postback')),
>   impressions        int         NOT NULL DEFAULT 0 CHECK (impressions      >= 0),
>   engagements        int         NOT NULL DEFAULT 0 CHECK (engagements      >= 0),
>   affiliate_clicks   int         NOT NULL DEFAULT 0 CHECK (affiliate_clicks >= 0),
>   revenue_cents      int         NOT NULL DEFAULT 0 CHECK (revenue_cents    >= 0),
>   collected_at       timestamptz NOT NULL DEFAULT now(),
>   created_at         timestamptz NOT NULL DEFAULT now(),
>   -- One row per (creative, signal source): the baseline 'organic' row at generation, later upserted by the
>   -- collector; 'affiliate_click' and 'postback' rows are written by their own writers (click ledger / postback).
>   CONSTRAINT creative_metrics_variant_source_uniq UNIQUE (content_variant_id, source)
> );
> 
> ALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;
> 
> -- SELECT own only. No INSERT/UPDATE policy → authenticated default-deny; the generator/collector write via the
> -- service key. A tenant reads its own creative performance (future dashboard FR-VA-015) and nothing else.
> CREATE POLICY "creative_metrics_select_own" ON public.creative_metrics
>   FOR SELECT USING (auth.uid() = user_id);
> 
> -- Financial ledger → clients can NEVER delete a metric row (RESTRICTIVE forbids it even if a future permissive
> -- policy is added). Mirrors the RESTRICTIVE pattern on financial/affiliate tables.
> CREATE POLICY "creative_metrics_no_client_delete" ON public.creative_metrics
>   AS RESTRICTIVE FOR DELETE USING (false);
> 
> CREATE INDEX IF NOT EXISTS creative_metrics_variant_idx  ON public.creative_metrics (content_variant_id);
> CREATE INDEX IF NOT EXISTS creative_metrics_user_idx     ON public.creative_metrics (user_id, collected_at DESC);
> CREATE INDEX IF NOT EXISTS creative_metrics_cycle_idx    ON public.creative_metrics (cycle_id);
> CREATE INDEX IF NOT EXISTS creative_metrics_product_idx  ON public.creative_metrics (product_id);
> 
> COMMENT ON TABLE public.creative_metrics IS
>   'Viral Autopilot canonical per-creative metrics ledger (FR-VA-009), keyed by content_variant_id '
>   '(= content_library.id). Unifies 3 signals (affiliate_click/organic/postback — Decisão 3). SELECT-own RLS, '
>   'service-role write (default-deny), RESTRICTIVE no client delete. Generator writes a baseline row at '
> === END creative_metrics cols ===
> ```

## 🤖 Claude *(23:15:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"optimization_policy\\|top_features\\|top_hook\\|top_product\\|reward\\|weight\" supabase/functions/autopilot-analyze/index.ts 2>/dev/null | head -40; echo \"=== analyze fn ===\"; ls supabase/functions/ | grep -i \"autopilot\\|analyze\" ",
  "description": "Inspect autopilot-analyze optimization_policy shape"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/functions/autopilot-analyze/index.ts:6:// product + platform, and writes an optimization_policy that the generator injects next cycle (FR-VA-011).
> supabase/functions/autopilot-analyze/index.ts:85:      top_product_id: topProductId, top_product_name: topProductName, top_platform: topPlatform,
> supabase/functions/autopilot-analyze/index.ts:88:    const { data: pol } = await admin.from("optimization_policy").insert({
> supabase/functions/autopilot-analyze/index.ts:90:      reward: totalClicks, context: { scope: `viral_autopilot:${planId}`, plan_id: planId, cycle_id: prevCycleId }, applied: false,
> === analyze fn ===
> analyze-node
> analyze-sem
> analyze-seo
> autopilot-analyze
> autopilot-cadence-cron
> autopilot-collect
> autopilot-run
> ```

## 🤖 Claude *(23:15:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"social_platform\\|reach\\|impressions\\|engagement\\|follower\\|brand\" supabase/migrations/*social* supabase/migrations/*creative_metrics* 2>/dev/null | head -30; echo \"=== brand-persona prep ===\"; ls .claude/context/ | grep -i \"brand\\|yt-tiktok\\|persona\" 2>/dev/null",
  "description": "Find reach/engagement signals and brand-persona prep doc"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql:9:--   plaintext credentials with no owning row, unreachable yet never revoked. This is the exact
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:3:--           3-signal metrics: affiliate_clicks + organic engagement + revenue — Decisão 3 "combo").
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:34:  impressions        int         NOT NULL DEFAULT 0 CHECK (impressions      >= 0),
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:35:  engagements        int         NOT NULL DEFAULT 0 CHECK (engagements      >= 0),
> === brand-persona prep ===
> yt-tiktok-brand-persona-integration-prep-2026-06-26.md
> ```

## 🤖 Claude *(23:15:55)*

This is the critical finding: the existing `autopilot-analyze` already writes `optimization_policy` with **`reward: totalClicks`** — a single-metric reward. That's the exact Goodhart trap the paper warns about. Let me read the analyze function's reward logic and the optimization_policy schema precisely.

## 🤖 Claude *(23:15:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '50,100p' supabase/functions/autopilot-analyze/index.ts; echo \"=== END analyze body ===\"",
  "description": "Read autopilot-analyze ranking and reward logic"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>       .select("product_id, platform, affiliate_clicks, revenue_cents")
>       .eq("cycle_id", prevCycleId).eq("user_id", userId);
>     const rows = (metrics ?? []) as Array<{ product_id: string | null; platform: string | null; affiliate_clicks: number | null; revenue_cents: number | null }>;
> 
>     const byProduct = new Map<string, { clicks: number; rev: number }>();
>     const byPlatform = new Map<string, { clicks: number; rev: number }>();
>     const bump = (m: Map<string, { clicks: number; rev: number }>, k: string | null, clicks: number, rev: number) => {
>       if (!k) return; const e = m.get(k) ?? { clicks: 0, rev: 0 }; e.clicks += clicks; e.rev += rev; m.set(k, e);
>     };
>     let totalClicks = 0, totalRev = 0;
>     for (const r of rows) {
>       const clicks = Number(r.affiliate_clicks ?? 0), rev = Number(r.revenue_cents ?? 0);
>       bump(byProduct, r.product_id, clicks, rev);
>       bump(byPlatform, r.platform, clicks, rev);
>       totalClicks += clicks; totalRev += rev;
>     }
> 
>     const hasRealData = totalClicks > 0 || totalRev > 0;
>     if (!hasRealData) {
>       logEvent("autopilot_analyze_empty");
>       return json({ ok: true, has_real_data: false, charged: 0 });
>     }
> 
>     // Pick the winner: most clicks, revenue as tiebreak.
>     const pick = (m: Map<string, { clicks: number; rev: number }>) =>
>       [...m.entries()].sort((a, b) => (b[1].clicks - a[1].clicks) || (b[1].rev - a[1].rev))[0]?.[0] ?? null;
>     const topProductId = pick(byProduct);
>     const topPlatform = pick(byPlatform);
>     let topProductName: string | null = null;
>     if (topProductId) {
>       const { data: p } = await admin.from("vm_affiliate_products").select("name").eq("external_id", topProductId).maybeSingle();
>       topProductName = (p as { name?: string } | null)?.name ?? null;
>     }
> 
>     const actionDetails = {
>       top_product_id: topProductId, top_product_name: topProductName, top_platform: topPlatform,
>       signal: "affiliate_clicks", clicks_total: totalClicks, revenue_cents_total: totalRev,
>     };
>     const { data: pol } = await admin.from("optimization_policy").insert({
>       user_id: userId, action_type: "viral_autopilot", action_details: actionDetails,
>       reward: totalClicks, context: { scope: `viral_autopilot:${planId}`, plan_id: planId, cycle_id: prevCycleId }, applied: false,
>     }).select("id").single();
> 
>     // Self-bill ONLY on the standalone path; the inline (prepaid) path was pre-reserved by the cycle.
>     let charged = 0;
>     if (!prepaid) {
>       const { error: dErr } = await admin.rpc("deduct_mco_coins", {
>         p_user_id: userId, p_amount: ANALYZE_COST, p_action: "autopilot_analyze", p_context: { cycle_id: prevCycleId },
>       });
>       if (dErr) return json({ error: "insufficient_balance", detail: dErr.message }, 402);
>       charged = ANALYZE_COST;
> === END analyze body ===
> ```

## 🤖 Claude *(23:15:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"optimization_policy\" supabase/migrations/*.sql | grep -i \"create table\\|reward\\|context\\|applied\\|policy_features\\|features\" | head -20; echo \"=== policy table ===\"; grep -rln \"CREATE TABLE.*optimization_policy\\|optimization_policy (\" supabase/migrations/*.sql 2>/dev/null",
  "description": "Find optimization_policy table schema"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:179:CREATE TABLE public.optimization_policy (
> === policy table ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql
> ```

## 🤖 Claude *(23:16:01)*

I have the decisive material finding. The `optimization_policy` table exists and the analyzer ranks the winner by `pick = most clicks, revenue tiebreak`, storing `reward: totalClicks` — single-metric. Let me confirm the optimization_policy columns and check the brand-persona prep doc's key signal/platform facts quickly.

## 🤖 Claude *(23:16:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '179,205p' supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql; echo \"=== END policy schema ===\"",
  "description": "Read optimization_policy table columns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> CREATE TABLE public.optimization_policy (
>   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   campaign_id UUID REFERENCES public.campaigns(id) ON DELETE SET NULL,
>   action_type TEXT NOT NULL,
>   action_details JSONB NOT NULL DEFAULT '{}',
>   reward NUMERIC(8,4) DEFAULT 0,
>   context JSONB DEFAULT '{}',
>   applied BOOLEAN DEFAULT FALSE,
>   created_at TIMESTAMPTZ NOT NULL DEFAULT now()
> );
> ALTER TABLE public.optimization_policy ENABLE ROW LEVEL SECURITY;
> 
> -- 13. HEALING ACTIONS
> CREATE TABLE public.healing_actions (
>   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   issue_type TEXT NOT NULL,
>   issue_details TEXT,
>   action_taken TEXT NOT NULL,
>   success BOOLEAN DEFAULT FALSE,
>   related_resource_type TEXT,
>   related_resource_id UUID,
>   metadata JSONB DEFAULT '{}',
>   created_at TIMESTAMPTZ NOT NULL DEFAULT now()
> );
> ALTER TABLE public.healing_actions ENABLE ROW LEVEL SECURITY;
> === END policy schema ===
> ```

## 🤖 Claude *(23:16:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"reach\\|video_views\\|followers\\|impressions\\|engagement\\|brand\\|alcance\\|auto-publish.*video_url\\|VIDEO_FLOW\\|publish-social\" .claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md 2>/dev/null | head -25; echo \"=== END brand prep ===\"",
  "description": "Extract reach/brand signal facts from brand-persona prep"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 1:# YouTube + TikTok — Blueprint de Preparação (virada brand-persona / Gabriel AI CCIO)
> 3:> **Data:** 2026-06-26 · **Origem:** diretiva Sovereign (virada de product-first → brand-first; Gabriel AI = CCIO como rosto/voz unificada de todos os canais) + workflow de pesquisa fundamentada `wf_24e9eb67` (3 agentes, Lei 1 — cada claim com URL oficial).
> 24:| Publisher | `publish-social/index.ts:233` (antes do fallback) | `else if (platform==='youtube')` (videos.insert resumable) · `else if (platform==='tiktok')` (Content Posting API) — espelhar o padrão IG REELS criar→poll→publicar (`:141-196`) |
> 28:| **Gap real** | `auto-publish/index.ts:54-83` | hoje só passa **texto**; p/ Shorts/TikTok agendados precisa resolver o MP4 9:16 (bucket privado → **URL pública/assinada**) e passar `content.video_url`. O Reel E2E foi invoke DIRETO; o caminho cron-de-vídeo ainda não está fechado. |
> 29:| Cadência+billing | `autopilot-run/index.ts:109` | adicionar `'youtube'`/`'tiktok'` ao `VIDEO_FLOW_PLATFORMS` → o ciclo enfileira render 9:16 e cobra vídeo p/ esses canais (FR-VA-022/024) |
> 66:**PASSO 3 — Fatia C · Cadência:** `'youtube'`/`'tiktok'` no `VIDEO_FLOW_PLATFORMS` + **fechar o gap do `auto-publish`** (resolver/assinar o MP4 9:16 e passar `content.video_url`). Isso fecha o caminho cron-de-vídeo p/ TODOS os canais (incl. IG Reel agendado, hoje só provado por invoke direto).
> === END brand prep ===
> ```

## 🤖 Claude *(23:17:01)*

I have everything I need — material grounding on all four survey artifacts, the exact reward bug, the schema columns, and the brand-persona signal map. Writing the design now.

---

## Loop de Learning & Adaptation que COMPÕE — design para OTD-AG-002

**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (blast radius = decisão de pauta autônoma que queima mco sem retorno de marca).

### Survey — o que já temos (e o que cada coisa REALMENTE aprende)

- **Obstáculo→Síntese (CLAUDE.md §5):** é Via-3-micro *manual* — aprende sobre o **processo de dev**, não sobre o produto. Cada bug vira SOP+skill+agent. É um loop fechado e materialmente verificável (o ecossistema fica melhor), mas o "reward" é o julgamento humano do Sovereign, e o sujeito que muda é o *tooling do agente*, não o conteúdo publicado. **Não é o loop que falta.**
- **OpenClaw Dreaming (`.claude/skills/openclaw-dreaming/SKILL.md`):** a fase Deep promove por ranking ponderado (`Relevance 0.30 · Frequency 0.24 · QueryDiversity 0.15 · Recency 0.15 · Consolidation 0.10 · Conceptual 0.06`) com gates (`minScore/minRecallCount/minUniqueQueries`). **Isto é precedente de ouro:** já é um reward *multi-métrica* anti-Goodhart, só que o desfecho que ele aprende é "qual memória vale promover" — utilidade de recall, não desfecho de mercado. Copiar a *forma* (vetor ponderado + gates), trocar o *domínio*.
- **`ab_variants` (viral-autopilot):** a infra existe — `autopilot_plans.ab_variants int CHECK 1-5` (migration `20260620120000:32`), FR-VA-019 manda gerar N variantes e "a vencedora é escolhida pelo desempenho do ciclo anterior". **Mas o seletor de vencedora ainda não roda multi-métrica:** `autopilot-analyze/index.ts:74` faz `pick = sort(clicks desc, rev tiebreak)` e grava **`reward: totalClicks`** (linha 90). Isso é Goodhart cravado em produção — clique de afiliado é um proxy único e gameável (clickbait que não converte e não constrói marca pontua alto).
- **`creative_metrics` + Collective Efficiency Ledger:** `creative_metrics` (migration `20260619140000`) já carrega os 4 sinais brutos por criativo — `impressions, engagements, affiliate_clicks, revenue_cents`, keyed por `content_variant_id`, UNIQUE `(content_variant_id, source)`. O Ledger (`20260626120000`) mede **mco/resultado** (eficiência), explicitamente *não* valor de desfecho. **Os termos do reward de desfecho já estão coletados — falta a fórmula que os combina.**

### 1. North-star reward multi-métrica (anti-Goodhart, alinhado à virada brand-persona)

Como hoje o objetivo é **MARCA + alcance** (não receita de afiliado — `project_brand_persona_ccio`), o reward é um vetor ponderado **derivado de `creative_metrics`** (verdade já coletada, nunca auto-reportada — princípio §5.6 da doutrina):

```
R(creative) = w_reach·z(impressions) + w_eng·z(engagements/impressions)
            + w_rev·z(revenue_cents) + w_brand·z(brand_signal)
```

- **z()** = z-score *dentro do ciclo* (normaliza por janela, impede que um pico absoluto domine — espelha o `recencyHalfLife` do Dreaming).
- **`engagements/impressions`** (taxa, não bruto) → impede gaming por volume: post que alcança muito mas não engaja não vence.
- **`brand_signal`** = retenção/saves/comentários por seguidor — o termo que materializa "marca". Hoje `creative_metrics` não distingue *tipo* de engajamento; **isto é o único campo a adicionar** (ver §3).
- **Pesos da virada brand-first (proposta inicial, datada e versionada como o Dreaming):** `w_reach 0.40 · w_eng 0.30 · w_brand 0.20 · w_rev 0.10`. Receita pesa pouco *de propósito* — afiliado é subproduto de longo prazo. Quando a virada de monetização vier, o Sovereign reponderaria (o vetor é dado, não código).

**Por que isso resiste a Goodhart:** nenhum termo isolado vence sozinho (z-score + taxa derrubam o proxy bruto); é derivado de financial/engagement truth, não escrito *para* o ledger; e o vetor de pesos é explícito e auditável — gaming exigiria mover 4 sinais correlacionados ao mesmo tempo, que é aproximadamente "fazer um bom post".

### 2. O MENOR loop genuinamente fechado que COMPÕE

**Não construir RL novo. Endurecer o loop FR-VA-010/011 que já existe** — ele já é fechado (analisa→policy→injeta), só está com reward de métrica única. A mudança mínima:

1. **MEDE:** `autopilot-analyze` deixa de fazer `pick(clicks)` e passa a computar `R(creative)` sobre `impressions/engagements/affiliate_clicks/revenue_cents` por variante (`content_variant_id`) do ciclo anterior. Já lê essas linhas — só amplia o `SELECT` (hoje só pega `product_id, platform, affiliate_clicks, revenue_cents` em `:50`).
2. **GUARDA o reward:** grava `reward = R(winner)` e `action_details.reward_vector = {reach, eng, brand, rev, weights}` na `optimization_policy` (coluna `reward NUMERIC` + `action_details jsonb` já existem — migration `20260402014040:179`). O vetor guardado é a prova auditável do *porquê* venceu.
3. **MUDA o próximo ciclo:** FR-VA-011 já injeta o `optimization_policy` mais recente no system prompt. O comportamento muda porque a variante vencedora (hook/produto/formato/horário) é promovida e re-semeada via `ab_variants` — exatamente a infra que está parada. Variante perdedora é podada; nasce 1 nova de exploração (ε-greedy mínimo: 1 das N variantes sempre é aleatória, p/ não colapsar em ótimo local — equivalente ao `QueryDiversity` do Dreaming).
4. **PROVA material que melhorou (Lei 1):** o **Collective Efficiency Ledger já é o medidor honesto** — `R̄(ciclo N+1) > R̄(ciclo N)` com `mco_actual` estável ou caindo prova *composição* (melhor desfecho por mco). Materialmente: `SELECT avg(reward) FROM optimization_policy WHERE scope GROUP BY cycle ORDER BY created_at` mostrando série crescente + UUID de cada policy. Sem isso é poesia.

### 3. O gargalo REAL — honestidade

**Não é falta de loop. O loop está construído e a 1 linha de virar honesto** (trocar `pick(clicks)`/`reward:totalClicks` por `R()` multi-métrica em `autopilot-analyze`). O gargalo real é **DADO DE DESFECHO**, e tem dois nós:

- **Termo `brand_signal` não existe ainda** — `creative_metrics` tem `engagements` agregado, não saves/comentários/retenção. Adicionar a coluna é trivial; **preenchê-la depende da frente B** (publish-social YouTube/TikTok + o `auto-publish` que ainda *não passa `video_url`* — `auto-publish/index.ts:54-83`, gap cravado no prep brand-persona). Sem os canais de marca publicando, o coletor (FR-VA-008) não tem reach/brand real pra coletar → o reward roda só com `affiliate_clicks/revenue` e **degrada de volta ao proxy único**.
- **Atribuição de receita (FR-VA-017)** depende de postback ML, mas com `w_rev 0.10` isso é tolerável — o loop não trava por falta de receita.

**Veredito:** o loop multi-métrica é shippável **agora** sobre os 2 sinais que já fluem (engagement-rate + revenue), e isso *já* mata o Goodhart de `reward:totalClicks` em produção — ganho imediato. Mas ele só **COMPÕE de verdade** (melhora medida ciclo-a-ciclo no eixo MARCA, que é o north-star da virada) **quando a frente B destrava reach/brand**: publish YouTube/TikTok + o gap do `auto-publish video_url`. Ordem honesta: (a) virar o reward multi-métrica em `autopilot-analyze` + guardar o vetor — fecha o anti-Goodhart hoje; (b) frente B publica nos canais de marca — alimenta `brand_signal`; (c) só então o Ledger prova `R̄` crescente no eixo certo.

**Arquivos-âncora:** `supabase/functions/autopilot-analyze/index.ts:74,90` (o bug a corrigir) · `supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql:34-37` (sinais brutos) · `supabase/migrations/20260620120000_viral_autopilot_plans.sql:32` (`ab_variants`) · `supabase/migrations/20260402014040…:179` (`optimization_policy.reward/action_details`) · `supabase/migrations/20260626120000…` (Ledger = medidor) · `.claude/skills/openclaw-dreaming/SKILL.md` (precedente do vetor ponderado) · `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md:28` (gap `auto-publish video_url` = dependência da frente B).

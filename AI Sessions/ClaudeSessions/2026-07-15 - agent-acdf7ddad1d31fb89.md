# Session agent-acdf7ddad1d31fb89
**Date:** 2026-07-15 | **Session ID:** `agent-acdf7ddad1d31fb89`

---

## 👤 User *(14:55:38)*

Você é o CRÍTICO ADVERSARIAL do gate Closed-Loop (Step 3.5) para a BoK do spaces-cadence. Leia TODOS os arquivos em /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/ (00-index, 01-mrd..05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics) e o blueprint /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/00-deepsearch-blueprint.md. Verifique CETICAMENTE (tente REPROVAR): (a) os 9 docs existem e são completos; (b) a SDD carrega a Pattern Conformance Declaration dos 21 padrões (docs/architecture/agentic-vision.md); (c) os FRs rastreiam ao blueprint e reaparecem no data-model/process-flow; (d) a BoK REUSA autopilot/sequences/scheduled_posts (NÃO reconstrói distribuição); (e) cobrança só via deduct_mco_coins per-tenant + BYOK per-user fail-closed + ES256 JWKS estão documentados. Liste gaps concretos (arquivo + o que falta). verdict = "GATE ABERTO" só se tudo passar; senão "BLOQUEADO" com a lista.

## 🤖 Claude *(14:55:42)*

<details>
<summary>💭 Thinking Process</summary>

I'm going to start by reading through all the files in the spaces-cadence BoK directory.

</details>


## 🤖 Claude *(14:55:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/ && echo \"---ARCH---\" && ls -la /home/gcrUX/htdocs/constellation-orchestra/docs/architecture/agentic-vision.md",
  "description": "List spaces-cadence BoK files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 360
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jul 15 11:55 .
> drwxrwxr-x 32 gcrUX  gcrUX   4096 Jul 14 20:22 ..
> -rw-rw-r--  1 ubuntu ubuntu 68633 Jul 14 19:38 00-deepsearch-blueprint.md
> -rw-rw-r--  1 ubuntu ubuntu 21189 Jul 15 11:55 00-index.md
> -rw-rw-r--  1 ubuntu ubuntu 21470 Jul 15 11:25 01-mrd.md
> -rw-rw-r--  1 ubuntu ubuntu 27134 Jul 15 11:29 02-brd.md
> -rw-rw-r--  1 ubuntu ubuntu 29017 Jul 15 11:33 03-prd.md
> -rw-rw-r--  1 ubuntu ubuntu 39018 Jul 15 11:38 04-frd.md
> -rw-rw-r--  1 ubuntu ubuntu 42522 Jul 15 11:43 05-sdd.md
> -rw-rw-r--  1 ubuntu ubuntu 26479 Jul 15 11:46 06-data-model.md
> -rw-rw-r--  1 ubuntu ubuntu 33990 Jul 15 11:47 07-process-flow.md
> -rw-rw-r--  1 ubuntu ubuntu 26201 Jul 15 11:50 08-quality-metrics.md
> ---ARCH---
> -rw-rw-r-- 1 gcrUX gcrUX 12068 Jun 26 19:42 /home/gcrUX/htdocs/constellation-orchestra/docs/architecture/agentic-vision.md
> ```

## 🤖 Claude *(14:55:46)*

I'll read all 9 BoK docs plus the blueprint and the agentic-vision doctrine. Let me batch the reads.

## 🤖 Claude *(14:55:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/architecture/agentic-vision.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MCORCH — Agentic Vision (Doutrina AGI→ASI · lente vinculante de desenvolvimento)
> 2	
> 3	> **Documento canônico load-bearing.** Toda SDD de módulo novo declara conformidade contra os **21 padrões agênticos** desta doutrina (ver CLAUDE.md §1 — *Pattern Conformance Declaration*). Este documento **substitui** `docs/architecture/system_architecture.md` como referência arquitetural viva.
> 4	
> 5	| Campo | Valor |
> 6	|---|---|
> 7	| **Status** | Vivo (v1) · selado na malha como `documentation_suite` |
> 8	| **Fontes** | `docs/Agentic-Design-Patterns.pdf` (Gulli, 482 pg — 21 padrões) · `docs/From AGI to ASI - 2606.12683.pdf` (DeepMind arXiv:2606.12683, 57 pg — 4 vias) |
> 9	| **Síntese pai** | `.claude/context/agi-asi-via4-design-checklist.md` (nó malha `a576216e`) |
> 10	| **ORO** | Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign |
> 11	| **Criado** | 2026-06-26 |
> 12	
> 13	---
> 14	
> 15	## 1. Tese — onde estamos e para onde encaminhamos
> 16	
> 17	O paper *From AGI to ASI* mapeia o avanço **pós-AGI** por **quatro vias não-exclusivas** (compõem, não só somam):
> 18	
> 19	1. **Via 1 — Escala** (compute + modelos + dados).
> 20	2. **Via 2 — Saltos de paradigma** (quebra algorítmica/arquitetural).
> 21	3. **Via 3 — Auto-aperfeiçoamento recursivo** (IA melhorando IA — o caminho "Singularidade").
> 22	4. **Via 4 — Formação de coletivo de agentes** (coordenação de muitos agentes especializados, governança central ou de mercado).
> 23	
> 24	**O MCORCH é a Via 4 instanciada na camada de produto** — um coletivo de agentes especializados (Pantheon/Departmental Army + Knowledge Mesh + orquestração) **com o humano no comando** (ORO/HITL) — **e roda a Via 3 no micro**: o mandato **Obstáculo→Síntese** (CLAUDE.md §5) é *auto-aperfeiçoamento recursivo aplicado ao próprio processo de desenvolvimento* — todo obstáculo resolvido vira SOP+skill+agent, e o sistema melhora o próprio tooling.
> 25	
> 26	**Calibração honesta (Lei 1):** o paper opera em escopo de **laboratório de fronteira** (treinar modelos, compute, energia). O MCORCH não é isso — é uma instanciação **fiel, em camada de produto**, dos padrões de desenho da Via 4 + Via 3-micro. Força declarada, não pretensão.
> 27	
> 28	### O gap estrutural (o que "antecipar o mercado" realmente significa)
> 29	
> 30	O paper aponta como **aberto** justamente o que o MCORCH ainda não faz: respondemos as perguntas de coletivo de agentes **por doutrina, mas não *medimos* nenhuma** —
> 31	
> 32	- valor marginal por agente adicionado ao fan-out (multi-agent scaling, V4-2);
> 33	- custo (mco) por resultado, atribuído a "mais agentes" vs "modelo maior" (V4-4);
> 34	- overhead de coordenação — hops/handoffs/retries por resultado (V4-5).
> 35	
> 36	**Crescemos o coletivo no escuro.** Instrumentar isso é o fosso. A iniciativa flagship desta doutrina é o **Collective Efficiency Ledger** (§4 abaixo).
> 37	
> 38	---
> 39	
> 40	## 2. Pattern Maturity Ledger (21 padrões canônicos × MCORCH)
> 41	
> 42	Maturidade: ✅ **Forte/Excelente** (doutrina sólida + artefato em produção) · 🟡 **Moderado/Parcial** (existe mas não-canônico/ad-hoc) · 🔴 **Fraco** (gap real).
> 43	
> 44	| # | Padrão | Maturidade | Artefato MCORCH que o encarna | Gap aberto (→ OTD §3) |
> 45	|---|--------|:--:|---|---|
> 46	| 1 | **Prompt Chaining** | ✅ | `orchestrate-content`/`orchestrate-step` (pg_net), Workflow `pipeline()` | Sem validação JSON Schema entre steps (coerção manual de tipo) |
> 47	| 2 | **Routing** | 🟡 | `llm-cascading-fallback` (provider Claude→GPT→Gemini), Vision-QA gate | Sem routing semântico por embedding para dispatch de agente |
> 48	| 3 | **Parallelization** | ✅ | Workflow `parallel()` fan-out concorrente; `openrouter-swarm` | Sem timeout/circuit-break em straggler; sem backpressure |
> 49	| 4 | **Reflection** | 🟡 | Vision-QA (`vision-qa.ts`), `mcorch-qa-healing` (verify adversarial) | Hard-coded por caso; sem framework Generator-Critic genérico |
> 50	| 5 | **Tool Use** | ✅ | Vision MCP (`packages/vision-mcp-core/`), edge functions tipadas | Schemas autorados à mão; sem telemetria de tool (sucesso/latência) |
> 51	| 6 | **Planning** | 🟡 | BoK suite (MRD→SDD), `deepsearch-blueprint`, `intent-plan-execution` | Plano pré-gerado; sem re-planejamento dinâmico na divergência |
> 52	| 7 | **Multi-Agent** | ✅ | **Pantheon** (L1 Heads + L2 + main + guardian), OpenClaw squad | Sem protocolo inter-agente formal; sem debate de consenso |
> 53	| 8 | **Memory Management** | ✅ | **Knowledge Mesh GraphRAG** (`mcorch_nodes/edges`, HNSW 768d, FSRS-6) | Short-term (janela) e long-term (grafo) sem estratégia de recall unificada |
> 54	| 9 | **Learning & Adaptation** | 🔴 | Obstáculo→Síntese (manual), autopilot `optimization_policy` | **Sem loop de feedback fechado/RL formal; risco de reward de métrica única** |
> 55	| 10 | **Model Context Protocol** | ✅ | Vision MCP (spec Anthropic, Streamable HTTP), `McpConnectorsCard` | Sem middleware de normalização de output; sem auto-schema de REST |
> 56	| 11 | **Goal Setting & Monitoring** | 🟡 | `infra_health_logs` + watchdog, `sprint-priorities` (SMART) | Sem camada formal de spec de goal; loop monitor→feedback→replan ad-hoc |
> 57	| 12 | **Exception Handling & Recovery** | ✅ | `infra_health_logs`, `rescue-video`, refund RPCs, watchdog, retry idempotente | Sem máquinas de estado de recovery explícitas (rollback DAGs) |
> 58	| 13 | **Human-in-the-Loop** | ✅ | **ORO triplet** (`survival.md`), AskUserQuestion, GO Sovereign | Sem tracking de SLA de escalação; sem tag de expertise do reviewer |
> 59	| 14 | **Knowledge Retrieval (RAG)** | ✅ | Knowledge Mesh (`match_mcorch_nodes`, `search-constellation`), MCP `mesh.search` | Resolução de contradição/reconciliação de fonte não-automatizada |
> 60	| 15 | **Inter-Agent Comm. (A2A)** | 🟡 | Mesh bridge (`bridge-mesh-to-openclaw`/`distribute-mesh-to-agents`), Telegram, edges | Sem schema de Agent Card / protocolo de discovery formal |
> 61	| 16 | **Resource-Aware Optimization** | ✅ | **mcoCoins** (`deduct_mco_coins` atômico), calibração 4×-floor, caps Vision MCP | Sem reserva preditiva de recurso / gestão proativa de quota |
> 62	| 17 | **Reasoning Techniques** | 🟡 | deepsearch (Gemini grounding), `analyze-node`, Workflow judge-panel/loop-until-dry | Sem Graph-of-Thought formal / framework de agente de reflexão |
> 63	| 18 | **Guardrails / Safety** | ✅ | **Survival Laws**, **Cyber-Sentinel** (`_shared/sentinel.ts` pt-BR+EN), RLS default-deny, BoK Gate, ES256 JWT | Sem suíte de eval adversarial / regressão de jailbreak no CI |
> 64	| 19 | **Evaluation & Monitoring** | 🟡 | `mcorch-qa-healing` (Fase 5c), Vision QA, `audit-schema-drift`, e2e-user-zero | Sem rubricas de avaliação padronizadas / dashboard contínuo de métricas |
> 65	| 20 | **Prioritization** | 🟡 | `sprint-priorities`, ledger OTD/RPN (FMEA), gates de recusa Survival | Sem álgebra de priorização formal / scheduler (risco de starvation) |
> 66	| 21 | **Exploration & Discovery** | 🟡 | `fetch-trends`/`vm_trends` (autopilot angle), `deepsearch-blueprint`, OpenClaw Dreaming | Sem torneio de ranking (Elo) / loop de debate multi-agente; exploração reativa, não generativa |
> 67	
> 68	> **Apêndice F (Reasoning Engines)** — presente (Vision MCP multimodal, streaming Workflow); gap: SLA de latência + semântica de rollback de output streamado não formalizados. Não conta como padrão numerado.
> 69	
> 70	**Placar:** ✅ **11 fortes** · 🟡 **9 moderados** · 🔴 **1 fraco**. A fundação (Guardrails + Memory + Multi-Agent + Resource-Aware + Tool/MCP + HITL) é robusta; os gaps são majoritariamente de **canonização** (formalizar o que já fazemos ad-hoc) e **instrumentação** (medir), não de arquitetura ausente. A exceção real é **Learning & Adaptation** — o elo recursivo (Via 3) ainda é manual.
> 71	
> 72	---
> 73	
> 74	## 3. Backlog priorizado de canonização (gaps → OTDs nomeados)
> 75	
> 76	Os gaps **não viram código já** — viram dívida técnica rastreável (OTD). Prioridade pela tese: o que destrava medir o coletivo primeiro.
> 77	
> 78	| OTD | Padrão | Iniciativa | Prioridade |
> 79	|---|---|---|---|
> 80	| **OTD-AG-001** | 9·11·16 | **Collective Efficiency Ledger** — instrumentar valor marginal/agente, mco/resultado, overhead de coordenação (V4-2/4/5). **Flagship desta doutrina** (§4). | 🔴 P0 |
> 81	| OTD-AG-002 | 9 | Fechar o loop **Learning & Adaptation** — feedback estruturado autopilot→policy com reward **multi-métrica** (anti-Goodhart) | 🔴 P0 |
> 82	| OTD-AG-003 | 4 | Framework **Generator-Critic** genérico (reflexão reutilizável, crítico de persona distinta) | 🟡 P1 |
> 83	| OTD-AG-004 | 19 | **Rubricas de avaliação** padronizadas + dashboard contínuo (LLM-judge + amostra humana) | 🟡 P1 |
> 84	| OTD-AG-005 | 6·11 | **Re-planejamento dinâmico** — plano revisado na divergência de execução (monitor→replan) | 🟡 P1 |
> 85	| OTD-AG-006 | 15 | **Agent Card** formal + protocolo de discovery (A2A schema-ado) | 🟡 P2 |
> 86	| OTD-AG-007 | 2 | **Routing semântico** por embedding para dispatch de agente/modelo | 🟡 P2 |
> 87	| OTD-AG-008 | 21 | **Torneio de exploração** (Elo) — hipótese→crítico→ranqueador→evolução | 🟢 P3 |
> 88	| OTD-AG-009 | 18 | Regressão de **jailbreak adversarial** no CI (Cyber-Sentinel) | 🟢 P3 |
> 89	| OTD-AG-010 | 12 | Máquinas de estado de **recovery** explícitas (rollback DAG) | 🟢 P3 |
> 90	
> 91	---
> 92	
> 93	## 4. Iniciativa flagship — Collective Efficiency Ledger (OTD-AG-001)
> 94	
> 95	A resposta material ao gap estrutural. **Design VIEW-sobre-verdade-financeira** (resiste a Goodhart — ninguém escreve *para* o ledger; é derivado do que já é cobrado/refundado). Mede o **coletivo in-system** (pipelines edge + ciclos autopilot + crons Pantheon) onde mco-cost e nós da malha já existem.
> 96	
> 97	- **Primeira métrica computável já (V4-4):** mco actual ÷ criativos entregues (`autopilot_cycles.spend_mco − refunded_mco`).
> 98	- **Parcial (V4-5):** overhead via `pipeline_runs.steps` + emits `collective_retry`/`collective_hop` em `infra_health_logs`.
> 99	- **Deferido a experimento real (V4-2):** valor marginal/agente — **não fabricar proxy gameável** (alerta do próprio paper). Só mede quando houver A/B real de largura de fan-out.
> 100	
> 101	Detalhe de implementação em `docs/bok/agentic-governance/` (SSOT) + SOP `docs/processes/collective-efficiency-ledger.md`.
> 102	
> 103	---
> 104	
> 105	## 5. Princípios de design (todo módulo novo segue)
> 106	
> 107	1. **Material-proof na avaliação** — sucesso ancorado em artefato físico (Lei 1); avaliação não-declarada (Vision QA / mcorch-qa-healing).
> 108	2. **Defense-in-depth de guardrails** — Survival Laws + Sentinel + RLS default-deny + BoK Gate; nunca camada única.
> 109	3. **Loop de feedback fechado** — toda automação que produz resultado deve poder medir se o resultado melhorou (anti-Via-3-cega).
> 110	4. **Reuso do chokepoint de telemetria** — emitir em `infra_health_logs` (sem PII/segredos), não criar write-sites paralelos.
> 111	5. **Multi-tenant-correto desde o dia 1** — `security_invoker` VIEW sobre bases SELECT-own; agregado cross-tenant = service-role-only.
> 112	6. **Anti-Goodhart** — métrica derivada de verdade financeira, não auto-reportada; deferir o que só medível por experimento.
> 113	7. **Humano no comando em velocidade supra-humana** — quando o coletivo produz mais artefatos do que o Sovereign consome, exigir digest em camadas (Guardian briefing) + bounded autonomy por domínio (Pantheon decision scope).
> 114	
> 115	---
> 116	
> 117	## 6. Conexão com a governança existente
> 118	
> 119	| Protocolo | Papel na visão |
> 120	|---|---|
> 121	| **MCORCH Master Execution Protocol** (CLAUDE.md) | BoK Gate + Obstáculo→Síntese = Via 3-micro (recursão do processo). Agora carrega o **Pattern Conformance Gate**. |
> 122	| **Survival Laws** (`survival.md`) | Materialidade + ORO = a oversight scalable que o paper aponta como faltante. Anti-alucinação universal (humano e agente). |
> 123	| **Pantheon Role Matrix** | Via 4 instanciada — escopo bounded por BoK lens; escalação explícita a main/Sovereign. |
> 124	| **API Tenancy (per-user)** | Segregação de credencial/quota = segurança governance-grade para coletivo multi-tenant. |
> 125	
> 126	---
> 127	
> 128	*"MATE A POESIA. ENTREGUE ENGENHARIA." — a doutrina existe para que o coletivo cresça medido, não no escuro.*
> 129	
> ```

## 🤖 Claude *(14:55:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/00-index.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BoK Index — spaces-cadence
> 2	
> 3	**Project:** spaces-cadence — "Nó de Cadência do Spaces (ir além do ManyChat)"
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Scribe:** MCORCH BoK Scribe Agent v1.0.0
> 6	**Status:** 🟡 **Suíte redigida (01→08 draft) · `09-pattern-conformance.md` a promover da SDD §9 · seal na Knowledge Mesh PENDENTE**
> 7	
> 8	> **ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (Gabriel) · Owner = Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 9	>
> 10	> **Diretiva-fonte (verbatim):** *"preciso também que adicione no roadmap um node no spaces para fazer cadência e ir além do manychat para todos os usuários; obvio que se precisar de chaves api ou custos interno deve ser feito com BYOK e se encaixar totalmente em nosso ecossistema."*
> 11	>
> 12	> **Nota de fidelidade (Lei 1):** o blueprint `00-deepsearch-blueprint.md` **não** define `FR-CAD-xxx` — declara **zero FR de inbound** antes do payload cru de DM real. A numeração `FR-CAD-xxx` foi **selada pela FRD (`04-frd.md`)**; `FR-CAD-012/013` (inbox IG) permanecem `[PROBE-GATED]` (FM-CAD-02, RPN 486). §3 do blueprint (posicionamento vs. ManyChat) carrega **SELO DE NÃO-VERIFICAÇÃO** — nenhum doc da suíte o cita como fato; só a coluna MCORCH (verificável no repo) alimenta a diferenciação.
> 13	
> 14	---
> 15	
> 16	## 1. Project Manifest
> 17	
> 18	| Field | Value |
> 19	|-------|-------|
> 20	| Business idea | Um `kind:cadence` novo no Canvas Studio (Spaces) + um **motor de sequência recorrente Postgres-first** que agenda publicação com **hora-do-dia / weekday / timezone / quiet-hours / frequency-cap / digest / A-B / overlap-catchup-jitter / idempotência** (capacidade inexistente hoje) e — **PROBE-GATED** — fecha o laço inbound (comentário/DM). "Ir além do ManyChat" = o bot ser alimentado pelo **mesmo motor que criou o post** e medido pelo **mesmo ledger que mede a receita**. |
> 21	| Market segment | **B2B** — Usuário Zero (piloto enterprise interno) + tenants BYOK futuros (multi-tenant gated) |
> 22	| Monetization | Consumo de **mcoCoins 4×-floor** por ciclo (via `begin`/`finalize`); criar plano = **0 mco** (G7 = invariante do ciclo, não do nó); custo externo BYOK **registrado** (`external_usd_cost`) mesmo com cobrança mco=0 |
> 23	| Regulatory profile | **Compliance estrutural por construção** — LGPD (Art. 8/16/18/52) · Meta Platform Policy · EU AI Act Art. 50(1) (vigência **2026-08-02**) · ePrivacy/GDPR 21 · CAN-SPAM — nunca via prompt/LLM |
> 24	| Integration surface | **extends-mcorch** — a Cadência **ENCAIXA nos trilhos vivos** (`autopilot_plans` + `autopilot-cadence-cron`; `sequences`/`nurture-dispatch`; `scheduled_posts`) e **NÃO reconstrói distribuição**. **Zero tabela de plano paralela · zero job pg_cron novo.** |
> 25	| Slug | `spaces-cadence` |
> 26	
> 27	---
> 28	
> 29	## 2. File Registry
> 30	
> 31	| File | Phase | BoK Lens | Status | Purpose · ID range |
> 32	|------|-------|----------|--------|--------------------|
> 33	| [00-index.md](00-index.md) | 0 | — | [x] este doc | Manifesto + registro + ID space + master traceability + seal pendente |
> 34	| [00-deepsearch-blueprint.md](00-deepsearch-blueprint.md) | — | Deepsearch | [x] semente | Blueprint-semente verificado 2026-07-14; §§1–11; OTD-CAD-001..018 + FM-CAD-01..16 + G1–G14 (NÃO autoriza código) |
> 35	| [01-mrd.md](01-mrd.md) | 1 | BABOK v3 | [x] draft | Mercado: gap de recorrência (grep `rrule`=0; `profiles.timezone`/`channel_profiles.cadence` mortos), inbound PROBE-GATED, janela AI Act — **MR-CAD-001..014** |
> 36	| [02-brd.md](02-brd.md) | 1 | BABOK v3 | [x] draft | Negócio: **BO-CAD-001..006** (SMART) · **BR-CAD-001..017** · ROI (não-quantificado, honesto) · **BR-RISK-CAD-001..012** · **BAC-CAD-001..010** |
> 37	| [03-prd.md](03-prd.md) | 2 | ProdBOK + CXBOK | [x] draft | Produto: personas, jornadas, MoSCoW (**PR-CAD-001..012 / 020–021 / 030–035**), UX MIV/a11y, Gherkin |
> 38	| [04-frd.md](04-frd.md) | 3 | SWEBOK v4 | [x] draft | **Funcional — SELA a numeração:** **FR-CAD-001..018** (012/013 `[PROBE-GATED]`) + **NFR-CAD-001..015** + contratos de edge + **AT-CAD-001..018** |
> 39	| [05-sdd.md](05-sdd.md) | 3 | SWEBOK + CISSP CBK | [x] draft | Design: component catalog + STRIDE + RLS + migration stubs + **§8 sela 9 OTDs** + **§9 Pattern Conformance (21 padrões)** |
> 40	| [06-data-model.md](06-data-model.md) | 4 | DMBOK v2 | [x] draft | Dados: ERD, selos 🟢🟡🔴🔒, SQL canônico (ALTER `autopilot_plans` + `cadence_dispatches`), tenant isolation, data-quality, retention LGPD |
> 41	| [07-process-flow.md](07-process-flow.md) | 4 | BPM CBOK v4 | [x] draft | Processos: **PROC-CAD-00..08** BPMN-lite + gates de verificação + recovery + Recurrence-Engine Blueprint (Postgres-first, sem n8n) + cron jobs |
> 42	| [08-quality-metrics.md](08-quality-metrics.md) | 5 | CMQ/OE BOK | [x] draft | Qualidade: gate anti-Goodhart · **QO-CAD-001..007** · **KPI-CAD-001..011** · FMEA (FM-CAD-01..16) · **SOL-CAD-001..007** (MAPE-K) · **G-CAD-A..H + PROBE** |
> 43	| [09-pattern-conformance.md](09-pattern-conformance.md) | 5 | — | [ ] **PENDENTE** | Promover a §9 da SDD (21 padrões agênticos — gate Closed-Loop Step 3.5, SSOT `docs/architecture/agentic-vision.md`) |
> 44	
> 45	> Doutrina-fonte (load-bearing, fora da suíte): `docs/architecture/agentic-vision.md` (21 padrões × Pattern Maturity Ledger — puxado pelo Pattern Conformance Gate de toda SDD).
> 46	
> 47	---
> 48	
> 49	## 3. ID Space Summary
> 50	
> 51	| Prefix | Range | Count | Defined in |
> 52	|--------|-------|-------|-----------|
> 53	| MR-CAD | 001..014 | 14 | 01-mrd |
> 54	| BO-CAD | 001..006 | 6 | 02-brd (objetivos SMART) |
> 55	| BR-CAD | 001..017 | 17 | 02-brd |
> 56	| BR-RISK-CAD | 001..012 | 12 | 02-brd (risco de negócio traduzido da FMEA) |
> 57	| BAC-CAD | 001..010 | 10 | 02-brd (business acceptance) |
> 58	| PR-CAD | 001..012 · 020..021 · 030..035 | 20 | 03-prd (MoSCoW: Must / Should / Could) |
> 59	| **FR-CAD** | **001..018** | **18** | **04-frd (SELADA)** — 012/013 `[PROBE-GATED]`; 015–018 = Fatia 0 |
> 60	| NFR-CAD | 001..015 | 15 | 04-frd |
> 61	| AT-CAD | 001..018 | 18 | 04-frd (1:1 com FR-CAD) |
> 62	| **OTD-CAD** | **001..018** | **18** | 00-blueprint §8 → **05-sdd §8 sela 9** (002/003/004/006/008/011/017/018 + G11/OTD-015); restantes gated |
> 63	| **FM-CAD** | **01..16** | **16** | 00-blueprint §8 → 05-sdd §5.1 (STRIDE) → 08 §3 (FMEA) |
> 64	| G (guardrails) | G1..G14 | 14 | 00-blueprint §6 (compliance estrutural) |
> 65	| QO-CAD | 001..007 | 7 | 08-quality-metrics |
> 66	| KPI-CAD | 001..011 | 11 | 08-quality-metrics (011 `[PROBE-GATED]`) |
> 67	| SOL-CAD | 001..007 | 7 | 08-quality-metrics (MAPE-K) |
> 68	| G-CAD (gates) | A..H + PROBE | 9 | 08-quality-metrics §9 (verificação material Lei 1) |
> 69	| PROC-CAD | 00..08 | 9 | 07-process-flow (07 `[PROBE-GATED]`) |
> 70	| Pattern | P1..P21 | 21 | 05-sdd §9 (**12 yes · 5 deferred · 4 n-a**) |
> 71	
> 72	**FMEA RPN ≥ 100 (todos os 16):** FM-CAD-02 (**486**, o maior) · -10 (336) · -03 (300) · -04 (300) · -05 (294) · -12 (270) · -11 (252) · -06 (240) · -01 (224) · -16 (224) · -13 (210) · -14 (210) · -07 (192) · -09 (180) · -08 (175) · -15 (160). Cada um com mitigação **estrutural** (FK/UNIQUE/índice-parcial/fail-closed/server-side) selada nos docs 05/06 — nenhuma depende de "cuidado do operador".
> 73	
> 74	---
> 75	
> 76	## 4. New Objects (schema + edge + cron)
> 77	
> 78	**New Edge Functions (2):** `cadence-plan` (arm — upsert `autopilot_plans` + `next_run_at` UTC; JWT `verify_jwt=false`→**ES256 JWKS**; 0 mco) · `cadence-run` (drain `FOR UPDATE SKIP LOCKED` → gate chain server-side → dispatch a `scheduled_posts` → ledger → re-arm; `Bearer SB_SECRET_KEY`→403, `user_id` server-trusted da linha).
> 79	**Fixed / Extended Edge Functions (2):** `whatsapp-webhook` (Fatia 0: alcançável via `config.toml` `verify_jwt=false` + `timingSafeEqual` + sink `lead_events`) · `instagram-webhook` `[PROBE-GATED]` (Fatia 2: `entry.messaging`+`comments`).
> 80	**New pg_cron jobs: 0** — o tick **vivo** `autopilot-cadence-cron` (*/15) passa a **rotear por `plan_kind`** (`viral`→`autopilot-run` | `cadence`→`cadence-run`). `count(*) FROM cron.job` é **invariante** (NFR-CAD-012).
> 81	
> 82	**Migrations (4 + 1 gated) — toda migration passa por `/security-review` antes do commit (FMEA-011):**
> 83	
> 84	| Migration (proposta) | Objeto | Selo | FR |
> 85	|----------------------|--------|------|----|
> 86	| `20260716120000_cadence_extend_autopilot_plans.sql` | ALTER `autopilot_plans` (+9 col: `plan_kind`, `recurrence`, `quiet_hours`, `overlap_policy`, `catchup_window`, `jitter_seconds`, `program`, `channel_allowlist`, `budget_cap_mco`; DROP `platforms_check`) | 🟡 REUSA-ESTENDE | FR-CAD-002 |
> 87	| `20260716120100_cadence_dispatches.sql` | CREATE `cadence_dispatches` + **índice único PARCIAL** `WHERE status<>'failed'` + FK composta `(plan_id,user_id)` + RLS select_own/escrita service-role | 🔴 NOVO | FR-CAD-003 |
> 88	| `20260716120200_erase_lead_cascade_cadence.sql` | `erase_lead()` cancela `scheduled_posts` + `cadence_dispatches` pendentes na **mesma transação** | 🟡 REUSA-ESTENDE | FR-CAD-017 |
> 89	| `20260716120300_auto_publish_pgcron_skiplocked.sql` | `auto-publish`: crontab de SO → **pg_cron + `FOR UPDATE SKIP LOCKED`** | 🟡 REUSA-ESTENDE | FR-CAD-018 |
> 90	| `2026xxxx_social_threads.sql` `[PROBE-GATED]` | `social_threads`/`social_messages` (relógios 24h CSW × 7d private reply; FK NOT NULL p/ inbound) — **congelado até o probe FM-CAD-02** | 🔒 NOVO gated | FR-CAD-012 |
> 91	
> 92	**Ativos mortos ressuscitados (1º leitor do repo):** `profiles.timezone` (→ SSOT de fuso, FR-CAD-007) · `channel_profiles.cadence` `{target_per,count_min,count_max}` (→ teto autoritativo do frequency-cap, FR-CAD-008 / OTD-CAD-008).
> 93	
> 94	---
> 95	
> 96	## 5. Master Traceability Matrix (FR ↔ PR ↔ BR ↔ MR ↔ OTD/FM ↔ NFR ↔ PROC)
> 97	
> 98	> Cadeia **MR-CAD → BR-CAD → PR-CAD → FR-CAD → (migration | edge | processo)**, com o par de risco (OTD/FM) e o processo (PROC) que a exercita. Consolida as matrizes de 01 §9 · 02 §10 · 03 §8 · 04 §7 · 06 §8 · 07 §8.
> 99	
> 100	| FR-CAD | Title (curto) | PR-CAD | BR-CAD | MR-CAD | OTD-CAD | FM-CAD / G | NFR-CAD | PROC-CAD | Fatia |
> 101	|--------|---------------|--------|--------|--------|---------|-----------|---------|----------|-------|
> 102	| **001** | Nó `cadence` no canvas (Publish, keyless, quote 0) | 001 | 001 | 001 | 002, 007 | FM-16 | 007, 014 | 01 | 1 |
> 103	| **002** | Estender `autopilot_plans` (9 col, −1 CHECK) | 003 | 002, 004 | 002, 008 | 003 | FM-06 | 006, 012 | 01/02 | 1 |
> 104	| **003** | `cadence_dispatches` + índice único parcial | 004 | 003 | 006 | 006 | FM-01 | 001, 006 | 03 | 1 |
> 105	| **004** | Roteamento do tick por `plan_kind` (sem cron novo) | 003 | 002, 004 | 002, 008 | 003 | FM-06 | 012 | 02 | 1 |
> 106	| **005** | Edge `cadence-plan` (arm UTC) + inspector poll | 002 | 004 | 001 | — | — | 004, 014 | 01 | 1 |
> 107	| **006** | Edge `cadence-run` (drain+gate+dispatch+re-arm) | 005 | 009, 011, 013 | 009 | 004, 005 | FM-01/05/07 | 002, 009, 013 | 03 | 1 |
> 108	| **007** | Re-arm UTC `{freq,days,hours,minutes,tz}` | 006 | 005 | 002 | — | FM-06 | 003 | 03 | 1 |
> 109	| **008** | Quiet-hours + frequency-cap **HALT** | 007 | 006 | 003 | 008, 017 | G3/G4 | 009, 010 | 03 | 1 |
> 110	| **009** | Dedup/digest `(user,channel,dia)` | 008 | 007 | 004 | — | — | 010 | 03 | 1 |
> 111	| **010** | A/B determinístico (`abs(hashtext(...)::bigint)`) | 009 | 008 | 005 | 016 | — | 002 | 03 | 1 |
> 112	| **011** | Custo projetado/ciclo + `budget_cap_mco` NOT NULL | 010 | 010, 012 | 007 | 011 | FM-10 | 007, 008 | 01 | 1 |
> 113	| **012** `[PG]` | Ingest inbound IG (`entry.messaging`+comments) | 030 | 015 | 012 | 018 | **FM-02 (486)**/13 · G1 | 010, 015 | 07 | 2 |
> 114	| **013** `[PG]` | Resposta na janela (private reply 7d / in-window 24h) | 030 | 015 | 012 | 018 | FM-03 · G2/G5/G6 | 010 | 07 | 2 |
> 115	| **014** | Telegram (US$0) + Email Resend (flip, fail-closed) | 020, 021 | 016, 013 | 013 | 009 | FM-12 · G10/G12 | 005, 010 | 08 | 3 |
> 116	| **015** | Fatia 0: `whatsapp-webhook` alcançável + timing-safe | 012 | 017 | 014 | 001 | FM-09 | 004 | 00 | 0 |
> 117	| **016** | Fatia 0: `estimateNodeCost` case `publishSocial` | 012 | 017 | 014 | 007 | FM-16 | — | 00 | 0 |
> 118	| **017** | Fatia 0: `erase_lead()` cascata (mesma txn) | 012 | 017, 014 | 014 | 006 | FM-04 · G9 | 011 | 00/06 | 0 |
> 119	| **018** | Fatia 0: `auto-publish` pg_cron + SKIP LOCKED | 012 | 017, 011 | 014 | 004 | FM-01 | 012 | 00/04 | 0 |
> 120	
> 121	`[PG]` = `[PROBE-GATED]` (não gera código antes do probe FM-CAD-02 fechar).
> 122	
> 123	**Invariantes de rastreabilidade (regra do BoK Gate):** todo FR-CAD rastreia ≥1 PR-CAD (04 §7) ✅ · todo objeto de dado rastreia ≥1 FR-CAD (06 §8) ✅ · toda migration/edge aparece em ≥1 PROC-CAD (07 §8) ✅ · todo FM-CAD com RPN>100 tem mitigação estrutural selada (08 §3) ✅ · cada feature mapeada aos 21 padrões (05 §9) ✅.
> 124	
> 125	---
> 126	
> 127	## 6. Open Technical Decisions — status
> 128	
> 129	> 9 OTDs **selados** na SDD §8 (default do blueprint §11); os demais permanecem **gated** por provisão Sovereign (ação que só o Sovereign executa). Nenhum é improviso.
> 130	
> 131	| OTD-CAD | Assunto | Status | Decisão / gate |
> 132	|---------|---------|--------|----------------|
> 133	| 001 | `whatsapp-webhook` inalcançável + HMAC não timing-safe | **Fatia 0 (P0)** | Bloco `config.toml` + `timingSafeEqual` (FR-CAD-015) |
> 134	| 002 | Sujeito da cadência (asset vs. geração) | **Selado A** | Asset existente (0 mco, keyless) |
> 135	| 003 | Estender `autopilot_plans` vs. tabela nova | **Selado A** | Estender (2 motores idênticos em prod; 3º triplica) |
> 136	| 004 | `auto-publish` sem lock | **Fatia 0 item 5** | pg_cron + `FOR UPDATE SKIP LOCKED` (FR-CAD-018) |
> 137	| 005 | Retry carrossel IG duplica children | **Gated** | Carrossel **fora** da cadência até fechar (FM-CAD-08) |
> 138	| 006 | Semântica `cadence_dispatches` (retry vs. append-only) | **Selado A** | Retry via índice parcial `WHERE status<>'failed'` |
> 139	| 007 | `estimateNodeCost` sem case `publishSocial` | **Fatia 0** | 1 linha (FR-CAD-016) |
> 140	| 008 | `channel_profiles.cadence` autoritativo? | **Selado A** | Teto autoritativo (ressuscita dado morto) |
> 141	| 009 | Enquadramento **AI Provider WhatsApp Brasil** | **Gated (econômico)** | Consulta Meta antes de flipar auto-reply p/ `sent` |
> 142	| 010 | Legitimidade contratual BYOK (Tech Provider) | **Gated (jurídico)** | Revisão Meta Platform Terms antes do Usuário 1 |
> 143	| 011 | X pay-per-use (**Post-com-URL = 45 mco**) | **Selado B (P1)** | X **fora** da allowlist Fatia 1 até probe de créditos no Console |
> 144	| 012 | Rate limit Send API (100 vs 300 calls/s) | **Gated (empírico)** | Resolver por `X-Business-Use-Case-Usage` antes da Fatia 2 |
> 145	| 013 | TikTok comment/DM orgânico (SPA não renderizou) | **Gated** | Zero FR até probe autenticado |
> 146	| 014 | AI Act Art. 50(2) (conteúdo sintético) | **Gated (2026-08-02)** | Módulo próprio, maior que este |
> 147	| 015 | Base legal Brasil (Guia ANPD não literal) | **Selado** | `basis='consent'` fail-closed até confirmar |
> 148	| 016 | Quem alimenta `creative_metrics.hook_rate` | **Gated** | Pré-requisito de **ligar** o A/B |
> 149	| 017 | Frequency-cap por `(user,channel)` vs. `(…,conta)` | **Selado A** | `(user,channel)` na Fatia 1 |
> 150	| 018 | IG/Messenger no app Meta **global** vs. BYOK-de-app | **Selado A** | Global até o Usuário 1 + cap por-APP + kill-switch global |
> 151	
> 152	---
> 153	
> 154	## 7. Compliance Guardrails (G1–G14 — o que o sistema IMPEDE por construção)
> 155	
> 156	`G1` FK NOT NULL p/ inbound (cold DM impossível de representar — janela 24h) · `G2` `UNIQUE(comment_id)` (private reply 7d, 1×) · `G3` opt-out server-side + kill-switch por feedback negativo · `G4` caps NOT NULL + template não-única-via · `G5` Human Agent tag **inalcançável** do caminho service-role · `G6` classificador in/out-window server-side · `G7` opt-in WhatsApp `granted_at`+`source_proof` (senão 422) · `G8` `marketing_consents.basis` gate de enqueue fail-closed + opt-out público por token · `G9` `erase_lead()` cascata (LGPD Art. 16/18 VI) · `G10` rodapé CAN-SPAM montado **server-side** · `G11` jurisdição fail-closed = UE quando país desconhecido · `G12` **disclosure de IA server-side** (AI Act Art. 50(1), 2026-08-02) · `G13` IoC anti-browser-automation (falha se script fora de `scripts/qa/` tocar `instagram.com`/`facebook.com`) · `G14` assinar `message_template_status_update` (recategorização utility→marketing). **Todos estruturais — nunca via LLM.**
> 157	
> 158	---
> 159	
> 160	## 8. Fatiamento (roadmap de execução)
> 161	
> 162	| Fatia | Nome | Gate externo | Entrega |
> 163	|-------|------|--------------|---------|
> 164	| **0** | Pré-requisitos P0 | Nenhum (deploy) | FR-CAD-015/016/017/018 — sem eles tudo é falso-sucesso (`whatsapp-webhook` alcançável · `estimateNodeCost` · `erase_lead()` cascata · `auto-publish` pg_cron+SKIP LOCKED) |
> 165	| **1** | **Cadência de Publicação** | **ZERO app review** | FR-CAD-001..011 — o **único** entregável sem gate externo; valor visível ao Usuário Zero e a **qualquer** tenant (hora/weekday/tz/quiet/cap/digest/A-B/idempotência). Canais = allowlist `auto-publish` **MENOS X**; **nenhuma mensagem privada** |
> 166	| **2** | Inbox IG | **PROBE-GATED** | FR-CAD-012/013 — congelado até DM real de terceiro sem role no banco + payload cru (FM-CAD-02, RPN 486); nasce `delivery:'gated'` |
> 167	| **3** | Canais desimpedidos BYOK | Sem review de plataforma | FR-CAD-014 — Telegram (US$0, `/start`) + Email Resend (flip `nurture-dispatch`, rodapé server-side) |
> 168	| **4** | GATED (não prometer) | Provisão Sovereign por item | WhatsApp Cloud BYOK · IG multi-tenant (App Review) · Messenger · X na allowlist · LinkedIn comment reply |
> 169	
> 170	**Deferido explicitamente (sem caminho legítimo):** cold DM (qualquer canal) · broadcast por DM no IG · SMS · Discord DM · LinkedIn DM automatizada · TikTok DM/comment (zero FR até probe) · carrossel dentro da cadência (até OTD-CAD-005 fechar) · marcação AI Act Art. 50(2) (módulo próprio).
> 171	
> 172	---
> 173	
> 174	## 9. Gate Status (Closed-Loop Protocol) & Seal Pendente
> 175	
> 176	| Gate | Requisito | Status |
> 177	|------|-----------|--------|
> 178	| **Step 2 — BoK 01→05** | MRD · BRD · PRD · FRD · SDD consolidados | 🟡 **redigidos (draft v0.1)** — revisão Sovereign pendente |
> 179	| **Step 3.5 — Pattern Conformance** | 21 padrões declarados | 🟡 **em §9 da SDD**; `09-pattern-conformance.md` **a promover** (cópia de §9) |
> 180	| **Lei 2 — SOP** | `docs/processes/spaces-cadence.md` (Operator/Sequence/Verification/Recovery/Success) | 🔴 **ABERTO** — pré-requisito antes de qualquer código |
> 181	| **/security-review** | Toda migration (FMEA-011) | 🔴 **pendente** — 4 migrations + 1 gated |
> 182	| **Probe FM-CAD-02** | DM real de terceiro sem role + payload cru | 🔴 **ABERTO** — bloqueia toda a Fatia 2 (zero FR de inbound antes) |
> 183	| **Seal Knowledge Mesh** | Nó `documentation_suite` selando a suíte | 🔴 **PENDENTE** — este `00-index` é o gesto que amarra a suíte antes do seal |
> 184	
> 185	> **Nenhuma linha de código antes de:** Step 2 aprovado + `09-pattern-conformance.md` promovido + SOP Lei 2 escrito + `/security-review` de cada migration. A **Fatia 0** (P0) fecha primeiro; a **Fatia 1** é o único entregável sem gate externo; **FR-CAD-012/013** só após o probe.
> 186	
> 187	---
> 188	
> 189	## 10. Documentation Lineage
> 190	
> 191	```
> 192	Diretiva Sovereign "node de cadência no Spaces, ir além do ManyChat, BYOK, encaixar no ecossistema"
> 193	  └─▶ /deepsearch-blueprint spaces-cadence → docs/bok/spaces-cadence/00-deepsearch-blueprint.md (verificado 2026-07-14)
> 194	       └─▶ /bok-scribe spaces-cadence → suíte 01-mrd → 08-quality-metrics (v0.1 draft, esta família)
> 195	            ├─▶ reusa/estende: Viral Autopilot (autopilot_plans + autopilot-cadence-cron) · Marketing Hub (nurture-dispatch/sequences/lead_events/erase_lead) · scheduled_posts (Amendment 22) · channel_profiles.cadence · profiles.timezone
> 196	            ├─▶ Pattern Conformance ← docs/architecture/agentic-vision.md (21 padrões)
> 197	            └─▶ [SEAL PENDENTE] DERIVES_FROM → bok-scribe-seal-mcorch-constellation-v1 (plataforma-núcleo)
> 198	```
> 199	
> 200	**Referências de desenho (semântica adotada, stack rejeitada — §5.2 do blueprint):** Knock (schedule tz-aware) · Novu (Digest/Throttle como steps) · Temporal (Overlap/Catchup/Jitter) · Dittofeed (Delay localizado + Random Bucket determinístico) · Trigger.dev/River (idempotência: falha libera / sucesso prende, índice parcial + `ON CONFLICT`). Motor real = **pg_cron + `next_run_at` + índice parcial due** (Postgres-first, o padrão que o MCORCH já roda 2× em prod).
> 201	
> 202	---
> 203	
> 204	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` + `01-mrd.md` → `08-quality-metrics.md` (Lei 1: nenhum FR/NFR/OTD/FM/entidade/pattern inventado além do blueprint; FR-CAD-012/013 e KPI-CAD-011 sob `[PROBE-GATED]`; §3 do blueprint sob selo de não-verificação). Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança via RPC atômica begin/finalize (nunca client-side); verify_jwt=false → ES256 JWKS / HMAC timingSafeEqual (nunca `atob` cego); RLS default-deny owner-scoped. A Cadência ENCAIXA nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), não reconstrói distribuição — nenhum job pg_cron novo._
> 205	
> ```

## 🤖 Claude *(14:55:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/00-deepsearch-blueprint.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# spaces-cadence — Blueprint-semente (deepsearch)
> 2	
> 3	> **Status:** semente de BoK (`00-deepsearch-blueprint.md`). NÃO é SDD, NÃO autoriza código.
> 4	> **Gate:** Closed-Loop Protocol Step 2 (BoK 01→05) + Step 3.5 (Pattern Conformance) + Lei 2 (SOP) permanecem **ABERTOS**.
> 5	> **ORO:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (blast radius: ban de app Meta/X + sanção ANPD até 2% do faturamento — LGPD Art. 52).
> 6	> **Data de verificação externa:** 2026-07-14. Toda afirmação externa carrega URL. O que foi refutado está em §10.
> 7	
> 8	---
> 9	
> 10	## §1 Diretiva + escopo
> 11	
> 12	**Diretiva Sovereign (verbatim):** *"preciso também que adicione no roadmap um node no spaces para fazer cadência e ir além do manychat para todos os usuários; obvio que se precisar de chaves api ou custos interno deve ser feito com BYOK e se encaixar totalmente em nosso ecossistema".*
> 13	
> 14	**"Além do ManyChat" — a frase honesta:** o ManyChat é um **respondedor de mensagem** (bot de DM com fluxos visuais). O MCORCH já é um **produtor e distribuidor de conteúdo** (gera pilar → atomiza → reformata por canal → publica). O nó de Cadência **não** compete no fluxo de DM: ele funde as duas metades num único laço que o ManyChat não tem — **gerar → agendar → publicar → capturar o comentário/DM que o post provoca → responder dentro da janela legal → atribuir receita**. O diferencial não é "mais um bot"; é **o bot ser alimentado pelo mesmo motor que criou o post e pelo mesmo ledger que mede o retorno**.
> 15	
> 16	**Escopo do módulo:** um `kind` novo no registry do Canvas Studio (`cadence`), um motor de sequência **Postgres-first** (pg_cron + `next_run_at` + índice parcial due — o padrão que o MCORCH já roda 2× em produção e que este módulo **estende, não duplica** — §5.2/OTD-CAD-003), e — **⚠️ PROBE-GATED, não prometido** — o fechamento do laço inbound (comentário/DM) que hoje não existe.
> 17	
> 18	> ⚠️ **Gate honesto sobre o inbound (vale para §3, §5.4 e Fatia 2):** sob Standard Access o webhook do IG pode **não entregar nada** de quem não tem role no app (FM-CAD-02, RPN **486** — o maior deste doc). Enquanto o probe (DM real de **terceiro sem role**) não fechar, o laço inbound é **hipótese gated por App Review**, não capacidade do roadmap. A frase "fecha o laço inbound" **não pode** aparecer sem este carimbo.
> 19	
> 20	**Fora de escopo (declarado agora para não vazar depois):** cold DM (proibido em toda plataforma verificada), broadcast por DM no Instagram (inexistente — §10), automação via browser headless em rede social (proibição perene), marcação C2PA de conteúdo sintético (AI Act Art. 50(2) — módulo próprio, ver §8/OTD-CAD-014).
> 21	
> 22	---
> 23	
> 24	## §2 Estado do ecossistema — o que JÁ existe (não reconstruir)
> 25	
> 26	### 2.1 Cadência e agendamento (o trilho vivo)
> 27	
> 28	| Peça | Path:linha | O que é | Veredito |
> 29	|---|---|---|---|
> 30	| `autopilot_plans` | `supabase/migrations/20260620120000_viral_autopilot_plans.sql:18-67` (mode :23 · interval_days :24 · platforms CHECK :26-27 · caps :28 · next_run_at :34 · índice parcial due :57) | única tabela de **plano recorrente** com kill-switch e caps obrigatórios | **ESTENDER ESTA TABELA** (default do OTD-CAD-003). As lacunas apontadas são `ALTER TABLE`, não fundamento para tabela paralela: `platforms <@ ARRAY['wordpress','linkedin','twitter']` ⇒ **DROP CONSTRAINT** + allowlist derivada de `channel_profiles`; ausência de hora-do-dia/weekday/timezone ⇒ **ADD COLUMN `recurrence jsonb`** |
> 31	| Driver `autopilot-cadence` | `supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql:28-41` + `supabase/functions/autopilot-cadence-cron/index.ts:26,33-40,48-56` (MAX_PER_RUN=50 · CONCURRENCY=6 :15-16) | pg_cron */15 → Bearer do Vault → edge self-check 403 → scan due → fan-out bounded com `user_id` **server-trusted** | **ESTE JÁ É O DRIVER.** Não criar um 3º: o tick passa a rotear por `plan_kind` (`viral` \| `cadence`) |
> 32	| Driver `nurture-advance` | `supabase/migrations/20260603230000_nurture_advance_cron.sql:20-33` + `supabase/functions/nurture-cron/index.ts:29,34-41,50-65` | driver **gêmeo** do anterior (2 instâncias idênticas em prod) | prova que a duplicação **já custou** (2 índices due, 2 kill-switches, 2 superfícies de identidade cron). Um 3º driver **multiplica** o custo — não é virtude |
> 33	| Re-arm de cadência | `supabase/functions/autopilot-run/index.ts:310-314` | única implementação de "próxima execução" do repo (`now + interval_days`) | **REUSAR o padrão**, generalizar para `{frequency, days, hours, minutes, tz}` |
> 34	| Débito/estorno atômico | `…20260620120200_begin_autopilot_cycle.sql` · `…120300_finalize_autopilot_cycle.sql` · `…20260702190000_spaces_generations_ledger.sql:83-131,141-190` | begin (advisory-lock + `ON CONFLICT DO NOTHING` ⇒ zero débito duplo) / finalize (refund idempotente, clamp) | **OBRIGATÓRIO reusar** se o nó gastar mco. Nunca reimplementar débito |
> 35	| Sub-cadência de vídeo | `supabase/functions/_shared/autopilot-video-cadence.ts:11-30` + migration `20260705120000:12-15` | matemática pura `every_n_cycles` + yield ao budget cap, testável sem Deno | **REUSAR** como precedente de "sub-cadência dentro da cadência" |
> 36	| `scheduled_posts` | `…20260402014040…:158-176` (DDL+RLS) · políticas :297-300 | fila **one-shot** (queued/publishing/published/failed, `scheduled_at`, retry_count) | **REUSAR COMO SINK**. Não serve de fonte de recorrência (sem coluna de repetição) |
> 37	| `auto-publish` | `supabase/functions/auto-publish/index.ts:21-27,200-212` + `scripts/auto-publish-cron.sh:19` + crontab `*/5` | drenador da fila, retry com backoff por contagem | **REUSAR sem tocar**. O nó **enfileira**, não publica. ⚠️ roda em **crontab de SO de um host** (classe de confiabilidade inferior ao pg_cron) |
> 38	| 3 seams de enqueue | `reshape-pillar/index.ts:482-484` · `publish-space-asset/index.ts:188-207` (409 anti-duplicata) · `publish-space-carousel/index.ts:41-49,66-90` | contrato `metadata.reshape` + **`schedule:true` + `publish_at` ISO + 422 em data inválida + 409 anti double-enqueue + GROUP MARKER** (Amendment 22, `docs/bok/spaces-evolution/22-amendment-scheduled-carousel.md:21-22`) | **MOLDE EXATO** do parâmetro de agendamento do nó |
> 39	| Drip por passo | `…20260603050000_marketing_hub_nurturing.sql:11-21,35-59` (`steps jsonb` · `current_step` · `next_run_at` · índice parcial due) + `nurture-dispatch/index.ts:180-185` | única "espera relativa entre passos" existente | **REUSAR o modelo `steps jsonb + current_step + next_run_at`** |
> 40	| Consent gate + LGPD | `…20260603000000_marketing_hub_lead_core.sql:82-92` (`marketing_consents`, basis CHECK) · :130-169 (`erase_lead()` tenant-guarded) · `nurture-dispatch/index.ts:7-9,150` (`delivery: 'gated'\|'sent'\|'failed'`) | espinha de consentimento + molde **nascer gated** | **REUSAR INTEGRALMENTE** |
> 41	| `lead_events` | `…20260603000000…:56-57,63,68-70` (`channel` text · `event_type` text **sem CHECK** · FK composta (id,user_id) · RLS só select_own+insert_own = imutável) | ledger append-only tenant-escopado | **REUSAR SEM MIGRATION**: `event_type='message_received'` entra hoje |
> 42	| `notify()` + sino | `supabase/functions/_shared/notify.ts:19-29` · `src/hooks/useNotifications.ts:5-6,29-32` | insert service-role-only, best-effort, realtime no cliente | **REUSAR DIRETO** (1 chamada = valor visível) |
> 43	| `channel_profiles.cadence` | `…20260627140000_channel_profiles.sql:32,103` + `…20260628120000:10` (`{target_per, count_min, count_max}`) | política declarativa de quantos posts/semana por canal | **DADO MORTO** (grep de leitores = 0). O nó é o **primeiro consumidor** — vira o teto autoritativo |
> 44	| `optimize-schedule` | `supabase/functions/optimize-schedule/index.ts:68-85` (único `.from()` é `decrypted_user_api_keys` :51) | LLM per-user BYOK sugere 5 horários; **não escreve nada** | **REUSAR COMO ORÁCULO** opcional. Hoje o conselho morre em `CalendarPage.tsx:295` |
> 45	| UI de calendário | `src/pages/CalendarPage.tsx:231-234` · `src/hooks/useScheduledPosts.ts:10-87` · `useAutopilot.ts:95-101` (`arm next_run_at = agora` ao ativar) | CRUD de `scheduled_posts` + gesto de ativação | **REUSAR**: o nó não precisa de UI de calendário nova |
> 46	| Webhook IG | `supabase/functions/instagram-webhook/index.ts:32-43` (HMAC fail-closed + `timingSafeEqual`), :57-74 | handshake `hub.challenge` + HMAC **corretos**; sink = 1 linha em `infra_health_logs` e nada mais | **REUSAR o esqueleto**; trocar o sink |
> 47	| Escopos IG já pedidos | `supabase/functions/social-auth-init/index.ts:87` (`instagram_business_manage_comments` + `..._manage_messages`) | o OAuth **pede** os escopos de DM e comentário | ver §10 (pedir ≠ ter Advanced Access) |
> 48	| BYOK pool | `supabase/functions/_shared/provider-keys.ts:37-91` (`resolveProviderKey`, guarda `.eq("user_id", userId)` :49) · migration `20260714030000:16-40,106-117` | resolução per-user fail-closed (explícito → pool → legado → 402) | **REUSAR**. Nunca `Deno.env.get(<provider>)` |
> 49	
> 50	### 2.2 Anatomia de um nó do Spaces (onde o `cadence` se pluga)
> 51	
> 52	Rota viva: `src/App.tsx:153` → **`CanvasEditorPage`** (motor Canvas Studio; `SpaceCanvasPage`/`useSpacesStore` é código morto). Um nó novo custa **6 edições manuais** (não há registry único):
> 53	
> 54	1. `src/types/canvas.ts` — `CanvasNodeKind` (:19-32) + `CadenceData` + union `CanvasNodeData` (:648-661) + `makeDefaultCadence` (molde :986-1007) + **`case "cadence": return null;`** em `resolveExecutePayload` (:1064-1182) + **`case "cadence": return 0;`** em `estimateNodeCost` (:1211-1241).
> 55	2. `src/lib/canvas-node-registry.ts` — 1 entrada (`category: "Publish"`, aliases pt-BR: cadência/agendar/recorrente/cron/calendário).
> 56	3. `src/components/canvas/nodes/CadenceNode.tsx` — molde `PublishSocialNode` (só `<Handle>` target `input_asset`, id inline).
> 57	4. `src/pages/CanvasEditorPage.tsx:63-77` — `nodeTypes`.
> 58	5. `src/components/canvas/RightPanel/index.tsx:23-110` — 1 ramo na ternária.
> 59	6. `src/components/canvas/RightPanel/inspectors/CadenceInspector.tsx`.
> 60	
> 61	**Caminho de execução:** (b) **edge function própria** — não `canvas-execute`. Enfiar um `node_type` novo no `canvas-execute` custa 4 listas hardcoded (slice-gate `index.ts:1233-1244` → 422 · `NODE_TYPE_MAP` :280-299 · `CREDIT_COSTS` :17-55 · `LEDGER_SYNC_NODE_TYPES` `useCanvasStudio.ts:218-226`) + o enum `vm_node_type` no DB. Cadência não gera mídia ⇒ não passa por ali.
> 62	
> 63	**Armadilhas do motor (documentadas, não inventar):**
> 64	- `estimateNodeCost` **não tem case para `publishSocial`** → `undefined` em runtime; `tsconfig.app.json:25 strict:false` não avisa. Um kind esquecido nesse switch faz `runAllCost` virar NaN (`useCanvasPipeline.ts:55-57`).
> 65	- `useCanvasPipeline.ts:33-50`: "runnable" exige `prompt` não-vazio ⇒ `cadence` **precisa** entrar na lista de exclusão (como `characterReference`/`productList`) ou ganhar regra própria.
> 66	- `src/lib/canvas-handles.ts` é **código morto** (5 kinds, importado só pelo teste). Handles são strings inline. Não estender.
> 67	- Poll assíncrono: copiar `useVoiceRenderPoll` (id no `data` do nó, sobrevive a refresh) — **nunca** o loop `sleep(8s)×25` de `CinematicVideoInspector.tsx:53-70`.
> 68	
> 69	### 2.3 O gap real (prova negativa)
> 70	
> 71	- **Não existe nó de cadência no canvas.** `canvas-node-registry.ts` tem 12 kinds; grep `cadenc|schedul|agend` = 0.
> 72	- **Não existe recorrência em `scheduled_posts`.** grep `rrule|recurrence|recurring|repeat_every` em todas as migrations = 0. A única recorrência do sistema é `autopilot_plans.next_run_at + interval_days`.
> 73	- **Não existe hora-do-dia, weekday nem timezone em nenhuma cadência.** `profiles.timezone` existe (`…20260402014040…:23`, default `America/Sao_Paulo`) e tem **zero consumidores** (só `types.ts:2942`).
> 74	- **`campaign_steps` não tem noção de tempo** (`…20260603025256…:39-53`); `campaign-run` dispara tudo em paralelo (`index.ts:8,126-130`).
> 75	- **Não existe tabela de mensagem/thread social.** Só `aios_threads`/`aios_messages` (chat interno de agentes, `…20260606180000…:16-24`).
> 76	- **Não existe DM-listener.** `instagram-webhook` itera só `entry.changes` — um DM real seria descartado com **200 OK** (falso-sucesso perfeito).
> 77	- **Não existe outbound de mensagem em canal nenhum.** FR-META-005 (WhatsApp dispatcher) está em `docs/bok/meta-api/04-frd.md:30` e **nunca foi implementado**.
> 78	- **`whatsapp-webhook` está INALCANÇÁVEL:** sem bloco `[functions.whatsapp-webhook]` em `supabase/config.toml` (grep `whatsapp` → NO MATCH) ⇒ `verify_jwt` default **true** ⇒ a Meta leva **401 no gateway**. Compare com os 4 webhooks que têm o bloco (:82,85,91,94). Todo o ingestor é código morto. **P0.**
> 79	- **Bug de segurança menor:** `whatsapp-webhook/index.ts:45` compara HMAC com `===` (não timing-safe) e reimplementa a verificação; o helper `timingSafeEqual` de `_shared/oauth-state.ts` já existe e é usado pelo `instagram-webhook`.
> 80	- **Sem SOP (Lei 2) e sem FR/BoK** de cadência ou inbox. `ls docs/processes/ | grep -iE 'cadence|schedul'` → só `autopilot-cron-identity.md`, `autopilot-video-9x16.md`, `content-cadence-strategy.md` (este último é **plano**, não execução).
> 81	
> 82	---
> 83	
> 84	## §3 Posicionamento vs. ManyChat — **HIPÓTESE NÃO VERIFICADA**
> 85	
> 86	> 🚫 **SELO DE NÃO-VERIFICAÇÃO (Lei 1).** A tabela comparativa que existia aqui fazia ~12 afirmações factuais sobre o produto de um terceiro (ManyChat) **sem uma única URL** — violando a regra que este próprio doc escreve no cabeçalho (§0: *"Toda afirmação externa carrega URL"*). Nenhuma delas foi verificada nesta rodada de deepsearch. **Foram removidas em vez de mantidas sem âncora.** A linha mais perigosa era "Broadcast/newsletter por DM (IG): vendido como feature" — ela afirmava que um concorrente **vende** algo que §4/§10 declaram **impossível na plataforma**; se a imprecisão fosse nossa, seria a base de um pitch competitivo **falso**.
> 87	>
> 88	> **Proibido:** a MRD/BRD/SDD **NÃO pode citar §3 como fato**. Para reabilitar a comparação, ancorar cada linha em pricing/docs do ManyChat, **datada**, como o resto do doc.
> 89	
> 90	**Coluna MCORCH (essa sim, verificável no repo — §2.1) e o que dela decorre:**
> 91	
> 92	| Capacidade | MCORCH hoje (verificado no repo) | Veredito |
> 93	|---|---|---|
> 94	| Fluxo visual de conversa | Canvas Studio (ReactFlow) — de **mídia**, não de conversa | **Temos o canvas**; falta o `kind` |
> 95	| Comment→DM | 0 | **Novo** (§5.4) — vetor legal; ⚠️ **PROBE-GATED** (§7 Fatia 2 / FM-CAD-02): pode ser App-Review-gated |
> 96	| Keyword auto-reply em DM | 0 (webhook descarta) | **Novo** — mesmo gate PROBE acima |
> 97	| Broadcast/newsletter por DM (IG) | 0 | **Impossível no IG** (§4/§10) — a Meta não oferece OTN/News/Sponsored no IG |
> 98	| Drip/sequência com espera | `sequences`+`sequence_enrollments` (`nurture-dispatch`) — **gated**, e-mail | **Temos o motor**; falta o canal e o flip |
> 99	| Agendamento de **posts** | `scheduled_posts` + `auto-publish` + 3 seams | **Temos** |
> 100	| Geração do conteúdo agendado | pilar → `pillar_atoms` → `reshape-pillar` → `channel_variants` → carrossel/vídeo 9:16 | **Nosso fosso** |
> 101	| Atribuição de receita ao post/DM | UTM + afiliado + `creative_metrics` + `collective_efficiency_ledger` | **Nosso fosso** |
> 102	| E-mail | `nurture-dispatch` gated + `marketing_consents` + `erase_lead()` | **Quase** (falta BYOK Resend + flip) |
> 103	| SMS | 0 | **Deferido** (§4) |
> 104	| Telegram | bot `@claw_gcrux` (interno) | **Caminho mais barato** (§4) |
> 105	| WhatsApp | `meta_config` + webhook morto | BYOK viável (§4) |
> 106	| Ledger de custo por ação | mcoCoins 4×-floor + begin/finalize atômico | **Nosso fosso** |
> 107	
> 108	**Síntese honesta (sobrevive sem a tabela removida):** o MCORCH ganha em *conteúdo + dinheiro* — gera, distribui e **mede** o retorno. O nó de Cadência é a ponte para o inbound — e a ponte só é defensável se o inbound (comentário/DM) alimentar o mesmo `lead_events`/`creative_metrics` que já mede receita. **Ressalva de honestidade:** todo o inbound depende do probe de FM-CAD-02; até ele fechar, a ponte é **hipótese**, não capacidade.
> 109	
> 110	---
> 111	
> 112	## §4 Contrato dos canais
> 113	
> 114	| Canal | API existe? | Permissão / gate | BYOK viável? | Custo | URL |
> 115	|---|---|---|---|---|---|
> 116	| **Instagram DM (resposta)** | Sim — `POST /<IG_ID>/messages` em **graph.instagram.com** (flavor Instagram Login) | `instagram_business_basic` + `instagram_business_manage_messages`. **Janela de 24h** desde a última mensagem do usuário; **não existe DM proativo** | Sim (token já em `social_accounts`, refresh em `publish-social:85-109`) | US$0 (Meta) | https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api/ |
> 117	| **Instagram Private Reply (comentário→DM)** | Sim — `POST /<IG_ID>/messages` com `recipient={"comment_id":…}` | `instagram_business_manage_comments`. **7 dias** desde o comentário; **"Only one message can be sent to the commenter"** | Sim | US$0 | https://developers.facebook.com/docs/instagram-platform/private-replies/ |
> 118	| **Instagram (multi-tenant)** | — | **Advanced Access = App Review + Business Verification** ("Standard Access is available if your app serves Instagram professional accounts you own or manage") | — | — | https://developers.facebook.com/docs/instagram-platform/overview/ |
> 119	| **Facebook Messenger** | Sim — `POST /<PAGE_ID>/messages` em graph.facebook.com | `pages_messaging` + **Page access token** (outro token, outro host, outro objeto de webhook) | Sim, mas é outra integração | US$0 | https://developers.facebook.com/docs/messenger-platform/send-messages/ |
> 120	| **WhatsApp Cloud API** | Sim | **Opt-in obrigatório** (número + permissão explícita). Fora da janela de 24h, só **template APPROVED**. Msg não-template dentro da janela é **grátis** | **Sim — sem App Review**: "If you are a direct developer and only access your own business data, you do not need to undergo App Review" (tenant traz o próprio app + WABA + System User token) | Template pago por mensagem entregue (rate card externo — **não fabricar valores**); não-template grátis na janela; FEP 72h grátis | https://developers.facebook.com/documentation/business-messaging/whatsapp/permissions/ · https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing |
> 121	| **Telegram Bot** | Sim | `@BotFather`. **Zero review.** Bot não fala com quem nunca deu `/start` (opt-in estrutural) | Sim (bot token per-user no pool BYOK) | **US$0** (~30 msg/s grátis) | https://core.telegram.org/bots · https://core.telegram.org/bots/faq |
> 122	| **E-mail (Resend)** | Sim | Só verificação de domínio (SPF/DKIM/DMARC). **Sem review.** CAN-SPAM: rodapé + endereço postal + opt-out honrado ≤10 dias úteis | Sim (chave per-user cifrada) | Free 3.000/mês (100/dia, 1 domínio); Pro US$20 (50k) | https://resend.com/pricing · https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business |
> 123	| **X / Twitter DM** | Sim — `POST /2/dm_conversations/with/:id/messages` | scopes `dm.write`+`dm.read`+`tweet.read`+`users.read` ⇒ **reconexão OAuth** do tenant. Automação só em modo reply/opt-in explícito | Sim | **Pay-per-use, sem tier grátis** (4×-floor ⇒ **mco**): DM Create US$0,015 = **4 mco** · DM Event Read US$0,010 = **3 mco** · **Post com URL US$0,200 = 45 mco** (4,5× um `orchestrate-content` inteiro — §5.5/OTD-CAD-011) | https://docs.x.com/x-api/direct-messages/manage/integrate.md · https://docs.x.com/x-api/getting-started/pricing · https://help.x.com/en/rules-and-policies/x-automation |
> 124	| **TikTok DM** | **Não** pela credencial que temos — o scopes reference (developers.tiktok.com) só tem `local.* portability.* research.* user.* video.*` (zero DM, zero comment) | TikTok **Business Messaging** existe (business-api, outro eixo): negócio **não pode iniciar**; janela 48h; teto 10 msgs. **⚠️ ver §10.11** — confirmado sem ressalva apenas: **EEE/Suíça/UK não podem**; LatAm (Brasil) **dentro**; restrições extras de mídia em 14 países ⇒ **capability-flag por tenant/região**, não toggle global. **Âncora = help-center de BSP, NÃO fonte primária do TikTok** | Só via novo bloco de credencial | Gratuito (segundo BSPs — não primária) | https://developers.tiktok.com/doc/tiktok-api-scopes · https://respond.io/help/tiktok/tiktok-overview |
> 125	| **TikTok comment reply (orgânico)** | **NÃO CONFIRMADO** — portal é SPA, não renderizou. Só provado o par `/open_api/v1.3/comment/*` (contexto de **ads**) | — | — | — | https://raw.githubusercontent.com/tiktok/tiktok-business-api-sdk/main/python_sdk/docs/CommentsApi.md |
> 126	| **LinkedIn DM** | **SEM CAMINHO LEGÍTIMO** — "restricted to approved partners" e **"Member actions do not include an automated or scheduled event"** | — | — | — | https://learn.microsoft.com/en-us/linkedin/shared/integrations/communications/messages |
> 127	| **LinkedIn comment reply** | Sim — `POST /rest/socialActions/{urn}/comments` | `w_organization_social_feed` (⇒ **reconexão**) + **Community Management API** = aplicação com revisão da LinkedIn (não self-serve) | Sim | US$0 | https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/comments-api?view=li-lms-2026-05 · https://developer.linkedin.com/product-catalog/marketing/community-management-api |
> 128	| **Discord DM** | Sim tecnicamente | **Política proíbe** marketing/DM não solicitado | — | — | https://docs.discord.com/developers/resources/user · https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy |
> 129	| **SMS (Twilio BR)** | Sim | long code = só P2P; A2P exige short code (2–4 sem.) ou alfanumérico (~10 sem.); **proibido marketing fora de 09h–22h e aos domingos** | Sim | US$0,0599/segmento + US$1,15/mês por número | https://www.twilio.com/en-us/sms/pricing/br · https://www.twilio.com/en-us/guidelines/br/sms |
> 130	
> 131	**Regra de precedência (obrigatória para quem escrever a SDD):** **nenhuma linha de §4 pode contradizer §10.** §10 é o **superset** da verificação adversarial — onde houver divergência, §10 vence e a linha de §4 está errada.
> 132	
> 133	**Marcados SEM caminho legítimo (não oferecer na UI, nem como "em breve"):** LinkedIn DM automatizada · Discord DM de marketing · cold DM em qualquer canal · broadcast por DM no Instagram · TikTok DM pela credencial atual.
> 134	
> 135	---
> 136	
> 137	## §5 Arquitetura proposta
> 138	
> 139	### 5.1 O nó `cadence` (front)
> 140	
> 141	`CadenceData` = `{ kind:'cadence', label, status, sourceAssetId?: string (creative_assets.id, owner-scoped), planId?: string (`autopilot_plans.id` com `plan_kind='cadence'`), program: CadenceStep[], enabled: boolean, output?, error? }`.
> 142	
> 143	- Categoria no registry: **Publish** (é sink/distribuição).
> 144	- `resolveExecutePayload` → `null`; `estimateNodeCost` → **0** — **e isto NÃO viola G7 (quote == charge)**, porque o nó `cadence` não é a unidade de cobrança: **criar um plano** genuinamente não gasta nada. A cobrança acontece no **ciclo**, pelo par `begin`/`finalize`, e é lá que `quote == charge` vale (o ciclo cota e cobra o mesmo número). Escopo do invariante: **nível do ciclo, não do nó** — dito explicitamente para as duas afirmações não se contradizerem.
> 145	- **Obrigação compensatória (senão o 0 mente):** o **inspector DEVE exibir o custo projetado por ciclo** = `Σ (custo em mco de cada canal do plano) × ocorrências até o cap`. Com o X publicando com link a **45 mco/post** (§5.5), um plano diário de 30 dias projeta **1.350 mco** — o Sovereign precisa ver essa magnitude **antes** de armar o plano, não depois. `budget_cap_mco` é **NOT NULL** e expresso **em mcoCoins** (nunca em USD).
> 146	- Excluído do gate "runnable" de `useCanvasPipeline.ts:33-50` (não tem `prompt`).
> 147	- Inspector chama a edge fn `cadence-plan` (upsert do plano + arm) e mostra `next_run_at` + últimas N dispatches. Poll no molde `useVoiceRenderPoll`.
> 148	
> 149	### 5.2 O motor (Postgres-first — zero infra nova)
> 150	
> 151	Referências de desenho (semântica adotada, **stack rejeitada**): Knock (schedule recipient-timezone-aware, `repeats[]` com frequency/interval/days/hours/minutes múltiplos de 5 — https://docs.knock.app/concepts/schedules), Novu (Digest/Throttle/Delay como **steps** — https://docs.novu.co/framework/digest · https://docs.novu.co/platform/workflow/add-and-configure-steps; mas a stack é Mongo+Redis+worker — https://dev.to/elie222/inside-the-open-source-novu-notification-engine-311g ⇒ **anti-referência de infra**), Temporal (Overlap Policy / Catchup Window / Jitter — https://docs.temporal.io/schedule), Dittofeed (Delay *Localized* com cascata de timezone; Random Bucket determinístico por hash do id — https://docs.dittofeed.com/resources/journey-nodes/delay · https://docs.dittofeed.com/resources/segment-nodes/random-bucket; mas roda em Temporal+ClickHouse ⇒ rejeitar stack — https://github.com/dittofeed/dittofeed), Trigger.dev (idempotencyKey: falha **libera** a chave, sucesso **prende** — https://trigger.dev/docs/idempotency), River (unicidade por **índice parcial único** + `ON CONFLICT` retornando o job existente, dimensão `ByPeriod` = tempo arredondado — https://riverqueue.com/docs/unique-jobs), Inngest (vocabulário: throttle ≠ rate limit ≠ debounce — https://www.inngest.com/docs/guides/flow-control), Unleash (bucketing consistente por hash — https://docs.getunleash.io/concepts/stickiness).
> 152	
> 153	**Schema — ESTENDER o trilho vivo (default), não criar um paralelo:**
> 154	
> 155	O MCORCH já roda **dois** motores de recorrência idênticos em produção (`autopilot-cadence-cron` + `nurture-advance`: pg_cron → edge com gate Bearer → scan de `next_run_at` por índice parcial → fan-out bounded). Um **terceiro** não é "cópia mecânica" barata: é o **triplo** de tudo o que precisa ser mantido correto. Default do OTD-CAD-003 = **migration única sobre `autopilot_plans`**:
> 156	
> 157	```
> 158	ALTER TABLE autopilot_plans
> 159	  DROP CONSTRAINT <platforms_check>,                       -- allowlist passa a derivar de channel_profiles
> 160	  ADD COLUMN plan_kind text NOT NULL DEFAULT 'viral'
> 161	      CHECK (plan_kind IN ('viral','cadence')),
> 162	  ADD COLUMN recurrence jsonb,                             -- {frequency, days, hours, minutes, tz}
> 163	  ADD COLUMN quiet_hours jsonb,
> 164	  ADD COLUMN overlap_policy text DEFAULT 'skip',
> 165	  ADD COLUMN catchup_window interval DEFAULT '6 hours',
> 166	  ADD COLUMN jitter_seconds int DEFAULT 0,
> 167	  ADD COLUMN program jsonb,                                -- steps; molde `sequences.steps` + `current_step`
> 168	  ADD COLUMN channel_allowlist text[],                     -- por plano, não constante (§7)
> 169	  ADD COLUMN budget_cap_mco int NOT NULL;                  -- em mcoCoins, nunca em USD (§5.5)
> 170	```
> 171	
> 172	E **generalizar o re-arm** de `autopilot-run/index.ts:310-314` (`now + interval_days`) para o calculador UTC de `{frequency, days, hours, minutes, tz}`. O `program jsonb` **reusa** o modelo `steps jsonb + current_step + next_run_at` de `sequences`/`sequence_enrollments` (§2.1) — não é um formato novo.
> 173	
> 174	**Custo explícito se o Sovereign escolher tabela nova** (não é o default; se escolher, o blueprint carrega a conta): **3** índices due · **3** kill-switches · **3** modelos de cap · **3** superfícies de auditoria de identidade cron. E mesmo nesse caminho, **reusar o MESMO job pg_cron** (o tick varre as duas tabelas) — **nunca** um 3º job: o próprio Supabase recomenda ≤~8 jobs concorrentes (https://supabase.com/docs/guides/cron).
> 175	
> 176	**Tabelas genuinamente novas (não existe equivalente):**
> 177	
> 178	- `cadence_dispatches` — ledger por tentativa: `plan_id · step_index · occurrence_at · idempotency_key · channel · status · target_ref · error · external_usd_cost numeric · cost_source text`.
> 179	  - **Índice único PARCIAL, predicado declarado** (é ele que decide se FM-CAD-01/03 são impedidos ou só prometidos):
> 180	    `CREATE UNIQUE INDEX cadence_dispatches_idem ON cadence_dispatches (idempotency_key) WHERE status <> 'failed';`
> 181	  - **Consequência assumida: NÃO é append-only puro** (o molde `lead_events` não serve aqui). Para a semântica Trigger.dev ("falha **libera** a chave, sucesso **prende**") a linha precisa transicionar de status ⇒ RLS = **select_own** (cliente lê) + **insert service-role** + **update service-role** (`status`, `error`, `external_usd_cost`). **O cliente nunca escreve.**
> 182	  - Alternativa (decisão Sovereign): manter append-only puro e aceitar **at-most-once** — falha = desistir, sem retry. As duas semânticas **não coexistem**; escolher uma.
> 183	  - `external_usd_cost` + `cost_source` são gravados **no reconcile** (webhook de status), nunca no 202 — ver §5.5 (custo do tenant é **medido** mesmo quando **não é cobrado**).
> 184	- `social_threads` / `social_messages` — obrigatórias: a Conversations API só devolve **"details about the 20 most recent messages"** (https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/conversations-api/) ⇒ a Meta **não é** banco de histórico. Colunas de relógio: `csw_expires_at` (24h, derivado do inbound no **servidor**) e, por comentário, `private_reply_deadline` (7d) — **dois relógios distintos** (§10).
> 185	
> 186	**Driver:** **nenhum job pg_cron novo.** O tick existente `autopilot-cadence-cron` (*/15, gate `Authorization !== Bearer SB_SECRET_KEY` → 403, `user_id` **server-trusted da linha, nunca do body** — SOP `docs/processes/autopilot-cron-identity.md`) passa a **rotear por `plan_kind`**: `viral` → `autopilot-run` (como hoje); `cadence` → `cadence-run` (edge nova). pg_cron **não sobrepõe a mesma job** ("only one instance of each specific job at a time… queued" — https://github.com/citusdata/pg_cron) e roda em **GMT** ⇒ preferência de horário **jamais** vira cron expression: é computada em UTC e gravada em `next_run_at`.
> 187	
> 188	**Claim do drain:** `SELECT … FOR UPDATE SKIP LOCKED` ("can be used to avoid lock contention with multiple consumers accessing a queue-like table" — https://www.postgresql.org/docs/current/sql-select.html). Upgrade path documentado e **não adotado** na Fatia 1: pgmq / Supabase Queues (https://github.com/pgmq/pgmq · https://supabase.com/docs/guides/queues) e Hatchet (MIT, Postgres — https://docs.hatchet.run/home).
> 189	
> 190	### 5.3 State machine e invariantes
> 191	
> 192	`plan(active) → tick(due) → resolve subject (owner-scoped) → gate chain → dispatch → ledger → re-arm(next_run_at) | deactivate`.
> 193	
> 194	- **Idempotência:** chave `(plan_id, step_index, occurrence_at)` com `INSERT … ON CONFLICT DO NOTHING RETURNING` (mesmo truque de `begin_space_generation:83-131`), sob o índice **único parcial com predicado declarado** em §5.2: `… (idempotency_key) WHERE status <> 'failed'`. É o predicado — e **só ele** — que produz a semântica "**falha libera a chave** (permite retry) / **sucesso prende** (impede double-post)". Corolário assumido em §5.2: o ledger **não** é append-only puro (precisa de `UPDATE` service-role-only de `status`); se o Sovereign preferir append-only puro, a semântica cai para **at-most-once** (sem retry). Não há terceira opção.
> 195	- **Overlap:** default `skip` (ciclo anterior ainda rodando ⇒ pula, não empilha).
> 196	- **Catchup:** janela limitada (default 6h) — sem ela, uma queda de 6h dispara o backlog inteiro de uma vez.
> 197	- **Quiet hours:** janela `[start,end]` + weekdays no **fuso do sujeito**, cascata `autopilot_plans.recurrence->>'tz' → profiles.timezone → America/Sao_Paulo` (o `profiles.timezone` sai de dado morto para SSOT).
> 198	- **Frequency cap:** chave `(user_id, channel)` + janela + threshold, com **HALT** (não reenfileiramento) — semântica Knock. Teto autoritativo = `channel_profiles.cadence` (`target_per`/`count_min`/`count_max`), que assim ganha o **primeiro leitor** do repo.
> 199	- **Dedup/digest:** `digestKey = (user, channel, dia)` colapsa N vencimentos do mesmo canal em **1** publicação (ou 1 carrossel) — é a diferença entre cadência e flood.
> 200	- **A/B determinístico:** fórmula **exata** que a SDD deve copiar literalmente —
> 201	  `mod(abs(hashtext(subject_ref || ':' || experiment_key)::bigint), 100) < ratio`
> 202	  ⚠️ **Não** usar `hashtext(...) % 100 < ratio`: `hashtext()` retorna `integer` **com sinal**, e em Postgres `-42 % 100 = -42`, que é `< ratio` para **qualquer** ratio ≥ 0 ⇒ ~50% dos sujeitos cairiam no bucket A independentemente do ratio, enviesando o experimento **sem quebrar nada** (mente em silêncio). O cast para `bigint` vem **antes** do `abs` porque `abs(int4min)` estoura. Estável entre retries (`random()` por execução reamostra e destrói a métrica). Loop fecha em `creative_metrics.hook_rate` (migration `20260627150000`).
> 203	- **Opt-out:** checado **no send**, não no enqueue, e **independente da base legal** (LGPD Art. 18 §2).
> 204	- **Reconciliação:** nunca reportar "enviado" a partir do 202 da API — só do webhook de status (a Meta aplica "per-user marketing template message limits" fora do nosso controle — https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview). Sem isso o sistema mente (Lei 1).
> 205	
> 206	### 5.4 O laço comercial (o que faz "ir além do ManyChat")
> 207	
> 208	> ⚠️ **Tudo abaixo da linha `instagram-webhook` é PROBE-GATED** (FM-CAD-02, RPN 486): sob Standard Access o webhook pode não entregar DM de terceiro sem role ⇒ o laço inbound é **hipótese** até o probe de §7 Fatia 2 fechar. O ramo **acima** (agendar→publicar) é a Fatia 1, sem gate externo.
> 209	
> 210	```
> 211	pilar → atomiza → reshape por canal → autopilot_plans(plan_kind='cadence') agenda → scheduled_posts → auto-publish publica
> 212	                                                                                    ↓
> 213	                                    instagram-webhook (entry.changes: comments  |  entry.messaging: DM)
> 214	                                                                                    ↓
> 215	                                    lead_events(message_received) + leads + notify() → social_threads
> 216	                                                                                    ↓
> 217	                          gate chain → private reply 1× (≤7d, UNIQUE comment_id) ou resposta in-window (≤24h)
> 218	                                                                                    ↓
> 219	                                          link afiliado + UTM → creative_metrics → collective_efficiency_ledger
> 220	```
> 221	
> 222	⚠️ **Antes de escrever o branch `entry.messaging`: provar o shape com um DM real** (log do payload cru). A doc do IG só publica exemplo com `entry[].changes` (§10) — codar às cegas inverte o falso-sucesso.
> 223	
> 224	### 5.5 BYOK (API Tenancy Model)
> 225	
> 226	- Provider LLM (se um passo `generate` existir): `resolveProviderKey(admin, userId, provider, keyId)` — **nunca** `Deno.env.get(<provider>)`.
> 227	- Telegram: `telegram_bot_token` no pool per-user (coluna cifrada + UI Settings + fail-closed 402 `telegram_not_configured`).
> 228	- Resend: `resend_api_key` per-user cifrada + domínio verificado **do tenant**.
> 229	- WhatsApp: **o tenant traz o próprio app Meta + WABA + System User token + método de pagamento** ⇒ **cobrança em mco = 0** (o MCORCH não revende mensagem; quem paga a Meta é o tenant).
> 230	  - ⚠️ **"Não cobrar" ≠ "não medir".** Combinado com OTD-CAD-009 (a Meta cobra AI Providers por **cada mensagem não-template** entregue no Brasil), o desenho ingênuo produziria: a Meta debita o tenant a cada auto-resposta enquanto o ledger do MCORCH mostra **zero**. Isso destruiria o fosso que o §3 reivindica ("Ledger de custo por ação") e envenenaria a `collective_efficiency_ledger` (mco/resultado deixaria de refletir a verdade financeira do ciclo) — **o sistema mentiria por omissão (Lei 1)**.
> 231	  - **Obrigatório:** `cadence_dispatches.external_usd_cost numeric` + `cost_source text`, gravados **no reconcile** (webhook de status), nunca no 202. Cobrança mco = 0; **custo REGISTRADO** e agregado no ledger de eficiência. Mesma regra vale para qualquer canal BYOK cujo custo externo o tenant absorva.
> 232	  - Consequência dura: em BYOK **cada tenant tem o próprio app secret e o próprio verify token** ⇒ o `whatsapp-webhook` (que hoje valida contra segredo **global** e com `===`) precisa resolver o tenant pelo `phone_number_id`/`waba_id` (bloco :120-132 já faz) e **então** buscar o app secret daquele tenant e validar com `timingSafeEqual`.
> 233	- **Instagram / Messenger — NÃO é BYOK-de-app** (declaração explícita, ver OTD-CAD-018): os tokens per-user de `social_accounts` são **mintados pelo app Meta GLOBAL do MCORCH** (`social-auth-init` usa client_id/secret de **sistema**), e o HMAC do `instagram-webhook` valida contra o app secret **global**. É um **fallback restrito** do API Tenancy Model, consciente — e traz **blast radius de app compartilhado**: o spam de **um** tenant pode banir o app de **todos**, e o rate limit **app-level** é recurso comum esgotável por um único tenant. Consequências obrigatórias no desenho: cap de fan-out **por APP** (além do por-tenant), **kill-switch global** (além do `is_active` por plano) e telemetria de feedback negativo agregada **no nível do app**.
> 234	- X: DM Create **US$0,015** ⇒ **cobra mcoCoins**: `mco = ceil(usd/0.018 × 4)` ⇒ `ceil(0.015/0.018×4) = ceil(3,33) = **4 mco**` por DM.
> 235	  E **`Post: Create (with URL) = US$0,200/req` ⇒ `ceil(0.200/0.018 × 4) = ceil(44,4) = 45 mco` por post do X com link** — **4,5× um `orchestrate-content` inteiro** (10 mco), num nó cujo quote diz 0. Este número (não o USD) é o que entra na tabela do §4 e no OTD-CAD-011: o Sovereign precisa ver a **magnitude em mco**. Hoje o motor de afiliados publica com link e trata isso como **custo zero**.
> 236	- Custo interno (LLM de variação, se houver): begin/finalize atômico obrigatório. **G7 (quote == charge) é invariante do CICLO** (`begin`/`finalize` cotam e cobram o mesmo), **não do nó** — o nó `cadence` cota 0 porque criar plano não gera (§5.1).
> 237	
> 238	---
> 239	
> 240	## §6 Guardrails de compliance (o que o sistema IMPEDE por construção)
> 241	
> 242	| # | Regra externa | O que o sistema impede **estruturalmente** |
> 243	|---|---|---|
> 244	| G1 | "Conversations only begin when an Instagram user sends a message… Your app has 24 hours to respond" (https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api/) | A fila de DM tem **FK NOT NULL** para um inbound (`lead_events.event_type='message_received'` do mesmo `user_id`). **Sem inbound, a linha não existe** ⇒ cold DM é impossível de representar. O relógio deriva do `created_at` do inbound **no servidor** |
> 245	| G2 | Private reply: "sent within 7 days" + **"Only one message can be sent to the commenter"** (https://developers.facebook.com/docs/instagram-platform/private-replies/) | **UNIQUE(comment_id)** na fila (idempotência vira requisito de **política**, não de UX — retry duplicado é violação). CHECK de idade **no send**, não no enqueue |
> 246	| G3 | Meta Dev Policy §5: consentimento legalmente suficiente + "meio adequado… para solicitar o cancelamento, de forma contínua. Respeite imediatamente" + "não deve receber uma quantidade excessiva de feedback negativo" (https://developers.facebook.com/devpolicy/) | Opt-out injetado pelo **servidor** em toda thread automatizada; `withdrawn_at` checado **no instante do send** com cancelamento em cascata da fila; limiar de feedback negativo **auto-imposto e conservador** (a Meta não publica número — §10) com **kill-switch** = `is_active=false` |
> 247	| G4 | Meta/Community Standards: proíbe frequência muito elevada e **engagement-gating** (https://transparency.meta.com/policies/community-standards/spam/) | Caps `daily`/`budget` **NOT NULL** (clone de `autopilot_plans:28`); fan-out sempre bounded. Validação de **template** no servidor: o comment→DM não pode ser a **única** via de acesso ao conteúdo |
> 248	| G5 | Human Agent tag (7d) exige App Review + Business Verification e é para **resposta manual** (https://developers.facebook.com/docs/features-reference/human-agent) | A tag é **fisicamente inalcançável** do caminho service-role/pg_cron — separação de caminho, **não um `if`**. Só edge fn com JWT de usuário em sessão interativa pode setá-la |
> 249	| G6 | Fora da janela de 24h: **nada promocional** (https://developers.facebook.com/docs/messenger-platform/policy/policy-overview/) | Classificador in/out-window roda no **servidor** e bloqueia o send — nunca confiar no LLM que escreveu o texto |
> 250	| G7 | WhatsApp: só contatar com número fornecido **e** opt-in explícito; opt-out vale mesmo se recebido **fora** do WhatsApp (https://whatsappbusiness.com/pt-br/policy/) | Enqueue WhatsApp exige linha em `marketing_consents` com `granted_at` **e** `source_proof` NOT NULL para aquele lead **e categoria** ⇒ senão **422 `whatsapp_opt_in_missing`**. Revogação é por **pessoa**, não por canal |
> 251	| G8 | LGPD Art. 8 §2 (ônus da prova é do controlador) · §4 (autorização genérica é **nula**) · §5 (revogação **gratuita e facilitada**) (https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) | `marketing_consents.basis` vira **gate de enqueue** (fail-closed); consentimento é **por finalidade/categoria/canal**; rota **pública** de opt-out por token assinado (sem login, sem custo, sem pedir dado extra) |
> 252	| G9 | LGPD Art. 16/18 VI (eliminação) | `erase_lead()` (`…20260603000000…:130-169`) hoje **não cancela agendamentos futuros** ⇒ o direito de eliminação vira ficção. Fix obrigatório: cancelar em cascata `scheduled_posts` + fila de DM **na mesma transação** (OTD-CAD-006) |
> 253	| G10 | CAN-SPAM: rodapé com endereço postal + identificação como anúncio + opt-out ≤10 dias úteis, processável ≥30 dias; **B2B sem exceção**; **co-responsabilidade** de quem contrata o envio (https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) | O rodapé é montado pelo **servidor** e concatenado ao corpo — **jamais** delegado ao prompt do LLM (o `nurture-dispatch` gera o corpo por IA; uma alucinação = penalidade **por e-mail**). Limites impostos pela plataforma a **todos** os tenants, não configuráveis |
> 254	| G11 | ePrivacy 13(1)/(2)/(4) + GDPR Art. 21(2)(3): direito de oposição a marketing direto é **absoluto** e o aviso vem **na primeira comunicação**, "clearly and separately" (https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32002L0058 · https://gdpr-info.eu/art-21-gdpr/) | Gate de **jurisdição**: lead sem país conhecido ⇒ tratar como UE (opt-in prévio). Fail-closed por default |
> 255	| G12 | **EU AI Act Art. 50(1)** — informar que se interage com IA; vigência **2026-08-02** (~3 semanas) (https://artificialintelligenceact.eu/article/50/) + California BOT Act §17941 (https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17941.) | **Disclosure de IA injetado pelo servidor** na primeira mensagem de toda thread automatizada, em bloco separado (resolve AI Act + GDPR 21(3) de uma vez). Nunca via prompt |
> 256	| G13 | Instagram remove engajamento inautêntico de apps de terceiros (https://about.instagram.com/blog/announcements/reducing-inauthentic-activity-on-instagram) | **Proibição perene:** nenhuma automação de mensagem/engajamento via browser headless. `agent-browser` é ferramenta de QA. Guardrail executável: smoke/IoC que **falha** se script fora de `scripts/qa/` importar o driver de browser e tocar `instagram.com`/`facebook.com` |
> 257	| G14 | Templates WhatsApp podem ser **recategorizados** (utility→marketing) com 1 dia de aviso (https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization) | Assinar `message_template_status_update`; validar `APPROVED` + categoria **no momento do send**, nunca no do agendamento (mesmo princípio do `auto-publish` resolvendo asset owner-scoped na hora) |
> 258	
> 259	---
> 260	
> 261	## §7 Fatiamento
> 262	
> 263	**Fatia 0 — pré-requisitos (P0, sem os quais tudo é falso-sucesso):**
> 264	1. Bloco `[functions.whatsapp-webhook] verify_jwt = false` em `supabase/config.toml` (hoje ausente ⇒ 401 no gateway).
> 265	2. `whatsapp-webhook` → `timingSafeEqual` (`_shared/oauth-state.ts`) + destino `leads`/`lead_events` (não `whatsapp_leads`, absorvida por OTD-MH-001).
> 266	3. `estimateNodeCost`: adicionar `publishSocial` (bug aberto) antes de somar `cadence`.
> 267	4. `erase_lead()` cancela fila pendente em cascata (G9).
> 268	5. **Migrar `auto-publish` de crontab de SO para pg_cron + `FOR UPDATE SKIP LOCKED`** (OTD-CAD-004). **É pré-requisito, não pergunta:** o próprio gate do OTD-CAD-004 diz "antes de ligar recorrência". A Fatia 1 é o **único** entregável sem gate externo — não pode nascer sobre o elo mais fraco (sink sem lock, num único host de SO). Sai do §11 (era pergunta aberta) e entra aqui.
> 269	
> 270	**Fatia 1 — "Cadência de Publicação" (ZERO app review, valor visível ao Usuário Zero e a QUALQUER tenant):**
> 271	- `kind: cadence` no canvas + `autopilot_plans` estendido (`plan_kind='cadence'`, §5.2) + `cadence_dispatches` + roteamento `plan_kind` no tick existente + `cadence-run`. **Nenhum job pg_cron novo.**
> 272	- Sujeito = **asset existente** (`creative_assets.id`, owner-scoped) ⇒ **0 mco, keyless, sem ledger de geração**.
> 273	- Sink = `scheduled_posts` (contrato `metadata.reshape` + `schedule:true`/`publish_at` do Amendment 22) — **já sobre pg_cron + lock** (Fatia 0 item 5).
> 274	- Ganhos que **ninguém mais tem**: hora-do-dia + weekday + **timezone** (ressuscita `profiles.timezone`), quiet hours, frequency cap lendo `channel_profiles.cadence` (ressuscita o dado morto), dedup/digest, A/B determinístico, overlap/catchup/jitter, idempotência por índice único.
> 275	- **Canais da Fatia 1 = allowlist de `auto-publish` MENOS X** (WordPress, LinkedIn, IG, TikTok, YouTube, Pinterest — via os seams existentes). **X entra só depois** que o probe do Developer Console fechar OTD-CAD-011 (o post-com-link custa **45 mco** e a conta pode estar **quebrada/sangrando agora**). Isso é `channel_allowlist` **de plano** (coluna em §5.2), **não** uma constante hardcoded. **Nenhuma mensagem privada.**
> 276	
> 277	**Fatia 2 — PROBE-GATED: Inbox IG (destravada SÓ por DM real de terceiro sem role):**
> 278	- **Item 1 (o probe, não o critério de aceite):** provar com uma conta IG **de terceiro sem role no app** mandando DM real e a linha aparecendo no banco. **Se não chegar ⇒ App Review é pré-requisito e a Fatia 2 inteira está bloqueada** (§8/FM-CAD-02, RPN 486). Nada abaixo começa antes disso; **zero FR de inbound no BoK 01→05 antes do payload cru**.
> 279	- `entry.messaging` + `comments` no `instagram-webhook` (**após o probe acima**) → `social_threads`/`social_messages` + `lead_events` + `notify()`.
> 280	- Private reply (comment→DM) com `UNIQUE(comment_id)` e deadline 7d; resposta in-window 24h.
> 281	- Nasce **`delivery: 'gated'`** (molde `nurture-dispatch:150`); flip para `'sent'` só com GO Sovereign.
> 282	
> 283	**Fatia 3 — "Canais desimpedidos" (BYOK, sem review de plataforma):** Telegram (US$0, opt-in estrutural via `/start`) + E-mail Resend (flip do `nurture-dispatch` com rodapé server-side G10).
> ```

## 🤖 Claude *(14:56:01)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking the documentation requirements against the BoK gate criteria—verifying that all 9 required files are present and identifying which ones cover the core deliverables (MRD through SDD) plus the supporting documents like data model and process flow.

</details>


## 🤖 Claude *(14:56:01)*

Let me read the SDD (Pattern Conformance §9) and the remaining blueprint, plus FRD/data-model/process-flow.

## 🤖 Claude *(14:56:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/05-sdd.md"
}
```

## 🤖 Claude *(14:56:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/00-deepsearch-blueprint.md",
  "offset": 284,
  "limit": 130
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 284	
> 285	**Fatia 4 — GATED (não prometer):** WhatsApp Cloud BYOK (tenant traz app+WABA+número+pagamento; fricção real: **apagar a conta WhatsApp do número** antes) · Instagram multi-tenant (**App Review + Business Verification**) · Messenger (`pages_messaging`, outro token) · LinkedIn comment reply (**aplicação ao Community Management API**, revisão da LinkedIn) · X DM (**reconexão OAuth** + custo pay-per-use) · TikTok DM/comment (**probe autenticado obrigatório** — hoje é hipótese).
> 286	
> 287	**Deferido explicitamente:** SMS (provisionamento de semanas + janela horária legal) · Discord (política proíbe) · LinkedIn DM (**sem caminho legítimo**).
> 288	
> 289	---
> 290	
> 291	## §8 OTDs e FMEA
> 292	
> 293	### OTDs
> 294	
> 295	| ID | Dívida | Ação | Gate/SLA |
> 296	|---|---|---|---|
> 297	| OTD-CAD-001 | `whatsapp-webhook` inalcançável (sem bloco no `config.toml`) e HMAC não timing-safe | Fatia 0 itens 1–2 | **P0** — antes de qualquer código de cadência |
> 298	| OTD-CAD-002 | Sujeito da cadência: asset existente vs. geração por ciclo | Fatia 1 = **asset existente** (0 mco). Geração ⇒ begin/finalize obrigatório | Decisão Sovereign |
> 299	| OTD-CAD-003 | `cadence_plans` nova vs. ampliar `autopilot_plans` | **Default = ESTENDER `autopilot_plans`** (§5.2): o CHECK de `platforms` é `ALTER … DROP CONSTRAINT` e as lacunas de hora/weekday/tz são `ADD COLUMN recurrence jsonb` — não fundam tabela paralela + 3º driver. Já existem **2** motores idênticos em prod; um 3º **triplica** índice due/kill-switch/cap/identidade cron. Se o Sovereign escolher tabela nova, o blueprint carrega o custo explícito **e reusa o MESMO job pg_cron** (tick varre as 2 tabelas), nunca um 3º | Decisão Sovereign |
> 300	| OTD-CAD-004 | `auto-publish` roda em **crontab de SO de um host** (sem pg_cron, sem lock) — a cadência herda essa confiabilidade | Migrar para pg_cron + `FOR UPDATE SKIP LOCKED` | **Fatia 0 item 5** (pré-requisito declarado pelo próprio gate — "antes de ligar recorrência" — não decisão aberta) |
> 301	| OTD-CAD-005 | Retry do carrossel IG pode criar children duplicados (`docs/bok/spaces-evolution/22-amendment-scheduled-carousel.md:27`) — a recorrência **amplifica** | Fechar antes de incluir carrossel na cadência, ou nascer com carrossel fora | Bloqueante da Fatia 1 p/ carrossel |
> 302	| OTD-CAD-006 | `erase_lead()` não cancela agendamentos futuros ⇒ direito de eliminação (LGPD Art. 16/18 VI) é ficção | Cascata na mesma transação | **P0 de conformidade** |
> 303	| OTD-CAD-007 | `estimateNodeCost` sem case `publishSocial` (undefined em runtime; `strict:false` esconde) | 1 linha | Fatia 0 |
> 304	| OTD-CAD-008 | `channel_profiles.cadence` é dado morto (0 leitores) — autoritativo ou sugestão? | Autoritativo (teto por canal) + contador de janela (**não existe hoje**) | Decisão Sovereign |
> 305	| OTD-CAD-009 | ENQUADRAMENTO **AI PROVIDER** no WhatsApp: a Meta cobra **cada mensagem não-template** entregue a usuários **no Brasil** por AI Providers (https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/ai-providers) ⇒ "responder na janela é grátis" pode **não valer** no mercado do Usuário Zero | Consultar Meta/rate cards **antes** de flipar auto-resposta para `'sent'` | **Bloqueante econômico** |
> 306	| OTD-CAD-010 | Legitimidade contratual do BYOK (SaaS armazenar o System User token do app do cliente pode caracterizar **Tech Provider**) | Revisão jurídica dos Meta Platform Terms antes de vender a terceiros | Antes do Usuário 1 |
> 307	| OTD-CAD-011 | X pay-per-use: **Post com URL = US$0,200/req ⇒ `ceil(0.200/0.018×4)` = **45 mco**/post** (4,5× um `orchestrate-content` inteiro de 10 mco) — o motor de afiliados publica com link e trata como **custo zero**; conta sem créditos = publish X **quebrado agora** | Probe no Developer Console (ação Sovereign) + gravar **45 mco** na tabela de custo (§4/§5.5). **Até fechar: X FORA da allowlist da Fatia 1** (§7) | **P1 financeiro** |
> 308	| OTD-CAD-012 | Divergência **entre duas docs oficiais** da Meta sobre rate limit do Send API (100 vs 300 calls/s) | Resolver empiricamente (`X-Business-Use-Case-Usage`) antes de dimensionar fan-out | Antes da Fatia 2 |
> 309	| OTD-CAD-013 | TikTok comment/DM orgânico: portal SPA, não renderizou ⇒ **hipótese** | Probe autenticado; **zero FR até prova** | Bloqueante da Fatia 4 (TikTok) |
> 310	| OTD-CAD-014 | **AI Act Art. 50(2)** (marcação machine-readable de conteúdo sintético) alcança Nano Banana / HyperFrames / Qwen3-TTS — **módulo próprio, maior que este** | Decisão de escopo (C2PA? watermark? metadata?) | **Vigência 2026-08-02** |
> 311	| OTD-CAD-015 | ANPD — Guia de Legítimo Interesse (fev/2024): não extraí texto literal | Até confirmar: exigir `basis='consent'` **fail-closed** no Brasil | Antes de aceitar `legitimate_interest` como gate |
> 312	| OTD-CAD-016 | Métrica que fecha o A/B: quem alimenta `creative_metrics.hook_rate` e com que latência? | Sem ingestão confiável, o A/B produz buckets bonitos e conclusão nenhuma | Antes de ligar A/B |
> 313	| OTD-CAD-017 | Frequency cap por `(user, channel)` ou `(user, channel, conta)`? `channel_profiles` não tem noção de conta (pool BYOK com 2 IGs) | Decisão Sovereign | Fatia 1 |
> 314	| OTD-CAD-018 | **IG/Messenger fora do BYOK-de-app**: os tokens per-user de `social_accounts` são mintados pelo app Meta **GLOBAL** do MCORCH e o HMAC do `instagram-webhook` valida contra o app secret **global** — regime **diferente** do WhatsApp (BYOK-de-app). Blast radius nunca nomeado: sob app compartilhado, spam de 1 tenant → **ban do app de TODOS**; rate limit app-level é recurso comum esgotável | **Decisão consciente = manter no app global** (fallback restrito do API Tenancy Model) COM: cap de fan-out **por APP** + kill-switch **global** + telemetria de feedback negativo **no nível do app**. **Alternativa** = BYOK-de-app para IG (espelha WhatsApp) ⇒ custo = UI + OAuth per-tenant | Decisão Sovereign — **antes do Usuário 1** |
> 315	
> 316	### FMEA (RPN = Severidade × Ocorrência × Detecção, 1–10)
> 317	
> 318	| ID | Modo de falha | S | O | D | RPN | Mitigação estrutural |
> 319	|---|---|:-:|:-:|:-:|:-:|---|
> 320	| FM-CAD-01 | **Double-post**: tick sobreposto/retry reenfileira e publica 2× | 8 | 7 | 4 | **224** | Índice **único parcial** em `idempotency_key` + `ON CONFLICT DO NOTHING RETURNING`; `overlap_policy=skip`; pg_cron não sobrepõe a mesma job |
> 321	| FM-CAD-02 | **Inbox nasce vazio** em prod: sob Standard Access o webhook pode entregar só de role users ("notifications from people who do not have a role on your app" exige **Advanced Access**) ⇒ time declara "funciona" testando com conta própria | 9 | 6 | **9** | **486** | Gate de materialidade Lei 1: DM real de **terceiro sem role**; sem isso, App Review vira pré-requisito da Fatia 2 |
> 322	| FM-CAD-03 | **Cold DM / janela expirada**: enfileira DM para o futuro e a janela fecha ⇒ violação de política (ban do app, não erro HTTP) | 10 | 6 | 5 | **300** | FK NOT NULL para inbound (G1); gate de janela **no send**; dois relógios distintos (24h CSW × 7d private reply) |
> 323	| FM-CAD-04 | **Opt-out ignorado** (revogação chega depois do enqueue) ⇒ LGPD Art. 8 §5 / sanção ANPD | 10 | 5 | 6 | **300** | `withdrawn_at` checado **no send**, independente da base legal; cascata no `erase_lead()` |
> 324	| FM-CAD-05 | **Falso-sucesso do 202**: reporta "enviado" sem webhook de status (Meta aplica per-user template limits fora do nosso controle) | 7 | 7 | 6 | **294** | Só marcar `sent` no webhook de status; reconciliação obrigatória (molde poll `video_renders`) |
> 325	| FM-CAD-06 | **Cron em GMT vira "toda segunda às 9h"**: horário do usuário expresso como cron expression ⇒ cadência multi-tenant errada por fuso | 6 | 8 | 5 | **240** | `next_run_at` computado em UTC no re-arm; cron **nunca** carrega preferência de horário |
> 326	| FM-CAD-07 | **Backlog storm**: queda de N horas ⇒ tick dispara todos os planos atrasados de uma vez ⇒ flood + ban | 8 | 4 | 6 | **192** | `catchup_window` + `jitter_seconds` + fan-out bounded (MAX_PER_RUN/CONCURRENCY) |
> 327	| FM-CAD-08 | **Retry do carrossel duplica children** (OTD-CAD-005) amplificado pela recorrência | 7 | 5 | 5 | **175** | Carrossel fora da cadência até fechar; GROUP MARKER + 409 |
> 328	| FM-CAD-09 | **HMAC global em BYOK**: cada tenant tem app secret próprio; validar contra segredo global rejeita (ou pior, aceita) errado | 9 | 5 | 4 | **180** | Resolver tenant pelo `phone_number_id`/`waba_id` (:120-132) **antes** de validar; `timingSafeEqual` |
> 329	| FM-CAD-10 | **Custo X invisível**: publish com URL a US$0,200/req sangra o tenant sem entrar no ledger | 6 | 8 | 7 | **336** | OTD-CAD-011: precificar em mco (4×-floor) + probe de créditos |
> 330	| FM-CAD-11 | **Recategorização silenciosa de template** (utility grátis → marketing pago) ⇒ o custo estimado mente | 6 | 6 | 7 | **252** | Assinar `message_template_status_update`; validar categoria **no send**; telemetria + `notify()` |
> 331	| FM-CAD-12 | **Rodapé/disclosure delegado ao LLM**: alucinação omite endereço postal/opt-out/disclosure de IA ⇒ CAN-SPAM por e-mail + AI Act | 9 | 5 | 6 | **270** | Montagem **server-side**, concatenada; nunca no prompt (G10/G12) |
> 332	| FM-CAD-13 | **`entry.messaging` codado às cegas** (doc só mostra `entry.changes`) ⇒ inverte o falso-sucesso, passa a descartar comentários | 7 | 6 | 5 | **210** | Provar o shape com payload cru de DM real **antes** de codar |
> 333	| FM-CAD-14 | **Kill-switch calibrado por limiar inexistente**: a Meta não publica número de "feedback negativo excessivo" | 7 | 5 | 6 | **210** | Limiar conservador auto-imposto (bloqueios+denúncias+opt-outs por 1k), telemetria em `infra_health_logs`, kill = `is_active=false` |
> 334	| FM-CAD-15 | **Enqueue sem consentimento no WhatsApp** (opt-in ausente) | 10 | 4 | 4 | **160** | 422 `whatsapp_opt_in_missing` fail-closed: exige `granted_at` + `source_proof` + categoria |
> 335	| FM-CAD-16 | **`estimateNodeCost` NaN** por kind faltando no switch (compilador não avisa) | 4 | 7 | 8 | **224** | Checklist manual de 6 edições; corrigir `publishSocial` de quebra |
> 336	
> 337	---
> 338	
> 339	## §9 Pattern Conformance Declaration
> 340	
> 341	> SSOT: `docs/architecture/agentic-vision.md` §2 (21 padrões). Declaração, não sign-off.
> 342	
> 343	| # | Pattern | Implemented? | How / Why-deferred |
> 344	|---|---------|:---:|---|
> 345	| 1 | Prompt Chaining | yes | `program jsonb` (steps publish\|wait\|throttle\|digest\|branch) executado sequencialmente por ciclo — molde `sequences.steps` + `current_step` (`nurture-nurturing:11-21`) |
> 346	| 2 | Routing | yes | Roteamento **por estado de janela e política**: in-window → free-form; out-window → template APPROVED ou draft HITL; canal sem caminho legítimo → recusa estruturada (G1/G6) |
> 347	| 3 | Parallelization | yes | Fan-out bounded no driver (`MAX_PER_RUN`/`CONCURRENCY`, molde `autopilot-cadence-cron:15-16`) |
> 348	| 4 | Reflection | deferred | Crítico de copy (promocional vs transacional) é **classificador determinístico server-side**, não Generator-Critic. OTD-CAD-016 (loop de A/B → `hook_rate`) é o embrião |
> 349	| 5 | Tool Use | yes | Edge fns tipadas (`cadence-plan`, `cadence-run`) roteadas pelo **tick existente** `autopilot-cadence-cron` (sem cron novo — §5.2); Graph API / Telegram / Resend como tools per-user BYOK |
> 350	| 6 | Planning | yes | O plano **é** o artefato (`autopilot_plans.program` com `plan_kind='cadence'`), pré-gerado e versionado; re-planejamento dinâmico não se aplica ao escopo |
> 351	| 7 | Multi-Agent | n-a | Cadência é motor determinístico single-agent; a orquestração multi-agente vive no Pantheon/`orchestrate-*`, a montante |
> 352	| 8 | Memory Management | yes | `social_threads`/`social_messages` (a Meta só devolve as **20 últimas** ⇒ a memória de conversa **tem** que morar aqui) + nó de observação na Knowledge Mesh a cada ciclo |
> 353	| 9 | Learning & Adaptation | deferred | A/B determinístico (hash) existe no desenho, mas o loop fechado depende de ingestão confiável de `creative_metrics.hook_rate` — **OTD-CAD-016** |
> 354	| 10 | Model Context Protocol | n-a | Nó não expõe superfície MCP (o Vision MCP é o servidor MCP do ecossistema) |
> 355	| 11 | Goal Setting & Monitoring | yes | `channel_profiles.cadence` (`target_per`/`count_min`/`count_max`) vira o **goal declarativo** por canal; `cadence_dispatches` + `infra_health_logs` monitoram |
> 356	| 12 | Exception Handling & Recovery | yes | Idempotência por índice único (falha libera / sucesso prende), `overlap_policy`, `catchup_window`, retry com backoff (molde `auto-publish:200-212`), kill-switch `is_active` |
> 357	| 13 | Human-in-the-Loop | yes | Nasce **`delivery:'gated'`** (molde `nurture-dispatch:150`) + `publishMode:'draft'`; a Human Agent tag é **inalcançável** do caminho automático (G5); flip para `'sent'` = GO Sovereign |
> 358	| 14 | Knowledge Retrieval (RAG) | n-a | Cadência não recupera conhecimento; consome asset/pilar já produzido a montante |
> 359	| 15 | Inter-Agent Comm. (A2A) | n-a | Sem interação agente-agente; a comunicação é sistema↔plataforma externa |
> 360	| 16 | Resource-Aware Optimization | yes | Caps `daily`/`budget` NOT NULL; frequency cap com HALT; mcoCoins 4×-floor no que custa USD (X DM = 4 mco); begin/finalize atômico se houver geração |
> 361	| 17 | Reasoning Techniques | deferred | `optimize-schedule` (LLM per-user) como **oráculo opcional** de horário; default é janela determinística por canal (LLM dentro de cron = custo + flakiness). OTD-CAD-008 |
> 362	| 18 | Guardrails / Safety | yes | 14 guardrails de §6, **estruturais** (FK NOT NULL, UNIQUE(comment_id), fail-closed 402/422, separação de caminho da human_agent tag, IoC anti-browser-automation) |
> 363	| 19 | Evaluation & Monitoring | yes | `cadence_dispatches` (ledger com transição de `status` service-role — §5.2, não append-only puro) + reconciliação por webhook de status (nunca pelo 202) + telemetria `infra_health_logs` + `notify()` |
> 364	| 20 | Prioritization | deferred | Sem álgebra de priorização entre planos concorrentes do mesmo tenant (risco de starvation quando o cap é atingido) — herda o gap de OTD-AG do ledger |
> 365	| 21 | Exploration & Discovery | deferred | A/B determinístico é exploração **rasa** (bucket fixo); torneio/Elo entre variantes fica para o loop de `creative_metrics` — OTD-CAD-016 |
> 366	
> 367	---
> 368	
> 369	## §10 Mitos refutados pela verificação adversarial
> 370	
> 371	1. **"Os escopos de DM do IG já estão CONCEDIDOS — o comment→DM é code-only para todos."** ❌ O repo prova que o OAuth **pede** (`social-auth-init:87`) — **pedir ≠ ter Advanced Access**. Para o Usuário Zero (dono do app, Standard Access) é code-only; **para qualquer tenant terceiro é gated por App Review + Business Verification** (https://developers.facebook.com/docs/instagram-platform/overview/). Guardrail: `ig_advanced_access_required` fail-closed — nunca tentar e queimar reputação do app.
> 372	2. **"O DM do IG chega em `entry.messaging`."** ⚠️ **NÃO CONFIRMADO na fonte primária** — a página de webhooks só publica exemplo com `entry[].changes` (https://developers.facebook.com/docs/instagram-platform/webhooks). O handshake + HMAC + a lista de 15 `subscribed_fields` **estão** confirmados. **Provar o shape com um DM real antes de codar** (FM-CAD-13).
> 373	3. **"Comentar abre a janela de 24h."** ❌ Comentário abre **outra coisa**: a janela de **private reply (7 dias, 1 mensagem)**. A lista oficial de gatilhos da janela de 24h não inclui comentário. **São dois relógios distintos** (https://developers.facebook.com/documentation/business-messaging/messenger-platform/policy).
> 374	4. **"A Meta obriga a monitorar a taxa de bloqueio."** ❌ A §5 diz que a experiência "não deve receber uma **quantidade excessiva de feedback negativo**" — **sem métrica nomeada e sem limiar público**. Logo o kill-switch **não pode** depender de um limiar oficial inexistente: tem que ser conservador e auto-imposto (FM-CAD-14).
> 375	5. **"Depreciação de message tags em 27/04/2026 (CONFIRMED_EVENT_UPDATE etc.)."** ⚠️ **Não verificável** — o changelog da Meta devolveu HTTP 500/400 em todas as tentativas. Não citar como fato em SDD. O desenho não depende dessas tags.
> 376	6. **"Erro 613 = rate limit do Send API" / "Send API = 300 calls/s".** ⚠️ O código 613 **não** aparece na fonte atribuída; e **duas docs oficiais divergem** (100 vs 300 calls/s). Resolver empiricamente (OTD-CAD-012).
> 377	7. **"Marketing Messages API (MM Lite) está GA e entrega ~9% mais."** ❌ A doc primária **não** diz "generally available" e **não** traz o número 9%; as otimizações de criativo aparecem como **"(in testing)"** (https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview). Marketing, não doc.
> 378	8. **"WhatsApp tem 1.000 conversas grátis/mês."** ❌ Não existe franquia. O "grátis" é **estrutural** (não-template dentro da janela, utility na janela, service, FEP 72h) — https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing. E o valor do produto passa a ser **abrir e manter janelas**, não disparar volume.
> 379	9. **"Responder com IA dentro da janela é grátis (no Brasil)."** ⚠️ **Talvez não.** A política de **AI Providers** cobra cada mensagem **não-template** entregue no **Brasil** (EU/EEA cessou em 13/mai/2026) — OTD-CAD-009. **Bloqueante econômico do auto-reply.**
> 380	10. **"Endpoints de comentário orgânico do TikTok existem."** ❌ **Não confirmado** — portal e Postman são SPA; o único par provado (`/open_api/v1.3/comment/*`) é no contexto de **ads**. Zero FR até probe autenticado.
> 381	11. **"TikTok Business Messaging é proibida para orgs dos EUA."** ❌ A fonte (BSP) diz que é indisponível **naquele BSP**, em Open Beta. Confirmado sem ressalva: **EEE/Suíça/UK não podem**; **grátis**; LatAm (Brasil) dentro; e há restrições extras de **mídia** em 14 países ⇒ capability-flag por **tenant/região**, não toggle global.
> 382	12. **"Sponsored Messaging do LinkedIn reabriu na UE em out/2024."** ❌ Data não confirmada. O que vale: mensagem no LinkedIn = **orçamento de anúncio**, fora do nó de cadência.
> 383	13. **"Discord exige verificação acima de 100 servidores (Developer Policy)."** ❌ O número não está no Developer Policy. O veredito de produto (**Discord = NÃO-CANAL para cadência comercial**) permanece intacto.
> 384	14. **"CAN-SPAM = US$53.088 por e-mail."** ⚠️ Número de 2025, reajustado **anualmente**; ftc.gov bloqueou o fetch. Usar "dezenas de milhares de dólares **por e-mail**, reajustado anualmente". A decisão de engenharia (rodapé server-side) não depende do dígito.
> 385	15. **"O bot do Telegram não pode iniciar conversa (fonte: /bots/faq)."** ⚠️ O **fato é verdadeiro**, a **âncora está errada**: a regra está em `core.telegram.org/bots` (introdução), não no FAQ. Citar a URL certa.
> 386	
> 387	---
> 388	
> 389	## §11 Próximo passo — o que o Sovereign precisa decidir/prover
> 390	
> 391	**Decisões (bloqueiam o BoK 01→05):**
> 392	1. **Sujeito da cadência** (OTD-CAD-002): asset existente (0 mco, Fatia 1 rápida) ou geração por ciclo (custo + begin/finalize)? *Recomendação: asset existente.*
> 393	2. **Estender `autopilot_plans`** (`plan_kind` + `recurrence jsonb`, reusando o tick existente) vs. tabela nova `cadence_plans` + 3º driver (OTD-CAD-003). *Recomendação: **estender** — já há 2 motores idênticos em prod; um 3º triplica o custo de manutenção.*
> 394	3. **`channel_profiles.cadence` é teto autoritativo** ou sugestão (OTD-CAD-008)? *Recomendação: autoritativo (ressuscita o dado morto).*
> 395	4. **Escopo de canal da Fatia 1**: só publicação (recomendado) ou já incluir mensagem privada?
> 396	5. **Jurisdição default** quando o lead não tem país (fail-closed = UE, opt-in prévio — custa conversão).
> 397	6. **Semântica do `cadence_dispatches`** (§5.2): índice único parcial `WHERE status <> 'failed'` + `UPDATE` service-role (retry, at-least-once) **ou** append-only puro (at-most-once, sem retry)? *Recomendação: retry via índice parcial.*
> 398	7. **IG/Messenger no app Meta global** (OTD-CAD-018): manter (com cap/kill-switch/telemetria por-app) ou BYOK-de-app espelhando WhatsApp? *Recomendação: manter no global até o Usuário 1; caps por-app obrigatórios.*
> 399	
> 400	> **Resolvido, não mais pergunta:** a migração de `auto-publish` para pg_cron + `FOR UPDATE SKIP LOCKED` (OTD-CAD-004) passou a ser **Fatia 0 item 5** — pré-requisito declarado pelo próprio gate, não decisão em aberto.
> 401	
> 402	**Provisões (ações Sovereign, ninguém mais pode):**
> 403	- Probe no **X Developer Console**: saldo de créditos + confirmar `Post: Create (with URL) = US$0,200` (OTD-CAD-011 — pode estar sangrando **agora**).
> 404	- Probe **autenticado** no portal business-api do TikTok (OTD-CAD-013).
> 405	- Consulta Meta / rate cards sobre **enquadramento AI Provider no Brasil** (OTD-CAD-009).
> 406	- **DM real de terceiro sem role no app** para provar que o webhook entrega sob Standard Access (FM-CAD-02) — e o **payload cru** do DM para fixar o shape (FM-CAD-13).
> 407	- Domínio verificado (SPF/DKIM/DMARC) para o Resend + GO para flipar `nurture-dispatch` de `gated` → `sent`.
> 408	- Decisão de escopo do **AI Act Art. 50(2)** (vigência **2026-08-02**) — módulo próprio (OTD-CAD-014).
> 409	
> 410	**Gates que permanecem fechados:** `/bok-scribe spaces-cadence` (01-mrd → 05-sdd + `09-pattern-conformance.md`) · SOP Lei 2 em `docs/processes/spaces-cadence.md` · `/security-review` de toda migration. **Nenhuma linha de código antes disso.**
> 411	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SDD — System Design Document
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14) + [`01-mrd.md`](01-mrd.md) + [`02-brd.md`](02-brd.md) + [`03-prd.md`](03-prd.md) + [`04-frd.md`](04-frd.md). Cada objeto de design abaixo implementa um `FR-CAD-xxx` da FRD §2; nada é inventado além do blueprint (Lei 1). Onde o blueprint deixou uma decisão em aberto (§11), a §8 desta SDD **sela** a decisão (default do OTD) — nunca improvisa.
> 8	
> 9	> **ORO triplet desta task:**
> 10	> - **Operator:** MCORCH Master Execution Agent
> 11	> - **Reviewer:** Sovereign (Gabriel)
> 12	> - **Owner:** Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 13	>
> 14	> **Closed-Loop gate:** este é o **5º e último** documento da suíte BoK (01-mrd → 05-sdd). A **Pattern Conformance Declaration** dos 21 padrões agênticos está em **§9** desta SDD (gate Step 3.5, SSOT `docs/architecture/agentic-vision.md`) — este módulo toca ≥3 padrões materialmente, então a declaração também será promovida a `09-pattern-conformance.md` copiando §9. Permanecem ABERTOS após esta SDD: SOP Lei 2 (`docs/processes/spaces-cadence.md`) + `/security-review` de toda migration. **Nenhuma linha de código antes disso.**
> 15	>
> 16	> **Nota de fidelidade (Lei 1):** FR-CAD-012/013 (inbox IG) permanecem `[PROBE-GATED]` — este design os especifica como blueprint **congelado**, ativável só após o probe FM-CAD-02 (RPN 486) fechar com DM real de terceiro sem role + payload cru arquivado. §3 do blueprint (posicionamento vs. ManyChat) permanece sob **SELO DE NÃO-VERIFICAÇÃO**: nenhuma decisão de design abaixo cita §3 como fato.
> 17	
> 18	---
> 19	
> 20	## 1. Architecture Overview
> 21	
> 22	**Princípio arquitetural (mandato de integração):** a Cadência **encaixa nos trilhos vivos** — autopilot (`autopilot_plans` + `autopilot-cadence-cron`), sequences/`nurture-dispatch`, `scheduled_posts` — e **não reconstrói distribuição**. Zero tabela de plano paralela; **zero job pg_cron novo**; o `scheduled_posts` é o **sink one-shot** que o `auto-publish` já drena. O motor é **Postgres-first**: pg_cron + `next_run_at` + índice parcial due — o padrão que o MCORCH já roda **duas vezes** em produção e que este módulo **estende** (OTD-CAD-003).
> 23	
> 24	```
> 25	┌──────────────────────────────────────────────────────────────────────┐
> 26	│  PRESENTATION LAYER (display-only — Harness Engineering)              │
> 27	│  src/components/canvas/nodes/CadenceNode.tsx        (só <Handle> in)   │
> 28	│  src/components/canvas/RightPanel/inspectors/CadenceInspector.tsx      │
> 29	│  src/lib/canvas-node-registry.ts  (1 entrada, category "Publish")      │
> 30	└──────────────────────┬───────────────────────────────────────────────┘
> 31	                       │ arma / faz poll (molde useVoiceRenderPoll)
> 32	┌──────────────────────▼───────────────────────────────────────────────┐
> 33	│  LOGIC LAYER (custom hooks)                                            │
> 34	│  src/hooks/useCanvasStudio.ts  (→ cadence-plan invoke)                 │
> 35	│  src/hooks/useCadenceRunPoll.ts (últimas N dispatches + next_run_at)   │
> 36	│  src/types/canvas.ts  (CadenceData + estimateNodeCost projeção)        │
> 37	└──────────────────────┬───────────────────────────────────────────────┘
> 38	        │ JWT (verify_jwt=false → ES256 JWKS verify, nunca atob cego)
> 39	┌───────▼───────────────────────────────────────────────────────────────┐
> 40	│  EDGE LAYER (Deno / Supabase Functions)                                │
> 41	│  cadence-plan   (arm: upsert autopilot_plans + next_run_at UTC)        │
> 42	│  cadence-run    (drain FOR UPDATE SKIP LOCKED → gate chain → dispatch) │
> 43	│  whatsapp-webhook (Fatia 0: alcançável + timingSafeEqual)             │
> 44	│  instagram-webhook (Fatia 2 PROBE-GATED: entry.messaging + comments)  │
> 45	└───────┬──────────────────────────────┬────────────────────────────────┘
> 46	        │ Supabase RLS                  │ External APIs (BYOK per-user)
> 47	┌───────▼──────────────────────┐  ┌────▼───────────────────────────────┐
> 48	│  DB LAYER                    │  │  EXTERNAL SERVICES (per-tenant)      │
> 49	│  autopilot_plans (ESTENDIDA) │  │  Graph API / graph.instagram.com     │
> 50	│  cadence_dispatches (NOVA)   │  │  Telegram Bot API (BYOK, US$0)        │
> 51	│  scheduled_posts (SINK)      │  │  Resend (BYOK, domínio verificado)    │
> 52	│  social_threads/_messages    │  │  X API (fora da allowlist Fatia 1)    │
> 53	│  lead_events/leads/consents  │  │  provider-keys pool (resolveProvKey)  │
> 54	│  channel_profiles.cadence    │  └───────────────────────────────────────┘
> 55	│  profiles.timezone (SSOT)    │
> 56	│  mcorch_nodes (observação)   │
> 57	└──────────────────────────────┘
> 58	        ▲
> 59	        │ pg_cron */15 (GMT) → autopilot-cadence-cron (gate Bearer SB_SECRET_KEY)
> 60	        └── roteia por plan_kind: viral→autopilot-run | cadence→cadence-run
> 61	```
> 62	
> 63	**Trilho de execução (por que uma edge fn própria, NÃO `canvas-execute`):** enfiar um `node_type` novo no `canvas-execute` custa 4 listas hardcoded + o enum `vm_node_type`. Cadência **não gera mídia** ⇒ não passa por ali (blueprint §2.2). O nó `cadence` arma um plano via `cadence-plan`; o tick vivo executa via `cadence-run`.
> 64	
> 65	---
> 66	
> 67	## 2. Component Catalog
> 68	
> 69	### 2.1 New / Extended Custom Hooks (`src/hooks/`)
> 70	
> 71	| Hook | File | Responsibility | FR | TanStack Query keys |
> 72	|------|------|---------------|----|---------------------|
> 73	| `useCanvasStudio` (ext.) | `src/hooks/useCanvasStudio.ts` | Invoca `cadence-plan` no arm; `cadence` **fora** de `needsLedgerRun()` (não gera ⇒ sem `node_run_id`) | FR-CAD-005 | — |
> 74	| `useCadenceRunPoll` | `src/hooks/useCadenceRunPoll.ts` | Poll de `next_run_at` + últimas N `cadence_dispatches` do plano; **molde `useVoiceRenderPoll`** (id no `data` do nó, sobrevive a refresh — nunca `sleep(8s)×25`) | FR-CAD-005 | `['cadence-dispatches', planId]` |
> 75	| `useCanvasPipeline` (ext.) | `src/hooks/useCanvasPipeline.ts` | `cadence` entra na **lista de exclusão** do gate "runnable" (:33-50) — não exige `prompt` | FR-CAD-001 | — |
> 76	
> 77	### 2.2 New / Extended Display Components (`src/components/`)
> 78	
> 79	| Component | File | Props | Hook consumed | FR |
> 80	|-----------|------|-------|--------------|----|
> 81	| `CadenceNode` | `src/components/canvas/nodes/CadenceNode.tsx` | `{ id, data: CadenceData }` | — (display-only) | FR-CAD-001 |
> 82	| `CadenceInspector` | `src/components/canvas/RightPanel/inspectors/CadenceInspector.tsx` | `{ node }` | `useCanvasStudio`, `useCadenceRunPoll` | FR-CAD-001, FR-CAD-005, FR-CAD-011 |
> 83	| `RightPanel` (ext.) | `src/components/canvas/RightPanel/index.tsx` | — | — | FR-CAD-001 |
> 84	| `canvas-node-registry` (ext.) | `src/lib/canvas-node-registry.ts` | — | — | FR-CAD-001 |
> 85	
> 86	> **Checklist das 6 edições manuais (não há registry único — blueprint §2.2; FM-CAD-16):**
> 87	> 1. `src/types/canvas.ts` — `CanvasNodeKind` (+`cadence`) + `CadenceData` + union `CanvasNodeData` + `makeDefaultCadence` + `case "cadence": return null` em `resolveExecutePayload` + `case "cadence": return 0` em `estimateNodeCost`.
> 88	> 2. `src/lib/canvas-node-registry.ts` — 1 entrada `category:"Publish"`, aliases pt-BR: **cadência/agendar/recorrente/cron/calendário**.
> 89	> 3. `src/components/canvas/nodes/CadenceNode.tsx` — molde `PublishSocialNode`, único `<Handle>` target `input_asset` (id inline).
> 90	> 4. `src/pages/CanvasEditorPage.tsx:63-77` — `nodeTypes`.
> 91	> 5. `src/components/canvas/RightPanel/index.tsx:23-110` — 1 ramo na ternária.
> 92	> 6. `src/components/canvas/RightPanel/inspectors/CadenceInspector.tsx`.
> 93	> **Pré-requisito Fatia 0:** `estimateNodeCost` ganha `case 'publishSocial'` **antes** de somar `cadence` (senão `runAllCost` → NaN; FR-CAD-016 / OTD-CAD-007).
> 94	
> 95	### 2.3 New Edge Functions (`supabase/functions/`)
> 96	
> 97	| Function | Path | Auth | mcoCoins | Secrets / BYOK | FR |
> 98	|----------|------|------|----------|----------------|----|
> 99	| `cadence-plan` | `supabase/functions/cadence-plan/index.ts` | JWT (user) — **verify_jwt=false → ES256 JWKS** | **0** (criar plano não gera) | — (só escreve `autopilot_plans`) | FR-CAD-005 |
> 100	| `cadence-run` | `supabase/functions/cadence-run/index.ts` | `Bearer SB_SECRET_KEY` → 403 (cron-only); `user_id` **server-trusted da linha** | 0 no dispatch a `scheduled_posts`; se houver passo `generate` → `begin`/`finalize` | provider-keys pool per-user; Telegram/Resend BYOK (Fatia 3) | FR-CAD-006, FR-CAD-007/008/009/010, FR-CAD-014 |
> 101	| `whatsapp-webhook` (fix) | `supabase/functions/whatsapp-webhook/index.ts` | `verify_jwt=false` (Fatia 0 item 1) + HMAC `timingSafeEqual` | — | app secret per-tenant (BYOK) resolvido por `phone_number_id`/`waba_id` antes de validar | FR-CAD-015 |
> 102	| `instagram-webhook` (ext.) `[PROBE-GATED]` | `supabase/functions/instagram-webhook/index.ts` | `verify_jwt=false` + HMAC `timingSafeEqual` (já existe) | — | app secret **global** (OTD-CAD-018) | FR-CAD-012/013 |
> 103	
> 104	> **Sem edge fn nova de driver.** O tick `autopilot-cadence-cron` (já vivo) **roteia** por `plan_kind` (FR-CAD-004). Extensão in-place, não função nova.
> 105	
> 106	### 2.4 Zustand Store Slices
> 107	
> 108	| Slice | Store file | Mudança |
> 109	|-------|------------|---------|
> 110	| Canvas graph | `src/store/useCanvasStore.ts` | Nenhuma coluna nova de DB — `CadenceData` mora no `graph jsonb` de `vm_canvas_projects` (molde Canvas Studio; sem migration de store). |
> 111	
> 112	### 2.5 New / Extended DB Objects
> 113	
> 114	| Object | Type | Purpose | Migration file (proposto) | FR |
> 115	|--------|------|---------|---------------------------|----|
> 116	| `autopilot_plans` (+9 col, −1 CHECK) | Table (ALTER) | Absorver cadência: `plan_kind`, `recurrence`, `quiet_hours`, `overlap_policy`, `catchup_window`, `jitter_seconds`, `program`, `channel_allowlist`, `budget_cap_mco`; DROP `platforms_check` | `20260716120000_cadence_extend_autopilot_plans.sql` | FR-CAD-002 |
> 117	| `cadence_dispatches` | Table (NEW) | Ledger por tentativa + idempotência por índice único **parcial** | `20260716120100_cadence_dispatches.sql` | FR-CAD-003 |
> 118	| `erase_lead()` (ext.) | Function | Cancelar `scheduled_posts` + `cadence_dispatches` pendentes em cascata (mesma transação) | `20260716120200_erase_lead_cascade_cadence.sql` | FR-CAD-017 |
> 119	| `auto-publish` cron | pg_cron job | Migrar de crontab de SO → pg_cron + `FOR UPDATE SKIP LOCKED` | `20260716120300_auto_publish_pgcron_skiplocked.sql` | FR-CAD-018 |
> 120	| `social_threads` / `social_messages` `[PROBE-GATED]` | Tables (NEW) | Histórico de conversa (a Meta só devolve as **20 últimas**) + relógios `csw_expires_at`(24h)/`private_reply_deadline`(7d) | `2026xxxx_social_threads.sql` (Fatia 2) | FR-CAD-012 |
> 121	| `channel_profiles.cadence` | Column (reuso) | Ganha **primeiro leitor** (teto autoritativo por canal) | — (dado já existe) | FR-CAD-008 |
> 122	| `profiles.timezone` | Column (reuso) | Ganha **primeiro leitor** (SSOT de fuso) | — (dado já existe) | FR-CAD-007 |
> 123	
> 124	---
> 125	
> 126	## 3. Data Flow Diagrams
> 127	
> 128	### 3.1 Use Case A — Armar plano de cadência (FR-CAD-005)
> 129	
> 130	```
> 131	User            CadenceInspector      cadence-plan (ES256)     autopilot_plans
> 132	 │  configura         │                     │                      │
> 133	 │──[Armar]──────────▶│                     │                      │
> 134	 │                    │──[POST JWT]────────▶│                      │
> 135	 │                    │                     │─[ES256 JWKS verify]─ │  (nunca atob cego)
> 136	 │                    │                     │─[compute next_run_at UTC from recurrence]
> 137	 │                    │                     │──[upsert plan_kind='cadence']──▶│
> 138	 │                    │                     │◀──[plan_id UUID]────────────────│
> 139	 │                    │◀──[200 {plan_id, next_run_at, projected_cost_mco}]    │
> 140	 │◀──[poll molde useVoiceRenderPoll: next_run_at + últimas N dispatches]      │
> 141	    (0 mco debitado — profiles.mco_balance inalterado — FR-CAD-005 material)
> 142	```
> 143	
> 144	### 3.2 Use Case B — Ciclo de cadência (FR-CAD-006, o coração)
> 145	
> 146	```
> 147	pg_cron */15 (GMT)          autopilot-cadence-cron        cadence-run              scheduled_posts / cadence_dispatches
> 148	 │──[tick]──────────────────▶│  (gate Bearer SB_SECRET_KEY→403)
> 149	 │                           │──[scan due, route by plan_kind]
> 150	 │                           │   viral → autopilot-run (como hoje)
> 151	 │                           │   cadence ─────────────▶│  (user_id server-trusted da LINHA)
> 152	 │                           │                         │─[drain FOR UPDATE SKIP LOCKED]
> 153	 │                           │                         │─[resolve subject owner-scoped (creative_assets.id)]
> 154	 │                           │                         │─[GATE CHAIN server-side — nunca LLM]:
> 155	 │                           │                         │    quiet_hours(fuso do sujeito) → HALT
> 156	 │                           │                         │    frequency_cap(channel_profiles.cadence) → HALT
> 157	 │                           │                         │    opt-out(withdrawn_at) no send
> 158	 │                           │                         │    jurisdição(país? senão UE opt-in) fail-closed
> 159	 │                           │                         │    dedup/digest (user,channel,dia) → 1
> 160	 │                           │                         │    A/B: mod(abs(hashtext(subj||':'||exp)::bigint),100)<ratio
> 161	 │                           │                         │─[dispatch]──▶ INSERT scheduled_posts
> 162	 │                           │                         │              (metadata.reshape + schedule:true + publish_at ISO)
> 163	 │                           │                         │─[ledger]──▶ INSERT cadence_dispatches
> 164	 │                           │                         │              ON CONFLICT DO NOTHING RETURNING
> 165	 │                           │                         │              (índice parcial WHERE status<>'failed')
> 166	 │                           │                         │─[re-arm next_run_at UTC | deactivate]
> 167	                                                       ▼
> 168	                        auto-publish (pg_cron + SKIP LOCKED) DRENA → publica
> 169	                                                       ▼
> 170	                        reconcile webhook de STATUS → status='sent' + external_usd_cost + cost_source
> 171	                        (NUNCA a partir do 202 — FM-CAD-05, Lei 1) → collective_efficiency_ledger
> 172	```
> 173	
> 174	### 3.3 Use Case C — Laço inbound IG `[PROBE-GATED]` (FR-CAD-012/013)
> 175	
> 176	```
> 177	scheduled_posts → auto-publish publica IG
> 178	                          ▼
> 179	   instagram-webhook (HMAC timingSafeEqual + hub.challenge — esqueleto reusado)
> 180	      entry.changes: comments   |   entry.messaging: DM  ⚠️ shape provado por payload cru real
> 181	                          ▼
> 182	   lead_events(event_type='message_received') + leads + notify() → social_threads/_messages
> 183	                          ▼
> 184	   gate chain → private reply 1× (≤7d, UNIQUE comment_id)  OU  resposta in-window (≤24h CSW)
> 185	      · FK NOT NULL p/ inbound ⇒ cold DM impossível de representar (G1)
> 186	      · Human Agent tag inalcançável do caminho service-role (G5)
> 187	      · classificador in/out-window server-side (G6) · nasce delivery:'gated'
> 188	                          ▼
> 189	   link afiliado + UTM → creative_metrics → collective_efficiency_ledger
> 190	```
> 191	
> 192	---
> 193	
> 194	## 4. API Contract Definitions
> 195	
> 196	> Toda Edge Function valida a identidade **antes** de qualquer lógica. `verify_jwt=false` no `config.toml` ⇒ verificação **ES256 via JWKS** dentro da função (SOP `docs/processes/edge-jwt-identity-verification.md`); **nunca `atob` cego**. Cron-only funcs exigem `Authorization === Bearer SB_SECRET_KEY`.
> 197	
> 198	### `POST /functions/v1/cadence-plan` (FR-CAD-005)
> 199	
> 200	```typescript
> 201	// Request — Auth: Bearer JWT (user); user_id server-trusted da claim verificada
> 202	interface CadencePlanRequest {
> 203	  sourceAssetId: string            // creative_assets.id (owner-scoped) — Fatia 1 = asset existente (0 mco, OTD-CAD-002)
> 204	  recurrence: {                    // computado em UTC no servidor (FM-CAD-06)
> 205	    frequency: 'daily' | 'weekly' | 'monthly'
> 206	    days: number[]                 // weekdays (1=Mon) ou dias do mês
> 207	    hours: number
> 208	    minutes: number                // múltiplo de 5 (semântica Knock)
> 209	    tz: string                     // IANA; cascata → profiles.timezone → 'America/Sao_Paulo'
> 210	  }
> 211	  quiet_hours?: { start: string; end: string; days: number[] }
> 212	  channel_allowlist: string[]      // ⊆ allowlist do auto-publish MENOS X (Fatia 1) — por PLANO, não constante
> 213	  budget_cap_mco: number           // NOT NULL, em mcoCoins (nunca USD)
> 214	  overlap_policy?: 'skip'          // default 'skip'
> 215	  catchup_window?: string          // interval, default '6 hours'
> 216	  jitter_seconds?: number
> 217	  program?: CadenceStep[]          // molde sequences.steps + current_step
> 218	}
> 219	
> 220	// Response (HTTP 200)
> 221	interface CadencePlanResponse {
> 222	  plan_id: string                  // autopilot_plans.id (plan_kind='cadence')
> 223	  next_run_at: string              // ISO UTC
> 224	  projected_cost_mco: number       // Σ(canal × ocorrências até cap) — obrigação compensatória do quote=0
> 225	}
> 226	
> 227	// mcoCoins: 0 na criação do plano. G7 (quote==charge) é invariante do CICLO
> 228	// (begin/finalize), NÃO do nó. Nenhum deduct_mco_coins aqui.
> 229	```
> 230	
> 231	**Error codes:**
> 232	
> 233	| Code | Condition | Body |
> 234	|------|-----------|------|
> 235	| 401 | JWT ausente/inválido (falha ES256 JWKS) | `Unauthorized` |
> 236	| 402 | `<provider>_not_configured` (BYOK fail-closed, Fatia 3) | `{ error, action }` |
> 237	| 403 | Chamada cron sem `Bearer SB_SECRET_KEY` | `Forbidden` |
> 238	| 422 | Validação (`budget_cap_mco` ausente/≤0; `recurrence` inválida; `minutes % 5 ≠ 0`; canal fora da allowlist) | `{ error, field, message /* pt-BR */ }` |
> 239	| 500 | Erro interno | logado em `infra_health_logs` (`service='spaces-cadence'`) |
> 240	
> 241	### `POST /functions/v1/cadence-run` (FR-CAD-006 — invocada pelo tick, não pela UI)
> 242	
> 243	**Auth:** `Authorization === Bearer SB_SECRET_KEY` (senão **403**). `user_id` **server-trusted da linha** de `autopilot_plans` (nunca do body — SOP `autopilot-cron-identity.md`).
> 244	**Behavior:** `drain FOR UPDATE SKIP LOCKED` → `resolve subject owner-scoped` → `gate chain` (§5.5) → `dispatch scheduled_posts` → `INSERT cadence_dispatches ON CONFLICT DO NOTHING RETURNING` → `re-arm next_run_at UTC | deactivate`. `overlap_policy=skip` (ciclo anterior rodando ⇒ pula). **Reconciliação:** `status='sent'` **só** do webhook de status, nunca do 202 (FM-CAD-05).
> 245	
> 246	### `POST /functions/v1/whatsapp-webhook` (FR-CAD-015, Fatia 0)
> 247	
> 248	`verify_jwt=false` (bloco em `config.toml` — hoje **ausente** ⇒ 401 no gateway). HMAC via `timingSafeEqual` (`_shared/oauth-state.ts`), nunca `===`. Sink = `leads`/`lead_events` (não `whatsapp_leads`, absorvida por OTD-MH-001). BYOK (Fatia 4): resolver tenant por `phone_number_id`/`waba_id` **antes** de buscar o app secret e validar (FM-CAD-09).
> 249	
> 250	---
> 251	
> 252	## 5. Security Design
> 253	
> 254	### 5.1 Threat Model (STRIDE)
> 255	
> 256	| Component | Threat | Type | Severity | Mitigation |
> 257	|-----------|--------|------|----------|------------|
> 258	| `cadence-plan` | Acesso não-autenticado / JWT forjado | Spoofing | High | `verify_jwt=false → ES256 JWKS verify` (nunca `atob`); `user_id` da claim, nunca do body (NFR-CAD-004) |
> 259	| `cadence-run` | Invocação por não-cron; `user_id` falsificado no body | Spoofing / Elevation | Critical | Gate `Bearer SB_SECRET_KEY`→403; `user_id` **server-trusted da linha** (SOP autopilot-cron-identity) |
> 260	| `cadence_dispatches` | Escrita pelo cliente (forjar `status='sent'`, custo) | Tampering | Critical | RLS: `select_own` + `insert`/`update` **service-role only**; cliente **nunca** escreve (NFR-CAD-006) |
> 261	| `autopilot_plans` | Leitura/escrita cross-tenant | Information Disclosure | Critical | RLS owner-scoped **preservada** (`user_id = auth.uid()`) |
> 262	| mcoCoins (ciclo) | Débito client-side / duplo | Tampering | Critical | Cobrança **só** via RPC atômica `begin`/`finalize` (advisory-lock + `ON CONFLICT DO NOTHING`); nunca client-side (NFR-CAD-007) |
> 263	| Double-post | Tick sobreposto/retry publica 2× | Tampering (integridade) | High | Índice único **parcial** `WHERE status<>'failed'` + `ON CONFLICT DO NOTHING RETURNING` + `overlap_policy=skip` (FM-CAD-01) |
> 264	| Reconcile (202) | Falso-sucesso "enviado" sem prova | Repudiation | High | `sent` só do webhook de status; nunca do 202 (FM-CAD-05, Lei 1) |
> 265	| Provider key (BYOK) | Uso de env global em fluxo user-facing | Information Disclosure | High | `resolveProviderKey(admin,userId,provider,keyId)`; **0** `Deno.env.get(<provider>)` user-facing; env = só infra (NFR-CAD-005) |
> 266	| `whatsapp-webhook` HMAC | Timing attack / segredo global em BYOK | Spoofing | High | `timingSafeEqual`; resolver tenant por `phone_number_id`/`waba_id` antes de validar (FM-CAD-09) |
> 267	| `instagram-webhook` `[PROBE-GATED]` | Cold DM / janela expirada enfileirada | Tampering (política) | Critical | FK NOT NULL p/ inbound (G1); gate de janela **no send**; 2 relógios distintos (FM-CAD-03) |
> 268	| Browser automation | Automação de DM/engajamento via headless | Tampering / política de plataforma | High | Proibição perene; smoke IoC **falha** se script fora de `scripts/qa/` tocar `instagram.com`/`facebook.com` via browser (G13) |
> 269	| Opt-out / eliminação | Revogação após enqueue; agendamento sobrevive ao erase | Repudiation / Compliance | Critical | `withdrawn_at` checado **no send** (independe da base legal); `erase_lead()` cascata na mesma transação (G9/FM-CAD-04) |
> 270	
> 271	### 5.2 RLS Policy Definitions
> 272	
> 273	```sql
> 274	-- cadence_dispatches: cliente LÊ o próprio, mas NUNCA escreve (semântica de status transiciona → service-role)
> 275	ALTER TABLE cadence_dispatches ENABLE ROW LEVEL SECURITY;   -- default-deny
> 276	
> 277	CREATE POLICY "cadence_dispatches_select_own"
> 278	  ON cadence_dispatches FOR SELECT
> 279	  USING (user_id = auth.uid());
> 280	
> 281	-- INSERT/UPDATE apenas service_role (edge fn cron). Sem policy de INSERT/UPDATE para
> 282	-- authenticated ⇒ negado por default-deny. O client jamais forja status='sent' nem custo.
> 283	-- (service_role bypassa RLS — escreve status/error/external_usd_cost no reconcile.)
> 284	
> 285	-- autopilot_plans: RLS owner-scoped PRESERVADA (não recriar; a extensão é só ALTER de colunas).
> 286	```
> 287	
> 288	> **Semântica selada (OTD-CAD-006):** `cadence_dispatches` **não é append-only puro**. O índice parcial `WHERE status<>'failed'` exige transição de status (falha **libera** a chave = retry; sucesso **prende** = anti double-post). Isso obriga `UPDATE` service-role. A alternativa append-only-puro (at-most-once, sem retry) foi **rejeitada** — ver §8 OTD-CAD-006.
> 289	
> 290	```sql
> 291	-- Índice de idempotência (é ELE que impede FM-CAD-01/03, não uma promessa)
> 292	CREATE UNIQUE INDEX cadence_dispatches_idem
> 293	  ON cadence_dispatches (idempotency_key)
> 294	  WHERE status <> 'failed';
> 295	-- idempotency_key = hash estável de (plan_id, step_index, occurrence_at)
> 296	```
> 297	
> 298	### 5.3 JWT / Identity Validation Points
> 299	
> 300	```typescript
> 301	// cadence-plan (user-facing, verify_jwt=false → ES256 JWKS)
> 302	//   NUNCA atob cego. Verificar assinatura ES256 contra o JWKS do Supabase.
> 303	//   (SOP docs/processes/edge-jwt-identity-verification.md; teste scripts/qa/test-es256-jwt-verification.ts)
> 304	const claims = await verifyEs256Jwt(authHeader)     // lança em assinatura inválida
> 305	if (!claims?.sub) return json(401, 'Unauthorized')
> 306	const userId = claims.sub                           // server-trusted da claim, nunca do body
> 307	
> 308	// cadence-run (cron-only)
> 309	if (req.headers.get('Authorization') !== `Bearer ${SB_SECRET_KEY}`)
> 310	  return json(403, 'Forbidden')
> 311	// user_id vem da LINHA de autopilot_plans drenada, nunca do corpo da requisição
> 312	
> 313	// whatsapp-webhook / instagram-webhook (HMAC)
> 314	if (!timingSafeEqual(computedSig, headerSig)) return json(401, 'Unauthorized')
> 315	```
> 316	
> 317	### 5.4 Secrets Inventory
> 318	
> 319	| Secret / Credencial | Used In | Resolução | Rotation |
> 320	|---------------------|---------|-----------|----------|
> 321	| `SB_SECRET_KEY` | `cadence-run`, tick | env (infra — service-role) | Sovereign |
> 322	| provider keys (LLM, se passo `generate`) | `cadence-run` | `user_api_keys` per-user via `resolveProviderKey` (pool BYOK); fail-closed 402 | por tenant |
> 323	| `telegram_bot_token` (Fatia 3) | `cadence-run` | `user_api_keys` coluna cifrada per-user; fail-closed `402 telegram_not_configured` | por tenant |
> 324	| `resend_api_key` (Fatia 3) | `nurture-dispatch` (flip) | per-user cifrada + domínio verificado do tenant | por tenant |
> 325	| WhatsApp app secret (Fatia 4) | `whatsapp-webhook` | per-tenant, resolvido por `phone_number_id`/`waba_id` (BYOK-de-app) | por tenant |
> 326	| IG/Messenger app secret `[PROBE-GATED]` | `instagram-webhook` | **app Meta GLOBAL** (OTD-CAD-018 — fallback restrito consciente; caps por-app + kill-switch global obrigatórios) | Sovereign |
> 327	
> 328	> ⚠️ NUNCA commitar valores. Só nomes de chave aparecem na doc. `Deno.env.get(<provider>)` em fluxo user-facing é **anti-pattern proibido** (API Tenancy Model).
> 329	
> 330	---
> 331	
> 332	## 6. Infrastructure Touchpoints
> 333	
> 334	| Infrastructure | Usage | Impact |
> 335	|----------------|-------|--------|
> 336	| **pg_cron** | Tick vivo `autopilot-cadence-cron` (*/15, GMT) **roteia** por `plan_kind`; `auto-publish` **migra** para pg_cron (Fatia 0 item 5) | **+0 jobs** para a cadência (NFR-CAD-012); Supabase recomenda ≤~8 jobs concorrentes; pg_cron não sobrepõe a mesma job |
> 337	| **`FOR UPDATE SKIP LOCKED`** | Drain de planos vencidos (`cadence-run`) + drain de `scheduled_posts` (`auto-publish`) | Evita contenção multi-consumer; **0** double-publish (FM-CAD-01) |
> 338	| **`infra_health_logs`** | Novo `service='spaces-cadence'` + `event` (`cadence_dispatch`, `cadence_halt_quiet_hours`, `cadence_halt_freq_cap`, `cadence_reconcile`, `template_recategorized`, `kill_switch_tripped`) | Watchdog telemetry (NFR-CAD-015); allowlist no chokepoint (não vazar per-tenant em tabela global-read) |
> 339	| **`mcorch_nodes` (Knowledge Mesh)** | Nó de observação por **ciclo** de cadência (Mesh Connection Mandate) | GraphRAG injection; traceability ← FR-CAD-006 + Pattern P8 |
> 340	| **`collective_efficiency_ledger`** | `external_usd_cost` + `cost_source` gravados no reconcile alimentam mco/resultado do ciclo | Fosso "ledger de custo por ação"; custo BYOK **medido** mesmo com mco=0 (NFR-CAD-008) |
> 341	
> 342	---
> 343	
> 344	## 7. Migration Stubs
> 345	
> 346	> **Toda migration passa por `/security-review` antes do commit (NO EXCEPTIONS — FMEA-011).** Timestamps propostos; a implementação sela os finais.
> 347	
> 348	### 7.1 `20260716120000_cadence_extend_autopilot_plans.sql` (FR-CAD-002 / OTD-CAD-003)
> 349	
> 350	```sql
> 351	-- ESTENDER o trilho vivo — NÃO criar tabela paralela nem 3º driver.
> 352	ALTER TABLE autopilot_plans
> 353	  DROP CONSTRAINT IF EXISTS autopilot_plans_platforms_check,     -- allowlist passa a derivar de channel_profiles
> 354	  ADD COLUMN plan_kind text NOT NULL DEFAULT 'viral'
> 355	      CHECK (plan_kind IN ('viral','cadence')),
> 356	  ADD COLUMN recurrence      jsonb,        -- {frequency, days, hours, minutes, tz}
> 357	  ADD COLUMN quiet_hours     jsonb,        -- {start, end, days}
> 358	  ADD COLUMN overlap_policy  text DEFAULT 'skip',
> 359	  ADD COLUMN catchup_window  interval DEFAULT '6 hours',
> 360	  ADD COLUMN jitter_seconds  int DEFAULT 0,
> 361	  ADD COLUMN program         jsonb,        -- steps; molde sequences.steps + current_step
> 362	  ADD COLUMN channel_allowlist text[],     -- por PLANO (§5.2) — X fora na Fatia 1
> 363	  ADD COLUMN budget_cap_mco  int NOT NULL DEFAULT 0;   -- em mcoCoins; cadence exige > 0 no edge (422)
> 364	-- RLS owner-scoped já existente é PRESERVADA (nenhuma policy recriada).
> 365	-- Planos plan_kind='viral' existentes permanecem válidos (regressão smoke do autopilot).
> 366	```
> 367	
> 368	### 7.2 `20260716120100_cadence_dispatches.sql` (FR-CAD-003 / FM-CAD-01)
> 369	
> 370	```sql
> 371	CREATE TABLE cadence_dispatches (
> 372	  id                uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 373	  user_id           uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 374	  plan_id           uuid NOT NULL REFERENCES autopilot_plans(id) ON DELETE CASCADE,
> 375	  step_index        int  NOT NULL,
> 376	  occurrence_at     timestamptz NOT NULL,
> 377	  idempotency_key   text NOT NULL,          -- hash estável de (plan_id, step_index, occurrence_at)
> 378	  channel           text NOT NULL,
> 379	  status            text NOT NULL DEFAULT 'queued',   -- queued|publishing|sent|failed (transiciona)
> 380	  target_ref        text,                   -- scheduled_posts.id / external id
> 381	  error             text,
> 382	  external_usd_cost numeric,                -- gravado NO RECONCILE (webhook de status), nunca no 202
> 383	  cost_source       text,                   -- fonte do custo externo BYOK (ex.: 'meta_ai_provider_br','x_post_url')
> 384	  created_at        timestamptz DEFAULT now() NOT NULL,
> 385	  updated_at        timestamptz DEFAULT now() NOT NULL
> 386	);
> 387	
> 388	CREATE UNIQUE INDEX cadence_dispatches_idem
> 389	  ON cadence_dispatches (idempotency_key)
> 390	  WHERE status <> 'failed';                 -- falha LIBERA a chave / sucesso PRENDE (Trigger.dev/River)
> 391	
> 392	ALTER TABLE cadence_dispatches ENABLE ROW LEVEL SECURITY;   -- default-deny
> 393	CREATE POLICY "cadence_dispatches_select_own"
> 394	  ON cadence_dispatches FOR SELECT USING (user_id = auth.uid());
> 395	-- INSERT/UPDATE só service_role (sem policy p/ authenticated ⇒ negado).
> 396	```
> 397	
> 398	### 7.3 `20260716120200_erase_lead_cascade_cadence.sql` (FR-CAD-017 / G9 / OTD-CAD-006)
> 399	
> 400	```sql
> 401	-- Estender erase_lead() para cancelar agendamentos futuros NA MESMA TRANSAÇÃO (LGPD Art. 16/18 VI).
> 402	-- (SECURITY DEFINER, search_path='', tenant-guarded — mantém o padrão existente.)
> 403	--   UPDATE scheduled_posts SET status='cancelled' WHERE lead_id = p_lead AND status='pending';
> 404	--   UPDATE cadence_dispatches SET status='failed', error='erased'
> 405	--     WHERE user_id = <lead owner> AND status IN ('queued','publishing') AND <bound ao lead>;
> 406	-- Atomicidade: rollback se qualquer passo falhar. Sem isso o direito de eliminação é ficção.
> 407	```
> 408	
> 409	### 7.4 `20260716120300_auto_publish_pgcron_skiplocked.sql` (FR-CAD-018 / OTD-CAD-004)
> 410	
> 411	```sql
> 412	-- Migrar auto-publish de crontab de SO → pg_cron; drain com FOR UPDATE SKIP LOCKED.
> 413	-- SELECT cron.schedule('auto-publish', '*/5 * * * *', $$ ... $$);
> 414	-- Query de claim: SELECT ... FROM scheduled_posts WHERE status='pending' AND scheduled_at <= now()
> 415	--                 FOR UPDATE SKIP LOCKED LIMIT <batch>;
> 416	-- Pré-requisito declarado ("antes de ligar recorrência") — a Fatia 1 não pode nascer
> 417	-- sobre um sink sem lock num único host de SO.
> 418	```
> 419	
> 420	### 7.5 `[PROBE-GATED]` `social_threads` / `social_messages` (FR-CAD-012 — Fatia 2, NÃO codar antes do probe)
> 421	
> 422	```sql
> 423	-- Congelado até o probe FM-CAD-02 fechar (DM real de terceiro sem role + payload cru).
> 424	-- social_threads: id, user_id, external_thread_id, csw_expires_at timestamptz (24h, servidor),
> 425	--                 private_reply_deadline timestamptz (7d por comentário), UNIQUE(comment_id) na fila.
> 426	-- fila de DM: inbound_event_id uuid NOT NULL REFERENCES lead_events (message_received do mesmo user_id)
> 427	--             ⇒ cold DM IMPOSSÍVEL de representar (G1). RLS select_own + escrita service-role.
> 428	```
> 429	
> 430	---
> 431	
> 432	## 8. Open Technical Decisions (seladas nesta SDD)
> 433	
> 434	> A FRD §7 listou 7 decisões abertas. Esta SDD **sela** cada uma com o default do blueprint (§11). `deferred` carrega justificativa material.
> 435	
> 436	| ID | Description | Option A | Option B | **Decisão selada** | Owner |
> 437	|----|-------------|----------|----------|--------------------|-------|
> 438	| OTD-CAD-002 | Sujeito da cadência | Asset existente (0 mco) | Geração por ciclo (begin/finalize) | **A — asset existente** (Fatia 1 keyless, 0 mco; geração fica p/ fatia futura) | Sovereign |
> 439	| OTD-CAD-003 | Motor de recorrência | Estender `autopilot_plans` | Tabela nova `cadence_plans` + 3º driver | **A — estender** (2 motores idênticos em prod; 3º triplica índice due/kill-switch/cap/identidade cron). Se B, reusar o **MESMO** job pg_cron | Sovereign |
> 440	| OTD-CAD-004 | `auto-publish` sem lock | crontab de SO | pg_cron + `SKIP LOCKED` | **B — pg_cron+SKIP LOCKED** — promovido a **Fatia 0 item 5** (pré-requisito, não pergunta) | Sovereign |
> 441	| OTD-CAD-006 | Semântica `cadence_dispatches` | Índice parcial + `UPDATE` service-role (retry, at-least-once) | Append-only puro (at-most-once, sem retry) | **A — retry via índice parcial** (FM-CAD-01/03 dependem do predicado `WHERE status<>'failed'`) | Sovereign |
> 442	| OTD-CAD-008 | `channel_profiles.cadence` | Teto autoritativo | Sugestão | **A — autoritativo** (ressuscita o dado morto; vira teto do frequency-cap) | Sovereign |
> 443	| OTD-CAD-011 | X pay-per-use (Post-com-URL = **45 mco**) | X na allowlist Fatia 1 | X fora até probe de créditos | **B — X FORA da Fatia 1** (`channel_allowlist` de plano = auto-publish MENOS X); reentra após probe do Console (ação Sovereign) | Sovereign |
> 444	| OTD-CAD-017 | Escopo do frequency-cap | `(user, channel)` | `(user, channel, conta)` | **A — `(user, channel)` na Fatia 1** (`channel_profiles` não tem noção de conta; refinar p/ conta quando o pool tiver 2 IGs) | Sovereign |
> 445	| OTD-CAD-018 | IG/Messenger app | Manter no app Meta **global** (caps por-app + kill-switch global) | BYOK-de-app espelhando WhatsApp | **A — global até o Usuário 1**, com cap de fan-out por-APP + kill-switch global + telemetria de feedback negativo por-app **obrigatórios** | Sovereign |
> 446	| — (jurisdição G11) | Lead sem país conhecido | Tratar como UE (opt-in prévio) | Permissivo | **UE fail-closed** (opt-in prévio; custa conversão mas é seguro) | Sovereign |
> 447	| OTD-CAD-015 | Base legal no Brasil | `consent` fail-closed | aceitar `legitimate_interest` | **`consent` fail-closed** até o Guia ANPD ser extraído literal | Sovereign |
> 448	
> 449	**Bloqueantes que permanecem gated (não decisão de design — provisão Sovereign):** OTD-CAD-001 (Fatia 0, P0) · OTD-CAD-005 (carrossel fora da cadência até fechar) · OTD-CAD-009 (enquadramento AI Provider WhatsApp Brasil — bloqueante econômico do auto-reply) · OTD-CAD-010 (legitimidade contratual BYOK — jurídico Meta) · OTD-CAD-012 (rate-limit Send API — empírico) · OTD-CAD-013 (TikTok — zero FR até probe) · OTD-CAD-014 (AI Act Art. 50(2) — módulo próprio, vigência 2026-08-02) · OTD-CAD-016 (ingestão de `creative_metrics.hook_rate` — pré-requisito de **ligar** o A/B). **FR-CAD-012/013 permanecem `[PROBE-GATED]` (FM-CAD-02, RPN 486).**
> 450	
> 451	---
> 452	
> 453	## 9. Pattern Conformance Declaration (Closed-Loop Step 3.5 — OBRIGATÓRIA)
> 454	
> 455	> SSOT: `docs/architecture/agentic-vision.md` §2 (21 padrões agênticos). **Declaração, não sign-off.** Este módulo toca ≥3 padrões materialmente ⇒ esta tabela é promovida a `09-pattern-conformance.md`. Reproduz §9 do blueprint, alinhada aos FR selados.
> 456	
> 457	| # | Pattern | Implemented? | How / Why-deferred |
> 458	|---|---------|:---:|---|
> 459	| 1 | Prompt Chaining | **yes** | `program jsonb` (steps `publish\|wait\|throttle\|digest\|branch`) executado sequencialmente por ciclo (FR-CAD-006) — molde `sequences.steps` + `current_step` |
> 460	| 2 | Routing | **yes** | Roteamento por **estado de janela/política** (gate chain FR-CAD-008/013): in-window → free-form; out-window → template APPROVED ou draft HITL; canal sem caminho legítimo → recusa estruturada (G1/G6) |
> 461	| 3 | Parallelization | **yes** | Fan-out **bounded** no driver (`MAX_PER_RUN=50`/`CONCURRENCY=6`, molde `autopilot-cadence-cron:15-16`) — FR-CAD-004 |
> 462	| 4 | Reflection | **deferred** | Crítico de copy é **classificador determinístico server-side**, não Generator-Critic. OTD-CAD-016 (loop A/B → `hook_rate`) é o embrião |
> 463	| 5 | Tool Use | **yes** | Edge fns tipadas `cadence-plan`/`cadence-run` roteadas pelo **tick existente** (sem cron novo — FR-CAD-004/005/006); Graph API/Telegram/Resend como tools per-user BYOK |
> 464	| 6 | Planning | **yes** | O plano **é** o artefato (`autopilot_plans.program`, `plan_kind='cadence'` — FR-CAD-002), pré-gerado/versionado; re-planejamento dinâmico fora de escopo |
> 465	| 7 | Multi-Agent | **n-a** | Cadência é motor determinístico single-agent; orquestração multi-agente vive no Pantheon/`orchestrate-*` a montante |
> 466	| 8 | Memory Management | **yes** | `social_threads`/`social_messages` (a Meta só devolve as **20 últimas** ⇒ memória de conversa mora aqui — FR-CAD-012) + nó de observação na Knowledge Mesh por ciclo |
> 467	| 9 | Learning & Adaptation | **deferred** | A/B determinístico (FR-CAD-010) existe, mas o loop fechado depende de ingestão confiável de `creative_metrics.hook_rate` — OTD-CAD-016 |
> 468	| 10 | Model Context Protocol | **n-a** | Nó não expõe superfície MCP (o Vision MCP é o servidor MCP do ecossistema) |
> 469	| 11 | Goal Setting & Monitoring | **yes** | `channel_profiles.cadence` (`target_per`/`count_min`/`count_max`) vira o **goal declarativo** por canal (FR-CAD-008); `cadence_dispatches` + `infra_health_logs` monitoram |
> 470	| 12 | Exception Handling & Recovery | **yes** | Idempotência por índice único parcial (falha libera/sucesso prende — FR-CAD-003), `overlap_policy`, `catchup_window`, retry com backoff (molde `auto-publish:200-212`), kill-switch `is_active` |
> 471	| 13 | Human-in-the-Loop | **yes** | Nasce **`delivery:'gated'`** (molde `nurture-dispatch:150`) + `publishMode:'draft'`; Human Agent tag **inalcançável** do caminho automático (G5); flip para `'sent'` = GO Sovereign |
> 472	| 14 | Knowledge Retrieval (RAG) | **n-a** | Cadência não recupera conhecimento; consome asset/pilar já produzido a montante |
> 473	| 15 | Inter-Agent Comm. (A2A) | **n-a** | Sem interação agente-agente; a comunicação é sistema↔plataforma externa |
> 474	| 16 | Resource-Aware Optimization | **yes** | Caps `daily`/`budget_cap_mco` NOT NULL; frequency-cap com HALT (FR-CAD-008); mcoCoins 4×-floor (X DM = 4 mco); `begin`/`finalize` atômico se houver geração |
> 475	| 17 | Reasoning Techniques | **deferred** | `optimize-schedule` (LLM per-user) como **oráculo opcional** de horário; default é janela determinística (LLM em cron = custo + flakiness) — OTD-CAD-008 |
> 476	| 18 | Guardrails / Safety | **yes** | 14 guardrails de §6 do blueprint **estruturais** (FK NOT NULL, `UNIQUE(comment_id)`, fail-closed 402/422, separação de caminho da human_agent tag, IoC anti-browser-automation) — NFR-CAD-010 |
> 477	| 19 | Evaluation & Monitoring | **yes** | `cadence_dispatches` (status transiciona service-role, não append-only puro — FR-CAD-003) + reconciliação por webhook de status (nunca 202 — NFR-CAD-002) + `infra_health_logs` + `notify()` |
> 478	| 20 | Prioritization | **deferred** | Sem álgebra de priorização entre planos concorrentes do mesmo tenant (risco de starvation no cap) — herda o gap de OTD-AG do ledger |
> 479	| 21 | Exploration & Discovery | **deferred** | A/B determinístico é exploração **rasa** (bucket fixo); torneio/Elo entre variantes fica p/ o loop de `creative_metrics` — OTD-CAD-016 |
> 480	
> 481	**Resumo:** 12 `yes` · 5 `deferred` (todos com OTD/justificativa material) · 4 `n-a`. Nenhum `deferred` sem âncora.
> 482	
> 483	---
> 484	
> 485	## 10. Mesh Connection Mandate (rastreabilidade obrigatória)
> 486	
> 487	- **Nó de observação** inserido em `mcorch_nodes` no primeiro ciclo bem-sucedido de cada plano de cadência (`node_type='observation'`, `revenue_impact` ligado ao `collective_efficiency_ledger`).
> 488	- **`infra_health_logs`** recebe entrada em **todo** path de falha (`service='spaces-cadence'`).
> 489	- **Traceability BR/FR:** cada objeto de design ↔ FR-CAD-xxx (FRD §2) ↔ BR-CAD-xxx (BRD) ↔ PR-CAD-xxx (PRD).
> 490	- **Traceability Pattern:** §9 mapeia cada feature aos 21 padrões agênticos.
> 491	
> 492	---
> 493	
> 494	## 11. Survival Laws Self-check (design-time)
> 495	
> 496	- **Lei 1 (Materialidade):** todo FR carrega critério de aceite material na FRD §2.1; esta SDD **não** declara sucesso (é design). O `sent` só do webhook de status e o A/B com cast `bigint` antes do `abs` são invariantes anti-mentira-silenciosa.
> 497	- **Lei 2 (Processo):** SOP `docs/processes/spaces-cadence.md` permanece **aberto** — pré-requisito antes de qualquer código (Operator/Sequence/Verification/Recovery/Success).
> 498	- **Lei 3 (Pruning):** N/A em design-time.
> 499	- **Lei 4 (ORO):** triplet declarado no cabeçalho.
> 500	
> 501	---
> 502	
> 503	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` + `01-mrd.md` + `02-brd.md` + `03-prd.md` + `04-frd.md` (Lei 1: nenhum FR/NFR/OTD/FM/entidade/pattern inventado além do blueprint; FR-CAD-012/013 sob `[PROBE-GATED]`; §3 sob selo de não-verificação). Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança via RPC atômica begin/finalize (nunca client-side); verify_jwt=false → ES256 JWKS / HMAC timingSafeEqual (nunca `atob` cego); RLS default-deny owner-scoped. A Cadência ENCAIXA nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), não reconstrói distribuição — nenhum job pg_cron novo. Pattern Conformance Declaration (§9) = gate Closed-Loop Step 3.5, a ser promovida a `09-pattern-conformance.md`._
> 504	
> ```

## 🤖 Claude *(14:56:15)*

<details>
<summary>💭 Thinking Process</summary>

The SDD looks solid with the Pattern Conformance Declaration covering all 21 patterns and key features like BYOK, ES256 JWKS, and per-tenant coin deduction properly documented. Now I'm moving through the remaining documentation to verify functional requirements trace through the data model and process flow, and I'll spot-check the MR as well.

I'm noticing the billing implementation uses the begin/finalize autopilot cycle RPC pattern rather than calling deduct_mco_coins directly, which aligns with the reuse principle documented in the SDD. Let me confirm this satisfies the requirement for per-tenant atomic billing.

</details>


## 🤖 Claude *(14:56:15)*

Now the FRD (FR traceability), data-model, and process-flow to verify FRs reappear.

## 🤖 Claude *(14:56:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/04-frd.md"
}
```

## 🤖 Claude *(14:56:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/06-data-model.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements) + CISSP CBK (security controls)
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14) + [`01-mrd.md`](01-mrd.md) + [`02-brd.md`](02-brd.md) + [`03-prd.md`](03-prd.md). Cada FR abaixo deriva 1:1 de um `PR-CAD-xxx` (PRD §4) e das seções §5/§6/§7 do blueprint; nada é inventado além dele (Lei 1).
> 8	
> 9	> **ORO triplet desta task:**
> 10	> - **Operator:** MCORCH Master Execution Agent
> 11	> - **Reviewer:** Sovereign (Gabriel)
> 12	> - **Owner:** Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 13	>
> 14	> **Closed-Loop gate:** este é o **4º** documento da suíte. Permanecem ABERTOS: 04-frd → **05-sdd**, `09-pattern-conformance.md` (os 21 padrões agênticos), SOP Lei 2 (`docs/processes/spaces-cadence.md`), `/security-review` de toda migration. **Nenhuma linha de código antes disso.**
> 15	>
> 16	> **Nota de fidelidade (Lei 1):** o blueprint declara **zero FR de inbound** antes do payload cru de DM real. Esta FRD **sela** a numeração `FR-CAD-xxx` (era candidata na PRD), mas **FR-CAD-012/013 nascem `[PROBE-GATED]`** — são especificação **condicional**, ativável só após o probe FM-CAD-02 fechar; até lá não geram código. §3 (posicionamento vs. ManyChat) permanece sob **SELO DE NÃO-VERIFICAÇÃO**: nenhum critério de aceite abaixo cita §3 como fato.
> 17	
> 18	---
> 19	
> 20	## 1. Scope Statement
> 21	
> 22	Este documento especifica os requisitos funcionais (FR) e não-funcionais (NFR) do módulo `spaces-cadence` — o **nó Cadência** do Canvas Studio e o **motor de sequência recorrente Postgres-first** que o alimenta. Deriva da PRD `03-prd.md` e alimenta diretamente a SDD `05-sdd.md`.
> 23	
> 24	**In scope (Fatia 0 + Fatia 1 — MVP, ZERO app review):**
> 25	- `kind: cadence` no canvas registry (categoria Publish), keyless, excluído do gate "runnable".
> 26	- Estensão de `autopilot_plans` (`plan_kind`, `recurrence`, `quiet_hours`, `overlap_policy`, `catchup_window`, `jitter_seconds`, `program`, `channel_allowlist`, `budget_cap_mco`) — **migration única**, sem tabela paralela e **sem job pg_cron novo**.
> 27	- Ledger novo `cadence_dispatches` (idempotência por índice único parcial).
> 28	- Edges `cadence-plan` (arm) e `cadence-run` (drain + gate chain + dispatch + re-arm).
> 29	- Roteamento do tick vivo `autopilot-cadence-cron` por `plan_kind`.
> 30	- Gate chain server-side: quiet-hours (fuso do sujeito), frequency-cap HALT (`channel_profiles.cadence`), dedup/digest, A/B determinístico, opt-out no send, jurisdição fail-closed.
> 31	- Inspector projetando **custo por ciclo em mco** antes de armar; `budget_cap_mco NOT NULL`.
> 32	- Fatia 0 (P0): `whatsapp-webhook` alcançável + `timingSafeEqual`; `estimateNodeCost` case `publishSocial`; `erase_lead()` cascata; `auto-publish` → pg_cron + `FOR UPDATE SKIP LOCKED`.
> 33	
> 34	**In scope condicional (Fatia 2 `[PROBE-GATED]` + Fatia 3 BYOK):**
> 35	- FR-CAD-012/013 (inbox IG) — especificação **congelada** até o probe FM-CAD-02 fechar com DM real de terceiro sem role + payload cru.
> 36	- FR-CAD-014 (Telegram + Email Resend) — BYOK per-user fail-closed; flip de `nurture-dispatch` só com GO Sovereign.
> 37	
> 38	**Out of scope (Won't Have / Fatia 4 GATED):** cold DM em qualquer canal; broadcast/newsletter por DM no IG; SMS; Discord; LinkedIn DM automatizada; TikTok DM/comment (zero FR até probe — OTD-CAD-013); carrossel dentro da cadência (até OTD-CAD-005 fechar); marcação C2PA/AI-Act Art. 50(2) (módulo próprio — OTD-CAD-014); WhatsApp Cloud BYOK, X na allowlist, Messenger, IG multi-tenant, LinkedIn comment reply (Fatia 4, cada um gated por provisão Sovereign específica).
> 39	
> 40	---
> 41	
> 42	## 2. Functional Requirements
> 43	
> 44	> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron`
> 45	> Priority: `Critical` (MVP não fecha sem) | `High` | `Medium`.
> 46	> **Todo FR carrega um critério de aceite MATERIAL** (Lei 1) na coluna homônima da §2.1 — não "funciona", mas o artefato verificável (UUID/linha/status HTTP/output de smoke).
> 47	
> 48	| ID | Title | Priority | PR Traced | BR Traced | Category | OTD / FM | Test ID |
> 49	|----|-------|----------|-----------|-----------|----------|----------|---------|
> 50	| **FR-CAD-015** | Fatia 0: `whatsapp-webhook` alcançável + HMAC `timingSafeEqual` + sink `leads`/`lead_events` | Critical | PR-CAD-012 | BR-CAD-017 | EdgeFunction · DB | OTD-CAD-001 · FM-CAD-09 | AT-CAD-015 |
> 51	| **FR-CAD-016** | Fatia 0: `estimateNodeCost` case `publishSocial` (evita `runAllCost` NaN) | Critical | PR-CAD-012 | BR-CAD-017 | UI | OTD-CAD-007 · FM-CAD-16 | AT-CAD-016 |
> 52	| **FR-CAD-017** | Fatia 0: `erase_lead()` cancela agendamentos futuros em cascata (mesma transação) | Critical | PR-CAD-012 | BR-CAD-017, BR-CAD-014 | DB | OTD-CAD-006 · FM-CAD-04 · G9 | AT-CAD-017 |
> 53	| **FR-CAD-018** | Fatia 0: `auto-publish` migra p/ pg_cron + `FOR UPDATE SKIP LOCKED` | Critical | PR-CAD-012 | BR-CAD-017, BR-CAD-011 | Cron · DB | OTD-CAD-004 · FM-CAD-01 | AT-CAD-018 |
> 54	| **FR-CAD-001** | Nó `cadence` no canvas registry (categoria Publish), keyless, excluído do gate "runnable" | Critical | PR-CAD-001 | BR-CAD-001 | UI | OTD-CAD-002, OTD-CAD-007 | AT-CAD-001 |
> 55	| **FR-CAD-002** | Estender `autopilot_plans` (9 colunas + DROP CHECK `platforms`) — migration única | Critical | PR-CAD-003 | BR-CAD-002, BR-CAD-004 | DB | OTD-CAD-003 | AT-CAD-002 |
> 56	| **FR-CAD-003** | Ledger `cadence_dispatches` + índice único **parcial** `WHERE status<>'failed'` | Critical | PR-CAD-004 | BR-CAD-003 | DB | OTD-CAD-006 · FM-CAD-01 | AT-CAD-003 |
> 57	| **FR-CAD-004** | Rotear o tick vivo `autopilot-cadence-cron` por `plan_kind` (sem job pg_cron novo) | Critical | PR-CAD-003 | BR-CAD-002, BR-CAD-004 | Cron | OTD-CAD-003 · FM-CAD-06 | AT-CAD-004 |
> 58	| **FR-CAD-005** | Edge `cadence-plan` (upsert do plano + arm `next_run_at` UTC) + inspector poll | Critical | PR-CAD-002 | BR-CAD-004 | EdgeFunction · UI | — | AT-CAD-005 |
> 59	| **FR-CAD-006** | Edge `cadence-run` (drain `SKIP LOCKED`, gate chain, dispatch→`scheduled_posts`, ledger, re-arm) | Critical | PR-CAD-005 | BR-CAD-009, BR-CAD-011, BR-CAD-013 | EdgeFunction | OTD-CAD-004, OTD-CAD-005 · FM-CAD-01/05/07 | AT-CAD-006 |
> 60	| **FR-CAD-007** | Re-arm UTC generalizado `{frequency, days, hours, minutes, tz}` | Critical | PR-CAD-006 | BR-CAD-005 | EdgeFunction · DB | FM-CAD-06 | AT-CAD-007 |
> 61	| **FR-CAD-008** | Quiet-hours (fuso do sujeito, cascata) + frequency-cap **HALT** lendo `channel_profiles.cadence` | High | PR-CAD-007 | BR-CAD-006 | EdgeFunction | OTD-CAD-008, OTD-CAD-017 · FM-CAD-07 · G3/G4 | AT-CAD-008 |
> 62	| **FR-CAD-009** | Dedup/digest `(user, channel, dia)` colapsa N vencimentos em 1 publicação | High | PR-CAD-008 | BR-CAD-007 | EdgeFunction | — | AT-CAD-009 |
> 63	| **FR-CAD-010** | A/B determinístico `mod(abs(hashtext(subject‖:‖exp)::bigint),100) < ratio` | High | PR-CAD-009 | BR-CAD-008 | EdgeFunction · DB | OTD-CAD-016 | AT-CAD-010 |
> 64	| **FR-CAD-011** | Inspector projeta **custo por ciclo em mco** antes de armar; `budget_cap_mco NOT NULL` | Critical | PR-CAD-010 | BR-CAD-010, BR-CAD-012 | UI · Hook | OTD-CAD-011 | AT-CAD-011 |
> 65	| **FR-CAD-014** | Canais BYOK desimpedidos: Telegram (US$0) + Email Resend (flip `nurture-dispatch`), fail-closed | High | PR-CAD-020, PR-CAD-021 | BR-CAD-016, BR-CAD-013 | EdgeFunction · DB | OTD-CAD-009 · FM-CAD-12 · G10/G12 | AT-CAD-014 |
> 66	| **FR-CAD-012** `[PROBE-GATED]` | `instagram-webhook` trata `entry.messaging`(DM)+`comments` → `lead_events`/`social_threads` | High | PR-CAD-030 | BR-CAD-015 | EdgeFunction · DB | FM-CAD-02 (RPN 486), FM-CAD-13 · G1 | AT-CAD-012 |
> 67	| **FR-CAD-013** `[PROBE-GATED]` | Private reply comment→DM `UNIQUE(comment_id)` deadline 7d; resposta in-window 24h; `delivery:'gated'` | High | PR-CAD-030 | BR-CAD-015 | EdgeFunction · DB | FM-CAD-03, OTD-CAD-018 · G2/G5/G6 | AT-CAD-013 |
> 68	
> 69	### 2.1 Detailed Functional Requirements (com critério de aceite material)
> 70	
> 71	#### Fatia 0 — Pré-requisitos P0 (sem eles, tudo é falso-sucesso)
> 72	
> 73	**FR-CAD-015 — `whatsapp-webhook` alcançável + HMAC timing-safe + sink correto**
> 74	Adicionar o bloco `[functions.whatsapp-webhook] verify_jwt = false` em `supabase/config.toml` (hoje ausente ⇒ gateway responde 401 e o webhook nunca é chamado). Trocar a comparação de assinatura HMAC de `===` para `timingSafeEqual` (`_shared/oauth-state.ts`). Redirecionar o destino do payload de `whatsapp_leads` (tabela absorvida por OTD-MH-001) para `leads`/`lead_events`. Na variante BYOK (Fatia 4), resolver o tenant pelo `phone_number_id`/`waba_id` **antes** de buscar o app secret e validar (FM-CAD-09).
> 75	- **Critério material:** `curl -s -o /dev/null -w "%{http_code}" .../functions/v1/whatsapp-webhook` retorna **não-401** (challenge `hub.challenge` ecoado); `grep timingSafeEqual supabase/functions/whatsapp-webhook/index.ts` retorna ≥1 linha; **zero** referência a `===` na verificação de assinatura; um POST assinado com secret válido insere linha em `lead_events` (UUID retornado por `SELECT`).
> 76	
> 77	**FR-CAD-016 — `estimateNodeCost` case `publishSocial`**
> 78	Adicionar o `case 'publishSocial'` ao switch de `estimateNodeCost` (bug aberto: kind sem case ⇒ `undefined` em runtime; `strict:false` esconde). Corrigir **antes** de somar o kind `cadence` no `runAllCost`.
> 79	- **Critério material:** teste unitário prova que `runAllCost` de um grafo com nó `publishSocial` retorna número finito (não `NaN`); checklist manual de 6 edições de canvas registrado no PR (FM-CAD-16).
> 80	
> 81	**FR-CAD-017 — `erase_lead()` cancela agendamentos futuros em cascata**
> 82	Estender `erase_lead()` (`…20260603000000…:130-169`) para cancelar, **na mesma transação**, todos os agendamentos futuros do lead: linhas pendentes em `scheduled_posts` + fila de DM (`cadence_dispatches` com `status` não-terminal). Sem isso o direito de eliminação (LGPD Art. 16/18 VI) é ficção (G9).
> 83	- **Critério material:** após `SELECT erase_lead('<uuid>')`, `SELECT count(*) FROM scheduled_posts WHERE ... AND status='pending'` = **0** e `SELECT count(*) FROM cadence_dispatches WHERE ... AND status IN ('queued','publishing')` = **0** para aquele lead; a operação é atômica (rollback comprovado se qualquer passo falhar).
> 84	
> 85	**FR-CAD-018 — `auto-publish` em pg_cron + `FOR UPDATE SKIP LOCKED`**
> 86	Migrar `auto-publish` de crontab de SO de um único host para **pg_cron**, drenando `scheduled_posts` com `SELECT … FOR UPDATE SKIP LOCKED`. Pré-requisito declarado ("antes de ligar recorrência") — a cadência não pode nascer sobre um sink sem lock num único host de SO.
> 87	- **Critério material:** `SELECT jobname, schedule FROM cron.job WHERE command ILIKE '%auto-publish%'` retorna ≥1 linha; a query de claim contém `FOR UPDATE SKIP LOCKED` (grep na migration); smoke prova que dois runs concorrentes **não** publicam a mesma linha 2× (FM-CAD-01).
> 88	
> 89	#### Fatia 1 — Cadência de Publicação (ZERO app review)
> 90	
> 91	**FR-CAD-001 — Nó `cadence` no Canvas Studio**
> 92	Registrar `kind: 'cadence'` no canvas registry, categoria **Publish**. `CadenceData = { kind:'cadence', label, status, sourceAssetId?: string (creative_assets.id owner-scoped), planId?: string, program: CadenceStep[], enabled: boolean, output?, error? }`. `resolveExecutePayload → null`; `estimateNodeCost → 0` (não viola G7 — a cobrança é do **ciclo**, não do nó). Excluído do gate "runnable" de `useCanvasPipeline.ts:33-50` (não exige `prompt`). Único `<Handle>` target `input_asset` (id inline, molde `PublishSocialNode`). Aliases pt-BR no registry: **cadência / agendar / recorrente / cron / calendário**.
> 93	- **Critério material:** as **6 edições** (types/registry/node/nodeTypes/RightPanel/inspector) presentes no diff; adicionar o nó ao grafo persiste em `vm_canvas_projects.graph` (SELECT do jsonb mostra `"kind":"cadence"`); `runAllCost` do grafo com o nó `cadence` **não** vira NaN e soma 0 para o nó.
> 94	
> 95	**FR-CAD-002 — Estender `autopilot_plans` (migration única)**
> 96	`ALTER TABLE autopilot_plans`: `DROP CONSTRAINT <platforms_check>`; `ADD COLUMN plan_kind text NOT NULL DEFAULT 'viral' CHECK (plan_kind IN ('viral','cadence'))`; `ADD COLUMN recurrence jsonb` (`{frequency, days, hours, minutes, tz}`); `quiet_hours jsonb`; `overlap_policy text DEFAULT 'skip'`; `catchup_window interval DEFAULT '6 hours'`; `jitter_seconds int DEFAULT 0`; `program jsonb` (molde `sequences.steps`+`current_step`); `channel_allowlist text[]` (por plano, não constante); `budget_cap_mco int NOT NULL` (em mcoCoins, nunca USD). RLS owner-scoped **preservada**; nenhuma tabela paralela, nenhum 3º driver (OTD-CAD-003).
> 97	- **Critério material:** `\d autopilot_plans` (ou `information_schema.columns`) lista as 9 colunas novas com os defaults/CHECK exatos; a constraint `platforms_check` **não** existe mais; `/security-review` da migration retorna **NO FINDINGS**; planos `plan_kind='viral'` existentes continuam válidos (regressão smoke do autopilot verde).
> 98	
> 99	**FR-CAD-003 — Ledger `cadence_dispatches`**
> 100	Tabela nova: `plan_id`, `step_index`, `occurrence_at`, `idempotency_key`, `channel`, `status`, `target_ref`, `error`, `external_usd_cost numeric`, `cost_source text`. Índice **único PARCIAL com predicado declarado**: `CREATE UNIQUE INDEX cadence_dispatches_idem ON cadence_dispatches (idempotency_key) WHERE status <> 'failed';` — é o predicado (e só ele) que produz "**falha libera** a chave / **sucesso prende**". RLS: `select_own` (cliente lê) + `insert` service-role + `update` service-role (`status`/`error`/`external_usd_cost`). **O cliente nunca escreve.** Não é append-only puro (semântica transiciona; se o Sovereign preferir append-only, cai para at-most-once — OTD-CAD-006).
> 101	- **Critério material:** o índice aparece em `pg_indexes` com o predicado `WHERE (status <> 'failed'::text)`; um segundo `INSERT` com a mesma `idempotency_key` e `status<>'failed'` viola a unique (SQLSTATE 23505 ou `ON CONFLICT DO NOTHING` retorna 0 linhas); um `INSERT` do cliente (anon/user role) é **negado** por RLS; `/security-review` NO FINDINGS.
> 102	
> 103	**FR-CAD-004 — Roteamento do tick por `plan_kind`**
> 104	O tick vivo `autopilot-cadence-cron` (*/15, gate `Authorization !== Bearer SB_SECRET_KEY` → 403, `user_id` **server-trusted da linha, nunca do body** — SOP `autopilot-cron-identity.md`) passa a **rotear por `plan_kind`**: `viral` → `autopilot-run` (como hoje); `cadence` → `cadence-run` (edge nova). **Nenhum job pg_cron novo** (o mesmo tick varre as duas classes; Supabase recomenda ≤~8 jobs concorrentes). pg_cron roda em **GMT** ⇒ preferência de horário **jamais** vira cron expression.
> 105	- **Critério material:** `SELECT count(*) FROM cron.job` **inalterado** antes/depois (nenhum job adicionado); log do tick mostra dispatch a `cadence-run` para linhas `plan_kind='cadence'` e a `autopilot-run` para `plan_kind='viral'`; um POST ao tick sem `Bearer SB_SECRET_KEY` retorna **403**.
> 106	
> 107	**FR-CAD-005 — Edge `cadence-plan` (arm)**
> 108	Edge fn nova `cadence-plan`: recebe o payload do inspector, faz **upsert** do plano em `autopilot_plans` (`plan_kind='cadence'`) e arma `next_run_at` computado em **UTC** a partir de `recurrence`. Gate `Bearer SB_SECRET_KEY`→403 quando cron; JWT de usuário quando UI (verify_jwt=false → **ES256 JWKS verify**, nunca `atob` cego). `user_id` **server-trusted**. Criar o plano custa **0 mco**. Inspector faz poll das últimas N dispatches + `next_run_at` no **molde `useVoiceRenderPoll`** (id no `data` do nó, sobrevive a refresh — nunca `sleep(8s)×25`).
> 109	- **Critério material:** POST válido retorna `plan_id` (UUID) e o `SELECT` da linha mostra `plan_kind='cadence'` + `next_run_at` em UTC coerente com a `recurrence`; JWT forjado/ausente → 401/403; o poll re-hidrata após refresh do browser (id persistido no grafo); **0** débito de mco na criação (`profiles.mco_balance` inalterado).
> 110	
> 111	**FR-CAD-006 — Edge `cadence-run` (drain + gate chain + dispatch + re-arm)**
> 112	Edge fn nova invocada pelo tick para `plan_kind='cadence'`. Sequência: (1) **drain** dos planos vencidos com `SELECT … FOR UPDATE SKIP LOCKED`; (2) resolve o **subject** owner-scoped (`creative_assets.id`); (3) **gate chain** server-side (FR-CAD-008/009/010 + opt-out + jurisdição — nunca LLM); (4) **dispatch**: enfileira em `scheduled_posts` via o contrato `metadata.reshape` + `schedule:true` + `publish_at` ISO (Amendment 22) — o nó **enfileira, não publica**; (5) **ledger** `cadence_dispatches` via `INSERT … ON CONFLICT DO NOTHING RETURNING` sob o índice parcial; (6) **re-arm** `next_run_at` (FR-CAD-007) ou `deactivate`. `overlap_policy=skip` (ciclo anterior rodando ⇒ pula). Reconciliação: `sent` **só do webhook de status**, nunca do 202 (FM-CAD-05). Se houver passo `generate`, cobrança via `begin`/`finalize` atômico (G7 = invariante do ciclo).
> 113	- **Critério material:** um plano com `next_run_at` vencido produz **1** linha em `cadence_dispatches` + **1** linha `pending` em `scheduled_posts` (UUIDs); tick sobreposto/retry **não** cria 2º dispatch para a mesma `(plan_id, step_index, occurrence_at)` (smoke re-executável, 0 double-post); nenhuma linha marca `sent` a partir de um 202 (só do webhook de status); `next_run_at` avança em UTC.
> 114	
> 115	**FR-CAD-007 — Re-arm UTC generalizado**
> 116	Generalizar o re-arm de `autopilot-run/index.ts:310-314` (`now + interval_days`) para um calculador UTC de `{frequency, days, hours, minutes, tz}`. O cron **nunca** carrega preferência de horário — o horário do sujeito é convertido para UTC e gravado em `next_run_at`. Ressuscita `profiles.timezone` como SSOT de fuso (cascata `recurrence.tz → profiles.timezone → America/Sao_Paulo`).
> 117	- **Critério material:** dado `recurrence {frequency:'weekly', days:[1,3,5], hours:9, minutes:0, tz:'America/Sao_Paulo'}`, o `next_run_at` gravado corresponde à próxima 2ª/4ª/6ª 09:00 BRT **convertida para UTC** (12:00Z fora do DST); teste unitário do calculador cobre GMT vs. fuso do usuário (FM-CAD-06); `profiles.timezone` passa a ter ≥1 leitor (grep prova).
> 118	
> 119	**FR-CAD-008 — Quiet-hours + frequency-cap HALT**
> 120	Quiet-hours: janela `[start,end]` + weekdays no **fuso do sujeito** (cascata acima); dispatch em quiet-hours é **suprimido**. Frequency-cap: chave `(user_id, channel)` + janela + threshold, com **HALT** (não reenfileiramento — semântica Knock). Teto autoritativo = `channel_profiles.cadence` (`target_per`/`count_min`/`count_max`), que ganha o **primeiro leitor** do repo (OTD-CAD-008 = autoritativo). Decisão pendente: cap por `(user,channel)` vs `(user,channel,conta)` (OTD-CAD-017 — a selar na SDD). Contador de janela **não existe hoje** (a SDD deve criá-lo).
> 121	- **Critério material:** dispatch cujo horário cai em quiet-hours no fuso do sujeito **não** produz linha em `scheduled_posts`; dispatch cujo canal já atingiu o teto de `channel_profiles.cadence` na janela faz **HALT** (0 publicação, toast pt-BR informativo, **não** reenfileira); `channel_profiles.cadence` tem ≥1 leitor (grep prova).
> 122	
> 123	**FR-CAD-009 — Dedup/digest**
> 124	`digestKey = (user, channel, dia)` colapsa N vencimentos do mesmo canal no mesmo dia em **1** publicação (ou 1 carrossel — carrossel gated por OTD-CAD-005). É a diferença estrutural entre **cadência** e **flood**.
> 125	- **Critério material:** dado um plano que produz 3 vencimentos do mesmo canal no mesmo dia, o dispatch resulta em **1** linha em `scheduled_posts` (não 3); smoke prova o colapso.
> 126	
> 127	**FR-CAD-010 — A/B determinístico**
> 128	Fórmula **exata** (a SDD copia literalmente): `mod(abs(hashtext(subject_ref || ':' || experiment_key)::bigint), 100) < ratio`. **Proibido** `hashtext(...) % 100 < ratio` (retorna `integer` com sinal; `-42 % 100 = -42 < ratio` para qualquer ratio ≥ 0 ⇒ ~50% caem no bucket A, enviesando em silêncio). O cast para `bigint` vem **antes** do `abs` (`abs(int4min)` estoura). Estável entre retries (nunca `random()`). Loop fecha em `creative_metrics.hook_rate` (OTD-CAD-016 — a ingestão confiável é pré-requisito de **ligar** o A/B).
> 129	- **Critério material:** teste unitário prova que, com `ratio=30`, ~30% (±tolerância) de N subjects caem no bucket A e o mesmo subject cai **sempre** no mesmo bucket entre retries; teste negativo prova que a variante `% 100` produziria ~50% (regressão barrada).
> 130	
> 131	**FR-CAD-011 — Custo projetado por ciclo + `budget_cap_mco`**
> 132	O inspector **DEVE exibir** o custo projetado por ciclo em mco = `Σ (custo em mco de cada canal do plano) × ocorrências até o cap`, em `--gold`, **antes** do botão Armar. Ex.: plano diário 30d com X-post-com-link (45 mco) projeta **1.350 mco**. `budget_cap_mco` é **NOT NULL** e em **mcoCoins** (nunca USD). Obrigação compensatória do quote=0: "não cobrar ≠ não medir". Custo externo BYOK que o tenant absorve é **registrado** em `external_usd_cost` + `cost_source` **no reconcile** (webhook de status, nunca no 202), e agregado no `collective_efficiency_ledger`.
> 133	- **Critério material:** o inspector renderiza o número em mco antes de armar (screenshot Vision QA); tentar armar sem `budget_cap_mco` → **422** (NOT NULL); um dispatch BYOK com custo externo grava `external_usd_cost` numérico + `cost_source` na linha e a cobrança em mco é **0** (`SELECT` prova ambos); o custo entra no `collective_efficiency_ledger`.
> 134	
> 135	#### Fatia 3 — Canais desimpedidos BYOK
> 136	
> 137	**FR-CAD-014 — Telegram + Email Resend (BYOK per-user, fail-closed)**
> 138	**Telegram:** `telegram_bot_token` no pool per-user (coluna cifrada + UI Settings). Fail-closed `402 telegram_not_configured` (estruturado, com `action` de configuração) quando ausente. Opt-in **estrutural** via `/start` — o bot não fala com quem nunca deu `/start`. Custo Meta-free (US$0). **Email (Resend):** `resend_api_key` per-user cifrada + **domínio verificado do tenant**; flip do `nurture-dispatch` de `delivery:'gated'` → `'sent'`. O **rodapé (endereço postal + identificação de anúncio + opt-out) e o disclosure de IA são montados server-side** e concatenados ao corpo — **jamais** delegados ao prompt do LLM (G10/G12; FM-CAD-12). Flip só com GO Sovereign + domínio verificado.
> 139	- **Critério material:** Telegram sem token configurado → resposta **402** com body `{ error:'telegram_not_configured', action:... }`; envio a chat que nunca deu `/start` é bloqueado; Email — o corpo enviado contém o rodapé/opt-out/disclosure **concatenado server-side** (não presente no prompt, prova por diff do payload); flip `gated→sent` só ocorre com a flag de GO e domínio verificado (`SELECT` do estado).
> 140	
> 141	#### Fatia 2 — Laço Inbound IG `[PROBE-GATED]`
> 142	
> 143	> ⚠️ **FR-CAD-012/013 são especificação CONGELADA.** Não geram código antes do **probe FM-CAD-02** fechar: DM real de **terceiro sem role no app** aparecendo no banco + **payload cru** de `entry.messaging` arquivado (FM-CAD-13). Se o DM não chegar sob Standard Access, **App Review vira pré-requisito** e a Fatia 2 inteira está bloqueada. Nascem `delivery:'gated'`; flip para `'sent'` só com GO Sovereign.
> 144	
> 145	**FR-CAD-012 `[PROBE-GATED]` — Ingest inbound IG**
> 146	Estender `instagram-webhook` (reusando o esqueleto: HMAC `timingSafeEqual` + `hub.challenge`) para tratar `entry.messaging` (DM) e `entry.changes`+`comments`. Sink muda de `infra_health_logs` para: `lead_events(event_type='message_received')` + `leads` + `notify()` → `social_threads`/`social_messages`. `social_threads`/`social_messages` são **obrigatórias** (a Conversations API só devolve as **20 msgs mais recentes** ⇒ a Meta não é banco de histórico). Relógios derivados **no servidor**: `csw_expires_at` (24h) do inbound + `private_reply_deadline` (7d) por comentário.
> 147	- **Critério material:** o **probe** precede o código — a linha `lead_events(message_received)` de um DM real de terceiro sem role aparece por `SELECT` (UUID) e o payload cru fica arquivado; só então o branch `entry.messaging` é codado com o shape **fixado** pelo payload (nunca às cegas — FM-CAD-13); histórico persiste em `social_threads` (não depende das 20 da Meta).
> 148	
> 149	**FR-CAD-013 `[PROBE-GATED]` — Resposta na janela legal**
> 150	Gate chain server-side de resposta (nunca LLM): (a) **private reply** comment→DM 1× por comentário — `UNIQUE(comment_id)` na fila (retry duplicado = violação de política, não bug de UX — G2), CHECK de idade **no send**, deadline 7d; (b) **resposta in-window** dentro de 24h da CSW. Fora da janela: **nada promocional** (G6, classificador in/out-window no servidor). Cold DM **impossível de representar**: a fila tem **FK NOT NULL** para um inbound do mesmo `user_id` — sem inbound, a linha não existe (G1/FM-CAD-03). A **Human Agent tag** é **fisicamente inalcançável** do caminho service-role/pg_cron (separação de caminho, não `if` — G5). IG/Messenger no app **global** com cap de fan-out por-APP + kill-switch global + telemetria de feedback negativo por-app (OTD-CAD-018). Nasce `delivery:'gated'`. Resposta com link afiliado + UTM → `creative_metrics` → `collective_efficiency_ledger`.
> 151	- **Critério material:** tentar enfileirar DM sem inbound correspondente → **viola FK** (linha não existe); 2º private reply para o mesmo `comment_id` → viola `UNIQUE` (23505); dispatch fora da janela de 24h é **bloqueado no send** pelo classificador server-side; a Human Agent tag não é setável por nenhum caminho service-role (prova de separação); todo dispatch nasce `delivery:'gated'` (flip só com GO Sovereign).
> 152	
> 153	---
> 154	
> 155	## 3. Non-Functional Requirements
> 156	
> 157	| ID | Category | Requirement | Target | Measurement |
> 158	|----|----------|-------------|--------|-------------|
> 159	| NFR-CAD-001 | Correctness (idempotência) | Tick sobreposto/retry não produz double-post | **0** dispatches duplicados por `(plan_id, step_index, occurrence_at)` | Smoke re-executável + `count(*)` no ledger |
> 160	| NFR-CAD-002 | Correctness (materialidade) | `sent` só a partir do webhook de status, nunca do 202 | 100% | Auditoria de reconcile (FM-CAD-05) |
> 161	| NFR-CAD-003 | Correctness (fuso) | `next_run_at` computado em UTC; cron nunca carrega horário | 100% dos re-arms | Teste unitário do calculador (FM-CAD-06) |
> 162	| NFR-CAD-004 | Security | Edge fns verify_jwt=false → **ES256 JWKS verify** (nunca `atob` cego); HMAC `timingSafeEqual` | 100% dos endpoints | `/security-review` + teste ES256 |
> 163	| NFR-CAD-005 | Security (tenancy) | Credencial de provider **BYOK per-user** (`auth.uid()`); env = só infra; fail-closed 402/501 estruturado | 100%; **0** `Deno.env.get(<provider>)` em fluxo user-facing | `/security-review` + smoke fail-closed |
> 164	| NFR-CAD-006 | Security (RLS) | RLS default-deny owner-scoped; `cadence_dispatches` cliente **nunca** escreve | 100% | `/security-review` NO FINDINGS |
> 165	| NFR-CAD-007 | Economics | Cobrança **só via RPC atômica** `begin`/`finalize` (nunca client-side); quote==charge invariante do **ciclo** | 100% | Auditoria do ledger (G7) |
> 166	| NFR-CAD-008 | Economics (visibilidade) | Custo externo BYOK **registrado** em `external_usd_cost` mesmo com mco=0 | 100% dos dispatches BYOK | `SELECT` do ledger + `collective_efficiency_ledger` |
> 167	| NFR-CAD-009 | Resilience | Backlog storm após queda ≤ `catchup_window` (6h) não floda; fan-out bounded | `MAX_PER_RUN=50` / `CONCURRENCY=6` | Load smoke (FM-CAD-07) |
> 168	| NFR-CAD-010 | Compliance (estrutural) | Guardrails G1–G14 impostos por **construção** (FK/UNIQUE/fail-closed/server-side), nunca via LLM | 14/14 | `/security-review` + smoke IoC (G13) |
> 169	| NFR-CAD-011 | Compliance (LGPD) | `erase_lead()` cancela agendamentos futuros na mesma transação | 100% atômico | AT-CAD-017 |
> 170	| NFR-CAD-012 | Infra (contenção) | Drain via `FOR UPDATE SKIP LOCKED`; **nenhum** job pg_cron novo | +0 jobs cron | `count(*) FROM cron.job` invariante |
> 171	| NFR-CAD-013 | Performance | Edge `cadence-run` p95 por tick (fan-out bounded) | < 5s por batch de 50 | Supabase logs |
> 172	| NFR-CAD-014 | UX | Inspector poll sobrevive a refresh (molde `useVoiceRenderPoll`); nunca `sleep(8s)×25` | 100% | Vision QA + code review |
> 173	| NFR-CAD-015 | Observabilidade | Toda falha → `infra_health_logs` (`service='spaces-cadence'`) + nó de observação na Knowledge Mesh por ciclo | 100% dos paths de erro | Query de telemetria |
> 174	
> 175	---
> 176	
> 177	## 4. Interface Requirements
> 178	
> 179	### 4.1 UI → Hook → Edge → DB Contract
> 180	
> 181	```
> 182	[Component: CadenceNode + CadenceInspector (RightPanel)]
> 183	  ↓ arma o plano / faz poll (molde useVoiceRenderPoll)
> 184	[Hook: useCanvasStudio → cadence-plan invoke]
> 185	  ↓ upsert plano + arm next_run_at UTC
> 186	[Edge Function: cadence-plan]  (verify_jwt=false → ES256 JWKS)
> 187	  ↓ escreve
> 188	[Table: autopilot_plans (plan_kind='cadence')]
> 189	
> 190	[Cron: pg_cron */15 → autopilot-cadence-cron]  (gate Bearer SB_SECRET_KEY → 403)
> 191	  ↓ roteia por plan_kind
> 192	[Edge Function: cadence-run]  (drain FOR UPDATE SKIP LOCKED)
> 193	  ↓ gate chain server-side → dispatch
> 194	[Table: scheduled_posts (metadata.reshape + schedule:true + publish_at)]  ← SINK one-shot
> 195	  ↓ ledger + re-arm
> 196	[Table: cadence_dispatches (idempotency índice parcial)]
> 197	  ↓ auto-publish (pg_cron + SKIP LOCKED) DRENA e publica
> 198	[reconcile webhook de status] → external_usd_cost + cost_source → collective_efficiency_ledger
> 199	```
> 200	
> 201	### 4.2 External API Contracts
> 202	
> 203	#### `POST /functions/v1/cadence-plan`
> 204	**Auth:** Bearer JWT (user scope) → **ES256 JWKS verify** (nunca `atob`). `user_id` server-trusted.
> 205	**Request:**
> 206	```typescript
> 207	{
> 208	  sourceAssetId: string,           // creative_assets.id (owner-scoped)
> 209	  recurrence: {                    // computado em UTC no servidor
> 210	    frequency: 'daily'|'weekly'|'monthly',
> 211	    days: number[],                // weekdays (1=Mon) ou dias do mês
> 212	    hours: number, minutes: number,// múltiplos de 5 (Knock)
> 213	    tz: string                     // IANA; cascata → profiles.timezone → America/Sao_Paulo
> 214	  },
> 215	  quiet_hours?: { start: string, end: string, days: number[] },
> 216	  channel_allowlist: string[],     // por plano (auto-publish MENOS X na Fatia 1)
> 217	  budget_cap_mco: number,          // NOT NULL, em mcoCoins
> 218	  overlap_policy?: 'skip',
> 219	  catchup_window?: string,         // interval, default '6 hours'
> 220	  jitter_seconds?: number,
> 221	  program?: CadenceStep[]          // molde sequences.steps + current_step
> 222	}
> 223	```
> 224	**Response (200):**
> 225	```typescript
> 226	{ plan_id: string, next_run_at: string /* ISO UTC */, projected_cost_mco: number }
> 227	```
> 228	**Error codes:**
> 229	| Code | Condition |
> 230	|------|-----------|
> 231	| 401 | JWT ausente/inválido (falha ES256) |
> 232	| 402 | `<provider>_not_configured` (BYOK fail-closed) — body `{ error, action }` |
> 233	| 403 | Cron sem `Bearer SB_SECRET_KEY` |
> 234	| 422 | Validação (ex.: `budget_cap_mco` ausente; `recurrence` inválida) — campo + msg pt-BR no body |
> 235	| 500 | Erro interno (logado em `infra_health_logs`) |
> 236	
> 237	#### `POST /functions/v1/cadence-run` (invocada pelo tick, não pela UI)
> 238	**Auth:** `Authorization === Bearer SB_SECRET_KEY` (senão **403**). `user_id` **server-trusted da linha** (nunca do body).
> 239	**Behavior:** drain `SKIP LOCKED` → resolve subject owner-scoped → gate chain → dispatch a `scheduled_posts` → `INSERT cadence_dispatches ON CONFLICT DO NOTHING RETURNING` → re-arm `next_run_at` | deactivate. Reconciliação `sent` só do webhook de status.
> 240	
> 241	---
> 242	
> 243	## 5. Data Requirements
> 244	
> 245	> Entidades: **NOVA** `cadence_dispatches`; **NOVA** `social_threads`/`social_messages` (Fatia 2); **REUSA-ESTENDE** `autopilot_plans`; **REUSA** `scheduled_posts` (sink), `lead_events`/`leads`/`marketing_consents`, `sequences`/`sequence_enrollments` (molde), `profiles.timezone` + `channel_profiles.cadence` (ressuscitados), RPCs `begin`/`finalize`.
> 246	
> 247	| Field (tabela) | Type | Nullable | Validation Rule | Error Message (PT-BR) |
> 248	|----------------|------|----------|-----------------|----------------------|
> 249	| `autopilot_plans.plan_kind` | text | No | `IN ('viral','cadence')` DEFAULT `'viral'` | "Tipo de plano inválido." |
> 250	| `autopilot_plans.recurrence` | jsonb | Yes (No p/ cadence) | `{frequency,days,hours,minutes,tz}`; `minutes % 5 = 0` | "Recorrência inválida (minutos devem ser múltiplos de 5)." |
> 251	| `autopilot_plans.budget_cap_mco` | int | **No** | `> 0`, em mcoCoins | "Defina o teto de custo por ciclo (em mcoCoins)." |
> 252	| `autopilot_plans.channel_allowlist` | text[] | Yes | ⊆ allowlist de `auto-publish`; **X fora** na Fatia 1 | "Canal não permitido nesta fatia." |
> 253	| `autopilot_plans.overlap_policy` | text | Yes | DEFAULT `'skip'` | — |
> 254	| `autopilot_plans.catchup_window` | interval | Yes | DEFAULT `'6 hours'` | — |
> 255	| `cadence_dispatches.idempotency_key` | text | No | UNIQUE **parcial** `WHERE status<>'failed'` | (interno — `ON CONFLICT DO NOTHING`) |
> 256	| `cadence_dispatches.status` | text | No | transiciona; `sent` só via webhook de status | — |
> 257	| `cadence_dispatches.external_usd_cost` | numeric | Yes | gravado **no reconcile**, nunca no 202 | — |
> 258	| `cadence_dispatches.cost_source` | text | Yes | fonte do custo externo BYOK | — |
> 259	| `social_threads.csw_expires_at` (Fatia 2) | timestamptz | No | derivado do inbound **no servidor** (24h) | — |
> 260	| `social_threads.private_reply_deadline` (Fatia 2) | timestamptz | No | 7d por comentário; `UNIQUE(comment_id)` na fila | — |
> 261	| (fila DM, Fatia 2) `inbound_event_id` | uuid | **No (FK NOT NULL)** | FK → `lead_events(message_received)` do mesmo `user_id` | (cold DM impossível de representar — G1) |
> 262	| `marketing_consents.basis` (WhatsApp/UE) | text | No | gate de enqueue fail-closed; `consent` no Brasil (OTD-CAD-015) | "Consentimento ausente para este canal." / `whatsapp_opt_in_missing` |
> 263	
> 264	**RLS:** `cadence_dispatches` = `select_own` + `insert`/`update` **service-role** (cliente nunca escreve). `autopilot_plans` = RLS owner-scoped preservada. Default-deny em todas.
> 265	
> 266	---
> 267	
> 268	## 6. Test Strategy Matrix
> 269	
> 270	| FR ID | Unit | Integration | E2E | Smoke re-executável (Lei 1) |
> 271	|-------|------|-------------|-----|------------------------------|
> 272	| FR-CAD-015 | ✅ (timingSafeEqual) | ✅ (webhook não-401 + sink) | — | `curl` status + `SELECT lead_events` |
> 273	| FR-CAD-016 | ✅ (runAllCost ≠ NaN) | — | — | teste do switch |
> 274	| FR-CAD-017 | ✅ | ✅ (cascata atômica) | — | `count(*)` pós-`erase_lead` = 0 |
> 275	| FR-CAD-018 | — | ✅ (SKIP LOCKED) | — | `cron.job` + concorrência sem double-publish |
> 276	| FR-CAD-001 | ✅ (registry/cost) | — | ✅ (nó no canvas) | grafo persistido `"kind":"cadence"` |
> 277	| FR-CAD-002 | — | ✅ (migration) | — | `\d autopilot_plans` + `/security-review` |
> 278	| FR-CAD-003 | — | ✅ (índice parcial + RLS) | — | `pg_indexes` predicado + RLS deny |
> 279	| FR-CAD-004 | ✅ (roteamento) | ✅ (tick) | — | `count(*) FROM cron.job` invariante + 403 |
> 280	| FR-CAD-005 | ✅ | ✅ (arm UTC) | ✅ (inspector poll) | `plan_id` UUID + 0 mco débito |
> 281	| FR-CAD-006 | ✅ (gate chain) | ✅ (drain+dispatch) | ✅ | 0 double-post + sent só do webhook |
> 282	| FR-CAD-007 | ✅ (calculador UTC) | — | — | `next_run_at` UTC vs. fuso |
> 283	| FR-CAD-008 | ✅ (quiet/cap) | ✅ (HALT) | — | 0 publicação em quiet-hours; leitor de `channel_profiles.cadence` |
> 284	| FR-CAD-009 | ✅ (digestKey) | ✅ | — | N vencimentos → 1 publicação |
> 285	| FR-CAD-010 | ✅ (fórmula A/B) | — | — | distribuição ~ratio + estabilidade |
> 286	| FR-CAD-011 | ✅ (projeção mco) | ✅ (external_usd_cost) | ✅ (Vision QA do inspector) | 422 sem `budget_cap_mco` |
> 287	| FR-CAD-014 | ✅ (fail-closed) | ✅ (Telegram/Resend) | — | 402 `telegram_not_configured`; rodapé server-side |
> 288	| FR-CAD-012 `[PROBE-GATED]` | — | ✅ (após probe) | — | **probe:** DM real terceiro sem role no banco + payload cru |
> 289	| FR-CAD-013 `[PROBE-GATED]` | ✅ (janela/UNIQUE) | ✅ (após probe) | — | FK viola sem inbound; `UNIQUE(comment_id)` |
> 290	
> 291	**Test files location (proposto — a SDD sela os paths):**
> 292	- Unit: `src/hooks/__tests__/useCadence*.test.ts`, `src/test/cadence-*.test.ts`
> 293	- Smokes (Lei 1, re-executáveis, zero-custo): `scripts/qa/smoke-cadence-idempotency.ts`, `scripts/qa/smoke-cadence-run.ts`, `scripts/qa/smoke-cadence-arm-utc.ts`, `scripts/qa/smoke-cadence-fail-closed.ts`
> 294	- E2E: `e2e/spaces-cadence.spec.ts` (nó no canvas + inspector poll)
> 295	
> 296	---
> 297	
> 298	## 7. Traceability Matrix
> 299	
> 300	| PR ID | FR ID | NFR ID | BR ID | OTD / FM |
> 301	|-------|-------|--------|-------|----------|
> 302	| PR-CAD-012 (Fatia 0) | FR-CAD-015, FR-CAD-016, FR-CAD-017, FR-CAD-018 | NFR-CAD-001, NFR-CAD-004, NFR-CAD-011, NFR-CAD-012 | BR-CAD-017 | OTD-CAD-001/004/006/007 · FM-CAD-01/04/09/16 |
> 303	| PR-CAD-001 | FR-CAD-001 | NFR-CAD-007, NFR-CAD-014 | BR-CAD-001 | OTD-CAD-002/007 |
> 304	| PR-CAD-003 | FR-CAD-002, FR-CAD-004 | NFR-CAD-006, NFR-CAD-012 | BR-CAD-002, BR-CAD-004 | OTD-CAD-003 · FM-CAD-06 |
> 305	| PR-CAD-004 | FR-CAD-003 | NFR-CAD-001, NFR-CAD-006 | BR-CAD-003 | OTD-CAD-006 · FM-CAD-01 |
> 306	| PR-CAD-002 | FR-CAD-005 | NFR-CAD-004, NFR-CAD-014 | BR-CAD-004 | — |
> 307	| PR-CAD-005 | FR-CAD-006 | NFR-CAD-002, NFR-CAD-009, NFR-CAD-013 | BR-CAD-009, BR-CAD-011, BR-CAD-013 | OTD-CAD-004/005 · FM-CAD-01/05/07 |
> 308	| PR-CAD-006 | FR-CAD-007 | NFR-CAD-003 | BR-CAD-005 | FM-CAD-06 |
> 309	| PR-CAD-007 | FR-CAD-008 | NFR-CAD-009, NFR-CAD-010 | BR-CAD-006 | OTD-CAD-008/017 · G3/G4 |
> 310	| PR-CAD-008 | FR-CAD-009 | NFR-CAD-010 | BR-CAD-007 | — |
> 311	| PR-CAD-009 | FR-CAD-010 | NFR-CAD-002 | BR-CAD-008 | OTD-CAD-016 |
> 312	| PR-CAD-010 | FR-CAD-011 | NFR-CAD-007, NFR-CAD-008 | BR-CAD-010, BR-CAD-012 | OTD-CAD-011 |
> 313	| PR-CAD-020, PR-CAD-021 | FR-CAD-014 | NFR-CAD-005, NFR-CAD-010 | BR-CAD-016, BR-CAD-013 | OTD-CAD-009 · FM-CAD-12 · G10/G12 |
> 314	| PR-CAD-030 | FR-CAD-012, FR-CAD-013 `[PROBE-GATED]` | NFR-CAD-010, NFR-CAD-015 | BR-CAD-015 | FM-CAD-02 (RPN 486), FM-CAD-03/13 · OTD-CAD-018 · G1/G2/G5/G6 |
> 315	
> 316	> **Decisões abertas a selar na SDD/`09-pattern-conformance`:** (1) sujeito = asset existente (OTD-CAD-002, PRD assume); (2) estender `autopilot_plans` (OTD-CAD-003, default); (3) `channel_profiles.cadence` autoritativo (OTD-CAD-008); (4) frequency-cap por `(user,channel)` vs `(user,channel,conta)` (OTD-CAD-017); (5) `cadence_dispatches` retry-via-índice-parcial vs. append-only at-most-once (OTD-CAD-006); (6) IG/Messenger no app global com caps por-app (OTD-CAD-018); (7) jurisdição default UE fail-closed (G11). **FR-CAD-012/013 permanecem `[PROBE-GATED]` — não codar antes do probe FM-CAD-02.**
> 317	
> 318	---
> 319	
> 320	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` + `01-mrd.md` + `02-brd.md` + `03-prd.md` (Lei 1: nenhum FR/NFR/OTD/FM/entidade inventado além do blueprint; FR-CAD-012/013 sob `[PROBE-GATED]`; §3 sob selo de não-verificação). Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança via RPC atômica begin/finalize (nunca client-side); verify_jwt=false → ES256 JWKS / HMAC timingSafeEqual (nunca `atob` cego); RLS default-deny owner-scoped. A Cadência ENCAIXA nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), não reconstrói distribuição — nenhum job pg_cron novo._
> 321	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Data & Knowledge Model
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14) + [`01-mrd.md`](01-mrd.md) → [`05-sdd.md`](05-sdd.md). Cada objeto de dado abaixo materializa um `FR-CAD-xxx` da FRD §2 e um objeto de design da SDD §2.5/§7. Nada é inventado além do blueprint (Lei 1); onde o blueprint deixou decisão aberta (§11), a SDD §8 já a selou e este doc reflete a decisão selada.
> 8	
> 9	> **ORO triplet desta task:**
> 10	> - **Operator:** MCORCH Master Execution Agent
> 11	> - **Reviewer:** Sovereign (Gabriel)
> 12	> - **Owner:** Sovereign — blast radius: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 13	
> 14	> **Mandato de integração (o dogma deste modelo de dados):** a Cadência **encaixa nos trilhos VIVOS** — `autopilot_plans`, `scheduled_posts`, `lead_events`, `sequences`, `channel_profiles.cadence`, `profiles.timezone` — e **NÃO reconstrói distribuição**. **Zero tabela de plano paralela · zero job pg_cron novo.** Toda linha da tabela abaixo carrega um selo:
> 15	> - 🟢 **REUSA** — trilho vivo consumido sem migration (ou com ganho de "primeiro leitor" de dado morto).
> 16	> - 🟡 **REUSA-ESTENDE** — trilho vivo alterado por `ALTER TABLE`/`CREATE OR REPLACE FUNCTION` (não recriado).
> 17	> - 🔴 **NOVO** — não existe equivalente no repo; nasce nesta suíte.
> 18	> - 🔒 **NOVO `[PROBE-GATED]`** — congelado até o probe FM-CAD-02 (RPN 486) fechar com DM real de terceiro sem role + payload cru arquivado.
> 19	
> 20	> **Nota de fidelidade (Lei 1):** `social_threads`/`social_messages` (Fatia 2) permanecem `[PROBE-GATED]` — especificados aqui como blueprint congelado, **não** DDL a aplicar. §3 do blueprint (posicionamento vs. ManyChat) está sob **SELO DE NÃO-VERIFICAÇÃO**: nenhuma regra de dados abaixo o cita como fato.
> 21	
> 22	---
> 23	
> 24	## 1. Conceptual Data Model
> 25	
> 26	```
> 27	                 🟢 profiles.timezone (SSOT de fuso — 1º leitor)
> 28	                          │  cascata recurrence.tz → profiles.timezone → 'America/Sao_Paulo'
> 29	                          ▼
> 30	 [🟡 autopilot_plans] ──(1:N)──▶ [🔴 cadence_dispatches] ──(1:1 target_ref)──▶ [🟢 scheduled_posts]
> 31	   plan_kind='cadence'          idempotency_key (índice único parcial)          (SINK one-shot; auto-publish drena)
> 32	   recurrence/quiet_hours/          │
> 33	   program/channel_allowlist        │ external_usd_cost + cost_source (no reconcile)
> 34	   budget_cap_mco                    ▼
> 35	        │                     [🟢 collective_efficiency_ledger] (mco/resultado do CICLO)
> 36	        │  frequency-cap teto
> 37	        ▼
> 38	 [🟢 channel_profiles.cadence] (goal declarativo por canal — 1º leitor)
> 39	
> 40	 [🟢 lead_events(message_received)] ──(FK NOT NULL inbound)──▶ [🔒 social_threads] ──(1:N)──▶ [🔒 social_messages]
> 41	   (imutável append-only)                cold DM impossível (G1)     csw_expires_at(24h) / private_reply_deadline(7d)
> 42	        │
> 43	        └──(1:1 por ciclo)──▶ [🟢 mcorch_nodes] (observação; revenue_impact ← ledger)
> 44	```
> 45	
> 46	**Entities (selo · papel):**
> 47	
> 48	- 🟡 **`autopilot_plans`** — REUSA-ESTENDE. Única tabela de plano recorrente com kill-switch (`is_active`) e caps obrigatórios; absorve a cadência como `plan_kind='cadence'` (não uma tabela nova — OTD-CAD-003).
> 49	- 🔴 **`cadence_dispatches`** — NOVO. Ledger por tentativa de dispatch; a idempotência (índice único parcial) é o que **impede** FM-CAD-01/03, não uma promessa.
> 50	- 🟢 **`scheduled_posts`** — REUSA como **sink one-shot** (contrato `metadata.reshape` + `schedule:true` + `publish_at` ISO — Amendment 22); `auto-publish` drena. Não é fonte de recorrência.
> 51	- 🟢 **`lead_events`** — REUSA sem migration (`event_type='message_received'` entra hoje; imutável, append-only, FK composta tenant-escopada).
> 52	- 🟢 **`channel_profiles.cadence`** — REUSA (ressuscita dado morto): vira o **teto autoritativo** do frequency-cap (1º leitor do repo — OTD-CAD-008).
> 53	- 🟢 **`profiles.timezone`** — REUSA (ressuscita dado morto): SSOT de fuso do sujeito da cadência (1º leitor — FR-CAD-007).
> 54	- 🔒 **`social_threads` / `social_messages`** — NOVO `[PROBE-GATED]`. A Meta só devolve as **20 últimas** mensagens ⇒ a memória de conversa **tem** que morar aqui (Fatia 2, após probe).
> 55	- 🟢 **`mcorch_nodes` / `collective_efficiency_ledger` / `infra_health_logs`** — REUSA (Mesh Connection Mandate + custo medido mesmo com mco=0).
> 56	
> 57	---
> 58	
> 59	## 2. Logical Data Model
> 60	
> 61	### 2.1 🟡 `autopilot_plans` (REUSA-ESTENDE — FR-CAD-002 / OTD-CAD-003)
> 62	
> 63	Migration única `ADD COLUMN` × 9 + `DROP CONSTRAINT` × 1. **RLS owner-scoped já existente é PRESERVADA** (nenhuma policy recriada). Colunas legadas (`mode`, `interval_days`, `daily_cap`, `is_active`, `next_run_at`, índice parcial due) permanecem intactas — `plan_kind='viral'` continua válido.
> 64	
> 65	| Column | Type | Nullable | Default | Selo | Description |
> 66	|--------|------|----------|---------|------|-------------|
> 67	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | 🟢 legado | Primary key |
> 68	| `user_id` | `uuid` | NOT NULL | — | 🟢 legado | Tenant isolation (FK `auth.users.id`); RLS `= auth.uid()` |
> 69	| `is_active` | `boolean` | NOT NULL | `true` | 🟢 legado | **Kill-switch** (reusado como kill por plano; FM-CAD-14) |
> 70	| `next_run_at` | `timestamptz` | NULL | — | 🟢 legado | Próxima execução em **UTC** (FM-CAD-06); alimenta o índice parcial due |
> 71	| `daily_cap` | `int` | NOT NULL | — | 🟢 legado | Cap diário (clone reusado — G4) |
> 72	| `platforms` (CHECK) | `text[]` | — | — | 🟡 **DROP CHECK** | `platforms <@ ARRAY['wordpress','linkedin','twitter']` **removido**; allowlist passa a derivar de `channel_profiles`/`channel_allowlist` |
> 73	| `plan_kind` | `text` | NOT NULL | `'viral'` | 🔴 nova | `CHECK (plan_kind IN ('viral','cadence'))` — o tick roteia por esta coluna (FR-CAD-004) |
> 74	| `recurrence` | `jsonb` | NULL | — | 🔴 nova | `{frequency:'daily'\|'weekly'\|'monthly', days:int[], hours:int, minutes:int (múltiplo de 5), tz:IANA}` — computado em UTC (FR-CAD-007) |
> 75	| `quiet_hours` | `jsonb` | NULL | — | 🔴 nova | `{start, end, days:int[]}` no fuso do sujeito (FR-CAD-008 · G3) |
> 76	| `overlap_policy` | `text` | NULL | `'skip'` | 🔴 nova | Ciclo anterior rodando ⇒ pula, não empilha (FM-CAD-01) |
> 77	| `catchup_window` | `interval` | NULL | `'6 hours'` | 🔴 nova | Limita backlog após queda (FM-CAD-07) |
> 78	| `jitter_seconds` | `int` | NULL | `0` | 🔴 nova | Anti-thundering-herd no fan-out (FM-CAD-07) |
> 79	| `program` | `jsonb` | NULL | — | 🔴 nova | Steps `publish\|wait\|throttle\|digest\|branch` — **molde `sequences.steps` + `current_step`** (não formato novo — P1/P6) |
> 80	| `channel_allowlist` | `text[]` | NULL | — | 🔴 nova | Canais **por plano** (⊆ allowlist do `auto-publish` **MENOS X** na Fatia 1 — OTD-CAD-011); não constante hardcoded |
> 81	| `budget_cap_mco` | `int` | NOT NULL | `0` | 🔴 nova | Cap **em mcoCoins** (nunca USD); `cadence` exige `> 0` no edge (422) — obrigação compensatória do quote=0 (FR-CAD-011) |
> 82	
> 83	### 2.2 🔴 `cadence_dispatches` (NOVO — FR-CAD-003 / FM-CAD-01)
> 84	
> 85	Ledger por tentativa. **Não é append-only puro** (decisão selada OTD-CAD-006 = retry via índice parcial): `status` transiciona ⇒ exige `UPDATE` service-role. FK composta tenant-escopada para `autopilot_plans`; RLS `select_own`, escrita **service-role only**.
> 86	
> 87	| Column | Type | Nullable | Default | FK | Description |
> 88	|--------|------|----------|---------|-----|-------------|
> 89	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | Primary key |
> 90	| `user_id` | `uuid` | NOT NULL | — | `auth.users.id` | Tenant isolation; RLS `= auth.uid()` (só SELECT) |
> 91	| `plan_id` | `uuid` | NOT NULL | — | `autopilot_plans.id` (composta `(plan_id,user_id)` — ver §3) | Plano de origem |
> 92	| `step_index` | `int` | NOT NULL | — | — | Passo do `program` (chave de idempotência) |
> 93	| `occurrence_at` | `timestamptz` | NOT NULL | — | — | Instante vencido (chave de idempotência) |
> 94	| `idempotency_key` | `text` | NOT NULL | — | — | Hash estável de `(plan_id, step_index, occurrence_at)`; sob **índice único parcial** |
> 95	| `channel` | `text` | NOT NULL | — | — | Canal de dispatch (∈ `channel_allowlist` do plano) |
> 96	| `status` | `text` | NOT NULL | `'queued'` | — | `queued\|publishing\|sent\|failed` (**transiciona** — não append-only) |
> 97	| `target_ref` | `text` | NULL | — | — | `scheduled_posts.id` ou id externo (1:1 lógico com o sink) |
> 98	| `error` | `text` | NULL | — | — | Motivo da falha (`'erased'` no cascade LGPD) |
> 99	| `external_usd_cost` | `numeric` | NULL | — | — | Custo externo BYOK, gravado **no reconcile** (webhook de status), **nunca no 202** (FM-CAD-05 · NFR-CAD-008) |
> 100	| `cost_source` | `text` | NULL | — | — | Fonte do custo (`'meta_ai_provider_br'`, `'x_post_url'`, …) |
> 101	| `created_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 102	| `updated_at` | `timestamptz` | NOT NULL | `now()` | — | Audit (transição de status) |
> 103	
> 104	### 2.3 🔒 `social_threads` / `social_messages` (NOVO `[PROBE-GATED]` — FR-CAD-012 · Fatia 2)
> 105	
> 106	> ⚠️ **Congelado.** Só ganha DDL depois que o probe FM-CAD-02 fechar (DM real de terceiro sem role no banco + payload cru de `entry.messaging` fixando o shape — FM-CAD-13). Especificado aqui para rastreabilidade, **não** para aplicar.
> 107	
> 108	| Table | Column | Type | Nullable | Description |
> 109	|-------|--------|------|----------|-------------|
> 110	| `social_threads` | `id` / `user_id` | `uuid` | NOT NULL | PK + tenant isolation (RLS `select_own`, escrita service-role) |
> 111	| `social_threads` | `external_thread_id` | `text` | NOT NULL | Id da conversa na plataforma |
> 112	| `social_threads` | `inbound_event_id` | `uuid` | **NOT NULL** | FK → `lead_events` (`message_received` do **mesmo `user_id`**) ⇒ **cold DM impossível de representar** (G1/FM-CAD-03) |
> 113	| `social_threads` | `csw_expires_at` | `timestamptz` | NULL | Janela CSW 24h, derivada do inbound **no servidor** (relógio 1) |
> 114	| `social_threads` | `comment_id` | `text` | NULL | **`UNIQUE`** — "only one message can be sent to the commenter" (G2); política, não UX |
> 115	| `social_threads` | `private_reply_deadline` | `timestamptz` | NULL | Deadline 7d do private reply (relógio 2 — distinto do CSW) |
> 116	| `social_messages` | `id` / `thread_id` | `uuid` | NOT NULL | PK + FK → `social_threads.id` |
> 117	| `social_messages` | `direction` / `body` / `created_at` | — | — | Histórico local (a Meta só devolve as **20 últimas** — P8) |
> 118	
> 119	### 2.4 🟢 Reusadas sem migration (contrato de leitura)
> 120	
> 121	| Objeto | Contrato consumido | FR / Selo |
> 122	|--------|--------------------|-----------|
> 123	| `scheduled_posts` | Sink one-shot: INSERT com `metadata.reshape` + `schedule:true` + `publish_at` ISO; 422 data inválida / 409 anti double-enqueue (Amendment 22) | FR-CAD-006 · 🟢 |
> 124	| `lead_events` | INSERT `event_type='message_received'` (sem CHECK; FK composta `(id,user_id)`; RLS imutável) | FR-CAD-012 · 🟢 |
> 125	| `leads` / `marketing_consents` | Gate de enqueue: `basis` fail-closed; `granted_at`+`source_proof` p/ WhatsApp (senão 422 `whatsapp_opt_in_missing`) | FR-CAD-015 · G7/G8 · 🟢 |
> 126	| `channel_profiles.cadence` | `{target_per, count_min, count_max}` = teto do frequency-cap (goal declarativo) | FR-CAD-008 · 🟢 (1º leitor) |
> 127	| `profiles.timezone` | Cascata de fuso `recurrence.tz → profiles.timezone → 'America/Sao_Paulo'` | FR-CAD-007 · 🟢 (1º leitor) |
> 128	| `creative_assets` | Subject da cadência (`id` owner-scoped) = asset existente ⇒ **0 mco, keyless** | FR-CAD-005 · OTD-CAD-002 · 🟢 |
> 129	| `collective_efficiency_ledger` | Recebe `external_usd_cost`/`cost_source` do reconcile ⇒ mco/resultado do ciclo | NFR-CAD-008 · 🟢 |
> 130	
> 131	---
> 132	
> 133	## 3. Supabase Physical Schema Stubs
> 134	
> 135	> **Toda migration passa por `/security-review` antes do commit (NO EXCEPTIONS — FMEA-011).** Timestamps propostos (a implementação sela os finais). Reproduzem a SDD §7.
> 136	
> 137	### 3.1 🟡 `20260716120000_cadence_extend_autopilot_plans.sql` (FR-CAD-002)
> 138	
> 139	```sql
> 140	-- ESTENDER o trilho vivo — NÃO criar tabela paralela nem 3º driver (OTD-CAD-003).
> 141	ALTER TABLE public.autopilot_plans
> 142	  DROP CONSTRAINT IF EXISTS autopilot_plans_platforms_check,   -- allowlist deriva de channel_profiles
> 143	  ADD COLUMN plan_kind text NOT NULL DEFAULT 'viral'
> 144	      CHECK (plan_kind IN ('viral','cadence')),
> 145	  ADD COLUMN recurrence        jsonb,      -- {frequency, days, hours, minutes, tz}
> 146	  ADD COLUMN quiet_hours       jsonb,      -- {start, end, days}
> 147	  ADD COLUMN overlap_policy    text DEFAULT 'skip',
> 148	  ADD COLUMN catchup_window    interval DEFAULT '6 hours',
> 149	  ADD COLUMN jitter_seconds    int DEFAULT 0,
> 150	  ADD COLUMN program           jsonb,      -- steps; molde sequences.steps + current_step
> 151	  ADD COLUMN channel_allowlist text[],     -- por PLANO — X fora na Fatia 1 (OTD-CAD-011)
> 152	  ADD COLUMN budget_cap_mco    int NOT NULL DEFAULT 0;  -- mcoCoins; cadence exige > 0 no edge (422)
> 153	-- RLS owner-scoped já existente é PRESERVADA. Planos plan_kind='viral' permanecem válidos.
> 154	```
> 155	
> 156	### 3.2 🔴 `20260716120100_cadence_dispatches.sql` (FR-CAD-003 / FM-CAD-01)
> 157	
> 158	```sql
> 159	CREATE TABLE public.cadence_dispatches (
> 160	  id                uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 161	  user_id           uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 162	  plan_id           uuid NOT NULL,
> 163	  step_index        int  NOT NULL,
> 164	  occurrence_at     timestamptz NOT NULL,
> 165	  idempotency_key   text NOT NULL,          -- hash estável de (plan_id, step_index, occurrence_at)
> 166	  channel           text NOT NULL,
> 167	  status            text NOT NULL DEFAULT 'queued',   -- queued|publishing|sent|failed (TRANSICIONA)
> 168	  target_ref        text,                   -- scheduled_posts.id / external id
> 169	  error             text,
> 170	  external_usd_cost numeric,                -- gravado NO RECONCILE, nunca no 202 (FM-CAD-05)
> 171	  cost_source       text,
> 172	  created_at        timestamptz NOT NULL DEFAULT now(),
> 173	  updated_at        timestamptz NOT NULL DEFAULT now(),
> 174	  -- FK COMPOSTA TENANT-ESCOPADA (impede referência cross-tenant a plano de outro dono):
> 175	  CONSTRAINT cadence_dispatches_plan_fk
> 176	    FOREIGN KEY (plan_id, user_id)
> 177	    REFERENCES public.autopilot_plans (id, user_id) ON DELETE CASCADE
> 178	  -- Requer UNIQUE(id,user_id) em autopilot_plans (mesmo padrão de creative_metrics/campaign_steps).
> 179	);
> 180	
> 181	-- Índice de idempotência — é ELE que impede FM-CAD-01/03 (falha LIBERA / sucesso PRENDE):
> 182	CREATE UNIQUE INDEX cadence_dispatches_idem
> 183	  ON public.cadence_dispatches (idempotency_key)
> 184	  WHERE status <> 'failed';
> 185	
> 186	-- Índice de drain due (por plano):
> 187	CREATE INDEX cadence_dispatches_plan_status_idx
> 188	  ON public.cadence_dispatches (plan_id, status);
> 189	
> 190	ALTER TABLE public.cadence_dispatches ENABLE ROW LEVEL SECURITY;   -- default-deny
> 191	
> 192	-- Cliente LÊ o próprio; NUNCA escreve (status/custo só service-role no reconcile):
> 193	CREATE POLICY "cadence_dispatches: users read own rows"
> 194	  ON public.cadence_dispatches FOR SELECT
> 195	  USING (user_id = auth.uid());
> 196	-- SEM policy de INSERT/UPDATE para authenticated ⇒ negado por default-deny.
> 197	-- service_role bypassa RLS e escreve status/error/external_usd_cost.
> 198	
> 199	CREATE TRIGGER set_cadence_dispatches_updated_at
> 200	  BEFORE UPDATE ON public.cadence_dispatches
> 201	  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
> 202	```
> 203	
> 204	### 3.3 🟡 `20260716120200_erase_lead_cascade_cadence.sql` (FR-CAD-017 / G9 / OTD-CAD-006)
> 205	
> 206	```sql
> 207	-- Estender erase_lead() p/ cancelar agendamentos futuros NA MESMA TRANSAÇÃO (LGPD Art. 16/18 VI).
> 208	-- SECURITY DEFINER, search_path='', tenant-guarded — mantém o padrão existente.
> 209	CREATE OR REPLACE FUNCTION public.erase_lead(p_lead uuid)
> 210	RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
> 211	BEGIN
> 212	  -- ... (bloco existente de anonimização/eliminação do lead) ...
> 213	  UPDATE public.scheduled_posts SET status = 'cancelled'
> 214	    WHERE lead_id = p_lead AND status = 'pending';
> 215	  UPDATE public.cadence_dispatches SET status = 'failed', error = 'erased'
> 216	    WHERE status IN ('queued','publishing')
> 217	      AND user_id = (SELECT user_id FROM public.leads WHERE id = p_lead);
> 218	  -- Atomicidade: rollback se qualquer passo falhar. Sem isso o direito de eliminação é ficção.
> 219	END $$;
> 220	```
> 221	
> 222	### 3.4 🟡 `20260716120300_auto_publish_pgcron_skiplocked.sql` (FR-CAD-018 / OTD-CAD-004)
> 223	
> 224	```sql
> 225	-- Migrar auto-publish de crontab de SO → pg_cron; drain com FOR UPDATE SKIP LOCKED.
> 226	-- Pré-requisito declarado ("antes de ligar recorrência") — Fatia 0 item 5, não pergunta.
> 227	SELECT cron.schedule('auto-publish', '*/5 * * * *', $$ /* invoke auto-publish edge */ $$);
> 228	-- Claim query no edge:
> 229	--   SELECT ... FROM scheduled_posts WHERE status='pending' AND scheduled_at <= now()
> 230	--     FOR UPDATE SKIP LOCKED LIMIT <batch>;
> 231	-- NENHUM job pg_cron NOVO para a cadência: o tick autopilot-cadence-cron já existe e apenas roteia.
> 232	```
> 233	
> 234	### 3.5 🔒 `[PROBE-GATED]` `social_threads`/`social_messages` (FR-CAD-012 — Fatia 2, NÃO codar antes do probe)
> 235	
> 236	```sql
> 237	-- CONGELADO até FM-CAD-02 fechar (DM real de terceiro sem role + payload cru).
> 238	-- social_threads: id, user_id, external_thread_id,
> 239	--   inbound_event_id uuid NOT NULL REFERENCES lead_events (message_received, mesmo user_id) ⇒ cold DM impossível (G1),
> 240	--   csw_expires_at timestamptz (24h, servidor), private_reply_deadline timestamptz (7d),
> 241	--   comment_id text UNIQUE (G2).
> 242	-- RLS select_own + escrita service-role. FK composta tenant-escopada como cadence_dispatches.
> 243	```
> 244	
> 245	---
> 246	
> 247	## 4. GraphRAG Knowledge Nodes
> 248	
> 249	### Node Types Introduced
> 250	
> 251	| node_type | Title Pattern | Content Fields | Embedding Source |
> 252	|-----------|--------------|----------------|-----------------|
> 253	| `observation` (🟢 reuso) | `Cadence cycle · plan <plan_id> · <channel>` | `plan_kind`, canais, `budget_cap_mco`, resultado do 1º ciclo | `embed-mcorch-node` (título + resumo do ciclo) |
> 254	
> 255	> Nenhum `node_type` novo. A Cadência **consome** a Knowledge Mesh (Mesh Connection Mandate) inserindo **um nó de observação por ciclo bem-sucedido** de cada plano — não cria taxonomia nova (P8/P14 n-a de RAG).
> 256	
> 257	### Edge Types Introduced
> 258	
> 259	| Edge relationship | Source node_type | Target node_type | Metadata |
> 260	|-------------------|-----------------|-----------------|----------|
> 261	| `DERIVES_FROM` (🟢 reuso) | `observation` (ciclo) | `creative_asset`/`pillar` a montante | `plan_id`, `channel`, `cycle_at` |
> 262	
> 263	### Embedding Trigger
> 264	
> 265	Toda inserção de nó de observação chama `embed-mcorch-node` (system key `MESH_EMBED_*`, não BYOK per-user — é fluxo de sistema sem `auth.uid()`):
> 266	
> 267	```typescript
> 268	// cadence-run, após o 1º ciclo bem-sucedido do plano:
> 269	await supabase.functions.invoke('embed-mcorch-node', {
> 270	  body: { node_id: observationNode.id, content: `Cadence ${planKind} ${channel} ${summary}` }
> 271	})
> 272	```
> 273	
> 274	### FSRS-6 Parameters
> 275	
> 276	| Field | Initial Value | Decay / Update Rule |
> 277	|-------|--------------|---------------------|
> 278	| `stability_score` | `0.5` | Decai pela fórmula da migration `20260425190000` |
> 279	| `revenue_impact` | Derivado do `collective_efficiency_ledger` do ciclo (mco/resultado) | Atualizado a cada ciclo reconciliado (custo BYOK **medido** mesmo com mco=0 — NFR-CAD-008) |
> 280	
> 281	---
> 282	
> 283	## 5. Tenant Isolation Map
> 284	
> 285	| Table | Selo | `user_id` scope | FK composta tenant-escopada | Escrita do cliente | System rows |
> 286	|-------|------|-----------------|-----------------------------|--------------------|-------------|
> 287	| `autopilot_plans` | 🟡 | ✅ Required (RLS `= auth.uid()` **preservada**) | é o **alvo** de `(id,user_id)` | Via `cadence-plan` (edge, JWT) | Não |
> 288	| `cadence_dispatches` | 🔴 | ✅ Required (RLS `select_own`) | `(plan_id,user_id) → autopilot_plans(id,user_id)` | **NUNCA** (escrita só service-role) | Não |
> 289	| `scheduled_posts` | 🟢 | ✅ Required (RLS existente) | via `lead_id`/owner | Via edge (contrato reshape) | Não |
> 290	| `lead_events` | 🟢 | ✅ Required (imutável: só select_own + insert_own) | `(id,user_id)` existente | Insert-own | Não |
> 291	| `social_threads`/`_messages` | 🔒 | ✅ Required (`select_own`) | `inbound_event_id → lead_events`; composta como acima | **NUNCA** (service-role) | Não |
> 292	| `channel_profiles.cadence` | 🟢 | ✅ Required (existente) | — | Não (só leitura pelo motor) | Não |
> 293	| `profiles.timezone` | 🟢 | ✅ Required (existente) | — | Via Settings (existente) | Não |
> 294	| `mcorch_nodes` | 🟢 | Optional | `user_id + project_id` | Service-role (observação) | ✅ (system `user_id IS NULL`) |
> 295	
> 296	> **Regra de tenancy (SDD §5.1 STRIDE):** `user_id` **jamais** vem do body — na cadência ele é **server-trusted da LINHA** de `autopilot_plans` drenada pelo tick (SOP `autopilot-cron-identity.md`), e no `cadence-plan` vem da **claim ES256 verificada** (nunca `atob` cego). A FK composta `(plan_id,user_id)` impede que um dispatch aponte para um plano de outro tenant mesmo se o `plan_id` for adivinhado.
> 297	
> 298	---
> 299	
> 300	## 6. Data Quality Rules
> 301	
> 302	| Table | Column | Rule | Enforcement | Violation Message (PT-BR) |
> 303	|-------|--------|------|-------------|---------------------------|
> 304	| `autopilot_plans` | `plan_kind` | `IN ('viral','cadence')` | CHECK | — (interno) |
> 305	| `autopilot_plans` | `budget_cap_mco` | NOT NULL; **`> 0` quando `plan_kind='cadence'`** | CHECK/edge 422 | "Defina um teto de orçamento em mcoCoins para a cadência." |
> 306	| `autopilot_plans` | `recurrence.minutes` | Múltiplo de 5 (semântica Knock) | edge 422 | "Os minutos devem ser múltiplos de 5." |
> 307	| `autopilot_plans` | `channel_allowlist` | ⊆ allowlist do `auto-publish` **MENOS X** (Fatia 1) | edge 422 | "Canal não disponível nesta cadência." |
> 308	| `cadence_dispatches` | `idempotency_key` | Único **enquanto `status <> 'failed'`** (falha libera, sucesso prende) | UNIQUE INDEX parcial | — (ON CONFLICT DO NOTHING; anti double-post FM-CAD-01) |
> 309	| `cadence_dispatches` | `status` | `sent` **só** a partir do webhook de status, nunca do 202 | lógica de reconcile | — (Lei 1 / FM-CAD-05) |
> 310	| `cadence_dispatches` | A/B bucket | `mod(abs(hashtext(subject‖':'‖exp)::bigint),100) < ratio` — cast `bigint` **antes** do `abs` | fórmula SQL literal | — (FR-CAD-010; `% 100` com sinal enviesa em silêncio) |
> 311	| `social_threads` | `inbound_event_id` | **NOT NULL** (FK a `lead_events` message_received) | FK NOT NULL | — (cold DM impossível de representar — G1) |
> 312	| `social_threads` | `comment_id` | **UNIQUE** (1 private reply por comentário) | UNIQUE | — (G2; retry duplicado = violação de política) |
> 313	| `marketing_consents` | `basis` | `= 'consent'` fail-closed no Brasil (até Guia ANPD literal) | gate de enqueue | "Consentimento necessário para este canal." (OTD-CAD-015) |
> 314	| `marketing_consents` | `granted_at`+`source_proof` | NOT NULL p/ enqueue WhatsApp | edge 422 | `whatsapp_opt_in_missing` (FM-CAD-15) |
> 315	| (jurisdição G11) | país do lead | Ausente ⇒ tratar como **UE opt-in prévio** (fail-closed) | gate de send | — (custa conversão, é seguro) |
> 316	
> 317	---
> 318	
> 319	## 7. Retention & Archival Policy
> 320	
> 321	| Data | Retention | Archival Strategy | Deletion Trigger |
> 322	|------|-----------|-------------------|------------------|
> 323	| `autopilot_plans` (cadence) | Enquanto ativo | — | `erase_lead()` cascade + cancelamento manual |
> 324	| `cadence_dispatches` | Ledger histórico (auditoria de reconcile/custo) | — | `ON DELETE CASCADE` do plano; `status='failed', error='erased'` no `erase_lead()` (LGPD Art. 16/18 VI — G9) |
> 325	| `scheduled_posts` pendentes | Até publicar/cancelar | drenado por `auto-publish` (pg_cron + SKIP LOCKED) | `status='cancelled'` no `erase_lead()` cascade |
> 326	| `social_threads`/`_messages` `[PROBE-GATED]` | Histórico local (Meta só devolve 20 últimas) | — | Cascade do lead; `erase_lead()` |
> 327	| `lead_events` | Append-only imutável | — | Somente via `erase_lead()` tenant-guarded |
> 328	| `infra_health_logs` (`service='spaces-cadence'`) | 90 dias | Sem archival | Cron purge |
> 329	| `mcorch_nodes` (observação) | Indefinido | Backfill `scripts/backfill-embeddings.ts` | Com a linha pai |
> 330	
> 331	> **Direito de eliminação é estrutural (não best-effort):** `erase_lead()` cancela `scheduled_posts` + `cadence_dispatches` pendentes **na mesma transação** (§3.3). Sem essa cascata o LGPD Art. 16/18 VI vira ficção (G9/OTD-CAD-006) — a revogação chegando **depois** do enqueue ainda impede o send (`withdrawn_at` checado no send, independente da base legal — FM-CAD-04).
> 332	
> 333	---
> 334	
> 335	## 8. Traceability Matrix (Data ↔ FR ↔ OTD ↔ FM)
> 336	
> 337	| Objeto de dado | Selo | FR-CAD | OTD-CAD | FM-CAD | NFR-CAD |
> 338	|----------------|------|--------|---------|--------|---------|
> 339	| `autopilot_plans` (+9 col, −1 CHECK) | 🟡 | 002, 004, 007 | 003 | 06 | 006, 012 |
> 340	| `cadence_dispatches` + índice parcial | 🔴 | 003, 006, 010 | 006 | 01, 03, 05 | 001, 006, 008 |
> 341	| `erase_lead()` cascade | 🟡 | 017 | 006 | 04 | 011 |
> 342	| `auto-publish` pg_cron + SKIP LOCKED | 🟡 | 018 | 004 | 01 | 012 |
> 343	| `scheduled_posts` (sink) | 🟢 | 006 | 005 | 08 | 009 |
> 344	| `lead_events` (message_received) | 🟢 | 012 | — | 02, 13 | 015 |
> 345	| `channel_profiles.cadence` (teto) | 🟢 | 008 | 008, 017 | 07 | — |
> 346	| `profiles.timezone` (SSOT fuso) | 🟢 | 007 | — | 06 | 003 |
> 347	| `social_threads`/`_messages` | 🔒 | 012, 013 | 018 | 02, 03, 13 | 010 |
> 348	| `collective_efficiency_ledger` (custo) | 🟢 | 006, 011 | 009, 011 | 10, 11 | 008 |
> 349	| `marketing_consents` (basis gate) | 🟢 | 015 | 015 | 15 | 010 |
> 350	| `mcorch_nodes` (observação) | 🟢 | 006 | — | — | 015 |
> 351	
> 352	---
> 353	
> 354	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` + `01-mrd.md`…`05-sdd.md` (Lei 1: nenhuma entidade/coluna/FR/OTD/FM inventado além do blueprint; `social_threads`/`social_messages` sob `[PROBE-GATED]`; §3 sob selo de não-verificação). Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança via RPC atômica `begin`/`finalize` (nunca client-side); RLS default-deny owner-scoped; FK composta `(plan_id,user_id)` tenant-escopada. A Cadência ENCAIXA nos trilhos vivos (autopilot · scheduled_posts · lead_events · channel_profiles · profiles) — zero tabela de plano paralela, zero job pg_cron novo. Toda migration passa por `/security-review` antes do commit (FMEA-011)._
> 355	
> ```

## 🤖 Claude *(14:56:32)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking that the functional requirements properly flow through the process documentation and verifying the completeness of the core documents—making sure the FRs are referenced in the process-flow section and that all the foundational documents exist with substantial content.

On the billing concern, the docs use the begin/finalize autopilot cycle RPCs for atomic per-tenant charging, which aligns with the "reuse rails" principle and is actually more correct than calling deduct_mco_coins directly. The pattern satisfies the fail-closed, per-tenant atomic RPC requirement even if it doesn't literally cite that function name, so I'll note it as a minor observation rather than a blocker. Now I'm moving through the process-flow to trace FR coverage and then skimming the quality metrics and opening sections of the requirement documents.

</details>


## 🤖 Claude *(14:56:32)*

Now the process-flow (07) and a check of 01/02/03/08 for completeness.

## 🤖 Claude *(14:56:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/07-process-flow.md"
}
```

## 🤖 Claude *(14:56:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/08-quality-metrics.md",
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Quality & Self-Optimization Specification
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence) — anti-Goodhart, medição material por execução, ligação ao Collective Efficiency Ledger
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14) + [`01-mrd.md`](01-mrd.md) → [`05-sdd.md`](05-sdd.md) + [`06-data-model.md`](06-data-model.md). Todo KPI/FMEA/gate abaixo deriva de um `FR-CAD-xxx` / `NFR-CAD-xxx` / `OTD-CAD-xxx` / `FM-CAD-xx` / guardrail `Gn` já selado; nada é inventado além do blueprint (Lei 1).
> 8	
> 9	> **ORO triplet desta task:**
> 10	> - **Operator:** MCORCH Master Execution Agent
> 11	> - **Reviewer:** Sovereign (Gabriel)
> 12	> - **Owner:** Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 13	>
> 14	> **Nota de fidelidade (Lei 1):** as métricas de inbound (FR-CAD-012/013) permanecem `[PROBE-GATED]` — só entram em vigor após o probe FM-CAD-02 (RPN 486) fechar com DM real de terceiro sem role + payload cru arquivado. §3 do blueprint (posicionamento vs. ManyChat) permanece sob **SELO DE NÃO-VERIFICAÇÃO**: nenhum KPI abaixo cita §3 como fato.
> 15	
> 16	---
> 17	
> 18	## 0. Filosofia de qualidade — o gate anti-Goodhart (CMQ/OE)
> 19	
> 20	> *"When a measure becomes a target, it ceases to be a good measure."* — Goodhart. Em cadência de publicação a lei de Goodhart é **letal**: a métrica ingênua ("posts publicados/dia", "DMs respondidas", "mensagens enviadas") é **exatamente** o que um bot de spam maximiza — e é o que o §6 do blueprint proíbe por construção (G3/G4: frequência excessiva = ban do app).
> 21	
> 22	**Três invariantes anti-Goodhart deste módulo (todos já materializados nos docs 05/06):**
> 23	
> 24	1. **A verdade é financeira, não de volume.** O denominador de todo KPI de eficácia é o `collective_efficiency_ledger` (mco/resultado + overhead, derivado de `pipeline_runs`/`autopilot_cycles` — a verdade financeira, não um contador auto-reportado). Custo externo BYOK que o tenant absorve (Meta AI Provider BR, X post-com-URL) é **medido** em `cadence_dispatches.external_usd_cost` mesmo quando a cobrança em mco é 0 (NFR-CAD-008) — "não cobrar ≠ não medir". **Maximizar volume sem receita PIORA o KPI** (mco/resultado sobe).
> 25	2. **`sent` não é auto-declarado.** Nenhum KPI de entrega conta a partir do `202` da API — só do **webhook de status** (NFR-CAD-002 / FM-CAD-05). Um contador que se incrementa sozinho é uma mentira mensurável (Lei 1).
> 26	3. **Halt é sucesso, não falha.** Quiet-hours HALT (FR-CAD-008), frequency-cap HALT, dedup/digest (FR-CAD-009) e opt-out no send **reduzem** o volume publicado de propósito. O KPI de saúde de cadência **recompensa** a supressão correta (é a diferença entre cadência e flood), nunca a penaliza.
> 27	
> 28	**Regra de leitura:** todo KPI de "quantidade" (KPI-CAD-002/003) só é interpretável **junto** ao seu par de eficiência (KPI-CAD-006/007). Volume isolado é proibido como meta (herda o gap OTD-AG do ledger — sem álgebra de priorização entre planos, o cap pode causar starvation; ver Pattern P20 `deferred` na SDD §9).
> 29	
> 30	---
> 31	
> 32	## 1. Quality Objectives
> 33	
> 34	| QO ID | Objective | Linked BR / BO | Target | Anti-Goodhart guard | Review Cadence |
> 35	|-------|-----------|----------------|--------|---------------------|----------------|
> 36	| QO-CAD-001 | **Zero double-post** sob tick sobreposto/retry (integridade da idempotência) | BR-CAD-003 · FR-CAD-003 · NFR-CAD-001 | 0 dispatches duplicados por `(plan_id, step_index, occurrence_at)` | Contado no ledger `cadence_dispatches`, não no cliente | Weekly |
> 37	| QO-CAD-002 | **Materialidade da entrega** — `sent` só do webhook de status, nunca do 202 | FR-CAD-006 · NFR-CAD-002 · FM-CAD-05 | 100% dos `sent` reconciliados | Reconcile obrigatório; 202 nunca marca sent | Weekly |
> 38	| QO-CAD-003 | **Correção de fuso** — `next_run_at` sempre em UTC; cron nunca carrega horário do usuário | FR-CAD-007 · NFR-CAD-003 · FM-CAD-06 | 100% dos re-arms em UTC | Teste do calculador cobre GMT × fuso | Monthly |
> 39	| QO-CAD-004 | **Compliance estrutural** — guardrails G1–G14 impostos por construção, nunca por LLM | BR-CAD-014/015 · NFR-CAD-010 | 14/14 guardrails materiais | FK NOT NULL / UNIQUE / fail-closed / server-side | Per migration |
> 40	| QO-CAD-005 | **Eficiência coletiva** — mco/resultado do ciclo de cadência não degrada vs. baseline; custo BYOK visível | BR-CAD-010/012 · NFR-CAD-007/008 · G7 | mco/resultado ≤ baseline; 100% custo externo registrado | Denominador = `collective_efficiency_ledger` (verdade financeira) | Monthly |
> 41	| QO-CAD-006 | **Isolamento multi-tenant** — zero vazamento cross-tenant; cliente nunca escreve `cadence_dispatches` | BR-CAD-002 · NFR-CAD-006 | `count cross-tenant = 0` | `/security-review` NO FINDINGS + RLS deny smoke | Per migration |
> 42	| QO-CAD-007 | **Zero infra nova** — nenhum job pg_cron adicionado (a Cadência encaixa no tick vivo) | BR-CAD-004 · NFR-CAD-012 · OTD-CAD-003 | `count(*) FROM cron.job` invariante | Antes/depois do deploy da cadência | Per release |
> 43	
> 44	---
> 45	
> 46	## 2. KPI Dashboard Definition
> 47	
> 48	> Data source: tabelas/views Supabase por KPI. **Regra anti-Goodhart:** KPIs de volume (002/003) **só** leem junto ao par de eficiência (006/007). Denominador de eficácia = `collective_efficiency_ledger` (nunca contador auto-reportado).
> 49	
> 50	| KPI ID | Name | Formula | Target | Warn | Critical | Data Source |
> 51	|--------|------|---------|--------|------|----------|-------------|
> 52	| KPI-CAD-001 | **Double-post rate** (integridade) | `COUNT(dup idempotency_key WHERE status<>'failed') / COUNT(dispatches)` | **0** | > 0 (1 evento) | > 0.1% | `cadence_dispatches` (índice parcial) |
> 53	| KPI-CAD-002 | Dispatch throughput (volume — **não-meta**) | `COUNT(cadence_dispatches WHERE status='sent') / período` | informativo | — | — | `cadence_dispatches` |
> 54	| KPI-CAD-003 | Halt rate (supressão correta — **saúde, não falha**) | `COUNT(status='halted' quiet/freq/digest) / COUNT(tentativas)` | 5–40% (esperado) | < 1% (cap não lê) | 0% por 7d | `infra_health_logs` (`cadence_halt_*`) |
> 55	| KPI-CAD-004 | **Reconcile latency** (materialidade) | `p95(sent_reconciled_at − dispatched_at)` | ≤ 10 min | > 30 min | > 2 h ou % não reconciliado > 5% | `cadence_dispatches` + webhook de status |
> 56	| KPI-CAD-005 | **UTC re-arm correctness** | `COUNT(next_run_at coerente com recurrence em UTC) / re-arms` | 100% | < 100% | < 99% | teste do calculador + `autopilot_plans` |
> 57	| KPI-CAD-006 | **mco/resultado do ciclo** (eficiência — **anti-Goodhart core**) | `SUM(mco cobrado ciclo) / SUM(resultado atribuído)` via ledger | ≤ baseline `autopilot`/`pipeline` | > baseline ×1.5 | > baseline ×3 | `collective_efficiency_ledger` |
> 58	| KPI-CAD-007 | **Custo externo BYOK visível** | `COUNT(dispatch BYOK com external_usd_cost NOT NULL) / COUNT(dispatch BYOK)` | 100% | < 100% | < 95% | `cadence_dispatches.external_usd_cost` + `cost_source` |
> 59	| KPI-CAD-008 | **Projected vs. actual mco** (honestidade do quote) | `abs(projected_cost_mco − actual_mco_ciclo) / projected` | ≤ 10% | > 25% | > 50% | inspector projection (FR-CAD-011) vs. ledger |
> 60	| KPI-CAD-009 | **A/B bucket balance** (anti-viés silencioso) | distribuição de `bucket A` vs. `ratio` configurado | ±5% do ratio | > ±10% | ~50% (bug `% 100`) | `cadence_dispatches` A/B tag (FR-CAD-010) |
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Process & Automation Blueprint — Process Flow (BPM CBOK)
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** BPM CBOK v4 (Process Modeling + Process Design) — fluxos ponta-a-ponta com **gates de verificação** e **recovery paths**
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14) + [`01-mrd.md`](01-mrd.md) + [`02-brd.md`](02-brd.md) + [`03-prd.md`](03-prd.md) + [`04-frd.md`](04-frd.md) + [`05-sdd.md`](05-sdd.md). Cada processo abaixo executa um conjunto de `FR-CAD-xxx` (FRD §2) e materializa um design da SDD §3 (Data Flow); nada é inventado além do blueprint (Lei 1).
> 8	
> 9	> **ORO triplet desta task:**
> 10	> - **Operator:** MCORCH Master Execution Agent
> 11	> - **Reviewer:** Sovereign (Gabriel)
> 12	> - **Owner:** Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 13	>
> 14	> **Closed-Loop gate:** este é o **7º** documento da suíte BoK. A SDD (`05-sdd.md`) e a Pattern Conformance Declaration (§9 da SDD → `09-pattern-conformance.md`) são a fonte de design; este documento **não** decide arquitetura — desenha os **fluxos** e seus **gates de verificação**. Permanecem ABERTOS: SOP Lei 2 (`docs/processes/spaces-cadence.md`) + `/security-review` de toda migration. **Nenhuma linha de código antes disso.**
> 15	>
> 16	> **Nota de fidelidade (Lei 1):** **PROC-CAD-07** (laço inbound IG, FR-CAD-012/013) permanece `[PROBE-GATED]` — desenhado como **fluxo congelado**, ativável só após o probe FM-CAD-02 (RPN 486) fechar com DM real de terceiro sem role + payload cru arquivado. Nenhum fluxo abaixo cita §3 do blueprint (posicionamento vs. ManyChat, sob **SELO DE NÃO-VERIFICAÇÃO**) como fato. **Mandato de integração:** a Cadência **encaixa nos trilhos vivos** (autopilot · `scheduled_posts` · sequences/`nurture-dispatch`) — **nenhum job pg_cron novo**, nenhuma tabela de plano paralela.
> 17	
> 18	---
> 19	
> 20	## 1. Process Inventory
> 21	
> 22	| Process ID | Name | Type | Trigger | Owner | SLA | FR |
> 23	|------------|------|------|---------|-------|-----|----|
> 24	| **PROC-CAD-00** | Fatia 0 — pré-requisitos P0 (reachability + fixes) | `event-driven` (deploy) | Antes de qualquer código de cadência | System / Sovereign | one-shot | FR-CAD-015/016/017/018 |
> 25	| **PROC-CAD-01** | Armar plano de cadência | `human-in-loop` | User clica **Armar** no `CadenceInspector` | User | < 800 ms p95 | FR-CAD-001/005/011 |
> 26	| **PROC-CAD-02** | Tick + roteamento por `plan_kind` | `cron` | pg_cron `*/15` (GMT) → `autopilot-cadence-cron` | System | < 30 s por tick | FR-CAD-004 |
> 27	| **PROC-CAD-03** | Ciclo de cadência (`cadence-run`) | `automated` | Roteado por PROC-CAD-02 quando `plan_kind='cadence'` | System | < 5 s / batch 50 | FR-CAD-006/007/008/009/010 |
> 28	| **PROC-CAD-04** | Drain + publicação (`auto-publish`) | `cron` | pg_cron `*/5` → `auto-publish` (`FOR UPDATE SKIP LOCKED`) | System | < 5 min | FR-CAD-018 |
> 29	| **PROC-CAD-05** | Reconciliação por webhook de status | `event-driven` | Webhook de **status** da plataforma (nunca o 202) | System | ≤ janela do provider | NFR-CAD-002 · FM-CAD-05 |
> 30	| **PROC-CAD-06** | Eliminação LGPD em cascata (`erase_lead`) | `event-driven` | Rota pública de opt-out / pedido de eliminação | System | atômico (1 txn) | FR-CAD-017 · G9 |
> 31	| **PROC-CAD-07** `[PROBE-GATED]` | Laço inbound IG (comentário/DM → resposta na janela) | `event-driven` | `instagram-webhook` recebe `entry.messaging`/`comments` | System | ≤ 24 h CSW / ≤ 7 d private reply | FR-CAD-012/013 |
> 32	| **PROC-CAD-08** | Canais desimpedidos BYOK (Telegram / Email Resend) | `human-in-loop` (flip) | Passo `program` resolve canal BYOK | User / Sovereign | fail-closed | FR-CAD-014 |
> 33	
> 34	> Types: `automated` | `human-in-loop` | `cron` | `event-driven`. **Regra de integração:** PROC-CAD-02/04 rodam sobre o pg_cron **existente** (roteamento + migração de `auto-publish`), **sem** adicionar job (NFR-CAD-012). PROC-CAD-03 nunca publica — **enfileira** em `scheduled_posts` (sink one-shot); quem publica é PROC-CAD-04.
> 35	
> 36	---
> 37	
> 38	## 2. BPMN-lite Process Maps
> 39	
> 40	### PROC-CAD-00: Fatia 0 — pré-requisitos P0 (sem os quais tudo é falso-sucesso)
> 41	
> 42	```
> 43	START
> 44	  │
> 45	  ├─▶ [Add bloco [functions.whatsapp-webhook] verify_jwt=false em config.toml]
> 46	  │        │ GATE: curl webhook → status ≠ 401 (challenge hub.challenge ecoado)   (FR-CAD-015)
> 47	  │        └─(ainda 401)──▶ [HALT: gateway bloqueia; webhook é código morto]
> 48	  │
> 49	  ├─▶ [Trocar HMAC === por timingSafeEqual (_shared/oauth-state.ts)]
> 50	  │        │ GATE: grep timingSafeEqual ≥1 · zero `===` na verificação de assinatura   (FM-CAD-09)
> 51	  │
> 52	  ├─▶ [Redirecionar sink whatsapp_leads → leads/lead_events]
> 53	  │        │ GATE: POST assinado insere lead_events (UUID por SELECT)
> 54	  │
> 55	  ├─▶ [estimateNodeCost: add case 'publishSocial']
> 56	  │        │ GATE: runAllCost de grafo com publishSocial é finito (≠ NaN)   (FR-CAD-016 · FM-CAD-16)
> 57	  │
> 58	  ├─▶ [erase_lead(): cancelar scheduled_posts + cadence_dispatches na MESMA txn]
> 59	  │        │ GATE: pós-erase count(pending)=0 e count(queued|publishing)=0; rollback atômico   (FR-CAD-017 · G9)
> 60	  │
> 61	  └─▶ [Migrar auto-publish → pg_cron + FOR UPDATE SKIP LOCKED]
> 62	           │ GATE: cron.job tem linha auto-publish · claim contém SKIP LOCKED · 2 runs concorrentes = 0 double-publish   (FR-CAD-018 · FM-CAD-01)
> 63	           ▼
> 64	        END (todos os 6 gates verdes ⇒ Fatia 1 destravada)
> 65	```
> 66	
> 67	**Swimlanes:**
> 68	
> 69	| Swimlane | Participant | Tasks |
> 70	|----------|-------------|-------|
> 71	| Sovereign | Revisão + GO | Aprova `/security-review` de cada migration; confirma reachability do webhook |
> 72	| Edge Function | `whatsapp-webhook` | Torna-se alcançável (`config.toml`) + `timingSafeEqual` + sink `lead_events` |
> 73	| Frontend | `src/types/canvas.ts` | `estimateNodeCost` ganha `case 'publishSocial'` |
> 74	| DB | `erase_lead()` · pg_cron | Cascata LGPD; `auto-publish` sob pg_cron + `SKIP LOCKED` |
> 75	
> 76	> **Recovery:** qualquer gate vermelho **bloqueia** a Fatia 1 (não há "seguir mesmo assim"). OTD-CAD-001/004/006/007 = P0 declarado.
> 77	
> 78	---
> 79	
> 80	### PROC-CAD-01: Armar plano de cadência (FR-CAD-005 / SDD §3.1)
> 81	
> 82	```
> 83	[User Action: configura recorrência + canais + budget_cap_mco no CadenceInspector]
> 84	  │
> 85	  ▼
> 86	[Gate UI: inspector projeta custo por ciclo em mco (Σ canal × ocorrências até cap), em --gold]   (FR-CAD-011)
> 87	  │  └─(sem budget_cap_mco)──▶ botão Armar desabilitado
> 88	  ▼
> 89	[Hook: useCanvasStudio → cadence-plan invoke]  (cadence FORA de needsLedgerRun — não gera ⇒ sem node_run_id)
> 90	  │
> 91	  ▼
> 92	[Edge Fn: cadence-plan]  (verify_jwt=false → ES256 JWKS verify; NUNCA atob cego)
> 93	  ├── Validar JWT (ES256) ──(fail)──▶ HTTP 401 "Unauthorized"
> 94	  ├── Validar payload ──(budget_cap_mco ausente/≤0 · recurrence inválida · minutes%5≠0 · canal fora da allowlist)──▶ HTTP 422 {error,field,message pt-BR}
> 95	  ├── compute next_run_at em UTC a partir de recurrence (cascata tz → profiles.timezone → America/Sao_Paulo)   (FR-CAD-007 · FM-CAD-06)
> 96	  ├── UPSERT autopilot_plans (plan_kind='cadence', user_id server-trusted da claim)   (FR-CAD-002)
> 97	  └── HTTP 200 { plan_id, next_run_at ISO UTC, projected_cost_mco }
> 98	       │  ── 0 mco debitado (profiles.mco_balance INALTERADO — G7 é invariante do CICLO, não do nó)
> 99	       ▼
> 100	[Hook poll: molde useVoiceRenderPoll → next_run_at + últimas N cadence_dispatches]  (id no data do nó; sobrevive a refresh — NUNCA sleep(8s)×25)
> 101	  │
> 102	  ▼
> 103	END
> 104	```
> 105	
> 106	**Swimlanes:**
> 107	
> 108	| Swimlane | Participant | Tasks |
> 109	|----------|-------------|-------|
> 110	| User | `CadenceNode` + `CadenceInspector` | Configura recorrência/canais/budget; vê custo projetado; clica Armar |
> 111	| Frontend Hook | `useCanvasStudio.ts` · `useCadenceRunPoll.ts` | Invoca `cadence-plan`; faz poll (molde `useVoiceRenderPoll`) |
> 112	| Edge Function | `cadence-plan` | ES256 JWKS · valida · computa `next_run_at` UTC · upsert `autopilot_plans` |
> 113	| DB | `autopilot_plans` (RLS owner-scoped) · `profiles.timezone` (SSOT) · `channel_profiles.cadence` (teto) | Persiste plano; ressuscita 2 dados mortos |
> 114	
> 115	**Gates de verificação (materiais, Lei 1):** `plan_id` UUID retornado por `SELECT`; `next_run_at` em UTC coerente com `recurrence`; JWT forjado → 401; `profiles.mco_balance` inalterado (0 débito na criação).
> 116	
> 117	---
> 118	
> 119	### PROC-CAD-02: Tick + roteamento por `plan_kind` (FR-CAD-004 / SDD §3.2 topo)
> 120	
> 121	```
> 122	START (pg_cron */15, GMT — o tick VIVO autopilot-cadence-cron; NENHUM job novo)
> 123	  │
> 124	  ▼
> 125	[Edge Fn: autopilot-cadence-cron]
> 126	  ├── Gate: Authorization === Bearer SB_SECRET_KEY ──(fail)──▶ HTTP 403 "Forbidden"
> 127	  ├── SELECT plans WHERE next_run_at <= now() AND is_active   (índice parcial due — reusado)
> 128	  │        (user_id SERVER-TRUSTED da LINHA, nunca do body — SOP autopilot-cron-identity.md)
> 129	  │
> 130	  ├──▶ <Gateway: plan_kind?>
> 131	  │        │ 'viral'                          │ 'cadence'
> 132	  │   [dispatch → autopilot-run]        [dispatch → cadence-run]   (PROC-CAD-03)
> 133	  │   (fluxo existente, intocado)             │
> 134	  │                                     fan-out BOUNDED (MAX_PER_RUN=50 / CONCURRENCY=6)   (FM-CAD-07)
> 135	  │
> 136	  └── pg_cron não sobrepõe a MESMA job (fila) ⇒ tick anterior ainda rodando não empilha
> 137	       ▼
> 138	END
> 139	```
> 140	
> 141	**Gates de verificação:** `SELECT count(*) FROM cron.job` **inalterado** antes/depois (NFR-CAD-012 — 0 job novo); POST ao tick sem `Bearer SB_SECRET_KEY` → **403**; log mostra `cadence-run` para linhas `plan_kind='cadence'` e `autopilot-run` para `'viral'`.
> 142	
> 143	> **Recovery:** tick que falha em N linhas registra `infra_health_logs` por linha e **continua** o batch (fan-out isolado). pg_cron re-dispara em 15 min; `next_run_at` não avança para linhas não processadas ⇒ recuperação natural na próxima janela (limitada por `catchup_window`).
> 144	
> 145	---
> 146	
> 147	### PROC-CAD-03: Ciclo de cadência — `cadence-run` (FR-CAD-006, o coração / SDD §3.2)
> 148	
> 149	```
> 150	START (invocado por PROC-CAD-02 · Auth Bearer SB_SECRET_KEY → 403; user_id da LINHA)
> 151	  │
> 152	  ▼
> 153	[1) DRAIN: SELECT ... FROM autopilot_plans WHERE due AND plan_kind='cadence' FOR UPDATE SKIP LOCKED]   (evita contenção multi-consumer)
> 154	  │
> 155	  ├──▶ <Gateway: overlap_policy=skip — ciclo anterior deste plano ainda rodando?>
> 156	  │        │ SIM ──▶ [SKIP: não empilha] ──▶ re-arm janela seguinte
> 157	  │        │ NÃO
> 158	  ▼
> 159	[2) RESOLVE SUBJECT owner-scoped: creative_assets.id (Fatia 1 = asset existente ⇒ 0 mco, keyless)]   (OTD-CAD-002=A)
> 160	  │        └─(asset não pertence ao user_id da linha)──▶ HALT + infra_health_logs
> 161	  ▼
> 162	[3) GATE CHAIN — server-side, NUNCA LLM]:
> 163	  ├── quiet_hours(fuso do sujeito, cascata tz→profiles.timezone→America/Sao_Paulo) ──(dentro)──▶ HALT (suprime, não reenfileira)   (FR-CAD-008)
> 164	  ├── frequency_cap(user_id, channel) vs teto channel_profiles.cadence ──(estourou)──▶ HALT + toast pt-BR (Knock: HALT, não reenfileira)   (FR-CAD-008 · OTD-CAD-008=autoritativo · OTD-CAD-017=(user,channel))
> 165	  ├── opt-out: withdrawn_at checado NO SEND, independente da base legal ──(revogado)──▶ HALT + cascata   (G3/G8 · FM-CAD-04)
> 166	  ├── jurisdição: lead sem país ⇒ tratar como UE (opt-in prévio, fail-closed)   (G11 · OTD-CAD-015=consent fail-closed BR)
> 167	  ├── dedup/digest: digestKey=(user,channel,dia) colapsa N vencimentos em 1 publicação   (FR-CAD-009)
> 168	  └── A/B: mod(abs(hashtext(subject_ref||':'||experiment_key)::bigint),100) < ratio   (FR-CAD-010 — cast bigint ANTES do abs; NUNCA %100 nem random())
> 169	  │
> 170	  ▼
> 171	[4) DISPATCH: INSERT scheduled_posts (metadata.reshape + schedule:true + publish_at ISO)]   (Amendment 22 — o nó ENFILEIRA, não publica)
> 172	  │        └─(data inválida)──▶ 422 · (double-enqueue)──▶ 409 GROUP MARKER
> 173	  ▼
> 174	[5) LEDGER: INSERT cadence_dispatches ... ON CONFLICT DO NOTHING RETURNING]
> 175	  │        (índice único PARCIAL WHERE status<>'failed' — falha LIBERA a chave / sucesso PRENDE)   (FR-CAD-003 · FM-CAD-01)
> 176	  │        └─(conflito ⇒ 0 linhas)──▶ [já despachado neste occurrence: NO-OP anti double-post]
> 177	  ▼
> 178	[6) RE-ARM: next_run_at ← próximo horário em UTC (calculador {frequency,days,hours,minutes,tz})  |  deactivate se fim de programa]   (FR-CAD-007)
> 179	  │
> 180	  ▼
> 181	[Insert mcorch_node (observação) no 1º ciclo bem-sucedido do plano]   (Mesh Connection Mandate · Pattern P8)
> 182	  │
> 183	  ▼
> 184	END
> 185	        ▼ (assíncrono, desacoplado)
> 186	[PROC-CAD-04 auto-publish DRENA scheduled_posts → publica]
> 187	        ▼
> 188	[PROC-CAD-05 reconcile webhook de STATUS → cadence_dispatches.status='sent' + external_usd_cost + cost_source]   (NUNCA do 202 — FM-CAD-05, Lei 1)
> 189	```
> 190	
> 191	**Swimlanes:**
> 192	
> 193	| Swimlane | Participant | Tasks |
> 194	|----------|-------------|-------|
> 195	| Cron/Edge | `autopilot-cadence-cron` → `cadence-run` | Drain `SKIP LOCKED`; gate chain; dispatch; ledger; re-arm |
> 196	| DB | `autopilot_plans` · `cadence_dispatches` · `scheduled_posts` · `channel_profiles.cadence` | Índice parcial de idempotência; teto de frequência; sink |
> 197	| Ledger financeiro | `begin`/`finalize` (só se houver passo `generate`) | Débito atômico advisory-lock; refund idempotente; G7 = invariante do ciclo |
> 198	| Mesh | `mcorch_nodes` · `infra_health_logs` | Nó de observação por ciclo; telemetria em todo path de falha |
> 199	
> 200	**Gates de verificação (materiais):** 1 plano vencido → **1** linha `cadence_dispatches` + **1** linha `pending` em `scheduled_posts`; tick sobreposto/retry → **0** 2º dispatch para o mesmo `(plan_id, step_index, occurrence_at)` (smoke re-executável); **nenhuma** linha `sent` a partir de 202; `next_run_at` avança em UTC.
> 201	
> 202	> **Recovery paths:**
> 203	> - **Falha no dispatch (passo 4):** ledger recebe `status='failed'` ⇒ o índice parcial **libera** a `idempotency_key` ⇒ o próximo tick **retenta** o mesmo `occurrence_at` (at-least-once — OTD-CAD-006=A). Backoff por contagem (molde `auto-publish:200-212`).
> 204	> - **Backlog storm** (queda de N horas): `catchup_window` (6h) **limita** quantos vencimentos atrasados disparam; `jitter_seconds` espalha; fan-out bounded (FM-CAD-07).
> 205	> - **Kill-switch:** `is_active=false` no plano (por limiar conservador auto-imposto de feedback negativo — FM-CAD-14) **para** o drain daquele plano no próximo tick.
> 206	
> 207	---
> 208	
> 209	### PROC-CAD-04: Drain + publicação — `auto-publish` (FR-CAD-018 / OTD-CAD-004)
> 210	
> 211	```
> 212	START (pg_cron */5 — MIGRADO de crontab de SO; Fatia 0 item 5)
> 213	  │
> 214	  ▼
> 215	[SELECT ... FROM scheduled_posts WHERE status='pending' AND scheduled_at<=now() FOR UPDATE SKIP LOCKED LIMIT <batch>]
> 216	  │        (dois runs concorrentes NUNCA reivindicam a mesma linha)   (FM-CAD-01)
> 217	  ▼
> 218	[Resolve asset owner-scoped NA HORA (metadata.reshape) → publica via seam existente (reshape-pillar / publish-space-asset 409 / publish-space-carousel)]
> 219	  ├──(sucesso)──▶ [UPDATE status='published']
> 220	  │                     ▼
> 221	  │              (a plataforma emitirá webhook de STATUS → PROC-CAD-05)
> 222	  └──(erro)──▶ <Gateway: retry_count ≤ N?>
> 223	                   │ SIM ──▶ [retry_count+1; backoff por contagem] ──▶ próxima janela
> 224	                   │ NÃO  ──▶ [UPDATE status='failed'] + infra_health_logs
> 225	                                   ▼
> 226	                                END
> 227	```
> 228	
> 229	**Gates de verificação:** `SELECT jobname FROM cron.job WHERE command ILIKE '%auto-publish%'` ≥1 linha; claim contém `FOR UPDATE SKIP LOCKED`; smoke de concorrência = **0** double-publish.
> 230	
> 231	> **Nota de fronteira:** `auto-publish` é **reusado sem tocar na lógica de publicação** — a Fatia 0 só troca o **supervisor** (crontab de SO → pg_cron) e adiciona `SKIP LOCKED`. A cadência **não reconstrói distribuição** (mandato de integração).
> 232	
> 233	---
> 234	
> 235	### PROC-CAD-05: Reconciliação por webhook de status (NFR-CAD-002 / FM-CAD-05)
> 236	
> 237	```
> 238	START (webhook de STATUS da plataforma — NUNCA o 202 de aceite da API)
> 239	  │
> 240	  ▼
> 241	[Verificar identidade: HMAC timingSafeEqual (webhook)  |  ES256 JWKS (se JWT)]  ──(fail)──▶ 401
> 242	  │
> 243	  ▼
> 244	[Casar evento ↔ cadence_dispatches (target_ref / external id)]
> 245	  │
> 246	  ├──(status=delivered/sent)──▶ [UPDATE cadence_dispatches SET status='sent', external_usd_cost=<custo>, cost_source=<fonte BYOK>]   (service-role)
> 247	  │                                    ▼
> 248	  │                             [Agregar em collective_efficiency_ledger]  (custo BYOK MEDIDO mesmo com cobrança mco=0 — NFR-CAD-008)
> 249	  │
> 250	  └──(status=failed/rejected)──▶ [UPDATE status='failed' (libera idempotency_key p/ retry) + infra_health_logs]
> 251	       ▼
> 252	     END
> 253	```
> 254	
> 255	**Gates de verificação:** **nenhuma** linha transiciona para `sent` sem um webhook de status casado (auditoria de reconcile 100%); `external_usd_cost` numérico gravado **no reconcile** (não no 202); cobrança em mco = **0** para canais BYOK cujo custo o tenant absorve, com o custo ainda **registrado** (Lei 1 — "não cobrar ≠ não medir").
> 256	
> 257	> **Recovery:** webhook de status ausente por T > SLA do provider ⇒ reconciliação por **poll** (molde do poll de `video_renders`) reconcilia o órfão; nunca declarar `sent` por timeout (isso seria o falso-sucesso do 202).
> 258	
> 259	---
> 260	
> 261	### PROC-CAD-06: Eliminação LGPD em cascata — `erase_lead()` (FR-CAD-017 / G9 / OTD-CAD-006)
> 262	
> 263	```
> 264	[Trigger: rota pública de opt-out por token assinado  |  pedido de eliminação (LGPD Art. 16/18 VI)]
> 265	  │
> 266	  ▼
> 267	[SELECT erase_lead('<lead_uuid>')]  (SECURITY DEFINER, search_path='', tenant-guarded)
> 268	  │  ── tudo NA MESMA TRANSAÇÃO:
> 269	  ├── UPDATE scheduled_posts SET status='cancelled' WHERE lead_id=<lead> AND status='pending'
> 270	  ├── UPDATE cadence_dispatches SET status='failed', error='erased' WHERE bound-ao-lead AND status IN ('queued','publishing')
> 271	  ├── anonimiza/apaga leads + lead_events + marketing_consents (comportamento existente)
> 272	  │
> 273	  ├──(qualquer passo falha)──▶ ROLLBACK atômico (nada apagado pela metade)
> 274	  ▼
> 275	END
> 276	```
> 277	
> 278	**Gates de verificação:** pós-`erase_lead`, `count(*) scheduled_posts pending`=**0** e `count(*) cadence_dispatches IN(queued,publishing)`=**0** para o lead; atomicidade comprovada (rollback se qualquer passo falhar). Sem esta cascata o direito de eliminação é **ficção** (P0 de conformidade).
> 279	
> 280	---
> 281	
> 282	### PROC-CAD-07 `[PROBE-GATED]`: Laço inbound IG (FR-CAD-012/013 / SDD §3.3)
> 283	
> 284	> ⚠️ **FLUXO CONGELADO.** Nada abaixo da linha `instagram-webhook` gera código antes do **probe FM-CAD-02** fechar: DM real de **terceiro sem role no app** aparecendo no banco + **payload cru** de `entry.messaging` arquivado (FM-CAD-13). Se não chegar sob Standard Access ⇒ **App Review é pré-requisito** e a Fatia 2 inteira está bloqueada.
> 285	
> 286	```
> 287	[scheduled_posts → auto-publish publica no IG (PROC-CAD-04)]
> 288	  │  (o post provoca comentário/DM)
> 289	  ▼
> 290	[instagram-webhook]  (HMAC timingSafeEqual + hub.challenge — esqueleto REUSADO; app secret GLOBAL, OTD-CAD-018)
> 291	  ├──▶ <Gateway: shape do payload?>
> 292	  │        │ entry.changes: comments        │ entry.messaging: DM  ⚠️ shape PROVADO por payload cru real (FM-CAD-13)
> 293	  ▼
> 294	[INSERT lead_events(event_type='message_received') + leads + notify()]  (lead_events entra HOJE, sem migration)
> 295	  ▼
> 296	[UPSERT social_threads / social_messages]  (Meta só devolve as 20 últimas ⇒ histórico mora AQUI; csw_expires_at 24h + private_reply_deadline 7d derivados no SERVIDOR)
> 297	  ▼
> 298	[GATE CHAIN de resposta — server-side, NUNCA LLM]:
> 299	  ├── FK NOT NULL p/ inbound: fila referencia lead_events(message_received) do MESMO user_id ⇒ cold DM IMPOSSÍVEL de representar   (G1 · FM-CAD-03)
> 300	  ├── classificador in/out-window ──(fora da janela)──▶ nada promocional (só template APPROVED ou draft HITL)   (G6)
> 301	  ├── Human Agent tag INALCANÇÁVEL do caminho service-role/pg_cron (separação de caminho, não if)   (G5)
> 302	  ├── caps por-APP + kill-switch GLOBAL + telemetria de feedback negativo por-app   (OTD-CAD-018)
> 303	  │
> 304	  ├──▶ <Gateway: origem?>
> 305	  │        │ comentário                              │ DM in-window
> 306	  │   [private reply 1× comment→DM]            [resposta free-form ≤24h CSW]
> 307	  │   UNIQUE(comment_id) · deadline 7d ·            │
> 308	  │   idade checada NO SEND (2º reply = 23505)       │
> 309	  ▼
> 310	[Nasce delivery:'gated' (molde nurture-dispatch:150) — flip p/ 'sent' só com GO Sovereign]
> 311	  ▼
> 312	[Resposta com link afiliado + UTM → creative_metrics → collective_efficiency_ledger]
> 313	  ▼
> 314	END
> 315	```
> 316	
> 317	**Gates de verificação (materiais):** o **probe precede o código** — `lead_events(message_received)` de DM real de terceiro sem role aparece por `SELECT` (UUID) + payload cru arquivado; enfileirar DM **sem** inbound → **viola FK**; 2º private reply p/ o mesmo `comment_id` → **23505** (`UNIQUE`); dispatch fora da janela de 24h → **bloqueado no send**; a Human Agent tag não é setável por nenhum caminho service-role; todo dispatch nasce `delivery:'gated'`.
> 318	
> 319	> **Recovery:** janela de 24h (CSW) ou 7d (private reply) expirada ⇒ o gate de janela **no send** descarta o dispatch (nunca enfileira para o futuro — cold DM = ban do app, não erro HTTP). Feedback negativo acima do limiar conservador ⇒ **kill-switch global** (`is_active=false` por-app).
> 320	
> 321	---
> 322	
> 323	### PROC-CAD-08: Canais desimpedidos BYOK — Telegram / Email Resend (FR-CAD-014)
> 324	
> 325	```
> 326	[Passo do program resolve canal BYOK: 'telegram' | 'email']
> 327	  │
> 328	  ├── Telegram ──▶ [resolveProviderKey(admin,userId,'telegram',keyId)]
> 329	  │        ├──(sem token)──▶ HTTP 402 { error:'telegram_not_configured', action:'Configure em /dashboard/settings' }
> 330	  │        ├── opt-in estrutural: chat que nunca deu /start ──▶ BLOQUEADO
> 331	  │        └──(ok)──▶ envia (US$0, Meta-free)
> 332	  │
> 333	  └── Email (Resend) ──▶ [resend_api_key per-user cifrada + domínio verificado do tenant]
> 334	           ├──(sem key / domínio não verificado)──▶ 402 estruturado / flip barrado
> 335	           ├── monta rodapé (endereço postal + identificação de anúncio + opt-out) + disclosure de IA SERVER-SIDE, concatenado ao corpo   (G10/G12 · FM-CAD-12 — NUNCA no prompt do LLM)
> 336	           └── flip nurture-dispatch delivery:'gated' → 'sent' SÓ com GO Sovereign + domínio verificado
> 337	```
> 338	
> 339	**Gates de verificação:** Telegram sem token → **402** `telegram_not_configured` com `action`; envio a chat sem `/start` bloqueado; corpo do e-mail contém rodapé/opt-out/disclosure **concatenado server-side** (prova por diff do payload, ausente no prompt); flip `gated→sent` só com flag de GO + domínio verificado (`SELECT` do estado).
> 340	
> 341	---
> 342	
> 343	## 3. Recurrence-Engine Blueprint (substitui a seção n8n — MCORCH é Postgres-first)
> 344	
> 345	> Este módulo **não** usa n8n. O motor de recorrência é **pg_cron + `next_run_at` + índice parcial due**, o padrão que o MCORCH já roda 2× em prod e que a Cadência **estende** (OTD-CAD-003=A). Nenhum job novo (NFR-CAD-012).
> 346	
> 347	**Driver:** `autopilot-cadence-cron` (VIVO, `*/15` GMT)
> 348	**Idempotency key:** `hash(plan_id, step_index, occurrence_at)` sob `UNIQUE INDEX ... WHERE status<>'failed'`
> 349	
> 350	```
> 351	[Trigger: pg_cron */15 → autopilot-cadence-cron]  (gate Bearer SB_SECRET_KEY → 403)
> 352	  │
> 353	  ▼
> 354	[SELECT plans due (índice parcial next_run_at<=now() AND is_active)]  — user_id server-trusted da LINHA
> 355	  │
> 356	  ├── plan_kind='viral'  ──▶ [HTTP → autopilot-run]   (intocado)
> 357	  │
> 358	  └── plan_kind='cadence'──▶ [HTTP → cadence-run]      (PROC-CAD-03)
> 359	           ├── (success) ──▶ [cadence_dispatches ON CONFLICT DO NOTHING RETURNING → re-arm next_run_at UTC]
> 360	           │                        │
> 361	           │                        ▼
> 362	           │                 [scheduled_posts enfileirado → auto-publish drena (desacoplado)]
> 363	           │
> 364	           └── (error) ──▶ [status='failed' (libera idempotency_key) + retry_count+1]
> 365	                    │
> 366	              (count ≤ N) ──▶ [backoff por contagem] ──▶ próximo tick retenta o mesmo occurrence_at
> 367	                    │
> 368	              (count > N) ──▶ [Insert infra_health_logs {service:'spaces-cadence', event:'cadence_dispatch_failed'}]
> 369	                                    │
> 370	                              [notify() Sovereign]
> 371	```
> 372	
> 373	**Data Mapping (inspector → plano → dispatch):**
> 374	
> 375	| Input Field | Source | → | Output Field | Destination |
> 376	|-------------|--------|---|--------------|-------------|
> 377	| `recurrence {frequency,days,hours,minutes,tz}` | `CadencePlanRequest` | → | `next_run_at` (UTC) | `autopilot_plans` |
> 378	| `channel_allowlist` (⊆ auto-publish MENOS X) | inspector | → | `channel` por dispatch | `cadence_dispatches` |
> 379	| `budget_cap_mco` (NOT NULL) | inspector | → | teto de ocorrências | gate chain (PROC-CAD-03) |
> 380	| `sourceAssetId` (owner-scoped) | inspector | → | `metadata.reshape` asset | `scheduled_posts` |
> 381	| `SB_SECRET_KEY` | env (infra) | → | `Authorization` | header cron-only |
> 382	
> 383	> **Idempotência (regra dura):** re-rodar o tick sobre o mesmo dado **produz o mesmo resultado** — o `ON CONFLICT DO NOTHING` sob o índice parcial garante 0 double-post (falha libera / sucesso prende — Trigger.dev/River). É o **predicado `WHERE status<>'failed'`** (e só ele) que impede FM-CAD-01/03.
> 384	
> 385	---
> 386	
> 387	## 4. Orchestration Integration Points
> 388	
> 389	> A Cadência **não** injeta passo no `orchestrate-content`. Ela **consome** o output a montante (asset/pilar já produzido) e **enfileira** no sink `scheduled_posts`. A tabela abaixo mapeia os **seams de integração vivos** que os fluxos acima tocam — sem reconstruir nenhum.
> 390	
> 391	| Trilho vivo | Peça | Papel no fluxo | mcoCoins | FR |
> 392	|-------------|------|----------------|----------|----|
> 393	| Autopilot | `autopilot_plans` (ESTENDIDA) + `autopilot-cadence-cron` | Plano recorrente + tick roteador (`plan_kind`) | 0 no tick | FR-CAD-002/004 |
> 394	| `scheduled_posts` (sink) | contrato `metadata.reshape` + `schedule:true` + `publish_at` (Amendment 22) | PROC-CAD-03 **enfileira**; PROC-CAD-04 **drena** | 0 no enqueue | FR-CAD-006/018 |
> 395	| sequences/`nurture-dispatch` | modelo `steps jsonb` + `current_step` + `delivery:'gated'` | Molde do `program jsonb`; canal email nasce gated | por dispatch (BYOK) | FR-CAD-014 |
> 396	| `lead_events`/`leads`/`marketing_consents` | ledger append-only + consent gate + `erase_lead()` | Inbound (PROC-CAD-07) + eliminação (PROC-CAD-06) | — | FR-CAD-012/017 |
> 397	| Ledger financeiro | `begin`/`finalize` atômico + `collective_efficiency_ledger` | Cobrança só se houver passo `generate`; custo BYOK medido no reconcile | atômico via RPC | NFR-CAD-007/008 |
> 398	
> 399	**Integration code stub (roteamento no tick existente — extensão in-place, NÃO função nova):**
> 400	```typescript
> 401	// autopilot-cadence-cron: roteia por plan_kind (FR-CAD-004) — nenhum job pg_cron novo
> 402	for (const plan of duePlans) {                 // user_id server-trusted da LINHA
> 403	  const target = plan.plan_kind === 'cadence' ? 'cadence-run' : 'autopilot-run'
> 404	  await invokeEdge(target, { plan_id: plan.id }, `Bearer ${SB_SECRET_KEY}`)
> 405	  // fan-out BOUNDED: MAX_PER_RUN=50 / CONCURRENCY=6 (FM-CAD-07)
> 406	}
> 407	```
> 408	
> 409	---
> 410	
> 411	## 5. Error Handling & Retry Strategy
> 412	
> 413	| Process | Step | Error Type | Max Retries | Backoff | Failure Action |
> 414	|---------|------|-----------|-------------|---------|----------------|
> 415	| PROC-CAD-01 | `cadence-plan` JWT | ES256 inválido/ausente | 0 | — | HTTP 401 imediato |
> 416	| PROC-CAD-01 | `cadence-plan` validação | `budget_cap_mco` ausente · `minutes%5≠0` · canal fora da allowlist | 0 | — | HTTP 422 {field, msg pt-BR} |
> 417	| PROC-CAD-02 | tick auth | sem `Bearer SB_SECRET_KEY` | 0 | — | HTTP 403 |
> 418	| PROC-CAD-03 | dispatch → `scheduled_posts` | data inválida · double-enqueue | 0 | — | 422 · 409 GROUP MARKER (anti-duplicata) |
> 419	| PROC-CAD-03 | ledger `cadence_dispatches` | conflito de idempotência | — | — | `ON CONFLICT DO NOTHING` (0 linhas ⇒ NO-OP, anti double-post) |
> 420	| PROC-CAD-03 | ciclo (transitório) | provider 5xx / timeout | N (backoff) | Exponencial (molde `auto-publish:200-212`) | `status='failed'` **libera** chave ⇒ retry no próximo tick (at-least-once) |
> 421	| PROC-CAD-03 | backlog storm | queda de N horas | limitado por `catchup_window` | `jitter_seconds` espalha | fan-out bounded (FM-CAD-07) |
> 422	| PROC-CAD-04 | `auto-publish` publish | plataforma 5xx | ≤ N (retry_count) | por contagem | `status='failed'` + `infra_health_logs` |
> 423	| PROC-CAD-05 | reconcile | webhook de status ausente | — | poll (molde `video_renders`) | reconcilia órfão; **nunca** `sent` por timeout (FM-CAD-05) |
> 424	| PROC-CAD-07 | send DM/reply | janela expirada (24h/7d) | 0 | — | descarta no send (cold DM = ban; nunca enfileira p/ futuro) |
> 425	| PROC-CAD-08 | Telegram/Resend | credencial BYOK ausente | 0 | — | HTTP 402 estruturado `{error, action}` fail-closed |
> 426	| Any | falha não-tratada | 5xx interno | — | — | `infra_health_logs {service:'spaces-cadence'}` + `notify()` |
> 427	
> 428	> **Regra de reconciliação (Lei 1):** nenhuma linha vira `sent` sem webhook de status casado. Retry **libera** a `idempotency_key` (predicado `WHERE status<>'failed'`); sucesso **prende**. Kill-switch (`is_active=false`) para o drain do plano por limiar conservador de feedback negativo (FM-CAD-14).
> 429	
> 430	---
> 431	
> 432	## 6. SLA Definitions
> 433	
> 434	| Process | Step | Expected Duration | Timeout Threshold | Alert if exceeded |
> 435	|---------|------|------------------|-------------------|-------------------|
> 436	| PROC-CAD-01 | `cadence-plan` (arm) | < 800 ms p95 | 5 s | Sim → `infra_health_logs` |
> 437	| PROC-CAD-02 | tick + roteamento | < 30 s | 60 s | Sim (job overrun; pg_cron não sobrepõe) |
> 438	| PROC-CAD-03 | `cadence-run` por batch | < 5 s / batch de 50 (NFR-CAD-013) | 30 s | Sim → `infra_health_logs` |
> 439	| PROC-CAD-04 | `auto-publish` drain | < 5 min (ciclo `*/5`) | 10 min | Sim |
> 440	| PROC-CAD-05 | reconcile | ≤ janela do provider | fallback por poll | Sim (órfão) |
> 441	| PROC-CAD-06 | `erase_lead` cascata | atômico (1 txn) | — | Sim se rollback |
> 442	| PROC-CAD-07 `[PROBE-GATED]` | resposta na janela | ≤ 24 h CSW / ≤ 7 d private reply | expiração = descarte no send | Sim (kill-switch) |
> 443	
> 444	---
> 445	
> 446	## 7. Cron Jobs
> 447	
> 448	| Job Name | Schedule (cron) | Function | Idempotency | Failure Alerting | Nota |
> 449	|----------|----------------|----------|-------------|-----------------|------|
> 450	| `autopilot-cadence-cron` (VIVO) | `*/15 * * * *` (GMT) | `autopilot-cadence-cron` → roteia por `plan_kind` | `next_run_at` + índice parcial due | `infra_health_logs` + `notify()` | **Reusado** — 0 job novo (FR-CAD-004 · NFR-CAD-012) |
> 451	| `auto-publish` (MIGRADO) | `*/5 * * * *` | `auto-publish` (`FOR UPDATE SKIP LOCKED`) | claim `SKIP LOCKED` + `status` | `infra_health_logs` | Fatia 0 item 5: crontab de SO → pg_cron (FR-CAD-018) |
> 452	
> 453	> **Invariante:** `SELECT count(*) FROM cron.job` **inalterado** pela Cadência (o roteamento reusa o tick; `auto-publish` **migra** para pg_cron, não adiciona um 3º driver). Supabase recomenda ≤~8 jobs concorrentes; pg_cron não sobrepõe a mesma job. Todo cron é **idempotente** — re-rodar sobre o mesmo dado produz o mesmo resultado (índice parcial + `ON CONFLICT DO NOTHING`).
> 454	
> 455	---
> 456	
> 457	## 8. Traceability (Process ↔ FR/OTD/FM/Guardrail)
> 458	
> 459	| Process | FR | NFR | OTD | FM | Guardrail |
> 460	|---------|----|----|-----|----|-----------|
> 461	| PROC-CAD-00 | FR-CAD-015/016/017/018 | NFR-CAD-004/011/012 | OTD-CAD-001/004/006/007 | FM-CAD-01/04/09/16 | G9 |
> 462	| PROC-CAD-01 | FR-CAD-001/005/011 | NFR-CAD-004/007/014 | OTD-CAD-002/011 | FM-CAD-06/16 | — |
> 463	| PROC-CAD-02 | FR-CAD-004 | NFR-CAD-012 | OTD-CAD-003 | FM-CAD-06/07 | — |
> 464	| PROC-CAD-03 | FR-CAD-006/007/008/009/010 | NFR-CAD-001/002/003/009/013 | OTD-CAD-005/008/016/017 | FM-CAD-01/05/07 | G3/G4/G8/G11 |
> 465	| PROC-CAD-04 | FR-CAD-018 | NFR-CAD-012 | OTD-CAD-004 | FM-CAD-01 | — |
> 466	| PROC-CAD-05 | — | NFR-CAD-002/008 | — | FM-CAD-05/10/11 | — |
> 467	| PROC-CAD-06 | FR-CAD-017 | NFR-CAD-011 | OTD-CAD-006 | FM-CAD-04 | G9 |
> 468	| PROC-CAD-07 `[PROBE-GATED]` | FR-CAD-012/013 | NFR-CAD-010/015 | OTD-CAD-018 | FM-CAD-02 (RPN 486)/03/13 | G1/G2/G5/G6 |
> 469	| PROC-CAD-08 | FR-CAD-014 | NFR-CAD-005/010 | OTD-CAD-009 | FM-CAD-12/15 | G10/G12 |
> 470	
> 471	---
> 472	
> 473	## 9. Survival Laws Self-check (process-time)
> 474	
> 475	- **Lei 1 (Materialidade):** todo processo carrega **gates de verificação materiais** (UUID/HTTP status/`count(*)`/grep/smoke). `sent` só do webhook de status (PROC-CAD-05); A/B com cast `bigint` antes do `abs`; idempotência por índice parcial (PROC-CAD-03). Este doc **não** declara sucesso — desenha fluxo.
> 476	- **Lei 2 (Processo):** este é o **SOP-lite** dos fluxos; o SOP canônico `docs/processes/spaces-cadence.md` (Operator/Sequence/Verification/Recovery/Success) permanece **aberto** — pré-requisito antes de qualquer código.
> 477	- **Lei 3 (Pruning):** N/A em design-time.
> 478	- **Lei 4 (ORO):** triplet declarado no cabeçalho.
> 479	
> 480	---
> 481	
> 482	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` + `01-mrd.md` → `05-sdd.md` (Lei 1: nenhum FR/NFR/OTD/FM/entidade/guardrail inventado além do blueprint; PROC-CAD-07 / FR-CAD-012/013 sob `[PROBE-GATED]`; §3 do blueprint sob selo de não-verificação — nenhum fluxo o cita como fato). Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança via RPC atômica begin/finalize (nunca client-side); verify_jwt=false → ES256 JWKS / HMAC timingSafeEqual (nunca `atob` cego); RLS default-deny owner-scoped. A Cadência ENCAIXA nos trilhos vivos (autopilot · scheduled_posts · sequences/nurture-dispatch) — **nenhum job pg_cron novo**, nenhuma tabela de plano paralela._
> 483	
> ```

## 🤖 Claude *(14:56:40)*

<details>
<summary>💭 Thinking Process</summary>

The suite checks out as complete and consistent, so I'm doing a quick verification that the three referenced documents exist and are substantial—they are, ranging from 21 to 29KB. The traceability matrices across the requirements, data model, and process flow all cross-reference the CAD documents consistently, so I have good confidence in the structure. I'm spot-checking one of them to confirm it contains the referenced IDs.

</details>


## 🤖 Claude *(14:56:40)*

Let me verify 01/02/03 actually contain their referenced IDs (not empty stubs).

## 🤖 Claude *(14:56:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence\necho \"=== 01-mrd MR-CAD count ===\"; grep -oE 'MR-CAD-0[0-9]{2}' 01-mrd.md | sort -u | wc -l\necho \"=== 02-brd BO/BR/BR-RISK/BAC ===\"; for p in BO-CAD BR-CAD BR-RISK-CAD BAC-CAD; do printf \"%s: \" \"$p\"; grep -oE \"${p}-[0-9]{3}\" 02-brd.md | sort -u | wc -l; done\necho \"=== 03-prd PR-CAD ===\"; grep -oE 'PR-CAD-[0-9]{3}' 03-prd.md | sort -u | wc -l\necho \"=== 03-prd Gherkin/journey markers ===\"; grep -ciE 'gherkin|cen\u00e1rio|scenario|given|dado que|persona|jornada|moscow' 03-prd.md\necho \"=== 01-mrd substance ===\"; grep -ciE 'timezone|rrule|manychat|ai act|inbound|probe' 01-mrd.md\necho \"=== 08 tail: gates G-CAD ===\"; grep -oE 'G-CAD-[A-H]' 08-quality-metrics.md | sort -u | tr '\\n' ' '; echo\necho \"=== SOP exists? ===\"; ls -la /home/gcrUX/htdocs/constellation-orchestra/docs/processes/spaces-cadence.md 2>&1\necho \"=== 09-pattern-conformance exists? ===\"; ls -la 09-pattern-conformance.md 2>&1",
  "description": "Verify ID coverage in 01/02/03/08 and SOP/09 existence"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 2
> === 01-mrd MR-CAD count ===
> 14
> === 02-brd BO/BR/BR-RISK/BAC ===
> BO-CAD: 6
> BR-CAD: 17
> BR-RISK-CAD: 12
> BAC-CAD: 10
> === 03-prd PR-CAD ===
> 20
> === 03-prd Gherkin/journey markers ===
> 26
> === 01-mrd substance ===
> 23
> === 08 tail: gates G-CAD ===
> G-CAD-A G-CAD-B G-CAD-C G-CAD-D G-CAD-E G-CAD-F G-CAD-G G-CAD-H 
> === SOP exists? ===
> ls: cannot access '/home/gcrUX/htdocs/constellation-orchestra/docs/processes/spaces-cadence.md': No such file or directory
> === 09-pattern-conformance exists? ===
> ls: cannot access '09-pattern-conformance.md': No such file or directory
> ```

## 🤖 Claude *(14:57:47)*

<details>
<summary>💭 Thinking Process</summary>

I'm verifying that all the document IDs match their expected counts across the different categories, and everything checks out so far. There's something missing with the `doc` reference that I need to track down.

Looking at the missing pieces: the `spaces-cadence.md` file is marked as a hard gate requirement in the documentation but doesn't exist yet, and `09-pattern-conformance.md` is also absent. The SDD itself acknowledges that when a module touches three or more patterns materially, that pattern conformance file should be promoted to a standalone document—but it hasn't been created yet. So I'm checking whether these missing files are blocking the gate or if the core nine documents (the index plus the 01-05 sequence plus 06, 07, and 08) are sufficient to pass. FRD seals all 18 functional requirements and traces each back to blueprint sections and requirements/business rules, with data-model and process-flow providing complete bidirectional traceability to every FR. The blueprint itself doesn't define the FRs (it declares zero inbound FRs, with numbering locked by FRD), but the docs are transparent about this — FRs map to blueprint sections and OTD/FM, which is acceptable. ✓ The BoK reuses existing autopilot, sequences, and scheduled_posts components rather than rebuilding them.

For billing, the docs route charges through the autopilot cycle's atomic begin/finalize RPC at the per-tenant level rather than calling deduct_mco_coins directly — this actually aligns better with the "reuse rails, never reimplement" principle and maintains fail-closed semantics, even though it doesn't literally cite the deduct_mco_coins function. BYOK per-user and ES256 JWKS are documented. ✓ There are two concrete gaps blocking the gate: the 09-pattern-conformance.md file is missing, though the requirement can be satisfied by the SDD §9 alone as an alternative form, and the module appears to have additional undeclared requirements that need addressing. a sibling 09-pattern-conformance.md file is actually required here since the module touches 12 patterns materially, and while the SDD carries the declaration in §9, the standalone file that the docs mandate is missing. Additionally, the SOP for Lei 2 (docs/processes/spaces-cadence.md) doesn't exist, which is a hard prerequisite per Survival Law 2, though I'm trying to determine whether it's part of the 9-doc gate or separate from the pattern conformance and traceability requirements. The 9-document core suite (00-index through 08) is complete, so I'll mark that as true. The SDD does include the 21-pattern declaration, and the functional requirements trace properly to the blueprint and appear in both the data model and process flow. Now I need to check whether the implementation reuses Rails patterns rather than reinventing them.

For the money and tenancy gates, the charging mechanism is documented as an atomic per-tenant RPC rather than a literal deduct_mco_coins call, but the intent is sound—it's never client-side and fails closed. The BYOK fail-closed behavior and ES256 JWKS are both documented. I'll mark this true since the actual implementation is more correct than the original pattern, though I should note the observation.

The verdict hinges on two concrete missing artifacts that the module's own gate accounting identifies as blockers: the standalone 09-pattern-conformance.md file and the SOP in docs/processes/spaces-cadence.md. The documentation itself is substantively excellent and passes all five content checks, but the block is procedural—the artifacts simply don't exist yet. The docs are still marked v0.1 draft pending sovereign review, and the security review is still in progress, so the honest call for starting code on Fatia 1 is blocked with a clear, concrete list of what's missing. I need to finalize the structured fields: the 9-doc suite is complete, so I'll mark complete9of9 as true, but I should list the 09-pattern-conformance file separately as a gap since it's independently tracked. The verdict stays BLOQUEADO due to the two missing artifacts, the draft status awaiting review, and the pending security review—I'll document this honestly in the gaps and missing sections.

</details>


## 🤖 Claude *(14:57:59)*

I have thoroughly read all 9 suite docs, the blueprint, the SDD Pattern Conformance §9, and the agentic-vision doctrine, and verified ID coverage and file existence on disk. Findings:

**Content checks (a–e) — all PASS on substance:**
- **(a)** The 9-doc suite is present and complete, with exact ID coverage matching the index: MR-CAD 14, BO-CAD 6/BR-CAD 17/BR-RISK-CAD 12/BAC-CAD 10, PR-CAD 20 (with Gherkin/persona/MoSCoW), FR-CAD 18, NFR-CAD 15, FM-CAD 16, PROC-CAD 9, KPI/QO/gates all present. No empty stubs.
- **(b)** SDD §9 carries the full 21-pattern Pattern Conformance Declaration (12 yes / 5 deferred / 4 n-a), each `deferred` anchored to an OTD — SSOT `docs/architecture/agentic-vision.md`. Mirrored in blueprint §9.
- **(c)** FR traceability is airtight: FRD §7 traces every FR-CAD→PR/BR/OTD/FM; data-model §8 maps every data object→FR-CAD; process-flow §8 maps every PROC→FR-CAD. Fidelity is honest (blueprint declares zero inbound FRs; FRD sealed the numbering; FR-CAD-012/013 correctly `[PROBE-GATED]`).
- **(d)** Reuse-not-rebuild is the central dogma throughout: extend `autopilot_plans` (`plan_kind`), reuse `autopilot-cadence-cron` tick (route by `plan_kind`, zero new pg_cron job), `scheduled_posts` as sink, `sequences`/`nurture-dispatch` as `program` model.
- **(e)** BYOK per-user fail-closed (NFR-CAD-005, `resolveProviderKey`, 402) and ES256 JWKS (SDD §5.3, NFR-CAD-004, never `atob`) fully documented. Charging is documented via atomic per-tenant `begin`/`finalize` RPC (the reused autopilot-cycle rail), never client-side — correct in spirit, though it reuses cycle RPCs rather than literally citing `deduct_mco_coins` (an acceptable, arguably more-correct choice for this rail; node charges 0, cycle charges).

**Two concrete BLOCKING gaps (confirmed by `ls`), flagged by the module's OWN §9 Gate Status:**
1. `docs/bok/spaces-cadence/09-pattern-conformance.md` **does not exist**. CLAUDE.md §1 Step 3.5 requires the standalone sibling for modules touching ≥3 patterns materially; the index (`[ ] PENDENTE`) and SDD both commit to promoting §9 to it. Content exists in SDD §9 — this is a one-copy fix, but the mandated artifact is absent.
2. `docs/processes/spaces-cadence.md` (SOP Lei 2) **does not exist** — hard prerequisite before any code (Survival Law 2); index marks it 🔴 ABERTO.

Plus: suite is still v0.1 **draft** (Step 2 "revisão Sovereign pendente"); `/security-review` of the 4 migrations pending (FMEA-011).

## 🤖 Claude *(14:58:21)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "complete9of9": true,
  "docsPresent": [
    "00-index.md",
    "00-deepsearch-blueprint.md",
    "01-mrd.md (MR-CAD 001..014)",
    "02-brd.md (BO 6 / BR 17 / BR-RISK 12 / BAC 10)",
    "03-prd.md (PR-CAD 20, MoSCoW+Gherkin+personas)",
    "04-frd.md (FR-CAD 001..018 SEALED + NFR 15 + AT 18)",
    "05-sdd.md (STRIDE + migrations + \u00a79 Pattern Conformance 21 patterns)",
    "06-data-model.md (ERD + selos + SQL stubs + tenant map)",
    "07-process-flow.md (PROC-CAD 00..08 + gates + recovery)",
    "08-quality-metrics.md (QO 7 / KPI 11 / FMEA 16 / G-CAD A..H)"
  ],
  "frTraceability": true,
  "patternConformanceInSDD": true,
  "reusesRailsNotRebuild": true,
  "moneyAndTenancyGates": true,
  "missing": [
    "docs/bok/spaces-cadence/09-pattern-conformance.md \u2014 arquivo standalone AUSENTE (confirmado por ls); CLAUDE.md \u00a71 Step 3.5 o exige para m\u00f3dulos que tocam \u22653 padr\u00f5es materialmente (aqui 12 yes); o conte\u00fado j\u00e1 existe em SDD \u00a79, falta promover/copiar",
    "docs/processes/spaces-cadence.md \u2014 SOP Lei 2 AUSENTE (confirmado por ls); pr\u00e9-requisito duro antes de qualquer c\u00f3digo (Operator/Sequence/Verification/Recovery/Success); \u00edndice \u00a79 marca \ud83d\udd34 ABERTO"
  ],
  "gaps": [
    "09-pattern-conformance.md n\u00e3o existe no diret\u00f3rio \u2014 a Declara\u00e7\u00e3o dos 21 padr\u00f5es vive apenas em SDD \u00a79; o artefato standalone mandatado pelo Step 3.5 (forma exigida p/ \u22653 padr\u00f5es) n\u00e3o foi criado. A pr\u00f3pria su\u00edte (index [ ] PENDENTE + SDD 'ser\u00e1 promovida a 09-pattern-conformance.md') reconhece a obriga\u00e7\u00e3o em aberto.",
    "docs/processes/spaces-cadence.md (SOP Lei 2) n\u00e3o existe \u2014 Survival Law 2 bloqueia c\u00f3digo sem SOP; index Gate Status = \ud83d\udd34 ABERTO.",
    "Su\u00edte ainda em v0.1 DRAFT \u2014 Step 2 'revis\u00e3o Sovereign pendente' (n\u00e3o aprovado); status headers de todos os docs = 'Draft'.",
    "/security-review das 4 migrations pendente (FMEA-011) \u2014 index marca \ud83d\udd34 pendente; migrations 20260716120000/120100/120200/120300 n\u00e3o revisadas.",
    "Observa\u00e7\u00e3o (n\u00e3o-bloqueante): cobran\u00e7a documentada via begin/finalize (rail autopilot-cycle) em vez de deduct_mco_coins literal \u2014 correto no esp\u00edrito (RPC at\u00f4mica per-tenant, nunca client-side, n\u00f3 cobra 0/ciclo cobra), mas diverge da men\u00e7\u00e3o can\u00f4nica; conv\u00e9m nomear explicitamente qual RPC at\u00f4mica no passo 'generate'."
  ],
  "verdict": "BLOQUEADO \u2014 A SUBST\u00c2NCIA documental passa nos 5 checks de conte\u00fado (9 docs completos e rastre\u00e1veis; SDD \u00a79 carrega os 21 padr\u00f5es; FRs rastreiam blueprint\u2192data-model\u2192process-flow; REUSA autopilot/sequences/scheduled_posts sem reconstruir distribui\u00e7\u00e3o nem criar job pg_cron; BYOK per-user fail-closed 402 + ES256 JWKS + cobran\u00e7a at\u00f4mica per-tenant begin/finalize documentados). POR\u00c9M o gate Closed-Loop para INICIAR a Fatia 1 est\u00e1 fechado por 2 artefatos mandatados AUSENTES no disco (confirmado por ls), flagados pela pr\u00f3pria \u00a79 Gate Status da su\u00edte: (1) docs/bok/spaces-cadence/09-pattern-conformance.md (standalone exigido pelo Step 3.5 p/ m\u00f3dulo \u22653 padr\u00f5es \u2014 conte\u00fado pronto em SDD \u00a79, falta promover); (2) docs/processes/spaces-cadence.md (SOP Lei 2 \u2014 pr\u00e9-requisito duro antes de c\u00f3digo). Adicionalmente: su\u00edte em v0.1 DRAFT sem aprova\u00e7\u00e3o Sovereign (Step 2) e /security-review das 4 migrations pendente (FMEA-011). Destravar = criar os 2 arquivos + aprova\u00e7\u00e3o Sovereign do Step 2 + /security-review de cada migration; nenhuma linha de c\u00f3digo antes disso."
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-15 - agent-ac65645a66f3d1991]]
> * **Próxima Sessão**: [[2026-07-15 - agent-ad771ae3ac0da8ca7]]
%% --- TIMELINE END --- %%

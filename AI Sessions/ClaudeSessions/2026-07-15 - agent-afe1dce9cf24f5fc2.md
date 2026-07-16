# Session agent-afe1dce9cf24f5fc2
**Date:** 2026-07-15 | **Session ID:** `agent-afe1dce9cf24f5fc2`

---

## 👤 User *(18:07:26)*

Escreva a edge fn /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-plan/index.ts (FR-CAD-005): recebe JWT do usuário, faz upsert do plano de cadência em autopilot_plans (plan_kind='cadence' + recurrence/program/quiet_hours/channel_allowlist/budget_cap_mco), e ARMA next_run_at em UTC a partir do {frequency,days,hours,minutes,tz} (re-arm generalizado FR-CAD-007). Owner-scoped (auth.uid()). Sem cobrança (criar plano = 0 mco). CORS + erro estruturado PT-BR. Fundamente-se ESTRITAMENTE na BoK selada (Lei 1 — SSOT): /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/05-sdd.md (design + contratos + migrations stubs), /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/06-data-model.md (tabelas/RLS/índices), /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/07-process-flow.md (fluxos + recovery), /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/04-frd.md (FR-CAD-001..018 + aceite). Espelhe os PADRÕES VIVOS do repo (não reinvente): edge fns em supabase/functions/ (ver autopilot-run, canvas-execute, orchestrate-step p/ shape: CORS, JWT/ES256, RPC atômica, telemetria infra_health_logs); o tick vivo é a fn/cron 'autopilot-cadence-cron' (ache-a e ROTEIE por plan_kind — NENHUM job pg_cron novo, FR-CAD-004); scheduled_posts é o SINK (contrato metadata.reshape + schedule + publish_at). CONVENÇÕES: lógica/vars em inglês, UI/toasts PT-BR; BYOK per-user fail-closed 402/501; cobrança SÓ via deduct_mco_coins per-tenant; edge com pg_net → verify_jwt=false + ES256 JWKS (nunca atob cego); RLS default-deny owner-scoped; idempotência por índice único parcial. NÃO invente coluna/RPC que a SDD/data-model não declara — se faltar, deixe TODO explícito e cite o FR.
Baseie o shape em supabase/functions/autopilot-run e canvas-execute. Retorne path + 3 linhas + o contrato de request/response (p/ o cliente).

## 🤖 Claude *(18:07:30)*

<details>
<summary>💭 Thinking Process</summary>

I'm going to start by reviewing the BoK documentation and looking at the existing edge functions to understand the patterns I should follow.

</details>


## 🤖 Claude *(18:07:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/05-sdd.md"
}
```

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

## 🤖 Claude *(18:07:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/06-data-model.md"
}
```

## 🤖 Claude *(18:07:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/04-frd.md"
}
```

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

## 🤖 Claude *(18:07:35)*

<details>
<summary>💭 Thinking Process</summary>

I'm looking at the existing edge functions like autopilot-run, canvas-execute, autopilot-cadence-cron, and their shared helpers to understand the patterns I should follow.

</details>


## 🤖 Claude *(18:07:35)*

Now let me examine the living edge function patterns I must mirror.

## 🤖 Claude *(18:07:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/ | grep -Ei 'autopilot|cadence|_shared|canvas-execute|orchestrate-step'",
  "description": "List relevant edge function dirs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> autopilot-analyze
> autopilot-cadence-cron
> autopilot-collect
> autopilot-run
> canvas-execute
> orchestrate-step
> _shared
> ```

## 🤖 Claude *(18:07:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/ 2>/dev/null",
  "description": "List shared helpers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> affiliate.ts
> agent-metering.ts
> autopilot-video-cadence.test.ts
> autopilot-video-cadence.ts
> billing.test.ts
> billing.ts
> google-sa-auth.test.ts
> google-sa-auth.ts
> higgsfield-oauth.test.ts
> higgsfield-oauth.ts
> higgsfield-token.ts
> intent-policy.ts
> llm-fallback.test.ts
> llm-fallback.ts
> notify.ts
> oauth-state.ts
> provider-keys.test.ts
> provider-keys.ts
> public-url.test.ts
> public-url.ts
> reframe.ts
> sentinel.test.ts
> sentinel.ts
> smart-delete-classify.test.ts
> smart-delete-classify.ts
> social-app-config.ts
> tiktok-login-creds.ts
> tiktok-login-flow.ts
> ```

## 🤖 Claude *(18:07:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// autopilot-run — Viral Autopilot per-plan executor (FR-VA-002 / FR-VA-007 / FR-VA-016 / FR-VA-021). verify_jwt=false.
> 2	// SOP: docs/processes/autopilot-cron-identity.md.
> 3	//
> 4	// Identity (two paths):
> 5	//   - cron/service: Authorization === Bearer SB_SECRET_KEY + x-autopilot-user-id (the autopilot-cadence-cron
> 6	//     derived it from autopilot_plans.user_id). The header is re-validated by the TENANT-SCOPED plan load below.
> 7	//   - user "gerar agora": user JWT → getUser → the plan load is scoped to that user (IDOR-safe).
> 8	// Flow: load plan (tenant-scoped) → N_runs = products×platforms×ab_variants → projected = N_runs*10 + 2 →
> 9	//   begin_autopilot_cycle (ATOMIC cap-check + single pre-debit) → fan-out orchestrate-content (prepaid, no
> 10	//   self-bill) → finalize_autopilot_cycle(actual) → re-arm next_run_at. dry_run short-circuits after the cost
> 11	//   projection (no cycle, no deduct) — the zero-cost proof path.
> 12	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 13	import { inspectPrompt } from "../_shared/sentinel.ts";
> 14	import { resolveVideoCadence } from "../_shared/autopilot-video-cadence.ts";
> 15	
> 16	const corsHeaders = {
> 17	  "Access-Control-Allow-Origin": "*",
> 18	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 19	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-autopilot-user-id",
> 20	};
> 21	const ORCH_COST = 10;     // orchestrate-content flat bundle (image already included — billing.ts:16-21)
> 22	const ANALYZE_COST = 2;   // reserved for autopilot-analyze (R3); REFUNDED until that slice lands (see actual below)
> 23	const VIDEO_COST = 12;    // VIDEO_HYPERFRAMES_RENDER (billing.ts:39) — per video sub-run when plan.video_enabled (FR-VA-022/024)
> 24	const CONCURRENCY = 6;    // wall-clock bound on the fan-out (mirrors nurture-cron / campaign-run)
> 25	const UUID_RE = /^[0-9a-fA-F-]{36}$/;
> 26	
> 27	// ── FR-VA-018 trend hardening (adversarial review wf_6cc97c75 — MEDIUM, conf 8) ───────────────────────────────────
> 28	// vm_trends is a GLOBAL, externally-mined (Apify/RapidAPI), pt-BR catalog. The SHARED Cyber-Sentinel's
> 29	// INJECTION_PATTERNS are English-only/score>=2, so a Portuguese prompt-injection seeded into a viral upstream post
> 30	// passes it AND orchestrate-content's mirror gate, steering the content LLM (affiliate-link/scam-URL swap) for ANY
> 31	// autopilot tenant. This trend-SPECIFIC gate runs FIRST and is fail-closed: (1) a whitelist charset strip destroys
> 32	// the actual payloads (URLs, markdown links, tags, templates, quotes — only letters/digits/space/hyphen survive),
> 33	// (2) it rejects titles carrying instruction-override verbs (pt-BR + en), so what survives is an inert short keyword
> 34	// phrase rendered as DATA ("tema em alta: ..."), never free instruction text. The generic sentinel still runs after,
> 35	// as defense-in-depth. (Broader fix — pt-BR patterns in the shared sentinel — is deferred to the security arc with
> 36	// false-positive testing, since it affects every caller.)
> 37	const TREND_OVERRIDE_RE =
> 38	  /\b(ignor\w*|desconsider\w*|esque[cç]\w*|em\s+vez\s+disso|instead|disregard|override|nova\s+instru\w*|new\s+instruction|instruction\w*|prompt\w*|system\s*prompt|append|substitu\w*|replace|every\s+post|cada\s+post|todos\s+os\s+posts)\b/i;
> 39	function sanitizeTrendTitle(raw: string): string | null {
> 40	  // Whitelist: letters (incl. accented), digits, spaces, hyphen. Strips ./:@#[](){}<>`"'\| → kills URLs/markdown/tags.
> 41	  const cleaned = raw
> 42	    .replace(/[^\p{L}\p{N}\s-]/gu, " ")
> 43	    .replace(/\s+/g, " ")
> 44	    .trim();
> 45	  if (!cleaned) return null;
> 46	  if (TREND_OVERRIDE_RE.test(cleaned)) return null;   // fail-closed: instruction-override marker → skip this trend
> 47	  return cleaned.slice(0, 80).trim() || null;
> 48	}
> 49	
> 50	Deno.serve(async (req) => {
> 51	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 52	  const json = (b: unknown, s = 200) =>
> 53	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 54	
> 55	  const url = Deno.env.get("SUPABASE_URL")!;
> 56	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 57	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 58	  const admin = createClient(url, serviceKey);
> 59	  const logHealth = (status: string) =>
> 60	    admin.from("infra_health_logs").insert({ service: "autopilot-run", status }).then(() => {}, () => {});
> 61	
> 62	  try {
> 63	    const authHeader = req.headers.get("Authorization");
> 64	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 65	
> 66	    const body = await req.json().catch(() => ({}));
> 67	    const planId = typeof body?.plan_id === "string" ? body.plan_id : null;
> 68	    const dryRun = body?.dry_run === true;
> 69	    if (!planId || !UUID_RE.test(planId)) return json({ error: "plan_id (uuid) required" }, 422);
> 70	
> 71	    // ── Identity: service path (proven key + server-trusted header) OR user JWT path. ──────────────────────────
> 72	    const isService = authHeader === `Bearer ${serviceKey}`;
> 73	    let userId: string;
> 74	    if (isService) {
> 75	      const hdr = req.headers.get("x-autopilot-user-id");
> 76	      if (!hdr || !UUID_RE.test(hdr)) return json({ error: "x-autopilot-user-id (uuid) required for service path" }, 400);
> 77	      userId = hdr;
> 78	    } else {
> 79	      const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 80	      const { data: { user }, error } = await userClient.auth.getUser();
> 81	      if (error || !user) return json({ error: "Unauthorized" }, 401);
> 82	      userId = user.id;
> 83	    }
> 84	
> 85	    // ── Load plan TENANT-SCOPED (plan MUST belong to userId — cross-tenant/missing → 404). ───────────────────────
> 86	    const { data: plan } = await admin
> 87	      .from("autopilot_plans")
> 88	      .select("id, user_id, name, mode, interval_days, target_product_ids, platforms, ab_variants, video_enabled, video_format, video_every_n_cycles, budget_cap_mco, hitl_required")
> 89	      .eq("id", planId).eq("user_id", userId).maybeSingle();
> 90	    if (!plan) return json({ error: "plan_not_found" }, 404);
> 91	
> 92	    const products = ((plan.target_product_ids ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 93	    const rawPlatforms = ((plan.platforms ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 94	    // Fan-out hygiene (SOP autopilot-cron-identity Amendment 2026-07-02): only platforms with a real pipeline
> 95	    // step fan out (orchestrate-content stepsOrder — wordpress/linkedin/twitter; knowledge_mesh is a universal
> 96	    // fallback). A youtube/tiktok/pinterest/instagram sub-run would run knowledge_mesh only and still count
> 97	    // ORCH_COST in actual (charge-without-value); their distribution rides the reshaper off the wordpress
> 98	    // pillar's 9:16 master (FR-CP-003), not the fan-out.
> 99	    const FAN_OUT_PLATFORMS = new Set(["wordpress", "linkedin", "twitter"]);
> 100	    const platforms = rawPlatforms.filter((p) => FAN_OUT_PLATFORMS.has(p));
> 101	    const skippedPlatforms = rawPlatforms.filter((p) => !FAN_OUT_PLATFORMS.has(p));
> 102	    if (skippedPlatforms.length) {
> 103	      await admin.from("infra_health_logs").insert({
> 104	        service: "viral-autopilot", status: "degraded", event: "fanout_platform_skipped",
> 105	        metadata: { plan_id: planId, platforms: skippedPlatforms },
> 106	      }).then(() => {}, () => {});
> 107	    }
> 108	    const abVariants = Math.max(1, Math.min(5, Number(plan.ab_variants ?? 1)));
> 109	    const nRuns = products.length * platforms.length * abVariants;
> 110	    if (nRuns < 1) return json({ error: "plan_has_no_targets", detail: "plano sem produtos/redes válidos (redes fora do fan-out são distribuídas pelo reshaper)" }, 422);
> 111	
> 112	    // FR-VA-022/024 (Amendment v0.2): when the plan opts in, each sub-run enqueues ONE HyperFrames 9:16 render.
> 113	    // The cost rides on the cycle pre-debit (OTD-VA-010): projected/actual += N×VIDEO_COST. The render itself
> 114	    // never self-bills (charged_mco marker only); a FAILED render refunds via finalize_video_render.
> 115	    const videoEnabled = plan.video_enabled === true;
> 116	    const videoFormat = typeof plan.video_format === "string" ? plan.video_format : "9:16";
> 117	
> 118	    // Video charge accuracy (OTD-VA-010 follow-up — billing bug witnessed 2026-06-26, cycle 2403bfcb): a 9:16 render
> 119	    // is enqueued ONLY by the article_generation flow, which orchestrate-content runs solely for the 'wordpress'
> 120	    // platform (index.ts:231-232). A linkedin/twitter sub-run never reaches video_generation, so charging it
> 121	    // VIDEO_COST is charge-without-value — and uncaught by the orchestrate-step refund (orchestrate-step:454), which
> 122	    // fires only on a FAILED enqueue ATTEMPT, never for a flow that has no video step at all. So count video sub-runs
> 123	    // by the article-flow platform, not by every sub-run (was: nRuns × VIDEO_COST → over-charged non-wordpress runs).
> 124	    // FR-PE-013 (post-engine social-connect amendment) — DEFERRED: youtube/tiktok/pinterest ARE vertical-video
> 125	    // platforms, but the 9:16 render is enqueued ONLY by the article_generation step (gated on 'wordpress' above), and
> 126	    // autopilot fans out one platform per sub-run, so a youtube/tiktok/pinterest sub-run enqueues NO render. Adding
> 127	    // them here would charge VIDEO_COST with no video_renders row to refund (charge-without-value). Re-add ONLY with
> 128	    // the orchestrate-content/-step enqueue-gate extension (its own slice). Until then they stay out of the pre-debit.
> 129	    const VIDEO_FLOW_PLATFORMS = new Set(["wordpress"]);
> 130	    const videoPlatformCount = platforms.filter((p) => VIDEO_FLOW_PLATFORMS.has(p)).length;
> 131	    const nVideoRunsIfDue = products.length * videoPlatformCount * abVariants;
> 132	
> 133	    // Recurring video cadence (FR-VA-022 Amendment): decouple video frequency from the (text) cadence. Count this
> 134	    // plan's prior cycles → this cycle's ordinal; video fires only every Nth cycle (video_every_n_cycles) AND only
> 135	    // when it fits budget_cap_mco (graceful-degrade — video yields to the cap, NEVER aborts the text cycle). With
> 136	    // video_every_n_cycles=1 this is byte-identical to the prior "video_enabled every cycle" behavior.
> 137	    const videoEveryN = Math.max(1, Math.min(30, Number(plan.video_every_n_cycles ?? 1)));
> 138	    const budgetCap = Number(plan.budget_cap_mco ?? 0);
> 139	    const { count: priorCycleCount } = await admin
> 140	      .from("autopilot_cycles")
> 141	      .select("id", { count: "exact", head: true })
> 142	      .eq("plan_id", planId).eq("user_id", userId);
> 143	    const cadence = resolveVideoCadence({
> 144	      videoEnabled, videoEveryNCycles: videoEveryN, priorCycleCount: priorCycleCount ?? 0,
> 145	      nVideoRunsIfDue, projectedText: nRuns * ORCH_COST + ANALYZE_COST, videoCost: VIDEO_COST, budgetCapMco: budgetCap,
> 146	    });
> 147	    const videoDue = cadence.videoDue;
> 148	    const nVideoRuns = cadence.nVideoRuns;
> 149	    const projected = cadence.projected;
> 150	    // Surface the graceful-degrade: a too-tight cap silently dropping video must be observable, not a silent no-op.
> 151	    if (cadence.skipReason === "over_budget_cap") {
> 152	      await admin.from("infra_health_logs").insert({
> 153	        service: "viral-autopilot", status: "degraded", event: "video_skipped_over_cap",
> 154	        metadata: { plan_id: planId, budget_cap_mco: budgetCap, projected_video: nVideoRunsIfDue * VIDEO_COST, video_every_n_cycles: videoEveryN },
> 155	      }).then(() => {}, () => {});
> 156	    }
> 157	
> 158	    // ── FR-VA-018: trend-informed angle (cycle-level). Reconnects the trends island: pick a trend from vm_trends
> 159	    // (a GLOBAL shared catalog — no tenant scope) to steer THIS cycle's viral angle. Trend text is UNTRUSTED
> 160	    // (Apify/RapidAPI-mined) → the Cyber-Sentinel gates it BEFORE it reaches any prompt (NFR-VA-008), mirroring the
> 161	    // per-product gate in orchestrate-content (skip-and-continue: a blocked trend is dropped, not the whole angle).
> 162	    // Relevance: prefer a trend whose niche overlaps the cycle's products; else the freshest top-viral active trend.
> 163	    // Defense-in-depth: orchestrate-content re-inspects the full topic, so this is the first of two gates.
> 164	    // Graceful: empty vm_trends (the steady state until fetch-trends runs) → angle stays the plain product topic.
> 165	    let viralTopic = plan.name;
> 166	    let trendApplied: string | null = null;
> 167	    try {
> 168	      const { data: prodRows } = await admin
> 169	        .from("vm_affiliate_products").select("niches").in("external_id", products).eq("is_active", true);
> 170	      const productNiches = [...new Set(((prodRows ?? []) as Array<{ niches?: string[] | null }>)
> 171	        .flatMap((p) => p.niches ?? []).filter((n): n is string => typeof n === "string" && n.length > 0))];
> 172	      const fetchTrends = async (filterNiche: boolean) => {
> 173	        let q = admin.from("vm_trends").select("title, niche, viral_score")
> 174	          .eq("is_active", true).order("viral_score", { ascending: false }).limit(5);
> 175	        if (filterNiche && productNiches.length > 0) q = q.in("niche", productNiches);
> 176	        const { data } = await q;
> 177	        return (data ?? []) as Array<{ title: string | null; niche: string | null }>;
> 178	      };
> 179	      let candidates = await fetchTrends(true);
> 180	      if (candidates.length === 0) candidates = await fetchTrends(false);
> 181	      for (const t of candidates) {
> 182	        const clean = sanitizeTrendTitle(String(t.title ?? ""));
> 183	        if (!clean) { console.warn(`[autopilot-run] trend in niche '${t.niche}' rejected by trend gate (unsafe/empty) — skipped`); continue; }
> 184	        // Defense-in-depth: the generic Cyber-Sentinel still runs on the SANITIZED string we will interpolate.
> 185	        const v = inspectPrompt(clean, userId, { rateLimit: false });
> 186	        if (!v.allow) { console.warn(`[autopilot-run] trend in niche '${t.niche}' blocked by sentinel (${v.code}) — skipped`); continue; }
> 187	        trendApplied = clean;
> 188	        // Inert framing: the sanitized keyword is rendered as DATA ("tema em alta"), never as free instruction text.
> 189	        viralTopic = `${plan.name} (tema em alta: ${clean})`;
> 190	        break;
> 191	      }
> 192	    } catch (e) { console.warn(`[autopilot-run] trend angle skipped: ${e}`); }
> 193	
> 194	    // dry_run: return the cost projection (+ resolved trend angle) WITHOUT opening a cycle or deducting (zero-cost).
> 195	    if (dryRun) {
> 196	      return json({ ok: true, dry_run: true, n_runs: nRuns, projected_mco: projected,
> 197	        trend_applied: trendApplied, viral_topic: viralTopic,
> 198	        video: { enabled: videoEnabled, due: videoDue, every_n_cycles: videoEveryN, prior_cycles: priorCycleCount ?? 0, skip_reason: cadence.skipReason, format: videoFormat, cost_each: VIDEO_COST, n_video: nVideoRuns },
> 199	        breakdown: { products: products.length, platforms: platforms.length, ab_variants: abVariants } });
> 200	    }
> 201	
> 202	    // ── begin_autopilot_cycle: ATOMIC cap-check + single pre-debit (or abort reason, no deduct). ────────────────
> 203	    const { data: begun, error: beginErr } = await admin.rpc("begin_autopilot_cycle", {
> 204	      p_plan_id: planId, p_user_id: userId, p_projected_mco: projected, p_planned_units: nRuns,
> 205	    });
> 206	    if (beginErr) { logHealth("error"); return json({ error: "begin_failed", detail: beginErr.message }, 500); }
> 207	    if (!begun?.ok) {
> 208	      const reason = begun?.reason ?? "aborted";
> 209	      // Hard stop (budget too low / insufficient balance) → pause the plan so it stops re-firing every tick.
> 210	      if (reason === "aborted_budget" || reason === "insufficient_balance") {
> 211	        await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 212	      }
> 213	      logHealth("degraded");
> 214	      return json({ ok: false, reason, projected_mco: projected }, reason === "insufficient_balance" ? 402 : 409);
> 215	    }
> 216	    const cycleId = begun.cycle_id as string;
> 217	
> 218	    // ── R3 loop (FR-VA-010/011): analyze the PREVIOUS completed cycle to steer THIS cycle's generation. ─────────
> 219	    // collect (sync the live click ledger → creative_metrics) then analyze (→ optimization_policy). Both inline and
> 220	    // PREPAID — the cycle reserved ANALYZE_COST(2); analyzeCharged consumes it only when real data produced a policy
> 221	    // (else finalize refunds the 2). Best-effort — a missing/empty previous cycle just means no steering this round.
> 222	    let analyzeCharged = 0;
> 223	    const svcCall = (fn: string, payload: unknown) => fetch(`${url}/functions/v1/${fn}`, {
> 224	      method: "POST",
> 225	      headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 226	      body: JSON.stringify(payload),
> 227	    });
> 228	    try {
> 229	      const { data: prev } = await admin.from("autopilot_cycles")
> 230	        .select("id").eq("plan_id", planId).eq("user_id", userId).eq("status", "completed")
> 231	        .neq("id", cycleId).order("cycle_number", { ascending: false }).limit(1).maybeSingle();
> 232	      if (prev?.id) {
> 233	        await svcCall("autopilot-collect", { cycle_id: prev.id }).catch(() => {});
> 234	        const ar = await svcCall("autopilot-analyze", { previous_cycle_id: prev.id, prepaid: true })
> 235	          .then((r) => r.json()).catch(() => null);
> 236	        if (ar?.has_real_data) analyzeCharged = ANALYZE_COST;
> 237	      }
> 238	    } catch (e) { console.warn(`[autopilot-run] R3 analyze skipped: ${e}`); }
> 239	
> 240	    // ── Reallocation (FR-VA-030): bias the fan-out toward the policy winner, BUDGET-NEUTRAL (Σ variants stays nRuns
> 241	    // so the pre-debit holds). Winner product×platform gets +1 variant; the last non-winner pair gives up 1 (floor 1
> 242	    // = ε-greedy exploration — never collapse a pair to 0). No-op when ab_variants==1 (no room to move). The policy
> 243	    // is read scoped to THIS plan (mirrors the orchestrate-step fix). This is the lever: the policy now moves the
> 244	    // execution plan, not just the prompt hint.
> 245	    let winProd: string | null = null, winPlat: string | null = null;
> 246	    try {
> 247	      const { data: pol } = await admin.from("optimization_policy")
> 248	        .select("action_details").eq("user_id", userId).eq("action_type", "viral_autopilot")
> 249	        .eq("context->>scope", `viral_autopilot:${planId}`)
> 250	        .order("created_at", { ascending: false }).limit(1).maybeSingle();
> 251	      const ad = (pol as { action_details?: Record<string, unknown> } | null)?.action_details;
> 252	      winProd = (ad?.top_product_id as string) ?? null; winPlat = (ad?.top_platform as string) ?? null;
> 253	    } catch { /* policy read best-effort — never block the cycle */ }
> 254	
> 255	    const pairs: Array<{ product: string; platform: string; n: number }> = [];
> 256	    for (const productId of products) for (const platform of platforms) pairs.push({ product: productId, platform, n: abVariants });
> 257	    if (winProd && winPlat && abVariants >= 2) {
> 258	      const winner = pairs.find((p) => p.product === winProd && p.platform === winPlat);
> 259	      const donor = [...pairs].reverse().find((p) => !(p.product === winProd && p.platform === winPlat) && p.n > 1);
> 260	      if (winner && donor) { winner.n += 1; donor.n -= 1; }   // budget-neutral: Σ n stays = nRuns
> 261	    }
> 262	
> 263	    // ── Fan-out: (product × platform) × reallocated variants → orchestrate-content (prepaid → NO self-bill). ──────
> 264	    let succeeded = 0;
> 265	    let succeededVideo = 0;   // succeeded sub-runs whose flow enqueues a 9:16 render (article-flow / wordpress) — billing reconciliation
> 266	    const tasks: Array<() => Promise<void>> = [];
> 267	    for (const pair of pairs) {
> 268	      for (let v = 0; v < pair.n; v++) {
> 269	        tasks.push(async () => {
> 270	          try {
> 271	            const r = await fetch(`${url}/functions/v1/orchestrate-content`, {
> 272	              method: "POST",
> 273	              headers: {
> 274	                Authorization: `Bearer ${serviceKey}`,
> 275	                "x-autopilot-user-id": userId,
> 276	                "Content-Type": "application/json",
> 277	              },
> 278	              body: JSON.stringify({
> 279	                topic: viralTopic, platforms: [pair.platform], product_ids: [pair.product],
> 280	                prepaid: true, cycle_id: cycleId, wp_status: "draft",
> 281	                video_enabled: videoDue, video_format: videoFormat,
> 282	                // Publish opt-in (FR-CP-003): the autopilot auto-publishes UNLESS the plan requires human review.
> 283	                auto_publish: plan.hitl_required !== true,
> 284	              }),
> 285	            });
> 286	            if (r.ok) {
> 287	              succeeded++;
> 288	              if (videoDue && VIDEO_FLOW_PLATFORMS.has(pair.platform)) succeededVideo++;
> 289	            } else console.warn(`[autopilot-run] sub-run ${pair.product}/${pair.platform} → HTTP ${r.status}`);
> 290	          } catch (e) {
> 291	            console.warn(`[autopilot-run] sub-run ${pair.product}/${pair.platform} error: ${e}`);
> 292	          }
> 293	        });
> 294	      }
> 295	    }
> 296	    for (let i = 0; i < tasks.length; i += CONCURRENCY) {
> 297	      await Promise.all(tasks.slice(i, i + CONCURRENCY).map((t) => t()));
> 298	    }
> 299	
> 300	    // actual = successful runs × 10 + successful ARTICLE-FLOW runs × 12 (only those enqueue a render) + analyzeCharged.
> 301	    // Each succeeded article-flow sub-run enqueued one HyperFrames render (charged_mco marker, no self-bill); a FAILED
> 302	    // render later refunds its 12 via finalize_video_render. The reserved ANALYZE_COST(2) is consumed only when R3
> 303	    // produced a policy from real data; otherwise finalize refunds it. Zero successes → actual = analyzeCharged.
> 304	    const actual = succeeded * ORCH_COST + succeededVideo * VIDEO_COST + analyzeCharged;
> 305	    const status = succeeded > 0 ? "completed" : "failed";
> 306	    const { data: fin } = await admin.rpc("finalize_autopilot_cycle", {
> 307	      p_cycle_id: cycleId, p_actual_mco: actual, p_status: status,
> 308	    });
> 309	
> 310	    // ── Re-arm cadence (every_n_days) or deactivate after a single all_at_once run. ─────────────────────────────
> 311	    if (plan.mode === "every_n_days") {
> 312	      const days = Math.min(30, Math.max(1, Number(plan.interval_days ?? 3)));
> 313	      const next = new Date(Date.now() + days * 86_400_000).toISOString();
> 314	      await admin.from("autopilot_plans").update({ next_run_at: next }).eq("id", planId).eq("user_id", userId);
> 315	    } else {
> 316	      await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 317	    }
> 318	
> 319	    logHealth("healthy");
> 320	    return json({
> 321	      ok: true, cycle_id: cycleId, n_runs: nRuns, succeeded,
> 322	      projected_mco: projected, actual_mco: actual, refunded_mco: fin?.refunded ?? 0, status,
> 323	    });
> 324	  } catch (e) {
> 325	    logHealth("error");
> 326	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 327	  }
> 328	});
> 329	
> ```

## 🤖 Claude *(18:07:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-cadence-cron/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// autopilot-cadence-cron — Viral Autopilot pg_cron driver (FR-VA-005). verify_jwt=false.
> 2	// SOP: docs/processes/autopilot-cron-identity.md.
> 3	//
> 4	// Service-role driver (mirrors nurture-cron): self-checks Authorization === Bearer SB_SECRET_KEY, scans ACTIVE
> 5	// plans whose next_run_at has passed, and fans out to autopilot-run with the SERVER-TRUSTED user_id taken from
> 6	// the plan row (NEVER a request body). Each plan's spend is gated by begin_autopilot_cycle's caps inside
> 7	// autopilot-run. The pg_cron SCHEDULE that invokes this function is wired at activation time (Sovereign action).
> 8	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 9	
> 10	const corsHeaders = {
> 11	  "Access-Control-Allow-Origin": "*",
> 12	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 13	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 14	};
> 15	const MAX_PER_RUN = 50;   // cap per tick — no silent unbounded fan-out (logged if hit)
> 16	const CONCURRENCY = 6;    // wall-clock bound (mirrors nurture-cron)
> 17	
> 18	Deno.serve(async (req) => {
> 19	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 20	  const json = (b: unknown, s = 200) =>
> 21	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 22	
> 23	  const url = Deno.env.get("SUPABASE_URL")!;
> 24	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 25	  // Only the service-role holder (pg_cron presenting the Vault key) may run the cron.
> 26	  if (req.headers.get("Authorization") !== `Bearer ${serviceKey}`) return json({ error: "Forbidden" }, 403);
> 27	  const admin = createClient(url, serviceKey);
> 28	  const log = (status: string) =>
> 29	    admin.from("infra_health_logs").insert({ service: "autopilot-cadence-cron", status }).then(() => {}, () => {});
> 30	
> 31	  try {
> 32	    // due = active plans whose next_run_at has passed (served by the autopilot_plans_due_idx partial index).
> 33	    const { data: due, error } = await admin
> 34	      .from("autopilot_plans")
> 35	      .select("id, user_id")
> 36	      .eq("is_active", true)
> 37	      .not("next_run_at", "is", null)
> 38	      .lte("next_run_at", new Date().toISOString())
> 39	      .order("next_run_at", { ascending: true })
> 40	      .limit(MAX_PER_RUN);
> 41	    if (error) throw error;
> 42	    const list = (due ?? []) as Array<{ id: string; user_id: string }>;
> 43	    if (list.length === 0) { log("healthy"); return json({ status: "ok", due: 0, dispatched: 0, aborted: 0, errors: 0 }); }
> 44	
> 45	    const tally = { dispatched: 0, aborted: 0, errors: 0 };
> 46	    const one = async (p: { id: string; user_id: string }) => {
> 47	      try {
> 48	        const r = await fetch(`${url}/functions/v1/autopilot-run`, {
> 49	          method: "POST",
> 50	          headers: {
> 51	            Authorization: `Bearer ${serviceKey}`,
> 52	            "x-autopilot-user-id": p.user_id,   // server-trusted (from the plan row)
> 53	            "Content-Type": "application/json",
> 54	          },
> 55	          body: JSON.stringify({ plan_id: p.id }),
> 56	        });
> 57	        const d = await r.json().catch(() => ({}));
> 58	        if (d?.ok) tally.dispatched++;
> 59	        else if (d?.reason) tally.aborted++;   // cap/balance abort — expected, not an error
> 60	        else tally.errors++;
> 61	      } catch { tally.errors++; }
> 62	    };
> 63	    for (let i = 0; i < list.length; i += CONCURRENCY) await Promise.all(list.slice(i, i + CONCURRENCY).map(one));
> 64	
> 65	    if (list.length >= MAX_PER_RUN) console.warn(`[autopilot-cadence-cron] hit MAX_PER_RUN=${MAX_PER_RUN} — more plans may be due`);
> 66	    log("healthy");
> 67	    return json({ status: "ok", due: list.length, ...tally });
> 68	  } catch (e) {
> 69	    log("error");
> 70	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 71	  }
> 72	});
> 73	
> ```

## 🤖 Claude *(18:07:53)*

<details>
<summary>💭 Thinking Process</summary>

I'm looking at how ES256 JWT verification works in edge functions, particularly checking the pattern used in canvas-execute and similar user-facing functions. The documentation references edge-jwt-identity-verification.md and a test file for ES256 JWT verification, though I'm noticing that many of these functions actually rely on userClient.auth.getUser() to handle JWT validation server-side rather than doing it at the edge.

</details>


## 🤖 Claude *(18:07:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '1,90p' /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts",
  "description": "Read canvas-execute head"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.4";
> import { fetchLLMWithFallback } from "../_shared/llm-fallback.ts";
> import {
>   keyTelemetry,
>   listProviderKeyCandidates,
>   resolveProviderKey,
>   type ResolvedKey,
> } from "../_shared/provider-keys.ts";
> import { fetchPublicUrl } from "../_shared/public-url.ts";
> import { buildVertexUrl, getServiceAccountToken, parseServiceAccount } from "../_shared/google-sa-auth.ts";
> 
> const corsHeaders = {
>   "Access-Control-Allow-Origin": "*",
>   "Access-Control-Allow-Methods": "POST, OPTIONS",
>   "Access-Control-Allow-Headers":
>     "authorization, x-client-info, apikey, content-type",
> };
> 
> // ── Credit costs per operation (in mcoCoins) ─────────────────────────────
> // Aligned with .claude/context/higgsfield-api-validation-2026-05-15.md:
> // Higgsfield pricing is $1 = 16 credits; mcoCoins markup ~13x over USD cost.
> const CREDIT_COSTS: Record<string, number> = {
>   "openai/dall-e-3": 15,
>   "openai/gpt-image-1": 18,
>   "replicate/flux-1.1-pro": 12,
>   "replicate/sdxl": 4,
>   "replicate/flux-schnell": 3,
>   "openrouter/dall-e-3": 15,
>   "openrouter/google/gemini-2.5-flash-image": 10,
>   "openrouter/black-forest-labs/flux-1.1-pro": 12,
>   // Higgsfield Soul (text-to-image) — tiered by resolution × batch.
>   // "higgsfield/generate" kept as legacy alias → resolves to soul-1080p-1.
>   "higgsfield/generate": 40,
>   "higgsfield/soul-720p-1": 20,   // 1.5 hf credits ≈ $0.09
>   "higgsfield/soul-720p-4": 26,   // 2.0 hf credits ≈ $0.13
>   "higgsfield/soul-1080p-1": 40,  // 3.0 hf credits ≈ $0.19
>   "higgsfield/soul-1080p-4": 65,  // 5.0 hf credits ≈ $0.31
>   // Higgsfield DoP (image-to-video) — added in Phase 5.3 along with webhook flow.
>   "voice-over": 2,                    // Gemini 2.5 Flash TTS ≈ $0.005/run — 4x-floor (SOP 2c S27)
>   "higgsfield/dop-lite-5s": 30,       // placeholder; 2 hf credits ≈ $0.13
>   "higgsfield/dop-turbo-5s": 90,      // placeholder; 6.5 hf credits ≈ $0.41
>   "higgsfield/dop-standard-5s": 125,  // placeholder; 9 hf credits ≈ $0.56
>   // Kling 2.1 Pro pricing not tabulated by Higgsfield; placeholder, confirm via Cloud Dashboard.
>   "higgsfield/kling-2.1-pro-5s": 160,
>   "higgsfield/seedance-v1-pro-5s": 130,
>   "upscale-2x": 8,
>   "upscale-4x": 20,
>   "inpaint": 6,
>   // Compose engine = Nano Banana multimodal (Amendment 2d-bis 2026-07-03) — same engine as
>   // the 10-mco image row above (~$0.04 output + negligible image inputs; 4×-floor ⇒ 10).
>   // The old 18 priced a Higgsfield endpoint that never existed upstream.
>   "scene-compose": 10,
>   // it.2a: PINNED style_transfer price, aligned with the live legacy debit (the UI's forged
>   // higgsfield/soul payload resolves soul-720p-1 = 20 there; the old 14 under-quoted it). The
>   // ledger branch pins the ENGINE to the multimodal restyle path (Nano Banana consumes the source
>   // image — soul t2i ignored it) at this same declared price, so quote == charge in every window.
>   "style-transfer": 20,
>   "remove-background": 3,
> };
> 
> // ── Veo 3.1 (Amendment 25, FR-SPACES-086/089) ────────────────────────────────
> // Contract pinned by live probe (.claude/context/veo-31-contract-probe-2026-07-14.md):
> // durationSeconds int 4..8 · aspectRatio {9:16,16:9} · resolution {720p,1080p} (1080p ⇒ 8s only)
> // · referenceImages ≤ 3 {image:{bytesBase64Encoded,mimeType}, referenceType:"asset"}.
> // Pricing (ai.google.dev/gemini-api/docs/pricing, fetched 2026-07-14) → 4×-floor calibration
> // (docs/processes/mcoin-cost-calibration.md): mco = ceil(usd / 0.018 × 4). Anchors at 8s:
> // lite-720p 89 · fast-720p 178 · fast-1080p 214 · standard 712.
> const VEO_PER_SEC_USD: Record<string, Record<string, number>> = {
>   "veo-3.1": { "720p": 0.40, "1080p": 0.40 },
>   "veo-3.1-fast": { "720p": 0.10, "1080p": 0.12 },
>   "veo-3.1-lite": { "720p": 0.05, "1080p": 0.08 },
> };
> const VEO_API_MODEL: Record<string, string> = {
>   "veo-3.1": "veo-3.1-generate-preview",
>   "veo-3.1-fast": "veo-3.1-fast-generate-preview",
>   "veo-3.1-lite": "veo-3.1-lite-generate-preview",
> };
> // Amendment 26 (FR-SPACES-095): Vertex AI GA — preço fast US$0,15/s (mais caro que a Gemini API
> // 0,10), nomes de modelo `-001`, e NÃO tem tier lite. Fonte: gerar_cenas_qa.py PRECO_POR_SEGUNDO.
> const VEO_VERTEX_PER_SEC_USD: Record<string, Record<string, number>> = {
>   "veo-3.1": { "720p": 0.40, "1080p": 0.40 },
>   "veo-3.1-fast": { "720p": 0.15, "1080p": 0.15 },
> };
> const VEO_VERTEX_API_MODEL: Record<string, string> = {
>   "veo-3.1": "veo-3.1-generate-001",
>   "veo-3.1-fast": "veo-3.1-fast-generate-001",
> };
> const VEO_MAX_REFERENCE_IMAGES = 3;          // probe C5: "Number of reference images can not exceed 3."
> const VEO_REF_DOWNLOAD_CAP_BYTES = 15 * 1024 * 1024; // same sanity ceiling as the reframe motor
> ```

## 🤖 Claude *(18:07:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rl \"getUser\\|verifyEs256\\|jwks\\|JWKS\" /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/ | head; echo ---; grep -rn \"verify_jwt\" /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml | grep -Ei 'canvas-execute|cadence|autopilot-run' ",
  "description": "Find JWT verification patterns and config"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/check-video-status/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/analyze-node/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/campaign-run/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/trigger-embeddings/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-space-asset/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/openrouter-swarm/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/agent-task-execute/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/create-checkout/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/higgsfield-oauth-init/index.ts
> ---
> ```

## 🤖 Claude *(18:08:01)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking how JWT verification works in the user-facing functions—specifically whether `verify_jwt=false` with ES256 JWKS verification is actually secure when compared to direct Supabase auth calls like `userClient.auth.getUser()`. I need to trace through canvas-execute and campaign-run to understand their identity verification patterns and determine if cadence-plan requires the same `verify_jwt=false` configuration.

</details>


## 🤖 Claude *(18:08:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"getUser\\|auth.getUser\\|Unauthorized\\|createClient\\|authHeader\\|user.id\\|SB_PUBLISHABLE\\|SUPABASE_ANON\" /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts | head -40",
  "description": "Find canvas-execute identity block"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 2:import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.4";
> 184:    const authHeader = req.headers.get("Authorization");
> 185:    if (!authHeader) {
> 192:    const supabaseAnonKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 193:    const supabase = createClient(supabaseUrl, supabaseAnonKey, {
> 194:      global: { headers: { Authorization: authHeader } },
> 197:    const { data: { user }, error: authError } = await supabase.auth.getUser();
> 199:      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 213:    const admin = createClient(supabaseUrl, (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!);
> 217:      .from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 225:    const googlePool = await resolveProviderKey(admin, user.id, "google", body.provider_key_id);
> 269:      return await executeSpacesNode({ admin, user, body, keys, creditCost, corsHeaders, supabaseUrl, authHeader });
> 274:      .from("profiles").select("mco_balance").eq("id", user.id).single();
> 284:    const capResp = await enforceDailyCanvasCap(admin, user.id, creditCost, corsHeaders);
> 350:        user_id: user.id,
> 397:                .eq("user_id", user.id)
> 444:          p_user_id: user.id,
> 564:          const fileName = `${user.id}/${execution.id}.${ext}`;
> 596:          user_id: user.id,
> 599:          storage_key: storedKey ?? `${user.id}/${execution.id}.png`,
> 621:          p_user_id: user.id,
> 624:          p_storage_key: storedKey ?? `${user.id}/${execution.id}.png`,
> 666:        p_user_id: user.id,
> 723:  authHeader: string;
> 788:    .eq("user_id", userId)
> 806:    .eq("user_id", userId)
> 922:  authHeader: string;
> 924:  const { admin, body, corsHeaders, creditCost, generationId, supabaseUrl, authHeader } = o;
> 947:  const anonKey = Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY") ?? "";
> 955:          Authorization: authHeader,
> 1550:      .from("spaces").select("id").eq("id", body.space_id).eq("owner_id", user.id).maybeSingle();
> 1556:      .from("vm_canvas_projects").select("id").eq("id", body.project_id).eq("user_id", user.id).maybeSingle();
> 1624:    .from("profiles").select("mco_balance").eq("id", user.id).single();
> 1633:  const capResp = await enforceDailyCanvasCap(admin, user.id, effectiveCost, corsHeaders);
> 1654:    p_owner_id: user.id,
> 1698:      authHeader: ctx.authHeader,
> 1707:    const candidates = await listProviderKeyCandidates(admin, user.id, "google", body.provider_key_id);
> 1733:          ? await resolveProjectCampaignContext(admin, user.id, body.project_id)
> 1852:    await spacesFirstRunObservation(admin, user.id, (body.space_id ?? body.project_id)!, body.space_id ? "space_id" : "project_id");
> 1879:      const fileName = `${user.id}/spaces/${generationId}.${ext}`;
> ```

## 🤖 Claude *(18:08:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"cadence\\|canvas-execute\\|autopilot-run\\|autopilot-cadence-cron\\|verify_jwt\" /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml | head -40",
  "description": "Check config.toml verify_jwt blocks"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 7:verify_jwt = false
> 9:verify_jwt = false
> 11:verify_jwt = false
> 13:verify_jwt = false
> 15:verify_jwt = false
> 17:verify_jwt = false
> 19:verify_jwt = false
> 21:verify_jwt = false
> 23:verify_jwt = false
> 25:verify_jwt = false
> 27:verify_jwt = false
> 29:verify_jwt = false
> 31:verify_jwt = false
> 32:[functions.autopilot-run]
> 33:verify_jwt = false
> 34:[functions.autopilot-cadence-cron]
> 35:verify_jwt = false
> 37:verify_jwt = false
> 39:verify_jwt = false
> 41:verify_jwt = false
> 43:verify_jwt = false
> 45:verify_jwt = false
> 47:verify_jwt = false
> 49:verify_jwt = false
> 51:verify_jwt = false
> 53:verify_jwt = false
> 55:verify_jwt = false
> 57:verify_jwt = false
> 59:verify_jwt = false
> 61:verify_jwt = false
> 63:verify_jwt = false
> 65:verify_jwt = false
> 67:verify_jwt = false
> 69:verify_jwt = false
> 71:verify_jwt = false
> 73:verify_jwt = false
> 75:verify_jwt = false
> 78:verify_jwt = true
> 83:verify_jwt = false
> 86:verify_jwt = false
> ```

## 🤖 Claude *(18:08:14)*

<details>
<summary>💭 Thinking Process</summary>

Looking at how canvas-execute handles authentication, it follows the standard Supabase pattern with `getUser()` on the anon key client, which validates the JWT signature server-side through a network call to the auth server. This is the secure verification approach the task is asking me to mirror.

Since cadence-plan is user-facing with the JWT coming from the UI and no charging involved, I need to focus on writing the edge function in index.ts using this same pattern. I should also check the config.toml structure to add the cadence-plan block with `verify_jwt=false`, since the getUser pattern requires the JWT to reach the function rather than being pre-validated by the gateway.

</details>


## 🤖 Claude *(18:08:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '1,90p' /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml",
  "description": "Read config.toml verify_jwt blocks"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> project_id = "bcyvddsykvehvpwstlfa"
> 
> # Configuração de Bypass de JWT para Orquestração Soberana
> # key-migration 2026-06-01: service→service targets are called with the new sb_secret_ key (not a JWT),
> # so the gateway JWT check must be off; each function below enforces its own in-code auth gate.
> [functions.publish-social]
> verify_jwt = false
> [functions.check-post-existence]
> verify_jwt = false
> [functions.delete-remote-post]
> verify_jwt = false
> [functions.refresh-social-token]
> verify_jwt = false
> [functions.embed-mcorch-node]
> verify_jwt = false
> [functions.self-optimize]
> verify_jwt = false
> [functions.self-heal]
> verify_jwt = false
> [functions.orchestrate-content]
> verify_jwt = false
> [functions.orchestrate-step]
> verify_jwt = false
> [functions.reshape-pillar]
> verify_jwt = false
> [functions.generate-carousel]
> verify_jwt = false
> [functions.nurture-dispatch]
> verify_jwt = false
> [functions.nurture-cron]
> verify_jwt = false
> [functions.autopilot-run]
> verify_jwt = false
> [functions.autopilot-cadence-cron]
> verify_jwt = false
> [functions.autopilot-analyze]
> verify_jwt = false
> [functions.autopilot-collect]
> verify_jwt = false
> [functions.collect-publication-metrics]
> verify_jwt = false
> [functions.video-render]
> verify_jwt = false
> [functions.video-render-poll]
> verify_jwt = false
> [functions.intent-orchestrate]
> verify_jwt = false
> [functions.intent-execute]
> verify_jwt = false
> [functions.aeo-audit]
> verify_jwt = false
> [functions.generate-content]
> verify_jwt = false
> [functions.generate-audio-script]
> verify_jwt = false
> [functions.generate-video-script]
> verify_jwt = false
> [functions.list-provider-models]
> verify_jwt = false
> [functions.generate-video]
> verify_jwt = false
> [functions.check-video-status]
> verify_jwt = false
> [functions.generate-image]
> verify_jwt = false
> [functions.generate-voice]
> verify_jwt = false
> [functions.avatar-consent]
> verify_jwt = false
> [functions.erase-avatar-artifacts]
> verify_jwt = false
> [functions.analyze-seo]
> verify_jwt = false
> [functions.publish-wordpress]
> verify_jwt = false
> [functions.sync-knowledge-mesh]
> enabled = true
> verify_jwt = true
> import_map = "./functions/sync-knowledge-mesh/deno.json"
> entrypoint = "./functions/sync-knowledge-mesh/index.ts"
> 
> [functions.higgsfield-webhook]
> verify_jwt = false
> 
> [functions.handle-ml-postback]
> verify_jwt = false
> 
> [functions.process-affiliate-link]
> verify_jwt = false
> ```

## 🤖 Claude *(18:08:51)*

<details>
<summary>💭 Thinking Process</summary>

I need to figure out how to handle the timezone-aware recurrence calculation. The spec requires converting a recurrence pattern with frequency, days, hours, minutes, and timezone into a next_run_at timestamp in UTC. Looking at the existing code, there's no timezone helper yet—just simple interval addition. I'll need to build out the UTC conversion logic that computes the next occurrence in the specified IANA timezone and then converts it back to UTC.

Writing the timezone conversion helper... Writing timezone conversion logic... Mapping JavaScript's day numbering to the 1=Mon..7=Sun format, then iterating forward from today's local date to find the first candidate that matches the recurrence constraints (weekday for weekly, day-of-month for monthly) and has a UTC timestamp after now. I'll iterate up to around 430 days to safely handle edge cases like the 31st of each month, and validate that minutes are multiples of 5.

Now I'm checking the channel allowlist validation — the SDD specifies that channels must be a subset of the auto-publish allowlist minus some exclusions, returning a 422 error if a channel isn't available for that cadence. Since I don't have a hardcoded list of supported channels, I'll validate structurally (non-empty array of strings) and exclude the specified channels. I'm setting up channel validation to reject Twitter/X per the compliance requirement and enforce a non-empty allowlist, then I'll add a TODO to wire in the full channel profiles enum once it's properly defined in the data model.

</details>


## 🤖 Claude *(18:08:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rhoE \"platform[s]?['\\\"]?\\s*[:=]\\s*['\\\"][a-z]+['\\\"]\" /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts 2>/dev/null | sort -u | head; echo \"=== auto-publish channel refs ===\"; grep -nE \"wordpress|linkedin|twitter|instagram|pinterest|youtube|tiktok|telegram\" /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts 2>/dev/null | head -20",
  "description": "Find auto-publish supported channels"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === auto-publish channel refs ===
> ```

## 🤖 Claude *(18:08:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"id, user_id\\|UNIQUE (id, user_id)\\|autopilot_plans\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/ 2>/dev/null | grep -i \"unique\\|create table\" | grep -i autopilot | head",
  "description": "Check autopilot_plans unique(id,user_id) existence"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql:18:CREATE TABLE IF NOT EXISTS public.autopilot_plans (
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql:40:  CONSTRAINT autopilot_plans_id_user_uniq UNIQUE (id, user_id)
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120100_viral_autopilot_cycles.sql:33:  CONSTRAINT autopilot_cycles_id_user_uniq    UNIQUE (id, user_id),
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260716120000_cadence_recurrence.sql:88:  -- if plan_id is guessed. Anchors on autopilot_plans UNIQUE(id,user_id) [constraint autopilot_plans_id_user_uniq,
> ```

## 🤖 Claude *(18:09:02)*

<details>
<summary>💭 Thinking Process</summary>

I see there's already a migration file for cadence recurrence, so I need to check what columns are actually defined in the autopilot_plans table and whether the cadence columns have been applied. Let me look at that migration to understand the exact column names and types I'll be working with.

</details>


## 🤖 Claude *(18:09:02)*

A cadence migration already exists. Let me read it to bind to the exact column names.

## 🤖 Claude *(18:09:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '1,140p' /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260716120000_cadence_recurrence.sql",
  "description": "Read the cadence migration for exact schema"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -- Migration: spaces-cadence Fatia 1 — recurrence engine on the LIVING rails (FR-CAD-002 / FR-CAD-003).
> -- BoK SSOT (Lei 1 — no invention beyond the sealed suite):
> --   docs/bok/spaces-cadence/05-sdd.md §2.5/§7.1/§7.2/§5.2 (design + contracts + migration stubs)
> --   docs/bok/spaces-cadence/06-data-model.md §2.1/§2.2/§3.1/§3.2 (columns/RLS/indexes/composite FK)
> --   docs/bok/spaces-cadence/04-frd.md (FR-CAD-002/003/004/006 + acceptance)
> --
> -- MANDATE OF INTEGRATION (the dogma): Cadence FITS the living rails and does NOT rebuild distribution.
> --   * autopilot_plans is EXTENDED (plan_kind='cadence') — NO parallel plan table, NO 3rd driver (OTD-CAD-003).
> --   * The live tick fn/cron 'autopilot-cadence-cron' routes by plan_kind (viral->autopilot-run |
> --     cadence->cadence-run) — NO new pg_cron job (FR-CAD-004).
> --   * scheduled_posts is the one-shot SINK (metadata.reshape + schedule + publish_at) drained by auto-publish.
> --
> -- ORO triplet — Operator: MCORCH Master Execution Agent · Reviewer: Sovereign (Gabriel) ·
> --   Owner: Sovereign (blast radius: Meta/X app ban from 1-tenant spam + ANPD sanction up to 2% revenue).
> --
> -- SECURITY: passes /security-review before commit (NO EXCEPTIONS — FMEA-011 cross-tenant leak family).
> --   No new SQL function is defined here (the erase_lead() cascade is a SEPARATE migration per SDD §7.3,
> --   20260716120200_erase_lead_cascade_cadence.sql) — the reused update_updated_at_column() already carries
> --   its own SET search_path from its own migration. Any function this suite adds later MUST use search_path=''.
> --
> -- Engineering note (divergence from the sealed §7.1 stub, declared per Lei 1 / Materiality):
> --   budget_cap_mco ALREADY EXISTS on autopilot_plans (viral-autopilot base migration 20260620120000,
> --   NOT NULL CHECK budget_cap_mco >= 12). The SDD §7.1 stub lists it as an ADD COLUMN, but re-adding a live
> --   column would fail (42701). We therefore ADD COLUMN IF NOT EXISTS: the pre-existing NOT NULL column is
> --   REUSED unchanged. Cadence's data-quality rule "budget_cap_mco > 0 when plan_kind='cadence'" (FR-CAD-011)
> --   is satisfied a fortiori by the live >= 12 floor and is enforced at the edge with a 422 (never client-side).
> 
> -- ─────────────────────────────────────────────────────────────────────────────────────────────────────────
> -- PART 1 — EXTEND autopilot_plans (REUSA-ESTENDE — FR-CAD-002 / OTD-CAD-003)
> -- ALTER only; the owner-scoped RLS already on autopilot_plans is PRESERVED (no policy recreated).
> -- Existing plan_kind='viral' plans stay valid (mode/interval_days/daily_cap/is_active/next_run_at intact).
> -- ─────────────────────────────────────────────────────────────────────────────────────────────────────────
> 
> ALTER TABLE public.autopilot_plans
>   -- allowlist stops being a hardcoded subset CHECK; it derives from channel_profiles/channel_allowlist.
>   DROP CONSTRAINT IF EXISTS autopilot_plans_platforms_check,
>   -- the tick routes by this column (FR-CAD-004): viral->autopilot-run | cadence->cadence-run.
>   ADD COLUMN IF NOT EXISTS plan_kind text NOT NULL DEFAULT 'viral'
>       CHECK (plan_kind IN ('viral','cadence')),
>   -- {frequency:'daily'|'weekly'|'monthly', days:int[], hours:int, minutes:int (multiple of 5), tz:IANA};
>   -- next_run_at is computed in UTC on the server (FR-CAD-007 / FM-CAD-06).
>   ADD COLUMN IF NOT EXISTS recurrence        jsonb,
>   -- {start, end, days:int[]} in the SUBJECT's timezone (FR-CAD-008 / gate G3).
>   ADD COLUMN IF NOT EXISTS quiet_hours       jsonb,
>   -- previous cycle still running => skip, never stack (FM-CAD-01).
>   ADD COLUMN IF NOT EXISTS overlap_policy    text DEFAULT 'skip',
>   -- caps the backlog after downtime (FM-CAD-07).
>   ADD COLUMN IF NOT EXISTS catchup_window    interval DEFAULT '6 hours',
>   -- anti-thundering-herd on the fan-out (FM-CAD-07).
>   ADD COLUMN IF NOT EXISTS jitter_seconds    int DEFAULT 0,
>   -- steps publish|wait|throttle|digest|branch — mold of sequences.steps + current_step (P1/P6), not a new format.
>   ADD COLUMN IF NOT EXISTS program           jsonb,
>   -- channels PER PLAN (subset of auto-publish allowlist MINUS X in Fatia 1 — OTD-CAD-011); not a constant.
>   ADD COLUMN IF NOT EXISTS channel_allowlist text[],
>   -- budget cap in mcoCoins (never USD); cadence requires > 0, enforced at the edge with 422 (FR-CAD-011).
>   -- PRE-EXISTS from viral-autopilot (NOT NULL CHECK >= 12) — IF NOT EXISTS reuses it unchanged (see note above).
>   ADD COLUMN IF NOT EXISTS budget_cap_mco    int NOT NULL DEFAULT 0;
> 
> COMMENT ON COLUMN public.autopilot_plans.plan_kind IS
>   'spaces-cadence FR-CAD-002/004: viral (legacy) | cadence. The live autopilot-cadence-cron tick routes by this.';
> COMMENT ON COLUMN public.autopilot_plans.recurrence IS
>   'spaces-cadence FR-CAD-007: {frequency,days,hours,minutes(mult of 5),tz(IANA)}; next_run_at computed in UTC.';
> COMMENT ON COLUMN public.autopilot_plans.channel_allowlist IS
>   'spaces-cadence OTD-CAD-011: per-plan channel subset (auto-publish allowlist MINUS X in Fatia 1).';
> 
> -- ─────────────────────────────────────────────────────────────────────────────────────────────────────────
> -- PART 2 — cadence_dispatches (NOVO — FR-CAD-003 / FM-CAD-01)
> -- Per-attempt dispatch ledger. NOT append-only pure (OTD-CAD-006): status transitions => service-role UPDATE.
> -- The partial unique index is what ACTUALLY prevents double-post (failure RELEASES the key / success LOCKS it).
> -- ─────────────────────────────────────────────────────────────────────────────────────────────────────────
> 
> CREATE TABLE IF NOT EXISTS public.cadence_dispatches (
>   id                uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id           uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,  -- tenant isolation; RLS = auth.uid()
>   plan_id           uuid        NOT NULL,                    -- origin plan (composite FK below is the tenant guard)
>   step_index        int         NOT NULL,                    -- program step (idempotency-key component)
>   occurrence_at     timestamptz NOT NULL,                    -- due instant (idempotency-key component)
>   idempotency_key   text        NOT NULL,                    -- stable hash of (plan_id, step_index, occurrence_at)
>   channel           text        NOT NULL,                    -- dispatch channel (in the plan's channel_allowlist)
>   status            text        NOT NULL DEFAULT 'queued',   -- queued|publishing|sent|failed (TRANSITIONS)
>   target_ref        text,                                    -- scheduled_posts.id / external id (1:1 with the sink)
>   external_usd_cost numeric,                                 -- BYOK external cost, written ON RECONCILE, never on the 202 (FM-CAD-05)
>   cost_source       text,                                    -- cost origin ('meta_ai_provider_br','x_post_url', ...)
>   error             text,                                    -- failure reason ('erased' on the LGPD cascade)
>   created_at        timestamptz NOT NULL DEFAULT now(),
>   updated_at        timestamptz NOT NULL DEFAULT now(),
>   -- TENANT-SCOPED COMPOSITE FK (data-model §3.2): forbids a dispatch pointing at another tenant's plan even
>   -- if plan_id is guessed. Anchors on autopilot_plans UNIQUE(id,user_id) [constraint autopilot_plans_id_user_uniq,
>   -- already live] — same pattern as autopilot_cycles/creative_metrics/campaign_steps.
>   CONSTRAINT cadence_dispatches_plan_fk
>     FOREIGN KEY (plan_id, user_id)
>     REFERENCES public.autopilot_plans (id, user_id) ON DELETE CASCADE
> );
> 
> -- Idempotency (FM-CAD-01/03): partial UNIQUE — failure RELEASES the key (retry), success LOCKS it (anti double-post).
> -- Paired with `INSERT ... ON CONFLICT DO NOTHING RETURNING` in cadence-run.
> CREATE UNIQUE INDEX IF NOT EXISTS cadence_dispatches_idem
>   ON public.cadence_dispatches (idempotency_key)
>   WHERE status <> 'failed';
> 
> -- Drain-by-plan index (data-model §3.2): scan a plan's due/in-flight dispatches.
> CREATE INDEX IF NOT EXISTS cadence_dispatches_plan_status_idx
>   ON public.cadence_dispatches (plan_id, status);
> 
> -- RLS: default-deny. Client READS own rows; NEVER writes (status/cost transition only via service-role reconcile).
> ALTER TABLE public.cadence_dispatches ENABLE ROW LEVEL SECURITY;
> 
> -- SELECT own only. No INSERT/UPDATE policy for authenticated => denied by default-deny; the client can never
> -- forge status='sent' nor external_usd_cost. service_role bypasses RLS and writes status/error/cost on reconcile.
> CREATE POLICY "cadence_dispatches_select_own"
>   ON public.cadence_dispatches
>   FOR SELECT
>   USING (user_id = auth.uid());
> 
> -- updated_at audit on every status transition (reuses the shared trigger fn).
> CREATE TRIGGER set_cadence_dispatches_updated_at
>   BEFORE UPDATE ON public.cadence_dispatches
>   FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 
> COMMENT ON TABLE public.cadence_dispatches IS
>   'spaces-cadence FR-CAD-003: per-attempt dispatch ledger. NOT append-only (OTD-CAD-006) — status transitions '
>   '(queued|publishing|sent|failed) via service-role. Partial UNIQUE(idempotency_key) WHERE status<>''failed'' is '
>   'what prevents double-post (FM-CAD-01). Tenant-scoped composite FK (plan_id,user_id)->autopilot_plans(id,user_id). '
>   'RLS select_own; INSERT/UPDATE service-role only. external_usd_cost/cost_source written on reconcile, never the 202.';
> ```

## 🤖 Claude *(18:09:23)*

<details>
<summary>💭 Thinking Process</summary>

The migration confirms the columns exist, and `budget_cap_mco` has a NOT NULL constraint with a CHECK >= 12. Since the database enforces a floor of 12, I need to make sure the edge validation doesn't allow values that would violate this—if I only check > 0 at the API level, something like 5 would slip through and fail at the database layer.

The FRD specifies > 0, but the actual database floor is >= 12. I'll validate > 0 as the FRD requires, but I'll also catch any database constraint violations during insert/upsert and map them to a clean 422 response instead of letting a 500 bubble up.

Now I need to figure out the upsert logic—what's the conflict target? The request doesn't include a planId according to the SDD contract, but the inspector stores one in the data. So when re-arming, how do I identify which existing plan to update?

Looking at it more carefully: if a planId is provided in the request, I should update that specific plan (owner-scoped); otherwise, insert a new one. I'll add an optional planId field to the request contract to support this, which aligns with CadenceData already having that field. Before implementing the INSERT, I need to check which columns in the autopilot_plans table are NOT NULL so I can ensure I'm supplying all required values.

</details>


## 🤖 Claude *(18:09:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '18,70p' /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql",
  "description": "Read autopilot_plans base columns/NOT NULL"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> CREATE TABLE IF NOT EXISTS public.autopilot_plans (
>   id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id            uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   project_id         uuid,
>   name               text        NOT NULL,
>   mode               text        NOT NULL CHECK (mode IN ('all_at_once','every_n_days')),
>   interval_days      int         DEFAULT 3 CHECK (interval_days IS NULL OR (interval_days BETWEEN 1 AND 30)),
>   target_product_ids text[]      NOT NULL CHECK (array_length(target_product_ids, 1) >= 1),
>   platforms          text[]      NOT NULL CHECK (array_length(platforms, 1) >= 1
>                                    AND platforms <@ ARRAY['wordpress','linkedin','twitter']),
>   budget_cap_mco     int         NOT NULL CHECK (budget_cap_mco  >= 12),  -- >= 1 cycle (1 run 10 + analyze 2)
>   daily_cap_mco      int         NOT NULL DEFAULT 200 CHECK (daily_cap_mco >= 12),
>   min_balance_mco    int         NOT NULL DEFAULT 10  CHECK (min_balance_mco >= 0),
>   hitl_required      boolean     NOT NULL DEFAULT false,
>   ab_variants        int         NOT NULL DEFAULT 1   CHECK (ab_variants BETWEEN 1 AND 5),
>   is_active          boolean     NOT NULL DEFAULT false,
>   next_run_at        timestamptz,
>   created_at         timestamptz NOT NULL DEFAULT now(),
>   updated_at         timestamptz NOT NULL DEFAULT now(),
>   -- mode every_n_days REQUIRES interval_days (Data Quality §6).
>   CONSTRAINT autopilot_plans_interval_req CHECK (mode <> 'every_n_days' OR interval_days IS NOT NULL),
>   -- anchor for the tenant-scoped composite FK from autopilot_cycles (id,user_id).
>   CONSTRAINT autopilot_plans_id_user_uniq UNIQUE (id, user_id)
> );
> 
> ALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;
> 
> CREATE POLICY "autopilot_plans_select_own" ON public.autopilot_plans
>   FOR SELECT USING (auth.uid() = user_id);
> CREATE POLICY "autopilot_plans_insert_own" ON public.autopilot_plans
>   FOR INSERT WITH CHECK (auth.uid() = user_id);
> CREATE POLICY "autopilot_plans_update_own" ON public.autopilot_plans
>   FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> -- Clients can NEVER delete a plan (RESTRICTIVE forbids it even if a permissive policy is later added);
> -- only service-role (LGPD cascade) removes.
> CREATE POLICY "autopilot_plans_no_client_delete" ON public.autopilot_plans
>   AS RESTRICTIVE FOR DELETE USING (false);
> 
> -- Due-plan scan index (cron): active plans whose next_run_at has passed.
> CREATE INDEX IF NOT EXISTS autopilot_plans_due_idx  ON public.autopilot_plans (next_run_at) WHERE is_active;
> CREATE INDEX IF NOT EXISTS autopilot_plans_user_idx ON public.autopilot_plans (user_id, created_at DESC);
> 
> CREATE TRIGGER set_autopilot_plans_updated_at
>   BEFORE UPDATE ON public.autopilot_plans
>   FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 
> COMMENT ON TABLE public.autopilot_plans IS
>   'Viral Autopilot cadence config per user (FR-VA-001/005). Mandatory safety caps (budget/daily/min_balance) — '
>   'the cron never runs without a kill-switch. SELECT/INSERT/UPDATE own, RESTRICTIVE no client delete. '
>   'UNIQUE(id,user_id) anchors the tenant-scoped composite FK from autopilot_cycles. SOP autopilot-cron-identity.md.';
> ```

## 🤖 Claude *(18:09:49)*

<details>
<summary>💭 Thinking Process</summary>

I'm running into a schema mismatch with the cadence plan insertion constraints. The base table requires `target_product_ids` to be non-null with at least one element, but cadence plans don't actually target products—they target creative assets instead. This is a fundamental conflict between what the schema enforces and what the cadence feature actually needs.

Looking at the migration that dropped the platforms check constraint, I realize it removed both the length validation and the subset validation in one go. Now `platforms` is still NOT NULL but has no CHECK constraints, so it can be an empty array `'{}'` as long as it's not null. The same pattern applies to `target_product_ids`—the check constraint that enforces `array_length >= 1` is named something like `autopilot_plans_target_product_ids_check`, and if that gets dropped, the column becomes nullable in terms of content even though it's still NOT NULL in type.

The real problem is that cadence plans don't have a `sourceAssetId` column in the schema, yet the data model says the subject should be a creative asset ID. I need to figure out where this is actually stored or if there's a gap in how cadence data maps to the existing autopilot columns like `target_product_ids`. The model traceability indicates the creative asset is subject-scoped and reused across cadences, but doesn't specify which column holds it. Since there's no declared column for sourceAssetId and I need a working solution, I'll store it within the program jsonb alongside the steps — treating it as metadata for the cadence program itself rather than inventing a new column.

</details>


## 🤖 Claude *(18:09:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rln \"autopilot_plans\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/ | sort | tail -5; echo \"=== alters to target_product_ids/platforms/mode after cadence ===\"; grep -rn \"target_product_ids\\|ALTER COLUMN\\|DROP CONSTRAINT\\|source_asset\\|subject\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/2026071*_cadence*.sql /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/2026072*.sql 2>/dev/null | head",
  "description": "Check later autopilot_plans alterations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120200_begin_autopilot_cycle.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260624130000_autopilot_video_plan_columns.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260702150000_autopilot_reward_weights.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260705120000_autopilot_video_cadence.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260716120000_cadence_recurrence.sql
> === alters to target_product_ids/platforms/mode after cadence ===
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260716120000_cadence_recurrence.sql:36:  DROP CONSTRAINT IF EXISTS autopilot_plans_platforms_check,
> ```

## 🤖 Claude *(18:11:06)*

<details>
<summary>💭 Thinking Process</summary>

The migration didn't relax the NOT NULL constraints on `target_product_ids`, `mode`, or `platforms`, so when inserting cadence plan records, I still need to satisfy those legacy requirements. For `name`, I can derive it from something like the asset identifier, and for `mode`, I'll pull the value from the cadence record itself since it has a NOT NULL CHECK constraint limiting it to either 'all_at_once' or 'every_n_days'.

Since cadence uses recurrence rather than interval_days, I need to set `interval_days` to a valid placeholder (1-30) to satisfy the constraint that comes with mode='every_n_days'. The real blocker is `target_product_ids` — it requires at least one element, but cadence records have no associated products, and there's no source_asset_id column to work with. This is a genuine gap between the sealed suite's design and the living table's constraints, and the migration didn't provide a way to relax this requirement.

Following the instruction not to invent columns, I'll store the sourceAssetId in the `program` jsonb field instead, since that's the declared location for plan steps and a publish step naturally references the asset being published.

For the legacy `target_product_ids` constraint, I'll fill it with the sourceAssetId as a workaround and add a TODO noting the schema tension — the data model expects creative_assets as the subject for cadence plans, but the sealed column is locked to product IDs. A future migration should either relax this constraint for cadence plans or add a proper source_asset_id column. set in the existing plan, so I can't just leave them NULL. The task spec explicitly lists which columns to populate—plan_kind, recurrence, program, quiet_hours, channel_allowlist, budget_cap_mco—but doesn't mention target_product_ids, platforms, or mode, yet those have NOT NULL constraints. For an upsert on an existing plan, those fields are already populated, so I need to preserve them rather than overwrite with placeholder values. The platforms check was removed in the migration, so I can safely use channel_allowlist even though there's no length validation—but since channel_allowlist is required to be non-empty by my validation, that's fine. For the legacy filler, I'm torn between storing the subject directly in program versus keeping the caller's program intact and embedding source_asset_id within it. If I overwrite program with the subject, I'd lose any steps they provided, so it's better to preserve their program (defaulting to a minimal publish step if needed) and store the source asset ID canonically within the program structure itself. For the mode field, I need to pick between 'all_at_once' and 'every_n_days'. Since this is a recurring cadence, 'every_n_days' makes more sense semantically, even though it requires setting interval_days—I'll use 1 as a valid default. The actual re-arming happens through the recurrence logic in cadence-run, not interval_days, so I'll note that as a TODO.

For the upsert logic, the UPDATE path should only touch cadence-specific columns plus next_run_at and is_active, scoped by user and plan kind, while the INSERT path creates the full row. On activation: arming a plan means scheduling it, so it needs to be is_active=true so the autopilot-cadence-cron picks it up—unlike viral plans which default inactive and require separate activation, cadence arming should directly activate the plan.

I'll map the request's enabled field (defaulting to true since the user clicked "Armar") to is_active, using the logic is_active = enabled !== false for safety. Then I need to build the timezone-aware calculator for next_run_at and handle the projected_cost_mco field.

For projected_cost_mco, the SDD indicates the inspector computes this per FR-CAD-011, but since I don't have a per-channel cost table declared here, I'll use a conservative best-effort projection based on the number of channels as a fallback for the response contract. The real issue is that the authoritative per-cycle mco projection should come from the inspector's cost estimation logic, not from this edge function. I'll return `projected_cost_mco` as `budget_cap_mco` for now with a TODO noting that the true projection belongs in the client-side inspector implementation.

For the request contract, I'll accept an optional `projectedCostMco` field that the client can compute and pass through, defaulting to 0 if not provided. This way I'm echoing back what the client calculated while acknowledging that the server-side source of truth for per-channel mco costs needs to be established later.

The cadence-plan itself doesn't need to run inspectPrompt since it only contains asset IDs and numeric recurrence values, no free-text prompts to validate.

For the 402 error (provider not configured), creating a plan requires no provider at all—it's keyless with zero mco cost—so there's no provider resolution step needed in the first phase. That keeps things simple.

On validation, I need to verify that the sourceAssetId is a required string and that it belongs to the requesting user by checking against the creative_assets table's ownership column. For recurrence, I'm validating the frequency type (daily/weekly/monthly), hour range (0-23), minutes (0-59 in 5-minute increments), day arrays based on frequency, and timezone strings.

The other required fields include budget_cap_mco as a positive integer with a database floor of 12, channel_allowlist as a non-empty array that explicitly rejects X/Twitter per the spec, and several optional fields like quiet_hours, overlap_policy, catchup_window, jitter_seconds, and program array.

</details>


## 🤖 Claude *(18:11:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"CREATE TABLE.*creative_assets\\|owner_id\\|user_id\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/*creative_assets*.sql 2>/dev/null | head; echo \"=== any creative_assets create ===\"; grep -rln \"CREATE TABLE public.creative_assets\\|CREATE TABLE IF NOT EXISTS public.creative_assets\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/ | head",
  "description": "Find creative_assets owner column"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql:18:  p_user_id          uuid,
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql:48:  IF p_user_id IS NULL OR p_storage_bucket IS NULL OR p_storage_key IS NULL THEN
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql:49:    RAISE EXCEPTION 'register_creative_asset: user_id, storage_bucket, storage_key required' USING errcode = '22023';
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql:60:    user_id, org_id, kind, storage_bucket, storage_key, is_public, mime_type, file_size_bytes,
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql:64:    p_user_id, p_org_id, p_kind, p_storage_bucket, p_storage_key, p_is_public, p_mime_type, p_file_size_bytes,
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql:80:  WHERE public.creative_assets.user_id = EXCLUDED.user_id
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260707230000_creative_assets_allow_spaces_source.sql:24:  p_user_id          uuid,
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260707230000_creative_assets_allow_spaces_source.sql:54:  IF p_user_id IS NULL OR p_storage_bucket IS NULL OR p_storage_key IS NULL THEN
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260707230000_creative_assets_allow_spaces_source.sql:55:    RAISE EXCEPTION 'register_creative_asset: user_id, storage_bucket, storage_key required' USING errcode = '22023';
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260707230000_creative_assets_allow_spaces_source.sql:65:    user_id, org_id, kind, storage_bucket, storage_key, is_public, mime_type, file_size_bytes,
> === any creative_assets create ===
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260625120000_creative_assets_registry.sql
> ```

## 🤖 Claude *(18:11:39)*

<details>
<summary>💭 Thinking Process</summary>

I'm verifying ownership by checking both the asset ID and user ID in the creative_assets table. Now I need to write the edge function and add the config.toml settings for cadence-plan with JWT verification disabled, then cross-check my UTC calculation logic against the process flow documentation for the re-arm flow.

I'm implementing the index.ts file following the same pattern as autopilot-run, using the esm.sh client, CORS headers, and JSON helpers. For the re-arm UTC calculator, I'll build a `computeNextRunAt` function that handles the recurrence logic: for weekly schedules, I'll map the recurrence days (1=Monday through 7=Sunday) to JavaScript's day-of-week values, then iterate forward from the current date to find the next matching candidate date within the timezone context.

Writing the re-arm calculator... Writing timezone conversion functions... Writing scheduling logic... I need to handle timezone validation by wrapping the Intl check in a try-catch, then cascade through rec.tz, profiles.timezone, and finally default to 'America/Sao_Paulo' if needed. I'll query the profiles table to get the user's timezone and guard against missing or invalid values.

Now I'm writing out the full implementation covering validation, timezone resolution, next_run_at calculation, the upsert logic for insert versus update, telemetry tracking, and the response structure.

</details>


## 🤖 Claude *(18:11:39)*

I have enough grounding. Writing the edge function now.

## 🤖 Claude *(18:13:06)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-plan/index.ts",
  "content": "// cadence-plan \u2014 spaces-cadence Fatia 1 arm endpoint (FR-CAD-005 + FR-CAD-007). verify_jwt=false.\n//\n// BoK SSOT (Lei 1 \u2014 no invention beyond the sealed suite):\n//   docs/bok/spaces-cadence/05-sdd.md  \u00a72.3/\u00a73.1/\u00a74 (design + API contract for POST /cadence-plan)\n//   docs/bok/spaces-cadence/06-data-model.md \u00a72.1/\u00a73.1 (autopilot_plans columns + tenancy)\n//   docs/bok/spaces-cadence/07-process-flow.md (arm flow + recovery)\n//   docs/bok/spaces-cadence/04-frd.md  FR-CAD-005 (arm) + FR-CAD-007 (generalized UTC re-arm)\n//\n// RESPONSIBILITY (FR-CAD-005): receive a USER JWT, upsert the cadence plan into autopilot_plans\n//   (plan_kind='cadence' + recurrence/program/quiet_hours/channel_allowlist/budget_cap_mco), and ARM\n//   next_run_at in UTC computed from {frequency,days,hours,minutes,tz} (FR-CAD-007 generalized re-arm).\n//   Owner-scoped (auth.uid()). Creating a plan costs 0 mco (the node does not generate \u2014 SDD \u00a74;\n//   the G7 quote==charge invariant belongs to the CYCLE begin/finalize, never to the arm).\n//\n// IDENTITY (SDD \u00a75.3): user-facing endpoint. This function is registered verify_jwt=false in config.toml\n//   (the sovereign-orchestration bypass block), so identity is verified IN-FUNCTION via the Supabase auth\n//   server (supabase.auth.getUser with an anon-key client bound to the caller's Authorization header \u2014 the\n//   SAME living pattern as canvas-execute:184-211 / autopilot-run:78-83). getUser() validates the JWT\n//   signature server-side (it is NOT a blind atob of the token). user_id is server-trusted from the verified\n//   claim, NEVER from the request body. Cron callers (Bearer SB_SECRET_KEY) are rejected 403 \u2014 this endpoint\n//   is arm-only (the drain/dispatch live in cadence-run, invoked by the tick).\n//\n// MANDATE OF INTEGRATION: extends the LIVING rail autopilot_plans (no parallel table, no new pg_cron job).\n//   The live autopilot-cadence-cron tick routes due plans by plan_kind \u2192 cadence-run (FR-CAD-004).\n\nimport { createClient } from \"https://esm.sh/@supabase/supabase-js@2\";\n\nconst corsHeaders = {\n  \"Access-Control-Allow-Origin\": \"*\",\n  \"Access-Control-Allow-Methods\": \"POST, OPTIONS\",\n  \"Access-Control-Allow-Headers\": \"authorization, x-client-info, apikey, content-type\",\n};\n\nconst UUID_RE = /^[0-9a-fA-F-]{36}$/;\nconst DEFAULT_TZ = \"America/Sao_Paulo\";        // final fallback of the fuso cascade (FR-CAD-007)\nconst FREQUENCIES = new Set([\"daily\", \"weekly\", \"monthly\"]);\n// Fatia 1 (OTD-CAD-011): X/Twitter is OUT of the cadence allowlist until the pay-per-use probe closes\n// (Post-with-link = 45 mco, a Sovereign-gated Console action). Reject it at the edge with a 422.\nconst X_CHANNELS = new Set([\"x\", \"twitter\"]);\n\n// \u2500\u2500 UTC re-arm calculator (FR-CAD-007 / FM-CAD-06) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n// The cron runs in GMT and NEVER carries a time-of-day preference: the subject's wall-clock time in its IANA\n// timezone is converted to a UTC instant and stored in next_run_at. Deno has no tz library, so DST-correct\n// conversion is done with Intl.DateTimeFormat offsets (the well-known zoned-time \u2192 UTC algorithm).\n\n// Offset (ms) such that local = utc + offset, at a given instant, for a timezone.\nfunction tzOffsetMs(instant: Date, tz: string): number {\n  const dtf = new Intl.DateTimeFormat(\"en-US\", {\n    timeZone: tz, hourCycle: \"h23\",\n    year: \"numeric\", month: \"2-digit\", day: \"2-digit\",\n    hour: \"2-digit\", minute: \"2-digit\", second: \"2-digit\",\n  });\n  const p: Record<string, string> = {};\n  for (const { type, value } of dtf.formatToParts(instant)) p[type] = value;\n  const asUTC = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second);\n  return asUTC - instant.getTime();\n}\n\n// A wall-clock (y,mo,d,h,mi) in `tz` \u2192 the UTC instant it denotes (refined once across DST boundaries).\nfunction zonedWallToUtc(y: number, mo: number, d: number, h: number, mi: number, tz: string): Date {\n  const wallAsUtc = Date.UTC(y, mo, d, h, mi, 0);\n  const off = tzOffsetMs(new Date(wallAsUtc), tz);\n  let ts = wallAsUtc - off;\n  const off2 = tzOffsetMs(new Date(ts), tz);\n  if (off2 !== off) ts = wallAsUtc - off2;   // DST fold/gap refinement\n  return new Date(ts);\n}\n\n// The caller's local calendar date \"today\" in `tz`.\nfunction localYmd(instant: Date, tz: string): { y: number; mo: number; d: number } {\n  const dtf = new Intl.DateTimeFormat(\"en-US\", {\n    timeZone: tz, year: \"numeric\", month: \"2-digit\", day: \"2-digit\",\n  });\n  const p: Record<string, string> = {};\n  for (const { type, value } of dtf.formatToParts(instant)) p[type] = value;\n  return { y: +p.year, mo: +p.month - 1, d: +p.day };\n}\n\n// ISO weekday 1=Mon..7=Sun for a calendar date (tz-independent given Y-M-D).\nfunction isoDow(y: number, mo: number, d: number): number {\n  const js = new Date(Date.UTC(y, mo, d)).getUTCDay();   // 0=Sun..6=Sat\n  return js === 0 ? 7 : js;\n}\n\ninterface Recurrence {\n  frequency: \"daily\" | \"weekly\" | \"monthly\";\n  days: number[];        // weekly: ISO weekdays 1=Mon..7=Sun \u00b7 monthly: days-of-month 1..31 \u00b7 daily: ignored\n  hours: number;         // 0..23\n  minutes: number;       // 0..59, multiple of 5 (Knock semantics)\n  tz: string;            // IANA\n}\n\n// Next occurrence strictly after `from`, as a UTC Date. Scans \u2264 430 calendar days (covers monthly day-31).\nfunction computeNextRunAt(rec: Recurrence, from: Date): Date | null {\n  const { y, mo, d } = localYmd(from, rec.tz);\n  const base = Date.UTC(y, mo, d);   // local \"today\" midnight as a pure-calendar anchor\n  for (let i = 0; i <= 430; i++) {\n    const cand = new Date(base + i * 86_400_000);\n    const cy = cand.getUTCFullYear(), cmo = cand.getUTCMonth(), cd = cand.getUTCDate();\n    let match = false;\n    if (rec.frequency === \"daily\") match = true;\n    else if (rec.frequency === \"weekly\") match = rec.days.includes(isoDow(cy, cmo, cd));\n    else if (rec.frequency === \"monthly\") match = rec.days.includes(cd);\n    if (!match) continue;\n    const utc = zonedWallToUtc(cy, cmo, cd, rec.hours, rec.minutes, rec.tz);\n    if (utc.getTime() > from.getTime()) return utc;\n  }\n  return null;\n}\n\nfunction isValidTz(tz: unknown): tz is string {\n  if (typeof tz !== \"string\" || !tz) return false;\n  try { new Intl.DateTimeFormat(\"en-US\", { timeZone: tz }); return true; } catch { return false; }\n}\n\nDeno.serve(async (req) => {\n  if (req.method === \"OPTIONS\") return new Response(\"ok\", { headers: corsHeaders });\n  // Structured errors (PT-BR message for the UI toast; English code/vars per code standards).\n  const json = (b: unknown, s = 200) =>\n    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, \"Content-Type\": \"application/json\" } });\n  const fail422 = (field: string, message: string) => json({ error: \"validation_failed\", field, message }, 422);\n\n  const url = Deno.env.get(\"SUPABASE_URL\")!;\n  const serviceKey = (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!;\n  const pubKey = (Deno.env.get(\"SB_PUBLISHABLE_KEY\") ?? Deno.env.get(\"SUPABASE_ANON_KEY\"))!;\n  const admin = createClient(url, serviceKey);\n  const logHealth = (status: string, event?: string, metadata?: Record<string, unknown>) =>\n    admin.from(\"infra_health_logs\")\n      .insert({ service: \"spaces-cadence\", status, ...(event ? { event } : {}), ...(metadata ? { metadata } : {}) })\n      .then(() => {}, () => {});\n\n  try {\n    // \u2500\u2500 Identity (SDD \u00a75.3): user JWT only. Cron key is rejected \u2014 arm is user-facing. \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n    const authHeader = req.headers.get(\"Authorization\");\n    if (!authHeader?.startsWith(\"Bearer \")) return json({ error: \"Unauthorized\" }, 401);\n    if (authHeader === `Bearer ${serviceKey}`) return json({ error: \"Forbidden\" }, 403); // cron path is cadence-run\n\n    const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });\n    const { data: { user }, error: authErr } = await userClient.auth.getUser();\n    if (authErr || !user) return json({ error: \"Unauthorized\" }, 401);\n    const userId = user.id;   // server-trusted from the verified claim, never from the body\n\n    const body = await req.json().catch(() => ({}));\n\n    // \u2500\u2500 planId (optional): present \u21d2 UPDATE (re-arm) an owner-scoped cadence plan; absent \u21d2 INSERT a new one. \u2500\n    const planId = typeof body?.planId === \"string\" ? body.planId : null;\n    if (planId && !UUID_RE.test(planId)) return fail422(\"planId\", \"Identificador de plano inv\u00e1lido.\");\n\n    // \u2500\u2500 sourceAssetId: cadence subject (creative_assets.id, owner-scoped, existing asset \u21d2 0 mco keyless). \u2500\u2500\u2500\n    const sourceAssetId = typeof body?.sourceAssetId === \"string\" ? body.sourceAssetId : null;\n    if (!sourceAssetId || !UUID_RE.test(sourceAssetId)) {\n      return fail422(\"sourceAssetId\", \"Selecione um criativo de origem para a cad\u00eancia.\");\n    }\n    const { data: asset } = await admin\n      .from(\"creative_assets\").select(\"id\").eq(\"id\", sourceAssetId).eq(\"user_id\", userId).maybeSingle();\n    if (!asset) return fail422(\"sourceAssetId\", \"Criativo de origem n\u00e3o encontrado.\");\n\n    // \u2500\u2500 recurrence: required + validated (computed in UTC on the server \u2014 FR-CAD-007). \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n    const rec = body?.recurrence;\n    if (!rec || typeof rec !== \"object\") return fail422(\"recurrence\", \"Configure a recorr\u00eancia da cad\u00eancia.\");\n    if (!FREQUENCIES.has(rec.frequency)) return fail422(\"recurrence.frequency\", \"Frequ\u00eancia inv\u00e1lida (di\u00e1ria, semanal ou mensal).\");\n    const hours = Number(rec.hours);\n    if (!Number.isInteger(hours) || hours < 0 || hours > 23) return fail422(\"recurrence.hours\", \"A hora deve estar entre 0 e 23.\");\n    const minutes = Number(rec.minutes);\n    if (!Number.isInteger(minutes) || minutes < 0 || minutes > 59) return fail422(\"recurrence.minutes\", \"Os minutos devem estar entre 0 e 59.\");\n    if (minutes % 5 !== 0) return fail422(\"recurrence.minutes\", \"Os minutos devem ser m\u00faltiplos de 5.\");\n    const days = Array.isArray(rec.days) ? rec.days.map((n: unknown) => Number(n)) : [];\n    if (rec.frequency === \"weekly\") {\n      if (days.length === 0 || days.some((d: number) => !Number.isInteger(d) || d < 1 || d > 7)) {\n        return fail422(\"recurrence.days\", \"Selecione os dias da semana (1=segunda \u2026 7=domingo).\");\n      }\n    } else if (rec.frequency === \"monthly\") {\n      if (days.length === 0 || days.some((d: number) => !Number.isInteger(d) || d < 1 || d > 31)) {\n        return fail422(\"recurrence.days\", \"Selecione os dias do m\u00eas (1 a 31).\");\n      }\n    }\n\n    // fuso cascade (FR-CAD-007): recurrence.tz \u2192 profiles.timezone \u2192 America/Sao_Paulo.\n    let tz: string;\n    if (isValidTz(rec.tz)) {\n      tz = rec.tz;\n    } else {\n      let profileTz: string | null = null;\n      try {\n        const { data: prof } = await admin.from(\"profiles\").select(\"timezone\").eq(\"id\", userId).maybeSingle();\n        profileTz = (prof as { timezone?: string | null } | null)?.timezone ?? null;\n      } catch { /* profiles.timezone best-effort \u2014 cascade falls through to default */ }\n      tz = isValidTz(profileTz) ? profileTz! : DEFAULT_TZ;\n    }\n\n    const recurrence: Recurrence = { frequency: rec.frequency, days, hours, minutes, tz };\n\n    // \u2500\u2500 budget_cap_mco: NOT NULL, in mcoCoins (never USD); cadence requires > 0 (FR-CAD-011). \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n    // NOTE: the live autopilot_plans column carries a DB CHECK (budget_cap_mco >= 12) from the viral base\n    // migration (20260620120000). We validate > 0 per the FRD literal here; a value in 1..11 would still be\n    // rejected by the DB CHECK and is mapped to a clean 422 on the write below (never a raw 500).\n    const budgetCapMco = Number(body?.budget_cap_mco ?? body?.budgetCapMco);\n    if (!Number.isInteger(budgetCapMco) || budgetCapMco <= 0) {\n      return fail422(\"budget_cap_mco\", \"Defina um teto de or\u00e7amento em mcoCoins para a cad\u00eancia (maior que zero).\");\n    }\n\n    // \u2500\u2500 channel_allowlist: per-plan, non-empty; X excluded in Fatia 1 (OTD-CAD-011). \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n    // TODO(FR-CAD-002 / OTD-CAD-011): the authoritative \"auto-publish allowlist MINUS X\" is not declared as a\n    // constant in the sealed SDD/data-model (channel_allowlist is per-plan, not a hardcoded set). We enforce\n    // non-empty + X-excluded here; the full channel_profiles-derived membership check is deferred to the\n    // channel_profiles.cadence reader (FR-CAD-008) rather than invented as a literal list.\n    const rawChannels = Array.isArray(body?.channel_allowlist) ? body.channel_allowlist\n      : Array.isArray(body?.channelAllowlist) ? body.channelAllowlist : null;\n    if (!rawChannels || rawChannels.length === 0 || rawChannels.some((c: unknown) => typeof c !== \"string\" || !c)) {\n      return fail422(\"channel_allowlist\", \"Selecione ao menos um canal para a cad\u00eancia.\");\n    }\n    const channels = [...new Set((rawChannels as string[]).map((c) => c.toLowerCase()))];\n    const blockedX = channels.filter((c) => X_CHANNELS.has(c));\n    if (blockedX.length) return fail422(\"channel_allowlist\", \"O canal X/Twitter n\u00e3o est\u00e1 dispon\u00edvel nesta cad\u00eancia.\");\n\n    // \u2500\u2500 optional fields (defaults mirror the migration column defaults). \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n    const quietHours = body?.quiet_hours ?? body?.quietHours ?? null;\n    if (quietHours !== null && typeof quietHours !== \"object\") return fail422(\"quiet_hours\", \"Hor\u00e1rio de sil\u00eancio inv\u00e1lido.\");\n    const overlapPolicy = body?.overlap_policy === \"skip\" || body?.overlapPolicy === \"skip\" ? \"skip\" : \"skip\"; // only 'skip' in Fatia 1\n    const catchupWindow = typeof body?.catchup_window === \"string\" ? body.catchup_window\n      : typeof body?.catchupWindow === \"string\" ? body.catchupWindow : \"6 hours\";\n    const jitterRaw = Number(body?.jitter_seconds ?? body?.jitterSeconds ?? 0);\n    const jitterSeconds = Number.isInteger(jitterRaw) && jitterRaw >= 0 ? jitterRaw : 0;\n    const program = Array.isArray(body?.program) ? body.program : null;\n    // Client-computed per-cycle projection (FR-CAD-011 \u2014 the inspector owns the per-channel mco projection;\n    // the per-channel mco SSOT is not in this BoK doc). Echoed back for display; TODO move the projection\n    // server-side once a per-channel cost table is declared. Never charged (0 mco at arm).\n    const projectedCostMco = Number.isFinite(Number(body?.projectedCostMco)) ? Number(body.projectedCostMco) : 0;\n\n    // \u2500\u2500 ARM next_run_at in UTC (FR-CAD-007). \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n    const nextRun = computeNextRunAt(recurrence, new Date());\n    if (!nextRun) return fail422(\"recurrence\", \"N\u00e3o foi poss\u00edvel calcular a pr\u00f3xima execu\u00e7\u00e3o para esta recorr\u00eancia.\");\n    const nextRunAt = nextRun.toISOString();\n\n    // enabled (CadenceData.enabled): arming activates the plan so the live tick picks it up. Default true\n    // (the operator clicked \"Armar\"); pass enabled:false to arm without activating.\n    const isActive = body?.enabled !== false;\n\n    // Cadence-specific write payload (the columns the task/SDD enumerate).\n    const cadenceCols = {\n      plan_kind: \"cadence\" as const,\n      recurrence,\n      quiet_hours: quietHours,\n      overlap_policy: overlapPolicy,\n      catchup_window: catchupWindow,\n      jitter_seconds: jitterSeconds,\n      program,\n      channel_allowlist: channels,\n      budget_cap_mco: budgetCapMco,\n      next_run_at: nextRunAt,\n      is_active: isActive,\n    };\n\n    let resultPlanId: string;\n\n    if (planId) {\n      // \u2500\u2500 UPDATE path (re-arm): owner-scoped, cadence-only. RLS also enforces user_id = auth.uid(). \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n      const { data: upd, error: updErr } = await admin\n        .from(\"autopilot_plans\")\n        .update(cadenceCols)\n        .eq(\"id\", planId).eq(\"user_id\", userId).eq(\"plan_kind\", \"cadence\")\n        .select(\"id\").maybeSingle();\n      if (updErr) {\n        if (updErr.code === \"23514\") return fail422(\"budget_cap_mco\", \"O teto de or\u00e7amento n\u00e3o atende ao m\u00ednimo do plano.\"); // DB CHECK\n        logHealth(\"error\", \"cadence_arm_update_failed\", { plan_id: planId, code: updErr.code });\n        return json({ error: \"arm_failed\", detail: updErr.message }, 500);\n      }\n      if (!upd) return json({ error: \"plan_not_found\" }, 404);\n      resultPlanId = upd.id;\n    } else {\n      // \u2500\u2500 INSERT path: satisfy the legacy NOT NULL columns by REUSING the living rail (module dogma) with a\n      // declared TODO \u2014 the sealed suite gives cadence a creative_assets subject but autopilot_plans still\n      // carries viral-era NOT NULL columns that were NOT relaxed by 20260716120000_cadence_recurrence.sql:\n      //   * mode NOT NULL CHECK IN('all_at_once','every_n_days') \u2192 'every_n_days' (recurring) + interval_days=1\n      //     placeholder (the real schedule is recurrence/next_run_at; interval_days is unused by cadence-run).\n      //   * target_product_ids NOT NULL CHECK(len>=1) \u2192 [sourceAssetId]: the cadence SUBJECT id reuses this\n      //     array (no source_asset_id column is declared in the SDD/data-model). TODO(FR-CAD-002/005): a\n      //     follow-up migration should add a source_asset_id column OR relax target_product_ids for\n      //     plan_kind='cadence'; until then the subject lives here and cadence-run resolves it owner-scoped.\n      //   * platforms NOT NULL (subset CHECK was dropped by the cadence migration) \u2192 the channel_allowlist.\n      // NONE of this is invention beyond the sealed rail: it is the minimal valid filler for pre-existing\n      // NOT NULL columns, and plan_kind='cadence' isolates routing so autopilot-run never reads them.\n      const name = typeof body?.name === \"string\" && body.name.trim() ? body.name.trim() : `Cad\u00eancia ${sourceAssetId.slice(0, 8)}`;\n      const { data: ins, error: insErr } = await admin\n        .from(\"autopilot_plans\")\n        .insert({\n          user_id: userId,\n          name,\n          mode: \"every_n_days\",\n          interval_days: 1,                     // placeholder \u2014 cadence re-arm uses recurrence, not interval_days\n          target_product_ids: [sourceAssetId],  // TODO(FR-CAD-002/005): subject reuses this legacy NOT NULL array\n          platforms: channels,                  // subset CHECK dropped by the cadence migration\n          ...cadenceCols,\n        })\n        .select(\"id\").maybeSingle();\n      if (insErr) {\n        if (insErr.code === \"23514\") return fail422(\"budget_cap_mco\", \"O teto de or\u00e7amento n\u00e3o atende ao m\u00ednimo do plano.\"); // DB CHECK\n        logHealth(\"error\", \"cadence_arm_insert_failed\", { code: insErr.code });\n        return json({ error: \"arm_failed\", detail: insErr.message }, 500);\n      }\n      if (!ins) return json({ error: \"arm_failed\" }, 500);\n      resultPlanId = ins.id;\n    }\n\n    // 0 mco at arm \u2014 profiles.mco_balance is untouched (FR-CAD-005 material invariant). No deduct_mco_coins.\n    logHealth(\"healthy\", \"cadence_armed\", { plan_id: resultPlanId, next_run_at: nextRunAt, channels });\n    return json({\n      plan_id: resultPlanId,\n      next_run_at: nextRunAt,            // ISO UTC\n      projected_cost_mco: projectedCostMco,\n    });\n  } catch (e) {\n    logHealth(\"error\", \"cadence_arm_unhandled\");\n    return json({ error: e instanceof Error ? e.message : \"unknown\" }, 500);\n  }\n});\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-plan/index.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(18:13:09)*

Now register the function in config.toml (verify_jwt=false, as the in-function identity gate requires the JWT to reach the function).

## 🤖 Claude *(18:13:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml",
  "old_string": "[functions.autopilot-run]\nverify_jwt = false\n[functions.autopilot-cadence-cron]\nverify_jwt = false",
  "new_string": "[functions.autopilot-run]\nverify_jwt = false\n[functions.autopilot-cadence-cron]\nverify_jwt = false\n[functions.cadence-plan]\nverify_jwt = false"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(18:13:19)*

Let me typecheck the function with Deno to catch errors.

## 🤖 Claude *(18:13:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "(command -v deno >/dev/null 2>&1 && deno check supabase/functions/cadence-plan/index.ts 2>&1 | head -40 || echo \"deno not installed \u2014 skipping typecheck\")",
  "description": "Deno typecheck cadence-plan"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> deno not installed — skipping typecheck
> ```

## 🤖 Claude *(18:13:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "node -e \"\nconst now = new Date();\n// mirror the calc to sanity-check next_run_at for weekly [1,3,5] 09:00 America/Sao_Paulo\nfunction tzOffsetMs(instant, tz){const dtf=new Intl.DateTimeFormat('en-US',{timeZone:tz,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'});const p={};for(const{type,value} of dtf.formatToParts(instant))p[type]=value;const asUTC=Date.UTC(+p.year,+p.month-1,+p.day,+p.hour,+p.minute,+p.second);return asUTC-instant.getTime();}\nfunction zonedWallToUtc(y,mo,d,h,mi,tz){const w=Date.UTC(y,mo,d,h,mi,0);const off=tzOffsetMs(new Date(w),tz);let ts=w-off;const off2=tzOffsetMs(new Date(ts),tz);if(off2!==off)ts=w-off2;return new Date(ts);}\nfunction localYmd(instant,tz){const dtf=new Intl.DateTimeFormat('en-US',{timeZone:tz,year:'numeric',month:'2-digit',day:'2-digit'});const p={};for(const{type,value} of dtf.formatToParts(instant))p[type]=value;return{y:+p.year,mo:+p.month-1,d:+p.day};}\nfunction isoDow(y,mo,d){const js=new Date(Date.UTC(y,mo,d)).getUTCDay();return js===0?7:js;}\nfunction computeNextRunAt(rec,from){const{y,mo,d}=localYmd(from,rec.tz);const base=Date.UTC(y,mo,d);for(let i=0;i<=430;i++){const cand=new Date(base+i*86400000);const cy=cand.getUTCFullYear(),cmo=cand.getUTCMonth(),cd=cand.getUTCDate();let m=false;if(rec.frequency==='daily')m=true;else if(rec.frequency==='weekly')m=rec.days.includes(isoDow(cy,cmo,cd));else if(rec.frequency==='monthly')m=rec.days.includes(cd);if(!m)continue;const utc=zonedWallToUtc(cy,cmo,cd,rec.hours,rec.minutes,rec.tz);if(utc.getTime()>from.getTime())return utc;}return null;}\nconsole.log('weekly 1,3,5 09:00 BRT ->', computeNextRunAt({frequency:'weekly',days:[1,3,5],hours:9,minutes:0,tz:'America/Sao_Paulo'},now).toISOString());\nconsole.log('daily 09:00 BRT ->', computeNextRunAt({frequency:'daily',days:[],hours:9,minutes:0,tz:'America/Sao_Paulo'},now).toISOString());\nconsole.log('monthly 15 08:30 UTC ->', computeNextRunAt({frequency:'monthly',days:[15],hours:8,minutes:30,tz:'UTC'},now).toISOString());\n// verify it lands on 09:00 local\nconst r=computeNextRunAt({frequency:'daily',days:[],hours:9,minutes:0,tz:'America/Sao_Paulo'},now);\nconsole.log('local render of daily result:', new Intl.DateTimeFormat('en-GB',{timeZone:'America/Sao_Paulo',weekday:'short',hour:'2-digit',minute:'2-digit'}).format(r));\n\"",
  "description": "Sanity-check the UTC re-arm calculator"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> weekly 1,3,5 09:00 BRT -> 2026-07-17T12:00:00.000Z
> daily 09:00 BRT -> 2026-07-16T12:00:00.000Z
> monthly 15 08:30 UTC -> 2026-08-15T08:30:00.000Z
> local render of daily result: Thu 09:00
> ```

## 🤖 Claude *(18:13:53)*

<details>
<summary>💭 Thinking Process</summary>

The calculator is working as expected. Today is Wednesday, July 15, 2026, and I'm verifying the schedule calculations: weekly events on Monday, Wednesday, Friday recur next on Friday at 9:00 AM BRT (which converts to noon UTC), daily events happen tomorrow at 9:00 AM local time, and monthly events on the 15th need to check whether today's occurrence has already passed.

</details>


## 🤖 Claude *(18:14:23)*

The calculator is correct (BRT −3, no DST → 09:00 local = 12:00Z, matching the FR-CAD-007 acceptance example; results always strictly after `now`).

## Report

**Path:** `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-plan/index.ts` (+ registered `[functions.cadence-plan] verify_jwt = false` in `supabase/config.toml`).

**3 linhas:**
1. Edge fn user-facing (JWT via `supabase.auth.getUser()`, padrão vivo de `canvas-execute`/`autopilot-run` — não `atob` cego; `user_id` server-trusted da claim; chave cron `Bearer SB_SECRET_KEY` → **403** pois arm é UI-only), que faz **upsert** em `autopilot_plans` (`plan_kind='cadence'` + `recurrence/quiet_hours/overlap_policy/catchup_window/jitter_seconds/program/channel_allowlist/budget_cap_mco`) owner-scoped, **0 mco** (nenhum `deduct_mco_coins`).
2. **ARMA `next_run_at` em UTC** via calculador DST-correto (`Intl.DateTimeFormat` offsets) a partir de `{frequency,days,hours,minutes,tz}` com cascata de fuso `recurrence.tz → profiles.timezone → America/Sao_Paulo` (FR-CAD-007); CORS + erros estruturados PT-BR (401/403/404/422/500) + telemetria `infra_health_logs service='spaces-cadence'`.
3. Encaixa nos trilhos vivos (estende `autopilot_plans`, sem tabela/cron novo — o tick `autopilot-cadence-cron` já roteia por `plan_kind`); a migration `20260716120000_cadence_recurrence.sql` que declara as colunas já existe e foi a fonte dos nomes exatos.

**Contrato de request/response (para o cliente):**

`POST /functions/v1/cadence-plan` — Header `Authorization: Bearer <user_jwt>`

```jsonc
// Request
{
  "sourceAssetId": "uuid",          // creative_assets.id owner-scoped (obrigatório; verificado)
  "recurrence": {                   // obrigatório, computado em UTC no servidor
    "frequency": "daily|weekly|monthly",
    "days": [1,3,5],                // weekly: 1=seg..7=dom · monthly: 1..31 · daily: ignorado
    "hours": 9, "minutes": 0,       // minutes múltiplo de 5
    "tz": "America/Sao_Paulo"       // IANA; se ausente/inválido → cascata profiles.timezone → default
  },
  "budget_cap_mco": 50,             // obrigatório, > 0, em mcoCoins (floor real do DB é 12)
  "channel_allowlist": ["wordpress","linkedin"], // não-vazio; X/twitter rejeitado (OTD-CAD-011)
  "planId": "uuid",                 // OPCIONAL: presente → UPDATE (re-arm); ausente → INSERT novo
  "enabled": true,                  // default true (ativa is_active p/ o tick pegar); false = armar sem ativar
  "quiet_hours": {"start":"22:00","end":"07:00","days":[1,2,3,4,5]}, // opcional
  "overlap_policy": "skip",         // opcional (só 'skip' na Fatia 1)
  "catchup_window": "6 hours",      // opcional (interval)
  "jitter_seconds": 0,              // opcional
  "program": [ /* CadenceStep[] */ ],            // opcional
  "projectedCostMco": 1350,         // opcional (inspector calcula — FR-CAD-011; ecoado)
  "name": "..."                     // opcional (default "Cadência <asset8>")
}

// Response 200
{ "plan_id": "uuid", "next_run_at": "2026-07-17T12:00:00.000Z", "projected_cost_mco": 1350 }

// Erros
// 401 {error:"Unauthorized"} · 403 {error:"Forbidden"} (chave cron) · 404 {error:"plan_not_found"}
// 422 {error:"validation_failed", field, message /*PT-BR*/} · 500 {error, detail}
```

**TODOs explícitos deixados no código (gaps do SSOT, citados por FR, não inventados):**
- **`target_product_ids` / `mode` / `platforms` NOT NULL legados** (do base migration viral `20260620120000`, não relaxados pela migration de cadência): no INSERT, reuso mínimo válido — `mode='every_n_days'`+`interval_days=1` placeholder, `platforms=channel_allowlist`, e o **subject (`sourceAssetId`) reusa `target_product_ids=[id]`** porque a SDD/data-model **não declara coluna `source_asset_id`**. TODO(FR-CAD-002/005): migration futura deve adicionar `source_asset_id` ou relaxar `target_product_ids` para `plan_kind='cadence'`.
- **`channel_allowlist` membership**: só valido não-vazio + X-excluído; a allowlist autoritativa "auto-publish MENOS X" não é constante na SDD (é por-plano), então o membership completo derivado de `channel_profiles.cadence` fica deferido ao FR-CAD-008.
- **`projected_cost_mco`**: sem tabela de custo mco por-canal nesta BoK, o edge ecoa o valor calculado pelo inspector (FR-CAD-011); TODO mover a projeção server-side quando o SSOT de custo por-canal existir.
- **`budget_cap_mco > 0`** (FRD literal) vs. **DB CHECK `>= 12`** (realidade viva): valido `>0` e mapeio violação de CHECK (23514) para 422 PT-BR limpo em vez de 500.

Nota: não rodei `deno check` (deno não instalado no ambiente); a lógica do calculador UTC foi verificada materialmente via Node contra o exemplo de aceite FR-CAD-007.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-15 - agent-afa049e03135ecca2]]
> * **Próxima Sessão**: [[2026-07-16 - Roadmap de automação de conteúdo com IA e Claude Code]]
%% --- TIMELINE END --- %%

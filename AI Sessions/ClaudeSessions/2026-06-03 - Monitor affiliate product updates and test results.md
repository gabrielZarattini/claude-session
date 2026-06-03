# Monitor affiliate product updates and test results
**Date:** 2026-06-03 | **Session ID:** `10450854-0c9b-4ef1-9d52-adab9c1b16ed`

---

## 👤 User *(14:05:37)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(14:05:37)*

# ShakeHands — Session Pick-Up Protocol v3

Execute the ShakeHands /handson ritual for this project.

> **v3 (2026-05-08):** Added BoK Gate enforcement per MCORCH Master Execution Protocol — alert when active module work has no sealed BoK suite at `docs/bok/<slug>/`.

---

## PRE-FLIGHT (execute ALL in parallel before reading anything)

```bash
git log --oneline -7                        # recent history + commit style
git status --short                          # uncommitted changes
git diff HEAD --stat                        # change scope
npx tsc --noEmit 2>&1 | tail -20           # TypeScript strict check
docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
docker ps --filter "name=mega-brain" --format "{{.Names}}: {{.Status}}"
curl -s http://localhost:8001/api/v2/heartbeat  # Chroma API v2 health
ls docs/bok/ 2>/dev/null                    # BoK suites disponíveis
wc -l HANDOFF.md                            # total lines — drives the read-from-end offset
```

Read in parallel (HANDOFF.md uses **read-from-end strategy** — SSP-01 v6.5.0; arquivo monolítico newest-first em ~3170+ linhas, leitura completa estoura limite de 25k tokens):
- `HANDOFF.md` with `limit=71` → Task State header + FIRST ACTION FOR NEXT AGENT (sempre estável, contém summary da fase atual selada)
- `HANDOFF.md` with `offset=<total_lines - 400>` `limit=400` → últimas 1-2 Records + Pending Actions + GraphRAG State + Infrastructure + Key Files (suffix sections always at the tail)
- `CLAUDE.md` (architecture rules, data flow, key files — incluindo MCORCH Master Execution Protocol + Survival Laws link)
- `.claude/context/sprint-priorities.md` (sprint goal, 4Cs snapshot, top gaps)
- `/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md` (memory index)

> ⚠️ **Auditoria histórica de seals antigos:** usar `Read` com offset arbitrário em HANDOFF.md (fora do fluxo padrão de pickup). Ordering newest-first: seal mais antigo ≈ linha 2805, seal mais recente logo após linha 71. Cada `## <Phase> Record (YYYY-MM-DD)` marca um seal. Manter o Read em chunks ≤ 400 linhas para preservar budget de tokens.

Also check for loose files in scratch/:
```bash
ls scratch/ 2>/dev/null && echo "⚠️ scratch/ has files — consider moving to .claude/scripts/db/" || echo "scratch/ clean ✅"
```

### BoK Gate check (v3 — MCORCH Master Execution Protocol)

For each BoK suite in `docs/bok/<slug>/`, verify completeness:
```bash
for slug in $(ls docs/bok/ 2>/dev/null); do
  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)
  missing=()
  for doc in "${required[@]}"; do
    [ -f "docs/bok/$slug/$doc.md" ] || missing+=("$doc")
  done
  [ ${#missing[@]} -eq 0 ] && echo "✅ $slug — BoK complete" || echo "⚠️ $slug — missing: ${missing[*]}"
done
```

If the user mentions working on a **new module / complex feature / integration / architectural change**:
- Check whether `docs/bok/<expected-slug>/` exists with all 9 docs.
- If missing: surface in the **ALERTAS** section as a critical block per CLAUDE.md MCORCH Master Execution Protocol.
- Recommend `/bok-scribe <idea summary>` before any code is written.

---

## BRIEF OUTPUT

After gathering all context, produce a structured brief in **Portuguese (Brasil)**:

```
═══════════════════════════════════════════════════════════
  HANDSON — <FASE SELADA> (<data do último seal>)
═══════════════════════════════════════════════════════════

🏁 ESTADO ATUAL
  Fase selada: <nome da última fase — do Task State header>
  Últimos commits:
    <hash> — <mensagem>
    <hash> — <mensagem>
    <hash> — <mensagem>

📂 MUDANÇAS PENDENTES
  <lista de arquivos M/?? com descrição do que contém, ou "Worktree limpo ✅">

🏗️ INFRA
  mcorch_chroma:     <status> — Chroma API: <OK / ERRO>
  mcorch_claude_mem: <status>
  mega-brain-*:      <status resumido>

🧠 KNOWLEDGE MESH
  <totalNodes> nós · <totalEdges> arestas (fonte: HANDOFF.md GraphRAG State)
  Top tipos: <milestone:N · architecture:N · decision:N ...>

🔧 TYPESCRIPT
  <"Zero erros ✅" ou lista dos erros críticos>

📚 BoK SUITES (v3 — MCORCH Master Execution Protocol)
  Sealed: <list of docs/bok/<slug>/ com 9 docs completos>
  Incomplete: <slugs com docs faltando ou "nenhum">
  Mesh seal nodes:
    <slug> → <node_id> (stability X.XX)

⚠️ **GATE alert:** se sessão tocar módulo significativo sem BoK selada,
    listar como bloqueador crítico e sugerir /bok-scribe antes de qualquer commit.

📌 SPRINT
  Goal: <Sprint Goal de sprint-priorities.md, ou "⚠️ Sprint goal não definido — rode /audit">
  Top gap: <Gap #1 da seção "Top 3 Gap Closures", ou "não definido">

⚡ PRÓXIMOS PASSOS (prioridade)
  1. <item de maior prioridade do Pending Actions — com contexto de por que é urgente>
  2. <segundo item>
  3. <terceiro item>

⚠️ ALERTAS
  <containers unhealthy, TS errors, uncommitted changes que conflitam, scratch/ com arquivos, ou "Nenhum alerta ✅">

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

---

## Rules

- **TypeScript errors → report immediately.** If there are TS errors, list them under ALERTAS. Do not start implementing new features until errors are resolved (unless the user explicitly asks to proceed despite errors).
- **Unhealthy containers → report with triage.** Suggest the fix command if known (e.g., `docker compose restart mcorch-vector-engine` for chroma).
- **Uncommitted changes → describe, do not commit.** Only describe what exists in the working tree; committing is the user's call.
- **Keep the brief tight.** No padding. No repetition of CLAUDE.md architecture. The user already knows the architecture — they need the delta: what changed, what's broken, what's next.
- **Pending Actions priority order:** CRITICAL (before first client) > NON-CRITICAL > Phase Zeta > Core v3 > Epsilon v9.
- **Knowledge Mesh numbers:** use `GraphRAG State` section from HANDOFF.md as the source. Do not invent counts.


## 🤖 Claude *(14:05:42)*


## 🤖 Claude *(14:05:43)*

I'll execute the ShakeHands /handson ritual. Let me start with all pre-flight checks in parallel.

## 🤖 Claude *(14:05:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin 2>&1 | tail -3; echo \"--- LOG ---\"; git log --oneline -7; echo \"--- STATUS ---\"; git status --short; echo \"--- DIFF STAT ---\"; git diff HEAD --stat; echo \"--- vs origin/main ---\"; git rev-list --left-right --count HEAD...origin/main 2>/dev/null",
  "description": "Git fetch + log + status + diff scope"
}
```

## 🤖 Claude *(14:05:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20; echo \"--- TSC EXIT: done ---\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- LOG ---
> 9d48bf9 chore(sprint): update sprint-priorities — v6.22.0 Campaign Core + OTD-LLM-FALLBACK + lead-score
> 458d74f docs(handoff): seal v6.22.0 — Campaign Core + OTD-LLM-FALLBACK closed + lead-score live
> 2017714 docs(readme): v6.22.0 — Campaign Core + OTD-LLM-FALLBACK closed + lead-score live
> d3f6015 chore(billing): centraliza COIN_COSTS (LEAD_SCORE/CAMPAIGN_RUN) + divida de calibracao
> 46362c4 feat(marketing-hub): lead-score edge fn (FR-MH-003) — JWT + 1 mco + IA fail-soft
> 0a182d3 feat(llm-fallback): telemetria infra_health_logs + teste de cascata — fecha OTD-LLM-FALLBACK
> 7fd8e7a feat(marketing-hub): MVP-2 Campaign Core — campaigns absorvida + campaign_steps + marketing_attribution
> --- STATUS ---
> --- DIFF STAT ---
> --- vs origin/main ---
> 0	0
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- TSC EXIT: done ---
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> --- BoK suites ---
> aios-sql-bridge
> canvas-design
> constellation-v2
> conteudo-v2
> e2e-user-zero
> gamificacao-nodes
> marketing-hub
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> viralmind
> --- HANDOFF lines ---
> 6470 HANDOFF.md
> --- scratch ---
> scratch clean or absent
> ```

## 🤖 Claude *(14:05:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- mcorch containers ---\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"--- mega-brain ---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"--- chroma heartbeat ---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat 2>&1; echo \"\"; echo \"--- done ---\"",
  "description": "Docker containers + Chroma health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- mcorch containers ---
> mcorch_chroma: Up 10 days (healthy)
> mcorch_claude_mem: Up 10 days (healthy)
> --- mega-brain ---
> mega-brain-dashboard: Up 10 days
> mega-brain-webhook: Up 10 days (healthy)
> mega-brain-daemon: Up 10 days (healthy)
> --- chroma heartbeat ---
> {"nanosecond heartbeat":1780495548195534751}
> --- done ---
> ```

## 🤖 Claude *(14:05:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- BoK suites ---\"; ls docs/bok/ 2>/dev/null; echo \"--- HANDOFF lines ---\"; wc -l HANDOFF.md; echo \"--- scratch ---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean or absent\"",
  "description": "BoK suites + HANDOFF size + scratch check"
}
```

## 🤖 Claude *(14:06:07)*


## 🤖 Claude *(14:06:08)*

Sync clean (`0 0` vs origin/main), TSC zero errors, all containers healthy, scratch clean. HANDOFF.md grew to 6470 lines. Reading the key files now (CLAUDE.md and MEMORY.md already in my context).

## 🤖 Claude *(14:06:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 80
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# HANDOFF — MCORCH Constellation Orchestra
> 2	
> 3	## ⚡ FIRST ACTION FOR NEXT AGENT
> 4	
> 5	```bash
> 6	git log --oneline -5
> 7	# Then explore the codebase — do NOT start from the file tree
> 8	```
> 9	
> 10	---
> 11	
> 12	## Task State
> 13	
> 14	## Campaign Core + LLM Fallback + Lead Scoring Record (2026-06-03)
> 15	
> 16	**v6.22.0 (2026-06-03)** — Sessão `/handson` → ação nos alertas → próximos passos priores. Quatro entregas materiais (cada claim provada NESTE turno, não auto-declarada) + decisão de design financeiro **registrada em vez de improvisada** (Master Protocol).
> 17	
> 18	**O que foi entregue:**
> 19	
> 20	- **Alerta `meta_config` — verificado VAZIO (nada a limpar).** O "achado lateral" da v6.20.4 (4 linhas órfãs) já fora varrido: `meta_config_table` 0 linhas (`*/0`), `auth.users` 1 == `profiles` 1 (zero user sem profile), RPC `disconnect_meta` (migration 160000) viva e fail-closed (`28000`). Não fabriquei limpeza inexistente (Lei 1). Cérebro-sem-mãos parcial honesto: `vault.secrets` não-lido via REST.
> 21	- **MVP-2 Campaign Core LIVE** (migration `20260603025256`) — `campaigns` **ABSORVIDA** via `ALTER` (probe-first pegou que já existia + `campaign_metrics` também): `+intent +channels text[] +mesh_node_id uuid→mcorch_nodes + UNIQUE(id,user_id)`. Novas: `campaign_steps` (FK composta tenant-escopada `(campaign_id,user_id)→campaigns` CASCADE, espelha lead_events) + `marketing_attribution` (FK simples SET NULL + RLS WITH CHECK de posse, espelha marketing_consents — retém receita de-linkada). `erase_lead()` estendida (FMEA-MH-003 → `attributions_delinked`). BoK data-model patcheado (absorb-not-create + FK pattern). `/security-review` SAFE (subagente independente, 0 findings ≥8). **Prova comportamental**: `23503` (FK composta, ataque cross-tenant) + `42501` (WITH CHECK attribution, B autenticado plantando campanha de A) + 201 legítimos + cleanup zero-resíduo. types.ts 3307→3544. Mesh seal `7628892b` + edge `0d58d93b` DERIVES_FROM BoK `d5163fed`.
> 22	- **OTD-LLM-FALLBACK FECHADA cedo** (SLA 2026-06-07, owner engineer) — probe-first: o helper `fetchLLMWithFallback` (OpenRouter→Gemini Free→OpenRouter Free→502) já estava live em 11 edge fns. Gap real vs SOP success-signal = observabilidade: helper agora emite `infra_health_logs` (degraded/unhealthy), autossuficiente em Deno (POST PostgREST, sem SDK), fire-and-forget, no-op em teste. **Primeiro teste de edge-helper do projeto** (6 casos de cascata) + vitest estendido a supabase/functions + setup node-tolerant. 3 fns fora do escopo por design (aios-chat gemini-native / search-constellation embeddings / openrouter-swarm arena). 6/6 testes · 11 fns redeployadas · telemetria insert 201 · Gemini 200. Mesh seal `6061a6d2`.
> 23	- **lead-score edge fn LIVE** (FR-MH-003) — JWT (`getUser`), débito atômico 1 mcoCoin (`deduct_mco_coins`), scoring 0-100 via IA per-user→sistema (reusa o cascade helper), **fail-soft heurístico**, persiste `leads.score` + promove `new→scored` + `lead_event` imutável + pulse infra_health. **Smoke real E2E**: HTTP 200 · score=80 · rationale coerente (`source=ai`) · débito 100→99 · cleanup zero-resíduo. Deploy 84.31kB.
> 24	- **Calibração mcoCoins — dívida levantada (OTD-MCOIN-CALIBRATION).** Sovereign questionou se `10` é calibrado: **não é** (número redondo; `orchestrate-content` cobra 10 flat < soma dos componentes 18; `mcoin_transactions` mostram canvas_video dominante ~122/vídeo). `COIN_COSTS` centralizado (`LEAD_SCORE 1`/`CAMPAIGN_RUN 10`) + nota de calibração. **`campaign-run` ESPECIFICADA** (cascata fiel) mas **ADIADA por decisão Sovereign** (Lei 3 — contexto saturado; código financeiro merece sessão fresca + preços $).
> 25	
> 26	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = schema comercial + débito financeiro mcoCoins; migration + 12 deploys com GO "Aprovado").
> 27	
> 28	| Verificação | Resultado |
> 29	|---|---|
> 30	| Alerta meta_config | ✅ VAZIO material (0 linhas · 1==1 user/profile · RPC 160000 fail-closed) |
> 31	| MVP-2 migration aplicada | ✅ `db push Finished` · `20260603025256` |
> 32	| MVP-2 tenant-FK comportamental | ✅ 23503 (composta) + 42501 (WITH CHECK auth) + 201 + zero-resíduo |
> 33	| MVP-2 /security-review | ✅ SAFE (independente, 0 findings ≥8) |
> 34	| OTD-LLM-FALLBACK | ✅ telemetria + 6/6 testes + 11 fns redeploy + insert 201 |
> 35	| lead-score smoke E2E | ✅ 200 · score=80 source=ai · débito 100→99 · zero-resíduo |
> 36	| tsc / suíte | ✅ 0 erros · 244 passed / 2 skipped |
> 37	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 38	| Handoff node | ✅ `aec4cb9c-3765-4d58-9d92-d8130fe568bd` embedded 768d |
> 39	| Mesh | ✅ 8759 nós |
> 40	
> 41	| Commit | Conteúdo |
> 42	|---|---|
> 43	| `7fd8e7a` | feat(marketing-hub): MVP-2 Campaign Core — campaigns absorvida + campaign_steps + marketing_attribution |
> 44	| `0a182d3` | feat(llm-fallback): telemetria infra_health_logs + teste de cascata — fecha OTD-LLM-FALLBACK |
> 45	| `46362c4` | feat(marketing-hub): lead-score edge fn (FR-MH-003) |
> 46	| `d3f6015` | chore(billing): centraliza COIN_COSTS + dívida de calibração |
> 47	| `2017714` | docs(readme): v6.22.0 |
> 48	
> 49	### Survival Laws Self-audit
> 50	```
> 51	Law 1 (Materiality): ✅ toda claim provada NESTE turno — meta_config (count */0 + admin API 1==1), MVP-2 (db push Finished + REST schema + 23503/42501/201 + cleanup REST), OTD (6/6 vitest + 11× Deployed + insert 201 + Gemini 200), lead-score (smoke E2E 200 + REST score/event/balance + zero-resíduo), calibração (mcoin_transactions REST). /security-review por subagente INDEPENDENTE. Fase 5c executada abaixo. Zero fabricação.
> 52	Law 2 (Process): ✅ BoK data-model patcheado ANTES da migration MVP-2; SOP llm-cascading-fallback.md honrado; campaign-run NÃO improvisada (ambiguidade financeira → decisão Sovereign).
> 53	Law 3 (Pruning): ✅ 1 poda explícita após MVP-2+OTD; sessão SELADA por decisão consciente em vez de forçar campaign-run com contexto saturado.
> 54	Law 4 (ORO): ✅ triplet declarado; toda ação outward (migration, 12 deploys, mesh seals) com GO Sovereign.
> 55	```
> 56	
> 57	**Pendências/Próximos (sessão fresca):**
> 58	- **campaign-run (MVP-3 parte 2)** — cascata fiel: `CAMPAIGN_RUN` (10) + por passo `invoke('orchestrate-content')` (10 cada) + sync `campaign_steps.status`. Contrato: `{campaign_id}` → `{status,campaign_id,run_id,steps_dispatched,new_balance}`; errors 401/402/404/422/500.
> 59	- **OTD-MCOIN-CALIBRATION** — calibrar `COIN_COSTS` contra custo $ real (preço por-modelo OpenRouter + Higgsfield vídeo). Vídeo é o maior custo real.
> 60	- **MVP-4** hooks (`useLeads`/`useCampaigns`/`useLeadScore`) + UI (`LeadBoard`/`CampaignComposer`) + rota `/dashboard/marketing`.
> 61	- **MVP-5** attribution → `ROIWidget` por campanha + testes E2E.
> 62	- **lead-score follow-up:** granularidade `functionName` nas outras 10 fns do helper (hoje logam "unknown" no fallback).
> 63	
> 64	---
> 65	
> 66	## Marketing Hub v2 — BoK Suite + 11-Agent System + MVP-1 Lead Core Record (2026-06-03)
> 67	
> 68	**v6.21.0 (2026-06-03)** — Sessão dirigida pelo Sovereign para criar o módulo **marketing-hub** a partir de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). Padrão dominante: **governança BoK-first** (Master Execution Protocol) + **probe-first material** antes da migration. Fluxo: `/handson` → escopo via AskUserQuestion → `/bok-scribe` (9/9) → `/bok-agents-generator` (11 agentes) → revisão Sovereign ("aprovado") → MVP-1 (migration + `/security-review` + apply + prova adversarial) → este selo.
> 69	
> 70	**O que foi entregue:**
> 71	- **Suíte BoK 9/9 selada** (`docs/bok/marketing-hub/`, 1732 LOC) — módulo nasce como **v2 de consolidação**: absorve e escala o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**). Natureza **Ambos** (núcleo interno Usuário Zero + comercial per-tenant). Traceability **0 órfãos** (MR-MH→BR-MH→PR-MH→FR-MH). Mesh seal `d5163fed-da85-4f95-8445-0d0aa5b6bafe` (DERIVES_FROM meta-api `ca791bdd`, embedded 768d).
> 72	- **Sistema de 11 agentes** (`bok-agents-system--marketing-hub.md` via `/bok-agents-generator`) — 8 BoK (BABOK/EABOK/DMBOK/BPM/SWEBOK/CISSP/CXBOK/ProdBOK) + 3 delta (AEO, Intent Orchestration, Demand-gen/Growth) + 3 camadas cross-agent + Pantheon Reconciliation.
> 73	- **MVP-1 Lead Core LIVE** (migration `20260603000000`) — `leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` (LGPD: SECURITY DEFINER, `search_path=''`, fail-closed `28000`, tenant guard `42501`, EXECUTE só authenticated). RLS default-deny nas 3. Backfill de whatsapp_leads (no-op: tabela vazia em prod). `/security-review` (subagente independente) pegou **1 cross-tenant MEDIUM** (FK de filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta `(lead_id,user_id)→leads(id,user_id)`** + `UNIQUE(id,user_id)` + EXISTS no WITH CHECK do consent.
> 74	
> 75	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = novo módulo comercial + PII de lead LGPD; migration aplicada em prod com GO "aprovado").
> 76	
> 77	| Verificação | Resultado |
> 78	|---|---|
> 79	| BoK gate marketing-hub | ✅ 9/9 (1732 LOC) · traceability 0 órfãos |
> 80	| Mesh seal | ✅ `d5163fed` embedded 768d · DERIVES_FROM meta-api `ca791bdd` |
> ```

## 🤖 Claude *(14:06:10)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 80,
  "limit": 420
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 80	| Mesh seal | ✅ `d5163fed` embedded 768d · DERIVES_FROM meta-api `ca791bdd` |
> 81	| Sistema de agentes | ✅ 11 agentes (8 BoK + 3 delta) · 40 KB · `bok-agents-system--marketing-hub.md` |
> 82	| `/security-review` da migration | ✅ 1 MEDIUM cross-tenant achado → REMEDIADO (não suprimido) |
> 83	| Fix tenant-FK (prova comportamental) | ✅ **23503** no ataque (bogus lead + cross-tenant) · **201** no legítimo · cleanup zero-resíduo |
> 84	| Migration aplicada | ✅ `db push` Finished · `20260603000000` no remoto |
> 85	| `tsc --noEmit` | ✅ 0 erros |
> 86	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 87	| Handoff node | ✅ `a48d8ff4-1069-4ca0-8764-f01922e2e12f` embedded 768d |
> 88	| Mesh | ✅ 8755 nós |
> 89	
> 90	| Commit | Conteúdo |
> 91	|---|---|
> 92	| `c4be815` | docs(bok): sela suíte marketing-hub 9/9 + sistema de 11 agentes |
> 93	| `ff81c4f` | feat(marketing-hub): Lead Core migration — leads/lead_events/consents + erase_lead RPC |
> 94	| `8d4b24e` | docs(readme): v6.21.0 |
> 95	
> 96	### Arquitetura — Lead Core (tenant isolation)
> 97	```
> 98	CAPTURE    whatsapp-webhook → whatsapp_leads → (backfill OTD-MH-001) → leads
> 99	LIFECYCLE  leads.status: new → scored → nurturing → converted | lost     (RLS auth.uid())
> 100	EVENTS     lead_events  FK composta (lead_id,user_id)→leads(id,user_id)  ← fecha cross-tenant linkage
> 101	CONSENT    marketing_consents  basis LGPD · FK lead_id ON DELETE SET NULL = retém prova legal
> 102	ERASURE    erase_lead(uuid) SECURITY DEFINER → delete lead+events + withdraw consent (zero-residue)
> 103	```
> 104	
> 105	### Survival Laws Self-audit
> 106	```
> 107	Law 1 (Materiality): ✅ toda claim provada NESTE turno — BoK gate 9/9 (wc -l + ls), mesh seal d5163fed (INSERT RETURNING + embedding REST 768d), 11 agentes (grep count), /security-review por subagente INDEPENDENTE (não auto-avaliação), fix provado comportamental (23503/201 + cleanup via REST), db push Finished, handoff node embedded. Achado schema↔realidade (campaigns já existe / projects não existe) pego por probe-first ANTES de codar. Zero fabricação. Fase 5c executada abaixo.
> 108	Law 2 (Process): ✅ BoK É o processo antecipado (Master Protocol); scope-lock em disco antes do scribe; /security-review obrigatório na migration (regra CLAUDE.md) — finding REMEDIADO material, não suprimido.
> 109	Law 3 (Pruning): ✅ checkpoint explícito após MVP-1 (foundation live) antes de MVP-2..5; tasks rastreadas (MVP-2..5 pendentes); memória de projeto project_marketing_hub_v2 gravada.
> 110	Law 4 (ORO): ✅ triplet declarado; toda ação outward (mesh seal, db push) com GO Sovereign ("aprovado").
> 111	```
> 112	
> 113	**Pendências/Próximos (anotados p/ próxima sessão):**
> 114	- **MVP-2 Campaign Core** — **ABSORVER** a `campaigns` existente (de `20260402014040`: user_id/name/objective/status `campaign_status`/platforms/budget_cents) via `ALTER` (add intent/channels/mesh_node_id) + nova `campaign_steps` + `marketing_attribution`. **NÃO** criar `campaigns` nova (colisão real). Patch nos docs BoK (data-model/SDD) p/ refletir absorb-not-create + `projects` sem-FK.
> 115	- **MVP-3** edge fns `lead-score` (1 mco) / `campaign-run` (10 mco, orquestra orchestrate-content) — JWT gate + `deduct_mco_coins` + `infra_health_logs`.
> 116	- **MVP-4** hooks (`useLeads`/`useCampaigns`/`useLeadScore`/`useMarketingConsent`) + UI (`LeadBoard`/`CampaignComposer`) + rota `/dashboard/marketing`.
> 117	- **MVP-5** attribution → `ROIWidget` por campanha + testes + deploy (build-deploy-guardian).
> 118	- **`erase_lead` extensão obrigatória:** cada nova tabela PII do marketing-hub DEVE estender `erase_lead()` (disciplina FMEA-MH-003 — completude da erasure).
> 119	
> 120	---
> 121	
> 122	## ML Affiliate OAuth Probe + Disconnect UI Verification Record (2026-06-02)
> 123	
> 124	**v6.20.4 (2026-06-02)** — **Seal de conhecimento — zero código de produção tocado** (working tree limpo do início ao fim). Sessão dirigida por duas diretivas do Sovereign, no padrão **probe-first material**: (#1) fechar o resíduo visual que a v6.20.3 anotou — confirmar o disconnect Meta/social pela UI **logada** — e (#2) destravar a iniciativa do **Operador de Browser Autenticado** decidindo o runtime por **probe ANTES** de qualquer `/bok-scribe`/código.
> 125	
> 126	**#1 — disconnect verificado NON-DESTRUTIVO na UI logada.** Loguei como Usuário Zero via Supabase **Admin API `generate_link`** (magic link — método per-user reproduzível, sem token do DevTools nem senha crua) dirigindo `agent-browser` 0.27.0 (Chromium real). `/dashboard/social` renderiza as 3 contas ativas (LinkedIn/Instagram/Facebook), cada uma com botão Desconectar **interativo** (snapshot refs e11/e12/e13) wired a `rpc('disconnect_social')`; `useMetaConfig.ts:78`/`useSocialAccounts.ts:43` chamam `disconnect_meta`/`disconnect_social` (zero `.delete()` resquício). **Nenhum clique destrutivo** — as 3 contas seguem `is_active`; o clique→RPC→revogação-Vault já era DB-proven na v6.20.3. Fecha o resíduo "browser autenticado indisponível" da seal anterior.
> 127	
> 128	**#2 — probe OAuth ML CONCLUÍDO (veredito material):**
> 129	- **Sem API oficial de afiliados ML** — convergência de múltiplas fontes + 403 até no WebFetch da Anthropic. OAuth/login-consentimento daria só um API token, que não existe p/ afiliados.
> 130	- **Link oficial exige portal LOGADO** — segui o `meli.la` do Usuário Zero → redireciona p/ `mercadolivre.com.br/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`. O `ref` é token assinado **não-fabricável**, gerado só no portal.
> 131	- **Datacenter BLOQUEADO p/ browser REAL** — `agent-browser` no portal de afiliados do IP Oracle → página "Hubo un error accediendo a esta pagina" (antes "não-testado"; agora provado). ⇒ Browser Operator **não roda do datacenter**; runtime tem de ser navegador do user ou IP residencial.
> 132	- **Resolver incompleto** — `src/lib/affiliate.ts` seta só `matt_word`; o formato oficial carrega também `matt_tool` (per-user, não armazenado hoje no `affiliate_config`).
> 133	
> 134	**Experimento em curso (Sovereign):** teste de atribuição de clique de links `matt_word`-anexados por dispositivo independente; resultado ~2026-06-03. **Decisão do #2 (Browser Operator vs. só completar o resolver) PAUSADA aguardando o dado.** Não vejo o painel de afiliados (logado + IP bloqueado) — Cérebro sem mãos: Sovereign reporta o nº.
> 135	
> 136	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign · blast radius **nulo** (verificação non-destrutiva + probe read-only; nenhuma mutação de produção, nenhuma credencial manuseada).
> 137	
> 138	| Verificação | Resultado |
> 139	|---|---|
> 140	| #1 login UI (Admin API `generate_link`) | ✅ `/dashboard/settings` + `/dashboard/social` logado (sem redirect p/ `/auth`); header 5351 mcoCoins |
> 141	| #1 disconnect wiring | ✅ `rpc('disconnect_social'/'disconnect_meta'/'disconnect_wordpress')`; zero `.delete()` resquício |
> 142	| #1 não-mutação | ✅ 3 contas sociais seguem `is_active=true` (nenhum clique destrutivo) |
> 143	| #2 ML sem API | ✅ múltiplas fontes + 403 (WebFetch) |
> 144	| #2 link oficial = portal | ✅ `meli.la` → `/social/…&ref=<assinado>` não-fabricável |
> 145	| #2 datacenter bloqueado (browser real) | ✅ "Hubo un error accediendo a esta pagina" |
> 146	| `tsc --noEmit` | ✅ 0 erros |
> 147	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 148	| Handoff node | ✅ `af6bffa2-bce8-4c43-952e-67c0db9c3d23` embedded 768d |
> 149	| Mesh | ✅ 8753 nós |
> 150	
> 151	### Survival Laws Self-audit
> 152	```
> 153	Law 1 (Materiality): ✅ toda claim provada NESTE turno — login via Admin API (URL+título+screenshot), wiring por grep do código, não-mutação por REST (3 is_active), probe por redirect real do meli.la + screenshot do bloqueio ML + 403 do WebFetch. Cérebro-sem-mãos declarado p/ o painel de afiliados (logado+IP bloqueado → Sovereign reporta). Zero fabricação. Fase 5c executada. Zero código → sem claims de commit de feature.
> 154	Law 2 (Process): seal de conhecimento; nenhuma feature nova ganhou código — probe-first respeitado (NÃO construí matt_tool/Browser Operator antes do dado). Memória project_authenticated_browser_operator atualizada com o veredito.
> 155	Law 3 (Pruning): contexto < 50%; decisão consciente de selar no ponto natural em vez de misturar #3/LLM-fallback. Probe consolidado por evidência (UUID/screenshot/redirect).
> 156	Law 4 (ORO): ✅ declarado no início da fase de execução.
> 157	```
> 158	
> 159	**Pendências/Próximos:**
> 160	- **[AGUARDANDO DADO ~2026-06-03] Atribuição de clique ML** — Sovereign reporta o nº de cliques do painel (esperado 1→3 se `matt_word` anexado rastrear) + se o painel mostra por-link ou só total. Decide o destino do #2: (a) `matt_word` basta → quase mata o #2; (b) falta `matt_tool` → add campo per-user no `affiliate_config` + testar; (c) precisa do `ref` → `/bok-scribe` do Browser Operator com runtime FORA do datacenter.
> 161	- **[ACHADO LATERAL] 4 linhas `meta_config` sem profile** — Usuário Zero tem 0 meta_config; as 4 linhas no total pertencem a user_ids sem profile (possível resíduo órfão). Investigar/limpar à parte.
> 162	- **[PRAZO] OTD-LLM-FALLBACK SLA 2026-06-07** — Cascading LLM fallback (owner engineer) — candidato a sessão dedicada após fechar os afiliados.
> 163	
> 164	---
> 165	
> 166	## Meta/Social Disconnect — Orphaned-Secret Revocation Record (2026-06-02)
> 167	
> 168	**v6.20.3 (2026-06-02)** — Sessão disparada por duas diretivas do Sovereign: (A) rodar `/security-review` **redundante** apontado para o `87c926f` (o guard de tenant meta/social selado em v6.20.2) — cinto-e-suspensório; e (B) atacar o débito de **segredo Vault órfão** que a própria seal v6.20.2 anotou no Pending. Padrão dominante mantido: **probe-first material** (Management API, todo teste mutante em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify**. Antes de codar a Parte B, confirmei materialmente que o gap de tenant guard da diretiva original já estava 100% fechado em prod (`pg_get_functiondef` das 2 triggers + ataque comportamental 5/5 → `42501`), evitando uma migration redundante.
> 169	
> 170	**O que foi entregue (Parte B):**
> 171	- **`disconnect_meta()` / `disconnect_social(p_account_id uuid)`** (migration `20260602160000`) — RPCs SECURITY DEFINER, `search_path=''`, fail-closed `28000` sem `auth.uid()`, EXECUTE só `authenticated`. Espelham `disconnect_wordpress`: deletam a linha **E** revogam o segredo Vault. Hooks `useMetaConfig`/`useSocialAccounts` migrados de `.delete()` → `.rpc()`; `types.ts` regenerado (3 entradas: as 2 RPCs + `vault_upsert_secret`).
> 172	- **Guard de tenant por name-binding** (diferença do WP): segredos meta/social são nomeados pelo `id` da linha, não `user_id`. Cada `DELETE` no Vault é double-bound (`id = ref-da-própria-linha` **E** `name = '<prefix>_' || id-da-própria-linha`); como `id` é PK, o id do atacante nunca iguala o da vítima → impossível revogar segredo alheio. Defesa independente: o UUID bruto nunca vaza ao cliente.
> 173	- **Limpeza one-time** dos órfãos preexistentes (`12 → 0` segredos Meta), provadamente orphan-scoped (`NOT EXISTS` linha base via `right(name,36)`), preservando os 3 segredos sociais vivos.
> 174	
> 175	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = retenção de plaintext órfão LGPD + integridade do disconnect per-user).
> 176	
> 177	| Verificação | Resultado |
> 178	|---|---|
> 179	| Parte A — `/security-review` do `87c926f` | ✅ **LIMPO 9/10** (net-hardening; `IS DISTINCT FROM` fecha bypass NULL, UPDATE só vê OLD do próprio tenant, sem SQL dinâmico) |
> 180	| Gap original já fechado (pré-build) | ✅ `pg_get_functiondef` das 2 triggers c/ guard+`42501`+`search_path=""` · ataque comportamental 5/5 `42501` |
> 181	| Suíte RPC (BEGIN/ROLLBACK, dados reais) | ✅ **5/5** — happy meta+social · foreign-id no-op · planted-ref name-binding aguenta · unauth `28000` · zero resíduo |
> 182	| Limpeza de órfãos (preview→apply) | ✅ `12 → 0` segredos Meta órfãos · 3 sociais vivos + 3 linhas intactos |
> 183	| Parte B — `/security-review` da `20260602160000` | ✅ **LIMPO/SAFE 9/10** (PK garante id distinto + UUID não-vazado) |
> 184	| Apply em prod (Mgmt API, txn atômica) | ✅ `20260602160000` no `schema_migrations`; funções SECURITY DEFINER `search_path=""`; EXECUTE authenticated✓/anon revogado✓ |
> 185	| `tsc --noEmit` | ✅ 0 erros |
> 186	| Testes | ✅ 238 passed / 2 skipped · eslint 0 |
> 187	| Frontend deploy | ✅ build exit 0; bundle servido contém `disconnect_meta`/`disconnect_social` + Supabase URL baked |
> 188	| Mesh | ✅ 8752 nós |
> 189	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 190	| Handoff node | ✅ `f7805e20-bebd-4a30-8533-09806238f135` embedded 768d |
> 191	
> 192	| Commit | Conteúdo |
> 193	|---|---|
> 194	| `76bb9e3` | fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão |
> 195	| `610e1f3` | docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão) |
> 196	| `ac1cba1` | docs(readme): v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social) |
> 197	
> 198	### Arquitetura — disconnect com revogação de segredo órfão
> 199	```
> 200	DISCONNECT (meta/social), antes:  client .delete() → INSTEAD OF DELETE → DELETE base row
> 201	                                  → segredo Vault FICA ÓRFÃO (plaintext retido) ❌
> 202	DISCONNECT (meta/social), agora:  client .rpc('disconnect_meta' | 'disconnect_social', {p_account_id})
> 203	   disconnect_*(): IF auth.uid() IS NULL → 28000
> 204	     v_row_id, v_*_ref ← SELECT da PRÓPRIA linha (WHERE user_id = auth.uid() [+ id = p_account_id])
> 205	     DELETE base row
> 206	     DELETE vault.secrets WHERE id = v_*_ref  AND  name = '<prefix>_' || v_row_id   ← double-bind
> 207	       (id é PK ⇒ id-do-atacante ≠ id-da-vítima ⇒ name nunca casa segredo alheio = tenant-safe)
> 208	CLEANUP one-time: DELETE vault.secrets WHERE name ~ '^<prefix>_<uuid>$'
> 209	                  AND NOT EXISTS (linha base com id = right(name,36))   ← só órfãos (12→0)
> 210	```
> 211	
> 212	### Survival Laws Self-audit
> 213	```
> 214	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API — gap original já-fechado (pg_get_functiondef + 5/5 comportamental), suíte RPC 5/5 rolled-back, preview→apply da limpeza (12→0 / 3 vivos), pós-apply (funções+grants+tracking), build+bundle servido com as RPCs. Zero fabricação. 1 armadilha divulgada (urllib→Cloudflare 1010 → troquei p/ curl). Fase 5c executada abaixo. NÃO criei migration redundante p/ o gap já fechado (seria fabricar trabalho).
> 215	Law 2 (Process): ✅ SOP credential-disconnect-clear.md estendido (seção disconnect meta/social + equivalência LGPD) antes do commit; CLAUDE.md Key Files. Extensão de feature documentada (disconnect/clear) → sem BoK gate.
> 216	Law 3 (Pruning): investigação focada; outputs consumidos, referência por path/UUID/migration/commit.
> 217	Law 4 (ORO): ✅ declarado no início da Parte B; "faça os dois" = autorização autônoma do Sovereign.
> 218	```
> 219	
> 220	**Pendências/Próximos (anotados p/ próxima sessão):**
> 221	- **E2E no navegador:** o disconnect foi verificado pela perspectiva do banco (RPC 5/5 + bundle servido contém as RPCs); o clique real na UI logada (`/dashboard/settings` → Desconectar Meta/social) não foi executado (browser autenticado indisponível). Confirmar visualmente no próximo passe.
> 222	
> 223	---
> 224	
> 225	## Vault Idempotent Encrypt + Tenant Guard Record (2026-06-02)
> 226	
> 227	**v6.20.2 (2026-06-02)** — Sessão disparada pela dívida residual que a própria seal v6.20.1 anotou no Pending: o `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` **incondicionalmente** → re-salvar um segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`) — o caso "editar a senha WP sem desconectar antes". Padrão dominante: **probe-first material** (Management API, todo teste em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify** — um achado HIGH do `/security-review` foi REFUTADO materialmente (o overwrite cross-tenant é fail-closed pelo `PRIMARY KEY`, md5 da vítima inalterado), mas a investigação revelou um gap REAL paralelo (injeção cross-tenant id-novo nas INSTEAD OF de meta/social), fechado na mesma sessão.
> 228	
> 229	**O que foi entregue:**
> 230	- **Idempotência (fecha o 23505 no re-save):** helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated → não é RPC alcançável) resolve o segredo por nome e rotaciona in-place via `vault.update_secret` (COALESCE-keep de nome/desc), senão cria; +fallback `unique_violation` p/ a corrida. As 3 encrypt triggers passam a usá-lo + ganham `search_path=''`. A coluna mantém o MESMO UUID Vault entre rotações (sem órfãos). Migration `20260602140000`.
> 231	- **Guard de tenant (fecha injeção cross-tenant):** as INSTEAD OF de `meta_config`/`social_accounts` não tinham o guard `auth.uid()` da `130000`. Views `SECURITY DEFINER` + o WHERE de view não restringe INSERT → autenticado injetava credencial em nome de outro (user_id spoofado + id novo). Guard `42501` portado pras branches INSERT+UPDATE das 2, recriadas **verbatim** do `pg_get_functiondef` live + `search_path=''`. `service_role` isento. Migration `20260602150000`.
> 232	
> 233	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (escopo aprovado: "analise tudo e faça"; toda ação outward com prova material por turno, rolled-back).
> 234	
> 235	| Verificação | Resultado |
> 236	|---|---|
> 237	| 23505 no re-save (prova do bug) | ✅ reproduzido — `ERROR 23505 secrets_name_idx ... trg_encrypt_user_api_keys() line 72` |
> 238	| Re-save pós-fix (`user_api_keys`) | ✅ `{decrypted_wp:"wp-pass-BRAVO", secret_count:1, col_is_uuid_ref:true, sibling_groq_intact:true}` |
> 239	| Re-save pós-fix (`social_accounts`, linha real `39ce0ebb…`) | ✅ `{decrypted_access:"sa-BRAVO", secret_count:1}` |
> 240	| Helper lockdown | ✅ EXECUTE anon/authenticated=false; postgres=true |
> 241	| Injeção cross-tenant ANTES | ✅ atacante criou `meta_config` da vítima (`decrypted_token:"INJECTED-BY-ATTACKER"`) |
> 242	| Injeção cross-tenant DEPOIS | ✅ `42501` nas 2 tabelas; self-insert + `service_role` intactos |
> 243	| HIGH do `/security-review` (overwrite) | ✅ REFUTADO material — PK fail-closed (`23505 social_accounts_pkey`) + md5 vítima inalterado |
> 244	| `tsc --noEmit` | ✅ 0 erros |
> 245	| 2 migrations `/security-review` | ✅ ambas **SAFE** |
> 246	| Migrations aplicadas (Mgmt API, txn) | ✅ `20260602140000`+`20260602150000` no `schema_migrations` |
> 247	| Cleanliness | ✅ meta=0/social=3 linhas · 0 segredos de teste · dados reais intactos |
> 248	| Mesh | ✅ 8751 nós |
> 249	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 250	| Handoff node | ✅ `ea6a3a17-2804-4de3-b153-31f823a9fdb5` embedded 768d |
> 251	
> 252	| Commit | Conteúdo |
> 253	|---|---|
> 254	| `2db5f62` | fix(credentials): vault_upsert_secret idempotente — elimina 23505 ao rotacionar segredo |
> 255	| `87c926f` | fix(credentials): guard de tenant nas INSTEAD OF de meta_config/social_accounts |
> 256	| `deb661c` | docs(processes): fecha débito de idempotência + guard meta/social no SOP |
> 257	| `beec4aa` | docs(readme): v6.20.2 |
> 258	
> 259	### Arquitetura — idempotência + isolamento de tenant na camada Vault
> 260	```
> 261	RE-SAVE (rotação): encrypt trigger → public.vault_upsert_secret(value,name,desc)
> 262	                   SELECT id FROM vault.secrets WHERE name=p_name
> 263	                     achou → vault.update_secret(id,value)   [mesmo UUID, só rotaciona o valor]
> 264	                     senão → vault.create_secret(...)        [unique_violation → re-resolve+update]
> 265	GUARD (meta/social INSTEAD OF, branches INSERT+UPDATE):
> 266	   auth.role()<>'service_role' AND NEW.user_id<>auth.uid() → 42501
> 267	   (DELETE fica SEM guard de propósito — o WHERE da view mascarada já filtra DELETE/UPDATE/SELECT;
> 268	    só INSERT escapa do WHERE → é exatamente onde o guard entra)
> 269	```
> 270	
> 271	### Survival Laws Self-audit
> 272	```
> 273	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API, tudo rolled-back — 23505 reproduzido + before/after de re-save (user_api_keys + social_accounts) + lockdown do helper + injeção antes/depois (42501) + metadados pós-apply + cleanliness. Zero fabricação. Achado HIGH do /security-review REFUTADO com teste material (PK fail-closed + md5 da vítima inalterado), não com argumento. 1 armadilha de ambiente divulgada (`UID` readonly do bash → `$U`). Fase 5c executada abaixo.
> 274	Law 2 (Process): ✅ SOP credential-disconnect-clear.md atualizado (débito → Resolved + bloco de isolamento de tenant) antes do commit; CLAUDE.md Key Files. Bug fix em features documentadas → sem BoK gate.
> 275	Law 3 (Pruning): investigação longa (probes C1-C4, V1-V2, before/after meta+social) — outputs consumidos, referência por path/UUID/migration.
> 276	Law 4 (ORO): ✅ declarado no início; "analise tudo e faça" = autorização autônoma do Sovereign p/ resolver em-sessão + selar.
> 277	```
> 278	
> 279	**Pendências/Próximos (anotados p/ próxima sessão):**
> 280	- ~~**Segredo órfão no disconnect Meta/social:** desconectar Meta (`useMetaConfig.disconnect`) ou social deleta só a linha base via INSTEAD OF DELETE — o segredo Vault (`meta_config_long_lived_token_<id>` etc.) **fica órfão** (plaintext retido). Paralelo ao que `disconnect_wordpress()` resolveu pro WP; precisa de RPC dedicada (nula linha + revoga segredo) + `/security-review`. Débito LGPD/retenção.~~ ✅ **FECHADO 2026-06-02 (v6.20.3)** — RPCs `disconnect_meta()`/`disconnect_social(uuid)` (migration `20260602160000`); 12 segredos Meta órfãos limpos (12→0); ver Record no topo.
> 281	- **E2E no navegador:** verifiquei PostgREST + triggers + Vault pela perspectiva do banco; o clique na UI logada não foi executado (browser autenticado indisponível).
> 282	
> 283	---
> 284	
> 285	## WordPress BYOK Credential-Write Fix + Encrypt Double-Fire Record (2026-06-02)
> 286	
> 287	**v6.20.1 (2026-06-02)** — Sessão disparada pelo P0 que a própria seal v6.20.0 sinalizou: `SocialAccountsPage` salvava/desconectava WordPress via `.upsert(onConflict)` numa VIEW mascarada. Corrigir os 2 `.upsert` reportados revelou um bug **muito maior e pré-existente** na camada `credential_encryption`: o `INSTEAD OF` do `user_api_keys` disparava o trigger de encriptação **2×** numa só statement → `23505`, quebrando connect/save de **qualquer** usuário com linha já existente (não só WP). Padrão dominante: **probe-first material** (Management API) — cada hipótese provada antes de codar, o que pegou o double-fire (que o `.insert` sozinho não resolveria), a colisão do sentinela `••••` no `.update`, e uma escrita cross-tenant que o `ON CONFLICT` mascarava com o crash.
> 288	
> 289	**O que foi entregue:**
> 290	- **Fix dos 2 `.upsert` (SocialAccountsPage):** save → `.insert()` (roteia pelo INSTEAD OF que faz upsert interno; `.upsert` numa view dá HTTP 400 `42P10`); disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `search_path=''`, escopada a `auth.uid()`) que nula as 3 colunas WP **e deleta o segredo do Vault** (revogação real LGPD; delete amarrado a `id` E nome determinístico → tenant-safe). `null` não limpa via view (guard `COALESCE-NULLIF` preserva). Migration `20260602120000`.
> 291	- **[Descoberto] Fix do double-fire:** `trg_instead_of_user_api_keys` trocado de `INSERT...ON CONFLICT DO UPDATE` (dispara encrypt 2× → `vault.create_secret` nome duplicado → `23505`; `.update` ainda re-encripta o `••••`) para **UPDATE-first / INSERT-if-not-found** (encrypt 1×, igual aos irmãos meta/social) + **guard de tenant** (`auth.uid()` → `42501`). `wp_site_url`/`wp_username` viraram `COALESCE(NEW,base)` (não zeram em save parcial). Migration `20260602130000`. Só `user_api_keys` usava `ON CONFLICT`.
> 292	- **types.ts** regenerado (inclui `disconnect_wordpress`); **SOP** `docs/processes/credential-disconnect-clear.md` (Lei 2 + Obstáculo→Síntese); 3 entradas na Key Files Reference.
> 293	
> 294	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (escopo profundo aprovado explicitamente via AskUserQuestion; toda ação outward com provas materiais por turno).
> 295	
> 296	| Verificação | Resultado |
> 297	|---|---|
> 298	| `.upsert` na view (prova do bug) | ✅ HTTP **400 `42P10`** reproduzido |
> 299	| connect pós-fix (caso 23505) | ✅ persiste + cifra (base=UUID, 1 segredo Vault), groq intacto |
> 300	| `.update` pós-fix (caso 23505 groq) | ✅ sucesso, sem re-encriptar `••••`, `wp_site_url` preservado |
> 301	| `disconnect_wordpress()` | ✅ 3 cols `null` + segredo Vault deletado + AI keys intactas |
> 302	| guard cross-tenant | ✅ `ERROR 42501 cannot write credentials for another user` |
> 303	| `tsc --noEmit` | ✅ 0 erros |
> 304	| 2 migrations `/security-review` | ✅ ambas **SAFE** |
> 305	| `db push` (ambas) | ✅ Finished · `20260602120000`+`20260602130000` no remoto |
> 306	| Frontend deploy (nginx) | ✅ chunk `SocialAccountsPage-4_GWJ_p-.js` com `disconnect_wordpress`, `.env` baked |
> 307	| Mesh | ✅ 8750 nós |
> 308	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 309	| Handoff node | ✅ `7bf9bb0e-a063-43d9-b473-0dd7cdfc97d3` embedded 768d |
> 310	
> 311	| Commit | Conteúdo |
> 312	|---|---|
> 313	| `5dc8084` | fix(credentials): disconnect_wordpress RPC + elimina double-fire do INSTEAD OF |
> 314	| `bafa7a2` | fix(settings): WordPress conecta via .insert e desconecta via RPC |
> 315	| `377251e` | docs(processes): SOP de disconnect/clear de credencial |
> 316	| `6b2f8db` | docs(readme): v6.20.1 |
> 317	
> 318	### Arquitetura — write/clear de credencial nas views Vault-mascaradas
> 319	```
> 320	SAVE  (cliente): .insert() → INSTEAD OF (UPDATE-first / INSERT-if-not-found) → encrypt trigger 1× → vault.create_secret
> 321	                 guard: auth.role()<>'service_role' AND NEW.user_id<>auth.uid() → 42501
> 322	CLEAR (cliente): supabase.rpc('disconnect_wordpress') → SECURITY DEFINER auth.uid() →
> 323	                 UPDATE base SET wp_*=NULL + DELETE vault.secrets WHERE id=ref AND name='...<uid>'
> 324	NUNCA: .upsert (400 42P10) · null-write via view (COALESCE preserva) · INSERT...ON CONFLICT (double-fire 23505)
> 325	```
> 326	
> 327	### Survival Laws Self-audit
> 328	```
> 329	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API — 400 42P10 real, connect/disconnect/guard com SELECT em decrypted_user_api_keys + vault.secrets, db push Finished, 2 /security-review SAFE, chunk servido com a string nova, node 7bf9bb0e embedded. Zero fabricação. O double-fire foi PROVADO (T1/T3/T4 + vault.create_secret = INSERT sem ON CONFLICT) antes de afirmar que existia. Fase 5c executada abaixo.
> 330	Law 2 (Process): ✅ SOP credential-disconnect-clear.md antes do commit; dívida residual documentada + task spawned.
> 331	Law 3 (Pruning): contexto longo de investigação (T1-T5) — outputs de exploração consumidos, referência por path/UUID.
> 332	Law 4 (ORO): ✅ declarado no início; escopo profundo aprovado explicitamente pelo Sovereign via AskUserQuestion.
> 333	```
> 334	
> 335	**Pendências/Próximos (anotados p/ próxima sessão):**
> 336	- ~~**Dívida residual (task spawned):** tornar `trg_encrypt_user_api_keys` (+ irmãos meta/social) idempotente (update-or-create por nome) — editar um segredo p/ valor novo sem desconectar antes ainda dá `23505`.~~ ✅ **FECHADA em v6.20.2** (migration `20260602140000`, helper `vault_upsert_secret`; + guard de tenant meta/social `20260602150000`).
> 337	- **E2E no navegador:** verifiquei todas as camadas abaixo da UI (PostgREST 400/201 + triggers + RPC + Vault); o clique na UI logada não foi executado (browser autenticado indisponível).
> 338	
> 339	---
> 340	
> 341	## Afiliados Híbrido + Catálogo Apify Real + BYOK per-user Record (2026-06-01)
> 342	
> 343	**v6.20.0 (2026-06-01)** — Sessão disparada pelo Sovereign dogfoodando `/dashboard/affiliate-products`: o link de afiliado copiado abria a **tela de login do CloudPanel** em vez do produto. Fluxo: diagnóstico material → fix dos links → enriquecimento do catálogo → descoberta de produtos → BYOK per-user → seal. Padrão dominante: **probe-first** (provar materialmente antes de construir) — economizou esforço em 3 becos (API ML, Firecrawl, actor com selectors velhos) e pegou 2 IDs fabricados + 1 regressão de credencial no `/security-review`.
> 344	
> 345	**O que foi entregue:**
> 346	- **Fix dos links de afiliado (híbrido meli.la/matt_word):** o catálogo e `process-affiliate-link` (GET+POST) roteavam via `panel.gcrux.com/api/ml-redirect` (proxy morto = login wall, zero atribuição) usando o `app_id` OAuth como affiliate id — ambos banidos pelo SOP. Agora resolve em camadas: short link `meli.la` **cravado** (per-user em `affiliate_config.metadata.shortlinks[MLB]`) quando existir, senão `product_url` real + `matt_word=<affiliate_tag>`, **fail-closed**. `src/lib/affiliate.ts` puro (`resolveAffiliateLink`/`buildMattWordUrl`/`isMlShortLink`/`readShortlinks`) + 14 testes; editor de link cravado por produto na página; `useAffiliateConfig` expõe `affiliate_tag` + `setProductShortlink`. Prova: 302s reais da edge function — `MLB27834876`→`meli.la/2gh13Sw` (override) · `MLB36263268`→`mercadolivre.com.br/p/...?matt_word=caga6077534` (fallback), zero `panel.gcrux.com`.
> 347	- **Catálogo real via Apify (ML bloqueia todo server-side):** provado materialmente que `api.mercadolibre.com/{items,products,search,categories}` → 403/401 e a página → 302 `/gz/account-verification`, **tanto do nosso IP quanto da Supabase Edge** (probe `ml-probe` deployada+deletada). OAuth não furaria (IP-block). Único caminho: actor Apify residencial `karamelo~mercadolivre-scraper-brasil-portugues` (devolve `eTituloProduto`/`novoPreco`/`imagemLink`/`SKU`). `scripts/enrich-affiliate-products.ts` (busca por nome → casa `SKU===external_id` → preço/foto/disponibilidade, retry anti-bot intermitente, resolução token per-user→sistema) + `scripts/discover-affiliate-products.ts` (descoberta real — valida "viral mind") + `useAffiliateProducts` gate (só lista `is_active`+`price`+`availability=available`; `hiddenCount`) + cron `affiliate-enrich-cron.sh` 6/6h.
> 348	- **2 produtos fabricados removidos:** `MLB36263268`/`MLB37674259` eram IDs inventados (link-forge hardcoded — nunca "descobertos"); busca real retornou SKUs reais diferentes → DELETE permanente. Catálogo agora: **3 produtos reais novos** — Roborock S8 Pro Ultra `MLB27834876` R$17.770 · Family Hub `MLB32642694` R$18.946 · 75" 8K Neo QLED QN900B `MLB4699602679` R$39.000 (todos `available`, foto+preço reais).
> 349	- **BYOK per-user `apify_token`:** migration `20260601060000` adiciona `apify_token` no padrão Vault de `credential_encryption` (coluna → trigger cifragem → view mascarada → INSTEAD OF → decrypted view service_role-only) — **passou `/security-review`**, que pegou e corrigiu eu revertendo a view mascarada p/ `security_invoker` sem o `WHERE` (quebraria leitura authenticated). Resolução em camadas per-user→`APIFY_TOKENS` sistema (provada: `--user` resolveu o token do Sovereign e dirigiu um scrape real). Campo no `SettingsPage`. **Corrige P0 pré-existente de `000600`:** `useUserApiKeys.saveKeys` usava `.upsert()` → HTTP 400 (view sem constraint) → `.insert()` (INSTEAD OF trigger faz upsert via `ON CONFLICT user_id`).
> 350	
> 351	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (todas as ações outward — DB writes, deploys, migration Vault, gasto Apify — com GO explícito; provas materiais por turno).
> 352	
> 353	| Verificação | Resultado |
> 354	|---|---|
> 355	| `tsc --noEmit` | ✅ 0 erros |
> 356	| Suite vitest | ✅ **238 passed / 2 skipped / 240** (+14 testes `affiliate.test.ts`) |
> 357	| Migration Vault aplicada | ✅ `db push` exit 0 · chaves existentes ainda decifram (openrouter/groq) · `apify_token` round-trip OK · mascarada na view pública |
> 358	| `/security-review` | ✅ 0 findings + pegou/corrigiu regressão `security_invoker` |
> 359	| BYOK per-user funcional | ✅ `--user` → token resolvido → scrape Roborock matched R$17.770 |
> 360	| Edge 302s (deploy 82.73 kB) | ✅ override→meli.la · fallback→ML real · zero panel.gcrux |
> 361	| Frontend deploy (nginx) | ✅ chunks `AffiliateProductsPage`/`SettingsPage` servidos HTTP 200 com código novo |
> 362	| Cron monitoramento | ✅ `0 */6 * * *` instalado (vizinhos intactos) |
> 363	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 364	| Handoff node | ✅ `af33a839-acd9-412d-a770-8ad5a2edccb4` embedded 768d |
> 365	
> 366	| Commit | Conteúdo |
> 367	|---|---|
> 368	| `4a9df8d` | feat(afiliados): links híbridos meli.la/matt_word — fim do proxy morto |
> 369	| `5288bb8` | feat(afiliados): enriquecimento Apify + descoberta + gate + cron |
> 370	| `fb07323` | feat(settings): BYOK Apify token per-user (Vault) + fix salvamento de chaves |
> 371	| `adcbd6f` | docs(afiliados): SOPs + revenue-flywheel com IDs reais |
> 372	| `eb9653d` | docs(readme): v6.20.0 |
> 373	
> 374	### Arquitetura — resolução de link de afiliado (híbrida, OTD-ML-001)
> 375	```
> 376	resolveAffiliateLink(product, config):
> 377	  1. config.metadata.shortlinks[external_id] é meli.la/sec?  → { shortlink }   (definitivo, per-user)
> 378	  2. config.affiliate_tag presente?  → product_url + ?matt_word=<tag>+utm      (best-effort)
> 379	  3. senão → { needs_config }  (fail-closed — nunca link sem atribuição)
> 380	process-affiliate-link GET (clique do leitor): node→owner→affiliate_config → mesma resolução → 302 ML real
> 381	Enriquecimento: Apify karamelo (residencial) → SKU match → vm_affiliate_products{price,image_url,availability}
> 382	  token: per-user (decrypted_user_api_keys.apify_token) → sistema (APIFY_TOKENS)
> 383	```
> 384	
> 385	### Survival Laws Self-audit
> 386	```
> 387	Law 1 (Materiality): ✅ toda claim provada NESTE turno — 302s reais, db push exit 0, round-trips (sem imprimir segredo), suite 238/240, nginx 200, scrape matched. Quando o ML bloqueou tudo, disse "não dá" (probe ml-probe) em vez de fabricar. O 8K errado (4K→usado) foi corrigido materialmente 2×, não maquiado. Fase 5c executada (veredito mecânico abaixo).
> 388	Law 2 (Process): ✅ 2 SOPs (ml-affiliate-attribution atualizada + affiliate-catalog-enrichment nova) antes/junto do código. Migration passou /security-review (regra CLAUDE.md). API Tenancy (per-user→sistema) honrada.
> 389	Law 3 (Pruning): ✅ checkpoint explícito antes do BYOK (item de maior blast radius isolado); probes (Firecrawl/ml-probe) extraídos a conclusão e deletados.
> 390	Law 4 (ORO): ✅ triplet declarado; toda ação outward com GO Sovereign.
> 391	```
> 392	
> 393	**Pendências/Próximos (anotados p/ próxima sessão):**
> 394	- **Operador de Browser Autenticado (módulo novo — PROBE-FIRST):** browser LOGADO humano-paced p/ ações que nos barram (canônico: ML "Compartilhar" → `meli.la` cravado → gravar em `shortlinks`). Datacenter IP bloqueado até p/ browser real; logado não-testado. Decisões Sovereign: probe de viabilidade → runtime decidido após probe → `/bok-scribe` (BoK Gate) → build. Auth = login interativo 1×+profile persistido, sem senha crua. Tool: `agent-browser`. Memória: `project_authenticated_browser_operator`.
> 395	- **P0 pré-existente (de `000600`, NÃO desta sessão) — task spawnada:** `SocialAccountsPage.tsx:51,68` salva/desconecta WordPress via `user_api_keys.upsert(onConflict)` → 400, e disconnect com null não limpa (COALESCE-guard). Fix: `.insert()` + clear via service-role. Memória: `reference_encrypted_views_write_pattern`.
> 396	- **8K via keyword é fuzzy:** descoberta do 8K exigiu filtro de título (`\b8k\b` + NEW) — keyword "8k" sozinha traz 4K. Refinar termos por categoria ao descobrir.
> 397	
> 398	---
> 399	
> 400	## e2e-user-zero v2 + 3-Stream Sweep Record (2026-06-01)
> 401	
> 402	**v6.19.0 (2026-06-01)** — Sessão de execução de 3 streams autorizados pelo Sovereign (e2e-user-zero 2ª iteração · gaps reais do Canvas · 1ª campanha real). Padrão dominante: **o código estava sistematicamente à frente dos próprios Pending Actions** — verificação material (Lei 1) ANTES de codar evitou reconstruir 2 features já prontas. Fluxo: `/handson` → priorização → descoberta de que Canvas 4.2 + consistência já estavam shipados → build real do Stream B → readiness do Stream C → seal.
> 403	
> 404	**O que foi entregue:**
> 405	- **Stream B — e2e-user-zero 2ª iteração (build real):** `scripts/qa/e2e-user-zero/lib/redactor.ts` (LGPD Layer 2 — redação de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body em `redactedPaths` + sanitização de cookie; `scanResidualSecrets` p/ o tripwire), `scripts/qa/e2e-user-zero/lib/mesh-persistor.ts` (finding → `observation` node + aresta `OBSERVES`, idempotente via SHA-256 do `name`, fail-soft, `SB_SECRET_KEY`), `scripts/qa/e2e-user-zero/lib/telemetry.ts` (pulse de ciclo de vida em `infra_health_logs`), 6 flows (`dashboard-tour`·`orchestrate-pipeline-view`·`content-library`·`billing-flow`·`settings-tour`·`constellation-view`) + helper `_nav-capture`, runner fiado (started/complete/failure/auth-expired exit-3 + persist), selftest vitest `src/test/e2e-user-zero-selftest.test.ts` (8 testes). Guard do runner endurecido (`includes("runner")` pegava `runner.test.ts`).
> 406	- **Stream A — consistência + Canvas 4.2 (VERIFICADO, não reconstruído):** auditoria material confirmou reference threading + seed-lock (`generateReplicate:675-690`·`generateOpenRouter:749-759` + inspectors/pipeline `findUpstreamImages` + toggle `fixedSeed`) e os 5 nós tipados + pipeline async de vídeo JÁ shipados. Único gap real fechado: `higgsfield-webhook` mapeia `nsfw`/`canceled` p/ razão clara de soft-fail (sem cobrança).
> 407	- **Pre-commit hardening + versionamento:** `scripts/hooks/pre-commit` (cópia versionada; antes só viva em `.git/hooks`) + README; PATTERN ampliado (`sk_/rk_(live|test)_`·`whsec_`·`sbp_`·`sb_secret_`·`r8_`) + tripwire de diretório que escaneia o `e2e-output/` gitignored (defesa Layer 4). Testado: bloqueia secret plantado (exit 1) · libera limpo (exit 0).
> 408	- **Stream C — readiness (gated):** flywheel sondado read-only — `orchestrate-content` HTTP 200, `affiliate_config` Sovereign `ada39fae` mercadolivre `is_active:true`, `mco_balance` 5351, Higgsfield creds presentes. Execução (publica + gasta) **gated em GO Sovereign**.
> 409	
> 410	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (Stream C paga/externa não disparada sem GO; deploy do `higgsfield-webhook` idem).
> 411	
> 412	| Verificação | Resultado |
> 413	|---|---|
> 414	| Selftest e2e-user-zero | ✅ 8/8 (vitest) |
> 415	| Suite completa | ✅ 224 passed / 2 skipped / 226 · **exit 0** — os 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` neste seal (antes falhavam por chave revogada); +8 desta sessão, baseline git-stash 218→226 |
> 416	| `tsc --noEmit` | ✅ 0 erros |
> 417	| Pre-commit tripwire | ✅ bloqueia secret em e2e-output (exit 1) · libera limpo (exit 0) · PATTERN pega sbp_ no staged-diff |
> 418	| Stream A consistência | ✅ wired backend+frontend — verificado por grep material, não reconstruído |
> 419	| Stream C readiness | ✅ orchestrate-content 200 · affiliate ativo · balance 5351 |
> 420	| Handoff node | ✅ `59f92fe0-e346-4320-aeaf-842a91458125` embedded 768d (chunks:1, openai/text-embedding-3-small) |
> 421	| Containers | ✅ 5 healthy · Chroma v2 OK |
> 422	
> 423	| Commit | Conteúdo |
> 424	|---|---|
> 425	| `cf6e464` | feat(e2e-user-zero): 2ª iteração — redactor + mesh-persistor + telemetry + 6 flows + selftest |
> 426	| `e788d76` | chore(hooks): versiona pre-commit + tripwire e2e-output |
> 427	| `09a5bae` | fix(higgsfield-webhook): nsfw/canceled soft-fail claro |
> 428	| `5f21caf` | docs(readme): v6.19.0 |
> 429	| `0c5eefd` | fix(tests): gateia smokes live (canvas pago + sql-bridge) atrás de RUN_LIVE_SMOKE → suíte verde |
> 430	
> 431	### Arquitetura — e2e-user-zero runner (v2)
> 432	```
> 433	runner.ts (focused) → emitRunStarted (telemetry)
> 434	  → flow(driver, ctx) [6 dashboard flows + auth-login, static whitelist]
> 435	  → classify() → buildReport() → report.md + findings.json
> 436	  → insertFindings() [mesh-persistor: observation node + OBSERVES edge, idempotent, fail-soft]
> 437	  → emitRunComplete (telemetry: infra_health_logs pulse) · exit 0/1/2/3
> 438	Defesa de segredo: redactor (Layer 2) → .gitignore e2e-output/ (Layer 3) → pre-commit tripwire (Layer 4)
> 439	```
> 440	
> 441	### Survival Laws Self-audit
> 442	```
> 443	Law 1 (Materiality): ✅ toda claim provada NESTE turno — selftest 8/8 + suite 224/226 + git-stash baseline (prova de zero regressão) + tsc 0 + hook testado (exit 1/0) + handoff node embedded via REST + readiness via curl real. Descoberta-chave: 2 features "pendentes" estavam shipadas (provado por grep de código real antes de codar) → zero retrabalho/fabricação. Excerpt do mesh-persistor do SDD corrigido contra schema real (relation_type + SB_SECRET_KEY).
> 444	Law 2 (Process): ✅ e2e-user-zero BoK 9/9 + SDD como SSOT. Webhook é fix em feature documentada. Desvio consciente: selftest em src/test/ (vitest include=src/**) — justificado. OTD-E2E-TELEM-001 registrada (infra_health_logs sem coluna metadata → migration aditiva diferida a /security-review).
> 445	Law 3 (Pruning): ✅ 2 podas explícitas (relatórios dos subagentes após extração de conclusões; detalhes de impl do Stream B no checkpoint).
> 446	Law 4 (ORO): ✅ triplet por stream; Stream C paga/externa gated em Sovereign.
> 447	```
> 448	
> 449	---
> 450	
> 451	## Constellation v2 Cockpit Live — Fase 3+4 E2E + Build/Login/Settings Fixes Record (2026-06-01)
> 452	
> 453	**v6.18.0 (2026-06-01)** — Sessão densa que levou a Constelação v2 de casca decorativa a **cockpit operacional per-user provado ponta-a-ponta**, mais 3 incidentes de produção resolvidos (build quebrado, P0 login, teste de chaves). Fluxo: `/handson` → resolver alertas prioritários → Fase 3 UI → (o gate de build revelou um blocker pré-existente do lucide) → P0 login reportado pelo Sovereign → Fase 0 reset destrutivo → botão Zerar → teste de chaves falhando (descoberta da cripto de credenciais) → Tabs → Fase 4 E2E provado → este selo.
> 454	
> 455	**O que foi entregue:**
> 456	- **Fase 3 — cockpit (`constellation-v2`, BoK selada `38d7e7a4`):** empty-state com CTA duplo (`EmptyConstellation`) + wizard 2-portas (`CrewWizard` + `useCreateCrew`: mapa 4×4 = Núcleo + 4 Leads + 13 subagentes módulo-bound, OU builder guiado depto→capability→nome) com keys estáveis (FR-CV2-006) + upsert idempotente; `AccessConfigCard` (BYOK + cap diário por subagente, FR-CV2-023); `useAgentTask`+`agent-task-result` (FR-CV2-004: envia `capability_key`, trata 402/422/502+`status:failed`); `useAgentActivity` projeta capability/result nos Live Logs (FR-CV2-050); `CrewGraph` cap≤21 + LOD + z-index estrito (FR-CV2-060/061); botão legado "Deploy Enterprise" → "Criar crew".
> 457	- **Fase 0 — reset destrutivo:** `scripts/reset-constellation-v2.ts --execute` arquivou 35 execs → wipou 746 crew_agents + 717 crew_edges → 0; `profiles`=1 intacto. Verificado independente via REST.
> 458	- **Botão "Zerar" per-user** (`useResetCrew`, RLS-scoped a `auth.uid()`): qualquer user reinicia do zero / re-semeia o 4×4 quando quiser. Preserva `mco_balance` e histórico.
> 459	- **Blocker de build (pré-existente) morto:** `lucide-react@1.x` removeu os ícones de marca → `vite build` (rollup) quebrava em `MetaConfigCard`/`v0-ai-chat` enquanto o dev (esbuild) tolerava → produção servia bundle stale de May-30. Fix: shim local `src/components/icons/brand-icons.tsx` + anticorpo `scripts/qa/audit-lucide-imports.ts` (cruza imports de lucide vs exports reais).
> 460	- **P0 login (outage):** o bundle vivo assava uma publishable key que a migration de cripto rotacionou/desregistrou (`UNAUTHORIZED_UNREGISTERED_API_KEY` em `/auth/v1/user`); redeploy assou a registrada do `.env`. Env-driven (`client.ts` lê `import.meta.env`), então o rebuild foi o fix. Lição na memória [[reference_supabase_keys_migrated]].
> 461	- **Teste de chaves server-side + Tabs:** `user_api_keys` é VIEW que mascara (migration `credential_encryption`); o cliente só via `••••` → teste client-side mandava o mask → 401 sempre ("Falhou" ≠ chave inválida). Edge fn `test-api-key` (JWT-guarded) resolve a chave real (`decrypted_user_api_keys` ou valor digitado) e testa server-side (cobre Replicate, que bloqueia CORS). 4 seções de Settings em Tabs. Lição na memória [[reference_user_api_keys_encrypted]].
> 462	
> 463	**Prova material da Fase 4 (E2E):** exec `488a7744-ceb6-4048-a482-f78462e0aa2a` → capability `watchdog_infra` → `get-infra-status` → `done` · `cost_mcoin` 0 · `latency_ms` 255 · `result_summary` `{"chroma":"healthy","intelligence":"healthy",...}` (output real do módulo). Primeira execução real no cockpit per-user pós-reset, com o nó pulsando e o Live Logs exibindo o resultado.
> 464	
> 465	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (Fase 0 destrutiva + deploys de produção autorizados explicitamente; blast radius: 746 crew decorativos apagados/arquivados, `profiles`+ledger preservados).
> 466	
> 467	| Verificação | Resultado |
> 468	|---|---|
> 469	| Fase 4 E2E exec | ✅ `488a7744` done · watchdog_infra · 0 mco · 255ms · result real |
> 470	| Fase 0 reset | ✅ crew 0 · archive 35 · profiles 1 (REST independente) |
> 471	| Build lucide | ✅ audit 5835 exports limpo · `built in ~22s` · prod desbloqueado |
> 472	| P0 login | ✅ index.html → `index-BY2MQsU-` → chave `FkE` registrada · chunks velhos 404 |
> 473	| `test-api-key` edge fn | ✅ deploy 103.5kB · OPTIONS 200 · sem JWT 401 |
> 474	| Chaves no Vault | ✅ `decrypted_user_api_keys` = reais válidas (prefixos `gsk_`/`sk-o`/`sk-p`/`AIza`/`r8_`) |
> 475	| `tsc --noEmit` | ✅ 0 erros |
> 476	| Handoff node | ✅ `a0eb5da7-d2b1-43b0-9ee6-cfb6cccd14c9` embedded 768d |
> 477	| Mesh total | **8746 nós / 9070 arestas** (REST count=exact) |
> 478	| Containers | ✅ 5 healthy |
> 479	
> 480	| Commit | Conteúdo |
> 481	|---|---|
> 482	| `9a4b569` | fix(build): lucide brand-icon shim + audit antibody |
> 483	| `7b2b277` | feat(constellation-v2): Fase 3 cockpit + wizard + capability real |
> 484	| `8ed3f78` | docs: runbooks → SB_SECRET_KEY |
> 485	| `9a13545` | feat(constellation-v2): botão Zerar per-user |
> 486	| `8a0c547` | fix(settings): teste de chaves server-side |
> 487	| `1dacd10` | feat(settings): tabs IA/WordPress/Meta/LGPD |
> 488	| `18dd696` | docs(readme): v6.18.0 |
> 489	
> 490	### Arquitetura — capability execution (v2)
> 491	```
> 492	Subagente (capability_key) → AgentDetail "Executar capability"
> 493	  → agent-task-execute (ramo capability): resolve agent_capabilities allowlist → denylist sistema → cap check
> 494	  → invoke target_function (get-infra-status) c/ JWT do user → meter (module_self_bills → 0)
> 495	  → agent_executions (done, result_summary) → useAgentActivity → Live Logs + pulse 3D
> 496	```
> 497	
> 498	### Arquitetura — credenciais BYOK (descoberta da sessão)
> 499	```
> ```

## 🤖 Claude *(14:06:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 6080,
  "limit": 390
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 6080	          → handleMonetizeLinks(item):
> 6081	               match(ML_URL_RE) → unique URLs
> 6082	               for url of unique:
> 6083	                 POST process-affiliate-link → affiliate_url
> 6084	                 body.split(url).join(affiliate_url)
> 6085	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 6086	          → Badge 💰 ML (emerald) exibido após monetização
> 6087	```
> 6088	
> 6089	---
> 6090	
> 6091	## Pending Actions (Commercial Launch)
> 6092	
> 6093	### CRITICAL — Must complete before first client
> 6094	
> 6095	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 6096	
> 6097	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 6098	
> 6099	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 6100	
> 6101	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 6102	
> 6103	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 6104	
> 6105	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 6106	
> 6107	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 6108	
> 6109	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 6110	
> 6111	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 6112	   ```bash
> 6113	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 6114	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 6115	   ```
> 6116	
> 6117	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 6118	
> 6119	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 6120	
> 6121	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 6122	
> 6123	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 6124	
> 6125	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 6126	
> 6127	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 6128	
> 6129	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 6130	
> 6131	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 6132	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 6133	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 6134	
> 6135	### SOCIAL — Next steps
> 6136	
> 6137	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 6138	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 6139	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 6140	
> 6141	### NON-CRITICAL
> 6142	
> 6143	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 6144	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 6145	- `browserslist` — ✅ updated (2026-04-26)
> 6146	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 6147	
> 6148	### GITNEXUS MCP — Next steps
> 6149	
> 6150	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 6151	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 6152	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 6153	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 6154	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 6155	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 6156	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 6157	
> 6158	### PHASE EPSILON — Next iterations
> 6159	
> 6160	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 6161	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 6162	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 6163	
> 6164	### CORE — Next iterations
> 6165	
> 6166	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 6167	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 6168	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 6169	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 6170	
> 6171	### PHASE DELTA — Next iterations
> 6172	
> 6173	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 6174	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 6175	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 6176	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 6177	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 6178	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 6179	
> 6180	### USUÁRIO ZERO — Checklist de validação
> 6181	
> 6182	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 6183	- ✅ Stripe sandbox secrets no vault
> 6184	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 6185	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 6186	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 6187	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 6188	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 6189	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 6190	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 6191	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 6192	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 6193	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 6194	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 6195	
> 6196	---
> 6197	
> 6198	## Infrastructure
> 6199	
> 6200	| Service | Container | Port | Status |
> 6201	|---------|-----------|------|--------|
> 6202	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 6203	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 6204	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 6205	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 6206	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 6207	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 6208	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 6209	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 6210	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 6211	
> 6212	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 6213	
> 6214	```bash
> 6215	docker compose up -d
> 6216	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 6217	```
> 6218	
> 6219	---
> 6220	
> 6221	## Security Model (Post-Go-Live)
> 6222	
> 6223	| Table | Isolation |
> 6224	|-------|-----------|
> 6225	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 6226	| `mcorch_edges` | Same pattern |
> 6227	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 6228	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 6229	
> 6230	---
> 6231	
> 6232	## Billing Architecture
> 6233	
> 6234	| Decision | Value |
> 6235	|----------|-------|
> 6236	| Canonical billing ledger | `profiles.mco_balance` |
> 6237	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 6238	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 6239	| Orchestration cost | 10 mcoCoins/run |
> 6240	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 6241	| Stripe | Sandbox keys active — swap to live before first client |
> 6242	
> 6243	---
> 6244	
> 6245	## GraphRAG State
> 6246	
> 6247	- **8759 total nodes** (v6.22.0: +handoff `aec4cb9c` +milestones MVP-2 `7628892b`/OTD `6061a6d2`; was 8755 in v6.21.0)
> 6248	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 6249	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 6250	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 6251	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 6252	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 6253	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 6254	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 6255	- HNSW cosine index operational
> 6256	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 6257	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 6258	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 6259	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 6260	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 6261	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 6262	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 6263	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 6264	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 6265	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 6266	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 6267	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 6268	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 6269	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 6270	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 6271	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 6272	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 6273	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 6274	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 6275	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 6276	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 6277	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 6278	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 6279	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 6280	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 6281	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 6282	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 6283	
> 6284	### Embedding Model
> 6285	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 6286	Schema: `vector(768)` — HNSW cosine index.
> 6287	
> 6288	### Embedding Pipeline (Autônomo — 2026-05-03)
> 6289	Três camadas eliminam intervenção manual:
> 6290	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 6291	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 6292	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 6293	
> 6294	### Comandos de manutenção da Mesh
> 6295	```bash
> 6296	# Verificar nós sem embedding (deveria retornar array vazio):
> 6297	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 6298	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 6299	
> 6300	# Backfill manual (Bun-native — requer .env):
> 6301	bun run scripts/backfill-embeddings.ts
> 6302	
> 6303	# Backfill de código-fonte nos nós AST:
> 6304	bun run scripts/backfill-node-content.ts
> 6305	
> 6306	# Re-sync AST completo:
> 6307	cd packages/gitnexus-core && npm run sync-mesh
> 6308	
> 6309	# Acompanhar re-ingesta pós-commit:
> 6310	tail -f /tmp/mcorch-ingest.log
> 6311	```
> 6312	
> 6313	---
> 6314	
> 6315	## Video Rescue Protocol
> 6316	
> 6317	When a video generation operation (Google Veo) times out or client disconnects:
> 6318	```bash
> 6319	# Via edge function (production):
> 6320	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 6321	  -H "Authorization: Bearer <user_jwt>" \
> 6322	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 6323	
> 6324	# Via local script (admin/debug):
> 6325	source .env && bun run rescue.ts <operation_id> <content_id>
> 6326	```
> 6327	
> 6328	---
> 6329	
> 6330	## Architecture Pillars
> 6331	
> 6332	| Layer | Implementation |
> 6333	|-------|---------------|
> 6334	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 6335	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 6336	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 6337	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 6338	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 6339	
> 6340	---
> 6341	
> 6342	## Phase Delta — Architecture
> 6343	
> 6344	```
> 6345	OrchestrationPage (full-canvas, p-0)
> 6346	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 6347	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 6348	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 6349	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 6350	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 6351	        ├── nodes/PublishNode.tsx    ← final distribution output
> 6352	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 6353	        └── NodePalette.tsx          ← top toolbar to add nodes
> 6354	
> 6355	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 6356	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 6357	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 6358	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 6359	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 6360	```
> 6361	
> 6362	### Canvas State Architecture (Hybrid)
> 6363	
> 6364	```
> 6365	User interaction → ReactFlow internal state (positions, drag)
> 6366	                         ↓ (debounced 600ms)
> 6367	                   localStorage (positions persist across refresh)
> 6368	                         ↑
> 6369	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 6370	     ↓ (status changes sync to ReactFlow via useEffect)
> 6371	ReactFlow renders visual status (idle/running/done/error/blocked)
> 6372	```
> 6373	
> 6374	## Key Files
> 6375	
> 6376	| Purpose | Path |
> 6377	|---------|------|
> 6378	| Architecture rules | `CLAUDE.md` |
> 6379	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 6380	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 6381	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 6382	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 6383	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 6384	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 6385	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 6386	| **Node types** | `src/components/orchestrator/nodes/` |
> 6387	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 6388	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 6389	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 6390	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 6391	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 6392	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 6393	| Billing utilities | `src/lib/billing.ts` |
> 6394	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 6395	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 6396	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 6397	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 6398	| Video rescue (local) | `rescue.ts` |
> 6399	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 6400	| Backfill script | `scripts/backfill-embeddings.ts` |
> 6401	| Deploy harness | `scripts/harness-deploy.sh` |
> 6402	
> 6403	---
> 6404	
> 6405	## First Client Onboarding Checklist
> 6406	
> 6407	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 6408	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 6409	3. ~~Activate watchdog cron~~ ✅ Done
> 6410	4. ~~Deploy rescue-video function~~ ✅ Done
> 6411	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 6412	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 6413	7. Monitor `infra_health_logs` for first 24h.
> 6414	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 6415	
> 6416	---
> 6417	
> 6418	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 6419	
> 6420	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 6421	
> 6422	| Action | Result |
> 6423	|--------|--------|
> 6424	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 6425	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 6426	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 6427	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 6428	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 6429	
> 6430	| Commit | Conteúdo |
> 6431	|--------|----------|
> 6432	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 6433	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 6434	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 6435	
> 6436	### Arquitetura Matrix Intelligence
> 6437	
> 6438	```
> 6439	ConstellationMatrix (Stabilized Engine)
> 6440	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 6441	  └── NodeDetailsPanel (Tabbed Navigation)
> 6442	        ├── Tab Meta: Neighbor exploration + Net Context
> 6443	        ├── Tab Code: Source code preview (Supabase sync)
> 6444	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 6445	
> 6446	useNodeIntelligence Hook:
> 6447	  - contentQuery: fetch nodes.content column
> 6448	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 6449	  - state: isAnalyzing, analysisResult, progress
> 6450	```
> 6451	
> 6452	---
> 6453	
> 6454	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 6455	
> 6456	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 6457	
> 6458	| Action | Result |
> 6459	|--------|--------|
> 6460	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 6461	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 6462	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 6463	
> 6464	**Output da análise (estruturado em pt-BR):**
> 6465	- Visão Geral — papel do módulo no sistema
> 6466	- Padrões Detectados — design patterns, antipatterns
> 6467	- Acoplamento & Dependências — análise In/Out-Degree
> 6468	- Recomendações — 1-3 ações priorizadas
> 6469	
> ```

## 🤖 Claude *(14:06:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-53 of 189 total (36519 tokens, cap 25000). Call Read with offset=54 limit=53 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.22.0 selado em 2026-06-03** — Campaign Core + LLM Fallback + Lead Scoring: 4 entregas materiais via `/handson`→ação nos alertas→próximos priores. **(1) Alerta meta_config** verificado **VAZIO** (0 linhas · `auth.users` 1==`profiles` 1 — não fabriquei limpeza inexistente, Lei 1). **(2) MVP-2 Campaign Core LIVE** (migration `20260603025256`): `campaigns` **ABSORVIDA** via `ALTER` (+intent/channels/mesh_node_id + `UNIQUE(id,user_id)`) + `campaign_steps` (FK composta tenant-`CASCADE`, espelha lead_events) + `marketing_attribution` (FK simples `SET NULL` + RLS `WITH CHECK`, espelha consents); tenant-FK provado **comportamental** (23503 + 42501 autenticado + 201 + zero-resíduo); `/security-review` **SAFE** (subagente independente); mesh `7628892b`. **(3) OTD-LLM-FALLBACK FECHADA cedo** (SLA 06-07, owner engineer): probe-first achou o helper já live em 11 fns → fechei o gap de observabilidade do SOP (telemetria `infra_health_logs` autossuficiente em Deno) + **1º teste de edge-helper do projeto** (6 casos) + 11 fns redeploy; mesh `6061a6d2`. **(4) lead-score LIVE** (FR-MH-003): JWT + 1 mco atômico + IA per-user→sistema fail-soft; **smoke E2E** 200 · score=80 (`source=ai`) · débito 100→99 · zero-resíduo. **Calibração mcoCoins**: `COIN_COSTS` centralizado + dívida **OTD-MCOIN-CALIBRATION** (o `10` é redondo, não $-calibrado; `orchestrate` cobra 10 flat < soma dos componentes 18; vídeo é o maior custo real). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8759**. Survival Laws **4/4**. 6 commits. **Novo Top Gap:** `campaign-run` cascata fiel (**ADIADA por decisão Sovereign** — código financeiro + contexto saturado, Lei 3) + OTD-MCOIN-CALIBRATION (preços $ por-modelo/vídeo) · MVP-4 hooks+UI `/dashboard/marketing` · MVP-5 attribution. **Lição:** probe-first pegou a OTD já 80% pronta (zero retrabalho) e a divergência `campaigns`/`campaign_metrics` já-existentes; decisão financeira de `campaign-run` **registrada ao Sovereign em vez de improvisada** (Master Protocol).
> 8	
> 9	**Sprint v6.21.0 selado em 2026-06-03** — Marketing Hub (v2): BoK 9/9 + 11 agentes + MVP-1 Lead Core LIVE. Novo **módulo soberano** criado do zero seguindo o Master Execution Protocol (BoK-first), dirigido pela diretiva Sovereign de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). `/bok-scribe` selou a **suíte BoK 9/9** (1732 LOC, `docs/bok/marketing-hub/`, traceability **0 órfãos**, mesh seal `d5163fed` DERIVES_FROM meta-api) — módulo nasce como **v2 de consolidação** que **absorve e escala** o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**), natureza **Ambos** (interno Usuário Zero + comercial per-tenant). `/bok-agents-generator` produziu o **sistema de 11 agentes** (8 BoK + AEO/Intent-Orchestration/Demand-gen + Pantheon Reconciliation). Após revisão Sovereign ("aprovado"), **MVP-1 Lead Core** foi ao ar: migration `20260603000000` (`leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` LGPD SECURITY DEFINER), aplicada via `db push`. O `/security-review` (subagente **independente**) pegou **1 cross-tenant MEDIUM** (FK de tabela-filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta tenant-escopada `(lead_id,user_id)→leads(id,user_id)`** + provado **material** (23503 no ataque, 201 no legítimo, cleanup zero-resíduo). Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8755**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** MVP-2 Campaign Core deve **ABSORVER** a `campaigns` já existente (colisão real achada por probe-first), NÃO criar nova; + MVP-3 edge fns (`lead-score`/`campaign-run`) · MVP-4 hooks+UI (`/dashboard/marketing`) · MVP-5 attribution. **Lição:** probe-first do schema ANTES de codar pegou 2 divergências doc↔realidade (`campaigns` existe, `projects` não) que quebrariam o apply; e o `/security-review` por subagente independente (não auto-avaliação) pegou o furo de tenant que o self-review deixou passar.
> 10	
> 11	**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 12	
> 13	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 14	
> 15	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 16	
> 17	**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 18	
> 19	**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> 20	
> 21	**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 22	
> 23	**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 24	
> 25	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 26	
> 27	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 28	
> 29	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 30	
> 31	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 32	
> 33	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 34	
> 35	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 36	
> 37	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 38	
> 39	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 40	
> 41	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 42	
> 43	**Sprint v6.1.0 selado em 2026-05-14** — Canvas Studio UX Shell + Higgsfield Fix: shell do Canvas Studio migrado do `viralmind-builder` (store Zustand+zundo, lanes overlay, TopBar/LeftPanel/StatusBar, catálogo de 9 receitas, ImageLightbox, PipelineEdge); `canvas-execute` com endpoint Higgsfield corrigido (`platform.higgsfield.ai` rota Soul) + RPC `deduct_mco_coins`. Plano Phase 4.2 selado em `~/.claude/plans/floating-sleeping-sparrow.md`.
> 44	
> 45	**Sprint v6.1.1 selado em 2026-05-14** — viralmind BoK Suite Sealed: dívida documental do override consciente do BoK Gate quitada. 6 docs autorados (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) + `04-frd` reescrito de handbook CLAUDE.md → FRD real (32 FR + 14 NFR + matriz PR→FR). Ancorado nas 10 tabelas `vm_*` + 6 enums + Edge Functions `fetch-trends`/`canvas-execute`. Mesh seal `bok-scribe-seal-viralmind-v1` (`documentation_suite`, stability 0.85, revenue_impact R\$14M, embedded 768d). 7 OTDs registrados (destaques: `vector(1536)` vs padrão `768` sem índice HNSW — FMEA-VM-002 RPN 288; bucket `canvas-assets` público — FMEA-VM-003 RPN 140). BoK Gate do viralmind **liberado**. Sessão selada com ~51% de contexto — Canvas Studio Phase 4.2 diferida para sessão nova. 7463 nós · 100% embedded. 6 commits granulares. **Pendência conhecida (não desta sessão):** `docs/bok/gamificacao-nodes/` incompleta (5/9 docs) — rodar `/bok-scribe` ou completar antes de tocar o módulo.
> 46	
> 47	**Sprint v6.6.9 selado em 2026-05-20** — mcorch-qa-healing v1 — Material Proof Gate: novo módulo de QA sênior que fecha a fraqueza de Lei 1 (Materialidade) — o bloco Survival Laws Self-audit do `/handoff` era auto-declarado; agora é verificado mecanicamente pela nova **Fase 5c**. Executado em 6 stages na ordem de governança não-negociável (BoK → SOP → código): suíte BoK 9/9 `docs/bok/mcorch-qa-healing/` (1423 LOC, 6ª suíte do projeto, gerada via `/bok-scribe`, campos de mercado/monetização honestamente N/A para tooling interno) + SOP `docs/processes/handoff-material-proof-audit.md` (Lei 2) + engine `scripts/qa/` (5 módulos Bun, 710 LOC, injeção de dependências para reuso pelo cron OpenClaw) + skill `mcorch-qa-healing` + Fase 5c wired no `/handoff` (entre 5b e 6 — bloqueia em qualquer 🔴) + 2 suítes Vitest. O dry-run contra o selo v6.6.8 real pegou e fechou um falso-positivo (`COMMIT_RE` agarrava prefixos de UUID de 8-hex como commits — FMEA-002 fechada antes do gate ir ao ar). **Material proofs**: TS zero erros · 165 testes (122→165, +43) · **Fase 5c ao vivo neste selo → 13 verified · 0 skipped · 0 failed → SEAL ALLOWED** · 9 commits granulares · milestone node `a08780dc-f665-47c5-b34b-a2eb7c9eea5c` + documentation_suite seal `b00e938a-717b-4f62-b936-f4934845ec52` (DERIVES_FROM openclaw seal) embedded 768d · mesh **8361+ nodes** · Survival Laws Self-audit 4/4 ✓. **Hazard registrado**: agente main do OpenClaw (Qwen3.5 local) operou na mesma working dir durante a sessão — 3 diretórios gitignorados, zero overlap de path. **Próximo**: Canvas Design (Initiative B — integração `nexu-io/open-design`) em sessão dedicada via `/bok-scribe canvas-design`.
> 48	
> 49	**Sprint v6.6.8 selado em 2026-05-19** — Bridge Recovery + MAPE-K Audit + SDD aios-sql-bridge + Survival Laws 4/4: sessão de auditoria reativa disparada por Sovereign observando `claw.gcrux.com/dreaming` stagnation (Imported Insights congelado em 2026-05-16, Memory Palace counts estáticos, Dream Scene "0 promovido"). **Root cause material**: Stage 2 cron `nightly-bridge-refresh.sh` invocava `node` PATH-resolved como v18.19.1 no env do user `ubuntu` apesar do interativo ter v22.22.3 — OpenClaw CLI exige v22.12+ → 100% FAIL silently em Step 3 (reindex SQLite) há ≥3 dias; Steps 1+2 (bridge + distribute) rodavam clean. **Fix dual no mesmo edit**: (1) `NODE_BIN=/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolved-target (não symlink); (2) descoberta runtime de bug latente segundo — `claw-master` foi adicionado em v6.3.1 ao distribute script MAS NÃO ao indexer loop (`for agent in main artisan engineer scientist marketing-growth guardian; do` omitia claw-master) → `claw-master.sqlite` stale May 16 → exatamente o checkpoint "AIOS Core v2 (2026-05-16)" que Sovereign observou na UI. **SOP first per Lei 2**: `docs/processes/openclaw-bridge-recovery.md` 86 LOC autorada ANTES do edit. **5 phases materializadas** (todas com ORO triplet + Survival Laws ✓): Phase A (bridge fix + claw-master loop), Phase B (MAPE-K closed-loop audit + 4 observation nodes em mesh — Plan `a4c4c026` / Execute `69f6e356` / Monitor `d605bdda` / Analyze `d8952ce8` com edges DERIVES_FROM v6.6.7), Phase C (9 untracked files versionados via 3 commits: miv landing assets + miv tools + memory audit trail), Phase D (esta seal + milestone `c4643058`), Phase E (OTD-SSP01-001 closed via SDD `aios-sql-bridge` 376 LOC enterprise-grade + 00-index 69 LOC suite skeleton + documentation_suite seal `4e0acc7e` stability 0.85 DERIVES_FROM openclaw seal). **Material proofs**: 6 commits granulares pushed (`03911e9` fix(cron) + `cbdee4f` feat(landing) + `bb1cc96` chore(tools) + `2aa80f1` chore(memory) + `1b3bdd8` docs(bok) + `b71b991` docs(handoff) + `230ad70` docs(readme)); 7/7 SQLites OpenClaw reindexed (was 0/6 fail); log final `[2026-05-19T19:06:32-03:00] nightly-bridge-refresh DONE (zero failures)`; mesh **8359 nodes** (+6 desta seal); TS zero erros; 5 containers healthy. **Survival Laws Self-audit 4/4 ✓ pela primeira vez consecutivamente desde v6.6.0** — encerra retroativamente OTD-PROC-001 (RPN 60) + OTD-PROC-002 (RPN 40) + OTD-SSP01-001 (RPN 240 SLA 2026-05-24). **Pending TOP**: OE-661 Step 1.5 first-run E2E (Sovereign click `/dashboard/orchestration` TriggerNode); OTD-OE661-PER-USER refactor (SLA 2026-06-02, 14 dias); MAPE-K gaps 1/2/3 implementáveis em v6.7.x/v6.8.x conforme plans dedicados (recomendações registradas no mesh, aguardam acionamento).
> 50	
> 51	**Sprint v6.6.7 selado em 2026-05-19** — OE-661 Phase 1 Prep + API Tenancy Directive: sessão executou parcialmente o plan persistido OE-661 — toda a preparação completada, Step 1.5 (first run E2E) **DEFERRED** por context budget Sovereign 92% (retoma em ~3h). Infraestrutura material: SOP `docs/processes/orchestration-content-mesh-asset-emission.md` (120 LOC) escrita ANTES do código (Lei 2); `orchestrate-content/index.ts:404-465` emite `content_mesh_asset` em paralelo com observation via `Promise.allSettled` (Amendment A) gated por `wpPostUrl` (Amendment B); `link-forge.ts:153` ganha `.eq("project_id", "mcorch-affiliate")` (Amendment C); `handle-ml-postback/index.ts` ganha pulse `infra_health_logs` em 4 return paths (Amendment E — fecha cegueira de 17 dias). Deploys material: `orchestrate-content` 113.6kB + `handle-ml-postback` 60.45kB. Vault `GCRUX_ML_AFFILIATE_TOKEN` provisionado (digest `e86f74a0...`). **DIRETIVA SOVEREIGN-CLASS NOVA "API Tenancy Model"** emitida durante sessão (questionamento direto sobre por que usar env global se `affiliate_config` per-user já existia) — selada em 3 superfícies: `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` com resolution order de 3 níveis + 5 tabelas canônicas + 5 anti-patterns; `CLAUDE.md > Code standards` one-liner enforcement; auto-memory `feedback_api_tenancy_per_user.md` indexada. **OTD-OE661-PER-USER** registrada (RPN 120 · SLA 2026-06-02) catalogando violação em `link-forge.ts` + `process-affiliate-link` GET branch. Sovereign autorizou Opção B (provisionar global temporário com `affiliate_config.app_id` value, deferir refactor). **Survival Laws Self-audit retroativo (Amendment H)** v6.6.1..v6.6.5 + esta seal — conclusão: Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 (overrides conscientes v6.6.1+v6.6.3) · Lei 3 ✗ 0/5 (OTD-PROC-002 RPN 40) · Lei 4 ✗ 0/5 (OTD-PROC-001 RPN 60 — esta seal v6.6.7 começa cumprimento). **Material proofs**: TS zero erros · 122/122 testes em 4.84s · 7 commits granulares locais (`03f6822` SOP · `e662da3` orchestrate Amendments A+B · `bafac16` link-forge Amendment C · `9cec88a` postback Amendment E · `044f21e` CLAUDE+OTD diretiva · `96ee72a` README v6.6.7 · `7d06934` HANDOFF seal + redactions) · milestone node `9d482014-a759-4656-93d9-99e05ab4a714` embedded 768d · mesh **8353 nodes** (+1 desde v6.6.6) · 11650 edges (+33). Path correção material: `/dashboard/orchestrate` → `/dashboard/orchestration` (Sovereign clarification). **Próximos deliverables**: (a) Sovereign dispara primeira campanha real em `/dashboard/orchestration` (TriggerNode + topic Link Forge catálogo + wp+linkedin platforms + Run) → eu monitoro pipeline_runs + content_mesh_asset emit material via REST; (b) ao completar, synthetic postback chain (Amendment D) + cleanup (Amendment J); (c) selar v6.6.8 com flywheel rodando E2E pela primeira vez na história do projeto; (d) atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias) — SDD `aios-sql-bridge`; (e) executar Phase 2 (`mcoins-ledger-reconciliation.md`) — fecha OTD-V660-001.
> 52	
> 53	**Sprint v6.6.6 selado em 2026-05-19** — Planning Seal + Debt Audit + Self-audit Retroativo: sessão dedicada a (a) `/handson` brief v6.6.5; (b) persistir execution plan dos 3 carry-overs OE-661 + Ledger SOP + Canvas 4.2c por diretiva Sovereign "slave o plano atual para posteriormente implantar"; (c) auditoria completa em 3 frentes paralelas; (d) emendas críticas; (e) /handoff oficial. **Zero código de produção tocado**. Plan persistido em `.claude/context/execution-plan-oe661-carryovers.md` (~403 LOC, md5 `0e5f0ba9...`) + observation node `3dde2572-cad6-491b-b523-c56ec763ff8e` (autoembed 768d). Audit em `.claude/context/audit-2026-05-19-oe661-debt-sweep.md` (~297 LOC, md5 `5c4f8a9f...`) + observation node `6164c80f-cadd-48d5-95a4-f87f22ebd09b` + DERIVES_FROM edge `acb4b0d9-091d-4973-96a8-d40515be7990`. **21 OTDs ativos catalogados (8 RPN ≥ 100): VM-OTD-001 RPN 288 viralmind HNSW · OTD-SSP01-005 RPN 280 admin claim · OTD-SSP01-001 RPN 240 SLA 2026-05-24 · OTD-V660-002 RPN 150 · VM-OTD-004 RPN 140 · OTD-V660-001 RPN 120 (coberta pelo plan Phase 2) · OTD-V660-003 RPN 80 · OTD-CV42C-001**. **5 inconsistências processuais**: (1) **5 seals consecutivas (v6.6.1..v6.6.5) omitiram bloco mandatory Survival Laws Self-audit** — Severidade ALTA; (2) Survival Audit v2 não re-rodado em 32 dias; (3) 3 SOPs implícitas não formalizadas; (4) HANDOFF v6.6.3 claimed 4 content_mesh_asset mas reality = 1 row (3 "products" têm `node_type='feature'`); (5) `handle-ml-postback` cego — zero `infra_health_logs` em 17 dias. **4 bugs concretos no plan**: A race condition obs+asset não atômicos · B wpPostUrl null não gated · C Link Forge query global sem project_id · D postback content_id drift. **10 amendments aplicados** (A-J) via Amendments Appendix no topo do plan. Schema drift fixed: `infra_health_logs.created_at` NÃO EXISTE (real: `last_seen_at`). **Predicted Survival Audit v3** (não emitido formalmente): Memory 5/5 · Skill 4/5 · Cost Discipline 4.5/5 ↑ · Observability 4/5 ↑ · SOP 5/5 · **avg 4.4/5 · min 4/5** — Phase Commercial threshold mantido. **Material proofs**: 14 integrity checks paralelos · 4 commits granulares (`ea7efaf` plan + `44e464c` audit + `fb6f07d` README + `99d70f6` handoff seal) push → origin/main · milestone handoff node `821dc554-78e2-4abb-999d-37363c5df6c9` embedded 768d · mesh total **8352 nodes** (+4 desde v6.6.5). **Próximos deliverables**: (a) Sovereign autoriza execução das Fases 1-3 do plan quando convier (bugs A-D já fixed); (b) **atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias)** — BoK Gate override `aios-sql-bridge` precisa SDD; (c) provisionar `SUPABASE_POOLER_URL` (OTD-V660-003); (d) materializar Survival Audit v3 formal antes de Phase Commercial; (e) executar Phase 2 do plan (SOP `mcoins-ledger-reconciliation.md`) — Sovereign-only — fecha OTD-V660-001.
> ```

## 🤖 Claude *(14:06:21)*


## 🤖 Claude *(14:06:21)*

Now the BoK Gate check — the active module is `marketing-hub`. Let me verify completeness materially.

## 🤖 Claude *(14:06:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nfor slug in marketing-hub meta-api mercado-livre-api; do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  if [ ${#missing[@]} -eq 0 ]; then echo \"\u2705 $slug \u2014 BoK complete (9/9)\"; else echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"; fi\ndone",
  "description": "BoK gate check for active modules"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ marketing-hub — BoK complete (9/9)
> ✅ meta-api — BoK complete (9/9)
> ✅ mercado-livre-api — BoK complete (9/9)
> ```

## 🤖 Claude *(14:06:37)*


## 🤖 Claude *(14:07:00)*

Tudo verificado materialmente. Segue o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — v6.22.0 Campaign Core + LLM Fallback + Lead Scoring (2026-06-03)
═══════════════════════════════════════════════════════════

🏁 ESTADO ATUAL
  Fase selada: Campaign Core + OTD-LLM-FALLBACK + lead-score (v6.22.0)
  Sync: HEAD == origin/main (0↔0) · working tree limpo
  Últimos commits:
    9d48bf9 — chore(sprint): update sprint-priorities v6.22.0
    458d74f — docs(handoff): seal v6.22.0
    d3f6015 — chore(billing): centraliza COIN_COSTS (LEAD_SCORE/CAMPAIGN_RUN) + dívida calibração
    46362c4 — feat(marketing-hub): lead-score edge fn (FR-MH-003) — JWT + 1 mco + IA fail-soft
    7fd8e7a — feat(marketing-hub): MVP-2 Campaign Core — campaigns absorvida + campaign_steps

📂 MUDANÇAS PENDENTES
  Worktree limpo ✅ (nada a commitar; scratch/ ausente)

🏗️ INFRA
  mcorch_chroma:     Up 10 days (healthy) — Chroma API v2: OK (heartbeat real)
  mcorch_claude_mem: Up 10 days (healthy)
  mega-brain-*:      daemon/webhook healthy · dashboard up (3/3)

🧠 KNOWLEDGE MESH
  8759 nós · 9070 arestas (fonte: HANDOFF GraphRAG State) · 100% embedded (768d HNSW)
  Último seal: handoff aec4cb9c + milestones MVP-2 7628892b / OTD 6061a6d2

🔧 TYPESCRIPT
  Zero erros ✅

📚 BoK SUITES (Master Execution Protocol)
  marketing-hub: ✅ 9/9 completa (seal d5163fed) — módulo ativo, gate liberado
  meta-api / mercado-livre-api: ✅ 9/9
  GATE alert: nenhum — todo trabalho ativo (Campaign Core) nasce sob BoK selada ✅

📌 SPRINT
  Goal (estático): Distribuição social autônoma operacional
  Trilho real ativo: Marketing Hub v2 — MVP-1/2/lead-score LIVE; falta campaign-run + MVP-4/5
  Top gap: campaign-run (cascata fiel) — ADIADA por decisão Sovereign (código $ + Lei 3)

⚡ PRÓXIMOS PASSOS (prioridade)
  1. campaign-run (MVP-3 parte 2) — cascata fiel: CAMPAIGN_RUN(10) + por passo
     invoke('orchestrate-content')(10) + sync campaign_steps.status. Contrato pronto no seal.
     ⚠️ Sovereign ADIOU conscientemente (código financeiro merece sessão fresca + preços $).
  2. OTD-MCOIN-CALIBRATION — calibrar COIN_COSTS vs custo $ real (vídeo Higgsfield ~122 é o maior).
     Acoplada ao #1: não cravar 10 flat sem decidir o preço.
  3. MVP-4 — hooks (useLeads/useCampaigns/useLeadScore) + UI (LeadBoard/CampaignComposer)
     + rota /dashboard/marketing. Caminho não-financeiro se preferir destravar UI antes do $.

⚠️ ALERTAS
  Nenhum bloqueador técnico ✅ (TS limpo · 5 containers healthy · sync com origin)
  📲 Decisão aguardando dado: o experimento de atribuição de clique ML (matt_word) era esperado
     ~hoje (2026-06-03). Se você já tem o nº de cliques, ele decide o destino do
     "Operador de Browser Autenticado" (matt_word basta vs. falta matt_tool vs. precisa do ref).

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

Duas bifurcações reais aguardam **sua** decisão, Maestro:

1. **`campaign-run` agora vs. depois** — é o próximo passo natural do Marketing Hub, mas você o adiou na última sessão por ser código financeiro com contexto saturado. Contexto agora está fresco. Quer atacá-lo (exige também decidir os preços $ da calibração mcoCoins), ou prefere destravar a **UI (MVP-4)** primeiro — caminho não-financeiro?

2. **Atribuição de clique ML** — o experimento que você ia rodar num dispositivo independente estava previsto para hoje. Se já tem o número, ele resolve a iniciativa do Browser Autenticado.

Para onde aponto?

## 👤 User *(14:23:41)*

Sim continue



Estou aguardando atualizar pois a ultima atualização foi dia 02 mas fizemos os testes no final do dia 02/05 então amanhã no dia 03/05 falo se contabilizou ou não, pois ainda esta somente 1 click no mes de junho que pode ter acontecido no dia 01 que fizemos as ultimas mudanças em produtos afiliados.



Próximos passos você decide as prioridades mas lembre-se, você esta dizendo que o contexto está longo mas fizemos upgrade no claude pro para o max, agora temos maior limite de 5 horas apesar da janela de contexto ser a mesma no modelo atual você esta dizendo que esta longa quando passa de 400k de toknes na janela de contexto de 1M, então sugiro pensar melhor nisso, pois o handoff não gasta tanto para selar as sessões agoar.

## 🤖 Claude *(14:25:18)*


## 🤖 Claude *(14:25:30)*

Entendido, Maestro. Dois pontos absorvidos:

**1. Atribuição ML** — ainda inconclusiva (1 clique em junho, provavelmente do dia 01 quando mexemos nos produtos, não do teste `matt_word`). Fica pausada aguardando seu número quando os dados maturarem. Não toco no Browser Operator até lá.

**2. Calibração de contexto — feedback recebido e você está certo.** Eu (na sessão anterior) tratei "contexto saturado" como bloqueador para o `campaign-run` cedo demais. Com janela de 1M e o plano Max (limite de 5h), o gatilho real da Lei 3 é ~400k+, não antes. E selar via `/handoff` é barato agora. Vou registrar isso na memória para não repetir a poda prematura.

Como você delegou a priorização: **decido construir o `campaign-run` (MVP-3 parte 2) agora.** Razão: é o próximo passo natural e já especificado (contrato no seal + irmão do `lead-score` recém-construído), completa o **backend** inteiro do Marketing Hub antes do MVP-4 (UI) — assim a UI tem o backend completo para conectar. O único motivo do adiamento (contexto) acabou de ser refutado por você. A calibração $ (OTD-MCOIN-CALIBRATION) é decisão **sua** — não vou improvisar preços; uso a cascata fiel já documentada (`CAMPAIGN_RUN` 10 + 10×N por passo) e deixo a calibração como OTD aberta.

**ORO triplet desta task:**
- **Operator:** MCORCH Agent
- **Reviewer:** Sovereign + gate `/security-review` (se tocar schema) — mas é edge fn, então review de código
- **Owner:** Sovereign (blast radius = débito financeiro em cascata + invoca `orchestrate-content` pago; **o primeiro run pago real fica gated em GO seu**)

Deixa eu registrar a calibração de contexto e fazer o probe-first material antes de codar (padrão que tem evitado retrabalho neste projeto).

## 🤖 Claude *(14:25:38)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_context_budget_calibration.md",
  "content": "---\nname: feedback_context_budget_calibration\ndescription: N\u00e3o declarar \"contexto longo\"/adiar trabalho por Lei 3 antes de ~400k tokens \u2014 janela \u00e9 1M, plano \u00e9 Max, handoff seal \u00e9 barato\nmetadata:\n  type: feedback\n---\n\nDiretiva Sovereign 2026-06-03: parei de construir `campaign-run` na v6.22.0 citando \"Lei 3 \u2014 contexto saturado\". O Sovereign refutou: o plano Claude foi atualizado de **Pro \u2192 Max** (limite maior de 5h de uso); a janela de contexto do modelo atual \u00e9 **1M tokens**; \"contexto longo\" s\u00f3 vale a partir de **~400k/1M**, n\u00e3o antes. E o `/handoff` \"n\u00e3o gasta tanto para selar as sess\u00f5es agora\".\n\n**Why:** adiar trabalho (especialmente c\u00f3digo financeiro como campaign-run) por medo de contexto deixa valor na mesa quando ainda h\u00e1 runway enorme. A poda prematura da Lei 3 vira pretexto para n\u00e3o terminar a fase.\n\n**How to apply:** s\u00f3 invocar poda/adiamento da Lei 3 quando genuinamente perto de ~400k+ tokens OU uma fase realmente terminou. Selar a meio de uma feature \"para economizar contexto\" \u00e9 quase sempre desnecess\u00e1rio agora. Continuar a executar at\u00e9 a entrega natural; o seal \u00e9 barato. Refina [[project_mcoin_calibration]] (campaign-run foi adiada por esse motivo) e a Lei 3 de `.claude/rules/survival.md` (o crit\u00e9rio \"50%\" deve ser lido contra 1M).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_context_budget_calibration.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:25:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/lead-score/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// lead-score — marketing-hub FR-MH-003 (BoK SSOT: docs/bok/marketing-hub/04-frd.md §4.2 + 05-sdd.md §3).
> 2	// JWT-guarded · debits 1 mcoCoin atomically (deduct_mco_coins RPC) · scores a lead 0-100 via the
> 3	// per-user AI key (API Tenancy Model) with the shared LLM cascade fallback · FAIL-SOFT to a heuristic
> 4	// when the LLM is unavailable · persists leads.score + an immutable lead_event + an infra_health pulse.
> 5	import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> 6	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 7	import { fetchLLMWithFallback } from "../_shared/llm-fallback.ts";
> 8	
> 9	const corsHeaders = {
> 10	  "Access-Control-Allow-Origin": "*",
> 11	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 12	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 13	};
> 14	
> 15	const SCORE_COST = 1;
> 16	
> 17	interface LeadRow {
> 18	  id: string;
> 19	  user_id: string;
> 20	  status: string;
> 21	  name: string | null;
> 22	  intent_signal: Record<string, unknown> | null;
> 23	}
> 24	
> 25	// Fail-soft heuristic when the LLM is unavailable: a rough 0-100 from non-PII lifecycle signals.
> 26	function heuristicScore(lead: LeadRow): number {
> 27	  if (lead.status === "converted") return 95;
> 28	  if (lead.status === "lost") return 15;
> 29	  let s = 40;
> 30	  if (lead.name) s += 10;
> 31	  const intentKeys = lead.intent_signal ? Object.keys(lead.intent_signal).length : 0;
> 32	  s += Math.min(intentKeys * 8, 32);
> 33	  if (lead.status === "nurturing") s += 10;
> 34	  return Math.max(0, Math.min(100, s));
> 35	}
> 36	
> 37	serve(async (req) => {
> 38	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 39	  const json = (body: unknown, status = 200) =>
> 40	    new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 41	
> 42	  const url = Deno.env.get("SUPABASE_URL")!;
> 43	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 44	  const admin = createClient(url, serviceKey);
> 45	
> 46	  try {
> 47	    const authHeader = req.headers.get("Authorization");
> 48	    if (!authHeader) return json({ error: "Missing authorization" }, 401);
> 49	
> 50	    const userClient = createClient(url, (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!, {
> 51	      global: { headers: { Authorization: authHeader } },
> 52	    });
> 53	    const { data: { user }, error: authError } = await userClient.auth.getUser();
> 54	    if (authError || !user) return json({ error: "Unauthorized" }, 401);
> 55	
> 56	    const { lead_id, context } = await req.json().catch(() => ({}));
> 57	    if (!lead_id || typeof lead_id !== "string") return json({ error: "lead_id é obrigatório" }, 422);
> 58	
> 59	    // existence + ownership (tenant-scoped); 404 also covers another tenant's lead.
> 60	    const { data: lead } = await admin
> 61	      .from("leads")
> 62	      .select("id, user_id, status, name, intent_signal")
> 63	      .eq("id", lead_id)
> 64	      .eq("user_id", user.id)
> 65	      .maybeSingle();
> 66	    if (!lead) return json({ error: "Lead não encontrado" }, 404);
> 67	
> 68	    // mcoCoins gatekeeper: pre-check, then atomic server-side deduction (never client-side).
> 69	    const { data: bal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 70	    if ((bal?.mco_balance ?? 0) < SCORE_COST) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 71	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: user.id, p_amount: SCORE_COST });
> 72	    if (deductErr) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 73	
> 74	    // per-user AI key (API Tenancy Model) -> system fallback.
> 75	    const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 76	    const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 77	    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 78	    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 79	    const aiKey = groqKey || openRouterKey;
> 80	
> 81	    let score: number | null = null;
> 82	    let rationale = "";
> 83	
> 84	    if (aiKey) {
> 85	      const isGroq = !!groqKey;
> 86	      const endpoint = isGroq
> 87	        ? "https://api.groq.com/openai/v1/chat/completions"
> 88	        : "https://openrouter.ai/api/v1/chat/completions";
> 89	      const model = isGroq ? "llama-3.3-70b-versatile" : "meta-llama/llama-3.3-70b-instruct";
> 90	      const sys =
> 91	        'Você é um especialista em qualificação de leads. Avalie a intenção de compra do lead numa ' +
> 92	        'escala 0-100 (0=frio, 100=pronto para comprar). Responda APENAS com JSON válido: ' +
> 93	        '{"score": <inteiro 0-100>, "rationale": "<1 frase em pt-BR>"}';
> 94	      const userMsg =
> 95	        `Lead: status=${lead.status}, tem_nome=${!!lead.name}, sinais=${JSON.stringify(lead.intent_signal ?? {})}` +
> 96	        `${context ? `, contexto=${String(context).slice(0, 240)}` : ""}. Pontue.`;
> 97	      try {
> 98	        const aiResp = await fetchLLMWithFallback(
> 99	          endpoint,
> 100	          {
> 101	            method: "POST",
> 102	            headers: {
> 103	              Authorization: `Bearer ${aiKey}`,
> 104	              "Content-Type": "application/json",
> 105	              "HTTP-Referer": "https://mcorch.com",
> 106	              "X-Title": "GCRUX Constellation",
> 107	            },
> 108	            body: JSON.stringify({
> 109	              model,
> 110	              messages: [{ role: "system", content: sys }, { role: "user", content: userMsg }],
> 111	              stream: false,
> 112	              temperature: 0.2,
> 113	            }),
> 114	          },
> 115	          { openRouterKey, geminiKey, groqKey, functionName: "lead-score" },
> 116	        );
> 117	        if (aiResp.ok) {
> 118	          const data = await aiResp.json();
> 119	          const content: string = data?.choices?.[0]?.message?.content ?? "";
> 120	          const m = content.match(/\{[\s\S]*\}/);
> 121	          if (m) {
> 122	            const parsed = JSON.parse(m[0]);
> 123	            const n = Number(parsed.score);
> 124	            if (Number.isFinite(n)) {
> 125	              score = Math.max(0, Math.min(100, Math.round(n)));
> 126	              rationale = String(parsed.rationale ?? "").slice(0, 280);
> 127	            }
> 128	          }
> 129	        }
> 130	      } catch (_) {
> 131	        // fail-soft below
> 132	      }
> 133	    }
> 134	
> 135	    // FAIL-SOFT: heuristic when the LLM was unavailable, errored, or returned unparseable output.
> 136	    if (score === null) {
> 137	      score = heuristicScore(lead as LeadRow);
> 138	      rationale = rationale ||
> 139	        "Pontuação heurística (IA indisponível): baseada em status, identificação e sinais de intenção.";
> 140	    }
> 141	
> 142	    // persist: score + promote new->scored; immutable scored event; best-effort health pulse.
> 143	    await admin.from("leads")
> 144	      .update({ score, status: lead.status === "new" ? "scored" : lead.status })
> 145	      .eq("id", lead_id).eq("user_id", user.id);
> 146	    await admin.from("lead_events").insert({
> 147	      lead_id, user_id: user.id, channel: "system", event_type: "scored",
> 148	      payload: { score, rationale, source: aiKey ? "ai" : "heuristic" },
> 149	    });
> 150	    admin.from("infra_health_logs").insert({ service: "lead-score", status: "healthy" }).then(() => {}, () => {});
> 151	
> 152	    const { data: newBal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 153	    return json({ status: "ok", lead_id, score, rationale, new_balance: newBal?.mco_balance ?? null });
> 154	  } catch (err) {
> 155	    admin.from("infra_health_logs").insert({ service: "lead-score", status: "unhealthy" }).then(() => {}, () => {});
> 156	    return json({ error: "Erro interno ao pontuar lead", detail: String((err as Error)?.message ?? err) }, 500);
> 157	  }
> 158	});
> 159	
> ```

## 🤖 Claude *(14:25:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/billing.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import type { SupabaseClient } from '@supabase/supabase-js';
> 2	
> 3	// mcoCoins cost per operation — single source of truth (frontend).
> 4	// CALIBRATION NOTE (2026-06-03 · OTD-MCOIN-CALIBRATION): these are round figures, NOT yet derived from
> 5	// real provider $ cost. ORCHESTRATION_RUN (10) is charged FLAT and is LESS than the sum of its parts
> 6	// (3×CONTENT_GENERATION + IMAGE_GENERATION = 18); real spend (mcoin_transactions) shows canvas_video as
> 7	// the dominant cost (~122/video). campaign-run (FR-MH-004) is a CASCADE: CAMPAIGN_RUN once + N×ORCHESTRATION_RUN
> 8	// per dispatched step. Edge functions currently mirror these constants by hand (Deno can't import src/lib).
> 9	// → Pending: tune against per-model token $ + Higgsfield video price before commercial pricing.
> 10	export const COIN_COSTS = {
> 11	  ORCHESTRATION_RUN: 10,
> 12	  CONTENT_GENERATION: 5,
> 13	  IMAGE_GENERATION: 3,
> 14	  EMBED_NODE: 1,
> 15	  LEAD_SCORE: 1, // marketing-hub FR-MH-003 (lead-score edge fn mirrors this)
> 16	  CAMPAIGN_RUN: 10, // marketing-hub FR-MH-004 — orchestration fee ON TOP of the cascaded per-step ORCHESTRATION_RUN
> 17	} as const;
> 18	
> 19	export type CoinOperation = keyof typeof COIN_COSTS;
> 20	
> 21	/**
> 22	 * Deducts mcoCoins from the authenticated user's profile.
> 23	 * Calls the `deduct_mco_coins` SECURITY DEFINER RPC which enforces
> 24	 * the balance check atomically in the database.
> 25	 * Throws if balance is insufficient or the RPC fails.
> 26	 */
> 27	export async function deductMcoCoins(
> 28	  supabase: SupabaseClient,
> 29	  userId: string,
> 30	  amount: number,
> 31	): Promise<void> {
> 32	  const { error } = await supabase.rpc('deduct_mco_coins', {
> 33	    p_user_id: userId,
> 34	    p_amount: amount,
> 35	  });
> 36	
> 37	  if (error) {
> 38	    throw new Error(error.message || 'Falha ao deduzir mcoCoins');
> 39	  }
> 40	}
> 41	
> 42	/**
> 43	 * Returns the current mco_balance for the given user.
> 44	 * Returns 0 if the profile row is not found.
> 45	 */
> 46	export async function getMcoBalance(
> 47	  supabase: SupabaseClient,
> 48	  userId: string,
> 49	): Promise<number> {
> 50	  const { data, error } = await supabase
> 51	    .from('profiles')
> 52	    .select('mco_balance')
> 53	    .eq('id', userId)
> 54	    .maybeSingle();
> 55	
> 56	  if (error) throw new Error(error.message);
> 57	  return (data?.mco_balance as number | null) ?? 0;
> 58	}
> 59	
> 60	/**
> 61	 * Returns true if the user has enough mcoCoins for the operation.
> 62	 * Prefer this for UI guard checks (non-destructive read).
> 63	 */
> 64	export async function hasSufficientBalance(
> 65	  supabase: SupabaseClient,
> 66	  userId: string,
> 67	  required: number,
> 68	): Promise<boolean> {
> 69	  const balance = await getMcoBalance(supabase, userId);
> 70	  return balance >= required;
> 71	}
> 72	
> 73	/**
> 74	 * Convenience wrapper: checks balance then deducts in sequence.
> 75	 * Use this in Edge Functions where you want an explicit pre-check message.
> 76	 */
> 77	export async function checkAndDeductCoins(
> 78	  supabase: SupabaseClient,
> 79	  userId: string,
> 80	  operation: CoinOperation,
> 81	): Promise<void> {
> 82	  const cost = COIN_COSTS[operation];
> 83	  const sufficient = await hasSufficientBalance(supabase, userId, cost);
> 84	  if (!sufficient) {
> 85	    throw new Error(
> 86	      `Saldo insuficiente: operação "${operation}" custa ${cost} mcoCoins`,
> 87	    );
> 88	  }
> 89	  await deductMcoCoins(supabase, userId, cost);
> 90	}
> 91	
> ```

## 🤖 Claude *(14:25:47)*


## 🤖 Claude *(14:25:48)*

Lead-score pattern is clear and clean. Now I need the exact `campaigns`/`campaign_steps` schema, the FRD spec for campaign-run (FR-MH-004), and the `orchestrate-content` input contract since campaign-run dispatches to it.

## 🤖 Claude *(14:25:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== migration files matching campaign ===\"\nls -1 supabase/migrations/ | grep -iE \"campaign|2026060302\" || echo \"none by name\"\necho \"\"\necho \"=== campaign_steps + campaigns ALTER in the MVP-2 migration ===\"\ngrep -rln \"campaign_steps\" supabase/migrations/ 2>/dev/null\necho \"\"\necho \"=== FR-MH-004 / campaign-run mentions in FRD ===\"\ngrep -nE \"FR-MH-004|campaign-run|campaign_run|CAMPAIGN_RUN\" docs/bok/marketing-hub/04-frd.md 2>/dev/null | head -30",
  "description": "Locate campaign migration + FRD spec for campaign-run"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === migration files matching campaign ===
> 20260603025256_marketing_hub_campaign_core.sql
> 
> === campaign_steps + campaigns ALTER in the MVP-2 migration ===
> supabase/migrations/20260603025256_marketing_hub_campaign_core.sql
> 
> === FR-MH-004 / campaign-run mentions in FRD ===
> 30:| FR-MH-004 | Campaign Run Edge Fn | `campaign-run`: JWT-guarded, debita 10 mcoCoins, orquestra `orchestrate-content` por passo de campanha, sincroniza status | Critical | PR-MH-003 | EdgeFunction | AT-MH-004 |
> 49:| NFR-MH-004 | Availability | Uptime SLO do módulo | 99.5%/mês | Watchdog telemetry |
> 68:[Edge Function: lead-score / campaign-run / nurture-dispatch / intent-orchestrate / aeo-audit]
> 104:#### `POST /functions/v1/campaign-run`
> 133:| FR-MH-004 | ✅ Required | ✅ Required | ✅ Required | Campaign run orquestra orchestrate-content |
> 156:| PR-MH-003 | FR-MH-004, FR-MH-005 | NFR-MH-002, NFR-MH-008 |
> ```

## 🤖 Claude *(14:25:58)*


## 🤖 Claude *(14:25:58)*

BoK confirmed — FR-MH-004 is fully specified. Reading the exact contract + schema + the orchestrate-content input shape.

## 🤖 Claude *(14:25:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/04-frd.md",
  "offset": 95,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 95	**Error codes:**
> 96	| Code | Condition |
> 97	|------|-----------|
> 98	| 401 | Missing or invalid JWT |
> 99	| 402 | Insufficient mcoCoins balance |
> 100	| 404 | Lead não encontrado / não pertence ao tenant |
> 101	| 422 | Validation failure (campo + mensagem PT-BR) |
> 102	| 500 | Internal error (logged to infra_health_logs) |
> 103	
> 104	#### `POST /functions/v1/campaign-run`
> 105	
> 106	**Auth:** Bearer JWT (user scope)  
> 107	**Request:** `{ campaign_id: string }`  
> 108	**Response (200):** `{ status: 'ok', campaign_id: string, run_id: string, steps_dispatched: number, new_balance: number }`  
> 109	**Errors:** 401 / 402 / 404 / 422 / 500 (mesma semântica acima).
> 110	
> 111	---
> 112	
> 113	## 5. Data Requirements
> 114	
> 115	| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |
> 116	|-------|------|----------|-----------------|----------------------|
> 117	| `leads.contact` | `text` | NOT NULL | E.164 (telefone) OU email válido | "Contato inválido — informe telefone (E.164) ou email" |
> 118	| `leads.status` | `enum` | NOT NULL | ∈ {new, scored, nurturing, converted, lost} | "Status de lead inválido" |
> 119	| `leads.score` | `int2` | NULL | 0 ≤ score ≤ 100 | "Score deve estar entre 0 e 100" |
> 120	| `marketing_consents.basis` | `enum` | NOT NULL | ∈ {consent, legitimate_interest, contract} | "Base legal LGPD obrigatória" |
> 121	| `campaigns.name` | `text` | NOT NULL | 1–120 chars | "Nome da campanha é obrigatório (1–120)" |
> 122	| `aeo_audits.query` | `text` | NOT NULL | 1–280 chars | "Query de AEO obrigatória" |
> 123	
> 124	---
> 125	
> 126	## 6. Test Strategy Matrix
> 127	
> 128	| FR ID | Unit Test | Integration Test | E2E Test | Notes |
> 129	|-------|-----------|-----------------|----------|-------|
> 130	| FR-MH-001 | ✅ Required | ✅ Required | ✅ Required | Board states + RLS isolation |
> 131	| FR-MH-002 | ✅ Required | ✅ Required | — | Migration backfill count before/after |
> 132	| FR-MH-003 | ✅ Required | ✅ Required | ✅ Required | Score + mcoCoins débito atômico + 402 path |
> 133	| FR-MH-004 | ✅ Required | ✅ Required | ✅ Required | Campaign run orquestra orchestrate-content |
> 134	| FR-MH-005 | ✅ Required | ✅ Required | — | Composer persist |
> 135	| FR-MH-006 | ✅ Required | ✅ Required | ✅ Required | Erasure cascade zero-residue (crítico LGPD) |
> 136	| FR-MH-007 | ✅ Required | ✅ Required | — | Attribution por campaign_id |
> 137	| FR-MH-008 | ✅ Required | ✅ Required | — | Opt-out respeitado + idempotência |
> 138	| FR-MH-009 | ✅ Required | ✅ Required | — | Policy engine auto vs HITL |
> 139	| FR-MH-010 | ✅ Required | — | — | Provider real OU degradado documentado |
> 140	| FR-MH-011 | ✅ Required | — | — | 360 aggregation |
> 141	| FR-MH-012 | ✅ Required | ✅ Required | — | BYOK resolve per-user→sistema |
> 142	
> 143	**Test files location:**
> 144	- Unit: `src/hooks/__tests__/useLeads.test.ts`, `useCampaigns.test.ts`, etc.
> 145	- Integration: `src/__tests__/integration/marketing-hub.test.ts`
> 146	- E2E: `e2e/marketing-hub.spec.ts`
> 147	
> 148	---
> 149	
> 150	## 7. Traceability Matrix
> 151	
> 152	| PR ID | FR ID | NFR ID |
> 153	|-------|-------|--------|
> 154	| PR-MH-001 | FR-MH-001, FR-MH-002 | NFR-MH-001, NFR-MH-006 |
> ```

## 🤖 Claude *(14:26:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603025256_marketing_hub_campaign_core.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: marketing-hub Campaign Core — ALTER campaigns (absorb) + campaign_steps + marketing_attribution
> 2	-- BoK SSOT: docs/bok/marketing-hub/06-data-model.md (§2 campaigns/campaign_steps/marketing_attribution
> 3	--           + "Absorb-not-create reconciliation" + "FK pattern" notes) · 05-sdd.md · 04-frd.md.
> 4	-- Scope: MVP-2 Campaign Core. REUSE-NOT-REBUILD:
> 5	--   · public.campaigns ALREADY EXISTS (20260402014040, RLS default-deny + 4 policies) -> ALTERed, NOT recreated.
> 6	--   · public.campaign_metrics ALREADY EXISTS (per-platform telemetry) -> untouched.
> 7	--   · public.projects does NOT exist -> no project_id FK is introduced.
> 8	-- Tenant safety (lesson from MVP-1 /security-review — cross-tenant child linkage):
> 9	--   · campaign_steps         -> COMPOSITE FK CASCADE on (campaign_id, user_id) (mirrors lead_events).
> 10	--   · marketing_attribution  -> SIMPLE FK SET NULL + RLS WITH CHECK ownership (mirrors marketing_consents),
> 11	--     because a composite FK with SET NULL would also null user_id (NOT NULL) and break the lead-erasure path.
> 12	
> 13	-- ─────────────────────────────────────────────────────────────────────────────
> 14	-- 1. ALTER campaigns — absorb the v1 table; add Campaign Core columns + composite-unique FK target.
> 15	-- ─────────────────────────────────────────────────────────────────────────────
> 16	ALTER TABLE public.campaigns
> 17	  ADD COLUMN IF NOT EXISTS intent       text,
> 18	  ADD COLUMN IF NOT EXISTS channels     text[] NOT NULL DEFAULT '{}',  -- content | social | email | affiliate
> 19	  ADD COLUMN IF NOT EXISTS mesh_node_id uuid REFERENCES public.mcorch_nodes(id) ON DELETE SET NULL;
> 20	
> 21	-- Composite-unique target so child tables can tenant-scope their FK on (id, user_id).
> 22	-- id is already PK (unique alone); this UNIQUE exists purely as an FK reference target. Idempotent guard.
> 23	DO $$
> 24	BEGIN
> 25	  IF NOT EXISTS (
> 26	    SELECT 1 FROM pg_constraint WHERE conname = 'uniq_campaigns_id_user'
> 27	  ) THEN
> 28	    ALTER TABLE public.campaigns ADD CONSTRAINT uniq_campaigns_id_user UNIQUE (id, user_id);
> 29	  END IF;
> 30	END $$;
> 31	
> 32	CREATE INDEX IF NOT EXISTS idx_campaigns_mesh_node ON public.campaigns (mesh_node_id);
> 33	
> 34	-- ─────────────────────────────────────────────────────────────────────────────
> 35	-- 2. campaign_steps — ordered multichannel steps (each step drives orchestrate-content).
> 36	--    Tenant-scoped composite FK CASCADE: a step can only reference a campaign owned by the SAME
> 37	--    tenant; deleting the campaign cascades its steps. user_id denormalized for simple RLS.
> 38	-- ─────────────────────────────────────────────────────────────────────────────
> 39	CREATE TABLE IF NOT EXISTS public.campaign_steps (
> 40	  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 41	  campaign_id uuid NOT NULL,
> 42	  user_id     uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,  -- denormalized for RLS
> 43	  position    smallint NOT NULL,
> 44	  channel     text NOT NULL,                          -- content | social | email | affiliate
> 45	  action      text NOT NULL
> 46	                CHECK (action IN ('generate_content','publish','affiliate_attach')),
> 47	  status      text NOT NULL DEFAULT 'idle'
> 48	                CHECK (status IN ('idle','running','done','error','blocked')),
> 49	  created_at  timestamptz NOT NULL DEFAULT timezone('utc'::text, now()),
> 50	  -- closes cross-tenant linkage (A attaching a step to B's campaign_id) — same fix as lead_events.
> 51	  CONSTRAINT fk_campaign_steps_campaign FOREIGN KEY (campaign_id, user_id)
> 52	    REFERENCES public.campaigns (id, user_id) ON DELETE CASCADE
> 53	);
> 54	
> 55	ALTER TABLE public.campaign_steps ENABLE ROW LEVEL SECURITY;
> 56	
> 57	CREATE POLICY "campaign_steps_select_own" ON public.campaign_steps
> 58	  FOR SELECT USING (auth.uid() = user_id);
> 59	CREATE POLICY "campaign_steps_insert_own" ON public.campaign_steps
> 60	  FOR INSERT WITH CHECK (auth.uid() = user_id);
> 61	CREATE POLICY "campaign_steps_update_own" ON public.campaign_steps
> 62	  FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 63	-- DELETE cascades with the parent campaign; no standalone client DELETE policy.
> 64	
> 65	CREATE INDEX IF NOT EXISTS idx_campaign_steps_campaign ON public.campaign_steps (campaign_id);
> 66	CREATE INDEX IF NOT EXISTS idx_campaign_steps_user ON public.campaign_steps (user_id);
> 67	
> 68	-- ─────────────────────────────────────────────────────────────────────────────
> 69	-- 3. marketing_attribution — links revenue -> campaign/lead/touchpoint.
> 70	--    SIMPLE FK SET NULL (NOT composite) + RLS WITH CHECK ownership (mirrors marketing_consents):
> 71	--    the financial record is RETAINED de-linked when a referenced lead/campaign is removed.
> 72	-- ─────────────────────────────────────────────────────────────────────────────
> 73	CREATE TABLE IF NOT EXISTS public.marketing_attribution (
> 74	  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 75	  user_id       uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 76	  campaign_id   uuid REFERENCES public.campaigns(id) ON DELETE SET NULL,
> 77	  lead_id       uuid REFERENCES public.leads(id) ON DELETE SET NULL,
> 78	  touchpoint    text,                                 -- e.g. linkedin_post | wp_article | affiliate_click
> 79	  revenue_cents integer NOT NULL DEFAULT 0 CHECK (revenue_cents >= 0),
> 80	  model         text NOT NULL DEFAULT 'last_touch'
> 81	                  CHECK (model IN ('last_touch','multi_touch')),
> 82	  occurred_at   timestamptz NOT NULL DEFAULT timezone('utc'::text, now())
> 83	);
> 84	
> 85	ALTER TABLE public.marketing_attribution ENABLE ROW LEVEL SECURITY;
> 86	
> 87	CREATE POLICY "attribution_select_own" ON public.marketing_attribution
> 88	  FOR SELECT USING (auth.uid() = user_id);
> 89	-- INSERT/UPDATE assert ownership of the row AND (when set) that the referenced campaign/lead belong
> 90	-- to the caller — closes cross-tenant linkage via a planted foreign id (mirrors marketing_consents).
> 91	CREATE POLICY "attribution_insert_own" ON public.marketing_attribution
> 92	  FOR INSERT WITH CHECK (
> 93	    auth.uid() = user_id
> 94	    AND (campaign_id IS NULL OR EXISTS (
> 95	      SELECT 1 FROM public.campaigns c WHERE c.id = campaign_id AND c.user_id = auth.uid()))
> 96	    AND (lead_id IS NULL OR EXISTS (
> 97	      SELECT 1 FROM public.leads l WHERE l.id = lead_id AND l.user_id = auth.uid()))
> 98	  );
> 99	CREATE POLICY "attribution_update_own" ON public.marketing_attribution
> 100	  FOR UPDATE USING (auth.uid() = user_id)
> 101	  WITH CHECK (
> 102	    auth.uid() = user_id
> 103	    AND (campaign_id IS NULL OR EXISTS (
> 104	      SELECT 1 FROM public.campaigns c WHERE c.id = campaign_id AND c.user_id = auth.uid()))
> 105	    AND (lead_id IS NULL OR EXISTS (
> 106	      SELECT 1 FROM public.leads l WHERE l.id = lead_id AND l.user_id = auth.uid()))
> 107	  );
> 108	-- No DELETE policy: financial record retained (de-linked) for revenue traceability.
> 109	
> 110	CREATE INDEX IF NOT EXISTS idx_attribution_user ON public.marketing_attribution (user_id);
> 111	CREATE INDEX IF NOT EXISTS idx_attribution_campaign ON public.marketing_attribution (campaign_id);
> 112	CREATE INDEX IF NOT EXISTS idx_attribution_lead ON public.marketing_attribution (lead_id);
> 113	
> 114	-- ─────────────────────────────────────────────────────────────────────────────
> 115	-- 4. Extend erase_lead() (FMEA-MH-003 — erasure completeness) to report de-linked attributions.
> 116	--    marketing_attribution.lead_id is ON DELETE SET NULL, so the financial record survives de-linked;
> 117	--    this adds an observable count to the erasure receipt (no semantic change to the erasure itself).
> 118	-- ─────────────────────────────────────────────────────────────────────────────
> 119	CREATE OR REPLACE FUNCTION public.erase_lead(p_lead_id uuid)
> 120	RETURNS jsonb
> 121	LANGUAGE plpgsql
> 122	SECURITY DEFINER
> 123	SET search_path = ''
> 124	AS $$
> 125	DECLARE
> 126	  v_uid      uuid := auth.uid();
> 127	  v_owner    uuid;
> 128	  v_events   integer := 0;
> 129	  v_consents integer := 0;
> 130	  v_attr     integer := 0;
> 131	BEGIN
> 132	  IF v_uid IS NULL THEN
> 133	    RAISE EXCEPTION 'authentication required' USING errcode = '28000';
> 134	  END IF;
> 135	
> 136	  SELECT user_id INTO v_owner FROM public.leads WHERE id = p_lead_id;
> 137	  IF v_owner IS NULL THEN
> 138	    RETURN jsonb_build_object('erased', false, 'reason', 'not_found');
> 139	  END IF;
> 140	  IF v_owner <> v_uid THEN
> 141	    RAISE EXCEPTION 'cannot erase a lead owned by another tenant' USING errcode = '42501';
> 142	  END IF;
> 143	
> 144	  DELETE FROM public.lead_events WHERE lead_id = p_lead_id AND user_id = v_uid;
> 145	  GET DIAGNOSTICS v_events = ROW_COUNT;
> 146	
> 147	  -- Count attributions about to be de-linked (FK SET NULL retains the financial record itself).
> 148	  SELECT count(*) INTO v_attr
> 149	    FROM public.marketing_attribution WHERE lead_id = p_lead_id AND user_id = v_uid;
> 150	
> 151	  -- Retain consent proof (basis/timestamps) but mark withdrawn; FK SET NULL de-links on lead delete.
> 152	  UPDATE public.marketing_consents
> 153	     SET granted = false, withdrawn_at = COALESCE(withdrawn_at, timezone('utc'::text, now()))
> 154	   WHERE lead_id = p_lead_id AND user_id = v_uid;
> 155	  GET DIAGNOSTICS v_consents = ROW_COUNT;
> 156	
> 157	  DELETE FROM public.leads WHERE id = p_lead_id AND user_id = v_uid;
> 158	
> 159	  RETURN jsonb_build_object(
> 160	    'erased', true,
> 161	    'lead_id', p_lead_id,
> 162	    'events_deleted', v_events,
> 163	    'consents_withdrawn', v_consents,
> 164	    'attributions_delinked', v_attr
> 165	  );
> 166	END;
> 167	$$;
> 168	
> 169	REVOKE ALL ON FUNCTION public.erase_lead(uuid) FROM PUBLIC;
> 170	REVOKE ALL ON FUNCTION public.erase_lead(uuid) FROM anon;
> 171	GRANT EXECUTE ON FUNCTION public.erase_lead(uuid) TO authenticated;
> 172	
> ```

## 🤖 Claude *(14:26:28)*


## 🤖 Claude *(14:26:30)*

Schema is clear. Now the critical design question — the **cascade billing**: does `orchestrate-content` self-bill the 10 per run (so campaign-run only charges its own `CAMPAIGN_RUN` fee once)? And what's its input contract + auth? Let me verify materially, plus the SDD dispatch semantics and the `campaign_status` enum.

## 🤖 Claude *(14:26:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== campaign-run already exists? ===\"\nls -la supabase/functions/campaign-run/ 2>/dev/null || echo \"NO \u2014 campaign-run does not exist yet (good, building fresh)\"\necho \"\"\necho \"=== campaign_status enum definition ===\"\ngrep -rnE \"campaign_status\" supabase/migrations/20260402014040*.sql 2>/dev/null | head -10\necho \"\"\necho \"=== SDD campaign-run dispatch semantics ===\"\ngrep -nE \"campaign-run|campaign_run|orchestrate-content|steps_dispatched|dispatch\" docs/bok/marketing-hub/05-sdd.md 2>/dev/null | head -25",
  "description": "Check campaign-run absence + enum + SDD dispatch spec"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === campaign-run already exists? ===
> NO — campaign-run does not exist yet (good, building fresh)
> 
> === campaign_status enum definition ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:8:CREATE TYPE public.campaign_status AS ENUM ('draft', 'active', 'paused', 'completed', 'archived');
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:109:  status campaign_status NOT NULL DEFAULT 'draft',
> 
> === SDD campaign-run dispatch semantics ===
> 30:│  lead-score · campaign-run · nurture-dispatch · intent-orchestrate ·│
> 32:│  REUSES: orchestrate-content (campaign executor), embed-mcorch-node│
> 41:│  marketing_attribution        │  │  n8n (sequence cron dispatch)     │
> 81:| `campaign-run` | `supabase/functions/campaign-run/index.ts` | JWT (user) | 10 | (reusa orchestrate-content secrets) |
> 82:| `nurture-dispatch` | `supabase/functions/nurture-dispatch/index.ts` | JWT/service | 2 / message | per-user AI + channel creds (`social_credentials`/`meta_config`) |
> 150:### `POST /functions/v1/campaign-run`
> 163:  steps_dispatched: number
> 167:// → After JWT + ownership check, before dispatch:
> 170:// → Then per step: invoke('orchestrate-content', { ...stepPayload }) and sync status
> 198:| Nurturing dispatch | Envio sem consentimento | Repudiation / Compliance | **Critical** | Gate de consent obrigatório pré-envio; opt-out interrompe; audit trail |
> 243:| channel creds (`social_credentials`/`meta_config`) | `nurture-dispatch` | Vault (cifrado) | User-managed / reauth |
> 259:| `orchestrate-content` (reuse) | Executor de passo de campanha | Reuso (não duplica) |
> ```

## 🤖 Claude *(14:26:34)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/orchestrate-content/index.ts",
  "limit": 130
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	const corsHeaders = {
> 2	  "Access-Control-Allow-Origin": "*",
> 3	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 4	  "Access-Control-Allow-Headers":
> 5	    "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 6	};
> 7	
> 8	import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
> 9	
> 10	// FMEA-008: content length/structure validation before any content_library INSERT
> 11	const CONTENT_MIN_LENGTH: Record<string, number> = { article: 500, linkedin: 50, twitter_thread: 30 };
> 12	function validateContent(type: string, content: string): { valid: boolean; reason: string } {
> 13	  const trimmed = content.trim();
> 14	  if (!trimmed) return { valid: false, reason: "empty_content" };
> 15	  const min = CONTENT_MIN_LENGTH[type] ?? 30;
> 16	  if (trimmed.length < min) return { valid: false, reason: `too_short:${trimmed.length}/<${min}` };
> 17	  return { valid: true, reason: "ok" };
> 18	}
> 19	
> 20	Deno.serve(async (req) => {
> 21	  if (req.method === "OPTIONS") return new Response('ok', { headers: corsHeaders });
> 22	
> 23	  try {
> 24	    const authHeader = req.headers.get("Authorization");
> 25	    if (!authHeader?.startsWith("Bearer ")) {
> 26	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 27	        status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 28	      });
> 29	    }
> 30	
> 31	    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
> 32	    const supabaseKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 33	    const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 34	    
> 35	    const userClient = createClient(supabaseUrl, supabaseKey, {
> 36	      global: { headers: { Authorization: authHeader } },
> 37	    });
> 38	    const { data: { user }, error: userErr } = await userClient.auth.getUser();
> 39	    if (userErr || !user) {
> 40	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 41	        status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 42	      });
> 43	    }
> 44	
> 45	    const admin = createClient(supabaseUrl, serviceKey);
> 46	
> 47	    // pre-flight: check AI keys before charging user
> 48	    const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 49	    const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 50	    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 51	
> 52	    const prefModel = userKeys?.pref_ai_model ?? null;
> 53	    const prefRequiresOR = prefModel && (prefModel.includes("/") || prefModel.startsWith("gemini-"));
> 54	    const aiKey = prefRequiresOR ? (openRouterKey || groqKey) : (groqKey || openRouterKey);
> 55	
> 56	    if (!aiKey) {
> 57	      return new Response(JSON.stringify({ error: "GROQ_API_KEY or OPENROUTER_API_KEY not configured" }), {
> 58	        status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 59	      });
> 60	    }
> 61	
> 62	    const isGroq = !prefRequiresOR && !!groqKey && aiKey === groqKey;
> 63	    const aiEndpoint = isGroq ? "https://api.groq.com/openai/v1/chat/completions" : "https://openrouter.ai/api/v1/chat/completions";
> 64	    const orPrefModel = prefModel?.startsWith("gemini-") ? `google/${prefModel}` : prefModel;
> 65	    const selectedModel = orPrefModel ?? (isGroq ? "llama-3.3-70b-versatile" : "meta-llama/llama-3.3-70b-instruct");
> 66	
> 67	    const { topic, campaign_id, platforms = ["wordpress", "linkedin", "twitter"], site_url = "mcorch.com", wp_status = "draft" } = await req.json();
> 68	
> 69	    if (!topic) {
> 70	      return new Response(JSON.stringify({ error: "topic is required" }), {
> 71	        status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 72	      });
> 73	    }
> 74	
> 75	    // mcoCoins gatekeeper
> 76	    const ORCHESTRATION_COST = 10;
> 77	    const { data: profileBalance } = await admin
> 78	      .from("profiles")
> 79	      .select("mco_balance")
> 80	      .eq("id", user.id)
> 81	      .maybeSingle();
> 82	
> 83	    if ((profileBalance?.mco_balance ?? 0) < ORCHESTRATION_COST) {
> 84	      return new Response(
> 85	        JSON.stringify({ error: "Saldo insuficiente de mcoCoins para executar a orquestração" }),
> 86	        { status: 402, headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 87	      );
> 88	    }
> 89	
> 90	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", {
> 91	      p_user_id: user.id,
> 92	      p_amount: ORCHESTRATION_COST,
> 93	    });
> 94	    if (deductErr) {
> 95	      return new Response(
> 96	        JSON.stringify({ error: "Saldo insuficiente de mcoCoins para executar a orquestração" }),
> 97	        { status: 402, headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 98	      );
> 99	    }
> 100	
> 101	    // utm_campaign uses the campaign_id for per-campaign attribution; fallback to slug for unnamed runs
> 102	    const utmCampaign = campaign_id
> 103	      ? encodeURIComponent(campaign_id)
> 104	      : `mcorch_${topic.slice(0, 24).replace(/\s+/g, "_").toLowerCase()}`;
> 105	
> 106	    // --- Create pipeline_run record ---
> 107	    const runStarted = new Date().toISOString();
> 108	    const { data: runRow } = await admin
> 109	      .from("pipeline_runs")
> 110	      .insert({
> 111	        user_id: user.id,
> 112	        topic,
> 113	        platforms,
> 114	        status: "running",
> 115	        steps: [],
> 116	        started_at: runStarted,
> 117	        metadata: {
> 118	          topic,
> 119	          platforms,
> 120	          campaign_id: campaign_id || null,
> 121	          wp_status,
> 122	          site_url,
> 123	          selectedModel,
> 124	          isGroq,
> 125	          aiEndpoint,
> 126	          utmCampaign,
> 127	        }
> 128	      })
> 129	      .select("id")
> 130	      .single();
> ```

## 🤖 Claude *(14:26:55)*


## 🤖 Claude *(14:26:57)*

The cascade is confirmed material: `orchestrate-content` **self-bills 10** (line 76-99), takes `{ topic, campaign_id, platforms, wp_status }`, returns 401/400/402. So `campaign-run` charges its own `CAMPAIGN_RUN` (10) once + passes the user JWT so each dispatched step self-bills 10 = faithful `10 + 10×N`. Let me read the exact SDD pseudocode (the SSOT) so I honor the dispatch precisely.

## 🤖 Claude *(14:26:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md",
  "offset": 148,
  "limit": 45
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 148	> All Edge Functions must validate JWT before any business logic.
> 149	
> 150	### `POST /functions/v1/campaign-run`
> 151	
> 152	```typescript
> 153	// Request
> 154	interface CampaignRunRequest {
> 155	  campaign_id: string
> 156	}
> 157	
> 158	// Response (HTTP 200)
> 159	interface CampaignRunResponse {
> 160	  status: 'ok'
> 161	  campaign_id: string
> 162	  run_id: string
> 163	  steps_dispatched: number
> 164	}
> 165	
> 166	// mcoCoins deduction point:
> 167	// → After JWT + ownership check, before dispatch:
> 168	//   await supabase.rpc('deduct_mco_coins', { p_user_id, p_amount: 10 })
> 169	// → HTTP 402 if insufficient balance
> 170	// → Then per step: invoke('orchestrate-content', { ...stepPayload }) and sync status
> 171	```
> 172	
> 173	### `POST /functions/v1/aeo-audit`
> 174	
> 175	```typescript
> 176	interface AeoAuditRequest { queries: string[]; brand: string }
> 177	interface AeoAuditResponse {
> 178	  status: 'ok'
> 179	  audit_id: string
> 180	  citation_rate: number        // % queries citando a marca
> 181	  findings: Array<{ query: string; cited: boolean; recommendation: string }>
> 182	}
> 183	// mcoCoins: deduct 5 at entry. Provider per OTD-MH-003; degraded mode documented if no provider.
> 184	```
> 185	
> 186	---
> 187	
> 188	## 5. Security Design
> 189	
> 190	### 5.1 Threat Model (STRIDE)
> 191	
> 192	| Component | Threat | Type | Severity | Mitigation |
> ```

## 🤖 Claude *(14:28:58)*


## 🤖 Claude *(14:29:01)*

Full SSOT confirmed. The SDD prescribes: deduct 10 (CAMPAIGN_RUN) after JWT+ownership → 402 if short → per step `invoke('orchestrate-content', {...stepPayload})` + sync status. The cascade is faithful since orchestrate-content self-bills its own 10.

Two more material checks before I write: the campaign-level observation-node shape (mesh mandate) and the v1 `campaigns.platforms` type, plus any edge→edge invoke precedent.

## 🤖 Claude *(14:29:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== orchestrate-content observation node insert shape ===\"\ngrep -nE \"mcorch_nodes|node_type|relation_type|project_id|from\\(.mcorch\" supabase/functions/orchestrate-content/index.ts | head -20\necho \"\"\necho \"=== campaigns v1 columns (platforms type etc.) ===\"\nsed -n '104,125p' supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql 2>/dev/null\necho \"\"\necho \"=== edge->edge invoke precedent in functions/ ===\"\ngrep -rnE \"functions/v1/|functions\\.invoke\" supabase/functions/ 2>/dev/null | grep -v \"_shared\" | head -15",
  "description": "Observation node shape + campaigns columns + invoke precedent"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === orchestrate-content observation node insert shape ===
> 
> === campaigns v1 columns (platforms type etc.) ===
>   description TEXT,
>   objective TEXT,
>   target_audience JSONB DEFAULT '{}',
>   platforms social_platform[] DEFAULT '{}',
>   budget_cents INTEGER DEFAULT 0,
>   status campaign_status NOT NULL DEFAULT 'draft',
>   starts_at TIMESTAMPTZ,
>   ends_at TIMESTAMPTZ,
>   metadata JSONB DEFAULT '{}',
>   created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
>   updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
> );
> ALTER TABLE public.campaigns ENABLE ROW LEVEL SECURITY;
> 
> -- 9. CAMPAIGN METRICS
> CREATE TABLE public.campaign_metrics (
>   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
>   campaign_id UUID NOT NULL REFERENCES public.campaigns(id) ON DELETE CASCADE,
>   user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   platform social_platform,
>   impressions INTEGER DEFAULT 0,
>   clicks INTEGER DEFAULT 0,
> 
> === edge->edge invoke precedent in functions/ ===
> supabase/functions/agent-task-execute/index.ts:396:    targetResp = await fetch(`${supabaseUrl}/functions/v1/${cap.target_function}`, {
> supabase/functions/social-auth-callback/index.ts:48:    const callbackUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/social-auth-callback`;
> supabase/functions/publish-social/index.ts:85:      const refreshRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/refresh-social-token`, {
> supabase/functions/trigger-embeddings/index.ts:57:    const functionsUrl = `${supabaseUrl}/functions/v1/embed-mcorch-node`;
> supabase/functions/auto-publish/index.ts:70:          `${Deno.env.get("SUPABASE_URL")}/functions/v1/publish-social`,
> supabase/functions/self-heal/index.ts:80:          const refreshRes = await fetch(`${supabaseUrl}/functions/v1/refresh-social-token`, {
> supabase/functions/self-heal/index.ts:129:          const refreshRes = await fetch(`${supabaseUrl}/functions/v1/refresh-social-token`, {
> supabase/functions/social-auth-init/index.ts:51:    const callbackUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/social-auth-callback`;
> supabase/functions/orchestrate-step/index.ts:213:          const wpRes = await fetch(`${supabaseUrl}/functions/v1/publish-wordpress`, {
> supabase/functions/canvas-execute/index.ts:1041:  const webhookUrl = `${supabaseUrl}/functions/v1/higgsfield-webhook?token=${execution.webhook_token}`;
> supabase/functions/higgsfield-webhook/index.ts:3:// URL pattern: https://<project>.supabase.co/functions/v1/higgsfield-webhook?token=<webhook_token>
> ```

## 🤖 Claude *(14:29:17)*


## 🤖 Claude *(14:29:18)*

`campaigns.platforms` is `social_platform[]` (not orchestrate-content's platform names) — so I'll derive platforms from each step's `channel`, not pass campaign.platforms raw. Let me see the exact edge→edge dispatch pattern (agent-task-execute) and a clean mcorch_nodes insert precedent.

## 🤖 Claude *(14:29:20)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/agent-task-execute/index.ts",
  "offset": 388,
  "limit": 42
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 388	    return json({ status: "failed", error: "failed_to_create_execution", detail: insErr?.message }, 500);
> 389	  }
> 390	  const execId = execRow.id;
> 391	
> 392	  // 5. Invoke the real target module with the CALLER's auth (module enforces own RLS + BYOK)
> 393	  const t0 = Date.now();
> 394	  let targetResp: Response;
> 395	  try {
> 396	    targetResp = await fetch(`${supabaseUrl}/functions/v1/${cap.target_function}`, {
> 397	      method: "POST",
> 398	      headers: { "Content-Type": "application/json", "Authorization": authHeader },
> 399	      body: JSON.stringify(payload),
> 400	    });
> 401	  } catch (e) {
> 402	    const msg = e instanceof Error ? e.message : "fetch failed";
> 403	    await admin.from("agent_executions").update({
> 404	      status: "failed", error_msg: `target_unreachable: ${msg}`,
> 405	      latency_ms: Date.now() - t0, completed_at: new Date().toISOString(),
> 406	    }).eq("id", execId);
> 407	    await pulse(admin, "error");
> 408	    return json({ status: "failed", execution_id: execId, capability_key: capabilityKey, error: "target_unreachable", detail: msg }, 502);
> 409	  }
> 410	  const latencyMs = Date.now() - t0;
> 411	  const rawText = await targetResp.text();
> 412	  let result: unknown;
> 413	  try { result = JSON.parse(rawText); } catch { result = rawText; }
> 414	
> 415	  if (!targetResp.ok) {
> 416	    await admin.from("agent_executions").update({
> 417	      status: "failed", error_msg: `target_${targetResp.status}: ${rawText.slice(0, 500)}`,
> 418	      latency_ms: latencyMs, completed_at: new Date().toISOString(),
> 419	    }).eq("id", execId);
> 420	    await pulse(admin, "error");
> 421	    // 200 envelope with status:'failed' → frontend assertExecuteSuccess() throws (single error semantics)
> 422	    return json({ status: "failed", execution_id: execId, capability_key: capabilityKey, target_status: targetResp.status, result });
> 423	  }
> 424	
> 425	  // 6. Meter — module_self_bills → 0 (anti-double-charge); else base_mcoin_cost. Sovereign freebie.
> 426	  const costMcoin = cap.module_self_bills ? 0 : Number(cap.base_mcoin_cost ?? 0);
> 427	  let billed = false;
> 428	  if (costMcoin > 0 && user.id !== SOVEREIGN_USER_ID) {
> 429	    const { error: dErr } = await admin.rpc("deduct_mco_coins", { p_user_id: user.id, p_amount: costMcoin });
> ```

## 🤖 Claude *(14:29:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== mcorch_nodes insert precedents across edge functions ===\"\ngrep -rnE '\\.from\\(.?mcorch_nodes.?\\)\\.insert|node_type:|relation_type:' supabase/functions/ 2>/dev/null | grep -v \"_shared\" | head -20\necho \"\"\necho \"=== how orchestrate-content does its 'step 6 knowledge node' ===\"\ngrep -nE \"observation|knowledge|mcorch|mesh|node\" supabase/functions/orchestrate-content/index.ts | head -15",
  "description": "Edge dispatch pattern + mcorch_nodes insert precedent"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === mcorch_nodes insert precedents across edge functions ===
> supabase/functions/embed-mcorch-node/index.ts:336:        relation_type: "observes",
> supabase/functions/canvas-execute/index.ts:79:  node_type: string;
> supabase/functions/canvas-execute/index.ts:281:        node_type: dbNodeType,
> supabase/functions/canvas-execute/index.ts:528:          node_type: dbNodeType,
> supabase/functions/canvas-execute/index.ts:576:          node_type: body.node_type,
> supabase/functions/orchestrate-step/index.ts:407:        const observationInsert = admin.from("mcorch_nodes").insert({
> supabase/functions/orchestrate-step/index.ts:409:          node_type: "observation",
> supabase/functions/orchestrate-step/index.ts:428:          : admin.from("mcorch_nodes").insert({
> supabase/functions/orchestrate-step/index.ts:430:              node_type: "content_mesh_asset",
> supabase/functions/orchestrate-step/index.ts:455:            ? { wordpress_url: wpPostUrl || null, node_type: "observation", obs_id: (obsResult.value as any).data?.id ?? null }
> supabase/functions/publish-meta/index.ts:193:        const { data: obsNode } = await admin.from("mcorch_nodes").insert({
> supabase/functions/publish-meta/index.ts:195:          node_type: "observation",
> supabase/functions/publish-meta/index.ts:205:            relation_type: "observes",
> supabase/functions/handle-ml-postback/index.ts:294:    const { data: obsNode } = await supabase.from("mcorch_nodes").insert({
> supabase/functions/handle-ml-postback/index.ts:296:      node_type: "observation",
> supabase/functions/handle-ml-postback/index.ts:315:        relation_type: "ATTRIBUTES_REVENUE_TO",
> supabase/functions/whatsapp-webhook/index.ts:170:        const { data: obsNode } = await admin.from("mcorch_nodes").insert({
> supabase/functions/whatsapp-webhook/index.ts:172:          node_type: "observation",
> supabase/functions/whatsapp-webhook/index.ts:192:              relation_type: "observes",
> supabase/functions/higgsfield-webhook/index.ts:31:  node_type: string;
> 
> === how orchestrate-content does its 'step 6 knowledge node' ===
> 67:    const { topic, campaign_id, platforms = ["wordpress", "linkedin", "twitter"], site_url = "mcorch.com", wp_status = "draft" } = await req.json();
> 104:      : `mcorch_${topic.slice(0, 24).replace(/\s+/g, "_").toLowerCase()}`;
> 139:    const stepsOrder = ["article_generation", "wordpress_publish", "linkedin_post", "twitter_thread", "knowledge_mesh"];
> 148:      } else if (candidate === "knowledge_mesh") {
> ```

## 🤖 Claude *(14:29:26)*


## 🤖 Claude *(14:29:27)*

The dispatch pattern is clear (`fetch` with `Authorization: authHeader`). Let me grab the exact observation-node + OBSERVES-edge shape from a clean recent precedent (publish-meta) to mirror the mesh mandate correctly.

## 🤖 Claude *(14:29:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-meta/index.ts",
  "offset": 188,
  "limit": 28
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 188	          media_url: image_url ?? null,
> 189	          status: "published",
> 190	        });
> 191	
> 192	        // PROC-META-002 / data-model §4 — knowledge mesh observation (+ observes edge to source content).
> 193	        const { data: obsNode } = await admin.from("mcorch_nodes").insert({
> 194	          name: `post:${target}:${metaPostId}`,
> 195	          node_type: "observation",
> 196	          content: `Published ${target} post ${metaPostId}${postUrl ? ` — ${postUrl}` : ""}`,
> 197	          stability_score: 1.0,
> 198	          metadata: { platform: target, meta_post_id: metaPostId, campaign_id: campaign_id ?? null, event: "meta_publish" },
> 199	          user_id: userId,
> 200	        }).select("id").single();
> 201	        if (obsNode && content_node_id) {
> 202	          await admin.from("mcorch_edges").insert({
> 203	            source_id: obsNode.id,
> 204	            target_id: content_node_id,
> 205	            relation_type: "observes",
> 206	            weight: 1.0,
> 207	          });
> 208	        }
> 209	
> 210	        results.push({ platform: target, status: "published", meta_post_id: metaPostId, post_url: postUrl ?? undefined });
> 211	      } catch (err) {
> 212	        console.error(`publish-meta ${target} error:`, err);
> 213	        if (isAuthError(err)) authFailure = true;
> 214	        const message = (err as { message?: string })?.message ?? "publish_failed";
> 215	        await admin.from("meta_posts").insert({
> ```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-03 - Fix TradeUX deployment path and Docker setup]]
> * **Próxima Sessão**: [[2026-06-03 - a9beda03-6192-4989-aed8-b75558abf414]]
%% --- TIMELINE END --- %%

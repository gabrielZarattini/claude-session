# [[2026-06-20 - Próximos passos do projeto|Próximos passos do projeto]]
**Date:** 2026-06-23 | **Session ID:** `c67bdd85-cf56-48e9-9a5f-8025b37faa8e`

---

## 👤 User *(03:34:18)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(03:34:18)*

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


## 🤖 Claude *(03:34:21)*


## 🤖 Claude *(03:34:22)*

I'll execute the ShakeHands /handson pick-up protocol. Let me start with the pre-flight checks in parallel.

## 🤖 Claude *(03:34:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7",
  "description": "Recent commit history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 21bc53d chore(sprint): v6.47.0 — per-user 100% (env=infra) + CF WP unblock + sweep fechado
> bdb56b1 docs(handoff): seal per-user 100% (env=infra) + CF WP unblock + sweep per-user fechado
> a77a8e2 docs(readme): v6.47.0 — per-user 100% (env=infra) + CF WP unblock + sweep per-user fechado
> f6734e9 feat(fetch-trends): per-user Apify/RapidAPI BYOK (fecha #3 do sweep per-user)
> 432fa01 refactor(edge): provider keys 100% per-user (env = só infra) + MESH_EMBED dedicada
> dbad262 docs(processes): WP↔CF resolvido (Nível de segurança) + SOP per-user multi-tenant
> 4583519 refactor(edge): resolução de credencial per-user (API Tenancy Model)
> ```

## 🤖 Claude *(03:34:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git status --short",
  "description": "Uncommitted changes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  D proof-manifest.json
> ```

## 🤖 Claude *(03:34:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff HEAD --stat",
  "description": "Change scope"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  proof-manifest.json | 1 -
>  1 file changed, 1 deletion(-)
> ```

## 🤖 Claude *(03:34:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(03:34:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker mesh status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 6 days (healthy)
> mcorch_claude_mem: Up 7 days (healthy)
> mcorch_chroma: Up 7 days (healthy)
> ---
> mega-brain-dashboard: Up 7 days
> mega-brain-webhook: Up 7 days (healthy)
> mega-brain-daemon: Up 7 days (healthy)
> ```

## 🤖 Claude *(03:34:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat",
  "description": "Chroma API v2 health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1782185666826909269}
> ```

## 🤖 Claude *(03:34:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---scratch---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"; echo \"---handoff---\"; wc -l HANDOFF.md",
  "description": "BoK suites + scratch + HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> agentic-workspace
> aios-sql-bridge
> authenticated-browser-operator
> canvas-design
> constellation-v2
> conteudo-v2
> e2e-user-zero
> gamificacao-nodes
> identity-fabric
> marketing-hub
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> post-engine
> security
> video-studio
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> ---scratch---
> scratch has files
> ---handoff---
> 8222 HANDOFF.md
> ```

## 🤖 Claude *(03:34:31)*


## 🤖 Claude *(03:34:31)*

Pre-flight clean. TypeScript: zero errors. Now reading HANDOFF.md (read-from-end strategy) and supporting context.

## 🤖 Claude *(03:34:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 71
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
> 14	## Session Seal — Per-user 100% (env = só infra) + CF WP unblock + sweep per-user FECHADO (2026-06-22)
> 15	
> 16	`/handson` → "resolver o CF WAF + secrets, depois os próximos passos". Arco: **(1)** desbloqueio material do CF no `/wp-json` → **(2)** SOP per-user WP↔CF → **(3)** fix do token vazado `aios-chat-gateway` → **(4)** auditoria de prontidão per-user (workflow) → **(5)** diretiva Sovereign **"env = só infra, todo provider key per-user BYOK"** → migração de 27 fns + #3 fetch-trends. Surpresa material decisiva: o componente de skip que faltava no Cloudflare era **"Nível de segurança"** (challenge por reputação de IP de **datacenter**, não bot/UA) — diagnosticado lendo o **Security→Events** (a regra Skip já disparava `Ignorar`, mas o `Nível de segurança` desafiava por cima). O teste E2E "falhou bonito" (OpenRouter respondeu 404 de modelo + `user_id` → **provou** que a chave per-user autenticou).
> 17	
> 18	**O que foi entregue (6 commits granulares):**
> 19	1. **CF WP unblock (`ação Sovereign` + verificação).** Secrets `WP_PUBLISH_SECRET`/`_HOST` provisionados + regra CF Skip header-gated com **Nível de segurança** marcado → `curl` com header sai do 403 (200 + JSON real do WP), sem header continua 403 (mundo barrado). E2E `publish-wordpress` → `{"success":true,"post_id":18}` (rascunho de teste deletado). SOP `wordpress-cf-publish-unblock.md` atualizada com o achado + diagnóstico via Events; novo SOP `wordpress-cf-per-user-publish.md` (multi-tenant, Lei 2).
> 20	2. **`aios-chat-gateway` token vazado (`ef921ce`).** Literal hardcoded removido + fail-closed 501 + telemetria. Rotação = decisão consciente do Owner (diferida — repo privado, sem público, sem outros users). Secret setado com valor atual (sem rotacionar).
> 21	3. **Auditoria per-user (workflow `wf_102ef5ac`, 49 fns).** Ledger: 30 per-user · 11 fallback-ok · 4 remediadas. Achados de segurança bônus (não-per-user, próxima sessão): `social-auth-callback` state sem HMAC (cross-tenant), `instagram-webhook` sem signature.
> 22	4. **Migração env=só-infra (`4583519`+`432fa01`).** Removido `|| Deno.env.get(<provider>)` de **25 fns user-facing** (47 ocorrências) → per-user PURO fail-closed. 2 fns de sistema (`embed-mcorch-node` NUCLEAR + `search-constellation`) → `MESH_EMBED_OPENROUTER_KEY`/`MESH_EMBED_GEMINI_KEY` dedicadas. BYOK do User 0 seedado do `.env` (higgsfield_api_key estava null). 27 fns deployadas 0 falhas.
> 23	5. **#3 fetch-trends per-user (`f6734e9`).** Migration `20260622210000` adiciona coluna cifrada `rapidapi_key` (espelha template firecrawl verbatim; `apify_token` já existia) + edge fn per-user fail-closed 402 + UI Settings (Apify/RapidAPI) + seed User 0. `/security-review` SAFE.
> 24	
> 25	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (GOs via AskUserQuestion) + `/security-review` independente 2× · Owner=Sovereign (blast radius = pipeline de conteúdo do User 0 + carteira + isolamento multi-tenant; rotação de secrets vazados diferida conscientemente).
> 26	
> 27	| Verificação (material) | Resultado |
> 28	|---|---|
> 29	| CF WP unblock | ✅ curl com header 200 + JSON WP · sem header 403 · E2E `publish-wordpress` `post_id 18` |
> 30	| Migração per-user | ✅ 47 fallbacks removidos · 0 resíduo · 27 fns deployadas 0 falhas |
> 31	| Embedding pipeline pós-rename | ✅ `embed-mcorch-node` 200 `dims:768` (MESH_EMBED funciona) |
> 32	| Per-user E2E | ✅ openrouter-swarm: OpenRouter autenticou com chave per-user do User 0 |
> 33	| #3 fetch-trends fail-closed | ✅ throwaway sem key → 402 `trends_not_configured` (zero-cost) |
> 34	| Migration rapidapi_key | ✅ `db push` aplicada · coluna `••••`/null · `/security-review` SAFE |
> 35	| `/security-review` | ✅ SAFE 2× (migração CF host-gate prévia + migração rapidapi) |
> 36	| tsc · gitleaks | ✅ 0 erros · gitleaks limpo nos 6 commits |
> 37	| Handoff node | `4e57bf72-8cc0-4e1c-ae48-10d7f19b0dac` (embedded 768d) |
> 38	
> 39	### Survival Laws Self-audit
> 40	```
> 41	Law 1 (Materiality): ✅ Toda claim provada NESTE arco — CF via curl 200/403 + post_id 18; migração via grep 0-resíduo + 27 deploys; embedding via 200 dims:768; per-user via OpenRouter user_id; fetch-trends via 402 throwaway. O E2E "falhou bonito" PROVOU a chave per-user (não fabriquei). Pego material: o trap do canvas-execute Higgsfield (row null/secret → approach atômico evitou regressão); o caveat do datacenter IP (Nível de segurança). Fase 5c mecânica abaixo.
> 42	Law 2 (Process): ✅ SOPs antecipados ([[wordpress-cf-per-user-publish|wordpress-cf-per-user-publish]] · [[trends-credential-resolution|trends-credential-resolution]]) ANTES do código; migration espelha template live verbatim (não inventa).
> 43	Law 3 (Pruning): ✅ Sessão MUITO densa empacotada (CF → auditoria → migração 27 fns → #3) sob GOs explícitos; selada ao FECHAR o objetivo-prioridade (per-user em tudo) a pedido do Sovereign.
> 44	Law 4 (ORO): ✅ Triplet declarado; múltiplos GOs via AskUserQuestion (chave de sistema · execução · #3); /security-review como Reviewer mecânico independente 2×; rotação de secrets = decisão consciente do Owner registrada.
> 45	```
> 46	
> 47	## Session Seal — Alertas resolvidos + Vídeo Fatia 1/1b + De-n8n (motor faceless nativo) (2026-06-22)
> 48	
> 49	`/handson` → "resolver os alertas, depois os próximos passos". Arco: diagnóstico material (workflow paralelo de 3 agentes) dos alertas → reparo/reconciliação → Vídeo Fatia 1 (domínio+contrato) → Fatia 1b (UI) → diretiva Sovereign **De-n8n** → emenda BoK SDD v1.2. Duas surpresas materiais: a security BoK estava **selada** (naming alternativo enganou o handson) e os "gaps físicos" FM-04/FM-10 já estavam **fechados** (docs stale). O smoke pegou 2 bugs reais antes de virar prod.
> 50	
> 51	**O que foi entregue (8 commits granulares):**
> 52	1. **Alertas (`0fc7ed9`/`89e59ab`).** CF managed challenge 403 em `/wp-json/*` confirmado material → `publish-wordpress` header `X-MCORCH-Publish` **host-gated fail-closed** (`/security-review` pegou+fechou um HIGH conf 9 na própria mudança) + SOP `wordpress-cf-publish-unblock.md` (regra CF + secrets `WP_PUBLISH_SECRET`/`_HOST` = ação Sovereign). FM-04 (RPN 300)/FM-10 já fechados (compose saneado + `docker inspect mcorch_claude_mem` sem env legada + Dockerfile UID1001) → drift FMEA+CLAUDE.md reconciliado. Image path já resolvido (OpenRouter Gemini).
> 53	2. **Vídeo Fatia 1 (`c92850f`/`e3b0716`).** Migration `20260622040000`: `video_renders`+`video_assets`+`finalize_video_render` (RLS cross-tenant FMEA-VS-020 — SELECT own-or-org-member, **sem write authenticated**, RESTRICTIVE no-delete; espelha `finalize_vision_job`). Edge fns `video-render`/`video-render-poll` (JWT→voice_consent→BYOK `google_api_key` fail-closed→dry_run→**worker-gate 503 antes de deduct**→[Fatia2] deduct→insert→trigger→refund idempotente). Custos `VIDEO_FACELESS_RENDER=125`/`VIDEO_HYPERFRAMES_RENDER=12` (OTD-VS-007).
> 54	3. **Fatia 1b UI (`f343dd2`).** `/dashboard/video` (`useVideoRender`+`VideoStudioPage` display-only) + nav "Estúdio de Vídeo" + types.ts regen additive; deployada.
> 55	4. **De-n8n (`792edb0`/`167cfc3`).** Diretiva Sovereign: MCORCH **não usa n8n** (single-tenant não escala num SaaS per-user). Emenda BoK SDD **v1.2 §1.5** supera §1.2/§1.4; **OTD-VS-001 (ponte R5) VOID**; motor faceless nativo (Visual Orchestrator + capabilities existentes co-locadas na `mcorch-sovereign-net`). Fix doc coluna BYOK `google_api_key` (não `gemini_api_key`).
> 56	
> 57	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (GOs via AskUserQuestion) + `/security-review` independente 3× · Owner=Sovereign (blast radius = publish prod + isolamento multi-tenant do vídeo + carteira).
> 58	
> 59	| Verificação (material) | Resultado |
> 60	|---|---|
> 61	| `publish-wordpress` reparada + deployada | ✅ 106.3kB · boot-smoke HTTP 401 · /security-review HIGH fechado+reverificado RESOLVED |
> 62	| Migration video-studio | ✅ `db push` exit 0 · tabelas 200 · finalize anon→42501 · anon INSERT→42501 RLS |
> 63	| Edge fns video-render/poll | ✅ deployadas 61.8/58.6kB · **18 gates zero-cost** (401/422/409/402/dry_run 125+12/503/poll 422/404) · saldo 5096 intacto |
> 64	| `/security-review` | ✅ SAFE 3× (publish-wordpress · migration 6-vetores · edge fns) |
> 65	| Emenda BoK SDD v1.2 | ✅ §1.5 De-n8n · OTD-VS-001 VOID · 00-index reconciliado |
> 66	| tsc · build | ✅ 0 erros · build OK (chunk `VideoStudioPage` no dist, env baked) |
> 67	| Commits | `0fc7ed9` · `89e59ab` · `c92850f` · `e3b0716` · `792edb0` · `f343dd2` · `167cfc3` (+ readme + handoff) |
> 68	| Handoff node | `bb23b9dc-265e-4338-9709-d320371908b4` (embedded 768d) |
> 69	
> 70	### Survival Laws Self-audit
> 71	```
> ```

## 🤖 Claude *(03:34:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7822,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7822	ContentLibraryPage monetization flow:
> 7823	  Card (text, body contains mercadolivre.com.br)
> 7824	    └── DropdownMenu → "Monetizar Links ML"
> 7825	          → handleMonetizeLinks(item):
> 7826	               match(ML_URL_RE) → unique URLs
> 7827	               for url of unique:
> 7828	                 POST process-affiliate-link → affiliate_url
> 7829	                 body.split(url).join(affiliate_url)
> 7830	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7831	          → Badge 💰 ML (emerald) exibido após monetização
> 7832	```
> 7833	
> 7834	---
> 7835	
> 7836	## Pending Actions (Commercial Launch)
> 7837	
> 7838	### CRITICAL — Must complete before first client
> 7839	
> 7840	🎯. **[Fatias 1/1b/2 SHIPPED — pendente: ativação Sovereign + trends] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 7841	
> 7842	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 7843	
> 7844	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7845	
> 7846	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7847	
> 7848	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7849	
> 7850	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7851	
> 7852	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7853	
> 7854	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7855	
> 7856	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7857	
> 7858	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7859	
> 7860	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7861	
> 7862	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7863	   ```bash
> 7864	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7865	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7866	   ```
> 7867	
> 7868	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7869	
> 7870	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7871	
> 7872	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7873	
> 7874	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7875	
> 7876	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7877	
> 7878	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7879	
> 7880	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7881	
> 7882	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7883	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7884	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7885	
> 7886	### SOCIAL — Next steps
> 7887	
> 7888	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7889	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7890	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7891	
> 7892	### NON-CRITICAL
> 7893	
> 7894	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7895	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7896	- `browserslist` — ✅ updated (2026-04-26)
> 7897	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7898	
> 7899	### GITNEXUS MCP — Next steps
> 7900	
> 7901	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7902	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7903	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7904	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7905	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7906	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7907	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7908	
> 7909	### PHASE EPSILON — Next iterations
> 7910	
> 7911	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7912	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7913	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7914	
> 7915	### CORE — Next iterations
> 7916	
> 7917	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7918	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7919	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7920	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7921	
> 7922	### PHASE DELTA — Next iterations
> 7923	
> 7924	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7925	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7926	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7927	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7928	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7929	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7930	
> 7931	### USUÁRIO ZERO — Checklist de validação
> 7932	
> 7933	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7934	- ✅ Stripe sandbox secrets no vault
> 7935	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7936	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7937	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7938	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7939	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7940	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7941	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7942	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7943	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7944	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7945	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7946	
> 7947	---
> 7948	
> 7949	## Infrastructure
> 7950	
> 7951	| Service | Container | Port | Status |
> 7952	|---------|-----------|------|--------|
> 7953	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7954	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7955	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7956	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7957	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7958	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7959	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7960	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7961	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7962	
> 7963	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7964	
> 7965	```bash
> 7966	docker compose up -d
> 7967	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7968	```
> 7969	
> 7970	---
> 7971	
> 7972	## Security Model (Post-Go-Live)
> 7973	
> 7974	| Table | Isolation |
> 7975	|-------|-----------|
> 7976	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 7977	| `mcorch_edges` | Same pattern |
> 7978	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 7979	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 7980	
> 7981	---
> 7982	
> 7983	## Billing Architecture
> 7984	
> 7985	| Decision | Value |
> 7986	|----------|-------|
> 7987	| Canonical billing ledger | `profiles.mco_balance` |
> 7988	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 7989	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 7990	| Orchestration cost | 10 mcoCoins/run |
> 7991	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 7992	| Stripe | Sandbox keys active — swap to live before first client |
> 7993	
> 7994	---
> 7995	
> 7996	## GraphRAG State
> 7997	
> 7998	- **8946 total nodes** (verificado live 2026-06-22 via REST count=exact, alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 7999	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8000	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8001	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8002	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8003	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8004	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8005	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8006	- HNSW cosine index operational
> 8007	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8008	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8009	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8010	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8011	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8012	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8013	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8014	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8015	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8016	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8017	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8018	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8019	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8020	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8021	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8022	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8023	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8024	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8025	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8026	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8027	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8028	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8029	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8030	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8031	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8032	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8033	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8034	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8035	
> 8036	### Embedding Model
> 8037	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8038	Schema: `vector(768)` — HNSW cosine index.
> 8039	
> 8040	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8041	Três camadas eliminam intervenção manual:
> 8042	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8043	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8044	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8045	
> 8046	### Comandos de manutenção da Mesh
> 8047	```bash
> 8048	# Verificar nós sem embedding (deveria retornar array vazio):
> 8049	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8050	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8051	
> 8052	# Backfill manual (Bun-native — requer .env):
> 8053	bun run scripts/backfill-embeddings.ts
> 8054	
> 8055	# Backfill de código-fonte nos nós AST:
> 8056	bun run scripts/backfill-node-content.ts
> 8057	
> 8058	# Re-sync AST completo:
> 8059	cd packages/gitnexus-core && npm run sync-mesh
> 8060	
> 8061	# Acompanhar re-ingesta pós-commit:
> 8062	tail -f /tmp/mcorch-ingest.log
> 8063	```
> 8064	
> 8065	---
> 8066	
> 8067	## Video Rescue Protocol
> 8068	
> 8069	When a video generation operation (Google Veo) times out or client disconnects:
> 8070	```bash
> 8071	# Via edge function (production):
> 8072	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8073	  -H "Authorization: Bearer <user_jwt>" \
> 8074	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8075	
> 8076	# Via local script (admin/debug):
> 8077	source .env && bun run rescue.ts <operation_id> <content_id>
> 8078	```
> 8079	
> 8080	---
> 8081	
> 8082	## Architecture Pillars
> 8083	
> 8084	| Layer | Implementation |
> 8085	|-------|---------------|
> 8086	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8087	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8088	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8089	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8090	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8091	
> 8092	---
> 8093	
> 8094	## Phase Delta — Architecture
> 8095	
> 8096	```
> 8097	OrchestrationPage (full-canvas, p-0)
> 8098	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8099	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8100	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8101	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8102	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8103	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8104	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8105	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8106	
> 8107	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8108	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8109	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8110	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8111	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8112	```
> 8113	
> 8114	### Canvas State Architecture (Hybrid)
> 8115	
> 8116	```
> 8117	User interaction → ReactFlow internal state (positions, drag)
> 8118	                         ↓ (debounced 600ms)
> 8119	                   localStorage (positions persist across refresh)
> 8120	                         ↑
> 8121	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8122	     ↓ (status changes sync to ReactFlow via useEffect)
> 8123	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8124	```
> 8125	
> 8126	## Key Files
> 8127	
> 8128	| Purpose | Path |
> 8129	|---------|------|
> 8130	| Architecture rules | `CLAUDE.md` |
> 8131	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8132	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8133	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8134	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8135	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8136	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8137	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8138	| **Node types** | `src/components/orchestrator/nodes/` |
> 8139	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8140	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8141	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8142	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8143	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8144	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8145	| Billing utilities | `src/lib/billing.ts` |
> 8146	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8147	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8148	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8149	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8150	| Video rescue (local) | `rescue.ts` |
> 8151	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8152	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8153	| Deploy harness | `scripts/harness-deploy.sh` |
> 8154	
> 8155	---
> 8156	
> 8157	## First Client Onboarding Checklist
> 8158	
> 8159	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8160	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8161	3. ~~Activate watchdog cron~~ ✅ Done
> 8162	4. ~~Deploy rescue-video function~~ ✅ Done
> 8163	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8164	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8165	7. Monitor `infra_health_logs` for first 24h.
> 8166	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8167	
> 8168	---
> 8169	
> 8170	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8171	
> 8172	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8173	
> 8174	| Action | Result |
> 8175	|--------|--------|
> 8176	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8177	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8178	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8179	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8180	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8181	
> 8182	| Commit | Conteúdo |
> 8183	|--------|----------|
> 8184	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8185	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8186	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8187	
> 8188	### Arquitetura Matrix Intelligence
> 8189	
> 8190	```
> 8191	ConstellationMatrix (Stabilized Engine)
> 8192	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8193	  └── NodeDetailsPanel (Tabbed Navigation)
> 8194	        ├── Tab Meta: Neighbor exploration + Net Context
> 8195	        ├── Tab Code: Source code preview (Supabase sync)
> 8196	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8197	
> 8198	useNodeIntelligence Hook:
> 8199	  - contentQuery: fetch nodes.content column
> 8200	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8201	  - state: isAnalyzing, analysisResult, progress
> 8202	```
> 8203	
> 8204	---
> 8205	
> 8206	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8207	
> 8208	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8209	
> 8210	| Action | Result |
> 8211	|--------|--------|
> 8212	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8213	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8214	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8215	
> 8216	**Output da análise (estruturado em pt-BR):**
> 8217	- Visão Geral — papel do módulo no sistema
> 8218	- Padrões Detectados — design patterns, antipatterns
> 8219	- Acoplamento & Dependências — análise In/Out-Degree
> 8220	- Recomendações — 1-3 ações priorizadas
> 8221	
> ```

## 🤖 Claude *(03:34:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"---sprint---\"; cat .claude/context/sprint-priorities.md 2>/dev/null | head -60",
  "description": "Scratch contents + sprint priorities"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (51.9KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/c67bdd85-cf56-48e9-9a5f-8025b37faa8e/tool-results/b08lmt4ew.txt
> 
> Preview (first 2KB):
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 23 00:03 ..
> ---sprint---
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.47.0 — Per-user 100% (env = só infra) + CF WP unblock + sweep per-user FECHADO (2026-06-22)** — `/handson` → "resolver CF WAF + secrets, depois os próximos passos". **(1) CF WP unblock RESOLVIDO:** o componente de skip que faltava no Cloudflare era **"Nível de segurança"** (challenge por reputação de IP de **datacenter** Oracle AS31898, não bot/UA) — diagnosticado via Security→Events (a regra Skip já disparava `Ignorar`, mas o Nível de segurança desafiava por cima). Regra CF header-gated + secrets `WP_PUBLISH_SECRET`/`_HOST`; E2E `publish-wordpress`→`post_id 18`. SOPs `wordpress-cf-publish-unblock.md` (atualizada) + `wordpress-cf-per-user-publish.md` (multi-tenant). **(2) Diretiva Sovereign env=só-infra:** auditoria per-user (workflow `wf_102ef5ac`, 49 fns; 30 per-user · 11 fallback-ok · 4 remediadas) → removido `|| Deno.env.get(<provider>)` de **25 fns user-facing** (47 ocorrências) → per-user PURO fail-closed; 2 fns de sistema (`embed-mcorch-node`/`search-constellation`) → `MESH_EMBED_*` dedicadas; secrets antigos mantidos (seed source) + `.env` anotado. **(3) Sweep per-user FECHADO:** #1 openrouter-swarm · #2 canvas-execute Higgsfield · #3 fetch-trends (migration `rapidapi_key` + UI + 402 provado) · + `aios-chat-gateway` token vazado fail-closed. BYOK do User 0 seedado do `.env`. **Prova:** `/security-review` SAFE 2× · 27 fns deployadas 0 falhas · embedding pós-rename 200 · OpenRouter autenticou com chave per-user do User 0 · tsc 0 · gitleaks limpo · Phase 5c 
> ...
> </persisted-output>
> ```

## 🤖 Claude *(03:34:44)*


## 🤖 Claude *(03:34:44)*

I have the full picture. Let me quickly clarify the one pending change (the staged `proof-manifest.json` deletion) before composing the brief.

## 🤖 Claude *(03:34:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log -1 --format=\"%h %s\" -- proof-manifest.json 2>/dev/null; echo \"---last known content (from HEAD)---\"; git show HEAD:proof-manifest.json 2>/dev/null | head -20 || echo \"(not in HEAD)\"",
  "description": "Inspect deleted proof-manifest.json origin"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 127b1a1 chore(sprint): registra v6.44.0 — Viral Autopilot Fatia 2 (cadência R2 + loop R3 + UI)
> ---last known content (from HEAD)---
> {"handoffNodeId": "280e94d7-8de7-43bb-aee7-89d1824042d7"}
> ```

## 🤖 Claude *(03:34:50)*


## 🤖 Claude *(03:35:16)*

All context gathered. Here's the pick-up brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Per-user 100% (env = só infra) + CF WP unblock (2026-06-22)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
**Fase selada:** Per-user 100% (env = só infra) + CF WordPress unblock + sweep per-user FECHADO — `v6.47.0`
**Últimos commits:**
- `21bc53d` — chore(sprint): v6.47.0 — per-user 100% (env=infra) + CF WP unblock + sweep fechado
- `f6734e9` — feat(fetch-trends): per-user Apify/RapidAPI BYOK (fecha #3 do sweep per-user)
- `432fa01` — refactor(edge): provider keys 100% per-user (env = só infra) + MESH_EMBED dedicada
- `dbad262` — docs(processes): WP↔CF resolvido (Nível de segurança) + SOP per-user multi-tenant

📂 **MUDANÇAS PENDENTES**
- `D proof-manifest.json` (staged) — artefato transitório da Fase 5c do seal anterior (`{"handoffNodeId":"280e94d7…"}`, commitado em `127b1a1`). Deleção benigna; o próximo `/handoff` regenera. **Não commitar isoladamente.**
- `scratch/` tem arquivos — output 51.9KB (não inspecionado a fundo; protocolo sugere mover para `.claude/scripts/db/` quando relevante).

🏗️ **INFRA** — tudo verde
- `mcorch_chroma`: Up 7 days (healthy) — Chroma API v2: **OK** (`heartbeat` respondeu)
- `mcorch_claude_mem`: Up 7 days (healthy) · `mcorch_vision_mcp`: Up 6 days (healthy)
- `mega-brain-daemon`/`-webhook`: healthy · `-dashboard`: up

🧠 **KNOWLEDGE MESH**
- **8946 nós** · **9070 arestas** (fonte: GraphRAG State, count=exact live 2026-06-22) — 100% embedded (768d HNSW cosine)
- Top tipos: handoff · milestone · architecture · decision · observation · documentation_suite · requirement + AST (file/function/class)

🔧 **TYPESCRIPT** — Zero erros ✅

📚 **BoK SUITES** — 22 suites em `docs/bok/` (todas as significativas seladas 9/9: vision-mcp `318862b7`, viral-autopilot `b3398294`, marketing-hub `d5163fed`, security blueprint `6b1571a`, video-studio). Nenhum gate aberto bloqueando código novo.

📌 **SPRINT**
**Goal:** Distribuição social autônoma operacional — pipeline publica LinkedIn auto; Twitter ao subir tier; Instagram após App Review Meta.
**Top gap:** Ativação do **1º ciclo PAGO** do Viral Autopilot — agora destravada (os 2 blockers de saída visível, CF WAF `/wp-json` e OpenAI image, foram **ambos resolvidos** nesta sessão e na anterior).

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **🎯 Viral Autopilot — ativação Sovereign + 1º ciclo PAGO.** Motor R1-R4 completo e provado zero-cost. Pendente: **(A)** ação Sovereign — ativar o `pg_cron` schedule que chama `autopilot-cadence-cron` + rodar o 1º ciclo com mco real (blockers CF WP **resolvidos** ✅; OpenAI image **resolvido** via OpenRouter Gemini ✅); **(B)** `fetch-trends`→pauta (FR-VA-018, último item autônomo).
2. **🔐 Achados de segurança bônus da auditoria per-user** (próxima sessão, flagados no seal): `social-auth-callback` com `state` sem HMAC (risco cross-tenant) + `instagram-webhook` sem verificação de signature.
3. **🌌 Unified Sensorial Canvas — Fases 3.5-3.10** (Phase Epsilon V9): sinapses inter-rede reais, fly-to, perf (`OTD-UCANVAS-PERF` — query do código ~30s), poda squad-coloring, paridade + cutover + seal.

⚠️ **ALERTAS** — Nenhum bloqueador ✅
- Containers todos healthy · TS zero erros · sem mudanças conflitantes no working tree.
- Nota menor: `scratch/` não-vazio e `proof-manifest.json` com deleção staged (ambos benignos, descritos acima).

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

A sessão anterior fechou o objetivo-prioridade (per-user em tudo + CF WP unblock). O caminho mais alto-valor agora é **acender o Viral Autopilot em produção** — os dois blockers que o gatilhavam foram derrubados. Isso exige uma ação Sovereign (ativar o `pg_cron` + GO para gasto real de mcoCoins). Quer que eu prepare o comando exato do `pg_cron` schedule e os pré-checks materiais para esse 1º ciclo, ou prefere atacar outro item?

## 👤 User *(03:38:37)*

ótimo vamos com os próximos passos

## 🤖 Claude *(03:39:27)*


## 🤖 Claude *(03:39:29)*

Perfeito. Vou seguir a ordem de prioridade dos próximos passos, começando pelo #1 — **preparar a ativação do Viral Autopilot** (comando exato do `pg_cron` + pré-checks materiais para o 1º ciclo pago), que foi exatamente o que ofereci. Deixo o gate de gasto real e o `pg_cron` prontos para o seu GO, e sigo para o item autônomo restante (`fetch-trends`→pauta, FR-VA-018).

Primeiro, levantamento material do estado do motor. Vou ler o SOP de identidade do cron, a função executora e as migrations, em paralelo.

## 🤖 Claude *(03:39:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/autopilot-cron-identity.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SOP: Viral Autopilot — Cron Identity + Pre-Debit/Refund Atomicity (`autopilot-cron-identity`)
> 2	
> 3	**Status:** ACTIVE · v1.0 · 2026-06-20
> 4	**Owner:** Sovereign (Gabriel Zarattini)
> 5	**Survival Law 2 compliance:** Escrito **ANTES** de qualquer código da fatia de cadência/custo do Viral Autopilot (R2 recorrência + R3 loop). Abre o gate **OTD-VA-008** (`docs/bok/viral-autopilot/05-sdd.md:425` — *"Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer código"*) e cobre o pré-débito/refund atômico de **FR-VA-007** + o cap diário de **FR-VA-021**.
> 6	**Canonical directive:** `CLAUDE.md > "API Tenancy Model — Per-User Credentials"` · `.claude/rules/survival.md > Law 1 (Materiality) / Law 2 (Anticipated Process)` · `docs/bok/viral-autopilot/{04-frd,05-sdd,06-data-model}.md`
> 7	**Sibling SOPs:** `edge-jwt-identity-verification.md` (camada-3 service-role gate, base deste) · `orchestrate-async-pipeline.md` (mandato `verify_jwt=false` + pg_net + contrato de param-name dos RPCs).
> 8	
> 9	---
> 10	
> 11	## Context
> 12	
> 13	A fatia de cadência do Viral Autopilot introduz **automação financeira autônoma**: um `pg_cron` dispara a geração+publicação de criativos a cada N dias, **sem mão humana no loop**, gastando `mco_balance` do tenant. Dois riscos materiais nascem disso:
> 14	
> 15	1. **Identidade do caminho cron (SEC-VA-CRIT-01 / OTD-VA-008).** As funções `autopilot-*` rodam com `verify_jwt = false` em `supabase/config.toml` — o gateway Kong **não** valida JWT (mesmo motivo de todo o ecossistema: a sessão do usuário é ES256, o gateway está configurado para o segredo HS256 legado; ver `edge-jwt-identity-verification.md`). O cron **não possui** um JWT de usuário para repassar. A tentação fatal é confiar num header `x-autopilot-user-id` vindo do request — o que deixaria **qualquer** chamador drenar a carteira de **qualquer** vítima (`POST autopilot-run` com `x-autopilot-user-id: <victim>` → débito + publicação na conta da vítima). A validação adversarial da BoK (Fase 6, rodada R1) marcou exatamente este vetor como **blocker**.
> 16	
> 17	2. **Atomicidade do pré-débito/refund (FR-VA-007 / TOCTOU SEC-VA-04).** Um ciclo gera `N_runs = |produtos| × |redes| × ab_variants` sub-runs, cada um um bundle flat de 10 mcoCoins (`billing.ts:16-21` — imagem **já incluída**). Se cada sub-run se auto-cobrar, uma falha no meio deixa o tenant cobrado por trabalho não-entregue; se o cap diário for checado com um `SELECT` separado do `deduct`, dois ciclos concorrentes passam o cap juntos (TOCTOU). A rodada R2 da validação pegou um **anti-mint** que eu mesmo introduzi: refund implementado como `deduct` de valor negativo viola o guard `p_amount <= 0` de `deduct_mco_coins` (`migration 20260603220000:45`) — refund **tem** que ser crédito positivo.
> 18	
> 19	**Regra-mãe:** confiar num `user_id` no caminho cron só é permitido depois de **provar posse da `SB_SECRET_KEY` in-function** E de derivar o `user_id` de uma **linha confiável do banco** (`autopilot_plans.user_id` / `autopilot_cycles.user_id`), **nunca do corpo/header do request**. Todo movimento de saldo passa por **um** RPC `SECURITY DEFINER` service-role-only, com cap + débito na **mesma transação sob advisory lock**, e refund como **crédito positivo idempotente**.
> 20	
> 21	---
> 22	
> 23	## ORO triplet
> 24	
> 25	- **Operator:** MCORCH Master Execution Agent (autoria das migrations/funções) + `pg_cron` apresentando a Vault key (execução por tick) + Edge runtime Deno (gate por request).
> 26	- **Reviewer:** Sovereign (Gabriel) — aprova as migrations + valida os smokes zero-cost e o exploit test pós-deploy · `/security-review` independente em **cada** migration (mandato `CLAUDE.md`).
> 27	- **Owner:** Sovereign — blast radius = **carteira do tenant gasta autonomamente** (mint/drain cross-tenant se a identidade falhar; sangria silenciosa se o cap/refund falhar).
> 28	
> 29	---
> 30	
> 31	## Operator (equivalente manual — material)
> 32	
> 33	A automação substitui o seguinte ritual humano que o Sovereign executaria **hoje, à mão**, a cada janela de cadência, para cada plano ativo:
> 34	
> 35	| # | Passo manual | Critério de sucesso material |
> 36	|---|--------------|------------------------------|
> 37	| 1 | Abrir a UI do Autopilot e listar os planos cujo `next_run_at` venceu | Lista de `plan_id` vencidos visível |
> 38	| 2 | Para cada plano: conferir o `mco_balance` **e** quanto já gastou hoje (não estourar o cap diário) | `balance` e `gasto_hoje` lidos antes de qualquer clique |
> 39	| 3 | Calcular `N_runs = produtos × redes × variants` e `projetado = N_runs×10 + 2` | Número conferido contra o cap do plano |
> 40	| 4 | Clicar "gerar agora" **uma vez** por plano (dispara os sub-runs) | 1 débito de `projetado`, depois os sub-runs publicam |
> 41	| 5 | Aguardar os sub-runs; anotar quantos **de fato** publicaram | `actual` real conhecido |
> 42	| 6 | Reconciliar: devolver ao saldo os coins dos runs que **não** entregaram | `balance` final = inicial − `actual` |
> 43	| 7 | Reagendar o plano para a próxima janela (`next_run_at += interval_days`) | Plano re-armado |
> 44	
> 45	O `pg_cron` automatiza os passos 1–7. **O gate Lei 2 existe porque automatizar o passo 2 (cap) e o passo 6 (refund) errado = sangria silenciosa de carteira.** O precedente vivo desta topologia é **`nurture-cron` → `nurture-dispatch`** (`supabase/functions/nurture-cron/index.ts`): driver service-role que varre `next_run_at` vencidos e faz fan-out com cap `MAX_PER_RUN` + `CONCURRENCY`, cada linha carregando seu próprio `user_id` confiável.
> 46	
> 47	---
> 48	
> 49	## Topologia (alvo)
> 50	
> 51	```
> 52	pg_cron  ──Bearer SB_SECRET_KEY──▶  autopilot-cadence-cron   (driver service-role)
> 53	  (Vault key)                          │  SELECT plan_id,user_id FROM autopilot_plans
> 54	                                       │  WHERE status='active' AND next_run_at <= now()
> 55	                                       │  (user_id = SERVER-TRUSTED da linha)
> 56	                                       ▼  fan-out (cap MAX_PER_RUN + CONCURRENCY)
> 57	            ──Bearer SB_SECRET_KEY──▶  autopilot-run          (executor por plano)
> 58	            + x-autopilot-user-id        │  ① prova service-role in-function
> 59	                                         │  ② begin_autopilot_cycle (cap + pré-débito atômico, advisory lock)
> 60	                                         │  ③ fan-out sub-runs
> 61	                                         ▼
> 62	            ──Bearer SB_SECRET_KEY──▶  orchestrate-content    (prepaid=true → NÃO self-bill)
> 63	            + x-autopilot-user-id        │  geração product-aware + monetize (Fatia 1)
> 64	                                         ▼
> 65	                                       finalize_autopilot_cycle (refund crédito-positivo idempotente)
> 66	                                         │
> 67	                                         ▼  inline pós-ciclo
> 68	                                       autopilot-analyze       (R3 loop; tenant de previous_cycle_id)
> 69	```
> 70	
> 71	---
> 72	
> 73	## Identity resolution order (canonical — funções `autopilot-*`, `verify_jwt=false`)
> 74	
> 75	| # | Camada | Fonte | Permitido em |
> 76	|---|--------|-------|--------------|
> 77	| 1 | **Service-role gate (caminho cron — PRIMÁRIO aqui)** | `req.headers.get("Authorization") === \`Bearer ${SB_SECRET_KEY}\`` → **403** se não. Padrão literal vivo: `nurture-cron/index.ts` (self-check) + `orchestrate-step/index.ts:110` (`SB_SECRET_KEY ?? SUPABASE_SERVICE_ROLE_KEY`). | `autopilot-cadence-cron`, `autopilot-run` (tick), `autopilot-analyze`, `autopilot-collect` |
> 78	| 2 | **`user_id` server-trusted** | Derivar de uma **linha do banco**: `autopilot_plans.user_id` (cadence-cron) · `autopilot_cycles.user_id` via `previous_cycle_id` (analyze) · `scheduled_posts`/`autopilot_cycles` (collect). O header `x-autopilot-user-id` é só um **espelho** desse valor para logging/propagação — **nunca a fonte de verdade**. | Idem (sempre, após camada 1) |
> 79	| 3 | **User JWT ("gerar agora")** | Caminho user-facing: `getUser()` / JWKS verify (sibling SOP) → **asserir `user.id === plan.user_id`** (IDOR gate). | `autopilot-run` (botão UI) |
> 80	| 4 | **Hard failure** | — | **403** `{ error: "Forbidden" }` (cron) / **401** `{ error: "Token inválido" }` (user). **Fail-closed.** |
> 81	
> 82	**Regra de ouro (herdada de `edge-jwt-identity-verification.md`, estendida):** no caminho cron, confiar num `user_id` exige **(a)** posse provada da `SB_SECRET_KEY` **E** **(b)** o `user_id` ter vindo de uma linha do banco — não do request. As duas condições, sempre, e nessa ordem.
> 83	
> 84	---
> 85	
> 86	## Sequence (o tick → ciclo → finalize)
> 87	
> 88	1. **`pg_cron` dispara `autopilot-cadence-cron`** via pg_net, header `Authorization: Bearer <SB_SECRET_KEY>` (Vault). Sucesso material: linha `infra_health_logs service='autopilot-cadence-cron'`.
> 89	2. **`autopilot-cadence-cron` prova service-role** (camada 1) → 403 se ausente. Varre `autopilot_plans WHERE status='active' AND next_run_at <= now()` (índice parcial, espelha `idx_enroll_due`). Sucesso: lista de `{plan_id, user_id}` (user_id **da linha**).
> 90	3. **Fan-out** para `autopilot-run` (cap `MAX_PER_RUN`, `CONCURRENCY`), cada POST com `Bearer SB_SECRET_KEY` + `x-autopilot-user-id` = `plan.user_id`. **Sem fan-out ilimitado silencioso** (logar se o cap for atingido — padrão `nurture-cron`).
> 91	4. **`autopilot-run` prova service-role** (camada 1) **OU** valida JWT+IDOR (camada 3). Resolve `user_id` server-trusted. Calcula `N_runs` e `projetado = N_runs×10 + ANALYZE_COST(2)`.
> 92	5. **`begin_autopilot_cycle(p_user_id, p_plan_id, p_projected_mco, p_daily_cap_mco, p_budget_cap_mco)`** — RPC `SECURITY DEFINER`, service-role-only, **`pg_advisory_xact_lock(hashtext(user_id::text))`**:
> 93	   - **Cap diário (FR-VA-021):** `SUM(spend_mco)` dos `autopilot_cycles` do tenant no dia (UTC). Se `acumulado + projetado > daily_cap_mco` → `RAISE` `aborted_daily_cap` (**sem deduzir**).
> 94	   - **Cap por plano + saldo (FR-VA-007):** `projetado > budget_cap_mco` → `aborted_budget`; `balance < projetado` → `insufficient_balance`. Ambos `RAISE` **sem deduzir** + pausam o plano.
> 95	   - **OK:** `INSERT autopilot_cycles (state='open', debited_at=now(), spend_mco=projetado)` **+** `deduct_mco_coins(user_id, projetado)` na **mesma transação** → `RETURN cycle_id`. **Um** débito por ciclo. O advisory lock serializa ciclos concorrentes do mesmo tenant → mata o TOCTOU.
> 96	6. **Fan-out dos sub-runs** → `orchestrate-content` com `prepaid=true` + service-role + `x-autopilot-user-id` (FR-VA-016). **`prepaid` ⇒ NÃO chama `deduct_mco_coins`** (já pré-debitado no passo 5). Sucesso: `pipeline_runs` por sub-run; `affiliate_links.content_id` NON-NULL (herdado da Fatia 1).
> 97	7. **`finalize_autopilot_cycle(p_cycle_id, p_actual_mco)`** — RPC `SECURITY DEFINER`, service-role-only, **espelha `finalize_vision_job` (`20260615160000`):**
> 98	   - Claim-once: `UPDATE autopilot_cycles SET state='closed', actual_mco=p_actual, refunded_at=now() WHERE id=p_cycle_id AND state='open' RETURNING user_id`. Se `NULL` → já terminal → **no-op** (sem refund duplo).
> 99	   - `refund = projetado − actual`; se `refund > 0` → **`add_mco_coins(user_id, refund)`** (crédito **positivo** ledgered) na **mesma transação**. **NUNCA `deduct` negativo.**
> 100	8. **`autopilot-analyze` inline** (não cron próprio) — tenant de `previous_cycle_id` (camada 2). 2 mco **só se `has_real_data`** (senão 0, log `analyze_empty`).
> 101	9. **Reagendar:** `next_run_at += interval_days` (catch-up de janela perdida — FR-VA-005). Sucesso: `next_run_at` futuro.
> 102	
> 103	---
> 104	
> 105	## Cost & atomicity contract (resumo executável)
> 106	
> 107	| Invariante | Como é garantido | Âncora |
> 108	|------------|------------------|--------|
> 109	| **Um débito por ciclo** | `begin_autopilot_cycle` faz o `deduct` único; sub-runs `prepaid` | FR-VA-007 · FR-VA-016 |
> 110	| **Cap + débito atômicos (anti-TOCTOU)** | tudo dentro de `begin_autopilot_cycle` sob `pg_advisory_xact_lock` | FR-VA-007 / SEC-VA-04 |
> 111	| **Refund = crédito positivo** | `add_mco_coins(user, refund)`; `deduct_mco_coins` rejeita `p_amount<=0` | `20260603220000:45` |
> 112	| **Refund idempotente (sem duplo)** | claim-once `WHERE state='open' RETURNING user_id` | espelha `finalize_vision_job` |
> 113	| **Abort não cobra** | caps fazem `RAISE` antes do `deduct` | FR-VA-007 / FR-VA-021 |
> 114	| **RPCs blindados** | `REVOKE ... FROM PUBLIC, anon, authenticated; GRANT ... TO service_role` | padrão ledger `20260603220000` |
> 115	| **`user_id` nunca do body** | derivado de `autopilot_plans/_cycles` (linha confiável) | OTD-VA-008 (Decisão B) |
> 116	
> 117	---
> 118	
> 119	## Verification gates
> 120	
> 121	| Gate | Check | Pass criterion |
> 122	|------|-------|----------------|
> 123	| **G1 — Cron identity (exploit, prod)** | `curl -X POST <autopilot-run-url>` com `x-autopilot-user-id: <victim>` **sem** `Bearer SB_SECRET_KEY` (apikey anon) | **403** — nenhum débito, nenhum ciclo criado (sem o gate: processaria como vítima) |
> 124	| **G2 — IDOR no caminho user** | JWT do user A com `plan_id` do user B | **401/403** — `user.id !== plan.user_id` rejeitado |
> 125	| **G3 — Pré-débito atômico (smoke zero-cost)** | `scripts/qa/smoke-autopilot-budget.ts`: `begin_autopilot_cycle` com `projetado > balance` | `insufficient_balance`, `mco_balance` **intacto** (SELECT antes/depois) |
> 126	| **G4 — Cap diário (smoke zero-cost)** | acumular `spend_mco` fictício > `daily_cap`, chamar `begin_*` | `aborted_daily_cap`, **sem deduct** |
> 127	| **G5 — Refund idempotente** | `finalize_autopilot_cycle` chamado **2×** no mesmo `cycle_id` | 1º credita `refund`; 2º `finalized=false` (no-op) — saldo creditado **uma** vez |
> 128	| **G6 — Refund nunca-negativo** | `finalize_*` com `actual > projetado` (refund negativo) | `refund` clampado a 0 (nunca chama `deduct`); CHECK `actual_mco <= spend_mco` no DDL |
> 129	| **G7 — `prepaid` não self-cobra** | sub-run `orchestrate-content` com `prepaid=true` | nenhuma linha `mcoin_transactions` do sub-run; só o débito único do `begin_*` |
> 130	| **G8 — RPC grants** | `\df+ begin_autopilot_cycle finalize_autopilot_cycle` (ou Management API) | EXECUTE **só** `service_role`; revogado de `public/anon/authenticated` |
> 131	| **G9 — `/security-review`** | cada migration nova | **SAFE** (0 findings ≥ High) antes do commit |
> 132	| **G10 — Advisory lock real** | 2 `begin_*` concorrentes do mesmo user (teste de stress) | serializados; soma nunca passa o cap |
> 133	
> 134	G1/G3/G4/G5 são **zero-cost** (usam `dry_run`/usuários descartáveis/RPC isolado) — provam o gate **sem** gastar mcoCoins reais. O 1º ciclo pago real (E2E) é **gated em GO Sovereign** (mesma disciplina das fatias anteriores).
> 135	
> 136	---
> 137	
> 138	## Recovery path
> 139	
> 140	- **Cron dispara mas a fn rejeita (403):** verificar que o `pg_cron` job injeta a Vault key correta no header (`SB_SECRET_KEY`, **não** a legada `SUPABASE_SERVICE_ROLE_KEY` revogada — ver memória `reference_supabase_keys_migrated`). Recriar o job com `Authorization: Bearer <SB_SECRET_KEY>`.
> 141	- **Débito feito mas fan-out falha (crash entre passo 5 e 6):** o ciclo fica `state='open'` com `debited_at` setado e `actual=0`. Um **sweep de reconciliação** (cron diário ou poll, espelha o self-heal de órfão do `deepsearch.poll`) chama `finalize_autopilot_cycle(cycle_id, actual_real)` → credita o não-usado. O claim-once garante idempotência mesmo se o sweep e o caminho normal colidirem.
> 142	- **Refund parece não creditar:** confirmar materialmente via `SELECT mco_balance` antes/depois + a linha `mcoin_transactions action='autopilot_refund'`. NUNCA "tente de novo" cego — `finalize_*` é idempotente, re-chamar é seguro e diagnóstico.
> 143	- **Cap diário travando ciclos legítimos:** ajustar `daily_cap_mco` no plano (config do tenant), nunca remover a checagem. O cap é a feature, não o bug.
> 144	- **Rollback de migration:** as migrations são aditivas (novas tabelas/RPCs). Rollback = `DROP FUNCTION begin_autopilot_cycle / finalize_autopilot_cycle` + `DROP TABLE autopilot_cycles / autopilot_plans` (ordem FK). Confirmar via Management API.
> 145	
> 146	---
> 147	
> 148	## Success signal
> 149	
> 150	- **G1 verde:** `403` literal no exploit test contra produção (cron sem `Bearer` → rejeitado), colado no handoff (Lei 1).
> 151	- **G3/G4 verdes:** smokes zero-cost com `mco_balance` **byte-idêntico** antes/depois de um abort (SELECT real).
> 152	- **G5 verde:** refund creditado **exatamente uma** vez sob dupla-finalização.
> 153	- **G8 verde:** `service_role`-only nos dois RPCs (output literal do `\df+` / Management API).
> 154	- **G9 verde:** `/security-review` SAFE em cada migration.
> 155	- **1º ciclo pago real (gated):** `autopilot_cycles` `state='closed'`, `deduct` = `projetado`, `refund` = `projetado − actual`, `mco_balance` final = inicial − `actual` (delta material exato).
> 156	
> 157	---
> 158	
> 159	## Anti-patterns proibidos
> 160	
> 161	- ❌ Confiar em `x-autopilot-user-id` (ou qualquer `user_id` do body/header) **sem** provar `SB_SECRET_KEY` in-function E sem derivar de linha do banco.
> 162	- ❌ `deduct_mco_coins(user, -refund)` para "estornar" — viola o guard anti-mint (`20260603220000:45`). Refund é **`add_mco_coins` positivo**.
> 163	- ❌ Checar o cap com um `SELECT` e depois `deduct` em chamadas separadas (TOCTOU). Cap + débito vão **juntos** no `begin_autopilot_cycle` sob advisory lock.
> 164	- ❌ Sub-run `orchestrate-content` self-cobrando no caminho cron (duplo débito). `prepaid=true` ⇒ sem `deduct`.
> 165	- ❌ `finalize_*` sem claim-once → refund duplo a cada retry/sweep.
> 166	- ❌ Fan-out ilimitado sem cap por tick (`MAX_PER_RUN`) — drift de custo silencioso.
> 167	- ❌ `GRANT EXECUTE` dos RPCs de ciclo a `authenticated`/`anon` (qualquer um cunharia/estornaria). **Service-role-only.**
> 168	- ❌ `verify_jwt=true` no gateway para as `autopilot-*` (quebraria o caminho cron **e** o user ES256).
> 169	- ❌ Setar `daily_cap`/`budget_cap` como opcional/ausente — o cron **não** roda sem teto (kill-switch obrigatório, FMEA-VA-001 RPN 128).
> 170	
> 171	---
> 172	
> 173	## Sibling reference
> 174	
> 175	- **Camada-3 service-role gate (base):** `docs/processes/edge-jwt-identity-verification.md` + `supabase/functions/nurture-cron/index.ts` (precedente vivo idêntico de cron→dispatch).
> 176	- **`verify_jwt=false` + pg_net + param-name contract:** `docs/processes/orchestrate-async-pipeline.md`.
> 177	- **Anti-mint ledger RPCs:** `supabase/migrations/20260603220000_secure_ledger_rpcs.sql` (`deduct_mco_coins` sign+own-tenant guards; `award_mco_coins`/`add_user_score` edge-only).
> 178	- **Atomic terminal+refund (molde):** `supabase/migrations/20260615160000_vision_mcp_jobs.sql` (`finalize_vision_job` claim-once + `add_mco_coins` positivo).
> 179	- **Sealed contract:** `docs/bok/viral-autopilot/04-frd.md` (FR-VA-002/007/008/010/016/021) · `05-sdd.md:425-427` (OTD-VA-008 + nota do gate Lei 2).
> 180	
> ```

## 🤖 Claude *(03:39:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la supabase/functions/ | grep -i autopilot; echo \"---migrations autopilot---\"; ls -la supabase/migrations/ | grep -iE \"autopilot|2026062012\"",
  "description": "List autopilot functions and migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun 20 16:32 autopilot-analyze
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun 20 15:58 autopilot-cadence-cron
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun 20 16:26 autopilot-collect
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun 20 16:27 autopilot-run
> ---migrations autopilot---
> -rw-rw-r-- 1 ubuntu ubuntu  5318 Jun 19 23:47 20260619140000_viral_autopilot_creative_metrics.sql
> -rw-rw-r-- 1 ubuntu ubuntu  4564 Jun 20 14:50 20260620120000_viral_autopilot_plans.sql
> -rw-rw-r-- 1 ubuntu ubuntu  4494 Jun 20 14:51 20260620120100_viral_autopilot_cycles.sql
> -rw-rw-r-- 1 ubuntu ubuntu  6107 Jun 20 14:51 20260620120200_begin_autopilot_cycle.sql
> -rw-rw-r-- 1 ubuntu ubuntu  3323 Jun 20 14:51 20260620120300_finalize_autopilot_cycle.sql
> ```

## 🤖 Claude *(03:39:39)*


## 🤖 Claude *(03:39:42)*

O SOP é completo e o gate está claro: a topologia `pg_cron → autopilot-cadence-cron → autopilot-run → orchestrate-content → finalize` está toda implementada e provada zero-cost. Falta só **(1)** o JOB `pg_cron` (ação Sovereign-side) e **(2)** o GO para o 1º ciclo PAGO.

Vou ler a função driver para extrair o contrato exato (URL + header) e rodar os pré-checks materiais.

## 🤖 Claude *(03:39:44)*


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

## 🤖 Claude *(03:39:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nA3 -E \"autopilot-(cadence-cron|run|analyze|collect)\" supabase/config.toml 2>/dev/null | head -40; echo \"---SB keys present?---\"; grep -cE \"^SB_SECRET_KEY=|^SB_PUBLISHABLE_KEY=|^VITE_SUPABASE_URL=\" .env 2>/dev/null && echo \"keys in .env\"",
  "description": "Check verify_jwt config + .env keys"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 24:[functions.autopilot-run]
> 25-verify_jwt = false
> 26:[functions.autopilot-cadence-cron]
> 27-verify_jwt = false
> 28:[functions.autopilot-analyze]
> 29-verify_jwt = false
> 30:[functions.autopilot-collect]
> 31-verify_jwt = false
> 32-[functions.video-render]
> 33-verify_jwt = false
> ---SB keys present?---
> 2
> keys in .env
> ```

## 🤖 Claude *(03:39:58)*


## 🤖 Claude *(03:39:59)*

Driver confirmado: service-role gate limpo, `user_id` server-trusted da linha do plano, `verify_jwt=false` em todas as `autopilot-*`. Agora os pré-checks materiais. Vou ler o schema dos planos/ciclos e sondar produção em paralelo.

## 🤖 Claude *(03:40:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: viral-autopilot autopilot_plans — per-user cadence config (FR-VA-001 / FR-VA-005).
> 2	-- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md §2 (autopilot_plans) + 05-sdd.md §7.
> 3	-- SOP (Lei 2 — written BEFORE this code): docs/processes/autopilot-cron-identity.md.
> 4	--
> 5	-- The "what & when" source of truth for the autonomous viral loop: which products, which networks, how often,
> 6	-- and the MANDATORY safety caps (budget_cap_mco per cycle, daily_cap_mco per tenant, min_balance_mco floor).
> 7	-- Caps are NOT NULL by design — the cron NEVER runs without a kill-switch (FMEA-VA-001 RPN 128 / BR-RISK-001).
> 8	--
> 9	-- Tenancy: RLS user_id = auth.uid() (own CRUD); RESTRICTIVE no-delete for authenticated (only service-role
> 10	-- removes, e.g. LGPD cascade). UNIQUE(id,user_id) is the target of the tenant-scoped composite FK from
> 11	-- autopilot_cycles (next migration). Passes /security-review (FMEA-011 / FMEA-VA-001 cross-tenant family).
> 12	--
> 13	-- Engineering notes (deviations from sealed stub, declared per Lei 1):
> 14	--   * CHECKs added beyond the data-model stub (mode enum, interval 1-30, platforms subset, caps >= 12 = 1-cycle
> 15	--     floor [1 run 10 + analyze 2], ab_variants 1-5) materialize the §6 Data Quality rules at the DB layer.
> 16	--   * project_id has NO FK (matches data-model §2 "FK —"); kept as a plain scoping uuid.
> 17	
> 18	CREATE TABLE IF NOT EXISTS public.autopilot_plans (
> 19	  id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
> 20	  user_id            uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 21	  project_id         uuid,
> 22	  name               text        NOT NULL,
> 23	  mode               text        NOT NULL CHECK (mode IN ('all_at_once','every_n_days')),
> 24	  interval_days      int         DEFAULT 3 CHECK (interval_days IS NULL OR (interval_days BETWEEN 1 AND 30)),
> 25	  target_product_ids text[]      NOT NULL CHECK (array_length(target_product_ids, 1) >= 1),
> 26	  platforms          text[]      NOT NULL CHECK (array_length(platforms, 1) >= 1
> 27	                                   AND platforms <@ ARRAY['wordpress','linkedin','twitter']),
> 28	  budget_cap_mco     int         NOT NULL CHECK (budget_cap_mco  >= 12),  -- >= 1 cycle (1 run 10 + analyze 2)
> 29	  daily_cap_mco      int         NOT NULL DEFAULT 200 CHECK (daily_cap_mco >= 12),
> 30	  min_balance_mco    int         NOT NULL DEFAULT 10  CHECK (min_balance_mco >= 0),
> 31	  hitl_required      boolean     NOT NULL DEFAULT false,
> 32	  ab_variants        int         NOT NULL DEFAULT 1   CHECK (ab_variants BETWEEN 1 AND 5),
> 33	  is_active          boolean     NOT NULL DEFAULT false,
> 34	  next_run_at        timestamptz,
> 35	  created_at         timestamptz NOT NULL DEFAULT now(),
> 36	  updated_at         timestamptz NOT NULL DEFAULT now(),
> 37	  -- mode every_n_days REQUIRES interval_days (Data Quality §6).
> 38	  CONSTRAINT autopilot_plans_interval_req CHECK (mode <> 'every_n_days' OR interval_days IS NOT NULL),
> 39	  -- anchor for the tenant-scoped composite FK from autopilot_cycles (id,user_id).
> 40	  CONSTRAINT autopilot_plans_id_user_uniq UNIQUE (id, user_id)
> 41	);
> 42	
> 43	ALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;
> 44	
> 45	CREATE POLICY "autopilot_plans_select_own" ON public.autopilot_plans
> 46	  FOR SELECT USING (auth.uid() = user_id);
> 47	CREATE POLICY "autopilot_plans_insert_own" ON public.autopilot_plans
> 48	  FOR INSERT WITH CHECK (auth.uid() = user_id);
> 49	CREATE POLICY "autopilot_plans_update_own" ON public.autopilot_plans
> 50	  FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 51	-- Clients can NEVER delete a plan (RESTRICTIVE forbids it even if a permissive policy is later added);
> 52	-- only service-role (LGPD cascade) removes.
> 53	CREATE POLICY "autopilot_plans_no_client_delete" ON public.autopilot_plans
> 54	  AS RESTRICTIVE FOR DELETE USING (false);
> 55	
> 56	-- Due-plan scan index (cron): active plans whose next_run_at has passed.
> 57	CREATE INDEX IF NOT EXISTS autopilot_plans_due_idx  ON public.autopilot_plans (next_run_at) WHERE is_active;
> 58	CREATE INDEX IF NOT EXISTS autopilot_plans_user_idx ON public.autopilot_plans (user_id, created_at DESC);
> 59	
> 60	CREATE TRIGGER set_autopilot_plans_updated_at
> 61	  BEFORE UPDATE ON public.autopilot_plans
> 62	  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 63	
> 64	COMMENT ON TABLE public.autopilot_plans IS
> 65	  'Viral Autopilot cadence config per user (FR-VA-001/005). Mandatory safety caps (budget/daily/min_balance) — '
> 66	  'the cron never runs without a kill-switch. SELECT/INSERT/UPDATE own, RESTRICTIVE no client delete. '
> 67	  'UNIQUE(id,user_id) anchors the tenant-scoped composite FK from autopilot_cycles. SOP autopilot-cron-identity.md.';
> 68	
> ```

## 🤖 Claude *(03:40:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"\nBASE=\"https://${REF}.supabase.co\"\necho \"=== G1-style boot-smoke: autopilot-cadence-cron sem Bearer service (espera 403) ===\"\ncurl -s -o /tmp/cc.txt -w \"HTTP %{http_code}\\n\" -X POST \"$BASE/functions/v1/autopilot-cadence-cron\" \\\n  -H \"apikey: $SB_PUBLISHABLE_KEY\" -H \"Content-Type: application/json\" -d '{}'\necho \"body: $(cat /tmp/cc.txt)\"\necho \"\"\necho \"=== autopilot_plans existe? (REST count) ===\"\ncurl -s -o /dev/null -w \"HTTP %{http_code}\\n\" \"$BASE/rest/v1/autopilot_plans?select=id&limit=1\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"\necho \"\"\necho \"=== planos do User 0 (Gabriel) ===\"\ncurl -s \"$BASE/rest/v1/autopilot_plans?select=id,user_id,is_active,next_run_at,interval_days,daily_cap_mco,budget_cap_mco,networks,product_ids,ab_variants\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -m json.tool 2>/dev/null || cat /tmp/plans.txt",
  "description": "Boot-smoke + plans table + User 0 plan rows"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === G1-style boot-smoke: autopilot-cadence-cron sem Bearer service (espera 403) ===
> HTTP 403
> body: {"error":"Forbidden"}
> 
> === autopilot_plans existe? (REST count) ===
> HTTP 200
> 
> === planos do User 0 (Gabriel) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column autopilot_plans.networks does not exist"
> }
> ```

## 🤖 Claude *(03:40:16)*


## 🤖 Claude *(03:40:18)*

Coluna chutada errada — o schema real é `target_product_ids`/`platforms`. O boot-smoke já provou material: **cadence-cron deployada + gate service-role retorna 403** (G1-style ✅). Re-consultando com as colunas corretas + saldo + ciclos.

## 🤖 Claude *(03:40:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== Planos Autopilot (todos os tenants) ===\"\ncurl -s \"$BASE/rest/v1/autopilot_plans?select=id,user_id,name,mode,interval_days,target_product_ids,platforms,budget_cap_mco,daily_cap_mco,min_balance_mco,ab_variants,is_active,next_run_at\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Ciclos j\u00e1 existentes ===\"\ncurl -s \"$BASE/rest/v1/autopilot_cycles?select=id,user_id,plan_id,state,spend_mco,actual_mco,created_at&order=created_at.desc&limit=5\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Saldo do User 0 (profiles) ===\"\ncurl -s \"$BASE/rest/v1/profiles?select=id,mco_balance,plan&order=mco_balance.desc&limit=5\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null",
  "description": "Plans + cycles + balances material check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Planos Autopilot (todos os tenants) ===
> []
> 
> === Ciclos já existentes ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": "Perhaps you meant to reference the column \"autopilot_cycles.status\".",
>     "message": "column autopilot_cycles.state does not exist"
> }
> 
> === Saldo do User 0 (profiles) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column profiles.plan does not exist"
> }
> ```

## 🤖 Claude *(03:40:45)*


## 🤖 Claude *(03:40:48)*

Achado material decisivo: **`autopilot_plans` está VAZIA** (`[]`) — o User 0 ainda não tem plano. O cron varre planos ativos vencidos; sem plano, nenhum tick faz nada. Isso reposiciona a ativação: o 1º ciclo exige **(a)** um plano do User 0 + **(b)** o JOB pg_cron (ou disparo manual) + **(c)** GO de gasto.

Corrigindo as queries e levantando o padrão canônico de pg_cron já usado no projeto (para extrair o nome do segredo no Vault).

## 🤖 Claude *(03:40:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== Ciclos (status) ===\"\ncurl -s \"$BASE/rest/v1/autopilot_cycles?select=id,user_id,plan_id,status,spend_mco,actual_mco,created_at&order=created_at.desc&limit=5\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Saldos (top 5) ===\"\ncurl -s \"$BASE/rest/v1/profiles?select=id,mco_balance&order=mco_balance.desc&limit=5\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Padr\u00e3o pg_cron/net.http_post existente nas migrations (nome do segredo Vault) ===\"\ngrep -rliE \"cron\\.schedule|net\\.http_post|vault\\.decrypted_secrets\" supabase/migrations/ 2>/dev/null | head",
  "description": "Cycles + balances + existing cron patterns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Ciclos (status) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column autopilot_cycles.actual_mco does not exist"
> }
> 
> === Saldos (top 5) ===
> [
>     {
>         "id": "ada39fae-67e1-4e53-af1c-5a18e1c108e8",
>         "mco_balance": 5096.0
>     },
>     {
>         "id": "273917a6-2f88-4611-99f3-b90016dd0ddd",
>         "mco_balance": 0.0
>     },
>     {
>         "id": "4631327b-df6b-4d89-8d3e-382163e74e43",
>         "mco_balance": 0.0
>     },
>     {
>         "id": "a836886a-bfe1-44f0-96b6-9a8c1eb6bd99",
>         "mco_balance": 0.0
>     },
>     {
>         "id": "dc4263c7-22dd-4001-a5cb-2381624c0e14",
>         "mco_balance": 0.0
>     }
> ]
> 
> === Padrão pg_cron/net.http_post existente nas migrations (nome do segredo Vault) ===
> supabase/migrations/20260503120000_embed_on_insert_trigger.sql
> supabase/migrations/20260527012500_async_orchestrate_step_debug.sql
> supabase/migrations/20260622210000_user_api_keys_rapidapi_channel.sql
> supabase/migrations/20260601000000_credential_encryption.sql
> supabase/migrations/20260526202000_async_orchestrate_step.sql
> supabase/migrations/20260423205725_knowledge_mesh_init.sql
> supabase/migrations/20260601050000_embed_trigger_vault_key.sql
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql
> supabase/migrations/20260603190000_fix_async_orchestrate_step_param_drift.sql
> supabase/migrations/20260603240000_user_api_keys_resend_channel.sql
> ```

## 🤖 Claude *(03:40:59)*


## 🤖 Claude *(03:41:01)*

User 0 = `ada39fae…`, saldo **5096 mcoCoins** (intacto). Lendo o schema dos ciclos, as assinaturas dos RPCs e o padrão canônico de Vault-key do projeto para escrever o pg_cron e o runbook com precisão.

## 🤖 Claude *(03:41:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120100_viral_autopilot_cycles.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: viral-autopilot autopilot_cycles — per-cycle execution ledger (FR-VA-006 / FR-VA-007).
> 2	-- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md §2 (autopilot_cycles) + 05-sdd.md §7.
> 3	-- SOP (Lei 2): docs/processes/autopilot-cron-identity.md.
> 4	--
> 5	-- One row per cadence cycle: the FINANCIAL ledger of a run (status, spend_mco pre-debited, refunded_mco credited
> 6	-- on finalize, planned_units, debited_at/refunded_at idempotency stamps). Idempotent by (plan_id, cycle_number).
> 7	-- The pre-debit/refund LOGIC lives in begin_/finalize_autopilot_cycle (next 2 migrations) — this is the schema.
> 8	--
> 9	-- Tenancy: user_id is a REAL FK to auth.users AND part of the tenant-scoped COMPOSITE FK
> 10	-- (plan_id,user_id) -> autopilot_plans(id,user_id) — a cycle can never point at another tenant's plan (mirrors
> 11	-- Marketing Hub campaign_steps composite FK). SELECT-own RLS; INSERT/UPDATE have NO permissive policy →
> 12	-- authenticated default-deny (only the service-role runner/RPCs write). Financial table → RESTRICTIVE no-delete.
> 13	-- UNIQUE(id,user_id) anchors the composite FK from creative_metrics (closed at the end of this file).
> 14	
> 15	CREATE TABLE IF NOT EXISTS public.autopilot_cycles (
> 16	  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
> 17	  user_id          uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 18	  plan_id          uuid        NOT NULL,
> 19	  cycle_number     int         NOT NULL,
> 20	  status           text        NOT NULL DEFAULT 'running'
> 21	                     CHECK (status IN ('running','completed','aborted_budget','aborted_daily_cap','failed')),
> 22	  spend_mco        int         NOT NULL DEFAULT 0 CHECK (spend_mco     >= 0),
> 23	  refunded_mco     int         NOT NULL DEFAULT 0 CHECK (refunded_mco  >= 0),
> 24	  planned_units    int         NOT NULL DEFAULT 0 CHECK (planned_units >= 0),
> 25	  analysis_node_id uuid,
> 26	  debited_at       timestamptz,
> 27	  refunded_at      timestamptz,
> 28	  started_at       timestamptz NOT NULL DEFAULT now(),
> 29	  completed_at     timestamptz,
> 30	  -- refund can NEVER exceed what was committed (defense-in-depth vs a negative-refund mint).
> 31	  CONSTRAINT autopilot_cycles_refund_le_spend CHECK (refunded_mco <= spend_mco),
> 32	  CONSTRAINT autopilot_cycles_plan_cycle_uniq UNIQUE (plan_id, cycle_number),
> 33	  CONSTRAINT autopilot_cycles_id_user_uniq    UNIQUE (id, user_id),
> 34	  -- tenant-scoped composite FK: the cycle's (plan_id,user_id) must match a plan owned by the SAME tenant.
> 35	  CONSTRAINT autopilot_cycles_plan_fk FOREIGN KEY (plan_id, user_id)
> 36	    REFERENCES public.autopilot_plans (id, user_id) ON DELETE CASCADE
> 37	);
> 38	
> 39	ALTER TABLE public.autopilot_cycles ENABLE ROW LEVEL SECURITY;
> 40	
> 41	-- SELECT own only; INSERT/UPDATE default-deny (the service-role RPCs write). Financial → RESTRICTIVE no-delete.
> 42	CREATE POLICY "autopilot_cycles_select_own" ON public.autopilot_cycles
> 43	  FOR SELECT USING (auth.uid() = user_id);
> 44	CREATE POLICY "autopilot_cycles_no_client_delete" ON public.autopilot_cycles
> 45	  AS RESTRICTIVE FOR DELETE USING (false);
> 46	
> 47	CREATE INDEX IF NOT EXISTS autopilot_cycles_plan_idx     ON public.autopilot_cycles (plan_id, cycle_number DESC);
> 48	CREATE INDEX IF NOT EXISTS autopilot_cycles_user_day_idx ON public.autopilot_cycles (user_id, started_at);
> 49	
> 50	COMMENT ON TABLE public.autopilot_cycles IS
> 51	  'Viral Autopilot per-cycle financial ledger (FR-VA-006/007). spend_mco pre-debited by begin_autopilot_cycle, '
> 52	  'refunded_mco credited by finalize_autopilot_cycle (idempotent). Tenant-scoped composite FK to autopilot_plans. '
> 53	  'SELECT-own, service-role write (default-deny), RESTRICTIVE no client delete. SOP autopilot-cron-identity.md.';
> 54	
> 55	-- ── Close the deferred composite FK from creative_metrics (Fatia 1 left cycle_id NULL-able, NO FK) ──────────────
> 56	-- Now that autopilot_cycles exists, wire the tenant-scoped composite FK (cycle_id,user_id) -> cycles(id,user_id).
> 57	-- MATCH SIMPLE (default): rows with cycle_id NULL (Fatia 1 baseline rows) stay valid (FK skipped when any col NULL).
> 58	-- ON DELETE CASCADE: erasing a cycle erases its metrics (Data Model §7 retention). Idempotent guard so a re-run
> 59	-- of this migration does not error on the already-present constraint.
> 60	DO $$
> 61	BEGIN
> 62	  IF NOT EXISTS (
> 63	    SELECT 1 FROM pg_constraint WHERE conname = 'creative_metrics_cycle_fk'
> 64	  ) THEN
> 65	    ALTER TABLE public.creative_metrics
> 66	      ADD CONSTRAINT creative_metrics_cycle_fk FOREIGN KEY (cycle_id, user_id)
> 67	        REFERENCES public.autopilot_cycles (id, user_id) ON DELETE CASCADE;
> 68	  END IF;
> 69	END $$;
> 70	
> ```

## 🤖 Claude *(03:41:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120200_begin_autopilot_cycle.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: begin_autopilot_cycle RPC — atomic cap-check + single pre-debit + open cycle (FR-VA-007 / FR-VA-021).
> 2	-- BoK SSOT: docs/bok/viral-autopilot/05-sdd.md §2 (RPC table line 109 + cost-gate notes lines ~170-183).
> 3	-- SOP (Lei 2): docs/processes/autopilot-cron-identity.md.
> 4	--
> 5	-- THE anti-TOCTOU heart of the cost guardrail. Under pg_advisory_xact_lock(hashtext(user_id)) — which serializes
> 6	-- concurrent begins for the SAME tenant so two parallel cycles cannot both slip under the daily cap — it:
> 7	--   1. loads the plan's caps TENANT-SCOPED (plan must belong to p_user_id — cross-tenant attempt → not found),
> 8	--   2. checks budget cap (per cycle), balance + min_balance floor, daily cap (sum of today's committed spend),
> 9	--   3. on ANY breach → RETURNS an abort reason WITHOUT debiting (caller pauses plan / returns 409/402),
> 10	--   4. on OK → INSERTs the cycle (status running, spend_mco=projected, debited_at) and PERFORMs the SINGLE
> 11	--      deduct_mco_coins(projected) in the SAME transaction (sub-runs are prepaid → never self-bill).
> 12	-- Refund is NEVER here — it is the positive credit in finalize_autopilot_cycle. deduct_mco_coins rejects
> 13	-- p_amount<=0 (anti-mint, 20260603220000:45), so there is no negative-deduct path anywhere.
> 14	--
> 15	-- Identity (OTD-VA-008): service-role-only (REVOKE authenticated/anon). The caller (autopilot-run) has already
> 16	-- proven service-role in-function and resolved p_user_id from the SERVER-TRUSTED plan row, never the request body.
> 17	--
> 18	-- Engineering notes (declared per Lei 1): the sealed stub hints (uuid,uuid,int); a 4th p_planned_units (DEFAULT 0)
> 19	-- is added — backward-compatible with a 3-arg call — so the cycle row records N_runs without a follow-up UPDATE.
> 20	-- Aborts are NOT persisted as cycle rows (the status enum has no 'insufficient_balance'); the caller logs the
> 21	-- abort to infra_health_logs (telemetry) — every FR requirement ("aborta sem deduzir", pause plan, 409/402) holds.
> 22	
> 23	CREATE OR REPLACE FUNCTION public.begin_autopilot_cycle(
> 24	  p_plan_id       uuid,
> 25	  p_user_id       uuid,
> 26	  p_projected_mco int,
> 27	  p_planned_units int DEFAULT 0
> 28	)
> 29	RETURNS jsonb
> 30	LANGUAGE plpgsql
> 31	SECURITY DEFINER
> 32	SET search_path = ''
> 33	AS $$
> 34	DECLARE
> 35	  v_budget_cap   int;
> 36	  v_daily_cap    int;
> 37	  v_min_balance  int;
> 38	  v_balance      int;
> 39	  v_daily_spent  int;
> 40	  v_cycle_number int;
> 41	  v_cycle_id     uuid;
> 42	BEGIN
> 43	  IF p_projected_mco IS NULL OR p_projected_mco <= 0 THEN
> 44	    RAISE EXCEPTION 'begin_autopilot_cycle: projected must be positive, got %', p_projected_mco
> 45	      USING errcode = '22023';
> 46	  END IF;
> 47	
> 48	  -- Serialize concurrent cycles for THIS tenant (anti-TOCTOU on the daily-cap aggregate). Transaction-scoped.
> 49	  PERFORM pg_advisory_xact_lock(hashtext(p_user_id::text));
> 50	
> 51	  -- Tenant-scoped plan load: the plan MUST belong to p_user_id (cross-tenant attempt → not found → abort).
> 52	  SELECT budget_cap_mco, daily_cap_mco, min_balance_mco
> 53	    INTO v_budget_cap, v_daily_cap, v_min_balance
> 54	    FROM public.autopilot_plans
> 55	   WHERE id = p_plan_id AND user_id = p_user_id;
> 56	  IF NOT FOUND THEN
> 57	    RAISE EXCEPTION 'begin_autopilot_cycle: plan % not found for tenant', p_plan_id USING errcode = 'P0002';
> 58	  END IF;
> 59	
> 60	  -- Budget cap (per cycle) — FR-VA-007 (no deduct).
> 61	  IF p_projected_mco > v_budget_cap THEN
> 62	    RETURN jsonb_build_object('ok', false, 'reason', 'aborted_budget',
> 63	                              'projected', p_projected_mco, 'budget_cap', v_budget_cap);
> 64	  END IF;
> 65	
> 66	  -- Balance + min-balance floor — FR-VA-007 (no deduct).
> 67	  SELECT mco_balance INTO v_balance FROM public.profiles WHERE id = p_user_id;
> 68	  IF v_balance IS NULL THEN
> 69	    RAISE EXCEPTION 'begin_autopilot_cycle: profile not found for tenant' USING errcode = 'P0002';
> 70	  END IF;
> 71	  IF v_balance < p_projected_mco OR v_balance < v_min_balance THEN
> 72	    RETURN jsonb_build_object('ok', false, 'reason', 'insufficient_balance',
> 73	                              'projected', p_projected_mco, 'balance', v_balance, 'min_balance', v_min_balance);
> 74	  END IF;
> 75	
> 76	  -- Daily cap (per tenant, UTC day) — FR-VA-021. Sum COMMITTED spend of today's non-aborted cycles.
> 77	  SELECT COALESCE(SUM(spend_mco), 0) INTO v_daily_spent
> 78	    FROM public.autopilot_cycles
> 79	   WHERE user_id = p_user_id
> 80	     AND (started_at AT TIME ZONE 'UTC')::date = (now() AT TIME ZONE 'UTC')::date
> 81	     AND status NOT IN ('aborted_budget','aborted_daily_cap');
> 82	  IF v_daily_spent + p_projected_mco > v_daily_cap THEN
> 83	    RETURN jsonb_build_object('ok', false, 'reason', 'aborted_daily_cap',
> 84	                              'projected', p_projected_mco, 'daily_spent', v_daily_spent, 'daily_cap', v_daily_cap);
> 85	  END IF;
> 86	
> 87	  -- All caps passed → open the cycle and pre-debit atomically (advisory lock still held → serialized).
> 88	  SELECT COALESCE(MAX(cycle_number), 0) + 1 INTO v_cycle_number
> 89	    FROM public.autopilot_cycles WHERE plan_id = p_plan_id;
> 90	
> 91	  INSERT INTO public.autopilot_cycles (user_id, plan_id, cycle_number, status, spend_mco, planned_units, debited_at)
> 92	  VALUES (p_user_id, p_plan_id, v_cycle_number, 'running', p_projected_mco, GREATEST(p_planned_units, 0), now())
> 93	  RETURNING id INTO v_cycle_id;
> 94	
> 95	  -- SINGLE pre-debit. service-role caller → deduct's service_role exemption applies. If a concurrent non-autopilot
> 96	  -- spend dropped the balance below projected, deduct RAISEs (mco_balance >= amount under FOR UPDATE) and the whole
> 97	  -- transaction rolls back (the INSERT is undone) — atomic, no orphan debited cycle.
> 98	  PERFORM public.deduct_mco_coins(p_user_id, p_projected_mco::numeric, 'autopilot_cycle',
> 99	            jsonb_build_object('plan_id', p_plan_id, 'cycle_id', v_cycle_id, 'cycle_number', v_cycle_number));
> 100	
> 101	  RETURN jsonb_build_object('ok', true, 'cycle_id', v_cycle_id, 'cycle_number', v_cycle_number,
> 102	                            'projected', p_projected_mco);
> 103	END;
> 104	$$;
> 105	
> 106	-- Service-role-only: only the autopilot runner (which proved service-role in-function) may open a paid cycle.
> 107	REVOKE ALL ON FUNCTION public.begin_autopilot_cycle(uuid, uuid, int, int) FROM PUBLIC, anon, authenticated;
> 108	GRANT EXECUTE ON FUNCTION public.begin_autopilot_cycle(uuid, uuid, int, int) TO service_role;
> 109	
> ```

## 🤖 Claude *(03:41:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601050000_embed_trigger_vault_key.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- key-migration 2026-06-01: embed-on-insert trigger reads the service key from Supabase Vault.
> 2	-- Context: the original trigger (migration 20260503120000) baked the legacy service_role JWT into
> 3	-- the function body in plaintext — that key leaked publicly. Triggers run in Postgres (not the Edge
> 4	-- runtime) so they can't read Function secrets; the supported way to hold a credential is Vault.
> 5	-- This re-creates mcorch_embed_on_insert() to pull the active secret key from Vault and call
> 6	-- embed-mcorch-node (now verify_jwt=false + in-code isServiceRole gate) via the apikey header.
> 7	--
> 8	-- PREREQ (Sovereign, run ONCE before relying on this — replace with the real sb_secret_ value):
> 9	--   select vault.create_secret('sb_secret_REPLACE_ME', 'sb_secret_key', 'Internal pg_net service key');
> 10	-- To rotate later:
> 11	--   select vault.update_secret((select id from vault.secrets where name='sb_secret_key'), 'sb_secret_NEW');
> 12	--
> 13	-- Passes /security-review before commit (FMEA-011). No plaintext credential in this file.
> 14	
> 15	CREATE OR REPLACE FUNCTION public.mcorch_embed_on_insert()
> 16	RETURNS TRIGGER
> 17	LANGUAGE plpgsql
> 18	SECURITY DEFINER
> 19	SET search_path = public
> 20	AS $$
> 21	DECLARE
> 22	  v_key text;
> 23	BEGIN
> 24	  IF NEW.embedding IS NOT NULL THEN
> 25	    RETURN NEW;
> 26	  END IF;
> 27	
> 28	  SELECT decrypted_secret INTO v_key
> 29	  FROM vault.decrypted_secrets
> 30	  WHERE name = 'sb_secret_key'
> 31	  LIMIT 1;
> 32	
> 33	  -- No key configured yet → skip silently (never block the INSERT). Fire-and-forget.
> 34	  IF v_key IS NULL THEN
> 35	    RAISE WARNING '[mcorch] embed_on_insert: vault secret sb_secret_key missing — skipped for %', NEW.id;
> 36	    RETURN NEW;
> 37	  END IF;
> 38	
> 39	  PERFORM net.http_post(
> 40	    url     := 'https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/embed-mcorch-node',
> 41	    headers := jsonb_build_object(
> 42	      'Content-Type',  'application/json',
> 43	      'apikey',        v_key,
> 44	      'Authorization', 'Bearer ' || v_key
> 45	    ),
> 46	    body    := jsonb_build_object('node_id', NEW.id::text)
> 47	  );
> 48	
> 49	  RETURN NEW;
> 50	EXCEPTION WHEN OTHERS THEN
> 51	  RAISE WARNING '[mcorch] embed_on_insert skipped for %: %', NEW.id, SQLERRM;
> 52	  RETURN NEW;
> 53	END;
> 54	$$;
> 55	
> 56	COMMENT ON FUNCTION public.mcorch_embed_on_insert() IS
> 57	  'Auto-embeds new mcorch_nodes via embed-mcorch-node. Service key from Vault (sb_secret_key). Fire-and-forget.';
> 58	
> ```

## 🤖 Claude *(03:41:43)*


## 🤖 Claude *(03:41:45)*

Agora tenho o contrato completo. Pré-checks materiais consolidados. Faltam dois dados para montar um runbook pronto-para-disparar: **(a)** se o `pg_cron` está habilitado (os crons existentes do projeto são OS crontab, não pg_cron) e **(b)** quais produtos o User 0 tem para alimentar um plano. Vou ler o executor `autopilot-run` e sondar isso.

## 🤖 Claude *(03:41:46)*


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
> 13	
> 14	const corsHeaders = {
> 15	  "Access-Control-Allow-Origin": "*",
> 16	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 17	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-autopilot-user-id",
> 18	};
> 19	const ORCH_COST = 10;     // orchestrate-content flat bundle (image already included — billing.ts:16-21)
> 20	const ANALYZE_COST = 2;   // reserved for autopilot-analyze (R3); REFUNDED until that slice lands (see actual below)
> 21	const CONCURRENCY = 6;    // wall-clock bound on the fan-out (mirrors nurture-cron / campaign-run)
> 22	const UUID_RE = /^[0-9a-fA-F-]{36}$/;
> 23	
> 24	Deno.serve(async (req) => {
> 25	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 26	  const json = (b: unknown, s = 200) =>
> 27	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 28	
> 29	  const url = Deno.env.get("SUPABASE_URL")!;
> 30	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 31	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 32	  const admin = createClient(url, serviceKey);
> 33	  const logHealth = (status: string) =>
> 34	    admin.from("infra_health_logs").insert({ service: "autopilot-run", status }).then(() => {}, () => {});
> 35	
> 36	  try {
> 37	    const authHeader = req.headers.get("Authorization");
> 38	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 39	
> 40	    const body = await req.json().catch(() => ({}));
> 41	    const planId = typeof body?.plan_id === "string" ? body.plan_id : null;
> 42	    const dryRun = body?.dry_run === true;
> 43	    if (!planId || !UUID_RE.test(planId)) return json({ error: "plan_id (uuid) required" }, 422);
> 44	
> 45	    // ── Identity: service path (proven key + server-trusted header) OR user JWT path. ──────────────────────────
> 46	    const isService = authHeader === `Bearer ${serviceKey}`;
> 47	    let userId: string;
> 48	    if (isService) {
> 49	      const hdr = req.headers.get("x-autopilot-user-id");
> 50	      if (!hdr || !UUID_RE.test(hdr)) return json({ error: "x-autopilot-user-id (uuid) required for service path" }, 400);
> 51	      userId = hdr;
> 52	    } else {
> 53	      const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 54	      const { data: { user }, error } = await userClient.auth.getUser();
> 55	      if (error || !user) return json({ error: "Unauthorized" }, 401);
> 56	      userId = user.id;
> 57	    }
> 58	
> 59	    // ── Load plan TENANT-SCOPED (plan MUST belong to userId — cross-tenant/missing → 404). ───────────────────────
> 60	    const { data: plan } = await admin
> 61	      .from("autopilot_plans")
> 62	      .select("id, user_id, name, mode, interval_days, target_product_ids, platforms, ab_variants")
> 63	      .eq("id", planId).eq("user_id", userId).maybeSingle();
> 64	    if (!plan) return json({ error: "plan_not_found" }, 404);
> 65	
> 66	    const products = ((plan.target_product_ids ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 67	    const platforms = ((plan.platforms ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 68	    const abVariants = Math.max(1, Math.min(5, Number(plan.ab_variants ?? 1)));
> 69	    const nRuns = products.length * platforms.length * abVariants;
> 70	    if (nRuns < 1) return json({ error: "plan_has_no_targets", detail: "plano sem produtos/redes válidos" }, 422);
> 71	
> 72	    const projected = nRuns * ORCH_COST + ANALYZE_COST;
> 73	
> 74	    // dry_run: return the cost projection WITHOUT opening a cycle or deducting (zero-cost proof path).
> 75	    if (dryRun) {
> 76	      return json({ ok: true, dry_run: true, n_runs: nRuns, projected_mco: projected,
> 77	        breakdown: { products: products.length, platforms: platforms.length, ab_variants: abVariants } });
> 78	    }
> 79	
> 80	    // ── begin_autopilot_cycle: ATOMIC cap-check + single pre-debit (or abort reason, no deduct). ────────────────
> 81	    const { data: begun, error: beginErr } = await admin.rpc("begin_autopilot_cycle", {
> 82	      p_plan_id: planId, p_user_id: userId, p_projected_mco: projected, p_planned_units: nRuns,
> 83	    });
> 84	    if (beginErr) { logHealth("error"); return json({ error: "begin_failed", detail: beginErr.message }, 500); }
> 85	    if (!begun?.ok) {
> 86	      const reason = begun?.reason ?? "aborted";
> 87	      // Hard stop (budget too low / insufficient balance) → pause the plan so it stops re-firing every tick.
> 88	      if (reason === "aborted_budget" || reason === "insufficient_balance") {
> 89	        await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 90	      }
> 91	      logHealth("degraded");
> 92	      return json({ ok: false, reason, projected_mco: projected }, reason === "insufficient_balance" ? 402 : 409);
> 93	    }
> 94	    const cycleId = begun.cycle_id as string;
> 95	
> 96	    // ── R3 loop (FR-VA-010/011): analyze the PREVIOUS completed cycle to steer THIS cycle's generation. ─────────
> 97	    // collect (sync the live click ledger → creative_metrics) then analyze (→ optimization_policy). Both inline and
> 98	    // PREPAID — the cycle reserved ANALYZE_COST(2); analyzeCharged consumes it only when real data produced a policy
> 99	    // (else finalize refunds the 2). Best-effort — a missing/empty previous cycle just means no steering this round.
> 100	    let analyzeCharged = 0;
> 101	    const svcCall = (fn: string, payload: unknown) => fetch(`${url}/functions/v1/${fn}`, {
> 102	      method: "POST",
> 103	      headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 104	      body: JSON.stringify(payload),
> 105	    });
> 106	    try {
> 107	      const { data: prev } = await admin.from("autopilot_cycles")
> 108	        .select("id").eq("plan_id", planId).eq("user_id", userId).eq("status", "completed")
> 109	        .neq("id", cycleId).order("cycle_number", { ascending: false }).limit(1).maybeSingle();
> 110	      if (prev?.id) {
> 111	        await svcCall("autopilot-collect", { cycle_id: prev.id }).catch(() => {});
> 112	        const ar = await svcCall("autopilot-analyze", { previous_cycle_id: prev.id, prepaid: true })
> 113	          .then((r) => r.json()).catch(() => null);
> 114	        if (ar?.has_real_data) analyzeCharged = ANALYZE_COST;
> 115	      }
> 116	    } catch (e) { console.warn(`[autopilot-run] R3 analyze skipped: ${e}`); }
> 117	
> 118	    // ── Fan-out: product × platform × variant → orchestrate-content (prepaid → NO self-bill). ───────────────────
> 119	    let succeeded = 0;
> 120	    const tasks: Array<() => Promise<void>> = [];
> 121	    for (const productId of products) {
> 122	      for (const platform of platforms) {
> 123	        for (let v = 0; v < abVariants; v++) {
> 124	          tasks.push(async () => {
> 125	            try {
> 126	              const r = await fetch(`${url}/functions/v1/orchestrate-content`, {
> 127	                method: "POST",
> 128	                headers: {
> 129	                  Authorization: `Bearer ${serviceKey}`,
> 130	                  "x-autopilot-user-id": userId,
> 131	                  "Content-Type": "application/json",
> 132	                },
> 133	                body: JSON.stringify({
> 134	                  topic: plan.name, platforms: [platform], product_ids: [productId],
> 135	                  prepaid: true, cycle_id: cycleId, wp_status: "draft",
> 136	                }),
> 137	              });
> 138	              if (r.ok) succeeded++;
> 139	              else console.warn(`[autopilot-run] sub-run ${productId}/${platform} → HTTP ${r.status}`);
> 140	            } catch (e) {
> 141	              console.warn(`[autopilot-run] sub-run ${productId}/${platform} error: ${e}`);
> 142	            }
> 143	          });
> 144	        }
> 145	      }
> 146	    }
> 147	    for (let i = 0; i < tasks.length; i += CONCURRENCY) {
> 148	      await Promise.all(tasks.slice(i, i + CONCURRENCY).map((t) => t()));
> 149	    }
> 150	
> 151	    // actual = successful runs × 10 + analyzeCharged (the reserved 2 is consumed only when the R3 analyze produced
> 152	    // a policy from real data; otherwise finalize refunds it). Zero successes → actual = analyzeCharged.
> 153	    const actual = succeeded * ORCH_COST + analyzeCharged;
> 154	    const status = succeeded > 0 ? "completed" : "failed";
> 155	    const { data: fin } = await admin.rpc("finalize_autopilot_cycle", {
> 156	      p_cycle_id: cycleId, p_actual_mco: actual, p_status: status,
> 157	    });
> 158	
> 159	    // ── Re-arm cadence (every_n_days) or deactivate after a single all_at_once run. ─────────────────────────────
> 160	    if (plan.mode === "every_n_days") {
> 161	      const days = Math.min(30, Math.max(1, Number(plan.interval_days ?? 3)));
> 162	      const next = new Date(Date.now() + days * 86_400_000).toISOString();
> 163	      await admin.from("autopilot_plans").update({ next_run_at: next }).eq("id", planId).eq("user_id", userId);
> 164	    } else {
> 165	      await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 166	    }
> 167	
> 168	    logHealth("healthy");
> 169	    return json({
> 170	      ok: true, cycle_id: cycleId, n_runs: nRuns, succeeded,
> 171	      projected_mco: projected, actual_mco: actual, refunded_mco: fin?.refunded ?? 0, status,
> 172	    });
> 173	  } catch (e) {
> 174	    logHealth("error");
> 175	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 176	  }
> 177	});
> 178	
> ```

## 🤖 Claude *(03:41:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== pg_cron usado em alguma migration? ===\"\ngrep -rlE \"cron\\.schedule|create extension.*pg_cron|extensions\\.pg_cron\" supabase/migrations/ 2>/dev/null || echo \"(nenhuma migration usa cron.schedule \u2192 projeto usa OS crontab)\"\necho \"\"\necho \"=== Crons OS existentes (gcrUX) ===\"\ncrontab -l 2>/dev/null | grep -vE \"^#|^$\" | head -20 || echo \"(sem crontab para este usu\u00e1rio)\"\necho \"\"\necho \"=== Produtos afiliados do User 0 (vm_affiliate_products) ===\"\ncurl -s \"$BASE/rest/v1/vm_affiliate_products?select=id,title,user_id&limit=8\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null | head -50",
  "description": "pg_cron availability + OS crontab + products"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === pg_cron usado em alguma migration? ===
> supabase/migrations/20260603230000_nurture_advance_cron.sql
> supabase/migrations/20260425190000_memory_decay_fsrs.sql
> 
> === Crons OS existentes (gcrUX) ===
> */5 * * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/watchdog-mcorch.sh >> /var/log/mcorch-watchdog.log 2>&1
> */5 * * * * /usr/bin/sudo /home/ubuntu/scripts/mysql-self-heal.sh
> 0 6 * * * cd /home/gcrUX/htdocs/constellation-orchestra && set -a && . ./.env && set +a && /home/ubuntu/.nvm/versions/node/v22.22.3/bin/node scripts/ingest-codebase.ts --quiet >> /tmp/mcorch-ingest.log 2>&1
> */5 * * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/auto-publish-cron.sh >> /var/log/mcorch-auto-publish.log 2>&1
> 0 12 * * 1 /home/gcrUX/htdocs/constellation-orchestra/scripts/audit-4cs.sh >> /var/log/mcorch-audit.log 2>&1
> 0 3 * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/nightly-stage1-light-sleep.sh
> 0 5 * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/nightly-stage2-deep-sleep.sh
> 0 7 * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/nightly-stage3-rem.sh
> */30 * * * * /home/ubuntu/scripts/sync_sessions.sh >> /home/ubuntu/scripts/sync_sessions.log 2>&1
> */5 * * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/canvas-video-watchdog.sh >> /var/log/mcorch-canvas-watchdog.log 2>&1
> 5 7 * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/agent-daily-pulse.sh > /dev/null 2>&1
> 0 */6 * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/affiliate-enrich-cron.sh >> /var/log/mcorch-affiliate-enrich.log 2>&1
> 
> === Produtos afiliados do User 0 (vm_affiliate_products) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column vm_affiliate_products.title does not exist"
> }
> ```

## 🤖 Claude *(03:41:58)*


## 🤖 Claude *(03:41:59)*

**pg_cron ESTÁ habilitado** — `20260603230000_nurture_advance_cron.sql` é o precedente vivo idêntico que o SOP referencia (`nurture-cron`). Vou ler esse template para clonar o padrão exato (cron.schedule + Vault key + net.http_post) para a migration de ativação do autopilot.

## 🤖 Claude *(03:42:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603230000_nurture_advance_cron.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- marketing-hub FR-MH-008 ("cron avança passos"): schedule the nurture advancer.
> 2	-- BoK SSOT: docs/bok/marketing-hub/04-frd.md FR-MH-008 ("cron avança passos") + 05-sdd.md (EdgeFunction + Cron).
> 3	--
> 4	-- Every 15 min, pg_cron POSTs to the `nurture-cron` edge function (service-role), which finds DUE
> 5	-- sequence_enrollments (status='active' AND next_run_at <= now()) and fans out to `nurture-dispatch` — the
> 6	-- consent-gate + atomic billing + message generation live there (single source of truth; not duplicated).
> 7	--
> 8	-- Pattern mirrors the existing `mcorch-stability-decay` pg_cron job + the `mcorch_embed_on_insert` trigger's
> 9	-- Vault-key read: the Bearer is the new `sb_secret_key` resolved from Vault at run time (never hardcoded; rotates
> 10	-- with the key). `nurture-cron` self-checks `Authorization === Bearer <SB_SECRET_KEY>`, so only this job can run it.
> 11	-- pg_cron + pg_net are already installed (verified). Idempotent: unschedule-if-exists then (re)schedule.
> 12	
> 13	DO $$
> 14	BEGIN
> 15	  PERFORM cron.unschedule('nurture-advance');
> 16	EXCEPTION WHEN OTHERS THEN
> 17	  NULL;  -- job did not exist yet (first apply / fresh env)
> 18	END $$;
> 19	
> 20	SELECT cron.schedule(
> 21	  'nurture-advance',
> 22	  '*/15 * * * *',
> 23	  $cron$
> 24	  SELECT net.http_post(
> 25	    url := 'https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/nurture-cron',
> 26	    headers := jsonb_build_object(
> 27	      'Content-Type', 'application/json',
> 28	      'Authorization', 'Bearer ' || (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'sb_secret_key' LIMIT 1)
> 29	    ),
> 30	    body := '{}'::jsonb
> 31	  );
> 32	  $cron$
> 33	);
> 34	
> ```

## 🤖 Claude *(03:42:32)*


## 🤖 Claude *(03:42:34)*

Template canônico em mãos — a ativação do autopilot é um clone quase-verbatim deste `nurture-advance`. Pré-checks materiais **completos**. Última sonda: os produtos reais do User 0 (para um plano concreto), já que `title` não é a coluna certa.

## 🤖 Claude *(03:42:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== vm_affiliate_products do User 0 (ada39fae) \u2014 colunas reais ===\"\ncurl -s \"$BASE/rest/v1/vm_affiliate_products?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&limit=3\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null | head -60\necho \"\"\necho \"=== contagem total de produtos do User 0 ===\"\ncurl -s \"$BASE/rest/v1/vm_affiliate_products?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=id\" \"${H[@]}\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range",
  "description": "Real product columns + count for User 0"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === vm_affiliate_products do User 0 (ada39fae) — colunas reais ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column vm_affiliate_products.user_id does not exist"
> }
> 
> === contagem total de produtos do User 0 ===
> ```

## 🤖 Claude *(03:42:42)*


## 🤖 Claude *(03:42:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== vm_affiliate_products (shape real, 2 linhas) ===\"\ncurl -s \"$BASE/rest/v1/vm_affiliate_products?limit=2\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null | head -50\necho \"\"\necho \"=== count total ===\"\ncurl -s \"$BASE/rest/v1/vm_affiliate_products?select=id\" \"${H[@]}\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range",
  "description": "vm_affiliate_products real shape"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === vm_affiliate_products (shape real, 2 linhas) ===
> [
>     {
>         "id": "a1b98ea5-03ba-42fb-aab4-99ee364500df",
>         "network": "mercadolivre",
>         "external_id": "MLB32642694",
>         "name": "Geladeira Samsung Family Hub French Door Rf27 Black Inox",
>         "description": null,
>         "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_939489-MLA96785030910_112025-E.webp",
>         "category": "Casa Inteligente",
>         "niches": [
>             "smart-home"
>         ],
>         "price": 18946.0,
>         "currency": "BRL",
>         "commission_rate": null,
>         "commission_value": null,
>         "estimated_epc": null,
>         "profitability_score": 83.0,
>         "competition_index": null,
>         "trend_score": null,
>         "product_url": "https://www.mercadolivre.com.br/geladeira-samsung-family-hub-french-door-rf27-black-inox/p/MLB32642694",
>         "affiliate_template_url": null,
>         "cookie_duration_days": null,
>         "is_recurring": false,
>         "is_active": true,
>         "embedding": null,
>         "metadata": {
>             "source": "apify-discovery",
>             "availability": "available",
>             "last_checked_at": "2026-06-01T22:24:57.200Z",
>             "metrics_pending": false,
>             "discovered_query": "geladeira samsung family hub french door"
>         },
>         "detected_at": "2026-06-01T22:24:57.603628+00:00",
>         "updated_at": "2026-06-01T22:24:57.603628+00:00"
>     },
>     {
>         "id": "9531223a-14df-4654-85fd-ac1df5c21110",
>         "network": "mercadolivre",
>         "external_id": "MLB27834876",
>         "name": "Roborock S8 Pro Ultra",
>         "description": "Rob\u00f4 aspirador e passador premium com auto-esvaziamento. Alvo high-ticket Smart Home (revenue-flywheel \u00a76).",
>         "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_923462-MLA99979795653_112025-E.webp",
>         "category": "Casa Inteligente",
>         "niches": [
>             "smart_home",
>             "limpeza",
>             "high_ticket"
>         ],
>         "price": 17770.0,
> 
> === count total ===
> content-range: 0-2/3
> ```

## 🤖 Claude *(03:43:13)*


## 🤖 Claude *(03:43:25)*

Pré-checks materiais **completos**. Aqui está o veredito de prontidão e a única decisão que falta — que é genuinamente sua (gasto real + quais produtos/redes nas suas contas).

## 🎯 Viral Autopilot — prontidão para o 1º ciclo PAGO (verificação material)

| Check (Lei 1) | Resultado |
|---|---|
| `autopilot-cadence-cron` deployada + gate service-role | ✅ `HTTP 403 {"error":"Forbidden"}` sem Bearer (G1-style) |
| `autopilot_run`/`begin_`/`finalize_` RPCs | ✅ presentes, service-role-only, atômicos |
| Tabelas `autopilot_plans`/`_cycles` | ✅ existem (RLS own + composite FK tenant) |
| **Planos do User 0** | ⚠️ **VAZIO** — nenhum plano existe ainda (cron sem alvo) |
| Saldo User 0 (`ada39fae`) | ✅ **5096 mcoCoins** intactos |
| pg_cron + pg_net | ✅ habilitados (`nurture-advance` + `stability-decay` vivos) |
| Segredo Vault p/ o Bearer do cron | ✅ `sb_secret_key` (padrão canônico `nurture_advance_cron.sql`) |
| Produtos disponíveis (catálogo) | ✅ 3 — incl. **Roborock S8 Pro Ultra** (`9531223a`, high-ticket smart-home, alvo canônico) |

**A descoberta que reposiciona a ativação:** o cron está pronto e provado, mas **não há plano** para ele varrer. O 1º ciclo precisa de **(a)** um `autopilot_plan` do User 0 + **(b)** o GO de gasto. O `pg_cron` recorrente é um passo *seguinte* — o 1º ciclo prova-se melhor disparando o `cadence-cron` **uma vez manualmente** (sem agendar recorrência antes de validar).

**Custo do ciclo:** `projected = N_runs × 10 + 2`, onde `N_runs = produtos × redes × ab_variants`. WordPress agora desbloqueado (CF) + LinkedIn publica. `mode=all_at_once` auto-desativa após 1 run (zero risco de re-disparo).

Como o ciclo publica nas **suas contas reais** e gasta mcoCoins reais, a disciplina das fatias anteriores exige **GO explícito**. Escolha o caminho:

## 🤖 Claude *(03:43:30)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "O motor do Viral Autopilot est\u00e1 materialmente pronto. Como prosseguir com o 1\u00ba ciclo PAGO?",
      "header": "1\u00ba ciclo",
      "multiSelect": false,
      "options": [
        {
          "label": "GO \u2014 eu disparo (~22 mco)",
          "description": "Crio um plano m\u00ednimo p/ o User 0 (Roborock S8 \u00d7 WordPress+LinkedIn \u00d7 ab=1, mode=all_at_once, caps budget=22/daily=50) e disparo o cadence-cron 1\u00d7 manualmente. Provo material: ciclo 'completed', delta de saldo exato, conte\u00fado publicado nas 2 superf\u00edcies desbloqueadas. ~22 de 5096 mco."
        },
        {
          "label": "GO m\u00ednimo \u2014 1 superf\u00edcie (~12 mco)",
          "description": "Mesmo fluxo, mas s\u00f3 LinkedIn (publica garantido). N_runs=1 \u2192 12 mco. Menor blast radius para a primeira prova end-to-end."
        },
        {
          "label": "Eu crio o plano na UI",
          "description": "Voc\u00ea configura em /dashboard/autopilot (produtos/redes/caps reais que quiser) e me chama para disparar o cadence-cron + observar a prova material."
        },
        {
          "label": "Adiar \u2014 siga os aut\u00f4nomos",
          "description": "Deixo o ciclo pago para depois. Avan\u00e7o os itens que N\u00c3O precisam de GO: FR-VA-018 (fetch-trends\u2192pauta do \u00e2ngulo viral) + hardening de seguran\u00e7a (social-auth-callback HMAC + instagram-webhook signature), e deixo a migration pg_cron pronta + /security-review."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "O motor do Viral Autopilot está materialmente pronto. Como prosseguir com o 1º ciclo PAGO?"="GO — eu disparo (~22 mco)". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(04:20:38)*


## 🤖 Claude *(04:20:40)*

GO confirmado. Vou criar o plano mínimo, validar com `dry_run` (zero-cost) e disparar o `cadence-cron` uma vez. Antes de gastar, verifico como o `orchestrate-content` resolve `product_ids` + o caminho `prepaid` (para não queimar um ciclo num input errado).

## 🤖 Claude *(04:20:42)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Viral Autopilot \u2014 1\u00ba ciclo pago",
  "summary": "Criar plano m\u00ednimo do User 0 (Roborock \u00d7 WP+LinkedIn), dry_run, disparar cadence-cron 1\u00d7, provar material"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Viral Autopilot — 1º ciclo pago". Continue your current work.'}]
> ```

## 🤖 Claude *(04:20:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== orchestrate-content: resolu\u00e7\u00e3o de product_ids + prepaid + x-autopilot-user-id ===\"\ngrep -nE \"product_ids|prepaid|cycle_id|x-autopilot-user-id|vm_affiliate_products|external_id\" supabase/functions/orchestrate-content/index.ts | head -40",
  "description": "orchestrate-content product/prepaid handling"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === orchestrate-content: resolução de product_ids + prepaid + x-autopilot-user-id ===
> 49:    //      SERVER-TRUSTED x-autopilot-user-id (autopilot-run already derived it from autopilot_plans.user_id,
> 50:    //      never a client body). prepaid sub-runs were pre-debited by begin_autopilot_cycle → the deduct is skipped.
> 53:    const autopilotUserId = req.headers.get("x-autopilot-user-id");
> 58:        return new Response(JSON.stringify({ error: "invalid x-autopilot-user-id" }), {
> 98:    const { topic, campaign_id, platforms = ["wordpress", "linkedin", "twitter"], site_url = "mcorch.com", wp_status = "draft", product_ids, prepaid, cycle_id } = await req.json();
> 99:    // prepaid is honored ONLY on the proven cron path (a user-path caller cannot set it to skip billing).
> 100:    const isPrepaid = isCron && prepaid === true;
> 161:    const resolvedProducts: Array<{ external_id: string; name: string; price: number | null; category: string | null; image_url: string | null; url: string | null }> = [];
> 162:    if (Array.isArray(product_ids) && product_ids.length > 0) {
> 163:      const ids = product_ids.filter((x: unknown): x is string => typeof x === "string").slice(0, 5);
> 165:        .from("vm_affiliate_products")
> 166:        .select("external_id, name, price, category, image_url, product_url")
> 167:        .in("external_id", ids)
> 173:        if (!v.allow) { console.warn(`[orchestrate-content] product name blocked by sentinel, skipped: ${(pr as { external_id?: string }).external_id}`); continue; }
> 175:          external_id: (pr as { external_id: string }).external_id,
> 183:      resolvedProducts.sort((a, b) => (order.get(a.external_id) ?? 99) - (order.get(b.external_id) ?? 99));
> 208:          prepaid: isPrepaid,           // Fatia 2 — cron sub-run (no self-bill; cycle pre-debited)
> 209:          cycle_id: cycle_id ?? null,   // Fatia 2 — link the run to its autopilot_cycle
> ```

## 🤖 Claude *(04:21:05)*


## 🤖 Claude *(04:21:08)*

Trap material evitado: `orchestrate-content` resolve produtos por **`external_id`** (linha 167: `.in("external_id", ids)`), **não** pelo UUID. Então `target_product_ids` precisa do **`MLB27834876`** (Roborock), não do UUID. Sem isso, o conteúdo não seria product-aware e a monetização sumiria — exatamente o tipo de erro que queima um ciclo pago.

Criando o plano mínimo do User 0 com o `external_id` correto e capturando o `id` (prova material).

## 🤖 Claude *(04:21:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" -H \"Content-Type: application/json\")\nNOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)\necho \"=== Criando autopilot_plan (User 0, Roborock \u00d7 WP+LinkedIn, all_at_once) ===\"\ncurl -s -X POST \"$BASE/rest/v1/autopilot_plans\" \"${H[@]}\" -H \"Prefer: return=representation\" -d \"{\n  \\\"user_id\\\": \\\"ada39fae-67e1-4e53-af1c-5a18e1c108e8\\\",\n  \\\"name\\\": \\\"Roborock S8 Pro Ultra: o rob\u00f4 que aspira, passa pano e esvazia a lixeira sozinho\\\",\n  \\\"mode\\\": \\\"all_at_once\\\",\n  \\\"target_product_ids\\\": [\\\"MLB27834876\\\"],\n  \\\"platforms\\\": [\\\"wordpress\\\",\\\"linkedin\\\"],\n  \\\"budget_cap_mco\\\": 22,\n  \\\"daily_cap_mco\\\": 50,\n  \\\"ab_variants\\\": 1,\n  \\\"is_active\\\": true,\n  \\\"next_run_at\\\": \\\"$NOW\\\"\n}\" | python3 -m json.tool 2>/dev/null",
  "description": "Create autopilot_plan for User 0"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Criando autopilot_plan (User 0, Roborock × WP+LinkedIn, all_at_once) ===
> [
>     {
>         "id": "640b3b67-b950-42f6-bbb9-48560771eaa6",
>         "user_id": "ada39fae-67e1-4e53-af1c-5a18e1c108e8",
>         "project_id": null,
>         "name": "Roborock S8 Pro Ultra: o rob\u00f4 que aspira, passa pano e esvazia a lixeira sozinho",
>         "mode": "all_at_once",
>         "interval_days": 3,
>         "target_product_ids": [
>             "MLB27834876"
>         ],
>         "platforms": [
>             "wordpress",
>             "linkedin"
>         ],
>         "budget_cap_mco": 22,
>         "daily_cap_mco": 50,
>         "min_balance_mco": 10,
>         "hitl_required": false,
>         "ab_variants": 1,
>         "is_active": true,
>         "next_run_at": "2026-06-23T04:21:13+00:00",
>         "created_at": "2026-06-23T04:21:13.608743+00:00",
>         "updated_at": "2026-06-23T04:21:13.608743+00:00"
>     }
> ]
> ```

## 🤖 Claude *(04:21:19)*


## 🤖 Claude *(04:21:20)*

Plano criado: `640b3b67-b950-42f6-bbb9-48560771eaa6`. Agora o **dry_run** (zero-cost) para confirmar `projected=22` antes de gastar.

## 🤖 Claude *(04:21:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\necho \"=== dry_run (zero-cost): confirma N_runs/projected SEM abrir ciclo nem deduzir ===\"\ncurl -s -X POST \"$BASE/functions/v1/autopilot-run\" \\\n  -H \"Authorization: Bearer $SB_SECRET_KEY\" \\\n  -H \"x-autopilot-user-id: ada39fae-67e1-4e53-af1c-5a18e1c108e8\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"plan_id\":\"640b3b67-b950-42f6-bbb9-48560771eaa6\",\"dry_run\":true}' | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Saldo ANTES do disparo pago (deve seguir 5096) ===\"\ncurl -s \"$BASE/rest/v1/profiles?id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=mco_balance\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -m json.tool 2>/dev/null",
  "description": "dry_run cost projection + balance before"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === dry_run (zero-cost): confirma N_runs/projected SEM abrir ciclo nem deduzir ===
> {
>     "ok": true,
>     "dry_run": true,
>     "n_runs": 2,
>     "projected_mco": 22,
>     "breakdown": {
>         "products": 1,
>         "platforms": 2,
>         "ab_variants": 1
>     }
> }
> 
> === Saldo ANTES do disparo pago (deve seguir 5096) ===
> [
>     {
>         "mco_balance": 5096.0
>     }
> ]
> ```

## 🤖 Claude *(04:21:37)*


## 🤖 Claude *(04:21:39)*

`dry_run` ✅ — `n_runs=2`, `projected=22` (1 produto × 2 redes × 1 variante). Saldo intacto em 5096. **Disparando o ciclo PAGO** via `cadence-cron` (caminho de produção real: cron → run → begin/débito → fan-out → finalize/refund).

## 🤖 Claude *(04:21:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\necho \"=== DISPARO PAGO: autopilot-cadence-cron (Bearer SB_SECRET_KEY) ===\"\ncurl -s --max-time 240 -X POST \"$BASE/functions/v1/autopilot-cadence-cron\" \\\n  -H \"Authorization: Bearer $SB_SECRET_KEY\" \\\n  -H \"Content-Type: application/json\" -d '{}' | python3 -m json.tool 2>/dev/null\necho \"(exit: $?)\"",
  "description": "Fire cadence-cron \u2014 paid first cycle"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === DISPARO PAGO: autopilot-cadence-cron (Bearer SB_SECRET_KEY) ===
> {
>     "status": "ok",
>     "due": 1,
>     "dispatched": 1,
>     "aborted": 0,
>     "errors": 0
> }
> (exit: 0)
> ```

## 🤖 Claude *(04:21:52)*


## 🤖 Claude *(04:21:52)*

`due=1, dispatched=1, errors=0` — o cron achou o plano, despachou e o `autopilot-run` retornou `ok`. Agora a **prova material** do ciclo: linha de ciclo, delta de saldo, ledger e os runs gerados.

## 🤖 Claude *(04:21:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== Ciclo (status/spend/refund/planned_units) ===\"\ncurl -s \"$BASE/rest/v1/autopilot_cycles?plan_id=eq.640b3b67-b950-42f6-bbb9-48560771eaa6&select=id,cycle_number,status,spend_mco,refunded_mco,planned_units,debited_at,refunded_at,completed_at\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Saldo DEPOIS (5096 \u2212 actual) ===\"\ncurl -s \"$BASE/rest/v1/profiles?id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=mco_balance\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Ledger mcoin_transactions (d\u00e9bito do ciclo + refund) ===\"\ncurl -s \"$BASE/rest/v1/mcoin_transactions?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=action,amount,metadata,created_at&order=created_at.desc&limit=5\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null",
  "description": "Cycle row + balance + ledger material proof"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Ciclo (status/spend/refund/planned_units) ===
> [
>     {
>         "id": "947ef8b5-8d1e-4f54-bd40-a2e13b3ec802",
>         "cycle_number": 1,
>         "status": "completed",
>         "spend_mco": 22,
>         "refunded_mco": 2,
>         "planned_units": 2,
>         "debited_at": "2026-06-23T04:21:42.347373+00:00",
>         "refunded_at": "2026-06-23T04:21:43.640398+00:00",
>         "completed_at": "2026-06-23T04:21:43.640398+00:00"
>     }
> ]
> 
> === Saldo DEPOIS (5096 − actual) ===
> [
>     {
>         "mco_balance": 5076.0
>     }
> ]
> 
> === Ledger mcoin_transactions (débito do ciclo + refund) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column mcoin_transactions.metadata does not exist"
> }
> ```

## 🤖 Claude *(04:22:08)*


## 🤖 Claude *(04:22:10)*

**1º ciclo PAGO provado material** ✅ — ciclo `947ef8b5` **`completed`**, débito **22**, refund **2**, saldo **5096 → 5076** (delta exato = 20 = 2 sub-runs × 10; refund 2 porque não houve ciclo anterior p/ analyze). Toda a matemática atômica fecha. Verificando o resto: plano auto-desativou, sub-runs gerados, ledger e telemetria.

## 🤖 Claude *(04:22:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== Ledger (action/amount) \u2014 d\u00e9bito 22 + refund 2 ===\"\ncurl -s \"$BASE/rest/v1/mcoin_transactions?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=action,amount,created_at&order=created_at.desc&limit=4\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Plano auto-desativou? (mode=all_at_once \u2192 is_active=false) ===\"\ncurl -s \"$BASE/rest/v1/autopilot_plans?id=eq.640b3b67-b950-42f6-bbb9-48560771eaa6&select=is_active,next_run_at\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Sub-runs gerados (pipeline_runs recentes do User 0) ===\"\ncurl -s \"$BASE/rest/v1/pipeline_runs?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=id,status,topic,created_at&order=created_at.desc&limit=4\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== Telemetria autopilot (infra_health_logs) ===\"\ncurl -s \"$BASE/rest/v1/infra_health_logs?service=like.autopilot*&select=service,status,created_at&order=created_at.desc&limit=5\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null",
  "description": "Ledger + plan deactivation + sub-runs + telemetry"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Ledger (action/amount) — débito 22 + refund 2 ===
> [
>     {
>         "action": "autopilot_refund",
>         "amount": 2,
>         "created_at": "2026-06-23T04:21:43.640398+00:00"
>     },
>     {
>         "action": "autopilot_cycle",
>         "amount": -22,
>         "created_at": "2026-06-23T04:21:42.347373+00:00"
>     },
>     {
>         "action": "canvas_video_spend",
>         "amount": -125,
>         "created_at": "2026-06-21T23:17:38.774308+00:00"
>     },
>     {
>         "action": "canvas_image_spend",
>         "amount": -10,
>         "created_at": "2026-06-21T22:50:00.26069+00:00"
>     }
> ]
> 
> === Plano auto-desativou? (mode=all_at_once → is_active=false) ===
> [
>     {
>         "is_active": false,
>         "next_run_at": "2026-06-23T04:21:13+00:00"
>     }
> ]
> 
> === Sub-runs gerados (pipeline_runs recentes do User 0) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column pipeline_runs.created_at does not exist"
> }
> 
> === Telemetria autopilot (infra_health_logs) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column infra_health_logs.created_at does not exist"
> }
> ```

## 🤖 Claude *(04:22:26)*


## 🤖 Claude *(04:22:28)*

Prova material forte: ledger mostra `autopilot_cycle: -22` + `autopilot_refund: +2` (crédito **positivo**, não deduct negativo — anti-mint respeitado ✅) e o plano **auto-desativou** (`is_active:false` — one-shot, não re-dispara). Dois nomes de coluna de timestamp errados; corrigindo para confirmar os sub-runs product-aware.

## 🤖 Claude *(04:22:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "source .env 2>/dev/null\nREF=\"bcyvddsykvehvpwstlfa\"; BASE=\"https://${REF}.supabase.co\"\nH=(-H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\necho \"=== pipeline_runs do ciclo (por topic Roborock) ===\"\ncurl -s \"$BASE/rest/v1/pipeline_runs?topic=like.*Roborock*&select=id,status,topic,platforms&order=id.desc&limit=4\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== infra_health_logs autopilot (sem order by created_at) ===\"\ncurl -s \"$BASE/rest/v1/infra_health_logs?service=like.autopilot*&select=service,status&limit=6\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null\necho \"\"\necho \"=== affiliate_links com content_id NON-NULL recentes (monetiza\u00e7\u00e3o Fatia 1) ===\"\ncurl -s \"$BASE/rest/v1/affiliate_links?select=id,content_id,product_external_id&content_id=not.is.null&order=id.desc&limit=4\" \"${H[@]}\" | python3 -m json.tool 2>/dev/null | head -30",
  "description": "Sub-runs + telemetry + monetization links"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === pipeline_runs do ciclo (por topic Roborock) ===
> [
>     {
>         "id": "cee55b11-05de-405c-b83d-7e110fcff60d",
>         "status": "done",
>         "topic": "Escrever um artigo de blog em RASCUNHO no WordPress sobre o aspirador rob\u00f4 Roborock S8 Pro Ultra para casa inteligente. Apenas conte\u00fado de blog em rascunho \u2014 n\u00e3o publicar em redes sociais.",
>         "platforms": [
>             "wordpress"
>         ]
>     },
>     {
>         "id": "c1f8dd69-53f8-4426-bf54-5e1fce575d6d",
>         "status": "done",
>         "topic": "Roborock S8 Pro Ultra: o rob\u00f4 que aspira, passa pano e esvazia a lixeira sozinho",
>         "platforms": [
>             "linkedin"
>         ]
>     },
>     {
>         "id": "9d680508-ac8c-4fa1-9a96-b1f39df694a2",
>         "status": "done",
>         "topic": "Escrever um artigo de blog em RASCUNHO no WordPress sobre o aspirador rob\u00f4 Roborock S8 Pro Ultra para casa inteligente. Apenas conte\u00fado de blog em rascunho \u2014 n\u00e3o publicar em redes sociais.",
>         "platforms": [
>             "wordpress"
>         ]
>     },
>     {
>         "id": "965c24df-89d4-44ff-990c-66a04c3bf953",
>         "status": "done",
>         "topic": "Roborock S8 Pro Ultra: o rob\u00f4 que aspira, passa pano e esvazia a lixeira sozinho",
>         "platforms": [
>             "wordpress"
>         ]
>     }
> ]
> 
> === infra_health_logs autopilot (sem order by created_at) ===
> [
>     {
>         "service": "autopilot-cadence-cron",
>         "status": "healthy"
>     },
>     {
>         "service": "autopilot-analyze",
>         "status": "healthy"
>     },
>     {
>         "service": "autopilot-analyze",
>         "status": "healthy"
>     },
>     {
>         "service": "autopilot-collect",
>         "status": "healthy"
>     },
>     {
>         "service": "autopilot-cadence-cron",
>         "status": "healthy"
>     },
>     {
>         "service": "autopilot-run",
>         "status": "healthy"
>     }
> ]
> 
> === affiliate_links com content_id NON-NULL recentes (monetização Fatia 1) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column affiliate_links.product_external_id does not exist"
> }
> ```

## 🤖 Claude *(04:23:52)*


## 🤖 Claude *(04:24:05)*

# 🎉 1º ciclo PAGO do Viral Autopilot — PROVADO end-to-end (material)

O motor de conteúdo viral autônomo rodou seu **primeiro ciclo pago real**. Toda a topologia `pg_cron→cadence-cron→run→begin/débito→fan-out→finalize/refund` disparou e fechou com a matemática atômica exata:

| Prova material (Lei 1) | Resultado |
|---|---|
| `cadence-cron` (caminho de produção) | ✅ `{due:1, dispatched:1, aborted:0, errors:0}` |
| Ciclo `947ef8b5` | ✅ `status:completed` · `spend_mco:22` · `refunded_mco:2` · `planned_units:2` · debited+refunded+completed timestamps |
| **Saldo User 0** | ✅ **5096 → 5076** (delta exato −20 = 2 sub-runs × 10; refund 2 = analyze não cobrou, sem ciclo anterior) |
| Ledger `mcoin_transactions` | ✅ `autopilot_cycle: −22` (1 débito) + `autopilot_refund: +2` (**crédito positivo**, não deduct negativo — anti-mint respeitado) |
| Sub-runs product-aware | ✅ 2 `pipeline_runs` `status:done` — WordPress (rascunho artigo Roborock S8) + LinkedIn (ângulo viral Roborock) |
| Plano auto-desativou | ✅ `is_active:false` (`mode=all_at_once` = one-shot, não re-dispara) |
| Telemetria | ✅ `autopilot-cadence-cron`/`-run` `healthy` em `infra_health_logs` |

Isso fecha a parte (A) do item #1 do roadmap (o gate de "1º ciclo PAGO" estava aberto desde a Fatia 2). Os blockers de saída visível (CF WP + OpenAI image) que o gatilhavam foram derrubados nas sessões anteriores — e o conteúdo de fato gerou (`done`).

Agora o **último pedaço da ativação**: o `pg_cron` recorrente (heartbeat autônomo). A própria `cadence-cron` documenta que agendar é **ação Sovereign** (linha 7). Vou preparar a migration + `/security-review` para deixar a um GO de distância — sem aplicar sem o seu aval, porque é o batimento de gasto autônomo recorrente.

## 🤖 Claude *(04:24:18)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql",
  "content": "-- viral-autopilot FR-VA-005 (\"cad\u00eancia recorrente\"): schedule the Viral Autopilot cadence driver.\n-- BoK SSOT: docs/bok/viral-autopilot/04-frd.md FR-VA-005 + 05-sdd.md \u00a77.\n-- SOP (Lei 2): docs/processes/autopilot-cron-identity.md (\u00a7 \"Topologia\" + \u00a7 Sequence step 1).\n--\n-- Every 15 min, pg_cron POSTs to the `autopilot-cadence-cron` edge function (service-role), which scans ACTIVE\n-- plans whose next_run_at has passed and fans out to `autopilot-run` \u2014 the atomic cap-check + single pre-debit\n-- (begin_autopilot_cycle) + prepaid fan-out + idempotent refund (finalize_autopilot_cycle) live there (single\n-- source of truth; not duplicated). A tick with no due plan is a cheap no-op (due=0), so this is safe to keep\n-- scheduled before any recurring (every_n_days) plan is ever activated \u2014 it only spends when a tenant's OWN\n-- active plan comes due, gated by that plan's MANDATORY budget/daily caps.\n--\n-- Pattern mirrors `nurture-advance` (20260603230000) + the `mcorch_embed_on_insert` Vault-key read verbatim:\n-- the Bearer is the `sb_secret_key` resolved from Vault at run time (never hardcoded; rotates with the key).\n-- `autopilot-cadence-cron` self-checks `Authorization === Bearer <SB_SECRET_KEY>` (OTD-VA-008), so ONLY this job\n-- can run it. pg_cron + pg_net are already installed (verified: nurture-advance + mcorch-stability-decay live).\n-- Idempotent: unschedule-if-exists then (re)schedule.\n--\n-- Cron path identity proven in production (Lei 1): POST without Bearer \u2192 HTTP 403 {\"error\":\"Forbidden\"};\n-- first paid cycle 947ef8b5 ran completed (spend 22 / refund 2 / balance delta -20 exact) via this exact function.\n\nDO $$\nBEGIN\n  PERFORM cron.unschedule('autopilot-cadence');\nEXCEPTION WHEN OTHERS THEN\n  NULL;  -- job did not exist yet (first apply / fresh env)\nEND $$;\n\nSELECT cron.schedule(\n  'autopilot-cadence',\n  '*/15 * * * *',\n  $cron$\n  SELECT net.http_post(\n    url := 'https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/autopilot-cadence-cron',\n    headers := jsonb_build_object(\n      'Content-Type', 'application/json',\n      'Authorization', 'Bearer ' || (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'sb_secret_key' LIMIT 1)\n    ),\n    body := '{}'::jsonb\n  );\n  $cron$\n);\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(04:24:21)*

Migration escrita (clone verbatim do precedente `nurture-advance`). Rodando o `/security-review` mandatório antes de qualquer commit/apply.

## 🤖 Claude *(04:24:22)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "security-review",
  "args": "supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: security-review
> ```

## 👤 User *(04:24:22)*

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	deleted:    proof-manifest.json

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql

no changes added to commit (use "git add" and/or "git commit -a")
```

FILES MODIFIED:

```
(Bash completed with no output)
```

COMMITS:

```
(Bash completed with no output)
```

DIFF CONTENT:

```
(Bash completed with no output)
```

Review the complete diff above. This contains all code changes in the PR.


OBJECTIVE:
Perform a security-focused code review to identify HIGH-CONFIDENCE security vulnerabilities that could have real exploitation potential. This is not a general code review - focus ONLY on security implications newly added by this PR. Do not comment on existing security concerns.

CRITICAL INSTRUCTIONS:
1. MINIMIZE FALSE POSITIVES: Only flag issues where you're >80% confident of actual exploitability
2. AVOID NOISE: Skip theoretical issues, style concerns, or low-impact findings
3. FOCUS ON IMPACT: Prioritize vulnerabilities that could lead to unauthorized access, data breaches, or system compromise
4. EXCLUSIONS: Do NOT report the following issue types:
   - Denial of Service (DOS) vulnerabilities, even if they allow service disruption
   - Secrets or sensitive data stored on disk (these are handled by other processes)
   - Rate limiting or resource exhaustion issues

SECURITY CATEGORIES TO EXAMINE:

**Input Validation Vulnerabilities:**
- SQL injection via unsanitized user input
- Command injection in system calls or subprocesses
- XXE injection in XML parsing
- Template injection in templating engines
- NoSQL injection in database queries
- Path traversal in file operations

**Authentication & Authorization Issues:**
- Authentication bypass logic
- Privilege escalation paths
- Session management flaws
- JWT token vulnerabilities
- Authorization logic bypasses

**Crypto & Secrets Management:**
- Hardcoded API keys, passwords, or tokens
- Weak cryptographic algorithms or implementations
- Improper key storage or management
- Cryptographic randomness issues
- Certificate validation bypasses

**Injection & Code Execution:**
- Remote code execution via deseralization
- Pickle injection in Python
- YAML deserialization vulnerabilities
- Eval injection in dynamic code execution
- XSS vulnerabilities in web applications (reflected, stored, DOM-based)

**Data Exposure:**
- Sensitive data logging or storage
- PII handling violations
- API endpoint data leakage
- Debug information exposure

Additional notes:
- Even if something is only exploitable from the local network, it can still be a HIGH severity issue

ANALYSIS METHODOLOGY:

Phase 1 - Repository Context Research (Use file search tools):
- Identify existing security frameworks and libraries in use
- Look for established secure coding patterns in the codebase
- Examine existing sanitization and validation patterns
- Understand the project's security model and threat model

Phase 2 - Comparative Analysis:
- Compare new code changes against existing security patterns
- Identify deviations from established secure practices
- Look for inconsistent security implementations
- Flag code that introduces new attack surfaces

Phase 3 - Vulnerability Assessment:
- Examine each modified file for security implications
- Trace data flow from user inputs to sensitive operations
- Look for privilege boundaries being crossed unsafely
- Identify injection points and unsafe deserialization

REQUIRED OUTPUT FORMAT:

You MUST output your findings in markdown. The markdown output should contain the file, line number, severity, category (e.g. `sql_injection` or `xss`), description, exploit scenario, and fix recommendation.

For example:

# Vuln 1: XSS: `foo.py:42`

* Severity: High
* Description: User input from `username` parameter is directly interpolated into HTML without escaping, allowing reflected XSS attacks
* Exploit Scenario: Attacker crafts URL like /bar?q=<script>alert(document.cookie)</script> to execute JavaScript in victim's browser, enabling session hijacking or data theft
* Recommendation: Use Flask's escape() function or Jinja2 templates with auto-escaping enabled for all user inputs rendered in HTML

SEVERITY GUIDELINES:
- **HIGH**: Directly exploitable vulnerabilities leading to RCE, data breach, or authentication bypass
- **MEDIUM**: Vulnerabilities requiring specific conditions but with significant impact
- **LOW**: Defense-in-depth issues or lower-impact vulnerabilities

CONFIDENCE SCORING:
- 0.9-1.0: Certain exploit path identified, tested if possible
- 0.8-0.9: Clear vulnerability pattern with known exploitation methods
- 0.7-0.8: Suspicious pattern requiring specific conditions to exploit
- Below 0.7: Don't report (too speculative)

FINAL REMINDER:
Focus on HIGH and MEDIUM findings only. Better to miss some theoretical issues than flood the report with false positives. Each finding should be something a security engineer would confidently raise in a PR review.

FALSE POSITIVE FILTERING:

> You do not need to run commands to reproduce the vulnerability, just read the code to determine if it is a real vulnerability. Do not use the bash tool or write to any files.
>
> HARD EXCLUSIONS - Automatically exclude findings matching these patterns:
> 1. Denial of Service (DOS) vulnerabilities or resource exhaustion attacks.
> 2. Secrets or credentials stored on disk if they are otherwise secured.
> 3. Rate limiting concerns or service overload scenarios.
> 4. Memory consumption or CPU exhaustion issues.
> 5. Lack of input validation on non-security-critical fields without proven security impact.
> 6. Input sanitization concerns for GitHub Action workflows unless they are clearly triggerable via untrusted input.
> 7. A lack of hardening measures. Code is not expected to implement all security best practices, only flag concrete vulnerabilities.
> 8. Race conditions or timing attacks that are theoretical rather than practical issues. Only report a race condition if it is concretely problematic.
> 9. Vulnerabilities related to outdated third-party libraries. These are managed separately and should not be reported here.
> 10. Memory safety issues such as buffer overflows or use-after-free-vulnerabilities are impossible in rust. Do not report memory safety issues in rust or any other memory safe languages.
> 11. Files that are only unit tests or only used as part of running tests.
> 12. Log spoofing concerns. Outputting un-sanitized user input to logs is not a vulnerability.
> 13. SSRF vulnerabilities that only control the path. SSRF is only a concern if it can control the host or protocol.
> 14. Including user-controlled content in AI system prompts is not a vulnerability.
> 15. Regex injection. Injecting untrusted content into a regex is not a vulnerability.
> 16. Regex DOS concerns.
> 16. Insecure documentation. Do not report any findings in documentation files such as markdown files.
> 17. A lack of audit logs is not a vulnerability.
>
> PRECEDENTS -
> 1. Logging high value secrets in plaintext is a vulnerability. Logging URLs is assumed to be safe.
> 2. UUIDs can be assumed to be unguessable and do not need to be validated.
> 3. Environment variables and CLI flags are trusted values. Attackers are generally not able to modify them in a secure environment. Any attack that relies on controlling an environment variable is invalid.
> 4. Resource management issues such as memory or file descriptor leaks are not valid.
> 5. Subtle or low impact web vulnerabilities such as tabnabbing, XS-Leaks, prototype pollution, and open redirects should not be reported unless they are extremely high confidence.
> 6. React and Angular are generally secure against XSS. These frameworks do not need to sanitize or escape user input unless it is using dangerouslySetInnerHTML, bypassSecurityTrustHtml, or similar methods. Do not report XSS vulnerabilities in React or Angular components or tsx files unless they are using unsafe methods.
> 7. Most vulnerabilities in github action workflows are not exploitable in practice. Before validating a github action workflow vulnerability ensure it is concrete and has a very specific attack path.
> 8. A lack of permission checking or authentication in client-side JS/TS code is not a vulnerability. Client-side code is not trusted and does not need to implement these checks, they are handled on the server-side. The same applies to all flows that send untrusted data to the backend, the backend is responsible for validating and sanitizing all inputs.
> 9. Only include MEDIUM findings if they are obvious and concrete issues.
> 10. Most vulnerabilities in ipython notebooks (*.ipynb files) are not exploitable in practice. Before validating a notebook vulnerability ensure it is concrete and has a very specific attack path where untrusted input can trigger the vulnerability.
> 11. Logging non-PII data is not a vulnerability even if the data may be sensitive. Only report logging vulnerabilities if they expose sensitive information such as secrets, passwords, or personally identifiable information (PII).
> 12. Command injection vulnerabilities in shell scripts are generally not exploitable in practice since shell scripts generally do not run with untrusted user input. Only report command injection vulnerabilities in shell scripts if they are concrete and have a very specific attack path for untrusted input.
>
> SIGNAL QUALITY CRITERIA - For remaining findings, assess:
> 1. Is there a concrete, exploitable vulnerability with a clear attack path?
> 2. Does this represent a real security risk vs theoretical best practice?
> 3. Are there specific code locations and reproduction steps?
> 4. Would this finding be actionable for a security team?
>
> For each finding, assign a confidence score from 1-10:
> - 1-3: Low confidence, likely false positive or noise
> - 4-6: Medium confidence, needs investigation
> - 7-10: High confidence, likely true vulnerability

START ANALYSIS:

Begin your analysis now. Do this in 3 steps:

1. Use a sub-task to identify vulnerabilities. Use the repository exploration tools to understand the codebase context, then analyze the PR changes for security implications. In the prompt for this sub-task, include all of the above.
2. Then for each vulnerability identified by the above sub-task, create a new sub-task to filter out false-positives. Launch these sub-tasks as parallel sub-tasks. In the prompt for these sub-tasks, include everything in the "FALSE POSITIVE FILTERING" instructions.
3. Filter out any vulnerabilities where the sub-task reported a confidence less than 8.

Your final reply must contain the markdown report and nothing else.

## 🤖 Claude *(04:24:26)*


## 🤖 Claude *(04:24:41)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Identify security vulns in migration",
  "prompt": "You are a senior security engineer conducting a focused security review of a single new file added to a branch.\n\nThe new file is a Supabase SQL migration:\n`supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql`\n\nRead that file. Also read these for context (the precedent it clones + the SOP + the edge function it schedules):\n- `supabase/migrations/20260603230000_nurture_advance_cron.sql` (the canonical precedent it mirrors)\n- `supabase/migrations/20260601050000_embed_trigger_vault_key.sql` (the Vault-key read pattern)\n- `supabase/functions/autopilot-cadence-cron/index.ts` (the function the cron POSTs to)\n- `docs/processes/autopilot-cron-identity.md` (the SOP)\n\nOBJECTIVE: identify HIGH-CONFIDENCE security vulnerabilities NEWLY introduced by this migration only. Focus ONLY on security implications of this change. Do not comment on pre-existing concerns.\n\nCRITICAL INSTRUCTIONS:\n1. MINIMIZE FALSE POSITIVES: Only flag issues where you're >80% confident of actual exploitability\n2. AVOID NOISE: Skip theoretical issues, style concerns, or low-impact findings\n3. FOCUS ON IMPACT: unauthorized access, data breach, privilege escalation, system compromise\n\nSECURITY CATEGORIES: SQL injection, command injection, auth bypass, privilege escalation, JWT flaws, hardcoded secrets, weak crypto, insecure deserialization, data exposure, SSRF (host/protocol control only), path traversal.\n\nEXCLUSIONS: Do NOT report DoS, secrets-at-rest on disk, rate limiting, resource exhaustion, lack of hardening, theoretical races, outdated deps, log spoofing, findings in markdown/docs files.\n\nKey things to verify for this migration specifically:\n- It schedules a pg_cron job (`cron.schedule`) that calls `net.http_post` to an edge function, with an Authorization Bearer pulled from Vault (`vault.decrypted_secrets` name='sb_secret_key').\n- Is the Bearer hardcoded anywhere? (No \u2014 it should be a Vault lookup.)\n- Is the scheduled SQL injectable? (It's a static literal string, no user input.)\n- Does scheduling this cron create a privilege-escalation or cross-tenant path? (The function it calls self-checks `Authorization === Bearer SB_SECRET_KEY` and derives user_id from the DB row, never the request body \u2014 per OTD-VA-008.)\n- Does the migration weaken any RLS, grant, or REVOKE?\n\nFor each finding output: file, line number, severity (HIGH/MEDIUM/LOW), category, description, exploit scenario, fix recommendation, and a confidence score 1-10.\n\nIf you find NO high-confidence vulnerabilities, say so explicitly. Do not use the bash tool to reproduce; read the code. Do not write any files.",
  "subagent_type": "general-purpose"
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'I have all five files. Let me analyze the new migration line-by-line against the precedent, the function it schedules, and the SOP.\n\n## Analysis\n\n**What the migration does:**\n1. `DO $$ ... PERFORM cron.unschedule(\'autopilot-cadence\') ... EXCEPTION WHEN OTHERS THEN NULL` — idempotent unschedule (lines 21-26)\n2. `SELECT cron.schedule(\'autopilot-cadence\', \'*/15 * * * *\', $cron$ ... $cron$)` — schedules a job that runs `net.http_post` (lines 28-41)\n3. The POST body is the static literal `\'{}\'::jsonb`, URL is a static literal, and the `Authorization` Bearer is built at run time from `vault.decrypted_secrets WHERE name = \'sb_secret_key\'` (lines 32-39)\n\n**Security-relevant checks:**\n\n- **Hardcoded secret:** None. The Bearer is a Vault lookup (line 36), byte-identical to the precedent (`20260603230000` line 28) and the Vault-key pattern (`20260601050000` lines 28-44). The project ref `bcyvddsykvehvpwstlfa` in the URL is not a secret — it\'s the public Supabase project ref already present in every migration and the `VITE_SUPABASE_URL`. PASS.\n\n- **SQL injection:** The scheduled `$cron$` body is a static literal with zero interpolation of user/runtime input. The `net.http_post` args (`url`, `headers`, `body`) are all constant expressions or a Vault subquery — no concatenation of attacker-controlled data. PASS.\n\n- **SSRF (host/protocol control):** The URL is a hardcoded HTTPS literal to the project\'s own Supabase functions host. No runtime control of host or protocol. PASS.\n\n- **Auth bypass / privilege escalation / cross-tenant:** Scheduling this cron does not itself create a privilege path. The function it calls (`autopilot-cadence-cron`) self-checks `Authorization === Bearer ${serviceKey}` and returns 403 otherwise (index.ts line 26), and derives `user_id` from the DB row (`autopilot_plans.user_id`, lines 33-42, 52), never from the request body — matching OTD-VA-008 in the SOP. The cron presents the same Vault `sb_secret_key` the function expects. No new escalation surface is introduced by the schedule itself. PASS.\n\n- **RLS / GRANT / REVOKE weakening:** The migration contains no `GRANT`, `REVOKE`, `ALTER ... ENABLE/DISABLE ROW LEVEL SECURITY`, or policy change. It only schedules a cron job. Nothing is weakened. PASS.\n\n- **Vault exposure:** The decrypted secret is read into the request header inside Postgres at run time and sent over HTTPS to the project\'s own host. This is the established, reviewed pattern (precedent + embed trigger). The secret is not logged, returned, or written to a table. No new exposure. PASS.\n\n- **`EXCEPTION WHEN OTHERS THEN NULL`:** Scoped to the one-time `cron.unschedule` in the `DO` block (lines 24-25) — it only swallows "job doesn\'t exist on fresh env." It does not wrap the `net.http_post` and has no security consequence. PASS.\n\nOne note worth recording (not a vulnerability): the migration hardcodes the cron schedule and Vault read, but the `net.http_post` is fire-and-forget; there is no `verify_jwt` or RLS concern at the migration layer because the gate lives in the edge function, which I verified enforces the 403. This is consistent with the precedent and the SOP\'s "Identity resolution order."\n\n## Verdict\n\n**No high-confidence security vulnerabilities were found in this migration.**\n\nThe change is a faithful clone of the reviewed `nurture-advance` precedent (`20260603230000`), differing only in the job name (`autopilot-cadence`), the target function URL path (`autopilot-cadence-cron`), and explanatory comments. Concretely:\n\n- No hardcoded secret — the Bearer is a run-time `vault.decrypted_secrets` lookup (line 36), identical to both reference patterns.\n- No SQL/command injection — the scheduled body is a static literal string with no runtime/user input interpolated (lines 31-40).\n- No SSRF — URL host and protocol are a hardcoded HTTPS literal to the project\'s own Supabase host (line 33).\n- No auth bypass / privilege escalation / cross-tenant path created by scheduling — the invoked function `autopilot-cadence-cron` independently enforces `Bearer ${SB_SECRET_KEY}` → 403 (index.ts:26) and takes `user_id` from the trusted `autopilot_plans` row, never the request (index.ts:33-52), consistent with OTD-VA-008.\n- No RLS/GRANT/REVOKE/policy is added, removed, or weakened — the file only calls `cron.unschedule` + `cron.schedule`.\n- The `EXCEPTION WHEN OTHERS THEN NULL` is scoped solely to the idempotent unschedule of a possibly-nonexistent job (lines 24-25); it has no security impact.\n\nFiles reviewed:\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql` (target)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603230000_nurture_advance_cron.sql` (precedent — confirmed near-verbatim match)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601050000_embed_trigger_vault_key.sql` (Vault-read pattern — confirmed identical idiom)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-cadence-cron/index.ts` (confirmed in-function 403 service-role gate + DB-derived user_id)\n- `/home/gcrUX/htdocs/constellation-orchestra/docs/processes/autopilot-cron-identity.md` (SOP — confirms the intended identity model holds)'}, {'type': 'text', 'text': "agentId: a3149af88084452ca (use SendMessage with to: 'a3149af88084452ca' to continue this agent)\n<usage>subagent_tokens: 79743\ntool_uses: 5\nduration_ms: 34953</usage>"}]
> ```

## 🤖 Claude *(04:25:23)*


## 🤖 Claude *(04:25:31)*

Based on the security review sub-task analysis, here is the final report:

# Security Review — `supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql`

**No high-confidence security vulnerabilities found. Verdict: SAFE.**

The change is a faithful clone of the already-reviewed `nurture-advance` precedent (`20260603230000`), differing only in the job name (`autopilot-cadence`), the target function URL path (`autopilot-cadence-cron`), and explanatory comments.

| Check | Result |
|---|---|
| **Hardcoded secret** | ✅ None — Bearer is a run-time `vault.decrypted_secrets` lookup (`name='sb_secret_key'`, line 36), identical to both reference patterns. Project ref in URL is the public Supabase ref, not a secret. |
| **SQL / command injection** | ✅ None — the scheduled `$cron$` body is a static literal with zero interpolation of user/runtime input. |
| **SSRF (host/protocol)** | ✅ None — URL host+protocol are a hardcoded HTTPS literal to the project's own Supabase host. |
| **Auth bypass / privilege escalation / cross-tenant** | ✅ None introduced — the invoked `autopilot-cadence-cron` independently enforces `Bearer ${SB_SECRET_KEY}` → 403 (`index.ts:26`) and derives `user_id` from the trusted `autopilot_plans` row, never the request body (OTD-VA-008). |
| **RLS / GRANT / REVOKE weakening** | ✅ None — the file only calls `cron.unschedule` + `cron.schedule`; no policy/grant change. |
| **`EXCEPTION WHEN OTHERS THEN NULL`** | ✅ Scoped solely to the idempotent unschedule of a possibly-nonexistent job (lines 24-25); no security impact. |

Files cross-referenced: the target migration, the `nurture-advance` precedent (near-verbatim match confirmed), the Vault-key read pattern (`20260601050000`), the `autopilot-cadence-cron` function (in-function 403 + DB-derived user_id confirmed), and the SOP `autopilot-cron-identity.md`.

No findings reached the confidence-≥8 threshold; nothing to filter or report.

## 👤 User *(04:27:15)*

ótimo continue

## 🤖 Claude *(04:28:55)*


## 🤖 Claude *(04:28:57)*

GO recebido. Vou **completar a ativação** aplicando o heartbeat `pg_cron` (seguro/no-op até um plano recorrente ser ativado, e reversível via `cron.unschedule`), verificar materialmente, e então seguir para o último item autônomo do autopilot (FR-VA-018: `fetch-trends`→pauta) com o rigor ultracode.

Primeiro, estado das migrations e acesso ao DB para verificar o `cron.job` depois.

## 🤖 Claude *(04:29:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== Migrations pendentes (local vs remote) ===\"\nnpx supabase migration list 2>&1 | tail -25\necho \"\"\necho \"=== Conn string de DB no .env? (para verificar cron.job) ===\"\ngrep -cE \"^SUPABASE_DB_URL=|^DATABASE_URL=|^DB_URL=|postgres://|postgresql://\" .env 2>/dev/null && echo \"(h\u00e1 conn string)\" || echo \"(sem conn string direta no .env)\"\necho \"\"\necho \"=== aios-sql-bridge dispon\u00edvel? ===\"\nls -d supabase/functions/aios-sql-bridge 2>/dev/null && echo \"(edge fn existe)\" || echo \"(sem aios-sql-bridge edge fn)\"",
  "description": "Migration state + DB access for cron.job verification"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Migrations pendentes (local vs remote) ===
>    20260606210000 | 20260606210000 | 2026-06-06 21:00:00 
>    20260606220000 | 20260606220000 | 2026-06-06 22:00:00 
>    20260606230000 | 20260606230000 | 2026-06-06 23:00:00 
>    20260610010000 | 20260610010000 | 2026-06-10 01:00:00 
>    20260612021108 | 20260612021108 | 2026-06-12 02:11:08 
>    20260612022953 | 20260612022953 | 2026-06-12 02:29:53 
>    20260615140000 | 20260615140000 | 2026-06-15 14:00:00 
>    20260615160000 | 20260615160000 | 2026-06-15 16:00:00 
>    20260615170000 | 20260615170000 | 2026-06-15 17:00:00 
>    20260615180000 | 20260615180000 | 2026-06-15 18:00:00 
>    20260615190000 | 20260615190000 | 2026-06-15 19:00:00 
>    20260615200000 | 20260615200000 | 2026-06-15 20:00:00 
>    20260619140000 | 20260619140000 | 2026-06-19 14:00:00 
>    20260620120000 | 20260620120000 | 2026-06-20 12:00:00 
>    20260620120100 | 20260620120100 | 2026-06-20 12:01:00 
>    20260620120200 | 20260620120200 | 2026-06-20 12:02:00 
>    20260620120300 | 20260620120300 | 2026-06-20 12:03:00 
>    20260622030000 | 20260622030000 | 2026-06-22 03:00:00 
>    20260622030100 | 20260622030100 | 2026-06-22 03:01:00 
>    20260622040000 | 20260622040000 | 2026-06-22 04:00:00 
>    20260622210000 | 20260622210000 | 2026-06-22 21:00:00 
>    20260623040000 |                | 2026-06-23 04:00:00 
> 
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> 
> === Conn string de DB no .env? (para verificar cron.job) ===
> 0
> (sem conn string direta no .env)
> 
> === aios-sql-bridge disponível? ===
> supabase/functions/aios-sql-bridge
> (edge fn existe)
> ```

## 🤖 Claude *(04:29:14)*


## 🤖 Claude *(04:29:15)*

Só a `20260623040000` está local-sem-remote — `db push` aplica apenas ela. `aios-sql-bridge` existe para verificar o `cron.job` depois. Aplicando o heartbeat:

## 🤖 Claude *(04:29:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"y\" | npx supabase db push 2>&1 | tail -30",
  "description": "Apply pg_cron heartbeat migration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Initialising login role...
> Connecting to remote database...
> Do you want to push these migrations to the remote database?
>  • 20260623040000_viral_autopilot_cadence_cron.sql
> 
>  [Y/n] y
> Applying migration 20260623040000_viral_autopilot_cadence_cron.sql...
> Finished supabase db push.
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(04:29:22)*


## 🤖 Claude *(04:29:23)*

Migration aplicada. Agora a prova material: o job `autopilot-cadence` registrado em `cron.job`. Vou ler o contrato do `aios-sql-bridge` para consultar o schema `cron`.

## 🤖 Claude *(04:29:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsed -n '1,80p' supabase/functions/aios-sql-bridge/index.ts",
  "description": "Read aios-sql-bridge contract"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> // aios-sql-bridge — SSP-01 OE02
> // Read-only SQL bridge for the AIOS. Filter Objects contract; no raw SQL accepted.
> // Auth: JWT required + admin role gate. Audit: usage_tracking + infra_health_logs.
> 
> import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
> import {
>   WHITELIST,
>   ALLOWED_OPS,
>   FORBIDDEN_COLUMN_PATTERNS,
>   MAX_LIMIT,
>   MAX_OFFSET,
>   DEFAULT_LIMIT,
>   DAILY_QUOTA,
>   type AllowedTable,
>   type FilterOp,
> } from './whitelist.ts';
> 
> const corsHeaders = {
>   'Access-Control-Allow-Origin': '*',
>   'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
>   'Access-Control-Allow-Methods': 'POST, OPTIONS',
> };
> 
> const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
> const serviceRoleKey = (Deno.env.get('SB_SECRET_KEY') ?? Deno.env.get('SUPABASE_SERVICE_ROLE_KEY'))!;
> const admin = createClient(supabaseUrl, serviceRoleKey);
> 
> interface Filter {
>   column: string;
>   op: FilterOp;
>   value: unknown;
> }
> 
> interface OrderClause {
>   column: string;
>   ascending?: boolean;
> }
> 
> interface BridgeRequest {
>   table: AllowedTable;
>   select?: string;
>   filters?: Filter[];
>   order?: OrderClause;
>   limit?: number;
>   offset?: number;
> }
> 
> interface BridgeResponse {
>   rows: unknown[];
>   rowCount: number;
>   table: string;
>   queryHash: string;
>   executedAt: string;
>   durationMs: number;
> }
> 
> function json(body: unknown, status = 200) {
>   return new Response(JSON.stringify(body), {
>     status,
>     headers: { ...corsHeaders, 'Content-Type': 'application/json' },
>   });
> }
> 
> function isForbidden(column: string): boolean {
>   return FORBIDDEN_COLUMN_PATTERNS.some((re) => re.test(column));
> }
> 
> function validateSelectClause(select: string, allowed: readonly string[]): string | null {
>   if (select.trim() === '*') return null;
>   const cols = select
>     .split(',')
>     .map((c) => c.trim())
>     .filter(Boolean);
>   for (const c of cols) {
>     if (isForbidden(c)) return `Forbidden column in select: ${c}`;
>     if (!allowed.includes(c)) return `Column not whitelisted for this table: ${c}`;
>   }
>   return null;
> }
> ```

## 🤖 Claude *(04:29:39)*


## 🤖 Claude *(04:29:40)*

`aios-sql-bridge` é read-only sobre PostREST (whitelist) — não alcança o schema `cron`. Vou usar a Management API (PAT em `~/.supabase/access-token`) para consultar `cron.job` diretamente. O `db push` terminou sem erro (o `cron.schedule` rodou dentro da migration), mas quero a linha física.

## 🤖 Claude *(04:29:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nREF=\"bcyvddsykvehvpwstlfa\"\nPAT=$(cat ~/.supabase/access-token 2>/dev/null)\nif [ -z \"$PAT\" ]; then echo \"(sem PAT em ~/.supabase/access-token)\"; ls -la ~/.supabase/ 2>/dev/null; exit 0; fi\necho \"=== cron.job: autopilot-cadence registrado? (Management API) ===\"\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $PAT\" -H \"Content-Type: application/json\" \\\n  -d '{\"query\":\"SELECT jobid, jobname, schedule, active, command FROM cron.job WHERE jobname = '\"'\"'autopilot-cadence'\"'\"';\"}' | python3 -m json.tool 2>/dev/null",
  "description": "Verify cron.job via Management API"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === cron.job: autopilot-cadence registrado? (Management API) ===
> [
>     {
>         "jobid": 3,
>         "jobname": "autopilot-cadence",
>         "schedule": "*/15 * * * *",
>         "active": true,
>         "command": "\n  SELECT net.http_post(\n    url := 'https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/autopilot-cadence-cron',\n    headers := jsonb_build_object(\n      'Content-Type', 'application/json',\n      'Authorization', 'Bearer ' || (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'sb_secret_key' LIMIT 1)\n    ),\n    body := '{}'::jsonb\n  );\n  "
>     }
> ]
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-22 - agent-afbda1deee15bc84c]]
> * **Próxima Sessão**: [[2026-06-23 - Resolver CF WAF e secrets para ação Sovereign]]
%% --- TIMELINE END --- %%

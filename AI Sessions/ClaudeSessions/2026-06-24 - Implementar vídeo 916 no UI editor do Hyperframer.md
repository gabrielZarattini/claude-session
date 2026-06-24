# Implementar vídeo 9:16 no UI editor do Hyperframer
**Date:** 2026-06-24 | **Session ID:** `e8d1ce6a-96c0-474b-ab24-c66705a25d2e`

---

## 👤 User *(02:36:49)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(02:36:49)*

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


## 🤖 Claude *(02:36:54)*


## 🤖 Claude *(02:36:55)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with parallel pre-flight checks.

## 🤖 Claude *(02:36:55)*


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
> f6c8914 chore(sprint): v6.48.0 — Viral Autopilot ativado + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR
> a7f3f95 docs(handoff): seal Viral Autopilot ativado + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR
> 15dab4d docs(readme): v6.48.0 — Viral Autopilot ativado + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR
> 06c59c0 feat(security): paridade pt-BR no Cyber-Sentinel (OTD-VA-018-SENTINEL-PTBR)
> 3488005 fix(security): assina state OAuth (HMAC) + verifica X-Hub-Signature-256 do webhook IG
> 489dd61 feat(viral-autopilot): FR-VA-018 ângulo informado por trends + gate de fonte
> 139fc3f feat(viral-autopilot): ativa cadência pg_cron (heartbeat recorrente FR-VA-005)
> ```

## 🤖 Claude *(02:36:56)*


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
> (Bash completed with no output)
> ```

## 🤖 Claude *(02:36:56)*


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
> (Bash completed with no output)
> ```

## 🤖 Claude *(02:36:57)*


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

## 🤖 Claude *(02:36:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker container health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 6 days (healthy)
> mcorch_claude_mem: Up 8 days (healthy)
> mcorch_chroma: Up 8 days (healthy)
> ---
> mega-brain-dashboard: Up 8 days
> mega-brain-webhook: Up 8 days (healthy)
> mega-brain-daemon: Up 8 days (healthy)
> ```

## 🤖 Claude *(02:36:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat; echo \" (exit $?)\"",
  "description": "Chroma API v2 heartbeat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1782268619832831873} (exit 0)
> ```

## 🤖 Claude *(02:37:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---scratch---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"",
  "description": "BoK suites + scratch check"
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
> ⚠️ scratch/ has files
> ```

## 🤖 Claude *(02:37:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l HANDOFF.md",
  "description": "HANDOFF total lines"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 8253 HANDOFF.md
> ```

## 🤖 Claude *(02:37:05)*


## 🤖 Claude *(02:37:05)*

Clean worktree, zero TS errors, all containers healthy. Now reading HANDOFF (head + tail) and context files in parallel.

## 🤖 Claude *(02:37:06)*


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
> 14	## Session Seal — Viral Autopilot ATIVADO (1º ciclo pago + pg_cron) + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR (2026-06-23)
> 15	
> 16	`/handson` → "vamos com os próximos passos" → "continue" (×N) sob **ultracode**. Três arcos completos, verificados e deployados, depois selados a pedido (`/handoff`). Arco: **(1)** ativação do Viral Autopilot (1º ciclo PAGO real + heartbeat pg_cron) → **(2)** FR-VA-018 ângulo informado por trends (com revisão adversarial que pegou um MEDIUM de injection pt-BR cross-tenant, hardened) → **(3)** os 2 achados de segurança da auditoria per-user (state OAuth HMAC + assinatura do webhook IG) → **(4)** paridade pt-BR no Cyber-Sentinel (OTD-VA-018, o gap system-wide que a revisão da Fatia FR-VA-018 expôs). Surpresa material decisiva: `orchestrate-content` resolve produto por **`external_id`** (não o UUID) — pego antes de queimar o 1º ciclo pago.
> 17	
> 18	**O que foi entregue (6 commits granulares + handoff):**
> 19	1. **Viral Autopilot ATIVADO (`139fc3f`).** Migration `20260623040000_viral_autopilot_cadence_cron.sql` (clone verbatim do `nurture-advance`, Bearer do Vault `sb_secret_key`) → `cron.job` jobid 3 `autopilot-cadence` `*/15` `active` (verificado Management API). **1º ciclo PAGO real:** plano mínimo do User 0 (`640b3b67`, Roborock `MLB27834876` × WP+LinkedIn × ab=1) → `autopilot-cadence-cron` disparado 1× → cycle `947ef8b5` `completed`, débito 22 / refund 2 (`autopilot_refund` crédito POSITIVO, anti-mint OK), saldo **5096→5076** (delta exato −20 = 2 sub-runs×10), 2 `pipeline_runs` product-aware `done`, telemetria healthy.
> 20	2. **FR-VA-018 ângulo informado por trends (`489dd61`).** `autopilot-run` lê `vm_trends` (catálogo GLOBAL minerado = fonte não-confiável) → gate fail-closed `sanitizeTrendTitle` (whitelist de charset destrói URLs/markdown/tags/aspas + `TREND_OVERRIDE_RE` rejeita verbos de override pt-BR/en) → sentinel genérico → trend entra como DADO inerte (`tema em alta: …`). Revisão adversarial `wf_6cc97c75` pegou MEDIUM (conf 8): o sentinel compartilhado era English-only → injection pt-BR semeada num trend global dirigia o LLM cross-tenant. Fix + smoke material (3 payloads do red-team rejeitados, 0 resíduo). SOP `trend-informed-angle-sanitization.md`.
> 21	3. **Segurança social-auth (`3488005`).** (a) `social-auth-callback` confiava cego no `userId` de um `state` base64 **não assinado** (redirect sem JWT) → account-linking cross-tenant; agora `social-auth-init` **assina (HMAC-SHA256, `_shared/oauth-state.ts`)** e o callback rejeita forjado/tampered/**expirado** (janela ts 10 min) antes de escrever `social_accounts`. (b) `instagram-webhook` sem verificação de assinatura → spoofing; agora valida `X-Hub-Signature-256` contra `INSTAGRAM_APP_SECRET` fail-closed 403. Revisão adversarial 2-lente safe (1 LOW `ts` corrigido) · 8/8 gates materiais · `/security-review` SAFE.
> 22	4. **Paridade pt-BR no Cyber-Sentinel (`06c59c0`, OTD-VA-018-SENTINEL-PTBR).** 7 famílias pt-BR (f1-f7) espelham as inglesas (mesmo threshold score≥2). **0 FP real** contra 58 amostras (loop adversarial `wf_0459e1c1` FP-hunter+bypass-hunter → tunei f3/f4/f5 removendo `segredos`/`desenvolvedor`/`livre` que pegavam tropes legítimas). Live: injection encadeada pt-BR → `orchestrate-content` 403 `score=2`; inglês sem regressão. Limite por design (=inglês): single-intent + beyond-triage passam.
> 23	
> 24	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (GO via AskUserQuestion p/ 1º ciclo pago + direção; `/security-review` mecânico independente + 4 workflows adversariais) · Owner=Sovereign (blast radius = carteira do User 0 gasta autonomamente + isolamento cross-tenant social/conteúdo).
> 25	
> 26	| Verificação (material) | Resultado |
> 27	|---|---|
> 28	| 1º ciclo pago Autopilot | ✅ cycle `947ef8b5` completed · −22/+2 ledger · saldo 5096→5076 · 2 sub-runs `done` |
> 29	| pg_cron heartbeat | ✅ `cron.job` jobid 3 `autopilot-cadence */15` `active` (Management API) · `/security-review` SAFE |
> 30	| FR-VA-018 hardened | ✅ deploy 71.11kB · red-team 3/3 payloads rejeitados · 0 resíduo |
> 31	| Segurança social-auth | ✅ 8/8 gates (forjado/expirado/tampered/legacy→reject · sem/errada assinatura→403) |
> 32	| Sentinel pt-BR | ✅ 0 FP em 58 amostras · live 403 `score=2` pt-BR · inglês double-match 403 (sem regressão) |
> 33	| Saldo final User 0 | ✅ 5076 (1º ciclo −20; testes prepaid/dry_run não cobraram) |
> 34	| tsc · gitleaks | ✅ 0 erros · gitleaks limpo nos 6 commits |
> 35	| Handoff node | `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` (embedded 768d via trigger) |
> 36	
> 37	### Survival Laws Self-audit
> 38	```
> 39	Law 1 (Materiality): ✅ Toda claim provada NESTE arco — ciclo via SELECT (947ef8b5/ledger/saldo); pg_cron via cron.job Management API; FR-VA-018 + sentinel via smoke contra o código REAL (lexicalScore importado, zero drift) + live 403; social-auth via 8 gates curl. Pego material: produto por external_id (não UUID) antes de gastar; o gap English-only do sentinel (red-team). Fase 5c mecânica abaixo.
> 40	Law 2 (Process): ✅ SOP `trend-informed-angle-sanitization.md` (FR-VA-018, untrusted-source gate) ANTES de confiar no fluxo; os 2 fixes de segurança são bug-fixes em features documentadas (Social OAuth ADRs / IG webhook) → isentos de BoK gate; OTD-VA-018 documentada+fechada no SOP.
> 41	Law 3 (Pruning): ✅ Sessão MUITO densa (3 arcos + 4 workflows) sob "continue" repetido; usei a janela até o ponto de seal a pedido explícito do Sovereign (/handoff). Corpora/harness de teste em /tmp (referência por path, não recarregados).
> 42	Law 4 (ORO): ✅ Triplet declarado por arco; GO explícito do Sovereign p/ o 1º ciclo PAGO (gasto real) e p/ a direção (sentinel pt-BR escolhido via AskUserQuestion); /security-review + 4 workflows adversariais como Reviewer independente.
> 43	```
> 44	
> 45	## Session Seal — Per-user 100% (env = só infra) + CF WP unblock + sweep per-user FECHADO (2026-06-22)
> 46	
> 47	`/handson` → "resolver o CF WAF + secrets, depois os próximos passos". Arco: **(1)** desbloqueio material do CF no `/wp-json` → **(2)** SOP per-user WP↔CF → **(3)** fix do token vazado `aios-chat-gateway` → **(4)** auditoria de prontidão per-user (workflow) → **(5)** diretiva Sovereign **"env = só infra, todo provider key per-user BYOK"** → migração de 27 fns + #3 fetch-trends. Surpresa material decisiva: o componente de skip que faltava no Cloudflare era **"Nível de segurança"** (challenge por reputação de IP de **datacenter**, não bot/UA) — diagnosticado lendo o **Security→Events** (a regra Skip já disparava `Ignorar`, mas o `Nível de segurança` desafiava por cima). O teste E2E "falhou bonito" (OpenRouter respondeu 404 de modelo + `user_id` → **provou** que a chave per-user autenticou).
> 48	
> 49	**O que foi entregue (6 commits granulares):**
> 50	1. **CF WP unblock (`ação Sovereign` + verificação).** Secrets `WP_PUBLISH_SECRET`/`_HOST` provisionados + regra CF Skip header-gated com **Nível de segurança** marcado → `curl` com header sai do 403 (200 + JSON real do WP), sem header continua 403 (mundo barrado). E2E `publish-wordpress` → `{"success":true,"post_id":18}` (rascunho de teste deletado). SOP `wordpress-cf-publish-unblock.md` atualizada com o achado + diagnóstico via Events; novo SOP `wordpress-cf-per-user-publish.md` (multi-tenant, Lei 2).
> 51	2. **`aios-chat-gateway` token vazado (`ef921ce`).** Literal hardcoded removido + fail-closed 501 + telemetria. Rotação = decisão consciente do Owner (diferida — repo privado, sem público, sem outros users). Secret setado com valor atual (sem rotacionar).
> 52	3. **Auditoria per-user (workflow `wf_102ef5ac`, 49 fns).** Ledger: 30 per-user · 11 fallback-ok · 4 remediadas. Achados de segurança bônus (não-per-user, próxima sessão): `social-auth-callback` state sem HMAC (cross-tenant), `instagram-webhook` sem signature.
> 53	4. **Migração env=só-infra (`4583519`+`432fa01`).** Removido `|| Deno.env.get(<provider>)` de **25 fns user-facing** (47 ocorrências) → per-user PURO fail-closed. 2 fns de sistema (`embed-mcorch-node` NUCLEAR + `search-constellation`) → `MESH_EMBED_OPENROUTER_KEY`/`MESH_EMBED_GEMINI_KEY` dedicadas. BYOK do User 0 seedado do `.env` (higgsfield_api_key estava null). 27 fns deployadas 0 falhas.
> 54	5. **#3 fetch-trends per-user (`f6734e9`).** Migration `20260622210000` adiciona coluna cifrada `rapidapi_key` (espelha template firecrawl verbatim; `apify_token` já existia) + edge fn per-user fail-closed 402 + UI Settings (Apify/RapidAPI) + seed User 0. `/security-review` SAFE.
> 55	
> 56	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (GOs via AskUserQuestion) + `/security-review` independente 2× · Owner=Sovereign (blast radius = pipeline de conteúdo do User 0 + carteira + isolamento multi-tenant; rotação de secrets vazados diferida conscientemente).
> 57	
> 58	| Verificação (material) | Resultado |
> 59	|---|---|
> 60	| CF WP unblock | ✅ curl com header 200 + JSON WP · sem header 403 · E2E `publish-wordpress` `post_id 18` |
> 61	| Migração per-user | ✅ 47 fallbacks removidos · 0 resíduo · 27 fns deployadas 0 falhas |
> 62	| Embedding pipeline pós-rename | ✅ `embed-mcorch-node` 200 `dims:768` (MESH_EMBED funciona) |
> 63	| Per-user E2E | ✅ openrouter-swarm: OpenRouter autenticou com chave per-user do User 0 |
> 64	| #3 fetch-trends fail-closed | ✅ throwaway sem key → 402 `trends_not_configured` (zero-cost) |
> 65	| Migration rapidapi_key | ✅ `db push` aplicada · coluna `••••`/null · `/security-review` SAFE |
> 66	| `/security-review` | ✅ SAFE 2× (migração CF host-gate prévia + migração rapidapi) |
> 67	| tsc · gitleaks | ✅ 0 erros · gitleaks limpo nos 6 commits |
> 68	| Handoff node | `4e57bf72-8cc0-4e1c-ae48-10d7f19b0dac` (embedded 768d) |
> 69	
> 70	### Survival Laws Self-audit
> 71	```
> ```

## 🤖 Claude *(02:37:07)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7853,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7853	ContentLibraryPage monetization flow:
> 7854	  Card (text, body contains mercadolivre.com.br)
> 7855	    └── DropdownMenu → "Monetizar Links ML"
> 7856	          → handleMonetizeLinks(item):
> 7857	               match(ML_URL_RE) → unique URLs
> 7858	               for url of unique:
> 7859	                 POST process-affiliate-link → affiliate_url
> 7860	                 body.split(url).join(affiliate_url)
> 7861	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7862	          → Badge 💰 ML (emerald) exibido após monetização
> 7863	```
> 7864	
> 7865	---
> 7866	
> 7867	## Pending Actions (Commercial Launch)
> 7868	
> 7869	### CRITICAL — Must complete before first client
> 7870	
> 7871	🎯. **[✅ ATIVADO + FR-VA-018 — 2026-06-23 · pendente só: mídia 9:16 (fase 2) + postback ML] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 7872	
> 7873	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 7874	
> 7875	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7876	
> 7877	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7878	
> 7879	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7880	
> 7881	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7882	
> 7883	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7884	
> 7885	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7886	
> 7887	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7888	
> 7889	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7890	
> 7891	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7892	
> 7893	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7894	   ```bash
> 7895	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7896	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7897	   ```
> 7898	
> 7899	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7900	
> 7901	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7902	
> 7903	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7904	
> 7905	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7906	
> 7907	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7908	
> 7909	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7910	
> 7911	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7912	
> 7913	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7914	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7915	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7916	
> 7917	### SOCIAL — Next steps
> 7918	
> 7919	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7920	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7921	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7922	
> 7923	### NON-CRITICAL
> 7924	
> 7925	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7926	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7927	- `browserslist` — ✅ updated (2026-04-26)
> 7928	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7929	
> 7930	### GITNEXUS MCP — Next steps
> 7931	
> 7932	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7933	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7934	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7935	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7936	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7937	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7938	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7939	
> 7940	### PHASE EPSILON — Next iterations
> 7941	
> 7942	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7943	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7944	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7945	
> 7946	### CORE — Next iterations
> 7947	
> 7948	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7949	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7950	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7951	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7952	
> 7953	### PHASE DELTA — Next iterations
> 7954	
> 7955	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7956	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7957	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7958	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7959	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7960	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7961	
> 7962	### USUÁRIO ZERO — Checklist de validação
> 7963	
> 7964	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7965	- ✅ Stripe sandbox secrets no vault
> 7966	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7967	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7968	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7969	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7970	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7971	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7972	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7973	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7974	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7975	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7976	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7977	
> 7978	---
> 7979	
> 7980	## Infrastructure
> 7981	
> 7982	| Service | Container | Port | Status |
> 7983	|---------|-----------|------|--------|
> 7984	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7985	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7986	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7987	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7988	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7989	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7990	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7991	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7992	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7993	
> 7994	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7995	
> 7996	```bash
> 7997	docker compose up -d
> 7998	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7999	```
> 8000	
> 8001	---
> 8002	
> 8003	## Security Model (Post-Go-Live)
> 8004	
> 8005	| Table | Isolation |
> 8006	|-------|-----------|
> 8007	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8008	| `mcorch_edges` | Same pattern |
> 8009	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8010	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8011	
> 8012	---
> 8013	
> 8014	## Billing Architecture
> 8015	
> 8016	| Decision | Value |
> 8017	|----------|-------|
> 8018	| Canonical billing ledger | `profiles.mco_balance` |
> 8019	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8020	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8021	| Orchestration cost | 10 mcoCoins/run |
> 8022	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8023	| Stripe | Sandbox keys active — swap to live before first client |
> 8024	
> 8025	---
> 8026	
> 8027	## GraphRAG State
> 8028	
> 8029	- **8954 total nodes** (verificado live 2026-06-23 via REST count=exact, autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8030	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8031	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8032	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8033	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8034	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8035	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8036	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8037	- HNSW cosine index operational
> 8038	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8039	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8040	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8041	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8042	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8043	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8044	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8045	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8046	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8047	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8048	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8049	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8050	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8051	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8052	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8053	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8054	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8055	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8056	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8057	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8058	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8059	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8060	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8061	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8062	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8063	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8064	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8065	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8066	
> 8067	### Embedding Model
> 8068	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8069	Schema: `vector(768)` — HNSW cosine index.
> 8070	
> 8071	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8072	Três camadas eliminam intervenção manual:
> 8073	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8074	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8075	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8076	
> 8077	### Comandos de manutenção da Mesh
> 8078	```bash
> 8079	# Verificar nós sem embedding (deveria retornar array vazio):
> 8080	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8081	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8082	
> 8083	# Backfill manual (Bun-native — requer .env):
> 8084	bun run scripts/backfill-embeddings.ts
> 8085	
> 8086	# Backfill de código-fonte nos nós AST:
> 8087	bun run scripts/backfill-node-content.ts
> 8088	
> 8089	# Re-sync AST completo:
> 8090	cd packages/gitnexus-core && npm run sync-mesh
> 8091	
> 8092	# Acompanhar re-ingesta pós-commit:
> 8093	tail -f /tmp/mcorch-ingest.log
> 8094	```
> 8095	
> 8096	---
> 8097	
> 8098	## Video Rescue Protocol
> 8099	
> 8100	When a video generation operation (Google Veo) times out or client disconnects:
> 8101	```bash
> 8102	# Via edge function (production):
> 8103	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8104	  -H "Authorization: Bearer <user_jwt>" \
> 8105	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8106	
> 8107	# Via local script (admin/debug):
> 8108	source .env && bun run rescue.ts <operation_id> <content_id>
> 8109	```
> 8110	
> 8111	---
> 8112	
> 8113	## Architecture Pillars
> 8114	
> 8115	| Layer | Implementation |
> 8116	|-------|---------------|
> 8117	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8118	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8119	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8120	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8121	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8122	
> 8123	---
> 8124	
> 8125	## Phase Delta — Architecture
> 8126	
> 8127	```
> 8128	OrchestrationPage (full-canvas, p-0)
> 8129	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8130	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8131	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8132	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8133	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8134	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8135	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8136	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8137	
> 8138	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8139	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8140	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8141	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8142	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8143	```
> 8144	
> 8145	### Canvas State Architecture (Hybrid)
> 8146	
> 8147	```
> 8148	User interaction → ReactFlow internal state (positions, drag)
> 8149	                         ↓ (debounced 600ms)
> 8150	                   localStorage (positions persist across refresh)
> 8151	                         ↑
> 8152	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8153	     ↓ (status changes sync to ReactFlow via useEffect)
> 8154	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8155	```
> 8156	
> 8157	## Key Files
> 8158	
> 8159	| Purpose | Path |
> 8160	|---------|------|
> 8161	| Architecture rules | `CLAUDE.md` |
> 8162	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8163	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8164	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8165	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8166	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8167	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8168	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8169	| **Node types** | `src/components/orchestrator/nodes/` |
> 8170	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8171	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8172	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8173	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8174	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8175	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8176	| Billing utilities | `src/lib/billing.ts` |
> 8177	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8178	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8179	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8180	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8181	| Video rescue (local) | `rescue.ts` |
> 8182	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8183	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8184	| Deploy harness | `scripts/harness-deploy.sh` |
> 8185	
> 8186	---
> 8187	
> 8188	## First Client Onboarding Checklist
> 8189	
> 8190	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8191	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8192	3. ~~Activate watchdog cron~~ ✅ Done
> 8193	4. ~~Deploy rescue-video function~~ ✅ Done
> 8194	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8195	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8196	7. Monitor `infra_health_logs` for first 24h.
> 8197	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8198	
> 8199	---
> 8200	
> 8201	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8202	
> 8203	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8204	
> 8205	| Action | Result |
> 8206	|--------|--------|
> 8207	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8208	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8209	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8210	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8211	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8212	
> 8213	| Commit | Conteúdo |
> 8214	|--------|----------|
> 8215	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8216	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8217	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8218	
> 8219	### Arquitetura Matrix Intelligence
> 8220	
> 8221	```
> 8222	ConstellationMatrix (Stabilized Engine)
> 8223	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8224	  └── NodeDetailsPanel (Tabbed Navigation)
> 8225	        ├── Tab Meta: Neighbor exploration + Net Context
> 8226	        ├── Tab Code: Source code preview (Supabase sync)
> 8227	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8228	
> 8229	useNodeIntelligence Hook:
> 8230	  - contentQuery: fetch nodes.content column
> 8231	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8232	  - state: isAnalyzing, analysisResult, progress
> 8233	```
> 8234	
> 8235	---
> 8236	
> 8237	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8238	
> 8239	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8240	
> 8241	| Action | Result |
> 8242	|--------|--------|
> 8243	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8244	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8245	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8246	
> 8247	**Output da análise (estruturado em pt-BR):**
> 8248	- Visão Geral — papel do módulo no sistema
> 8249	- Padrões Detectados — design patterns, antipatterns
> 8250	- Acoplamento & Dependências — análise In/Out-Degree
> 8251	- Recomendações — 1-3 ações priorizadas
> 8252	
> ```

## 🤖 Claude *(02:37:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null",
  "description": "List scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 23 23:27 ..
> ```

## 🤖 Claude *(02:37:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -80 || echo \"NO sprint-priorities.md\"",
  "description": "Sprint priorities"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (67.1KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/e8d1ce6a-96c0-474b-ab24-c66705a25d2e/tool-results/bn53ieh7t.txt
> 
> Preview (first 2KB):
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.48.0 — Viral Autopilot ATIVADO + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR (2026-06-23)** — `/handson` → "vamos com os próximos passos" → "continue" (×N) sob **ultracode** (4 workflows adversariais). 3 arcos. **(1) Viral Autopilot ATIVADO:** heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** (cycle `947ef8b5` completed, débito 22/refund 2, saldo 5096→5076, 2 sub-runs `done`) — GO Sovereign respeitado; trap material: produto resolve por `external_id`, não UUID. **(2) FR-VA-018** trend-informed angle: `autopilot-run` lê `vm_trends` (fonte global não-confiável) → gate `sanitizeTrendTitle` (whitelist destrói URLs/payloads + reject de verbos) → DADO inerte; red-team `wf_6cc97c75` pegou MEDIUM (sentinel English-only → injection pt-BR cross-tenant), hardened. **(3) Segurança social-auth** (auditoria per-user): state OAuth **HMAC** fail-closed + janela ts 10min (`_shared/oauth-state.ts`) + `instagram-webhook` **X-Hub-Signature-256**; 8/8 gates. **(4) OTD-VA-018-SENTINEL-PTBR:** 7 famílias pt-BR no Cyber-Sentinel, **0 FP real** em 58 amostras (loop `wf_0459e1c1` → tunei f3/f4/f5), live 403 `score=2` sem regressão do inglês. **Prova:** `/security-review` SAFE múltiplo · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8954** · handoff `bc175ac9` · 6 commits. **Pending (próxima):** Unified Canvas 3.5-3.10 (gate visual 1920×1080) · mídia viral 9:16 · postback ML real · Security BoK suite (diferida). **Lição:** o sentinel é TRIAGE score≥2 — single-intent passa por design (=inglês), defesa cross-t
> ...
> </persisted-output>
> ```

## 🤖 Claude *(02:37:14)*


## 🤖 Claude *(02:37:14)*

I have most of the picture. Let me pull the "Top 3 Gap" section from sprint-priorities and confirm the BoK gate completeness check.

## 🤖 Claude *(02:37:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -iE \"top 3|gap closure|gap #|#1|#2|#3\" /home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md | head -20",
  "description": "Find gap closures section"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9:**Sprint v6.47.0 — Per-user 100% (env = só infra) + CF WP unblock + sweep per-user FECHADO (2026-06-22)** — `/handson` → "resolver CF WAF + secrets, depois os próximos passos". **(1) CF WP unblock RESOLVIDO:** o componente de skip que faltava no Cloudflare era **"Nível de segurança"** (challenge por reputação de IP de **datacenter** Oracle AS31898, não bot/UA) — diagnosticado via Security→Events (a regra Skip já disparava `Ignorar`, mas o Nível de segurança desafiava por cima). Regra CF header-gated + secrets `WP_PUBLISH_SECRET`/`_HOST`; E2E `publish-wordpress`→`post_id 18`. SOPs `wordpress-cf-publish-unblock.md` (atualizada) + `wordpress-cf-per-user-publish.md` (multi-tenant). **(2) Diretiva Sovereign env=só-infra:** auditoria per-user (workflow `wf_102ef5ac`, 49 fns; 30 per-user · 11 fallback-ok · 4 remediadas) → removido `|| Deno.env.get(<provider>)` de **25 fns user-facing** (47 ocorrências) → per-user PURO fail-closed; 2 fns de sistema (`embed-mcorch-node`/`search-constellation`) → `MESH_EMBED_*` dedicadas; secrets antigos mantidos (seed source) + `.env` anotado. **(3) Sweep per-user FECHADO:** #1 openrouter-swarm · #2 canvas-execute Higgsfield · #3 fetch-trends (migration `rapidapi_key` + UI + 402 provado) · + `aios-chat-gateway` token vazado fail-closed. BYOK do User 0 seedado do `.env`. **Prova:** `/security-review` SAFE 2× · 27 fns deployadas 0 falhas · embedding pós-rename 200 · OpenRouter autenticou com chave per-user do User 0 · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8947** · handoff `4e57bf72`. **Pending (próxima):** segurança `social-auth-callback` HMAC + `instagram-webhook` signature · **C** 1º ciclo pago (CF desbloqueado!) · BYOK imagem opt-in · impl WP-CF per-user. **Lição:** o E2E "falhou bonito" (OpenRouter 404-de-modelo + `user_id`) PROVOU a chave per-user; o approach atômico do Higgsfield pegou o trap do row null/secret antes do deploy; o "Nível de segurança" só apareceu no Security→Events (não chutei checkbox).
> 25:**Sprint v6.38.0 — Vision MCP `deepsearch.run`/`poll` async (FR-VM-007 · job→poll→partial-refund §4.5) (2026-06-15)** — `/handson` → Sovereign puxou o item #1 do roadmap vision-mcp. Closed-Loop: workflow de **mapeamento (5 readers)** leu contrato selado + schema vivo + wiring ANTES do código — e **pegou que minha premissa contradizia a BoK** (a SDD sela **Firecrawl**, não "google/gemini"). Surfaceei; Sovereign decidiu (custom): *"não pagar Firecrawl agora; usar chaves já disponíveis"* → motor = **Gemini Google-Search grounding** (chave `google` já provisionada; BYOK→plataforma→402), **desvio consciente OTD-VM-024** (débito de emenda BoK); contrato job/refund/state 100% fiel à BoK. **Entregue:** `deepsearch.run` (3 mco, débito-na-entrada→`job_id`→worker in-process→refund parcial §4.5 floor-a-favor-do-tenant) + `deepsearch.poll` (grátis, tenant-bound, **self-heal de órfão**); `vision_jobs` (SELECT-own RLS) + **RPC atômico `finalize_vision_job`** (service-role-only, terminal+refund 1×/job); menores (`infra_health_logs` event/metadata + OTD-VM-023 orphan-sub). **Reviews:** workflow adversarial 5-lentes (2 HIGH: charge-without-value + refund-atomicity → fechados com finalize+reconcile) + **recuperação dos 3 verify mortos por session-limit** dos transcripts (achado novo: sem teto GLOBAL da chave-plataforma → **OTD-VM-025** semáforo; bucket era só per-sub) + allowlist de telemetria (side-channel cross-tenant) + erro de provider opaco + sentinel no `source_allowlist` + URLs http(s) + CHECK `refunded_mco≤charged_mco`. `/security-review` independente **SAFE** (0≥8). pkg **46/46** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8918** · handoff `fc0b5efc` · 6 commits · container `b24360c8` smoke **10/10** LIVE. **Top Gap novo:** Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 (root Sovereign) · cap diário per-tenant + rate-limiter compartilhado (OTD-VM-014/025) · emenda BoK do engine (OTD-VM-024) · per-plan `planned_units` (DD-VM-003). **Lição:** o workflow de mapeamento pré-código pegou a contradição Firecrawl-vs-Gemini ANTES de eu codar a coisa errada (Lei 2); e recuperar findings órfãos de transcript (em vez de re-rodar) achou 1 HIGH novo de custo que o /security-review (classe DoS excluída) não pegaria.
> 57:**Sprint v6.25.0 selado em 2026-06-03** — **Flywheel ressuscitado + calibração mcoCoins**. `/handson` → diretiva Sovereign ("o que falta pro 1º run pago E2E + já calibrar o COIN_COST?"). Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados): **OTD-MCOIN-CALIBRATION FECHADA** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso=Enterprise); surpresa honesta — `10` (orchestrate) e `125` (canvas vídeo) **já** eram ~4× sobre custo real, único furo `IMAGE_GENERATION 3→9` (`CONTENT_GENERATION 5→2`). O **1º run pago E2E então expôs que o flywheel de conteúdo estava MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo run preso em `running`: **#1** `orchestrate-step` faltava no `config.toml` (`verify_jwt=true` → gateway **401** na chave opaca `sb_secret_` do pg_net); **#2** `async_orchestrate_step` hotfixada em prod **sem migration** (`p_service_jwt_legacy`≠`p_service_key` → **PGRST202** → auto-chain morto) → migration `20260603190000` realinha + `GRANT service_role`, `/security-review` SAFE, RPC **204**; **#3** `wp_site_url` não-www → **301 → POST vira GET** → WP devolve LISTA de posts → `publish-wordpress` endurecido (valida `id`, 502 honesto) + `wp_site_url→www`. **Provado E2E**: run `89f18bea` **auto-completou 6/6 passos sem kick** → rascunho WP `?p=14` + `content_mesh_asset` done. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8769**. Survival Laws **4/4**. 7 commits. **Novo Top Gap:** auditar **drift deployado↔migrations** (outras RPCs/fns hotfixadas em prod?) · limpar artefatos de teste (5 posts parqueados 2027 + 2 rascunhos WP) · FR-MH-009/010/012 + Nurturing follow-up · functionName nas 9 fns. **Lição:** o 1º run pago **não "falhou"** — fez seu trabalho: expôs 3 P0s silenciosos no coração do produto (falha sem erro visível, sem auto-refund); calibrar **antes** do run foi a decisão certa (transação econômica honesta).
> 67:**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 148:## 🔴 Top Gap Closures (by leverage)
> ```

## 🤖 Claude *(02:37:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK completeness per suite"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ agentic-workspace
> ✅ aios-sql-bridge
> ✅ authenticated-browser-operator
> ✅ canvas-design
> ✅ constellation-v2
> ✅ conteudo-v2
> ✅ e2e-user-zero
> ✅ gamificacao-nodes
> ✅ identity-fabric
> ✅ marketing-hub
> ✅ mcorch-constellation
> ✅ mcorch-qa-healing
> ✅ mercado-livre-api
> ✅ meta-api
> ✅ openclaw
> ✅ post-engine
> ⚠️ security — missing: 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> ✅ video-studio
> ✅ viral-autopilot
> ✅ viral-daily-canvas
> ✅ viralmind
> ✅ vision-mcp
> ```

## 🤖 Claude *(02:37:22)*


## 🤖 Claude *(02:37:23)*

Let me grab the Top Gap Closures section to complete the brief.

## 🤖 Claude *(02:37:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '148,185p' /home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md; echo \"---security bok files---\"; ls docs/bok/security/",
  "description": "Top Gap section + security bok actual files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ## 🔴 Top Gap Closures (by leverage)
> 
> 1. ~~**Loop/rotina de cadência**~~ ✅ `audit-4cs.sh` toda segunda 09:00 BRT · `auto-publish-cron.sh` */5min · `watchdog` */5min
> 2. ~~**Primeiro run Usuário Zero**~~ ✅ Publicado em mcorch.com · LinkedIn + Twitter gerados · pipeline_runs persistido
> 3. ~~**`publish-social` realmente publicar**~~ ✅ Bug JWT corrigido · LinkedIn publicando · Twitter: CreditsDepleted (Free tier API X)
> 4. **Instagram App Review Meta** — verificação empresarial necessária para produção com terceiros → bloqueante para onboarding clientes (diferir até User 1)
> 5. **Twitter API tier upgrade** — Free tier esgotou créditos de escrita. Upgrade para Basic ($100/mês) desbloqueia publicação no X (diferir até User 1)
> 6. ~~**Consolidação N+1 queries**~~ ✅ issues #002/#003/#009 resolvidos (2026-05-04)
> 7. ~~**Settings Overhaul**~~ ✅ useUserApiKeys + pref_ai_model + mcoCoins RPC + Testar key + ConfigPanel real data (2026-05-05)
> 8. ~~**A2UI live em produção**~~ ✅ parseAgentMessage → AIOSTerminal.onMessage (2026-05-07) — surfaces dinâmicas spawnam automaticamente
> 9. ~~**Test coverage hooks críticos**~~ ✅ 66 → 122 testes (useOrchestrationGraph + useKnowledgeMesh + useSubscription) (2026-05-07)
> 10. ~~**BoK Scribe v1**~~ ✅ 9 docs · ~29k palavras · grounded em código real · selada na mesh (2026-05-07)
> 11. ~~**Phase 2 BoK enrichment**~~ ✅ 6 docs enriquecidos (+227 linhas voz estratégica) (2026-05-08)
> 12. ~~**Phase 3 BoK → Agents**~~ ✅ 8-agent system gerado (704 linhas) via /bok-agents-generator (2026-05-08)
> 13. ~~**Endurecer FMEA-008 + FMEA-011**~~ ✅ validateContent() em orchestrate-content + checklist obrigatório /migration (2026-05-08)
> 14. ~~**LGPD data export**~~ ✅ data-export Edge Function + useDataExport hook + UI (2026-05-08)
> 15. ~~**Self-service account deletion**~~ ✅ delete_account() RPC + delete-account Edge Function + useDeleteAccount + modal (2026-05-08)
> 16. ~~**FMEA-005** (RPN 144) — smart chunked embeddings~~ ✅ Selado 2026-05-08 — `splitChunks()` + batch API + `averageVectors()` · zero truncação silenciosa para nós grandes
> 17. ~~**Deploy para produção**~~ ✅ Confirmado 2026-05-08 — data-export + delete-account em produção · migration aplicada
> 18. **Phase Commercial** — Stripe live keys + first external user onboarding. Todos os blockers LGPD removidos.
> 19. **Redesign completo com base no MIV** — Alinhamento visual da plataforma com a identidade definida no MIV (Three.js, tipografia Editorial, paleta de cores harmoniosa) → OTD-MIV-REDESIGN.
> 
> ---
> 
> ## 🛠️ Skills a criar ou evoluir
> 
> | Skill | Ação | Gatilho |
> |-------|------|---------|
> | `feature` | Evoluir para incluir scaffold de edge function junto | `/feature` |
> 
> ---
> 
> ## 🔌 Conexões a implementar
> 
> - [ ] Twitter API Basic tier — upgrade no developer.twitter.com para desbloquear tweet.write
> - [ ] Instagram produção — após App Review Meta (verificação empresarial)
> - [ ] Facebook/Threads — secrets configurados, aguarda App Review
> 
> ---security bok files---
> 00-deepsearch-blueprint.md
> 01-brd-security.md
> 02-srs-secure-spec.md
> 03-sdd-hardening-architecture.md
> 04-fmea-security.md
> ```

## 🤖 Claude *(02:37:36)*


## 🤖 Claude *(02:38:01)*

═══════════════════════════════════════════════════════════
  HANDSON — Viral Autopilot ATIVADO + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR (2026-06-23 · v6.48.0)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **Viral Autopilot ATIVADO** (1º ciclo pago real + pg_cron) + FR-VA-018 trend-angle hardened + segurança social-auth (state HMAC + webhook IG sig) + paridade pt-BR do Cyber-Sentinel
  Últimos commits:
   `f6c8914` — chore(sprint): v6.48.0 — Viral Autopilot ativado + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR
   `06c59c0` — feat(security): paridade pt-BR no Cyber-Sentinel (OTD-VA-018-SENTINEL-PTBR)
   `3488005` — fix(security): assina state OAuth (HMAC) + verifica X-Hub-Signature-256 do webhook IG
   `489dd61` — feat(viral-autopilot): FR-VA-018 ângulo informado por trends + gate de fonte
   `139fc3f` — feat(viral-autopilot): ativa cadência pg_cron (heartbeat recorrente FR-VA-005)

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (nada staged, nada untracked)

🏗️ **INFRA**
  mcorch_chroma:     Up 8 days (healthy) — Chroma API v2: ✅ OK (heartbeat respondeu)
  mcorch_claude_mem: Up 8 days (healthy)
  mcorch_vision_mcp: Up 6 days (healthy)
  mega-brain-daemon/webhook/dashboard: ✅ todos up/healthy

🧠 **KNOWLEDGE MESH**
  **8954 nós** (verificado live 2026-06-23) · **9070 arestas** (verificado 2026-06-01) · 100% embedded (768d HNSW cosine)
  Último handoff node: `bc175ac9-e8a8-483b-a32f-4660dd0b90ba`

🔧 **TYPESCRIPT**
  Zero erros ✅

📚 **BoK SUITES (MCORCH Master Execution Protocol)**
  Sealed (9/9): agentic-workspace · aios-sql-bridge · authenticated-browser-operator · canvas-design · constellation-v2 · conteudo-v2 · e2e-user-zero · gamificacao-nodes · identity-fabric · marketing-hub · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · post-engine · **video-studio** · **viral-autopilot** · viral-daily-canvas · viralmind · vision-mcp
  "Incompleta": `security` — **falso alarme**: é a suíte Cyber-Sentinel **deliberadamente diferida** com naming não-padrão (`01-brd-security`/`02-srs-secure-spec`/`03-sdd-hardening-architecture`/`04-fmea-security` + blueprint). Não é gate aberto.
  ⚠️ **GATE alert:** Nenhum bloqueador. Todo módulo significativo tem BoK selada.

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional — pipeline publica LinkedIn auto; Twitter ao subir tier; Instagram pós App Review.
  Top gap aberto: **#18 Phase Commercial** (Stripe live + 1º user externo — blockers LGPD já removidos) · **#19 Redesign MIV** (OTD-MIV-REDESIGN)

⚡ **PRÓXIMOS PASSOS (prioridade)**
  1. **Viral Autopilot — fechar o resíduo** (motor R1+R2+R3+R4 já ativo e provado com 1º ciclo pago `947ef8b5`). Restam só: **(C)** mídia viral 9:16 + canais TikTok/IG/YT (fase 2) e **(D)** provar postback ML real (OTD-VA-007 / OTD-ML-MP-PER-USER). Saída visível WP↔CF já desbloqueada.
  2. **Unified Sensorial Canvas — Fases 3.5→3.10** (Epsilon V9, EM ANDAMENTO): sinapses inter-rede reais de `mcorch_edges` · fly-to · **perf** (`OTD-UCANVAS-PERF` — query do código ~30s com 2 canvases) · poda squad-coloring · paridade + cutover de nav + **gate E2E 1920×1080** · seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`.
  3. **Suíte BoK de Segurança (Cyber-Sentinel)** — diferida; blueprint commitado (`6b1571a`). Sessão dedicada para gerar 01-brd/02-srs/03-sdd/04-fmea production-ready.

⚠️ **ALERTAS**
  Nenhum alerta crítico ✅ (TS limpo · containers saudáveis · worktree limpo · `scratch/` na verdade vazio — o warning do pre-flight foi falso-positivo de `ls` em diretório vazio)

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

O motor do Viral Autopilot está **vivo e provado** (1º ciclo pago real, heartbeat pg_cron `*/15` ativo). O caminho de maior alavancagem agora é **fechar o vídeo 9:16 + postback ML** (monetização real ponta a ponta) ou avançar o **Unified Sensorial Canvas** rumo ao gate visual. Qual frente puxo?

## 👤 User *(02:40:30)*

ótimo vamos nessa fichar o video 9:16 com a UI editor do hyperframer que estavamos implantando assim como o open design

## 👤 User *(02:40:33)*

[Request interrupted by user]

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-24 - Analisar mudanças recentes e contato]]
> * **Próxima Sessão**: [[2026-06-24 - Lovable Loop self-host + n8n 2.27.3 + Safe Browsing]]
%% --- TIMELINE END --- %%

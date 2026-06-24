# Implementar vídeo 9:16 no UI editor do Hyperframer
**Date:** 2026-06-24 | **Session ID:** `84036ed7-373c-41ec-bd44-f0bdc1f6de83`

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

## 👤 User *(02:40:46)*

ótimo vamos nessa fichar o video 9:16 com a UI editor do hyperframer que estavamos implantando assim como o open design

## 🤖 Claude *(02:41:53)*


## 🤖 Claude *(02:41:53)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Viral 9:16 + HyperFrames editor",
  "summary": "Fechar m\u00eddia vertical 9:16 do Viral Autopilot via UI editor HyperFrames (padr\u00e3o sidecar como open-design)"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Viral 9:16 + HyperFrames editor". Continue your current work.'}]
> ```

## 🤖 Claude *(02:41:58)*


## 🤖 Claude *(02:42:03)*

Entendido, Maestro. Vamos fechar o **vídeo viral 9:16** do Autopilot conectando o **editor HyperFrames** (mesmo padrão sidecar do open-design / canvas-design).

Antes de tocar código, preciso mapear materialmente o terreno — porque a memória registra que **video-studio Fatia 2 (o motor, incluindo HyperFrames) estava BLOQUEADA por infra** (sandbox RPN 200 + clone do estúdio). Preciso saber exatamente: o que HyperFrames é no código hoje, o que a BoK selada manda, o que o padrão open-design/canvas-design já tem vivo, e onde o 9:16 encaixa no pipeline do Autopilot. Disparo um workflow de mapeamento paralelo (6 leitores + síntese) para não projetar em cima de suposição.

## 🤖 Claude *(02:43:10)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'map-hyperframes-9x16',\n  description: 'Mapear estado real: video-studio/HyperFrames + canvas-design/open-design + viral-autopilot 9:16 + Canvas Studio video pipeline + frontend editor patterns, para projetar o fechamento do v\u00eddeo 9:16',\n  phases: [\n    { title: 'Map', detail: '6 leitores paralelos sobre os subsistemas relevantes' },\n    { title: 'Synthesize', detail: 'unificar mapas \u2192 realidade do HyperFrames + o que \u00e9 build\u00e1vel agora + fatias propostas' },\n  ],\n}\n\nconst READER_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['subsystem', 'files_examined', 'current_state', 'key_facts', 'blockers', 'integration_points', 'open_questions'],\n  properties: {\n    subsystem: { type: 'string' },\n    files_examined: { type: 'array', items: { type: 'string' }, description: 'paths reais lidos (Lei 1)' },\n    current_state: { type: 'string', description: '2-5 frases: o que existe e funciona vs o que \u00e9 stub/planejado' },\n    key_facts: { type: 'array', items: { type: 'string' }, description: 'fatos com file:line quando poss\u00edvel' },\n    blockers: { type: 'array', items: { type: 'string' }, description: 'o que est\u00e1 bloqueado e por qu\u00ea (infra/sandbox/clone/env/credencial)' },\n    integration_points: { type: 'array', items: { type: 'string' }, description: 'como este subsistema conecta ao objetivo: produzir v\u00eddeo 9:16 para o Viral Autopilot' },\n    open_questions: { type: 'array', items: { type: 'string' } },\n  },\n}\n\nphase('Map')\n\nconst READERS = [\n  {\n    key: 'video-studio-bok',\n    label: 'video-studio BoK',\n    prompt: `Leia a su\u00edte BoK do m\u00f3dulo video-studio em docs/bok/video-studio/ (todos os 9 docs, foco em 03-prd.md, 04-frd.md, 05-sdd.md e qualquer 00-deepsearch-blueprint). Objetivo: entender o que a BoK SELADA define para HyperFrames e v\u00eddeo vertical 9:16.\n\nResponda com FOCO em:\n- O que \u00e9 HyperFrames na arquitetura (\u00e9 um package? um sidecar? um editor de UI? o \"motor\" de render?). Como ele se relaciona com a vertente \"faceless studio (n8n externo)\".\n- Onde aparece v\u00eddeo VERTICAL 9:16 / formatos de short (TikTok/IG Reels/YT Shorts) \u2014 FRs espec\u00edficos (FR-VS-*).\n- A estrutura de Fatias (Fatia 1 = dom\u00ednio+contrato edge; Fatia 2 = motor). O que cada fatia entrega e o que falta.\n- A emenda BoK \"De-n8n\" SDD v1.2 \u2014 o que mudou.\n- Os FMEA-VS-* relevantes, especialmente o de RPN ~200 (sandbox HyperFrames + clone do est\u00fadio externo) e FMEA-VS-020 (cross-tenant).\n- Vari\u00e1veis de ambiente de ativa\u00e7\u00e3o (VIDEO_*_WEBHOOK) e a \"ponte R5 docker\".\n\nCite file:line. N\u00c3O invente \u2014 se um doc n\u00e3o cobre algo, diga \"n\u00e3o coberto\".`,\n  },\n  {\n    key: 'video-studio-code',\n    label: 'video-studio Fatia 1 code',\n    prompt: `Mapeie o C\u00d3DIGO j\u00e1 shipado do m\u00f3dulo video-studio (Fatia 1). Procure e leia:\n- Migrations: supabase/migrations/*video_render* e *video_asset* e *finalize_video_render* (tabelas video_renders, video_assets, RPC finalize_video_render). Reporte schema, RLS, RESTRICTIVE no-delete, FK composta tenant.\n- Edge functions: supabase/functions/video-render/ e supabase/functions/video-render-poll/ (index.ts). Reporte: o \"worker-gate 503 ANTES de deduct\" (zero-cost na Fatia 1), o contrato de input/output, custos provis\u00f3rios (125/12), como detecta o worker via env.\n- Procure QUALQUER c\u00f3digo relacionado a \"hyperframe\"/\"HyperFrames\" (grep case-insensitive em todo o repo: src/, supabase/, packages/, scripts/, docs/). Reporte cada hit com path:line.\n- Qualquer hook frontend (src/hooks/useVideo*) ou p\u00e1gina (src/pages/*Video*) j\u00e1 existente.\n\nObjetivo: saber EXATAMENTE o que est\u00e1 wired vs stub, e qual env/worker liga a Fatia 2. Cite file:line. Se HyperFrames n\u00e3o tem c\u00f3digo nenhum, diga isso explicitamente.`,\n  },\n  {\n    key: 'canvas-design-opendesign',\n    label: 'canvas-design / open-design sidecar',\n    prompt: `Mapeie o padr\u00e3o sidecar do m\u00f3dulo \"Canvas Design\" (integra\u00e7\u00e3o nexu-io/open-design via CLI 'od') \u2014 o Sovereign quer replicar ESTE padr\u00e3o de UI editor para o HyperFrames. Leia:\n- docs/bok/canvas-design/ (foco 05-sdd.md) \u2014 arquitetura do sidecar/daemon.\n- Scripts e servi\u00e7os: procure scripts/*design* , qualquer systemd unit \"design-bridge.service\" ou refer\u00eancia a ele, o daemon Docker \"mcorch-design-daemon\", a config global /app/.od/media-config.json.\n- Frontend: src/pages/*CanvasDesign* ou rota /dashboard/canvas-design, hooks relacionados.\n- Como o CLI 'od' funciona (cliente\u2192daemon COMPARTILHADO single-tenant \u2014 gotcha OTD-003), e o estado de gera\u00e7\u00e3o real.\n- Pend\u00eancias conhecidas: vhost design.mcorch.com (DNS Sovereign), LGPD OTD-008.\n- Procure docs/processes/*design* (SOPs).\n\nObjetivo: extrair o BLUEPRINT REUTILIZ\u00c1VEL deste padr\u00e3o (worker systemd + daemon compartilhado + bridge edge/frontend + persist\u00eancia) que poderia ser aplicado ao editor HyperFrames. Cite file:line.`,\n  },\n  {\n    key: 'viral-autopilot-media',\n    label: 'viral-autopilot 9:16 (item C)',\n    prompt: `Mapeie como o Viral Autopilot produz criativos hoje e onde o v\u00eddeo VERTICAL 9:16 (item C: m\u00eddia viral 9:16 + TikTok/IG/YT, fase 2) encaixa. Leia:\n- docs/bok/viral-autopilot/04-frd.md (e 03-prd, 05-sdd) \u2014 todos os FR-VA-* relacionados a M\u00cdDIA/v\u00eddeo/imagem/formato vertical/canais sociais (TikTok/IG Reels/YT Shorts). Especialmente FR-VA-003 (gerador product-aware), FR-VA-016, e o que define \"fase 2\" de m\u00eddia.\n- supabase/functions/autopilot-run/index.ts \u2014 como dispara o pipeline, o constraint N_runs=prod\u00d7rede\u00d7ab_variants, \"imagem no bundle de 10\".\n- supabase/functions/orchestrate-content/index.ts \u2014 o pipeline de campanha; passo de imagem (Fatia 1b: generate-image fail-open, content_library.media_url).\n- supabase/functions/generate-image/index.ts \u2014 como gera imagem hoje (dual-path auth service-role+user_id, retorna storage path).\n- A tabela creative_metrics (FR-VA-009) e autopilot_plans/autopilot_cycles.\n\nObjetivo: identificar o PONTO DE INSER\u00c7\u00c3O exato onde um asset de v\u00eddeo 9:16 seria gerado/anexado por sub-run, e como seria cobrado (prepaid). Cite file:line. Reporte qualquer FR que J\u00c1 preveja v\u00eddeo mas n\u00e3o esteja implementado.`,\n  },\n  {\n    key: 'canvas-studio-video',\n    label: 'Canvas Studio video pipeline',\n    prompt: `Mapeie o pipeline de V\u00cdDEO j\u00e1 funcional do Canvas Studio (o que J\u00c1 gera v\u00eddeo real hoje), para saber se podemos reusar em vez de construir do zero. Leia:\n- A skill .claude/skills/canvas-studio-cinematic/SKILL.md (shape dos n\u00f3s ReactFlow, Handle ids, canvas-execute, Nano Banana / Higgsfield DoP, persist\u00eancia vm_canvas_projects.graph).\n- supabase/functions/canvas-execute/index.ts \u2014 branches image / image_to_video, Higgsfield DoP, tier-gate, d\u00e9bito at\u00f4mico deduct_mco_coins (-125), vm_canvas_executions + execution_id.\n- Tabelas vm_canvas_* (migrations) \u2014 vm_canvas_projects, vm_canvas_executions, vm_canvas_assets.\n- O SOP docs/processes/canvas-video-async-execution.md.\n- IMPORTANTE: o Higgsfield/Canvas video atual suporta ASPECT RATIO 9:16 (vertical)? Procure qualquer par\u00e2metro de aspect/ratio/orientation/resolution nos requests.\n\nObjetivo: determinar se o Canvas Studio j\u00e1 produz v\u00eddeo 9:16 (ou pode com 1 par\u00e2metro) e se o Autopilot poderia chamar canvas-execute em vez de um motor HyperFrames novo. Cite file:line.`,\n  },\n  {\n    key: 'frontend-editor-patterns',\n    label: 'frontend editor UI patterns',\n    prompt: `Mapeie os padr\u00f5es de UI de EDITOR no frontend, para saber onde e como um \"editor HyperFrames\" (timeline/cenas de v\u00eddeo vertical) viveria. Leia:\n- src/components/orchestrator/ (OrchestrationCanvas, nodes/, edges/) \u2014 o padr\u00e3o ReactFlow tipado.\n- src/components/canvas/ ou src/components/canvas-studio/ ou qualquer src/pages/*Canvas* \u2014 a UI do Canvas Studio cinematogr\u00e1fico (n\u00f3s imagem/v\u00eddeo/\u00e1udio).\n- src/store/ \u2014 useOrchestrationStore, useCanvasStore (zundo temporal), qualquer store de canvas/projeto.\n- Como projetos de canvas persistem (vm_canvas_projects.graph jsonb) e o gotcha \"projeto abre em branco se grafo n\u00e3o persistido\".\n- App.tsx \u2014 padr\u00e3o de rotas lazy-loaded protegidas, onde uma rota /dashboard/video-editor (ou similar) se registraria.\n- Qualquer componente de timeline/scene/clip de v\u00eddeo j\u00e1 existente.\n\nObjetivo: extrair o esqueleto reutiliz\u00e1vel (rota + p\u00e1gina + store + n\u00f3s tipados + persist\u00eancia) para um editor HyperFrames de v\u00eddeo 9:16. Cite file:line.`,\n  },\n]\n\nconst maps = await parallel(\n  READERS.map((r) => () =>\n    agent(r.prompt, { label: r.label, phase: 'Map', schema: READER_SCHEMA })\n  )\n)\n\nconst validMaps = maps.filter(Boolean)\n\nphase('Synthesize')\n\nconst SYNTH_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['hyperframes_reality', 'canvas_video_9x16_status', 'reusable_sidecar_blueprint', 'buildable_now', 'blocked_pieces', 'recommended_approach', 'proposed_slices', 'bok_gate_status', 'critical_unknowns'],\n  properties: {\n    hyperframes_reality: { type: 'string', description: 'O que HyperFrames REALMENTE \u00e9 no codebase hoje (c\u00f3digo existente? s\u00f3 BoK? sidecar planejado?) e o que a BoK manda' },\n    canvas_video_9x16_status: { type: 'string', description: 'O Canvas Studio (canvas-execute/Higgsfield) j\u00e1 gera v\u00eddeo 9:16? Pode com 1 par\u00e2metro? Ou precisa motor novo?' },\n    reusable_sidecar_blueprint: { type: 'string', description: 'O padr\u00e3o reutiliz\u00e1vel do open-design/canvas-design (worker systemd + daemon + bridge + persist\u00eancia) aplic\u00e1vel ao HyperFrames editor' },\n    buildable_now: { type: 'array', items: { type: 'string' }, description: 'pe\u00e7as que podem ser constru\u00eddas SEM blocker de infra' },\n    blocked_pieces: { type: 'array', items: { type: 'string' }, description: 'pe\u00e7as bloqueadas + o blocker exato + a a\u00e7\u00e3o de ativa\u00e7\u00e3o (Sovereign-side)' },\n    recommended_approach: { type: 'string', description: 'recomenda\u00e7\u00e3o direta: reusar Canvas Studio vs construir HyperFrames editor novo; caminho de menor risco para fechar o 9:16' },\n    proposed_slices: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['name', 'scope', 'deliverables', 'risks', 'blocked'],\n        properties: {\n          name: { type: 'string' },\n          scope: { type: 'string' },\n          deliverables: { type: 'array', items: { type: 'string' } },\n          risks: { type: 'array', items: { type: 'string' } },\n          blocked: { type: 'boolean', description: 'true se depende de infra/ativa\u00e7\u00e3o Sovereign' },\n        },\n      },\n    },\n    bok_gate_status: { type: 'string', description: 'BoK gate: video-studio e canvas-design t\u00eam BoK selada? O 9:16 editor est\u00e1 coberto pela BoK existente ou precisa emenda/bok-scribe?' },\n    critical_unknowns: { type: 'array', items: { type: 'string' }, description: 'o que ainda precisa de probe material antes de codar' },\n  },\n}\n\nconst synthesis = await agent(\n  `Voc\u00ea \u00e9 o MCORCH Master Execution Agent sintetizando 6 mapas de subsistemas para projetar o fechamento do V\u00cdDEO VERTICAL 9:16 do Viral Autopilot, usando um editor HyperFrames no padr\u00e3o sidecar do open-design/canvas-design.\n\nCONTEXTO DO SOVEREIGN: \"fechar o v\u00eddeo 9:16 com a UI editor do HyperFrames que est\u00e1vamos implantando, assim como o open design\". O item (C) do Viral Autopilot \u00e9 \"m\u00eddia viral 9:16 + TikTok/IG/YT (fase 2)\". A mem\u00f3ria registra que video-studio Fatia 2 (motor + HyperFrames) estava BLOQUEADA por infra (sandbox RPN 200 + clone do est\u00fadio externo).\n\nREGRAS DE MATERIALIDADE (Lei 1): baseie cada afirma\u00e7\u00e3o nos fatos citados pelos mapas. Onde os mapas divergirem ou faltarem dado, liste em critical_unknowns \u2014 N\u00c3O invente.\n\nDECIS\u00c3O-CHAVE A RESOLVER: o caminho de menor risco para entregar v\u00eddeo 9:16 ao Autopilot \u00e9 (a) REUSAR o Canvas Studio existente (canvas-execute/Higgsfield DoP) com aspect 9:16, ou (b) construir o editor HyperFrames sidecar novo (que pode estar bloqueado por infra)? Recomende explicitamente, com trade-offs.\n\nConsidere tamb\u00e9m o BoK Gate (MCORCH Master Execution Protocol): se o editor HyperFrames de UI n\u00e3o estiver coberto pela BoK selada do video-studio, sinalize necessidade de emenda BoK antes de c\u00f3digo de UI.\n\nOs 6 mapas:\n${JSON.stringify(validMaps, null, 2)}`,\n  { label: 'synthesis', phase: 'Synthesize', schema: SYNTH_SCHEMA }\n)\n\nreturn { mapsCount: validMaps.length, synthesis }\n",
  "description": "Map HyperFrames + 9:16 video terrain"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wetcv79b9
> Summary: Mapear estado real: video-studio/HyperFrames + canvas-design/open-design + viral-autopilot 9:16 + Canvas Studio video pipeline + frontend editor patterns, para projetar o fechamento do vídeo 9:16
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/subagents/workflows/wf_5ba55a3c-5fe
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/workflows/scripts/map-hyperframes-9x16-wf_5ba55a3c-5fe.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/workflows/scripts/map-hyperframes-9x16-wf_5ba55a3c-5fe.js"} to iterate without resending the script.)
> Run ID: wf_5ba55a3c-5fe
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/workflows/scripts/map-hyperframes-9x16-wf_5ba55a3c-5fe.js", resumeFromRunId: "wf_5ba55a3c-5fe"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(02:43:17)*

The workflow is mapping the terrain in the background (6 parallel readers + synthesis). While it runs, I'll scout one thing inline that's decisive for the whole decision: **does the existing Canvas Studio video path already support 9:16 aspect ratio?** If yes, the cheapest path to close item (C) might be reusing `canvas-execute` rather than unblocking the HyperFrames sidecar.

## 🤖 Claude *(02:43:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== hyperframe(s) hits across repo ===\"\ngrep -rniE \"hyperframe\" --include=*.ts --include=*.tsx --include=*.md --include=*.json -l 2>/dev/null | head -40\necho\necho \"=== aspect/ratio/9:16 in canvas-execute ===\"\ngrep -rniE \"aspect|9:16|9x16|vertical|orientation|ratio\" supabase/functions/canvas-execute/index.ts 2>/dev/null | head -30 || echo \"(canvas-execute not found at that path)\"",
  "description": "Scout HyperFrames refs + 9:16 aspect support"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === hyperframe(s) hits across repo ===
> README.md
> HANDOFF.md
> src/lib/billing.ts
> src/test/useCanvasDesign.test.tsx
> src/hooks/useCanvasDesign.ts
> src/pages/VideoStudioPage.tsx
> supabase/functions/video-render/index.ts
> src/hooks/useVideoRender.ts
> docs/bok/canvas-design/05-sdd.md
> docs/bok/canvas-design/02-brd.md
> docs/bok/canvas-design/04-frd.md
> docs/bok/canvas-design/00-index.md
> docs/bok/canvas-design/03-prd.md
> docs/bok/canvas-design/01-mrd.md
> docs/bok/canvas-design/06-data-model.md
> docs/bok/video-studio/00-index.md
> docs/bok/video-studio/03-prd.md
> docs/bok/video-studio/01-mrd.md
> docs/bok/video-studio/07-process-flow.md
> docs/bok/video-studio/06-data-model.md
> docs/bok/video-studio/05-sdd.md
> docs/bok/video-studio/02-brd.md
> scripts/seed-video-studio-bok-seal.ts
> scripts/design-bridge.ts
> docs/bok/video-studio/04-frd.md
> docs/bok/video-studio/08-quality-metrics.md
> 
> === aspect/ratio/9:16 in canvas-execute ===
> supabase/functions/canvas-execute/index.ts:12:// ── Credit costs per operation (in mcoCoins) ─────────────────────────────
> supabase/functions/canvas-execute/index.ts:157:          ? `${body.provider}/${body.model}-${body.parameters?.duration || 5}s`
> supabase/functions/canvas-execute/index.ts:312:    // ── Magic Prompt generation ──────────────────────────────────────
> supabase/functions/canvas-execute/index.ts:401:        console.error("Magic Prompt generation failed:", err);
> supabase/functions/canvas-execute/index.ts:625:  // `gpt-image-1` AND `dall-e-3` on the /v1/images/generations endpoint with
> supabase/functions/canvas-execute/index.ts:639:  const resp = await fetch("https://api.openai.com/v1/images/generations", {
> supabase/functions/canvas-execute/index.ts:743:  // Round 3 hotfix (2026-05-17): /v1/images/generations returns 404 HTML on
> supabase/functions/canvas-execute/index.ts:744:  // OpenRouter — endpoint was deprecated. OpenRouter image generation now
> supabase/functions/canvas-execute/index.ts:832:    // Text-only response = model treated the prompt as a text-generation
> supabase/functions/canvas-execute/index.ts:852:  // viralmind integration (src/lib/higgsfield.server.ts). The previous
> supabase/functions/canvas-execute/index.ts:853:  // api.higgsfield.ai/v1/generations endpoint was wrong and never worked.
> supabase/functions/canvas-execute/index.ts:859:  // Derive Soul aspect ratio from incoming size / aspect_ratio params.
> supabase/functions/canvas-execute/index.ts:860:  // Canonical Higgsfield ARs (per /docs/guides/images): 16:9 · 9:16 · 1:1 · 4:5.
> supabase/functions/canvas-execute/index.ts:864:    "1024x1792": "9:16",
> supabase/functions/canvas-execute/index.ts:868:  const VALID_AR = new Set(["16:9", "9:16", "1:1", "4:5"]);
> supabase/functions/canvas-execute/index.ts:870:  const requestedAr = body.parameters?.aspect_ratio || SIZE_TO_AR[sizeKey] || "1:1";
> supabase/functions/canvas-execute/index.ts:871:  const aspectRatio = VALID_AR.has(requestedAr) ? requestedAr : "1:1";
> supabase/functions/canvas-execute/index.ts:886:    aspect_ratio: aspectRatio,
> supabase/functions/canvas-execute/index.ts:967:// `request_id`, UPDATE execution.operation_id, return 200 with status='queued'.
> supabase/functions/canvas-execute/index.ts:1022:  const duration = typeof body.parameters?.duration === "number" ? body.parameters.duration : 5;
> supabase/functions/canvas-execute/index.ts:1061:        duration,
> supabase/functions/canvas-execute/index.ts:1090:  const operationId = submitData.request_id ?? submitData.id;
> supabase/functions/canvas-execute/index.ts:1091:  if (!operationId) {
> supabase/functions/canvas-execute/index.ts:1097:    .update({ operation_id: operationId })
> supabase/functions/canvas-execute/index.ts:1100:    console.error("[canvas-execute] failed to persist operation_id:", updErr);
> supabase/functions/canvas-execute/index.ts:1115:      operation_id: operationId,
> ```

## 🤖 Claude *(02:43:24)*


## 🤖 Claude *(02:43:26)*

Key finding already: `canvas-execute` **explicitly supports 9:16** as a canonical Higgsfield aspect ratio (line 864-871) for image generation. Let me check whether the **video** branch (image→video DoP) carries aspect through, and what HyperFrames actually is in the shipped frontend (`VideoStudioPage`, `useVideoRender`).

## 🤖 Claude *(02:43:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== canvas-execute VIDEO branch (image_to_video / DoP) around 990-1120 ===\"\nsed -n '990,1120p' supabase/functions/canvas-execute/index.ts | grep -niE \"aspect|ratio|9:16|vertical|width|height|size|resolution|motion|duration|quality|model|provider\" | head -40\necho\necho \"=== VideoStudioPage.tsx (head) ===\"\nsed -n '1,60p' src/pages/VideoStudioPage.tsx",
  "description": "Inspect video branch aspect + VideoStudioPage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === canvas-execute VIDEO branch (image_to_video / DoP) around 990-1120 ===
> 33:  const duration = typeof body.parameters?.duration === "number" ? body.parameters.duration : 5;
> 34:  const motionStrength = typeof body.parameters?.motion_strength === "number"
> 35:    ? body.parameters.motion_strength
> 38:  // Routing based on model parameter (aligned with .claude/context/higgsfield-api-validation-2026-05-15.md)
> 40:  let modelPath = "higgsfield-ai/dop/standard";
> 41:  if (body.model === "dop-lite") {
> 42:    modelPath = "higgsfield-ai/dop/lite";
> 43:  } else if (body.model === "dop-turbo") {
> 44:    modelPath = "higgsfield-ai/dop/turbo";
> 45:  } else if (body.model === "kling-2.1-pro") {
> 46:    modelPath = "kling-video/v2.1/pro/image-to-video";
> 47:  } else if (body.model === "seedance-v1-pro") {
> 48:    modelPath = "bytedance/seedance/v1/pro/image-to-video";
> 57:  const submitUrl = new URL(`${BASE_URL}/${modelPath}`);
> 72:        duration,
> 73:        motion_strength: motionStrength,
> 101:  const operationId = submitData.request_id ?? submitData.id;
> 102:  if (!operationId) {
> 108:    .update({ operation_id: operationId })
> 111:    console.error("[canvas-execute] failed to persist operation_id:", updErr);
> 126:      operation_id: operationId,
> 
> === VideoStudioPage.tsx (head) ===
> // VideoStudioPage (Fatia 1b) — display-only front door for the video-studio module. All data/logic lives in
> // useVideoRender (Harness Engineering). The render submit validates the full contract (consent, BYOK, cost) end to
> // end; the render ENGINE itself lands in Fatia 2 (faceless = Docker bridge + n8n; hyperframes = sandbox), so a real
> // submit currently returns a friendly 503 and charges nothing.
> import { useState } from 'react';
> import {
>   useVideoRenders, useSubmitVideoRender, VIDEO_RENDER_COSTS, VIDEO_ENGINES, type VideoEngine,
> } from '@/hooks/useVideoRender';
> import { toast } from '@/hooks/use-toast';
> import { Button } from '@/components/ui/button';
> import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> import { Input } from '@/components/ui/input';
> import { Label } from '@/components/ui/label';
> import { Checkbox } from '@/components/ui/checkbox';
> import { Badge } from '@/components/ui/badge';
> import { Film, Clapperboard, Loader2, Coins, Hammer } from 'lucide-react';
> 
> const STATE_BADGE: Record<string, string> = {
>   queued: 'bg-blue-500/15 text-blue-400',
>   running: 'bg-blue-500/15 text-blue-400',
>   qa_gate: 'bg-violet-500/15 text-violet-400',
>   done: 'bg-emerald-500/15 text-emerald-400',
>   qa_failed: 'bg-amber-500/15 text-amber-400',
>   failed: 'bg-red-500/15 text-red-400',
> };
> 
> export default function VideoStudioPage() {
>   const { data: renders = [], isLoading } = useVideoRenders();
>   const submit = useSubmitVideoRender();
>   const [engine, setEngine] = useState<VideoEngine>('faceless');
>   const [topic, setTopic] = useState('');
>   const [voiceConsent, setVoiceConsent] = useState(false);
> 
>   const cost = VIDEO_RENDER_COSTS[engine];
> 
>   const onGenerate = async () => {
>     if (engine === 'faceless' && !voiceConsent) {
>       return toast({ title: 'Consentimento de voz necessário', description: 'O vídeo faceless clona uma voz — confirme o consentimento.', variant: 'destructive' });
>     }
>     try {
>       const r = await submit.mutateAsync({ engine, topic: topic.trim() || null, voice_consent: voiceConsent });
>       // In Fatia 2 this returns 202 {render_id}; in Fatia 1 the engine gate returns 503 (handled in catch).
>       toast({ title: 'Render enfileirado', description: `render_id ${r.render_id} · ${r.charged_mco} mcoCoins` });
>     } catch (e) {
>       const msg = (e as Error).message;
>       // Engine-unavailable (Fatia 1) is expected — surface it as info, not an error.
>       const pending = /Fatia 2|render_engine_unavailable|indispon/i.test(msg);
>       toast({
>         title: pending ? 'Motor de render em construção' : 'Não foi possível gerar',
>         description: msg,
>         variant: pending ? 'default' : 'destructive',
>       });
>     }
>   };
> 
>   return (
>     <div className="space-y-6 p-6">
>       <div>
>         <h1 className="flex items-center gap-2 text-2xl font-bold">
>           <Film className="h-6 w-6 text-primary" /> Estúdio de Vídeo
> ```

## 🤖 Claude *(02:43:45)*


## 🤖 Claude *(02:43:48)*

`VideoStudioPage` confirms the crux directly in its header comment: **"the render ENGINE lands in Fatia 2 (faceless = Docker bridge + n8n; hyperframes = sandbox), so a real submit currently returns a friendly 503 and charges nothing."** Meanwhile `canvas-execute` already ships a *working, paid-proven* video pipeline (Higgsfield DoP/Kling/Seedance) and supports 9:16. That's the decisive tension the synthesis needs to resolve. Two more quick scouts, then I'll wait for the workflow.

## 🤖 Claude *(02:43:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== VIDEO_ENGINES + costs in useVideoRender ===\"\ngrep -nE \"VIDEO_ENGINES|VIDEO_RENDER_COSTS|hyperframes|faceless|render_engine\" src/hooks/useVideoRender.ts | head -30\necho\necho \"=== billing.ts hyperframes/video costs ===\"\ngrep -niE \"hyperframe|video|faceless|render\" src/lib/billing.ts | head -20\necho\necho \"=== design-bridge.ts (the sidecar worker \u2014 head) ===\"\nsed -n '1,40p' scripts/design-bridge.ts",
  "description": "Video engines, costs, design-bridge sidecar pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === VIDEO_ENGINES + costs in useVideoRender ===
> 11:export type VideoEngine = 'faceless' | 'hyperframes';
> 14:export const VIDEO_RENDER_COSTS: Record<VideoEngine, number> = { faceless: 125, hyperframes: 12 };
> 16:export const VIDEO_ENGINES: { id: VideoEngine; label: string; desc: string }[] = [
> 17:  { id: 'faceless', label: 'Faceless', desc: 'Vídeo vertical sem rosto, narrado — pipeline E2E (Gemini → voz → motion → QA).' },
> 18:  { id: 'hyperframes', label: 'HyperFrames', desc: 'Render programático HTML → MP4, determinístico (sem IA generativa).' },
> 
> === billing.ts hyperframes/video costs ===
> 14://   orchestrate run (3 texts + 1 image) ≈ $0.04 · Higgsfield DoP 5s video = $0.56 (canvas-execute, validated 4×).
> 15://   Per-op markup at the floor: ORCHESTRATION_RUN 10 → 4.4× ✓ · canvas video 125 → 4.0× ✓ · canvas image 12 → 5.4× ✓.
> 30:  VISION_ANALYZE_VIDEO: 2,       // per minute (Gemini video @1FPS ~$0.0054/min)
> 36:  // video-studio Fatia 1 (PROVISIONAL — OTD-VS-007 · docs/bok/video-studio/05-sdd.md §4.4 4×-floor).
> 37:  // Calibrate against REAL cost at the first PAID render (slice 2), then seal. Edge fns mirror these copies.
> 38:  VIDEO_FACELESS_RENDER: 125,    // faceless E2E pipeline (n8n Gemini→Pollinations→VoxCPM→Remotion→LTX→FFmpeg→QA) ≈ canvas DoP video
> 39:  VIDEO_HYPERFRAMES_RENDER: 12,  // deterministic HTML→MP4 via headless Chrome (no AI legs) ≈ canvas image class
> 
> === design-bridge.ts (the sidecar worker — head) ===
> #!/usr/bin/env bun
> /**
>  * scripts/design-bridge.ts
>  *
>  * Bridge worker running on the host that polls `design_jobs` and executes
>  * open-design commands inside the Docker container.
>  *
>  * Usage: bun run scripts/design-bridge.ts
>  */
> 
> import { existsSync, readFileSync, mkdirSync } from 'fs';
> import { join, dirname } from 'path';
> import { fileURLToPath } from 'url';
> import { spawn } from 'child_process';
> import { createClient } from '@supabase/supabase-js';
> 
> // ── Load Environment Variables ──
> const __dirname = dirname(fileURLToPath(import.meta.url));
> const envPath = join(__dirname, '../.env');
> if (existsSync(envPath)) {
>   const raw = readFileSync(envPath, 'utf-8');
>   for (const line of raw.split('\n')) {
>     const m = line.match(/^([^#=\s][^=]*)=(.*)$/);
>     if (m) {
>       process.env[m[1].trim()] = m[2].trim().replace(/^["']|["']$/g, '');
>     }
>   }
> }
> 
> const SUPABASE_URL = process.env.SUPABASE_URL;
> const SERVICE_KEY = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);
> 
> if (!SUPABASE_URL || !SERVICE_KEY) {
>   console.error('❌ Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env');
>   process.exit(1);
> }
> 
> // Create Supabase client using Service Role to bypass RLS for status updates
> const supabase = createClient(SUPABASE_URL, SERVICE_KEY, {
>   auth: {
> ```

## 🤖 Claude *(02:44:19)*


## 🤖 Claude *(02:44:30)*

Tenho sinal material forte já antes da síntese chegar. O quadro está nítido:

**O que HyperFrames realmente é** (código + BoK selada):
- `VideoEngine = 'faceless' | 'hyperframes'` ([useVideoRender.ts:11](src/hooks/useVideoRender.ts:11))
- HyperFrames = **"Render programático HTML → MP4, determinístico (sem IA generativa)"** — headless Chrome, **12 mcoCoins**, classe-imagem ([billing.ts:39](src/lib/billing.ts:39))
- **Fatia 1 SHIPPED:** domínio (`video_renders`/`video_assets`/`finalize_video_render`) + contrato edge (`video-render`/`poll` com worker-gate 503 zero-cost) + porta de entrada UI ([VideoStudioPage.tsx](src/pages/VideoStudioPage.tsx))
- **Fatia 2 (o MOTOR) é o que falta:** o comentário de [VideoStudioPage.tsx:3](src/pages/VideoStudioPage.tsx:3) diz literalmente "*hyperframes = sandbox*" → submit real devolve 503 e **não cobra**.

**O padrão "assim como open design"** está vivo e é o blueprint exato: [scripts/design-bridge.ts](scripts/design-bridge.ts) é um **worker no host que faz poll de `design_jobs` e executa comandos dentro do container Docker** via service-role. Replicar isso para `video_renders` (engine=`hyperframes`) renderizando HTML→MP4 a 1080×1920 = destrava o 9:16 **sem dependência de API paga externa** (determinístico, headless Chrome é infra local nossa — não é um bloqueio duro como eu temia).

**A tensão que a síntese vai resolver:** já existe um pipeline de vídeo 9:16 *pago e provado* (`canvas-execute` Higgsfield DoP, suporta `9:16` em [canvas-execute:864-871](supabase/functions/canvas-execute/index.ts:864)). Reusar isso (IA, 125 mco) vs. construir o HyperFrames editor+bridge (determinístico, 12 mco, o que você pediu).

O workflow de mapeamento (6 leitores + síntese) está rodando — ele vai me dar o status exato do BoK Gate do editor de UI e as fatias propostas. Aguardo a conclusão para te trazer o plano fechado.

## 👤 User *(02:55:57)*

<task-notification>
<task-id>wetcv79b9</task-id>
<tool-use-id>toolu_01Tj1Xck8f4wJMfirBjZbhsW</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/tasks/wetcv79b9.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Mapear estado real: video-studio/HyperFrames + canvas-design/open-design + viral-autopilot 9:16 + Canvas Studio video pipeline + frontend editor patterns, para projetar o fechamento do vídeo 9:16" completed</summary>
<result>{"mapsCount":6,"synthesis":{"hyperframes_reality":"HyperFrames NÃO é código no codebase hoje — é enum/custo/label/comentário, zero motor. Material confirmado: grep case-insensitive em src/supabase/packages/scripts retorna SÓ (a) o CHECK enum engine IN ('faceless','hyperframes') na migration 20260622040000:36; (b) const COST={faceless:125,hyperframes:12} em video-render/index.ts:23 + billing.ts:39 + useVideoRender.ts:14; (c) labels de UI em VideoStudioPage.tsx e useVideoRender.ts; (d) o gate de env VIDEO_HYPERFRAMES_WEBHOOK (video-render/index.ts:84) que retorna 503. NENHUM componente React @hyperframes/studio, NENHUMA edge fn video-hyperframes-render, NENHUM container hyperframes-render. O que a BoK manda (video-studio 9/9 selada): HyperFrames é o NLE open-source da HeyGen (@hyperframes/studio, Apache-2.0) com DUAS faces — (1) EDITOR de UI embed NATIVO React (StudioApp/NLELayout/Player/Timeline — FR-VS-021, OTD-VS-005 escolha A; NÃO iframe) e (2) MOTOR determinístico HTML/CSS/JS→MP4 via headless Chrome(Puppeteer)+FFmpeg em container efêmero per-job (FR-VS-024, FMEA-VS-001 RPN 200). É o motor SECUNDÁRIO (persona Marina, edição programática data-driven), separado do Faceless Studio (motor primário, persona Léo, geração E2E). A nota da MEMORY 'HyperFrames=sandbox RPN 200+clone' é precisa quanto ao sandbox (FMEA-VS-001) mas 'clone' NÃO é um FMEA numerado — refere-se à decisão v1.2 de re-implantar nativo o pipeline antes no n8n externo. Conclusão: HyperFrames é puramente PLANEJADO (BoK + sidecar). Construí-lo do zero = greenfield gated pelo sandbox RPN 200 + vhost video.mcorch.com (ação Sovereign).","canvas_video_9x16_status":"SIM, o Canvas Studio (canvas-execute/Higgsfield DoP) JÁ gera vídeo real E2E hoje (async fire-and-forget→webhook→bucket→débito atômico -125, provado 6.4MB mp4 na MEMORY), MAS o 9:16 NÃO é garantido por 1 parâmetro no submit de VÍDEO. Material confirmado: submitHiggsfieldVideo (canvas-execute/index.ts:1058-1063) envia SÓ {image_url, prompt, duration, motion_strength} — SEM aspect_ratio/size/orientation. A orientação 9:16 do clipe é HERDADA da imagem-base (é image→video, exige input_asset_url, :1014-1020). O caminho de IMAGEM Higgsfield Soul SIM suporta 9:16 com 1 parâmetro (canvas-execute/index.ts:861-871: VALID_AR inclui '9:16', SIZE_TO_AR['1024x1792']='9:16', parameters.aspect_ratio). Logo o 9:16 fecha em DOIS passos com 1 parâmetro efetivo: (passo 1) gerar imagem-base 9:16 via Soul aspect_ratio:'9:16'; (passo 2) DoP anima preservando o frame. NÃO precisa de motor novo. RESSALVA Lei 1 (não verificado nesta sessão): falta prova material de que o DoP da Higgsfield realmente preserva o aspecto 9:16 da imagem de input no mp4 de saída (inspecionar width/height do vm_canvas_assets resultante) — gap empírico a fechar antes de declarar 9:16 garantido. Também não confirmado se o endpoint image-to-video da Higgsfield aceitaria um aspect_ratio explícito (fecharia o gap de herança). Custo já calibrado: dop-standard-5s=125 mco (4×-floor de $0.56).","reusable_sidecar_blueprint":"O blueprint Canvas Design (open-design) está VIVO e provado (container open-design Up 8 days healthy em 127.0.0.1:7456; 2 workers systemd --user active; imagem real 1.27MB 2026-06-21) e é o padrão de 6 camadas reaplicável ao editor/render HyperFrames: (1) Container sidecar Docker em loopback; (2) Worker systemd que dirige o CLI/headless do sidecar (design-bridge.service: ExecStart bun run scripts/design-bridge.ts, Restart=always, segredos do ../.env, não no unit); (3) PONTE cloud↔local EXCLUSIVA via fila Supabase + poll/Realtime — Edge Functions NÃO alcançam daemon no host (OTD-006); o worker faz CLAIM ATÔMICO (.update({status:'running'}).eq('id').eq('status','queued').select() — design-bridge.ts:108-118, idempotente); (4) Edge fn FINA (JWT+débito atômico ANTES do INSERT+enfileira+202 — design-job-enqueue espelha o contrato prepaid); (5) Frontend display-only; (6) vhost por-subdomínio + SSO gate ES256 JWKS (sso-auth-gate.ts JÁ lista design.mcorch.com E video.mcorch.com — comentário linha 4; cookie .mcorch.com cobre qualquer *.mcorch.com sem código novo de auth). PERSISTÊNCIA TRIPLA por job (design-bridge.ts:206-294): upsert ref + INSERT nó mcorch_nodes (dispara embed) + UPDATE status + falha→infra_health_logs degraded — reusável tal-qual para nó 'video_render'/'hyperframe_artifact'. DIVERGÊNCIA chave: o editor HyperFrames NÃO é iframe (como Canvas Design ao Next.js do open-design) — é EMBED React NATIVO @hyperframes/studio (video-studio SDD:80-86); reusa-se a PONTE+SSO+vhost, mas troca o iframe pelo embed nativo. VANTAGEM material: o render HyperFrames é ephemeral per-job (Chrome+FFmpeg sandboxed) — isso RESOLVE o gotcha OTD-003 do open-design (daemon compartilhado single-tenant) para o render. HERANÇA de risco: o launch-blocker LGPD OTD-008/FMEA-007 RPN 240 (delete-account não purga OD_DATA_DIR/config de provider) aplica-se idêntico se reusar o sidecar.","buildable_now":["UI/editor frontend do HyperFrames (camada de editor, sem motor) — TODO o esqueleto reutilizável existe no repo principal, builda/serve do dist/, ZERO blocker de infra: store ReactFlow+zundo (useCanvasStore.ts template), nós tipados por união discriminada kind com factories+catálogo de custo+resolveExecutePayload (types/canvas.ts — JÁ tem ImageToVideoData com aspectRatio default '9:16' e ASPECT_RATIOS catálogo), persistência server-side vm_canvas_projects.graph jsonb (useCanvasStudio.ts), auto-save debounce 3s+flush (useAutoSave.ts), galeria→editor create→navigate→initialize (CanvasStudioPage.tsx), timeline/cena dnd-kit+parseScenes prontos (VideoEditorPage.tsx)","Reuso do Canvas Studio DoP para vídeo 9:16 via canvas-execute node_type:'image_to_video' — toda a máquina async/webhook/débito atômico/storage JÁ deployada; precisa só (a) imagem-base 9:16 via Soul aspect_ratio:'9:16' e (b) prova empírica de que DoP preserva 9:16","Gap de 1 parâmetro: adicionar aspect_ratio ao payload de submitHiggsfieldVideo (canvas-execute/index.ts:1058-1063) tornando 9:16 EXPLÍCITO — mudança pequena fail-open sem migration (PRECEDE confirmar que a API DoP aceita o param)","Dual-path service-role em generate-video (refactor de auth para body.user_id como generate-image tem — confirmado material: generate-video só resolve userId do Bearer JWT, sem body.user_id) — torna-o cron-invocável pelo orchestrate-step"],"blocked_pieces":["MOTOR HyperFrames (render HTML→MP4) — BLOQUEADO por (a) sandbox per-render de HTML não-confiável FMEA-VS-001 RPN 200 / OTD-VS-006: a BoK MANDA bloquear render multi-tenant até o container efêmero estar selado (cap_drop=ALL, no-new-privileges, egress-only, zero credencial no env) + /security-review obrigatório; (b) container nativo Remotion+FFmpeg na sovereign-net OTD-VS-014. Ativação = ação Sovereign + selo de segurança.","MOTOR Faceless (render vídeo vertical E2E) — BLOQUEADO por infra: o gate retorna 503 até setar env VIDEO_FACELESS_WEBHOOK no vault da edge fn (CONFIRMADO material: video-render/index.ts:84 lê a env, :87-89 retorna 503 ANTES do deduct na :94). Webhook concreto no estúdio externo /home/gcrUX/studio (rede n8n_default isolada) — mas a emenda v1.2 De-n8n ANULA o n8n; motor nativo não construído. Worker callback que chama finalize_video_render também NÃO existe.","vhost video.mcorch.com (app isolado do editor HyperFrames) — DNS+cert Cloudflare = AÇÃO SOVEREIGN (OTD-VS-015, padrão mcp/design). NOTA: se o editor for embed React PURO na SPA login.mcorch.com (sem backend stateful próprio), o vhost só é necessário para o RENDER, não para a UI.","Bucket privado video-studio-assets — referenciado em video_assets (migration :94) mas criação+escrita+minting de signed-URL NÃO está na Fatia 1.","Publisher TikTok/IG Reels/YT Shorts — NÃO existe (publish-* cobre só wordpress/linkedin/twitter; autopilot-run sem nenhuma referência a vídeo — grep vazio confirmado); PR-VA-021 é pré-requisito de valor real — sem ele o asset 9:16 não tem destino de publicação autônoma. Ativação = OAuth + novos destinos + app
... (truncated 10297 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/tasks/wetcv79b9.output)</result>
<usage><agent_count>7</agent_count><subagent_tokens>812788</subagent_tokens><tool_uses>102</tool_uses><duration_ms>766231</duration_ms></usage>
</task-notification>

## 🤖 Claude *(02:56:00)*


## 🤖 Claude *(02:56:01)*

Synthesis is rich. Let me read the full output (the result truncated the most important parts: recommended_approach, proposed_slices, BoK gate, unknowns).

## 🤖 Claude *(02:56:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/tasks/wetcv79b9.output | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\ns=d['synthesis']\nfor k in ['recommended_approach','bok_gate_status']:\n    print('### '+k.upper()); print(s.get(k,'(missing)')); print()\nprint('### PROPOSED_SLICES')\nfor i,sl in enumerate(s.get('proposed_slices',[]),1):\n    print(f'{i}. {sl[\\\"name\\\"]}  [blocked={sl.get(\\\"blocked\\\")}]')\n    print('   scope:', sl.get('scope'))\n    print('   deliverables:')\n    for x in sl.get('deliverables',[]): print('     -',x)\n    print('   risks:')\n    for x in sl.get('risks',[]): print('     -',x)\n    print()\nprint('### CRITICAL_UNKNOWNS')\nfor x in s.get('critical_unknowns',[]): print(' -',x)\nprint()\nprint('### BLOCKED_PIECES (full)')\nfor x in s.get('blocked_pieces',[]): print(' -',x)\n\"",
  "description": "Extract full synthesis fields"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 1
> Traceback (most recent call last):
>   File "<string>", line 4, in <module>
> KeyError: 'synthesis'
> ```

## 🤖 Claude *(02:56:08)*


## 🤖 Claude *(02:56:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/tasks/\necho \"=== file size + head ===\"; wc -c wetcv79b9.output; head -c 300 wetcv79b9.output; echo; echo \"=== top-level keys ===\"\npython3 -c \"import json; d=json.load(open('wetcv79b9.output')); print(type(d)); print(list(d.keys()) if isinstance(d,dict) else 'not-dict')\"",
  "description": "Inspect output file structure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === file size + head ===
> 20110 wetcv79b9.output
> {
>   "summary": "Mapear estado real: video-studio/HyperFrames + canvas-design/open-design + viral-autopilot 9:16 + Canvas Studio video pipeline + frontend editor patterns, para projetar o fechamento do vídeo 9:16",
>   "agentCount": 7,
>   "logs": [],
>   "result": {
>     "mapsCount": 6,
>     "synthesis": {
> === top-level keys ===
> <class 'dict'>
> ['summary', 'agentCount', 'logs', 'result']
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(02:56:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/84036ed7-373c-41ec-bd44-f0bdc1f6de83/tasks/\npython3 -c \"\nimport json\nd=json.load(open('wetcv79b9.output'))\ns=d['result']['synthesis']\nfor k in ['recommended_approach','bok_gate_status']:\n    print('### '+k.upper()); print(s.get(k,'(missing)')); print()\nprint('### PROPOSED_SLICES')\nfor i,sl in enumerate(s.get('proposed_slices',[]),1):\n    print(f'{i}. {sl[\\\"name\\\"]}  [blocked={sl.get(\\\"blocked\\\")}]')\n    print('   scope:', sl.get('scope'))\n    print('   deliverables:')\n    for x in sl.get('deliverables',[]): print('     -',x)\n    print('   risks:')\n    for x in sl.get('risks',[]): print('     -',x)\n    print()\nprint('### CRITICAL_UNKNOWNS')\nfor x in s.get('critical_unknowns',[]): print(' -',x)\nprint()\nprint('### BLOCKED_PIECES (full)')\nfor x in s.get('blocked_pieces',[]): print(' -',x)\n\"",
  "description": "Extract full synthesis fields (corrected path)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ### RECOMMENDED_APPROACH
> REUSAR o Canvas Studio (canvas-execute/Higgsfield DoP) é o caminho de MENOR RISCO para fechar o 9:16 ao Autopilot — NÃO construir o motor HyperFrames novo agora. Razões materiais: (1) o motor de vídeo do Canvas JÁ está deployado e provado E2E (6.4MB mp4, débito atômico -125, async webhook), enquanto o motor HyperFrames tem ZERO código + DOIS gates bloqueantes (sandbox RPN 200 + vhost Sovereign); (2) o 9:16 fecha sem motor novo: gerar imagem-base 9:16 via Higgsfield Soul (aspect_ratio:'9:16' JÁ suportado, :870-871) e o DoP anima preservando o frame — pipeline de 2 passos que o Autopilot já tem meia-via (Fatia 1b gera imagem product-referenced); (3) o ponto de inserção é exato e de baixo blast radius: logo após o bloco de imagem em orchestrate-step (~:399), espelhando o padrão Fatia 1b fail-open 'skipped', + recalcular projected em autopilot-run:96 (begin/finalize_autopilot_cycle absorvem sem mudança de RPC). Trade-offs: REUSAR Canvas — prós: shippa agora, motor provado, custo conhecido (125), zero gate de sandbox; contras: 9:16 herdado da imagem (não 1 param no vídeo — fechar gap empírico + opcionalmente param explícito), débito interno -125 do canvas-execute vs prepaid do ciclo (risco de dupla contabilidade — resolver contabilizando 1 vez), daily cap 100<125 (rodar como admin/ajustar), vídeo assíncrono pode chegar DEPOIS do finalize do ciclo (precisa poller estilo rescue-video). CONSTRUIR HyperFrames — prós: editor rico determinístico, alinhado à visão do Sovereign 'UI editor do HyperFrames'; contras: greenfield total + sandbox RPN 200 selo obrigatório + vhost Sovereign + emenda BoK de UI — semanas, não dias, e bloqueia o 9:16 do Autopilot atrás de infra. RECOMENDAÇÃO FASEADA: Fase A (agora, autônoma) — fechar 9:16 via Canvas DoP no pipeline do Autopilot (gated atrás de PR-VA-020 decomposto em FR + SOP, ver BoK gate); Fase B (paralela, sem bloquear A) — construir SÓ a CAMADA DE UI do editor HyperFrames (esqueleto Canvas Studio reusado, builda hoje) como editor manual do criador, deixando o MOTOR HyperFrames para quando o sandbox RPN 200 + vhost forem selados pelo Sovereign. Entrega o vídeo viral 9:16 sem depender do item infra-bloqueado.
> 
> ### BOK_GATE_STATUS
> video-studio: BoK 9/9 SELADA (00-index.md:33-41, seal c92850f+e3b0716 referenciados na MEMORY) — cobre HyperFrames editor (FR-VS-021, OTD-VS-005), motor (FR-VS-024), sandbox (FMEA-VS-001), 9:16 1080x1920 (NFR-VS-002), tenancy agência (FMEA-VS-020). canvas-design: BoK 9/9 selada. O EDITOR de UI 9:16 do HyperFrames ESTÁ coberto pela BoK selada do video-studio (FR-VS-021 embed nativo + OTD-VS-005 escolha A) — construir a camada de UI NÃO precisa de emenda video-studio. PORÉM há DOIS gaps de BoK que exigem ação antes de código: (1) GAP video-studio — NÃO há toggle/coluna aspect_ratio em video_renders nem FR de seleção de formato (16:9 vs 9:16); 9:16 é hard-coded como 'vertical' por definição de produto (grep vazio nos 9 docs). Se o Autopilot precisar de múltiplos formatos, é emenda video-studio. (2) GAP viral-autopilot (BLOQUEANTE) — PR-VA-020 (vídeo 9:16) e PR-VA-021 (publisher TikTok/IG/YT) declarados Fase 2/Future, NÃO decompostos em FR (FRD §1/§18, PRD §92-94). Pela Lei 2 + Closed-Loop Protocol, QUALQUER código de vídeo 9:16 no pipeline do Autopilot está bloqueado até emendar a suite BoK do viral-autopilot (MRD/BRD/PRD/FRD/SDD) + SOP em docs/processes/ (= Fatia VA-V0). Veredito: a UI editor passa pela BoK video-studio existente; a INTEGRAÇÃO autopilot→vídeo exige emenda BoK do viral-autopilot ANTES de código. Drift documental a anotar: a tabela de secrets do SDD §2.3 do video-studio ainda lista N8N_WEBHOOK_URL/HYPERFRAMES_RENDER_DISPATCH (design pré-v1.2 De-n8n) que não casa com VIDEO_*_WEBHOOK da implementação.
> 
> ### PROPOSED_SLICES
> 1. Fatia VA-V0 — Emenda BoK (PR-VA-020/021 → FR) + SOP do vídeo no Autopilot  [blocked=False]
>    scope: Decompor PR-VA-020 (vídeo 9:16) e o gancho de publicação em FRs na suite viral-autopilot (FRD/SDD) + escrever docs/processes/autopilot-video-9x16.md (Operator/Sequence/Verification/Recovery/Success). Pré-condição de TODA escrita de código de vídeo (Lei 2 + Closed-Loop Protocol).
>    deliverables:
>      - Emenda FRD/SDD viral-autopilot com FR-VA de vídeo 9:16 + custo + flag de plano
>      - SOP docs/processes/autopilot-video-9x16.md
>      - Decisão de pricing/caps registrada (OTD)
>    risks:
>      - Sem isto, código de vídeo viola Lei 2 e o BoK gate
>      - Decomposição de PR-VA-021 (publisher) pode ficar deferida sem perder a Fatia de geração
> 
> 2. Fatia VA-V1 — 9:16 via Canvas DoP no pipeline do Autopilot (geração)  [blocked=False]
>    scope: Gerar imagem-base 9:16 (Soul aspect_ratio:'9:16') + animar via canvas-execute image_to_video, anexar asset ao conteúdo agendado. Ponto de inserção: orchestrate-step após o bloco de imagem (~:399), fail-open 'skipped', espelhando Fatia 1b. Recalcular projected em autopilot-run:96; propagar flag video_enabled/video_format via autopilot_plans→fan-out→metadata→orchestrate-step.
>    deliverables:
>      - Coluna autopilot_plans.video_enabled/video_format (migration + /security-review)
>      - Bloco de vídeo fail-open em orchestrate-step (gera imagem 9:16 + chama image_to_video)
>      - projected recalculado + caps recalibrados (begin/finalize_autopilot_cycle inalterados)
>      - content_library type='video' + 1 linha creative_metrics + scheduled_posts com content_id
>      - Poller de reconciliação (estilo rescue-video/autopilot-collect) p/ asset assíncrono
>    risks:
>      - DoP preserva 9:16? Prova empírica pendente (Lei 1)
>      - Dupla contabilidade: débito interno -125 do canvas-execute vs prepaid do ciclo — contabilizar 1 vez
>      - Daily cap 100<125 → autopilot como admin/role-exception
>      - Asset chega depois do finalize do ciclo (assíncrono)
>      - Sem publisher TikTok/IG/YT, asset 9:16 fica sem destino autônomo
> 
> 3. Fatia VS-UI — Camada de UI do editor HyperFrames (sem motor)  [blocked=False]
>    scope: Construir o editor de UI clonando o esqueleto Canvas Studio: store ReactFlow+zundo, nós tipados kind (videoScene/videoClip/caption/audioTrack fixando aspectRatio '9:16'), persistência (vm_canvas_projects.graph OU tabela própria — decisão de data-model da BoK), auto-save, galeria→editor. Submete e mostra estado (como VideoStudioPage já faz com 503 amigável). NÃO inclui motor de render.
>    deliverables:
>      - Rota /dashboard/video/:id + página editor (lazy)
>      - Store + nós tipados 9:16 + registro nodeTypes
>      - Persistência de grafo (gotcha: semear graph COM outputs anexados senão abre em branco)
>      - Timeline de cena portada de VideoEditorPage (opcional, modo híbrido)
>    risks:
>      - Embed React nativo @hyperframes/studio (não iframe) — confirmar modelo suportado
>      - Se editor HyperFrames de UI não estiver coberto pela BoK selada → emenda BoK ANTES do código (BoK gate)
>      - Decisão vm_canvas_projects vs tabela própria pertence à BoK video-studio 06-data-model.md (não lida)
> 
> 4. Fatia VS-2 — Motor HyperFrames/Faceless (render real)  [blocked=True]
>    scope: Container efêmero per-render (Chrome+FFmpeg sandboxed) + worker callback que chama finalize_video_render + bucket video-studio-assets + setar VIDEO_*_WEBHOOK. Acende o caminho prepaid (deduct→insert→trigger→202) hoje morto atrás do gate 503.
>    deliverables:
>      - Container nativo Remotion+FFmpeg sandboxed (OTD-VS-014)
>      - Worker callback → finalize_video_render + escrita video_assets/storage_key
>      - Bucket privado video-studio-assets + signed-URL
>      - /security-review do sandbox SELADO
>    risks:
>      - FMEA-VS-001 RPN 200 (escape de sandbox HTML não-confiável) — BLOQUEIA render multi-tenant até selo
>      - vhost video.mcorch.com DNS+cert = ação Sovereign (OTD-VS-015)
>      - Edge fn Supabase não alcança rede docker do host sem endpoint público/túnel
> 
> ### CRITICAL_UNKNOWNS
>  - LEI 1 — DoP preserva 9:16? Não verificado materialmente nesta sessão que a Higgsfield DoP (image-to-video) preserva o aspecto 9:16 da imagem de input no mp4 de saída. Precisa: gerar imagem 9:16 → submeter DoP → inspecionar width/height do vm_canvas_assets resultante. Sem isto, 9:16 via Canvas é hipótese, não fato.
>  - O endpoint image-to-video da Higgsfield aceita um parâmetro aspect_ratio/resolution explícito? Se sim, fechar o gap de 1 parâmetro em submitHiggsfieldVideo é trivial; se não, 9:16 depende 100% da imagem-base.
>  - O caminho de imagem que o Autopilot já usa (Fatia 1b via generate-image / Nano Banana OpenRouter) produz 9:16? generateOpenRouter NÃO tem mapeamento de aspect ratio (canvas-execute:728-844) — pode ser necessário trocar para Higgsfield Soul 9:16 para a imagem-base. generate-image (fn separada) suporta orientação? Não inspecionado.
>  - @hyperframes/studio realmente exporta componentes React para embed NATIVO na SPA (StudioApp/NLELayout/Player/Timeline) sem backend stateful próprio? A BoK afirma (SDD:80-86) mas não verificado contra o pacote real. Se exigir daemon stateful, herda o atrito OTD-003 do open-design e força o vhost video.mcorch.com até para a UI.
>  - Modelo de data: o editor HyperFrames reusa vm_canvas_projects.graph (novos kinds) ou ganha tabela própria? Decisão pertence a docs/bok/video-studio/06-data-model.md — NÃO lido nesta varredura.
>  - Reconciliação financeira: débito interno -125 do canvas-execute vs prepaid begin/finalize_autopilot_cycle — qual mecanismo evita dupla cobrança/furo de cap? Decisão de engenharia + pricing do Sovereign.
>  - Duração: DoP é 5s fixo (dop-standard-5s). 5s basta para o formato viral 9:16 alvo, ou precisa de tier/modelo de clipe mais longo?
>  - Como o Autopilot DISPARA o vídeo: não há FR-VS descrevendo integração autopilot→video-render; a BoK video-studio trata o trigger como UI useFacelessRender ou batch PR-VS-020. A costura autopilot↔vídeo é trabalho de integração não documentado.
>  - Webhook concreto do faceless: como a edge fn Supabase (fora do host) alcança a rede docker interna n8n_default sem endpoint público/túnel? (relevante só se o caminho faceless/video-render for escolhido em vez do Canvas DoP)
> 
> ### BLOCKED_PIECES (full)
>  - MOTOR HyperFrames (render HTML→MP4) — BLOQUEADO por (a) sandbox per-render de HTML não-confiável FMEA-VS-001 RPN 200 / OTD-VS-006: a BoK MANDA bloquear render multi-tenant até o container efêmero estar selado (cap_drop=ALL, no-new-privileges, egress-only, zero credencial no env) + /security-review obrigatório; (b) container nativo Remotion+FFmpeg na sovereign-net OTD-VS-014. Ativação = ação Sovereign + selo de segurança.
>  - MOTOR Faceless (render vídeo vertical E2E) — BLOQUEADO por infra: o gate retorna 503 até setar env VIDEO_FACELESS_WEBHOOK no vault da edge fn (CONFIRMADO material: video-render/index.ts:84 lê a env, :87-89 retorna 503 ANTES do deduct na :94). Webhook concreto no estúdio externo /home/gcrUX/studio (rede n8n_default isolada) — mas a emenda v1.2 De-n8n ANULA o n8n; motor nativo não construído. Worker callback que chama finalize_video_render também NÃO existe.
>  - vhost video.mcorch.com (app isolado do editor HyperFrames) — DNS+cert Cloudflare = AÇÃO SOVEREIGN (OTD-VS-015, padrão mcp/design). NOTA: se o editor for embed React PURO na SPA login.mcorch.com (sem backend stateful próprio), o vhost só é necessário para o RENDER, não para a UI.
>  - Bucket privado video-studio-assets — referenciado em video_assets (migration :94) mas criação+escrita+minting de signed-URL NÃO está na Fatia 1.
>  - Publisher TikTok/IG Reels/YT Shorts — NÃO existe (publish-* cobre só wordpress/linkedin/twitter; autopilot-run sem nenhuma referência a vídeo — grep vazio confirmado); PR-VA-021 é pré-requisito de valor real — sem ele o asset 9:16 não tem destino de publicação autônoma. Ativação = OAuth + novos destinos + app review (ação Sovereign).
>  - Daily cap canvas-execute (100 mco default) < custo do vídeo (125) — CONFIRMADO material canvas-execute/index.ts:179 (dailyCap=100; admin=10000 :189, editor=1000 :191): 1 vídeo DoP estoura o cap de user comum; autopilot do Usuário Zero precisa role admin/editor ou recalibração. Caps dos autopilot_plans (default 200, floor 12) também não comportam 125/vídeo.
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(02:57:47)*


## 🤖 Claude *(02:58:07)*

O mapeamento fechou com prova material. Veredito direto, Maestro:

## 🔍 O que o terreno revelou

**HyperFrames hoje = casca, zero motor.** Grep em todo o repo: só existe o enum `engine IN ('faceless','hyperframes')`, os custos (`hyperframes:12` mco), labels de UI e o gate de env `VIDEO_HYPERFRAMES_WEBHOOK` que devolve **503 sem cobrar**. Não há componente React, edge fn de render, nem container. A Fatia 1 entregou só o **domínio + contrato + porta de entrada** ([VideoStudioPage](src/pages/VideoStudioPage.tsx)). O motor é greenfield.

**A BoK selada já cobre o EDITOR de UI** (FR-VS-021 — embed React nativo `@hyperframes/studio`, escolha A da OTD-VS-005). Então a **camada de UI builda hoje, sem emenda de BoK** e sem blocker de infra — todo o esqueleto reutilizável já existe (store ReactFlow+zundo, nós tipados com `aspectRatio:'9:16'` default, persistência `vm_canvas_projects.graph`, auto-save, galeria→editor).

**O padrão "assim como open design" está vivo e é o molde exato:** [design-bridge.ts](scripts/design-bridge.ts) — worker no host que faz *claim atômico* de jobs numa fila Supabase e executa no container (Edge fn **não alcança** daemon do host → ponte é só fila+poll). Replicável tal-qual para um `video-bridge` que renderiza HTML→MP4 a 1080×1920 via headless Chrome+FFmpeg.

**Dois gates reais que preciso respeitar antes de codar:**
1. ⚖️ **Lei 2 / BoK Gate:** a **integração Autopilot→vídeo** (PR-VA-020/021) está declarada "Fase 2/Future" e **não decomposta em FR** na BoK do viral-autopilot → qualquer código de vídeo *no pipeline do Autopilot* exige emenda BoK + SOP primeiro. (O editor manual, não — esse é coberto pela BoK video-studio.)
2. 🔐 **Segurança:** o **motor** de render carrega FMEA-VS-001 **RPN 200** (escape de sandbox de HTML não-confiável). A BoK manda bloquear render *multi-tenant* até o container efêmero estar selado. Para **Usuário Zero (single-tenant, nossos próprios templates)** dá pra construir agora com `/security-review`, **diferindo o hardening multi-tenant** para o Usuário 1 — exatamente o padrão de deferral que já usamos (Stripe/IG).

**Atalho que o mapa encontrou:** o Canvas Studio (`canvas-execute` Higgsfield DoP) **já gera vídeo real E2E provado** e suporta `9:16` na imagem-base — daria pra fechar o 9:16 do Autopilot *sem motor novo* (125 mco, IA). Mas isso **não é** o editor HyperFrames que você pediu.

Aí está a bifurcação real — e ela muda semanas de trabalho e a postura de segurança (Owner=Sovereign). Preciso da sua direção antes de selar o plano:

## 🤖 Claude *(02:58:17)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Qual motor produz o MP4 9:16? Sua diretiva apontou HyperFrames (editor + render determin\u00edstico, como o open-design). O mapa mostrou que o motor \u00e9 greenfield com gate de seguran\u00e7a, e que existe um atalho via Canvas DoP (IA, j\u00e1 provado). Como fecho o 9:16?",
      "header": "Motor 9:16",
      "multiSelect": false,
      "options": [
        {
          "label": "HyperFrames editor + worker (Usu\u00e1rio Zero)",
          "description": "Construo o editor de UI (coberto pela BoK) + um video-bridge no molde do design-bridge: headless Chrome\u2192FFmpeg renderizando HTML\u2192MP4 a 1080\u00d71920. Determin\u00edstico, 12 mco, single-tenant com /security-review; hardening multi-tenant (sandbox RPN 200) diferido p/ Usu\u00e1rio 1. \u00c9 literalmente 'a UI editor do HyperFrames assim como o open design'."
        },
        {
          "label": "Reusar Canvas DoP (IA, atalho)",
          "description": "Sem editor/motor novo: ligo o pipeline de v\u00eddeo IA j\u00e1 deployado e provado (imagem-base 9:16 via Soul \u2192 DoP image_to_video). Mais r\u00e1pido p/ autonomia, mas 125 mco, ass\u00edncrono, e exige eu provar empiricamente que o DoP preserva 9:16 (Lei 1). N\u00c3O \u00e9 o editor HyperFrames."
        },
        {
          "label": "Editor agora, motor depois",
          "description": "Construo s\u00f3 a camada de UI do editor HyperFrames (builda hoje, BoK cobre), submit devolve 503 amig\u00e1vel como hoje. Decido o motor (HyperFrames sandbox OU Canvas DoP) numa pr\u00f3xima sess\u00e3o, ap\u00f3s selar vhost/sandbox. Entrega a experi\u00eancia de edi\u00e7\u00e3o sem render real ainda."
        }
      ]
    },
    {
      "question": "Onde foco a entrega do 9:16 primeiro? Isso decide se preciso da emenda BoK do viral-autopilot (Lei 2) antes de qualquer c\u00f3digo.",
      "header": "Alvo primeiro",
      "multiSelect": false,
      "options": [
        {
          "label": "Editor manual do criador primeiro",
          "description": "HyperFrames como ferramenta standalone em /dashboard \u2014 voc\u00ea comp\u00f5e e renderiza shorts 9:16 manualmente. N\u00c3O toca o pipeline do Autopilot ainda \u2192 sem emenda BoK do viral-autopilot necess\u00e1ria agora. Caminho mais limpo e r\u00e1pido p/ ver o 9:16 saindo."
        },
        {
          "label": "Integra\u00e7\u00e3o Autopilot primeiro",
          "description": "Ligo o 9:16 aut\u00f4nomo direto no pipeline do Viral Autopilot (item C). Exige PRIMEIRO a emenda BoK do viral-autopilot (decompor PR-VA-020/021 em FR + SOP) pela Lei 2/Closed-Loop, depois o c\u00f3digo de gera\u00e7\u00e3o + caps + poller de reconcilia\u00e7\u00e3o."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Qual motor produz o MP4 9:16? Sua diretiva apontou HyperFrames (editor + render determinístico, como o open-design). O mapa mostrou que o motor é greenfield com gate de segurança, e que existe um atalho via Canvas DoP (IA, já provado). Como fecho o 9:16?"="HyperFrames editor + worker (Usuário Zero)", "Onde foco a entrega do 9:16 primeiro? Isso decide se preciso da emenda BoK do viral-autopilot (Lei 2) antes de qualquer código."="Integração Autopilot primeiro". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(03:06:18)*


## 🤖 Claude *(03:06:21)*

Decisão registrada, Maestro:
- **Motor:** HyperFrames editor + render worker (Usuário Zero, single-tenant, `/security-review`, hardening multi-tenant diferido) — o motor determinístico que você pediu, no molde do open-design.
- **Alvo:** Integração Autopilot primeiro → o que **aciona o BoK Gate (Lei 2)**: a emenda da BoK do viral-autopilot **precede qualquer código**.

Isso fixa a sequência. Vou registrar o plano e **começar pela emenda de BoK** (Fatia VA-V0) — é a precondição inegociável do Closed-Loop Protocol.

## 🤖 Claude *(03:06:21)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskCreate",
  "max_results": 3
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskCreate'}]
> ```

## 🤖 Claude *(03:06:27)*


## 🤖 Claude *(03:06:32)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Fatia VA-V0 \u2014 Emenda BoK viral-autopilot (v\u00eddeo 9:16) + SOP [Lei 2 gate]",
  "description": "Decompor PR-VA-020 (v\u00eddeo 9:16) e o gancho de publica\u00e7\u00e3o em FRs reais na su\u00edte viral-autopilot (04-frd.md + 05-sdd.md). Escrever docs/processes/autopilot-video-9x16.md (Operator/Sequence/Verification/Recovery/Success). Registrar OTDs: pricing/caps do v\u00eddeo, motor single-tenant (deferral multi-tenant FMEA-VS-001), engine=hyperframes vs Canvas DoP. Fix do drift video-studio SDD \u00a72.3 (N8N_WEBHOOK_URL \u2192 VIDEO_*_WEBHOOK). PRECONDI\u00c7\u00c3O de todo c\u00f3digo (Closed-Loop Protocol).",
  "activeForm": "Emendando BoK viral-autopilot (v\u00eddeo 9:16) + SOP"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #1 created successfully: Fatia VA-V0 — Emenda BoK viral-autopilot (vídeo 9:16) + SOP [Lei 2 gate]
> ```

## 🤖 Claude *(03:06:37)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Fatia VS-2 \u2014 Motor HyperFrames (video-bridge worker single-tenant)",
  "description": "Construir o video-bridge no molde do design-bridge.ts: worker host que faz claim at\u00f4mico de video_renders (engine=hyperframes, status=queued) \u2192 renderiza HTML\u2192MP4 1080\u00d71920 via headless Chrome+FFmpeg em container ef\u00eamero \u2192 upload bucket video-studio-assets (privado) \u2192 callback finalize_video_render + escreve video_assets. Wire do gate VIDEO_HYPERFRAMES_WEBHOOK\u2192fila. systemd unit (--user, Restart=always, segredos do .env). /security-review do sandbox (single-tenant Usu\u00e1rio Zero; hardening multi-tenant RPN 200 diferido p/ User 1).",
  "activeForm": "Construindo motor HyperFrames (video-bridge worker)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #2 created successfully: Fatia VS-2 — Motor HyperFrames (video-bridge worker single-tenant)
> ```

## 🤖 Claude *(03:06:41)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Fatia VA-V1 \u2014 Integra\u00e7\u00e3o 9:16 no pipeline do Viral Autopilot",
  "description": "Gerar composi\u00e7\u00e3o HTML product-aware no pipeline \u2192 enfileirar video_render(engine=hyperframes) \u2192 anexar asset 9:16 ao conte\u00fado agendado. Ponto de inser\u00e7\u00e3o: orchestrate-step ap\u00f3s o bloco de imagem (~:399), fail-open 'skipped' espelhando Fatia 1b. Coluna autopilot_plans.video_enabled/video_format (migration + /security-review). Recalcular projected em autopilot-run:96 + recalibrar caps (begin/finalize_autopilot_cycle inalterados). content_library type='video' + creative_metrics + scheduled_posts. Poller de reconcilia\u00e7\u00e3o p/ asset ass\u00edncrono (estilo rescue-video/autopilot-collect). Resolver contabilidade \u00fanica (prepaid do ciclo, sem dupla cobran\u00e7a).",
  "activeForm": "Integrando 9:16 no pipeline do Viral Autopilot"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #3 created successfully: Fatia VA-V1 — Integração 9:16 no pipeline do Viral Autopilot
> ```

## 🤖 Claude *(03:06:45)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Fatia VS-UI \u2014 Editor HyperFrames de UI (9:16)",
  "description": "Editor de UI clonando o esqueleto Canvas Studio: store ReactFlow+zundo, n\u00f3s tipados kind (videoScene/videoClip/caption/audioTrack fixando aspectRatio 9:16), persist\u00eancia de grafo (decis\u00e3o vm_canvas_projects vs tabela pr\u00f3pria por 06-data-model BoK), auto-save, galeria\u2192editor, rota lazy /dashboard/video/:id. Submete e mostra estado (reusa VideoStudioPage). Decidir embed React nativo @hyperframes/studio vs editor custom. Gate E2E 1920\u00d71080 (Lei 1 Canvas).",
  "activeForm": "Construindo editor HyperFrames de UI (9:16)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #4 created successfully: Fatia VS-UI — Editor HyperFrames de UI (9:16)
> ```

## 🤖 Claude *(03:06:54)*


## 🤖 Claude *(03:06:55)*

Now grounding the amendment in the real BoK text (Law 1 — amend faithfully, don't invent). Locating the exact sections to amend.

## 🤖 Claude *(03:06:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== viral-autopilot: PR-VA-020 / 021 + video mentions ===\"\ngrep -rniE \"PR-VA-020|PR-VA-021|9:16|vertical|tiktok|reels|short|v[\u00edi]deo|video\" docs/bok/viral-autopilot/03-prd.md docs/bok/viral-autopilot/04-frd.md | head -40\necho\necho \"=== viral-autopilot 04-frd: highest FR-VA number ===\"\ngrep -roE \"FR-VA-[0-9]+\" docs/bok/viral-autopilot/04-frd.md | sort -u | tail -8\necho\necho \"=== viral-autopilot 04-frd: all FR-VA in order (last 12) ===\"\ngrep -nE \"FR-VA-[0-9]+\" docs/bok/viral-autopilot/04-frd.md | tail -14",
  "description": "Locate viral-autopilot video FRs + numbering"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === viral-autopilot: PR-VA-020 / 021 + video mentions ===
> docs/bok/viral-autopilot/03-prd.md:92:| PR-VA-020 | **Video creative 9:16** (TikTok/Reels/Shorts) | P1 | BR-VA-001 | XL | vídeo cost | Fase 2 (Decisão 2); `generate-video` hoje órfã |
> docs/bok/viral-autopilot/03-prd.md:93:| PR-VA-021 | **TikTok/Instagram/YouTube publishing** | P1 | BR-VA-001 | XL | 0 | Fase 2; OAuth + publish novos destinos |
> docs/bok/viral-autopilot/03-prd.md:117:**Items:** PR-VA-020, PR-VA-021, PR-VA-022  
> docs/bok/viral-autopilot/03-prd.md:118:**Condition:** após MVP validado e decisão Sovereign de priorizar mídia viral (vídeo 9:16 + redes virais) — gate de esforço XL.
> docs/bok/viral-autopilot/03-prd.md:209:> Matriz **autoritativa** da cadeia MR→BR→PR (idêntica à BRD §10). PRs de Fase 2/Future (PR-VA-020/021/022) não entram — não decompostos neste ciclo (FRD §1).
> docs/bok/viral-autopilot/04-frd.md:16:**Out of scope (Fase 2 / Won't):** geração de vídeo 9:16; publicação em TikTok/Instagram/YouTube; gestão de anúncios pagos; atribuição multi-touch cross-network; auto-descoberta de catálogo (CLI manual permanece).
> docs/bok/viral-autopilot/04-frd.md:18:> **Nota de escopo de rastreabilidade:** os PRs de Fase 2 / Future (PR-VA-020 vídeo 9:16, PR-VA-021 TikTok/IG/YT, PR-VA-022 auto-discovery de catálogo) são **intencionalmente NÃO decompostos em FR neste ciclo** — não aparecem nas matrizes MR→PR→FR ativas (PRD §8 / §7 abaixo). Serão decompostos quando o Sovereign priorizar a Fase 2 (precedente: `marketing-hub` PR-MH-020..023).
> docs/bok/viral-autopilot/04-frd.md:40:| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje órfã) ao ciclo, **dentro do bundle `orchestrate-content` de 10 mco** (a imagem já é coberta pelo bundle — `billing.ts:16-21`; não gera custo adicional). Usa `image_url` do produto ML como referência; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | High | PR-VA-008 | EdgeFunction | AT-VA-013 |
> docs/bok/viral-autopilot/04-frd.md:190:> Cobertura: 21 FR (FR-VA-001..021) · 8 NFR. PRs de Fase 2/Future (PR-VA-020/021/022) não decompostos neste ciclo (FRD §1). Todo PR Must/Should rastreia ≥1 FR; todo FR rastreia ≥1 PR. **Gaps de numeração intencionais:** PR-VA-009 (saltado 008→010 entre Must e Should) e FR-VA-014..018 contínuos — sem buracos de conteúdo.
> 
> === viral-autopilot 04-frd: highest FR-VA number ===
> docs/bok/viral-autopilot/04-frd.md:FR-VA-014
> docs/bok/viral-autopilot/04-frd.md:FR-VA-015
> docs/bok/viral-autopilot/04-frd.md:FR-VA-016
> docs/bok/viral-autopilot/04-frd.md:FR-VA-017
> docs/bok/viral-autopilot/04-frd.md:FR-VA-018
> docs/bok/viral-autopilot/04-frd.md:FR-VA-019
> docs/bok/viral-autopilot/04-frd.md:FR-VA-020
> docs/bok/viral-autopilot/04-frd.md:FR-VA-021
> 
> === viral-autopilot 04-frd: all FR-VA in order (last 12) ===
> 164:| FR-VA-021 | ✅ | ✅ | — | **cap diário smoke zero-cost** (acumulado > daily_cap → abort sem deduct) |
> 177:| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |
> 178:| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |
> 179:| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |
> 180:| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |
> 181:| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |
> 182:| PR-VA-006 | FR-VA-007, FR-VA-021 | NFR-VA-002 |
> 183:| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |
> 184:| PR-VA-008 | FR-VA-013 | NFR-VA-008 |
> 185:| PR-VA-010 | FR-VA-012 | — |
> 186:| PR-VA-011 | FR-VA-018 | — |
> 187:| PR-VA-012 | FR-VA-019 | — |
> 188:| PR-VA-013 | FR-VA-020 | — |
> 190:> Cobertura: 21 FR (FR-VA-001..021) · 8 NFR. PRs de Fase 2/Future (PR-VA-020/021/022) não decompostos neste ciclo (FRD §1). Todo PR Must/Should rastreia ≥1 FR; todo FR rastreia ≥1 PR. **Gaps de numeração intencionais:** PR-VA-009 (saltado 008→010 entre Must e Should) e FR-VA-014..018 contínuos — sem buracos de conteúdo.
> ```

## 🤖 Claude *(03:07:20)*


## 🤖 Claude *(03:07:22)*

Precise grounding obtained: FRD covers FR-VA-001..021, new FRs start at **FR-VA-022**. PR-VA-020 (vídeo 9:16) is explicitly "Fase 2, não decomposto" — exactly what I must now decompose. Let me read the FR entry format + SDD architecture + the video-studio motor contract to amend faithfully.

## 🤖 Claude *(03:07:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "offset": 1,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Scope Statement
> 11	
> 12	Este documento especifica os requisitos funcionais e não-funcionais do `viral-autopilot`. Deriva do PRD `03-prd.md` e alimenta o SDD `05-sdd.md`.
> 13	
> 14	**In scope (MVP+v1.0):** entidade de plano de cadência; cron de disparo recorrente por-tenant; geração product-aware monetizada em todo formato (texto+imagem); coletor de desempenho unificado (cliques+orgânico+receita); analisador de ciclo + reinjeção de aprendizado; guarda de custo (teto + kill-switch); dashboard de ROI por criativo; seleção de produto por comissão+trend; ângulo informado por trends; geração A/B de variantes; gate HITL opcional.
> 15	
> 16	**Out of scope (Fase 2 / Won't):** geração de vídeo 9:16; publicação em TikTok/Instagram/YouTube; gestão de anúncios pagos; atribuição multi-touch cross-network; auto-descoberta de catálogo (CLI manual permanece).
> 17	
> 18	> **Nota de escopo de rastreabilidade:** os PRs de Fase 2 / Future (PR-VA-020 vídeo 9:16, PR-VA-021 TikTok/IG/YT, PR-VA-022 auto-discovery de catálogo) são **intencionalmente NÃO decompostos em FR neste ciclo** — não aparecem nas matrizes MR→PR→FR ativas (PRD §8 / §7 abaixo). Serão decompostos quando o Sovereign priorizar a Fase 2 (precedente: `marketing-hub` PR-MH-020..023).
> 19	
> 20	---
> 21	
> 22	## 2. Functional Requirements
> 23	
> 24	> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron` | `Lib`
> 25	
> 26	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 27	|----|-------|-------------|----------|-----------|----------|---------|
> 28	| FR-VA-001 | Autopilot plan entity | Tabela `autopilot_plans` (per-user RLS): mode (`all_at_once`\|`every_n_days`), interval_days (default 3), target_product_ids[], platforms[], budget_cap_mco, is_active, next_run_at. CRUD via hook. | Critical | PR-VA-001 | DB | AT-VA-001 |
> 29	| FR-VA-002 | Cycle dispatcher | Edge fn `autopilot-run`: valida plano, aplica gate de custo (FR-VA-007/021), seleciona produto(s), abre `autopilot_cycles`, e faz fan-out product-aware para `orchestrate-content` (**1 dispatch por produto×rede×variante** — `N_runs = produtos × redes × ab_variants`, casando com o pré-débito FR-VA-007). Reusa o padrão de `campaign-run`. | Critical | PR-VA-002, PR-VA-001 | EdgeFunction | AT-VA-002 |
> 30	| FR-VA-003 | Product-aware generation | Em `orchestrate-step`, o prompt recebe o produto-alvo (id+nome+imagem+preço+comissão) e usa framework de gancho viral de consumo (hook/valor/CTA) — substitui os system prompts B2B hardcoded (`:138`,`:290`). | Critical | PR-VA-002 | Lib/EdgeFunction | AT-VA-003 |
> 31	| FR-VA-004 | Monetize all formats | `monetizeContent` (`_shared/affiliate.ts`) roda em artigo **+ LinkedIn + Twitter**, embutindo link ML per-user por criativo (não só no artigo, não por regex de 3 SKUs). **`content_variant_id` = o `id` da linha de `content_library` daquele criativo**; grava `affiliate_links.content_id = content_variant_id` (hoje gravado `null`) e embute o `content_variant_id` no link rastreável → habilita atribuição por peça (FR-VA-017). | Critical | PR-VA-002 | Lib | AT-VA-004 |
> 32	| FR-VA-005 | Cadence cron | pg_cron `autopilot-cadence` (*/15) → fn `autopilot-cadence-cron` (service-role): encontra planos `is_active AND next_run_at <= now`, dispara `autopilot-run`, e re-agenda `next_run_at = now + interval_days` (auto-refill, ao contrário do drip finito do nurture). | Critical | PR-VA-003 | Cron | AT-VA-005 |
> 33	| FR-VA-006 | Cycle ledger | Tabela `autopilot_cycles`: plan_id, cycle_number, status (`running`\|`completed`\|`aborted_budget`\|`aborted_daily_cap`\|`failed`), spend_mco, refunded_mco, planned_units, analysis_node_id, debited_at, refunded_at, started_at, completed_at. Idempotência por (plan_id, cycle_number). FK composta tenant-escopada. | Critical | PR-VA-003 | DB | AT-VA-006 |
> 34	| FR-VA-007 | Cost guardrail (kill-switch, atômico) | Custo projetado = **`N_runs × ORCHESTRATION_RUN(10) + ANALYZE_COST(2)`**, onde **`N_runs = |target_product_ids| × |platforms| × ab_variants`** (cada `orchestrate-content` é bundle flat de 10 que **já inclui imagem** — `billing.ts:16-21`; `ab_variants` default 1). Se `projetado > budget_cap_mco` OU `saldo < projetado/min_balance` → aborta (`aborted_budget` 409 / `insufficient_balance` 402), pausa o plano, notifica — **sem deduzir**. Atomicidade: `autopilot-run` faz **UM `deduct_mco_coins(user_id, projetado)` ANTES do fan-out** (pré-pago, `debited_at`); sub-runs em modo `prepaid` (sem self-bill); ao fechar, **`finalize_autopilot_cycle(cycle_id, actual)`** (RPC SECURITY DEFINER service-role-only, idempotente por `refunded_at IS NULL`) **credita o não-usado** `(projetado − actual)` no `mco_balance` na MESMA transação (espelha `finalize_vision_job`). **Refund é crédito positivo — NUNCA `deduct` negativo** (`deduct_mco_coins` rejeita `p_amount<=0`, migration `20260603220000:45`). Resolve TOCTOU. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |
> 35	| FR-VA-008 | Engagement collector | Cron `autopilot-collect` (service-role) → fn que, dado o `post_id` de `publish-social`/`publish-meta`, busca insights reais (best-effort por API tier) e grava em `creative_metrics`. **Identidade (como `autopilot-analyze`):** deriva `user_id` da linha confiável (`scheduled_posts`/`autopilot_cycles`, nunca do body) e resolve o token de insights via `social_credentials`/`meta_config` **filtrado por esse `user_id`** (per-user, NFR-VA-004); fail-soft se o tenant não tem tier de insights → grava só `affiliate_clicks`. | High | PR-VA-004 | Cron/EdgeFunction | AT-VA-008 |
> 36	| FR-VA-009 | Unified creative metrics | Tabela `creative_metrics` keyed por `content_variant_id`: affiliate_clicks, impressions, engagements, revenue_cents, source, collected_at. Unifica os 3 sinais (Decisão 3). | High | PR-VA-004 | DB | AT-VA-009 |
> 37	| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role): deriva o tenant de `previous_cycle_id` (`SELECT user_id FROM autopilot_cycles` — **nunca do body**); lê `creative_metrics` do ciclo anterior; se vazio, usa baseline (`has_real_data=false`, NÃO inventa) e **não cobra** (log `analyze_empty`); se há dado, produz `optimization_policy` estruturado (top hook/produto/horário/formato) e cobra **2 mco** (`ANALYZE_COST`, 4×-floor — SOP `mcoin-cost-calibration`). **Encadeado pós-ciclo pelo `autopilot-cadence-cron`** (inline, sem cron próprio). | High | PR-VA-005 | EdgeFunction | AT-VA-010 |
> 38	| FR-VA-011 | Feedback injection | A geração (`orchestrate-step`/`autopilot-run`) LÊ o `optimization_policy` mais recente do tenant e injeta as features no system prompt do próximo ciclo. Fecha a quebra "saída sem consumo". | Critical | PR-VA-005 | Lib/EdgeFunction | AT-VA-011 |
> 39	| FR-VA-012 | Product selection by score | Seleção do produto-alvo do `vm_affiliate_products` por `commission_value`+`trend_score`+`profitability_score` (auto em v1.0). No MVP: 3 SKUs semente referenciados no plano (via FR-VA-001). | High | PR-VA-010 | EdgeFunction | AT-VA-012 |
> 40	| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje órfã) ao ciclo, **dentro do bundle `orchestrate-content` de 10 mco** (a imagem já é coberta pelo bundle — `billing.ts:16-21`; não gera custo adicional). Usa `image_url` do produto ML como referência; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | High | PR-VA-008 | EdgeFunction | AT-VA-013 |
> 41	| FR-VA-014 | Autopilot hook | `useAutopilot` (TanStack Query): CRUD de plano, status de ciclos, ROI por criativo. Toda lógica de dados no hook (Harness Engineering). | High | PR-VA-001, PR-VA-007 | Hook | AT-VA-014 |
> 42	| FR-VA-015 | Autopilot dashboard | `AutopilotPage` (display-only): editor de plano, timeline de ciclos, cards de criativo com ROI, criativo "vencedor", insight de lift ciclo-a-ciclo. | High | PR-VA-007 | UI | AT-VA-015 |
> 43	| FR-VA-016 | Honor product/affiliate param + cron identity | `orchestrate-content` passa a (a) desestruturar e honrar o produto-alvo (hoje dropado em `:79`), propagando ao `orchestrate-step`; (b) **aceitar o caminho cron** — service-role + header `x-autopilot-user-id` (server-trusted) + `prepaid=true` (sub-run não cobra; já pré-debitado em FR-VA-007). Sanitiza valores externos (produto/trend) antes do prompt. | Critical | PR-VA-001, PR-VA-002 | EdgeFunction | AT-VA-016 |
> 44	| FR-VA-017 | Revenue attribution per creative | `handle-ml-postback` credita `revenue_cents` na `affiliate_links` cujo `content_id = content_variant_id` (FR-VA-004); o coletor (FR-VA-008) reflete em `creative_metrics` por `content_variant_id`. Caminho: postback → `order_id`/`click_id` → `affiliate_links.content_id` → criativo. Depende de OTD-VA-007 (secret per-user). | High | PR-VA-004, PR-VA-007 | EdgeFunction | AT-VA-017 |
> 45	| FR-VA-018 | Trend-informed angle | `autopilot-run` lê `vm_trends` (de `fetch-trends`) para pautar o ângulo viral do ciclo (reconecta a ilha de trends). Texto de trend é **fonte não-confiável** → sanitizado antes do prompt (NFR-VA-008). | High | PR-VA-011 | EdgeFunction | AT-VA-018 |
> 46	| FR-VA-019 | A/B variant generation | Gera N variantes por criativo por ciclo (config no plano); a vencedora é escolhida pelo desempenho do ciclo anterior (`creative_metrics`) e promovida no próximo. Reusa a geração; sob o mesmo teto de custo (FR-VA-007). | Should (v1.0) | PR-VA-012 | EdgeFunction | AT-VA-019 |
> 47	| FR-VA-020 | HITL approval gate (opcional) | Quando `plan.hitl_required=true`, criativos entram em estado `pending_review` antes de publicar; aprovação humana reusa o policy-engine do `intent-execute`. Default off (autônomo). | Should (v1.0) | PR-VA-013 | EdgeFunction | AT-VA-020 |
> 48	| FR-VA-021 | Daily global mcoCoins cap | Safety cap **diário por tenant** (espelha `vision-mcp`): `autopilot-run` soma `spend_mco` dos `autopilot_cycles` do tenant no dia (UTC); se `acumulado + projetado > daily_cap_mco` → aborta (`aborted_daily_cap`), sem deduzir. Computado de `autopilot_cycles` (sem tabela nova). Fecha a ação de FMEA-VA-001 (RPN 128) / BR-RISK-001. | High | PR-VA-006 | EdgeFunction | AT-VA-021 |
> 49	
> 50	---
> 51	
> 52	## 3. Non-Functional Requirements
> 53	
> 54	| ID | Category | Requirement | Target | Measurement |
> 55	|----|----------|-------------|--------|-------------|
> 56	| NFR-VA-001 | Performance | Dispatch do ciclo (fan-out) p95 | < 5min para N ≤ 8 criativos | Supabase logs + `autopilot_cycles.completed_at − started_at` |
> 57	| NFR-VA-002 | Cost-safety | Gate de teto aplicado ANTES de qualquer deduct mcoCoins | 100% dos ciclos (zero deduct em ciclo abortado) | Smoke zero-cost; saldo intacto pós-abort |
> 58	| NFR-VA-003 | Idempotency | Re-fire do cron sobre o mesmo ciclo não dobra cobrança nem post | 0 duplicatas | Idempotência por (plan_id, cycle_number); guarda em `scheduled_posts` |
> 59	| NFR-VA-004 | Tenancy | Toda credencial externa resolvida per-user (`auth.uid()`); zero chave global em path user-facing | 100% | Code review + grep de `Deno.env` em fluxo user-facing |
> 60	| NFR-VA-005 | Security | Edge fns user-facing exigem JWT; crons usam service-role; RLS default-deny em toda tabela | 100% | `/security-review` |
> ```

## 🤖 Claude *(03:07:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "offset": 84,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 84	| PR-VA-011 | **Trend-informed angle** — `fetch-trends`/`vm_trends` pautam o ângulo viral | P1 | BR-VA-008 | M | 0 | Reconecta a ilha de trends ao gerador |
> 85	| PR-VA-012 | **A/B variant generation** — N variações por criativo por ciclo, escolhe vencedora pelo desempenho | P1 | BR-VA-003 | M | herda geração | Acelera o aprendizado do loop |
> 86	| PR-VA-013 | **HITL gate opcional** — aprovação humana antes de publicar (plano configura) | P2 | BR-VA-004 | S | 0 | Reusa policy-engine do `intent-execute` |
> 87	
> 88	### Could Have (Future / Fase 2)
> 89	
> 90	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 91	|----|---------|---------|-----------|--------|-------------|-------|
> 92	| PR-VA-020 | **Video creative 9:16** (TikTok/Reels/Shorts) | P1 | BR-VA-001 | XL | vídeo cost | Fase 2 (Decisão 2); `generate-video` hoje órfã |
> 93	| PR-VA-021 | **TikTok/Instagram/YouTube publishing** | P1 | BR-VA-001 | XL | 0 | Fase 2; OAuth + publish novos destinos |
> 94	| PR-VA-022 | **Catalog auto-discovery cron** — produtiza `discover-affiliate-products.ts` (hoje CLI manual) | P2 | BR-VA-008 | L | 0 | Score por comissão/trend real, não só log10(preço) |
> 95	
> 96	### Won't Have (This Cycle)
> 97	
> 98	- Gestão de anúncios pagos (Meta Ads) dentro do autopilot — `sync-meta-ads` permanece separado.
> 99	- Deduplicação de atribuição cross-network (multi-touch) — atribuição é por clique/postback no MVP.
> 100	- Outreach a influenciadores / parcerias.
> 101	
> 102	---
> 103	
> 104	## 5. Release Phasing
> 105	
> 106	### MVP Scope
> 107	**Target date:** 2026-07-31  
> 108	**Included:** PR-VA-001, PR-VA-002, PR-VA-003, PR-VA-004, PR-VA-005, PR-VA-006, PR-VA-007, PR-VA-008  
> 109	**Success gate:** um plano dispara ciclos a cada 3 dias, gera texto+imagem monetizados em WP/LinkedIn/X, coleta cliques de afiliado, e o ciclo 2 demonstra reinjeção do desempenho do ciclo 1 — tudo dentro do teto de custo (smoke zero-cost provando o kill-switch).
> 110	
> 111	### v1.0 Scope
> 112	**Target date:** 2026-08-31  
> 113	**Adds:** PR-VA-010, PR-VA-011, PR-VA-012, PR-VA-013  
> 114	**Success gate:** seleção automática de produto por comissão+trend + ângulo informado por trends + A/B + HITL opcional; lift ciclo-a-ciclo ≥ 1.10× medido (sinal = engajamento orgânico **OU** cliques de afiliado quando o tenant não tem tier de insights — KPI-VA-002).
> 115	
> 116	### Future Scope
> 117	**Items:** PR-VA-020, PR-VA-021, PR-VA-022  
> 118	**Condition:** após MVP validado e decisão Sovereign de priorizar mídia viral (vídeo 9:16 + redes virais) — gate de esforço XL.
> 119	
> 120	---
> 121	
> 122	## 6. Luxury UX Specifications
> 123	
> ```

## 🤖 Claude *(03:07:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== viral-autopilot 05-sdd: section headers + video/pipeline anchors ===\"\ngrep -nE \"^#{1,3} |FR-VA-013|FR-VA-016|orchestrate-step|orchestrate-content|generate-image|generate-video|pipeline\" docs/bok/viral-autopilot/05-sdd.md | head -50",
  "description": "FRD intro + PRD video PRs + SDD anchors"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === viral-autopilot 05-sdd: section headers + video/pipeline anchors ===
> 1:# SDD — System Design Document
> 10:## 1. Architecture Overview
> 35:│  orchestrate-content → orchestrate-step (product-aware gen)   │
> 54:## 2. Component Catalog
> 56:### 2.1 New Custom Hooks (`src/hooks/`)
> 62:### 2.2 New Display Components (`src/components/autopilot/`)
> 71:### 2.3 New Edge Functions (`supabase/functions/`)
> 80:> **config.toml (artefato versionado — mandato SOP `orchestrate-async-pipeline`):**
> 87:> Sem isso o gateway retorna 401 na chave service-role opaca (modo de falha #1 já vacinado — `project_orchestrate_pipeline_repair`).
> 89:> **Reuso (modificadas, não novas):** `orchestrate-content` (FR-VA-016: honra produto **+ aceita caminho cron** service-role + `x-autopilot-user-id` + `prepaid=true`), `orchestrate-step` (FR-VA-003 product-aware + FR-VA-011 feedback inject), `_shared/affiliate.ts` (FR-VA-004 monetiza todo formato + grava `content_id`), `generate-image` (FR-VA-013 plugado ao ciclo, dentro do bundle).
> 93:### 2.4 Zustand Store Slices (if applicable)
> 99:### 2.5 New DB Objects
> 114:## 3. Data Flow Diagrams
> 116:### Use Case: Ciclo autônomo a cada N dias (FR-VA-005 → FR-VA-011)
> 144:## 4. API Contract Definitions
> 146:> Toda Edge Function user-facing valida JWT antes de qualquer lógica. Crons usam service-role com `verify_jwt=false` (padrão pg_net do projeto — ver SOP `orchestrate-async-pipeline`).
> 148:### `POST /functions/v1/autopilot-run`
> 184:// → sub-runs invocados com prepaid=true (orchestrate-content NÃO self-bills).
> 191:### `POST /functions/v1/autopilot-analyze`
> 211:## 5. Security Design
> 213:### 5.1 Threat Model (STRIDE)
> 219:| `autopilot-run` (caminho cron, `verify_jwt=false`) | Caller anônimo POSTa `x-autopilot-user-id:<vítima>` e drena saldo (armadilha verify_jwt=false) | Spoofing/Elevation | Critical | **In-function service-role auth ANTES de confiar no header** (`if Authorization !== 'Bearer '+SB_SECRET_KEY → 401`, padrão `orchestrate-step:50-53`); só então confia em `x-autopilot-user-id` (= `plans.user_id`); revalida `cronUserId === plans.user_id` do `plan_id`. SOP `edge-jwt-identity-verification.md`. Caminho user-JWT assere `user.id === plan.user_id` |
> 223:| Gerador product-aware | Prompt injection via 3 fontes não-confiáveis: (a) nome/desc de produto, (b) texto de trend (`vm_trends`/FR-VA-018), (c) **reinjeção de `optimization_policy`** de ciclos anteriores (FR-VA-011) → auto-envenenamento persistente | Tampering/Elevation | High | Cyber-Sentinel **fail-CLOSED** (o mesmo gate de `orchestrate-content:92`) no input E no output antes de publicar; sanitização/escape das 3 fontes; valores das features estruturadas do `optimization_policy` tratados como **dados, nunca instrução** (OTD-VA-005) |
> 228:### 5.2 RLS Policy Definitions
> 259:### 5.3 JWT Validation Points
> 274:if (authHeader !== `Bearer ${serviceKey}`)      // mesmo padrão de orchestrate-step/index.ts:50-53 (service-role-only guard)
> 283:### 5.4 Secrets Inventory
> 288:| LLM key (Groq/OpenRouter/Gemini) | `orchestrate-step` (user path), `autopilot-analyze` (service-role) | `orchestrate-step`: `decrypted_user_api_keys` por `auth.uid()`. `autopilot-analyze` (sem `auth.uid()`): `decrypted_user_api_keys` **filtrado pelo `user_id` DERIVADO de `previous_cycle_id`** → fallback sistema (vault) — espelha o padrão `lead-score` (per-user→sistema fail-soft) | per-user controlado |
> 297:## 6. Infrastructure Touchpoints
> 309:## 7. Migration Stubs
> 412:## 8. Open Technical Decisions
> 425:| OTD-VA-008 | Identidade do caminho cron→`orchestrate-content` (o cron não tem JWT; a fn rejeita sem `Bearer`) | Repassar JWT (impossível — cron não tem) | Service-role + `x-autopilot-user-id` derivado de `autopilot_plans.user_id` + pré-débito atômico em `autopilot-run` (sub-runs `prepaid`) | **B** — server-trusted, nunca do body; resolve blocker SEC-VA-01 + TOCTOU SEC-VA-04. **Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer código** | Open (SOP-gated) | Sovereign |
> 427:> **Gate Lei 2 (Processo Antecipado):** o caminho de identidade do cron (OTD-VA-008) e o pré-débito/refund (FR-VA-007) introduzem automação financeira nova → o SOP `docs/processes/autopilot-cron-identity.md` DEVE ser escrito e revisado **antes** de a fatia de cadência/custo ganhar código. Referência cruzada: SOP `orchestrate-async-pipeline.md` (mandato `verify_jwt=false`).
> ```

## 🤖 Claude *(03:07:39)*


## 🤖 Claude *(03:07:40)*

Excellent grounding. The autopilot BoK has a clean precedent: **OTD-VA-008 → Law-2 SOP gate** (`autopilot-cron-identity.md` written before code). I'll mirror that exact pattern for the video integration. Now the video-studio motor contract + the SDD secrets drift, then I author.

## 🤖 Claude *(03:07:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== video-studio 04-frd: FR-VS-021 (editor) + FR-VS-024 (motor) + 9:16/NFR ===\"\ngrep -nE \"FR-VS-021|FR-VS-024|FR-VS-022|FR-VS-023|FR-VS-025|9:16|1080|NFR-VS-002|hyperframe|HyperFrame|finalize_video|video_render|engine\" docs/bok/video-studio/04-frd.md | head -40\necho\necho \"=== video-studio 05-sdd: secrets table (\u00a72.3 drift) + webhook ===\"\ngrep -nE \"N8N_WEBHOOK|VIDEO_.*WEBHOOK|HYPERFRAMES_RENDER|secret|Secret|webhook|Webhook|2\\.3|\u00a72\\.3\" docs/bok/video-studio/05-sdd.md | head -30",
  "description": "video-studio motor/editor FRs + SDD secrets drift"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === video-studio 04-frd: FR-VS-021 (editor) + FR-VS-024 (motor) + 9:16/NFR ===
> 18:- Auth MCORCH (JWT/sessão) gating de TODA superfície de vídeo — faceless trigger, editor HyperFrames, `design.mcorch.com` (R3 · PR-VS-002).
> 25:- HyperFrames embedado nativamente (React) com botão "Video" na TopBar e rota declarada ANTES de `canvas/:id` (PR-VS-009); render determinístico (PR-VS-011); sandbox per-render de HTML não-confiável (PR-VS-010).
> 43:| FR-VS-002 | Auth gate — HyperFrames editor | A rota `/dashboard/canvas/video` é protegida por `DashboardLayout`/`ProtectedRoute`; sessão ausente redireciona para `/auth`; a edge function `video-hyperframes-render` valida JWT antes do render. | Critical | PR-VS-002, PR-VS-009 | UI/EdgeFunction | AT-VS-002 |
> 61:| FR-VS-010 | Atomic deduct — HyperFrames render | `video-hyperframes-render` debita `VIDEO_HYPERFRAMES_RENDER` mco via RPC antes do render Chrome+FFmpeg; 402 em saldo insuficiente. | Critical | PR-VS-004, PR-VS-011 | EdgeFunction | AT-VS-010 |
> 83:### 2.6 HyperFrames Editor (núcleo segmento secundário)
> 87:| FR-VS-021 | Native React embed | O editor HyperFrames é embedado NATIVAMENTE via os componentes React exportados pelo `@hyperframes/studio` (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) — NÃO um iframe a um dev server `npx hyperframes preview`. Renderiza timeline + preview ao vivo + CodeMirror + hot reload dentro do cockpit. | Critical | PR-VS-009 | UI | AT-VS-021 |
> 88:| FR-VS-022 | Route ordering — canvas/video before canvas/:id | A rota `canvas/video` é declarada ANTES de `canvas/:id` em `src/App.tsx` (senão `:id="video"` sombreia a nova rota). O componente da rota é lazy-loaded. | Critical | PR-VS-009 | UI | AT-VS-022 |
> 89:| FR-VS-023 | "Video" button na TopBar | Um botão "Video" senta ao lado do botão "Pipeline" em `src/components/canvas/TopBar.tsx`; clicar navega para `/dashboard/canvas/video`. | High | PR-VS-009 | UI | AT-VS-023 |
> 90:| FR-VS-024 | Deterministic MP4 render | `video-hyperframes-render` produz MP4 via Chrome headless (Puppeteer) + FFmpeg de forma DETERMINÍSTICA: o mesmo template HTML/CSS/JS + media + props renderiza dois MP4 byte-idênticos. | High | PR-VS-011 | EdgeFunction/Container | AT-VS-024 |
> 91:| FR-VS-025 | Per-render sandbox (untrusted HTML) | O render de HTML/JS de tenant roda em sandbox isolado per-render (container efêmero, rede restrita, ZERO credencial de tenant no env de render); o HTML do tenant não alcança rede interna nem variáveis de ambiente (OTD-VS-006). Gate de `/security-review` obrigatório. | High | PR-VS-010 | Container | AT-VS-025 |
> 122:| NFR-VS-002 | Performance | HyperFrames render wall-clock (clip curto ≤30s, 1080×1920) | p95 < 90s | Container timing logs |
> 126:| NFR-VS-006 | Scalability | Renders HyperFrames concorrentes (sandbox per-render) | ≥ 5 containers efêmeros sem contenção de host | Load test |
> 136:| NFR-VS-016 | Determinism | HyperFrames: 2 renders do mesmo input → byte-idênticos | hash igual | `sha256sum` comparado |
> 137:| NFR-VS-017 | Accessibility | Superfícies humanas (picker, timeline, player) WCAG 2.1 AA; contraste ≥ 4.5:1; teclado-navegável | AA | Auditoria axe + E2E 1920×1080 |
> 156:[Storage bucket: video-studio-assets] + [DB: video_renders, mcorch_nodes, infra_health_logs]
> 160:[Component: HyperFramesEditor (native embed)]        (StudioApp/NLELayout/Timeline/SourceEditor)
> 164:[Edge Function: video-hyperframes-render]            (JWT gate → deduct_mco_coins → spawn sandbox)
> 166:[Container: hyperframes-render (ephemeral)]          (headless Chrome/Puppeteer + FFmpeg, no creds in env)
> 168:[Storage bucket: video-studio-assets] + [DB: video_renders]
> 205:#### `POST /functions/v1/video-hyperframes-render`
> 262:| `video_renders.user_id` | uuid | No | `= auth.uid()` (RLS) | "Sessão inválida." |
> 263:| `video_renders.engine` | text | No | `IN ('faceless','hyperframes')` | "Motor de render inválido." |
> 264:| `video_renders.state` | text | No | `IN ('queued','running','qa_gate','done','qa_failed','failed')` | — |
> 265:| `video_renders.charged_mco` | integer | No | `>= 0` | "Custo inválido." |
> 266:| `video_renders.refunded_mco` | integer | No (default 0) | `>= 0` e `<= charged_mco` | — |
> 267:| `video_renders.storage_key` | text | Yes (até `done`) | objeto existe no bucket; vídeo ≥ 100KB | "Asset de vídeo não persistido." |
> 268:| `video_renders.product_id` | uuid | Yes | FK product do tenant (se product-aware) | "Produto não encontrado." |
> 269:| `video_renders.voice_consent` | boolean | No (default false) | `true` exigido se clonagem de voz identificável | "Consentimento de voz obrigatório para clonagem." |
> 287:| FR-VS-021/022/023 | ✅ | ✅ | ✅ | AT-VS-021..023 — embed nativo carrega; rota não sombreada; botão Video navega (E2E 1920×1080) |
> 288:| FR-VS-024 | ✅ | ✅ | ✅ | AT-VS-024 — 2 renders byte-idênticos (`sha256sum`) |
> 289:| FR-VS-025 | ✅ | ✅ | — | AT-VS-025 — `/security-review`; HTML não alcança rede/env; zero cred no sandbox |
> 296:- Integration / smoke (zero-cost gates): `scripts/qa/smoke-video-faceless.ts`, `scripts/qa/smoke-video-hyperframes.ts`, `scripts/qa/smoke-video-auth.ts`, `scripts/qa/smoke-video-byok.ts`
> 297:- E2E (logado, 1920×1080): `scripts/qa/e2e-user-zero/flows/video-studio.json` + `e2e/video-studio.spec.ts`
> 313:| PR-VS-009 | FR-VS-021, FR-VS-022, FR-VS-023 | NFR-VS-003, NFR-VS-017 |
> 314:| PR-VS-010 | FR-VS-025 | NFR-VS-009 |
> 315:| PR-VS-011 | FR-VS-010, FR-VS-024 | NFR-VS-002, NFR-VS-006, NFR-VS-016 |
> 322:| (UX house style) | FR-VS-021, FR-VS-023 | NFR-VS-017 |
> 336:> - Amend de `video_renders`/`video_scenes`/`video_assets`/`video_templates`/`affiliate_links`/ledger mcoCoins: **ADD `org_id` + `client_id` nullable** (NULL = solo-creator; setado = escopo de um cliente da agência). RLS estendida de `user_id = auth.uid()` para `user_id = auth.uid() OR org_id IN (SELECT org_id FROM organization_members WHERE user_id = auth.uid() AND seat_active)`.
> 368:| FR-VS-037 | Per-client render scoping | `video-faceless-render` / `video-hyperframes-render` aceitam `org_id` + `client_id` opcionais; quando setados, o render escreve `video_renders.org_id/client_id` (e `video_scenes`/`video_assets` herdam) — **amenda FR-VS-014/FR-VS-024**. NULL = solo-creator (backward-compat). `client_id` de outra org → 403. BYOK resolve por `clients.byok_ref` (per-client) antes do per-user (R1 estendido). | Critical | PR-VS-025 | EdgeFunction | AT-VS-037 |
> 396:| NFR-VS-021 | Security (White-label TLS) | Domínio white-label (`custom_domain`) servido com TLS válido (CF→origin); domínio de uma org não resolve recursos de outra (anti-hijack); provisão de cert documentada (OTD-VS-011) | TLS A; 0 cross-domain resolution | Handshake por origin `--resolve` + cert check |
> 
> === video-studio 05-sdd: secrets table (§2.3 drift) + webhook ===
> 67:**Regras do layer map:** componentes display-only → hooks (toda lógica de dados) → edge functions (ops sensíveis) → tabelas RLS. O plano de dados quente (legs do pipeline, billing, mesh) NUNCA passa pelo frontend — o débito vive na edge function, o render vive no container, ambos falando com o Supabase por PostgREST/RPC com o secret de nome `SB_SECRET_KEY` (server-side only · NFR-VS-010).
> 116:- **Execução:** motor de steps async nativo (padrão `orchestrate-content`/`orchestrate-step` + `vision_jobs`/`finalize_*`). O `video-render` (Fatia 1) muda **só o destino do trigger** — em vez de webhook n8n, dispara a orquestração nativa; o contrato (JWT → BYOK → `deduct_mco_coins` → INSERT `video_renders` queued → 202 → poll → `finalize_video_render` refund idempotente) fica **idêntico**.
> 152:### 2.3 New Edge Functions (`supabase/functions/`)
> 154:| Function | Path | Auth | mcoCoins | Secrets needed (NOMES) |
> 156:| `video-faceless-render` | `supabase/functions/video-faceless-render/index.ts` | JWT (user) | `VIDEO_FACELESS_RENDER` (deduct na entrada) | `SB_SECRET_KEY`, `VIDEO_STUDIO_PAT` (studio identity), `N8N_WEBHOOK_URL` |
> 157:| `video-hyperframes-render` | `supabase/functions/video-hyperframes-render/index.ts` | JWT (user) | `VIDEO_HYPERFRAMES_RENDER` (deduct na entrada) | `SB_SECRET_KEY`, `HYPERFRAMES_RENDER_DISPATCH` |
> 188:| `user_api_keys.gemini_api_key` (reuso) / `.<video_provider>_api_key` | Columns (VIEW Vault family) | BYOK de provider de vídeo (padrão Vault `vault_upsert_secret` idempotente) | `<ts>_video_studio_byok.sql` |
> 238: │                    │                       │                       │──deduct_mco_coins(uid, VIDEO_HYPERFRAMES_RENDER)─▶ 402
> 340:// deduction point: ~L45 — deduct_mco_coins(user.id, COIN_COSTS.VIDEO_HYPERFRAMES_RENDER, 'video.hyperframes').
> 366:| `VIDEO_HYPERFRAMES_RENDER` | ~12 (render local barato; análogo IMAGE_GENERATION 9–12) | idem | medir custo de compute do sandbox |
> 439:### 5.4 Secrets Inventory (POR NOME — nunca valores)
> 441:| Secret Name | Used In | Vault Location | Rotation Policy |
> 450:> ⚠️ NUNCA commitar valores de secret. Apenas NOMES de chave aparecem na documentação.
> ```

## 🤖 Claude *(03:07:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "offset": 412,
  "limit": 20
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 412	## 8. Open Technical Decisions
> 413	
> 414	> Coluna **Status** alinhada com a tabela do `00-index.md` (mesma fonte).
> 415	
> 416	| ID | Description | Option A | Option B | Recommendation | Status | Owner |
> 417	|----|-------------|----------|----------|----------------|--------|-------|
> 418	| OTD-VA-001 | Tabela de métricas | Estender `campaign_metrics` (campaign-level) | Nova `creative_metrics` (por content_variant_id) | **B** — `creative_metrics` é a unidade canônica de métrica do viral-autopilot; **`campaign_metrics` fica DEPRECADA p/ este módulo** (não há FR de ETL — o loop R3 lê só `creative_metrics`). ROIWidget/Analytics legados que leem `campaign_metrics` permanecem, mas o autopilot não os alimenta | Decided | Sovereign |
> 419	| OTD-VA-002 | Infra de cron | pg_cron (como `nurture-advance`) | OS crontab (como `auto-publish`) | **A** — pg_cron service-role, consistente com o cron de cadência existente | Open | Sovereign |
> 420	| OTD-VA-003 | Fonte de engajamento orgânico | Só cliques de afiliado (sempre disponível) | + insights de API por rede (tier-dependente) | **Ambos faseado** — cliques no MVP; orgânico best-effort gated por tier (Twitter Basic, LinkedIn, Meta) | Open | Sovereign |
> 421	| OTD-VA-004 | Unidade do teto de custo | Por ciclo (no plano) | Diário global por tenant | **Ambos** — cap por ciclo (FR-VA-007) + safety diário global (**FR-VA-021**, computado de `autopilot_cycles`, espelha `vision-mcp`) | Decided (FR-VA-007+021) | Sovereign |
> 422	| OTD-VA-005 | Reinjeção de feedback | Texto cru do `optimization_policy` no prompt | Features estruturadas (top hook/produto/horário/formato) | **B** — estruturado mantém o prompt enxuto e auditável; valores = dados, nunca instrução | Open | Sovereign |
> 423	| OTD-VA-006 | Autonomia de seleção de produto | Auto-score por comissão+trend | Shortlist curada pelo Sovereign | **Shortlist (3 SKUs) no MVP** (Decisão 4); auto-score em v1.0 (PR-VA-010) | Decided (seeds) | Sovereign |
> 424	| OTD-VA-007 | Secret de postback per-user (herdada `OTD-ML-MP-PER-USER`) | Manter secret global (Usuário Zero) | Per-user `meta`/MP config | **B antes de multi-tenant** — atribuição de receita por tenant exige secret per-user | Open (herdada) | Sovereign |
> 425	| OTD-VA-008 | Identidade do caminho cron→`orchestrate-content` (o cron não tem JWT; a fn rejeita sem `Bearer`) | Repassar JWT (impossível — cron não tem) | Service-role + `x-autopilot-user-id` derivado de `autopilot_plans.user_id` + pré-débito atômico em `autopilot-run` (sub-runs `prepaid`) | **B** — server-trusted, nunca do body; resolve blocker SEC-VA-01 + TOCTOU SEC-VA-04. **Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer código** | Open (SOP-gated) | Sovereign |
> 426	
> 427	> **Gate Lei 2 (Processo Antecipado):** o caminho de identidade do cron (OTD-VA-008) e o pré-débito/refund (FR-VA-007) introduzem automação financeira nova → o SOP `docs/processes/autopilot-cron-identity.md` DEVE ser escrito e revisado **antes** de a fatia de cadência/custo ganhar código. Referência cruzada: SOP `orchestrate-async-pipeline.md` (mandato `verify_jwt=false`).
> 428	
> 429	---
> 430	
> 431	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> ```

## 🤖 Claude *(03:09:05)*


## 🤖 Claude *(03:09:07)*

The video-studio BoK **already fully specifies** the HyperFrames editor + motor (FR-VS-021..025, NFR-VS-002 = 1080×1920, the `video-hyperframes-render` contract, the `/security-review` sandbox gate). So the editor/motor need **no** BoK amendment — only implementation. The amendment work is purely the **viral-autopilot↔video integration** + reconciling the video-studio secrets drift the synthesis flagged.

Let me read the FRD tail (traceability + end) and the video-studio secrets table to place the amendments cleanly.

## 🤖 Claude *(03:09:08)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "offset": 165,
  "limit": 35
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 165	
> 166	**Test files location:**
> 167	- Unit: `src/hooks/__tests__/useAutopilot.test.ts`
> 168	- Integration / smokes: `scripts/qa/smoke-autopilot-run.ts`, `scripts/qa/smoke-autopilot-budget.ts` (zero-cost)
> 169	- E2E: `e2e/viral-autopilot.spec.ts` + gate `/e2e-audit` 1920×1080 para `AutopilotPage`
> 170	
> 171	---
> 172	
> 173	## 7. Traceability Matrix
> 174	
> 175	| PR ID | FR ID | NFR ID |
> 176	|-------|-------|--------|
> 177	| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |
> 178	| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |
> 179	| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |
> 180	| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |
> 181	| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |
> 182	| PR-VA-006 | FR-VA-007, FR-VA-021 | NFR-VA-002 |
> 183	| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |
> 184	| PR-VA-008 | FR-VA-013 | NFR-VA-008 |
> 185	| PR-VA-010 | FR-VA-012 | — |
> 186	| PR-VA-011 | FR-VA-018 | — |
> 187	| PR-VA-012 | FR-VA-019 | — |
> 188	| PR-VA-013 | FR-VA-020 | — |
> 189	
> 190	> Cobertura: 21 FR (FR-VA-001..021) · 8 NFR. PRs de Fase 2/Future (PR-VA-020/021/022) não decompostos neste ciclo (FRD §1). Todo PR Must/Should rastreia ≥1 FR; todo FR rastreia ≥1 PR. **Gaps de numeração intencionais:** PR-VA-009 (saltado 008→010 entre Must e Should) e FR-VA-014..018 contínuos — sem buracos de conteúdo.
> 191	
> 192	---
> 193	
> 194	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 195	
> ```

## 🤖 Claude *(03:09:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md",
  "offset": 152,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 152	### 2.3 New Edge Functions (`supabase/functions/`)
> 153	
> 154	| Function | Path | Auth | mcoCoins | Secrets needed (NOMES) |
> 155	|----------|------|------|----------|------------------------|
> 156	| `video-faceless-render` | `supabase/functions/video-faceless-render/index.ts` | JWT (user) | `VIDEO_FACELESS_RENDER` (deduct na entrada) | `SB_SECRET_KEY`, `VIDEO_STUDIO_PAT` (studio identity), `N8N_WEBHOOK_URL` |
> 157	| `video-hyperframes-render` | `supabase/functions/video-hyperframes-render/index.ts` | JWT (user) | `VIDEO_HYPERFRAMES_RENDER` (deduct na entrada) | `SB_SECRET_KEY`, `HYPERFRAMES_RENDER_DISPATCH` |
> 158	| `video-render-poll` | `supabase/functions/video-render-poll/index.ts` | JWT (user) | 0 (read) | `SB_SECRET_KEY` |
> 159	| `delete-account` (EXTENSÃO) | `supabase/functions/delete-account/index.ts` | JWT (user) | 0 | `SB_SECRET_KEY` (cascade erasure FR-VS-031) |
> 160	
> 161	> Todas seguem o JWT stub do §5.3. BYOK resolvido per-user via `decrypted_user_api_keys` (§5.6). `deduct_mco_coins` é a ÚNICA forma de débito (R2).
> 162	
> 163	### 2.4 Container Service Modules
> ```

## 🤖 Claude *(03:09:17)*


## 🤖 Claude *(03:09:17)*

I have full grounding. Marking the BoK gate task in progress and authoring the amendment.

## 🤖 Claude *(03:09:18)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskUpdate",
  "max_results": 2
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskUpdate'}]
> ```

## 🤖 Claude *(03:09:21)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #1 status
> ```

## 🤖 Claude *(03:09:21)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "3",
  "addBlockedBy": [
    "1",
    "2"
  ]
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #3 blockedBy
> ```

## 🤖 Claude *(03:09:30)*


## 🤖 Claude *(03:09:31)*

Now authoring the FRD amendment. First the scope statement (§1) — move video 9:16 *generation* into scope via Amendment v0.2, keep *publishing* deferred:

## 🤖 Claude *(03:09:42)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "**Out of scope (Fase 2 / Won't):** gera\u00e7\u00e3o de v\u00eddeo 9:16; publica\u00e7\u00e3o em TikTok/Instagram/YouTube; gest\u00e3o de an\u00fancios pagos; atribui\u00e7\u00e3o multi-touch cross-network; auto-descoberta de cat\u00e1logo (CLI manual permanece).\n\n> **Nota de escopo de rastreabilidade:** os PRs de Fase 2 / Future (PR-VA-020 v\u00eddeo 9:16, PR-VA-021 TikTok/IG/YT, PR-VA-022 auto-discovery de cat\u00e1logo) s\u00e3o **intencionalmente N\u00c3O decompostos em FR neste ciclo** \u2014 n\u00e3o aparecem nas matrizes MR\u2192PR\u2192FR ativas (PRD \u00a78 / \u00a77 abaixo). Ser\u00e3o decompostos quando o Sovereign priorizar a Fase 2 (precedente: `marketing-hub` PR-MH-020..023).",
  "new_string": "**In scope (Amendment v0.2 \u2014 2026-06-24):** **gera\u00e7\u00e3o de v\u00eddeo vertical 9:16** product-aware no ciclo aut\u00f4nomo, rendered pelo motor determin\u00edstico HyperFrames do `video-studio` (FR-VS-024/025) \u2014 decomp\u00f5e PR-VA-020 em FR-VA-022..026 (\u00a72.A abaixo). Diretiva Sovereign 2026-06-24 (\"fechar o v\u00eddeo 9:16 com a UI editor do HyperFrames, assim como o open-design\"; alvo = **integra\u00e7\u00e3o Autopilot primeiro**).\n\n**Out of scope (Fase 2 / Won't):** publica\u00e7\u00e3o aut\u00f4noma em TikTok/Instagram/YouTube (PR-VA-021 \u2014 diferida em OTD-VA-012: depende de OAuth + App Review = a\u00e7\u00e3o Sovereign; o asset 9:16 anexa a `scheduled_posts`/`content_library` hoje); gest\u00e3o de an\u00fancios pagos; atribui\u00e7\u00e3o multi-touch cross-network; auto-descoberta de cat\u00e1logo (CLI manual permanece).\n\n> **Nota de escopo de rastreabilidade:** PR-VA-020 (v\u00eddeo 9:16) **passa a ser decomposto** em FR-VA-022..026 pela Amendment v0.2 (\u00a72.A + Traceability \u00a77). PR-VA-021 (TikTok/IG/YT) e PR-VA-022 (auto-discovery de cat\u00e1logo) seguem **intencionalmente N\u00c3O decompostos** \u2014 ser\u00e3o decompostos quando o Sovereign priorizar (precedente: `marketing-hub` PR-MH-020..023). **Gate Lei 2:** todo c\u00f3digo de v\u00eddeo no pipeline exige o SOP `docs/processes/autopilot-video-9x16.md` ANTES (OTD-VA-009, espelha o gate OTD-VA-008)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:09:51)*


## 🤖 Claude *(03:09:52)*

Now the §2.A amendment block with the decomposed FRs (FR-VA-022..026), inserted before the NFR section:

## 🤖 Claude *(03:10:21)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "## 3. Non-Functional Requirements",
  "new_string": "## 2.A Amendment v0.2 \u2014 PR-VA-020 Video creative 9:16 (decomposi\u00e7\u00e3o)\n\n> **Selada por:** Diretiva Sovereign 2026-06-24. **Motor:** HyperFrames determin\u00edstico (`video-studio` FR-VS-024 \u2014 `video-hyperframes-render`/`video-render` engine=`hyperframes`; HTML\u2192MP4 1080\u00d71920 via Chrome headless + FFmpeg), **n\u00e3o** IA-DoP (OTD-VA-009). **Cobran\u00e7a:** `VIDEO_HYPERFRAMES_RENDER` (~12 mco) **dentro do pr\u00e9-d\u00e9bito do ciclo** (FR-VA-007 estendido \u2014 OTD-VA-010, contabilizado UMA vez, sub-render `prepaid`). **Tenancy:** o autopilot do Usu\u00e1rio Zero renderiza **seus pr\u00f3prios templates** (single-tenant) \u2014 hardening multi-tenant do sandbox (FR-VS-025 / FMEA-VS-001 RPN 200) **diferido** para o Usu\u00e1rio 1 (OTD-VA-011). O Autopilot **chama** o motor do `video-studio`; **n\u00e3o** o constr\u00f3i (motor = Fatia VS-2, BoK `video-studio` j\u00e1 selada).\n\n| ID | Title | Description | Priority | PR Traced | Category | Test ID |\n|----|-------|-------------|----------|-----------|----------|---------|\n| FR-VA-022 | Plan video opt-in | `autopilot_plans` ganha `video_enabled boolean DEFAULT false` + `video_format text DEFAULT '9:16' CHECK (video_format IN ('9:16'))` (extens\u00edvel). Opt-in por plano (default off = backward-compat com ciclos texto+imagem). Quando `true`, cada sub-run product-aware ganha **um** render de v\u00eddeo 9:16. Exposto no `useAutopilot`/`AutopilotPage` (FR-VA-014/015). | High | PR-VA-020 | DB/UI | AT-VA-022 |\n| FR-VA-023 | Product-aware 9:16 composition | Em `orchestrate-step`, quando `video_enabled`, monta uma **composi\u00e7\u00e3o HTML 1080\u00d71920** a partir do produto-alvo (imagem do produto \u2014 reusa o asset de FR-VA-013 \u2014 + gancho viral + caption + CTA + branding) usando um **template de short determin\u00edstico**. As 3 fontes n\u00e3o-confi\u00e1veis (nome/desc de produto, texto de trend FR-VA-018, `optimization_policy` FR-VA-011) s\u00e3o **sanitizadas/escapadas** antes de entrar no HTML (NFR-VA-008 + Cyber-Sentinel fail-closed, espelha `orchestrate-content:92`). | High | PR-VA-020 | Lib/EdgeFunction | AT-VA-023 |\n| FR-VA-024 | Enqueue HyperFrames render (prepaid) | O ciclo enfileira **um** `video_render(engine='hyperframes', prepaid=true)` via o motor `video-studio` por sub-run com v\u00eddeo. O motor **n\u00e3o cobra** no caminho `prepaid` (espelha `orchestrate-content` FR-VA-016 \u2014 d\u00e9bito j\u00e1 feito no pr\u00e9-d\u00e9bito do ciclo FR-VA-007). Identidade do caminho cron = service-role + `user_id` server-trusted derivado da linha (`autopilot_cycles`/`autopilot_plans`, **nunca do body** \u2014 OTD-VA-008). `video_render.product_id` = produto-alvo do sub-run. | Critical | PR-VA-020 | EdgeFunction | AT-VA-024 |\n| FR-VA-025 | Async asset reconciliation + attach | Render \u00e9 ass\u00edncrono e **pode chegar depois** do `finalize_autopilot_cycle`. Um poller de reconcilia\u00e7\u00e3o (estilo `autopilot-collect`/`rescue-video`, service-role, `user_id` da linha) detecta `video_render.state='done'`, l\u00ea `storage_key` (asset \u2265 100KB), e **anexa** o v\u00eddeo ao criativo: `content_library` linha `type='video'` (`media_url` = signed/durable path no bucket privado `video-studio-assets`) + 1 linha `creative_metrics` por `content_variant_id` (FR-VA-009) + `scheduled_posts.content_id`. Falha de render = **fail-open `skipped`** (espelha Fatia 1b \u2014 n\u00e3o derruba o ciclo de texto/imagem). | High | PR-VA-020 | Cron/EdgeFunction | AT-VA-025 |\n| FR-VA-026 | Vertical-network publish (DIFERIDO) | Publica\u00e7\u00e3o aut\u00f4noma em TikTok/IG Reels/YT Shorts \u00e9 **diferida** (PR-VA-021, OTD-VA-012 \u2014 depende de OAuth + App Review = a\u00e7\u00e3o Sovereign, espelha o deferral do IG App Review existente). Nesta amendment o asset 9:16 **anexa a `scheduled_posts`/`content_library`** (destino atual: superf\u00edcies j\u00e1 public\u00e1veis + biblioteca para download/uso manual). Quando os destinos verticais acenderem, herdam o asset por `content_id`. | Deferred | PR-VA-021 | EdgeFunction | AT-VA-026 |\n\n> **Extens\u00e3o do cost-guardrail (FR-VA-007):** o custo projetado passa a `N_runs \u00d7 ORCHESTRATION_RUN(10) + N_video \u00d7 VIDEO_HYPERFRAMES_RENDER(12) + ANALYZE_COST(2)`, onde `N_video = N_runs` quando `video_enabled`, sen\u00e3o `0`. O pr\u00e9-d\u00e9bito at\u00f4mico, o refund cr\u00e9dito-positivo idempotente (`finalize_autopilot_cycle`) e o cap di\u00e1rio (FR-VA-021) **absorvem o custo de v\u00eddeo sem mudan\u00e7a de RPC** \u2014 s\u00f3 recalculam `projected`. Caps do plano (default 200) e cap di\u00e1rio (default 100 em `canvas-execute`; o autopilot computa seu pr\u00f3prio cap de `autopilot_cycles`) devem comportar o acr\u00e9scimo (OTD-VA-010).\n\n---\n\n## 3. Non-Functional Requirements"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:10:24)*


## 🤖 Claude *(03:10:24)*

Now the traceability matrix (§7) and coverage note:

## 🤖 Claude *(03:10:30)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| PR-VA-013 | FR-VA-020 | \u2014 |\n\n> Cobertura: 21 FR (FR-VA-001..021) \u00b7 8 NFR. PRs de Fase 2/Future (PR-VA-020/021/022) n\u00e3o decompostos neste ciclo (FRD \u00a71). Todo PR Must/Should rastreia \u22651 FR; todo FR rastreia \u22651 PR. **Gaps de numera\u00e7\u00e3o intencionais:** PR-VA-009 (saltado 008\u2192010 entre Must e Should) e FR-VA-014..018 cont\u00ednuos \u2014 sem buracos de conte\u00fado.",
  "new_string": "| PR-VA-013 | FR-VA-020 | \u2014 |\n| PR-VA-020 _(Amendment v0.2)_ | FR-VA-022, FR-VA-023, FR-VA-024, FR-VA-025 | NFR-VA-002, NFR-VA-008 |\n| PR-VA-021 _(diferido)_ | FR-VA-026 | \u2014 |\n\n> Cobertura: **26 FR (FR-VA-001..026)** \u00b7 8 NFR. Amendment v0.2 decomp\u00f5e PR-VA-020 (v\u00eddeo 9:16) em FR-VA-022..025 (+ FR-VA-026 diferido p/ PR-VA-021). PR-VA-022 (auto-discovery) segue n\u00e3o decomposto. Todo PR Must/Should rastreia \u22651 FR; todo FR rastreia \u22651 PR. **Gaps de numera\u00e7\u00e3o intencionais:** PR-VA-009 (saltado 008\u2192010 entre Must e Should) e FR-VA-014..018 cont\u00ednuos \u2014 sem buracos de conte\u00fado."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:10:33)*


## 🤖 Claude *(03:10:34)*

Now the SDD — adding OTD-VA-009..012 and extending the Law 2 gate. Inserting after OTD-VA-008:

## 🤖 Claude *(03:11:00)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "| OTD-VA-008 | Identidade do caminho cron\u2192`orchestrate-content` (o cron n\u00e3o tem JWT; a fn rejeita sem `Bearer`) | Repassar JWT (imposs\u00edvel \u2014 cron n\u00e3o tem) | Service-role + `x-autopilot-user-id` derivado de `autopilot_plans.user_id` + pr\u00e9-d\u00e9bito at\u00f4mico em `autopilot-run` (sub-runs `prepaid`) | **B** \u2014 server-trusted, nunca do body; resolve blocker SEC-VA-01 + TOCTOU SEC-VA-04. **Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer c\u00f3digo** | Open (SOP-gated) | Sovereign |\n\n> **Gate Lei 2 (Processo Antecipado):** o caminho de identidade do cron (OTD-VA-008) e o pr\u00e9-d\u00e9bito/refund (FR-VA-007) introduzem automa\u00e7\u00e3o financeira nova \u2192 o SOP `docs/processes/autopilot-cron-identity.md` DEVE ser escrito e revisado **antes** de a fatia de cad\u00eancia/custo ganhar c\u00f3digo. Refer\u00eancia cruzada: SOP `orchestrate-async-pipeline.md` (mandato `verify_jwt=false`).",
  "new_string": "| OTD-VA-008 | Identidade do caminho cron\u2192`orchestrate-content` (o cron n\u00e3o tem JWT; a fn rejeita sem `Bearer`) | Repassar JWT (imposs\u00edvel \u2014 cron n\u00e3o tem) | Service-role + `x-autopilot-user-id` derivado de `autopilot_plans.user_id` + pr\u00e9-d\u00e9bito at\u00f4mico em `autopilot-run` (sub-runs `prepaid`) | **B** \u2014 server-trusted, nunca do body; resolve blocker SEC-VA-01 + TOCTOU SEC-VA-04. **Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer c\u00f3digo** | Open (SOP-gated) | Sovereign |\n| OTD-VA-009 _(Amendment v0.2)_ | Motor do v\u00eddeo 9:16 do Autopilot | **A** \u2014 HyperFrames determin\u00edstico (`video-studio` FR-VS-024; HTML\u2192MP4 1080\u00d71920; ~12 mco; on-brand templated; reusa a imagem de produto de FR-VA-013 como camada) | **B** \u2014 Canvas DoP IA (`canvas-execute` image_to_video; ~125 mco; 9:16 herdado da imagem-base, n\u00e3o provado; ass\u00edncrono webhook) | **A** \u2014 diretiva Sovereign 2026-06-24: determin\u00edstico, barato, alinhado \u00e0 vis\u00e3o \"UI editor do HyperFrames\". **Gate Lei 2: exige SOP `docs/processes/autopilot-video-9x16.md` ANTES de qualquer c\u00f3digo de v\u00eddeo** (espelha OTD-VA-008) | Decided (SOP-gated) | Sovereign |\n| OTD-VA-010 _(Amendment v0.2)_ | Contabilidade do custo de v\u00eddeo no ciclo | D\u00e9bito interno do motor (FR-VS-010, `video-render` deduz na entrada) | Contabilizado **uma vez** no pr\u00e9-d\u00e9bito do ciclo (FR-VA-007 estendido); sub-render `prepaid=true` suprime o deduct do motor (espelha `orchestrate-content` FR-VA-016) | **B** \u2014 evita dupla cobran\u00e7a; `projected += N_video \u00d7 VIDEO_HYPERFRAMES_RENDER`; `begin/finalize_autopilot_cycle` inalterados (s\u00f3 recalc). Caps do plano/di\u00e1rio devem comportar +12/sub-run | Decided | Sovereign |\n| OTD-VA-011 _(Amendment v0.2)_ | Tenancy do motor HyperFrames p/ o Autopilot | Render multi-tenant hardened j\u00e1 (FR-VS-025 / FMEA-VS-001 RPN 200 \u2014 container ef\u00eamero selado, egress-only, zero cred) | Single-tenant Usu\u00e1rio Zero agora (renderiza **seus pr\u00f3prios** templates, baixo vetor de HTML n\u00e3o-confi\u00e1vel) + `/security-review`; hardening multi-tenant **diferido p/ Usu\u00e1rio 1** | **B antes de multi-tenant** \u2014 espelha os deferrals Stripe/IG existentes; Owner absorve o blast radius single-tenant. Acende o gate 503 do `video-render` s\u00f3 p/ o tenant 0 | Decided (deferral) | Sovereign |\n| OTD-VA-012 _(Amendment v0.2)_ | Destino do asset 9:16 (publisher) | Publicar aut\u00f4nomo em TikTok/IG/YT j\u00e1 (PR-VA-021) | Anexar a `scheduled_posts`/`content_library` agora; publish vertical **diferido** (OAuth + App Review = a\u00e7\u00e3o Sovereign) | **B** \u2014 PR-VA-021 \u00e9 XL e gated por OAuth/App Review (espelha o deferral do IG App Review); FR-VA-026 herda o asset por `content_id` quando os destinos acenderem | Open (herda PR-VA-021) | Sovereign |\n\n> **Gate Lei 2 (Processo Antecipado):** o caminho de identidade do cron (OTD-VA-008) e o pr\u00e9-d\u00e9bito/refund (FR-VA-007) introduzem automa\u00e7\u00e3o financeira nova \u2192 o SOP `docs/processes/autopilot-cron-identity.md` DEVE ser escrito e revisado **antes** de a fatia de cad\u00eancia/custo ganhar c\u00f3digo. Refer\u00eancia cruzada: SOP `orchestrate-async-pipeline.md` (mandato `verify_jwt=false`).\n>\n> **Gate Lei 2 \u2014 Amendment v0.2 (v\u00eddeo 9:16):** a gera\u00e7\u00e3o de v\u00eddeo no ciclo (FR-VA-022..025, OTD-VA-009/010) adiciona (a) **automa\u00e7\u00e3o financeira nova** (custo de v\u00eddeo no pr\u00e9-d\u00e9bito) e (b) uma **depend\u00eancia de render externa** (motor HyperFrames + reconcilia\u00e7\u00e3o ass\u00edncrona) \u2192 o SOP `docs/processes/autopilot-video-9x16.md` DEVE ser escrito e revisado **antes** da Fatia VA-V1 ganhar c\u00f3digo (Operator/Sequence/Verification/Recovery/Success). O motor single-tenant (OTD-VA-011) exige `/security-review` do sandbox de render. Cross-ref: `video-studio` SDD (FR-VS-024/025) + SOP `autopilot-cron-identity.md`."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:11:06)*


## 🤖 Claude *(03:11:07)*

Now annotating the PRD to reflect PR-VA-020 is decomposed. Updating the Could-Have entry and the Future Scope condition:

## 🤖 Claude *(03:11:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "old_string": "| PR-VA-020 | **Video creative 9:16** (TikTok/Reels/Shorts) | P1 | BR-VA-001 | XL | v\u00eddeo cost | Fase 2 (Decis\u00e3o 2); `generate-video` hoje \u00f3rf\u00e3 |",
  "new_string": "| PR-VA-020 | **Video creative 9:16** (TikTok/Reels/Shorts) | P1 | BR-VA-001 | XL | ~12 mco (HyperFrames) | **DECOMPOSTO \u2014 FRD Amendment v0.2 (2026-06-24): FR-VA-022..025.** Motor = HyperFrames determin\u00edstico (`video-studio` FR-VS-024), n\u00e3o `generate-video` IA (OTD-VA-009). Single-tenant Usu\u00e1rio Zero (OTD-VA-011) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:11:14)*


## 🤖 Claude *(03:11:14)*

Now the PRD §8 traceability note and Future-Scope condition:

## 🤖 Claude *(03:11:17)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "old_string": "> Matriz **autoritativa** da cadeia MR\u2192BR\u2192PR (id\u00eantica \u00e0 BRD \u00a710). PRs de Fase 2/Future (PR-VA-020/021/022) n\u00e3o entram \u2014 n\u00e3o decompostos neste ciclo (FRD \u00a71).",
  "new_string": "> Matriz **autoritativa** da cadeia MR\u2192BR\u2192PR (id\u00eantica \u00e0 BRD \u00a710). PR-VA-020 (v\u00eddeo 9:16) **passa a ser decomposto** na FRD Amendment v0.2 (FR-VA-022..025). PR-VA-021/022 seguem n\u00e3o decompostos (FRD \u00a71)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:11:26)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "old_string": "**Items:** PR-VA-020, PR-VA-021, PR-VA-022  \n**Condition:** ap\u00f3s MVP validado e decis\u00e3o Sovereign de priorizar m\u00eddia viral (v\u00eddeo 9:16 + redes virais) \u2014 gate de esfor\u00e7o XL.",
  "new_string": "**Items:** ~~PR-VA-020~~ (promovido \u2014 FRD Amendment v0.2, 2026-06-24), PR-VA-021, PR-VA-022  \n**Condition:** ap\u00f3s MVP validado e decis\u00e3o Sovereign de priorizar m\u00eddia viral (v\u00eddeo 9:16 + redes virais) \u2014 gate de esfor\u00e7o XL. **PR-VA-020 (gera\u00e7\u00e3o 9:16) foi promovido** por diretiva Sovereign 2026-06-24 via motor HyperFrames determin\u00edstico (custo XL\u2192M); PR-VA-021 (publish vertical) permanece Future (OAuth + App Review)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:11:31)*


## 🤖 Claude *(03:11:32)*

Now reconciling the video-studio SDD §2.3 secrets drift the synthesis flagged (the sealed table still lists pre-De-n8n `N8N_WEBHOOK_URL`/`HYPERFRAMES_RENDER_DISPATCH`, and the shipped Fatia 1 consolidated into one `video-render` fn). Adding a reconciliation annotation rather than rewriting the sealed table:

## 🤖 Claude *(03:11:41)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md",
  "old_string": "> Todas seguem o JWT stub do \u00a75.3. BYOK resolvido per-user via `decrypted_user_api_keys` (\u00a75.6). `deduct_mco_coins` \u00e9 a \u00daNICA forma de d\u00e9bito (R2).",
  "new_string": "> Todas seguem o JWT stub do \u00a75.3. BYOK resolvido per-user via `decrypted_user_api_keys` (\u00a75.6). `deduct_mco_coins` \u00e9 a \u00daNICA forma de d\u00e9bito (R2).\n>\n> **\ud83d\udd27 Reconcilia\u00e7\u00e3o de drift (2026-06-24 \u00b7 cross-ref Amendment v0.2 do `viral-autopilot`):** a tabela acima reflete o design **pr\u00e9-De-n8n** (SDD \u00a78-A v1.2). A implementa\u00e7\u00e3o da **Fatia 1 (shipped)** consolidou `video-faceless-render` + `video-hyperframes-render` numa **\u00fanica** edge fn `video-render` (branching por `engine`) + `video-render-poll`, e os secrets `N8N_WEBHOOK_URL`/`HYPERFRAMES_RENDER_DISPATCH` foram substitu\u00eddos pelos **gates de env `VIDEO_FACELESS_WEBHOOK`/`VIDEO_HYPERFRAMES_WEBHOOK`** (worker-gate 503 ANTES do deduct \u2192 zero-cost na Fatia 1; `video-render/index.ts:84`). Os contratos FR-VS-010/024/025 permanecem v\u00e1lidos \u2014 realizados pela fn unificada. A **Fatia VS-2** (motor) acende esse gate via um **worker host no molde de `scripts/design-bridge.ts`** (claim at\u00f4mico de `video_renders` \u2192 render no container \u2192 `finalize_video_render`), single-tenant Usu\u00e1rio Zero primeiro (OTD-VA-011 do `viral-autopilot`)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:11:46)*


## 🤖 Claude *(03:11:47)*

The BoK amendments are placed. Now the Law-2 deliverable — the SOP. Let me match the house style of the precedent SOP (`autopilot-cron-identity.md`):

## 🤖 Claude *(03:11:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== autopilot-cron-identity.md structure (headers) ===\"\ngrep -nE \"^#{1,3} |^\\*\\*Operator|^\\| *Operator|Sequence|Verification|Recovery|Success|Gate G[0-9]\" docs/processes/autopilot-cron-identity.md | head -50\necho \"=== total lines ===\"; wc -l docs/processes/autopilot-cron-identity.md",
  "description": "Inspect precedent SOP structure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === autopilot-cron-identity.md structure (headers) ===
> 1:# SOP: Viral Autopilot — Cron Identity + Pre-Debit/Refund Atomicity (`autopilot-cron-identity`)
> 11:## Context
> 23:## ORO triplet
> 31:## Operator (equivalente manual — material)
> 49:## Topologia (alvo)
> 73:## Identity resolution order (canonical — funções `autopilot-*`, `verify_jwt=false`)
> 86:## Sequence (o tick → ciclo → finalize)
> 105:## Cost & atomicity contract (resumo executável)
> 119:## Verification gates
> 138:## Recovery path
> 148:## Success signal
> 159:## Anti-patterns proibidos
> 173:## Sibling reference
> === total lines ===
> 179 docs/processes/autopilot-cron-identity.md
> ```

## 🤖 Claude *(03:11:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/autopilot-cron-identity.md",
  "offset": 1,
  "limit": 73
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
> ```

## 🤖 Claude *(03:12:00)*


## 🤖 Claude *(03:12:00)*

The SOP house style is clear. Authoring the Law-2 gate SOP now:

## 🤖 Claude *(03:13:20)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/autopilot-video-9x16.md",
  "content": "# SOP: Viral Autopilot \u2014 V\u00eddeo Vertical 9:16 via HyperFrames (`autopilot-video-9x16`)\n\n**Status:** ACTIVE \u00b7 v1.0 \u00b7 2026-06-24\n**Owner:** Sovereign (Gabriel Zarattini)\n**Survival Law 2 compliance:** Escrito **ANTES** de qualquer c\u00f3digo da Fatia VA-V1 (integra\u00e7\u00e3o 9:16 no pipeline do Autopilot). Abre o gate **OTD-VA-009** (`docs/bok/viral-autopilot/05-sdd.md` \u2014 *\"Gate Lei 2 \u2014 Amendment v0.2: exige SOP `docs/processes/autopilot-video-9x16.md` ANTES de qualquer c\u00f3digo de v\u00eddeo\"*) e cobre FR-VA-022..026 + a extens\u00e3o de custo de FR-VA-007.\n**Canonical directive:** `CLAUDE.md > MCORCH Master Execution Protocol` (Closed-Loop) \u00b7 `.claude/rules/survival.md > Law 1/Law 2` \u00b7 `docs/bok/viral-autopilot/{03-prd,04-frd,05-sdd}.md` (Amendment v0.2) \u00b7 `docs/bok/video-studio/{04-frd,05-sdd}.md` (FR-VS-024/025 motor + sandbox).\n**Sibling SOPs:** `autopilot-cron-identity.md` (identidade cron + pr\u00e9-d\u00e9bito/refund \u2014 **base financeira deste**) \u00b7 `orchestrate-async-pipeline.md` (`verify_jwt=false` + pg_net + contrato de RPC) \u00b7 `build-deploy-materiality.md` (worker host \u2260 worktree) \u00b7 `canvas-video-async-execution.md` (precedente de render async + reconcilia\u00e7\u00e3o).\n\n---\n\n## Context\n\nA Amendment v0.2 do `viral-autopilot` adiciona **um asset de v\u00eddeo vertical 9:16** a cada sub-run product-aware, quando o plano opta (`video_enabled`). O v\u00eddeo \u00e9 renderizado pelo **motor determin\u00edstico HyperFrames** do `video-studio` (HTML\u2192MP4 1080\u00d71920 via Chrome headless + FFmpeg \u2014 FR-VS-024/025), **n\u00e3o** por IA (OTD-VA-009 escolha A). Tr\u00eas riscos materiais nascem disso:\n\n1. **Render de HTML n\u00e3o-confi\u00e1vel (FMEA-VS-001 RPN 200 / FR-VS-025).** A composi\u00e7\u00e3o 9:16 mistura 3 fontes n\u00e3o-confi\u00e1veis (nome/descri\u00e7\u00e3o de produto ML, texto de trend `vm_trends`, `optimization_policy` reinjetado) dentro de um HTML que um Chrome headless executa. Se o HTML escapar do template e injetar `<script>`/`fetch`, um render pode exfiltrar segredos do ambiente ou bater na rede interna. **Mitiga\u00e7\u00e3o desta fase:** (a) Cyber-Sentinel fail-closed + escape das 3 fontes ANTES de entrarem no HTML (espelha `orchestrate-content:92`); (b) o motor roda **single-tenant Usu\u00e1rio Zero** (OTD-VA-011), renderizando **templates do pr\u00f3prio tenant 0** \u2014 o hardening multi-tenant (container ef\u00eamero selado, egress-only, zero credencial no env, `cap_drop=ALL`) \u00e9 **diferido** para o Usu\u00e1rio 1, mas o `/security-review` do worker \u00e9 **obrigat\u00f3rio** j\u00e1 agora.\n\n2. **Dupla cobran\u00e7a (OTD-VA-010 / TOCTOU financeiro).** O motor `video-render` deduz `VIDEO_HYPERFRAMES_RENDER` na entrada (FR-VS-010). O ciclo do Autopilot **j\u00e1 pr\u00e9-debitou** o custo de v\u00eddeo no `begin_autopilot_cycle` (FR-VA-007 estendido). Se o enqueue n\u00e3o sinalizar `prepaid=true`, o tenant \u00e9 cobrado **duas vezes**. **Regra:** o caminho Autopilot\u2192motor \u00e9 **`prepaid`** (motor N\u00c3O self-bill \u2014 espelha `orchestrate-content` FR-VA-016); o \u00daNICO d\u00e9bito de v\u00eddeo \u00e9 o do pr\u00e9-d\u00e9bito do ciclo.\n\n3. **Asset ass\u00edncrono que chega depois do `finalize` (FR-VA-025).** O render \u00e9 fire-and-forget; o `finalize_autopilot_cycle` (refund) roda quando os sub-runs de **texto/imagem** terminam \u2014 o MP4 pode aterrissar **minutos depois**. Se o ciclo fechar sem reconciliar, o asset some. **Regra:** um poller de reconcilia\u00e7\u00e3o (estilo `autopilot-collect`/`rescue-video`) anexa o asset por `content_variant_id` **ap\u00f3s** o `done`, e a falha de render \u00e9 **fail-open `skipped`** \u2014 nunca derruba o ciclo de texto/imagem.\n\n**Regra-m\u00e3e:** o v\u00eddeo \u00e9 uma **camada aditiva fail-open** sobre o ciclo j\u00e1 existente. Nenhuma falha de render, sanitiza\u00e7\u00e3o ou reconcilia\u00e7\u00e3o pode (a) cobrar o tenant a mais, (b) derrubar a gera\u00e7\u00e3o de texto/imagem, ou (c) publicar HTML n\u00e3o-escapado. O custo de v\u00eddeo \u00e9 contabilizado **uma vez**, no pr\u00e9-d\u00e9bito do ciclo.\n\n---\n\n## ORO triplet\n\n- **Operator:** MCORCH Master Execution Agent (autoria da migration `video_enabled`/`video_format`, do bloco de composi\u00e7\u00e3o em `orchestrate-step`, do enqueue prepaid, do poller de reconcilia\u00e7\u00e3o) + worker host HyperFrames (render por job) + Edge runtime (enqueue + reconcile).\n- **Reviewer:** Sovereign (Gabriel) \u2014 aprova a migration + o `/security-review` **obrigat\u00f3rio** do worker de render (sandbox) + valida os smokes zero-cost \u00b7 `/security-review` independente na migration de schema.\n- **Owner:** Sovereign \u2014 blast radius = **carteira do tenant 0 gasta autonomamente** (dupla cobran\u00e7a se o prepaid falhar) + **superf\u00edcie de execu\u00e7\u00e3o de HTML** (escape de sandbox se a sanitiza\u00e7\u00e3o falhar) + **asset \u00f3rf\u00e3o** (custo pago sem entrega se a reconcilia\u00e7\u00e3o falhar).\n\n---\n\n## Operator (equivalente manual \u2014 material)\n\nO ritual humano que a automa\u00e7\u00e3o substitui, a cada sub-run de um plano com v\u00eddeo ligado:\n\n| # | Passo manual | Crit\u00e9rio de sucesso material |\n|---|--------------|------------------------------|\n| 1 | Abrir o produto-alvo do ciclo (imagem, nome, pre\u00e7o, comiss\u00e3o) + o gancho viral do \u00e2ngulo | Dados do produto + hook conferidos |\n| 2 | Compor um short 9:16 (1080\u00d71920): imagem do produto + texto do gancho + caption + CTA + branding, num template fixo | Composi\u00e7\u00e3o visual aprovada, sem texto n\u00e3o-escapado |\n| 3 | Renderizar a composi\u00e7\u00e3o em MP4 (determin\u00edstico) | MP4 \u2265 100KB, 1080\u00d71920, ratio 9:16 conferido |\n| 4 | Conferir que o custo do render saiu **uma vez** (n\u00e3o cobrar de novo se j\u00e1 pr\u00e9-pago) | Saldo debitado 1\u00d7, igual ao projetado |\n| 5 | Anexar o MP4 ao criativo daquele produto/rede (biblioteca + post agendado) | `content_library type=video` + `scheduled_posts.content_id` setados |\n| 6 | Se o render falhar, **publicar o texto/imagem mesmo assim** (n\u00e3o bloquear o ciclo) | Ciclo de texto/imagem intacto; v\u00eddeo marcado `skipped` |\n\nO passo 4 (cobran\u00e7a \u00fanica) e o passo 6 (fail-open) s\u00e3o exatamente o que o gate Lei 2 protege.\n\n---\n\n## Topologia (alvo)\n\n```\nautopilot-run (begin_autopilot_cycle: projected += N_video \u00d7 VIDEO_HYPERFRAMES_RENDER, pr\u00e9-d\u00e9bito at\u00f4mico)\n  \u2502  fan-out sub-runs (Bearer SB_SECRET_KEY + x-autopilot-user-id server-trusted)\n  \u25bc\norchestrate-content \u2192 orchestrate-step  (prepaid=true)\n  \u2502  \u2460 gera texto + imagem product-aware (Fatia 1/1b)\n  \u2502  \u2461 SE video_enabled:\n  \u2502     \u251c\u2500 sanitiza 3 fontes (Cyber-Sentinel fail-closed + escape HTML)   \u25c0\u2500\u2500 FR-VA-023\n  \u2502     \u251c\u2500 monta composi\u00e7\u00e3o HTML 1080\u00d71920 (template + imagem do produto)\n  \u2502     \u2514\u2500 enqueue video_render(engine='hyperframes', prepaid=true,        \u25c0\u2500\u2500 FR-VA-024\n  \u2502           product_id, user_id da linha, content_variant_id)\n  \u2502        (fail-open: erro \u2192 marca 'skipped', segue o ciclo de texto/imagem)\n  \u25bc\n[worker host HyperFrames] \u2500\u2500 claim at\u00f4mico video_renders (engine=hyperframes, state=queued)\n  \u2502  render no container ef\u00eamero (Chrome headless + FFmpeg) \u2192 MP4 1080\u00d71920\n  \u2502  upload bucket privado video-studio-assets \u2192 finalize_video_render(refund=0 no prepaid)\n  \u25bc\nautopilot-video-reconcile (poller service-role, user_id da linha)            \u25c0\u2500\u2500 FR-VA-025\n  \u2502  detecta video_renders.state='done' do ciclo\n  \u2502  content_library(type='video', media_url=storage_key) + creative_metrics + scheduled_posts.content_id\n  \u25bc\nfinalize_autopilot_cycle (refund cr\u00e9dito-positivo idempotente \u2014 inalterado; absorve N_video no actual)\n```\n\n---\n\n## Cost & atomicity contract (resumo execut\u00e1vel)\n\n| Regra | Implementa\u00e7\u00e3o |\n|-------|---------------|\n| Custo de v\u00eddeo no projetado | `projected = N_runs\u00d710 + N_video\u00d7VIDEO_HYPERFRAMES_RENDER(12) + ANALYZE_COST(2)`, `N_video = N_runs` se `video_enabled` sen\u00e3o 0 (FR-VA-007 estendido) |\n| D\u00e9bito \u00fanico | Pr\u00e9-d\u00e9bito do ciclo cobre o v\u00eddeo; o enqueue usa **`prepaid=true`** \u2192 o motor `video-render` **suprime** o `deduct_mco_coins` (espelha `orchestrate-content` FR-VA-016) |\n| Refund | `finalize_autopilot_cycle(cycle_id, actual)` \u2014 `actual` inclui os renders que **de fato** entregaram; o n\u00e3o-usado volta como **cr\u00e9dito positivo idempotente** (NUNCA `deduct` negativo \u2014 `migration 20260603220000:45`) |\n| Cap di\u00e1rio | `N_video\u00d712` entra no `acumulado + projetado` do cap di\u00e1rio (FR-VA-021); o plano (default 200) e o cap di\u00e1rio devem comportar +12/sub-run (OTD-VA-010) |\n| Identidade | service-role + `user_id` server-trusted da linha (`autopilot_cycles`/`autopilot_plans`/`video_renders`), **nunca do body** (OTD-VA-008, herdado de `autopilot-cron-identity`) |\n\n---\n\n## Verification gates\n\n| Gate | Comando/observa\u00e7\u00e3o material | Esperado |\n|------|------------------------------|----------|\n| G1 \u2014 sanitiza\u00e7\u00e3o | Smoke com produto/trend contendo `<script>`, `</template>`, `${...}`, aspas, URL \u2192 inspecionar o HTML gerado | Zero tag/script n\u00e3o-escapado; Cyber-Sentinel 403 em inje\u00e7\u00e3o (espelha sentinel pt-BR/en) |\n| G2 \u2014 prepaid (sem dupla cobran\u00e7a) | Smoke zero-cost: ciclo `video_enabled` em `dry_run`/saldo controlado \u2192 `SELECT` no ledger | **1** d\u00e9bito de v\u00eddeo (no pr\u00e9-d\u00e9bito do ciclo); `video_renders` do sub-run com `charged_mco=0` (prepaid) |\n| G3 \u2014 ratio 9:16 | Render real (1 sub-run) \u2192 `ffprobe` no MP4 do bucket | `width=1080 height=1920` (ratio 9:16); arquivo \u2265 100KB; `Content-Type: video/mp4` |\n| G4 \u2014 determinismo | 2 renders do mesmo input \u2192 `sha256sum` (NFR-VS-016) | Hashes id\u00eanticos |\n| G5 \u2014 fail-open | For\u00e7ar erro de render (template inv\u00e1lido) \u2192 conferir o ciclo | Texto/imagem publicam; `video_render.state='failed'`/`skipped`; ciclo N\u00c3O aborta; saldo de v\u00eddeo refundado |\n| G6 \u2014 reconcilia\u00e7\u00e3o async | Render que termina **depois** do `finalize` \u2192 rodar o poller | `content_library type=video` + `creative_metrics` + `scheduled_posts.content_id` populados; sem asset \u00f3rf\u00e3o |\n| G7 \u2014 sandbox | `/security-review` do worker host + inspe\u00e7\u00e3o do container de render | Sem credencial de tenant no env de render; HTML n\u00e3o alcan\u00e7a rede interna; `/security-review` SAFE |\n| G8 \u2014 tenancy | Smoke: enqueue com `user_id` de outro tenant no body \u2192 conferir | Ignorado; `user_id` resolvido **da linha** (OTD-VA-008); RLS `video_renders` SELECT-own |\n\n---\n\n## Recovery path\n\n| Falha no passo | Rollback/retry exato |\n|----------------|----------------------|\n| Sanitiza\u00e7\u00e3o rejeita (G1) | Sub-run gera texto/imagem normalmente; v\u00eddeo `skipped`; log `infra_health_logs` `service='autopilot-video' event='sanitize_blocked'`. Sem deduct extra. |\n| Enqueue falha (motor 503/erro) | **fail-open**: `skipped`; o pr\u00e9-d\u00e9bito de v\u00eddeo daquele sub-run vira refund no `finalize` (`actual` n\u00e3o conta o v\u00eddeo n\u00e3o-entregue). Nunca derruba o ciclo. |\n| Render trava (worker morto) | O poller `autopilot-video-reconcile` reaproveita o padr\u00e3o `rescue-video`: re-claim de `video_renders` em `running` h\u00e1 > timeout \u2192 `failed` + refund; ou re-render manual via `video-render-poll`. |\n| Asset chega ap\u00f3s `finalize` | \u00c9 o caso **normal** \u2014 o poller anexa por `content_variant_id` depois do `done`. Idempotente (n\u00e3o re-anexa se `content_library` j\u00e1 tem a linha do `content_variant_id`). |\n| Dupla cobran\u00e7a detectada | Bug de contrato: o enqueue n\u00e3o passou `prepaid=true`. Halt, corrigir o flag, refund manual via `finalize_autopilot_cycle` reconciliando `actual`. |\n\n---\n\n## Success signal\n\nMaterialmente observ\u00e1vel que o flow 9:16 est\u00e1 completo e seguro:\n\n1. **`ffprobe`** de um asset real do ciclo \u2192 `1080\u00d71920` (9:16), \u2265 100KB, `video/mp4` no bucket privado `video-studio-assets`.\n2. **Ledger:** saldo do tenant caiu exatamente `N_runs\u00d710 + N_video\u00d712 + 2` (\u2212 refund do n\u00e3o-entregue); **nenhum** `video_renders.charged_mco > 0` no caminho prepaid.\n3. **`content_library`** tem a linha `type='video'` + **`creative_metrics`** tem a linha do `content_variant_id` + **`scheduled_posts.content_id`** aponta para o criativo.\n4. **Smoke G5 (fail-open):** um ciclo com render for\u00e7ado a falhar publica texto/imagem e fecha sem abortar, com refund do v\u00eddeo.\n5. **`/security-review` SAFE** do worker de render + da migration de schema.\n\n---\n\n## Anti-patterns proibidos\n\n- \u274c Enqueue do render **sem** `prepaid=true` \u2192 dupla cobran\u00e7a (motor self-bill + pr\u00e9-d\u00e9bito do ciclo).\n- \u274c `user_id` do v\u00eddeo vindo do **body/header** do request em vez da linha confi\u00e1vel \u2192 inje\u00e7\u00e3o cross-tenant (viola OTD-VA-008).\n- \u274c Falha de render **derrubando** o ciclo de texto/imagem (deve ser fail-open `skipped`).\n- \u274c Interpolar nome de produto / texto de trend / `optimization_policy` **direto** no HTML sem escape + Cyber-Sentinel \u2192 XSS/escape de sandbox no Chrome headless.\n- \u274c Render **multi-tenant** antes do hardening do sandbox selado (`/security-review` + container ef\u00eamero egress-only) \u2014 Usu\u00e1rio Zero single-tenant \u00e9 o limite desta fase (OTD-VA-011).\n- \u274c Fechar o ciclo (`finalize`) **sem** reconciliar o asset ass\u00edncrono \u2192 custo pago, asset \u00f3rf\u00e3o.\n- \u274c Refund de v\u00eddeo como `deduct` negativo \u2192 viola o guard anti-mint `p_amount<=0` (`migration 20260603220000:45`).\n\n---\n\n## Sibling reference\n\nEsta SOP \u00e9 a **camada de v\u00eddeo** sobre a base financeira de `autopilot-cron-identity.md` (que j\u00e1 cobre identidade do cron + pr\u00e9-d\u00e9bito/refund + cap di\u00e1rio). Reusa o motor de `video-studio` (FR-VS-024/025) e o padr\u00e3o de render async + reconcilia\u00e7\u00e3o de `canvas-video-async-execution.md`. O worker host segue o molde de `scripts/design-bridge.ts` (claim at\u00f4mico + execu\u00e7\u00e3o em container) descrito na reconcilia\u00e7\u00e3o de drift do `video-studio` SDD \u00a72.3.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/autopilot-video-9x16.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:13:45)*


## 🤖 Claude *(03:13:46)*

BoK amendment authored. Let me verify the FRD numbering is clean and locate the CLAUDE.md Key Files spot to register the new SOP:

## 🤖 Claude *(03:13:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== FR-VA-022..026 present in FRD? ===\"\ngrep -oE \"FR-VA-02[2-6]\" docs/bok/viral-autopilot/04-frd.md | sort | uniq -c\necho \"=== OTD-VA-009..012 present in SDD? ===\"\ngrep -oE \"OTD-VA-0(09|1[012])\" docs/bok/viral-autopilot/05-sdd.md | sort | uniq -c\necho \"=== CLAUDE.md: autopilot SOP key-files line ===\"\ngrep -nE \"autopilot-cron-identity|Viral Autopilot cron-identity\" CLAUDE.md",
  "description": "Verify amendment numbering + find CLAUDE.md insert point"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === FR-VA-022..026 present in FRD? ===
>       5 FR-VA-022
>       2 FR-VA-023
>       2 FR-VA-024
>       2 FR-VA-025
>       3 FR-VA-026
> === OTD-VA-009..012 present in SDD? ===
>       2 OTD-VA-009
>       1 OTD-VA-010
>       2 OTD-VA-011
>       1 OTD-VA-012
> === CLAUDE.md: autopilot SOP key-files line ===
> 425:| **Viral Autopilot cron-identity SOP (Lei 2)** | `docs/processes/autopilot-cron-identity.md` (OTD-VA-008 gate — cron prova `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da linha [nunca body]; pré-débito/refund atômico FR-VA-007/021; 10 gates) |
> ```

## 🤖 Claude *(03:13:52)*


## 🤖 Claude *(03:13:53)*

All FRs/OTDs present. Registering the new SOP in CLAUDE.md Key Files Reference (process mandate), right after the cron-identity entry:

## 🤖 Claude *(03:14:00)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "old_string": "| **Viral Autopilot cron-identity SOP (Lei 2)** | `docs/processes/autopilot-cron-identity.md` (OTD-VA-008 gate \u2014 cron prova `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da linha [nunca body]; pr\u00e9-d\u00e9bito/refund at\u00f4mico FR-VA-007/021; 10 gates) |",
  "new_string": "| **Viral Autopilot cron-identity SOP (Lei 2)** | `docs/processes/autopilot-cron-identity.md` (OTD-VA-008 gate \u2014 cron prova `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da linha [nunca body]; pr\u00e9-d\u00e9bito/refund at\u00f4mico FR-VA-007/021; 10 gates) |\n| **Viral Autopilot v\u00eddeo 9:16 SOP (Lei 2 \u00b7 Amendment v0.2)** | `docs/processes/autopilot-video-9x16.md` (OTD-VA-009 gate \u2014 v\u00eddeo vertical 9:16 product-aware via motor HyperFrames determin\u00edstico [`video-studio` FR-VS-024/025], **n\u00e3o** IA-DoP; cobran\u00e7a \u00daNICA no pr\u00e9-d\u00e9bito do ciclo [`prepaid=true` suprime self-bill do motor \u2014 OTD-VA-010]; single-tenant Usu\u00e1rio Zero [hardening multi-tenant diferido \u2014 OTD-VA-011]; render async + reconcilia\u00e7\u00e3o fail-open; 8 gates G1-G8; FRD Amendment v0.2 = FR-VA-022..026) |"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(03:14:04)*


## 🤖 Claude *(03:14:04)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "offset": 424,
  "limit": 3
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 424	| **mcoCoins cost calibration SOP** | `docs/processes/mcoin-cost-calibration.md` (4×-floor model `mco=ceil(usd/$0.018×4)`; OTD-MCOIN-CALIBRATION closed) |
> 425	| **Viral Autopilot cron-identity SOP (Lei 2)** | `docs/processes/autopilot-cron-identity.md` (OTD-VA-008 gate — cron prova `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da linha [nunca body]; pré-débito/refund atômico FR-VA-007/021; 10 gates) |
> 426	| **Viral Autopilot cadence schema + money RPCs (Fatia 2)** | `supabase/migrations/20260620120000_viral_autopilot_plans.sql` · `…120100_viral_autopilot_cycles.sql` (FK composta tenant-escopada + RESTRICTIVE no-delete + fecha FK composta de `creative_metrics`) · `…120200_begin_autopilot_cycle.sql` (cap+pré-débito atômico advisory-lock, service-role-only) · `…120300_finalize_autopilot_cycle.sql` (refund crédito-positivo idempotente, espelha `finalize_vision_job`) |
> ```

## 🤖 Claude *(03:14:14)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "old_string": "| **Viral Autopilot cron-identity SOP (Lei 2)** | `docs/processes/autopilot-cron-identity.md` (OTD-VA-008 gate \u2014 cron prova `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da linha [nunca body]; pr\u00e9-d\u00e9bito/refund at\u00f4mico FR-VA-007/021; 10 gates) |\n| **Viral Autopilot cadence schema + money RPCs (Fatia 2)** |",
  "new_string": "| **Viral Autopilot cron-identity SOP (Lei 2)** | `docs/processes/autopilot-cron-identity.md` (OTD-VA-008 gate \u2014 cron prova `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da linha [nunca body]; pr\u00e9-d\u00e9bito/refund at\u00f4mico FR-VA-007/021; 10 gates) |\n| **Viral Autopilot v\u00eddeo 9:16 SOP (Lei 2 \u00b7 Amendment v0.2)** | `docs/processes/autopilot-video-9x16.md` (OTD-VA-009 gate \u2014 v\u00eddeo vertical 9:16 product-aware via motor HyperFrames determin\u00edstico [`video-studio` FR-VS-024/025], **n\u00e3o** IA-DoP; cobran\u00e7a \u00daNICA no pr\u00e9-d\u00e9bito do ciclo [`prepaid=true` suprime self-bill do motor \u2014 OTD-VA-010]; single-tenant Usu\u00e1rio Zero [hardening multi-tenant diferido \u2014 OTD-VA-011]; render async + reconcilia\u00e7\u00e3o fail-open; 8 gates G1-G8; FRD Amendment v0.2 = FR-VA-022..026) |\n| **Viral Autopilot cadence schema + money RPCs (Fatia 2)** |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:14:50)*


## 🤖 Claude *(03:14:52)*

**Fatia VA-V0 (BoK gate) — COMPLETO.** A Lei 2 está satisfeita: PR-VA-020 decomposto (FR-VA-022..026), OTD-VA-009..012 selados, SOP `autopilot-video-9x16.md` escrito, drift do video-studio reconciliado, CLAUDE.md registrado. O gate Closed-Loop está **aberto** para código de vídeo.

## 🤖 Claude *(03:14:53)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #1 status
> ```

## 🤖 Claude *(03:14:53)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "2",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #2 status
> ```

## 🤖 Claude *(03:14:56)*

Now the motor (Fatia VS-2). Before building, I need the exact shipped Fatia 1 contract (Law 1 grounding) + the real render-infra reality. Probing both:

## 🤖 Claude *(03:14:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== video-render edge fn: gate + contract (full, it's small) ===\"\nwc -l supabase/functions/video-render/index.ts\necho \"--- the 503 gate + insert + cost ---\"\nsed -n '1,140p' supabase/functions/video-render/index.ts",
  "description": "Read shipped video-render edge fn contract"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === video-render edge fn: gate + contract (full, it's small) ===
> 136 supabase/functions/video-render/index.ts
> --- the 503 gate + insert + cost ---
> // video-render — video-studio render submit (FR-VS-001/005/009/014/032). verify_jwt=false (auth in-code).
> // BoK SSOT: docs/bok/video-studio/05-sdd.md §3.1 (UI→Hook→Edge contract) + 04-frd.md (FR-VS-009 charge-at-entry,
> //           FR-VS-011 refund, FR-VS-032 voice consent). SOP: 07-process-flow.md PROC-VS-001/004.
> //
> // CONTRACT (charge-at-entry + refund-on-failure): JWT verify → engine validate → voice-consent gate →
> //   BYOK resolve fail-closed → [dry_run short-circuit] → worker-availability gate → deduct_mco_coins →
> //   INSERT video_renders(queued) via service key → trigger worker → 202 {render_id}. 401/409/402/503 NEVER
> //   charge. A trigger failure AFTER deduct refunds idempotently via finalize_video_render.
> //
> // SLICE 1 (this): the render worker is NOT wired yet (faceless = n8n bridge OTD-VS-001 / hyperframes = sandbox
> //   OTD-VS-006), so the engine-availability gate returns 503 BEFORE any deduct — nobody pays for a render that
> //   cannot run. Everything up to that gate is provable zero-cost (401/422/409/402/dry_run). SLICE 2 sets the
> //   worker webhook env → the prepaid path below activates unchanged.
> import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 
> const corsHeaders = {
>   "Access-Control-Allow-Origin": "*",
>   "Access-Control-Allow-Methods": "POST, OPTIONS",
>   "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> };
> 
> // Mirror of src/lib/billing.ts COIN_COSTS (Deno can't import src/lib — keep in sync; OTD-VS-007 provisional).
> const COST = { faceless: 125, hyperframes: 12 } as const;
> type Engine = keyof typeof COST;
> 
> Deno.serve(async (req) => {
>   if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
>   const json = (b: unknown, s = 200) =>
>     new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 
>   const url = Deno.env.get("SUPABASE_URL")!;
>   const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
>   const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
>   const admin = createClient(url, serviceKey);
>   const logHealth = (status: string, event?: string) =>
>     admin.from("infra_health_logs").insert({ service: "video-render", status, event }).then(() => {}, () => {});
> 
>   try {
>     const authHeader = req.headers.get("Authorization");
>     if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 
>     // Identity: user JWT (this is a user-initiated submit). getUser rejects an invalid/forged token.
>     const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
>     const { data: { user }, error: authErr } = await userClient.auth.getUser();
>     if (authErr || !user) return json({ error: "Unauthorized" }, 401);
>     const userId = user.id;
> 
>     const body = await req.json().catch(() => ({}));
>     const engine = body?.engine as Engine | undefined;
>     if (engine !== "faceless" && engine !== "hyperframes") {
>       return json({ error: "engine_invalid", detail: "engine deve ser 'faceless' ou 'hyperframes'" }, 422);
>     }
>     const dryRun = body?.dry_run === true;
>     const voiceConsent = body?.voice_consent === true;
>     const topic = typeof body?.topic === "string" ? body.topic.slice(0, 500) : null;
>     const productId = typeof body?.product_id === "string" ? body.product_id : null;
> 
>     // Voice-consent gate (FR-VS-032): faceless clones a voice (VoxCPM) → identifiable biometric (LGPD Art. 11).
>     if (engine === "faceless" && !voiceConsent) {
>       return json({ error: "voice_consent_required", action: "Confirme o consentimento de uso de voz para gerar o vídeo faceless." }, 409);
>     }
> 
>     // BYOK fail-closed (FR-VS-005/006): faceless needs the tenant's Gemini/Google key (director + vision QA). Per-user
>     // first; NO silent global fallback in a user-facing path (API Tenancy Model). hyperframes is deterministic (no AI leg).
>     // The canonical Vault column is `google_api_key` (NOT `gemini_api_key` — the BoK 06 §2.5 / CLAUDE.md naming is
>     // stale; canvas-execute + the live decrypted view use google_api_key, verified 2026-06-22 via 42703 on gemini_api_key).
>     if (engine === "faceless") {
>       const { data: keys } = await admin
>         .from("decrypted_user_api_keys").select("google_api_key").eq("user_id", userId).maybeSingle();
>       if (!keys?.google_api_key) {
>         return json({ error: "gemini_not_configured", action: "Configure sua chave Gemini/Google em /dashboard/settings para gerar vídeo." }, 402);
>       }
>     }
> 
>     const cost = COST[engine];
> 
>     // dry_run: cost projection WITHOUT deduct or row (zero-cost proof path; mirrors autopilot-run).
>     if (dryRun) return json({ ok: true, dry_run: true, engine, cost_mco: cost });
> 
>     // Engine-availability gate (SLICE 1): the worker webhook is unset until slice 2 wires the render engine.
>     // Returning 503 HERE — before any deduct — guarantees no tenant is charged for a render that cannot complete.
>     const workerWebhook = engine === "faceless"
>       ? Deno.env.get("VIDEO_FACELESS_WEBHOOK")
>       : Deno.env.get("VIDEO_HYPERFRAMES_WEBHOOK");
>     if (!workerWebhook) {
>       return json({
>         error: "render_engine_unavailable",
>         detail: `O motor de render '${engine}' entra na Fatia 2 (faceless: ponte de rede + n8n; hyperframes: sandbox). Nenhum mcoCoin foi debitado.`,
>       }, 503);
>     }
> 
>     // ── SLICE 2 prepaid path (activates once the worker webhook env is set) ──────────────────────────────────────
>     // Charge-at-entry (FR-VS-009): atomic deduct BEFORE any leg. 402 if balance < cost (zero rows created).
>     const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: cost });
>     if (deductErr) {
>       logHealth("degraded", "insufficient_balance");
>       return json({ error: "insufficient_balance", detail: `Saldo insuficiente: render '${engine}' custa ${cost} mcoCoins.`, cost_mco: cost }, 402);
>     }
> 
>     // INSERT the queued render (service key — RLS denies tenant writes; this is the only writer). org_id/client_id
>     // NULL = solo creator (§AG agency scoping wires in a later slice).
>     const { data: render, error: insErr } = await admin
>       .from("video_renders")
>       .insert({ user_id: userId, engine, topic, product_id: productId, voice_consent: voiceConsent, charged_mco: cost, state: "queued" })
>       .select("id").single();
>     if (insErr || !render) {
>       // Could not even create the ledger row → refund the just-charged cost (no render_id yet → direct credit).
>       await admin.rpc("add_mco_coins", { p_user_id: userId, p_amount: cost }).then(() => {}, () => {});
>       logHealth("error", "insert_failed");
>       return json({ error: "render_create_failed", detail: insErr?.message }, 500);
>     }
>     const renderId = render.id as string;
> 
>     // Trigger the worker. On failure AFTER the charge, refund idempotently via the terminal authority.
>     try {
>       const r = await fetch(workerWebhook, {
>         method: "POST",
>         headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
>         body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),
>       });
>       if (!r.ok) throw new Error(`worker HTTP ${r.status}`);
>     } catch (e) {
>       await admin.rpc("finalize_video_render", {
>         p_render_id: renderId, p_state: "failed", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,
>       }).then(() => {}, () => {});
>       logHealth("error", "worker_trigger_failed");
>       return json({ error: "worker_unavailable", detail: e instanceof Error ? e.message : "trigger failed", render_id: renderId }, 502);
>     }
> 
>     logHealth("healthy", "render_submitted");
>     return json({ ok: true, render_id: renderId, engine, charged_mco: cost, state: "queued" }, 202);
>   } catch (e) {
>     logHealth("error", "exception");
>     return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
>   }
> });
> ```

## 🤖 Claude *(03:15:44)*


## 🤖 Claude *(03:15:46)*

Now I have the full shipped contract: `video-render` gates on `VIDEO_HYPERFRAMES_WEBHOOK`, then prepaid deduct → INSERT `video_renders(queued)` → POSTs to the webhook → 202. But the synthesis established that **the edge runtime can't reach a host worker** — design-bridge *polls* instead. So the motor must reconcile these. Before designing, I'll probe the real infra (schema, RPC, design-bridge claim pattern, and whether render tooling even exists on this host).

## 🤖 Claude *(03:15:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== video_renders schema (migration) ===\"\nls supabase/migrations/ | grep -iE \"video_render|video_studio|video_asset\" \necho \"--- columns ---\"\ngrep -nE \"create table|CREATE TABLE|^\\s+[a-z_]+ +(uuid|text|integer|boolean|jsonb|timestamptz|numeric)|composition|template|storage_key|engine|state\" supabase/migrations/*video_render* 2>/dev/null | head -50",
  "description": "video_renders table schema"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === video_renders schema (migration) ===
> 20260622030000_video_studio_org_tenancy.sql
> 20260622030100_video_studio_org_grant_hardening.sql
> 20260622040000_video_studio_renders_and_assets.sql
> --- columns ---
> ```

## 🤖 Claude *(03:15:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== render tooling on host ===\"\nwhich ffmpeg && ffmpeg -version 2>/dev/null | head -1 || echo \"NO ffmpeg\"\necho \"---\"\nls node_modules/.bin/ 2>/dev/null | grep -iE \"playwright|puppeteer\" || echo \"NO playwright/puppeteer in node_modules/.bin\"\necho \"--- playwright/puppeteer in package.json ---\"\ngrep -iE \"playwright|puppeteer|remotion\" package.json || echo \"(none in package.json)\"\necho \"=== design-bridge claim + enqueue pattern ===\"\ngrep -nE \"\\.update|\\.eq\\(|status|claim|design_jobs|poll|setInterval|while\" scripts/design-bridge.ts | head -25",
  "description": "Render tooling + design-bridge poll/claim pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === render tooling on host ===
> /usr/bin/ffmpeg
> ffmpeg version 6.1.1-3ubuntu5 Copyright (c) 2000-2023 the FFmpeg developers
> ---
> playwright
> playwright-core
> --- playwright/puppeteer in package.json ---
>     "@playwright/test": "^1.57.0",
> === design-bridge claim + enqueue pattern ===
> 5: * Bridge worker running on the host that polls `design_jobs` and executes
> 38:// Create Supabase client using Service Role to bypass RLS for status updates
> 79: * Main polling cycle.
> 81:async function pollJobs() {
> 82:  console.log(`🤖 design-bridge is running and polling design_jobs...`);
> 84:  while (true) {
> 87:        .from('design_jobs')
> 89:        .eq('status', 'queued')
> 107:        // Atomic claim check
> 108:        const { data: claimed, error: claimError } = await supabase
> 109:          .from('design_jobs')
> 110:          .update({ status: 'running', updated_at: new Date().toISOString() })
> 111:          .eq('id', job.id)
> 112:          .eq('status', 'queued')
> 115:        if (claimError || !claimed || claimed.length === 0) {
> 116:          console.log(`⚠️ Job ${job.id} already claimed by another worker. Skipping.`);
> 137:            // Update DB status
> 139:              .from('design_jobs')
> 140:              .update({
> 141:                status: 'complete',
> 145:              .eq('id', job.id);
> 256:                .update({ mesh_node_id: node.id })
> 257:                .eq('id', ref.id);
> 260:            // Update job status to complete
> 262:              .from('design_jobs')
> ```

## 🤖 Claude *(03:16:03)*


## 🤖 Claude *(03:16:05)*

Infra is **green**: FFmpeg 6.1.1 + Playwright both present on the host → HTML→MP4 1080×1920 is fully buildable, no infra blocker. The design-bridge poll/claim pattern is confirmed (`while(true)` → SELECT queued → atomic `.update(running).eq(status,queued)`). Now the exact `video_renders` schema + `finalize_video_render`:

## 🤖 Claude *(03:16:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260622040000_video_studio_renders_and_assets.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: video-studio Fatia 1 — domain foundation (video_renders + video_assets + finalize/refund RPC).
> 2	-- BoK SSOT: docs/bok/video-studio/06-data-model.md (§2.1 video_renders, §2.4 video_assets, §3 RLS/index plan)
> 3	--           + 04-frd.md (FR-VS-009/010/011/014/024/026/030) + 05-sdd.md (§2.6 New DB Objects).
> 4	-- Anticipated process (Lei 2): docs/bok/video-studio/07-process-flow.md PROC-VS-001/004 (charge-at-entry + refund).
> 5	--
> 6	-- SCOPE (slice 1 — foundation + edge contract; render engine deferred to slice 2):
> 7	--   • video_renders — render state machine + atomic charged/refunded ledger, poll-able, tenancy-aware from birth
> 8	--     (org_id/client_id NULLABLE: NULL = solo creator v0.1, byte-identical backward-compat; set = agency §AG).
> 9	--   • video_assets — material artifact manifest (Storage object + node_id) = the erasure unit (FR-VS-030).
> 10	--   • finalize_video_render — the ONLY terminal+refund authority (service-role), mirrors finalize_vision_job
> 11	--     (20260615160000): atomic guard `state IN (queued,running,qa_gate)` ⇒ first finalizer wins, idempotent,
> 12	--     never money-without-guard nor double-refund.
> 13	--
> 14	-- TENANCY MODEL (FMEA-VS-020 — cross-tenant isolation is the v1.1 top RPN; /security-review gated):
> 15	--   SELECT = own row OR (agency) a row of an org the caller is an active member of (public.is_org_member, the
> 16	--   anti-recursion SECURITY DEFINER helper from 20260622030000). NO INSERT/UPDATE policy for authenticated ⇒
> 17	--   default-deny writes: the edge fn (video-render) is the ONLY writer, via the service key, AFTER deduct_mco_coins.
> 18	--   A tenant therefore can NEVER forge a render row (bypassing the charge) nor mutate one (zeroing its charge /
> 19	--   faking 'done' to read another tenant's asset). Mirrors vision_jobs (20260615160000) + lead_core tenancy.
> 20	--   video_renders carries a RESTRICTIVE no-delete (financial ledger family: creative_metrics / autopilot_cycles).
> 21	--
> 22	-- project_id is uuid WITHOUT FK (there is no `projects` table — project_id is text/uuid tenant tag elsewhere;
> 23	-- mirrors vision_jobs:19). The (org_id, client_id) composite FK → clients(org_id, id) is NOT VALID (no backfill
> 24	-- scan; existing/solo rows have NULLs ⇒ MATCH SIMPLE skips the FK) and proves a render's client truly belongs to
> 25	-- the stated org. CHECK keeps client_id from being set without an org.
> 26	
> 27	-- ─────────────────────────────────────────────────────────────────────────────
> 28	-- 1. video_renders — render state machine + atomic ledger (FR-VS-009/010/011/014/024/026)
> 29	-- ─────────────────────────────────────────────────────────────────────────────
> 30	CREATE TABLE IF NOT EXISTS public.video_renders (
> 31	  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),    -- = render_id (returned in 202; poll-able)
> 32	  user_id       uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 33	  org_id        uuid        REFERENCES public.organizations(id) ON DELETE CASCADE,  -- NULL = solo creator (§AG opt-in)
> 34	  client_id     uuid,                                                 -- agency cost-center; FK is composite (below)
> 35	  project_id    uuid,                                                 -- optional tenant project tag (no projects table)
> 36	  engine        text        NOT NULL CHECK (engine IN ('faceless','hyperframes')),
> 37	  state         text        NOT NULL DEFAULT 'queued'
> 38	                  CHECK (state IN ('queued','running','qa_gate','done','qa_failed','failed')),
> 39	  product_id    uuid,                                                 -- product-aware (FR-VS-017); logical, no FK (prunable)
> 40	  topic         text,                                                 -- free topic when no product
> 41	  template_id   uuid,                                                 -- HyperFrames reuse (FR-VS-024); logical until templates land
> 42	  legs          jsonb       NOT NULL DEFAULT '[]'::jsonb,             -- per-leg status (script/image/voice/motion/overlay/composite/qa)
> 43	  qa            jsonb,                                                -- { consistent, confidence } from the VLM gate (FR-VS-019/020)
> 44	  charged_mco   int         NOT NULL DEFAULT 0 CHECK (charged_mco >= 0),
> 45	  refunded_mco  int         NOT NULL DEFAULT 0 CHECK (refunded_mco >= 0 AND refunded_mco <= charged_mco),
> 46	  refunded_at   timestamptz,                                          -- idempotency guard (refund 1×/render — PROC-VS-004)
> 47	  storage_key   text,                                                 -- set at `done`; object ≥100KB (Lei 1 proof)
> 48	  voice_consent boolean     NOT NULL DEFAULT false,                   -- required for identifiable voice cloning (FR-VS-032)
> 49	  node_id       uuid,                                                 -- mesh observation (FR-VS-026); logical → mcorch_nodes.id
> 50	  expires_at    timestamptz NOT NULL DEFAULT (now() + interval '24 hours'),  -- poll retention ≥24h
> 51	  created_at    timestamptz NOT NULL DEFAULT now(),
> 52	  updated_at    timestamptz NOT NULL DEFAULT now(),
> 53	  CONSTRAINT video_renders_client_needs_org CHECK (client_id IS NULL OR org_id IS NOT NULL),
> 54	  CONSTRAINT video_renders_client_fk FOREIGN KEY (org_id, client_id)
> 55	    REFERENCES public.clients(org_id, id) ON DELETE SET NULL NOT VALID
> 56	);
> 57	
> 58	ALTER TABLE public.video_renders ENABLE ROW LEVEL SECURITY;
> 59	
> 60	-- SELECT: own row, OR an agency row whose org the caller actively belongs to (anti-recursion helper).
> 61	CREATE POLICY "video_renders_select_own_or_org" ON public.video_renders
> 62	  FOR SELECT USING (
> 63	    auth.uid() = user_id
> 64	    OR (org_id IS NOT NULL AND public.is_org_member(org_id))
> 65	  );
> 66	
> 67	-- No INSERT/UPDATE policy for authenticated ⇒ default-deny: the edge fn writes via the service key AFTER the
> 68	-- atomic deduct. RESTRICTIVE no-delete: the financial ledger is never client-deletable (service-role erasure only).
> 69	CREATE POLICY "video_renders_no_client_delete" ON public.video_renders
> 70	  AS RESTRICTIVE FOR DELETE USING (false);
> 71	
> 72	CREATE INDEX IF NOT EXISTS video_renders_user_state_idx   ON public.video_renders (user_id, state);
> 73	CREATE INDEX IF NOT EXISTS video_renders_user_created_idx ON public.video_renders (user_id, created_at DESC);
> 74	CREATE INDEX IF NOT EXISTS video_renders_org_idx          ON public.video_renders (org_id) WHERE org_id IS NOT NULL;
> 75	CREATE INDEX IF NOT EXISTS video_renders_expires_idx      ON public.video_renders (expires_at);
> 76	
> 77	CREATE TRIGGER tr_update_video_renders_updated_at
> 78	  BEFORE UPDATE ON public.video_renders
> 79	  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 80	
> 81	COMMENT ON TABLE public.video_renders IS
> 82	  'video-studio render state machine (FR-VS-009/014/024). queued→running→qa_gate→done|qa_failed|failed; atomic '
> 83	  'charged/refunded ledger (refunded_mco<=charged_mco, refunded_at idempotency). SELECT own-or-org-member RLS; '
> 84	  'edge fn writes via service key after deduct; RESTRICTIVE no client delete. org_id/client_id NULL = solo (§AG opt-in).';
> 85	
> 86	-- ─────────────────────────────────────────────────────────────────────────────
> 87	-- 2. video_assets — material artifact manifest = the erasure unit (FR-VS-030/031)
> 88	-- ─────────────────────────────────────────────────────────────────────────────
> 89	CREATE TABLE IF NOT EXISTS public.video_assets (
> 90	  id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
> 91	  user_id         uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 92	  render_id       uuid        NOT NULL REFERENCES public.video_renders(id) ON DELETE CASCADE,
> 93	  kind            text        NOT NULL CHECK (kind IN ('video','image','audio')),
> 94	  storage_key     text        NOT NULL,                              -- object in private bucket video-studio-assets
> 95	  node_id         uuid,                                              -- derived mesh node (FR-VS-026); logical
> 96	  bytes           bigint      CHECK (bytes IS NULL OR bytes >= 0),   -- material size (video ≥100KB) — Lei 1
> 97	  retention_until timestamptz,                                       -- LGPD retention clock (Art. 16)
> 98	  created_at      timestamptz NOT NULL DEFAULT now()
> 99	);
> 100	
> 101	ALTER TABLE public.video_assets ENABLE ROW LEVEL SECURITY;
> 102	
> 103	-- SELECT own only (the asset row is tenant-bound via user_id; org members read assets through the render join in
> 104	-- the app layer when agency surfaces land). No write policy ⇒ service-role writes only (same billing-integrity rule).
> 105	CREATE POLICY "video_assets_select_own" ON public.video_assets
> 106	  FOR SELECT USING (auth.uid() = user_id);
> 107	
> 108	CREATE INDEX IF NOT EXISTS video_assets_render_idx    ON public.video_assets (render_id);
> 109	CREATE INDEX IF NOT EXISTS video_assets_user_idx      ON public.video_assets (user_id);
> 110	CREATE INDEX IF NOT EXISTS video_assets_retention_idx ON public.video_assets (retention_until);
> 111	
> 112	COMMENT ON TABLE public.video_assets IS
> 113	  'video-studio material artifact manifest (FR-VS-030). Storage object + node_id = atomic erasure unit. '
> 114	  'SELECT-own RLS; service-role writes. bytes>=100KB enforced app-side before render reaches done (Lei 1).';
> 115	
> 116	-- ─────────────────────────────────────────────────────────────────────────────
> 117	-- 3. finalize_video_render — atomic terminal + refund authority (FR-VS-011 · mirrors finalize_vision_job)
> 118	--    Closes the /security-review HIGH class (charge-without-value + refund/guard atomicity). The ONLY way a
> 119	--    render goes terminal. Guard `state IN (queued,running,qa_gate)` ⇒ the FIRST finalizer wins (worker OR a
> 120	--    future poll lazy-reconcile OR a sweep); a second call on an already-terminal render is a no-op (no double
> 121	--    refund). The video_renders guard write AND the balance credit (add_mco_coins) commit in ONE transaction.
> 122	--    service_role-only (the worker/edge calls it via SB_SECRET_KEY; tenants never reach it). FMEA-011 reviewed.
> 123	-- ─────────────────────────────────────────────────────────────────────────────
> 124	CREATE OR REPLACE FUNCTION public.finalize_video_render(
> 125	  p_render_id   uuid,
> 126	  p_state       text,
> 127	  p_storage_key text,    -- NULL keeps existing (set on success)
> 128	  p_qa          jsonb,   -- NULL keeps existing (VLM verdict)
> 129	  p_node_id     uuid,    -- NULL keeps existing (mesh observation)
> 130	  p_refund      int      -- refund to credit (0 = none, e.g. 'done'); must be <= charged_mco
> 131	)
> 132	RETURNS jsonb
> 133	LANGUAGE plpgsql
> 134	SECURITY DEFINER
> 135	SET search_path = ''
> 136	AS $$
> 137	DECLARE
> 138	  v_uid uuid;
> 139	BEGIN
> 140	  IF p_state NOT IN ('done','qa_failed','failed') THEN
> 141	    RAISE EXCEPTION 'finalize_video_render: terminal state required, got %', p_state USING errcode = '22023';
> 142	  END IF;
> 143	
> 144	  -- Claim + finalize a NON-TERMINAL render exactly once.
> 145	  UPDATE public.video_renders
> 146	     SET state        = p_state,
> 147	         storage_key  = COALESCE(p_storage_key, storage_key),
> 148	         qa           = COALESCE(p_qa, qa),
> 149	         node_id      = COALESCE(p_node_id, node_id),
> 150	         refunded_mco = CASE WHEN p_refund > 0 THEN p_refund ELSE refunded_mco END,
> 151	         refunded_at  = CASE WHEN p_refund > 0 THEN now()    ELSE refunded_at END
> 152	   WHERE id = p_render_id
> 153	     AND state IN ('queued','running','qa_gate')
> 154	   RETURNING user_id INTO v_uid;
> 155	
> 156	  IF v_uid IS NULL THEN
> 157	    RETURN jsonb_build_object('finalized', false);   -- already terminal → no-op (no double refund)
> 158	  END IF;
> 159	
> 160	  IF p_refund > 0 THEN
> 161	    PERFORM public.add_mco_coins(v_uid, p_refund);
> 162	    RETURN jsonb_build_object('finalized', true, 'refunded', p_refund);
> 163	  END IF;
> 164	
> 165	  RETURN jsonb_build_object('finalized', true, 'refunded', 0);
> 166	END;
> 167	$$;
> 168	
> 169	REVOKE ALL ON FUNCTION public.finalize_video_render(uuid, text, text, jsonb, uuid, int) FROM PUBLIC, anon, authenticated;
> 170	GRANT EXECUTE ON FUNCTION public.finalize_video_render(uuid, text, text, jsonb, uuid, int) TO service_role;
> 171	
> ```

## 🤖 Claude *(03:17:10)*


## 🤖 Claude *(03:17:14)*

Complete schema + RPC obtained. Critical facts for the motor:
- `video_renders` has `legs jsonb`, `template_id`, `topic`, `product_id` but **no composition/HTML column** — I'll add one. `finalize_video_render(p_render_id, p_state, p_storage_key, p_qa, p_node_id, p_refund)` is the atomic terminal authority (service-role).
- Infra is green (FFmpeg + Playwright on host).

The riskiest/most novel piece is the **render core** (HTML→1080×1920 MP4, deterministic). Per Law 1, I'll build and *materially prove* that first — a real MP4 with `ffprobe` showing 1080×1920 — before wiring queue/edge/migration around it. Let me confirm the Playwright browser is installed and check the bucket:

## 🤖 Claude *(03:17:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== playwright chromium installed? ===\"\nls ~/.cache/ms-playwright/ 2>/dev/null | grep -i chrom || echo \"NO chromium cache \u2014 needs: npx playwright install chromium\"\necho \"=== bucket video-studio-assets exists? ===\"\nsource .env 2>/dev/null\ncurl -s \"${SUPABASE_URL}/storage/v1/bucket\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" 2>/dev/null | python3 -c \"import json,sys; d=json.load(sys.stdin); print([b['id'] for b in d] if isinstance(d,list) else d)\" 2>/dev/null || echo \"(bucket list query failed \u2014 check later)\"\necho \"=== design-bridge.service systemd unit (template) ===\"\nls -la ~/.config/systemd/user/design-bridge.service 2>/dev/null && cat ~/.config/systemd/user/design-bridge.service 2>/dev/null || (systemctl --user cat design-bridge.service 2>/dev/null || echo \"(design-bridge.service not found at user scope)\")",
  "description": "Check playwright browser, bucket, systemd template"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === playwright chromium installed? ===
> chromium-1217
> chromium-1226
> chromium_headless_shell-1217
> chromium_headless_shell-1226
> mcp-chrome-6d4d142
> mcp-chrome-8a5edab
> mcp-chrome-dc082d7
> mcp-chrome-for-testing-8a5edab
> === bucket video-studio-assets exists? ===
> ['generated-images', 'generated-videos', 'canvas-assets', 'vision-artifacts']
> === design-bridge.service systemd unit (template) ===
> -rw-rw-r-- 1 ubuntu ubuntu 773 Jun 21 20:33 /home/ubuntu/.config/systemd/user/design-bridge.service
> [Unit]
> Description=MCORCH Canvas Design Bridge (open-design worker — polls design_jobs, runs `od` in the open-design container)
> After=network-online.target docker.service
> Wants=network-online.target
> StartLimitBurst=5
> StartLimitIntervalSec=60
> 
> [Service]
> WorkingDirectory=/home/gcrUX/htdocs/constellation-orchestra
> ExecStart=/home/ubuntu/.bun/bin/bun run scripts/design-bridge.ts
> Restart=always
> RestartSec=5
> TimeoutStopSec=20
> KillMode=control-group
> # design-bridge.ts loads SUPABASE_URL/SB_SECRET_KEY from ../.env itself — no secrets in the unit.
> Environment=HOME=/home/ubuntu
> Environment=TMPDIR=/tmp
> Environment=NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
> Environment=PATH=/home/ubuntu/.bun/bin:/usr/local/bin:/usr/bin:/bin
> 
> [Install]
> WantedBy=default.target
> ```

## 🤖 Claude *(03:17:41)*


## 🤖 Claude *(03:17:42)*

Everything green: Playwright chromium installed, FFmpeg present, `design-bridge.service` is a clean systemd template to mirror. Bucket `video-studio-assets` doesn't exist yet (I'll create it in the VS-2 migration). 

Now building the **render core** — the novel/risky piece. First the deterministic 1080×1920 HTML template:

## 🤖 Claude *(03:18:15)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/templates/viral-short-9x16.html",
  "content": "<!doctype html>\n<!--\n  viral-short-9x16.html \u2014 HyperFrames deterministic 9:16 template (1080\u00d71920) for the Viral Autopilot.\n  BoK SSOT: docs/bok/video-studio/04-frd.md FR-VS-024 (deterministic HTML\u2192MP4) \u00b7 viral-autopilot FR-VA-023.\n  Driven ENTIRELY by window.applyFrame(i, total) \u2014 NO wallclock, NO requestAnimationFrame, NO Math.random,\n  NO external fonts \u2192 byte-reproducible across renders (NFR-VS-016). Props injected via window.applyProps()\n  set text with textContent ONLY (XSS-safe \u2014 the SOP G1 sanitization gate; product/trend/policy are untrusted).\n-->\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\" />\n<style>\n  /* System font stack only \u2014 no network font load race (determinism). */\n  :root { --sans: -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif; }\n  * { margin: 0; padding: 0; box-sizing: border-box; }\n  html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0a0a12; }\n  #stage {\n    position: relative; width: 1080px; height: 1920px;\n    font-family: var(--sans); color: #fff; -webkit-font-smoothing: antialiased;\n    background: radial-gradient(120% 80% at 50% 0%, #1b1430 0%, #0a0a12 60%, #05050a 100%);\n  }\n  /* Product visual \u2014 upper 56%; object-fit cover; deterministic ken-burns via inline transform. */\n  #media {\n    position: absolute; top: 0; left: 0; width: 1080px; height: 1075px; overflow: hidden;\n    background: linear-gradient(135deg, #2a2350, #120e22);\n  }\n  #media img { width: 100%; height: 100%; object-fit: cover; display: block; transform-origin: 50% 45%; }\n  /* Fallback \"product\" card when no image \u2014 deterministic gradient + initials. */\n  #mediaFallback {\n    position: absolute; inset: 0; display: none; align-items: center; justify-content: center;\n    background: linear-gradient(135deg, #6d28d9 0%, #2a2350 55%, #0a0a12 100%);\n    font-size: 220px; font-weight: 800; color: rgba(255,255,255,.14); letter-spacing: -8px;\n  }\n  /* Scrim so text reads over any image. */\n  #scrim { position: absolute; top: 0; left: 0; width: 1080px; height: 1075px;\n    background: linear-gradient(180deg, rgba(10,10,18,.05) 0%, rgba(10,10,18,0) 38%, rgba(10,10,18,.78) 100%); }\n  /* Brand watermark \u2014 top-left. */\n  #brand { position: absolute; top: 54px; left: 60px; font-size: 34px; font-weight: 700;\n    letter-spacing: .5px; opacity: .92; display: flex; align-items: center; gap: 16px; }\n  #brand .dot { width: 18px; height: 18px; border-radius: 50%;\n    background: linear-gradient(135deg, #a855f7, #6366f1); box-shadow: 0 0 24px rgba(168,85,247,.8); }\n  /* Copy block \u2014 lower third. */\n  #copy { position: absolute; left: 60px; right: 60px; bottom: 360px; }\n  #hook { font-size: 96px; line-height: 1.02; font-weight: 800; letter-spacing: -2px;\n    text-shadow: 0 6px 40px rgba(0,0,0,.6); }\n  #caption { margin-top: 34px; font-size: 44px; line-height: 1.28; font-weight: 500;\n    color: rgba(255,255,255,.88); text-shadow: 0 4px 24px rgba(0,0,0,.55); }\n  /* CTA pill \u2014 bottom. */\n  #cta { position: absolute; left: 60px; bottom: 190px; display: inline-flex; align-items: center;\n    gap: 22px; padding: 34px 56px; border-radius: 999px; font-size: 46px; font-weight: 700;\n    background: linear-gradient(135deg, #a855f7, #6366f1); box-shadow: 0 18px 60px rgba(99,102,241,.55);\n    transform-origin: left center; }\n  #cta .arrow { font-size: 40px; }\n  /* Progress bar \u2014 very bottom. */\n  #progress { position: absolute; left: 0; bottom: 0; height: 10px; width: 0;\n    background: linear-gradient(90deg, #a855f7, #6366f1); }\n</style>\n</head>\n<body>\n  <div id=\"stage\">\n    <div id=\"media\">\n      <img id=\"mediaImg\" alt=\"\" />\n      <div id=\"mediaFallback\"></div>\n    </div>\n    <div id=\"scrim\"></div>\n    <div id=\"brand\"><span class=\"dot\"></span><span id=\"brandText\">MCORCH</span></div>\n    <div id=\"copy\">\n      <div id=\"hook\"></div>\n      <div id=\"caption\"></div>\n    </div>\n    <div id=\"cta\"><span id=\"ctaText\"></span><span class=\"arrow\">\u2192</span></div>\n    <div id=\"progress\"></div>\n  </div>\n\n<script>\n// \u2500\u2500 Props injection (textContent ONLY \u2192 XSS-safe; image via validated src) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nwindow.applyProps = function (p) {\n  p = p || {};\n  document.getElementById('brandText').textContent = String(p.brand || 'MCORCH');\n  document.getElementById('hook').textContent      = String(p.hook || '');\n  document.getElementById('caption').textContent   = String(p.caption || '');\n  document.getElementById('ctaText').textContent   = String(p.cta || 'Ver oferta');\n  var img = document.getElementById('mediaImg');\n  var fb  = document.getElementById('mediaFallback');\n  var url = typeof p.product_image_url === 'string' ? p.product_image_url : '';\n  var ok = /^https:\\/\\//i.test(url) || /^data:image\\//i.test(url); // https or data-uri only\n  if (ok) {\n    img.style.display = 'block'; fb.style.display = 'none';\n    img.onerror = function () { img.style.display = 'none'; fb.style.display = 'flex'; };\n    img.src = url;\n  } else {\n    img.style.display = 'none'; fb.style.display = 'flex';\n    var initials = String(p.brand || p.hook || 'MC').replace(/[^A-Za-z\u00c0-\u00ff ]/g, '').trim().slice(0, 2).toUpperCase() || 'MC';\n    fb.textContent = initials;\n  }\n};\n\n// \u2500\u2500 Deterministic per-frame animation. p = i/(total-1) \u2208 [0,1]. No wallclock. \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nfunction easeOutCubic(t) { t = Math.max(0, Math.min(1, t)); return 1 - Math.pow(1 - t, 3); }\nfunction seg(p, a, b) { return easeOutCubic((p - a) / (b - a)); } // 0 before a, eased a\u2192b, 1 after b\n\nwindow.applyFrame = function (i, total) {\n  var p = total > 1 ? i / (total - 1) : 0;\n\n  // Ken-burns: scale 1.00 \u2192 1.09 across the whole clip.\n  var img = document.getElementById('mediaImg');\n  var fb  = document.getElementById('mediaFallback');\n  var kb = 'scale(' + (1 + 0.09 * easeOutCubic(p)).toFixed(5) + ')';\n  img.style.transform = kb; fb.style.transform = kb;\n\n  // Hook: slide up + fade in over 0.00\u21920.22.\n  var h = seg(p, 0.0, 0.22);\n  var hook = document.getElementById('hook');\n  hook.style.opacity = h.toFixed(4);\n  hook.style.transform = 'translateY(' + ((1 - h) * 48).toFixed(2) + 'px)';\n\n  // Caption: fade in 0.14\u21920.40.\n  var c = seg(p, 0.14, 0.40);\n  var cap = document.getElementById('caption');\n  cap.style.opacity = c.toFixed(4);\n  cap.style.transform = 'translateY(' + ((1 - c) * 36).toFixed(2) + 'px)';\n\n  // CTA: pop in 0.30\u21920.52, then deterministic pulse via cosine of frame index (no wallclock).\n  var ci = seg(p, 0.30, 0.52);\n  var pulse = 1 + 0.035 * (0.5 - 0.5 * Math.cos((i / 9) * Math.PI)); // period = 18 frames\n  var cta = document.getElementById('cta');\n  cta.style.opacity = ci.toFixed(4);\n  cta.style.transform = 'scale(' + (ci * pulse).toFixed(5) + ')';\n\n  // Progress bar.\n  document.getElementById('progress').style.width = (p * 1080).toFixed(2) + 'px';\n};\n\n// Initial state.\nwindow.applyProps({});\nwindow.applyFrame(0, 2);\n</script>\n</body>\n</html>\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/templates/viral-short-9x16.html (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:18:19)*

Now the render core — composition spec → frames (Playwright) → MP4 (FFmpeg), deterministic:

## 🤖 Claude *(03:18:51)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/render-core.ts",
  "content": "#!/usr/bin/env bun\n/**\n * scripts/hyperframes/render-core.ts\n *\n * HyperFrames deterministic render engine: a composition spec \u2192 9:16 1080\u00d71920 MP4.\n * BoK SSOT: docs/bok/video-studio/04-frd.md FR-VS-024 (deterministic HTML\u2192MP4 via headless Chrome + FFmpeg)\n *           + FR-VS-025 (per-render sandbox) \u00b7 viral-autopilot FR-VA-023/024 \u00b7 SOP autopilot-video-9x16.md.\n *\n * Pipeline (no AI leg \u2014 fully deterministic, NFR-VS-016):\n *   1. Playwright Chromium headless, viewport 1080\u00d71920, deviceScaleFactor 1.\n *   2. Load templates/<template>.html (file://), inject props via applyProps (textContent \u2192 XSS-safe).\n *   3. For each of N = duration_s \u00d7 fps frames: applyFrame(i, N) \u2192 page.screenshot(PNG).\n *   4. FFmpeg: PNG sequence \u2192 H.264 yuv420p MP4, fixed fps, -fflags +bitexact (reproducible).\n *\n * This is the renderer CORE \u2014 pure (no DB, no network beyond the product image). The host worker\n * (video-bridge.ts) wraps it with the queue claim + upload + finalize_video_render.\n *\n * CLI (material proof): bun run scripts/hyperframes/render-core.ts --out /tmp/test.mp4 \\\n *     --hook \"Sua casa limpa sozinha\" --caption \"Rob\u00f4 aspirador...\" --cta \"Ver no ML\" --duration 4\n */\n\nimport { chromium } from 'playwright';\nimport { spawn } from 'child_process';\nimport { mkdtempSync, rmSync, existsSync, statSync } from 'fs';\nimport { join, dirname, resolve } from 'path';\nimport { tmpdir } from 'os';\nimport { fileURLToPath } from 'url';\n\nconst __dirname = dirname(fileURLToPath(import.meta.url));\n\nexport interface CompositionProps {\n  hook?: string;\n  caption?: string;\n  cta?: string;\n  brand?: string;\n  product_image_url?: string;\n}\n\nexport interface RenderSpec {\n  template?: string;        // template name under templates/ (default 'viral-short-9x16')\n  props: CompositionProps;\n  duration_s?: number;      // default 6\n  fps?: number;             // default 30\n  width?: number;           // default 1080\n  height?: number;          // default 1920\n}\n\nexport interface RenderResult {\n  outPath: string;\n  bytes: number;\n  width: number;\n  height: number;\n  frames: number;\n  fps: number;\n  durationMs: number;\n}\n\nconst VALID_TEMPLATES = new Set(['viral-short-9x16']); // allowlist \u2014 never load an arbitrary path\n\nfunction runFfmpeg(args: string[]): Promise<void> {\n  return new Promise((res, rej) => {\n    const p = spawn('ffmpeg', args, { stdio: ['ignore', 'ignore', 'pipe'] });\n    let err = '';\n    p.stderr.on('data', (d) => { err += d.toString(); });\n    p.on('error', rej);\n    p.on('close', (code) => (code === 0 ? res() : rej(new Error(`ffmpeg exit ${code}: ${err.slice(-800)}`))));\n  });\n}\n\n/**\n * Render a composition spec to a deterministic 9:16 MP4 at `outPath`.\n * Throws on any failure (the worker translates that to finalize_video_render(failed, refund)).\n */\nexport async function renderComposition(spec: RenderSpec, outPath: string): Promise<RenderResult> {\n  const t0 = Date.now();\n  const template = spec.template && VALID_TEMPLATES.has(spec.template) ? spec.template : 'viral-short-9x16';\n  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));\n  const durationS = Math.max(1, Math.min(60, spec.duration_s ?? 6));\n  const width = spec.width ?? 1080;\n  const height = spec.height ?? 1920;\n  const totalFrames = Math.round(durationS * fps);\n\n  const templatePath = resolve(__dirname, 'templates', `${template}.html`);\n  if (!existsSync(templatePath)) throw new Error(`template_not_found: ${template}`);\n\n  const frameDir = mkdtempSync(join(tmpdir(), 'hf-frames-'));\n  const browser = await chromium.launch({\n    headless: true,\n    // Single-tenant Usu\u00e1rio Zero (OTD-VA-011). Multi-tenant hardening (seccomp/egress-only container) = User 1.\n    args: ['--no-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb', '--disable-lcd-text'],\n  });\n  try {\n    const page = await browser.newPage({\n      viewport: { width, height },\n      deviceScaleFactor: 1,\n    });\n    await page.goto(`file://${templatePath}`, { waitUntil: 'load' });\n    await page.evaluate((props) => (window as any).applyProps(props), spec.props as Record<string, unknown>);\n\n    // Deterministically wait for the product image (if any) to settle \u2014 bounded, no wallclock leakage into frames.\n    await page.evaluate(() => new Promise<void>((res) => {\n      const img = document.getElementById('mediaImg') as HTMLImageElement | null;\n      if (!img || img.style.display === 'none' || img.complete) return res();\n      const done = () => res();\n      img.addEventListener('load', done, { once: true });\n      img.addEventListener('error', done, { once: true });\n      setTimeout(done, 8000);\n    }));\n\n    // Frame-by-frame capture (driven by index, not time \u2192 reproducible).\n    for (let i = 0; i < totalFrames; i++) {\n      await page.evaluate(([idx, total]) => (window as any).applyFrame(idx, total), [i, totalFrames] as [number, number]);\n      await page.screenshot({\n        path: join(frameDir, `f_${String(i).padStart(5, '0')}.png`),\n        clip: { x: 0, y: 0, width, height },\n        animations: 'disabled',\n      });\n    }\n    await browser.close();\n\n    // PNG sequence \u2192 MP4. -fflags/-flags +bitexact + no metadata \u2192 byte-reproducible (NFR-VS-016).\n    await runFfmpeg([\n      '-y',\n      '-framerate', String(fps),\n      '-i', join(frameDir, 'f_%05d.png'),\n      '-c:v', 'libx264',\n      '-preset', 'medium',\n      '-crf', '20',\n      '-pix_fmt', 'yuv420p',\n      '-r', String(fps),\n      '-movflags', '+faststart',\n      '-fflags', '+bitexact',\n      '-flags:v', '+bitexact',\n      '-map_metadata', '-1',\n      outPath,\n    ]);\n\n    if (!existsSync(outPath)) throw new Error('render_produced_no_file');\n    const bytes = statSync(outPath).size;\n    if (bytes < 100 * 1024) throw new Error(`render_too_small: ${bytes} bytes (< 100KB, Lei 1 gate)`);\n\n    return { outPath, bytes, width, height, frames: totalFrames, fps, durationMs: Date.now() - t0 };\n  } finally {\n    await browser.close().catch(() => {});\n    rmSync(frameDir, { recursive: true, force: true });\n  }\n}\n\n// \u2500\u2500 CLI (material proof harness) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nif (import.meta.main) {\n  const argv = process.argv.slice(2);\n  const get = (k: string, d?: string) => {\n    const i = argv.indexOf(`--${k}`);\n    return i >= 0 && argv[i + 1] ? argv[i + 1] : d;\n  };\n  const out = get('out', '/tmp/hyperframes-test.mp4')!;\n  const spec: RenderSpec = {\n    template: 'viral-short-9x16',\n    duration_s: Number(get('duration', '4')),\n    fps: Number(get('fps', '30')),\n    props: {\n      hook: get('hook', 'Sua casa limpa sozinha'),\n      caption: get('caption', 'O rob\u00f4 aspirador que faz tudo enquanto voc\u00ea vive a vida.'),\n      cta: get('cta', 'Ver no Mercado Livre'),\n      brand: get('brand', 'MCORCH'),\n      product_image_url: get('image', ''),\n    },\n  };\n  renderComposition(spec, out)\n    .then((r) => {\n      console.log(JSON.stringify(r, null, 2));\n      console.log(`\u2705 rendered ${r.frames} frames \u2192 ${out} (${(r.bytes / 1024).toFixed(0)} KB, ${r.durationMs}ms)`);\n    })\n    .catch((e) => {\n      console.error(`\u274c render failed: ${e instanceof Error ? e.message : e}`);\n      process.exit(1);\n    });\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/render-core.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:18:55)*

Now the material proof (Law 1) — render a real MP4 and `ffprobe` it for 1080×1920:

## 🤖 Claude *(03:18:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== render a 4s 9:16 short ===\"\nbun run scripts/hyperframes/render-core.ts --out /tmp/hf-proof.mp4 --duration 4 --fps 30 2>&1 | tail -20\necho\necho \"=== ffprobe (G3 gate: width=1080 height=1920) ===\"\nffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name,nb_frames,r_frame_rate,pix_fmt -of default=noprint_wrappers=1 /tmp/hf-proof.mp4 2>&1\necho \"--- file ---\"\nls -la /tmp/hf-proof.mp4 && file /tmp/hf-proof.mp4",
  "description": "Render + ffprobe material proof"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === render a 4s 9:16 short ===
> {
>   "outPath": "/tmp/hf-proof.mp4",
>   "bytes": 357938,
>   "width": 1080,
>   "height": 1920,
>   "frames": 120,
>   "fps": 30,
>   "durationMs": 66977
> }
> ✅ rendered 120 frames → /tmp/hf-proof.mp4 (350 KB, 66977ms)
> 
> === ffprobe (G3 gate: width=1080 height=1920) ===
> codec_name=h264
> width=1080
> height=1920
> pix_fmt=yuv420p
> r_frame_rate=30/1
> nb_frames=120
> --- file ---
> -rw-rw-r-- 1 ubuntu ubuntu 357938 Jun 24 00:20 /tmp/hf-proof.mp4
> /tmp/hf-proof.mp4: ISO Media, MP4 Base Media v1 [ISO 14496-12:2003]
> ```

## 🤖 Claude *(03:20:19)*


## 🤖 Claude *(03:20:21)*

**Material proof green (Law 1 · G3):** real MP4, **width=1080 height=1920** (9:16), h264/yuv420p, 30fps, 120 frames, 350KB (≥100KB). The HyperFrames render core works.

Now the determinism gate (G4 / NFR-VS-016 — 2 renders byte-identical). Running a short clip twice and comparing sha256:

## 🤖 Claude *(03:20:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== render twice (2s each) for determinism check ===\"\nbun run scripts/hyperframes/render-core.ts --out /tmp/hf-d1.mp4 --duration 2 --fps 24 --hook \"Determinismo\" >/dev/null 2>&1 && echo \"render 1 done\"\nbun run scripts/hyperframes/render-core.ts --out /tmp/hf-d2.mp4 --duration 2 --fps 24 --hook \"Determinismo\" >/dev/null 2>&1 && echo \"render 2 done\"\necho \"--- sha256 (G4: must match) ---\"\nsha256sum /tmp/hf-d1.mp4 /tmp/hf-d2.mp4\nA=$(sha256sum /tmp/hf-d1.mp4 | cut -d' ' -f1); B=$(sha256sum /tmp/hf-d2.mp4 | cut -d' ' -f1)\n[ \"$A\" = \"$B\" ] && echo \"\u2705 G4 byte-identical (deterministic)\" || echo \"\u26a0\ufe0f G4 NOT byte-identical \u2014 frames may differ or encoder non-determinism\"\necho \"--- frame-level determinism (decode to png, compare) ---\"\nls -la /tmp/hf-d1.mp4 /tmp/hf-d2.mp4",
  "description": "Determinism check \u2014 2 renders sha256"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === render twice (2s each) for determinism check ===
> render 1 done
> render 2 done
> --- sha256 (G4: must match) ---
> 3c58fc3078f12a4a0a6659715f2b99ec7d416fa41ced033570993b4898916bbe  /tmp/hf-d1.mp4
> 3c58fc3078f12a4a0a6659715f2b99ec7d416fa41ced033570993b4898916bbe  /tmp/hf-d2.mp4
> ✅ G4 byte-identical (deterministic)
> --- frame-level determinism (decode to png, compare) ---
> -rw-rw-r-- 1 ubuntu ubuntu 231189 Jun 24 00:20 /tmp/hf-d1.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 231189 Jun 24 00:21 /tmp/hf-d2.mp4
> ```

## 🤖 Claude *(03:21:51)*


## 🤖 Claude *(03:21:54)*

Both material gates **green**:
- **G3:** 1080×1920 (9:16) ✅
- **G4 / NFR-VS-016:** byte-identical sha256 across 2 renders → fully deterministic ✅

The hard part of the motor is proven. (Perf note: ~0.56s/frame via screenshot capture — a 5s@24fps short ≈ 67s, within NFR-VS-002's 90s, but longer clips need CDP-screencast optimization later; I'll log it as an OTD.)

Now wiring it to the queue. Let me check the existing private-bucket + storage-RLS migration pattern (vision-artifacts) to mirror it for `video-studio-assets`:

## 🤖 Claude *(03:21:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nf=$(ls supabase/migrations/*vision_mcp_artifacts* 2>/dev/null | head -1); echo \"=== $f ===\"\ncat \"$f\" 2>/dev/null | head -70",
  "description": "Read vision-artifacts bucket + storage RLS pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === supabase/migrations/20260615190000_vision_mcp_artifacts.sql ===
> -- Migration: vision-mcp artifacts — vision_artifacts + private Storage bucket (FR-VM-009 · FM-VM-11). Fatia 3.
> -- BoK SSOT: docs/bok/vision-mcp/05-sdd.md §7 (migration 4) + §5.2 (RLS + Storage) + 06-data-model.md §2.3.
> -- SOP: docs/processes/vision-mcp-pat-and-erasure.md (Lei 2 — Parte B).
> --
> -- Tracks a vision artifact (frame/crop/derived nodes) for the LGPD erasure cascade: content_ref is the erase
> -- key; node_ids[]/storage_paths[] are the cascade targets; provider_copies records copies sent to providers
> -- (makes their deletion requestable/auditable — FM-VM-11). retention_until drives the daily sweep (art. 16).
> -- RLS: SELECT-own only; writes + DELETE go through the service key (container broker / erase RPC / sweep).
> -- Storage bucket vision-artifacts is PRIVATE (default-deny for anon/authenticated; container brokers signed URLs).
> -- Passes /security-review before commit (FMEA-011 / NFR-VM-007).
> 
> CREATE TABLE IF NOT EXISTS public.vision_artifacts (
>   id              uuid        DEFAULT gen_random_uuid() PRIMARY KEY,
>   content_ref     text        NOT NULL UNIQUE,                 -- chave do cascade de erasure
>   user_id         uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   project_id      uuid,
>   node_ids        uuid[]      NOT NULL DEFAULT '{}',           -- nós mcorch_nodes derivados
>   storage_paths   text[]      NOT NULL DEFAULT '{}',           -- objetos no bucket vision-artifacts
>   provider_copies jsonb       NOT NULL DEFAULT '[]'::jsonb,    -- cópias enviadas a providers (FM-VM-11)
>   retention_until timestamptz NOT NULL,                        -- > now(); ≤ teto DD-VM-004 (sweep diário)
>   created_at      timestamptz NOT NULL DEFAULT now()
> );
> 
> ALTER TABLE public.vision_artifacts ENABLE ROW LEVEL SECURITY;
> 
> -- SELECT-own only. DELETE only via erase_vision_artifacts (SECURITY DEFINER, auth.uid()-scoped) or the
> -- retention sweep (service-role) — no client write/delete policy → default-deny.
> CREATE POLICY "vision_artifacts_select_own" ON public.vision_artifacts
>   FOR SELECT USING (user_id = auth.uid());
> 
> CREATE INDEX IF NOT EXISTS vision_artifacts_retention_idx ON public.vision_artifacts (retention_until);
> CREATE INDEX IF NOT EXISTS vision_artifacts_user_idx      ON public.vision_artifacts (user_id);
> 
> COMMENT ON TABLE public.vision_artifacts IS
>   'Vision MCP artifact ledger for the LGPD erasure cascade (FR-VM-009). content_ref = erase key; node_ids/'
>   'storage_paths = cascade targets; provider_copies = auditable provider-copy registry. SELECT-own RLS.';
> 
> -- Private Storage bucket (parity with generated-videos). Container brokers short signed URLs; client never
> -- reads the bucket directly.
> INSERT INTO storage.buckets (id, name, public) VALUES ('vision-artifacts', 'vision-artifacts', false)
>   ON CONFLICT (id) DO NOTHING;
> -- NOTE (apply-reality): storage.objects RLS is ALREADY enabled project-wide and EVERY existing policy is
> -- bucket-scoped (USING bucket_id='<specific>'); there is NO broad USING(true) policy (verified 2026-06-15). So
> -- the new private bucket 'vision-artifacts' inherits DEFAULT-DENY for anon/authenticated automatically — no
> -- permissive policy matches it. The SDD's explicit `…_no_direct_anon` SELECT policy is therefore REDUNDANT
> -- (service_role already bypasses RLS) and is intentionally OMITTED here: the migration role is not the owner of
> -- storage.objects (42501), and a dashboard/storage-admin-applied policy would only restate the default-deny.
> -- Isolation = private bucket + project-wide bucket-scoped RLS (no matching policy). If an explicit belt-and-
> -- suspenders policy is ever wanted, apply it via the Supabase dashboard (storage-admin role).
> ```

## 🤖 Claude *(03:22:00)*


## 🤖 Claude *(03:22:01)*

Pattern clear: private bucket inherits default-deny from project-wide bucket-scoped RLS; no `CREATE POLICY` on `storage.objects` (migration role isn't owner). Writing the VS-2 migration — `composition` column + private bucket:

## 🤖 Claude *(03:22:16)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260624120000_video_studio_composition_and_bucket.sql",
  "content": "-- Migration: video-studio Fatia VS-2 \u2014 render composition spec + private asset bucket.\n-- BoK SSOT: docs/bok/video-studio/04-frd.md FR-VS-024 (deterministic HTML\u2192MP4) + 05-sdd.md \u00a72.3 (drift\n--           reconciliation 2026-06-24) \u00b7 viral-autopilot FR-VA-023/024 (Amendment v0.2).\n-- SOP (Lei 2): docs/processes/autopilot-video-9x16.md (gate OTD-VA-009 \u2014 escrito ANTES deste c\u00f3digo).\n--\n-- SCOPE (slice VS-2 \u2014 HyperFrames motor wiring for the single-tenant Usu\u00e1rio Zero, OTD-VA-011):\n--   \u2022 video_renders.composition jsonb \u2014 the render spec the host worker (video-bridge.ts) consumes:\n--       { template, props:{hook,caption,cta,brand,product_image_url}, duration_s, fps }. NULL = legacy/faceless.\n--       Untrusted fields (product/trend/policy) are sanitized+escaped UPSTREAM (FR-VA-023 / SOP G1) and rendered\n--       via textContent in the template (XSS-safe); this column only TRANSPORTS the already-sanitized spec.\n--   \u2022 Storage bucket video-studio-assets (PRIVATE) \u2014 the MP4 lands here; video_assets.storage_key references it.\n--       Parity with vision-artifacts (20260615190000): project-wide bucket-scoped RLS gives DEFAULT-DENY to\n--       anon/authenticated automatically; the worker writes via the service key; clients read via signed URLs.\n--\n-- No new RLS on video_renders (the sealed 20260622040000 policies stand: SELECT own-or-org; service-role writes).\n-- Passes /security-review before commit (additive column + private bucket; no policy/grant surface change).\n\n-- 1. Composition spec column (additive, nullable \u2014 backward-compat with faceless + Fatia 1 rows).\nALTER TABLE public.video_renders\n  ADD COLUMN IF NOT EXISTS composition jsonb;\n\nCOMMENT ON COLUMN public.video_renders.composition IS\n  'HyperFrames render spec consumed by the host worker (video-bridge.ts): { template, props, duration_s, fps }. '\n  'Untrusted props are sanitized/escaped upstream (FR-VA-023 / SOP autopilot-video-9x16 G1); rendered via '\n  'textContent (XSS-safe). NULL = faceless/legacy. FR-VS-024 deterministic HTML\u2192MP4.';\n\n-- 2. Private asset bucket (mirrors vision-artifacts / generated-videos). Default-deny inherited from the\n--    project-wide bucket-scoped storage.objects RLS \u2014 no explicit policy needed (and the migration role does\n--    not own storage.objects \u2192 a CREATE POLICY here would 42501). Worker writes via service key; client reads\n--    via short signed URLs minted server-side.\nINSERT INTO storage.buckets (id, name, public)\n  VALUES ('video-studio-assets', 'video-studio-assets', false)\n  ON CONFLICT (id) DO NOTHING;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260624120000_video_studio_composition_and_bucket.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:22:29)*


## 🤖 Claude *(03:22:30)*

Now applying the migration (additive column + private bucket — low risk, mirrors vision-artifacts):

## 🤖 Claude *(03:22:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== applying VS-2 migration ===\"\nnpx supabase db push --include-all 2>&1 | tail -25",
  "description": "Apply VS-2 migration via supabase db push"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === applying VS-2 migration ===
> Initialising login role...
> Connecting to remote database...
> Do you want to push these migrations to the remote database?
>  • 20260624120000_video_studio_composition_and_bucket.sql
> 
>  [Y/n] 
> Applying migration 20260624120000_video_studio_composition_and_bucket.sql...
> Finished supabase db push.
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(03:22:39)*


## 🤖 Claude *(03:22:39)*

Migration applied. Verifying materially (column + bucket exist):

## 🤖 Claude *(03:22:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env 2>/dev/null\necho \"=== composition column present? ===\"\ncurl -s \"${SUPABASE_URL}/rest/v1/video_renders?select=id,composition&limit=1\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" 2>/dev/null | head -c 200\necho\necho \"=== bucket video-studio-assets present? ===\"\ncurl -s \"${SUPABASE_URL}/storage/v1/bucket\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" 2>/dev/null | python3 -c \"import json,sys; d=json.load(sys.stdin); ids=[b['id'] for b in d]; print('buckets:', ids); print('\u2705 video-studio-assets present' if 'video-studio-assets' in ids else '\u274c MISSING')\"",
  "description": "Verify composition column + bucket materially"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === composition column present? ===
> []
> === bucket video-studio-assets present? ===
> buckets: ['generated-images', 'generated-videos', 'canvas-assets', 'vision-artifacts', 'video-studio-assets']
> ✅ video-studio-assets present
> ```

## 🤖 Claude *(03:22:58)*


## 🤖 Claude *(03:22:59)*

Both verified: `composition` column live (select succeeded), bucket `video-studio-assets` present. Now the host worker — `video-bridge.ts`, mirroring the design-bridge poll/claim pattern + the proven render core:

## 🤖 Claude *(03:23:33)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-bridge.ts",
  "content": "#!/usr/bin/env bun\n/**\n * scripts/video-bridge.ts\n *\n * HyperFrames render bridge \u2014 host worker that polls `video_renders` (engine='hyperframes', state='queued'),\n * atomically claims each, renders the composition \u2192 9:16 1080\u00d71920 MP4 (render-core.ts), uploads to the private\n * bucket `video-studio-assets`, and closes the render via `finalize_video_render` (the ONLY terminal authority).\n *\n * BoK SSOT: docs/bok/video-studio/04-frd.md FR-VS-024/026 + 05-sdd.md \u00a72.3 (drift reconciliation 2026-06-24).\n * SOP (Lei 2): docs/processes/autopilot-video-9x16.md (gate OTD-VA-009).\n * Pattern: mirrors scripts/design-bridge.ts (poll + atomic claim) \u2014 the proven host\u2194cloud bridge (Edge fns can't\n *          reach a host daemon, OTD-VS-... ; the worker pulls). Tenancy: single-tenant Usu\u00e1rio Zero (OTD-VA-011);\n *          multi-tenant sandbox hardening (FR-VS-025 ephemeral container) is deferred to User 1.\n *\n * Supervisor: systemd --user video-bridge.service (Restart=always). Secrets load from ../.env (NOT in the unit).\n * Usage: bun run scripts/video-bridge.ts   (or `--once` to drain queued renders and exit \u2014 used by the smoke).\n */\n\nimport { createClient } from '@supabase/supabase-js';\nimport { existsSync, readFileSync, readFileSync as read, rmSync } from 'fs';\nimport { join, dirname } from 'path';\nimport { fileURLToPath } from 'url';\nimport { renderComposition, type RenderSpec } from './hyperframes/render-core.ts';\n\n// \u2500\u2500 Env (same loader as design-bridge.ts \u2014 no secrets in the systemd unit) \u2500\u2500\nconst __dirname = dirname(fileURLToPath(import.meta.url));\nconst envPath = join(__dirname, '../.env');\nif (existsSync(envPath)) {\n  for (const line of readFileSync(envPath, 'utf-8').split('\\n')) {\n    const m = line.match(/^([^#=\\s][^=]*)=(.*)$/);\n    if (m) process.env[m[1].trim()] = m[2].trim().replace(/^[\"']|[\"']$/g, '');\n  }\n}\n\nconst SUPABASE_URL = process.env.SUPABASE_URL;\nconst SERVICE_KEY = process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY;\nif (!SUPABASE_URL || !SERVICE_KEY) {\n  console.error('\u274c Missing SUPABASE_URL or SB_SECRET_KEY in .env');\n  process.exit(1);\n}\nconst supabase = createClient(SUPABASE_URL, SERVICE_KEY, { auth: { persistSession: false } });\n\nconst BUCKET = 'video-studio-assets';\nconst POLL_MS = 4000;\nconst RUNNING_TIMEOUT_MS = 10 * 60 * 1000; // re-claim a render stuck in 'running' beyond this (dead worker)\n\nfunction logHealth(status: string, event: string, metadata?: Record<string, unknown>) {\n  return supabase.from('infra_health_logs')\n    .insert({ service: 'video-bridge', status, event, metadata: metadata ?? null })\n    .then(() => {}, () => {});\n}\n\n/** Atomic claim: queued\u2192running for exactly one worker. Returns the claimed row or null. */\nasync function claim(renderId: string) {\n  const { data, error } = await supabase\n    .from('video_renders')\n    .update({ state: 'running', updated_at: new Date().toISOString() })\n    .eq('id', renderId)\n    .eq('state', 'queued')\n    .select('id, user_id, engine, charged_mco, composition')\n    .maybeSingle();\n  if (error || !data) return null;\n  return data;\n}\n\n/** Render one claimed row end to end. Never throws \u2014 translates failure to finalize(failed, refund). */\nasync function processRender(row: {\n  id: string; user_id: string; charged_mco: number; composition: unknown;\n}) {\n  const renderId = row.id;\n  const charged = row.charged_mco ?? 0;\n  let outPath: string | null = null;\n  try {\n    const spec = row.composition as RenderSpec | null;\n    if (!spec || typeof spec !== 'object' || !spec.props) {\n      throw new Error('composition_missing_or_invalid');\n    }\n\n    outPath = `/tmp/video-render-${renderId}.mp4`;\n    const result = await renderComposition(spec, outPath);\n\n    // Upload to the private bucket under <user_id>/<render_id>.mp4 (path scopes tenant isolation).\n    const storageKey = `${row.user_id}/${renderId}.mp4`;\n    const bytes = read(outPath);\n    const { error: upErr } = await supabase.storage\n      .from(BUCKET)\n      .upload(storageKey, bytes, { contentType: 'video/mp4', upsert: true });\n    if (upErr) throw new Error(`upload_failed: ${upErr.message}`);\n\n    // Material manifest (the erasure unit, FR-VS-030).\n    await supabase.from('video_assets').insert({\n      user_id: row.user_id, render_id: renderId, kind: 'video',\n      storage_key: storageKey, bytes: result.bytes,\n    }).then(() => {}, () => {});\n\n    // Mesh observation (FR-VS-026) \u2014 best-effort; the embed trigger fires on insert.\n    let nodeId: string | null = null;\n    const { data: node } = await supabase.from('mcorch_nodes').insert({\n      user_id: row.user_id, node_type: 'observation',\n      name: `video-render:${renderId}`,\n      content: `HyperFrames 9:16 render ${result.width}x${result.height} ${result.frames}f @${result.fps}fps (${(result.bytes / 1024).toFixed(0)}KB)`,\n      metadata: { kind: 'video_render', render_id: renderId, storage_key: storageKey, bytes: result.bytes },\n    }).select('id').maybeSingle();\n    nodeId = node?.id ?? null;\n\n    // Terminal: done, refund 0 (prepaid path \u2014 the cycle already paid; the motor never self-bills here).\n    const { data: fin } = await supabase.rpc('finalize_video_render', {\n      p_render_id: renderId, p_state: 'done', p_storage_key: storageKey, p_qa: null, p_node_id: nodeId, p_refund: 0,\n    });\n    console.log(`\u2705 render ${renderId} done \u2192 ${storageKey} (${(result.bytes / 1024).toFixed(0)}KB, ${result.durationMs}ms)`, fin);\n    await logHealth('healthy', 'render_done', { render_id: renderId, bytes: result.bytes });\n  } catch (e) {\n    const msg = e instanceof Error ? e.message : String(e);\n    console.error(`\u274c render ${renderId} failed: ${msg}`);\n    // Refund the charge (failed render delivered no value). finalize is idempotent (guard state IN queued/running).\n    await supabase.rpc('finalize_video_render', {\n      p_render_id: renderId, p_state: 'failed', p_storage_key: null, p_qa: null, p_node_id: null, p_refund: charged,\n    }).then(() => {}, () => {});\n    await logHealth('error', 'render_failed', { render_id: renderId, error: msg });\n  } finally {\n    if (outPath) rmSync(outPath, { force: true });\n  }\n}\n\n/** One drain pass: claim + render every queued hyperframes render. Returns count processed. */\nasync function drainOnce(): Promise<number> {\n  // Reap renders stuck in 'running' past the timeout (dead worker) \u2192 back to queued for re-claim.\n  const cutoff = new Date(Date.now() - RUNNING_TIMEOUT_MS).toISOString();\n  await supabase.from('video_renders')\n    .update({ state: 'queued' })\n    .eq('engine', 'hyperframes').eq('state', 'running').lt('updated_at', cutoff)\n    .then(() => {}, () => {});\n\n  const { data: queued, error } = await supabase\n    .from('video_renders')\n    .select('id')\n    .eq('engine', 'hyperframes').eq('state', 'queued')\n    .order('created_at', { ascending: true })\n    .limit(10);\n  if (error || !queued?.length) return 0;\n\n  let n = 0;\n  for (const q of queued) {\n    const row = await claim(q.id);\n    if (!row) continue; // already claimed by another worker\n    await processRender(row as any);\n    n++;\n  }\n  return n;\n}\n\nasync function main() {\n  const once = process.argv.includes('--once');\n  if (once) {\n    const n = await drainOnce();\n    console.log(`drained ${n} render(s)`);\n    process.exit(0);\n  }\n  console.log('\ud83c\udfac video-bridge running \u2014 polling video_renders (engine=hyperframes, queued)...');\n  await logHealth('healthy', 'worker_started');\n  // eslint-disable-next-line no-constant-condition\n  while (true) {\n    try {\n      await drainOnce();\n    } catch (e) {\n      console.error('poll cycle error:', e);\n      await logHealth('degraded', 'poll_error', { error: e instanceof Error ? e.message : String(e) });\n    }\n    await new Promise((r) => setTimeout(r, POLL_MS));\n  }\n}\n\nmain();\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/video-bridge.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:23:40)*


## 🤖 Claude *(03:23:40)*

Let me clean up a redundant import alias:

## 🤖 Claude *(03:23:42)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-bridge.ts",
  "old_string": "import { existsSync, readFileSync, readFileSync as read, rmSync } from 'fs';",
  "new_string": "import { existsSync, readFileSync, rmSync } from 'fs';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/video-bridge.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:23:43)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-bridge.ts",
  "old_string": "    const storageKey = `${row.user_id}/${renderId}.mp4`;\n    const bytes = read(outPath);",
  "new_string": "    const storageKey = `${row.user_id}/${renderId}.mp4`;\n    const bytes = readFileSync(outPath);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/video-bridge.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:23:52)*


## 🤖 Claude *(03:23:53)*

Worker built. Now the **E2E material proof** of the full motor: insert a queued `video_renders` row → run the worker → verify it renders, uploads, and finalizes. First, User 0's id + insert a test render:

## 🤖 Claude *(03:24:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env 2>/dev/null\necho \"=== User 0 id ===\"\nUID0=$(curl -s \"${SUPABASE_URL}/rest/v1/profiles?select=id,mco_balance&limit=1\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d[0]['id']) if d else print('NONE')\")\necho \"User 0: $UID0\"\nBAL=$(curl -s \"${SUPABASE_URL}/rest/v1/profiles?select=mco_balance&id=eq.${UID0}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -c \"import json,sys; print(json.load(sys.stdin)[0]['mco_balance'])\")\necho \"balance: $BAL\"\necho \"=== insert queued hyperframes render (charged_mco=0 \u2192 prepaid path; no deduct in this motor test) ===\"\nRENDER=$(curl -s -X POST \"${SUPABASE_URL}/rest/v1/video_renders\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n  -d \"{\\\"user_id\\\":\\\"${UID0}\\\",\\\"engine\\\":\\\"hyperframes\\\",\\\"state\\\":\\\"queued\\\",\\\"charged_mco\\\":0,\\\"composition\\\":{\\\"template\\\":\\\"viral-short-9x16\\\",\\\"duration_s\\\":3,\\\"fps\\\":24,\\\"props\\\":{\\\"hook\\\":\\\"Teste do motor HyperFrames\\\",\\\"caption\\\":\\\"Render determin\u00edstico 9:16 via worker host.\\\",\\\"cta\\\":\\\"Ver no ML\\\",\\\"brand\\\":\\\"MCORCH\\\"}}}\")\necho \"$RENDER\" | python3 -c \"import json,sys; d=json.load(sys.stdin); r=d[0] if isinstance(d,list) else d; print('render_id:', r.get('id'), '| state:', r.get('state'))\"\necho \"$RENDER\" | python3 -c \"import json,sys; d=json.load(sys.stdin); r=d[0] if isinstance(d,list) else d; print(r.get('id'))\" > /tmp/test_render_id.txt\necho \"saved render_id: $(cat /tmp/test_render_id.txt)\"",
  "description": "Get User 0 + insert test queued render"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === User 0 id ===
> User 0: ada39fae-67e1-4e53-af1c-5a18e1c108e8
> balance: 5076.0
> === insert queued hyperframes render (charged_mco=0 → prepaid path; no deduct in this motor test) ===
> render_id: ae3b9e97-07bc-4bc6-8c30-f94db25ac47c | state: queued
> saved render_id: ae3b9e97-07bc-4bc6-8c30-f94db25ac47c
> ```

## 🤖 Claude *(03:24:05)*

Render queued (`ae3b9e97`). Now run the worker once to drain it, then verify the full chain:

## 🤖 Claude *(03:24:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== run worker (--once drain) ===\"\ntimeout 120 bun run scripts/video-bridge.ts --once 2>&1 | tail -15",
  "description": "Run video-bridge worker once"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === run worker (--once drain) ===
> ✅ render ae3b9e97-07bc-4bc6-8c30-f94db25ac47c done → ada39fae-67e1-4e53-af1c-5a18e1c108e8/ae3b9e97-07bc-4bc6-8c30-f94db25ac47c.mp4 (265KB, 35076ms) {
>   refunded: 0,
>   finalized: true,
> }
> drained 1 render(s)
> ```

## 🤖 Claude *(03:24:47)*


## 🤖 Claude *(03:24:48)*

Worker drained it (`finalized: true`). Now the full material verification chain — DB state, asset manifest, and the actual MP4 from the bucket (ffprobe):

## 🤖 Claude *(03:24:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env 2>/dev/null\nRID=$(cat /tmp/test_render_id.txt)\nUID0=ada39fae-67e1-4e53-af1c-5a18e1c108e8\necho \"=== 1. video_renders terminal state ===\"\ncurl -s \"${SUPABASE_URL}/rest/v1/video_renders?select=id,state,storage_key,charged_mco,refunded_mco,node_id&id=eq.${RID}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -m json.tool\necho \"=== 2. video_assets manifest ===\"\ncurl -s \"${SUPABASE_URL}/rest/v1/video_assets?select=kind,storage_key,bytes&render_id=eq.${RID}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -m json.tool\necho \"=== 3. download MP4 from bucket + ffprobe (G3) ===\"\ncurl -s \"${SUPABASE_URL}/storage/v1/object/video-studio-assets/${UID0}/${RID}.mp4\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" -o /tmp/bucket-asset.mp4\nls -la /tmp/bucket-asset.mp4\nffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name -of default=noprint_wrappers=1 /tmp/bucket-asset.mp4 2>&1\necho \"=== 4. mesh observation node ===\"\ncurl -s \"${SUPABASE_URL}/rest/v1/mcorch_nodes?select=id,node_type,name&name=eq.video-render:${RID}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print('node:', d[0]['id'], d[0]['node_type'], d[0]['name']) if d else print('NO NODE')\"",
  "description": "Verify full motor chain materially"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === 1. video_renders terminal state ===
> [
>     {
>         "id": "ae3b9e97-07bc-4bc6-8c30-f94db25ac47c",
>         "state": "done",
>         "storage_key": "ada39fae-67e1-4e53-af1c-5a18e1c108e8/ae3b9e97-07bc-4bc6-8c30-f94db25ac47c.mp4",
>         "charged_mco": 0,
>         "refunded_mco": 0,
>         "node_id": "8e5237c6-8cc8-4465-bcfd-a6bfb440a0f1"
>     }
> ]
> === 2. video_assets manifest ===
> [
>     {
>         "kind": "video",
>         "storage_key": "ada39fae-67e1-4e53-af1c-5a18e1c108e8/ae3b9e97-07bc-4bc6-8c30-f94db25ac47c.mp4",
>         "bytes": 271202
>     }
> ]
> === 3. download MP4 from bucket + ffprobe (G3) ===
> -rw-rw-r-- 1 ubuntu ubuntu 271202 Jun 24 00:24 /tmp/bucket-asset.mp4
> codec_name=h264
> width=1080
> height=1920
> === 4. mesh observation node ===
> node: 8e5237c6-8cc8-4465-bcfd-a6bfb440a0f1 observation video-render:ae3b9e97-07bc-4bc6-8c30-f94db25ac47c
> ```

## 🤖 Claude *(03:25:38)*


## 🤖 Claude *(03:25:41)*

**FULL MOTOR CHAIN VERIFIED (Law 1):**
1. ✅ `video_renders.state='done'`, storage_key set, refunded_mco=0
2. ✅ `video_assets` manifest: kind=video, **271202 bytes** (≥100KB)
3. ✅ MP4 from bucket: **width=1080 height=1920** (9:16), h264
4. ✅ Mesh observation node `8e5237c6` linked

The HyperFrames motor works end-to-end (queued → claim → render 9:16 → upload → manifest+mesh → finalize), exactly the design-bridge pattern. Now wiring the enqueue paths: the `video-render` edge fn needs `composition` + a `poll://` trigger (since the edge runtime can't reach the host worker). Three precise edits:

## 🤖 Claude *(03:25:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "old_string": "    const productId = typeof body?.product_id === \"string\" ? body.product_id : null;",
  "new_string": "    const productId = typeof body?.product_id === \"string\" ? body.product_id : null;\n    // HyperFrames render spec (FR-VS-024). The worker (video-bridge.ts) consumes it. Untrusted props are\n    // sanitized/escaped UPSTREAM (FR-VA-023 / SOP G1) and rendered via textContent; here it is only transported.\n    const composition = engine === \"hyperframes\" && body?.composition && typeof body.composition === \"object\"\n      ? body.composition : null;"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(03:25:47)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "old_string": "      .insert({ user_id: userId, engine, topic, product_id: productId, voice_consent: voiceConsent, charged_mco: cost, state: \"queued\" })",
  "new_string": "      .insert({ user_id: userId, engine, topic, product_id: productId, composition, voice_consent: voiceConsent, charged_mco: cost, state: \"queued\" })"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(03:25:55)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "old_string": "    // Trigger the worker. On failure AFTER the charge, refund idempotently via the terminal authority.\n    try {\n      const r = await fetch(workerWebhook, {\n        method: \"POST\",\n        headers: { Authorization: `Bearer ${serviceKey}`, \"Content-Type\": \"application/json\" },\n        body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),\n      });\n      if (!r.ok) throw new Error(`worker HTTP ${r.status}`);\n    } catch (e) {\n      await admin.rpc(\"finalize_video_render\", {\n        p_render_id: renderId, p_state: \"failed\", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,\n      }).then(() => {}, () => {});\n      logHealth(\"error\", \"worker_trigger_failed\");\n      return json({ error: \"worker_unavailable\", detail: e instanceof Error ? e.message : \"trigger failed\", render_id: renderId }, 502);\n    }",
  "new_string": "    // Trigger the worker. Two transports:\n    //   \u2022 poll://  \u2192 a HOST worker (video-bridge.ts for hyperframes) POLLS video_renders; the queued row IS the\n    //                trigger (Edge fns can't reach a host daemon \u2014 the design-bridge lesson). No kick \u2192 202; the\n    //                poller atomically claims (queued\u2192running) and finalizes. This is the hyperframes path.\n    //   \u2022 http(s)  \u2192 a reachable webhook (e.g. a faceless external studio); POST the kick, refund on failure.\n    if (!workerWebhook.startsWith(\"poll://\")) {\n      try {\n        const r = await fetch(workerWebhook, {\n          method: \"POST\",\n          headers: { Authorization: `Bearer ${serviceKey}`, \"Content-Type\": \"application/json\" },\n          body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),\n        });\n        if (!r.ok) throw new Error(`worker HTTP ${r.status}`);\n      } catch (e) {\n        await admin.rpc(\"finalize_video_render\", {\n          p_render_id: renderId, p_state: \"failed\", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,\n        }).then(() => {}, () => {});\n        logHealth(\"error\", \"worker_trigger_failed\");\n        return json({ error: \"worker_unavailable\", detail: e instanceof Error ? e.message : \"trigger failed\", render_id: renderId }, 502);\n      }\n    }"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(03:26:00)*


## 🤖 Claude *(03:26:00)*

I read it via `sed` earlier, not the Read tool. Let me Read it properly first:

## 🤖 Claude *(03:26:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "offset": 58,
  "limit": 75
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 58	    // Voice-consent gate (FR-VS-032): faceless clones a voice (VoxCPM) → identifiable biometric (LGPD Art. 11).
> 59	    if (engine === "faceless" && !voiceConsent) {
> 60	      return json({ error: "voice_consent_required", action: "Confirme o consentimento de uso de voz para gerar o vídeo faceless." }, 409);
> 61	    }
> 62	
> 63	    // BYOK fail-closed (FR-VS-005/006): faceless needs the tenant's Gemini/Google key (director + vision QA). Per-user
> 64	    // first; NO silent global fallback in a user-facing path (API Tenancy Model). hyperframes is deterministic (no AI leg).
> 65	    // The canonical Vault column is `google_api_key` (NOT `gemini_api_key` — the BoK 06 §2.5 / CLAUDE.md naming is
> 66	    // stale; canvas-execute + the live decrypted view use google_api_key, verified 2026-06-22 via 42703 on gemini_api_key).
> 67	    if (engine === "faceless") {
> 68	      const { data: keys } = await admin
> 69	        .from("decrypted_user_api_keys").select("google_api_key").eq("user_id", userId).maybeSingle();
> 70	      if (!keys?.google_api_key) {
> 71	        return json({ error: "gemini_not_configured", action: "Configure sua chave Gemini/Google em /dashboard/settings para gerar vídeo." }, 402);
> 72	      }
> 73	    }
> 74	
> 75	    const cost = COST[engine];
> 76	
> 77	    // dry_run: cost projection WITHOUT deduct or row (zero-cost proof path; mirrors autopilot-run).
> 78	    if (dryRun) return json({ ok: true, dry_run: true, engine, cost_mco: cost });
> 79	
> 80	    // Engine-availability gate (SLICE 1): the worker webhook is unset until slice 2 wires the render engine.
> 81	    // Returning 503 HERE — before any deduct — guarantees no tenant is charged for a render that cannot complete.
> 82	    const workerWebhook = engine === "faceless"
> 83	      ? Deno.env.get("VIDEO_FACELESS_WEBHOOK")
> 84	      : Deno.env.get("VIDEO_HYPERFRAMES_WEBHOOK");
> 85	    if (!workerWebhook) {
> 86	      return json({
> 87	        error: "render_engine_unavailable",
> 88	        detail: `O motor de render '${engine}' entra na Fatia 2 (faceless: ponte de rede + n8n; hyperframes: sandbox). Nenhum mcoCoin foi debitado.`,
> 89	      }, 503);
> 90	    }
> 91	
> 92	    // ── SLICE 2 prepaid path (activates once the worker webhook env is set) ──────────────────────────────────────
> 93	    // Charge-at-entry (FR-VS-009): atomic deduct BEFORE any leg. 402 if balance < cost (zero rows created).
> 94	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: cost });
> 95	    if (deductErr) {
> 96	      logHealth("degraded", "insufficient_balance");
> 97	      return json({ error: "insufficient_balance", detail: `Saldo insuficiente: render '${engine}' custa ${cost} mcoCoins.`, cost_mco: cost }, 402);
> 98	    }
> 99	
> 100	    // INSERT the queued render (service key — RLS denies tenant writes; this is the only writer). org_id/client_id
> 101	    // NULL = solo creator (§AG agency scoping wires in a later slice).
> 102	    const { data: render, error: insErr } = await admin
> 103	      .from("video_renders")
> 104	      .insert({ user_id: userId, engine, topic, product_id: productId, voice_consent: voiceConsent, charged_mco: cost, state: "queued" })
> 105	      .select("id").single();
> 106	    if (insErr || !render) {
> 107	      // Could not even create the ledger row → refund the just-charged cost (no render_id yet → direct credit).
> 108	      await admin.rpc("add_mco_coins", { p_user_id: userId, p_amount: cost }).then(() => {}, () => {});
> 109	      logHealth("error", "insert_failed");
> 110	      return json({ error: "render_create_failed", detail: insErr?.message }, 500);
> 111	    }
> 112	    const renderId = render.id as string;
> 113	
> 114	    // Trigger the worker. On failure AFTER the charge, refund idempotently via the terminal authority.
> 115	    try {
> 116	      const r = await fetch(workerWebhook, {
> 117	        method: "POST",
> 118	        headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 119	        body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),
> 120	      });
> 121	      if (!r.ok) throw new Error(`worker HTTP ${r.status}`);
> 122	    } catch (e) {
> 123	      await admin.rpc("finalize_video_render", {
> 124	        p_render_id: renderId, p_state: "failed", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,
> 125	      }).then(() => {}, () => {});
> 126	      logHealth("error", "worker_trigger_failed");
> 127	      return json({ error: "worker_unavailable", detail: e instanceof Error ? e.message : "trigger failed", render_id: renderId }, 502);
> 128	    }
> 129	
> 130	    logHealth("healthy", "render_submitted");
> 131	    return json({ ok: true, render_id: renderId, engine, charged_mco: cost, state: "queued" }, 202);
> 132	  } catch (e) {
> ```

## 🤖 Claude *(03:26:10)*


## 🤖 Claude *(03:26:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "offset": 51,
  "limit": 7
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 51	      return json({ error: "engine_invalid", detail: "engine deve ser 'faceless' ou 'hyperframes'" }, 422);
> 52	    }
> 53	    const dryRun = body?.dry_run === true;
> 54	    const voiceConsent = body?.voice_consent === true;
> 55	    const topic = typeof body?.topic === "string" ? body.topic.slice(0, 500) : null;
> 56	    const productId = typeof body?.product_id === "string" ? body.product_id : null;
> 57	
> ```

## 🤖 Claude *(03:26:21)*

Now the three edits to `video-render`:

## 🤖 Claude *(03:26:24)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "old_string": "    const productId = typeof body?.product_id === \"string\" ? body.product_id : null;\n",
  "new_string": "    const productId = typeof body?.product_id === \"string\" ? body.product_id : null;\n    // HyperFrames render spec (FR-VS-024). The host worker (video-bridge.ts) consumes it. Untrusted props are\n    // sanitized/escaped UPSTREAM (FR-VA-023 / SOP autopilot-video-9x16 G1) and rendered via textContent (XSS-safe);\n    // here the spec is only transported into the queued row.\n    const composition = engine === \"hyperframes\" && body?.composition && typeof body.composition === \"object\"\n      ? body.composition : null;\n"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:26:26)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "old_string": "      .insert({ user_id: userId, engine, topic, product_id: productId, voice_consent: voiceConsent, charged_mco: cost, state: \"queued\" })",
  "new_string": "      .insert({ user_id: userId, engine, topic, product_id: productId, composition, voice_consent: voiceConsent, charged_mco: cost, state: \"queued\" })"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:26:35)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts",
  "old_string": "    // Trigger the worker. On failure AFTER the charge, refund idempotently via the terminal authority.\n    try {\n      const r = await fetch(workerWebhook, {\n        method: \"POST\",\n        headers: { Authorization: `Bearer ${serviceKey}`, \"Content-Type\": \"application/json\" },\n        body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),\n      });\n      if (!r.ok) throw new Error(`worker HTTP ${r.status}`);\n    } catch (e) {\n      await admin.rpc(\"finalize_video_render\", {\n        p_render_id: renderId, p_state: \"failed\", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,\n      }).then(() => {}, () => {});\n      logHealth(\"error\", \"worker_trigger_failed\");\n      return json({ error: \"worker_unavailable\", detail: e instanceof Error ? e.message : \"trigger failed\", render_id: renderId }, 502);\n    }",
  "new_string": "    // Trigger the worker. Two transports:\n    //   \u2022 poll://  \u2192 a HOST worker (video-bridge.ts for hyperframes) POLLS video_renders; the queued row IS the\n    //                trigger (Edge fns can't reach a host daemon \u2014 the design-bridge lesson). No kick \u2192 202; the\n    //                poller atomically claims (queued\u2192running) and finalizes via finalize_video_render.\n    //   \u2022 http(s)  \u2192 a reachable webhook (e.g. a faceless external studio); POST the kick, refund on failure.\n    if (!workerWebhook.startsWith(\"poll://\")) {\n      try {\n        const r = await fetch(workerWebhook, {\n          method: \"POST\",\n          headers: { Authorization: `Bearer ${serviceKey}`, \"Content-Type\": \"application/json\" },\n          body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),\n        });\n        if (!r.ok) throw new Error(`worker HTTP ${r.status}`);\n      } catch (e) {\n        await admin.rpc(\"finalize_video_render\", {\n          p_render_id: renderId, p_state: \"failed\", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,\n        }).then(() => {}, () => {});\n        logHealth(\"error\", \"worker_trigger_failed\");\n        return json({ error: \"worker_unavailable\", detail: e instanceof Error ? e.message : \"trigger failed\", render_id: renderId }, 502);\n      }\n    }"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:26:42)*


## 🤖 Claude *(03:26:43)*

Now activating the hyperframes engine: set the `VIDEO_HYPERFRAMES_WEBHOOK=poll://hyperframes` secret (engine-live signal + poll transport) and deploy the edge fn:

## 🤖 Claude *(03:26:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== set poll sentinel secret ===\"\nnpx supabase secrets set VIDEO_HYPERFRAMES_WEBHOOK=poll://hyperframes 2>&1 | tail -4\necho \"=== deploy video-render ===\"\nnpx supabase functions deploy video-render 2>&1 | tail -8",
  "description": "Set poll secret + deploy video-render edge fn"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === set poll sentinel secret ===
> Finished supabase secrets set.
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> === deploy video-render ===
> Bundling Function: video-render
> Deploying Function: video-render (script size: 62.54kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: video-render
> You can inspect your deployment in the Dashboard: https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa/functions
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(03:27:25)*


## 🤖 Claude *(03:27:25)*

Edge fn deployed (62.54kB), engine now live. Now the systemd unit so the worker runs persistently (mirroring `design-bridge.service`):

## 🤖 Claude *(03:27:29)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.config/systemd/user/video-bridge.service",
  "content": "[Unit]\nDescription=MCORCH HyperFrames Video Bridge (polls video_renders engine=hyperframes, renders HTML\u2192MP4 9:16 via Playwright+FFmpeg)\nAfter=network-online.target\nWants=network-online.target\nStartLimitBurst=5\nStartLimitIntervalSec=60\n\n[Service]\nWorkingDirectory=/home/gcrUX/htdocs/constellation-orchestra\nExecStart=/home/ubuntu/.bun/bin/bun run scripts/video-bridge.ts\nRestart=always\nRestartSec=5\nTimeoutStopSec=20\nKillMode=control-group\n# video-bridge.ts loads SUPABASE_URL/SB_SECRET_KEY from ../.env itself \u2014 no secrets in the unit (parity design-bridge).\nEnvironment=HOME=/home/ubuntu\nEnvironment=TMPDIR=/tmp\nEnvironment=NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt\nEnvironment=PATH=/home/ubuntu/.bun/bin:/usr/local/bin:/usr/bin:/bin\n\n[Install]\nWantedBy=default.target\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.config/systemd/user/video-bridge.service (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:27:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "export XDG_RUNTIME_DIR=/run/user/$(id -u ubuntu 2>/dev/null || echo 1001)\necho \"=== enable + start video-bridge.service ===\"\nsystemctl --user daemon-reload 2>&1\nsystemctl --user enable --now video-bridge.service 2>&1\nsleep 3\necho \"=== status ===\"\nsystemctl --user is-active video-bridge.service\nsystemctl --user status video-bridge.service --no-pager 2>&1 | head -14",
  "description": "Enable and start video-bridge systemd service"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === enable + start video-bridge.service ===
> Created symlink /home/ubuntu/.config/systemd/user/default.target.wants/video-bridge.service → /home/ubuntu/.config/systemd/user/video-bridge.service.
> === status ===
> active
> ● video-bridge.service - MCORCH HyperFrames Video Bridge (polls video_renders engine=hyperframes, renders HTML→MP4 9:16 via Playwright+FFmpeg)
>      Loaded: loaded (/home/ubuntu/.config/systemd/user/video-bridge.service; enabled; preset: enabled)
>      Active: active (running) since Wed 2026-06-24 00:27:34 -03; 3s ago
>    Main PID: 900006 (bun)
>       Tasks: 13 (limit: 28691)
>      Memory: 56.5M (peak: 61.0M)
>         CPU: 542ms
>      CGroup: /user.slice/user-1001.slice/user@1001.service/app.slice/video-bridge.service
>              └─900006 /home/ubuntu/.bun/bin/bun run scripts/video-bridge.ts
> 
> Jun 24 00:27:34 panel.gcrux.com systemd[1255]: Started video-bridge.service - MCORCH HyperFrames Video Bridge (polls video_renders engine=hyperframes, renders HTML→MP4 9:16 via Playwright+FFmpeg).
> Jun 24 00:27:35 panel.gcrux.com bun[900006]: 🎬 video-bridge running — polling video_renders (engine=hyperframes, queued)...
> ```

## 🤖 Claude *(03:28:06)*


## 🤖 Claude *(03:28:07)*

Worker is **`active (running)`** (PID 900006), polling live. The HyperFrames motor (Fatia VS-2) is deployed and operational.

Let me clean up the test render artifact (prod hygiene — the proof is already captured) and confirm the worker survives a fresh queued render through the *running service* (not just `--once`):

## 🤖 Claude *(03:28:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env 2>/dev/null\nUID0=ada39fae-67e1-4e53-af1c-5a18e1c108e8\necho \"=== fresh queued render \u2192 live service should pick it up within ~8s ===\"\nR2=$(curl -s -X POST \"${SUPABASE_URL}/rest/v1/video_renders\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n  -d \"{\\\"user_id\\\":\\\"${UID0}\\\",\\\"engine\\\":\\\"hyperframes\\\",\\\"state\\\":\\\"queued\\\",\\\"charged_mco\\\":0,\\\"composition\\\":{\\\"template\\\":\\\"viral-short-9x16\\\",\\\"duration_s\\\":2,\\\"fps\\\":24,\\\"props\\\":{\\\"hook\\\":\\\"Service live\\\",\\\"caption\\\":\\\"Picked up by the running systemd worker.\\\",\\\"cta\\\":\\\"OK\\\"}}}\" \\\n  | python3 -c \"import json,sys; print(json.load(sys.stdin)[0]['id'])\")\necho \"queued: $R2\"\necho \"--- wait for the live worker to process (poll=4s + render ~25s) ---\"\nfor i in $(seq 1 12); do\n  sleep 5\n  ST=$(curl -s \"${SUPABASE_URL}/rest/v1/video_renders?select=state&id=eq.${R2}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -c \"import json,sys; print(json.load(sys.stdin)[0]['state'])\")\n  echo \"  t+$((i*5))s: state=$ST\"\n  [ \"$ST\" = \"done\" ] && break\ndone\necho \"=== cleanup BOTH test renders (prod hygiene; proof already captured) ===\"\nfor RID in ae3b9e97-07bc-4bc6-8c30-f94db25ac47c $R2; do\n  curl -s -X DELETE \"${SUPABASE_URL}/storage/v1/object/video-studio-assets/${UID0}/${RID}.mp4\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" >/dev/null\n  curl -s -X DELETE \"${SUPABASE_URL}/rest/v1/video_assets?render_id=eq.${RID}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" >/dev/null\n  curl -s -X DELETE \"${SUPABASE_URL}/rest/v1/mcorch_nodes?name=eq.video-render:${RID}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" >/dev/null\n  curl -s -X DELETE \"${SUPABASE_URL}/rest/v1/video_renders?id=eq.${RID}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" >/dev/null\n  echo \"  cleaned $RID\"\ndone\necho \"--- verify clean ---\"\ncurl -s \"${SUPABASE_URL}/rest/v1/video_renders?select=id&user_id=eq.${UID0}\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print(f'{len(d)} test renders remaining')\"",
  "description": "Prove live service E2E + clean up test artifacts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === fresh queued render → live service should pick it up within ~8s ===
> queued: b907aa5a-9dec-4541-888b-4fd2ed01bd60
> --- wait for the live worker to process (poll=4s + render ~25s) ---
>   t+5s: state=running
>   t+10s: state=running
>   t+15s: state=running
>   t+20s: state=running
>   t+25s: state=running
>   t+30s: state=done
> === cleanup BOTH test renders (prod hygiene; proof already captured) ===
>   cleaned ae3b9e97-07bc-4bc6-8c30-f94db25ac47c
>   cleaned b907aa5a-9dec-4541-888b-4fd2ed01bd60
> --- verify clean ---
> 0 test renders remaining
> ```

## 🤖 Claude *(03:29:13)*


## 🤖 Claude *(03:29:14)*

The live systemd worker picked up the fresh render within ~5s → done at t+30s. Both test artifacts cleaned (0 remaining). **Fatia VS-2 (HyperFrames motor) is COMPLETE and LIVE.**

Per the mandate (every migration + this security-sensitive worker that executes HTML in headless Chrome), running `/security-review` on the VS-2 changes before any commit:

## 🤖 Claude *(03:29:15)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "security-review"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: security-review
> ```

## 👤 User *(03:29:15)*

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   CLAUDE.md
	modified:   docs/bok/video-studio/05-sdd.md
	modified:   docs/bok/viral-autopilot/03-prd.md
	modified:   docs/bok/viral-autopilot/04-frd.md
	modified:   docs/bok/viral-autopilot/05-sdd.md
	modified:   supabase/functions/video-render/index.ts

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/processes/autopilot-video-9x16.md
	scripts/hyperframes/
	scripts/video-bridge.ts
	supabase/migrations/20260624120000_video_studio_composition_and_bucket.sql

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

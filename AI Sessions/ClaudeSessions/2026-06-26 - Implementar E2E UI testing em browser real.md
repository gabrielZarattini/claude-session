# Implementar E2E UI testing em browser real
**Date:** 2026-06-26 | **Session ID:** `3ee740c7-9900-4d37-a9a4-207b63e460bb`

---

## 👤 User *(00:22:28)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(00:22:28)*

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


## 🤖 Claude *(00:22:33)*


## 🤖 Claude *(00:22:34)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with the pre-flight checks in parallel.

## 🤖 Claude *(00:22:34)*


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
> 09a4203 chore(sprint): v6.51.0 — Fatia 2 Reel E2E + notificações P0 + malha cross-módulo + receita
> bfbf2c5 docs(handoff): seal Fatia 2 Reel E2E + notificações P0 + malha cross-módulo + receita
> 8fdb7a9 docs(readme): v6.51.0 — Fatia 2 Reel LIVE (instagram.com/reel/DaBtVAQkiuz) + notificações P0 + malha cross-módulo
> bfb0ba3 fix(notifications): sino real (P0 — notificações nunca funcionaram)
> 3be06ee fix(meta): Reel real publica pela conexão IG existente (Fatia 2 E2E provada)
> 9d9ec03 feat(meta): Fatia 2 — publicar vídeo do ecossistema como Reel (IG + FB)
> 3efbe75 feat(video-studio): starter MCORCH 9:16 lint-clean substitui o demo HeyGen
> ```

## 🤖 Claude *(00:22:35)*


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

## 🤖 Claude *(00:22:36)*


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

## 🤖 Claude *(00:22:36)*


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

## 🤖 Claude *(00:22:38)*


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
> mcorch_vision_mcp: Up 8 days (healthy)
> mcorch_claude_mem: Up 10 days (healthy)
> mcorch_chroma: Up 10 days (healthy)
> ---
> mega-brain-dashboard: Up 10 days
> mega-brain-webhook: Up 10 days (healthy)
> mega-brain-daemon: Up 10 days (healthy)
> ```

## 🤖 Claude *(00:22:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat; echo; ls docs/bok/ 2>/dev/null; echo \"---scratch---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"; echo \"---handoff lines---\"; wc -l HANDOFF.md",
  "description": "Chroma health + BoK list + scratch + handoff size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1782433359730455144}
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
> ---handoff lines---
> 8385 HANDOFF.md
> ```

## 🤖 Claude *(00:22:43)*


## 🤖 Claude *(00:22:43)*

Now reading HANDOFF.md (head + tail), sprint priorities, and checking scratch contents.

## 🤖 Claude *(00:22:44)*


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
> 14	## Session Seal — Fatia 2 vídeo→Instagram Reel PROVADO E2E + Notificações P0 + malha criativa cross-módulo + receita destravada (2026-06-25)
> 15	
> 16	Sessão-maratona multi-arco (`/handson` → "força total pelo primeiro R$" → ecossistema criativo → P0 notificações), operando como **Usuário 00 sobre o Usuário 0** em produção real. **9 commits, tudo provado materialmente (Lei 1).**
> 17	
> 18	**Arco 1 — Reparo do loop de receita (`1ad04c5`).** Diagnóstico material (workflow `wf_792d5d48`): gargalo do 1º R$ = **distribuição + atribuição**, não geração. Cron de auto-publish estava MORTO dias (redirect crontab → `/var/log` inacessível, abortava antes do script) → path durável + telemetria `infra_health_logs`. `buildMlProductUrl` agora publica o **link meli.la assinado** (sale-attributable, estava parado no DB) em vez do bare matt_word; `login.mcorch.com/go` CF-morto → unset `AFFILIATE_REDIRECT_BASE`. CTA-leak (`href=mcorch.com`) fechado por guard determinístico. Backfill links + `matt_tool`. 2 posts injection removidos do LinkedIn real (DELETE 204), 1 post limpo monetizado vivo.
> 19	
> 20	**Arco 2 — Canvas white-screen fix + verificação por browser real (`46f18ca`).** Projeto `63d406fe` abria EM BRANCO (provado em browser via agent-browser + preview local + sessão injetada): `MODEL_INFO[modelId].coinCost` estourava em modelId fora do catálogo (grafo recuperado guardou o id bruto da execução). `getImageModelInfo`/`getVideoModelInfo` com fallback nos 6 sites de render → nunca mais white-screena. Diretiva Sovereign: **verificar todo entregável de UI em browser real**.
> 21	
> 22	**Arco 3 — Malha criativa cross-módulo.** Asset clicável → **handoff real** (asset → novo projeto Canvas como node, provado E2E) (`8c00f88`); white-label HyperFrames via nginx `sub_filter` (logo HeyGen escondido) (`5d58b15`); Biblioteca: **scroll consertado** (`/canvas/assets` não é mais full-canvas) + **filtro por data** + **metadados ricos** no diálogo (`8fdb435`); backfill cross-módulo (galeria mostra 2 source_modules); **starter MCORCH 9:16 lint-clean 0/0** substitui o demo HeyGen (`3efbe75`, decisão Sovereign via AskUserQuestion).
> 23	
> 24	**Arco 4 — Fatia 2: vídeo → Instagram Reel, PROVADO E2E (`9d9ec03`/`3be06ee`).** A saída do ecossistema vira distribuição real. Descoberta: o Usuário 0 **já está conectado** (Instagram `magicorch`, MEDIA_CREATOR, `instagram_business_content_publish`) — não precisa de app/token novo. `publish-social` IG corrigido p/ `graph.instagram.com` (era facebook.com, base errada) + `media_type=REELS` + id de publish via `/me?fields=user_id` (o `platform_user_id` guardado é app-scoped → rejeitado code 100/33). **Reel REAL ao vivo: `https://www.instagram.com/reel/DaBtVAQkiuz/`.**
> 25	
> 26	**Arco 5 — P0 Notificações (`bfb0ba3`).** Achado do Sovereign: notificações não funcionam em nenhuma camada. Causa material: o sino era placeholder MORTO (badge hardcoded "3", sem clique/painel/dados) + nada escrevia na tabela. Camada in-app consertada: `useNotifications` + `NotificationBell` (badge real, popover, marcar-lida) + `_shared/notify.ts` (writer service-role) + `publish-social` notifica no publish + 4 eventos reais semeados. Provado em browser: badge "5" + painel com 5 notificações. Camada **push** (browser/OS) segue sem infra.
> 27	
> 28	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (GOs via AskUserQuestion + diretivas) + verificação browser-real independente · Owner=Sovereign (carteira User 0 + blast radius IG/marca).
> 29	
> 30	| Verificação (material) | Resultado |
> 31	|---|---|
> 32	| Reel real publicado | ✅ `instagram.com/reel/DaBtVAQkiuz` (media_product_type=REELS, HTTP 200) |
> 33	| Notificações sino | ✅ browser: badge "5" + 5 eventos reais (screenshot) |
> 34	| Canvas white-screen | ✅ re-render provado (3 nós + criativos visíveis) |
> 35	| Asset handoff cross-módulo | ✅ asset → novo projeto Canvas com node (browser) |
> 36	| White-label HyperFrames | ✅ logo escondido (seletor browser-provado) + Sovereign confirmou |
> 37	| Starter MCORCH 9:16 | ✅ lint 0/0 · service active · carrega no editor |
> 38	| meli.la assinado + Family Hub | ✅ 2/3 produtos sale-attributable; TV indisponível desativada |
> 39	| tsc · gitleaks | ✅ 0 erros · limpo nos 9 commits |
> 40	| Handoff node | `468c15dc-ef07-406e-a417-501f08fbcf7a` (embedded 768d) |
> 41	
> 42	### Survival Laws Self-audit
> 43	```
> 44	Law 1 (Materiality): ✅ Tudo provado neste turno — Reel via HTTP 200 + permalink real; notificações via screenshot do browser; canvas/handoff/white-label via agent-browser; deploys por size; achados (cron /var/log morto, modelId fora do catálogo, id IG app-scoped 100/33) corrigidos com prova. Diretiva durável: verificar UI em browser real antes de declarar pronto.
> 45	Law 2 (Process): ✅ SOPs: meta-reels-publish.md (caminho IG Business Login que funciona). Fatia 2 = débito BoK FR-META-REELS registrado (override consciente "comece a Fatia 2 agora"). Notificações = consertar camada existente (não módulo novo). Canvas/scroll fixes isentos (single-file).
> 46	Law 3 (Pruning): ✅ Sessão longa com workflow (wf_792d5d48) como subagente; resultados por path, não recarregados. Selada a ~limite da janela.
> 47	Law 4 (ORO): ✅ Triplet declarado; decisões soberanas via AskUserQuestion (workspace init) + diretivas explícitas (P0, Fatia 2 GO).
> 48	```
> 49	
> 50	## Session Seal — HyperFrames editor LIVE + creative_assets spine (Fatia 1 bidirecional) + auth gating + Canvas bug fix (2026-06-25)
> 51	
> 52	Sessão longa multi-arco (`/handson` → editor HyperFrames → pedidos do Sovereign). **Quatro arcos entregues e provados:**
> 53	
> 54	**Arco 1 — Editor HyperFrames VIVO (Fatia VS-UI Fase A).** Descoberta material decisiva: o servidor oficial **`hyperframes preview`** (CLI unscoped `hyperframes@0.7.5`, NÃO `@hyperframes/cli` que não existe) **É** o editor NLE completo (StudioApp React 19 + Hono `/api`) — roda como **processo node standalone** → o conflito React 19/18 some **sem Docker**. Implantado como serviço host systemd `video-studio.service` (node v22 EXPLÍCITO — systemd pega `/usr/bin/node` v18 que quebra com `styleText`), projeto 9:16 semeado (`hyperframes init --example warm-grain --resolution portrait`), atrás do vhost `nginx/video.mcorch.com.conf` (SSO-gated, espelha design). Contrato `/api` (`StudioApiAdapter`) selado dos `.d.ts` publicados (Lei 2) — SDD §VS-UI Amendment v0.4 + SOP `video-studio-editor-deploy-and-provision.md`. Frontend `VideoStudioEditorPage` iframe `/dashboard/canvas/video` (rota ANTES de `canvas/:id`). **Sovereign executou os 2 sudo (cert + symlink+reload); provado E2E pela screenshot dele** (projeto 9:16 carregado, SSO redireciona em aba anônima). Render-parity resolvido por construção (`@hyperframes/core/runtime` IIFE compartilhado).
> 55	
> 56	**Arco 2 — Auth gating por `?devLogin`.** `/auth` público mostra só email/senha (Google/Apple/Cadastrar ocultos); `?devLogin` reaparece Google + aba Cadastrar (Apple removido). Gate client-side temporário/reversível (UX, não controle de auth — a auth real é server-side Supabase+RLS).
> 57	
> 58	**Arco 3 — Bug de perda de nós do Canvas FIXADO + projeto recuperado.** Race load/save: `useAutoSave` dava flush do estado vazio `{nodes:[]}` antes de `initialize()` hidratar → sobrescrevia o DB (assets sobrevivem em `vm_canvas_executions`). Fix single-file: guard no `useSaveCanvasGraph` que lê-antes-de-grava e BLOQUEIA sobrescrever grafo não-vazio com vazio. Projeto `63d406fe` reconstruído das execuções (3 nós + 1 aresta de linhagem; posições auto-layout, x/y originais perdidas).
> 59	
> 60	**Arco 4 — `creative_assets` SPINE (Fatia 1 do ecossistema criativo bidirecional).** Diretiva Sovereign "o poder das saídas": cada módulo usa assets um do outro, bidirecional. Tabela canônica fina que só APONTA pros buckets existentes (sem migrar bytes) + RPC `register_creative_asset` (SECURITY DEFINER service-role-only, idempotente, guard cross-tenant `WHERE user_id=EXCLUDED.user_id`). Dual-write fail-soft em 3 produtores (video-bridge/canvas-execute/generate-image) + backfill **73 assets reais** + UI **Biblioteca de Assets** (`/dashboard/canvas/assets`). **Lição de apply (registrada):** a Management API (`api.supabase.com`) bane UA `Python-urllib` com **erro 1010** → aplicar via **curl**.
> 61	
> 62	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (GOs via AskUserQuestion: arquitetura híbrida bidirecional + ordem das fatias + recuperar projeto) + `/security-review` independente (migration SAFE) · Owner=Sovereign (carteira User 0 + blast radius do registry per-tenant).
> 63	
> 64	| Verificação (material) | Resultado |
> 65	|---|---|
> 66	| Editor HyperFrames | ✅ `video-studio.service` active · curl :3210 → 200 · `/api/projects` 9:16 · screenshot Sovereign |
> 67	| vhost video.mcorch.com | ✅ cert+symlink+reload · origin 302 SSO provado · símbolo Sovereign |
> 68	| Canvas bug guard + recovery | ✅ guard tsc 0 deployado · `63d406fe` 3 nós/1 aresta verificado por re-read |
> 69	| `/security-review` creative_assets | ✅ SAFE (0 findings) |
> 70	| Smoke creative_assets | ✅ 5/5 (register · idempotência · anon→42501 · guard cross-tenant · cleanup) |
> 71	| Dual-write produtores | ✅ video-bridge restart · canvas-execute 151.6kB · generate-image 129.6kB deployados |
> ```

## 🤖 Claude *(00:22:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7985,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7985	ContentLibraryPage monetization flow:
> 7986	  Card (text, body contains mercadolivre.com.br)
> 7987	    └── DropdownMenu → "Monetizar Links ML"
> 7988	          → handleMonetizeLinks(item):
> 7989	               match(ML_URL_RE) → unique URLs
> 7990	               for url of unique:
> 7991	                 POST process-affiliate-link → affiliate_url
> 7992	                 body.split(url).join(affiliate_url)
> 7993	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7994	          → Badge 💰 ML (emerald) exibido após monetização
> 7995	```
> 7996	
> 7997	---
> 7998	
> 7999	## Pending Actions (Commercial Launch)
> 8000	
> 8001	### CRITICAL — Must complete before first client
> 8002	
> 8003	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8004	
> 8005	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8006	
> 8007	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8008	
> 8009	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8010	
> 8011	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8012	
> 8013	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8014	
> 8015	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8016	
> 8017	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8018	
> 8019	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8020	
> 8021	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8022	
> 8023	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8024	
> 8025	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8026	   ```bash
> 8027	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8028	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8029	   ```
> 8030	
> 8031	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8032	
> 8033	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8034	
> 8035	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8036	
> 8037	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8038	
> 8039	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8040	
> 8041	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8042	
> 8043	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8044	
> 8045	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8046	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8047	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8048	
> 8049	### SOCIAL — Next steps
> 8050	
> 8051	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8052	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8053	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8054	
> 8055	### NON-CRITICAL
> 8056	
> 8057	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8058	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8059	- `browserslist` — ✅ updated (2026-04-26)
> 8060	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8061	
> 8062	### GITNEXUS MCP — Next steps
> 8063	
> 8064	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8065	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8066	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8067	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8068	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8069	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8070	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8071	
> 8072	### PHASE EPSILON — Next iterations
> 8073	
> 8074	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8075	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8076	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8077	
> 8078	### CORE — Next iterations
> 8079	
> 8080	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8081	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8082	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8083	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8084	
> 8085	### PHASE DELTA — Next iterations
> 8086	
> 8087	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8088	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8089	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8090	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8091	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8092	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8093	
> 8094	### USUÁRIO ZERO — Checklist de validação
> 8095	
> 8096	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8097	- ✅ Stripe sandbox secrets no vault
> 8098	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8099	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8100	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8101	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8102	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8103	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8104	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8105	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8106	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8107	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8108	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8109	
> 8110	---
> 8111	
> 8112	## Infrastructure
> 8113	
> 8114	| Service | Container | Port | Status |
> 8115	|---------|-----------|------|--------|
> 8116	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8117	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8118	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8119	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8120	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8121	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8122	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8123	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8124	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8125	
> 8126	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8127	
> 8128	```bash
> 8129	docker compose up -d
> 8130	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8131	```
> 8132	
> 8133	---
> 8134	
> 8135	## Security Model (Post-Go-Live)
> 8136	
> 8137	| Table | Isolation |
> 8138	|-------|-----------|
> 8139	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8140	| `mcorch_edges` | Same pattern |
> 8141	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8142	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8143	
> 8144	---
> 8145	
> 8146	## Billing Architecture
> 8147	
> 8148	| Decision | Value |
> 8149	|----------|-------|
> 8150	| Canonical billing ledger | `profiles.mco_balance` |
> 8151	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8152	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8153	| Orchestration cost | 10 mcoCoins/run |
> 8154	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8155	| Stripe | Sandbox keys active — swap to live before first client |
> 8156	
> 8157	---
> 8158	
> 8159	## GraphRAG State
> 8160	
> 8161	- **8960 total nodes** (verificado live 2026-06-25 via REST count=exact, creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8162	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8163	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8164	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8165	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8166	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8167	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8168	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8169	- HNSW cosine index operational
> 8170	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8171	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8172	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8173	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8174	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8175	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8176	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8177	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8178	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8179	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8180	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8181	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8182	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8183	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8184	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8185	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8186	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8187	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8188	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8189	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8190	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8191	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8192	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8193	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8194	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8195	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8196	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8197	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8198	
> 8199	### Embedding Model
> 8200	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8201	Schema: `vector(768)` — HNSW cosine index.
> 8202	
> 8203	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8204	Três camadas eliminam intervenção manual:
> 8205	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8206	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8207	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8208	
> 8209	### Comandos de manutenção da Mesh
> 8210	```bash
> 8211	# Verificar nós sem embedding (deveria retornar array vazio):
> 8212	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8213	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8214	
> 8215	# Backfill manual (Bun-native — requer .env):
> 8216	bun run scripts/backfill-embeddings.ts
> 8217	
> 8218	# Backfill de código-fonte nos nós AST:
> 8219	bun run scripts/backfill-node-content.ts
> 8220	
> 8221	# Re-sync AST completo:
> 8222	cd packages/gitnexus-core && npm run sync-mesh
> 8223	
> 8224	# Acompanhar re-ingesta pós-commit:
> 8225	tail -f /tmp/mcorch-ingest.log
> 8226	```
> 8227	
> 8228	---
> 8229	
> 8230	## Video Rescue Protocol
> 8231	
> 8232	When a video generation operation (Google Veo) times out or client disconnects:
> 8233	```bash
> 8234	# Via edge function (production):
> 8235	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8236	  -H "Authorization: Bearer <user_jwt>" \
> 8237	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8238	
> 8239	# Via local script (admin/debug):
> 8240	source .env && bun run rescue.ts <operation_id> <content_id>
> 8241	```
> 8242	
> 8243	---
> 8244	
> 8245	## Architecture Pillars
> 8246	
> 8247	| Layer | Implementation |
> 8248	|-------|---------------|
> 8249	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8250	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8251	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8252	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8253	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8254	
> 8255	---
> 8256	
> 8257	## Phase Delta — Architecture
> 8258	
> 8259	```
> 8260	OrchestrationPage (full-canvas, p-0)
> 8261	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8262	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8263	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8264	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8265	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8266	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8267	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8268	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8269	
> 8270	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8271	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8272	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8273	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8274	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8275	```
> 8276	
> 8277	### Canvas State Architecture (Hybrid)
> 8278	
> 8279	```
> 8280	User interaction → ReactFlow internal state (positions, drag)
> 8281	                         ↓ (debounced 600ms)
> 8282	                   localStorage (positions persist across refresh)
> 8283	                         ↑
> 8284	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8285	     ↓ (status changes sync to ReactFlow via useEffect)
> 8286	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8287	```
> 8288	
> 8289	## Key Files
> 8290	
> 8291	| Purpose | Path |
> 8292	|---------|------|
> 8293	| Architecture rules | `CLAUDE.md` |
> 8294	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8295	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8296	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8297	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8298	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8299	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8300	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8301	| **Node types** | `src/components/orchestrator/nodes/` |
> 8302	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8303	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8304	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8305	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8306	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8307	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8308	| Billing utilities | `src/lib/billing.ts` |
> 8309	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8310	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8311	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8312	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8313	| Video rescue (local) | `rescue.ts` |
> 8314	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8315	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8316	| Deploy harness | `scripts/harness-deploy.sh` |
> 8317	
> 8318	---
> 8319	
> 8320	## First Client Onboarding Checklist
> 8321	
> 8322	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8323	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8324	3. ~~Activate watchdog cron~~ ✅ Done
> 8325	4. ~~Deploy rescue-video function~~ ✅ Done
> 8326	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8327	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8328	7. Monitor `infra_health_logs` for first 24h.
> 8329	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8330	
> 8331	---
> 8332	
> 8333	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8334	
> 8335	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8336	
> 8337	| Action | Result |
> 8338	|--------|--------|
> 8339	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8340	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8341	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8342	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8343	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8344	
> 8345	| Commit | Conteúdo |
> 8346	|--------|----------|
> 8347	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8348	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8349	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8350	
> 8351	### Arquitetura Matrix Intelligence
> 8352	
> 8353	```
> 8354	ConstellationMatrix (Stabilized Engine)
> 8355	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8356	  └── NodeDetailsPanel (Tabbed Navigation)
> 8357	        ├── Tab Meta: Neighbor exploration + Net Context
> 8358	        ├── Tab Code: Source code preview (Supabase sync)
> 8359	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8360	
> 8361	useNodeIntelligence Hook:
> 8362	  - contentQuery: fetch nodes.content column
> 8363	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8364	  - state: isAnalyzing, analysisResult, progress
> 8365	```
> 8366	
> 8367	---
> 8368	
> 8369	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8370	
> 8371	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8372	
> 8373	| Action | Result |
> 8374	|--------|--------|
> 8375	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8376	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8377	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8378	
> 8379	**Output da análise (estruturado em pt-BR):**
> 8380	- Visão Geral — papel do módulo no sistema
> 8381	- Padrões Detectados — design patterns, antipatterns
> 8382	- Acoplamento & Dependências — análise In/Out-Degree
> 8383	- Recomendações — 1-3 ações priorizadas
> 8384	
> ```

## 🤖 Claude *(00:22:46)*


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
> Output too large (51.8KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/3ee740c7-9900-4d37-a9a4-207b63e460bb/tool-results/bmfjnl1cw.txt
> 
> Preview (first 2KB):
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 25 21:14 ..
> ---sprint---
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.51.0 — Fatia 2 vídeo→Instagram Reel PROVADO E2E + Notificações P0 + malha criativa cross-módulo + receita destravada (2026-06-25)** — sessão-maratona "força total pelo primeiro R$", Usuário 00 sobre Usuário 0. **9 commits.** **(1) Receita** (`1ad04c5`): cron auto-publish morto (`/var/log` inacessível)→durável+telemetria; link **meli.la assinado** publicado (sale-attributable, Roborock+Family Hub); CTA-leak fechado; 2 posts injection removidos do LinkedIn. **(2) Canvas white-screen fix** (`46f18ca`): `MODEL_INFO[id].coinCost` em modelId fora do catálogo → `getImageModelInfo`/`getVideoModelInfo` com fallback; **verificação por browser real** (agent-browser+preview+sessão injetada) virou diretiva durável. **(3) Malha cross-módulo:** asset clicável→handoff Canvas (`8c00f88`); white-label HyperFrames nginx sub_filter (`5d58b15`); Biblioteca scroll+filtro-data+metadados (`8fdb435`); starter MCORCH 9:16 **lint 0/0** substitui demo HeyGen (`3efbe75`, AskUserQuestion). **(4) Fatia 2 — vídeo→Reel PROVADO E2E** (`9d9ec03`/`3be06ee`): User 0 **já conectado** (IG `magicorch` MEDIA_CREATOR); `publish-social` IG via `graph.instagram.com`+REELS+id do `/me` (stored id app-scoped rejeitava 100/33). **Reel real: `instagram.com/reel/DaBtVAQkiuz`.** **(5) P0 Notificações** (`bfb0ba3`): sino era placeholder morto (badge "3" hardcoded) + nada escrevia na tabela → `useNotifications`+`NotificationBell`+`_shared/notify.ts`+seed 4 eventos; browser badge "5". **Prova:** tsc 0 · gitleaks lim
> ...
> </persisted-output>
> ```

## 🤖 Claude *(00:22:52)*


## 🤖 Claude *(00:22:52)*

Let me run the BoK Gate completeness check and inspect the scratch/ contents (which appear numerous).

## 🤖 Claude *(00:22:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nfor slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK Gate completeness check"
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

## 🤖 Claude *(00:22:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"scratch file count: $(ls scratch/ 2>/dev/null | wc -l)\"; echo \"--- newest 12 ---\"; ls -t scratch/ 2>/dev/null | head -12; echo \"--- gitignored? ---\"; git check-ignore scratch/ 2>/dev/null && echo \"scratch IS gitignored\" || echo \"scratch NOT gitignored\"",
  "description": "Scratch summary + gitignore status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> scratch file count: 0
> --- newest 12 ---
> --- gitignored? ---
> scratch/
> scratch IS gitignored
> ```

## 🤖 Claude *(00:23:05)*


## 🤖 Claude *(00:23:06)*

Clean — scratch/ is empty (gitignored; earlier large output was a glitch). The `security` BoK uses the Cyber-Sentinel naming convention (deferred suite, not the standard 9 docs). Let me confirm sync with origin and grab the sprint's top gap.

## 🤖 Claude *(00:23:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; git fetch origin --quiet 2>&1; echo \"local vs origin/main:\"; git rev-list --left-right --count origin/main...HEAD 2>/dev/null; echo \"--- top gaps ---\"; grep -nA8 -i \"Top 3 Gap\" .claude/context/sprint-priorities.md 2>/dev/null | head -20",
  "description": "Fetch origin + sprint top gaps"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> local vs origin/main:
> 0	0
> --- top gaps ---
> ```

## 🤖 Claude *(00:23:25)*


## 🤖 Claude *(00:23:47)*

═══════════════════════════════════════════════════════════
  **HANDSON — v6.51.0** · selada em 2026-06-25
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
Fase selada: **Fatia 2 vídeo→Instagram Reel PROVADO E2E + Notificações P0 + malha criativa cross-módulo + receita destravada** — sessão-maratona "força total pelo primeiro R$", operando como Usuário 00 sobre o Usuário 0. 9 commits, tudo provado materialmente.
```
09a4203 chore(sprint): v6.51.0 — Fatia 2 Reel E2E + notificações P0 + malha cross-módulo + receita
bfbf2c5 docs(handoff): seal Fatia 2 Reel E2E + notificações P0 + ...
bfb0ba3 fix(notifications): sino real (P0 — notificações nunca funcionaram)
3be06ee fix(meta): Reel real publica pela conexão IG existente (Fatia 2 E2E provada)
9d9ec03 feat(meta): Fatia 2 — publicar vídeo do ecossistema como Reel (IG + FB)
```

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ · sincronizado com `origin/main` (0↔0) · `scratch/` vazio.

🏗️ **INFRA**
`mcorch_chroma` ✅ healthy (10d) — Chroma API v2 OK (heartbeat respondeu) · `mcorch_claude_mem` ✅ healthy · `mcorch_vision_mcp` ✅ healthy (8d) · `mega-brain-daemon`/`-webhook`/`-dashboard` ✅ up.

🧠 **KNOWLEDGE MESH**
**8960 nós** · ~**9070 arestas** (fonte: GraphRAG State, verificado live 2026-06-25). Último handoff node: `8eb84bce…` (creative_assets spine + editor HyperFrames). 100% embedded (768d HNSW cosine).

🔧 **TYPESCRIPT**
Zero erros ✅ (`tsc --noEmit` limpo).

📚 **BoK SUITES**
21 suítes completas (9/9 docs cada) — incl. `viral-autopilot`, `video-studio`, `vision-mcp`, `marketing-hub`, `meta-api`.
`security` → incompleta **por design** (suíte Cyber-Sentinel, naming próprio `00-blueprint`/`01-brd-security`/… e **deferida** por diretiva). Não bloqueia o trabalho atual; só relevante se a sessão tocar hardening de segurança.

📌 **SPRINT**
Goal: *Distribuição social autônoma operacional — pipeline publica LinkedIn auto, Twitter ao subir tier, Instagram pós App Review.* O Reel real (`instagram.com/reel/DaBtVAQkiuz`) já provou a saída IG E2E.

⚡ **PRÓXIMOS PASSOS** (prioridade — herdados da sessão de receita + ecossistema criativo)
1. **Trilha Sovereign do loop de receita** (do reparo `1ad04c5`, gated em ação Sovereign): **(A)** ativar `pg_cron` + `is_active` do auto-publish/autopilot; **(B)** limpar CF público em `www.mcorch.com`; **(C)** gerar os links assinados meli.la dos outros 2 produtos (exige IP residencial). É o caminho mais curto para o **primeiro R$ atribuível**.
2. **Viral Autopilot — vídeo autônomo:** 1º ciclo PAGO de vídeo *witnessed* (habilitar `video_enabled` + GO) + **postback ML real** (OTD-VA-007). Motor 9:16 e cadência já vivos.
3. **Editor HyperFrames Studio (módulo-container, VS-UI):** blueprint material pronto (`.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`); falta `studio.mcorch.com` (DNS Sovereign) + bridge `McorchAdapter.startRender`. Alinha com a diretiva "entregar valor visível, menos plumbing".

⚠️ **ALERTAS**
Nenhum alerta crítico ✅ — TS limpo, containers saudáveis, worktree limpo, scratch limpo, em sync com origin.
⚠️ Lembrete do CLAUDE.md: módulo novo/feature complexa → **BoK Gate** (rodar `/bok-scribe` antes de código). E **verificar UI em browser real** antes de declarar pronto (diretiva durável da última sessão).

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

Qual frente quer puxar — destravar a receita (trilha Sovereign A/B/C), o ciclo pago de vídeo do Autopilot, ou o editor HyperFrames Studio?

## 👤 User *(00:27:40)*

ótimo vamos aos próximos passos faça tudo inclusive o passo de E2E UI em Browser real antes de declarar pronto.

## 🤖 Claude *(00:28:51)*


## 🤖 Claude *(00:28:56)*

O Sovereign deu GO. Antes de executar às cegas, preciso saber materialmente o estado real de cada frente — porque vários itens dos "próximos passos" estão fisicamente travados na ação Sovereign (DNS, Cloudflare, IP residencial) ou gastam dinheiro real (ciclo pago de vídeo), e o HANDOFF pode estar parcialmente stale. Vou fazer recon material paralelo das 3 frentes primeiro (Lei 1), depois executo tudo que for genuinamente executável e provo por browser real, surfando honestamente o que estiver gated.

Como ultracode está ON, vou usar um workflow para o recon paralelo.

## 🤖 Claude *(00:28:56)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Recon material das 3 frentes",
  "summary": "Probe live: receita (cron/pg_cron/links), ciclo pago v\u00eddeo Autopilot, editor HyperFrames Studio \u2014 antes de executar"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Recon material das 3 frentes". Continue your current work.'}]
> ```

## 🤖 Claude *(00:28:59)*


## 🤖 Claude *(00:30:00)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'next-steps-recon',\n  description: 'Recon material paralelo das 3 frentes (receita / v\u00eddeo Autopilot / editor HyperFrames) antes de executar',\n  phases: [{ title: 'Recon', detail: '3 agentes read-only sondam estado live' }],\n}\n\nconst FINDING_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['frontier', 'liveState', 'executableNow', 'sovereignGated', 'recommendation'],\n  properties: {\n    frontier: { type: 'string' },\n    liveState: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['item', 'status', 'proof'],\n        properties: {\n          item: { type: 'string' },\n          status: { type: 'string', enum: ['done', 'live', 'partial', 'broken', 'absent', 'unknown'] },\n          proof: { type: 'string', description: 'Material evidence: command output, HTTP status, row count, file size, docker status. NEVER fabricate.' },\n        },\n      },\n    },\n    executableNow: {\n      type: 'array',\n      description: 'Actions the AI agent can perform from this datacenter WITHOUT Sovereign hands (no DNS/CF dashboard/residential-IP/real-money).',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['action', 'how', 'reversible', 'spendsMoney'],\n        properties: {\n          action: { type: 'string' },\n          how: { type: 'string', description: 'Exact commands/files/edits' },\n          reversible: { type: 'boolean' },\n          spendsMoney: { type: 'boolean', description: 'Spends real mcoCoins from User 0 wallet or publishes to live external service' },\n        },\n      },\n    },\n    sovereignGated: {\n      type: 'array',\n      description: 'Items physically impossible from datacenter or requiring Sovereign-only access.',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['item', 'why', 'whatNeeded'],\n        properties: {\n          item: { type: 'string' },\n          why: { type: 'string' },\n          whatNeeded: { type: 'string' },\n        },\n      },\n    },\n    recommendation: { type: 'string', description: 'One-paragraph executive recommendation in PT-BR on what to execute now vs surface.' },\n  },\n}\n\nphase('Recon')\n\nconst REPO = '/home/gcrUX/htdocs/constellation-orchestra'\nconst SUPA = 'https://bcyvddsykvehvpwstlfa.supabase.co'\n\nconst common = `Voc\u00ea \u00e9 um agente de RECON READ-ONLY do MCORCH. Workspace: ${REPO}.\nREGRAS DE FERRO (Survival Law 1 \u2014 Materialidade):\n- N\u00c3O mute NADA: zero git commit, zero edit de arquivo, zero INSERT/UPDATE/DELETE, zero deploy, zero gasto de mcoCoins. S\u00f3 LEITURA e diagn\u00f3stico.\n- Toda claim carrega prova material: output literal de comando, HTTP status+body, contagem de linha real, size de arquivo, 'docker ps' status. NUNCA fabrique UUID/hash/contagem.\n- Se faltar acesso (sem credencial, sem shell, query falha), declare \"C\u00e9rebro sem m\u00e3os\" no campo proof \u2014 n\u00e3o invente.\n- Credenciais: rode 'source ${REPO}/.env' antes de curl. Supabase REST: ${SUPA}/rest/v1/<tabela> com headers 'apikey: \\$SB_SECRET_KEY' e 'Authorization: Bearer \\$SB_SECRET_KEY'. As chaves legadas SUPABASE_SERVICE_ROLE_KEY/ANON est\u00e3o MORTAS \u2014 use SB_SECRET_KEY.\n- Para SQL fora de REST (ex: cron.job do pg_cron, RLS, RPC), procure um caminho funcional (scripts/qa helpers, aios-sql-bridge, ou RPC existente). Se nenhum funcionar, reporte unknown + \"C\u00e9rebro sem m\u00e3os\".\n- Distinga claramente: o que J\u00c1 est\u00e1 done/live \u00b7 o que EU (datacenter) posso executar agora sem m\u00e3os Sovereign \u00b7 o que \u00e9 fisicamente Sovereign-gated (DNS, dashboard Cloudflare, IP residencial p/ portal ML, GO de gasto real).\nRetorne SOMENTE o objeto estruturado.`\n\nconst [revenue, video, studio] = await parallel([\n  () => agent(`${common}\n\nFRENTE: REPARO DO LOOP DE RECEITA (Trilha Sovereign A/B/C).\nContexto (pode estar stale \u2014 VERIFIQUE tudo live): commit 1ad04c5 consertou o cron auto-publish (estava morto por redirect /var/log inacess\u00edvel) \u2192 path dur\u00e1vel + telemetria infra_health_logs; buildMlProductUrl passou a publicar o link meli.la ASSINADO (sale-attributable); login.mcorch.com/go estava CF-morto \u2192 unset AFFILIATE_REDIRECT_BASE. Trilha pendente: (A) ativar pg_cron + flag is_active; (B) limpar CF p\u00fablico www.mcorch.com; (C) links assinados meli.la dos outros 2 produtos (exige IP residencial no portal ML).\n\nSONDE materialmente:\n1. Crontab atual (ubuntu e gcrUX): 'crontab -l' \u2014 auto-publish-cron.sh e watchdog ainda agendados? Aponta pra path v\u00e1lido? H\u00e1 log recente? ('ls -la' + tail do log que o script usa).\n2. scripts/auto-publish-cron.sh \u2014 leia: o redirect est\u00e1 dur\u00e1vel agora? qual log path?\n3. pg_cron: existe job ativo chamando autopilot-cadence-cron e/ou auto-publish? Tente cron.job via algum caminho SQL. Reporte jobid/schedule/active ou unknown.\n4. affiliate_links via REST: quantos links existem? quantos com affiliate_url meli.la assinado? quantos revenue_cents>0? (use select + count). content_id NULL vs preenchido.\n5. autopilot_plans via REST: existe plano do User 0? is_active? video_enabled? Qual user_id.\n6. CF p\u00fablico: 'curl -sI https://www.mcorch.com' e 'curl -sI https://login.mcorch.com/go' \u2014 o que retorna (challenge CF? 200? 530?).\n7. AFFILIATE_REDIRECT_BASE: est\u00e1 no .env? setado ou unset? (grep .env, N\u00c3O imprima segredos \u2014 s\u00f3 presen\u00e7a/valor da var de redirect que n\u00e3o \u00e9 segredo).\n\nDetermine: o que de A/B/C eu consigo executar AGORA do datacenter (prov\u00e1vel: ativar is_active/pg_cron via SQL se houver caminho de escrita \u2014 MAS recon \u00e9 read-only, s\u00f3 DIGA se \u00e9 execut\u00e1vel e como), e o que \u00e9 hard-gated (B precisa dashboard CF; C precisa IP residencial \u2014 confirme se o datacenter realmente \u00e9 barrado).`,\n    { label: 'recon:receita', phase: 'Recon', schema: FINDING_SCHEMA }),\n\n  () => agent(`${common}\n\nFRENTE: VIRAL AUTOPILOT \u2014 1\u00ba CICLO PAGO DE V\u00cdDEO 9:16 WITNESSED + POSTBACK ML.\nContexto (verifique live): motor HyperFrames determin\u00edstico vivo (video-bridge.service render 1080\u00d71920 sha256-id\u00eantico, bucket video-studio-assets); orchestrate-step enfileira render do \u00e2ngulo viral REAL com custo no pr\u00e9-d\u00e9bito do ciclo (OTD-VA-010, cr\u00e9dito compensat\u00f3rio refund_autopilot_video_enqueue migration 20260624140000); attach content_library+creative_metrics. Pendente: habilitar video_enabled + GO p/ 1\u00ba ciclo PAGO real + postback ML (OTD-VA-007).\n\nSONDE materialmente:\n1. video-bridge.service: 'systemctl --user status video-bridge.service' (ou system). active? Desde quando?\n2. video_renders via REST: existe a tabela? quantas linhas? engine=hyperframes? status distribution (queued/running/done/failed)? Alguma do User 0?\n3. Bucket video-studio-assets: existe? via storage API liste objetos (qualquer .mp4 real, size).\n4. autopilot edge fns: autopilot-run, autopilot-cadence-cron, orchestrate-step, orchestrate-content est\u00e3o deployadas? (npx supabase functions list, OU verifique no diret\u00f3rio supabase/functions/). N\u00c3O deploy.\n5. Saldo do User 0: profiles.mco_balance via REST (qual user_id, qual saldo atual).\n6. Custo de um ciclo: leia o pr\u00e9-d\u00e9bito no c\u00f3digo (begin_autopilot_cycle / orchestrate-content ORCH_COST / cost do enqueue de v\u00eddeo) \u2014 quanto custa 1 ciclo COM v\u00eddeo? Some os componentes (texto+imagem+v\u00eddeo).\n7. Providers de imagem do User 0: o HANDOFF dizia que estavam quebrados (nanobana mock / openai erro) mas depois 'generate-image roteia por OpenRouter Gemini'. Verifique user_api_keys (decrypted view N\u00c3O acess\u00edvel por REST normal \u2014 reporte o que der). O ciclo pago realmente produziria m\u00eddia ou falha?\n8. video_enabled: onde mora a flag (autopilot_plans.video_enabled?) e est\u00e1 true/false p/ User 0?\n9. Postback ML (OTD-VA-007): handle-ml-postback deployada? H\u00e1 algum revenue_cents>0 real? O que falta pra postback real.\n\nDetermine: rodar 1 ciclo pago de v\u00eddeo \u00e9 (a) tecnicamente pronto E2E?, (b) custo exato em mcoCoins, (c) gasta dinheiro real do User 0 (sim) \u2192 portanto requer GO expl\u00edcito do Sovereign. Liste o comando/edge-fn exato pra disparar 1 ciclo e o que observar como prova.`,\n    { label: 'recon:video', phase: 'Recon', schema: FINDING_SCHEMA }),\n\n  () => agent(`${common}\n\nFRENTE: EDITOR HYPERFRAMES STUDIO (Fatia VS-UI \u2014 m\u00f3dulo-container).\nContexto (verifique live): Fase A LIVE \u2014 servidor oficial 'hyperframes preview' roda como systemd video-studio.service (node v22, loopback 127.0.0.1:3210), projeto 9:16 semeado, atr\u00e1s do vhost nginx/video.mcorch.com.conf (SSO-gated, espelha design.mcorch.com); frontend VideoStudioEditorPage iframe em /dashboard/canvas/video. Pendente Fase B: bridge McorchAdapter.startRender\u2192video-render + vhost studio.mcorch.com (DNS Sovereign). Blueprint: .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md.\n\nSONDE materialmente:\n1. video-studio.service: 'systemctl --user status video-studio.service'. active? 'curl -sI http://127.0.0.1:3210' \u2192 200? '/api/projects' retorna o projeto 9:16?\n2. nginx/video.mcorch.com.conf existe? 'curl -sI https://video.mcorch.com' \u2192 SSO redirect (302)? cert ok?\n3. Rota /dashboard/canvas/video: existe VideoStudioEditorPage.tsx? est\u00e1 ANTES de canvas/:id no App.tsx? leia o componente (iframe src).\n4. studio.mcorch.com: DNS resolve? 'curl -sI https://studio.mcorch.com'. vhost existe?\n5. McorchAdapter / StudioApiAdapter: existe algum arquivo de bridge no repo (grep McorchAdapter, StudioApiAdapter)? Fase B (startRender\u2192video-render) est\u00e1 implementada ou \u00e9 s\u00f3 blueprint?\n6. Leia o blueprint .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md \u2014 qual \u00e9 exatamente o gate #1 (render-parity) e o seam, e o que \u00e9 necess\u00e1rio p/ Fase B.\n7. White-label: o sub_filter nginx que esconde o logo HeyGen est\u00e1 ativo? (grep no .conf).\n\nDetermine: qual parte do editor j\u00e1 est\u00e1 VIVA e VERIFIC\u00c1VEL por browser real (prov\u00e1vel: /dashboard/canvas/video via video.mcorch.com com SSO), o que \u00e9 Fase B execut\u00e1vel por mim (bridge code), e o que \u00e9 Sovereign-gated (studio.mcorch.com DNS+cert). D\u00ea a URL/rota exata pra E2E browser e o que esperar ver.`,\n    { label: 'recon:studio', phase: 'Recon', schema: FINDING_SCHEMA }),\n])\n\nreturn { revenue, video, studio }",
  "description": "Recon material 3 frentes"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wd20a5wcm
> Summary: Recon material paralelo das 3 frentes (receita / vídeo Autopilot / editor HyperFrames) antes de executar
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/3ee740c7-9900-4d37-a9a4-207b63e460bb/subagents/workflows/wf_6475e2f8-44d
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/3ee740c7-9900-4d37-a9a4-207b63e460bb/workflows/scripts/next-steps-recon-wf_6475e2f8-44d.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/3ee740c7-9900-4d37-a9a4-207b63e460bb/workflows/scripts/next-steps-recon-wf_6475e2f8-44d.js"} to iterate without resending the script.)
> Run ID: wf_6475e2f8-44d
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/3ee740c7-9900-4d37-a9a4-207b63e460bb/workflows/scripts/next-steps-recon-wf_6475e2f8-44d.js", resumeFromRunId: "wf_6475e2f8-44d"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(00:30:07)*


## 🤖 Claude *(00:30:12)*

Lancei o recon material em background (workflow `wf_6475e2f8-44d`, 3 agentes read-only em paralelo). Eles sondam o estado **live** de cada frente — sem mutar nada — para eu saber exatamente o que é executável daqui do datacenter vs. o que está fisicamente travado na sua ação (DNS, Cloudflare, IP residencial) ou gasta mcoCoins reais:

- **Receita** — cron auto-publish, pg_cron, links meli.la assinados, estado do CF público, `AFFILIATE_REDIRECT_BASE`.
- **Vídeo Autopilot** — `video-bridge.service`, `video_renders`, saldo do User 0, custo exato de 1 ciclo pago, se os providers de imagem realmente produzem mídia.
- **Editor HyperFrames** — `video-studio.service`, vhost `video.mcorch.com`, rota `/dashboard/canvas/video`, estado da Fase B (bridge) vs. blueprint.

Aguardo a conclusão (serei reinvocado automaticamente) e então executo tudo que for executável, com prova material + **verificação E2E em browser real** antes de declarar pronto. O que estiver gated na sua mão eu surfarei explicitamente.

# Vamos em frente com o projeto
**Date:** 2026-06-30 | **Session ID:** `8774b91e-56ce-422f-aa7a-2a61eaf326df`

---

## 👤 User *(04:48:52)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(04:48:52)*

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
  if [ "$slug" = "security" ]; then
    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)
    missing=()
    for doc in "${required_sec[@]}"; do
      [ -f "docs/bok/security/$doc.md" ] || missing+=("$doc")
    done
    [ ${#missing[@]} -eq 0 ] && echo "✅ security — BoK complete (ciso-4-artifact)" || echo "⚠️ security — missing: ${missing[*]}"
    continue
  fi
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


## 🤖 Claude *(04:48:56)*


## 🤖 Claude *(04:48:57)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with the pre-flight checks in parallel.

## 🤖 Claude *(04:48:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7",
  "description": "Recent git history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9d04641 docs(handoff): seal Gabriel AI program — BoK avatar-clone-ai + Fatia 1 BYOK + Spaces P0 + Kanban live
> 71f4c47 docs(readme): v6.60.0 — Gabriel AI BoK+Fatia1 + Spaces P0 + Kanban live — mesh 8993
> 7b05945 feat(kanban): non-destructive roadmap reconciler + cron (live board)
> ce28265 feat(kanban): card detail dialog with manual actions
> 3f36d27 feat(spaces): Phase 0 — promote Spaces canvas scaffold + BoK suite
> 50dc6bb feat(avatar-clone-ai): Fatia 1 — BYOK avatar per-user (hedra/cartesia/fal) + Settings UI
> a5814d2 docs(bok): avatar-clone-ai suite — deepsearch + Fatia 0 GO-HYBRID + BoK 10/10 sealed
> ```

## 🤖 Claude *(04:48:58)*


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

## 🤖 Claude *(04:48:59)*


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

## 🤖 Claude *(04:49:00)*


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

## 🤖 Claude *(04:49:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---chroma---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat",
  "description": "Docker mesh + Chroma health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 11 hours (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> ---
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> ---chroma---
> {"nanosecond heartbeat":1782794941571501254}
> ```

## 🤖 Claude *(04:49:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---handoff-lines---\"; wc -l HANDOFF.md; echo \"---scratch---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"",
  "description": "BoK suites + HANDOFF size + scratch"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> agentic-governance
> agentic-workspace
> aios-sql-bridge
> authenticated-browser-operator
> avatar-clone-ai
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
> spaces-evolution
> video-studio
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> ---handoff-lines---
> 8792 HANDOFF.md
> ---scratch---
> ⚠️ scratch/ has files
> ```

## 🤖 Claude *(04:49:07)*


## 🤖 Claude *(04:49:07)*

Now reading the key context files (HANDOFF head + tail using read-from-end strategy) and checking scratch.

## 🤖 Claude *(04:49:08)*


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
> 14	## Session Seal — Programa "Gabriel AI": BoK avatar-clone-ai + Fatia 1 BYOK + Spaces Phase 0 + Kanban vivo (2026-06-30)
> 15	
> 16	Sessão-maratona iniciada por `/handson`, sob **ultracode** (orquestração via Workflow). Da diretiva Sovereign "criar estratégias de conteúdo + cadência 30d + avatar treinado fiel à minha pessoa/voz" até **código verificado em produção**, mais duas tarefas encadeadas (Spaces Phase 0 + Kanban detalhado/vivo).
> 17	
> 18	**Arco 1 — Programa "Gabriel AI" (módulo per-user `avatar-clone-ai`):**
> 19	- **Deepsearch força-total** (14 frentes web+codebase + verificação adversarial — 6 claims refutadas: HeyGen-BYOK, ElevenLabs PVC+v3, F5-TTS license, Identity-Gate numbers, CONAR-AI-label, reshaper-já-publica) → `00-deepsearch-blueprint.md`.
> 20	- **Gate Fatia 0 = GO-HYBRID** (probe de viabilidade: NÃO 100%-avatar — crater Julia McCoy 30k→3k subs/mês, FM-AC-014 — mas híbrido rosto-real + avatar-backfill **declarado** cresce; baseline real via curl: YT @uxnai 49 subs/32 vídeos · TikTok @gabriel_mcorch 0 vídeos público) → `00b`. F1-F7 fechado (BYOK por provider Modelo A; auto-dub=alcance vs voz-clonada=premium [F3 refutado]; economics datado Hedra ~$35/ciclo; LGPD+EU AI Act; gating por canal) → `00c`.
> 21	- Decisões Sovereign travadas: híbrido · **global-EN-first** (áudio EN-âncora + auto-dub PT) · BYOK puro per-user (Hedra default / OmniHuman / Higgsfield; Magnific=conta-org / HeyGen=partnership FORA) · reply X core · idioma/freq opt-in.
> 22	- **BoK 10/10 selada** via Scribe orquestrado (com recovery após session-limit via `resumeFromRunId`) → nó `ee81987d` (embedded, DERIVES_FROM video-studio).
> 23	- **Fatia 1** construída: BYOK avatar (migration `20260630000000` hedra/cartesia/fal espelhando o maquinário Vault verbatim) + Settings UI; round-trip de cifragem provado E2E; browser-verified.
> 24	
> 25	**Arco 2 — Spaces canvas Phase 0:** promovido o scaffold tsc-clean (`spaces-evolution`) p/ `src/lib`+`src/store`+`src/hooks` (guards z.object `SpaceEdgeData`/`SpaceEntity` + `buildPorts` derivando `NODE_PORTS`), imports `@/lib/*`. Gate verde (tsc 0 · lint · 295 testes); legado intacto.
> 26	
> 27	**Arco 3 — Kanban de Inteligência vivo:** (1) clicar num card abre **painel de detalhe** (edit/move/**delegar-ao-agente-no-Chat**/excluir; `updateTask`/`deleteTask` net-new). (2) **Reconciliador não-destrutivo + cron `*/15`** (migration `20260630010000` `source`/`external_key`; status derivado de sinais reais; **G1 manual-sobrevive + G2 sem-dup provados**; SOP Lei 2). Anti-corpo do board mockado que mostrava `RUNNING` falso.
> 28	
> 29	| Action | Result |
> 30	|--------|--------|
> 31	| `docs/bok/avatar-clone-ai/` (13 docs) | ✅ blueprint + 00b/00c Fatia 0 + suíte BoK 10/10 (3117 linhas) |
> 32	| `supabase/migrations/20260630000000_user_api_keys_avatar_byok.sql` | ✅ BYOK hedra/cartesia/fal Vault-cifrado (aplicada + round-trip provado) |
> 33	| `src/pages/SettingsPage.tsx` + `src/integrations/supabase/types.ts` | ✅ 3 campos avatar BYOK (browser-verified) + types regen |
> 34	| `src/lib/{spaces-schema,port-compat,node-registry}` + `src/store/useSpacesStore` + `src/hooks/useParamRegistry` | ✅ Spaces Phase 0 (tsc/lint/295 verde) |
> 35	| `src/components/kanban/CardDetailDialog.tsx` + `src/pages/KanbanPage.tsx` + `src/hooks/useAiosKanban.ts` | ✅ painel de detalhe + ações manuais + delegar-ao-agente |
> 36	| `supabase/migrations/20260630010000_*.sql` + `scripts/reconcile-kanban-roadmap.ts` + SOP | ✅ reconciliador vivo não-destrutivo + cron */15 (G1/G2 provados) |
> 37	| `tsc --noEmit` / `bun run test` / `/security-review` ×3 | ✅ 0 erros · 295 passed · NO FINDINGS |
> 38	
> 39	| Commit | Conteúdo |
> 40	|--------|----------|
> 41	| `a5814d2` | docs(bok): avatar-clone-ai suite — deepsearch + Fatia 0 GO-HYBRID + BoK 10/10 |
> 42	| `50dc6bb` | feat(avatar-clone-ai): Fatia 1 — BYOK avatar per-user + Settings UI |
> 43	| `3f36d27` | feat(spaces): Phase 0 — promote Spaces canvas scaffold + BoK |
> 44	| `ce28265` | feat(kanban): card detail dialog with manual actions |
> 45	| `7b05945` | feat(kanban): non-destructive roadmap reconciler + cron (live board) |
> 46	| `71f4c47` | docs(readme): v6.60.0 — mesh 8993 |
> 47	
> 48	Handoff node `aba1458e-2df1-4813-a71b-34360bf7417e` inserido + auto-embedado (768d, trigger pg_net). BoK seal `ee81987d` + DERIVES_FROM edge `faff13ab` → video-studio (`c99b7875`). Mesh **8993 nós**.
> 49	
> 50	---
> 51	
> 52	## Session Seal — Minerador de Produtos: Reparo de Confiabilidade do Vision MCP + Extração Assíncrona Timeout-Proof (2026-06-29)
> 53	
> 54	Continuação do QA que estava com o Antigravity. A extração ao vivo do TikTok voltava `non-2xx` ("Extração ao vivo falhou, usando dados do cache"). Como sênior, verifiquei materialmente (Lei 1) e achei que **não era só tamanho** — diagnostiquei 3 causas-raiz e endureci o pipeline inteiro de ponta a ponta, fechando com a diretiva Sovereign de **assincronização timeout-proof** (tempo/tamanho de vídeo viral nunca podem ser gargalo do Vision MCP).
> 55	
> 56	**Arcos entregues:**
> 57	- **Tamanho de vídeo** — Vision MCP `analyze_video` agora sobe vídeos **20–100MB via Gemini Files API** (resumable upload → poll ACTIVE → `fileData.fileUri`); ≤20MB segue inline rápido. Provado: MP4 30MB → análise real, log `tool_ok`.
> 58	- **`directVideoUrl` frágil (stub 5KB)** — voltei pro `shouldDownloadVideos:true` (URL Apify público estável `api.apify.com/.../video-*.mp4`) → **análise de VÍDEO rica em TODO vídeo** (não a capa fina), com **retry antes de degradar** + fallback cover-image como rede de segurança (MCP rejeita `<50KB` `video_too_small`).
> 59	- **Síntese** — `:free` do OpenRouter (429 do pool compartilhado que ignora BYOK) cai automaticamente pro **irmão pago BYOK**; parser JSON tolerante (quoted **e** unquoted, sobrevive a aspas não-escapadas/truncamento); **seleção de produto por fit de audiência** (vídeo sem produto → infere o que a audiência compraria, não o objeto incidental) + **badge de confiança** honesto.
> 60	- **Extração ASSÍNCRONA timeout-proof** — `vm_miner_jobs` (RLS owner-scoped, writes service-role = tamper-proof, na publicação `supabase_realtime` + replica identity) + action `mine-async` (retorna `job_id` em ~2.4s, roda extract→vision num `EdgeRuntime.waitUntil` em background) + hook `useMinerJob` (Realtime + polling de fallback) → **barra de progresso (estágio + % + ETA)** + **notificação no sino** quando volta.
> 61	- **Hardening de brinde** — fechado o bloqueante de tenancy (`Deno.env.get("APIFY_TOKENS")` global removido → per-user fail-closed) + guard SSRF no edge.
> 62	
> 63	| Action | Result |
> 64	|--------|--------|
> 65	| `packages/vision-mcp-core/src/tools/analyze-video.ts` | ✅ Gemini Files API p/ 20–100MB + `MIN_VIDEO_BYTES` rejeita stub <50KB (FR-VM-024); container `mcorch_vision_mcp` rebuildado/healthy |
> 66	| `supabase/functions/discover-products/index.ts` | ✅ `shouldDownloadVideos:true` + `coverUrl` + vision-analyze com retry+cover fallback + tenancy per-user + SSRF guard + action `mine-async` (background `EdgeRuntime.waitUntil`) |
> 67	| `supabase/functions/openrouter-swarm/index.ts` | ✅ `:free` 429 → retry irmão pago BYOK + `max_tokens` 1024 |
> 68	| `supabase/migrations/20260629170000_vm_miner_jobs.sql` | ✅ tabela job RLS owner + publicação realtime + replica identity (aplicada via Management API) |
> 69	| `src/hooks/useMinerJob.ts` | ✅ kick + Realtime + polling 3s fallback |
> 70	| `src/pages/AffiliateProductsPage.tsx` | ✅ barra de progresso async + cover_url + síntese por fit de audiência + badge de confiança + parser robusto |
> 71	| `tsc --noEmit` / `bun run test` | ✅ 0 erros · 295 passed |
> ```

## 🤖 Claude *(04:49:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8392,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8392	  Card (text, body contains mercadolivre.com.br)
> 8393	    └── DropdownMenu → "Monetizar Links ML"
> 8394	          → handleMonetizeLinks(item):
> 8395	               match(ML_URL_RE) → unique URLs
> 8396	               for url of unique:
> 8397	                 POST process-affiliate-link → affiliate_url
> 8398	                 body.split(url).join(affiliate_url)
> 8399	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8400	          → Badge 💰 ML (emerald) exibido após monetização
> 8401	```
> 8402	
> 8403	---
> 8404	
> 8405	## Pending Actions (Commercial Launch)
> 8406	
> 8407	### CRITICAL — Must complete before first client
> 8408	
> 8409	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8410	
> 8411	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8412	
> 8413	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8414	
> 8415	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8416	
> 8417	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8418	
> 8419	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8420	
> 8421	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8422	
> 8423	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8424	
> 8425	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8426	
> 8427	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8428	
> 8429	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8430	
> 8431	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8432	   ```bash
> 8433	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8434	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8435	   ```
> 8436	
> 8437	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8438	
> 8439	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8440	
> 8441	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8442	
> 8443	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8444	
> 8445	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8446	
> 8447	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8448	
> 8449	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8450	
> 8451	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8452	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8453	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8454	
> 8455	### SOCIAL — Next steps
> 8456	
> 8457	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8458	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8459	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8460	
> 8461	### NON-CRITICAL
> 8462	
> 8463	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8464	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8465	- `browserslist` — ✅ updated (2026-04-26)
> 8466	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8467	
> 8468	### GITNEXUS MCP — Next steps
> 8469	
> 8470	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8471	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8472	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8473	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8474	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8475	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8476	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8477	
> 8478	### PHASE EPSILON — Next iterations
> 8479	
> 8480	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8481	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8482	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8483	
> 8484	### CORE — Next iterations
> 8485	
> 8486	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8487	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8488	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8489	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8490	
> 8491	### PHASE DELTA — Next iterations
> 8492	
> 8493	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8494	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8495	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8496	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8497	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8498	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8499	
> 8500	### USUÁRIO ZERO — Checklist de validação
> 8501	
> 8502	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8503	- ✅ Stripe sandbox secrets no vault
> 8504	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8505	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8506	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8507	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8508	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8509	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8510	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8511	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8512	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8513	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8514	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8515	
> 8516	---
> 8517	
> 8518	## Infrastructure
> 8519	
> 8520	| Service | Container | Port | Status |
> 8521	|---------|-----------|------|--------|
> 8522	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8523	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8524	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8525	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8526	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8527	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8528	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8529	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8530	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8531	
> 8532	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8533	
> 8534	```bash
> 8535	docker compose up -d
> 8536	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8537	```
> 8538	
> 8539	---
> 8540	
> 8541	## Security Model (Post-Go-Live)
> 8542	
> 8543	| Table | Isolation |
> 8544	|-------|-----------|
> 8545	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8546	| `mcorch_edges` | Same pattern |
> 8547	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8548	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8549	
> 8550	---
> 8551	
> 8552	## Billing Architecture
> 8553	
> 8554	| Decision | Value |
> 8555	|----------|-------|
> 8556	| Canonical billing ledger | `profiles.mco_balance` |
> 8557	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8558	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8559	| Orchestration cost | 10 mcoCoins/run |
> 8560	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8561	| Stripe | Sandbox keys active — swap to live before first client |
> 8562	
> 8563	---
> 8564	
> 8565	## GraphRAG State
> 8566	
> 8567	- **8993 total nodes** (verificado live 2026-06-30 via REST count=exact, gabriel-ai-fatia1-spaces-p0-kanban-live seal: +handoff `aba1458e-2df1-4813-a71b-34360bf7417e` embedded 768d — Programa Gabriel AI [deepsearch força-total → BoK `avatar-clone-ai` 10/10 selada nó `ee81987d` GO-HYBRID + Fatia 1 BYOK hedra/cartesia/fal] + Spaces canvas Phase 0 (scaffold promovido) + Kanban painel-de-detalhe + reconciliador vivo não-destrutivo + cron */15; 6 commits `a5814d2`..`71f4c47`; prev 8992 = BoK seal `ee81987d` `documentation_suite` avatar-clone-ai DERIVES_FROM video-studio `c99b7875`)
> 8568	- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8569	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8570	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8571	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8572	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8573	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8574	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8575	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8576	- HNSW cosine index operational
> 8577	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8578	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8579	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8580	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8581	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8582	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8583	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8584	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8585	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8586	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8587	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8588	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8589	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8590	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8591	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8592	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8593	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8594	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8595	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8596	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8597	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8598	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8599	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8600	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8601	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8602	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8603	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8604	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8605	
> 8606	### Embedding Model
> 8607	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8608	Schema: `vector(768)` — HNSW cosine index.
> 8609	
> 8610	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8611	Três camadas eliminam intervenção manual:
> 8612	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8613	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8614	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8615	
> 8616	### Comandos de manutenção da Mesh
> 8617	```bash
> 8618	# Verificar nós sem embedding (deveria retornar array vazio):
> 8619	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8620	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8621	
> 8622	# Backfill manual (Bun-native — requer .env):
> 8623	bun run scripts/backfill-embeddings.ts
> 8624	
> 8625	# Backfill de código-fonte nos nós AST:
> 8626	bun run scripts/backfill-node-content.ts
> 8627	
> 8628	# Re-sync AST completo:
> 8629	cd packages/gitnexus-core && npm run sync-mesh
> 8630	
> 8631	# Acompanhar re-ingesta pós-commit:
> 8632	tail -f /tmp/mcorch-ingest.log
> 8633	```
> 8634	
> 8635	---
> 8636	
> 8637	## Video Rescue Protocol
> 8638	
> 8639	When a video generation operation (Google Veo) times out or client disconnects:
> 8640	```bash
> 8641	# Via edge function (production):
> 8642	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8643	  -H "Authorization: Bearer <user_jwt>" \
> 8644	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8645	
> 8646	# Via local script (admin/debug):
> 8647	source .env && bun run rescue.ts <operation_id> <content_id>
> 8648	```
> 8649	
> 8650	---
> 8651	
> 8652	## Architecture Pillars
> 8653	
> 8654	| Layer | Implementation |
> 8655	|-------|---------------|
> 8656	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8657	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8658	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8659	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8660	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8661	
> 8662	---
> 8663	
> 8664	## Phase Delta — Architecture
> 8665	
> 8666	```
> 8667	OrchestrationPage (full-canvas, p-0)
> 8668	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8669	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8670	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8671	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8672	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8673	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8674	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8675	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8676	
> 8677	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8678	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8679	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8680	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8681	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8682	```
> 8683	
> 8684	### Canvas State Architecture (Hybrid)
> 8685	
> 8686	```
> 8687	User interaction → ReactFlow internal state (positions, drag)
> 8688	                         ↓ (debounced 600ms)
> 8689	                   localStorage (positions persist across refresh)
> 8690	                         ↑
> 8691	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8692	     ↓ (status changes sync to ReactFlow via useEffect)
> 8693	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8694	```
> 8695	
> 8696	## Key Files
> 8697	
> 8698	| Purpose | Path |
> 8699	|---------|------|
> 8700	| Architecture rules | `CLAUDE.md` |
> 8701	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8702	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8703	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8704	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8705	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8706	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8707	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8708	| **Node types** | `src/components/orchestrator/nodes/` |
> 8709	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8710	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8711	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8712	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8713	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8714	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8715	| Billing utilities | `src/lib/billing.ts` |
> 8716	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8717	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8718	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8719	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8720	| Video rescue (local) | `rescue.ts` |
> 8721	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8722	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8723	| Deploy harness | `scripts/harness-deploy.sh` |
> 8724	
> 8725	---
> 8726	
> 8727	## First Client Onboarding Checklist
> 8728	
> 8729	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8730	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8731	3. ~~Activate watchdog cron~~ ✅ Done
> 8732	4. ~~Deploy rescue-video function~~ ✅ Done
> 8733	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8734	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8735	7. Monitor `infra_health_logs` for first 24h.
> 8736	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8737	
> 8738	---
> 8739	
> 8740	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8741	
> 8742	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8743	
> 8744	| Action | Result |
> 8745	|--------|--------|
> 8746	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8747	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8748	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8749	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8750	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8751	
> 8752	| Commit | Conteúdo |
> 8753	|--------|----------|
> 8754	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8755	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8756	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8757	
> 8758	### Arquitetura Matrix Intelligence
> 8759	
> 8760	```
> 8761	ConstellationMatrix (Stabilized Engine)
> 8762	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8763	  └── NodeDetailsPanel (Tabbed Navigation)
> 8764	        ├── Tab Meta: Neighbor exploration + Net Context
> 8765	        ├── Tab Code: Source code preview (Supabase sync)
> 8766	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8767	
> 8768	useNodeIntelligence Hook:
> 8769	  - contentQuery: fetch nodes.content column
> 8770	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8771	  - state: isAnalyzing, analysisResult, progress
> 8772	```
> 8773	
> 8774	---
> 8775	
> 8776	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8777	
> 8778	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8779	
> 8780	| Action | Result |
> 8781	|--------|--------|
> 8782	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8783	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8784	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8785	
> 8786	**Output da análise (estruturado em pt-BR):**
> 8787	- Visão Geral — papel do módulo no sistema
> 8788	- Padrões Detectados — design patterns, antipatterns
> 8789	- Acoplamento & Dependências — análise In/Out-Degree
> 8790	- Recomendações — 1-3 ações priorizadas
> 8791	
> ```

## 🤖 Claude *(04:49:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"---sprint---\"; ls -la .claude/context/sprint-priorities.md 2>/dev/null && echo \"exists\" || echo \"MISSING\"",
  "description": "scratch contents + sprint file existence"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun 30 01:44 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 30 01:42 ..
> ---sprint---
> -rw-rw-r-- 1 ubuntu ubuntu 139328 Jun 27 00:37 .claude/context/sprint-priorities.md
> exists
> ```

## 🤖 Claude *(04:49:20)*


## 🤖 Claude *(04:49:20)*

Let me run the BoK gate check and pull the sprint goal head.

## 🤖 Claude *(04:49:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nfor slug in $(ls docs/bok/ 2>/dev/null); do\n  if [ \"$slug\" = \"security\" ]; then\n    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)\n    missing=()\n    for doc in \"${required_sec[@]}\"; do\n      [ -f \"docs/bok/security/$doc.md\" ] || missing+=(\"$doc\")\n    done\n    [ ${#missing[@]} -eq 0 ] && echo \"\u2705 security \u2014 complete\" || echo \"\u26a0\ufe0f security \u2014 missing: ${missing[*]}\"\n    continue\n  fi\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK gate completeness check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ agentic-governance
> ✅ agentic-workspace
> ✅ aios-sql-bridge
> ✅ authenticated-browser-operator
> ✅ avatar-clone-ai
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
> ✅ security — complete
> ⚠️ spaces-evolution — missing: 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> ✅ video-studio
> ✅ viral-autopilot
> ✅ viral-daily-canvas
> ✅ viralmind
> ✅ vision-mcp
> ```

## 🤖 Claude *(04:49:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -iE \"sprint goal|## .*goal|^# \" .claude/context/sprint-priorities.md | head -15",
  "description": "Sprint goal extraction"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # 🧠 Sprint Priorities — Constellation Orchestra
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> **Sprint v6.42.0 — Viral Autopilot BoK 9/9: motor de conteúdo viral autônomo (R1-R4) (2026-06-17)** — `/handson` → diretiva Sovereign de **retomar o objetivo-núcleo de receita** (= o próprio Sprint Goal "distribuição social autônoma operacional"): alimentar redes com conteúdo viral auto-gerado/agendado (tudo de uma vez OU a cada N dias), que a cada ciclo analisa o anterior p/ melhorar os próximos criativos, monetizado c/ afiliado ML. Arco Closed-Loop puro (zero código de produto): **(1) Auditoria material** (workflow 7 agentes, prova path:linha) — R1/R4 parciais vivos, **R2 (recorrência) e R3 (loop auto-melhorável) AUSENTES** (`campaign_metrics` sem writer, `optimization_policy` nunca lida, `self-optimize` sem cron); **(2) 4 decisões soberanas** (AskUserQuestion: suite NOVO · MVP texto+imagem · sinal R3 combo · 3 SKUs); **(3) BoK 9/9** (1889 LOC, FR-VA-001..021, 12 FMEA 4×RPN>100); **(4) Validação Fase 6 em 4 rodadas adversariais** (4 críticos/rodada) + grep determinístico — pegou buraco de segurança real (cron `verify_jwt=false` sem prova service-role in-function) + anti-mint (refund por deduct negativo, que EU introduzi); **(5) seal** (node `b3398294` embedded 768d, DERIVES_FROM marketing-hub). **Prova:** tsc 0 · 3 commits pushed · Phase 5c **SEAL ALLOWED** (10) · mesh **8928** · handoff `496ec17c`. **BoK Gate ABERTO.** Pending: fatia 1 (product-aware + monetize, NÃO depende do cron) + SOP `autopilot-cron-identity.md` (Lei 2/OTD-VA-008) antes da cadência. **Lição:** verificação adversarial multi-rodada foi essencial — cada "fix" meu deixava um resíduo que a rodada seguinte pegava; não auto-declarar GO (Lei 1).
> ```

## 🤖 Claude *(04:49:34)*


## 🤖 Claude *(04:49:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; ls docs/bok/spaces-evolution/ 2>/dev/null; echo \"---agentic-workspace (sibling?)---\"; ls docs/bok/agentic-workspace/ 2>/dev/null | head",
  "description": "Inspect spaces-evolution BoK contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 00-index.md
> 01-mrd-spaces.md
> 02-brd-spaces.md
> 03-prd-spaces.md
> 04-frd-spaces.md
> 05-sdd-spaces.md
> 09-live-recon-spaces.md
> 10-ui-inventory-spaces.md
> 11-node-registry-spaces.md
> 12-node-anatomy-spaces.md
> IMPLEMENTATION-PROMPT.md
> scaffold
> ---agentic-workspace (sibling?)---
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

## 🤖 Claude *(04:49:54)*


## 🤖 Claude *(04:50:16)*

═══════════════════════════════════════════════════════════
  HANDSON — Programa "Gabriel AI" (selada 2026-06-30)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  **Fase selada:** Programa "Gabriel AI" — BoK `avatar-clone-ai` + Fatia 1 BYOK + Spaces Phase 0 + Kanban vivo
  **Últimos commits:**
```
9d04641 docs(handoff): seal Gabriel AI — BoK avatar-clone-ai + Fatia 1 BYOK + Spaces P0 + Kanban live
71f4c47 docs(readme): v6.60.0 — mesh 8993
7b05945 feat(kanban): non-destructive roadmap reconciler + cron (live board)
ce28265 feat(kanban): card detail dialog with manual actions
3f36d27 feat(spaces): Phase 0 — promote Spaces canvas scaffold + BoK suite
```

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ · `scratch/` limpo ✅

🏗️ **INFRA** — tudo saudável ✅
  `mcorch_vision_mcp`: Up 11h (healthy) · `mcorch_chroma`: Up 2w (healthy) · Chroma API v2: **OK** (heartbeat)
  `mcorch_claude_mem`: healthy · `mega-brain-daemon`/`-webhook`: healthy · `-dashboard`: up

🧠 **KNOWLEDGE MESH**
  **8993 nós** · 9070 arestas (fonte: GraphRAG State, nós verificados live 2026-06-30)
  Último seal node: `aba1458e` (handoff, 768d) + BoK seal `ee81987d` (avatar-clone-ai, DERIVES_FROM video-studio)

🔧 **TYPESCRIPT** — Zero erros ✅

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
  **Seladas (24):** todas completas — incl. `avatar-clone-ai` (10/10, recém-selada), `security` (4-artifact CISO), `video-studio`, `viral-autopilot`, `post-engine`, `vision-mcp`…
  **Ressalva (não-bloqueante):** `spaces-evolution` usa naming sufixado (`01-mrd-spaces.md`…`05-sdd-spaces.md` + docs 09-12). O gate de 5-docs MCORCH (MRD→SDD) está **satisfeito**; só o checker de 9-docs canônicos faz falso-positivo (06/07/08 substituídos por 09-live-recon/10-ui-inventory/11-node-registry/12-node-anatomy).

📌 **SPRINT**
  **Goal:** Distribuição social autônoma operacional (LinkedIn auto ✅ · Twitter gated em API tier · IG gated em App Review).
  **Eixo estratégico atual** (memória): virada **brand-first** — persona Gabriel AI/CCIO evangeliza o MCORCH; reusa o motor Viral Autopilot.

⚡ **PRÓXIMOS PASSOS** (prioridade — todos com BoK Gate ABERTO)
  1. **Avatar-clone-ai Fatia 2** — dar sequência ao programa Gabriel AI recém-iniciado (Fatia 1 BYOK já vive). Próxima fatia = pipeline de geração de avatar fiel (Hedra default) → entrega valor visível ao Usuário Zero (alinhado à diretiva `feedback_deliver_user_value_not_plumbing`).
  2. **Viral Autopilot — fechar saída visível:** 1º ciclo PAGO de **vídeo 9:16 witnessed** (habilitar `video_enabled` + GO) + **publish vertical** TikTok/IG/YT (OAuth já conectado por canal desde 2026-06-27; gap conhecido: `auto-publish` não passa `video_url` + `VIDEO_FLOW_PLATFORMS`) + postback ML real (atribuição).
  3. **Spaces canvas** — avançar além da Phase 0 (scaffold promovido); ou **Unified Sensorial Canvas 3.5-3.10** (sinapses reais + fly-to + perf).

⚠️ **ALERTAS**
  Nenhum bloqueador ✅ — tsc limpo, infra saudável, worktree limpo.
  Lembrete operacional ativo (memória): **Vision QA** (`scripts/qa/vision-qa.ts`) obrigatório em todo print de inspeção + criativo antes de declarar pronto; **verificar UI em browser real** antes de "pronto" (Lei 1). Gates Sovereign-side pendentes: ativar `video_enabled` do Autopilot, audits YT/TikTok publish.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

Qual frente seguimos, Maestro? Minha recomendação é **Avatar-clone-ai Fatia 2** — continua o programa que você acabou de abrir e entrega algo que você *abre e toca*, em vez de mais plumbing.

## 👤 User *(04:51:06)*

ótimo então vamos em frente continue

## 🤖 Claude *(04:51:17)*


## 🤖 Claude *(04:51:21)*

O Sovereign autorizou seguir com **Avatar-clone-ai Fatia 2**. BoK Gate já está ABERTO (suíte 10/10 selada). Vou primeiro mapear materialmente o que a Fatia 2 exige antes de qualquer código.

**ORO triplet desta task:**
- **Operator:** AI Agent (MCORCH Master Execution Agent)
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign (ROI = primeiro ciclo de avatar fiel ao Usuário Zero; blast radius = crédito BYOK per-user + reputação de marca)

Deixa eu mapear a BoK e o estado da Fatia 1 para saber exatamente o que é Fatia 2.

## 🤖 Claude *(04:51:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; ls -la docs/bok/avatar-clone-ai/; echo \"=== wc ===\"; wc -l docs/bok/avatar-clone-ai/*.md",
  "description": "List avatar-clone-ai BoK docs with sizes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 476
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun 30 00:24 .
> drwxrwxr-x 27 gcrUX  gcrUX   4096 Jun 29 21:21 ..
> -rw-rw-r--  1 ubuntu ubuntu 23856 Jun 29 22:08 00b-fatia0-viability-format-probe.md
> -rw-rw-r--  1 ubuntu ubuntu 39367 Jun 29 22:41 00c-fatia0-fronts-closure.md
> -rw-rw-r--  1 ubuntu ubuntu 58216 Jun 29 22:23 00-deepsearch-blueprint.md
> -rw-rw-r--  1 ubuntu ubuntu 16352 Jun 30 00:24 00-index.md
> -rw-rw-r--  1 ubuntu ubuntu 29807 Jun 29 22:53 01-mrd.md
> -rw-rw-r--  1 ubuntu ubuntu 38907 Jun 29 22:57 02-brd.md
> -rw-rw-r--  1 ubuntu ubuntu 34852 Jun 29 23:01 03-prd.md
> -rw-rw-r--  1 ubuntu ubuntu 45488 Jun 30 00:09 04-frd.md
> -rw-rw-r--  1 ubuntu ubuntu 47020 Jun 30 00:13 05-sdd.md
> -rw-rw-r--  1 ubuntu ubuntu 42731 Jun 30 00:18 06-data-model.md
> -rw-rw-r--  1 ubuntu ubuntu 29419 Jun 30 00:17 07-process-flow.md
> -rw-rw-r--  1 ubuntu ubuntu 28948 Jun 30 00:22 08-quality-metrics.md
> -rw-rw-r--  1 ubuntu ubuntu 16022 Jun 30 00:20 09-pattern-conformance.md
> === wc ===
>    185 docs/bok/avatar-clone-ai/00b-fatia0-viability-format-probe.md
>    287 docs/bok/avatar-clone-ai/00c-fatia0-fronts-closure.md
>    434 docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md
>    153 docs/bok/avatar-clone-ai/00-index.md
>    185 docs/bok/avatar-clone-ai/01-mrd.md
>    243 docs/bok/avatar-clone-ai/02-brd.md
>    302 docs/bok/avatar-clone-ai/03-prd.md
>    453 docs/bok/avatar-clone-ai/04-frd.md
>    577 docs/bok/avatar-clone-ai/05-sdd.md
>    492 docs/bok/avatar-clone-ai/06-data-model.md
>    395 docs/bok/avatar-clone-ai/07-process-flow.md
>    253 docs/bok/avatar-clone-ai/08-quality-metrics.md
>     64 docs/bok/avatar-clone-ai/09-pattern-conformance.md
>   4023 total
> ```

## 🤖 Claude *(04:51:27)*


## 🤖 Claude *(04:51:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-index.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BoK Documentation Suite — avatar-clone-ai
> 2	
> 3	**Generated:** 2026-06-30
> 4	**Version:** v0.1
> 5	**Agent:** MCORCH BoK Scribe Agent v1.0.0
> 6	**Sovereign:** Gabriel (Maestro / Reviewer + Owner)
> 7	
> 8	> **Posição no Closed-Loop Protocol (CLAUDE.md §1).** Este é o **manifesto** da suíte BoK do módulo `avatar-clone-ai` (programa "Gabriel AI") — selada a partir do gate **GO-HYBRID** (`00b-fatia0-viability-format-probe.md` §1). A suíte está **completa (MRD → BRD → PRD → FRD → SDD + Data Model + Process Flow + Quality Metrics + Pattern Conformance Declaration)**, o que fecha o **Closed-Loop Protocol Step 3 + Step 3.5** e **destrava a escrita de código das Fatias** (Refusal Mode levantado). Nenhuma linha de código de Fatia foi escrita antes desta suíte existir.
> 9	>
> 10	> **Fonte da Verdade (não reabrir):** os **3 seeds da Fatia 0** — `00-deepsearch-blueprint.md`, `00b-fatia0-viability-format-probe.md`, `00c-fatia0-fronts-closure.md` — são a **única** Fonte da Verdade fundamentada em deepsearch. Toda requirement da suíte rastreia esses seeds; nada inventa além deles. Ambiguidade → retorno a `/bok-scribe`, nunca improvisação.
> 11	>
> 12	> **ORO triplet desta suíte** — Operator: MCORCH Master Execution Agent + L1 engineer / L1 marketing-growth · Reviewer: Sovereign (Gabriel) · Owner: Sovereign até v6.x (blast radius = persona pública sintética + artefatos biométricos PII per-tenant + risco contratual BYOK por provider; migra a marketing-growth quando a North-Star de marca for definida e atingida — OTD-AC-013).
> 13	
> 14	---
> 15	
> 16	## Project Metadata
> 17	
> 18	| Field | Value |
> 19	|-------|-------|
> 20	| Business Idea | Estúdio de **persona-IA híbrida** per-user no Canvas Studio (programa "Gabriel AI", instância-zero): clona rosto + voz clonada + "cérebro clonado" (RAG sobre a memory mesh) e alimenta a cadência de 30 dias sobre o Viral Autopilot — rosto real do fundador **ancora**, avatar-IA escala volume/idiomas **declarado** (NÃO 100%-avatar) |
> 21	| Market Segment | **B2B2C** — instância-zero (Sovereign / Usuário Zero, fundador-CCIO build-in-public) → generalizável a criadores-fundadores / AI-educators que clonam **a si mesmos** (self-clone) ou criam persona fictícia original |
> 22	| Monetization Model | **Híbrida** — mcoCoins por render (4×-floor `mco=ceil(usd/$0.018×4)` via RPC atômica `deduct_mco_coins`; Hedra 60s ~480 mco / OmniHuman 1.5 ~2169 mco / dia footage-real ~36 mco) + planos Starter/Pro/Enterprise + afiliado ML como subproduto (≤20% dos posts) |
> 23	| Regulatory Profile | **LGPD (biométrico = dado sensível, Art. 5 II + 11/16/18)** + **EU AI Act Art. 50 (C2PA machine-readable §50(2) + disclosure deepfake §50(4), vigência 02/08/2026) + Art. 5(1)(g) red-line** + CONAR (solidary-liability + identificação de influencer virtual) + TSE (red-line eleitoral) + disclosure por plataforma (YouTube/TikTok/Meta) |
> 24	| Integration Surface | **extends-mcorch** — monta sobre primitivos em produção (Canvas node registry, `generate-image`/`canvas-execute`, HyperFrames, Channel Reshaper/`channel_variants`/`pillar_atoms`, `creative_assets`, `video_renders`/`finalize`, Viral Autopilot/`autopilot_plans`, `user_api_keys` Vault, Vision MCP erase, `_shared/sentinel.ts`/`llm-fallback.ts`); net-new = 5 nós Canvas tipados + `generate-voice` + reply engine X + tabelas biométricas + compliance gate |
> 25	| Project Slug | `avatar-clone-ai` |
> 26	
> 27	**Decisões travadas (a suíte respeita, não reabre):** (1) postura **HÍBRIDO** rosto-real + avatar-backfill declarado, NÃO 100%-avatar (crater McCoy, FM-AC-014); (2) **GLOBAL ENGLISH-FIRST** — 1 trilha-fonte EN + auto-dub nativo da plataforma p/ PT-BR (alcance) / voz PT clonada + re-lip-sync (premium); (3) avatar = módulo **per-user BYOK PURO (Modelo A)** no Canvas Studio — Hedra Character-3 (default) / OmniHuman / Higgsfield; Magnific = conta-org **interna** (enhance final); HeyGen = partnership **futuro**; **INVARIANTE: nunca multiplexar conta-mestra (service bureau proibido)**; (4) **reply engine do X = escopo core** (agent loop real-time mentions→reply); (5) idioma + frequência = per-user opt-in; (6) Gabriel AI = instância-zero (B2B2C); (7) monetização **híbrida** mcoCoins 4×-floor + planos; (8) LGPD biométrico Art. 11 + EU AI Act Art. 50.
> 28	
> 29	---
> 30	
> 31	## Document Registry
> 32	
> 33	| # | File | Document | BoK Applied | LOC | Status |
> 34	|---|------|----------|-------------|-----|--------|
> 35	| — | `00-deepsearch-blueprint.md` | DeepSearch Blueprint (**SEED — Fonte da Verdade**) | Deep Research + Adversarial Verify | 434 | [x] complete |
> 36	| — | `00b-fatia0-viability-format-probe.md` | Fatia 0 — Viability & Format Probe (**SEED — gate GO-HYBRID**) | Deep Research + Adversarial Verify | 185 | [x] complete |
> 37	| — | `00c-fatia0-fronts-closure.md` | Fatia 0 — Fronts F1–F7 Closure (**SEED — Fonte da Verdade**) | Deep Research + Adversarial Verify | 287 | [x] complete |
> 38	| 0 | `00-index.md` | Project Manifest | — | (este doc) | [x] complete |
> 39	| 1 | `01-mrd.md` | Market Requirements Document | BABOK v3 (Strategy Analysis + Elicitation) | 185 | [x] complete |
> 40	| 2 | `02-brd.md` | Business Requirements Document | BABOK v3 (Requirements Analysis & Design Definition) | 243 | [x] complete |
> 41	| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | 302 | [x] complete |
> 42	| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 (Software Requirements) | 453 | [x] complete |
> 43	| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 (Software Design) + CISSP CBK 2024 | 577 | [x] complete |
> 44	| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | 492 | [x] complete |
> 45	| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | 395 | [x] complete |
> 46	| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | 253 | [x] complete |
> 47	| 9 | `09-pattern-conformance.md` | Pattern Conformance Declaration (21 Agentic Patterns) | Gulli *Agentic Design Patterns* (`agentic-vision.md` §2) | 64 | [x] complete |
> 48	
> 49	> **Nota de Fonte da Verdade.** Os três seeds `00`/`00b`/`00c` (Fatia 0) são a **ÚNICA** Fonte da Verdade fundamentada em deepsearch desta suíte. Cada documento 01→09 deriva exclusivamente deles (+ o documento a montante na cadeia BABOK→ProdBOK→SWEBOK→DMBOK→BPM→CMQ/OE). Qualquer afirmação externa carrega URL-fonte nos seeds; claims refutadas pela verificação adversarial estão marcadas `❌ REFUTADO` e só aparecem na versão corrigida (Lei 1 Materialidade). **A suíte não pode ser emendada acima do superset dos seeds sem reabrir `/bok-scribe`.**
> 50	
> 51	---
> 52	
> 53	## ID Space Summary
> 54	
> 55	> IDs prefixados `*-AC-*` zero-pad 3 dígitos. OTD-AC-* e FM-AC-* **reusam** os ids cunhados nos seeds (não renumerados). Cadeia de rastreabilidade completa **MR → BR → PR → FR → NFR** fechada (cada FR-AC rastreia ≥1 PR-AC; cada PR-AC ≥1 BR-AC; cada BR-AC ≥1 MR-AC).
> 56	
> 57	| ID Family | Range | Count | Owning Document | Meaning |
> 58	|-----------|-------|-------|-----------------|---------|
> 59	| **MR-AC** (Market Requirements) | MR-AC-001 .. MR-AC-019 | 19 | `01-mrd.md` | Requisitos de mercado (BABOK) |
> 60	| **BR-AC** (Business Requirements) | BR-AC-001 .. BR-AC-028 | 28 | `02-brd.md` | Requisitos de negócio + custo mcoCoins + critério de aceite |
> 61	| **BO** (Business Objectives, SMART) | BO-001 .. BO-004 | 4 | `02-brd.md` | Objetivos SMART de negócio |
> 62	| **BR-RISK** (Business Risk Register) | BR-RISK-001 .. BR-RISK-012 | 12 | `02-brd.md` | Riscos com RPN (mapeiam FM-AC-*) |
> 63	| **BAC** (Business Acceptance Criteria) | BAC-001 .. BAC-014 | 14 | `02-brd.md` | Critérios de aceite materiais |
> 64	| **PR-AC** (Product Requirements) | PR-AC-001 .. PR-AC-028 | 28 | `03-prd.md` | Features (MoSCoW + Release Phasing) |
> 65	| **FR-AC** (Functional Requirements) | FR-AC-001 .. FR-AC-054 | 54 | `04-frd.md` | Comportamento implementável (UI/Hook/EdgeFunction/DB/Cron) |
> 66	| **NFR-AC** (Non-Functional Requirements) | NFR-AC-001 .. NFR-AC-020 | 20 | `04-frd.md` | Performance · Scalability · Security · Privacy/Compliance · Identity Fidelity · Render Determinism · Cost Integrity · Observability |
> 67	| **AT-AC** (Acceptance Test IDs) | AT-AC-001 .. AT-AC-054 | 54 | `04-frd.md` | Matriz de teste (Unit/Integration/E2E) |
> 68	| **PROC-AC** (Process Inventory) | PROC-AC-001 .. PROC-AC-008 | 8 | `07-process-flow.md` | Processos BPMN-lite + SLA |
> 69	| **QO-AC** (Quality Objectives) | QO-AC-001 .. QO-AC-005 | 5 | `08-quality-metrics.md` | Objetivos de qualidade (CMQ/OE) |
> 70	| **KPI-AC** (KPI Dashboard) | KPI-AC-001 .. KPI-AC-016 | 16 | `08-quality-metrics.md` | KPIs anti-Goodhart cruzados com `collective_efficiency_ledger` |
> 71	| **OTD-AC** (Open Technical Decisions) | OTD-AC-001 .. OTD-AC-014 (+ -011-a/b/c) | 14 (+3 sub) | seeds (reusados) | Decisões técnicas — maioria FECHADA na Fatia 0; gaps Lei 1 OTD-AC-011-a/b/c abertos p/ GA |
> 72	| **FM-AC** (FMEA Failure Modes) | FM-AC-001 .. FM-AC-014 | 14 | seeds (reusados) | Modos de falha; FM-AC-014 (uncanny-valley) = **maior RPN** |
> 73	
> 74	### Pattern Conformance scorecard (`09-pattern-conformance.md`)
> 75	
> 76	21 Agentic Patterns (`docs/architecture/agentic-vision.md` §2): **`yes` × 13** (#1 Prompt Chaining · #2 Routing · #4 Reflection · #5 Tool Use · #8 Memory · #11 Goal Monitoring · #12 Exception Recovery · #13 HITL · #14 RAG · #16 Resource-Aware · #18 Guardrails · #19 Evaluation · #21 Exploration) · **`deferred` × 5** (#3 Parallelization→OTD-AC-012 · #6 Planning→OTD-AG-005 · #7 Multi-Agent→OTD-AG-006 · #9 Learning→OTD-AG-002 · #20 Prioritization→OTD-AG-020) · **`n-a` × 3** (#10 MCP · #15 A2A · #17 Reasoning Techniques). Concentração em execução criativa multimodal (Tool Use + Chaining + RAG + Reflection + Guardrails + Resource-Aware + Evaluation + HITL) confirma a natureza declarada.
> 77	
> 78	---
> 79	
> 80	## Traceability Chain
> 81	
> 82	```
> 83	MR-AC-001..019           (01-mrd.md — BABOK)
> 84	  └── BR-AC-001..028     (02-brd.md — BABOK; + BO/BR-RISK/BAC)
> 85	        └── PR-AC-001..028   (03-prd.md — ProdBOK + CXBOK)
> 86	              └── FR-AC-001..054 + NFR-AC-001..020   (04-frd.md — SWEBOK)
> 87	                    └── [05-sdd.md design · 06-data-model schema · 07-process-flow PROC-AC · 08-quality-metrics KPI-AC]
> 88	                          └── 09-pattern-conformance.md (Gate Step 3.5 — 21 patterns)
> 89	
> 90	Cross-cutting (seeds): OTD-AC-001..014 (+011-a/b/c) · FM-AC-001..014 → reusados em toda a cadeia
> 91	```
> 92	
> 93	---
> 94	
> 95	## Phase Completion Log
> 96	
> 97	| Phase | Name | Completed | Notes |
> 98	|-------|------|-----------|-------|
> 99	| 0 | Project Bootstrap (Fatia 0: blueprint + viability probe + fronts closure) | 2026-06-29 | Gate **GO-HYBRID** fechado; Refusal Mode levantado; 3 seeds = Fonte da Verdade |
> 100	| 1 | Market & Business Intelligence (MRD + BRD) | 2026-06-29 | 19 MR-AC + 28 BR-AC + 4 BO + 12 BR-RISK + 14 BAC |
> 101	| 2 | Product Definition (PRD) | 2026-06-29 | 28 PR-AC (MoSCoW + 3 personas + Release Phasing MVP/v1.0/Future) |
> 102	| 3 | Technical Specification (FRD + SDD) | 2026-06-30 | 54 FR-AC + 20 NFR-AC + 54 AT-AC; SDD design + STRIDE + migration stubs |
> 103	| 4 | Data & Process Engineering (Data Model + Process Flow) | 2026-06-30 | OTD-AC-005 (reuso `video_renders`); 3 tabelas biométricas net-new; 8 PROC-AC |
> 104	| 5 | Quality & Autonomic Engineering (Quality Metrics) | 2026-06-30 | 5 QO-AC + 16 KPI-AC anti-Goodhart + FMEA RPN + PDCA |
> 105	| 6 | Traceability Validation | 2026-06-30 | Cadeia MR→BR→PR→FR→NFR fechada; matrizes em cada doc |
> 106	| 7 | Pattern Conformance (Gate Step 3.5) | 2026-06-30 | `09-pattern-conformance.md` — 13 yes / 5 deferred / 3 n-a |
> 107	
> 108	---
> 109	
> 110	## Open Technical Decisions (status pós-Fatia 0)
> 111	
> 112	> Reusados dos seeds (`00c-fatia0-fronts-closure.md` §Fechamento). Maioria **FECHADA** na Fatia 0; os 3 gaps Lei 1 (-011-a/b/c) + OTD-AC-013 permanecem abertos com SLA.
> 113	
> 114	| OTD ID | Description | Status | Resolução / SLA |
> 115	|--------|-------------|--------|-----------------|
> 116	| OTD-AC-001 | Motor talking-head (BYOK self-serve) | **FECHADO + refinado** | Roteamento por uso: OmniHuman 1.5 p/ re-lip-sync footage real; Hedra/Kling p/ avatar-IA backfill (F3) |
> 117	| OTD-AC-004 | Identity Gate / qualidade avatar | **FECHADO** | Cosine calibrado empírico FAR/FRR/EER (nunca hardcode); + Vision QA gate |
> 118	| OTD-AC-005 | Modelo de dados do render avatar | **FECHADO** | REUSA `video_renders` + `composition.avatar` jsonb (NÃO tabela dedicada) — `06-data-model.md` |
> 119	| OTD-AC-006 | Cost model 4×-floor | **FECHADO (datado)** | `AVATAR_VIDEO_COST` ≠ `VIDEO_COST`; Hedra 480 / OmniHuman 2169 / footage-real 36 mco; recalibrar no SDD |
> 120	| OTD-AC-008 | C2PA × determinismo sha256 (NFR-VS-016) | **ELEVADO a REQUISITO LEGAL** | Spike de determinismo ANTES de selar render (FR-AC-037); Art. 50(2) machine-readable |
> 121	| OTD-AC-009 | Reply engine X | **FECHADO (core) + economia redefinida** | Pay-per-use, polling, cap per-user; "tier acessível" REFUTADO |
> 122	| OTD-AC-010 | Consent + identity-verification | **FECHADO (gate de lançamento)** | Consent por-render fail-closed + erasure + segregação (F6) |
> 123	| OTD-AC-011 | BYOK legal por provider | **FECHADO condicional (Modelo A)** | Invariante anti-conta-mestra; 3 gaps Lei 1 abertos abaixo |
> 124	| OTD-AC-011-a | Magnific §3 "API Services" (truncada) | **ABERTO (Lei 1)** | Ler literalmente + confirmar chave per-end-user — antes do GA |
> 125	| OTD-AC-011-b | ElevenLabs resale-clause | **ABERTO (Lei 1)** | Confirmar palavra-por-palavra a frase de resale — antes do GA |
> 126	| OTD-AC-011-c | OmniHuman titular contratual (fal.ai vs BytePlus) | **ABERTO (Lei 1)** | Confirmar se user-com-conta-própria é "Customer" — antes do GA |
> 127	| OTD-AC-012 | Idioma/frequência (custo 2×) | **FECHADO** | Auto-dub = ALCANCE (não dispensa voz clonada); trilha clonada = PREMIUM; 1 trilha EN-fonte |
> 128	| OTD-AC-013 | North-Star de marca + trigger Owner | **ABERTO** | Define quando Owner migra Sovereign→marketing-growth; gate de fracasso = não antes de ~100 posts |
> 129	| OTD-AC-014 | RAMP × 12+/mês | **FECHADO** | Ramp por-canal independente; volume agregado cross-canal cresce com cada canal em ramp suave |
> 130	
> 131	---
> 132	
> 133	## FMEA Failure Modes (reusados dos seeds — `00`/`00c`)
> 134	
> 135	| FM ID | Failure Mode | Status | Mitigação-âncora |
> 136	|-------|--------------|--------|------------------|
> 137	| FM-AC-014 | **Rejeição de audiência ao avatar 100%-puro (uncanny-valley)** — **MAIOR RPN** (crater McCoy 30k→3k) | mitigado | Postura híbrida invariante (FR-AC-033) + injeção de clipe real + Vision QA descarta uncanny |
> 138	| FM-AC-002/007 | Motor de cadência vira slop suprimido (inauthentic content) | mitigado | Gate anti-templating duro (FR-AC-050); variantes NATIVAS por canal |
> 139	| FM-AC-004 | Disclosure faltando → strike/desmonetização + risco legal | **FECHADO (gate não-pulável)** | C2PA + disclosure deepfake (FR-AC-035/036); rotular NÃO reduz reach |
> 140	| FM-AC-011 | Vazamento cross-tenant de artefato biométrico (PII) | **FECHADO (design)** | RLS own + bucket isolado cifrado + signed URLs curtos (FR-AC-025/026) |
> 141	| FM-AC-010 | BYOK pass-through viola ToS (escorregar p/ Modelo B) | **FECHADO condicional** | Invariante anti-conta-mestra (FR-AC-006); Magnific=org-key, HeyGen=partnership FORA |
> 142	| FM-AC-006 | Conta nova flagada / publicação bloqueada sem audit | endereçado | RAMP por-canal (FR-AC-049) + gates per-canal ação Sovereign (FR-AC-053) |
> 143	| FM-AC-012 | Lip-sync PT-BR fora de sincronia (auto-dub voz genérica) | endereçado | Dois caminhos PT-BR: auto-dub (alcance) / re-lip-sync próprio (premium, FR-AC-041) |
> 144	| FM-AC-013 | Code-switching PT-BR↔EN intra-frase / accent-bleed | mitigado | Code-switching guard (FR-AC-010); um idioma por geração |
> 145	| FM-AC-001 | Shippar pesos non-commercial (InfiniteYou/F5-TTS/FLUX.1-dev/XTTS-v2) | mitigado | Gate de licença (FR-AC-016); BYOK escapa via conta do user |
> 146	| FM-AC-003 | Passo high-Creativity tocando o rosto por último (deriva identidade) | mitigado | Ordem identidade-ANTES-de-enhance (FR-AC-023) |
> 147	| FM-AC-005 | Charge-without-value (render avatar sem refund) | mitigado | `finalize_avatar_render` + `refund_autopilot_video_enqueue` idempotente (FR-AC-021/048) |
> 148	| FM-AC-008 | Identity Gate mal-calibrado (hardcode) | mitigado | Calibração empírica FAR/FRR/EER (FR-AC-014) |
> 149	| FM-AC-009 | Conteúdo eleitoral/candidato (TSE red-line) | escopado fora | Won't Have; autoridade restrita a produto/tech |
> 150	
> 151	---
> 152	
> 153	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 154	
> ```

## 🤖 Claude *(04:51:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/05-sdd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SDD — System Design Document
> 2	
> 3	**Project:** avatar-clone-ai (programa "Gabriel AI")
> 4	**Version:** v0.1 | **Date:** 2026-06-30
> 5	**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)
> 6	**Status:** Draft
> 7	
> 8	> **Posição no Closed-Loop Protocol (CLAUDE.md §1).** Quinto e último documento da suíte BoK, derivado do gate **GO-HYBRID** (`00b-fatia0-viability-format-probe.md` §1). Fonte da Verdade = `01-mrd.md` + `02-brd.md` + `03-prd.md` + `04-frd.md` (a montante) + os três artefatos-semente da Fatia 0 (`00-deepsearch-blueprint.md`, `00b-fatia0-viability-format-probe.md`, `00c-fatia0-fronts-closure.md`). Este SDD traduz cada FR-AC/NFR-AC do `04-frd.md` em design implementável (componentes, contratos, threat model STRIDE, migration stubs) sob a lente SWEBOK Design + CISSP Software Development Security. **Nenhuma invenção além das fontes;** ambiguidade → retorno a `/bok-scribe`, nunca improvisação. **A Pattern Conformance Declaration (Gate Step 3.5)** vive em `09-pattern-conformance.md` (sibling, este módulo toca ≥3 padrões materialmente) — referenciada em §8.
> 9	>
> 10	> **ORO triplet deste SDD** — Operator: MCORCH Master Execution Agent + L1 engineer · Reviewer: Sovereign (Gabriel) · Owner: Sovereign até v6.x (blast radius = persona pública sintética + artefatos biométricos per-tenant + risco contratual BYOK por provider; migra a marketing-growth quando a North-Star de marca for definida e atingida — OTD-AC-013).
> 11	>
> 12	> **Decisões travadas que este SDD respeita (não reabre):** (1) postura HÍBRIDO rosto-real + avatar-backfill declarado (NÃO 100%-avatar — FM-AC-014); (2) posicionamento GLOBAL ENGLISH-FIRST (1 trilha-fonte EN + auto-dub nativo da plataforma p/ PT-BR como alcance; voz PT clonada + re-lip-sync como premium); (3) avatar = módulo per-user BYOK PURO **Modelo A** no Canvas Studio — nunca conta-mestra multiplexada (service bureau proibido); (4) reply engine do X = escopo core; (5) idioma + frequência = per-user opt-in; (6) Gabriel AI = instância-zero B2B2C; (7) monetização híbrida mcoCoins 4×-floor por render via RPC `deduct_mco_coins` + planos; (8) LGPD biométrico Art. 11 + EU AI Act Art. 50.
> 13	>
> 14	> **Constraints Harness não-negociáveis aplicados neste SDD:** lógica em hooks (hook-first; páginas/componentes display-only); SDD lista apenas o **NOME** da vault key BYOK per-user, nunca o valor do secret; billing SEMPRE via RPC `deduct_mco_coins` (nunca client-side); nós do Canvas seguem o registry existente (factory + handles + inspector + nodeTypes map + resolveExecutePayload); toda tabela nova nasce com RLS default-deny + trigger `embed-mcorch-node` + isolamento tenant `user_id`(+`project_id`); Edge Function com JWT validation; artefatos biométricos (`avatar_identities`/`voice_profiles`/`avatar_consents`) = RLS own + storage isolado per-tenant + erase RPC (molde `erase_vision_artifacts`).
> 15	
> 16	---
> 17	
> 18	## 1. Architecture Overview
> 19	
> 20	### 1.1 Harness Layer Map
> 21	
> 22	```
> 23	┌───────────────────────────────────────────────────────────────────────────┐
> 24	│  PRESENTATION LAYER (display-only)                                          │
> 25	│  src/pages/AvatarStudioPage.tsx          → iframe/host do Avatar Studio      │
> 26	│  src/components/avatar/AvatarStudioCanvas.tsx  (xyflow; nodeTypes registry) │
> 27	│  src/components/avatar/nodes/{AvatarIdentity,VoiceClone,AvatarScript,       │
> 28	│                               TalkingHead,AvatarEnhance}Node.tsx            │
> 29	│  src/components/avatar/ConsentWizard.tsx · IdentityVerificationGate.tsx     │
> 30	│  src/components/settings/AvatarProvidersCard.tsx (BYOK cards)               │
> 31	│  src/components/avatar/DisclosureMarkerBadge.tsx · McoCostBadge.tsx         │
> 32	└──────────────────────────────┬────────────────────────────────────────────┘
> 33	                               │ calls (zero data-fetch in components)
> 34	┌──────────────────────────────▼────────────────────────────────────────────┐
> 35	│  LOGIC LAYER (Harness Engineering — hook-first)                            │
> 36	│  src/hooks/useAvatarProviders.ts   (BYOK state; test-api-key invoke)        │
> 37	│  src/hooks/useAvatarConsent.ts     (wizard state; identity-verification)    │
> 38	│  src/hooks/useAvatarRender.ts      (talkingHead/voice render orchestration) │
> 39	│  src/hooks/useAvatarErasure.ts     (erase on-revoke + attestation)          │
> 40	│  src/store/useAvatarStudioStore.ts (Zustand — Canvas nodes/edges/run state) │
> 41	│  src/lib/avatar.ts                 (CanvasNodeKind recipes, SAFE_COLUMNS,    │
> 42	│                                     engine routing, COIN_COSTS avatar)       │
> 43	└──────────────────────────────┬────────────────────────────────────────────┘
> 44	                               │ HTTP + JWT (Bearer user scope)
> 45	┌──────────────────────────────▼────────────────────────────────────────────┐
> 46	│  EDGE LAYER (Deno / Supabase Functions — sensitive ops only)               │
> 47	│  generate-voice              (NET-NEW; ElevenLabs/Cartesia BYOK)            │
> 48	│  canvas-execute (kind=talkingHead)  (EXTEND; cost-gate + daily-cap + async) │
> 49	│  avatar-identity-train       (NET-NEW; Soul ID/LoRA + Identity Gate loop)   │
> 50	│  avatar-script               (EXTEND of generate-content path; RAG brain)   │
> 51	│  erase-avatar-artifacts      (NET-NEW; molde erase_vision_artifacts)        │
> 52	│  avatar-reply-engine         (NET-NEW; X mentions poll → reply)             │
> 53	│  avatar-retention-sweep      (NET-NEW cron; sweep por inatividade)          │
> 54	│  orchestrate-step (step=avatar_generation)  (EXTEND; Autopilot junction)    │
> 55	│  publish-social / publish gate  (EXTEND; LinkedIn+X video branches + C2PA)  │
> 56	└────────────┬──────────────────────────────────────┬───────────────────────┘
> 57	             │ Supabase RLS                          │ External BYOK APIs
> 58	┌────────────▼───────────────────────┐  ┌────────────▼───────────────────────┐
> 59	│  DB LAYER (RLS default-deny)        │  │  EXTERNAL SERVICES (Modelo A BYOK)  │
> 60	│  avatar_identities  (biometric)     │  │  Hedra Character-3 (talking-head)   │
> 61	│  voice_profiles     (biometric)     │  │  fal.ai / OmniHuman 1.5 (re-lipsync)│
> 62	│  avatar_consents    (immutable)     │  │  Higgsfield Soul ID / Kling         │
> 63	│  user_api_keys      (Vault BYOK)    │  │  ElevenLabs / Cartesia (voice)      │
> 64	│  video_renders · creative_assets    │  │  Magnific (≡Freepik) — ORG-KEY only │
> 65	│  channel_variants · autopilot_plans │  │  X/Twitter API (per-user OAuth)     │
> 66	│  mcorch_nodes (mesh) · infra_health │  │  OpenRouter (mesh embeddings/RAG)   │
> 67	└─────────────────────────────────────┘  └─────────────────────────────────────┘
> 68	```
> 69	
> 70	### 1.2 Canonical Pipeline (FRD §1 in-scope)
> 71	
> 72	```
> 73	[avatarIdentity] rosto-lock (Soul ID / LoRA per-user, ladder Tier1/2/3)
> 74	      │ output: input_face_identity        (avatar_identities, RLS own)
> 75	      ▼
> 76	   ┌─ Identity Gate (ArcFace cosine vs canonical embedding; limiar CALIBRADO
> 77	   │  FAR/FRR/EER — NUNCA hardcode 0.95/0.7-0.8) → fail-and-regenerate ──┐
> 78	   └────────────────────────────────────────────────────────────────────┘
> 79	      ▼
> 80	[voiceClone] voz clonada EN-âncora (PT-BR premium) — ElevenLabs PVC/IVC / Cartesia Sonic
> 81	      │ output: input_voice_profile        (voice_profiles, voiceprint cifrado Vault)
> 82	      │ guard: code-switching PT↔EN intra-frase BLOQUEADO (FM-AC-013)
> 83	      ▼
> 84	[avatarScript] roteiro do "cérebro clonado" — RAG sobre mcorch_nodes (GraphRAG, NÃO fine-tune)
> 85	      │ output: input_script               (+ Brand Voice DNA quantificado; sentinel pt-BR+EN)
> 86	      ▼
> 87	[talkingHead] lip-sync + animação — roteamento por source_type
> 88	      │ footage_real → OmniHuman 1.5 (re-lip-sync) · avatar_ai → Hedra/Kling
> 89	      │ output: output_avatar_video (MP4 9:16 1080×1920) via canvas-execute (async)
> 90	      │ deduct AVATAR_VIDEO_COST via RPC deduct_mco_coins (atômico, server-side)
> 91	      ▼
> 92	[avatarEnhance] Magnific Relight/upscale (polish FINAL via ORG-KEY interna)
> 93	      │ DISCIPLINA DE ORDEM (FM-AC-003): identidade ANTES de enhance; nunca high-Creativity por último
> 94	      ▼
> 95	→ Identity Gate (re-check pós-enhance) → Vision QA (uncanny descarte, BYOK-free)
> 96	→ C2PA embed (Art. 50(2) machine-readable) + disclosure marker (Art. 50(4))
> 97	→ creative_assets (source_module='avatar-studio') → Viral Autopilot (cadência 30d híbrida)
> 98	```
> 99	
> 100	### 1.3 Reuse-First Design Principle
> 101	
> 102	O módulo é **construído por reuso** (`00c §F4` build-vs-buy = construir orquestração, integrar motores via BYOK). Reusa, sem reescrever: o Canvas node registry (`src/lib/canvas-node-registry.ts`), `canvas-execute` (cost-gate/daily-cap/async), `video_renders` + `finalize_video_render`, `creative_assets` + `register_creative_asset`, `channel_variants`/`reshape-pillar`/`pillar_atoms`, `user_api_keys` Vault (encrypt trigger + masked/decrypted views — recipe `20260622210000`), `_shared/sentinel.ts` + `_shared/llm-fallback.ts`, e o pattern de erasure do Vision MCP (`erase_vision_artifacts` + `retention-sweep`). NET-NEW concentra-se em: pipeline de voz, infraestrutura biométrica (tabelas/storage/erase), gates de compliance (consent/identity-verification/disclosure/C2PA), reply engine do X, e a junção com o Viral Autopilot.
> 103	
> 104	---
> 105	
> 106	## 2. Component Catalog
> 107	
> 108	### 2.1 New Custom Hooks (`src/hooks/`)
> 109	
> 110	| Hook | File | Responsibility | TanStack Query keys |
> 111	|------|------|---------------|---------------------|
> 112	| `useAvatarProviders` | `useAvatarProviders.ts` | Lê estado mascarado dos BYOK providers; invoca `test-api-key` server-side; connect (`.insert`, nunca `.upsert`) / disconnect (RPC); registra os 2 atestados (FR-AC-003/005) | `['avatar-providers', userId]` |
> 113	| `useAvatarConsent` | `useAvatarConsent.ts` | Estado do wizard (3 checkboxes separados); grava `avatar_consents`; aciona identity-verification gate; expõe `persona_type` (FR-AC-030/032) | `['avatar-consents', userId]` |
> 114	| `useAvatarRender` | `useAvatarRender.ts` | Orquestra `generate-voice` + `canvas-execute(talkingHead)`; lê `mco_estimate` (badge); poll de `video_renders` status async (FR-AC-019/020/021) | `['avatar-render', renderId]` |
> 115	| `useAvatarErasure` | `useAvatarErasure.ts` | Dispara `erase-avatar-artifacts` on-revoke; expõe atestado de eliminação (FR-AC-027) | `['avatar-erasure', userId]` |
> 116	| `useAvatarCadence` | `useAvatarCadence.ts` | Opt-in idioma/frequência; dispara ciclo 30d sobre Viral Autopilot; bloqueia config 100%-avatar (FR-AC-033/049/052) | `['avatar-cadence', userId]` |
> 117	
> 118	> **Constraint:** complexidade ciclomática ≤ 10 por hook (NFR-AC-009). Nenhum data-fetch/mutation fora de hooks (NFR-AC-010).
> 119	
> 120	### 2.2 New Display Components (`src/components/`)
> 121	
> 122	| Component | File | Props | Hook consumed |
> 123	|-----------|------|-------|--------------|
> 124	| `AvatarStudioCanvas` | `avatar/AvatarStudioCanvas.tsx` | `{ projectId }` | `useAvatarRender` + `useAvatarStudioStore` |
> 125	| `AvatarIdentityNode` | `avatar/nodes/AvatarIdentityNode.tsx` | `NodeProps` (tier badge, Soul ID/LoRA) | via store / inspector |
> 126	| `VoiceCloneNode` | `avatar/nodes/VoiceCloneNode.tsx` | `NodeProps` (badge "code-switching-safe") | via store |
> 127	| `AvatarScriptNode` | `avatar/nodes/AvatarScriptNode.tsx` | `NodeProps` (badge Brand Voice DNA) | via store |
> 128	| `TalkingHeadNode` | `avatar/nodes/TalkingHeadNode.tsx` | `NodeProps` (mco cost badge + status pulse) | `useAvatarRender` |
> 129	| `AvatarEnhanceNode` | `avatar/nodes/AvatarEnhanceNode.tsx` | `NodeProps` (badge "enhance ≠ identidade") | via store |
> 130	| `ConsentWizard` | `avatar/ConsentWizard.tsx` | `{ onComplete }` | `useAvatarConsent` |
> 131	| `IdentityVerificationGate` | `avatar/IdentityVerificationGate.tsx` | `{ personaType }` | `useAvatarConsent` |
> 132	| `AvatarProvidersCard` | `settings/AvatarProvidersCard.tsx` | `{}` | `useAvatarProviders` |
> 133	| `DisclosureMarkerBadge` | `avatar/DisclosureMarkerBadge.tsx` | `{ removable: false }` | — (display-only, não-removível) |
> 134	| `McoCostBadge` | `avatar/McoCostBadge.tsx` | `{ mcoEstimate }` | — |
> 135	
> 136	> Todos display-only: chamam hooks e renderizam. Texto de UI / toasts / validações em **Português (Brasil)**; código/comentários em English.
> 137	
> 138	### 2.3 New / Extended Edge Functions (`supabase/functions/`)
> 139	
> 140	| Function | Path | Status | Auth | mcoCoins | Vault key names (BYOK per-user — só NOMES) |
> 141	|----------|------|--------|------|----------|----------------|
> 142	| `generate-voice` | `generate-voice/index.ts` | NET-NEW | JWT (user) | **36** (voz EN ~900 chars, recalibrável; Flash/Turbo halva) | `elevenlabs_api_key`, `cartesia_api_key` |
> 143	| `canvas-execute` (kind=`talkingHead`) | `canvas-execute/index.ts` | EXTEND | JWT (user) | **480 Hedra / 2169 OmniHuman / 36 footage-real** (`AVATAR_VIDEO_COST`) | `hedra_api_key`, `omnihuman_api_key`(≡`fal_api_key`), `higgsfield_api_key` |
> 144	| `avatar-identity-train` | `avatar-identity-train/index.ts` | NET-NEW | JWT (user) | n/a (config; regeneração herda custo) | `higgsfield_api_key` |
> 145	| `avatar-script` | `avatar-script/index.ts` | NET-NEW | JWT (user) | **~2** (mapeado a `CONTENT_COST`) | — (usa per-user LLM key via `_shared/llm-fallback.ts`) |
> 146	| `erase-avatar-artifacts` | `erase-avatar-artifacts/index.ts` | NET-NEW | JWT (user) tenant-guarded | n/a | — (chama delete nas APIs terceiras com a key per-user em escopo) |
> 147	| `avatar-reply-engine` | `avatar-reply-engine/index.ts` | NET-NEW | service-role (cron) + per-user OAuth | reply texto = `CONTENT_COST`; reply-com-vídeo = `AVATAR_VIDEO_COST`; cap X separado | `social_credentials.access_token` (per-user OAuth) |
> 148	| `avatar-retention-sweep` | `avatar-retention-sweep/index.ts` | NET-NEW (cron) | service-role | n/a | — |
> 149	| `orchestrate-step` (step=`avatar_generation`) | `orchestrate-step/index.ts` | EXTEND | service-role | prepaid (suprime self-bill — molde OTD-VA-010) | — |
> 150	| `test-api-key` | `test-api-key/index.ts` | EXTEND | JWT (user) | n/a | (testa as novas keys server-side) |
> 151	
> 152	> **JWT stub (toda edge fn user-facing) — ver §5.3.** `avatar-reply-engine` e `avatar-retention-sweep` são cron/service-role: provam `Bearer SB_SECRET_KEY` in-function + resolvem `user_id` server-trusted da linha (nunca do body — molde OTD-VA-008).
> 153	
> 154	### 2.4 Zustand Store Slice
> 155	
> 156	| Slice | Store file | State shape | Actions |
> 157	|-------|------------|-------------|---------|
> 158	| Avatar Studio canvas | `src/store/useAvatarStudioStore.ts` | `{ nodes: AvatarNode[], edges, runState: 'idle'\|'running'\|'done'\|'error', activeRenderId, mcoEstimate }` | `addNode`, `updateNodeStatus`, `setRunState`, `syncFromReactFlow` |
> 159	
> 160	> **Hybrid canvas state (molde `useOrchestrationStore`):** ReactFlow owns positions/drag → debounced 600ms → persisted (`vm_canvas_projects.graph` analog). Zustand owns run state → status sync via `useEffect`. Selectors via `useShallow`; `getState()` dentro de intervalos (zero deps) p/ evitar React 18 cascade (Error #185).
> 161	
> 162	### 2.5 New DB Objects
> 163	
> 164	| Object | Type | Purpose | Migration file |
> 165	|--------|------|---------|---------------|
> 166	| `avatar_identities` | Table | LoRA weights ref + ArcFace canonical embedding + `persona_type` + `verification_passed` (RLS own; storage isolado) | `20260701120000_avatar_clone_ai_biometric.sql` |
> 167	| `voice_profiles` | Table | Voiceprint Vault ref + provider + language (RLS own) | `20260701120000_…biometric.sql` |
> 168	| `avatar_consents` | Table (imutável) | Consent por finalidade (LGPD Art. 11) — versão termo/timestamp/finalidade/IP/user | `20260701120000_…biometric.sql` |
> 169	| `user_api_keys` (+cols) | View/Table ALTER | `hedra_api_key`/`omnihuman_api_key`/`elevenlabs_api_key`/`cartesia_api_key` cifradas | `20260701120500_avatar_byok_keys.sql` |
> 170	| `video_renders` (+cols) | Table ALTER | `composition.avatar` jsonb + `engine IN (…,'hedra','omnihuman','kling')` | `20260701121000_avatar_video_renders.sql` |
> 171	| `erase_avatar_artifacts` | RPC (SECURITY DEFINER) | Cascade tenant-guarded apaga SQL+Storage + dispara delete terceiros (Art. 18) | `20260701121500_erase_avatar_artifacts.sql` |
> 172	| `finalize_avatar_render` | RPC (service-role-only) | Terminal + refund atômico (molde `finalize_video_render`) | `20260701121000_avatar_video_renders.sql` |
> 173	| `autopilot_plans` (CHECK) | Table ALTER | Relaxar `platforms` CHECK p/ +youtube/tiktok/instagram/pinterest | `20260701122000_avatar_autopilot_platforms.sql` |
> 174	| `<table>_embedding_idx` | HNSW index | Cosine similarity sobre `avatar_identities.embedding` (mesh) | `20260701120000_…biometric.sql` |
> 175	
> 176	---
> 177	
> 178	## 3. Data Flow Diagrams
> 179	
> 180	### Use Case A: BYOK fail-closed render de talking-head (FR-AC-004/020/021)
> 181	
> 182	```
> 183	User            useAvatarRender      canvas-execute        DB / RPC            Hedra (BYOK)
> 184	 │                  │                    │                   │                    │
> 185	 │─[Render 60s]────▶│                    │                   │                    │
> 186	 │                  │─[POST JWT,kind]───▶│                   │                    │
> 187	 │                  │                    │─[getUser(JWT)]───▶│ auth.getUser       │
> 188	 │                  │                    │◀─[user ok]────────│                    │
> 189	 │                  │                    │─[resolve key]────▶│ decrypted_user_api │
> 190	 │                  │                    │                   │ _keys auth.uid()   │
> 191	 │                  │                    │◀─[hedra_api_key?]─│                    │
> 192	 │                  │                    │  (null → HTTP 402 hedra_not_configured, ZERO deduct)
> 193	 │                  │                    │─[consent active?]▶│ avatar_consents    │
> 194	 │                  │                    │  (revoked → HTTP 403 fail-closed)      │
> 195	 │                  │                    │─[hybrid posture]──│ ≥1 footage real?   │
> 196	 │                  │                    │  (100%-avatar → HTTP 403 FM-AC-014)    │
> 197	 │                  │                    │─[deduct_mco_coins(user, AVATAR_VIDEO_COST)]▶ RPC (atomic)
> 198	 │                  │                    │  (insufficient → HTTP 402, no media)   │
> 199	 │                  │                    │─[render req]──────────────────────────▶│
> 200	 │                  │                    │◀─[operation_id / async]────────────────│
> 201	 │                  │                    │─[insert video_renders queued]────▶│    │
> 202	 │                  │◀─[200 {render_id, status:queued, transport:poll://}]   │    │
> 203	 │◀─[badge "rendering" + mco debited]───│                    │                    │
> 204	 │   (worker claims render → finalize_avatar_render → bucket video-studio-assets) │
> 205	```
> 206	
> 207	### Use Case B: Consent revoke → erasure cascade (FR-AC-027/031, Art. 18)
> 208	
> 209	```
> 210	Titular         useAvatarErasure     erase-avatar-artifacts    DB/Storage         3rd-party engines
> 211	 │                  │                    │                        │                   │
> 212	 │─[Revoke consent]▶│                    │                        │                   │
> 213	 │                  │─[POST JWT]────────▶│                        │                   │
> 214	 │                  │                    │─[tenant guard auth.uid()]▶ avatar_consents.revoked_at=now()
> 215	 │                  │                    │─[erase_avatar_artifacts RPC]▶ DELETE avatar_identities/voice_profiles
> 216	 │                  │                    │─[Storage API remove prefix user_id/]──▶ bucket
> 217	 │                  │                    │─[delete weights/voice]──────────────────▶│ (best-effort + reconcile)
> 218	 │                  │                    │─[INSERT attestation log]──▶ infra_health_logs (event='avatar_erase')
> 219	 │                  │◀─[200 {erased, attestation_log_id}]        │                   │
> 220	 │◀─[atestado de eliminação]────────────│  (próximo render fail-closed: consent revoked)
> 221	```
> 222	
> 223	### Use Case C: Avatar cadence junction com Viral Autopilot (FR-AC-046..049)
> 224	
> 225	```
> 226	autopilot-cadence-cron → begin_autopilot_cycle (cap+pré-débito atômico, prepaid=true)
> 227	  → orchestrate-step (step=avatar_generation, independente de article_generation)
> 228	      → AVATAR_FLOW_PLATFORMS gate (youtube/tiktok/instagram/linkedin/x — não só wordpress)
> 229	      → enqueue video_renders (engine por source_type) — prepaid suprime self-bill
> 230	      → render → finalize_avatar_render → reshape-pillar (scope=video) → channel_variants
> 231	      → publish gate (C2PA + disclosure não-pulável) → auto-publish → publish-social
> 232	  → finalize_autopilot_cycle (refund crédito-positivo idempotente)
> 233	  → refund_autopilot_video_enqueue (se !enqueued — molde 20260624140000)
> 234	```
> 235	
> 236	---
> 237	
> 238	## 4. API Contract Definitions
> 239	
> 240	> Toda Edge Function valida JWT **antes** de qualquer lógica de negócio (§5.3). Ponto de `deduct_mco_coins` anotado por função. mcoCoins SEMPRE server-side via RPC — nunca client-side (NFR-AC-019).
> 241	
> 242	### `POST /functions/v1/generate-voice` (FR-AC-009)
> 243	
> 244	```typescript
> 245	// Request (Bearer JWT user scope)
> 246	interface GenerateVoiceRequest {
> 247	  script: string                       // input_script
> 248	  language: 'en' | 'pt-BR'             // idioma ÚNICO — nunca code-switch (FR-AC-010)
> 249	  provider: 'elevenlabs' | 'cartesia'
> 250	  voice_profile_id: string             // voice_profiles ref (owner-scoped)
> 251	  project_id?: string
> 252	}
> 253	
> 254	// Response (HTTP 200)
> 255	interface GenerateVoiceResponse {
> 256	  audio_url: string                    // signed URL curta (bucket privado)
> 257	  creative_asset_id: string            // creative_assets (source_module='avatar-studio')
> 258	  mco_charged: number                  // ~36 (recalibrável)
> 259	}
> 260	
> 261	// mcoCoins deduction point:
> 262	// → after JWT + BYOK resolve + consent active check:
> 263	//   await supabase.rpc('deduct_mco_coins', { p_user_id: user.id, p_amount: VOICE_COST })
> 264	// → HTTP 402 { error: 'elevenlabs_not_configured', action: '…/dashboard/settings' } (BYOK fail-closed)
> 265	//   OR HTTP 402 saldo insuficiente; HTTP 403 consent revogado / sentinel block; HTTP 422 idioma misto.
> 266	```
> 267	
> 268	### `POST /functions/v1/canvas-execute` (kind=`talkingHead`) (FR-AC-020/021)
> 269	
> 270	```typescript
> 271	interface TalkingHeadRequest {
> 272	  kind: 'talkingHead'
> 273	  input_face_identity: string          // avatar_identities ref (owner-scoped)
> 274	  input_voice_profile: string          // audio asset ref
> 275	  input_script: string
> 276	  source_type: 'footage_real' | 'avatar_ai'   // dirige roteamento de motor (FR-AC-022)
> 277	  engine?: 'hedra' | 'omnihuman' | 'kling'
> 278	  reference_image_urls?: string[]
> 279	  seed?: number
> 280	}
> 281	
> 282	interface TalkingHeadResponse {        // HTTP 200 / async
> 283	  render_id: string                    // video_renders row
> 284	  status: 'queued'
> 285	  transport: 'poll://'                 // async (NFR-AC-004 — UI nunca bloqueia)
> 286	  mco_estimate: number                 // 480 Hedra / 2169 OmniHuman / 36 footage-real
> 287	}
> 288	
> 289	// mcoCoins deduction point (ORDER MATTERS — fail-closed gates ANTES do débito):
> 290	//   1. JWT validate  2. BYOK resolve (<engine>_api_key per-user → 402 se null)
> 291	//   3. consent active (→403 revoked)  4. hybrid posture (≥1 footage real → 403 se 100%-avatar)
> 292	//   5. await supabase.rpc('deduct_mco_coins', { p_user_id, p_amount: AVATAR_VIDEO_COST[engine] })
> 293	//      → 402 saldo insuficiente SEM gerar mídia  6. enqueue video_renders
> 294	//   AVATAR_VIDEO_COST É SEPARADO de VIDEO_COST (OTD-AC-006 / NFR-AC-019)
> 295	```
> 296	
> 297	### `POST /functions/v1/erase-avatar-artifacts` (FR-AC-027)
> 298	
> 299	```typescript
> 300	interface EraseAvatarRequest {
> 301	  avatar_identity_id?: string
> 302	  voice_profile_id?: string
> 303	  reason: 'revoke' | 'retention_sweep'
> 304	}
> 305	interface EraseAvatarResponse {        // HTTP 200
> 306	  erased: { sql: number; storage: number; third_party: string[] }
> 307	  attestation_log_id: string           // log em infra_health_logs (event='avatar_erase')
> 308	}
> 309	// No mcoCoins. tenant-guarded (403 tenant mismatch). Notificação a terceiros (Art. 18) =
> 310	// best-effort com reconciliação (NFR-AC-008, eventually consistent ≤24h).
> 311	```
> 312	
> 313	### `POST /functions/v1/avatar-identity-train` (FR-AC-012/013/032)
> 314	
> 315	```typescript
> 316	interface AvatarIdentityTrainRequest {
> 317	  training_photo_urls: string[]        // ≥20 (Soul ID) owner-scoped
> 318	  liveness_selfie_url: string          // identity-verification gate (self-clone)
> 319	  persona_type: 'self_clone' | 'fictional'
> 320	  tier: 1 | 2 | 3
> 321	}
> 322	interface AvatarIdentityTrainResponse { // HTTP 200 / async
> 323	  avatar_identity_id: string
> 324	  verification_passed: boolean          // só true após selfie-liveness bater (self-clone)
> 325	  status: 'queued'
> 326	}
> 327	// GATE (ANTES de gerar weights): identity-verification — selfie-liveness vs training photos.
> 328	//   Falha → HTTP 403, NÃO persiste artefato biométrico (clone de terceiro bloqueado por design).
> 329	//   Requer avatar_consents ativos (train_lora + face_embedding) → senão HTTP 403.
> 330	// No deduct aqui; render subsequente cobra. Commercial-license gate bloqueia pesos non-commercial.
> 331	```
> 332	
> 333	### `POST /functions/v1/avatar-reply-engine` (FR-AC-042..045)
> 334	
> 335	```typescript
> 336	// cron/service-role driver: prova Bearer SB_SECRET_KEY in-function; user_id server-trusted da linha.
> 337	interface ReplyEngineCycle {
> 338	  user_id: string                      // server-trusted (NUNCA do body — OTD-VA-008)
> 339	  poll_window: 'mentions'
> 340	}
> 341	// Loop: GET /2/users/:id/mentions (≤300/15min) → dedup 24h UTC → gera reply (cérebro-RAG + sentinel)
> 342	//   → POST /2/tweets (≤100/15min). Pay-per-use: read $0.005 + reply $0.015 / $0.20-com-link.
> 343	//   Cap de gasto per-user (per-plano + diário, molde deepsearch.run). Disclosure deepfake aplicada.
> 344	//   reply-com-link só quando explicitamente monetizado; reply-com-vídeo herda AVATAR_VIDEO_COST.
> 345	```
> 346	
> 347	---
> 348	
> 349	## 5. Security Design
> 350	
> 351	### 5.1 Threat Model (STRIDE por componente)
> 352	
> 353	| Component | Threat | STRIDE Type | Severity | Mitigation |
> 354	|-----------|--------|-------------|----------|------------|
> 355	| `generate-voice` / `canvas-execute` / `avatar-identity-train` | Acesso não-autenticado a síntese paga | Spoofing | High | JWT validation no entry-point (§5.3); 401 sem token válido |
> 356	| `avatar_identities` / `voice_profiles` | Leitura cross-tenant de PII biométrica (weights/voiceprint de outro tenant) | Information Disclosure | **Critical** | RLS own `auth.uid() = user_id` default-deny; FMEA-011; storage prefixo `user_id/` + signed URL curta (NFR-AC-013) |
> 357	| `deduct_mco_coins` (avatar render) | Bypass client-side da dedução | Tampering | **Critical** | RPC server-side only; `AVATAR_VIDEO_COST` ≠ `VIDEO_COST`; zero dedução no cliente (NFR-AC-019) |
> 358	| BYOK key resolution | Fan-out de conta-mestra (service bureau) | Elevation of Privilege | **Critical** | Invariante anti-conta-mestra: toda chamada resolve `auth.uid()`; grep audit zero fan-out (FR-AC-006); Modelo A estrito |
> 359	| `avatar_consents` | Falsificação/edição retroativa de consentimento | Tampering / Repudiation | **Critical** | Tabela imutável (sem UPDATE de conteúdo; só `revoked_at`); versão termo + IP + timestamp (LGPD Art. 11) |
> 360	| `avatar-identity-train` | Clone de terceiro privado real (TikTok bane) | Spoofing (identidade) | **Critical** | Identity-verification gate: selfie-liveness vs fotos de treino ANTES de weights; falha → não persiste (FR-AC-032) |
> 361	| publish gate / `avatar-reply-engine` | Publicar deepfake sem disclosure (EU AI Act / CONAR) | Repudiation / Compliance | **Critical** | Disclosure-by-default não-pulável: C2PA Art.50(2) + deepfake disclosure Art.50(4); render sem disclosure bloqueado (FR-AC-035/036) |
> 362	| `erase-avatar-artifacts` | Erase de artefato de outro tenant | Elevation of Privilege | High | Tenant-guarded `auth.uid()`; 403 tenant mismatch; cascade só na linha do titular |
> 363	| `avatar-script` (RAG) | Prompt injection / jailbreak via mentions ou material RAG | Tampering | High | `_shared/sentinel.ts` (pt-BR + EN famílias f1-f7); sanitização de fonte não-confiável |
> 364	| `avatar-reply-engine` | DoS de gasto (gasto X descontrolado) | Denial of Service | High | Cap de gasto per-user (per-plano + diário); rate-limit poll (≤300/15min); reply-com-link gated |
> 365	| Storage bucket biométrico | Vazamento por URL longa/pública | Information Disclosure | High | Bucket privado; signed URL curta owner-scoped; segregado de `mcorch_nodes`/conteúdo (FR-AC-026) |
> 366	| `voice_profiles` / Art. 5(1)(g) | Inferir características sensíveis de pessoas dos vídeos | Information Disclosure | Medium | Red-line por design: uso restrito à identidade do próprio titular consentido (FR-AC-029) |
> 367	
> 368	### 5.2 RLS Policy Definitions
> 369	
> 370	```sql
> 371	-- avatar_identities (biometric — RLS own default-deny)
> 372	ALTER TABLE avatar_identities ENABLE ROW LEVEL SECURITY;
> 373	
> 374	CREATE POLICY "avatar_identities_select_own"
> 375	  ON avatar_identities FOR SELECT USING (user_id = auth.uid());
> 376	CREATE POLICY "avatar_identities_insert_own"
> 377	  ON avatar_identities FOR INSERT WITH CHECK (user_id = auth.uid());
> 378	CREATE POLICY "avatar_identities_update_own"
> 379	  ON avatar_identities FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());
> 380	-- DELETE só via RPC erase_avatar_artifacts (SECURITY DEFINER tenant-guarded) — sem policy DELETE direta.
> 381	
> 382	-- voice_profiles — idêntico padrão own.
> 383	-- avatar_consents — SELECT/INSERT own; SEM UPDATE de conteúdo (imutável); revoke = UPDATE só de revoked_at.
> 384	CREATE POLICY "avatar_consents_select_own"
> 385	  ON avatar_consents FOR SELECT USING (user_id = auth.uid());
> 386	CREATE POLICY "avatar_consents_insert_own"
> 387	  ON avatar_consents FOR INSERT WITH CHECK (user_id = auth.uid());
> 388	CREATE POLICY "avatar_consents_revoke_own"
> 389	  ON avatar_consents FOR UPDATE USING (user_id = auth.uid())
> 390	  WITH CHECK (user_id = auth.uid());  -- trigger restringe colunas mutáveis a revoked_at
> 391	```
> 392	
> 393	### 5.3 JWT Validation Points
> 394	
> 395	Toda Edge Function user-facing segue o stub (CISSP CBK — authentication at trust boundary):
> 396	
> 397	```typescript
> 398	const authHeader = req.headers.get('Authorization')
> 399	if (!authHeader) return json({ error: 'unauthorized' }, 401)
> 400	const { data: { user }, error } = await supabase.auth.getUser(
> 401	  authHeader.replace('Bearer ', '')
> 402	)
> 403	if (error || !user) return json({ error: 'unauthorized' }, 401)
> 404	// → só depois: BYOK resolve → consent check → hybrid posture → deduct_mco_coins → business logic
> 405	```
> 406	
> 407	Funções cron/service-role (`avatar-reply-engine`, `avatar-retention-sweep`, `orchestrate-step`):
> 408	
> 409	```typescript
> 410	const auth = req.headers.get('Authorization') ?? ''
> 411	if (auth !== `Bearer ${Deno.env.get('SB_SECRET_KEY')}`) return json({ error: 'forbidden' }, 403)
> 412	// user_id resolvido server-trusted da linha (video_renders / autopilot_cycles) — NUNCA do body (OTD-VA-008)
> 413	```
> 414	
> 415	### 5.4 Secrets Inventory (NOMES de vault key — nunca valores)
> 416	
> 417	| Secret Name | Tipo | Used In | Resolution | Rotation Policy |
> 418	|-------------|------|---------|------------|----------------|
> 419	| `hedra_api_key` | BYOK per-user (`user_api_keys`, Vault) | `canvas-execute(talkingHead)` | `auth.uid()` decrypted view; 402 se null | Per-user (titular rotaciona) |
> 420	| `omnihuman_api_key` (≡ `fal_api_key`) | BYOK per-user (Vault) | `canvas-execute(talkingHead)` re-lip-sync | `auth.uid()`; 402 se null | Per-user |
> 421	| `higgsfield_api_key` | BYOK per-user (Vault — já existe) | `avatar-identity-train`, Kling render | `auth.uid()`; 402 se null | Per-user |
> 422	| `elevenlabs_api_key` | BYOK per-user (Vault) | `generate-voice` | `auth.uid()`; 402 se null | Per-user |
> 423	| `cartesia_api_key` | BYOK per-user (Vault) | `generate-voice` (real-time Sonic) | `auth.uid()`; 402 se null | Per-user |
> 424	| `MAGNIFIC_ORG_API_KEY` | **ORG-key (system-level, NÃO per-user)** | `avatar-enhance` / `canvas-execute(avatarEnhance)` | env vault (custo interno MCORCH; per-user PROIBIDO sem consent escrito) | Org-managed |
> 425	| `social_credentials.access_token` | per-user OAuth (Vault) | `avatar-reply-engine`, `publish-social` | `auth.uid()` / linha do titular | Per-user OAuth refresh |
> 426	| `SB_SECRET_KEY` | service-role | cron/service-role fns | env | System-managed |
> 427	| `MESH_EMBED_OPENROUTER_KEY` | system (mesh) | `embed-mcorch-node` (trigger biométrico) | env | System-managed |
> 428	
> 429	> ⚠️ **NUNCA commit de valor de secret.** Só NOMES de vault key aparecem na documentação. BYOK per-user fail-closed: zero `Deno.env.get('<provider>')` em fluxo user-facing de síntese (NFR-AC-012). Magnific é a única exceção declarada (org-key interna — `00c §F1`).
> 430	
> 431	---
> 432	
> 433	## 6. Infrastructure Touchpoints
> 434	
> 435	| Infrastructure | Usage | Impact |
> 436	|----------------|-------|--------|
> 437	| **Render worker** (`scripts/avatar-render-bridge.ts`, molde `video-bridge.ts` + systemd `avatar-render-bridge.service`) | Claim atômico de `video_renders` (engine ∈ hedra/omnihuman/kling) → chama API BYOK per-user → upload bucket `video-studio-assets` (prefixo `user_id/`) → `finalize_avatar_render` → kick `reshape-pillar scope=video` | Off-band render async (NFR-AC-004); UI nunca bloqueia; refund atômico em fail |
> 438	| **Storage bucket** `video-studio-assets` (+ prefixo biométrico isolado) | Artefatos biométricos (LoRA weights, voiceprint refs) em prefixo privado `user_id/`; signed URL curta owner-scoped | Segregação per-tenant (FR-AC-026); nenhuma URL pública |
> 439	| **Supabase Vault** (`vault.secrets` via `vault_upsert_secret`) | Voiceprints cifrados + BYOK keys per-user (encrypt trigger idempotente, recipe `20260622210000`) | PII biométrica nunca em claro; masked view `••••` |
> 440	| `mcorch_chroma` (ChromaDB port 8001) | Não usado diretamente — RAG do cérebro-clonado roda sobre `mcorch_nodes` + pgvector HNSW (GraphRAG), não ChromaDB | n/a (mesh nativa Supabase é o substrato; ChromaDB permanece para outras cargas) |
> 441	| `embed-mcorch-node` trigger | Toda inserção em `avatar_identities` (e nó de observação no 1º render bem-sucedido) gera embedding mesh | Knowledge Mesh node no 1º sucesso (Mesh Connection Mandate) |
> 442	| `infra_health_logs` | Novos events: `avatar_render`, `avatar_voice`, `avatar_erase`, `avatar_reply`, `avatar_identity_gate` — `service='avatar-clone-ai'`, cada path (success/degraded/error) | Watchdog telemetry (NFR-AC-020); allowlist no chokepoint p/ não vazar per-tenant na tabela global-read |
> 443	| `pg_cron` | Drivers `avatar-reply-engine` (poll mentions) + `avatar-retention-sweep` (diário) — encadeados sem quebrar crons existentes | Reply loop + erasure por inatividade (FR-AC-028/042) |
> 444	| `mega-brain-daemon` (watchdog) | Monitora uptime do pipeline avatar (render→finalize) → SLO 99.5%/mês | Self-heal + telemetria de degradação |
> 445	
> 446	---
> 447	
> 448	## 7. Migration Stubs
> 449	
> 450	```sql
> 451	-- Migration: 20260701120000_avatar_clone_ai_biometric.sql
> 452	-- /security-review OBRIGATÓRIO antes do commit (FMEA-011 cross-tenant biometric leak).
> 453	
> 454	CREATE TABLE avatar_identities (
> 455	  id                   uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 456	  user_id              uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 457	  project_id           uuid REFERENCES projects(id) ON DELETE CASCADE,
> 458	  persona_type         text NOT NULL CHECK (persona_type IN ('self_clone','fictional')),
> 459	  tier                 smallint NOT NULL CHECK (tier IN (1,2,3)),
> 460	  identity_storage_key text NOT NULL,                 -- bucket privado, prefixo user_id/
> 461	  arcface_threshold    numeric NOT NULL,              -- calibrado FAR/FRR/EER (NUNCA hardcode)
> 462	  verification_passed  boolean NOT NULL DEFAULT false,-- true só após identity-verification gate
> 463	  embedding            vector(768),                   -- mesh embedding (trigger embed-mcorch-node)
> 464	  created_at           timestamptz DEFAULT now() NOT NULL,
> 465	  updated_at           timestamptz DEFAULT now() NOT NULL
> 466	);
> 467	
> 468	CREATE TABLE voice_profiles (
> 469	  id                   uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 470	  user_id              uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 471	  project_id           uuid REFERENCES projects(id) ON DELETE CASCADE,
> 472	  provider             text NOT NULL CHECK (provider IN ('elevenlabs','cartesia')),
> 473	  voiceprint_vault_ref text NOT NULL,                 -- cifrado no Vault (nunca valor em claro)
> 474	  language             text NOT NULL CHECK (language IN ('en','pt-BR')),  -- sem code-switch
> 475	  created_at           timestamptz DEFAULT now() NOT NULL
> 476	);
> 477	
> 478	CREATE TABLE avatar_consents (                          -- imutável (sem UPDATE de conteúdo)
> 479	  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 480	  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 481	  purpose         text NOT NULL CHECK (purpose IN ('train_lora','face_embedding','voice_clone')),
> 482	  term_version    text NOT NULL,
> 483	  consent_granted boolean NOT NULL,                    -- true só com checkbox específico
> 484	  ip_address      inet NOT NULL,
> 485	  revoked_at      timestamptz,                         -- null=ativo; preenchido=fail-closed
> 486	  created_at      timestamptz DEFAULT now() NOT NULL
> 487	);
> 488	
> 489	ALTER TABLE avatar_identities ENABLE ROW LEVEL SECURITY;
> 490	ALTER TABLE voice_profiles    ENABLE ROW LEVEL SECURITY;
> 491	ALTER TABLE avatar_consents   ENABLE ROW LEVEL SECURITY;
> 492	-- (políticas RLS own de §5.2; DELETE só via erase_avatar_artifacts RPC)
> 493	
> 494	-- Trigger imutabilidade avatar_consents: bloqueia UPDATE de qualquer coluna != revoked_at.
> 495	CREATE OR REPLACE FUNCTION enforce_avatar_consent_immutable() RETURNS trigger
> 496	  LANGUAGE plpgsql SET search_path = '' AS $$
> 497	BEGIN
> 498	  IF (to_jsonb(NEW) - 'revoked_at') IS DISTINCT FROM (to_jsonb(OLD) - 'revoked_at') THEN
> 499	    RAISE EXCEPTION 'avatar_consents é imutável (só revoked_at pode mudar)';
> 500	  END IF;
> 501	  RETURN NEW;
> 502	END $$;
> 503	CREATE TRIGGER trg_avatar_consent_immutable BEFORE UPDATE ON avatar_consents
> 504	  FOR EACH ROW EXECUTE FUNCTION enforce_avatar_consent_immutable();
> 505	
> 506	-- HNSW index (mesh similarity sobre o embedding canônico):
> 507	CREATE INDEX avatar_identities_embedding_idx
> 508	  ON avatar_identities USING hnsw (embedding vector_cosine_ops)
> 509	  WITH (m = 16, ef_construction = 64);
> 510	
> 511	-- embed-mcorch-node trigger (mesh node no insert):
> 512	CREATE TRIGGER trg_avatar_identities_embed AFTER INSERT ON avatar_identities
> 513	  FOR EACH ROW EXECUTE FUNCTION trigger_embed_mcorch_node();
> 514	```
> 515	
> 516	```sql
> 517	-- Migration: 20260701120500_avatar_byok_keys.sql  (recipe 20260622210000)
> 518	-- ALTER user_api_keys + colunas cifradas; encrypt trigger + masked view + INSTEAD OF + decrypted LEFT JOIN.
> 519	-- Colunas: hedra_api_key, omnihuman_api_key (≡ fal_api_key), elevenlabs_api_key, cartesia_api_key.
> 520	-- higgsfield_api_key JÁ EXISTE — confirmar/reusar (não recriar).
> 521	-- INSTEAD OF = UPDATE-first/INSERT-if-not-found + guard de tenant (fix double-fire 20260602130000).
> 522	```
> 523	
> 524	```sql
> 525	-- Migration: 20260701121000_avatar_video_renders.sql
> 526	-- ALTER video_renders ADD composition jsonb avatar branch; relax engine CHECK p/ +hedra/omnihuman/kling.
> 527	-- RPC finalize_avatar_render (service-role-only, molde finalize_video_render): terminal + refund atômico.
> 528	```
> 529	
> 530	```sql
> 531	-- Migration: 20260701121500_erase_avatar_artifacts.sql
> 532	-- RPC erase_avatar_artifacts (SECURITY DEFINER, search_path='', service/owner tenant-guarded):
> 533	-- cascade DELETE avatar_identities/voice_profiles do titular + retorna counts; Storage API remove
> 534	-- (não-SQL — OTD-VM-026 lição); atestado em infra_health_logs. EXECUTE revogado de anon/authenticated
> 535	-- exceto self-scoped. Notificação a terceiros é orquestrada na edge fn (não no RPC).
> 536	```
> 537	
> 538	```sql
> 539	-- Migration: 20260701122000_avatar_autopilot_platforms.sql
> 540	-- ALTER autopilot_plans relax CHECK platforms p/ +youtube/tiktok/instagram/pinterest
> 541	-- (preserva FK composta tenant-escopada de 20260620120000; NÃO dropa RESTRICTIVE no-delete).
> 542	```
> 543	
> 544	---
> 545	
> 546	## 8. Open Technical Decisions
> 547	
> 548	> **REUSO dos OTD-AC-* dos seeds** (`00-blueprint §8` + `00b §6` + `00c` Fechamento), agora com a recomendação-semente já resolvida pela Fatia 0. Os que a Fatia 0 fechou aparecem como `FECHADO` com a decisão de implementação cravada; os que restam carregam SLA. A Pattern Conformance Declaration completa (21 padrões agênticos) vive em `09-pattern-conformance.md`.
> 549	
> 550	| ID | Description | Option A | Option B | Recommendation (resolvida) | Owner |
> 551	|----|-------------|----------|----------|----------------------------|-------|
> 552	| OTD-AC-001 | Motor talking-head | BYOK self-serve (Hedra/OmniHuman/Higgsfield) | Motor próprio soberano / HeyGen partnership | **FECHADO** — BYOK self-serve; roteamento por `source_type` (footage_real→OmniHuman 1.5 re-lip-sync; avatar_ai→Hedra/Kling). Motor próprio + HeyGen = futuro diferido | Sovereign |
> 553	| OTD-AC-004 | Limiar do Identity Gate | Hardcode (0.95 / 0.7-0.8) | Calibrar empírico FAR/FRR/EER | **FECHADO** — calibração empírica em frames reais do Gabriel; limiar é coluna `arcface_threshold` (config), NÃO constante; reconhece verification-cosine vs CSIM generativo | Sovereign + engineer |
> 554	| OTD-AC-006 | Cost model do render avatar | Reusar `VIDEO_COST` | `AVATAR_VIDEO_COST` separado | **FECHADO (datado)** — `AVATAR_VIDEO_COST` ≠ `VIDEO_COST`; Hedra 480 / OmniHuman 2169 / footage-real 36 mco/60s; **recalibrar ao vivo no momento da implementação** (ElevenLabs Flash/Turbo halva voz; Hedra SD halva render) | Sovereign + engineer |
> 555	| OTD-AC-008 | C2PA × determinismo sha256 (NFR-VS-016) | Embed C2PA quebra determinismo | Embed sem quebrar / waiver | **ELEVADO A REQUISITO LEGAL** (Art. 50(2), vigência 02/08/2026) — spike FR-AC-037 ANTES de selar render-core; decisão (embed determinístico OU waiver documentado) registrada na migration de render | engineer |
> 556	| OTD-AC-009 | Reply engine do X | Fatia-9-gated | Escopo core | **FECHADO (core)** — pay-per-use (read $0.005 / reply $0.015 / $0.20-com-link), polling de mentions, cap per-user; "tier acessível" REFUTADO; trilha de implementação = Fatia 9 | Sovereign |
> 557	| OTD-AC-010 | Consent + identity-verification | OTD diferível | Gate de lançamento | **FECHADO (gate de lançamento)** — consent por-render fail-closed + identity-verification self-clone + erasure on-revoke + segregação de storage | Sovereign |
> 558	| OTD-AC-011 | BYOK legal por provider | Conta-mestra multiplexada | Modelo A per-user fail-closed | **FECHADO condicional** — Modelo A estrito (invariante anti-conta-mestra); Magnific=org-key interna, HeyGen=partnership ficam DE FORA do BYOK puro. **Gaps Lei 1 abertos:** OTD-AC-011-a (Magnific §3 API), -b (ElevenLabs resale-clause), -c (OmniHuman titular fal.ai vs BytePlus) — consulta jurídica formal não-AI **antes do GA comercial** (não bloqueia piloto Usuário Zero) | Sovereign + jurídico |
> 559	| OTD-AC-012 | Idioma / frequência + custo 2× | Render ×N por idioma | 1 trilha-fonte + auto-dub | **FECHADO** — 1 trilha-fonte EN + auto-dub nativo da plataforma (alcance, $0/idioma); voz PT clonada + re-lip-sync = premium opt-in (auto-dub NÃO dispensa voz própria — REFUTADO); idioma/frequência per-user opt-in sem duplicação forçada | Sovereign |
> 560	| OTD-AC-013 | North-Star de marca + trigger de migração de Owner | Indefinida | Definida + atingida → Owner migra a marketing-growth | **ABERTO (SLA: pós-MVP)** — gate de fracasso honesto: não julgar morto antes de ~100 posts com cadência sustentada (comp: ~3 meses p/ sair do 200-view jail) | Sovereign |
> 561	| OTD-AC-014 | Tensão RAMP anti-flag × 12+ uploads/mês | Volume alto desde D1 | Ramp por-canal independente | **FECHADO** — ramp por-canal independente (S1-3 suave anti-flag; steady-state S4+); volume agregado cross-canal cresce mesmo com cada canal em ramp | Sovereign + marketing-growth |
> 562	| OTD-AC-011-a | Magnific §3 "API Services" (truncada) | — | — | **ABERTO (SLA antes do GA)** — ler literalmente a §3; confirmar se existe chave per-end-user. Default seguro = org-key interna (não pass-through) | jurídico |
> 563	| OTD-AC-011-b | ElevenLabs resale-clause | — | — | **ABERTO (SLA antes do GA)** — confirmar palavra-por-palavra a frase de resale do `terms-of-use` | jurídico |
> 564	| OTD-AC-011-c | OmniHuman titular contratual | fal.ai = Customer (ok) | BytePlus End-User (proibido §4(b)(ii)) | **ABERTO (SLA antes do GA)** — confirmar com fal.ai/ByteDance se user-com-conta-própria-via-app-terceiro é "Customer" | jurídico |
> 565	
> 566	---
> 567	
> 568	## 9. Survival Laws & Mesh Connection (design-level compliance)
> 569	
> 570	- **Lei 1 (Materiality):** todo número de custo/mco neste SDD é derivado aritmético do modelo 4×-floor sobre preços datados (`00c §F5`) — **recalibrar ao vivo** na implementação (OTD-AC-006). Nenhum UUID/hash/contagem fabricado; provas materiais (build/test/`/security-review` SAFE) exigidas no `/handoff` de cada Fatia.
> 571	- **Lei 2 (Process):** SOP `docs/processes/avatar-biometric-retention-erasure.md` (molde `vision-mcp-pat-and-erasure.md`) **antes** de codar sweep/erasure (FR-AC-027/028). SOPs irmãos: `avatar-byok-credential-resolution.md`, `avatar-identity-verification-gate.md`, `avatar-disclosure-c2pa-gate.md`.
> 572	- **Lei 4 (ORO):** triplet declarado no cabeçalho; Owner = Sovereign até a North-Star (OTD-AC-013).
> 573	- **Mesh Connection Mandate:** nó de observação na Knowledge Mesh no 1º render bem-sucedido; entrada em `infra_health_logs` em todo path de falha; traceability link a FR-AC/PR-AC; link à Pattern Conformance Declaration (`09-pattern-conformance.md`) — os padrões implementados (Tool Use, Self-Correction/Reflection no Identity Gate, RAG no cérebro-clonado, Multi-step Orchestration, Guardrails/Safety, Conversational loop no reply engine) declarados ali.
> 574	
> 575	---
> 576	
> 577	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 578	
> ```

## 🤖 Claude *(04:51:40)*


## 🤖 Claude *(04:51:41)*

Large module — 54 FRs across multiple slices. I need to pin down exactly what Fatia 1 shipped and what Fatia 2 is. Let me find the slice roadmap and the current code state.

## 🤖 Claude *(04:51:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== Fatia mentions across BoK ===\"; grep -rn \"Fatia [0-9]\" docs/bok/avatar-clone-ai/*.md | grep -iE \"fatia [1-9]\" | head -40",
  "description": "Find slice/Fatia roadmap in BoK"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Fatia mentions across BoK ===
> docs/bok/avatar-clone-ai/00b-fatia0-viability-format-probe.md:153:| **Fatia 7 (repurpose nativo)** | reshaper p/ avatar | **+requisito multi-audio track output** (FR de faixa de áudio nativa por idioma). |
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:22:3. **OTD-AC-009 reply engine do X → ESCOPO CORE AGORA.** Sobe de Fatia 9-gated para fatia core.
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:337:2. **Embed C2PA no render = REQUISITO LEGAL** (EU Art.50, machine-readable, + auto-label TikTok), NÃO polish — move da Fatia 6 para FR de compliance first-class. ⚠️ resolve com OTD-AC-008 (C2PA vs determinismo sha256 NFR-VS-016) ANTES de selar a arquitetura de render.
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:356:| OTD-AC-009 | Motor de reply do X (real-time agent loop) | **✅ RESOLVIDO (Sovereign 2026-06-29): ESCOPO CORE AGORA.** Agent loop conversacional real-time (monitorar mentions → reply do "cérebro clonado" → postar em minutos) entra no core; sobe de Fatia 9-gated. Padrão agêntico Conversational/Reactive loop = **implementado**, não candidato |
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:420:- **Fatia 1 — BYOK credenciais avatar.** Migration `user_api_keys` (heygen/magnific/elevenlabs/cartesia) + UI Settings + test-api-key + lookup helper, **gated em F1 (ToS pass-through por provider)**.
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:421:- **Fatia 2 — Nó `voiceClone`.** `generate-voice` edge fn (ElevenLabs Multilingual-v2-PVC OU IVC-v3) + nó Canvas + creative_assets. **Validar code-switching PT-BR↔EN (FM-AC-013) + voice_profiles RLS (§4.4b).**
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:422:- **Fatia 3 — Nó `avatarIdentity` + Identity Gate.** Soul ID/LoRA (⚠️ resolver TREINO-via-API) + ArcFace cosine gate (estende Vision QA, limiar CALIBRADO via FAR/FRR). `avatar_identities` RLS own + storage isolado.
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:423:- **Fatia 4 — Nó `avatarScript` (cérebro clonado).** RAG sobre `mcorch_nodes` + Brand Voice DNA quantificado (PT-BR/EN).
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:424:- **Fatia 5 — Nó `talkingHead` + `avatarEnhance`.** Motor por-vídeo-referência (OTD-AC-001 resolvido) + Magnific Relight/upscale (ordem: identidade ANTES de enhance) → MP4 9:16. Reusa video_renders/finalize.
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:425:- **Fatia 6 — C2PA + disclosure/consent gate.** Embed manifest no render (**REQUISITO LEGAL**, spike determinismo OTD-AC-008) + gate de publish não-pulável + identity-verification self-clone (§5.4).
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:426:- **Fatia 7 — Repurpose nativo por canal.** Estender `reshape-pillar`/`channel_variants` p/ avatar (campos de script + asset_key vídeo); branches vídeo LinkedIn/X net-new em publish-social. (Caminho reshaper→publish-social JÁ existe — §6.2.)
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:427:- **Fatia 8 — JUNÇÃO com Viral Autopilot.** **Relaxar CHECK de `autopilot_plans.platforms`** (add yt/tiktok/ig/pinterest) + estender `VIDEO_FLOW_PLATFORMS`→`AVATAR_FLOW_PLATFORMS` + step `avatar_generation` independente do article-flow + billing avatar separado + refund idempotente. Cadência 30-dias com RAMP server-side (números ilustrativos).
> docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md:428:- **Fatia 9 (gated, decisão Sovereign) — motor de REPLY do X** (OTD-AC-009, novo agent loop real-time) + X Premium.
> docs/bok/avatar-clone-ai/04-frd.md:46:### 2.1 BYOK & Tenancy (Fatia 1)
> docs/bok/avatar-clone-ai/04-frd.md:58:### 2.2 Voice Clone — nó `voiceClone` (Fatia 2)
> docs/bok/avatar-clone-ai/04-frd.md:67:### 2.3 Identity-lock & Identity Gate — nó `avatarIdentity` (Fatia 3)
> docs/bok/avatar-clone-ai/04-frd.md:77:### 2.4 Cloned-brain script — nó `avatarScript` (Fatia 4)
> docs/bok/avatar-clone-ai/04-frd.md:84:### 2.5 Talking-head render & enhance — nós `talkingHead` / `avatarEnhance` (Fatia 5)
> docs/bok/avatar-clone-ai/04-frd.md:124:### 2.9 Vision QA (Fatia 5)
> docs/bok/avatar-clone-ai/04-frd.md:130:### 2.10 Multilingual reach (Fatia 7)
> docs/bok/avatar-clone-ai/04-frd.md:137:### 2.11 X reply engine (escopo core — Fatia 9 de implementação)
> docs/bok/avatar-clone-ai/04-frd.md:146:### 2.12 Cadence & Viral Autopilot junction (Fatia 8)
> docs/bok/avatar-clone-ai/05-sdd.md:556:| OTD-AC-009 | Reply engine do X | Fatia-9-gated | Escopo core | **FECHADO (core)** — pay-per-use (read $0.005 / reply $0.015 / $0.20-com-link), polling de mentions, cap per-user; "tier acessível" REFUTADO; trilha de implementação = Fatia 9 | Sovereign |
> docs/bok/avatar-clone-ai/03-prd.md:95:| PR-AC-005 | **Módulo Avatar per-user BYOK PURO (Modelo A)** no Canvas Studio: 5 nós tipados (`avatarIdentity`, `voiceClone`, `avatarScript`, `talkingHead`, `avatarEnhance`) via recipe do registry; chaves cifradas no Vault; resolução fail-closed → HTTP 402 `<service>_not_configured` | P1, P2, P3 | BR-AC-005, BR-AC-026 | XL | n/a (config; render cobra na execução) | Fatia 1; nunca chave global em fluxo user-facing |
> docs/bok/avatar-clone-ai/03-prd.md:97:| PR-AC-014 | **Wizard de consentimento biométrico** explícito/destacado/específico: 3 checkboxes separados (treinar LoRA / extrair face embedding / clonar voz); grava `avatar_consents` imutável RLS per-user (versão do termo, timestamp, finalidade, IP, user) | P1, P2, P3 | BR-AC-014 | L | n/a | LGPD Art. 11; ausência bloqueia treino; Fatia 3/6 |
> docs/bok/avatar-clone-ai/03-prd.md:101:| PR-AC-009 | **Nó `voiceClone`** + edge fn `generate-voice` (net-new, paralelo a `generate-image`): ElevenLabs PVC/IVC + Cartesia; BYOK per-user; registra em `creative_assets`; deduz custo de voz via RPC | P1, P2 | BR-AC-009 | L | **36 mco** (voz EN ~900 chars × $0,182/1k, 4×-floor) | Fatia 2; chave ausente → 402 `elevenlabs_not_configured`; validar code-switching PT↔EN (FM-AC-013) |
> docs/bok/avatar-clone-ai/03-prd.md:102:| PR-AC-011 | **Nó `avatarIdentity` + Identity Gate**: Soul ID/LoRA por-usuário → ArcFace cosine vs embedding canônico → fail-and-regenerate abaixo do limiar **calibrado empiricamente** (FAR/FRR/EER); nunca hardcode 0.95 nem 0.7-0.8 | P1, P2, P3 | BR-AC-011 | XL | n/a (regeneração herda custo do render) | Fatia 3; estende Vision QA; OTD-AC-004 |
> docs/bok/avatar-clone-ai/03-prd.md:103:| PR-AC-010 | **Nó `avatarScript`** (cérebro clonado): RAG sobre `mcorch_nodes` + Brand Voice DNA quantificado (PT-BR/EN); sentinel anti-jailbreak; fallback de provider per-user→sistema | P1, P2, P3 | BR-AC-010 | M | ~2 mco (mapear a CONTENT_COST; texto ~free) | Fatia 4; ancora saídas em material aprovado (anti-alucinação) |
> docs/bok/avatar-clone-ai/03-prd.md:104:| PR-AC-008 | **Nó `talkingHead`** (render avatar-IA image+audio→MP4 9:16) via `canvas-execute` (cost-gate + daily-cap); deduz `AVATAR_VIDEO_COST` via RPC `deduct_mco_coins`; saldo insuficiente → HTTP 402 | P1, P2 | BR-AC-008, BR-AC-023 | XL | **Hedra 480 mco** / **OmniHuman 1.5 2169 mco** (60s, recalibrável) | Fatia 5; reusa video_renders/finalize; `AVATAR_VIDEO_COST` ≠ `VIDEO_COST` |
> docs/bok/avatar-clone-ai/03-prd.md:106:| PR-AC-019 | **Nó `avatarEnhance`** (Magnific Relight/upscale, polish FINAL, nunca autor de identidade) + **erase/retention RPC** on-revoke (molde `erase_vision_artifacts`): apaga storage MCORCH + dispara delete nos motores terceiros (Art. 18) + retention-sweep por inatividade configurável | P1, P2, P3 | BR-AC-019 | L | n/a (enhance = conta-org interna) | Fatia 5/6; ordem identidade-ANTES-de-enhance (FM-AC-003); prazo parametrizável (NÃO hard-code) |
> docs/bok/avatar-clone-ai/03-prd.md:114:| PR-AC-015 | **Consentimento por-render fail-closed**: cada render grava consentimento-ativo derivado do opt-in vigente; revogado ⇒ render bloqueado | P1, P2, P3 | BR-AC-015 | M | n/a | Fatia 6; revogação materialmente efetiva |
> docs/bok/avatar-clone-ai/03-prd.md:115:| PR-AC-020 | **Disclosure-by-default não-pulável** no publish E no reply engine: C2PA machine-readable (Art. 50(2)) + disclosure deepfake visível (Art. 50(4)) no 1º contato + identificação de influencer virtual (CONAR); bio declara avatar | P1, P2, P3 | BR-AC-020 | L | n/a | Fatia 6; gate de publish (mesma severidade do CF WordPress); rotular NÃO reduz reach |
> docs/bok/avatar-clone-ai/03-prd.md:119:| PR-AC-024 | **Cadência 30 dias** sobre o Viral Autopilot: relaxar `autopilot_plans.platforms` CHECK + `VIDEO_FLOW_PLATFORMS`→`AVATAR_FLOW_PLATFORMS` + step `avatar_generation` independente; ramp anti-flag por-canal (S1-3 suave, S4+ steady); funil S1→S4; 1 pilar → N variantes nativas; tie-in afiliado ≤20% | P1, P2 | BR-AC-024 | XL | por render de cada variante (PR-AC-008/009) | Fatia 7/8; junção final; OTD-AC-014 |
> docs/bok/avatar-clone-ai/03-prd.md:122:### Could Have (Future — Fatia 9 gated + extensões)
> docs/bok/avatar-clone-ai/03-prd.md:126:| PR-AC-013 | **Reply engine do X** core: agent loop poll `GET /2/users/:id/mentions` → reply contextual do cérebro-clonado → posta em minutos; pay-per-use; cap de gasto per-user (per-plano + diário); separar reply-engajamento (sem link) de post-monetizado (com link, $0.20) | P1 | BR-AC-013 | XL | reply texto = geração de texto; reply-com-vídeo herda `AVATAR_VIDEO_COST`; cap X separado | OTD-AC-009 resolvido = CORE (não Fatia-9-gated p/ escopo; trilha de implementação Fatia 9); "tier acessível" REFUTADO |
> docs/bok/avatar-clone-ai/03-prd.md:144:> Mapeamento direto das Fatias do roadmap (`00-blueprint §9`). MVP = Fatias 1-5 (avatar gera 1 short EN híbrido). v1.0 = Fatias 6-8 (compliance gate + cadência + repurpose). Futuro = Fatia 9 + extensões. Fatia 0 (BoK + verify adversarial) = **Done** (gate GO-HYBRID fechado).
> docs/bok/avatar-clone-ai/03-prd.md:147:**Target date:** 1º ciclo 30d pago E2E concluído em até **90 dias** do início da Fatia 1 (BO-001).
> docs/bok/avatar-clone-ai/03-prd.md:153:**Adds:** PR-AC-002, PR-AC-003, PR-AC-015, PR-AC-020, PR-AC-021, PR-AC-022, PR-AC-024, PR-AC-027 — compliance gate não-pulável (C2PA + disclosure deepfake, Fatia 6) + repurpose nativo por canal (Fatia 7) + junção com Viral Autopilot e cadência 30d com ramp (Fatia 8); 1 trilha-fonte EN + auto-dub; gates de publicação per-canal (ação Sovereign).
> docs/bok/avatar-clone-ai/03-prd.md:156:### Future Scope (Fatia 9 + extensões)
> docs/bok/avatar-clone-ai/03-prd.md:157:**Items:** PR-AC-013 (reply engine X — escopo já CORE por OTD-AC-009, trilha de implementação Fatia 9), PR-AC-004 (trilha PT-BR premium re-lip-sync), PR-AC-023 (cost model mapeado a planos B2B2C), PR-AC-025 (idioma/frequência opt-in), PR-AC-028 (baseline + atribuição).
> ```

## 🤖 Claude *(04:51:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== existing avatar code ===\"; find src -iname \"*avatar*\" 2>/dev/null; echo \"--- avatar hooks/lib ---\"; ls -la src/lib/avatar.ts src/hooks/useAvatar*.ts src/store/useAvatarStudioStore.ts 2>/dev/null; echo \"--- avatar edge fns ---\"; ls supabase/functions/ | grep -i avatar; echo \"--- generate-voice ---\"; ls supabase/functions/ | grep -i voice; echo \"--- avatar migrations ---\"; ls supabase/migrations/ | grep -iE \"avatar|2026063|2026070\"",
  "description": "Inventory existing avatar code + migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === existing avatar code ===
> src/components/ui/avatar.tsx
> --- avatar hooks/lib ---
> --- avatar edge fns ---
> --- generate-voice ---
> --- avatar migrations ---
> 20260630000000_user_api_keys_avatar_byok.sql
> 20260630010000_kanban_task_source_external_key.sql
> ```

## 🤖 Claude *(04:53:26)*


## 🤖 Claude *(04:53:29)*

Now I have the slice map. **Fatia 1 (DONE):** BYOK keys migration `20260630000000` (hedra/cartesia/fal) + Settings UI — confirmed no avatar hooks/edge-fns/store exist yet (only the unrelated shadcn `ui/avatar.tsx`). **Fatia 2 (NEXT) = Voice Clone slice:** nó `voiceClone` + `generate-voice` edge fn (ElevenLabs/Cartesia BYOK) + `voice_profiles` RLS + `creative_assets` + code-switching guard (FM-AC-013).

BoK Gate is OPEN (suite 10/10) and the SDD carries the Pattern Conformance Declaration (`09-pattern-conformance.md`) — Closed-Loop Step 3 + 3.5 satisfied. Per ultracode, I'll run a parallel **Understand** workflow to extract the exact contracts I must mirror before writing a line of code.

## 🤖 Claude *(04:53:30)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Avatar-clone-ai Fatia 2 (Voice Clone)",
  "summary": "Implement the voiceClone slice: generate-voice edge fn + voice_profiles + BYOK + Canvas node"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Avatar-clone-ai Fatia 2 (Voice Clone)". Continue your current work.'}]
> ```

## 🤖 Claude *(04:53:33)*


## 🤖 Claude *(04:54:29)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'avatar-fatia2-understand',\n  description: 'Gather exact reuse contracts + FRD scope for avatar-clone-ai Fatia 2 (voiceClone) before coding',\n  phases: [{ title: 'Understand', detail: 'parallel readers over reference patterns + FRD scope + external API research' }],\n}\n\nphase('Understand')\n\nconst ROOT = '/home/gcrUX/htdocs/constellation-orchestra'\n\nconst readers = [\n  {\n    label: 'fatia1-state',\n    prompt: `You are a code reader for the MCORCH repo at ${ROOT}. Report ONLY verified facts with path:line citations (Law 1 Materiality \u2014 never fabricate).\n\nTASK: Establish the EXACT state left by avatar-clone-ai Fatia 1.\n1. Read the full migration ${ROOT}/supabase/migrations/20260630000000_user_api_keys_avatar_byok.sql. Report: the EXACT BYOK columns it added to user_api_keys (names), and the EXACT recipe objects it created/modified (encrypt trigger name(s), masked view rebuild, INSTEAD OF trigger, decrypted_user_api_keys view rebuild) \u2014 quote the key SQL verbatim.\n2. Determine whether an 'elevenlabs_api_key' column exists ANYWHERE for user_api_keys: grep the migrations dir and src for 'elevenlabs'. Report yes/no with citations.\n3. Find the Settings UI integration from Fatia 1: grep src for 'hedra'/'cartesia'/'fal_api_key' in SettingsPage and any AvatarProvidersCard. Report which file/component renders the avatar BYOK fields and the exact pattern used (hook used, masked-view read, .insert vs RPC for save/disconnect).\n\nOUTPUT: a tight markdown report: (a) columns added, (b) verbatim recipe SQL skeleton for adding ONE encrypted column, (c) elevenlabs present? y/n, (d) Settings UI file + pattern.`,\n  },\n  {\n    label: 'byok-recipe',\n    prompt: `You are a code reader for the MCORCH repo at ${ROOT}. Report ONLY verified facts with path:line citations.\n\nTASK: Extract the CANONICAL recipe for adding a new encrypted per-user BYOK column to user_api_keys. Read ${ROOT}/supabase/migrations/20260622210000*.sql (the firecrawl/rapidapi recipe referenced in CLAUDE.md) IN FULL. Also read the vault idempotent encrypt migration 20260602140000*.sql and the INSTEAD OF double-fire fix 20260602130000*.sql if present.\n\nOUTPUT: the EXACT, copy-pasteable SQL pattern (verbatim, with placeholders like <new_col>) to: (1) ALTER the underlying table to add the cifrado column, (2) the encrypt trigger that pushes plaintext to Vault via vault_upsert_secret, (3) rebuild the masked view (\u2022\u2022\u2022\u2022 ), (4) the INSTEAD OF trigger UPDATE-first/INSERT-if-not-found with tenant guard, (5) rebuild decrypted_user_api_keys LEFT JOIN. Cite the source migration lines for each piece. Flag any gotcha (e.g. must DROP+CREATE the view; EXECUTE revoke; search_path='').`,\n  },\n  {\n    label: 'generate-image-template',\n    prompt: `You are a code reader for the MCORCH repo at ${ROOT}. Report ONLY verified facts with path:line citations.\n\nTASK: generate-voice will be NET-NEW, parallel to generate-image. Read ${ROOT}/supabase/functions/generate-image/index.ts IN FULL (and ${ROOT}/supabase/functions/_shared/*.ts that it imports \u2014 cors, sentinel, llm-fallback).\n\nOUTPUT: the EXACT skeleton I must mirror for a new user-facing edge fn, quoting verbatim where possible:\n1. CORS headers + OPTIONS handling.\n2. JWT validation block (auth.getUser) \u2192 401 shape.\n3. BYOK resolution: how it reads decrypted_user_api_keys filtered by auth.uid() and the EXACT fail-closed 402 response shape ({ error: '<svc>_not_configured', action: '...' }).\n4. deduct_mco_coins RPC call shape + the 402 insufficient-balance handling (and whether deduct happens AFTER fail-closed gates).\n5. Whether/how it registers creative_assets (RPC name + args) and uploads to a storage bucket (bucket name, signed URL).\n6. infra_health_logs telemetry calls (service/event/metadata shape) on success/degraded/error.\n7. The dual-path service-role+user auth pattern if present (Fatia 1b mentioned generate-image has dual-path auth).\nReport the import lines for _shared helpers verbatim.`,\n  },\n  {\n    label: 'billing-cost',\n    prompt: `You are a code reader for the MCORCH repo at ${ROOT}. Report ONLY verified facts with path:line citations.\n\nTASK: Read ${ROOT}/src/lib/billing.ts (COIN_COSTS) IN FULL and ${ROOT}/docs/processes/mcoin-cost-calibration.md. Also grep edge functions for how they reference a per-action cost constant server-side (e.g. how canvas-execute or orchestrate-content define VIDEO_COST/CONTENT_COST inside the Deno function, since client COIN_COSTS is separate from server cost).\n\nOUTPUT: (1) the current COIN_COSTS object verbatim, (2) the 4\u00d7-floor model formula and the floor value, (3) how a new cost (VOICE_COST = 36 per FRD) should be added to client billing.ts AND where the SERVER-SIDE cost constant lives in edge fns (is it duplicated in the Deno fn? cite an example). (4) Confirm deduct_mco_coins RPC param names verbatim (p_user_id, p_amount?) from a real call site.`,\n  },\n  {\n    label: 'canvas-node-registry',\n    prompt: `You are a code reader for the MCORCH repo at ${ROOT}. Report ONLY verified facts with path:line citations.\n\nTASK: Understand how to add a NEW typed node to the existing Canvas Studio (canvas-studio-cinematic). Find and read the canvas node registry (try ${ROOT}/src/lib/canvas-node-registry.ts, ${ROOT}/src/lib/canvas-utils.ts, src/components/canvas/* or src/components/orchestrator/*), the nodeTypes map, an existing node component (e.g. an image/video node), how canvas-execute resolves the execute payload per node kind (resolveExecutePayload / kind dispatch), and how the graph persists (vm_canvas_projects.graph).\n\nOUTPUT: the EXACT extension points to add a 'voiceClone' node: (1) node factory/recipe shape (fields, handle ids), (2) nodeTypes registration file+line, (3) the inspector pattern, (4) how canvas-execute dispatches by node kind and where I'd add a 'voiceClone'/'talkingHead' branch, (5) persistence shape. Cite each. If the Canvas Studio is the right host vs a dedicated Avatar Studio page, state which exists today and recommend the reuse-first path. Quote the canvas-studio-cinematic skill if it clarifies node shape.`,\n  },\n  {\n    label: 'creative-assets',\n    prompt: `You are a code reader for the MCORCH repo at ${ROOT}. Report ONLY verified facts with path:line citations.\n\nTASK: generate-voice must register output audio in creative_assets (source_module='avatar-studio'). Read the creative_assets migration + the register_creative_asset RPC (grep migrations for 'creative_assets' and 'register_creative_asset'), and find a real call site (grep edge functions for register_creative_asset \u2014 e.g. video-bridge, canvas-execute, generate-image).\n\nOUTPUT: (1) creative_assets schema columns verbatim, (2) register_creative_asset RPC signature (exact param names + types) verbatim from the migration, (3) a real call-site example showing the args passed (asset_type, storage_key, source_module, etc.), (4) which storage bucket audio should go to and how signed URLs are generated. Cite each.`,\n  },\n  {\n    label: 'frd-fatia2-scope',\n    prompt: `You are a requirements reader for the MCORCH repo at ${ROOT}. Report ONLY what the docs say, with path:line citations. Do NOT invent.\n\nTASK: Read ${ROOT}/docs/bok/avatar-clone-ai/04-frd.md sections 2.1 (Fatia 1 BYOK), 2.2 (Voice Clone \u2014 Fatia 2), 2.7/2.8/2.9 (security/privacy/Vision QA NFRs), and the NFR-AC list + the AT-AC acceptance-test matrix rows for Fatia 2 FRs. Also read ${ROOT}/docs/bok/avatar-clone-ai/06-data-model.md voice_profiles section and any Vault voiceprint storage detail.\n\nOUTPUT a precise scope sheet for Fatia 2:\n1. Each FR-AC in Fatia 2 (id + verbatim 'shall' statement) \u2014 especially FR-AC-009 (generate-voice) and FR-AC-010 (code-switching guard).\n2. Whether Fatia 2 REQUIRES a consent gate (does FR-AC-009/010 reference avatar_consents?) or whether consent is deferred to Fatia 3/6. Quote the exact text that decides this.\n3. The voice_profiles table schema from the data model (columns + RLS) verbatim.\n4. NFRs that constrain Fatia 2 (security/privacy/cost/observability) \u2014 list ids + one line each.\n5. The acceptance tests (AT-AC ids) that must pass for Fatia 2.\n6. Cost: FRD-stated VOICE_COST value + calibration note.`,\n  },\n  {\n    label: 'sop-templates',\n    prompt: `You are a code reader for the MCORCH repo at ${ROOT}. Report ONLY verified facts with path:line citations.\n\nTASK: I must author a Lei 2 SOP at docs/processes/avatar-voice-credential-resolution.md BEFORE coding the voice slice. Read two existing SOPs as templates: ${ROOT}/docs/processes/trends-credential-resolution.md and ${ROOT}/docs/processes/affiliate-credential-resolution.md (or meta-credential-resolution.md). Also note the SDD \u00a79 requirement that names sibling SOPs.\n\nOUTPUT: (1) the exact SOP section structure these follow (Operator / Sequence / Verification gates / Recovery path / Success signal \u2014 the Lei 2 table), quoting headers, (2) the credential-resolution-order pattern they document (per-user table \u2192 fail-closed 402), (3) a skeleton I can fill for avatar-voice (ElevenLabs/Cartesia per-user BYOK fail-closed). Keep it copy-ready.`,\n  },\n  {\n    label: 'voice-api-research',\n    prompt: `You are a research agent. Find the CURRENT (2026) API contracts for two text-to-speech / voice-cloning providers, with source URLs for every claim (Law 1 \u2014 cite URLs). Use web search/fetch.\n\nPROVIDER 1 \u2014 ElevenLabs:\n- Text-to-Speech endpoint: exact URL, HTTP method, auth header name, request JSON body (voice_id, model_id e.g. eleven_multilingual_v2 / eleven_v3 / flash / turbo, text), response (audio bytes / content-type).\n- Instant Voice Cloning (IVC) / add-voice endpoint: exact URL, multipart form fields (name, files[] samples), response (voice_id).\n- Note model ids that support pt-BR + EN multilingual.\n\nPROVIDER 2 \u2014 Cartesia (Sonic):\n- TTS endpoint: exact URL, auth header, request body (model_id e.g. sonic, voice id/embedding, transcript, output_format), response.\n- Voice cloning endpoint if available.\n\nOUTPUT: a compact contract sheet per provider (endpoint, method, headers, body shape, response, relevant model ids for en + pt-BR), each line carrying its source URL. If a detail can't be verified, say \"unverified\" rather than guessing.`,\n  },\n]\n\nconst results = await parallel(readers.map(r => () =>\n  agent(r.prompt, { label: r.label, phase: 'Understand', agentType: 'Explore' }).then(text => ({ label: r.label, text }))\n))\n\nreturn results.filter(Boolean)\n",
  "description": "Understand phase: gather Fatia 2 contracts"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: w6zo9cxho
> Summary: Gather exact reuse contracts + FRD scope for avatar-clone-ai Fatia 2 (voiceClone) before coding
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/8774b91e-56ce-422f-aa7a-2a61eaf326df/subagents/workflows/wf_1e5dfbc5-a66
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/8774b91e-56ce-422f-aa7a-2a61eaf326df/workflows/scripts/avatar-fatia2-understand-wf_1e5dfbc5-a66.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/8774b91e-56ce-422f-aa7a-2a61eaf326df/workflows/scripts/avatar-fatia2-understand-wf_1e5dfbc5-a66.js"} to iterate without resending the script.)
> Run ID: wf_1e5dfbc5-a66
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/8774b91e-56ce-422f-aa7a-2a61eaf326df/workflows/scripts/avatar-fatia2-understand-wf_1e5dfbc5-a66.js", resumeFromRunId: "wf_1e5dfbc5-a66"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(04:54:37)*


## 🤖 Claude *(04:54:42)*

Disparei a fase **Understand** (workflow `wf_1e5dfbc5-a66`, 9 leitores em paralelo) para extrair os contratos exatos que a Fatia 2 precisa reusar — estado da Fatia 1, recipe de coluna BYOK cifrada, template do `generate-image`, billing/custo, registry de nós do Canvas, `register_creative_asset`, escopo preciso do FRD §2.2, templates de SOP (Lei 2) e os contratos atuais das APIs ElevenLabs/Cartesia (com URLs-fonte, Lei 1).

Vou aguardar o retorno para sintetizar o plano de implementação da Fatia 2 sem inventar nada além da Fonte da Verdade. Te aviso assim que tiver o mapa consolidado e o plano cravado.

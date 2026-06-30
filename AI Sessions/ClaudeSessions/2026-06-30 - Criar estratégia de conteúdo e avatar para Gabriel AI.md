# Criar estratégia de conteúdo e avatar para Gabriel AI
**Date:** 2026-06-30 | **Session ID:** `20894beb-8faf-40d8-bce8-715b0c184c7f`

---

## 👤 User *(22:53:56)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(22:53:56)*

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


## 🤖 Claude *(22:54:04)*


## 🤖 Claude *(22:54:04)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with all pre-flight commands in parallel.

## 🤖 Claude *(22:54:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin --quiet 2>&1 | tail -3; echo \"=== LOG ===\"; git log --oneline -7; echo \"=== STATUS ===\"; git status --short; echo \"=== DIFF STAT ===\"; git diff HEAD --stat; echo \"=== vs origin/main ===\"; git rev-list --left-right --count origin/main...HEAD 2>/dev/null",
  "description": "Git history, status, diff scope, fetch origin"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === LOG ===
> a723f32 docs(handoff): seal product-miner vision reliability + async timeout-proof extraction
> b18173f docs(readme): v6.59.0 — Product Miner vision reliability + async — mesh 8991 nodes
> 722a843 feat(miner): smarter product synthesis — audience-fit logic + confidence + robust JSON parse
> f3515e8 feat(miner): async timeout-proof extraction — background job + Realtime progress + notification
> 3827d37 fix(discover-products): retry video analysis once before any cover fallback (quality-first)
> bde7b61 feat(discover-products): rich full-video analysis for every TikTok (shouldDownloadVideos:true)
> 5713306 fix(miner): robust synthesis — tolerant JSON parse + stricter prompt + larger max_tokens
> === STATUS ===
> === DIFF STAT ===
> === vs origin/main ===
> 0	0
> ```

## 🤖 Claude *(22:54:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== DOCKER mcorch ===\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"=== DOCKER mega-brain ===\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"=== CHROMA ===\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat 2>&1; echo \"\"; echo \"=== BoK suites ===\"; ls docs/bok/ 2>/dev/null; echo \"=== HANDOFF lines ===\"; wc -l HANDOFF.md; echo \"=== scratch ===\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "Docker, Chroma health, BoK suites, HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === DOCKER mcorch ===
> mcorch_vision_mcp: Up 5 hours (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> === DOCKER mega-brain ===
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> === CHROMA ===
> {"nanosecond heartbeat":1782773649592816780}
> === BoK suites ===
> agentic-governance
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
> === HANDOFF lines ===
> 8753 HANDOFF.md
> === scratch ===
> scratch has files
> ```

## 🤖 Claude *(22:54:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20; echo \"=== TSC EXIT: done ===\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === TSC EXIT: done ===
> ```

## 🤖 Claude *(22:54:14)*


## 🤖 Claude *(22:54:14)*

Worktree clean, TS zero errors, infra healthy. Now reading HANDOFF.md (head + tail) and sprint priorities in parallel.

## 🤖 Claude *(22:54:16)*


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
> 14	## Session Seal — Minerador de Produtos: Reparo de Confiabilidade do Vision MCP + Extração Assíncrona Timeout-Proof (2026-06-29)
> 15	
> 16	Continuação do QA que estava com o Antigravity. A extração ao vivo do TikTok voltava `non-2xx` ("Extração ao vivo falhou, usando dados do cache"). Como sênior, verifiquei materialmente (Lei 1) e achei que **não era só tamanho** — diagnostiquei 3 causas-raiz e endureci o pipeline inteiro de ponta a ponta, fechando com a diretiva Sovereign de **assincronização timeout-proof** (tempo/tamanho de vídeo viral nunca podem ser gargalo do Vision MCP).
> 17	
> 18	**Arcos entregues:**
> 19	- **Tamanho de vídeo** — Vision MCP `analyze_video` agora sobe vídeos **20–100MB via Gemini Files API** (resumable upload → poll ACTIVE → `fileData.fileUri`); ≤20MB segue inline rápido. Provado: MP4 30MB → análise real, log `tool_ok`.
> 20	- **`directVideoUrl` frágil (stub 5KB)** — voltei pro `shouldDownloadVideos:true` (URL Apify público estável `api.apify.com/.../video-*.mp4`) → **análise de VÍDEO rica em TODO vídeo** (não a capa fina), com **retry antes de degradar** + fallback cover-image como rede de segurança (MCP rejeita `<50KB` `video_too_small`).
> 21	- **Síntese** — `:free` do OpenRouter (429 do pool compartilhado que ignora BYOK) cai automaticamente pro **irmão pago BYOK**; parser JSON tolerante (quoted **e** unquoted, sobrevive a aspas não-escapadas/truncamento); **seleção de produto por fit de audiência** (vídeo sem produto → infere o que a audiência compraria, não o objeto incidental) + **badge de confiança** honesto.
> 22	- **Extração ASSÍNCRONA timeout-proof** — `vm_miner_jobs` (RLS owner-scoped, writes service-role = tamper-proof, na publicação `supabase_realtime` + replica identity) + action `mine-async` (retorna `job_id` em ~2.4s, roda extract→vision num `EdgeRuntime.waitUntil` em background) + hook `useMinerJob` (Realtime + polling de fallback) → **barra de progresso (estágio + % + ETA)** + **notificação no sino** quando volta.
> 23	- **Hardening de brinde** — fechado o bloqueante de tenancy (`Deno.env.get("APIFY_TOKENS")` global removido → per-user fail-closed) + guard SSRF no edge.
> 24	
> 25	| Action | Result |
> 26	|--------|--------|
> 27	| `packages/vision-mcp-core/src/tools/analyze-video.ts` | ✅ Gemini Files API p/ 20–100MB + `MIN_VIDEO_BYTES` rejeita stub <50KB (FR-VM-024); container `mcorch_vision_mcp` rebuildado/healthy |
> 28	| `supabase/functions/discover-products/index.ts` | ✅ `shouldDownloadVideos:true` + `coverUrl` + vision-analyze com retry+cover fallback + tenancy per-user + SSRF guard + action `mine-async` (background `EdgeRuntime.waitUntil`) |
> 29	| `supabase/functions/openrouter-swarm/index.ts` | ✅ `:free` 429 → retry irmão pago BYOK + `max_tokens` 1024 |
> 30	| `supabase/migrations/20260629170000_vm_miner_jobs.sql` | ✅ tabela job RLS owner + publicação realtime + replica identity (aplicada via Management API) |
> 31	| `src/hooks/useMinerJob.ts` | ✅ kick + Realtime + polling 3s fallback |
> 32	| `src/pages/AffiliateProductsPage.tsx` | ✅ barra de progresso async + cover_url + síntese por fit de audiência + badge de confiança + parser robusto |
> 33	| `tsc --noEmit` / `bun run test` | ✅ 0 erros · 295 passed |
> 34	| `/security-review` (independente ×3) | ✅ NO findings (Files API, async job, edge) |
> 35	
> 36	| Commit | Conteúdo |
> 37	|--------|----------|
> 38	| `b13018b` | fix(vision-mcp): analyze_video handles 20-100MB via Gemini Files API |
> 39	| `36bf180` | fix(discover-products): video cap + per-user Apify tenancy + SSRF guard |
> 40	| `e99004b` | fix(vision-mcp): reject sub-50KB stub videos (video_too_small) |
> 41	| `08f1e47` | feat(discover-products): cover-image vision fallback |
> 42	| `80ca697` | fix(openrouter-swarm): :free 429 → paid BYOK sibling |
> 43	| `5713306` | fix(miner): robust synthesis — tolerant JSON + prompt + max_tokens |
> 44	| `bde7b61` | feat(discover-products): rich full-video analysis (shouldDownloadVideos:true) |
> 45	| `3827d37` | fix(discover-products): retry video before cover fallback (quality-first) |
> 46	| `f3515e8` | feat(miner): async timeout-proof extraction + Realtime progress + notification |
> 47	| `722a843` | feat(miner): smarter product synthesis — audience-fit + confidence + robust parse |
> 48	
> 49	Handoff node `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` inserido + auto-embedado (768d, trigger pg_net). Mesh **8991 nós**.
> 50	
> 51	---
> 52	
> 53	## Session Seal — Minerador de Produtos: Extração TikTok Otimizada, Fila Sequencial e Deseleção de Modelos (2026-06-29)
> 54	
> 55	Diretiva Sovereign: resolver os gargalos de timeout de 30s da Supabase Edge Function e adicionar a capacidade de deseleção/limpeza completa de modelos (incluindo o preset inicial).
> 56	
> 57	**Melhorias Implementadas:**
> 58	- **TikTok Scraper Otimizado (shouldDownloadVideos: false)**: Alteramos a chamada para a Apify para não baixar fisicamente os arquivos de vídeo, reduzindo o tempo do scraper de ~35s para apenas ~6-8s.
> 59	- **Fallback de URL de Stream MP4**: Desenvolvemos a extração do endereço de vídeo direto (`directVideoUrl`) a partir do array `subtitleLinks` quando o download de vídeo está desativado. Isso preserva os links funcionais de CDN sem o gargalo de banda.
> 60	- **Requisição Sequencial Segura (Anti-timeout)**: A interface no frontend chama `extract-metadata` e `vision-analyze` de forma sequencial e controlada. Nenhum request individual ultrapassa 15 segundos, eliminando inteiramente os timeouts de 30s do Supabase gateway.
> 61	- **Deseleção de Modelos ("Limpar Seleções")**: Adicionamos o prop `onClearAll` no componente reutilizável `SwarmModelSelector` e renderizamos um botão vermelho "Limpar Seleções" dentro do dropdown. Integrado em `AffiliateProductsPage.tsx` e `ModelArenaPage.tsx`, permitindo zerar a seleção de modelos ativos, inclusive o preset padrão.
> 62	- **Validação de Produção E2E**: Verificado com sucesso no ambiente em produção (login efetuado, extração sequencial e importação de produto pelo operador do navegador sem erros).
> 63	
> 64	| Action | Result |
> 65	|--------|--------|
> 66	| `supabase/functions/discover-products/index.ts` | ✅ Suporte a sequential extract-metadata/vision-analyze, extraction do stream e performance optimization |
> 67	| `src/components/core/SwarmModelSelector.tsx` | ✅ Prop onClearAll e botão Limpar Seleções integrado no painel |
> 68	| `src/hooks/useSwarmArena.ts` | ✅ Função clearAllModels exportada para limpeza e sincronização no localStorage |
> 69	| `src/pages/AffiliateProductsPage.tsx` | ✅ Sequência assíncrona com toasts dinâmicos e controle de limpeza do Swarm |
> 70	| `src/pages/ModelArenaPage.tsx` | ✅ Associação do botão Limpar Seleções do SwarmModelSelector |
> 71	| `tsc --noEmit` / build | ✅ 0 erros de compilação TypeScript · build de produção gerado com sucesso |
> ```

## 🤖 Claude *(22:54:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8353,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8353	ContentLibraryPage monetization flow:
> 8354	  Card (text, body contains mercadolivre.com.br)
> 8355	    └── DropdownMenu → "Monetizar Links ML"
> 8356	          → handleMonetizeLinks(item):
> 8357	               match(ML_URL_RE) → unique URLs
> 8358	               for url of unique:
> 8359	                 POST process-affiliate-link → affiliate_url
> 8360	                 body.split(url).join(affiliate_url)
> 8361	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8362	          → Badge 💰 ML (emerald) exibido após monetização
> 8363	```
> 8364	
> 8365	---
> 8366	
> 8367	## Pending Actions (Commercial Launch)
> 8368	
> 8369	### CRITICAL — Must complete before first client
> 8370	
> 8371	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8372	
> 8373	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8374	
> 8375	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8376	
> 8377	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8378	
> 8379	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8380	
> 8381	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8382	
> 8383	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8384	
> 8385	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8386	
> 8387	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8388	
> 8389	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8390	
> 8391	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8392	
> 8393	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8394	   ```bash
> 8395	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8396	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8397	   ```
> 8398	
> 8399	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8400	
> 8401	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8402	
> 8403	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8404	
> 8405	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8406	
> 8407	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8408	
> 8409	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8410	
> 8411	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8412	
> 8413	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8414	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8415	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8416	
> 8417	### SOCIAL — Next steps
> 8418	
> 8419	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8420	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8421	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8422	
> 8423	### NON-CRITICAL
> 8424	
> 8425	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8426	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8427	- `browserslist` — ✅ updated (2026-04-26)
> 8428	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8429	
> 8430	### GITNEXUS MCP — Next steps
> 8431	
> 8432	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8433	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8434	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8435	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8436	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8437	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8438	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8439	
> 8440	### PHASE EPSILON — Next iterations
> 8441	
> 8442	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8443	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8444	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8445	
> 8446	### CORE — Next iterations
> 8447	
> 8448	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8449	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8450	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8451	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8452	
> 8453	### PHASE DELTA — Next iterations
> 8454	
> 8455	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8456	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8457	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8458	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8459	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8460	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8461	
> 8462	### USUÁRIO ZERO — Checklist de validação
> 8463	
> 8464	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8465	- ✅ Stripe sandbox secrets no vault
> 8466	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8467	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8468	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8469	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8470	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8471	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8472	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8473	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8474	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8475	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8476	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8477	
> 8478	---
> 8479	
> 8480	## Infrastructure
> 8481	
> 8482	| Service | Container | Port | Status |
> 8483	|---------|-----------|------|--------|
> 8484	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8485	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8486	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8487	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8488	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8489	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8490	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8491	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8492	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8493	
> 8494	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8495	
> 8496	```bash
> 8497	docker compose up -d
> 8498	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8499	```
> 8500	
> 8501	---
> 8502	
> 8503	## Security Model (Post-Go-Live)
> 8504	
> 8505	| Table | Isolation |
> 8506	|-------|-----------|
> 8507	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8508	| `mcorch_edges` | Same pattern |
> 8509	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8510	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8511	
> 8512	---
> 8513	
> 8514	## Billing Architecture
> 8515	
> 8516	| Decision | Value |
> 8517	|----------|-------|
> 8518	| Canonical billing ledger | `profiles.mco_balance` |
> 8519	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8520	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8521	| Orchestration cost | 10 mcoCoins/run |
> 8522	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8523	| Stripe | Sandbox keys active — swap to live before first client |
> 8524	
> 8525	---
> 8526	
> 8527	## GraphRAG State
> 8528	
> 8529	- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8530	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8531	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8532	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8533	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8534	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8535	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8536	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8537	- HNSW cosine index operational
> 8538	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8539	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8540	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8541	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8542	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8543	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8544	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8545	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8546	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8547	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8548	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8549	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8550	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8551	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8552	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8553	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8554	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8555	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8556	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8557	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8558	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8559	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8560	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8561	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8562	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8563	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8564	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8565	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8566	
> 8567	### Embedding Model
> 8568	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8569	Schema: `vector(768)` — HNSW cosine index.
> 8570	
> 8571	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8572	Três camadas eliminam intervenção manual:
> 8573	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8574	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8575	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8576	
> 8577	### Comandos de manutenção da Mesh
> 8578	```bash
> 8579	# Verificar nós sem embedding (deveria retornar array vazio):
> 8580	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8581	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8582	
> 8583	# Backfill manual (Bun-native — requer .env):
> 8584	bun run scripts/backfill-embeddings.ts
> 8585	
> 8586	# Backfill de código-fonte nos nós AST:
> 8587	bun run scripts/backfill-node-content.ts
> 8588	
> 8589	# Re-sync AST completo:
> 8590	cd packages/gitnexus-core && npm run sync-mesh
> 8591	
> 8592	# Acompanhar re-ingesta pós-commit:
> 8593	tail -f /tmp/mcorch-ingest.log
> 8594	```
> 8595	
> 8596	---
> 8597	
> 8598	## Video Rescue Protocol
> 8599	
> 8600	When a video generation operation (Google Veo) times out or client disconnects:
> 8601	```bash
> 8602	# Via edge function (production):
> 8603	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8604	  -H "Authorization: Bearer <user_jwt>" \
> 8605	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8606	
> 8607	# Via local script (admin/debug):
> 8608	source .env && bun run rescue.ts <operation_id> <content_id>
> 8609	```
> 8610	
> 8611	---
> 8612	
> 8613	## Architecture Pillars
> 8614	
> 8615	| Layer | Implementation |
> 8616	|-------|---------------|
> 8617	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8618	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8619	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8620	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8621	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8622	
> 8623	---
> 8624	
> 8625	## Phase Delta — Architecture
> 8626	
> 8627	```
> 8628	OrchestrationPage (full-canvas, p-0)
> 8629	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8630	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8631	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8632	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8633	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8634	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8635	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8636	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8637	
> 8638	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8639	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8640	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8641	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8642	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8643	```
> 8644	
> 8645	### Canvas State Architecture (Hybrid)
> 8646	
> 8647	```
> 8648	User interaction → ReactFlow internal state (positions, drag)
> 8649	                         ↓ (debounced 600ms)
> 8650	                   localStorage (positions persist across refresh)
> 8651	                         ↑
> 8652	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8653	     ↓ (status changes sync to ReactFlow via useEffect)
> 8654	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8655	```
> 8656	
> 8657	## Key Files
> 8658	
> 8659	| Purpose | Path |
> 8660	|---------|------|
> 8661	| Architecture rules | `CLAUDE.md` |
> 8662	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8663	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8664	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8665	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8666	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8667	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8668	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8669	| **Node types** | `src/components/orchestrator/nodes/` |
> 8670	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8671	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8672	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8673	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8674	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8675	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8676	| Billing utilities | `src/lib/billing.ts` |
> 8677	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8678	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8679	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8680	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8681	| Video rescue (local) | `rescue.ts` |
> 8682	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8683	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8684	| Deploy harness | `scripts/harness-deploy.sh` |
> 8685	
> 8686	---
> 8687	
> 8688	## First Client Onboarding Checklist
> 8689	
> 8690	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8691	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8692	3. ~~Activate watchdog cron~~ ✅ Done
> 8693	4. ~~Deploy rescue-video function~~ ✅ Done
> 8694	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8695	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8696	7. Monitor `infra_health_logs` for first 24h.
> 8697	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8698	
> 8699	---
> 8700	
> 8701	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8702	
> 8703	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8704	
> 8705	| Action | Result |
> 8706	|--------|--------|
> 8707	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8708	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8709	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8710	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8711	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8712	
> 8713	| Commit | Conteúdo |
> 8714	|--------|----------|
> 8715	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8716	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8717	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8718	
> 8719	### Arquitetura Matrix Intelligence
> 8720	
> 8721	```
> 8722	ConstellationMatrix (Stabilized Engine)
> 8723	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8724	  └── NodeDetailsPanel (Tabbed Navigation)
> 8725	        ├── Tab Meta: Neighbor exploration + Net Context
> 8726	        ├── Tab Code: Source code preview (Supabase sync)
> 8727	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8728	
> 8729	useNodeIntelligence Hook:
> 8730	  - contentQuery: fetch nodes.content column
> 8731	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8732	  - state: isAnalyzing, analysisResult, progress
> 8733	```
> 8734	
> 8735	---
> 8736	
> 8737	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8738	
> 8739	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8740	
> 8741	| Action | Result |
> 8742	|--------|--------|
> 8743	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8744	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8745	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8746	
> 8747	**Output da análise (estruturado em pt-BR):**
> 8748	- Visão Geral — papel do módulo no sistema
> 8749	- Padrões Detectados — design patterns, antipatterns
> 8750	- Acoplamento & Dependências — análise In/Out-Degree
> 8751	- Recomendações — 1-3 ações priorizadas
> 8752	
> ```

## 🤖 Claude *(22:54:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -80 || echo \"NO sprint-priorities.md\"; echo \"=== scratch contents ===\"; ls -la scratch/ 2>/dev/null",
  "description": "Read sprint priorities and scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (70.2KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/tool-results/b1ls74bij.txt
> 
> Preview (first 2KB):
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.53.0 — Doutrina Agêntica AGI→ASI + Learning & Adaptation + analytics honesto (2026-06-27)** — sessão-maratona multi-arco. **7 commits.** **(1)** Doutrina `agentic-vision.md` (21 padrões × maturidade + tese Via 4-produto/Via 3-micro) + **Pattern Conformance gate vinculante** no CLAUDE.md §1 + BoK `agentic-governance` 10/10 (seal `34748570`) + 2 docs stale deprecados. **(2)** **Collective Efficiency Ledger** (`81210ab`) — VIEW security_invoker + RPC service-role medem mco/resultado anti-Goodhart (G6 isolamento provado; rollup real 334s vs 2.4s). **(3)** **Learning & Adaptation** (o único padrão fraco) atacado: nervo sensorial (`publication_metrics` + coletor fail-soft IG/FB + painel "Por Publicação" browser-provado) + reward multi-métrica brand-first (mata `totalClicks` Goodhart, prova policy `7d9856d0`) + realocação ε-greedy (`1371094`/`47474ac`). **(4)** Analytics honesto — demo-kill (`b6abff1`) + zeramento dos perfis sociais antigos (marca **Gabriel AI**/**@gabrielOrchAI** começam do zero). **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8971** · handoff `326949f1`. **Pending:** re-OAuth IG insights (destrava o payoff visível) · B4 EWMA · B5 pauta de receita · V4-2 experimento · postback ML · emenda BoK post-engine (YT/TikTok). **Lição:** "não avançamos apesar do dev incrível" = o motor aprendia sobre **placar em branco**; medir o desfecho real é o que faz capacidade virar avanço.
> 
> ...
> </persisted-output>
> ```

## 🤖 Claude *(22:54:26)*


## 🤖 Claude *(22:54:50)*

Tenho todo o contexto necessário. Compilando o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Minerador de Produtos: Confiabilidade Vision MCP
            + Extração Assíncrona Timeout-Proof (2026-06-29)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
Fase selada: **Reparo de confiabilidade do Minerador de Produtos** (Vision MCP + extração async). Worktree em paridade exata com `origin/main` (0 ahead / 0 behind).

Últimos commits:
- `a723f32` — docs(handoff): seal product-miner vision reliability + async timeout-proof
- `b18173f` — docs(readme): v6.59.0 — mesh 8991 nodes
- `722a843` — feat(miner): smarter product synthesis (audience-fit + confidence + robust parse)
- `f3515e8` — feat(miner): async timeout-proof extraction (background job + Realtime + notification)
- `3827d37` — fix(discover-products): retry video analysis before cover fallback

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ (nenhum arquivo M/??). Único ruído: `scratch/` tem arquivos soltos — candidato a mover para `.claude/scripts/db/`.

🏗️ **INFRA** — tudo saudável
- `mcorch_chroma`: Up 2 weeks (healthy) — Chroma API v2 heartbeat **OK**
- `mcorch_claude_mem`: Up 2 weeks (healthy)
- `mcorch_vision_mcp`: Up 5 hours (healthy) — *rebuildado na seal anterior (Files API 20-100MB)*
- `mega-brain-daemon/webhook/dashboard`: healthy/up

🧠 **KNOWLEDGE MESH**
**8991 nós** · ~9070 arestas (100% embedded, 768d HNSW cosine). Handoff desta seal: `1c100e2a-…7ab0a8`.
Top tipos: handoff · milestone · architecture · decision · observation · documentation_suite + AST (file/function/interface).

🔧 **TYPESCRIPT** — Zero erros ✅ · suíte 295 passed (registrado na seal)

📚 **BoK SUITES** — 23 suítes presentes; nenhuma incompleta detectada. As 5 canônicas (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw) seladas. O trabalho recém-selado (Minerador) é **fix/hardening de feature já documentada** (exemption do BoK Gate — sem suíte nova exigida).

📌 **SPRINT**
Goal: **Distribuição social autônoma operacional** — pipeline publica LinkedIn auto; Twitter ao subir tier; Instagram pós App Review.
Foco recente (v6.53.0): doutrina agêntica AGI→ASI + Collective Efficiency Ledger + Learning & Adaptation (reward multi-métrica brand-first).

⚡ **PRÓXIMOS PASSOS** (do Pending Actions — CRITICAL primeiro)
1. **Viral Autopilot — fechar o vídeo + saída visível**: editor HyperFrames Studio (módulo-container, vhost `studio.mcorch.com` = ação Sovereign DNS) + 1º ciclo pago de vídeo *witnessed* + postback ML real (OTD-VA-007). Motor R1–R4 já provado; falta a ponta visível.
2. **Unified Sensorial Canvas — Fases 3.5–3.10**: sinapses inter-rede reais (`mcorch_edges` código↔memória), fly-to, perf (`OTD-UCANVAS-PERF` — query ~30s com 2 canvases), paridade + cutover + seal.
3. **Re-OAuth IG insights** (destrava o payoff visível do Learning & Adaptation) · `fetch-trends`→pauta do ângulo viral (FR-VA-018) · emenda BoK post-engine (YT/TikTok).

⚠️ **ALERTAS**
- `scratch/` com arquivos soltos — limpeza recomendada (não bloqueante).
- Nenhum container unhealthy, nenhum erro TS, nenhuma mudança não-commitada conflitante. ✅

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

Sessão anterior selou um reparo profundo de confiabilidade no Minerador de Produtos (3 causas-raiz no `non-2xx` do Vision MCP + assincronização timeout-proof), tudo verificado materialmente e com `/security-review` limpo ×3. Base estável e em paridade com `origin/main`.

Qual frente o senhor quer atacar, Maestro?

## 👤 User *(23:26:28)*

ótimo começe com scratch limpando tudo e depois vamos para os próximos passos. Pois precisamos crair nossas estrategias de conteúdo e uma cadencia de 30 dias verificar a frequencia e formato, duração, thema, produtos tudo isso para testar e começar gerar conteúdo. Lembrando que vamos precisar fazer um deepresearch com força total para descobrir e aplicar as melhores estrategias de conteúdo viral, para nosso perfil que é Gabriel AI, vamos precisar tambem adicionar um avatar treinado e consistente fiel a minha pessoa e voz, o projeto é o Gabriel (eu) AI com toda minhas caracteristicas e personalidades usando o cerebro clonado. Então temos que criar todas as peças antes de juntaar tudo com o viral autopilot.

## 🤖 Claude *(23:28:34)*


## 🤖 Claude *(23:28:35)*

Entendido, Maestro. Vou começar limpando o `scratch/` e em seguida aimar a artilharia da pesquisa força-total. Primeiro deixe-me **olhar** o que há no scratch antes de remover (Lei 1 — nunca deletar às cegas).

## 🤖 Claude *(23:28:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== scratch/ contents ===\"; ls -la scratch/ 2>/dev/null; echo \"=== size ===\"; du -sh scratch/ 2>/dev/null; echo \"=== gitignored? ===\"; git check-ignore scratch/ && echo \"scratch/ IS gitignored\" || echo \"scratch/ NOT ignored\"; echo \"=== tracked files in scratch? ===\"; git ls-files scratch/ | head",
  "description": "Inspect scratch/ contents, size, git status before cleaning"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === scratch/ contents ===
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun 29 18:49 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 29 18:48 ..
> === size ===
> 4.0K	scratch/
> === gitignored? ===
> scratch/
> scratch/ IS gitignored
> === tracked files in scratch? ===
> ```

## 🤖 Claude *(23:29:07)*


## 🤖 Claude *(23:29:15)*

Verifiquei materialmente: o `scratch/` **já está vazio** — só `.` e `..`, zero arquivos (4.0K = a entrada do diretório em si), gitignored, nenhum arquivo rastreado. O `/handson` reportou "scratch has files" por um falso-positivo do `ls` (exit 0 em dir vazio também). **Nada a limpar** — não vou fabricar uma limpeza que não existiu (Lei 1). ✅

```
**ORO triplet desta task (programa Gabriel AI Content Engine):**
- Operator: MCORCH Master Execution Agent (eu) — pesquisa + blueprint + peças
- Reviewer: Sovereign (Gabriel) — aprova blueprint/cadência/avatar antes de qualquer código
- Owner: Sovereign — ROI de marca (alcance/autoridade/receita de afiliado de longo prazo)
```

Agora, antes de disparar a **deepsearch força-total** — porque é canhão caro e o alvo importa muito — preciso travar 4 eixos. Cada um muda o que pesquiso **e** como desenho a cadência de 30 dias. Isso respeita o **Closed-Loop Protocol** (pesquisa → blueprint-semente da BoK → sua revisão → BoK → código; nada de código antes disso).

Contexto que já tenho da malha/memória e vou assumir (corrija se preciso): persona = **Gabriel AI / CCIO** evangelizando o MCORCH (marca primeiro, produto/afiliado como subproduto de longo prazo); motor de publicação = reusar o **Viral Autopilot** vivo; perfis sociais zerados (começam do zero).

## 🤖 Claude *(23:29:31)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Para o avatar treinado fiel \u00e0 sua pessoa e voz (talking-head digital + clone de voz), qual caminho a pesquisa deve priorizar e recomendar?",
      "header": "Avatar",
      "multiSelect": false,
      "options": [
        {
          "label": "Pesquisa recomenda (comparar)",
          "description": "A deepsearch avalia SaaS comercial vs. self-hosted soberano lado a lado \u2014 fidelidade, consist\u00eancia, clone de voz pt-BR, custo/m\u00eas, esfor\u00e7o de engenharia \u2014 e recomenda o melhor com prova. Voc\u00ea decide depois com os dados na m\u00e3o."
        },
        {
          "label": "Self-hosted soberano (BYOK)",
          "description": "Clone de voz (XTTS/F5-TTS-class) + talking-head em modelos open-source rodando na nossa Sovereign Mesh. Controle total, sem mensalidade, fiel ao ethos BYOK do MCORCH \u2014 mais engenharia."
        },
        {
          "label": "SaaS comercial (r\u00e1pido)",
          "description": "Avatar treinado tipo HeyGen/Synthesia/Argil/Captions. Fidelidade alta e r\u00e1pido pra ir ao ar; custo mensal recorrente; menos soberania."
        }
      ]
    },
    {
      "question": "Quais canais entram na cad\u00eancia de 30 dias? (avatar \u00e9 v\u00eddeo-first \u2014 marque todos que quer ativar)",
      "header": "Canais",
      "multiSelect": true,
      "options": [
        {
          "label": "YouTube (Shorts + longo)",
          "description": "V\u00eddeo 9:16 (Shorts) + long-form. Autoridade dur\u00e1vel e SEO de v\u00eddeo. Branch publish-social net-new (gate audit YT \u2014 v\u00eddeo nasce private)."
        },
        {
          "label": "TikTok",
          "description": "V\u00eddeo 9:16 nativo, maior alcance viral org\u00e2nico. Branch net-new (gate SELF_ONLY at\u00e9 audit)."
        },
        {
          "label": "Instagram Reels",
          "description": "Reels 9:16 \u2014 j\u00e1 PROVADO E2E vivo (conex\u00e3o @magicorch publica). Caminho mais curto pra valor vis\u00edvel."
        },
        {
          "label": "LinkedIn + X (texto/repurpose)",
          "description": "Reaproveita o pilar de texto + clipe do v\u00eddeo. LinkedIn j\u00e1 publica; X precisa de tier Basic."
        }
      ]
    },
    {
      "question": "Sobre o que a marca Gabriel AI fala? Isso define os temas e os produtos que entram na cad\u00eancia.",
      "header": "Pilares",
      "multiSelect": false,
      "options": [
        {
          "label": "Mix: autoridade + educa\u00e7\u00e3o + produtos",
          "description": "Build-in-public do MCORCH/jornada AGI\u2192ASI + educa\u00e7\u00e3o pr\u00e1tica de IA/automa\u00e7\u00e3o + tie-ins de afiliado/produto. Equilibra alcance, autoridade e monetiza\u00e7\u00e3o."
        },
        {
          "label": "Build-in-public MCORCH",
          "description": "Foco em autoridade t\u00e9cnica: bastidores da malha, AGI\u2192ASI, CCIO thought-leadership. Nicho premium, audi\u00eancia tech."
        },
        {
          "label": "Educa\u00e7\u00e3o de IA para empreendedores",
          "description": "Conte\u00fado amplo de IA/automa\u00e7\u00e3o para crescer r\u00e1pido em volume. Alcance largo, monetiza\u00e7\u00e3o via produto depois."
        }
      ]
    },
    {
      "question": "Em qual idioma a marca publica nos primeiros 30 dias? (muda as normas virais que pesquiso e o alcance)",
      "header": "Idioma",
      "multiSelect": false,
      "options": [
        {
          "label": "PT-BR (Brasil primeiro)",
          "description": "Foco no mercado brasileiro, voz nativa do clone. Normas virais e hor\u00e1rios otimizados pro BR."
        },
        {
          "label": "PT-BR + EN (bil\u00edngue)",
          "description": "Dobra o esfor\u00e7o de produ\u00e7\u00e3o mas abre o mercado global de IA. Clone de voz precisa de pt + en consistentes."
        },
        {
          "label": "EN primeiro (global de IA)",
          "description": "Mira o mercado global de tech/IA desde o dia 1. Maior teto de alcance, mais competi\u00e7\u00e3o."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Para o avatar treinado fiel à sua pessoa e voz (talking-head digital + clone de voz), qual caminho a pesquisa deve priorizar e recomendar?"="Vamos contruir nosso próprio módilo de Avatar ou Clone AI ou Person AI dentro do menu Canvas  temos que criar esse novo módulo, ou me diga se é melhor manter isso dentro do stuido, que foi desde o inicio a ideia, utilizar o canvas studio criando mais tipos de nós com referencia no antigo freepik atual magnific e tambem o martini art e martini film mas de preferencia focar no maginific e sempre per user. Usuários do MCORCH (incluindo o usuário 0) deve tambem usar as estrategias e possibilidade de encontrar a melhor estrategia dentro do ecossistema então o Clone AI ou Avatar AI pois os usuários podem querer se clonar ou somente criar um personagem avatar para criar audiencia nas redes sociais", "Quais canais entram na cadência de 30 dias? (avatar é vídeo-first — marque todos que quer ativar)"="Todos os canais devem ser usados para cadências ou seja postagens automaticas em todas", "Sobre o que a marca Gabriel AI fala? Isso define os temas e os produtos que entram na cadência."="Mix: autoridade + educação + produtos", "Em qual idioma a marca publica nos primeiros 30 dias? (muda as normas virais que pesquiso e o alcance)"="PT-BR + EN (bilíngue)". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(23:42:29)*


## 🤖 Claude *(23:42:37)*

Perfeito, Maestro — recebido e travado. Sua resposta **muda a escala**: o avatar não é um asset único do Gabriel — é um **módulo per-user "Avatar / Clone AI / Person AI"** dentro do Canvas Studio (novos tipos de nós), espelhando **Magnific** (foco), Freepik e "Martin/Martini Art + Film", onde qualquer usuário (User 0 incluso) pode se clonar ou criar um personagem. Isso é **módulo novo → BoK Gate**. O caminho correto é exatamente o que você pediu: **deepsearch força-total primeiro** → blueprint-semente → você aprova → BoK → código. Nada de código antes disso.

Decisões cravadas que vão alimentar TODA a pesquisa:
- **Avatar** = módulo próprio per-user no Canvas Studio (Magnific-primário, BYOK), clone-de-si **ou** personagem
- **Canais** = todos, cadência automática em todos
- **Pilares** = autoridade + educação + produtos
- **Idioma** = PT-BR + EN bilíngue

Disparando a **deepsearch força-total** agora — 14 frentes (10 web + 4 internas do nosso código), verificação adversarial das claims que sustentam o plano, crítica de gaps, e síntese no blueprint-semente `docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md`. Roda em background; eu te trago o sumário executivo + a cadência de 30 dias + a recomendação do avatar quando fechar.

## 🤖 Claude *(23:44:05)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'gabriel-ai-content-engine-deepsearch',\n  description: 'Forca-total deepsearch: estrategia de conteudo viral + cadencia 30 dias + modulo Avatar/Clone AI per-user -> blueprint-semente da BoK avatar-clone-ai',\n  phases: [\n    { title: 'Research', detail: '10 frentes web + 4 frentes internas (codebase) em paralelo' },\n    { title: 'Synthesize', detail: 'Rascunho do blueprint + extrai claims que sustentam o plano' },\n    { title: 'Verify', detail: 'Verificacao adversarial das claims load-bearing' },\n    { title: 'Critique', detail: 'Caca gaps e frentes faltantes' },\n    { title: 'Finalize', detail: 'Escreve o blueprint-semente + retorna sumario executivo' },\n  ],\n}\n\nconst CONTEXT = `\nPROGRAM: \"Gabriel AI\" \u2014 building a faithful, bilingual (PT-BR + EN) AI-thought-leader persona that posts video-first content across ALL channels (YouTube Shorts+long, TikTok, Instagram Reels, LinkedIn, X) on a fully-automated 30-day cadence via MCORCH's existing \"Viral Autopilot\" engine. Gabriel AI is instance-zero of a generalized capability.\n\nSOVEREIGN DECISIONS (already made \u2014 research must SERVE these, not re-open them):\n- AVATAR = build OUR OWN per-user \"Avatar / Clone AI / Person AI\" MODULE inside the Canvas Studio (new typed nodes), NOT a one-off asset and NOT a single SaaS lock-in. Reference products to emulate: Magnific AI (PRIMARY focus), Freepik AI, and tools the Sovereign calls \"Martin/Martini Art\" and \"Martini Film\". Always per-user / BYOK (each MCORCH user brings their own key). Users can clone THEMSELVES (face + cloned voice + \"cloned brain\"/knowledge) OR create a fictional character avatar to grow a social audience.\n- CHANNELS = all of them, automated cadence on every one.\n- PILLARS = mix of authority (build-in-public MCORCH / AGI->ASI journey) + practical AI/automation education + product/affiliate tie-ins.\n- LANGUAGE = bilingual PT-BR + EN.\n- \"Cloned brain\" = the persona's knowledge/tone is grounded in MCORCH's existing memory mesh.\n\nLAW 1 (Materiality): every web claim MUST carry the EXACT source URL you read it from. Never fabricate a number, a tool capability, or a URL. Prefer 2025-2026 sources. Where PT-BR (Brazil) and EN/global norms differ, give BOTH.\n`;\n\nconst WEB_FRONTS = [\n  { key: 'youtube', prompt: 'FRONT: YouTube viral playbook 2025-2026 for an AI/tech founder persona. Research with sources: optimal Shorts duration & retention patterns, long-form ideal length, hook techniques (first 3 seconds), title/thumbnail patterns, posting frequency for fast channel growth, best posting times, algorithm signals (watch time, CTR, average view duration), the Shorts->long-form funnel, and which formats win for AI/automation education + build-in-public content.' },\n  { key: 'tiktok', prompt: 'FRONT: TikTok viral playbook 2025-2026 for an AI/tech founder persona. Research with sources: optimal video duration, hook patterns, trending audio usage, caption/hashtag strategy, posting frequency and best times, the For You algorithm signals, watch-time/completion-rate thresholds, and which formats win for AI/automation + founder content. Include Brazil-specific TikTok norms.' },\n  { key: 'reels', prompt: 'FRONT: Instagram Reels viral playbook 2025-2026 for an AI/tech founder persona. Research with sources: optimal Reel duration, hook + cover/thumbnail patterns, trending audio, Reels vs carousels for reach, posting frequency, best times, algorithm/reach signals in 2026, and how Reels interplay with Stories. Include Brazil norms.' },\n  { key: 'linkedin-x', prompt: 'FRONT: LinkedIn + X (Twitter) playbook 2025-2026 for an AI thought-leader. Research with sources: text-post hook patterns, document/carousel posts on LinkedIn, video-repurpose strategy, optimal posting cadence, what drives reach/impressions in 2026 on each, thread strategy on X, and how to repurpose ONE video pillar into native LinkedIn + X posts.' },\n  { key: 'cadence', prompt: 'FRONT: 30-day content cadence & calendar design for a SOLO creator scaling output via an AI avatar. Research with sources: how many posts/day per platform is optimal vs spammy, batching & repurposing workflows (1 pillar -> many native variants), content-pillar rotation ratios (authority / education / product), ramp-up schedule for a brand-NEW account (avoid spam-flagging), consistency cadence science, and concrete published example 30-day calendars. Give both PT-BR and EN norms.' },\n  { key: 'avatar-tech', prompt: 'FRONT: AI avatar / digital twin / talking-head technology 2025-2026. Research BOTH commercial (HeyGen, Synthesia, Argil, Captions AI, D-ID, Arcads, Hedra) AND open-source self-hostable (SadTalker, Hallo, EMO, LivePortrait, OmniHuman) with sources: faithfulness to a real person, lip-sync quality, per-video cost, PUBLIC API availability, training requirements (how many photos/seconds of video to train a faithful clone), and consistency across many videos. Flag which support a per-user / BYOK (key-per-user) integration. Recommend the best path for a faithful talking-head of a real founder embeddable as a Canvas node.' },\n  { key: 'voice-clone', prompt: 'FRONT: Voice cloning 2025-2026 for PT-BR + EN. Research ElevenLabs, PlayHT, Cartesia, and open-source (XTTS-v2/Coqui, F5-TTS, OpenVoice, MeloTTS, Fish-Speech) with sources: Brazilian-Portuguese quality, cloning data needed, latency, cost, PUBLIC API availability, self-host feasibility, and emotional/prosody control. Recommend the best for a faithful BILINGUAL founder voice with per-user/BYOK.' },\n  { key: 'reference-tools', prompt: 'FRONT: Identify and analyze the reference products the Sovereign named. (1) Magnific AI \u2014 PRIMARY focus: research with sources its features (Mystic generator, upscale, relight, style transfer, character/identity consistency) and CRITICALLY whether it has a PUBLIC API for a per-user/BYOK integration + pricing. (2) Freepik AI suite \u2014 features + API + pricing. (3) Tools he calls \"Martin/Martini Art\" and \"Martini Film\" \u2014 IDENTIFY EXACTLY what these are (strong candidates to investigate: Krea AI, Higgsfield, Hailuo/MiniMax, Marey by Moonvalley, Kling, Runway, Pika, \"Martin AI\") and report what each does + character consistency + API availability. For EVERY tool: API availability + per-user feasibility is the load-bearing question.' },\n  { key: 'persona-clone', prompt: 'FRONT: Building a faithful AI persona / \"digital clone\" of a real person for social media 2025-2026. Research with sources: the AI-clone-influencer trend, how creators clone face+voice+\"brain\"(knowledge/tone) to scale content, brand-voice consistency techniques, and IMPORTANT: platform rules & required labeling for AI-generated / synthetic media on YouTube, TikTok, and Meta (Instagram) in 2026 \u2014 what disclosure is mandatory. Also monetization patterns (affiliate, product, sponsorship) for an AI-thought-leader persona. Give PT-BR + EN.' },\n  { key: 'consistency', prompt: 'FRONT: Keeping an AI avatar/character VISUALLY faithful & consistent across hundreds of posts. Research with sources: seed/reference image threading, IP-Adapter, character LoRA training on a specific person, FaceID/InstantID/PuLID, Magnific-style enhancement for consistency, and QA techniques to detect identity drift. How to architect a \"reference-locked\" character so every generated frame looks like the same person. Cite specific tools + techniques.' },\n];\n\nconst INTERNAL_FRONTS = [\n  { key: 'canvas-nodes', prompt: 'INTERNAL REPO EXPLORATION (read-only) of /home/gcrUX/htdocs/constellation-orchestra. Map the Canvas Studio node architecture so we can add NEW typed nodes for an \"Avatar/Clone AI\" capability. Find the ReactFlow node-type registry, the EXACT node shape & Handle ids, how nodes persist (vm_canvas_projects.graph), and how a node runs via canvas-execute. Look under src/components/orchestrator/, the Canvas/VideoStudio pages in src/pages/, src/store/useOrchestrationStore.ts, supabase/functions/canvas-execute, and the canvas-studio-cinematic skill in .claude/skills/. Report exact file paths + the precise seam where new node types plug in.' },\n  { key: 'creative-reuse', prompt: 'INTERNAL REPO EXPLORATION (read-only) of /home/gcrUX/htdocs/constellation-orchestra. Inventory the existing creative pipeline we can REUSE for an avatar/clone module: supabase/functions/generate-image, supabase/functions/canvas-execute, the HyperFrames video motor (scripts/hyperframes/, scripts/video-bridge.ts), the Channel Reshaper (supabase/functions/reshape-pillar + atomizer), the creative_assets spine (migration + RPC + dual-write), and the Vision QA gate (scripts/qa/vision-qa.ts). For each: what it does, key files, and how it could serve avatar generation / voice / consistency / video. Report reusable seams + gaps.' },\n  { key: 'autopilot-publish', prompt: 'INTERNAL REPO EXPLORATION (read-only) of /home/gcrUX/htdocs/constellation-orchestra. Map the Viral Autopilot + auto-publish + per-channel publishing seams. Find supabase/functions/{orchestrate-content,orchestrate-step,autopilot-run,autopilot-cadence-cron,auto-publish,publish-social,publish-meta}, the social_platform enum + social_accounts / social_app_config tables, and the known gap where auto-publish does not pass video_url + the VIDEO_FLOW_PLATFORMS concept. Report EXACTLY what is net-new to publish avatar VIDEO automatically to YouTube + TikTok + Instagram Reels + LinkedIn + X, and where the avatar video plugs into the 30-day cadence loop.' },\n  { key: 'byok-creds', prompt: 'INTERNAL REPO EXPLORATION (read-only) of /home/gcrUX/htdocs/constellation-orchestra. Map the per-user BYOK credential model so we can add Magnific / Freepik / voice-clone keys per user. Find the user_api_keys VIEW + decrypted_user_api_keys + the Vault encryption pattern, existing key columns, the INSTEAD OF trigger, and the settings UI hook (src/hooks/useUserApiKeys.ts) + settings card. Cite an existing precedent (e.g. a recent migration that added a new per-user provider key column). Report the exact recipe (column + UI + lookup helper) to add a new per-user provider key following the API Tenancy Model.' },\n];\n\nconst FRONT_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['front', 'keyFindings', 'recommendations', 'openQuestions'],\n  properties: {\n    front: { type: 'string' },\n    keyFindings: { type: 'array', items: { type: 'object', additionalProperties: false,\n      required: ['claim', 'detail', 'sourceUrl', 'confidence'],\n      properties: {\n        claim: { type: 'string' }, detail: { type: 'string' },\n        sourceUrl: { type: 'string' }, confidence: { enum: ['high', 'medium', 'low'] },\n      } } },\n    recommendations: { type: 'array', items: { type: 'string' } },\n    openQuestions: { type: 'array', items: { type: 'string' } },\n  },\n};\n\nconst INTERNAL_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['area', 'findings', 'integrationSeams', 'reusable', 'gaps'],\n  properties: {\n    area: { type: 'string' },\n    findings: { type: 'array', items: { type: 'object', additionalProperties: false,\n      required: ['what', 'files', 'detail'],\n      properties: { what: { type: 'string' }, files: { type: 'array', items: { type: 'string' } }, detail: { type: 'string' } } } },\n    integrationSeams: { type: 'array', items: { type: 'string' } },\n    reusable: { type: 'array', items: { type: 'string' } },\n    gaps: { type: 'array', items: { type: 'string' } },\n  },\n};\n\nconst SYNTH_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['draftMarkdown', 'loadBearingClaims'],\n  properties: {\n    draftMarkdown: { type: 'string' },\n    loadBearingClaims: { type: 'array', items: { type: 'object', additionalProperties: false,\n      required: ['claim', 'whyItMatters'],\n      properties: { claim: { type: 'string' }, whyItMatters: { type: 'string' } } } },\n  },\n};\n\nconst VERDICT_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['claim', 'verdict', 'evidence', 'sourceUrl'],\n  properties: {\n    claim: { type: 'string' }, verdict: { enum: ['confirmed', 'refuted', 'uncertain'] },\n    evidence: { type: 'string' }, sourceUrl: { type: 'string' },\n  },\n};\n\nconst CRITIQUE_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['gaps', 'missingFronts', 'corrections'],\n  properties: {\n    gaps: { type: 'array', items: { type: 'string' } },\n    missingFronts: { type: 'array', items: { type: 'string' } },\n    corrections: { type: 'array', items: { type: 'string' } },\n  },\n};\n\nconst FINAL_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['path', 'executiveSummary', 'avatarRecommendation', 'cadenceSummary', 'openDecisions'],\n  properties: {\n    path: { type: 'string' },\n    executiveSummary: { type: 'string' },\n    avatarRecommendation: { type: 'string' },\n    cadenceSummary: { type: 'string' },\n    openDecisions: { type: 'array', items: { type: 'string' } },\n  },\n};\n\nphase('Research')\nlog('Disparando 10 frentes web + 4 frentes internas (forca total)...')\nconst webThunks = WEB_FRONTS.map(f => () => agent(CONTEXT + '\\n\\n' + f.prompt + '\\n\\nReturn structured findings; every keyFinding MUST carry the exact source URL.', { label: 'web:' + f.key, phase: 'Research', schema: FRONT_SCHEMA, agentType: 'deepsearch-blueprint' }))\nconst internalThunks = INTERNAL_FRONTS.map(f => () => agent(f.prompt, { label: 'repo:' + f.key, phase: 'Research', schema: INTERNAL_SCHEMA, agentType: 'Explore' }))\nconst research = (await parallel([...webThunks, ...internalThunks])).filter(Boolean)\nlog('Frentes concluidas: ' + research.length + '/14. Sintetizando...')\n\nphase('Synthesize')\nconst synth = await agent(\n  CONTEXT + '\\n\\nYou are the BLUEPRINT SYNTHESIZER for MCORCH. Below is the full JSON of all 14 research fronts (10 web with source URLs, 4 internal codebase maps).\\n\\n=== RESEARCH JSON ===\\n' + JSON.stringify(research) + '\\n=== END ===\\n\\n'\n  + 'Produce a COMPREHENSIVE draft blueprint-semente in Brazilian Portuguese (executive register; English for technical terms) that a BoK Scribe will later expand. It MUST contain these sections:\\n'\n  + '1. Tese & posicionamento da marca \"Gabriel AI\" (autoridade + educacao + produtos, bilingue PT-BR/EN).\\n'\n  + '2. Estrategia de conteudo viral POR CANAL (YouTube Shorts+longo, TikTok, IG Reels, LinkedIn, X) \u2014 duracao otima, hooks, frequencia, melhores horarios, formatos vencedores \u2014 com a URL-fonte de cada numero.\\n'\n  + '3. CADENCIA DE 30 DIAS concreta: uma TABELA com cada dia/semana, por canal, com formato, duracao, pilar (autoridade/educacao/produto), tema, produto/afiliado, idioma (PT-BR/EN), e a estrategia de repurpose (1 pilar -> N variantes nativas reusando o Channel Reshaper).\\n'\n  + '4. MODULO Avatar/Clone AI (per-user, Canvas Studio): tipos de nos novos propostos, pipeline (referencia de rosto -> consistencia -> talking-head -> voz clonada -> video 9:16), espelhando Magnific (foco) + Freepik + Martin/Martini Art/Film; recomendacao de stack (commercial vs self-host) por sub-capacidade com tradeoffs e custo; modelo BYOK per-user.\\n'\n  + '5. Consistencia & QA do avatar (reference-lock, FaceID/LoRA, Vision QA gate existente).\\n'\n  + '6. MAPA DE INTEGRACAO no ecossistema existente (Canvas nodes, generate-image, canvas-execute, HyperFrames, Channel Reshaper, creative_assets, Viral Autopilot, auto-publish) \u2014 o que reusa e o que e net-new por canal.\\n'\n  + '7. Compliance: regras de rotulagem de midia sintetica (YouTube/TikTok/Meta) por canal.\\n'\n  + '8. OTDs (Open Technical Decisions, ids OTD-AC-001..) + FMEA (FM-AC-001..) iniciais.\\n'\n  + '9. Roadmap de FATIAS (pieces) na ordem de construcao, terminando na juncao com o Viral Autopilot.\\n\\n'\n  + 'Also return loadBearingClaims: the 8-12 factual claims this whole plan depends on (especially: tool API availability for per-user BYOK, optimal durations/frequencies, voice-clone PT-BR quality, what \"Martini Art/Film\" actually are) that MUST be adversarially verified before code.',\n  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA, agentType: 'general-purpose', effort: 'high' })\n\nphase('Verify')\nconst claims = (synth.loadBearingClaims || []).slice(0, 12)\nlog('Verificando ' + claims.length + ' claims load-bearing de forma adversarial...')\nconst verdicts = (await parallel(claims.map((c, i) => () => agent(\n  'Adversarially fact-check this load-bearing claim for an MCORCH product blueprint. Try to REFUTE it; default to \"uncertain\" if you cannot find a clear authoritative source. Search the web and cite the exact source URL.\\n\\nCLAIM: ' + c.claim + '\\nWHY IT MATTERS: ' + c.whyItMatters,\n  { label: 'verify:' + i, phase: 'Verify', schema: VERDICT_SCHEMA, agentType: 'deepsearch-blueprint' }))) ).filter(Boolean)\nconst refuted = verdicts.filter(v => v.verdict === 'refuted')\nlog('Verificacao: ' + verdicts.filter(v => v.verdict === 'confirmed').length + ' confirmadas, ' + refuted.length + ' refutadas, ' + verdicts.filter(v => v.verdict === 'uncertain').length + ' incertas.')\n\nphase('Critique')\nconst critique = await agent(\n  CONTEXT + '\\n\\nYou are an adversarial CRITIC reviewing a draft blueprint-semente before it seeds a BoK. Find what is MISSING or WEAK.\\n\\n=== DRAFT ===\\n' + synth.draftMarkdown + '\\n=== END DRAFT ===\\n\\n'\n  + '=== VERIFICATION VERDICTS ===\\n' + JSON.stringify(verdicts) + '\\n=== END ===\\n\\n'\n  + 'Report: gaps (important things absent or under-specified \u2014 e.g. cost model, multi-tenant risk, a channel under-covered, the 30-day cadence not concrete enough), missingFronts (research angles not covered), and corrections (claims contradicted by the verdicts that must be fixed/softened in the final).',\n  { label: 'critique', phase: 'Critique', schema: CRITIQUE_SCHEMA, agentType: 'general-purpose', effort: 'high' })\n\nphase('Finalize')\nconst final = await agent(\n  CONTEXT + '\\n\\nYou are the FINALIZER. Write the production-grade blueprint-semente to the file docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md (run `mkdir -p docs/bok/avatar-clone-ai` first; cwd is the repo root /home/gcrUX/htdocs/constellation-orchestra).\\n\\n'\n  + 'Start from this DRAFT, then (a) apply every correction implied by the verdicts (mark any REFUTED claim clearly and remove/soften it), (b) close the gaps and missing fronts from the critique, (c) keep EVERY source URL inline as a citation (Law 1).\\n\\n'\n  + '=== DRAFT ===\\n' + synth.draftMarkdown + '\\n=== END DRAFT ===\\n\\n'\n  + '=== VERDICTS ===\\n' + JSON.stringify(verdicts) + '\\n=== END ===\\n\\n'\n  + '=== CRITIQUE ===\\n' + JSON.stringify(critique) + '\\n=== END ===\\n\\n'\n  + 'The final doc MUST keep all 9 sections from the draft spec, with a CONCRETE 30-day cadence table and a clear avatar-module architecture. Write it in Brazilian Portuguese (executive register, English technical terms), matching MCORCH deepsearch-blueprint style (precedents: docs/bok/security/00-deepsearch-blueprint.md and docs/bok/vision-mcp/00-deepsearch-blueprint.md \u2014 Read one for format). End the doc with the next step: run `/bok-scribe avatar-clone-ai` to seal the BoK suite before any code.\\n\\n'\n  + 'After writing, return: path, executiveSummary (8-12 lines max), avatarRecommendation (the recommended per-user avatar stack + why), cadenceSummary (the gist of the 30-day cadence: posts/day per channel + pillar mix), and openDecisions (the questions only the Sovereign can resolve before /bok-scribe).',\n  { label: 'finalize', phase: 'Finalize', schema: FINAL_SCHEMA, agentType: 'general-purpose', effort: 'high' })\n\nlog('Blueprint-semente escrito em ' + final.path)\nreturn { final, refutedCount: refuted.length, verdictCount: verdicts.length, fronts: research.length }",
  "description": "Deepsearch for\u00e7a-total Gabriel AI content engine"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: w73j82355
> Summary: Forca-total deepsearch: estrategia de conteudo viral + cadencia 30 dias + modulo Avatar/Clone AI per-user -> blueprint-semente da BoK avatar-clone-ai
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/subagents/workflows/wf_64171f41-742
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/workflows/scripts/gabriel-ai-content-engine-deepsearch-wf_64171f41-742.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/workflows/scripts/gabriel-ai-content-engine-deepsearch-wf_64171f41-742.js"} to iterate without resending the script.)
> Run ID: wf_64171f41-742
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/workflows/scripts/gabriel-ai-content-engine-deepsearch-wf_64171f41-742.js", resumeFromRunId: "wf_64171f41-742"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(23:44:22)*


## 🤖 Claude *(23:44:35)*

Deepsearch força-total **rodando em background** (run `wf_64171f41-742`, 14 frentes + verificação adversarial + crítica + síntese). Você acompanha ao vivo em `/workflows`; eu sou notificado quando fechar e trago o resultado mastigado.

**O que vai sair dela** (escrito em `docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md`):
1. Estratégia viral **por canal** (YT/TikTok/Reels/LinkedIn/X) — duração, hook, frequência, horário, formato — cada número com URL-fonte
2. **Cadência de 30 dias concreta** (tabela: dia × canal × formato × duração × pilar × tema × produto × idioma + repurpose via Channel Reshaper)
3. **Módulo Avatar/Clone AI** per-user no Canvas Studio (novos nós, Magnific-primário, BYOK, clone-de-si ou personagem) + recomendação de stack
4. Consistência/QA do avatar · mapa de integração no ecossistema · compliance de rótulo de mídia sintética · OTDs/FMEA · roadmap de fatias

**Roadmap do programa "Gabriel AI" (Closed-Loop)** — onde estamos e o que vem:

| # | Etapa | Status |
|---|-------|--------|
| 1 | **Deepsearch força-total** → blueprint-semente | 🔄 rodando agora |
| 2 | Você revisa o blueprint + cadência + recomendação de avatar | ⏳ aguarda (1) |
| 3 | `/bok-scribe avatar-clone-ai` → sela a BoK (MRD→SDD + Pattern Conformance) | 🚪 BoK Gate |
| 4 | Construir as **peças**: módulo Avatar/Clone AI · clone de voz · pipeline de consistência · branches de publish YT/TikTok | ⏳ pós-BoK |
| 5 | **Juntar tudo com o Viral Autopilot** + ligar a cadência de 30 dias | 🎯 alvo final |

Decisões que provavelmente vão precisar do seu OK no passo 2 (a pesquisa vai trazer os dados, mas a escolha é sua): se o Magnific tem API pública pra BYOK per-user (se não tiver, qual é o substituto), e self-host vs SaaS para o clone de voz PT-BR+EN.

Enquanto roda, **não toco em código** (Closed-Loop — peça nasce da BoK, que nasce do blueprint). Te aviso assim que o blueprint estiver no disco. 🛰️

## 👤 User *(00:28:08)*

<task-notification>
<task-id>w73j82355</task-id>
<tool-use-id>toolu_01Q5yMfeurnD7XuzYAx4CgSg</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/tasks/w73j82355.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Forca-total deepsearch: estrategia de conteudo viral + cadencia 30 dias + modulo Avatar/Clone AI per-user -&gt; blueprint-semente da BoK avatar-clone-ai" completed</summary>
<result>{"final":{"path":"/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md","executiveSummary":"Blueprint-semente do programa \"Gabriel AI\" escrito em PT-BR (registro executivo, termos técnicos em EN), 421 linhas, 9 seções, estilo deepsearch MCORCH (precedente vision-mcp). Apliquei TODOS os 13 veredictos: refutações marcadas e corrigidas inline — HeyGen Avatar V (NÃO $3/min self-serve: $4/min Digital Twin, API direta indisponível, BYOK partnership-gated); ElevenLabs (NÃO \"PVC+v3\": v2-PVC ou IVC-v3, code-switching PT-BR↔EN é falha conhecida); F5-TTS e FLUX.1-dev marcados non-commercial; números do Identity Gate (~85%/0.7-0.8) removidos por atribuição falsa, princípio FAR/FRR/EER preservado; CONAR separado por jurisdição (NÃO impõe AI-label, só solidary-liability + identificação de persona virtual); reshaper→publish-social CORRIGIDO (caminho JÁ existe wired no codebase — gaps reais = CHECK de platforms + VIDEO_FLOW_PLATFORMS + step avatar_generation); ramp 1→2→3/dia rebaixado a heurística ilustrativa, citação reelforgeai.io removida. Fechei os gaps da crítica: economics/unit-cost (§8.5, maior gap), duplicação bilíngue 2× (OTD-AC-012), storage/RLS/erase de PII biométrica (§4.4b), consent+identity-verification self-clone como gate de lançamento (§5.4), X reply engine (OTD-AC-009), North-Star de marca (§8.4), C2PA como requisito legal não-polish (§7), 7 frentes pendentes (F1-F7), Pattern Conformance esboçada. Tabela de cadência concreta Dia 1→30 com funil semanal, idioma-âncora alternado e tie-ins. Todas as URLs-fonte preservadas inline (Lei 1).","avatarRecommendation":"Stack per-user/BYOK multi-provider (espelha API Tenancy Model), NÃO lock-in SaaS único. Pipeline: avatarIdentity → voiceClone → avatarScript → talkingHead → avatarEnhance → Identity Gate → C2PA → creative_assets → Viral Autopilot. Recomendações por sub-capacidade (com caveats verificados): IDENTIDADE = Higgsfield Soul ID (≥20 fotos, 3-5 min) — mas TREINO via API self-serve é NÃO-VERIFICADO, ler docs logadas antes do SDD; alternativa soberana LoRA FLUX (⚠️ checkpoint base FLUX.1-dev é non-commercial). VOZ = ElevenLabs PVC sobre Multilingual-v2 OU IVC/Voice-Design sobre v3 (NÃO \"PVC+v3\"), $0.05-0.10/1k chars, BYOK header trivial; Cartesia Sonic (variante Brazilian) p/ real-time; NÃO usar F5-TTS (pesos CC-BY-NC). TALKING-HEAD = ❌ HeyGen Avatar V NÃO ancora BYOK self-serve (partnership-gated, $4/min, API direta indisponível) → re-avaliar Hedra Character-3 ($0.05/min)/OmniHuman OU modelar tenancy master-account; núcleo verdadeiro = motor por-vídeo-referência supera por-foto em consistência. ENHANCE = Magnific (≡ Freepik, header x-magnific-api-key) só como polish final, NUNCA autor de identidade — ⚠️ exige plano PAGO per-tenant (free tier não gera key). Consistência garantida por Identity Gate ArcFace (limiar calibrado empiricamente, NÃO hardcodado) reusando o Vision QA existente (cost 0). Por quê: módulo próprio dá soberania, billing mcoCoins atômico, isolamento de risco per-tenant, e evita a armadilha de qualquer SaaS único cujo ToS/preço/disponibilidade muda (HeyGen provou isso).","cadenceSummary":"30 dias = 1ª perna de compromisso de 90d, com RAMP anti-shadowban server-side (1→2→3/dia ILUSTRATIVO, não regra de plataforma) e 4 semanas-funil: S1 Awareness · S2 Education · S3 Social-Proof · S4 Conversion. Steady-state pós-ramp por canal: YouTube Shorts 5/sem + longo 1-2/sem (8-15min, atomizado em 3-5 Shorts com end-card ao mesmo tópico); TikTok 3-5/sem (15-35s); IG Reels 4-5/sem + Stories diárias (7-30s); LinkedIn 3-4/sem (carrossel/vídeo nativo&lt;90s/texto); X 3-5/dia (thread 3-6 + vídeo 9:16 nativo). Mix de pilares: ~40% educação (AI/automação prática) + ~40% autoridade/build-in-public (jornada AGI→ASI) + ≤20% produto/afiliado ML — conta NOVA começa 70/20/10 e relaxa após 3 semanas. 1 pilar-fonte/dia → N variantes NATIVAS via Channel Reshaper (mesmo MP4 9:16, hook/corte/legenda mudam por canal). Bilíngue = idioma-âncora alterna PT-BR/EN por dia (NÃO duplica nº de pilares-fonte; trilha B reusa o mestre re-locando voz clonada cross-lingual — decisão OTD-AC-012 a ratificar, pois \"2 línguas no mesmo dia\" dobraria custo). Anchor de volume: vidIQ 12+ uploads/mês = ~8x views/~3x subs (estudo 5,08M canais). Tabela concreta Dia 1→30 entregue.","openDecisions":["OTD-AC-001 — Motor talking-head primário: HeyGen está REFUTADO como BYOK self-serve (partnership-gated, $4/min, API direta indisponível). Aceitar Hedra/OmniHuman (self-serve, por-imagem, menor fidelidade) OU autorizar modelo de tenancy master-account/partnership (muda economics + quem-paga)? Bloqueante antes do SDD.","OTD-AC-009 — Motor de REPLY do X (multiplicador ~150x author-reply) é um agent loop conversacional real-time NET-NEW que o Autopilot broadcast-only não tem. Entra no escopo core OU a promessa 'paridade de automação em TODOS os canais' é explicitamente suavizada (X cresce capado sem ele)?","OTD-AC-012 — Modelo de duplicação bilíngue: cada pilar renderiza UMA vez (idioma-âncora alterna por dia, trilha B reusa mestre) OU as DUAS línguas no MESMO dia (dobra volume/custo de render ~2×)? Determina o custo mensal do ciclo.","OTD-AC-013 / §8.4 — North-Star de marca: brand evangelism não produz R$ direto, então o trigger de migração de Owner (Sovereign→marketing-growth) e a definição de sucesso estão indefinidos. Qual métrica (seguidores qualificados? hook_rate agregado? 1ª conversão atribuída?) destrava a ownership?","§5.4 / OTD-AC-010 — Para a capacidade GENERALIZADA (clonar qualquer user), como provar que o user clona A SI MESMO e não um terceiro privado real (TikTok bane sintético de privados reais mesmo rotulado)? Aceitar selfie-liveness/attestation no onboarding como gate de lançamento (não OTD diferido)?","§4.4 / Front F1 — BYOK pass-through legal difere por provider (Magnific exige plano PAGO per-tenant; HeyGen partnership; ElevenLabs/Cartesia/Higgsfield a verificar). Autorizar a frente de leitura de ToS por provider antes do FRD, e aceitar que alguns providers podem NÃO permitir a chave do end-user guardada pelo MCORCH?","§7 / OTD-AC-008 — C2PA embedding é REQUISITO LEGAL (EU AI Act Art.50 a partir de 02/08/2026, machine-readable) mas pode quebrar o determinismo sha256 (NFR-VS-016) do HyperFrames. Autorizar spike técnico para resolver embed-vs-determinismo antes de selar a arquitetura de render?","Front F2 (viabilidade) — Antes de escalar: pesquisar case studies REAIS de canais 100%-avatar com dados de retenção/crescimento, dado o escrutínio MAIOR a sintético (TikTok detecta no upload). É a hipótese que pode invalidar o programa inteiro — aceitar como gate de Fatia 0?"]},"refutedCount":6,"verdictCount":12,"fronts":14}</result>
<usage><agent_count>29</agent_count><subagent_tokens>2051971</subagent_tokens><tool_uses>435</tool_uses><duration_ms>2642402</duration_ms></usage>
</task-notification>

## 🤖 Claude *(00:29:11)*


## 🤖 Claude *(00:29:13)*

Deepsearch fechou — **14 frentes, 12 claims verificadas (6 refutadas), 29 agentes, ~2M tokens, 44 min**. Antes de te apresentar, vou **verificar materialmente** que o blueprint existe no disco (Lei 1 — não confio na claim do agente) e lê-lo inteiro.

## 🤖 Claude *(00:29:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== ls ===\"; ls -la docs/bok/avatar-clone-ai/ 2>&1; echo \"=== wc ===\"; wc -l docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md 2>&1; echo \"=== git status ===\"; git status --short docs/bok/avatar-clone-ai/ 2>&1; echo \"=== section headers ===\"; grep -nE '^#{1,3} ' docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md 2>&1 | head -60",
  "description": "Verify blueprint file exists, line count, git status, section headers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === ls ===
> total 64
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun 29 21:27 .
> drwxrwxr-x 27 gcrUX  gcrUX   4096 Jun 29 21:21 ..
> -rw-rw-r--  1 ubuntu ubuntu 55068 Jun 29 21:27 00-deepsearch-blueprint.md
> === wc ===
> 421 docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md
> === git status ===
> ?? docs/bok/avatar-clone-ai/
> === section headers ===
> 1:# 🎭 MCORCH Avatar/Clone AI — Programa "Gabriel AI" (persona-IA bilíngue, video-first, multicanal)
> 16:## 1. Tese & posicionamento da marca "Gabriel AI"
> 35:## 2. Estratégia de conteúdo viral POR CANAL (com URL-fonte de cada número)
> 39:### 2.1 YouTube (Shorts + longo) — funil Shorts→longo
> 61:### 2.2 TikTok
> 77:### 2.3 Instagram Reels
> 91:### 2.4 LinkedIn (canal de PROFUNDIDADE)
> 103:### 2.5 X/Twitter (único canal onde TEXTO bate vídeo)
> 114:### 2.6 Repurpose 1→N (COPE / atomização)
> 119:## 3. CADÊNCIA DE 30 DIAS concreta
> 138:### 3.1 Cadência dia-a-dia concreta (30 dias) — 1 pilar → N variantes via Channel Reshaper
> 181:## 4. MÓDULO Avatar/Clone AI (per-user, Canvas Studio)
> 185:### 4.1 Pipeline (nós tipados novos no Canvas)
> 209:### 4.2 Recomendação de stack por sub-capacidade (commercial vs self-host) — verificada e CORRIGIDA
> 221:### 4.3 Os produtos-referência do Sovereign — desambiguação verificada
> 225:### 4.4 Modelo BYOK per-user + storage de artefatos biométricos
> 238:## 5. Consistência & QA do avatar
> 248:### 5.1 Identity Gate (novo nó pós-geração) — ❌ números do draft REFUTADOS, princípio preservado
> 255:### 5.2 Reuso do Vision QA existente
> 258:### 5.3 Gate de licença (FM-AC-001) — verificado
> 261:### 5.4 Consentimento & personalidade-legal (gap de lançamento, NÃO OTD a diferir)
> 267:### 5.5 ⚠️ Hipótese de viabilidade (Front F2) — avatares sintéticos crescem em 2025-2026?
> 272:## 6. MAPA DE INTEGRAÇÃO no ecossistema existente
> 274:### 6.1 O que REUSA (já em produção)
> 289:### 6.2 O que é NET-NEW por canal (gaps CORRIGIDOS contra o codebase real)
> 309:## 7. Compliance — rotulagem de mídia sintética por canal (SEPARADO POR JURISDIÇÃO)
> 330:## 8. OTDs, FMEA, Frentes-pendentes, Pattern Conformance & Economics
> 332:### 8.1 OTDs (Open Technical Decisions)
> 350:### 8.2 FMEA (modos de falha)
> 367:### 8.3 Frentes de pesquisa pendentes (a fechar antes do FRD)
> 376:### 8.4 Métricas de sucesso da MARCA (gap do draft — definir antes do /bok-scribe)
> 382:### 8.5 ⚠️ Economics — unit cost a modelar (MAIOR GAP do draft, F5)
> 390:### 8.6 Pattern Conformance Declaration (esboço — Gate Step 3.5)
> 402:## 9. Roadmap de FATIAS (ordem de construção)
> 419:## Próximo passo (Gate Closed-Loop)
> ```

## 🤖 Claude *(00:29:19)*


## 🤖 Claude *(00:29:20)*

Material confirmado: **55KB · 421 linhas · 9 seções + Próximo passo · untracked** (`?? docs/bok/avatar-clone-ai/`). Estrutura completa. Lendo o conteúdo inteiro para te apresentar com fidelidade.

## 🤖 Claude *(00:29:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-342 of 422 total (26218 tokens, cap 25000). Call Read with offset=343 limit=342 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🎭 MCORCH Avatar/Clone AI — Programa "Gabriel AI" (persona-IA bilíngue, video-first, multicanal)
> 2	
> 3	**Blueprint DeepSearch · SEED / Fonte da Verdade para `/bok-scribe`**
> 4	`docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md` · slug `avatar-clone-ai` · v0.1.0 (2026-06-29)
> 5	
> 6	> **Natureza deste documento.** Artefato-semente (precedentes: `docs/bok/security/00-deepsearch-blueprint.md` e `docs/bok/vision-mcp/00-deepsearch-blueprint.md`). NÃO é código nem especificação final — é a **Fonte da Verdade fundamentada em deepsearch** que destrava o **Closed-Loop Protocol** (CLAUDE.md §1): com este blueprint consolidado e revisado, o Sovereign roda `/bok-scribe avatar-clone-ai` para gerar MRD → BRD → PRD → FRD → SDD **+ Pattern Conformance Declaration**. Nenhuma linha de código de `avatar-clone-ai` deve ser escrita antes dessa suíte existir.
> 7	>
> 8	> **ORO triplet deste blueprint** — Operator: MCORCH Master Execution Agent + L1 marketing-growth · Reviewer: Sovereign (Gabriel) · Owner: Sovereign até v6.x (blast radius = persona pública sintética + artefatos biométricos per-tenant; migra a marketing-growth quando uma North-Star de marca for definida e atingida — ver §8 OTD-AC-013).
> 9	>
> 10	> **Materialidade (Lei 1).** Toda afirmação externa carrega sua URL-fonte. Afirmações **refutadas** pela verificação adversarial NÃO aparecem como fato — aparecem na versão **corrigida** e marcadas `❌ REFUTADO (corrigido)`. Não-verificáveis: `⚠️ não-verificado`. Referências de repositório foram materialmente confirmadas contra o codebase (citadas com path + linhas).
> 11	>
> 12	> **Decisões Sovereign já tomadas (a pesquisa SERVE, não reabre):** (1) Avatar = **MÓDULO próprio multi-provider per-user/BYOK** no Canvas Studio (nós tipados novos), não asset único nem lock-in SaaS; referências de emulação = Magnific (foco primário), Freepik, "Martini Art", "Martini Film". (2) Canais = **todos**, cadência automatizada em cada um. (3) Pilares = autoridade (build-in-public AGI→ASI) + educação prática + tie-in produto/afiliado. (4) Idioma = **bilíngue PT-BR + EN**. (5) "Cérebro clonado" = RAG sobre a memory mesh existente. Gabriel AI = **instância-zero** de uma capacidade generalizável (qualquer user clona A SI MESMO ou cria personagem fictício).
> 13	
> 14	---
> 15	
> 16	## 1. Tese & posicionamento da marca "Gabriel AI"
> 17	
> 18	**Tese central.** "Gabriel AI" é a **instância-zero** de uma capacidade generalizável: uma persona-IA fiel (rosto + voz clonada + "cérebro clonado") que publica conteúdo **video-first** em **todos os canais** numa cadência automatizada de 30 dias, alimentada pelo motor **Viral Autopilot** já em produção. O Gabriel AI não vende um produto — **evangeliza o MCORCH** e a jornada AGI→ASI (build-in-public), com produto/afiliado como subproduto de longo prazo.
> 19	
> 20	**O fosso (moat) é a diferenciação autoral, não o volume.** O YouTube de 2025 não bane IA — ele **rebaixa output indiferenciado**: "se um humano não distingue seu canal de 50 outros do nicho, você é rebaixado" (https://www.codewords.ai/blog/complete-guide-youtube-automation). Logo a persona PRECISA carregar rosto/voz/POV consistentes — a decisão Sovereign do módulo Avatar próprio serve diretamente a isso. **⚠️ Risco existencial correlato (ver §5.5 e Front F2):** há evidência afirmativa de que plataformas (esp. TikTok) tratam avatares 100%-sintéticos com escrutínio MAIOR — detecção no upload (artefatos GAN, lip-sync) + padrões "templated/synthetic" enterrados mesmo quando compliant. Isto NÃO é só um FM — é hipótese de viabilidade a validar com case studies reais antes de escalar (Front F2).
> 21	
> 22	**Três pilares (ratio recomendado).** Mapeando a diretiva (autoridade + educação + produto) à norma de mercado 40% educacional / 25% inspiracional / 20% promocional / 15% brand-story (https://bulk.ly/creating-content-pillars-for-social-media/):
> 23	- **Educação ~40%** — AI/automação prática, how-to, tutoriais.
> 24	- **Autoridade + build-in-public ~40%** — jornada AGI→ASI do MCORCH, bastidores, prova social.
> 25	- **Produto/afiliado ≤20%** — tie-ins ML/afiliado. Para conta NOVA começar em **70/20/10** (só ~10% promo duro) e relaxar para 20% só após o ramp de 3 semanas (https://www.automateed.com/how-to-plan-30-days-of-content).
> 26	
> 27	**"Cérebro clonado" = camada RAG sobre a memory mesh existente** (`mcorch_nodes` via GraphRAG), não fine-tune. É o best-practice 2025 verificado: System Prompt carrega "Brand Voice DNA" quantificado (ex.: autoridade 8/10, entusiasmo 7/10) + RAG ancora as saídas em material aprovado, cortando alucinação (https://searchengineland.com/guide/how-to-train-in-house-llms-on-brand-voice). Voz inconsistente pode derrubar conversão até 33% (mesma fonte).
> 28	
> 29	**Bilíngue = duas trilhas NATIVAS, não tradução.** PT-BR e EN rodam como variantes nativas separadas por canal — hooks e "voz autêntica" diferem; packaging deve ser platform-native não-duplicado. **⚠️ Consequência de custo/volume não-trivial (Gap quantificado em §3.1 e §8 OTD-AC-012):** duas trilhas nativas ≈ **2× volume de render, 2× custo, 2× Identity Gate, 2× geração de voz**. Decisão de design obrigatória ANTES do FRD: cada pilar é renderizado DUAS vezes (uma por idioma) ou os dias se dividem por idioma sem duplicar o pilar? Isto determina se o custo mensal dobra.
> 30	
> 31	**Dois modos de persona (decisão de arquitetura com peso legal — ver §5.4 e §7).** As regras de plataforma tratam diferente: **self-clone** do dono da conta = permitido com rótulo em todas as plataformas; **personagem fictício** pode pegar a isenção mais leve do EU AI Act Art. 50 (obras criativas) mas **nunca pode retratar terceiros privados reais** — TikTok bane mídia sintética de privados reais mesmo rotulada (https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content). Gabriel AI = self-clone do Usuário Zero. **Para a capacidade GENERALIZADA ("clonar qualquer user"), provar que o user clona A SI MESMO (e não um terceiro) é gate de lançamento, não OTD a diferir** (§5.4).
> 32	
> 33	---
> 34	
> 35	## 2. Estratégia de conteúdo viral POR CANAL (com URL-fonte de cada número)
> 36	
> 37	> **Aviso de rigor (Lei 1):** a maioria dos números é de blogs de agências/ferramentas citando estudos terceiros. Tratar como **benchmarks direcionais derivados de aggregators**, não garantias oficiais — e validar contra o `creative_metrics` real do Gabriel. Os poucos claims first-party são marcados.
> 38	
> 39	### 2.1 YouTube (Shorts + longo) — funil Shorts→longo
> 40	
> 41	> **Veredicto adversarial (uncertain → corrigido):** a TESE ARQUITETURAL central — **Shorts e longo ranqueados por sistemas/modelos SEPARADOS, otimizar funções-objetivo diferentes, não gastar budget de thumbnail em Shorts** — é **CONFIRMADA first-party** (porta-vozes oficiais Todd Beaupré/Todd Sherman/Creator Liaison: "long-form and Shorts now compete in separate discovery lanes"). **MAS** os números abaixo NÃO são "YouTube-official" — são derivados de aggregators e aqui rotulados como tal.
> 42	
> 43	| Parâmetro | Valor | Fonte / status |
> 44	|---|---|---|
> 45	| Modelos de ranking | Shorts e longo ranqueados por **sistemas separados** (first-party confirmado) | https://www.shortimize.com/blog/how-does-youtube-shorts-algorithm-work |
> 46	| CTR em Shorts | "CTR não rastreado em Shorts" é **inferência de aggregator** (lógica do autoplay), NÃO documentado first-party — há aggregator que lista CTR entre fatores | idem (rotular como inferência) |
> 47	| Sinal-rei 2025 | **Satisfação** + comportamento pós-watch acima de watch-time bruto | https://blog.hootsuite.com/youtube-algorithm/ |
> 48	| Duração Shorts | **15-35s** (completion alta); teto subiu p/ 3 min mas dificulta completion | https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention |
> 49	| Métricas Shorts (corrigido) | **view rate** (visto-vs-swipado) ~75% + **completion** 80-90% p/ top performers — são DUAS métricas distintas, não conflar em ">75% completion" | https://www.shortimize.com/blog/youtube-shorts-retention-rate |
> 50	| Primeiros 3s | 50-60% do drop-off; hook nos 2s retém +19%; captions burned-in +15-25% | https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026 |
> 51	| Duração longo | **8-15 min** (8 min destrava mid-roll); 15-30 min monetiza se retenção segura | https://www.creator-hero.com/blog/how-long-should-a-youtube-video-be |
> 52	| Retenção longo | 50-60% sólido; **70%+** prioriza suggested | https://www.solveigmm.com/blog/en/how-the-youtube-algorithm-works-in-2025/ |
> 53	| Thumbnail (longo) | CTR **4-6% médio** (3-5% canais grandes / 6-10% pequenos); rosto +20-30%; 0-3 palavras; A/B de 3 títulos/3 thumbs | https://clickyapps.com/creator/thumbnails/guides/youtube-thumbnail-best-practices |
> 54	| Frequência | **12+ uploads/mês** = ~8x views, ~3x subs vs <1/mês (estudo 5,08M canais — anchor sólido) | https://vidiq.com/blog/post/How-Often-Post-on-Youtube/ |
> 55	| Funil | rodar ambos = +41% crescimento; 75% dos views de Shorts são de não-inscritos | https://subscribr.ai/p/convert-shorts-viewers-to-subscribers |
> 56	| Horário GLOBAL/EN | longo: Dom 10h (manhãs 8-11h); Shorts: Sex 16h (noites 18-23h) | https://buffer.com/resources/best-time-to-post-on-youtube/ |
> 57	| Horário BRASIL | dias úteis 14h-16h; fim de semana 9h-11h (confiança baixa) | https://www.adobe.com/br/express/learn/blog/best-times-to-post-youtube-shorts |
> 58	
> 59	**Arquitetura:** cada longo (pilar AGI→ASI ou tutorial) → atomizado em 3-5 Shorts cujo end-card aponta ao MESMO tópico do longo. Otimizar Shorts (hold 3s + completion) e longo (thumbnail CTR + AVD) em funções-objetivo DIFERENTES. **Tensão a resolver (§3.3):** o anchor "12+/mês" exige volume ALTO desde o início, o que conflita parcialmente com o RAMP anti-shadowban (volume baixo nas semanas 1-3).
> 60	
> 61	### 2.2 TikTok
> 62	| Parâmetro | Valor | Fonte |
> 63	|---|---|---|
> 64	| Sinais (oficial) | watch-time + completion = mais fortes; shares > comments > likes | https://blog.hootsuite.com/tiktok-algorithm/ |
> 65	| Follower count | NÃO é fator — conta nova viraliza por interesse | https://blog.hootsuite.com/tiktok-algorithm/ |
> 66	| Completion viral | ~70% em 2025-2026 (era 50%); otimizar watch-time ABSOLUTO | https://www.socialync.io/blog/tiktok-viral-retention-rate-2026 |
> 67	| Duração | sweet-spot **21-34s**; viralidade 11-18s; variar durações +35% eng | https://www.opus.pro/research/tiktok-video-guide |
> 68	| Primeiros 3s | reter 70-85% = 2,2x views; <60% = push mínimo | https://insights.ttsvibes.com/tiktok-first-3-seconds-hook-retention-rate/ |
> 69	| Hashtags | **3-5** (CapCut/ByteDance); legenda keyword = peso igual/maior (TikTok SEO) | https://sproutsocial.com/insights/tiktok-hashtags/ |
> 70	| Frequência | **3-5/semana** (maior eng médio em 1,1M vídeos — Buffer, fonte primária) | https://buffer.com/resources/how-often-should-you-post-on-tiktok/ |
> 71	| Horário GLOBAL | Dom 9h; tardes 16-18h | https://blog.hootsuite.com/best-time-to-post-on-tiktok/ |
> 72	| Horário BRASIL | noite domina: 16h-21h (ter/qua/qui); 20h-meia-noite; evitar 2h-10h (conf. baixa) | https://psicopedagogia.com.br/blog/melhores-horarios-para-postar-tiktok-2025 |
> 73	| Vantagem estrutural | **feed STEM** expandido por padrão a todos + busca como descoberta | https://blog.hootsuite.com/tiktok-algorithm/ |
> 74	| Áudio | trending +até 47% reach, dura 1-3 sem (detecção semanal!); original ancora marca | https://www.outfame.com/blog/trending-sounds-drive-tiktok-virality |
> 75	| ⚠️ Disclosure IA | label "AI-generated" obrigatório p/ mídia realista; auto-label via C2PA; sintético de PRIVADO real banido mesmo rotulado | https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content |
> 76	
> 77	### 2.3 Instagram Reels
> 78	| Parâmetro | Valor | Fonte |
> 79	|---|---|---|
> 80	| Duração reach | **7-15s** (completion); 15-60s tutoriais; >90s cai reach | https://www.inro.social/blog/instagram-reels-can-now-be-20-minutes-long-new-time-limit-explained-2025 |
> 81	| Primeiros 3s | até 50% saem; hold >60% supera <40% em 5-10x; alvo 65-70%+ | https://www.opus.pro/blog/instagram-reels-hook-formulas |
> 82	| Sinais 2026 (Mosseri) | watch-time #1; **sends-per-reach (DM)** = 3-5x mais que likes | https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers |
> 83	| Reels vs carrossel | Reels 2.25x reach; carrossel +12% interações (autoridade) | https://www.creatorsjet.com/blog/instagram-reels-vs-carousels-vs-images |
> 84	| Áudio | voz/áudio ORIGINAL preferido em educacional; trending só 24-48h | https://www.truefuturemedia.com/articles/instagram-reels-reach-2026-business-growth-guide |
> 85	| Frequência | **3-5/sem** (Reels 4-7/sem) + Stories diárias | https://www.kontentino.com/blog/how-often-to-post-on-instagram/ |
> 86	| Horário GLOBAL | Qua>Qui>Ter; noite 18-23h ou manhã 8-12h | https://buffer.com/resources/when-is-the-best-time-to-post-on-instagram/ |
> 87	| Horário BRASIL | pico 20h-00h (27%); 18-20h (20%); eficiência 12-13h | https://www.amper.ag/post/melhor-horario-postar-instagram-brasil |
> 88	| Funil | Reels=topo (+36% reach), Stories=meio (+23% retenção, +DM); mix 40/30/30 | https://creatorflow.so/blog/instagram-algorithm-2026/ |
> 89	| Cover/safe-zone | grid corta 9:16→3:4 (240px topo+base); texto na zona central ~70-80% | https://zeely.ai/blog/master-instagram-safe-zones/ |
> 90	
> 91	### 2.4 LinkedIn (canal de PROFUNDIDADE)
> 92	| Parâmetro | Valor | Fonte |
> 93	|---|---|---|
> 94	| Sinal | primeiros 30-60 min decidem; dwell + comments > likes; "Depth Score" 24-48h | https://growleads.io/blog/linkedin-algorithm-2026-text-vs-video-reach/ |
> 95	| Hierarquia de formato | carrossel PDF ~6.60% (líder) > vídeo nativo ~5.60% > texto ~2%; link externo -30-60%; 0-3 hashtags | https://www.dataslayer.ai/blog/linkedin-algorithm-february-2026-whats-working-now |
> 96	| Carrossel | 6-10 slides, retrato 1080x1350, 24pt min, 1 ideia/slide | https://postunreel.com/blog/linkedin-carousel-engagement-rate-statistics-2026 |
> 97	| Vídeo | nativo ~3.5x reach vs link YT; vertical 4:5/9:16; <90s | https://www.visla.us/blog/guides/linkedin-video-in-2026-whats-working-and-how-to-make-it/ |
> 98	| Cadência | **3-4 nativos/sem**, Ter-Qui 9-11h | https://www.visla.us/blog/guides/linkedin-video-in-2026-whats-working-and-how-to-make-it/ |
> 99	| Hook | 1ª linha decide (2-3 linhas antes do "ver mais"); curiosity/dado/contrário | https://tonemark.ai/blog/linkedin-viral-posts-psychology |
> 100	
> 101	**Regra crítica:** link de afiliado/blog vai no **primeiro comentário**, nunca no corpo.
> 102	
> 103	### 2.5 X/Twitter (único canal onde TEXTO bate vídeo)
> 104	| Parâmetro | Valor | Fonte |
> 105	|---|---|---|
> 106	| Pesos | reply ~27x like; reply-com-resposta-do-autor ~150x; RT ~20x; QT ~25x | https://opentweet.io/blog/how-twitter-x-algorithm-works-2026 |
> 107	| Texto vs vídeo | texto +~30% vs vídeo; link externo -30-50% (workaround: 1ª reply); X Premium remove supressão | https://posteverywhere.ai/blog/how-the-x-twitter-algorithm-works |
> 108	| Threads | **3-6 tweets**; 1º tweet standalone <10 palavras; +40-60% impressões | https://www.indiehackers.com/post/the-2026-x-growth-system-how-top-creators-engineer-virality-with-threads-replies-quote-posts-66200ecdc5 |
> 109	| Cadência | 3-5 posts/dia (0-1K); replies > posts originais p/ crescer; 7-9h/12h/15-16h/19-21h | https://grahammann.net/blog/how-to-grow-on-x-twitter-2026 |
> 110	| Vídeo nativo | upload 9:16 bate LINK de vídeo; alimenta Video Tab | https://blog.postful.ai/how-to-upload-videos-on-twitter/ |
> 111	
> 112	**Gap operacional CRÍTICO (ver §6.2 + §8 OTD-AC-009):** o motor de **reply** (persona respondendo a comentadores na 1ª hora p/ gatilhar o multiplicador ~150x author-reply) é uma **capacidade conversacional real-time net-new** — um novo agent loop (monitorar mentions → gerar reply → postar em minutos), não um gap de render. O Viral Autopilot atual é **broadcast-only** e não tem primitivo para isto. **Decisão obrigatória ANTES do FRD:** ou o reply engine entra no escopo core, ou a promessa "paridade de automação em TODOS os canais" é explicitamente SUAVIZADA (X cresce capado sem ele).
> 113	
> 114	### 2.6 Repurpose 1→N (COPE / atomização)
> 115	Extrair 25-40 "átomos" por vídeo-fonte (hooks, soundbites, FAQs, quotes), recompor NATIVAMENTE por plataforma — não cramming de char-limit (https://aimaker.substack.com/p/ai-content-repurposing-n8n-workflow-7-platforms). Mapeia 1:1 ao `pillar_atoms` + `reshape-pillar`/`channel_variants` já em produção no MCORCH (https://www.postquick.ai/blog/content-repurpose-workflow-for-social-media-create-once-post-everywhere).
> 116	
> 117	---
> 118	
> 119	## 3. CADÊNCIA DE 30 DIAS concreta
> 120	
> 121	**Princípios de design:** (a) 30 dias = 1ª perna de um compromisso de 90 dias (consistência ~3x mais crescimento — confiança média, https://www.mlabs.com.br/blog/frequencia-de-postagens-nas-redes-sociais); (b) **RAMP anti-shadowban server-side** — princípio CONFIRMADO (picos súbitos parecem bot → ramp gradual; recovery = pausar 48-72h, https://www.kontentino.com/blog/how-often-to-post-on-instagram/), **MAS os números exatos abaixo são ILUSTRATIVOS/heurística de vendor, NÃO regra de plataforma** (fontes divergem: alguns dizem posts #2-5 a cada 2-3 DIAS, não no mesmo dia — GeeLark); (c) funil semanal: S1 Awareness, S2 Education, S3 Social-Proof, S4 Conversion; (d) trilhas PT-BR e EN em janelas SEPARADAS.
> 122	
> 123	> ⚠️ A citação `reelforgeai.io` do draft foi **removida** (não verificável como fonte do ramp). Fontes do RAMP = Buffer (https://buffer.com/resources/how-often-should-you-post-on-tiktok/) + GeeLark/Kontentino.
> 124	
> 125	**Tensão RAMP × 12+/mês (§2.1) — resolução de design proposta (OTD-AC-014):** a contradição é aparente. O anchor vidIQ "12+ uploads/mês" é medido sobre canais ESTABELECIDOS; conta nova prioriza **sobrevivência anti-flag** nas semanas 1-3 e só atinge steady-state (que já entrega 12+/mês de Shorts) na semana 4. Recomendação: ramp por CANAL independente; o volume agregado cross-canal cresce mesmo com cada canal individual em ramp suave.
> 126	
> 127	**Grade-mestre por canal (steady-state, pós-ramp):**
> 128	
> 129	| Canal | Freq/sem | Formato âncora | Dur. | Trilha idioma | Janela PT-BR | Janela EN |
> 130	|---|---|---|---|---|---|---|
> 131	| YouTube Shorts | 5 | 9:16 hook+payoff | 15-35s | alternado | — | — |
> 132	| YouTube longo | 1-2 | tutorial/build-in-public | 8-15 min | alternado | seg 9-11h | Dom 10h |
> 133	| TikTok | 3-5 | 9:16 educacional | 15-35s | nativo | 16-21h ter/qua/qui | Dom 9h / 16-18h |
> 134	| IG Reels | 4-5 + Stories diárias | 9:16 + cover safe-zone | 7-30s | nativo | 18-00h | Qua/Qui 18-23h |
> 135	| LinkedIn | 3-4 | carrossel/vídeo nativo/texto | <90s vídeo | nativo | Ter-Qui 9-11h BRT | Ter-Qui 9-11h |
> 136	| X | 3-5/dia | thread 3-6 / vídeo nativo | — | nativo | 7-9h/12h/19-21h | idem fuso EN |
> 137	
> 138	### 3.1 Cadência dia-a-dia concreta (30 dias) — 1 pilar → N variantes via Channel Reshaper
> 139	
> 140	> **Modelo de duplicação bilíngue (decisão de design embutida, a ratificar — OTD-AC-012):** cada **pilar-fonte** é renderizado UMA vez no idioma-âncora do dia; o reshaper emite a variante nativa por canal. Dias alternam idioma-âncora (PT-BR/EN) para distribuir a marca nas duas trilhas SEM dobrar o número de pilares-fonte. A "trilha B" (segundo idioma) reusa o MESMO mestre 9:16 quando o áudio é re-locado pela voz clonada cross-lingual (custo = re-síntese de voz + re-render lip-sync, NÃO re-roteiro). **Se o Sovereign exigir as DUAS línguas no MESMO dia, o volume/custo de render dobra — ver §8 economics.**
> 141	
> 142	Funil: **S1 Awareness · S2 Education · S3 Social-Proof · S4 Conversion**. Idioma-âncora alterna 🇧🇷/🇬🇧.
> 143	
> 144	| Dia | Sem/Funil | Pilar-fonte (1×) | Idioma | YT Short | YT longo | TikTok | IG Reel | LinkedIn | X | Produto |
> 145	|---|---|---|---|---|---|---|---|---|---|---|
> 146	| 1 | S1 Aware | "O que é o MCORCH (build-in-public)" | 🇧🇷 | atom A | — | atom A | atom A | texto-hook | thread 4 | — |
> 147	| 2 | S1 | (reuso D1) | 🇬🇧 | atom B | — | atom B | atom B | — | thread 3 | — |
> 148	| 3 | S1 | "Por que 90% dos agentes de IA morrem em 6m" (autoridade) | 🇧🇷 | atom C | longo 10min | atom C | atom C | vídeo <90s | thread 5 | — |
> 149	| 4 | S1 | (reuso D3) | 🇬🇧 | atom D | — | atom D | atom D | carrossel 6 | thread 3 | — |
> 150	| 5 | S1 | "Demo ao vivo: mesh GraphRAG" (build-in-public) | 🇧🇷 | atom E | — | atom E | atom E | vídeo nativo | thread 4 | tie-in soft |
> 151	| 6 | S1 | (reuso semana) | 🇬🇧 | atom F | — | atom F | Story-only | — | thread 3 | — |
> 152	| 7 | S1 | (recap semanal) | 🇧🇷 | atom G | — | — | atom G | — | thread 4 | — |
> 153	| 8 | S2 Educ | "Automatizar X com 1 agente" (tutorial) | 🇧🇷 | atom A | — | atom A | atom A | carrossel 6 | thread 4 | — |
> 154	| 9 | S2 | (reuso D8) | 🇬🇧 | atom B | — | atom B | atom B | — | thread 3 | tie-in ML soft |
> 155	| 10 | S2 | "Anatomia de um pipeline self-healing" | 🇧🇷 | atom C | longo 12min | atom C | atom C | vídeo <90s | thread 5 | — |
> 156	| 11 | S2 | (reuso D10) | 🇬🇧 | atom D | — | atom D | atom D | texto contrário | thread 3 | — |
> 157	| 12 | S2 | "RAG vs fine-tune: quando usar cada um" | 🇧🇷 | atom E | — | atom E | atom E | — | vídeo nativo | afiliado ML |
> 158	| 13 | S2 | (reuso semana) | 🇬🇧 | atom F | — | atom F | Story-only | — | thread 3 | — |
> 159	| 14 | S2 | (recap) | 🇧🇷 | atom G | — | — | atom G | carrossel 8 | thread 4 | — |
> 160	| 15 | S3 Proof | "Mostrando a malha de 8.9k nós ao vivo" | 🇧🇷 | atom A | — | atom A | atom A | vídeo nativo | thread 4 | — |
> 161	| 16 | S3 | (reuso D15) | 🇬🇧 | atom B | — | atom B | atom B | — | thread 3 | — |
> 162	| 17 | S3 | "Resultado real: 1º R$ do Autopilot" (case) | 🇧🇷 | atom C | longo 10min | atom C | atom C | carrossel 6 | thread 5 | afiliado ML |
> 163	| 18 | S3 | (reuso D17) | 🇬🇧 | atom D | — | atom D | atom D | vídeo <90s | thread 3 | — |
> 164	| 19 | S3 | "Bastidores: como o Identity Gate funciona" | 🇧🇷 | atom E | — | atom E | atom E | — | vídeo nativo | — |
> 165	| 20 | S3 | (reuso semana) | 🇬🇧 | atom F | — | atom F | Story-only | — | thread 3 | — |
> 166	| 21 | S3 | (recap) | 🇧🇷 | atom G | — | — | atom G | — | thread 4 | tie-in soft |
> 167	| 22 | S4 Conv | "Como você clona A SI MESMO no MCORCH" (produto) | 🇧🇷 | atom A | — | atom A | atom A | carrossel 8 | thread 4 | CTA produto |
> 168	| 23 | S4 | (reuso D22) | 🇬🇧 | atom B | — | atom B | atom B | — | thread 3 | CTA produto |
> 169	| 24 | S4 | "Tutorial completo: avatar→cadência 30d" | 🇧🇷 | atom C | longo 15min | atom C | atom C | vídeo <90s | thread 5 | CTA produto |
> 170	| 25 | S4 | (reuso D24) | 🇬🇧 | atom D | — | atom D | atom D | texto-hook | thread 3 | afiliado ML |
> 171	| 26 | S4 | "ROI real: o que 30 dias geraram" | 🇧🇷 | atom E | — | atom E | atom E | vídeo nativo | vídeo nativo | CTA produto |
> 172	| 27 | S4 | (reuso semana) | 🇬🇧 | atom F | — | atom F | Story-only | — | thread 3 | — |
> 173	| 28 | S4 | "Roadmap: para onde vai a persona" | 🇧🇷 | atom G | — | atom G | atom G | carrossel 6 | thread 4 | — |
> 174	| 29 | S4 | (reuso) | 🇬🇧 | atom A2 | — | atom A2 | atom A2 | — | thread 3 | afiliado ML |
> 175	| 30 | S4 | "Recap do mês + convite" (CTA final) | 🇧🇷 | atom B2 | longo 8min | atom B2 | atom B2 | vídeo nativo | thread 5 | CTA produto |
> 176	
> 177	> **Regra de repurpose (FM-AC-007):** o reshaper emite variantes **NATIVAS** (não clip byte-idêntico + caption copiada — exatamente o sinal de "duplicate/automation" que plataformas suprimem). Mesmo MP4 9:16 sobe nativo em YT/TikTok/IG/LinkedIn/X, mas **corte/hook/legenda mudam por canal**. O end-card do Short aponta ao MESMO tópico do longo. O texto EXATO de cada post (copy + hook) é trabalho do BoK Scribe — aqui está a grade completa Dia 1→30 + funil + idioma-âncora + tie-ins.
> 178	
> 179	---
> 180	
> 181	## 4. MÓDULO Avatar/Clone AI (per-user, Canvas Studio)
> 182	
> 183	**Decisão de arquitetura:** módulo PRÓPRIO multi-provider BYOK per-user (não wrapper de SaaS único), espelhando o API Tenancy Model do MCORCH. **⚠️ Caveat transversal (ver §8 Front F1):** "BYOK per-user" NÃO é uniformemente viável — a legalidade de pass-through de chave end-user difere por provider (HeyGen é partnership-gated; Magnific exige plano PAGO). É uma frente de verificação de ToS própria ANTES do FRD.
> 184	
> 185	### 4.1 Pipeline (nós tipados novos no Canvas)
> 186	```
> 187	[avatarIdentity] rosto-lock (Soul ID / LoRA por-usuário)
> 188	      │ output: input_face_identity
> 189	      ▼
> 190	[voiceClone] voz clonada PT-BR+EN (ElevenLabs IVC/v2-PVC / Cartesia)
> 191	      │ output: input_voice_profile
> 192	      ▼
> 193	[avatarScript] roteiro do "cérebro clonado" (RAG sobre mcorch_nodes + Brand Voice DNA)
> 194	      │ output: input_script
> 195	      ▼
> 196	[talkingHead] lip-sync + animação (motor por-vídeo-referência — ver OTD-AC-001)
> 197	      │ output: output_avatar_video
> 198	      ▼
> 199	[avatarEnhance] Magnific Relight + upscale (polish FINAL, nunca autor de identidade)
> 200	      │ output: output_video (9:16)
> 201	      ▼
> 202	→ Identity Gate (ArcFace cosine, limiar CALIBRADO) → C2PA embed → creative_assets → Viral Autopilot
> 203	```
> 204	
> 205	**Disciplina de ordem (FM-AC-003):** identidade (LoRA/conditioner) → Identity Gate → Magnific Precision/high-Resemblance como ÚLTIMO passo. NUNCA deixar um passo high-Creativity tocar o rosto por último (deriva identidade).
> 206	
> 207	**Tipos de nós propostos (CanvasNodeKind):** `avatarIdentity`, `voiceClone`, `avatarScript`, `talkingHead`, `avatarEnhance`. Cada um segue o recipe do registry existente (factory + handles + inspector + nodeTypes map — ver §6).
> 208	
> 209	### 4.2 Recomendação de stack por sub-capacidade (commercial vs self-host) — verificada e CORRIGIDA
> 210	
> 211	| Sub-capacidade | Default comercial (BYOK) | Self-host soberano | Trade-off / status verificado | Fonte |
> 212	|---|---|---|---|---|
> 213	| **Identity-lock de rosto** | **Higgsfield Soul ID** (treina ⚠️ **≥20 fotos** [não "10-20"], 3-5 min) | LoRA FLUX por-pessoa ⚠️ (FLUX.1-dev base é **non-commercial** — verificar checkpoint) | ⚠️ **API self-serve só p/ GERAÇÃO confirmada; TREINO de identity-lock via API NÃO-VERIFICADO em docs públicas** — ler docs logadas antes do SDD (é exatamente o OTD-AC-003 "clonar a si mesmo") | https://higgsfield.ai/blog/SOUL-ID-Superior-Level-of-AI-Character-Consistency |
> 214	| **Talking-head fiel** | ❌ **REFUTADO (corrigido): HeyGen Avatar V NÃO é $3/min nem self-serve.** Avatar V Digital Twin/Studio = **$0.0667/s = $4.00/min**; API direta **"not yet publicly available"** (webinar 2026-04); BYOK/OAuth **partnership-gated** (Redirect URI só após Intake form; ToS restringe white-label multi-tenant). $3/min é o **Avatar IV Photo Avatar** (motor por-foto). **Re-avaliar motor ou modelar tenancy master-account** | Hallo2 (4K, GPU) / LivePortrait+MuseTalk | ✅ núcleo verdadeiro preservado: **motor por-vídeo-referência > por-foto** p/ consistência. ⚠️ HeyGen NÃO ancora BYOK self-serve hoje | https://developers.heygen.com/docs/pricing · https://www.heygen.com/research/avatar-v-model |
> 215	| **Talking-head barato/live** | **Hedra Character-3** ($0.05/min live) / **OmniHuman** ($0.16/s via fal.ai) | — | barato e bom lip-sync MAS fidelidade por-imagem | https://medium.com/@CherryZhouTech/hedra-live-avatars-the-future-of-ai-video-at-0-05-minute-f423b144ad3b · https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5 |
> 216	| **Voz clonada bilíngue** | ❌ **REFUTADO (corrigido): NÃO usar "PVC + Eleven v3".** ElevenLabs doc: PVCs "not fully optimized for Eleven v3". **Default = PVC sobre Multilingual v2 OU IVC/Voice-Design sobre v3.** ⚠️ falhas documentadas: accent bleed se a voz não foi clonada no idioma-alvo; drift de idioma DENTRO de uma geração → **code-switching PT-BR↔EN na MESMA frase é falha conhecida**. v3 é alpha/research-preview | F5-TTS ❌ **NÃO é commercial-clean**: código MIT mas pesos base (SWivid/F5-TTS) e `firstpixel/F5-TTS-pt-br` são **CC-BY-NC-4.0** (Emilia dataset) | ✅ confirmado: BYOK header trivial (`xi-api-key`); preço **$0.05-0.10/1k chars** | https://help.elevenlabs.io/hc/en-us/articles/13313681788305 · https://huggingface.co/firstpixel/F5-TTS-pt-br |
> 217	| **Voz real-time** | **Cartesia Sonic** (40-90ms, variante "Brazilian") | — | menor controle emocional; bom p/ live | https://www.cartesia.ai/languages/ |
> 218	| **Enhance/relight final** | **Magnific** (Mystic style+structure, Relight, upscale; api unificada Freepik) ⚠️ **API-key só com plano PAGO; server-to-server only** | — | NÃO anima nem trava identidade — é polish | https://docs.magnific.com/authentication |
> 219	| **Vídeo legal-safe** | **Marey/Moonvalley** ($0.30/s, treino licenciado) | — | mitiga risco copyright de persona pública | https://fal.ai/models/moonvalley/marey/i2v |
> 220	
> 221	### 4.3 Os produtos-referência do Sovereign — desambiguação verificada
> 222	- **Magnific ≡ Freepik (a partir de 28/04/2026).** ✅ CONFIRMADO com **correção direcional:** NÃO é "Magnific é rebrand DE Freepik" como produto separado — é a **MESMA empresa** (Freepik, que comprou a Magnific em 2024) **adotando o nome Magnific**. `api.freepik.com` e `api.magnific.com` são **intercambiáveis**; chave Freepik existente vale em ambos; header canônico = `x-magnific-api-key` (legado `x-freepik-api-key` ainda em docs antigas). **⚠️ Precondição BYOK omitida no draft:** geração de API-key **não é self-serve** — exige **plano PAGO** (free tier não gera chave) e só server-to-server. BYOK viável **somente** se cada tenant trouxer a PRÓPRIA chave de plano PAGO; chave compartilhada do MCORCH revendendo créditos = violação de ToS (https://docs.magnific.com/authentication · https://tech.eu/2026/04/28/freepik-rebrands-as-magnific-unifying-its-ai-creative-stack-as-enterprise-and-no-collar-growth-accelerates/). É camada de ENHANCEMENT (Relight/upscale/Mystic), NÃO motor de talking-head nem identity-lock.
> 223	- **"Martini Art" = martini.art** (canvas infinito multi-modelo, 100+ modelos) e **"Martini Film" = martini.film** ("Film Set for AI Videos", YC-backed). ✅ CONFIRMADO: **AMBOS são produtos WEB sem API pública** (integração = só export de arquivo p/ Premiere/DaVinci/Final Cut) → servem de **inspiração de UX** dos nós tipados do Canvas, NÃO alvo de integração (https://martini.art/en/features · https://www.martini.film/). ⚠️ caveat: docs.martini.art retornou 403 bot-challenge — não dá p/ provar ausência de beta enterprise não-listado. ⚠️ **NÃO confundir** com o "Martini" low-code iPaaS da **Lonti/Toro Cloud** — entidade distinta, é o único "Martini" com API (https://www.lonti.com/martini · https://developer.lonti.com/docs/martini/).
> 224	
> 225	### 4.4 Modelo BYOK per-user + storage de artefatos biométricos
> 226	Espelha o pattern verificado em `user_api_keys` (Vault). **Duas superfícies distintas:**
> 227	
> 228	**(a) Chaves de API (recipe pronto):** novas colunas cifradas `heygen_api_key`, `magnific_api_key` (≡ chave Freepik), `elevenlabs_api_key`, `cartesia_api_key`, `higgsfield_api_key` (já existe — confirmar/reusar). Resolução per-user fail-closed → HTTP 402 `<service>_not_configured`. Migration segue o template de `20260622210000` (ALTER + encrypt trigger + masked view + INSTEAD OF + decrypted LEFT JOIN). **⚠️ Cada coluna exige verificação de ToS de pass-through (Front F1) — Magnific=plano pago; HeyGen=partnership.**
> 229	
> 230	**(b) Artefatos TREINADOS biométricos (gap do draft — NET-NEW, a real superfície de vazamento):** LoRA weights, voice profiles e ArcFace embeddings são **PII biométrica**. Tabelas novas `avatar_identities` + `voice_profiles` com:
> 231	- **RLS own-or-org** estrita (`auth.uid() = user_id`), NUNCA weights compartilhados cross-tenant (FM-AC-011).
> 232	- **Storage per-tenant isolado** (bucket privado, prefixo por `user_id`; signed URLs curtos).
> 233	- **Consent artifact por-render** (não só reuso do flag `voice_consent` existente — ver §5.4).
> 234	- **Erase/retention RPC** espelhando o pattern Vision MCP (`erase_vision_artifacts` + retention-sweep) → cascade tenant-guarded + Storage API remove, sob LGPD (dado biométrico = categoria sensível) + EU AI Act (ver Front F6).
> 235	
> 236	---
> 237	
> 238	## 5. Consistência & QA do avatar
> 239	
> 240	**Ladder de identidade de 3 tiers** (Gabriel = Tier 3 desde o dia 1; clones per-user sobem do Tier 1):
> 241	- **Tier 1** (1 imagem) = InstantID / IP-Adapter FaceID (~76-86% match).
> 242	- **Tier 2** (multi-imagem) = IP-Adapter FaceID-Portrait / PuLID-Flux2 (~88-93%).
> 243	- **Tier 3** (canônico) = LoRA por-pessoa FLUX (20-40 imgs, dim 32-64, ~1000 steps). ⚠️ **base FLUX.1-dev é non-commercial — verificar checkpoint comercial.**
> 244	Fontes: https://apatero.com/blog/instantid-vs-pulid-vs-faceid-ultimate-face-swap-comparison-2025 · https://www.freepik.com/ai/docs/custom-characters
> 245	
> 246	**Substrato único = embeddings InsightFace/ArcFace** — o MESMO embedding conduz geração E o drift-QA (loop fechado) (https://medium.com/design-bootcamp/ai-face-swap-battle-pulid-vs-instantid-vs-faceid-2f08db230509).
> 247	
> 248	### 5.1 Identity Gate (novo nó pós-geração) — ❌ números do draft REFUTADOS, princípio preservado
> 249	> **Veredicto adversarial (refuted):** o teto "~85% consistência", a banda cosine "0.7-0.8" e o aviso "anti-0.95" **NÃO constam** das fontes citadas (gensgpt/skywork) — atribuição falsa. Pior: "0.7-0.8" **conflata duas escalas** — o default de verificação ArcFace no DeepFace é cosine **DISTANCE 0.68** (~0.32 similarity), enquanto "0.7+ similarity" é barra de **CSIM generativo** (SOTA reporta CSIM ~0.62-0.71), grandeza DIFERENTE. O teto ~85% é não-corroborado.
> 250	
> 251	**O que SOBREVIVE (princípio correto, independentemente confirmado):** ArcFace-embed cada frame → cosine vs embedding canônico → **fail-and-regenerate** com seed fixo + conditioning mais forte abaixo do limiar. **NÃO hardcodar 0.95 nem 0.7-0.8** — **calibrar empiricamente** em frames reais do Gabriel via **FAR/FRR/EER**, reconhecendo que o valor depende do embedding model e do contexto (verificação vs CSIM generativo) (https://github.com/serengil/deepface/blob/master/deepface/modules/verification.py).
> 252	
> 253	**Bloco de personagem verbatim** (copiar byte-a-byte por cena, estender só variáveis de cena). QA automatizado obrigatório.
> 254	
> 255	### 5.2 Reuso do Vision QA existente
> 256	`scripts/qa/vision-qa.ts` (modo compare frame-A↔frame-B) — estender para face-consistency, voice-identity-drift, lip-sync-offset. BYOK-free (cost 0) para o Usuário Zero. (Diretiva Sovereign 2026-06-26: todo criativo gerado passa pelo Vision QA antes de declarar pronto.)
> 257	
> 258	### 5.3 Gate de licença (FM-AC-001) — verificado
> 259	**Pesos non-comerciais a NÃO shippar (CONFIRMADOS):** **InfiniteYou** (CC-BY-NC), **Fish-Speech/OpenAudio S1** (research-license / CC-BY-NC-SA), **XTTS-v2** (CPML não-comercial órfã — Coqui fechou jan/2024, sem ninguém p/ vender licença comercial). **❌ CORREÇÃO:** **F5-TTS NÃO é caminho comercial limpo** (código MIT mas pesos base + `firstpixel/F5-TTS-pt-br` = CC-BY-NC-4.0). **⚠️ FLUX.1-dev** (base de "LoRA FLUX"/IP-Adapter-for-FLUX) é **non-commercial** — verificar checkpoint base separadamente. Preferir SaaS licenciado via BYOK ou pesos genuinamente Apache/MIT (PuLID/IP-Adapter; F5-TTS só se treinado do zero em dataset comercial).
> 260	
> 261	### 5.4 Consentimento & personalidade-legal (gap de lançamento, NÃO OTD a diferir)
> 262	A distinção **self-clone vs personagem fictício** (§1) tem consequências profundas para a capacidade GENERALIZADA:
> 263	- **Identity-verification gate:** como o sistema PROVA que o user clona A SI MESMO e não um terceiro privado real? (TikTok bane sintético de privados reais mesmo rotulado.) Requer prova de identidade no onboarding do avatar (selfie-liveness vs fotos de treino, ou attestation legal) ANTES de gerar weights.
> 264	- **Consent artifact por-render** armazenado (não só o flag `voice_consent` reusado): cada render carrega o consentimento ativo do titular biométrico + `persona_type` (self-clone vs fictício) que dirige templates de compliance diferentes.
> 265	- **Para o produto generalizado isto é gate de lançamento** — modelar como FR de compliance first-class no FRD, não OTD diferido.
> 266	
> 267	### 5.5 ⚠️ Hipótese de viabilidade (Front F2) — avatares sintéticos crescem em 2025-2026?
> 268	Evidência afirmativa de escrutínio MAIOR a sintético (detecção de upload + supressão de padrões templated mesmo compliant). **Nenhum dado de ramp é avatar-específico.** Antes de escalar: pesquisar case studies REAIS de canais 100%-avatar com dados de retenção/crescimento. É a frente que pode invalidar (ou validar) o programa inteiro.
> 269	
> 270	---
> 271	
> 272	## 6. MAPA DE INTEGRAÇÃO no ecossistema existente
> 273	
> 274	### 6.1 O que REUSA (já em produção)
> 275	| Primitivo | Reuso para Avatar/Gabriel AI |
> 276	|---|---|
> 277	| **Canvas node registry** (`src/lib/canvas-node-registry.ts`, `canvas-handles.ts`, `RightPanel/inspectors`) | Adicionar 5 kinds via recipe existente (factory + handles + inspector + nodeTypes map + resolveExecutePayload) |
> 278	| **generate-image** (multi-provider, BYOK, dual-write creative_assets) | Template do roteamento de provider p/ voz/face; storage + register_creative_asset |
> 279	| **canvas-execute** (cost-gate, daily-cap, async webhook, reference_image_urls + seed) | Execução dos nós; CREDIT_COSTS ganha entradas avatar |
> 280	| **HyperFrames** (`scripts/hyperframes/render-core.ts` Playwright+FFmpeg → MP4 9:16 sha256-idêntico; `scripts/video-bridge.ts` worker) | Render core reutilizável; novos templates `avatar-presenter-9x16`; molde do worker p/ `avatar-render-bridge` |
> 281	| **Channel Reshaper** (`reshape-pillar`, `channel_variants`, `pillar_atoms`) | Repurpose 1→N nativo; field_map grammar p/ avatar-script; idempotência UNIQUE |
> 282	| **creative_assets** + `register_creative_asset` RPC | Spine de assets; source_module='avatar-studio', parent_asset_id p/ versionamento |
> 283	| **video_renders** + `finalize_video_render` (refund atômico) + `voice_consent` flag (FR-VS-032) | Ledger de render avatar; copiar finalize p/ `finalize_avatar_render`; voice_consent existe (mas insuficiente p/ consent per-render — §5.4) |
> 284	| **Viral Autopilot** (`autopilot_plans`, `begin/finalize_autopilot_cycle`, prepaid) | Junção final — cadência + billing atômico |
> 285	| **user_api_keys** Vault (encrypt trigger + masked/decrypted views) | BYOK das chaves avatar (recipe `20260622210000`) |
> 286	| **Vision MCP retention/erase** (`erase_vision_artifacts` + retention-sweep) | Molde p/ erasure de artefatos biométricos (LGPD — §4.4b) |
> 287	| **_shared/llm-fallback.ts** + **sentinel.ts** | Geração de roteiro provider-agnóstica; validar consentimento/jailbreak |
> 288	
> 289	### 6.2 O que é NET-NEW por canal (gaps CORRIGIDOS contra o codebase real)
> 290	
> 291	> ❌ **Correção material (refuted):** o draft afirmava "o reshaper nunca assina asset_key nem chama publish-social". **FALSO.** Verificado: `reshape-pillar/index.ts` em scope='video' (kickado por `video-bridge.ts:158-171` após `finalize_video_render`) **RESOLVE o master de `video_renders`, seta `channel_variants.asset_key` (linha 462), marca instagram/tiktok/youtube/pinterest operacionais (linhas 39-41)**; e `auto-publish/index.ts:117-139` resolve `channel_variants.asset_key` (asset_kind='video') em `video_url` assinado e chama `publish-social`. **Esse caminho EXISTE e está wired.** Logo o fix "ensinar o reshaper a assinar+publicar vídeo" é **parcialmente redundante**. Os gaps REAIS:
> 292	
> 293	| Gap REAL | Onde | Severidade |
> 294	|---|---|---|
> 295	| **CHECK de `autopilot_plans.platforms`** só permite `['wordpress','linkedin','twitter']` → canais de vídeo nem entram no plano | `supabase/migrations/20260620120000_viral_autopilot_plans.sql:26-27` (migration `20260624130000` add video cols mas NÃO relaxa o CHECK) | CRÍTICO |
> 296	| **VIDEO_FLOW_PLATFORMS** gateia enqueue de render a `wordpress` apenas | `autopilot-run/index.ts:114` `const VIDEO_FLOW_PLATFORMS = new Set(["wordpress"])` | CRÍTICO |
> 297	| **Sem step `avatar_generation`** independente do `article_generation` | `orchestrate-step` — vídeo hoje só enfileirado por `article_generation` gated em wordpress | CRÍTICO |
> 298	| **`AVATAR_FLOW_PLATFORMS`** + contagem/billing avatar separados | `autopilot-run` | MÉDIO |
> 299	| **Branches de vídeo p/ LinkedIn/X** em publish-social | publish-social tem vídeo p/ IG/TikTok/YT/Pinterest; LinkedIn nativo + X 9:16 = net-new por canal | MÉDIO |
> 300	| **Motor de REPLY do X** (multiplicador ~150x author-reply) | broadcast-only não cresce no X — novo agent loop real-time (§2.5) | MÉDIO-ALTO (capacidade conversacional) |
> 301	| **Pipeline de voz** (`generate-voice` edge fn) | inexistente — paralelo a generate-image | NET-NEW |
> 302	| **Lip-sync verify / consistency multi-leg** | Vision QA compara frames mas sem checker dedicado | NET-NEW |
> 303	| **C2PA embedding no render** (LEGAL, não polish — §7) | render-core não embute manifest; pode quebrar sha256 determinismo (spike OTD-AC-008) | NET-NEW (compliance first-class) |
> 304	| **Storage/RLS/erase de artefatos biométricos** | tabelas `avatar_identities`/`voice_profiles` inexistentes (§4.4b) | CRÍTICO (PII biométrica) |
> 305	| **Identity-verification + consent artifact** (self-clone vs terceiro) | inexistente (§5.4) | CRÍTICO (gate de lançamento generalizado) |
> 306	
> 307	---
> 308	
> 309	## 7. Compliance — rotulagem de mídia sintética por canal (SEPARADO POR JURISDIÇÃO)
> 310	
> 311	> Gabriel AI é rosto+voz sintéticos de pessoa real → **rotular onde a jurisdição obriga**. ❌ **CORREÇÃO material:** o draft agrupava o **Brasil/CONAR** sob "disclosure de IA OBRIGATÓRIO" — INCORRETO. Separar FRs por jurisdição.
> 312	
> 313	| Canal / Jurisdição | Obrigação | Fonte |
> 314	|---|---|---|
> 315	| **YouTube** | toggle "Altered or synthetic content" obrigatório; tópicos sensíveis (saúde/notícia/eleição/finança) = rótulo proeminente ON-vídeo; aplica a vídeos/Shorts/lives; não-disclosure recorrente → desmonetização | https://blog.youtube/news-and-events/disclosing-ai-generated-content/ |
> 316	| **TikTok** | label "AI-generated" obrigatório p/ mídia realista; **auto-label via C2PA** confirmado em Help Center oficial (sem toggle quando Content Credentials presentes); sintético de PRIVADO real banido mesmo rotulado | https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content |
> 317	| **Meta/IG** | "AI Info"/"Made with AI" on-detect (C2PA/IPTC) ou self-disclose; ads com IA = disclosure no Ads Manager | https://transparency.meta.com/governance/tracking-impact/labeling-ai-content |
> 318	| **EU AI Act Art. 50** | a partir de **02/08/2026**: deployer de deepfake DEVE divulgar + provider DEVE **marcar output em formato machine-readable (C2PA)** — **NÃO adiado** pelo Digital Omnibus; GenAI já no mercado antes de 02/08/2026 tem até **02/12/2026** p/ a marcação machine-readable [Art.50(2)] | https://artificialintelligenceact.eu/article/50/ |
> 319	| **Brasil — CONAR** ❌ CORRIGIDO | vigor **01/06/2026** · **responsabilidade SOLIDÁRIA** anunciante+agência+influencer · obrigação de **identificar influencer virtual/avatar COMO personagem artificial** · afiliado = "#publi"/"parceria paga". **NÃO impõe** label "gerado por IA" como YouTube/TikTok/Meta/EU — modelar como (a) solidary-liability + (b) virtual-persona-identification, **não** como "AI-label mandate" | https://lawletter.com.br/guia-conar-2026-o-que-todo-influenciador-precisa-saber-agora/ · https://www.em.com.br/trends/2026/06/7443221-publi-escondida-e-ilegal-o-que-muda-com-as-novas-regras-do-conar-em-2026.html |
> 320	| **Brasil — TSE/Eleições 2026** | rótulo expresso+imediato p/ conteúdo político-IA; **EVITAR conteúdo eleitoral/candidato** | https://www.tribunadosertao.com.br/geral/2026/04/22/891114-influenciador-criado-por-ia-o-novo-foco-de-desinformacao-nas-eleicoes |
> 321	
> 322	**Recomendação de engenharia (FRs first-class, divididos por jurisdição):**
> 323	1. **Disclosure label** como **gate de publish não-pulável** no Viral Autopilot (mesma severidade do gate CF do WordPress) — FR aplicável a YouTube/TikTok/Meta.
> 324	2. **Embed C2PA no render = REQUISITO LEGAL** (EU Art.50, machine-readable, + auto-label TikTok), NÃO polish — move da Fatia 6 para FR de compliance first-class. ⚠️ resolve com OTD-AC-008 (C2PA vs determinismo sha256 NFR-VS-016) ANTES de selar a arquitetura de render.
> 325	3. **Brasil:** FR de identificação de persona virtual como artificial + solidary-liability (NÃO AI-label).
> 326	4. Encodar `persona_type` que dirige templates de compliance por jurisdição.
> 327	
> 328	---
> 329	
> 330	## 8. OTDs, FMEA, Frentes-pendentes, Pattern Conformance & Economics
> 331	
> 332	### 8.1 OTDs (Open Technical Decisions)
> 333	| ID | Decisão | Recomendação semente |
> 334	|---|---|---|
> 335	| OTD-AC-001 | Motor talking-head primário | ❌ HeyGen Avatar V **NÃO ancora self-serve BYOK** (partnership-gated, API direta indisponível, $4/min). Re-avaliar: Hedra/OmniHuman (self-serve, por-imagem) OU modelar tenancy master-account/partnership. **Decidir ANTES do SDD.** Manter só o núcleo: por-vídeo-referência > por-foto |
> 336	| OTD-AC-002 | Voz default | ❌ NÃO "PVC+v3". **PVC sobre Multilingual v2 OU IVC/Voice-Design sobre v3** + A/B material medindo sotaque PT-BR e code-switching |
> 337	| OTD-AC-003 | Identity-lock | Higgsfield Soul ID (≥20 fotos) — ⚠️ **TREINO via API self-serve NÃO-VERIFICADO**; ler docs logadas antes do SDD |
> 338	| OTD-AC-004 | Limiar cosine do Identity Gate | calibrar empiricamente (FAR/FRR/EER) — NÃO hardcodar 0.95 nem 0.7-0.8 |
> 339	| OTD-AC-005 | `avatar_renders` dedicada vs reuso `video_renders` + composition.template | reuso curto-prazo; dedicada se billing/finalize complexar |
> 340	| OTD-AC-006 | Cost model mcoCoins do avatar (4×-floor) | `AVATAR_VIDEO_COST` separado de `VIDEO_COST`; recalibrar com preços datados (ver §8.5) |
> 341	| OTD-AC-007 | Reshaper→publish: estender auto-publish (A) vs reshaper chama publish-social (B) | **caminho B JÁ EXISTE wired** (§6.2) — usar; falta só relaxar CHECK + gate de enqueue + step avatar |
> 342	| OTD-AC-008 | C2PA embed vs determinismo sha256 (NFR-VS-016) | **REQUISITO LEGAL (não opcional)** — spike técnico antes de selar render |
> ```

## 🤖 Claude *(00:29:30)*


## 🤖 Claude *(00:29:31)*

Lendo o restante (FMEA, frentes-pendentes, economics, roadmap de fatias).

## 🤖 Claude *(00:29:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md",
  "offset": 343,
  "limit": 80
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 343	| OTD-AC-009 | Motor de reply do X (real-time agent loop) | in-scope core OU suavizar promessa "paridade em TODOS os canais" — **decidir com Sovereign** |
> 344	| OTD-AC-010 | Fluxo de consentimento + identity-verification per-tenant | **gate de lançamento, não OTD diferido** (§5.4) |
> 345	| OTD-AC-011 | BYOK pass-through legal por provider | Front F1 — verificar ToS de cada provider antes do FRD |
> 346	| OTD-AC-012 | Modelo de duplicação bilíngue (renderizar 2× por idioma vs split por dia) | define se custo mensal dobra — **ratificar com Sovereign** |
> 347	| OTD-AC-013 | North-Star de marca + trigger de migração de Owner | brand evangelism não produz R$ direto — definir métrica (ver §8.4) |
> 348	| OTD-AC-014 | Reconciliar RAMP × 12+/mês | ramp por-canal independente; volume agregado cross-canal |
> 349	
> 350	### 8.2 FMEA (modos de falha)
> 351	| ID | Modo de falha | Mitigação |
> 352	|---|---|---|
> 353	| FM-AC-001 | Pesos non-comercial shippados (InfiniteYou/Fish/XTTS/**F5-TTS/FLUX.1-dev**) | gate de licença no SDD; só Apache/MIT/SaaS-BYOK |
> 354	| FM-AC-002 | Conteúdo IA indiferenciado → rebaixamento | persona com face/voz/POV consistente (o moat) |
> 355	| FM-AC-003 | Identity drift entre vídeos | Identity Gate ArcFace fail-and-regenerate + ordem identidade-antes-de-enhance |
> 356	| FM-AC-004 | Disclosure faltando (por jurisdição) | gate de publish não-pulável + C2PA (separado YouTube/TikTok/Meta/EU vs Brasil) |
> 357	| FM-AC-005 | Charge-without-value (video_renders sem row) | `refund_autopilot_video_enqueue` idempotente |
> 358	| FM-AC-006 | Conta nova flagada por spam/sintético | RAMP server-side + Front F2 (viabilidade avatar) |
> 359	| FM-AC-007 | Clip byte-idêntico cross-canal | reshaper emite variante NATIVA |
> 360	| FM-AC-008 | Trending audio morto postado | detecção semanal; default original-sound |
> 361	| FM-AC-009 | Conteúdo eleitoral BR (TSE) | escopar autoridade a produto/tech, não política |
> 362	| FM-AC-010 | BYOK ToS proíbe pass-through (HeyGen/Magnific) | Front F1 antes de codar |
> 363	| FM-AC-011 | Cross-tenant leak de weights LoRA/voz/embeddings (PII biométrica) | RLS own-or-org + storage isolado per-tenant + erase RPC (§4.4b) |
> 364	| FM-AC-012 | Lip-sync/prosódia PT-BR ruim (benchmarks são EN) | Front F3 — validar fonemas PT-BR antes de declarar fiel |
> 365	| FM-AC-013 | Code-switching PT-BR↔EN na mesma geração (falha ElevenLabs documentada) | separar idiomas por geração; nunca code-switch intra-frase |
> 366	
> 367	### 8.3 Frentes de pesquisa pendentes (a fechar antes do FRD)
> 368	- **F1 — Legalidade BYOK pass-through por provider** (ElevenLabs/Cartesia/Magnific/Higgsfield/HeyGen diferem): cada ToS lido p/ saber se a chave do end-user pode ser guardada+usada pelo MCORCH em nome dele. **Bloqueante p/ §4.4a.**
> 369	- **F2 — Avatares sintéticos crescem em 2025-2026?** Case studies reais com dados de retenção/crescimento. **Hipótese de viabilidade do programa inteiro.**
> 370	- **F3 — Fidelidade talking-head + voz p/ FONEMAS PT-BR** (todos os benchmarks atuais são EN). Load-bearing pelo mandato bilíngue.
> 371	- **F4 — Landscape competitivo de produtos AI-persona end-to-end** (Argil, Captions, HeyGen Video Agent, plataformas de AI-influencer): de-risca build-vs-buy do módulo.
> 372	- **F5 — Custo-at-scale com preços datados 2026** (HeyGen já provou-se errado no draft) — cenário mensal worked (ver §8.5).
> 373	- **F6 — Storage/retention/erasure de artefatos biométricos sob LGPD + EU AI Act** (limites de retenção de dado biométrico no Brasil).
> 374	- **F7 — Account-warming/onboarding de 6 canais × 2 idiomas** (App Review IG, audit YouTube, TikTok SELF_ONLY, X Premium): dependências gating.
> 375	
> 376	### 8.4 Métricas de sucesso da MARCA (gap do draft — definir antes do /bok-scribe)
> 377	Brand evangelism não produz R$ direto → trigger de Owner indefinido. Propor North-Star + KPIs por canal ANTES de selar BoK:
> 378	- **North-Star candidata:** crescimento de seguidores qualificados + `creative_metrics.hook_rate` agregado cross-canal + 1ª conversão de marca (signup atribuído a um post).
> 379	- **Por-canal:** YT (subs/mês, AVD), TikTok/IG (completion, sends-per-reach), LinkedIn (depth/comments), X (author-reply rate).
> 380	- **Tie ao existente:** `creative_metrics` + `collective_efficiency_ledger` (mco/resultado anti-Goodhart).
> 381	
> 382	### 8.5 ⚠️ Economics — unit cost a modelar (MAIOR GAP do draft, F5)
> 383	O draft NÃO computou custo por-vídeo nem por-ciclo-30d. Com preços CORRIGIDOS, **1 Short avatar de 30s tem custo marginal real** (talking-head + voz + Magnific enhance + regenerações do Identity Gate). Em steady-state (5 YT Shorts + 3-5 TikTok + 4-5 IG + 3-4 LinkedIn + X/dia × **2 trilhas idioma**) o volume mensal é grande. **A construir no FRD (Lei 1, preços datados):**
> 384	- tabela unit-economics datada 2026 (talking-head $/min CORRETO, voz $/1k chars, Magnific $/op, taxa de regeneração do gate);
> 385	- `AVATAR_VIDEO_COST` mcoCoins via modelo 4×-floor (`mco=ceil(usd/$0.018×4)`);
> 386	- daily-cap budget por tenant;
> 387	- **custo de 1 ciclo de 30 dias** com e sem duplicação bilíngue (OTD-AC-012 muda o total ~2×).
> 388	Sem isto o Sovereign NÃO consegue dimensionar o custo de um ciclo. **Este é o maior gap único.**
> 389	
> 390	### 8.6 Pattern Conformance Declaration (esboço — Gate Step 3.5)
> 391	Módulo toca ≥3 padrões agênticos → o `/bok-scribe` DEVE produzir a tabela completa dos 21 padrões (`docs/architecture/agentic-vision.md`). Padrões que este módulo claramente implementa (a confirmar no SDD):
> 392	- **Tool Use / Function Calling** — nós chamam providers (talking-head, voz, enhance).
> 393	- **Self-Correction / Reflection** — Identity Gate fail-and-regenerate (loop ArcFace).
> 394	- **Retrieval-Augmented Generation** — "cérebro clonado" (RAG sobre `mcorch_nodes`).
> 395	- **Multi-step Pipeline / Orchestration** — pipeline identity→voice→script→head→enhance + junção Autopilot.
> 396	- **Guardrails / Safety** — sentinel + disclosure/consent gates.
> 397	- **(candidato) Conversational/Reactive loop** — reply engine do X (se OTD-AC-009 = in-scope).
> 398	Os demais 15 marcados `deferred`/`n-a` com justificativa material na SDD.
> 399	
> 400	---
> 401	
> 402	## 9. Roadmap de FATIAS (ordem de construção)
> 403	
> 404	> **Gate Closed-Loop:** módulo novo tocando ≥3 padrões agênticos → **BoK suite (MRD/BRD/PRD/FRD/SDD) + Pattern Conformance Declaration ANTES de qualquer código** (`/bok-scribe avatar-clone-ai`).
> 405	
> 406	- **Fatia 0 — BoK + verify adversarial.** Fechar Frentes F1-F7 (BYOK-legality, viabilidade-avatar, PT-BR fonemas, competidores, economics, biometric-erasure, account-warming). Dobrar disclosure/C2PA/CONAR-por-jurisdição/Art.50/consent-self-clone como FRs de compliance **first-class**. Definir North-Star de marca (§8.4) e modelo de duplicação bilíngue (OTD-AC-012).
> 407	- **Fatia 1 — BYOK credenciais avatar.** Migration `user_api_keys` (heygen/magnific/elevenlabs/cartesia) + UI Settings + test-api-key + lookup helper, **gated em F1 (ToS pass-through por provider)**.
> 408	- **Fatia 2 — Nó `voiceClone`.** `generate-voice` edge fn (ElevenLabs Multilingual-v2-PVC OU IVC-v3) + nó Canvas + creative_assets. **Validar code-switching PT-BR↔EN (FM-AC-013) + voice_profiles RLS (§4.4b).**
> 409	- **Fatia 3 — Nó `avatarIdentity` + Identity Gate.** Soul ID/LoRA (⚠️ resolver TREINO-via-API) + ArcFace cosine gate (estende Vision QA, limiar CALIBRADO via FAR/FRR). `avatar_identities` RLS own + storage isolado.
> 410	- **Fatia 4 — Nó `avatarScript` (cérebro clonado).** RAG sobre `mcorch_nodes` + Brand Voice DNA quantificado (PT-BR/EN).
> 411	- **Fatia 5 — Nó `talkingHead` + `avatarEnhance`.** Motor por-vídeo-referência (OTD-AC-001 resolvido) + Magnific Relight/upscale (ordem: identidade ANTES de enhance) → MP4 9:16. Reusa video_renders/finalize.
> 412	- **Fatia 6 — C2PA + disclosure/consent gate.** Embed manifest no render (**REQUISITO LEGAL**, spike determinismo OTD-AC-008) + gate de publish não-pulável + identity-verification self-clone (§5.4).
> 413	- **Fatia 7 — Repurpose nativo por canal.** Estender `reshape-pillar`/`channel_variants` p/ avatar (campos de script + asset_key vídeo); branches vídeo LinkedIn/X net-new em publish-social. (Caminho reshaper→publish-social JÁ existe — §6.2.)
> 414	- **Fatia 8 — JUNÇÃO com Viral Autopilot.** **Relaxar CHECK de `autopilot_plans.platforms`** (add yt/tiktok/ig/pinterest) + estender `VIDEO_FLOW_PLATFORMS`→`AVATAR_FLOW_PLATFORMS` + step `avatar_generation` independente do article-flow + billing avatar separado + refund idempotente. Cadência 30-dias com RAMP server-side (números ilustrativos).
> 415	- **Fatia 9 (gated, decisão Sovereign) — motor de REPLY do X** (OTD-AC-009, novo agent loop real-time) + X Premium.
> 416	
> 417	---
> 418	
> 419	## Próximo passo (Gate Closed-Loop)
> 420	
> 421	> **Antes de qualquer linha de código:** rodar **`/bok-scribe avatar-clone-ai`** para selar a suíte BoK (MRD → BRD → PRD → FRD → SDD) **+ a Pattern Conformance Declaration** (os 21 padrões de `docs/architecture/agentic-vision.md`), usando este blueprint como Fonte da Verdade única. Os OTDs marcados "decidir com Sovereign" (esp. OTD-AC-001 motor, OTD-AC-009 reply engine, OTD-AC-012 duplicação bilíngue, OTD-AC-013 North-Star) e as Frentes F1-F7 devem ser fechados na Fatia 0 do Scribe. Refusal Mode permanece ativo até a suíte existir.
> 422	
> ```

## 🤖 Claude *(00:30:36)*


## 🤖 Claude *(00:30:54)*

Blueprint inteiro lido e verificado. É um **seed forte e materialmente honesto** — a verificação adversarial pegou e corrigiu **6 claims falsas** antes de virarem premissa (isso é ouro, evita selar a BoK sobre dado furado):

| Refutado | Verdade corrigida |
|---|---|
| HeyGen Avatar V = $3/min self-serve BYOK | ❌ **$4/min, API direta indisponível, BYOK partnership-gated** — não ancora self-serve |
| Voz = "ElevenLabs PVC + v3" | PVC é sobre Multilingual-v2; **code-switching PT↔EN na mesma frase é falha conhecida** |
| F5-TTS = self-host comercial limpo | ❌ pesos **CC-BY-NC** (não-comercial) — não shippar |
| Identity Gate "~85% / cosine 0.7-0.8" | números sem fonte; **calibrar empiricamente (FAR/FRR/EER)**, não hardcodar |
| Brasil/CONAR impõe "rótulo de IA" | ❌ CONAR = **responsabilidade solidária + identificar persona virtual**, não AI-label |
| "reshaper não publica vídeo" | ❌ **caminho já existe wired** no código — gap real é o CHECK de plataformas + step avatar |

**📦 O que está no disco:** `docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md` — 55KB, 421 linhas, 9 seções, untracked. Slug **`avatar-clone-ai`** (Gabriel AI = instância-zero de um módulo per-user generalizável).

**🎯 A estratégia (resumo):**
- **Moat ≠ volume.** O YouTube de 2026 não bane IA — **rebaixa output indiferenciado**. Por isso a persona PRECISA de rosto/voz/POV consistentes (= seu módulo Avatar). Mas há um **risco existencial** (abaixo).
- **Cadência 30 dias = 1ª perna de 90d**, funil S1 Awareness → S2 Education → S3 Social-Proof → S4 Conversion. Steady-state: YT 5 Shorts+1-2 longos/sem · TikTok 3-5/sem · IG 4-5/sem+Stories · LinkedIn 3-4/sem · X 3-5/dia. Mix **40% educação / 40% autoridade / ≤20% produto** (conta nova começa 70/20/10). **1 pilar/dia → N variantes nativas** via o Channel Reshaper que já temos. Tabela Dia 1→30 completa no doc.
- **Avatar (stack corrigido):** módulo próprio multi-provider BYOK no Canvas — `avatarIdentity → voiceClone → avatarScript(RAG da malha) → talkingHead → avatarEnhance(Magnific) → Identity Gate(ArcFace) → C2PA → Autopilot`. **Magnific ≡ Freepik** (mesma empresa; chave intercambiável) mas **só com plano PAGO per-tenant** e é **polish final, nunca autor de identidade**. **"Martini Art/Film" = web sem API** → servem de inspiração de UX dos nós, não alvo de integração.
- **Compliance é requisito legal, não polish:** **C2PA machine-readable** (EU AI Act Art.50 a partir de 02/08/2026 + auto-label TikTok) + disclosure por jurisdição. Brasil tem regra própria (CONAR solidário + TSE eleitoral — escopar longe de política).

## 🤖 Claude *(00:30:56)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Programa Gabriel AI \u2014 blueprint",
  "summary": "Deepsearch for\u00e7a-total \u2192 blueprint-semente avatar-clone-ai (m\u00f3dulo per-user Avatar/Clone AI + estrat\u00e9gia viral + cad\u00eancia 30d); decis\u00f5es Sovereign antes do /bok-scribe"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Programa Gabriel AI — blueprint". Continue your current work.'}]
> ```

## 🤖 Claude *(00:30:58)*


## 🤖 Claude *(00:31:00)*

O Closed-Loop manda agora: **`/bok-scribe avatar-clone-ai`** para selar a BoK antes de qualquer código. Mas antes de eu disparar o Scribe, **4 decisões são suas** (Lei 4 — o blueprint as marcou explicitamente como "decidir com Sovereign"; elas mudam as premissas da BoK). Te dou minha recomendação em cada uma:

## 🤖 Claude *(00:31:28)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "A verifica\u00e7\u00e3o trouxe um risco que pode invalidar o programa inteiro: plataformas (esp. TikTok) d\u00e3o escrut\u00ednio MAIOR a avatares 100%-sint\u00e9ticos \u2014 detec\u00e7\u00e3o no upload + supress\u00e3o de padr\u00e3o 'templated' mesmo rotulado. Nenhum dado de crescimento que achamos \u00e9 avatar-espec\u00edfico. Como tratar?",
      "header": "Viabilidade",
      "multiSelect": false,
      "options": [
        {
          "label": "Probe de viabilidade (Fatia 0)",
          "description": "Antes de selar a BoK, rodar pesquisa focada em case studies REAIS de canais 100%-avatar (reten\u00e7\u00e3o/crescimento/bans 2025-2026) \u2192 go/no-go com dado. Barato; evita construir o m\u00f3dulo inteiro sobre uma hip\u00f3tese furada."
        },
        {
          "label": "H\u00edbrido: avatar + seu rosto real",
          "description": "N\u00e3o 100% avatar. Alternar conte\u00fado com seu rosto real e o avatar \u2014 reduz risco de detec\u00e7\u00e3o/rebaixamento desde o dia 1 e ainda valida a persona. O avatar entra gradual."
        },
        {
          "label": "Seguir na convic\u00e7\u00e3o",
          "description": "Tratar como risco gerenci\u00e1vel (r\u00f3tulo honesto + qualidade autoral + POV consistente) e ir direto pro /bok-scribe sem o probe."
        }
      ]
    },
    {
      "question": "HeyGen caiu na verifica\u00e7\u00e3o (sem API self-serve, partnership-gated, $4/min). Qual dire\u00e7\u00e3o pro motor de talking-head fiel? (muda economics + quem-paga)",
      "header": "Motor avatar",
      "multiSelect": false,
      "options": [
        {
          "label": "Self-serve per-user (Hedra/OmniHuman)",
          "description": "BYOK puro: cada user traz a pr\u00f3pria chave (Hedra Character-3 ~$0.05/min). Fiel ao 'sempre per-user' do MCORCH; fidelidade por-imagem (um pouco menor que digital-twin). Soberano e multi-tenant limpo."
        },
        {
          "label": "Conta-mestra MCORCH (partnership)",
          "description": "MCORCH det\u00e9m a conta premium (HeyGen/parceria); maior fidelidade de talking-head; muda o modelo de tenancy + quem-paga (mcoCoins cobre o custo). Menos soberano, depende de aprova\u00e7\u00e3o de parceria."
        },
        {
          "label": "BoK decide ap\u00f3s ler docs logadas",
          "description": "Adiar a escolha do motor; o /bok-scribe l\u00ea ToS/docs logadas de cada provider (Hedra/OmniHuman/Higgsfield) e fecha OTD-AC-001 na Fatia 0 com prova."
        }
      ]
    },
    {
      "question": "PT-BR + EN \u2014 como renderizar os v\u00eddeos? Isso define se o custo mensal do ciclo dobra (OTD-AC-012).",
      "header": "Bil\u00edngue",
      "multiSelect": false,
      "options": [
        {
          "label": "1 render/dia, idioma alterna",
          "description": "Cada pilar renderiza UMA vez; os dias alternam PT/EN; a trilha B reusa o mesmo mestre 9:16 re-locando a voz clonada cross-lingual. ~Metade do custo. Marca aparece nas duas l\u00ednguas sem dobrar render."
        },
        {
          "label": "2 l\u00ednguas no mesmo dia",
          "description": "Cada pilar sai em PT e EN no MESMO dia. Dobra o alcance e ~dobra o custo de render + voz + Identity Gate. Cobertura m\u00e1xima, custo m\u00e1ximo."
        },
        {
          "label": "S\u00f3 PT-BR agora, EN depois",
          "description": "Come\u00e7ar monol\u00edngue pra validar barato (mercado BR, voz nativa) e ligar a trilha EN s\u00f3 ap\u00f3s os primeiros resultados. De-risca custo e viabilidade primeiro."
        }
      ]
    },
    {
      "question": "Crescer no X exige um motor de REPLY (a persona responde comentadores na 1\u00aa hora \u2192 multiplicador ~150x author-reply). \u00c9 um agent loop conversacional real-time NET-NEW que o Autopilot (broadcast-only) n\u00e3o tem. Entra no escopo?",
      "header": "Reply X",
      "multiSelect": false,
      "options": [
        {
          "label": "Fatia posterior (gated)",
          "description": "Lan\u00e7ar X em modo broadcast agora (posta thread+v\u00eddeo); o reply engine vira fatia separada depois. X cresce capado at\u00e9 l\u00e1, mas mant\u00e9m o escopo inicial enxuto e entrega valor mais r\u00e1pido."
        },
        {
          "label": "Escopo core agora",
          "description": "Construir o reply engine j\u00e1: monitorar mentions \u2192 gerar reply do 'c\u00e9rebro clonado' \u2192 postar em minutos. X cresce de verdade, mas adiciona uma capacidade conversacional real-time ao programa (mais escopo)."
        },
        {
          "label": "Suavizar promessa do X",
          "description": "Aceitar que o X n\u00e3o ter\u00e1 paridade total de automa\u00e7\u00e3o; tratar como canal secund\u00e1rio e focar a for\u00e7a nos canais de v\u00eddeo (YT/TikTok/IG)."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "A verificação trouxe um risco que pode invalidar o programa inteiro: plataformas (esp. TikTok) dão escrutínio MAIOR a avatares 100%-sintéticos — detecção no upload + supressão de padrão 'templated' mesmo rotulado. Nenhum dado de crescimento que achamos é avatar-específico. Como tratar?"="Probe de viabilidade (Fatia 0)", "HeyGen caiu na verificação (sem API self-serve, partnership-gated, $4/min). Qual direção pro motor de talking-head fiel? (muda economics + quem-paga)"="Sempre per-user, então usar hedra/omniHuman e higgsfield são obrigatórios para os usuários caso queiram ter maior fidelidade de talking-head, mas tambem podemos ter a opção hibrida onde depois podemos procurar alguma forma de criar nosso próprio motor de fidelidade clone ai ou avatar ai, e tentar no futuro programas de partnership", "PT-BR + EN — como renderizar os vídeos? Isso define se o custo mensal do ciclo dobra (OTD-AC-012)."="O idioma deve ser opt-in e conforme a liguagem padrão do usuário, se nas configurações de usuários é pt-br o padrão selecionado para ele vai ser pt-br com optin (opçõa) de alterar o idioma. E tambem a frequencia, além disso para o usuário 0 vamos fazer o padrão validado para quem esta produzindo do Brasil, apesar de que as contas tiktok e youtube que ja tem videos postados mesmo que sem muitos resultados mas que já dão um norte para continuar https://www.youtube.com/@uxnai/videos e https://www.tiktok.com/@gabriel_mcorch audios em ingles e legendas em portugues mas se necessário pesquise qual o melhor formato para nós e adicione isso em algum lugar do nosso ecossistema para ser revisitado no UI, não sei foi pensando nisso que eu pedi para criar o workspace kanban em https://login.mcorch.com/dashboard/kanban e tambem https://login.mcorch.com/dashboard/chat para ver o que esta rolando, qual os planos, pipelines e roadmaps em ação e definidos.", "Crescer no X exige um motor de REPLY (a persona responde comentadores na 1ª hora → multiplicador ~150x author-reply). É um agent loop conversacional real-time NET-NEW que o Autopilot (broadcast-only) não tem. Entra no escopo?"="Escopo core agora". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(00:50:46)*


## 🤖 Claude *(00:50:51)*

Decisões capturadas, Maestro — e elas são **mais ricas que as opções**. Deixa eu registrar no blueprint (Fonte da Verdade do Scribe) e então rodar **exatamente o probe de viabilidade que você pediu** como gate.

Resumo do que você decidiu:
1. **Viabilidade → probe primeiro** (gate antes da BoK) ✅
2. **Motor avatar → self-serve per-user obrigatório** (Hedra/OmniHuman/Higgsfield BYOK); **híbrido futuro** = construir nosso próprio motor de fidelidade + buscar partnership (HeyGen) depois ✅
3. **Idioma/frequência → per-user opt-in** (default = língua das settings do user; opção de trocar idioma E frequência; sem duplicação forçada 2×); **Usuário Zero = default BR validado**. Sinal first-party real: suas contas [@uxnai](https://www.youtube.com/@uxnai/videos) (YT) e [@gabriel_mcorch](https://www.tiktok.com/@gabriel_mcorch) (TikTok) usam **áudio EN + legenda PT** — a Fatia 0 vai analisar e recomendar o melhor formato ✅
4. **Reply do X → escopo core agora** ✅

Gravando no blueprint:

## 🤖 Claude *(00:50:55)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md",
  "old_string": "Re-avaliar: Hedra/OmniHuman (self-serve, por-imagem) OU modelar tenancy master-account/partnership. **Decidir ANTES do SDD.** Manter s\u00f3 o n\u00facleo: por-v\u00eddeo-refer\u00eancia > por-foto |",
  "new_string": "**\u2705 RESOLVIDO (Sovereign 2026-06-29): SELF-SERVE PER-USER obrigat\u00f3rio** \u2014 Hedra/OmniHuman/Higgsfield BYOK (cada user traz a pr\u00f3pria chave p/ maior fidelidade). **H\u00edbrido FUTURO (deferido):** (a) construir motor PR\u00d3PRIO de fidelidade Clone/Avatar AI; (b) buscar partnership (HeyGen). N\u00facleo preservado: por-v\u00eddeo-refer\u00eancia > por-foto |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:50:58)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md",
  "old_string": "| OTD-AC-009 | Motor de reply do X (real-time agent loop) | in-scope core OU suavizar promessa \"paridade em TODOS os canais\" \u2014 **decidir com Sovereign** |",
  "new_string": "| OTD-AC-009 | Motor de reply do X (real-time agent loop) | **\u2705 RESOLVIDO (Sovereign 2026-06-29): ESCOPO CORE AGORA.** Agent loop conversacional real-time (monitorar mentions \u2192 reply do \"c\u00e9rebro clonado\" \u2192 postar em minutos) entra no core; sobe de Fatia 9-gated. Padr\u00e3o ag\u00eantico Conversational/Reactive loop = **implementado**, n\u00e3o candidato |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:51:02)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md",
  "old_string": "| OTD-AC-012 | Modelo de duplica\u00e7\u00e3o bil\u00edngue (renderizar 2\u00d7 por idioma vs split por dia) | define se custo mensal dobra \u2014 **ratificar com Sovereign** |",
  "new_string": "| OTD-AC-012 | Modelo de idioma + frequ\u00eancia (era \"duplica\u00e7\u00e3o bil\u00edngue\") | **\u2705 RESOLVIDO (Sovereign 2026-06-29): PER-USER OPT-IN.** Idioma default = l\u00edngua das settings do user (pt-BR nas settings \u2192 render pt-BR), com op\u00e7\u00e3o (opt-in) de trocar idioma E frequ\u00eancia. SEM duplica\u00e7\u00e3o for\u00e7ada 2\u00d7. Usu\u00e1rio Zero = default validado p/ produtor BR. Formato-\u00e2ncora a pesquisar na Fatia 0 (contas reais @uxnai/@gabriel_mcorch usam \u00e1udio EN + legenda PT) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:51:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md",
  "old_string": "---\n\n## 1. Tese & posicionamento da marca \"Gabriel AI\"",
  "new_string": "---\n\n## 0. Decis\u00f5es Sovereign (2026-06-29) \u2014 resolu\u00e7\u00e3o p\u00f3s-blueprint\n\nQuatro OTDs \"decidir com Sovereign\" foram resolvidos; registrados aqui como Fonte da Verdade para o `/bok-scribe`:\n\n1. **Viabilidade (gate) \u2192 PROBE PRIMEIRO (Fatia 0).** Antes de selar a BoK, rodar pesquisa de viabilidade com case studies REAIS de canais 100%-avatar / h\u00edbrido / faceless (reten\u00e7\u00e3o/crescimento/penalidades 2025-2026) \u2192 go/no-go material. Produz `00b-fatia0-viability-format-probe.md`. Refusal Mode da BoK permanece at\u00e9 este gate fechar.\n2. **OTD-AC-001 motor talking-head \u2192 SELF-SERVE PER-USER obrigat\u00f3rio** (Hedra/OmniHuman/Higgsfield BYOK; user traz a pr\u00f3pria chave). **H\u00edbrido FUTURO (deferido):** (a) motor PR\u00d3PRIO de fidelidade Clone/Avatar AI; (b) partnership (HeyGen). N\u00e3o bloqueia o lan\u00e7amento self-serve.\n3. **OTD-AC-009 reply engine do X \u2192 ESCOPO CORE AGORA.** Sobe de Fatia 9-gated para fatia core.\n4. **OTD-AC-012 idioma/frequ\u00eancia \u2192 PER-USER OPT-IN.** Default = l\u00edngua das settings do user; op\u00e7\u00e3o de trocar idioma E frequ\u00eancia; sem duplica\u00e7\u00e3o 2\u00d7 for\u00e7ada. Usu\u00e1rio Zero = default BR validado.\n\n**Formato-\u00e2ncora a pesquisar (sinal first-party do Sovereign):** as contas j\u00e1 no ar \u2014 YouTube `@uxnai` (https://www.youtube.com/@uxnai/videos) e TikTok `@gabriel_mcorch` (https://www.tiktok.com/@gabriel_mcorch) \u2014 usam hoje **\u00e1udio em ingl\u00eas + legenda em portugu\u00eas** (resultado modesto, mas d\u00e1 o \"norte\"). A Fatia 0 deve analisar essas contas + recomendar o MELHOR formato para um criador de IA bil\u00edngue de origem BR, e **expor a recomenda\u00e7\u00e3o no ecossistema (UI) para revisitar** \u2014 candidatos: os workspaces **Kanban** (`/dashboard/kanban`) e **Chat** (`/dashboard/chat`), onde o Sovereign quer ver planos/pipelines/roadmaps em a\u00e7\u00e3o.\n\n---\n\n## 1. Tese & posicionamento da marca \"Gabriel AI\""
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/avatar-clone-ai/00-deepsearch-blueprint.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:51:13)*


## 🤖 Claude *(00:51:15)*

Blueprint atualizado com as 4 resoluções. Agora o **gate**: disparando o **probe de viabilidade + formato (Fatia 0)** — a pesquisa que decide se canal 100%-avatar cresce de verdade, analisa suas 2 contas reais, e crava o melhor formato pra nós. Roda em background.

## 🤖 Claude *(00:52:11)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'avatar-clone-ai-fatia0-viability-format-probe',\n  description: 'Gate Fatia 0: viabilidade de canal 100%-avatar/hibrido/faceless (go-no-go) + analise das contas reais @uxnai/@gabriel_mcorch + melhor formato bilingue BR -> 00b-fatia0 report',\n  phases: [\n    { title: 'Probe', detail: 'Viabilidade (case studies + risco) + contas reais + formato + competidores' },\n    { title: 'Verify', detail: 'Refutar adversarialmente o veredicto central go/no-go + o formato' },\n    { title: 'Synthesize', detail: 'Escreve 00b-fatia0-viability-format-probe.md + go/no-go' },\n  ],\n}\n\nconst CTX = `\nGATE Fatia 0 do modulo MCORCH \"avatar-clone-ai\" (programa \"Gabriel AI\"). O Sovereign decidiu: avatar = modulo per-user BYOK no Canvas Studio (Hedra/OmniHuman/Higgsfield self-serve); idioma/frequencia per-user opt-in (default = lingua das settings; Usuario Zero = produtor BR). ANTES de selar a BoK, esta pesquisa-gate decide UMA pergunta de viabilidade que pode invalidar o programa inteiro: canais 100%-avatar (talking-head sintetico de pessoa real) realmente CRESCEM em 2025-2026, ou plataformas suprimem/penalizam sintetico a ponto de inviabilizar? E qual o MELHOR formato para nos.\n\nPersona \"Gabriel AI\" = fundador de IA/automacao bilingue (PT-BR + EN), video-first, build-in-public do MCORCH (jornada AGI->ASI) + educacao + tie-in afiliado. Contas reais ja no ar (sinal first-party, resultado modesto mas dao o norte): YouTube https://www.youtube.com/@uxnai/videos e TikTok https://www.tiktok.com/@gabriel_mcorch \u2014 formato atual = AUDIO EM INGLES + LEGENDA EM PORTUGUES.\n\nLAW 1 (Materiality): toda claim externa carrega a URL-fonte EXATA. NUNCA fabricar numero de views/inscritos/retencao nem URL. Se uma pagina (TikTok/YouTube) bloquear scraping/bot, DIGA isso honestamente e caia para web-search do handle + mencoes publicas \u2014 nao invente metricas. Prefira fontes 2025-2026.\n`;\n\nconst FRONTS = [\n  { key: 'viab-growth', prompt: 'FRENTE VIABILIDADE-CRESCIMENTO: ache CASE STUDIES REAIS de canais 100%-avatar / digital-twin / AI-presenter que CRESCERAM em 2025-2026 (YouTube/TikTok/IG/Reels). Numeros concretos: inscritos/views/retencao/monetizacao, nicho, e o que funcionou. Existe prova de que um canal de talking-head sintetico de IA atinge audiencia significativa hoje? Quais nichos toleram melhor? Cada numero com URL-fonte.' },\n  { key: 'viab-risk', prompt: 'FRENTE VIABILIDADE-RISCO: levante a EVIDENCIA NEGATIVA \u2014 penalidades, supressao, shadowban, desmonetizacao ou banimento de conteudo sintetico/avatar em TikTok/YouTube/IG em 2025-2026; deteccao no upload (artefatos GAN/lip-sync); supressao de padrao \"templated/spam\" mesmo quando rotulado. Compare: canais FACELESS (voz real + b-roll, sem rosto) e HIBRIDOS (rosto real + avatar) sofrem menos? Qual a trajetoria da postura das plataformas? Cada claim com URL-fonte.' },\n  { key: 'acct-youtube', prompt: 'FRENTE CONTA-REAL YT: analise o canal YouTube https://www.youtube.com/@uxnai/videos \u2014 que conteudo posta, formato (audio EN + legenda PT?), duracao, cadencia, e quaisquer sinais publicos de performance (views/inscritos). Use WebFetch/WebSearch; se o YouTube bloquear, busque \"uxnai youtube\" + use socialblade/mencoes publicas. Reporte HONESTAMENTE o que conseguiu e o que NAO conseguiu acessar (Lei 1). Diagnostico: o que esta funcionando/nao no formato atual?' },\n  { key: 'acct-tiktok', prompt: 'FRENTE CONTA-REAL TIKTOK: analise o perfil TikTok https://www.tiktok.com/@gabriel_mcorch \u2014 conteudo, formato (audio EN + legenda PT?), duracao, cadencia, sinais publicos (views/seguidores/likes). Use WebFetch/WebSearch; TikTok frequentemente bloqueia bot \u2014 se bloquear, busque \"@gabriel_mcorch tiktok\" + agregadores publicos e DIGA o que nao deu p/ acessar (Lei 1, nunca invente metrica). Diagnostico do formato atual.' },\n  { key: 'best-format', prompt: 'FRENTE FORMATO: qual o MELHOR formato para um criador de IA bilingue de ORIGEM BRASIL mirando BR + global? Compare com evidencia: (a) AUDIO EM INGLES + legenda PT (formato atual do Sovereign), (b) AUDIO PT + legenda EN, (c) duas trilhas nativas separadas por idioma, (d) audio nativo + auto-captions/dub. Cobertura: alcance/retencao de legendas vs dublagem, preferencia de audiencia BR por audio nativo vs EN, como YouTube/TikTok tratam multi-idioma (audio tracks, auto-dub, legendas), e o trade-off alcance-global vs conexao-local. Recomende UM formato-ancora + por que. Cada claim com URL-fonte.' },\n  { key: 'comp-playbook', prompt: 'FRENTE COMPETIDOR-PLAYBOOK: ache criadores/canais AI-persona ou faceless que ESCALARAM de verdade (com numeros) e destile o playbook replicavel \u2014 cadencia, formato, hooks, como lidam com disclosure de IA, monetizacao. O que copiar para o \"Gabriel AI\". Cada claim com URL-fonte.' },\n];\n\nconst FRONT_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['front', 'keyFindings', 'recommendations', 'openQuestions'],\n  properties: {\n    front: { type: 'string' },\n    keyFindings: { type: 'array', items: { type: 'object', additionalProperties: false,\n      required: ['claim', 'detail', 'sourceUrl', 'confidence'],\n      properties: { claim: { type: 'string' }, detail: { type: 'string' }, sourceUrl: { type: 'string' }, confidence: { enum: ['high', 'medium', 'low'] } } } },\n    recommendations: { type: 'array', items: { type: 'string' } },\n    openQuestions: { type: 'array', items: { type: 'string' } },\n  },\n};\n\nconst VERDICT_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['claim', 'verdict', 'evidence', 'sourceUrl'],\n  properties: {\n    claim: { type: 'string' }, verdict: { enum: ['confirmed', 'refuted', 'uncertain'] },\n    evidence: { type: 'string' }, sourceUrl: { type: 'string' },\n  },\n};\n\nconst SYNTH_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  required: ['path', 'verdict', 'recommendedPosture', 'bestFormat', 'executiveSummary', 'kanbanSurfacingNote'],\n  properties: {\n    path: { type: 'string' },\n    verdict: { enum: ['go', 'go-hybrid', 'no-go', 'uncertain'] },\n    recommendedPosture: { type: 'string' },\n    bestFormat: { type: 'string' },\n    executiveSummary: { type: 'string' },\n    kanbanSurfacingNote: { type: 'string' },\n  },\n};\n\nphase('Probe')\nlog('Disparando 6 frentes de viabilidade + contas reais + formato...')\nconst research = (await parallel(FRONTS.map(f => () => agent(CTX + '\\n\\n' + f.prompt + '\\n\\nRetorne findings estruturados; cada keyFinding com a URL-fonte exata.', { label: 'probe:' + f.key, phase: 'Probe', schema: FRONT_SCHEMA, agentType: 'deepsearch-blueprint' })))).filter(Boolean)\nlog('Frentes: ' + research.length + '/6. Verificando o veredicto central...')\n\nphase('Verify')\nconst claims = [\n  'Um canal 100%-avatar (talking-head sintetico de uma pessoa real) consegue crescer ate uma audiencia significativa e monetizavel em 2025-2026 sem ser suprimido/penalizado pelas plataformas.',\n  'Para um criador de IA bilingue de origem Brasil, audio em ingles + legenda em portugues maximiza alcance melhor do que audio nativo PT-BR.',\n  'Canais faceless ou hibridos (rosto real + avatar) crescem com MENOS risco de supressao do que canais 100%-avatar sintetico.',\n];\nconst verdicts = (await parallel(claims.map((c, i) => () => agent('Fact-check adversarial (tente REFUTAR; default \"uncertain\" se nao houver fonte autoritativa). Busque na web e cite a URL exata.\\n\\nCLAIM: ' + c, { label: 'verify:' + i, phase: 'Verify', schema: VERDICT_SCHEMA, agentType: 'deepsearch-blueprint' })))).filter(Boolean)\nlog('Veredictos: ' + JSON.stringify(verdicts.map(v => v.verdict)))\n\nphase('Synthesize')\nconst final = await agent(\n  CTX + '\\n\\nVoce e o SINTETIZADOR do gate Fatia 0. Escreva o relatorio em docs/bok/avatar-clone-ai/00b-fatia0-viability-format-probe.md (rode `mkdir -p docs/bok/avatar-clone-ai` antes; cwd = repo root /home/gcrUX/htdocs/constellation-orchestra). PT-BR, registro executivo, estilo MCORCH.\\n\\n'\n  + '=== RESEARCH JSON ===\\n' + JSON.stringify(research) + '\\n=== VERDICTS ===\\n' + JSON.stringify(verdicts) + '\\n=== END ===\\n\\n'\n  + 'O relatorio DEVE conter: (1) VEREDICTO go / go-hybrid / no-go / uncertain com justificativa material; (2) POSTURA recomendada (100%-avatar vs hibrido rosto-real+avatar vs faceless) ancorada nos case studies + verdicts; (3) diagnostico das 2 contas reais (@uxnai, @gabriel_mcorch) \u2014 o que conseguiu medir e o que ficou bloqueado (Lei 1); (4) FORMATO-ancora recomendado (audio EN+legenda PT vs alternativas) com fontes; (5) playbook competitivo a copiar; (6) como isto ATUALIZA o blueprint 00 (quais OTDs/FMEA/Fatias mudam); (7) nota de surfacing no UI (Kanban /dashboard/kanban + Chat /dashboard/chat) \u2014 o que expor do roadmap/cadencia. Toda claim com URL-fonte; refutadas marcadas. Termine com: se verdict=go ou go-hybrid -> proximo passo = fechar frentes F1/F3/F4/F5/F6/F7 e rodar /bok-scribe avatar-clone-ai; se no-go -> recomendar o pivot.\\n\\n'\n  + 'Retorne: path, verdict, recommendedPosture, bestFormat, executiveSummary (8-12 linhas), kanbanSurfacingNote.',\n  { label: 'synthesize-fatia0', phase: 'Synthesize', schema: SYNTH_SCHEMA, agentType: 'general-purpose', effort: 'high' })\n\nlog('Relatorio Fatia 0 escrito em ' + final.path + ' \u2014 verdict=' + final.verdict)\nreturn { final, verdicts, fronts: research.length }",
  "description": "Probe de viabilidade + formato Fatia 0 (gate)"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: w4vtwrye2
> Summary: Gate Fatia 0: viabilidade de canal 100%-avatar/hibrido/faceless (go-no-go) + analise das contas reais @uxnai/@gabriel_mcorch + melhor formato bilingue BR -> 00b-fatia0 report
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/subagents/workflows/wf_b949ad64-396
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/workflows/scripts/avatar-clone-ai-fatia0-viability-format-probe-wf_b949ad64-396.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/workflows/scripts/avatar-clone-ai-fatia0-viability-format-probe-wf_b949ad64-396.js"} to iterate without resending the script.)
> Run ID: wf_b949ad64-396
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/20894beb-8faf-40d8-bce8-715b0c184c7f/workflows/scripts/avatar-clone-ai-fatia0-viability-format-probe-wf_b949ad64-396.js", resumeFromRunId: "wf_b949ad64-396"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(00:52:19)*


## 🤖 Claude *(00:52:31)*

Probe **rodando em background** (run `wf_b949ad64-396`) — 6 frentes + verificação adversarial de 3 claims-chave + síntese. Eu sou notificado quando fechar.

**Onde estamos no Closed-Loop:**

| Etapa | Status |
|---|---|
| Deepsearch força-total → blueprint `00-deepsearch-blueprint.md` | ✅ no disco (421 linhas) |
| 4 decisões Sovereign gravadas no blueprint (OTD-AC-001/009/012 + gate) | ✅ feito |
| **Probe de viabilidade + formato (Fatia 0)** → `00b-fatia0-...md` + go/no-go | 🔄 rodando |
| Fechar frentes F1/F3/F4/F5/F6/F7 (ToS BYOK, fonemas PT, competidor, economics, LGPD biométrico, account-warming) | ⏳ gated no go/no-go |
| `/bok-scribe avatar-clone-ai` → sela MRD→SDD + Pattern Conformance | 🚪 BoK Gate |
| Construir peças (voz → identidade → script-RAG → talking-head → C2PA → reply X) → juntar no Autopilot | ⏳ pós-BoK |

**O que o probe me traz pra você decidir:** veredicto **go / go-híbrido / no-go**, a **postura** (100%-avatar vs híbrido rosto-real+avatar vs faceless), o diagnóstico honesto das suas contas [@uxnai](https://www.youtube.com/@uxnai/videos) e [@gabriel_mcorch](https://www.tiktok.com/@gabriel_mcorch), e o **formato-âncora** recomendado (seu EN-áudio+PT-legenda vs alternativas).

**Anotado pro próximo passo:** você apontou o **[Kanban](https://login.mcorch.com/dashboard/kanban)** e o **[Chat](https://login.mcorch.com/dashboard/chat)** como onde quer ver planos/pipelines/roadmaps em ação. Depois do go/no-go, eu **trago o roadmap das fatias + a cadência de 30 dias pra dentro do Kanban** (valor visível, não plumbing) — mas primeiro deixo o gate decidir se construímos 100%-avatar ou pivotamos pra híbrido, pra não encher o board com um plano que a viabilidade pode mudar.

Não toco em código enquanto o gate roda (Refusal Mode da BoK ativo). Te aviso assim que o relatório cair no disco. 🛰️

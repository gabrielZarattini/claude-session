# Implementar reshaper para posts nativos multiplataforma
**Date:** 2026-06-28 | **Session ID:** `2c25c853-bfbe-43d0-96c9-675282d65093`

---

## 👤 User *(02:12:44)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(02:12:44)*

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


## 🤖 Claude *(02:12:47)*


## 🤖 Claude *(02:12:48)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with parallel pre-flight checks.

## 🤖 Claude *(02:12:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7; echo \"---STATUS---\"; git status --short; echo \"---DIFFSTAT---\"; git diff HEAD --stat",
  "description": "Git history, status, and diff scope"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> f4ed255 docs(handoff): seal TikTok/YouTube E2E + Channel Format Intelligence (FR-CP-001)
> 296d62f docs(readme): v6.55.0 — Channel Format Intelligence + TikTok/YouTube provados E2E
> f7dd556 docs(bok): emenda channel-format-intelligence no post-engine (Closed-Loop)
> a446c36 feat(db): channel_profiles + pillar_atoms — engenharia reversa de formato (FR-CP-001)
> 96b4d9f feat(creative): botões Publicar TikTok + YouTube na Biblioteca de Assets
> def5d03 fix(ui): mensagem acionável ao conectar rede social (402 action hint)
> f5e092c fix(social): publish-social força SELF_ONLY no TikTok para cliente não-auditado
> ---STATUS---
> ---DIFFSTAT---
> ```

## 🤖 Claude *(02:12:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---MEGABRAIN---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat; echo; echo \"---BOK---\"; ls docs/bok/ 2>/dev/null; echo \"---HANDOFF-WC---\"; wc -l HANDOFF.md; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "Containers, Chroma health, BoK suites, HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 10 days (healthy)
> mcorch_claude_mem: Up 12 days (healthy)
> mcorch_chroma: Up 12 days (healthy)
> ---MEGABRAIN---
> mega-brain-dashboard: Up 12 days
> mega-brain-webhook: Up 12 days (healthy)
> mega-brain-daemon: Up 12 days (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1782612772626097187}
> ---BOK---
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
> ---HANDOFF-WC---
> 8530 HANDOFF.md
> ---SCRATCH---
> scratch has files
> ```

## 🤖 Claude *(02:12:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "timeout 180 npx tsc --noEmit 2>&1 | tail -20; echo \"EXIT:$?\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> EXIT:0
> ```

## 🤖 Claude *(02:12:58)*


## 🤖 Claude *(02:12:59)*

Pre-flight looks healthy. Now reading HANDOFF.md (read-from-end strategy) and context files.

## 🤖 Claude *(02:13:00)*


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
> 14	## Session Seal — TikTok/YouTube provados E2E + Channel Format Intelligence (engenharia reversa de formato · FR-CP-001) (2026-06-27)
> 15	
> 16	Diretiva Sovereign: *"vamos conectar as redes"* → *"go"* repetido + *"cada rede tem sua pegada... fazer bem feito antes de qualquer coisa"*. Operado sob o Closed-Loop: registro dos apps (Sovereign) → prova material E2E → deepsearch dos 8 canais → emenda BoK → código FR-CP-001 → seal. Tudo provado (Lei 1); nada declarado sem prova.
> 17	
> 18	**Arco 1 — TikTok + YouTube ao vivo (apps em review).** O Sovereign registrou os 3 apps de dev (TikTok Content Posting · Google OAuth + canal Brand · Pinterest Trial pendente). Eu provei cada integração headless e consertei o que quebrou contra a API real.
> 19	
> 20	| Action | Result |
> 21	|--------|--------|
> 22	| TikTok OAuth (sandbox) | ✅ token com `user.info.basic`+`video.publish`, conta @gabriel_mcorch — provado via `social-auth-init` 200 + `social_accounts` gravado |
> 23	| **TikTok Direct Post** | ✅ **`publish_id v_pub_file~v2-1.7656202273302792214` · PUBLISH_COMPLETE** após fix: cliente não-auditado só aceita `SELF_ONLY` (código caía em `FOLLOWER_OF_CREATOR`→403). Achado: post só publica se a CONTA estiver privada (`unaudited_client_can_only_post_to_private_accounts`) |
> 24	| **YouTube upload** | ✅ **`video_id 5Q6BQRUw85o`** via `videos.insert` resumable + **refresh_token presente** (access_type=offline). Achado: upload **público** funciona pré-audit neste projeto (doc diz forçar privado; não forçou) |
> 25	| UI publish | ✅ botões TikTok + YouTube (+Reel) na Biblioteca de Assets (`publishTo` generalizado) + erro acionável ao conectar (402 `action` hint) — build deployado, strings no bundle |
> 26	| TikTok audit / YouTube Gate B | ✅ submetidos (in review); demo gravado pelo Sovereign |
> 27	
> 28	**Arco 2 — Channel Format Intelligence (BoK + FR-CP-001).** Deepsearch dos 8 canais (workflow `wf_98eede6d-069`, 18 agentes, specs verificados adversarialmente) → emenda BoK `post-engine` → migration shipada.
> 29	
> 30	| Action | Result |
> 31	|--------|--------|
> 32	| Blueprint + emenda BoK | ✅ `docs/bok/post-engine/11-...blueprint.md` + `12-amendment-...md` (MR/BR/PR-CP + FR-CP-001..012 + OTD-CP-001..007 + Pattern Conformance 21 padrões [12 yes/5 deferred/4 n-a] + traceability zero-órfãos) + `00-index` |
> 33	| Migration `channel_profiles`+`pillar_atoms` | ✅ `20260627140000` aplicada (`Finished db push`) · `/security-review` limpo · RLS provada **G1** seed=16 · **G2** system visível · **G3** injeção→403 · **G4** write em system row=0-afetadas · **G5** integridade |
> 34	| Seed dos 8 canais | ✅ 16 linhas-sistema (`user_id NULL`) com specs verificados + `spec_source_urls` (Lei 1) |
> 35	
> 36	| Commit | Conteúdo |
> 37	|--------|----------|
> 38	| `f5e092c` | fix(social): publish-social SELF_ONLY TikTok não-auditado |
> 39	| `def5d03` | fix(ui): mensagem acionável ao conectar (402 action hint) |
> 40	| `96b4d9f` | feat(creative): botões TikTok + YouTube na Biblioteca de Assets |
> 41	| `a446c36` | feat(db): channel_profiles + pillar_atoms (FR-CP-001) |
> 42	| `f7dd556` | docs(bok): emenda channel-format-intelligence (Closed-Loop) |
> 43	| `296d62f` | docs(readme): v6.55.0 |
> 44	
> 45	**Mesh seal:** handoff node `df5c1ea5-7c8a-4bec-a6da-9d30a8f77e1b` (embedded 768d). Mesh **8974 nós**.
> 46	
> 47	**Próximo:** (Sovereign) esperar reviews (TikTok 2-6sem · YouTube Gate B ~dias-sem · Pinterest Trial ~1d útil) + conectar/provar Pinterest quando Trial sair. (código) **FR-CP-002 atomizer** + **FR-CP-003 reshaper** (o item de maior alavancagem — sem ele a espinha 9:16 vira 1 arquivo cross-postado = penalidade) + FR-CP-004/005 (16:9 + reframe 4:5/2:3/1.91:1) + FR-CP-006 coerção de formato API (IG JPEG / TikTok WebP / envelope 100MB). Endurecer read-back do `privacyStatus` do YouTube (voltou null).
> 48	
> 49	---
> 50	
> 51	## Session Seal — Conectar redes: TikTok + YouTube + Pinterest (brand persona Gabriel AI) — BoK gate + Vault app-creds + OAuth/publisher branches + UI (2026-06-27)
> 52	
> 53	Diretiva Sovereign: *"vamos conectar as redes — TikTok, YouTube, Pinterest"* + *"continue força total"*. Operado sob o Closed-Loop Protocol: pesquisa fundamentada → gate BoK → migration → edge code → UI → seal. Tudo provado materialmente (Lei 1); nada declarado sem prova.
> 54	
> 55	**Achado central:** ~90% da infra já existia (enum `social_platform` já tinha as 3 · `social_accounts` Vault · OAuth genérico `social-auth-init`/`-callback` · MESMO MP4 9:16). Net-new = credenciais de app per-user (Vault) + 3 pares de branches OAuth/publisher + UI. Os blockers duros são 100% **Sovereign-gated** (registrar 3 apps de dev + 3 audits — sem app não há `client_id`/`secret` → nenhum OAuth; sem audit o público é invisível: TikTok SELF_ONLY · YouTube forced-private · Pinterest sandbox).
> 56	
> 57	| Action | Result |
> 58	|--------|--------|
> 59	| Pesquisa fundamentada (workflow `wf_b5a35451`, 8 agentes, adversarial-verify) | ✅ 3 plataformas verificadas HIGH; blueprint `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md` + playbook `…/social-app-registration-playbook-2026-06-27.md` |
> 60	| PASSO 0 — gate BoK | ✅ `post-engine` `06`/`09-pattern-conformance`(21 padrões)/`10-amendment`(FR-PE-005..016) + 3 SOPs Lei 2 `docs/processes/{tiktok,youtube,pinterest}-publish-credential-resolution.md` |
> 61	| Migration `20260627120000_social_app_config` | ✅ aplicada+provada — coluna crua=UUID Vault `55caaf7b…` · masked view `••••` · decrypted view anon→**42501** · `/security-review` SAFE |
> 62	| Helper `supabase/functions/_shared/social-app-config.ts` | ✅ `resolveSocialAppCreds` per-user→env→**402** fail-closed (nunca chave compartilhada silenciosa) |
> 63	| Branches `social-auth-init`/`-callback`/`refresh-social-token`/`publish-social` + `auto-publish` video_url | ✅ `deno check` 8/8 · deployadas · **fail-closed provado LIVE (3×402)** |
> 64	| `autopilot-run` VIDEO_FLOW_PLATFORMS / FR-PE-013 | ⏸️ **DEFERIDO** — manter `['wordpress']`; adicionar youtube/tiktok/pinterest cobraria VIDEO_COST sem render (charge-without-value) até estender o enqueue-gate de `orchestrate-content`/`-step` |
> 65	| UI `useSocialAppConfig` + `SocialAppConfigCard` (Settings→Social) + 3 connect cards (`/dashboard/social`) | ✅ tsc 0 · build deployado (chunk `SettingsPage-CHgtU2cG.js` + env baked) · **browser-verified + Vision QA "high"** · 0 erro de console |
> 66	
> 67	| Commit | Conteúdo |
> 68	|--------|----------|
> 69	| `ea12afc` | docs(post-engine): BoK amendment + SOPs + blueprint |
> 70	| `c94bd75` | feat(db): social_app_config Vault-cifrada (FR-PE-005) |
> 71	| `25477a8` | feat(social): OAuth + publisher branches + helper fail-closed (FR-PE-006..016) |
> ```

## 🤖 Claude *(02:13:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8130,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8130	ContentLibraryPage monetization flow:
> 8131	  Card (text, body contains mercadolivre.com.br)
> 8132	    └── DropdownMenu → "Monetizar Links ML"
> 8133	          → handleMonetizeLinks(item):
> 8134	               match(ML_URL_RE) → unique URLs
> 8135	               for url of unique:
> 8136	                 POST process-affiliate-link → affiliate_url
> 8137	                 body.split(url).join(affiliate_url)
> 8138	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8139	          → Badge 💰 ML (emerald) exibido após monetização
> 8140	```
> 8141	
> 8142	---
> 8143	
> 8144	## Pending Actions (Commercial Launch)
> 8145	
> 8146	### CRITICAL — Must complete before first client
> 8147	
> 8148	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8149	
> 8150	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8151	
> 8152	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8153	
> 8154	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8155	
> 8156	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8157	
> 8158	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8159	
> 8160	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8161	
> 8162	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8163	
> 8164	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8165	
> 8166	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8167	
> 8168	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8169	
> 8170	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8171	   ```bash
> 8172	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8173	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8174	   ```
> 8175	
> 8176	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8177	
> 8178	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8179	
> 8180	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8181	
> 8182	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8183	
> 8184	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8185	
> 8186	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8187	
> 8188	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8189	
> 8190	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8191	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8192	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8193	
> 8194	### SOCIAL — Next steps
> 8195	
> 8196	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8197	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8198	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8199	
> 8200	### NON-CRITICAL
> 8201	
> 8202	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8203	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8204	- `browserslist` — ✅ updated (2026-04-26)
> 8205	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8206	
> 8207	### GITNEXUS MCP — Next steps
> 8208	
> 8209	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8210	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8211	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8212	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8213	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8214	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8215	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8216	
> 8217	### PHASE EPSILON — Next iterations
> 8218	
> 8219	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8220	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8221	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8222	
> 8223	### CORE — Next iterations
> 8224	
> 8225	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8226	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8227	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8228	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8229	
> 8230	### PHASE DELTA — Next iterations
> 8231	
> 8232	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8233	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8234	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8235	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8236	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8237	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8238	
> 8239	### USUÁRIO ZERO — Checklist de validação
> 8240	
> 8241	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8242	- ✅ Stripe sandbox secrets no vault
> 8243	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8244	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8245	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8246	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8247	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8248	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8249	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8250	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8251	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8252	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8253	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8254	
> 8255	---
> 8256	
> 8257	## Infrastructure
> 8258	
> 8259	| Service | Container | Port | Status |
> 8260	|---------|-----------|------|--------|
> 8261	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8262	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8263	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8264	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8265	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8266	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8267	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8268	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8269	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8270	
> 8271	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8272	
> 8273	```bash
> 8274	docker compose up -d
> 8275	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8276	```
> 8277	
> 8278	---
> 8279	
> 8280	## Security Model (Post-Go-Live)
> 8281	
> 8282	| Table | Isolation |
> 8283	|-------|-----------|
> 8284	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8285	| `mcorch_edges` | Same pattern |
> 8286	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8287	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8288	
> 8289	---
> 8290	
> 8291	## Billing Architecture
> 8292	
> 8293	| Decision | Value |
> 8294	|----------|-------|
> 8295	| Canonical billing ledger | `profiles.mco_balance` |
> 8296	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8297	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8298	| Orchestration cost | 10 mcoCoins/run |
> 8299	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8300	| Stripe | Sandbox keys active — swap to live before first client |
> 8301	
> 8302	---
> 8303	
> 8304	## GraphRAG State
> 8305	
> 8306	- **8973 total nodes** (verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8307	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8308	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8309	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8310	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8311	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8312	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8313	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8314	- HNSW cosine index operational
> 8315	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8316	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8317	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8318	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8319	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8320	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8321	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8322	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8323	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8324	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8325	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8326	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8327	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8328	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8329	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8330	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8331	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8332	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8333	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8334	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8335	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8336	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8337	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8338	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8339	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8340	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8341	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8342	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8343	
> 8344	### Embedding Model
> 8345	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8346	Schema: `vector(768)` — HNSW cosine index.
> 8347	
> 8348	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8349	Três camadas eliminam intervenção manual:
> 8350	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8351	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8352	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8353	
> 8354	### Comandos de manutenção da Mesh
> 8355	```bash
> 8356	# Verificar nós sem embedding (deveria retornar array vazio):
> 8357	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8358	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8359	
> 8360	# Backfill manual (Bun-native — requer .env):
> 8361	bun run scripts/backfill-embeddings.ts
> 8362	
> 8363	# Backfill de código-fonte nos nós AST:
> 8364	bun run scripts/backfill-node-content.ts
> 8365	
> 8366	# Re-sync AST completo:
> 8367	cd packages/gitnexus-core && npm run sync-mesh
> 8368	
> 8369	# Acompanhar re-ingesta pós-commit:
> 8370	tail -f /tmp/mcorch-ingest.log
> 8371	```
> 8372	
> 8373	---
> 8374	
> 8375	## Video Rescue Protocol
> 8376	
> 8377	When a video generation operation (Google Veo) times out or client disconnects:
> 8378	```bash
> 8379	# Via edge function (production):
> 8380	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8381	  -H "Authorization: Bearer <user_jwt>" \
> 8382	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8383	
> 8384	# Via local script (admin/debug):
> 8385	source .env && bun run rescue.ts <operation_id> <content_id>
> 8386	```
> 8387	
> 8388	---
> 8389	
> 8390	## Architecture Pillars
> 8391	
> 8392	| Layer | Implementation |
> 8393	|-------|---------------|
> 8394	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8395	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8396	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8397	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8398	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8399	
> 8400	---
> 8401	
> 8402	## Phase Delta — Architecture
> 8403	
> 8404	```
> 8405	OrchestrationPage (full-canvas, p-0)
> 8406	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8407	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8408	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8409	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8410	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8411	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8412	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8413	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8414	
> 8415	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8416	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8417	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8418	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8419	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8420	```
> 8421	
> 8422	### Canvas State Architecture (Hybrid)
> 8423	
> 8424	```
> 8425	User interaction → ReactFlow internal state (positions, drag)
> 8426	                         ↓ (debounced 600ms)
> 8427	                   localStorage (positions persist across refresh)
> 8428	                         ↑
> 8429	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8430	     ↓ (status changes sync to ReactFlow via useEffect)
> 8431	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8432	```
> 8433	
> 8434	## Key Files
> 8435	
> 8436	| Purpose | Path |
> 8437	|---------|------|
> 8438	| Architecture rules | `CLAUDE.md` |
> 8439	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8440	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8441	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8442	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8443	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8444	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8445	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8446	| **Node types** | `src/components/orchestrator/nodes/` |
> 8447	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8448	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8449	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8450	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8451	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8452	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8453	| Billing utilities | `src/lib/billing.ts` |
> 8454	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8455	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8456	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8457	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8458	| Video rescue (local) | `rescue.ts` |
> 8459	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8460	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8461	| Deploy harness | `scripts/harness-deploy.sh` |
> 8462	
> 8463	---
> 8464	
> 8465	## First Client Onboarding Checklist
> 8466	
> 8467	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8468	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8469	3. ~~Activate watchdog cron~~ ✅ Done
> 8470	4. ~~Deploy rescue-video function~~ ✅ Done
> 8471	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8472	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8473	7. Monitor `infra_health_logs` for first 24h.
> 8474	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8475	
> 8476	---
> 8477	
> 8478	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8479	
> 8480	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8481	
> 8482	| Action | Result |
> 8483	|--------|--------|
> 8484	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8485	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8486	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8487	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8488	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8489	
> 8490	| Commit | Conteúdo |
> 8491	|--------|----------|
> 8492	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8493	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8494	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8495	
> 8496	### Arquitetura Matrix Intelligence
> 8497	
> 8498	```
> 8499	ConstellationMatrix (Stabilized Engine)
> 8500	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8501	  └── NodeDetailsPanel (Tabbed Navigation)
> 8502	        ├── Tab Meta: Neighbor exploration + Net Context
> 8503	        ├── Tab Code: Source code preview (Supabase sync)
> 8504	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8505	
> 8506	useNodeIntelligence Hook:
> 8507	  - contentQuery: fetch nodes.content column
> 8508	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8509	  - state: isAnalyzing, analysisResult, progress
> 8510	```
> 8511	
> 8512	---
> 8513	
> 8514	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8515	
> 8516	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8517	
> 8518	| Action | Result |
> 8519	|--------|--------|
> 8520	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8521	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8522	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8523	
> 8524	**Output da análise (estruturado em pt-BR):**
> 8525	- Visão Geral — papel do módulo no sistema
> 8526	- Padrões Detectados — design patterns, antipatterns
> 8527	- Acoplamento & Dependências — análise In/Out-Degree
> 8528	- Recomendações — 1-3 ações priorizadas
> 8529	
> ```

## 🤖 Claude *(02:13:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"---SPRINT---\"; cat .claude/context/sprint-priorities.md 2>/dev/null | head -60",
  "description": "Scratch contents + sprint priorities"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (50.5KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/2c25c853-bfbe-43d0-96c9-675282d65093/tool-results/bpuhhaid8.txt
> 
> Preview (first 2KB):
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 27 23:06 ..
> ---SPRINT---
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

## 🤖 Claude *(02:13:07)*


## 🤖 Claude *(02:13:08)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Handson pickup",
  "summary": "Session pick-up \u2014 TikTok/YouTube E2E + Channel Format Intelligence sealed"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Handson pickup". Continue your current work.'}]
> ```

## 🤖 Claude *(02:13:10)*


## 🤖 Claude *(02:13:33)*

```
═══════════════════════════════════════════════════════════
  HANDSON — TikTok/YouTube E2E + Channel Format Intelligence (2026-06-27)
═══════════════════════════════════════════════════════════

🏁 ESTADO ATUAL
  Fase selada: TikTok/YouTube provados E2E + Channel Format Intelligence (FR-CP-001)
  Últimos commits:
    f4ed255 — docs(handoff): seal TikTok/YouTube E2E + Channel Format Intelligence
    296d62f — docs(readme): v6.55.0 — Channel Format Intelligence + TikTok/YouTube
    f7dd556 — docs(bok): emenda channel-format-intelligence no post-engine
    a446c36 — feat(db): channel_profiles + pillar_atoms (FR-CP-001)
    96b4d9f — feat(creative): botões Publicar TikTok + YouTube na Biblioteca

📂 MUDANÇAS PENDENTES
  Worktree limpo ✅ (scratch/ vazio também)

🏗️ INFRA  — tudo saudável ✅
  mcorch_chroma:     Up 12 days (healthy) — Chroma API v2: OK (heartbeat respondeu)
  mcorch_claude_mem: Up 12 days (healthy)
  mcorch_vision_mcp: Up 10 days (healthy)
  mega-brain-*:      daemon/webhook (healthy) · dashboard (up)

🧠 KNOWLEDGE MESH
  8974 nós · ~9070 arestas (fonte: HANDOFF GraphRAG State) · 100% embedded (768d HNSW)
  Último seal node: df5c1ea5 (handoff, embedded)

🔧 TYPESCRIPT
  Zero erros ✅ (tsc --noEmit exit 0)

📚 BoK SUITES — 24 suítes em docs/bok/ (todas as do roadmap ativo seladas)
  Relevante à fase atual: post-engine (emendado com channel-format-intelligence,
  FR-CP-001..012 + Pattern Conformance 21 padrões) ✅
  GATE: nenhum bloqueador — fase atual operou sob Closed-Loop completo.

📌 SPRINT
  Goal: Distribuição social autônoma operacional (LinkedIn live; TikTok/YouTube
        em review; Pinterest aguardando Trial)
  Top gap: FR-CP-002 atomizer + FR-CP-003 reshaper — sem o reshaper a espinha
           9:16 vira 1 arquivo cross-postado = penalidade de algoritmo

⚡ PRÓXIMOS PASSOS (prioridade)
  1. FR-CP-003 reshaper (MAIOR ALAVANCAGEM) — reformata por canal em vez de
     cross-postar o mesmo MP4. + FR-CP-002 atomizer (pilar→átomos por canal).
  2. FR-CP-004/005/006 — variantes 16:9, reframe 4:5/2:3/1.91:1, coerção de
     formato na API (IG JPEG / TikTok WebP / envelope 100MB).
  3. Endurecer read-back do privacyStatus do YouTube (voltou null no E2E).

  Trilhos Sovereign-gated (aguardam, não codáveis por mim):
    • Reviews: TikTok audit (2-6sem) · YouTube Gate B (~dias-sem) · Pinterest Trial (~1d)
    • Conectar/provar Pinterest quando o Trial sair.

⚠️ ALERTAS
  Nenhum alerta crítico ✅
  Nota: FR-PE-013 (video-cadence p/ YT/TikTok no autopilot) DEFERIDO de propósito
  — adicionar plataformas de vídeo cobraria VIDEO_COST sem render até estender
  o enqueue-gate. Não é bug; é decisão registrada.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

Contexto carregado. O sistema está limpo e saudável — worktree sem pendências, tsc zerado, mesh e containers de pé.

O ponto de maior alavancagem no roadmap é o **FR-CP-003 reshaper** (+ FR-CP-002 atomizer): a infra de Channel Format Intelligence está selada no banco (`channel_profiles` + `pillar_atoms`, 16 specs-sistema), mas sem o reshaper o vídeo 9:16 ainda é cross-postado idêntico em todos os canais — exatamente a penalidade que a fase atual mapeou.

Como quer seguir? Posso (a) atacar o **FR-CP-002/003** (atomizer + reshaper — o trabalho codável de maior valor agora), (b) endurecer o read-back do `privacyStatus` do YouTube, ou (c) outra direção.

## 👤 User *(02:19:44)*

ótimo vamos continuar e o proximo passo seria o reshaper (FR-CP-003): 1 ideia → posts nativos em todas as redes? Continue com força total para finalizar todo o mapeamento da distribuição social autônoma operacional.

## 🤖 Claude *(02:20:14)*


## 🤖 Claude *(02:20:17)*

The Sovereign wants full force on **FR-CP-003 reshaper** (1 ideia → posts nativos em todas as redes) and to finalize the autonomous social distribution mapping. This is squarely in the `post-engine` module whose BoK already carries the channel-format-intelligence amendment (FR-CP-001..012) — so the Closed-Loop gate is open. But per the protocol, that amendment is my **one and only Single Source of Truth**, so I'll read it carefully before any code.

Let me set up tracking and start by confirming the BoK contract + reading the load-bearing files myself, in parallel.

## 🤖 Claude *(02:20:18)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskCreate,TaskUpdate,TaskList",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskCreate'}, {'type': 'tool_reference', 'tool_name': 'TaskUpdate'}, {'type': 'tool_reference', 'tool_name': 'TaskList'}]
> ```

## 🤖 Claude *(02:20:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== post-engine BoK dir ===\"; ls -la docs/bok/post-engine/; echo; echo \"=== migration FR-CP-001 ===\"; ls -la supabase/migrations/ | grep -E \"2026062714|2026062712\" ",
  "description": "List post-engine BoK docs + FR-CP migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === post-engine BoK dir ===
> total 140
> drwxrwxr-x  2 gcrUX  gcrUX   4096 Jun 27 22:45 .
> drwxrwxr-x 25 gcrUX  gcrUX   4096 Jun 26 19:50 ..
> -rw-rw-r--  1 ubuntu ubuntu  4896 Jun 27 22:45 00-index.md
> -rw-r--r--  1 gcrUX  gcrUX   4120 Jun  6 17:11 01-mrd.md
> -rw-r--r--  1 gcrUX  gcrUX   2825 Jun  6 17:11 02-brd.md
> -rw-r--r--  1 gcrUX  gcrUX   2630 Jun  6 17:11 03-prd.md
> -rw-r--r--  1 gcrUX  gcrUX   2439 Jun  6 17:11 04-frd.md
> -rw-r--r--  1 gcrUX  gcrUX   2327 Jun  6 17:11 05-sdd.md
> -rw-r--r--  1 ubuntu ubuntu 11171 Jun 27 12:32 06-data-model.md
> -rw-r--r--  1 gcrUX  gcrUX   1830 Jun  6 17:12 07-process-flow.md
> -rw-r--r--  1 gcrUX  gcrUX   1973 Jun  6 17:12 08-quality-metrics.md
> -rw-rw-r--  1 ubuntu ubuntu 12159 Jun 27 12:33 09-pattern-conformance.md
> -rw-rw-r--  1 ubuntu ubuntu 25136 Jun 27 12:35 10-amendment-social-connect-tiktok-youtube-pinterest.md
> -rw-rw-r--  1 ubuntu ubuntu 16618 Jun 27 22:32 11-channel-format-intelligence-blueprint.md
> -rw-rw-r--  1 ubuntu ubuntu 17955 Jun 27 22:44 12-amendment-channel-format-intelligence.md
> 
> === migration FR-CP-001 ===
> -rw-rw-r-- 1 ubuntu ubuntu 11453 Jun 27 12:44 20260627120000_social_app_config.sql
> -rw-rw-r-- 1 ubuntu ubuntu 20751 Jun 27 22:53 20260627140000_channel_profiles.sql
> ```

## 🤖 Claude *(02:20:24)*


## 🤖 Claude *(02:20:25)*

The gate is open — the channel-format-intelligence amendment is sealed. Let me read the load-bearing BoK docs (my Single Source of Truth) and the schema migration in full.

## 🤖 Claude *(02:20:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/12-amendment-channel-format-intelligence.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Amendment — Channel Format Intelligence (Engenharia Reversa de Formato · Fonte da Verdade)
> 2	
> 3	| Campo | Valor |
> 4	|-------|-------|
> 5	| **Módulo** | `post-engine` — emenda "Channel Format Intelligence" (camada de reshape pré-publicação) |
> 6	| **Lineage** | Semente: [`11-channel-format-intelligence-blueprint.md`](11-channel-format-intelligence-blueprint.md) (deepsearch `wf_98eede6d-069`, 8 canais × research+verify adversarial). Reusa `viral-autopilot` (cadência) + `orchestrate-content` (pilar) + HyperFrames (render) + emenda social-connect (publishers, doc 10). |
> 7	| **ORO** | Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (Gabriel) · Owner = Sovereign (blast radius = FRs construídas sobre spec errado → upload quebra silenciosamente / penalidade de cross-post) |
> 8	| **Traça** | MR-CP → BR-CP → PR-CP → FR-CP-001..012 · OTD-CP-001..007 · Pattern Conformance (§10) |
> 9	| **Gate** | Emenda BoK ANTES de código (Closed-Loop). SDD desta emenda **carrega a Pattern Conformance Declaration** (§10, Step 3.5 — ≥3 padrões materiais). Código liberado só após review desta emenda. |
> 10	| **Versão** | emenda channel-format-intelligence v1.0 — 2026-06-27 |
> 11	
> 12	---
> 13	
> 14	## 1. Tese e veredito
> 15	
> 16	> **"Os dados mandam."** Uma ideia-pilar → o motor lê o dicionário de dados `channel_profiles` → reshapa o pilar no **formato, voz e cadência** corretos de cada canal. **Zero branch por canal**: a regra vive em dados. Formaliza o GaryVee reverse-pyramid + Content Atomization sobre o stack `viral-autopilot` + HyperFrames.
> 17	
> 18	**Veredito (confirmado contra docs oficiais + código vivo):**
> 19	- **A espinha já existe.** O master **9:16 1080×1920 H.264 MP4** (HyperFrames) é nativo em **7 superfícies** (IG Reels · FB Reels · TikTok · YT Shorts · X · Pinterest Video Pin · IG Story). ⇒ *um render serve sete.*
> 20	- **~90% reusa.** Cadência (`autopilot_plans`), pilar (`orchestrate-content`), creds Vault (`social_accounts`), 5 publishers vivos + 3 em review, RLS/tenancy, `creative_metrics`.
> 21	- **O net-new é o acabamento por canal** — o reshaper que lê `transform_recipe`, mais os GAPs de formato (16:9, reframe de imagem, coerção de formato API, fan-out de variante nativa, PDF carousel, Pinterest-SEO).
> 22	
> 23	A matriz de formato completa e verificada (vídeo/imagem/texto/voz/cadência/descoberta dos 8 canais) está em [`11-...blueprint.md` §1](11-channel-format-intelligence-blueprint.md). Esta emenda referencia, não duplica.
> 24	
> 25	---
> 26	
> 27	## 2. Armadilhas de quebra silenciosa (a verificação adversarial pegou — viram regra de dados)
> 28	
> 29	Estas **DEVEM** ser codificadas no `channel_profiles` (senão o publish falha sem erro óbvio):
> 30	
> 31	1. **Formato de imagem API ≠ in-app.** Publicação via API: **IG = só JPEG · TikTok = WebP/JPEG (sem PNG)**. Nosso default PNG (canvas/Gemini) quebra o publish via API. → `channel_profiles.image.format` + coerção (FR-CP-006).
> 32	2. **IG Reels via API = teto 100 MB / VBR ≤5 Mbps** (não os 4 GB do in-app). O HyperFrames deve renderizar dentro desse envelope. → `channel_profiles.video.max_file_mb`/`max_vbr_mbps` por `publish_path` (FR-CP-006, OTD-CP-002).
> 33	3. **TikTok foto: título ≤90 + desc ≤4.000** (≠ caption de vídeo 2.200 runes). Campo único trunca errado. → `channel_profiles.text` por `surface` (FR-CP-001).
> 34	4. **API vs in-app gate.** TikTok in-app ~72 MB Android / 287 MB iOS; só a Content Posting **API** dá 4 GB. O `publish_path` decide qual teto vale. → coluna `publish_path` (OTD-CP-002).
> 35	5. **Penalidade de cross-post ~40-60% de alcance** se o mesmo MP4 é re-postado idêntico. Master limpo é asset; variante nativa por canal é obrigatória. → FR-CP-007.
> 36	
> 37	---
> 38	
> 39	## 3. MRD delta (Market Requirements)
> 40	
> 41	| ID | Market Requirement |
> 42	|----|--------------------|
> 43	| **MR-CP-001** | Uma persona de marca (Gabriel AI/CCIO) precisa de presença **nativa** em 8 canais a partir de **uma** ideia-pilar — sem produzir 8× o conteúdo manualmente. |
> 44	| **MR-CP-002** | Cada canal tem "pegada" própria (formato de asset, tom de voz, cadência, mecânica de descoberta); conteúdo genérico cross-postado é penalizado por algoritmo (−40-60% alcance) e por percepção. |
> 45	| **MR-CP-003** | Specs de plataforma mudam; o sistema deve tratar formato como **dado versionado e fundamentado** (com fonte), não constante hardcoded — para sobreviver ao drift sem reescrever código. |
> 46	
> 47	## 4. BRD delta (Business Requirements)
> 48	
> 49	| ID | Business Requirement | Deriva de |
> 50	|----|----------------------|-----------|
> 51	| **BR-CP-001** | Maximizar alcance/engajamento por unidade de esforço: 1 pilar → N posts nativos, cada um no formato que o canal premia. | MR-CP-001/002 |
> 52	| **BR-CP-002** | Evitar penalidade de cross-post: cada superfície recebe **variante nativa** (hook/caption/safe-zone/CTA próprios), nunca o arquivo idêntico. | MR-CP-002 |
> 53	| **BR-CP-003** | Reuso máximo de custo: a espinha 9:16 alimenta 7 canais sem re-render; só onde diverge (16:9, 2:3, 1.91:1) há custo adicional. | MR-CP-001 |
> 54	| **BR-CP-004** | Conformidade de upload garantida: nenhum publish deve falhar por formato/spec errado (gate de dados). | MR-CP-003 |
> 55	| **BR-CP-005** | Cada regra de spec carrega sua fonte (URL oficial) — auditável (Lei 1) e re-verificável. | MR-CP-003 |
> 56	
> 57	## 5. PRD delta (Product Requirements)
> 58	
> 59	| ID | Product Requirement |
> 60	|----|--------------------|
> 61	| **PR-CP-001** | O Sovereign (e, no futuro, cada tenant) vê/edita o perfil de cada canal (formato, voz, cadência) como dado — linhas-sistema default + override per-user. |
> 62	| **PR-CP-002** | Ao gerar um pilar, o motor produz automaticamente as variantes nativas de cada canal ativo e as agenda pela cadência do canal. |
> 63	| **PR-CP-003** | O conteúdo-pilar tem um **lar canônico** (artigo WordPress / vídeo YouTube long) e cada micro-post linka de volta a ele (funil). |
> 64	| **PR-CP-004** | Todo criativo gerado passa pelo gate de Vision-QA antes de publicar (olho criativo — diretiva vigente). |
> 65	
> 66	---
> 67	
> 68	## 6. FRD delta — Functional Requirements (FR-CP-001..012)
> 69	
> 70	| FR | Requisito | Reusa | Net-new |
> 71	|----|-----------|-------|---------|
> 72	| **FR-CP-001** | Schema `channel_profiles` + `pillar_atoms` (§7.2) + seed de linhas-sistema (`user_id NULL`) dos 8 canais com specs verificados + `spec_source_urls`. | RLS/Vault/tenancy | tabelas + seed |
> 73	| **FR-CP-002** | **Atomizer**: nó upstream que decompõe o pilar em `pillar_atoms` (hook, key_points[], stat, quote, cta, pillar_url). | orchestrate-content | prompt de atomização |
> 74	| **FR-CP-003** | **Reshaper por canal**: edge fn que lê `channel_profiles.transform_recipe` + `pillar_atoms` e produz o asset nativo, aplicando os constraints da linha como gate. | HyperFrames, image engine, text gen | interpretador da recipe |
> 75	| **FR-CP-004** | **Render 16:9** no HyperFrames (YouTube long-form) — template horizontal determinístico. | render-core | template 16:9 |
> 76	| **FR-CP-005** | **Reframe de imagem** 4:5 (1080×1350 feed) · 2:3 (1000×1500 Pinterest) · 1.91:1 (1200×630 og:image/link-card) com safe-zone. | canvas/Gemini | reframe + safe-zone |
> 77	| **FR-CP-006** | **Coerção de formato API** por `publish_path`: IG→JPEG, TikTok→WebP/JPEG, envelope IG Reels (≤100 MB / VBR ≤5 Mbps), split de caption TikTok-foto (90+4000). | publish branches (doc 10) | gate de formato |
> 78	| **FR-CP-007** | **Fan-out de variante nativa** (anti cross-post): cada superfície ativa recebe hook/caption/safe-zone/CTA próprios derivados do mesmo átomo — nunca o arquivo idêntico. | — | emissor de variantes |
> 79	| **FR-CP-008** | **Modo Pinterest-SEO** de texto: título+descrição+tags keyword-rich (não caption de feed). | text gen | prompt SEO |
> 80	| **FR-CP-009** | **PDF carousel / multi-página** (LinkedIn ~7% maior engajamento; também TikTok-foto/IG-carousel/Pinterest Idea Pin via átomos→slides). | — | doc/slide renderer |
> 81	| **FR-CP-010** | **Scheduler por cadência**: liga `channel_profiles.cadence` (+ `priority`) ao `autopilot_plans` — drip per-canal. | autopilot cron | binding |
> 82	| **FR-CP-011** | **KPI hook-rate** (watch-past-3s) + alcance por canal em `creative_metrics`. | creative_metrics | métrica |
> 83	| **FR-CP-012** | **Auto-segmentação** 1 fonte longa → N shorts distintos (modelo Hormozi). *(slice posterior)* | HyperFrames | segmenter |
> 84	
> 85	**NFR (herdados + novos):** NFR-PE-001 sucesso ≥90% (por canal, falha isolada) · **NFR-CP-001** nenhum publish quebra por spec (gate de dados) · **NFR-CP-002** spec carrega fonte+confiança (re-verificável) · NFR-PE-004 tokens só em Vault.
> 86	
> 87	---
> 88	
> 89	## 7. SDD delta (System Design)
> 90	
> 91	### 7.1 Arquitetura (fluxo data-driven, zero branch por canal)
> 92	
> 93	```
> 94	ideia-pilar
> 95	  → orchestrate-content (existente)            ── gera o pilar (artigo + master 9:16 + imagens)
> 96	  → [NOVO] atomizer node → pillar_atoms        ── FR-CP-002
> 97	  → para cada channel_profiles row WHERE is_active:
> 98	       reshaper edge fn (FR-CP-003)
> 99	         lê row.transform_recipe + pillar_atoms
> 100	         → deriva o asset (reframe / re-export / atoms→carousel / seo_text)  FR-CP-004/005/008/009
> 101	         → aplica constraints da row como GATE (formato/tamanho/texto)        FR-CP-006
> 102	         → emite variante NATIVA (hook/cta/safe-zone próprios)                FR-CP-007
> 103	         → Vision-QA gate (PR-CP-004)
> 104	         → publica via row.publish_path  (publishers da doc 10)
> 105	  → autopilot scheduler dripa por row.cadence + row.priority                  FR-CP-010
> 106	  → creative_metrics ← hook-rate + alcance por canal                          FR-CP-011
> 107	```
> 108	
> 109	**Princípio:** o reshaper é o **único** lugar que toca formato; tudo que ele precisa saber vem da linha de dados. Adicionar/ajustar um canal = editar uma linha, não código (a skill de engenharia reversa).
> 110	
> 111	### 7.2 Data Model (autoritativo — ver shapes JSONB no blueprint §3)
> 112	
> 113	Duas tabelas (Supabase, RLS default-deny, `search_path=''`):
> 114	- **`channel_profiles`** — dicionário de regras. PK `id`; `UNIQUE(user_id, channel, surface)`; `user_id NULL` = linha-sistema (visível a todos os tenants) + override per-user. Colunas: `channel`, `surface`, `is_active`, `priority`, `video jsonb`, `image jsonb`, `text jsonb`, `publish_path`, `voice_prompt_seed`, `cadence jsonb`, `discovery jsonb`, `transform_recipe jsonb`, `confidence`, `spec_source_urls text[]`. RLS SELECT `user_id IS NULL OR user_id = auth.uid()`; write own.
> 115	- **`pillar_atoms`** — pilar atomizado. `user_id` (RLS own), `pillar_run_id` (liga ao ciclo orchestrate/autopilot), `hook`, `key_points jsonb`, `stat`, `quote`, `cta`, `pillar_url`.
> 116	
> 117	`creative_metrics` ganha `hook_rate` (FR-CP-011). `06-data-model.md` a reconciliar com as 2 tabelas novas.
> 118	
> 119	### 7.3 Constantes de integração (cravar — fonte: blueprint §1, verificado)
> 120	- Espinha: `9:16 1080×1920 H.264/AAC MP4`.
> 121	- Divergências obrigatórias: YouTube long `16:9 1920×1080`; Pinterest `2:3 1000×1500`; link-card/og:image `1.91:1 1200×630`; feed image `4:5 1080×1350`; YT thumb `16:9 1280×720`.
> 122	- Envelope IG Reels API: `≤100 MB`, `VBR ≤5 Mbps`, `moov atom front`, `closed GOP`, `4:2:0`, áudio AAC 128 kbps.
> 123	- Formato API: IG `JPEG`; TikTok `WebP/JPEG`.
> 124	
> 125	### 7.4 Integração com a doutrina (gate Step 3.5)
> 126	Esta camada implementa materialmente Planning (atomização), Tool Use (render/reframe/publish), Routing/Parallelization (fan-out), Resource-Aware (espinha 1→7). Declaração completa em §10.
> 127	
> 128	---
> 129	
> 130	## 8. OTDs (Open Technical Decisions)
> 131	
> 132	| OTD | Decisão / risco |
> 133	|-----|-----------------|
> 134	| **OTD-CP-001** | Spec drift — linhas carregam `spec_source_urls`+`confidence`; cadência de re-verificação trimestral (workflow deepsearch reexecutável). |
> 135	| **OTD-CP-002** | Gate API-path vs in-app — `publish_path` governa o teto (IG 100 MB API vs 4 GB in-app; TikTok idem). |
> 136	| **OTD-CP-003** | Pinterest descrição 800 (campo) vs ≤500 (best-practice) — soft-cap 500, hard 800. |
> 137	| **OTD-CP-004** | Profundidade da mitigação de cross-post — variante nativa completa (áudio/efeitos) vs mínima (safe-zone+CTA). HyperFrames é determinístico ⇒ sem trending-audio ainda (GAP conhecido). |
> 138	| **OTD-CP-005** | LinkedIn 9:16 cru vs reframe-para-4:5 (9:16 sobe mas fica com padding branco no feed). |
> 139	| **OTD-CP-006** | Multi-tenant: linhas-sistema (`user_id NULL`) como default + override per-user (espelha tenancy de `mcorch_nodes`). |
> 140	| **OTD-CP-007** | Reflection/RAG: wirar Vision-QA como crítico do output do reshaper + RAG sobre posts vencedores p/ informar `voice_prompt_seed` — hoje seed estático + Vision-QA é regra comportamental. Liga ao loop OTD-AG-002. |
> 141	
> 142	---
> 143	
> 144	## 9. Quality Metrics delta
> 145	
> 146	| KPI | Meta |
> 147	|-----|------|
> 148	| **KPI-CP-001** | % de canais ativos publicados a partir de 1 pilar = 100% dos `is_active`. |
> 149	| **KPI-CP-002** | Hook-rate (watch-past-3s) por canal — tendência ↑ (FR-CP-011). |
> 150	| **KPI-CP-003** | Zero publish falho por formato/spec (NFR-CP-001). |
> 151	| **KPI-CP-004** | Reuso de render: ≥7 canais servidos por master 9:16 (BR-CP-003). |
> 152	| **KPI-CP-005** | Zero variante idêntica cross-postada (anti-penalidade, BR-CP-002). |
> 153	
> 154	---
> 155	
> 156	## 10. Pattern Conformance Declaration (os 21 padrões — `docs/architecture/agentic-vision.md`)
> 157	
> 158	> Declaração honesta (Step 3.5): nenhum `yes` sem FR/artefato; nenhum `deferred` sem OTD; nenhum `n-a` sem razão.
> 159	
> 160	| # | Pattern | Implemented? | How / Why-deferred |
> 161	|---|---------|--------------|--------------------|
> 162	| 1 | Prompt Chaining | **yes** | Cadeia pilar→átomos→voz/caption por canal (FR-CP-002→003); reusa o chaining do orchestrate-content. |
> 163	| 2 | Routing | **yes** | O motor roteia o pilar para N reshapers conforme `channel_profiles` ativos + escolhe o gate por `publish_path` (FR-CP-003/006). |
> 164	| 3 | Parallelization | **yes** | Fan-out: reshape+publish em N canais em paralelo a partir de um master (FR-CP-007). |
> 165	| 4 | Reflection | deferred | Laço generator-critic sobre a variante (caption cabe no tom? reframe respeita safe-zone?) via Vision-QA — hoje regra comportamental, wiring é **OTD-CP-007**. |
> 166	| 5 | Tool Use | **yes** | HyperFrames (render 9:16/16:9), reframe de imagem (canvas/Gemini), FFmpeg, APIs de publish (FR-CP-003/004/005/006). |
> 167	| 6 | Planning | **yes** | Atomizer + `transform_recipe` = o plano: decompõe o pilar em planos de asset por canal (FR-CP-002/003). |
> 168	| 7 | Multi-Agent | n-a | Pipeline determinístico de transformação dentro do motor; o coletivo de agentes (Pantheon/autopilot) é outra camada, não esta. |
> 169	| 8 | Memory Management | **yes** | `channel_profiles` + seal na Knowledge Mesh; `spec_source_urls`; o blueprint é puxado da malha (FR-CP-001). |
> 170	| 9 | Learning & Adaptation | deferred | Performance por canal (hook-rate/alcance) deve realimentar `transform_recipe`/cadência — sinal vem de FR-CP-011, o loop é **OTD-AG-002 / OTD-CP-007**. Marcar `yes` fabricaria o elo recursivo ainda manual. |
> 171	| 10 | Model Context Protocol | n-a | Esta camada não expõe nem consome MCP (o Vision MCP é módulo separado). |
> 172	| 11 | Goal Setting & Monitoring | **yes** | Metas de cadência por canal + KPI-CP-001..005 monitorados (FR-CP-010/011). |
> 173	| 12 | Exception Handling & Recovery | **yes** | Falha de um canal é **isolada** (fail-open por superfície) + telemetria `infra_health_logs` (espelha o pulse de publish-social) (FR-CP-006/007). |
> 174	| 13 | Human-in-the-Loop | **yes** | Sovereign aprova `voice_prompt_seed`/cadência + gate Vision-QA (PR-CP-004) + publish público gated por audit; override per-user (FR-CP-001). |
> 175	| 14 | Knowledge Retrieval (RAG) | deferred | `voice_prompt_seed` é estático hoje; RAG sobre posts vencedores p/ informar voz = **OTD-CP-007**. |
> 176	| 15 | Inter-Agent Communication (A2A) | n-a | Sem troca de mensagens entre agentes nesta pipeline. |
> 177	| 16 | Resource-Aware Optimization | **yes** | A espinha **1 render → 7 canais** É otimização de recurso; envelope API evita re-encode desperdiçado; custo só onde diverge (BR-CP-003 · FR-CP-003/004). |
> 178	| 17 | Reasoning Techniques | n-a | Transformações determinísticas + geração LLM single-pass; sem CoT/ToT explícito. |
> 179	| 18 | Guardrails / Safety | **yes** | Gate de formato (constraints da linha) impede upload inválido; anti cross-post (FR-CP-007); RLS tenancy; `spec_source_urls` (Lei 1); sentinel pt-BR herdado p/ títulos de trend. |
> 180	| 19 | Evaluation & Monitoring | **yes** | Métricas por canal (creative_metrics + hook-rate) + re-verify de spec (OTD-CP-001) + Vision-QA (FR-CP-011). |
> 181	| 20 | Prioritization | **yes** | `channel_profiles.priority` + cadência ordenam o scheduler; herda ε-greedy budget do autopilot (FR-CP-010). |
> 182	| 21 | Exploration & Discovery | deferred | A/B de hook/formato por canal estende `ab_variants` do autopilot — slice posterior (OTD-CP-004 / FR-VA ab). |
> 183	
> 184	**Resumo:** 12 `yes` · 5 `deferred` (cada um com OTD) · 4 `n-a` (com razão). Padrão dominante: **Resource-Aware + Parallelization + Planning** (a essência da engenharia reversa: um pilar, N variantes nativas, custo mínimo).
> 185	
> 186	---
> 187	
> 188	## 11. Traceability (MR → BR → PR → FR)
> 189	
> 190	| MR | BR | PR | FR |
> 191	|----|----|----|----|
> 192	| MR-CP-001 | BR-CP-001/003 | PR-CP-002 | FR-CP-002/003/004/005/010 |
> 193	| MR-CP-002 | BR-CP-002 | PR-CP-002/003 | FR-CP-007/008/009 |
> 194	| MR-CP-003 | BR-CP-004/005 | PR-CP-001 | FR-CP-001/006/011 |
> 195	
> 196	Zero órfãos: 3 MR → 5 BR → 4 PR → 12 FR, todas rastreadas.
> 197	
> 198	---
> 199	
> 200	## 12. Fontes (Lei 1)
> 201	
> 202	Specs verificados (verbatim, upload-gate): blueprint §1 + URLs em [`11-...blueprint.md`](11-channel-format-intelligence-blueprint.md) (LinkedIn a1311816 · Meta IG content-publishing · FB Reels API · X help videos · TikTok media-transfer-guide + photo-post · YouTube 71673/10059070 · Pinterest review-pin-specs · WordPress VideoPress). Frameworks: GaryVee reverse-pyramid · Content Atomization (Aprimo) · hook-body-CTA · cross-post penalty · cadence (Buffer). Pesquisa: workflow `wf_98eede6d-069` (18 agentes, 311 buscas). Doutrina: `docs/architecture/agentic-vision.md` (21 padrões).
> 203	
> ```

## 🤖 Claude *(02:20:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260627140000_channel_profiles.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: channel_profiles + pillar_atoms — Channel Format Intelligence (FR-CP-001)
> 2	-- ─────────────────────────────────────────────────────────────────────────────
> 3	-- BoK SSOT: docs/bok/post-engine/12-amendment-channel-format-intelligence.md (FR-CP-001, §7.2 data model)
> 4	--           + 11-channel-format-intelligence-blueprint.md (verified spec matrix, deepsearch wf_98eede6d-069).
> 5	-- Thesis: "data dictates the rules" — one pillar idea is reshaped per channel by reading these rows; NO
> 6	-- per-channel code branch. channel_profiles = the rule dictionary; pillar_atoms = the atomized pillar each
> 7	-- reshaper reads. No secrets here (RLS only, no Vault).
> 8	--
> 9	-- Tenancy (mirrors mcorch_nodes 20260425210000): channel_profiles rows with user_id IS NULL are SYSTEM
> 10	-- defaults visible to ALL tenants; a tenant may add/override their OWN rows (user_id = auth.uid()) but can
> 11	-- NEVER read/write another tenant's rows nor mutate the system rows (those are service_role-managed).
> 12	-- pillar_atoms is strictly per-user own.
> 13	--
> 14	-- Security posture: HARDENS (adds RLS-isolated tables, default-deny, no SECURITY DEFINER reachable by clients).
> 15	-- MANDATORY /security-review before commit (FMEA-011 cross-tenant leak class).
> 16	
> 17	-- ─────────────────────────────────────────────────────────────────────────────
> 18	-- 1. channel_profiles — the per-channel rule dictionary
> 19	-- ─────────────────────────────────────────────────────────────────────────────
> 20	CREATE TABLE IF NOT EXISTS public.channel_profiles (
> 21	    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 22	    user_id           UUID REFERENCES auth.users(id) ON DELETE CASCADE,   -- NULL = system default (all tenants)
> 23	    channel           TEXT NOT NULL,
> 24	    surface           TEXT NOT NULL,
> 25	    is_active         BOOLEAN NOT NULL DEFAULT TRUE,
> 26	    priority          INT NOT NULL DEFAULT 100,
> 27	    video             JSONB,    -- {aspect,width,height,duration_s{min,max,sweet},max_file_mb,container,vcodec,acodec,max_vbr_mbps,fps,muxing,safe_zone}
> 28	    image             JSONB,    -- {aspect,width,height,format,max_mb,notes}
> 29	    "text"            JSONB,    -- {caption_max|title_max+desc_max,unit,hashtags}
> 30	    publish_path      TEXT,     -- governs WHICH size/format gate applies (api vs in-app)
> 31	    voice_prompt_seed TEXT NOT NULL DEFAULT '',
> 32	    cadence           JSONB,    -- {target_per:day|week|month,count_min,count_max,note}
> 33	    discovery         JSONB,    -- {primary,signals[],hashtag_policy,keyword_seo:bool}
> 34	    transform_recipe  JSONB NOT NULL DEFAULT '{}'::jsonb,
> 35	    confidence        TEXT NOT NULL DEFAULT 'high',
> 36	    spec_source_urls  TEXT[] NOT NULL DEFAULT '{}',
> 37	    created_at        TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
> 38	    updated_at        TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
> 39	    CONSTRAINT channel_profiles_channel_chk CHECK (channel IN
> 40	        ('linkedin','instagram','facebook','twitter_x','tiktok','youtube','pinterest','wordpress')),
> 41	    CONSTRAINT channel_profiles_confidence_chk CHECK (confidence IN ('high','medium','uncertain')),
> 42	    -- one row per (tenant, channel, surface); system rows share the NULL-user namespace
> 43	    CONSTRAINT channel_profiles_unique_user_channel_surface UNIQUE (user_id, channel, surface)
> 44	);
> 45	
> 46	ALTER TABLE public.channel_profiles ENABLE ROW LEVEL SECURITY;
> 47	
> 48	-- SELECT: system rows (user_id IS NULL) are visible to everyone authenticated + own rows.
> 49	CREATE POLICY "channel_profiles read system or own" ON public.channel_profiles
> 50	    FOR SELECT USING (user_id IS NULL OR auth.uid() = user_id);
> 51	-- WRITE: a tenant may only create/modify/delete its OWN rows. System rows (NULL) are service_role-only
> 52	-- (service_role bypasses RLS). WITH CHECK forbids inserting a NULL-user row or spoofing another user_id.
> 53	CREATE POLICY "channel_profiles insert own" ON public.channel_profiles
> 54	    FOR INSERT WITH CHECK (auth.uid() = user_id);
> 55	CREATE POLICY "channel_profiles update own" ON public.channel_profiles
> 56	    FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 57	CREATE POLICY "channel_profiles delete own" ON public.channel_profiles
> 58	    FOR DELETE USING (auth.uid() = user_id);
> 59	
> 60	CREATE TRIGGER tr_update_channel_profiles_updated_at
> 61	    BEFORE UPDATE ON public.channel_profiles
> 62	    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 63	
> 64	CREATE INDEX IF NOT EXISTS idx_channel_profiles_channel_surface ON public.channel_profiles (channel, surface);
> 65	CREATE INDEX IF NOT EXISTS idx_channel_profiles_user ON public.channel_profiles (user_id);
> 66	CREATE INDEX IF NOT EXISTS idx_channel_profiles_active ON public.channel_profiles (is_active) WHERE is_active;
> 67	
> 68	-- UNIQUE(user_id, channel, surface) treats NULL user_id as distinct (Postgres), so system rows could
> 69	-- duplicate per (channel, surface). Enforce single system row per surface explicitly (also makes re-seed safe).
> 70	CREATE UNIQUE INDEX IF NOT EXISTS uq_channel_profiles_system_channel_surface
> 71	    ON public.channel_profiles (channel, surface) WHERE user_id IS NULL;
> 72	
> 73	-- ─────────────────────────────────────────────────────────────────────────────
> 74	-- 2. pillar_atoms — the atomized pillar (per-user own)
> 75	-- ─────────────────────────────────────────────────────────────────────────────
> 76	CREATE TABLE IF NOT EXISTS public.pillar_atoms (
> 77	    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 78	    user_id       UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 79	    pillar_run_id UUID,                                    -- links to orchestrate-content / autopilot cycle
> 80	    hook          TEXT,
> 81	    key_points    JSONB NOT NULL DEFAULT '[]'::jsonb,
> 82	    stat          TEXT,
> 83	    quote         TEXT,
> 84	    cta           TEXT,
> 85	    pillar_url    TEXT,                                    -- canonical home each micro-post links back to
> 86	    created_at    TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
> 87	);
> 88	
> 89	ALTER TABLE public.pillar_atoms ENABLE ROW LEVEL SECURITY;
> 90	
> 91	CREATE POLICY "pillar_atoms own" ON public.pillar_atoms
> 92	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 93	
> 94	CREATE INDEX IF NOT EXISTS idx_pillar_atoms_user ON public.pillar_atoms (user_id);
> 95	CREATE INDEX IF NOT EXISTS idx_pillar_atoms_run ON public.pillar_atoms (pillar_run_id);
> 96	
> 97	-- ─────────────────────────────────────────────────────────────────────────────
> 98	-- 3. SEED — system rows (user_id NULL) for the 8 channels, VERIFIED specs (blueprint §1)
> 99	--    Every row carries spec_source_urls (Law 1) + confidence. Persona voice = Gabriel AI / CCIO (brand-first).
> 100	-- ─────────────────────────────────────────────────────────────────────────────
> 101	-- ── THE 9:16 SPINE (one HyperFrames master serves these video surfaces) + divergences + text surfaces ──
> 102	INSERT INTO public.channel_profiles
> 103	  (user_id, channel, surface, priority, video, image, "text", publish_path, voice_prompt_seed, cadence, discovery, transform_recipe, confidence, spec_source_urls)
> 104	VALUES
> 105	(NULL,'instagram','reel',10,
> 106	  '{"aspect":"9:16","width":1080,"height":1920,"duration_s":{"min":5,"max":90,"sweet":[15,45]},"max_file_mb":100,"container":"mp4","vcodec":"h264","acodec":"aac","max_vbr_mbps":5,"audio_kbps":128,"fps":[23,60],"muxing":"moov_atom_front,no_edit_lists,closed_gop,4:2:0","safe_zone":{"top_pct":14,"bottom_pct":35}}'::jsonb,
> 107	  NULL,'{"caption_max":2200,"unit":"chars","hashtags":{"rec":[3,5],"max":30}}'::jsonb,
> 108	  'content_publishing_api','Visual-native, hook nos 3 primeiros segundos, autêntico; Gabriel AI evangeliza a visão MCORCH.',
> 109	  '{"target_per":"day","count_min":1,"count_max":2}'::jsonb,
> 110	  '{"primary":"watch_time","signals":["watch_time","sends","reach"],"hashtag_policy":"3-5 in caption"}'::jsonb,
> 111	  '{"derive_from":"9x16_master","reshape":"reexport_native","structure":["hook_0_3s","value_4_15s","payoff_16_45s","cta_end"],"cta":"link_in_bio_pillar","watermark":"none","field_map":{"caption":"atoms.hook + atoms.cta"}}'::jsonb,
> 112	  'high','{https://developers.facebook.com/docs/instagram-platform/content-publishing}'),
> 113	
> 114	(NULL,'facebook','reel',20,
> 115	  '{"aspect":"9:16","width":1080,"height":1920,"min_width":540,"min_height":960,"duration_s":{"min":3,"max":180,"boost_max":90},"container":"mp4","vcodec":"h264","acodec":"aac","fps":[24,60]}'::jsonb,
> 116	  NULL,'{"caption_max":63206,"unit":"chars","note":"sound-off captions mandatory"}'::jsonb,
> 117	  'graph_api','Conversacional, legenda funciona sem som; mesma essência da persona Gabriel AI.',
> 118	  '{"target_per":"day","count_min":1,"count_max":1}'::jsonb,
> 119	  '{"primary":"predicted_watch_duration","signals":["watch_duration","session_continuation"]}'::jsonb,
> 120	  '{"derive_from":"9x16_master","reshape":"reexport_native","cta":"link_in_caption","watermark":"none","field_map":{"caption":"atoms.hook + atoms.cta"}}'::jsonb,
> 121	  'high','{https://developers.facebook.com/docs/video-api/guides/reels-publishing}'),
> 122	
> 123	(NULL,'tiktok','video',10,
> 124	  '{"aspect":"9:16","width":1080,"height":1920,"duration_s":{"min":3,"max":600,"sweet":[15,34]},"max_file_mb":4096,"container":"mp4","vcodec":"h264","fps":[23,60],"is_aigc":true}'::jsonb,
> 125	  NULL,'{"caption_max":2200,"unit":"utf16_runes","hashtags":{"rec":[3,5]}}'::jsonb,
> 126	  'content_publishing_api','Casual, trend-aware, nativo; hook imediato. Persona Gabriel AI sem cara corporativa.',
> 127	  '{"target_per":"week","count_min":3,"count_max":5}'::jsonb,
> 128	  '{"primary":"watch_time","signals":["watch_time","skip_behavior","profile_visits"]}'::jsonb,
> 129	  '{"derive_from":"9x16_master","reshape":"reexport_native","structure":["hook_0_3s","value_4_15s","payoff_16_34s","cta_end"],"cta":"link_in_bio_pillar","watermark":"none","privacy_note":"unaudited=SELF_ONLY"}'::jsonb,
> 130	  'high','{https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide/}'),
> 131	
> 132	(NULL,'youtube','short',10,
> 133	  '{"aspect":"9:16","width":1080,"height":1920,"duration_s":{"min":3,"max":180},"container":"mp4","vcodec":"h264_high","acodec":"aac_lc","muxing":"moov_atom_front,closed_gop","bitrate_1080p_mbps":8}'::jsonb,
> 134	  NULL,'{"title_max":100,"desc_max":5000,"unit":"chars","hashtags":{"max":15,"note":">15 = all ignored"}}'::jsonb,
> 135	  'youtube_data_api','Educacional, value-dense, hook forte; #Shorts no título/desc.',
> 136	  '{"target_per":"day","count_min":1,"count_max":1}'::jsonb,
> 137	  '{"primary":"retention","signals":["retention","shorts_feed_swipes"]}'::jsonb,
> 138	  '{"derive_from":"9x16_master","reshape":"reexport_native","field_map":{"title":"atoms.hook","description":"atoms.key_points + atoms.pillar_url"}}'::jsonb,
> 139	  'high','{https://support.google.com/youtube/answer/10059070}'),
> 140	
> 141	(NULL,'twitter_x','video',30,
> 142	  '{"aspect":"9:16","aspect_range":"1:2.39-2.39:1","max_width":1920,"max_height":1200,"duration_s":{"min":0.5,"max":140,"premium_max":14400},"max_file_mb":512,"container":"mp4","vcodec":"h264","acodec":"aac","fps_max":40,"bitrate_max_mbps":25}'::jsonb,
> 143	  NULL,'{"caption_max":280,"premium_max":25000,"unit":"chars","url_cost_chars":23}'::jsonb,
> 144	  'x_api','Punchy, toma posição, conversacional; thread quando o pilar pede profundidade.',
> 145	  '{"target_per":"day","count_min":3,"count_max":5}'::jsonb,
> 146	  '{"primary":"early_velocity","signals":["likes","reposts","replies"],"note":"first 30-60min matter"}'::jsonb,
> 147	  '{"derive_from":"9x16_master","reshape":"reexport_native","cta":"link_in_post","field_map":{"caption":"atoms.hook"}}'::jsonb,
> 148	  'high','{https://help.x.com/en/using-x/x-videos}'),
> 149	
> 150	(NULL,'pinterest','video_pin',20,
> 151	  '{"aspect":"9:16","width":1080,"height":1920,"aspect_alts":["1:2","2:3","3:4","4:5","1:1"],"duration_s":{"min":4,"max":300,"rec":[6,15]},"max_file_mb":2048,"container":"mp4","vcodec":"h264"}'::jsonb,
> 152	  NULL,'{"title_max":100,"desc_max":800,"desc_best":500,"unit":"chars","keyword_seo":true}'::jsonb,
> 153	  'pinterest_api','Headline keyword-SEO (não caption); resolve uma intenção de busca.',
> 154	  '{"target_per":"week","count_min":3,"count_max":7}'::jsonb,
> 155	  '{"primary":"search_seo","signals":["keyword_match","visual_search"],"keyword_seo":true}'::jsonb,
> 156	  '{"derive_from":"9x16_master","reshape":"reexport_native","mode":"seo_text","field_map":{"title":"atoms.hook_keyworded","description":"atoms.key_points_keyworded"}}'::jsonb,
> 157	  'high','{https://help.pinterest.com/en/article/review-pin-specs}'),
> 158	
> 159	(NULL,'linkedin','video',40,
> 160	  '{"aspect":"9:16","aspect_range":"1:2.4-2.4:1","width":1080,"height":1920,"duration_s":{"min":3,"max":600},"max_file_mb":5120,"min_file_kb":75,"container":"mp4","vcodec":"h264","acodec":"aac","fps":[10,60],"unsupported":["avi","mov","quicktime"]}'::jsonb,
> 161	  NULL,'{"caption_max":3000,"optimal":[1300,1900],"fold_desktop":210,"unit":"chars"}'::jsonb,
> 162	  'linkedin_api','POV profissional-autoritativo, behind-the-build; thought leadership da marca.',
> 163	  '{"target_per":"week","count_min":2,"count_max":5}'::jsonb,
> 164	  '{"primary":"dwell","signals":["dwell","early_engagement"]}'::jsonb,
> 165	  '{"derive_from":"9x16_master","reshape":"reexport_native","cta":"link_in_post","field_map":{"caption":"atoms.hook + atoms.key_points + atoms.cta"}}'::jsonb,
> 166	  'high','{https://www.linkedin.com/help/linkedin/answer/a1311816}'),
> 167	
> 168	-- ── DIVERGENCES (distinct asset required) ──
> 169	(NULL,'youtube','long_video',50,
> 170	  '{"aspect":"16:9","width":1920,"height":1080,"duration_s":{"max":900,"verified_max":43200},"container":"mp4","vcodec":"h264_high","muxing":"moov_atom_front,closed_gop","bitrate_1080p_mbps":8,"color":"bt709"}'::jsonb,
> 171	  NULL,'{"title_max":100,"desc_max":5000,"unit":"chars","hashtags":{"max":15}}'::jsonb,
> 172	  'youtube_data_api','Educacional/value-dense, gancho nos 15s; o pilar canônico em vídeo.',
> 173	  '{"target_per":"week","count_min":1,"count_max":1}'::jsonb,
> 174	  '{"primary":"ctr_then_retention","signals":["thumbnail_ctr","retention"]}'::jsonb,
> 175	  '{"derive_from":"pillar_video_16x9","reshape":"render_16x9","field_map":{"title":"atoms.hook","description":"atoms.key_points + atoms.pillar_url"}}'::jsonb,
> 176	  'high','{https://support.google.com/youtube/answer/71673}'),
> 177	
> 178	(NULL,'youtube','thumbnail',60,
> 179	  NULL,'{"aspect":"16:9","width":1280,"height":720,"format":"jpeg","max_mb":2,"min_width":640}'::jsonb,
> 180	  NULL,'youtube_data_api','Texto curto + rosto/símbolo de alto contraste; maximizar CTR.',
> 181	  NULL,'{"primary":"ctr","keyword_seo":false}'::jsonb,
> 182	  '{"derive_from":"pillar_image","reshape":"render_thumbnail_16x9","field_map":{"overlay_text":"atoms.hook_short"}}'::jsonb,
> 183	  'high','{https://support.google.com/youtube/answer/72431}'),
> 184	
> 185	(NULL,'pinterest','standard_pin',30,
> 186	  NULL,'{"aspect":"2:3","width":1000,"height":1500,"format":"jpeg","max_mb":20,"keyword_in_first_chars":100}'::jsonb,
> 187	  '{"title_max":100,"desc_max":800,"desc_best":500,"unit":"chars","keyword_seo":true}'::jsonb,
> 188	  'pinterest_api','Headline keyword-SEO; imagem 2:3 vertical é obrigatória.',
> 189	  '{"target_per":"week","count_min":3,"count_max":7}'::jsonb,
> 190	  '{"primary":"search_seo","signals":["keyword_match","visual_search"],"keyword_seo":true}'::jsonb,
> 191	  '{"derive_from":"pillar_image","reshape":"reframe_2x3","mode":"seo_text","field_map":{"title":"atoms.hook_keyworded","description":"atoms.key_points_keyworded"}}'::jsonb,
> 192	  'high','{https://help.pinterest.com/en/article/review-pin-specs}'),
> 193	
> 194	(NULL,'instagram','feed_image',40,
> 195	  NULL,'{"aspect":"4:5","width":1080,"height":1350,"format":"jpeg","alt_ratios":["1:1","1.91:1"]}'::jsonb,
> 196	  '{"caption_max":2200,"unit":"chars","hashtags":{"rec":[3,5],"max":30}}'::jsonb,
> 197	  'content_publishing_api','Visual-native, hook-first; JPEG obrigatório via API.',
> 198	  '{"target_per":"week","count_min":3,"count_max":5}'::jsonb,
> 199	  '{"primary":"saves","signals":["saves","reach"]}'::jsonb,
> 200	  '{"derive_from":"pillar_image","reshape":"reframe_4x5","format_coerce":"jpeg","field_map":{"caption":"atoms.hook + atoms.cta"}}'::jsonb,
> 201	  'high','{https://developers.facebook.com/docs/instagram-platform/content-publishing}'),
> 202	
> 203	(NULL,'linkedin','feed_image',50,
> 204	  NULL,'{"aspect":"4:5","width":1080,"height":1350,"format":"png_or_jpeg","max_mb":3,"alt_ratios":["1:1"]}'::jsonb,
> 205	  '{"caption_max":3000,"optimal":[1300,1900],"unit":"chars"}'::jsonb,
> 206	  'linkedin_api','POV profissional; imagem 4:5 ocupa mais feed.',
> 207	  '{"target_per":"week","count_min":2,"count_max":4}'::jsonb,
> 208	  '{"primary":"dwell","signals":["dwell","early_engagement"]}'::jsonb,
> 209	  '{"derive_from":"pillar_image","reshape":"reframe_4x5","field_map":{"caption":"atoms.hook + atoms.key_points + atoms.cta"}}'::jsonb,
> 210	  'high','{https://www.linkedin.com/help/linkedin/answer/a563309}'),
> 211	
> 212	(NULL,'facebook','link_card',60,
> 213	  NULL,'{"aspect":"1.91:1","width":1200,"height":630,"format":"jpg_or_png","min_width":200,"min_height":200,"og_image":true}'::jsonb,
> 214	  '{"caption_max":63206,"unit":"chars"}'::jsonb,
> 215	  'graph_api','Conversacional; card de link puxa o pilar canônico.',
> 216	  '{"target_per":"week","count_min":2,"count_max":4}'::jsonb,
> 217	  '{"primary":"link_clicks","signals":["clicks","reach"]}'::jsonb,
> 218	  '{"derive_from":"pillar_image","reshape":"render_link_card_1.91x1","field_map":{"caption":"atoms.hook","link":"atoms.pillar_url"}}'::jsonb,
> 219	  'high','{https://developers.facebook.com/docs/sharing/webmasters/images}'),
> 220	
> 221	-- ── TEXT-FIRST surfaces ──
> 222	(NULL,'linkedin','text_post',30,
> 223	  NULL,NULL,'{"caption_max":3000,"optimal":[1300,1900],"fold_desktop":210,"fold_mobile":140,"unit":"chars"}'::jsonb,
> 224	  'linkedin_api','POV profissional-autoritativo, behind-the-build; primeiras 2 linhas = o gancho (fold).',
> 225	  '{"target_per":"week","count_min":2,"count_max":5}'::jsonb,
> 226	  '{"primary":"dwell","signals":["dwell","early_engagement"]}'::jsonb,
> 227	  '{"derive_from":"pillar_atoms","reshape":"text_post","field_map":{"body":"atoms.hook + atoms.key_points + atoms.cta + atoms.pillar_url"}}'::jsonb,
> 228	  'high','{https://www.linkedin.com/help/linkedin/answer/a1337010}'),
> 229	
> 230	(NULL,'twitter_x','thread',40,
> 231	  NULL,NULL,'{"per_tweet_max":280,"premium_max":25000,"unit":"chars","url_cost_chars":23}'::jsonb,
> 232	  'x_api','Punchy; 1 ideia por tweet; primeiro tweet = o gancho; último = CTA + link.',
> 233	  '{"target_per":"day","count_min":3,"count_max":5}'::jsonb,
> 234	  '{"primary":"early_velocity","signals":["likes","reposts","replies"]}'::jsonb,
> 235	  '{"derive_from":"pillar_atoms","reshape":"atoms_to_thread","field_map":{"tweet_1":"atoms.hook","tweets_n":"atoms.key_points","tweet_last":"atoms.cta + atoms.pillar_url"}}'::jsonb,
> 236	  'high','{https://help.x.com/en/using-x/how-to-tweet}'),
> 237	
> 238	(NULL,'wordpress','article',10,
> 239	  NULL,'{"aspect":"1.91:1","width":1200,"height":630,"format":"jpeg_or_webp","featured":true}'::jsonb,
> 240	  '{"body_max":null,"seo_title_best":60,"meta_desc_best":155,"unit":"chars","note":"long-form canonical home"}'::jsonb,
> 241	  'wp_rest','Profundidade + E-E-A-T (confiança), byline real; o LAR canônico que todo micro-post linka.',
> 242	  '{"target_per":"month","count_min":6,"count_max":8}'::jsonb,
> 243	  '{"primary":"organic_search","signals":["helpful_content","on_page_seo","backlinks"],"keyword_seo":true}'::jsonb,
> 244	  '{"derive_from":"pillar_article","reshape":"publish_long_form","field_map":{"title":"atoms.hook","body":"pillar_article","featured_image":"reframe_1.91x1"}}'::jsonb,
> 245	  'high','{https://wordpress.com/support/videopress/recommended-video-settings/}');
> 246	
> 247	-- ─────────────────────────────────────────────────────────────────────────────
> 248	-- 4. Telemetry note: reshaper/atomizer edge fns (FR-CP-002/003) emit to infra_health_logs
> 249	--    with service='reshape-<channel>'; creative_metrics gains hook_rate in a later slice (FR-CP-011).
> 250	-- ─────────────────────────────────────────────────────────────────────────────
> 251	
> ```

## 🤖 Claude *(02:21:15)*


## 🤖 Claude *(02:21:15)*

This is the load-bearing contract — crystal clear. The data dictionary is fully seeded: 16 system rows, each carrying a `transform_recipe` JSONB that drives the reshaper (zero per-channel code branch). The reshaper (FR-CP-003) is a recipe interpreter; the atomizer (FR-CP-002) feeds it `pillar_atoms`.

Before writing any code, I need to ground my design in the *real* existing pipeline (Lei 1 — not assumptions). Let me set up tracking and fan out a comprehensive UNDERSTAND pass over the live code.

## 🤖 Claude *(02:21:15)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Map existing social distribution pipeline (understand)",
  "description": "Fan-out readers over orchestrate-content, publish-social, auto-publish cron, HyperFrames render, generate-image/canvas-execute, autopilot-run/orchestrate-step, _shared helpers, creative_assets/social_accounts schema. Produce a grounded map of contracts + reshaper integration hooks.",
  "activeForm": "Mapping existing distribution pipeline"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #1 created successfully: Map existing social distribution pipeline (understand)
> ```

## 🤖 Claude *(02:21:17)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Design reshaper + atomizer architecture (FR-CP-002/003)",
  "description": "Design the atomizer node (pillar \u2192 pillar_atoms) and the reshaper edge fn (recipe interpreter reading channel_profiles.transform_recipe). Cover all reshape directives, format-coercion gate (FR-CP-006), native-variant fan-out (FR-CP-007), Pinterest-SEO text (FR-CP-008), scheduler binding (FR-CP-010).",
  "activeForm": "Designing reshaper + atomizer architecture"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #2 created successfully: Design reshaper + atomizer architecture (FR-CP-002/003)
> ```

## 🤖 Claude *(02:21:19)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Implement atomizer (FR-CP-002)",
  "description": "Edge fn / node that decomposes a pillar into pillar_atoms (hook, key_points[], stat, quote, cta, pillar_url). Reuses orchestrate-content chaining; sentinel-safe; per-user JWT; mco atomic if billable.",
  "activeForm": "Implementing atomizer"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #3 created successfully: Implement atomizer (FR-CP-002)
> ```

## 🤖 Claude *(02:21:21)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Implement reshaper edge fn (FR-CP-003/006/007/008)",
  "description": "Recipe interpreter: reads channel_profiles.transform_recipe + pillar_atoms, derives native asset per reshape directive, applies row constraints as upload gate (FR-CP-006), emits native variant per surface (FR-CP-007), Pinterest-SEO text mode (FR-CP-008). Fail-open per channel + infra_health_logs telemetry.",
  "activeForm": "Implementing reshaper edge fn"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #4 created successfully: Implement reshaper edge fn (FR-CP-003/006/007/008)
> ```

## 🤖 Claude *(02:21:22)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Wire reshaper into pipeline + scheduler (FR-CP-010)",
  "description": "Bind reshaper output to publish branches (doc 10) via row.publish_path and to autopilot scheduler by cadence + priority. Hook into orchestrate-content / autopilot-run flow.",
  "activeForm": "Wiring reshaper into pipeline + scheduler"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #5 created successfully: Wire reshaper into pipeline + scheduler (FR-CP-010)
> ```

## 🤖 Claude *(02:21:24)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Schema deltas + tests + /security-review + deploy + seal",
  "description": "Migration for creative_metrics.hook_rate (FR-CP-011) and any reshape-output table; zero-cost smokes (gates); /security-review on migrations; deploy edge fns; seal with mesh node + HANDOFF.",
  "activeForm": "Schema deltas, tests, security-review, deploy, seal"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #6 created successfully: Schema deltas + tests + /security-review + deploy + seal
> ```

## 🤖 Claude *(02:21:31)*


## 🤖 Claude *(02:21:31)*

Now the comprehensive UNDERSTAND pass — fanning out grounded readers over the live pipeline so the design is anchored in real code.

## 🤖 Claude *(02:21:31)*


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

## 🤖 Claude *(02:22:20)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'understand-social-distribution',\n  description: 'Map the live MCORCH social distribution pipeline to ground the FR-CP-003 reshaper design',\n  phases: [\n    { title: 'Map', detail: 'parallel readers over each subsystem' },\n    { title: 'Critic', detail: 'completeness pass \u2014 what is missing for the reshaper' },\n  ],\n}\n\nconst SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['area', 'files', 'mechanism', 'contracts', 'gotchas', 'reshaper_hooks'],\n  properties: {\n    area: { type: 'string' },\n    files: {\n      type: 'array',\n      items: {\n        type: 'object', additionalProperties: false,\n        required: ['path', 'role'],\n        properties: { path: { type: 'string' }, role: { type: 'string' } },\n      },\n    },\n    mechanism: { type: 'string', description: 'How this subsystem works end-to-end, concrete, citing file:line where possible' },\n    contracts: {\n      type: 'array',\n      description: 'Exact integration contracts: function signatures, request/response shapes, table columns, API call shapes, env/secret names',\n      items: {\n        type: 'object', additionalProperties: false,\n        required: ['name', 'detail'],\n        properties: { name: { type: 'string' }, detail: { type: 'string' } },\n      },\n    },\n    gotchas: { type: 'array', items: { type: 'string' }, description: 'Silent-failure traps, format defaults, auth quirks, billing pitfalls' },\n    reshaper_hooks: { type: 'array', items: { type: 'string' }, description: 'Precisely where/how the FR-CP-003 reshaper would integrate with this subsystem (call point, table to write, asset to read)' },\n  },\n}\n\nconst DIMENSIONS = [\n  {\n    key: 'orchestrate-content',\n    prompt: `Read supabase/functions/orchestrate-content/index.ts and supabase/functions/orchestrate-step/index.ts in full. Map how the content PILLAR is generated: the article (generate-content), the 9:16 video master (HyperFrames enqueue), the images (generate-image). Document: what tables it writes (content_library, creative_assets, creative_metrics, pillar/run ids), how pillar_run_id / cycle id flows, the prepaid billing model (FR-VA-016 prepaid flag, deduct_mco_coins), how it is invoked (JWT vs service-role), and where the atomizer (FR-CP-002) and reshaper (FR-CP-003) would slot in. Cite file:line. This is for building a data-driven reshaper that consumes the pillar output.`,\n  },\n  {\n    key: 'publish-social',\n    prompt: `Read supabase/functions/publish-social/index.ts in full plus the auto-publish cron (find it: likely supabase/functions/auto-publish/ or scripts/auto-publish-cron.sh) and supabase/functions/_shared/social-app-config.ts. Map EVERY platform publish branch (linkedin, instagram, facebook, twitter_x, tiktok, youtube, pinterest, wordpress if present): the exact external API call, what media format/aspect each expects, how it receives the media (video_url / image url / path / storage bucket), how creds resolve (social_accounts Vault + resolveSocialAppCreds + meta_config), and the known gotchas (TikTok SELF_ONLY, IG graph.instagram.com vs facebook.com, YouTube videos.insert private, IG JPEG-only, format coercion). Document the request body the reshaper must send to each publish path (publish_path values: content_publishing_api, graph_api, x_api, tiktok content_publishing_api, youtube_data_api, pinterest_api, linkedin_api, wp_rest). Cite file:line.`,\n  },\n  {\n    key: 'hyperframes-render',\n    prompt: `Read scripts/hyperframes/render-core.ts, scripts/video-bridge.ts, supabase/functions/video-render/index.ts, and scripts/hyperframes/templates/viral-short-9x16.html. Map how a 9:16 1080x1920 MP4 master is produced: the video_renders table (claim/finalize RPCs), the composition jsonb shape, where the rendered MP4 lands (bucket video-studio-assets / creative_assets), the edge transport (poll://), and the deterministic render contract (NFR-VS-016 sha256). CRITICAL for FR-CP-004 (16:9 render): is there a 16:9 template? How would a new horizontal template be added? Document the EXACT composition jsonb shape a reshaper must pass to enqueue a render (9:16 reexport vs 16:9), and how it reads back the finished asset. Cite file:line.`,\n  },\n  {\n    key: 'image-engine',\n    prompt: `Read supabase/functions/generate-image/index.ts and supabase/functions/canvas-execute/index.ts (the image-generation paths). Map: how images are generated (which providers, BYOK via decrypted_user_api_keys, the google_api_key Gemini column), the OUTPUT FORMAT (is it PNG by default? the FR-CP-006 gotcha is IG needs JPEG, TikTok WebP/JPEG, no PNG), the aspect/dimensions produced, where images land (bucket, creative_assets, content_library.media_url). CRITICAL for FR-CP-005 (image reframe 4:5 / 2:3 / 1.91:1 with safe-zone) and FR-CP-006 (format coercion to JPEG/WebP): is there ANY existing crop/reframe/format-convert capability (sharp, ffmpeg, ImageMagick, a Deno image lib)? If not, what's the lightest path to reframe+convert an image in an edge fn or worker? Cite file:line.`,\n  },\n  {\n    key: 'autopilot-scheduler',\n    prompt: `Read supabase/functions/autopilot-run/index.ts, supabase/functions/autopilot-cadence-cron/index.ts, and the autopilot migrations (supabase/migrations/20260620120000_viral_autopilot_plans.sql, ...120100_viral_autopilot_cycles.sql, ...120200_begin_autopilot_cycle.sql, ...120300_finalize_autopilot_cycle.sql). Map the cadence/scheduling model: how autopilot_plans drives runs, begin/finalize_autopilot_cycle atomic RPCs, how N_runs is computed (prod x rede x ab_variants), how content gets scheduled for publish (is there a social_posts / scheduled_posts table? how does auto-publish pick them up?). CRITICAL for FR-CP-010 (scheduler binding cadence+priority to autopilot_plans): document exactly how the reshaper's per-channel cadence (channel_profiles.cadence {target_per, count_min, count_max} + priority) would bind to the existing autopilot scheduler. Cite file:line.`,\n  },\n  {\n    key: 'shared-infra-schema',\n    prompt: `Map the shared edge-fn conventions and the relevant DB schema. Read supabase/functions/_shared/sentinel.ts (inspectPrompt pt-BR), supabase/config.toml (verify_jwt settings per function), and find the table definitions for: social_accounts (Vault token columns), social_posts / scheduled posts (the queue auto-publish reads), creative_assets (the spine \u2014 migration ~20260624 or search), creative_metrics (and whether hook_rate column exists yet \u2014 FR-CP-011 wants to add it). Document the standard edge-fn scaffold (CORS headers, JWT guard, mcoCoins deduct_mco_coins RPC, infra_health_logs emit shape with event+metadata allowlist), the ES256 JWKS verify pattern for verify_jwt=false fns, and the COIN_COSTS in src/lib/billing.ts. Cite file:line. This grounds the reshaper/atomizer edge-fn scaffold + any migration deltas.`,\n  },\n]\n\nphase('Map')\nconst maps = await parallel(DIMENSIONS.map(d => () =>\n  agent(d.prompt, { label: `map:${d.key}`, phase: 'Map', schema: SCHEMA })\n))\nconst found = maps.filter(Boolean)\n\nphase('Critic')\nconst critic = await agent(\n  `You are the completeness critic for a design about to begin: the FR-CP-003 \"reshaper\" \u2014 a data-driven edge function that reads channel_profiles.transform_recipe + pillar_atoms and produces NATIVE social posts for 8 channels from one pillar idea (zero per-channel code branch).\n\nHere are the grounded subsystem maps produced by readers:\n\n${found.map(m => `### ${m.area}\\nMECHANISM: ${m.mechanism}\\nCONTRACTS:\\n${(m.contracts||[]).map(c => `- ${c.name}: ${c.detail}`).join('\\n')}\\nGOTCHAS:\\n${(m.gotchas||[]).map(g => `- ${g}`).join('\\n')}\\nRESHAPER HOOKS:\\n${(m.reshaper_hooks||[]).map(h => `- ${h}`).join('\\n')}`).join('\\n\\n')}\n\nThe BoK contract (post-engine amendment 12) requires the reshaper to handle these reshape directives from transform_recipe.reshape: reexport_native (9:16 master \u2192 7 video surfaces), render_16x9 (YouTube long), render_thumbnail_16x9, reframe_2x3 (Pinterest pin), reframe_4x5 (IG/LinkedIn feed image), render_link_card_1.91x1 (FB), text_post (LinkedIn), atoms_to_thread (X), publish_long_form (WordPress). Plus a format-coercion upload gate (FR-CP-006), native-variant emission (FR-CP-007), Pinterest-SEO text (FR-CP-008).\n\nIdentify what is STILL UNKNOWN or UNVERIFIED that would block or derail the reshaper implementation. Be specific and concrete. For each gap: what exactly is missing, why it blocks, and the cheapest way to resolve it (a file to read, a query to run, a decision to make). Also flag any contradiction between the maps and the BoK contract.`,\n  { label: 'critic:completeness', phase: 'Critic', schema: {\n    type: 'object', additionalProperties: false,\n    required: ['blocking_gaps', 'contradictions', 'recommended_build_order', 'reuse_vs_netnew'],\n    properties: {\n      blocking_gaps: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['gap','why','resolve'], properties: { gap:{type:'string'}, why:{type:'string'}, resolve:{type:'string'} } } },\n      contradictions: { type: 'array', items: { type: 'string' } },\n      recommended_build_order: { type: 'array', items: { type: 'string' } },\n      reuse_vs_netnew: { type: 'string', description: 'concise: what reshaper can reuse vs what is genuinely net-new code' },\n    },\n  } }\n)\n\nreturn { maps: found, critic }\n",
  "description": "Map live social distribution pipeline"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wj8bku6oe
> Summary: Map the live MCORCH social distribution pipeline to ground the FR-CP-003 reshaper design
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/2c25c853-bfbe-43d0-96c9-675282d65093/subagents/workflows/wf_a390c0f0-b6e
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/2c25c853-bfbe-43d0-96c9-675282d65093/workflows/scripts/understand-social-distribution-wf_a390c0f0-b6e.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/2c25c853-bfbe-43d0-96c9-675282d65093/workflows/scripts/understand-social-distribution-wf_a390c0f0-b6e.js"} to iterate without resending the script.)
> Run ID: wf_a390c0f0-b6e
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/2c25c853-bfbe-43d0-96c9-675282d65093/workflows/scripts/understand-social-distribution-wf_a390c0f0-b6e.js", resumeFromRunId: "wf_a390c0f0-b6e"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(02:22:26)*


## 🤖 Claude *(02:22:27)*

Workflow running in background. While it maps the live code, let me read the remaining load-bearing BoK docs myself (my SSOT) — the verified spec matrix in the blueprint and the data-model reconciliation.

## 🤖 Claude *(02:22:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/11-channel-format-intelligence-blueprint.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Channel Format Intelligence — Data-Driven Reverse-Engineering Engine (Blueprint Seed)
> 2	
> 3	> **Status:** Blueprint seed (pre-BoK-amendment) · **Date:** 2026-06-27
> 4	> **Provenance:** grounded deepsearch workflow `wf_98eede6d-069` — 18 agents (8 channels × research+adversarial-spec-verify pipeline + validated-frameworks front + synthesis), 311 web tool calls. Raw per-channel verified specs (139 KB): session task output `wvmmbwzie` (`tasks/wvmmbwzie.output`).
> 5	> **SSOT directive:** CLAUDE.md Closed-Loop Protocol + API Tenancy Model. This is the **seed** for a `post-engine` / `viral-autopilot` BoK amendment — code stays gated until MRD/BRD/PRD/FRD/SDD are amended (SDD must carry the Pattern Conformance Declaration, Step 3.5).
> 6	> **Thesis:** "Data dictates the rules." One pillar idea → engine reads a `channel_profiles` data dictionary → reshapes the pillar into each channel's correct **format, voice, cadence**. No per-channel code branches; rules live in data. Formalizes the GaryVee reverse-pyramid + Content Atomization onto our `viral-autopilot` + HyperFrames stack.
> 7	
> 8	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (Gabriel) · Owner = Sovereign (blast radius = downstream FRs built on wrong specs).
> 9	
> 10	**Confidence legend:** ✅ official/verbatim · ⚠️ ratio-correct / convention pixels · ❓ uncertain (verify-flagged) · 🔴 GAP for current pipeline · 🟢 FIT
> 11	
> 12	---
> 13	
> 14	## 1. CROSS-CHANNEL FORMAT MATRIX
> 15	
> 16	### 1.1 Video specs (the load-bearing upload gates)
> 17	
> 18	| Channel | Aspect | Resolution | Duration (API/practical) | Max file | Codec/container | Encoding caps | Conf |
> 19	|---|---|---|---|---|---|---|---|
> 20	| **LinkedIn** | 1:2.4–2.4:1 (9:16 inside) | 256×144 → 4096×2304; 1080p rec | 3s → **10min Pages/mobile, 15min profile-desktop** | **5 GB** (min 75 KB) | MP4 H.264/AAC (+MKV/WebM/VP8/9; **no AVI/MOV/QuickTime**) | 10–60 fps; 192 Kbps–30 Mbps | ✅ (dur corrected) |
> 21	| **Instagram Reels** | **9:16 req for Reels-tab** (API 0.01–10:1) | 1080×1920 | API ≤15min; **5–90s Reels-tab eligible**; algo favors <90s | **100 MB (API path!)** | MOV/MP4, **moov front, no edit lists**, H.264/HEVC, closed GOP, 4:2:0; AAC ≤48kHz | **VBR ≤5 Mbps**, audio 128 kbps, ≤1920 horiz, 23–60 fps | ✅ |
> 22	| **Facebook Reels** | 9:16 rec | 1080×1920 (min 540×960) | post-Jun2025 cap dropped → ~180s, boost ≤90s | **No documented Reels cap**; feed ~4 GB | MP4/MOV, H.264/H.265/VP9/AV1, AAC-LC 48kHz, 4:2:0, closed GOP 2–5s | 24–60 fps fixed | ✅ (size/dur corrected) |
> 23	| **Twitter/X** | **1:2.39–2.39:1** (9:16 inside) | min 32×32, max 1920×1200 | **140s free** / <4h Premium | **512 MB free** / 16 GB Premium | MP4 H.264+AAC (MOV ok) | ≤40 fps, ≤25 Mbps; ≤60s auto-loops | ✅ |
> 24	| **TikTok** | 9:16 rec (1:1/16:9 letterbox) | 1080×1920; API 360–4096 px/side | **API ≤10min**; FYP sweet 15–34s | **4 GB (API)** (~72MB Android/287MB iOS in-app) | MP4(rec)/WebM/MOV; H.264(rec)/H.265/VP8/VP9 | 23–60 fps | ✅ |
> 25	| **YouTube Shorts** | **9:16** | 1080×1920 | **≤180s (3min)** | (256 GB/12h global) | MP4 H.264 High, moov-front, closed GOP, AAC-LC/Opus 48kHz | SDR 1080p 8 Mbps / 60fps 12 Mbps | ✅ |
> 26	| **YouTube long-form** | **16:9** | 1920×1080+ | ≤15min unverified / ≤12h verified | 256 GB or 12h | (same stack) | 1440p 16/24 Mbps, 4K 35–68 Mbps; BT.709 | ✅ |
> 27	| **Pinterest Video Pin** | **9:16 rec** (1:2,2:3,3:4,4:5,1:1) | 1080×1920 | **4s–5min** (organic); ad rec 6–15s | **2 GB** | MP4/MOV/M4V, H.264/H.265 | — | ✅ |
> 28	| **WordPress (VideoPress)** | landscape framed (9:16 plays, ❓not spec'd) | 1920×1080 rec / 4K max | host/plan-governed | host-governed | MP4 H.264, Fast Start, AAC ≥160kbps | 1080p30 8 Mbps / 1080p60 12 Mbps | ✅ / ❓ vertical |
> 29	
> 30	### 1.2 Image specs
> 31	
> 32	| Channel | Canonical ratio / px | Format (API note) | Max size | Conf |
> 33	|---|---|---|---|---|
> 34	| **LinkedIn** | feed **4:5 1080×1350** / 1:1; link-preview **1.91:1 1200×627** ✅ | PNG/JPEG | 3 MB | ⚠️ feed px convention |
> 35	| **Instagram** | feed **4:5 1080×1350** / 1:1 1080×1080 / 1.91:1; Story 9:16; **grid crops 3:4** | **JPEG only (API)** 🔴 | — | ✅ |
> 36	| **Facebook** | feed **4:5 1080×1350**; **og:image 1.91:1 1200×630** (min 200×200) | JPG/PNG | photo ~30 MB ❓ | ✅ |
> 37	| **Twitter/X** | **16:9 1200×675** / 1.91:1 link / 1:1; 1–4 imgs | **GIF/JPEG/PNG only** | **5 MB** | ✅ size · ⚠️ px |
> 38	| **TikTok carousel** | **9:16 1080×1920**; up to **35 imgs** | **WebP/JPEG (no PNG)** 🔴 | **20 MB/img** | ✅ |
> 39	| **YouTube thumbnail** | **16:9 1280×720 → 3840×2160** | JPG/GIF/PNG | 2 MB mobile / 50 MB desktop | ✅ |
> 40	| **Pinterest Standard Pin** | **2:3 1000×1500** (the one rec ratio) | PNG/JPEG (+BMP/TIFF/WEBP organic) | 20 MB web / 32 MB in-app | ✅ |
> 41	| **WordPress** | featured **1.91:1 1200×628/630**; hero 16:9 1920×1080 | JPEG/PNG/**WebP/AVIF** | host-governed | ✅ |
> 42	
> 43	### 1.3 Text / content types / voice / cadence / discovery
> 44	
> 45	| Channel | Body max / fold | Title | Content types | Tone/voice | Cadence | Discovery driver | Conf |
> 46	|---|---|---|---|---|---|---|---|
> 47	| **LinkedIn** | **3,000** / fold ~140 mob ~210 desk; optimal 1,300–1,900 | article 150 | text, **PDF carousel (≤300pg/100MB, highest eng ~7%)** 🔴, img, native video, poll | Professional-authoritative POV / behind-the-build | **2–5×/wk** | dwell + early eng | ✅ |
> 48	| **Instagram** | caption **2,200** / fold ~125; 3–5 hashtags (max 30) | — | Reels, **carousel ≤10 (50/24h)**, Story, photo | Visual-native, hook-first, authentic | **3–5 feed/wk + 1–2 Reels/day** | watch time > sends > likes; originality bonus | ✅ |
> 49	| **Facebook** | **63,206** / trunc ~125 mob | — | Reels, feed video, link post (**og:image** 🔴), photo 4:5 | Conversational, sound-off captions | Reels daily | predicted watch-duration; negatives hurt | ✅ |
> 50	| **Twitter/X** | **280 free** / 25,000 Premium; URL=23 chars | none | thread (N×280), single, 1–4 imgs, video | Punchy, takes-a-stance | **3–5/day** (>10 ~14% less eng) | NN on Like/Repost/Reply; first 30–60min velocity | ✅ |
> 51	| **TikTok** | **video 2,200 runes**; **photo title 90 + desc 4,000** 🔴 | photo: 90 | FYP video, photo carousel (4–35) | Casual, trend-aware, native | **2–5×/wk** | watch time weighted most | ✅ |
> 52	| **YouTube** | desc **5,000** / fold ~150; **≤15 hashtags (>15 = all ignored)** | **100** (trunc ~60-70) | Short ≤3min, long 16:9, thumbnail | Educational/value-dense, strong hook | **Short daily + ~1 long/wk** | thumbnail CTR (long) + retention | ✅ |
> 53	| **Pinterest** | desc **800 field / ≤500 best** ❓; on-image 250 | **100** (40 visible) | Video Pin, Standard Pin 2:3, carousel, Idea Pin 🔴 | **Keyword SEO headline**, not caption | **weekly** (trends last ~2×) | **search/SEO + visual search** | ✅ / ❓ |
> 54	| **WordPress** | **no limit** (long-form home); SEO title ~60 / meta ~155 | ~60 best | long article (canonical), VideoPress | Depth + **E-E-A-T**, real byline | **6–8/mo** | organic Google; helpful content + on-page SEO + backlinks | ✅ |
> 55	
> 56	---
> 57	
> 58	## 2. COMMON SPINE vs DIVERGENCE — mapped to what we PRODUCE
> 59	
> 60	We already produce: **(A) 9:16 1080×1920 H.264 MP4** (HyperFrames, deterministic) · **(B) images** (canvas/Gemini) · **(C) text** (long article + LinkedIn post + X thread).
> 61	
> 62	### 2.1 Common Spine — ONE render serves many (the win)
> 63	
> 64	| Asset | Channels it fits | Output | Status |
> 65	|---|---|---|---|
> 66	| **9:16 1080×1920 MP4** | IG Reels, FB Reels, TikTok, YT Shorts, X (in range), Pinterest Video Pin, IG Story (≤60s), LinkedIn (soft-fit) | (A) HyperFrames master | 🟢 **FIT — 7 channels off ONE master** |
> 67	| **Long article text** | WordPress (canonical pillar home) | (C) | 🟢 FIT |
> 68	| **Short text post** | LinkedIn post, X thread | (C) | 🟢 FIT |
> 69	
> 70	**Anti cross-post guardrail:** identical re-push = ~40–60% reach loss (recycled-content flag). Our HyperFrames master is **clean/watermark-free** (an asset) — but the engine MUST **re-export per-channel native variants** (caption style, end-card CTA, safe-zones, hook). Spine = same idea+base render; divergence = per-channel finishing.
> 71	
> 72	### 2.2 Divergence — distinct asset required
> 73	
> 74	| Distinct asset | Channels | Produce it? | Status |
> 75	|---|---|---|---|
> 76	| **16:9 horizontal video** | YouTube long-form | only 9:16 | 🔴 GAP — HyperFrames 16:9 path |
> 77	| **4:5 1080×1350 image** | IG/FB/LinkedIn feed | square/landscape default | 🔴 GAP (reshape) |
> 78	| **2:3 1000×1500 image** | Pinterest (only rec ratio) | default not 2:3 | 🔴 GAP (required) |
> 79	| **1.91:1 1200×630 og:image / link card** | WP featured, FB link, X/LinkedIn preview | not produced | 🔴 GAP |
> 80	| **16:9 thumbnail 1280×720** | YouTube long | image engine can | 🟡 top CTR lever |
> 81	| **PDF carousel (multi-page)** | LinkedIn (~7% eng), TikTok photo, IG carousel, Pinterest Idea Pin | single only | 🔴 GAP |
> 82	| **Native MP4 variants** | TikTok/Reels/Shorts (distinct hook/safe-zone/audio) | one render | 🟡 partial GAP |
> 83	| **1 long → N distinct shorts** | Hormozi model | one MP4 | 🔴 GAP |
> 84	| **Pinterest-SEO text** | Pinterest (keyword title+desc) | feed-caption | 🔴 GAP |
> 85	
> 86	**Silent-break clashes the data model MUST encode (verify-caught):**
> 87	- **IG/TikTok API image format ≠ in-app.** API: IG = **JPEG only**, TikTok = **WebP/JPEG (no PNG)**. Our PNG default breaks API publish.
> 88	- **IG Reels API ceiling = 100 MB / VBR ≤5 Mbps** (NOT 4 GB in-app). HyperFrames envelope must target the API path.
> 89	- **TikTok photo caption split** (title ≤90 + desc ≤4,000) ≠ video caption (2,200).
> 90	- **TikTok in-app ~72MB Android / 287MB iOS** — only Content Posting **API** gets 4 GB; publisher path determines the gate.
> 91	
> 92	---
> 93	
> 94	## 3. PROPOSED DATA MODEL — `channel_profiles` (rules as data)
> 95	
> 96	Two tables: `channel_profiles` (rule dictionary, system rows + per-user override) + `pillar_atoms` (atomized pillar each reshaper reads).
> 97	
> 98	```sql
> 99	CREATE TABLE public.channel_profiles (
> 100	  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 101	  user_id           uuid REFERENCES auth.users(id),   -- NULL = system default (visible all tenants)
> 102	  channel           text NOT NULL,   -- linkedin|instagram|facebook|twitter_x|tiktok|youtube|pinterest|wordpress
> 103	  surface           text NOT NULL,   -- reel|short|feed_video|story|feed_image|carousel|link_card|thumbnail|long_video|video_pin|standard_pin|article|text_post|thread
> 104	  is_active         boolean NOT NULL DEFAULT true,
> 105	  priority          int NOT NULL DEFAULT 100,
> 106	  video             jsonb,           -- {aspect,width,height,duration_s{min,max,sweet},max_file_mb,container,vcodec,acodec,max_vbr_mbps,fps,muxing,safe_zone}
> 107	  image             jsonb,           -- {aspect,width,height,format,max_mb,...}
> 108	  text              jsonb,           -- {caption_max|title_max+desc_max,unit,hashtags}
> 109	  publish_path      text,            -- content_publishing_api|native_upload|graph_api|wp_rest → governs WHICH size/format gate applies
> 110	  voice_prompt_seed text NOT NULL,   -- persona-aware (Gabriel AI/CCIO) shaped per channel
> 111	  cadence           jsonb,           -- {target_per:day|week|month,count_min,count_max,note}
> 112	  discovery         jsonb,           -- {primary,signals[],hashtag_policy,keyword_seo:bool}
> 113	  transform_recipe  jsonb NOT NULL,  -- HOW to derive this asset from pillar_atoms (reverse-engineering core)
> 114	  confidence        text NOT NULL DEFAULT 'high',
> 115	  spec_source_urls  text[] NOT NULL, -- Law 1: every spec carries its grounding URL
> 116	  updated_at        timestamptz DEFAULT now(),
> 117	  UNIQUE (user_id, channel, surface)
> 118	);
> 119	-- RLS: SELECT user_id IS NULL OR user_id = auth.uid(); write own only. search_path=''.
> 120	
> 121	CREATE TABLE public.pillar_atoms (
> 122	  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 123	  user_id       uuid NOT NULL REFERENCES auth.users(id),
> 124	  pillar_run_id uuid,             -- links to orchestrate-content / autopilot cycle
> 125	  hook          text,             -- 0-3s scroll-stopper
> 126	  key_points    jsonb,            -- 3-5 → carousel slides / thread tweets
> 127	  stat text, quote text, cta text,
> 128	  pillar_url    text,             -- canonical home (WP blog / YT long) every micro links back to
> 129	  created_at    timestamptz DEFAULT now()
> 130	);
> 131	```
> 132	
> 133	**transform_recipe example (the reverse-engineering instruction set):**
> 134	```jsonc
> 135	{ "derive_from":"9x16_master", "reshape":"reexport_native",
> 136	  "structure":["hook_0_3s","value_4_15s","payoff_16_45s","cta_end"],
> 137	  "cta":"link_in_bio_pillar", "watermark":"none",
> 138	  "field_map":{"caption":"atoms.hook + atoms.cta"} }
> 139	```
> 140	
> 141	**Engine flow (zero per-channel code):** pillar idea → orchestrate-content → emit `pillar_atoms` (NEW node) → for each active `channel_profiles` row: reshaper reads `transform_recipe`+atoms → applies row constraints (the gate) → publishes via `publish_path` → autopilot drips per `cadence`.
> 142	
> 143	---
> 144	
> 145	## 4. RECOMMENDATION — encoding & roadmap
> 146	
> 147	**AMEND the `post-engine` / `viral-autopilot` BoK — NOT a new sibling module.** It reuses autopilot cadence schema, orchestrate-content pillar gen, HyperFrames 9:16 master, social_accounts Vault creds, the 5 live + 3 in-review publish branches. A sibling would fork that plumbing = debt. SDD amendment MUST carry the Pattern Conformance Declaration (atomization=planning, reshape=tool-use, cadence=scheduling ⇒ ≥3 patterns).
> 148	
> 149	### FRs (extend FR-CP series)
> 150	
> 151	| FR | Title | Reuse | Net-new |
> 152	|---|---|---|---|
> 153	| FR-CP-001 | `channel_profiles` + `pillar_atoms` schema + system rows | RLS/Vault | tables + seed |
> 154	| FR-CP-002 | Pillar atomizer (article → atoms) | orchestrate-content | atom prompt |
> 155	| FR-CP-003 | Per-channel reshaper (reads transform_recipe) | HyperFrames, image engine | recipe interpreter |
> 156	| FR-CP-004 | **16:9 HyperFrames render path** (YouTube long) | render-core | 16:9 template |
> 157	| FR-CP-005 | **Image reframe** 4:5 / 2:3 / 1.91:1 link-card | canvas/Gemini | reframe+safe-zone |
> 158	| FR-CP-006 | **API format coercion** (IG JPEG, TikTok WebP/JPEG, ≤100MB IG envelope) | publish branches | format gate |
> 159	| FR-CP-007 | **Native-variant fan-out** (anti cross-post) | — | variant emitter |
> 160	| FR-CP-008 | Pinterest-SEO text mode | text gen | SEO prompt |
> 161	| FR-CP-009 | **PDF carousel / multi-page** (LinkedIn highest-eng) | — | doc renderer |
> 162	| FR-CP-010 | Cadence scheduler binding `channel_profiles.cadence` → autopilot_plans | autopilot cron | binding |
> 163	| FR-CP-011 | Hook-rate KPI (watch-past-3s) in creative_metrics | creative_metrics | metric |
> 164	| FR-CP-012 | Auto-segment 1 long → N shorts (Hormozi) | — | segmenter (later) |
> 165	
> 166	### OTDs
> 167	
> 168	| OTD | Decision / risk |
> 169	|---|---|
> 170	| OTD-CP-001 | Spec drift — rows carry `spec_source_urls`+`confidence`; quarterly re-verify cadence. |
> 171	| OTD-CP-002 | API-path vs in-app gate (`publish_path` governs ceiling — IG 100MB API vs 4GB in-app). |
> 172	| OTD-CP-003 | Pinterest desc 800 field vs 500 best — soft-cap 500, hard 800. |
> 173	| OTD-CP-004 | Cross-post mitigation depth — full native variants vs minimal (safe-zone+CTA). HyperFrames deterministic → no trending audio yet (GAP). |
> 174	| OTD-CP-005 | LinkedIn 9:16 raw vs reframe-to-4:5 (9:16 uploads but white-padded in feed). |
> 175	| OTD-CP-006 | Multi-tenant: system rows (`user_id NULL`) defaults + per-user override (mirrors mcorch_nodes tenancy). |
> 176	
> 177	### Reusable NOW vs net-new
> 178	- **Reusable (~90%):** 9:16 master (7-channel spine), orchestrate-content pillar gen, autopilot cadence, social_accounts Vault, 5 live + 3 in-review publishers, RLS/tenancy, creative_metrics.
> 179	- **Net-new (the build):** the `channel_profiles` dictionary (this seed) + atomizer + **reshaper interpreter** (highest leverage — without it the spine is one cross-posted file = penalty trap) + 16:9 render + image reframe + API format coercion + native-variant fan-out + PDF carousel + Pinterest-SEO text.
> 180	
> 181	---
> 182	
> 183	## Load-bearing source URLs (upload-gate verbatim)
> 184	LinkedIn video `linkedin.com/help/linkedin/answer/a1311816` · Meta IG Content Publishing `developers.facebook.com/docs/instagram-platform/content-publishing` (JPEG-only, 10/24h caps) · FB Reels API `developers.facebook.com/docs/video-api/guides/reels-publishing` · X video `help.x.com/en/using-x/x-videos` · TikTok `developers.tiktok.com/doc/content-posting-api-media-transfer-guide/` + photo-post (90/4000 split) · YouTube `support.google.com/youtube/answer/71673` + Shorts `10059070` · Pinterest `help.pinterest.com/en/article/review-pin-specs` · WordPress VideoPress `wordpress.com/support/videopress/recommended-video-settings/`. Frameworks: GaryVee reverse-pyramid · Content Atomization (Aprimo) · hook-body-CTA · cross-post penalty · cadence (Buffer).
> 185	
> ```

## 🤖 Claude *(02:23:08)*


## 🤖 Claude *(02:23:10)*

I now have full command of the BoK contract (amendment §6 + blueprint §1-3 spec matrix + the seeded `transform_recipe` directives). The workflow is mapping the live code. While it runs, let me independently read the absolute crux — how a variant actually gets published — so my design isn't built on a wrong assumption about the publish queue.

## 🤖 Claude *(02:23:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== publish-social size ===\"; wc -l supabase/functions/publish-social/index.ts 2>/dev/null\necho \"=== auto-publish locations ===\"; ls -d supabase/functions/auto-publish* 2>/dev/null; ls scripts/auto-publish* 2>/dev/null\necho \"=== scheduled posts table migrations ===\"; grep -rlE \"social_posts|scheduled_posts|CREATE TABLE.*posts\" supabase/migrations/ 2>/dev/null | head\necho \"=== creative_assets migration ===\"; ls supabase/migrations/ | grep -iE \"creative_assets|creative-assets\"\necho \"=== social_accounts table ===\"; grep -rl \"CREATE TABLE.*social_accounts\" supabase/migrations/ 2>/dev/null | head",
  "description": "Locate publish-social, auto-publish, scheduled posts queue, creative_assets, social_accounts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === publish-social size ===
> 619 supabase/functions/publish-social/index.ts
> === auto-publish locations ===
> supabase/functions/auto-publish
> scripts/auto-publish-cron.sh
> === scheduled posts table migrations ===
> supabase/migrations/20260527004739_soft_reset_account_rpc.sql
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql
> supabase/migrations/20260626130000_publication_metrics.sql
> supabase/migrations/20260530210000_meta_api_foundation.sql
> supabase/migrations/20260508025933_delete_account_rpc.sql
> supabase/migrations/20260527005036_soft_reset_account_rpc_v2.sql
> === creative_assets migration ===
> 20260625120000_creative_assets_registry.sql
> === social_accounts table ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql
> ```

## 🤖 Claude *(02:23:16)*


## 🤖 Claude *(02:23:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	import { notify } from "../_shared/notify.ts";
> 3	
> 4	const corsHeaders = {
> 5	  "Access-Control-Allow-Origin": "*",
> 6	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 7	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 8	};
> 9	
> 10	Deno.serve(async (req) => {
> 11	  if (req.method === "OPTIONS") {
> 12	    return new Response("ok", { headers: corsHeaders });
> 13	  }
> 14	
> 15	  try {
> 16	    const authHeader = req.headers.get("Authorization");
> 17	    if (!authHeader?.startsWith("Bearer ")) {
> 18	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 19	        status: 401,
> 20	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 21	      });
> 22	    }
> 23	
> 24	    const body = await req.json();
> 25	    const { platform, content, social_account_id, scheduled_post_id, user_id: bodyUserId } = body;
> 26	
> 27	    if (!platform || !content) {
> 28	      return new Response(JSON.stringify({ error: "platform and content required" }), {
> 29	        status: 400,
> 30	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 31	      });
> 32	    }
> 33	
> 34	    const adminClient = createClient(
> 35	      Deno.env.get("SUPABASE_URL")!,
> 36	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!
> 37	    );
> 38	
> 39	    const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 40	    const isServiceRole = authHeader === `Bearer ${serviceKey}`;
> 41	
> 42	    // Resolve caller identity:
> 43	    // - User JWT (frontend): auth.getUser() returns a user
> 44	    // - Service role (auto-publish cron): auth.getUser() returns null; trust user_id from body
> 45	    //   since Supabase infrastructure already validated the JWT signature
> 46	    const supabase = createClient(
> 47	      Deno.env.get("SUPABASE_URL")!,
> 48	      (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
> 49	      { global: { headers: { Authorization: authHeader } } }
> 50	    );
> 51	    const { data: { user } } = await supabase.auth.getUser();
> 52	
> 53	    let userId: string;
> 54	    if (user) {
> 55	      userId = user.id;
> 56	    } else if (isServiceRole && bodyUserId) {
> 57	      userId = bodyUserId;
> 58	    } else {
> 59	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 60	        status: 401,
> 61	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 62	      });
> 63	    }
> 64	
> 65	    let query = adminClient
> 66	      .from("decrypted_social_accounts")
> 67	      .select("*")
> 68	      .eq("user_id", userId)
> 69	      .eq("platform", platform)
> 70	      .eq("is_active", true);
> 71	
> 72	    if (social_account_id) query = query.eq("id", social_account_id);
> 73	
> 74	    const { data: accounts, error: accError } = await query.limit(1).single();
> 75	    if (accError || !accounts) {
> 76	      return new Response(JSON.stringify({ error: `No active ${platform} account found` }), {
> 77	        status: 404,
> 78	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 79	      });
> 80	    }
> 81	
> 82	    const account = accounts;
> 83	
> 84	    // Refresh token if expired, then re-fetch account to get the new access_token
> 85	    if (account.token_expires_at && new Date(account.token_expires_at) < new Date()) {
> 86	      const refreshRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/refresh-social-token`, {
> 87	        method: "POST",
> 88	        headers: {
> 89	          "Content-Type": "application/json",
> 90	          Authorization: `Bearer ${(Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))}`,
> 91	        },
> 92	        body: JSON.stringify({ social_account_id: account.id }),
> 93	      });
> 94	      if (!refreshRes.ok) {
> 95	        return new Response(JSON.stringify({ error: "Token expired and refresh failed" }), {
> 96	          status: 401,
> 97	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 98	        });
> 99	      }
> 100	      // refresh-social-token updates the DB but does not return the token;
> 101	      // re-fetch to get the updated access_token
> 102	      const { data: refreshedAccount } = await adminClient
> 103	        .from("decrypted_social_accounts")
> 104	        .select("access_token, refresh_token, token_expires_at")
> 105	        .eq("id", account.id)
> 106	        .single();
> 107	      if (refreshedAccount) {
> 108	        account.access_token = refreshedAccount.access_token;
> 109	        account.token_expires_at = refreshedAccount.token_expires_at;
> 110	      }
> 111	    }
> 112	
> 113	    let result: any;
> 114	
> 115	    // Best-effort materiality telemetry (Lei 1 / FR-PE-016) — fire-and-forget so a logging hiccup
> 116	    // never blocks a publish. Mirrors the publish-meta pulse pattern (service='publish-<platform>').
> 117	    const pulse = (status: "ok" | "degraded" | "error", event?: string, metadata?: Record<string, unknown>) =>
> 118	      adminClient
> 119	        .from("infra_health_logs")
> 120	        .insert({ service: `publish-${platform}`, status, event: event ?? null, metadata: metadata ?? {} })
> 121	        .then(() => {}, () => {});
> 122	
> 123	    if (platform === "linkedin") {
> 124	      const res = await fetch("https://api.linkedin.com/v2/ugcPosts", {
> 125	        method: "POST",
> 126	        headers: {
> 127	          Authorization: `Bearer ${account.access_token}`,
> 128	          "Content-Type": "application/json",
> 129	          "X-Restli-Protocol-Version": "2.0.0",
> 130	        },
> 131	        body: JSON.stringify({
> 132	          author: `urn:li:person:${account.platform_user_id}`,
> 133	          lifecycleState: "PUBLISHED",
> 134	          specificContent: {
> 135	            "com.linkedin.ugc.ShareContent": {
> 136	              shareCommentary: { text: content.text || content },
> 137	              shareMediaCategory: "NONE",
> 138	            },
> 139	          },
> 140	          visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" },
> 141	        }),
> 142	      });
> 143	      result = await res.json();
> 144	      if (!res.ok) {
> 145	        console.error("LinkedIn publish error:", res.status, result);
> 146	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 147	      }
> 148	
> 149	    } else if (platform === "instagram") {
> 150	      // Instagram Business Login token (instagram_business_content_publish) publishes via graph.INSTAGRAM.com —
> 151	      // NOT graph.facebook.com (that base needs a Page token). video_url → REELS (Fatia 2: vídeo do ecossistema
> 152	      // vira Reel pela conexão IG que JÁ existe — sem app/token manual).
> 153	      const IG_BASE = "https://graph.instagram.com/v21.0";
> 154	      // The stored platform_user_id can be an app-scoped id that the publishing endpoint rejects (code 100/33).
> 155	      // The token's own /me?fields=user_id is the correct content-publishing id — resolve it at publish time.
> 156	      const meRes = await fetch(`${IG_BASE}/me?fields=user_id&access_token=${account.access_token}`);
> 157	      const me = await meRes.json().catch(() => ({}));
> 158	      const igAccountId = me.user_id ?? account.platform_user_id;
> 159	      const videoUrl = content.video_url;
> 160	      const createRes = await fetch(
> 161	        `${IG_BASE}/${igAccountId}/media`,
> 162	        {
> 163	          method: "POST",
> 164	          headers: { "Content-Type": "application/json" },
> 165	          body: JSON.stringify(
> 166	            videoUrl
> 167	              ? { media_type: "REELS", video_url: videoUrl, caption: content.text || content, access_token: account.access_token }
> 168	              : { caption: content.text || content, image_url: content.image_url, access_token: account.access_token },
> 169	          ),
> 170	        }
> 171	      );
> 172	      const container = await createRes.json();
> 173	      if (!createRes.ok) {
> 174	        console.error("Instagram media create error:", createRes.status, container);
> 175	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 176	      }
> 177	
> 178	      // REELS transcode is async — poll the container until FINISHED before publishing (≤ ~90s; short clips finish fast).
> 179	      if (videoUrl) {
> 180	        for (let i = 0; i < 30; i++) {
> 181	          const st = await fetch(`${IG_BASE}/${container.id}?fields=status_code&access_token=${account.access_token}`);
> 182	          const stData = await st.json().catch(() => ({}));
> 183	          if (stData.status_code === "FINISHED") break;
> 184	          if (stData.status_code === "ERROR") throw new Error("IG_REELS_CONTAINER_ERROR");
> 185	          await new Promise((r) => setTimeout(r, 3000));
> 186	        }
> 187	      }
> 188	
> 189	      const pubRes = await fetch(
> 190	        `${IG_BASE}/${igAccountId}/media_publish`,
> 191	        {
> 192	          method: "POST",
> 193	          headers: { "Content-Type": "application/json" },
> 194	          body: JSON.stringify({
> 195	            creation_id: container.id,
> 196	            access_token: account.access_token,
> 197	          }),
> 198	        }
> 199	      );
> 200	      result = await pubRes.json();
> 201	      if (!pubRes.ok) {
> 202	        console.error("Instagram publish error:", pubRes.status, result);
> 203	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 204	      }
> 205	
> 206	    } else if (platform === "facebook") {
> 207	      const pageId = account.platform_user_id;
> 208	      const res = await fetch(
> 209	        `https://graph.facebook.com/v19.0/${pageId}/feed`,
> 210	        {
> 211	          method: "POST",
> 212	          headers: { "Content-Type": "application/json" },
> 213	          body: JSON.stringify({
> 214	            message: content.text || content,
> 215	            access_token: account.access_token,
> 216	          }),
> 217	        }
> 218	      );
> 219	      result = await res.json();
> 220	      if (!res.ok) {
> 221	        console.error("Facebook publish error:", res.status, result);
> 222	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 223	      }
> 224	
> 225	    } else if (platform === "twitter") {
> 226	      const res = await fetch("https://api.x.com/2/tweets", {
> 227	        method: "POST",
> 228	        headers: {
> 229	          Authorization: `Bearer ${account.access_token}`,
> 230	          "Content-Type": "application/json",
> 231	        },
> 232	        body: JSON.stringify({
> 233	          text: content.text || content,
> 234	        }),
> 235	      });
> 236	      result = await res.json();
> 237	      if (!res.ok) {
> 238	        console.error("Twitter publish error:", res.status, result);
> 239	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 240	      }
> 241	
> 242	    } else if (platform === "tiktok") {
> 243	      // TikTok Content Posting API — Direct Post, FILE_UPLOAD (the Supabase signed URL does NOT pass the
> 244	      // PULL_FROM_URL domain-ownership check, so we transfer the bytes ourselves). User access_token only —
> 245	      // publishing needs no client_secret. Mirrors the IG REELS create→poll→publish shape. video_url from payload.
> 246	      const TIKTOK_BASE = "https://open.tiktokapis.com";
> 247	      const videoUrl = content.video_url;
> 248	      if (!videoUrl) {
> 249	        pulse("degraded", "tiktok_no_video");
> 250	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 251	      }
> 252	
> 253	      // (1) Pre-flight creator_info — pick a privacy_level that the (possibly unaudited) account actually allows.
> 254	      const ciRes = await fetch(`${TIKTOK_BASE}/v2/post/publish/creator_info/query/`, {
> 255	        method: "POST",
> 256	        headers: {
> 257	          Authorization: `Bearer ${account.access_token}`,
> 258	          "Content-Type": "application/json; charset=UTF-8",
> 259	        },
> 260	      });
> 261	      const creatorInfo = await ciRes.json();
> 262	      if (!ciRes.ok) {
> 263	        console.error("TikTok creator_info error:", ciRes.status, creatorInfo);
> 264	        pulse("error", "tiktok_creator_info_failed", { status: ciRes.status });
> 265	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 266	      }
> 267	      const privacyOptions: string[] = creatorInfo?.data?.privacy_level_options ?? [];
> 268	      // Prefer public when available (post-audit). Otherwise an UNAUDITED client can ONLY post as
> 269	      // SELF_ONLY — TikTok rejects FOLLOWER_OF_CREATOR / MUTUAL_FOLLOW_FRIENDS with
> 270	      // `unaudited_client_can_only_post_to_private_accounts` (proven 2026-06-27). So fall back to
> 271	      // SELF_ONLY explicitly, NOT to privacyOptions[0] (which is FOLLOWER_OF_CREATOR on a private acct).
> 272	      const privacyLevel =
> 273	        privacyOptions.find((p) => p === "PUBLIC_TO_EVERYONE") ??
> 274	        privacyOptions.find((p) => p === "SELF_ONLY") ??
> 275	        privacyOptions[0] ??
> 276	        "SELF_ONLY";
> 277	
> 278	      // Fetch the MP4 bytes once (FILE_UPLOAD requires the exact size up-front).
> 279	      const mp4Res = await fetch(videoUrl);
> 280	      if (!mp4Res.ok) {
> 281	        console.error("TikTok video fetch error:", mp4Res.status);
> 282	        pulse("error", "tiktok_video_fetch_failed", { status: mp4Res.status });
> 283	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 284	      }
> 285	      const videoBytes = new Uint8Array(await mp4Res.arrayBuffer());
> 286	      const videoSize = videoBytes.byteLength;
> 287	      // Single-chunk transfer (HyperFrames clips are well under the 64MB chunk ceiling / <128MB final).
> 288	      const chunkSize = videoSize;
> 289	      const totalChunkCount = 1;
> 290	
> 291	      // IDEMPOTENCY NOTE: /video/init/ mints a fresh publish_id every call — re-running this branch on a
> 292	      // transient retry WITHOUT an external content/run-id guard would double-post. The caller is expected to
> 293	      // gate re-publish on scheduled_post_id/content state; do NOT re-init blindly inside a retry loop.
> 294	      const initRes = await fetch(`${TIKTOK_BASE}/v2/post/publish/video/init/`, {
> 295	        method: "POST",
> 296	        headers: {
> 297	          Authorization: `Bearer ${account.access_token}`,
> 298	          "Content-Type": "application/json; charset=UTF-8",
> 299	        },
> 300	        body: JSON.stringify({
> 301	          post_info: {
> 302	            title: (content.text || content)?.toString()?.slice(0, 2200) ?? "",
> 303	            privacy_level: privacyLevel,
> 304	            is_aigc: true, // AIGC disclosure is mandatory for AI-generated persona content (compliance).
> 305	          },
> 306	          source_info: {
> 307	            source: "FILE_UPLOAD",
> 308	            video_size: videoSize,
> 309	            chunk_size: chunkSize,
> 310	            total_chunk_count: totalChunkCount,
> 311	          },
> 312	        }),
> 313	      });
> 314	      const initData = await initRes.json();
> 315	      if (!initRes.ok || !initData?.data?.upload_url || !initData?.data?.publish_id) {
> 316	        console.error("TikTok init error:", initRes.status, initData);
> 317	        pulse("error", "tiktok_init_failed", { status: initRes.status });
> 318	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 319	      }
> 320	      const uploadUrl: string = initData.data.upload_url;
> 321	      const publishId: string = initData.data.publish_id;
> 322	
> 323	      // (3) PUT the bytes to the returned upload_url with a Content-Range (single chunk = whole file).
> 324	      const putRes = await fetch(uploadUrl, {
> 325	        method: "PUT",
> 326	        headers: {
> 327	          "Content-Type": "video/mp4",
> 328	          "Content-Range": `bytes 0-${videoSize - 1}/${videoSize}`,
> 329	        },
> 330	        body: videoBytes,
> 331	      });
> 332	      if (!putRes.ok) {
> 333	        console.error("TikTok upload PUT error:", putRes.status);
> 334	        pulse("error", "tiktok_upload_failed", { status: putRes.status });
> 335	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 336	      }
> 337	
> 338	      // (4) Poll status until PUBLISH_COMPLETE. publicaly_available_post_id may stay null pre-audit (SELF_ONLY).
> 339	      let publishStatus = "";
> 340	      let publicPostId: string | null = null;
> 341	      for (let i = 0; i < 30; i++) {
> 342	        const stRes = await fetch(`${TIKTOK_BASE}/v2/post/publish/status/fetch/`, {
> 343	          method: "POST",
> 344	          headers: {
> 345	            Authorization: `Bearer ${account.access_token}`,
> 346	            "Content-Type": "application/json; charset=UTF-8",
> 347	          },
> 348	          body: JSON.stringify({ publish_id: publishId }),
> 349	        });
> 350	        const stData = await stRes.json().catch(() => ({}));
> 351	        publishStatus = stData?.data?.status ?? "";
> 352	        const publicIds: string[] = stData?.data?.publicaly_available_post_id ?? [];
> 353	        if (publicIds.length) publicPostId = publicIds[0];
> 354	        if (publishStatus === "PUBLISH_COMPLETE") break;
> 355	        if (publishStatus === "FAILED") {
> 356	          console.error("TikTok publish failed:", stData?.data?.fail_reason, stData);
> 357	          pulse("error", "tiktok_publish_failed", { fail_reason: stData?.data?.fail_reason ?? null });
> 358	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 359	        }
> 360	        await new Promise((r) => setTimeout(r, 3000));
> 361	      }
> 362	      if (publishStatus !== "PUBLISH_COMPLETE") {
> 363	        pulse("degraded", "tiktok_publish_timeout", { publish_id: publishId });
> 364	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 365	      }
> 366	      // Materiality (Lei 1): PUBLISH_COMPLETE proves transport; the public id is null until the account is
> 367	      // audited (SELF_ONLY) — that's expected and NOT a failure.
> 368	      result = { id: publicPostId, publish_id: publishId, status: publishStatus };
> 369	      pulse("ok", "tiktok_publish_complete", { publish_id: publishId, public: publicPostId !== null });
> 370	
> 371	    } else if (platform === "youtube") {
> 372	      // YouTube Data API v3 videos.insert — resumable upload (no remote ingest → fetch the signed bytes, then
> 373	      // PUT). User access_token only (publishing needs no client_secret). Shorts is implicit (9:16 + ≤3min).
> 374	      const videoUrl = content.video_url;
> 375	      if (!videoUrl) {
> 376	        pulse("degraded", "youtube_no_video");
> 377	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 378	      }
> 379	      const mp4Res = await fetch(videoUrl);
> 380	      if (!mp4Res.ok) {
> 381	        console.error("YouTube video fetch error:", mp4Res.status);
> 382	        pulse("error", "youtube_video_fetch_failed", { status: mp4Res.status });
> 383	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 384	      }
> 385	      const videoBytes = new Uint8Array(await mp4Res.arrayBuffer());
> 386	      const videoSize = videoBytes.byteLength;
> 387	
> 388	      // (1) Initiate the resumable session.
> 389	      const initRes = await fetch(
> 390	        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
> 391	        {
> 392	          method: "POST",
> 393	          headers: {
> 394	            Authorization: `Bearer ${account.access_token}`,
> 395	            "Content-Type": "application/json; charset=UTF-8",
> 396	            "X-Upload-Content-Length": String(videoSize),
> 397	            "X-Upload-Content-Type": "video/mp4",
> 398	          },
> 399	          body: JSON.stringify({
> 400	            snippet: {
> 401	              title: (content.text || content)?.toString()?.slice(0, 100) || "Gabriel AI",
> 402	              description: typeof content === "object" && content?.text ? String(content.text) : "",
> 403	              categoryId: "22",
> 404	            },
> 405	            status: {
> 406	              privacyStatus: "public",
> 407	              selfDeclaredMadeForKids: false,
> 408	              containsSyntheticMedia: true, // AIGC disclosure is mandatory for AI-generated content (compliance).
> 409	            },
> 410	          }),
> 411	        }
> 412	      );
> 413	      if (!initRes.ok) {
> 414	        const initErr = await initRes.json().catch(() => ({}));
> 415	        console.error("YouTube resumable init error:", initRes.status, initErr);
> 416	        pulse("error", "youtube_init_failed", { status: initRes.status });
> 417	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 418	      }
> 419	      // (2) Capture the session URI from the Location header.
> 420	      const sessionUri = initRes.headers.get("Location");
> 421	      if (!sessionUri) {
> 422	        pulse("error", "youtube_no_session_uri");
> 423	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 424	      }
> 425	
> 426	      // (3) PUT the bytes to the session URI.
> 427	      const putRes = await fetch(sessionUri, {
> 428	        method: "PUT",
> 429	        headers: { "Content-Type": "video/mp4", "Content-Length": String(videoSize) },
> 430	        body: videoBytes,
> 431	      });
> 432	      const putData = await putRes.json().catch(() => ({}));
> 433	      // (4) Success = 201 with the video resource id.
> 434	      if (putRes.status !== 200 && putRes.status !== 201) {
> 435	        console.error("YouTube upload PUT error:", putRes.status, putData);
> 436	        pulse("error", "youtube_upload_failed", { status: putRes.status });
> 437	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 438	      }
> 439	      const videoId: string | undefined = putData?.id;
> 440	      if (!videoId) {
> 441	        pulse("error", "youtube_no_video_id");
> 442	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 443	      }
> 444	
> 445	      // Materiality (Lei 1): a 201 does NOT mean public — an unaudited project FORCES the upload to private,
> 446	      // ignoring the requested privacyStatus. Read back the REAL status; never assume 'public'.
> 447	      let realPrivacyStatus: string | null = null;
> 448	      const statusRes = await fetch(
> 449	        `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&part=status`,
> 450	        { headers: { Authorization: `Bearer ${account.access_token}` } }
> 451	      );
> 452	      const statusData = await statusRes.json().catch(() => ({}));
> 453	      realPrivacyStatus = statusData?.items?.[0]?.status?.privacyStatus ?? null;
> 454	
> 455	      result = { id: videoId, privacyStatus: realPrivacyStatus };
> 456	      pulse("ok", "youtube_upload_complete", { video_id: videoId, privacy_status: realPrivacyStatus });
> 457	
> 458	    } else if (platform === "pinterest") {
> 459	      // Pinterest API v5 — video pin (register → upload multipart → poll → create). User access_token only for
> 460	      // pin/board/media REST; the multipart upload itself carries NO Authorization (presigned S3 POST). video_url
> 461	      // from payload; cover_image_url must be a PUBLIC https URL (Pinterest fetches it async).
> 462	      const PIN_BASE = "https://api.pinterest.com/v5";
> 463	      const videoUrl = content.video_url;
> 464	      if (!videoUrl) {
> 465	        pulse("degraded", "pinterest_no_video");
> 466	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 467	      }
> 468	      const pinHeaders = {
> 469	        Authorization: `Bearer ${account.access_token}`,
> 470	        "Content-Type": "application/json",
> 471	      };
> 472	
> 473	      // (0) Ensure a destination board — prefer a cached metadata.board_id, else the first existing board, else
> 474	      // create one once. (Do NOT create a board per run.)
> 475	      let boardId: string | null = account.metadata?.board_id ?? null;
> 476	      if (!boardId) {
> 477	        const boardsRes = await fetch(`${PIN_BASE}/boards`, { headers: pinHeaders });
> 478	        const boardsData = await boardsRes.json().catch(() => ({}));
> 479	        if (!boardsRes.ok) {
> 480	          console.error("Pinterest boards list error:", boardsRes.status, boardsData);
> 481	          pulse("error", "pinterest_boards_failed", { status: boardsRes.status });
> 482	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 483	        }
> 484	        boardId = boardsData?.items?.[0]?.id ?? null;
> 485	        if (!boardId) {
> 486	          const createBoardRes = await fetch(`${PIN_BASE}/boards`, {
> 487	            method: "POST",
> 488	            headers: pinHeaders,
> 489	            body: JSON.stringify({ name: "Gabriel AI", privacy: "PUBLIC" }),
> 490	          });
> 491	          const createBoardData = await createBoardRes.json().catch(() => ({}));
> 492	          if (!createBoardRes.ok || !createBoardData?.id) {
> 493	            console.error("Pinterest board create error:", createBoardRes.status, createBoardData);
> 494	            pulse("error", "pinterest_board_create_failed", { status: createBoardRes.status });
> 495	            throw new Error("PLATFORM_PUBLISH_FAILED");
> 496	          }
> 497	          boardId = createBoardData.id;
> 498	        }
> 499	      }
> 500	
> 501	      // (1) Register the media upload → media_id + upload_url + upload_parameters.
> 502	      const mediaRes = await fetch(`${PIN_BASE}/media`, {
> 503	        method: "POST",
> 504	        headers: pinHeaders,
> 505	        body: JSON.stringify({ media_type: "video" }),
> 506	      });
> 507	      const mediaData = await mediaRes.json().catch(() => ({}));
> 508	      if (!mediaRes.ok || !mediaData?.media_id || !mediaData?.upload_url) {
> 509	        console.error("Pinterest media register error:", mediaRes.status, mediaData);
> 510	        pulse("error", "pinterest_media_register_failed", { status: mediaRes.status });
> 511	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 512	      }
> 513	      const mediaId: string = mediaData.media_id;
> 514	      const uploadUrl: string = mediaData.upload_url;
> 515	      const uploadParams: Record<string, string> = mediaData.upload_parameters ?? {};
> 516	
> 517	      // (2) POST the MP4 to upload_url as multipart/form-data — ALL upload_parameters VERBATIM and the file LAST,
> 518	      // with NO Authorization header (presigned POST). Success = 204.
> 519	      const mp4Res = await fetch(videoUrl);
> 520	      if (!mp4Res.ok) {
> 521	        console.error("Pinterest video fetch error:", mp4Res.status);
> 522	        pulse("error", "pinterest_video_fetch_failed", { status: mp4Res.status });
> 523	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 524	      }
> 525	      const videoBlob = await mp4Res.blob();
> 526	      const form = new FormData();
> 527	      for (const [k, v] of Object.entries(uploadParams)) form.append(k, v);
> 528	      form.append("file", videoBlob); // file field MUST be last (presigned-POST ordering).
> 529	      const uploadRes = await fetch(uploadUrl, { method: "POST", body: form });
> 530	      if (uploadRes.status !== 204 && !uploadRes.ok) {
> 531	        console.error("Pinterest media upload error:", uploadRes.status);
> 532	        pulse("error", "pinterest_upload_failed", { status: uploadRes.status });
> 533	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 534	      }
> 535	
> 536	      // (3) Poll the media until status='succeeded'.
> 537	      let mediaStatus = "";
> 538	      for (let i = 0; i < 30; i++) {
> 539	        const stRes = await fetch(`${PIN_BASE}/media/${mediaId}`, { headers: pinHeaders });
> 540	        const stData = await stRes.json().catch(() => ({}));
> 541	        mediaStatus = stData?.status ?? "";
> 542	        if (mediaStatus === "succeeded") break;
> 543	        if (mediaStatus === "failed") {
> 544	          console.error("Pinterest media processing failed:", stData);
> 545	          pulse("error", "pinterest_media_failed", { media_id: mediaId });
> 546	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 547	        }
> 548	        await new Promise((r) => setTimeout(r, 3000));
> 549	      }
> 550	      if (mediaStatus !== "succeeded") {
> 551	        pulse("degraded", "pinterest_media_timeout", { media_id: mediaId });
> 552	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 553	      }
> 554	
> 555	      // (4) Create the pin. cover_image_url must be a PUBLIC https URL (Pinterest fetches it async).
> 556	      const coverImageUrl = content.cover_image_url || content.image_url || videoUrl;
> 557	      const pinRes = await fetch(`${PIN_BASE}/pins`, {
> 558	        method: "POST",
> 559	        headers: pinHeaders,
> 560	        body: JSON.stringify({
> 561	          board_id: boardId,
> 562	          title: (content.text || content)?.toString()?.slice(0, 100) ?? "",
> 563	          description: typeof content === "object" && content?.text ? String(content.text).slice(0, 800) : "",
> 564	          media_source: {
> 565	            source_type: "video_id",
> 566	            media_id: mediaId,
> 567	            cover_image_url: coverImageUrl,
> 568	          },
> 569	        }),
> 570	      });
> 571	      result = await pinRes.json();
> 572	      if (!pinRes.ok) {
> 573	        console.error("Pinterest pin create error:", pinRes.status, result);
> 574	        pulse("error", "pinterest_pin_create_failed", { status: pinRes.status });
> 575	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 576	      }
> 577	      // Materiality (Lei 1): under Trial the pin is sandbox/creator-only (no public URL) — a 201 proves
> 578	      // transport, not live reach. Honest 'live' claim waits for Standard tier.
> 579	      pulse("ok", "pinterest_pin_created", { pin_id: result?.id ?? null, board_id: boardId });
> 580	
> 581	    } else {
> 582	      return new Response(JSON.stringify({ error: `Publishing to ${platform} not yet supported` }), {
> 583	        status: 400,
> 584	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 585	      });
> 586	    }
> 587	
> 588	    if (scheduled_post_id) {
> 589	      await adminClient
> 590	        .from("scheduled_posts")
> 591	        .update({
> 592	          status: "published",
> 593	          published_at: new Date().toISOString(),
> 594	          platform_post_id: result.id || result.data?.id || result["X-RestLi-Id"],
> 595	        })
> 596	        .eq("id", scheduled_post_id);
> 597	    }
> 598	
> 599	    // In-app notification (best-effort) — the user sees publishes in the bell (P0 notifications).
> 600	    const platformLabel = platform === "instagram" ? "Instagram" : platform === "linkedin" ? "LinkedIn" : platform;
> 601	    await notify(adminClient, userId, {
> 602	      type: "success",
> 603	      title: `Publicado no ${platformLabel}`,
> 604	      message: typeof content === "object" && content?.text ? String(content.text).slice(0, 120) : null,
> 605	      action_url: "/dashboard/social",
> 606	      metadata: { platform, post_id: result?.id ?? null },
> 607	    });
> 608	
> 609	    return new Response(JSON.stringify({ success: true, result }), {
> 610	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 611	    });
> 612	  } catch (err) {
> 613	    console.error("publish-social error:", err);
> 614	    return new Response(
> 615	      JSON.stringify({ error: "Falha ao publicar. Tente novamente em instantes." }),
> 616	      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 617	    );
> 618	  }
> 619	});
> 620	
> ```

## 🤖 Claude *(02:23:50)*


## 🤖 Claude *(02:23:52)*

`publish-social` is clear and first-hand now. Critical finding already: of the 7 video-spine surfaces, only **IG, TikTok, YouTube, Pinterest** actually publish video today — **LinkedIn, Facebook, Twitter/X branches are text-only** (no video/image/thread). That's the honest gap the reshaper exposes. Also `channel='twitter_x'` but publish-social expects `'twitter'` (name mapping needed). Let me read the queue (`scheduled_posts`) and `auto-publish` cron — the drip mechanism the reshaper must feed.

## 🤖 Claude *(02:23:53)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	
> 3	const corsHeaders = {
> 4	  "Access-Control-Allow-Origin": "*",
> 5	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 6	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token",
> 7	};
> 8	
> 9	Deno.serve(async (req) => {
> 10	  if (req.method === "OPTIONS") {
> 11	    return new Response("ok", { headers: corsHeaders });
> 12	  }
> 13	
> 14	  try {
> 15	    const adminClient = createClient(
> 16	      Deno.env.get("SUPABASE_URL")!,
> 17	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!
> 18	    );
> 19	
> 20	    // Find all queued posts where scheduled_at <= now
> 21	    const { data: duePosts, error } = await adminClient
> 22	      .from("scheduled_posts")
> 23	      .select("*")
> 24	      .eq("status", "queued")
> 25	      .lte("scheduled_at", new Date().toISOString())
> 26	      .order("scheduled_at")
> 27	      .limit(50);
> 28	
> 29	    if (error) {
> 30	      console.error("Error fetching due posts:", error);
> 31	      return new Response(JSON.stringify({ error: error.message }), {
> 32	        status: 500,
> 33	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 34	      });
> 35	    }
> 36	
> 37	    if (!duePosts || duePosts.length === 0) {
> 38	      return new Response(JSON.stringify({ processed: 0, message: "No posts due" }), {
> 39	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 40	      });
> 41	    }
> 42	
> 43	    const results: Array<{ id: string; status: string; error?: string }> = [];
> 44	
> 45	    for (const post of duePosts) {
> 46	      try {
> 47	        // Mark as publishing
> 48	        await adminClient
> 49	          .from("scheduled_posts")
> 50	          .update({ status: "publishing" })
> 51	          .eq("id", post.id);
> 52	
> 53	        // Get the content body if content_id exists
> 54	        let contentText = "";
> 55	        if (post.content_id) {
> 56	          const { data: content } = await adminClient
> 57	            .from("content_library")
> 58	            .select("body, title")
> 59	            .eq("id", post.content_id)
> 60	            .single();
> 61	          contentText = content?.body || content?.title || "";
> 62	        }
> 63	
> 64	        if (!contentText) {
> 65	          contentText = `Post agendado para ${post.platform}`;
> 66	        }
> 67	
> 68	        // ── FR-PE-011: video transport gap. The scheduled post's content_id points at the TEXT row; the 9:16 render
> 69	        // (video-bridge.ts) lands as a SEPARATE content_library row (type='video', media_url = a path inside the
> 70	        // private `video-studio-assets` bucket — metadata.storage_bucket) sharing this post's campaign_id. Resolve
> 71	        // that sibling and sign it to a LONG-TTL URL so the URL survives Pinterest/IG's async fetch (a 1h signed URL
> 72	        // dies before the publish window). Pass it as content.video_url → publish-social's REELS/TikTok/YouTube/Pin
> 73	        // video branches. Text-only posts keep the plain-string path UNCHANGED (no campaign_id / no video sibling).
> 74	        let videoUrl: string | null = null;
> 75	        if (post.campaign_id) {
> 76	          try {
> 77	            const { data: vid } = await adminClient
> 78	              .from("content_library")
> 79	              .select("media_url, metadata")
> 80	              .eq("campaign_id", post.campaign_id)
> 81	              .eq("type", "video")
> 82	              .eq("status", "approved")
> 83	              .order("created_at", { ascending: false })
> 84	              .limit(1)
> 85	              .maybeSingle();
> 86	            const storageKey = vid?.media_url as string | undefined;
> 87	            if (storageKey) {
> 88	              const bucket = (vid?.metadata as { storage_bucket?: string } | null)?.storage_bucket || "video-studio-assets";
> 89	              if (/^https?:\/\//i.test(storageKey)) {
> 90	                videoUrl = storageKey; // already a public URL — pass through
> 91	              } else {
> 92	                // 6h TTL — outlives the async pull (cover/video fetch) on Pinterest/IG. Private bucket → re-sign on read.
> 93	                const { data: signed } = await adminClient.storage
> 94	                  .from(bucket)
> 95	                  .createSignedUrl(storageKey, 21600);
> 96	                videoUrl = signed?.signedUrl ?? null;
> 97	              }
> 98	            }
> 99	          } catch (e) {
> 100	            console.warn(`[auto-publish] video_url resolve skipped for post ${post.id}:`, e instanceof Error ? e.message : e);
> 101	          }
> 102	        }
> 103	
> 104	        // content stays a bare string for text-only posts (publish-social reads `content.text || content`); when a
> 105	        // video sibling resolved, send the object shape so the platform's video branch fires with video_url.
> 106	        const contentPayload = videoUrl ? { text: contentText, video_url: videoUrl } : contentText;
> 107	
> 108	        // Call publish-social
> 109	        const publishRes = await fetch(
> 110	          `${Deno.env.get("SUPABASE_URL")}/functions/v1/publish-social`,
> 111	          {
> 112	            method: "POST",
> 113	            headers: {
> 114	              "Content-Type": "application/json",
> 115	              Authorization: `Bearer ${(Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))}`,
> 116	            },
> 117	            body: JSON.stringify({
> 118	              platform: post.platform,
> 119	              content: contentPayload,
> 120	              social_account_id: post.social_account_id,
> 121	              scheduled_post_id: post.id,
> 122	              user_id: post.user_id,
> 123	            }),
> 124	          }
> 125	        );
> 126	
> 127	        if (publishRes.ok) {
> 128	          results.push({ id: post.id, status: "published" });
> 129	        } else {
> 130	          const errBody = await publishRes.json().catch(() => ({ error: "Unknown" }));
> 131	          const retryCount = (post.retry_count || 0) + 1;
> 132	          const maxRetries = post.max_retries || 3;
> 133	
> 134	          await adminClient
> 135	            .from("scheduled_posts")
> 136	            .update({
> 137	              status: retryCount >= maxRetries ? "failed" : "queued",
> 138	              retry_count: retryCount,
> 139	              error_message: errBody.error || "Publish failed",
> 140	            })
> 141	            .eq("id", post.id);
> 142	
> 143	          results.push({ id: post.id, status: "failed", error: errBody.error });
> 144	        }
> 145	      } catch (e) {
> 146	        const retryCount = (post.retry_count || 0) + 1;
> 147	        await adminClient
> 148	          .from("scheduled_posts")
> 149	          .update({
> 150	            status: retryCount >= (post.max_retries || 3) ? "failed" : "queued",
> 151	            retry_count: retryCount,
> 152	            error_message: e instanceof Error ? e.message : String(e),
> 153	          })
> 154	          .eq("id", post.id);
> 155	
> 156	        results.push({ id: post.id, status: "error", error: e instanceof Error ? e.message : String(e) });
> 157	      }
> 158	    }
> 159	
> 160	    return new Response(
> 161	      JSON.stringify({ processed: results.length, results }),
> 162	      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 163	    );
> 164	  } catch (err) {
> 165	    console.error("auto-publish error:", err);
> 166	    return new Response(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }), {
> 167	      status: 500,
> 168	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 169	    });
> 170	  }
> 171	});
> 172	
> ```

## 🤖 Claude *(02:24:19)*


## 🤖 Claude *(02:24:23)*

Now the queue is fully clear. **Key architectural insight**: `auto-publish` currently derives ONE generic text (from `content_library` by `content_id`) + ONE video (sibling by `campaign_id`) and sends them to *every* platform — that **IS the cross-post penalty trap** the BoK fights. The reshaper fixes this by writing a **per-channel native variant** into the queue.

The cleanest, backward-compatible integration: add a `payload jsonb` override to `scheduled_posts` that `auto-publish` prefers over the generic derivation. Let me ground that by reading the queue schema + `creative_assets` registry (the spine I'll resolve assets from) first-hand, since I'll be ALTERing one of them.

## 🤖 Claude *(02:24:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260625120000_creative_assets_registry.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: creative_assets — the canonical ecosystem ASSET REGISTRY (bidirectional interop spine).
> 2	-- BoK SSOT: docs/processes/creative-assets-registry.md (Lei 2 anticipated process) + the creative-ecosystem
> 3	--           program (project_creative_ecosystem_program). Realizes the Sovereign directive 2026-06-25:
> 4	--           "o poder das saídas" — each module (canvas-studio / hyperframes / open-design / content-pipeline /
> 5	--           generate-image / faceless) writes & reads each other's assets, bidirectionally, with provenance.
> 6	--
> 7	-- DESIGN: a THIN registry/index over EXISTING storage — bytes stay in their current buckets (canvas-assets,
> 8	--   video-studio-assets, generated-images, public). This table only POINTS at them (storage_bucket+storage_key)
> 9	--   and adds: kind, provenance (parent_asset_id chain + mesh_node_id), source attribution, and curation. No data
> 10	--   migration; producers DUAL-WRITE a row on success (fail-soft — never break the producer if registration fails).
> 11	--
> 12	-- TENANCY (mirrors video_renders 20260622040000): SELECT = own row OR an agency row whose org the caller actively
> 13	--   belongs to (public.is_org_member anti-recursion helper). NO INSERT/UPDATE policy for authenticated ⇒ default-deny
> 14	--   writes: register_creative_asset (SECURITY DEFINER, service-role-only) is the ONLY writer. DELETE own allowed
> 15	--   (the registry row; Storage object cleanup is a separate Storage-API concern). org_id NULL = solo creator (§AG).
> 16	
> 17	-- ─────────────────────────────────────────────────────────────────────────────
> 18	-- 1. creative_assets — the asset spine
> 19	-- ─────────────────────────────────────────────────────────────────────────────
> 20	CREATE TABLE IF NOT EXISTS public.creative_assets (
> 21	  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
> 22	  user_id          uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 23	  org_id           uuid        REFERENCES public.organizations(id) ON DELETE CASCADE,  -- NULL = solo (§AG opt-in)
> 24	  kind             text        NOT NULL CHECK (kind IN ('image','video','audio','design','article','template')),
> 25	  storage_bucket   text        NOT NULL,   -- existing bucket: canvas-assets | video-studio-assets | generated-images | public
> 26	  storage_key      text        NOT NULL,   -- object path inside the bucket
> 27	  is_public        boolean     NOT NULL DEFAULT false,  -- public bucket (public URL) vs private (signed URL at read)
> 28	  mime_type        text,
> 29	  file_size_bytes  bigint      CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0),
> 30	  width            int,
> 31	  height           int,
> 32	  duration_seconds numeric     CHECK (duration_seconds IS NULL OR duration_seconds >= 0),
> 33	  parent_asset_id  uuid        REFERENCES public.creative_assets(id) ON DELETE SET NULL,  -- provenance/lineage
> 34	  source_module    text        NOT NULL CHECK (source_module IN
> 35	                     ('canvas-studio','hyperframes','open-design','content-pipeline','generate-image','faceless')),
> 36	  source_job_id    text,        -- polymorphic origin: execution_id | render_id | design_job_id | operation_id
> 37	  mesh_node_id     uuid,        -- mcorch_nodes.id (logical, no FK — the mesh is multi-tenant, prunable)
> 38	  provider         text,
> 39	  model            text,
> 40	  prompt           text,
> 41	  title            text,
> 42	  tags             text[]      NOT NULL DEFAULT '{}',
> 43	  is_favorite      boolean     NOT NULL DEFAULT false,
> 44	  metadata         jsonb       NOT NULL DEFAULT '{}'::jsonb,
> 45	  created_at       timestamptz NOT NULL DEFAULT now(),
> 46	  updated_at       timestamptz NOT NULL DEFAULT now(),
> 47	  -- One Storage object = one asset row (idempotency anchor for dual-write ON CONFLICT).
> 48	  CONSTRAINT creative_assets_uq_object UNIQUE (storage_bucket, storage_key)
> 49	);
> 50	
> 51	ALTER TABLE public.creative_assets ENABLE ROW LEVEL SECURITY;
> 52	
> 53	-- SELECT: own, OR an agency row whose org the caller actively belongs to (anti-recursion helper).
> 54	CREATE POLICY "creative_assets_select_own_or_org" ON public.creative_assets
> 55	  FOR SELECT USING (
> 56	    auth.uid() = user_id
> 57	    OR (org_id IS NOT NULL AND public.is_org_member(org_id))
> 58	  );
> 59	
> 60	-- DELETE own (a user can remove their own asset from the registry). No INSERT/UPDATE policy ⇒ default-deny:
> 61	-- register_creative_asset (service-role) is the only writer, so source_module/user_id can never be forged.
> 62	CREATE POLICY "creative_assets_delete_own" ON public.creative_assets
> 63	  FOR DELETE USING (auth.uid() = user_id);
> 64	
> 65	CREATE INDEX IF NOT EXISTS creative_assets_user_kind_idx   ON public.creative_assets (user_id, kind, created_at DESC);
> 66	CREATE INDEX IF NOT EXISTS creative_assets_user_created_idx ON public.creative_assets (user_id, created_at DESC);
> 67	CREATE INDEX IF NOT EXISTS creative_assets_parent_idx      ON public.creative_assets (parent_asset_id) WHERE parent_asset_id IS NOT NULL;
> 68	CREATE INDEX IF NOT EXISTS creative_assets_source_idx      ON public.creative_assets (source_module, source_job_id);
> 69	CREATE INDEX IF NOT EXISTS creative_assets_mesh_idx        ON public.creative_assets (mesh_node_id) WHERE mesh_node_id IS NOT NULL;
> 70	CREATE INDEX IF NOT EXISTS creative_assets_org_idx         ON public.creative_assets (org_id) WHERE org_id IS NOT NULL;
> 71	
> 72	CREATE TRIGGER tr_update_creative_assets_updated_at
> 73	  BEFORE UPDATE ON public.creative_assets
> 74	  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 75	
> 76	COMMENT ON TABLE public.creative_assets IS
> 77	  'Canonical ecosystem asset registry (bidirectional interop spine). Thin index over existing buckets — bytes stay '
> 78	  'put; modules dual-write. provenance = parent_asset_id chain + mesh_node_id. SELECT own-or-org RLS; DELETE own; '
> 79	  'writes via register_creative_asset (service-role). One Storage object = one row (UNIQUE bucket+key).';
> 80	
> 81	-- ─────────────────────────────────────────────────────────────────────────────
> 82	-- 2. register_creative_asset — the ONLY writer (SECURITY DEFINER, service-role-only, idempotent)
> 83	--    Producers (canvas-execute, video-bridge, generate-image, design-bridge, orchestrate-content) call this
> 84	--    FAIL-SOFT on success. ON CONFLICT (object) refreshes mutable metadata without forging identity.
> 85	-- ─────────────────────────────────────────────────────────────────────────────
> 86	CREATE OR REPLACE FUNCTION public.register_creative_asset(
> 87	  p_user_id          uuid,
> 88	  p_kind             text,
> 89	  p_storage_bucket   text,
> 90	  p_storage_key      text,
> 91	  p_source_module    text,
> 92	  p_source_job_id    text     DEFAULT NULL,
> 93	  p_is_public        boolean  DEFAULT false,
> 94	  p_mime_type        text     DEFAULT NULL,
> 95	  p_file_size_bytes  bigint   DEFAULT NULL,
> 96	  p_width            int      DEFAULT NULL,
> 97	  p_height           int      DEFAULT NULL,
> 98	  p_duration_seconds numeric  DEFAULT NULL,
> 99	  p_parent_asset_id  uuid     DEFAULT NULL,
> 100	  p_mesh_node_id     uuid     DEFAULT NULL,
> 101	  p_provider         text     DEFAULT NULL,
> 102	  p_model            text     DEFAULT NULL,
> 103	  p_prompt           text     DEFAULT NULL,
> 104	  p_title            text     DEFAULT NULL,
> 105	  p_org_id           uuid     DEFAULT NULL,
> 106	  p_tags             text[]   DEFAULT '{}',
> 107	  p_metadata         jsonb    DEFAULT '{}'::jsonb
> 108	)
> 109	RETURNS uuid
> 110	LANGUAGE plpgsql
> 111	SECURITY DEFINER
> 112	SET search_path = ''
> 113	AS $$
> 114	DECLARE
> 115	  v_id uuid;
> 116	BEGIN
> 117	  IF p_user_id IS NULL OR p_storage_bucket IS NULL OR p_storage_key IS NULL THEN
> 118	    RAISE EXCEPTION 'register_creative_asset: user_id, storage_bucket, storage_key required' USING errcode = '22023';
> 119	  END IF;
> 120	  IF p_kind NOT IN ('image','video','audio','design','article','template') THEN
> 121	    RAISE EXCEPTION 'register_creative_asset: invalid kind %', p_kind USING errcode = '22023';
> 122	  END IF;
> 123	  IF p_source_module NOT IN ('canvas-studio','hyperframes','open-design','content-pipeline','generate-image','faceless') THEN
> 124	    RAISE EXCEPTION 'register_creative_asset: invalid source_module %', p_source_module USING errcode = '22023';
> 125	  END IF;
> 126	
> 127	  INSERT INTO public.creative_assets (
> 128	    user_id, org_id, kind, storage_bucket, storage_key, is_public, mime_type, file_size_bytes,
> 129	    width, height, duration_seconds, parent_asset_id, source_module, source_job_id, mesh_node_id,
> 130	    provider, model, prompt, title, tags, metadata
> 131	  ) VALUES (
> 132	    p_user_id, p_org_id, p_kind, p_storage_bucket, p_storage_key, p_is_public, p_mime_type, p_file_size_bytes,
> 133	    p_width, p_height, p_duration_seconds, p_parent_asset_id, p_source_module, p_source_job_id, p_mesh_node_id,
> 134	    p_provider, p_model, p_prompt, p_title, COALESCE(p_tags, '{}'), COALESCE(p_metadata, '{}'::jsonb)
> 135	  )
> 136	  ON CONFLICT (storage_bucket, storage_key) DO UPDATE SET
> 137	    -- Refresh mutable descriptors only; NEVER reassign user_id (tenant) or source_module (provenance integrity).
> 138	    kind            = EXCLUDED.kind,
> 139	    mime_type       = COALESCE(EXCLUDED.mime_type, public.creative_assets.mime_type),
> 140	    file_size_bytes = COALESCE(EXCLUDED.file_size_bytes, public.creative_assets.file_size_bytes),
> 141	    width           = COALESCE(EXCLUDED.width, public.creative_assets.width),
> 142	    height          = COALESCE(EXCLUDED.height, public.creative_assets.height),
> 143	    duration_seconds= COALESCE(EXCLUDED.duration_seconds, public.creative_assets.duration_seconds),
> 144	    parent_asset_id = COALESCE(EXCLUDED.parent_asset_id, public.creative_assets.parent_asset_id),
> 145	    mesh_node_id    = COALESCE(EXCLUDED.mesh_node_id, public.creative_assets.mesh_node_id),
> 146	    title           = COALESCE(EXCLUDED.title, public.creative_assets.title),
> 147	    metadata        = public.creative_assets.metadata || EXCLUDED.metadata,
> 148	    updated_at      = now()
> 149	  WHERE public.creative_assets.user_id = EXCLUDED.user_id   -- never let one tenant's object overwrite another's row
> 150	  RETURNING id INTO v_id;
> 151	
> 152	  RETURN v_id;
> 153	END;
> 154	$$;
> 155	
> 156	REVOKE ALL ON FUNCTION public.register_creative_asset(uuid, text, text, text, text, text, boolean, text, bigint, int, int, numeric, uuid, uuid, text, text, text, text, uuid, text[], jsonb) FROM PUBLIC, anon, authenticated;
> 157	GRANT EXECUTE ON FUNCTION public.register_creative_asset(uuid, text, text, text, text, text, boolean, text, bigint, int, int, numeric, uuid, uuid, text, text, text, text, uuid, text[], jsonb) TO service_role;
> 158	
> ```

## 🤖 Claude *(02:24:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== scheduled_posts schema (grep across migrations) ===\"\ngrep -rn \"scheduled_posts\" supabase/migrations/*.sql | grep -iE \"CREATE TABLE|ADD COLUMN|ALTER TABLE\" | head -40",
  "description": "Read creative_assets registry + find scheduled_posts schema definition"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === scheduled_posts schema (grep across migrations) ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:158:CREATE TABLE public.scheduled_posts (
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:176:ALTER TABLE public.scheduled_posts ENABLE ROW LEVEL SECURITY;
> ```

## 🤖 Claude *(02:24:29)*


## 🤖 Claude *(02:24:30)*

Let me read the exact `scheduled_posts` schema (I'll be ALTERing it) and check the `campaign_id`/`content_id` columns + RLS.

## 🤖 Claude *(02:24:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql",
  "offset": 150,
  "limit": 70
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 150	  version INTEGER DEFAULT 1,
> 151	  is_favorite BOOLEAN DEFAULT FALSE,
> 152	  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
> 153	  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
> 154	);
> 155	ALTER TABLE public.content_library ENABLE ROW LEVEL SECURITY;
> 156	
> 157	-- 11. SCHEDULED POSTS
> 158	CREATE TABLE public.scheduled_posts (
> 159	  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 160	  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 161	  content_id UUID REFERENCES public.content_library(id) ON DELETE SET NULL,
> 162	  campaign_id UUID REFERENCES public.campaigns(id) ON DELETE SET NULL,
> 163	  social_account_id UUID REFERENCES public.social_accounts(id) ON DELETE SET NULL,
> 164	  platform social_platform NOT NULL,
> 165	  scheduled_at TIMESTAMPTZ NOT NULL,
> 166	  published_at TIMESTAMPTZ,
> 167	  status post_status NOT NULL DEFAULT 'queued',
> 168	  platform_post_id TEXT,
> 169	  error_message TEXT,
> 170	  retry_count INTEGER DEFAULT 0,
> 171	  max_retries INTEGER DEFAULT 3,
> 172	  metadata JSONB DEFAULT '{}',
> 173	  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
> 174	  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
> 175	);
> 176	ALTER TABLE public.scheduled_posts ENABLE ROW LEVEL SECURITY;
> 177	
> 178	-- 12. OPTIMIZATION POLICY
> 179	CREATE TABLE public.optimization_policy (
> 180	  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 181	  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 182	  campaign_id UUID REFERENCES public.campaigns(id) ON DELETE SET NULL,
> 183	  action_type TEXT NOT NULL,
> 184	  action_details JSONB NOT NULL DEFAULT '{}',
> 185	  reward NUMERIC(8,4) DEFAULT 0,
> 186	  context JSONB DEFAULT '{}',
> 187	  applied BOOLEAN DEFAULT FALSE,
> 188	  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
> 189	);
> 190	ALTER TABLE public.optimization_policy ENABLE ROW LEVEL SECURITY;
> 191	
> 192	-- 13. HEALING ACTIONS
> 193	CREATE TABLE public.healing_actions (
> 194	  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 195	  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 196	  issue_type TEXT NOT NULL,
> 197	  issue_details TEXT,
> 198	  action_taken TEXT NOT NULL,
> 199	  success BOOLEAN DEFAULT FALSE,
> 200	  related_resource_type TEXT,
> 201	  related_resource_id UUID,
> 202	  metadata JSONB DEFAULT '{}',
> 203	  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
> 204	);
> 205	ALTER TABLE public.healing_actions ENABLE ROW LEVEL SECURITY;
> 206	
> 207	-- 14. AUDIT LOGS
> 208	CREATE TABLE public.audit_logs (
> 209	  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 210	  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 211	  action TEXT NOT NULL,
> 212	  resource_type TEXT NOT NULL,
> 213	  resource_id UUID,
> 214	  details JSONB DEFAULT '{}',
> 215	  ip_address TEXT,
> 216	  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
> 217	);
> 218	ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
> 219	
> ```

## 🤖 Claude *(02:24:48)*


## 🤖 Claude *(02:24:50)*

`scheduled_posts` already has a `metadata jsonb` column and `campaign_id`/`content_id` — so I can carry the native variant payload there with **zero migration on the queue** (lean, per the "deliver value not plumbing" directive). The `platform` is a `social_platform` enum; `channel_profiles.channel='twitter_x'` must map to enum `'twitter'`.

Let me check the workflow's progress on the parts I haven't read first-hand (HyperFrames 16:9, image reframe/format, autopilot scheduler).

## 🤖 Claude *(02:24:51)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskOutput,TaskGet",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskOutput'}, {'type': 'tool_reference', 'tool_name': 'TaskGet'}]
> ```

## 🤖 Claude *(02:24:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== social_platform enum ===\"\ngrep -rn \"social_platform\" supabase/migrations/*.sql | grep -iE \"CREATE TYPE|ENUM|ADD VALUE\" | head\necho \"=== COIN_COSTS ===\"\ngrep -nE \"COIN_COSTS|[A-Z_]+:\\s*[0-9]+\" src/lib/billing.ts | head -40",
  "description": "Find social_platform enum values + COIN_COSTS"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === social_platform enum ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:12:CREATE TYPE public.social_platform AS ENUM ('linkedin', 'instagram', 'facebook', 'twitter', 'tiktok', 'youtube', 'pinterest', 'wordpress');
> === COIN_COSTS ===
> 18:export const COIN_COSTS = {
> 19:  ORCHESTRATION_RUN: 10,   // 3 texts + 1 image, charged flat (bundle discount vs the 15 below). ~4.4× at floor.
> 20:  CONTENT_GENERATION: 2,   // 1 LLM article (~$0.0006). Strict floor is 1; held at 2 as a conservative minimum. (was 5)
> 21:  IMAGE_GENERATION: 9,     // 1 DALL·E 3 1024² image ($0.04 → 4× at floor). WAS 3 = 1.36× (under-margined) → fixed.
> 22:  EMBED_NODE: 1,           // 1 embedding call (~$0.000002). Floor minimum.
> 23:  LEAD_SCORE: 1,           // 1 LLM scoring call (~$0.0005). marketing-hub FR-MH-003 (lead-score edge fn mirrors this).
> 24:  CAMPAIGN_RUN: 10,        // marketing-hub FR-MH-004 — orchestration FEE on top of the cascaded per-step ORCHESTRATION_RUN.
> 25:  NURTURE_DISPATCH: 2,     // marketing-hub FR-MH-008 — 1 LLM message (~$0.0006). nurture-dispatch edge fn mirrors this.
> 27:  // Mirrored from packages/vision-mcp-core/src/infra/billing.ts COIN_COSTS (G3 triple-mirror gate).
> 29:  VISION_DESCRIBE_IMAGE: 2,      // VLM ~$0.0004/img (Gemini Flash) → 4×-floor
> 30:  VISION_ANALYZE_VIDEO: 2,       // per minute (Gemini video @1FPS ~$0.0054/min)
> 31:  VISION_OCR: 1,                 // per page (Mistral OCR ~$0.002)
> 32:  VISION_DETECT: 2,              // Gemini native boxes
> 33:  DEEPSEARCH_SCRAPE: 1,          // Firecrawl (~$0.0006/pág Growth)
> 34:  DEEPSEARCH_RUN: 3,             // deepsearch orchestration
> 35:  MESH_CONSOLIDATE_REFERENCE: 1, // mesh write (embedding async ~free)
> 38:  VIDEO_FACELESS_RENDER: 125,    // faceless E2E pipeline (n8n Gemini→Pollinations→VoxCPM→Remotion→LTX→FFmpeg→QA) ≈ canvas DoP video
> 39:  VIDEO_HYPERFRAMES_RENDER: 12,  // deterministic HTML→MP4 via headless Chrome (no AI legs) ≈ canvas image class
> 42:export type CoinOperation = keyof typeof COIN_COSTS;
> 105:  const cost = COIN_COSTS[operation];
> ```

## 🤖 Claude *(02:25:05)*


## 🤖 Claude *(02:25:06)*

Enum confirmed: `social_platform = (linkedin, instagram, facebook, twitter, tiktok, youtube, pinterest, wordpress)` — so `twitter_x→twitter` mapping is the only rename needed. No atomize/reshape cost in `COIN_COSTS` yet (I'll add lean ones). Now let me collect the workflow map.

## 🤖 Claude *(02:25:06)*


🛠️ **Tool Call**: `TaskOutput`
```json
{
  "task_id": "wj8bku6oe",
  "block": true,
  "timeout": 240000
}
```

> **Tool Result (TaskOutput)** - ✅ Success
>
> ```
> <retrieval_status>timeout</retrieval_status>
> 
> <task_id>wj8bku6oe</task_id>
> 
> <task_type>local_workflow</task_type>
> 
> <status>running</status>
> ```

## 🤖 Claude *(02:29:13)*


## 🤖 Claude *(02:29:14)*

Still running (map + critic phases). Let me wait for it to finish — the HyperFrames 16:9, image-reframe, and scheduler findings are load-bearing for the reshaper's render-dispatch design.

## 🤖 Claude *(02:29:15)*


🛠️ **Tool Call**: `TaskOutput`
```json
{
  "task_id": "wj8bku6oe",
  "block": true,
  "timeout": 300000
}
```

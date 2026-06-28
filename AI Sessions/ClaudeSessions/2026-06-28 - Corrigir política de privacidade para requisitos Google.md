# Corrigir política de privacidade para requisitos Google
**Date:** 2026-06-28 | **Session ID:** `760b6087-837f-483e-be18-bcfc2f4fc89a`

---

## 👤 User *(04:26:31)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(04:26:31)*

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


## 🤖 Claude *(04:26:34)*


## 🤖 Claude *(04:26:35)*

I'll execute the ShakeHands /handson pickup protocol. Starting with pre-flight checks in parallel.

## 🤖 Claude *(04:26:35)*


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
> 6c30136 docs(readme): v6.58.0 badge + neural_mesh 8980 nodes (distribution mapping complete)
> 2116904 chore(deno): lock pdf-lib deps for generate-carousel
> 390eb0a docs(handoff): seal distribution mapping complete — CP-008/010/011 (sem pular nada)
> 293b041 feat(reshaper): PDF carousel generation (FR-CP-009, CP-011 partial)
> 6c3bc66 feat(publish): X thread + FB photo + Pinterest image-pin branches (CP-010 partial)
> 2e4c3fb feat(reshaper): 16:9 YouTube long-form render (FR-CP-004, OTD-CP-008 closed)
> e34a14e docs(handoff): seal reshaper continuation — publish opt-in + image reframe (OTD-CP-009 closed)
> ```

## 🤖 Claude *(04:26:36)*


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

## 🤖 Claude *(04:26:37)*


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

## 🤖 Claude *(04:26:37)*


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

## 🤖 Claude *(04:26:38)*


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
> mcorch_vision_mcp: Up 11 days (healthy)
> mcorch_claude_mem: Up 12 days (healthy)
> mcorch_chroma: Up 12 days (healthy)
> ---
> mega-brain-dashboard: Up 12 days
> mega-brain-webhook: Up 12 days (healthy)
> mega-brain-daemon: Up 12 days (healthy)
> ```

## 🤖 Claude *(04:26:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat; echo \"\"; echo \"---BoK---\"; ls docs/bok/ 2>/dev/null; echo \"---scratch---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"; echo \"---HANDOFF lines---\"; wc -l HANDOFF.md",
  "description": "Chroma health + BoK + scratch + HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1782620800755273849}
> ---BoK---
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
> ---scratch---
> scratch has files
> ---HANDOFF lines---
> 8616 HANDOFF.md
> ```

## 🤖 Claude *(04:26:44)*


## 🤖 Claude *(04:26:44)*

Pre-flight clean (TS zero errors, all containers healthy). Now reading HANDOFF head/tail and key context.

## 🤖 Claude *(04:26:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 71
}
```

## 🤖 Claude *(04:26:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8216,
  "limit": 400
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
> 14	## Session Seal — Distribuição social: mapeamento COMPLETO — CP-008 (16:9) + CP-010 (publishers) + CP-011 (carrossel) (2026-06-28)
> 15	
> 16	Diretiva Sovereign: *"continue sem pular nada"*. Fechei os 3 OTDs restantes do reshaper, cada um provado materialmente (Lei 1) ou honestamente diferido com razão.
> 17	
> 18	**CP-008 — render 16:9 YouTube long (FR-CP-004, OTD-CP-008 FECHADA).** Template determinístico `viral-long-16x9.html` (1920×1080, **sha256-idêntico** em 2 renders = NFR-VS-016) + `VALID_TEMPLATES`. Reshaper enfileira o render 16:9 on opt-in `long_form` (`charged_mco=0` single-tenant ⇒ sem refund-mint; billing multi-tenant = OTD-CP-008-BILLING), resolve 9:16 vs 16:9 por `composition.template`, youtube long_video → operacional. **E2E provado:** enqueue → video-bridge renderiza (548KB) → scope=video resolve `reused_master` (smoke 8/8).
> 19	
> 20	**CP-010 — publishers (parcial honesto).** `publish-social` ganhou **X thread (reply-chain)** + **FB photo** + **Pinterest image-pin** (deno-check + deploy; live E2E **gated em conta conectada/auditada** — mesmo gate de TikTok/YT). Reshaper marca IG/Pinterest/FB image surfaces operacionais (reframe smoke prova enqueue). **Diferido** (binary-upload **não verificável sem conta**): LinkedIn registerUpload (vídeo/imagem/document) · FB Reels vídeo · X chunked vídeo — o asset já é produzido; falta só o branch.
> 21	
> 22	**CP-011 — carrossel PDF (FR-CP-009 geração) + auto-segment.** `generate-carousel` (pdf-lib in-process) transforma atoms → **PDF de 6 páginas** (hook+key_points+stat+cta) — nova linha `channel_profiles` `linkedin:carousel` (`atoms_to_carousel`). Smoke prova `%PDF` baixável. Publisher LinkedIn-document diferido (OTD-CP-010). **Auto-segment FR-CP-012 = N/A hoje** (não há vídeo-fonte LONGO no pipeline p/ segmentar; aplica quando entrar input de vídeo longo).
> 23	
> 24	| Commit | Conteúdo |
> 25	|--------|----------|
> 26	| `2e4c3fb` | feat(reshaper): 16:9 YouTube long-form render (FR-CP-004, OTD-CP-008 fechada) |
> 27	| `6c3bc66` | feat(publish): X thread + FB photo + Pinterest image-pin (CP-010 parcial) |
> 28	| `293b041` | feat(reshaper): PDF carousel generation (FR-CP-009) |
> 29	
> 30	**Verificação:** `tsc` 0 · `deno check` todas verdes · **4 smokes verdes** (opt-in 17/17 · reframe c/ enqueue de imagem · carrossel 6-page %PDF · 16:9 E2E 8/8). Migration `20260628120000` (carousel seed, data-only — RLS já revisada). Mesh node `f8065479-3e8d-4420-b530-bc206e998bfd` · **8980 nós**.
> 31	
> 32	**Estado final do mapeamento (1 ideia → posts nativos):** vídeo 9:16 (IG Reel · TikTok · YT Short · Pinterest) + 16:9 (YT long, opt-in) · texto (LinkedIn · X thread) · imagem (IG feed · Pinterest pin · FB link_card) · carrossel PDF (LinkedIn). **O cérebro data-driven está COMPLETO**; o que resta é REACH externamente gated (audits dos apps = ação Sovereign) + os publishers binary-upload (prováveis só com conta conectada). **Próximo natural:** quando os audits saírem, conectar contas e provar os publishers live (LinkedIn media · FB Reels · X video) + primeiro pilar real witnessed E2E.
> 33	
> 34	---
> 35	
> 36	## Session Seal — Reshaper continuação: publish opt-in + image reframe (FR-CP-005/006 · OTD-CP-009 fechada) (2026-06-28)
> 37	
> 38	Continuação da seal do reshaper abaixo. Diretiva Sovereign: *"continue"* + OBS *"publicar ou deixar como rascunho deve ser opt-in se possível"*. Dois arcos, ambos provados (Lei 1).
> 39	
> 40	**Arco 1 — Publish opt-in (a OBS).** Posts sociais nascem **rascunho**; publicar é escolha explícita.
> 41	- Flag `auto_publish` flui `orchestrate-content`→`pipeline_runs.metadata`→reshaper. User-path default **false** (rascunho); cron/autopilot default **true** mas honra `autopilot_plans.hitl_required` (HITL⇒rascunho). Espelha o `wp_status='draft'`.
> 42	- Reshaper SEMPRE produz a variante (`channel_variants`); só **enfileira** quando `auto_publish`. Default ⇒ zero `scheduled_posts`.
> 43	- **Double-post eliminado:** os steps legados `linkedin_post`/`twitter_thread` do `orchestrate-step` **deixaram de enfileirar** (só geram `content_library` record) → o reshaper é a **autoridade única de enqueue social**.
> 44	- **`publish-channel-variant`** (edge fn user-JWT): publica UM rascunho escolhido (owner-bound, 409 idempotente; asset assinado owner-scoped pelo `auto-publish`). Gancho da futura UI de revisão.
> 45	
> 46	**Arco 2 — Image reframe (CP-009, OTD-CP-009 FECHADA).** Resolvido **in-process com `imagescript` (WASM, Deno)** — **sem host worker / FFmpeg**. O reshaper baixa o master, center-crop→resize→**JPEG** (formato universal API-safe): IG/LinkedIn/FB feed **4:5 1080×1350** · Pinterest **2:3 1000×1500** · FB link_card **1.91:1 1200×630** · YT thumb **16:9 1280×720**. **IG feed_image agora operacional** (publish-social `image_url`).
> 47	
> 48	| Action | Result |
> 49	|--------|--------|
> 50	| Publish opt-in (5 edge fns) | ✅ deployadas — `orchestrate-content`/`-step` (flag+legacy enqueue retirado) · `reshape-pillar` (gate) · `autopilot-run` (hitl) · `publish-channel-variant` (novo) |
> 51	| Image reframe in-process | ✅ `reshape-pillar` 113.8 kB (imagescript bundled) — reframe+JPEG, fail-open `pending_reframe` |
> 52	| /security-review | ✅ **limpo** (sub-agente adversarial): `publish-channel-variant` owner-bound (`getUser`+`.eq(user_id)`), sem leak de asset cross-tenant, legacy-removal não tirou authz |
> 53	| Smokes zero-cost | ✅ `smoke-reshape-pillar.ts` **17/17** (draft default · manual publish · auto mode · tenancy) + `smoke-reframe-image.ts` (geometria EXATA 1080×1350/1000×1500/1280×720 + magic bytes JPEG, baixado do bucket) |
> 54	
> 55	| Commit | Conteúdo |
> 56	|--------|----------|
> 57	| `475d01d` | feat(reshaper): publish opt-in — default draft + publish-channel-variant + retira legacy enqueue |
> 58	| `d77f9ff` | feat(reshaper): image reframe in-process (imagescript) FR-CP-005/006, OTD-CP-009 fechada |
> 59	
> 60	**Mesh seal:** handoff node `dc383bb7-8f0d-4f31-a6aa-d0f17352d7d9` (embedded 768d). Mesh **8976 nós**.
> 61	
> 62	**7 surfaces operacionais:** IG Reel · TikTok · YT Short · Pinterest vídeo · LinkedIn texto · X tweet · **IG feed_image**. **Próximo:** **OTD-CP-008** render 16:9 HyperFrames (YouTube long — template `*-16x9.html` + render-core + enqueue; secundário p/ marca em lançamento) · **OTD-CP-010** publishers faltantes (asset JÁ produzido; falta o branch de publish — LinkedIn/FB/X vídeo · FB/Pinterest/LinkedIn imagem · X thread multi-tweet; audit-gated) · **OTD-CP-011** PDF carousel/auto-segment. Reach público segue gated nos audits (ação Sovereign).
> 63	
> 64	---
> 65	
> 66	## Session Seal — Channel Reshaper + Atomizer: 1 pilar → posts nativos por canal (FR-CP-002/003) (2026-06-28)
> 67	
> 68	Diretiva Sovereign: *"o próximo passo seria o reshaper (FR-CP-003): 1 ideia → posts nativos em todas as redes? Continue com força total para finalizar todo o mapeamento da distribuição social autônoma operacional."* Operado sob ultracode + Closed-Loop. **O mapeamento data-driven (o cérebro) está finalizado e provado**; os hands de render/reframe divergentes ficam como OTDs honestos.
> 69	
> 70	**Achado central:** o `channel_profiles` (16 linhas-sistema seeded) já era o dicionário; faltava o **interpretador**. O `auto-publish` cru cross-postava o MESMO texto+vídeo a todas as redes = exatamente a penalidade que a tese combate. O reshaper produz **variante NATIVA por canal** (anti cross-post FR-CP-007) com **zero branch por canal** — toda a lógica vem da `transform_recipe`.
> 71	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8216	ContentLibraryPage monetization flow:
> 8217	  Card (text, body contains mercadolivre.com.br)
> 8218	    └── DropdownMenu → "Monetizar Links ML"
> 8219	          → handleMonetizeLinks(item):
> 8220	               match(ML_URL_RE) → unique URLs
> 8221	               for url of unique:
> 8222	                 POST process-affiliate-link → affiliate_url
> 8223	                 body.split(url).join(affiliate_url)
> 8224	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8225	          → Badge 💰 ML (emerald) exibido após monetização
> 8226	```
> 8227	
> 8228	---
> 8229	
> 8230	## Pending Actions (Commercial Launch)
> 8231	
> 8232	### CRITICAL — Must complete before first client
> 8233	
> 8234	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8235	
> 8236	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8237	
> 8238	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8239	
> 8240	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8241	
> 8242	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8243	
> 8244	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8245	
> 8246	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8247	
> 8248	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8249	
> 8250	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8251	
> 8252	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8253	
> 8254	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8255	
> 8256	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8257	   ```bash
> 8258	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8259	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8260	   ```
> 8261	
> 8262	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8263	
> 8264	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8265	
> 8266	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8267	
> 8268	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8269	
> 8270	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8271	
> 8272	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8273	
> 8274	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8275	
> 8276	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8277	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8278	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8279	
> 8280	### SOCIAL — Next steps
> 8281	
> 8282	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8283	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8284	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8285	
> 8286	### NON-CRITICAL
> 8287	
> 8288	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8289	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8290	- `browserslist` — ✅ updated (2026-04-26)
> 8291	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8292	
> 8293	### GITNEXUS MCP — Next steps
> 8294	
> 8295	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8296	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8297	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8298	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8299	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8300	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8301	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8302	
> 8303	### PHASE EPSILON — Next iterations
> 8304	
> 8305	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8306	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8307	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8308	
> 8309	### CORE — Next iterations
> 8310	
> 8311	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8312	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8313	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8314	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8315	
> 8316	### PHASE DELTA — Next iterations
> 8317	
> 8318	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8319	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8320	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8321	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8322	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8323	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8324	
> 8325	### USUÁRIO ZERO — Checklist de validação
> 8326	
> 8327	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8328	- ✅ Stripe sandbox secrets no vault
> 8329	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8330	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8331	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8332	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8333	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8334	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8335	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8336	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8337	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8338	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8339	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8340	
> 8341	---
> 8342	
> 8343	## Infrastructure
> 8344	
> 8345	| Service | Container | Port | Status |
> 8346	|---------|-----------|------|--------|
> 8347	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8348	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8349	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8350	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8351	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8352	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8353	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8354	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8355	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8356	
> 8357	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8358	
> 8359	```bash
> 8360	docker compose up -d
> 8361	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8362	```
> 8363	
> 8364	---
> 8365	
> 8366	## Security Model (Post-Go-Live)
> 8367	
> 8368	| Table | Isolation |
> 8369	|-------|-----------|
> 8370	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8371	| `mcorch_edges` | Same pattern |
> 8372	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8373	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8374	
> 8375	---
> 8376	
> 8377	## Billing Architecture
> 8378	
> 8379	| Decision | Value |
> 8380	|----------|-------|
> 8381	| Canonical billing ledger | `profiles.mco_balance` |
> 8382	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8383	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8384	| Orchestration cost | 10 mcoCoins/run |
> 8385	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8386	| Stripe | Sandbox keys active — swap to live before first client |
> 8387	
> 8388	---
> 8389	
> 8390	## GraphRAG State
> 8391	
> 8392	- **8973 total nodes** (verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8393	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8394	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8395	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8396	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8397	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8398	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8399	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8400	- HNSW cosine index operational
> 8401	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8402	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8403	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8404	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8405	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8406	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8407	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8408	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8409	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8410	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8411	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8412	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8413	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8414	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8415	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8416	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8417	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8418	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8419	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8420	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8421	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8422	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8423	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8424	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8425	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8426	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8427	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8428	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8429	
> 8430	### Embedding Model
> 8431	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8432	Schema: `vector(768)` — HNSW cosine index.
> 8433	
> 8434	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8435	Três camadas eliminam intervenção manual:
> 8436	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8437	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8438	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8439	
> 8440	### Comandos de manutenção da Mesh
> 8441	```bash
> 8442	# Verificar nós sem embedding (deveria retornar array vazio):
> 8443	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8444	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8445	
> 8446	# Backfill manual (Bun-native — requer .env):
> 8447	bun run scripts/backfill-embeddings.ts
> 8448	
> 8449	# Backfill de código-fonte nos nós AST:
> 8450	bun run scripts/backfill-node-content.ts
> 8451	
> 8452	# Re-sync AST completo:
> 8453	cd packages/gitnexus-core && npm run sync-mesh
> 8454	
> 8455	# Acompanhar re-ingesta pós-commit:
> 8456	tail -f /tmp/mcorch-ingest.log
> 8457	```
> 8458	
> 8459	---
> 8460	
> 8461	## Video Rescue Protocol
> 8462	
> 8463	When a video generation operation (Google Veo) times out or client disconnects:
> 8464	```bash
> 8465	# Via edge function (production):
> 8466	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8467	  -H "Authorization: Bearer <user_jwt>" \
> 8468	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8469	
> 8470	# Via local script (admin/debug):
> 8471	source .env && bun run rescue.ts <operation_id> <content_id>
> 8472	```
> 8473	
> 8474	---
> 8475	
> 8476	## Architecture Pillars
> 8477	
> 8478	| Layer | Implementation |
> 8479	|-------|---------------|
> 8480	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8481	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8482	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8483	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8484	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8485	
> 8486	---
> 8487	
> 8488	## Phase Delta — Architecture
> 8489	
> 8490	```
> 8491	OrchestrationPage (full-canvas, p-0)
> 8492	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8493	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8494	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8495	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8496	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8497	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8498	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8499	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8500	
> 8501	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8502	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8503	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8504	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8505	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8506	```
> 8507	
> 8508	### Canvas State Architecture (Hybrid)
> 8509	
> 8510	```
> 8511	User interaction → ReactFlow internal state (positions, drag)
> 8512	                         ↓ (debounced 600ms)
> 8513	                   localStorage (positions persist across refresh)
> 8514	                         ↑
> 8515	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8516	     ↓ (status changes sync to ReactFlow via useEffect)
> 8517	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8518	```
> 8519	
> 8520	## Key Files
> 8521	
> 8522	| Purpose | Path |
> 8523	|---------|------|
> 8524	| Architecture rules | `CLAUDE.md` |
> 8525	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8526	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8527	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8528	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8529	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8530	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8531	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8532	| **Node types** | `src/components/orchestrator/nodes/` |
> 8533	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8534	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8535	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8536	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8537	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8538	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8539	| Billing utilities | `src/lib/billing.ts` |
> 8540	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8541	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8542	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8543	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8544	| Video rescue (local) | `rescue.ts` |
> 8545	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8546	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8547	| Deploy harness | `scripts/harness-deploy.sh` |
> 8548	
> 8549	---
> 8550	
> 8551	## First Client Onboarding Checklist
> 8552	
> 8553	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8554	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8555	3. ~~Activate watchdog cron~~ ✅ Done
> 8556	4. ~~Deploy rescue-video function~~ ✅ Done
> 8557	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8558	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8559	7. Monitor `infra_health_logs` for first 24h.
> 8560	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8561	
> 8562	---
> 8563	
> 8564	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8565	
> 8566	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8567	
> 8568	| Action | Result |
> 8569	|--------|--------|
> 8570	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8571	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8572	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8573	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8574	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8575	
> 8576	| Commit | Conteúdo |
> 8577	|--------|----------|
> 8578	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8579	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8580	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8581	
> 8582	### Arquitetura Matrix Intelligence
> 8583	
> 8584	```
> 8585	ConstellationMatrix (Stabilized Engine)
> 8586	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8587	  └── NodeDetailsPanel (Tabbed Navigation)
> 8588	        ├── Tab Meta: Neighbor exploration + Net Context
> 8589	        ├── Tab Code: Source code preview (Supabase sync)
> 8590	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8591	
> 8592	useNodeIntelligence Hook:
> 8593	  - contentQuery: fetch nodes.content column
> 8594	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8595	  - state: isAnalyzing, analysisResult, progress
> 8596	```
> 8597	
> 8598	---
> 8599	
> 8600	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8601	
> 8602	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8603	
> 8604	| Action | Result |
> 8605	|--------|--------|
> 8606	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8607	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8608	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8609	
> 8610	**Output da análise (estruturado em pt-BR):**
> 8611	- Visão Geral — papel do módulo no sistema
> 8612	- Padrões Detectados — design patterns, antipatterns
> 8613	- Acoplamento & Dependências — análise In/Out-Degree
> 8614	- Recomendações — 1-3 ações priorizadas
> 8615	
> ```

## 🤖 Claude *(04:26:47)*


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
> Output too large (50.5KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/tool-results/bjc02zhqb.txt
> 
> Preview (first 2KB):
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 28 01:21 ..
> ---sprint---
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

## 🤖 Claude *(04:26:53)*


## 🤖 Claude *(04:26:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nfor slug in post-engine viral-autopilot video-studio vision-mcp; do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK gate check for active modules"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ post-engine — BoK complete
> ✅ viral-autopilot — BoK complete
> ✅ video-studio — BoK complete
> ✅ vision-mcp — BoK complete
> ```

## 🤖 Claude *(04:26:58)*


## 🤖 Claude *(04:27:20)*

```
═══════════════════════════════════════════════════════════
  HANDSON — Distribuição Social: Mapeamento COMPLETO (2026-06-28)
═══════════════════════════════════════════════════════════

🏁 ESTADO ATUAL
  Fase selada: Channel Reshaper + Atomizer — CP-008/010/011 ("continue sem pular nada")
  Últimos commits:
    6c30136 — docs(readme): v6.58.0 badge + neural_mesh 8980 nodes
    2116904 — chore(deno): lock pdf-lib deps for generate-carousel
    390eb0a — docs(handoff): seal distribution mapping complete — CP-008/010/011
    293b041 — feat(reshaper): PDF carousel generation (FR-CP-009, CP-011 partial)
    6c3bc66 — feat(publish): X thread + FB photo + Pinterest image-pin (CP-010 partial)

📂 MUDANÇAS PENDENTES
  Worktree limpo ✅ (git status vazio, HEAD = 6c30136)

🏗️ INFRA
  mcorch_chroma:     Up 12 days (healthy) — Chroma API v2: OK (heartbeat ✅)
  mcorch_claude_mem: Up 12 days (healthy)
  mcorch_vision_mcp: Up 11 days (healthy)
  mega-brain-*:      daemon/webhook healthy · dashboard up

🧠 KNOWLEDGE MESH
  8980 nós · ~9070 arestas (100% embedded, 768d HNSW cosine)
  Seal node desta fase: f8065479-…-bc206e998bfd

🔧 TYPESCRIPT
  Zero erros ✅ (tsc --noEmit limpo)

📚 BoK SUITES (MCORCH Master Execution Protocol)
  Sealed (todas as ativas 9/9): post-engine · viral-autopilot · video-studio · vision-mcp ✅
  Incomplete: nenhuma das ativas
  GATE: liberado — nenhum módulo novo em aberto

📌 SPRINT
  Goal: Distribuição social autônoma operacional (LinkedIn live; Twitter/IG/YT/TikTok gated em API tier/audits)
  Estado: o CÉREBRO data-driven (1 ideia → posts nativos por canal) está COMPLETO e provado.
          O que resta é REACH externamente gated (audits dos apps = ação Sovereign).

⚡ PRÓXIMOS PASSOS (prioridade)
  1. 🎯 Publishers binary-upload (OTD-CP-010) — asset JÁ produzido, falta só o branch:
     LinkedIn registerUpload (vídeo/imagem/document) · FB Reels vídeo · X chunked vídeo.
     Verificável live SÓ com conta conectada/auditada (mesmo gate de TikTok/YT).
  2. 📹 Viral Autopilot — 1º ciclo PAGO de vídeo witnessed (habilitar video_enabled + GO)
     + editor HyperFrames Studio (módulo-container, vhost studio.mcorch.com = DNS Sovereign).
  3. 💰 Postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER) — fechar revenue_cents > 0 no ROIWidget.

⚠️ ALERTAS
  • scratch/ contém arquivos — protocolo sugere mover p/ .claude/scripts/db/ (não urgente; revisar).
  • REACH público segue bloqueado nos audits dos apps sociais (LinkedIn/FB/X/TikTok/YT/IG) — ação Sovereign.
  • Stripe ainda em sandbox (intencional — Usuário Zero). Demais: nenhum bloqueador técnico ✅

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

O mapeamento da distribuição social está **materialmente completo** (tsc 0, 4 smokes verdes, mesh 8980). A fronteira agora é externa: os **publishers binary-upload** e o **reach público** dependem de contas conectadas + audits dos apps (ação sua).

Qual frente seguimos? Sugiro **(1)** os branches de publish faltantes (LinkedIn/FB/X binary), que são código que posso escrever e deixar pronto mesmo antes do audit, ou **(2)** destravar o 1º ciclo de vídeo do Autopilot witnessed.

## 👤 User *(04:28:12)*

EU mandei pro coowork isso.:

prpeciso saber se minhas paginas estão de acordo com.:

https://support.google.com/cloud/answer/13806988?hl=pt-BR

Minhas paginas.: 
https://login.mcorch.com/
https://login.mcorch.com/terms
https://login.mcorch.com/privacy

---


Ele respondeu.:

The Google requirements page loaded fully, but your three pages returned only a shell (meta tags + two links) — they're client-rendered (built on Lovable), so a plain fetch can't see the real text. I'll render them with a browser to read the actual content.I'll read the terms and homepage in one batch.The privacy and terms pages render fully. The homepage extracted almost no text — let me screenshot it to see what's actually there before judging it.Verifiquei as três páginas renderizadas (são client-rendered/Lovable; o fetch simples só via o "esqueleto", por isso abri no navegador). Resumo:

**Veredito: em boa forma.** A política de privacidade atende à maioria dos requisitos do guia "App Privacy Policy". Faltam 3–4 ajustes para reduzir risco de rejeição na verificação OAuth — sobretudo por ser um app de IA.

Política de Privacidade (`/privacy`) vs. checklist do Google:

- ✅ Página HTML dedicada, em domínio próprio, URL diferente da home
- ✅ Associada à marca (cita "Magic Constellation", não é template)
- ✅ Diz **quais** dados do Google coleta (e-mail, nome, foto, tokens de acesso/atualização)
- ✅ Diz **como** usa os dados (identificação, personalização, manter conexão, prestar/melhorar o serviço)
- ✅ Diz **com quem** compartilha (Supabase, Stripe, ou por lei) e que **não vende** dados
- ✅ Segurança e **retenção/exclusão** (inclui exclusão via conta ou contato@mcorch.com)
- ✅ Cita a Política de Dados do Usuário das APIs do Google, incluindo **Uso Limitado**

Lacunas a corrigir (em ordem de prioridade):

1. **Treino de IA (crítico p/ seu caso).** Como é uma plataforma de IA, o Google é rigoroso aqui. Adicione frase explícita: *"Não usamos dados de usuários do Google para desenvolver, melhorar ou treinar modelos de IA/ML generalizados."* Hoje seu texto diz só "melhorar nossos serviços", o que pode ser interpretado como uso proibido.
2. **Aviso de alterações.** O Google exige avisar o usuário quando você muda como usa os dados do Google. A política tem data de atualização, mas falta uma cláusula "Alterações nesta política / notificaremos os usuários".
3. **Revogação de acesso / tokens.** Como você armazena tokens, explique como o usuário revoga o acesso (ex.: página de permissões da conta Google) e que os tokens são apagados ao desconectar.
4. **Segurança mais específica.** Troque "medidas robustas" por algo concreto como "criptografia em trânsito e em repouso".

Termos de Uso (`/terms`): completos e adequados — não são exigidos por este guia específico, mas ajudam.

Homepage (`/`): ✅ descreve a funcionalidade do app e tem o link "Política de Privacidade" em destaque no menu superior, como o Google pede.

Dois pontos que **só você confirma no Console** (não dá pra ver daqui): que `mcorch.com` está **verificado como seu** no Search Console, e que as URLs na tela de consentimento OAuth apontam exatamente para essas páginas.

Importante: isso é uma checagem dos requisitos técnicos do Google, não aconselhamento jurídico.

Quer que eu já escreva o texto corrigido da política de privacidade com esses 4 ajustes, pronto pra colar?

---


Preciso que você me ajude a aplicar os pontos que ele falou, Lacunas a corrigir (em ordem de prioridade). O resto ja verifiquei e esta correto

## 👤 User *(04:28:12)*

[Request interrupted by user]

## 👤 User *(04:28:17)*

EU mandei pro coowork isso.:

prpeciso saber se minhas paginas estão de acordo com.:

https://support.google.com/cloud/answer/13806988?hl=pt-BR

Minhas paginas.: 
https://login.mcorch.com/
https://login.mcorch.com/terms
https://login.mcorch.com/privacy

---


Ele respondeu.:

The Google requirements page loaded fully, but your three pages returned only a shell (meta tags + two links) — they're client-rendered (built on Lovable), so a plain fetch can't see the real text. I'll render them with a browser to read the actual content.I'll read the terms and homepage in one batch.The privacy and terms pages render fully. The homepage extracted almost no text — let me screenshot it to see what's actually there before judging it.Verifiquei as três páginas renderizadas (são client-rendered/Lovable; o fetch simples só via o "esqueleto", por isso abri no navegador). Resumo:

**Veredito: em boa forma.** A política de privacidade atende à maioria dos requisitos do guia "App Privacy Policy". Faltam 3–4 ajustes para reduzir risco de rejeição na verificação OAuth — sobretudo por ser um app de IA.

Política de Privacidade (`/privacy`) vs. checklist do Google:

- ✅ Página HTML dedicada, em domínio próprio, URL diferente da home
- ✅ Associada à marca (cita "Magic Constellation", não é template)
- ✅ Diz **quais** dados do Google coleta (e-mail, nome, foto, tokens de acesso/atualização)
- ✅ Diz **como** usa os dados (identificação, personalização, manter conexão, prestar/melhorar o serviço)
- ✅ Diz **com quem** compartilha (Supabase, Stripe, ou por lei) e que **não vende** dados
- ✅ Segurança e **retenção/exclusão** (inclui exclusão via conta ou contato@mcorch.com)
- ✅ Cita a Política de Dados do Usuário das APIs do Google, incluindo **Uso Limitado**

Lacunas a corrigir (em ordem de prioridade):

1. **Treino de IA (crítico p/ seu caso).** Como é uma plataforma de IA, o Google é rigoroso aqui. Adicione frase explícita: *"Não usamos dados de usuários do Google para desenvolver, melhorar ou treinar modelos de IA/ML generalizados."* Hoje seu texto diz só "melhorar nossos serviços", o que pode ser interpretado como uso proibido.
2. **Aviso de alterações.** O Google exige avisar o usuário quando você muda como usa os dados do Google. A política tem data de atualização, mas falta uma cláusula "Alterações nesta política / notificaremos os usuários".
3. **Revogação de acesso / tokens.** Como você armazena tokens, explique como o usuário revoga o acesso (ex.: página de permissões da conta Google) e que os tokens são apagados ao desconectar.
4. **Segurança mais específica.** Troque "medidas robustas" por algo concreto como "criptografia em trânsito e em repouso".

Termos de Uso (`/terms`): completos e adequados — não são exigidos por este guia específico, mas ajudam.

Homepage (`/`): ✅ descreve a funcionalidade do app e tem o link "Política de Privacidade" em destaque no menu superior, como o Google pede.

Dois pontos que **só você confirma no Console** (não dá pra ver daqui): que `mcorch.com` está **verificado como seu** no Search Console, e que as URLs na tela de consentimento OAuth apontam exatamente para essas páginas.

Importante: isso é uma checagem dos requisitos técnicos do Google, não aconselhamento jurídico.

Quer que eu já escreva o texto corrigido da política de privacidade com esses 4 ajustes, pronto pra colar?

---


Preciso que você me ajude a aplicar os pontos que ele falou, Lacunas a corrigir (em ordem de prioridade). O resto ja verifiquei e esta correto

## 🤖 Claude *(04:28:25)*


## 🤖 Claude *(04:28:27)*

Vou aplicar as 4 lacunas na política de privacidade. Primeiro preciso localizar a página `/privacy` e ler o texto atual para casar o estilo e corrigir exatamente os trechos certos.

## 🤖 Claude *(04:28:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rl -i \"privacy\\|privacidade\\|Uso Limitado\\|Limited Use\" src/pages src/components 2>/dev/null | head -20; echo \"---routes---\"; grep -rn -i \"privacy\\|terms\" src/App.tsx 2>/dev/null",
  "description": "Locate privacy/terms page files and routes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/pages/SettingsPage.tsx
> src/components/landing/Footer.tsx
> src/pages/PrivacyPolicy.tsx
> src/components/landing/Navbar.tsx
> ---routes---
> src/App.tsx:41:const PrivacyPolicy = lazy(() => import("./pages/PrivacyPolicy.tsx"));
> src/App.tsx:42:const TermsOfService = lazy(() => import("./pages/TermsOfService.tsx"));
> src/App.tsx:146:              <Route path="/privacy" element={<PrivacyPolicy />} />
> src/App.tsx:147:              <Route path="/terms" element={<TermsOfService />} />
> ```

## 🤖 Claude *(04:28:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { Navbar } from '@/components/landing/Navbar';
> 2	import { Footer } from '@/components/landing/Footer';
> 3	import { Helmet } from 'react-helmet-async';
> 4	import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> 5	import { Separator } from '@/components/ui/separator';
> 6	
> 7	export default function PrivacyPolicy() {
> 8	  return (
> 9	    <>
> 10	      <Helmet>
> 11	        <title>Magic Constellation</title>
> 12	        <meta name="description" content="Política de Privacidade da plataforma Magic Constellation." />
> 13	      </Helmet>
> 14	
> 15	      <div className="min-h-screen bg-background text-foreground">
> 16	        <Navbar />
> 17	        
> 18	        <main className="container mx-auto px-4 py-24 max-w-4xl">
> 19	          <Card className="glass-panel border-border/50">
> 20	            <CardHeader className="text-center space-y-4 py-12">
> 21	              <CardTitle className="text-4xl md:text-5xl font-bold text-gradient-primary">
> 22	                Política de Privacidade
> 23	              </CardTitle>
> 24	              <p className="text-muted-foreground font-medium uppercase tracking-widest text-xs">Magic Constellation</p>
> 25	              <p className="text-muted-foreground/60 text-sm">Última atualização: 17 de Abril de 2026</p>
> 26	            </CardHeader>
> 27	            <CardContent className="prose prose-invert max-w-none px-6 md:px-12 pb-16">
> 28	              <section className="space-y-8">
> 29	                <div>
> 30	                  <h2 className="text-2xl font-semibold text-primary">1. Introdução</h2>
> 31	                  <p className="text-muted-foreground leading-relaxed">
> 32	                    A Magic Constellation ("nós", "nosso") valoriza a sua privacidade. Esta Política de Privacidade descreve como coletamos, usamos e protegemos suas informações ao utilizar nossa plataforma de marketing com IA.
> 33	                  </p>
> 34	                </div>
> 35	
> 36	                <Separator className="bg-border/30" />
> 37	
> 38	                <div>
> 39	                  <h2 className="text-2xl font-semibold text-primary">2. Dados do Usuário do Google</h2>
> 40	                  <p className="text-muted-foreground leading-relaxed mb-4">
> 41	                    Ao utilizar o login social do Google ou conectar sua conta do Google para funcionalidades de marketing (como publicação no YouTube ou Google Business), acessamos as seguintes informações:
> 42	                  </p>
> 43	                  <ul className="list-disc list-inside text-muted-foreground space-y-2 ml-4">
> 44	                    <li>Seu endereço de e-mail (para identificação da conta).</li>
> 45	                    <li>Seu nome e foto de perfil (para personalização da interface).</li>
> 46	                    <li>Tokens de acesso e atualização (para manter a conexão ativa).</li>
> 47	                  </ul>
> 48	                  <p className="text-muted-foreground leading-relaxed mt-4 font-medium italic">
> 49	                    O uso e a transferência de informações recebidas das APIs do Google pela Magic Constellation obedecerão à <a href="https://developers.google.com/terms/api-services-user-data-policy#limited-use-policy" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">Política de Dados do Usuário dos Serviços de API do Google</a>, incluindo os requisitos de Uso Limitado.
> 50	                  </p>
> 51	                </div>
> 52	
> 53	                <Separator className="bg-border/30" />
> 54	
> 55	                <div>
> 56	                  <h2 className="text-2xl font-semibold text-primary">3. Coleta e Uso de Dados</h2>
> 57	                  <p className="text-muted-foreground leading-relaxed">
> 58	                    Coletamos informações que você nos fornece diretamente ao se cadastrar. Utilizamos seus dados para fornecer e melhorar nossos serviços, processar pagamentos, enviar comunicações importantes e garantir a segurança da plataforma.
> 59	                  </p>
> 60	                </div>
> 61	
> 62	                <Separator className="bg-border/30" />
> 63	
> 64	                <div>
> 65	                  <h2 className="text-2xl font-semibold text-primary">4. Compartilhamento de Dados</h2>
> 66	                  <p className="text-muted-foreground leading-relaxed">
> 67	                    Não vendemos seus dados para terceiros. O compartilhamento ocorre apenas com provedores de serviços essenciais (como Supabase para infraestrutura e Stripe para pagamentos) ou quando exigido por lei.
> 68	                  </p>
> 69	                </div>
> 70	
> 71	                <Separator className="bg-border/30" />
> 72	
> 73	                <div>
> 74	                  <h2 className="text-2xl font-semibold text-primary">5. Segurança e Retenção</h2>
> 75	                  <p className="text-muted-foreground leading-relaxed">
> 76	                    Implementamos medidas de segurança robustas para proteger seus dados. Os dados são retidos apenas pelo tempo necessário para cumprir as finalidades descritas nesta política ou conforme exigido por obrigações legais.
> 77	                  </p>
> 78	                </div>
> 79	
> 80	                <Separator className="bg-border/30" />
> 81	
> 82	                <div>
> 83	                  <h2 className="text-2xl font-semibold text-primary">6. Seus Direitos</h2>
> 84	                  <p className="text-muted-foreground leading-relaxed">
> 85	                    Você tem o direito de acessar, corrigir ou excluir seus dados pessoais a qualquer momento através das configurações da sua conta ou entrando em contato pelo e-mail <span className="text-primary">contato@mcorch.com</span>.
> 86	                  </p>
> 87	                </div>
> 88	              </section>
> 89	            </CardContent>
> 90	          </Card>
> 91	        </main>
> 92	
> 93	        <Footer />
> 94	      </div>
> 95	    </>
> 96	  );
> 97	}
> 98	
> ```

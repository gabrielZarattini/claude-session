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

## 🤖 Claude *(04:29:27)*


## 🤖 Claude *(04:29:32)*

Encontrei a página: [src/pages/PrivacyPolicy.tsx](src/pages/PrivacyPolicy.tsx) (última atualização: 17 Abr 2026). Vejo exatamente os 4 pontos que o coowork apontou:

1. **Treino de IA** — falta cláusula explícita (hoje a §3 diz só "melhorar nossos serviços").
2. **Aviso de alterações** — não existe seção.
3. **Revogação de acesso / tokens** — não existe seção (e vocês armazenam tokens).
4. **Segurança específica** — §5 diz "medidas robustas" (vago).

Como esses textos vão a verificação OAuth do Google (rejeição é cara, especialmente o item de IA), vou **fundamentar o texto no documento oficial do Google** antes de colar — em vez de improvisar a redação. Disparo uma verificação grounded + revisão adversarial do texto, e aplico em seguida.

## 🤖 Claude *(04:30:04)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'privacy-policy-google-oauth-grounding',\n  description: 'Ground 4 privacy-policy fixes in Google OAuth/Limited-Use requirements, draft JSX, adversarially verify',\n  phases: [\n    { title: 'Research', detail: 'fetch Google OAuth verification + Limited Use / AI-ML policy text' },\n    { title: 'Draft+Verify', detail: 'draft the 4 corrected sections, then adversarially check each vs requirements' },\n  ],\n}\n\nconst REQ_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    requirements: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        properties: {\n          gap: { type: 'string', description: 'which of the 4 gaps: ai-training | change-notice | revocation-tokens | security-specific | other' },\n          requirement: { type: 'string', description: 'what Google requires, in plain terms' },\n          exact_quote: { type: 'string', description: 'verbatim quote from the Google page that establishes this' },\n          source_url: { type: 'string' },\n        },\n        required: ['gap', 'requirement', 'exact_quote', 'source_url'],\n      },\n    },\n    canonical_ai_ml_phrasing: { type: 'string', description: 'The canonical sentence Google reviewers expect re: not using user data to develop/improve/train generalized AI/ML models \u2014 quote Google verbatim if possible' },\n    notes: { type: 'string' },\n  },\n  required: ['requirements', 'canonical_ai_ml_phrasing', 'notes'],\n}\n\nphase('Research')\nconst research = await parallel([\n  () => agent(\n    `You are researching Google's OAuth app verification and privacy-policy requirements. Fetch and read these pages (use WebFetch; fall back to WebSearch for the canonical text if a fetch is blocked):\n - https://support.google.com/cloud/answer/13806988?hl=en (App Privacy Policy requirements for OAuth verification)\n - https://support.google.com/cloud/answer/9110914 if relevant (Limited Use)\nExtract the EXACT requirements relevant to these 4 gaps a reviewer flagged on a privacy policy for an AI marketing SaaS that stores Google OAuth tokens:\n (1) AI/ML training disclosure, (2) notice of changes to how Google user data is used, (3) how a user revokes access / what happens to stored tokens, (4) concrete security wording.\nReturn verbatim quotes + source URLs. Focus on what the privacy policy TEXT must contain to pass review.`,\n    { agentType: 'general-purpose', phase: 'Research', label: 'research:oauth-verification', schema: REQ_SCHEMA }\n  ),\n  () => agent(\n    `You are researching Google's \"API Services User Data Policy\" \u2014 specifically the Limited Use requirements and the AI/ML clause. Fetch and read:\n - https://developers.google.com/terms/api-services-user-data-policy\n - the Limited Use section and any \"machine learning\" / \"AI models\" language within it.\nThe critical thing I need: the EXACT canonical phrasing Google uses to prohibit using Google user data to develop, improve, or train generalized / non-personalized AI and ML models. Quote it verbatim with the source URL. Also extract any requirement about notifying users of changes, data deletion/retention, and revocation. Return structured findings with verbatim quotes.`,\n    { agentType: 'general-purpose', phase: 'Research', label: 'research:limited-use-aiml', schema: REQ_SCHEMA }\n  ),\n])\n\nconst grounded = research.filter(Boolean)\n\nphase('Draft+Verify')\nconst DRAFT_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    sections: {\n      type: 'array',\n      description: 'Final PT-BR text content for each fix, ready to drop into JSX paragraphs/sections',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        properties: {\n          gap: { type: 'string' },\n          heading: { type: 'string', description: 'PT-BR section heading (or \"\" if it augments an existing section)' },\n          body_text: { type: 'string', description: 'PT-BR paragraph text, plain prose (no JSX), can mention links by URL' },\n          placement: { type: 'string', description: 'where it goes: new-section | augment-section-2 | replace-section-5-paragraph' },\n        },\n        required: ['gap', 'heading', 'body_text', 'placement'],\n      },\n    },\n  },\n  required: ['sections'],\n}\n\nconst draft = await agent(\n  `You are a privacy-policy author for \"Magic Constellation\" (an AI marketing SaaS that stores Google OAuth access/refresh tokens). Write the corrected PT-BR (Brazil) text for these 4 gaps, grounded in the Google requirements below. Match a professional but plain register consistent with an existing policy that already has sections: 1 Introdu\u00e7\u00e3o, 2 Dados do Usu\u00e1rio do Google, 3 Coleta e Uso de Dados, 4 Compartilhamento, 5 Seguran\u00e7a e Reten\u00e7\u00e3o, 6 Seus Direitos.\n\nGROUNDED REQUIREMENTS (verbatim from Google research):\n${JSON.stringify(grounded, null, 2)}\n\nProduce text for:\n (1) ai-training: an explicit clause stating Magic Constellation does NOT use Google user data to develop, improve, or train generalized/non-personalized AI/ML models. Should clarify that \"melhorar nossos servi\u00e7os\" elsewhere does NOT include training generalized AI models on Google data. Place: augment-section-2 (Dados do Usu\u00e1rio do Google).\n (2) revocation-tokens: a new section explaining how the user revokes access (via Google Account permissions at myaccount.google.com/permissions AND via disconnecting inside the app) and that stored access/refresh tokens are deleted upon disconnection. Place: new-section.\n (3) change-notice: a new section \"Altera\u00e7\u00f5es nesta Pol\u00edtica\" stating they will post changes with a new date and notify users of material changes to how Google user data is used. Place: new-section.\n (4) security-specific: replace the vague \"medidas de seguran\u00e7a robustas\" with concrete wording \u2014 encryption in transit (TLS/HTTPS) and at rest, plus access controls. Place: replace-section-5-paragraph.\n\nReturn concise, paste-ready PT-BR prose for each. No JSX, no markdown headers in body_text.`,\n  { phase: 'Draft+Verify', label: 'draft:sections', schema: DRAFT_SCHEMA, effort: 'high' }\n)\n\nconst VERDICT_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    verdicts: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        properties: {\n          gap: { type: 'string' },\n          passes: { type: 'boolean', description: 'would this wording satisfy a Google OAuth reviewer?' },\n          problem: { type: 'string', description: 'specific issue if it would NOT pass, else \"\"' },\n          improved_text: { type: 'string', description: 'corrected PT-BR text if needed, else the original' },\n        },\n        required: ['gap', 'passes', 'problem', 'improved_text'],\n      },\n    },\n    overall_pass: { type: 'boolean' },\n  },\n  required: ['verdicts', 'overall_pass'],\n}\n\nconst verdict = await agent(\n  `You are an adversarial Google OAuth-verification reviewer. Your job is to REJECT weak privacy-policy wording. For each drafted section below, judge whether it would actually pass Google's OAuth app verification for an AI app that stores Google tokens. Be strict: vague wording, missing the \"develop/improve/train generalized or non-personalized AI/ML models\" phrasing, or failing to say tokens are deleted on disconnect = FAIL. If it fails, provide improved PT-BR text.\n\nGROUNDED REQUIREMENTS:\n${JSON.stringify(grounded, null, 2)}\n\nDRAFTED SECTIONS:\n${JSON.stringify(draft, null, 2)}\n\nReturn a verdict per gap.`,\n  { phase: 'Draft+Verify', label: 'verify:adversarial', schema: VERDICT_SCHEMA, effort: 'high' }\n)\n\nreturn { grounded, draft, verdict }\n"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wzkaf383v
> Summary: Ground 4 privacy-policy fixes in Google OAuth/Limited-Use requirements, draft JSX, adversarially verify
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/subagents/workflows/wf_46126ab4-149
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/workflows/scripts/privacy-policy-google-oauth-grounding-wf_46126ab4-149.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/workflows/scripts/privacy-policy-google-oauth-grounding-wf_46126ab4-149.js"} to iterate without resending the script.)
> Run ID: wf_46126ab4-149
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/workflows/scripts/privacy-policy-google-oauth-grounding-wf_46126ab4-149.js", resumeFromRunId: "wf_46126ab4-149"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(04:30:07)*

The workflow is grounding the wording in Google's actual requirements and adversarially verifying it. It'll notify me when done.

## 👤 User *(04:34:11)*

<task-notification>
<task-id>wzkaf383v</task-id>
<tool-use-id>toolu_012rZD42dMedtNmCZZeGbvvL</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/tasks/wzkaf383v.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Ground 4 privacy-policy fixes in Google OAuth/Limited-Use requirements, draft JSX, adversarially verify" completed</summary>
<result>{"grounded":[{"requirements":[{"gap":"ai-training","requirement":"The privacy policy must comprehensively disclose how the app accesses, uses, stores, or shares Google user data, and must NOT indicate any use of Google user data beyond providing/improving user-facing features. \"Training AI models\" is explicitly listed as a prohibited use — so the policy text must not claim AI/ML training on Google data, and reviewers will flag a policy that implies it.","exact_quote":"Our policy requires that you limit your use of data to providing or improving user-facing features. All other uses of Google user data are prohibited, including any of the following reasons: Targeted advertising, Selling to data brokers, Providing to information resellers, Determining credit-worthiness, Lending purposes, User advertisements, Personalized advertisements, Retargeted advertisements, Interest-based advertisements, Creating databases, Training AI models","source_url":"https://support.google.com/cloud/answer/13806988?hl=en"},{"gap":"ai-training","requirement":"For Workspace API scopes, the privacy policy must affirmatively commit that the app does NOT retain/use Google user data to develop, improve, or train generalized/non-personalized AI/ML models. This is the canonical sentence to mirror in the policy text.","exact_quote":"Developers that access Workspace APIs will be required to commit via their privacy policies that they do not retain user data obtained through Workspace APIs to develop, improve, or train non-personalized AI and/or ML models.","source_url":"https://workspace.google.com/blog/ai-and-machine-learning/api-policy-protections"},{"gap":"ai-training","requirement":"The Limited Use restriction itself: using Google user data to create, train, or improve any ML/AI model beyond the specific user's personalized model is prohibited. The policy text should reflect this boundary (personalized-only, no generalized/foundational models).","exact_quote":"Transferring, selling, or using user data to create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature.","source_url":"https://developers.google.com/workspace/workspace-api-user-data-developer-policy"},{"gap":"ai-training","requirement":"The app (in its application or on a website/privacy policy) must carry an affirmative Limited Use compliance statement. This is the verbatim affirmative-statement Google itself offers as the model wording to include.","exact_quote":"An affirmative or other similar statement that your use of the data complies with the Limited Use restrictions must be disclosed in your application or on a website belonging to your web-service or application; for example, a link on a homepage to a dedicated page or privacy policy noting: 'The use of information received from Google Workspace APIs will adhere to the Google User Data Policy, including the Limited Use requirements.'","source_url":"https://developers.google.com/workspace/workspace-api-user-data-developer-policy"},{"gap":"change-notice","requirement":"The privacy policy (and in-product privacy notifications) must be kept current AND must notify users when the app changes how it uses Google user data. The policy text needs an explicit \"we will notify you of changes to how we use your Google data\" clause.","exact_quote":"Current and notify users if you change how your app uses Google user data","source_url":"https://support.google.com/cloud/answer/13806988?hl=en"},{"gap":"revocation-tokens","requirement":"The privacy policy must include disclosures about data retention AND deletion, including how a user can request deletion of their data and what happens when the retention period expires. (Google does not mandate exact revocation/token wording, but reviewers require retention+deletion text covering stored Google data; for stored OAuth tokens this is the relevant hook — state retention duration and deletion-on-disconnect/request.) Google provides these example sentences to include.","exact_quote":"Please update your privacy policy to include disclaimers around data retention and deletion to inform users about any actions you take on their behalf. Examples include: \"We store your personal information for a period of time that is consistent with our business purposes.\" \"We will retain your personal information for the length of time needed to fulfill the purposes outlined in this privacy policy unless a longer retention period is required or permitted by law.\" \"When the data retention period expires for a given type of data, we will delete or destroy it.\" \"You may request for your data to be deleted by...\"","source_url":"https://support.google.com/cloud/answer/13806988?hl=en"},{"gap":"security-specific","requirement":"The privacy policy must specify concrete data-protection mechanisms for sensitive data — i.e., explicit security wording about how Google user data is protected (e.g., security procedures, encryption). Vague/absent security language is flagged. Google gives these exact example sentences to include.","exact_quote":"Please update your privacy policy to include information about how you protect Google user data. Examples include: \"Security procedures are in place to protect the confidentiality of your data\" \"We use encryption to protect your information\"","source_url":"https://support.google.com/cloud/answer/13806988?hl=en"},{"gap":"other","requirement":"Baseline requirement framing every gap: the privacy policy must comprehensively disclose how the app accesses, uses, stores, or shares Google user data, be hosted on a verified domain the developer owns, be prominently linked, and not be a template/sample.","exact_quote":"comprehensively disclose how your app accesses, uses, stores, or shares Google user data","source_url":"https://support.google.com/cloud/answer/13806988?hl=en"}],"canonical_ai_ml_phrasing":"Developers that access Workspace APIs will be required to commit via their privacy policies that they do not retain user data obtained through Workspace APIs to develop, improve, or train non-personalized AI and/or ML models. (Source: Google Workspace Blog, \"Google Workspace API policy protections for generative AI\" — https://workspace.google.com/blog/ai-and-machine-learning/api-policy-protections.) The underlying Limited Use restriction states the prohibited act verbatim as: \"Transferring, selling, or using user data to create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature.\" (Workspace API User Data and Developer Policy.) RECOMMENDED policy sentence to satisfy reviewers, combining Google's own phrasing: \"We do not retain, use, or transfer Google user data obtained through Google APIs to develop, improve, or train generalized/non-personalized AI and/or ML models. Our use of information received from Google APIs adheres to the Google API Services User Data Policy, including the Limited Use requirements.\"","notes":"SOURCES FETCHED: (1) https://support.google.com/cloud/answer/13806988?hl=en — \"App Privacy Policy requirements\" — this is the reviewer-facing checklist and is the primary source for gaps 1 (prohibited uses incl. \"Training AI models\"), 2 (change notice), 3 (retention/deletion), and 4 (security). Its \"General Guidance\" lists the 4 baseline policy requirements (linked/prominent; current + notify of changes; hosted on verified domain; clearly linked, not a template). (2) https://developers.google.com/workspace/workspace-api-user-data-developer-policy — canonical Limited Use restriction text + the affirmative-statement requirement. (3) https://workspace.google.com/blog/ai-and-machine-learning/api-policy-protections — the verbatim \"commit via their privacy policies ... develop, improve, or train non-personalized AI and/or ML models\" sentence (the single best phrasing
... (truncated 23792 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/tasks/wzkaf383v.output)</result>
<usage><agent_count>4</agent_count><subagent_tokens>303096</subagent_tokens><tool_uses>37</tool_uses><duration_ms>247074</duration_ms></usage>
</task-notification>

## 🤖 Claude *(04:34:14)*

The research came back grounded in Google's actual policy text. Let me read the full result to get the drafted + adversarially-verified final wording.

## 🤖 Claude *(04:34:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/tasks/wzkaf383v.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	{
> 2	  "summary": "Ground 4 privacy-policy fixes in Google OAuth/Limited-Use requirements, draft JSX, adversarially verify",
> 3	  "agentCount": 4,
> 4	  "logs": [],
> 5	  "result": {
> 6	    "grounded": [
> 7	      {
> 8	        "requirements": [
> 9	          {
> 10	            "gap": "ai-training",
> 11	            "requirement": "The privacy policy must comprehensively disclose how the app accesses, uses, stores, or shares Google user data, and must NOT indicate any use of Google user data beyond providing/improving user-facing features. \"Training AI models\" is explicitly listed as a prohibited use — so the policy text must not claim AI/ML training on Google data, and reviewers will flag a policy that implies it.",
> 12	            "exact_quote": "Our policy requires that you limit your use of data to providing or improving user-facing features. All other uses of Google user data are prohibited, including any of the following reasons: Targeted advertising, Selling to data brokers, Providing to information resellers, Determining credit-worthiness, Lending purposes, User advertisements, Personalized advertisements, Retargeted advertisements, Interest-based advertisements, Creating databases, Training AI models",
> 13	            "source_url": "https://support.google.com/cloud/answer/13806988?hl=en"
> 14	          },
> 15	          {
> 16	            "gap": "ai-training",
> 17	            "requirement": "For Workspace API scopes, the privacy policy must affirmatively commit that the app does NOT retain/use Google user data to develop, improve, or train generalized/non-personalized AI/ML models. This is the canonical sentence to mirror in the policy text.",
> 18	            "exact_quote": "Developers that access Workspace APIs will be required to commit via their privacy policies that they do not retain user data obtained through Workspace APIs to develop, improve, or train non-personalized AI and/or ML models.",
> 19	            "source_url": "https://workspace.google.com/blog/ai-and-machine-learning/api-policy-protections"
> 20	          },
> 21	          {
> 22	            "gap": "ai-training",
> 23	            "requirement": "The Limited Use restriction itself: using Google user data to create, train, or improve any ML/AI model beyond the specific user's personalized model is prohibited. The policy text should reflect this boundary (personalized-only, no generalized/foundational models).",
> 24	            "exact_quote": "Transferring, selling, or using user data to create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature.",
> 25	            "source_url": "https://developers.google.com/workspace/workspace-api-user-data-developer-policy"
> 26	          },
> 27	          {
> 28	            "gap": "ai-training",
> 29	            "requirement": "The app (in its application or on a website/privacy policy) must carry an affirmative Limited Use compliance statement. This is the verbatim affirmative-statement Google itself offers as the model wording to include.",
> 30	            "exact_quote": "An affirmative or other similar statement that your use of the data complies with the Limited Use restrictions must be disclosed in your application or on a website belonging to your web-service or application; for example, a link on a homepage to a dedicated page or privacy policy noting: 'The use of information received from Google Workspace APIs will adhere to the Google User Data Policy, including the Limited Use requirements.'",
> 31	            "source_url": "https://developers.google.com/workspace/workspace-api-user-data-developer-policy"
> 32	          },
> 33	          {
> 34	            "gap": "change-notice",
> 35	            "requirement": "The privacy policy (and in-product privacy notifications) must be kept current AND must notify users when the app changes how it uses Google user data. The policy text needs an explicit \"we will notify you of changes to how we use your Google data\" clause.",
> 36	            "exact_quote": "Current and notify users if you change how your app uses Google user data",
> 37	            "source_url": "https://support.google.com/cloud/answer/13806988?hl=en"
> 38	          },
> 39	          {
> 40	            "gap": "revocation-tokens",
> 41	            "requirement": "The privacy policy must include disclosures about data retention AND deletion, including how a user can request deletion of their data and what happens when the retention period expires. (Google does not mandate exact revocation/token wording, but reviewers require retention+deletion text covering stored Google data; for stored OAuth tokens this is the relevant hook — state retention duration and deletion-on-disconnect/request.) Google provides these example sentences to include.",
> 42	            "exact_quote": "Please update your privacy policy to include disclaimers around data retention and deletion to inform users about any actions you take on their behalf. Examples include: \"We store your personal information for a period of time that is consistent with our business purposes.\" \"We will retain your personal information for the length of time needed to fulfill the purposes outlined in this privacy policy unless a longer retention period is required or permitted by law.\" \"When the data retention period expires for a given type of data, we will delete or destroy it.\" \"You may request for your data to be deleted by...\"",
> 43	            "source_url": "https://support.google.com/cloud/answer/13806988?hl=en"
> 44	          },
> 45	          {
> 46	            "gap": "security-specific",
> 47	            "requirement": "The privacy policy must specify concrete data-protection mechanisms for sensitive data — i.e., explicit security wording about how Google user data is protected (e.g., security procedures, encryption). Vague/absent security language is flagged. Google gives these exact example sentences to include.",
> 48	            "exact_quote": "Please update your privacy policy to include information about how you protect Google user data. Examples include: \"Security procedures are in place to protect the confidentiality of your data\" \"We use encryption to protect your information\"",
> 49	            "source_url": "https://support.google.com/cloud/answer/13806988?hl=en"
> 50	          },
> 51	          {
> 52	            "gap": "other",
> 53	            "requirement": "Baseline requirement framing every gap: the privacy policy must comprehensively disclose how the app accesses, uses, stores, or shares Google user data, be hosted on a verified domain the developer owns, be prominently linked, and not be a template/sample.",
> 54	            "exact_quote": "comprehensively disclose how your app accesses, uses, stores, or shares Google user data",
> 55	            "source_url": "https://support.google.com/cloud/answer/13806988?hl=en"
> 56	          }
> 57	        ],
> 58	        "canonical_ai_ml_phrasing": "Developers that access Workspace APIs will be required to commit via their privacy policies that they do not retain user data obtained through Workspace APIs to develop, improve, or train non-personalized AI and/or ML models. (Source: Google Workspace Blog, \"Google Workspace API policy protections for generative AI\" — https://workspace.google.com/blog/ai-and-machine-learning/api-policy-protections.) The underlying Limited Use restriction states the prohibited act verbatim as: \"Transferring, selling, or using user data to create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature.\" (Workspace API User Data and Developer Policy.) RECOMMENDED policy sentence to satisfy reviewers, combining Google's own phrasing: \"We do not retain, use, or transfer Google user data obtained through Google APIs to develop, improve, or train generalized/non-personalized AI and/or ML models. Our use of information received from Google APIs adheres to the Google API Services User Data Policy, including the Limited Use requirements.\"",
> 59	        "notes": "SOURCES FETCHED: (1) https://support.google.com/cloud/answer/13806988?hl=en — \"App Privacy Policy requirements\" — this is the reviewer-facing checklist and is the primary source for gaps 1 (prohibited uses incl. \"Training AI models\"), 2 (change notice), 3 (retention/deletion), and 4 (security). Its \"General Guidance\" lists the 4 baseline policy requirements (linked/prominent; current + notify of changes; hosted on verified domain; clearly linked, not a template). (2) https://developers.google.com/workspace/workspace-api-user-data-developer-policy — canonical Limited Use restriction text + the affirmative-statement requirement. (3) https://workspace.google.com/blog/ai-and-machine-learning/api-policy-protections — the verbatim \"commit via their privacy policies ... develop, improve, or train non-personalized AI and/or ML models\" sentence (the single best phrasing to quote to reviewers).\n\nIMPORTANT NUANCES FOR THE 4 GAPS:\n- GAP 1 (AI/ML): Google does NOT frame this as \"disclose that you train on data.\" It is the OPPOSITE: training generalized/non-personalized AI/ML models on Google user data is PROHIBITED, and developers must affirmatively COMMIT in the privacy policy that they do NOT do this. For an AI marketing SaaS this is the riskiest gap — the policy must (a) state Google data is not used to train/develop/improve generalized or foundational AI/ML models, and (b) carry the Limited Use affirmative statement. Personalized models scoped to that one user, for the user-facing feature, are the only permitted ML use.\n- GAP 2 (change notice): The ONLY verbatim hook is the \"Current and notify users if you change how your app uses Google user data\" bullet under General Guidance on the 13806988 page. There is no separate dedicated section; this single requirement is what reviewers cite. Policy needs an explicit changes-notification clause covering Google user data specifically.\n- GAP 3 (revocation/tokens): Google's reviewer page does NOT have a literally-titled \"revoke access / OAuth token deletion\" requirement. The flagged check is \"data retention or deletion\" disclosures. For stored OAuth tokens, satisfy this by stating: retention duration, that users can request deletion, and that tokens/data are deleted when the user disconnects/revokes or on request. The four example sentences quoted are Google's own suggested language. (Account-revocation mechanics — e.g., pointing users to https://myaccount.google.com/permissions — are best practice and recommended, but the verbatim policy-text requirement Google enforces is retention+deletion.)\n- GAP 4 (security): Reviewer check titled \"Your privacy policy does not specify any data protection mechanisms for sensitive data.\" Must include CONCRETE wording (security procedures + encryption are the two examples Google itself provides). Generic \"we take security seriously\" is insufficient — name mechanisms (encryption at rest/in transit, access controls, etc.).\n\nON THE 9110914 LINK: support.google.com/cloud/answer/9110914 did NOT serve Limited Use text (it is now an OAuth verification overview/landing page; WebFetch returned only navigation). The canonical Limited Use text lives at https://developers.google.com/terms/api-services-user-data-policy (general) and, for the AI/ML-specific commitment, the Workspace API User Data and Developer Policy + the Workspace blog. I fetched all of these to get verbatim text. WebFetch summarized rather than perfectly quoting the data-policy page's AI/ML sentence, so the canonical AI/ML quotes above are sourced from the Workspace policy page and Workspace blog, which carry the exact \"develop, improve, or train non-personalized AI and/or ML models\" phrasing reviewers use.\n\nMATERIALITY CAVEAT (Law 1): All quotes above were returned by WebFetch/WebSearch against the live Google pages in this session. WebFetch normalizes/summarizes; I cross-verified the load-bearing AI/ML sentence across two independent Google-owned URLs (workspace policy page + workspace blog) and they agree on the \"develop, improve, or train ... non-personalized AI and/or ML models\" wording. Recommend a final human eyeball of the exact bullet text on 13806988 before pasting into the policy, since Google occasionally re-words the example sentences."
> 60	      },
> 61	      {
> 62	        "requirements": [
> 63	          {
> 64	            "gap": "ai-training",
> 65	            "requirement": "Developers may NOT transfer, sell, or use Google user data to create, train, or improve a machine learning or AI model EXCEPT for that specific user's own personalized model tied to the appropriate use case / user-facing feature. This is the binding clause that prohibits using Google user data to build generalized / non-personalized (i.e. foundational) AI/ML models. NOTE: this exact clause lives in the PRODUCT-SPECIFIC Limited Use policies (Google Workspace, Google Photos, etc.), NOT in the umbrella api-services-user-data-policy page — which is the single most-misunderstood point.",
> 66	            "exact_quote": "Transferring, selling, or using user data to create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature.",
> 67	            "source_url": "https://developers.google.com/workspace/workspace-api-user-data-developer-policy"
> 68	          },
> 69	          {
> 70	            "gap": "ai-training",
> 71	            "requirement": "Identical AI/ML prohibition restated verbatim in the Google Photos APIs policy — confirms it is Google's canonical cross-product Limited Use phrasing, not Workspace-specific wording.",
> 72	            "exact_quote": "Transferring, selling, or using user data to create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature.",
> 73	            "source_url": "https://developers.google.com/photos/support/api-policy"
> 74	          },
> 75	          {
> 76	            "gap": "ai-training",
> 77	            "requirement": "Photos APIs additionally carry a SEPARATE anti-competition training prohibition: data obtained via the API may not be used (directly or indirectly) to create/train/improve competing or similar products. This is distinct from the personalized-model carve-out above and is product-specific to Photos.",
> 78	            "exact_quote": "Do not use this Google Photos APIs to create, train, or improve (directly or indirectly) similar or competing products or services.",
> 79	            "source_url": "https://developers.google.com/photos/support/api-policy"
> 80	          },
> 81	          {
> 82	            "gap": "other",
> 83	            "requirement": "Umbrella Limited Use baseline (section 2 of the main policy): use of API data is restricted to providing/improving prominent user-facing features. The main api-services-user-data-policy page does NOT itself spell out the AI/ML clause — it only states the general limited-use rule; the AI/ML specificity is delegated to each product's User Data and Developer Policy.",
> 84	            "exact_quote": "Limited Use: Your use of data obtained via the product's specified scopes must comply with the below requirements. These requirements apply to the raw data obtained from the scopes and data aggregated, anonymized, or derived from them. Limit your use of data to providing or improving user-facing features that are prominent in the requesting application's user interface;",
> 85	            "source_url": "https://developers.google.com/terms/api-services-user-data-policy"
> 86	          },
> 87	          {
> 88	            "gap": "ai-training",
> 89	            "requirement": "Affirmative-statement / disclosure obligation tied to Limited Use: an app relying on these scopes must publicly state that its use of the data complies with the Limited Use restrictions (Google supplies the canonical attestation sentence).",
> 90	            "exact_quote": "An affirmative or other similar statement that your use of the data complies with the Limited Use restrictions must be disclosed in your application or on a website belonging to your web-service or application; for example, a link on a homepage to a dedicated page or privacy policy noting: \"The use of information received from Google Workspace APIs will adhere to the Google User Data Policy, including the Limited Use restrictions.\"",
> 91	            "source_url": "https://developers.google.com/workspace/workspace-api-user-data-developer-policy"
> 92	          },
> 93	          {
> 94	            "gap": "change-notice",
> 95	            "requirement": "If the application changes how it uses Google user data, the developer MUST notify users and obtain renewed consent to an updated privacy policy BEFORE the new use begins. This is the primary change-notification requirement.",
> 96	            "exact_quote": "If you change the way your application uses Google user data, you must notify users and prompt them to consent to an updated privacy policy before you make use of Google user data in a new way or for a different purpose than originally disclosed.",
> 97	            "source_url": "https://developers.google.com/terms/api-services-user-data-policy"
> 98	          },
> 99	          {
> 100	            "gap": "change-notice",
> 101	            "requirement": "Newly-accessed data types not in the original disclosure require a privacy-policy update plus fresh user consent before access.",
> 102	            "exact_quote": "if you plan to access or use a type of user data that was not originally disclosed in your privacy policy (or in-product disclosures) when a Google user initially authorized access, you must update your privacy policy and prompt the user to consent to any changes before you may access that data.",
> 103	            "source_url": "https://developers.google.com/terms/api-services-user-data-policy"
> 104	          },
> 105	          {
> 106	            "gap": "change-notice",
> 107	            "requirement": "Secondary-use notification: if data requested for one purpose will also serve a secondary purpose, users must be told about both.",
> 108	            "exact_quote": "If your application requests data for one reason but the data will also be utilized for a secondary purpose, you must notify Google users of both use cases.",
> 109	            "source_url": "https://developers.google.com/terms/api-services-user-data-policy"
> 110	          },
> 111	          {
> 112	            "gap": "revocation-tokens",
> 113	            "requirement": "Developers must provide user-facing help documentation explaining how users can manage AND delete their data from the app/service (the deletion/revocation self-service requirement).",
> 114	            "exact_quote": "You must provide user help documentation that explains how users can manage and delete their data from your app or service.",
> 115	            "source_url": "https://developers.google.com/workspace/workspace-api-user-data-developer-policy"
> 116	          },
> 117	          {
> 118	            "gap": "revocation-tokens",
> 119	            "requirement": "Core respect principle: developers must honor user requests to delete their data (stated verbatim in both Workspace and Photos policies).",
> 120	            "exact_quote": "Be respectful: Honor user requests to delete their data.",
> 121	            "source_url": "https://developers.google.com/photos/support/api-policy"
> 122	          },
> 123	          {
> 124	            "gap": "revocation-tokens",
> 125	            "requirement": "Google's own enforcement-side revocation: Google may revoke/suspend the developer's access to Google API Services for non-compliance, and may also revoke access if the app enables others to violate the Terms/policies. (This is Google revoking the developer, distinct from end-user revocation of their own grant.)",
> 126	            "exact_quote": "Google may revoke or suspend your access to Google API Services and other Google products and services if you are found in violation of other product policies, terms of service, or other guidelines. Your access to Google API Services may also be revoked if your application enables end-users or other parties to violate the Google APIs Terms of Service and/or Google policies.",
> 127	            "source_url": "https://developers.google.com/terms/api-services-user-data-policy"
> 128	          },
> 129	          {
> 130	            "gap": "security-specific",
> 131	            "requirement": "Secure-handling baseline: all user data must be secured in transit and at rest, with reasonable steps to protect against unauthorized access, use, destruction, loss, alteration, or disclosure.",
> 132	            "exact_quote": "We expect all user data is secure in transit and at rest. Take reasonable and appropriate steps to protect all applications or systems that make use of Google API Service and any data derived from it against unauthorized or unlawful access, use, destruction, loss, alteration, or disclosure.",
> 133	            "source_url": "https://developers.google.com/terms/api-services-user-data-policy"
> 134	          },
> 135	          {
> 136	            "gap": "security-specific",
> 137	            "requirement": "Sensitive/Restricted scopes require annual third-party security assessment and a Letter of Assessment from a Google-designated assessor to obtain/keep access (Secure Data Handling).",
> 138	            "exact_quote": "Secure Data Handling: Applications accessing the product specified scopes (the \"Sensitive and Restricted Scopes\") must demonstrate that they adhere to certain security practices. Depending on the API being accessed and number of user grants or users, applications must pass an annual security assessment and obtain a Letter of Assessment from a Google-designated third party.",
> 139	            "source_url": "https://developers.google.com/terms/api-services-user-data-policy"
> 140	          }
> 141	        ],
> 142	        "canonical_ai_ml_phrasing": "\"Transferring, selling, or using user data to create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature.\" — This is Google's exact, currently-live canonical sentence. It appears verbatim (the only difference being the product name) in BOTH the Google Workspace API user data and developer policy (https://developers.google.com/workspace/workspace-api-user-data-developer-policy) and the Google Photos APIs policy (https://developers.google.com/photos/support/api-policy), as the final item in the \"All other transfers, uses, or sale of user data is completely prohibited, including:\" list under \"Limited use of user data\". The construction \"create, train, or improve … beyond that specific user's personalized model\" is precisely how Google draws the line between a permitted PERSONALIZED model (for that one user's user-facing feature) and a prohibited GENERALIZED / non-personalized / foundational model. Reviewers expect this language echoed, and a developer should additionally publish the verbatim attestation: \"The use of information received from Google [Workspace/Photos] APIs will adhere to the Google User Data Policy, including the Limited Use requirements.\"",
> 143	        "notes": "CRITICAL DISTINCTION (verified materially, not from memory): The umbrella page the user asked for — https://developers.google.com/terms/api-services-user-data-policy — does NOT contain the AI/ML training clause. Its \"Limited Use\" section (section 2) only states the general rule (limit use to prominent user-facing features; no transfers except listed exceptions; no human reading except listed exceptions; and a prohibited list covering ad-targeting, data-broker sale, and credit-worthiness). The explicit \"create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model\" sentence lives in the PRODUCT-SPECIFIC Limited Use policies (Workspace, Photos, and by reference other products), which the umbrella page delegates to via \"Additional Requirements for Specific API Scopes\" → each product's User Data and Developer Policy. Any compliance answer that quotes only the umbrella page for the AI clause is wrong.\n\nMETHOD / MATERIALITY (Law 1): firecrawl CLI was unavailable (not on PATH, no FIRECRAWL_API_KEY); used curl with a desktop UA + a Python HTML-to-text strip. The umbrella, Workspace, and Photos policy pages all returned full server-rendered policy bodies via curl (verified by grep hits on the exact clauses). WebFetch's auto-summary FALSELY reported \"no explicit clause prohibiting AI model training\" on the umbrella page — that was correct for the umbrella page specifically but would have been a misleading conclusion; the raw curl extraction + targeted product-policy fetches corrected it. The support.google.com Cloud help pages that surfaced the words \"foundational\" / \"generalized or non-personalized\" are JS-rendered (curl got only the shell, ~1KB usable) and one candidate URL (answer/13806097) 404'd; therefore the \"foundational model\" wording is Google's support/FAQ gloss, while the BINDING, currently-live policy text uses \"machine learning or artificial intelligence model beyond that specific user's personalized model.\" Quote the binding policy text; the \"generalized / non-personalized\" phrasing is an accurate paraphrase of its intent, not a verbatim policy string.\n\nLocal artifacts (scratchpad, absolute paths): /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/google-policy.txt (umbrella), .../ws.txt (Workspace), .../photos.txt (Photos). Source HTML retained alongside each.\n\nADDITIONAL clauses worth noting for a full compliance posture (not separately quoted above): main policy \"Don't allow humans to read the data, unless…\" (affirmative consent / security / law / aggregated-internal-ops exceptions) and \"Transfers of data are not allowed, except…\" (improve-feature-with-consent / security / law / M&A-with-consent). No explicit fixed RETENTION PERIOD is mandated by these policies — the retention obligation is expressed as honor-deletion-requests + provide manage/delete documentation + secure-at-rest, rather than a numeric retention cap."
> 144	      }
> 145	    ],
> 146	    "draft": {
> 147	      "sections": [
> 148	        {
> 149	          "gap": "ai-training",
> 150	          "heading": "",
> 151	          "body_text": "Uso restrito de dados do Google (Limited Use). O Magic Constellation NÃO retém, usa ou transfere dados de usuário do Google obtidos por meio das APIs do Google para desenvolver, melhorar ou treinar modelos de inteligência artificial ou de aprendizado de máquina generalizados ou não personalizados (incluindo modelos fundacionais). Qualquer uso de modelo de IA/ML envolvendo seus dados do Google fica restrito exclusivamente ao seu próprio modelo personalizado, vinculado à funcionalidade voltada a você dentro do aplicativo. Quando, em outras partes desta política, mencionamos \"melhorar nossos serviços\", isso NÃO inclui — em nenhuma hipótese — o treinamento de modelos de IA generalizados sobre seus dados do Google. Reforçamos ainda que não utilizamos dados do Google para publicidade direcionada, venda a corretores de dados, revenda de informações, avaliação de crédito ou criação de bancos de dados. O uso das informações recebidas das APIs do Google está em conformidade com a Política de Dados de Usuário dos Serviços de API do Google (Google API Services User Data Policy), incluindo os requisitos de Uso Restrito (Limited Use).",
> 152	          "placement": "augment-section-2"
> 153	        },
> 154	        {
> 155	          "gap": "revocation-tokens",
> 156	          "heading": "Revogação de Acesso e Exclusão de Tokens",
> 157	          "body_text": "Você pode revogar o acesso do Magic Constellation aos seus dados do Google a qualquer momento, por dois caminhos. Primeiro, dentro do próprio aplicativo, na área de configurações, usando a opção de desconectar sua conta do Google. Segundo, diretamente na sua Conta Google, acessando a página de permissões em https://myaccount.google.com/permissions e removendo o acesso concedido ao Magic Constellation. Ao desconectar sua conta — por qualquer um desses caminhos — os tokens de acesso (access tokens) e de atualização (refresh tokens) que armazenamos são excluídos dos nossos sistemas, encerrando nosso acesso aos seus dados do Google. Mantemos seus dados pessoais apenas pelo período necessário para cumprir as finalidades descritas nesta política, salvo quando um período maior for exigido ou permitido por lei. Você também pode solicitar a exclusão dos seus dados a qualquer momento entrando em contato conosco pelos canais informados nesta política; quando o período de retenção de um determinado tipo de dado expira, ou mediante sua solicitação, nós o excluímos ou destruímos.",
> 158	          "placement": "new-section"
> 159	        },
> 160	        {
> 161	          "gap": "change-notice",
> 162	          "heading": "Alterações nesta Política",
> 163	          "body_text": "Podemos atualizar esta Política de Privacidade periodicamente. Sempre que isso ocorrer, publicaremos a versão revisada nesta mesma página, com a data de atualização correspondente, para que você possa identificar quando houve mudanças. Caso alteremos de forma material a maneira como acessamos, usamos, armazenamos ou compartilhamos seus dados do Google — ou passemos a usar esses dados para uma finalidade diferente da originalmente divulgada — notificaremos você e solicitaremos seu consentimento à política atualizada antes de aplicar o novo uso. Recomendamos revisar esta política regularmente para se manter informado sobre como tratamos seus dados.",
> 164	          "placement": "new-section"
> 165	        },
> 166	        {
> 167	          "gap": "security-specific",
> 168	          "heading": "",
> 169	          "body_text": "Adotamos mecanismos concretos de proteção de dados. Todas as informações do usuário, incluindo os dados do Google e os tokens de acesso e atualização armazenados, são protegidas por criptografia tanto em trânsito — por meio de conexões TLS/HTTPS — quanto em repouso. Aplicamos controles de acesso que limitam o acesso aos dados apenas a sistemas e pessoal autorizados, além de procedimentos de segurança destinados a preservar a confidencialidade das suas informações e protegê-las contra acesso, uso, alteração, divulgação, perda ou destruição não autorizados.",
> 170	          "placement": "replace-section-5-paragraph"
> 171	        }
> 172	      ]
> 173	    },
> 174	    "verdict": {
> 175	      "overall_pass": true,
> 176	      "verdicts": [
> 177	        {
> 178	          "gap": "ai-training",
> 179	          "passes": true,
> 180	          "problem": "",
> 181	          "improved_text": "Uso restrito de dados do Google (Limited Use). O Magic Constellation NÃO retém, usa ou transfere dados de usuário do Google obtidos por meio das APIs do Google para desenvolver, melhorar ou treinar modelos de inteligência artificial ou de aprendizado de máquina generalizados ou não personalizados (incluindo modelos fundacionais). Qualquer uso de modelo de IA/ML envolvendo seus dados do Google fica restrito exclusivamente ao seu próprio modelo personalizado, vinculado à funcionalidade voltada a você dentro do aplicativo, para o caso de uso apropriado. Quando, em outras partes desta política, mencionamos \"melhorar nossos serviços\", isso NÃO inclui — em nenhuma hipótese — o treinamento de modelos de IA generalizados sobre seus dados do Google. Reforçamos ainda que não utilizamos dados do Google para publicidade direcionada, venda a corretores de dados, revenda de informações, avaliação de crédito ou criação de bancos de dados. O uso das informações recebidas das APIs do Google está em conformidade com a Política de Dados de Usuário dos Serviços de API do Google (Google API Services User Data Policy), incluindo os requisitos de Uso Restrito (Limited Use)."
> 182	        },
> 183	        {
> 184	          "gap": "revocation-tokens",
> 185	          "passes": true,
> 186	          "problem": "",
> 187	          "improved_text": "Você pode revogar o acesso do Magic Constellation aos seus dados do Google a qualquer momento, por dois caminhos. Primeiro, dentro do próprio aplicativo, na área de configurações, usando a opção de desconectar sua conta do Google. Segundo, diretamente na sua Conta Google, acessando a página de permissões em https://myaccount.google.com/permissions e removendo o acesso concedido ao Magic Constellation. Ao desconectar sua conta — por qualquer um desses caminhos — os tokens de acesso (access tokens) e de atualização (refresh tokens) que armazenamos são excluídos dos nossos sistemas, encerrando nosso acesso aos seus dados do Google. Mantemos seus dados pessoais apenas pelo período necessário para cumprir as finalidades descritas nesta política, salvo quando um período maior for exigido ou permitido por lei. Você também pode solicitar a exclusão dos seus dados a qualquer momento entrando em contato conosco pelos canais informados nesta política; quando o período de retenção de um determinado tipo de dado expira, ou mediante sua solicitação, nós o excluímos ou destruímos."
> 188	        },
> 189	        {
> 190	          "gap": "change-notice",
> 191	          "passes": true,
> 192	          "problem": "",
> 193	          "improved_text": "Podemos atualizar esta Política de Privacidade periodicamente. Sempre que isso ocorrer, publicaremos a versão revisada nesta mesma página, com a data de atualização correspondente, para que você possa identificar quando houve mudanças. Caso alteremos a maneira como acessamos, usamos, armazenamos ou compartilhamos seus dados do Google — ou passemos a usar esses dados para uma finalidade diferente da originalmente divulgada, ou a acessar um tipo de dado do Google não divulgado anteriormente — notificaremos você e solicitaremos seu consentimento à política atualizada antes de aplicar o novo uso. Recomendamos revisar esta política regularmente para se manter informado sobre como tratamos seus dados."
> 194	        },
> 195	        {
> 196	          "gap": "security-specific",
> 197	          "passes": true,
> 198	          "problem": "",
> 199	          "improved_text": "Adotamos mecanismos concretos de proteção de dados. Todas as informações do usuário, incluindo os dados do Google e os tokens de acesso e atualização armazenados, são protegidas por criptografia tanto em trânsito — por meio de conexões TLS/HTTPS — quanto em repouso. Aplicamos controles de acesso que limitam o acesso aos dados apenas a sistemas e pessoal autorizados, além de procedimentos de segurança destinados a preservar a confidencialidade das suas informações e protegê-las contra acesso, uso, alteração, divulgação, perda ou destruição não autorizados."
> 200	        }
> 201	      ]
> 202	    }
> 203	  },
> 204	  "workflowProgress": [
> 205	    {
> 206	      "type": "workflow_phase",
> 207	      "index": 1,
> 208	      "title": "Research"
> 209	    },
> 210	    {
> 211	      "type": "workflow_phase",
> 212	      "index": 2,
> 213	      "title": "Draft+Verify"
> 214	    },
> 215	    {
> 216	      "type": "workflow_agent",
> 217	      "index": 1,
> 218	      "label": "research:oauth-verification",
> 219	      "phaseIndex": 1,
> 220	      "phaseTitle": "Research",
> 221	      "agentId": "a505c014a973cd09f",
> 222	      "agentType": "general-purpose",
> 223	      "model": "claude-opus-4-8",
> 224	      "state": "done",
> 225	      "startedAt": 1782621004646,
> 226	      "queuedAt": 1782621004603,
> 227	      "attempt": 1,
> 228	      "lastToolName": "StructuredOutput",
> 229	      "lastToolSummary": "Developers that access Workspace APIs will be required to c…",
> 230	      "promptPreview": "You are researching Google's OAuth app verification and privacy-policy requirements. Fetch and read these pages (use WebFetch; fall back to WebSearch for the canonical text if a fetch is blocked):\n - https://support.google.com/cloud/answer/13806988?hl=en (App Privacy Policy requirements for OAuth verification)\n - https://support.google.com/cloud/answer/9110914 if relevant (Limited Use)\nExtract the…",
> 231	      "lastProgressAt": 1782621120366,
> 232	      "tokens": 73450,
> 233	      "toolCalls": 11,
> 234	      "durationMs": 115719,
> 235	      "resultPreview": "{\"requirements\":[{\"gap\":\"ai-training\",\"requirement\":\"The privacy policy must comprehensively disclose how the app accesses, uses, stores, or shares Google user data, and must NOT indicate any use of Google user data beyond providing/improving user-facing features. \\\"Training AI models\\\" is explicitly listed as a prohibited use — so the policy text must not claim AI/ML training on Google data, and …"
> 236	    },
> 237	    {
> 238	      "type": "workflow_agent",
> 239	      "index": 2,
> 240	      "label": "research:limited-use-aiml",
> 241	      "phaseIndex": 1,
> 242	      "phaseTitle": "Research",
> 243	      "agentId": "a65e02bf351ab3e78",
> 244	      "agentType": "general-purpose",
> 245	      "model": "claude-opus-4-8",
> 246	      "state": "done",
> 247	      "startedAt": 1782621004648,
> 248	      "queuedAt": 1782621004603,
> 249	      "attempt": 1,
> 250	      "lastToolName": "StructuredOutput",
> 251	      "lastToolSummary": "\"Transferring, selling, or using user data to create, train…",
> 252	      "promptPreview": "You are researching Google's \"API Services User Data Policy\" — specifically the Limited Use requirements and the AI/ML clause. Fetch and read:\n - https://developers.google.com/terms/api-services-user-data-policy\n - the Limited Use section and any \"machine learning\" / \"AI models\" language within it.\nThe critical thing I need: the EXACT canonical phrasing Google uses to prohibit using Google user da…",
> 253	      "lastProgressAt": 1782621210311,
> 254	      "tokens": 84970,
> 255	      "toolCalls": 24,
> 256	      "durationMs": 205662,
> 257	      "resultPreview": "{\"requirements\":[{\"gap\":\"ai-training\",\"requirement\":\"Developers may NOT transfer, sell, or use Google user data to create, train, or improve a machine learning or AI model EXCEPT for that specific user's own personalized model tied to the appropriate use case / user-facing feature. This is the binding clause that prohibits using Google user data to build generalized / non-personalized (i.e. founda…"
> 258	    },
> 259	    {
> 260	      "type": "workflow_agent",
> 261	      "index": 3,
> 262	      "label": "draft:sections",
> 263	      "phaseIndex": 2,
> 264	      "phaseTitle": "Draft+Verify",
> 265	      "agentId": "a99d76f5c7474f245",
> 266	      "model": "claude-opus-4-8",
> 267	      "state": "done",
> 268	      "startedAt": 1782621210366,
> 269	      "queuedAt": 1782621210312,
> 270	      "attempt": 1,
> 271	      "lastToolName": "StructuredOutput",
> 272	      "promptPreview": "You are a privacy-policy author for \"Magic Constellation\" (an AI marketing SaaS that stores Google OAuth access/refresh tokens). Write the corrected PT-BR (Brazil) text for these 4 gaps, grounded in the Google requirements below. Match a professional but plain register consistent with an existing policy that already has sections: 1 Introdução, 2 Dados do Usuário do Google, 3 Coleta e Uso de Dados,…",
> 273	      "lastProgressAt": 1782621232309,
> 274	      "tokens": 71784,
> 275	      "toolCalls": 1,
> 276	      "durationMs": 21943,
> 277	      "resultPreview": "{\"sections\":[{\"gap\":\"ai-training\",\"heading\":\"\",\"body_text\":\"Uso restrito de dados do Google (Limited Use). O Magic Constellation NÃO retém, usa ou transfere dados de usuário do Google obtidos por meio das APIs do Google para desenvolver, melhorar ou treinar modelos de inteligência artificial ou de aprendizado de máquina generalizados ou não personalizados (incluindo modelos fundacionais). Qualquer…"
> 278	    },
> 279	    {
> 280	      "type": "workflow_agent",
> 281	      "index": 4,
> 282	      "label": "verify:adversarial",
> 283	      "phaseIndex": 2,
> 284	      "phaseTitle": "Draft+Verify",
> 285	      "agentId": "adb7444b9d0b9cc5e",
> 286	      "model": "claude-opus-4-8",
> 287	      "state": "done",
> 288	      "startedAt": 1782621232339,
> 289	      "queuedAt": 1782621232315,
> 290	      "attempt": 1,
> 291	      "lastToolName": "StructuredOutput",
> 292	      "promptPreview": "You are an adversarial Google OAuth-verification reviewer. Your job is to REJECT weak privacy-policy wording. For each drafted section below, judge whether it would actually pass Google's OAuth app verification for an AI app that stores Google tokens. Be strict: vague wording, missing the \"develop/improve/train generalized or non-personalized AI/ML models\" phrasing, or failing to say tokens are de…",
> 293	      "lastProgressAt": 1782621251644,
> 294	      "tokens": 72892,
> 295	      "toolCalls": 1,
> 296	      "durationMs": 19305,
> 297	      "resultPreview": "{\"overall_pass\":true,\"verdicts\":[{\"gap\":\"ai-training\",\"passes\":true,\"problem\":\"\",\"improved_text\":\"Uso restrito de dados do Google (Limited Use). O Magic Constellation NÃO retém, usa ou transfere dados de usuário do Google obtidos por meio das APIs do Google para desenvolver, melhorar ou treinar modelos de inteligência artificial ou de aprendizado de máquina generalizados ou não personalizados (inc…"
> 298	    }
> 299	  ],
> 300	  "totalTokens": 303096,
> 301	  "totalToolCalls": 37
> 302	}
> ```

## 🤖 Claude *(04:35:06)*


## 🤖 Claude *(04:35:08)*

Texto fundamentado na política real do Google e aprovado na revisão adversarial (4/4 `passes: true`). Um achado importante da pesquisa: a cláusula vinculante de IA do Google é *"create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model"* — a redação "generalizado/não-personalizado/fundacional" é paráfrase fiel. Meu texto cobre **as duas formulações**, que é o mais seguro. Aplicando agora.

Edit 1 — data de atualização (a cláusula de alterações usa a data como sinal de mudança):

## 🤖 Claude *(04:35:10)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx",
  "old_string": "              <p className=\"text-muted-foreground/60 text-sm\">\u00daltima atualiza\u00e7\u00e3o: 17 de Abril de 2026</p>",
  "new_string": "              <p className=\"text-muted-foreground/60 text-sm\">\u00daltima atualiza\u00e7\u00e3o: 28 de Junho de 2026</p>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(04:35:13)*

Edit 2 — cláusula de treino de IA na §2 (Dados do Usuário do Google), antes do parágrafo Limited Use existente:

## 🤖 Claude *(04:35:22)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx",
  "old_string": "                  </ul>\n                  <p className=\"text-muted-foreground leading-relaxed mt-4 font-medium italic\">\n                    O uso e a transfer\u00eancia de informa\u00e7\u00f5es recebidas das APIs do Google pela Magic Constellation obedecer\u00e3o \u00e0 <a href=\"https://developers.google.com/terms/api-services-user-data-policy#limited-use-policy\" target=\"_blank\" rel=\"noopener noreferrer\" className=\"text-primary hover:underline\">Pol\u00edtica de Dados do Usu\u00e1rio dos Servi\u00e7os de API do Google</a>, incluindo os requisitos de Uso Limitado.\n                  </p>",
  "new_string": "                  </ul>\n                  <p className=\"text-muted-foreground leading-relaxed mt-4\">\n                    <span className=\"font-semibold text-foreground\">Uso restrito de dados do Google (Limited Use).</span> O Magic Constellation <span className=\"font-semibold\">n\u00e3o</span> ret\u00e9m, usa ou transfere dados de usu\u00e1rio do Google obtidos por meio das APIs do Google para desenvolver, melhorar ou treinar modelos de intelig\u00eancia artificial ou de aprendizado de m\u00e1quina generalizados ou n\u00e3o personalizados (incluindo modelos fundacionais). Qualquer uso de modelo de IA/ML envolvendo seus dados do Google fica restrito exclusivamente ao seu pr\u00f3prio modelo personalizado, vinculado \u00e0 funcionalidade voltada a voc\u00ea dentro do aplicativo, para o caso de uso apropriado. Quando, em outras partes desta pol\u00edtica, mencionamos \"melhorar nossos servi\u00e7os\", isso n\u00e3o inclui \u2014 em nenhuma hip\u00f3tese \u2014 o treinamento de modelos de IA generalizados sobre seus dados do Google. Tampouco utilizamos dados do Google para publicidade direcionada, venda a corretores de dados, revenda de informa\u00e7\u00f5es, avalia\u00e7\u00e3o de cr\u00e9dito ou cria\u00e7\u00e3o de bancos de dados.\n                  </p>\n                  <p className=\"text-muted-foreground leading-relaxed mt-4 font-medium italic\">\n                    O uso e a transfer\u00eancia de informa\u00e7\u00f5es recebidas das APIs do Google pela Magic Constellation obedecer\u00e3o \u00e0 <a href=\"https://developers.google.com/terms/api-services-user-data-policy#limited-use-policy\" target=\"_blank\" rel=\"noopener noreferrer\" className=\"text-primary hover:underline\">Pol\u00edtica de Dados do Usu\u00e1rio dos Servi\u00e7os de API do Google</a>, incluindo os requisitos de Uso Limitado.\n                  </p>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(04:35:25)*

Edit 3 — §5 Segurança com mecanismos concretos (criptografia em trânsito/repouso + controles de acesso):

## 🤖 Claude *(04:35:30)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx",
  "old_string": "                  <h2 className=\"text-2xl font-semibold text-primary\">5. Seguran\u00e7a e Reten\u00e7\u00e3o</h2>\n                  <p className=\"text-muted-foreground leading-relaxed\">\n                    Implementamos medidas de seguran\u00e7a robustas para proteger seus dados. Os dados s\u00e3o retidos apenas pelo tempo necess\u00e1rio para cumprir as finalidades descritas nesta pol\u00edtica ou conforme exigido por obriga\u00e7\u00f5es legais.\n                  </p>",
  "new_string": "                  <h2 className=\"text-2xl font-semibold text-primary\">5. Seguran\u00e7a e Reten\u00e7\u00e3o</h2>\n                  <p className=\"text-muted-foreground leading-relaxed\">\n                    Adotamos mecanismos concretos de prote\u00e7\u00e3o de dados. Todas as informa\u00e7\u00f5es do usu\u00e1rio, incluindo os dados do Google e os tokens de acesso e atualiza\u00e7\u00e3o armazenados, s\u00e3o protegidas por criptografia tanto em tr\u00e2nsito \u2014 por meio de conex\u00f5es TLS/HTTPS \u2014 quanto em repouso. Aplicamos controles de acesso que limitam o acesso aos dados apenas a sistemas e pessoal autorizados, al\u00e9m de procedimentos de seguran\u00e7a destinados a preservar a confidencialidade das suas informa\u00e7\u00f5es e proteg\u00ea-las contra acesso, uso, altera\u00e7\u00e3o, divulga\u00e7\u00e3o, perda ou destrui\u00e7\u00e3o n\u00e3o autorizados. Os dados s\u00e3o retidos apenas pelo tempo necess\u00e1rio para cumprir as finalidades descritas nesta pol\u00edtica ou conforme exigido por obriga\u00e7\u00f5es legais.\n                  </p>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(04:35:33)*

Edit 4 — nova §6 (Revogação/Tokens) + renumera "Seus Direitos" para §7 + nova §8 (Alterações):

## 🤖 Claude *(04:35:46)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx",
  "old_string": "                <Separator className=\"bg-border/30\" />\n\n                <div>\n                  <h2 className=\"text-2xl font-semibold text-primary\">6. Seus Direitos</h2>\n                  <p className=\"text-muted-foreground leading-relaxed\">\n                    Voc\u00ea tem o direito de acessar, corrigir ou excluir seus dados pessoais a qualquer momento atrav\u00e9s das configura\u00e7\u00f5es da sua conta ou entrando em contato pelo e-mail <span className=\"text-primary\">contato@mcorch.com</span>.\n                  </p>\n                </div>",
  "new_string": "                <Separator className=\"bg-border/30\" />\n\n                <div>\n                  <h2 className=\"text-2xl font-semibold text-primary\">6. Revoga\u00e7\u00e3o de Acesso e Exclus\u00e3o de Tokens</h2>\n                  <p className=\"text-muted-foreground leading-relaxed\">\n                    Voc\u00ea pode revogar o acesso do Magic Constellation aos seus dados do Google a qualquer momento, por dois caminhos. Primeiro, dentro do pr\u00f3prio aplicativo, na \u00e1rea de configura\u00e7\u00f5es, usando a op\u00e7\u00e3o de desconectar sua conta do Google. Segundo, diretamente na sua Conta Google, acessando a p\u00e1gina de permiss\u00f5es em <a href=\"https://myaccount.google.com/permissions\" target=\"_blank\" rel=\"noopener noreferrer\" className=\"text-primary hover:underline\">myaccount.google.com/permissions</a> e removendo o acesso concedido ao Magic Constellation. Ao desconectar sua conta \u2014 por qualquer um desses caminhos \u2014 os tokens de acesso (access tokens) e de atualiza\u00e7\u00e3o (refresh tokens) que armazenamos s\u00e3o exclu\u00eddos dos nossos sistemas, encerrando nosso acesso aos seus dados do Google. Voc\u00ea tamb\u00e9m pode solicitar a exclus\u00e3o dos seus dados a qualquer momento entrando em contato pelo e-mail <span className=\"text-primary\">contato@mcorch.com</span>; quando o per\u00edodo de reten\u00e7\u00e3o de um determinado tipo de dado expira, ou mediante sua solicita\u00e7\u00e3o, n\u00f3s o exclu\u00edmos ou destru\u00edmos.\n                  </p>\n                </div>\n\n                <Separator className=\"bg-border/30\" />\n\n                <div>\n                  <h2 className=\"text-2xl font-semibold text-primary\">7. Seus Direitos</h2>\n                  <p className=\"text-muted-foreground leading-relaxed\">\n                    Voc\u00ea tem o direito de acessar, corrigir ou excluir seus dados pessoais a qualquer momento atrav\u00e9s das configura\u00e7\u00f5es da sua conta ou entrando em contato pelo e-mail <span className=\"text-primary\">contato@mcorch.com</span>.\n                  </p>\n                </div>\n\n                <Separator className=\"bg-border/30\" />\n\n                <div>\n                  <h2 className=\"text-2xl font-semibold text-primary\">8. Altera\u00e7\u00f5es nesta Pol\u00edtica</h2>\n                  <p className=\"text-muted-foreground leading-relaxed\">\n                    Podemos atualizar esta Pol\u00edtica de Privacidade periodicamente. Sempre que isso ocorrer, publicaremos a vers\u00e3o revisada nesta mesma p\u00e1gina, com a data de atualiza\u00e7\u00e3o correspondente, para que voc\u00ea possa identificar quando houve mudan\u00e7as. Caso alteremos a maneira como acessamos, usamos, armazenamos ou compartilhamos seus dados do Google \u2014 ou passemos a usar esses dados para uma finalidade diferente da originalmente divulgada, ou a acessar um tipo de dado do Google n\u00e3o divulgado anteriormente \u2014 notificaremos voc\u00ea e solicitaremos seu consentimento \u00e0 pol\u00edtica atualizada antes de aplicar o novo uso. Recomendamos revisar esta pol\u00edtica regularmente para se manter informado sobre como tratamos seus dados.\n                  </p>\n                </div>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(04:35:50)*

Os 4 ajustes estão aplicados. Agora valido (tsc) e faço build+deploy com prova material — a página é client-rendered, então só sobe pro `login.mcorch.com` depois do build no repo principal.

## 🤖 Claude *(04:35:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -10 && echo \"TSC_EXIT=$?\"",
  "description": "TypeScript check after edits"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> TSC_EXIT=0
> ```

## 🤖 Claude *(04:36:02)*


## 🤖 Claude *(04:36:03)*

tsc limpo (exit 0). Estou no **repo principal** (não worktree), então build = deploy direto pro nginx. Vou delegar ao **build-deploy-guardian** para buildar e provar materialmente que o texto novo foi pro `dist/` servido (Lei 1 — sem falso-sucesso).

## 🤖 Claude *(04:36:17)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Build & deploy privacy policy fix",
  "subagent_type": "build-deploy-guardian",
  "prompt": "Contexto: editei `src/pages/PrivacyPolicy.tsx` no REPO PRINCIPAL (/home/gcrUX/htdocs/constellation-orchestra \u2014 N\u00c3O \u00e9 worktree), adicionando 4 ajustes de conformidade Google OAuth na pol\u00edtica de privacidade que serve em https://login.mcorch.com/privacy. A p\u00e1gina \u00e9 client-rendered (Lovable/Vite), ent\u00e3o s\u00f3 vai ao ar ap\u00f3s `bun run build` \u2192 dist/ \u2192 nginx.\n\nTarefa: buildar e VERIFICAR materialmente o deploy (Lei 1). Especificamente:\n\n1. Confirmar que estou no repo principal e que existe `.env` com as chaves Supabase (o bundle precisa do env baked).\n2. Rodar `bun run build` (produ\u00e7\u00e3o) \u2014 capturar o output literal (chunk hashes, \"built in Xs\").\n3. Provar MATERIALMENTE que o texto novo foi para o dist/ servido. Procure no `dist/assets/*.js` por trechos-\u00e2ncora EXATOS das 4 mudan\u00e7as (est\u00e3o em portugu\u00eas, em algum chunk lazy do PrivacyPolicy):\n   - \"treinar modelos de intelig\u00eancia artificial ou de aprendizado de m\u00e1quina generalizados\"   (cl\u00e1usula de treino de IA)\n   - \"Revoga\u00e7\u00e3o de Acesso e Exclus\u00e3o de Tokens\"   (nova se\u00e7\u00e3o 6)\n   - \"myaccount.google.com/permissions\"\n   - \"Altera\u00e7\u00f5es nesta Pol\u00edtica\"   (nova se\u00e7\u00e3o 8)\n   - \"criptografia tanto em tr\u00e2nsito\"   (seguran\u00e7a concreta)\n   - \"28 de Junho de 2026\"   (nova data)\n   Use grep -r nos arquivos do dist (cuidado: o texto pode estar com escapes unicode JS tipo \u00e3 para \u00e3 \u2014 se o grep literal falhar com acento, procure por uma \u00e2ncora SEM acento, ex.: \"Revogac\" / \"myaccount.google.com/permissions\" / \"generalizados\" / \"trito\" n\u00e3o; melhor: \"myaccount.google.com\" e \"generalizados\" e \"Tokens\" s\u00e3o ASCII-safe).\n4. Confirmar que o env foi baked (procure a URL Supabase ou VITE_SUPABASE no bundle, como faz normalmente).\n\nN\u00c3O declare \"deployed\" sem os greens. Reporte: comando rodado + output literal + quais \u00e2ncoras bateram em qual arquivo do dist + veredito (deployed / N\u00c3O deployed). Se algo falhar, diga exatamente o qu\u00ea."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Todos os gates verdes. Veredito: **DEPLOYED**.\n\n---\n\n## Build & Deploy Guardian — Veredito: DEPLOYED\n\nSurface única: **frontend** (`src/pages/PrivacyPolicy.tsx`), editada no **repo principal** (`/home/gcrUX/htdocs/constellation-orchestra`, branch `main`, toplevel == cwd → **não é worktree**, sem armadilha de worktree). Caminho usado: `bun run build` direto (repo principal tem `.env`, build = deploy).\n\n### Comando + output literal\n- `bun run build` → `✓ built in 26.76s`\n- Chunk PrivacyPolicy escrito: `dist/assets/PrivacyPolicy-IF1BhbgS.js` (8783 bytes, `Jun 28 01:37`)\n- Entry servido: `dist/assets/index-C41FfpHP.js` (661674 bytes, `Jun 28 01:37`)\n\n### Gates\n\n| Gate | Resultado | Prova literal |\n|------|-----------|---------------|\n| **G1 — env baked** | VERDE | `grep -rl bcyvddsykvehvpwstlfa dist/assets/ \\| wc -l` = **9**; URL completa `bcyvddsykvehvpwstlfa.supabase.co` presente no entry `index-C41FfpHP.js` |\n| **G2 — entry → chunk novo** | VERDE | `dist/index.html` aponta `src="/assets/index-C41FfpHP.js"`; esse entry referencia `PrivacyPolicy-IF1BhbgS` (único chunk que o cita) |\n| **G3 — origem nginx (best-effort)** | VERDE | `curl http://localhost/ -H "Host: login.mcorch.com"` serve `index-C41FfpHP.js`; fetch direto do chunk da origem retorna `myaccount.google.com/permissions` |\n\n### Âncoras das 4 mudanças — todas batem em `dist/assets/PrivacyPolicy-IF1BhbgS.js`\n\n| Mudança | Âncora verificada | Hits |\n|---------|-------------------|------|\n| Cláusula treino de IA | `treinar modelos de intelig` + `ncia artificial ou de aprendizado de m` + `generalizados` | 1 / 1 / 2 |\n| Seção 6 (Revogação) | `o de Acesso e Exclus` + `Revoga` + `o de Tokens` (Exclusão de Tokens) | match / match / match |\n| Link Google permissions | `myaccount.google.com/permissions` | 2 |\n| Seção 8 (Alterações) | `es nesta Pol` (Alterações nesta Política) + `ltera` | match |\n| Segurança concreta | `criptografia tanto em tr` (em trânsito) + `trânsito` | 1 / 1 |\n| Nova data | `28 de Junho de 2026` | 1 |\n\nObservação sobre acentos: os trechos com `ç`/`ã`/`í` (Revogação, Alterações, inteligência, trânsito) aparecem como bytes UTF-8 reais no bundle, não como escapes `\\u` — por isso os slices ASCII e os termos acentanados literais bateram diretamente, sem precisar de fallback de escape unicode.\n\n### Débitos pendentes\nNenhum débito de merge-para-main: a edição e o build aconteceram no repo principal servido pelo nginx. Nada a reconciliar.\n\n### Instrução final (Cloudflare)\nA origem (nginx) já serve o entry e o chunk novos. Cloudflare pode estar cacheando — no browser, faça **hard-refresh `Ctrl+Shift+R`** em `https://login.mcorch.com/privacy` para ver as 4 mudanças de conformidade Google OAuth.\n\nArquivos relevantes:\n- Fonte editada: `/home/gcrUX/htdocs/constellation-orchestra/src/pages/PrivacyPolicy.tsx`\n- Chunk servido: `/home/gcrUX/htdocs/constellation-orchestra/dist/assets/PrivacyPolicy-IF1BhbgS.js`\n- Entry servido: `/home/gcrUX/htdocs/constellation-orchestra/dist/assets/index-C41FfpHP.js`'}, {'type': 'text', 'text': "agentId: a90446f08a99126b9 (use SendMessage with to: 'a90446f08a99126b9', summary: '<5-10 word recap>' to continue this agent)\n<usage>subagent_tokens: 55624\ntool_uses: 11\nduration_ms: 98782</usage>"}]
> ```

## 🤖 Claude *(04:38:12)*


## 🤖 Claude *(04:38:14)*

Deploy provado materialmente — todas as 6 âncoras batem no chunk servido `dist/assets/PrivacyPolicy-IF1BhbgS.js`, env baked, origem nginx serve o entry+chunk novos.

Agora, honrando a diretiva Sovereign de **ver a página renderizada antes de declarar pronto** (Lei 1 — já pegou white-screen antes), vou subir um preview local do dist e abrir `/privacy` num browser real para confirmar que as 4 seções renderizam (a página é pública, sem login, então evito o bloqueio CF de datacenter).

## 🤖 Claude *(04:38:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -E '\"(preview|dev)\"' package.json",
  "description": "Check preview/dev scripts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>     "dev": "vite",
>     "preview": "vite preview",
> ```

## 🤖 Claude *(04:38:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "(npx vite preview --port 4319 --strictPort > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/vite-preview.log 2>&1 &) ; sleep 3 ; cat /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/vite-preview.log",
  "description": "Start vite preview of dist on port 4319"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   ➜  Local:   http://localhost:4319/
>   ➜  Network: http://10.0.0.143:4319/
>   ➜  Network: http://172.17.0.1:4319/
>   ➜  Network: http://172.23.0.1:4319/
>   ➜  Network: http://172.27.0.1:4319/
>   ➜  Network: http://172.24.0.1:4319/
>   ➜  Network: http://172.22.0.1:4319/
>   ➜  Network: http://172.18.0.1:4319/
>   ➜  Network: http://172.25.0.1:4319/
> ```

## 🤖 Claude *(04:38:29)*

Preview no ar em `localhost:4319`. Vou abrir `/privacy` com o agent-browser e capturar screenshot.

## 🤖 Claude *(04:38:30)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "agent-browser",
  "args": "navigate to http://localhost:4319/privacy, wait for it to render, then take a full-page screenshot and extract the visible text of all section headings (h2 elements). Report the headings list and the screenshot path."
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: agent-browser
> ```

## 👤 User *(04:38:30)*

Base directory for this skill: /home/gcrUX/htdocs/constellation-orchestra/.claude/skills/agent-browser

# agent-browser

Fast browser automation CLI for AI agents. Chrome/Chromium via CDP with
accessibility-tree snapshots and compact `@eN` element refs.

Install: `npm i -g agent-browser && agent-browser install`

## Start here

This file is a discovery stub, not the usage guide. Before running any
`agent-browser` command, load the actual workflow content from the CLI:

```bash
agent-browser skills get core             # start here — workflows, common patterns, troubleshooting
agent-browser skills get core --full      # include full command reference and templates
```

The CLI serves skill content that always matches the installed version,
so instructions never go stale. The content in this stub cannot change
between releases, which is why it just points at `skills get core`.

## Specialized skills

Load a specialized skill when the task falls outside browser web pages:

```bash
agent-browser skills get electron          # Electron desktop apps (VS Code, Slack, Discord, Figma, ...)
agent-browser skills get slack             # Slack workspace automation
agent-browser skills get dogfood           # Exploratory testing / QA / bug hunts
agent-browser skills get vercel-sandbox    # agent-browser inside Vercel Sandbox microVMs
agent-browser skills get agentcore         # AWS Bedrock AgentCore cloud browsers
```

Run `agent-browser skills list` to see everything available on the
installed version.

## Why agent-browser

- Fast native Rust CLI, not a Node.js wrapper
- Works with any AI agent (Cursor, Claude Code, Codex, Continue, Windsurf, etc.)
- Chrome/Chromium via CDP with no Playwright or Puppeteer dependency
- Accessibility-tree snapshots with element refs for reliable interaction
- Sessions, authentication vault, state persistence, video recording
- Specialized skills for Electron apps, Slack, exploratory testing, cloud providers

## Observability Dashboard

The dashboard runs independently of browser sessions on port 4848 and can also be opened through a proxied or forwarded URL such as `https://dashboard.agent-browser.localhost`. Agents should stay on the dashboard origin: session tabs, status, and stream traffic are proxied internally, so session ports do not need to be exposed.


ARGUMENTS: navigate to http://localhost:4319/privacy, wait for it to render, then take a full-page screenshot and extract the visible text of all section headings (h2 elements). Report the headings list and the screenshot path.

## 🤖 Claude *(04:38:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "agent-browser skills get core 2>&1 | head -120",
  "description": "Load agent-browser core skill"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---
> name: core
> description: Core agent-browser usage guide. Read this before running any agent-browser commands. Covers the snapshot-and-ref workflow, navigating pages, interacting with elements (click, fill, type, select), extracting text and data, taking screenshots, managing tabs, handling forms and auth, waiting for content, running multiple browser sessions in parallel, and troubleshooting common failures. Use when the user asks to interact with a website, fill a form, click something, extract data, take a screenshot, log into a site, test a web app, or automate any browser task.
> allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
> ---
> 
> # agent-browser core
> 
> Fast browser automation CLI for AI agents. Chrome/Chromium via CDP, no
> Playwright or Puppeteer dependency. Accessibility-tree snapshots with compact
> `@eN` refs let agents interact with pages in ~200-400 tokens instead of
> parsing raw HTML.
> 
> Most normal web tasks (navigate, read, click, fill, extract, screenshot) are
> covered here. Load a specialized skill when the task falls outside browser
> web pages — see [When to load another skill](#when-to-load-another-skill).
> 
> ## The core loop
> 
> ```bash
> agent-browser open <url>        # 1. Open a page
> agent-browser snapshot -i       # 2. See what's on it (interactive elements only)
> agent-browser click @e3         # 3. Act on refs from the snapshot
> agent-browser snapshot -i       # 4. Re-snapshot after any page change
> ```
> 
> Refs (`@e1`, `@e2`, ...) are assigned fresh on every snapshot. They become
> **stale the moment the page changes** — after clicks that navigate, form
> submits, dynamic re-renders, dialog opens. Always re-snapshot before your
> next ref interaction.
> 
> ## Quickstart
> 
> ```bash
> # Install once
> npm i -g agent-browser && agent-browser install
> 
> # Take a screenshot of a page
> agent-browser open https://example.com
> agent-browser screenshot home.png
> agent-browser close
> 
> # Search, click a result, and capture it
> agent-browser open https://duckduckgo.com
> agent-browser snapshot -i                      # find the search box ref
> agent-browser fill @e1 "agent-browser cli"
> agent-browser press Enter
> agent-browser wait --load networkidle
> agent-browser snapshot -i                      # refs now reflect results
> agent-browser click @e5                        # click a result
> agent-browser screenshot result.png
> ```
> 
> The browser stays running across commands so these feel like a single
> session. Use `agent-browser close` (or `close --all`) when you're done.
> 
> ## Reading a page
> 
> ```bash
> agent-browser snapshot                    # full tree (verbose)
> agent-browser snapshot -i                 # interactive elements only (preferred)
> agent-browser snapshot -i -u              # include href urls on links
> agent-browser snapshot -i -c              # compact (no empty structural nodes)
> agent-browser snapshot -i -d 3            # cap depth at 3 levels
> agent-browser snapshot -s "#main"         # scope to a CSS selector
> agent-browser snapshot -i --json          # machine-readable output
> ```
> 
> Snapshot output looks like:
> 
> ```
> Page: Example - Log in
> URL: https://example.com/login
> 
> @e1 [heading] "Log in"
> @e2 [form]
>   @e3 [input type="email"] placeholder="Email"
>   @e4 [input type="password"] placeholder="Password"
>   @e5 [button type="submit"] "Continue"
>   @e6 [link] "Forgot password?"
> ```
> 
> For unstructured reading (no refs needed):
> 
> ```bash
> agent-browser get text @e1                # visible text of an element
> agent-browser get html @e1                # innerHTML
> agent-browser get attr @e1 href           # any attribute
> agent-browser get value @e1               # input value
> agent-browser get title                   # page title
> agent-browser get url                     # current URL
> agent-browser get count ".item"           # count matching elements
> ```
> 
> ## Interacting
> 
> ```bash
> agent-browser click @e1                   # click
> agent-browser click @e1 --new-tab         # open link in new tab instead of navigating
> agent-browser dblclick @e1                # double-click
> agent-browser hover @e1                   # hover
> agent-browser focus @e1                   # focus (useful before keyboard input)
> agent-browser fill @e2 "hello"            # clear then type
> agent-browser type @e2 " world"           # type without clearing
> agent-browser press Enter                 # press a key at current focus
> agent-browser press Control+a             # key combination
> agent-browser check @e3                   # check checkbox
> agent-browser uncheck @e3                 # uncheck
> agent-browser select @e4 "option-value"   # select dropdown option
> agent-browser select @e4 "a" "b"          # select multiple
> agent-browser upload @e5 file1.pdf        # upload file(s)
> agent-browser scroll down 500             # scroll page (up/down/left/right)
> agent-browser scrollintoview @e1          # scroll element into view
> agent-browser drag @e1 @e2                # drag and drop
> ```
> 
> ### When refs don't work or you don't want to snapshot
> 
> Use semantic locators:
> ```

## 🤖 Claude *(04:38:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nagent-browser open \"http://localhost:4319/privacy\" 2>&1 | tail -3\nagent-browser wait --load networkidle 2>&1 | tail -2\nsleep 1\necho \"=== HEADINGS (h2) ===\"\nagent-browser eval \"Array.from(document.querySelectorAll('h2')).map(h=>h.textContent.trim()).join('\\n')\" 2>&1 | tail -20\necho \"=== TITLE/UPDATE DATE ===\"\nagent-browser eval \"document.body.innerText.match(/\u00daltima atualiza\u00e7\u00e3o:[^\\n]*/)?.[0] || 'NOT FOUND'\" 2>&1 | tail -3",
  "description": "Open /privacy and extract h2 headings + update date"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Magic Constellation
>   http://localhost:4319/privacy
> ✓ Done
> === HEADINGS (h2) ===
> "1. Introdução\n2. Dados do Usuário do Google\n3. Coleta e Uso de Dados\n4. Compartilhamento de Dados\n5. Segurança e Retenção\n6. Revogação de Acesso e Exclusão de Tokens\n7. Seus Direitos\n8. Alterações nesta Política"
> === TITLE/UPDATE DATE ===
> "Última atualização: 28 de Junho de 2026"
> ```

## 🤖 Claude *(04:38:47)*


## 🤖 Claude *(04:38:48)*

Renderiza perfeito — 8 headings, incluindo as 2 novas seções e o "7. Seus Direitos" renumerado, data atualizada. Vou capturar a screenshot e confirmar os trechos-chave (cláusula de IA + segurança), depois encerro.

## 🤖 Claude *(04:38:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSHOT=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png\"\nagent-browser screenshot \"$SHOT\" --full-page 2>&1 | tail -2\necho \"=== AI clause present? ===\"\nagent-browser eval \"document.body.innerText.includes('treinar modelos de intelig\u00eancia artificial') ? 'AI_CLAUSE_OK' : 'MISSING'\" 2>&1 | tail -1\necho \"=== Security concrete? ===\"\nagent-browser eval \"document.body.innerText.includes('criptografia tanto em tr\u00e2nsito') ? 'SECURITY_OK' : 'MISSING'\" 2>&1 | tail -1\necho \"=== Google permissions link href? ===\"\nagent-browser eval \"document.querySelector('a[href*=\\\"myaccount.google.com/permissions\\\"]')?.href || 'MISSING'\" 2>&1 | tail -1\nagent-browser close 2>&1 | tail -1\necho \"SHOT=$SHOT\"; ls -la \"$SHOT\"",
  "description": "Screenshot + verify AI clause, security, permissions link render"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 2
> ✓ Screenshot saved to --full-page
> === AI clause present? ===
> "AI_CLAUSE_OK"
> === Security concrete? ===
> "SECURITY_OK"
> === Google permissions link href? ===
> "https://myaccount.google.com/permissions"
> ✓ Browser closed
> SHOT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png
> ls: cannot access '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png': No such file or directory
> ```

## 🤖 Claude *(04:39:03)*


## 🤖 Claude *(04:39:03)*

Os checks de DOM passaram todos (cláusula IA ✓, segurança concreta ✓, link Google permissions ✓). A screenshot salvou com nome errado (a flag virou filename). Vou recapturar corretamente para o registro visual:

## 🤖 Claude *(04:39:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nls -la -- --full-page 2>/dev/null && rm -f -- --full-page\nSHOT=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png\"\nagent-browser open \"http://localhost:4319/privacy\" 2>&1 | tail -1\nagent-browser wait --load networkidle 2>&1 | tail -1\nagent-browser screenshot \"$SHOT\" 2>&1 | tail -1\nagent-browser close 2>&1 | tail -1\nls -la \"$SHOT\"\n# stop preview server\npkill -f \"vite preview --port 4319\" 2>/dev/null && echo \"preview stopped\" || echo \"preview already gone\"",
  "description": "Re-capture screenshot properly and stop preview"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 144
> -rw-rw-r-- 1 ubuntu ubuntu 83509 Jun 28 01:38 --full-page
>   http://localhost:4319/privacy
> ✓ Done
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png
> ✓ Browser closed
> -rw-rw-r-- 1 ubuntu ubuntu 83509 Jun 28 01:39 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png
> ```

## 🤖 Claude *(04:39:12)*


## 🤖 Claude *(04:39:13)*

Screenshot capturada (83KB). Vou ver a renderização para confirmar visualmente (Lei 1 — ver de fato):

## 🤖 Claude *(04:39:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(04:39:27)*


## 🤖 Claude *(04:39:40)*

A página renderiza limpa — título, data **28 de Junho de 2026**, seções na ordem certa. Render verificado de ponta a ponta.

Pronto, Maestro. Os 4 ajustes que o coowork apontou estão **aplicados, no ar e verificados materialmente**.

## O que foi feito em [src/pages/PrivacyPolicy.tsx](src/pages/PrivacyPolicy.tsx)

| # | Lacuna | Como ficou |
|---|--------|-----------|
| 1 | **Treino de IA** (crítico) | Cláusula nova na §2: *"…NÃO retém, usa ou transfere dados do Google… para desenvolver, melhorar ou treinar modelos de IA/ML generalizados ou não personalizados (incluindo modelos fundacionais)"* + explicita que *"melhorar nossos serviços"* **não** inclui treino sobre dados do Google. |
| 2 | **Aviso de alterações** | Nova **§8 — Alterações nesta Política**: publica versão revisada + notifica e pede novo consentimento antes de mudar o uso dos dados do Google. |
| 3 | **Revogação / tokens** | Nova **§6 — Revogação de Acesso e Exclusão de Tokens**: 2 caminhos (desconectar no app + `myaccount.google.com/permissions`) e que os access/refresh tokens são **excluídos** ao desconectar. |
| 4 | **Segurança concreta** | §5 trocou "medidas robustas" por **criptografia em trânsito (TLS/HTTPS) e em repouso + controles de acesso**. |

Também atualizei a data para **28 de Junho de 2026** (a §8 usa a data como sinal de mudança) e renumerei "Seus Direitos" → §7.

## Rigor aplicado (não improvisei a redação)
- Fundamentei o texto na **política oficial do Google** (workflow de pesquisa + revisão adversarial). Achado-chave: a cláusula **vinculante** do Google é *"create, train, or improve a machine learning or AI model beyond that specific user's personalized model"* — meu texto cobre essa formulação **e** a paráfrase "generalizado/não-personalizado", que é a redação mais segura para passar na verificação. O revisor adversarial aprovou os 4 (`passes: true`).

## Provas materiais (Lei 1)
- **tsc**: exit 0 (zero erros).
- **Build+deploy**: `bun run build` ✓ em 26.76s → `dist/assets/PrivacyPolicy-IF1BhbgS.js`; env Supabase baked (9 chunks); nginx serve o entry+chunk novos. Todas as 6 âncoras de texto batem no chunk servido.
- **Render real** (preview local do dist, sem CF): 8 headings na ordem correta, cláusula de IA ✓, segurança ✓, link `myaccount.google.com/permissions` ✓, data nova ✓.

## 🤖 Claude *(04:39:44)*


🛠️ **Tool Call**: `SendUserFile`
```json
{
  "__unparsedToolInput": {
    "raw": "{\"files\": /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png, \"caption\": \"Pol\u00edtica de Privacidade renderizada do dist novo \u2014 data 28/Jun/2026 e se\u00e7\u00f5es atualizadas\", \"status\": \"normal\"}",
    "len": 262
  }
}
```

> **Tool Result (SendUserFile)** - ❌ Error
>
> ```
> <tool_use_error>InputValidationError: SendUserFile was called with input that could not be parsed as JSON.
> You sent (first 200 of 262 bytes): {"files": /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png, "caption": "Política de Privacidade renderizada do dist novo
> Common causes: unescaped backslashes in file paths (use / or \\), unescaped control characters, or truncated output. Retry with valid JSON.</tool_use_error>
> ```

## 🤖 Claude *(04:39:48)*


🛠️ **Tool Call**: `SendUserFile`
```json
{
  "files": [
    "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/760b6087-837f-483e-be18-bcfc2f4fc89a/scratchpad/privacy-rendered.png"
  ],
  "caption": "Pol\u00edtica de Privacidade renderizada do dist novo \u2014 data 28/Jun/2026 e se\u00e7\u00f5es atualizadas",
  "status": "normal"
}
```

> **Tool Result (SendUserFile)** - ✅ Success
>
> ```
> 1 file delivered to user.
> ```

## 🤖 Claude *(04:39:55)*


## 🤖 Claude *(04:39:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "pgrep -fa \"vite preview --port 4319\" >/dev/null && { pkill -f \"vite preview --port 4319\"; echo \"preview stopped now\"; } || echo \"preview not running \u2705\"\nls -la -- --full-page 2>/dev/null && rm -f -- --full-page && echo \"stray file removed\" || echo \"no stray file \u2705\"\ngit status --short",
  "description": "Cleanup preview + stray file, show git status"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 144
> ```

## 🤖 Claude *(04:40:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git status --short; echo \"---\"; pgrep -fa \"vite preview\" || echo \"no vite preview running\"",
  "description": "Confirm git status and no lingering preview"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  M src/pages/PrivacyPolicy.tsx
> ---
> 889452 /bin/bash -c source /home/ubuntu/.claude/shell-snapshots/snapshot-bash-1782620795876-7ra401.sh 2>/dev/null || true && shopt -u extglob 2>/dev/null || true && eval 'git status --short; echo "---"; pgrep -fa "vite preview" || echo "no vite preview running"' < /dev/null && pwd -P >| /tmp/claude-9fa4-cwd
> ```

## 🤖 Claude *(04:40:06)*


## 🤖 Claude *(04:40:13)*

Tudo verificado e limpo. Resumo final:

- ✅ **No ar agora** em `https://login.mcorch.com/privacy` (dist servido pelo nginx). Faça **hard-refresh (Ctrl+Shift+R)** no browser — o Cloudflare pode estar cacheando a versão antiga.
- ⚠️ A edição está **no working tree, não commitada** (`M src/pages/PrivacyPolicy.tsx`). O deploy não depende do commit (o nginx serve o `dist/`), mas para preservar no git é bom selar.

Dois pontos que **só você confirma** (fora do que dá pra ver daqui, como o coowork também notou):
1. `mcorch.com` verificado como seu no Search Console.
2. As URLs na tela de consentimento OAuth (Google Cloud Console) apontando exatamente para `/privacy` e a home.

E o lembrete jurídico do coowork continua valendo: isto é conformidade técnica com os requisitos do Google, não aconselhamento jurídico.

Quer que eu **commite** essa mudança (`fix(legal): privacy policy — Google OAuth Limited Use/AI-training/revocation/security`)? Posso commitar só isso, ou rodar o `/handoff` completo se preferir selar a sessão.

## 👤 User *(14:25:42)*

<command-message>handoff</command-message>
<command-name>/handoff</command-name>

## 👤 User *(14:25:42)*

# ShakeHands — Session Seal Protocol v4

Execute the ShakeHands /handoff ritual to seal this session.

> **v4 (2026-05-15):** Reordered phases — Knowledge Mesh Milestone (Phase 3) now runs
> **before** README.md update (Phase 4), so the live node count query captures the handoff
> node itself. Previously the badge was always 1-3 nodes behind.
>
> **v3 (2026-05-14):** Added Phase 6 BoK Seal Status — verifies any module
> work in this session has a corresponding sealed BoK suite per MCORCH Master
> Execution Protocol. Blocks seal if significant module work lacks BoK.

---

## PRE-FLIGHT (execute ALL in parallel before anything else)

```bash
git status --short                          # inventory uncommitted changes
git diff HEAD --stat                        # change scope
git log --oneline -7                        # recent history + commit style
npx tsc --noEmit 2>&1 | tail -20           # TypeScript strict check
docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
docker ps --filter "name=mega-brain" --format "{{.Names}}: {{.Status}}"
curl -s http://localhost:8001/api/v2/heartbeat  # chroma API v2 health
```

Read in parallel:
- `HANDOFF.md` (current state, pending actions)
- `CLAUDE.md` (architecture rules)
- `/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md`

If TypeScript has errors → fix them before proceeding. Report any infra anomalies in the final summary.

---

## PHASE 1 — SECURITY AUDIT

Run these checks and report findings. **Block the seal if any CRITICAL finding exists.**

> ⚠️ **SCOPE NOTE:** This phase scans changes that exist NOW (before Phase 5 writes HANDOFF.md).
> A second mandatory scan runs in Phase 5b, after HANDOFF.md is written and before it is committed.

```bash
# 1a. Secret leak scan — check staged + working tree for hardcoded credentials
git diff HEAD | grep -E "(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{20,}|STRIPE_|SECRET_KEY|ACCESS_TOKEN|api_key\s*=\s*['\"][^'\"]{10,})" \
  | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_" | head -20

# 1b. Edge function JWT enforcement — every user-facing function must verify JWT
grep -rL "Authorization\|jwt\|JWT\|service_role" supabase/functions/*/index.ts \
  | grep -v "get-infra-status\|watchdog" || echo "ALL FUNCTIONS: JWT enforced ✅"

# 1c. Client-side coin deduction guard — must NEVER update mco_balance directly from client
grep -rn "mco_balance.*update\|UPDATE.*mco_balance" src/ \
  | grep -v "settings\|top.up\|topup\|SettingsPage" | head -10 || echo "NO VIOLATIONS ✅"

# 1d. RLS bypass risk — check for supabase.rpc calls without auth context
grep -rn "service_role\|bypass.*rls\|rls.*bypass" src/ | head -10 || echo "NO VIOLATIONS ✅"

# 1e. Sensitive data in console.log
grep -rn "console\.log.*token\|console\.log.*key\|console\.log.*secret\|console\.log.*password" src/ \
  | head -10 || echo "NO SENSITIVE LOGS ✅"
```

**Security verdict:** list each check as ✅ PASS / ⚠️ WARN / 🔴 BLOCK.
Only proceed if no 🔴 findings.

---

### DOCUMENTATION CREDENTIAL RULE (invariant — never violate)

**When writing HANDOFF.md, README.md, or any committed documentation:**

- ✅ DO: describe WHERE a credential is stored → `VITE_GEMINI_API_KEY` is set in `.env` (local) and `GEMINI_API_KEY` in the Supabase vault
- ✅ DO: reference digest/fingerprint if useful → `GEMINI_API_KEY (digest 0fe0e159...)`
- 🔴 NEVER: include the actual credential value → `AIzaSyBv...`, `sk-...`, `eyJ...`

> **Rationale:** Phase 1 scans changes that predate the HANDOFF.md write. Any credential embedded
> in HANDOFF.md during Phase 5 escapes Phase 1 entirely and goes directly to the remote.
> This rule is the primary prevention layer; Phase 5b is the detection backstop.

---

## PHASE 2 — GRANULAR COMMITS

Group uncommitted changes by concern and commit each group separately.

**Commit rules (from memory + project convention):**
- Prefix: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`
- Body: one paragraph explaining the WHY (milestone orientation, not diff description)
- **NEVER** add `Co-Authored-By` trailer
- **NEVER** use `git add -A` — stage files explicitly by name
- Skip: `build_log.txt`, `node_modules/`, `dist/`, `.env`, `check_types.ts`, `scratch/`

Stage and commit each logical group before moving to the next phase.

---

## PHASE 3 — KNOWLEDGE MESH MILESTONE

> ⚠️ **ORDER MATTERS:** This phase runs BEFORE Phase 4 (README badge) so the live count
> query captures this handoff node. Do not swap the order.

Insert a milestone node into mcorch_nodes to mark this session in the knowledge graph:

```bash
source .env
SUPABASE_URL="https://bcyvddsykvehvpwstlfa.supabase.co"
SESSION_PHASE="<phase-name-slug>"
SESSION_SUMMARY="<one-sentence summary of what was accomplished>"

curl -s -X POST "${SUPABASE_URL}/rest/v1/mcorch_nodes" \
  -H "apikey: ${SB_SECRET_KEY}" \
  -H "Authorization: Bearer ${SB_SECRET_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d "{
    \"name\": \"session-handoff-$(date +%Y%m%d)-${SESSION_PHASE}\",
    \"node_type\": \"handoff\",
    \"content\": \"[HANDOFF SEAL] ${SESSION_SUMMARY}\",
    \"stability_score\": 1.0,
    \"project_id\": null,
    \"user_id\": null,
    \"metadata\": {
      \"session\": \"${SESSION_PHASE}\",
      \"sealed_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
      \"commits\": \"$(git log --oneline -5 | head -5 | tr '\n' '|')\"
    }
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Node ID:', d[0]['id'] if isinstance(d,list) else d.get('id','error'))" 2>/dev/null \
  || echo "⚠️ Knowledge Mesh insert failed — log manually"
```

Then trigger embedding for the new node:
```bash
NODE_ID="<id-from-above>"
curl -s -X POST "${SUPABASE_URL}/functions/v1/embed-mcorch-node" \
  -H "apikey: ${SB_SECRET_KEY}" \
  -H "Authorization: Bearer ${SB_SECRET_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"record\": {\"id\": \"${NODE_ID}\"}}" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Embedded:', d)" 2>/dev/null \
  || echo "⚠️ Embedding failed — node persisted but not vectorized"
```

Emit `proof-manifest.json` so Phase 5c can verify this handoff node strictly:
```bash
echo "{\"handoffNodeId\": \"${NODE_ID}\"}" > proof-manifest.json
```

---

## PHASE 4 — README.md UPDATE

> ℹ️ Phase 3 (milestone node) has already been inserted — the live count below includes it.

Update `/README.md` to reflect the current session's work.

**Required updates:**
1. **Badges block** (top of file) — update dynamic values:
   - `neural_mesh-XXX_nodes` badge → fetch real count:
     ```bash
     curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id&limit=1" \
       -H "apikey: $(grep SB_SECRET_KEY .env | cut -d'"' -f2)" \
       -H "Authorization: Bearer $(grep SB_SECRET_KEY .env | cut -d'"' -f2)" \
       -H "Prefer: count=exact" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'
     ```
   - `version-X.X.X` badge → increment patch version (or minor if major feature landed)
   - If new phase shipped → add phase badge (e.g. `Phase_Zeta-live-cyan`)

2. **Phase Status table** — add new row for this session's phase:
   ```
   | Phase Zeta — <Name> | ✅ <one-line summary> |
   ```

3. **What's New section** — prepend a new entry under the most recent one:
   ```markdown
   ### [v5.X.X] — <Phase Name> (<date>)
   - <bullet: major feature 1>
   - <bullet: major feature 2>
   ```

4. **Core metrics** (if present in README) — update node/edge counts.

Commit README separately:
```
docs(readme): vX.X.X — <phase name> — <one-line change summary>
```

---

## PHASE 5 — HANDOFF.md UPDATE

Rewrite the relevant sections of `HANDOFF.md` — **append, never replace history**.

**Required updates:**
1. **Task State table** — add new row:
   ```
   | **<Phase Name>** | ✅ <one-line summary> |
   ```

2. **New Record section** — add at the top of the history (after the Task State table):
   ```markdown
   ## <Phase Name> Record (<YYYY-MM-DD>)

   <one-paragraph prose summary of what changed and why>

   | Action | Result |
   |--------|--------|
   | `<file/function changed>` | ✅ <what it does now> |
   ...

   | Commit | Conteúdo |
   |--------|----------|
   | `<hash>` | <message> |
   ...

   ### Arquitetura <Phase Name>
   ```code block with data flow or key architecture diagram```
   ```

3. **Pending Actions** — check off completed items (~~strikethrough~~), add new ones discovered this session.

4. **GraphRAG State** section — update node/edge counts.

5. **Infrastructure** table — update container health.

---

## PHASE 5b — HANDOFF.md SECRET SCAN (mandatory before commit)

**Run this scan on the HANDOFF.md content about to be committed. Block if any finding exists.**

```bash
# 5b-1. Scan HANDOFF.md for real credential values
grep -nE "(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]+|[a-zA-Z0-9]{32,}=\s*['\"]?[A-Za-z0-9+/]{40,})" HANDOFF.md \
  | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_\|digest\|sha256\|hash\|fingerprint" \
  | head -20 || echo "HANDOFF.md: NO CREDENTIALS FOUND ✅"

# 5b-2. Specifically check for Google API keys (AIza prefix = 39 chars total)
grep -n "AIza[0-9A-Za-z_-]\{35\}" HANDOFF.md | head -10 || echo "NO GOOGLE API KEYS ✅"

# 5b-3. Check for any = "value" pattern that looks like a real assignment
grep -nE "=\s*['\"][A-Za-z0-9_\-]{20,}['\"]" HANDOFF.md \
  | grep -v "example\|placeholder\|<.*>\|your-\|YOUR_\|digest\|hash\|uuid\|id.*[0-9a-f-]\{36\}" \
  | head -10 || echo "NO INLINE ASSIGNMENTS ✅"
```

**If any check returns a match:**
1. 🔴 **DO NOT COMMIT** HANDOFF.md
2. Rewrite the offending section — replace the actual value with its location description
3. Re-run Phase 5b until all checks pass
4. Only then proceed to commit HANDOFF.md

Commit HANDOFF.md only after Phase 5b passes:
```
docs(handoff): seal <phase name> — <one-line summary>
```

---

## PHASE 5c — MATERIAL PROOF AUDIT (mandatory before push)

**Independently re-verify every material-proof claim of this seal. Block if any is contradicted.**

> ⚠️ Closes the Survival Law 1 (Materiality) self-grading weakness — this audit is mechanical,
> not self-reported. Skill: `mcorch-qa-healing` · SOP: `docs/processes/handoff-material-proof-audit.md`.

```bash
# Runs after Phase 5b, so the newest HANDOFF.md Record block is this seal's.
bun run scripts/qa/run-audit.ts HANDOFF.md
```

The audit parses the newest `## … Record` block and verifies each claim — commit hashes
(`git cat-file`), mesh UUIDs (`mcorch_nodes`/`mcorch_edges`), `tsc --noEmit`, the test suite,
edge-function reachability, file paths — then prints a Proof Manifest table and exits.

**Gate verdict:**
- **exit 0 — `SEAL ALLOWED`** → embed the Proof Manifest in the Phase 8 report (`📋 PROVA MATERIAL`); proceed to Phase 6.
- **exit 1 — `SEAL BLOCKED`** → 🔴 **BLOCK the seal.** Do NOT push. For each 🔴, fix the real
  cause — never fabricate proof (Law 1) — and re-run this phase until `SEAL ALLOWED`. If a 🔴 is a
  strict handoff-node claim, re-attempt the Phase 3 insert once (SOP Cenário D), then re-run.
- `⏭ skip` rows (infra unreachable · non-mesh UUID · size-only deploy) never block — report them.

---

## PHASE 6 — BoK SEAL STATUS (mandatory before push)

**Verify any significant module work in this session has a sealed BoK suite per CLAUDE.md MCORCH Master Execution Protocol.**

```bash
# 6-1. List BoK suites present + check completeness
for slug in $(ls docs/bok/ 2>/dev/null); do
  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)
  missing=()
  for doc in "${required[@]}"; do
    [ -f "docs/bok/$slug/$doc.md" ] || missing+=("$doc")
  done
  [ ${#missing[@]} -eq 0 ] \
    && echo "✅ $slug — BoK complete (9 docs)" \
    || echo "⚠️ $slug — incomplete (missing: ${missing[*]})"
done

# 6-2. Check session touched code in new src/pages/ or new supabase/functions/ that lacks BoK
session_new_modules=$(git diff --name-only HEAD~10..HEAD 2>/dev/null | grep -E "^(src/pages/|supabase/functions/|src/components/[A-Z])" | awk -F/ '{print "/"}' | sort -u)
echo "Session touched modules: $session_new_modules"

# 6-3. Mesh seal nodes for sealed BoK suites
source .env 2>/dev/null
if [ -n "$SB_SECRET_KEY" ]; then
  curl -s "$SUPABASE_URL/rest/v1/mcorch_nodes?node_type=eq.documentation_suite&select=id,name,stability_score,created_at" \
    -H "apikey: $SB_SECRET_KEY" \
    -H "Authorization: Bearer $SB_SECRET_KEY" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f\"  🌐 {n['name']} ({n['stability_score']})\") for n in d]" 2>/dev/null \
    || echo "  ⚠️ Could not query seal nodes"
fi
```

**Gate verdict:**
- ✅ All session modules have sealed BoK → proceed to Phase 7 push.
- ⚠️ Module work without BoK (e.g. `feat:` commit creating new page/edge fn without `docs/bok/<slug>/`)
  → 🔴 **BLOCK seal**. Run `/bok-scribe <module>` first OR add module to exemption list (typo/dep bump/single-file patch).

Report BoK status in final seal output (Phase 8).

---

## PHASE 7 — PUSH

```bash
git push origin main
```

Report: branch, number of commits pushed, remote URL.

If push fails (non-fast-forward): run `git pull --rebase origin main` first, then push again. Never force-push main.

---

## PHASE 7b — SPRINT & CONNECTIONS HYGIENE

### Sprint priorities update

Review `.claude/context/sprint-priorities.md` and update:
1. Check off completed items in "Skills a criar ou evoluir" and "Conexões a implementar"
2. Add new gaps discovered this session under "Top 3 Gap Closures" if applicable
3. Update the 4Cs Audit Snapshot scores if `/audit` was run this session
4. Append to the Retrospective section if this was the last session of the sprint

Commit if changed:
```
chore(sprint): update sprint-priorities — <one-line progress note>
```

### Scratch cleanup

```bash
ls scratch/ 2>/dev/null
```

If `scratch/` has `.ts` diagnostic scripts, move them to `.claude/scripts/db/`:
```bash
mkdir -p .claude/scripts/db
mv scratch/*.ts .claude/scripts/db/ 2>/dev/null && echo "Moved ✅" || echo "Nothing to move"
```

Commit if files were moved:
```
chore(scripts): migrate scratch diagnostics to .claude/scripts/db/
```

### MCP documentation check

```bash
cat .mcp.json
```

For each MCP server listed, verify it has an entry in `.claude/references/` or is documented in CLAUDE.md. If a new MCP was added this session and has no documentation, add a one-liner to the relevant reference file.

---

## PHASE 8 — FINAL REPORT

Print seal summary in **Portuguese (Brasil)**:

```
═══════════════════════════════════════════════════════════
  HANDOFF SEALED — <PHASE NAME> (<date>)
═══════════════════════════════════════════════════════════

🔐 SEGURANÇA
  <security check results — each as ✅ / ⚠️ / 🔴>

📦 COMMITS (<N> total)
  <hash> — <message>
  ...

⬡ KNOWLEDGE MESH
  Milestone node: <node id> — <name>
  Embedding: ✅ / ⚠️

📖 README.md
  Versão: <old> → <new>
  Badge neural_mesh: <old> → <new> nós
  Seção adicionada: <section name>

🧠 HANDOFF.md
  Fase selada: <phase name>
  Seções atualizadas: Task State, Record, Pending Actions, GraphRAG State

📋 PROVA MATERIAL (Fase 5c)
  Veredito: <SEAL ALLOWED / SEAL BLOCKED>
  Claims: <N> verificadas · <M> skipped · <K> falhas

🚀 PUSH
  Branch: main → origin/main
  Commits enviados: <N>

📌 SPRINT
  sprint-priorities.md: <atualizado ✅ / sem mudanças>
  scratch/ cleanup: <arquivos movidos ✅ / limpo ✅>
  MCP docs: <ok ✅ / pendência: X>

⏭  PRÓXIMOS PASSOS
  1. <top pending action>
  2. <second pending action>
  3. <third pending action>

═══════════════════════════════════════════════════════════
  Assinado: Claude Code — Braço de Engenharia do AIOS
═══════════════════════════════════════════════════════════
```

**Invariants — never skip:**
- Security audit must run and report before any commit (Phase 1)
- **Phase 3 (milestone node) must run BEFORE Phase 4 (README badge query)** — ensures count includes the handoff node
- **Phase 5b secret scan must run on HANDOFF.md before its commit** — no exceptions
- **Phase 5c material proof audit must run and return `SEAL ALLOWED` before push** — a contradicted claim blocks the seal
- **Documentation must NEVER contain actual credential values** — only describe where they live
- README.md badge counts must reflect real DB state (query live, after milestone insert)
- HANDOFF.md must be updated even if nothing changed (session note)
- Push must happen — remote must always mirror local main
- Knowledge Mesh milestone must be attempted (failures are logged, not blocking)
- git pre-commit hook (`.git/hooks/pre-commit`) is the last barrier — do not bypass with `--no-verify`


## 🤖 Claude *(14:25:52)*

I'll execute the /handoff seal protocol. Starting with pre-flight + Phase 1 security audit in parallel.

## 🤖 Claude *(14:25:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git status --short; echo \"---stat---\"; git diff HEAD --stat; echo \"---log---\"; git log --oneline -7",
  "description": "Inventory changes + recent history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  M src/pages/PrivacyPolicy.tsx
> ---stat---
>  src/pages/PrivacyPolicy.tsx | 27 ++++++++++++++++++++++++---
>  1 file changed, 24 insertions(+), 3 deletions(-)
> ---log---
> 6c30136 docs(readme): v6.58.0 badge + neural_mesh 8980 nodes (distribution mapping complete)
> 2116904 chore(deno): lock pdf-lib deps for generate-carousel
> 390eb0a docs(handoff): seal distribution mapping complete — CP-008/010/011 (sem pular nada)
> 293b041 feat(reshaper): PDF carousel generation (FR-CP-009, CP-011 partial)
> 6c3bc66 feat(publish): X thread + FB photo + Pinterest image-pin branches (CP-010 partial)
> 2e4c3fb feat(reshaper): 16:9 YouTube long-form render (FR-CP-004, OTD-CP-008 closed)
> e34a14e docs(handoff): seal reshaper continuation — publish opt-in + image reframe (OTD-CP-009 closed)
> ```

## 🤖 Claude *(14:25:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -10; echo \"TSC_EXIT=$?\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> TSC_EXIT=0
> ```

## 🤖 Claude *(14:25:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---chroma---\"; curl -s http://localhost:8001/api/v2/heartbeat",
  "description": "Infra health"
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
> ---chroma---
> {"nanosecond heartbeat":1782656756192944549}
> ```

## 🤖 Claude *(14:25:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== 1a. Secret leak scan ===\"\ngit diff HEAD | grep -E \"(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{20,}|STRIPE_|SECRET_KEY|ACCESS_TOKEN)\" | grep -v \"example\\|placeholder\\|<.*>\\|your-key\\|YOUR_\\|access tokens\\|refresh tokens\\|access token\\|tokens de acesso\" | head -20 || echo \"NO SECRETS \u2705\"\necho \"=== 1e. Sensitive console.log (src) ===\"\ngrep -rn \"console\\.log.*token\\|console\\.log.*secret\\|console\\.log.*password\" src/ | head -10 || echo \"NO SENSITIVE LOGS \u2705\"",
  "description": "Security scan 1a + 1e"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === 1a. Secret leak scan ===
> === 1e. Sensitive console.log (src) ===
> src/test/canvas-video-async-smoke.test.ts:239:    console.log("🔒 [GATE 5] Probing webhook endpoint with an invalid token...");
> src/test/canvas-video-async-smoke.test.ts:247:    console.log(`✅ [GATE 5] Verified endpoint security blocks invalid tokens with status: ${secResp.status}`);
> src/test/canvas-video-async-smoke.test.ts:252:    console.log("🔁 [GATE 6] Probing webhook endpoint with duplicate callback token (replay defense)...");
> ```

## 🤖 Claude *(14:26:09)*


## 🤖 Claude *(14:26:13)*

**Pre-flight + Phase 1:** worktree limpo exceto `src/pages/PrivacyPolicy.tsx` (24+/3-), tsc exit 0, infra 100% healthy. Segurança: 1a sem secrets ✅; 1e os matches são strings de teste pré-existentes (`canvas-video-async-smoke.test.ts`, probes de token inválido — não são credenciais, não são desta sessão) ✅. 1b/1c/1d = N/A (toquei só uma página TSX de texto — sem edge fn, sem `mco_balance`, sem rpc). Nenhum 🔴.

**Phase 2 — Commit granular** (grupo único: o fix legal):

## 🤖 Claude *(14:26:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add src/pages/PrivacyPolicy.tsx\ngit commit -m \"fix(legal): privacy policy \u2014 Google OAuth compliance (Limited Use / AI-training / revocation / security)\n\nCloses the 4 gaps a reviewer flagged against Google's OAuth app verification\nrequirements (support.google.com/cloud/answer/13806988) for an AI app that\nstores Google OAuth tokens. Wording grounded in Google's binding Limited Use\nclause and adversarially verified before shipping:\n\n- AI training: explicit clause that Google user data is NOT used to develop,\n  improve, or train generalized/non-personalized (incl. foundational) AI/ML\n  models; clarifies that 'melhorar nossos servi\u00e7os' excludes such training.\n- Section 6 (new): access revocation + token deletion (in-app disconnect +\n  myaccount.google.com/permissions; access/refresh tokens deleted on disconnect).\n- Section 8 (new): change-notice clause (notify + re-consent before new use of\n  Google data).\n- Section 5: concrete security wording (encryption in transit TLS/HTTPS + at\n  rest + access controls) replacing vague 'medidas robustas'.\n- Update date bumped to 28 Jun 2026; 'Seus Direitos' renumbered to 7.\" 2>&1 | tail -15",
  "description": "Commit privacy policy fix"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.07 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.03 seconds)
> ✔️ gitleaks-staged (0.05 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> [main f40e989] fix(legal): privacy policy — Google OAuth compliance (Limited Use / AI-training / revocation / security)
>  1 file changed, 24 insertions(+), 3 deletions(-)
> ```

## 🤖 Claude *(14:26:23)*


## 🤖 Claude *(14:26:25)*

Commit `f40e989` — hooks verdes (gitleaks/secret-scan ✅).

**Phase 3 — Knowledge Mesh milestone node** (antes do README para o count incluir este nó):

## 🤖 Claude *(14:26:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env\nSUPABASE_URL=\"https://bcyvddsykvehvpwstlfa.supabase.co\"\nSESSION_PHASE=\"privacy-policy-google-oauth-compliance\"\nSESSION_SUMMARY=\"Privacy policy hardened for Google OAuth app verification: AI-training prohibition clause (Limited Use), access-revocation + token-deletion section, change-notice section, concrete security wording (encryption in transit/at rest). Wording grounded in Google policy + adversarially verified; built, deployed to login.mcorch.com/privacy, browser-rendered verified.\"\n\nRESP=$(curl -s -X POST \"${SUPABASE_URL}/rest/v1/mcorch_nodes\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" \\\n  -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" \\\n  -H \"Prefer: return=representation\" \\\n  -d \"{\n    \\\"name\\\": \\\"session-handoff-$(date +%Y%m%d)-${SESSION_PHASE}\\\",\n    \\\"node_type\\\": \\\"handoff\\\",\n    \\\"content\\\": \\\"[HANDOFF SEAL] ${SESSION_SUMMARY}\\\",\n    \\\"stability_score\\\": 1.0,\n    \\\"project_id\\\": null,\n    \\\"user_id\\\": null,\n    \\\"metadata\\\": {\n      \\\"session\\\": \\\"${SESSION_PHASE}\\\",\n      \\\"sealed_at\\\": \\\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\\\",\n      \\\"commits\\\": \\\"$(git log --oneline -3 | tr '\\n' '|')\\\"\n    }\n  }\")\necho \"$RESP\" | python3 -c \"import sys,json; d=json.load(sys.stdin); print('Node ID:', d[0]['id'] if isinstance(d,list) else d.get('id','error'))\" 2>/dev/null || { echo \"RAW: $RESP\"; echo \"\u26a0\ufe0f insert failed\"; }",
  "description": "Insert handoff milestone node"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Node ID: d5476bb8-c5ea-4dc4-a3c0-86d1e0895456
> ```

## 🤖 Claude *(14:26:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env\nSUPABASE_URL=\"https://bcyvddsykvehvpwstlfa.supabase.co\"\nNODE_ID=\"d5476bb8-c5ea-4dc4-a3c0-86d1e0895456\"\ncurl -s -X POST \"${SUPABASE_URL}/functions/v1/embed-mcorch-node\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" \\\n  -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"record\\\": {\\\"id\\\": \\\"${NODE_ID}\\\"}}\" | python3 -c \"import sys,json; d=json.load(sys.stdin); print('Embedded:', d)\" 2>/dev/null || echo \"\u26a0\ufe0f Embedding failed\"\necho \"{\\\"handoffNodeId\\\": \\\"${NODE_ID}\\\"}\" > proof-manifest.json\ncat proof-manifest.json",
  "description": "Embed node + write proof manifest"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Embedded: {'error': 'Request body must contain { node_id: string }'}
> {"handoffNodeId": "d5476bb8-c5ea-4dc4-a3c0-86d1e0895456"}
> ```

## 🤖 Claude *(14:26:43)*


## 🤖 Claude *(14:26:43)*

O embed espera `{ node_id }`, não `{ record: { id } }`. Corrigindo:

## 🤖 Claude *(14:26:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env\nSUPABASE_URL=\"https://bcyvddsykvehvpwstlfa.supabase.co\"\nNODE_ID=\"d5476bb8-c5ea-4dc4-a3c0-86d1e0895456\"\ncurl -s -X POST \"${SUPABASE_URL}/functions/v1/embed-mcorch-node\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" \\\n  -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"node_id\\\": \\\"${NODE_ID}\\\"}\" | head -c 400\necho \"\"\necho \"=== verify embedding present ===\"\ncurl -s \"${SUPABASE_URL}/rest/v1/mcorch_nodes?id=eq.${NODE_ID}&select=id,embedding\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  | python3 -c \"import sys,json; d=json.load(sys.stdin); e=d[0].get('embedding'); print('embedding:', 'PRESENT ('+str(len(e))+' chars)' if e else 'NULL')\" 2>/dev/null",
  "description": "Re-embed with correct payload + verify"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"node_id":"d5476bb8-c5ea-4dc4-a3c0-86d1e0895456","dims":768,"chunks":1,"model":"openai/text-embedding-3-small","provider":"openrouter","stitched":0}
> === verify embedding present ===
> embedding: PRESENT (9505 chars)
> ```

## 🤖 Claude *(14:26:52)*


## 🤖 Claude *(14:26:53)*

Embedding presente (768d). **Phase 4 — README**: buscando count live (inclui o nó novo):

## 🤖 Claude *(14:26:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsource .env\nSUPABASE_URL=\"https://bcyvddsykvehvpwstlfa.supabase.co\"\nCOUNT=$(curl -s \"${SUPABASE_URL}/rest/v1/mcorch_nodes?select=id&limit=1\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$')\necho \"LIVE NODE COUNT: $COUNT\"\necho \"=== current README badges/version ===\"\ngrep -nE \"version-[0-9]|neural_mesh-[0-9]\" README.md | head -5",
  "description": "Live node count + current README badges"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> LIVE NODE COUNT: 8982
> === current README badges/version ===
> 3:  <img src="https://img.shields.io/badge/version-6.58.0--Distribution--Mapping--Complete-blueviolet?style=for-the-badge" alt="Version" />
> 6:  <img src="https://img.shields.io/badge/neural_mesh-8980_nodes-blueviolet?style=for-the-badge" alt="Neural Mesh" />
> ```

## 🤖 Claude *(14:27:00)*


## 🤖 Claude *(14:27:02)*

Count live: **8982**. Versão atual 6.58.0 → bump patch para **6.58.1** (fix legal, não feature). Lendo o topo do README + seção "What's New":

## 🤖 Claude *(14:27:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	<p align="center">
> 2	  <img src="https://img.shields.io/badge/status-production-brightgreen?style=for-the-badge" alt="Status" />
> 3	  <img src="https://img.shields.io/badge/version-6.58.0--Distribution--Mapping--Complete-blueviolet?style=for-the-badge" alt="Version" />
> 4	  <img src="https://img.shields.io/badge/license-proprietary-red?style=for-the-badge" alt="License" />
> 5	  <img src="https://img.shields.io/badge/typescript-strict-blue?style=for-the-badge&logo=typescript" alt="TypeScript" />
> 6	  <img src="https://img.shields.io/badge/neural_mesh-8980_nodes-blueviolet?style=for-the-badge" alt="Neural Mesh" />
> 7	  <img src="https://img.shields.io/badge/Agentic_Vision-21_patterns_%2B_Collective_Ledger-blueviolet?style=for-the-badge" alt="Agentic Vision" />
> 8	  <img src="https://img.shields.io/badge/API_Tenancy-100%25_per--user_(env%3Dinfra)-brightgreen?style=for-the-badge" alt="API Tenancy" />
> 9	  <img src="https://img.shields.io/badge/BoK_video--studio-9%2F9_%2B_agency_v1.1-fuchsia?style=for-the-badge" alt="BoK video-studio" />
> 10	  <img src="https://img.shields.io/badge/MCORCH_SSO-cross--subdomain_gate_live-darkgreen?style=for-the-badge" alt="MCORCH SSO" />
> 11	  <img src="https://img.shields.io/badge/Agency_Tenancy-org%2Fclient_RLS_sealed-blueviolet?style=for-the-badge" alt="Agency Tenancy" />
> 12	  <img src="https://img.shields.io/badge/viral--autopilot-ATIVADO_1o_ciclo_pago_%2B_FR--VA--018-brightgreen?style=for-the-badge" alt="Viral Autopilot" />
> 13	  <img src="https://img.shields.io/badge/social--connect-TikTok%2FYouTube_proven_E2E_%C2%B7_in_review-brightgreen?style=for-the-badge" alt="Social Connect" />
> 14	  <img src="https://img.shields.io/badge/channel--format-FR--CP--001_live_(8_canais)-brightgreen?style=for-the-badge" alt="Channel Format Intelligence" />
> 15	  <img src="https://img.shields.io/badge/Epsilon_V9-unified_canvas_3.4_live-cyan?style=for-the-badge" alt="Phase Epsilon V9" />
> 16	  <img src="https://img.shields.io/badge/test_coverage-295_tests-success?style=for-the-badge" alt="Test Coverage" />
> 17	  <img src="https://img.shields.io/badge/Cyber_Sentinel-prompt_gate_live_%2B_BoK_4%2F4-darkred?style=for-the-badge" alt="Cyber-Sentinel" />
> 18	  <img src="https://img.shields.io/badge/marketing--hub-FR--MH--001..012_live-brightgreen?style=for-the-badge" alt="Marketing Hub" />
> 19	  <img src="https://img.shields.io/badge/e2e--user--zero-v2_runnable_harness-teal?style=for-the-badge" alt="e2e-user-zero v2" />
> 20	  <img src="https://img.shields.io/badge/BoK_Suite-v1_sealed-fuchsia?style=for-the-badge" alt="BoK Suite" />
> 21	  <img src="https://img.shields.io/badge/AIOS_DevKit-4Cs_100%2F100-brightgreen?style=for-the-badge" alt="AIOS DevKit" />
> 22	  <img src="https://img.shields.io/badge/mcoCoins-gatekeeper-gold?style=for-the-badge" alt="mcoCoins" />
> 23	  <img src="https://img.shields.io/badge/AIOS-consciousness_v3-cyan?style=for-the-badge" alt="AIOS" />
> 24	  <img src="https://img.shields.io/badge/affiliate_flywheel-closed-emerald?style=for-the-badge" alt="Flywheel" />
> 25	  <img src="https://img.shields.io/badge/embedding_pipeline-autonomous-violet?style=for-the-badge" alt="Embedding Pipeline" />
> 26	  <img src="https://img.shields.io/badge/Core_Fable-Mega_Brain_%2B_Cymatics_%2B_A2UI-fuchsia?style=for-the-badge" alt="Core Fable" />
> 27	  <img src="https://img.shields.io/badge/LGPD-DD--001_%2B_DD--002_compliant-green?style=for-the-badge" alt="LGPD" />
> 28	  <img src="https://img.shields.io/badge/BoK_Agents-8_agents_generated-orange?style=for-the-badge" alt="BoK Agents" />
> 29	  <img src="https://img.shields.io/badge/Constellation_v2-backend_sealed-blueviolet?style=for-the-badge" alt="Constellation v2" />
> 30	  <img src="https://img.shields.io/badge/Departmental_Army-7_agents_%7C_9641_chunks-orange?style=for-the-badge" alt="Departmental Army" />
> 31	  <img src="https://img.shields.io/badge/Secrets_Vault-file--based_SecretRef-darkgreen?style=for-the-badge" alt="Secrets Vault" />
> 32	  <img src="https://img.shields.io/badge/mcoCoins_Ledger-canonical-gold?style=for-the-badge" alt="mcoCoins Ledger" />
> 33	  <img src="https://img.shields.io/badge/Nightly_Dreaming-gemini_embed_%2B_recovered-violet?style=for-the-badge" alt="Nightly Dreaming" />
> 34	  <img src="https://img.shields.io/badge/OpenClaw_Gateway-systemd_single--owner-darkgreen?style=for-the-badge" alt="OpenClaw Gateway" />
> 35	  <img src="https://img.shields.io/badge/Survival_Laws-4_of_4_consecutive-darkred?style=for-the-badge" alt="Survival Laws" />
> 36	  <img src="https://img.shields.io/badge/BoK_aios--sql--bridge-SDD_sealed-fuchsia?style=for-the-badge" alt="BoK aios-sql-bridge" />
> 37	  <img src="https://img.shields.io/badge/MAPE--K-audit_seeded-cyan?style=for-the-badge" alt="MAPE-K" />
> 38	  <img src="https://img.shields.io/badge/SQL_Bridge-aios--sql--bridge_live-darkgreen?style=for-the-badge" alt="SQL Bridge" />
> 39	  <img src="https://img.shields.io/badge/Circadian_Cycle-3_stages_BRT-violet?style=for-the-badge" alt="Circadian Cycle" />
> 40	  <img src="https://img.shields.io/badge/Canvas_4.2c-async_video_live-brightgreen?style=for-the-badge" alt="Canvas 4.2c" />
> 41	  <img src="https://img.shields.io/badge/Memory_Wiki-live_20_pages-darkviolet?style=for-the-badge" alt="Memory Wiki" />
> 42	  <img src="https://img.shields.io/badge/OE--661-flywheel_validated_E2E-emerald?style=for-the-badge" alt="OE-661 Flywheel Validated" />
> 43	  <img src="https://img.shields.io/badge/Target_Binding-100%25_coverage-success?style=for-the-badge" alt="Target Binding" />
> 44	  <img src="https://img.shields.io/badge/Link_Forge-3_real_products_enriched-orange?style=for-the-badge" alt="Link Forge" />
> 45	  <img src="https://img.shields.io/badge/Affiliate_Links-hybrid_meli.la%2Fmatt__word-emerald?style=for-the-badge" alt="Affiliate Links Hybrid" />
> 46	  <img src="https://img.shields.io/badge/Apify_BYOK-per--user_apify__token-teal?style=for-the-badge" alt="Apify BYOK" />
> 47	  <img src="https://img.shields.io/badge/API_Tenancy-per--user_credentials-teal?style=for-the-badge" alt="API Tenancy Model" />
> 48	  <img src="https://img.shields.io/badge/BoK_gamificacao--nodes-9_of_9_sealed-fuchsia?style=for-the-badge" alt="BoK gamificacao-nodes" />
> 49	  <img src="https://img.shields.io/badge/BoK_openclaw-9_of_9_sealed-fuchsia?style=for-the-badge" alt="BoK openclaw" />
> 50	  <img src="https://img.shields.io/badge/BoK_e2e--user--zero-9_of_9_sealed-fuchsia?style=for-the-badge" alt="BoK e2e-user-zero" />
> 51	  <img src="https://img.shields.io/badge/agent--browser-v0.27.0_validated-teal?style=for-the-badge" alt="agent-browser CLI" />
> 52	  <img src="https://img.shields.io/badge/ML_Affiliate-no_official_API_(probe--first)-red?style=for-the-badge" alt="ML Affiliate Probe" />
> 53	  <img src="https://img.shields.io/badge/Browser_Operator-runtime_blocked_at_datacenter-darkred?style=for-the-badge" alt="Browser Operator Probe" />
> 54	  <img src="https://img.shields.io/badge/Pantheon-7_agents_BoK_full-orange?style=for-the-badge" alt="Pantheon" />
> 55	  <img src="https://img.shields.io/badge/Material_Proof_Gate-Phase_5c_live-darkred?style=for-the-badge" alt="Material Proof Gate" />
> 56	  <img src="https://img.shields.io/badge/Admin_Panel-user_management_live-brightgreen?style=for-the-badge" alt="Admin Panel" />
> 57	  <img src="https://img.shields.io/badge/Great_Reset-Sovereign_soft--reset_live-darkred?style=for-the-badge" alt="Great Reset" />
> 58	  <img src="https://img.shields.io/badge/Constellation_Economic_Activation-agents_billable-gold?style=for-the-badge" alt="CEA" />
> 59	  <img src="https://img.shields.io/badge/Hybrid_Billing-Sovereign_free_others_charged-teal?style=for-the-badge" alt="Hybrid Billing" />
> 60	  <img src="https://img.shields.io/badge/Agent_Pricing-7_models_seeded-fuchsia?style=for-the-badge" alt="Agent Pricing" />
> ```

## 🤖 Claude *(14:27:07)*

Now updating the version + neural_mesh badges:

## 🤖 Claude *(14:27:09)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/version-6.58.0--Distribution--Mapping--Complete-blueviolet?style=for-the-badge\" alt=\"Version\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/version-6.58.1--Privacy--Policy--Google--OAuth--Compliance-blueviolet?style=for-the-badge\" alt=\"Version\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:27:16)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-8980_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-8982_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:27:19)*


## 🤖 Claude *(14:27:20)*

Agora a seção "What's New" — localizando:

## 🤖 Claude *(14:27:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"What's New|##.*What|### \\[v6\\.58|### \\[v6\\.5\" README.md | head -10",
  "description": "Locate What's New section"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 78:## 🆕 What's new in v6.58.0 (2026-06-28)
> 83:## 🆕 What's new in v6.57.0 (2026-06-28)
> 88:## 🆕 What's new in v6.56.0 (2026-06-28)
> 93:## 🆕 What's new in v6.55.0 (2026-06-27)
> 98:## 🆕 What's new in v6.54.0 (2026-06-27)
> 102:## 🆕 What's new in v6.53.0 (2026-06-27)
> 109:## 🆕 What's new in v6.52.0 (2026-06-26)
> 116:## 🆕 What's new in v6.51.0 (2026-06-25)
> 123:## 🆕 What's new in v6.50.0 (2026-06-25)
> 130:## 🆕 What's new in v6.45.0 (2026-06-22)
> ```

## 🤖 Claude *(14:27:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "offset": 76,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 76	</p>
> 77	
> 78	## 🆕 What's new in v6.58.0 (2026-06-28)
> 79	
> 80	- **Mapeamento de distribuição COMPLETO — 1 ideia → posts nativos em todos os formatos.** Fechados os 3 OTDs restantes do reshaper: **(CP-008)** render **16:9 YouTube long-form** — template determinístico `viral-long-16x9` (sha256-idêntico, NFR-VS-016), o reshaper enfileira o render on opt-in `long_form` e resolve 9:16 vs 16:9 pelo template (E2E: enqueue → render 548KB → resolve). **(CP-010)** novos publishers `publish-social` — **X thread** (reply-chain), **Facebook photo**, **Pinterest image-pin** (live E2E gated em conta conectada). **(CP-011)** **carrossel PDF** do LinkedIn (pdf-lib in-process, atoms → 6 slides), o formato de maior engajamento.
> 81	- **Cobertura nativa:** vídeo 9:16 (IG/TikTok/YT/Pinterest) + 16:9 (YT long) · texto (LinkedIn/X thread) · imagem (IG feed/Pinterest pin/FB card) · carrossel PDF (LinkedIn). Diferidos honestos: publishers binary-upload (LinkedIn media/FB Reels/X video — só prováveis com conta conectada) e auto-segment (N/A sem vídeo-fonte longo). `tsc` 0 · 4 smokes verdes (opt-in · reframe · carrossel · 16:9 E2E).
> 82	
> 83	## 🆕 What's new in v6.57.0 (2026-06-28)
> 84	
> 85	- **Publish opt-in — posts sociais nascem RASCUNHO (diretiva Sovereign).** Publicar é escolha explícita: a flag `auto_publish` (default OFF no fluxo manual; ON no autopilot ativado, honrando `hitl_required`) controla se o reshaper enfileira ou só gera rascunho. Nova edge fn `publish-channel-variant` publica um rascunho escolhido (owner-bound, idempotente). O enqueue social legado de LinkedIn/Twitter foi **aposentado** — o reshaper é a autoridade única (acabou o double-post). `/security-review` limpo.
> 86	- **Image reframe in-process (FR-CP-005/006 · OTD-CP-009 fechada).** Sem host worker/FFmpeg: o reshaper usa `imagescript` (WASM) para recortar+redimensionar+converter a imagem-pilar em **JPEG** na geometria de cada canal — IG/LinkedIn/FB feed **4:5**, Pinterest **2:3**, FB link-card **1.91:1**, YT thumbnail **16:9**. **IG feed_image agora publica** (via `image_url`). Smoke prova geometria exata + bytes JPEG baixados do bucket. **7 superfícies operacionais** a partir de 1 ideia.
> 87	
> ```

## 🤖 Claude *(14:27:38)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "## \ud83c\udd95 What's new in v6.58.0 (2026-06-28)\n\n- **Mapeamento de distribui\u00e7\u00e3o COMPLETO \u2014 1 ideia \u2192 posts nativos em todos os formatos.**",
  "new_string": "## \ud83c\udd95 What's new in v6.58.1 (2026-06-28)\n\n- **Pol\u00edtica de Privacidade endurecida para a verifica\u00e7\u00e3o do Google OAuth.** Fechadas as 4 lacunas que um revisor apontou contra os requisitos do Google (`support.google.com/cloud/answer/13806988`) para um app de IA que armazena tokens OAuth do Google: **(1) treino de IA** \u2014 cl\u00e1usula expl\u00edcita de que dados do Google N\u00c3O s\u00e3o usados para desenvolver/melhorar/treinar modelos de IA/ML generalizados ou n\u00e3o personalizados (Limited Use), com esclarecimento de que \"melhorar nossos servi\u00e7os\" exclui treino; **(2) revoga\u00e7\u00e3o + tokens** (nova \u00a76) \u2014 desconectar no app + `myaccount.google.com/permissions`, com exclus\u00e3o dos access/refresh tokens ao desconectar; **(3) aviso de altera\u00e7\u00f5es** (nova \u00a78) \u2014 notificar + re-consentir antes de novo uso; **(4) seguran\u00e7a concreta** (\u00a75) \u2014 criptografia em tr\u00e2nsito (TLS/HTTPS) e em repouso + controles de acesso, no lugar de \"medidas robustas\".\n- **Rigor:** reda\u00e7\u00e3o fundamentada na cl\u00e1usula vinculante de Limited Use do Google + revis\u00e3o adversarial (4/4 aprovados) antes do deploy. `tsc` 0 \u00b7 build+deploy provados materialmente (chunk servido + env baked) \u00b7 render verificado em browser real (8 se\u00e7\u00f5es, data 28/Jun/2026). Em produ\u00e7\u00e3o em `login.mcorch.com/privacy`.\n\n## \ud83c\udd95 What's new in v6.58.0 (2026-06-28)\n\n- **Mapeamento de distribui\u00e7\u00e3o COMPLETO \u2014 1 ideia \u2192 posts nativos em todos os formatos.**"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:27:42)*

Commit do README:

## 🤖 Claude *(14:27:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add README.md\ngit commit -m \"docs(readme): v6.58.1 badge + neural_mesh 8982 nodes (privacy policy Google OAuth compliance)\" 2>&1 | tail -4",
  "description": "Commit README update"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> [main 37eabe0] docs(readme): v6.58.1 badge + neural_mesh 8982 nodes (privacy policy Google OAuth compliance)
>  1 file changed, 7 insertions(+), 2 deletions(-)
> ```

## 🤖 Claude *(14:27:54)*


## 🤖 Claude *(14:27:54)*

README `37eabe0`. **Phase 5 — HANDOFF.md** (append, nunca substituir). Lendo o topo para inserir o novo Record:

## 🤖 Claude *(14:27:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 10,
  "limit": 8
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 10	---
> 11	
> 12	## Task State
> 13	
> 14	## Session Seal — Distribuição social: mapeamento COMPLETO — CP-008 (16:9) + CP-010 (publishers) + CP-011 (carrossel) (2026-06-28)
> 15	
> 16	Diretiva Sovereign: *"continue sem pular nada"*. Fechei os 3 OTDs restantes do reshaper, cada um provado materialmente (Lei 1) ou honestamente diferido com razão.
> 17	
> ```

## 🤖 Claude *(14:28:21)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "## Task State\n\n## Session Seal \u2014 Distribui\u00e7\u00e3o social: mapeamento COMPLETO \u2014 CP-008 (16:9) + CP-010 (publishers) + CP-011 (carrossel) (2026-06-28)",
  "new_string": "## Task State\n\n## Session Seal \u2014 Pol\u00edtica de Privacidade: conformidade Google OAuth (Limited Use / treino-IA / revoga\u00e7\u00e3o / seguran\u00e7a) (2026-06-28)\n\nDiretiva Sovereign: aplicar as 4 lacunas que o coowork apontou na auditoria das p\u00e1ginas legais (`login.mcorch.com/privacy`) contra os requisitos de verifica\u00e7\u00e3o de app OAuth do Google (`support.google.com/cloud/answer/13806988`) \u2014 \"o resto j\u00e1 verifiquei e est\u00e1 correto\". Tarefa cir\u00fargica em uma p\u00e1gina, mas com rigor de conformidade (rejei\u00e7\u00e3o na verifica\u00e7\u00e3o OAuth \u00e9 cara, sobretudo por ser app de IA).\n\n**Achado central (fundamentado, n\u00e3o improvisado):** disparei um workflow de pesquisa+revis\u00e3o adversarial sobre a pol\u00edtica REAL do Google. A cl\u00e1usula **vinculante** de IA do Google \u00e9 *\"create, train, or improve a machine learning or artificial intelligence model beyond that specific user's personalized model for the appropriate use case or user-facing feature\"* \u2014 que vive nas pol\u00edticas **product-specific** (Workspace/Photos), **n\u00e3o** na p\u00e1gina umbrella `api-services-user-data-policy`. A reda\u00e7\u00e3o \"generalizado / n\u00e3o-personalizado / fundacional\" \u00e9 par\u00e1frase fiel do intent. O texto novo cobre **as duas formula\u00e7\u00f5es** (a vinculante + a par\u00e1frase), que \u00e9 o mais seguro p/ passar no revisor. Revisor adversarial aprovou os 4 (`passes: true`, `overall_pass: true`).\n\n**As 4 lacunas fechadas em `src/pages/PrivacyPolicy.tsx`:**\n\n| # | Lacuna | Como ficou |\n|---|--------|-----------|\n| 1 | Treino de IA (cr\u00edtico) | Cl\u00e1usula na \u00a72: N\u00c3O ret\u00e9m/usa/transfere dados do Google p/ desenvolver, melhorar ou treinar modelos de IA/ML generalizados ou n\u00e3o personalizados (incl. fundacionais); IA/ML s\u00f3 no modelo personalizado do pr\u00f3prio user; \"melhorar nossos servi\u00e7os\" N\u00c3O inclui treino sobre dados do Google. |\n| 2 | Revoga\u00e7\u00e3o / tokens | Nova **\u00a76 \u2014 Revoga\u00e7\u00e3o de Acesso e Exclus\u00e3o de Tokens**: desconectar no app + `myaccount.google.com/permissions`; access/refresh tokens exclu\u00eddos ao desconectar. |\n| 3 | Aviso de altera\u00e7\u00f5es | Nova **\u00a78 \u2014 Altera\u00e7\u00f5es nesta Pol\u00edtica**: publica vers\u00e3o revisada + data; notifica e pede novo consentimento antes de novo uso dos dados do Google. |\n| 4 | Seguran\u00e7a concreta | \u00a75: criptografia em tr\u00e2nsito (TLS/HTTPS) e em repouso + controles de acesso (substitui \"medidas robustas\"). |\n\nData de atualiza\u00e7\u00e3o da pol\u00edtica \u2192 28/Jun/2026; \"Seus Direitos\" renumerado \u00a76\u2192\u00a77.\n\n| Action | Result |\n|--------|--------|\n| `src/pages/PrivacyPolicy.tsx` (24+/3-) | \u2705 4 lacunas aplicadas, grounded na pol\u00edtica Google + revis\u00e3o adversarial 4/4 |\n| Workflow grounding+verify (`wf_46126ab4-149`) | \u2705 2 research agents (quotes verbatim Google) + draft + adversarial verify; `overall_pass: true` |\n| `tsc --noEmit` | \u2705 exit 0 |\n| Build + deploy (build-deploy-guardian) | \u2705 `bun run build` 26.76s \u2192 `dist/assets/PrivacyPolicy-IF1BhbgS.js`; env baked (9 chunks); nginx serve entry+chunk novos; 6/6 \u00e2ncoras de texto no chunk servido |\n| Render real (preview local do dist, sem CF) | \u2705 8 headings na ordem certa; cl\u00e1usula IA + seguran\u00e7a + link `myaccount.google.com/permissions` + data nova confirmados via DOM eval + screenshot |\n\n| Commit | Conte\u00fado |\n|--------|----------|\n| `f40e989` | fix(legal): privacy policy \u2014 Google OAuth compliance (Limited Use / AI-training / revocation / security) |\n| `37eabe0` | docs(readme): v6.58.1 badge + neural_mesh 8982 nodes (privacy policy Google OAuth compliance) |\n\n**Pendente (s\u00f3 o Sovereign confirma \u2014 fora do alcance daqui):** (a) `mcorch.com` verificado como seu no Search Console; (b) URLs na tela de consentimento OAuth (Google Cloud Console) apontando exatamente p/ `/privacy` e a home. Lembrete jur\u00eddico do coowork mantido: isto \u00e9 conformidade t\u00e9cnica com os requisitos do Google, n\u00e3o aconselhamento jur\u00eddico.\n\n---\n\n## Session Seal \u2014 Distribui\u00e7\u00e3o social: mapeamento COMPLETO \u2014 CP-008 (16:9) + CP-010 (publishers) + CP-011 (carrossel) (2026-06-28)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:28:31)*


## 🤖 Claude *(14:28:31)*

Atualizando o GraphRAG State count + nó desta seal:

## 🤖 Claude *(14:28:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8438,
  "limit": 4
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8438	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8439	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8440	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8441	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> ```

## 🤖 Claude *(14:28:36)*


## 🤖 Claude *(14:28:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"^- \\*\\*8[0-9]{3} total nodes\" HANDOFF.md | head -3",
  "description": "Find GraphRAG total nodes header line"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 8426:- **8973 total nodes** (verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> ```

## 🤖 Claude *(14:28:44)*


## 🤖 Claude *(14:28:51)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "- **8973 total nodes** (verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d",
  "new_string": "- **8982 total nodes** (verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d \u2014 pol\u00edtica de privacidade endurecida p/ verifica\u00e7\u00e3o Google OAuth: cl\u00e1usula treino-IA Limited Use + \u00a76 revoga\u00e7\u00e3o/exclus\u00e3o de tokens + \u00a78 aviso de altera\u00e7\u00f5es + \u00a75 seguran\u00e7a concreta [criptografia tr\u00e2nsito/repouso]; grounded na pol\u00edtica Google + revis\u00e3o adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:28:55)*

**Phase 5b — Secret scan no HANDOFF.md** antes do commit:

## 🤖 Claude *(14:29:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== 5b-1 credentials ===\"\ngrep -nE \"(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]+)\" HANDOFF.md | grep -v \"example\\|placeholder\\|<.*>\\|your-key\\|YOUR_\\|digest\\|sha256\\|hash\\|fingerprint\" | head -20 || echo \"NO CREDENTIALS FOUND \u2705\"\necho \"=== 5b-2 google keys ===\"\ngrep -n \"AIza[0-9A-Za-z_-]\\{35\\}\" HANDOFF.md | head -10 || echo \"NO GOOGLE API KEYS \u2705\"\necho \"=== 5b-3 inline assignments ===\"\ngrep -nE \"=\\s*['\\\"][A-Za-z0-9_\\-]{20,}['\\\"]\" HANDOFF.md | grep -v \"example\\|placeholder\\|<.*>\\|your-\\|YOUR_\\|digest\\|hash\\|uuid\\|id.*[0-9a-f-]\\{36\\}\" | head -10 || echo \"NO INLINE ASSIGNMENTS \u2705\"",
  "description": "Phase 5b secret scan on HANDOFF.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === 5b-1 credentials ===
> === 5b-2 google keys ===
> === 5b-3 inline assignments ===
> 1331:- ✅ **FEITO (2026-06-08, commit `2522e71`)** Antibody anti-reincidência: optei por `no-restricted-syntax` core casando `JSXAttribute[name.name='dangerouslySetInnerHTML']` (não `react/no-danger` — `eslint-plugin-react` ausente, evita dep nova). Todo sink vira exceção `eslint-disable-next-line` justificada; 2 sinks legítimos marcados (DashboardHome DOMPurify · chart.tsx CSS shadcn). Provado material: sink cru plantado pego pelo lint, justificados passam, tsc 0; obs node `505fb670`.
> 5209:- Ledger ledger é canônico desde migration `20260516224541_deduct_mco_coins_ledger.sql`; ledger entry de reconciliação UUID `4caa9314-2fdf-4d60-9cb2-b7ed63bbcf5a` (`action='opening_balance_reconciliation'`, `amount=5533`) é o âncora histórico.
> 5242:**2) Phase 2 — OE02 Reconciliação do Ledger.** Direct INSERT em `mcoin_transactions` via service-role REST: HTTP 201 + UUID `4caa9314-2fdf-4d60-9cb2-b7ed63bbcf5a`, `action='opening_balance_reconciliation'`, `amount=5533`, `context={source: "SSP-01 OE02", directive, reconciled_at: "2026-05-17", drift_before: 5533, drift_after: 0, operator, reviewer, owner, audit_ref, sop_ref}`. Verificação pós-INSERT: `mco_balance=5533.00` (profiles) vs `SUM(amount)=5533` (mcoin_transactions) → **drift = 0**. SOP `mcoins-ledger-reconciliation.md` Step 5 Opção A executada à risca (action prefix `opening_balance_*` como manda anti-pattern). Outros 2 users (`924cb32e` balance 50; mais 2 com balance 0) ainda drift — registrado como OTD-V660-001 RPN 120 para próxima sessão.
> 7945:  ├── mcorch_nodes WHERE project_id = 'mcorch-constellation'  → 493 AST nodes
> 7947:  ├── mcorch_edges WHERE project_id = 'mcorch-constellation'  → 344 edges
> 7948:  └── count(embedding IS NULL, project_id = 'mcorch-constellation') → neuralDensity
> 7990:  ├── mcorch_nodes WHERE project_id = 'mcorch-constellation'  → 493 AST nodes
> 7992:  └── mcorch_edges WHERE project_id = 'mcorch-constellation'  → 344 edges
> ```

## 🤖 Claude *(14:29:07)*


## 🤖 Claude *(14:29:08)*

Phase 5b ✅ — 5b-1/5b-2 limpos; os matches de 5b-3 são UUIDs documentados e `project_id` strings (não credenciais), todos pré-existentes, nenhum da minha edição. Commitando HANDOFF.md:

## 🤖 Claude *(14:29:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add HANDOFF.md proof-manifest.json\ngit commit -m \"docs(handoff): seal privacy policy Google OAuth compliance \u2014 Limited Use / AI-training / revocation / security\" 2>&1 | tail -4",
  "description": "Commit HANDOFF.md + proof manifest"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> summary: (done in 0.01 seconds)
> ✔️ mesh-reingest (0.01 seconds)
> [main 1b085aa] docs(handoff): seal privacy policy Google OAuth compliance — Limited Use / AI-training / revocation / security
>  2 files changed, 36 insertions(+), 2 deletions(-)
> ```

## 🤖 Claude *(14:29:15)*

**Phase 5c — Material Proof Audit** (verificação mecânica independente):

## 🤖 Claude *(14:29:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nbun run scripts/qa/run-audit.ts HANDOFF.md 2>&1 | tail -40; echo \"AUDIT_EXIT=${PIPESTATUS[0]}\"",
  "description": "Phase 5c material proof audit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ### 📋 Proof Manifest — Material Proof Audit (Phase 5c)
> 
> | Claim | Kind | Expected | Actual | Verdict |
> |-------|------|----------|--------|---------|
> | mesh node 3459bfd3 | mesh_node | 3459bfd3-fa24-4785-99fb-1ebfda9dcf36 | 3459bfd3-fa24-4785-99fb-1ebfda9dcf36 | ✅ |
> | commit c3b8702 | git_commit | c3b8702 | c3b8702 | ✅ |
> | commit f273231 | git_commit | f273231 | f273231 | ✅ |
> | commit b2c39f6 | git_commit | b2c39f6 | b2c39f6 | ✅ |
> | commit bb999c1 | git_commit | bb999c1 | bb999c1 | ✅ |
> | commit 9bb5bba | git_commit | 9bb5bba | 9bb5bba | ✅ |
> | commit 7cbd036 | git_commit | 7cbd036 | 7cbd036 | ✅ |
> | test suite — 269 passing | test_suite | 269 | 295 passed | ✅ |
> | oro triplet compliance | oro_compliance | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (3×, todos  | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (3×, todos  | ✅ |
> | handoff node d5476bb8 | mesh_node | d5476bb8-c5ea-4dc4-a3c0-86d1e0895456 | d5476bb8-c5ea-4dc4-a3c0-86d1e0895456 | ✅ |
> 
> QA VERDICT: 10 verified · 0 skipped · 0 failed → SEAL ALLOWED
> 
> (audit completed in 13.3s)
> AUDIT_EXIT=0
> ```

## 🤖 Claude *(14:29:33)*


## 🤖 Claude *(14:29:34)*

**Phase 5c: SEAL ALLOWED** (10 verificadas · 0 falhas, exit 0) — nó `d5476bb8` confirmado na malha.

**Phase 6 — BoK Seal Status:**

## 🤖 Claude *(14:29:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== m\u00f3dulos tocados nesta sess\u00e3o ===\"\ngit diff --name-only HEAD~3..HEAD 2>/dev/null\necho \"=== veredito ===\"\necho \"\u00danica mudan\u00e7a de c\u00f3digo: src/pages/PrivacyPolicy.tsx \u2014 edi\u00e7\u00e3o de TEXTO em p\u00e1gina legal J\u00c1 existente.\"\necho \"Exemp\u00e7\u00e3o MCORCH Master Execution Protocol: single-file patch a feature documentada existente (n\u00e3o \u00e9 m\u00f3dulo/feature/integra\u00e7\u00e3o nova) \u2192 BoK gate N/A.\"",
  "description": "Phase 6 BoK gate check + exemption"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === módulos tocados nesta sessão ===
> HANDOFF.md
> README.md
> proof-manifest.json
> src/pages/PrivacyPolicy.tsx
> === veredito ===
> Única mudança de código: src/pages/PrivacyPolicy.tsx — edição de TEXTO em página legal JÁ existente.
> Exempção MCORCH Master Execution Protocol: single-file patch a feature documentada existente (não é módulo/feature/integração nova) → BoK gate N/A.
> ```

## 🤖 Claude *(14:29:41)*


## 🤖 Claude *(14:29:41)*

**Phase 6 ✅** — BoK gate N/A (single-file patch a página legal existente; exempção do Master Execution Protocol).

**Phase 7 — Push:**

## 🤖 Claude *(14:29:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit push origin main 2>&1 | tail -8\necho \"---\"\ngit log --oneline -4\necho \"---remote---\"\ngit remote get-url origin",
  "description": "Push to origin main"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [90m11:29AM[0m [32mINF[0m scan completed in 28.7ms
> [90m11:29AM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.08 seconds)
> ✔️ gitleaks-range (0.08 seconds)
> To github.com:gabrielZarattini/constellation-orchestra.git
>    6c30136..1b085aa  main -> main
> ---
> 1b085aa docs(handoff): seal privacy policy Google OAuth compliance — Limited Use / AI-training / revocation / security
> 37eabe0 docs(readme): v6.58.1 badge + neural_mesh 8982 nodes (privacy policy Google OAuth compliance)
> f40e989 fix(legal): privacy policy — Google OAuth compliance (Limited Use / AI-training / revocation / security)
> 6c30136 docs(readme): v6.58.0 badge + neural_mesh 8980 nodes (distribution mapping complete)
> ---remote---
> git@github.com:gabrielZarattini/constellation-orchestra.git
> ```

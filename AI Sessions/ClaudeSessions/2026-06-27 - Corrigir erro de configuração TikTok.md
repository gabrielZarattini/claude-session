# Corrigir erro de configuração TikTok
**Date:** 2026-06-27 | **Session ID:** `f23f934d-28f6-402d-a438-cbc319022dfc`

---

## 👤 User *(17:43:44)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(17:43:44)*

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


## 🤖 Claude *(17:43:49)*


## 🤖 Claude *(17:43:49)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with the parallel pre-flight checks.

## 🤖 Claude *(17:43:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7; echo \"---STATUS---\"; git status --short; echo \"---DIFFSTAT---\"; git diff HEAD --stat",
  "description": "Git history, status, diff scope"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9fc3020 docs(handoff): seal social-connect TikTok/YouTube/Pinterest — BoK gate + Vault app-creds + OAuth/publisher branches + UI
> cbe16c8 docs(readme): v6.54.0 — Social Connect TikTok/YouTube/Pinterest (code-complete + fail-closed proven)
> e81d868 feat(settings): social app-config card + TikTok/YouTube/Pinterest connect cards
> 25477a8 feat(social): TikTok/YouTube/Pinterest OAuth + publisher branches, fail-closed cred resolution (FR-PE-006..016)
> c94bd75 feat(db): social_app_config — per-user Vault-encrypted OAuth app credentials (FR-PE-005)
> ea12afc docs(post-engine): social-connect BoK amendment + Lei-2 SOPs + grounded blueprint (TikTok/YouTube/Pinterest)
> 2d8e46d chore(sprint): v6.53.0 — Agentic Governance + Learning Loop + analytics honesto
> ---STATUS---
>  M proof-manifest.json
> ---DIFFSTAT---
>  proof-manifest.json | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> ```

## 🤖 Claude *(17:43:51)*


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

## 🤖 Claude *(17:43:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s http://localhost:8001/api/v2/heartbeat; echo; echo \"---BOK---\"; ls docs/bok/ 2>/dev/null; echo \"---HANDOFF---\"; wc -l HANDOFF.md; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "Docker, Chroma, BoK, HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 10 days (healthy)
> mcorch_claude_mem: Up 12 days (healthy)
> mcorch_chroma: Up 12 days (healthy)
> ---
> mega-brain-dashboard: Up 12 days
> mega-brain-webhook: Up 12 days (healthy)
> mega-brain-daemon: Up 12 days (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1782582234054931820}
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
> ---HANDOFF---
> 8493 HANDOFF.md
> ---SCRATCH---
> scratch has files
> ```

## 🤖 Claude *(17:43:58)*


## 🤖 Claude *(17:44:02)*

TypeScript is clean. Now reading HANDOFF (head + tail) and sprint priorities in parallel.

## 🤖 Claude *(17:44:02)*


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
> 14	## Session Seal — Conectar redes: TikTok + YouTube + Pinterest (brand persona Gabriel AI) — BoK gate + Vault app-creds + OAuth/publisher branches + UI (2026-06-27)
> 15	
> 16	Diretiva Sovereign: *"vamos conectar as redes — TikTok, YouTube, Pinterest"* + *"continue força total"*. Operado sob o Closed-Loop Protocol: pesquisa fundamentada → gate BoK → migration → edge code → UI → seal. Tudo provado materialmente (Lei 1); nada declarado sem prova.
> 17	
> 18	**Achado central:** ~90% da infra já existia (enum `social_platform` já tinha as 3 · `social_accounts` Vault · OAuth genérico `social-auth-init`/`-callback` · MESMO MP4 9:16). Net-new = credenciais de app per-user (Vault) + 3 pares de branches OAuth/publisher + UI. Os blockers duros são 100% **Sovereign-gated** (registrar 3 apps de dev + 3 audits — sem app não há `client_id`/`secret` → nenhum OAuth; sem audit o público é invisível: TikTok SELF_ONLY · YouTube forced-private · Pinterest sandbox).
> 19	
> 20	| Action | Result |
> 21	|--------|--------|
> 22	| Pesquisa fundamentada (workflow `wf_b5a35451`, 8 agentes, adversarial-verify) | ✅ 3 plataformas verificadas HIGH; blueprint `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md` + playbook `…/social-app-registration-playbook-2026-06-27.md` |
> 23	| PASSO 0 — gate BoK | ✅ `post-engine` `06`/`09-pattern-conformance`(21 padrões)/`10-amendment`(FR-PE-005..016) + 3 SOPs Lei 2 `docs/processes/{tiktok,youtube,pinterest}-publish-credential-resolution.md` |
> 24	| Migration `20260627120000_social_app_config` | ✅ aplicada+provada — coluna crua=UUID Vault `55caaf7b…` · masked view `••••` · decrypted view anon→**42501** · `/security-review` SAFE |
> 25	| Helper `supabase/functions/_shared/social-app-config.ts` | ✅ `resolveSocialAppCreds` per-user→env→**402** fail-closed (nunca chave compartilhada silenciosa) |
> 26	| Branches `social-auth-init`/`-callback`/`refresh-social-token`/`publish-social` + `auto-publish` video_url | ✅ `deno check` 8/8 · deployadas · **fail-closed provado LIVE (3×402)** |
> 27	| `autopilot-run` VIDEO_FLOW_PLATFORMS / FR-PE-013 | ⏸️ **DEFERIDO** — manter `['wordpress']`; adicionar youtube/tiktok/pinterest cobraria VIDEO_COST sem render (charge-without-value) até estender o enqueue-gate de `orchestrate-content`/`-step` |
> 28	| UI `useSocialAppConfig` + `SocialAppConfigCard` (Settings→Social) + 3 connect cards (`/dashboard/social`) | ✅ tsc 0 · build deployado (chunk `SettingsPage-CHgtU2cG.js` + env baked) · **browser-verified + Vision QA "high"** · 0 erro de console |
> 29	
> 30	| Commit | Conteúdo |
> 31	|--------|----------|
> 32	| `ea12afc` | docs(post-engine): BoK amendment + SOPs + blueprint |
> 33	| `c94bd75` | feat(db): social_app_config Vault-cifrada (FR-PE-005) |
> 34	| `25477a8` | feat(social): OAuth + publisher branches + helper fail-closed (FR-PE-006..016) |
> 35	| `e81d868` | feat(settings): app-config card + connect cards |
> 36	| `cbe16c8` | docs(readme): v6.54.0 |
> 37	
> 38	**Mesh seal:** handoff node `311a55b1-fb7b-410f-9582-625fb4721619` (embedded 768d). Mesh **8973 nós**.
> 39	
> 40	**Próximo (o unlock):** (Sovereign) registrar TikTok/Google/Pinterest dev apps + submeter 3 audits + entrar `client_id`/`secret` (UI Settings→Social OU env `TIKTOK_CLIENT_KEY`/`_SECRET`·`GOOGLE_CLIENT_ID`/`_SECRET`·`PINTEREST_CLIENT_ID`/`_SECRET`) → o botão Conectar acende o OAuth (provo o publish E2E no mesmo dia); público pós-audit. (código) slice FR-PE-013 video-cadence das novas redes + spine de persona CCIO.
> 41	
> 42	---
> 43	
> 44	## Session Seal — Doutrina Agêntica AGI→ASI + Learning & Adaptation: gate vinculante · Collective Efficiency Ledger · nervo sensorial + reward brand-first · analytics honesto (2026-06-27)
> 45	
> 46	Sessão-maratona multi-arco. **Arco 1** — Diretiva Sovereign: *"que todos os nossos próximos protocolos de desenvolvimento sigam essa visão clara de futuro para antecipar o mercado e a tecnologia"* — ancorada em `docs/Agentic-Design-Patterns.pdf` (Gulli, 21 padrões) + `docs/From AGI to ASI - 2606.12683.pdf` (DeepMind, 4 vias). **Arco 2** — atacar o único padrão FRACO (Learning & Adaptation). **Arco 3** — analytics honesto + perfis da marca limpos. 6 commits, tudo provado materialmente (Lei 1).
> 47	
> 48	**Achado material (3 deep-reads dos PDFs + verificação de schema):** o MCORCH JÁ encarna ~metade dos 21 padrões por doutrina (11 fortes · 9 moderados · 1 fraco=Learning&Adaptation). **Somos a Via 4 (coletivo de agentes) na camada de produto + a Via 3 (auto-aperfeiçoamento recursivo) no micro** (Obstáculo→Síntese). O gap estrutural é o que o paper aponta como ABERTO: respondíamos as perguntas de coletivo por doutrina mas **não medíamos nenhuma** — crescíamos no escuro.
> 49	
> 50	**Entregue (5 fases):**
> 51	- **Fase 1 (docs):** doutrina load-bearing `docs/architecture/agentic-vision.md` (Pattern Maturity Ledger dos 21 padrões + tese) · gate vinculante `CLAUDE.md §1 Step 3.5` (toda SDD declara conformidade) + §3/§4 · 2 docs stale (`system_architecture.md`/`agents.md`, descreviam plataforma AdSense pré-virada) DEPRECADOS+redirect.
> 52	- **Fase 2 (BoK):** suíte `docs/bok/agentic-governance/` 10/10 (autorada via workflow `wf_5fb96548`, espinha pinada; `09-pattern-conformance.md` = template mestre dos 21 padrões). Zero placeholders.
> 53	- **Fase 3 (SOP Lei 2):** `docs/processes/collective-efficiency-ledger.md` (8 gates; G6 `count cross-tenant=0` = gate-mãe).
> 54	- **Fase 4 (código):** migration `20260626120000_collective_efficiency_ledger.sql` — VIEW `collective_efficiency_ledger` (security_invoker per-tenant) + RPC `collective_efficiency_rollup` (SECURITY DEFINER service-role-only) DERIVAM a métrica da verdade financeira (`pipeline_runs`+`autopilot_cycles`), anti-Goodhart · 2 emits aditivos `collective_hop`/`collective_retry` em orchestrate-content/-step (deployadas). **/security-review SAFE.**
> 55	- **Fase 5 (seal):** nó `documentation_suite` `34748570-0cf2-470d-ba0e-f3ceab1cb550` (embedded 768d) + edge DERIVES_FROM `2f3b7a76` → mcorch-constellation.
> 56	
> 57	**Prova material (Lei 1, LIVE em prod):** migration aplicada (`Finished db push`) · VIEW 16 linhas reais · **G6 isolamento provado** (tenant throwaway vê **0**, service-role vê 16) · RPC negado a authenticated (**403 / 42501 permission denied**) · G7 métrica bate com a base exata (`93659c88`: mco 10·n_units 6·wall_clock 59985) · **rollup já dá insight: orchestrate-content avg 334.6s vs autopilot-cycle 2.4s** (o coletivo medido). `tsc` 0.
> 58	
> 59	**Honestidade (DD-AG-004):** **V4-2 (valor marginal por agente) DEFERIDO** a experimento A/B real — não fabricar proxy gameável (alerta do próprio paper). **Backlog de canonização OTD-AG-001..010** (001 Ledger=ENTREGUE; 002 fechar loop Learning&Adaptation reward multi-métrica = P0 próximo).
> 60	
> 61	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (aprovou o plano + escopo máximo via AskUserQuestion) · Owner=Sovereign (risco = instrumentação errada induzir decisão de escala errada).
> 62	
> 63	### Arco 2 — Learning & Adaptation: o loop que COMPÕE (OTD-AG-002 · emenda BoK viral-autopilot v0.3)
> 64	
> 65	**Diagnóstico material (`wob2d279d`):** o motor aprendia sobre um **placar em branco** — `creative_metrics` impressions/engagements sempre 0; reward = `totalClicks` mono-métrica (Goodhart, `autopilot-analyze:90`); a política só sussurrava um hint, não realocava esforço (`ab_variants` parada); 2 bugs latentes. **Causa raiz do "não avançamos apesar do dev incrível".**
> 66	
> 67	**Fatia A — nervo sensorial:** BoK viral-autopilot v0.3 (FR-VA-027..031 + `09-pattern-conformance` + SOP Lei 2 `publication-metrics-collection.md`) · migration `20260626130000_publication_metrics.sql` (time-series, RLS SELECT-own, **G6 provado** — throwaway vê 0; + `meta_posts.content_id` link fix) · edge `collect-publication-metrics` (insights IG/FB per-user, **fail-soft** por plataforma, nunca fabrica — provado: 2 posts LinkedIn → skip honesto) · painel **"Por Publicação"** (`usePublicationMetrics`+`PublicationMetricsPanel`) **verificado em browser real** (estado honesto, nunca demo).
> 68	
> 69	**Fatia B — o loop honesto:** `autopilot-analyze` reward multi-métrica brand-first `R=0.40·reach+0.30·eng+0.20·brand+0.10·rev` (z-score anti-Goodhart, degrada honesto — **prova policy `7d9856d0` reward 0.9 modo fallback**) · `autopilot-run` realocação ε-greedy budget-neutral (a política move o `tasks[]`, não só sussurra) · `orchestrate-step` read filtrado por scope=plan_id + `applied=true`. **Diferidos:** V4-2 (valor marginal/agente) · B4 EWMA · B5 pauta de receita.
> 70	
> 71	### Arco 3 — Analytics honesto + perfis da marca limpos
> ```

## 🤖 Claude *(17:44:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8093,
  "limit": 400
}
```

## 🤖 Claude *(17:44:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -60; echo \"===SCRATCH===\"; ls -la scratch/ 2>/dev/null",
  "description": "Sprint priorities + scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (50.5KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/f23f934d-28f6-402d-a438-cbc319022dfc/tool-results/bqrfdvhvi.txt
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

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8093	ContentLibraryPage monetization flow:
> 8094	  Card (text, body contains mercadolivre.com.br)
> 8095	    └── DropdownMenu → "Monetizar Links ML"
> 8096	          → handleMonetizeLinks(item):
> 8097	               match(ML_URL_RE) → unique URLs
> 8098	               for url of unique:
> 8099	                 POST process-affiliate-link → affiliate_url
> 8100	                 body.split(url).join(affiliate_url)
> 8101	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8102	          → Badge 💰 ML (emerald) exibido após monetização
> 8103	```
> 8104	
> 8105	---
> 8106	
> 8107	## Pending Actions (Commercial Launch)
> 8108	
> 8109	### CRITICAL — Must complete before first client
> 8110	
> 8111	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8112	
> 8113	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8114	
> 8115	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8116	
> 8117	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8118	
> 8119	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8120	
> 8121	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8122	
> 8123	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8124	
> 8125	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8126	
> 8127	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8128	
> 8129	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8130	
> 8131	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8132	
> 8133	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8134	   ```bash
> 8135	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8136	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8137	   ```
> 8138	
> 8139	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8140	
> 8141	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8142	
> 8143	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8144	
> 8145	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8146	
> 8147	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8148	
> 8149	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8150	
> 8151	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8152	
> 8153	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8154	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8155	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8156	
> 8157	### SOCIAL — Next steps
> 8158	
> 8159	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8160	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8161	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8162	
> 8163	### NON-CRITICAL
> 8164	
> 8165	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8166	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8167	- `browserslist` — ✅ updated (2026-04-26)
> 8168	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8169	
> 8170	### GITNEXUS MCP — Next steps
> 8171	
> 8172	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8173	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8174	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8175	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8176	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8177	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8178	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8179	
> 8180	### PHASE EPSILON — Next iterations
> 8181	
> 8182	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8183	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8184	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8185	
> 8186	### CORE — Next iterations
> 8187	
> 8188	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8189	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8190	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8191	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8192	
> 8193	### PHASE DELTA — Next iterations
> 8194	
> 8195	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8196	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8197	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8198	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8199	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8200	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8201	
> 8202	### USUÁRIO ZERO — Checklist de validação
> 8203	
> 8204	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8205	- ✅ Stripe sandbox secrets no vault
> 8206	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8207	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8208	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8209	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8210	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8211	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8212	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8213	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8214	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8215	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8216	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8217	
> 8218	---
> 8219	
> 8220	## Infrastructure
> 8221	
> 8222	| Service | Container | Port | Status |
> 8223	|---------|-----------|------|--------|
> 8224	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8225	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8226	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8227	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8228	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8229	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8230	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8231	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8232	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8233	
> 8234	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8235	
> 8236	```bash
> 8237	docker compose up -d
> 8238	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8239	```
> 8240	
> 8241	---
> 8242	
> 8243	## Security Model (Post-Go-Live)
> 8244	
> 8245	| Table | Isolation |
> 8246	|-------|-----------|
> 8247	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8248	| `mcorch_edges` | Same pattern |
> 8249	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8250	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8251	
> 8252	---
> 8253	
> 8254	## Billing Architecture
> 8255	
> 8256	| Decision | Value |
> 8257	|----------|-------|
> 8258	| Canonical billing ledger | `profiles.mco_balance` |
> 8259	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8260	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8261	| Orchestration cost | 10 mcoCoins/run |
> 8262	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8263	| Stripe | Sandbox keys active — swap to live before first client |
> 8264	
> 8265	---
> 8266	
> 8267	## GraphRAG State
> 8268	
> 8269	- **8973 total nodes** (verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8270	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8271	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8272	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8273	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8274	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8275	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8276	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8277	- HNSW cosine index operational
> 8278	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8279	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8280	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8281	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8282	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8283	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8284	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8285	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8286	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8287	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8288	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8289	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8290	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8291	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8292	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8293	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8294	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8295	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8296	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8297	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8298	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8299	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8300	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8301	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8302	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8303	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8304	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8305	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8306	
> 8307	### Embedding Model
> 8308	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8309	Schema: `vector(768)` — HNSW cosine index.
> 8310	
> 8311	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8312	Três camadas eliminam intervenção manual:
> 8313	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8314	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8315	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8316	
> 8317	### Comandos de manutenção da Mesh
> 8318	```bash
> 8319	# Verificar nós sem embedding (deveria retornar array vazio):
> 8320	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8321	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8322	
> 8323	# Backfill manual (Bun-native — requer .env):
> 8324	bun run scripts/backfill-embeddings.ts
> 8325	
> 8326	# Backfill de código-fonte nos nós AST:
> 8327	bun run scripts/backfill-node-content.ts
> 8328	
> 8329	# Re-sync AST completo:
> 8330	cd packages/gitnexus-core && npm run sync-mesh
> 8331	
> 8332	# Acompanhar re-ingesta pós-commit:
> 8333	tail -f /tmp/mcorch-ingest.log
> 8334	```
> 8335	
> 8336	---
> 8337	
> 8338	## Video Rescue Protocol
> 8339	
> 8340	When a video generation operation (Google Veo) times out or client disconnects:
> 8341	```bash
> 8342	# Via edge function (production):
> 8343	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8344	  -H "Authorization: Bearer <user_jwt>" \
> 8345	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8346	
> 8347	# Via local script (admin/debug):
> 8348	source .env && bun run rescue.ts <operation_id> <content_id>
> 8349	```
> 8350	
> 8351	---
> 8352	
> 8353	## Architecture Pillars
> 8354	
> 8355	| Layer | Implementation |
> 8356	|-------|---------------|
> 8357	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8358	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8359	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8360	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8361	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8362	
> 8363	---
> 8364	
> 8365	## Phase Delta — Architecture
> 8366	
> 8367	```
> 8368	OrchestrationPage (full-canvas, p-0)
> 8369	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8370	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8371	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8372	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8373	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8374	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8375	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8376	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8377	
> 8378	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8379	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8380	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8381	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8382	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8383	```
> 8384	
> 8385	### Canvas State Architecture (Hybrid)
> 8386	
> 8387	```
> 8388	User interaction → ReactFlow internal state (positions, drag)
> 8389	                         ↓ (debounced 600ms)
> 8390	                   localStorage (positions persist across refresh)
> 8391	                         ↑
> 8392	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8393	     ↓ (status changes sync to ReactFlow via useEffect)
> 8394	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8395	```
> 8396	
> 8397	## Key Files
> 8398	
> 8399	| Purpose | Path |
> 8400	|---------|------|
> 8401	| Architecture rules | `CLAUDE.md` |
> 8402	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8403	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8404	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8405	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8406	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8407	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8408	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8409	| **Node types** | `src/components/orchestrator/nodes/` |
> 8410	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8411	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8412	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8413	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8414	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8415	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8416	| Billing utilities | `src/lib/billing.ts` |
> 8417	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8418	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8419	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8420	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8421	| Video rescue (local) | `rescue.ts` |
> 8422	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8423	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8424	| Deploy harness | `scripts/harness-deploy.sh` |
> 8425	
> 8426	---
> 8427	
> 8428	## First Client Onboarding Checklist
> 8429	
> 8430	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8431	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8432	3. ~~Activate watchdog cron~~ ✅ Done
> 8433	4. ~~Deploy rescue-video function~~ ✅ Done
> 8434	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8435	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8436	7. Monitor `infra_health_logs` for first 24h.
> 8437	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8438	
> 8439	---
> 8440	
> 8441	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8442	
> 8443	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8444	
> 8445	| Action | Result |
> 8446	|--------|--------|
> 8447	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8448	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8449	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8450	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8451	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8452	
> 8453	| Commit | Conteúdo |
> 8454	|--------|----------|
> 8455	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8456	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8457	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8458	
> 8459	### Arquitetura Matrix Intelligence
> 8460	
> 8461	```
> 8462	ConstellationMatrix (Stabilized Engine)
> 8463	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8464	  └── NodeDetailsPanel (Tabbed Navigation)
> 8465	        ├── Tab Meta: Neighbor exploration + Net Context
> 8466	        ├── Tab Code: Source code preview (Supabase sync)
> 8467	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8468	
> 8469	useNodeIntelligence Hook:
> 8470	  - contentQuery: fetch nodes.content column
> 8471	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8472	  - state: isAnalyzing, analysisResult, progress
> 8473	```
> 8474	
> 8475	---
> 8476	
> 8477	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8478	
> 8479	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8480	
> 8481	| Action | Result |
> 8482	|--------|--------|
> 8483	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8484	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8485	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8486	
> 8487	**Output da análise (estruturado em pt-BR):**
> 8488	- Visão Geral — papel do módulo no sistema
> 8489	- Padrões Detectados — design patterns, antipatterns
> 8490	- Acoplamento & Dependências — análise In/Out-Degree
> 8491	- Recomendações — 1-3 ações priorizadas
> 8492	
> ```

## 🤖 Claude *(17:44:07)*


## 🤖 Claude *(17:44:08)*

All context gathered. Quick BoK gate check on the active module before producing the brief.

## 🤖 Claude *(17:44:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; for slug in post-engine viral-autopilot agentic-governance; do required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics); missing=(); for doc in \"${required[@]}\"; do [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\"); done; [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 completo\" || echo \"\u26a0\ufe0f $slug \u2014 falta: ${missing[*]}\"; done",
  "description": "BoK completeness for active modules"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ post-engine — completo
> ✅ viral-autopilot — completo
> ✅ agentic-governance — completo
> ```

## 🤖 Claude *(17:44:13)*


## 🤖 Claude *(17:44:35)*

```
═══════════════════════════════════════════════════════════
  HANDSON — Social Connect TikTok/YouTube/Pinterest (2026-06-27)
═══════════════════════════════════════════════════════════

🏁 ESTADO ATUAL
  Fase selada: Conectar redes — TikTok + YouTube + Pinterest (brand persona Gabriel AI)
  Últimos commits:
    9fc3020 — docs(handoff): seal social-connect TikTok/YouTube/Pinterest
    cbe16c8 — docs(readme): v6.54.0 — Social Connect (code-complete + fail-closed proven)
    e81d868 — feat(settings): social app-config card + connect cards
    25477a8 — feat(social): OAuth + publisher branches, fail-closed cred resolution (FR-PE-006..016)
    c94bd75 — feat(db): social_app_config — Vault-encrypted OAuth app creds (FR-PE-005)

📂 MUDANÇAS PENDENTES
  M proof-manifest.json (1 linha — artefato da última seal; não conflita)
  Worktree essencialmente limpo ✅

🏗️ INFRA
  mcorch_chroma:     Up 12 days (healthy) — Chroma API v2: OK (heartbeat respondeu)
  mcorch_claude_mem: Up 12 days (healthy)
  mcorch_vision_mcp: Up 10 days (healthy)
  mega-brain-*:      daemon/webhook healthy · dashboard up

🧠 KNOWLEDGE MESH
  8973 nós · ~9070 arestas (fonte: HANDOFF GraphRAG State) · 100% embedded (768d HNSW)
  Seal node desta fase: handoff 311a55b1 (embedded)

🔧 TYPESCRIPT
  Zero erros ✅ (tsc --noEmit limpo)

📚 BoK SUITES
  Módulos ativos completos: post-engine ✅ · viral-autopilot ✅ · agentic-governance ✅
  Total: 23 suítes em docs/bok/ — BoK Gate ABERTO para código

📌 SPRINT
  Goal: Distribuição social autônoma operacional (LinkedIn live; TikTok/YT/Pinterest code-complete, gated em registro de apps)
  Top gap: ativar OAuth real das 3 novas redes — bloqueado por ação Sovereign (registro de dev apps + audits)

⚡ PRÓXIMOS PASSOS (prioridade)
  1. 🔓 UNLOCK das redes (Sovereign-gated): registrar dev apps TikTok/Google/Pinterest +
     submeter 3 audits + inserir client_id/secret (UI Settings→Social OU env). Sem isso o
     botão Conectar não acende OAuth. Código 100% pronto e fail-closed provado (3×402 live).
  2. (código) FR-PE-013 — video-cadence das novas redes (DEFERIDO: hoje cobraria VIDEO_COST
     sem render; precisa estender o enqueue-gate de orchestrate-content/-step antes).
  3. Re-OAuth IG insights (destrava payoff visível do Learning&Adaptation) + postback ML real
     (OTD-VA-007) + 1º ciclo pago de vídeo 9:16 witnessed (Viral Autopilot, video_enabled).

⚠️ ALERTAS
  Nenhum bloqueador técnico ✅ — tsc limpo, containers saudáveis, Chroma OK.
  ⚠️ scratch/ tem arquivos (script /handson sugere mover p/ .claude/scripts/db/ — não-crítico).
  ⚠️ Blockers de ativação social são 100% ação Sovereign (não destraváveis por código).

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

A sessão anterior selou o **Social Connect** (TikTok/YouTube/Pinterest) com a infra de código completa e fail-closed materialmente provada. O que falta é puramente **ação sua (Sovereign)**: registrar os 3 dev apps e submeter os audits — sem `client_id`/`secret` nenhum OAuth acende.

Há três frentes onde posso avançar **autonomamente sem o gate de registro**: (2) o slice `FR-PE-013` de video-cadence, (3) re-OAuth IG insights e postback ML. Qual frente seguimos — ou tem nova diretiva?

## 👤 User *(17:50:39)*

tiktok_not_configured
Erro ao conectarEdge Function returned a non-2xx status code

## 🤖 Claude *(17:50:46)*


## 🤖 Claude *(17:50:47)*

Esse `tiktok_not_configured` é exatamente o fail-closed esperado — mas deixa eu confirmar no código o caminho exato e o que destrava, em vez de assumir.

## 🤖 Claude *(17:50:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"===HELPER===\"; cat supabase/functions/_shared/social-app-config.ts 2>/dev/null | head -120; echo \"===INIT FILE EXISTS?===\"; ls -la supabase/functions/social-auth-init/index.ts 2>/dev/null",
  "description": "Read social-app-config helper + check init fn"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===HELPER===
> // Shared: per-user OAuth APP credential resolution for TikTok / YouTube / Pinterest.
> // API Tenancy Model (CLAUDE.md): resolve credentials per-user first, env fallback as a
> // Sovereign-only onboarding default (OTD-PE-SOCIAL-APPCREDS), hard-fail otherwise — never a
> // silent shared key. BoK SSOT: docs/bok/post-engine/10-amendment-social-connect-*.md (FR-PE-005..009).
> //
> // Resolution order:
> //   (1) social_app_config per-user (is_active=true) — read via the service-role decrypted_* view.
> //   (2) env fallback — TIKTOK_CLIENT_KEY/SECRET · GOOGLE_CLIENT_ID/SECRET · PINTEREST_CLIENT_ID/SECRET.
> //   (3) SocialAppConfigError(402) {error:"<platform>_not_configured", action:"Configure ... /dashboard/settings"}.
> //
> // SECURITY: client_secret lives encrypted in Vault; only the service-role decrypted_social_app_config view
> // exposes plaintext. NEVER read the masked public view for the secret (it returns '••••••••••••').
> 
> import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2";
> 
> export type SocialAppPlatform = "tiktok" | "youtube" | "pinterest";
> 
> export interface SocialAppCreds {
>   clientId: string;
>   clientSecret: string;
>   scopes: string[] | null;
>   metadata: Record<string, unknown>;
>   source: "per-user" | "env";
> }
> 
> // Values are env-var NAMES (looked up in Deno.env), NOT secret values. The `*Env` suffix keeps them
> // unambiguous to the secret-scan hook (a `secret: "..."` literal would false-positive).
> const ENV_MAP: Record<SocialAppPlatform, { idEnv: string; secretEnv: string; label: string }> = {
>   tiktok: { idEnv: "TIKTOK_CLIENT_KEY", secretEnv: "TIKTOK_CLIENT_SECRET", label: "TikTok" },
>   youtube: { idEnv: "GOOGLE_CLIENT_ID", secretEnv: "GOOGLE_CLIENT_SECRET", label: "YouTube" },
>   pinterest: { idEnv: "PINTEREST_CLIENT_ID", secretEnv: "PINTEREST_CLIENT_SECRET", label: "Pinterest" },
> };
> 
> /** Structured fail-closed error → maps to a 402 JSON body the client can act on. */
> export class SocialAppConfigError extends Error {
>   readonly httpStatus = 402;
>   readonly body: { error: string; action: string };
>   constructor(platform: string, label: string) {
>     super(`${platform}_not_configured`);
>     this.name = "SocialAppConfigError";
>     this.body = {
>       error: `${platform}_not_configured`,
>       action: `Configure suas credenciais de app ${label} em /dashboard/settings`,
>     };
>   }
> }
> 
> /**
>  * Resolve OAuth app credentials for a platform, scoped to a user.
>  * @param supabase a SERVICE-ROLE client (reads the decrypted_social_app_config view).
>  * @throws SocialAppConfigError(402) when neither per-user nor env credentials resolve.
>  */
> export async function resolveSocialAppCreds(
>   supabase: SupabaseClient,
>   userId: string,
>   platform: SocialAppPlatform,
> ): Promise<SocialAppCreds> {
>   const env = ENV_MAP[platform];
>   if (!env) throw new SocialAppConfigError(platform, platform);
> 
>   // (1) per-user
>   if (userId) {
>     const { data, error } = await supabase
>       .from("decrypted_social_app_config")
>       .select("client_id, client_secret, scopes, metadata, is_active")
>       .eq("user_id", userId)
>       .eq("platform", platform)
>       .eq("is_active", true)
>       .maybeSingle();
> 
>     if (!error && data && data.client_id && data.client_secret) {
>       return {
>         clientId: String(data.client_id),
>         clientSecret: String(data.client_secret),
>         scopes: (data.scopes as string[] | null) ?? null,
>         metadata: (data.metadata as Record<string, unknown>) ?? {},
>         source: "per-user",
>       };
>     }
>   }
> 
>   // (2) env fallback (Sovereign-only onboarding default — OTD-PE-SOCIAL-APPCREDS)
>   const envId = Deno.env.get(env.idEnv);
>   const envSecret = Deno.env.get(env.secretEnv);
>   if (envId && envSecret) {
>     return { clientId: envId, clientSecret: envSecret, scopes: null, metadata: {}, source: "env" };
>   }
> 
>   // (3) hard fail
>   throw new SocialAppConfigError(platform, env.label);
> }
> 
> /** Build a fail-closed Response from a thrown SocialAppConfigError (or rethrow others). */
> export function socialAppConfigErrorResponse(err: unknown, corsHeaders: Record<string, string>): Response | null {
>   if (err instanceof SocialAppConfigError) {
>     return new Response(JSON.stringify(err.body), {
>       status: err.httpStatus,
>       headers: { ...corsHeaders, "Content-Type": "application/json" },
>     });
>   }
>   return null;
> }
> ===INIT FILE EXISTS?===
> -rw-rw-r-- 1 ubuntu ubuntu 8923 Jun 27 13:04 supabase/functions/social-auth-init/index.ts
> ```

## 🤖 Claude *(17:50:59)*


## 🤖 Claude *(17:51:02)*

Confirmado: `tiktok_not_configured` é o **fail-closed esperado (402)** — não é bug de código. Significa que nenhuma das duas fontes de credencial de app TikTok existe ainda: (1) linha per-user em `social_app_config` nem (2) env `TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET`.

Mas há um detalhe de UX que **é** um bug e que posso corrigir: a UI mostrou o genérico *"Edge Function returned a non-2xx status code"* em vez da mensagem útil em PT-BR (*"Configure suas credenciais de app TikTok em /dashboard/settings"*) que o edge function já retorna no corpo. Deixa eu verificar como o card de conexão trata o erro.

## 🤖 Claude *(17:51:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"===CONNECT CARD(S)===\"; grep -rln \"tiktok\\|social-auth-init\\|Erro ao conectar\" src/components/settings src/hooks src/pages 2>/dev/null | head; echo \"===edge helper usage===\"; grep -rln \"edgeErrorMessage\" src/ 2>/dev/null | head",
  "description": "Find connect card + edgeErrorMessage usage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===CONNECT CARD(S)===
> src/components/settings/SocialAppConfigCard.tsx
> src/hooks/useSocialAccounts.ts
> src/pages/CalendarPage.tsx
> src/pages/ViralMinerPage.tsx
> src/hooks/useCampaigns.ts
> src/pages/SocialAccountsPage.tsx
> src/pages/DashboardHome.tsx
> src/pages/CampaignWizard.tsx
> src/pages/AnalyticsPage.tsx
> src/pages/ContentLibraryPage.tsx
> ===edge helper usage===
> src/lib/edge.ts
> src/test/marketing-hub.test.ts
> src/components/creative/AssetDetailDialog.tsx
> src/hooks/useAEO.ts
> src/hooks/useVideoRender.ts
> src/hooks/useCampaigns.ts
> src/hooks/useSocialAccounts.ts
> src/hooks/useLeads.ts
> src/hooks/useIntentOrchestrator.ts
> src/hooks/useAutopilot.ts
> ```

## 🤖 Claude *(17:51:08)*


## 🤖 Claude *(17:51:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -rln \"Erro ao conectar\\|social-auth-init\" src/ 2>/dev/null; echo \"===find connect card component===\"; ls src/components/settings/ | grep -i \"social\\|connect\\|tiktok\\|youtube\\|pinterest\"",
  "description": "Locate connect card + error string"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/pages/SocialAccountsPage.tsx
> src/lib/social-app-config.ts
> src/hooks/useSocialAccounts.ts
> ===find connect card component===
> McpConnectorsCard.tsx
> SocialAppConfigCard.tsx
> ```

## 🤖 Claude *(17:51:14)*


## 🤖 Claude *(17:51:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -n \"Erro ao conectar\\|social-auth-init\\|edgeErrorMessage\\|invoke\\|catch\\|toast\" src/pages/SocialAccountsPage.tsx | head -40",
  "description": "Inspect error handling in SocialAccountsPage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9:import { useToast } from '@/hooks/use-toast';
> 35:  const { toast } = useToast();
> 63:      toast({ title: 'Campos obrigatórios', description: 'Preencha URL, usuário e Application Password.', variant: 'destructive' });
> 81:      toast({ title: 'WordPress conectado!', description: 'Credenciais salvas com sucesso.' });
> 82:    } catch (err: any) {
> 83:      toast({ title: 'Erro ao salvar', description: err.message, variant: 'destructive' });
> 101:      toast({ title: 'WordPress desconectado' });
> 102:    } catch (err: any) {
> 103:      toast({ title: 'Erro', description: err.message, variant: 'destructive' });
> 111:    } catch (err: any) {
> 112:      toast({ title: 'Erro ao conectar', description: err.message, variant: 'destructive' });
> 120:      toast({ title: 'Desconectado', description: `${name} foi desconectado com sucesso.` });
> 121:    } catch {
> 122:      toast({ title: 'Erro', description: 'Não foi possível desconectar.', variant: 'destructive' });
> ```

## 🤖 Claude *(17:51:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "offset": 104,
  "limit": 20
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 104	    }
> 105	  };
> 106	
> 107	  const handleConnect = async (platform: SocialPlatform) => {
> 108	    setConnectingPlatform(platform);
> 109	    try {
> 110	      await initiateOAuth(platform);
> 111	    } catch (err: any) {
> 112	      toast({ title: 'Erro ao conectar', description: err.message, variant: 'destructive' });
> 113	      setConnectingPlatform(null);
> 114	    }
> 115	  };
> 116	
> 117	  const handleDisconnect = async (id: string, name: string) => {
> 118	    try {
> 119	      await disconnectAccount.mutateAsync(id);
> 120	      toast({ title: 'Desconectado', description: `${name} foi desconectado com sucesso.` });
> 121	    } catch {
> 122	      toast({ title: 'Erro', description: 'Não foi possível desconectar.', variant: 'destructive' });
> 123	    }
> ```

## 🤖 Claude *(17:51:23)*


## 🤖 Claude *(17:51:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -n \"initiateOAuth\\|edgeErrorMessage\\|invoke\\|FunctionsHttpError\\|throw\\|\\.context\\|return\" src/hooks/useSocialAccounts.ts | head -40",
  "description": "Inspect initiateOAuth in hook"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 5:import { edgeErrorMessage } from '@/lib/edge';
> 33:      if (error) throw error;
> 34:      return data as SocialAccount[];
> 45:      if (error) throw error;
> 50:  const initiateOAuth = async (platform: SocialPlatform) => {
> 51:    const { data, error } = await supabase.functions.invoke('social-auth-init', {
> 64:        // For platforms whose edge fn returns a structured non-2xx body (e.g. 402
> 66:        const surfaced = await edgeErrorMessage(error, `Erro ao conectar ${platform}: ${msg || 'Tente novamente.'}`);
> 69:      throw error;
> 81:      throw new Error(serverMsg);
> 87:    return data;
> 91:    if (!account.token_expires_at) return false;
> 92:    return new Date(account.token_expires_at) < new Date();
> 95:  return {
> 100:    initiateOAuth,
> ```

## 🤖 Claude *(17:51:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts",
  "offset": 50,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 50	  const initiateOAuth = async (platform: SocialPlatform) => {
> 51	    const { data, error } = await supabase.functions.invoke('social-auth-init', {
> 52	      body: { platform, redirect_uri: `${window.location.origin}/social/callback` },
> 53	    });
> 54	
> 55	    if (error) {
> 56	      const msg: string = error?.message ?? '';
> 57	      if (msg.includes('LinkedIn not configured')) {
> 58	        toast.error('Configuração Pendente: As credenciais do LinkedIn não estão configuradas no servidor.');
> 59	      } else if (msg.includes('Instagram') || msg.includes('Facebook not configured')) {
> 60	        toast.error('Configuração Pendente: As credenciais do Instagram/Facebook não estão configuradas no servidor.');
> 61	      } else if (msg.includes('Twitter') || msg.includes('X not configured')) {
> 62	        toast.error('Configuração Pendente: As credenciais do Twitter/X não estão configuradas no servidor.');
> 63	      } else {
> 64	        // For platforms whose edge fn returns a structured non-2xx body (e.g. 402
> 65	        // `<platform>_not_configured` with a PT-BR `action`), surface that exact message.
> 66	        const surfaced = await edgeErrorMessage(error, `Erro ao conectar ${platform}: ${msg || 'Tente novamente.'}`);
> 67	        toast.error(surfaced);
> 68	      }
> 69	      throw error;
> 70	    }
> 71	
> 72	    if (data?.error) {
> 73	      const serverMsg: string = data.error;
> 74	      if (serverMsg === 'LinkedIn not configured') {
> 75	        toast.error('Configuração Pendente: As credenciais do LinkedIn não estão configuradas no servidor.');
> 76	      } else {
> 77	        // 200-with-error-body path: prefer the PT-BR `action` hint when present (402 contract).
> 78	        const action: string | undefined = (data as { action?: string }).action;
> 79	        toast.error(action ? `${serverMsg} — ${action}` : `Erro ao conectar ${platform}: ${serverMsg}`);
> 80	      }
> 81	      throw new Error(serverMsg);
> 82	    }
> 83	
> 84	    if (data?.url) {
> 85	      window.location.href = data.url;
> 86	    }
> 87	    return data;
> 88	  };
> 89	
> ```

## 🤖 Claude *(17:51:48)*


## 🤖 Claude *(17:51:51)*

O hook (`useSocialAccounts.ts:66`) já tenta mostrar a mensagem amigável via `edgeErrorMessage`, mas o `handleConnect` da página **re-mostra** um segundo toast genérico. Isso explica o empilhamento que você viu (`tiktok_not_configured` + `Erro ao conectar / non-2xx`). Deixa eu confirmar o que o `edgeErrorMessage` extrai:

## 🤖 Claude *(17:51:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/edge.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Shared helper for Supabase Edge Function invocations from the client.
> 2	// supabase.functions.invoke() returns a FunctionsHttpError for any non-2xx response, with the raw
> 3	// Response on `error.context`. Our edge fns return a PT-BR `{ error }` body (e.g. 402 "Saldo insuficiente"),
> 4	// so we read that to surface the real message to the user instead of the generic "Edge Function returned a
> 5	// non-2xx status code".
> 6	
> 7	/** Extract a PT-BR error message from a Supabase Edge Function non-2xx response. */
> 8	export async function edgeErrorMessage(error: unknown, fallback: string): Promise<string> {
> 9	  const ctx = (error as { context?: { json?: () => Promise<{ error?: string }> } })?.context;
> 10	  try {
> 11	    const body = await ctx?.json?.();
> 12	    if (body?.error) return body.error;
> 13	  } catch { /* response body was not JSON */ }
> 14	  return (error as { message?: string })?.message || fallback;
> 15	}
> 16	
> ```

## 🤖 Claude *(17:52:25)*


## 🤖 Claude *(17:52:33)*

O `edgeErrorMessage` retorna `body.error` (o código de máquina `tiktok_not_configured`) e **ignora** o `body.action` (a dica humana *"Configure suas credenciais de app TikTok em /dashboard/settings"*). Some isso ao toast duplicado da página e você vê exatamente o empilhamento confuso que colou.

Vou ser claro sobre a causa raiz e corrigir o UX:

## Causa raiz (não é bug — é o fail-closed funcionando)
`tiktok_not_configured` = **nenhuma credencial de app TikTok existe ainda**. O OAuth não pode iniciar sem `client_key`/`client_secret`. O desbloqueio é o item Sovereign-gated do handoff:

1. Registrar um dev app em **developers.tiktok.com** → obter `client_key` + `client_secret` (+ submeter audit p/ sair do `SELF_ONLY`).
2. Inserir as credenciais em **Settings → Social** (card per-user, cifrado no Vault) **ou** como secrets `TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET`.
3. Aí o botão *Conectar* acende o OAuth.

Eu **não consigo** gerar essas credenciais — exigem login no portal de devs do TikTok (ação sua). Mesma lógica vale para YouTube (`GOOGLE_CLIENT_ID/SECRET`) e Pinterest.

## O que **posso** consertar agora: a mensagem inútil
Deixo o erro acionável (mostra a dica em PT-BR em vez do código + remove o toast genérico duplicado).

## 🤖 Claude *(17:52:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"===usages in hook===\"; grep -n \"edgeErrorMessage\" src/hooks/useSocialAccounts.ts; echo \"===noUnusedLocals?===\"; grep -n \"noUnused\" tsconfig*.json 2>/dev/null || echo \"none\"",
  "description": "Check edgeErrorMessage usages + unused-locals config"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===usages in hook===
> 5:import { edgeErrorMessage } from '@/lib/edge';
> 66:        const surfaced = await edgeErrorMessage(error, `Erro ao conectar ${platform}: ${msg || 'Tente novamente.'}`);
> ===noUnusedLocals?===
> tsconfig.json:5:    "noUnusedLocals": false,
> tsconfig.json:6:    "noUnusedParameters": false,
> tsconfig.app.json:17:    "noUnusedLocals": false,
> tsconfig.app.json:18:    "noUnusedParameters": false,
> tsconfig.node.json:17:    "noUnusedLocals": false,
> tsconfig.node.json:18:    "noUnusedParameters": false,
> ```

## 🤖 Claude *(17:52:55)*


## 🤖 Claude *(17:52:57)*

`noUnusedLocals: false` — então sem risco. Vou fazer a correção no lugar mais limpo: ensinar o `edgeErrorMessage` a preferir o `action` humano (backward-compatible — o `action` quase sempre é ausente nos outros 402, ex. "Saldo insuficiente" vem em `error`), e remover o toast genérico duplicado da página.

## 🤖 Claude *(17:53:01)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/edge.ts",
  "old_string": "/** Extract a PT-BR error message from a Supabase Edge Function non-2xx response. */\nexport async function edgeErrorMessage(error: unknown, fallback: string): Promise<string> {\n  const ctx = (error as { context?: { json?: () => Promise<{ error?: string }> } })?.context;\n  try {\n    const body = await ctx?.json?.();\n    if (body?.error) return body.error;\n  } catch { /* response body was not JSON */ }\n  return (error as { message?: string })?.message || fallback;\n}",
  "new_string": "/** Extract a PT-BR error message from a Supabase Edge Function non-2xx response. */\nexport async function edgeErrorMessage(error: unknown, fallback: string): Promise<string> {\n  const ctx = (error as { context?: { json?: () => Promise<{ error?: string; action?: string }> } })?.context;\n  try {\n    const body = await ctx?.json?.();\n    // Prefer the human-readable `action` hint (e.g. \"Configure suas credenciais de app TikTok em\n    // /dashboard/settings\") over the machine code in `error` (e.g. \"tiktok_not_configured\").\n    if (body?.action) return body.action;\n    if (body?.error) return body.error;\n  } catch { /* response body was not JSON */ }\n  return (error as { message?: string })?.message || fallback;\n}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/lib/edge.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:53:06)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "    try {\n      await initiateOAuth(platform);\n    } catch (err: any) {\n      toast({ title: 'Erro ao conectar', description: err.message, variant: 'destructive' });\n      setConnectingPlatform(null);\n    }",
  "new_string": "    try {\n      await initiateOAuth(platform);\n    } catch {\n      // initiateOAuth already surfaced a precise toast (e.g. the 402 `action` hint such as\n      // \"Configure suas credenciais de app TikTok ...\"); avoid a second generic \"non-2xx\" toast.\n      setConnectingPlatform(null);\n    }"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:53:10)*


## 🤖 Claude *(17:53:10)*

Verificando tsc:

## 🤖 Claude *(17:53:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; npx tsc --noEmit 2>&1 | tail -10 && echo \"EXIT=$?\"",
  "description": "TypeScript check after edits"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> EXIT=0
> ```

## 🤖 Claude *(17:53:25)*


## 🤖 Claude *(17:53:27)*

tsc limpo (exit 0). Estou no **repo principal** (não worktree), então `build = deploy` direto pro dist/ que o nginx serve. Vou buildar e verificar materialmente.

## 🤖 Claude *(17:53:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; ls -la .env >/dev/null 2>&1 && echo \".env OK\" || echo \"NO .env\"; bun run build 2>&1 | tail -15",
  "description": "Production build (= deploy in main repo)",
  "timeout": 300000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> .env OK
> dist/assets/useConstellationSigma-BIrZwAod.js   97.31 kB │ gzip:  21.58 kB
> dist/assets/proxy-DOzfm97d.js                  125.30 kB │ gzip:  41.24 kB
> dist/assets/ConstellationMatrix-CzQ-jbDI.js    136.25 kB │ gzip:  37.77 kB
> dist/assets/CanvasEditorPage-0-nEtSXK.js       142.18 kB │ gzip:  39.60 kB
> dist/assets/index-DzcCzeyl.js                  167.01 kB │ gzip:  53.33 kB
> dist/assets/ConstellationPage-DfgpNR90.js      184.36 kB │ gzip:  63.64 kB
> dist/assets/CartesianChart-Bl8LTn2S.js         325.07 kB │ gzip:  96.83 kB
> dist/assets/index-CQoFzTzs.js                  661.63 kB │ gzip: 196.01 kB
> dist/assets/react-three-fiber.esm-Bjse3WGa.js  824.11 kB │ gzip: 221.90 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 23.41s
> ```

## 🤖 Claude *(17:53:55)*


## 🤖 Claude *(17:53:56)*

Build OK (23.41s). Verificação material (Lei 1) — chunk novo do SocialAccountsPage + env baked:

## 🤖 Claude *(17:53:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"===SocialAccounts chunk (fresh?)===\"; ls -la --time-style=+%H:%M:%S dist/assets/ | grep -i \"social\"; echo \"===env baked (supabase URL in bundle)?===\"; grep -rl \"bcyvddsykvehvpwstlfa.supabase.co\" dist/assets/*.js >/dev/null 2>&1 && echo \"\u2705 Supabase URL baked into bundle\" || echo \"\u274c env NOT baked\"",
  "description": "Verify fresh chunk + env baked"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===SocialAccounts chunk (fresh?)===
> -rw-rw-r-- 1 ubuntu ubuntu   8692 14:53:51 SocialAccountsPage-uycVrkKk.js
> -rw-rw-r-- 1 ubuntu ubuntu   1624 14:53:51 SocialCallback-Dfa41lp5.js
> -rw-rw-r-- 1 ubuntu ubuntu   2465 14:53:51 useSocialAccounts-v30gq1vW.js
> ===env baked (supabase URL in bundle)?===
> ✅ Supabase URL baked into bundle
> ```

## 🤖 Claude *(17:54:10)*


## 🤖 Claude *(17:54:21)*

Pronto. Resumo material:

## ✅ Correção de UX — buildada e deployada (Lei 1)
- `src/lib/edge.ts` — `edgeErrorMessage` agora prefere o `action` humano sobre o código de máquina (backward-compatible; os outros 402 como "Saldo insuficiente" vêm em `error` e seguem iguais).
- `src/pages/SocialAccountsPage.tsx` — removido o toast genérico duplicado *"Erro ao conectar / non-2xx"*.
- **Prova:** tsc exit 0 · chunks frescos `SocialAccountsPage-uycVrkKk.js` + `useSocialAccounts-v30gq1vW.js` (14:53:51) · env baked no bundle · nginx serve o `dist/` direto.

→ Faça **Ctrl+Shift+R** em login.mcorch.com (Cloudflare pode cachear). Ao clicar Conectar agora aparece **"Configure suas credenciais de app TikTok em /dashboard/settings"** em vez do erro críptico.

## ⚠️ O bloqueio real continua de pé (não é código — é ação sua)
`tiktok_not_configured` = **nenhuma credencial de app TikTok existe**. Para o botão Conectar funcionar de verdade:

1. **developers.tiktok.com** → registrar um app → pegar `client_key` + `client_secret`.
2. Submeter o **audit** do TikTok (sem ele, a API fica em `SELF_ONLY` — só o seu próprio perfil enxerga).
3. Colar `client_key`/`client_secret` em **Settings → Social** (card per-user, cifrado no Vault) **ou** setar os secrets `TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET`.

Não consigo gerar essas credenciais — exigem login no portal de devs do TikTok. Mesma coisa para **YouTube** (`GOOGLE_CLIENT_ID/SECRET` + audit OAuth) e **Pinterest** (`PINTEREST_CLIENT_ID/SECRET` + sair do sandbox).

---

**Quer que eu:**
- (a) verifique o toast novo num browser logado real (preview do dist + sessão injetada), ou
- (b) commite essa correção de UX, ou
- (c) assim que você registrar o app TikTok e colar as credenciais, eu provo o OAuth + publish E2E no mesmo dia?

Os arquivos estão deployados mas **não commitados** ainda (aguardando seu OK).

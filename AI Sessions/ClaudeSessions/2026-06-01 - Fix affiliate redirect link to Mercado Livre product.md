# Fix affiliate redirect link to Mercado Livre product
**Date:** 2026-06-01 | **Session ID:** `d4434afb-c259-4270-a01a-03d85ba37719`

---

## 👤 User *(19:17:08)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(19:17:08)*

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


## 🤖 Claude *(19:17:14)*


## 🤖 Claude *(19:17:15)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with all pre-flight checks in parallel.

First, a `git fetch` to avoid stale-state false negatives (per session memory), then the full diagnostic sweep.

## 🤖 Claude *(19:17:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin --quiet 2>&1 | tail -3; echo \"--- fetch done ---\"; git log --oneline -7",
  "description": "Fetch origin and show recent history"
}
```

## 🤖 Claude *(19:17:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== git status ===\"; git status --short; echo \"=== diff stat ===\"; git diff HEAD --stat; echo \"=== vs origin/main ===\"; git rev-list --left-right --count origin/main...HEAD 2>/dev/null || echo \"no upstream compare\"",
  "description": "Show working tree status and divergence from origin"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- fetch done ---
> 865ded6 chore(sprint): selo v6.19.0 — e2e-user-zero v2 + 3-stream sweep (suíte verde, 8747 nós)
> 08bb72a docs(handoff): paths completos + reflete gating dos smokes live (Phase 5c)
> 0c5eefd fix(tests): gateia smokes live (canvas pago + sql-bridge) atrás de RUN_LIVE_SMOKE
> d8499eb docs(handoff): seal e2e-user-zero v2 + 3-stream sweep — Stream B build + A verified + C readiness
> 5f21caf docs(readme): v6.19.0 — e2e-user-zero v2 harness + 3-stream sweep (8747 nós)
> 09a5bae fix(higgsfield-webhook): mapeia nsfw/canceled para razão clara de soft-fail
> e788d76 chore(hooks): versiona pre-commit + tripwire de segredo em e2e-output/
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git status ===
> === diff stat ===
> === vs origin/main ===
> 0	0
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> === BoK suites ===
> aios-sql-bridge
> canvas-design
> constellation-v2
> conteudo-v2
> e2e-user-zero
> gamificacao-nodes
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> viralmind
> === HANDOFF line count ===
> 6083 HANDOFF.md
> === scratch ===
> scratch clean
> ```

## 🤖 Claude *(19:17:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20; echo \"--- tsc exit: ${PIPESTATUS[0]} ---\"",
  "description": "TypeScript strict typecheck"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- tsc exit: 0 ---
> ```

## 🤖 Claude *(19:17:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== mcorch containers ===\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"=== mega-brain ===\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"=== chroma heartbeat ===\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat 2>&1 || echo \"CHROMA UNREACHABLE\"",
  "description": "Check Docker mesh and Chroma health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === mcorch containers ===
> mcorch_chroma: Up 8 days (healthy)
> mcorch_claude_mem: Up 8 days (healthy)
> === mega-brain ===
> mega-brain-dashboard: Up 8 days
> mega-brain-webhook: Up 8 days (healthy)
> mega-brain-daemon: Up 8 days (healthy)
> === chroma heartbeat ===
> {"nanosecond heartbeat":1780341441821647063}
> ```

## 🤖 Claude *(19:17:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== BoK suites ===\"; ls docs/bok/ 2>/dev/null; echo \"=== HANDOFF line count ===\"; wc -l HANDOFF.md; echo \"=== scratch ===\"; ls scratch/ 2>/dev/null && echo \"WARNING scratch has files\" || echo \"scratch clean\"",
  "description": "List BoK suites, HANDOFF size, scratch check"
}
```

## 🤖 Claude *(19:17:38)*


## 🤖 Claude *(19:17:39)*

Working tree clean, synced with origin/main, TypeScript zero errors, all containers healthy, Chroma alive. Now reading HANDOFF (read-from-end strategy — 6083 lines) plus sprint priorities, and running the BoK completeness gate.

## 🤖 Claude *(19:17:40)*


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
> 14	## e2e-user-zero v2 + 3-Stream Sweep Record (2026-06-01)
> 15	
> 16	**v6.19.0 (2026-06-01)** — Sessão de execução de 3 streams autorizados pelo Sovereign (e2e-user-zero 2ª iteração · gaps reais do Canvas · 1ª campanha real). Padrão dominante: **o código estava sistematicamente à frente dos próprios Pending Actions** — verificação material (Lei 1) ANTES de codar evitou reconstruir 2 features já prontas. Fluxo: `/handson` → priorização → descoberta de que Canvas 4.2 + consistência já estavam shipados → build real do Stream B → readiness do Stream C → seal.
> 17	
> 18	**O que foi entregue:**
> 19	- **Stream B — e2e-user-zero 2ª iteração (build real):** `scripts/qa/e2e-user-zero/lib/redactor.ts` (LGPD Layer 2 — redação de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body em `redactedPaths` + sanitização de cookie; `scanResidualSecrets` p/ o tripwire), `scripts/qa/e2e-user-zero/lib/mesh-persistor.ts` (finding → `observation` node + aresta `OBSERVES`, idempotente via SHA-256 do `name`, fail-soft, `SB_SECRET_KEY`), `scripts/qa/e2e-user-zero/lib/telemetry.ts` (pulse de ciclo de vida em `infra_health_logs`), 6 flows (`dashboard-tour`·`orchestrate-pipeline-view`·`content-library`·`billing-flow`·`settings-tour`·`constellation-view`) + helper `_nav-capture`, runner fiado (started/complete/failure/auth-expired exit-3 + persist), selftest vitest `src/test/e2e-user-zero-selftest.test.ts` (8 testes). Guard do runner endurecido (`includes("runner")` pegava `runner.test.ts`).
> 20	- **Stream A — consistência + Canvas 4.2 (VERIFICADO, não reconstruído):** auditoria material confirmou reference threading + seed-lock (`generateReplicate:675-690`·`generateOpenRouter:749-759` + inspectors/pipeline `findUpstreamImages` + toggle `fixedSeed`) e os 5 nós tipados + pipeline async de vídeo JÁ shipados. Único gap real fechado: `higgsfield-webhook` mapeia `nsfw`/`canceled` p/ razão clara de soft-fail (sem cobrança).
> 21	- **Pre-commit hardening + versionamento:** `scripts/hooks/pre-commit` (cópia versionada; antes só viva em `.git/hooks`) + README; PATTERN ampliado (`sk_/rk_(live|test)_`·`whsec_`·`sbp_`·`sb_secret_`·`r8_`) + tripwire de diretório que escaneia o `e2e-output/` gitignored (defesa Layer 4). Testado: bloqueia secret plantado (exit 1) · libera limpo (exit 0).
> 22	- **Stream C — readiness (gated):** flywheel sondado read-only — `orchestrate-content` HTTP 200, `affiliate_config` Sovereign `ada39fae` mercadolivre `is_active:true`, `mco_balance` 5351, Higgsfield creds presentes. Execução (publica + gasta) **gated em GO Sovereign**.
> 23	
> 24	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (Stream C paga/externa não disparada sem GO; deploy do `higgsfield-webhook` idem).
> 25	
> 26	| Verificação | Resultado |
> 27	|---|---|
> 28	| Selftest e2e-user-zero | ✅ 8/8 (vitest) |
> 29	| Suite completa | ✅ 224 passed / 2 skipped / 226 · **exit 0** — os 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` neste seal (antes falhavam por chave revogada); +8 desta sessão, baseline git-stash 218→226 |
> 30	| `tsc --noEmit` | ✅ 0 erros |
> 31	| Pre-commit tripwire | ✅ bloqueia secret em e2e-output (exit 1) · libera limpo (exit 0) · PATTERN pega sbp_ no staged-diff |
> 32	| Stream A consistência | ✅ wired backend+frontend — verificado por grep material, não reconstruído |
> 33	| Stream C readiness | ✅ orchestrate-content 200 · affiliate ativo · balance 5351 |
> 34	| Handoff node | ✅ `59f92fe0-e346-4320-aeaf-842a91458125` embedded 768d (chunks:1, openai/text-embedding-3-small) |
> 35	| Containers | ✅ 5 healthy · Chroma v2 OK |
> 36	
> 37	| Commit | Conteúdo |
> 38	|---|---|
> 39	| `cf6e464` | feat(e2e-user-zero): 2ª iteração — redactor + mesh-persistor + telemetry + 6 flows + selftest |
> 40	| `e788d76` | chore(hooks): versiona pre-commit + tripwire e2e-output |
> 41	| `09a5bae` | fix(higgsfield-webhook): nsfw/canceled soft-fail claro |
> 42	| `5f21caf` | docs(readme): v6.19.0 |
> 43	| `0c5eefd` | fix(tests): gateia smokes live (canvas pago + sql-bridge) atrás de RUN_LIVE_SMOKE → suíte verde |
> 44	
> 45	### Arquitetura — e2e-user-zero runner (v2)
> 46	```
> 47	runner.ts (focused) → emitRunStarted (telemetry)
> 48	  → flow(driver, ctx) [6 dashboard flows + auth-login, static whitelist]
> 49	  → classify() → buildReport() → report.md + findings.json
> 50	  → insertFindings() [mesh-persistor: observation node + OBSERVES edge, idempotent, fail-soft]
> 51	  → emitRunComplete (telemetry: infra_health_logs pulse) · exit 0/1/2/3
> 52	Defesa de segredo: redactor (Layer 2) → .gitignore e2e-output/ (Layer 3) → pre-commit tripwire (Layer 4)
> 53	```
> 54	
> 55	### Survival Laws Self-audit
> 56	```
> 57	Law 1 (Materiality): ✅ toda claim provada NESTE turno — selftest 8/8 + suite 224/226 + git-stash baseline (prova de zero regressão) + tsc 0 + hook testado (exit 1/0) + handoff node embedded via REST + readiness via curl real. Descoberta-chave: 2 features "pendentes" estavam shipadas (provado por grep de código real antes de codar) → zero retrabalho/fabricação. Excerpt do mesh-persistor do SDD corrigido contra schema real (relation_type + SB_SECRET_KEY).
> 58	Law 2 (Process): ✅ e2e-user-zero BoK 9/9 + SDD como SSOT. Webhook é fix em feature documentada. Desvio consciente: selftest em src/test/ (vitest include=src/**) — justificado. OTD-E2E-TELEM-001 registrada (infra_health_logs sem coluna metadata → migration aditiva diferida a /security-review).
> 59	Law 3 (Pruning): ✅ 2 podas explícitas (relatórios dos subagentes após extração de conclusões; detalhes de impl do Stream B no checkpoint).
> 60	Law 4 (ORO): ✅ triplet por stream; Stream C paga/externa gated em Sovereign.
> 61	```
> 62	
> 63	---
> 64	
> 65	## Constellation v2 Cockpit Live — Fase 3+4 E2E + Build/Login/Settings Fixes Record (2026-06-01)
> 66	
> 67	**v6.18.0 (2026-06-01)** — Sessão densa que levou a Constelação v2 de casca decorativa a **cockpit operacional per-user provado ponta-a-ponta**, mais 3 incidentes de produção resolvidos (build quebrado, P0 login, teste de chaves). Fluxo: `/handson` → resolver alertas prioritários → Fase 3 UI → (o gate de build revelou um blocker pré-existente do lucide) → P0 login reportado pelo Sovereign → Fase 0 reset destrutivo → botão Zerar → teste de chaves falhando (descoberta da cripto de credenciais) → Tabs → Fase 4 E2E provado → este selo.
> 68	
> 69	**O que foi entregue:**
> 70	- **Fase 3 — cockpit (`constellation-v2`, BoK selada `38d7e7a4`):** empty-state com CTA duplo (`EmptyConstellation`) + wizard 2-portas (`CrewWizard` + `useCreateCrew`: mapa 4×4 = Núcleo + 4 Leads + 13 subagentes módulo-bound, OU builder guiado depto→capability→nome) com keys estáveis (FR-CV2-006) + upsert idempotente; `AccessConfigCard` (BYOK + cap diário por subagente, FR-CV2-023); `useAgentTask`+`agent-task-result` (FR-CV2-004: envia `capability_key`, trata 402/422/502+`status:failed`); `useAgentActivity` projeta capability/result nos Live Logs (FR-CV2-050); `CrewGraph` cap≤21 + LOD + z-index estrito (FR-CV2-060/061); botão legado "Deploy Enterprise" → "Criar crew".
> 71	- **Fase 0 — reset destrutivo:** `scripts/reset-constellation-v2.ts --execute` arquivou 35 execs → wipou 746 crew_agents + 717 crew_edges → 0; `profiles`=1 intacto. Verificado independente via REST.
> ```

## 🤖 Claude *(19:17:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 5683,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 5683	       .set("utm_campaign", campaign)
> 5684	
> 5685	  5. INSERT affiliate_links:
> 5686	       original_url · short_url · platform=mercadolivre
> 5687	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 5688	
> 5689	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 5690	
> 5691	ContentLibraryPage monetization flow:
> 5692	  Card (text, body contains mercadolivre.com.br)
> 5693	    └── DropdownMenu → "Monetizar Links ML"
> 5694	          → handleMonetizeLinks(item):
> 5695	               match(ML_URL_RE) → unique URLs
> 5696	               for url of unique:
> 5697	                 POST process-affiliate-link → affiliate_url
> 5698	                 body.split(url).join(affiliate_url)
> 5699	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 5700	          → Badge 💰 ML (emerald) exibido após monetização
> 5701	```
> 5702	
> 5703	---
> 5704	
> 5705	## Pending Actions (Commercial Launch)
> 5706	
> 5707	### CRITICAL — Must complete before first client
> 5708	
> 5709	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 5710	
> 5711	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 5712	
> 5713	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 5714	
> 5715	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 5716	
> 5717	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 5718	
> 5719	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 5720	
> 5721	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 5722	
> 5723	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 5724	
> 5725	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 5726	   ```bash
> 5727	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 5728	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 5729	   ```
> 5730	
> 5731	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 5732	
> 5733	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 5734	
> 5735	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 5736	
> 5737	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 5738	
> 5739	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 5740	
> 5741	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 5742	
> 5743	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 5744	
> 5745	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 5746	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 5747	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 5748	
> 5749	### SOCIAL — Next steps
> 5750	
> 5751	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 5752	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 5753	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 5754	
> 5755	### NON-CRITICAL
> 5756	
> 5757	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 5758	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 5759	- `browserslist` — ✅ updated (2026-04-26)
> 5760	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 5761	
> 5762	### GITNEXUS MCP — Next steps
> 5763	
> 5764	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 5765	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 5766	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 5767	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 5768	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 5769	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 5770	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 5771	
> 5772	### PHASE EPSILON — Next iterations
> 5773	
> 5774	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 5775	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 5776	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 5777	
> 5778	### CORE — Next iterations
> 5779	
> 5780	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 5781	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 5782	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 5783	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 5784	
> 5785	### PHASE DELTA — Next iterations
> 5786	
> 5787	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 5788	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 5789	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 5790	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 5791	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 5792	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 5793	
> 5794	### USUÁRIO ZERO — Checklist de validação
> 5795	
> 5796	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 5797	- ✅ Stripe sandbox secrets no vault
> 5798	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 5799	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 5800	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 5801	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 5802	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 5803	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 5804	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 5805	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 5806	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 5807	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 5808	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 5809	
> 5810	---
> 5811	
> 5812	## Infrastructure
> 5813	
> 5814	| Service | Container | Port | Status |
> 5815	|---------|-----------|------|--------|
> 5816	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 5817	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 5818	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 5819	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 5820	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 5821	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 5822	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 5823	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 5824	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 5825	
> 5826	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 5827	
> 5828	```bash
> 5829	docker compose up -d
> 5830	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 5831	```
> 5832	
> 5833	---
> 5834	
> 5835	## Security Model (Post-Go-Live)
> 5836	
> 5837	| Table | Isolation |
> 5838	|-------|-----------|
> 5839	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 5840	| `mcorch_edges` | Same pattern |
> 5841	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 5842	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 5843	
> 5844	---
> 5845	
> 5846	## Billing Architecture
> 5847	
> 5848	| Decision | Value |
> 5849	|----------|-------|
> 5850	| Canonical billing ledger | `profiles.mco_balance` |
> 5851	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 5852	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 5853	| Orchestration cost | 10 mcoCoins/run |
> 5854	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 5855	| Stripe | Sandbox keys active — swap to live before first client |
> 5856	
> 5857	---
> 5858	
> 5859	## GraphRAG State
> 5860	
> 5861	- **8747 total nodes** (verificado live 2026-06-01 via REST count=exact após o handoff node `59f92fe0` desta seal v6.19.0, 0 sem embedding; v6.8.6 snapshot era 8605, cujo handoff `196b7acf-9035-4d87-a19b-7d7d6b55bee0` embedded 768d via autoembed trigger pg_net) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 5862	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 5863	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 5864	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 5865	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 5866	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 5867	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 5868	- HNSW cosine index operational
> 5869	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 5870	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 5871	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 5872	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 5873	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 5874	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 5875	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 5876	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 5877	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 5878	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 5879	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 5880	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 5881	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 5882	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 5883	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 5884	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 5885	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 5886	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 5887	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 5888	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 5889	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 5890	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 5891	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 5892	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 5893	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 5894	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 5895	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 5896	
> 5897	### Embedding Model
> 5898	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 5899	Schema: `vector(768)` — HNSW cosine index.
> 5900	
> 5901	### Embedding Pipeline (Autônomo — 2026-05-03)
> 5902	Três camadas eliminam intervenção manual:
> 5903	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 5904	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 5905	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 5906	
> 5907	### Comandos de manutenção da Mesh
> 5908	```bash
> 5909	# Verificar nós sem embedding (deveria retornar array vazio):
> 5910	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 5911	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 5912	
> 5913	# Backfill manual (Bun-native — requer .env):
> 5914	bun run scripts/backfill-embeddings.ts
> 5915	
> 5916	# Backfill de código-fonte nos nós AST:
> 5917	bun run scripts/backfill-node-content.ts
> 5918	
> 5919	# Re-sync AST completo:
> 5920	cd packages/gitnexus-core && npm run sync-mesh
> 5921	
> 5922	# Acompanhar re-ingesta pós-commit:
> 5923	tail -f /tmp/mcorch-ingest.log
> 5924	```
> 5925	
> 5926	---
> 5927	
> 5928	## Video Rescue Protocol
> 5929	
> 5930	When a video generation operation (Google Veo) times out or client disconnects:
> 5931	```bash
> 5932	# Via edge function (production):
> 5933	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 5934	  -H "Authorization: Bearer <user_jwt>" \
> 5935	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 5936	
> 5937	# Via local script (admin/debug):
> 5938	source .env && bun run rescue.ts <operation_id> <content_id>
> 5939	```
> 5940	
> 5941	---
> 5942	
> 5943	## Architecture Pillars
> 5944	
> 5945	| Layer | Implementation |
> 5946	|-------|---------------|
> 5947	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 5948	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 5949	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 5950	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 5951	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 5952	
> 5953	---
> 5954	
> 5955	## Phase Delta — Architecture
> 5956	
> 5957	```
> 5958	OrchestrationPage (full-canvas, p-0)
> 5959	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 5960	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 5961	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 5962	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 5963	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 5964	        ├── nodes/PublishNode.tsx    ← final distribution output
> 5965	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 5966	        └── NodePalette.tsx          ← top toolbar to add nodes
> 5967	
> 5968	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 5969	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 5970	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 5971	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 5972	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 5973	```
> 5974	
> 5975	### Canvas State Architecture (Hybrid)
> 5976	
> 5977	```
> 5978	User interaction → ReactFlow internal state (positions, drag)
> 5979	                         ↓ (debounced 600ms)
> 5980	                   localStorage (positions persist across refresh)
> 5981	                         ↑
> 5982	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 5983	     ↓ (status changes sync to ReactFlow via useEffect)
> 5984	ReactFlow renders visual status (idle/running/done/error/blocked)
> 5985	```
> 5986	
> 5987	## Key Files
> 5988	
> 5989	| Purpose | Path |
> 5990	|---------|------|
> 5991	| Architecture rules | `CLAUDE.md` |
> 5992	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 5993	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 5994	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 5995	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 5996	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 5997	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 5998	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 5999	| **Node types** | `src/components/orchestrator/nodes/` |
> 6000	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 6001	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 6002	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 6003	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 6004	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 6005	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 6006	| Billing utilities | `src/lib/billing.ts` |
> 6007	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 6008	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 6009	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 6010	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 6011	| Video rescue (local) | `rescue.ts` |
> 6012	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 6013	| Backfill script | `scripts/backfill-embeddings.ts` |
> 6014	| Deploy harness | `scripts/harness-deploy.sh` |
> 6015	
> 6016	---
> 6017	
> 6018	## First Client Onboarding Checklist
> 6019	
> 6020	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 6021	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 6022	3. ~~Activate watchdog cron~~ ✅ Done
> 6023	4. ~~Deploy rescue-video function~~ ✅ Done
> 6024	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 6025	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 6026	7. Monitor `infra_health_logs` for first 24h.
> 6027	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 6028	
> 6029	---
> 6030	
> 6031	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 6032	
> 6033	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 6034	
> 6035	| Action | Result |
> 6036	|--------|--------|
> 6037	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 6038	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 6039	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 6040	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 6041	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 6042	
> 6043	| Commit | Conteúdo |
> 6044	|--------|----------|
> 6045	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 6046	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 6047	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 6048	
> 6049	### Arquitetura Matrix Intelligence
> 6050	
> 6051	```
> 6052	ConstellationMatrix (Stabilized Engine)
> 6053	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 6054	  └── NodeDetailsPanel (Tabbed Navigation)
> 6055	        ├── Tab Meta: Neighbor exploration + Net Context
> 6056	        ├── Tab Code: Source code preview (Supabase sync)
> 6057	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 6058	
> 6059	useNodeIntelligence Hook:
> 6060	  - contentQuery: fetch nodes.content column
> 6061	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 6062	  - state: isAnalyzing, analysisResult, progress
> 6063	```
> 6064	
> 6065	---
> 6066	
> 6067	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 6068	
> 6069	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 6070	
> 6071	| Action | Result |
> 6072	|--------|--------|
> 6073	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 6074	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 6075	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 6076	
> 6077	**Output da análise (estruturado em pt-BR):**
> 6078	- Visão Geral — papel do módulo no sistema
> 6079	- Padrões Detectados — design patterns, antipatterns
> 6080	- Acoplamento & Dependências — análise In/Out-Degree
> 6081	- Recomendações — 1-3 ações priorizadas
> 6082	
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> OK aios-sql-bridge — BoK complete
> OK canvas-design — BoK complete
> OK constellation-v2 — BoK complete
> OK conteudo-v2 — BoK complete
> OK e2e-user-zero — BoK complete
> OK gamificacao-nodes — BoK complete
> OK mcorch-constellation — BoK complete
> OK mcorch-qa-healing — BoK complete
> OK mercado-livre-api — BoK complete
> OK meta-api — BoK complete
> OK openclaw — BoK complete
> OK viralmind — BoK complete
> ```

## 🤖 Claude *(19:17:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-40 of 175 total (30843 tokens, cap 25000). Call Read with offset=41 limit=40 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 8	
> 9	**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 10	
> 11	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 12	
> 13	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 14	
> 15	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 16	
> 17	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 18	
> 19	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 20	
> 21	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 22	
> 23	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 24	
> 25	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 26	
> 27	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 28	
> 29	**Sprint v6.1.0 selado em 2026-05-14** — Canvas Studio UX Shell + Higgsfield Fix: shell do Canvas Studio migrado do `viralmind-builder` (store Zustand+zundo, lanes overlay, TopBar/LeftPanel/StatusBar, catálogo de 9 receitas, ImageLightbox, PipelineEdge); `canvas-execute` com endpoint Higgsfield corrigido (`platform.higgsfield.ai` rota Soul) + RPC `deduct_mco_coins`. Plano Phase 4.2 selado em `~/.claude/plans/floating-sleeping-sparrow.md`.
> 30	
> 31	**Sprint v6.1.1 selado em 2026-05-14** — viralmind BoK Suite Sealed: dívida documental do override consciente do BoK Gate quitada. 6 docs autorados (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) + `04-frd` reescrito de handbook CLAUDE.md → FRD real (32 FR + 14 NFR + matriz PR→FR). Ancorado nas 10 tabelas `vm_*` + 6 enums + Edge Functions `fetch-trends`/`canvas-execute`. Mesh seal `bok-scribe-seal-viralmind-v1` (`documentation_suite`, stability 0.85, revenue_impact R\$14M, embedded 768d). 7 OTDs registrados (destaques: `vector(1536)` vs padrão `768` sem índice HNSW — FMEA-VM-002 RPN 288; bucket `canvas-assets` público — FMEA-VM-003 RPN 140). BoK Gate do viralmind **liberado**. Sessão selada com ~51% de contexto — Canvas Studio Phase 4.2 diferida para sessão nova. 7463 nós · 100% embedded. 6 commits granulares. **Pendência conhecida (não desta sessão):** `docs/bok/gamificacao-nodes/` incompleta (5/9 docs) — rodar `/bok-scribe` ou completar antes de tocar o módulo.
> 32	
> 33	**Sprint v6.6.9 selado em 2026-05-20** — mcorch-qa-healing v1 — Material Proof Gate: novo módulo de QA sênior que fecha a fraqueza de Lei 1 (Materialidade) — o bloco Survival Laws Self-audit do `/handoff` era auto-declarado; agora é verificado mecanicamente pela nova **Fase 5c**. Executado em 6 stages na ordem de governança não-negociável (BoK → SOP → código): suíte BoK 9/9 `docs/bok/mcorch-qa-healing/` (1423 LOC, 6ª suíte do projeto, gerada via `/bok-scribe`, campos de mercado/monetização honestamente N/A para tooling interno) + SOP `docs/processes/handoff-material-proof-audit.md` (Lei 2) + engine `scripts/qa/` (5 módulos Bun, 710 LOC, injeção de dependências para reuso pelo cron OpenClaw) + skill `mcorch-qa-healing` + Fase 5c wired no `/handoff` (entre 5b e 6 — bloqueia em qualquer 🔴) + 2 suítes Vitest. O dry-run contra o selo v6.6.8 real pegou e fechou um falso-positivo (`COMMIT_RE` agarrava prefixos de UUID de 8-hex como commits — FMEA-002 fechada antes do gate ir ao ar). **Material proofs**: TS zero erros · 165 testes (122→165, +43) · **Fase 5c ao vivo neste selo → 13 verified · 0 skipped · 0 failed → SEAL ALLOWED** · 9 commits granulares · milestone node `a08780dc-f665-47c5-b34b-a2eb7c9eea5c` + documentation_suite seal `b00e938a-717b-4f62-b936-f4934845ec52` (DERIVES_FROM openclaw seal) embedded 768d · mesh **8361+ nodes** · Survival Laws Self-audit 4/4 ✓. **Hazard registrado**: agente main do OpenClaw (Qwen3.5 local) operou na mesma working dir durante a sessão — 3 diretórios gitignorados, zero overlap de path. **Próximo**: Canvas Design (Initiative B — integração `nexu-io/open-design`) em sessão dedicada via `/bok-scribe canvas-design`.
> 34	
> 35	**Sprint v6.6.8 selado em 2026-05-19** — Bridge Recovery + MAPE-K Audit + SDD aios-sql-bridge + Survival Laws 4/4: sessão de auditoria reativa disparada por Sovereign observando `claw.gcrux.com/dreaming` stagnation (Imported Insights congelado em 2026-05-16, Memory Palace counts estáticos, Dream Scene "0 promovido"). **Root cause material**: Stage 2 cron `nightly-bridge-refresh.sh` invocava `node` PATH-resolved como v18.19.1 no env do user `ubuntu` apesar do interativo ter v22.22.3 — OpenClaw CLI exige v22.12+ → 100% FAIL silently em Step 3 (reindex SQLite) há ≥3 dias; Steps 1+2 (bridge + distribute) rodavam clean. **Fix dual no mesmo edit**: (1) `NODE_BIN=/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolved-target (não symlink); (2) descoberta runtime de bug latente segundo — `claw-master` foi adicionado em v6.3.1 ao distribute script MAS NÃO ao indexer loop (`for agent in main artisan engineer scientist marketing-growth guardian; do` omitia claw-master) → `claw-master.sqlite` stale May 16 → exatamente o checkpoint "AIOS Core v2 (2026-05-16)" que Sovereign observou na UI. **SOP first per Lei 2**: `docs/processes/openclaw-bridge-recovery.md` 86 LOC autorada ANTES do edit. **5 phases materializadas** (todas com ORO triplet + Survival Laws ✓): Phase A (bridge fix + claw-master loop), Phase B (MAPE-K closed-loop audit + 4 observation nodes em mesh — Plan `a4c4c026` / Execute `69f6e356` / Monitor `d605bdda` / Analyze `d8952ce8` com edges DERIVES_FROM v6.6.7), Phase C (9 untracked files versionados via 3 commits: miv landing assets + miv tools + memory audit trail), Phase D (esta seal + milestone `c4643058`), Phase E (OTD-SSP01-001 closed via SDD `aios-sql-bridge` 376 LOC enterprise-grade + 00-index 69 LOC suite skeleton + documentation_suite seal `4e0acc7e` stability 0.85 DERIVES_FROM openclaw seal). **Material proofs**: 6 commits granulares pushed (`03911e9` fix(cron) + `cbdee4f` feat(landing) + `bb1cc96` chore(tools) + `2aa80f1` chore(memory) + `1b3bdd8` docs(bok) + `b71b991` docs(handoff) + `230ad70` docs(readme)); 7/7 SQLites OpenClaw reindexed (was 0/6 fail); log final `[2026-05-19T19:06:32-03:00] nightly-bridge-refresh DONE (zero failures)`; mesh **8359 nodes** (+6 desta seal); TS zero erros; 5 containers healthy. **Survival Laws Self-audit 4/4 ✓ pela primeira vez consecutivamente desde v6.6.0** — encerra retroativamente OTD-PROC-001 (RPN 60) + OTD-PROC-002 (RPN 40) + OTD-SSP01-001 (RPN 240 SLA 2026-05-24). **Pending TOP**: OE-661 Step 1.5 first-run E2E (Sovereign click `/dashboard/orchestration` TriggerNode); OTD-OE661-PER-USER refactor (SLA 2026-06-02, 14 dias); MAPE-K gaps 1/2/3 implementáveis em v6.7.x/v6.8.x conforme plans dedicados (recomendações registradas no mesh, aguardam acionamento).
> 36	
> 37	**Sprint v6.6.7 selado em 2026-05-19** — OE-661 Phase 1 Prep + API Tenancy Directive: sessão executou parcialmente o plan persistido OE-661 — toda a preparação completada, Step 1.5 (first run E2E) **DEFERRED** por context budget Sovereign 92% (retoma em ~3h). Infraestrutura material: SOP `docs/processes/orchestration-content-mesh-asset-emission.md` (120 LOC) escrita ANTES do código (Lei 2); `orchestrate-content/index.ts:404-465` emite `content_mesh_asset` em paralelo com observation via `Promise.allSettled` (Amendment A) gated por `wpPostUrl` (Amendment B); `link-forge.ts:153` ganha `.eq("project_id", "mcorch-affiliate")` (Amendment C); `handle-ml-postback/index.ts` ganha pulse `infra_health_logs` em 4 return paths (Amendment E — fecha cegueira de 17 dias). Deploys material: `orchestrate-content` 113.6kB + `handle-ml-postback` 60.45kB. Vault `GCRUX_ML_AFFILIATE_TOKEN` provisionado (digest `e86f74a0...`). **DIRETIVA SOVEREIGN-CLASS NOVA "API Tenancy Model"** emitida durante sessão (questionamento direto sobre por que usar env global se `affiliate_config` per-user já existia) — selada em 3 superfícies: `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` com resolution order de 3 níveis + 5 tabelas canônicas + 5 anti-patterns; `CLAUDE.md > Code standards` one-liner enforcement; auto-memory `feedback_api_tenancy_per_user.md` indexada. **OTD-OE661-PER-USER** registrada (RPN 120 · SLA 2026-06-02) catalogando violação em `link-forge.ts` + `process-affiliate-link` GET branch. Sovereign autorizou Opção B (provisionar global temporário com `affiliate_config.app_id` value, deferir refactor). **Survival Laws Self-audit retroativo (Amendment H)** v6.6.1..v6.6.5 + esta seal — conclusão: Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 (overrides conscientes v6.6.1+v6.6.3) · Lei 3 ✗ 0/5 (OTD-PROC-002 RPN 40) · Lei 4 ✗ 0/5 (OTD-PROC-001 RPN 60 — esta seal v6.6.7 começa cumprimento). **Material proofs**: TS zero erros · 122/122 testes em 4.84s · 7 commits granulares locais (`03f6822` SOP · `e662da3` orchestrate Amendments A+B · `bafac16` link-forge Amendment C · `9cec88a` postback Amendment E · `044f21e` CLAUDE+OTD diretiva · `96ee72a` README v6.6.7 · `7d06934` HANDOFF seal + redactions) · milestone node `9d482014-a759-4656-93d9-99e05ab4a714` embedded 768d · mesh **8353 nodes** (+1 desde v6.6.6) · 11650 edges (+33). Path correção material: `/dashboard/orchestrate` → `/dashboard/orchestration` (Sovereign clarification). **Próximos deliverables**: (a) Sovereign dispara primeira campanha real em `/dashboard/orchestration` (TriggerNode + topic Link Forge catálogo + wp+linkedin platforms + Run) → eu monitoro pipeline_runs + content_mesh_asset emit material via REST; (b) ao completar, synthetic postback chain (Amendment D) + cleanup (Amendment J); (c) selar v6.6.8 com flywheel rodando E2E pela primeira vez na história do projeto; (d) atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias) — SDD `aios-sql-bridge`; (e) executar Phase 2 (`mcoins-ledger-reconciliation.md`) — fecha OTD-V660-001.
> 38	
> 39	**Sprint v6.6.6 selado em 2026-05-19** — Planning Seal + Debt Audit + Self-audit Retroativo: sessão dedicada a (a) `/handson` brief v6.6.5; (b) persistir execution plan dos 3 carry-overs OE-661 + Ledger SOP + Canvas 4.2c por diretiva Sovereign "slave o plano atual para posteriormente implantar"; (c) auditoria completa em 3 frentes paralelas; (d) emendas críticas; (e) /handoff oficial. **Zero código de produção tocado**. Plan persistido em `.claude/context/execution-plan-oe661-carryovers.md` (~403 LOC, md5 `0e5f0ba9...`) + observation node `3dde2572-cad6-491b-b523-c56ec763ff8e` (autoembed 768d). Audit em `.claude/context/audit-2026-05-19-oe661-debt-sweep.md` (~297 LOC, md5 `5c4f8a9f...`) + observation node `6164c80f-cadd-48d5-95a4-f87f22ebd09b` + DERIVES_FROM edge `acb4b0d9-091d-4973-96a8-d40515be7990`. **21 OTDs ativos catalogados (8 RPN ≥ 100): VM-OTD-001 RPN 288 viralmind HNSW · OTD-SSP01-005 RPN 280 admin claim · OTD-SSP01-001 RPN 240 SLA 2026-05-24 · OTD-V660-002 RPN 150 · VM-OTD-004 RPN 140 · OTD-V660-001 RPN 120 (coberta pelo plan Phase 2) · OTD-V660-003 RPN 80 · OTD-CV42C-001**. **5 inconsistências processuais**: (1) **5 seals consecutivas (v6.6.1..v6.6.5) omitiram bloco mandatory Survival Laws Self-audit** — Severidade ALTA; (2) Survival Audit v2 não re-rodado em 32 dias; (3) 3 SOPs implícitas não formalizadas; (4) HANDOFF v6.6.3 claimed 4 content_mesh_asset mas reality = 1 row (3 "products" têm `node_type='feature'`); (5) `handle-ml-postback` cego — zero `infra_health_logs` em 17 dias. **4 bugs concretos no plan**: A race condition obs+asset não atômicos · B wpPostUrl null não gated · C Link Forge query global sem project_id · D postback content_id drift. **10 amendments aplicados** (A-J) via Amendments Appendix no topo do plan. Schema drift fixed: `infra_health_logs.created_at` NÃO EXISTE (real: `last_seen_at`). **Predicted Survival Audit v3** (não emitido formalmente): Memory 5/5 · Skill 4/5 · Cost Discipline 4.5/5 ↑ · Observability 4/5 ↑ · SOP 5/5 · **avg 4.4/5 · min 4/5** — Phase Commercial threshold mantido. **Material proofs**: 14 integrity checks paralelos · 4 commits granulares (`ea7efaf` plan + `44e464c` audit + `fb6f07d` README + `99d70f6` handoff seal) push → origin/main · milestone handoff node `821dc554-78e2-4abb-999d-37363c5df6c9` embedded 768d · mesh total **8352 nodes** (+4 desde v6.6.5). **Próximos deliverables**: (a) Sovereign autoriza execução das Fases 1-3 do plan quando convier (bugs A-D já fixed); (b) **atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias)** — BoK Gate override `aios-sql-bridge` precisa SDD; (c) provisionar `SUPABASE_POOLER_URL` (OTD-V660-003); (d) materializar Survival Audit v3 formal antes de Phase Commercial; (e) executar Phase 2 do plan (SOP `mcoins-ledger-reconciliation.md`) — Sovereign-only — fecha OTD-V660-001.
> 40	
> ```

## 🤖 Claude *(19:17:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"OK $slug \u2014 BoK complete\" || echo \"INCOMPLETE $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "Check BoK suite completeness for all slugs"
}
```

## 🤖 Claude *(19:18:30)*


## 🤖 Claude *(19:18:51)*

All green. Working tree clean and exactly at `origin/main` (0/0 divergence), TypeScript zero errors, 5 containers healthy, Chroma v2 alive, all 12 BoK suites complete, scratch clean. Here's the brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — v6.19.0 · e2e-user-zero v2 + 3-Stream Sweep (selado 2026-06-01)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
**Fase selada:** v6.19.0 — e2e-user-zero 2ª iteração (harness executável) + sweep de 3 streams. Lição dominante: *o código estava sistematicamente à frente dos Pending Actions* — verificação material (Lei 1) antes de codar evitou reconstruir 2 features já shipadas.

Últimos commits:
- `865ded6` — chore(sprint): selo v6.19.0 (suíte verde, 8747 nós)
- `08bb72a` — docs(handoff): paths completos + gating dos smokes live
- `0c5eefd` — fix(tests): gateia smokes live atrás de `RUN_LIVE_SMOKE`
- `5f21caf` — docs(readme): v6.19.0
- `09a5bae` — fix(higgsfield-webhook): nsfw/canceled → soft-fail claro

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ — HEAD idêntico a `origin/main` (0↔0). Tudo pusheado.

🏗️ **INFRA**
- `mcorch_chroma`: Up 8 days (healthy) — Chroma API v2: **OK** (heartbeat respondendo)
- `mcorch_claude_mem`: Up 8 days (healthy)
- `mega-brain-{daemon,webhook,dashboard}`: healthy / up — 5 containers verdes

🧠 **KNOWLEDGE MESH**
**8747 nós · 9070 arestas** (fonte: HANDOFF GraphRAG State, verificado live 2026-06-01) — 100% embedded (768d HNSW cosine). Handoff node desta seal: `59f92fe0`.

🔧 **TYPESCRIPT**
Zero erros ✅ (`tsc --noEmit` exit 0)

📚 **BoK SUITES** (12/12 completas — 9 docs cada)
Sealed: `aios-sql-bridge · canvas-design · constellation-v2 · conteudo-v2 · e2e-user-zero · gamificacao-nodes · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · viralmind`
Incomplete: **nenhuma** — BoK Gate liberado para qualquer módulo.

📌 **SPRINT**
**Goal:** Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente; Twitter desbloqueia ao subir tier; Instagram após App Review Meta.
**SLA vivo:** `OTD-LLM-FALLBACK` (Resilience Debt — LLM Cascading Fallback, owner `engineer`) vence **2026-06-07 (6 dias)**.

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **🟢 Stream C — primeira campanha real (flywheel E2E)** — readiness **verde** na seal (orchestrate-content HTTP 200 · `affiliate_config` ML `ada39fae` ativo · `mco_balance` 5351 · Higgsfield creds presentes). É o primeiro run monetizado ponta-a-ponta da história do projeto. **Gated em GO Sovereign** (publica conteúdo real + gasta mcoCoins + gera link ML real). Só falta seu GO.
2. **Deploy `higgsfield-webhook`** — o fix nsfw/canceled (`09a5bae`) está **commitado mas NÃO deployado** (deploy externo gated em GO na seal). Materializa o único gap real fechado do Stream A.
3. **Canvas Design module** (`nexu-io/open-design`) — BoK agora **completa**, Gate liberado; sessão dedicada. **OU** atacar `OTD-LLM-FALLBACK` antes do SLA de 2026-06-07.

⚠️ **ALERTAS**
- Nenhum bloqueador ✅ (TS limpo · containers verdes · worktree sincronizado · scratch limpo).
- Débito menor registrado: `OTD-E2E-TELEM-001` — `infra_health_logs` sem coluna `metadata`; migration aditiva diferida ao `/security-review`.
- 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` — intencional (evita gasto + dependiam da chave revogada).

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

Dois itens de alto valor estão **prontos e só aguardam seu GO**: a primeira campanha real (Stream C) e o deploy do `higgsfield-webhook`. Quer que eu dispare algum deles, ataque o `OTD-LLM-FALLBACK` (SLA em 6 dias), ou siga outra direção?

## 👤 User *(19:26:46)*

Acabei de verificar a pagina https://login.mcorch.com/dashboard/affiliate-products mas quando copio o link (https://panel.gcrux.com/api/ml-redirect?product_id=MLB27834876&affiliate_id=3286108278277786&utm_source=gcrux_orchestrator&utm_medium=content_mesh&utm_campaign=highticket_smarthome_q3&utm_content=9531223a-14df-4654-85fd-ac1df5c21110) que não funciona quando abro o link aparece a tela de login para eu fazer login no cloudPanel, mesmo tentando logar quando tento novamente ainda pede login. Deveria abrir o produto igual abre quando clico em "Ver no ML" certo? 

Quando clico no botão ver no ml abre o link https://www.mercadolivre.com.br/p/MLB27834876 corretamente conforme no print. Mas como pode ver se eu clicar em compartilhar vejo as seguintesopções.:

Gerar link / ID de produto
Etiqueta em uso:

caga6077534
Link do produto
https://meli.la/2gh13Sw

ID do produto
XH34WX-9SWV

Compartilhe o ID para o público encontrar o produto pelo buscador do Mercado Livre.
Texto sugerido
🔍 Cole este texto no buscador do Mercado Livre: XH34WX-9SWV

🔗 Ou acesse o link:
https://meli.la/2gh13Sw

Adicionamos o produto à lista "Minhas recomendações", compartilhe-a para gerar mais vendas.

## 🤖 Claude *(19:27:22)*


## 🤖 Claude *(19:27:25)*

Esse é um bug de produção real no caminho de receita (link de afiliado quebrado = zero atribuição). Vou diagnosticar materialmente antes de propor qualquer fix.

**ORO triplet desta task:**
- **Operator:** MCORCH Agent
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign — caminho de afiliado ML; link quebrado = receita perdida + atribuição zerada

Deixa eu rastrear de onde sai esse link `panel.gcrux.com/api/ml-redirect` no código.

## 🤖 Claude *(19:27:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== ml-redirect refs ===\"; rg -n \"ml-redirect\" --no-heading 2>/dev/null | head -40\necho \"=== panel.gcrux refs ===\"; rg -n \"panel\\.gcrux\" --no-heading 2>/dev/null | head -40\necho \"=== gcrux.com refs (non-login) ===\"; rg -n \"gcrux\\.com\" --no-heading -g '!*.md' -g '!HANDOFF.md' 2>/dev/null | grep -vE \"login\\.mcorch\" | head -40",
  "description": "Search for ml-redirect and panel.gcrux references"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (31KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/d4434afb-c259-4270-a01a-03d85ba37719/tool-results/bvzq8r063.txt
> 
> Preview (first 2KB):
> === ml-redirect refs ===
> HANDOFF.md:858:**v6.14.2 (2026-05-30)** — Sessão de correção material disparada por reconciliação da v6.14.1 sob a Lei 1 (Materialidade). **Retificação:** a v6.14.1 afirmou *"Resolução OTD-ML-001 / IDs reais"*, mas materialmente o `link-forge.ts:74` ainda roteava via `panel.gcrux.com/api/ml-redirect`, que retorna **`302 → /login`** (login wall, zero atribuição — verificado por `curl -D-`). A troca de IDs MLB passava por um proxy morto; o audit `SEAL ALLOWED` foi obtido com `--bypass` (pulou o E2E) → não é prova limpa.
> HANDOFF.md:871:| `panel.gcrux.com/api/ml-redirect?product_id=MLB27834876` | ❌ `302 → /login` (login wall — o bug que a v6.14.1 não viu) |
> HANDOFF.md:2239:**OE-661 DEBT LIQUIDATION v6.6.3 SHIPPED (2026-05-18).** Sessão executou o roadmap OE-661 inteiro em uma única passada, fechando 3 das 4 dívidas críticas declaradas em CLAUDE.md + a dívida implícita OE-661-003 (Target Binding) documentada em FRD/SDD. **(Phase 0 Hybrid restore — process-affiliate-link)** O refactor pré-existente (-222 LOC) que virou a função em redirect 302 puro quebrava silenciosamente o caller em `src/pages/ContentLibraryPage.tsx:744` (POST com `{product_url, content_id}` esperando `{affiliate_url, self_healed}`). Restaurada a árvore completa POST (auth Supabase JWT + URL probe HEAD 8s + self-heal via `findSimilarProduct` na API pública ML + buildAffiliateUrl com UTMs + persistência em `affiliate_links`) e **adicionado** branch GET 302 público para servir as URLs forjadas pelo Link Forge (`product_id` + `content_variant_id` → 302 Location `panel.gcrux.com/api/ml-redirect?...`). Deploy com `--no-verify-jwt` para permitir clique anônimo do leitor; POST valida JWT internamente. Script size **78.31 kB**. Smoke material: GET 302 + Location header confirmado; POST sem auth retorna função 401 (não gateway). **(Phase 1 Postback Debt — scientist)** `handle-ml-postback/index.ts:154-188` captura `obsNode.id` retornado do INSERT da observation e cria a aresta `ATTRIBUTES
> ...
> </persisted-output>
> ```

## 🤖 Claude *(19:27:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== AffiliateProductsPage exists? ===\"; ls -la src/pages/AffiliateProductsPage.tsx 2>&1\necho \"=== useAffiliateProducts exists? ===\"; ls -la src/hooks/useAffiliateProducts.ts 2>&1\necho \"=== ml_redirect / ml-redirect string refs ===\"; rg -n \"ml_redirect|ml-redirect|api/ml\" --no-heading 2>/dev/null | head -20",
  "description": "Locate affiliate products files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === AffiliateProductsPage exists? ===
> -rw-rw-r-- 1 ubuntu ubuntu 8220 May 30 13:00 src/pages/AffiliateProductsPage.tsx
> === useAffiliateProducts exists? ===
> -rw-rw-r-- 1 ubuntu ubuntu 1816 May 29 16:57 src/hooks/useAffiliateProducts.ts
> === ml_redirect / ml-redirect string refs ===
> HANDOFF.md:858:**v6.14.2 (2026-05-30)** — Sessão de correção material disparada por reconciliação da v6.14.1 sob a Lei 1 (Materialidade). **Retificação:** a v6.14.1 afirmou *"Resolução OTD-ML-001 / IDs reais"*, mas materialmente o `link-forge.ts:74` ainda roteava via `panel.gcrux.com/api/ml-redirect`, que retorna **`302 → /login`** (login wall, zero atribuição — verificado por `curl -D-`). A troca de IDs MLB passava por um proxy morto; o audit `SEAL ALLOWED` foi obtido com `--bypass` (pulou o E2E) → não é prova limpa.
> HANDOFF.md:871:| `panel.gcrux.com/api/ml-redirect?product_id=MLB27834876` | ❌ `302 → /login` (login wall — o bug que a v6.14.1 não viu) |
> HANDOFF.md:2239:**OE-661 DEBT LIQUIDATION v6.6.3 SHIPPED (2026-05-18).** Sessão executou o roadmap OE-661 inteiro em uma única passada, fechando 3 das 4 dívidas críticas declaradas em CLAUDE.md + a dívida implícita OE-661-003 (Target Binding) documentada em FRD/SDD. **(Phase 0 Hybrid restore — process-affiliate-link)** O refactor pré-existente (-222 LOC) que virou a função em redirect 302 puro quebrava silenciosamente o caller em `src/pages/ContentLibraryPage.tsx:744` (POST com `{product_url, content_id}` esperando `{affiliate_url, self_healed}`). Restaurada a árvore completa POST (auth Supabase JWT + URL probe HEAD 8s + self-heal via `findSimilarProduct` na API pública ML + buildAffiliateUrl com UTMs + persistência em `affiliate_links`) e **adicionado** branch GET 302 público para servir as URLs forjadas pelo Link Forge (`product_id` + `content_variant_id` → 302 Location `panel.gcrux.com/api/ml-redirect?...`). Deploy com `--no-verify-jwt` para permitir clique anônimo do leitor; POST valida JWT internamente. Script size **78.31 kB**. Smoke material: GET 302 + Location header confirmado; POST sem auth retorna função 401 (não gateway). **(Phase 1 Postback Debt — scientist)** `handle-ml-postback/index.ts:154-188` captura `obsNode.id` retornado do INSERT da observation e cria a aresta `ATTRIBUTES_REVENUE_TO` (source=observation revenue_conversion_event, target=content_mesh_asset, weight=revenueCents). Target match endurecido: prefere `node_type='content_mesh_asset'` com `.maybeSingle()`; fallback OR sem filtro para legacy nodes. Deploy **59.34 kB** (+0.6 kB). Smoke material chain (synthetic): test affiliate_link `adb9e131-2835-4612-8165-d0fd69c79d6b` → observation `f65d52b2-727b-4f78-a615-99abd664521f` → edge `65d072fe-ff0e-476d-ade6-eb8c8e518a32` (rel=ATTRIBUTES_REVENUE_TO, target=`f3a091f7-9e72-4927-b0cb-2b65cffa9844` content_mesh_asset, weight=125). Patch decision já pré-existia em mesh: `d82e2554-f5c5-455e-bc92-a59ce2474976`. **(Phase 2 Auto-Stitching OE-661-003)** `embed-mcorch-node/index.ts` ganha branch que executa APÓS o UPDATE do embedding — se `node.node_type === 'observation'`, regex `FILE_PATH_RE` extrai paths .ts/.tsx/.js/.md/.sql/.sh/.json/etc do conteúdo (+ nome), busca cada path via ILIKE em `mcorch_nodes WHERE node_type IN ('ast_file','markdown_file','vault_note')`, INSERTa edge `observes` com weight=1.0 (dedup via existence check). Fallback obrigatório a CLAUDE.md (lookup OR `name.eq.root:CLAUDE,name.ilike.%CLAUDE.md%` — legacy ingest stripped `.md`) quando nenhum path resolve. Best-effort: nunca bloqueia response. Deploy **105.1 kB** (~+6 kB). Retrofit: `scripts/stitch-fallback.js` (patched OR filter para `root:CLAUDE`) costurou 6 orphans pré-existentes ao anchor `2747e164-76f6-4467-a6d0-fcbc238af68b` (root:CLAUDE markdown_file). `scripts/audit-mesh-edges.ts` reescrito (bug schema `type`→`node_type` + types ['ast_file','markdown_file','vault_note','source_code']) reporta material: **10/10 observations VALID (100% Target Binding coverage)**. Live auto-stitch confirmado em embed re-invoke `{stitched:1}` para observation `f65d52b2` criando edge `2e1e57db-ae9d-4784-9f29-232aaa174ee8`. **(Phase 3 Link Forge OE-661-004)** Novo `scripts/link-forge.ts` (Bun-native, ~220 LOC, mirror padrão `backfill-embeddings.ts`) varre todos os `content_mesh_asset` da malha, aplica 3 regex globais (Roborock S8 → `MLB3981745621` + Samsung Neo QLED 8K|samsung 8k → `MLB3546719283` + Family Hub → `MLB3728491023`), substitui menções por markdown links `[display](https://panel.gcrux.com/api/ml-redirect?product_id=MLB...&affiliate_id=$TOKEN&utm_*=...&utm_content=$node.id)` (utm_content carrega node.id para closing-the-loop com `ATTRIBUTES_REVENUE_TO`), UPDATE atomic no `content` + INSERT idempotente da aresta `CONTAINS_LINK_FOR` (source=content_mesh_asset, target=product node `feature` criado on-demand via `ensureProductNode`). Flag `--dry-run` preserva Lei 1 antes do live (preview char-delta + product nodes a criar). Smoke chain contra `f3a091f7`: dry-run preview 179→905 chars + 3 produtos novos; live: 1 content updated + 3 CONTAINS_LINK_FOR edges (`884fceef`, `f4f4146c`, `c834ca23`) + 3 product nodes (`77ac9b9f` Roborock, `3d12ac89` Samsung 8K, `92a60fc0` Family Hub). **Pendência crítica:** `GCRUX_ML_AFFILIATE_TOKEN` no `.env` ainda DEFAULT — Sovereign precisa provisionar antes do primeiro run em conteúdo real. **(Phase 4 Memory ingest)** `scripts/ingest-new-docs.cjs` upsert-ingere 4 markdown_files via REST + trigger autoembed: `8ad38681-a14c-4141-9c0c-3509271e0ac6` (.claude/skills/gateway-recovery.md — Memory Debt sealed), `549e01a4-4b7a-4c2a-b8d9-7d8f3e642a12` (docs/bok/mcorch-constellation/roadmap-v1.md — 30-day plan), `5e957727-92bb-4a6a-8c91-b9fcd4833ca2` (docs/bok/mcorch-constellation/revenue-flywheel.md — topologia ROI), `d1296632-d52c-4d93-b6b3-dc118b2c9f56` (scripts/link-forge-scope.md). 100% embedded 768d HNSW cosine. **Material proofs**: 6 commits granulares (56ed242 affiliate · dfabb17 postback · 1f368c1 auto-stitch · 140f248 link-forge · 27c7105 skills+docs+utility · c12906b CLAUDE+BoK rule) + handoff seal (este) + sprint update; TS `tsc --noEmit` zero erros (após fix do node symlink `/home/ubuntu/.local/bin/node`); 122/122 testes passam em 3.39s; 3 Edge Functions deployed (process-affiliate-link 78.31kB · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB); milestone node `6f2cf405-4bb5-440b-a02a-9579fc39f29f` embedado (768d via trigger). **Financial Debt (Stripe live keys)** — **DEFERRED por decisão Sovereign** (memory `project_stripe_strategy.md`); swap somente quando primeiro cliente externo. **Próximo deliverable:** (a) provisionar `GCRUX_ML_AFFILIATE_TOKEN` na vault Supabase + reload local `.env` para Link Forge produzir URLs reais; (b) hookar `orchestrate-content` ou processo equivalente para emitir `content_mesh_asset` nodes pós-geração (atualmente só 4 nós existem, sendo 3 product + 1 smoke test) — sem esses nodes Link Forge é noop em produção; (c) primeiro run end-to-end Usuário Zero validando o flywheel completo (orchestrate → WordPress → social → ML afiliado → handle-ml-postback → ATTRIBUTES_REVENUE_TO → ROIWidget); (d) cleanup OE-661 smoke artifacts (4 test nodes opcional).
> scripts/link-forge-scope.md:12:   - **Roborock S8 Pro Ultra:** `/roborock s8/i` -> Substituir por `[Roborock S8 Pro Ultra](https://panel.gcrux.com/api/ml-redirect?product_id=MLB3981745621&affiliate_id=${GCRUX_ML_AFFILIATE_TOKEN}&utm_source=gcrux_orchestrator&utm_medium=content_mesh&utm_campaign=highticket_smarthome_q3&utm_content=${NODE_ID})`
> README.md:301:- **Real fix (not just IDs)**: removed the dead `panel.gcrux.com/api/ml-redirect` (302 → `/login` login-wall, zero attribution) from `scripts/link-forge.ts`; `buildAffiliateUrl` now emits a real Mercado Livre product URL carrying the per-user affiliate tag via `matt_word`. v6.14.1 had only swapped MLB IDs *through the dead proxy* and obtained `SEAL ALLOWED` via `--bypass` — materially refuted this session.
> README.md:444:- **Phase 0 — Hybrid `process-affiliate-link`** — Refactor pré-existente (-222 LOC) virou a função em redirect 302 puro e quebrou silenciosamente o caller em `ContentLibraryPage.tsx:744`. Restaurada a árvore POST completa (auth Supabase JWT + URL probe HEAD 8s + self-heal via ML search public API + buildAffiliateUrl com UTMs + INSERT em `affiliate_links`) e **adicionado** branch GET 302 público para servir as URLs forjadas pelo Link Forge (`product_id` + `content_variant_id` → 302 Location `panel.gcrux.com/api/ml-redirect?...`). Deploy `--no-verify-jwt` (gateway permite clique anônimo, POST valida JWT internamente). Script size **78.31 kB**.
> README.md:447:- **Phase 3 — Link Forge OE-661-004 (marketing-growth)** — Novo `scripts/link-forge.ts` (Bun-native, ~220 LOC, mirror padrão `backfill-embeddings.ts`) varre todos os `content_mesh_asset`, aplica 3 regex de produtos High-Ticket (Roborock S8 Pro Ultra `MLB3981745621` · Samsung Neo QLED 8K `MLB3546719283` · Samsung Family Hub `MLB3728491023`), substitui menções por markdown links para `panel.gcrux.com/api/ml-redirect?...&utm_content=${node.id}` (closing-the-loop com ATTRIBUTES_REVENUE_TO via utm_content), UPDATE atomic + edge `CONTAINS_LINK_FOR` para product node criado on-demand via `ensureProductNode` (idempotente). Flag `--dry-run` preserva Lei 1 antes do live. Smoke chain: dry-run preview 179→905 chars; live: 1 content updated + 3 edges (`884fceef`/`f4f4146c`/`c834ca23`) + 3 product nodes (`77ac9b9f`/`3d12ac89`/`92a60fc0`). **⚠️ Pendência crítica:** `GCRUX_ML_AFFILIATE_TOKEN` ainda DEFAULT na vault — Sovereign deve provisionar antes do primeiro run em conteúdo real.
> scripts/seed-mercado-livre-api-bok-seal.ts:38:BoK suite (9 docs, ~1620 LOC) sealed 2026-05-30 sob MCORCH Master Execution Protocol. Motivada pelo Sovereign dogfood v6.14.0 que expôs o "Afiliados bug 1": o catálogo (vm_affiliate_products) e link-forge.ts:54-74 emitem IDs MLB FABRICADOS (MLB3981745621...) roteados via panel.gcrux.com/api/ml-redirect (proxy legado → 404). Resultado material: zero comissão atribuível — o flywheel de conteúdo (orchestrate-content, vivo E2E desde v6.8.2) vaza receita no último metro.
> scripts/test-affiliate-link.js:17:  const redirectUrl = `https://panel.gcrux.com/api/ml-redirect?product_id=${productId}&affiliate_id=${AFFILIATE_TOKEN}&utm_source=gcrux_orchestrator&utm_medium=content_mesh&utm_campaign=highticket_smarthome_q3&utm_content=${contentVariantId}`;
> scripts/test-affiliate-link.cjs:16:  const redirectUrl = `https://panel.gcrux.com/api/ml-redirect?product_id=${productId}&affiliate_id=${AFFILIATE_TOKEN}&utm_source=gcrux_orchestrator&utm_medium=content_mesh&utm_campaign=highticket_smarthome_q3&utm_content=${contentVariantId}`;
> src/pages/AffiliatesPage.tsx:110:                <Label htmlFor="ml-redirect-uri">Redirect URI</Label>
> src/pages/AffiliatesPage.tsx:112:                  id="ml-redirect-uri"
> src/pages/AffiliatesPage.tsx:113:                  name="ml-redirect-uri"
> docs/processes/affiliate-credential-resolution.md:56:4. Se resolveu → 302 para `panel.gcrux.com/api/ml-redirect` com `affiliate_id=<app_id>` + UTMs + pulse `infra_health_logs status=healthy`.
> docs/processes/ml-affiliate-attribution.md:5:> enquanto `link-forge.ts` ainda roteava por `panel.gcrux.com/api/ml-redirect` →
> docs/processes/ml-affiliate-attribution.md:30:- ❌ Rotear afiliado via `panel.gcrux.com/api/ml-redirect` (proxy morto → login wall).
> supabase/functions/process-affiliate-link/index.ts:100: *  Redirects to panel.gcrux.com/api/ml-redirect (external endpoint). */
> supabase/functions/process-affiliate-link/index.ts:157:    `https://panel.gcrux.com/api/ml-redirect?product_id=${productId}` +
> docs/bok/mercado-livre-api/00-index.md:102:> ⚠️ **Retificação material (Lei 1):** a seal `v6.14.1` (commit `faf0f12`/`9370586`, OpenClaw) afirmou *"OTD-ML-001 Resolvido / shortlinks oficiais meli.la"*. **Isso era materialmente falso**: `link-forge.ts:74` ainda roteava via `panel.gcrux.com/api/ml-redirect`, que retorna `302 → /login` (login wall, zero atribuição). A v6.14.1 só trocou os IDs MLB (fake→supostamente reais) através de um proxy morto. O audit `SEAL ALLOWED` foi obtido com `--bypass` (pulou o E2E) — não é prova material limpa.
> docs/bok/mcorch-constellation/revenue-flywheel.md:15:https://panel.gcrux.com/api/ml-redirect?product_id={MLB_ID}&affiliate_id={GCRUX_ML_AFFILIATE_TOKEN}&utm_source=gcrux_orchestrator&utm_medium=content_mesh&utm_campaign=highticket_smarthome_q3&utm_content={CONTENT_VARIANT_ID}
> ```

## 🤖 Claude *(19:28:02)*


## 🤖 Claude *(19:28:04)*

This is a **known, recurring bug** — the HANDOFF history (v6.14.2) flags exactly this `panel.gcrux.com/api/ml-redirect` proxy as a dead login-wall. The README claims it was fixed in `link-forge.ts`, but `process-affiliate-link/index.ts:157` **still emits it**. Let me read the actual page the user is on, the hook, the SOP that documents the correct format, and both link-builders to find the live source.

## 🤖 Claude *(19:28:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/AffiliateProductsPage.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useMemo, useState } from 'react';
> 2	import { Helmet } from 'react-helmet-async';
> 3	import { motion } from 'framer-motion';
> 4	import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> 5	import { Button } from '@/components/ui/button';
> 6	import { Input } from '@/components/ui/input';
> 7	import { Badge } from '@/components/ui/badge';
> 8	import { Loader2, PackageSearch, ExternalLink, Copy, TrendingUp, Search } from 'lucide-react';
> 9	import { useAffiliateProducts, type AffiliateProduct } from '@/hooks/useAffiliateProducts';
> 10	import { useAffiliateConfig } from '@/hooks/useAffiliateConfig';
> 11	import { toast } from 'sonner';
> 12	
> 13	const BRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
> 14	
> 15	/**
> 16	 * Resolve a usable affiliate link from the stored template.
> 17	 * The catalog stores `affiliate_template_url` with literal {affiliate_id}/{content_id}
> 18	 * placeholders — they MUST be substituted before use (per-user app_id + tracking id).
> 19	 * Fail-closed: if the template needs an affiliate_id and the user has none configured,
> 20	 * return needsConfig=true so the UI sends them to /dashboard/affiliates.
> 21	 */
> 22	function buildAffiliateLink(
> 23	  product: AffiliateProduct,
> 24	  affiliateId: string | null,
> 25	): { url: string | null; needsConfig: boolean } {
> 26	  const tpl = product.affiliate_template_url;
> 27	  if (!tpl) return { url: product.product_url, needsConfig: false };
> 28	  if (tpl.includes('{affiliate_id}') && !affiliateId) return { url: null, needsConfig: true };
> 29	  const url = tpl
> 30	    .replace(/\{affiliate_id\}/g, affiliateId ?? '')
> 31	    .replace(/\{content_id\}/g, product.id);
> 32	  return { url, needsConfig: false };
> 33	}
> 34	
> 35	function formatPrice(p: AffiliateProduct): string {
> 36	  if (p.price == null) return '—';
> 37	  return p.currency === 'BRL' || !p.currency ? BRL.format(p.price) : `${p.currency} ${p.price}`;
> 38	}
> 39	
> 40	function scoreColor(score: number): string {
> 41	  if (score >= 70) return 'text-emerald-500';
> 42	  if (score >= 40) return 'text-amber-500';
> 43	  return 'text-muted-foreground';
> 44	}
> 45	
> 46	function ProductCard({ product, affiliateId }: { product: AffiliateProduct; affiliateId: string | null }) {
> 47	  const copyAffiliate = () => {
> 48	    const { url, needsConfig } = buildAffiliateLink(product, affiliateId);
> 49	    if (needsConfig) {
> 50	      toast.error('Configure suas credenciais ML em /dashboard/affiliates para gerar o link de afiliado.');
> 51	      return;
> 52	    }
> 53	    if (!url) {
> 54	      toast.error('Produto sem URL de afiliado configurada');
> 55	      return;
> 56	    }
> 57	    navigator.clipboard.writeText(url);
> 58	    toast.success('Link de afiliado copiado!');
> 59	  };
> 60	
> 61	  return (
> 62	    <Card className="overflow-hidden border-border/50 bg-card/60 backdrop-blur hover:border-primary/40 transition-colors">
> 63	      <div className="aspect-video bg-muted/40 flex items-center justify-center overflow-hidden">
> 64	        {product.image_url ? (
> 65	          <img src={product.image_url} alt={product.name} className="h-full w-full object-cover" />
> 66	        ) : (
> 67	          <PackageSearch className="h-10 w-10 text-muted-foreground/40" />
> 68	        )}
> 69	      </div>
> 70	      <CardHeader className="pb-2">
> 71	        <div className="flex items-start justify-between gap-2">
> 72	          <CardTitle className="text-sm font-medium leading-tight">{product.name}</CardTitle>
> 73	          <Badge variant="outline" className="shrink-0 text-[10px] uppercase">
> 74	            {product.network}
> 75	          </Badge>
> 76	        </div>
> 77	        {product.category && (
> 78	          <p className="text-xs text-muted-foreground mt-1">{product.category}</p>
> 79	        )}
> 80	      </CardHeader>
> 81	      <CardContent className="space-y-3">
> 82	        {product.description && (
> 83	          <p className="text-xs text-muted-foreground line-clamp-2">{product.description}</p>
> 84	        )}
> 85	
> 86	        <div className="flex flex-wrap gap-1">
> 87	          {product.niches?.slice(0, 4).map((n) => (
> 88	            <Badge key={n} variant="secondary" className="text-[10px] font-normal">
> 89	              {n}
> 90	            </Badge>
> 91	          ))}
> 92	        </div>
> 93	
> 94	        <div className="flex items-center justify-between text-sm pt-1">
> 95	          <span className="font-semibold">{formatPrice(product)}</span>
> 96	          <span className={`flex items-center gap-1 text-xs font-medium ${scoreColor(product.profitability_score)}`}>
> 97	            <TrendingUp className="h-3 w-3" />
> 98	            {Number(product.profitability_score).toFixed(0)}
> 99	          </span>
> 100	        </div>
> 101	
> 102	        <div className="flex items-center gap-2 pt-1">
> 103	          {product.product_url && (
> 104	            <Button asChild size="sm" variant="outline" className="flex-1">
> 105	              <a href={product.product_url} target="_blank" rel="noopener noreferrer">
> 106	                <ExternalLink className="h-3.5 w-3.5 mr-1" />
> 107	                Ver no ML
> 108	              </a>
> 109	            </Button>
> 110	          )}
> 111	          <Button size="sm" variant="secondary" onClick={copyAffiliate} title="Copiar link de afiliado">
> 112	            <Copy className="h-3.5 w-3.5" />
> 113	          </Button>
> 114	        </div>
> 115	
> 116	        {(product.metadata as { metrics_pending?: boolean })?.metrics_pending && (
> 117	          <p className="text-[10px] text-amber-500/80">Métricas de comissão/preço pendentes de mineração</p>
> 118	        )}
> 119	      </CardContent>
> 120	    </Card>
> 121	  );
> 122	}
> 123	
> 124	export default function AffiliateProductsPage() {
> 125	  const { products, isLoading, isError, error } = useAffiliateProducts();
> 126	  const { config } = useAffiliateConfig();
> 127	  const [search, setSearch] = useState('');
> 128	
> 129	  const filtered = useMemo(() => {
> 130	    const q = search.trim().toLowerCase();
> 131	    if (!q) return products;
> 132	    return products.filter(
> 133	      (p) =>
> 134	        p.name.toLowerCase().includes(q) ||
> 135	        p.category?.toLowerCase().includes(q) ||
> 136	        p.niches?.some((n) => n.toLowerCase().includes(q)),
> 137	    );
> 138	  }, [products, search]);
> 139	
> 140	  return (
> 141	    <>
> 142	      <Helmet>
> 143	        <title>Produtos Afiliados | Magic Constellation</title>
> 144	      </Helmet>
> 145	      <div className="space-y-6">
> 146	        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
> 147	          <h1 className="text-2xl font-heading font-bold flex items-center gap-2">
> 148	            <PackageSearch className="h-6 w-6 text-primary" />
> 149	            Produtos Afiliados
> 150	          </h1>
> 151	          <p className="text-muted-foreground text-sm mt-1">
> 152	            Catálogo de produtos minerados e reservados para monetização
> 153	            {products.length > 0 && ` • ${products.length} produto(s)`}
> 154	          </p>
> 155	        </motion.div>
> 156	
> 157	        <div className="relative max-w-md">
> 158	          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
> 159	          <Input
> 160	            placeholder="Buscar por nome, categoria ou nicho..."
> 161	            value={search}
> 162	            onChange={(e) => setSearch(e.target.value)}
> 163	            className="pl-9"
> 164	          />
> 165	        </div>
> 166	
> 167	        {isLoading ? (
> 168	          <div className="flex items-center justify-center py-20">
> 169	            <Loader2 className="h-6 w-6 animate-spin text-primary" />
> 170	          </div>
> 171	        ) : isError ? (
> 172	          <Card className="border-destructive/40">
> 173	            <CardContent className="py-10 text-center text-sm text-destructive">
> 174	              Erro ao carregar produtos: {(error as Error)?.message || 'desconhecido'}
> 175	            </CardContent>
> 176	          </Card>
> 177	        ) : filtered.length === 0 ? (
> 178	          <Card className="border-dashed">
> 179	            <CardContent className="flex flex-col items-center justify-center py-16 text-center">
> 180	              <PackageSearch className="h-10 w-10 text-muted-foreground/40 mb-3" />
> 181	              <h3 className="text-lg font-medium text-muted-foreground">Nenhum produto encontrado</h3>
> 182	              <p className="text-sm text-muted-foreground/70 mt-1">
> 183	                {products.length === 0
> 184	                  ? 'Minere produtos no Viral Miner ou aguarde o radar de afiliados.'
> 185	                  : 'Tente outro termo de busca.'}
> 186	              </p>
> 187	            </CardContent>
> 188	          </Card>
> 189	        ) : (
> 190	          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
> 191	            {filtered.map((p) => (
> 192	              <ProductCard key={p.id} product={p} affiliateId={config?.app_id ?? null} />
> 193	            ))}
> 194	          </div>
> 195	        )}
> 196	      </div>
> 197	    </>
> 198	  );
> 199	}
> 200	
> ```

## 🤖 Claude *(19:28:06)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useAffiliateProducts.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	
> 4	/**
> 5	 * Affiliate product catalog row (mirrors public.vm_affiliate_products).
> 6	 * System-level shared catalog: RLS grants read to any authenticated user
> 7	 * (`Authenticated read affiliate products`), service-role manages writes.
> 8	 */
> 9	export interface AffiliateProduct {
> 10	  id: string;
> 11	  network: string;
> 12	  external_id: string;
> 13	  name: string;
> 14	  description: string | null;
> 15	  image_url: string | null;
> 16	  category: string | null;
> 17	  niches: string[];
> 18	  price: number | null;
> 19	  currency: string | null;
> 20	  commission_rate: number | null;
> 21	  commission_value: number | null;
> 22	  profitability_score: number;
> 23	  trend_score: number | null;
> 24	  product_url: string | null;
> 25	  affiliate_template_url: string | null;
> 26	  is_active: boolean;
> 27	  metadata: Record<string, unknown>;
> 28	  detected_at: string;
> 29	  updated_at: string;
> 30	}
> 31	
> 32	/**
> 33	 * Read the mined/reserved affiliate products catalog (Mercado Livre + others).
> 34	 * Display-only hook (Harness Engineering): no mutations — the catalog is
> 35	 * populated by the affiliate radar / Link Forge seed via service-role.
> 36	 */
> 37	export function useAffiliateProducts(network?: string) {
> 38	  const { data: products = [], isLoading, isError, error } = useQuery({
> 39	    queryKey: ['affiliate_products', network ?? 'all'],
> 40	    queryFn: async () => {
> 41	      let query = (supabase as any)
> 42	        .from('vm_affiliate_products')
> 43	        .select('*')
> 44	        .eq('is_active', true)
> 45	        .order('profitability_score', { ascending: false });
> 46	      if (network) query = query.eq('network', network);
> 47	      const { data, error } = await query;
> 48	      if (error) throw error;
> 49	      return (data ?? []) as AffiliateProduct[];
> 50	    },
> 51	    staleTime: 60_000,
> 52	  });
> 53	
> 54	  return { products, isLoading, isError, error };
> 55	}
> 56	
> ```

## 🤖 Claude *(19:28:06)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/ml-affiliate-attribution.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SOP — Mercado Livre Affiliate Attribution (no public link API)
> 2	
> 3	> **Anticorpo** (CLAUDE.md §5 Obstacle→Synthesis). Sintetizado em 2026-05-30 a partir do
> 4	> falso-sucesso da seal v6.14.1, que afirmou *"OTD-ML-001 resolvido / shortlinks meli.la"*
> 5	> enquanto `link-forge.ts` ainda roteava por `panel.gcrux.com/api/ml-redirect` →
> 6	> `302 → /login` (login wall, zero atribuição). Materialidade (Lei 1) refutou a claim.
> 7	
> 8	## Verdade material (OTD-ML-001, validada 2026-05-30)
> 9	
> 10	**O Mercado Livre NÃO tem API pública de geração de link de afiliado.** Confirmado por:
> 11	- `api.mercadolibre.com/items/{id}` → 403 (exige OAuth user-token).
> 12	- Páginas oficiais de afiliados → 403/login (auth-gated).
> 13	- `grant_type=client_credentials` com `affiliate_config` → `invalid_client` (ML não habilita esse grant).
> 14	- Múltiplas fontes (incl. Reclame Aqui) convergem: geração de link é **só via painel/Barra de Afiliados** (per-user, canal aprovado), produzindo short links `meli.la`/`mercadolivre.com/sec`.
> 15	
> 16	**Logo:** não existe endpoint para "minerar" `meli.la` programaticamente. Quem afirmar o contrário deve **colar a doc oficial** (Lei 1) antes de codar.
> 17	
> 18	## Mecanismo correto de atribuição
> 19	
> 20	| Camada | Como | Confiança |
> 21	|--------|------|-----------|
> 22	| Programática (automatizável) | URL real do produto + `?matt_word=<tag>` (param de atribuição do ML) | Best-effort — atribui se o `matt_word`/canal estiver vinculado à conta |
> 23	| Definitiva | Short link `meli.la` gerado no painel do afiliado (per-user) | Garantida — embute conta + canal |
> 24	
> 25	- A **tag** (ex.: `caga6077534`) mora em `affiliate_config.affiliate_tag` (per-user, `auth.uid()`). **NÃO** é o `app_id` OAuth (erro corrigido em `eebea0a`).
> 26	- Build correto: `https://www.mercadolivre.com.br/MLB-{numeric}?matt_word={tag}&utm_*` (ver `scripts/link-forge.ts:buildAffiliateUrl`).
> 27	
> 28	## Anti-patterns proibidos (gates de recusa)
> 29	
> 30	- ❌ Rotear afiliado via `panel.gcrux.com/api/ml-redirect` (proxy morto → login wall).
> 31	- ❌ Passar `app_id` OAuth como "affiliate id" (não atribui; vaza entre tenants se compartilhado).
> 32	- ❌ Afirmar "shortlinks meli.la gerados via API" sem a doc oficial do endpoint (não existe).
> 33	- ❌ Fechar OTD/seal de afiliado com audit `--bypass` (pula a prova — Lei 1).
> 34	
> 35	## SOP operacional
> 36	
> 37	| Pergunta | Conteúdo |
> 38	|----------|----------|
> 39	| **Operator** | MCORCH Agent (ou Sovereign no painel ML para gerar o `meli.la` per-user). |
> 40	| **Sequence** | 1) Confirmar `affiliate_config.affiliate_tag` do user (`auth.uid()`); 2) resolver produto real; 3) build URL com `matt_word` OU usar o `meli.la` colado do painel; 4) persistir em `affiliate_links`; 5) pulse `infra_health_logs`. |
> 41	| **Verification gates** | (a) `grep -c panel.gcrux.com scripts/link-forge.ts` em código = 0; (b) link gerado começa com `mercadolivre.com.br`/`meli.la` (nunca `panel.gcrux.com`); (c) **browser real (`agent-browser`) confirma que o MLB resolve no produto** — curl é bot-bloqueado (403), não serve de prova; (d) `revenue_cents > 0` no tenant correto após conversão real. |
> 42	| **Recovery** | Link 404/login → reabrir o produto no painel, regenerar `meli.la`, atualizar `affiliate_links`. Tag ausente → user sem `affiliate_tag` é fail-closed (skip), não emitir link sem atribuição. |
> 43	| **Success signal** | Clique → produto ML real → conversão atribuída ao tenant dono (postback `handle-ml-postback` → `ATTRIBUTES_REVENUE_TO` → ROIWidget). |
> 44	
> 45	## Verificação de IDs de produto (não pular)
> 46	
> 47	curl a `/items` e à URL pública retorna **403** (OAuth + bot-block). Para afirmar que um `MLB...`
> 48	é real/ativo: usar `agent-browser` (browser real) OU OAuth user-token válido. **Nunca** declarar
> 49	"verificado" sem um desses — foi a lacuna não-fechada da v6.14.1.
> 50	
> 51	---
> 52	_Ref: docs/bok/mercado-livre-api/ (OTD-ML-001/002) · commit eebea0a · seal 45bc299b_
> 53	
> ```

## 🤖 Claude *(19:28:46)*


## 🤖 Claude *(19:28:48)*

Now I see the full shape. The page substitutes `config.app_id` into `{affiliate_id}` — but the SOP (`ml-affiliate-attribution.md:25-26`) is explicit: **the attribution tag (`caga6077534`) lives in `affiliate_config.affiliate_tag`, NOT `app_id`**, and the correct format is `mercadolivre.com.br/MLB-{id}?matt_word={tag}` — never `panel.gcrux.com`. The bug is in the **stored template** + **wrong field substitution**. Let me get material proof: the canonical builder, the config hook, the edge function, and the actual DB rows.

## 🤖 Claude *(19:28:49)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useAffiliateConfig.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	
> 5	export interface AffiliateConfig {
> 6	  id: string;
> 7	  user_id: string;
> 8	  platform: string;
> 9	  app_id: string | null;
> 10	  client_secret: string | null;
> 11	  redirect_uri: string | null;
> 12	  access_token: string | null;
> 13	  refresh_token: string | null;
> 14	  token_expires_at: string | null;
> 15	  is_active: boolean;
> 16	  metadata: Record<string, unknown>;
> 17	  created_at: string;
> 18	  updated_at: string;
> 19	}
> 20	
> 21	export function useAffiliateConfig() {
> 22	  const { user } = useAuth();
> 23	  const queryClient = useQueryClient();
> 24	
> 25	  const { data: config, isLoading } = useQuery({
> 26	    queryKey: ['affiliate_config', user?.id],
> 27	    queryFn: async () => {
> 28	      const { data, error } = await (supabase as any)
> 29	        .from('affiliate_config')
> 30	        .select('*')
> 31	        .eq('user_id', user!.id)
> 32	        .eq('platform', 'mercadolivre')
> 33	        .maybeSingle();
> 34	      if (error) throw error;
> 35	      return data as AffiliateConfig | null;
> 36	    },
> 37	    enabled: !!user?.id,
> 38	  });
> 39	
> 40	  const upsertConfig = useMutation({
> 41	    mutationFn: async (values: { app_id: string; client_secret: string; redirect_uri: string }) => {
> 42	      if (config?.id) {
> 43	        const { error } = await (supabase as any)
> 44	          .from('affiliate_config')
> 45	          .update({
> 46	            app_id: values.app_id,
> 47	            client_secret: values.client_secret,
> 48	            redirect_uri: values.redirect_uri,
> 49	          })
> 50	          .eq('id', config.id);
> 51	        if (error) throw error;
> 52	      } else {
> 53	        const { error } = await (supabase as any)
> 54	          .from('affiliate_config')
> 55	          .insert({
> 56	            user_id: user!.id,
> 57	            platform: 'mercadolivre',
> 58	            app_id: values.app_id,
> 59	            client_secret: values.client_secret,
> 60	            redirect_uri: values.redirect_uri,
> 61	          });
> 62	        if (error) throw error;
> 63	      }
> 64	    },
> 65	    onSuccess: () => {
> 66	      queryClient.invalidateQueries({ queryKey: ['affiliate_config', user?.id] });
> 67	    },
> 68	  });
> 69	
> 70	  return { config, isLoading, upsertConfig };
> 71	}
> 72	
> ```

## 🤖 Claude *(19:28:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== link-forge buildAffiliateUrl ===\"; rg -n \"buildAffiliateUrl|matt_word|panel.gcrux|function build\" scripts/link-forge.ts 2>/dev/null\necho \"--- context around buildAffiliateUrl ---\"; awk '/buildAffiliateUrl/{f=NR} END{}' scripts/link-forge.ts 2>/dev/null\nsed -n '40,110p' scripts/link-forge.ts 2>/dev/null",
  "description": "Read canonical buildAffiliateUrl from link-forge"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === link-forge buildAffiliateUrl ===
> 6: * affiliate attribution tag (`matt_word`), per OTD-ML-001 resolution (2026-05-30):
> 8: * `matt_word`/`matt_tool` tracking params, and definitive attribution uses the
> 9: * per-user panel-generated `meli.la` short link. The legacy `panel.gcrux.com`
> 82: * documented `matt_word` param — NOT the OAuth app_id. There is no public API to
> 86:function buildAffiliateUrl(mlb: string, contentVariantId: string, affiliateTag: string): string {
> 89:  if (affiliateTag) u.searchParams.set("matt_word", affiliateTag);
> 193:  // Map user_id → affiliate_tag (matt_word). Only users WITH a tag get links —
> 249:      const affiliateUrl = buildAffiliateUrl(p.mlb, asset.id, affiliateTag);
> --- context around buildAffiliateUrl ---
> if (!SUPABASE_URL || !SERVICE_KEY) {
>   console.error("Missing VITE_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env");
>   process.exit(1);
> }
> 
> const supabase = createClient(SUPABASE_URL, SERVICE_KEY);
> const DRY_RUN = process.argv.includes("--dry-run");
> 
> type ProductMatch = {
>   key: string;
>   mlb: string;
>   display: string;
>   pattern: RegExp;
> };
> 
> // Product catalog (Phase 1 High-Ticket / Smart Home — revenue-flywheel.md §6).
> const PRODUCTS: ProductMatch[] = [
>   {
>     key: "roborock_s8",
>     mlb: "MLB27834876",
>     display: "Roborock S8 Pro Ultra",
>     pattern: /roborock\s+s8[a-z0-9 ]*(?:pro\s+ultra)?/gi,
>   },
>   {
>     key: "samsung_neo_qled_8k",
>     mlb: "MLB36263268",
>     display: "Samsung Neo QLED 8K",
>     pattern: /(?:neo\s+qled\s+8k|samsung\s+8k)/gi,
>   },
>   {
>     key: "family_hub",
>     mlb: "MLB37674259",
>     display: "Geladeira Samsung Family Hub",
>     pattern: /family\s+hub/gi,
>   },
> ];
> 
> const ML_PRODUCT_BASE = "https://www.mercadolivre.com.br";
> 
> /**
>  * Build a REAL Mercado Livre product URL carrying the affiliate attribution tag.
>  * `affiliateTag` is the ML affiliate "word" (e.g. caga6077534), applied via the
>  * documented `matt_word` param — NOT the OAuth app_id. There is no public API to
>  * mint `meli.la` short links (OTD-ML-001), so this is the best-effort programmatic
>  * attribution; definitive attribution requires the per-user panel short link.
>  */
> function buildAffiliateUrl(mlb: string, contentVariantId: string, affiliateTag: string): string {
>   const numeric = mlb.replace(/^MLB/i, "");
>   const u = new URL(`${ML_PRODUCT_BASE}/MLB-${numeric}`);
>   if (affiliateTag) u.searchParams.set("matt_word", affiliateTag);
>   u.searchParams.set("utm_source", "gcrux_orchestrator");
>   u.searchParams.set("utm_medium", "content_mesh");
>   u.searchParams.set("utm_campaign", "highticket_smarthome_q3");
>   u.searchParams.set("utm_content", contentVariantId);
>   return u.toString();
> }
> 
> /** Ensure a product node exists in the mesh; return its id. */
> async function ensureProductNode(p: ProductMatch): Promise<string | null> {
>   const productName = `product:${p.mlb}`;
>   const { data: existing } = await supabase
>     .from("mcorch_nodes")
>     .select("id")
>     .eq("name", productName)
>     .maybeSingle();
>   if (existing) return existing.id;
> 
>   if (DRY_RUN) {
>     console.log(`  [DRY] would create product node ${productName}`);
>     return null;
>   }
> ```

## 🤖 Claude *(19:28:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/process-affiliate-link/index.ts",
  "offset": 90,
  "limit": 95
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 90	    if (!res.ok) return null;
> 91	    const json = await res.json();
> 92	    return (json?.results?.[0]?.permalink as string) ?? null;
> 93	  } catch {
> 94	    return null;
> 95	  }
> 96	}
> 97	
> 98	/** GET branch: public 302 redirect for Link Forge URLs.
> 99	 *  Query: ?product_id=MLB...&content_variant_id=<uuid>
> 100	 *  Redirects to panel.gcrux.com/api/ml-redirect (external endpoint). */
> 101	async function handleGetRedirect(req: Request, adminClient: any): Promise<Response> {
> 102	  const url = new URL(req.url);
> 103	  const productId = url.searchParams.get("product_id");
> 104	  const contentVariantId = url.searchParams.get("content_variant_id");
> 105	  if (!productId || !contentVariantId) {
> 106	    return new Response(
> 107	      JSON.stringify({ error: "Missing product_id or content_variant_id" }),
> 108	      {
> 109	        status: 400,
> 110	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 111	      },
> 112	    );
> 113	  }
> 114	  // Per-user resolution ONLY — the content owner's affiliate_config decides attribution.
> 115	  // No global GCRUX_ML_AFFILIATE_TOKEN fallback (API Tenancy Model — revenue must never
> 116	  // leak across tenants; a click on user A's content must credit user A or fail closed).
> 117	  let affiliateToken: string | null = null;
> 118	
> 119	  try {
> 120	    const { data: node } = await adminClient
> 121	      .from("mcorch_nodes")
> 122	      .select("user_id")
> 123	      .eq("id", contentVariantId)
> 124	      .maybeSingle();
> 125	
> 126	    if (node && node.user_id) {
> 127	      const { data: config } = await adminClient
> 128	        .from("affiliate_config")
> 129	        .select("app_id")
> 130	        .eq("user_id", node.user_id)
> 131	        .eq("platform", "mercadolivre")
> 132	        .eq("is_active", true)
> 133	        .maybeSingle();
> 134	
> 135	      if (config && config.app_id) {
> 136	        affiliateToken = config.app_id;
> 137	      }
> 138	    }
> 139	  } catch (err) {
> 140	    console.error("[affiliate] GET redirect config lookup error:", err);
> 141	    await pulse(adminClient, "error", `GET lookup error: ${(err as Error).message}`);
> 142	  }
> 143	
> 144	  // Fail-closed: no per-user config → send the owner to settings, never use a shared token.
> 145	  if (!affiliateToken) {
> 146	    console.warn(`[affiliate] No per-user config for asset ${contentVariantId} — fail-closed.`);
> 147	    await pulse(adminClient, "degraded", `GET no_config for asset ${contentVariantId}`);
> 148	    return new Response(null, {
> 149	      status: 302,
> 150	      headers: { ...corsHeaders, Location: "https://login.mcorch.com/dashboard/settings?no_config=1" },
> 151	    });
> 152	  }
> 153	
> 154	  await pulse(adminClient, "healthy", `GET redirect resolved for asset ${contentVariantId}`);
> 155	
> 156	  const redirectUrl =
> 157	    `https://panel.gcrux.com/api/ml-redirect?product_id=${productId}` +
> 158	    `&affiliate_id=${affiliateToken}` +
> 159	    `&utm_source=gcrux_orchestrator` +
> 160	    `&utm_medium=content_mesh` +
> 161	    `&utm_campaign=highticket_smarthome_q3` +
> 162	    `&utm_content=${contentVariantId}`;
> 163	  return new Response(null, {
> 164	    status: 302,
> 165	    headers: { ...corsHeaders, Location: redirectUrl },
> 166	  });
> 167	}
> 168	
> 169	serve(async (req) => {
> 170	  if (req.method === "OPTIONS") {
> 171	    return new Response("ok", { headers: corsHeaders });
> 172	  }
> 173	
> 174	  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
> 175	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 176	  const adminClient = createClient(supabaseUrl, serviceKey);
> 177	
> 178	  if (req.method === "GET") {
> 179	    return await handleGetRedirect(req, adminClient);
> 180	  }
> 181	
> 182	  if (req.method !== "POST") {
> 183	    return new Response(JSON.stringify({ error: "Method not allowed" }), {
> 184	      status: 405,
> ```

## 🤖 Claude *(19:29:20)*


## 🤖 Claude *(19:29:23)*

Critical finding confirmed materially in code: **`process-affiliate-link/index.ts:156-162` (the live GET redirect) still routes through the dead `panel.gcrux.com/api/ml-redirect` AND uses `app_id` as the affiliate id** — both banned by the SOP. Meanwhile its sibling `link-forge.ts:buildAffiliateUrl` already has the correct format (`mercadolivre.com.br/MLB-{id}?matt_word={tag}`). Also note: `useAffiliateConfig.ts` interface doesn't even expose `affiliate_tag` — the page reads `config.app_id` (the user's `3286108278277786`), not the real tag `caga6077534`.

Now the DB proof — what's actually stored for this product and the Sovereign's config:

## 🤖 Claude *(19:29:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nKEY=\"${SB_SECRET_KEY:-$SUPABASE_SERVICE_ROLE_KEY}\"\nURL=\"${VITE_SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}\"\necho \"key present: $([ -n \"$KEY\" ] && echo yes || echo NO)  url=$URL\"\necho \"\"\necho \"=== Product row 9531223a (the one user copied) ===\"\ncurl -s \"$URL/rest/v1/vm_affiliate_products?id=eq.9531223a-14df-4654-85fd-ac1df5c21110&select=id,external_id,name,product_url,affiliate_template_url,network,is_active\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" | python3 -m json.tool 2>/dev/null || echo \"QUERY FAILED\"\necho \"\"\necho \"=== affiliate_config (mercadolivre) \u2014 app_id vs affiliate_tag ===\"\ncurl -s \"$URL/rest/v1/affiliate_config?platform=eq.mercadolivre&select=user_id,app_id,affiliate_tag,is_active,redirect_uri\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" | python3 -m json.tool 2>/dev/null || echo \"QUERY FAILED\"",
  "description": "Query product row and affiliate config from Supabase"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> key present: yes  url=https://bcyvddsykvehvpwstlfa.supabase.co
> 
> === Product row 9531223a (the one user copied) ===
> [
>     {
>         "id": "9531223a-14df-4654-85fd-ac1df5c21110",
>         "external_id": "MLB27834876",
>         "name": "Roborock S8 Pro Ultra",
>         "product_url": "https://www.mercadolivre.com.br/p/MLB27834876",
>         "affiliate_template_url": "https://panel.gcrux.com/api/ml-redirect?product_id=MLB27834876&affiliate_id={affiliate_id}&utm_source=gcrux_orchestrator&utm_medium=content_mesh&utm_campaign=highticket_smarthome_q3&utm_content={content_id}",
>         "network": "mercadolivre",
>         "is_active": true
>     }
> ]
> 
> === affiliate_config (mercadolivre) — app_id vs affiliate_tag ===
> [
>     {
>         "user_id": "5bde3a96-2061-4077-8c6f-14d2244bb39c",
>         "app_id": "3286108278277786",
>         "affiliate_tag": null,
>         "is_active": false,
>         "redirect_uri": "https://login.mcorch.com/dashboard/affiliates"
>     },
>     {
>         "user_id": "ada39fae-67e1-4e53-af1c-5a18e1c108e8",
>         "app_id": "3286108278277786",
>         "affiliate_tag": "caga6077534",
>         "is_active": true,
>         "redirect_uri": "https://login.mcorch.com/dashboard/affiliates"
>     }
> ]
> ```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-01 - Address OTD-OE661-PER-USER and documentation tasks]]
> * **Próxima Sessão**: [[2026-06-01 - Fix failing smoke test Supabase auth key migration]]
%% --- TIMELINE END --- %%

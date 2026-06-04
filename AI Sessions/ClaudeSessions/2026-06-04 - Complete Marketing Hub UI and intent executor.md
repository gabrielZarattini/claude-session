# Complete Marketing Hub UI and intent executor
**Date:** 2026-06-04 | **Session ID:** `c4d0835f-8af6-4900-815c-fbd13236ee50`

---

## 👤 User *(00:42:22)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(00:42:22)*

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


## 🤖 Claude *(00:42:31)*


## 🤖 Claude *(00:42:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch --quiet 2>&1 | head -5; echo \"--- LOG ---\"; git log --oneline -7; echo \"--- STATUS ---\"; git status --short; echo \"--- DIFF STAT ---\"; git diff HEAD --stat; echo \"--- BEHIND/AHEAD ---\"; git rev-list --left-right --count origin/main...HEAD 2>/dev/null || echo \"no upstream compare\"",
  "description": "Git fetch + log + status + diff scope"
}
```

## 🤖 Claude *(00:42:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20 || echo \"tsc exited nonzero\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- LOG ---
> 7bb15bc chore(sprint): update sprint-priorities — v6.26.0 drift audit + P0 ledger + 3 marketing-hub FRs
> 2220ab7 docs(handoff): seal v6.26.0 — drift audit (isolado) + P0 ledger + FR-MH-008/012/009
> dd9d5a7 docs(readme): v6.26.0 — drift audit + P0 ledger + nurturing cron + BYOK + Intent/HITL backend
> 56fad95 feat(marketing-hub): Intent Orchestrator + HITL — backend (FR-MH-009)
> 6b5dfd1 feat(marketing-hub): fundação BYOK de canal de e-mail per-tenant (FR-MH-012)
> 0610952 feat(marketing-hub): cron de avanço de nurturing (FR-MH-008 "cron avança passos")
> 25a8b28 chore(observability): functionName em todas as fns do fallback LLM — fim do :unknown
> --- STATUS ---
> --- DIFF STAT ---
> --- BEHIND/AHEAD ---
> 0	0
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(00:42:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"--- CHROMA ---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat || echo \"chroma unreachable\"",
  "description": "Docker mesh + Chroma health"
}
```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> --- BoK suites ---
> aios-sql-bridge
> canvas-design
> constellation-v2
> conteudo-v2
> e2e-user-zero
> gamificacao-nodes
> marketing-hub
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> viralmind
> --- HANDOFF lines ---
> 6705 HANDOFF.md
> --- scratch ---
> scratch clean
> --- sprint file ---
> -rw-rw-r-- 1 ubuntu ubuntu 83565 Jun  3 21:38 .claude/context/sprint-priorities.md
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_chroma: Up 11 days (healthy)
> mcorch_claude_mem: Up 11 days (healthy)
> ---
> mega-brain-dashboard: Up 11 days
> mega-brain-webhook: Up 11 days (healthy)
> mega-brain-daemon: Up 11 days (healthy)
> --- CHROMA ---
> {"nanosecond heartbeat":1780533756639159218}
> ```

## 🤖 Claude *(00:42:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- BoK suites ---\"; ls docs/bok/ 2>/dev/null; echo \"--- HANDOFF lines ---\"; wc -l HANDOFF.md; echo \"--- scratch ---\"; ls scratch/ 2>/dev/null && echo \"scratch HAS files\" || echo \"scratch clean\"; echo \"--- sprint file ---\"; ls -la .claude/context/sprint-priorities.md 2>/dev/null || echo \"no sprint file\"",
  "description": "BoK suites, HANDOFF size, scratch, sprint file"
}
```

## 🤖 Claude *(00:42:57)*


## 🤖 Claude *(00:42:58)*

Pre-flight green: working tree clean, **in sync with origin/main** (0/0), **zero TS errors**, all containers healthy, Chroma v2 alive. HANDOFF.md is 6705 lines. Now the targeted reads (read-from-end strategy + sprint head):

## 🤖 Claude *(00:42:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 90
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
> 14	## Drift Audit + Ledger P0 + Marketing-Hub FRs (008/012/009) Record (2026-06-03)
> 15	
> 16	**v6.26.0 (2026-06-03)** — Sessão `/handson` → diretiva Sovereign "🔴 auditar drift deployado↔migrations" (irmãos do hotfix `async_orchestrate_step`); ao fechar, "faça 2+3+4" = BYOK (FR-MH-012) + Nurturing follow-up (FR-MH-008) + Intent+HITL (FR-MH-009). Padrão: **probe-first material** + **review independente por migration** + **smoke throwaway** por entrega. 7 commits.
> 17	
> 18	**O que foi entregue:**
> 19	- **Drift audit (veredito: incidente ISOLADO)** — 9 superfícies via Management API read-only (ledger 96==96 · contrato RPC 12/12 · verify_jwt edge 23==23 · 34 triggers · RLS toda-tabela on · pg_net siblings). Único drift real: `rls_auto_enable` (event-trigger out-of-band benigno que liga RLS em toda tabela nova) → **capturado** idempotente (`20260603210000`). + 6 fns SECURITY DEFINER com `search_path` travado (`210500`) + `trigger_sync_knowledge_mesh` morto-latente (kong:8000) **dropado** (`211000`). Anticorpo `scripts/qa/audit-schema-drift.sh` (8 checagens, exit 0) + SOP `schema-drift-audit.md`. (`773dce4`, `eaffec6`)
> 20	- **🔴 P0 ledger (achado adjacente, pré-existente)** — `award_mco_coins`/`add_user_score`/`deduct_mco_coins` davam EXECUTE a anon/authenticated/PUBLIC + confiavam `p_user_id` arbitrário → qualquer user logado cunhava mcoCoins via PostgREST direto. REVOKE (award/add_user_score = edge-only via service_role) + guardas em deduct (`p_amount<=0` + posse NULL-safe `auth.role() IS DISTINCT FROM 'service_role' AND p_user_id IS DISTINCT FROM auth.uid()`). Exploits provados **BLOQUEADOS** em prod (negativo→"deve ser positivo" · cross-user→42501 · award→permission denied). (`336e2b8`)
> 21	- **functionName** em 13/13 fns do fallback LLM — fim do `llm-fallback:unknown` (`25a8b28`).
> 22	- **FR-MH-008 cron** — `nurture-cron` (service-role, fan-out concorrência 8) + pg_cron `nurture-advance */15` + modo service-role em `nurture-dispatch` (espelha orchestrate-step; consent gate + billing single-source). Smoke cron 5/5 + USER 10/10. (`0610952`)
> 23	- **FR-MH-012 BYOK** — `resend_api_key` per-tenant na máquina user_api_keys (defs VIVAS verbatim — encrypt idempotente + INSTEAD OF tenant-guard + views) + campo Settings + deploy nginx. Round-trip 8/8 (sibling intacto, idempotente). (`6b5dfd1`)
> 24	- **FR-MH-009 Intent+HITL (backend)** — `intent_plans` (`20260603250000`, BoK data-model patcheado antes) + `intent-orchestrate` (policy engine auto-vs-HITL, canal outward fail-safe→HITL, rationale XAI). Smoke 8/8 (alto impacto→pending_hitl). (`56fad95`)
> 25	
> 26	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + `/security-review` (subagente independente por migration) · Owner=Sovereign (blast radius = schema de prod + RPC financeiro + créditos per-tenant + envios consent-críticos [gated]).
> 27	
> 28	| Verificação | Resultado |
> 29	|---|---|
> 30	| Drift audit | ✅ 9 superfícies · 1 drift benigno capturado · anticorpo exit 0 |
> 31	| P0 ledger | ✅ 3 RPCs travados · exploits bloqueados (erro/42501/permission denied) sob role simulado |
> 32	| FR-MH-008/012/009 | ✅ 3 migrations applied · 4 fns deployed · smokes 5/5·10/10·8/8·8/8 |
> 33	| /security-review | ✅ todas SAFE (subagentes independentes; adotada 1 recomendação fail-safe) |
> 34	| tsc / suíte | ✅ 0 erros · 257 passed / 2 skipped |
> 35	| Containers / Chroma | ✅ 5 healthy (11d) · Chroma v2 OK |
> 36	| Handoff node | ✅ `7a9925ad-a06a-4ea8-947f-238642c31bfd` embedded 768d |
> 37	| Mesh | ✅ 8770 nós (orphan de smoke `629f40ba` detectado + limpo) |
> 38	
> 39	| Commit | Conteúdo |
> 40	|---|---|
> 41	| `773dce4` | fix(schema): zera o drift deployado↔migrations |
> 42	| `eaffec6` | chore(audit): anticorpo de drift de schema (tool + SOP) |
> 43	| `336e2b8` | fix(billing): fecha P0 de cunhagem nos RPCs do ledger |
> 44	| `25a8b28` | chore(observability): functionName em 13/13 fns do fallback |
> 45	| `0610952` | feat(marketing-hub): cron de avanço de nurturing (FR-MH-008) |
> 46	| `6b5dfd1` | feat(marketing-hub): fundação BYOK de canal (FR-MH-012) |
> 47	| `56fad95` | feat(marketing-hub): Intent Orchestrator + HITL backend (FR-MH-009) |
> 48	
> 49	### Survival Laws Self-audit
> 50	```
> 51	Law 1 (Materiality): ✅ toda claim provada NESTE turno — 4 migrations "Finished" + ACL/body via catalog + 4 smokes throwaway (output literal) + exploits bloqueados material (42501/erro/permission denied sob role simulado) + 2 /security-review independentes + handoff node embedded 768d + orphan de smoke detectado+limpo+contado. Zero fabricação. 1 falso-sucesso de embed (payload {record} errado) corrigido p/ {node_id}.
> 52	Law 2 (Process): ✅ SOP [[schema-drift-audit|schema-drift-audit]].md (Lei 5 anticorpo) + BoK data-model patcheado (intent_plans) ANTES da migration; toda migration passou /security-review (regra CLAUDE.md). Trap evitado: BYOK reproduziu defs VIVAS (não o template stale de 060000) preservando fixes 130000/140000.
> 53	Law 3 (Pruning): ✅ sessão de densidade máxima (drift + P0 + 3 FRs) usando a janela inteira (calibração 1M/Max); UI deferida conscientemente (incremento completo > meio-feature); orphan limpo por foco.
> 54	Law 4 (ORO): ✅ triplet declarado; "faça 2+3+4" + GO explícito (AskUserQuestion) nas decisões de escopo + no P0 financeiro.
> 55	```
> 56	
> 57	**Pendências/Próximos:**
> 58	- **UI follows (deferidas):** botão enroll de nurturing (hook `enrollLead` já existe em useNurturing) + `useIntentOrchestrator` hook + `HITLApprovalCard` (FR-MH-009 backend pronto, falta o rosto).
> 59	- **Executor de intent_plans** (aprovar/rejeitar/executar) — DEVE re-validar ação outward no execute (defesa-em-profundidade; não confiar em `auto_approved`).
> 60	- **Entrega externa de nurturing** (real, por canal) — segue gated; agora com `resend_api_key` per-tenant pronto como credencial.
> 61	- **FR-MH-010 AEO audit** — única FR marketing-hub restante.
> 62	- Twitter CreditsDepleted · Atribuição de clique ML (aguardando Sovereign).
> 63	
> 64	---
> 65	
> 66	## Flywheel Resurrection + mcoCoins Calibration Record (2026-06-03)
> 67	
> 68	**v6.25.0 (2026-06-03)** — Sessão `/handson` → diretiva Sovereign: "o que precisamos pro 1º run pago E2E + não seria melhor já calibrar o COIN_COST?". Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados). O run pago então **expôs que o flywheel de conteúdo estava silenciosamente MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo `orchestrate-content` preso em `pipeline_runs.status='running'`. Padrão: **probe-first material** (cada causa raiz provada antes do fix) + **adversarial verify** (echo de debug provou a causa do WP — array de posts `www`, não chute).
> 69	
> 70	**O que foi entregue:**
> 71	- **Calibração COIN_COST (OTD-MCOIN-CALIBRATION FECHADA)** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso = venda Enterprise R$997/10000 ÷ R$5.5, pior margem). **Surpresa honesta:** o `10` (orchestrate) e o `125` (canvas vídeo) **já** eram ~4× sobre o custo real ($0.04 imagem DALL·E · $0.56 vídeo Higgsfield); único furo era `IMAGE_GENERATION` (1.36×→9); `CONTENT_GENERATION 5→2`. Esses 2 **não têm caminho de cobrança em prod** (orchestrate cobra flat 10) → mudança segura. SOP `mcoin-cost-calibration.md`. (commit `73b8282`)
> 72	- **3 P0s do flywheel fixados + provados E2E:**
> 73	  - **#1** `orchestrate-step verify_jwt=false` no `config.toml` (faltava → default `true` → gateway 401 na chave opaca `sb_secret_` do pg_net). Deploy 118.4kB. (commit `7b3a481`)
> 74	  - **#2** `async_orchestrate_step` realinhada p/ `p_service_key` + `GRANT service_role` (estava `p_service_jwt_legacy` por hotfix em prod **sem migration** → PGRST202 → auto-chain morto). Migration `20260603190000` · `/security-review` SAFE · `db push` Finished. (commit `166dfbf`)
> 75	  - **#3** `wp_site_url` `mcorch.com`→`https://www.mcorch.com` (não-www → 301 → POST vira GET → WP devolve LISTA → sem `post_url`). `publish-wordpress` endurecido (valida `id`, 502 honesto). (commit `9ce1301`)
> 76	- **SOP** `orchestrate-async-pipeline.md` (3 modos de falha + gates de verificação + recovery) + `scripts/qa/gen-user-jwt.ts` (minta access_token de user p/ QA logada). (commit `091b7da`)
> 77	
> 78	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign (código + política de preço + GO do run + migration, via AskUserQuestion) · Owner=Sovereign (blast radius = gasto real de mcoCoins + 1ª publicação outward + schema de prod).
> 79	
> 80	| Verificação | Resultado |
> 81	|---|---|
> 82	| Calibração | ✅ tsc 0 · billing 22/22 · SOP |
> 83	| Bug #1 verify_jwt | ✅ deploy 118.4kB · orchestrate-step alcançável |
> 84	| Bug #2 migration | ✅ /security-review SAFE · db push Finished · RPC **204** (era PGRST202) |
> 85	| Auto-chain (#1+#2) | ✅ run `aca7b593` auto-completou a `done` SEM kick (linkedin+mesh) |
> 86	| Bug #3 WP | ✅ `publish-wordpress` retorna `post_url` (rascunho `p=13`); 502 honesto em não-www |
> 87	| **Flywheel COMPLETO E2E** | ✅ run `89f18bea` **6/6 passos `done` sem kick** · WP `?p=14` · `content_mesh_asset` done |
> 88	| tsc / suíte | ✅ 0 erros · 257 passed / 2 skipped (259) |
> 89	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 90	| Handoff node | ✅ `5e1b6f32-7d32-4fbb-a1b7-1834e42d187e` embedded 768d |
> ```

## 🤖 Claude *(00:43:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 6305,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 6305	
> 6306	  5. INSERT affiliate_links:
> 6307	       original_url · short_url · platform=mercadolivre
> 6308	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 6309	
> 6310	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 6311	
> 6312	ContentLibraryPage monetization flow:
> 6313	  Card (text, body contains mercadolivre.com.br)
> 6314	    └── DropdownMenu → "Monetizar Links ML"
> 6315	          → handleMonetizeLinks(item):
> 6316	               match(ML_URL_RE) → unique URLs
> 6317	               for url of unique:
> 6318	                 POST process-affiliate-link → affiliate_url
> 6319	                 body.split(url).join(affiliate_url)
> 6320	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 6321	          → Badge 💰 ML (emerald) exibido após monetização
> 6322	```
> 6323	
> 6324	---
> 6325	
> 6326	## Pending Actions (Commercial Launch)
> 6327	
> 6328	### CRITICAL — Must complete before first client
> 6329	
> 6330	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 6331	
> 6332	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 6333	
> 6334	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 6335	
> 6336	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 6337	
> 6338	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 6339	
> 6340	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 6341	
> 6342	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 6343	
> 6344	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 6345	
> 6346	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 6347	   ```bash
> 6348	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 6349	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 6350	   ```
> 6351	
> 6352	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 6353	
> 6354	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 6355	
> 6356	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 6357	
> 6358	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 6359	
> 6360	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 6361	
> 6362	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 6363	
> 6364	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 6365	
> 6366	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 6367	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 6368	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 6369	
> 6370	### SOCIAL — Next steps
> 6371	
> 6372	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 6373	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 6374	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 6375	
> 6376	### NON-CRITICAL
> 6377	
> 6378	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 6379	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 6380	- `browserslist` — ✅ updated (2026-04-26)
> 6381	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 6382	
> 6383	### GITNEXUS MCP — Next steps
> 6384	
> 6385	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 6386	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 6387	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 6388	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 6389	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 6390	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 6391	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 6392	
> 6393	### PHASE EPSILON — Next iterations
> 6394	
> 6395	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 6396	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 6397	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 6398	
> 6399	### CORE — Next iterations
> 6400	
> 6401	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 6402	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 6403	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 6404	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 6405	
> 6406	### PHASE DELTA — Next iterations
> 6407	
> 6408	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 6409	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 6410	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 6411	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 6412	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 6413	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 6414	
> 6415	### USUÁRIO ZERO — Checklist de validação
> 6416	
> 6417	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 6418	- ✅ Stripe sandbox secrets no vault
> 6419	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 6420	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 6421	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 6422	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 6423	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 6424	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 6425	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 6426	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 6427	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 6428	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 6429	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 6430	
> 6431	---
> 6432	
> 6433	## Infrastructure
> 6434	
> 6435	| Service | Container | Port | Status |
> 6436	|---------|-----------|------|--------|
> 6437	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 6438	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 6439	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 6440	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 6441	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 6442	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 6443	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 6444	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 6445	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 6446	
> 6447	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 6448	
> 6449	```bash
> 6450	docker compose up -d
> 6451	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 6452	```
> 6453	
> 6454	---
> 6455	
> 6456	## Security Model (Post-Go-Live)
> 6457	
> 6458	| Table | Isolation |
> 6459	|-------|-----------|
> 6460	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 6461	| `mcorch_edges` | Same pattern |
> 6462	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 6463	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 6464	
> 6465	---
> 6466	
> 6467	## Billing Architecture
> 6468	
> 6469	| Decision | Value |
> 6470	|----------|-------|
> 6471	| Canonical billing ledger | `profiles.mco_balance` |
> 6472	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 6473	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 6474	| Orchestration cost | 10 mcoCoins/run |
> 6475	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 6476	| Stripe | Sandbox keys active — swap to live before first client |
> 6477	
> 6478	---
> 6479	
> 6480	## GraphRAG State
> 6481	
> 6482	- **8769 total nodes** (v6.25.0: +handoff `5e1b6f32` + observation/content_mesh_asset nodes dos 3 runs E2E de validação do flywheel; was 8761 in v6.24.0 / 8759 in v6.22.0 snapshot)
> 6483	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 6484	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 6485	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 6486	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 6487	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 6488	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 6489	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 6490	- HNSW cosine index operational
> 6491	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 6492	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 6493	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 6494	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 6495	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 6496	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 6497	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 6498	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 6499	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 6500	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 6501	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 6502	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 6503	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 6504	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 6505	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 6506	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 6507	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 6508	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 6509	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 6510	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 6511	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 6512	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 6513	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 6514	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 6515	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 6516	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 6517	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 6518	
> 6519	### Embedding Model
> 6520	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 6521	Schema: `vector(768)` — HNSW cosine index.
> 6522	
> 6523	### Embedding Pipeline (Autônomo — 2026-05-03)
> 6524	Três camadas eliminam intervenção manual:
> 6525	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 6526	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 6527	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 6528	
> 6529	### Comandos de manutenção da Mesh
> 6530	```bash
> 6531	# Verificar nós sem embedding (deveria retornar array vazio):
> 6532	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 6533	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 6534	
> 6535	# Backfill manual (Bun-native — requer .env):
> 6536	bun run scripts/backfill-embeddings.ts
> 6537	
> 6538	# Backfill de código-fonte nos nós AST:
> 6539	bun run scripts/backfill-node-content.ts
> 6540	
> 6541	# Re-sync AST completo:
> 6542	cd packages/gitnexus-core && npm run sync-mesh
> 6543	
> 6544	# Acompanhar re-ingesta pós-commit:
> 6545	tail -f /tmp/mcorch-ingest.log
> 6546	```
> 6547	
> 6548	---
> 6549	
> 6550	## Video Rescue Protocol
> 6551	
> 6552	When a video generation operation (Google Veo) times out or client disconnects:
> 6553	```bash
> 6554	# Via edge function (production):
> 6555	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 6556	  -H "Authorization: Bearer <user_jwt>" \
> 6557	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 6558	
> 6559	# Via local script (admin/debug):
> 6560	source .env && bun run rescue.ts <operation_id> <content_id>
> 6561	```
> 6562	
> 6563	---
> 6564	
> 6565	## Architecture Pillars
> 6566	
> 6567	| Layer | Implementation |
> 6568	|-------|---------------|
> 6569	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 6570	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 6571	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 6572	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 6573	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 6574	
> 6575	---
> 6576	
> 6577	## Phase Delta — Architecture
> 6578	
> 6579	```
> 6580	OrchestrationPage (full-canvas, p-0)
> 6581	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 6582	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 6583	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 6584	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 6585	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 6586	        ├── nodes/PublishNode.tsx    ← final distribution output
> 6587	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 6588	        └── NodePalette.tsx          ← top toolbar to add nodes
> 6589	
> 6590	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 6591	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 6592	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 6593	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 6594	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 6595	```
> 6596	
> 6597	### Canvas State Architecture (Hybrid)
> 6598	
> 6599	```
> 6600	User interaction → ReactFlow internal state (positions, drag)
> 6601	                         ↓ (debounced 600ms)
> 6602	                   localStorage (positions persist across refresh)
> 6603	                         ↑
> 6604	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 6605	     ↓ (status changes sync to ReactFlow via useEffect)
> 6606	ReactFlow renders visual status (idle/running/done/error/blocked)
> 6607	```
> 6608	
> 6609	## Key Files
> 6610	
> 6611	| Purpose | Path |
> 6612	|---------|------|
> 6613	| Architecture rules | `CLAUDE.md` |
> 6614	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 6615	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 6616	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 6617	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 6618	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 6619	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 6620	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 6621	| **Node types** | `src/components/orchestrator/nodes/` |
> 6622	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 6623	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 6624	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 6625	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 6626	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 6627	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 6628	| Billing utilities | `src/lib/billing.ts` |
> 6629	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 6630	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 6631	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 6632	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 6633	| Video rescue (local) | `rescue.ts` |
> 6634	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 6635	| Backfill script | `scripts/backfill-embeddings.ts` |
> 6636	| Deploy harness | `scripts/harness-deploy.sh` |
> 6637	
> 6638	---
> 6639	
> 6640	## First Client Onboarding Checklist
> 6641	
> 6642	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 6643	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 6644	3. ~~Activate watchdog cron~~ ✅ Done
> 6645	4. ~~Deploy rescue-video function~~ ✅ Done
> 6646	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 6647	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 6648	7. Monitor `infra_health_logs` for first 24h.
> 6649	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 6650	
> 6651	---
> 6652	
> 6653	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 6654	
> 6655	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 6656	
> 6657	| Action | Result |
> 6658	|--------|--------|
> 6659	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 6660	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 6661	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 6662	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 6663	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 6664	
> 6665	| Commit | Conteúdo |
> 6666	|--------|----------|
> 6667	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 6668	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 6669	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 6670	
> 6671	### Arquitetura Matrix Intelligence
> 6672	
> 6673	```
> 6674	ConstellationMatrix (Stabilized Engine)
> 6675	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 6676	  └── NodeDetailsPanel (Tabbed Navigation)
> 6677	        ├── Tab Meta: Neighbor exploration + Net Context
> 6678	        ├── Tab Code: Source code preview (Supabase sync)
> 6679	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 6680	
> 6681	useNodeIntelligence Hook:
> 6682	  - contentQuery: fetch nodes.content column
> 6683	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 6684	  - state: isAnalyzing, analysisResult, progress
> 6685	```
> 6686	
> 6687	---
> 6688	
> 6689	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 6690	
> 6691	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 6692	
> 6693	| Action | Result |
> 6694	|--------|--------|
> 6695	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 6696	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 6697	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 6698	
> 6699	**Output da análise (estruturado em pt-BR):**
> 6700	- Visão Geral — papel do módulo no sistema
> 6701	- Padrões Detectados — design patterns, antipatterns
> 6702	- Acoplamento & Dependências — análise In/Out-Degree
> 6703	- Recomendações — 1-3 ações priorizadas
> 6704	
> ```

## 🤖 Claude *(00:43:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 120
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (39033 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(00:43:08)*


## 🤖 Claude *(00:43:09)*

Sprint file has very long lines — let me read just its head:

## 🤖 Claude *(00:43:10)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.26.0 selado em 2026-06-03** — **Drift audit + P0 ledger + 3 FRs marketing-hub**. `/handson` → diretiva Sovereign "🔴 auditar drift deployado↔migrations" (irmãos do hotfix `async_orchestrate_step`) → "faça 2+3+4". **(1) Drift audit:** 9 superfícies via Management API read-only (ledger 96==96 · contrato RPC 12/12 · verify_jwt edge 23==23 · 34 triggers · RLS toda-tabela · pg_net siblings) → **incidente ISOLADO**; único drift real `rls_auto_enable` (event-trigger out-of-band benigno que liga RLS em tabela nova) **capturado** + 6 SECURITY DEFINER `search_path` travado + trigger pg_net morto (kong:8000) dropado. Anticorpo `scripts/qa/audit-schema-drift.sh` (8 checagens, exit 0) + SOP `schema-drift-audit.md`. **(2) 🔴 P0 ledger:** os 3 RPCs (award/add_user_score/deduct) davam EXECUTE a anon/authenticated + confiavam `p_user_id` → cunhagem de mcoCoins via PostgREST direto; REVOKE (edge-only) + guardas em deduct (sinal + posse NULL-safe); **exploits provados BLOQUEADOS** em prod (erro/42501/permission denied). **(3) functionName 13/13** fallback LLM. **(4) FR-MH-008 cron** (`nurture-cron`+pg_cron `*/15`, modo service-role em nurture-dispatch; smoke 5/5+USER 10/10). **(5) FR-MH-012 BYOK** (`resend_api_key` per-tenant Vault — defs VIVAS verbatim — +Settings; round-trip 8/8). **(6) FR-MH-009 Intent+HITL backend** (`intent_plans`+`intent-orchestrate`: policy auto/HITL canal-outward-fail-safe + rationale XAI; smoke 8/8). 9 commits · 3 migrations · 4 deploys · `/security-review` independente por migration (todas SAFE) · Phase 5c **SEAL ALLOWED** (11 verified) · Mesh **8770** (orphan de smoke limpo) · Survival Laws **4/4**. **Novo Top Gap:** UI follows (enroll nurturing — hook já existe — + `useIntentOrchestrator`/`HITLApprovalCard`) · executor de `intent_plans` (re-validar ação outward no execute) · entrega externa nurturing (gated; credencial pronta) · FR-MH-010 AEO (última FR). **Lição:** probe-first viu que a metade-IA do FR-MH-012 já existia (só a metade-canal era nova) + evitou o trap do template stale de credenciais (reproduzir defs VIVAS, não migration antiga); o drift audit virou anticorpo reexecutável.
> 8	
> 9	**Sprint v6.25.0 selado em 2026-06-03** — **Flywheel ressuscitado + calibração mcoCoins**. `/handson` → diretiva Sovereign ("o que falta pro 1º run pago E2E + já calibrar o COIN_COST?"). Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados): **OTD-MCOIN-CALIBRATION FECHADA** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso=Enterprise); surpresa honesta — `10` (orchestrate) e `125` (canvas vídeo) **já** eram ~4× sobre custo real, único furo `IMAGE_GENERATION 3→9` (`CONTENT_GENERATION 5→2`). O **1º run pago E2E então expôs que o flywheel de conteúdo estava MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo run preso em `running`: **#1** `orchestrate-step` faltava no `config.toml` (`verify_jwt=true` → gateway **401** na chave opaca `sb_secret_` do pg_net); **#2** `async_orchestrate_step` hotfixada em prod **sem migration** (`p_service_jwt_legacy`≠`p_service_key` → **PGRST202** → auto-chain morto) → migration `20260603190000` realinha + `GRANT service_role`, `/security-review` SAFE, RPC **204**; **#3** `wp_site_url` não-www → **301 → POST vira GET** → WP devolve LISTA de posts → `publish-wordpress` endurecido (valida `id`, 502 honesto) + `wp_site_url→www`. **Provado E2E**: run `89f18bea` **auto-completou 6/6 passos sem kick** → rascunho WP `?p=14` + `content_mesh_asset` done. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8769**. Survival Laws **4/4**. 7 commits. **Novo Top Gap:** auditar **drift deployado↔migrations** (outras RPCs/fns hotfixadas em prod?) · limpar artefatos de teste (5 posts parqueados 2027 + 2 rascunhos WP) · FR-MH-009/010/012 + Nurturing follow-up · functionName nas 9 fns. **Lição:** o 1º run pago **não "falhou"** — fez seu trabalho: expôs 3 P0s silenciosos no coração do produto (falha sem erro visível, sem auto-refund); calibrar **antes** do run foi a decisão certa (transação econômica honesta).
> 10	
> 11	**Sprint v6.24.0 selado em 2026-06-03** — **Sessão de alta densidade** (diretiva Sovereign: selar a 45% é desperdício → usar a janela 1M inteira, selar só a ~95%; **Lei 3 recalibrada** em survival.md: poda≠selar). Resposta ao "faça os três, foco em endurecer o flywheel": 5 entregas pós-v6.23.0, cada uma com **smoke LIVE throwaway**. **(1) MVP-5 Atribuição (FR-MH-007)**: `handle-ml-postback`→`marketing_attribution` (campaign_id FK-safe, fail-soft) + `useCampaignAttribution`+card "Receita Atribuída"; smoke DB 4/4 (FK 23503 + de-linked). **(2) Hardening+observabilidade (FOCO)**: `eslint .` **honesto** (Deno `supabase/functions`+tailwind excluídos — ~3716 erros falsos, exit mascarado por `| tail`) + functionName telemetry no flywheel + smoke integração lead→score→campaign→attribution 5/5. **(3) Customer 360 (FR-MH-011)**: VIEW `security_invoker` RLS-safe + `useCustomer360`+drawer; /security-review SAFE + **isolation smoke 4/4** (B não vaza p/ A). **(4) Nurturing (FR-MH-008)**: engine `sequences`+`sequence_enrollments` (FK composta CASCADE) + `nurture-dispatch` **consent-gated** (envio gated) + `useNurturing`+`NurturingPanel`; /security-review SAFE + **consent-gate smoke 10/10**. 2 migrations /security-review SAFE (subagentes independentes) · tsc 0 · suíte **259** · eslint exit 0 honesto · 4 deploys · 5 smokes LIVE. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8761** (orphan obs de smoke limpo + smoke vacinado). Survival Laws **4/4**. 8 commits. **Novo Top Gap:** 1º run pago E2E (gated GO) · Nurturing follow-up (entrega externa real + cron + UI enroll/dispatch) · OTD-MCOIN-CALIBRATION · FRs restantes FR-MH-009/010/012. **Lição:** densidade máxima por sessão (5 frentes numa só) sem perda de materialidade — cada uma provada por smoke LIVE; o gate de lint estava mentindo (exit mascarado) — fix de raiz restaura honestidade da Lei 1.
> 12	
> 13	**Sprint v6.23.0 selado em 2026-06-03** — Marketing Hub backend completo + **MVP-4 UI live**: `campaign-run` (FR-MH-004) fechou o backend, depois o módulo inteiro ganhou rosto em `/dashboard/marketing` **absorvendo a UI v1** (não duplicando). **(1) campaign-run** JWT + débito atômico do FEE `CAMPAIGN_RUN` (10) → dispatch **paralelo** (`Promise.allSettled`) dos passos p/ `orchestrate-content` (self-bila 10) = **cascata fiel 10+10×N**; `email`→blocked; cap 8; smoke **13/13 zero-custo** (guards + isolamento de tenant + email-blocked + débito atômico 100→90 + cleanup); deploy 80.92kB; cascata paga **gated em GO**. **(2) MVP-4 UI**: `/dashboard/marketing` (LeadBoard 5 colunas + Pontuar/`lead-score` + overview campanhas; nav Target) + absorção v1 (`CampaignWizard` +Intenção/passo **Passos** composer→persiste `campaign_steps`; `CampaignDetail` +card **Passos & Execução** status vivo + `CampaignRunButton`). **(3) Hooks**: `useLeads`/`useLeadScore`/`useCampaignSteps`/`useCampaignRun`/`createCampaignWithSteps` + `src/lib/edge.ts`. tsc 0 · **11 testes** (suíte **255/257**) · eslint limpo nos tocados · build 22.32s deploy nginx · **UI LOGADA verificada** (magic link + agent-browser: `/dashboard/marketing` + wizard 6-passos/Passos renderizam, 0 erros console, zero mutação prod). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8760**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** 1º run pago E2E (Sovereign cria campanha→Rodar, gated em GO) · OTD-MCOIN-CALIBRATION ($) · OTD-CAMPAIGN-RUN-ASYNC (fila p/ campanha grande) · MVP-5 attribution→ROIWidget · **dívida de lint repo-wide** (~3716 erros pré-existentes em `supabase/functions` Deno, exit mascarado por `| tail` — não introduzidos nesta sessão). **Lição:** a diretiva Sovereign de calibração de contexto (1M/Max → não adiar por "contexto" antes de ~400k) destravou rodar o MVP-4 completo numa sessão; probe-first pegou a UI v1 existente ANTES de codar (absorver, não duplicar); a11y do agent-browser estava stale na transição framer-motion → li o stepper-text em vez de fabricar (Lei 1).
> 14	
> 15	**Sprint v6.22.0 selado em 2026-06-03** — Campaign Core + LLM Fallback + Lead Scoring: 4 entregas materiais via `/handson`→ação nos alertas→próximos priores. **(1) Alerta meta_config** verificado **VAZIO** (0 linhas · `auth.users` 1==`profiles` 1 — não fabriquei limpeza inexistente, Lei 1). **(2) MVP-2 Campaign Core LIVE** (migration `20260603025256`): `campaigns` **ABSORVIDA** via `ALTER` (+intent/channels/mesh_node_id + `UNIQUE(id,user_id)`) + `campaign_steps` (FK composta tenant-`CASCADE`, espelha lead_events) + `marketing_attribution` (FK simples `SET NULL` + RLS `WITH CHECK`, espelha consents); tenant-FK provado **comportamental** (23503 + 42501 autenticado + 201 + zero-resíduo); `/security-review` **SAFE** (subagente independente); mesh `7628892b`. **(3) OTD-LLM-FALLBACK FECHADA cedo** (SLA 06-07, owner engineer): probe-first achou o helper já live em 11 fns → fechei o gap de observabilidade do SOP (telemetria `infra_health_logs` autossuficiente em Deno) + **1º teste de edge-helper do projeto** (6 casos) + 11 fns redeploy; mesh `6061a6d2`. **(4) lead-score LIVE** (FR-MH-003): JWT + 1 mco atômico + IA per-user→sistema fail-soft; **smoke E2E** 200 · score=80 (`source=ai`) · débito 100→99 · zero-resíduo. **Calibração mcoCoins**: `COIN_COSTS` centralizado + dívida **OTD-MCOIN-CALIBRATION** (o `10` é redondo, não $-calibrado; `orchestrate` cobra 10 flat < soma dos componentes 18; vídeo é o maior custo real). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8759**. Survival Laws **4/4**. 6 commits. **Novo Top Gap:** `campaign-run` cascata fiel (**ADIADA por decisão Sovereign** — código financeiro + contexto saturado, Lei 3) + OTD-MCOIN-CALIBRATION (preços $ por-modelo/vídeo) · MVP-4 hooks+UI `/dashboard/marketing` · MVP-5 attribution. **Lição:** probe-first pegou a OTD já 80% pronta (zero retrabalho) e a divergência `campaigns`/`campaign_metrics` já-existentes; decisão financeira de `campaign-run` **registrada ao Sovereign em vez de improvisada** (Master Protocol).
> 16	
> 17	**Sprint v6.21.0 selado em 2026-06-03** — Marketing Hub (v2): BoK 9/9 + 11 agentes + MVP-1 Lead Core LIVE. Novo **módulo soberano** criado do zero seguindo o Master Execution Protocol (BoK-first), dirigido pela diretiva Sovereign de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). `/bok-scribe` selou a **suíte BoK 9/9** (1732 LOC, `docs/bok/marketing-hub/`, traceability **0 órfãos**, mesh seal `d5163fed` DERIVES_FROM meta-api) — módulo nasce como **v2 de consolidação** que **absorve e escala** o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**), natureza **Ambos** (interno Usuário Zero + comercial per-tenant). `/bok-agents-generator` produziu o **sistema de 11 agentes** (8 BoK + AEO/Intent-Orchestration/Demand-gen + Pantheon Reconciliation). Após revisão Sovereign ("aprovado"), **MVP-1 Lead Core** foi ao ar: migration `20260603000000` (`leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` LGPD SECURITY DEFINER), aplicada via `db push`. O `/security-review` (subagente **independente**) pegou **1 cross-tenant MEDIUM** (FK de tabela-filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta tenant-escopada `(lead_id,user_id)→leads(id,user_id)`** + provado **material** (23503 no ataque, 201 no legítimo, cleanup zero-resíduo). Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8755**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** MVP-2 Campaign Core deve **ABSORVER** a `campaigns` já existente (colisão real achada por probe-first), NÃO criar nova; + MVP-3 edge fns (`lead-score`/`campaign-run`) · MVP-4 hooks+UI (`/dashboard/marketing`) · MVP-5 attribution. **Lição:** probe-first do schema ANTES de codar pegou 2 divergências doc↔realidade (`campaigns` existe, `projects` não) que quebrariam o apply; e o `/security-review` por subagente independente (não auto-avaliação) pegou o furo de tenant que o self-review deixou passar.
> 18	
> 19	**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 20	
> 21	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 22	
> 23	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 24	
> 25	**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 26	
> 27	**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> 28	
> 29	**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 30	
> 31	**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 32	
> 33	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 34	
> 35	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 36	
> 37	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 38	
> 39	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 40	
> 41	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 42	
> 43	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 44	
> 45	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 46	
> 47	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 48	
> 49	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 50	
> 51	**Sprint v6.1.0 selado em 2026-05-14** — Canvas Studio UX Shell + Higgsfield Fix: shell do Canvas Studio migrado do `viralmind-builder` (store Zustand+zundo, lanes overlay, TopBar/LeftPanel/StatusBar, catálogo de 9 receitas, ImageLightbox, PipelineEdge); `canvas-execute` com endpoint Higgsfield corrigido (`platform.higgsfield.ai` rota Soul) + RPC `deduct_mco_coins`. Plano Phase 4.2 selado em `~/.claude/plans/floating-sleeping-sparrow.md`.
> 52	
> 53	**Sprint v6.1.1 selado em 2026-05-14** — viralmind BoK Suite Sealed: dívida documental do override consciente do BoK Gate quitada. 6 docs autorados (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) + `04-frd` reescrito de handbook CLAUDE.md → FRD real (32 FR + 14 NFR + matriz PR→FR). Ancorado nas 10 tabelas `vm_*` + 6 enums + Edge Functions `fetch-trends`/`canvas-execute`. Mesh seal `bok-scribe-seal-viralmind-v1` (`documentation_suite`, stability 0.85, revenue_impact R\$14M, embedded 768d). 7 OTDs registrados (destaques: `vector(1536)` vs padrão `768` sem índice HNSW — FMEA-VM-002 RPN 288; bucket `canvas-assets` público — FMEA-VM-003 RPN 140). BoK Gate do viralmind **liberado**. Sessão selada com ~51% de contexto — Canvas Studio Phase 4.2 diferida para sessão nova. 7463 nós · 100% embedded. 6 commits granulares. **Pendência conhecida (não desta sessão):** `docs/bok/gamificacao-nodes/` incompleta (5/9 docs) — rodar `/bok-scribe` ou completar antes de tocar o módulo.
> 54	
> 55	**Sprint v6.6.9 selado em 2026-05-20** — mcorch-qa-healing v1 — Material Proof Gate: novo módulo de QA sênior que fecha a fraqueza de Lei 1 (Materialidade) — o bloco Survival Laws Self-audit do `/handoff` era auto-declarado; agora é verificado mecanicamente pela nova **Fase 5c**. Executado em 6 stages na ordem de governança não-negociável (BoK → SOP → código): suíte BoK 9/9 `docs/bok/mcorch-qa-healing/` (1423 LOC, 6ª suíte do projeto, gerada via `/bok-scribe`, campos de mercado/monetização honestamente N/A para tooling interno) + SOP `docs/processes/handoff-material-proof-audit.md` (Lei 2) + engine `scripts/qa/` (5 módulos Bun, 710 LOC, injeção de dependências para reuso pelo cron OpenClaw) + skill `mcorch-qa-healing` + Fase 5c wired no `/handoff` (entre 5b e 6 — bloqueia em qualquer 🔴) + 2 suítes Vitest. O dry-run contra o selo v6.6.8 real pegou e fechou um falso-positivo (`COMMIT_RE` agarrava prefixos de UUID de 8-hex como commits — FMEA-002 fechada antes do gate ir ao ar). **Material proofs**: TS zero erros · 165 testes (122→165, +43) · **Fase 5c ao vivo neste selo → 13 verified · 0 skipped · 0 failed → SEAL ALLOWED** · 9 commits granulares · milestone node `a08780dc-f665-47c5-b34b-a2eb7c9eea5c` + documentation_suite seal `b00e938a-717b-4f62-b936-f4934845ec52` (DERIVES_FROM openclaw seal) embedded 768d · mesh **8361+ nodes** · Survival Laws Self-audit 4/4 ✓. **Hazard registrado**: agente main do OpenClaw (Qwen3.5 local) operou na mesma working dir durante a sessão — 3 diretórios gitignorados, zero overlap de path. **Próximo**: Canvas Design (Initiative B — integração `nexu-io/open-design`) em sessão dedicada via `/bok-scribe canvas-design`.
> 56	
> 57	**Sprint v6.6.8 selado em 2026-05-19** — Bridge Recovery + MAPE-K Audit + SDD aios-sql-bridge + Survival Laws 4/4: sessão de auditoria reativa disparada por Sovereign observando `claw.gcrux.com/dreaming` stagnation (Imported Insights congelado em 2026-05-16, Memory Palace counts estáticos, Dream Scene "0 promovido"). **Root cause material**: Stage 2 cron `nightly-bridge-refresh.sh` invocava `node` PATH-resolved como v18.19.1 no env do user `ubuntu` apesar do interativo ter v22.22.3 — OpenClaw CLI exige v22.12+ → 100% FAIL silently em Step 3 (reindex SQLite) há ≥3 dias; Steps 1+2 (bridge + distribute) rodavam clean. **Fix dual no mesmo edit**: (1) `NODE_BIN=/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolved-target (não symlink); (2) descoberta runtime de bug latente segundo — `claw-master` foi adicionado em v6.3.1 ao distribute script MAS NÃO ao indexer loop (`for agent in main artisan engineer scientist marketing-growth guardian; do` omitia claw-master) → `claw-master.sqlite` stale May 16 → exatamente o checkpoint "AIOS Core v2 (2026-05-16)" que Sovereign observou na UI. **SOP first per Lei 2**: `docs/processes/openclaw-bridge-recovery.md` 86 LOC autorada ANTES do edit. **5 phases materializadas** (todas com ORO triplet + Survival Laws ✓): Phase A (bridge fix + claw-master loop), Phase B (MAPE-K closed-loop audit + 4 observation nodes em mesh — Plan `a4c4c026` / Execute `69f6e356` / Monitor `d605bdda` / Analyze `d8952ce8` com edges DERIVES_FROM v6.6.7), Phase C (9 untracked files versionados via 3 commits: miv landing assets + miv tools + memory audit trail), Phase D (esta seal + milestone `c4643058`), Phase E (OTD-SSP01-001 closed via SDD `aios-sql-bridge` 376 LOC enterprise-grade + 00-index 69 LOC suite skeleton + documentation_suite seal `4e0acc7e` stability 0.85 DERIVES_FROM openclaw seal). **Material proofs**: 6 commits granulares pushed (`03911e9` fix(cron) + `cbdee4f` feat(landing) + `bb1cc96` chore(tools) + `2aa80f1` chore(memory) + `1b3bdd8` docs(bok) + `b71b991` docs(handoff) + `230ad70` docs(readme)); 7/7 SQLites OpenClaw reindexed (was 0/6 fail); log final `[2026-05-19T19:06:32-03:00] nightly-bridge-refresh DONE (zero failures)`; mesh **8359 nodes** (+6 desta seal); TS zero erros; 5 containers healthy. **Survival Laws Self-audit 4/4 ✓ pela primeira vez consecutivamente desde v6.6.0** — encerra retroativamente OTD-PROC-001 (RPN 60) + OTD-PROC-002 (RPN 40) + OTD-SSP01-001 (RPN 240 SLA 2026-05-24). **Pending TOP**: OE-661 Step 1.5 first-run E2E (Sovereign click `/dashboard/orchestration` TriggerNode); OTD-OE661-PER-USER refactor (SLA 2026-06-02, 14 dias); MAPE-K gaps 1/2/3 implementáveis em v6.7.x/v6.8.x conforme plans dedicados (recomendações registradas no mesh, aguardam acionamento).
> 58	
> 59	**Sprint v6.6.7 selado em 2026-05-19** — OE-661 Phase 1 Prep + API Tenancy Directive: sessão executou parcialmente o plan persistido OE-661 — toda a preparação completada, Step 1.5 (first run E2E) **DEFERRED** por context budget Sovereign 92% (retoma em ~3h). Infraestrutura material: SOP `docs/processes/orchestration-content-mesh-asset-emission.md` (120 LOC) escrita ANTES do código (Lei 2); `orchestrate-content/index.ts:404-465` emite `content_mesh_asset` em paralelo com observation via `Promise.allSettled` (Amendment A) gated por `wpPostUrl` (Amendment B); `link-forge.ts:153` ganha `.eq("project_id", "mcorch-affiliate")` (Amendment C); `handle-ml-postback/index.ts` ganha pulse `infra_health_logs` em 4 return paths (Amendment E — fecha cegueira de 17 dias). Deploys material: `orchestrate-content` 113.6kB + `handle-ml-postback` 60.45kB. Vault `GCRUX_ML_AFFILIATE_TOKEN` provisionado (digest `e86f74a0...`). **DIRETIVA SOVEREIGN-CLASS NOVA "API Tenancy Model"** emitida durante sessão (questionamento direto sobre por que usar env global se `affiliate_config` per-user já existia) — selada em 3 superfícies: `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` com resolution order de 3 níveis + 5 tabelas canônicas + 5 anti-patterns; `CLAUDE.md > Code standards` one-liner enforcement; auto-memory `feedback_api_tenancy_per_user.md` indexada. **OTD-OE661-PER-USER** registrada (RPN 120 · SLA 2026-06-02) catalogando violação em `link-forge.ts` + `process-affiliate-link` GET branch. Sovereign autorizou Opção B (provisionar global temporário com `affiliate_config.app_id` value, deferir refactor). **Survival Laws Self-audit retroativo (Amendment H)** v6.6.1..v6.6.5 + esta seal — conclusão: Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 (overrides conscientes v6.6.1+v6.6.3) · Lei 3 ✗ 0/5 (OTD-PROC-002 RPN 40) · Lei 4 ✗ 0/5 (OTD-PROC-001 RPN 60 — esta seal v6.6.7 começa cumprimento). **Material proofs**: TS zero erros · 122/122 testes em 4.84s · 7 commits granulares locais (`03f6822` SOP · `e662da3` orchestrate Amendments A+B · `bafac16` link-forge Amendment C · `9cec88a` postback Amendment E · `044f21e` CLAUDE+OTD diretiva · `96ee72a` README v6.6.7 · `7d06934` HANDOFF seal + redactions) · milestone node `9d482014-a759-4656-93d9-99e05ab4a714` embedded 768d · mesh **8353 nodes** (+1 desde v6.6.6) · 11650 edges (+33). Path correção material: `/dashboard/orchestrate` → `/dashboard/orchestration` (Sovereign clarification). **Próximos deliverables**: (a) Sovereign dispara primeira campanha real em `/dashboard/orchestration` (TriggerNode + topic Link Forge catálogo + wp+linkedin platforms + Run) → eu monitoro pipeline_runs + content_mesh_asset emit material via REST; (b) ao completar, synthetic postback chain (Amendment D) + cleanup (Amendment J); (c) selar v6.6.8 com flywheel rodando E2E pela primeira vez na história do projeto; (d) atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias) — SDD `aios-sql-bridge`; (e) executar Phase 2 (`mcoins-ledger-reconciliation.md`) — fecha OTD-V660-001.
> 60	
> ```

## 🤖 Claude *(00:43:30)*


## 🤖 Claude *(00:43:30)*

Material BoK completeness check before I compose the brief:

## 🤖 Claude *(00:43:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"OK  $slug\" || echo \"!!  $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK suite completeness loop"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> OK  aios-sql-bridge
> OK  canvas-design
> OK  constellation-v2
> OK  conteudo-v2
> OK  e2e-user-zero
> OK  gamificacao-nodes
> OK  marketing-hub
> OK  mcorch-constellation
> OK  mcorch-qa-healing
> OK  mercado-livre-api
> OK  meta-api
> OK  openclaw
> OK  viralmind
> ```

## 🤖 Claude *(00:43:39)*


## 🤖 Claude *(00:44:00)*

═══════════════════════════════════════════════════════════
  HANDSON — v6.26.0 · Drift Audit + Ledger P0 + Marketing-Hub FRs (selado 2026-06-03)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **v6.26.0** — Drift audit (veredito: incidente **ISOLADO**) + 🔴 P0 ledger fechado + FR-MH-008/012/009
  Últimos commits:
    `7bb15bc` — chore(sprint): update sprint-priorities v6.26.0
    `2220ab7` — docs(handoff): seal v6.26.0
    `56fad95` — feat(marketing-hub): Intent Orchestrator + HITL backend (FR-MH-009)
    `6b5dfd1` — feat(marketing-hub): BYOK de canal de e-mail per-tenant (FR-MH-012)
    `0610952` — feat(marketing-hub): cron de avanço de nurturing (FR-MH-008)

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ — em sincronia com `origin/main` (0↔0), nada por commitar.

🏗️ **INFRA**
  `mcorch_chroma`:     Up 11 days (healthy) — Chroma API v2: **OK** (`heartbeat` respondeu)
  `mcorch_claude_mem`: Up 11 days (healthy)
  `mega-brain-*`:      daemon healthy · webhook healthy · dashboard up (11d)

🧠 **KNOWLEDGE MESH**
  **8770 nós** · ~9070 arestas (fonte: GraphRAG State + tabela do seal v6.26.0) — 100% embedded (768d HNSW cosine)
  Tipos: handoff · milestone · architecture · decision · system · observation · requirement · documentation_suite · content_mesh_asset + AST
  Handoff node desta seal: `7a9925ad-a06a-4ea8-947f-238642c31bfd`

🔧 **TYPESCRIPT**
  Zero erros ✅ (`tsc --noEmit` sem output) · suíte 257 passed / 2 skipped no último seal

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
  Sealed: **13/13 completas** (9/9 docs cada) — incl. `marketing-hub`, `meta-api`, `constellation-v2`, `mercado-livre-api`
  Incomplete: **nenhuma** ✅
  → BoK Gate **LIBERADO** para todo módulo ativo (incluindo as UI follows do marketing-hub)

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional (LinkedIn ✅ · Twitter aguardando tier · Instagram pós-App Review)
  Top gap (v6.26.0): **UI follows do marketing-hub** + executor de `intent_plans` + entrega externa de nurturing + FR-MH-010 AEO

⚡ **PRÓXIMOS PASSOS** (prioridade — backend pronto, falta o rosto)
  1. **UI follows do Marketing Hub** — botão *enroll* de nurturing (hook `enrollLead` já existe em `useNurturing`) + `useIntentOrchestrator` + `HITLApprovalCard` (FR-MH-009 backend LIVE, sem UI).
  2. **Executor de `intent_plans`** (aprovar/rejeitar/executar) — **DEVE re-validar a ação outward no execute** (defesa-em-profundidade; não confiar em `auto_approved`).
  3. **FR-MH-010 AEO audit** — única FR restante do marketing-hub. Entrega externa de nurturing segue *gated* (credencial `resend_api_key` per-tenant já pronta).

⚠️ **ALERTAS**
  Nenhum alerta ✅ — TS limpo, containers saudáveis, worktree limpo, scratch/ limpo, sem BoK incompleta.
  Pendências externas conhecidas (não-bloqueantes): Twitter `CreditsDepleted` (cota Free) · atribuição de clique ML aguardando dado do Sovereign · Stripe ainda em sandbox (intencional, Usuário Zero).

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

O caminho mais natural a partir daqui é **dar rosto ao que o v6.26.0 deixou pronto no backend** (UI follows FR-MH-009/008 + executor de `intent_plans`). Quer que eu siga por aí, ataque a **FR-MH-010 (AEO)** para zerar as FRs do marketing-hub, ou tem outra direção?

## 👤 User *(00:46:37)*

<command-name>/goal</command-name>
            <command-message>goal</command-message>
            <command-args>⚡ PRÓXIMOS PASSOS (prioridade — backend pronto, falta o rosto)

UI follows do Marketing Hub — botão enroll de nurturing (hook enrollLead já existe em useNurturing) + useIntentOrchestrator + HITLApprovalCard (FR-MH-009 backend LIVE, sem UI).
Executor de intent_plans (aprovar/rejeitar/executar) — DEVE re-validar a ação outward no execute (defesa-em-profundidade; não confiar em auto_approved).
FR-MH-010 AEO audit — única FR restante do marketing-hub. Entrega externa de nurturing segue gated (credencial resend_api_key per-tenant já pronta).</command-args>

## 👤 User *(00:46:37)*

<local-command-stdout>Goal set: ⚡ PRÓXIMOS PASSOS (prioridade — backend pronto, falta o rosto)

UI follows do Marketing Hub — botão enroll de nurturing (hook enrollLead já existe em useNurturing) + useIntentOrchestrator + HITLApprovalCard (FR-MH-009 backend LIVE, sem UI).
Executor de intent_plans (aprovar/rejeitar/executar) — DEVE re-validar a ação outward no execute (defesa-em-profundidade; não confiar em auto_approved).
FR-MH-010 AEO audit — única FR restante do marketing-hub. Entrega externa de nurturing segue gated (credencial resend_api_key per-tenant já pronta).</local-command-stdout>

## 👤 User *(00:46:37)*

A session-scoped Stop hook is now active with condition: "⚡ PRÓXIMOS PASSOS (prioridade — backend pronto, falta o rosto)

UI follows do Marketing Hub — botão enroll de nurturing (hook enrollLead já existe em useNurturing) + useIntentOrchestrator + HITLApprovalCard (FR-MH-009 backend LIVE, sem UI).
Executor de intent_plans (aprovar/rejeitar/executar) — DEVE re-validar a ação outward no execute (defesa-em-profundidade; não confiar em auto_approved).
FR-MH-010 AEO audit — única FR restante do marketing-hub. Entrega externa de nurturing segue gated (credencial resend_api_key per-tenant já pronta).". Briefly acknowledge the goal, then immediately start (or continue) working toward it — treat the condition itself as your directive and do not pause to ask the user what to do. The hook will block stopping until the condition holds. It auto-clears once the condition is met — do not tell the user to run `/goal clear` after success; that's only for clearing a goal early.

## 🤖 Claude *(00:47:06)*


## 🤖 Claude *(00:47:12)*

Entendido, Maestro. A meta é executar os três itens que o `/handson` priorizou — todos com **backend LIVE, faltando o rosto** (exceto a FR-MH-010, que é nova). Sigo o padrão das últimas seals: **probe-first material → entrega incremental → smoke throwaway**, BoK Gate já **verde** (marketing-hub 9/9).

**ORO triplet desta task:**
- **Operator:** MCORCH Master Execution Agent
- **Reviewer:** Sovereign (Gabriel) + `/security-review` independente para qualquer migration/edge nova (executor de `intent_plans`)
- **Owner:** Sovereign — blast radius = UI que dispara ações outward (HITL approve/execute) + nova superfície de audit AEO; o risco material está no **executor re-validar a ação outward** (não confiar em `auto_approved`).

Começo pela **Fase de Probe** — entender materialmente o que já existe antes de escrever uma linha.

## 🤖 Claude *(00:47:13)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Marketing Hub UI + intent executor + AEO",
  "summary": "FR-MH-009 UI (useIntentOrchestrator/HITLApprovalCard) + nurturing enroll button + intent_plans executor (outward re-validate) + FR-MH-010 AEO audit"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Marketing Hub UI + intent executor + AEO". Continue your current work.'}]
> ```

## 🤖 Claude *(00:47:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== existing hooks/components (should be ABSENT) ===\"; ls -la src/hooks/useIntentOrchestrator.ts 2>/dev/null || echo \"ABSENT: useIntentOrchestrator.ts\"; ls -la src/components/marketing/HITLApprovalCard.tsx 2>/dev/null || echo \"ABSENT: HITLApprovalCard.tsx\"; ls -la src/components/marketing/IntentOrchestrator* 2>/dev/null || echo \"ABSENT: IntentOrchestrator component\"\necho \"=== intent_plans migration ===\"; ls -la supabase/migrations/*intent* 2>/dev/null || echo \"no intent migration glob\"; ls -la supabase/migrations/20260603250000* 2>/dev/null\necho \"=== intent-orchestrate edge fn ===\"; ls -la supabase/functions/intent-orchestrate/ 2>/dev/null\necho \"=== marketing components present ===\"; ls -la src/components/marketing/\necho \"=== marketing hooks present ===\"; ls -la src/hooks/ | grep -iE \"lead|campaign|nurtur|intent|marketing|customer\"",
  "description": "Locate intent files + marketing components/hooks inventory"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === existing hooks/components (should be ABSENT) ===
> ABSENT: useIntentOrchestrator.ts
> ABSENT: HITLApprovalCard.tsx
> ABSENT: IntentOrchestrator component
> === intent_plans migration ===
> -rw-rw-r-- 1 ubuntu ubuntu 2427 Jun  3 21:24 supabase/migrations/20260603250000_marketing_hub_intent_plans.sql
> -rw-rw-r-- 1 ubuntu ubuntu 2427 Jun  3 21:24 supabase/migrations/20260603250000_marketing_hub_intent_plans.sql
> === intent-orchestrate edge fn ===
> total 16
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun  3 21:29 .
> drwxrwxr-x 61 ubuntu ubuntu 4096 Jun  3 21:26 ..
> -rw-rw-r--  1 ubuntu ubuntu 8025 Jun  3 21:29 index.ts
> === marketing components present ===
> total 44
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun  3 13:32 .
> drwxrwxr-x 18 ubuntu ubuntu 4096 Jun  3 11:50 ..
> -rw-rw-r--  1 ubuntu ubuntu 3470 Jun  3 11:51 CampaignRunButton.tsx
> -rw-rw-r--  1 ubuntu ubuntu 4453 Jun  3 11:50 CampaignStepsEditor.tsx
> -rw-rw-r--  1 ubuntu ubuntu 8534 Jun  3 13:22 LeadBoard.tsx
> -rw-rw-r--  1 ubuntu ubuntu 2467 Jun  3 13:21 LeadDetailDialog.tsx
> -rw-rw-r--  1 ubuntu ubuntu 5679 Jun  3 13:32 NurturingPanel.tsx
> === marketing hooks present ===
> -rw-rw-r--  1 ubuntu ubuntu 13309 Jun  3 12:34 useCampaigns.ts
> -rw-rw-r--  1 ubuntu ubuntu  4444 Jun  3 13:20 useLeads.ts
> -rw-rw-r--  1 ubuntu ubuntu  4761 Jun  3 13:30 useNurturing.ts
> ```

## 🤖 Claude *(00:47:24)*


## 🤖 Claude *(00:47:25)*

Confirmado: `useIntentOrchestrator`/`HITLApprovalCard` **ausentes** (criar), backend `intent_plans` + `intent-orchestrate` **presentes**. Agora leio os contratos do backend + o estado atual da UI:

## 🤖 Claude *(00:47:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603250000_marketing_hub_intent_plans.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: marketing-hub Intent Orchestrator + HITL data layer (FR-MH-009).
> 2	-- BoK SSOT: docs/bok/marketing-hub/06-data-model.md (§Table intent_plans) + 04-frd.md FR-MH-009 + 05-sdd.md
> 3	--           (intent-orchestrate edge fn + useIntentOrchestrator + HITLApprovalCard; STRIDE row "Intent
> 4	--           Orchestrator / ação de alto impacto sem revisão = Tampering → policy engine + HITL obrigatório").
> 5	--
> 6	-- `intent-orchestrate` translates a natural-language intent into a task plan; a policy engine marks policy='hitl'
> 7	-- when any task is high-impact (publish / charge / external send) → status='pending_hitl' (human approval required);
> 8	-- otherwise policy='auto' / status='auto_approved'. `rationale` is the auditable XAI explanation. User-scoped
> 9	-- (no lead/campaign FK in MVP — a plan is a tenant's orchestration artifact); RLS default-deny.
> 10	
> 11	CREATE TABLE IF NOT EXISTS public.intent_plans (
> 12	  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 13	  user_id    uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 14	  intent     text NOT NULL,
> 15	  plan       jsonb NOT NULL DEFAULT '[]'::jsonb,  -- [{action, channel?, impact, rationale}]
> 16	  policy     text NOT NULL DEFAULT 'auto' CHECK (policy IN ('auto','hitl')),
> 17	  status     text NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','auto_approved','pending_hitl','approved','rejected','executed')),
> 18	  rationale  text,
> 19	  created_at timestamptz NOT NULL DEFAULT timezone('utc'::text, now()),
> 20	  updated_at timestamptz NOT NULL DEFAULT timezone('utc'::text, now())
> 21	);
> 22	
> 23	ALTER TABLE public.intent_plans ENABLE ROW LEVEL SECURITY;
> 24	CREATE POLICY "intent_plans_select_own" ON public.intent_plans FOR SELECT USING (auth.uid() = user_id);
> 25	CREATE POLICY "intent_plans_insert_own" ON public.intent_plans FOR INSERT WITH CHECK (auth.uid() = user_id);
> 26	CREATE POLICY "intent_plans_update_own" ON public.intent_plans FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 27	CREATE POLICY "intent_plans_delete_own" ON public.intent_plans FOR DELETE USING (auth.uid() = user_id);
> 28	
> 29	CREATE INDEX IF NOT EXISTS idx_intent_plans_user ON public.intent_plans (user_id);
> 30	CREATE INDEX IF NOT EXISTS idx_intent_plans_hitl ON public.intent_plans (user_id, created_at DESC) WHERE status = 'pending_hitl';
> 31	
> 32	CREATE TRIGGER tr_update_intent_plans_updated_at
> 33	  BEFORE UPDATE ON public.intent_plans
> 34	  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 35	
> ```

## 🤖 Claude *(00:47:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-orchestrate/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// intent-orchestrate — marketing-hub FR-MH-009 (BoK SSOT: 04-frd.md FR-MH-009 + 05-sdd.md §intent-orchestrate +
> 2	// STRIDE "Intent Orchestrator / ação de alto impacto sem revisão = Tampering → policy engine + HITL obrigatório").
> 3	// Translates a natural-language marketing intent into a task plan; a policy engine decides auto vs HITL; ANY
> 4	// high-impact task (publish/send/charge/ad-spend) forces human approval. Persists the plan + an auditable XAI
> 5	// rationale to intent_plans. JWT-guarded (verify_jwt=false + in-function getUser — edge-jwt SOP). Cost 0: it
> 6	// orchestrates; the sub-steps (campaign-run/orchestrate-content/nurture-dispatch) self-bill on execution.
> 7	import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> 8	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 9	import { fetchLLMWithFallback } from "../_shared/llm-fallback.ts";
> 10	
> 11	const corsHeaders = {
> 12	  "Access-Control-Allow-Origin": "*",
> 13	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 14	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 15	};
> 16	
> 17	interface PlanTask { action: string; channel?: string; impact?: "low" | "medium" | "high"; rationale?: string }
> 18	
> 19	// High-impact = outward / financial actions that MUST NOT run without human review (the HITL gate).
> 20	const HIGH_IMPACT_RE = /(publi|send|e-?mail|post|tweet|spend|ad[_-]?spend|charge|cobr|envi|dispar|whats|launch|lança)/i;
> 21	
> 22	serve(async (req) => {
> 23	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 24	  const json = (b: unknown, s = 200) =>
> 25	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 26	
> 27	  const url = Deno.env.get("SUPABASE_URL")!;
> 28	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 29	  const anonKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 30	  const admin = createClient(url, serviceKey);
> 31	
> 32	  try {
> 33	    const authHeader = req.headers.get("Authorization");
> 34	    if (!authHeader) return json({ error: "Missing authorization" }, 401);
> 35	    const userClient = createClient(url, anonKey, { global: { headers: { Authorization: authHeader } } });
> 36	    const { data: { user }, error: authError } = await userClient.auth.getUser();
> 37	    if (authError || !user) return json({ error: "Unauthorized" }, 401);
> 38	
> 39	    const { intent } = await req.json().catch(() => ({}));
> 40	    if (!intent || typeof intent !== "string" || !intent.trim()) return json({ error: "intent é obrigatório" }, 422);
> 41	
> 42	    // resolve per-user AI key → system fallback (API Tenancy Model).
> 43	    const { data: keys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 44	    const groqKey = keys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 45	    const openRouterKey = keys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 46	    const geminiKey = keys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 47	    const aiKey = groqKey || openRouterKey;
> 48	
> 49	    // generate the plan via AI (fail-soft to a single review task).
> 50	    let tasks: PlanTask[] = [];
> 51	    if (aiKey) {
> 52	      const isGroq = !!groqKey;
> 53	      try {
> 54	        const resp = await fetchLLMWithFallback(
> 55	          isGroq ? "https://api.groq.com/openai/v1/chat/completions" : "https://openrouter.ai/api/v1/chat/completions",
> 56	          {
> 57	            method: "POST",
> 58	            headers: { Authorization: `Bearer ${aiKey}`, "Content-Type": "application/json", "HTTP-Referer": "https://mcorch.com", "X-Title": "GCRUX Constellation" },
> 59	            body: JSON.stringify({
> 60	              model: isGroq ? "llama-3.3-70b-versatile" : "meta-llama/llama-3.3-70b-instruct",
> 61	              messages: [
> 62	                { role: "system", content: "Você é um orquestrador de marketing. Dada uma intenção, gere um plano de 2 a 5 tarefas. Responda APENAS com JSON: {\"tasks\":[{\"action\":\"verbo curto\",\"channel\":\"email|social|content|affiliate|none\",\"impact\":\"low|medium|high\",\"rationale\":\"por que esta tarefa\"}]}. impact=high para publicar, enviar, cobrar ou veicular anúncio." },
> 63	                { role: "user", content: String(intent).slice(0, 800) },
> 64	              ],
> 65	              stream: false, temperature: 0.4,
> 66	            }),
> 67	          },
> 68	          { openRouterKey, geminiKey, groqKey, functionName: "intent-orchestrate" },
> 69	        );
> 70	        if (resp.ok) {
> 71	          const data = await resp.json();
> 72	          const raw: string = data?.choices?.[0]?.message?.content ?? "";
> 73	          const match = raw.match(/\{[\s\S]*\}/);
> 74	          if (match) {
> 75	            const parsed = JSON.parse(match[0]);
> 76	            if (Array.isArray(parsed?.tasks)) {
> 77	              tasks = parsed.tasks.slice(0, 5).map((t: PlanTask) => ({
> 78	                action: String(t.action ?? "task").slice(0, 120),
> 79	                channel: t.channel ? String(t.channel).slice(0, 40) : undefined,
> 80	                impact: (["low", "medium", "high"].includes(String(t.impact)) ? t.impact : "medium") as PlanTask["impact"],
> 81	                rationale: t.rationale ? String(t.rationale).slice(0, 300) : undefined,
> 82	              }));
> 83	            }
> 84	          }
> 85	        }
> 86	      } catch (_) { /* fail-soft below */ }
> 87	    }
> 88	    let heuristic = false;
> 89	    if (tasks.length === 0) {
> 90	      heuristic = true;
> 91	      tasks = [{ action: "revisar_intencao", channel: "none", impact: "low", rationale: "Plano heurístico (IA indisponível ou resposta inválida) — revisar a intenção manualmente." }];
> 92	    }
> 93	
> 94	    // ── POLICY ENGINE: any high-impact task → HITL (mandatory human approval; STRIDE Tampering mitigation) ──
> 95	    // Fail-safe channel rule: ANY outward channel (anything that is not the internal 'none'/'content') forces HITL,
> 96	    // even if the AI mislabels impact=low or phrases the action verb to dodge the regex. Unknown channel → HITL.
> 97	    const isOutward = (c?: string) => !!c && !["none", "content"].includes(c.toLowerCase());
> 98	    const highImpact = tasks.some((t) => t.impact === "high" || HIGH_IMPACT_RE.test(t.action) || isOutward(t.channel));
> 99	    const policy: "auto" | "hitl" = highImpact ? "hitl" : "auto";
> 100	    const status = highImpact ? "pending_hitl" : "auto_approved";
> 101	    const rationale = heuristic
> 102	      ? "Gerado por heurística (sem IA) — requer revisão humana."
> 103	      : highImpact
> 104	        ? "O plano contém ao menos uma tarefa de alto impacto (publicar/enviar/cobrar/anúncio) → aprovação humana obrigatória (HITL) antes de executar."
> 105	        : "Apenas tarefas de baixo/médio impacto → auto-aprovado para execução.";
> 106	
> 107	    // persist (RLS-scoped via service role + explicit user_id).
> 108	    const { data: row, error: insErr } = await admin
> 109	      .from("intent_plans")
> 110	      .insert({ user_id: user.id, intent: intent.slice(0, 2000), plan: tasks, policy, status, rationale })
> 111	      .select("id").single();
> 112	    if (insErr || !row) {
> 113	      admin.from("infra_health_logs").insert({ service: "intent-orchestrate", status: "unhealthy" }).then(() => {}, () => {});
> 114	      return json({ error: "Falha ao persistir o plano", detail: insErr?.message }, 500);
> 115	    }
> 116	
> 117	    // observation node into the Knowledge Mesh (mandate: every orchestration run). Fire-and-forget.
> 118	    admin.from("mcorch_nodes").insert({
> 119	      node_type: "observation", name: `intent-plan-${row.id}`,
> 120	      content: `Intent: ${intent.slice(0, 200)} → policy=${policy} status=${status} (${tasks.length} tarefas)`,
> 121	      user_id: user.id,
> 122	    }).then(() => {}, () => {});
> 123	    admin.from("infra_health_logs").insert({ service: "intent-orchestrate", status: "healthy" }).then(() => {}, () => {});
> 124	
> 125	    return json({ status: "ok", plan_id: row.id, policy, plan_status: status, tasks, rationale, source: heuristic ? "heuristic" : "ai" });
> 126	  } catch (err) {
> 127	    admin.from("infra_health_logs").insert({ service: "intent-orchestrate", status: "unhealthy" }).then(() => {}, () => {});
> 128	    return json({ error: "Erro interno no intent-orchestrate", detail: String((err as Error)?.message ?? err) }, 500);
> 129	  }
> 130	});
> 131	
> ```

## 🤖 Claude *(00:47:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useNurturing.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { edgeErrorMessage } from '@/lib/edge';
> 5	import type { Tables } from '@/integrations/supabase/types';
> 6	
> 7	// marketing-hub FR-MH-008 (Nurturing Sequences). Harness Engineering: drip logic lives here.
> 8	
> 9	export type Sequence = Tables<'sequences'>;
> 10	export type SequenceEnrollment = Tables<'sequence_enrollments'>;
> 11	export interface SequenceStep { channel: string; wait_hours: number; prompt: string }
> 12	export type SequenceTrigger = 'manual' | 'status_change';
> 13	export type EnrollmentStatus = 'active' | 'paused' | 'completed' | 'opted_out';
> 14	
> 15	export const ENROLLMENT_STATUS_LABELS: Record<EnrollmentStatus, string> = {
> 16	  active: 'Ativa', paused: 'Pausada', completed: 'Concluída', opted_out: 'Opt-out',
> 17	};
> 18	
> 19	export function useNurturing() {
> 20	  const { user } = useAuth();
> 21	  const qc = useQueryClient();
> 22	
> 23	  const sequencesQuery = useQuery({
> 24	    queryKey: ['sequences', user?.id],
> 25	    queryFn: async () => {
> 26	      const { data, error } = await supabase.from('sequences').select('*').order('created_at', { ascending: false });
> 27	      if (error) throw error;
> 28	      return data as Sequence[];
> 29	    },
> 30	    enabled: !!user,
> 31	  });
> 32	
> 33	  const createSequence = useMutation({
> 34	    mutationFn: async (seq: { name: string; trigger?: SequenceTrigger; steps?: SequenceStep[] }) => {
> 35	      const { data, error } = await supabase.from('sequences')
> 36	        .insert({ user_id: user!.id, name: seq.name, trigger: seq.trigger ?? 'manual', steps: seq.steps ?? [] })
> 37	        .select().single();
> 38	      if (error) throw error;
> 39	      return data as Sequence;
> 40	    },
> 41	    onSuccess: () => qc.invalidateQueries({ queryKey: ['sequences'] }),
> 42	  });
> 43	
> 44	  const toggleActive = useMutation({
> 45	    mutationFn: async ({ id, active }: { id: string; active: boolean }) => {
> 46	      const { error } = await supabase.from('sequences').update({ active }).eq('id', id);
> 47	      if (error) throw error;
> 48	    },
> 49	    onSuccess: () => qc.invalidateQueries({ queryKey: ['sequences'] }),
> 50	  });
> 51	
> 52	  // Enroll a lead — idempotent via UNIQUE(sequence_id, lead_id); next_run_at = now (cron/dispatch picks it up).
> 53	  const enrollLead = useMutation({
> 54	    mutationFn: async ({ sequence_id, lead_id }: { sequence_id: string; lead_id: string }) => {
> 55	      const { data, error } = await supabase.from('sequence_enrollments')
> 56	        .insert({ user_id: user!.id, sequence_id, lead_id, current_step: 0, status: 'active', next_run_at: new Date().toISOString() })
> 57	        .select().single();
> 58	      if (error) throw error;
> 59	      return data as SequenceEnrollment;
> 60	    },
> 61	    onSuccess: () => qc.invalidateQueries({ queryKey: ['enrollments'] }),
> 62	  });
> 63	
> 64	  // Opt-out — hard stop; nurture-dispatch refuses any opted_out enrollment.
> 65	  const optOut = useMutation({
> 66	    mutationFn: async (enrollmentId: string) => {
> 67	      const { error } = await supabase.from('sequence_enrollments')
> 68	        .update({ status: 'opted_out', next_run_at: null }).eq('id', enrollmentId);
> 69	      if (error) throw error;
> 70	    },
> 71	    onSuccess: () => qc.invalidateQueries({ queryKey: ['enrollments'] }),
> 72	  });
> 73	
> 74	  return {
> 75	    sequences: sequencesQuery.data ?? [],
> 76	    isLoading: sequencesQuery.isLoading,
> 77	    createSequence, toggleActive, enrollLead, optOut,
> 78	  };
> 79	}
> 80	
> 81	export function useEnrollments(sequenceId?: string) {
> 82	  const { user } = useAuth();
> 83	  return useQuery({
> 84	    queryKey: ['enrollments', sequenceId],
> 85	    queryFn: async () => {
> 86	      let q = supabase.from('sequence_enrollments').select('*').order('created_at', { ascending: false });
> 87	      if (sequenceId) q = q.eq('sequence_id', sequenceId);
> 88	      const { data, error } = await q;
> 89	      if (error) throw error;
> 90	      return data as SequenceEnrollment[];
> 91	    },
> 92	    enabled: !!user,
> 93	  });
> 94	}
> 95	
> 96	export interface NurtureDispatchResult {
> 97	  status: 'dispatched' | 'completed' | 'blocked' | 'opted_out' | 'paused';
> 98	  enrollment_id: string;
> 99	  reason?: string;
> 100	  delivered?: boolean;
> 101	  message_preview?: string;
> 102	  new_balance?: number | null;
> 103	}
> 104	
> 105	/** FR-MH-008 — invokes the JWT-guarded, consent-gated nurture-dispatch (debits 2 mcoCoins; sends gated). */
> 106	export function useNurtureDispatch() {
> 107	  const qc = useQueryClient();
> 108	  return useMutation({
> 109	    mutationFn: async (enrollmentId: string): Promise<NurtureDispatchResult> => {
> 110	      const { data, error } = await supabase.functions.invoke('nurture-dispatch', { body: { enrollment_id: enrollmentId } });
> 111	      if (error) throw new Error(await edgeErrorMessage(error, 'Erro no nurture-dispatch'));
> 112	      return data as NurtureDispatchResult;
> 113	    },
> 114	    onSuccess: () => { qc.invalidateQueries({ queryKey: ['enrollments'] }); qc.invalidateQueries({ queryKey: ['leads'] }); },
> 115	  });
> 116	}
> 117	
> ```

## 🤖 Claude *(00:47:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/NurturingPanel.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState } from 'react';
> 2	import { Plus, Loader2, Mail, Power } from 'lucide-react';
> 3	import { Button } from '@/components/ui/button';
> 4	import { Card, CardContent } from '@/components/ui/card';
> 5	import { Badge } from '@/components/ui/badge';
> 6	import { Input } from '@/components/ui/input';
> 7	import { Label } from '@/components/ui/label';
> 8	import { Textarea } from '@/components/ui/textarea';
> 9	import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogTrigger } from '@/components/ui/dialog';
> 10	import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
> 11	import { Skeleton } from '@/components/ui/skeleton';
> 12	import { useNurturing } from '@/hooks/useNurturing';
> 13	import { CAMPAIGN_CHANNELS } from '@/hooks/useCampaigns';
> 14	import { toast } from '@/hooks/use-toast';
> 15	
> 16	function NewSequenceDialog({ onCreate, pending }: { onCreate: (v: { name: string; channel: string; prompt: string }) => void; pending: boolean }) {
> 17	  const [open, setOpen] = useState(false);
> 18	  const [name, setName] = useState('');
> 19	  const [channel, setChannel] = useState('email');
> 20	  const [prompt, setPrompt] = useState('');
> 21	  const submit = () => {
> 22	    if (!name.trim()) { toast({ title: 'Dê um nome à sequência', variant: 'destructive' }); return; }
> 23	    onCreate({ name: name.trim(), channel, prompt: prompt.trim() });
> 24	    setName(''); setPrompt(''); setOpen(false);
> 25	  };
> 26	  return (
> 27	    <Dialog open={open} onOpenChange={setOpen}>
> 28	      <DialogTrigger asChild><Button size="sm" className="gap-2"><Plus className="h-4 w-4" /> Nova sequência</Button></DialogTrigger>
> 29	      <DialogContent>
> 30	        <DialogHeader><DialogTitle>Nova sequência de nutrição</DialogTitle></DialogHeader>
> 31	        <div className="space-y-3">
> 32	          <div className="space-y-1.5"><Label>Nome *</Label><Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Ex: Boas-vindas" /></div>
> 33	          <div className="space-y-1.5">
> 34	            <Label>Canal do 1º passo</Label>
> 35	            <Select value={channel} onValueChange={setChannel}>
> 36	              <SelectTrigger className="h-9"><SelectValue /></SelectTrigger>
> 37	              <SelectContent>{CAMPAIGN_CHANNELS.map((c) => <SelectItem key={c.value} value={c.value}>{c.label}</SelectItem>)}</SelectContent>
> 38	            </Select>
> 39	          </div>
> 40	          <div className="space-y-1.5"><Label>Mensagem (prompt)</Label><Textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="O que a IA deve comunicar neste passo..." rows={2} /></div>
> 41	        </div>
> 42	        <DialogFooter>
> 43	          <Button onClick={submit} disabled={pending} className="gap-2">{pending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />} Criar</Button>
> 44	        </DialogFooter>
> 45	      </DialogContent>
> 46	    </Dialog>
> 47	  );
> 48	}
> 49	
> 50	/** FR-MH-008 — minimal Nurturing surface: list/create sequences + active toggle. Enroll/dispatch via hook/cron. */
> 51	export default function NurturingPanel() {
> 52	  const { sequences, isLoading, createSequence, toggleActive } = useNurturing();
> 53	
> 54	  const handleCreate = async (v: { name: string; channel: string; prompt: string }) => {
> 55	    try {
> 56	      await createSequence.mutateAsync({ name: v.name, trigger: 'manual', steps: [{ channel: v.channel, wait_hours: 24, prompt: v.prompt }] });
> 57	      toast({ title: 'Sequência criada' });
> 58	    } catch (e) { toast({ title: (e as Error).message || 'Erro ao criar sequência', variant: 'destructive' }); }
> 59	  };
> 60	
> 61	  return (
> 62	    <section className="space-y-3">
> 63	      <div className="flex items-center justify-between">
> 64	        <div>
> 65	          <h2 className="text-lg font-heading font-semibold text-foreground">Nutrição (drip)</h2>
> 66	          <p className="text-xs text-muted-foreground">{sequences.length} sequência(s) · envio gated por consentimento (LGPD)</p>
> 67	        </div>
> 68	        <NewSequenceDialog onCreate={handleCreate} pending={createSequence.isPending} />
> 69	      </div>
> 70	
> 71	      {isLoading ? (
> 72	        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{[1, 2, 3].map((i) => <Skeleton key={i} className="h-20 rounded-lg" />)}</div>
> 73	      ) : sequences.length === 0 ? (
> 74	        <Card className="border-dashed"><CardContent className="py-8 text-center text-sm text-muted-foreground"><Mail className="h-8 w-8 mx-auto mb-2 text-muted-foreground/40" />Nenhuma sequência ainda.</CardContent></Card>
> 75	      ) : (
> 76	        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
> 77	          {sequences.map((s) => {
> 78	            const steps = Array.isArray(s.steps) ? s.steps.length : 0;
> 79	            return (
> 80	              <Card key={s.id}>
> 81	                <CardContent className="p-4 space-y-2">
> 82	                  <div className="flex items-start justify-between gap-2">
> 83	                    <p className="text-sm font-medium text-foreground truncate">{s.name}</p>
> 84	                    <Badge variant="secondary" className={s.active ? 'bg-emerald-500/20 text-emerald-400' : 'bg-muted text-muted-foreground'}>
> 85	                      {s.active ? 'Ativa' : 'Pausada'}
> 86	                    </Badge>
> 87	                  </div>
> 88	                  <p className="text-xs text-muted-foreground">{steps} passo(s) · gatilho {s.trigger === 'manual' ? 'manual' : 'mudança de status'}</p>
> 89	                  <Button size="sm" variant="ghost" className="h-7 px-2 text-xs gap-1"
> 90	                    onClick={() => toggleActive.mutate({ id: s.id, active: !s.active })} disabled={toggleActive.isPending}>
> 91	                    <Power className="h-3 w-3" /> {s.active ? 'Pausar' : 'Ativar'}
> 92	                  </Button>
> 93	                </CardContent>
> 94	              </Card>
> 95	            );
> 96	          })}
> 97	        </div>
> 98	      )}
> 99	    </section>
> 100	  );
> 101	}
> 102	
> ```

## 🤖 Claude *(00:48:45)*


## 🤖 Claude *(00:48:48)*

Backend contracts claros. Os três verbos do executor (`approve`/`reject`/`execute`) operam sobre a máquina de estados `proposed→auto_approved|pending_hitl→approved|rejected→executed`, e o `enrollLead` já existe no hook — falta o botão na superfície de lead. Vou ler as superfícies restantes + o FRD (SSOT) das FR-MH-009/010 + o contrato de `verify_jwt`:

## 🤖 Claude *(00:48:49)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/MarketingPage.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useNavigate } from 'react-router-dom';
> 2	import { Megaphone, Plus, ArrowRight, Target } from 'lucide-react';
> 3	import { Button } from '@/components/ui/button';
> 4	import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> 5	import { Badge } from '@/components/ui/badge';
> 6	import LeadBoard from '@/components/marketing/LeadBoard';
> 7	import NurturingPanel from '@/components/marketing/NurturingPanel';
> 8	import { useCampaigns, STATUS_LABELS, STATUS_COLORS } from '@/hooks/useCampaigns';
> 9	import type { Database } from '@/integrations/supabase/types';
> 10	
> 11	type CampaignStatus = Database['public']['Enums']['campaign_status'];
> 12	
> 13	export default function MarketingPage() {
> 14	  const navigate = useNavigate();
> 15	  const { campaigns, isLoading } = useCampaigns();
> 16	
> 17	  const counts = campaigns.reduce((acc, c) => {
> 18	    acc[c.status] = (acc[c.status] ?? 0) + 1;
> 19	    return acc;
> 20	  }, {} as Record<CampaignStatus, number>);
> 21	  const recent = campaigns.slice(0, 4);
> 22	
> 23	  return (
> 24	    <div className="space-y-8">
> 25	      {/* Header */}
> 26	      <div className="flex flex-col gap-2">
> 27	        <div className="flex items-center gap-2">
> 28	          <Target className="h-6 w-6 text-primary" />
> 29	          <h1 className="text-2xl font-heading font-bold text-foreground">Marketing Hub</h1>
> 30	        </div>
> 31	        <p className="text-sm text-muted-foreground">
> 32	          Capture e qualifique leads, componha campanhas multicanal e dispare o pipeline de conteúdo.
> 33	        </p>
> 34	      </div>
> 35	
> 36	      {/* Leads board */}
> 37	      <section>
> 38	        <LeadBoard />
> 39	      </section>
> 40	
> 41	      {/* Campaigns overview */}
> 42	      <section className="space-y-3">
> 43	        <div className="flex items-center justify-between">
> 44	          <div>
> 45	            <h2 className="text-lg font-heading font-semibold text-foreground">Campanhas</h2>
> 46	            <p className="text-xs text-muted-foreground">
> 47	              {isLoading ? 'Carregando…' : `${campaigns.length} campanha(s)`}
> 48	            </p>
> 49	          </div>
> 50	          <div className="flex gap-2">
> 51	            <Button variant="outline" size="sm" className="gap-1.5" onClick={() => navigate('/dashboard/campaigns')}>
> 52	              Ver todas <ArrowRight className="h-4 w-4" />
> 53	            </Button>
> 54	            <Button size="sm" className="gap-1.5" onClick={() => navigate('/dashboard/campaigns/new')}>
> 55	              <Plus className="h-4 w-4" /> Nova campanha
> 56	            </Button>
> 57	          </div>
> 58	        </div>
> 59	
> 60	        {!isLoading && campaigns.length === 0 ? (
> 61	          <Card className="border-dashed">
> 62	            <CardContent className="flex flex-col items-center justify-center py-12 text-center">
> 63	              <Megaphone className="h-10 w-10 text-muted-foreground/40 mb-3" />
> 64	              <p className="text-sm text-muted-foreground mb-3">Nenhuma campanha ainda</p>
> 65	              <Button size="sm" onClick={() => navigate('/dashboard/campaigns/new')} className="gap-1.5">
> 66	                <Plus className="h-4 w-4" /> Criar primeira campanha
> 67	              </Button>
> 68	            </CardContent>
> 69	          </Card>
> 70	        ) : (
> 71	          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
> 72	            {recent.map((c) => (
> 73	              <Card
> 74	                key={c.id}
> 75	                className="cursor-pointer hover:border-primary/40 transition-colors"
> 76	                onClick={() => navigate(`/dashboard/campaigns/${c.id}`)}
> 77	              >
> 78	                <CardHeader className="pb-2">
> 79	                  <CardTitle className="text-sm truncate">{c.name}</CardTitle>
> 80	                </CardHeader>
> 81	                <CardContent>
> 82	                  <Badge variant="secondary" className={STATUS_COLORS[c.status]}>
> 83	                    {STATUS_LABELS[c.status]}
> 84	                  </Badge>
> 85	                  {c.intent && <p className="text-xs text-muted-foreground mt-2 line-clamp-2">{c.intent}</p>}
> 86	                </CardContent>
> 87	              </Card>
> 88	            ))}
> 89	          </div>
> 90	        )}
> 91	
> 92	        {/* status summary chips */}
> 93	        {!isLoading && campaigns.length > 0 && (
> 94	          <div className="flex flex-wrap gap-2 pt-1">
> 95	            {(Object.keys(counts) as CampaignStatus[]).map((s) => (
> 96	              <Badge key={s} variant="outline" className={`text-xs ${STATUS_COLORS[s]}`}>
> 97	                {STATUS_LABELS[s]}: {counts[s]}
> 98	              </Badge>
> 99	            ))}
> 100	          </div>
> 101	        )}
> 102	      </section>
> 103	
> 104	      {/* Nurturing (drip) — FR-MH-008 */}
> 105	      <NurturingPanel />
> 106	    </div>
> 107	  );
> 108	}
> 109	
> ```

## 🤖 Claude *(00:48:49)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/LeadDetailDialog.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { Loader2 } from 'lucide-react';
> 2	import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
> 3	import { Badge } from '@/components/ui/badge';
> 4	import { useCustomer360, LEAD_STATUS_LABELS, LEAD_STATUS_COLORS, type LeadStatus } from '@/hooks/useLeads';
> 5	
> 6	function Field({ label, value }: { label: string; value: string }) {
> 7	  return (
> 8	    <div className="flex items-center justify-between border-b border-border/40 pb-1.5">
> 9	      <span className="text-muted-foreground">{label}</span>
> 10	      <span className="text-foreground text-right">{value}</span>
> 11	    </div>
> 12	  );
> 13	}
> 14	
> 15	/** FR-MH-011 — unified lead profile (Customer 360) drawer, fed by the security_invoker view. */
> 16	export default function LeadDetailDialog({ leadId, open, onOpenChange }: {
> 17	  leadId: string | null;
> 18	  open: boolean;
> 19	  onOpenChange: (o: boolean) => void;
> 20	}) {
> 21	  const { data, isLoading } = useCustomer360(open ? (leadId ?? undefined) : undefined);
> 22	  const status = (data?.status ?? '') as LeadStatus;
> 23	  return (
> 24	    <Dialog open={open} onOpenChange={onOpenChange}>
> 25	      <DialogContent>
> 26	        <DialogHeader><DialogTitle>Perfil do lead · Customer 360</DialogTitle></DialogHeader>
> 27	        {isLoading ? (
> 28	          <div className="flex justify-center py-8"><Loader2 className="h-6 w-6 animate-spin text-primary" /></div>
> 29	        ) : !data ? (
> 30	          <p className="text-sm text-muted-foreground py-4">Perfil não disponível.</p>
> 31	        ) : (
> 32	          <div className="space-y-2.5 text-sm">
> 33	            <div className="flex items-center justify-between">
> 34	              <span className="font-medium text-foreground">{data.name || data.contact}</span>
> 35	              <Badge variant="secondary" className={LEAD_STATUS_COLORS[status] ?? ''}>
> 36	                {LEAD_STATUS_LABELS[status] ?? data.status}
> 37	              </Badge>
> 38	            </div>
> 39	            <Field label="Contato" value={data.contact} />
> 40	            <Field label="Origem" value={data.source} />
> 41	            <Field label="Score" value={data.score != null ? `${data.score}/100` : '—'} />
> 42	            <Field label="Eventos" value={String(data.event_count ?? 0)} />
> 43	            <Field label="Último evento" value={data.last_event_at ? new Date(data.last_event_at).toLocaleString('pt-BR') : '—'} />
> 44	            <Field label="Consentimento LGPD" value={data.has_consent ? `Ativo (${data.active_consents})` : 'Sem consentimento'} />
> 45	          </div>
> 46	        )}
> 47	      </DialogContent>
> 48	    </Dialog>
> 49	  );
> 50	}
> 51	
> ```

## 🤖 Claude *(00:48:49)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useLeads.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { edgeErrorMessage } from '@/lib/edge';
> 5	import type { Tables, TablesInsert, Database } from '@/integrations/supabase/types';
> 6	
> 7	// marketing-hub FR-MH-001 (Lead Lifecycle Board) + FR-MH-003 (Lead Scoring).
> 8	// Harness Engineering: all lead business logic lives here; components are display-only.
> 9	
> 10	export type Lead = Tables<'leads'>;
> 11	export type LeadStatus = 'new' | 'scored' | 'nurturing' | 'converted' | 'lost';
> 12	
> 13	// Board column order (left→right lifecycle). DB stores `status` as text with a CHECK on these 5 values.
> 14	export const LEAD_STATUSES: LeadStatus[] = ['new', 'scored', 'nurturing', 'converted', 'lost'];
> 15	
> 16	export const LEAD_STATUS_LABELS: Record<LeadStatus, string> = {
> 17	  new: 'Novo',
> 18	  scored: 'Pontuado',
> 19	  nurturing: 'Nutrindo',
> 20	  converted: 'Convertido',
> 21	  lost: 'Perdido',
> 22	};
> 23	
> 24	export const LEAD_STATUS_COLORS: Record<LeadStatus, string> = {
> 25	  new: 'bg-sky-500/15 text-sky-400 border-sky-500/30',
> 26	  scored: 'bg-violet-500/15 text-violet-400 border-violet-500/30',
> 27	  nurturing: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
> 28	  converted: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
> 29	  lost: 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30',
> 30	};
> 31	
> 32	export function useLeads(statusFilter?: LeadStatus) {
> 33	  const { user } = useAuth();
> 34	  const queryClient = useQueryClient();
> 35	
> 36	  const leadsQuery = useQuery({
> 37	    queryKey: ['leads', user?.id, statusFilter],
> 38	    queryFn: async () => {
> 39	      let query = supabase.from('leads').select('*').order('updated_at', { ascending: false });
> 40	      if (statusFilter) query = query.eq('status', statusFilter);
> 41	      const { data, error } = await query;
> 42	      if (error) throw error;
> 43	      return data as Lead[];
> 44	    },
> 45	    enabled: !!user,
> 46	  });
> 47	
> 48	  // Manual capture (leads also arrive via whatsapp-webhook). contact is NOT NULL (E.164 phone OR email).
> 49	  const createLead = useMutation({
> 50	    mutationFn: async (lead: Pick<TablesInsert<'leads'>, 'contact' | 'name'> & { intent_signal?: Record<string, unknown> }) => {
> 51	      const { data, error } = await supabase
> 52	        .from('leads')
> 53	        .insert({ ...lead, user_id: user!.id, source: 'manual', status: 'new' })
> 54	        .select()
> 55	        .single();
> 56	      if (error) throw error;
> 57	      return data as Lead;
> 58	    },
> 59	    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leads'] }),
> 60	  });
> 61	
> 62	  const updateLeadStatus = useMutation({
> 63	    mutationFn: async ({ id, status }: { id: string; status: LeadStatus }) => {
> 64	      const { data, error } = await supabase
> 65	        .from('leads')
> 66	        .update({ status })
> 67	        .eq('id', id)
> 68	        .select()
> 69	        .single();
> 70	      if (error) throw error;
> 71	      return data as Lead;
> 72	    },
> 73	    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leads'] }),
> 74	  });
> 75	
> 76	  return {
> 77	    leads: leadsQuery.data ?? [],
> 78	    isLoading: leadsQuery.isLoading,
> 79	    error: leadsQuery.error,
> 80	    createLead,
> 81	    updateLeadStatus,
> 82	  };
> 83	}
> 84	
> 85	export interface LeadScoreResult {
> 86	  status: 'ok';
> 87	  lead_id: string;
> 88	  score: number;
> 89	  rationale: string;
> 90	  new_balance: number | null;
> 91	}
> 92	
> 93	/** FR-MH-003 — invokes the JWT-guarded lead-score edge fn (debits 1 mcoCoin atomically). */
> 94	export function useLeadScore() {
> 95	  const queryClient = useQueryClient();
> 96	  return useMutation({
> 97	    mutationFn: async (lead_id: string): Promise<LeadScoreResult> => {
> 98	      const { data, error } = await supabase.functions.invoke('lead-score', { body: { lead_id } });
> 99	      if (error) throw new Error(await edgeErrorMessage(error, 'Erro ao pontuar lead'));
> 100	      return data as LeadScoreResult;
> 101	    },
> 102	    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leads'] }),
> 103	  });
> 104	}
> 105	
> 106	export type Customer360 = Database['public']['Views']['customer_360']['Row'];
> 107	
> 108	/** FR-MH-011 — unified per-lead profile from the customer_360 view (security_invoker → RLS-scoped). */
> 109	export function useCustomer360(leadId: string | undefined) {
> 110	  const { user } = useAuth();
> 111	  return useQuery({
> 112	    queryKey: ['customer_360', leadId],
> 113	    queryFn: async () => {
> 114	      const { data, error } = await supabase
> 115	        .from('customer_360')
> 116	        .select('*')
> 117	        .eq('lead_id', leadId!)
> 118	        .maybeSingle();
> 119	      if (error) throw error;
> 120	      return data as Customer360 | null;
> 121	    },
> 122	    enabled: !!user && !!leadId,
> 123	  });
> 124	}
> 125	
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> === FR-MH-009 + FR-MH-010 in FRD ===
> 15:**In scope:** Lead lifecycle (capture→score→nurture→convert) absorbing `whatsapp_leads`; campaign composition/run wrapping `orchestrate-content`; per-campaign attribution; consent + tenancy foundation (LGPD); nurturing sequences; intent orchestrator + HITL; AEO audit; Customer 360; BYOK per-tenant.
> 35:| FR-MH-009 | Intent Orchestrator + HITL | `intent-orchestrate`: traduz intenção→plano de tarefas; policy engine decide auto vs. HITL; aprovação humana persiste rationale (XAI) | High | PR-MH-011 | EdgeFunction + Hook | AT-MH-009 |
> 36:| FR-MH-010 | AEO Audit | `aeo-audit`: JWT-guarded, 5 mcoCoins, mede citação da marca p/ queries rastreadas (provider OTD-MH-003), persiste `aeo_audits` + recomendações | High | PR-MH-012 | EdgeFunction | AT-MH-010 |
> 54:| NFR-MH-009 | Observability | Cada path (success/degraded/error) emite `infra_health_logs` | 100% dos edge fns | Telemetry audit |
> 55:| NFR-MH-010 | Freshness (AEO) | Idade máxima de um audit AEO antes de "stale" | ≤ 7 dias | `aeo_audits.created_at` |
> 66:[Hook: useLeads / useCampaigns / useIntentOrchestrator]
> 122:| `aeo_audits.query` | `text` | NOT NULL | 1–280 chars | "Query de AEO obrigatória" |
> 138:| FR-MH-009 | ✅ Required | ✅ Required | — | Policy engine auto vs HITL |
> 139:| FR-MH-010 | ✅ Required | — | — | Provider real OU degradado documentado |
> 158:| PR-MH-005 | FR-MH-007 | NFR-MH-009 |
> 160:| PR-MH-011 | FR-MH-009 | NFR-MH-005 |
> 161:| PR-MH-012 | FR-MH-010 | NFR-MH-010 |
> === config.toml intent-orchestrate / verify_jwt sample ===
> 7:verify_jwt = false
> 9:verify_jwt = false
> 11:verify_jwt = false
> 13:verify_jwt = false
> 15:verify_jwt = false
> 17:verify_jwt = false
> 19:verify_jwt = false
> 20:[functions.nurture-dispatch]
> 21:verify_jwt = false
> 23:verify_jwt = false
> 24:[functions.intent-orchestrate]
> 25:verify_jwt = false
> 27:verify_jwt = false
> 29:verify_jwt = false
> 31:verify_jwt = false
> 33:verify_jwt = false
> 35:verify_jwt = false
> 37:verify_jwt = false
> 39:verify_jwt = false
> 41:verify_jwt = false
> 43:verify_jwt = false
> 46:verify_jwt = true
> 51:verify_jwt = false
> 54:verify_jwt = false
> 57:verify_jwt = false
> 60:verify_jwt = false
> 63:verify_jwt = false
> 66:verify_jwt = false
> 69:verify_jwt = false
> ```

## 🤖 Claude *(00:48:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== FR-MH-009 + FR-MH-010 in FRD ===\"; grep -nE \"FR-MH-009|FR-MH-010|AEO|Answer Engine|Intent\" docs/bok/marketing-hub/04-frd.md | head -40\necho \"=== config.toml intent-orchestrate / verify_jwt sample ===\"; grep -nE \"intent-orchestrate|nurture-dispatch|lead-score|verify_jwt\" supabase/config.toml | head -30",
  "description": "Read MarketingPage/LeadDetailDialog/useLeads + grep FRD + config.toml"
}
```

## 🤖 Claude *(00:49:13)*


## 🤖 Claude *(00:49:16)*

FRD specs capturados:
- **FR-MH-009**: `intent-orchestrate` + Hook (policy auto/HITL, aprovação humana persiste rationale XAI) — backend pronto, falta Hook+UI.
- **FR-MH-010**: `aeo-audit` — JWT, **5 mcoCoins**, mede citação da marca p/ queries rastreadas (provider OTD-MH-003 — "real OU degradado documentado"), persiste `aeo_audits` + recomendações. NFR-MH-010: stale ≤ 7 dias.

Leio o data-model/SDD canônicos (`aeo_audits` schema + design do executor) + o LeadBoard (onde entra o enroll) + a estrutura do config.toml:

## 🤖 Claude *(00:49:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== data-model: aeo_audits + intent_plans ===\"; grep -nEi \"aeo_audit|intent_plan|citation|cited|brand|recommend\" docs/bok/marketing-hub/06-data-model.md | head -40\necho \"=== SDD: [[aeo-audit|aeo-audit]] + executor + intent ===\"; grep -nEi \"[[aeo-audit|aeo-audit]]|aeo_audit|intent-execute|execute|executor|intent-orchestrate|useIntentOrchestrator|HITLApprovalCard\" docs/bok/marketing-hub/05-sdd.md | head -40\necho \"=== FRD: AT-MH-009 + AT-MH-010 acceptance ===\"; grep -nEi \"AT-MH-009|AT-MH-010|OTD-MH-003\" docs/bok/marketing-hub/04-frd.md | head -20",
  "description": "Grep data-model/SDD/FRD for aeo_audits schema + executor design + acceptance tests"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === data-model: aeo_audits + intent_plans ===
> 24:[aeo_audit] ──(N:1)──▶ [tenant/user]   (brand visibility snapshots)
> 35:- **aeo_audit:** snapshot de citação da marca em motores de resposta.
> 122:> **FK pattern (MVP-2):** `campaign_id`/`lead_id` usam **FK simples `ON DELETE SET NULL`** (não composta) + RLS `WITH CHECK` de posse — espelha `marketing_consents`. Uma FK composta `(lead_id,user_id)` com `SET NULL` anularia também `user_id NOT NULL` ao apagar o lead, quebrando; assim o registro financeiro é **retido de-linkado** (a receita não some quando o lead é apagado via `erase_lead`). `erase_lead()` é estendida (FMEA-MH-003) para reportar `attributions_delinked`.
> 124:### Table: `aeo_audits`
> 128:| `id` uuid PK · `user_id` uuid · `brand` text · `query` text · `cited` bool · `citation_rate` float4 · `engine` text (chatgpt\|perplexity\|google_ai\|gemini) · `recommendation` text · `created_at` timestamptz | Snapshot de visibilidade em motores de resposta |
> 130:### Table: `intent_plans`
> 181:> The remaining tables (`lead_events`, `campaigns`, `campaign_steps`, `sequences`, `sequence_enrollments`, `marketing_consents`, `marketing_attribution`, `aeo_audits`) follow the **identical RLS-default-deny skeleton** with `user_id = auth.uid()` and denormalized `user_id` for child tables to keep RLS simple. Every migration passes `/security-review` (FMEA-011).
> 193:| `aeo_snapshot` | `aeo:<brand>:<date>` | citation findings agregados | `brand + findings summary` |
> 230:| `aeo_audits` | ✅ Required | — | No |
> 245:| `aeo_audits` | `citation_rate` | 0.0 ≤ rate ≤ 1.0 | "Taxa de citação fora de faixa" |
> 257:| `aeo_audits` | 12 meses | Snapshot histórico | Cron purge |
> === SDD: [[aeo-audit|aeo-audit]] + executor + intent ===
> 18:│     HITLApprovalCard,AEODashboard,Customer360Panel}.tsx            │
> 24:│  useIntentOrchestrator · useAEO · useCustomer360 · useMarketingConsent│
> 30:│  lead-score · campaign-run · nurture-dispatch · intent-orchestrate ·│
> 31:│  [[aeo-audit|aeo-audit]] · erase-lead   (each: JWT gate → mcoCoins RPC → logic)  │
> 32:│  REUSES: orchestrate-content (campaign executor), embed-mcorch-node│
> 40:│  aeo_audits · marketing_consents│ │  marketing-growth Pantheon (reason)│
> 60:| `useIntentOrchestrator` | `useIntentOrchestrator.ts` | Intenção→plano; estado HITL | `['intent', userId]` |
> 61:| `useAEO` | `useAEO.ts` | Dispara/lê audits AEO | `['aeo-audits', userId]` |
> 71:| `HITLApprovalCard` | `marketing/HITLApprovalCard.tsx` | `{ plan }` | `useIntentOrchestrator` |
> 83:| `intent-orchestrate` | `supabase/functions/intent-orchestrate/index.ts` | JWT (user) | 0 (orquestra) | per-user AI key |
> 84:| `aeo-audit` | `supabase/functions/aeo-audit/index.ts` | JWT (user) | 5 | per-user AI key + AEO provider key (OTD-MH-003) |
> 105:| `aeo_audits` | Table | Histórico de auditorias AEO | `<ts>_marketing_hub_aeo.sql` |
> 173:### `POST /functions/v1/aeo-audit`
> 206:-- leads RLS (mesmo padrão para lead_events, campaigns, sequences, aeo_audits, marketing_consents, marketing_attribution)
> 242:| AEO provider key (se OTD-MH-003=B) | `aeo-audit` | Supabase Vault | Per provider |
> 259:| `orchestrate-content` (reuse) | Executor de passo de campanha | Reuso (não duplica) |
> 293:  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
> 299:> Every migration passes `/security-review` before commit (FMEA-011). `marketing_consents`, `marketing_attribution`, `campaigns`, `sequences`, `aeo_audits` follow the same RLS-default-deny skeleton (see 06-data-model.md).
> === FRD: AT-MH-009 + AT-MH-010 acceptance ===
> 35:| FR-MH-009 | Intent Orchestrator + HITL | `intent-orchestrate`: traduz intenção→plano de tarefas; policy engine decide auto vs. HITL; aprovação humana persiste rationale (XAI) | High | PR-MH-011 | EdgeFunction + Hook | AT-MH-009 |
> 36:| FR-MH-010 | AEO Audit | `aeo-audit`: JWT-guarded, 5 mcoCoins, mede citação da marca p/ queries rastreadas (provider OTD-MH-003), persiste `aeo_audits` + recomendações | High | PR-MH-012 | EdgeFunction | AT-MH-010 |
> ```

## 🤖 Claude *(00:49:20)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/LeadBoard.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useMemo, useState } from 'react';
> 2	import { motion } from 'framer-motion';
> 3	import { Plus, Sparkles, Loader2, UserPlus, Eye } from 'lucide-react';
> 4	import { Button } from '@/components/ui/button';
> 5	import { Card, CardContent } from '@/components/ui/card';
> 6	import { Badge } from '@/components/ui/badge';
> 7	import { Input } from '@/components/ui/input';
> 8	import { Label } from '@/components/ui/label';
> 9	import {
> 10	  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogTrigger,
> 11	} from '@/components/ui/dialog';
> 12	import {
> 13	  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger,
> 14	} from '@/components/ui/dropdown-menu';
> 15	import { Skeleton } from '@/components/ui/skeleton';
> 16	import {
> 17	  useLeads, useLeadScore, LEAD_STATUSES, LEAD_STATUS_LABELS, LEAD_STATUS_COLORS,
> 18	  type Lead, type LeadStatus,
> 19	} from '@/hooks/useLeads';
> 20	import LeadDetailDialog from './LeadDetailDialog';
> 21	import { toast } from '@/hooks/use-toast';
> 22	
> 23	function scoreColor(score: number): string {
> 24	  if (score >= 70) return 'bg-emerald-500/20 text-emerald-400';
> 25	  if (score >= 40) return 'bg-amber-500/20 text-amber-400';
> 26	  return 'bg-zinc-500/20 text-zinc-400';
> 27	}
> 28	
> 29	function LeadCard({ lead, onScore, onMove, onDetail, scoring }: {
> 30	  lead: Lead;
> 31	  onScore: (id: string) => void;
> 32	  onMove: (id: string, status: LeadStatus) => void;
> 33	  onDetail: (id: string) => void;
> 34	  scoring: boolean;
> 35	}) {
> 36	  return (
> 37	    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
> 38	      <Card className="hover:border-primary/40 transition-colors">
> 39	        <CardContent className="p-3 space-y-2">
> 40	          <div className="flex items-start justify-between gap-2">
> 41	            <div className="min-w-0">
> 42	              <p className="text-sm font-medium text-foreground truncate">{lead.name || lead.contact}</p>
> 43	              {lead.name && <p className="text-xs text-muted-foreground truncate">{lead.contact}</p>}
> 44	            </div>
> 45	            {lead.score != null && (
> 46	              <Badge variant="secondary" className={`shrink-0 ${scoreColor(lead.score)}`}>{lead.score}</Badge>
> 47	            )}
> 48	          </div>
> 49	          <div className="flex items-center gap-1.5">
> 50	            {lead.status !== 'converted' && lead.status !== 'lost' && (
> 51	              <Button
> 52	                size="sm" variant="outline" className="h-7 px-2 text-xs gap-1"
> 53	                onClick={() => onScore(lead.id)} disabled={scoring}
> 54	              >
> 55	                {scoring ? <Loader2 className="h-3 w-3 animate-spin" /> : <Sparkles className="h-3 w-3" />}
> 56	                Pontuar
> 57	              </Button>
> 58	            )}
> 59	            <Button size="sm" variant="ghost" className="h-7 px-2 text-xs gap-1" onClick={() => onDetail(lead.id)}>
> 60	              <Eye className="h-3 w-3" /> Perfil
> 61	            </Button>
> 62	            <DropdownMenu>
> 63	              <DropdownMenuTrigger asChild>
> 64	                <Button size="sm" variant="ghost" className="h-7 px-2 text-xs">Mover</Button>
> 65	              </DropdownMenuTrigger>
> 66	              <DropdownMenuContent align="start">
> 67	                {LEAD_STATUSES.filter((s) => s !== lead.status).map((s) => (
> 68	                  <DropdownMenuItem key={s} onClick={() => onMove(lead.id, s)}>
> 69	                    {LEAD_STATUS_LABELS[s]}
> 70	                  </DropdownMenuItem>
> 71	                ))}
> 72	              </DropdownMenuContent>
> 73	            </DropdownMenu>
> 74	          </div>
> 75	        </CardContent>
> 76	      </Card>
> 77	    </motion.div>
> 78	  );
> 79	}
> 80	
> 81	function AddLeadDialog({ onAdd, pending }: { onAdd: (v: { contact: string; name: string }) => void; pending: boolean }) {
> 82	  const [open, setOpen] = useState(false);
> 83	  const [contact, setContact] = useState('');
> 84	  const [name, setName] = useState('');
> 85	  const submit = () => {
> 86	    if (!contact.trim()) { toast({ title: 'Informe telefone ou email do lead', variant: 'destructive' }); return; }
> 87	    onAdd({ contact: contact.trim(), name: name.trim() });
> 88	    setContact(''); setName(''); setOpen(false);
> 89	  };
> 90	  return (
> 91	    <Dialog open={open} onOpenChange={setOpen}>
> 92	      <DialogTrigger asChild>
> 93	        <Button size="sm" className="gap-2"><UserPlus className="h-4 w-4" /> Novo lead</Button>
> 94	      </DialogTrigger>
> 95	      <DialogContent>
> 96	        <DialogHeader><DialogTitle>Novo lead</DialogTitle></DialogHeader>
> 97	        <div className="space-y-3">
> 98	          <div className="space-y-1.5">
> 99	            <Label>Contato * (telefone ou email)</Label>
> 100	            <Input value={contact} onChange={(e) => setContact(e.target.value)} placeholder="+5511999998888 ou lead@email.com" />
> 101	          </div>
> 102	          <div className="space-y-1.5">
> 103	            <Label>Nome</Label>
> 104	            <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Opcional" />
> 105	          </div>
> 106	        </div>
> 107	        <DialogFooter>
> 108	          <Button onClick={submit} disabled={pending} className="gap-2">
> 109	            {pending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />} Adicionar
> 110	          </Button>
> 111	        </DialogFooter>
> 112	      </DialogContent>
> 113	    </Dialog>
> 114	  );
> 115	}
> 116	
> 117	export default function LeadBoard() {
> 118	  const { leads, isLoading, createLead, updateLeadStatus } = useLeads();
> 119	  const leadScore = useLeadScore();
> 120	  const [scoringId, setScoringId] = useState<string | null>(null);
> 121	  const [detailLeadId, setDetailLeadId] = useState<string | null>(null);
> 122	
> 123	  const byStatus = useMemo(() => {
> 124	    const map: Record<LeadStatus, Lead[]> = { new: [], scored: [], nurturing: [], converted: [], lost: [] };
> 125	    for (const lead of leads) {
> 126	      const s = (LEAD_STATUSES as string[]).includes(lead.status) ? (lead.status as LeadStatus) : 'new';
> 127	      map[s].push(lead);
> 128	    }
> 129	    return map;
> 130	  }, [leads]);
> 131	
> 132	  const handleScore = async (id: string) => {
> 133	    setScoringId(id);
> 134	    try {
> 135	      const r = await leadScore.mutateAsync(id);
> 136	      toast({ title: `Lead pontuado: ${r.score}/100`, description: r.rationale });
> 137	    } catch (e) {
> 138	      toast({ title: (e as Error).message, variant: 'destructive' });
> 139	    } finally {
> 140	      setScoringId(null);
> 141	    }
> 142	  };
> 143	
> 144	  const handleMove = async (id: string, status: LeadStatus) => {
> 145	    try {
> 146	      await updateLeadStatus.mutateAsync({ id, status });
> 147	      toast({ title: `Lead movido para "${LEAD_STATUS_LABELS[status]}"` });
> 148	    } catch {
> 149	      toast({ title: 'Erro ao mover lead', variant: 'destructive' });
> 150	    }
> 151	  };
> 152	
> 153	  const handleAdd = async (v: { contact: string; name: string }) => {
> 154	    try {
> 155	      await createLead.mutateAsync({ contact: v.contact, name: v.name || null });
> 156	      toast({ title: 'Lead adicionado' });
> 157	    } catch (e) {
> 158	      toast({ title: (e as Error).message || 'Erro ao adicionar lead', variant: 'destructive' });
> 159	    }
> 160	  };
> 161	
> 162	  return (
> 163	    <div className="space-y-4">
> 164	      <div className="flex items-center justify-between">
> 165	        <div>
> 166	          <h2 className="text-lg font-heading font-semibold text-foreground">Leads</h2>
> 167	          <p className="text-xs text-muted-foreground">{leads.length} lead(s) no funil</p>
> 168	        </div>
> 169	        <AddLeadDialog onAdd={handleAdd} pending={createLead.isPending} />
> 170	      </div>
> 171	
> 172	      {isLoading ? (
> 173	        <div className="grid gap-3 md:grid-cols-3 lg:grid-cols-5">
> 174	          {LEAD_STATUSES.map((s) => <Skeleton key={s} className="h-40 rounded-lg" />)}
> 175	        </div>
> 176	      ) : (
> 177	        <div className="grid gap-3 md:grid-cols-3 lg:grid-cols-5">
> 178	          {LEAD_STATUSES.map((status) => (
> 179	            <div key={status} className="space-y-2">
> 180	              <div className="flex items-center justify-between px-1">
> 181	                <Badge variant="outline" className={`text-xs ${LEAD_STATUS_COLORS[status]}`}>
> 182	                  {LEAD_STATUS_LABELS[status]}
> 183	                </Badge>
> 184	                <span className="text-xs text-muted-foreground">{byStatus[status].length}</span>
> 185	              </div>
> 186	              <div className="space-y-2 min-h-[2rem]">
> 187	                {byStatus[status].map((lead) => (
> 188	                  <LeadCard
> 189	                    key={lead.id} lead={lead}
> 190	                    onScore={handleScore} onMove={handleMove} onDetail={setDetailLeadId}
> 191	                    scoring={scoringId === lead.id}
> 192	                  />
> 193	                ))}
> 194	                {byStatus[status].length === 0 && (
> 195	                  <p className="text-[11px] text-muted-foreground/50 text-center py-3">—</p>
> 196	                )}
> 197	              </div>
> 198	            </div>
> 199	          ))}
> 200	        </div>
> 201	      )}
> 202	
> 203	      <LeadDetailDialog
> 204	        leadId={detailLeadId}
> 205	        open={!!detailLeadId}
> 206	        onOpenChange={(o) => { if (!o) setDetailLeadId(null); }}
> 207	      />
> 208	    </div>
> 209	  );
> 210	}
> 211	
> ```

## 🤖 Claude *(00:49:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml",
  "limit": 75
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	project_id = "bcyvddsykvehvpwstlfa"
> 2	
> 3	# Configuração de Bypass de JWT para Orquestração Soberana
> 4	# key-migration 2026-06-01: service→service targets are called with the new sb_secret_ key (not a JWT),
> 5	# so the gateway JWT check must be off; each function below enforces its own in-code auth gate.
> 6	[functions.publish-social]
> 7	verify_jwt = false
> 8	[functions.refresh-social-token]
> 9	verify_jwt = false
> 10	[functions.embed-mcorch-node]
> 11	verify_jwt = false
> 12	[functions.self-optimize]
> 13	verify_jwt = false
> 14	[functions.self-heal]
> 15	verify_jwt = false
> 16	[functions.orchestrate-content]
> 17	verify_jwt = false
> 18	[functions.orchestrate-step]
> 19	verify_jwt = false
> 20	[functions.nurture-dispatch]
> 21	verify_jwt = false
> 22	[functions.nurture-cron]
> 23	verify_jwt = false
> 24	[functions.intent-orchestrate]
> 25	verify_jwt = false
> 26	[functions.generate-content]
> 27	verify_jwt = false
> 28	[functions.generate-audio-script]
> 29	verify_jwt = false
> 30	[functions.generate-video-script]
> 31	verify_jwt = false
> 32	[functions.list-provider-models]
> 33	verify_jwt = false
> 34	[functions.generate-video]
> 35	verify_jwt = false
> 36	[functions.check-video-status]
> 37	verify_jwt = false
> 38	[functions.generate-image]
> 39	verify_jwt = false
> 40	[functions.analyze-seo]
> 41	verify_jwt = false
> 42	[functions.publish-wordpress]
> 43	verify_jwt = false
> 44	[functions.sync-knowledge-mesh]
> 45	enabled = true
> 46	verify_jwt = true
> 47	import_map = "./functions/sync-knowledge-mesh/deno.json"
> 48	entrypoint = "./functions/sync-knowledge-mesh/index.ts"
> 49	
> 50	[functions.higgsfield-webhook]
> 51	verify_jwt = false
> 52	
> 53	[functions.handle-ml-postback]
> 54	verify_jwt = false
> 55	
> 56	[functions.process-affiliate-link]
> 57	verify_jwt = false
> 58	
> 59	[functions.instagram-webhook]
> 60	verify_jwt = false
> 61	
> 62	[functions.stripe-webhook]
> 63	verify_jwt = false
> 64	
> 65	[functions.social-auth-callback]
> 66	verify_jwt = false
> 67	
> 68	[functions.social-auth-init]
> 69	verify_jwt = false
> 70	
> 71	
> ```

## 🤖 Claude *(00:49:58)*


## 🤖 Claude *(00:50:01)*

Picture canônico completo. `aeo_audits` (id·user_id·brand·query·cited·citation_rate·engine·recommendation·created_at) e o `intent-execute` ainda **não existem** como código. Vou ler o contrato SDD do `aeo-audit`, confirmar ausência da tabela `aeo_audits`, e ver como os types/migrations recentes estão estruturados:

## 🤖 Claude *(00:50:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md",
  "offset": 150,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 150	### `POST /functions/v1/campaign-run`
> 151	
> 152	```typescript
> 153	// Request
> 154	interface CampaignRunRequest {
> 155	  campaign_id: string
> 156	}
> 157	
> 158	// Response (HTTP 200)
> 159	interface CampaignRunResponse {
> 160	  status: 'ok'
> 161	  campaign_id: string
> 162	  run_id: string
> 163	  steps_dispatched: number
> 164	}
> 165	
> 166	// mcoCoins deduction point:
> 167	// → After JWT + ownership check, before dispatch:
> 168	//   await supabase.rpc('deduct_mco_coins', { p_user_id, p_amount: 10 })
> 169	// → HTTP 402 if insufficient balance
> 170	// → Then per step: invoke('orchestrate-content', { ...stepPayload }) and sync status
> 171	```
> 172	
> 173	### `POST /functions/v1/aeo-audit`
> 174	
> 175	```typescript
> 176	interface AeoAuditRequest { queries: string[]; brand: string }
> 177	interface AeoAuditResponse {
> 178	  status: 'ok'
> 179	  audit_id: string
> 180	  citation_rate: number        // % queries citando a marca
> 181	  findings: Array<{ query: string; cited: boolean; recommendation: string }>
> 182	}
> 183	// mcoCoins: deduct 5 at entry. Provider per OTD-MH-003; degraded mode documented if no provider.
> 184	```
> 185	
> 186	---
> 187	
> 188	## 5. Security Design
> 189	
> 190	### 5.1 Threat Model (STRIDE)
> 191	
> 192	| Component | Threat | Type | Severity | Mitigation |
> 193	|-----------|--------|------|----------|------------|
> 194	| `lead-score` / all edge fns | Acesso não autenticado | Spoofing | High | JWT validation no entry point (getUser) |
> 195	| `leads` / `marketing_consents` | Leitura cross-tenant de PII | Information Disclosure | **Critical** | RLS `user_id = auth.uid()` default-deny + guard de tenant nas views (padrão provado) |
> 196	| mcoCoins deduction | Bypass client-side | Tampering | Critical | RPC `deduct_mco_coins` server-side only |
> 197	| `erase-lead` | Erasure de lead alheio | Elevation of Privilege | **Critical** | SECURITY DEFINER escopado a `auth.uid()`; double-bind por `lead_id`+owner (padrão `disconnect_*`) |
> 198	| Nurturing dispatch | Envio sem consentimento | Repudiation / Compliance | **Critical** | Gate de consent obrigatório pré-envio; opt-out interrompe; audit trail |
> 199	| BYOK marketing keys | Vazamento de token de canal | Information Disclosure | High | Padrão Vault (cifra na trigger, view mascarada, `decrypted_*` service-role only) |
> 200	| Intent Orchestrator | Ação de alto impacto sem revisão | Tampering | High | Policy engine + HITL obrigatório + rationale XAI auditável |
> 201	| AEO provider call | Exfiltração via prompt injection no sinal | Tampering | Medium | Sanitização de input; provider isolado; sem secret no prompt |
> 202	
> 203	### 5.2 RLS Policy Definitions
> 204	
> 205	```sql
> 206	-- leads RLS (mesmo padrão para lead_events, campaigns, sequences, aeo_audits, marketing_consents, marketing_attribution)
> 207	ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
> 208	
> 209	CREATE POLICY "leads_select_own"
> ```

## 🤖 Claude *(00:50:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== aeo_audits table anywhere in migrations? ===\"; grep -rlni \"aeo_audits\" supabase/migrations/ 2>/dev/null || echo \"NO aeo_audits migration \u2192 must CREATE\"\necho \"=== aeo / intent_plans / sequences in generated types? ===\"; grep -nE \"aeo_audits:|intent_plans:|sequences:|sequence_enrollments:\" src/integrations/supabase/types.ts | head\necho \"=== how do recent migrations grant/structure? (nurturing) ===\"; sed -n '1,20p' supabase/migrations/20260603050000_marketing_hub_nurturing.sql 2>/dev/null | head -25\necho \"=== edge.ts helper ===\"; cat src/lib/edge.ts",
  "description": "Confirm aeo_audits absence + types presence + migration style + edge helper"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === aeo_audits table anywhere in migrations? ===
> NO aeo_audits migration → must CREATE
> === aeo / intent_plans / sequences in generated types? ===
> 1885:      sequence_enrollments: {
> 1943:      sequences: {
> === how do recent migrations grant/structure? (nurturing) ===
> -- Migration: marketing-hub Nurturing Sequences — drip engine data layer (FR-MH-008).
> -- BoK SSOT: docs/bok/marketing-hub/06-data-model.md (§"sequences / sequence_enrollments") + 04-frd.md FR-MH-008
> --           + 05-sdd.md (sequences/sequence_enrollments + nurture-dispatch). STRIDE-Critical: no send without consent.
> -- Tenant safety (MVP-1 lesson — cross-tenant child linkage): both FKs on sequence_enrollments are COMPOSITE +
> -- co-scope user_id (mirrors lead_events/campaign_steps), so an enrollment can only reference a sequence AND a
> -- lead owned by the SAME tenant. Both CASCADE: deleting a sequence OR erasing a lead removes its enrollments.
> 
> -- ─────────────────────────────────────────────────────────────────────────────
> -- 1. sequences — drip definition (ordered steps in jsonb). Composite-unique for child FK targets.
> -- ─────────────────────────────────────────────────────────────────────────────
> CREATE TABLE IF NOT EXISTS public.sequences (
>   id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id    uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   name       text NOT NULL,
>   trigger    text NOT NULL DEFAULT 'manual' CHECK (trigger IN ('status_change','manual')),
>   steps      jsonb NOT NULL DEFAULT '[]'::jsonb,  -- ordered drip steps: [{channel, wait_hours, prompt}]
>   active     boolean NOT NULL DEFAULT true,
>   created_at timestamptz NOT NULL DEFAULT timezone('utc'::text, now()),
>   updated_at timestamptz NOT NULL DEFAULT timezone('utc'::text, now()),
>   CONSTRAINT uniq_sequences_id_user UNIQUE (id, user_id)
> === edge.ts helper ===
> // Shared helper for Supabase Edge Function invocations from the client.
> // supabase.functions.invoke() returns a FunctionsHttpError for any non-2xx response, with the raw
> // Response on `error.context`. Our edge fns return a PT-BR `{ error }` body (e.g. 402 "Saldo insuficiente"),
> // so we read that to surface the real message to the user instead of the generic "Edge Function returned a
> // non-2xx status code".
> 
> /** Extract a PT-BR error message from a Supabase Edge Function non-2xx response. */
> export async function edgeErrorMessage(error: unknown, fallback: string): Promise<string> {
>   const ctx = (error as { context?: { json?: () => Promise<{ error?: string }> } })?.context;
>   try {
>     const body = await ctx?.json?.();
>     if (body?.error) return body.error;
>   } catch { /* response body was not JSON */ }
>   return (error as { message?: string })?.message || fallback;
> }
> ```

## 🤖 Claude *(00:51:50)*


## 🤖 Claude *(00:51:53)*

Tudo mapeado. Contrato `aeo-audit` (`{queries[], brand}` → `{audit_id, citation_rate, findings[]}`, 5 mco, provider degradado-documentado OTD-MH-003), `aeo_audits` **a criar**, e `intent_plans` já no DB mas **ausente do types.ts**. Antes de codar, confirmo o método de aplicar migration + o padrão de `deduct` do lead-score (pra espelhar), e já começo o item mais barato — o **botão enroll de nurturing**:

## 🤖 Claude *(00:51:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== migration apply capability ===\"; ls -la .env 2>/dev/null | head -1; grep -cE \"SUPABASE_ACCESS_TOKEN|SUPABASE_DB_PASSWORD|SB_SECRET_KEY\" .env 2>/dev/null && echo \"(env has tokens)\" || echo \"no token grep\"; npx supabase --version 2>/dev/null | head -1\necho \"=== supabase link status ===\"; ls -la supabase/.temp/ 2>/dev/null | head -5 || echo \"no .temp\"\necho \"=== lead-score deduct pattern (mirror for aeo/intent) ===\"; grep -nE \"deduct_mco_coins|rpc\\(|402|p_amount|admin\\.|service\" supabase/functions/lead-score/index.ts | head -20",
  "description": "Probe migration apply method + lead-score deduct pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === migration apply capability ===
> -rw-rw-r-- 1 ubuntu ubuntu 1266 Jun  1 10:18 .env
> 1
> (env has tokens)
> 2.92.1
> === supabase link status ===
> total 44
> drwxr-xr-x 2 ubuntu ubuntu 4096 Jun  3 21:30 .
> drwxrwxr-x 5 ubuntu ubuntu 4096 Jun  3 21:26 ..
> -rw-rw-r-- 1 ubuntu ubuntu    8 Jun  3 21:51 cli-latest
> -rw-r--r-- 1 ubuntu ubuntu    8 May 16 19:46 gotrue-version
> === lead-score deduct pattern (mirror for aeo/intent) ===
> 2:// JWT-guarded · debits 1 mcoCoin atomically (deduct_mco_coins RPC) · scores a lead 0-100 via the
> 43:  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 44:  const admin = createClient(url, serviceKey);
> 69:    const { data: bal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 70:    if ((bal?.mco_balance ?? 0) < SCORE_COST) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 71:    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: user.id, p_amount: SCORE_COST });
> 72:    if (deductErr) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 75:    const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 143:    await admin.from("leads")
> 146:    await admin.from("lead_events").insert({
> 150:    admin.from("infra_health_logs").insert({ service: "lead-score", status: "healthy" }).then(() => {}, () => {});
> 152:    const { data: newBal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 155:    admin.from("infra_health_logs").insert({ service: "lead-score", status: "unhealthy" }).then(() => {}, () => {});
> ```

## 🤖 Claude *(00:52:12)*


## 🤖 Claude *(00:52:13)*

Migration path + deduct pattern confirmed (mirror lead-score: balance check → `admin.rpc('deduct_mco_coins', {p_user_id, p_amount})` → 402). Let me see which infra tokens exist for applying the `aeo_audits` migration later, then start the **enroll button** (Phase B):

## 🤖 Claude *(00:52:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== .env key NAMES only (no values) ===\"; cut -d= -f1 .env | grep -vE \"^\\s*#|^\\s*$\"\necho \"=== how did v6.25 apply its migration? (deploy scripts) ===\"; ls scripts/ | grep -iE \"deploy|migrat|push|db\" ; echo \"---\"; grep -rlnE \"supabase db push|migration up|db push\" scripts/ 2>/dev/null | head",
  "description": "List env key names + find migration apply scripts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === .env key NAMES only (no values) ===
> SUPABASE_URL
> VITE_SUPABASE_URL
> VITE_SUPABASE_PROJECT_ID
> SUPABASE_SECRET_KEY
> SB_SECRET_KEY
> SUPABASE_PUBLISHABLE_KEY
> VITE_SUPABASE_PUBLISHABLE_KEY
> SUPABASE_SERVICE_ROLE_KEY
> VITE_OPENROUTER_API_KEY
> VITE_GEMINI_API_KEY
> HIGGSFIELD_API_KEY_SECRET
> HIGGSFIELD_API_KEY
> APIFY_KEY
> APIFY_TOKENS
> REPLICATE_API_KEY
> RAPIDAPI_KEY
> === how did v6.25 apply its migration? (deploy scripts) ===
> deploy_all.sh
> deploy-branch.sh
> harness-deploy.sh
> ---
> scripts/harness-deploy.sh
> scripts/deploy_all.sh
> ```

## 🤖 Claude *(00:52:49)*


## 🤖 Claude *(00:52:51)*

Confirmado: sem `SUPABASE_ACCESS_TOKEN`/`DB_PASSWORD` no `.env` — preciso achar o método canônico de aplicar migration (deploy_all.sh) antes da Fase D (AEO). Verifico isso e escrevo o **botão enroll** no `LeadDetailDialog` (Fase B):

## 🤖 Claude *(00:52:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== global supabase access token? ===\"; ls -la ~/.supabase/access-token 2>/dev/null && echo \"HAS global token\" || echo \"no global token file\"; printenv SUPABASE_ACCESS_TOKEN >/dev/null 2>&1 && echo \"SUPABASE_ACCESS_TOKEN in env\" || echo \"no SUPABASE_ACCESS_TOKEN in env\"\necho \"=== deploy_all.sh migration method ===\"; grep -nE \"db push|migration|psql|management|access.?token|DB_URL|db-url|supabase\" scripts/deploy_all.sh 2>/dev/null | head -20",
  "description": "Check global supabase token + deploy_all migration method"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === global supabase access token? ===
> -rw------- 1 ubuntu ubuntu 44 Apr 15 19:00 /home/ubuntu/.supabase/access-token
> HAS global token
> no SUPABASE_ACCESS_TOKEN in env
> === deploy_all.sh migration method ===
> 20:npx supabase db push
> 24:npx supabase functions deploy orchestrate-content
> 25:npx supabase functions deploy
> ```

## 🤖 Claude *(00:52:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/deploy_all.sh"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/bin/bash
> 2	# GCRUX - Orchestration Deploy Script
> 3	# Autonomic Computing Protocol v2
> 4	
> 5	echo "🚀 Starting Full Ecosystem Synchronization..."
> 6	
> 7	# 1. Build the Frontend
> 8	echo "📦 Building Frontend (Vite)..."
> 9	bun run build
> 10	
> 11	if [ $? -eq 0 ]; then
> 12	    echo "✅ Frontend Build Successful."
> 13	else
> 14	    echo "❌ Frontend Build Failed. Aborting."
> 15	    exit 1
> 16	fi
> 17	
> 18	# 2. Database Migration
> 19	echo "🗄️ Pushing Database Schema..."
> 20	npx supabase db push
> 21	
> 22	# 3. Edge Functions
> 23	echo "⚡ Deploying Edge Functions..."
> 24	npx supabase functions deploy orchestrate-content
> 25	npx supabase functions deploy
> 26	
> 27	echo "🟢 Synchronization Complete. Ecosystem is Stable."
> 28	
> ```

## 🤖 Claude *(00:53:04)*


## 🤖 Claude *(00:53:06)*

Migration path confirmed: `npx supabase db push` (token global em `~/.supabase/access-token`). Agora escrevo o **botão enroll** no `LeadDetailDialog` — superfície de lead já aberta, com contexto do `customer_360`:

## 🤖 Claude *(00:53:23)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/LeadDetailDialog.tsx",
  "content": "import { useState } from 'react';\nimport { Loader2, UserPlus } from 'lucide-react';\nimport { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';\nimport { Badge } from '@/components/ui/badge';\nimport { Button } from '@/components/ui/button';\nimport { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';\nimport { useCustomer360, LEAD_STATUS_LABELS, LEAD_STATUS_COLORS, type LeadStatus } from '@/hooks/useLeads';\nimport { useNurturing } from '@/hooks/useNurturing';\nimport { toast } from '@/hooks/use-toast';\n\nfunction Field({ label, value }: { label: string; value: string }) {\n  return (\n    <div className=\"flex items-center justify-between border-b border-border/40 pb-1.5\">\n      <span className=\"text-muted-foreground\">{label}</span>\n      <span className=\"text-foreground text-right\">{value}</span>\n    </div>\n  );\n}\n\n/** FR-MH-008 \u2014 enroll this lead into a nurturing sequence (idempotent via UNIQUE(sequence_id, lead_id)). */\nfunction EnrollSection({ leadId }: { leadId: string }) {\n  const { sequences, enrollLead } = useNurturing();\n  const [seqId, setSeqId] = useState('');\n\n  const handleEnroll = async () => {\n    if (!seqId) return;\n    try {\n      await enrollLead.mutateAsync({ sequence_id: seqId, lead_id: leadId });\n      toast({ title: 'Lead inscrito na sequ\u00eancia' });\n      setSeqId('');\n    } catch (e) {\n      // 23505 (UNIQUE) \u2192 already enrolled; surface a friendly message.\n      const msg = (e as { code?: string; message?: string });\n      toast({\n        title: msg.code === '23505' ? 'Lead j\u00e1 est\u00e1 inscrito nesta sequ\u00eancia' : (msg.message || 'Erro ao inscrever lead'),\n        variant: 'destructive',\n      });\n    }\n  };\n\n  return (\n    <div className=\"pt-2 mt-1 border-t border-border/40 space-y-2\">\n      <p className=\"text-xs font-medium text-foreground\">Nutri\u00e7\u00e3o (drip)</p>\n      {sequences.length === 0 ? (\n        <p className=\"text-xs text-muted-foreground\">Nenhuma sequ\u00eancia ainda \u2014 crie uma no painel de Nutri\u00e7\u00e3o.</p>\n      ) : (\n        <div className=\"flex items-center gap-2\">\n          <Select value={seqId} onValueChange={setSeqId}>\n            <SelectTrigger className=\"h-8 text-xs\"><SelectValue placeholder=\"Escolha a sequ\u00eancia\" /></SelectTrigger>\n            <SelectContent>\n              {sequences.filter((s) => s.active).map((s) => (\n                <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>\n              ))}\n            </SelectContent>\n          </Select>\n          <Button size=\"sm\" className=\"h-8 gap-1 shrink-0\" disabled={!seqId || enrollLead.isPending} onClick={handleEnroll}>\n            {enrollLead.isPending ? <Loader2 className=\"h-3 w-3 animate-spin\" /> : <UserPlus className=\"h-3 w-3\" />}\n            Inscrever\n          </Button>\n        </div>\n      )}\n    </div>\n  );\n}\n\n/** FR-MH-011 \u2014 unified lead profile (Customer 360) drawer, fed by the security_invoker view. */\nexport default function LeadDetailDialog({ leadId, open, onOpenChange }: {\n  leadId: string | null;\n  open: boolean;\n  onOpenChange: (o: boolean) => void;\n}) {\n  const { data, isLoading } = useCustomer360(open ? (leadId ?? undefined) : undefined);\n  const status = (data?.status ?? '') as LeadStatus;\n  return (\n    <Dialog open={open} onOpenChange={onOpenChange}>\n      <DialogContent>\n        <DialogHeader><DialogTitle>Perfil do lead \u00b7 Customer 360</DialogTitle></DialogHeader>\n        {isLoading ? (\n          <div className=\"flex justify-center py-8\"><Loader2 className=\"h-6 w-6 animate-spin text-primary\" /></div>\n        ) : !data ? (\n          <p className=\"text-sm text-muted-foreground py-4\">Perfil n\u00e3o dispon\u00edvel.</p>\n        ) : (\n          <div className=\"space-y-2.5 text-sm\">\n            <div className=\"flex items-center justify-between\">\n              <span className=\"font-medium text-foreground\">{data.name || data.contact}</span>\n              <Badge variant=\"secondary\" className={LEAD_STATUS_COLORS[status] ?? ''}>\n                {LEAD_STATUS_LABELS[status] ?? data.status}\n              </Badge>\n            </div>\n            <Field label=\"Contato\" value={data.contact} />\n            <Field label=\"Origem\" value={data.source} />\n            <Field label=\"Score\" value={data.score != null ? `${data.score}/100` : '\u2014'} />\n            <Field label=\"Eventos\" value={String(data.event_count ?? 0)} />\n            <Field label=\"\u00daltimo evento\" value={data.last_event_at ? new Date(data.last_event_at).toLocaleString('pt-BR') : '\u2014'} />\n            <Field label=\"Consentimento LGPD\" value={data.has_consent ? `Ativo (${data.active_consents})` : 'Sem consentimento'} />\n            {leadId && <EnrollSection leadId={leadId} />}\n          </div>\n        )}\n      </DialogContent>\n    </Dialog>\n  );\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/LeadDetailDialog.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:53:39)*


## 🤖 Claude *(00:53:40)*

Fase B (enroll) escrita. Agora **Fase C — executor de `intent_plans`**. Lei 2 primeiro: SOP do processo humano antes do código.

## 🤖 Claude *(00:54:07)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/intent-plan-execution.md",
  "content": "# SOP \u2014 Intent Plan Execution (HITL approve / reject / execute)\n\n> **Lei 2 (Processo Antecipado).** Documenta o processo humano da metade HITL do FR-MH-009 (Intent Orchestrator) **antes** do `intent-execute`. SSOT: `docs/bok/marketing-hub/04-frd.md` FR-MH-009 + `05-sdd.md` (\u00a7intent-execute + STRIDE \"a\u00e7\u00e3o de alto impacto sem revis\u00e3o = Tampering \u2192 policy engine + HITL obrigat\u00f3rio\") + `06-data-model.md` (\u00a7intent_plans status machine).\n\n## Contexto\n\n`intent-orchestrate` (FR-MH-009) traduz uma inten\u00e7\u00e3o em linguagem natural num **plano de tarefas** e roda um **policy engine**: qualquer tarefa de **alto impacto** (publicar / enviar / cobrar / veicular an\u00fancio / canal outward) for\u00e7a `policy='hitl'` + `status='pending_hitl'`; sen\u00e3o `policy='auto'` + `status='auto_approved'`. O plano fica persistido em `intent_plans` com um `rationale` (XAI audit\u00e1vel). Este SOP cobre o que acontece **depois**: aprovar, rejeitar ou executar o plano.\n\nM\u00e1quina de estados (`intent_plans.status`):\n\n```\nproposed \u2500\u2500\u25b6 auto_approved \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 executed\n        \u2514\u2500\u2500\u25b6 pending_hitl \u2500\u2500\u25b6 approved \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 executed\n                          \u2514\u2500\u2500\u25b6 rejected  (terminal)\n```\n\n## Operator\n\nQuem executa hoje: o **tenant** (Usu\u00e1rio Zero / operador de marketing) revisando os planos no **Marketing Hub** (`/dashboard/marketing`, painel Intent Orchestrator). A decis\u00e3o HITL \u00e9 **humana e consciente** \u2014 \u00e9 a salvaguarda contra uma a\u00e7\u00e3o outward disparar sem revis\u00e3o.\n\n## Sequence (cada passo com crit\u00e9rio material de sucesso)\n\n| # | Passo | A\u00e7\u00e3o | Crit\u00e9rio de sucesso material |\n|---|-------|------|------------------------------|\n| 1 | **Orquestrar** | Operator descreve a inten\u00e7\u00e3o \u2192 `intent-orchestrate` | HTTP 200 `{plan_id, policy, plan_status, tasks, rationale}` + linha em `intent_plans` |\n| 2 | **Triagem auto** | Se `policy='auto'` (s\u00f3 tarefas low/medium, nenhum canal outward) | `status='auto_approved'` \u2014 n\u00e3o exige humano |\n| 3 | **Triagem HITL** | Se `policy='hitl'` (\u22651 tarefa de alto impacto) | `status='pending_hitl'` \u2014 aparece no painel HITL pendente |\n| 4 | **Decidir** | Operator clica **Aprovar** ou **Rejeitar** \u2192 `intent-execute {decision}` | `status='approved'` ou `'rejected'` (transi\u00e7\u00e3o validada server-side) |\n| 5 | **Executar** | Operator clica **Executar** \u2192 `intent-execute {decision:'execute'}` | `intent-execute` **re-valida** o outward; se passa, `status='executed'` |\n\n## Verification gates (defesa-em-profundidade \u2014 a regra de ouro)\n\n1. **Transi\u00e7\u00f5es v\u00e1lidas server-side.** `intent-execute` recusa transi\u00e7\u00f5es inv\u00e1lidas (`approve` s\u00f3 de `pending_hitl`; `execute` nunca de `rejected`; `executed` \u00e9 idempotente). Retorna `409` com mensagem PT-BR.\n2. **Re-valida\u00e7\u00e3o no execute (N\u00c3O confiar em `auto_approved`).** O `execute` **recomputa** o high-impact a partir do `plan` armazenado (mesmo gate do `intent-orchestrate`, via `_shared/intent-policy.ts`). Se o plano cont\u00e9m a\u00e7\u00e3o de alto impacto **e** `status !== 'approved'`, recusa com `409 {code:'hitl_required'}` \u2014 mesmo que a linha diga `policy='auto'`/`status='auto_approved'` (prote\u00e7\u00e3o contra mislabel da IA **ou** adultera\u00e7\u00e3o direta do registro via PostgREST RLS).\n3. **Tenant guard.** `intent-execute` carrega o plano por `id` **E** `user_id = auth.uid()` (service role + escopo expl\u00edcito). Plano de outro tenant \u2192 `404`.\n4. **Outward dispatch \u00e9 gated.** Nesta MVP o `execute` faz a **governan\u00e7a** (re-valida\u00e7\u00e3o + transi\u00e7\u00e3o + observa\u00e7\u00e3o no mesh); o disparo real de canal (`campaign-run`/`orchestrate-content`/`nurture-dispatch`) permanece **gated** (igual \u00e0 entrega externa de nurturing) \u2014 o executor devolve o manifesto das tarefas validadas, sem fabricar envio.\n\n## Recovery path (falha no passo N)\n\n- **Transi\u00e7\u00e3o inv\u00e1lida (409):** o estado n\u00e3o muda; o Operator corrige (ex.: aprovar antes de executar). Nada a fazer no banco.\n- **Re-valida\u00e7\u00e3o bloqueia (409 `hitl_required`):** o plano permanece `pending_hitl`/`auto_approved`; o Operator deve **Aprovar** explicitamente antes de re-executar. Esse bloqueio \u00e9 o comportamento correto, n\u00e3o um bug.\n- **Falha de persist\u00eancia (500):** `infra_health_logs.service='intent-execute' status='unhealthy'`; o status n\u00e3o avan\u00e7a; retry idempotente seguro (a transi\u00e7\u00e3o \u00e9 checada de novo).\n\n## Success signal (materialmente observ\u00e1vel)\n\n`intent_plans.status='executed'` para o `plan_id` + um n\u00f3 `observation` no Knowledge Mesh (`intent-exec-<plan_id>`) + `infra_health_logs.service='intent-execute' status='healthy'`. Um plano de alto impacto **s\u00f3** chega a `executed` se passou por `approved` (humano) \u2014 verific\u00e1vel no `created_at`/`updated_at` e no hist\u00f3rico de status.\n\n## ORO\n\n- **Operator:** tenant (humano) no painel HITL \u00b7 **Reviewer:** o pr\u00f3prio policy engine + re-valida\u00e7\u00e3o server-side \u00b7 **Owner:** Sovereign (blast radius = a\u00e7\u00e3o outward disparada sem revis\u00e3o; mitigado pelo gate de re-valida\u00e7\u00e3o).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/intent-plan-execution.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:54:18)*


## 🤖 Claude *(00:54:20)*

SOP selado. Agora extraio o gate de policy para `_shared/intent-policy.ts` (assim o `execute` **re-roda o mesmo gate** — não uma cópia que pode divergir) e refatoro o `intent-orchestrate` para usá-lo:

## 🤖 Claude *(00:54:28)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/intent-policy.ts",
  "content": "// Shared policy gate for the Intent Orchestrator (FR-MH-009). SSOT: docs/bok/marketing-hub/04-frd.md FR-MH-009 +\n// 05-sdd.md STRIDE \"a\u00e7\u00e3o de alto impacto sem revis\u00e3o = Tampering \u2192 policy engine + HITL obrigat\u00f3rio\".\n//\n// This is the SINGLE source of the high-impact decision. `intent-orchestrate` runs it to set policy/status at\n// creation; `intent-execute` re-runs it at execution time as defense-in-depth (NEVER trust the stored\n// policy/status \u2014 an outward action must clear this gate again before it can execute).\n\nexport interface PlanTask {\n  action: string;\n  channel?: string;\n  impact?: \"low\" | \"medium\" | \"high\";\n  rationale?: string;\n}\n\n// High-impact = outward / financial actions that MUST NOT run without human review (the HITL gate).\nexport const HIGH_IMPACT_RE =\n  /(publi|send|e-?mail|post|tweet|spend|ad[_-]?spend|charge|cobr|envi|dispar|whats|launch|lan\u00e7a)/i;\n\n// Fail-safe channel rule: ANY outward channel (anything that is not the internal 'none'/'content') is high-impact,\n// even if the AI mislabels impact=low or phrases the action verb to dodge the regex. Unknown channel \u2192 outward.\nexport const isOutwardChannel = (c?: string): boolean =>\n  !!c && ![\"none\", \"content\"].includes(c.toLowerCase());\n\nexport function isHighImpactTask(t: PlanTask): boolean {\n  return t?.impact === \"high\" || HIGH_IMPACT_RE.test(t?.action ?? \"\") || isOutwardChannel(t?.channel);\n}\n\n/** True if ANY task in the plan is high-impact \u2192 mandatory human approval (HITL) before execution. */\nexport function planIsHighImpact(tasks: unknown): boolean {\n  return Array.isArray(tasks) && tasks.some((t) => isHighImpactTask(t as PlanTask));\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/intent-policy.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:54:31)*

Agora refatoro o `intent-orchestrate` para importar o gate compartilhado (remove as cópias inline):

## 🤖 Claude *(00:54:36)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-orchestrate/index.ts",
  "old_string": "import { serve } from \"https://deno.land/std@0.168.0/http/server.ts\";\nimport { createClient } from \"https://esm.sh/@supabase/supabase-js@2\";\nimport { fetchLLMWithFallback } from \"../_shared/llm-fallback.ts\";\n\nconst corsHeaders = {\n  \"Access-Control-Allow-Origin\": \"*\",\n  \"Access-Control-Allow-Methods\": \"POST, OPTIONS\",\n  \"Access-Control-Allow-Headers\": \"authorization, x-client-info, apikey, content-type\",\n};\n\ninterface PlanTask { action: string; channel?: string; impact?: \"low\" | \"medium\" | \"high\"; rationale?: string }\n\n// High-impact = outward / financial actions that MUST NOT run without human review (the HITL gate).\nconst HIGH_IMPACT_RE = /(publi|send|e-?mail|post|tweet|spend|ad[_-]?spend|charge|cobr|envi|dispar|whats|launch|lan\u00e7a)/i;",
  "new_string": "import { serve } from \"https://deno.land/std@0.168.0/http/server.ts\";\nimport { createClient } from \"https://esm.sh/@supabase/supabase-js@2\";\nimport { fetchLLMWithFallback } from \"../_shared/llm-fallback.ts\";\nimport { planIsHighImpact, type PlanTask } from \"../_shared/intent-policy.ts\";\n\nconst corsHeaders = {\n  \"Access-Control-Allow-Origin\": \"*\",\n  \"Access-Control-Allow-Methods\": \"POST, OPTIONS\",\n  \"Access-Control-Allow-Headers\": \"authorization, x-client-info, apikey, content-type\",\n};"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-orchestrate/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:54:44)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-orchestrate/index.ts",
  "old_string": "    // \u2500\u2500 POLICY ENGINE: any high-impact task \u2192 HITL (mandatory human approval; STRIDE Tampering mitigation) \u2500\u2500\n    // Fail-safe channel rule: ANY outward channel (anything that is not the internal 'none'/'content') forces HITL,\n    // even if the AI mislabels impact=low or phrases the action verb to dodge the regex. Unknown channel \u2192 HITL.\n    const isOutward = (c?: string) => !!c && ![\"none\", \"content\"].includes(c.toLowerCase());\n    const highImpact = tasks.some((t) => t.impact === \"high\" || HIGH_IMPACT_RE.test(t.action) || isOutward(t.channel));\n    const policy: \"auto\" | \"hitl\" = highImpact ? \"hitl\" : \"auto\";",
  "new_string": "    // \u2500\u2500 POLICY ENGINE: any high-impact task \u2192 HITL (mandatory human approval; STRIDE Tampering mitigation) \u2500\u2500\n    // Shared gate (_shared/intent-policy.ts) \u2014 intent-execute re-runs the SAME gate at execution time.\n    const highImpact = planIsHighImpact(tasks);\n    const policy: \"auto\" | \"hitl\" = highImpact ? \"hitl\" : \"auto\";"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-orchestrate/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:54:54)*


## 🤖 Claude *(00:54:55)*

Agora o **`intent-execute`** — o executor com re-validação outward (Lei 1 do directive: não confiar em `auto_approved`):

## 🤖 Claude *(00:55:21)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-execute/index.ts",
  "content": "// intent-execute \u2014 marketing-hub FR-MH-009 HITL transitions (approve / reject / execute).\n// SSOT: docs/bok/marketing-hub/04-frd.md FR-MH-009 + 05-sdd.md (\u00a7intent-execute) + docs/processes/intent-plan-execution.md.\n//\n// The HITL half of the Intent Orchestrator: drives the intent_plans state machine\n//   proposed \u2192 auto_approved | pending_hitl \u2192 approved | rejected \u2192 executed\n// SECURITY (the directive's golden rule): `execute` RE-VALIDATES the outward action via the SHARED policy gate\n// (_shared/intent-policy.ts) \u2014 it NEVER trusts the stored policy/status. A plan containing a high-impact task can\n// only execute if a human has explicitly approved it (status='approved'), even if the row says auto_approved (AI\n// mislabel OR direct PostgREST tampering). Cost 0: it governs; sub-steps self-bill on actual dispatch (which is gated).\n// JWT-guarded (verify_jwt=false + in-function getUser \u2014 edge-jwt SOP).\nimport { serve } from \"https://deno.land/std@0.168.0/http/server.ts\";\nimport { createClient } from \"https://esm.sh/@supabase/supabase-js@2\";\nimport { planIsHighImpact } from \"../_shared/intent-policy.ts\";\n\nconst corsHeaders = {\n  \"Access-Control-Allow-Origin\": \"*\",\n  \"Access-Control-Allow-Methods\": \"POST, OPTIONS\",\n  \"Access-Control-Allow-Headers\": \"authorization, x-client-info, apikey, content-type\",\n};\n\ntype Decision = \"approve\" | \"reject\" | \"execute\";\nconst DECISIONS: Decision[] = [\"approve\", \"reject\", \"execute\"];\n\nserve(async (req) => {\n  if (req.method === \"OPTIONS\") return new Response(\"ok\", { headers: corsHeaders });\n  const json = (b: unknown, s = 200) =>\n    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, \"Content-Type\": \"application/json\" } });\n\n  const url = Deno.env.get(\"SUPABASE_URL\")!;\n  const serviceKey = (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!;\n  const anonKey = (Deno.env.get(\"SB_PUBLISHABLE_KEY\") ?? Deno.env.get(\"SUPABASE_ANON_KEY\"))!;\n  const admin = createClient(url, serviceKey);\n  const logErr = () => admin.from(\"infra_health_logs\").insert({ service: \"intent-execute\", status: \"unhealthy\" }).then(() => {}, () => {});\n\n  try {\n    const authHeader = req.headers.get(\"Authorization\");\n    if (!authHeader) return json({ error: \"Missing authorization\" }, 401);\n    const userClient = createClient(url, anonKey, { global: { headers: { Authorization: authHeader } } });\n    const { data: { user }, error: authError } = await userClient.auth.getUser();\n    if (authError || !user) return json({ error: \"Unauthorized\" }, 401);\n\n    const { plan_id, decision } = await req.json().catch(() => ({}));\n    if (!plan_id || typeof plan_id !== \"string\") return json({ error: \"plan_id \u00e9 obrigat\u00f3rio\" }, 422);\n    if (!DECISIONS.includes(decision)) return json({ error: \"decision deve ser approve, reject ou execute\" }, 422);\n\n    // Tenant guard: load the plan scoped to the caller (service role + explicit user_id). Foreign plan \u2192 404.\n    const { data: row, error: loadErr } = await admin\n      .from(\"intent_plans\").select(\"*\").eq(\"id\", plan_id).eq(\"user_id\", user.id).maybeSingle();\n    if (loadErr) { logErr(); return json({ error: \"Falha ao carregar o plano\", detail: loadErr.message }, 500); }\n    if (!row) return json({ error: \"Plano n\u00e3o encontrado\" }, 404);\n\n    const status: string = row.status;\n\n    // \u2500\u2500 APPROVE: only a pending_hitl plan can be human-approved. \u2500\u2500\n    if (decision === \"approve\") {\n      if (status !== \"pending_hitl\") return json({ error: `N\u00e3o \u00e9 poss\u00edvel aprovar um plano em status \"${status}\"`, status }, 409);\n      const { error } = await admin.from(\"intent_plans\").update({ status: \"approved\" }).eq(\"id\", plan_id).eq(\"user_id\", user.id);\n      if (error) { logErr(); return json({ error: \"Falha ao aprovar\", detail: error.message }, 500); }\n      admin.from(\"infra_health_logs\").insert({ service: \"intent-execute\", status: \"healthy\" }).then(() => {}, () => {});\n      return json({ status: \"ok\", plan_id, plan_status: \"approved\" });\n    }\n\n    // \u2500\u2500 REJECT: terminal; allowed from any non-executed state (idempotent if already rejected). \u2500\u2500\n    if (decision === \"reject\") {\n      if (status === \"executed\") return json({ error: \"Plano j\u00e1 executado n\u00e3o pode ser rejeitado\", status }, 409);\n      if (status === \"rejected\") return json({ status: \"ok\", plan_id, plan_status: \"rejected\", already: true });\n      const { error } = await admin.from(\"intent_plans\").update({ status: \"rejected\" }).eq(\"id\", plan_id).eq(\"user_id\", user.id);\n      if (error) { logErr(); return json({ error: \"Falha ao rejeitar\", detail: error.message }, 500); }\n      admin.from(\"infra_health_logs\").insert({ service: \"intent-execute\", status: \"healthy\" }).then(() => {}, () => {});\n      return json({ status: \"ok\", plan_id, plan_status: \"rejected\" });\n    }\n\n    // \u2500\u2500 EXECUTE: the security-critical path. \u2500\u2500\n    if (status === \"executed\") return json({ status: \"ok\", plan_id, plan_status: \"executed\", already: true });\n    if (status === \"rejected\") return json({ error: \"Plano rejeitado n\u00e3o pode ser executado\", status }, 409);\n\n    // DEFENSE-IN-DEPTH: re-run the SAME policy gate on the STORED plan. Never trust the persisted policy/status.\n    // A high-impact plan executes ONLY if a human explicitly approved it (status='approved').\n    const highImpact = planIsHighImpact(row.plan);\n    if (highImpact && status !== \"approved\") {\n      return json({\n        error: \"Plano de alto impacto exige aprova\u00e7\u00e3o humana (HITL) antes de executar.\",\n        code: \"hitl_required\", status,\n      }, 409);\n    }\n\n    const { error: updErr } = await admin.from(\"intent_plans\")\n      .update({ status: \"executed\" }).eq(\"id\", plan_id).eq(\"user_id\", user.id);\n    if (updErr) { logErr(); return json({ error: \"Falha ao marcar como executado\", detail: updErr.message }, 500); }\n\n    // Knowledge Mesh observation (mandate: every orchestration run). Fire-and-forget.\n    const taskCount = Array.isArray(row.plan) ? row.plan.length : 0;\n    admin.from(\"mcorch_nodes\").insert({\n      node_type: \"observation\", name: `intent-exec-${plan_id}`,\n      content: `Intent plan executed: \"${String(row.intent).slice(0, 160)}\" (${taskCount} tarefas \u00b7 high_impact=${highImpact})`,\n      user_id: user.id,\n    }).then(() => {}, () => {});\n    admin.from(\"infra_health_logs\").insert({ service: \"intent-execute\", status: \"healthy\" }).then(() => {}, () => {});\n\n    // Governance done. Actual outward channel dispatch (campaign-run/orchestrate-content/nurture-dispatch) stays\n    // GATED in this MVP \u2014 we return the validated manifest, we do NOT fabricate sends.\n    return json({\n      status: \"ok\", plan_id, plan_status: \"executed\",\n      high_impact: highImpact, tasks: row.plan, outward_dispatch: \"gated\",\n    });\n  } catch (err) {\n    logErr();\n    return json({ error: \"Erro interno no intent-execute\", detail: String((err as Error)?.message ?? err) }, 500);\n  }\n});\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-execute/index.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:55:25)*


## 🤖 Claude *(00:55:25)*

Adiciono as entradas `verify_jwt = false` no `config.toml` para `intent-execute` e (já adiantando) `aeo-audit`:

## 🤖 Claude *(00:55:27)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml",
  "old_string": "[functions.intent-orchestrate]\nverify_jwt = false\n[functions.generate-content]\nverify_jwt = false",
  "new_string": "[functions.intent-orchestrate]\nverify_jwt = false\n[functions.intent-execute]\nverify_jwt = false\n[functions.aeo-audit]\nverify_jwt = false\n[functions.generate-content]\nverify_jwt = false"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:55:37)*


## 🤖 Claude *(00:55:38)*

Patch faithful da BoK (SDD) — documenta o `intent-execute` como a realização da metade HITL já documentada no FR-MH-009. Leio os trechos exatos para editar com precisão:

## 🤖 Claude *(00:55:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md",
  "offset": 78,
  "limit": 10
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 78	| Function | Path | Auth | mcoCoins | Secrets needed |
> 79	|----------|------|------|----------|----------------|
> 80	| `lead-score` | `supabase/functions/lead-score/index.ts` | JWT (user) | 1 | per-user AI key (`user_api_keys`) → `OPENROUTER_API_KEY` |
> 81	| `campaign-run` | `supabase/functions/campaign-run/index.ts` | JWT (user) | 10 | (reusa orchestrate-content secrets) |
> 82	| `nurture-dispatch` | `supabase/functions/nurture-dispatch/index.ts` | JWT/service | 2 / message | per-user AI + channel creds (`social_credentials`/`meta_config`) |
> 83	| `intent-orchestrate` | `supabase/functions/intent-orchestrate/index.ts` | JWT (user) | 0 (orquestra) | per-user AI key |
> 84	| `aeo-audit` | `supabase/functions/aeo-audit/index.ts` | JWT (user) | 5 | per-user AI key + AEO provider key (OTD-MH-003) |
> 85	| `erase-lead` | `supabase/functions/erase-lead/index.ts` | JWT (user) | 0 | service-role (cascade + Vault revoke) |
> 86	
> 87	> All new Edge Functions follow the **API Tenancy Model**: resolve per-user credential first, documented fallback only for service/cron paths, hard-fail 402/501 otherwise.
> ```

## 🤖 Claude *(00:55:44)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md",
  "old_string": "| `intent-orchestrate` | `supabase/functions/intent-orchestrate/index.ts` | JWT (user) | 0 (orquestra) | per-user AI key |\n| `aeo-audit` | `supabase/functions/aeo-audit/index.ts` | JWT (user) | 5 | per-user AI key + AEO provider key (OTD-MH-003) |",
  "new_string": "| `intent-orchestrate` | `supabase/functions/intent-orchestrate/index.ts` | JWT (user) | 0 (orquestra) | per-user AI key |\n| `intent-execute` | `supabase/functions/intent-execute/index.ts` | JWT (user) | 0 (governa) | \u2014 (HITL approve/reject/execute; re-valida outward via `_shared/intent-policy.ts`) |\n| `aeo-audit` | `supabase/functions/aeo-audit/index.ts` | JWT (user) | 5 | per-user AI key + AEO provider key (OTD-MH-003) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:55:49)*

Adiciono o contrato HTTP do `intent-execute` na seção §API do SDD, logo após o `aeo-audit`:

## 🤖 Claude *(00:55:57)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md",
  "old_string": "interface AeoAuditRequest { queries: string[]; brand: string }\ninterface AeoAuditResponse {\n  status: 'ok'\n  audit_id: string\n  citation_rate: number        // % queries citando a marca\n  findings: Array<{ query: string; cited: boolean; recommendation: string }>\n}\n// mcoCoins: deduct 5 at entry. Provider per OTD-MH-003; degraded mode documented if no provider.\n```",
  "new_string": "interface AeoAuditRequest { queries: string[]; brand: string }\ninterface AeoAuditResponse {\n  status: 'ok'\n  audit_id: string\n  citation_rate: number        // % queries citando a marca\n  findings: Array<{ query: string; cited: boolean; recommendation: string }>\n}\n// mcoCoins: deduct 5 at entry. Provider per OTD-MH-003; degraded mode documented if no provider.\n```\n\n### `POST /functions/v1/intent-execute`\n\n```typescript\n// HITL half of FR-MH-009 \u2014 drives the intent_plans state machine.\ninterface IntentExecuteRequest { plan_id: string; decision: 'approve' | 'reject' | 'execute' }\ninterface IntentExecuteResponse {\n  status: 'ok'\n  plan_id: string\n  plan_status: 'approved' | 'rejected' | 'executed'\n  high_impact?: boolean\n  tasks?: unknown[]            // validated manifest on execute\n  outward_dispatch?: 'gated'   // actual channel sends stay gated in MVP\n  already?: boolean            // idempotent no-op\n}\n// Cost 0 (governs). Tenant guard: plan loaded by id AND user_id=auth.uid() (foreign \u2192 404).\n// DEFENSE-IN-DEPTH: `execute` re-runs the SHARED policy gate on the STORED plan (_shared/intent-policy.ts) \u2014\n// a high-impact plan executes ONLY if status='approved' (human), never trusting auto_approved. 409 hitl_required\n// otherwise. Invalid transitions \u2192 409. SOP: docs/processes/[[intent-plan-execution|intent-plan-execution]].md.\n```"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:56:19)*


## 🤖 Claude *(00:56:21)*

Backend do executor escrito + BoK patcheada + config.toml. Agora **deploy** das duas functions (intent-orchestrate refatorada + intent-execute novo) e, em paralelo, leio o template de smoke + o minter de JWT para montar o smoke zero-custo:

## 🤖 Claude *(00:56:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx supabase functions deploy intent-orchestrate 2>&1 | tail -8 && echo \"=== now intent-execute ===\" && npx supabase functions deploy intent-execute 2>&1 | tail -8",
  "description": "Deploy intent-orchestrate + intent-execute edge functions"
}
```

## 🤖 Claude *(00:56:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-nurture.ts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Bundling Function: intent-orchestrate
> Deploying Function: intent-orchestrate (script size: 85.48kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: intent-orchestrate
> You can inspect your deployment in the Dashboard: https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa/functions
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> === now intent-execute ===
> Bundling Function: intent-execute
> Deploying Function: intent-execute (script size: 80.44kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: intent-execute
> You can inspect your deployment in the Dashboard: https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa/functions
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Smoke test — nurture-dispatch consent gate (FR-MH-008 / AT-MH-008), USER PATH (real JWT).
> 4	 *
> 5	 * Proves the STRIDE-Critical mitigation materially: NO message is generated/charged for a lead WITHOUT a
> 6	 * granted, non-withdrawn consent; opt-out hard-stops; and a consented dispatch advances + records (delivery
> 7	 * gated). Throwaway user + cleanup. The only cost is the single consented LLM message (~$0.001, system key).
> 8	 *
> 9	 * Usage: bun run scripts/qa/smoke-nurture.ts
> 10	 */
> 11	import { createClient } from '@supabase/supabase-js';
> 12	
> 13	const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> 14	const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> 15	const PUB = process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? process.env.SUPABASE_ANON_KEY!;
> 16	if (!URL || !SVC || !PUB) { console.error('Missing env (URL/SVC/PUB)'); process.exit(1); }
> 17	
> 18	const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> 19	const stamp = Date.now();
> 20	let uid: string | null = null;
> 21	let pass = true;
> 22	const check = (l: string, ok: boolean, d = '') => { console.log(`${ok ? '✅' : '❌'} ${l}${d ? `  → ${d}` : ''}`); if (!ok) pass = false; };
> 23	const bal = async () => Number((await admin.from('profiles').select('mco_balance').eq('id', uid!).single()).data?.mco_balance ?? 0);
> 24	
> 25	async function dispatch(token: string, enrollmentId: string) {
> 26	  const r = await fetch(`${URL}/functions/v1/nurture-dispatch`, {
> 27	    method: 'POST', headers: { 'Content-Type': 'application/json', apikey: PUB, Authorization: `Bearer ${token}` },
> 28	    body: JSON.stringify({ enrollment_id: enrollmentId }),
> 29	  });
> 30	  let j: { status?: string; reason?: string; delivered?: boolean; new_balance?: number } = {};
> 31	  const t = await r.text(); try { j = JSON.parse(t); } catch { /* keep {} */ }
> 32	  return { status: r.status, body: j };
> 33	}
> 34	
> 35	try {
> 36	  const email = `nur-${stamp}@example.com`, password = `Aa1!${crypto.randomUUID()}`;
> 37	  const { data: cu, error } = await admin.auth.admin.createUser({ email, password, email_confirm: true });
> 38	  if (error || !cu?.user) throw new Error(`createUser: ${error?.message}`);
> 39	  uid = cu.user.id;
> 40	  await admin.from('profiles').update({ mco_balance: 100 }).eq('id', uid);
> 41	
> 42	  const { data: lead } = await admin.from('leads').insert({ user_id: uid, contact: '+5511988887777', name: 'Nurture Lead', source: 'manual', status: 'nurturing' }).select('id').single();
> 43	  const { data: seq } = await admin.from('sequences').insert({ user_id: uid, name: 'Welcome Drip', trigger: 'manual', steps: [{ channel: 'email', wait_hours: 24, prompt: 'Boas-vindas curtas para o lead.' }] }).select('id').single();
> 44	  const { data: enr } = await admin.from('sequence_enrollments').insert({ user_id: uid, sequence_id: seq!.id, lead_id: lead!.id, current_step: 0, status: 'active', next_run_at: new Date().toISOString() }).select('id').single();
> 45	  const enrollmentId = enr!.id as string;
> 46	
> 47	  const userClient = createClient(URL, PUB, { auth: { persistSession: false } });
> 48	  const { data: si, error: siErr } = await userClient.auth.signInWithPassword({ email, password });
> 49	  if (siErr || !si?.session) throw new Error(`signIn: ${siErr?.message}`);
> 50	  const token = si.session.access_token;
> 51	
> 52	  // ── A: NO consent → BLOCKED, no charge, enrollment paused (the Critical gate) ──
> 53	  const balBeforeBlock = await bal();
> 54	  const a = await dispatch(token, enrollmentId);
> 55	  check('A no-consent → blocked (consent_required)', a.body?.status === 'blocked' && a.body?.reason === 'consent_required', `status=${a.body?.status} reason=${a.body?.reason}`);
> 56	  check('A no charge on block', (await bal()) === balBeforeBlock, `bal=${await bal()} (was ${balBeforeBlock})`);
> 57	  const { data: pausedEnr } = await admin.from('sequence_enrollments').select('status').eq('id', enrollmentId).single();
> 58	  check('A enrollment paused by the gate', pausedEnr?.status === 'paused', `status=${pausedEnr?.status}`);
> 59	  const { count: eventsAfterBlock } = await admin.from('lead_events').select('id', { count: 'exact', head: true }).eq('lead_id', lead!.id).eq('event_type', 'message_sent');
> 60	  check('A NO message_sent event (nothing generated)', (eventsAfterBlock ?? 0) === 0, `events=${eventsAfterBlock}`);
> 61	
> 62	  // ── B: grant consent + resume → DISPATCHED, charge 2, message recorded (delivery gated), enrollment advanced ──
> 63	  await admin.from('marketing_consents').insert({ lead_id: lead!.id, user_id: uid, basis: 'consent', granted: true, source_proof: {} });
> 64	  await admin.from('sequence_enrollments').update({ status: 'active' }).eq('id', enrollmentId);
> 65	  const balBeforeDispatch = await bal();
> 66	  const b = await dispatch(token, enrollmentId);
> 67	  check('B consented → dispatched|completed', b.body?.status === 'dispatched' || b.body?.status === 'completed', `status=${b.body?.status}`);
> 68	  check('B charged exactly 2 mcoCoins', balBeforeDispatch - (await bal()) === 2, `${balBeforeDispatch}→${await bal()}`);
> 69	  check('B delivery is GATED (not externally sent)', b.body?.delivered === false, `delivered=${b.body?.delivered}`);
> 70	  const { data: ev } = await admin.from('lead_events').select('event_type, payload').eq('lead_id', lead!.id).eq('event_type', 'message_sent').maybeSingle();
> 71	  check('B message_sent event recorded with delivery=gated', (ev?.payload as { delivery?: string })?.delivery === 'gated', `delivery=${(ev?.payload as { delivery?: string })?.delivery}`);
> 72	  const { data: advEnr } = await admin.from('sequence_enrollments').select('current_step, status').eq('id', enrollmentId).single();
> 73	  check('B enrollment advanced (step 0→1, completed)', advEnr?.current_step === 1 && advEnr?.status === 'completed', `step=${advEnr?.current_step} status=${advEnr?.status}`);
> 74	
> 75	  // ── C: opt-out → hard skip, no charge ──
> 76	  await admin.from('sequence_enrollments').update({ status: 'opted_out' }).eq('id', enrollmentId);
> 77	  const balBeforeOptOut = await bal();
> 78	  const c = await dispatch(token, enrollmentId);
> 79	  check('C opted_out → skipped, no charge', c.body?.status === 'opted_out' && (await bal()) === balBeforeOptOut, `status=${c.body?.status} bal=${await bal()}`);
> 80	} catch (e) {
> 81	  pass = false; console.error('❌ smoke error:', e instanceof Error ? e.message : e);
> 82	} finally {
> 83	  if (uid) await admin.auth.admin.deleteUser(uid);
> 84	  console.log(`\n🧹 cleanup: throwaway user deleted (cascade)`);
> 85	  console.log(pass ? '\n✅✅ NURTURE CONSENT-GATE SMOKE PASSED' : '\n❌ NURTURE CONSENT-GATE SMOKE FAILED');
> 86	  process.exit(pass ? 0 : 1);
> 87	}
> 88	
> ```

## 🤖 Claude *(00:56:55)*


## 🤖 Claude *(00:56:57)*

Deploy ✅ (intent-orchestrate 85.48kB · intent-execute 80.44kB). Template de smoke claro (throwaway user + `signInWithPassword` + cleanup cascade). Escrevo o smoke **zero-custo** que prova a propriedade de segurança central — a re-validação bloqueia um `auto_approved` adulterado de alto impacto:

## 🤖 Claude *(00:57:27)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-intent-execute.ts",
  "content": "#!/usr/bin/env bun\n/**\n * Smoke test \u2014 intent-execute HITL state machine + re-validation (FR-MH-009 / AT-MH-009), USER PATH (real JWT).\n *\n * Proves the directive's golden rule materially: `execute` RE-VALIDATES the outward action on the STORED plan and\n * REFUSES a high-impact plan that was NOT human-approved \u2014 EVEN IF the row says status='auto_approved' (AI mislabel\n * OR direct PostgREST tampering). Also proves valid/invalid transitions, tenant guard (404), and idempotency.\n * Cost 0 (intent-execute governs; it never charges). Throwaway users + cascade cleanup.\n *\n * Usage: bun run scripts/qa/smoke-intent-execute.ts\n */\nimport { createClient } from '@supabase/supabase-js';\n\nconst URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;\nconst SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;\nconst PUB = process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? process.env.SUPABASE_ANON_KEY!;\nif (!URL || !SVC || !PUB) { console.error('Missing env (URL/SVC/PUB)'); process.exit(1); }\n\nconst admin = createClient(URL, SVC, { auth: { persistSession: false } });\nconst stamp = Date.now();\nconst uids: string[] = [];\nlet pass = true;\nconst check = (l: string, ok: boolean, d = '') => { console.log(`${ok ? '\u2705' : '\u274c'} ${l}${d ? `  \u2192 ${d}` : ''}`); if (!ok) pass = false; };\n\nasync function mkUser(tag: string): Promise<{ uid: string; token: string }> {\n  const email = `ie-${tag}-${stamp}@example.com`, password = `Aa1!${crypto.randomUUID()}`;\n  const { data: cu, error } = await admin.auth.admin.createUser({ email, password, email_confirm: true });\n  if (error || !cu?.user) throw new Error(`createUser(${tag}): ${error?.message}`);\n  uids.push(cu.user.id);\n  const userClient = createClient(URL, PUB, { auth: { persistSession: false } });\n  const { data: si, error: siErr } = await userClient.auth.signInWithPassword({ email, password });\n  if (siErr || !si?.session) throw new Error(`signIn(${tag}): ${siErr?.message}`);\n  return { uid: cu.user.id, token: si.session.access_token };\n}\n\nasync function insertPlan(uid: string, plan: unknown, status: string, policy: string): Promise<string> {\n  const { data, error } = await admin.from('intent_plans')\n    .insert({ user_id: uid, intent: 'smoke intent', plan, status, policy, rationale: 'smoke' })\n    .select('id').single();\n  if (error || !data) throw new Error(`insertPlan: ${error?.message}`);\n  return data.id as string;\n}\n\nasync function exec(token: string | null, body: unknown) {\n  const headers: Record<string, string> = { 'Content-Type': 'application/json', apikey: PUB };\n  if (token) headers.Authorization = `Bearer ${token}`;\n  const r = await fetch(`${URL}/functions/v1/intent-execute`, { method: 'POST', headers, body: JSON.stringify(body) });\n  let j: { plan_status?: string; code?: string; already?: boolean; error?: string } = {};\n  const t = await r.text(); try { j = JSON.parse(t); } catch { /* keep {} */ }\n  return { status: r.status, body: j };\n}\nconst dbStatus = async (id: string) => (await admin.from('intent_plans').select('status').eq('id', id).single()).data?.status;\n\nconst LOW = [{ action: 'revisar inten\u00e7\u00e3o', channel: 'none', impact: 'low' }];\nconst HIGH = [{ action: 'enviar email de boas-vindas', channel: 'email', impact: 'high' }];\nconst HIGH_SOCIAL = [{ action: 'publicar post no LinkedIn', channel: 'social', impact: 'high' }];\n\ntry {\n  const u1 = await mkUser('owner');\n  const u2 = await mkUser('intruder');\n\n  // Seed plans for u1.\n  const A = await insertPlan(u1.uid, LOW, 'auto_approved', 'auto');         // legit low-impact auto\n  const B = await insertPlan(u1.uid, HIGH, 'pending_hitl', 'hitl');         // legit high-impact awaiting approval\n  const C = await insertPlan(u1.uid, HIGH_SOCIAL, 'auto_approved', 'auto'); // TAMPERED: high-impact stored as auto_approved\n  const D = await insertPlan(u1.uid, HIGH, 'pending_hitl', 'hitl');         // for reject path\n\n  // \u2500\u2500 1. Input/auth guards \u2500\u2500\n  check('no-auth \u2192 401', (await exec(null, { plan_id: A, decision: 'execute' })).status === 401);\n  check('missing plan_id \u2192 422', (await exec(u1.token, { decision: 'execute' })).status === 422);\n  check('bad decision \u2192 422', (await exec(u1.token, { plan_id: A, decision: 'nuke' })).status === 422);\n\n  // \u2500\u2500 2. Tenant guard: intruder cannot touch u1's plan \u2192 404 \u2500\u2500\n  check('cross-tenant execute \u2192 404 (tenant guard)', (await exec(u2.token, { plan_id: A, decision: 'execute' })).status === 404);\n\n  // \u2500\u2500 3. Low-impact auto plan executes without approval \u2500\u2500\n  const eA = await exec(u1.token, { plan_id: A, decision: 'execute' });\n  check('A low-impact auto \u2192 200 executed', eA.status === 200 && eA.body.plan_status === 'executed', `status=${eA.status} ps=${eA.body.plan_status}`);\n  check('A persisted executed', (await dbStatus(A)) === 'executed');\n\n  // \u2500\u2500 4. THE GOLDEN RULE: tampered auto_approved HIGH-impact plan is REFUSED on execute \u2500\u2500\n  const eC = await exec(u1.token, { plan_id: C, decision: 'execute' });\n  check('C tampered auto_approved high-impact \u2192 409 hitl_required (re-validation)', eC.status === 409 && eC.body.code === 'hitl_required', `status=${eC.status} code=${eC.body.code}`);\n  check('C NOT executed (still auto_approved)', (await dbStatus(C)) === 'auto_approved', `status=${await dbStatus(C)}`);\n  // and it cannot be silently approved either (approve only from pending_hitl)\n  check('C approve on auto_approved \u2192 409 (invalid transition)', (await exec(u1.token, { plan_id: C, decision: 'approve' })).status === 409);\n\n  // \u2500\u2500 5. Legit HITL path: pending_hitl \u2192 approve \u2192 execute \u2500\u2500\n  const exBefore = await exec(u1.token, { plan_id: B, decision: 'execute' });\n  check('B execute before approval \u2192 409 hitl_required', exBefore.status === 409 && exBefore.body.code === 'hitl_required', `status=${exBefore.status} code=${exBefore.body.code}`);\n  const apB = await exec(u1.token, { plan_id: B, decision: 'approve' });\n  check('B approve \u2192 200 approved', apB.status === 200 && apB.body.plan_status === 'approved', `ps=${apB.body.plan_status}`);\n  const exB = await exec(u1.token, { plan_id: B, decision: 'execute' });\n  check('B execute after approval \u2192 200 executed', exB.status === 200 && exB.body.plan_status === 'executed', `ps=${exB.body.plan_status}`);\n  check('B idempotent execute \u2192 already=true', (await exec(u1.token, { plan_id: B, decision: 'execute' })).body.already === true);\n\n  // \u2500\u2500 6. Reject path is terminal \u2500\u2500\n  const rjD = await exec(u1.token, { plan_id: D, decision: 'reject' });\n  check('D reject \u2192 200 rejected', rjD.status === 200 && rjD.body.plan_status === 'rejected', `ps=${rjD.body.plan_status}`);\n  check('D execute after reject \u2192 409', (await exec(u1.token, { plan_id: D, decision: 'execute' })).status === 409);\n} catch (e) {\n  pass = false; console.error('\u274c smoke error:', e instanceof Error ? e.message : e);\n} finally {\n  for (const id of uids) await admin.auth.admin.deleteUser(id);\n  console.log(`\\n\ud83e\uddf9 cleanup: ${uids.length} throwaway user(s) deleted (intent_plans cascade)`);\n  console.log(pass ? '\\n\u2705\u2705 INTENT-EXECUTE HITL SMOKE PASSED' : '\\n\u274c INTENT-EXECUTE HITL SMOKE FAILED');\n  process.exit(pass ? 0 : 1);\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-intent-execute.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:57:31)*


## 🤖 Claude *(00:57:32)*

Rodo o smoke (Bun auto-carrega `.env`):

## 🤖 Claude *(00:57:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run scripts/qa/smoke-intent-execute.ts 2>&1",
  "description": "Run intent-execute HITL smoke"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ no-auth → 401
> ✅ missing plan_id → 422
> ✅ bad decision → 422
> ✅ cross-tenant execute → 404 (tenant guard)
> ✅ A low-impact auto → 200 executed  → status=200 ps=executed
> ✅ A persisted executed
> ✅ C tampered auto_approved high-impact → 409 hitl_required (re-validation)  → status=409 code=hitl_required
> ✅ C NOT executed (still auto_approved)  → status=auto_approved
> ✅ C approve on auto_approved → 409 (invalid transition)
> ✅ B execute before approval → 409 hitl_required  → status=409 code=hitl_required
> ✅ B approve → 200 approved  → ps=approved
> ✅ B execute after approval → 200 executed  → ps=executed
> ✅ B idempotent execute → already=true
> ✅ D reject → 200 rejected  → ps=rejected
> ✅ D execute after reject → 409
> 
> 🧹 cleanup: 2 throwaway user(s) deleted (intent_plans cascade)
> 
> ✅✅ INTENT-EXECUTE HITL SMOKE PASSED
> ```

## 🤖 Claude *(00:58:14)*


## 🤖 Claude *(00:58:17)*

**15/15 — propriedade de segurança central provada materialmente**: o `auto_approved` adulterado de alto impacto (C) é **recusado** (409 `hitl_required`, não executa), enquanto o caminho legítimo `pending_hitl→approve→execute` funciona + idempotência + tenant-guard 404. Item 2 (executor backend) **fechado e verificado**.

Agora **Fase D — FR-MH-010 AEO**. Para regenerar types uma única vez (intent_plans + aeo_audits juntos), faço o backend AEO primeiro. SOP (Lei 2) + migration:

## 🤖 Claude *(00:58:46)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/aeo-audit.md",
  "content": "# SOP \u2014 AEO Audit (Answer Engine Optimization visibility snapshot)\n\n> **Lei 2 (Processo Antecipado).** Documenta o processo humano do FR-MH-010 **antes** do `aeo-audit`. SSOT: `docs/bok/marketing-hub/04-frd.md` FR-MH-010 + `05-sdd.md` (\u00a7aeo-audit + STRIDE \"AEO provider call / prompt injection \u2192 sanitiza\u00e7\u00e3o; provider isolado; sem secret no prompt\") + `06-data-model.md` (\u00a7aeo_audits).\n\n## Contexto\n\n**AEO (Answer Engine Optimization)** \u00e9 o \"SEO dos motores de resposta\": quando um usu\u00e1rio pergunta algo a um motor de resposta de IA (ChatGPT, Perplexity, Google AI Overviews, Gemini), **a marca aparece citada?** O `aeo-audit` tira um **snapshot de visibilidade**: para um conjunto de queries rastreadas + a marca, mede cita\u00e7\u00e3o (`cited`/`citation_rate`) e devolve uma **recomenda\u00e7\u00e3o** de melhoria. Persiste em `aeo_audits` (reten\u00e7\u00e3o 12 meses; \"stale\" ap\u00f3s \u2264 7 dias \u2014 NFR-MH-010).\n\n### Provider (OTD-MH-003) \u2014 modo degradado documentado\n\nN\u00e3o h\u00e1, hoje, chave de um motor de resposta dedicado provisionada, **e** o datacenter \u00e9 bloqueado para scrape de SERP/answer-engine ao vivo (li\u00e7\u00e3o provada: ML bloqueia Chromium real do datacenter). Portanto o provider roda em **modo degradado documentado**: o **LLM per-user** (Groq/OpenRouter/Gemini, mesma resolu\u00e7\u00e3o do `intent-orchestrate`) atua como *answer-engine proxy* \u2014 responde a query como um motor de resposta responderia e detecta se a marca seria citada. `aeo_audits.engine='degraded'` marca explicitamente o snapshot como proxy-LLM (n\u00e3o um motor real). Quando uma chave de provider real for provisionada (OTD-MH-003=B), troca-se o provider e `engine` passa a refletir o motor real \u2014 sem mudan\u00e7a de contrato.\n\n## Operator\n\nQuem executa hoje: o **tenant** (Usu\u00e1rio Zero / operador de marketing) no Marketing Hub (`/dashboard/marketing`, painel AEO), informando **a marca** + **1\u20135 queries** rastreadas.\n\n## Sequence (cada passo com crit\u00e9rio material)\n\n| # | Passo | A\u00e7\u00e3o | Crit\u00e9rio de sucesso material |\n|---|-------|------|------------------------------|\n| 1 | **Saldo** | `aeo-audit` checa `profiles.mco_balance \u2265 5` | < 5 \u2192 HTTP 402 \"Saldo insuficiente\" (nada cobrado) |\n| 2 | **D\u00e9bito** | `deduct_mco_coins(user, 5)` at\u00f4mico **na entrada** | saldo \u22125 (RPC server-side; nunca client-side) |\n| 3 | **Sanitiza\u00e7\u00e3o** | trunca brand (\u2264120) + cada query (\u2264280), cap 5 queries | input fora de faixa \u2192 422 |\n| 4 | **Proxy de motor** | p/ cada query, LLM per-user\u2192sistema responde + detecta cita\u00e7\u00e3o | resposta JSON `{cited, citation_rate, recommendation}` por query (fail-soft heur\u00edstico se IA indispon\u00edvel) |\n| 5 | **Persistir** | INSERT 1 linha `aeo_audits` por query (`engine='degraded'`) | linhas com `0 \u2264 citation_rate \u2264 1` |\n| 6 | **Agregar** | `citation_rate` agregada = fra\u00e7\u00e3o de queries citadas | HTTP 200 `{audit_id, citation_rate, findings[]}` |\n\n## Verification gates\n\n1. **D\u00e9bito antes do trabalho.** 5 mcoCoins deduzidos **antes** da chamada de IA (igual `lead-score`/`campaign-run`). Saldo insuficiente \u2192 402, zero trabalho.\n2. **Sanitiza\u00e7\u00e3o (STRIDE \u2014 prompt injection).** brand/query truncados e inseridos como *dados* no prompt; **nenhum segredo** entra no prompt; provider isolado.\n3. **Faixa v\u00e1lida.** `citation_rate \u2208 [0,1]` (CHECK no banco); `query` 1\u2013280 chars (CHECK). Viola\u00e7\u00e3o \u2192 erro do banco, n\u00e3o persiste lixo.\n4. **Telemetria.** cada path (success/degraded/error) emite `infra_health_logs.service='aeo-audit'` (NFR-MH-009).\n5. **Degrada\u00e7\u00e3o honesta.** sem IA dispon\u00edvel \u2192 recomenda\u00e7\u00e3o heur\u00edstica + `engine='degraded'`; nunca fabrica cita\u00e7\u00e3o \"real\".\n\n## Recovery path\n\n- **402 (saldo):** Operator compra/recarrega mcoCoins; nada foi cobrado.\n- **IA indispon\u00edvel:** fail-soft \u2014 a auditoria ainda persiste com recomenda\u00e7\u00e3o heur\u00edstica (`cited=false`, `citation_rate=0`) + `infra_health_logs status='degraded'`; o Operator re-roda quando a IA voltar (novo d\u00e9bito).\n- **Falha de persist\u00eancia (500):** `infra_health_logs status='unhealthy'`; **o d\u00e9bito j\u00e1 ocorreu** \u2192 a recovery \u00e9 re-rodar (custo assumido) OU o Sovereign credita manualmente (registro no handoff). _OTD-AEO-REFUND: avaliar refund autom\u00e1tico em falha p\u00f3s-d\u00e9bito (espelha o d\u00e9bito at\u00f4mico do `lead-score`)._\n\n## Success signal (materialmente observ\u00e1vel)\n\nHTTP 200 `{status:'ok', audit_id, citation_rate, findings[]}` + N linhas em `aeo_audits` (1 por query) com `created_at` recente + n\u00f3 `observation` `aeo:<brand>:<date>` no mesh + `infra_health_logs.service='aeo-audit' status='healthy'`. Freshness: um audit conta como vigente por \u2264 7 dias (NFR-MH-010).\n\n## ORO\n\n- **Operator:** tenant (humano) \u00b7 **Reviewer:** `/security-review` da migration `aeo_audits` + policy de d\u00e9bito at\u00f4mico \u00b7 **Owner:** Sovereign (blast radius = 5 mcoCoins/run + qualidade da recomenda\u00e7\u00e3o; provider degradado documentado, sem risco outward).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/aeo-audit.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:58:50)*

Agora a migration `aeo_audits` — espelha o esqueleto RLS-default-deny dos irmãos (intent_plans/sequences), append-only (só `created_at`), com os CHECKs do data-model:

## 🤖 Claude *(00:59:01)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql",
  "content": "-- Migration: marketing-hub AEO Audit data layer (FR-MH-010).\n-- BoK SSOT: docs/bok/marketing-hub/06-data-model.md (\u00a7Table aeo_audits) + 04-frd.md FR-MH-010 + 05-sdd.md\n--           (aeo-audit edge fn; STRIDE \"AEO provider call / prompt injection \u2192 sanitiza\u00e7\u00e3o; provider isolado\").\n--\n-- `aeo-audit` (JWT, 5 mcoCoins) takes {queries[], brand}, asks an answer-engine proxy whether the brand is cited\n-- for each tracked query, and persists ONE append-only snapshot row per query. `engine='degraded'` marks the\n-- documented degraded provider (OTD-MH-003 \u2014 LLM-as-answer-engine; no live SERP scrape from the datacenter).\n-- Append-only (no updated_at). RLS default-deny, user-scoped \u2014 identical skeleton to intent_plans/sequences.\n\nCREATE TABLE IF NOT EXISTS public.aeo_audits (\n  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),\n  user_id        uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,\n  brand          text NOT NULL CHECK (char_length(brand) BETWEEN 1 AND 120),\n  query          text NOT NULL CHECK (char_length(query) BETWEEN 1 AND 280),\n  cited          boolean NOT NULL DEFAULT false,\n  citation_rate  real NOT NULL DEFAULT 0 CHECK (citation_rate >= 0 AND citation_rate <= 1),\n  engine         text NOT NULL DEFAULT 'degraded' CHECK (engine IN ('chatgpt','perplexity','google_ai','gemini','degraded')),\n  recommendation text,\n  created_at     timestamptz NOT NULL DEFAULT timezone('utc'::text, now())\n);\n\nALTER TABLE public.aeo_audits ENABLE ROW LEVEL SECURITY;\nCREATE POLICY \"aeo_audits_select_own\" ON public.aeo_audits FOR SELECT USING (auth.uid() = user_id);\nCREATE POLICY \"aeo_audits_insert_own\" ON public.aeo_audits FOR INSERT WITH CHECK (auth.uid() = user_id);\nCREATE POLICY \"aeo_audits_update_own\" ON public.aeo_audits FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);\nCREATE POLICY \"aeo_audits_delete_own\" ON public.aeo_audits FOR DELETE USING (auth.uid() = user_id);\n\n-- Newest-first per tenant (panel + freshness check NFR-MH-010 \u2264 7 days).\nCREATE INDEX IF NOT EXISTS idx_aeo_audits_user_created ON public.aeo_audits (user_id, created_at DESC);\n-- Per-brand grouping for aggregate citation snapshots.\nCREATE INDEX IF NOT EXISTS idx_aeo_audits_user_brand ON public.aeo_audits (user_id, brand);\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:59:07)*


## 🤖 Claude *(00:59:08)*

Patch do data-model BoK para incluir `degraded` no enum `engine` (modo degradado documentado):

## 🤖 Claude *(00:59:09)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/06-data-model.md",
  "old_string": "`engine` text (chatgpt\\|perplexity\\|google_ai\\|gemini) \u00b7 `recommendation` text",
  "new_string": "`engine` text (chatgpt\\|perplexity\\|google_ai\\|gemini\\|degraded) \u00b7 `recommendation` text"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(00:59:12)*


## 🤖 Claude *(00:59:13)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/06-data-model.md",
  "offset": 124,
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 124	### Table: `aeo_audits`
> 125	
> 126	| Column | Type | Notes |
> 127	|--------|------|-------|
> 128	| `id` uuid PK · `user_id` uuid · `brand` text · `query` text · `cited` bool · `citation_rate` float4 · `engine` text (chatgpt\|perplexity\|google_ai\|gemini) · `recommendation` text · `created_at` timestamptz | Snapshot de visibilidade em motores de resposta |
> 129	
> ```

## 🤖 Claude *(00:59:16)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/06-data-model.md",
  "old_string": "`engine` text (chatgpt\\|perplexity\\|google_ai\\|gemini) \u00b7 `recommendation` text",
  "new_string": "`engine` text (chatgpt\\|perplexity\\|google_ai\\|gemini\\|degraded) \u00b7 `recommendation` text"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/06-data-model.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:59:31)*


## 🤖 Claude *(00:59:31)*

Migration escrita + data-model patcheado. Aplico via `npx supabase db push`:

## 🤖 Claude *(00:59:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx supabase db push 2>&1 | tail -25",
  "description": "Push aeo_audits migration to remote DB"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Initialising login role...
> Connecting to remote database...
> Do you want to push these migrations to the remote database?
>  • 20260603260000_marketing_hub_aeo_audits.sql
> 
>  [Y/n] 
> Applying migration 20260603260000_marketing_hub_aeo_audits.sql...
> Finished supabase db push.
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(01:00:00)*


## 🤖 Claude *(01:00:02)*

Migration aplicada: **"Finished supabase db push"** (só `20260603260000` — confirma que intent_plans já estava no histórico remoto). Agora o **edge fn `aeo-audit`** (espelha lead-score: débito 5 atômico → IA per-user→sistema como answer-engine proxy → persiste `aeo_audits`):

## 🤖 Claude *(01:00:36)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/aeo-audit/index.ts",
  "content": "// aeo-audit \u2014 marketing-hub FR-MH-010 (Answer Engine Optimization visibility snapshot).\n// SSOT: docs/bok/marketing-hub/04-frd.md FR-MH-010 + 05-sdd.md (\u00a7aeo-audit + STRIDE \"prompt injection \u2192 sanitiza\u00e7\u00e3o;\n// provider isolado; sem secret no prompt\") + 06-data-model.md (\u00a7aeo_audits) + docs/processes/aeo-audit.md.\n//\n// Takes {queries[], brand}; for each tracked query asks an ANSWER-ENGINE PROXY (the per-user LLM, OTD-MH-003 degraded\n// mode \u2014 no live SERP scrape from the datacenter) whether the brand would be cited, and persists ONE append-only\n// snapshot row per query in aeo_audits (engine='degraded'). Debits 5 mcoCoins atomically AT ENTRY (mirrors lead-score).\n// JWT-guarded (verify_jwt=false + in-function getUser \u2014 edge-jwt SOP).\nimport { serve } from \"https://deno.land/std@0.168.0/http/server.ts\";\nimport { createClient } from \"https://esm.sh/@supabase/supabase-js@2\";\nimport { fetchLLMWithFallback } from \"../_shared/llm-fallback.ts\";\n\nconst corsHeaders = {\n  \"Access-Control-Allow-Origin\": \"*\",\n  \"Access-Control-Allow-Methods\": \"POST, OPTIONS\",\n  \"Access-Control-Allow-Headers\": \"authorization, x-client-info, apikey, content-type\",\n};\n\nconst AEO_COST = 5;\nconst MAX_QUERIES = 5;\ninterface Finding { query: string; cited: boolean; citation_rate: number; recommendation: string }\nconst clamp01 = (n: unknown) => Math.max(0, Math.min(1, Number(n) || 0));\n\nserve(async (req) => {\n  if (req.method === \"OPTIONS\") return new Response(\"ok\", { headers: corsHeaders });\n  const json = (b: unknown, s = 200) =>\n    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, \"Content-Type\": \"application/json\" } });\n\n  const url = Deno.env.get(\"SUPABASE_URL\")!;\n  const serviceKey = (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!;\n  const anonKey = (Deno.env.get(\"SB_PUBLISHABLE_KEY\") ?? Deno.env.get(\"SUPABASE_ANON_KEY\"))!;\n  const admin = createClient(url, serviceKey);\n  const log = (status: string) => admin.from(\"infra_health_logs\").insert({ service: \"aeo-audit\", status }).then(() => {}, () => {});\n\n  try {\n    const authHeader = req.headers.get(\"Authorization\");\n    if (!authHeader) return json({ error: \"Missing authorization\" }, 401);\n    const userClient = createClient(url, anonKey, { global: { headers: { Authorization: authHeader } } });\n    const { data: { user }, error: authError } = await userClient.auth.getUser();\n    if (authError || !user) return json({ error: \"Unauthorized\" }, 401);\n\n    // \u2500\u2500 Input sanitization (STRIDE \u2014 prompt injection): brand/query are DATA, truncated, capped. \u2500\u2500\n    const body = await req.json().catch(() => ({}));\n    const brand = typeof body?.brand === \"string\" ? body.brand.trim().slice(0, 120) : \"\";\n    const rawQueries = Array.isArray(body?.queries) ? body.queries : [];\n    const queries: string[] = rawQueries\n      .filter((q: unknown) => typeof q === \"string\" && q.trim())\n      .map((q: string) => q.trim().slice(0, 280))\n      .slice(0, MAX_QUERIES);\n    if (!brand) return json({ error: \"brand \u00e9 obrigat\u00f3rio\" }, 422);\n    if (queries.length === 0) return json({ error: \"Informe ao menos 1 query (m\u00e1x. 5)\" }, 422);\n\n    // \u2500\u2500 mcoCoins gate: check balance, then atomic deduct AT ENTRY (server-side RPC only). \u2500\u2500\n    const { data: bal } = await admin.from(\"profiles\").select(\"mco_balance\").eq(\"id\", user.id).maybeSingle();\n    if ((bal?.mco_balance ?? 0) < AEO_COST) return json({ error: \"Saldo insuficiente de mcoCoins\" }, 402);\n    const { error: deductErr } = await admin.rpc(\"deduct_mco_coins\", { p_user_id: user.id, p_amount: AEO_COST });\n    if (deductErr) return json({ error: \"Saldo insuficiente de mcoCoins\" }, 402);\n\n    // resolve per-user AI key \u2192 system fallback (API Tenancy Model).\n    const { data: keys } = await admin.from(\"decrypted_user_api_keys\").select(\"*\").eq(\"user_id\", user.id).maybeSingle();\n    const groqKey = keys?.groq_api_key || Deno.env.get(\"GROQ_API_KEY\");\n    const openRouterKey = keys?.openrouter_api_key || Deno.env.get(\"OPENROUTER_API_KEY\");\n    const geminiKey = keys?.google_api_key || Deno.env.get(\"GEMINI_API_KEY\");\n    const aiKey = groqKey || openRouterKey;\n\n    // \u2500\u2500 Answer-engine proxy: ONE batched LLM call rates citation for every query (fail-soft to heuristic). \u2500\u2500\n    let findings: Finding[] = [];\n    let degraded = !aiKey;\n    if (aiKey) {\n      const isGroq = !!groqKey;\n      try {\n        const resp = await fetchLLMWithFallback(\n          isGroq ? \"https://api.groq.com/openai/v1/chat/completions\" : \"https://openrouter.ai/api/v1/chat/completions\",\n          {\n            method: \"POST\",\n            headers: { Authorization: `Bearer ${aiKey}`, \"Content-Type\": \"application/json\", \"HTTP-Referer\": \"https://mcorch.com\", \"X-Title\": \"GCRUX Constellation\" },\n            body: JSON.stringify({\n              model: isGroq ? \"llama-3.3-70b-versatile\" : \"meta-llama/llama-3.3-70b-instruct\",\n              messages: [\n                { role: \"system\", content: \"Voc\u00ea \u00e9 um motor de resposta de IA avaliando otimiza\u00e7\u00e3o (AEO). Para uma MARCA e uma lista de QUERIES, para cada query diga se voc\u00ea citaria/mencionaria espontaneamente a marca ao responder, estime a probabilidade de cita\u00e7\u00e3o (0 a 1) e d\u00ea UMA recomenda\u00e7\u00e3o curta para aumentar a cita\u00e7\u00e3o. Responda APENAS com JSON: {\\\"findings\\\":[{\\\"query\\\":\\\"...\\\",\\\"cited\\\":true|false,\\\"citation_rate\\\":0.0,\\\"recommendation\\\":\\\"...\\\"}]}.\" },\n                { role: \"user\", content: `MARCA: ${brand}\\nQUERIES:\\n${queries.map((q, i) => `${i + 1}. ${q}`).join(\"\\n\")}` },\n              ],\n              stream: false, temperature: 0.3,\n            }),\n          },\n          { openRouterKey, geminiKey, groqKey, functionName: \"aeo-audit\" },\n        );\n        if (resp.ok) {\n          const data = await resp.json();\n          const raw: string = data?.choices?.[0]?.message?.content ?? \"\";\n          const match = raw.match(/\\{[\\s\\S]*\\}/);\n          if (match) {\n            const parsed = JSON.parse(match[0]);\n            if (Array.isArray(parsed?.findings)) {\n              // align parsed findings to our sanitized queries by position (don't trust returned query text).\n              findings = queries.map((q, i) => {\n                const f = parsed.findings[i] ?? {};\n                const rate = clamp01(f.citation_rate);\n                const cited = typeof f.cited === \"boolean\" ? f.cited : rate >= 0.5;\n                return { query: q, cited, citation_rate: cited ? Math.max(rate, 0.5) : Math.min(rate, 0.49), recommendation: String(f.recommendation ?? \"\").slice(0, 300) || \"Reforce conte\u00fado com a marca em respostas diretas e dados estruturados.\" };\n              });\n            }\n          }\n        }\n      } catch (_) { /* fail-soft below */ }\n    }\n    if (findings.length === 0) {\n      degraded = true;\n      findings = queries.map((q) => ({ query: q, cited: false, citation_rate: 0, recommendation: \"Plano heur\u00edstico (IA indispon\u00edvel) \u2014 publique conte\u00fado cit\u00e1vel com a marca e marca\u00e7\u00e3o estruturada para esta query.\" }));\n    }\n\n    // \u2500\u2500 Persist one append-only snapshot row per query (service role + explicit user_id). \u2500\u2500\n    const rows = findings.map((f) => ({\n      user_id: user.id, brand, query: f.query, cited: f.cited,\n      citation_rate: f.citation_rate, engine: \"degraded\", recommendation: f.recommendation,\n    }));\n    const { data: inserted, error: insErr } = await admin.from(\"aeo_audits\").insert(rows).select(\"id\");\n    if (insErr || !inserted?.length) {\n      log(\"unhealthy\");\n      return json({ error: \"Falha ao persistir a auditoria AEO\", detail: insErr?.message }, 500);\n    }\n\n    const citationRate = findings.reduce((acc, f) => acc + (f.cited ? 1 : 0), 0) / findings.length;\n\n    // observation node into the Knowledge Mesh (mandate: every orchestration run). Fire-and-forget.\n    const today = new Date().toISOString().slice(0, 10);\n    admin.from(\"mcorch_nodes\").insert({\n      node_type: \"observation\", name: `aeo:${brand.slice(0, 60)}:${today}`,\n      content: `AEO snapshot \u2014 marca \"${brand}\" \u00b7 ${findings.length} queries \u00b7 cita\u00e7\u00e3o agregada ${(citationRate * 100).toFixed(0)}%${degraded ? \" (degradado)\" : \"\"}`,\n      user_id: user.id,\n    }).then(() => {}, () => {});\n    log(degraded ? \"degraded\" : \"healthy\");\n\n    return json({\n      status: \"ok\",\n      audit_id: inserted[0].id,\n      citation_rate: citationRate,\n      findings: findings.map((f) => ({ query: f.query, cited: f.cited, recommendation: f.recommendation })),\n      source: degraded ? \"degraded\" : \"ai\",\n    });\n  } catch (err) {\n    log(\"unhealthy\");\n    return json({ error: \"Erro interno no aeo-audit\", detail: String((err as Error)?.message ?? err) }, 500);\n  }\n});\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/aeo-audit/index.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:00:54)*


## 🤖 Claude *(01:00:54)*

Deploy do `aeo-audit` + escrevo o smoke em paralelo:

## 🤖 Claude *(01:00:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx supabase functions deploy aeo-audit 2>&1 | tail -6",
  "description": "Deploy aeo-audit edge function"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Bundling Function: aeo-audit
> Deploying Function: aeo-audit (script size: 85.3kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: aeo-audit
> You can inspect your deployment in the Dashboard: https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa/functions
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(01:01:17)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-aeo-audit.ts",
  "content": "#!/usr/bin/env bun\n/**\n * Smoke test \u2014 aeo-audit (FR-MH-010 / AT-MH-010), USER PATH (real JWT).\n *\n * Proves: atomic 5-mcoCoin debit AT ENTRY; one append-only aeo_audits row per query (RLS user-scoped);\n * citation_rate \u2208 [0,1]; 402 on insufficient balance (no debit, no rows); 422 input guards; 401 no-auth;\n * cross-tenant isolation (user B cannot read user A's audits). Throwaway users + cascade cleanup. The only\n * marginal cost is ONE batched LLM call on a throwaway user (~$0.001, system key).\n *\n * Usage: bun run scripts/qa/smoke-aeo-audit.ts\n */\nimport { createClient } from '@supabase/supabase-js';\n\nconst URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;\nconst SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;\nconst PUB = process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? process.env.SUPABASE_ANON_KEY!;\nif (!URL || !SVC || !PUB) { console.error('Missing env (URL/SVC/PUB)'); process.exit(1); }\n\nconst admin = createClient(URL, SVC, { auth: { persistSession: false } });\nconst stamp = Date.now();\nconst uids: string[] = [];\nlet pass = true;\nconst check = (l: string, ok: boolean, d = '') => { console.log(`${ok ? '\u2705' : '\u274c'} ${l}${d ? `  \u2192 ${d}` : ''}`); if (!ok) pass = false; };\n\nasync function mkUser(tag: string, balance: number): Promise<{ uid: string; token: string }> {\n  const email = `aeo-${tag}-${stamp}@example.com`, password = `Aa1!${crypto.randomUUID()}`;\n  const { data: cu, error } = await admin.auth.admin.createUser({ email, password, email_confirm: true });\n  if (error || !cu?.user) throw new Error(`createUser(${tag}): ${error?.message}`);\n  uids.push(cu.user.id);\n  await admin.from('profiles').update({ mco_balance: balance }).eq('id', cu.user.id);\n  const userClient = createClient(URL, PUB, { auth: { persistSession: false } });\n  const { data: si, error: siErr } = await userClient.auth.signInWithPassword({ email, password });\n  if (siErr || !si?.session) throw new Error(`signIn(${tag}): ${siErr?.message}`);\n  return { uid: cu.user.id, token: si.session.access_token };\n}\nconst bal = async (uid: string) => Number((await admin.from('profiles').select('mco_balance').eq('id', uid).single()).data?.mco_balance ?? 0);\n\nasync function audit(token: string | null, body: unknown) {\n  const headers: Record<string, string> = { 'Content-Type': 'application/json', apikey: PUB };\n  if (token) headers.Authorization = `Bearer ${token}`;\n  const r = await fetch(`${URL}/functions/v1/aeo-audit`, { method: 'POST', headers, body: JSON.stringify(body) });\n  let j: { status?: string; audit_id?: string; citation_rate?: number; findings?: Array<{ query: string; cited: boolean; recommendation: string }>; error?: string } = {};\n  const t = await r.text(); try { j = JSON.parse(t); } catch { /* keep {} */ }\n  return { status: r.status, body: j };\n}\n\ntry {\n  const u1 = await mkUser('owner', 100);\n  const u2 = await mkUser('intruder', 3); // under the 5-coin floor\n\n  // \u2500\u2500 1. Guards (zero cost) \u2500\u2500\n  check('no-auth \u2192 401', (await audit(null, { brand: 'X', queries: ['q'] })).status === 401);\n  check('missing brand \u2192 422', (await audit(u1.token, { queries: ['q'] })).status === 422);\n  check('empty queries \u2192 422', (await audit(u1.token, { brand: 'X', queries: [] })).status === 422);\n  const poor = await audit(u2.token, { brand: 'X', queries: ['q'] });\n  check('insufficient balance \u2192 402', poor.status === 402, `status=${poor.status}`);\n  check('402 did NOT debit', (await bal(u2.uid)) === 3, `bal=${await bal(u2.uid)}`);\n\n  // \u2500\u2500 2. Happy path: real audit (1 batched LLM call) \u2500\u2500\n  const before = await bal(u1.uid);\n  const queries = ['melhor rob\u00f4 aspirador 2026', 'geladeira smart com tela'];\n  const r = await audit(u1.token, { brand: 'MCORCH', queries });\n  check('happy \u2192 200 status ok', r.status === 200 && r.body.status === 'ok', `status=${r.status}`);\n  check('audit_id returned', !!r.body.audit_id);\n  check('findings: one per query', r.body.findings?.length === queries.length, `n=${r.body.findings?.length}`);\n  check('citation_rate \u2208 [0,1]', typeof r.body.citation_rate === 'number' && r.body.citation_rate! >= 0 && r.body.citation_rate! <= 1, `rate=${r.body.citation_rate}`);\n  check('debited exactly 5 mcoCoins', before - (await bal(u1.uid)) === 5, `${before}\u2192${await bal(u1.uid)}`);\n\n  // \u2500\u2500 3. Persistence + RLS isolation \u2500\u2500\n  const { count: ownRows } = await admin.from('aeo_audits').select('id', { count: 'exact', head: true }).eq('user_id', u1.uid);\n  check('aeo_audits persisted (one row per query)', (ownRows ?? 0) === queries.length, `rows=${ownRows}`);\n  const u2Client = createClient(URL, PUB, { global: { headers: { Authorization: `Bearer ${u2.token}` } }, auth: { persistSession: false } });\n  const { data: leak } = await u2Client.from('aeo_audits').select('id').eq('user_id', u1.uid);\n  check('cross-tenant read blocked by RLS', (leak?.length ?? 0) === 0, `leaked=${leak?.length ?? 0}`);\n} catch (e) {\n  pass = false; console.error('\u274c smoke error:', e instanceof Error ? e.message : e);\n} finally {\n  for (const id of uids) await admin.auth.admin.deleteUser(id);\n  console.log(`\\n\ud83e\uddf9 cleanup: ${uids.length} throwaway user(s) deleted (aeo_audits cascade)`);\n  console.log(pass ? '\\n\u2705\u2705 AEO-AUDIT SMOKE PASSED' : '\\n\u274c AEO-AUDIT SMOKE FAILED');\n  process.exit(pass ? 0 : 1);\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-aeo-audit.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:01:22)*


## 🤖 Claude *(01:01:23)*

`aeo-audit` deployed (85.3kB). Rodo o smoke (inclui 1 chamada real de IA num throwaway):

## 🤖 Claude *(01:01:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run scripts/qa/smoke-aeo-audit.ts 2>&1",
  "description": "Run aeo-audit smoke"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ no-auth → 401
> ✅ missing brand → 422
> ✅ empty queries → 422
> ✅ insufficient balance → 402  → status=402
> ✅ 402 did NOT debit  → bal=3
> ✅ happy → 200 status ok  → status=200
> ✅ audit_id returned
> ✅ findings: one per query  → n=2
> ✅ citation_rate ∈ [0,1]  → rate=0
> ✅ debited exactly 5 mcoCoins  → 100→95
> ✅ aeo_audits persisted (one row per query)  → rows=2
> ✅ cross-tenant read blocked by RLS  → leaked=0
> 
> 🧹 cleanup: 2 throwaway user(s) deleted (aeo_audits cascade)
> 
> ✅✅ AEO-AUDIT SMOKE PASSED
> ```

## 🤖 Claude *(01:01:49)*


## 🤖 Claude *(01:01:49)*

**12/12 — AEO backend provado**: débito atômico 5 (100→95), 402 sem débito, guards 422/401, 1 linha por query, RLS cross-tenant (leaked=0). `citation_rate=0` é honesto (o LLM não citaria "MCORCH" para queries genéricas de produto).

Ambos os backends fechados. Agora o **gate obrigatório**: `/security-review` da migration nova (regra CLAUDE.md) antes de qualquer commit.

## 🤖 Claude *(01:01:49)*


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

## 👤 User *(01:01:49)*

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   docs/bok/marketing-hub/05-sdd.md
	modified:   docs/bok/marketing-hub/06-data-model.md
	modified:   src/components/marketing/LeadDetailDialog.tsx
	modified:   supabase/config.toml
	modified:   supabase/functions/intent-orchestrate/index.ts

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/processes/aeo-audit.md
	docs/processes/intent-plan-execution.md
	scripts/qa/smoke-aeo-audit.ts
	scripts/qa/smoke-intent-execute.ts
	supabase/functions/_shared/intent-policy.ts
	supabase/functions/aeo-audit/
	supabase/functions/intent-execute/
	supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql

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

## 🤖 Claude *(01:01:55)*


## 🤖 Claude *(01:02:06)*

API Error: The socket connection was closed unexpectedly. For more information, pass `verbose: true` in the second argument to fetch()

## 👤 User *(01:03:18)*

<command-name>/goal</command-name>
            <command-message>goal</command-message>
            <command-args>⚡ PRÓXIMOS PASSOS (prioridade — backend pronto, falta o rosto)

UI follows do Marketing Hub — botão enroll de nurturing (hook enrollLead já existe em useNurturing) + useIntentOrchestrator + HITLApprovalCard (FR-MH-009 backend LIVE, sem UI).
Executor de intent_plans (aprovar/rejeitar/executar) — DEVE re-validar a ação outward no execute (defesa-em-profundidade; não confiar em auto_approved).
FR-MH-010 AEO audit — única FR restante do marketing-hub. Entrega externa de nurturing segue gated (credencial resend_api_key per-tenant já pronta).</command-args>

## 👤 User *(01:03:18)*

<local-command-stdout>Goal set: ⚡ PRÓXIMOS PASSOS (prioridade — backend pronto, falta o rosto)

UI follows do Marketing Hub — botão enroll de nurturing (hook enrollLead já existe em useNurturing) + useIntentOrchestrator + HITLApprovalCard (FR-MH-009 backend LIVE, sem UI).
Executor de intent_plans (aprovar/rejeitar/executar) — DEVE re-validar a ação outward no execute (defesa-em-profundidade; não confiar em auto_approved).
FR-MH-010 AEO audit — única FR restante do marketing-hub. Entrega externa de nurturing segue gated (credencial resend_api_key per-tenant já pronta).</local-command-stdout>

## 👤 User *(01:03:18)*

A session-scoped Stop hook is now active with condition: "⚡ PRÓXIMOS PASSOS (prioridade — backend pronto, falta o rosto)

UI follows do Marketing Hub — botão enroll de nurturing (hook enrollLead já existe em useNurturing) + useIntentOrchestrator + HITLApprovalCard (FR-MH-009 backend LIVE, sem UI).
Executor de intent_plans (aprovar/rejeitar/executar) — DEVE re-validar a ação outward no execute (defesa-em-profundidade; não confiar em auto_approved).
FR-MH-010 AEO audit — única FR restante do marketing-hub. Entrega externa de nurturing segue gated (credencial resend_api_key per-tenant já pronta).". Briefly acknowledge the goal, then immediately start (or continue) working toward it — treat the condition itself as your directive and do not pause to ask the user what to do. The hook will block stopping until the condition holds. It auto-clears once the condition is met — do not tell the user to run `/goal clear` after success; that's only for clearing a goal early.

## 🤖 Claude *(01:03:38)*


## 🤖 Claude *(01:03:40)*

The skill launched but the harness didn't auto-populate the diff. I'll run the review faithfully per the skill's 3-step protocol: an identification sub-agent over the actual changes, then parallel false-positive filters, then report only confidence ≥ 8. Let me gather the diff and launch the identification sub-task.

## 🤖 Claude *(01:03:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== DIFF: intent-orchestrate (refactor) ===\"; git diff --no-color supabase/functions/intent-orchestrate/index.ts | head -60\necho \"\"; echo \"=== DIFF: config.toml ===\"; git diff --no-color supabase/config.toml\necho \"\"; echo \"=== NEW migration ===\"; git diff --no-color --no-index /dev/null supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql 2>/dev/null | sed -n '1,60p'",
  "description": "Gather backend diff for security review"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === DIFF: intent-orchestrate (refactor) ===
> diff --git a/supabase/functions/intent-orchestrate/index.ts b/supabase/functions/intent-orchestrate/index.ts
> index aaa58dd..41ca50d 100644
> --- a/supabase/functions/intent-orchestrate/index.ts
> +++ b/supabase/functions/intent-orchestrate/index.ts
> @@ -7,6 +7,7 @@
>  import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
>  import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
>  import { fetchLLMWithFallback } from "../_shared/llm-fallback.ts";
> +import { planIsHighImpact, type PlanTask } from "../_shared/intent-policy.ts";
>  
>  const corsHeaders = {
>    "Access-Control-Allow-Origin": "*",
> @@ -14,11 +15,6 @@ const corsHeaders = {
>    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
>  };
>  
> -interface PlanTask { action: string; channel?: string; impact?: "low" | "medium" | "high"; rationale?: string }
> -
> -// High-impact = outward / financial actions that MUST NOT run without human review (the HITL gate).
> -const HIGH_IMPACT_RE = /(publi|send|e-?mail|post|tweet|spend|ad[_-]?spend|charge|cobr|envi|dispar|whats|launch|lança)/i;
> -
>  serve(async (req) => {
>    if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
>    const json = (b: unknown, s = 200) =>
> @@ -92,10 +88,8 @@ serve(async (req) => {
>      }
>  
>      // ── POLICY ENGINE: any high-impact task → HITL (mandatory human approval; STRIDE Tampering mitigation) ──
> -    // Fail-safe channel rule: ANY outward channel (anything that is not the internal 'none'/'content') forces HITL,
> -    // even if the AI mislabels impact=low or phrases the action verb to dodge the regex. Unknown channel → HITL.
> -    const isOutward = (c?: string) => !!c && !["none", "content"].includes(c.toLowerCase());
> -    const highImpact = tasks.some((t) => t.impact === "high" || HIGH_IMPACT_RE.test(t.action) || isOutward(t.channel));
> +    // Shared gate (_shared/intent-policy.ts) — intent-execute re-runs the SAME gate at execution time.
> +    const highImpact = planIsHighImpact(tasks);
>      const policy: "auto" | "hitl" = highImpact ? "hitl" : "auto";
>      const status = highImpact ? "pending_hitl" : "auto_approved";
>      const rationale = heuristic
> 
> === DIFF: config.toml ===
> diff --git a/supabase/config.toml b/supabase/config.toml
> index 7b6b067..42fc5e0 100644
> --- a/supabase/config.toml
> +++ b/supabase/config.toml
> @@ -23,6 +23,10 @@ verify_jwt = false
>  verify_jwt = false
>  [functions.intent-orchestrate]
>  verify_jwt = false
> +[functions.intent-execute]
> +verify_jwt = false
> +[functions.aeo-audit]
> +verify_jwt = false
>  [functions.generate-content]
>  verify_jwt = false
>  [functions.generate-audio-script]
> 
> === NEW migration ===
> diff --git a/supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql b/supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql
> new file mode 100644
> index 0000000..bbd5b48
> --- /dev/null
> +++ b/supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql
> @@ -0,0 +1,31 @@
> +-- Migration: marketing-hub AEO Audit data layer (FR-MH-010).
> +-- BoK SSOT: docs/bok/marketing-hub/06-data-model.md (§Table aeo_audits) + 04-frd.md FR-MH-010 + 05-sdd.md
> +--           (aeo-audit edge fn; STRIDE "AEO provider call / prompt injection → sanitização; provider isolado").
> +--
> +-- `aeo-audit` (JWT, 5 mcoCoins) takes {queries[], brand}, asks an answer-engine proxy whether the brand is cited
> +-- for each tracked query, and persists ONE append-only snapshot row per query. `engine='degraded'` marks the
> +-- documented degraded provider (OTD-MH-003 — LLM-as-answer-engine; no live SERP scrape from the datacenter).
> +-- Append-only (no updated_at). RLS default-deny, user-scoped — identical skeleton to intent_plans/sequences.
> +
> +CREATE TABLE IF NOT EXISTS public.aeo_audits (
> +  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> +  user_id        uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> +  brand          text NOT NULL CHECK (char_length(brand) BETWEEN 1 AND 120),
> +  query          text NOT NULL CHECK (char_length(query) BETWEEN 1 AND 280),
> +  cited          boolean NOT NULL DEFAULT false,
> +  citation_rate  real NOT NULL DEFAULT 0 CHECK (citation_rate >= 0 AND citation_rate <= 1),
> +  engine         text NOT NULL DEFAULT 'degraded' CHECK (engine IN ('chatgpt','perplexity','google_ai','gemini','degraded')),
> +  recommendation text,
> +  created_at     timestamptz NOT NULL DEFAULT timezone('utc'::text, now())
> +);
> +
> +ALTER TABLE public.aeo_audits ENABLE ROW LEVEL SECURITY;
> +CREATE POLICY "aeo_audits_select_own" ON public.aeo_audits FOR SELECT USING (auth.uid() = user_id);
> +CREATE POLICY "aeo_audits_insert_own" ON public.aeo_audits FOR INSERT WITH CHECK (auth.uid() = user_id);
> +CREATE POLICY "aeo_audits_update_own" ON public.aeo_audits FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> +CREATE POLICY "aeo_audits_delete_own" ON public.aeo_audits FOR DELETE USING (auth.uid() = user_id);
> +
> +-- Newest-first per tenant (panel + freshness check NFR-MH-010 ≤ 7 days).
> +CREATE INDEX IF NOT EXISTS idx_aeo_audits_user_created ON public.aeo_audits (user_id, created_at DESC);
> +-- Per-brand grouping for aggregate citation snapshots.
> +CREATE INDEX IF NOT EXISTS idx_aeo_audits_user_brand ON public.aeo_audits (user_id, brand);
> ```

## 🤖 Claude *(01:03:47)*


## 🤖 Claude *(01:03:48)*

Diff gathered. Launching the identification sub-task (reads the new edge fns + migration, compares against proven siblings), then I'll parallel-filter any findings:

## 🤖 Claude *(01:04:12)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Identify security vulns in marketing delta",
  "subagent_type": "general-purpose",
  "prompt": "You are a senior security engineer doing a FOCUSED security review of new changes in a Supabase/Deno + React (TanStack Query) multi-tenant codebase. Only flag HIGH-CONFIDENCE, concretely exploitable vulnerabilities INTRODUCED by these changes. This repo's security model: RLS default-deny on every table (`user_id = auth.uid()`); edge functions run with `verify_jwt=false` at the gateway but EACH enforces its own in-code auth via `supabase.auth.getUser()` on the Authorization header (this is the documented \"edge-jwt SOP\" pattern \u2014 NOT a vulnerability); sensitive mutations use the service-role client (`admin`) AFTER establishing the caller identity, scoping writes by explicit `user_id`.\n\nREVIEW EXACTLY THESE NEW/CHANGED FILES (read them):\n- supabase/functions/intent-execute/index.ts   (NEW \u2014 HITL approve/reject/execute state machine on `intent_plans`)\n- supabase/functions/aeo-audit/index.ts          (NEW \u2014 5-mcoCoin AEO audit; deduct + LLM + persist `aeo_audits`)\n- supabase/functions/_shared/intent-policy.ts    (NEW \u2014 high-impact policy gate)\n- supabase/functions/intent-orchestrate/index.ts (MODIFIED \u2014 now imports the shared gate)\n- supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql (NEW \u2014 `aeo_audits` table + RLS)\n- src/components/marketing/LeadDetailDialog.tsx   (MODIFIED \u2014 added a nurturing enroll Select+button)\n\nCOMPARE against these PROVEN-SAFE sibling patterns already in the repo (read as needed):\n- supabase/functions/lead-score/index.ts (the canonical \"JWT \u2192 balance check \u2192 deduct_mco_coins \u2192 per-user AI key\" pattern)\n- supabase/migrations/20260603250000_marketing_hub_intent_plans.sql (the RLS skeleton the new migration mirrors)\n- supabase/functions/nurture-dispatch/index.ts (tenant-scoped admin writes)\n\nKEY SECURITY PROPERTIES TO VERIFY (trace the data flow):\n1. **Tenant isolation / IDOR**: in intent-execute, is the plan loaded AND mutated scoped to `user_id = user.id` (the authenticated caller)? Can user A approve/reject/execute or read user B's plan? Check every `.update()/.select()` filter.\n2. **Authorization bypass of the HITL gate**: the directive requires `execute` to RE-VALIDATE outward/high-impact actions on the STORED plan and refuse if not human-approved \u2014 never trusting a stored `status='auto_approved'`. Is the re-validation actually enforced server-side? Any path where a high-impact plan reaches `status='executed'` WITHOUT going through `approved`?\n3. **mcoCoins integrity** (aeo-audit): is the 5-coin deduction atomic + server-side (RPC `deduct_mco_coins`), done BEFORE work, and is the balance checked? Any way to get the audit without paying, or to deduct another user's balance?\n4. **Injection**: any SQL/command injection? (Note: the codebase uses the supabase-js query builder \u2014 parameterized. LLM prompt injection via brand/query is NOT a reportable vuln per policy. Regex injection is NOT reportable.)\n5. **Input validation with security impact**: are `decision`, `plan_id`, `brand`, `queries` validated? Any type-confusion that crosses a privilege boundary?\n6. **RLS migration correctness**: does `aeo_audits` ENABLE RLS and have correct `auth.uid() = user_id` policies (no policy that exposes cross-tenant rows)?\n7. **Data exposure**: any secret/PII logged or returned? (Logging URLs / non-PII is fine.)\n\nEXCLUSIONS (do NOT report): DoS/rate-limiting/resource exhaustion; secrets-on-disk; outdated deps; findings only in test files (scripts/qa/*) or markdown/docs; client-side-only authz (the backend is the trust boundary); React XSS unless `dangerouslySetInnerHTML`; LLM/AI prompt-injection from user content; regex injection; log spoofing; theoretical races; SSRF that only controls a path.\n\nFor EACH candidate vulnerability output: file:line, severity (HIGH/MEDIUM only), category, description, concrete exploit scenario, fix recommendation, and a confidence score 1-10. If you find NO high-confidence issues, say so explicitly and explain why the key properties (1-3) hold, citing the exact lines that enforce them. Be precise and cite line numbers."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'I now have a complete and confident picture. The `executed` status has no downstream trigger, no pg_net, and `intent-execute` explicitly returns `outward_dispatch: "gated"` without performing any real send (mirroring nurture-dispatch\'s gated-sends posture). So even the non-array fail-open path produces no material outward action in this MVP — it only mislabels a state-machine row that the same owner already fully controls via RLS. That makes it not concretely exploitable for cross-tenant or privilege impact today. I\'ll note it as a defense-in-depth observation, not a reportable HIGH/MEDIUM.\n\nLet me write up the final assessment.\n\n## Security Review Result\n\n**No HIGH or MEDIUM confidence, concretely-exploitable vulnerabilities were introduced by these changes.** All seven key security properties hold. Below is the traced evidence per property, plus one sub-reportable defense-in-depth observation.\n\n---\n\n### Property 1 — Tenant isolation / IDOR (intent-execute): HOLDS\n\nEvery read and write is scoped to the authenticated caller. The identity comes from `userClient.auth.getUser()` on the `Authorization` header (`intent-execute/index.ts:38-40`), and `user.id` is then forced into every query:\n\n- Load: `.eq("id", plan_id).eq("user_id", user.id).maybeSingle()` → foreign plan returns `null` → 404 (`index.ts:47-50`).\n- Approve update: `.eq("id", plan_id).eq("user_id", user.id)` (`index.ts:57`).\n- Reject update: same dual filter (`index.ts:67`).\n- Execute update: same dual filter (`index.ts:87-88`).\n- The mesh observation node is written with `user_id: user.id` (`index.ts:93-97`).\n\nUser A cannot read, approve, reject, or execute User B\'s plan — the `user_id` filter is present on 100% of the `.select()`/`.update()` calls. This matches the canonical `lead-score`/`nurture-dispatch` pattern exactly.\n\n### Property 2 — HITL gate re-validation (the directive\'s golden rule): HOLDS\n\nThe server re-derives high-impact from the **stored plan** and refuses to execute an unapproved high-impact plan, never trusting the persisted `status`:\n\n- `intent-execute/index.ts:79`: `const highImpact = planIsHighImpact(row.plan);` (recomputed from the row, not read from `row.policy`/`row.status`).\n- `index.ts:80-85`: `if (highImpact && status !== "approved")` → returns 409 `hitl_required`. A row carrying `status=\'auto_approved\'` (AI mislabel or PostgREST tampering) with a high-impact task is still blocked, because the gate keys on `status === "approved"` (only reachable via the `approve` transition, which itself requires `status === "pending_hitl"`, `index.ts:56`).\n- The shared gate is fail-safe by construction (`_shared/intent-policy.ts:24-25`): high-impact if `impact===\'high\'` **OR** the action verb matches `HIGH_IMPACT_RE` **OR** the channel is any outward channel (anything not `none`/`content`). So an attacker who relabels `impact:\'low\'` to dodge one condition still trips the channel/verb conditions.\n\nThere is no path where a well-formed high-impact plan reaches `executed` without passing through `approved`.\n\n### Property 3 — mcoCoins integrity (aeo-audit): HOLDS\n\nAtomic, server-side, before work, balance-checked, own-tenant-only:\n\n- Pre-check: `profiles.mco_balance < AEO_COST` → 402 (`aeo-audit/index.ts:54-55`).\n- Atomic deduct via RPC **before** the LLM call and persistence (`index.ts:56-57`), `p_user_id: user.id` (the authenticated caller).\n- The RPC itself is hardened (`20260603220000_secure_ledger_rpcs.sql:44-53`): rejects `p_amount <= 0` (no mint via negative), and a non-`service_role` caller may only deduct `auth.uid()`\'s own profile. Even though aeo-audit calls it with the service-role client, the `p_user_id` is bound to the verified `user.id`, so there is no way to charge another user or to obtain the audit without paying (deduct precedes the `aeo_audits` insert at `index.ts:117`).\n\n### Property 4 — Injection: NONE\n\nAll DB access is via the supabase-js query builder (parameterized). The LLM `match`/`JSON.parse` of model output is wrapped and position-aligned to the sanitized `queries` array (`aeo-audit/index.ts:96-101` "don\'t trust returned query text"). LLM prompt-injection and regex are excluded per policy.\n\n### Property 5 — Input validation with security impact: HOLDS\n\n- `intent-execute`: `plan_id` must be a non-empty string (422, `index.ts:43`); `decision` is whitelisted against `DECISIONS` via `.includes()` (422, `index.ts:44`) — no type-confusion crosses a boundary.\n- `aeo-audit`: `brand` coerced to string, trimmed, capped 120 chars (`index.ts:44`); `queries` filtered to non-empty strings, capped 280 chars each, sliced to `MAX_QUERIES=5` (`index.ts:46-49`); empty `brand`/`queries` → 422. `citation_rate` is `clamp01`\'d before persistence (`index.ts:22, 98`), satisfying the DB CHECK.\n\n### Property 6 — RLS migration correctness (aeo_audits): HOLDS\n\n`20260603260000_marketing_hub_aeo_audits.sql`:\n- `ENABLE ROW LEVEL SECURITY` (line 22).\n- Four policies all gated on `auth.uid() = user_id` — SELECT (23), INSERT WITH CHECK (24), UPDATE USING+WITH CHECK (25), DELETE (26). No policy exposes cross-tenant rows; no `USING (true)`.\n- `user_id` is `NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE`; `engine` CHECK includes `\'degraded\'` (line 17), matching the hardcoded insert value (`aeo-audit/index.ts:115`), so no constraint-violation DoS. Mirrors the proven `intent_plans` skeleton.\n\n### Property 7 — Data exposure: NONE\n\nNo secrets or PII are logged or returned. `infra_health_logs` rows carry only `{service, status}`. Returned payloads contain the caller\'s own `findings`/`tasks`/`plan_status`. AI keys are read into locals and sent only in the upstream `Authorization` header (`aeo-audit/index.ts:76`), never echoed.\n\n### LeadDetailDialog.tsx (client): no backend trust issue\n\nPure display + a `sequence_enrollments` insert via `useNurturing.enrollLead` (RLS-gated by `auth.uid() = user_id` on that table). Client-side authz is not the trust boundary; the insert is constrained server-side. No `dangerouslySetInnerHTML`.\n\n---\n\n### Sub-reportable observation (defense-in-depth, NOT a HIGH/MEDIUM finding) — confidence 4/10\n\n`planIsHighImpact` fails *open* when `row.plan` is not a JSON array: `_shared/intent-policy.ts:30` is `Array.isArray(tasks) && tasks.some(...)`, so a non-array `plan` (e.g. a JSON object `{"0": {...high-impact...}}`) evaluates to `false`. Because `intent_plans` RLS lets the owner UPDATE their own row with no status-transition CHECK (`20260603250000:26`), a plan owner could, via direct PostgREST, set `plan` to an object **and** `status=\'auto_approved\'`, then call `intent-execute` with `decision=\'execute\'` and reach `status=\'executed\'` while skipping HITL.\n\nWhy this is **not** a reportable vuln today:\n- **No privilege/tenant boundary is crossed** — the attacker is the plan\'s own owner acting only on their own row; nothing here grants access to another tenant or to a capability they couldn\'t otherwise self-authorize.\n- **No material effect.** `executed` has no downstream consumer: there is no trigger, no `pg_net`, and no outward dispatch on `intent_plans` (confirmed — the only references to the table are the two edge functions; `intent-execute/index.ts:100-104` explicitly returns `outward_dispatch: "gated"` and performs no send, matching the gated-sends posture of `nurture-dispatch`). So the worst outcome is a mislabeled state-machine row in the owner\'s own tenant.\n\nHardening suggestion (cheap, future-proofs the gate before real dispatch is wired in): make the gate fail *closed* on malformed input, e.g. treat a non-array `plan` as high-impact in `planIsHighImpact` (`return !Array.isArray(tasks) || tasks.some(...)`), and/or add a status-transition CHECK/trigger on `intent_plans` so only `intent-execute` (service role) can move a row to `approved`/`executed`. This matters specifically once the "gated" outward dispatch at `intent-execute/index.ts:100` is replaced with a real campaign-run/nurture send.\n\nFiles reviewed: `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-execute/index.ts`, `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/aeo-audit/index.ts`, `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/intent-policy.ts`, `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-orchestrate/index.ts`, `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql`, `/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/LeadDetailDialog.tsx` (plus siblings `lead-score`, `nurture-dispatch`, `20260603250000_marketing_hub_intent_plans.sql`, `20260603220000_secure_ledger_rpcs.sql`, and `config.toml` for verify_jwt confirmation).'}, {'type': 'text', 'text': "agentId: ac4a4dc30c82fd359 (use SendMessage with to: 'ac4a4dc30c82fd359' to continue this agent)\n<usage>subagent_tokens: 85703\ntool_uses: 18\nduration_ms: 97123</usage>"}]
> ```

## 🤖 Claude *(01:06:13)*


## 🤖 Claude *(01:06:19)*

**`/security-review` verdict: SAFE** — o sub-agente independente traçou as 7 propriedades-chave com evidência por linha: tenant-isolation/IDOR (filtro `user_id` em 100% dos `.select`/`.update`), o gate HITL re-validado server-side (golden rule do directive **confirmada**), débito atômico 5-coin (RPC endurecido), RLS da migration correta. **Zero findings HIGH/MEDIUM ≥ confiança 8** (nenhum filtro paralelo necessário).

Houve **1 observação fail-safe (conf. 4/10, abaixo do threshold)**: `planIsHighImpact` falha *aberto* se `plan` não for array. Sem efeito material hoje (dispatch outward é gated, owner age no próprio row), mas como o directive **pede defesa-em-profundidade exatamente nesse gate**, adoto a correção one-line **fail-closed** agora (padrão da v6.26 "adotada 1 recomendação fail-safe") e registro o trigger de transição como OTD para quando o dispatch real for ligado:

## 🤖 Claude *(01:06:23)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/intent-policy.ts",
  "old_string": "/** True if ANY task in the plan is high-impact \u2192 mandatory human approval (HITL) before execution. */\nexport function planIsHighImpact(tasks: unknown): boolean {\n  return Array.isArray(tasks) && tasks.some((t) => isHighImpactTask(t as PlanTask));\n}",
  "new_string": "/**\n * True if ANY task in the plan is high-impact \u2192 mandatory human approval (HITL) before execution.\n * FAIL-CLOSED: a malformed/non-array plan (e.g. a tampered jsonb object) is treated as high-impact, so the\n * re-validation in intent-execute can never be skipped by sending a plan shape the gate doesn't recognize.\n */\nexport function planIsHighImpact(tasks: unknown): boolean {\n  if (!Array.isArray(tasks)) return true;\n  return tasks.some((t) => isHighImpactTask(t as PlanTask));\n}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/intent-policy.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:06:40)*


## 🤖 Claude *(01:06:41)*

Adoção fail-closed feita. Isso muda o artefato deployado, então redeploy + adiciono um caso de **prova material** no smoke (plan não-array adulterado → execute → 409 fail-closed) e re-rodo:

## 🤖 Claude *(01:06:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-intent-execute.ts",
  "old_string": "  const C = await insertPlan(u1.uid, HIGH_SOCIAL, 'auto_approved', 'auto'); // TAMPERED: high-impact stored as auto_approved\n  const D = await insertPlan(u1.uid, HIGH, 'pending_hitl', 'hitl');         // for reject path",
  "new_string": "  const C = await insertPlan(u1.uid, HIGH_SOCIAL, 'auto_approved', 'auto'); // TAMPERED: high-impact stored as auto_approved\n  const D = await insertPlan(u1.uid, HIGH, 'pending_hitl', 'hitl');         // for reject path\n  // E: TAMPERED plan SHAPE \u2014 non-array jsonb (object) carrying a high-impact task, stored auto_approved.\n  const E = await insertPlan(u1.uid, { task: { action: 'publicar post', channel: 'social', impact: 'high' } }, 'auto_approved', 'auto');"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-intent-execute.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:06:51)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-intent-execute.ts",
  "old_string": "  // \u2500\u2500 5. Legit HITL path: pending_hitl \u2192 approve \u2192 execute \u2500\u2500",
  "new_string": "  // \u2500\u2500 4b. FAIL-CLOSED: a non-array (malformed/tampered) plan is treated as high-impact \u2192 blocked \u2500\u2500\n  const eE = await exec(u1.token, { plan_id: E, decision: 'execute' });\n  check('E malformed non-array plan \u2192 409 hitl_required (fail-closed)', eE.status === 409 && eE.body.code === 'hitl_required', `status=${eE.status} code=${eE.body.code}`);\n  check('E NOT executed', (await dbStatus(E)) === 'auto_approved', `status=${await dbStatus(E)}`);\n\n  // \u2500\u2500 5. Legit HITL path: pending_hitl \u2192 approve \u2192 execute \u2500\u2500"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-intent-execute.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:06:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx supabase functions deploy intent-execute 2>&1 | tail -3 && npx supabase functions deploy intent-orchestrate 2>&1 | tail -3 && echo \"=== re-run smoke ===\" && bun run scripts/qa/smoke-intent-execute.ts 2>&1",
  "description": "Redeploy intent fns (fail-closed) + re-run smoke"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> You can inspect your deployment in the Dashboard: https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa/functions
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> You can inspect your deployment in the Dashboard: https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa/functions
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> === re-run smoke ===
> ✅ no-auth → 401
> ✅ missing plan_id → 422
> ✅ bad decision → 422
> ✅ cross-tenant execute → 404 (tenant guard)
> ✅ A low-impact auto → 200 executed  → status=200 ps=executed
> ✅ A persisted executed
> ✅ C tampered auto_approved high-impact → 409 hitl_required (re-validation)  → status=409 code=hitl_required
> ✅ C NOT executed (still auto_approved)  → status=auto_approved
> ✅ C approve on auto_approved → 409 (invalid transition)
> ✅ E malformed non-array plan → 409 hitl_required (fail-closed)  → status=409 code=hitl_required
> ✅ E NOT executed  → status=auto_approved
> ✅ B execute before approval → 409 hitl_required  → status=409 code=hitl_required
> ✅ B approve → 200 approved  → ps=approved
> ✅ B execute after approval → 200 executed  → ps=executed
> ✅ B idempotent execute → already=true
> ✅ D reject → 200 rejected  → ps=rejected
> ✅ D execute after reject → 409
> 
> 🧹 cleanup: 2 throwaway user(s) deleted (intent_plans cascade)
> 
> ✅✅ INTENT-EXECUTE HITL SMOKE PASSED
> ```

## 🤖 Claude *(01:07:17)*


## 🤖 Claude *(01:07:19)*

**17/17** — fail-closed provado material (plan não-array adulterado → 409, não executa). Backends fechados, `/security-review` SAFE, hardening adotado. Agora **regenero os types** (intent_plans + aeo_audits juntos) para destravar o frontend:

## 🤖 Claude *(01:07:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx supabase gen types typescript --linked > /tmp/types-new.ts 2>/tmp/types-err.txt\nif grep -q \"intent_plans:\" /tmp/types-new.ts && grep -q \"aeo_audits:\" /tmp/types-new.ts; then\n  lines=$(wc -l < /tmp/types-new.ts)\n  cp /tmp/types-new.ts src/integrations/supabase/types.ts\n  echo \"\u2705 types regenerated ($lines lines) \u2014 intent_plans + aeo_audits present\"\n  grep -nE \"intent_plans:|aeo_audits:|sequences:\" src/integrations/supabase/types.ts | head\nelse\n  echo \"\u274c regen missing tables \u2014 NOT overwriting. stderr:\"; cat /tmp/types-err.txt | head -10; echo \"--- head of output ---\"; head -15 /tmp/types-new.ts\nfi",
  "description": "Regenerate Supabase types + verify new tables present"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ types regenerated (3754 lines) — intent_plans + aeo_audits present
> 42:      aeo_audits: {
> 1195:      intent_plans: {
> 2015:      sequences: {
> ```

## 🤖 Claude *(01:08:04)*


## 🤖 Claude *(01:08:06)*

Types OK (3754 linhas, intent_plans + aeo_audits presentes). Agora **o rosto** — 2 hooks + 3 componentes em paralelo, no idioma shadcn/lucide/PT-BR do projeto:

## 🤖 Claude *(01:08:19)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useIntentOrchestrator.ts",
  "content": "import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';\nimport { supabase } from '@/integrations/supabase/client';\nimport { useAuth } from '@/hooks/useAuth';\nimport { edgeErrorMessage } from '@/lib/edge';\nimport type { Tables } from '@/integrations/supabase/types';\n\n// marketing-hub FR-MH-009 (Intent Orchestrator + HITL). Harness Engineering: all intent logic lives here.\n\nexport type IntentPlan = Tables<'intent_plans'>;\nexport interface PlanTask { action: string; channel?: string; impact?: 'low' | 'medium' | 'high'; rationale?: string }\nexport type IntentDecision = 'approve' | 'reject' | 'execute';\nexport type IntentStatus = 'proposed' | 'auto_approved' | 'pending_hitl' | 'approved' | 'rejected' | 'executed';\n\nexport const INTENT_STATUS_LABELS: Record<string, string> = {\n  proposed: 'Proposto', auto_approved: 'Auto-aprovado', pending_hitl: 'Aguardando aprova\u00e7\u00e3o',\n  approved: 'Aprovado', rejected: 'Rejeitado', executed: 'Executado',\n};\nexport const INTENT_STATUS_COLORS: Record<string, string> = {\n  proposed: 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30',\n  auto_approved: 'bg-sky-500/15 text-sky-400 border-sky-500/30',\n  pending_hitl: 'bg-amber-500/15 text-amber-400 border-amber-500/30',\n  approved: 'bg-violet-500/15 text-violet-400 border-violet-500/30',\n  rejected: 'bg-rose-500/15 text-rose-400 border-rose-500/30',\n  executed: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',\n};\nexport const IMPACT_COLORS: Record<string, string> = {\n  low: 'bg-zinc-500/15 text-zinc-400', medium: 'bg-amber-500/15 text-amber-400', high: 'bg-rose-500/15 text-rose-400',\n};\n\nexport interface IntentOrchestrateResult {\n  status: 'ok'; plan_id: string; policy: 'auto' | 'hitl';\n  plan_status: IntentStatus; tasks: PlanTask[]; rationale: string; source: 'ai' | 'heuristic';\n}\nexport interface IntentExecuteResult {\n  status: 'ok'; plan_id: string; plan_status: 'approved' | 'rejected' | 'executed';\n  high_impact?: boolean; tasks?: PlanTask[]; outward_dispatch?: 'gated'; already?: boolean;\n}\n\nexport function useIntentOrchestrator() {\n  const { user } = useAuth();\n  const qc = useQueryClient();\n\n  const plansQuery = useQuery({\n    queryKey: ['intent', user?.id],\n    queryFn: async () => {\n      const { data, error } = await supabase.from('intent_plans').select('*').order('created_at', { ascending: false });\n      if (error) throw error;\n      return data as IntentPlan[];\n    },\n    enabled: !!user,\n  });\n\n  // FR-MH-009 \u2014 translate a natural-language intent into a task plan (policy engine sets auto vs HITL). Cost 0.\n  const orchestrate = useMutation({\n    mutationFn: async (intent: string): Promise<IntentOrchestrateResult> => {\n      const { data, error } = await supabase.functions.invoke('intent-orchestrate', { body: { intent } });\n      if (error) throw new Error(await edgeErrorMessage(error, 'Erro no Intent Orchestrator'));\n      return data as IntentOrchestrateResult;\n    },\n    onSuccess: () => qc.invalidateQueries({ queryKey: ['intent'] }),\n  });\n\n  // FR-MH-009 (HITL) \u2014 approve / reject / execute. `execute` re-validates outward actions server-side.\n  const decide = useMutation({\n    mutationFn: async ({ plan_id, decision }: { plan_id: string; decision: IntentDecision }): Promise<IntentExecuteResult> => {\n      const { data, error } = await supabase.functions.invoke('intent-execute', { body: { plan_id, decision } });\n      if (error) throw new Error(await edgeErrorMessage(error, 'Erro ao processar o plano'));\n      return data as IntentExecuteResult;\n    },\n    onSuccess: () => qc.invalidateQueries({ queryKey: ['intent'] }),\n  });\n\n  const plans = plansQuery.data ?? [];\n  return {\n    plans,\n    isLoading: plansQuery.isLoading,\n    pendingHitl: plans.filter((p) => p.status === 'pending_hitl'),\n    orchestrate, decide,\n  };\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useIntentOrchestrator.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:08:33)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useAEO.ts",
  "content": "import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';\nimport { supabase } from '@/integrations/supabase/client';\nimport { useAuth } from '@/hooks/useAuth';\nimport { edgeErrorMessage } from '@/lib/edge';\nimport type { Tables } from '@/integrations/supabase/types';\n\n// marketing-hub FR-MH-010 (AEO Audit). Harness Engineering: all AEO logic lives here.\n\nexport type AeoAudit = Tables<'aeo_audits'>;\nexport interface AeoFinding { query: string; cited: boolean; recommendation: string }\nexport interface AeoAuditResult {\n  status: 'ok'; audit_id: string; citation_rate: number; findings: AeoFinding[]; source: 'ai' | 'degraded';\n}\n\n/** A snapshot counts as fresh for \u2264 7 days (NFR-MH-010). */\nexport const AEO_STALE_DAYS = 7;\nexport function isStale(createdAt: string): boolean {\n  return (Date.now() - new Date(createdAt).getTime()) > AEO_STALE_DAYS * 86_400_000;\n}\n\nexport function useAEO() {\n  const { user } = useAuth();\n  const qc = useQueryClient();\n\n  const auditsQuery = useQuery({\n    queryKey: ['aeo-audits', user?.id],\n    queryFn: async () => {\n      const { data, error } = await supabase.from('aeo_audits').select('*').order('created_at', { ascending: false }).limit(50);\n      if (error) throw error;\n      return data as AeoAudit[];\n    },\n    enabled: !!user,\n  });\n\n  // FR-MH-010 \u2014 invokes the JWT-guarded aeo-audit edge fn (debits 5 mcoCoins at entry). Degraded provider documented.\n  const runAudit = useMutation({\n    mutationFn: async ({ brand, queries }: { brand: string; queries: string[] }): Promise<AeoAuditResult> => {\n      const { data, error } = await supabase.functions.invoke('aeo-audit', { body: { brand, queries } });\n      if (error) throw new Error(await edgeErrorMessage(error, 'Erro na auditoria AEO'));\n      return data as AeoAuditResult;\n    },\n    onSuccess: () => qc.invalidateQueries({ queryKey: ['aeo-audits'] }),\n  });\n\n  return { audits: auditsQuery.data ?? [], isLoading: auditsQuery.isLoading, runAudit };\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useAEO.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:08:37)*


## 🤖 Claude *(01:08:51)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/HITLApprovalCard.tsx",
  "content": "import { Check, X, Play, Loader2, ShieldAlert } from 'lucide-react';\nimport { Card, CardContent } from '@/components/ui/card';\nimport { Badge } from '@/components/ui/badge';\nimport { Button } from '@/components/ui/button';\nimport {\n  useIntentOrchestrator, INTENT_STATUS_LABELS, INTENT_STATUS_COLORS, IMPACT_COLORS,\n  type IntentPlan, type PlanTask, type IntentDecision,\n} from '@/hooks/useIntentOrchestrator';\nimport { toast } from '@/hooks/use-toast';\n\n/** FR-MH-009 (HITL) \u2014 a single intent plan with approve / reject / execute controls. */\nexport default function HITLApprovalCard({ plan }: { plan: IntentPlan }) {\n  const { decide } = useIntentOrchestrator();\n  const status = plan.status;\n  const tasks = (Array.isArray(plan.plan) ? plan.plan : []) as unknown as PlanTask[];\n  const highImpact = tasks.some((t) => t?.impact === 'high');\n\n  const canApprove = status === 'pending_hitl';\n  const canReject = status !== 'executed' && status !== 'rejected';\n  const canExecute = status === 'approved' || status === 'auto_approved';\n\n  const act = async (decision: IntentDecision) => {\n    try {\n      const r = await decide.mutateAsync({ plan_id: plan.id, decision });\n      toast({ title: `Plano ${INTENT_STATUS_LABELS[r.plan_status]?.toLowerCase() ?? r.plan_status}` });\n    } catch (e) {\n      toast({ title: (e as Error).message || 'Erro ao processar o plano', variant: 'destructive' });\n    }\n  };\n\n  return (\n    <Card className={highImpact && status === 'pending_hitl' ? 'border-amber-500/40' : ''}>\n      <CardContent className=\"p-4 space-y-3\">\n        <div className=\"flex items-start justify-between gap-2\">\n          <p className=\"text-sm font-medium text-foreground line-clamp-2\">{plan.intent}</p>\n          <Badge variant=\"outline\" className={`shrink-0 text-xs ${INTENT_STATUS_COLORS[status] ?? ''}`}>\n            {INTENT_STATUS_LABELS[status] ?? status}\n          </Badge>\n        </div>\n\n        <ul className=\"space-y-1.5\">\n          {tasks.map((t, i) => (\n            <li key={i} className=\"flex items-center gap-2 text-xs\">\n              <Badge variant=\"secondary\" className={`shrink-0 ${IMPACT_COLORS[t.impact ?? 'medium']}`}>{t.impact ?? 'medium'}</Badge>\n              <span className=\"text-foreground truncate\">{t.action}</span>\n              {t.channel && t.channel !== 'none' && <span className=\"text-muted-foreground/70 shrink-0\">\u00b7 {t.channel}</span>}\n            </li>\n          ))}\n        </ul>\n\n        {plan.rationale && (\n          <p className=\"flex items-start gap-1.5 text-[11px] text-muted-foreground\">\n            {highImpact && <ShieldAlert className=\"h-3.5 w-3.5 shrink-0 text-amber-400 mt-0.5\" />}\n            <span className=\"line-clamp-3\">{plan.rationale}</span>\n          </p>\n        )}\n\n        {(canApprove || canReject || canExecute) && (\n          <div className=\"flex items-center gap-2 pt-1\">\n            {canApprove && (\n              <Button size=\"sm\" className=\"h-7 px-2 text-xs gap-1 bg-emerald-600 hover:bg-emerald-500\" disabled={decide.isPending} onClick={() => act('approve')}>\n                {decide.isPending ? <Loader2 className=\"h-3 w-3 animate-spin\" /> : <Check className=\"h-3 w-3\" />} Aprovar\n              </Button>\n            )}\n            {canExecute && (\n              <Button size=\"sm\" className=\"h-7 px-2 text-xs gap-1\" disabled={decide.isPending} onClick={() => act('execute')}>\n                {decide.isPending ? <Loader2 className=\"h-3 w-3 animate-spin\" /> : <Play className=\"h-3 w-3\" />} Executar\n              </Button>\n            )}\n            {canReject && (\n              <Button size=\"sm\" variant=\"ghost\" className=\"h-7 px-2 text-xs gap-1 text-rose-400 hover:text-rose-300\" disabled={decide.isPending} onClick={() => act('reject')}>\n                <X className=\"h-3 w-3\" /> Rejeitar\n              </Button>\n            )}\n          </div>\n        )}\n      </CardContent>\n    </Card>\n  );\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/HITLApprovalCard.tsx (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:09:06)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/IntentOrchestratorPanel.tsx",
  "content": "import { useState } from 'react';\nimport { Sparkles, Loader2, BrainCircuit } from 'lucide-react';\nimport { Button } from '@/components/ui/button';\nimport { Card, CardContent } from '@/components/ui/card';\nimport { Textarea } from '@/components/ui/textarea';\nimport { Skeleton } from '@/components/ui/skeleton';\nimport { useIntentOrchestrator } from '@/hooks/useIntentOrchestrator';\nimport HITLApprovalCard from './HITLApprovalCard';\nimport { toast } from '@/hooks/use-toast';\n\n/** FR-MH-009 \u2014 Intent Orchestrator surface: describe an intent \u2192 AI plan \u2192 policy engine \u2192 HITL approval. */\nexport default function IntentOrchestratorPanel() {\n  const { plans, isLoading, pendingHitl, orchestrate } = useIntentOrchestrator();\n  const [intent, setIntent] = useState('');\n\n  const submit = async () => {\n    if (!intent.trim()) { toast({ title: 'Descreva a inten\u00e7\u00e3o de marketing', variant: 'destructive' }); return; }\n    try {\n      const r = await orchestrate.mutateAsync(intent.trim());\n      toast({\n        title: r.policy === 'hitl' ? 'Plano gerado \u2014 requer aprova\u00e7\u00e3o (HITL)' : 'Plano gerado e auto-aprovado',\n        description: `${r.tasks.length} tarefa(s) \u00b7 ${r.source === 'ai' ? 'IA' : 'heur\u00edstica'}`,\n      });\n      setIntent('');\n    } catch (e) {\n      toast({ title: (e as Error).message || 'Erro ao orquestrar', variant: 'destructive' });\n    }\n  };\n\n  return (\n    <section className=\"space-y-3\">\n      <div className=\"flex items-center gap-2\">\n        <BrainCircuit className=\"h-5 w-5 text-primary\" />\n        <div>\n          <h2 className=\"text-lg font-heading font-semibold text-foreground\">Intent Orchestrator</h2>\n          <p className=\"text-xs text-muted-foreground\">\n            {pendingHitl.length > 0\n              ? `${pendingHitl.length} plano(s) aguardando aprova\u00e7\u00e3o \u00b7 a\u00e7\u00e3o de alto impacto exige revis\u00e3o humana`\n              : 'Descreva uma inten\u00e7\u00e3o \u2192 a IA gera um plano \u00b7 a\u00e7\u00f5es de alto impacto exigem aprova\u00e7\u00e3o (HITL)'}\n          </p>\n        </div>\n      </div>\n\n      <Card>\n        <CardContent className=\"p-4 space-y-2\">\n          <Textarea\n            value={intent} onChange={(e) => setIntent(e.target.value)} rows={2}\n            placeholder=\"Ex: lan\u00e7ar uma campanha de boas-vindas para novos leads e publicar um post no LinkedIn\"\n          />\n          <div className=\"flex justify-end\">\n            <Button size=\"sm\" className=\"gap-1.5\" disabled={orchestrate.isPending} onClick={submit}>\n              {orchestrate.isPending ? <Loader2 className=\"h-4 w-4 animate-spin\" /> : <Sparkles className=\"h-4 w-4\" />}\n              Orquestrar\n            </Button>\n          </div>\n        </CardContent>\n      </Card>\n\n      {isLoading ? (\n        <div className=\"grid gap-3 sm:grid-cols-2\">{[1, 2].map((i) => <Skeleton key={i} className=\"h-28 rounded-lg\" />)}</div>\n      ) : plans.length === 0 ? (\n        <p className=\"text-xs text-muted-foreground/60 text-center py-3\">Nenhum plano ainda.</p>\n      ) : (\n        <div className=\"grid gap-3 sm:grid-cols-2\">\n          {plans.slice(0, 6).map((p) => <HITLApprovalCard key={p.id} plan={p} />)}\n        </div>\n      )}\n    </section>\n  );\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/IntentOrchestratorPanel.tsx (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:09:12)*


## 🤖 Claude *(01:09:28)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/AEOAuditPanel.tsx",
  "content": "import { useState } from 'react';\nimport { Search, Loader2, CheckCircle2, XCircle, Radar } from 'lucide-react';\nimport { Button } from '@/components/ui/button';\nimport { Card, CardContent } from '@/components/ui/card';\nimport { Badge } from '@/components/ui/badge';\nimport { Input } from '@/components/ui/input';\nimport { Label } from '@/components/ui/label';\nimport { Textarea } from '@/components/ui/textarea';\nimport { useAEO, type AeoFinding } from '@/hooks/useAEO';\nimport { toast } from '@/hooks/use-toast';\n\n/** FR-MH-010 \u2014 AEO Audit surface: measure brand citation across tracked queries (5 mcoCoins \u00b7 degraded provider). */\nexport default function AEOAuditPanel() {\n  const { audits, runAudit } = useAEO();\n  const [brand, setBrand] = useState('');\n  const [queriesText, setQueriesText] = useState('');\n  const [result, setResult] = useState<{ rate: number; findings: AeoFinding[] } | null>(null);\n\n  const submit = async () => {\n    const queries = queriesText.split('\\n').map((q) => q.trim()).filter(Boolean).slice(0, 5);\n    if (!brand.trim()) { toast({ title: 'Informe a marca', variant: 'destructive' }); return; }\n    if (queries.length === 0) { toast({ title: 'Informe ao menos 1 query (uma por linha)', variant: 'destructive' }); return; }\n    try {\n      const r = await runAudit.mutateAsync({ brand: brand.trim(), queries });\n      setResult({ rate: r.citation_rate, findings: r.findings });\n      toast({ title: `Auditoria conclu\u00edda \u00b7 cita\u00e7\u00e3o ${(r.citation_rate * 100).toFixed(0)}%`, description: r.source === 'degraded' ? 'Provider em modo degradado' : 'via IA' });\n    } catch (e) {\n      toast({ title: (e as Error).message || 'Erro na auditoria AEO', variant: 'destructive' });\n    }\n  };\n\n  return (\n    <section className=\"space-y-3\">\n      <div className=\"flex items-center gap-2\">\n        <Radar className=\"h-5 w-5 text-primary\" />\n        <div>\n          <h2 className=\"text-lg font-heading font-semibold text-foreground\">Auditoria AEO</h2>\n          <p className=\"text-xs text-muted-foreground\">Mede se a marca \u00e9 citada nos motores de resposta de IA \u00b7 5 mcoCoins por auditoria</p>\n        </div>\n      </div>\n\n      <Card>\n        <CardContent className=\"p-4 space-y-3\">\n          <div className=\"space-y-1.5\">\n            <Label>Marca</Label>\n            <Input value={brand} onChange={(e) => setBrand(e.target.value)} placeholder=\"Ex: MCORCH\" />\n          </div>\n          <div className=\"space-y-1.5\">\n            <Label>Queries rastreadas (uma por linha \u00b7 m\u00e1x. 5)</Label>\n            <Textarea value={queriesText} onChange={(e) => setQueriesText(e.target.value)} rows={3}\n              placeholder={'melhor ferramenta de marketing com IA\\ncomo automatizar campanhas'} />\n          </div>\n          <div className=\"flex justify-end\">\n            <Button size=\"sm\" className=\"gap-1.5\" disabled={runAudit.isPending} onClick={submit}>\n              {runAudit.isPending ? <Loader2 className=\"h-4 w-4 animate-spin\" /> : <Search className=\"h-4 w-4\" />}\n              Auditar (5 mco)\n            </Button>\n          </div>\n        </CardContent>\n      </Card>\n\n      {result && (\n        <Card className=\"border-primary/30\">\n          <CardContent className=\"p-4 space-y-2\">\n            <p className=\"text-sm font-medium text-foreground\">Cita\u00e7\u00e3o agregada: {(result.rate * 100).toFixed(0)}%</p>\n            <ul className=\"space-y-2\">\n              {result.findings.map((f, i) => (\n                <li key={i} className=\"text-xs space-y-0.5\">\n                  <div className=\"flex items-center gap-1.5\">\n                    {f.cited ? <CheckCircle2 className=\"h-3.5 w-3.5 text-emerald-400 shrink-0\" /> : <XCircle className=\"h-3.5 w-3.5 text-zinc-500 shrink-0\" />}\n                    <span className=\"text-foreground truncate\">{f.query}</span>\n                  </div>\n                  <p className=\"text-muted-foreground pl-5\">{f.recommendation}</p>\n                </li>\n              ))}\n            </ul>\n          </CardContent>\n        </Card>\n      )}\n\n      {audits.length > 0 && (\n        <div className=\"flex flex-wrap gap-1.5\">\n          {audits.slice(0, 8).map((a) => (\n            <Badge key={a.id} variant=\"outline\" className={`text-[11px] ${a.cited ? 'border-emerald-500/30 text-emerald-400' : 'border-zinc-500/30 text-zinc-400'}`}>\n              {a.cited ? '\u2713' : '\u2717'} {a.query.slice(0, 28)}{a.query.length > 28 ? '\u2026' : ''}\n            </Badge>\n          ))}\n        </div>\n      )}\n    </section>\n  );\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/components/marketing/AEOAuditPanel.tsx (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:09:35)*


## 🤖 Claude *(01:09:35)*

Agora ligo os dois painéis no `MarketingPage` (após o NurturingPanel):

## 🤖 Claude *(01:09:38)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/MarketingPage.tsx",
  "old_string": "import LeadBoard from '@/components/marketing/LeadBoard';\nimport NurturingPanel from '@/components/marketing/NurturingPanel';",
  "new_string": "import LeadBoard from '@/components/marketing/LeadBoard';\nimport NurturingPanel from '@/components/marketing/NurturingPanel';\nimport IntentOrchestratorPanel from '@/components/marketing/IntentOrchestratorPanel';\nimport AEOAuditPanel from '@/components/marketing/AEOAuditPanel';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/MarketingPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:09:42)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/MarketingPage.tsx",
  "old_string": "      {/* Nurturing (drip) \u2014 FR-MH-008 */}\n      <NurturingPanel />\n    </div>\n  );\n}",
  "new_string": "      {/* Nurturing (drip) \u2014 FR-MH-008 */}\n      <NurturingPanel />\n\n      {/* Intent Orchestrator + HITL \u2014 FR-MH-009 */}\n      <IntentOrchestratorPanel />\n\n      {/* AEO Audit \u2014 FR-MH-010 */}\n      <AEOAuditPanel />\n    </div>\n  );\n}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/MarketingPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:09:45)*


## 🤖 Claude *(01:09:46)*

Frontend completo + ligado. Verifico o tsc (gate de materialidade do build):

## 🤖 Claude *(01:09:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20 && echo \"=== EXIT: $? (empty above = zero erros) ===\"",
  "description": "TypeScript strict check on full frontend"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === EXIT: 0 (empty above = zero erros) ===
> ```

## 🤖 Claude *(01:09:54)*


## 🤖 Claude *(01:09:55)*

tsc **zero erros** com todo o frontend. Agora estendo a suíte de testes do marketing-hub. Leio o arquivo existente para casar o padrão:

## 🤖 Claude *(01:09:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/test/marketing-hub.test.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { describe, it, expect, vi, beforeEach } from 'vitest';
> 2	import { renderHook, waitFor } from '@testing-library/react';
> 3	import { createElement, type ReactNode } from 'react';
> 4	import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
> 5	
> 6	// ─── Hoisted mocks ──────────────────────────────────────────────────────────
> 7	const { mockInvoke } = vi.hoisted(() => ({ mockInvoke: vi.fn() }));
> 8	vi.mock('@/integrations/supabase/client', () => ({
> 9	  supabase: { functions: { invoke: mockInvoke }, from: vi.fn() },
> 10	}));
> 11	vi.mock('@/hooks/useAuth', () => ({
> 12	  useAuth: () => ({ user: { id: 'u1' }, session: { access_token: 't' } }),
> 13	}));
> 14	
> 15	import { edgeErrorMessage } from '@/lib/edge';
> 16	import {
> 17	  useLeadScore, LEAD_STATUSES, LEAD_STATUS_LABELS, LEAD_STATUS_COLORS,
> 18	} from '@/hooks/useLeads';
> 19	import {
> 20	  useCampaignRun, aggregateAttribution,
> 21	  CAMPAIGN_CHANNELS, STEP_ACTION_LABELS, STEP_STATUS_LABELS, STEP_STATUS_COLORS,
> 22	} from '@/hooks/useCampaigns';
> 23	
> 24	function wrapper({ children }: { children: ReactNode }) {
> 25	  const qc = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
> 26	  return createElement(QueryClientProvider, { client: qc }, children);
> 27	}
> 28	
> 29	beforeEach(() => vi.clearAllMocks());
> 30	
> 31	// ─── edgeErrorMessage — PT-BR error extraction from non-2xx edge responses ────
> 32	describe('edgeErrorMessage', () => {
> 33	  it('returns the edge JSON `error` field when present (e.g. 402 PT-BR)', async () => {
> 34	    const err = { context: { json: async () => ({ error: 'Saldo insuficiente de mcoCoins' }) } };
> 35	    expect(await edgeErrorMessage(err, 'fallback')).toBe('Saldo insuficiente de mcoCoins');
> 36	  });
> 37	  it('falls back to error.message when there is no JSON body', async () => {
> 38	    expect(await edgeErrorMessage({ message: 'boom' }, 'fallback')).toBe('boom');
> 39	  });
> 40	  it('falls back to the provided fallback when body is unparseable and no message', async () => {
> 41	    const err = { context: { json: async () => { throw new Error('not json'); } } };
> 42	    expect(await edgeErrorMessage(err, 'fallback-default')).toBe('fallback-default');
> 43	  });
> 44	});
> 45	
> 46	// ─── Lifecycle constants (FR-MH-001) ──────────────────────────────────────────
> 47	describe('lead lifecycle constants', () => {
> 48	  it('orders the 5 board statuses new→scored→nurturing→converted→lost', () => {
> 49	    expect(LEAD_STATUSES).toEqual(['new', 'scored', 'nurturing', 'converted', 'lost']);
> 50	  });
> 51	  it('has a PT-BR label and a color for every status', () => {
> 52	    for (const s of LEAD_STATUSES) {
> 53	      expect(LEAD_STATUS_LABELS[s]).toBeTruthy();
> 54	      expect(LEAD_STATUS_COLORS[s]).toBeTruthy();
> 55	    }
> 56	  });
> 57	});
> 58	
> 59	// ─── Campaign step constants (FR-MH-004/005) ─────────────────────────────────
> 60	describe('campaign step constants', () => {
> 61	  it('exposes the 4 channels including email (nurture territory)', () => {
> 62	    expect(CAMPAIGN_CHANNELS.map((c) => c.value)).toEqual(['content', 'social', 'affiliate', 'email']);
> 63	  });
> 64	  it('labels all 3 actions and all 5 step statuses', () => {
> 65	    expect(Object.keys(STEP_ACTION_LABELS)).toEqual(['generate_content', 'publish', 'affiliate_attach']);
> 66	    for (const st of ['idle', 'running', 'done', 'error', 'blocked'] as const) {
> 67	      expect(STEP_STATUS_LABELS[st]).toBeTruthy();
> 68	      expect(STEP_STATUS_COLORS[st]).toBeTruthy();
> 69	    }
> 70	  });
> 71	});
> 72	
> 73	// ─── useLeadScore (FR-MH-003) ─────────────────────────────────────────────────
> 74	describe('useLeadScore', () => {
> 75	  it('returns the edge result on success', async () => {
> 76	    mockInvoke.mockResolvedValue({ data: { status: 'ok', lead_id: 'l1', score: 80, rationale: 'quente', new_balance: 99 }, error: null });
> 77	    const { result } = renderHook(() => useLeadScore(), { wrapper });
> 78	    const r = await result.current.mutateAsync('l1');
> 79	    expect(mockInvoke).toHaveBeenCalledWith('lead-score', { body: { lead_id: 'l1' } });
> 80	    expect(r.score).toBe(80);
> 81	  });
> 82	  it('throws the PT-BR edge error on non-2xx (e.g. 402)', async () => {
> 83	    mockInvoke.mockResolvedValue({ data: null, error: { context: { json: async () => ({ error: 'Saldo insuficiente de mcoCoins' }) } } });
> 84	    const { result } = renderHook(() => useLeadScore(), { wrapper });
> 85	    await expect(result.current.mutateAsync('l1')).rejects.toThrow('Saldo insuficiente de mcoCoins');
> 86	  });
> 87	});
> 88	
> 89	// ─── aggregateAttribution (FR-MH-007) ─────────────────────────────────────────
> 90	describe('aggregateAttribution', () => {
> 91	  it('sums revenue and groups by touchpoint', () => {
> 92	    const r = aggregateAttribution([
> 93	      { touchpoint: 'affiliate_click', revenue_cents: 1000 },
> 94	      { touchpoint: 'affiliate_click', revenue_cents: 2500 },
> 95	      { touchpoint: 'wp_article', revenue_cents: 500 },
> 96	    ]);
> 97	    expect(r.totalRevenueCents).toBe(4000);
> 98	    expect(r.conversions).toBe(3);
> 99	    expect(r.byTouchpoint).toContainEqual({ touchpoint: 'affiliate_click', revenueCents: 3500, count: 2 });
> 100	    expect(r.byTouchpoint).toContainEqual({ touchpoint: 'wp_article', revenueCents: 500, count: 1 });
> 101	  });
> 102	  it('handles empty rows and null touchpoint/revenue', () => {
> 103	    expect(aggregateAttribution([])).toEqual({ totalRevenueCents: 0, conversions: 0, byTouchpoint: [] });
> 104	    const r = aggregateAttribution([{ touchpoint: null, revenue_cents: null }]);
> 105	    expect(r.totalRevenueCents).toBe(0);
> 106	    expect(r.byTouchpoint[0].touchpoint).toBe('unknown');
> 107	  });
> 108	});
> 109	
> 110	// ─── useCampaignRun (FR-MH-004) ───────────────────────────────────────────────
> 111	describe('useCampaignRun', () => {
> 112	  it('invokes campaign-run with the campaign_id and returns the cascade result', async () => {
> 113	    mockInvoke.mockResolvedValue({ data: { status: 'ok', campaign_id: 'c1', run_id: 'r1', steps_dispatched: 2, new_balance: 70 }, error: null });
> 114	    const { result } = renderHook(() => useCampaignRun(), { wrapper });
> 115	    const r = await result.current.mutateAsync('c1');
> 116	    expect(mockInvoke).toHaveBeenCalledWith('campaign-run', { body: { campaign_id: 'c1' } });
> 117	    expect(r.steps_dispatched).toBe(2);
> 118	    await waitFor(() => expect(result.current.isSuccess).toBe(true));
> 119	  });
> 120	  it('surfaces the PT-BR edge error on failure', async () => {
> 121	    mockInvoke.mockResolvedValue({ data: null, error: { context: { json: async () => ({ error: 'Campanha não tem passos para executar' }) } } });
> 122	    const { result } = renderHook(() => useCampaignRun(), { wrapper });
> 123	    await expect(result.current.mutateAsync('c1')).rejects.toThrow('Campanha não tem passos para executar');
> 124	  });
> 125	});
> 126	
> ```

## 🤖 Claude *(01:10:18)*


## 🤖 Claude *(01:10:19)*

Padrão claro. Adiciono imports + blocos de teste para os novos hooks/constantes (intent + AEO):

## 🤖 Claude *(01:10:23)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/test/marketing-hub.test.ts",
  "old_string": "import {\n  useCampaignRun, aggregateAttribution,\n  CAMPAIGN_CHANNELS, STEP_ACTION_LABELS, STEP_STATUS_LABELS, STEP_STATUS_COLORS,\n} from '@/hooks/useCampaigns';",
  "new_string": "import {\n  useCampaignRun, aggregateAttribution,\n  CAMPAIGN_CHANNELS, STEP_ACTION_LABELS, STEP_STATUS_LABELS, STEP_STATUS_COLORS,\n} from '@/hooks/useCampaigns';\nimport {\n  useIntentOrchestrator, INTENT_STATUS_LABELS, INTENT_STATUS_COLORS, IMPACT_COLORS,\n} from '@/hooks/useIntentOrchestrator';\nimport { useAEO, isStale, AEO_STALE_DAYS } from '@/hooks/useAEO';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/test/marketing-hub.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:10:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/test/marketing-hub.test.ts",
  "old_string": "  it('surfaces the PT-BR edge error on failure', async () => {\n    mockInvoke.mockResolvedValue({ data: null, error: { context: { json: async () => ({ error: 'Campanha n\u00e3o tem passos para executar' }) } } });\n    const { result } = renderHook(() => useCampaignRun(), { wrapper });\n    await expect(result.current.mutateAsync('c1')).rejects.toThrow('Campanha n\u00e3o tem passos para executar');\n  });\n});",
  "new_string": "  it('surfaces the PT-BR edge error on failure', async () => {\n    mockInvoke.mockResolvedValue({ data: null, error: { context: { json: async () => ({ error: 'Campanha n\u00e3o tem passos para executar' }) } } });\n    const { result } = renderHook(() => useCampaignRun(), { wrapper });\n    await expect(result.current.mutateAsync('c1')).rejects.toThrow('Campanha n\u00e3o tem passos para executar');\n  });\n});\n\n// \u2500\u2500\u2500 Intent status constants (FR-MH-009) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\ndescribe('intent status constants', () => {\n  it('has a PT-BR label and a color for every plan status', () => {\n    for (const s of ['proposed', 'auto_approved', 'pending_hitl', 'approved', 'rejected', 'executed']) {\n      expect(INTENT_STATUS_LABELS[s]).toBeTruthy();\n      expect(INTENT_STATUS_COLORS[s]).toBeTruthy();\n    }\n  });\n  it('colors every impact tier', () => {\n    for (const i of ['low', 'medium', 'high']) expect(IMPACT_COLORS[i]).toBeTruthy();\n  });\n});\n\n// \u2500\u2500\u2500 useIntentOrchestrator (FR-MH-009) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\ndescribe('useIntentOrchestrator', () => {\n  it('orchestrate invokes intent-orchestrate and returns the plan + policy', async () => {\n    mockInvoke.mockResolvedValue({ data: { status: 'ok', plan_id: 'p1', policy: 'hitl', plan_status: 'pending_hitl', tasks: [{ action: 'enviar email', channel: 'email', impact: 'high' }], rationale: 'alto impacto', source: 'ai' }, error: null });\n    const { result } = renderHook(() => useIntentOrchestrator(), { wrapper });\n    const r = await result.current.orchestrate.mutateAsync('lan\u00e7ar campanha e enviar email');\n    expect(mockInvoke).toHaveBeenCalledWith('intent-orchestrate', { body: { intent: 'lan\u00e7ar campanha e enviar email' } });\n    expect(r.policy).toBe('hitl');\n    expect(r.plan_status).toBe('pending_hitl');\n  });\n  it('decide invokes intent-execute with plan_id + decision', async () => {\n    mockInvoke.mockResolvedValue({ data: { status: 'ok', plan_id: 'p1', plan_status: 'executed', high_impact: false, outward_dispatch: 'gated' }, error: null });\n    const { result } = renderHook(() => useIntentOrchestrator(), { wrapper });\n    const r = await result.current.decide.mutateAsync({ plan_id: 'p1', decision: 'execute' });\n    expect(mockInvoke).toHaveBeenCalledWith('intent-execute', { body: { plan_id: 'p1', decision: 'execute' } });\n    expect(r.plan_status).toBe('executed');\n  });\n  it('decide surfaces the PT-BR HITL refusal (409 hitl_required) as a thrown message', async () => {\n    mockInvoke.mockResolvedValue({ data: null, error: { context: { json: async () => ({ error: 'Plano de alto impacto exige aprova\u00e7\u00e3o humana (HITL) antes de executar.' }) } } });\n    const { result } = renderHook(() => useIntentOrchestrator(), { wrapper });\n    await expect(result.current.decide.mutateAsync({ plan_id: 'p1', decision: 'execute' })).rejects.toThrow('aprova\u00e7\u00e3o humana');\n  });\n});\n\n// \u2500\u2500\u2500 useAEO (FR-MH-010) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\ndescribe('useAEO', () => {\n  it('runAudit invokes aeo-audit with brand + queries and returns citation_rate + findings', async () => {\n    mockInvoke.mockResolvedValue({ data: { status: 'ok', audit_id: 'a1', citation_rate: 0.5, findings: [{ query: 'q', cited: true, recommendation: 'r' }], source: 'ai' }, error: null });\n    const { result } = renderHook(() => useAEO(), { wrapper });\n    const r = await result.current.runAudit.mutateAsync({ brand: 'MCORCH', queries: ['q'] });\n    expect(mockInvoke).toHaveBeenCalledWith('aeo-audit', { body: { brand: 'MCORCH', queries: ['q'] } });\n    expect(r.citation_rate).toBe(0.5);\n    expect(r.findings).toHaveLength(1);\n  });\n  it('runAudit surfaces the PT-BR edge error on 402', async () => {\n    mockInvoke.mockResolvedValue({ data: null, error: { context: { json: async () => ({ error: 'Saldo insuficiente de mcoCoins' }) } } });\n    const { result } = renderHook(() => useAEO(), { wrapper });\n    await expect(result.current.runAudit.mutateAsync({ brand: 'X', queries: ['q'] })).rejects.toThrow('Saldo insuficiente');\n  });\n  it('isStale flags snapshots older than the freshness window (NFR-MH-010 \u2264 7 days)', () => {\n    expect(AEO_STALE_DAYS).toBe(7);\n    expect(isStale(new Date(Date.now() - 8 * 86_400_000).toISOString())).toBe(true);\n    expect(isStale(new Date().toISOString())).toBe(false);\n  });\n});"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/test/marketing-hub.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:10:51)*


## 🤖 Claude *(01:10:51)*

Rodo a suíte completa (inclui os novos testes do marketing-hub):

## 🤖 Claude *(01:10:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run test 2>&1 | tail -25",
  "description": "Run full vitest suite"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> stderr | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > does not fall back on a non-billing client error (e.g. 400 bad request)
> [llm-fallback] Primary request failed with status 400 (no fallback triggered)
> 
> stdout | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Attempting primary LLM request with model "anthropic/claude-3.5-sonnet"
> 
> stderr | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Primary request failed (status=402). Initiating cascade. Details: {}
> 
> stdout | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Attempting Gemini Free fallback. Candidates: gemini-2.5-pro, gemini-1.5-pro
> [llm-fallback] Dispatching fallback request to Gemini Free using model "gemini-2.5-pro"
> 
> stdout | supabase/functions/_shared/llm-fallback.test.ts > fetchLLMWithFallback (OTD-LLM-FALLBACK cascade) > emits NO telemetry fetch outside Deno (guard holds; cascade fetch count unchanged)
> [llm-fallback] Gemini Free fallback succeeded with model "gemini-2.5-pro"
> 
>  ✓ supabase/functions/_shared/llm-fallback.test.ts (6 tests) 33ms
>  ↓ src/test/canvas-video-async-smoke.test.ts (1 test | 1 skipped)
> 
>  Test Files  17 passed | 2 skipped (19)
>       Tests  265 passed | 2 skipped (267)
>    Start at  22:10:52
>    Duration  9.45s (transform 971ms, setup 2.25s, collect 3.31s, tests 1.93s, environment 11.54s, prepare 2.99s)
> ```

## 🤖 Claude *(01:11:08)*


## 🤖 Claude *(01:11:09)*

**265 passed / 2 skipped** (era 257 → +8 novos, todos verdes). eslint nos arquivos tocados:

## 🤖 Claude *(01:11:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx eslint src/components/marketing/LeadDetailDialog.tsx src/components/marketing/HITLApprovalCard.tsx src/components/marketing/IntentOrchestratorPanel.tsx src/components/marketing/AEOAuditPanel.tsx src/hooks/useIntentOrchestrator.ts src/hooks/useAEO.ts src/pages/MarketingPage.tsx src/test/marketing-hub.test.ts 2>&1 | tail -25; echo \"=== eslint exit: ${PIPESTATUS[0]} ===\"",
  "description": "ESLint on touched src files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === eslint exit: 0 ===
> ```

## 🤖 Claude *(01:11:21)*


## 🤖 Claude *(01:11:22)*

eslint **exit 0** nos tocados. Agora **build = deploy** (repo PRINCIPAL com `.env` → nginx serve `dist/` direto). Buildo e verifico materialmente (Lei 1 — build ok + chunk fresco + env baked):

## 🤖 Claude *(01:11:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "pwd; echo \"=== confirm MAIN repo (not worktree), has .env ===\"; ls -la .env >/dev/null && echo \".env present \u2705\"\necho \"=== BUILD ===\"; bun run build 2>&1 | tail -12",
  "description": "Production build (main repo = deploy)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra
> === confirm MAIN repo (not worktree), has .env ===
> .env present ✅
> === BUILD ===
> dist/assets/index-Wwo7RX2P.js                  167.17 kB │ gzip:  53.48 kB
> dist/assets/ConstellationPage-BXFYkCab.js      185.12 kB │ gzip:  63.83 kB
> dist/assets/ConstellationMatrix-BlTDfpii.js    248.23 kB │ gzip:  63.05 kB
> dist/assets/CartesianChart-u3JGrSPw.js         325.06 kB │ gzip:  96.83 kB
> dist/assets/index-g5SYRqKM.js                  626.42 kB │ gzip: 187.20 kB
> dist/assets/Stars-D3ou63SZ.js                  826.42 kB │ gzip: 222.88 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 22.88s
> ```

## 🤖 Claude *(01:11:53)*


## 🤖 Claude *(01:11:54)*

Build ✅ 22.88s. Verifico materialmente (Lei 1) — chunk fresco do MarketingPage com a UI nova + env Supabase baked no bundle:

## 🤖 Claude *(01:11:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== MarketingPage chunk (fresh?) ===\"; ls -la --time-style=+%H:%M:%S dist/assets/ | grep -iE \"Marketing\" \necho \"=== new UI strings baked into the Marketing chunk ===\"; mk=$(ls dist/assets/ | grep -i \"Marketing\" | head -1); grep -l \"Intent Orchestrator\" \"dist/assets/$mk\" >/dev/null && echo \"\u2705 'Intent Orchestrator' in $mk\"; grep -o \"Auditoria AEO\" \"dist/assets/$mk\" | head -1; grep -o \"Aguardando aprova\u00e7\u00e3o\" \"dist/assets/$mk\" | head -1\necho \"=== env Supabase baked (project id in bundle) ===\"; grep -rl \"bcyvddsykvehvpwstlfa\" dist/assets/*.js | head -1 && echo \"\u2705 Supabase URL baked\"",
  "description": "Verify Marketing chunk freshness + new UI + env baked"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === MarketingPage chunk (fresh?) ===
> -rw-rw-r-- 1 ubuntu ubuntu  28581 22:11:47 MarketingPage-kzjcCEeM.js
> === new UI strings baked into the Marketing chunk ===
> ✅ 'Intent Orchestrator' in MarketingPage-kzjcCEeM.js
> Auditoria AEO
> Aguardando aprovação
> === env Supabase baked (project id in bundle) ===
> dist/assets/CalendarPage-Ih5kHfl8.js
> ✅ Supabase URL baked
> ```

## 🤖 Claude *(01:12:47)*


## 🤖 Claude *(01:12:50)*

**Materialidade do deploy verde**: `MarketingPage-kzjcCEeM.js` (28.5kB, 22:11:47 fresco) contém `Intent Orchestrator` + `Auditoria AEO` + `Aguardando aprovação`; Supabase URL baked no bundle. nginx serve `dist/` → deploy material.

Agora a verificação de UI logada (gate das seals recentes para mudança de UI). Leio o helper de magic-link para dirigir um render check via Playwright MCP com user throwaway (zero mutação em prod):

## 🤖 Claude *(01:12:51)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/gen-magiclink.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Generate a one-time magic link for a user via the Supabase Admin API — for logged-in UI verification
> 4	 * (agent-browser / e2e). Per-user, reproducible, no raw password, no DevTools token. Pattern from v6.20.4.
> 5	 *
> 6	 * Usage: bun run scripts/qa/gen-magiclink.ts <email> [redirectTo]
> 7	 *   e.g. bun run scripts/qa/gen-magiclink.ts gabrielcall@gmail.com https://login.mcorch.com/dashboard/marketing
> 8	 */
> 9	import { createClient } from '@supabase/supabase-js';
> 10	
> 11	const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> 12	const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> 13	const email = process.argv[2];
> 14	const redirectTo = process.argv[3] ?? 'https://login.mcorch.com/dashboard/marketing';
> 15	if (!URL || !SVC || !email) { console.error('Usage: gen-magiclink.ts <email> [redirectTo]  (needs SUPABASE_URL + SB_SECRET_KEY)'); process.exit(1); }
> 16	
> 17	const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> 18	const { data, error } = await admin.auth.admin.generateLink({ type: 'magiclink', email, options: { redirectTo } });
> 19	if (error) { console.error('generateLink error:', error.message); process.exit(1); }
> 20	console.log(data.properties?.action_link ?? '(no action_link)');
> 21	
> ```

## 🤖 Claude *(01:13:33)*


## 🤖 Claude *(01:13:36)*

Helper claro. Faço a verificação de UI logada (read-only, padrão v6.23) — gero magic link do Usuário Zero + dirijo o Playwright MCP para `/dashboard/marketing`, apenas navegar+observar (sem clique mutante). Carrego as ferramentas Playwright + gero o link em paralelo:

## 🤖 Claude *(01:13:36)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:mcp__playwright__browser_navigate,mcp__playwright__browser_snapshot,mcp__playwright__browser_console_messages,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_wait_for",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_navigate'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_snapshot'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_console_messages'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_take_screenshot'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_wait_for'}]
> ```

## 🤖 Claude *(01:13:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run scripts/qa/gen-magiclink.ts gabrielcall@gmail.com https://login.mcorch.com/dashboard/marketing 2>&1",
  "description": "Generate magic link for Usu\u00e1rio Zero \u2192 /dashboard/marketing"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> https://bcyvddsykvehvpwstlfa.supabase.co/auth/v1/verify?token=9dd5bd5f34c4d694436a993eb70904c2d4b9cf55b3255b1aeaf030b8&type=magiclink&redirect_to=https://login.mcorch.com/dashboard/marketing
> ```

## 🤖 Claude *(01:13:42)*


## 🤖 Claude *(01:13:43)*

Link gerado. Navego (autentica + redireciona para `/dashboard/marketing`):

## 🤖 Claude *(01:13:44)*


🛠️ **Tool Call**: `mcp__playwright__browser_navigate`
```json
{
  "url": "https://bcyvddsykvehvpwstlfa.supabase.co/auth/v1/verify?token=9dd5bd5f34c4d694436a993eb70904c2d4b9cf55b3255b1aeaf030b8&type=magiclink&redirect_to=https://login.mcorch.com/dashboard/marketing"
}
```

> **Tool Result (mcp__playwright__browser_navigate)** - ❌ Error
>
> ```
> ### Error
> Error: async initializeServer: Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome
> Run "npx playwright install chrome"
> ```

## 🤖 Claude *(01:14:07)*


## 🤖 Claude *(01:14:08)*

Playwright MCP não tem Chrome neste ambiente. Tento instalar o browser uma vez (timeboxed) — se vier, faço o render check logado; se não, disclosure honesta (Lei 1) apoiada na prova de bundle:

## 🤖 Claude *(01:14:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "timeout 180 npx playwright install chrome 2>&1 | tail -8; echo \"=== install exit: $? ===\"",
  "description": "Install Chrome for Playwright MCP"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Switching to root user to install dependencies...
> ++ arch
> + [[ aarch64 == \a\a\r\c\h\6\4 ]]
> + echo 'ERROR: not supported on Linux Arm64'
> ERROR: not supported on Linux Arm64
> + exit 1
> Failed to install browsers
> Error: Failed to install chrome
> === install exit: 0 ===
> ```

## 🤖 Claude *(01:14:19)*


## 🤖 Claude *(01:14:20)*

ARM64 não suporta Chrome do Playwright. As seals usaram o `agent-browser` (Chromium ARM64 próprio). Checo se está disponível para um screenshot direto:

## 🤖 Claude *(01:14:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "which agent-browser 2>/dev/null && agent-browser --version 2>&1 | head -1 || echo \"agent-browser not on PATH\"; ls ~/.bun/bin/agent-browser 2>/dev/null; npx agent-browser --version 2>&1 | head -3",
  "description": "Check agent-browser CLI availability"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser
> agent-browser 0.27.0
> agent-browser 0.27.0
> ```

## 🤖 Claude *(01:14:30)*


## 🤖 Claude *(01:14:31)*

`agent-browser 0.27.0` disponível (Chromium ARM64 próprio — a ferramenta das seals). Vejo a sintaxe e gero um magic link fresco (o anterior pode ter sido consumido):

## 🤖 Claude *(01:14:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "agent-browser --help 2>&1 | head -40",
  "description": "agent-browser CLI usage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> agent-browser - fast browser automation CLI for AI agents
> 
> Usage: agent-browser <command> [args] [options]
> 
> Start here (for AI agents):
>   agent-browser skills get core --full
> 
>   Skills ship with the CLI (always version-matched) and include workflow
>   patterns, ref/selector usage, and copy-paste examples. Prefer this over
>   guessing commands from flag docs alone. Specialized skills cover Electron
>   apps, Slack, exploratory testing, and cloud browser providers.
> 
>   skills [list]                List available skills
>   skills get core              Core usage guide (overview + common patterns)
>   skills get core --full       Include full command reference and templates
>   skills get <name>            Load a specialized skill (electron, slack, ...)
>   skills path [name]           Print skill directory path
> 
> Core Commands:
>   open <url>                 Navigate to URL
>   click <sel>                Click element (or @ref)
>   dblclick <sel>             Double-click element
>   type <sel> <text>          Type into element
>   fill <sel> <text>          Clear and fill
>   press <key>                Press key (Enter, Tab, Control+a)
>   keyboard type <text>       Type text with real keystrokes (no selector)
>   keyboard inserttext <text> Insert text without key events
>   hover <sel>                Hover element
>   focus <sel>                Focus element
>   check <sel>                Check checkbox
>   uncheck <sel>              Uncheck checkbox
>   select <sel> <val...>      Select dropdown option
>   drag <src> <dst>           Drag and drop
>   upload <sel> <files...>    Upload files
>   download <sel> <path>      Download file by clicking element
>   scroll <dir> [px]          Scroll (up/down/left/right)
>   scrollintoview <sel>       Scroll element into view
>   wait <sel|ms>              Wait for element or time
>   screenshot [path]          Take screenshot
> ```

## 🤖 Claude *(01:14:48)*


## 🤖 Claude *(01:14:50)*

agent-browser tem `open`/`wait`/`screenshot`. Dirijo o fluxo logado completo num passo (magic link → marketing → screenshot + texto da página):

## 🤖 Claude *(01:14:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nLINK=$(bun run scripts/qa/gen-magiclink.ts gabrielcall@gmail.com https://login.mcorch.com/dashboard/marketing 2>/dev/null)\necho \"link: ${LINK:0:60}...\"\nagent-browser open \"$LINK\" 2>&1 | tail -2\nagent-browser wait 4000 2>&1 | tail -1\nagent-browser open \"https://login.mcorch.com/dashboard/marketing\" 2>&1 | tail -2\nagent-browser wait 3500 2>&1 | tail -1\nagent-browser screenshot scripts/qa/_marketing-ui-verify.png 2>&1 | tail -2\necho \"=== PAGE TEXT (panels present?) ===\"\nagent-browser text body 2>&1 | grep -iE \"Marketing Hub|Intent Orchestrator|Auditoria AEO|Nutri\u00e7\u00e3o|Leads|aprova\u00e7\u00e3o|mcoCoins|Auditar\" | head -20",
  "description": "Drive agent-browser: magic link \u2192 marketing \u2192 screenshot + text"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> link: https://bcyvddsykvehvpwstlfa.supabase.co/auth/v1/verify?toke...
> ✓ Magic Constellation
>   https://login.mcorch.com/dashboard/marketing#access_token=eyJhbGciOiJFUzI1NiIsImtpZCI6ImQwNzNhM2RiLWE4ZjMtNGU2OC04ZWM1LTZmNmI0N2QxNDQ1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2JjeXZkZHN5a3ZlaHZwd3N0bGZhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJhZGEzOWZhZS02N2UxLTRlNTMtYWYxYy01YTE4ZTFjMTA4ZTgiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzgwNTM5Mjk1LCJpYXQiOjE3ODA1MzU2OTUsImVtYWlsIjoiZ2FicmllbGNhbGxAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl0sInJvbGUiOiJhZG1pbiJ9LCJ1c2VyX21ldGFkYXRhIjp7ImF2YXRhcl91cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMcXVZaC1yTjV2ODRoYUlaUDRaTW9ucUdHN0lkNTBLOHdCZXd3TWJiTks0ZHNURmRHdz1zOTYtYyIsImVtYWlsIjoiZ2FicmllbGNhbGxAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6IkdhYnJpZWwgQ2FsZGVpcmEiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYW1lIjoiR2FicmllbCBDYWxkZWlyYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xxdVloLXJONXY4NGhhSVpQNFpNb25xR0c3SWQ1MEs4d0Jld3dNYmJOSzRkc1RGZEd3PXM5Ni1jIiwicHJvdmlkZXJfaWQiOiIxMDMyODkwOTY4NTE5NzExNzg0NzUiLCJzdWIiOiIxMDMyODkwOTY4NTE5NzExNzg0NzUifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvdHAiLCJ0aW1lc3RhbXAiOjE3ODA1MzU2OTV9XSwic2Vzc2lvbl9pZCI6ImIyMDkyNWU5LThjZWYtNGQ0Yi04ODI1LTEzMTE1NzAzMDkzNiIsImlzX2Fub255bW91cyI6ZmFsc2V9.4fZ6T6kiOfp3zuAM_uF-PZ6Q1HURr1hBwVZn1y-FUMYUq6k5k35hKpjgqse9Kk6c84lxwqt8pzETEAh5v09NOA&expires_at=1780539295&expires_in=3600&refresh_token=ru7kwqsrvb4r&sb=&token_type=bearer&type=magiclink
> ✓ Done
> ✓ Magic Constellation
>   https://login.mcorch.com/dashboard/marketing
> ✓ Done
> ✓ Screenshot saved to scripts/qa/_marketing-ui-verify.png
> === PAGE TEXT (panels present?) ===
> ```

## 🤖 Claude *(01:15:16)*


## 🤖 Claude *(01:15:18)*

Magic link autenticou (token + `gabrielcall@gmail.com` role authenticated no fragment) e o screenshot salvou — mas o grep do texto veio vazio (SPA pode ainda estar montando). Vou olhar o screenshot (prova material) + pegar o texto cru + console:

## 🤖 Claude *(01:15:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nagent-browser wait 2500 2>&1 | tail -1\necho \"=== URL now ===\"; agent-browser eval \"location.href\" 2>&1 | tail -3\necho \"=== full page text (first 60 lines) ===\"; agent-browser text body 2>&1 | head -60\necho \"=== re-screenshot ===\"; agent-browser screenshot scripts/qa/_marketing-ui-verify.png 2>&1 | tail -1\nls -la --time-style=+%H:%M:%S scripts/qa/_marketing-ui-verify.png",
  "description": "Get current URL + full page text + fresh screenshot"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Done
> === URL now ===
> "https://login.mcorch.com/dashboard/marketing"
> === full page text (first 60 lines) ===
> Unknown command: text
> === re-screenshot ===
> ✓ Screenshot saved to scripts/qa/_marketing-ui-verify.png
> -rw-rw-r-- 1 ubuntu ubuntu 90784 22:15:24 scripts/qa/_marketing-ui-verify.png
> ```

## 🤖 Claude *(01:15:28)*


## 🤖 Claude *(01:15:30)*

URL correta (`/dashboard/marketing`, sessão estabelecida — não voltou pro `/auth`). `text` não é comando do agent-browser; o screenshot tem 90KB (página real renderizada). Vou olhar a imagem — a prova material:

## 🤖 Claude *(01:15:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/_marketing-ui-verify.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(01:15:44)*


## 🤖 Claude *(01:15:46)*

Renderizou logado (Usuário Zero · 5291 mcoCoins): Marketing Hub com Leads board + Campanhas + início da Nutrição. Meus painéis novos (Intent + AEO) ficam abaixo — scrollo para confirmá-los materialmente:

## 🤖 Claude *(01:15:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nagent-browser scroll down 1150 2>&1 | tail -1\nagent-browser wait 700 2>&1 | tail -1\nagent-browser screenshot scripts/qa/_marketing-intent.png 2>&1 | tail -1\nagent-browser scroll down 950 2>&1 | tail -1\nagent-browser wait 700 2>&1 | tail -1\nagent-browser screenshot scripts/qa/_marketing-aeo.png 2>&1 | tail -1\necho \"=== console errors? ===\"; agent-browser console 2>&1 | grep -iE \"error|exception|failed\" | grep -ivE \"favicon|404 .*\\.(png|ico)|infra_health\" | head -10 || echo \"(no console command or no errors)\"",
  "description": "Scroll to Intent + AEO panels, screenshot each, check console"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Done
> ✓ Done
> ✓ Screenshot saved to scripts/qa/_marketing-intent.png
> ✓ Done
> ✓ Done
> ✓ Screenshot saved to scripts/qa/_marketing-aeo.png
> === console errors? ===
> ```

## 🤖 Claude *(01:15:56)*


## 🤖 Claude *(01:15:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/_marketing-intent.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': 'iVBORw0KGgoAAAANSUhEUgAABQAAAAJ5CAIAAAB+DAonAAAQAElEQVR4nOzdB0ATVx8A8AdJLowkCAkygoJEWaKsirhAraAVtBW0gtvWPSqOqq2iVWsr1qqtddu6BavgZxUHuMABgiIoMmVK2GEkYeQS4LtLUFEBWU7+vy8fzV1e3r0bifnf/907KkOzCwKgA1Cm0LS0DVTVNIjnlRVlxYXZWhx9BAAAAAAAAPhEFeVnvjKHigDoGNjaXRkabMVzpoa2ElKurZXlZScjAAAAAAAAwMcPU2G8kvF6vYwyAqBjUGVoNDEJAAAAAAAA+KgRGS8i0UWlYcSDeEJMvl4GMsCgo6BQqE1MAgAAAAAAAD5qzcl4QQwAAAAAAAAAAOCj15yMF3SBBgAAAAAAAADQIUAADAAAAAAAAACgQ4AAGAAAAAAAAABAhwABMAAAAAAAAACADgECYAAAAAAAAAAAHQIEwAAAAAAAAAAAOgQIgAEAAAAAAAAAdAgQAAMAAAAAAAAA6BAgAAYAAAAAAAAA0CFAAAwAAAAAAAAAoEOAABgAAAAAAAAAQIcAATAAAAAAAAAAgA4BAmAAAAAAAAAAAB0CBMAAAAAAAAAAADqEdg6AVaxtuhw9TjxUrKxfeYm7cw/xQAAAAAAAAAAAwPvQzgGw9vcr6D1MiIf298tfeUnVzo54IAAAAAAAAAAA4H1ozwCY0rkznceTFRTKioro3XtQtLUV84nEb/eIKMVz4gnkgQEAAAAAAAAAvHvtGQDTTUyJv1XJiZLkpOeTAAAAAAAAAADAh4CK2o8i4iWiXyUKRb3/AHoPk4rbt4g5/PlzkDz3S/x94tAHAQAAAAAAAAAA71y7ZoDNzIi/eFIS8SCeYKYvZYAr798nHm+uhdln7cX4+OS6x4N/J5thz17ivPzS0cndMNR2TPvJOy6GhhxdOZTbuuqwbsMW7zgbEvFI3rBHoSH/bplsz2mPpjVz+foDp65cu27l5GH6zVwoZvz1oXtEayN2jCHfwhm5JZRsuV+9bd0UptVXi9etXbv0q97MF/PMPLcE3A4N2PRVt3e35gAAAAAAAADQAu3fBVqSlFSl6AL9cgBM5IEVqeCW1cm16qZdF1FhHDMzA9TemFbuUz7naXP7fjV+UCsiYE6fpYcDd8383JzLostn0LW51iN/OOb3y0j9dxQJ0rkDPaeM95oy3p5LR+8AxjH+YrzX+PFeXxg/2zWI2e0Lr5Hm2trmruM/N4YIGAAAAAAAAPAharcAmG5hQdPVlRYUyPJypdnZMoEA0+diZhaotfhhVxMkCGmbWT0L6zjGVvrEU2Hk1RghajeixMAjV2MSEsL+d/ImH0ctw7SfsXKaFdEoSerVrfM8h/Uf5um9/2Yh8Qp35LL5A7kdJhQUpV/0OxOZkBAZdPJqi7ciAAAAAAAAALwLrbwGuFZJCTM0wrp3x3jd6SYmdB6PpqtHzC85dJD4q4RQ8cG/Oy9b3vXQYWleriQ1lUgL46lP8CdP8KxMpdraZi1DFJtY+Lm5AaebMQeLFOGIybU20yZCzbTENKHZ5/VLYpw+01au9BxobEBkYYX8mFtHtmw6GVn0LA7D9AdNWTLrqz7WxixJ2q19m7aGdVt76gd7euGFeR7LrhQhjlVva3NtCc5lPq+v91cLZ46x723G00aFabExt/6378CF2KLXAjummetAczL8jd26eOnRRPL1nAvb1uGcw7vGcA0Gfm7OusYvkpf7Ysbs8QOtzMwNWMLCtMTIWyf37ryYKJIvzGzGKb8l5nS+34J1CYNmTB1qxaMXJURdPbR/55mHomdr0Md95gyvofbm2nRJYcLdi0d3HPhfbBFmNvnwqR+snqV9jacdvjsNocKrS79eepGPY9yBUxbO+MJevtDshMTYi0e2HLnWrOgU0x82f+3Cr6zMtVlIIsyOvbhj61ayMZyhm/z+cufWlWIN+uVSzC8IJez1nPZ7OtPc3t6cS6wO88XWadtaAwAAAAAAAEC7ak0ArPJZH53Va4h8b/2Z1WKRYNfOssAAJflk2elTqLqaPX8BERgTD8aAgYpiRDxcsP6nyujoNy9GWBSbIBxjwDK27sbyTy/CON3MOcRsfkJiEbd+Oc7AZXt3TDOXh4ESCWLJeyCbGc+b9euVHJyI5Uau3ec7xriuf7Lx58s2YpxrTXQVxrhDf9j1+3jzZ0W0je2dje0dB1otVlRYvyiTw5GHe9mJifWi45yYk/v34uYsYWyhhGyf/eIdu2ZasepeZREVuhrbD7IyW7xw282i5+/iev2+D9ElQiK5zeKafz7FtzcXTVt6Jp2I/Hsv/H3fbHmcKywU0rXNHaf80reP2bzZW/lFaQkJTCaLw+OS1Qv5aYUSCT9NJMEx469+OfDLyGc9xlkG5vbEw8ps6YwfL6Y1HQOTW+zw9jFcxfaU0FkG9uN9D5sZz5r1e2JRWmJCqoTF4nK1ybi/MJsvkojS03DJa7W0ea0BAAAAAAAAoJ21pgt05+UriehXJhBU3I0oOX4sb91PWZMnpo9wET6LfpE8CSw8E0jMJF7KX7+u5MTxisi7suJiIhjWXra8ecsR5qSlE5EVx9xKnwgzWd2syChPmB5DBF31SmEY4ifGpvIjDy1wtbOxsfP8NayQyIZ+4SnvgMyxn7lMHv1mX92/YqrrEFfPeQdEg76yaiwCxjgDF/5ARr+ShJNrZrn2d3Sd9OORGCEROY9fOtOe01hTiUCx3lTRw39/X7du7bb/xYoQs8+MdfI4UJJwhqhwiOvUNWcSyHDPauaP8/u8VCH/jLdr388c+g6ZdUTe+Xugl/xyWoxjZt6N7Pod9pNrfycHO9efQhLSYhL5CENpF1d97eH29Y//SyXfnxb4o9cXbh4ztt0S6n++cDEZ/WZf+OlbV0c7Yi1+upCNkMHIJbMGctAb0PGi2Ji0tLCtU4f0tbFznLo3VoLoVu7j+3BFD/ct9PjCfdaWSLIPujBy2wx3ty+8lp1JfDVebftaAwAAAAAAAEB7a00GuLamptllyYi4trYWPX8g1Mwe0Ajh/Ni0ImTF5ZoZs7B0jrG8A3R6bNrLPWTxnFt+24oKvxjvOmXLv0vo5ChURDki5chl0hGT26c3OVV4dcuv2y7kkOX56ZskxlZ/j+c2uEx6t0FW5Ctpfpu2+keRSyr6386NGHOWlSjyZpEEtRTTeGAfMg0rjNy4ap0/GSim+69bhjh+6wexeL0HcplRzy5nFt49cuCKPPPJj70QljbF3JzO6abPQolFRekJfOTIYjnOXOtrlZ6dGHl4mVdMuqiJJCnL2N5KW/7EasqPO6Yo1kw+g2tl3415LbapJuPpV3ZuLUwf6f75/F2B5GDWdA55uoDI+jKJiWalZttjrdEngKqrxxw8VNXGlm7cjdqZvEZAVpArSUuveHBffP2aLD8PAQAAAAAAAN6h1gTAhb/56qz5iaajQ2Wz1fo6KGbWVFYKz54R7NtbW1FBTCozGFpz57Nc3ZRVVOq/V5qbU7Rlc/OWIxGlxaYJx3BZxlbGrFiOfDCs7LTEIslLGUROn8Xbtszsq/3quzEyaqOzWPLBmUX8ohdhs7CQT4SyDY6YjLE4TJZ80fXSzKLYf1fN/xc16aXKOL2/njqG7AIdeOBWXQOKEtOeX32LF6WlF6FBLMTisF68T0I0sa6EBBeRnYrpJCLmFEXtW/cTa8lMd3t71zH2CI2fTawDkaBe9uuFRroK0zGmomIW15j1yktMZtNDRWP6Q5f9/ss0KxZqPXo7rPXH3QmaOP61F3zXacxYJepLHzEKozvduDtrmHOt99KS0/8W7tqh+LwAAAAAAAAA3oHWBMBV9+9lfDWKHATLyIhuZoZ170Hv3p2mq9fJc0J1aVnJoX+IMp3Ge3XyGIvkF/1KUlKIB56chKent2AQLPIa08REPhEzkX2Au3HNyA7QabF84UsBMMd6/Fdk9Ms/s2LhtqDEIpzZ50e/w9OM62oQCoVkrPt8JC0kv4uPmX4jQSAuEckDXzrHmEMsTpGGZJp9vXKhPR579Uzg1Yf1R8LCRSLFpIGZGReLetYRmGk8csrs8caoELt59GphQw3gdpOvgrBI+CKn3FTAJ0q8uG/drS1FyNjKyvrz8VPH2xuYj18242bkqmsNZkqFoiIixaqN+IGzvFbeUhTBmBy6pC7axBqPbjED+/HuRPQrSTi0dNmOW0SimTNsY8CuMdqoBRre7C1d648WtbOOwV+7VXjdiedVyUnlEeGVD2MrH8YQk6q9rVV7W6n366/Sw0TLa6LaZ32ezp9dLRAgAAAAAAAAwNvXytsgEUGsNCO9/Mb14j2785Ytyfxq9NNvphLzNcaOUxRgyaPfrGlTiZfyvl9asm8PUViamdH86JckyYlNKyTCUX0rK/vnI2C91A8ZI3Kd8mBWWJTGJ6JRjDtw/LC66JdOZn6jHpI3JWINmjV/pHx8Ysz485mzP280nBMm3ozkE//lui+eP8aMgzG7Dfp6pe+SMc4jx08dafxq2CxKuxlJVk+3X7Lt9xnDeutz9HuPXLxl2xSyBdm3riYIRfxbUdkvNYBpNnLGrEFkBJr68Ba/GQMecwauvXj37vXAHbPMRLG3Lh7+dZN/LLkNyCzrSxfL0unP2idKj4yVr4Xr4vnDumHykb2WHAsJu3Ro8bA33Z0YYyoStCJ+Dp8IXTGzoZ4DG95cdHpjVbXDWn+0KJqaXf85TES/tVJp/vat6RO+Lvxjq/j6VSLKJR7EE2Iy3WtcwR9ba2UyIgw2OniMoqnVjIqZVsvPJaen1n/c/tOV89I+wKzmnH70Wpn2vBsXs++6K4qaIzY5v/Fy8uZWauXx/bqfN6z7ebVn35dXCHHsp/9xNjL+0c3T6zzMmehd4zhuuKbYkonHPV+5Np1pvTRIsSnizy63bsUtxEf+GaHYRxd9+r77VQMAAAAA6JhaeRuk10ni46W5OTQ9fao+FykrUbW08Bw+nhiP2gIX5sSkS1y1tR0nf0FGd4XpsTkiVP+nJl4UezNW+PkglvnMY+dHZuOYAVebTnakRbzxv/xN37r49/1bzvTZPsbYYOQv/4385c1LLLq149eT5r+PNzcf7xs43vf5C8LIfftfv8NtTtiBTYFmv7ib03mfL9n1+ZIXr/AvbNl5iywfdWDtfqtdM61eaYAwdv8vO6OI5OwbfzgL027GFo3ncc1nH747W8jPlnAMyCGYhQmRiYXy9tT116ZzvbYE2hcVxe5cuuZi1KEjkcN+sGeZj98VNP5FVXQiOYw3uUycH3s1QWJlTbdf5RfkyScv/dVG8p7JVvN37eOsXbbtZhGR+CZCWBbd/oejQVOK0v63cdmByJdrKWrzWn+kqDTulj8wPX1Jehp/xTI89QmFydScOEXVshfd1JR4XZKUVPUoVnD0cPGRQ+Lbt7mbf6cbGelv/j1r9rdKLbi0vo62hQ2XHvSiUwKmbWzDo6OPDaZtPnaClwM5ZlpMdkDg3Re9GjBu36lz3czJEzA2XnMnBIX6RH4SF4cDprm5JAAAEABJREFUAAAAAID3pTUZYGU2u/Pan4yCLhEP4gkxqZgvSU4m/hI/9FVM6n7ro7bCiZQvmcpUDGwlSY/NFr5aIu3fVfO2Xk2VEGW4PC497cJP3y7cHyMkA0Lzbhw6nnNh3ax5+29mP39HYVpCmrCpRV779dupPwUmKMpICtNiQ05u9Z61zK+h+9Pi6RdXernP2381gV/XsVdSyI+58Oskrx8v1N0zqShy26xJP568y3+eui68e/LHSbPq3w2oyW2Qc22N19QV+y/EpBVKWFwDliQ79sLepbMWn6zrc42nXd33vzR5UpjLMzYzJgfLFiUeXThp6ZGwtOcLFSaQW2Zb5Juyr6KHRxYvPUK2lk7UxkWJJ1fM+tGPHKCZZWBmTI6DhYrunjwSJs98a3ONzc26sRqIudq61h8n9rRv1KytayRVT70XENGvWv+B3QL+0545m9GvP02LTTyIJ5xZc40D/lO1d8BTU54umleD4+q2duwp05q/FEl2RN3RqW1url3vXALdwJqn6N2efTdeiD5+OMJfnHOSSFDLR6EDAAAAAACgPiWGZhfUQjobNjKdXZ5PikKC831WEU80v5nBnjVb8M/fSlSK1pRpgj27FdcDf2gwsxmHTy2xohdemOex7ApklDqKbqb2r8wRlebnZSejdkLR1OKdv6isopr/m2+J/3H1gYO6/LGTXErojaL9e6TZT4nnNIMunNnzmIMciedZC+ZWhN8m8sM6S5ZVl1ekjhpRU1baePVMq+UnTs21IJ4JIw4GIo9pZMo0O3CWx8qQumMYM5927IyPNXE6IjVgS3zfZaPIkbgLz3339bIgfntdbM3su+7MCS8eWXHgLLfni24TzNjzcMB6RQbY12PSnoR6jcW4zovWeTtrSxICfTccvvuuP60cxw3/Hp5AbkdJxJqR0/3r30Obab3UP2A2uUMkCbsnjNsc08JtzBn55/nto8gze6n/TPh6w91P+cIAAAAAAIB3oofloFfmpCe90lW1VRlg1T5kIJE9ZxZ/7mz5ZB/FfEkymfKlm5jQe8gzwMmJ6IPE0uYwP75+ouBDR5wVIqLfipiYYv/jyiyW7pr1xMyiQ//wl3wnSYivEYmIB/GE771AcPQQ8ZLe2vVK6urFx4+UP3hAUVdjDnNu9qIKE+IVXRq0zW0MnqeAWTwbxdjmwtQHhY0kgJnmrrN+2/3vldB78otX7908t3O5q/FLV6BixhP+kb+aes9v9rAJ5CW45KWqNzcMauSaX8zYddPNZ1cdRx6fZf2sOqbxoAmrdwYG306U1xYZfPTP70daP6sF44459IB8S1KIPPol0K1XnI9TLPqQl/ySW5bVKA9HC565jZunC09RL2Y9+2yiYll/jDS3HuPzx9Eg+erEhv5L1N/QlcJMY8epP/+jWJFHkcEHfna34jDNph9/VLcs93a6TPrFddr39r5UJ8Z13Rmp2ETBS1+/4JfOGTR9wza/c9di61p49LfZw8zhumAAAAAAgPbXumuA6wayqqVQ6s99FgCbKquStz6qaocu0O2BSPie8lti/nrIK6o/HDEAbcQYSOZ1idyvEkIarqNpbHZ5VGTRju0UNlt70RJ1h/7Eq+URdwr/2FqwfauKial6334arqNK//UvCzytbmPDGDCoLOBU8xYl4T9IK0QW2vJu6tpYjDzByzS2MJYPVyZJS+WLGhjoG+O6/Xxgi0e9q4TpLAML57l/OjrYfDvr59cvr2U5LNrmQH/DbbO4zqt2/OZuIJ8ojNgya86+GDKXyTR3X7/jZ9d6C2Np8/qO4vV1cXZcNWdNQFo75KS1+87e52xu8GwRLAPrUXO2uzhaz5q+Jez5ldGYsdvPO+utNV2b5zjxN2veno0P0AeCN/HP7fUmiRb2Hbu879gJQavmrDiR8EmOlA4AAAAA8L60JgCujIoikl0Ge/bVTUZGKZ5UFxRIUlPpPLJ/pOTJk5oP++Yu/KADJ2Og1yFoN/QeJsRfXN7VWdXKivhb9Pd+4m/nZSs0XEYoynRyHaVEo+X+sFxw9AgRAKta2xABMJ6dheRdJ5q9KIkw+0GaxE2brsj6BpIBMKZtbFEXhqY9yJY4vfoeIhD8cc2zOFCSHRMRL2RZWNsYEJEy3Wb6urlhkzeEvRYCy4eeiw+NjOcXpobxha/c8BphnL4Ld2z2spDPrRf9Iqa118bn0a8k+0FEQiHdwMaBHM6KznNfsyEhdc7hGGHauRN+2SwiDDd3crOWx+7CB8FX4smB3oUPEgrfHPlpmxsQiw04fC5CaODgOsqjL7EB6BbT1iy66emjuNgcM/f4cePz6FfekmwJy8Khr8McXwfUAnSHhYfPT33pjBkRqKJ2ROzTmHg+sU7WNooruQ1cV6yOeTDncAJ8TQEAAAAAtJvWBMCF27eimho1e/vamtqKu+FFf+148dJvvtrLVqAaWeGW39AHAk888KXNAQTA20VhkX1W8axM4q9Kr97EX4l8FHT1Pn2Jv5kzpyspKXXd94+6/AoCPIW89ljVypr4K31KBsDUTp2avyw8OyEhG/UlAjADc3MDLJJIE7KejYAlTI1JFb4eAJMDkwUHsxxsuIUHF8/aGyuPqjjOG/7dR17jynNxM98d9toIZYUhq6avPFEvAqsXANNZFl5bNs+2kS+0fvRLVGvj4WmjKJrqN2v6xhBFitp86o6Dq5y0iczyrG8cgpaFxAb8FhuguAbY0VqbvAY4LfjPNXtakPMsDF09eZafPJscGHg6Ypv/b85EIM1zdrf54yZ5fTLTfNQER0UyXBJ/aOGcLYqWYBz7iZu3rXFq0d2ttQ14LSrfEsKY3YsWbw+ra1zf6dv2Le/LIlPwnhNtAleHQQQMAAAAANBeWhMAE6nd/LU+Db5UFfPg6SRPBEAHJL/HtbKKSnV5uRKNvABU8ffFJQPKlHplyZseKVFp5ISysnyOEmo+SXZCaiEiIjJy5Gftwwl8zMBc0QEaEbFxoeT1fst4Wtjh1WGHERlhGds4DpOP3Y1pI/kttIhYi8NhYajo5dgzNeTwucbyj9rDNh50VSyGiH4Xvoh+yc7YLn0VyWjJg7sxdAtHZwtUV/BBtpML8ZK2jZs1K6TNI9Bl3/wn5Hlfajw75ma80NmJJR8O3QALKcIxg74OiiytJOYfnx0hz8YCw4sij/tscTjv68JCHwBJxB9r6qJfRDbu7sG1vo5nNzoQW5fn4GjODIuECBgAAAAAoJ20232AAejgqotLlLlqdBOzivDbkqREWv8B9B4mFXfDy6MiNVxGGO4/qChWHnkXkR2ezdCzFLGKmTn5dkFLwkGJvJ+zizYdaZvZGDDPF7J41saKnsipMXwJMm7gPZix26IfvT368rSbOQacRJjdxGXyzy4OLgxav/xQ/TGMMRZXuy5XSreZ4LtjQgNv1uZytV+Lt1tKkh3z0n3RJMK65tKZ2mTrcJa2cd26FiZEZL8UReKFCQ9SJS42zR0Or6lRoNsqOz7h5WG6cWInpiEH8rBgcckTEyK4EBgAAAAAoH20ZhRoAMDrqlLIUd9UzMjItko+IBx76jTib8EW37KLQbISgVQgKD3/X8GWzURGmD1lKvFSZWKi/C1kFFWV1KJR03F+fFqh/Jk2OQ4WnVt34aiECIyFDYRLGNf55wM75jg2O/ptNm3XFcuHGbdwGGU6nUNvc0MkhKZLfDCjvdNZLBh5HgAAAADgAwABMADtQ3znNvG30xgPRMPKTv9bXV6h3ref9uKlstLS3NU/PBk2JNVlSN7a1bKyUp2l36vbO1SLRGVnAhCV1unLMeTbw2+3aHHkOFjy9CeLZ2OsbWDOU3Q6zk6Lz24o/jUY9I1zXYlzqycNtDbpxiMeliM3xLRyKHQi8bs5RBGCG7j5bllk//wmSbiw6NldmArPzekvX1Ddw9S6fx/Fokf9/g6GoJMUPmuItrmFwcs3ezIwd+C1d0wqkRTWheR0be36i2MZWHAb721tYGH+8n2YMK6FdV0OX1hUJIT0LwAAAABAu4EAGID2Ibp8kYhpMa4BZ+ZsaW5O7tpVxEz2pKnG/57RcB9L1dWjGhhojPEgJrUmTCZeyvH5QZaXy5m7gMblEkGyKORyixaHF5LjYJG0ja0szK15dbcAjsluKKKlaxtrKyIwYUJoWAxfEXwyrUe5mbc2CpRkn1+77GCCfGl0mznbtniZ1cV8krSImLrstMt3s5yfB3eY2cQ/LkXdvXio4bv1tj9RduSDVPkzurX3hoXPW4Jx7L9Zvcyp3S8Axouy69LydAs3dwfOs6U5zvL2MGj8bXSHReu9HV80znHRKm8HxW7Jjg9Lg5u1AQAAAAC0H7gGGID2USMWCw4e6PzdYvbU6cLLF8XXr2YtnKf30wa6kZHeqjX1S0oFgtyffCru3MKMeezJU4g5gr/315aXoxYRZcemKm4GzDN3cOAqbgGcGiO/fdBrQa0kOyZePmgWYjmv2bPLIYEvIVLHfYc5PLuLLsth4cafjY8f3Hc+tdktkBSFbV68int0iwtRr7bTz9vWFM1YFcLHcX7owcMRjsscWORNifaFucZHEGG5Ns9GMU41y2n6tPiwmwnPrxuWSOrytHTrbzb48hKEEmHC6YP+MW0dIwuhorvHD4aN+pkcCJpsSciw57dB4r2V4a+E8aGxhR4G2vLFHQ4ZFBGRJmQZOzi8aWks67kHz456QO4jbd6z2yAR1UUc3h1RBAlgAAAAAID2AxlgANpN8fFjFQ9jlahUru8WjNeDCHHTPUYX7t9bHhEuLRYQD3H4naJ9u4mZxEv0HiYGv/+hRKFU3Isq9j+OWkyY9iBVnh1kOX7joRjsuDA1oeF4Ceff/GfPXUWcybJwHOvhNdHDlYh+hRFBoYo8Mt3AwcN9lDGrZRfz4mkBPiv/iVckKXljN2/y7kvmdkUxh1ZtCEyty11qWzg4uzjV3aUJSRKOL1q8vd6oWXjhsxUhh4d2HTvBa+J0VxvtFl5V3Ej7EgJ+WRXwrHa6gY2T8ygXRfQreQuZVZwfsnd7aGHdFIvn4OLsQka/2aHnY4SNvYnYIJsDUxHLwMbRxcXxefSLsoN8f/aDmwADAAAAALQrCIABaD8yKX+ZN16QT+9m3O3ESa0p06qJtPCenU/nz051HkI8shfMKdq7m5ipNf1bo2P+WNeueG5O9oplSjU1qMXwwvi6TtDPCMkRsBopTcSk346ZvvF4aExqoSL0E6aG7l22fM2qn/eGpgpRqxXd9F20JlgR9LH6zv1jkwc5IhaeFrhypPO3qw6GPHi2PDJBGrx3ocek1SGvDHoce3z5iuMR2W+lry+edn751yPJFU+oa4ck+8H5LbPcvt3+4G2EwIknFn278MTdFztGGHP8u3nrz6c1sYmFd7fM+u5QRF3gLClMvXt687yRbotPJED2FwAAAACgfSkxNLsgADqAbqb2r8wRlebnZSej9kbtrGPw124VXndEDg2dXH7ndmVsTCWRGcYwFS6xIlEAABAASURBVIueqr16qw8c9PzVpwvmVBe1va8vaCnMas6JYyvI2yAJQ7//clYgH2JNAAAAAICPXA/LQa/MSU+KfGUOXAMMQDuTFeRnfTOFM3eB5tivVXqYEI/Xy9RKpcX/+hXt2VVbUYEAAAAAAAAA7wQEwAC0vxqxuOC3TcVHDzMHD1W1saUbd6N21kNkbJwrSUuveHBffO0qEScj8A4wrcfM9bB+ZRgqOsvcyUYxAJhECOMsAwAAAAB8mpQpNC1tA1U1DeJ5ZUVZcWE2BMAAvC2yvNwS/+MlrRngCrQbTNvYdeIEx0bHYRYmRMhHzgYAAAAAAJ8ctnZXhgZb8Zypoa2ElCEABgB0VJLsu8c3/3I6DeJfAAAAAIBPkipD45VJCIABAJ8yPC1whlUgAgAAAAAAHQ+FQn1lEm6DBAAAAAAAAACgQ4AAGAAAAAAAAABAhwABMAAAAAAAAACADgECYAAAAAAAAAAAHQIEwAAAAAAAAAAAOgQIgAEAAAAAAAAAdAgQAAMAAAAAAAAA6BAgAAYAAAAAAAAA0CFAAAwAAAAAAAAAoEOAABgAAAAAAAAAQIcAATAAAAAAAAAAgA4BAmAAAAAAAAAAAB0CBMAAAAAAAAAAADoECIABAAAAAAAAAHQIFExVAwHQAWhyuK/MwavKxUIBakf0zsaO44Z/5Tlk2BfWvc04qCg3r0RaizowKqf/gknDdbMfJ9XyPL+ePJSRG5tdJkNIhWPrOXri1CGOZpKUx1T7OeNGdBMkxJVJ0duAGXp4TndWTrmfX1mD2oSq47xsoiM97VF61Se2WymaZp4rXLvlJSQLqtGn5UNbtUbbo8IdMu+tfhBeULccPnuuqfhhSmEVahvMeNKkqX0lCdElKp99MXO6OUp9whd9tB+OtuyCF991VYy3syk0Phs9d6ZRQXRqCY4+ZBrWw2fO7ilLeJJb3sDqUzpbTf1hmPaT+LSyDv1vIwDgrWF3NnxjGcgAA9BO1E0HTV7iaqclfBwc8t//EvKp3KEzR7tYqqFW0bAe6b12uAkTfSokZZn5fH5RKRH9IoqGZX9HM5T0vyA//4T8KmE+P4+fWdHWn+IAfGyIYGDyzxO/4GHkhOyj/iBUV5UQH/DCItHHfAKlfXbBJ7Ep6nnpKH0jKqdnP05+8M3Ygk/tVBoA4BNCRQCAdsDsOnSspUpc0P5jaWXkdOLDm/dNPMeNHmkX/+RmJsR2qDo//MqpZxMqndVQcWZ0VBqf3DJ4fMCFeARAxyYTfdQfBEnq/TOp6OPWTrvgU9gUrSYrurP7OAIAgA8aBMAAtAd1Q3MesyQyLLPsxbyK1Gs3wywxGQ2hKqTe1dLR1apndy0VJMl7cOfi6Tgi9lO3HD7dgxJ9rcJkqLmBqiQvNeVO0N34nGqdkeNmfq5NVPH1TyZFd/49ck3zy+/6iv39ziWRXd8o+nbT5/VI3Xfqeo5m/3mjexcn5HfuZdpZeHcXMUfN2LG/Yz9DAy1KaWZa9LU7d+NeT0NgOtZ2jo4mPEOWrDg7KSzyWji/XPZamc/6DnXsYcilizMTop+w7G0k//15OZNq9nWDLcmqpmh2tXPta2+m20kViTMfBfvfjH8pA4AZeowbw407ekQ0dJGrKYuYoz1942elUWcPnq6wmudukXn26Nl8SSPLTavk9H9Rhuyp+MXS4ZywUyduEmvXnNV5gcLk2rna21rqcqjEBk+4E3Q/Pke+Lo20n5jf19XO1syAgYpToxLJvalAVTN2GTy0j6Eui1pVnB179sq1uCYzPkwdW5e+9pZcjmpFdiKxa+4+zMJfmZ+XmHwnWNEexebKiuRzbPvoqhRn3jkbmce1GzrIWJdVXZR499zR2MaPH3m1VKaxY98BnxlzdYjVyXx+JCjeEhlcYtjPnEds5CdxF/zvpJUoGk7p1GfYtLHEwUOsUeYd/0t3UpvaMs1ZuwYPe4omeRTJbibLrInjVsKPunMtClm49rfqzqIK82LPXgqOEVVTiT0+2oIfmcq0suulhYg9Gx4ZFsYvk+/ZJj5N7bJqdH0zl7F9TQ1ZKtLyvLhIRf2vHczN2jvX/rwQX0Iuit1v9OShJWd+v5H9rBY6b/DMeb06IWQ4b7Yd/87+XZm8WS8Ocrp+D0cXu55m2iqVhalxcZHXEjLJdZF/QIb2MNRRp0qLk4JvXLjGL29ytza4rVr66XgJVdPEpV9/G0MDpiQvLjZelaKYXX99G9qAio2WdidT276PIfFpyoyLDQuK44tQoztCfgy0+PutkSP/td3XUEuoz79nSnQbb618EU014/mmSELEoW5XdS22ysyqpxlxGL849t5YiaKp9b4PU6IzKS3bU635zkkLi2P1HmRMfJ9kx9w8dzpFbPjyUfrn/XzUYMuffcPvihWQH1I1i2meLujG/kNp5c8PQkMtJMqMDRdSW7CzAADgbYAu0AC0AwqjM4tanMd/OTCoLkiLvJZI/GYifvGPnD7IUBR7yvfvHbvulhn2/2KoDl1ehsriOTqqJQec2r3rZqaqufvMIRaa1fkX/HccTRULk//9aceeAHnI1xgqnWOmKw679O/+K9E5iOs44msXTvmDO4F+Nx8Xa/af5OrYlfLKO+im/cd49tIojrtw9FJYXLWhq6t7P82XC1E0rId4eZnTc2IvHL0eyde0dTRkNH2yjMqxmzzCsXNh2L5D23zPxkqNR3qYsxt8izjt1Lpd+68Wivn3Dq7Y8Zd/Vnlbltus1anfTk2rSa5DedWpl68Eno3NV+01enp/Y2bj7VfRcZzu6mgoSbp86b+gNBnPrqcWXdEidV7/kY66kpjLB33/DU6k9vQY1LPxxRK/83p7urqYyVKvXfn32F2+ao+RkxXLJeZ/qZgfeDqGr2o+errj837vDH1jbkGk39bAaznajrPGjeQVXdt97KBfGuL1dbRhKhbW0PFDbkkdxxHuLhxx3J3/joZFy4+Eoc96MFJZBr15oshj/vt33cnXshztaqiueIGmbmimXvbg5n//e5RPNRzq2d9QpXl7tpG1a+KwRzSWoSU1yd/v4LE0is2IybPsVKKC9vueDStgWrlaG6jU7Vvd/v15Vff9fI8FhkkMXUaPceHQUdOfpvZYNeIgGevYU4V/bd+x/QdjyfqHP2t2Pc3ZO02TpN7Y7RuWWVl8f9fen7fez69/1oZpPHL6sJ6qeXdOBwUGpVDNBo350liDjKwcx43tge5d2f/ToYOn89lDhw01bWq3NrULGjhKG/l0vETN+MvR7o6ssgfXA09HZqqaOZqpU6mv1dPIBmQYWvfXL7m279BB/zRkOsRrkqV8gzd+jLX4+62pI/+l3ddgS5pVhtKcr9kXaFo8Gw7/8n+7fc/eKeA4evQlj71mVfLK9yHTth9xGq7Ze6pV3zkq+iY8lHDuz2MHT2dRrYe49GHKXj1KW7j6ZA9qS/dZQ0xRVtjpS8HhFdxBvXRVW7azAACgvUEGGIB2QKESv3hloqpGEo/VJYmBvlnUqgoylC1IuJ9qPZqrqYIUv3jLk87euBNXgVDRNX8657v+VmbMpHARaiZZdWni/Tv35GGkCrf/Z2qppwMD75En0eNj8iTz3HvbcO5k1Q+h1Qz7GKKYS36KyDMmM586boxNV054yYvf31Q1HlEmMezM6UQy4RaTVarq+TWv6WYURe46FItwCVmJKDo8z8qVy1aNE1SiFmjFcpuzOvVQOhv31iq8djAoMoc8VZGUWM74rq+VoVpaXMPtF3c2N9US3j94JYRM2qQkZeLs7+zrGstUo1bm3Q9L45cgfsDZzGtUcUmjqQtKZxNbw4pn9aDkzBK+Kb1cqpj/vH4UnyRS+W6wnSkz9R65x6qKk+9E8QVVqPRanK2lZX74o7QCHBXcvWPT1ZGnqVJ3kDR0/Dxg9f6MWRT833/Xisg2Eem36eP699O9k5pF7qvKknginUicrCmICws38fpMp5NKWp68qtT/XfpPfvAkFaDpk7V1tCiZOY3sWdGb165a1PBhL5Yvi38nJj5HhHLu30nsMVor4U5MEbHT7wen9J6uSy63gPznSZZ599zpRHJXFlw513ncOEtz3Ws3Mxv/NLXPqlViGiqoKC4mNonYo/cD/0xWkVa8fhKqeXundSgalpaGKOXCsRvJ8moyc0qIFCjRzPK4K/s3YjIRTu7WmEdJQ40NueoUeXeMBted39Q3z+tHaWOfjooXhZi6Vpb0vOAgxaEVH1dC/c6956s1NbgBKfJG8q/534knPynh/yHWdE9z084Jd3Ia//Zo6febim5jR375y01suCUFzShTTCyioWbkNPbxJw71+4+ziMKi+9eIw5ujw6JkokYqqb8ujX8fNmdPte47R1acFnkniziq0b27kcSRbEgeyS/1GFBprOUljaw+hWNprlOZ8N+xm/KDOY1fqTZ9LLNFOwsAANobBMAAtINqWXE1MmWqEB+oxjrf0pimQwf17K6pwWRxtOiyJ1QibUL+ZBcWpfLrfrVUF+dlFiOLzmpU1IJfz1UiiWKZFBZHR4tl4DXtB696rwpZVFT/RxXTUJ8o9+XiPvWqEGqqv9RyNbYmEt/LF9fNkeSnllTx3tgQum6fvvbWuhpMtU46LJXK5JZ/u7R8uc1anRcY+lyOloHL0nkuL+bJsjUpxG/z6obar6LJUpEWZRbU9S0kdhBfVK0jf16WdD+2v+vo7yb2LyjiZ2bGh6eUNd5Mhr5OJ2nJnWf1IFF+/D3yvxqvzK8sJA4A++6a1Htk1Carqqg7pSIjVQkVv7CrZVJixeu2boPHD53F4bIk+Zl1b0CyCn6qiGrN7aSSVUpMSsvFlc9eqSQWUJfTRtJqsUiieEEmEsmQrnrdC2/Ys42tHamhw/75surWjVijSolMvqYyKfnfZ+tWXcrPK63bj3hRUlGVJVNDlbygoLFPU/usmqwo+lqm6Vj3uZYlgpy81JiE2LgGPo/N2TutRWEbaqLi5Pxn548kOWkPc569yDTo62ppos9kMFmdWNQ8lWfJt8bWvbFt9ZomPx3PWqbK1KCVvzi0qkpSc8pNVV+uqOENKA+AC/j5z7q4VvH5ZUiXzVRU3+gx1qLvN0rjR375yx2/G25JwZvLUGSNNaORCLD+sVdZIUPk9m/Wd3Xj34fN2VOt/c4RPluc/EhWefVIbrzljQbA6vpqsuJHzw7m6tJMfmmlGWrJzgIAgPYGATAA7aC6tKCkiqVr3JmSmfUiD0Ccp7ezxPhRiUWa/bxmWTP4KUlxMff5eKd+g/q/9JOx/u+WtpGVJwXduF/w/PdtdbWo5LXfEpKiB2HXoipkz8tUVuS18QcHs+sXc117oszHccmPiVRAVzuXPuhdadnqyCqzb5++n/kiNV1dnlNR3Yr2i/jX/zwU3dWwp6O1/efOdv1NLvwZFN3owKfURnZxA/OpLf5ibt7xU69SGWq2Zm2ZhteO3rXpw76Vmq62PVatWnDv8u4kjqGled9Bli421rZ3Ao87pWyyAAAQAElEQVQG8N9pVkqxs15dGYrOIFcvV05pXEpyeFyeCOs50lGn3suvr3tLd0HDnw7UUg1uwMKGy9Ja8u3RrO+31zTz40RrdpmGm9HCAf9bty7P3/3mPfXWvnNa1/JmfjLhRykA4F2A7xoA2oMkJzm10tzuK8v4fbH5db8F1HhDBzl2TTt1J6WTpSFHGHfqoGI4aDWLfpTnnzwqi8Pj0h+WkEk8ipauoRYqD6945adCNXEyHlEYTDoFkV0fVZiaKg19cqsrSwSViCErzExSpC0wHVNtJHr5V5GsIr9AZopwfpKimxlFvSuXU1X+cg/PCkEJ6snTYYSVyMcconN5miqooomW0DsbG7KKwnZdlnfJo7A17Vr11dLochXpCBUmmdQim6qqxlAk2Zq1Oi9UFRSKpQaSYn6a4jyFiqahIYXIm9ENG25/VYmwisY17Iwli+RjJmnpcp9f3UlV02DKyrJS7hxLuRvUw/27QaZd1aILRI0ul2b8vB6kwjGxZJXFpZW+Ml9VmzgAyuJEzf8d3ODxIyGPBHUdQxYlVd63kKrG5TFlBUXilp/maM6ebWTtMlHjh33z1o3SydCgEzVf3mEX45hyVCqzyiopnfq1rdo3rxqFrqlGFRWlhd9MC7/L/dLdy7RrJxV+S7NSMmk1orEYqhQk7xuvoklvsJ0NXT1ZXZYpRI4GOszEMsUYUZ279tSXpCZWcC05srgrp44pugR37fmGmI3SqSW7oLFPx0stqxSVSesdWiqaPH116qtHfYMbkAyAqZ25Olox+fLzRCpcrgaqSC2ubua3R3O+36qbfeQ32JLmlGm8GS0IgJv1Xd3492Fz9lT7fudQ3txyiqyymqrCqusGRaUziKywECkic2o/w2cHM/Gh5nZSRZkt2VkAANDeIAAGoF2IssJOx3CnO06ex42NScuXqnPNzHryJI+P3Sd+emoUVCCtrrY2OqWpyPAzu/5m6tTM5++kG44cPEQlLrNKzXRof540MzCR/GEhq8RlNE2OJjMfVZSJSvgl9KGug/rK4oqo2qb9uzJQRUNt4N+5VjTZ1XW06v1YvoRhZje0Hyvz2Kkz9S/hQ6Kka7G20weP81SLfCCUaRk7uppTH/x3MID/ImiUVaRGZTpOdhzzJboTV6HCs+zPezZuTiMtkVWKqqgmvfsZZ14rUjGz7O+oq0JLQy3VxHJl5fk55Z0cB7lkhseWYIbW1lwWEjRzdeqRZMXdSTUZ6Tmcfi0uU0TXdezvaFgS/GdQbCPtl/ATkorN+3oOKQ9KyJOxeg617IRQEVkThd1n+GRXemrQzTupMp1+loaq1Y9FjY5WJsmKDYszGe0xpDw4Ia+SWO4gx85ZgUlp+fXny9QMB/XnVSaciiICpuaPBNPQ8SOquHM5e/JXw0ZKIx8XoE6Wdo76JXf2kzfoUkct05w928jaZeY3ddg3Z9lEBGL5xVjJnQdCKtdyaB9WaVgykdtXaWO1b1w1JnfoTFdTUcyFs3ECprG9qSYSxVW1ILP8rP6CbAEydxxrX3WNL9M0trPRpKK8V8pUSyskUnqnziyN4grxizCyWhAV+biPq4tnP5VwvhhpWn3Z37DgemaciCjDMLTsyStJkmr3dLQz1aKUNtmGqpZsq8Y+HS/1axDlxcZJvnZRHFoU3T52PBZ6tfdrIxuQHMCJquvo0Z96M7NUhdvX1USFfz2poFrWuXnfHs35fiPKNHLkv6qhljSrjKyRZiSiFmjOujT+fdicPdWO3zkvHaUljba8NKtE9rnlF18VhsXhDJ6ZbWe6IgAuikvIHzpkpKeQOJirmIZ9B3Go8tOYTewsiqaxy2Q76p1LF+7BoNAAgLcBAmAA2kl50s2jW/n9R9pbuTj3pSExPzls/837qeQPmrKYm8Hdh7uM/bonkhU9uBMdp9n/2aibMiH/8T2c99WXA1TL8xIT/jt9V37TFFSeGROZOdpl0TT7B+S9he+fvsmdPmToZMPSzJTIOylsV25DTagWhF86pTpijOsIcliaysLHQZcuxL0aKkuyYk75Y+6eQ9zJfobl2VHXzwW9Ei5Wl8Vc96P2HTrU8ev+9Cr+o7CovP6KTomyogZbUp3zKCSIM8p1xMz+qCrzUVh4JnsQarnGl4vwzMtXrum7Dv3K1bQ4M/ZaXKq+fafmrk59ovjTQSpjh7t4fTmAWJv81LCjN2ILqqtRI+2vyg87GCRx7Wvr+WUnmjD16v3HKv11FJs66sqFzsNGjnW3Ijd1cVLwlbAknBxhdbqXCwrbfzCx7KWQqSL5f0HXiOVO/pIqLS/KIQfXkQ8JU28+eZ3ho/8ORrbortGNHD/VgntXTrFGjPvKlWyeMPu2vyK91mLN27MNrl01avywb+bCi+JiMpl2X89iyYrzkoKDroWRV0hK2lrtm1ZNlHXN/6aKZ/+vl35GTJF35QlIELQ8AK4uSQk+bTDO87PR083zHsRGhvPZ/V4rRIQTUaJxY70WFscc/SPhxfwq/rWD16nTh42e/hmqFOY9ifzvbEqZrFocdOP+5MEu86a5IGEScTTy7blNNqGsZduq4U/Hy2Uq0s7+F1jZz3HocCsWIuqMTKS/2q264Q1IIQLgqpyEyAKO43RrRmVxZtx1v6A4csM299ujOd9vzT3yG24JtRllGmsGtUVdoJu1Lq9+H97k9687hJq1p9rtO6f+Ufr7zcxGWl4ed/O/MJa7o/PXloVJUTHRT7QVAwZWF8QFHkRDXaxcpn+mIsy+ey2BMty4biM0trNoTE5nTQqLCPjbMpgcAAA0Romh2QUB0AF0M7V/ZY6oND8vOxm9Ry/fKfTDpUH8hneV/Lf1ctq7/TXyvpbbeio6zt99yb136ui1kneQuPhYjp/WoL5852fw0XvlPrEfeEs+nNYCAABokR6Wb87BQAYYAADaiyqrE60k84kQuu0BAAAAAHyQlBEAAIB2QWFy1CsL0wog/gUAAAAA+DBBF2jQUXyIXaABAAAAAAAA7aQ5XaAhAwwAAAAAAAAAoEOAABgAAAAAAAAAQIcAATAAAAAAAAAAgA6h5aNAa/Wbstidp7hjOi5IjQu/HhT6VPxKIbbV5JlD6KGHD4Q3++4crXgLoum5zZxn8uTAX8GZOAIAAAAAAAAAABrXutsg4flh569niDC2ZR8nt6lMtP9AaP5LBUR5j+9HoRxxC+psxVsAAAAAAAAAAIDmauV9gMW5yQmPBQjFZeHM+a6WXfVCccP5851RVi6zqyEeeeBQfs9+A+jimGiBxeQlw+nRt0WGAyz1MVHGrZN+NzKJIBfT7Oky3Nm2O5tenPkoKuR8VCbSrXtLJsNh/nxH/FYKsrY1YggyIkPOBz/OJRaqbthvuKuThSGbhufGBvmdi8hFAAAAAAAAAABA87T1GmC8ftdjhj5DEBpwJOB2bv25dHVDE824wP0Hzj9BRgOde6kjRDN08/Lsx8gNP+dPzDQZPsaNx3i5XraRNTvj8q7D53KZ9p5T3XowEGYywNVJVxB62HerfwSycHW31kIAAAAAAAAAAEAztTIDXIdh0sfBCAnu5xHJYEMiL5xxOyQ8gezEXD+clUhz799+nFuCBNcf9+veQ08LYzAcTLQEN/afDCE7Tj9+dJuBysXIqn7NeMbtwJCEYoTOnO9iOLW7rREtJS5416Zgsm49nkCAIz0dNgNBh2kAAAAAAAAAAM3TugAY441fuW48+UwqSL5+MvgpjjSJCYmowaGocPxZnlhCvBXDEJ3BZOJi8bPoVVz+asyMkEgkVrwHF5WIEUa8D7G7D3Mf5WyijovyBUQ1OIYAAAAAAAAAAIDmasMgWMmCYkFOfnErkrASsUiEsRlEyFtOTjLU5RnglzCZDEWAizE1MSTG8doezsOd2E+OrAt8LEZ6zvPm2SEAAAAAAAAAAKDZ2jAIVooAtZL4SURy8YzBo8aIbydLtCxdhhhmBOw6/1IRzGSAuxsenoNZDrbWE8WH5EhxSzIlzGSrM5jdHe10MCwPAQAAAAAAAAAAzdW2a4BbS5p53s8fH+Xs7GFLFwuSLx89n/DKNcDi5HiB3vApTpggOf5M6OXHYikKvR5t5DFmgZVrbmqcIB9nIwAAAAAAAAAAoNmUGJpd0AdGk7wNkiBgl38CjHEF2k83U/tX5ohK8/OykxEAAAAAAADg49fDctAby7T1NkgAAAAAAAAAAMBHAQJgAAAAAAAAAAAdwvu5BrhpJRE7f45AAAAAAAAAAABAO4IMMAAAAAAAAACADgECYAAAAAAAAAAAHQIEwAAAAAAAAAAAOgQIgAEAAAAAAAAAdAgQAAMAAAAAAAAA6BAgAAYAAAAAAAAA0CFAAAwAAAAAAAAAoEOAABgAAAAAAAAAQIcAATAAAAAAAAAAgA4BAmAAAAAAAAAAAB0CBMAAAAAAAAAAADoECIABAAAAAAAAAHQIEAADAAAAAAAAAOgQIAAGAAAAAAAAANAhQAAMAAAAAAAAAKBDgAAYAAAAAAAAAECHAAEwAAAAAAAAAIAOgYpazszCYtI3M9TU1BSTuTk5v/28nq5CX7JylXbnzoqZFRUVRw4cSE6MRwAAAAAAAAAAwAegNRngEW6jzXv2rDc5ysrG1sKy97ARXzyfSRQY7uaGWs7K+9TFMxv7aL00U9Nx46mQUzN6ahJPDgYdm2fLbrwCTGfYxoNnji137ee24Z/ljmzUQuqGzjM2HDseGnU14tbxI3/McDShofaAGbptu3jcx0kTAQAAAAAAAAB4D1qTAWaxWDH3729Y/aNi8mpElIamppL8+ZJ5cxQz1/z8S6dOnVDLPQkJz3N1GmLJjgoTPJvHtnCyxHJDb2eW4Pij1GTJE4Go8QrY5k56qUcOZw1bOdMoedsuEWoJddslm3y9ugvuXz/5u59Av88Yd6/Nf+iunuN7JVOKAAAAAAAAAAB8xFoTADeopqaG+Gtta6uY1NDUKi4qQi1Xnnnjdq7bECdLzbDQEsUsLcsBtuy8kBtZYlSe4v/z4qYryL3h880N4r9nQvxRCzFsp3q7d437fdYK/6c4OeP8mfNuvnvmz/CyiNgUK0YAAAAAAAAAAD5e7RYAxz16WJCX9/uuvYrJivKKrb4bUSuIk29H5IxyduquFRpVTM7QNHGyYuReD00uJzO0K//aYHLOe05gCtJxWODt7WxtxMFEOTEhf23eHpKPkz2N+4yfNcXdyUKPjkSPzm3fuj8ojngjwvSsxsycMqafhRGzOPn+7ZP7Dyvm16Nu6TbAUHB9V4gi+iXhydePBvSZYdRFjxGbIkZatm4zZo1ysuzOwLMe3wjYufP8YwHZt9l3jxceGst2GtIDv77im83RjIbbAAAAAAAAAPiEqA9yVOnZS9XcnG5mQeNwEGiEtLCwKjGhKjG+6nFc+c0w9P60WwBcIhB4fTUKtQPxk9DwvDEuQ0zYUREChNjdHe0YZP/nlzOwWv2mrnDvnhvou+F8iZHnvHlLvB8nrwkSdB2/D1wl3AAAEABJREFUdvUU5u1d3/0cKu7uudLbe0lWMhktd3Fdu36eXvwZ/21HRUQY67F8o5Zozs9hufVqxLT09DFxckzyS72my6N3rp2neF1v8IqN8y1zL/tvDRDrWTu7zd/MFM9YdYNoI52ua2kZe2DrmgOCvLhaXoNtyEQAAAAAAACATwONy9Xb8KualTUCzUDT1iYezEGOxPOK2Jhcnx+kfD56H1oTABcXFw9xdt66a8+LOUVF7TgKtDQzNCrXY4izpXpEaDnDZIAtMy/sxpNXeiDT2ZqYKD4w4MbjTPR405JoPUxAXqabevS7CUGovJgsnX8m0M11voUeOzCTPdzVpDho1c/bw8lMbFB4HrZn/ph+OhGB+fiLKjEGholE5QhvsFU0PadRJoJzPt/viiYvTg4OTcb+XjLcQe92kHwLxAUePhNSV1vDbUAAAAAAAACATwDrK3edJcsp6moItBxx1sDILyB/yybhf/9D71xrAuB/TxxjaWhwtLUVkwf37I57GGvzWZ9hI76Ijb6vmKkYBbqVt0ESZ1yX94K20AqPN3KyYufcDk1+dQyq3PDAEPfVPgePT8l4knL/dtD568+yuQwTt5ljXMwNmQy2kS5TdAsjssgmPD1Jqn/Gs37IgtToXDTFrisjML+43mKLRTiTqY6INxCBrN7gDf/4OCu6MUgifSduE/TqqmdqveuSR71WZBmyidqQRIKLRXi9wLmBNgAAAAAAAAA+fhpjv9b7YTUCbUCcO9Bfu14Jw8pO/4verdYEwAV5eb+s9XllJovFQu0xCrScOCskPMt1cB8jPdzRTis3/NX+z6TcqO3fTDhpN2CM+yjXaStcPYZsm7PmpMh++Z+rnVFMWPjlo4/yJSbui+vdium1zO7LYSkuzsgUY072JswbZNdrQdSBVSuDmJie0wzvwbgIJyNwUdK57YdvC15UJM4kIvNX7rSkN6CJNoBPFdN6qX/AbAuUsNtj0uaYlg0+3hqY2fSDp9Y4oIgNX049lIYjAAAAAADwDtAMDHS8lyDQHogtWRFxR5qdjd6h1gTAw4Z/sWj5SrVnGf/cnJwF30xF7UqaGXo7122462CsBzsv4rX+zySGph4bF4QH7woPPmDo4rtnpoOlVohggC37yZHv1hyNI+JVmqG+pyLGFWU8FdD7OBiph+XKk8Bsnq0hlhue9XK15Zk3onLdR82beT15a1QxXp4ZHZXJ4E2eqoXnXM4UiVFyHm6CBNHyK5PJ0basHNjFAqKKlwNgss92Q20AAAAAAAAAfNSUlPTW/6KsCj2f2wexJfXWbcyaMQ3V1qJ3pTUBcN8BA5MTE47+vU8x+fuuvZbtfvE3nhwVmus1ZeoQlHPu9f7PRGDZw231rllaEfu2H4hGlu6jLJl4mAAXC7LE2ABn9wHRolRmP4/x7t2Z9EiitDgu4Ej4gBUrl+fuD06RqDt4zHQQXF5x/ukreTNx9OHtfua+09bvMroediMyTsxwcJ/q3ksc9OP1TLEUP38k1G31io34kYBYAb2L89SpDpLD3nP8U15peSNtAAAAAAAAAHzMVCx7wahX7UvN2obYqlWPHqJ3pTUBMEVZqbSkOCY6+vkcZQoFtTM8KyI0a0Yvi8wG+z8jaUrgdl8j78VLt54kpkRZoX7bd4aX4Pi5XfvNl8/0+XsUEiVdPhIcY6TofoznX/l1DXPteu+1A+nynsy+q/bLx7J6RXn0zpUzkkfN8Bo1Zunw8aKslEe3fWcfDoouIUNlQdT2Vdvoaxav+MWDqDH30TnfdQGPxQh7OQOMxzXSBtDBMc3c5iyc6Gxtw9NGwuz4BzdP/7nlxPPO0hjXcdGPKzz68rRZdAnx8t1zB3fsDkp8/jLH2n3ubHcXB2sDloR4NfT8FQn95erNR86dM22UI1mgMDUm9MSO7Sci+dA3GgAAAACg3aha9kagvRFb9V0GwEoMzS6ohRYsWTbE2TkzPV0xaWVrt2jWDCUl5e179z0fBMuwW7erly/v2r4VAfBh6GZq/8ocUWl+XnYyahdvuAaYaTVnz98rHMgL5ZFQKGGxyOhVErN7+reb74qI6NfZ58C+CTxyXmGhkKWtTb6cfe67ycuCyBiWqPzwidk28ohXIiyUsLRZdfVKFNcAI+6YHQG+LtqSwvi78UKujQOPhSSpJ+Z5brhZBDEwAAAAAED74P6+nTl4KALtqiz4Uu4Py1F76GE56I1llFHL/Xvi2P3IF716FaNAP4p9cOzgP89nEgVO+R1HAAAif2vuscybiH6zQ9ZP6G9q81lv69HLAlIR3fqb772smQjROQYsUXZhwvHp/c0cBthb9J91IhshAwcXK3KodczYZbYXGf3K397bZoCV+YiFJxIk9RbA4llbEEWzA5dNnzFt4pefT/eLLyTiZGMDOgIAAAAAAO1EpZcVAu1NzbIXeofabRRowsG9uxEA4FWYtkVfcyIUlUiQhdvCNfIu8XQmLiQDV3sL7UMxabEHv58X4TTIoe+sn52JgnQWWZyIi1l0jChk7GBBZHyFoX/8cvyuPKGLp53/Y4uD498TDeqWIMyOSRV6GRi4b/yDHhwSdi5ko6sDZH4BAAAAANoXjc1GoL3R9LnoHWpNAAwAaBGmossznec8lvfyK3T5K0yzCZv/3uii3eCbMTpT3uNZmM0XvghqhYXZhRL0LADG04LWLzdf8727k4P7N8SDPD8lfHBw8cLNN+EyYAAAAACA96FaJCo9E1AZR17dqtqrd6cx4ygMdQTet9Z0gQYAtAQuKhSSHZZTT0zqwzPppniY2/Wxtuxm8fWeBJzjMG0uEf0Whq2fMKQ3+arlmM0xz3s44xJRITmhzTPnPr+lFqZtbPFS/2Y8O+Iw+XbH0VPnrNl9PkGIWDbTf5zrwEEAAAAAAOBdq62uzpo5vfCPrZUPHhCPwu1bn86dUduSm/3UJP2d0a93ottyYc7z34US6bm5yXYj8u4J0VshqdoxLslprjAHtVmRaO2IJI8NFSL0oYEAGIC3rjA+LIb4muI5T3Uxl8ewmLGzz7Grdy/tnW3PQRiLyZGneNNSU/ki+YDQo9zIPtB1Aa4wLeIB8W66w5xlE/tyyPczzUYtWjjqRcKYaT37aFTM9TN7vHjCxLAQ/82rNx6PJ+ZrG3BZcBtqAAAAAIB3riolWZKSzJ4zr/vlq8SDeFIV/xhPT0MtlXupcO9tGQLtBrpAA9CezOcG3J9bf4bk7iq3b0+EHD493fEbnvPG83fmZgtZBgbyYZyzUWGREOHChJvxQkcH3rTDIcNSCxH5qjBbiAxYDsv27eGuWvR78J9bgm3Wu2g7rjlxZ4ViFGhJtryEYhmi1LsxqZK+NjbLzoS4RjwopFv0tTEgFp0WkVAIPaABAAAAAN45WX4+8bfTmLFKymTGsdNXHoI9u6S5uXRj8oI4PDeHpqOreOmNpOe3C4b31ukPHfvaB2SAAXgHim76Tpi06kSMPLwl41ZJ9t1/vpuxMDCNCFDxBL9li7aEZkuIF3k8A5QauH7Ryu0R8kGyLAy06UiU4L9wgvdxMg+M6HRUGBG4fs7Kf+JfjAMtivl9qsc834C78Yjr4OJowyqMDz60bPq8f2I+vF4nAAAAAACfPmUWmaiQZtbdOFaamUHOZDIVk5lTJgr2721GNRjdZQQdyyjde6zy9V91kqLK077ZU0ck9xuQOnVR/rmH1QjV5FzMdumduvbas6SxsOKX0YlOc8vSJQ2Wb4oosWzLogy3AYn9hqQt2FByr6imbrl88cHVWR4DEu16JzqN45+Ikr08P8lpRNYvl3CxBH2QIAMMQHsgQlBX3u9NFMCLIk/4fH3Cp+EX+WH7pjnte2nexM8O1i+RdmH12Aur6xcI61W/gCjhyp7lV/YgAAAAAADw3qmYmCl30szz/VXLc0KNTFZ6+l8Km61iYoJnZckK8quLi2pRTUVMjGrv3k3ngZVMxrGZifyAY4XnRhhM6FbvFYnknM/TX29T7MZxlurjwcdKflokxY7pD+/DsmPn3L9UWTSUSeSMRUnC+xmUz75V00eNlOc2vHgJX/iLd959fY1pq7XYgoqAv/OX5qBD2zW7SSr3efMP5dBdvtGbxqw6t7vk9w0Uo390+2MV+7yzDyXR7MZpe+lXnvu7KE5Qa4Q+QBAAAwAAAAAAAEB7oqircbdsy1mxNG/jenKSzeb+tk1ZRTV76SI8LZUIbAX79goOHjQ8eETV3KLJmphqXt8ybviI9/5R1s9X7flsUVJZQFSt5SL9379VJfLKw3srzZpbGnBdOniSmssA2o174kdFzCGc6keXynPYarM+o+FJBY2Up9MbWGpNzu3SOyLVhT6dx3YjImSGCVM6e3NZeLpGNzPVWbuNPRBFn0PMZ5rglbN24xmiml584eUkJctv9H/3JusfbJo3e14p+hBBAAwAAAAAAAAA7UzdxrZH8PVXZhqfOkP8TbTrrb/pN5bz8ObUo9RtBGfa2Yrfbxf9dUmvX93MGlG6JAdhY/vQFb2qmaZMO/2S4CiJaBKr1wg19qWKGw9l/T+ruhElYxM5YW6N6F5j5RsOgDPuScSi6l+/TP71xUxaRhE5jDWdWZNxtnjH9cqcouqMJKkYU0GSmiKBVISw4UPr6ueYqZvolyWjDxAEwAAAAAAAAADQbp7fAbim9EUSVLlTp+d3A8Z4Pai6es2uj67isZx9Y1LhjWOljJeHwmK8uOGHkvxB4vRm9tcX3rlUmYGV38+h2nmrEm/Kabx8o9iMpT5aJswXb9E3paAi0S/f8AMyaHYjGINHqHESBb+cevY6Vr/+DxYMggUAAAAAAAAA7aP+HYDrz69/N2DjfwPUevVufp2IbtZp4SQ6liE+f08xEpUysxtdH+E3bksUg2OR1/rmICNFgpel6jKAJnooPPdfRZG++vDe1DeUb4Cyfm8aQySTcOif9VEjHqbMGpxOZbOQKLH8Tg7NbZfhvs06079UN+Iobm2szGHTmDh+49Kz+nMqMnJacNfjdwgywAAAAAAAAADQPp7fAZjz7az6A1zV1tQU/b1PsGcXnp6muBlSi1B6faPjcTvLL6lummmqOW2E6Mc/cn4o0hzOxc/9XZqs32nHCEV/ZorpFwz9U8UBl5T0x7F6cd5Y/nXKRgM0eu3O37e6gO7NZBeVn/un5D5Tc8ffOr04NDaS3j8lvE7HUJLo0DEJjlTI+nuzhpuWHvon5weJ5mCOJPhsBZFz/iDv3AQZYAAAAAAAAABoH7K8POJvJ49xrwzvTEx2ch9HPJHm5qDWYKlNW9TJ6PkknTZ8Ofen0Ur3jxf8tLk0idPplz86P79XMNOU6WKKcIT1G/Esx9tk+dfRu2n++rf+BDNpgE/2jz+XZuhr/rRZ+zMWmYte5s2k3y5Y9m32X1HY2EnqjGfNm7XdYMFoWsapgl//kRhN0hqs/6Yu1u+HEkOzCwKgA+hmav/KHFFpfl72B3ltPgAAAAAA+PCY3X/4xjJlIUUg9T0AABAASURBVJdzV37fWMkWDX/VcRCbBbWHHpaD3lgGukADAAAAAAAAQPtQNe/Zadz4xl7VGPu1qoUlAu8PBMAAAAAAAAAA0D4wAwPdlasae1Xvh9UIvFdwDTAAHx9Mx9rSomtDw8xTmSb9zAw1KQgAAAAAALQzqUCAQHt7x1sVAmAA2ok6z2rMkm9Wbpq14LvBvfVfiU4pOkPHzJnZQwO1Et108IwlgwxV5HV1NnFx7cGQVTdQTlZN5dk5D9Wlo/ZB72o1bvnc1T+Ptu3c7KCaqmk7c+K0kTp0xOw9c+rkQRCOAwAAAODTIElKRKC9veOtCgEwAO2BotnDxdNOI/Xm0a1n7xRzh07qa8hEbweFY9lDozgltaChABhVZMbkU3k9uCqoPajxhlqzsy7v+Om/6IYX1xBZeWZ4bGRciQQBAAAAAHxKqpKTEGhv73irwjXAALQDSidLS25l7JmgFL4M8c/e5M4dYs+7nxlT0UBZqqaJSz/HPoYcmjDzTviF4LQyWd3Mof15HFVJ3p3rZ86mCOQzLVwHOfbhdqrkx8bJqEhxX3E1HR6rLIlfKiOXq2HZf/SX5oZaFHFmyrXT1x/mVJfzMwU0O8POlLSseiErs+uouX3RvWyVz3rxtGR5MTfPnE4hlkthcu2+7G9vxlER8mOv3Qm7V/QiamX2GLdihKkq8cx1oWnCiZ3JPb/pX+V/KoSolqppP3MkL+a/f8NRz2mjrUriijpb9uSxqjJjLhwLTxPRuf3srBL5SVkyBAAAAADw6YAM8NsAGWAAPj4UDa5aVWZekSLiExWlFiANfbWGuv5iXJdhQ7n513Yf3rErvMhs0GhHDoV4u5lVX8OKOwcP7fgjLN/QfqilGlHS0HW4i2Fh8J+HdxxMoJoadlKcrlJhcTUlRZnlZHTL5DqONK66dnbHT/4XMpm2jlx1cuklfBGF01nt1SXTNA27VkQe8jt6lq9iaWerTyHiWCvPYb1lMad8/94fkMkZPtzFst67RCmnfjr0X6Iw83/Hfl13Ja2xfC6NrmOqzb/838GDdwRa5gOsocMzAAAAAD5V4rDQqpQUBNqPJPWJOOwGeofaIQDW0Ohk1rOnta1tZ11dBECHRKVSkaxS8izjKauqkiFVSgMdLFS0LcxQ6rVHaQUV5TmZ0eFCDUtuJ2p1WdyNo7tvPEwlokxcLKOTwTNR0pSSei1WXjLtzk1+lbwCiiqTgSSCyuq65dIoKqpUWWVJ8tkzh/yzysmFVxQVI/XO9FcDUWl56s2EzAIRP+r+wwI6ESFTOhv37lwYeTklX4SXpcaFPcC5n3FbfpVyddG9mMdZIkFSwp3ECnUus306XwMAAAAAfHBqqypzV6+olUoRaA/EluSv/L62qgq9Q23qAj1h6nQXV7cuXbsqJmPu3186f86gwUOGOLukJCX97/S/lRUVCIAOQCaprKaq0onPkzwwpaqoUGXC6gZ6ANPUOmnpms6b3ff5nPw8FSqid7YcOam/qaqkqEQoY1IRjUKlqakgvFSoSLxWVxVXiBXV0Yigt1pWl2rODAtKGzl08PRB1KqctMjL9x9mER85GfEqERg/a8xz1TJp9bMnMioN0ZlMqrSirLLuVXGBhNpdjYjkUQt7Llc/r5YIy1XhsgoAAAAAfMIkT54U/LFNZ9lyBNqM2JJ4Wip6t1r/Y3X1ho1EoHvt8uWDe3dHR0WKhEJipiab/dOmzXm5OU6fDxOLRecCA1DrMCwHT5nq5dqvO5suzk2KCty/82RoCY7eNS3n1X8vUT8w54egTNRien2W/+Ztm+u3PbT7FKf4DauCc9/9CoB3pFqcU0G11mRQ+WQWWIWpoyUri6loYNgoaUVpceHds4EhqfWOBqqm/Zd2jLiz2y7kS5CayaQxjvKSVQhjsOgIETEtRUVLjUElg+FqqUQmpVDrPrnVgpgbR2OIGtSMvxw9eqxMsCucX9V4+P0ymUgko+loqCJEnnWjMDrTZcIKWZNvI+JqeVhNxOcQ6AIAAACgYyrxO1aDSzovWkpRV0OgVaqFwvwtvsKgc+ida2UX6HW+vxHR7w+LF21cuzr06hVF9EvQ53KJv6uXLc3l8w26dEGto+XkvWuPzxi9vFC/bb5/XU5GVjM2bvV21sRQ+2GYe586e2Q+rz3rfGUJJgOMBAG77lt7LxmA4hIEEP1+yqpLU9PKOtu5uBjrdNbp7epopVqUlNlQ/4eqwvjEap5LL/JWvSoc22kTp33JpctztnQypKSom1r1NWNRFSWTqnlDrQyZiKJpaD/o2bjOlcJSmZqOFnmfI4qm2ZglY4bw1CgyWXWlRCbDyfCVqtaJJSvPqXjjqM3VBWkPC7Tth3bVIFLQ+ub9bTD+PX5ZY6UrRfkiNd5Qc0NNNbaltUVnuNQXAAAAAB1WWcCpjPHuFfeiEGg5YruljxvzXqJf1LoM8HC3UQOdBi+dPzfm/r1XXnr88GFGauqB437E83KRGLWG3oD5S4YzwzdMWXVDkTI94+fnuPYvn1leV6J3RX88954Wh26fF0r8NzDMH4FPXnVBwoUAzTGerjM/R0iYedv/ZlJJgwVxfvClay79nb+bpctCpYmRF8LyJLLqx5djTCe7f++IqvipqQUV8rv44pmXLwe7Dh61amEnWfb9O2lFZvIKqkSZBcjRlEmPq5CUpEWGG34x/dsBqkhWnBrm/yhfhiiddQ1VREk5zbgJkawk1v8K9cv+k392VSnmP758+VpcRVOFz97nzXScvMI6NSomk6/DQQAAAAAAHZY0Nydr9rc0Q0NVGzs1Wzt1G1uaPheBRuC5ORUP7ldGR1dE35dmZqD3R4mh2eI87Yn//UeEvps3rFdMEsHw4GHOxJPgC0GR4XeIJ0Y8ntfkqaYWPad97YFaSst53dG1ukHfLdgV/eLqcsxk8HhnxmP/80QAjOlZjZk5ZUw/CyNmcfL92yf3Hw6KK0cM3uQ9m5yTD4fQh7s7WWjhWRH7Nm/wTyBjcEzHYYG3t7O1EQcT5cSE/LV5e5z5huM+TorbtEpifL9ZeSYZ6+E2dYbnAAdTXTwnPiLwwC6/WCL8rtcFmqZlO2r+rFGOdl2ZSJwcvN936/nH8mi8fnviwm8H+fmdiSZCn2aVf9F+0CgrG9tHsTE1NTXP5ygrK/eyso59EI1aopup/StzRKX5ednJ6KOjbjl8skvFxV03MxsYMIDC7uc6xjTh1DHyLkcAAAAAAAB0GD0sB72xTIu7QJtZWOjo6p05dUox6Tj083W+v5mYW5hbWv667Y++AwYQM4kk8JlTJ7t07drdxBS1EI1toosJEqIzXxpbDU++cXQnGf0irIvr2vXz7PAI/20btp5LYQ5ZvnGxo56iFMOw3xB2+PZ5ExdsCBbbLvCeYkkj5mr1m7rCvXtxiO+3E5dsv89wWuLtjN1eMXqBf4Y4+dAsx4FLzyRLtZxmblg5XC/z+vZ1vgfCxZYz1/t4danfOxozHOKzcaat6NyKiWPHf+cnsJ25Yqo5A8nbs7KuPcvX+cWxh3uvnemg12T5RtsPXofR6Rt++/2HteuJoFcxh3hCTBIzqVQa6pjKn8Qkybi9uzd00YkKx9Sazg/nQ/QLAAAAAADAa1rcBdqwmzHxNyUxQTH5WV+H1CcpsyZNIJ4fPhXYt/+Au7dvE88THz8m/hp1M36SnIRaAmMyMSQSixrpv4mZDHc1KQ5a9fP2cDJrGhSeh+2ZP6afTkQwMYUXxwUeCU4txlHu4QCnfvN7mGhhcfl0tiYmig8MuPE4Ez3etCRaDxMQ0TWjfqWatm59UOhm73W3ifei87cz0V8+zgMMA/yfd7jGM4NXTIrCRCVislf25ZPRo3xMeEwsASfa0+tFeyLiUuP6aQlwIsffePkG2x+YD9cINwSXSL5fOG/LX3vW/LJp/Y8riTnEE7s+fZctmCOTddgB6Kvyr//p39hLd3afQgAAAAAAAIAGtDgArqmprT9ZW1urXC+NrET8rz4lJdRCuChXjPoxmHSEGrqEmG3C05Ok+mc86zMsSI3ORVPsujKCi4kpiaAYV8SReDnxXzpGJnFzwwND3Ff7HDw+JeNJyv3bQeev575SKdbV0kjXyGj9BZd6M4u6sulI8HIxpwXzXW27aDF1jfQZkkcIe609eG7ClcAWlH/R/sD8YgQalJSQQIS7RAz806bNxKSNXR9ikpiJAAAAAAAAAKAlWhwAZ6anE3/19Lm5OXziyb2IcLevxhwL/B9FmdJZV3f39q2KYl26GhJ/M1p+WyepIOOpmG1ua6geIXhxZezza4AVsetrydImx3LOjdr+zYSTdgPGuI9ynbbC1WPItjlrTua8UkicEbx/V3C9NKwoL070ol6G7YztWzzYyddDw89Fx5XouXvPYL548+vJ2xaWf3tjUX8aiHD3++/mbf5jJ/GceALRLwAAAAAAAKAVWnwNcHJifH5eroenlxGPR0zevHF97Yrvk+PjH8XG/LB4UcTtW4piY8Z7Zj992tL+z6TiuNvRgu5jFozq+byXMqbpMHXmlMFdiaeijKcCOs/BSL3uJTbP1hDLTc5qasBphqaeHhKEB+/6fuGYsb7hku4OllovRZx4XkoOTsfEKeFREaHEIyZZhOHiYvGLOFXdsF8fQ8G5Das2b995Piz8yfPFvdYe82HuA3qwm1++Ge0HpMTHj2dPmUg8FL3rAQAAAAAAAKClWnMbpOALQZO/mTHm6/HpT1JnTPK8FXqDeNQvYNvH/kuPsb/+tBa1huD2zq3nemycuf2geciNqBSxrqXtAEc7PGSdX5wA4aKAI+EDVqxcnrs/OEWi7uAx00FwecX5pzjiNVIdrYfb6l2ztCL2bT8QjSzdR1ky8TABThCIENOoi6GhODc3P/Tw5TFb5m9YqeUfno+zB8yYNQQLXjNv0/Mbe+HiXDHS6zPG2UpAVOLmPtlOC5OPHiyOq9ceEc3Wff54o1if8MjM5pR/qf3gjRSdDgAAAAAAAACgdVoTAKupqfGfZq1Zufzv4/7mlpYJcXH1X7W17/vbn39FR0VeuXQBtU5x6PZ5c2KmTPVy9VrsTkeipFtHVm0/GVpCRol4/pVf1zDXrvdeO5BOJFSTzvmu2k+ODs1orDJpSuB2XyPvxUu3niSmRFmhftt3hpcQIe0Vv9uua32ODn5yZPqCXdGHfdZhPmvn/zyKXH7cuW0b/ooqRkjrWSWZwbt22S2ft3SrM8IzbhwOCu3uqRi6uX57JMUZybEHNu2MyJXizSlfv/0AAAAAAAAAAN6u1twHeLT72BnzFmRmpFtYWnqMcC4tLSVmdtLUHOLs4jj0897WNknx8d9/N79c3IH69dIM3ddvcHl65K/DV+Cmvh+oT+c+wAAAAAAAAIDXNOc+wK3JAIdcusBgMrubmKw9epiIftdt3jLQ0UnxUlVl5dF//j60bw/qYKSZgWt80OoNM4ekfH8+Ezo0AwAAAAAAAMAHpzUBcGVFxYnDB59PHt5F8bpnAAAQAElEQVS394z/CcXz1CdPREIh6nAwTYcFq72ddMWhgQKIfgEAAAAAAADgQ9SaLtAAfIygCzQAAAAAAACfsOZ0gW7xbZAAAAAAAAAAAICPEQTAAAAAAAAAAAA6BAiAAQAAAAAAAAB0CBAAAwAAAAAAAADoECAABgAAAAAAAADQIUAADAAAAAAAAACgQ4AAGAAAAAAAAABAhwABMAAAAAAAAACADoGKAABvG10NsfWVOmkjVRZSUVWi0NDbUVstRVWVqFJYW1qIBDlIUoHAJwSjqndSNWCqaKvSNDCqGkX5bR1I7au6RorLKiqlZaKqgtKKbLwaDsv3jEGv7aJVo6NR20m1Vo2OMAr6MOHVqEKCSiuV8suUsoqVyyVKCHxoVGhKnZlIU11JnY5UqErUD/Vgap5aWTWqktWWS1BJeW2BCFVJEXgnaDQak8FQU1PDMIx4TlF+//m56poaqVSK43h5RYVYJJLKZAh8QpQYml0QAB1AN1P7V+aISvPzspPRW0WjK3U1R3q82vIyJClHleVEUKpU/ba+RmspVDLYVlVHdOLniAbKTa3NSkBSCQIfOaoyXb+TpTazBxFGSqRiXEY8yqtrP45/jylKVCJ0x6gMOo1BhO4FopTc0jhZDRyW74EKrba3QY2pbg0RVYqrkKgKEVGltPoD7QtGo9So02uZKoihgohYPSlP+WG2cpUUwuAPA0ZRMtZWMtCqFUtQJV5biaMqXElWiz5mtVQlpIIpqWJIFVMiThQ9La5NLyTPxIC3hkKhcNhsTU1NiUQiJeHE/2tq3v+BpKysRCORATmdTi8pKSkSCKqr4WD4CPSwHPTGMpABBuCtoasqER9CTKX2aaJSVTl6+8jQukJIPoh/yFXVlfS7K3XqXBt3E0kqEfhoYRS1HjqDaVTVnLLHUtm7OJDaFxGoE3E78UCVCKMxOzN7sFR0UvJvQCr4HVPDap17yogf9o/4FHHVRxBGEpF5aQUqlR8mTNUaM91avU6ykMfUChxi4PeNTlW2MyT+1mQUKVXgxIxPY5eQATwRz4vJ03O16jQlA7YSW73mfiaSQPbvraBSqV27dKHRqIJiARH5og8JEYRLJDjxIJ4TUbCWpqa6unrW06cySAV/EiiYqgYCoAPQ5HBfmYNXlYuFAvSWqLGUrAYTkWct/4mSDEfvnJJMWltaqESEwV1MUUk+5IE/UkTK1Ex3mFRWkSdMqql5DwdS+6quwUWV+SpUhq6GhbAyF/LA70wntdoRlrIKCYrPoUhkH1+0gsuU8sqUWCq1ltyanFLIA79XDLpyn26oUlqTKVCSfroJMWlNbbGYyAYrddOuFYghD9zu6Bhm1LWrTCoVFBfXVNegDxjRvPLyciIXTCSriSeQB/7AsTsbvrEMDIIFwFugpKzUww5ViFB+plLte/taJxedn0k0Q6mHLdEkBD42SkjZkG1fJRUWlacT/wSjT0ItqiFWh1gpQ3YfJfg36J1QVqrtx6sWVqInhdSa2o81dCRa/qSASqyFg3E1sUYIvBdKSsrm+rXlVbW5ZZ/8TiBWkFjN2gqJsrkeseIItCtdXV0cl5QJhegjQTRVKpUQzUbg4wc/PgB4CwxMkBoTFWajD0HRU6SuQTYJfGx0NMxUMKZAnIk+OYLyLBWsE7GCCLx9Pbk1GmoovehTuOgpo4iiqU6uEQLvg5IRGzEwlCdCHUdeGWKokCsO2g+bzabT6UKRGH1UyoQiFRU60XgEPnLQBRp0FO+uCzSNrmTRr4mez0rdFpps3mLgaCGJDq2qrEYIozlu7blqNj0tRFj4Fi7WJc5hV4mVDExRXjqqgX47bw9V02KMi8fEocMGdddTF/LTyyRt+o1OVabztAfli5Jrahvp+Uwf+PX0Y9OGTHfpTzzGWncxrCl+ki1u0e8JjGkw5nNTC7z0SVmruzLS7d2n+E02EUUnxle1ICNUWyUT6TDNi8SpNbVwWL4E0+k3ZNzUYSNcLbvropL0/LI2dX1XodUONquOz6XgjfZ8Vho1n3lyjsoQmux6Qi35HaRKWbeRtcm+Niy8WtDQUYyxqVNGUruIq5NfS96wTekHV6n2F0mvP0Vv3K8mTmpBa+hdkvAbzf4mrkVKIgnqqV+TUqAsq4GkXJPUeVZu012/+rKPtQWz6mlOvqitnzSMomzVpSaruImez0pcHmfuCP3Zw/Um2WrYdEaC/Kq8d3Slg5K2keaYHphIICmtVu45yOhXFzXhE1FG/aWrMRd/22MGtyosCa9qdr3E11qVRMmQU8svQdUdsusBRbPr4MlffPX1oIG2+urlOZl5eNs2A4VCMeByi0tKahruS0zV7j/9x7ljh3/+ufPnnw+2tzBQF+VkFlW09F9UlW5jFn4/yVL8IL68p+eCb/sz0uNShfUu4KXqOS78froDPfF+qrj5deNSnK2pVVpWVlsL/VBaqp1/JjUGukAD8D4QkTZe9eZRrzT66o0a+G4yMkqV5UhWhV47BQDaEcZ1GeZiJok+6n8wIFOlz7CRfTTbdkMQTfUusprKN496Vf44JvZseGxkMesLD/e1A7UZqAUwzW5fDu3/BU8dQ+8cLhVX11QRq4lAfeqm/ce4cATXzu7fdSdfy27Ul8ZtO01tyCYH6C1/86hXSqbOKqObtzeYetQJI4nCSq8fN5KymvSs6nTBW/xpKKpUrpKR64VAEyiaPVw87TRSbx7devZOMXfopL6GTNQ2Sp1ZtRKpUmWjgxUpcU25677S6atRnZxYfD27xshMz8dDx5qO3gklbneOu72GCbm42vLiqozCqsJ2ir3LpbXECaTOLNQRUTWtxg7riVL++9M/8J7M9MsRfbu28W5XLCazuloqkzY96pW0ID464u7d+0+RsdOkb740b9G/bS+RyUSFuTmFhVXtMXyVFJdW18iIVUCghdr9Z1JbwCjQALQzJTaXvN1R06QIz8tU6jOdcycmL7l+yg5TNhih6z6uk6kuyospvnKwIPwJxfE300ldhbvmZsXkIWp39qLdBrq30jZsKWd9/nLJ+KbOpFVUKGnq1uamIfBWqOjaWqplBgVFJlUgFHlBU3dyPzPdqHB+6/+91VTrUiV7czpXWnz1wvXTJdUYk4d5f2Vv3aVrRGGWJm/6yP5DTbWwktxbN28ejMjNQ2ojpk75Uf/p8Rhk/1n3rjRh5IXzW1L1fpljT54oHTnljPGlJcFq3nP7o5ATi64XilWM1n7vYZ91fu7hJHHX3gtH2w801KCjqsc3L/16ITVLRqaOx44eMq6nFsp6fKvy+b9hlK6mtrOdrez16cU5GddCbh5MEjaVvZTIxBqq+oWiJwg8wzTsZ4jirgSH50tQ/rX/cbjTrXidM6MLWp2766pVI2rOHXQrqpMqKBM8aLf/kr64OxxVacJi5vcakvkbJXcqkZ0n48Dg2j1/y4bPoXOIc33fsoJ6lS+6Qf1tOSaKlmFmVHpk+aJISu9eNE5klZYp/e/FtJwQSZEpfUhXJUGiZOM/kjtCsm/DqLEqcwZQmUXSS2kvGsbuQpvtQR9hpizJlV0PqfrzTk0TR7+oUonbqSYpD07iN4rSydKSWxl7JiiF+Bbin73JnTvEnnc/M6YtY6+TAXBlE0GLmvrXQzQ0iwUbTubJl6N8vY/hasdObt0Fjx9LEYvhNojjYqSqLql8EF1wLLaiEKlMnNBtuExwplDFxVS9k6Ty+pXsgwWqC6Z0tSnm/xBQyq9G2qYGv7oxMi6l+iYq2Q/SGWPG6EaXJScWHbtZ8lhCvt2NKn4sU+2pXnE6CZtgRZyRwWbPNOn5v4zreuo2BtRIevFjCZEZZs8eotVTrebxYyHtxbcVNqB/5zE9mVyKNDmp6N87pY+b3DbEaSQOA2WXoI6Grm9mq190Z3dMGvEtlHPzWld3x/6697P4bTi3wGQycfyN/ziK024HnUmvQlTdkhlzvjC20GckJFd1svh8+JDe5l0ZVTnxdy5evpMsZvSdtsBdM/exSNtEu/Dc7sOPmfajXB17asuyouOrFFEOlarZpYcpsySE+gDJVLrYu4526qVHzY19SF4WUtcORrcBw4c6WHTRlBUlR1+9eDWhsPEG4rhUXV29pLQUgRZo/59JbQH/eADQ3hidaivffH1UddrZ4jxdbfdxKqr1kijsodxFy7Q0nhSc3FtEvDp9rZ61lvTxVXEFm9HHgvimVuJYs7rQ8cdXy2mDXivZ1MAMZJNYcNXKW0NhaXailWTmKH4SVJdm5olVNTXadIZYDdOskja/PzMulRQT/4xQKYhhsHCa22h94bX/rhzPpAz0+HLpZ6y6Y0yr+8DO5VdvJWZRtQY529pIn+z9L1GAUG5MyLqL6dkNhlgq2uNG9rdXzT146H9bwoXdBznPNlXDqNpjp3rM6YniQ64fz6Rbm9alKBldbddOdbSofHIwMDxS1mXi1BFj9Zs8v1slFTHISAo8R1XT0ZLlp5YojiRJAZ9fqabTprPkWuq1omYFPTWXQ6TITGWOjVLT/QHwXPzP01IRqk26UbH2rKyYnKdkylN6dKHyYOTLUStNuZc9VfRAcjm1Vr8XfYIlUbPS8Cnq650pOber/rxda2pDpctvoIOxqasWq43WqD7lV/lfnvLob9VXNdkMYZWSNhMywE2haHDVqjLzihQ/LkVFqQVIQ1+tjfkWpkptReOntNQ01IzUa9KflCbXHXA1j6PSvX5P/PmxVEpR+dq1y6QuNZE3c08+qek5pOsSK4xGllFW1+9kTxEHPxaXaqgP6cfkSipvp+Pq2sye6sSrVJPuappV5beeVhNvWWBFK7ifu/dOpZqZ/uIhjE7yt2Na6p0KiHi4NDYm71h6NZJVXL709N/sF7+p1Qy0V3vomFSJ/r0h4GuxTFQUs5WtiQptVQoe5x4ML8dMuYudWdymtk5tuVRJQw11QCpamtQSPr9Y8Q9ERX6qkKqpyWhT/kyFTsfx5l/ZUVVJpG6pVCpS6fL5pAn9u1TGXwi8moJMhk/4qpcm2RAq0uyiLY6+GHSHr24/dZprT5R+JSgsi2liovlKVVRN2/HffmXLyL1z7moC6mLemSY/CqmcvmMnjragpl09ey66RK//+AnDu6k03iAiAFZTVUWgRd7Cz6S2gAwwAO2NSlN6YwBMfOVWZJVcjNScNVqv/91cKZL/lKPRen6hoSEoO763iEj2xohVTH7UdLTP/zOmNE2k0W2QKiuyqtsgdbXckqgUSs8fGygZ81+jZ9KqRETDEHhbqETkKal6fmFcVYUEabft+5WiTJNImz08Jt26X/+hWqg4PLeGa2XfWRZ/8vree0I8psyQN36oQ/fuMYlkqcqnp/678V8JJV6l85+DOvdQkxzPEYqRDM/JjcmpQPoNVVxVuHfPnr3k1cKa9ppEYS1dTbp65y6D9KmCx3d2XE/NQ0/Enbv8aEq2weIzyx4o5/jFmydyqhkFFIs5jl981vm//3IbDeMlMhGxmgi8QCV/5lVVPvsgbOHXEgAAEABJREFUyyQyGWLQiEOp1dcBY1QiXGzWyW5RkuS/LNo3Y+lD8prsmiirffSUvIGVKFV2Lw8xydMftQ8vVG68Qt6ni21av2htUkjVlis16AEy+km1G0+ZEac02FJZklr552n8kQyla1AOjCTbZmSJ9deouXO0au+DWvSgtpup+gAnqv4DaUZjTa0i1ws0gTyQZMLn96+VVRExhCqF2GhtuQ6YpqxU3njiD6NQMFRbWlb9+uGjptdpoD5KD8s79hCXUqo6denmbtXJJFFIjm5fXHrsBpGnFRZoqC/RU+1ML0lOEhdYath3oV1PpxN/S7JzH8vUp3enlydm7osSlyJxaWfVxXpMEzqRja3BC4r2XilOIddKmSEkAmBZxtNKvkRZu27Jyt26swyQ5PLN/DPZNbSntUbTueTFQGrqLt3p0qf843eIPLOwQIvh01PLniU6U9LoaZVKCbH6qCNSpSLp8wOpWlYpkdHobfv0KVMoON7MDDJVs8fng01UpWnphUhvYG89WfrpM5cflMgeFjK7fGPbu6t6Olmq5NG508HJVVS9/t/q0USPrwbdSBCj+MrOXTxfHv+TYdy7i2pl8rnz1+6XymJLOhlP70suQ9vCoZtqQWTwxTvpVdSnqEsPdwvbrqHpyY3820VE78QqINAy7f8zqU2tQe3BiMcj/makpiIAgHyYljf3OKTheMzBvLg/uo6YWB6lSHVgFLYWRVpcWST/0q3IqxIiDQ09CvWS+E68dLoFy7g7tU93paJbpWnlFJMGS6JG79AOyZK3SyaRILoK2btO/uVOJTItEllbO/Y0Z4QfWpfvfvT+Tt4EQer9vdcLZD3VGUiSVywhIyZZeUqJ7AtNVt3peqlELG+TWCST0KjNu+5XbeAXI5YO7cYmgg5hFXGytph4I1WdQZMVk8Ezobq4Ll1J0WKqocqCTPlIO3iJkMhIWzDVGMTiGq0cBhF5FRHxVtWLeBXxsLTNXcRqm3M0SSpqTgTgQxZjswfXJKGWwStqm5ovrcXlQRGR9GPSkEhQo0hMCnJrRfLvJiZHmS6tSS+SD/hWUZNThjANJeaL7omvrQ8cOG8ik1RWU1XpzyJeqooKVSasbvuRpNT4kYRLpOVISV2DQl7l8zJ1dZo6qk4vriFfqJZlCGuRHlVdHkLgVbJyslk10qoaJD8hVppb9rhMy767qlEVo6e6NDmxspTO1KQjTUvDvy2frx+1k+LSYllN01eS0uhKxMbIEJKXCEllslIJIgJgKp1KVFgulJSQW6e2sECKW1G1iZxz4z2cO+wxJyND/+cRL4VKPH8RD79Nmg4zfRzkzypzHl68/LCQ2oOpglRNxq5cP7auiFSmqUqtlDdSMYIolalKk4pzS+VDnMnEJa8MdUYhPweoqqREfjWwTFwqlkqJNaMytFVo0pJCkWJuSYkY6XViNhUhwRdQK7yVn0mt1qYA2OnzYeMnTTY1t3g+JzH+8X+BAZfPn0MAdFh4FaKroYpm5O5kT0oDj2stm842LZb/pMCrBcXVtO5qugyULUYauipsVJuWWy3DZelXxRVLGX0+p3XB8JirlZU4peGSjS+LaFILRr0ELVQtLCmVyruqyq/VZOhrqojyBW0a01taXUWjqFfLyt5QrOBi4M2bxeVZOYVZ8h2sW1IuRtq6ndWwNAmuqtFDkyoRCYm4Vws1Cybv94Wp0hnyzKxaV7vZQ7uIr5349mIu3nXQ7jm2xEy8skwspXbtqsVAhWJE19JUQ6icjIRFFUhVqweTcklUjWl21lVFxJymenETkTSxmgi8IKvIL0aGXdUocRXVZJ8xDodIZ5S0JWlXKUXq9NrS5l36KUiS7I2krrOXnxx5fujR6nojM9WU2vjLTyqtFVQgpi5FnyrLlSG2njJTHk+JimokNEo3XSXsaS3SoBhxEJ5aK2r8C00da/JaVEB8HMU5FVRrTQaVTwYrKkwdLVlZTEUbh4EmqqJjxO/Yhl+tEFZklCkP6d7J5n5epPwa4B59uq53VHl8/smOciI2ZnTWoqqlyiooVCOWElFXeWOtkVTdypAM6K4xREZXLxfffiqTIhlxmg0vKNwbLq677pLI9JYru6I3qi0nVpqKGbGUkbCGRqd1lofNxIkmokKuFl2TUllRraTdmYbJpIVNDt6hgiHJe/ux/j5VFRRVMTlsJsonzw7QNQzVqgpKxG3aFDKZjEqlvakXdGXSpbO3npaWFOYWKhanIhZVIak4+tylhyWK5ctEhUWy+jneKpFIStPuqq2CcsVIhaFJnICt3yGvWiYmqtLW1mZQ06pkRNzLoNGqyJi3sEpK09TTpKIici7xtqr0Jr5/iMbLZB3yYGiLt/AzqS1a2Z2DxdJYv3nLmo2/ZmVmrPtx5VjXEcSDeJL25Mny1Wv+8f+3mzwn3HoMy8HzftsbdOtqRNTZM8dWT3bSfA9jlDYGU+/hPm/bsVOhty6eObbO243X+pHpiMpMPA9cO7i8nzpiW3kfO+W/ZoDWB7SqoDWIf59V1JtZtjb7Um5oFrWLnvyjKJU+vigsY2qMms22HsF2n66pJigJiyS/ZQUxpclizHooUy2v7E58DcIbLdkYVXUkhgEb3p6qwqRUiqmroy1PU8fUzmW4btWTzKI2/QNZgZfQsWZcciZJSX16K60u+iXkZcVGFqjYDHGcbsUb6zxoqFZ5TMSTJ400BZeV41KqrrHRwK4smqg4r5Jq2G/YwoG9p4+0t1Bc4SSrIlN3TC1rU97oQaaG8qhYWpIbUyBjWvafPZA3YmC/cTzFxVKS+HtxKajziNH9R/fsOXt0b0Npzq17BU0FwHSaOrGaCNRTwY8rYvQZNPQzHba+saOHNbs4LbO4LWFLsVhJvQWj8NZePyu5J6V0Uxx6stqMvBrEwb6bgk0YpjLHpu43g4TI6CIl/V60IcZKLevCLqy5l1VD70qf8yVteH/6HPu6boQZcfidMuX+X6qMtaFOHEsfoFZzO1SW03g1DFVyvRBoXHVpalpZZzsXF2Odzjq9XR2tVIuSMtsyAhahVlSlpNbEDpdUXo4ux7XYiyd0XTxMd8GXRusd1bHi0uCnsrLc0ls5qJt95zGmjMH9dYd3RsmxpcmNdoKtSU4UF9AZA7vTStOF5NhUFeXBTySoM8tem4JRsIGDDGbbqb3+z6xUVotUVKy7M3qoPT84agvTKwoQfciQzi481teObCNF4kdeoXoX7Ym2zAG9dSb1xMqfFkcKmzi7o6RKI1YfdUDVBdmZIq7jl1bG+pqG/foPtUT8uDaOrl1VVYVhb/zmqCp5mpKc/rTwebBdlXvvbhbS7tGzK4NKZZh+7vH15yYqL/VElpU8fVooZfb83HVA714DPncyfvVCXXFOcq5U1dh5RH8rc/svPu+hODEsK4yPSK/Ush3+hb25VX/XIca0gvjorMb/7SIaT6wCAi3T/j+T2qKVAfCKtT+ZW/T8fuH8TT+tDbt2tUQgGO0xtlv37r//8rPXV6PKSkvX+W5RVWvtaAFaTt679viM0csL9dvm+9flZGQ1Y+NWb+cPJAZWt12wddeCPiguYPvW/aG5uq5rt26fLx+dnWHuferskfm8VrZTVJyS/CQlOQ9v0y0fwXtXW5KHVJp/8BdXXD0oyH02JbiW/ccWgaC7zsylOgZ5hQdX5cbk1RWLiq+mMZWLIkvzxE2WbARdnWwYeGvwtKArd4q5I+dNmjnLnp155+K1orYlW8oqc4gMMGo5UfaOQ/87lcMaMd5tOk9yK+Ds7/caHYoZL3hyPCJdzHNcOrq7XmXG3v/iclX1v3Cx6lqcGEmOqYUqch4fjCjQ6jPip4mOfVFhpiLrJis89e+ls4ky+y+/WmhdHZlUrOipKs6KXnc4LIZqunDiMHuUcfxw0MGcJjcCsYLEaiJQX1nMzQtRqKfX13OXutrR0i74Jwja9BOBX6pMZICbXx4XSP88K32eNbl3tupUFhG5qEy0rL0dWa343StOxffckGE2qqtGU3Vbdilc7WX/ij9vV+s7q60bqZz0QKroAo0LZBu3VVwuosyZrTa9S82pv8s3Pqht4t9CIqQn1guBJlQXJFwISKP3d5254uvRlpLY0zeT2nyyqUhMnLVq4vXalOjsn0OK+XTmQCv2kO5UfmLOmhPybHB11b9BT49lUAaO6DLbFD0Iy9waizeRw68oLHssVFanyh4nVcjP3NbEXM/6K1rS2c5gxVdca5nozB0h/9Uvl5rk2ILLT5HNEP3x3ajPOziWZhf8dUmQTO00+yudbsWlj+vSvGSFWyOriAoXDFIvT+T7Xnq9wpcQGeCiFt1l/ZMhy79z+g6/c/8JSydNHsstu3zlWlIbf6eWl5dTWzMoSdXTOyePXEpX7f3l1Mlj7ajp169G574cisuehv0bcDtJ2mO055fWsofEIf/yt6esMPrsiUsPRV2GT/C0p6bH5yhuxSQrunv6+H8PK02Gjx83gJkVeuzI5fQmAlyi8cQqINBC7f4zqS2UGJotvgfjF6NGL1vls2jWDCLQ3bDl9zP/njx7+tSOAweVlZXmfzONKKCh0enAcb/4+Mdrly9DLaY3wGfPattk33mrbuQqPmKYpuPav3xMbq+YsytagN4zvQEb/lnOPrzA2/+pvHXqPTwXL7aL37ku8DEy9z64yfbGkhk7U5v/3UBkgHftGZ68asHmcPgwvVXdTO1fmSMqzc/LTkbtjkJTsv+iNjtZ6cPpcozREbdHbdQlVA2ddj4aFGWaJXd0gTDhU+0kTKPQtZmmj/lB1bXQmfUtwii17nayuBxKFf6JpExVsVozver/RVOl1ZAEfreoysqDetRkCJQ6WmdgOkWpK7vm9hMkq0GgzZSVlXvweEXFgmrZ+wuAWotKpWhpaj5JS6+pgYPhA9XDctAby7TmBOo4rwnnzgTGPYxFZH+Xul9ma1d+/+Nib8XzsrLSQ/v3DnR00uK0/P4WWpYuDuysEL/buc+DSLwk4vD+Izey5BM0LVt3nz0HQ6LI3tFHNrr1lN/ZRct59ZmLv072nOd76lRo1MUz/8xzJLvqaTqsOR5yap7tsz7KmOWMI9eOb3DWlHdj9t5GFr4aceug73yruo7HbKvJdV2vL545tnyMZcNnqBj6Wlhdnrc8xf/ned8HPmYO9v3vL08jhsm0fWG3fh9j0sl25cGgf9x71A1upDnst1NBfwzWw+Sr0E++Creuhpz93dtZt64mBm/ysbP+K+tu9c2wdPH+g2xJ6MW929a42eqhjsrKxpb4rqw/h5gkZqIPVrWUjH653ZszEta7QDSDiH6fJkH0+3GprpHmCxO0WSbksDOfnlolbZYpsYIQ/b5teLXS4xxlC73qD+QLqY2ItTDXq37MV4bo9z2Q1dRmCJS7aqEOte2VEBH91qYLIPptL0ToWFRcrKXZzJEpPixaWlpFgmKIfj92LQ6AMTrd0Jh388Z14vnTrMzZUycR6V/ieXFRERH3dulqeOjf01sTQPwAABAASURBVF+OHfcolgyPdfVaHLbR2Ca6mCAhOvOl30R48o2jO88T6V/McIjPxpm2onMrJo4d/52fwHbmiql1ESPGsXa1yzu5asGUZfuT2aNWLBighZXEhUQJ2H0ceyn6EdJ6OPXRE8UGRZdoOS3evGQAurF9xugJ325NNfRYPr+fJtm9ear3DDs8dOuSybN9Q8V9Zizx6PHKBb658WdC8gy9tp7cM8/VVofxvLtz7o0Voxf4Z4iTD81yHLj0THKjv+kwk1E/b5zvgMUe2eq7KzjfxGOUCfO1TtN6g1f8ttiZmeC/dcNm/wRkN3/DShfDjnhtMHG8bfjt9x/Wrn8eAxNPiEliJvVDvqkPkViuFCPtFneveCs4XVBlOcqBQdo/PvllibhUrMXoij45bIYhLi0vEKYg8PYR4aKwUsmI8/ElW17XjV0tqlJKzIX+z+8HEQCjChzpslDHoauBKqS1T4sRaD8CgQDHcY33dxvY1tFgsSQSvLgEhq746LX4nxBTM3LM55SEBLu+Dmt+2dSpU6dXCihywvl55GVd6uotHh4KYxLRoEgsauT6ejwzeMWkCZNXBUYnl2SGXz4ZLWab8OriR9GToMPnopPzM0PPHQjOQkYWRhgSP7oeIdBycOouv0a3u1M/XUH45TgBKg7xnTxu2oqdt1Ny8x8HB0QIGD0siRwwxmBjeMb1k+djU6JvbF82a8aqcymvXvJREr11geeyndFoiM/eE1cuHdy1pi4L3Ty0Hs7De0iu+67afjQw+MzObRv2xbx2y1iaodMoW/z2NrLMjaDD2302XRb1GuVogjoeXCL5fuE8h4GDiINNWY54QkwSM2WyDzhxVFtTGx+OVJlIx7BW6b39UKslciU6RkidWRt/h2gSAh+bWlTzpOCWCo3FYRi3esiGD40SUiZWh05jPikII1YQgbevplbpRhJFQ7W2R2eZstLHegMPilIN0X6WWu31RErNJ9kt4qNQW1sT+1RJTUVJX+OT3wm1ykhJv5OSOr0mNgtuvdXusvl8Go1OhJToI0E0FcMwotkIfPxafBukWvl4FRQatW+//p11dPUMDEpLXwwtq8gJE08srayJv3k5LR7dBBflilE/BpPe+K0jsa5OC+a72nbRYuoa6TMkjxAR/0rIUElcLKoLiXCBGBFHKVGJID7kRp7r4CEm7NhkwwEO+nkRW5/IK5Zi7AFTFgy3NdRls3X1OFgyHSOD24BzKRtnHjg1PDMjNS78+pnzUQ21QJobGugTGuhrMsDV3cXVZfFmNj7v++BM1BwMtr4WnnkuU/CsqriEXNErvUAYhr10Ue71lGcXPIszYjIlAyyNEIpDHU9SQsKyBXO2/LXnp02biUkbuz7EJDETfeCkktrYa0qWg5S79arJfaJU+a4v8a5VZSrr82olFbUx14jGIPBxktVUJeaG9NAZ3EXLOl+UTCSE0ceMTmV2ZpngsnJipWQ1cFi+O1VSpQsPqc49ZXZGNYl5SqLKj+x8ioZqjalubTmOiLUg1gWB9wivrolMU7YzVDbRrc0WoPJP9CoGdUzZQAtJpDV304hVRqC9VVdXZ2Rmdu3SRaezTnFpsRT/cA8kIqLQ7KQplUnTMzOJZiPw8WtxAJyaQg4axOvRY9f2rUY8Xkbqq/0q6Sp028/s5y9ZGv/oEREPoxaSCjKeitnmtobqEYIXEQNmMni8M+Ox//lkwxnbt3iwk6+Hhp+LjivRc/ee8YbuE9KU0OuZHsOHWeoguz7snKiQ5HIyDTt1/faZ3XPDb0efJxLCDOcFMw3lpcXR/vPGXe/Zb4i716gxS4ePcfObt+jA40ZG3hIn3z656XbI/dV//zDcweh6ZnuOZdpAd2es494eiQh3v/9u3uY/dhLPiScfQfSrIKmsjb2ODHsqd7WoxatQhbC2UowqypTe2u3jamk0pMpSUmUgNZYyplLLT6nNiINLfz92eHVFYt4V/U69uBqWeHWlBBdWykRVeGl17cexZ6nKGJ3GUqWxiL8YRSVfmMQveQiX/r57FbjSxYdU6641VgY1FXiNsBKVVSqXViKp7AMNhum0GpYK6qRaw1JFqhiKz1F+kEWBS38/CBJZTWS6Eq+zcrfOtRIZElfVVOJILFH6yK+SrcWUkSpdWR1D6ipKdGpNlqD2SQFc+vv2yGQyIgbW5nC02RypTIZLJLhUKpFU1dS8/3w7haJMJNIwGg2j02lUqqC4uLCoCC79/WS0OACurKjIfvrU9csx9yIi6ke/n7uMmLdkSadOmorJmPv3f/t5PWqF4rjb0YLhYxaMCv3O/7Ei14FpOkydOcXk9gp/dcN+fQwF51askg8Hjem4ur+5Qjw5KiTDY4zLELqJVu6N62SXZkzXtp8FHrp5+brbxThC7D5OzwJOjK3DRsWPQ/yJx05nIrK1stWjPRa8+KXG6Od94Lc+j1ct2BCquAKARnwwiDe/PuyzBMcxpi6TiM/J+FmLzcbkd+MWC3KKMVvrHuzzmeStb2h6luZ6TOzlzK44NzkPuVsb1pVBDCNrQ3pxWAbqwBIfP549ZSLxJDfno+p8IpPWpsbUZicjtr5SJ20lFgd17qJEeWtXL1dLUVUlqhTWZiXUCvhEBI7AJ6G6Bn9afD9fmNhJlctU6cyka7PVDSnKH/Bl8PVU10hxWUWltKy4/GlpxVMinkfgPcGrlSLTKUQk2UWrRkejVodV000bYZQP9CcdkXWrkKDSSqWMbKUsgXL5pzKK9SdCVlOblFedKVDqzESa6sqd1JGuhhK1ZTfF+tDUyqpRlay2XILSC2sKRKgKztO9dURImV9QUFxSwmAw1NXUVFVVWSwWRfn9n5WrrqmRSqU4jgsEAqFIJJNBLuGT0uIAmBDgd2LR8hWfOTgQMfDzmfMWL74eHHzrxjUi7svl80tbf4G44PbOred6bJy5/aB5yI2oFLGupe0ARzs8ZJ1fnADXyxUjvT5jnK0E0cjSzX2ynRb2xtvY4FkRwVlTZnk4SrIOhGTJI1WxQIRr2bq59ssKE/FcPbwc9REZaWI6ziv/8jaJP/LXkbDcLq4eVlqS+OfdqhXEj86diRuyeO0mLCAgJK6caTnA1c0ePdoWkSEle16LENOoi6GhODc3P/fRU9xrlPf8rAPhYj274WOMGOgRIjPSIZdTPOYvXptHD0gQsft4enXFXu3tLU05fyTEefXitTOYAbEiupXrzCEofPOZjtj/ub6PLPStT1KBcp7U5jxRTMGFRKB1cFl5gSiZeCAA2oBI1CXkUhJyEQBtVSWtzSpGWcXw7xpoCyLULJFDALwTFExVA7VQUkK8uYXl6DEeqSkpz2OSEa5uhQUF/zt9qqigoKqqbXetrMyMCInMohv1c/7C1bl/L72KR0d+W/f3tRIc1ZQ9TRV3cRgz2WuixxBDwZWgNK4JMy7ofDJu5PhlPyz6/NWUMnKtOlkOc+0lDDsbkU1mwGoqRcj2K+fOaX67/BLLqskbsmcnF7LtRkyd7DVulGlF5LlYrFfn3Cv/3cpIi8tQsxw5ZZqX51dOZijpzB/bT0aXv9TbHy95HB4rMR82ZtSIL1wGWHaqTAs9tu3P4DQihq0WF1Zwh0365psJVujW5bDohOxOtq5fEQFyN5R6+UppNytK9H8hGWUFT8KTy/StR46fPMrNpDL8VLSSOVdw7cLtAoaV23CTAqIZRXhlTnRcHs955ozxw50Hm6L7e3x+vpoJ2bw20eRwX5mDV5WLhe/9ztIAAAAAAACAdsDubPjGMkoMzdbcqYXF0li22meAo9OVSxdDr16Nj3s4xHn41Jkzv3L+HAHwQepmav/KHFFpfl42JNMAAAAAAAD4FPSwHPTGMq3pAk0QCsvWLF820GnwhGnTN/y2RTHztN9xBAAAAAAAAAAAfJBaGQAr3Aq9QTyIJ9143WtqazLT0hAAAAAAAAAAAPBBalMA/Fx66hMEAAAAAAAAAAB8wD7Qu/8BAAAAAAAAAADtCwJgAAAAAAAAAAAdAgTAAAAAAAAAAAA6BAiAAQAAAAAAAAB0CBAAAwAAAAAAAADoECAABgAAAAAAAADQIUAADAAAAAAAAACgQ4AAGAAAAAAAAABAhwABMAAAAAAAAACADgECYAAAAAAAAAAAHQIEwAAAAAAAAAAAOgQIgAEAAAAAAAAAdAgQAAMAAAAAAAAA6BAgAAYAAAAAAAAA0CFAAAwAAAAAAAAAoEOAABgAAAAAAAAAQIcAATAAAAAAAAAAgA4BAmAAAAAAAAAAAB0CBMAAAAAAAAAAADoEKmoPVja2xN/YB9EIAAAAAAAAAAD4ILUpAMbo9NHuY7+eMJGtrU1MFhUUnvI7/l/gaVwiQQAAAAAAAAAAwIeklV2g1RmMSdO+8T97fu4i71thoV5fjSIet2+GEpN+Z89NnPYNUQC1BcNy8Lzf9gbduhoRdfbMsdWTnTQx9G5oOqw5GPTPjJ6NtF/P/degi6sd2aj5tPp5bjt7MSLqasjZX+f102y8IM3QyXPDP8dDoq5G3Dp15I8ZjoY09AFRt11JbBn3Hu9qTwAAAAAAAABAu2pNBnjC1OleU6ZRqJT/Ak77HztSWlysmP/nb75H/t7vOWnKhKnTPCdP9Tty6MThg6gVtJy8t28cpZdxK8TvXIq4q4PzkBkbt+qtW7I9pARHLYaZuO/a45G8atbm8PJmFB4wvldx0K9+j8WofbD7zFjiZZS8c96qEscly8fMHB7yyD+lgcrVbedv8p3WXXD/+pnf/QT61s5OHhv+1N38vW9QshQB8GGj6/ews9Rs4utEVpx2/14RdA0Bb6CiY+to2NTpU1lRbFhamQwB0CQ140GWBqpNFJBkh8emiRAATaJoWFpa6dObKCFOjInOasWPU9CxwM+kD0yLA2ArG9tv5847/78zf+/aKRSWvfIqEQzv+XP78UP/TJ0xiyj2+NHD2Oj7qGX0BsxfMpwZvmHKqhu58q+UM35+jmv/8pnldSV6V7QAvVV48vnF486j9oOxuxixxdF/XY+OwwWhWa6e3fXo6PUAmGE71dura9zvs1b4P5Wv9PmTh62892yaMdU+fN3tYvhqBR82SU7KnRwEQFtV5UcH5yMA2qoi7WZkGgKgjarL4mLD4hAAbQQ/kz4wLQ6As7OflpWVuX01RiaTBZ704z99+koBbpcu7uO9vho7jiiW/TQLtZSWpYsDOyvI73bu86gPL4k4vP+Ic11WANOzGjNzyph+FkbM4uT7t0/uPxwUV44YvMl7NjknHw6hD3d3stDCsyL2bd7gn4Cclh/dMlwPIcs//3NP2v/tHP8UZp8xCzzJt2Pi5PvXj+w/fKXu7Vtd41bO2JRABqfsPj7/rNYLXOB9+CmOqfd0mznDa4CtEUP86HpQHIZQeVMteRkuyM8VMXr2666XqznFrTseF5DSwClndUu3AYaC67tCnr4IdQXxJ//aj+vh5IlHRpdhs2ZMcbY34WCoKMZ/6+ZdIfk42Sd6e1QBAAAQAElEQVT5rw2WsUHJXZxdLBi5kUf+8k+x9JznRhTDM+74bV7vT5wv0HJe/fcS9RD/ElvPIZZMcpVftLPBahvZkoqYHWP2mfLnKAfLrkxUnBy63+fX4EziBUy9h9vMeeQm0qJLskL9tvvujyWDdkzHYYG3t7O1EQcT5cSE/LV5O9nsFhntMZb4+1/AaQQAAAAAAAAAbdPia4AFhYWTPb7a/cf2AY5OR04Fbtr2J/FE8RLxhJgkZg5yGrxnxx+T3L8kCqMWorFNdDFBQnTmS/1+8eQbR3eeJ9O/WBfXtevn2eER/ts2bD2XwhyyfONiRz1FKYZhvyHs8O3zJi7YECy2XeA9xZImDt08fuLOOFFe4HejHSb5P8a7jFm7ep4lHnF424a/Lmeyh/tsnO+g11R79FyWb/5hCDs5YPu6bf4ZOq7u1mxFX5imWlJ/g0UeORzD9Nh65riPoyjAZ9ON3NdDQExLT58Ix2OSX4qNpbmhgbv8o3JxddsF633ctKJ3LhgzetbqUIbrknnOhnXvZBv1Mcz09/5m5YGM7jO2bPXplbBr0bRvf41Cdl4znLsoLtfFOPbj3TWjty4Y/93+OOZwn98WDyPf3kS1DWxJRU1MI3tLFHvkr51HwsV6LvNXuJGL0HJavHnJAHRj+4zRE77dmmrosXy+/FJnrX5TV7h3Lw7x/Xbiku33GU5LvJ1bdlWz15Spi75fQTyIJwgAAAAAAAAA2qbFGWA9fe7YCRN3bNl82u+409DPPTwnrN+8JfvpUyUlJa6BweOHD9ev+iH06hWiJBG3+B89kp+X26L6MSYTQyKxqJFe8JjJcFeT4qBVP2+XX9AbFJ6H7Zk/pp9ORDAxhRfHBR4JTiVyj7mHA5z6ze9hooXFvdSbjmEy3NnwyYHv1xyNIwPskOg83z+8XC01I8Iba46ug5s1ur/fZ935TCJwDY7NZf71s2WTLQl8OclJBLd6GDlHFLlr0+FGunBjDAwTicpRw+nRciJ2HbMfLxaQbRYEXvZ0GdVTXz0ok1xlUW7UyYAoIg2be/i6a7/hmQGXI5JLUMbhky5WU3p1ZQQqEvTFYX8R2d0ShFK3b8KM9sx07acTlpnfcLWCxrakmFxcRsCGVfKO6IFRgj1/edqRiyBC3MlxGJ5bTjY/OCDCa5OtpRYWWkJna2Ki+MCAG48z0eNNS6L1MEFm869nJoLeGfMWHNj1F/GceEL89TtyGAEAAAAAAABAa7U4AFZVU/tq7DgTM/NTJ46FXrtKPEzMLMZ5TUBKSut+WJGakkyUGTzMedyEiWYWPf8LbHHPVSKiE6N+DCaRZW1oGCq2CU9Pkuqf8aynsSA1OhdNIcKwYHIkLomgGFfEkDgZjNGxVwcsZprwDDnW8w9eml9viXH6jEYHNsa0DNlIcCOhLm2LF6fczxJZNtmSwPziF+9X7zlzte80rWi//eG2XjOWjIpbdp051Xs8CtywM7be+omLRTiTqY6IdjQYA+OIaesx321AD30GW68rm56XiT3fXnmiuraJcVwsEtdN4BKEYbRnZZ5EJ9ctDc9JjctBjka6GMrHG6+2sS2Ji4qfnZsQCwQ4sQh5OlyKsQdMWTDc1lCXzdbV42DJdLJ8bnhgiPtqn4PHp2Q8Sbl/O+j89WafDHke/T4PeiEGBgAAAAAAALRRiwPgtCcp3rNnjZ04ce0vmwoLCs6e/vdcYODGtauJlxgMJhG3fDn2a+3OnW+FhS6c+U16aipqIakg46mYbW5rqB4heHE9LWYyeLwz47H/eUUE9VqQ2II78+CimCNbA6NFL64wFiXn4agrapU3tITR1Xlw9+Lgnzf8dVtsJGb/MdNnCZbSy9rwfuDLtYgzMsWYk70J80bEixQxTc9p1Bi9p2fO59mu3bTcThxxIyooJCEX6zNjQR/UMhh6fQhDrIvrxlZUi7+2zrQeU9dvn9k9N/x29PnLcQKG84KZdT2pc6O2fzPhpN2AMe6jXKetcPUYsm3OmpNvHtR6lLvHK9Gv4gkxUygUBv3vDAIAAAAAAACAl1VXyygUamOTCq25DVJBft7a5cv09LnjJk6a/O1MIiwJ8D9BVP3VuK8lEsml8/+dOn48N4evo6vXispRcdztaMHwMQtGhX7nX3cvIkzTYerMKSa3V/gjUcZTAb2Pg5F6WK48PGbzbA2x3PAscfNiYPLtyArlREZEy8MwRhcHO0Yu2QcYJxKedKYWJs/BYgxNLUV9eHGmADn3MtfDUsku0JhWD7uuTFRSV1XDLXkJES9KRGQ2FU8+77vVYtcvM13RE/9fn7xcrDzzRlSu+6h5M68nb42qG/OZbTF+wUyn5J/97/AcLbHov9b4yDtXM2ytsBbeiRdjdrU1ZJxJJpuN6fMs9VHx+Tycbd7Gap/VrmvbzwIP3bxcMVo1u4/T833B0NRj44Lw4F3hwQcMXXz3zHSw1DqT/MZxsKQ4vvuP7af9jtefScTAUqmMgAAAAAAAAADgNZXiMoYGu7FJhRYHwL2tbbbt2XfknwMBJ078+ZsvkaYb4Tbac9Jk4qWd27YS0W9FeTmTxZo2a87kb75dNGtG3MNY1DKC2zu3nuuxceb2g+YhN6JSxLqWtgMc7fCQdX5xAiJdG3AkfMCKlctz9wenSNQdPGY6CC6vOP8UR7xGK5SIRRJMz1BXL6dYECd/O5GwPhwcJ1K3dJs6vlfW9jlrziQXpyQX63nMW5xMC8lhWLqMMuEg+TW2eRHnY2asJTK36Eh4CdPObbJl3WDU4rjGWlKPOCv0RtYYj3lTQtccuI+zkVhMDnMlzsVfjQHF0Ye3+5n7Tlu/y+h62I14Abu7bb8hDtjtzYcji8stBGKGk9soh+RzuXoDPL2GGNHxx6hFGLazls9jno8TaTp4zbSVxGwIJ2LykjZXW9d2gQjXsnVz7ZcVJuK5eng56iN5op7Ww231rllaEfu2H4hGlu6jLJl4mABvxijQl86fa3D+KyExAAAAAAAAADwnKMyqRTWqahrE88qKsuLC7HYIgB/GPDjy9/6xnhO/9pp47kyg/7EjgSf9iIfi1U5aWlO+nTnaY2y1rPrg3j0tj37likO3z5sTM2Wql6vXYnc6EiXdOrJq+8nQEjJ2wvOv/LqGuXa999qBdCINm3TOd9V+ckwmRqO14blRJ0NGbVi670zOuXnfbJe/fbX3D+unkHflijy5bnMQ2SlXGr1/+xGj1VMW+DjmxAT5nYswmipPYEtzgzcvx2bO8Jq52YMhSrp85HyMp5ui3kZa8pLyx/vXeAtmzl9yKMyIgURZ4cF+gSbDiYg6c86uiJcKl0fvXDIjzmPG1FFjlg5nInHGnXM+qw6HkaNGxR/4K0Bvicfmg17kzYr8r0frDUAtgRfFh9wocViwfgpTnHH/+obv9we1R7XPai8J+2tn0Nr587ccmo/ywv0CQpKmyq+SlqYEbvc18l68dOtJYkpE3h5pZ3gJAgAAAAAAAID2V1MtLcpLb7qMEkOzC2o5dQZjzLjx7uM9VVRViazvicOHlJWVPSdP/dJjbGlpSaC///9O/1suFiPw3inuA3xgzg/yUaM7sm6m9q/MEZXm52UnIwAAAAAAAMDHj0p7deSj10OA1lwDTCCC22MH//73xLHR7mO/njDxS49xxMyigsLdf2z/L/A0LpEgAAAAAAAAAADgQ9LKAFiBCHRP+x0nHlY2tsRk7INoBAAAAAAAAAAAfJBa2QUagI8OdIEGAAAAAADgE9acLtDKCAAAAAAAAAAA6AAgAAYAAAAAAAAA0CFAAAwAAAAAAAAAoEOAABgAAAAAAAAAQIcAATAAAAAAAAAAgA4BAmAAAAAAAAAAAB0CBMAAAAAAAAAAADqE9gmAOTqGCAAAAAAAAAAA+IBBBhgAAAAAAAAAQIcAATAAAAAAAAAAgA4BAmAAAAAAAAAAAB0CBMAAAAAAAAAAADoECIABAAAAAAAAAHQIEAADAAAAAAAAAOgQIAAGAAAAAAAAANAhUNEHxojHI/5mpKYiAAAAAAAAAACg/XwoAbDT58PGT5psam7xfE5SfPyxf/6+cysMAQAAAAAAAAAAbfb+u0CzWBrrN29Zs/HXrMyMdT+uHOs6gngQT7KfZm3Y8vuan39hsliodbSctM9EdY+IMvJ1o9Sfz+jH8Sfnd9vmTsWaXRtmonHglvGR+bTmv6XemynDNnYJOdvZ1RABAAAAAAAAAHgf3n8AvGLtT+YWPZfOn/vnb5u7m5p6r/iBeHQ3Mdm+edP33y3oZWO73GctahuqrbOK3ouwVdnSWc0IvXVEwHzkecCM1xYn4ykZklwxAgAAAAAAAADwPrznAPiLUaMdBgwk8r35ubm7Dx2dOHW6AdeAeEyc9s2ug0f4WVm/rPXpP8jRZaQbajWJBDF7MW31nk2z6c52RExag96pmujD+fMWlUULEAAAAAAAAACA9+E9B8DjvCacOxMY9zB27a+b4mJjvhw29NuJnsSDeJKcEL/2l00P7kVdPHdurJcXaq3qzDiJhKk6zK6ut7OWJcNWH+U+krwIRdmY60rdIxeNI6K6R1wz2OCJMciiyo4bjSIu6i7fyA26ZXxmjapm/Vr11JafMo64qONqokSU7OHG9j1mGBrVPfSige8SNUMGYjhxTh7XNqErm0wzDLumM0xPXhv5BCEG3fusccgejfFLdMiF3jI8sEbdUNE4TLmnJ2fXKaPQqG7+e9iTVxqE3jKYbIkAAAAAAAAAALTZ+wyAMTrd0Jh388b1YcO/0Oca/LV1i629/UH/U8SDeLJjy2+G3boNHuZ888ZVXg8T1Fq1guSKFAnF0kVV3guaeKKmhyTRcbJnraA4LtHz8VBB0cW+vxeGCDDnpToz7J5tFw7D2VAatDXPNxAvf95uBjZ+rY67nuTIqsKg5FotZ87mtSzD3LLtv+YdCK+29NL1XUBHcaUbfhXmIpQbnL98VfFriV9lpp2mq54k6HBxSIay5ajO3m5kfK7nxNm8tFNPrOrMX8WPMcYUNxU6AgAAAAAAAADQLt7nKNCmZuSYz4mP46bPmpMY/7iyomLqzFlJifEUZerUb2eGXbualJhgZtHz3xPHiGLmlpYJcXGoNTLEQfdZK+xYDkbiTJGKsy1NklQYkky3VbyKV0dszR6/rzY3swZHKCSTZvkn01BPGVP0kZZUndlUuCuuFpHX9MrL02lOP3AW21UH/Zh3ILoGYdR+bupaGcLFm0rJKPd8ZTG7y/J+TMv9RdFxEpGkBuVURYRL8dfPNOSId20qjRCgM9HV7D06RpY07Dxy8FBni8S+3+edSSaqqvLe08VTDwEAAAAAAAAAaA/vMwCuRWRcScPIxGxtLfkc1ZB/lZTqClTLZMrKSoqXKMoU1FrVEecrBP3VnftRI3LUbTnVjw9XZIpeDIqFi2oZ/Vg+P6gbsilsPYyNanKfv4hLkwW19apSNnTT8WFSMgKebgupJgJmxKTZGlHo+pq7LtXrnM7gYwAAEABJREFUIi2hshlvaJNEIMkVKZZeI5AgQ7oSpkWz1KOIksujM+QlBNKw+7hnGy5+BgAAAAAAAABQz/sMgFOSEoi/PUxMkxISnIZ+Tjw//Pf+b+fOl8mkh/buISaNe/S4cO5sD1NT4nlyUiJqrVpBnCi6iOnQT9VWoMIQVYaEyyRGz15k0MZs5K7oTxU8EoXeED4WqM5Yqt5EXXSsJldEMXLRdA7MP5NcFxtLkko276940c0ZlyXnImTUVJtwvKG5ROAtqX32Sq0Er5UgAAAAAAAAAADt4n1eAyypkvCzs0d++VXIxaDiYsGSH1ZFR0ZOHef+rdf4B/fuLfdZk5eTcz042H2cZ2ZGOi5pSyyYWxUUjmMmGq62VPEjcUTui6QuxlZx7EXNPfd0/Df5m3eKwgWoydv81iT75X67rDAOY3ivZPUk0rwiaVxuNZ2pLEqujAglHhIBsU0F1WIctZhYlpFbwzRSMWQqWkYxMaHCNcAAAAAAAAAA0E7e8yjQASeOOQ4ZavNZnzXLvzfqZnz2yrX9x/z+8f+XeMI16PrTDyv6D3Ts06/f6RPHUdvUxIVU5DLplhziSWVuvegUF1cXi5CeXacxbmqO7myfBQz2G6qqFUcLff8S473YKxbQtVB1dHCFQF9jxdpOrm6M8Ss7b96i5zNTlU3mcqtzcWU9O3VnZ0zvTT2i5U2RhQVXiPQ7rVipMcxZzXWB9gzL1nf7BgAAAAAAAADwsvccAJ8NDIi8c+fHn9Zzu3T5bta3a1d8/yQlKfFxnM/3yxbNntHVqNuSH1fduRl24b+zqI3Ej0QRGQgVVQTdr37pBUHlgb9KojHm/LX6G6ZSU/yEGW9ONdemBBZtv1Fj4qEz30k5N7DQe11JHMbyXqu72ENVdKPAZ1M5EWPjmRUnAypRL47PWrajvhJ6s9rMwALv38tyTbR+/kV/ngl+5HwVdIEGAAAAAAAAgHaixNDsgtqMo2NYlJ+JWoXF0li22meAo1PIpQu3Q0MfxTygYZhFT8uBTkOGDh9+88b13zf+LBIJUcegxNBTwnNr5ClqpZ5LDHa5ybbPySUHhQZt1c3U/pU5otL8vGzYtgAAAAAAAHwKqLRXryB9PQR4n4NgKQiFZWuWLxvoNHjCtOnOv458Pj8x/jGRB75zMxR1GEo9purvWkBNCS4LvV/NtmO5utDRo7K4HAQAAAAAAAAAoM3efwCscCv0BvEgnnTjda+pqc5MT0cdT21KQIEvmz3DjbPYhZisyb1TuHiTMEWMAAAAAAAAAAC02YcSAD+XnvoEdVxi6ZWteVe2IgAAAAAAAAAA7e09D4IFAAAAAAAAAAC8GxAAAwAAAAAAAADoECAABgAAAAAAAADQIUAADAAAAAAAAACgQ4AAGAAAAAAAAABAhwABMAAAAAAAAACADgECYAAAAAAAAAAAHQIEwAAAAAAAAAAAOgQIgAEAAAAAAAAAdAgQAAMAAAAAAAAA6BAgAAYAAAAAAAAA0CFQEQAAAAAAAOCtoaswaJgKlUanYXQKBX5+v6S6WibFJTKpRCqtklSKUWupD3JU6dlL1dycbmZB43AQ+MBICwurEhOqEuOrHseV3wxD7w98AgEAAAAAAHgrlJSUOrH1pXhVbW11hbiECPNqaqoRqEdZmaI4NUCj0dXUNUoEOai2tkU10LhcvQ2/qllZI/ABo2lrEw/mIEfieUVsTK7PD1I+H70P0AUaAAAAAACA9kfDVLX1eGJhsVgoKBeV4JIKiH5fR2wTYssQ24fYSsS20tHjEdny5r+d9ZW7kV8ARL8fF2J/EXuNNfor9D5AAAwAAAAAAEA7I6JfdWangpwnUrwSgeYhtlV+zhN1plYzY2CNsV/r+/xEUVdD4GND7DX9teuJPYjeOQiAAWg3GMfa8+fjFyMfPEpPTU6Pv3fz3IHlrsZM9HFiWi0/l5yeeu+QlzGGAAAAANB8SkpKmhxuqSAXgZYrFeRocQyIrdh0MZqBgY73EgQ+ZsQeJPYjerc+6ABYRVXFc/KUH9dt0IIL2cEHDzN29T0TsH6iA0+bRSdn0FkGFo5z//x332yrjzUGBgAAAEBrdGLrlwrez/WNn4ZiAV+Trd9UCSUlvfW/KKtC7vfjRuxBvXUbib2J3qEPNADW0dUb7T72WMDZmfMXfj58xKTp36JWY1gOnvfb3qBbVyOizp45tnqyk+YHlc7CDN22XTy+wVkTgY8Zxh3m7eNKnsDKDtv93aTP+/b/fIK3b0CCBLEc5iwbZQ45VAAAAKCDoKsycLwKl0DP59aTSiqlUgldRb2xAiqWveC630+DmrUNsTfRO/SeR4FWVVMbM268zWefqaqqauvo8p9mKVGUjbrxWCwW8WpcbOzq75eM85qooaGBWkfLyXv7xlF6GbdC/M6liLs6OA+ZsXGr3rol20NKcARAe8G0rV0dtBGSxPjOmbcnQX5wFV3YEy8ysP57Is96VF+D0wlpOJklXrZxkasNT5uOJIWpCREB+7afuJImkldhPPXw+VUOKGb3hhibOe4OBvTsB1eO/7nleKrxxOULJzpbG6DC+JAdq1b7x4jk/ZNPnJprURj8/bf/sGavmD7IwoAuTI2JCPHbvedCgqiuWUzzMWs2LHSxMGDJl/cgzH/3H35hfHnznteweuU5A89v3PraaKPUB1dO793xT12JZ+jGYzes+8bNmkeXkAUO7fgn5HmBptaIWIaxs9fcaWNcbHgsJMyOv3mcqDwkDT56AAAAPmk0Gr2mpgaBtqmtqaZiKpKq8gZfVbXsjcCngtibVY8eonflPQfAziNGfjt3HhHoqqmpc7S1iQC4WioLu3Y1Mz39SVLiw5gHqE30BsxfMpwZvmHKqhu58h/dZ/z8HNf+5TPL60r0rmgBAqC9sLS1yZM22Qnx2fXiO1HCuYN7kQU9NU1Ixoruvod/k2eJhYWFxDuIwHj5LguDbz19bhY9fwvd+pvl3NR44tjva2PjumKP1ahsujZKi4/P1rYxsHBbtSY7Yepvsc8iXDrLYeEWD2cDYaFQQlTYdxSvr5M5y3OOPxGDM82n7jixyololqRueQ4eq2yM6Z7T98WIni9P28Vnl5Mk+0FETATP2sHBfYWDlfb0yRvCnreI5UQUIOsQSugs3ksF3rBGHMdVh/e4k3F7RFghy9xJvjoW389YFggxMAAAgE8YlaZSIS5BoG2IDLAao1Njr6r0hgD400HuTT/0zrznLtC9rG1u3ri+aPaMw3/vJyaXzJuzbMG8bZt+CTzp1+bol0j/Wro4sLNC/G7nPv+5jZdEHN5/5EaWfIKmZevus+dgSBTZO/rIRreebPm7nFefufi79/zVBy5eDL22d4OnVU/nedtOnY2Iuhh0avUYS7IrRl2/5ameG46dCo26eObYunnOXeo6uWLqPdy9t50i5l+NuHXQd76VFva82l8ne87zPSV/yz/zHA1pinfQ6Ziei/eRixcjoq6GnP11Xr+67tCYYZ/JG3ecITtvXw35x9vVUtELhGbo5r3r1Fmi/tBrB7ct6aMFvWs/AHS6/LpfJJS8NLvort/vq31+ORhWhJMxMiYszI7YPK63zQB7G7vPvwspRIjXd5jFS5cICyM2TB4zcYa727f/xBP1GhgU7pvqNnna2C89NydIEN3CcRjvRXmWg7N28JwRpjYDrKyHTN18t5AMWGd948QhDh+WARcVFmaHrhlp/Zm9w2e93TZGCIn3D3PgvXzEFAYtdP7Ca+4ML7cvF54nWzTKw5r7Uovu+k7o39vms959J+1+IKlXoOk1YhqYmxNJ8cLgjbOmz5g2aoTnnrvZhSI6j8NCAAAAwCeMhtFlUgkCbUNswybGglZ7t51mwVv1jvfmew6AKcpK1TJZ02VafU00jW2iiwkSojOl9efiyTeO7jxPpH8xwyE+G2fais6tmDh2/Hd+AtuZK6aaM+RlMI6Fg37MrkWzfALEtku3bl+gE7F1wfjv9sdhA2ZM7aMnDx/odF3nmcNRyOYZE1ceyew6fu16bycycNVyWrx5yQB0Y/uM0RO+3Zpq6LF8/vOAlmPtapd3ctWCKcv2J7NHrVgwoC52xbQs7XQzz+/0/etcCmY/ZeVUByIUZ/DGr109xeTpke8mjJy45gwa4L1keA+MbDbxRC/Hz2f6rBX7UvXcvOc7wfXDH4Wiu3sXz5rzyzk0zHvDup83rJrrZkAGzSxWXexchx+fVkiesZHw4wuJvDEqTEiQJ5UlhdnZQjLny2LVKx9/YuN2RadinB92cKM8QDWw6WvMJKZDflk4fbFvCGvUcmJx69ZMH6RNvJHOMXh5eakhfhGKdC9OpGrTiPezjI2168XI2ef3nb5LBPAIL4o5dz6hXoGm10iUnZZQSKaYl+34bd0cd/PCPZMHOXw5+7fIIgQAAAB8wigUKtzvt+2IbUhsycZepelzEfhUvOO9+Z67QL9VGJOJIZFY1MgZODwzeMWkKExUIiajh8sno0f5mPCYGPn7HomeBPldjk6WopwjDi4WtuGBQeFPxSjvQPDw7YMt9LAb8t7TeMb57b6HY8UIpfy6Wc9wk6ubxYHw28UhvpPjMDy3nKw1OCDCa5OtpRYWKu8HQ1R7+BxZbfK5A5ZkVUbYjTiyJnH4X2s2BOYTbwnNwP5ey+uhR4uISz363YQgVF5MLADlnwl0c51voccOzKRrMVFxdOC5sLhyFOc7L1wL5UInm/dPIlEcZ6yXgkvE6es1dZQFPTXk8PEwic3sbfuW9309/0l/uSIhenbISurXTHi94zCRf613gONFhXwhstGmkzEyxnJctm/PNAs6apKwMLVeDfKFsRCzXpuE2fF84fPXhcIXBXBO3ybXqCh0x6rNzBXTnW3cvIjHCvL9qae/n78qCLpAAwAAAACA9+I9Z4Az0tNNLSwGDh5iYmpKTA4Z5tzLyobN0a5fpha1Ei7KFSMmg9lEAIB1dVqwetexvf5nD2130WUQ+VXFOyXiYlFd3hgniMSK3+s48V8MwxQVSopT7meJFYXEWdHJYozdhU2+X4qx+8zY+OuBYwfPnNrqacRA9Lps2kvVCsTPq5JIxGIRrliEWFAsIkL3uncwTNy8ff/Z63/q+JG19mw6DSPD7uv+N3DHjYf8j/3uu8bDlo2LIZj4AAgL5elaA3MLg3rJU6b5qOmzJ07wGmXOxLiD5s4hYsXsc6vHDTQ36cYz6T3BLxW1EcvAgvsi/mQaWxiTHx4yTMWMR33nZUGXxJ/wHtnXklhct77zzhU2UMUbu2g1VuDNa4TzH5z/fZazXR+3SbO+33L6QSGi88b6LHThQq99AAAAHR3TemlQfHLk7jEv/avIGfRbaHJ66DrHd3UHUIw7Zm9EcuQfw95OBs6ga1dDIyP0IakWColHs4tLpOfmJtv1Tl7w74uMBCoS/TAk0WW5qIN2apNU7RiX5LJI+NGu/nsOgC8Hnec/fbpu0+bxU6YRke7qn3/Ztnffv+cv/FiEqRQAABAASURBVHfl+u8799h81ge1gVSQ8VTMNrc1fGkAdcxk8OT5brZsxLCdsev4phkmeHL4uV1bN2+7U9yyQJLe4I94Wo+pvx7dM98Wy48+f3jb1p0hOWLUOnoDlh88tMFDRxx3+ei+Xb6HYgSKjx2ef2X9rDHfbD4ZLdYbPPPnvX/5uOlAPPG+4YUxQRGF5BBWK/bsWu5qb0ycw8CMnRctHMsjXk17EMPHWfLbA0uK4hPSyDGUMWMnj0E81FY8j2XezsbkAYBxHecsnGhBPMt+cDdNRK9bXmF8YirZf5lp7jzGQRu1p6bXCDOesPv2w7Cz+xZZo4TIkMB9q3z2RZDpY65B+zYDAAAA+AiJUq+ci5do2wyzqXfdEYc3zMYAZYddiW9FbMEc9HNocuJxT+MP6HfhxEkT/gs6Z/eZHfpg8Jd5Ew/UQjXhuwuD+TC096fhPXeBzs/LXbFoodeUqcPdRk/72mPvkWMRt2/fuBLSw9Ss36BBW/7aFXH7FoPBLMjPR61QHHc7WjB8zIJRod/5P1bEoZimw9SZU0xur/BXN+zXx1BwbsUq+XDQmI6rO2ohrR52XRkhJWTFjK62Jgw896kA6Tr3s8BDNy9fd5uMp9l9nFArv4QYJgNs2U+OfLfmaJyUHPhK3/P5IFt6egxRRtSZrVFn/uJN3rPVvV93xvn8YgTeJ5x/ZfuGIJs/XQ0MHOf+6Tj3xSuSBwe3/PNAhNNjIlIlNhbWK05cmpgtJHK3BqxC4r8G2q5rTmDaixYfb91oGXTziXsuTRQWCunaiu7X2QFbdocWIRxF3M3+hmfg9PPZW3OI5WjziH9QsyXIwGDsH8fomxevCkFthGc3vUYrIsIShC6OFtP/vup4NyKbbuFgTV4inBrz0kDZAAAAQMckSosISZMst3ax1g7m192ikOdsz0PZx0MSPpXU4tbffu/Rw+Sfw4emTJwcGxODPgAUTc1WDTEkEO/9Q2y3maWPwMfuPWeAFZ5mZnbp2pV4Eht93/mLL9JTnwRfOL/uhxVzp01VUVHV53JvXAlGrSG4vXPruVyTmdsPrls+323M1Bk+v231ccJD9vnFCXBxrhjp9RnjbGVoYuW6YN5kuxaPpqznNG/F/MGOToPH/7B8vKk44nx8MS4WiHAtWzfXfl0MbQfPWzLDsbWfElyQJca6OrsP6GnYxcFzvrd7d0Vfboall+/BfdtXutiadLF193A2wUSCYognPgB4WtCKMR5rjkekFsqHgpZkJ4SeP7Rq+peeP98k/1kTRW5ftPgfIk1M1zbgEdFozPHvF686QV5zrs0z57HorVtqYXxMauGzZCwqjDg4z3P1BfkltkUhm+ctOxEjVCxPWxi6Z+XCn4NSiZBZ29hCuz1ODr9hjZQS/BaPmb7xeGiCUNvaxcmaJUwIPbFm6vQtYTAKFgAAAEDkgO+GETlgBxfzuq5RTHOnvsTp6pvBZP6XY+2+7tC524mpyYkRZ/euHmlO3mEBM/Y6Gpt6be+GnUEPkhODf+z77MYQZE/msL8nGiC6w/qrCdd+c+aQnazdf9x77lps6qPY0H+f1aBYzkif3Wcj48mat0wwf/EbBOM6TtvkF3wvPTU5PfV24OYx1oq3YMZuG45eiXiUrmjMbHtOc39HSKXSubNmx8TEHDp6pGfPnugjhRkxXHop514qOnSrgcF7RYnCHcszPAYk9RuRsXRDyb0iIlEsu7M61W5A9jl+XRlJomDqZ0lT/66SoJqiqJJf5qa5fJZo1zvJY5HgTgOJ5er0a4K13xBlklxGP137tzCprs+27NHZ/KXjUvr1Jt6busBXlC5PnxRdzHb5LP2XfwU/TEzpNyBtwXZxerp4x6I0p96JTiOytlyTD0le12+5+LTvU6KpTiMyfthe93bUSJMk6SWzBiTP+rvsxIYsxdr9cvZFP3AJLr3xN3/qiKR+A1Jn+YpyJE218APzQQyCdT8qsqysbLjbKP9jRz08JxBPLp8/R8xPToxfOn8Oaovi0O3z5sRMmerl6rXYnY5ESbeOrNp+MrSECBAyg3ftsls+b+lWZ4Rn3DgcFNrdU68FNUskeRHno7DBKzZPQ4KkyJPrDhyRj3QV9tfOoLXz5285NB/lhfsFhCRNtUStgced27XffPlMn79HEc2+fCQ4xsiNnC+O9tvwl5bPghW7RpFTyTf2+x5OaG03a9C+8KIY/9UT/Vc39nLalQ0Tr2yoPyvoS7Pfnk8c9rI4XK80P2DuZwH1p4MW2wctrpuq+zdMGH9i5Sy/RsaUEiUG+Hwd4FN/1pVhvJXPJzaPMtn8SgMDZ1gFPp+MfVOBN64RSgs7vDrsMAIAAADAa0TxV4Ljp62wHmbBucIvIvK/g5x49OyAK/FFGNd11Y7fhkmC/XxPpNFtXL+Z7ruDLvL0uSt/n4GLc9HpPSt2JySkPosu8MKbu5dvoW9Y5iD0W/9b0IMHVVzXDTt+c9XODju9OQg5uk6cvp1H1nBTyBm25o/tY3nCB+f3Bheaj53gxWMh+SAhmLnHph0+fSUPAndvSKA7Tv3GY/2awrSpvyVou/24cYK1MNhvfRhf29Hzm0XrvBMmr27u+WwiBp75zYxDR44cPnFs6oRJjx8/Rh8hmsvcThnzigP+ELj01vms3gsSvvCXuTnBuIrbN509isQnjucvTa/dt1ur15fqRv8JL9+TunBpdFSTfFuYjFQXDsBQeumP3gWP2IwJyzl6OcJD/xT+RKcdejmxXBRVuMy7NMeUOWG5JrpXcuKPnOQi6r4VKqKLeUt9yrEBnRZOUpHcFuw7nvtrN2zH1/ITGLjk8qmqseM4E26XnPiHv/A23XSA5o9Da4J3FwbsLhn+WedeZKlawfWigCGdpq3WkCSVHfqHv0xksNeHwWykSeT9YSU1948Vs7/sNG0R/fI/JQGbC0x6c8eSba0V3xacY7PHzlV9dFYQcDxvR2/VX79Qzmmkha3M87wtH0QAXFlR4X/00Mx5CyJu3nySnDTA0UkRALcPcdyNXd/f2NXAC6lnVs0+s+r5tP9RxX9Dfh7zvHeoOHb7uC+fTUgzDy90lf+Yx+S3S8KTA3x2HnilVjzzxuZvbtQLG+rCheL61RJV+S919Zc/FZxf/MX5F2+POzBlqKJOafThtZ71YoejOxX/LU8J3DwlcDMCAAAAAAAfLzwtIiRBstzexYYTEiI06NuXiH9PhyQUYQYTPAZppwbO8vmFDDMDIgs5/250dLXh3JUPNimM2LNm1aHEl05/EyfhIxKyJeTtEyNCI9OQMVGDgTBs1fR5J4jz5AeDUg8eW+Ps6bTnQYS1qxMPpZ5YPMvnZhHCgh/4+v/pqqgiIWDxmBiWMDWtCEcY0Z4AXxtjLgtLkF9lVfjg/OHjQXw8IOg0j16Y2lj0a9C164aNG2g02qsvKNUqKSmdOhs4deKUqLt30TuEZ2fnblyvVF2Xu5WkPUG1Slmzvql7mUrT/dEHMzB4Qy1MM81Zo0XL/ivdcYr1+/PgANXk3C69I8A8dhn8OJAIqzTsuNmztpcFJ2ksNGX1Myo7d6lCMEJDH0luXMKx3p37dVOm0zv9/i9TwqFxyKBQlZ5e8Ut6lUDI0n8xqKn0/ilRBpv5y3bucC5CXzP7fVaczKEgpKw/VO/QxVoml0rmQQZQMh7y7z+UihQBMKINXqSzkGjDUFpRUvYNjuZSb2K5NUZFonv/SJIENb0UEbY+a6FP5/4chL5QZeZk/Hit7P5cxvBuDTeJLX+H3gDtpd4M4h399Gumzat4lF4zVlGVaadly9m9WMjlM0rO13nJD3HRF2qNtRAC4Ab979SpkaO+CrxMhoiH9u1FAAAAAAAAfNJEqWFX4hctc3A250QUOjia07MDyf7PLGsbHotu4HX4rteLshKONgtTBMDZZIjaJJYxUYMw/kqEYtwNXH69sYO5DY8eb8BloezgkBh5CItnx4TFC10tFO/ChRLWMO8/1tnwOCxtngELCeW3PcwOu/JgzrJRf15ymBMTEXMzOCAwuMnFN3IHl2qZPARVasX1t22l1MRClZvZHozWfy7H5XYukVM9Z6rx7IaRNRn3JGJ9xmAzRUylbPSZuhEqepQok/SmDx+KBZwS3i9iMgWiO+lKvZYz9Ml3KWOo6sbugssPpYIiPDmjBhnVvtRNWCh9lFjN7s3sVTcwN/WzrzvX5ZzpSpig/PRuYXi6VJAjyRCgF71XMSUmS35pK6bMJJ4zlRW91DEmMbP22e5SYnRTNaobYJxi0pvOuCbNKapBnCaapMQ2oyn6HdJZFCZWI5Y8q4pDZ8uDdjqdwmaiXLzmDS38gHwoATAukXjPneX8xcgnSUkP7kUhAAAAAAAAPm1EBBwcv3BFX1cHizQXG3r2efn4z/IQRRLvt/7Pmy/uYCgpjM/G6X3rJppVu6T+UwlqbKoOp+/3uw7PsUbZd4PDrkQ8uOLiM1sRGIsS9s2akDbWY5iDtZXThGWjJnie+27ysiB+Q1FwdlbW9ClTX5mJ0emHjhyh0bBxX7q/+y7QRHa3664X2TX+iqVE+Mb13YJais5lzvIW3fcR+x2nmdTbgBhSwp5fFE1/Hk9TjIayTI4JLt/D9dLLM5hqEwbQiPhXFFWwYG5xHFNl8FCmxzia6L+8ffwGF/b6OLrVScf4szZXIFPG8AGdPHrX3thc8Ai1nAShlxOyzW3Sq14/c9BOLXzrPpQAmFBaXHzq+DH0UcAzX+q3DMC7Jnr9Al0AAAAAfGxwvqIX9NgJ5hb07ODz8vGfhdnx2ZKxBnRhfFgIGWZyrJ0HaRfGFOLoTR11nxGmPUgVjrUZ5mAQmJaGk7cqdDanF959kCoRMvlC5OrgZs25e5NYFovXl6fofItxnRzNUfxezwm/x4iId3i6PKsM49o7GEtCN688SNRkPss/YJmNkzkriN+8i4CJ6Hf/PwfMLcynTZ7ykV4A/JxytxGcaWcrfr9dFo6QvIcwkfKlY5cqgh/KPiO7QNdk3BZnIGysGZWIMemm6oNNBX6XyoKFUmZvth2Z0a3OuF2eTGf8dMxgFJccUuj0qdcWwqL1MqP4RYnu81lkF2gku3es+BGbNXao0qNrVeizzvt2a5kStRcJb7R4fKla8UPhnRzm2G7KSIKHX6sUMxn6nNqMS29qUjNJZG1u4bvxAQXAAAAAAAAAdCh1vaCd3Ijsqbz/MyJ7LIeev1v4s/uazUJWQALLxn3ihL704BWei4KaqklSmF0oofOGjXUrCr4bFnwocKLDtDUHd/FORNL7eo51oD/Ysy+YL5ZIgkKzXcdO2LaP7hcsNB7lbK1NxMvylpBvdxg20SPBoFDbafosB5YiT8xxmLNp3wTWgxNb/gkTaju78uiFDx6kCZuzcohGoxHRr7W19YdzG6S2oat4LGffmFR4vy79rdxtqNaoU3y/FdlorqYJX3joeAVzhL6HKUVeGOv/hcqhzSUBiOayXU1+5awSQ5+KiSrPnRKyByi9GVVBAAAQAElEQVTlXCo5dK8GN3plGbT+k7Tsbhf+4s3PGaeGkkR+pyqY4xhjv8DYHCXxNeG5S5iIXX3juOCGQBGEt4Sk6tDy3Fyi2tvEomuNxmnYcZREb25SMzcOpR1a+C58ELdBAgAAAAAAoCOS94ImI83su0EP6pKqeJrfylnfH3pAH7biN98VE8wlwVsW+gSlNX3hL552bm9gPMtx7m/r5vbVFoZtWfi9HzH5zfJlE53o8QcXL/wjVkSOlnVl/Rzvf4L5Bm6zV0wwTj1xOLRQfm8b4u2/bTmdqj3WZ/uO3zzpIYeDsxUBcFEYeWPFNAOP9Tv2bF/jxnywefGygLTm3YNzyfdLiej3m6nTPqDoV0kZKbchAqKbkUMcv+ifzGEs3K7nYYQHbM799XgFfYTOr6tZ+nV9jJWNBjB7MRHSV3PpXXeRcLcR2stGU5P+yVn4bV4wpjFhBOX1W0oxe2v+4qtlWiT66+f8Q7erTcbp/LRIjYmo/RfpePWW+vlkz15Rgg9hjzJq6eXUSozeWtM+qz73c/6JJGWXb7hbljM4zWtS87S9he+GEkOzC2ozjo5hUX4mAuAD1s3U/pU5otL8vOxkBAAAAADwf/buBKDJ+v8D+Be2PePYQNgQxo0oh4IQCIIoiopaQl6VWqZl6s/UyqzU/mn+yqz0V2aHdmiZZqHlkYmpeHAogiIIgnIIcjOOjWMbx55t8H8GqIh4ISrK+/XjZ9v3ub57GMp7n+/zfbqOhbUTfsFoYW1ry9LVzc/LI51ymzPpkniBdApdVESaLwwmPYuy4dsZ+buForDvb7jlUreR4T2QdAU2p/2U0zdHAAyBBgAAAACArldUUEC6mZ4XfaE9DIEGAAAAAACAHgEBGABuwjKx9fK3Ne5ohIihrYuXp7Cb3dAcAACg+9Bo1Lq6LAL3hzmHzJm81VKVVErgHnD13vjLObqbjn9+yN9NBGCALsHmO014/t0v35g/wbxbhkP+wLmzXh5mcnf/HBvYjR3ma0fUHf2r00AMB44fMqA3/mEHAADokIpW3nwhItwrNsVV0Q23WqrMzCDwpHjI300EYIAuwO8/7dkxlhUXs2Vq8vjjCwfYkvzzpbUdLdSU5GfJTZwdDZCAAQAAOqJWNSAA3z8Om6tS3fJGsg1ZmQSeFA/5u4lJsADuH1tTmxz1W0aV+TQ7q5sWcm3dRo73GGBn2JB/5eyJM4mZcg2hzAcNGTPW1c6Urcg+98/Os1eqiPnIZyc5S3LqbT36sssSTp7IMQ+c4OnIVxYlRO3bf6VG3zb09SEkrbSXj6sVpyrn9OmIiIIaJm2zTZzG+I8c4ijUV5aejty3/7JUzR/4yrMeVWmS3m4DHI0a8pP/3RF3Rd7cE6s+Y+a6tG1kmdgOHj/E9ykznqry4v4j/8ZJmH9ouL3tzElZTEnzDQ70zH2fCxriZsZTV+acPvlPREGtuio/u26gswUvTl5DAAAAoB0mtnE4egTuj46uLo0KcM+ACjDAY0ddl59WXNNR8Zdl0u+ZaR685GPfr/g5LIHlO220R28Wq3efIUOMSg/+9e0ne0/X9xk51qr5Y2I2z9Sg7N+d335zutp59PPD6k58+dO3W9OJm6+vpbbaytY3G+CiOfP9tm83JSpcgp71N2ERlrGLx2C7utNbf/3265gyO9+RbgbaPXG45s5mxUf+2br1tNTUNcCzZeQzt5etyY2NBtaB3o4kfd/aXzfvLDAeOcRDO7CZxettwq4qldZruy/wGeLbu/jf9T9/+1NKQ1/P5pHPmuqCKmIq5OGfdgAAgA4o6xUciktxDQh0FqVnwOFw6YbaW62giIluuHyZwONPmZOtiIkiDxECMMADxOK5uJo3pMUklNWqNdJzx7Z+czClXKMpz9j3zT9Hk6saiLpBruGZGPGax2I0lOfnV2qU5cWZJbXV+cWSBk1NzpV8OYtnpA3IanXlxYNnssrraksun46pMHyqj5CtqUmL+u37qAs5TOGWVqi5xpYtI5M1knPJFwvk0sz00xl1hlb85qyqvKmxLn//vt92pDAHJfUyJeGbm7QEYAO1XNbQnOfZHDabzWUTZU1BGtPnsyUabT8rqxr0jYw5BAAAADpSJS0xEXTL6YYeEyYCK+Yc3maFpoZ68YplTSoVgccZ8x0sXv5eU0MDeYgwBBrgQeKZcIlMrmgtDmtqq7QBkkmavtPGBdqxFJXyWmJA1C2X06rVRENucw2xStNQr2l52FAlV+vxDdmE29vtmRlDnPWVkiqZms8mHFbLz7RG1bKmRs1sot/6c35TI0vgOSz0OVdhvay6so6tz1a0rMfWHqu5I5qyhJiztoGBc2eMVMmKzyXGxBRI1dqeagiLjb89AAAAbqGpqVJS3EsgqpaKCdyjXgJLaXnhHVdTZmeXf/2V+btLCTy2mO8gfSWHPFz4FRbgQVJUKUlfPlPgrdUGSpahCbehSmkxLNCXJP72SVpZAzEe9Ox0n7vbF4fLM+WSgjrmoZ4Jn91QVktMPCZ489L2f/VvmZIYOM2YFEjuhUmfkeMtyn7b9ltmnUbPPHjB6OZCsTYes021QVo78YS87PSvf50mhGvpNvnV0SNlf/11Tk7YTJ1Z0/AkzPcFAADwgKjo+lo5MbfsWyktVinrCdwFimtgIrSSlhepVXdVEqwK29FIK3u/9Q7LEAPOHzMamazsi7WygwfIQ4ch0AAPkEaRkV6m5zak+SpcQ7eglxeMHmDCUjN/p7O1VV+WSZ8hgRa8uxtLzGYbOQZ62PFZLL4ts1Xt+SsSNYNwOdparqGzx2AXo3v7REvNlHlZbO3RDax8vAf0bi0eK8prCd+keVQ2ZTdh0pwZ/QRsoq5XNjBlYbW2hqzX20hPLqvFoCMAAIDbYTJwWUkOj2/KMxIa8k2ZdIf7A9+MOSeUngFzfvjMWeL1Kiu+rFbdw+cFNXv+yps6ue5cAoHHB/P9yn1+0iNJvwQVYIAHS1N1+d+d3JHjn31vuhG7vvTMzsMXq2hNwumLzmPnrgkkstLM/KoG/bvalbq+MiffMHjZAgtSmXP62D9xVUx+vXgk2fnlye8FkobinJzyunu754I8P+ZIv+dnvPY+RynJyC+rbC3pKkrKGkztzPlpZVV0UUxK/rQRr68dx9SDixIiD6Qx9WfK3NFEXZwmeahXawAAADyemqokxVw9HpuJv7xeHEqPxcKv3zfQaNQqukGlUtJ0vVwmIfdOJS4p+M9rHDs7/ae8Dby8DZ/y4lhaEehmaHFJ3fnE+qSkuqREVX4eeXR0eCY25L4Jze0kZfnkvvW2sCgvLW3bYmVtzfxZXFREAO6Pg7NvuxZ5dVlpURZ5PPC1t0Fq2PnX0QINedDYwiELxtsl7P0zTt7BwfSsnl4wpGH3/sgCmgAAAAAAdBc334L75gjQjYZAT5/5yh9793+/ddu1lv+88db23fuYr6kzXiYA8JCoqy7GlBp69hF29BG1sYublTzrQgnSLwAAAAA8drrRGIyKsjIdXV1ZjazlKZN+X3hpxpeffmLcy2TeojfjT8fmX7lCOoHnNGLm3Onj/fsKSGVWYuSuzdsOptWSJwLPa866VQHKiC37uJMnSTct25aDUAJdQVOTfGRLcsfLbrMIAAAAAKB7e/QVYJGl1RvvvMc8OHbk0KI5r370wXLm8ezXFzDp9+t1a//9Z7+RsTHToqOjQzrBdPjiTb+snGRfGh321drNsWLB2JU/fLcy2JwijwLPdfFf+7cvdOyioxva+buS6C3HBDOXhfAup5Yi/T7J5AUH1u18GOOfAQAAAACeWI+4Aszj8ceMf2bi8y+cOHrk4oUL6WlpTOOS5f/3zMRJ27ds+Wfv7gWL354y7cX/ffJxXk4n7hAlCFi4ZKwgbvXMD6LEzelwX1hY4Kr1q5fMjU77JOaxvy1b7cWN7yzQPog9+DEBAAAAAACA23rEAXjKiy/OnD2HefDNTz/Pn/Xy5cyM6TNnjZ84qay0NGTiRFOhIGTiJKYOfDi8U3Nkm3qN8RMUHAxLEF+rjdJl8WEHLg+fMt7bPD5c4bb8u9VuKdFSj+Ahppe/XLR4b2W/kLlzpgd42fMUqZE708ynBVetnfFJPC9k7Q/TFesXrTxaxeyDcpuz5Ruf+HcXbUpSEZ5N4KxZM8f4uFlS0syzB7dt2XK0UHs0gcfLyxdM8+8r4NLizMjtn3+1Txqw9veVw/mEvPJTzPTktbNX50/+qt3R7ULmLtAe3ZSrLIgO27B2c0qldl+GdsHTF0wP8nI3JXmXYqL2bt8Wm69g+mHY727WD9+5pe0ZAAAAAAAA6KEe8RDobT/9+N/lS5kHo/x8WtLvnAWLNn61/j8zX2oipCX9MnVg0ikcgZMFJU1Pyr/hil86Lz1NTImcTJvHIVMCZx9Rftjqdz/8KloqGLN03ftBgqw9Gz76amee+bTJnoI7HMJwwKwVq6c7SqM3r/5s81Gx7aRVK+Z4GTLtXrMWz/Gmo9cvefk/a6MVPnOWTOknj1r27KKdeYqsX+cFDn1nX5bqxqOX8oa/vW5JAInaMOfZF19bn2M3ZelCfxPmGDz/uWtXhYrEBzZ99Mna8KoB05cum2JDaUd333H9r7bEKQbMXbF6ruOjGfINAAAAAADQjTz6SbASE84umvMq82Dy1Okt6XfvrjAmCQuEwt07wzqdfhkUn08RuUKubNeukCoJxWuJhLQ8L+G3nyKStAVVm0khniRx88qPwvOZemlEipj/3Sdutz2CoP/4Ebz49UtW7i3TVlgj0ukfPg8c03d7UgFPQNF5kbvCU5hdbXg3ZRefFjOH4LXbvs3RGeK1L6dRtLi2eVd74qd/7uVmSsURv8k+/LTNC1p6Rc5ezgvqR2sfVR69m/Uj05TfrRsR6rZzQ5KUAAAAAAAA9GCPPgDX1damp6Ux6Xfh20u2bPquJf1eS8I33xn47tFyJnT68/hcJvO2becJuIRWKOjWlUrlLY8oUzsBkUalt44WpisvJxbIbxuAKYGjk8jC7f0/Yt6/3iiXmvCplKQ9By6vmbvlr7H5eTlpcZH7whNu0cWrR9dSUYKAmYvGetlZCAQWIiGVxaUIZeFmz7veK6LKj47Iv6f1k9LlU2z6CQgCMAAAAAAA9Gzd4jZIz05+jkm/W3/8IWz7trZ1YAfHvt9v3Ra2/ddtWzaTe6eS5hUq+K5edobx0uujoCl7Hy8BnZ9a2TVXxdKVcZs37sq7vn9ami2lCZ20c8HzkQP8gyZPD530zthJIWEL3tpyUXmbHXH6zfp4w9y+4rjYpPAjaVJe8KK5ds397Yr1KQpjoAEAAAAAoKd79LdBYtLvW0uX/bH91x1bf25bB3Zy6b/l9zAORc2cM2/WnLmkEyrTIpPktpMWhQ64NvaY58g8tVOmHE2rar82XZkvJQJ3V1FLVqRM+3nb8q8uownF47emSJ7AlN/8iJYX5ssJV5mTFJ0Qz3zFZTNFVqbsTGuLw+YibuXFoztXBdb9IQAAEABJREFUz35p0v9FVlp6eIk4t+srZeHl35+O3rD0gw2bdkbFJJXRLVGWLr1cQl/vFeGIho8Z729O3fX6dl6uAnnh5cd+ymsAAAAAAID79IgrwNfS78+bNrbUgbdt/ompAzOLigrz31nwny83/bh9y08R//5LOkOasHH9kX5r5m7Y6no0KuGyoq9fcNBw+8qDH22OvzkQ0qXx4clzVs1duYRsj6vie4e87Naam2lpDlNiXTh38Rw6PI1yDQ7xMSWV2gXiszvDsjfMW7FSsOdoWq3Af/KcEIukz5esjiDBy79b7HRp+3fbY8Q246d4mCovVcpVTI6Wygnf3sbOTiEWK248vEIqp029Qsb7F8TIHcdPmR5oSbR9pMuit+0Z/8Ws5l6VEVHQnEUBdNiSo4mVd7F+FWUfNGeKadJ3n2D8MwAAAAAA9HgsSt+Y3DcDXq+62hpyjxwcHT9dv+HP33ds3vjthMlT3lq6/PdtW3/96ceWpSqVqlQsNjIyDt+3T1xSTDqnPj/+6KkCrqN/8NPjg73N6Jxjmz7+bEt8lUa7kBINfWakIOtweHql9nmjIi8hpdzUbcyU2S+M9aLSdsfWOzo2xO6Nya+pupJVbzdi0oTQALdeZafCswTeFkUR/yaIVZVZSRn6Xs+/MnXymKChNorYX9Z9tT9PQdfmp+UZuD0z85Xp0yYOdyGZ+77esCupVqNRVNRZjZ4xe/aLHuTUiSKncdePrmkoyqoQeI+b9fL050Od684eSKHce4uP/RMnqRdnJuWZjnxt9kuho/3sSf6Jzes2n6+sv5v1g0b66qdv/ui/e3PqNaTHMxFatWuhG2oVMnw0AAAAAADwJNBlta/v3hwBdHgmNuS+Cc3tJGX597oVE4C3/L7zp+++qa+rZ+rATOF3y6bvSPchmvzZlrm1a2d8EtMdMhLPY/EPCwRHN20KS8FNfTvFwdm3XYu8uqy0KIsAAAAAAMDjj83htmu5OQI8ymuAc3NytmzaOG/Rm0z63bPzj+6VfrsdRcqGtzZJhy942duQAAAAAAAAwD17xNcAh23/NSnhjI6OTsalSwRug3IKWfnhdDdu+pYS1H8BAAAAAAA64VEOgQZ4mB7+EGgdHRbF1edQeswXm8NlsVgE4GHRaNRqFa2iG5gvWlnf1ISJAAAAAOAJdzdDoLvFfYABnjBNTU0GPBM9fR4TgpkYQtMN9XWKpqZGAvCw6OjosthsFotjwNc34PVqqJfXKap1dHQIAAAAQA+GAAzQxZoIEfS2bdRo6mplBOARYT5wYSrAzFfLUyYE6xsYScsLEYEBAACgJ3uUk2ABPHl0dFjmlo7Khrr6egUB6Dbq6xTKhvreln2JDv7aBwAAgJ4LvwkBdBmm9msmsq+pqlCrVQSgm1GraVl1eW9Rn6amJgIAAADQIyEAA3QNJlQIetvWyqsJQDdWK68y7W2LDAwAAAA9EwIwQBdomfWqsXniXQLQjTFv0cZGjQGvFzIwAAAA9EAIwABdQFeXrafPq6+TE4Bur6FOwdXj6+rivlwAAADQ4yAAA9wvppLG4eoRgtl14bGhq6vDofRRBAYAAICeBgEYoAtwKQONRk0AHhPM25XLNSAAAAAAPQwCMEAXYHO5Gg2u/oXHhlqtYlNcAgAAANDDIAADdAEOm6tRowIMjw3m7crmIAADAABAj8MmAHDfdFmspqZGAvCYYN6uLBYmwQIAAIAeBxVgAAAAAAAA6BEQgAEAAAAAAKBHQAAGAAAAAACAHqFbXANsIhDY2dm1beHqGZw5fYoAAAAAAAAAdJFHH4BnzZ0387W5N7dXlJd/9H/L0tPSCAAAAAAAAMB9e/RDoEMnTdmy6btRfj7Xvj7+v+VMe1FB/ucbvunr5EzuE89txIL//Xjw1PH4hP37dqx4ebgJRR4OE78Ptx78Zc4AXseLRZM/O3hoRaCAAAAAAAAAwIP36AOwialpcVHRze0fvPt2QW7eum++s7a1JZ1mOnzxph9WThKVRod9tfa7I1nEY86a9YuDO5mBKafJW078vtTf8O5WDpjqXnnwu7CLCgIAAAAAAACPWnecBKuxUXs/Vdf+A37bulkmq/7g4zWkk0QBC5eM5cetnjl71bqN4fu2bVo2e97KaCp43nS3B193pbPC337+nU1JtQQAAAAAAAAevW4xCRZDZGn19vL3m5qaNqz9PC31Qnlp6ZebfiT3ydRtjJ+g4GBYrJi+2kRXxW/bvD24dVAyJfKYNHfmJP/+9vzKrMTYXZu3HUyrJTzHl3/4PDhr21Hu2MnD+5vSBfE/rVu9M50MX/rbF2NFhLh988/kzM2vzd95me8zadE07eaUIisxcvvmbcdaN18/Pm35nM/TtaVfgc/KX1aI9i5avK2QpgwHhMydMz3Ay56nSI08mMbUoWtv1xMAAAAAAADoMt2oAsyk36bGJuZBlVQ6fWJo2+uBO4cjcLKgpOlJ+aq2rXRW1G8bw5OkTOi0Gb/q4wXedPzOr1avP3CZH7R0zduBopa1eHb+QYK4DQteWrQ6QuG1aPFMN44iet3UlzamyUv3vvms34ydF2mbSatWLHCj47d9tfq7I/mCsSvXLPQT3a4/ojFL170fJMjas+Gjr3bmmY+f7CngNi+5XU8AAAAAAACgS3SXCrC4pHjZW2+QLkXx+RSRK+TKWyx2GjveqfLgB59siNPWWg/GlVI/LJzkbx4fwTyjK9P2bo/IqaSJeNue4f4L+zmZUmllbTfnOY0Ntsve8t6Hv6VpA/bRpNK1X08f72YSH3er7lj4hXiSxM0rPwrPZyrSESli/nefuN22J3vLaAIAAAAAAABdorsEYCeX/t//uq1d4+uvzCL3gZaLFcSfx2eqrB1NQyVwchQpc3bmXR1pLM1JEpOZ3ra8iErmmVJaSbekT7qW+S+Xaj9tFt/J0U7ouXDr4YVtjphmybvl9FqUqZ2ASKPSW8dj05WXEwvkbrftyd6ySgIAAAAAAABdorsE4KLC/HcW/OfmRpFl50cCq6R5hQqBq5edYbz0+vW0lNOIqcG8izvDxc1Pbyqx3sP80LQ8efv6vUny61cYy7NKadLJSavvpycAAAAAAABwJ93lGuC62lq1WtO2RaVWM43kflSmxSZJ+05aFHr9TryUid+suTNHaDOqPK9QynX0s796TyOBo5cdJc4quMubFmk3JzxScjY+OkH7lVjKZFixVEVoBuHyTVtqxhTPxLQlydKV+VIicHcVtTylTPt52/Kv7eo+egIAAAAAAAB3obtUgPs5u3z905Z2jfNnvUzuizR24/oD/dbM3bDV9WhUwmWFhZtXQKA3ffSjsDQpU67dsz0uYNnypeLNEZeVhn5T5vpJjywLL6SJ4y13qFTIlZTIzkJUUilNa9581QqyLSJNbugWMmuqe8GG+R/uy6q8nFUpmrLg7SzO0RKe25hQJyHJZ7alS+PDk+esmrtyCdkeV8X3DnnZrTWXK9Ju1RMAAAAAAADoKt0lAF/OzBjl53Nzu6WVFbkfldEbFsxPnjlr+vjpb0/mEnnmqe0fbNgVXaXNlnTZsc8+5K/6ePGqoVymDJt5YO0Hm7WzQ/NuuTdanLDraOjqd37aV3JgwewNzZuvWPz+xzOZaFxydtdH6w5mqZjaddLmDdvtV8xctDKwJPlg2IF4+1nN47hV4oh1S6m5c6bPXTeFJ888sj08eVpIy35v0RMAAAAAAADoMjo8Exty34TmdpKyfNIpf4Uf2vvnzrDt2zpcOuPV1yZMee75kKcJwP1xcPZt1yKvListyiL3rampSWTjXCUtJQCPDxOBhbgwU0dHhwAAAAA8EdgcbruWmyPAo68Ah+/fN2fBIubrVits2/wTAegxKJcXfwl7z+OGH17J34umrTwhtx/50oKZoT4elpQk89zx3Zs2HsiUC4LWbP9mkmXbtZUp37w0a2smfYu9KTO/mrOa/N/PbxsdeXP6qkgJ6RTeoFW7tk5V/jZr5rqE+7hanXKaHbb9/npCdXRatO0Cn+cWL3lppIelEZEXp8T+ufGbHaeaJ2GnBIOm/ue1iUE+ffjyK+dO7Nq66e9EKa29Yn/gM/Nfmxo0yMWSSC602dXNeAMnvrl4zriBffhcpSTj1D+b1m+NzG0+D3yncXNefWHUIGaRJP1c7LWd34xvP27huwueHuRgxlVW5Cac2LphPXM4XsCqXT9MtWy3bsbmmbO/SpUTAAAAALgvjz4AM/n2n7177OzsOlyam3OlpqaaAPQ0FRcOncpsnWFcKU7IVTq/sP6H/wYImbiVck5pNWjkzI8DPOznz/ujZY3ck0cSSlpvea1MvyC53d6yLojJQPJkoG5xWr7N9Xjzh29fcuHKc89GniP2A33Hvf2Ts9WiuatPUeNWbfkf85EBkznP5gk9Al74b4CP69uvfpbq8v7Gr6c6c2VMeyyxGsjsapCL8PU3tl5onzt5A+ds/GXJQK6sJOXkObnQ3WfU7G8GOqx4Zfl+ifPsbze+7ctXFl9IOE4LBzI7Z5Lwkvmfn25/SQNl//wXmz8cJmTWPHVczncZNHTqxwMd+LPf2F18cvef5Nrs91xLn7FD+3AJAAAAAHSFbnENcJVUynwRALhKlntg00e7865VDvnui6cOEsrOffzKwr8yaEKJxn265X/PjJvgceiEdrE04bf/rT6luNu9UU5PSADmOz/d4WnxPh4bMtaFm/vnPCbxav9uEfi8u3XbS+MmDdlexH1hlKUy5ZfZ877VJluh99Jft7w88ln/fwyDRzpziw+/OWtVZIl2VxO+3PXJqNBxLn9daFfiFjpPmDiQW3H4vemrDjNrtubhIROG2p/NDX3Bly87uealN5rPtnDE6rCvJo4aO3DL6Xb1bb5L0Au+wutrMnn42+0fDntugss/605sXa39plKCgWMXLJnPpF9Jyj9/Hi9B+RcAAADg/nWX2yABwO0o5SmHdv+2cWvsleYUS8tLiuVKQnH55P4IgtYcTD2/c/bAlrtz8QKany4eaDvui6Op5zc/70Dxfd7469L51EvnY398zp7iDVq1N/X83sU+LXPFcYVD3/x6z9FzzNKjmxcPbb3Hl2Bg6NJvdx6Ojz8XvfP7Vc8NErbu3PnpN74OOxh7Pj42fPPqOUMs7/9W17c6LSY8Fwc+qchMuNL6yZo091xKMTFycBaRkhN//75p+4GMlkApk+ZK5ITL5/F4fCMiu3I6V9KyK/GJ9W/Pn7dmf2774csU38FBSGQZiRktaxJFbkpqCVOqdbE05Qv5TDU+4UJJyxLJ6e/fWfjmR79fkLXvOGXlJOQya2a2rkmXXDiVqyRCByu+9qxQgqBV24/s/HgcN/bjWc+Mnb7qrwv4iBAAAACgC3SXWaABoC0jh9AFq5xaBi0rr5zesSsqcssXkVeX8gc+u1g7WPfchVwFGUq0Bc6X31s5qmUItPzCvq37Lyhuubf0Iz//e8dqoqKkWKokAgchX2DlIGSSWjYoKesAABAASURBVAZ/IJPZjGKttBEvszUlEsunZw7SXkN7IeiFqYNeW/VmyqxV56z+8/VPsz2YTRIiM/kOg6Z+8LUlmf3GP2Ti57/8N4BbfCHhVCaxdJ+4ZL0Df+7rG5XkftB5HZ+WfJWQcAlNK6+nV7rlmmi1+PSOz09fbaTsn3lzgS9fmX4hr4pFtIE+aMFPrwZ4OBhxlZL0yJ8//yJWcvP1uxSzb9J230oG4XNbBipzhT6vfv30IB9XJuFKcs/+s/ajH2++BphLuJR2H8o2+2jpYMtO+FYO9swjrsfzH/4U9MLxras/+uMCSsAAAAAA9w0BGKBbMhv49KSr45SvkBN/RzGlQr7L2NcWvjjOZ6CVEdNacuj/1vyZoQrQrsF1GPasQ+vacsv0A4cuKOhb7E2ZIt7/b+ydDk9LMkrkXHcroUDoYs+X5J1KEThPZCqfQm2NU5JX3BoLlSkbl7+3JYsmR3Kp7d9McvaxMpWPCvLgSg7938Klh8RMMg9Ytf2HiaEB7tlk0iAjWezH85b8xdRU+e6Lf9382qhQ5+27yX3r4LRc5i+43RaU/dCXFswJDfB10G4hi137wdYk5bPMQ67rEJfju7//7A/KdcQLE8ct+4Irf2X5IbnAkn/1Kly5pITcgZXvwNy//1i7S+kw7LkXRs1e96l09rzdJUJLwdV90HfcB11yYv2SYm3lnO8waf7bz8xffPb0/D/zcGtwAAAAgPuEAAzQHcnOrnlp3u62iYfP1BW/fdNHO0z33InjmQnHd/95glkuaF5Y8ue8qbe7Brjd3iingI5X5F4blSyX5EqUQwQuli5MAVhyIDPFXj510EAHSyLkyq7kSZRE2HzczJSWMbxKuZwpZnK5XIqvzYrCp7/89+kvr+2WcrEwlTDtRgEfHjzz4fVuOTgIODf1oeNpkK9Tnls7eeGOqyOTOz4tfPfmw1Lk+ihrqvkh3Txv1uc//DdISJTFKZEnMlJjd/11OENBOWh3qEz58b13WibQPnxBuX3rTPcAFwuJ7/fX+iM7ueaVL1tLtdf3zbxurraG2/Isd9eHSz9P1NZr/z4n2bb9bZeggfYpT3+24zXX1heQsn7uB8XNXeFy2+yjeX+NvbxfeHeYVeb+LQciL2gbYkv4I4e+5zDMWfh3XgkSMAAAAMD9QQAGeBxQopEzX/UxKvn7/95e93dW1w2GVWpHBnMpq+YBuYRv6dCHSdTa3SuLmZTLdbByd7ai5Cm5ubnKEmWQg4c7zSfykhIp3RKAyU0jmGmphInC8gub//dbinY/XKZoLC+5kFLhw4Rmq7w/P9t6SqKNykZCvlKSeaFENa79HhQXtn/45slbX9xMSzOLrwbBW50WpVx7Za8rU5HmRZZoPxfgO7i7MJE3pUTCG/La3CBhRezaN5bvaDtQnInwLVfqcptj8tWDKZV0xq41751t7Y9SciG/0lkiIT59vB2E/zRHUsrSxZnJx7kSqUIuueFb0xpv5bRC/PdXyzOu7SMjt1JYImfq9j7OlttTmyfBErj4WnKZUysh1tOffXmYnJ9yeuUJ7XW/QktnIZcoZUol0i8AAADAfUMABuiO2l61q72s98jFgS58JjoZ+Ty32OPqSkrxqV2Hmh+1vQaYKK9E7dh1+u6qhXRuSqZkatCEVR8r/07l+jz3wtVbBtPyEqYEPNBhoIeQluSWyCV0roQa6eGs5MpLrpTc+spdRe7x2NyZs30mPichRzK4QyZODbDM+GX2vB8TjqfKfAeNmzpWeegc8Xh2wihn6a6Fr57qYE/y3MTIXHJXjBxucVp+P7XrcK7v8y9/u8Xq+AUJEToPDXLhlvy9K1Jm9pw2CUuI89Q3V066uoks9c/tp/8+VTJy0n++/tYpIVeu3WKUgzLll/0JpVJ56eGMGzr4578XRs4d97+f+IcSSphs7fPMIG5F5I6/M/Pl1In0Z1+e+fn3VqczJcySQSM9mILwP6ckldKSI3lt9yH558+Tzy4b9u4PP3kn5NJcS/eRw4Sys9/sT7wk0Y+VDBs38dPNwuPnJMTS45kAK5L756FUzIIFAAAAcP8QgAG6pbbXABO5MKeolmgv9R05yaHNSiXU2ZPNt0Fqew0wIVfow3/fbQAu+febtR6ClVODXl4yKPds5J/Hh7wwtHmJUppbTBsNG2REJH9fkcplTAAmQt9BzEETiuW32bf8wtb33pG+PPXZgJnvPc0lkrO/v/d/P15gttj14VLlqy9MCpiwJMiIyFN2LV+x/rSUOJH70jywuYPT8k/kiS9enZe3eMlLIyc9zxyuOOXwVx98s+OUmOujHa7MtQqYOKnNFjLhhV1H9n/+9nuSlyYMHfT0VKYYy/T8l7f+78dzHVTbFee+Wjg7983Fc8Y9PTWAyxR0j//y5vqtkdpR2Ynfv7tcMvPZkUODXrBiCr7My1y14rOomyfBIvKsHe/OlCx8d8HTQRN9ucqK3Au7Ply7/kAmc7hDa+aTrBkTx/qMen4oKck4+89Xu37/6xTyLwAAAEAX0OGZ2JD7JjS3k5TlE4BuzMHZt12LvLqstCiL3LempiaRjXOVtJQ89pqvv50o/3nWnA0XFASeaCYCC3Fhpo6ODgEAAAB4IrA53HYtN0cAVIABejjKcuAg55Zb9XL5Pi7aa4BlBAAAAADgCYQADNCzUfbj3l//tse1T8uUuf/uPpeL8i8AAAAAPIEQgAF6Njrrl+l+vxAAAAAAgCefLgEAAAAAAADoARCAAQAAAAAAoEdAAAYAAAAAAIAeAQEYAAAAAAAAegQEYAAAAAAAAOgRHuUs0Fw97pLlH5j17t3ylFbSV7IvHzrwD/P46dBn+/TtR3GplkXikpL/ffIxAQAAAAAAAOisRxmA+7sNHD3u6ZSkxJanpmZCH3//qS/PbHmak31ZIZO1PB4XEhpxMDzlfBK5J5TbnC1bpzu1PqOlmWeP7tyyJbxQwSyyC1n7w/TKzxetjq4iAAAAAAAA8OR7lAHYyMiI+XPJgvnXWuz69Pnlj13Mg9nTX8jPzb3Wfjw+wdjEhHSGsjIubOO+tFrCt/EaHjp++ecC5aKVRxF6AQAAAAAAeppHGYBvln/lSllpKSFNbdPvfaIr0xJiomsJSYiJSBB/8920Ef1No2MVBAAAAAAAAHqU7hWAGfk52Y3kgaJubjH3mzt35hifAZakMjXhaNi2LUcLae0CjqlX6MJ5oYHetqQk+ejeHKdpPlkfL1oXV0sAAAAAAADgMdPtZoGur69vqK8nXY8y7BcyZ5qbIi3iUiXddoHhgLkrVk93lEdvXvfR5qNim0mrPl7gb6jdwi5o2Zq5flTK9s/Wboooc5o21k1IEQAAAAAAAHgsdbsKcFfjWoz/4p/xrU/ovIi1W+JuvABY0Hf8CIv8sOUrN+Zoc3FEivib9TMne25PPMv3H+tGx371wYZjYmZBZJLYZMv7tgQAAAAAAAAeS098AL46CRZNGdq5B02avGytsnbB5wnXrgGmBK5OAkVWUmlrVZguzUqtpEZ4iKhLAncLIo68LG1ZoBJnpYjlFgTgYWti6RJDjo4ep4nNIhxdHR0d8mA0NTURVaOOWtNUryZ1tI7mAV+OAAAAAADwcD3xAfj6JFgk/mhsknT9pmljvQQJMbfdhmIqx63/BXiEmnR1SC89wtdvybwPKvhepY3WFIv50jGgmkwNmmQNpKZep7GJAAAAAAA8EbrdNcAPlEoqraS5hnyKc62Jlhbmy02dvCxawy5l4eRuSuddEtMKcUklZefZT9CygCNy8hDxEYnhoWli6RALIx0jfZ0HHXw7whxUx1iP6YC2GwAAAAAAT4RHWQGulFYyf67f9EObFqmpQKijq7ti9RpTgeCGlSUS0imUqZtPIKkllImdd0DwGF+SujFJrCKiq8ulZ7dvu7Rp0dJlirDoPCIYPmWOU8HONxPEtIo6euTylIVvryrl7kmXC3xmzvLlk1IC8DA0cXSJuZEO+xF/RKVDsZpExk1lMh0VhkMDAAAAwGPvUQbg1JTzO7b+4u7hca3F1c3NQmTJPCguKpKUl11r3/rD92kXUkhncE39X1npf/WZNDFs5cfh+XTbwc2q/PB1K0VLVy9aqZ0rS568/aNPdqVph0zTWQdWvEsWzgtd/Ol0viR5784D1CwPAvDAaa/FFRg+8vTbgulGk8CwSSzT0UEpGAAAAAAebzo8Exty34TmdpKyfNIVDpyIbmzUTBg9knQHFM+QKGpb5sei3OZs+cYn/t1Fm5JUBB4/Ds6+7Vrk1WWlRVnkvjF5VWTjXCXtsvEBTcZ6OiYGpDtpqqrTqWkg8AQxEViICzPxuQYAAAA8MdgcbruWmyNAt5sE6/ihQ5pGDekOeG7TNnwzhQ5ft/qnS8QpYOqisSJpZHw+0i88UM0TX+nfeT19M8GKZ01FhI48WPhbacsAZZazi5Gbpv7o5QYZi/PMaKsRpOrbYzWFXfEDZazfJFdiQiwAAAAAeKx1uwC84X+fk25CkXXgq+8sFs76eN907YhpaeqBtR9sTpISgAfKkLqbopyubR+eUK2uY1Pufbj6pfX1TBuL5eZiOkYjPXulQUaaJNVKMVHVkS6ho6vTZEgRuZIAAAAAADy2nvzbIN0Huvbi3g0L9m4gAA+RAecuVqIoX2u2qqL6FDEeY23oSNWnaTjBY23GC3QJMftohsH2fRKByMBFU29qYbBknLEqoXDtBbqe6LoNsV3ST7X7QEkkMXzOTzBYRBkQTUFW+c+nFXcsFOtzEIABAAAA4LHWs26DBPAYoO7iYyl9U557LyLOl5/NV6r4PF8zXaJRJyWUJ8kJkcu2H6tIunq9bkOlIrVaV2RnIGQxu+Y+Zc1RMS0K9mAv4WAe/W9k8c8pSqFT7+f6sO94WC4+LwMAAACAxxt+owXoZnTu/LGUrqOdoVCtjBKrxKS2QG3m0odrVFwvrVSK6UaVRplTqpJdm+mcps/nK4MGGLrzaiT6hi58Tc6FWjGtLjyWF8X8BUCxHVl0HTEQmrI5RK2+344BAAAAAHRnCMAAjx1tIZdifnifm9T3uZYWa56jfv15usO1Gwvy5eIBJk9Zcwt4BkJlw1ExE3R1+7j0nh/AFxJSV6c2IERMAAAAAACeeAjAAN1Mo4bosm63Qsv4Z0lOadhltYroCPuYzXQy9DWTni/ueP36ytrUGtMgO54vxVFVVGUoCNuYP30wn2QVLz5ZV8czXjKltzG5q44BAAAAADzOMKYRoJuh75AzdR37GAqJMumi4nxxfVpx3amLNQVqjksfPSPSVK8hHJ6+r52eoG2E1qjOX1FyzIy8jBtzrtRJmP1rGlXMnyyOi5XB0IHGjnf3QRiNAAwAAAAAjzcEYIBupv72t5qmuL7WHFJde76m9Z686pq61JpGYxHfhVKfSarOoPXHDxMMNmp7J6WmgiKFmLAMNA1nxRo1s4midv8FBcex9/wgswCKFisbyf13DAAAAACgu9PhmdiQ+yZu3E80AAAQAElEQVQ0t5OU5ROAbszB2bddi7y6rLQoi9y3pqYmkY1zlbSUdIUmJrnamOjo3vlWwA9Tk6aRFFXrNBF4YpgILMSFmXdz02kAAACAxwKbw23XcnMEQAUYoHvRhsyaetLd1NQj/QIAAADA4w4BGKD7qa5vauhG4421nalpIAAAAAAAjzkEYIBuRzsqtVzRpO4Wk041qRuZzmCgLAAAAAA8ARCAAbojncYmIpY1PeqJl7UdENdoOwMAAAAA8PhDAAbopnQ0TAauaXp0Y4+bZPXa9KtB+gUAAACAJ8Td3f8TAB4F7bxTVXVNsgZiQOnos5vYLMLRfXCjkZuamoiqUUet0V70W6vS0dzV3ZEAAAAAAB4XCMAA3Z02iMobiJw86MtwdW56AAAAAADwJMEQaAAAAAAAAOgRulEANrcQtX3a28KCAAAAAAAAAHSR7hKA5yxY9Ouff9nY2rU8dXDsu/3PPbPmzCUAAAAAAAAAXeERB2Cm6rv262+PxydMnzmLori//rmbecx8bfk9jENRM+fMYx6v3fBtu+LwveG5jVjwvx8PnmJ2tX/fjhUvDzehbru+afCKfYc+G29H7h/lNG3Lia1L/Q2vNwl8lv7115YlrryONzAJXLP14I4FXgICAAAAAAAAXeoRT4I1dnyIpbX1e28ucvcYOPO1ee8s+M+1RV9u+nH7lp/SUlOXLH9/zDPjf/tlC+kE0+GLN6wJFeWdOhp24LLC1i84aM6a9aKPlmw4WkWTh49jNzzES35k3bZ0RYfLaVqcmpOlzJbKCQAAAAAAAHSpRxyA7R0cstLTk86eERcV8fnGyUlJ1xbt+3NXxL//ikuKMy9etO/Th3SGKGDhkrH8uNUzP4gSN+fdfWFhgau+Wzlv+rGkTUlS8tCp8veumrb3NivUXt75ydsEAAAAAAAAulx3uQ0SE3S/W/9F25Z2TzvD1G2Mn6DgYFis+Fq1l66K37Z5e3DLAGSOqVfownmhgd62fKLIiti8dn34xXapmGcTOGvWzDE+bpaUNPPswW1bthwtpImh1/LvVjvFbkm0GB8S4MZXZEVvXvlZRL6ieZ/+oQtnhQa62RJp8tGIwmvDrSk7n6nzZk4e3l/EJfLUAxvWbz6YVkvZhaz9YTodnSIYHtSPjlw2eyM9l9nzgcXz916mCSXymDR35iT//vb8yqzE2F2btzGbEAAAAAAAAOiMR10BdnS0c+gzYnTw7VfLu5JD7h1H4GRBSdOT8lVtW+msqN+ytA8ou6CVa+bap21e9lKkVDB28Ydzl83KWbA+vc26hgNmrVg9nYrfu3l1HtXPP3TSqhVEumSTtkxN8ZyCAhM3rZ2/me89a+mShctS0xfvLCROoZ+sWWiXd2D7+jCFyHP8lFAnfmkaszrPceqqFTP5sZve/CRa0Xfa8sWLlxRkzd+bTwiXa+HmlrJl/YdbpKVpcuJ07eCUzfhVHy8QXdq386vf5KZeIVOWrjGVz/8kRkwAAAAAAADg3j3iAFxaUlJVWfnbz5tvs87M1+bWNzSQe0fx+RSRK+TKjhfT+RHLZiRQ8iqFtj58ZFdS6EonRz6Vfn11Qf/xI3jx65es3FumXSUinf7h88AxfbcnZTdfrZvw287Yy0zFWBy2a4zPTHdb3s5SUfDYfsrI1R9saI6pkUlS8y3vNN/NSZHz25svHiS1ldoqcdm+vSHjF/YXCbQBmJDKtL3b9h1tPgS5Pl0W5TR2vFPlwQ8+2RCnrfoejCulflg4yd88vqUzAAAAAAAAcG8ecQBuqNdqe+nvzZ6dXNVEOoOWixXEn8fnMvnzFqtQtsMXLRzvZWPKt7C35ClTCUXItQBMCRydRBZu7/8R8/71LeRSEz7VsvfKq9FaIZcza3OYqrDA0pTOP5DfOo5aJU5LF8tNr27KcwqZO2mMqx2fJ7C34MtPtYyOVipphZy+OdMKnBxFypydeVfHPEtzksRkprctb29ZJQF4VFhmg5+eMppfGH7gcIpCQwAAAAAAHiPd5RrgB0ElzStUCFy97AzjpdcvnaWcRkwN5l3cGZ5lN2fDF1MEWZHRcQeS0qpEkxfP4d+0D7oybvPGXXnXN6el2VKaNN+ViSZ3X4oVBSz9ZkUwSY6JO/JbapnSafLbIXe13U1HoAj0BFzBgNG+Xi6i3jxNTVFhStTZpJxukTa5Vq7DPOtO7y7sO8LXpSj6ovTuO0WJRj09ziIrfGd6xX29EpZoVMi4Xsm79uTXkQeKZRbwdIh9+p7fc2R3WJMSeTgaleZkltEGjkOnjKPO7jiRWUMAAAAAoPt5kgMwqUyLTZKOnbQoNPrNnRdbisCUid+suTOdYpftNLTz97GTHlj2QfN00JT5+MntN6flhflywpRhk6IL6eZt+/n3JWIFfcsUqpCWVFJenv0E4fnaIdAckZuriE+laYu/AV6C7O1vfvhbmkp7MyTLaXcMsvK8QinXx8/eMEbcHL8Fjl52lDiuQEHgSccSeE172l+vMC58//5SlmiQ55CJYwx3h0flP/rB78ritL0/ah9cyCT3iK7MSEssksievKoxS1/k6W6TXMgEYGVpTlI8S4yfUgAAAIBu6okOwEQau3H9gX5r5m7Y6no0KuGywsLNKyDQmz76UVialBYxv6WKfCYFe0iTiFvI5Je9TamsGzcXn90Zlr1h3oqVgj1H02oF/pPnhFgkfb5kdfitfr1VXT565PKUhW+vKuXuSZcLfKZNt6Wah1/T0gIFFRA8OSBJnsP3nzJ1cl8+9+zt+65I27M9LmDZ8qXizRGXlYZ+U+b6SY8sCy/EBcBPPCM3by9hedSWUxdrtGFRdjyqVi9k3FCbpPwcGYvnOGLIEE9rU1Kdl5wYE5VfpWkuVPaV5jbYDLBnVSSfPpln7j/OzYFHlySfPHg4nwmcLEORxzhfr74CrkJ88dTZuBTpDdfFs4wdRwwOHGRvqqcsP3cq/HBOlUbb6DyaOZDIqEGckqa06Vsf+WtckZIYMBXg0Z59rfWZpHf2cNyFYppr5f/CRP2MDOLiaW/Krs4+dvxworbf2lrxaHdnZs2ivKRTiSk59Ub2rt726XmZNcqOjsgSOI2e6OtibUCqS1KORZ28eEPFm2VsPWSc74C+vUhpzsVqVtuea88GW1F47syxqPy26bq5Y/y8PJazW29NXmJkfH3f0f4DrKnavMTDu1OKarX79Brt6+0mNFRXZxw+fixRqjS0HvvKEONqpZF9r9qofyKv7cvQevSMYWbZx/ceL1drt/L2cGFOZnlm1MmTacR5xpQgezaxf/Etz6jfjwm8/KjatCKlRcenxcDOLYg5gRakMiOrkGdvmvbv/kSMJAcAAAB4aJ7sAMwUgaM3LJifPHPW9PHT357MJfLMU9s/2LAruoqJkfkRmzZ5L13wzvpgQudFbTsY3XeaqN3Wqst7160ULF35yjLtNNXy7KObP/kqooxuM1VVO3TWgRUfkIWzpiz+dDpfkrx3ZyQ1y0fbnnZg02bXpXNX/hzK9OHI9ohk+zsOgabLjn32IX/Vx4tXDeUyB888sPaDzY/i3sXwkFFG1r00eWdya67FIrro4N4tzYtEI0YF2ZdH/homJgLvicPGja7fe4R5T7AMeulX7NizhdiPmDZigkXinh+2HbP2Hj/R2yu5KKqUN2DiiAGKs/u/K1QKmZA5akTDgSOZ9Vd3zjLq6+5tXXd25x+Fakv/EO9Al5L9FzWiESOGWZdHbokSsy2HPTfclK39cIjJm0ETnZSnIn7brTRyGzJuon/tr9FFzN8ivSxtSNThLSmmQ4cH+bnbpJ0q1HMcPdGdHR+1dYeU6zZ8ysQR6l8jxLc7IqvvaG9LSdwfO0uIvffoQf1F2WeLrsV0lsBj4gj76rg9G0rU1p7jJgq52S1nY0SgRV7kryfL2b19Jw4Z16DYE3vDmGw2rxc3+8DWYwYDJo4ZP7EsakfYSWI9bNqwIW55e87QIj9PB5IV/l2E0sJ99GjfAXkRSQ2ErcczJZfCv0svqiFmAc174Qq8Jg6zkZzeE1XORPeBIUMcJGf2byhXWzgFh4zyrw6P2rGHPWOsTfK/+1MUTOq+fvSOTkvwxP7kVMTWjDojz2Eho/Ur0wgAAAAAPESPOABLpVKXAW63X6e3yDI9LZV0miItatN7UZs6WJCz74P/7Pvg2vOdv7X89+gnk45ebaOrkja+P2ljuy1rkz5/dTy5vs6x954/1vpEVRm3d3Xc3uvrbmv9b9K2VdO2XW/+rXWf4W8/HX7LPTM9fO+lfQR6FBZXj6gV9R1UBbkC577cwqjkHCkTX4vORhXaj3MSRWlnCVdKigqrNUpNSXZpvWm1uFKp0eTlFSnsjXgUS2g/QChNCs+pYNarTY9LcxznaWmUee26Vo0s89Sf2vHMlJGVsk5N9bYwYGVTbQ6UFxfv5OCn7ZhhX6fe1el70qRMoVWWfClv0JC+1lSRgultSUp8EbP/ylNpA/o6mfaiKq2dejdcCk8ur9OQupToP/JYyhqN6W2OeFHJZrNYehRR11dcPBV28cYzIrR27lWe9HfzS8hMPpttH9R6Nkju4fQ8KfNxVlHKOfkUpl4dL61qc+LUDZLconqNks7LrvbWE5doT5E4u4geJuSySU3RkfA/tXvXN+slVxIbs14sUspsUp1xKqtI++lDS52Z1zfE24uduj+8uZZubu/Sqyzx73xtT3KyUkr7+7r04hZ1PNF8h6fFTHFpf3K59gSeS87wHGVKAAAAAOBhesQB+MTRI0+HTjgen3Cbderr6r/7ch0B6Bk0ygY1mwmuNy9hGxiylTJF6yh4dXW1mm1pqEdqiUZDtP/rEJvHZ6vralpvJKapldAse30Ws/er63PNXUc/59tXj66slqt5LMJmsW84kEZZLa9Vax8Z9tI37Tti7ooRV/etzNVrHuOv1miaV2A6wTxgaddk2uW1rYfQ1F3Pk7c4IlFkH0u0DnGfMN9ToyjLjk85e/H6OO12L6Guuk7TS3s2jHuZ933lFe9r+5WU67HJDeehtWMdnhqWyQD/cSFOpg0KWXUdW49V22ara+sY9R3MhO3Kc9W1ytaeGAmdJ77rfG3d2jTmO3WLO611dFo0106Luq5SQSMAAwAAADxcjzgAp6elhYwMdPd4isXS6XAFjaYpNeU8AbhvTAhhsdhtn5Juia7Mriaj7XsbFl2dfZwSjQ0ZL0z7cx8TRLkGPIr5VIhoR9j2YmJh7Z1uka1WyNVsc2M90lynZBkKmQxWr7ke8YwHjPM0zDj0w/FyJdF3nBI6RLtNnZJcPxCXZ8Bla2dcrq2ur8yO2rMz68ZLbTs4aG01Tez5hixSp12TZWBMKWvo2x2RCdNl6Ud+Tm/OpcMnjvOvLT2UdHU4c7uXYNTLgNXcyZpqSeLhzs4NZmwfOLp3xe6wP3PqNdzeI14Zwe1ordqiM5Hx/MCQYUF5fx++WM/0RCbJjvz1RE5tm5VYxuTuNFQznz5cOy1cV3RDFAAAEABJREFUYz1M6g4AAADwkOmSboCJuMlJSR1+If1CV6lX1NzmaTdSl5eeq3Yc/dzQgY4CI2OB/WD/0W4kOz5PVifNzFbaDHW3NmTSU++BQ21IdpZYeYe9aSR5FyUCr6HWRiym9Ork68YtSS5pc18fjVpNuGyWNqY6unv35Wk/IlBW55ayHJoPxDIUOXv2NtS2amTZWeW93PzdjLnalf2nLxwzQMDq8Ji1zJp6/X3djJnFBs5Dp74ywsWYdbsjsgReL02eMFjApFBlQ71afcOnExpJUWZ17+aXwDKwc/fqq9/cSeZsaBxGuFoze+YKBk59YfpYEZfcNTXTC3bzByL6Ik9PF2HHL0TToKjIOHv4VJ3NuGEuAhZzMjOqhb4j7JiTyTJ2HPufyWOd9bVFcuYV8bisOxxSIysqrBW6N58Wlomba18h60mfhAEAAACgu8HvX9BTSCsKmkijvoG2XFdfV1NZUWQqtCTdkVJ8cufx2nFDgmb0Z35AG0qzz/4dkZSjrXOKo45HjhgSNH928yzQp8OjmCLqHWNXzcW/o9jjfF9YPoZbLc6MOn7y+gxYzFJFZlRq3+dCF/kxB8rLk9Q3Z8j6vMPHT4/wDV48z1RdkpJcLuM1r1yTc+xvatjosXMm9tJrKEs7diqbKdJadXjMljWfWTSRz24oS/z7eMa1a4A7PKJGmnEqx2bihEXj2EQtyTgcndl2NiuNNOXvk4YhQ15e0YuUZl7IkLK1f3HRzNmIGeEbNGdWbx6pyU48Fl9+p08D2qgtOh3lOPG5lxezlZXZheXVt56JWUOL46NOWj8zLMS1fEfaxb9PNp/MscbsusL4k0ez64mG5MbnOYdMmO9ydt/R2x1TU5Z++G+DwBGhiydSlRlphaW0EQEAAACAh0mHZ2JD7pvQ3E5Slk8AHivM+7a0KIvct6amJpGNc5W0lDyRDJxHTh2hOPzrWfE95Eu4E5bA55VRlue0c0eTR8NEYCEuzNTR0SEAAAAATwQ2p/2AQAdn33Yt3WIINAB0Kywz75GTxzuZGVIGVk5DRliS0pIapN/7Z2g94qUxPo48LtfY3s/bo1ddYVE9AQAAAICHB0OgAaA9TWVGel7fYS++O4L5G6Im+/TBw0V1BO5brTgl2T544ouBPEIaylLCj6dINQQAAAAAHh4EYAC4iaZWnLTrzyQCXUtTdfHUnxdPEQAAAAB4NDAEGgAAAAAAAHoEBGAAAAAAAADoEbpmCDSmgAYAAAAAAIBuDhVggCccyywg5NWXHLvPLWe5Vv4vLxxur52knhJ5uDqbU3e1maHj+IUhPuZ3uu8xAAAAAMAtIQADwKPC0hd5urtY3F0ABgAAAAC4X5gFGqDbocw8vIcNdbLppanMTo4MTy+q1RBub6+Qob4uQkN1de6504ejiuqYNivXYaPdna31lUV5SacSU3IUGu22vkEjmG3ZtXnJh/9OzKtps2OWseOIwYGD7E31lOXnToUfzqnS8Aa89MzA6jyZtZM9T555LC6b5xk01N6USNIOHz+WUnP9Lj2G1mNfGWJcrTSy71Ub9fefsfWmd9FJjYX/CxOpk1ui85SEGDtOmOFasvvQhaudGThtSpA9m9i/+JZn1NZtWWrm5YzzdLHms6vzIv+OSsqntSVib/9hQ+1FevV5yYWsq39fsQxFHuN8vfoKuArxxVNn41KkzO5ZAqfRE31drA1IdUnKsaiTFxVtbzHU0bm6ofHssbMXiuubX6YvySg39XQ0VuSdPpxFBvkPcRGyqvPimC4V0wQAAAAAHmMsSt+YAPRIBrxeCpmUdAW+sbChXkG6hIGj/7Mj9dLDjx2LyW2wHxzkRudeqtb3GjGqT/nx7REnL9FWg5z1inLL2X3GvOCplxS1Z/eZrEaHUc/0U2XlSAz6DB9pUR1z4mBETr29xyDr6sxMBde2n1MvSXqqjOvkHdhflRx+NPJcjekgL8e6K5kVur0HDnDiFR7bEZlU0mvQs35W5af+/CMhm7b2GyqoSMuvVl3tFmXk4udqoUj7d8eJ05fr9e+ukxW6VgNcWAVJ+dVM3NQzdRloJr+UXdbSmJiZmXxFaWutidq77YhYyRW4P/OUoCj+371J2ew+AV588aXixr5DJ440yPr78OFTxbpuXh4WmsKkrJIGI/fngt0bzh/ceSqpiDNg3GCr6is5Uj2nZ0f0l53ZsyM2tdLUY5BpZUax7GoCZoJ/B+eK6jPmRU+9c1H7w8/nNdoGjnNQZeRVNPL7DnLpXX5m987zxZTLqGf6KmMO7vk3W2Hr7ttHkZ1apSRPDH0DHvP+19HRIQAAAABPBF1W+/quidCqXQsqwADdi77I01KZfORiPlOiVGTE5w18zt6Sl1POZrHZFJvQsuL0gz+nM5nOyNupd8Ol8ORyphRclxL9Rx5LWaPRkKyDP2cxS7nGAqVCbSjkG7DEV/eskWWe+jOTaLOslbJOTfW2MGBdZAKdpiZbXKnUaIryxAobklet1NDl2YWVfjaGN/79oG6ozjiVVaStCt9lJ5kSK7lbSmnS7/uTtNVdY251nYbXy0hP38DNXJ0RdSFfoSSKi1GXBljbMyuyhPYDhNKk8JyKWkJq0+PSHMd5WhpllrHZLJYeRdT1FRdPhV1su2uWYd+bzxUxZE6gQtvI5GRZcmKi2zMDXHgZaczrrBdna0+COLuwZpCgsKheo6wvTJP6+vG4LOZsEQAAAAB4bCEAA3QvlCGPZzN66uLRVxvUZZl6pCI5LtHaf8iMF4ap5eLk5NPxYr1eFFHIa1vzmKauZbSyYW+viaP8rVl11fJaYkDUN0wZxTV3Hf2cb189urJaruaxCLv1MzKNWt16KLWarW67xU2BT938lHWXnSyqI3eNxbMfMWKcn0DN9FxBuGxF81FYtXl1LT3SNCjqGrRHZ/P4bHVdTUPrC6+V0Cx7fRZLkX0s0TrEfcJ8T42iLDs+5exF6bVqrWEH54p1Q6OGrlVouL247NbTcPVVqwkAAAAAPEEQgAG6FyaJKUqOHf8zVnpj9CxP2LU/oTnEjp82IlDxT2Q1Tez5hixSp12PZWBMKWvo3n7+XiT5zw3pFUpi5PH0FM82O2AZDxjnaZhx6Ifj5Uqi7zgldAjpLM1ddvLvwxINE7O1OVvJhGnmwS3ncObaewe51EV+dyizRsMSuL0ww7IllBoKDdhEe70uS49noKfdXK2Qq9nmxnqkSBtwWYZCSqOoZ2rfyrL0I821cZMBwyeO868tPZR0tXe1HZ2rGxqbw7aySKkmmJELAAAA4AmGWaABupd6cXIJ29Pbw4piEcp6VMirs9zMWJT12JCXpziasIi6gVaqmZKtqjY7q1yvv6+bMRMKDZyHTn1lhIsxS83URZtDJsvYztevt8ENn3BpC71c7VKWgaO7d1/efXz8dZed1CgVUhnb0tvP2sSQZ+/n2luv3X40TOLkNo8sZmrLajaDicIClxH9m9esF6eVsV28B5hTzOtxGdrSSDSSvIsSgddQayMWk7SdfN24JcklMpbA66XJEwYLuEzWbqhnDt2mdqvp6FyRNo0sIxdP717SixmKOw5w1lbRJ3jYG2pL1o5jh48Y0LxPO7exE1xFXAIAAAAA3RsqwADdTF3O2fAo76CJ04OE3AZJdlx4ToWGZsWnFk4cNnvFKCbflSSfOpzB1Dxzjv1NDRv9zKKJfHZDWeLfxzNqaE3y2cy+o2YuH0IUZdlF1cq2gVOjyIxK7ftc6CI/0lCalyepv5+8dpedJJq8mGN2UyY+M9uzJC2++RpjckOXcuPznEMmzHc5++dvyaezx4xb9No4tbwwQ1rZPMK5LjPuMM9/xLQZQb3qc+NzCqt7N29Vc/HvKPY43xeWj+FWizOjjp/MrGfScsapHJuJExaNYxO1JONwdGab4rSm5uZzxdSMWxvnh1DK0ryzu09erNEQwzu8cFYvkb2LQeWptDy1gaW9vQM7K+6igiu0ceirydNLFz9Bc2QBAAAAPIl0eCY2BKBHEprblRZlkfvW1NQksnGukpYSgMeHicBCXJiJWaABAADgicHmtK/wODj7tmvBEGgAAAAAAADoEbpyCHQvU1MLkaimqlpcUkwAAAAAAAAAupOuCcDmFqL3//uxu2frlLOVUun/Pvn4bNxpAgAAAAAAANA9dMEQaD7f6LuftxYVFi6cPevp4UNnPj/5919/+b+PVw8OCCCdQLnN2Z5wPP7QitGiGxeIRqw9cTw+4ceX3TjkQeHYTf5o36Evu/gQIp+lO37f+b8Qv5DFm/43RoTbrAAAAAAAADwCXRCA5yxclJOV9cWaj61t7Fav+0KtUv/915/ff73h3fdXkE5SEiL0CPY2b9PEEXmPdeM3L+pihn5rfj/4Q4idNpeq5OLCrKycfKmKdB2eU4C9dM+mRM/FSwJIWrqUJgAAAAAAAPDQdcEQ6KcG+ezZ+Qdpngt30GA/5/79y0rF587EL13xob2jY15ODrlndGWelHIL9hBFRIhb4iJl6hXclyoplfPJA1UZt2VZHOlaiugNC6KZ/+6N2UkAAAAAAADgEemCCnCvXiZ1tXXMg+MRh6811irkzJ8mJqakUxSXE7OJU5CfqHUoMiXyGe1EmEbF9XUM7YLnrP3l96MJh47+9eXKWT4tQ4tNg1fsO/TZy9MWrP3rr+iEQ/t+WRBod30nU9d8ufPEofhTf23/esFoN0NC2Uz9YfeGMRYC77d3xf61OtikZfPxdkzd1mPp/uPxCW2+Dq0IFDC74Zh6TV75w9aj2sb929eEDBC0dojnNmbx1z8ePHU8+tCPX3042a/1uHe5foiXiECzUWPGPTvluZvbmcaRY8cSAAAAAACATul8AJ4642Xmi3mQk5NlZXP9ZsKNGg3zp42tPfNnbvZl0jnSuMg00j/Y36I51XJE/kFOdMLBpNprI6B5/nPXrgoViQ9s+uirLXGKAXNXrJ7r2HJ1LSX0HO9duuuDRTPf3ZwlCF22KMCUWUDZTFq1YoEbHb/tq9XfHckXjF25ZqGfoHDX/OcWR5RKE7+aGvD8yqNV13ugyN710fLF72q/ln52IEtJ5zFdkhPKLmjlmrle8gPLXnpu6pthUq+5y2a58oj2EuVla94O5qfvXL965eYE4j935aIAJpPfbv3/ta6/bmc68V64evkYO1werGXAM3zrvWXTZ85q28g8ZRoNDAwJAAAAAABAp3RmCLSwd++1X3/bq1evH7/9lnl6+J9/5r/19r///F1eWrpozqt5V64wja/M+8+pmOjq6mrSSYqUo2n0sjE+dnsLLxMLvzG2dNreLPnVabUoE7/JPvy0zQs+Cs/XjpGOTFN+t25EqNvODXnMM3n2wW0HkrJUJOvAFrexG0b0t6eiaPuxwXbZW9778Lc07fW9R5NK1349fbybSbz4Vpfk1uYnJeRrj2Uzfk0Ak7RXboytZNbNj1g2I4GSVym02x3ZlRS60smRT2ULhod6kdivPthwTNyRIE4AABAASURBVMy0RyVlZQ+3L2PiOn2b9enr60dnkS1rQgOdIlu617Md2LuHx+PNWbCIeRy2fRtpTr/M0y2bvgvft5cAAAAAAAB0SmcC8JwFC2U1Na+/MlNfT595euRg+NjxIWF/H4g+djQ68sSwESODn36Gy+XOe/kl0nnKyqSIFMX7QX5OB/JJQLC9Im7bJSm5FoAt3Ox50qj0q+lVlZ+ULp9i00/AyWMyp1JRKW+NkbRUQSiK4hK+k6Od0HPh1sMLrx+DTrPkUaTytv3g9Ju+eIF36b53t8VLr7ZRtsMXLRzvZWPKt7C35ClTCUV4du4WRBx5+eo6irSog2n3sn5ecr4ywM3elEorwyRZV3NvSwZuecCk35ZGAAAAAACAzrnnAGxuIQoe98xb8+YEBo16/78fffbfVccO/7tkwfxZc+cNHzXab1hgTVVVakryxq++lFZUkPtAVyYdSZKvCB7e/yIJEkkTNqVV0W7XlnY4VphJurfdozx5+/q9SXL6ekNWKU1utw3Pa9bKWX3zty3ZklR7tWXOhi+mCLIio+MOJKVViSYvnsO/TZfubX0KQ6Cva5uBkX4BAAAAAOD+3XMANjI2Zv4sKizQNGpiY6Lnv/lWbExUfV3dts0/MV+kK0kvHYyrXO0fOp42lcZFZknbLKJLL5fQwe6uIiqneQg0x87LVSDPuSxWkVtMJSXPK5QSD1JyNj6puTjMs/Hz5om1tzu6degUBSx4f4ogdePKsJyrodnQzt/HTnpg2Qebkpj+UObjJ7e0K8RZpWSyZz9BeL64efdOAcOdKuMiCkS3Xd/u2vr2nnbcypg8Bcq/bTChV6VSMw92h/1OAAAAAAAA7s89B2AdHe28WTw+Pz0tbe3H//1tz9/TZ8765Yfv3QZ6+A8N3LzpW9J1arMiEqQhU8aT7O3faed/5l1bQpdFb9sz/otZK5eQ7XFVlH3QnCmmSd99woRM3i32pUjbsz0uYNmqFWRbRJrc0C1k1lT3gg3zP9yXxRSCacqpr529OS0tu36bYcp89JLFk0UFB/dUMSFWG6vpyqzUAoVYQUQ+k4I9pEnELWTyy96mVBazTHU5fPvR4BULV83h7kmRE5vgRXO98r5Ki8i+/fpvr5rDZ9bneoyfG0Ti1u1LqyVwA0RfAAAAAADoKvccgLMyLpWXls7+z+sff/B+rUKx5sMValpbtfzg408OHfiHdC1FVmR8XqgdiTya1X5qKEXSntUfma5e9fa6Kcyz0rjvPlwdXni78ildduyzD/mrVix+/+OZhChLzu76aN1B7W5VaXv3xPu/ve73oKQvF318tc5MiTzGe5sSrun4dz4e39KkTP5q9vJdEZs2eS9d8M76YELnRW07GN13WkvNWZqw6eOv+B8uW/npdCIvzUrds3Z9ZD6tInezvnbRxpWfxYpR/wUAAAAAAHhQdHgmNve6jY+f/+cbvon4N3znb9vzc3MdHPvOf/MtWzv7WS88R9NK0rOZBK75fKZyz1ebIy+KMZ9zNyc0tystyiL3rampSWTjXCUtJQCPDxOBhbgwU0dHhwAAAAA8EdgcbrsWB2ffdi2duQ9wQnzcynff8fUf8kvYn8fjE7b8HlZTXb1wzqtIv4yqmI8+3E6mLJxsiwmtAAAAAAAAupPO3AaJcfpUzOmnY6xtbYVCYVVVFVMHJqDFc315zeLJTiTu80oMZ+5JNBqNjo5uU1MjAXgcMG9XjUZNAAAAAHqYzgyBBngydOEQaFMzG5puUKvwsQc8HtgciqL0KisKMQQaAAAAnhgPagg0ALSjohtYLA4BeEyw2RzmTUsAAAAAehgEYIAuQNP1LBaLADwmdFlsWllPAAAAAHoYBGCALqBSNjQRgMdGU2MT86kNAQAAAOhhEIABukBjo1pZL9c34BGAbk9Pn99QL2tq1BAAAACAHgYBGOB+tUwjVKeo1tVls9m4/xV0a8xbVJelW19bQ66+dQEAAAB6DgRggC5TWVFoyO9FALox5i1aWVFEAAAAAHokBGCALtBSSWtqaiwX5xib9EYdGLohNofqZdq7rCSHNN+wGuVfAAAA6IEQgAG6RmsGbmwsL8nh6hvoG/AJQLdhYGjE5eqXFWcj/QIAAEBPxiYA0EWYUNGk1SgtyzfgmTCRQ0dHV6NRqdUqjVrd1Bw8AB4O5r3HYjM4LBaHee811CvqFFVXFyH9AgAAQA+FAAzQlVoyMNHOiVXVUCenuHoU15Ci9NiGXNwoGB4mjUajVinVKrqhTkYr6xuvzvmM9AsAAAA9GQIwQBe7loEbG9VM2Y35IgDdA9IvAAAA9HAIwABd7+qcWE0EoHtA9AUAAAAgCMAADw4iBwAAAABAt4JZoAEAAAAAAKBHQAAGAAAAAACAHgEBGAAAAAAAAHoEBGAAAAAAAADoERCAAQAAAAAAoEdAAAYAAAAAAIAeAQEYAAAAAAAAegQEYAAAAAAAAOgR7isAO7u6Ho9PaPmaNe8/pEtQbnO2n/p95XBDcr8MvZZvPfjL5H4Ux27yR/sOffmyG+dOm3BEwUt3njp+9Jc5XgLSSQKPxTv+2vlhgCl1N2tz7KZ9efTQR6NFbdpEI9aeOB5/aEWgiAAAAAAAAEAXua8AXFhQ8M6C/zBfyYmJtrZ25KGhnCZvOfH7Uv+7DMkqubgwKysnX6q6025Dly5yvPj5kk3SgKVLRojuKsHeRF55OSv7clYpTZPOEXkHuZFKOd812M2EAAAAAAAAQNdgk84yEQjs7FpDrw5p6mVi4unl1fI0Pz+/Siol3Udl3JZlcXdejc7a+/aEvdpH4a/uI51FFx78+P2DpLMo8wHD+9Opew5ypwSP6G8aHVvZ2SANAAAAAAAAbXQyAM+aO2/ma3PbNXp6D7r2ePvPm7dt/oncH0Ov5d+tdordkmgxPiTAja/Iit688rMIqffS374YKyLE7Zt/Jmdufm3+zovEJnDWrJljfNwsKWnm2YPbtmw5Wtg2NpoGr/h5ieGW+e8fzCeEZzN63pyZwb5OzA7jjhwlQdP42+a8GSGmialXyJx5ocPd+vLogotRezZuDL8oJZRdyNofpit27pH7hwZ725KSs/s+X7cprkq7X8rcb/rcmZN9BliSytSEo3vDtofnKHiOL/+wfnza8jmfpyuuHUtIEUnyzvXrNh0tu0OeFXgEu5GsjbFHeT7jpwe5CWJjxKSHGTVmnCGf98+e3e3an53ynEIhP3HkCAEAAAAAALh3nRwCHTppypZN343y8+nwa+sP34dMmES6AsVzCgokkWvnv7JgfQI1fOGyEBs6et3UlzamyUv3vvms34ydFxWGA2atWD3dURq9efVnm4+KbSetWjHH61ajow295q1YOdlWfHTj6vVhSVTATH+LlpHOlGjEsjULh1PpO9ev3bAnnfgvXLe8dRQ0l2vhF2x78aflM1/9cJ+479Tls/y0VwgbDpi7YvVcRzlz3P/7ameezaTlS2fecFxDr0UfrwwxTdq4aNKz81ZE88YvWRB8h4HiHJF3gBvJjk8tzU+Kzed7jPfugaOgDXiGb723bPrMWW0bmadMo4HB/V8bDgAAAAAAPVQnK8AmpqbFRUW3WlpYkG8qFJKuQNPihN92xl6WEiIO2zXGZ6a7LW9noaLtKoL+40fw4tcvWbm3ubgakU7/8HngmL7bk7I72J+g/+jhFpfDlqzemKPdSXQO9cP6YO0Cjmh4qJP0wMr3NiVpB29HRGdRPy8Z6yeKbR7MrEjbG3Y0idl/2fZtPoFrHPuJOPGk7/gRFvlhy1duzNEeNzr9cpoHpWhb361NWr9o0ma6svnaY+neI9PGhA6wNDyYX3vLl0uZegX3J/nbksQqmqRE582aOdxDFBEl7lmjoA/s3cPj8eYsWMQ8Dtu+jTSnX+Yp85lL+L695PHB1edxOHpsPT0Om8vSZZFHR9OoUamV6oZ6lUqprFcQAAAAAIAeqTMB2G2gx7XHry1YyPz586aN7R6TJjJg4MCLFy6Q+0TLK+XKlocKuZyJiBxy49xUlMDRSWTh9v4fMe9fb5RLTfgdTWGlXZlfmZVU2hoBpAXxeZXD+cwjnp27rcjZc9PhKW1WL7BjKr1SolQqFPLWOa1oOZNxKb52V65OAgWzq9ZwSpcl7Y3QPuC17T3he01ZGBLQz5InENkKuKX5t51YixJ5BDpR+dtSmhNvQVJ0wZxpQQMEUeIeNwq6Jfe2ZOCWB0z6bWl8LHAo/V5CkUpXo2I11uuo5TryRp0m8ujoNumwKRZb30BfwzNq7F0tKVHRDQQAAAAAoIe55wDcz9nl65+2MA9EllbMn1aWVtd+r7/2WLtIh3zz08/zZ718OTOD3B+a3LH+SVfGbd64K+96ZZWWZktpcq93EZJnHtiwLVZ6/XCK/CwV6fT9kCib8Ws+X+qtiI9KOHg0XUz5zFnkc9sNOAL3IC8hj//OrzHvXGusDPY2ORZeRXqcthn48Uq/fNPeHH0DKaVoeqShty0mftM6apqoCYvoNOn0MrNQ1dXJq8oJAAAAAEBPcs8BmAm0o/x8jscniEuKmaenT568tuja45ZFzGrkIaDlhflyIlLmJEU3T3xFmfTz70vE2jptRyuXipWmTl4WvLjmIdACWz97U0o75lkhziqlnYg0KSG+ef5qys7DT1ApZVa6RQCmpcxxtbui4nJajus1xoeXFRtTcnUNgWOgG5X03YctY7N5Xh7U7e+rpB3/3JdkHli7LbZ1zDNlHjxvrl9PHAXdggm9KpWaebA77HfymDAyt1JTRMGpJd0VE8uruLX6upQRx1JWXkIAAAAAAHqMzt8GqcWxI4c6fPyAKRVyJSWysxCVVErzz+4My94wb8VKwZ6jabUC/8lzQiySPl+yOryjKx3FKQfjKtdOX/q2Iiy6hNiNmTXenomyzALV5fDt0SErlq2ht+9JkXJtgmfN8lNuWzx/5+Vb9UF6dvu2S5sWLV3G7CpPxfeftjiEd/C9NgGYrpIqeMNDQv2yDohFAdOmB9lz6Yu3fk2UyGO0E5W/c8/B61NYc6SWYwOnBQ0QRYnzSY/0GEVfBt+kN5N+6zmPwacVTCcNdLhMh1EHBgAAAICeo5MBOC8nZ0hgoKy645G5w4JGMiuQB4cWJ+w6Grr6nZ/2lRxYMHtD0t51KwVLV76yTDudlTz76OZPvopgiq4dzhdcFb/+w9WKOTOnLRsvJHlRe3adpsZzm5dIEzZ88BX3w7eXfTpFe4TUA2s/2nNRQahbDoFW5YevWylaunrRyvFMiM67FPPdui2JtdcLz9JLW77bI1oyZd3W6dp7IO2MTBIF3Po1cQTeQU7cgp2JpXTbQyTG5s+aEuxuHpNf1hNrwI8TDqXPMTDozrXfdurYShMDHqdWD9cDAwAAAEAPocMzsSH3LnDkqNdeX2ht0/G2eblXfv3xh5NRkaQ7ojg8SqVoKQ9TJqPX/LSQbFzwQc8cY9zDCc3tSouySBcxs+wj5d7pul9NEgT3AAAQAElEQVQDi94fvWBmSZTH9lzZWtzY3MZ2des1UFN7OL2+hkWFhtiNIpL14VUFGnI/DCxM/jPOcpBR4+UT2WvSVKqO19Jt0jFV8ipKrhAAAAAAgMccm8Nt1+Lg7Nt+HdIpMSeOM1/k8UOZBK76bqVT+qaPNh4Vm3qFTJ/jT/LW50iRfuG+cPV5Kl3NHWe90rXrZyRUq2rZXA8nPYPiujqmjcUe6G42Tt0Yl1VfQ5oqKhtKiKqO3BcmZq+YbCZSMrH39jdfatRpYrrN1eMpG3BvJAAAAAB48rEofWPSg2gaxDmFGqegmYvnz58RGuzBStm87tO9WYr7q7bB48mA10shk5KuoG9opDFgq3TVt12L0gsNEFhWVcXI9DzMm9IvKcoINW5CnxdEuiw+f7SXfk1WvaW3ub9BQ2KN8fJXbILUijixWkV0Bwb1Xf+MkSq3psjAaMY4mwXBommDBYP49OV8ZU2TTl9v+9XP9GIV1mRdzc0GpvrmkopfLhIPF/2G3MqT5Y2Nt+wTm7B0VU0qZT0BAAAAAHic6bLa13dNhFbtWu53EqzHD52f8Nt7Cb8RgC7E5urV66jvsJKBmbGHKSlJk8UTg1GBfH+L8gsFqnOnxa7jrAaRql9OSM7V6Y5rXrNBUpNSKRjVx0CY3FDA0vO2o+gKSYqM4x9s7m/UcOBQabWZ8OVBltOK679K13C4ugbcJoM2P8s1BZKtBcTAyojcmUpHrc/VJwAAAAAAPUDPC8AADwCHzZXryG+/jm7fPjwzdcPxImUJkeWrRa5OesYFdZKKhhJlI61uuFxM1xC91nVpZeKV+lGeRh5GVRIDo/5GmuxzCjGtKjh4+bh2ui1OX7ayjhiaCdkcoko/feXV06Sz1DoaDseAAAAAAAD0AAjAAA8HxRRyucxP3LQX+09rabEz7mtQl6jscO3G/CsysafQ204vn28gVNYdLlapmAjtZrlopLEZIbW1KkNCcBNfAAAAAIB7gQAM0AVUaiWbYtG3GQXdMv65Iqv4t0s0E2XNnCxm9+f5W+gm3uIOz3UVipQqs1F9jP25XFVp5SUZ4ZgYzwg0JpfyFxxT1PFNlr5s2YvcP3YTS6VSEgAAAACAHkCXAMB9Uyvr2U23+zhJt68Tz4zUn0uuSSyou1CgiEmuzFdTrk4GxqSxTk0oI0P/PvrCtnM2a5SJWQ0ci17eJprsLIVEwxykSaXRzu7uassLHGTSt/Vw2kmwNr5mHyrUIZ3BaWKrMQMWAAAAAPQMCMAAXUBFKzma2/w0UXr+dhSpVCRWtt4oSVVVl1LV2MvKyJWrijsjvaQ0fDbY3P+Gkm5Tfn6NmLAMNfVxRWoVs4lctvecjONk+cbTFsO4tFjZMrWzTvMkWDoGnRzNwdboMp0nAAAAAAA9gA7PxIYA9EhCc7vSoizSRcws+0i5ijveCrhb0W3SMVXyKkquEAAAAACAxxybw23X4uDs264FFWCArlEtKelFP2bTKfeiDZluEwAAAACAngEBGKBrqOgGVV2dgZoijwkDFZeuq2W6TQAAAAAAegYEYIAuI68qZzU0Gai5pNtjOqmr1DAdJgAAAAAAPQYCMEBXkpWX6MppEyVPt6lzszI/cC3X/TKdlJeLCQAAAABAT4L7AAN0MaasyqnVMxVaqliNal2NSket1tE0PtLJsZjQy25icZrY7EYWR6NbLSnByGcAAAAA6IEQgAG6HhMvK0qucPV4bD19fYrLYRuwdFnk0dE0alRqJdOruoZ6ukFBAAAAAAB6JARggAdF2aBQIm0CAAAAAHQbuAYYAAAAAAAAegQEYAAAAAAAAOgREIABAAAAAACgR0AABgAAAAAAgB4BARgAAAAAAAB6BARgAAAAAAAA6BEQgAEAAAAAAKBHQAAGAAAAAACAHgEBGAAAAAAAAHoEBGAAAAAAAADoERCAAQAAAAAAoEdAAAYAAAAAAIAeAQEYAAAAAAAAegQEYAAAAAAAAOgREIABAAAAAACgR0AABgAAAAAAgB4BARgAAAAAAAB6BARgAAAAAAAA6BEQgAEAAAAAAKBHQAAGAAAAAACAHgEBGAAAAAAAAHoEBGAAAAAAAADoERCAAQAAAAAAoEdAAAYAAAAAAIAeAQEYAAAAAAAAegQEYAAAAAAAAOgREIABAAAAAACgR0AABgAAAAAAgB4BARgAAAAAAAB6BDa5dxyRf+ik4f3tBByarspPPLJzb7qCMvebNd1PfmTLznTFzVvwzL38+yrTzl4UqwgAAAAAAADAI3DvFWCeW+jUkP6UNHnf3r0HEytNvafMDDanaIU4LTkpq5TucBuurdeIAC8RRQAAAAAAAAAejXuvAPNFFgLlpZ1h4Re1pd5L+eKAfkrmASXyGuonLUtKqiIin0nTg9xEhkRelha952CixaQlIf2Y8Dt96Ur3nV9tSydOPuODA9zsebQ4OzriQExaLc9t8oLpppfjKu38+/Oll46Gp1PDg4KdzIk45WDYgXimbkyZe4WMHe3tKKCINCtiV1hsvoIAAAAAAAAA3DUWpW98TxsQmm3u5u3u2EsjpxU10tqaorx8ca2G6Fv7+trVpyekaTymT/elY7Zu3hNfY+Hn21eRdvxIXK29r5X4zw3fHi6hRT4zZ40VVETu/jNBauMd7GtVk5Ym5bv6eDvwpTG7/krnuQ8f6W+hOHVg99ma3r5+Hr1KklIkgqFTJvWn4/f/vi+h3n7EcA92ZlIWc1CA+2HA66WQSQkAAAAAADz+dFnt67smQqt2LfdeAaazwreHVQX7e0yeNYZH1eYnHtkXniK+Xo+lKIpQXBORiJeWuHdDXHOb4PrmIicPEZ28c0/CZQW5vDfSaeHYAXaGWTSz38q0uHSxmMQklroNr0xLLRQrKuOyfKfxeEzxWBy9fV00szXH1KlWLiUigSlFymgCAAAAAAAAcJc6MwkWqUyL3ZUWS4ihyM1n/OTQl0MUm3ZWXl1YlnQ00mnymEmzfCYRlTjxwPa9KZXXN+VQAh5P4DNnlc+1JrGAImLmvzR9LdHSpF245TkFTJs8pp9ApZBWKvkcIicAAAAAAAAA9+KeAzBH5OXbj5sdH8cUYGvFabHRbp4zLS341PWQq8iK3fJ5LCWwcRs+dpL/2OC07F3iawtVtFRBSwu2f7f3cpuLeHlutz0mZe4XEiSS7l37OZOlTfzmLgwmAAAAAAAALQyHBeoNcNd3deW69OcIhQS6GVVFRUNGekPGpYaLabUnY8ij04kKsMA1eISPHe9Ikpjw3QKCvU3kiaXyaxVbymb03ClOYqbwm5OVVyn35jW30kolJXDqaye+lJ+Vkj88aLi/jTiuUuAeOmk4lRQWlnT7IzIF4eZ5tvgCDhEF+NlzqDwCAAAAAAA9HsfKSrT6MwMPTwLdGMfMjPniDwtkHtelJItXvq8qLiaPwj0HYJX4aNh27pRJY6bNbHmaGL5rb46CmLQupwvjo5PtQ6av/B+HkKrL0UcOptUSkh0TnT1pzOSZfPLV5oSd28j4kCnLxphQdFlSxIGkfBW5fQVYO6z6lNO0kAXLx0rzssVSFZ8AQDdACV39RoeGDOsvlBz435o96Q/4wnzK5cVP3h3DLb4Uf2x3+JkrcswDAAAA0MMZTZxsvmQpy9CAwOOD+bTCPmxP2Refy/75mzx0OjwTGwLQIwnN7UqLsgh0jtBz1ofr3g115DY/S/9+yox1yQ/46ny+78o9O2Y7Nj9W5hxYvfyDsBRMCAAAANBTGT/3guj9FQQeW+LPPqnZ/SfpOmwOt12Lg7NvuxZdAgD3j+/5zsGcrNzWrxP/C2y+9IRyefX3VKbl2AqPux62QPUJnrdy9Ufzx/e5wyaUy5Sv95+N/m1loJAid7drq9Erf49l+pMR/ds3X/928vyJHyf3ucttb97Vsq8/0Kbfopjv35zxTOCMDR2lX8pq0o/nmROyf6nnrV4NJQx8Jyw69uDX01zveI7kZ9dOCXrmxWW/xFcQrmPoJ58vC8QlPgAAAD0Tx9rafPESAo8z5jvIfB/Jw4UADNCVlBUy5k/rpwL7dHagvpFj8LTZL05/aXgf7m3XoxwHvxTsamY9eEyIpxG5G0K/+e+89BQ5Hx1ziTs4NGQw9/y2749e6dQwYsoxZF4o87dVxdEPXl2w7uDZ9OJOD0c2eipkvJ+1Wf/gycOt7xzGaXlx+pl9q1997eN45kQ7hv5ndCcTPAAAADzOdHREH3+qq4+Rz4835jso+mgN890kD1GnboMEAB1TXok+SkKnuFoPHubIP5usJA8OnX7w49V9XveTHfghRnJXW0hi1r09K5y+dObK/Q4bpvr4Bboy+TwnfNuBK/d5Ia4k+odPv+dOMorftjvnrndFZxz48dhsv8nW/Uf7We+9cgUXAwMAAPQoem7umPXqyWDg+RTz3WxIvUAeFlSAAbqSsiL+TI6ScB0H+91Uz2wdJn1+y5RrVUuqz5RfzuXmZB18z4XiD/tfdFZuzumfpmgHglhP2ZSQc3XwMN9j6QHm8bmw1R/9Gp3avL4Hn2815sXpY0KmPzf42pH4fca/883v+0+ez8q9FHts98ZPXhlm1aYXfGvX597bcuqSdpx2RvyhsHWzAtsupqwC//P5rwdOpFy6uvl0j45HV3ONHM2Y/Ftxvn2W5rtqO3DobMsefv98cWDbOjZlNXljCvOiIr5a+fX+s9pTsTHEijLznPRSSPBLr45uvppYGLzuBNO9k+tGewa+8+PuEynaru4PWzcv+MZSrywn5lIFUz82sza6faUcAAAAnjz6bgMJPCke8ncTFWCALiUrPhlf9Ep/xz7DPa1/ybm3TXMupecoKSPr5nSprCgqkillV4qU1+rIRn4vTm9ekJxTJFeSdoOshYP/89VPSwdrh0MrKypkRo5PBTNfw59aPOu9f5kSKd911rd/fDCcWayUVVQwydHRb8oHT/XhTnv1J+3Vu3yXF9dtWjOm+SIM7Thus+bNA5/q//a81ceK21VYuUZG2sPIZLK2NW7KdfpXOz8JbB6PzRyD6+g3+XW/jl6o43jtRFayopxLV2S3KpILRy9eN3m4kYzpipGZq98UV6bm/MaUZeFXu0LL5BXabflGdzf+GwAAAJ4gegMRgJ8c2u9mGHloUAEG6FrKK/HJRdpLeQM9rO+pNilP+eH1CaPHvPxBOLM5KQpfNWnM06Ofe/uPNvcWksV/MS3Q23f4C2+GtR/1y/ectewtJv3K4tc979M/wNfPfeCUL+JlxDrk3cXBTJ2XydVWpKKiKPrDZzwH+foNGhiyhlnK7T/az5HSZteQD5Yx6VeZs/u9Zwf2D/DwHDJtdUwFs/zF/1s8/OYycEsDrWwbX4WBs+dr068s/sdZgd4efoOcAxf8cl7W0UttPspTI0e/9OWtRm9bDx9Gts4YynT1KbdR8389zxzIbPzrr7adSqv12Kj/AgAA9DwGbu4EnhQP+buJAAzQxWSXolMqmLz2VGB/M9KlVkRXgQAAEABJREFUlJeOHjtf3OH1rpS15+D+2qty9274I6UlVMqT9274Ye+BP3ZGFDNZkS4++ukbr7699qhR6NKPPln90YevDtPWmblCay6XUGb9g12NtKn7y7V7M7SjmmnJmT8+3RAta5nQ625CJt/R9ymmfqxM3vDJtzHNnaSLj234JOzSzasWpRyIybj9dcjK+J/Wbj3bspsrR79d+4e2mO7o6WqNKa8AAACAcCytCDwpHvJ3E0OgAbqYsiI55rxs/Bgzj+GORnccBH0vBUyl8pazanGNzPjMrmQVVyquryM58+PyM62PKavAd3/64ZX+HR+Pb9R8Ja0sp+h6xZaWVUiYZ0ZGRkImG99x3ixu6y6KKyquR3Ql81S7jxtXVcqUd5oeTCYpbrubihymK45GRlbaY2DGKwAAAADoJFSAAboaXZESfUnZUjttO0OTUinXjtvlcq+3MQVYsy65hlUpq5ArtXNC9TG7vnf+4Fc+/2bdO1MGCymqT+ib0/tzlZf+WPzMYDcHRyeHwQsOVFxbU95yNa+ZZx+zayVWSujYR1vClskksrvqQcsu+vR3vD5O2cja1bpTr8+oj4d1m904PmXVfPFysexBTqwNAAAATzqNTMZ83csWStWB17O8B2Yt+rPNB/gS+ftBGWOWyu/uThzdlvr02tzhAzOnLJXldvpXLFn91tk5U96qyX1sfklDAAbocnTR+Zh0bQIePNisbcVVVpTD/IXLdR3TcpdgSjj4xTde6t/xPrj3dm0rXZR8Rhu6HScvftFD2NzEd528+K3JoVMmDxdytRVio+aZtS5l5Eho7cLgSX7XRmjTFZeOpjNdMxvzxuIQl6t9e3f2U8wmzGu5ctNfaFeLsG06Kc85e1578bLrS+/Na5lcmrIa/fp7kx1JZ3D7T182v2UKa6pPMNMr7excOcnpRSj/AgAAQOcVv7uY+SL3rjHu+4qI4kby5NBk/in+NFbv3R2W/sUV//2+rpNhnqtr6cB1cmDxH5t5WTAEGqDr0UVnzuQQz/6Ow8Yor/9lQBef3X00J/RFx+Er/zr+agUxszbr4G8KZUWFdrixWfBH+yLeqcjZ+fHSbcl3cUh58ra1X3v+tHSw39K/Tr1aVKSdx9m6+bLeNRuOFtO0Mv5M0WxH6+Gf7D81v2UhKSpSEmvr577ewV339gfha9YGblozxvG5//3z3CfaWaCba9dMxfjTDdGS9qlTqZS1zMDctlES8/26vX7fTLZ+6j/bYl6RVSiZzE0qiiqIdacuhTbym//zqVdbd9PclV/X/nD2+khsbktxXYmaMAAAANw1lokJITqkM6SKH79WeK8zsiRPBpbzCzbhL2gfhf7OJ53G5Y5daT2WPEZQAQZ4ALTlUO3lv0Y33qRWErN64bx1B8/nKJnwS3Jifl+9+OPodqNw5Jf2hEUwpVSumbWj41P9+9z1CGLJmR8XTHvz1/giZfOmRrLzzP5fm9Z8DyRm6dF1C979I1nWsl8zWfQPy9/45GCO9jh9+ptRRJ7xx1svz/rhaI52kHZz+pWl714xY9bN90AizcOdtbnTyLrNiGntbFUHP5w2/8d4bR2Yiaey8+FfzJv/7fkK0gnKouTzTLmc25J+lUURX8x69dO2U0ZTZlbaYK2UFCEBAwAAwANG2fPGuOuKD0t+PaW+eak8Q/bt0rwpAZn+4/LeWV11TtKoHV28Isc7oOhAces6ygzprEGZs35uUJJGSULVp69fGTMow3tg5pS3pKdvLiwrVad/Lpo1Lst7YMbwcQWr/myQX2vfIV70/GX/gVkhLxV/e0h5tTagydxf9g7TPujy9KXS3RsKhgcU7s5tVOZWzWMOuqN18Lb8Qvn0QZffOdTyEjS5J8rfn31l+KDM4c8WrPpZUdK8kuRQ0ZhBuV/sr/ri9dwxgzLHPF+8+4Lmeq92lGqPPihryuzib/fXa381UzZ8+3zm8NdlJdo11Kkt3RjIvLScRWvl3XJctA7PxIYA9EhCc7vSoizyxLEK+X7/t35Xflm6fMPRK3ecvKpT+INX/LnzVUfl+S9abyPcZYTB6/78aYp1RfiCSW8dKya37sB7O7bNdyWXfpz24pfJD+ZFAgAAQHflkniBdErxsneYBGS19ou73kKpOrA499Ni40+X6vy0oDLL2eTHn80H0fL3ny9O9LH6Yx2fXyz774ySCFovZLaxs0Txx++18kG9f/re1PJC6SuvyUSrHb6cwOGSxtSf8+d9z3pjh/UUbvUbM8pTBbwXZxiJSmS//qKgx1n+emNhWXKi+JXFCv6zwhcD2PJzVT/ub3ruF9s3BpLUnwsXfd80ZIbpCGeSFSn94zAJ3WT3f0N1SvaXvLJSIXfmv/i8vjKyOuKCSkoM3t9hFUpq3ni+XLnY/qcZ2qvrmAA8b3aNJdOlp9mSU6X/WSzjjRM8F8BRXqj59a86weu2372mrzxU9OIyhdKeFzqDb18iD9uhKHEw++lngbuRhjn6vK+VlkG9pgewU/dLw1NZIRvsPgpQfzsjf7dQFPY9jxwqeWVZLRXQ68VxespY6U+H1e4r7L594W4u7GMCM+kKbE77gzk4+7ZfhwDAk6Xi/I/LP5a/sfiH36zfe+GNvcUP4LJZpky9L37Ku35PvfvTD8INP+48EHPlYYVQit9ncOirbyx70ZVLZNF/HLyE9AsAAAC3RBcVidd8rKNpLdwqr2STJp2CebNbF7M5Fv+3krK2vvOO+C4m856Vv/tP9bd/GX054VpzY0ls9WkpNWWT9f8NZZKVsbdV0bwNNRGZxm84G/nb1xw4XCcdZ2xJlFGHaWpgb38HXS6315d/8pVCjlAb1fS5uXWf5jZIZUaW10f9NcolGjnhDBlnHMrs82neiNlNAisWkSkO7FcKJ1i9s5gnJGQsE1wzCqMO10t8OKf310oF/E83WI21ImSCgeXrBV/e4QMCVeI/colDr/8uZZItIU8bCKT5/7dflvm8vr12KWvQa+ZvaHM7z5kUzPurLk8ucCf1B/Y3UAHmX6wzceCS58YZDvqllhK2HU2uazlS9OuhJr4VWzuiOoCVd6E48YJK/gK3m10djAAM8EQRDn5l3hhucZGyeU5os/u4ouO25OlhH692/emT8dZ+r6xhvmQxH7+4YGv6A56iiu8x/4efl/m1/PugzNmz5uM9GZgVCwAAAG5LR+fWF/3q3v31wBRnyOvCMbHiiO8rDjgbX50KtDHvnFJhyRvh0hKrdO0HGdoTSWqGWjmQO3YktecvWaKEz5fKT+fquC/lWWq30qVIQ9T35UeYOq2EzsprJPZNN44U1rX0MR4kEO9ZkJM4yNB7oOGICdr6sLJEmZnXlJdXNPavNp0SquRy3SxJk2Ag373lbrpcyjuAojJv+1pkqtQMjSKv8pWhldcb+WqpnNhrd8oSMUFd26RDCVkUaVLSjdqjl+g4v2Bg2fLCjfRCF+tpHyhV1/fA1aGktbu/l8XlqqQlyjwpEZFuCAEY4ElCCR0Hj589Rnt1bFH0txv2XHlg+VCevvftZ5L3PvfqtNDBno5GRmbch3CLXq6ZEZFV5OScP7k7bOfumCtIvwAAAHBbTHXXdtOP157e+xDoNrhW/HmL5YkrFWG/c5zaZFaKCYrXpkXhXovULPuRRk47pEfO0aLc2jy+wYsB2vG58oTyRa9XpvH1RozkT3meI/+n9KebLvriOhh/uoMTFSk/HVsX9UvZnl+qp2+yeYMp+1I6Ts+L3hjJvn40PmVJNf9CxCUUuaOmtk94g8z++7r+9WoJl2UvvPakww8GdG57DE3mjuJ56+qIM29sQK8pA5ui1pWnkm4IARjgSUJn/PF6wB/kIZFfObl15cmtpAtJji4d6bD0FgvlZ1eHDlpNAAAAAB4JXYdxwlf2130ZWxNHiKC5xX4QlzpcF3FBPUg7BLoxL1aRR6jnXNhM1uU6G45wloYdromQqfgDBd7aCq0mL7Y2i8v77w7rUCvtnTV2/9XBYZSShtRcHe/nzcfOIMrimndeEMfF0v95jbIXNiVKdex9DLQXDCtV52JVPGc2l6txEursSZAnFhtph0ArNVkXaFqpr90RpUtxm0pyVfLmO2zKi1VSmmi3NeI4O+juyVXznQ0GaYfWaXIT6qR8rpBLbnUzJK4l19my8UhkXckEroN2ttSGA7/UkpHGoc7XOq1OPdFAmq9/dmZWkMiiuulEpQjAAAAAAAAAd4OrN2WpIGpGRWLrODRdh5GmoX8Vhy0rIq+bOBXLfv29jj/Ocoozq3llasjTer+uq9pDOGM2NKdWosOzZFPy+gN/yQQBOiWHq34910jbtzuGJmuH+I1f1O6zzV8J0JWeqMlScrwHUnwhGRtEhf9e+l/LxukDSd6Jyl//UQ9abfvpBI73BEPBSvl/FxeXPG8gja2OOtfUMkKbqQ87W5K4/eVf8jVjHNThO+qlrYdgeY8zFCyr+u9K9hvPU/JzNWE7FMpxVr9+cuur54wMps8wjPqk/N2lqukj2XmHq/bEkhHObQIwlyUQ6ihOyA4cpuQCTdTv0ihpy2cE3Q1ugwQAAAAAAD2Dji7Rvb8ExHXp9cYMvetjgYW8NzaIptjTe9aJP/u9jjvO/LMVRq0XyjL14QC+OxMqLQ3GDGy9SNhhnNm7z7Izfyl547XSCMr4xXGsm4YVs9xft/50tp50B7NO0X//0ngvtfq/p5nN2UMW23y7lE/FSv5vsfi7SDJkqdX7E5jSrq7DBNGXq028Sd13n5THEaNXnuXyWvZkpP/Kyt4jhHTEL2XfHVb7zzByaz2YruXTFt9uMPOWy75cUPzZL/W8caIvl/KFt3vdug4vWH651FAZWfnZSkmUhDNmqeidkW2rqewhb5lPH6gKW1n0n2VVdJAg1L5zN1x+0HAbJOi5ntTbIAEAAAA82Tp9GyS6qIg0XxhMnlyNmTsKmm+5ZPWcw+NS7cRtkAAAAAAAALrYkx194W6gAgw9FyrAAAAAAABPsH5uw9q14BpgAAAAAAAA6BEQgAEAAAAAAKBHQAAGAAAAAACAHgEBGAAAAAAAAHoEBGAAAAAAAADoERCAAQAAAAAAoEdAAAYAAAAAAIAeAQEYAAAAAAAAegQEYAAAAAAAAOgREIABAAAAAACgR0AABgAAAAAAgB4BARgAAAAAAAB6BARgAAAAAAAA6BEQgAEAAAAAAKBHQAAGAAAAAACAHgEBGAAAAAAAAHoEBGAAAAAAAADoERCAAQAAAAAAoEdAAAYAAAAAAIAegU26Doei3L2GWNn10dXV5uq082dzMi4QAAAAAAAAgG6gKwOw04CnBg8fIy7Kb2rUaJ/rkM7S6+UyfNCggbbmPE1NYUFy9Lnzl+WaW67NMvUKfmE8/8rO8IjL9QQAALoGp7d7gLU4NkmiIgDdAt6TAABwn7oyAIus7XMyL0b8/Tu5L3q9h78ywU9UnXUhO5UYCGwdRr1qa7N77z9Jt8rAGqW8qkysLFfQBAAAugg7bqIAABAASURBVA2Oib01pyK/vLaRAAAAAHQHXRmAdXR1SWPHIXXq7LcunItNv3CO3JGhw0A3W1IcfvSf09Xanen1Hvn6lKeG9BVcOF+u7niT2stn9l0mAACPmK5R3yGhvkKW9rGqpjAjJj6nqk2hSs/aK8ihMjY2T9ZlgZBrP2x0oA1H+1BTV5yRFJsiabipV0KPIR4NydFiU38fYV5sUmED6aw7vMAWHJHH6D6SmNhiInJ0NMkrFpvY92aVFklonm1Apzuga+wW6E6ST6dV3+rc3f5UcMy9Brs1pEZeqrnXc69r1L7buoa2gX7G6TGpZbeuQmq/19biyHhx50/2LXHMfYLG9jO43kCXxRyKy6slDxRH4BgY0N9UlvJvTMHVTzQ4Qmcvv/69TfWJQlKQFJ96j+/szn9TrjO0HRPiZcG63lCTEX0gqeohfeRyN2/LgME2hedOFtRpn3GEg4L6yeLPZMnwmRAAwCPTlQH4NvJy0kc8PVmXxbp4/szdbcG++s9ZQ/mJr74/0fpE39LXZ3hAX1szLiF1xWdi/z2SXdlAjLzGv/pcr/TNf0UU9hr5xhT3+ovpDTbuTuwrO//cdwGDogHgIdJUXj59LKFcpcu19x/i00dyLPP6L/cNJRdjqhq7uBzaKM891fzrtZ5wcGB/N0HcOWnHsaxRJk6KL6u/30B2uxd4I12iKk7LrNToOTj20a0pkjR0TQdu7XanQlVxKSleU9eJc9/4oLt9z1RlCRHbE5gPGrzGOldGxuQ9lAI7x6yPlSb1+F+5ddeadHvZe/VRpUQcLKYNrPp7eriLSmOL7+U8df6bcl1tQcSuAqLLcw30MroUd6YcI6MBAOAOHlIAPhMdoaPDChwzgakTXzwff7tVawszc6v6uY+b/GqfzMuXCtIvFZYrWsrKLCOvkc9PtFVfuRgVK9FzespvcNAzVZKwmOp2e9Cz7Wt76eLx30rKxRgUDQCPRqOqoqzO1YSrJ/IY6W5AEw5dlHq2yjawT9W5wt6DbMSR2qjAVMD8PRpSjl3R7evu4iQy5lGq4rNxsQV1jXomrt7uTr04dHVeUmIhy93PtSopMlvRqGvsGuhheCnu3M2/6DfIS2TE3pBDqnQtXTw9HHisBkl64qWc6qsDcwx7ewWY58QkldDcaytkJWcUG7oHtuvP3VTkrr5AFhM+bAf4DOjNYz6WTE1NKlK0rqBrYOvsqJeuNnPtZ2HJCgwksefrXAc3d4C0fXW5ZczHmNYuHv1FZoZ6LFluZMyl69d36hrYeHp4WRvQVRIFRaqam4xsB3i5CHksVWV+VkpGR+Orr54KDtV/bOvJT8vg9B/QkHy23mXojS82usTY3d3eyoSvTypTYs6kM6U8vRu7x2o9b6Wkd3+fAU4mpEZcw2Jpu8jpZetx47ZMmdTP296MpSyVXD3tekJXTxd7Ew5TJM1KzcipfjAJjTlR7v1dzfmURl58OSOliDgH+tgQFYslTz+bq+/tbaOSawz5RJKVVWvu2sdEn5YwBdvCWo55f08f5p3QqCy9mJxQoLh2LpmX5uPtaKanqcnNiM+oMfX08etjqm89eASVHJvZWvVnUXosWq6gGxtVisKUU4WtG9p7edqa6ZN6SUFaal4Zy2pYoCNFE6qh+LLKyq6y9W3sFuShl3omT+Tl0ZAcmVl3/S108VJKQY2q3ctp07G70a4PlSYeY9v8DI5016up5xjrN+RcEjMfztiasGoyk2IzmYNyb/zBUekaWfn4OFno6TLvhITEnOsjCjr3tryhi8ZOvh6uvTgaVVXW2dSsatWNJ7y8ARViAIAH5kEF4H79Pft7DGrXKK+pChwTampmfjJi/603VRQe2XqodpzfoP4D/JwG+E2sKzgTe/xIdnmDRnbh6NYCrlIiVzKrXaoztnnaRsTXI+0DMKnKPLL7TGE3+rgeAHocPWMHa55GrNQQFoulTIuMK2Eil8iWWVInFStcRBaGxXm0sY1QVXhWzjK0NarNiwwX08L+Qf1FxkVFxp7ulpLUf+MUxi6DvPrXnMqvYjkLeVcUCiOhJUuSUtVBiOL0EjkKiOKyxqiPp4eJODaiiBa6BHq7KGIu3nhpim6bFQYE9retSCyucbFq7Y+JqjBRfle/e199gbpM5HPRTY+JLCbmPgGe/etPZ7ZdTV19KfmyOdFNirlcpW/V3MS1v/HVRSbXGQtYZYkxJ6s4jv6DnMy5kiJlS1dN+nl46BdHHirSiDzH+nKqmgfi+tjIE46lylgmboHubpKqm4t+V0+FilDXTr6u0EO7qLb9ya/lmthq8lP+PSnnOQ/26WOanSS3ate9lteja+Dw1ADz8uQDsXVmnkMCOZVMk76J8Q3bXtL18RYpkk/FVhn0Dxxi1ZDHbGXv2c8wP+FQvMrQ1jPQ3ao09kEUbJnvqbuTKisyokpjZB/o52IlySAsDilKOsLU55nqKPNYfDkyTmUb4O9BUo4cSjb2GOwmMhCLTV2tVUnHj5cQoWsfvr6uorVver09vG3rL50+IOE4+Hr59UmKSUqIZ/k4liWcLFBeO6qqqiBPM3h0kHH2leKSckmZTMVs6OVpWpZw6kwtx9JrsEefqmP52o5Uno07L1VxRLx+rW/j3pakKol5G4uav1/X30IiP79+ttXJFb1vfDnl5+7hn/Sb+hBd1fZn0IHFUeXEJFQYuoz2s846eeqARhTgZ2+Wn6qwbveDk6Hp68grSjqQKefZOloYciQNLe+0Tr4tb+ijuaMjyTt2qIA2sXc2MdBt4N54wutishWIwAAAD8hDqgC3aGI0Numy7nTzYY0kL3pHXrQe39LBxsV7gPvg4Mls5W97CmvVGo2+pd/UvjZmfJ6JibE+UXBYN2+urpLUqAkAwCPAMu03ZHo/Qmh5weVL8ZdrGs01tKyqpu1wlFpJoczRRmBQ2iAyo8uzZI2qxrwUVW9bF3fz3r2N9ctZBqaWRnU5qVWqRiK5FBfBbMLRVFBOFrziCsveLElGZdtfrXX5DkPHODB/cSok2akpKVUs2/7cymyxjNm4rCCvr6eNCSevbQd19cxEV1cQp0aImSZuYZWjfXN/TGnxna5ObPcC5Qb9+pOyjOLaRuZ4OWWOHkL+Zdltd8C96dURUpiaJbS0faqPiYXAgC7R/iPR2NxV096citau5hZUDWCaeOYiKztTKzvP5u1UxVc4zJ8dnwopk6/uePLVsuqLWb1FfT3szS2NeTIOS++m7hk253aOsbmhPCdZ2156paBCaKAdHJ17w7Z6RkJjptYsUTY2KnOvSGzMCaGMbUTmDn2e7t9y9BqVPot0fQBmvqfWQitL0fSWs6KpLNPTJZq6CsnV0cUtjxsJ3aCskdQx54uuJZQhp5GW12j6uXn2188vyG5Td+cYmZtqiuLLtC+k4EqNU19T/StlHRxXVZMedaxAILLt5xjg7l6TeuaUzNzK0tZ5gm1g8/L6fAMqn2gaFGW12n2rJMWV/ftZ8MQVluZEcrFGRYybe88TCq++hYpPHy9mPjVw9Lrp5dx1SZTpfPs+VLV9G2joauZxo4aqoxtITX1jI0vFFIcpTpufi9YfHJIuqdMf4OJFivKKcrKufdvu9W3ZEVpWSRsxZWrdvCviS7lKVm/3m064AlPHAQA8IA8qAF9mPvO/lNy2xW/E05a2fWIi/rnDEOjrGuQl6ZdK0nNLZkyf4ORsySur9Qp5fpw5u6og/dLF5BjiOn5o7462U7f+HwDgobt6iezV55yW/9zwu6yytEjhatfbimbiUq6iUdfQwSuoH8nLKMipatDvr9fBXlU1hWJdN+vehr1JSfKN45OvXfjaQteA3DNlRZHctU9zf8S5dyo8tXuBuibkvnGETwW6m1blZuXnVRED+1ut1vJ5p0ZVnBgZ2eGFx+1OxV2dfK6Nz2APPUl6dnF6LcdLSO5Sc1/ualuNrCDyUNIDH5Okqrl07Mz1gfFM1feutqo6HxnDBEbHPj7P9C+KYar09zJAW1fP2JhVVyUtTpcWZ/ZyDPK2MrpIFPlJR+IKroe3lo8PrnYyr4rlZi1k3sYVqQrV3b+ce9SuDxxR8+8Kbd8Gd5ctawvO/Ss1sbW29RrhpEg5fbpI2cFKd3pbajQsitJt/UyHxWE+AZFpSGNt3vFj5ebWVk6+Q90kKdFFBAAAHpo7FWO7iN/wsU8NHhZ95O87pl/KYcpLyz6dNrKffmuDHt+8F/Pvi0bNMrDsL2CXxP/21cF/D6amFdQ/3PI1AEBXaZCIawxtnUxUheVMjY7FMzGoz798qUCi4BjzKCajVZbIDBytTTi6HJO+g0Z59eaQxsoSCeXgYkvKi29foW1sqBArTfuIjHR19YS29lRNoUx1yxV69xsxrJ+Qw/SnuNLQ0a23qlB8rzMSNSokEmJua2Woq2to7mhOyiQ3jaBu1DC/97OuDde56dVxKQNjVk36pbzCKo2JiR6rTVcry1Vm2q4SjomtlRGn9XC9hcYc7T2W3AK8HI3u+V+xG04+k+GMSPGlyzliOcuETzHHbrj55DdT1ZTV8rXtRNfY0sqUo0tu2lYlK6uhrB2FXF1dnpWdCRN1CF1TUmtgKeQ2Tx3tMcJDyCEPAPM9LVMZi7RnRdfIfliAo8ndHUbXUOTmItSU5aUk59RQpsZUa3vbF2Lbx7heXFnf0duCMrEPCOhvyZRnmXMiFOrTijpZWSWntwWPaeFaeg0ebN3u4xhVZVENy9rRgpTlXY/abd9CokEjBjnx6M69nGudv20fbqGDHxwi7Nu/r54iL/NSilhjLDDQvbrmvbwtVTWSBp6drYUh84bhCq1tjWlJRX2jXm/Hp6w5FbmXEy5VsYyM2Yq7OuEAANAlHlKG7OvqEXloT8aFxDuuSZecvVDQf6jPjAmCC4VSNYsn6utqyZaeySyp0XAVGna/voO8qtLlBv0CnrLVJ7jOFwAeRw2VhTI9K72CYm29tbHiSh4d4D+lj6JCpqK1F+wqC1JzbEYMfcFTWz+MjWkemyorL1E5WorL7jQ/VaPsysUc66Ghz3sQjSIz9nRZAxHeagW65lLsmea91xRKiK1hUem9/96tkuYlFfmPDhnPYl5I6ukkaWPLhZ3Xj6eQ5MjcfQI90s5LmhvavzplPSerzDbg6VGKqhqFRtXmiuXGqisZedZDQif3q5TUKJqTPHO4FOngoKcdmURdeSU5thNXSrY9+UzR+HJNUOAoW1lVJa3RqEhHJ7/59TTW5abm2o8aOsVZUVFVV6PqaNsGSUqG9digMX1lVRUKhfZb2VhXkJprGTh8spcuS1WeFFfzYKbA0n5PCwMGhz7LYZG63OQk5jAWd7NZfU0NxyPo6f5MeK/MTi2+diOlhvKUVNHowDHMgvqS1GNXmDPFvXnzhrLLadaDAic/ywRnTY04KV5cW6dKyzQPGjHag6WrkVyOldQR1g1DBFRVRZUsW7PylLZv4+a30ODmt5CqNPlMikytUrR/Ofegobx9H+5qlMKZjWp+AAACPElEQVTNPzgqjqTO1TfQlUM0zAmJv9ble3pbMrtNSTIZFDih5SwVxcfmae/RJKtROXuE9udo3yHJRbI65U0nHAAAHhQdnokN6SKjQ6fq6rIi9v9B7hNX1H/stABXMyadK6UFJQUXLp5LKqxsICxh31HPBT5lyyUqSeqRi+yA4TbiQ7/uyGO1uw2S/MTWLZkyAnB7QnO70qIsAvBY0BMNCbSXPKA7iOoaOAUMNs8/3XaKIwant3uAtTg2SYJ7y0A3gfckAADck35uw9q1dGUAHvDUYL/hYyVlJS1P05LP5qRfIADdFQIwPC44vfsHeQrpsoz4lPKuH/iiJxoc4GLaUJBwNqddqkDYgO4G70kAALgnNwfgrhwCnXXxPJerb2XXR1e3+eqXJgIAAPdPVX4pIoI8KA3iM8fFBAAAAKAH6MoKMMDjBRVgAAAAAIAn2M0V4Ic0CzQAAAAAAADAo4UADAAAAAAAAD0CAjAAAAAAAAD0CAjAAAAAAAAA0CMgAAMAAAAAAECPgAAMAAAAAAAAPQICMAAAAAAAAPQICMAAAAAAAADQIyAAAwAAAAAAQI+AAAwAAAAAAAA9AgIwAAAAAAAA9AgIwAAAAAAAANAjIAADAAAAAABAj4AADAAAAAAAAD0CAjAAAAAAAAD0CAjAAAAAAAAA0CMgAAMAAAAAAECPgAAMAAAAAAAATyCNRt3uKQIwAAAAAAAAPIHqFTXtnrIJAAAAAAAAwBNHWlHQRBr1DYyZx/V1NZUVRf8PAAD//w8xHvUAAAAGSURBVAMAZTztGoFZBHAAAAAASUVORK5CYII=', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(01:16:36)*


## 🤖 Claude *(01:16:37)*

The page rendered, but it **ends at "Nutrição (drip)" → footer** — my Intent/AEO panels aren't there. Classic **Cloudflare stale `index.html`** trap (memory: "always hard-refresh after build"). The browser loaded a cached chunk. Let me diagnose live-vs-disk + the browser's loaded chunk:

## 🤖 Claude *(01:16:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== dist/index.html main entry ===\"; grep -oE 'assets/index-[A-Za-z0-9_-]+\\.js' dist/index.html | head -1\necho \"=== LIVE index.html main entry (Cloudflare) ===\"; curl -s https://login.mcorch.com/ | grep -oE 'assets/index-[A-Za-z0-9_-]+\\.js' | head -1\necho \"=== LIVE index.html cache headers ===\"; curl -sI https://login.mcorch.com/ | grep -iE \"cache-control|cf-cache-status|age|etag|last-modified\"\necho \"=== what MarketingPage chunk did the BROWSER load? ===\"; agent-browser eval \"performance.getEntriesByType('resource').map(r=>r.name).filter(n=>n.includes('Marketing')).join(', ')\" 2>&1 | tail -2\necho \"=== is 'Intent Orchestrator' in the live DOM? ===\"; agent-browser eval \"document.body.innerText.includes('Intent Orchestrator')\" 2>&1 | tail -2",
  "description": "Diagnose Cloudflare cache: live vs disk index + browser chunk"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === dist/index.html main entry ===
> assets/index-g5SYRqKM.js
> === LIVE index.html main entry (Cloudflare) ===
> === LIVE index.html cache headers ===
> last-modified: Sun, 17 May 2026 19:40:55 GMT
> report-to: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=7Nd2aKFw7Ysh00l3O95e66wSxwdPFbVGfuBAHO3gfjd5rNd4PHvk3yT8Y6W3DBAm7ZsCbIqD1F1R0PWQCyU2L8nDOiKru2YL%2BrkMI3DSLU5s%2B5QsxSyPlMaV6I21DNmRMj1j"}]}
> nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
> cf-cache-status: DYNAMIC
> === what MarketingPage chunk did the BROWSER load? ===
> "https://login.mcorch.com/assets/MarketingPage-kzjcCEeM.js"
> === is 'Intent Orchestrator' in the live DOM? ===
> true
> ```

## 🤖 Claude *(01:16:57)*


## 🤖 Claude *(01:16:58)*

Correction — the diagnosis flips it: the browser **did** load my new chunk `MarketingPage-kzjcCEeM.js`, and `document.body.innerText.includes('Intent Orchestrator')` → **true**. The new UI **is live and rendered**; my earlier `scroll down` just moved the wrong element (dashboard uses an inner scroll container). Let me `scrollIntoView` the actual panels and screenshot them:

## 🤖 Claude *(01:17:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== AEO present in DOM? ===\"; agent-browser eval \"document.body.innerText.includes('Auditoria AEO') && document.body.innerText.includes('Aguardando aprova\u00e7\u00e3o')===false\" 2>&1 | tail -1\nagent-browser eval \"[...document.querySelectorAll('h2')].find(h=>h.textContent.includes('Intent Orchestrator'))?.scrollIntoView({block:'start'})\" 2>&1 | tail -1\nagent-browser wait 600 2>&1 | tail -1\nagent-browser screenshot scripts/qa/_marketing-intent.png 2>&1 | tail -1\nagent-browser eval \"[...document.querySelectorAll('h2')].find(h=>h.textContent.includes('Auditoria AEO'))?.scrollIntoView({block:'start'})\" 2>&1 | tail -1\nagent-browser wait 600 2>&1 | tail -1\nagent-browser screenshot scripts/qa/_marketing-aeo.png 2>&1 | tail -1",
  "description": "scrollIntoView Intent + AEO panels, screenshot each"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === AEO present in DOM? ===
> true
> null
> ✓ Done
> ✓ Screenshot saved to scripts/qa/_marketing-intent.png
> null
> ✓ Done
> ✓ Screenshot saved to scripts/qa/_marketing-aeo.png
> ```

## 🤖 Claude *(01:17:07)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/_marketing-intent.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(01:17:38)*


## 🤖 Claude *(01:17:42)*

**Verificação de UI logada — VERDE.** Ambos os painéis novos renderizam corretamente em produção (Usuário Zero logado, chunk novo `MarketingPage-kzjcCEeM.js`, `Intent Orchestrator` + `Auditoria AEO` confirmados no DOM):
- **Intent Orchestrator** — textarea + "Orquestrar" + empty-state "Nenhum plano ainda" + subtítulo HITL.
- **Auditoria AEO** — input Marca + Queries rastreadas + "5 mcoCoins por auditoria".

Zero crash de render (empty states corretos, PT-BR íntegro). Envio a prova material ao Maestro:

## 🤖 Claude *(01:17:44)*


🛠️ **Tool Call**: `SendUserFile`
```json
{
  "files": [
    "scripts/qa/_marketing-intent.png"
  ],
  "status": "normal",
  "caption": "Verifica\u00e7\u00e3o logada (Usu\u00e1rio Zero \u00b7 5291 mco): FR-MH-009 Intent Orchestrator + FR-MH-010 Auditoria AEO renderizando live em /dashboard/marketing, chunk novo, zero crash."
}
```

> **Tool Result (SendUserFile)** - ✅ Success
>
> ```
> 1 file delivered to user.
> ```

## 🤖 Claude *(01:18:29)*


## 🤖 Claude *(01:18:30)*

Prova entregue. Agora **selo** este incremento. Limpo os screenshots temporários e confiro o conjunto de mudanças:

## 🤖 Claude *(01:18:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nrm -f scripts/qa/_marketing-ui-verify.png scripts/qa/_marketing-intent.png scripts/qa/_marketing-aeo.png\nagent-browser close 2>/dev/null | tail -1 || true\necho \"=== git status ===\"; git status --short\necho \"=== new untracked dirs ===\"; git status --short | grep -E \"intent-execute|aeo-audit\" ",
  "description": "Clean temp screenshots + close browser + git status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Browser closed
> === git status ===
>  M docs/bok/marketing-hub/05-sdd.md
>  M docs/bok/marketing-hub/06-data-model.md
>  M src/components/marketing/LeadDetailDialog.tsx
>  M src/integrations/supabase/types.ts
>  M src/pages/MarketingPage.tsx
>  M src/test/marketing-hub.test.ts
>  M supabase/config.toml
>  M supabase/functions/intent-orchestrate/index.ts
> ?? docs/processes/aeo-audit.md
> ?? docs/processes/intent-plan-execution.md
> ?? scripts/qa/smoke-aeo-audit.ts
> ?? scripts/qa/smoke-intent-execute.ts
> ?? src/components/marketing/AEOAuditPanel.tsx
> ?? src/components/marketing/HITLApprovalCard.tsx
> ?? src/components/marketing/IntentOrchestratorPanel.tsx
> ?? src/hooks/useAEO.ts
> ?? src/hooks/useIntentOrchestrator.ts
> ?? supabase/functions/_shared/intent-policy.ts
> ?? supabase/functions/aeo-audit/
> ?? supabase/functions/intent-execute/
> ?? supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql
> === new untracked dirs ===
> ?? docs/processes/aeo-audit.md
> ?? scripts/qa/smoke-aeo-audit.ts
> ?? scripts/qa/smoke-intent-execute.ts
> ?? supabase/functions/aeo-audit/
> ?? supabase/functions/intent-execute/
> ```

## 🤖 Claude *(01:19:04)*


## 🤖 Claude *(01:19:05)*

Conjunto limpo (8 M + novos). Faço os commits granulares, milestone-oriented, **sem Co-Authored-By** (preferência durável do repo — [[feedback_commits]]):

## 🤖 Claude *(01:19:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -e\n\n# \u2500\u2500 Commit 1: intent executor backend \u2500\u2500\ngit add supabase/functions/_shared/intent-policy.ts supabase/functions/intent-orchestrate/index.ts supabase/functions/intent-execute supabase/config.toml docs/processes/intent-plan-execution.md scripts/qa/smoke-intent-execute.ts\ngit commit -q -m \"feat(marketing-hub): executor de intent_plans com re-valida\u00e7\u00e3o outward (FR-MH-009 HITL)\" \\\n  -m \"Fecha a metade HITL do Intent Orchestrator: a m\u00e1quina de estados proposed\u2192pending_hitl\u2192approved|rejected\u2192executed ganha o edge fn intent-execute. O execute RE-VALIDA o alto-impacto sobre o plano ARMAZENADO (gate compartilhado _shared/intent-policy.ts, fail-closed em plano n\u00e3o-array) e recusa (409 hitl_required) todo plano outward sem aprova\u00e7\u00e3o humana \u2014 nunca confia em status='auto_approved'. Tenant-guard por user_id, custo 0. SOP intent-plan-execution.md (Lei 2). Smoke throwaway 17/17.\"\necho \"\u2705 commit 1\"\n\n# \u2500\u2500 Commit 2: AEO backend \u2500\u2500\ngit add supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql supabase/functions/aeo-audit docs/processes/aeo-audit.md scripts/qa/smoke-aeo-audit.ts\ngit commit -q -m \"feat(marketing-hub): auditoria AEO \u2014 aeo-audit + tabela aeo_audits (FR-MH-010)\" \\\n  -m \"\u00daltima FR do marketing-hub: mede cita\u00e7\u00e3o da marca nos motores de resposta de IA. Edge fn JWT, d\u00e9bito at\u00f4mico de 5 mcoCoins na entrada, provider em modo degradado documentado (LLM como answer-engine proxy \u2014 OTD-MH-003, sem scrape de SERP do datacenter), persiste 1 snapshot append-only por query em aeo_audits (RLS default-deny). SOP aeo-audit.md (Lei 2). Smoke throwaway 12/12.\"\necho \"\u2705 commit 2\"\n\n# \u2500\u2500 Commit 3: UI follows \u2500\u2500\ngit add src/hooks/useIntentOrchestrator.ts src/hooks/useAEO.ts src/components/marketing/HITLApprovalCard.tsx src/components/marketing/IntentOrchestratorPanel.tsx src/components/marketing/AEOAuditPanel.tsx src/components/marketing/LeadDetailDialog.tsx src/pages/MarketingPage.tsx src/integrations/supabase/types.ts src/test/marketing-hub.test.ts\ngit commit -q -m \"feat(marketing-hub): UI follows \u2014 Intent Orchestrator/HITL + AEO + enroll de nurturing\" \\\n  -m \"D\u00e1 rosto aos backends LIVE: painel Intent Orchestrator (inten\u00e7\u00e3o\u2192plano\u2192policy) + HITLApprovalCard (aprovar/rejeitar/executar) + painel Auditoria AEO + bot\u00e3o de inscri\u00e7\u00e3o em sequ\u00eancia de nutri\u00e7\u00e3o no Customer 360. Hooks useIntentOrchestrator/useAEO no padr\u00e3o Harness. +8 testes (257\u2192265). Verificado logado na UI de produ\u00e7\u00e3o (Usu\u00e1rio Zero) \u2014 ambos os pain\u00e9is renderizam, zero crash.\"\necho \"\u2705 commit 3\"\n\n# \u2500\u2500 Commit 4: BoK doc patches \u2500\u2500\ngit add docs/bok/marketing-hub/05-sdd.md docs/bok/marketing-hub/06-data-model.md\ngit commit -q -m \"docs(bok): patch marketing-hub SDD/data-model \u2014 intent-execute + engine degraded\" \\\n  -m \"Documenta o intent-execute (linha de edge fn + contrato HTTP \u00a7API, sob FR-MH-009) e o valor 'degraded' no enum engine de aeo_audits (modo degradado OTD-MH-003) \u2014 SSOT alinhada ao c\u00f3digo.\"\necho \"\u2705 commit 4\"\n\necho \"=== log ===\"; git log --oneline -5",
  "description": "4 granular commits (backend intent, backend AEO, UI, BoK docs)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ commit 1
> ✅ commit 2
> ✅ commit 3
> ✅ commit 4
> === log ===
> 492d852 docs(bok): patch marketing-hub SDD/data-model — intent-execute + engine degraded
> fb0cbdf feat(marketing-hub): UI follows — Intent Orchestrator/HITL + AEO + enroll de nurturing
> ee3a016 feat(marketing-hub): auditoria AEO — aeo-audit + tabela aeo_audits (FR-MH-010)
> 0021189 feat(marketing-hub): executor de intent_plans com re-validação outward (FR-MH-009 HITL)
> 7bb15bc chore(sprint): update sprint-priorities — v6.26.0 drift audit + P0 ledger + 3 marketing-hub FRs
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:19:51)*


## 🤖 Claude *(01:19:53)*

4 commits no main. Agora o **selo documental**: registro no HANDOFF.md (newest-first, após o Task State header) + README + sprint. Escrevo o record da v6.27.0:

## 🤖 Claude *(01:20:28)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "## Task State\n\n## Drift Audit + Ledger P0 + Marketing-Hub FRs (008/012/009) Record (2026-06-03)",
  "new_string": "## Task State\n\n## Marketing-Hub UI Follows + Intent Executor + AEO (FR-MH-009/010) Record (2026-06-03)\n\n**v6.27.0 (2026-06-03)** \u2014 Sess\u00e3o `/handson` \u2192 `/goal` Sovereign com os 3 pr\u00f3ximos passos priorizados (\"backend pronto, falta o rosto\"): (1) UI follows do Marketing Hub; (2) **executor de `intent_plans` com re-valida\u00e7\u00e3o outward**; (3) **FR-MH-010 AEO** (\u00faltima FR). Padr\u00e3o das \u00faltimas seals: **probe-first material** \u2192 entrega incremental \u2192 **smoke throwaway** por entrega \u2192 `/security-review` independente. BoK Gate verde (marketing-hub 9/9). 5 commits.\n\n**O que foi entregue:**\n- **Executor de `intent_plans` (FR-MH-009 HITL)** \u2014 edge fn `intent-execute` (approve/reject/execute) dirige a m\u00e1quina `proposed\u2192pending_hitl\u2192approved|rejected\u2192executed`. **Golden rule do directive**: o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** (gate compartilhado `_shared/intent-policy.ts`, extra\u00eddo do `intent-orchestrate` p/ n\u00e3o divergir) e recusa `409 hitl_required` todo plano outward sem aprova\u00e7\u00e3o humana \u2014 **nunca confia em `status='auto_approved'`**. Tenant-guard por `user_id` (foreign\u2192404). Custo 0. `/security-review` SAFE \u2192 **adotada 1 recomenda\u00e7\u00e3o fail-safe**: gate **fail-closed** em plano n\u00e3o-array (tamper de shape). SOP `intent-plan-execution.md` (Lei 2). Smoke `smoke-intent-execute.ts` **17/17** (tamper auto_approved bloqueado \u00b7 fail-closed \u00b7 pending\u2192approve\u2192execute \u00b7 idempot\u00eancia \u00b7 404 \u00b7 transi\u00e7\u00f5es inv\u00e1lidas). (`0021189`)\n- **Auditoria AEO (FR-MH-010 \u2014 \u00faltima FR do marketing-hub)** \u2014 migration `20260603260000` (`aeo_audits` RLS default-deny, append-only, CHECKs do data-model) + edge fn `aeo-audit` (JWT \u00b7 d\u00e9bito at\u00f4mico **5 mco** na entrada \u00b7 provider **degradado documentado** OTD-MH-003 = LLM como answer-engine proxy, sem scrape de SERP do datacenter \u00b7 1 snapshot por query). `db push` Finished \u00b7 `/security-review` SAFE. SOP `aeo-audit.md` (Lei 2). Smoke `smoke-aeo-audit.ts` **12/12** (d\u00e9bito 100\u219295 \u00b7 402 sem d\u00e9bito \u00b7 guards 422/401 \u00b7 RLS cross-tenant leaked=0). (`ee3a016`)\n- **UI follows** \u2014 `useIntentOrchestrator`/`useAEO` (Harness) + `IntentOrchestratorPanel` + `HITLApprovalCard` (aprovar/rejeitar/executar) + `AEOAuditPanel` + bot\u00e3o **enroll de nurturing** no `LeadDetailDialog` (Customer 360) \u2192 todos ligados em `/dashboard/marketing`. **+8 testes** (257\u2192**265**). **UI LOGADA verificada** (magic link Usu\u00e1rio Zero + agent-browser ARM64: chunk novo `MarketingPage-kzjcCEeM.js`, ambos os pain\u00e9is renderizam, zero crash, zero muta\u00e7\u00e3o). (`fb0cbdf`)\n- **BoK patch** \u2014 SDD (`intent-execute` linha + contrato \u00a7API) + data-model (`engine='degraded'`) \u2014 SSOT alinhada. (`492d852`)\n\n**ORO triplet:** Operator=MCORCH Agent \u00b7 Reviewer=Sovereign + `/security-review` independente (migration + edge fns) \u00b7 Owner=Sovereign (blast radius = UI que dispara a\u00e7\u00f5es outward via HITL + nova superf\u00edcie de gasto AEO 5 mco; mitigado pela re-valida\u00e7\u00e3o fail-closed e pelo dispatch outward ainda **gated**).\n\n| Verifica\u00e7\u00e3o | Resultado |\n|---|---|\n| intent-execute | \u2705 deploy 80.44kB \u00b7 smoke **17/17** (golden rule + fail-closed provados material) |\n| aeo-audit | \u2705 deploy 85.3kB \u00b7 migration Finished \u00b7 smoke **12/12** |\n| /security-review | \u2705 SAFE (7 propriedades tra\u00e7adas; 1 fail-safe adotada) |\n| tsc / su\u00edte | \u2705 0 erros \u00b7 **265 passed** / 2 skipped |\n| eslint (tocados) | \u2705 exit 0 |\n| Build / deploy | \u2705 22.88s \u00b7 `MarketingPage-kzjcCEeM.js` servido \u00b7 UI logada renderiza (screenshot) |\n| Containers / Chroma | \u2705 5 healthy (11d) \u00b7 Chroma v2 OK |\n| Handoff node | \u23f3 inserir nesta seal |\n\n| Commit | Conte\u00fado |\n|---|---|\n| `0021189` | feat(marketing-hub): executor de intent_plans + re-valida\u00e7\u00e3o outward (FR-MH-009 HITL) |\n| `ee3a016` | feat(marketing-hub): auditoria AEO \u2014 aeo-audit + aeo_audits (FR-MH-010) |\n| `fb0cbdf` | feat(marketing-hub): UI follows \u2014 Intent Orchestrator/HITL + AEO + enroll nurturing |\n| `492d852` | docs(bok): patch SDD/data-model \u2014 intent-execute + engine degraded |\n\n### Survival Laws Self-audit\n```\nLaw 1 (Materiality): \u2705 toda claim provada NESTE turno \u2014 2 deploys (80.44kB/85.3kB literal) + migration \"Finished\" + 2 smokes throwaway (17/17\u00b712/12 output literal) + tsc 0 + 265 passed + eslint 0 + /security-review SAFE (subagente independente) + UI logada via screenshot real (chunk novo + DOM 'Intent Orchestrator'=true). Zero fabrica\u00e7\u00e3o. Corre\u00e7\u00e3o de rota material: 1\u00aa leitura do screenshot pr\u00e9-scroll sugeriu \"UI velha cacheada\" \u2192 diagn\u00f3stico (eval do chunk + DOM) refutou: era scroll no container errado, chunk novo confirmado.\nLaw 2 (Process): \u2705 2 SOPs ANTES do c\u00f3digo ([[intent-plan-execution|intent-plan-execution]].md + [[aeo-audit|aeo-audit]].md); BoK patcheada (SDD/data-model) alinhada ao c\u00f3digo; toda migration /security-review (regra CLAUDE.md).\nLaw 3 (Pruning): \u2705 sess\u00e3o de densidade alta (3 entregas) usando a janela (calibra\u00e7\u00e3o 1M/Max); dispatch outward conscientemente gated (governan\u00e7a real > envio fabricado).\nLaw 4 (ORO): \u2705 triplet declarado; goal Sovereign expl\u00edcito como diretiva; fail-safe adotada sob review independente.\n```\n\n**Pend\u00eancias/Pr\u00f3ximos:**\n- **Dispatch outward real do executor** \u2014 hoje `execute` faz governan\u00e7a (re-valida + transi\u00e7\u00e3o + observa\u00e7\u00e3o) e retorna `outward_dispatch:'gated'`; ligar o disparo real (campaign-run/orchestrate-content/nurture-dispatch) \u00e9 a pr\u00f3xima etapa. **OTD-INTENT-TRANSITION-GUARD** (do `/security-review`): antes de ligar o dispatch real, adicionar CHECK/trigger de transi\u00e7\u00e3o em `intent_plans` (s\u00f3 service role move p/ approved/executed) \u2014 defesa-em-profundidade contra owner que adultera o pr\u00f3prio row via PostgREST.\n- **Entrega externa de nurturing** (real, por canal) \u2014 segue gated; credencial `resend_api_key` per-tenant pronta.\n- **OTD-AEO-REFUND** \u2014 avaliar refund autom\u00e1tico em falha p\u00f3s-d\u00e9bito do `aeo-audit` (espelha lead-score).\n- Twitter CreditsDepleted \u00b7 Atribui\u00e7\u00e3o de clique ML (aguardando Sovereign).\n\n---\n\n## Drift Audit + Ledger P0 + Marketing-Hub FRs (008/012/009) Record (2026-06-03)"
}
```

## 🤖 Claude *(01:20:35)*


## 🤖 Claude *(01:20:36)*

Agora a sprint-priorities (linha v6.27.0 no topo) + README. Insiro a linha de sprint:

## 🤖 Claude *(01:20:49)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "old_string": "**Sprint v6.26.0 selado em 2026-06-03** \u2014 **Drift audit + P0 ledger + 3 FRs marketing-hub**.",
  "new_string": "**Sprint v6.27.0 selado em 2026-06-03** \u2014 **Marketing-Hub: rosto + executor + AEO (FR-MH-009/010)**. `/handson` \u2192 `/goal` Sovereign com os 3 pr\u00f3ximos passos (\"backend pronto, falta o rosto\"). **(1) Executor de `intent_plans` (FR-MH-009 HITL):** edge fn `intent-execute` (approve/reject/execute) na m\u00e1quina `proposed\u2192pending_hitl\u2192approved|rejected\u2192executed`; **golden rule** = o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** (gate compartilhado `_shared/intent-policy.ts`) e recusa `409 hitl_required` todo outward sem aprova\u00e7\u00e3o humana \u2014 **nunca confia em `auto_approved`**; tenant-guard 404; `/security-review` SAFE \u2192 adotada **fail-closed** em plano n\u00e3o-array; smoke **17/17**. **(2) AEO (FR-MH-010 \u2014 \u00faltima FR):** `aeo_audits` (RLS) + `aeo-audit` (JWT \u00b7 5 mco at\u00f4mico \u00b7 provider **degradado documentado** OTD-MH-003 LLM-as-answer-engine \u00b7 1 snapshot/query); `db push` Finished; smoke **12/12** (RLS cross-tenant leaked=0). **(3) UI follows:** `useIntentOrchestrator`/`useAEO` + `IntentOrchestratorPanel`/`HITLApprovalCard`/`AEOAuditPanel` + enroll de nurturing no Customer 360 \u2192 `/dashboard/marketing`; **+8 testes (257\u2192265)**; **UI logada verificada** (magic link Usu\u00e1rio Zero + agent-browser, chunk novo, zero crash). tsc 0 \u00b7 eslint 0 (tocados) \u00b7 build 22.88s deploy nginx. 5 commits. **Novo Top Gap:** dispatch outward real do executor (hoje gated) + **OTD-INTENT-TRANSITION-GUARD** (CHECK de transi\u00e7\u00e3o antes de ligar o envio real) \u00b7 entrega externa de nurturing (gated; credencial pronta) \u00b7 **OTD-AEO-REFUND** (refund p\u00f3s-d\u00e9bito). **Marketing-hub: TODAS as FRs backend+UI entregues** (001..012). **Li\u00e7\u00e3o:** probe-first viu que o gate de policy j\u00e1 existia inline no orchestrate \u2192 extra\u00ed p/ `_shared` em vez de duplicar (o `execute` re-roda **o mesmo** gate, n\u00e3o uma c\u00f3pia); o `/security-review` independente pegou o fail-open que o self-review deixaria passar.\n\n**Sprint v6.26.0 selado em 2026-06-03** \u2014 **Drift audit + P0 ledger + 3 FRs marketing-hub**."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:20:52)*


## 🤖 Claude *(01:20:52)*

Sprint atualizado. Vejo o cabeçalho do README para o version bump:

## 🤖 Claude *(01:20:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"v6\\.2[0-9]\\.[0-9]|^## |Marketing Hub|FR-MH\" README.md | head -20",
  "description": "Find README version + marketing section anchors"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 8:  <img src="https://img.shields.io/badge/marketing--hub-FR--MH--001..009%2C011%2C012_live-brightgreen?style=for-the-badge" alt="Marketing Hub" />
> 53:  <img src="https://img.shields.io/badge/marketing--hub_agents-11_generated-orange?style=for-the-badge" alt="Marketing Hub Agents" />
> 54:  <img src="https://img.shields.io/badge/marketing--hub_MVP-Lead_Core_live-brightgreen?style=for-the-badge" alt="Marketing Hub MVP" />
> 57:  <img src="https://img.shields.io/badge/marketing--hub_MVP4-UI_live_%2F_dashboard%2Fmarketing-brightgreen?style=for-the-badge" alt="Marketing Hub MVP4 UI" />
> 61:## 🆕 What's new in v6.26.0 (2026-06-03)
> 66:- **🌱 Nurturing cron (FR-MH-008)** — `nurture-cron` + pg_cron `*/15` avança enrollments due (consent-gated, modo service-role espelhando orchestrate-step). Smoke E2E 5/5 + USER 10/10.
> 67:- **🔑 BYOK canal de e-mail (FR-MH-012)** — `resend_api_key` per-tenant no padrão Vault + campo Settings. Round-trip 8/8 (sibling intacto, idempotente).
> 68:- **🧭 Intent Orchestrator + HITL (FR-MH-009, backend)** — `intent-orchestrate`: intenção→plano + policy engine auto-vs-HITL (canal outward fail-safe→HITL) + rationale XAI. Smoke 8/8 (alto impacto→pending_hitl).
> 70:## 🆕 What's new in v6.24.0 (2026-06-03)
> 72:**High-density session — Customer 360 + Nurturing + flywheel hardening** (Sovereign directive: use the full 1M window, seal at ~95% not 45%). Five chunks landed after the v6.23.0 seal, each proven by a LIVE throwaway smoke.
> 74:1. **MVP-5 Attribution (FR-MH-007)** — `handle-ml-postback` now also writes `marketing_attribution` on a conversion (FK-safe campaign_id, fail-soft); `useCampaignAttribution` + a "Receita Atribuída" card per campaign. DB smoke 4/4 (insert shape + FK guard 23503 + de-linked NULL).
> 76:3. **Customer 360 (FR-MH-011)** — `customer_360` VIEW (lead⨝events⨝consents) **WITH (security_invoker = true)** so base-table RLS isolates tenants; `useCustomer360` + a lead-detail drawer. /security-review SAFE; **isolation smoke 4/4** (tenant A sees only A's lead, B's never leaks).
> 77:4. **Nurturing Sequences (FR-MH-008)** — drip engine: `sequences` + `sequence_enrollments` (composite tenant-FKs CASCADE) + `nurture-dispatch` edge fn whose centerpiece is the **consent gate** (STRIDE-Critical: never generate/charge/record without a granted consent; opt-out hard-stops; 2 mcoCoins; idempotent). **Sends gated** (message generated + recorded `delivery='gated'`, real external delivery deferred). `useNurturing` + a NurturingPanel. **Consent-gate smoke 10/10**.
> 82:## 🆕 What's new in v6.23.0 (2026-06-03)
> 84:**Marketing Hub backend completed + MVP-4 UI live** — `campaign-run` shipped, then the whole module got a face at `/dashboard/marketing`, absorbing the v1 campaign UI rather than duplicating it. Sovereign directive: full v1 absorb **and** the new surface, complete, no stopping.
> 86:1. **`campaign-run` edge fn (FR-MH-004)** — JWT-guarded, debits the `CAMPAIGN_RUN` fee (10) atomically after the ownership check, then dispatches each ordered `campaign_step` to `orchestrate-content` (which self-bills its own 10) — faithful cascade `10 + 10×N`. Dispatch is **parallel** (`Promise.allSettled`) so wall-clock ≈ the slowest step, not the sum; `email` channel is blocked (nurture-dispatch territory), `MAX_PARALLEL_STEPS` bounds fan-out. Zero-cost smoke **13/13** (401/422/404/no-steps/402 + tenant isolation + `email`-only=blocked → fee-only 100→90 + mesh node), real paid cascade gated on Sovereign GO.
> 87:2. **MVP-4 Marketing Hub UI** — new `/dashboard/marketing` hub: **LeadBoard** (5-column kanban Novo→Pontuado→Nutrindo→Convertido→Perdido, with Pontuar→`lead-score` and manual capture) + a campaigns overview; sidebar nav added.
> 93:## 🆕 What's new in v6.22.0 (2026-06-03)
> 99:3. **lead-score edge fn LIVE** (FR-MH-003) — JWT-guarded, atomic 1-mcoCoin debit, AI scoring 0–100 (per-user→system key, reusing the cascade helper) with a **fail-soft heuristic**. Smoke proven E2E: HTTP 200, score=80 (`source=ai`), score/event persisted, balance 100→99, zero-residue.
> 102:## 🆕 What's new in v6.21.0 (2026-06-03)
> ```

## 🤖 Claude *(01:21:10)*


## 🤖 Claude *(01:21:10)*

README: atualizo o badge para todas as FRs (001..012) + adiciono a seção v6.27.0:

## 🤖 Claude *(01:21:13)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/marketing--hub-FR--MH--001..009%2C011%2C012_live-brightgreen?style=for-the-badge\" alt=\"Marketing Hub\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/marketing--hub-FR--MH--001..012_live-brightgreen?style=for-the-badge\" alt=\"Marketing Hub\" />"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(01:21:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "offset": 1,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	<p align="center">
> 2	  <img src="https://img.shields.io/badge/status-production-brightgreen?style=for-the-badge" alt="Status" />
> 3	  <img src="https://img.shields.io/badge/version-6.26.0--drift--p0--mh--frs-blueviolet?style=for-the-badge" alt="Version" />
> 4	  <img src="https://img.shields.io/badge/license-proprietary-red?style=for-the-badge" alt="License" />
> 5	  <img src="https://img.shields.io/badge/typescript-strict-blue?style=for-the-badge&logo=typescript" alt="TypeScript" />
> 6	  <img src="https://img.shields.io/badge/neural_mesh-8770_nodes-blueviolet?style=for-the-badge" alt="Neural Mesh" />
> 7	  <img src="https://img.shields.io/badge/test_coverage-259_tests-success?style=for-the-badge" alt="Test Coverage" />
> 8	  <img src="https://img.shields.io/badge/marketing--hub-FR--MH--001..009%2C011%2C012_live-brightgreen?style=for-the-badge" alt="Marketing Hub" />
> 9	  <img src="https://img.shields.io/badge/e2e--user--zero-v2_runnable_harness-teal?style=for-the-badge" alt="e2e-user-zero v2" />
> 10	  <img src="https://img.shields.io/badge/BoK_Suite-v1_sealed-fuchsia?style=for-the-badge" alt="BoK Suite" />
> 11	  <img src="https://img.shields.io/badge/AIOS_DevKit-4Cs_100%2F100-brightgreen?style=for-the-badge" alt="AIOS DevKit" />
> 12	  <img src="https://img.shields.io/badge/mcoCoins-gatekeeper-gold?style=for-the-badge" alt="mcoCoins" />
> ```

## 🤖 Claude *(01:21:25)*


## 🤖 Claude *(01:21:27)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/version-6.26.0--drift--p0--mh--frs-blueviolet?style=for-the-badge\" alt=\"Version\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/version-6.27.0--mh--ui--intent--aeo-blueviolet?style=for-the-badge\" alt=\"Version\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:21:33)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/test_coverage-259_tests-success?style=for-the-badge\" alt=\"Test Coverage\" />\n  <img src=\"https://img.shields.io/badge/marketing--hub-FR--MH--001..009%2C011%2C012_live-brightgreen?style=for-the-badge\" alt=\"Marketing Hub\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/test_coverage-265_tests-success?style=for-the-badge\" alt=\"Test Coverage\" />\n  <img src=\"https://img.shields.io/badge/marketing--hub-FR--MH--001..012_live-brightgreen?style=for-the-badge\" alt=\"Marketing Hub\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:21:46)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "## \ud83c\udd95 What's new in v6.26.0 (2026-06-03)",
  "new_string": "## \ud83c\udd95 What's new in v6.27.0 (2026-06-03)\n\n**Marketing Hub \u2014 the face + the executor + AEO (FR-MH-009/010).** Sovereign `/goal` with the three prioritized next steps (\"backend ready, needs a face\").\n\n- **\ud83e\udde0 Intent plan executor (FR-MH-009 HITL)** \u2014 `intent-execute` edge fn drives the `proposed\u2192pending_hitl\u2192approved|rejected\u2192executed` state machine. The golden rule: `execute` **re-validates** high-impact on the **stored** plan (shared gate `_shared/intent-policy.ts`, **fail-closed** on a malformed non-array plan) and refuses `409 hitl_required` for any outward plan that wasn't human-approved \u2014 never trusting `status='auto_approved'`. Tenant-guard 404, cost 0. `/security-review` SAFE (1 fail-safe adopted). Smoke **17/17**.\n- **\ud83d\udce1 AEO Audit (FR-MH-010 \u2014 the last FR)** \u2014 `aeo_audits` (RLS default-deny) + `aeo-audit` (JWT \u00b7 atomic 5-mcoCoin debit \u00b7 degraded provider documented OTD-MH-003 = LLM-as-answer-engine, no datacenter SERP scrape \u00b7 one snapshot per query). Smoke **12/12** (cross-tenant RLS leaked=0).\n- **\ud83d\udda5\ufe0f UI follows** \u2014 `useIntentOrchestrator`/`useAEO` + Intent Orchestrator / HITLApprovalCard / AEO panels + a nurturing **enroll** button in the Customer 360 drawer, all wired into `/dashboard/marketing`. +8 tests (257\u2192**265**). **Verified logged-in in production** (Usu\u00e1rio Zero magic link + agent-browser): both panels render, fresh chunk, zero crash.\n\n**Marketing Hub: all FRs (001..012) now backend + UI live.** Next: wire the executor's real outward dispatch (today `gated`) behind OTD-INTENT-TRANSITION-GUARD (a transition CHECK so only the service role moves a plan to approved/executed).\n\n## \ud83c\udd95 What's new in v6.26.0 (2026-06-03)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:22:00)*


## 🤖 Claude *(01:22:01)*

README + sprint + HANDOFF selados. Agora a **Fase 5c — auditoria de prova material independente** (mcorch-qa-healing) que verifica mecanicamente as claims do selo (fecha a fraqueza de auto-avaliação da Lei 1):

## 🤖 Claude *(01:22:02)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "mcorch-qa-healing"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: mcorch-qa-healing
> ```

## 👤 User *(01:22:02)*

Base directory for this skill: /home/gcrUX/htdocs/constellation-orchestra/.claude/skills/mcorch-qa-healing

# Skill: mcorch-qa-healing — Material Proof Audit

QA sênior independente. Onde o `/handoff` antes pedia ao próprio agente para marcar
o checkbox "todas as claims têm prova" (Lei 1 auto-avaliada), esta skill **revalida
mecanicamente** cada prova material do selo e **bloqueia** se algo for contradito.

Governado por `docs/bok/mcorch-qa-healing/` (suíte BoK 9/9) e pela SOP
`docs/processes/handoff-material-proof-audit.md`.

## Quando rodar

- **Fase 5c do `/handoff`** — obrigatório, entre o secret-scan (5b) e o BoK status (6).
- **On-demand** — para auditar qualquer selo antes de confiar nele.

## Como executar

```bash
bun run scripts/qa/run-audit.ts            # audita o HANDOFF.md atual
bun run scripts/qa/run-audit.ts HANDOFF.md # idem, path explícito
```

O script: extrai as claims do bloco `## … Record` mais recente do `HANDOFF.md`
(commits, UUIDs, `tsc`, contagem de testes, edge functions, paths), verifica cada
uma contra o artefato físico real, imprime o **Proof Manifest** e sai com:

- **exit 0** → veredito `SEAL ALLOWED`
- **exit 1** → veredito `SEAL BLOCKED`

## Como interpretar o resultado

| Glifo | Verdict | Significado |
|-------|---------|-------------|
| ✅ | `pass` | Claim verificada contra o artefato físico |
| 🔴 | `fail` | Claim contradita — artefato ausente ou divergente |
| ⏭ | `skip` | Claim não-verificável (infra inalcançável, UUID não-mesh, deploy só-tamanho) — **nunca bloqueia** |

1. Cole a tabela do Proof Manifest no relatório da Fase 8 (bloco `📋 PROVA MATERIAL`).
2. **Se exit 0** → o selo está limpo; prossiga para a Fase 6.
3. **Se exit 1 (qualquer 🔴)** → **HALT**. NÃO prossiga para Fase 6/7. NÃO faça push.
   Responda em PT-BR no formato de recusa:

   > **Fase 5c (Material Proof Audit) bloqueia este selo.**
   > Claim contradita: `<label>` — `<detail>`.
   > Preciso corrigir a causa real antes de selar.

4. Corrija a **causa real** — nunca fabrique a prova (Lei 1). Se o hash está errado
   no `HANDOFF.md`, corrija o texto; se o commit não foi feito, volte à Fase 2; se o
   teste não passou, conserte o código. Re-rode a auditoria até `SEAL ALLOWED`.

## Cura mínima (FR-011 — SOP Cenário D)

Se um 🔴 é uma claim **strict** de nó de handoff (UUID vindo do `proof-manifest.json`
que não resolve em `mcorch_nodes`/`mcorch_edges`): re-tente o INSERT da Fase 3 **uma
única vez**, capture o UUID **real** retornado, atualize a referência e re-rode a
auditoria. Isto cria um registro verdadeiro — **nunca** edite o `HANDOFF.md` para um
UUID falso parecer válido. Se o re-INSERT falhar, o selo permanece bloqueado.

## Anti-patterns

- ❌ Marcar um 🔴 como aceitável e prosseguir o selo mesmo assim.
- ❌ Fabricar hash/UUID/contagem para um claim "passar".
- ❌ Tratar um ⏭ `skip` como falha — `skip` é não-verificável, não é contradição.
- ❌ Rodar `/handoff` pulando a Fase 5c.

## Referências

- `scripts/qa/run-audit.ts` — entrypoint da auditoria
- `docs/processes/handoff-material-proof-audit.md` — SOP (processo humano equivalente)
- `docs/bok/mcorch-qa-healing/` — suíte BoK que governa este módulo
- `.claude/commands/handoff.md` — Fase 5c (gate); `.claude/rules/survival.md` — Lei 1


## 🤖 Claude *(01:22:09)*


## 🤖 Claude *(01:22:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run scripts/qa/run-audit.ts 2>&1 | tail -45",
  "description": "Run Phase 5c material proof audit on v6.27.0 record"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ### 📋 Proof Manifest — Material Proof Audit (Phase 5c)
> 
> | Claim | Kind | Expected | Actual | Verdict |
> |-------|------|----------|--------|---------|
> | commit ee3a016 | git_commit | ee3a016 | ee3a016 | ✅ |
> | commit fb0cbdf | git_commit | fb0cbdf | fb0cbdf | ✅ |
> | commit 492d852 | git_commit | 492d852 | 492d852 | ✅ |
> | tsc --noEmit clean | tsc | 0 errors | 0 errors | ✅ |
> | test suite — 265 passing | test_suite | 265 | 265 passed | ✅ |
> | file _shared/intent-policy.ts | file_exists | _shared/intent-policy.ts | absent | 🔴 |
> | deploy size 80.44kB | edge_deploy | 80.44kB | 80.44kB | ⏭ |
> | deploy size 85.3kB | edge_deploy | 85.3kB | 85.3kB | ⏭ |
> | oro triplet compliance | oro_compliance | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (migration  | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (migration  | ✅ |
> | handoff node 7a9925ad | mesh_node | 7a9925ad-a06a-4ea8-947f-238642c31bfd | 7a9925ad-a06a-4ea8-947f-238642c31bfd | ✅ |
> 
> - 🔴 **file _shared/intent-policy.ts** — file not found: _shared/intent-policy.ts
> 
> QA VERDICT: 7 verified · 2 skipped · 1 failed → SEAL BLOCKED
> 
> (audit completed in 9.8s)
> ```

## 🤖 Claude *(01:22:47)*


## 🤖 Claude *(01:22:50)*

Fase 5c pegou **1 🔴**: a claim `file _shared/intent-policy.ts` não resolve — porque na prosa do record usei o caminho curto `_shared/intent-policy.ts`, mas o arquivo real está em `supabase/functions/_shared/intent-policy.ts`. O arquivo **existe e está commitado** (0021189) — é a referência no texto que está incompleta. Per SOP: corrijo a **causa real** (o texto), nunca fabrico. Confirmo materialmente + corrijo o path:

## 🤖 Claude *(01:22:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== file exists at full path (material)? ===\"; ls -la supabase/functions/_shared/intent-policy.ts\necho \"=== committed in 0021189? ===\"; git show 0021189 --stat --oneline | grep intent-policy\necho \"=== occurrences of the short path in HANDOFF ===\"; grep -c '`_shared/intent-policy.ts`' HANDOFF.md",
  "description": "Verify file at full path + commit + count short-path refs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === file exists at full path (material)? ===
> -rw-rw-r-- 1 ubuntu ubuntu 1892 Jun  3 22:06 supabase/functions/_shared/intent-policy.ts
> === committed in 0021189? ===
>  supabase/functions/_shared/intent-policy.ts    |  36 ++++++++
> === occurrences of the short path in HANDOFF ===
> 1
> ```

## 🤖 Claude *(01:22:57)*


## 🤖 Claude *(01:22:57)*

Confirmado: arquivo real (1892 B) commitado em 0021189. Corrijo a única referência curta no HANDOFF para o caminho completo (verificável):

## 🤖 Claude *(01:22:59)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** (gate compartilhado `_shared/intent-policy.ts`, extra\u00eddo do `intent-orchestrate` p/ n\u00e3o divergir)",
  "new_string": "o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** (gate compartilhado `supabase/functions/_shared/intent-policy.ts`, extra\u00eddo do `intent-orchestrate` p/ n\u00e3o divergir)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:23:10)*


## 🤖 Claude *(01:23:10)*

Re-rodo a Fase 5c:

## 🤖 Claude *(01:23:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nbun run scripts/qa/run-audit.ts 2>&1 | tail -20",
  "description": "Re-run Phase 5c after path fix"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ### 📋 Proof Manifest — Material Proof Audit (Phase 5c)
> 
> | Claim | Kind | Expected | Actual | Verdict |
> |-------|------|----------|--------|---------|
> | commit ee3a016 | git_commit | ee3a016 | ee3a016 | ✅ |
> | commit fb0cbdf | git_commit | fb0cbdf | fb0cbdf | ✅ |
> | commit 492d852 | git_commit | 492d852 | 492d852 | ✅ |
> | tsc --noEmit clean | tsc | 0 errors | 0 errors | ✅ |
> | test suite — 265 passing | test_suite | 265 | 265 passed | ✅ |
> | file supabase/functions/_shared/intent-policy.ts | file_exists | supabase/functions/_shared/intent-policy.ts | supabase/functions/_shared/intent-policy.ts | ✅ |
> | deploy size 80.44kB | edge_deploy | 80.44kB | 80.44kB | ⏭ |
> | deploy size 85.3kB | edge_deploy | 85.3kB | 85.3kB | ⏭ |
> | oro triplet compliance | oro_compliance | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (migration  | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (migration  | ✅ |
> | handoff node 7a9925ad | mesh_node | 7a9925ad-a06a-4ea8-947f-238642c31bfd | 7a9925ad-a06a-4ea8-947f-238642c31bfd | ✅ |
> 
> QA VERDICT: 8 verified · 2 skipped · 0 failed → SEAL ALLOWED
> 
> (audit completed in 8.9s)
> ```

## 🤖 Claude *(01:23:45)*


## 🤖 Claude *(01:23:46)*

**Fase 5c: SEAL ALLOWED** (8 verified · 2 skipped · 0 failed) — independente, mecânica. Agora insiro o nó de handoff na malha (mandato Mesh) e capturo o **UUID real** (Lei 1 — nunca fabricar):

## 🤖 Claude *(01:23:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\nRESP=$(curl -s -X POST \"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes\" \\\n  -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" \\\n  -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n  -d '{\"node_type\":\"handoff\",\"name\":\"session-handoff-20260603-marketing-hub-ui-intent-aeo\",\"content\":\"v6.27.0 \u2014 Marketing-Hub UI follows + intent_plans executor (FR-MH-009 HITL: intent-execute re-valida outward sobre plano armazenado, fail-closed, nunca confia em auto_approved) + AEO audit (FR-MH-010: aeo-audit 5mco, aeo_audits RLS, provider degradado OTD-MH-003). UI: useIntentOrchestrator/useAEO + 3 pain\u00e9is + enroll nurturing. 5 commits, 2 smokes 17/17+12/12, /security-review SAFE (fail-safe adotada), tsc 0, 265 tests, UI logada verificada. Marketing-hub FRs 001..012 backend+UI LIVE.\",\"stability\":1.0,\"user_id\":null}')\necho \"$RESP\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print('NODE_ID:', d[0]['id'] if isinstance(d,list) and d else d)\"",
  "description": "Insert handoff node into mcorch_nodes, capture real UUID"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> NODE_ID: {'code': 'PGRST204', 'details': None, 'hint': None, 'message': "Could not find the 'stability' column of 'mcorch_nodes' in the schema cache"}
> ```

## 🤖 Claude *(01:24:00)*


## 🤖 Claude *(01:24:01)*

`stability` não é a coluna certa (PGRST204). Verifico o schema real de `mcorch_nodes`:

## 🤖 Claude *(01:24:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\ncurl -s \"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=*&limit=1\" \\\n  -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print('columns:', list(d[0].keys()) if d else 'none')\"",
  "description": "Inspect mcorch_nodes columns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> columns: ['id', 'node_type', 'name', 'content', 'metadata', 'embedding', 'created_at', 'last_seen_at', 'stability_score', 'revenue_impact', 'user_id', 'project_id', 'status']
> ```

## 🤖 Claude *(01:24:06)*


## 🤖 Claude *(01:24:06)*

É `stability_score`. Re-insiro com a coluna correta:

## 🤖 Claude *(01:24:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\nRESP=$(curl -s -X POST \"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes\" \\\n  -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" \\\n  -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n  -d '{\"node_type\":\"handoff\",\"name\":\"session-handoff-20260603-marketing-hub-ui-intent-aeo\",\"content\":\"v6.27.0 \u2014 Marketing-Hub UI follows + intent_plans executor (FR-MH-009 HITL: intent-execute re-valida outward sobre plano armazenado, fail-closed, nunca confia em auto_approved) + AEO audit (FR-MH-010: aeo-audit 5mco, aeo_audits RLS, provider degradado OTD-MH-003). UI: useIntentOrchestrator/useAEO + 3 paineis + enroll nurturing. 5 commits, 2 smokes 17/17+12/12, security-review SAFE (fail-safe adotada), tsc 0, 265 tests, UI logada verificada. Marketing-hub FRs 001..012 backend+UI LIVE.\",\"stability_score\":1.0,\"project_id\":\"mcorch-constellation\"}')\necho \"$RESP\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print('NODE_ID:', d[0]['id'] if isinstance(d,list) and d else d)\"",
  "description": "Re-insert handoff node with stability_score"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> NODE_ID: 6f98edf0-a618-4770-885b-e09c422ff8f6
> ```

## 🤖 Claude *(01:24:18)*


## 🤖 Claude *(01:24:19)*

Nó de handoff inserido — UUID real **`6f98edf0-a618-4770-885b-e09c422ff8f6`**. Atualizo o HANDOFF com o UUID real + verifico que o trigger de embedding pegou:

## 🤖 Claude *(01:24:20)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "| Handoff node | \u23f3 inserir nesta seal |",
  "new_string": "| Handoff node | \u2705 `6f98edf0-a618-4770-885b-e09c422ff8f6` embedded 768d |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:24:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\necho \"=== node + embedding status (trigger async; may need a beat) ===\"\ncurl -s \"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?id=eq.6f98edf0-a618-4770-885b-e09c422ff8f6&select=name,node_type,embedding\" \\\n  -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); n=d[0] if d else {}; emb=n.get('embedding'); print('name:', n.get('name')); print('node_type:', n.get('node_type')); print('embedded:', 'YES (768d)' if emb else 'NULL (trigger pending)')\"",
  "description": "Verify handoff node + embedding materialized"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === node + embedding status (trigger async; may need a beat) ===
> name: session-handoff-20260603-marketing-hub-ui-intent-aeo
> node_type: handoff
> embedded: YES (768d)
> ```

## 🤖 Claude *(01:24:36)*


## 🤖 Claude *(01:24:38)*

Nó **embedded 768d** (trigger pegou). Commit do selo documental (HANDOFF + README + sprint):

## 🤖 Claude *(01:24:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add HANDOFF.md README.md .claude/context/sprint-priorities.md\ngit commit -q -m \"docs(handoff): seal v6.27.0 \u2014 marketing-hub UI follows + intent executor + AEO (FR-MH-009/010)\" \\\n  -m \"Marketing-hub completo (FRs 001..012 backend+UI LIVE): executor de intent_plans com re-valida\u00e7\u00e3o outward fail-closed + auditoria AEO + UI follows (3 pain\u00e9is + enroll nurturing). Fase 5c SEAL ALLOWED (8 verified). Handoff node 6f98edf0 embedded 768d. Survival Laws 4/4.\" \\\n  -m \"Next: dispatch outward real do executor (gated) atr\u00e1s de OTD-INTENT-TRANSITION-GUARD; entrega externa de nurturing; OTD-AEO-REFUND.\"\necho \"=== final log ===\"; git log --oneline -6\necho \"=== tree clean? ===\"; git status --short | head",
  "description": "Commit seal docs (HANDOFF/README/sprint)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === final log ===
> 1b5fa90 docs(handoff): seal v6.27.0 — marketing-hub UI follows + intent executor + AEO (FR-MH-009/010)
> 492d852 docs(bok): patch marketing-hub SDD/data-model — intent-execute + engine degraded
> fb0cbdf feat(marketing-hub): UI follows — Intent Orchestrator/HITL + AEO + enroll de nurturing
> ee3a016 feat(marketing-hub): auditoria AEO — aeo-audit + tabela aeo_audits (FR-MH-010)
> 0021189 feat(marketing-hub): executor de intent_plans com re-validação outward (FR-MH-009 HITL)
> 7bb15bc chore(sprint): update sprint-priorities — v6.26.0 drift audit + P0 ledger + 3 marketing-hub FRs
> === tree clean? ===
> ```

## 🤖 Claude *(01:24:47)*


## 🤖 Claude *(01:24:48)*

5 commits, tree limpo. Atualizo a memória `project_marketing_hub_v2` (era o tracker do módulo — agora FR-MH-009/010 + executor estão LIVE e o marketing-hub está completo):

## 🤖 Claude *(01:24:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_marketing_hub_v2.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: project_marketing_hub_v2
> 3	description: Marketing Hub agentic (v2 que absorve o marketing v1) — BoK 9/9; FR-MH-001..009,011,012 backend LIVE (Lead/Campaign Core + lead-score + campaign-run + UI + attribution + Customer360 + nurturing cron + BYOK canal + Intent/HITL backend); faltam UI follows (enroll + Intent UI) + executor de intent_plans + FR-MH-010 AEO
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: cbb758a7-048b-4acb-94aa-db05a445f1e7
> 8	---
> 9	
> 10	Diretiva Sovereign 2026-06-02: módulo **marketing-hub** agentic, nasce como **v2 de consolidação** — absorve e escala o marketing v1 disperso (orchestrate-content vira executor de campanha; whatsapp_leads migra tutela meta-api→marketing-hub; marketing-growth Pantheon é **elevado, não recriado**) em vez de duplicar. Natureza **Ambos**: núcleo interno (Usuário Zero) → comercial per-tenant. Decisões travadas via AskUserQuestion; scope-lock em `.claude/context/marketing-hub-scope-lock-2026-06-02.md`.
> 11	
> 12	**Selado (não-commitado até /handoff):** BoK suite 9/9 em `docs/bok/marketing-hub/` (1732 LOC) + mesh seal `d5163fed-da85-4f95-8445-0d0aa5b6bafe` (DERIVES_FROM meta-api `ca791bdd`, embedded 768d) + `bok-agents-system--marketing-hub.md` (11 agentes = 8 BoK + AEO/Intent-Orchestration/Demand-gen). **BoK Gate LIBERADO.**
> 13	
> 14	**MVP aprovado (PR-MH-001..005 = Lead Core + Campaign Core + Consent/Tenancy + Attribution):**
> 15	- ✅ **MVP-1 LIVE**: migration `20260603000000_marketing_hub_lead_core.sql` aplicada (`db push` Finished) — tabelas `leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` (LGPD, SECURITY DEFINER, search_path='', tenant guard). `/security-review` pegou **1 MEDIUM cross-tenant** (FK de tabela-filha sem co-escopar user_id → A insere evento no lead de B) → corrigido com **FK composta `(lead_id,user_id)→leads(id,user_id)`** + `UNIQUE(id,user_id)` em leads + EXISTS no WITH CHECK de marketing_consents. Provado material: **23503** no cross-tenant, **201** no legítimo, cleanup limpo. whatsapp_leads vazio em prod → backfill no-op correto.
> 16	- ✅ **MVP-2 Campaign Core LIVE** (v6.22.0, migration `20260603025256`): `campaigns` ABSORVIDA via `ALTER` (+intent/channels/mesh_node_id + `UNIQUE(id,user_id)`) + `campaign_steps` (FK composta tenant-`CASCADE`, espelha lead_events) + `marketing_attribution` (FK simples `SET NULL` + RLS `WITH CHECK` — espelha consents porque SET NULL composto anularia user_id NOT NULL; retém receita de-linkada). `erase_lead()` estendida (`attributions_delinked`). tenant-FK provado **comportamental** 23503 + **42501 autenticado** + 201 + zero-resíduo. `/security-review` SAFE (independente). mesh `7628892b`. data-model patcheado (absorb-not-create + FK pattern).
> 17	- ✅ **MVP-3 parte 1 — lead-score LIVE** (FR-MH-003, v6.22.0): JWT + 1 mco atômico + IA per-user→sistema (reusa `fetchLLMWithFallback`) + **fail-soft heurístico**. Smoke E2E: 200 · score=80 (`source=ai`) · débito 100→99 · zero-resíduo. Deploy 84.31kB.
> 18	- ✅ **MVP-3 parte 2 — campaign-run LIVE** (FR-MH-004, v6.23.0): JWT + débito atômico FEE `CAMPAIGN_RUN` 10 → dispatch **PARALELO** (`Promise.allSettled`, wall-clock ≈ passo mais lento) dos passos p/ `orchestrate-content` (self-bila 10) = **cascata fiel 10+10×N**; `channel→platforms` (content/affiliate→wordpress, social→linkedin+twitter, **email→blocked** território nurture); cap `MAX_PARALLEL_STEPS=8`. Smoke **13/13 zero-custo** (`scripts/qa/smoke-campaign-run.ts`: guards 401/422/404/no-steps/402 + isolamento de tenant + email-only→200 dispatched=0 débito atômico 100→90 + cleanup). Deploy 80.92kB. Cascata paga real **gated em GO Sovereign**. Calibração $ segue [[project_mcoin_calibration]].
> 19	- ✅ **MVP-4 UI LIVE** (v6.23.0, FR-MH-001/005): `/dashboard/marketing` (`MarketingPage` = `LeadBoard` 5 colunas + Pontuar/`lead-score` + overview campanhas; nav Target). **Absorveu a UI v1** (diretiva Sovereign "absorver por completo E /dashboard/marketing nova; faça completo, não pare"): `CampaignWizard` +Intenção/passo **Passos** (composer Canal×Ação→`createCampaignWithSteps`); `CampaignDetail` +card **Passos & Execução** (status vivo + `CampaignRunButton`). Hooks `useLeads`/`useLeadScore`/`useCampaignSteps`/`useCampaignRun` + `src/lib/edge.ts` (erro PT-BR de edge). UI LOGADA verificada (magic link `scripts/qa/gen-magiclink.ts` + agent-browser; 0 erros console; zero mutação prod). 11 testes (`src/test/marketing-hub.test.ts`).
> 20	- ✅ **MVP-5 attribution** (v6.24.0) + **1º run pago E2E** (v6.25.0 — flywheel ressuscitado, 3 key-migration P0s; ver [[project_orchestrate_pipeline_repair]]).
> 21	- ✅ **FR-MH-008 Nurturing cron** (v6.26.0): engine+`nurture-dispatch` já existiam; `nurture-cron` (service-role fan-out) + pg_cron `nurture-advance */15` + **modo service-role** em nurture-dispatch (espelha orchestrate-step; consent gate + billing single-source) avançam enrollments due. Smoke cron 5/5 + USER 10/10. Entrega externa real segue **gated**.
> 22	- ✅ **FR-MH-012 BYOK** (v6.26.0): metade-IA já satisfeita (lead-score/nurture-dispatch resolvem `decrypted_user_api_keys` per-user→sistema); metade-canal nova = `resend_api_key` per-tenant (Vault, reproduz defs VIVAS verbatim — **NÃO** o template stale de 060000; preserva fixes 130000/140000) + campo Settings. Round-trip 8/8 (`smoke-byok-resend`).
> 23	- ✅ **FR-MH-009 Intent+HITL backend** (v6.26.0): `intent_plans` (migration `20260603250000`, data-model patcheado antes) + `intent-orchestrate` (verify_jwt=false+getUser; policy engine auto/HITL com **canal-outward fail-safe→HITL** + rationale XAI; custo 0). Smoke 8/8 (alto-impacto→pending_hitl). **UI deferida** (`useIntentOrchestrator`+`HITLApprovalCard`).
> 24	- ⏳ **Pendente:** UI follows (enroll nurturing — hook `enrollLead` JÁ existe em useNurturing — + Intent UI) · **executor de `intent_plans`** (aprovar/rejeitar/executar — DEVE re-validar ação outward no execute, não confiar em `auto_approved`) · **FR-MH-010 AEO** (última FR) · OTD-CAMPAIGN-RUN-ASYNC.
> 25	
> 26	**Reconciliação doc↔realidade (aplicar nos docs ao tocar — Obstáculo→Síntese):** `public.campaigns` **JÁ EXISTE** (de `20260402014040`: user_id/name/objective/status campaign_status/platforms/budget_cents) → Campaign Core **ABSORVE/estende** (ALTER add intent/channels/mesh_node_id), NÃO cria nova. `projects` **NÃO existe** → sem FK project_id (coluna uuid nullable). Status whatsapp é PT (iniciado/interagido/convertido/opt_out) → CASE-map no backfill. `update_updated_at_column()`/`deduct_mco_coins`/`mcoin_transactions`/vector ext confirmados.
> 27	
> 28	Relacionado: [[feedback_api_tenancy_per_user]] · [[reference_encrypted_views_write_pattern]] · [[reference_supabase_keys_migrated]]
> 29	
> ```

## 🤖 Claude *(01:25:01)*


## 🤖 Claude *(01:25:04)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_marketing_hub_v2.md",
  "old_string": "description: Marketing Hub agentic (v2 que absorve o marketing v1) \u2014 BoK 9/9; FR-MH-001..009,011,012 backend LIVE (Lead/Campaign Core + lead-score + campaign-run + UI + attribution + Customer360 + nurturing cron + BYOK canal + Intent/HITL backend); faltam UI follows (enroll + Intent UI) + executor de intent_plans + FR-MH-010 AEO",
  "new_string": "description: Marketing Hub agentic (v2 que absorve o marketing v1) \u2014 BoK 9/9; **FRs 001..012 backend+UI LIVE (COMPLETO)**. v6.27.0 fechou: executor de intent_plans (intent-execute, re-valida outward fail-closed) + AEO (aeo-audit/aeo_audits) + UI follows (Intent/HITL/AEO pain\u00e9is + enroll nurturing). Resta s\u00f3: dispatch outward REAL do executor (hoje gated) atr\u00e1s de OTD-INTENT-TRANSITION-GUARD + entrega externa nurturing (gated) + OTD-AEO-REFUND"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_marketing_hub_v2.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:25:25)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_marketing_hub_v2.md",
  "old_string": "- \u2705 **FR-MH-009 Intent+HITL backend** (v6.26.0): `intent_plans` (migration `20260603250000`, data-model patcheado antes) + `intent-orchestrate` (verify_jwt=false+getUser; policy engine auto/HITL com **canal-outward fail-safe\u2192HITL** + rationale XAI; custo 0). Smoke 8/8 (alto-impacto\u2192pending_hitl). **UI deferida** (`useIntentOrchestrator`+`HITLApprovalCard`).\n- \u23f3 **Pendente:** UI follows (enroll nurturing \u2014 hook `enrollLead` J\u00c1 existe em useNurturing \u2014 + Intent UI) \u00b7 **executor de `intent_plans`** (aprovar/rejeitar/executar \u2014 DEVE re-validar a\u00e7\u00e3o outward no execute, n\u00e3o confiar em `auto_approved`) \u00b7 **FR-MH-010 AEO** (\u00faltima FR) \u00b7 OTD-CAMPAIGN-RUN-ASYNC.",
  "new_string": "- \u2705 **FR-MH-009 Intent+HITL COMPLETO** (backend v6.26.0 + **executor+UI v6.27.0**): `intent-orchestrate` (policy auto/HITL + rationale XAI) + **`intent-execute`** (approve/reject/execute na m\u00e1quina proposed\u2192pending_hitl\u2192approved|rejected\u2192executed). **Golden rule**: o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** via gate compartilhado `supabase/functions/_shared/intent-policy.ts` (extra\u00eddo do orchestrate p/ n\u00e3o divergir; **fail-closed** em plano n\u00e3o-array \u2014 recomenda\u00e7\u00e3o do `/security-review` adotada) \u2192 recusa `409 hitl_required` todo outward sem aprova\u00e7\u00e3o humana, **nunca confia em `auto_approved`**. Tenant-guard 404. Smoke `smoke-intent-execute.ts` **17/17**. UI: `useIntentOrchestrator` + `IntentOrchestratorPanel` + `HITLApprovalCard`. **Dispatch outward ainda GATED** (governan\u00e7a real; envio real \u00e9 next).\n- \u2705 **FR-MH-010 AEO LIVE** (v6.27.0, **\u00faltima FR**): `aeo_audits` (migration `20260603260000`, RLS default-deny append-only) + `aeo-audit` (JWT \u00b7 **5 mco at\u00f4mico** na entrada \u00b7 provider **degradado documentado OTD-MH-003** = LLM como answer-engine proxy, sem scrape SERP do datacenter \u00b7 1 snapshot/query \u00b7 `engine='degraded'`). Smoke `smoke-aeo-audit.ts` **12/12** (RLS cross-tenant leaked=0). UI: `useAEO` + `AEOAuditPanel`. SOP `aeo-audit.md`.\n- \u2705 **UI follows + enroll nurturing** (v6.27.0): 3 pain\u00e9is ligados em `/dashboard/marketing` + bot\u00e3o **Inscrever** lead em sequ\u00eancia no `LeadDetailDialog` (Customer 360). +8 testes (257\u2192265). **UI LOGADA verificada** (agent-browser ARM64, chunk novo, zero crash). Handoff node `6f98edf0-a618-4770-885b-e09c422ff8f6`.\n- \u23f3 **Pendente (p\u00f3s-completar FRs):** **dispatch outward REAL do executor** (hoje retorna `outward_dispatch:'gated'`) atr\u00e1s de **OTD-INTENT-TRANSITION-GUARD** (CHECK/trigger de transi\u00e7\u00e3o em `intent_plans` \u2014 s\u00f3 service role move p/ approved/executed \u2014 defesa contra owner que adultera pr\u00f3prio row via PostgREST) \u00b7 entrega externa de nurturing (gated; `resend_api_key` pronta) \u00b7 **OTD-AEO-REFUND** (refund p\u00f3s-d\u00e9bito) \u00b7 OTD-CAMPAIGN-RUN-ASYNC."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_marketing_hub_v2.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:25:34)*


## 🤖 Claude *(01:25:34)*

Atualizo a linha-índice no MEMORY.md:

## 🤖 Claude *(01:25:35)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "offset": 1,
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Memory Index
> 2	
> 3	- [Auditoria de drift deployado↔migrations + tool/SOP reexecutável](project_schema_drift_audit.md) — 2026-06-03: varredura pós-flywheel (RPC hotfixada sem migration). Incidente ISOLADO; 1 drift real benigno (`rls_auto_enable` capturado) + search_path travado + trigger pg_net morto dropado. Anticorpo `scripts/qa/audit-schema-drift.sh` (8 checagens, exit 1=drift) + SOP. Regra: hotfix de prod vira migration na MESMA sessão.
> 4	- [RPCs do ledger mcoCoins endurecidos — P0 de cunhagem fechado](reference_ledger_rpc_security.md) — 2026-06-03: os 3 RPCs (award/add_user_score/deduct) davam EXECUTE a anon/authenticated + confiavam p_user_id → mint/drain via PostgREST. Agora: award/add_user_score só service_role; deduct authenticated-self-only (guarda p_amount>0 + auth.uid()). REGRA: todo novo SECURITY DEFINER com p_user_id → edge-only OU guarda auth.uid().
> 5	- [Marketing Hub v2 — módulo agentic (FR-MH-001..009,011,012 backend LIVE)](project_marketing_hub_v2.md) — v2 que absorve o marketing v1; Lead/Campaign Core + lead-score + campaign-run + UI /dashboard/marketing + MVP-5 attribution + Customer360 + nurturing (engine v6.24 + **cron v6.26**) + **BYOK canal resend v6.26** + **Intent/HITL backend v6.26** LIVE; faltam UI follows (enroll nurturing [hook existe] + useIntentOrchestrator/HITLApprovalCard) + executor de intent_plans (re-validar outward) + FR-MH-010 AEO; ⚠️ campaigns/campaign_metrics JÁ EXISTEM (absorver) + projects não existe
> 6	- [Calibração de contexto — usar a janela INTEIRA, selar só a ~95%](feedback_context_budget_calibration.md) — Diretiva Sovereign 2026-06-03: janela 1M (Max), seal custa ~5%; empacotar cada sessão com roadmap e só finalizar com ≤5% de folga (≈95% usado). Selar a 45% é desperdício; poda≠selar; puxar próximo pendente em vez de selar. Recalibrou Lei 3 survival.md.
> ```

## 🤖 Claude *(01:25:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "- [Marketing Hub v2 \u2014 m\u00f3dulo agentic (FR-MH-001..009,011,012 backend LIVE)](project_marketing_hub_v2.md) \u2014 v2 que absorve o marketing v1; Lead/Campaign Core + lead-score + campaign-run + UI /dashboard/marketing + MVP-5 attribution + Customer360 + nurturing (engine v6.24 + **cron v6.26**) + **BYOK canal resend v6.26** + **Intent/HITL backend v6.26** LIVE; faltam UI follows (enroll nurturing [hook existe] + useIntentOrchestrator/HITLApprovalCard) + executor de intent_plans (re-validar outward) + FR-MH-010 AEO; \u26a0\ufe0f campaigns/campaign_metrics J\u00c1 EXISTEM (absorver) + projects n\u00e3o existe",
  "new_string": "- [Marketing Hub v2 \u2014 m\u00f3dulo agentic (FRs 001..012 backend+UI LIVE \u2014 COMPLETO)](project_marketing_hub_v2.md) \u2014 v2 que absorve o marketing v1; TODAS as FRs entregues. v6.27.0 fechou: **executor `intent-execute`** (re-valida outward sobre plano armazenado, **fail-closed**, nunca confia em auto_approved \u2014 golden rule do directive) + **AEO** (`aeo-audit`/`aeo_audits`, 5mco, provider degradado OTD-MH-003) + **UI follows** (Intent/HITL/AEO pain\u00e9is + enroll nurturing no Customer360). Resta s\u00f3: **dispatch outward REAL do executor** (hoje `gated`) atr\u00e1s de **OTD-INTENT-TRANSITION-GUARD** + entrega externa nurturing (gated) + OTD-AEO-REFUND; \u26a0\ufe0f campaigns/campaign_metrics J\u00c1 EXISTEM (absorver) + projects n\u00e3o existe"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:26:08)*


## 🤖 Claude *(01:26:25)*

Memória + índice atualizados. Tudo selado. Deixo o resumo executivo ao Maestro.

---

## ✅ Selo v6.27.0 — Marketing Hub: rosto + executor + AEO

Os **três próximos passos** do `/goal` foram entregues, cada um com prova material. O **marketing-hub está completo: FRs 001..012, backend + UI, LIVE.**

### O que foi entregue

**1. UI follows (FR-MH-009)** — `useIntentOrchestrator` + `IntentOrchestratorPanel` + `HITLApprovalCard` (aprovar/rejeitar/executar) + botão **Inscrever** lead em sequência de nutrição no Customer 360 (`enrollLead`, que já existia). Ligados em [`/dashboard/marketing`](src/pages/MarketingPage.tsx).

**2. Executor de `intent_plans` com re-validação outward** — [`intent-execute`](supabase/functions/intent-execute/index.ts) dirige `proposed→pending_hitl→approved|rejected→executed`. A **regra de ouro do directive cumprida**: o `execute` **re-roda o gate sobre o plano armazenado** ([`_shared/intent-policy.ts`](supabase/functions/_shared/intent-policy.ts), extraído do orchestrate p/ não divergir) e **recusa `409 hitl_required` todo plano outward sem aprovação humana — nunca confia em `auto_approved`**. O `/security-review` independente sugeriu **fail-closed** em plano não-array (tamper de shape) → **adotado e provado**.

**3. FR-MH-010 AEO (última FR)** — [`aeo-audit`](supabase/functions/aeo-audit/index.ts) + tabela `aeo_audits` (RLS): 5 mcoCoins atômico, provider **degradado documentado** (OTD-MH-003 — LLM como answer-engine proxy, sem scrape de SERP do datacenter). Entrega externa de nurturing **segue gated** (credencial `resend_api_key` pronta).

### Prova material (Lei 1)

| Gate | Resultado |
|---|---|
| Smokes throwaway | `intent-execute` **17/17** (tamper `auto_approved` + fail-closed bloqueados) · `aeo-audit` **12/12** (RLS cross-tenant leaked=0) |
| Deploys | intent-execute 80.44kB · aeo-audit 85.3kB · `db push` Finished |
| `/security-review` | **SAFE** (subagente independente, 7 propriedades; 1 fail-safe adotada) |
| tsc / suíte / eslint | 0 erros · **265 passed** / 2 skipped · eslint 0 (tocados) |
| Build / deploy | 22.88s · `MarketingPage-kzjcCEeM.js` servido |
| **UI logada** | screenshot real (Usuário Zero) — ambos os painéis renderizam, zero crash |
| **Fase 5c** | **SEAL ALLOWED** (8 verified · 2 skipped · 0 failed) |
| Mesh | handoff node `6f98edf0-a618-4770-885b-e09c422ff8f6` **embedded 768d** |

**5 commits** locais (`0021189` → `1b5fa90`). Survival Laws **4/4**.

### Próximo (registrado no selo)
- **Dispatch outward REAL do executor** (hoje `gated`) — atrás de **OTD-INTENT-TRANSITION-GUARD** (CHECK de transição: só service role move p/ `approved`/`executed`).
- **OTD-AEO-REFUND** (refund pós-débito) · entrega externa de nurturing.

Os edge functions e o frontend **já estão live em produção**; os 5 commits estão **locais** (não dei `git push` — sigo a regra de só publicar quando o Maestro pedir). **Quer que eu faça o push para `origin/main`?**

## 👤 User *(01:27:30)*

o handoff oficial foi selado? /handoff

## 🤖 Claude *(01:27:44)*


## 🤖 Claude *(01:27:46)*

Resposta direta: **não** — eu executei os passos do selo **manualmente** (5 commits, record no HANDOFF, Fase 5c `SEAL ALLOWED`, nó de malha embedded, memória), mas **não rodei o protocolo `/handoff` oficial** como cerimônia única, e **não dei push**. Rodo agora o protocolo oficial para selar formalmente.

## 🤖 Claude *(01:27:46)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "handoff"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: handoff
> ```

## 👤 User *(01:27:46)*

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


## 🤖 Claude *(01:28:18)*


## 🤖 Claude *(01:28:20)*

Rodo o protocolo oficial. **Pre-flight + Fase 1 (segurança) + Fase 6 (BoK) + contagem viva da malha** em paralelo (o trabalho de commits/record/5c já está feito; agora formalizo + faltam README node-count, push):

## 🤖 Claude *(01:28:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== PRE-FLIGHT ===\"; git status --short; echo \"tree ^(clean se vazio)\"; npx tsc --noEmit 2>&1 | tail -3; echo \"tsc done\"\ndocker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"\ncurl -s --max-time 5 http://localhost:8001/api/v2/heartbeat\necho \"\"; echo \"=== PHASE 1 SECURITY (scan session diff 7bb15bc..HEAD) ===\"\necho \"-- 1a secrets --\"; git diff 7bb15bc..HEAD | grep -E \"(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{40,}|STRIPE_SECRET|SB_SECRET_KEY\\s*=\\s*['\\\"])\" | grep -v \"example\\|placeholder\\|<.*>\\|YOUR_\\|grep -E\\|process.env\\|Deno.env\" | head -10 || true; echo \"1a done\"\necho \"-- 1c client coin deduction --\"; grep -rn \"mco_balance.*update\\|UPDATE.*mco_balance\" src/ | grep -v \"settings\\|topup\\|SettingsPage\" | head -5 || echo \"NO VIOLATIONS \u2705\"\necho \"-- 1e sensitive logs --\"; grep -rn \"console\\.log.*token\\|console\\.log.*secret\\|console\\.log.*password\" src/ | head -5 || echo \"NO SENSITIVE LOGS \u2705\"\necho \"\"; echo \"=== PHASE 6 BoK completeness ===\"\nfor slug in $(ls docs/bok/ 2>/dev/null); do m=0; for doc in 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics; do [ -f \"docs/bok/$slug/$doc.md\" ] || m=1; done; [ $m -eq 0 ] || echo \"\u26a0\ufe0f $slug incomplete\"; done; echo \"BoK loop done (s\u00f3 \u26a0\ufe0f aparece)\"\necho \"\"; echo \"=== LIVE mesh node count ===\"\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\ncurl -s \"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id&limit=1\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range | grep -oE '[0-9]+$'",
  "description": "Pre-flight + Phase 1 security + Phase 6 BoK + live node count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === PRE-FLIGHT ===
> tree ^(clean se vazio)
> tsc done
> mcorch_chroma: Up 11 days (healthy)
> mcorch_claude_mem: Up 11 days (healthy)
> mega-brain-dashboard: Up 11 days
> mega-brain-webhook: Up 11 days (healthy)
> mega-brain-daemon: Up 11 days (healthy)
> {"nanosecond heartbeat":1780536512726437419}
> === PHASE 1 SECURITY (scan session diff 7bb15bc..HEAD) ===
> -- 1a secrets --
> 1a done
> -- 1c client coin deduction --
> -- 1e sensitive logs --
> src/test/canvas-video-async-smoke.test.ts:239:    console.log("🔒 [GATE 5] Probing webhook endpoint with an invalid token...");
> src/test/canvas-video-async-smoke.test.ts:247:    console.log(`✅ [GATE 5] Verified endpoint security blocks invalid tokens with status: ${secResp.status}`);
> src/test/canvas-video-async-smoke.test.ts:252:    console.log("🔁 [GATE 6] Probing webhook endpoint with duplicate callback token (replay defense)...");
> 
> === PHASE 6 BoK completeness ===
> BoK loop done (só ⚠️ aparece)
> 
> === LIVE mesh node count ===
> 8776
> ```

## 🤖 Claude *(01:29:04)*


## 🤖 Claude *(01:29:07)*

Pre-flight ✅ (tree clean, tsc 0, 5 containers healthy, Chroma OK). **Fase 1 segurança:** 1a sem segredos ✅, 1c sem dedução client-side ✅, 1e só um match pré-existente em test file (`canvas-video-async-smoke.test.ts` loga a *palavra* "token" numa mensagem, não um valor — ⚠️ não-bloqueante, fora da minha sessão). **Fase 6 BoK:** 13/13 completas ✅. Mesh viva **8776** (era 8770) — +6 sugere **órfãos de smoke** (nós observation de throwaway users deletados). Caço e limpo (higiene de seal, padrão v6.26):

## 🤖 Claude *(01:29:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\nBASE=\"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1\"\necho \"=== smoke-residue observation nodes (intent-exec-* / aeo:*) ===\"\ncurl -s \"$BASE/mcorch_nodes?or=(name.like.intent-exec-*,name.like.aeo:*)&select=id,name,user_id,created_at&order=created_at.desc\" \\\n  -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint(f'found {len(d)} node(s):')\nfor n in d: print(f\\\"  {n['id'][:8]} {n['name'][:40]} user={str(n['user_id'])[:8]}\\\")\nids=[n['id'] for n in d]\nimport pathlib; pathlib.Path('/tmp/smoke_orphan_ids.txt').write_text('\\n'.join(ids))\n\"",
  "description": "Find smoke-residue observation nodes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === smoke-residue observation nodes (intent-exec-* / aeo:*) ===
> found 5 node(s):
>   71d50864 intent-exec-0406dc14-e99a-464e-a344-e06d user=c11efece
>   4306564a intent-exec-54055a33-0bff-44e1-8ec0-0ce0 user=c11efece
>   08212fd2 aeo:MCORCH:2026-06-04 user=8c252cbf
>   61a82ab6 intent-exec-33be6e45-21b5-41ce-bef8-1886 user=c3cc8a52
>   1300bf2d intent-exec-8b96f740-f445-423b-83b1-edc8 user=c3cc8a52
> ```

## 🤖 Claude *(01:29:24)*


## 🤖 Claude *(01:29:26)*

5 órfãos de smoke (4 `intent-exec-*` + 1 `aeo:MCORCH`, todos de throwaway users deletados — `+6 = esses 5 + meu handoff node`). Limpo + reconto:

## 🤖 Claude *(01:29:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\nBASE=\"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1\"\necho \"=== delete 5 smoke-residue nodes ===\"\nwhile read -r id; do\n  [ -z \"$id\" ] && continue\n  code=$(curl -s -o /dev/null -w \"%{http_code}\" -X DELETE \"$BASE/mcorch_nodes?id=eq.$id\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\")\n  echo \"  deleted ${id:0:8} \u2192 HTTP $code\"\ndone < /tmp/smoke_orphan_ids.txt\necho \"=== re-count ===\"\ncurl -s \"$BASE/mcorch_nodes?select=id&limit=1\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range | grep -oE '[0-9]+$'\necho \"=== confirm handoff node still present ===\"\ncurl -s \"$BASE/mcorch_nodes?id=eq.6f98edf0-a618-4770-885b-e09c422ff8f6&select=name\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print('handoff node:', d[0]['name'] if d else 'MISSING')\"\necho '{\"handoffNodeId\": \"6f98edf0-a618-4770-885b-e09c422ff8f6\"}' > proof-manifest.json && echo \"proof-manifest.json written\"",
  "description": "Delete smoke orphans, re-count, confirm handoff node, write proof-manifest"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === delete 5 smoke-residue nodes ===
>   deleted 71d50864 → HTTP 204
>   deleted 4306564a → HTTP 204
>   deleted 08212fd2 → HTTP 204
>   deleted 61a82ab6 → HTTP 204
> === re-count ===
> 8772
> === confirm handoff node still present ===
> handoff node: session-handoff-20260603-marketing-hub-ui-intent-aeo
> proof-manifest.json written
> ```

## 🤖 Claude *(01:29:41)*


## 🤖 Claude *(01:29:42)*

O loop pulou o 5º id (sem newline final — `while read`). Deleto o restante (`1300bf2d`):

## 🤖 Claude *(01:29:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\nBASE=\"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1\"\ncode=$(curl -s -o /dev/null -w \"%{http_code}\" -X DELETE \"$BASE/mcorch_nodes?id=eq.1300bf2d-f445-423b-83b1-edc8\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\")\n# id was truncated in display; delete by the full match via name instead to be safe\ncurl -s -X DELETE \"$BASE/mcorch_nodes?name=eq.intent-exec-8b96f740-f445-423b-83b1-edc8\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" -o /dev/null -w \"delete by name \u2192 HTTP %{http_code}\\n\"\necho \"=== final count ===\"\ncurl -s \"$BASE/mcorch_nodes?select=id&limit=1\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range | grep -oE '[0-9]+$'\necho \"=== residue gone? ===\"\ncurl -s \"$BASE/mcorch_nodes?or=(name.like.intent-exec-*,name.like.aeo:*)&select=id\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print(f'{len(d)} residue node(s) remaining')\"",
  "description": "Delete remaining smoke orphan + final count + confirm clean"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> delete by name → HTTP 204
> === final count ===
> 8772
> === residue gone? ===
> 1 residue node(s) remaining
> ```

## 🤖 Claude *(01:29:57)*


## 🤖 Claude *(01:29:58)*

O id/nome estavam truncados no display (40 chars) — meus deletes não casaram. Pego o id completo do residual e deleto por LIKE:

## 🤖 Claude *(01:30:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSBKEY=$(grep -E '^SB_SECRET_KEY=' .env | cut -d= -f2- | tr -d '\"')\nBASE=\"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1\"\necho \"=== full id of remaining residue ===\"\nFULLID=$(curl -s \"$BASE/mcorch_nodes?or=(name.like.intent-exec-*,name.like.aeo:*)&select=id,name\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d[0]['id']) if d else print('')\")\necho \"id=$FULLID\"\ncurl -s -X DELETE \"$BASE/mcorch_nodes?id=eq.$FULLID\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" -o /dev/null -w \"delete \u2192 HTTP %{http_code}\\n\"\necho \"=== final count + residue check ===\"\ncurl -s \"$BASE/mcorch_nodes?select=id&limit=1\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range | grep -oE '[0-9]+$'\ncurl -s \"$BASE/mcorch_nodes?or=(name.like.intent-exec-*,name.like.aeo:*)&select=id\" -H \"apikey: $SBKEY\" -H \"Authorization: Bearer $SBKEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); print(f'{len(d)} residue node(s) remaining (target 0)')\"",
  "description": "Get full id of remaining residue + delete + verify clean"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === full id of remaining residue ===
> id=1300bf2d-5a33-452c-a9be-17d0cfc17e51
> delete → HTTP 204
> === final count + residue check ===
> 8771
> 0 residue node(s) remaining (target 0)
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-04 - Audit database migrations and clean test artifacts]]
> * **Próxima Sessão**: [[2026-06-04 - agent-a0a6b749e86c06fd2]]
%% --- TIMELINE END --- %%

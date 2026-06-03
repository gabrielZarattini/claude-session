# Audit database migrations and clean test artifacts
**Date:** 2026-06-03 | **Session ID:** `bd90bff2-59ea-4d8a-b987-808b97929c73`

---

## 👤 User *(22:40:38)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(22:40:38)*

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


## 🤖 Claude *(22:40:47)*


## 🤖 Claude *(22:40:48)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with all pre-flight checks in parallel.

## 🤖 Claude *(22:40:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin 2>&1 | tail -3; echo \"--- LOG ---\"; git log --oneline -7; echo \"--- STATUS ---\"; git status --short; echo \"--- DIFF STAT ---\"; git diff HEAD --stat; echo \"--- vs origin/main ---\"; git rev-list --left-right --count HEAD...origin/main 2>/dev/null",
  "description": "Git fetch, log, status, diff scope, vs origin"
}
```

## 🤖 Claude *(22:40:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20; echo \"--- TSC EXIT ---\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- LOG ---
> c6faafe chore(sprint): update sprint-priorities — v6.25.0 flywheel resurrection + mcoCoins calibration
> bcbe79a docs(handoff): seal v6.25.0 — flywheel resurrection (3 P0s) + mcoCoins calibration
> a5b89e8 docs(readme): v6.25.0 — flywheel resurrection (3 key-migration P0s) + mcoCoins calibration
> 091b7da docs(processes): SOPs pipeline async + calibracao mcoCoins + QA user-JWT minter
> 73b8282 feat(billing): calibra COIN_COST no modelo 4x-floor — IMAGE_GENERATION 3->9
> 9ce1301 fix(wordpress): valida post criado — fim do success:true falso no redirect nao-www
> 166dfbf fix(orchestrate): realinha async_orchestrate_step p/ p_service_key + grant service_role — religa o auto-chain
> --- STATUS ---
> --- DIFF STAT ---
> --- vs origin/main ---
> 0	0
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- TSC EXIT ---
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> ✅ aios-sql-bridge — BoK complete
> ✅ canvas-design — BoK complete
> ✅ constellation-v2 — BoK complete
> ✅ conteudo-v2 — BoK complete
> ✅ e2e-user-zero — BoK complete
> ✅ gamificacao-nodes — BoK complete
> ✅ marketing-hub — BoK complete
> ✅ mcorch-constellation — BoK complete
> ✅ mcorch-qa-healing — BoK complete
> ✅ mercado-livre-api — BoK complete
> ✅ meta-api — BoK complete
> ✅ openclaw — BoK complete
> ✅ viralmind — BoK complete
> ```

## 🤖 Claude *(22:40:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- mcorch containers ---\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"--- mega-brain ---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"--- Chroma heartbeat ---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat 2>&1; echo \"\"",
  "description": "Docker containers + Chroma health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- mcorch containers ---
> mcorch_chroma: Up 11 days (healthy)
> mcorch_claude_mem: Up 11 days (healthy)
> --- mega-brain ---
> mega-brain-dashboard: Up 11 days
> mega-brain-webhook: Up 11 days (healthy)
> mega-brain-daemon: Up 11 days (healthy)
> --- Chroma heartbeat ---
> {"nanosecond heartbeat":1780526453214655212}
> ```

## 🤖 Claude *(22:40:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- BoK suites ---\"; ls docs/bok/ 2>/dev/null; echo \"--- HANDOFF lines ---\"; wc -l HANDOFF.md; echo \"--- scratch ---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"",
  "description": "BoK suites, HANDOFF size, scratch check"
}
```

> **Tool Result (Bash)** - ✅ Success
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
> 6653 HANDOFF.md
> --- scratch ---
> scratch/ clean ✅
> ```

## 🤖 Claude *(22:40:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK Gate completeness check"
}
```

## 🤖 Claude *(22:41:17)*


## 🤖 Claude *(22:41:19)*

Pre-flight is materially clean: worktree clean, HEAD == origin/main (0/0), **TSC zero errors**, all containers healthy, Chroma heartbeat OK, all 13 BoK suites complete, scratch clean. Now reading HANDOFF (6653 lines — read-from-end strategy) + sprint priorities in parallel.

## 🤖 Claude *(22:41:20)*


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
> 14	## Flywheel Resurrection + mcoCoins Calibration Record (2026-06-03)
> 15	
> 16	**v6.25.0 (2026-06-03)** — Sessão `/handson` → diretiva Sovereign: "o que precisamos pro 1º run pago E2E + não seria melhor já calibrar o COIN_COST?". Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados). O run pago então **expôs que o flywheel de conteúdo estava silenciosamente MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo `orchestrate-content` preso em `pipeline_runs.status='running'`. Padrão: **probe-first material** (cada causa raiz provada antes do fix) + **adversarial verify** (echo de debug provou a causa do WP — array de posts `www`, não chute).
> 17	
> 18	**O que foi entregue:**
> 19	- **Calibração COIN_COST (OTD-MCOIN-CALIBRATION FECHADA)** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso = venda Enterprise R$997/10000 ÷ R$5.5, pior margem). **Surpresa honesta:** o `10` (orchestrate) e o `125` (canvas vídeo) **já** eram ~4× sobre o custo real ($0.04 imagem DALL·E · $0.56 vídeo Higgsfield); único furo era `IMAGE_GENERATION` (1.36×→9); `CONTENT_GENERATION 5→2`. Esses 2 **não têm caminho de cobrança em prod** (orchestrate cobra flat 10) → mudança segura. SOP `mcoin-cost-calibration.md`. (commit `73b8282`)
> 20	- **3 P0s do flywheel fixados + provados E2E:**
> 21	  - **#1** `orchestrate-step verify_jwt=false` no `config.toml` (faltava → default `true` → gateway 401 na chave opaca `sb_secret_` do pg_net). Deploy 118.4kB. (commit `7b3a481`)
> 22	  - **#2** `async_orchestrate_step` realinhada p/ `p_service_key` + `GRANT service_role` (estava `p_service_jwt_legacy` por hotfix em prod **sem migration** → PGRST202 → auto-chain morto). Migration `20260603190000` · `/security-review` SAFE · `db push` Finished. (commit `166dfbf`)
> 23	  - **#3** `wp_site_url` `mcorch.com`→`https://www.mcorch.com` (não-www → 301 → POST vira GET → WP devolve LISTA → sem `post_url`). `publish-wordpress` endurecido (valida `id`, 502 honesto). (commit `9ce1301`)
> 24	- **SOP** `orchestrate-async-pipeline.md` (3 modos de falha + gates de verificação + recovery) + `scripts/qa/gen-user-jwt.ts` (minta access_token de user p/ QA logada). (commit `091b7da`)
> 25	
> 26	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign (código + política de preço + GO do run + migration, via AskUserQuestion) · Owner=Sovereign (blast radius = gasto real de mcoCoins + 1ª publicação outward + schema de prod).
> 27	
> 28	| Verificação | Resultado |
> 29	|---|---|
> 30	| Calibração | ✅ tsc 0 · billing 22/22 · SOP |
> 31	| Bug #1 verify_jwt | ✅ deploy 118.4kB · orchestrate-step alcançável |
> 32	| Bug #2 migration | ✅ /security-review SAFE · db push Finished · RPC **204** (era PGRST202) |
> 33	| Auto-chain (#1+#2) | ✅ run `aca7b593` auto-completou a `done` SEM kick (linkedin+mesh) |
> 34	| Bug #3 WP | ✅ `publish-wordpress` retorna `post_url` (rascunho `p=13`); 502 honesto em não-www |
> 35	| **Flywheel COMPLETO E2E** | ✅ run `89f18bea` **6/6 passos `done` sem kick** · WP `?p=14` · `content_mesh_asset` done |
> 36	| tsc / suíte | ✅ 0 erros · 257 passed / 2 skipped (259) |
> 37	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 38	| Handoff node | ✅ `5e1b6f32-7d32-4fbb-a1b7-1834e42d187e` embedded 768d |
> 39	| Mesh | ✅ 8769 nós |
> 40	
> 41	| Commit | Conteúdo |
> 42	|---|---|
> 43	| `7b3a481` | fix(orchestrate): orchestrate-step verify_jwt=false |
> 44	| `166dfbf` | fix(orchestrate): realinha async_orchestrate_step + grant service_role |
> 45	| `9ce1301` | fix(wordpress): valida post criado — fim do success falso no redirect |
> 46	| `73b8282` | feat(billing): calibra COIN_COST 4×-floor — IMAGE_GENERATION 3→9 |
> 47	| `091b7da` | docs(processes): SOPs pipeline async + calibração + QA minter |
> 48	| `a5b89e8` | docs(readme): v6.25.0 |
> 49	
> 50	### Arquitetura — pipeline async ressuscitado
> 51	```
> 52	orchestrate-content (JWT user · cobra 10 · cria pipeline_run)
> 53	  └→ async_orchestrate_step RPC  [p_service_key ✓ · GRANT service_role ✓]   (pg_net, Bearer sb_secret_)
> 54	       └→ orchestrate-step  [verify_jwt=false ✓ · self-check Bearer===SB_SECRET_KEY]
> 55	            article_generation → wordpress_publish [www canônico ✓ → post_url] → linkedin_post → twitter_thread
> 56	              → knowledge_mesh + content_mesh_asset
> 57	            (cada passo chama async_orchestrate_step p/ o PRÓXIMO → auto-chain)
> 58	```
> 59	
> 60	### Survival Laws Self-audit
> 61	```
> 62	Law 1 (Materiality): ✅ cada claim provada NESTE turno — deploys ("Deployed"), migration ("Finished"), RPC 204, 2 runs auto-completos (output literal dos steps), /security-review por subagente INDEPENDENTE (SAFE), echo de debug provou a causa WP (array de posts www), tsc 0, suíte 257/259, handoff node embedded 768d. Falha do 1º run reportada honestamente (não mascarada). 1 incidente de higiene divulgado (ecoei valores de chave 1× → não reimprimi). Fase 5c abaixo. Zero fabricação.
> 63	Law 2 (Process): ✅ 2 SOPs novos ANTES de selar; migration passou /security-review (regra CLAUDE.md); Obstáculo→Síntese (3 P0s → SOP + Key Files + memória + nó). Calibração registrada como decisão Sovereign, não improvisada.
> 64	Law 3 (Pruning): ✅ sessão longa de alta densidade (calibração + caça a 3 bugs); contexto consumido em debugging material focado; selada em ponto natural de completude.
> 65	Law 4 (ORO): ✅ triplet declarado; toda ação outward (deploys, migration, db push, 2 runs pagos, edit de wp_site_url) com GO explícito (AskUserQuestion).
> 66	```
> 67	
> 68	**Pendências/Próximos:**
> 69	- **Limpar/liberar artefatos de teste:** 5 `scheduled_posts` parqueados em 2027 (campanha `29b85b73` + adhoc) + 2 rascunhos WP de teste (`?p=13`/`?p=14`) — Sovereign decide apagar ou liberar.
> 70	- **Drift deployado↔migrations:** a `async_orchestrate_step` fora hotfixada em prod sem migration — **auditar outras funções/RPCs por drift similar** (desconfiar do que as migrations dizem vs. o deployado).
> 71	- **Twitter** não conectado (CreditsDepleted) — passo gera conteúdo mas não publica.
> ```

## 🤖 Claude *(22:41:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 71,
  "limit": 430
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 71	- **Twitter** não conectado (CreditsDepleted) — passo gera conteúdo mas não publica.
> 72	- **Roadmap marketing-hub:** FR-MH-009 (Intent+HITL) · FR-MH-010 (AEO) · FR-MH-012 (BYOK) · Nurturing follow-up (entrega externa + cron) · `functionName` nas 9 fns restantes.
> 73	- **[AGUARDANDO] Atribuição de clique ML** — Sovereign reporta quando maturar.
> 74	
> 75	---
> 76	
> 77	## Customer 360 + Nurturing + Flywheel Hardening Record (2026-06-03)
> 78	
> 79	**v6.24.0 (2026-06-03)** — Sessão de **alta densidade** disparada por uma diretiva Sovereign de calibração: selar a v6.23.0 com **~45% da janela usada foi desperdício**; janela é 1M (plano Max), seal custa ~5% → **usar a janela inteira, selar só a ~95%**. Recalibrei a Lei 3 (survival.md) + memória, e segui empacotando: ao perguntar a próxima frente (AskUserQuestion), o Sovereign respondeu "**faça os três — com foco em endurecer o flywheel + observabilidade**". Cinco entregas depois do seal v6.23.0, cada uma provada por **smoke LIVE throwaway** (zero mutação de produção).
> 80	
> 81	**O que foi entregue:**
> 82	- **Calibração de contexto (Lei 3)** — `.claude/rules/survival.md` recalibrado: **poda ≠ selar**; gatilho de SELAR = ~95% de uso OU roadmap esgotado OU GO; fim do nudge "selar a 50%". Memória `feedback_context_budget_calibration` afiada. (commit `dbf4399`)
> 83	- **MVP-5 Atribuição por campanha (FR-MH-007)** — `handle-ml-postback` agora grava `marketing_attribution` numa conversão (campaign_id FK-safe: só linka se UUID real do mesmo tenant, senão NULL de-linkado; **fail-soft** — try/catch nunca quebra o postback de receita). `useCampaignAttribution`+`aggregateAttribution` (puro, testável) + card "Receita Atribuída" no CampaignDetail. **smoke DB 4/4** (`smoke-attribution.ts`: insert válido + total 4000 + bogus campaign_id→FK 23503 + de-linked NULL). (commit `2ed3f63`)
> 84	- **Hardening + observabilidade (foco)** — (a) **gate de lint honesto**: `eslint.config.js` exclui `supabase/functions` (Deno, mislintado por regras browser → ~3716 erros falsos, exit mascarado por `| tail`) + `tailwind.config.ts`; agora `eslint .` = **exit 0 honesto** sobre src/+scripts/. (b) **functionName telemetry** no flywheel (`generate-content`+`orchestrate-step` → `llm-fallback:<fn>`). (c) **smoke de integração** `smoke-marketing-hub.ts` (lead→score→campaign-run→attribution **5/5**). (commit `cae1dff`)
> 85	- **Customer 360 (FR-MH-011)** — VIEW `customer_360` (lead⨝lead_events⨝marketing_consents) **WITH (security_invoker = true)** → RLS das tabelas-base isola cada tenant (fecha o risco cross-tenant FMEA-011 da VIEW). `useCustomer360` + `LeadDetailDialog`. `/security-review` **SAFE** (subagente independente, 9/10) · **isolation smoke 4/4** (`smoke-customer360.ts`: A vê só o lead de A, lead de B **não vaza**). Migration `20260603040000`. (commit `297b0d6`)
> 86	- **Nurturing Sequences (FR-MH-008)** — engine de drip: `sequences`+`sequence_enrollments` (FKs **compostas** tenant-escopadas CASCADE; UNIQUE idempotente) + `nurture-dispatch` cujo centro é o **GATE DE CONSENTIMENTO** (STRIDE-Critical: nunca gera/cobra/registra sem consent granted; opt-out hard-stop; 2 mco; idempotente). **ENVIO GATED** (msg gerada+registrada `delivery='gated'`, entrega externa real diferida). `useNurturing`+`NurturingPanel`. `/security-review` **SAFE** (independente) · **consent-gate smoke 10/10** (`smoke-nurture.ts`: sem consent→blocked/0-cobrança/0-msg; com consent→dispatched/cobra 2/delivered=false; opt-out→skip). Migration `20260603050000`. (commit `ea6c8ba`)
> 87	
> 88	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign (código + gate `/security-review` em 2 migrations + estratégia de 3 frentes via AskUserQuestion) · Owner=Sovereign (blast radius = front comercial + cascata financeira + envios consent-críticos [GATED] + superfície VIEW cross-tenant [isolamento provado material]).
> 89	
> 90	| Verificação | Resultado |
> 91	|---|---|
> 92	| MVP-5 attribution | ✅ postback redeploy 64.73kB · smoke DB **4/4** (insert + FK 23503 + de-linked) |
> 93	| Hardening lint | ✅ `eslint .` exit 0 honesto (Deno/tailwind excluídos) · functionName flywheel deploy · integração **5/5** |
> 94	| Customer 360 | ✅ /security-review SAFE · db push Finished · **isolation 4/4** (B não vaza p/ A) |
> 95	| Nurturing | ✅ /security-review SAFE · db push Finished · nurture-dispatch deploy · **consent-gate 10/10** |
> 96	| tsc / suíte | ✅ 0 erros · **259** (257 passed / 2 skipped) |
> 97	| eslint | ✅ exit 0 honesto |
> 98	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 99	| Handoff node | ✅ `4486cdb1-3718-4cd3-8c90-4a5b601a4604` embedded 768d |
> 100	| Mesh | ✅ 8761 nós (orphan obs node de smoke limpo material + smoke vacinado) |
> 101	
> 102	| Commit | Conteúdo |
> 103	|---|---|
> 104	| `dbf4399` | chore(survival): recalibra Lei 3 — selar só a ~95% |
> 105	| `2ed3f63` | feat(marketing-hub): MVP-5 atribuição por campanha (FR-MH-007) |
> 106	| `cae1dff` | chore(hardening): lint honesto + functionName flywheel + smoke integração |
> 107	| `297b0d6` | feat(marketing-hub): Customer 360 (FR-MH-011) |
> 108	| `ea6c8ba` | feat(marketing-hub): Nurturing Sequences engine (FR-MH-008) consent-gated |
> 109	| `e9c2b66` | fix(qa): smoke-marketing-hub limpa mesh nodes do throwaway |
> 110	
> 111	### Arquitetura — flywheel completo (MVP-1..5) + Customer 360 + Nurturing
> 112	```
> 113	LEAD → lead-score(1mco) → CAMPAIGN(+steps) → campaign-run(10+10×N) → orchestrate-content → publish
> 114	  → affiliate → ML conversion → handle-ml-postback → marketing_attribution → useCampaignAttribution (ROI/campanha)
> 115	CUSTOMER 360 (view security_invoker): lead⨝events⨝consents → useCustomer360 → LeadDetailDialog
> 116	NURTURING: sequence(steps) → enroll(lead) → nurture-dispatch [CONSENT GATE] → msg (delivery gated) → advance
> 117	```
> 118	
> 119	### Survival Laws Self-audit
> 120	```
> 121	Law 1 (Materiality): ✅ toda claim provada NESTE turno — 5 smokes LIVE com output literal (attribution 4/4 · integração 5/5 · customer360 isolation 4/4 · nurture consent-gate 10/10), tsc 0, suíte 259, eslint exit 0 honesto, /security-review por 2 subagentes INDEPENDENTES, deploys OPTIONS 200, milestone embedded 768d, orphan node de smoke detectado+limpo+contado material (8762→8761). Fase 5c abaixo. Zero fabricação.
> 122	Law 2 (Process): ✅ FR-MH-007/011/008 já documentadas na BoK marketing-hub 9/9 selada (SSOT); 2 migrations passaram /security-review (regra CLAUDE.md); calibração registrada em survival.md + memória.
> 123	Law 3 (Pruning): ✅ ESTA sessão É a recalibração em ação — usou a janela inteira (5 entregas, não selou a 45%); poda≠selar; orphan limpo por foco, não acúmulo.
> 124	Law 4 (ORO): ✅ triplet declarado; fork de 3 frentes decidido pelo Sovereign (AskUserQuestion); envios consent-críticos GATED; ações outward com GO.
> 125	```
> 126	
> 127	**Pendências/Próximos:**
> 128	- **[GATED] 1º run pago E2E** — Sovereign cria campanha na UI → Rodar (cascata real).
> 129	- **Nurturing follow-up** — entrega externa real por canal (social/meta) + cron de avanço (enrollments due) + UI de enroll/dispatch a partir do lead. Envio real é outward → Sovereign-aware.
> 130	- **OTD-MCOIN-CALIBRATION** — calibrar `COIN_COSTS` ($ real) — decisão Sovereign.
> 131	- **functionName** nas 9 fns de fallback periféricas restantes (hoje `:unknown`).
> 132	- **FRs marketing-hub restantes:** FR-MH-009 (Intent Orchestrator+HITL) · FR-MH-010 (AEO Audit) · FR-MH-012 (BYOK per-tenant).
> 133	- **[AGUARDANDO] Atribuição de clique ML** — Sovereign reporta o nº quando maturar.
> 134	
> 135	---
> 136	
> 137	## Marketing Hub MVP-4 UI + campaign-run Record (2026-06-03)
> 138	
> 139	**v6.23.0 (2026-06-03)** — Sessão `/handson` → ação nos próximos passos priores. Diretiva Sovereign em duas etapas: (1) "Sim continue, você decide as prioridades" + **calibração de contexto** (parei de adiar `campaign-run` por "contexto saturado" cedo demais — janela é 1M, plano Max, seal é barato; gatilho real da Lei 3 é ~400k, não antes → [[feedback_context_budget_calibration]]); (2) ao chegar no MVP-4 a UI v1 de campanha (1146 LOC) já existia → **AskUserQuestion** sobre a estratégia de absorção → "**Faça absorver v1 por completo E /dashboard/marketing nova. Faça completo e não pare até terminar**". Padrão dominante: **probe-first** (achou a UI v1 existente ANTES de codar, evitando duplicação) + **prova material logada** (não auto-declarada).
> 140	
> 141	**O que foi entregue:**
> 142	- **`campaign-run` edge fn LIVE (FR-MH-004)** — fecha o backend do Marketing Hub. JWT + ownership tenant-escopada → débito atômico do FEE `CAMPAIGN_RUN` (10) → dispatch dos passos p/ `orchestrate-content` (que self-bila seu 10) = **cascata fiel 10+10×N**, JWT do caller encaminhado (billing+RLS mesmo tenant). Dispatch **PARALELO** (`Promise.allSettled`, wall-clock ≈ passo mais lento, não a soma — sequencial estouraria o budget da edge); `channel→platforms` (content/affiliate→wordpress, social→linkedin+twitter, **email→blocked** território nurture); cap `MAX_PARALLEL_STEPS=8`. Sincroniza `campaign_steps.status` + observation node + pulse. **Smoke 13/13 zero-custo** (`scripts/qa/smoke-campaign-run.ts`): 401/422/404/no-steps/402 + isolamento de tenant (campanha alheia→404) + `email`-only→200 dispatched=0 step→blocked débito atômico 100→90 mesh node, cleanup zero-resíduo. Deploy 80.92kB. Cascata PAGA real **gated em GO Sovereign**.
> 143	- **MVP-4 — UI do Marketing Hub** (`/dashboard/marketing`): **LeadBoard** kanban 5 colunas (Novo→Pontuado→Nutrindo→Convertido→Perdido) com Pontuar (`lead-score`) + mover + novo lead; overview de campanhas; nav "Marketing" (ícone Target) no DashboardSidebar.
> 144	- **Absorção da UI v1 (não duplicada)** — `CampaignWizard` ganhou campo **Intenção** + passo **Passos** (composer multicanal Canal×Ação → persiste `campaign_steps` na criação via `createCampaignWithSteps`); `CampaignDetail` ganhou card **Passos & Execução** (passos com status vivo + `CampaignRunButton` confirmando a cascata).
> 145	- **Hooks (Harness Engineering)** — `useLeads`+`useLeadScore` · `useCampaignSteps`+`useCampaignRun`+`createCampaignWithSteps` · `src/lib/edge.ts` (`edgeErrorMessage` extrai erro PT-BR do body non-2xx p/ toasts).
> 146	
> 147	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign (revisão de código + estratégia de absorção via AskUserQuestion) · Owner=Sovereign (blast radius = front comercial + débito financeiro em cascata; deploy nginx + cascata paga gated em GO).
> 148	
> 149	| Verificação | Resultado |
> 150	|---|---|
> 151	| campaign-run deploy | ✅ 80.92kB · smoke **13/13** zero-custo (guards + tenant + email-blocked + débito atômico + cleanup) |
> 152	| MVP-4 tsc | ✅ 0 erros |
> 153	| MVP-4 testes | ✅ 11 novos · suíte **255 passed / 2 skipped** (era 244) |
> 154	| eslint (arquivos tocados) | ✅ limpo (2 `any` pré-existentes da v1 limpos de quebra) |
> 155	| Build/deploy nginx | ✅ `built in 22.32s` · `MarketingPage-DtQfZKUB.js` servido (texto "Marketing Hub" + invokes `lead-score`/`campaign-run` no bundle) · env baked |
> 156	| **UI LOGADA (magic link + agent-browser)** | ✅ `/dashboard/marketing` renderiza (screenshot · 0 erros de console) · wizard **6 passos**, Passos/CampaignStepsEditor (Canal/Ação selects) renderizando · nav Marketing live · **zero mutação de produção** |
> 157	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 158	| Handoff node | ✅ `66447f91-6c00-48f0-8140-0e9193587554` embedded 768d |
> 159	| Mesh | ✅ 8760 nós |
> 160	
> 161	| Commit | Conteúdo |
> 162	|---|---|
> 163	| `2f51651` | feat(marketing-hub): campaign-run edge fn (FR-MH-004) — cascata fiel 10+10×N |
> 164	| `e13b19e` | feat(marketing-hub): MVP-4 — Marketing Hub UI (leads + campaign composer + run) absorvendo v1 |
> 165	| `2553488` | docs(readme): v6.23.0 — Marketing Hub MVP-4 UI + campaign-run |
> 166	
> 167	### Arquitetura — campaign-run (cascata fiel) + MVP-4 (Harness)
> 168	```
> 169	RUN (cliente): useCampaignRun → invoke('campaign-run', {campaign_id})
> 170	  campaign-run: JWT+getUser → ownership (404) → steps (422 vazio) → deduct CAMPAIGN_RUN(10) (402)
> 171	    → Promise.allSettled(steps): channel→platforms · email→blocked
> 172	        fetch orchestrate-content (JWT do caller → self-bila 10) → sync step done|error
> 173	    → observation node + infra pulse → {status, run_id, steps_dispatched, new_balance}
> 174	UI: /dashboard/marketing → LeadBoard (useLeads/useLeadScore) + overview
> 175	    CampaignWizard (+intent +Passos→createCampaignWithSteps) · CampaignDetail (+Passos&Execução +Run)
> 176	```
> 177	
> 178	### Survival Laws Self-audit
> 179	```
> 180	Law 1 (Materiality): ✅ toda claim provada NESTE turno — campaign-run smoke 13/13 (output literal), tsc 0, suíte 255/257, build 22.32s + grep do bundle servido (chunk+invokes+env), UI logada por screenshot+a11y+stepper-text+0 console (Usuário Zero ada39fae). Armadilha divulgada: a11y do agent-browser mostrava heading "Objetivo" stale durante transição framer-motion → resolvi lendo o texto do stepper ("Passo N de 6") em vez de fabricar. Fase 5c executada abaixo. Zero fabricação.
> 181	Law 2 (Process): ✅ campaign-run/MVP-4 = FR-MH-004/005/001/003 da BoK marketing-hub 9/9 selada (o processo antecipado JÁ existe — BoK é SSOT, sem novo SOP). Probe-first pegou a UI v1 existente ANTES de codar (absorver, não duplicar). Memória de calibração de contexto gravada.
> 182	Law 3 (Pruning): ✅ NÃO adiei prematuramente (correção da diretiva Sovereign sobre 1M/Max); rodei MVP-4 completo numa sessão; task list (#1-#4) rastreada e fechada.
> 183	Law 4 (ORO): ✅ triplet declarado; estratégia de absorção decidida pelo Sovereign (AskUserQuestion); cascata paga real gated em GO.
> 184	```
> 185	
> 186	**Pendências/Próximos:**
> 187	- **Primeiro run pago E2E** — Sovereign cria uma campanha na UI nova (`/dashboard/marketing/campaigns/new` → Passos) e clica **Rodar campanha** → cascata real (gasta mco + gera/publica rascunho). Gated em GO.
> 188	- **OTD-MCOIN-CALIBRATION** (segue aberta) — calibrar `COIN_COSTS` contra custo $ real (preço por-modelo OpenRouter + Higgsfield vídeo). Decisão Sovereign.
> 189	- **OTD-CAMPAIGN-RUN-ASYNC** (nova) — fan-out síncrono é simplificação MVP (cap 8 + budget de wall-clock); campanha grande precisa de fila async + callback por passo.
> 190	- **MVP-5** — attribution → `ROIWidget` por campanha + testes E2E.
> 191	- **[ACHADO LATERAL] Dívida de lint repo-wide** — `bun run lint` acusa ~3716 erros PRÉ-EXISTENTES (em `supabase/functions/*` Deno `any` + `tailwind.config.ts` require); o exit code era mascarado pelo `| tail` em seals anteriores. NÃO introduzidos nesta sessão (arquivos tocados estão limpos). Candidato a OTD de limpeza (escopo eslint p/ supabase/functions OU `--fix`).
> 192	- **lead-score follow-up** — granularidade `functionName` nas outras 10 fns do helper de fallback.
> 193	- **[AGUARDANDO DADO] Atribuição de clique ML** — só 1 clique em junho (provável dia 01); Sovereign reporta quando maturar → decide o Browser Operator.
> 194	
> 195	---
> 196	
> 197	## Campaign Core + LLM Fallback + Lead Scoring Record (2026-06-03)
> 198	
> 199	**v6.22.0 (2026-06-03)** — Sessão `/handson` → ação nos alertas → próximos passos priores. Quatro entregas materiais (cada claim provada NESTE turno, não auto-declarada) + decisão de design financeiro **registrada em vez de improvisada** (Master Protocol).
> 200	
> 201	**O que foi entregue:**
> 202	
> 203	- **Alerta `meta_config` — verificado VAZIO (nada a limpar).** O "achado lateral" da v6.20.4 (4 linhas órfãs) já fora varrido: `meta_config_table` 0 linhas (`*/0`), `auth.users` 1 == `profiles` 1 (zero user sem profile), RPC `disconnect_meta` (migration 160000) viva e fail-closed (`28000`). Não fabriquei limpeza inexistente (Lei 1). Cérebro-sem-mãos parcial honesto: `vault.secrets` não-lido via REST.
> 204	- **MVP-2 Campaign Core LIVE** (migration `20260603025256`) — `campaigns` **ABSORVIDA** via `ALTER` (probe-first pegou que já existia + `campaign_metrics` também): `+intent +channels text[] +mesh_node_id uuid→mcorch_nodes + UNIQUE(id,user_id)`. Novas: `campaign_steps` (FK composta tenant-escopada `(campaign_id,user_id)→campaigns` CASCADE, espelha lead_events) + `marketing_attribution` (FK simples SET NULL + RLS WITH CHECK de posse, espelha marketing_consents — retém receita de-linkada). `erase_lead()` estendida (FMEA-MH-003 → `attributions_delinked`). BoK data-model patcheado (absorb-not-create + FK pattern). `/security-review` SAFE (subagente independente, 0 findings ≥8). **Prova comportamental**: `23503` (FK composta, ataque cross-tenant) + `42501` (WITH CHECK attribution, B autenticado plantando campanha de A) + 201 legítimos + cleanup zero-resíduo. types.ts 3307→3544. Mesh seal `7628892b` + edge `0d58d93b` DERIVES_FROM BoK `d5163fed`.
> 205	- **OTD-LLM-FALLBACK FECHADA cedo** (SLA 2026-06-07, owner engineer) — probe-first: o helper `fetchLLMWithFallback` (OpenRouter→Gemini Free→OpenRouter Free→502) já estava live em 11 edge fns. Gap real vs SOP success-signal = observabilidade: helper agora emite `infra_health_logs` (degraded/unhealthy), autossuficiente em Deno (POST PostgREST, sem SDK), fire-and-forget, no-op em teste. **Primeiro teste de edge-helper do projeto** (6 casos de cascata) + vitest estendido a supabase/functions + setup node-tolerant. 3 fns fora do escopo por design (aios-chat gemini-native / search-constellation embeddings / openrouter-swarm arena). 6/6 testes · 11 fns redeployadas · telemetria insert 201 · Gemini 200. Mesh seal `6061a6d2`.
> 206	- **lead-score edge fn LIVE** (FR-MH-003) — JWT (`getUser`), débito atômico 1 mcoCoin (`deduct_mco_coins`), scoring 0-100 via IA per-user→sistema (reusa o cascade helper), **fail-soft heurístico**, persiste `leads.score` + promove `new→scored` + `lead_event` imutável + pulse infra_health. **Smoke real E2E**: HTTP 200 · score=80 · rationale coerente (`source=ai`) · débito 100→99 · cleanup zero-resíduo. Deploy 84.31kB.
> 207	- **Calibração mcoCoins — dívida levantada (OTD-MCOIN-CALIBRATION).** Sovereign questionou se `10` é calibrado: **não é** (número redondo; `orchestrate-content` cobra 10 flat < soma dos componentes 18; `mcoin_transactions` mostram canvas_video dominante ~122/vídeo). `COIN_COSTS` centralizado (`LEAD_SCORE 1`/`CAMPAIGN_RUN 10`) + nota de calibração. **`campaign-run` ESPECIFICADA** (cascata fiel) mas **ADIADA por decisão Sovereign** (Lei 3 — contexto saturado; código financeiro merece sessão fresca + preços $).
> 208	
> 209	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = schema comercial + débito financeiro mcoCoins; migration + 12 deploys com GO "Aprovado").
> 210	
> 211	| Verificação | Resultado |
> 212	|---|---|
> 213	| Alerta meta_config | ✅ VAZIO material (0 linhas · 1==1 user/profile · RPC 160000 fail-closed) |
> 214	| MVP-2 migration aplicada | ✅ `db push Finished` · `20260603025256` |
> 215	| MVP-2 tenant-FK comportamental | ✅ 23503 (composta) + 42501 (WITH CHECK auth) + 201 + zero-resíduo |
> 216	| MVP-2 /security-review | ✅ SAFE (independente, 0 findings ≥8) |
> 217	| OTD-LLM-FALLBACK | ✅ telemetria + 6/6 testes + 11 fns redeploy + insert 201 |
> 218	| lead-score smoke E2E | ✅ 200 · score=80 source=ai · débito 100→99 · zero-resíduo |
> 219	| tsc / suíte | ✅ 0 erros · 244 passed / 2 skipped |
> 220	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 221	| Handoff node | ✅ `aec4cb9c-3765-4d58-9d92-d8130fe568bd` embedded 768d |
> 222	| Mesh | ✅ 8759 nós |
> 223	
> 224	| Commit | Conteúdo |
> 225	|---|---|
> 226	| `7fd8e7a` | feat(marketing-hub): MVP-2 Campaign Core — campaigns absorvida + campaign_steps + marketing_attribution |
> 227	| `0a182d3` | feat(llm-fallback): telemetria infra_health_logs + teste de cascata — fecha OTD-LLM-FALLBACK |
> 228	| `46362c4` | feat(marketing-hub): lead-score edge fn (FR-MH-003) |
> 229	| `d3f6015` | chore(billing): centraliza COIN_COSTS + dívida de calibração |
> 230	| `2017714` | docs(readme): v6.22.0 |
> 231	
> 232	### Survival Laws Self-audit
> 233	```
> 234	Law 1 (Materiality): ✅ toda claim provada NESTE turno — meta_config (count */0 + admin API 1==1), MVP-2 (db push Finished + REST schema + 23503/42501/201 + cleanup REST), OTD (6/6 vitest + 11× Deployed + insert 201 + Gemini 200), lead-score (smoke E2E 200 + REST score/event/balance + zero-resíduo), calibração (mcoin_transactions REST). /security-review por subagente INDEPENDENTE. Fase 5c executada abaixo. Zero fabricação.
> 235	Law 2 (Process): ✅ BoK data-model patcheado ANTES da migration MVP-2; SOP llm-cascading-fallback.md honrado; campaign-run NÃO improvisada (ambiguidade financeira → decisão Sovereign).
> 236	Law 3 (Pruning): ✅ 1 poda explícita após MVP-2+OTD; sessão SELADA por decisão consciente em vez de forçar campaign-run com contexto saturado.
> 237	Law 4 (ORO): ✅ triplet declarado; toda ação outward (migration, 12 deploys, mesh seals) com GO Sovereign.
> 238	```
> 239	
> 240	**Pendências/Próximos (sessão fresca):**
> 241	- **campaign-run (MVP-3 parte 2)** — cascata fiel: `CAMPAIGN_RUN` (10) + por passo `invoke('orchestrate-content')` (10 cada) + sync `campaign_steps.status`. Contrato: `{campaign_id}` → `{status,campaign_id,run_id,steps_dispatched,new_balance}`; errors 401/402/404/422/500.
> 242	- **OTD-MCOIN-CALIBRATION** — calibrar `COIN_COSTS` contra custo $ real (preço por-modelo OpenRouter + Higgsfield vídeo). Vídeo é o maior custo real.
> 243	- **MVP-4** hooks (`useLeads`/`useCampaigns`/`useLeadScore`) + UI (`LeadBoard`/`CampaignComposer`) + rota `/dashboard/marketing`.
> 244	- **MVP-5** attribution → `ROIWidget` por campanha + testes E2E.
> 245	- **lead-score follow-up:** granularidade `functionName` nas outras 10 fns do helper (hoje logam "unknown" no fallback).
> 246	
> 247	---
> 248	
> 249	## Marketing Hub v2 — BoK Suite + 11-Agent System + MVP-1 Lead Core Record (2026-06-03)
> 250	
> 251	**v6.21.0 (2026-06-03)** — Sessão dirigida pelo Sovereign para criar o módulo **marketing-hub** a partir de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). Padrão dominante: **governança BoK-first** (Master Execution Protocol) + **probe-first material** antes da migration. Fluxo: `/handson` → escopo via AskUserQuestion → `/bok-scribe` (9/9) → `/bok-agents-generator` (11 agentes) → revisão Sovereign ("aprovado") → MVP-1 (migration + `/security-review` + apply + prova adversarial) → este selo.
> 252	
> 253	**O que foi entregue:**
> 254	- **Suíte BoK 9/9 selada** (`docs/bok/marketing-hub/`, 1732 LOC) — módulo nasce como **v2 de consolidação**: absorve e escala o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**). Natureza **Ambos** (núcleo interno Usuário Zero + comercial per-tenant). Traceability **0 órfãos** (MR-MH→BR-MH→PR-MH→FR-MH). Mesh seal `d5163fed-da85-4f95-8445-0d0aa5b6bafe` (DERIVES_FROM meta-api `ca791bdd`, embedded 768d).
> 255	- **Sistema de 11 agentes** (`bok-agents-system--marketing-hub.md` via `/bok-agents-generator`) — 8 BoK (BABOK/EABOK/DMBOK/BPM/SWEBOK/CISSP/CXBOK/ProdBOK) + 3 delta (AEO, Intent Orchestration, Demand-gen/Growth) + 3 camadas cross-agent + Pantheon Reconciliation.
> 256	- **MVP-1 Lead Core LIVE** (migration `20260603000000`) — `leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` (LGPD: SECURITY DEFINER, `search_path=''`, fail-closed `28000`, tenant guard `42501`, EXECUTE só authenticated). RLS default-deny nas 3. Backfill de whatsapp_leads (no-op: tabela vazia em prod). `/security-review` (subagente independente) pegou **1 cross-tenant MEDIUM** (FK de filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta `(lead_id,user_id)→leads(id,user_id)`** + `UNIQUE(id,user_id)` + EXISTS no WITH CHECK do consent.
> 257	
> 258	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = novo módulo comercial + PII de lead LGPD; migration aplicada em prod com GO "aprovado").
> 259	
> 260	| Verificação | Resultado |
> 261	|---|---|
> 262	| BoK gate marketing-hub | ✅ 9/9 (1732 LOC) · traceability 0 órfãos |
> 263	| Mesh seal | ✅ `d5163fed` embedded 768d · DERIVES_FROM meta-api `ca791bdd` |
> 264	| Sistema de agentes | ✅ 11 agentes (8 BoK + 3 delta) · 40 KB · `bok-agents-system--marketing-hub.md` |
> 265	| `/security-review` da migration | ✅ 1 MEDIUM cross-tenant achado → REMEDIADO (não suprimido) |
> 266	| Fix tenant-FK (prova comportamental) | ✅ **23503** no ataque (bogus lead + cross-tenant) · **201** no legítimo · cleanup zero-resíduo |
> 267	| Migration aplicada | ✅ `db push` Finished · `20260603000000` no remoto |
> 268	| `tsc --noEmit` | ✅ 0 erros |
> 269	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 270	| Handoff node | ✅ `a48d8ff4-1069-4ca0-8764-f01922e2e12f` embedded 768d |
> 271	| Mesh | ✅ 8755 nós |
> 272	
> 273	| Commit | Conteúdo |
> 274	|---|---|
> 275	| `c4be815` | docs(bok): sela suíte marketing-hub 9/9 + sistema de 11 agentes |
> 276	| `ff81c4f` | feat(marketing-hub): Lead Core migration — leads/lead_events/consents + erase_lead RPC |
> 277	| `8d4b24e` | docs(readme): v6.21.0 |
> 278	
> 279	### Arquitetura — Lead Core (tenant isolation)
> 280	```
> 281	CAPTURE    whatsapp-webhook → whatsapp_leads → (backfill OTD-MH-001) → leads
> 282	LIFECYCLE  leads.status: new → scored → nurturing → converted | lost     (RLS auth.uid())
> 283	EVENTS     lead_events  FK composta (lead_id,user_id)→leads(id,user_id)  ← fecha cross-tenant linkage
> 284	CONSENT    marketing_consents  basis LGPD · FK lead_id ON DELETE SET NULL = retém prova legal
> 285	ERASURE    erase_lead(uuid) SECURITY DEFINER → delete lead+events + withdraw consent (zero-residue)
> 286	```
> 287	
> 288	### Survival Laws Self-audit
> 289	```
> 290	Law 1 (Materiality): ✅ toda claim provada NESTE turno — BoK gate 9/9 (wc -l + ls), mesh seal d5163fed (INSERT RETURNING + embedding REST 768d), 11 agentes (grep count), /security-review por subagente INDEPENDENTE (não auto-avaliação), fix provado comportamental (23503/201 + cleanup via REST), db push Finished, handoff node embedded. Achado schema↔realidade (campaigns já existe / projects não existe) pego por probe-first ANTES de codar. Zero fabricação. Fase 5c executada abaixo.
> 291	Law 2 (Process): ✅ BoK É o processo antecipado (Master Protocol); scope-lock em disco antes do scribe; /security-review obrigatório na migration (regra CLAUDE.md) — finding REMEDIADO material, não suprimido.
> 292	Law 3 (Pruning): ✅ checkpoint explícito após MVP-1 (foundation live) antes de MVP-2..5; tasks rastreadas (MVP-2..5 pendentes); memória de projeto project_marketing_hub_v2 gravada.
> 293	Law 4 (ORO): ✅ triplet declarado; toda ação outward (mesh seal, db push) com GO Sovereign ("aprovado").
> 294	```
> 295	
> 296	**Pendências/Próximos (anotados p/ próxima sessão):**
> 297	- **MVP-2 Campaign Core** — **ABSORVER** a `campaigns` existente (de `20260402014040`: user_id/name/objective/status `campaign_status`/platforms/budget_cents) via `ALTER` (add intent/channels/mesh_node_id) + nova `campaign_steps` + `marketing_attribution`. **NÃO** criar `campaigns` nova (colisão real). Patch nos docs BoK (data-model/SDD) p/ refletir absorb-not-create + `projects` sem-FK.
> 298	- **MVP-3** edge fns `lead-score` (1 mco) / `campaign-run` (10 mco, orquestra orchestrate-content) — JWT gate + `deduct_mco_coins` + `infra_health_logs`.
> 299	- **MVP-4** hooks (`useLeads`/`useCampaigns`/`useLeadScore`/`useMarketingConsent`) + UI (`LeadBoard`/`CampaignComposer`) + rota `/dashboard/marketing`.
> 300	- **MVP-5** attribution → `ROIWidget` por campanha + testes + deploy (build-deploy-guardian).
> 301	- **`erase_lead` extensão obrigatória:** cada nova tabela PII do marketing-hub DEVE estender `erase_lead()` (disciplina FMEA-MH-003 — completude da erasure).
> 302	
> 303	---
> 304	
> 305	## ML Affiliate OAuth Probe + Disconnect UI Verification Record (2026-06-02)
> 306	
> 307	**v6.20.4 (2026-06-02)** — **Seal de conhecimento — zero código de produção tocado** (working tree limpo do início ao fim). Sessão dirigida por duas diretivas do Sovereign, no padrão **probe-first material**: (#1) fechar o resíduo visual que a v6.20.3 anotou — confirmar o disconnect Meta/social pela UI **logada** — e (#2) destravar a iniciativa do **Operador de Browser Autenticado** decidindo o runtime por **probe ANTES** de qualquer `/bok-scribe`/código.
> 308	
> 309	**#1 — disconnect verificado NON-DESTRUTIVO na UI logada.** Loguei como Usuário Zero via Supabase **Admin API `generate_link`** (magic link — método per-user reproduzível, sem token do DevTools nem senha crua) dirigindo `agent-browser` 0.27.0 (Chromium real). `/dashboard/social` renderiza as 3 contas ativas (LinkedIn/Instagram/Facebook), cada uma com botão Desconectar **interativo** (snapshot refs e11/e12/e13) wired a `rpc('disconnect_social')`; `useMetaConfig.ts:78`/`useSocialAccounts.ts:43` chamam `disconnect_meta`/`disconnect_social` (zero `.delete()` resquício). **Nenhum clique destrutivo** — as 3 contas seguem `is_active`; o clique→RPC→revogação-Vault já era DB-proven na v6.20.3. Fecha o resíduo "browser autenticado indisponível" da seal anterior.
> 310	
> 311	**#2 — probe OAuth ML CONCLUÍDO (veredito material):**
> 312	- **Sem API oficial de afiliados ML** — convergência de múltiplas fontes + 403 até no WebFetch da Anthropic. OAuth/login-consentimento daria só um API token, que não existe p/ afiliados.
> 313	- **Link oficial exige portal LOGADO** — segui o `meli.la` do Usuário Zero → redireciona p/ `mercadolivre.com.br/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`. O `ref` é token assinado **não-fabricável**, gerado só no portal.
> 314	- **Datacenter BLOQUEADO p/ browser REAL** — `agent-browser` no portal de afiliados do IP Oracle → página "Hubo un error accediendo a esta pagina" (antes "não-testado"; agora provado). ⇒ Browser Operator **não roda do datacenter**; runtime tem de ser navegador do user ou IP residencial.
> 315	- **Resolver incompleto** — `src/lib/affiliate.ts` seta só `matt_word`; o formato oficial carrega também `matt_tool` (per-user, não armazenado hoje no `affiliate_config`).
> 316	
> 317	**Experimento em curso (Sovereign):** teste de atribuição de clique de links `matt_word`-anexados por dispositivo independente; resultado ~2026-06-03. **Decisão do #2 (Browser Operator vs. só completar o resolver) PAUSADA aguardando o dado.** Não vejo o painel de afiliados (logado + IP bloqueado) — Cérebro sem mãos: Sovereign reporta o nº.
> 318	
> 319	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign · blast radius **nulo** (verificação non-destrutiva + probe read-only; nenhuma mutação de produção, nenhuma credencial manuseada).
> 320	
> 321	| Verificação | Resultado |
> 322	|---|---|
> 323	| #1 login UI (Admin API `generate_link`) | ✅ `/dashboard/settings` + `/dashboard/social` logado (sem redirect p/ `/auth`); header 5351 mcoCoins |
> 324	| #1 disconnect wiring | ✅ `rpc('disconnect_social'/'disconnect_meta'/'disconnect_wordpress')`; zero `.delete()` resquício |
> 325	| #1 não-mutação | ✅ 3 contas sociais seguem `is_active=true` (nenhum clique destrutivo) |
> 326	| #2 ML sem API | ✅ múltiplas fontes + 403 (WebFetch) |
> 327	| #2 link oficial = portal | ✅ `meli.la` → `/social/…&ref=<assinado>` não-fabricável |
> 328	| #2 datacenter bloqueado (browser real) | ✅ "Hubo un error accediendo a esta pagina" |
> 329	| `tsc --noEmit` | ✅ 0 erros |
> 330	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 331	| Handoff node | ✅ `af6bffa2-bce8-4c43-952e-67c0db9c3d23` embedded 768d |
> 332	| Mesh | ✅ 8753 nós |
> 333	
> 334	### Survival Laws Self-audit
> 335	```
> 336	Law 1 (Materiality): ✅ toda claim provada NESTE turno — login via Admin API (URL+título+screenshot), wiring por grep do código, não-mutação por REST (3 is_active), probe por redirect real do meli.la + screenshot do bloqueio ML + 403 do WebFetch. Cérebro-sem-mãos declarado p/ o painel de afiliados (logado+IP bloqueado → Sovereign reporta). Zero fabricação. Fase 5c executada. Zero código → sem claims de commit de feature.
> 337	Law 2 (Process): seal de conhecimento; nenhuma feature nova ganhou código — probe-first respeitado (NÃO construí matt_tool/Browser Operator antes do dado). Memória project_authenticated_browser_operator atualizada com o veredito.
> 338	Law 3 (Pruning): contexto < 50%; decisão consciente de selar no ponto natural em vez de misturar #3/LLM-fallback. Probe consolidado por evidência (UUID/screenshot/redirect).
> 339	Law 4 (ORO): ✅ declarado no início da fase de execução.
> 340	```
> 341	
> 342	**Pendências/Próximos:**
> 343	- **[AGUARDANDO DADO ~2026-06-03] Atribuição de clique ML** — Sovereign reporta o nº de cliques do painel (esperado 1→3 se `matt_word` anexado rastrear) + se o painel mostra por-link ou só total. Decide o destino do #2: (a) `matt_word` basta → quase mata o #2; (b) falta `matt_tool` → add campo per-user no `affiliate_config` + testar; (c) precisa do `ref` → `/bok-scribe` do Browser Operator com runtime FORA do datacenter.
> 344	- **[ACHADO LATERAL] 4 linhas `meta_config` sem profile** — Usuário Zero tem 0 meta_config; as 4 linhas no total pertencem a user_ids sem profile (possível resíduo órfão). Investigar/limpar à parte.
> 345	- **[PRAZO] OTD-LLM-FALLBACK SLA 2026-06-07** — Cascading LLM fallback (owner engineer) — candidato a sessão dedicada após fechar os afiliados.
> 346	
> 347	---
> 348	
> 349	## Meta/Social Disconnect — Orphaned-Secret Revocation Record (2026-06-02)
> 350	
> 351	**v6.20.3 (2026-06-02)** — Sessão disparada por duas diretivas do Sovereign: (A) rodar `/security-review` **redundante** apontado para o `87c926f` (o guard de tenant meta/social selado em v6.20.2) — cinto-e-suspensório; e (B) atacar o débito de **segredo Vault órfão** que a própria seal v6.20.2 anotou no Pending. Padrão dominante mantido: **probe-first material** (Management API, todo teste mutante em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify**. Antes de codar a Parte B, confirmei materialmente que o gap de tenant guard da diretiva original já estava 100% fechado em prod (`pg_get_functiondef` das 2 triggers + ataque comportamental 5/5 → `42501`), evitando uma migration redundante.
> 352	
> 353	**O que foi entregue (Parte B):**
> 354	- **`disconnect_meta()` / `disconnect_social(p_account_id uuid)`** (migration `20260602160000`) — RPCs SECURITY DEFINER, `search_path=''`, fail-closed `28000` sem `auth.uid()`, EXECUTE só `authenticated`. Espelham `disconnect_wordpress`: deletam a linha **E** revogam o segredo Vault. Hooks `useMetaConfig`/`useSocialAccounts` migrados de `.delete()` → `.rpc()`; `types.ts` regenerado (3 entradas: as 2 RPCs + `vault_upsert_secret`).
> 355	- **Guard de tenant por name-binding** (diferença do WP): segredos meta/social são nomeados pelo `id` da linha, não `user_id`. Cada `DELETE` no Vault é double-bound (`id = ref-da-própria-linha` **E** `name = '<prefix>_' || id-da-própria-linha`); como `id` é PK, o id do atacante nunca iguala o da vítima → impossível revogar segredo alheio. Defesa independente: o UUID bruto nunca vaza ao cliente.
> 356	- **Limpeza one-time** dos órfãos preexistentes (`12 → 0` segredos Meta), provadamente orphan-scoped (`NOT EXISTS` linha base via `right(name,36)`), preservando os 3 segredos sociais vivos.
> 357	
> 358	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = retenção de plaintext órfão LGPD + integridade do disconnect per-user).
> 359	
> 360	| Verificação | Resultado |
> 361	|---|---|
> 362	| Parte A — `/security-review` do `87c926f` | ✅ **LIMPO 9/10** (net-hardening; `IS DISTINCT FROM` fecha bypass NULL, UPDATE só vê OLD do próprio tenant, sem SQL dinâmico) |
> 363	| Gap original já fechado (pré-build) | ✅ `pg_get_functiondef` das 2 triggers c/ guard+`42501`+`search_path=""` · ataque comportamental 5/5 `42501` |
> 364	| Suíte RPC (BEGIN/ROLLBACK, dados reais) | ✅ **5/5** — happy meta+social · foreign-id no-op · planted-ref name-binding aguenta · unauth `28000` · zero resíduo |
> 365	| Limpeza de órfãos (preview→apply) | ✅ `12 → 0` segredos Meta órfãos · 3 sociais vivos + 3 linhas intactos |
> 366	| Parte B — `/security-review` da `20260602160000` | ✅ **LIMPO/SAFE 9/10** (PK garante id distinto + UUID não-vazado) |
> 367	| Apply em prod (Mgmt API, txn atômica) | ✅ `20260602160000` no `schema_migrations`; funções SECURITY DEFINER `search_path=""`; EXECUTE authenticated✓/anon revogado✓ |
> 368	| `tsc --noEmit` | ✅ 0 erros |
> 369	| Testes | ✅ 238 passed / 2 skipped · eslint 0 |
> 370	| Frontend deploy | ✅ build exit 0; bundle servido contém `disconnect_meta`/`disconnect_social` + Supabase URL baked |
> 371	| Mesh | ✅ 8752 nós |
> 372	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 373	| Handoff node | ✅ `f7805e20-bebd-4a30-8533-09806238f135` embedded 768d |
> 374	
> 375	| Commit | Conteúdo |
> 376	|---|---|
> 377	| `76bb9e3` | fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão |
> 378	| `610e1f3` | docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão) |
> 379	| `ac1cba1` | docs(readme): v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social) |
> 380	
> 381	### Arquitetura — disconnect com revogação de segredo órfão
> 382	```
> 383	DISCONNECT (meta/social), antes:  client .delete() → INSTEAD OF DELETE → DELETE base row
> 384	                                  → segredo Vault FICA ÓRFÃO (plaintext retido) ❌
> 385	DISCONNECT (meta/social), agora:  client .rpc('disconnect_meta' | 'disconnect_social', {p_account_id})
> 386	   disconnect_*(): IF auth.uid() IS NULL → 28000
> 387	     v_row_id, v_*_ref ← SELECT da PRÓPRIA linha (WHERE user_id = auth.uid() [+ id = p_account_id])
> 388	     DELETE base row
> 389	     DELETE vault.secrets WHERE id = v_*_ref  AND  name = '<prefix>_' || v_row_id   ← double-bind
> 390	       (id é PK ⇒ id-do-atacante ≠ id-da-vítima ⇒ name nunca casa segredo alheio = tenant-safe)
> 391	CLEANUP one-time: DELETE vault.secrets WHERE name ~ '^<prefix>_<uuid>$'
> 392	                  AND NOT EXISTS (linha base com id = right(name,36))   ← só órfãos (12→0)
> 393	```
> 394	
> 395	### Survival Laws Self-audit
> 396	```
> 397	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API — gap original já-fechado (pg_get_functiondef + 5/5 comportamental), suíte RPC 5/5 rolled-back, preview→apply da limpeza (12→0 / 3 vivos), pós-apply (funções+grants+tracking), build+bundle servido com as RPCs. Zero fabricação. 1 armadilha divulgada (urllib→Cloudflare 1010 → troquei p/ curl). Fase 5c executada abaixo. NÃO criei migration redundante p/ o gap já fechado (seria fabricar trabalho).
> 398	Law 2 (Process): ✅ SOP credential-disconnect-clear.md estendido (seção disconnect meta/social + equivalência LGPD) antes do commit; CLAUDE.md Key Files. Extensão de feature documentada (disconnect/clear) → sem BoK gate.
> 399	Law 3 (Pruning): investigação focada; outputs consumidos, referência por path/UUID/migration/commit.
> 400	Law 4 (ORO): ✅ declarado no início da Parte B; "faça os dois" = autorização autônoma do Sovereign.
> 401	```
> 402	
> 403	**Pendências/Próximos (anotados p/ próxima sessão):**
> 404	- **E2E no navegador:** o disconnect foi verificado pela perspectiva do banco (RPC 5/5 + bundle servido contém as RPCs); o clique real na UI logada (`/dashboard/settings` → Desconectar Meta/social) não foi executado (browser autenticado indisponível). Confirmar visualmente no próximo passe.
> 405	
> 406	---
> 407	
> 408	## Vault Idempotent Encrypt + Tenant Guard Record (2026-06-02)
> 409	
> 410	**v6.20.2 (2026-06-02)** — Sessão disparada pela dívida residual que a própria seal v6.20.1 anotou no Pending: o `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` **incondicionalmente** → re-salvar um segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`) — o caso "editar a senha WP sem desconectar antes". Padrão dominante: **probe-first material** (Management API, todo teste em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify** — um achado HIGH do `/security-review` foi REFUTADO materialmente (o overwrite cross-tenant é fail-closed pelo `PRIMARY KEY`, md5 da vítima inalterado), mas a investigação revelou um gap REAL paralelo (injeção cross-tenant id-novo nas INSTEAD OF de meta/social), fechado na mesma sessão.
> 411	
> 412	**O que foi entregue:**
> 413	- **Idempotência (fecha o 23505 no re-save):** helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated → não é RPC alcançável) resolve o segredo por nome e rotaciona in-place via `vault.update_secret` (COALESCE-keep de nome/desc), senão cria; +fallback `unique_violation` p/ a corrida. As 3 encrypt triggers passam a usá-lo + ganham `search_path=''`. A coluna mantém o MESMO UUID Vault entre rotações (sem órfãos). Migration `20260602140000`.
> 414	- **Guard de tenant (fecha injeção cross-tenant):** as INSTEAD OF de `meta_config`/`social_accounts` não tinham o guard `auth.uid()` da `130000`. Views `SECURITY DEFINER` + o WHERE de view não restringe INSERT → autenticado injetava credencial em nome de outro (user_id spoofado + id novo). Guard `42501` portado pras branches INSERT+UPDATE das 2, recriadas **verbatim** do `pg_get_functiondef` live + `search_path=''`. `service_role` isento. Migration `20260602150000`.
> 415	
> 416	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (escopo aprovado: "analise tudo e faça"; toda ação outward com prova material por turno, rolled-back).
> 417	
> 418	| Verificação | Resultado |
> 419	|---|---|
> 420	| 23505 no re-save (prova do bug) | ✅ reproduzido — `ERROR 23505 secrets_name_idx ... trg_encrypt_user_api_keys() line 72` |
> 421	| Re-save pós-fix (`user_api_keys`) | ✅ `{decrypted_wp:"wp-pass-BRAVO", secret_count:1, col_is_uuid_ref:true, sibling_groq_intact:true}` |
> 422	| Re-save pós-fix (`social_accounts`, linha real `39ce0ebb…`) | ✅ `{decrypted_access:"sa-BRAVO", secret_count:1}` |
> 423	| Helper lockdown | ✅ EXECUTE anon/authenticated=false; postgres=true |
> 424	| Injeção cross-tenant ANTES | ✅ atacante criou `meta_config` da vítima (`decrypted_token:"INJECTED-BY-ATTACKER"`) |
> 425	| Injeção cross-tenant DEPOIS | ✅ `42501` nas 2 tabelas; self-insert + `service_role` intactos |
> 426	| HIGH do `/security-review` (overwrite) | ✅ REFUTADO material — PK fail-closed (`23505 social_accounts_pkey`) + md5 vítima inalterado |
> 427	| `tsc --noEmit` | ✅ 0 erros |
> 428	| 2 migrations `/security-review` | ✅ ambas **SAFE** |
> 429	| Migrations aplicadas (Mgmt API, txn) | ✅ `20260602140000`+`20260602150000` no `schema_migrations` |
> 430	| Cleanliness | ✅ meta=0/social=3 linhas · 0 segredos de teste · dados reais intactos |
> 431	| Mesh | ✅ 8751 nós |
> 432	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 433	| Handoff node | ✅ `ea6a3a17-2804-4de3-b153-31f823a9fdb5` embedded 768d |
> 434	
> 435	| Commit | Conteúdo |
> 436	|---|---|
> 437	| `2db5f62` | fix(credentials): vault_upsert_secret idempotente — elimina 23505 ao rotacionar segredo |
> 438	| `87c926f` | fix(credentials): guard de tenant nas INSTEAD OF de meta_config/social_accounts |
> 439	| `deb661c` | docs(processes): fecha débito de idempotência + guard meta/social no SOP |
> 440	| `beec4aa` | docs(readme): v6.20.2 |
> 441	
> 442	### Arquitetura — idempotência + isolamento de tenant na camada Vault
> 443	```
> 444	RE-SAVE (rotação): encrypt trigger → public.vault_upsert_secret(value,name,desc)
> 445	                   SELECT id FROM vault.secrets WHERE name=p_name
> 446	                     achou → vault.update_secret(id,value)   [mesmo UUID, só rotaciona o valor]
> 447	                     senão → vault.create_secret(...)        [unique_violation → re-resolve+update]
> 448	GUARD (meta/social INSTEAD OF, branches INSERT+UPDATE):
> 449	   auth.role()<>'service_role' AND NEW.user_id<>auth.uid() → 42501
> 450	   (DELETE fica SEM guard de propósito — o WHERE da view mascarada já filtra DELETE/UPDATE/SELECT;
> 451	    só INSERT escapa do WHERE → é exatamente onde o guard entra)
> 452	```
> 453	
> 454	### Survival Laws Self-audit
> 455	```
> 456	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API, tudo rolled-back — 23505 reproduzido + before/after de re-save (user_api_keys + social_accounts) + lockdown do helper + injeção antes/depois (42501) + metadados pós-apply + cleanliness. Zero fabricação. Achado HIGH do /security-review REFUTADO com teste material (PK fail-closed + md5 da vítima inalterado), não com argumento. 1 armadilha de ambiente divulgada (`UID` readonly do bash → `$U`). Fase 5c executada abaixo.
> 457	Law 2 (Process): ✅ SOP credential-disconnect-clear.md atualizado (débito → Resolved + bloco de isolamento de tenant) antes do commit; CLAUDE.md Key Files. Bug fix em features documentadas → sem BoK gate.
> 458	Law 3 (Pruning): investigação longa (probes C1-C4, V1-V2, before/after meta+social) — outputs consumidos, referência por path/UUID/migration.
> 459	Law 4 (ORO): ✅ declarado no início; "analise tudo e faça" = autorização autônoma do Sovereign p/ resolver em-sessão + selar.
> 460	```
> 461	
> 462	**Pendências/Próximos (anotados p/ próxima sessão):**
> 463	- ~~**Segredo órfão no disconnect Meta/social:** desconectar Meta (`useMetaConfig.disconnect`) ou social deleta só a linha base via INSTEAD OF DELETE — o segredo Vault (`meta_config_long_lived_token_<id>` etc.) **fica órfão** (plaintext retido). Paralelo ao que `disconnect_wordpress()` resolveu pro WP; precisa de RPC dedicada (nula linha + revoga segredo) + `/security-review`. Débito LGPD/retenção.~~ ✅ **FECHADO 2026-06-02 (v6.20.3)** — RPCs `disconnect_meta()`/`disconnect_social(uuid)` (migration `20260602160000`); 12 segredos Meta órfãos limpos (12→0); ver Record no topo.
> 464	- **E2E no navegador:** verifiquei PostgREST + triggers + Vault pela perspectiva do banco; o clique na UI logada não foi executado (browser autenticado indisponível).
> 465	
> 466	---
> 467	
> 468	## WordPress BYOK Credential-Write Fix + Encrypt Double-Fire Record (2026-06-02)
> 469	
> 470	**v6.20.1 (2026-06-02)** — Sessão disparada pelo P0 que a própria seal v6.20.0 sinalizou: `SocialAccountsPage` salvava/desconectava WordPress via `.upsert(onConflict)` numa VIEW mascarada. Corrigir os 2 `.upsert` reportados revelou um bug **muito maior e pré-existente** na camada `credential_encryption`: o `INSTEAD OF` do `user_api_keys` disparava o trigger de encriptação **2×** numa só statement → `23505`, quebrando connect/save de **qualquer** usuário com linha já existente (não só WP). Padrão dominante: **probe-first material** (Management API) — cada hipótese provada antes de codar, o que pegou o double-fire (que o `.insert` sozinho não resolveria), a colisão do sentinela `••••` no `.update`, e uma escrita cross-tenant que o `ON CONFLICT` mascarava com o crash.
> 471	
> 472	**O que foi entregue:**
> 473	- **Fix dos 2 `.upsert` (SocialAccountsPage):** save → `.insert()` (roteia pelo INSTEAD OF que faz upsert interno; `.upsert` numa view dá HTTP 400 `42P10`); disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `search_path=''`, escopada a `auth.uid()`) que nula as 3 colunas WP **e deleta o segredo do Vault** (revogação real LGPD; delete amarrado a `id` E nome determinístico → tenant-safe). `null` não limpa via view (guard `COALESCE-NULLIF` preserva). Migration `20260602120000`.
> 474	- **[Descoberto] Fix do double-fire:** `trg_instead_of_user_api_keys` trocado de `INSERT...ON CONFLICT DO UPDATE` (dispara encrypt 2× → `vault.create_secret` nome duplicado → `23505`; `.update` ainda re-encripta o `••••`) para **UPDATE-first / INSERT-if-not-found** (encrypt 1×, igual aos irmãos meta/social) + **guard de tenant** (`auth.uid()` → `42501`). `wp_site_url`/`wp_username` viraram `COALESCE(NEW,base)` (não zeram em save parcial). Migration `20260602130000`. Só `user_api_keys` usava `ON CONFLICT`.
> 475	- **types.ts** regenerado (inclui `disconnect_wordpress`); **SOP** `docs/processes/credential-disconnect-clear.md` (Lei 2 + Obstáculo→Síntese); 3 entradas na Key Files Reference.
> 476	
> 477	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (escopo profundo aprovado explicitamente via AskUserQuestion; toda ação outward com provas materiais por turno).
> 478	
> 479	| Verificação | Resultado |
> 480	|---|---|
> 481	| `.upsert` na view (prova do bug) | ✅ HTTP **400 `42P10`** reproduzido |
> 482	| connect pós-fix (caso 23505) | ✅ persiste + cifra (base=UUID, 1 segredo Vault), groq intacto |
> 483	| `.update` pós-fix (caso 23505 groq) | ✅ sucesso, sem re-encriptar `••••`, `wp_site_url` preservado |
> 484	| `disconnect_wordpress()` | ✅ 3 cols `null` + segredo Vault deletado + AI keys intactas |
> 485	| guard cross-tenant | ✅ `ERROR 42501 cannot write credentials for another user` |
> 486	| `tsc --noEmit` | ✅ 0 erros |
> 487	| 2 migrations `/security-review` | ✅ ambas **SAFE** |
> 488	| `db push` (ambas) | ✅ Finished · `20260602120000`+`20260602130000` no remoto |
> 489	| Frontend deploy (nginx) | ✅ chunk `SocialAccountsPage-4_GWJ_p-.js` com `disconnect_wordpress`, `.env` baked |
> 490	| Mesh | ✅ 8750 nós |
> 491	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 492	| Handoff node | ✅ `7bf9bb0e-a063-43d9-b473-0dd7cdfc97d3` embedded 768d |
> 493	
> 494	| Commit | Conteúdo |
> 495	|---|---|
> 496	| `5dc8084` | fix(credentials): disconnect_wordpress RPC + elimina double-fire do INSTEAD OF |
> 497	| `bafa7a2` | fix(settings): WordPress conecta via .insert e desconecta via RPC |
> 498	| `377251e` | docs(processes): SOP de disconnect/clear de credencial |
> 499	| `6b2f8db` | docs(readme): v6.20.1 |
> 500	
> ```

## 🤖 Claude *(22:41:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 6253,
  "limit": 400
}
```

## 🤖 Claude *(22:41:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 6253	
> 6254	  5. INSERT affiliate_links:
> 6255	       original_url · short_url · platform=mercadolivre
> 6256	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 6257	
> 6258	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 6259	
> 6260	ContentLibraryPage monetization flow:
> 6261	  Card (text, body contains mercadolivre.com.br)
> 6262	    └── DropdownMenu → "Monetizar Links ML"
> 6263	          → handleMonetizeLinks(item):
> 6264	               match(ML_URL_RE) → unique URLs
> 6265	               for url of unique:
> 6266	                 POST process-affiliate-link → affiliate_url
> 6267	                 body.split(url).join(affiliate_url)
> 6268	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 6269	          → Badge 💰 ML (emerald) exibido após monetização
> 6270	```
> 6271	
> 6272	---
> 6273	
> 6274	## Pending Actions (Commercial Launch)
> 6275	
> 6276	### CRITICAL — Must complete before first client
> 6277	
> 6278	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 6279	
> 6280	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 6281	
> 6282	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 6283	
> 6284	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 6285	
> 6286	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 6287	
> 6288	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 6289	
> 6290	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 6291	
> 6292	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 6293	
> 6294	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 6295	   ```bash
> 6296	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 6297	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 6298	   ```
> 6299	
> 6300	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 6301	
> 6302	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 6303	
> 6304	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 6305	
> 6306	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 6307	
> 6308	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 6309	
> 6310	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 6311	
> 6312	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 6313	
> 6314	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 6315	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 6316	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 6317	
> 6318	### SOCIAL — Next steps
> 6319	
> 6320	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 6321	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 6322	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 6323	
> 6324	### NON-CRITICAL
> 6325	
> 6326	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 6327	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 6328	- `browserslist` — ✅ updated (2026-04-26)
> 6329	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 6330	
> 6331	### GITNEXUS MCP — Next steps
> 6332	
> 6333	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 6334	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 6335	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 6336	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 6337	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 6338	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 6339	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 6340	
> 6341	### PHASE EPSILON — Next iterations
> 6342	
> 6343	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 6344	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 6345	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 6346	
> 6347	### CORE — Next iterations
> 6348	
> 6349	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 6350	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 6351	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 6352	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 6353	
> 6354	### PHASE DELTA — Next iterations
> 6355	
> 6356	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 6357	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 6358	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 6359	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 6360	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 6361	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 6362	
> 6363	### USUÁRIO ZERO — Checklist de validação
> 6364	
> 6365	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 6366	- ✅ Stripe sandbox secrets no vault
> 6367	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 6368	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 6369	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 6370	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 6371	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 6372	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 6373	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 6374	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 6375	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 6376	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 6377	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 6378	
> 6379	---
> 6380	
> 6381	## Infrastructure
> 6382	
> 6383	| Service | Container | Port | Status |
> 6384	|---------|-----------|------|--------|
> 6385	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 6386	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 6387	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 6388	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 6389	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 6390	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 6391	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 6392	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 6393	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 6394	
> 6395	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 6396	
> 6397	```bash
> 6398	docker compose up -d
> 6399	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 6400	```
> 6401	
> 6402	---
> 6403	
> 6404	## Security Model (Post-Go-Live)
> 6405	
> 6406	| Table | Isolation |
> 6407	|-------|-----------|
> 6408	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 6409	| `mcorch_edges` | Same pattern |
> 6410	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 6411	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 6412	
> 6413	---
> 6414	
> 6415	## Billing Architecture
> 6416	
> 6417	| Decision | Value |
> 6418	|----------|-------|
> 6419	| Canonical billing ledger | `profiles.mco_balance` |
> 6420	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 6421	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 6422	| Orchestration cost | 10 mcoCoins/run |
> 6423	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 6424	| Stripe | Sandbox keys active — swap to live before first client |
> 6425	
> 6426	---
> 6427	
> 6428	## GraphRAG State
> 6429	
> 6430	- **8769 total nodes** (v6.25.0: +handoff `5e1b6f32` + observation/content_mesh_asset nodes dos 3 runs E2E de validação do flywheel; was 8761 in v6.24.0 / 8759 in v6.22.0 snapshot)
> 6431	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 6432	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 6433	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 6434	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 6435	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 6436	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 6437	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 6438	- HNSW cosine index operational
> 6439	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 6440	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 6441	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 6442	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 6443	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 6444	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 6445	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 6446	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 6447	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 6448	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 6449	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 6450	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 6451	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 6452	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 6453	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 6454	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 6455	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 6456	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 6457	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 6458	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 6459	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 6460	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 6461	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 6462	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 6463	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 6464	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 6465	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 6466	
> 6467	### Embedding Model
> 6468	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 6469	Schema: `vector(768)` — HNSW cosine index.
> 6470	
> 6471	### Embedding Pipeline (Autônomo — 2026-05-03)
> 6472	Três camadas eliminam intervenção manual:
> 6473	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 6474	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 6475	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 6476	
> 6477	### Comandos de manutenção da Mesh
> 6478	```bash
> 6479	# Verificar nós sem embedding (deveria retornar array vazio):
> 6480	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 6481	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 6482	
> 6483	# Backfill manual (Bun-native — requer .env):
> 6484	bun run scripts/backfill-embeddings.ts
> 6485	
> 6486	# Backfill de código-fonte nos nós AST:
> 6487	bun run scripts/backfill-node-content.ts
> 6488	
> 6489	# Re-sync AST completo:
> 6490	cd packages/gitnexus-core && npm run sync-mesh
> 6491	
> 6492	# Acompanhar re-ingesta pós-commit:
> 6493	tail -f /tmp/mcorch-ingest.log
> 6494	```
> 6495	
> 6496	---
> 6497	
> 6498	## Video Rescue Protocol
> 6499	
> 6500	When a video generation operation (Google Veo) times out or client disconnects:
> 6501	```bash
> 6502	# Via edge function (production):
> 6503	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 6504	  -H "Authorization: Bearer <user_jwt>" \
> 6505	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 6506	
> 6507	# Via local script (admin/debug):
> 6508	source .env && bun run rescue.ts <operation_id> <content_id>
> 6509	```
> 6510	
> 6511	---
> 6512	
> 6513	## Architecture Pillars
> 6514	
> 6515	| Layer | Implementation |
> 6516	|-------|---------------|
> 6517	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 6518	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 6519	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 6520	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 6521	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 6522	
> 6523	---
> 6524	
> 6525	## Phase Delta — Architecture
> 6526	
> 6527	```
> 6528	OrchestrationPage (full-canvas, p-0)
> 6529	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 6530	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 6531	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 6532	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 6533	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 6534	        ├── nodes/PublishNode.tsx    ← final distribution output
> 6535	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 6536	        └── NodePalette.tsx          ← top toolbar to add nodes
> 6537	
> 6538	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 6539	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 6540	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 6541	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 6542	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 6543	```
> 6544	
> 6545	### Canvas State Architecture (Hybrid)
> 6546	
> 6547	```
> 6548	User interaction → ReactFlow internal state (positions, drag)
> 6549	                         ↓ (debounced 600ms)
> 6550	                   localStorage (positions persist across refresh)
> 6551	                         ↑
> 6552	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 6553	     ↓ (status changes sync to ReactFlow via useEffect)
> 6554	ReactFlow renders visual status (idle/running/done/error/blocked)
> 6555	```
> 6556	
> 6557	## Key Files
> 6558	
> 6559	| Purpose | Path |
> 6560	|---------|------|
> 6561	| Architecture rules | `CLAUDE.md` |
> 6562	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 6563	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 6564	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 6565	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 6566	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 6567	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 6568	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 6569	| **Node types** | `src/components/orchestrator/nodes/` |
> 6570	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 6571	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 6572	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 6573	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 6574	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 6575	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 6576	| Billing utilities | `src/lib/billing.ts` |
> 6577	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 6578	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 6579	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 6580	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 6581	| Video rescue (local) | `rescue.ts` |
> 6582	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 6583	| Backfill script | `scripts/backfill-embeddings.ts` |
> 6584	| Deploy harness | `scripts/harness-deploy.sh` |
> 6585	
> 6586	---
> 6587	
> 6588	## First Client Onboarding Checklist
> 6589	
> 6590	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 6591	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 6592	3. ~~Activate watchdog cron~~ ✅ Done
> 6593	4. ~~Deploy rescue-video function~~ ✅ Done
> 6594	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 6595	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 6596	7. Monitor `infra_health_logs` for first 24h.
> 6597	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 6598	
> 6599	---
> 6600	
> 6601	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 6602	
> 6603	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 6604	
> 6605	| Action | Result |
> 6606	|--------|--------|
> 6607	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 6608	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 6609	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 6610	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 6611	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 6612	
> 6613	| Commit | Conteúdo |
> 6614	|--------|----------|
> 6615	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 6616	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 6617	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 6618	
> 6619	### Arquitetura Matrix Intelligence
> 6620	
> 6621	```
> 6622	ConstellationMatrix (Stabilized Engine)
> 6623	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 6624	  └── NodeDetailsPanel (Tabbed Navigation)
> 6625	        ├── Tab Meta: Neighbor exploration + Net Context
> 6626	        ├── Tab Code: Source code preview (Supabase sync)
> 6627	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 6628	
> 6629	useNodeIntelligence Hook:
> 6630	  - contentQuery: fetch nodes.content column
> 6631	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 6632	  - state: isAnalyzing, analysisResult, progress
> 6633	```
> 6634	
> 6635	---
> 6636	
> 6637	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 6638	
> 6639	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 6640	
> 6641	| Action | Result |
> 6642	|--------|--------|
> 6643	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 6644	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 6645	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 6646	
> 6647	**Output da análise (estruturado em pt-BR):**
> 6648	- Visão Geral — papel do módulo no sistema
> 6649	- Padrões Detectados — design patterns, antipatterns
> 6650	- Acoplamento & Dependências — análise In/Out-Degree
> 6651	- Recomendações — 1-3 ações priorizadas
> 6652	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-51 of 195 total (39392 tokens, cap 25000). Call Read with offset=52 limit=51 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.25.0 selado em 2026-06-03** — **Flywheel ressuscitado + calibração mcoCoins**. `/handson` → diretiva Sovereign ("o que falta pro 1º run pago E2E + já calibrar o COIN_COST?"). Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados): **OTD-MCOIN-CALIBRATION FECHADA** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso=Enterprise); surpresa honesta — `10` (orchestrate) e `125` (canvas vídeo) **já** eram ~4× sobre custo real, único furo `IMAGE_GENERATION 3→9` (`CONTENT_GENERATION 5→2`). O **1º run pago E2E então expôs que o flywheel de conteúdo estava MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo run preso em `running`: **#1** `orchestrate-step` faltava no `config.toml` (`verify_jwt=true` → gateway **401** na chave opaca `sb_secret_` do pg_net); **#2** `async_orchestrate_step` hotfixada em prod **sem migration** (`p_service_jwt_legacy`≠`p_service_key` → **PGRST202** → auto-chain morto) → migration `20260603190000` realinha + `GRANT service_role`, `/security-review` SAFE, RPC **204**; **#3** `wp_site_url` não-www → **301 → POST vira GET** → WP devolve LISTA de posts → `publish-wordpress` endurecido (valida `id`, 502 honesto) + `wp_site_url→www`. **Provado E2E**: run `89f18bea` **auto-completou 6/6 passos sem kick** → rascunho WP `?p=14` + `content_mesh_asset` done. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8769**. Survival Laws **4/4**. 7 commits. **Novo Top Gap:** auditar **drift deployado↔migrations** (outras RPCs/fns hotfixadas em prod?) · limpar artefatos de teste (5 posts parqueados 2027 + 2 rascunhos WP) · FR-MH-009/010/012 + Nurturing follow-up · functionName nas 9 fns. **Lição:** o 1º run pago **não "falhou"** — fez seu trabalho: expôs 3 P0s silenciosos no coração do produto (falha sem erro visível, sem auto-refund); calibrar **antes** do run foi a decisão certa (transação econômica honesta).
> 8	
> 9	**Sprint v6.24.0 selado em 2026-06-03** — **Sessão de alta densidade** (diretiva Sovereign: selar a 45% é desperdício → usar a janela 1M inteira, selar só a ~95%; **Lei 3 recalibrada** em survival.md: poda≠selar). Resposta ao "faça os três, foco em endurecer o flywheel": 5 entregas pós-v6.23.0, cada uma com **smoke LIVE throwaway**. **(1) MVP-5 Atribuição (FR-MH-007)**: `handle-ml-postback`→`marketing_attribution` (campaign_id FK-safe, fail-soft) + `useCampaignAttribution`+card "Receita Atribuída"; smoke DB 4/4 (FK 23503 + de-linked). **(2) Hardening+observabilidade (FOCO)**: `eslint .` **honesto** (Deno `supabase/functions`+tailwind excluídos — ~3716 erros falsos, exit mascarado por `| tail`) + functionName telemetry no flywheel + smoke integração lead→score→campaign→attribution 5/5. **(3) Customer 360 (FR-MH-011)**: VIEW `security_invoker` RLS-safe + `useCustomer360`+drawer; /security-review SAFE + **isolation smoke 4/4** (B não vaza p/ A). **(4) Nurturing (FR-MH-008)**: engine `sequences`+`sequence_enrollments` (FK composta CASCADE) + `nurture-dispatch` **consent-gated** (envio gated) + `useNurturing`+`NurturingPanel`; /security-review SAFE + **consent-gate smoke 10/10**. 2 migrations /security-review SAFE (subagentes independentes) · tsc 0 · suíte **259** · eslint exit 0 honesto · 4 deploys · 5 smokes LIVE. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8761** (orphan obs de smoke limpo + smoke vacinado). Survival Laws **4/4**. 8 commits. **Novo Top Gap:** 1º run pago E2E (gated GO) · Nurturing follow-up (entrega externa real + cron + UI enroll/dispatch) · OTD-MCOIN-CALIBRATION · FRs restantes FR-MH-009/010/012. **Lição:** densidade máxima por sessão (5 frentes numa só) sem perda de materialidade — cada uma provada por smoke LIVE; o gate de lint estava mentindo (exit mascarado) — fix de raiz restaura honestidade da Lei 1.
> 10	
> 11	**Sprint v6.23.0 selado em 2026-06-03** — Marketing Hub backend completo + **MVP-4 UI live**: `campaign-run` (FR-MH-004) fechou o backend, depois o módulo inteiro ganhou rosto em `/dashboard/marketing` **absorvendo a UI v1** (não duplicando). **(1) campaign-run** JWT + débito atômico do FEE `CAMPAIGN_RUN` (10) → dispatch **paralelo** (`Promise.allSettled`) dos passos p/ `orchestrate-content` (self-bila 10) = **cascata fiel 10+10×N**; `email`→blocked; cap 8; smoke **13/13 zero-custo** (guards + isolamento de tenant + email-blocked + débito atômico 100→90 + cleanup); deploy 80.92kB; cascata paga **gated em GO**. **(2) MVP-4 UI**: `/dashboard/marketing` (LeadBoard 5 colunas + Pontuar/`lead-score` + overview campanhas; nav Target) + absorção v1 (`CampaignWizard` +Intenção/passo **Passos** composer→persiste `campaign_steps`; `CampaignDetail` +card **Passos & Execução** status vivo + `CampaignRunButton`). **(3) Hooks**: `useLeads`/`useLeadScore`/`useCampaignSteps`/`useCampaignRun`/`createCampaignWithSteps` + `src/lib/edge.ts`. tsc 0 · **11 testes** (suíte **255/257**) · eslint limpo nos tocados · build 22.32s deploy nginx · **UI LOGADA verificada** (magic link + agent-browser: `/dashboard/marketing` + wizard 6-passos/Passos renderizam, 0 erros console, zero mutação prod). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8760**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** 1º run pago E2E (Sovereign cria campanha→Rodar, gated em GO) · OTD-MCOIN-CALIBRATION ($) · OTD-CAMPAIGN-RUN-ASYNC (fila p/ campanha grande) · MVP-5 attribution→ROIWidget · **dívida de lint repo-wide** (~3716 erros pré-existentes em `supabase/functions` Deno, exit mascarado por `| tail` — não introduzidos nesta sessão). **Lição:** a diretiva Sovereign de calibração de contexto (1M/Max → não adiar por "contexto" antes de ~400k) destravou rodar o MVP-4 completo numa sessão; probe-first pegou a UI v1 existente ANTES de codar (absorver, não duplicar); a11y do agent-browser estava stale na transição framer-motion → li o stepper-text em vez de fabricar (Lei 1).
> 12	
> 13	**Sprint v6.22.0 selado em 2026-06-03** — Campaign Core + LLM Fallback + Lead Scoring: 4 entregas materiais via `/handson`→ação nos alertas→próximos priores. **(1) Alerta meta_config** verificado **VAZIO** (0 linhas · `auth.users` 1==`profiles` 1 — não fabriquei limpeza inexistente, Lei 1). **(2) MVP-2 Campaign Core LIVE** (migration `20260603025256`): `campaigns` **ABSORVIDA** via `ALTER` (+intent/channels/mesh_node_id + `UNIQUE(id,user_id)`) + `campaign_steps` (FK composta tenant-`CASCADE`, espelha lead_events) + `marketing_attribution` (FK simples `SET NULL` + RLS `WITH CHECK`, espelha consents); tenant-FK provado **comportamental** (23503 + 42501 autenticado + 201 + zero-resíduo); `/security-review` **SAFE** (subagente independente); mesh `7628892b`. **(3) OTD-LLM-FALLBACK FECHADA cedo** (SLA 06-07, owner engineer): probe-first achou o helper já live em 11 fns → fechei o gap de observabilidade do SOP (telemetria `infra_health_logs` autossuficiente em Deno) + **1º teste de edge-helper do projeto** (6 casos) + 11 fns redeploy; mesh `6061a6d2`. **(4) lead-score LIVE** (FR-MH-003): JWT + 1 mco atômico + IA per-user→sistema fail-soft; **smoke E2E** 200 · score=80 (`source=ai`) · débito 100→99 · zero-resíduo. **Calibração mcoCoins**: `COIN_COSTS` centralizado + dívida **OTD-MCOIN-CALIBRATION** (o `10` é redondo, não $-calibrado; `orchestrate` cobra 10 flat < soma dos componentes 18; vídeo é o maior custo real). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8759**. Survival Laws **4/4**. 6 commits. **Novo Top Gap:** `campaign-run` cascata fiel (**ADIADA por decisão Sovereign** — código financeiro + contexto saturado, Lei 3) + OTD-MCOIN-CALIBRATION (preços $ por-modelo/vídeo) · MVP-4 hooks+UI `/dashboard/marketing` · MVP-5 attribution. **Lição:** probe-first pegou a OTD já 80% pronta (zero retrabalho) e a divergência `campaigns`/`campaign_metrics` já-existentes; decisão financeira de `campaign-run` **registrada ao Sovereign em vez de improvisada** (Master Protocol).
> 14	
> 15	**Sprint v6.21.0 selado em 2026-06-03** — Marketing Hub (v2): BoK 9/9 + 11 agentes + MVP-1 Lead Core LIVE. Novo **módulo soberano** criado do zero seguindo o Master Execution Protocol (BoK-first), dirigido pela diretiva Sovereign de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). `/bok-scribe` selou a **suíte BoK 9/9** (1732 LOC, `docs/bok/marketing-hub/`, traceability **0 órfãos**, mesh seal `d5163fed` DERIVES_FROM meta-api) — módulo nasce como **v2 de consolidação** que **absorve e escala** o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**), natureza **Ambos** (interno Usuário Zero + comercial per-tenant). `/bok-agents-generator` produziu o **sistema de 11 agentes** (8 BoK + AEO/Intent-Orchestration/Demand-gen + Pantheon Reconciliation). Após revisão Sovereign ("aprovado"), **MVP-1 Lead Core** foi ao ar: migration `20260603000000` (`leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` LGPD SECURITY DEFINER), aplicada via `db push`. O `/security-review` (subagente **independente**) pegou **1 cross-tenant MEDIUM** (FK de tabela-filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta tenant-escopada `(lead_id,user_id)→leads(id,user_id)`** + provado **material** (23503 no ataque, 201 no legítimo, cleanup zero-resíduo). Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8755**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** MVP-2 Campaign Core deve **ABSORVER** a `campaigns` já existente (colisão real achada por probe-first), NÃO criar nova; + MVP-3 edge fns (`lead-score`/`campaign-run`) · MVP-4 hooks+UI (`/dashboard/marketing`) · MVP-5 attribution. **Lição:** probe-first do schema ANTES de codar pegou 2 divergências doc↔realidade (`campaigns` existe, `projects` não) que quebrariam o apply; e o `/security-review` por subagente independente (não auto-avaliação) pegou o furo de tenant que o self-review deixou passar.
> 16	
> 17	**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 18	
> 19	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 20	
> 21	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 22	
> 23	**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 24	
> 25	**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> 26	
> 27	**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 28	
> 29	**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 30	
> 31	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 32	
> 33	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 34	
> 35	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 36	
> 37	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 38	
> 39	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 40	
> 41	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 42	
> 43	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 44	
> 45	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 46	
> 47	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 48	
> 49	**Sprint v6.1.0 selado em 2026-05-14** — Canvas Studio UX Shell + Higgsfield Fix: shell do Canvas Studio migrado do `viralmind-builder` (store Zustand+zundo, lanes overlay, TopBar/LeftPanel/StatusBar, catálogo de 9 receitas, ImageLightbox, PipelineEdge); `canvas-execute` com endpoint Higgsfield corrigido (`platform.higgsfield.ai` rota Soul) + RPC `deduct_mco_coins`. Plano Phase 4.2 selado em `~/.claude/plans/floating-sleeping-sparrow.md`.
> 50	
> 51	**Sprint v6.1.1 selado em 2026-05-14** — viralmind BoK Suite Sealed: dívida documental do override consciente do BoK Gate quitada. 6 docs autorados (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) + `04-frd` reescrito de handbook CLAUDE.md → FRD real (32 FR + 14 NFR + matriz PR→FR). Ancorado nas 10 tabelas `vm_*` + 6 enums + Edge Functions `fetch-trends`/`canvas-execute`. Mesh seal `bok-scribe-seal-viralmind-v1` (`documentation_suite`, stability 0.85, revenue_impact R\$14M, embedded 768d). 7 OTDs registrados (destaques: `vector(1536)` vs padrão `768` sem índice HNSW — FMEA-VM-002 RPN 288; bucket `canvas-assets` público — FMEA-VM-003 RPN 140). BoK Gate do viralmind **liberado**. Sessão selada com ~51% de contexto — Canvas Studio Phase 4.2 diferida para sessão nova. 7463 nós · 100% embedded. 6 commits granulares. **Pendência conhecida (não desta sessão):** `docs/bok/gamificacao-nodes/` incompleta (5/9 docs) — rodar `/bok-scribe` ou completar antes de tocar o módulo.
> ```

## 🤖 Claude *(22:41:46)*


## 🤖 Claude *(22:42:05)*

Contexto completo coletado. Todos os artefatos verificados materialmente neste turno. Segue o brief.

═══════════════════════════════════════════════════════════
  HANDSON — v6.25.0 · Flywheel Resurrection + mcoCoins Calibration (2026-06-03)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **v6.25.0 — Flywheel ressuscitado (3 P0s) + calibração mcoCoins**
  Últimos commits:
    `c6faafe` — chore(sprint): update sprint-priorities — v6.25.0
    `bcbe79a` — docs(handoff): seal v6.25.0
    `a5b89e8` — docs(readme): v6.25.0
    `091b7da` — docs(processes): SOPs pipeline async + calibração + QA minter
    `73b8282` — feat(billing): calibra COIN_COST 4×-floor — IMAGE_GENERATION 3→9

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ — `git status` vazio · HEAD == `origin/main` (0/0, fetch feito) · scratch/ limpo

🏗️ **INFRA**
  mcorch_chroma:     Up 11 days (healthy) — Chroma API v2: **OK** (heartbeat respondeu)
  mcorch_claude_mem: Up 11 days (healthy)
  mega-brain-*:      daemon/webhook healthy · dashboard up (todos 11d)

🧠 **KNOWLEDGE MESH**
  **8769 nós · 9070 arestas** (fonte: HANDOFF GraphRAG State) — 100% embedded (768d HNSW cosine)
  Handoff node da seal: `5e1b6f32-7d32-4fbb-a1b7-1834e42d187e`

🔧 **TYPESCRIPT**
  Zero erros ✅ (`tsc --noEmit` limpo)

📚 **BoK SUITES (Master Execution Protocol)**
  Sealed (13/13 completas, 9 docs cada): aios-sql-bridge · canvas-design · constellation-v2 · conteudo-v2 · e2e-user-zero · gamificacao-nodes · marketing-hub · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · viralmind
  Incomplete: **nenhum** ✅
  ⚠️ GATE alert: **nenhum** — BoK Gate liberado para qualquer módulo

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional (LinkedIn auto-publica; Twitter ao subir tier; IG após App Review)
  Top gap (v6.25.0): **auditar drift deployado↔migrations** — a `async_orchestrate_step` foi hotfixada em prod **sem migration**; suspeitar de outras RPCs/fns

⚡ **PRÓXIMOS PASSOS** (prioridade)
  1. **🔴 Auditar drift deployado↔migrations** — o flywheel ficou morto desde 01-06 em parte porque uma RPC viva em prod divergia das migrations (`p_service_jwt_legacy`≠`p_service_key`). É integridade sistêmica: o que as migrations dizem ≠ o deployado. Varrer outras funções/RPCs.
  2. **🧹 Limpar/liberar artefatos de teste** — 5 `scheduled_posts` parqueados em 2027 (campanha `29b85b73` + adhoc) + 2 rascunhos WP de teste (`?p=13`/`?p=14`) — decisão Sovereign: apagar ou liberar.
  3. **Roadmap marketing-hub** — FR-MH-009 (Intent+HITL) · FR-MH-010 (AEO) · FR-MH-012 (BYOK) · Nurturing follow-up (entrega externa real + cron de avanço) · `functionName` nas 9 fns de fallback restantes.

⚠️ **ALERTAS**
  Nenhum bloqueador técnico ✅ (tsc 0 · containers healthy · worktree limpo · BoK completa).
  Contexto operacional (não-bloqueante):
  • **Twitter** não conectado (`CreditsDepleted`) — passo gera conteúdo mas não publica.
  • **[AGUARDANDO]** Atribuição de clique ML — Sovereign reporta quando maturar.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

O flywheel de conteúdo está **vivo e provado E2E** (run `89f18bea` auto-completou 6/6 passos). O candidato mais forte para esta sessão é o **#1 — auditoria de drift** (o incidente que matou o pipeline silenciosamente por 2 dias pode ter irmãos escondidos). Qual frente seguimos?

## 👤 User *(22:48:14)*

⚡ PRÓXIMOS PASSOS (prioridade)

🔴 Auditar drift deployado↔migrations — o flywheel ficou morto desde 01-06 em parte porque uma RPC viva em prod divergia das migrations (p_service_jwt_legacy≠p_service_key). É integridade sistêmica: o que as migrations dizem ≠ o deployado. Varrer outras funções/RPCs.
🧹 Limpar/liberar artefatos de teste — 5 scheduled_posts parqueados em 2027 (campanha 29b85b73 + adhoc) + 2 rascunhos WP de teste (?p=13/?p=14) — decisão Sovereign: apagar ou liberar.
Roadmap marketing-hub — FR-MH-009 (Intent+HITL) · FR-MH-010 (AEO) · FR-MH-012 (BYOK) · Nurturing follow-up (entrega externa real + cron de avanço) · functionName nas 9 fns de fallback restantes.

## 🤖 Claude *(22:49:10)*


## 🤖 Claude *(22:49:12)*

The Sovereign confirmed the priorities verbatim, with **#1 flagged 🔴 critical** — and it's exactly what I recommended. I'll execute the drift audit now. It's read-only (probe-first, materially verifiable, zero blast radius), so no GO gate needed to *audit*; any *fix* it surfaces will be separately GO-gated.

## 🤖 Claude *(22:49:13)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Drift audit: deployed \u2194 migrations",
  "summary": "Varredura sist\u00eamica de RPCs/fun\u00e7\u00f5es/triggers vivas em prod vs. o que as migrations declaram \u2014 ca\u00e7a aos irm\u00e3os do hotfix async_orchestrate_step"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Drift audit: deployed ↔ migrations". Continue your current work.'}]
> ```

## 🤖 Claude *(22:49:23)*


## 🤖 Claude *(22:49:27)*

**ORO triplet desta task:**
- **Operator:** MCORCH Master Execution Agent
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign — blast radius da *auditoria* = nulo (read-only); qualquer *fix* de drift descoberto será ação outward separada, GO-gated.

A auditoria depende de uma capacidade material: comparar o **deployado** (definições vivas em prod via `pg_get_functiondef`) contra o **declarado** (SQL nas migrations). Primeiro vou mapear a tooling — se eu não tiver como rodar SQL contra prod, declaro "cérebro sem mãos" (Lei 1) em vez de fabricar. Descoberta em paralelo:

## 🤖 Claude *(22:49:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== MIGRATIONS COUNT ===\"; ls supabase/migrations/*.sql 2>/dev/null | wc -l; echo \"=== MIGRATIONS (last 25 by name) ===\"; ls supabase/migrations/ 2>/dev/null | tail -25; echo \"=== EDGE FUNCTIONS ===\"; ls supabase/functions/ 2>/dev/null",
  "description": "Inventory migrations + edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === MIGRATIONS COUNT ===
> 93
> === MIGRATIONS (last 25 by name) ===
> 20260527012421_inspect_net_v3.sql
> 20260527012500_async_orchestrate_step_debug.sql
> 20260527012945_agent_metering_minimal.sql
> 20260528093200_add_asset_lineage_fields.sql
> 20260530183000_affiliate_tag_per_user.sql
> 20260530210000_meta_api_foundation.sql
> 20260531193000_fix_meta_config_column_privileges.sql
> 20260531200000_whatsapp_lead_engine.sql
> 20260531210000_meta_ads_metrics.sql
> 20260601000000_credential_encryption.sql
> 20260601000500_fix_meta_config_instead_of_trigger.sql
> 20260601000600_secure_definer_views.sql
> 20260601031300_constellation_v2_foundation.sql
> 20260601050000_embed_trigger_vault_key.sql
> 20260601060000_user_api_keys_apify_token.sql
> 20260602120000_wordpress_disconnect_rpc.sql
> 20260602130000_fix_user_api_keys_instead_of_double_fire.sql
> 20260602140000_vault_upsert_secret_idempotent_encrypt.sql
> 20260602150000_meta_social_instead_of_tenant_guard.sql
> 20260602160000_meta_social_disconnect_rpc.sql
> 20260603000000_marketing_hub_lead_core.sql
> 20260603025256_marketing_hub_campaign_core.sql
> 20260603040000_marketing_hub_customer360_view.sql
> 20260603050000_marketing_hub_nurturing.sql
> 20260603190000_fix_async_orchestrate_step_param_drift.sql
> === EDGE FUNCTIONS ===
> admin-manage-user
> agent-task-execute
> aios-chat
> aios-sql-bridge
> analyze-node
> analyze-sem
> analyze-seo
> autonomic-action
> auto-publish
> award-mco-coins
> campaign-run
> canvas-execute
> check-subscription
> check-video-status
> create-checkout
> create-portal
> data-export
> delete-account
> design-job-enqueue
> embed-mcorch-node
> fetch-trends
> generate-audio-script
> generate-content
> generate-image
> generate-video
> generate-video-script
> get-infra-status
> handle-ml-postback
> higgsfield-webhook
> instagram-webhook
> lead-score
> list-provider-models
> nurture-dispatch
> openrouter-swarm
> optimize-schedule
> orchestrate-content
> orchestrate-step
> process-affiliate-link
> publish-meta
> publish-social
> publish-wordpress
> refresh-social-token
> rescue-video
> search-constellation
> self-heal
> self-optimize
> _shared
> social-auth-callback
> social-auth-init
> stripe-webhook
> sync-knowledge-mesh
> sync-meta-ads
> test-api-key
> trigger-embeddings
> trigger-ingest
> tts-speak
> whatsapp-webhook
> ```

## 🤖 Claude *(22:49:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== prod SQL exec mechanisms in scripts ===\"; grep -rlE \"pg_get_functiondef|/database/query|supabase.com/v1/projects|exec_sql|management\" scripts/ 2>/dev/null | head -30; echo \"=== aios-sql-bridge refs ===\"; grep -rlE \"sql-bridge|aios.sql|sqlBridge\" scripts/ .claude/ 2>/dev/null | head -20",
  "description": "Find prod SQL execution mechanism"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === prod SQL exec mechanisms in scripts ===
> scripts/seed-marketing-hub-bok-seal.ts
> === aios-sql-bridge refs ===
> .claude/rules/survival.md
> .claude/worktrees/eager-brown-6ef0f1/README.md
> .claude/worktrees/eager-brown-6ef0f1/.claude/rules/survival.md
> .claude/worktrees/eager-brown-6ef0f1/HANDOFF.md
> .claude/worktrees/eager-brown-6ef0f1/.claude/context/survival-audit-v2.md
> .claude/worktrees/eager-brown-6ef0f1/.claude/context/execution-plan-oe661-carryovers.md
> .claude/worktrees/eager-brown-6ef0f1/.claude/context/audit-2026-05-19-oe661-debt-sweep.md
> .claude/worktrees/eager-brown-6ef0f1/.claude/context/survival-audit-v1.md
> .claude/worktrees/eager-brown-6ef0f1/.claude/context/sprint-priorities.md
> .claude/worktrees/eager-brown-6ef0f1/supabase/functions/aios-sql-bridge/index.ts
> .claude/worktrees/eager-brown-6ef0f1/.agents/rules/survival.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/05-sdd.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/02-brd.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/01-mrd.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/07-process-flow.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/06-data-model.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/04-frd.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/08-quality-metrics.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/00-index.md
> .claude/worktrees/eager-brown-6ef0f1/docs/bok/aios-sql-bridge/03-prd.md
> ```

## 🤖 Claude *(22:49:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== .env keys present (NAMES ONLY, no values) ===\"; [ -f .env ] && grep -oE \"^[A-Z_]+=\" .env | tr -d '=' || echo \"no .env\"; echo \"=== project ref from config ===\"; [ -f supabase/config.toml ] && grep -E \"project_id|ref\" supabase/config.toml | head -5 || echo \"no config.toml project ref line\"",
  "description": "Env key names + project ref (no secret values)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === .env keys present (NAMES ONLY, no values) ===
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
> === project ref from config ===
> project_id = "bcyvddsykvehvpwstlfa"
> [functions.refresh-social-token]
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> === aios-sql-bridge SDD head ===
> # 05 — System Design Document — aios-sql-bridge
> 
> **BoK Lens:** SWEBOK v4 + CISSP CBK
> **Sealed:** 2026-05-19
> **Author:** MCORCH Master Execution Agent (Lei 1 — código fonte primário em `supabase/functions/aios-sql-bridge/`)
> **Reviewer:** Sovereign
> **Closes:** OTD-SSP01-001 (RPN 240 · SLA 2026-05-24 — bypass BoK Gate de v6.5.0)
> 
> ---
> 
> ## 1. Purpose & Scope
> 
> `aios-sql-bridge` é uma Supabase Edge Function (Deno) que expõe **SELECT controlado** sobre 4 tabelas operacionais do MCORCH para a camada AIOS (skills internas, dashboards, claude-mem agents). Cumpre o papel de **Monitor primary surface** no ciclo MAPE-K:
> 
> - **Habilita** introspecção operacional do Sovereign sem SQL bruto, sem acesso direto ao banco, sem expor service-role key fora do edge runtime.
> - **Bloqueia** acesso a colunas sensíveis (tokens, secrets, PII) por **defense-in-depth dupla**: whitelist explícito + regex global de FORBIDDEN_COLUMN_PATTERNS.
> - **Audita** cada query (success + falha) em duas tabelas (`usage_tracking`, `infra_health_logs`).
> - **Limita** abuso via gate de `admin` role + quota de 100 queries/dia/user.
> 
> **Out of scope:** INSERT/UPDATE/DELETE (read-only por design), raw SQL execution, dados de outros usuários sem admin role.
> 
> ---
> 
> ## 2. Architecture
> 
> ### 2.1 Topologia (component diagram em ASCII)
> 
> ```
> ┌────────────────────────────────────────────────────────────────────┐
> │ Caller (skill, dashboard, AIOS agent)                               │
> │   POST /functions/v1/aios-sql-bridge                                │
> │   Authorization: Bearer <JWT>                                       │
> │   { table, select?, filters?, order?, limit?, offset? }             │
> └──────────────────────────┬─────────────────────────────────────────┘
>                            ▼
> ┌────────────────────────────────────────────────────────────────────┐
> │ aios-sql-bridge Edge Function (Deno runtime)                        │
> │                                                                     │
> │ ┌─────────────┐  ┌────────────┐  ┌──────────┐  ┌──────────────┐    │
> │ │ Auth gate   │→ │ Admin gate │→ │ Quota gate│→│ Body parser   │    │
> │ │ getUser()   │  │ has_role() │  │ usage_tr.│  │ + Filter Obj  │    │
> │ │ (401/403)   │  │ (403)      │  │ (429)    │  │ contract      │    │
> │ └─────────────┘  └────────────┘  └──────────┘  └──────┬───────┘    │
> │                                                       ▼            │
> │                                          ┌──────────────────────┐  │
> │                                          │ Validators           │  │
> │                                          │ - select clause      │  │
> │                                          │ - filters (op+col)   │  │
> │                                          │ - order col          │  │
> │                                          │ - limit/offset clamp │  │
> │                                          │ - FORBIDDEN regex    │  │
> │                                          └──────────┬───────────┘  │
> │                                                     ▼              │
> │                                       ┌────────────────────────┐   │
> │                                       │ supabase-js builder    │   │
> │                                       │ .from(table)           │   │
> │                                       │ .select() .eq()...     │   │
> │                                       │ .order() .range()      │   │
> │                                       └──────────┬─────────────┘   │
> │                                                  ▼                 │
> === SQL bridge script files ===
> -rw-rw-r--  1 ubuntu ubuntu 13125 Jun  1 10:10 bridge-mesh-to-openclaw.ts
> -rwxr-xr-x  1 ubuntu ubuntu 11067 Jun  1 10:10 design-bridge.ts
> -rwxrwxr-x  1 ubuntu ubuntu  3122 May 19 19:14 nightly-bridge-refresh.sh
> -rw-rw-r--  1 ubuntu ubuntu 33197 Jun  1 10:10 opencode-bridge.ts
> audit-canvas-ui.ts
> audit-lucide-imports.ts
> e2e-user-zero
> extract-manifest.ts
> firecrawl-ml-probe.ts
> gen-magiclink.ts
> gen-user-jwt.ts
> health-pulse.ts
> run-audit.ts
> smoke-attribution.ts
> smoke-campaign-run.ts
> smoke-constellation-v2-router.ts
> smoke-customer360.ts
> smoke-marketing-hub.ts
> smoke-nurture.ts
> test-es256-jwt-verification.ts
> test-publish-meta-smoke.ts
> test-sync-meta-ads.ts
> test-whatsapp-webhook.ts
> types.ts
> verifiers.ts
> ```

## 🤖 Claude *(22:49:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== aios-sql-bridge SDD head ===\"; [ -f docs/bok/aios-sql-bridge/05-sdd.md ] && head -60 docs/bok/aios-sql-bridge/05-sdd.md || echo \"no SDD\"; echo \"=== SQL bridge script files ===\"; ls -la scripts/ 2>/dev/null | grep -iE \"sql|bridge|query\" ; ls scripts/qa/ 2>/dev/null | head -40",
  "description": "Read SQL bridge SDD + locate bridge scripts"
}
```

## 🤖 Claude *(22:50:15)*


## 🤖 Claude *(22:50:17)*

93 migrations · 57 edge functions. Key finding: `aios-sql-bridge` is **read-only by design** (4 tables, no `pg_get_functiondef`) — won't serve the audit. The material path is the Supabase **Management API `/database/query`** (what prior sessions used: "pg_get_functiondef ... via Management API") or the CLI's `db diff`. First I must confirm I actually have SQL-against-prod capability — otherwise it's "cérebro sem mãos" (Lei 1). Probing the token/CLI + studying the *known* drift signature to learn the hunting pattern:

## 🤖 Claude *(22:50:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== SUPABASE_ACCESS_TOKEN (set?/no value) ===\"; [ -n \"$SUPABASE_ACCESS_TOKEN\" ] && echo \"SET\" || echo \"UNSET\"; echo \"=== SB_SECRET_KEY (set?) ===\"; set -a; [ -f .env ] && . ./.env >/dev/null 2>&1; set +a; [ -n \"$SB_SECRET_KEY\" ] && echo \"SB_SECRET_KEY SET\" || echo \"SB_SECRET_KEY UNSET\"; [ -n \"$SUPABASE_ACCESS_TOKEN\" ] && echo \"ACCESS_TOKEN now SET (from .env)\" || echo \"ACCESS_TOKEN still UNSET\"; echo \"=== ~/.supabase dir (names only) ===\"; ls -a ~/.supabase/ 2>/dev/null || echo \"no ~/.supabase\"; echo \"=== supabase CLI ===\"; npx supabase --version 2>&1 | head -2",
  "description": "Probe management token + CLI auth capability"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === SUPABASE_ACCESS_TOKEN (set?/no value) ===
> UNSET
> === SB_SECRET_KEY (set?) ===
> SB_SECRET_KEY SET
> ACCESS_TOKEN still UNSET
> === ~/.supabase dir (names only) ===
> .
> ..
> access-token
> telemetry.json
> traces
> === supabase CLI ===
> 2.92.1
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> ```

## 🤖 Claude *(22:50:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== migrations mentioning async_orchestrate_step ===\"; grep -rl \"async_orchestrate_step\" supabase/migrations/ 2>/dev/null; echo \"=== the param-drift FIX migration (full) ===\"; cat supabase/migrations/20260603190000_fix_async_orchestrate_step_param_drift.sql",
  "description": "Study known drift signature + migration history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === migrations mentioning async_orchestrate_step ===
> supabase/migrations/20260527012500_async_orchestrate_step_debug.sql
> supabase/migrations/20260526202000_async_orchestrate_step.sql
> supabase/migrations/20260603190000_fix_async_orchestrate_step_param_drift.sql
> === the param-drift FIX migration (full) ===
> -- Fix: async_orchestrate_step parameter drift broke the orchestration auto-chain (P0).
> --
> -- Root cause (material, 2026-06-03): an out-of-band prod hotfix during the 2026-06-01 key migration renamed this
> -- function's key parameter to `p_service_jwt_legacy`, but the callers (orchestrate-content, orchestrate-step) invoke
> -- it by NAME with `p_service_key`. PostgREST/PL named-arg resolution then fails (PGRST202 "no function matches"),
> -- so the pg_net dispatch silently no-ops → every pipeline_run stalls at status='running' with an empty steps[].
> -- The rename was never captured as a migration (migrations on disk still declare `p_service_key`), so the function
> -- definition had drifted away from version control.
> --
> -- This realigns the signature to the callers' contract (`p_service_key`) and GRANTs service_role EXECUTE (the edge
> -- admin client runs as service_role; the original `REVOKE FROM public` left service_role ungranted). orchestrate-step
> -- is now `verify_jwt = false` (config.toml), so the opaque `sb_secret_` key works as the Bearer with no JWT check.
> --
> -- SECURITY: SECURITY DEFINER + empty search_path; net.http_post is schema-qualified. EXECUTE is revoked from
> -- public/anon/authenticated (SSRF guard — only the server-side service_role may trigger an outbound HTTP call) and
> -- granted solely to service_role. The function takes a caller-supplied URL/key, so locking the grant down is essential.
> 
> -- Drop every overload of the name first: the deployed positional order is unknown after the out-of-band rename,
> -- and a stale overload would leave PostgREST ambiguous between two signatures.
> DO $$
> DECLARE r record;
> BEGIN
>   FOR r IN
>     SELECT oid::regprocedure AS sig
>     FROM pg_proc
>     WHERE proname = 'async_orchestrate_step'
>       AND pronamespace = 'public'::regnamespace
>   LOOP
>     EXECUTE 'DROP FUNCTION ' || r.sig;
>   END LOOP;
> END $$;
> 
> CREATE FUNCTION public.async_orchestrate_step(
>   p_supabase_url text,
>   p_service_key  text,
>   p_run_id       uuid,
>   p_step         text
> )
> RETURNS void
> LANGUAGE plpgsql
> SECURITY DEFINER
> SET search_path = ''
> AS $$
> BEGIN
>   PERFORM net.http_post(
>     url     := p_supabase_url || '/functions/v1/orchestrate-step',
>     headers := jsonb_build_object(
>       'Content-Type',  'application/json',
>       'Authorization', 'Bearer ' || p_service_key
>     ),
>     body    := jsonb_build_object(
>       'run_id', p_run_id::text,
>       'step',   p_step
>     )
>   );
> END;
> $$;
> 
> -- SSRF guard: only the service_role (edge admin client) may invoke; never anon/authenticated/public.
> REVOKE ALL ON FUNCTION public.async_orchestrate_step(text, text, uuid, text) FROM PUBLIC, anon, authenticated;
> GRANT EXECUTE ON FUNCTION public.async_orchestrate_step(text, text, uuid, text) TO service_role;
> ```

## 🤖 Claude *(22:51:16)*


## 🤖 Claude *(22:51:19)*

Capability confirmed materially: `~/.supabase/access-token` exists (CLI logged in) → I can reach the **Management API `/database/query`** for read-only `pg_get_functiondef`/`pg_policies` introspection. Project ref `bcyvddsykvehvpwstlfa`. And the known-drift signature is now precise: a **prod hotfix renamed a function param** (`p_service_key`→`p_service_jwt_legacy`) that **no migration ever captured** → live definition diverged from version control.

So the hunting pattern is clear. Let me start with the cheapest, highest-signal check — **migration ledger parity** (applied-in-prod vs files-on-disk) — which doubles as my connectivity proof. The token stays in a variable, never echoed (per the key-hygiene memory).

## 🤖 Claude *(22:51:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nURL=\"https://api.supabase.com/v1/projects/$REF/database/query\"\n# Connectivity + ledger: live applied migration versions\njq -nc --arg q \"SELECT version FROM supabase_migrations.schema_migrations ORDER BY version\" \\\n  | curl -s -X POST \"$URL\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" --data-binary @- > /tmp/ledger.json\necho \"=== response type ===\"; jq -r 'type' /tmp/ledger.json 2>/dev/null || { echo \"NON-JSON:\"; head -c 500 /tmp/ledger.json; exit 0; }\necho \"=== applied count (prod) ===\"; jq 'length' /tmp/ledger.json 2>/dev/null\necho \"=== disk migration count ===\"; ls supabase/migrations/*.sql | wc -l",
  "description": "Management API connectivity + ledger parity check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === response type ===
> object
> === applied count (prod) ===
> 1
> === disk migration count ===
> 93
> ```

## 🤖 Claude *(22:51:27)*


## 🤖 Claude *(22:51:27)*

The response is an object (likely an error or wrapper), not the row array I expected. Let me inspect its actual shape.

## 🤖 Claude *(22:51:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== keys ===\"; jq -r 'keys' /tmp/ledger.json 2>/dev/null; echo \"=== raw (first 600 chars) ===\"; head -c 600 /tmp/ledger.json; echo",
  "description": "Inspect Management API response shape"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === keys ===
> [
>   "message"
> ]
> === raw (first 600 chars) ===
> {"message":"Unexpected token 'n', \"null\n\" is not valid JSON"}
> ```

## 🤖 Claude *(22:51:36)*


## 🤖 Claude *(22:51:37)*

Found my bug — I omitted the jq filter `'{query:$q}'`, so it posted `null` as the body. The channel itself works (the API responded). Fixing the payload construction:

## 🤖 Claude *(22:51:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nURL=\"https://api.supabase.com/v1/projects/bcyvddsykvehvpwstlfa/database/query\"\njq -nc --arg q \"SELECT version FROM supabase_migrations.schema_migrations ORDER BY version\" '{query:$q}' \\\n  | curl -s -X POST \"$URL\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" --data-binary @- > /tmp/ledger.json\necho \"=== type ===\"; jq -r 'type' /tmp/ledger.json\necho \"=== applied count (prod ledger) ===\"; jq 'length' /tmp/ledger.json\necho \"=== first/last applied ===\"; jq -r '.[0].version, .[-1].version' /tmp/ledger.json",
  "description": "Ledger query with correct JSON payload"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === type ===
> array
> === applied count (prod ledger) ===
> 93
> === first/last applied ===
> 20260402014040
> 20260603190000
> ```

## 🤖 Claude *(22:51:46)*


## 🤖 Claude *(22:51:47)*

Channel works. 93 applied in prod ledger = 93 files on disk. But equal counts could hide a swap — I need the **exact set diff** (a hotfix-applied version with no file, or a committed file never pushed).

## 🤖 Claude *(22:51:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\njq -r '.[].version' /tmp/ledger.json | sort -u > /tmp/applied.txt\nls supabase/migrations/*.sql | sed -E 's#.*/([0-9]+)_.*#\\1#' | sort -u > /tmp/ondisk.txt\necho \"=== applied-in-prod but NO file on disk (out-of-band / hotfix) ===\"; comm -23 /tmp/applied.txt /tmp/ondisk.txt || true\necho \"=== file on disk but NOT applied in prod (never pushed) ===\"; comm -13 /tmp/applied.txt /tmp/ondisk.txt || true\necho \"=== ledger parity verdict ===\"; if diff -q /tmp/applied.txt /tmp/ondisk.txt >/dev/null; then echo \"\u2705 EXACT MATCH \u2014 93 applied == 93 on disk, same set\"; else echo \"\u26a0\ufe0f DRIFT in migration ledger (see above)\"; fi",
  "description": "Exact set diff: prod ledger vs disk files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === applied-in-prod but NO file on disk (out-of-band / hotfix) ===
> === file on disk but NOT applied in prod (never pushed) ===
> === ledger parity verdict ===
> ✅ EXACT MATCH — 93 applied == 93 on disk, same set
> ```

## 🤖 Claude *(22:53:01)*


## 🤖 Claude *(22:53:03)*

**Ledger parity is clean** — but that's expected and *not* reassuring on its own: the async hotfix renamed a param via direct SQL, which never touches `schema_migrations`. So ledger parity being perfect **does not rule out object-level drift** — that's precisely the class that bit us. The real hunt is live-definition vs declared-definition.

Let me set up a read-only Management API helper (token isolated in one place, never echoed) and pull the **live function inventory** — the backbone of the audit.

## 🤖 Claude *(22:53:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat > /tmp/mq.sh <<'EOF'\n#!/usr/bin/env bash\n# Read-only Management API query helper for drift audit. SQL on stdin \u2192 JSON on stdout.\nTOKEN=$(cat ~/.supabase/access-token)\nURL=\"https://api.supabase.com/v1/projects/bcyvddsykvehvpwstlfa/database/query\"\nSQL=$(cat)\njq -nc --arg q \"$SQL\" '{query:$q}' \\\n  | curl -s -X POST \"$URL\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" --data-binary @-\nEOF\nchmod +x /tmp/mq.sh\n# L1 \u2014 live public function inventory\ncat <<'SQL' | /tmp/mq.sh > /tmp/live_funcs.json\nSELECT p.proname AS name,\n       pg_get_function_arguments(p.oid) AS args,\n       p.prosecdef AS secdef,\n       COALESCE(array_to_string(p.proconfig,'; '),'') AS config,\n       p.prokind::text AS kind\nFROM pg_proc p\nJOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public'\nORDER BY p.proname;\nSQL\necho \"=== type ===\"; jq -r 'type' /tmp/live_funcs.json\necho \"=== live public functions (count) ===\"; jq 'length' /tmp/live_funcs.json\necho \"=== SECURITY DEFINER count ===\"; jq '[.[]|select(.secdef==true)]|length' /tmp/live_funcs.json\necho \"=== kinds (f=func,a=agg,w=window,p=proc) ===\"; jq -r 'group_by(.kind)|map({(.[0].kind):length})|add' /tmp/live_funcs.json",
  "description": "Create read-only helper + pull live function inventory"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === type ===
> array
> === live public functions (count) ===
> 154
> === SECURITY DEFINER count ===
> 30
> === kinds (f=func,a=agg,w=window,p=proc) ===
> {
>   "a": 4,
>   "f": 150
> }
> ```

## 🤖 Claude *(22:53:21)*


## 🤖 Claude *(22:53:23)*

154 includes pgvector/extension functions (the 4 aggregates + many `public` vector ops). I must isolate **our** functions (migration- or hotfix-created) by excluding extension-owned objects via `pg_depend`. Then cross-reference names against migrations.

## 🤖 Claude *(22:53:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\n# OUR functions only (exclude extension-owned)\ncat <<'SQL' | /tmp/mq.sh > /tmp/our_funcs.json\nSELECT p.proname AS name,\n       pg_get_function_arguments(p.oid) AS args,\n       p.prosecdef AS secdef,\n       COALESCE(array_to_string(p.proconfig,'; '),'') AS config\nFROM pg_proc p\nJOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public'\n  AND p.prokind='f'\n  AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.objid=p.oid AND d.deptype='e')\nORDER BY p.proname;\nSQL\necho \"=== OUR live functions (count) ===\"; jq 'length' /tmp/our_funcs.json\njq -r '.[].name' /tmp/our_funcs.json | sort -u > /tmp/live_fn_names.txt\necho \"=== distinct live names ===\"; wc -l < /tmp/live_fn_names.txt\n# Function names DECLARED in migrations\ngrep -rhoiE 'CREATE (OR REPLACE )?FUNCTION (public\\.)?\"?[a-z_][a-z0-9_]*' supabase/migrations/ \\\n  | sed -E 's/.*FUNCTION (public\\.)?\"?//I' | tr 'A-Z' 'a-z' | sort -u > /tmp/decl_fn_names.txt\necho \"=== distinct names declared in migrations ===\"; wc -l < /tmp/decl_fn_names.txt\necho \"\"\necho \"=== \u26a0\ufe0f LIVE in prod but NEVER declared in any migration (out-of-band creations) ===\"\ncomm -23 /tmp/live_fn_names.txt /tmp/decl_fn_names.txt\necho \"\"\necho \"=== declared in migrations but NOT live (failed/dropped) ===\"\ncomm -13 /tmp/live_fn_names.txt /tmp/decl_fn_names.txt",
  "description": "Isolate our functions, cross-ref live vs migration-declared names"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === OUR live functions (count) ===
> 36
> === distinct live names ===
> 36
> === distinct names declared in migrations ===
> 37
> 
> === ⚠️ LIVE in prod but NEVER declared in any migration (out-of-band creations) ===
> rls_auto_enable
> 
> === declared in migrations but NOT live (failed/dropped) ===
> does
> preserves
> ```

## 🤖 Claude *(22:53:52)*


## 🤖 Claude *(22:53:54)*

Three hits to triage. `does`/`preserves` are almost certainly grep noise (not plausible function names — likely matched inside comments). The real signal: **`rls_auto_enable` is live in prod but no migration declares it** — a candidate out-of-band creation. Investigating all three materially:

## 🤖 Claude *(22:53:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== false-positive check: 'does'/'preserves' context in migrations ===\"\ngrep -rniE 'FUNCTION[^;]*(does|preserves)' supabase/migrations/ | head -8\necho \"\"\necho \"=== does ANY migration mention rls_auto_enable at all? ===\"\ngrep -rni \"rls_auto_enable\" supabase/migrations/ | head -5 || echo \"\u2192 ZERO references in migrations/\"\necho \"\"\necho \"=== rls_auto_enable: live definition + extension dependency ===\"\ncat <<'SQL' | /tmp/mq.sh | jq -r '.[0] // \"NULL\"'\nSELECT pg_get_functiondef(p.oid) AS def,\n       p.prosecdef,\n       EXISTS(SELECT 1 FROM pg_depend d WHERE d.objid=p.oid AND d.deptype='e') AS ext_owned,\n       (SELECT string_agg(t.tgname,', ') FROM pg_trigger t WHERE t.tgfoid=p.oid) AS used_by_triggers,\n       (SELECT string_agg(e.evtname,', ') FROM pg_event_trigger e WHERE e.evtfoid=p.oid) AS used_by_event_triggers\nFROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public' AND p.proname='rls_auto_enable';\nSQL",
  "description": "Triage false positives + investigate rls_auto_enable origin"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === false-positive check: 'does'/'preserves' context in migrations ===
> supabase/migrations/20260527004739_soft_reset_account_rpc.sql:11:--   [x] No PII exposure (function deletes/preserves; never returns sensitive payload)
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:45:-- their bindings (CREATE OR REPLACE FUNCTION preserves the function oid) — no trigger re-create.
> supabase/migrations/20260525173500_drop_deduct_mco_coins_overload.sql:4:-- Root cause (OTD-LEDGER-OVERLOAD, 2026-05-25): CREATE OR REPLACE FUNCTION does not replace
> 
> === does ANY migration mention rls_auto_enable at all? ===
> 
> === rls_auto_enable: live definition + extension dependency ===
> {
>   "def": "CREATE OR REPLACE FUNCTION public.rls_auto_enable()\n RETURNS event_trigger\n LANGUAGE plpgsql\n SECURITY DEFINER\n SET search_path TO 'pg_catalog'\nAS $function$\nDECLARE\n  cmd record;\nBEGIN\n  FOR cmd IN\n    SELECT *\n    FROM pg_event_trigger_ddl_commands()\n    WHERE command_tag IN ('CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO')\n      AND object_type IN ('table','partitioned table')\n  LOOP\n     IF cmd.schema_name IS NOT NULL AND cmd.schema_name IN ('public') AND cmd.schema_name NOT IN ('pg_catalog','information_schema') AND cmd.schema_name NOT LIKE 'pg_toast%' AND cmd.schema_name NOT LIKE 'pg_temp%' THEN\n      BEGIN\n        EXECUTE format('alter table if exists %s enable row level security', cmd.object_identity);\n        RAISE LOG 'rls_auto_enable: enabled RLS on %', cmd.object_identity;\n      EXCEPTION\n        WHEN OTHERS THEN\n          RAISE LOG 'rls_auto_enable: failed to enable RLS on %', cmd.object_identity;\n      END;\n     ELSE\n        RAISE LOG 'rls_auto_enable: skip % (either system schema or not in enforced list: %.)', cmd.object_identity, cmd.schema_name;\n     END IF;\n  END LOOP;\nEND;\n$function$\n",
>   "prosecdef": true,
>   "ext_owned": false,
>   "used_by_triggers": null,
>   "used_by_event_triggers": "ensure_rls"
> }
> ```

## 🤖 Claude *(22:54:28)*


## 🤖 Claude *(22:54:31)*

Confirmed: `does`/`preserves` are **grep noise** from code comments (`-- ...deletes/preserves...`, `CREATE OR REPLACE FUNCTION preserves the function oid` inside a comment) — not real missing functions. 

But **`rls_auto_enable` is a genuine out-of-band object**: an `event_trigger` function wired to event trigger `ensure_rls` that auto-enables RLS on every new `public` table — `SECURITY DEFINER`, **zero references in migrations/**, not extension-owned. Benign (it *enforces* the CLAUDE.md "RLS by default" mandate) but undocumented drift. Let me pin its origin and run the SECURITY DEFINER / search_path consistency pass (analyzing data I already pulled):

## 🤖 Claude *(22:54:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== rls_auto_enable owner + ensure_rls event trigger + repo-wide presence ===\"\ncat <<'SQL' | /tmp/mq.sh | jq -r '.[0]'\nSELECT pg_get_userbyid(p.proowner) AS owner,\n       (SELECT e.evtenabled::text FROM pg_event_trigger e WHERE e.evtname='ensure_rls') AS ensure_rls_enabled,\n       (SELECT pg_get_userbyid(e.evtowner) FROM pg_event_trigger e WHERE e.evtname='ensure_rls') AS et_owner\nFROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public' AND p.proname='rls_auto_enable';\nSQL\necho \"--- referenced ANYWHERE in repo (not just migrations)? ---\"\ngrep -rni \"rls_auto_enable\\|ensure_rls\" --include=*.sql --include=*.ts --include=*.md . 2>/dev/null | grep -v node_modules | grep -v \".claude/worktrees\" | head -5 || echo \"\u2192 NOWHERE in tracked repo\"\necho \"\"\necho \"=== L3: SECURITY DEFINER functions WITHOUT locked search_path (security drift signal) ===\"\njq -r '.[] | select(.secdef==true) | select((.config|test(\"search_path\"))|not) | \"\u26a0\ufe0f  \"+.name+\"(\"+.args+\")  config=[\"+.config+\"]\"' /tmp/our_funcs.json\necho \"--- (none above = all SECURITY DEFINER fns have search_path set) ---\"\necho \"\"\necho \"=== all 36 our-functions: secdef + config ===\"\njq -r '.[] | (if .secdef then \"DEF \" else \"inv \" end)+.name+\"  \u2192  [\"+.config+\"]\"' /tmp/our_funcs.json",
  "description": "Pin rls_auto_enable origin + SECURITY DEFINER search_path audit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === rls_auto_enable owner + ensure_rls event trigger + repo-wide presence ===
> {
>   "owner": "postgres",
>   "ensure_rls_enabled": "O",
>   "et_owner": "postgres"
> }
> --- referenced ANYWHERE in repo (not just migrations)? ---
> 
> === L3: SECURITY DEFINER functions WITHOUT locked search_path (security drift signal) ===
> ⚠️  add_user_score(user_id_param uuid, score_to_add integer)  config=[]
> ⚠️  award_mco_coins(p_user_id uuid, p_amount integer, p_action text, p_context jsonb DEFAULT '{}'::jsonb)  config=[]
> ⚠️  boost_aios_conversation(p_conv_id uuid, p_amount integer DEFAULT 1)  config=[]
> ⚠️  inspect_net_requests(p_limit integer DEFAULT 5)  config=[]
> ⚠️  inspect_net_responses(p_limit integer DEFAULT 5)  config=[]
> ⚠️  inspect_net_schema()  config=[]
> ⚠️  trigger_sync_knowledge_mesh()  config=[]
> --- (none above = all SECURITY DEFINER fns have search_path set) ---
> 
> === all 36 our-functions: secdef + config ===
> DEF add_mco_coins  →  [search_path=public]
> DEF add_user_score  →  []
> DEF async_orchestrate_step  →  [search_path=""]
> DEF award_mco_coins  →  []
> DEF boost_aios_conversation  →  []
> inv calc_agent_cost_mcoin  →  []
> DEF decay_mcorch_stability  →  [search_path=public]
> DEF deduct_mco_coins  →  [search_path=public]
> DEF delete_account  →  [search_path=public]
> DEF disconnect_meta  →  [search_path=""]
> DEF disconnect_social  →  [search_path=""]
> DEF disconnect_wordpress  →  [search_path=""]
> DEF erase_lead  →  [search_path=""]
> DEF handle_new_user  →  [search_path=public]
> inv handle_updated_at  →  [search_path=public]
> DEF has_role  →  [search_path=public]
> DEF inspect_net_requests  →  []
> DEF inspect_net_responses  →  []
> DEF inspect_net_schema  →  []
> inv match_mcorch_memory_v2  →  []
> DEF match_mcorch_nodes  →  [search_path=public]
> DEF mcorch_embed_on_insert  →  [search_path=public]
> DEF rls_auto_enable  →  [search_path=pg_catalog]
> DEF seed_crew_template  →  [search_path=public]
> DEF soft_reset_account  →  [search_path=public]
> DEF trg_encrypt_meta_config  →  [search_path=""]
> DEF trg_encrypt_social_accounts  →  [search_path=""]
> DEF trg_encrypt_user_api_keys  →  [search_path=""]
> DEF trg_instead_of_meta_config  →  [search_path=""]
> DEF trg_instead_of_social_accounts  →  [search_path=""]
> DEF trg_instead_of_user_api_keys  →  [search_path=""]
> DEF trigger_sync_knowledge_mesh  →  []
> inv update_aios_conversations_updated_at  →  []
> inv update_updated_at_column  →  []
> DEF vault_upsert_secret  →  [search_path=""]
> inv vm_update_updated_at  →  []
> ```

## 🤖 Claude *(22:55:08)*


## 🤖 Claude *(22:55:12)*

Two real signals now:

1. **`rls_auto_enable`**: owner `postgres`, event trigger `ensure_rls` **enabled**, zero repo references → confirmed benign-but-undocumented out-of-band object (enforces RLS-by-default — *desirable*, but uncaptured in version control).

2. **7 SECURITY DEFINER functions with NO locked `search_path`** — including the financial RPC **`award_mco_coins`** and `add_user_score`, `boost_aios_conversation`. That's a search-path-injection weakness, and it violates the project's own consistent `search_path=''`/`public` standard.

The decisive question for *this* audit: is that **drift** (migration sets search_path, live got stripped by a hotfix — like async) or a **latent standard gap** (the migration itself never set it)? Different category, different fix. Checking each of the 7 against its declaring migration:

## 🤖 Claude *(22:55:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nfor fn in add_user_score award_mco_coins boost_aios_conversation inspect_net_requests inspect_net_responses inspect_net_schema trigger_sync_knowledge_mesh; do\n  echo \"\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 $fn \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\"\n  files=$(grep -rlE \"CREATE (OR REPLACE )?FUNCTION (public\\.)?$fn\\b\" supabase/migrations/ 2>/dev/null | sort)\n  if [ -z \"$files\" ]; then echo \"  \u26a0\ufe0f NO migration CREATEs this \u2192 out-of-band OR created inline\"; \n  else\n    latest=$(echo \"$files\" | tail -1)\n    echo \"  declared in: $(echo \"$files\" | xargs -n1 basename | tr '\\n' ' ')\"\n    echo \"  LATEST: $(basename \"$latest\")\"\n    # does the latest migration set search_path anywhere for this fn's block?\n    if grep -qiE \"search_path\" \"$latest\"; then echo \"  \u2192 migration SETS search_path somewhere \u2705 (verify it's on THIS fn)\"; else echo \"  \u2192 migration does NOT set search_path \u274c (latent gap, NOT drift)\"; fi\n  fi\ndone",
  "description": "Classify each of the 7: drift vs latent standard gap"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ════════ add_user_score ════════
>   declared in: 20260417000000_gamification_engine.sql 
>   LATEST: 20260417000000_gamification_engine.sql
>   → migration does NOT set search_path ❌ (latent gap, NOT drift)
> ════════ award_mco_coins ════════
>   declared in: 20260508100000_mcoin_transactions.sql 
>   LATEST: 20260508100000_mcoin_transactions.sql
>   → migration does NOT set search_path ❌ (latent gap, NOT drift)
> ════════ boost_aios_conversation ════════
>   declared in: 20260502120000_aios_conversations.sql 
>   LATEST: 20260502120000_aios_conversations.sql
>   → migration does NOT set search_path ❌ (latent gap, NOT drift)
> ════════ inspect_net_requests ════════
>   declared in: 20260527012332_inspect_net_request.sql 20260527012421_inspect_net_v3.sql 
>   LATEST: 20260527012421_inspect_net_v3.sql
>   → migration does NOT set search_path ❌ (latent gap, NOT drift)
> ════════ inspect_net_responses ════════
>   declared in: 20260527012253_inspect_net_responses_rpc.sql 
>   LATEST: 20260527012253_inspect_net_responses_rpc.sql
>   → migration does NOT set search_path ❌ (latent gap, NOT drift)
> ════════ inspect_net_schema ════════
>   declared in: 20260527012404_inspect_net_v2.sql 
>   LATEST: 20260527012404_inspect_net_v2.sql
>   → migration does NOT set search_path ❌ (latent gap, NOT drift)
> ════════ trigger_sync_knowledge_mesh ════════
>   declared in: 20260423205725_knowledge_mesh_init.sql 
>   LATEST: 20260423205725_knowledge_mesh_init.sql
>   → migration does NOT set search_path ❌ (latent gap, NOT drift)
> ```

## 🤖 Claude *(22:55:56)*


## 🤖 Claude *(22:55:59)*

**Critical classification:** all 7 are **latent security gaps, NOT drift** — the migrations themselves never set `search_path` (they predate the June hardening standard). So deployed == declared for these. They're real tech debt (esp. `award_mco_coins` — a SECURITY DEFINER financial RPC open to search-path injection), but a *separate* hardening track, not the deployed↔migration drift this audit targets. Correctly filed, not conflated.

Now the **most important layer** — the actual async-class bug was a **signature/caller-contract mismatch** (callers invoke `p_service_key`, live had `p_service_jwt_legacy` → silent PGRST202). Let me hunt that across every RPC: names called in code that don't exist live, then arg-key mismatches.

## 🤖 Claude *(22:56:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\n# Pass A \u2014 every RPC name invoked from client/edge code\ngrep -rhoE \"\\.rpc\\(\\s*['\\\"][a-zA-Z_][a-zA-Z0-9_]*['\\\"]\" src supabase/functions packages 2>/dev/null \\\n  | sed -E \"s/.*['\\\"]([a-zA-Z0-9_]+)['\\\"].*/\\1/\" | sort -u > /tmp/rpc_called.txt\necho \"=== distinct RPC names called in code ===\"; cat /tmp/rpc_called.txt | tr '\\n' ' '; echo\necho \"\"\n# Live function names (already have for our funcs; but rpc may call extension/other \u2192 use ALL public live names)\njq -r '.[].name' /tmp/live_funcs.json | sort -u > /tmp/live_all_names.txt\necho \"=== \u26a0\ufe0f RPC names CALLED in code but NOT a live public function (PGRST202 risk = async-class) ===\"\ncomm -23 /tmp/rpc_called.txt /tmp/live_all_names.txt",
  "description": "RPC names called in code vs live functions (existence drift)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === distinct RPC names called in code ===
> add_user_score async_orchestrate_step award_mco_coins boost_aios_conversation calc_agent_cost_mcoin deduct_mco_coins delete_account disconnect_meta disconnect_social disconnect_wordpress has_role match_mcorch_nodes 
> 
> === ⚠️ RPC names CALLED in code but NOT a live public function (PGRST202 risk = async-class) ===
> ```

## 🤖 Claude *(22:56:21)*


## 🤖 Claude *(22:56:23)*

No existence drift — all 12 RPCs called in code exist live. Now the decisive async-class check: do the **arg keys** passed at each call site match the **live param names**? (The async bug was exactly this — `p_service_key` vs live `p_service_jwt_legacy`.) Extracting live signatures + call-site keys for all 12:

## 🤖 Claude *(22:56:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== LIVE signatures of the 12 called RPCs ===\"\njq -r '.[] | select([\"add_user_score\",\"async_orchestrate_step\",\"award_mco_coins\",\"boost_aios_conversation\",\"calc_agent_cost_mcoin\",\"deduct_mco_coins\",\"delete_account\",\"disconnect_meta\",\"disconnect_social\",\"disconnect_wordpress\",\"has_role\",\"match_mcorch_nodes\"]|index(.name)) | .name+\"(\"+.args+\")\"' /tmp/live_funcs.json\necho \"\"\necho \"=== CALL-SITE arg keys per RPC (object literal keys near each .rpc call) ===\"\nfor fn in add_user_score async_orchestrate_step award_mco_coins boost_aios_conversation calc_agent_cost_mcoin deduct_mco_coins delete_account disconnect_meta disconnect_social disconnect_wordpress has_role match_mcorch_nodes; do\n  hits=$(grep -rhA3 \"\\.rpc(['\\\"]$fn['\\\"]\" src supabase/functions packages 2>/dev/null \\\n    | grep -oE \"\\b(p_[a-z_]+|[a-z_]+_param|user_id_param|score_to_add|_[a-z_]+|role|query_embedding|match_threshold|match_count|filter_user_id)\\s*:\" \\\n    | sed -E 's/\\s*:$//' | sort -u | tr '\\n' ' ')\n  printf \"  %-26s args passed: %s\\n\" \"$fn\" \"${hits:-\uff08none/positional or variable\uff09}\"\ndone",
  "description": "Compare live signatures vs call-site arg keys for all 12 RPCs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === LIVE signatures of the 12 called RPCs ===
> jq: error (at /tmp/live_funcs.json:0): Cannot index array with string "name"
> 
> === CALL-SITE arg keys per RPC (object literal keys near each .rpc call) ===
>   add_user_score             args passed: score_to_add user_id_param 
>   async_orchestrate_step     args passed: p_run_id p_service_key p_supabase_url 
>   award_mco_coins            args passed: p_action p_amount p_user_id 
>   boost_aios_conversation    args passed: p_amount p_conv_id 
>   calc_agent_cost_mcoin      args passed: p_provider p_tokens_in p_tokens_out 
>   deduct_mco_coins           args passed: p_action p_amount p_user_id 
>   delete_account             args passed: p_user_id 
>   disconnect_meta            args passed: （none/positional or variable）
>   disconnect_social          args passed: p_account_id 
>   disconnect_wordpress       args passed: （none/positional or variable）
>   has_role                   args passed: _role 
>   match_mcorch_nodes         args passed: match_threshold query_embedding
> ```

## 🤖 Claude *(22:56:50)*


## 🤖 Claude *(22:56:52)*

jq precedence bug (the `|` rebound `.` inside `index()`), but the call-site extraction is clean and already shows the key result: **`async_orchestrate_step` call-site passes `p_run_id, p_service_key, p_supabase_url`** — matching the *fixed* live signature, confirming both my method works and the fix is materially live. Let me fetch live signatures correctly and do the automated subset check (call-keys ⊆ live-params) for all 12:

## 🤖 Claude *(22:57:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== LIVE signatures (corrected jq) ===\"\njq -r '.[] | . as $f | ([\"add_user_score\",\"async_orchestrate_step\",\"award_mco_coins\",\"boost_aios_conversation\",\"calc_agent_cost_mcoin\",\"deduct_mco_coins\",\"delete_account\",\"disconnect_meta\",\"disconnect_social\",\"disconnect_wordpress\",\"has_role\",\"match_mcorch_nodes\"]) as $w | select($w|index($f.name)) | $f.name+\"  ::  \"+$f.args' /tmp/live_funcs.json\necho \"\"\necho \"=== SUBSET CHECK: does each call-site key exist as a live param? ===\"\n# live param-name map (name -> space-separated param names)\njq -r '.[] | .name+\"|\"+([.args | scan(\"(^|, )(p_[a-z_]+|[a-z_]+_param|_[a-z_]+|[a-z_]+)\\\\s\")] | \"\")' /tmp/live_funcs.json >/dev/null 2>&1\ndeclare -A LIVE\nwhile IFS='|' read -r n a; do\n  pnames=$(echo \"$a\" | grep -oE '(^|, )[a-z_][a-z0-9_]*' | sed -E 's/^, //' | tr '\\n' ' ')\n  LIVE[\"$n\"]=\"$pnames\"\ndone < <(jq -r '.[] | .name+\"|\"+.args' /tmp/live_funcs.json)\n# call-site keys from previous step, hardcoded from material output:\ndeclare -A CALL=(\n [add_user_score]=\"score_to_add user_id_param\"\n [async_orchestrate_step]=\"p_run_id p_service_key p_supabase_url\"\n [award_mco_coins]=\"p_action p_amount p_user_id\"\n [boost_aios_conversation]=\"p_amount p_conv_id\"\n [calc_agent_cost_mcoin]=\"p_provider p_tokens_in p_tokens_out\"\n [deduct_mco_coins]=\"p_action p_amount p_user_id\"\n [delete_account]=\"p_user_id\"\n [disconnect_social]=\"p_account_id\"\n [has_role]=\"_role\"\n [match_mcorch_nodes]=\"match_threshold query_embedding\"\n)\nfor fn in \"${!CALL[@]}\"; do\n  live=\"${LIVE[$fn]}\"\n  bad=\"\"\n  for k in ${CALL[$fn]}; do\n    echo \" $live \" | grep -qw \"$k\" || bad=\"$bad $k\"\n  done\n  if [ -z \"$bad\" ]; then printf \"  \u2705 %-24s call-keys \u2286 live-params\\n\" \"$fn\"; else printf \"  \u274c %-24s MISMATCH \u2014 call passes [%s] not in live[%s]\\n\" \"$fn\" \"$bad\" \"$live\"; fi\ndone | sort",
  "description": "Automated subset check call-keys vs live params, all RPCs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === LIVE signatures (corrected jq) ===
> add_user_score  ::  user_id_param uuid, score_to_add integer
> async_orchestrate_step  ::  p_supabase_url text, p_service_key text, p_run_id uuid, p_step text
> award_mco_coins  ::  p_user_id uuid, p_amount integer, p_action text, p_context jsonb DEFAULT '{}'::jsonb
> boost_aios_conversation  ::  p_conv_id uuid, p_amount integer DEFAULT 1
> calc_agent_cost_mcoin  ::  p_tokens_in integer, p_tokens_out integer, p_provider text, p_model text, p_margin numeric DEFAULT 2.0
> deduct_mco_coins  ::  p_user_id uuid, p_amount numeric, p_action text DEFAULT 'spend'::text, p_context jsonb DEFAULT '{}'::jsonb
> delete_account  ::  p_user_id uuid
> disconnect_meta  ::  
> disconnect_social  ::  p_account_id uuid
> disconnect_wordpress  ::  
> has_role  ::  _role app_role
> match_mcorch_nodes  ::  query_embedding vector, match_threshold double precision DEFAULT 0.45, match_count integer DEFAULT 20, filter_project_id text DEFAULT NULL::text
> 
> === SUBSET CHECK: does each call-site key exist as a live param? ===
>   ✅ add_user_score           call-keys ⊆ live-params
>   ✅ async_orchestrate_step   call-keys ⊆ live-params
>   ✅ award_mco_coins          call-keys ⊆ live-params
>   ✅ boost_aios_conversation  call-keys ⊆ live-params
>   ✅ calc_agent_cost_mcoin    call-keys ⊆ live-params
>   ✅ deduct_mco_coins         call-keys ⊆ live-params
>   ✅ delete_account           call-keys ⊆ live-params
>   ✅ disconnect_social        call-keys ⊆ live-params
>   ✅ has_role                 call-keys ⊆ live-params
>   ✅ match_mcorch_nodes       call-keys ⊆ live-params
> ```

## 🤖 Claude *(22:57:34)*


## 🤖 Claude *(22:57:37)*

**RPC caller-contract layer is CLEAN** — all 12 pass; every call-site key exists as a live param. The `async_orchestrate_step` fix is materially confirmed live (`p_supabase_url, p_service_key, p_run_id, p_step`). No surviving signature-drift siblings.

But the flywheel incident had **three** root causes — and #1 was a *different* drift class: **edge-function `verify_jwt` config** (`orchestrate-step` was missing from `config.toml` → deployed with default `verify_jwt=true` → 401 on the opaque service key). I must audit that surface too: deployed function config vs `config.toml`, focusing on pg_net-invoked functions that *must* be `verify_jwt=false`.

## 🤖 Claude *(22:57:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\n# Deployed function configs (verify_jwt per function)\ncurl -s \"https://api.supabase.com/v1/projects/$REF/functions\" -H \"Authorization: Bearer $TOKEN\" > /tmp/deployed_fns.json\necho \"=== deployed functions (count) + verify_jwt distribution ===\"\njq 'length' /tmp/deployed_fns.json 2>/dev/null || { echo \"NON-JSON:\"; head -c 300 /tmp/deployed_fns.json; }\necho \"verify_jwt=false deployed:\"; jq -r '[.[]|select(.verify_jwt==false)]|length' /tmp/deployed_fns.json\necho \"\"\necho \"=== DEPLOYED functions with verify_jwt=false ===\"\njq -r '.[]|select(.verify_jwt==false)|\"  \"+.slug' /tmp/deployed_fns.json | sort\necho \"\"\necho \"=== config.toml declared verify_jwt entries ===\"\ngrep -A2 '^\\[functions\\.' supabase/config.toml | grep -E '\\[functions\\.|verify_jwt' | paste - - 2>/dev/null | sed -E 's/\\[functions\\.([a-z-]+)\\].*verify_jwt = (\\w+)/  \\1 = \\2/' || grep -B0 -A2 '^\\[functions' supabase/config.toml",
  "description": "Deployed edge function verify_jwt vs config.toml"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === deployed functions (count) + verify_jwt distribution ===
> 56
> verify_jwt=false deployed:
> 23
> 
> === DEPLOYED functions with verify_jwt=false ===
>   analyze-seo
>   check-video-status
>   embed-mcorch-node
>   generate-audio-script
>   generate-content
>   generate-image
>   generate-video
>   generate-video-script
>   handle-ml-postback
>   higgsfield-webhook
>   instagram-webhook
>   list-provider-models
>   orchestrate-content
>   orchestrate-step
>   process-affiliate-link
>   publish-social
>   publish-wordpress
>   refresh-social-token
>   self-heal
>   self-optimize
>   social-auth-callback
>   social-auth-init
>   stripe-webhook
> 
> === config.toml declared verify_jwt entries ===
>   publish-social = false
>   refresh-social-token = false
>   embed-mcorch-node = false
>   self-optimize = false
>   self-heal = false
>   orchestrate-content = false
>   orchestrate-step = false
>   generate-content = false
>   generate-audio-script = false
>   generate-video-script = false
>   list-provider-models = false
>   generate-video = false
>   check-video-status = false
>   generate-image = false
>   analyze-seo = false
>   publish-wordpress = false
>   sync-knowledge-mesh = true
>   higgsfield-webhook = false
>   handle-ml-postback = false
>   process-affiliate-link = false
>   instagram-webhook = false
>   stripe-webhook = false
>   social-auth-callback = false
>   social-auth-init = false
> ```

## 🤖 Claude *(22:58:07)*


## 🤖 Claude *(22:58:07)*

Let me make these comparisons precise (Law 1 — not eyeballed) and add repo↔deployed function existence:

## 🤖 Claude *(22:58:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\n# precise sets\njq -r '.[]|select(.verify_jwt==false)|.slug' /tmp/deployed_fns.json | sort -u > /tmp/dep_false.txt\ngrep -oE '\\[functions\\.[a-z-]+\\]' supabase/config.toml | sed -E 's/\\[functions\\.([a-z-]+)\\]/\\1/' > /tmp/cfg_all.txt\n# parse config.toml name=verify_jwt pairs\nawk '/^\\[functions\\./{name=$0; gsub(/\\[functions\\.|\\]/,\"\",name)} /verify_jwt/{print name\"=\"$3}' supabase/config.toml | grep '=false' | sed 's/=false//' | sort -u > /tmp/cfg_false.txt\necho \"=== verify_jwt=false: deployed vs config.toml ===\"\necho \"deployed-false NOT in config (drift: deployed open but undeclared):\"; comm -23 /tmp/dep_false.txt /tmp/cfg_false.txt | sed 's/^/  \u26a0\ufe0f /'\necho \"config-false NOT deployed-false (drift: declared but deployed verify_jwt=true):\"; comm -13 /tmp/dep_false.txt /tmp/cfg_false.txt | sed 's/^/  \u26a0\ufe0f /'\necho \"verdict:\"; diff -q /tmp/dep_false.txt /tmp/cfg_false.txt >/dev/null && echo \"  \u2705 EXACT MATCH (23=23)\" || echo \"  \u26a0\ufe0f drift above\"\necho \"\"\necho \"=== repo function dirs vs deployed slugs ===\"\nls supabase/functions/ | grep -v '^_' | sort -u > /tmp/repo_fns.txt\njq -r '.[].slug' /tmp/deployed_fns.json | sort -u > /tmp/dep_fns.txt\necho \"in repo but NOT deployed:\"; comm -23 /tmp/repo_fns.txt /tmp/dep_fns.txt | sed 's/^/  \u26a0\ufe0f /' || true\necho \"deployed but NOT in repo (orphan deploy):\"; comm -13 /tmp/repo_fns.txt /tmp/dep_fns.txt | sed 's/^/  \u26a0\ufe0f /' || true\necho \"verdict:\"; diff -q /tmp/repo_fns.txt /tmp/dep_fns.txt >/dev/null && echo \"  \u2705 repo == deployed\" || echo \"  \u26a0\ufe0f see above\"",
  "description": "Precise verify_jwt + repo/deployed function set diffs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === verify_jwt=false: deployed vs config.toml ===
> deployed-false NOT in config (drift: deployed open but undeclared):
> config-false NOT deployed-false (drift: declared but deployed verify_jwt=true):
> verdict:
>   ✅ EXACT MATCH (23=23)
> 
> === repo function dirs vs deployed slugs ===
> in repo but NOT deployed:
> deployed but NOT in repo (orphan deploy):
> verdict:
>   ✅ repo == deployed
> ```

## 🤖 Claude *(22:58:38)*


## 🤖 Claude *(22:58:40)*

Edge surface fully clean: **verify_jwt deployed == config.toml (23=23)** — the #1 root cause class is reconciled — and **repo functions == deployed slugs** (no orphan/missing). 

Two surfaces left: **triggers** (live vs migration-declared) and **RLS policies** (the highest-stakes — a policy altered out-of-band could open cross-tenant). Plus a sanity check on the *other* pg_net-dispatching functions (embed trigger, mesh sync) that could silently fail like async did:

## 🤖 Claude *(22:58:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== LIVE triggers (public, non-internal) ===\"\ncat <<'SQL' | /tmp/mq.sh > /tmp/live_trg.json\nSELECT t.tgname AS trigger, c.relname AS tbl, p.proname AS func,\n       CASE t.tgenabled WHEN 'O' THEN 'enabled' WHEN 'D' THEN 'DISABLED' WHEN 'R' THEN 'replica' WHEN 'A' THEN 'always' END AS state\nFROM pg_trigger t\nJOIN pg_class c ON c.oid=t.tgrelid\nJOIN pg_namespace n ON n.oid=c.relnamespace\nJOIN pg_proc p ON p.oid=t.tgfoid\nWHERE n.nspname='public' AND NOT t.tgisinternal\nORDER BY c.relname, t.tgname;\nSQL\njq -r '.[] | \"  \"+.tbl+\" \u2192 \"+.trigger+\" (\"+.func+\", \"+.state+\")\"' /tmp/live_trg.json\necho \"live trigger count:\"; jq 'length' /tmp/live_trg.json\necho \"\u26a0\ufe0f DISABLED triggers (drift signal):\"; jq -r '.[]|select(.state==\"DISABLED\")|\"  \"+.tbl+\".\"+.trigger' /tmp/live_trg.json\necho \"\"\necho \"=== migration-declared trigger names ===\"\ngrep -rhoiE 'CREATE (CONSTRAINT )?TRIGGER \"?[a-z_][a-z0-9_]*' supabase/migrations/ | sed -E 's/.*TRIGGER \"?//I' | tr 'A-Z' 'a-z' | sort -u > /tmp/decl_trg.txt\njq -r '.[].trigger' /tmp/live_trg.json | tr 'A-Z' 'a-z' | sort -u > /tmp/live_trg_names.txt\necho \"live triggers NOT declared in any migration (out-of-band):\"; comm -23 /tmp/live_trg_names.txt /tmp/decl_trg.txt | sed 's/^/  \u26a0\ufe0f /'",
  "description": "Live triggers vs migration-declared + disabled-trigger check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === LIVE triggers (public, non-internal) ===
>   affiliate_config → update_affiliate_config_updated_at (handle_updated_at, enabled)
>   affiliate_links → update_affiliate_links_updated_at (handle_updated_at, enabled)
>   aios_conversations → aios_conversations_updated_at (update_aios_conversations_updated_at, enabled)
>   campaigns → set_updated_at (handle_updated_at, enabled)
>   content_library → set_updated_at (handle_updated_at, enabled)
>   credits → update_credits_updated_at (handle_updated_at, enabled)
>   crew_agents → update_crew_agents_updated_at (handle_updated_at, enabled)
>   crew_edges → update_crew_edges_updated_at (handle_updated_at, enabled)
>   design_artifact_refs → set_design_artifact_refs_updated_at (handle_updated_at, enabled)
>   design_jobs → set_design_jobs_updated_at (handle_updated_at, enabled)
>   leads → tr_update_leads_updated_at (update_updated_at_column, enabled)
>   marketing_consents → tr_update_consents_updated_at (update_updated_at_column, enabled)
>   mcorch_nodes → trg_mcorch_embed_on_insert (mcorch_embed_on_insert, enabled)
>   meta_ads_metrics → tr_update_meta_ads_metrics_updated_at (update_updated_at_column, enabled)
>   meta_config → trg_instead_of_meta_config (trg_instead_of_meta_config, enabled)
>   meta_config_table → tr_encrypt_meta_config (trg_encrypt_meta_config, enabled)
>   meta_config_table → tr_update_meta_config_updated_at (update_updated_at_column, enabled)
>   profiles → set_updated_at (handle_updated_at, enabled)
>   scheduled_posts → set_updated_at (handle_updated_at, enabled)
>   sequence_enrollments → tr_update_enroll_updated_at (update_updated_at_column, enabled)
>   sequences → tr_update_sequences_updated_at (update_updated_at_column, enabled)
>   social_accounts → trg_instead_of_social_accounts (trg_instead_of_social_accounts, enabled)
>   social_accounts_table → set_updated_at (handle_updated_at, enabled)
>   social_accounts_table → tr_encrypt_social_accounts (trg_encrypt_social_accounts, enabled)
>   subscriptions → set_updated_at (handle_updated_at, enabled)
>   subscriptions → update_subscriptions_updated_at (handle_updated_at, enabled)
>   system_milestones → on_milestone_created (trigger_sync_knowledge_mesh, enabled)
>   user_api_keys → trg_instead_of_user_api_keys (trg_instead_of_user_api_keys, enabled)
>   user_api_keys_table → tr_encrypt_user_api_keys (trg_encrypt_user_api_keys, enabled)
>   vm_affiliate_links → vm_aff_links_updated_at (vm_update_updated_at, enabled)
>   vm_canvas_projects → vm_canvas_projects_updated_at (vm_update_updated_at, enabled)
>   vm_canvas_recipes → vm_canvas_recipes_updated_at (vm_update_updated_at, enabled)
>   vm_trends → vm_trends_updated_at (vm_update_updated_at, enabled)
>   whatsapp_leads → tr_update_whatsapp_leads_updated_at (update_updated_at_column, enabled)
> live trigger count:
> 34
> ⚠️ DISABLED triggers (drift signal):
> 
> === migration-declared trigger names ===
> live triggers NOT declared in any migration (out-of-band):
>   ⚠️ tr_encrypt_meta_config
>   ⚠️ tr_encrypt_social_accounts
>   ⚠️ tr_encrypt_user_api_keys
> ```

## 🤖 Claude *(22:59:13)*


## 🤖 Claude *(22:59:15)*

34 triggers, **none disabled** ✅. But three encryption triggers appear "live but not in migrations": `tr_encrypt_meta_config`, `tr_encrypt_social_accounts`, `tr_encrypt_user_api_keys`. Their *functions* (`trg_encrypt_*`) are migration-declared — so either the triggers are created via dynamic SQL my static grep can't see, or they're genuinely out-of-band. This is the exact ambiguity I must resolve materially (not assume):

## 🤖 Claude *(22:59:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== how are the encrypt triggers created in migrations? ===\"\ngrep -rniE \"tr_encrypt|CREATE TRIGGER.*encrypt|TRIGGER.*encrypt|EXECUTE.*TRIGGER\" supabase/migrations/ | grep -iE \"encrypt|trigger\" | head -30",
  "description": "Find how encrypt triggers are created (dynamic SQL vs out-of-band)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === how are the encrypt triggers created in migrations? ===
> supabase/migrations/20260423205725_knowledge_mesh_init.sql:61:FOR EACH ROW EXECUTE FUNCTION public.trigger_sync_knowledge_mesh();
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:137:-- (trigger tr_encrypt_user_api_keys already bound to the function — no re-create needed)
> supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql:6:--   trigger, which only does `DELETE FROM <base>_table WHERE id = OLD.id`. The encrypted token
> supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql:28:-- masked view — the encrypt trigger treats a UUID-shaped value as an already-encrypted ref and
> supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql:1:-- Migration: fix user_api_keys INSTEAD OF trigger — eliminate encrypt double-fire (23505)
> supabase/migrations/20260601000000_credential_encryption.sql:14:-- 2. TRIGGERS: Intercept writes on base tables and encrypt to vault.secrets
> supabase/migrations/20260601000000_credential_encryption.sql:50:CREATE OR REPLACE TRIGGER tr_encrypt_meta_config
> supabase/migrations/20260601000000_credential_encryption.sql:88:CREATE OR REPLACE TRIGGER tr_encrypt_social_accounts
> supabase/migrations/20260601000000_credential_encryption.sql:213:CREATE OR REPLACE TRIGGER tr_encrypt_user_api_keys
> ```

## 🤖 Claude *(22:59:45)*


## 🤖 Claude *(22:59:47)*

Resolved materially: those 3 are a **grep miss, not drift** — `credential_encryption.sql` lines 50/88/213 use `CREATE OR REPLACE TRIGGER` (PG14 syntax), which my regex (`CREATE [CONSTRAINT] TRIGGER`) didn't match. All 34 live triggers are migration-declared, none disabled. **Triggers clean.**

Final surfaces: **RLS policies** (highest security stakes) + the *other* pg_net-dispatching functions — because the 2026-06-01 key revocation that broke `async_orchestrate_step` could have stranded a sibling (e.g., the embed trigger) on a stale key:

## 🤖 Claude *(22:59:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== RLS: public tables WITHOUT row level security (security hole) ===\"\ncat <<'SQL' | /tmp/mq.sh | jq -r 'if length==0 then \"  \u2705 none \u2014 every public table has RLS enabled\" else (.[]|\"  \u26a0\ufe0f \"+.relname) end'\nSELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace\nWHERE n.nspname='public' AND c.relkind='r' AND c.relrowsecurity=false ORDER BY 1;\nSQL\necho \"\"\necho \"=== RLS: tables with RLS ENABLED but ZERO policies (locked/service-only) ===\"\ncat <<'SQL' | /tmp/mq.sh | jq -r 'if length==0 then \"  \u2705 none\" else (.[]|\"  \u2022 \"+.relname+\" (rls on, 0 policies)\") end'\nSELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace\nWHERE n.nspname='public' AND c.relkind='r' AND c.relrowsecurity=true\n  AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.schemaname='public' AND p.tablename=c.relname)\nORDER BY 1;\nSQL\necho \"\"\necho \"=== total live policies (public) ===\"\ncat <<'SQL' | /tmp/mq.sh | jq -r '.[0].n'\nSELECT count(*)::text AS n FROM pg_policies WHERE schemaname='public';\nSQL\necho \"\"\necho \"=== pg_net dispatch functions: target + key source (async-sibling check) ===\"\ncat <<'SQL' | /tmp/mq.sh | jq -r '.[] | \"\u2500\u2500\u2500\u2500 \"+.proname+\" \u2500\u2500\u2500\u2500\\n\"+.body'\nSELECT p.proname,\n       regexp_replace(p.prosrc, '\\s+', ' ', 'g') AS body\nFROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public' AND p.prosrc ILIKE '%net.http%'\nORDER BY p.proname;\nSQL",
  "description": "RLS coverage + pg_net dispatch functions key-source audit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === RLS: public tables WITHOUT row level security (security hole) ===
>   ✅ none — every public table has RLS enabled
> 
> === RLS: tables with RLS ENABLED but ZERO policies (locked/service-only) ===
>   • agent_executions_archive (rls on, 0 policies)
>   • async_orchestrate_step_debug (rls on, 0 policies)
> 
> === total live policies (public) ===
> 146
> 
> === pg_net dispatch functions: target + key source (async-sibling check) ===
> ──── async_orchestrate_step ────
>  BEGIN PERFORM net.http_post( url := p_supabase_url || '/functions/v1/orchestrate-step', headers := jsonb_build_object( 'Content-Type', 'application/json', 'Authorization', 'Bearer ' || p_service_key ), body := jsonb_build_object( 'run_id', p_run_id::text, 'step', p_step ) ); END; 
> ──── inspect_net_requests ────
>  DECLARE v_result jsonb; BEGIN SELECT jsonb_agg(t.* ORDER BY t.id DESC) INTO v_result FROM ( SELECT r.id, r.method, r.url, r.headers - 'Authorization' AS headers_safe, CASE WHEN r.headers ? 'Authorization' THEN jsonb_build_object( 'prefix', substring(r.headers->>'Authorization', 1, 20), 'suffix', substring(r.headers->>'Authorization' FROM length(r.headers->>'Authorization')-9), 'total_len', length(r.headers->>'Authorization') ) ELSE NULL END AS auth_preview, substring(r.body::text, 1, 200) AS body_preview FROM net.http_request_queue r ORDER BY r.id DESC LIMIT p_limit ) t; RETURN COALESCE(v_result, '[]'::jsonb); END; 
> ──── mcorch_embed_on_insert ────
>  DECLARE v_key text; BEGIN IF NEW.embedding IS NOT NULL THEN RETURN NEW; END IF; SELECT decrypted_secret INTO v_key FROM vault.decrypted_secrets WHERE name = 'sb_secret_key' LIMIT 1; -- No key configured yet → skip silently (never block the INSERT). Fire-and-forget. IF v_key IS NULL THEN RAISE WARNING '[mcorch] embed_on_insert: vault secret sb_secret_key missing — skipped for %', NEW.id; RETURN NEW; END IF; PERFORM net.http_post( url := 'https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/embed-mcorch-node', headers := jsonb_build_object( 'Content-Type', 'application/json', 'apikey', v_key, 'Authorization', 'Bearer ' || v_key ), body := jsonb_build_object('node_id', NEW.id::text) ); RETURN NEW; EXCEPTION WHEN OTHERS THEN RAISE WARNING '[mcorch] embed_on_insert skipped for %: %', NEW.id, SQLERRM; RETURN NEW; END; 
> ──── trigger_sync_knowledge_mesh ────
>  DECLARE request_id bigint; -- Default to local kong url for edge functions if not specified edge_url text := coalesce(current_setting('app.settings.sync_knowledge_mesh_url', true), 'http://kong:8000/functions/v1/sync-knowledge-mesh'); anon_key text := coalesce(current_setting('app.settings.anon_key', true), ''); BEGIN SELECT net.http_post( url:=edge_url, headers:=jsonb_build_object( 'Content-Type', 'application/json', 'Authorization', 'Bearer ' || anon_key ), body:=jsonb_build_object( 'type', TG_OP, 'table', TG_TABLE_NAME, 'schema', TG_TABLE_SCHEMA, 'record', row_to_json(NEW) ) ) INTO request_id; RETURN NEW; END;
> ```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-03 - Address alerts timezone issue and next steps]]
> * **Próxima Sessão**: [[2026-06-03 - Design agentic marketing framework for universal platforms]]
%% --- TIMELINE END --- %%

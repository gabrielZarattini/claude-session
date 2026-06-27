# Conectar redes sociais TikTok, YouTube e Pinterest
**Date:** 2026-06-27 | **Session ID:** `cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0`

---

## 👤 User *(03:39:21)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(03:39:21)*

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


## 🤖 Claude *(03:39:24)*


## 🤖 Claude *(03:39:24)*

I'll

## 👤 User *(03:39:24)*

[Request interrupted by user]

## 👤 User *(03:39:29)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(03:39:29)*

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


## 🤖 Claude *(03:39:35)*

I'll execute the ShakeHands /handson pickup ritual. Running all pre-flight commands in parallel.

## 🤖 Claude *(03:39:36)*


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
> 2d8e46d chore(sprint): v6.53.0 — Agentic Governance + Learning Loop + analytics honesto
> f486a8a docs(handoff): seal Agentic Governance + Learning Loop + analytics honesto + perfis da marca limpos
> 08e5ee3 docs(readme): v6.53.0 — Agentic Governance + Collective Efficiency Ledger + Learning Loop
> b6abff1 feat(analytics): painel por publicação + matar o fallback demo (números honestos)
> 47474ac feat(autopilot): loop que COMPÕE — reward multi-métrica brand-first + realocação ε-greedy
> 1371094 feat(autopilot): nervo sensorial — publication_metrics + coletor por publicação (FR-VA-027/028)
> 81210ab feat(ledger): Collective Efficiency Ledger — medir o coletivo, não no escuro (OTD-AG-001)
> ```

## 🤖 Claude *(03:39:37)*


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

## 🤖 Claude *(03:39:37)*


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

## 🤖 Claude *(03:39:37)*


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

## 🤖 Claude *(03:39:39)*


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
> mcorch_vision_mcp: Up 10 days (healthy)
> mcorch_claude_mem: Up 11 days (healthy)
> mcorch_chroma: Up 11 days (healthy)
> ---
> mega-brain-dashboard: Up 11 days
> mega-brain-webhook: Up 11 days (healthy)
> mega-brain-daemon: Up 11 days (healthy)
> ```

## 🤖 Claude *(03:39:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat; echo \" <- chroma\"",
  "description": "Chroma API v2 health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1782531580365631682} <- chroma
> ```

## 🤖 Claude *(03:39:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---scratch---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"; echo \"---wc---\"; wc -l HANDOFF.md",
  "description": "BoK suites, scratch, HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
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
> ---wc---
> 8463 HANDOFF.md
> ```

## 🤖 Claude *(03:39:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK completeness gate check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ agentic-governance — complete
> ✅ agentic-workspace — complete
> ✅ aios-sql-bridge — complete
> ✅ authenticated-browser-operator — complete
> ✅ canvas-design — complete
> ✅ constellation-v2 — complete
> ✅ conteudo-v2 — complete
> ✅ e2e-user-zero — complete
> ✅ gamificacao-nodes — complete
> ✅ identity-fabric — complete
> ✅ marketing-hub — complete
> ✅ mcorch-constellation — complete
> ✅ mcorch-qa-healing — complete
> ✅ mercado-livre-api — complete
> ✅ meta-api — complete
> ✅ openclaw — complete
> ✅ post-engine — complete
> ⚠️ security — missing: 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> ✅ video-studio — complete
> ✅ viral-autopilot — complete
> ✅ viral-daily-canvas — complete
> ✅ viralmind — complete
> ✅ vision-mcp — complete
> ```

## 🤖 Claude *(03:39:47)*


## 🤖 Claude *(03:39:48)*

Clean worktree, zero TS errors, all containers healthy. The `security` BoK "missing" is a false positive — it uses a different naming convention (blueprint/brd/srs/sdd/fmea per CLAUDE.md). Now reading HANDOFF + sprint context.

## 🤖 Claude *(03:39:49)*


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
> 14	## Session Seal — Doutrina Agêntica AGI→ASI + Learning & Adaptation: gate vinculante · Collective Efficiency Ledger · nervo sensorial + reward brand-first · analytics honesto (2026-06-27)
> 15	
> 16	Sessão-maratona multi-arco. **Arco 1** — Diretiva Sovereign: *"que todos os nossos próximos protocolos de desenvolvimento sigam essa visão clara de futuro para antecipar o mercado e a tecnologia"* — ancorada em `docs/Agentic-Design-Patterns.pdf` (Gulli, 21 padrões) + `docs/From AGI to ASI - 2606.12683.pdf` (DeepMind, 4 vias). **Arco 2** — atacar o único padrão FRACO (Learning & Adaptation). **Arco 3** — analytics honesto + perfis da marca limpos. 6 commits, tudo provado materialmente (Lei 1).
> 17	
> 18	**Achado material (3 deep-reads dos PDFs + verificação de schema):** o MCORCH JÁ encarna ~metade dos 21 padrões por doutrina (11 fortes · 9 moderados · 1 fraco=Learning&Adaptation). **Somos a Via 4 (coletivo de agentes) na camada de produto + a Via 3 (auto-aperfeiçoamento recursivo) no micro** (Obstáculo→Síntese). O gap estrutural é o que o paper aponta como ABERTO: respondíamos as perguntas de coletivo por doutrina mas **não medíamos nenhuma** — crescíamos no escuro.
> 19	
> 20	**Entregue (5 fases):**
> 21	- **Fase 1 (docs):** doutrina load-bearing `docs/architecture/agentic-vision.md` (Pattern Maturity Ledger dos 21 padrões + tese) · gate vinculante `CLAUDE.md §1 Step 3.5` (toda SDD declara conformidade) + §3/§4 · 2 docs stale (`system_architecture.md`/`agents.md`, descreviam plataforma AdSense pré-virada) DEPRECADOS+redirect.
> 22	- **Fase 2 (BoK):** suíte `docs/bok/agentic-governance/` 10/10 (autorada via workflow `wf_5fb96548`, espinha pinada; `09-pattern-conformance.md` = template mestre dos 21 padrões). Zero placeholders.
> 23	- **Fase 3 (SOP Lei 2):** `docs/processes/collective-efficiency-ledger.md` (8 gates; G6 `count cross-tenant=0` = gate-mãe).
> 24	- **Fase 4 (código):** migration `20260626120000_collective_efficiency_ledger.sql` — VIEW `collective_efficiency_ledger` (security_invoker per-tenant) + RPC `collective_efficiency_rollup` (SECURITY DEFINER service-role-only) DERIVAM a métrica da verdade financeira (`pipeline_runs`+`autopilot_cycles`), anti-Goodhart · 2 emits aditivos `collective_hop`/`collective_retry` em orchestrate-content/-step (deployadas). **/security-review SAFE.**
> 25	- **Fase 5 (seal):** nó `documentation_suite` `34748570-0cf2-470d-ba0e-f3ceab1cb550` (embedded 768d) + edge DERIVES_FROM `2f3b7a76` → mcorch-constellation.
> 26	
> 27	**Prova material (Lei 1, LIVE em prod):** migration aplicada (`Finished db push`) · VIEW 16 linhas reais · **G6 isolamento provado** (tenant throwaway vê **0**, service-role vê 16) · RPC negado a authenticated (**403 / 42501 permission denied**) · G7 métrica bate com a base exata (`93659c88`: mco 10·n_units 6·wall_clock 59985) · **rollup já dá insight: orchestrate-content avg 334.6s vs autopilot-cycle 2.4s** (o coletivo medido). `tsc` 0.
> 28	
> 29	**Honestidade (DD-AG-004):** **V4-2 (valor marginal por agente) DEFERIDO** a experimento A/B real — não fabricar proxy gameável (alerta do próprio paper). **Backlog de canonização OTD-AG-001..010** (001 Ledger=ENTREGUE; 002 fechar loop Learning&Adaptation reward multi-métrica = P0 próximo).
> 30	
> 31	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (aprovou o plano + escopo máximo via AskUserQuestion) · Owner=Sovereign (risco = instrumentação errada induzir decisão de escala errada).
> 32	
> 33	### Arco 2 — Learning & Adaptation: o loop que COMPÕE (OTD-AG-002 · emenda BoK viral-autopilot v0.3)
> 34	
> 35	**Diagnóstico material (`wob2d279d`):** o motor aprendia sobre um **placar em branco** — `creative_metrics` impressions/engagements sempre 0; reward = `totalClicks` mono-métrica (Goodhart, `autopilot-analyze:90`); a política só sussurrava um hint, não realocava esforço (`ab_variants` parada); 2 bugs latentes. **Causa raiz do "não avançamos apesar do dev incrível".**
> 36	
> 37	**Fatia A — nervo sensorial:** BoK viral-autopilot v0.3 (FR-VA-027..031 + `09-pattern-conformance` + SOP Lei 2 `publication-metrics-collection.md`) · migration `20260626130000_publication_metrics.sql` (time-series, RLS SELECT-own, **G6 provado** — throwaway vê 0; + `meta_posts.content_id` link fix) · edge `collect-publication-metrics` (insights IG/FB per-user, **fail-soft** por plataforma, nunca fabrica — provado: 2 posts LinkedIn → skip honesto) · painel **"Por Publicação"** (`usePublicationMetrics`+`PublicationMetricsPanel`) **verificado em browser real** (estado honesto, nunca demo).
> 38	
> 39	**Fatia B — o loop honesto:** `autopilot-analyze` reward multi-métrica brand-first `R=0.40·reach+0.30·eng+0.20·brand+0.10·rev` (z-score anti-Goodhart, degrada honesto — **prova policy `7d9856d0` reward 0.9 modo fallback**) · `autopilot-run` realocação ε-greedy budget-neutral (a política move o `tasks[]`, não só sussurra) · `orchestrate-step` read filtrado por scope=plan_id + `applied=true`. **Diferidos:** V4-2 (valor marginal/agente) · B4 EWMA · B5 pauta de receita.
> 40	
> 41	### Arco 3 — Analytics honesto + perfis da marca limpos
> 42	
> 43	**Demo-kill:** o fallback `DEMO_METRICS` (12.400 impressões falsas) da `AnalyticsPage` foi removido — vazio = **zero honesto + banner "sem dados reais ainda"** (browser-provado). **Zeramento dos perfis sociais antigos** (LinkedIn 6 posts + 5 métricas · Twitter 2+2, backup reversível) p/ as contas da marca começarem do zero: **Gabriel AI** (LinkedIn ativo · FB `gabrielorchai`) · **@gabrielOrchAI** (X/twitter). TikTok/YouTube/Pinterest já estavam 0 (não conectados). Resíduo inerte: 5 `creative_metrics` WordPress all-zero (limpeza ofertada, pendente da palavra do Sovereign).
> 44	
> 45	| Commit | Conteúdo |
> 46	|--------|----------|
> 47	| `a60e101` | feat(governance): doutrina Agêntica AGI→ASI + Pattern Conformance gate vinculante |
> 48	| `81210ab` | feat(ledger): Collective Efficiency Ledger + BoK agentic-governance 10/10 + seal `34748570` |
> 49	| `1371094` | feat(autopilot): nervo sensorial — publication_metrics + coletor (BoK v0.3) |
> 50	| `47474ac` | feat(autopilot): loop que COMPÕE — reward multi-métrica + realocação ε-greedy + bug fixes |
> 51	| `b6abff1` | feat(analytics): painel "Por Publicação" + matar o fallback demo |
> 52	| `08e5ee3` | docs(readme): v6.53.0 |
> 53	
> 54	**Mesh seal:** handoff node `326949f1-9430-4c49-8095-f86f269187a7` (embedded 768d). Mesh **8971 nós**.
> 55	
> 56	**Próximo (o unlock do payoff visível):** reconectar o **Instagram com escopo `instagram_business_manage_insights`** (hoje `magicorch` só tem publish) → o coletor grava reach/likes reais → o painel se enche → o reward flipa de `fallback` para `brand_first_multimetric` → o loop **compõe** (`R̄(N+1)>R̄(N)` via o Ledger).
> 57	
> 58	---
> 59	
> 60	## Session Seal — Gabriel AI mood board + Vision QA gate + 1º ciclo pago de vídeo 9:16 witnessed + billing/CTA fixes + virada brand-persona (2026-06-26)
> 61	
> 62	Sessão-maratona multi-arco (`/handson` → "faça tudo" → virada brand-persona → mood board animado), operando como **Usuário 00 sobre o Usuário 0** em produção real. **6 commits, tudo provado materialmente (Lei 1).**
> 63	
> 64	**Arco 1 — 1º ciclo pago de vídeo 9:16 autônomo, witnessed E2E + 2 bugs de receita (`df7505b`).** Recon material (workflow `wf_6475e2f8`) desmontou o HANDOFF stale: crons vivos, 2/3 produtos com shortlink assinado, CF público limpo — gargalo do 1º R$ = distribuição+conversão, não infra. Disparei o ciclo pago `2403bfcb` (plano `640b3b67`, flip `video_enabled`+`budget_cap 22→50`): **render 9:16 REAL `8b0787e0` 1080×1920 h264 5s 748KB** no bucket (ffprobe). O witness expôs 2 bugs: **(a) billing** — vídeo cobrado `succeeded×12` mas só o article-flow (wordpress) enfileira render → linkedin over-charged 12 sem refund (o refund de `orchestrate-step` só cobre enqueue-attempt-fail, não flow-sem-passo-de-vídeo); fix cobra por article-flow (`nVideoRuns`/`succeededVideo`, `dry_run` 46→34) + refund do tenant via `refund_autopilot_video_enqueue`. **(b) CTA-leak** — `rewriteHomepageCtas` só pegava href HTML; o LLM escreve `Garanta o seu aqui: https://mcorch.com` em texto puro → clique de maior intenção vazava pra homepage; guard estendido p/ bare-text nos 2 formatos + post `queued` corrigido antes do publish. **Cadência LinkedIn provada E2E:** auto-publish publicou a versão corrigida (post real `urn:li:share:7476089362896732160`).
> 65	
> 66	**Arco 2 — Virada brand-persona Gabriel AI / CCIO + blueprint YouTube/TikTok (`58e0389`).** Diretiva Sovereign: o conteúdo deixa de ser produto e vira evangelismo de marca via a persona **Gabriel AI (CCIO)** — rosto/voz única escalável. Plano de produto **pausado** (reversível). Workflow `wf_24e9eb67` (deepsearch fundamentado, Lei 1 c/ URLs oficiais) mapeou as integrações **YouTube + TikTok**: infra ~90% reusável (enum `social_platform` já tem yt/tiktok · `social_accounts` Vault · cadência · MESMO MP4 9:16 do Reel); net-new = 3 branches OAuth + gap `auto-publish` video_url. Gates de audit (YT `videos.insert` nasce private · TikTok SELF_ONLY) = ação Sovereign. Blueprint `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md` (seed p/ emenda BoK post-engine).
> 67	
> 68	**Arco 3 — Nó mood-board multi-foto + mood board Gabriel AI gerado E2E (`549e4dd`).** O nó `characterReference` virou **mood board** (até 6 fotos/nó via `imageUrls[]`; `pickNodeImages`/`findUpstreamImages` emitem todas → reference_image_urls, modelo usa até 4). Node grid 2×2 + badge 📸 + inspector upload múltiplo. **Demo + mood board provados E2E:** as 2 fotos do Sovereign → Nano Banana → **4 retratos face-consistentes** (Hero `c42d0336` + Estrategista/Palestrante/Visionário), cada um aprovado no **Vision QA** (cost 0 BYOK), + **2 animações DoP 9:16** disparadas (async) + grafo semeado no projeto `b57a59f7`. Verificado em browser real (nó + inspector). Fronteira: `sceneCompose` usa 2 handles (face-consistency = GenerateImage); Soul Character (`soulId`) = placeholder não-implementado.
> 69	
> 70	**Arco 4 — Vision QA como gate visual padrão + hardening do canvas (`a482132`).** Regra durável: todo print de inspeção + criativo passa por `scripts/qa/vision-qa.ts` (Vision MCP, BYOK grátis) antes de "pronto". E o **2º white-screen por nó malformado** (após o `coinCost`): clicar num `imageToVideo` sem `prompt` estourava `.length` e derrubava a página → guard `(node.data.prompt ?? "").length` nos 3 inspectors + os nós semeados corrigidos (prompts reais no sidebar).
> 71	
> ```

## 🤖 Claude *(03:39:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8063,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8063	ContentLibraryPage monetization flow:
> 8064	  Card (text, body contains mercadolivre.com.br)
> 8065	    └── DropdownMenu → "Monetizar Links ML"
> 8066	          → handleMonetizeLinks(item):
> 8067	               match(ML_URL_RE) → unique URLs
> 8068	               for url of unique:
> 8069	                 POST process-affiliate-link → affiliate_url
> 8070	                 body.split(url).join(affiliate_url)
> 8071	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8072	          → Badge 💰 ML (emerald) exibido após monetização
> 8073	```
> 8074	
> 8075	---
> 8076	
> 8077	## Pending Actions (Commercial Launch)
> 8078	
> 8079	### CRITICAL — Must complete before first client
> 8080	
> 8081	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8082	
> 8083	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8084	
> 8085	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8086	
> 8087	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8088	
> 8089	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8090	
> 8091	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8092	
> 8093	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8094	
> 8095	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8096	
> 8097	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8098	
> 8099	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8100	
> 8101	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8102	
> 8103	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8104	   ```bash
> 8105	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8106	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8107	   ```
> 8108	
> 8109	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8110	
> 8111	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8112	
> 8113	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8114	
> 8115	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8116	
> 8117	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8118	
> 8119	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8120	
> 8121	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8122	
> 8123	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8124	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8125	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8126	
> 8127	### SOCIAL — Next steps
> 8128	
> 8129	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8130	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8131	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8132	
> 8133	### NON-CRITICAL
> 8134	
> 8135	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8136	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8137	- `browserslist` — ✅ updated (2026-04-26)
> 8138	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8139	
> 8140	### GITNEXUS MCP — Next steps
> 8141	
> 8142	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8143	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8144	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8145	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8146	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8147	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8148	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8149	
> 8150	### PHASE EPSILON — Next iterations
> 8151	
> 8152	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8153	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8154	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8155	
> 8156	### CORE — Next iterations
> 8157	
> 8158	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8159	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8160	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8161	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8162	
> 8163	### PHASE DELTA — Next iterations
> 8164	
> 8165	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8166	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8167	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8168	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8169	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8170	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8171	
> 8172	### USUÁRIO ZERO — Checklist de validação
> 8173	
> 8174	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8175	- ✅ Stripe sandbox secrets no vault
> 8176	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8177	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8178	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8179	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8180	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8181	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8182	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8183	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8184	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8185	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8186	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8187	
> 8188	---
> 8189	
> 8190	## Infrastructure
> 8191	
> 8192	| Service | Container | Port | Status |
> 8193	|---------|-----------|------|--------|
> 8194	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8195	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8196	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8197	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8198	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8199	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8200	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8201	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8202	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8203	
> 8204	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8205	
> 8206	```bash
> 8207	docker compose up -d
> 8208	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8209	```
> 8210	
> 8211	---
> 8212	
> 8213	## Security Model (Post-Go-Live)
> 8214	
> 8215	| Table | Isolation |
> 8216	|-------|-----------|
> 8217	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8218	| `mcorch_edges` | Same pattern |
> 8219	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8220	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8221	
> 8222	---
> 8223	
> 8224	## Billing Architecture
> 8225	
> 8226	| Decision | Value |
> 8227	|----------|-------|
> 8228	| Canonical billing ledger | `profiles.mco_balance` |
> 8229	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8230	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8231	| Orchestration cost | 10 mcoCoins/run |
> 8232	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8233	| Stripe | Sandbox keys active — swap to live before first client |
> 8234	
> 8235	---
> 8236	
> 8237	## GraphRAG State
> 8238	
> 8239	- **8969 total nodes** (verificado live 2026-06-26 via REST count=exact, gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8240	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8241	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8242	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8243	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8244	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8245	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8246	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8247	- HNSW cosine index operational
> 8248	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8249	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8250	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8251	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8252	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8253	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8254	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8255	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8256	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8257	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8258	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8259	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8260	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8261	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8262	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8263	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8264	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8265	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8266	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8267	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8268	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8269	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8270	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8271	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8272	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8273	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8274	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8275	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8276	
> 8277	### Embedding Model
> 8278	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8279	Schema: `vector(768)` — HNSW cosine index.
> 8280	
> 8281	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8282	Três camadas eliminam intervenção manual:
> 8283	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8284	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8285	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8286	
> 8287	### Comandos de manutenção da Mesh
> 8288	```bash
> 8289	# Verificar nós sem embedding (deveria retornar array vazio):
> 8290	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8291	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8292	
> 8293	# Backfill manual (Bun-native — requer .env):
> 8294	bun run scripts/backfill-embeddings.ts
> 8295	
> 8296	# Backfill de código-fonte nos nós AST:
> 8297	bun run scripts/backfill-node-content.ts
> 8298	
> 8299	# Re-sync AST completo:
> 8300	cd packages/gitnexus-core && npm run sync-mesh
> 8301	
> 8302	# Acompanhar re-ingesta pós-commit:
> 8303	tail -f /tmp/mcorch-ingest.log
> 8304	```
> 8305	
> 8306	---
> 8307	
> 8308	## Video Rescue Protocol
> 8309	
> 8310	When a video generation operation (Google Veo) times out or client disconnects:
> 8311	```bash
> 8312	# Via edge function (production):
> 8313	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8314	  -H "Authorization: Bearer <user_jwt>" \
> 8315	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8316	
> 8317	# Via local script (admin/debug):
> 8318	source .env && bun run rescue.ts <operation_id> <content_id>
> 8319	```
> 8320	
> 8321	---
> 8322	
> 8323	## Architecture Pillars
> 8324	
> 8325	| Layer | Implementation |
> 8326	|-------|---------------|
> 8327	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8328	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8329	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8330	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8331	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8332	
> 8333	---
> 8334	
> 8335	## Phase Delta — Architecture
> 8336	
> 8337	```
> 8338	OrchestrationPage (full-canvas, p-0)
> 8339	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8340	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8341	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8342	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8343	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8344	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8345	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8346	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8347	
> 8348	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8349	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8350	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8351	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8352	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8353	```
> 8354	
> 8355	### Canvas State Architecture (Hybrid)
> 8356	
> 8357	```
> 8358	User interaction → ReactFlow internal state (positions, drag)
> 8359	                         ↓ (debounced 600ms)
> 8360	                   localStorage (positions persist across refresh)
> 8361	                         ↑
> 8362	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8363	     ↓ (status changes sync to ReactFlow via useEffect)
> 8364	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8365	```
> 8366	
> 8367	## Key Files
> 8368	
> 8369	| Purpose | Path |
> 8370	|---------|------|
> 8371	| Architecture rules | `CLAUDE.md` |
> 8372	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8373	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8374	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8375	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8376	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8377	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8378	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8379	| **Node types** | `src/components/orchestrator/nodes/` |
> 8380	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8381	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8382	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8383	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8384	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8385	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8386	| Billing utilities | `src/lib/billing.ts` |
> 8387	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8388	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8389	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8390	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8391	| Video rescue (local) | `rescue.ts` |
> 8392	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8393	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8394	| Deploy harness | `scripts/harness-deploy.sh` |
> 8395	
> 8396	---
> 8397	
> 8398	## First Client Onboarding Checklist
> 8399	
> 8400	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8401	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8402	3. ~~Activate watchdog cron~~ ✅ Done
> 8403	4. ~~Deploy rescue-video function~~ ✅ Done
> 8404	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8405	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8406	7. Monitor `infra_health_logs` for first 24h.
> 8407	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8408	
> 8409	---
> 8410	
> 8411	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8412	
> 8413	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8414	
> 8415	| Action | Result |
> 8416	|--------|--------|
> 8417	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8418	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8419	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8420	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8421	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8422	
> 8423	| Commit | Conteúdo |
> 8424	|--------|----------|
> 8425	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8426	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8427	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8428	
> 8429	### Arquitetura Matrix Intelligence
> 8430	
> 8431	```
> 8432	ConstellationMatrix (Stabilized Engine)
> 8433	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8434	  └── NodeDetailsPanel (Tabbed Navigation)
> 8435	        ├── Tab Meta: Neighbor exploration + Net Context
> 8436	        ├── Tab Code: Source code preview (Supabase sync)
> 8437	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8438	
> 8439	useNodeIntelligence Hook:
> 8440	  - contentQuery: fetch nodes.content column
> 8441	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8442	  - state: isAnalyzing, analysisResult, progress
> 8443	```
> 8444	
> 8445	---
> 8446	
> 8447	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8448	
> 8449	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8450	
> 8451	| Action | Result |
> 8452	|--------|--------|
> 8453	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8454	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8455	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8456	
> 8457	**Output da análise (estruturado em pt-BR):**
> 8458	- Visão Geral — papel do módulo no sistema
> 8459	- Padrões Detectados — design patterns, antipatterns
> 8460	- Acoplamento & Dependências — análise In/Out-Degree
> 8461	- Recomendações — 1-3 ações priorizadas
> 8462	
> ```

## 🤖 Claude *(03:39:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -80 || echo \"NO sprint-priorities.md\"; echo \"---scratch contents---\"; ls -la scratch/ 2>/dev/null",
  "description": "Sprint priorities + scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (70.2KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tool-results/bp05hpsuu.txt
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

## 🤖 Claude *(03:40:01)*


## 🤖 Claude *(03:40:02)*

All context gathered. Let me quickly check what's in `scratch/` to report it accurately.

## 🤖 Claude *(03:40:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null",
  "description": "Inspect scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 27 00:37 ..
> ```

## 🤖 Claude *(03:40:05)*


## 🤖 Claude *(03:40:32)*

`scratch/` is actually empty — the earlier "has files" was a false positive (the dir exists but contains nothing). Composing the brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Doutrina Agêntica AGI→ASI + Learning Loop + analytics honesto (2026-06-27)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
&nbsp;&nbsp;Fase selada: **v6.53.0** — Doutrina Agêntica (gate Pattern Conformance vinculante) · Collective Efficiency Ledger · nervo sensorial + reward brand-first · analytics honesto
&nbsp;&nbsp;Últimos commits:
- `2d8e46d` — chore(sprint): v6.53.0 — Agentic Governance + Learning Loop + analytics honesto
- `f486a8a` — docs(handoff): seal Agentic Governance + Learning Loop + analytics honesto
- `b6abff1` — feat(analytics): painel por publicação + matar o fallback demo (números honestos)
- `47474ac` — feat(autopilot): loop que COMPÕE — reward multi-métrica brand-first + ε-greedy

📂 **MUDANÇAS PENDENTES**
&nbsp;&nbsp;Worktree limpo ✅ — `git status` vazio, `git diff HEAD` vazio. Tudo selado em `main`.

🏗️ **INFRA**
&nbsp;&nbsp;mcorch_chroma: ✅ Up 11 days (healthy) — Chroma API v2: **OK** (`heartbeat` respondeu)
&nbsp;&nbsp;mcorch_claude_mem: ✅ Up 11 days (healthy)
&nbsp;&nbsp;mcorch_vision_mcp: ✅ Up 10 days (healthy)
&nbsp;&nbsp;mega-brain-{daemon,webhook,dashboard}: ✅ todos up/healthy

🧠 **KNOWLEDGE MESH**
&nbsp;&nbsp;**8971 nós** · ~9070 arestas (fonte: Task State header — seal node `326949f1`)
&nbsp;&nbsp;Top tipos: handoff · milestone · architecture · decision · observation · documentation_suite (BoK seals) · requirement + AST (file/function/interface)

🔧 **TYPESCRIPT**
&nbsp;&nbsp;Zero erros ✅ (`tsc --noEmit` limpo)

📚 **BoK SUITES**
&nbsp;&nbsp;Sealed: **22 suítes completas** (agentic-governance 10/10 · viral-autopilot · video-studio · vision-mcp · marketing-hub · post-engine · mcorch-constellation · meta-api · …)
&nbsp;&nbsp;Incomplete: **nenhuma** — o `security` aparece como "missing" mas é **falso positivo** (usa convenção própria: `00-blueprint/01-brd/02-srs/03-sdd/04-fmea`, não o template de 9 docs)
&nbsp;&nbsp;Mesh seal recente: agentic-governance → `34748570` (DERIVES_FROM `2f3b7a76` → mcorch-constellation)

📌 **SPRINT**
&nbsp;&nbsp;Goal: **Distribuição social autônoma operacional** — pipeline publica LinkedIn auto; Twitter desbloqueia ao subir tier; Instagram após App Review
&nbsp;&nbsp;Top gap (o "unlock do payoff visível"): **re-OAuth do Instagram com escopo `instagram_business_manage_insights`** — hoje `magicorch` só tem `publish`; sem insights o coletor não grava reach/likes reais e o reward fica preso em `fallback`

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **Reconectar Instagram com `instagram_business_manage_insights`** → o coletor `collect-publication-metrics` enche o painel "Por Publicação" → o reward flipa de `fallback` para `brand_first_multimetric` → o loop **compõe** (`R̄(N+1)>R̄(N)` via o Ledger). É o desbloqueio do payoff visível do Arco 2 desta seal. *(gate Sovereign: OAuth na conta da marca)*
2. **OTD-AG-002 / backlog de canonização** — B4 (EWMA no reward), B5 (pauta de receita), V4-2 (valor marginal por agente, diferido a experimento A/B real — não fabricar proxy gameável).
3. **Emenda BoK `post-engine`** (YouTube + TikTok) antes de codar as 3 branches OAuth — blueprint-semente pronto em `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md` (BoK Gate).

⚠️ **ALERTAS**
&nbsp;&nbsp;Nenhum alerta crítico ✅ — worktree limpo, tsc 0, containers healthy, scratch vazio.
&nbsp;&nbsp;Notas (não-bloqueantes): editor HyperFrames Studio (módulo-container) + postback ML real + publish vertical TikTok/IG/YT seguem como pendências do Viral Autopilot; resíduo inerte de 5 `creative_metrics` WordPress all-zero aguardando palavra do Sovereign para limpeza.

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

O estado está limpo e bem selado. O caminho de maior valor agora é destravar o **loop de aprendizado** — e o único bloqueio é a reconexão do Instagram com escopo de insights (ação sua, na conta da marca **Gabriel AI**). Quer que eu prepare o fluxo de re-OAuth, ataque um item do backlog OTD-AG-002 (B4/B5), ou puxe outra frente?

## 👤 User *(03:41:18)*

ótimo agora  vamos para conectar as redes
TikTok
YouTube
Pinterest

## 🤖 Claude *(03:42:19)*


## 🤖 Claude *(03:42:26)*

O Sovereign emitiu uma diretiva de **integração de 3 APIs externas novas** (TikTok, YouTube, Pinterest). Pelo MCORCH Master Execution Protocol (CLAUDE.md §1, regra inquebrável) isso **dispara o BoK Gate + o API Tenancy Model** — não posso sair codando OAuth direto. Mas isso não é um "não": é o trabalho certo na ordem certa. Vou conduzir a fase de pesquisa fundamentada + documentação eu mesmo (como o protocolo permite), e o memory já registra "amendar BoK post-engine antes de codar".

**ORO triplet desta task:**
- **Operator:** MCORCH Master Execution Agent
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign — risco = OAuth mal-feito vaza credencial cross-tenant / app rejeitado em audit / token-refresh quebrado mata a cadência da marca

Primeiro, um scout material inline para fundamentar o workflow (descobrir exatamente o que já existe vs. net-new). Depois disparo o workflow Ultracode de pesquisa+síntese.

## 🤖 Claude *(03:42:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# YouTube + TikTok — Blueprint de Preparação (virada brand-persona / Gabriel AI CCIO)
> 2	
> 3	> **Data:** 2026-06-26 · **Origem:** diretiva Sovereign (virada de product-first → brand-first; Gabriel AI = CCIO como rosto/voz unificada de todos os canais) + workflow de pesquisa fundamentada `wf_24e9eb67` (3 agentes, Lei 1 — cada claim com URL oficial).
> 4	> **Status:** PREPARAÇÃO. Nenhum código de publisher YT/TikTok escrito ainda. **Gate MCORCH Closed-Loop:** amendar o BoK `post-engine` (`/bok-scribe`) ANTES de codar.
> 5	
> 6	---
> 7	
> 8	## 0. Reframe estratégico (o "o quê")
> 9	
> 10	O conteúdo deixa de ser catálogo de produto e vira **evangelismo de marca com voz própria**. O **Gabriel AI / CCIO (Cofounder Chief Intelligence Office)** — primeira versão 100% digital do Sovereign — é o **rosto + a voz única**; a identidade visual do MCORCH é o corpo. A persona é o átomo de distribuição escalável: hoje 1 persona → N canais; amanhã N personas (cada "departamento" da Pantheon com seu avatar-porta-voz).
> 11	
> 12	**Implicação técnica decisiva:** os trilhos (gerar → render 9:16 → agendar → publicar → atribuir) **não mudam**. Muda (a) a *fonte do tema* (produto → pilar de marca/missão) e (b) o *número de bocas* (+ YouTube, + TikTok). Afiliado vira subproduto contextual de longo prazo, não o CTA principal.
> 13	
> 14	---
> 15	
> 16	## 1. Veredito de prontidão da infra (o achado central)
> 17	
> 18	**~90% já existe e é reusável as-is.** O `social_platform` enum **já contém `youtube` e `tiktok`** (migration `20260402014040:12`) — zero migration de enum. `social_accounts` (VIEW Vault mascarada) já cifra access/refresh token. `scheduled_posts` + `auto-publish` cron + motor `autopilot-run` já fazem a cadência. O OAuth connect é **genérico** (`social-auth-init` + `social-auth-callback`, state HMAC). O **MP4 9:16 que o IG Reel consome é o MESMO** que YT Shorts e TikTok consomem (motor HyperFrames `video-bridge.ts` → bucket `video-studio-assets`).
> 19	
> 20	**Net-new = só 3 pares de branches + 1 gap + 1 ajuste:**
> 21	
> 22	| Componente | Arquivo | O que adicionar |
> 23	|---|---|---|
> 24	| Publisher | `publish-social/index.ts:233` (antes do fallback) | `else if (platform==='youtube')` (videos.insert resumable) · `else if (platform==='tiktok')` (Content Posting API) — espelhar o padrão IG REELS criar→poll→publicar (`:141-196`) |
> 25	| OAuth init | `social-auth-init/index.ts:95` | branch Google (offline+consent) · branch TikTok |
> 26	| OAuth callback | `social-auth-callback/index.ts:171` | troca code→token + fetch perfil (channel id / open_id) · upsert já serve |
> 27	| Refresh | `refresh-social-token/index.ts:133` | branch Google · branch TikTok (refresh rotativo) |
> 28	| **Gap real** | `auto-publish/index.ts:54-83` | hoje só passa **texto**; p/ Shorts/TikTok agendados precisa resolver o MP4 9:16 (bucket privado → **URL pública/assinada**) e passar `content.video_url`. O Reel E2E foi invoke DIRETO; o caminho cron-de-vídeo ainda não está fechado. |
> 29	| Cadência+billing | `autopilot-run/index.ts:109` | adicionar `'youtube'`/`'tiktok'` ao `VIDEO_FLOW_PLATFORMS` → o ciclo enfileira render 9:16 e cobra vídeo p/ esses canais (FR-VA-022/024) |
> 30	| UI | `SocialAccountsPage.tsx` + `useSocialAccounts.ts:49` | `initiateOAuth(platform)` já é genérico — só faltam os cards YouTube/TikTok |
> 31	
> 32	**Schema:** NENHUMA tabela nova de token; NENHUMA migration de enum. (Único schema novo recomendado: `youtube_config`/`tiktok_config` per-user p/ app credentials, espelhando `meta_config`/`affiliate_config` — diferível p/ depois do Usuário Zero, env como override consciente com SLA.)
> 33	
> 34	---
> 35	
> 36	## 2. YouTube Shorts — fatos fundamentados (Lei 1)
> 37	
> 38	- **Mecanismo:** YouTube Data API v3 `videos.insert` **resumable** (2 fases: `POST /upload/youtube/v3/videos?uploadType=resumable&part=snippet,status` → `Location` session URI → `PUT` bytes → `201`). Não há "direct post" separado; **Short = formato** (vertical 9:16, ≤3min). Nosso MP4 1080×1920 casa nativo, sem reencode. [docs/youtube/v3/guides/using_resumable_upload_protocol · /docs/videos/insert · support.google.com/youtube/answer/10059070]
> 39	- **Scope:** `https://www.googleapis.com/auth/youtube.upload`. [identity/protocols/oauth2/.../sensitive-scope-verification]
> 40	- **🚧 2 portões (ambos bloqueiam PÚBLICO):**
> 41	  - **(A) Verificação do app OAuth** — `youtube.upload` é sensível → justificativa + **vídeo demo** + review Trust&Safety. Sem isso, app fica "Testing": **100 users + refresh token expira em 7 dias** (inviável p/ autopilot contínuo).
> 42	  - **(B) Audit do projeto de API (decisivo)** — citação oficial: *"All videos uploaded via the videos.insert endpoint from unverified API projects created after 28 July 2020 will be restricted to private viewing mode."* Ou seja, **mesmo mandando `public`, o YouTube sobrescreve p/ `private`** até passar o "Audit and Quota Extension Form". [docs/videos/insert · guides/quota_and_compliance_audits]
> 43	- **Quota:** bucket dedicado "Video Uploads" ~100 uploads/dia default (custo em units em transição 1600→reduzido em dez-2025 — ler a Quota Calculator na hora). [docs/youtube/v3/determine_quota_cost]
> 44	- **Per-user:** OAuth refresh token do canal (NÃO API key); `access_type=offline` + `prompt=consent` (refresh_token só vem na 1ª autorização). Em produção (verificado) não expira por tempo. → `social_accounts` platform='youtube'. [guides/auth/server-side-web-apps]
> 45	- **Gotchas:** vídeos nascem privados até o audit; canal precisa existir no upload; Brand Account exige permissão owner/manager; classificação sensitive-vs-restricted de `youtube.upload` confirmar no submit (se restricted → security assessment anual).
> 46	
> 47	## 3. TikTok — fatos fundamentados (Lei 1)
> 48	
> 49	- **Mecanismo:** Content Posting API sobre `open.tiktokapis.com`. **Direct Post** (server-side, autônomo): `creator_info/query` (obrigatório) → `/v2/post/publish/video/init/` → `PULL_FROM_URL` ou `FILE_UPLOAD` (chunked) → poll `status/fetch`. *Upload-to-inbox* (`/inbox/...`) exige o usuário finalizar no app → **não serve p/ autopilot**. [doc/content-posting-api-reference-direct-post · .../get-started]
> 50	- **Scopes:** `video.publish` (direct post), `video.upload` (draft).
> 51	- **🚧 Portão de audit (= IG App Review):** registrar app em developers.tiktok.com + audit do Content Posting API. **Sem audit:** todo post é **SELF_ONLY** (só o criador vê) + **conta precisa estar PRIVADA** no momento do post + ≤5 users/24h. Audit libera `PUBLIC_TO_EVERYONE`. *Ação Sovereign, ~2-4 semanas (terceiros).* [doc/content-sharing-guidelines]
> 52	- **Vídeo:** MP4 H.264 vertical OK (360–4096px, 23–60fps, ≤4GB). Nosso 1080×1920/30fps/<100MB cabe em 1 chunk ou PULL_FROM_URL. [doc/content-posting-api-media-transfer-guide]
> 53	- **Per-user:** OAuth access_token **24h** + refresh_token **365d** + `open_id` (guardar como `platform_user_id`). → `social_accounts` platform='tiktok'. [doc/oauth-user-access-token-management]
> 54	- **Gotchas:** `PULL_FROM_URL` exige **domínio verificado** (signed URL aleatória de bucket privado NÃO passa → usar FILE_UPLOAD ou servir de domínio próprio); `upload_url` expira em 1h; `access_token` expira em 24h (refresh automático obrigatório senão quebra no dia seguinte); rate 6 req/min por token; cap ~15 posts/dia/criador (não-oficial, validar).
> 55	
> 56	---
> 57	
> 58	## 4. Caminho recomendado (fatias finas, probe-first, single-tenant Usuário Zero)
> 59	
> 60	**PASSO 0 — Gate BoK (obrigatório antes de código).** `docs/bok/post-engine/` (5/5) já cita TikTok/Shorts/Reels, MAS (a) nomeia tabela errada `social_credentials` (a viva é `social_accounts`) e (b) não especifica scopes/audit/design dos branches. → **emenda via `/bok-scribe`** reconciliando o nome + cravando scopes, gates de audit e o design publish/oauth deste blueprint como Fonte da Verdade.
> 61	
> 62	**PASSO 1 — Fatia A · TikTok primeiro** (menor atrito p/ provar E2E em sandbox/self-post): branch OAuth + branch publish (Direct Post) consumindo o MP4 9:16 que o `video-bridge` JÁ gera. Provar 1 post real (SELF_ONLY até audit) com `video_url` público resolvido do bucket privado (como no Reel).
> 63	
> 64	**PASSO 2 — Fatia B · YouTube Shorts:** branch Google OAuth (offline+consent) + `videos.insert` resumable do mesmo MP4. Nasce `private` até o audit — válido p/ provar o transporte E2E.
> 65	
> 66	**PASSO 3 — Fatia C · Cadência:** `'youtube'`/`'tiktok'` no `VIDEO_FLOW_PLATFORMS` + **fechar o gap do `auto-publish`** (resolver/assinar o MP4 9:16 e passar `content.video_url`). Isso fecha o caminho cron-de-vídeo p/ TODOS os canais (incl. IG Reel agendado, hoje só provado por invoke direto).
> 67	
> 68	**PASSO 4 — Spine de persona (CCIO):** trocar a semente do prompt de `topic: produto` por um perfil de voz do CCIO (pilares fixos, ângulos variáveis) — onde "sempre falar da mesma coisa" vira engenharia. (Pode ser fatia própria ou parte da emenda BoK.)
> 69	
> 70	---
> 71	
> 72	## 5. Ações Sovereign (gated, fora do código — lead time de semanas)
> 73	
> 74	| Ação | Plataforma | Destrava |
> 75	|---|---|---|
> 76	| Criar canal YouTube MCORCH (converter o existente) | YouTube | pré-requisito do upload |
> 77	| OAuth app verification (Google Cloud) — consent screen + demo video | YouTube | tira a tela vermelha / Testing |
> 78	| **YouTube API Services Audit & Quota Extension Form** | YouTube | **vídeos públicos** (senão nascem privados) |
> 79	| Criar app em developers.tiktok.com + Content Posting API "Direct Post" | TikTok | conexão |
> 80	| **TikTok app audit** | TikTok | **posts públicos** (senão SELF_ONLY/privado) |
> 81	| (TikTok) verificar domínio p/ PULL_FROM_URL OU aceitar FILE_UPLOAD | TikTok | pull-from-url |
> 82	
> 83	**Estratégia realista:** construir os publishers + OAuth AGORA, validar E2E em **privado/sandbox** (TikTok SELF_ONLY, YT private), e o **público destrava com a aprovação** (igual ao caminho IG App Review). O código não bloqueia; o audit, sim.
> 84	
> 85	---
> 86	
> 87	## 6. Fontes (Lei 1) — ver `wf_24e9eb67` para a lista completa por claim
> 88	YouTube: developers.google.com/youtube/v3/{guides/using_resumable_upload_protocol, docs/videos/insert, determine_quota_cost, guides/quota_and_compliance_audits, guides/auth/server-side-web-apps} · identity/protocols/oauth2/production-readiness/{sensitive,restricted}-scope-verification · support.google.com/youtube/answer/10059070.
> 89	TikTok: developers.tiktok.com/doc/{content-posting-api-reference-direct-post, -upload-video, -get-started, -media-transfer-guide, content-sharing-guidelines, oauth-user-access-token-management}.
> 90	
> ```

## 🤖 Claude *(03:42:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== supabase functions (social-related) ===\"; ls supabase/functions/ | grep -iE 'social|publish|auth|meta|oauth|refresh' \necho \"\"; echo \"=== social_platform enum defs in migrations ===\"; grep -rEl \"social_platform\" supabase/migrations/ 2>/dev/null | head\necho \"\"; echo \"=== enum value lines ===\"; grep -rEn \"social_platform|ADD VALUE|CREATE TYPE.*social\" supabase/migrations/ 2>/dev/null | grep -iE \"tiktok|youtube|pinterest|linkedin|twitter|instagram|facebook|ADD VALUE|CREATE TYPE\" | head -40",
  "description": "Survey social functions and platform enum"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === supabase functions (social-related) ===
> auto-publish
> publish-meta
> publish-social
> publish-wordpress
> refresh-social-token
> social-auth-callback
> social-auth-init
> sync-meta-ads
> 
> === social_platform enum defs in migrations ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql
> 
> === enum value lines ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:12:CREATE TYPE public.social_platform AS ENUM ('linkedin', 'instagram', 'facebook', 'twitter', 'tiktok', 'youtube', 'pinterest', 'wordpress');
> ```

## 🤖 Claude *(03:43:52)*


## 🤖 Claude *(03:43:57)*

Material findings already reshape the plan:

1. **The enum is done** — `social_platform` already contains `'tiktok', 'youtube', 'pinterest'` (migration `20260402014040:12`). Zero enum migration for any of the three.
2. **Pinterest is the real research gap** — the existing blueprint covers YouTube + TikTok in grounded detail, but Pinterest was never researched.
3. **Generic seams already exist** — `publish-social`, `social-auth-init`, `social-auth-callback`, `refresh-social-token`, `auto-publish`.

Per the BoK Gate, the deliverable this turn is a **grounded, consolidated blueprint covering all 3 platforms + Pattern Conformance + per-integration SOPs** — the documentation that unblocks code. Under Ultracode I'll do this exhaustively: parallel material code-recon + grounded API research (Pinterest fresh; YT/TikTok verified & deepened) + adversarial verification (every claim carries an official URL — Lei 1) + synthesis.

Launching the workflow.

## 🤖 Claude *(03:45:26)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'social-connect-3platforms-blueprint',\n  description: 'Grounded blueprint to connect TikTok + YouTube + Pinterest publishers/OAuth to MCORCH (material code recon + API research + adversarial verify + synthesis)',\n  phases: [\n    { title: 'Recon & Research', detail: 'material code recon + grounded API research per platform (parallel)' },\n    { title: 'Verify', detail: 'adversarial source-check of each research front (every claim must carry an official URL)' },\n    { title: 'Synthesize', detail: 'consolidated readiness verdict + change-list + Pattern Conformance + per-integration SOPs + Sovereign-gated actions' },\n  ],\n}\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 Schemas \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nconst CODE_RECON_SCHEMA = {\n  type: 'object',\n  required: ['seams', 'igReelPattern', 'autoPublishGap', 'videoFlowPlatforms', 'socialAccounts', 'oauthGenericFlow', 'existingPlatformConfig', 'postEngineBokDrift'],\n  properties: {\n    seams: { type: 'array', items: { type: 'object', required: ['component','file','line','currentBehavior','changeNeeded'], properties: {\n      component: {type:'string'}, file: {type:'string'}, line: {type:'string'}, currentBehavior: {type:'string'}, changeNeeded: {type:'string'} } } },\n    igReelPattern: { type: 'string', description: 'The exact IG REELS create\u2192poll\u2192publish pattern to mirror, with file:line and the helper/shape names' },\n    autoPublishGap: { type: 'string', description: 'Exactly what auto-publish passes today and what is missing for scheduled video (video_url resolution from private bucket)' },\n    videoFlowPlatforms: { type: 'string', description: 'file:line of VIDEO_FLOW_PLATFORMS and current members' },\n    socialAccounts: { type: 'object', required: ['columns','rlsModel','vaultColumns','writePattern'], properties: {\n      columns: {type:'array', items:{type:'string'}}, rlsModel:{type:'string'}, vaultColumns:{type:'array', items:{type:'string'}}, writePattern:{type:'string', description:'insert vs upsert + INSTEAD OF trigger gotchas'} } },\n    oauthGenericFlow: { type: 'string', description: 'How social-auth-init builds the auth URL + state HMAC, what social-auth-callback does (code\u2192token\u2192profile\u2192upsert), what refresh-social-token branches on \u2014 with file:line' },\n    existingPlatformConfig: { type: 'array', items: {type:'string'}, description: 'Any per-user config tables/secrets for youtube/tiktok/pinterest app credentials (likely NONE) \u2014 name what exists for meta/affiliate as the mirror template' },\n    postEngineBokDrift: { type: 'array', items: {type:'string'}, description: 'Concrete discrepancies between docs/bok/post-engine/ and live code (e.g. wrong table name social_credentials vs social_accounts, missing scopes/audit/branch design)' },\n  },\n}\n\nconst RESEARCH_SCHEMA = {\n  type: 'object',\n  required: ['platform','oauth','publish','auditGates','tokenLifetimes','gotchas','claims'],\n  properties: {\n    platform: { type: 'string' },\n    oauth: { type: 'object', required: ['authUrl','tokenUrl','scopes','pkce','refreshModel'], properties: {\n      authUrl:{type:'string'}, tokenUrl:{type:'string'}, scopes:{type:'array',items:{type:'string'}}, pkce:{type:'string'}, refreshModel:{type:'string',description:'offline/consent, rotating refresh, access_type params, etc'}, extraParams:{type:'string'} } },\n    publish: { type: 'object', required: ['mechanism','steps','mediaTransfer','videoSpec'], properties: {\n      mechanism:{type:'string'}, endpoints:{type:'array',items:{type:'string'}}, steps:{type:'array',items:{type:'string'}}, mediaTransfer:{type:'string',description:'PULL_FROM_URL vs FILE_UPLOAD/resumable; domain-verification needs; signed-URL constraints'}, videoSpec:{type:'string'}, imageSupport:{type:'string',description:'for Pinterest: image pin vs video pin requirements'} } },\n    auditGates: { type: 'array', items: { type: 'object', required: ['gate','effectWithout','sovereignAction'], properties: {\n      gate:{type:'string'}, effectWithout:{type:'string'}, sovereignAction:{type:'string'} } } },\n    tokenLifetimes: { type: 'object', required: ['accessToken','refreshToken'], properties: { accessToken:{type:'string'}, refreshToken:{type:'string'}, notes:{type:'string'} } },\n    gotchas: { type: 'array', items: {type:'string'} },\n    claims: { type: 'array', items: { type: 'object', required: ['claim','sourceUrl'], properties: { claim:{type:'string'}, sourceUrl:{type:'string'} } }, description: 'EVERY material claim with the official doc URL consulted \u2014 Lei 1' },\n  },\n}\n\nconst VERIFY_SCHEMA = {\n  type: 'object',\n  required: ['platform','confidence','unverifiedClaims','corrections','missingTopics'],\n  properties: {\n    platform: { type: 'string' },\n    confidence: { type: 'string', enum: ['high','medium','low'] },\n    unverifiedClaims: { type: 'array', items: { type: 'object', properties: { claim:{type:'string'}, reason:{type:'string'} } }, description: 'claims whose sourceUrl does not actually support them or could not be confirmed' },\n    contradictions: { type: 'array', items: {type:'string'} },\n    corrections: { type: 'array', items: {type:'string'}, description: 'concrete corrections with the correct official URL' },\n    missingTopics: { type: 'array', items: {type:'string'}, description: 'topics the integration needs but research omitted (e.g. token refresh rotation, rate limits, app-review lead time)' },\n  },\n}\n\nconst SYNTHESIS_SCHEMA = {\n  type: 'object',\n  required: ['readinessVerdict','changeListByPlatform','patternConformance','sopSkeletons','sovereignGatedActions','openDecisions','recommendedSlicing'],\n  properties: {\n    readinessVerdict: { type: 'string', description: '2-4 sentences: what is reusable as-is across all 3 platforms vs net-new, grounded in the code recon' },\n    changeListByPlatform: { type: 'array', items: { type: 'object', required: ['platform','changes'], properties: {\n      platform: {type:'string'},\n      changes: { type: 'array', items: { type: 'object', required: ['file','seam','what'], properties: { file:{type:'string'}, seam:{type:'string'}, what:{type:'string'} } } },\n      newSchema: {type:'string', description:'any new per-user config table needed for app credentials, or NONE'} } } },\n    patternConformance: { type: 'array', items: { type: 'object', required: ['pattern','status','note'], properties: {\n      pattern: {type:'string'}, status: {type:'string', enum:['yes','deferred','n-a']}, note: {type:'string'} } }, description: 'Pattern Conformance Declaration rows for the social-publishing amendment \u2014 one per agentic pattern from docs/architecture/agentic-vision.md' },\n    sopSkeletons: { type: 'array', items: { type: 'object', required: ['platform','operator','sequence','verification','recovery','successSignal'], properties: {\n      platform:{type:'string'}, operator:{type:'string'}, sequence:{type:'array',items:{type:'string'}}, verification:{type:'array',items:{type:'string'}}, recovery:{type:'string'}, successSignal:{type:'string'} } }, description: 'Law 2 SOP skeleton per platform (Operator/Sequence/Verification gates/Recovery/Success signal)' },\n    sovereignGatedActions: { type: 'array', items: { type: 'object', required: ['action','platform','unblocks','leadTime'], properties: {\n      action:{type:'string'}, platform:{type:'string'}, unblocks:{type:'string'}, leadTime:{type:'string'} } }, description: 'Out-of-code actions ONLY the Sovereign can do: register developer apps (client_id/secret), submit audits, verify domains, create channels' },\n    openDecisions: { type: 'array', items: { type: 'object', required: ['decision','options','recommendation'], properties: {\n      decision:{type:'string'}, options:{type:'array',items:{type:'string'}}, recommendation:{type:'string'} } } },\n    recommendedSlicing: { type: 'array', items: {type:'string'}, description: 'thin probe-first slices, ordered' },\n  },\n}\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 Shared grounding \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nconst PRIOR_BLUEPRINT = `Prior grounded blueprint (.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md), key claims to VERIFY + DEEPEN (do not blindly trust \u2014 re-confirm against current 2026 official docs):\n- social_platform enum already contains youtube/tiktok/pinterest (confirmed in migration 20260402014040:12 \u2014 no enum migration needed).\n- YouTube: Data API v3 videos.insert resumable; scope youtube.upload (sensitive); 2 gates: OAuth app verification (else Testing: 100 users + refresh expires 7d) AND API project Audit (else uploads from unverified projects forced to private). Quota ~ bucket; cost in transition (1600 -> reduced Dec 2025). access_type=offline + prompt=consent for refresh_token.\n- TikTok: Content Posting API on open.tiktokapis.com; Direct Post = creator_info/query -> /v2/post/publish/video/init/ -> PULL_FROM_URL or FILE_UPLOAD chunked -> poll status/fetch. scopes video.publish/video.upload. Without audit: SELF_ONLY + account must be private + <=5 users/24h. access_token 24h, refresh 365d, open_id as platform_user_id. PULL_FROM_URL needs verified domain (random signed bucket URL fails -> FILE_UPLOAD).`\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 Phase 1: Recon & Research \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nphase('Recon & Research')\n\nconst CODE_RECON_PROMPT = `You are doing MATERIAL code recon of the MCORCH social-publishing subsystem to ground a multi-platform integration (TikTok + YouTube + Pinterest). Repo root: /home/gcrUX/htdocs/constellation-orchestra. Read these and report EXACT file:line seams (Lei 1 \u2014 no guessing):\n1. supabase/functions/publish-social/index.ts \u2014 find the Instagram REELS create->poll->publish branch (the exact pattern to mirror for new video publishers), the platform dispatch (if/else chain), and where the generic fallback is. Report the request/response shape and helper names.\n2. supabase/functions/social-auth-init/index.ts \u2014 how it builds the OAuth authorize URL per platform, the state HMAC signing, and the per-platform branch point.\n3. supabase/functions/social-auth-callback/index.ts \u2014 code->token exchange, profile fetch, and the upsert into social_accounts.\n4. supabase/functions/refresh-social-token/index.ts \u2014 per-platform refresh branches.\n5. supabase/functions/auto-publish/index.ts \u2014 what fields it passes to publish-social today (lines ~54-83); confirm the gap: does it resolve/sign a public video_url for scheduled video posts, or only pass text?\n6. supabase/functions/autopilot-run/index.ts \u2014 locate VIDEO_FLOW_PLATFORMS and its current members.\n7. src/hooks/useSocialAccounts.ts and the social accounts UI page (find it \u2014 likely src/pages/SocialAccountsPage.tsx) \u2014 how initiateOAuth(platform) is wired and where platform cards are defined.\n8. The social_accounts schema + RLS: grep migrations for 'social_accounts' (it is a Vault-masked VIEW). Report columns, the encrypted/vault columns (access_token/refresh_token), the RLS model, and the write pattern (insert vs upsert; INSTEAD OF trigger tenant-guard gotchas \u2014 see migrations around 20260602150000).\n9. Any existing per-user config table for youtube/tiktok/pinterest APP credentials (client_id/secret). Likely NONE \u2014 name the mirror templates that DO exist (meta_config, affiliate_config) and their shape/RLS.\n10. docs/bok/post-engine/ \u2014 read the suite; report concrete DRIFT vs the live code (e.g. wrong table name social_credentials vs the live social_accounts; missing scopes/audit/branch design for the 3 platforms).\nReturn the structured object. Use real line numbers from the files.`\n\nconst codeReconPromise = agent(CODE_RECON_PROMPT, { label: 'recon:code', phase: 'Recon & Research', schema: CODE_RECON_SCHEMA, agentType: 'Explore' })\n\nconst PLATFORMS = [\n  { key: 'tiktok', prompt: `${PRIOR_BLUEPRINT}\n\nRESEARCH TARGET: TikTok Content Posting API for AUTONOMOUS server-side video publishing (an autopilot bot, no human finalize-in-app step). Use WebSearch + WebFetch against the OFFICIAL developers.tiktok.com docs ONLY (2026 current). Produce grounded facts (every claim with its official URL \u2014 Lei 1):\n- OAuth: authorize URL, token URL, exact scopes for Direct Post vs draft, PKCE requirement, login-kit flow.\n- Token management: access_token lifetime, refresh_token lifetime, the EXACT refresh endpoint + whether refresh tokens ROTATE (must re-store the new refresh_token), and the consequence if not refreshed.\n- Direct Post flow: creator_info/query gate, /v2/post/publish/video/init/ payload, PULL_FROM_URL vs FILE_UPLOAD (chunked) \u2014 including the domain-verification requirement for PULL_FROM_URL and whether a Supabase-signed private-bucket URL qualifies; upload_url expiry; status/fetch polling.\n- Audit gates: unaudited app behaviour (SELF_ONLY, account-must-be-private, user cap), what the Content Posting API audit unlocks, and realistic lead time.\n- Video spec limits + rate limits + daily post caps.\n- Gotchas that break a daily autonomous cadence.\nBe exhaustive and current; correct any stale claim in the prior blueprint.` },\n  { key: 'youtube', prompt: `${PRIOR_BLUEPRINT}\n\nRESEARCH TARGET: YouTube Data API v3 video upload (Shorts = vertical formatting) for AUTONOMOUS server-side publishing. Use WebSearch + WebFetch against OFFICIAL developers.google.com/youtube + Google identity docs ONLY (2026 current). Produce grounded facts (every claim with its official URL \u2014 Lei 1):\n- OAuth: authorize + token endpoints, exact scope (youtube.upload \u2014 sensitive vs restricted classification), access_type=offline + prompt=consent semantics, when refresh_token is issued, whether it expires in production-verified vs Testing mode.\n- videos.insert RESUMABLE upload: the 2-phase protocol (initiate session -> Location URI -> PUT bytes -> 201), required parts (snippet,status), how to set privacyStatus and the Shorts vertical/duration requirement.\n- Audit gates: (A) OAuth consent-screen verification (Testing limits: 100 users, 7-day refresh expiry) and (B) the API project Audit & Quota Extension \u2014 the official statement that unverified projects' uploads are forced to private; what the audit unlocks; lead time.\n- Quota: current cost of videos.insert (note the Dec 2025 quota change \u2014 report the CURRENT number and link the quota calculator), default daily upload bucket.\n- Brand Account / channel prerequisites for upload.\n- Gotchas for a daily autonomous cadence.\nBe exhaustive and current; correct any stale claim in the prior blueprint.` },\n  { key: 'pinterest', prompt: `RESEARCH TARGET (NET-NEW \u2014 no prior blueprint exists): Pinterest API v5 for AUTONOMOUS server-side Pin creation (both image Pins and video Pins) for a brand persona. Use WebSearch + WebFetch against the OFFICIAL developers.pinterest.com docs ONLY (2026 current). Produce grounded facts (every claim with its official URL \u2014 Lei 1):\n- App access model: Trial access vs Standard access \u2014 what each allows, the rate/scope limits of Trial, and the app-review/verification process to reach Standard (this is the equivalent of TikTok/YouTube audit \u2014 describe it precisely + lead time).\n- OAuth v5: authorize URL, token URL, exact scopes needed to create pins and read boards (e.g. boards:read, boards:write, pins:read, pins:write \u2014 confirm exact names), PKCE/continuous-refresh, whether refresh tokens are issued and their lifetime, the refresh endpoint, and whether refresh tokens rotate. Note access_token + refresh_token lifetimes.\n- Create Pin: the POST /v5/pins endpoint, the required board_id (a board must exist \u2014 how to create/list boards via API), and the media model: IMAGE pins (image_url or base64) vs VIDEO pins (the media upload flow: register media -> upload to the returned URL -> poll media status -> reference media_id in the pin). Detail the video upload flow step-by-step and the supported video specs (does our 1080x1920 9:16 MP4 H.264 qualify? Pinterest historically prefers some formats \u2014 confirm).\n- Token lifetimes, rate limits, and daily creation caps.\n- Gotchas for a daily autonomous cadence (e.g. video processing async, board requirement, trial-access throttling, sandbox availability).\nBe exhaustive. This platform is the integration gap \u2014 depth matters most here.` },\n]\n\nconst researchVerifiedPromise = pipeline(\n  PLATFORMS,\n  (p) => agent(p.prompt, { label: `research:${p.key}`, phase: 'Recon & Research', schema: RESEARCH_SCHEMA, agentType: 'deepsearch-blueprint' }),\n  (research, p) => agent(\n    `Adversarially VERIFY this TikTok/YouTube/Pinterest research front for platform \"${p.key}\". Your job is to be the skeptic that protects Lei 1 (Materiality): for EACH claim, check the sourceUrl actually supports it; flag claims that look plausible but lack a real official-doc source; flag contradictions; and list integration-critical TOPICS the research MISSED (token-refresh rotation, rate limits, app-review/audit lead time, media transfer constraints, signed-URL/domain-verification issues). Use WebSearch/WebFetch against the OFFICIAL docs to confirm or refute. Default to flagging when uncertain. Research payload:\\n${JSON.stringify(research)}`,\n    { label: `verify:${p.key}`, phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'deepsearch-blueprint' }\n  ).then((v) => ({ platform: p.key, research, verify: v }))\n)\n\nconst [codeRecon, researchVerified] = [await codeReconPromise, await researchVerifiedPromise]\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 Phase 3: Synthesize \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nphase('Synthesize')\n\nconst SYNTHESIS_PROMPT = `You are the MCORCH synthesizer. Consolidate a material code recon + 3 grounded+verified API research fronts into a single integration blueprint for connecting TikTok + YouTube + Pinterest publishers/OAuth to the MCORCH social-publishing subsystem (brand persona \"Gabriel AI / CCIO\").\n\nFIRST read these repo files to ground the Pattern Conformance Declaration and the BoK amendment:\n- /home/gcrUX/htdocs/constellation-orchestra/docs/architecture/agentic-vision.md  (the 21 agentic patterns \u2014 your patternConformance array must have one row per pattern of this doctrine)\n- /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-governance/09-pattern-conformance.md  (the master template)\n- /home/gcrUX/htdocs/constellation-orchestra/.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md  (the prior blueprint you are EXTENDING to add Pinterest + Pattern Conformance + SOPs)\n\nThen produce the structured object:\n- readinessVerdict: grounded in codeRecon \u2014 what is reusable as-is (enum already has all 3; generic OAuth init/callback; social_accounts Vault; same 9:16 MP4) vs net-new.\n- changeListByPlatform: for EACH of tiktok/youtube/pinterest, the exact file:line seams (from codeRecon.seams) and what to add. Note any new per-user config table for app credentials (mirror meta_config) or NONE.\n- patternConformance: one row per pattern in agentic-vision.md (yes/deferred/n-a + honest note) for THIS social-publishing amendment.\n- sopSkeletons: Law 2 SOP skeleton per platform (Operator/Sequence with material success criteria per step/Verification gates/Recovery/Success signal).\n- sovereignGatedActions: the out-of-code blockers \u2014 register the 3 developer apps (client_id/secret), submit the 3 audits, verify domain (TikTok PULL_FROM_URL), create/convert the YouTube channel, Pinterest Trial->Standard. Each with what it unblocks + lead time. This is the CRITICAL PATH \u2014 without the developer apps there is NO client_id/secret so NO OAuth can even start.\n- openDecisions: genuine forks for the Sovereign (e.g. per-user config table now vs env-override-with-SLA for single-tenant User Zero; TikTok FILE_UPLOAD vs verify-domain-for-PULL_FROM_URL; which platform to build/prove E2E first).\n- recommendedSlicing: thin probe-first slices, ordered, single-tenant User Zero first.\n\nCODE RECON:\\n${JSON.stringify(codeRecon)}\\n\\nRESEARCH + VERIFY (3 platforms):\\n${JSON.stringify(researchVerified)}\\n\\nBe exhaustive, honest about deferrals, and keep every external claim anchored to the research sources.`\n\nconst synthesis = await agent(SYNTHESIS_PROMPT, { label: 'synthesize:blueprint', phase: 'Synthesize', schema: SYNTHESIS_SCHEMA, agentType: 'general-purpose' })\n\nreturn { codeRecon, researchVerified, synthesis }\n",
  "description": "Grounded 3-platform social connect blueprint"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wbrdr5f68
> Summary: Grounded blueprint to connect TikTok + YouTube + Pinterest publishers/OAuth to MCORCH (material code recon + API research + adversarial verify + synthesis)
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/subagents/workflows/wf_b5a35451-7dc
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-connect-3platforms-blueprint-wf_b5a35451-7dc.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-connect-3platforms-blueprint-wf_b5a35451-7dc.js"} to iterate without resending the script.)
> Run ID: wf_b5a35451-7dc
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-connect-3platforms-blueprint-wf_b5a35451-7dc.js", resumeFromRunId: "wf_b5a35451-7dc"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(03:45:32)*


## 🤖 Claude *(03:45:43)*

Workflow rodando em background (`wf_b5a35451-7dc`) — recon material + pesquisa fundamentada das 3 APIs + verificação adversarial + síntese. Você pode acompanhar ao vivo com `/workflows`. Serei reinvocado quando terminar.

Enquanto roda, o enquadramento honesto do que já sei materialmente:

**A boa notícia (infra ~90% pronta):** o enum `social_platform` **já tem `tiktok`, `youtube` E `pinterest`** — zero migration. Os trilhos genéricos (`social-auth-init`/`-callback`, `social_accounts` no Vault, cadência, o **mesmo MP4 9:16**) são reusáveis. O net-new é código de branches OAuth+publisher.

**O gate real do "conectar" (caminho crítico, ação sua):** OAuth não existe sem um **app de desenvolvedor registrado** em cada plataforma, que emite o `client_id`/`client_secret`. Hoje não temos esses 3 apps. Então a sequência inevitável é:

1. **Eu construo** os 3 pares de branches (OAuth + publisher) + fecho o gap do `auto-publish` para vídeo agendado — tudo provável E2E em **privado/sandbox**.
2. **Você registra** os 3 apps de dev (TikTok Developers, Google Cloud Console, Pinterest Developers) e me passa as credenciais → a conexão acende.
3. **Os audits** (TikTok Content Posting, YouTube API Audit, Pinterest Trial→Standard) destravam o **público** — lead time de semanas, igual ao IG App Review. O código não bloqueia; o audit, sim.

A síntese vai cravar exatamente isso por plataforma — incluindo o Pinterest, que é a peça nova que ninguém pesquisou ainda (modelo Trial/Standard, fluxo de video pin, board obrigatório). Volto com o blueprint consolidado + a Pattern Conformance + os SOPs assim que o workflow fechar.

## 👤 User *(03:59:15)*

<task-notification>
<task-id>wbrdr5f68</task-id>
<tool-use-id>toolu_016obiy6egsWyeMiuQxEVnrG</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wbrdr5f68.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Grounded blueprint to connect TikTok + YouTube + Pinterest publishers/OAuth to MCORCH (material code recon + API research + adversarial verify + synthesis)" completed</summary>
<result>{"codeRecon":{"seams":[{"component":"publish-social Instagram REELS dispatch","file":"/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts","line":"141-197","currentBehavior":"if platform==='instagram' creates media container with videoUrl?REELS:photo, polls status until FINISHED (max 30x, 3s interval), then publishes via media_publish endpoint. Returns result with id.","changeNeeded":"TikTok/YouTube/Pinterest need 3-step: (1) create container, (2) optional poll (sync vs async), (3) publish. Merge responses for platform_post_id extraction."},{"component":"publish-social platform dispatch chain","file":"/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts","line":"115-239","currentBehavior":"Platforms: linkedin (115-140), instagram (141-197), facebook (198-216), twitter (217-233), fallback (234-239).","changeNeeded":"Add tiktok/youtube/pinterest branches before fallback. Each handles token refresh pre-check (line 85), API endpoints, and result.id for platform_post_id."},{"component":"auto-publish content payload","file":"/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts","line":"77-83","currentBehavior":"Passes {platform, content:contentText, social_account_id, scheduled_post_id, user_id} to publish-social. No video_url field.","changeNeeded":"For video platforms: resolve/sign public video_url from content_library.media_url before passing. scheduled_posts schema lacks video_url column for transport."},{"component":"autopilot-run VIDEO_FLOW_PLATFORMS constant","file":"/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts","line":"109","currentBehavior":"VIDEO_FLOW_PLATFORMS = new Set(['wordpress']). Only wordpress sub-runs charge VIDEO_COST (line 111, 243).","changeNeeded":"Add 'youtube' to the Set when multi-platform video support lands. Updates billing reconciliation at lines 111, 243."}],"igReelPattern":"File: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts, Lines 141-197. Pattern: (1) create container via POST /{igAccountId}/media with media_type='REELS' + video_url + caption (152-163), (2) poll status via GET /{container.id}?fields=status_code up to 30x with 3s sleep until status_code='FINISHED' (172-178), (3) publish via POST /{igAccountId}/media_publish with creation_id (181-191). Helper: container.id = createRes.json().id extracted at line 164. Request body shapes: create = {media_type, video_url, caption, access_token}, status = {access_token}, publish = {creation_id, access_token}.","autoPublishGap":"auto-publish (lines 54-83) fetches scheduled_posts.content_id from content_library and extracts body/title as text. For scheduled video posts: (1) no video_url column on scheduled_posts to store resolved URL, (2) auto-publish does not resolve/sign storage_bucket URLs or pass media_url to publish-social, (3) publish-social expects content.video_url in request body (line 151) but auto-publish never provides it (line 79 always passes text-only content).","videoFlowPlatforms":"File: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts Line: 109. Current members: new Set(['wordpress']). Only wordpress product×platform pairs enqueue HyperFrames 9:16 renders and charge VIDEO_COST (12 MCO). Non-wordpress sub-runs (linkedin, twitter, etc.) never reach article_generation flow, so video_cost over-charge was fixed by scoping to VIDEO_FLOW_PLATFORMS (see lines 106-111, 243).","socialAccounts":{"columns":["id (uuid, PK)","user_id (uuid, FK auth.users)","platform (social_platform ENUM: linkedin|instagram|facebook|twitter|tiktok|youtube|pinterest|wordpress)","platform_user_id (text)","platform_username (text)","access_token (text, Vault-encrypted)","refresh_token (text, Vault-encrypted)","token_expires_at (timestamptz)","scopes (text[])","is_active (boolean)","metadata (jsonb)","created_at (timestamptz)","updated_at (timestamptz)"],"rlsModel":"Per-user isolation: authenticated users can SELECT/INSERT/UPDATE/DELETE only rows where user_id = auth.uid() (lines 275-278 of 20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql). Decrypted views (decrypted_social_accounts) restricted to service_role only (line 628-629 of 20260601000000_credential_encryption.sql).","vaultColumns":["access_token (stored as Vault secret UUID, decrypted via vault.decrypted_secrets join on UUID match, migration 20260601000000 lines 56-90 encryption trigger, 564-581 view join)","refresh_token (stored as Vault secret UUID, decrypted via vault.decrypted_secrets join on UUID match)"],"writePattern":"social_accounts is a Vault-masked VIEW (20260601000000 lines 369-384). INSERT/UPDATE/DELETE routed through INSTEAD OF trigger (trg_instead_of_social_accounts, 20260602150000 lines 102-151) to base table social_accounts_table. Tenant guard at line 117 (non-service_role can only write NEW.user_id = auth.uid()). Upsert pattern in social-auth-callback (line 180-195 of index.ts) via .upsert({...}, {onConflict: 'user_id,platform'}) on the masked view."},"oauthGenericFlow":"File: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts (OAuth authorize URL build + state HMAC) + social-auth-callback/index.ts (code-to-token + upsert). (1) social-auth-init: receives (platform, redirect_uri) from authenticated user, signs state via signState() with HMAC-SHA256 (line 56, imports ../_shared/oauth-state.ts), encodes authorize URL per platform (lines 60-100: linkedin/instagram/twitter branches). (2) social-auth-callback: verifies state signature via verifyState() (line 46-48, 10-min replay window via maxAgeMs), extracts userId from verified state, per-platform code-to-token exchange (lines 69-173: linkedin tokenRes, instagram short+long token exchange, twitter PKCE code_verifier), profile fetch (lines 92-169), upserts social_accounts at line 180-195 with {user_id, platform, access_token, refresh_token, token_expires_at, platform_user_id, platform_username, scopes, is_active}, fallback INSERT if upsert fails due to view trigger constraints (line 199-210).","existingPlatformConfig":["affiliate_config table (20260415201855_59f77a3a-3611-478f-9e5f-a6f85690f270.sql): per-user UNIQUE(user_id, platform) for mercadolivre affiliate tracking; columns: {id, user_id, platform (text), app_id, client_secret, redirect_uri, access_token, refresh_token, token_expires_at, is_active, metadata, created_at, updated_at}. RLS: auth.uid() = user_id.","meta_config table (20260530210000_meta_api_foundation.sql renamed to meta_config_table, masked as meta_config view): per-user Meta OAuth connection; columns: {id, user_id, facebook_user_id, long_lived_token (Vault), scopes, pages (Vault JSON), instagram_business_account_id, whatsapp_phone_number_id, whatsapp_waba_id, meta_ad_account_id, requires_reauth, token_expires_at, created_at, updated_at}. UNIQUE(user_id). Encrypted via 20260601000000 triggers, masked view + INSTEAD OF trigger for tenant guard.","No per-app youtube_config, tiktok_config, or pinterest_config tables exist. These platforms are enums in social_accounts only (line 12 of 20260402014040_b141fb0f)."],"postEngineBokDrift":["Drift 1: 06-data-model.md (line 18) references 'social_credentials' table; live code uses 'social_accounts' table (and social_accounts_table base). Docs are obsolete.","Drift 2: 06-data-model.md (line 21) lists platforms as 'tiktok|instagram|youtube|twitter' only; live social_platform ENUM (20260402014040 line 12) is 'linkedin|instagram|facebook|twitter|tiktok|youtube|pinterest|wordpress'.","Drift 3: 06-data-model.md (lines 23-24) references 'access_token (encrypted)' and 'refresh_token (encrypted)' but no mention of Vault or vault.decrypted_secrets. Migration 20260601000000 implemented Vault encryption after docs were written.","Drift 4: 07-process-flow.md PROC-PE-002 (line 26) mentions 'Descriptografa Token OAuth' but does not specify platform-specific branch logic (no link
... (truncated 125539 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wbrdr5f68.output)</result>
<usage><agent_count>8</agent_count><subagent_tokens>586860</subagent_tokens><tool_uses>130</tool_uses><duration_ms>828387</duration_ms></usage>
</task-notification>

## 🤖 Claude *(03:59:19)*


## 🤖 Claude *(03:59:20)*

Workflow completo (8 agentes, ~587K tokens, 14min). Lendo o resultado completo — foco na síntese, pesquisa Pinterest e verificações adversariais.

## 🤖 Claude *(03:59:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "f=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wbrdr5f68.output\"\necho \"=== FILE SIZE ===\"; wc -c \"$f\"\necho \"\"; echo \"=== keys present ===\"; python3 -c \"\nimport json\nd=json.load(open('$f'))\nprint(list(d.keys()))\nprint('synthesis keys:', list(d['synthesis'].keys()))\nprint('researchVerified platforms:', [r['platform'] for r in d['researchVerified']])\n\"",
  "description": "Inspect workflow result structure"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 1
> === FILE SIZE ===
> 157903 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wbrdr5f68.output
> 
> === keys present ===
> Traceback (most recent call last):
>   File "<string>", line 5, in <module>
> KeyError: 'synthesis'
> ['summary', 'agentCount', 'logs', 'result', 'workflowProgress', 'totalTokens', 'totalToolCalls']
> ```

## 🤖 Claude *(03:59:24)*


## 🤖 Claude *(03:59:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "f=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wbrdr5f68.output\"\npython3 -c \"\nimport json\nd=json.load(open('$f'))\nr=d['result']\nif isinstance(r,str): r=json.loads(r)\nprint('result keys:', list(r.keys()))\nprint('synthesis keys:', list(r['synthesis'].keys()))\nprint('platforms:', [x['platform'] for x in r['researchVerified']])\n# dump synthesis to a file\njson.dump(r['synthesis'], open('/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/synth.json','w'), indent=2, ensure_ascii=False)\njson.dump(r['researchVerified'], open('/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/research.json','w'), indent=2, ensure_ascii=False)\njson.dump(r['codeRecon'], open('/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/recon.json','w'), indent=2, ensure_ascii=False)\nprint('written')\n\"",
  "description": "Parse result and split into files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> result keys: ['codeRecon', 'researchVerified', 'synthesis']
> synthesis keys: ['readinessVerdict', 'changeListByPlatform', 'patternConformance', 'sopSkeletons', 'sovereignGatedActions', 'openDecisions', 'recommendedSlicing']
> platforms: ['tiktok', 'youtube', 'pinterest']
> written
> ```

## 🤖 Claude *(03:59:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/synth.json"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	{
> 2	  "readinessVerdict": "~90% reusable as-is, confirmed against live code. The social_platform ENUM already carries linkedin|instagram|facebook|twitter|tiktok|youtube|pinterest|wordpress (migration 20260402014040:12) — ZERO enum migration for any of the 3 platforms. social_accounts is a Vault-masked VIEW that already encrypts access_token/refresh_token + token_expires_at + scopes + metadata, written via the tenant-guarded INSTEAD OF trigger (auth.uid()=user_id) with the .upsert({onConflict:'user_id,platform'}) pattern — reusable verbatim. The OAuth scaffold is generic: social-auth-init signs HMAC-SHA256 state and social-auth-callback verifies it (10-min replay window) and upserts — only per-platform authorize-URL and code-to-token branches are net-new. publish-social already has a token-refresh pre-check (line 85) and the exact 3-step create→poll→publish pattern proven for IG REELS (lines 141-196) that TikTok and Pinterest-video mirror. The 9:16 1080x1920 H.264 HyperFrames MP4 (NFR-VS-016, bucket video-studio-assets) is in-spec for all three (TikTok 360-4096px/23-60fps; YouTube Shorts ≤3min vertical; Pinterest 9:16 recommended, ≥4s). Net-new = 3 publish branches + 3 oauth-init branches + 3 callback branches + 3 refresh branches (all rotating-token-aware), the auto-publish video_url transport gap (no video_url column on scheduled_posts; auto-publish never resolves/signs media_url), the VIDEO_FLOW_PLATFORMS Set, plus the platform-specific media-transfer divergence: YouTube is FILE_UPLOAD-only resumable PUT (no domain verification), TikTok needs FILE_UPLOAD (Supabase signed URLs fail PULL_FROM_URL domain ownership), Pinterest video is register→multipart-upload→poll→create with a mandatory PUBLIC cover_image_url. The hard blockers are entirely out-of-code (3 developer-app registrations + 3 audits) — without them there is no client_id/secret so no OAuth can even start, and every \"successful\" publish is invisible (TikTok SELF_ONLY, YouTube forced-private, Pinterest sandbox).",
> 3	  "changeListByPlatform": [
> 4	    {
> 5	      "platform": "tiktok",
> 6	      "newSchema": "RECOMMENDED tiktok_config per-user table mirroring meta_config (id, user_id UNIQUE, client_key, client_secret [Vault-encrypted, column-REVOKE], scopes text[], created_at, updated_at) — encrypted via the 20260601000000 trigger pattern + masked VIEW + INSTEAD OF tenant guard. DEFERRABLE for single-tenant User Zero: env TIKTOK_CLIENT_KEY/TIKTOK_CLIENT_SECRET as a conscious override-with-SLA (App Tenancy Model permits env fallback for Sovereign-only onboarding default). Token storage itself = NONE (reuses social_accounts platform='tiktok': access_token 24h, refresh_token 365d rotating, open_id as platform_user_id).",
> 7	      "changes": [
> 8	        {
> 9	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
> 10	          "seam": "line 95 (the `else` fallback after the twitter branch, before the 'not yet supported' 400)",
> 11	          "what": "Add `else if (platform==='tiktok')` building authorize URL https://www.tiktok.com/v2/auth/authorize/ with client_key, response_type=code, redirect_uri (pre-registered, https, static, no params/fragment, ≤512 chars), state (already signed at line 56), and scope=video.publish,user.info.basic — COMMA-separated, NOT space-separated (a space silently fails consent). video.publish (Direct Post) is the autonomy-critical scope; NEVER video.upload (draft-to-inbox needs a human to finish in-app). PKCE optional for server flow (client_secret held server-side) — add code_challenge S256 as defense-in-depth only."
> 12	        },
> 13	        {
> 14	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
> 15	          "seam": "line 171 (per-platform code-to-token block, after the twitter branch)",
> 16	          "what": "Add tiktok branch: POST https://open.tiktokapis.com/v2/oauth/token/ grant_type=authorization_code + client_key + client_secret + code + redirect_uri (+code_verifier if PKCE). Response gives access_token (expires_in 86400), refresh_token (refresh_expires_in 31536000), open_id, scope. Upsert into social_accounts: platform_user_id=open_id, token_expires_at=now+expires_in, scopes from response. Existing upsert at 180-195 serves."
> 17	        },
> 18	        {
> 19	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts",
> 20	          "seam": "line 233/234 (the `else` fallback after the twitter branch — add branch BEFORE it)",
> 21	          "what": "Add `else if (platform==='tiktok')` mirroring the IG REELS create→poll→publish shape (141-196) but as TikTok's 3-step: (1) MANDATORY pre-flight POST /v2/post/publish/creator_info/query/ (20/min) — read privacy_level_options and echo a value FROM that list (unaudited/private account: only FOLLOWER_OF_CREATOR/MUTUAL_FOLLOW_FRIENDS/SELF_ONLY, no PUBLIC_TO_EVERYONE); must NOT set disable_comment/duet/stitch=false when the corresponding *_disabled=true. (2) POST /v2/post/publish/video/init/ (6/min) with post_info{title ≤2200 UTF-16 runes, privacy_level, is_aigc:true [compliance MUST for an AI persona], brand_content_toggle ONLY if NOT SELF_ONLY} + source_info — use source=FILE_UPLOAD (video_size/chunk_size/total_chunk_count; chunks 5-64MB, final ≤128MB, <5MB single, 1-1000 chunks) because Supabase signed bucket URLs do NOT satisfy PULL_FROM_URL domain ownership. Returns publish_id. (3) PUT chunks to upload_url with Content-Range (re-init on 403 expired). (4) Poll POST /v2/post/publish/status/fetch/ (30/min) until PUBLISH_COMPLETE; handle full fail_reason set (video_pull_failed, file_format_check_failed, duration_check_failed, frame_rate_check_failed, picture_size_check_failed, publish_cancelled, auth_removed, spam_risk_too_many_posts/_user_banned_from_posting/_text/, internal). Extract result.id from publicaly_available_post_id (TikTok's literal misspelling; populated only when public+approved). Persist error envelope {code,message,log_id} per path. Add an idempotency guard keyed on content/run id BEFORE init — re-calling init mints a new publish_id and double-posts. Refresh-on-use with margin (<2h left) and ATOMICALLY re-store the rotated refresh_token (refresh response may return a NEW one)."
> 22	        },
> 23	        {
> 24	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts",
> 25	          "seam": "line 133 (per-platform refresh dispatch)",
> 26	          "what": "Add tiktok branch: POST https://open.tiktokapis.com/v2/oauth/token/ grant_type=refresh_token + client_key + client_secret + refresh_token. ROTATING: re-store the returned refresh_token whenever it differs (else slow-motion outage) + new access_token + token_expires_at=now+86400. No re-consent needed. Daily cron MUST refresh proactively before the 24h access_token expiry."
> 27	        }
> 28	      ]
> 29	    },
> 30	    {
> 31	      "platform": "youtube",
> 32	      "newSchema": "RECOMMENDED youtube_config per-user table mirroring meta_config (id, user_id UNIQUE, client_id, client_secret [Vault-encrypted, column-REVOKE], channel_id text, scopes text[], created_at, updated_at). DEFERRABLE for User Zero: env GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET as override-with-SLA. Token storage = NONE (social_accounts platform='youtube': access_token ~1h, refresh_token long-lived in production-verified mode, resolved channel_id stored as platform_user_id or in metadata). NOTE quota is per Cloud PROJECT not per channel — multi-tenant later needs per-project quota (FMEA item).",
> 33	      "changes": [
> 34	        {
> 35	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
> 36	          "seam": "line 95 (the `else` fallback)",
> 37	          "what": "Add `else if (platform==='youtube')` building https://accounts.google.com/o/oauth2/v2/auth with client_id, redirect_uri, response_type=code, scope=https://www.googleapis.com/auth/youtube.upload, state, AND access_type=offline + prompt=consent (refresh_token is returned ONLY on first authorization / forced re-consent — without prompt=consent a re-auth silently yields NO refresh_token). On the Google account-chooser the user MUST pick the correct Brand Account/channel (Gabriel AI / CCIO) — the upload targets whatever channel the token authorizes."
> 38	        },
> 39	        {
> 40	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
> 41	          "seam": "line 171 (per-platform code-to-token block)",
> 42	          "what": "Add youtube branch: POST https://oauth2.googleapis.com/token grant_type=authorization_code + code + redirect_uri + client_id + client_secret. Response gives access_token (~3600s), refresh_token (first-auth only), expires_in. Resolve channel id (GET youtube/v3/channels?mine=true with the access token) and store as platform_user_id/metadata.channel_id. Upsert with token_expires_at=now+3600. CRITICAL: never null-out a stored refresh_token on a response that lacks one."
> 43	        },
> 44	        {
> 45	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts",
> 46	          "seam": "line 233/234 (the `else` fallback — add branch BEFORE it)",
> 47	          "what": "Add `else if (platform==='youtube')` doing the resumable upload (NO PULL_FROM_URL — YouTube has no remote ingest, so FETCH the Supabase signed URL bytes then PUT them): (1) POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status with headers Authorization Bearer, Content-Type application/json, X-Upload-Content-Length=<bytes>, X-Upload-Content-Type=video/mp4; body {snippet:{title,description,tags,categoryId:'22'},status:{privacyStatus:'public',selfDeclaredMadeForKids:false,containsSyntheticMedia:true}}. (2) Capture the session URI from the Location header (HTTP 200). (3) PUT the MP4 bytes to that URI (256KB-multiple chunks + Content-Range for resilience; 308=Resume Incomplete → resume from the Range byte, but tolerate an ABSENT Range header = restart from 0, and a session-URI expiry ~1 week = re-initiate). (4) Success = HTTP 201 with the video resource id → persist as result.id. Shorts is IMPLICIT (1080x1920 + ≤3min auto-classifies; no Shorts flag, #Shorts optional). MATERIALITY (Lei 1): a 201 does NOT mean public — until the project Audit clears, an unverified API project FORCES every upload to private regardless of the requested privacyStatus; verify the resulting video's privacyStatus before claiming 'public'. Cap the daily counter to the videos.insert bucket (currently 100/day, 1 unit/call — READ the live Quota Calculator, the bucket model is recent/moving)."
> 48	        },
> 49	        {
> 50	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts",
> 51	          "seam": "line 133 (per-platform refresh dispatch)",
> 52	          "what": "Add youtube branch: POST https://oauth2.googleapis.com/token grant_type=refresh_token + client_id + client_secret + refresh_token → new access_token + expires_in; store token_expires_at=now+3600. Google generally does NOT rotate non-DPoP refresh tokens, but tolerate a new one arriving on forced re-consent and NEVER overwrite a good token with null. invalid_grant on day 8 = the app is still in Testing mode (sensitive scope → 7-day refresh expiry); the fix is gate A (In production), not a retry loop."
> 53	        },
> 54	        {
> 55	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
> 56	          "seam": "line 109 (VIDEO_FLOW_PLATFORMS = new Set(['wordpress']))",
> 57	          "what": "Add 'youtube' (and 'tiktok'/'pinterest' when their flows land) to the Set so those product×platform pairs enqueue the HyperFrames 9:16 render and charge VIDEO_COST. Update billing reconciliation at lines 111 and 243 accordingly (FR-VA-022/024)."
> 58	        }
> 59	      ]
> 60	    },
> 61	    {
> 62	      "platform": "pinterest",
> 63	      "newSchema": "RECOMMENDED pinterest_config per-user table mirroring meta_config (id, user_id UNIQUE, app_id/client_id, client_secret [Vault-encrypted, column-REVOKE], board_id text [cached destination board], scopes text[], created_at, updated_at). DEFERRABLE for User Zero: env PINTEREST_CLIENT_ID/PINTEREST_CLIENT_SECRET override-with-SLA. Token storage = NONE (social_accounts platform='pinterest': access_token 30d/2592000s, refresh_token 60d-from-last-use rotating + refresh_token_expires_at). Persist refresh_token_expires_at in metadata to schedule refresh inside the 60-day window.",
> 64	      "changes": [
> 65	        {
> 66	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
> 67	          "seam": "line 95 (the `else` fallback)",
> 68	          "what": "Add `else if (platform==='pinterest')` building https://www.pinterest.com/oauth/ with client_id, redirect_uri (EXACT match to a Configure>Redirect URIs entry — no wildcard), response_type=code, scope=boards:read,boards:write,pins:read,pins:write,user_accounts:read, state. Plan the FULL scope set up front — adding a scope later forces a full re-authorization (existing refresh token does not gain it). No PKCE (v5 is confidential-client Authorization-Code; client_secret stays server-side)."
> 69	        },
> 70	        {
> 71	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
> 72	          "seam": "line 171 (per-platform code-to-token block)",
> 73	          "what": "Add pinterest branch: POST https://api.pinterest.com/v5/oauth/token with grant_type=authorization_code + code + redirect_uri and header Authorization: Basic base64(client_id:client_secret). Response gives access_token (expires_in 2592000), refresh_token (continuous, rotating), refresh_token_expires_at. Resolve identity (GET /v5/user_account) for platform_username. Upsert with token_expires_at=now+2592000 and metadata.refresh_token_expires_at."
> 74	        },
> 75	        {
> 76	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts",
> 77	          "seam": "line 233/234 (the `else` fallback — add branch BEFORE it)",
> 78	          "what": "Add `else if (platform==='pinterest')` for a VIDEO pin (4-step async, mirroring IG's create→poll→publish): (0) ensure a destination board — GET https://api.pinterest.com/v5/boards to find board_id, else POST https://api.pinterest.com/v5/boards once; cache the board_id (do NOT create per run). (1) register: POST https://api.pinterest.com/v5/media {media_type:'video'} → media_id + upload_url + upload_parameters. (2) upload: POST the MP4 to upload_url as multipart/form-data with ALL upload_parameters sent VERBATIM and the file field LAST (S3 presigned-POST policy ordering; wrong order/mutated param → 403), NO Bearer auth, success=204. (3) poll: GET https://api.pinterest.com/v5/media/{media_id} with backoff until status='succeeded' (registered→processing→succeeded/failed). (4) create: POST https://api.pinterest.com/v5/pins {board_id, title ≤100, description ≤800, link, media_source:{source_type:'video_id', media_id, cover_image_url:'<PUBLIC https url>'}} → 201 with pin id = result.id. cover_image_url is MANDATORY and is PULLED by Pinterest → the cover still must sit on a PUBLIC (or long-TTL signed) URL — a too-short signed-URL TTL can expire before Pinterest's async fetch and silently fail the pin; the video binary itself is uploaded (not pulled). CORRECTED PATHS: REST routes are /v5/pins, /v5/boards, /v5/media (NOT /v5/pins/create etc. — those are doc-slugs and will 404). MATERIALITY (Lei 1): under Trial access the pin is sandbox/creator-only — no publicly-resolvable URL — do NOT claim 'published live' until Standard. Backoff on 429 against the org_write category limit (300/day Trial, 100/min Standard)."
> 79	        },
> 80	        {
> 81	          "file": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts",
> 82	          "seam": "line 133 (per-platform refresh dispatch)",
> 83	          "what": "Add pinterest branch: POST https://api.pinterest.com/v5/oauth/token grant_type=refresh_token + refresh_token, header Authorization: Basic base64(client_id:client_secret). ROTATING: each refresh returns a NEW access_token AND a NEW refresh_token — persist both ATOMICALLY (advisory-lock / SELECT-FOR-UPDATE around the refresh→persist txn, mirroring begin_autopilot_cycle) to avoid a lost-update race between cron and manual runs that breaks the chain and forces re-OAuth. Refresh inside the 60-day window keeps the chain alive indefinitely."
> 84	        }
> 85	      ]
> 86	    }
> 87	  ],
> 88	  "patternConformance": [
> 89	    {
> 90	      "pattern": "Prompt Chaining",
> 91	      "status": "yes",
> 92	      "note": "The publish branches extend the existing orchestrate-content/autopilot-run→auto-publish→publish-social chain; each platform publish is itself a multi-step chain (TikTok creator_info→init→upload→status; YouTube initiate→PUT→201; Pinterest register→upload→poll→create) mirroring the proven IG REELS create→poll→publish (publish-social:141-196)."
> 93	    },
> 94	    {
> 95	      "pattern": "Routing",
> 96	      "status": "yes",
> 97	      "note": "publish-social already routes by platform (the if/else-if dispatch ending at the fallback :234); this amendment adds 3 routing branches keyed on social_accounts.platform, plus per-platform media-transfer routing (TikTok FILE_UPLOAD vs YouTube resumable PUT vs Pinterest register-upload)."
> 98	    },
> 99	    {
> 100	      "pattern": "Parallelization",
> 101	      "status": "deferred",
> 102	      "note": "Multi-platform fan-out (publishing the same MP4 to IG+TikTok+YouTube+Pinterest concurrently) is the natural extension but is deferred to keep the probe-first slices serial and per-tenant-paced; tracked under the existing Parallelization gap (OTD doctrine #3, no timeout/circuit-break on stragglers). Initial cadence dispatches one platform per scheduled_post row sequentially."
> 103	    },
> 104	    {
> 105	      "pattern": "Reflection",
> 106	      "status": "deferred",
> 107	      "note": "Vision-QA over the generated 9:16 creative before publish is the relevant Generator-Critic loop, but it lives in the upstream creative layer (vision-qa.ts), not in the publisher branches. Closing it as a pre-publish gate per platform is deferred to OTD-AG-003 (generic Generator-Critic framework)."
> 108	    },
> 109	    {
> 110	      "pattern": "Tool Use",
> 111	      "status": "yes",
> 112	      "note": "Each branch is a typed external-API tool invocation (TikTok Content Posting API, YouTube Data API v3, Pinterest API v5) inside the JWT/service-role-guarded edge function — never exposing secrets to the client, per the Edge Functions mandate."
> 113	    },
> 114	    {
> 115	      "pattern": "Planning",
> 116	      "status": "n-a",
> 117	      "note": "The publishers execute a fixed, documented per-platform sequence; there is no agentic plan generation here. The cadence/scheduling plan is owned upstream by autopilot-run's optimization_policy, not by these transport branches."
> 118	    },
> 119	    {
> 120	      "pattern": "Multi-Agent",
> 121	      "status": "n-a",
> 122	      "note": "This is a transport/integration layer; it does not spawn or coordinate agents. The Pantheon collective that drives content upstream is unchanged by adding social mouths."
> 123	    },
> 124	    {
> 125	      "pattern": "Memory Management",
> 126	      "status": "yes",
> 127	      "note": "Per CLAUDE.md Mesh Connection Mandate, each first successful publish per new platform inserts a Knowledge Mesh observation node (mcorch_nodes, GraphRAG); platform_post_id (YouTube video id / TikTok publicaly_available_post_id / Pinterest pin id) + creative_metrics persist for attribution and recall."
> 128	    },
> 129	    {
> 130	      "pattern": "Learning & Adaptation",
> 131	      "status": "deferred",
> 132	      "note": "creative_metrics per platform feeds the autopilot reward loop, but the closed feedback loop (engagement→policy with multi-metric anti-Goodhart reward) is OTD-AG-002 (P0). Marking yes would fabricate the recursive link that is still manual."
> 133	    },
> 134	    {
> 135	      "pattern": "Model Context Protocol",
> 136	      "status": "n-a",
> 137	      "note": "No MCP surface is exposed or consumed by the social publishers; they are REST integrations behind edge functions."
> 138	    },
> 139	    {
> 140	      "pattern": "Goal Setting & Monitoring",
> 141	      "status": "yes",
> 142	      "note": "Every publish path (success/degraded/error) emits infra_health_logs telemetry with service='publish-<platform>' (CLAUDE.md telemetry reuse principle); the watchdog + Neural HUD monitor publish health. Materiality gates (verify YouTube privacyStatus='public'; TikTok PUBLISH_COMPLETE; Pinterest publicly-resolvable pin) are the monitored success signals."
> 143	    },
> 144	    {
> 145	      "pattern": "Exception Handling & Recovery",
> 146	      "status": "yes",
> 147	      "note": "Each branch maps the platform's full failure set to structured recovery: TikTok fail_reason switch + idempotency guard (init mints new publish_id → double-post) + upload_url 403 re-init; YouTube 308-resume + absent-Range restart + session-URI-expiry re-initiate; Pinterest async-poll-with-backoff + rotating-token atomic re-store. Mirrors rescue-video/refund-RPC recovery discipline."
> 148	    },
> 149	    {
> 150	      "pattern": "Human-in-the-Loop",
> 151	      "status": "yes",
> 152	      "note": "The hard gates are Sovereign-gated by design (sovereignGatedActions): developer-app registration, the 3 audits, domain verification, channel creation, Pinterest Trial→Standard. Until audits clear, publishes are private/SELF_ONLY/sandbox — the human must approve going public (ORO: Operator=MCORCH agent, Reviewer/Owner=Sovereign)."
> 153	    },
> 154	    {
> 155	      "pattern": "Knowledge Retrieval (RAG)",
> 156	      "status": "n-a",
> 157	      "note": "The publishers do not perform semantic retrieval at runtime; they write observation nodes (Memory #8) but do not query the mesh to publish."
> 158	    },
> 159	    {
> 160	      "pattern": "Inter-Agent Communication (A2A)",
> 161	      "status": "n-a",
> 162	      "note": "No agent-to-agent message exchange in the transport layer; the only cross-component call is the existing service-role edge-to-edge invoke (auto-publish→publish-social→refresh-social-token)."
> 163	    },
> 164	    {
> 165	      "pattern": "Resource-Aware Optimization",
> 166	      "status": "yes",
> 167	      "note": "VIDEO_COST charged atomically via the autopilot pre-debit when a platform joins VIDEO_FLOW_PLATFORMS (no client-side deduction); per-platform rate limits respected (TikTok init 6/min, YouTube videos.insert 100/day bucket, Pinterest org_write 100/min) and paced under the per-creator daily caps (TikTok ~15/day shared across clients). Refund/no-mint discipline reused for enqueue-fail."
> 168	    },
> 169	    {
> 170	      "pattern": "Reasoning Techniques",
> 171	      "status": "n-a",
> 172	      "note": "Deterministic API transport; no LLM reasoning in the publish branches."
> 173	    },
> 174	    {
> 175	      "pattern": "Guardrails / Safety",
> 176	      "status": "yes",
> 177	      "note": "Defense-in-depth: RLS default-deny on social_accounts (auth.uid()=user_id) + Vault-encrypted/column-REVOKE tokens + HMAC-signed OAuth state (cross-tenant account-link prevention) + per-user credential resolution fail-closed (App Tenancy Model) + is_aigc=true / containsSyntheticMedia=true compliant AI-persona disclosure + /security-review SAFE on any new migration (FMEA-011). New tiktok/youtube/pinterest_config tables follow the meta_config encrypted-VIEW + INSTEAD OF tenant-guard pattern."
> 178	    },
> 179	    {
> 180	      "pattern": "Evaluation & Monitoring",
> 181	      "status": "yes",
> 182	      "note": "Material-proof evaluation (Lei 1): success is NOT a 2xx — it is YouTube privacyStatus='public', TikTok status PUBLISH_COMPLETE + populated publicaly_available_post_id, Pinterest a publicly-resolvable pin URL (post-Standard). Vision-QA runs over the creative pre-publish (feedback_vision_qa_always). creative_metrics + infra_health_logs feed the Collective Efficiency Ledger."
> 183	    },
> 184	    {
> 185	      "pattern": "Prioritization",
> 186	      "status": "deferred",
> 187	      "note": "Slice ordering (single-tenant User Zero, TikTok-first by lowest E2E friction, then YouTube, then Pinterest) is human-curated, not a formal scheduler. Tracked under doctrine gap #20 / OTD-AG-020 (no anti-starvation priority algebra)."
> 188	    },
> 189	    {
> 190	      "pattern": "Exploration & Discovery",
> 191	      "status": "n-a",
> 192	      "note": "The publishers are confirmatory transport, not generative exploration. Trend-informed angle selection (fetch-trends/vm_trends, FR-VA-018) that picks WHAT to post lives upstream, not in these branches."
> 193	    }
> 194	  ],
> 195	  "sopSkeletons": [
> 196	    {
> 197	      "platform": "tiktok",
> 198	      "operator": "Sovereign (developer-app registration, audit submission, brand-account authorization via Login Kit) + MCORCH Master Execution Agent (publisher/OAuth code). Reviewer=Sovereign · Owner=Sovereign.",
> 199	      "sequence": [
> 200	        "1. Register app at developers.tiktok.com, add Content Posting API with Direct Post + scope video.publish; add the brand-persona TikTok account as a sandbox target user. Material success: client_key + client_secret visible in the portal; brand account listed as target user.",
> 201	        "2. Connect via OAuth: authorize URL (comma-separated scope video.publish,user.info.basic) → callback exchanges code at /v2/oauth/token/. Material success: a social_accounts row platform='tiktok' with non-null access_token + refresh_token + open_id (SELECT id returns a UUID).",
> 202	        "3. Pre-flight: POST /v2/post/publish/creator_info/query/. Material success: HTTP 200 with privacy_level_options array; echo a value FROM it (SELF_ONLY while unaudited).",
> 203	        "4. Init: POST /v2/post/publish/video/init/ with FILE_UPLOAD source + is_aigc=true. Material success: response carries a publish_id (string).",
> 204	        "5. Upload: PUT chunks to upload_url with Content-Range. Material success: each chunk returns 2xx; final chunk accepted.",
> 205	        "6. Poll: POST /v2/post/publish/status/fetch/ until PUBLISH_COMPLETE. Material success: status=PUBLISH_COMPLETE (unaudited: post exists SELF_ONLY); post-audit: publicaly_available_post_id populated + the tiktok.com URL resolves publicly."
> 206	      ],
> 207	      "verification": [
> 208	        "social_accounts row exists with a real open_id (Lei 1 UUID).",
> 209	        "creator_info/query returns 200 and the echoed privacy_level is in privacy_level_options.",
> 210	        "status/fetch returns PUBLISH_COMPLETE (not FAILED).",
> 211	        "infra_health_logs has service='publish-tiktok' rows for the run (success path).",
> 212	        "POST-AUDIT ONLY: the public tiktok.com URL from publicaly_available_post_id loads in a browser (the only proof of public reach)."
> 213	      ],
> 214	      "recovery": "On FAILED read fail_reason: video_pull_failed→switch to FILE_UPLOAD or verify domain; *_check_failed→fix MP4 encode; auth_removed→token dead, notify Sovereign to re-authorize via Login Kit (cannot be automated); spam_risk_*→back off and pace under ~15/day-per-creator. On upload_url 403 (expired)→re-init (new publish_id), guarded by the content/run idempotency key so a stalled worker does not double-post. On 429 (init 6/min)→exponential backoff capturing log_id. On rotated refresh_token→atomic re-store before next cycle.",
> 215	      "successSignal": "PRE-AUDIT: status PUBLISH_COMPLETE with a SELF_ONLY post visible to the creator (transport proven). POST-AUDIT: a publicly-resolvable tiktok.com URL (publicaly_available_post_id) — the only honest 'published live' claim."
> 216	    },
> 217	    {
> 218	      "platform": "youtube",
> 219	      "operator": "Sovereign (Brand Account/channel, Google Cloud OAuth consent-screen verification, Audit & Quota Extension form) + MCORCH Master Execution Agent (publisher/OAuth code). Reviewer=Sovereign · Owner=Sovereign.",
> 220	      "sequence": [
> 221	        "1. Ensure the Gabriel AI / CCIO Brand Account has a YouTube channel; create/convert if absent. Material success: channels?mine=true returns a channel id.",
> 222	        "2. In Google Cloud, configure OAuth consent (External), request youtube.upload (sensitive), add test users, then submit for verification + set publishing status to In production. Material success: consent screen verified (no unverified-app warning) so refresh tokens stop expiring in 7 days.",
> 223	        "3. Submit the YouTube API Services Audit & Quota Extension Form. Material success: email confirmation that the API project audit passed (lifts forced-private).",
> 224	        "4. Connect via OAuth with access_type=offline + prompt=consent, picking the Brand channel. Material success: social_accounts row platform='youtube' with a non-null refresh_token + stored channel_id.",
> 225	        "5. Resumable upload: POST initiate → capture Location session URI → PUT MP4 bytes (256KB-multiple chunks, 308-resume). Material success: HTTP 201 with a video resource id.",
> 226	        "6. Verify visibility: GET videos?id=<id>&part=status. Material success: status.privacyStatus='public' (NOT silently overridden to private)."
> 227	      ],
> 228	      "verification": [
> 229	        "channels?mine=true returns the intended Brand channel id (Lei 1).",
> 230	        "social_accounts row has a real refresh_token (and survives >7 days → proves In-production mode).",
> 231	        "Resumable upload returns HTTP 201 with a video id.",
> 232	        "videos.get status.privacyStatus === 'public' (the load-bearing gate — a 201 alone is NOT public proof).",
> 233	        "infra_health_logs service='publish-youtube' rows for the run.",
> 234	        "videos.insert daily count stays under the live Quota Calculator cap (~100/day)."
> 235	      ],
> 236	      "recovery": "308 Resume Incomplete→resume from the Range byte; ABSENT Range header→restart from byte 0; session-URI expired (~1 week)→re-initiate. invalid_grant on refresh→app is still in Testing (gate A not cleared): escalate to Sovereign, do NOT retry-loop. privacyStatus forced 'private' despite requesting public→project Audit (gate B) not cleared: halt 'public' claims until the audit email arrives. Never null-out a stored refresh_token on a refresh response lacking one.",
> 237	      "successSignal": "A YouTube video id whose videos.get returns privacyStatus='public' AND the youtube.com/shorts URL resolves publicly — both gate A (OAuth verified, refresh persists) and gate B (audit lifts forced-private) cleared."
> 238	    },
> 239	    {
> 240	      "platform": "pinterest",
> 241	      "operator": "Sovereign (Business account + Developer Terms + privacy-policy URL, Connect-app Trial request, Standard upgrade with OAuth+API demo video) + MCORCH Master Execution Agent (publisher/OAuth code). Reviewer=Sovereign · Owner=Sovereign.",
> 242	      "sequence": [
> 243	        "1. Create a Pinterest Business account, verify email, accept Developer Terms, register the app with a privacy-policy URL + complete description + EXACT redirect URI. Material success: app shows Trial access + client_id/secret in My apps.",
> 244	        "2. Submit the Standard-access upgrade with a video demo showing the OAuth flow AND a live v5 API action. Material success: email confirmation of Standard access (lifts sandbox-only visibility).",
> 245	        "3. Connect via OAuth: /oauth/ authorize → POST /v5/oauth/token (Basic auth) with the full scope set. Material success: social_accounts row platform='pinterest' with access_token (expires_in 2592000) + rotating refresh_token + stored refresh_token_expires_at.",
> 246	        "4. Ensure a brand board: GET /v5/boards (find) or POST /v5/boards (create once). Material success: a cached board_id.",
> 247	        "5. Video pin: POST /v5/media register → multipart upload (params verbatim, file LAST) → poll GET /v5/media/{id} until succeeded → POST /v5/pins with source_type='video_id' + PUBLIC cover_image_url. Material success: HTTP 201 with a pin id.",
> 248	        "6. Verify: under Standard, the pin's public URL resolves. Material success: pinterest.com/pin/<id> loads publicly (Trial cannot produce this)."
> 249	      ],
> 250	      "verification": [
> 251	        "social_accounts row has a real rotating refresh_token + refresh_token_expires_at (Lei 1).",
> 252	        "A cached board_id exists (not created per run).",
> 253	        "media status reaches 'succeeded' before pin create.",
> 254	        "POST /v5/pins returns HTTP 201 with a pin id.",
> 255	        "infra_health_logs service='publish-pinterest' rows for the run.",
> 256	        "STANDARD ONLY: pinterest.com/pin/<id> resolves publicly (Trial pins are sandbox/creator-only — no public proof)."
> 257	      ],
> 258	      "recovery": "media status='failed'→re-register + re-upload. Multipart 403 from S3→upload_parameters mutated or file not LAST: resend verbatim with file field last. Pin create fails because cover URL expired→use a long-TTL signed URL or public bucket for the cover (Pinterest fetches async, seconds-to-minutes later). 429→back off against org_write (300/day Trial, 100/min Standard). Rotated refresh_token lost (concurrency)→advisory-lock the refresh→persist txn; if chain broken, re-OAuth (Sovereign). Standard upgrade denied (missing OAuth demo)→re-record the demo video.",
> 259	      "successSignal": "PRE-STANDARD: HTTP 201 pin id under Trial (transport proven, sandbox-only). POST-STANDARD: a publicly-resolvable pinterest.com/pin/<id> URL — the only honest 'published live' claim."
> 260	    }
> 261	  ],
> 262	  "sovereignGatedActions": [
> 263	    {
> 264	      "action": "Register the TikTok developer app + add Content Posting API (Direct Post) + add the brand-persona TikTok account as a sandbox target user",
> 265	      "platform": "tiktok",
> 266	      "unblocks": "client_key/client_secret (WITHOUT these there is NO OAuth at all) + ability to test E2E pre-audit (only allowlisted target users can authorize in sandbox)",
> 267	      "leadTime": "Hours to 1-2 days (self-serve registration + ToS acceptance)"
> 268	    },
> 269	    {
> 270	      "action": "Submit the TikTok Content Posting API audit (usage-estimates form + a reviewable compliant-UX walkthrough/screencast) and obtain video.publish scope authorization",
> 271	      "platform": "tiktok",
> 272	      "unblocks": "PUBLIC posts (lifts SELF_ONLY + account-must-be-private + ≤5 users/24h) — until cleared every Direct Post is invisible to everyone but the creator",
> 273	      "leadTime": "~2-6 weeks (TikTok manual review, often multiple feedback rounds; no official SLA — budget weeks not days; estimate daily volume generously in the form so the 24h active-creator cap matches cadence)"
> 274	    },
> 275	    {
> 276	      "action": "(TikTok, only if PULL_FROM_URL is ever chosen over FILE_UPLOAD) Verify a MCORCH-owned domain or URL-prefix in the developer portal via DNS/prefix and serve the MP4 from it",
> 277	      "platform": "tiktok",
> 278	      "unblocks": "PULL_FROM_URL ingest — Supabase signed bucket URLs do NOT qualify; recommended to SKIP this by using FILE_UPLOAD instead",
> 279	      "leadTime": "Hours + DNS propagation (separate portal provisioning task); avoidable entirely with FILE_UPLOAD"
> 280	    },
> 281	    {
> 282	      "action": "Create/convert the Gabriel AI / CCIO YouTube channel on the correct Brand Account",
> 283	      "platform": "youtube",
> 284	      "unblocks": "Upload target — videos.insert posts to whatever channel the OAuth token authorizes; no channel = nowhere to upload",
> 285	      "leadTime": "Minutes (account-owner action)"
> 286	    },
> 287	    {
> 288	      "action": "Submit Google Cloud OAuth consent-screen verification for the sensitive youtube.upload scope (justification + demo video) and set publishing status to In production",
> 289	      "platform": "youtube",
> 290	      "unblocks": "Removes the unverified-app warning AND the 7-day refresh-token expiry (Testing mode kills a daily autopilot) — gate A",
> 291	      "leadTime": "Up to ~10 days (official sensitive-scope-verification SLA)"
> 292	    },
> 293	    {
> 294	      "action": "Submit the YouTube API Services Audit & Quota Extension Form",
> 295	      "platform": "youtube",
> 296	      "unblocks": "PUBLIC uploads — official: unverified API projects created after 28 Jul 2020 have every videos.insert upload FORCED to private until the audit passes (gate B, the load-bearing one) + quota beyond default",
> 297	      "leadTime": "Indeterminate, multi-week (no published SLA — 'contacted as soon as possible'). Gate A (~10d) and gate B (weeks) are SERIAL+independent → total readiness = the SUM, not the max"
> 298	    },
> 299	    {
> 300	      "action": "Create a Pinterest Business account + accept Developer Terms + provide a privacy-policy URL, then submit the Connect-app Trial request",
> 301	      "platform": "pinterest",
> 302	      "unblocks": "Any v5 API access at all (Trial) + client_id/secret — without it no OAuth and no API calls",
> 303	      "leadTime": "~1 business day (application requests reviewed each business day)"
> 304	    },
> 305	    {
> 306	      "action": "Submit the Pinterest Trial→Standard upgrade with a video demo of the OAuth flow AND a live API action",
> 307	      "platform": "pinterest",
> 308	      "unblocks": "PUBLIC pin visibility (Trial pins/boards are sandbox/creator-only) + raises rate limits from 1000/day/app to per-minute/user — until Standard, autonomous posts reach nobody",
> 309	      "leadTime": "No published SLA ('reviewed regularly', allow a few days); a denial (missing OAuth flow / non-OAuth auth / no live integration in the demo) adds a re-record round-trip"
> 310	    }
> 311	  ],
> 312	  "openDecisions": [
> 313	    {
> 314	      "decision": "Per-user app-credential config tables now vs env-override-with-SLA for single-tenant User Zero",
> 315	      "options": [
> 316	        "Build tiktok_config/youtube_config/pinterest_config now (mirror meta_config: encrypted VIEW + INSTEAD OF tenant guard + UI in Settings) — full API Tenancy Model compliance, multi-tenant-ready day 1, but adds 3 migrations + 3 UI cards + /security-review before any publish code",
> 317	        "Env override (TIKTOK_CLIENT_KEY/SECRET, GOOGLE_CLIENT_ID/SECRET, PINTEREST_CLIENT_ID/SECRET) as a conscious Sovereign-only onboarding default with a registered OTD + SLA — fastest path to prove E2E for User Zero; the App Tenancy Model explicitly permits env fallback for Sovereign-only/onboarding-default paths"
> 318	      ],
> 319	      "recommendation": "Env-override-with-SLA for the probe slices (User Zero is the only tenant; the 3 audits are the real critical path, not the config table), then promote to per-user config tables before any second tenant — register the deferral as an OTD with an explicit SLA so it does not become silent debt. Note: per-USER tokens still go to social_accounts (already per-user) regardless; only the APP credentials are env-deferred."
> 320	    },
> 321	    {
> 322	      "decision": "TikTok media transfer: FILE_UPLOAD vs verify-domain-for-PULL_FROM_URL",
> 323	      "options": [
> 324	        "FILE_UPLOAD (register init with chunk math, PUT chunks with Content-Range) — no domain-verification coupling, robust default, but strict chunk rules (5-64MB, final ≤128MB) and upload_url expiry handling",
> 325	        "PULL_FROM_URL — simpler request, but requires verifying a MCORCH-owned domain/URL-prefix in the portal AND serving the MP4 from it (Supabase signed bucket URLs are disqualified); secondary query-param/redirect concerns are inference, not doc-stated"
> 326	      ],
> 327	      "recommendation": "FILE_UPLOAD for the autopilot — it decouples publish from a Sovereign-gated domain-verification provisioning step and works directly off the existing private bucket. Revisit PULL_FROM_URL only if/when a verified video.mcorch.com static host already exists for other reasons."
> 328	    },
> 329	    {
> 330	      "decision": "Which platform to build + prove E2E first",
> 331	      "options": [
> 332	        "TikTok first — lowest friction to a real self-post (sandbox SELF_ONLY proves transport immediately), native 9:16, but rotating refresh + mandatory creator_info pre-flight + audit for public reach",
> 333	        "YouTube first — resumable upload is the simplest happy-path (fetch bytes, PUT, 201), no domain verification, but the DOUBLE gate (OAuth verification ~10d + Audit weeks, serial) is the longest critical path and uploads are forced-private until both clear",
> 334	        "Pinterest first — 4-step async + mandatory public cover URL + Trial-sandbox invisibility, most plumbing"
> 335	      ],
> 336	      "recommendation": "TikTok first to prove the FILE_UPLOAD + create→poll→publish transport E2E in sandbox fastest, in PARALLEL start the YouTube gate-A (OAuth verification) + gate-B (audit) submissions immediately since they are the longest lead time and serial — start the clock on the slowest dependency on day one even while coding TikTok."
> 337	    },
> 338	    {
> 339	      "decision": "auto-publish video_url transport: add a video_url column to scheduled_posts vs resolve-at-dispatch from content_library.media_url",
> 340	      "options": [
> 341	        "Add scheduled_posts.video_url column (migration) — explicit, the resolved/signed URL is persisted at schedule time",
> 342	        "Resolve+sign at dispatch in auto-publish (fetch content_library.media_url → sign → pass content.video_url) — no schema change, but signed-URL TTL must outlive the platform's async fetch (esp. Pinterest cover, minutes later)"
> 343	      ],
> 344	      "recommendation": "Resolve+sign at dispatch (no migration), generating a long-TTL signed URL (hours) at publish time so it survives Pinterest/IG async fetch; only add a column if a durable record of the exact transported URL becomes an audit/attribution requirement. This closes the documented auto-publish gap (it currently passes text-only content, never media_url) for IG Reels too (today only proven via direct invoke)."
> 345	    },
> 346	    {
> 347	      "decision": "is_aigc / containsSyntheticMedia / synthetic-media labeling for the AI persona",
> 348	      "options": [
> 349	        "Set is_aigc=true (TikTok) + containsSyntheticMedia=true (YouTube) unconditionally — honest AIGC disclosure, compliance MUST for an AI brand persona, but TikTok forbids brand_content_toggle=true together with SELF_ONLY (the unaudited forced state)",
> 350	        "Omit/soften labeling to avoid the platform AIGC tag"
> 351	      ],
> 352	      "recommendation": "Always label AI-generated (is_aigc=true / containsSyntheticMedia=true) — it is a compliance requirement, not optional, and platforms increasingly auto-detect; and while unaudited (TikTok SELF_ONLY) do NOT set brand_content_toggle (incompatible with SELF_ONLY)."
> 353	    }
> 354	  ],
> 355	  "recommendedSlicing": [
> 356	    "PASSO 0 — BoK gate (blocking, before any code): amend docs/bok/post-engine/ via /bok-scribe to (a) reconcile the obsolete 'social_credentials' name → live 'social_accounts'/social_accounts_table; (b) correct the platform list to the full live enum (adds facebook|linkedin|wordpress|pinterest); (c) document Vault encryption (post-dates the docs); (d) crave the per-platform scopes, audit gates, rotating-refresh semantics, and the publish/oauth branch designs from this blueprint as the Source of Truth; (e) embed the Pattern Conformance Declaration (this amendment's 21-row table). Register the env-credential deferral OTD + SLA.",
> 357	    "Slice 1 — Sovereign critical path STARTS DAY ONE (parallel to all coding): register the 3 developer apps (TikTok, Google/YouTube, Pinterest) to obtain client_id/secret, add TikTok sandbox target user, create/convert the YouTube Brand channel, and SUBMIT the longest-lead audits immediately (YouTube OAuth verification ~10d + Audit weeks SERIAL; TikTok audit ~2-6wk; Pinterest Trial ~1d then Standard). Without client_id/secret no OAuth can even begin — this gates everything.",
> 358	    "Slice 2 — TikTok E2E (single-tenant User Zero, env credentials): social-auth-init + callback + refresh branches + publish-social TikTok branch (FILE_UPLOAD + creator_info pre-flight + create→poll→publish + idempotency guard + rotating-refresh re-store). Prove 1 real SELF_ONLY self-post off the existing 9:16 HyperFrames MP4 (transport proven pre-audit; public reach unblocks on audit). /security-review any migration.",
> 359	    "Slice 3 — YouTube Shorts E2E (User Zero, env credentials): Google OAuth (offline+consent) branches + publish-social resumable videos.insert branch (fetch signed bytes → PUT → 201 → verify privacyStatus). Prove 1 upload (born private until Audit clears — transport proven). Materiality: assert privacyStatus, never claim public from a 201.",
> 360	    "Slice 4 — Pinterest video-pin E2E (User Zero, env credentials): Pinterest OAuth (Basic-auth, rotating-continuous-token, advisory-locked refresh) branches + publish-social 4-step video-pin branch (correct /v5/pins paths, board_id cache, multipart upload params-verbatim/file-last, public cover URL). Prove 1 pin (Trial sandbox-only — transport proven; public unblocks on Standard).",
> 361	    "Slice 5 — Cadence + auto-publish video gap (closes the cron-of-video path for ALL platforms incl. IG Reel): add youtube/tiktok/pinterest to VIDEO_FLOW_PLATFORMS (autopilot-run:109, reconcile billing at :111/:243) + fix auto-publish (:54-83) to resolve+sign content_library.media_url into a long-TTL public/signed video_url and pass content.video_url. This is the gap that makes scheduled video posts work autonomously (today only direct-invoke proven).",
> 362	    "Slice 6 — Persona spine (CCIO): swap the prompt seed from topic:product to the Gabriel AI / CCIO voice profile (fixed brand pillars, varied angles) so 'always speak about the brand' becomes engineering; optionally trend-informed angle via fetch-trends. Can fold into the BoK amendment.",
> 363	    "Slice 7 (deferred, post-audit + 2nd-tenant trigger): promote env credentials to per-user tiktok_config/youtube_config/pinterest_config tables (mirror meta_config encrypted-VIEW + INSTEAD OF + Settings UI cards); add multi-platform parallel fan-out with straggler timeout (OTD doctrine #3); close the Learning loop (OTD-AG-002)."
> 364	  ]
> 365	}
> ```

## 🤖 Claude *(03:59:36)*


## 🤖 Claude *(03:59:38)*

Síntese excelente e exaustiva. Deixa-me checar rapidamente as verificações adversariais (confiança + correções) para não carregar nada não-confirmado para a documentação.

## 🤖 Claude *(03:59:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 -c \"\nimport json\nd=json.load(open('/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/research.json'))\nfor x in d:\n    v=x['verify']\n    print('\u2550'*60)\n    print(f\\\"PLATFORM: {x['platform']}  | confidence: {v['confidence']}\\\")\n    if v.get('unverifiedClaims'):\n        print('  UNVERIFIED:')\n        for u in v['unverifiedClaims']:\n            c=u.get('claim','') if isinstance(u,dict) else str(u)\n            r=u.get('reason','') if isinstance(u,dict) else ''\n            print(f'    - {c[:160]} :: {r[:120]}')\n    if v.get('contradictions'):\n        print('  CONTRADICTIONS:')\n        for c in v['contradictions']: print(f'    - {c[:200]}')\n    if v.get('corrections'):\n        print('  CORRECTIONS:')\n        for c in v['corrections']: print(f'    - {c[:220]}')\n    if v.get('missingTopics'):\n        print('  MISSING TOPICS:')\n        for m in v['missingTopics']: print(f'    - {m[:160]}')\n\"",
  "description": "Summarize adversarial verify findings"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ════════════════════════════════════════════════════════════
> PLATFORM: tiktok  | confidence: high
>   UNVERIFIED:
>     - Error string on unaudited 24h cap violation is literally 'reached_active_user_cap' (and 'unaudited_client_can_only_post_to_private_accounts' for private-account :: PARTIAL. 'unaudited_client_can_only_post_to_private_accounts' IS confirmed verbatim in the official Direct Post referenc
>     - A Supabase-signed private-bucket URL is DISQUALIFIED for PULL_FROM_URL because it 'carries query params + is not under a static verified prefix' (in addition to :: The core fact IS confirmed: PULL_FROM_URL requires the video_url to be under a Domain or URL-Prefix property you have ve
>     - PULL_FROM_URL video_url 'MUST NOT redirect' (hard requirement). :: Doc wording is softer: 'The media URL must use https and should not redirect to another URL' — 'should not' (advisory) r
>     - fail_reason value 'spam_risk' (single value). :: Incomplete, not wrong. The official get-video-status doc enumerates more granular spam variants: 'spam_risk_too_many_pos
>   CORRECTIONS:
>     - SOURCE-URL FIX (unaudited caps): The claim about unaudited clients (5 users/24h, account-must-be-private, SELF_ONLY-only) and the '24-hour active creator cap from audit-form usage estimates' is attributed to https://deve
>     - PER-CREATOR CAP — exact number now official: The research says 'per-creator daily Direct-Post limit' without a number. Official content-sharing-guidelines states it: 'The upper limit may vary among creators (typically ar
>     - FAIL_REASON SET — expand: Official get-video-status fail_reason enumeration includes file_format_check_failed, duration_check_failed, frame_rate_check_failed, picture_size_check_failed, internal, video_pull_failed, photo
>     - PRIVATE-ACCOUNT PRIVACY OPTIONS — precise: creator_info/query for a PRIVATE account returns options FOLLOWER_OF_CREATOR, MUTUAL_FOLLOW_FRIENDS, SELF_ONLY (PUBLIC_TO_EVERYONE absent), per content-posting-api-reference-que
>   MISSING TOPICS:
>     - AUDIT LEAD TIME (quantified): Research correctly flags it as 'not published officially' — confirmed, TikTok's official docs state no timeline. But the integrati
>     - AUDIT REQUIRES A REVIEWABLE UX, not just a usage estimate: TikTok's audit verifies Terms-of-Service compliance and (per multiple sources) wants to see a complia
>     - UX / COMPLIANCE DISPLAY REQUIREMENTS (UX guidelines): TikTok publishes Content Sharing UX Guidance (creator must be shown/agree to privacy level, music-usage-co
>     - COMMERCIAL CONTENT / MUSIC USAGE CONFIRMATION: For branded/commercial content the API requires a music_usage_confirmation acknowledgement and the post may be re
>     - REVOCATION / DE-AUTH DETECTION beyond refresh: Research covers proactive refresh well, but does not describe detecting auth_removed at PUBLISH time (mid-flight 
>     - RATE-LIMIT / 429 HANDLING & BACKOFF: Per-endpoint per-token limits are listed, but no retry/backoff strategy, no mention of TikTok's standard error envelope (er
>     - SANDBOX / TARGET-USER ALLOWLIST for pre-audit testing: Before audit, TikTok apps run in a sandbox where only allowlisted 'target users' (added in the portal) ca
>     - DOMAIN/URL-PREFIX VERIFICATION = SEPARATE PORTAL PROVISIONING STEP (if PULL_FROM_URL ever used): The research recommends FILE_UPLOAD to sidestep this, which is 
>     - is_aigc LABELING — regulatory framing: Research correctly says set is_aigc=true. Worth elevating: TikTok applies a 'Creator labeled as AI-generated' tag and inc
>     - ERROR ENVELOPE / log_id for support + idempotency on init: No mention that every TikTok v2 response carries an error object {code, message, log_id} to persist f
> ════════════════════════════════════════════════════════════
> PLATFORM: youtube  | confidence: high
>   UNVERIFIED:
>     - As of the Dec 4 2025 change, videos.insert and search.list each have their OWN quota bucket with a default daily limit of 100 calls each, at 1 unit per call (so :: CONFLATION of two separate facts under one date. The revision_history Dec 4 2025 entry I fetched verbatim says ONLY: 'a 
>     - The Dec 4 2025 revision history logs the granular-quota transition starting with videos.insert and search.list (videos.insert cut from ~1600 to ~100/its own buc :: Mixes two distinct revision entries. Verbatim from revision_history: Dec 4 2025 = cost cut '~1600 units to ~100 units' (
>     - A member of YouTube's API Services team contacts you 'as soon as possible' (no fixed SLA) for the Audit & Quota Extension (sourceUrl: quota_and_compliance_audit :: The 'as soon as possible / no SLA' quote IS supported by the audit page (confirmed verbatim). BUT the research frames th
>     - 'the refresh_token is only returned on the FIRST authorization' ... ALWAYS send prompt=consent to force re-consent and GUARANTEE a fresh refresh_token (sourceUr :: Partially supported, slightly overstated. The web-server page confirms (a) refresh_token returned only if access_type=of
>   CONTRADICTIONS:
>     - Self-contradiction in the research's own quota narrative: the 'gotchas' block says videos.insert 'each call costs 1 unit with a dedicated default cap of 100 videos.insert calls/day' AND attributes thi
>     - Lead-time contradiction: the research's auditGates(A) says OAuth verification is 'reviewed manually' with no stated timeframe, but the official sensitive-scope-verification page states it 'can take up
>     - Source-tier contradiction for the videoSpec: the research presents '1080x1920, H.264, 30fps, <=3min, >=10 Mbps' as a hard spec but its only cited source for the Shorts spec is a third-party blog (shor
>   CORRECTIONS:
>     - Quota date/unit fix: On the Dec 4 2025 revision (https://developers.google.com/youtube/v3/revision_history), videos.insert cost dropped from ~1600 units to ~100 UNITS PER CALL — NOT to '1 unit'. The '1 unit per call + se
>     - OAuth verification lead-time: add the concrete SLA from https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification — 'the sensitive scope verification process can take up to
>     - Shorts duration source: replace the third-party https://www.shortsync.app/... source with the OFFICIAL YouTube Help page https://support.google.com/youtube/answer/15424877 ('Understand three-minute YouTube Shorts') — it 
>     - onBehalfOfContentOwner support: the server-side-web-apps page (https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps) supports the CMS-only claim only obliquely ('the YouTube Data API supports the ser
>   MISSING TOPICS:
>     - OAuth sensitive-scope verification lead time: the official 'up to 10 days' SLA for gate (A) is never stated; the research says 'no fixed SLA' which only applies
>     - Refresh-token rotation / DPoP: the web-server doc references DPoP-bound refresh tokens and re-issuance semantics. The research treats the refresh_token as a sta
>     - Live-token limit per client: Google caps the number of simultaneously-valid refresh tokens per OAuth client per user (default ~50/100 grants); when exceeded the
>     - Thumbnails.set as a SEPARATE sensitive operation: the research dismisses thumbnails as 'not required.' For brand persona content a custom thumbnail needs thumbn
>     - Quota-bucket volatility: because the per-method bucket model is brand-new (mid-2026) and was mis-dated in the research, the integration MUST treat the 100/day n
>     - Made-for-kids / synthetic-media disclosure enforcement: research sets containsSyntheticMedia=true and selfDeclaredMadeForKids=false but omits that YouTube indep
>     - Resumable-upload chunk/resume edge cases: the research states 256KB-multiple chunking and 308-resume, but omits the official guidance that the 308 response's Ra
> ════════════════════════════════════════════════════════════
> PLATFORM: pinterest  | confidence: high
>   UNVERIFIED:
>     - Create-pin endpoint is POST /v5/pins/create; board create is POST /v5/boards/create; media register is POST /v5/media (treated as a '/create'-style action). The :: REFUTED. The actual REST paths are POST /v5/pins, POST /v5/boards, GET /v5/boards, POST /v5/media, GET /v5/media/{media_
>     - Standard access is rate limited at 100 requests/second/user/app (sourceUrl rate-limits page). :: PARTIALLY CONTRADICTED by Pinterest's own docs. The rate-limits page does state 'Standard: 100 requests per second per u
>     - image_base64 is a supported media_source.source_type for image pins (alternative to image_url, sending data + content_type inline). :: Could NOT be confirmed from the official org-content guide (create-boards-and-pins), which only documented source_type=i
>     - The documented Trial-application denial triggers are a missing privacy policy URL and an incomplete app description ('privacy policy URL + complete app descript :: NOT supported by the connect-app page. The official page says only 'complete our request form with your app information'
>     - Carousel/multi-image pin field name (e.g. multiple_image_urls); and per-request max video FILE SIZE for organic pins. :: Both correctly self-flagged UNVERIFIED in the research, and verification CONFIRMS they remain unverified. The carousel l
>   CONTRADICTIONS:
>     - INTERNAL (Pinterest docs): Standard universal rate limit is '100 requests per SECOND per user per app' on the rate-limits page, but the access-tiers page describes Standard as 'calls per MINUTE per us
>     - RESEARCH vs OFFICIAL (paths): The research's endpoints[] list and steps[] use '/v5/pins/create', '/v5/boards/create' as REST paths, but the official org-content guide it cites uses these as doc-action
>     - RESEARCH-INTERNAL (board_id requirement): gotchas state 'BOARD MUST PRE-EXIST: /v5/pins/create requires board_id' as absolute, but the org-content guide notes an exception — ad-only Pins (is_removable
>   CORRECTIONS:
>     - CREATE-PIN PATH: Replace every 'POST /v5/pins/create' with the actual REST path 'POST https://api.pinterest.com/v5/pins'. The '/create' suffix is the doc-page slug (developers.pinterest.com/docs/api/v5/pins-create/), not
>     - CREATE-BOARD PATH: Replace 'POST /v5/boards/create' with 'POST https://api.pinterest.com/v5/boards' (doc slug: boards-create).
>     - LIST-BOARDS PATH: 'GET https://api.pinterest.com/v5/boards' is correct as written (doc slug: boards-list) — no change, but note the slug≠path pattern so the SDD doesn't 'fix' it wrongly.
>     - REGISTER-MEDIA PATH: 'POST https://api.pinterest.com/v5/media' is correct (doc slug: media-create) — confirmed by postproxy guide and the media-create slug. Keep as-is.
>     - POLL-MEDIA PATH: 'GET https://api.pinterest.com/v5/media/{media_id}' — correct (doc slug: media-get). Keep as-is.
>     - STANDARD RATE LIMIT UNIT: The binding creation limit is org_write = 100 requests/MINUTE/user/app under Standard (300/day under Trial), per https://developers.pinterest.com/docs/reference/rate-limits/. Use this, not the p
>     - DENIAL TRIGGERS: Soften the Trial denial-trigger claim — the official connect-app page does not enumerate denial reasons. Keep privacy-policy/description as recommended practice, not 'documented denial triggers'. Officia
>   MISSING TOPICS:
>     - TOKEN-REFRESH ATOMICITY UNDER CONCURRENCY: The research correctly flags that the rotating refresh_token must be persisted each cycle, but omits the concurrency 
>     - SCOPE-GRANT IMMUTABILITY ON RE-AUTH: Not addressed — if scopes change later (e.g. add pins:write_secret), the existing refresh token does NOT gain the new scope
>     - 429 RETRY-AFTER / RATE-LIMIT HEADERS: The research says 'design backoff on HTTP 429' but does not mention whether Pinterest returns X-RateLimit-Remaining / Retr
>     - SIGNED-URL TTL vs PINTEREST FETCH LATENCY: The public-URL dependency for image_url/cover_image_url is flagged, but not the operational constraint that Pinterest
>     - APP-REVIEW LEAD TIME (Standard upgrade) HAS NO SLA: Correctly noted there is no published SLA ('reviewed regularly'), but the integration plan needs an explicit
>     - UPLOAD-PARAMETERS VERBATIM + FIELD ORDER: The video step-2 multipart upload requires the upload_parameters map sent verbatim AND the file field LAST (S3 presign
>     - TRIAL SANDBOX-PIN URL RESOLVABILITY: Lei 1 materiality gap — under Trial, even the pin's own URL is creator-only/sandbox, so the autonomous run cannot produce a
>     - BUSINESS-ACCOUNT / DEVELOPER-TERMS as a SOVEREIGN IDENTITY ACTION: Like TikTok/YouTube, creating the Pinterest BUSINESS account, accepting Developer ToS, and ow
> ```

## 🤖 Claude *(04:00:17)*


## 🤖 Claude *(04:00:21)*

Todas as 3 plataformas verificadas em **confiança ALTA**. As correções adversariais já foram dobradas na síntese (paths `/v5/pins` corretos do Pinterest, FILE_UPLOAD no TikTok, atomicidade do refresh rotativo, gates de materialidade). Vou agora **selar o entregável de documentação** (PASSO 0 do gate BoK): o blueprint consolidado das 3 plataformas, fundamentado e com Pattern Conformance + SOPs.

## 🤖 Claude *(04:02:50)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/social-connect-3platforms-blueprint-2026-06-27.md",
  "content": "# Conectar Redes \u2014 TikTok + YouTube + Pinterest \u2014 Blueprint Consolidado (Lei 1)\n\n> **Data:** 2026-06-27 \u00b7 **Origem:** diretiva Sovereign *\"vamos conectar as redes \u2014 TikTok, YouTube, Pinterest\"* (virada brand-persona Gabriel AI / CCIO).\n> **Fundamenta\u00e7\u00e3o:** workflow `wf_b5a35451-7dc` (8 agentes \u00b7 recon material de c\u00f3digo + pesquisa fundamentada por plataforma + verifica\u00e7\u00e3o adversarial + s\u00edntese). **As 3 plataformas verificadas em confian\u00e7a ALTA**; cada claim externo ancorado em doc oficial (Lei 1).\n> **Supersede** o prep YT/TikTok de 2026-06-26 (`.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`) \u2014 acrescenta **Pinterest** (pe\u00e7a nova, antes n\u00e3o pesquisada) + Pattern Conformance + SOPs Lei 2 + corre\u00e7\u00f5es verificadas.\n> **Status:** PREPARA\u00c7\u00c3O / documenta\u00e7\u00e3o. **Nenhum c\u00f3digo de publisher escrito ainda.** **Gate MCORCH Closed-Loop:** PASSO 0 = emendar o BoK `post-engine` ANTES de codar (ver \u00a78).\n\n---\n\n## 1. Veredito de prontid\u00e3o (o achado central \u2014 confirmado contra o c\u00f3digo vivo)\n\n**~90% j\u00e1 existe e \u00e9 reus\u00e1vel as-is.**\n\n- **Enum pronto:** `social_platform` j\u00e1 cont\u00e9m `linkedin|instagram|facebook|twitter|tiktok|youtube|pinterest|wordpress` (migration `20260402014040:12`) \u2014 **ZERO migration de enum** para as 3.\n- **Storage de token pronto:** `social_accounts` \u00e9 VIEW Vault-mascarada que j\u00e1 cifra `access_token`/`refresh_token` + `token_expires_at` + `scopes` + `metadata`, escrita pelo INSTEAD OF trigger tenant-guarded (`auth.uid()=user_id`) com `.upsert({onConflict:'user_id,platform'})` \u2014 reuso verbatim.\n- **OAuth gen\u00e9rico pronto:** `social-auth-init` assina state HMAC-SHA256; `social-auth-callback` verifica (janela replay 10min) e faz upsert. S\u00f3 os **branches por-plataforma** (authorize-URL + code\u2192token) s\u00e3o net-new.\n- **Padr\u00e3o publish pronto:** `publish-social` j\u00e1 tem pre-check de refresh (`:85`) e o padr\u00e3o de 3 passos **create\u2192poll\u2192publish** provado no IG REELS (`:141-196`) que TikTok e Pinterest-v\u00eddeo espelham.\n- **M\u00eddia pronta:** o **MP4 9:16 1080\u00d71920 H.264** do HyperFrames (`video-studio-assets`, NFR-VS-016) est\u00e1 in-spec para as 3 (TikTok 360\u20134096px/23\u201360fps; YouTube Shorts \u22643min vertical; Pinterest 9:16 recomendado, \u22654s).\n\n**Net-new (c\u00f3digo):** 3 branches publish + 3 branches oauth-init + 3 branches callback + 3 branches refresh (todos cientes de **rota\u00e7\u00e3o de refresh token**), o **gap de transporte de `video_url`** no `auto-publish` (n\u00e3o h\u00e1 coluna `video_url` em `scheduled_posts`; o `auto-publish` nunca resolve/assina `media_url`), o Set `VIDEO_FLOW_PLATFORMS`, mais a **diverg\u00eancia de transfer\u00eancia de m\u00eddia por plataforma**.\n\n**Os blockers DUROS s\u00e3o 100% fora do c\u00f3digo** (3 registros de app de dev + 3 audits). Sem eles n\u00e3o h\u00e1 `client_id`/`secret` \u2192 **nenhum OAuth sequer come\u00e7a**, e todo publish \"bem-sucedido\" \u00e9 invis\u00edvel (TikTok SELF_ONLY \u00b7 YouTube forced-private \u00b7 Pinterest sandbox). **Ver \u00a76 \u2014 \u00e9 o caminho cr\u00edtico.**\n\n---\n\n## 2. Change-list por plataforma (seams file:line \u2014 do recon material)\n\nTodos os branches entram **antes** do fallback. Dispatch atual em `publish-social/index.ts`: linkedin `:115-140` \u00b7 instagram `:141-197` \u00b7 facebook `:198-216` \u00b7 twitter `:217-233` \u00b7 fallback `:234-239`.\n\n### 2.1 TikTok \u2014 Content Posting API (Direct Post, aut\u00f4nomo)\n\n| Componente | Arquivo:seam | O que adicionar |\n|---|---|---|\n| OAuth init | `social-auth-init/index.ts:95` | `else if (platform==='tiktok')` \u2192 `https://www.tiktok.com/v2/auth/authorize/` com `client_key`, `response_type=code`, `redirect_uri` (pr\u00e9-registrada, https, est\u00e1tica, \u2264512 chars), `state` (j\u00e1 assinado `:56`), `scope=video.publish,user.info.basic` **separado por V\u00cdRGULA** (espa\u00e7o falha o consent em sil\u00eancio). `video.publish` \u00e9 o scope cr\u00edtico (Direct Post); **NUNCA `video.upload`** (draft-to-inbox exige humano finalizar no app). PKCE opcional (defense-in-depth). |\n| OAuth callback | `social-auth-callback/index.ts:171` | branch TikTok: `POST https://open.tiktokapis.com/v2/oauth/token/` `grant_type=authorization_code` + `client_key`+`client_secret`+`code`+`redirect_uri`. Resposta: `access_token` (86400s), `refresh_token` (31536000s), `open_id`, `scope`. Upsert: `platform_user_id=open_id`. |\n| Publish | `publish-social/index.ts:233` | `else if (platform==='tiktok')` \u2014 3 passos: **(1)** pr\u00e9-flight obrigat\u00f3rio `POST /v2/post/publish/creator_info/query/` (20/min) \u2192 ecoar um valor DE `privacy_level_options` (conta n\u00e3o-auditada/privada: s\u00f3 `FOLLOWER_OF_CREATOR`/`MUTUAL_FOLLOW_FRIENDS`/`SELF_ONLY`, sem `PUBLIC_TO_EVERYONE`); **N\u00c3O** setar `disable_comment/duet/stitch=false` quando o respectivo `*_disabled=true`. **(2)** `POST /v2/post/publish/video/init/` (6/min) com `post_info{title \u22642200 runes UTF-16, privacy_level, is_aigc:true [compliance MUST p/ persona IA], brand_content_toggle S\u00d3 se N\u00c3O SELF_ONLY}` + `source_info` **source=FILE_UPLOAD** (`video_size`/`chunk_size`/`total_chunk_count`; chunks 5\u201364MB, final \u2264128MB, <5MB single, 1\u20131000 chunks) \u2014 Supabase signed URL **N\u00c3O** passa no domain-ownership do `PULL_FROM_URL`. Retorna `publish_id`. **(3)** PUT chunks no `upload_url` com `Content-Range` (re-init em 403 expirado). **(4)** poll `POST /v2/post/publish/status/fetch/` (30/min) at\u00e9 `PUBLISH_COMPLETE`; tratar o set de `fail_reason` (`video_pull_failed`,`file_format_check_failed`,`duration_check_failed`,`frame_rate_check_failed`,`picture_size_check_failed`,`publish_cancelled`,`auth_removed`,`spam_risk_*`,`internal`). `result.id` \u2190 `publicaly_available_post_id` (erro de grafia literal da TikTok; s\u00f3 populado quando p\u00fablico+aprovado). **Guard de idempot\u00eancia** keyed em content/run id ANTES do init (re-init cunha novo `publish_id` \u2192 double-post). Persistir envelope `{code,message,log_id}`. |\n| Refresh | `refresh-social-token/index.ts:133` | branch TikTok: `POST .../v2/oauth/token/` `grant_type=refresh_token`. **ROTATIVO** \u2014 re-armazenar o `refresh_token` retornado quando diferir (sen\u00e3o outage em c\u00e2mera lenta). Cron di\u00e1rio DEVE refrescar proativamente antes do expiry de 24h do access_token. |\n\n### 2.2 YouTube \u2014 Data API v3 `videos.insert` resumable (Shorts = formato)\n\n| Componente | Arquivo:seam | O que adicionar |\n|---|---|---|\n| OAuth init | `social-auth-init/index.ts:95` | `else if (platform==='youtube')` \u2192 `https://accounts.google.com/o/oauth2/v2/auth` com `client_id`, `redirect_uri`, `response_type=code`, `scope=https://www.googleapis.com/auth/youtube.upload`, `state`, **`access_type=offline`+`prompt=consent`** (refresh_token s\u00f3 vem na 1\u00aa autoriza\u00e7\u00e3o / re-consent for\u00e7ado \u2014 sem `prompt=consent` a re-auth devolve refresh_token NULO em sil\u00eancio). No account-chooser o user DEVE escolher o canal Brand correto (Gabriel AI / CCIO). |\n| OAuth callback | `social-auth-callback/index.ts:171` | branch YouTube: `POST https://oauth2.googleapis.com/token` `grant_type=authorization_code`. Resposta: `access_token` (~3600s), `refresh_token` (s\u00f3 1\u00aa auth), `expires_in`. Resolver canal (`GET youtube/v3/channels?mine=true`) \u2192 `platform_user_id`/`metadata.channel_id`. **CR\u00cdTICO: nunca anular um refresh_token armazenado numa resposta sem refresh.** |\n| Publish | `publish-social/index.ts:233` | `else if (platform==='youtube')` resumable (sem PULL_FROM_URL \u2014 YouTube n\u00e3o tem ingest remoto, ent\u00e3o FETCH dos bytes da signed URL \u2192 PUT): **(1)** `POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status` headers `Authorization Bearer`, `X-Upload-Content-Length=<bytes>`, `X-Upload-Content-Type=video/mp4`; body `{snippet:{title,description,tags,categoryId:'22'},status:{privacyStatus:'public',selfDeclaredMadeForKids:false,containsSyntheticMedia:true}}`. **(2)** capturar session URI do header `Location` (200). **(3)** PUT bytes (chunks m\u00faltiplos de 256KB + `Content-Range`; `308`=Resume Incomplete \u2192 retomar do byte do `Range`, mas tolerar `Range` AUSENTE = restart do 0, e session-URI expira ~1 semana = re-iniciar). **(4)** sucesso = `201` com video resource id \u2192 `result.id`. Shorts \u00e9 IMPL\u00cdCITO (1080\u00d71920+\u22643min auto-classifica). **MATERIALIDADE (Lei 1):** um `201` N\u00c3O significa p\u00fablico \u2014 at\u00e9 o Audit do projeto passar, projeto n\u00e3o-verificado FOR\u00c7A todo upload p/ `private` ignorando o `privacyStatus` pedido; **verificar `videos.get?part=status` `privacyStatus` antes de afirmar 'p\u00fablico'.** Cap di\u00e1rio no bucket `videos.insert` (atualmente ~100/dia \u2014 **ler a Quota Calculator viva, o modelo de bucket \u00e9 recente/m\u00f3vel**: Dec-2025 o custo caiu de ~1600 \u2192 ~100 **units** por call, cada m\u00e9todo com seu bucket). |\n| Refresh | `refresh-social-token/index.ts:133` | branch YouTube: `POST https://oauth2.googleapis.com/token` `grant_type=refresh_token` \u2192 novo `access_token`+`expires_in`; `token_expires_at=now+3600`. Google geralmente N\u00c3O rotaciona refresh tokens n\u00e3o-DPoP, mas tolerar um novo em re-consent e **NUNCA sobrescrever um token bom com null**. `invalid_grant` no dia 8 = app ainda em **Testing** (scope sens\u00edvel \u2192 refresh expira 7d); fix \u00e9 o gate A (In production), n\u00e3o retry-loop. |\n| Cad\u00eancia | `autopilot-run/index.ts:109` | `VIDEO_FLOW_PLATFORMS` (hoje `new Set(['wordpress'])`) ganha `'youtube'` (e `'tiktok'`/`'pinterest'` quando seus flows pousarem) \u2192 enfileira render 9:16 + cobra `VIDEO_COST`. Reconciliar billing em `:111` e `:243` (FR-VA-022/024). |\n\n### 2.3 Pinterest \u2014 API v5 (video pin, 4 passos async) \u2014 **NET-NEW**\n\n| Componente | Arquivo:seam | O que adicionar |\n|---|---|---|\n| OAuth init | `social-auth-init/index.ts:95` | `else if (platform==='pinterest')` \u2192 `https://www.pinterest.com/oauth/` com `client_id`, `redirect_uri` (match EXATO a uma entrada Configure>Redirect URIs \u2014 sem wildcard), `response_type=code`, `scope=boards:read,boards:write,pins:read,pins:write,user_accounts:read`, `state`. **Planejar o set COMPLETO de scopes de cara** \u2014 adicionar scope depois for\u00e7a re-autoriza\u00e7\u00e3o total (refresh token existente n\u00e3o ganha). Sem PKCE (v5 \u00e9 confidential-client Authorization-Code). |\n| OAuth callback | `social-auth-callback/index.ts:171` | branch Pinterest: `POST https://api.pinterest.com/v5/oauth/token` `grant_type=authorization_code`+`code`+`redirect_uri`, header `Authorization: Basic base64(client_id:client_secret)`. Resposta: `access_token` (2592000s=30d), `refresh_token` (cont\u00ednuo, rotativo), `refresh_token_expires_at`. Identidade: `GET /v5/user_account`. Upsert `token_expires_at=now+2592000` + `metadata.refresh_token_expires_at`. |\n| Publish | `publish-social/index.ts:233` | `else if (platform==='pinterest')` VIDEO pin 4 passos: **(0)** garantir board destino \u2014 `GET https://api.pinterest.com/v5/boards` (achar `board_id`) sen\u00e3o `POST .../v5/boards` UMA vez; **cachear o board_id (N\u00c3O criar por run)**. **(1)** register: `POST https://api.pinterest.com/v5/media {media_type:'video'}` \u2192 `media_id`+`upload_url`+`upload_parameters`. **(2)** upload: `POST` o MP4 no `upload_url` como `multipart/form-data` com TODOS os `upload_parameters` VERBATIM e o **campo `file` por \u00daLTIMO** (ordena\u00e7\u00e3o de presigned-POST S3; ordem errada/param mutado \u2192 403), SEM Bearer, sucesso=`204`. **(3)** poll: `GET https://api.pinterest.com/v5/media/{media_id}` com backoff at\u00e9 `status='succeeded'`. **(4)** create: `POST https://api.pinterest.com/v5/pins {board_id, title \u2264100, description \u2264800, link, media_source:{source_type:'video_id', media_id, cover_image_url:'<URL https P\u00daBLICA>'}}` \u2192 `201` com pin id = `result.id`. **`cover_image_url` \u00e9 OBRIGAT\u00d3RIA e \u00e9 PUXADA async pela Pinterest** \u2192 a cover precisa sobreviver num URL p\u00fablico/signed-de-TTL-longo (TTL curto expira antes do fetch e falha o pin em sil\u00eancio); o bin\u00e1rio do v\u00eddeo \u00e9 enviado (n\u00e3o puxado). **PATHS CORRETOS:** `/v5/pins`, `/v5/boards`, `/v5/media` (N\u00c3O `/v5/pins/create` etc. \u2014 aqueles s\u00e3o slugs de doc e d\u00e3o 404). **MATERIALIDADE (Lei 1):** sob **Trial** o pin \u00e9 sandbox/creator-only \u2014 sem URL p\u00fablico resolv\u00edvel \u2014 n\u00e3o afirmar 'publicado ao vivo' at\u00e9 **Standard**. Backoff em 429 contra `org_write` (300/dia Trial, 100/min Standard). |\n| Refresh | `refresh-social-token/index.ts:133` | branch Pinterest: `POST https://api.pinterest.com/v5/oauth/token` `grant_type=refresh_token`, header Basic. **ROTATIVO \u2014 cada refresh retorna NOVO access_token E NOVO refresh_token**; persistir ambos **ATOMICAMENTE** (advisory-lock/SELECT-FOR-UPDATE em torno do refresh\u2192persist, espelhando `begin_autopilot_cycle`) p/ evitar lost-update entre cron e run manual que quebra a cadeia e for\u00e7a re-OAuth. Refrescar dentro da janela de 60d mant\u00e9m a cadeia viva indefinidamente. |\n\n**Schema novo:** NENHUMA tabela de token nova; NENHUMA migration de enum. \u00danico schema recomendado (difer\u00edvel p/ Usu\u00e1rio Zero \u2014 ver \u00a77 decis\u00e3o #1): `tiktok_config`/`youtube_config`/`pinterest_config` per-user p/ **app credentials**, espelhando `meta_config` (VIEW cifrada + INSTEAD OF tenant-guard + column-REVOKE no secret).\n\n---\n\n## 3. Fatos fundamentados \u2014 tokens, audit gates, specs (verificado HIGH)\n\n| | TikTok | YouTube | Pinterest |\n|---|---|---|---|\n| **Access token** | 24h (86400s) | ~1h (3600s) | 30d (2592000s) |\n| **Refresh token** | 365d, **rotativo** | longo (prod-verified); 7d em Testing | 60d-from-last-use, **rotativo cont\u00ednuo** |\n| **Gate 1 (conex\u00e3o)** | registrar app + Content Posting API Direct Post + add conta como sandbox target user | criar/converter canal Brand + OAuth consent (External) | Business account + Developer Terms + privacy-policy URL \u2192 Trial |\n| **Gate 2 (p\u00fablico)** | **audit** Content Posting (~2\u20136 sem) \u2014 sem ele: SELF_ONLY + conta privada + \u22645 users/24h | **(A)** OAuth verification scope sens\u00edvel (**~10 dias**) + **(B)** API Audit & Quota Extension (semanas, **serial+independente** de A) \u2014 sem B: upload FOR\u00c7ADO a private | **Trial\u2192Standard** upgrade (demo de OAuth + a\u00e7\u00e3o API ao vivo) \u2014 sem ele: sandbox/creator-only |\n| **Transfer de m\u00eddia** | FILE_UPLOAD chunked (signed URL n\u00e3o passa no PULL_FROM_URL) | resumable PUT (fetch bytes \u2192 PUT; sem ingest remoto) | register\u2192multipart(params verbatim,file last)\u2192poll\u2192create + cover P\u00daBLICA |\n| **Rate/cap** | init 6/min \u00b7 ~15 posts/dia/criador | `videos.insert` ~100/dia (bucket pr\u00f3prio, modelo m\u00f3vel) | `org_write` 300/dia Trial \u00b7 100/min Standard |\n\n---\n\n## 4. Pattern Conformance Declaration (doutrina `docs/architecture/agentic-vision.md` \u2014 21 padr\u00f5es)\n\n> Para a emenda do BoK `post-engine`. `yes`=implementado nesta camada \u00b7 `deferred`=justificado \u00b7 `n-a`=fora de escopo da camada de transporte.\n\n| Pattern | Status | Como / Por que diferido |\n|---|---|---|\n| Prompt Chaining | yes | cada publish \u00e9 cadeia multi-step (TikTok creator_info\u2192init\u2192upload\u2192status; YT initiate\u2192PUT\u2192201; Pinterest register\u2192upload\u2192poll\u2192create), espelhando IG REELS `:141-196`. |\n| Routing | yes | `publish-social` roteia por `platform` (dispatch\u2192fallback `:234`); +3 branches + roteamento de media-transfer por plataforma. |\n| Parallelization | deferred | fan-out multi-plataforma do mesmo MP4 diferido p/ manter slices probe-first seriais; rastreado no gap de doutrina #3 (sem timeout/circuit-break em straggler). |\n| Reflection | deferred | Vision-QA do criativo 9:16 pr\u00e9-publish \u00e9 o loop Generator-Critic relevante, mas vive na camada criativa upstream (`vision-qa.ts`), n\u00e3o no publisher (OTD-AG-003). |\n| Tool Use | yes | cada branch \u00e9 invoca\u00e7\u00e3o tipada de API externa dentro do edge fn JWT/service-role-guarded; secrets nunca no cliente. |\n| Planning | n-a | publishers executam sequ\u00eancia fixa documentada; o plano de cad\u00eancia \u00e9 upstream (`autopilot-run` optimization_policy). |\n| Multi-Agent | n-a | camada de transporte; n\u00e3o spawna/coordena agentes. |\n| Memory Management | yes | 1\u00ba publish bem-sucedido por plataforma insere observation node na Knowledge Mesh; `platform_post_id` + `creative_metrics` p/ atribui\u00e7\u00e3o/recall. |\n| Learning & Adaptation | deferred | `creative_metrics` por plataforma alimenta o reward, mas o loop fechado \u00e9 OTD-AG-002 (P0); marcar `yes` fabricaria o link recursivo ainda manual. |\n| Model Context Protocol | n-a | sem superf\u00edcie MCP; s\u00e3o REST atr\u00e1s de edge fns. |\n| Goal Setting & Monitoring | yes | todo path (success/degraded/error) emite `infra_health_logs` `service='publish-<platform>'`; gates de materialidade = sinais monitorados. |\n| Exception Handling & Recovery | yes | cada branch mapeia o set de falha p/ recovery estruturado (TikTok fail_reason+idempot\u00eancia; YT 308-resume+restart; Pinterest poll-backoff+token at\u00f4mico). |\n| Human-in-the-Loop | yes | gates duros s\u00e3o Sovereign-gated by design (registro de app, 3 audits, domain verify, canal, Trial\u2192Standard); at\u00e9 audit, publishes privados \u2014 humano aprova ir p\u00fablico. |\n| Knowledge Retrieval (RAG) | n-a | publishers n\u00e3o fazem retrieval em runtime; escrevem observation nodes mas n\u00e3o consultam a mesh p/ publicar. |\n| Inter-Agent Communication (A2A) | n-a | sem troca agente-a-agente; s\u00f3 o invoke edge-to-edge service-role existente. |\n| Resource-Aware Optimization | yes | `VIDEO_COST` cobrado at\u00f4mico no pr\u00e9-d\u00e9bito do autopilot; rate limits respeitados; refund/no-mint reusado em enqueue-fail. |\n| Reasoning Techniques | n-a | transporte determin\u00edstico; sem reasoning LLM no publish. |\n| Guardrails / Safety | yes | RLS default-deny + Vault/column-REVOKE + state HMAC + resolu\u00e7\u00e3o per-user fail-closed + `is_aigc`/`containsSyntheticMedia` disclosure + `/security-review` em migration nova (FMEA-011). |\n| Evaluation & Monitoring | yes | sucesso \u2260 2xx (Lei 1): YT `privacyStatus='public'` \u00b7 TikTok `PUBLISH_COMPLETE`+`publicaly_available_post_id` \u00b7 Pinterest URL p\u00fablico (p\u00f3s-Standard); Vision-QA pr\u00e9-publish; feed do Collective Efficiency Ledger. |\n| Prioritization | deferred | ordem de slices \u00e9 curada por humano, n\u00e3o scheduler formal (gap doutrina #20). |\n| Exploration & Discovery | n-a | publishers s\u00e3o transporte confirmat\u00f3rio; sele\u00e7\u00e3o de \u00e2ngulo trend-informed (FR-VA-018) \u00e9 upstream. |\n\n---\n\n## 5. SOPs Lei 2 (esqueleto \u2014 Operator / Sequence / Verification / Recovery / Success)\n\n**ORO (as 3):** Operator = MCORCH Master Execution Agent (c\u00f3digo) + Sovereign (registro de app/audit/autoriza\u00e7\u00e3o) \u00b7 Reviewer = Sovereign \u00b7 Owner = Sovereign.\n\n### 5.1 TikTok\n- **Sequence:** 1) registrar app + Content Posting Direct Post + scope `video.publish` + add conta sandbox \u2192 **prova:** `client_key`+`client_secret` no portal. 2) OAuth (scope v\u00edrgula) \u2192 callback `/v2/oauth/token/` \u2192 **prova:** linha `social_accounts` platform=tiktok com `open_id` (SELECT id = UUID). 3) `creator_info/query` \u2192 **prova:** 200 + `privacy_level_options`. 4) `video/init/` FILE_UPLOAD + `is_aigc=true` \u2192 **prova:** `publish_id`. 5) PUT chunks `Content-Range` \u2192 **prova:** 2xx por chunk. 6) `status/fetch` at\u00e9 `PUBLISH_COMPLETE`.\n- **Recovery:** `fail_reason` switch (`*_check_failed`\u2192reencode; `auth_removed`\u2192re-autorizar via Login Kit, n\u00e3o-automatiz\u00e1vel; `spam_risk_*`\u2192back off ~15/dia); `upload_url` 403\u2192re-init guardado por idempotency key; 429\u2192backoff capturando `log_id`; refresh rotacionado\u2192re-store at\u00f4mico.\n- **Success:** PRE-AUDIT `PUBLISH_COMPLETE` SELF_ONLY vis\u00edvel ao criador (transporte provado). POST-AUDIT URL `tiktok.com` p\u00fablico (`publicaly_available_post_id`) \u2014 \u00fanica afirma\u00e7\u00e3o honesta de \"ao vivo\".\n\n### 5.2 YouTube\n- **Sequence:** 1) canal Brand existe (`channels?mine=true`=id). 2) OAuth consent verification + In production \u2192 **prova:** sem warning, refresh para de expirar em 7d. 3) submeter API Audit & Quota Extension \u2192 **prova:** email de aprova\u00e7\u00e3o (levanta forced-private). 4) OAuth offline+consent \u2192 **prova:** linha com refresh_token + channel_id. 5) resumable POST\u2192Location\u2192PUT \u2192 **prova:** `201` + video id. 6) `videos?id=&part=status` \u2192 **prova:** `privacyStatus='public'`.\n- **Recovery:** `308`\u2192retomar do Range; `Range` ausente\u2192restart byte 0; session expirada (~1sem)\u2192re-iniciar; `invalid_grant`\u2192app em Testing (gate A), escalar; forced-private apesar de public\u2192Audit (gate B) n\u00e3o passou, **halt** nas afirma\u00e7\u00f5es de \"p\u00fablico\".\n- **Success:** video id cujo `videos.get`=`privacyStatus='public'` E URL `youtube.com/shorts` resolve \u2014 gates A E B passados.\n\n### 5.3 Pinterest\n- **Sequence:** 1) Business account + Developer Terms + privacy-policy URL + redirect EXATO \u2192 **prova:** Trial + client_id/secret. 2) upgrade Standard com demo (OAuth + a\u00e7\u00e3o v5 ao vivo) \u2192 **prova:** email Standard. 3) OAuth Basic \u2192 `/v5/oauth/token` \u2192 **prova:** linha com refresh rotativo + `refresh_token_expires_at`. 4) `GET/POST /v5/boards` \u2192 **prova:** `board_id` cacheado. 5) register\u2192upload(params verbatim,file last)\u2192poll `succeeded`\u2192`POST /v5/pins` cover p\u00fablica \u2192 **prova:** `201` pin id. 6) sob Standard, URL p\u00fablico resolve.\n- **Recovery:** media `failed`\u2192re-register+re-upload; multipart 403\u2192params verbatim+file last; cover expirada\u2192signed TTL-longo/bucket p\u00fablico; 429\u2192backoff `org_write`; refresh rotativo perdido (concorr\u00eancia)\u2192advisory-lock; Standard negado\u2192re-gravar demo.\n- **Success:** PRE-STANDARD `201` pin id (Trial sandbox, transporte provado). POST-STANDARD URL `pinterest.com/pin/<id>` p\u00fablico.\n\n---\n\n## 6. \u26a0\ufe0f A\u00e7\u00f5es Sovereign \u2014 CAMINHO CR\u00cdTICO (fora do c\u00f3digo, lead-time de semanas)\n\n> **Sem o registro do app n\u00e3o h\u00e1 `client_id`/`secret` \u2192 nenhum OAuth come\u00e7a.** Come\u00e7ar HOJE; os audits t\u00eam o maior lead-time e correm em paralelo ao c\u00f3digo.\n\n| # | A\u00e7\u00e3o | Plataforma | Destrava | Lead-time |\n|---|---|---|---|---|\n| 1 | Registrar app TikTok + Content Posting API (Direct Post) + add a conta da persona como sandbox target user | TikTok | client_key/secret + teste E2E pr\u00e9-audit | horas\u20132 dias |\n| 2 | Submeter **TikTok Content Posting API audit** (usage-estimates + walkthrough/screencast de UX compliant) | TikTok | posts P\u00daBLICOS (levanta SELF_ONLY/privado/\u22645users) | **~2\u20136 semanas** (sem SLA) |\n| 3 | Criar/converter o canal YouTube Gabriel AI / CCIO no Brand Account correto | YouTube | alvo do upload | minutos |\n| 4 | OAuth consent verification (Google Cloud) p/ `youtube.upload` (justificativa + demo) + In production | YouTube | tira warning + mata expiry de 7d do refresh (gate A) | **~10 dias** |\n| 5 | Submeter **YouTube API Services Audit & Quota Extension Form** | YouTube | uploads P\u00daBLICOS (sen\u00e3o forced-private) (gate B) | semanas, sem SLA |\n| 6 | Pinterest Business + Developer Terms + privacy-policy URL \u2192 pedir Trial | Pinterest | qualquer acesso v5 + client_id/secret | ~1 dia \u00fatil |\n| 7 | Submeter **Pinterest Trial\u2192Standard** (demo OAuth + a\u00e7\u00e3o API ao vivo) | Pinterest | pins P\u00daBLICOS + rate maior | sem SLA (~dias) |\n\n**Gates A+B do YouTube s\u00e3o SERIAIS+independentes \u2192 prontid\u00e3o total = a SOMA (~10d + semanas), n\u00e3o o m\u00e1ximo.** Por isso submeter ambos no dia 1.\n\n---\n\n## 7. Decis\u00f5es abertas (genuinamente do Sovereign)\n\n1. **App-credentials: env-override-com-SLA vs tabelas per-user agora.** \u2192 **Recomenda\u00e7\u00e3o:** env (`TIKTOK_CLIENT_KEY/SECRET`, `GOOGLE_CLIENT_ID/SECRET`, `PINTEREST_CLIENT_ID/SECRET`) como default Sovereign-only de onboarding (o App Tenancy Model permite) p/ as slices probe \u2014 Usu\u00e1rio Zero \u00e9 o \u00fanico tenant e os 3 audits s\u00e3o o caminho cr\u00edtico real, n\u00e3o a tabela de config. **Registrar OTD + SLA** p/ n\u00e3o virar d\u00edvida silenciosa; promover a `*_config` per-user antes do 2\u00ba tenant. (Tokens per-USER j\u00e1 v\u00e3o p/ `social_accounts` de qualquer forma.)\n2. **TikTok media transfer: FILE_UPLOAD vs verificar-dom\u00ednio-p/-PULL_FROM_URL.** \u2192 **Recomenda\u00e7\u00e3o:** FILE_UPLOAD \u2014 desacopla do passo Sovereign-gated de domain verification e funciona direto do bucket privado.\n3. **Qual plataforma primeiro.** \u2192 **Recomenda\u00e7\u00e3o:** **TikTok primeiro** (menor atrito a um self-post real em sandbox, prova o transporte FILE_UPLOAD+create\u2192poll\u2192publish E2E mais r\u00e1pido), **em PARALELO** disparar J\u00c1 os gates A+B do YouTube (maior lead-time, serial \u2014 come\u00e7ar o rel\u00f3gio da depend\u00eancia mais lenta no dia 1).\n4. **`auto-publish` video_url: coluna em `scheduled_posts` vs resolver-no-dispatch.** \u2192 **Recomenda\u00e7\u00e3o:** resolver+assinar no dispatch (sem migration), signed URL de TTL longo (horas) p/ sobreviver ao fetch async de Pinterest/IG; coluna s\u00f3 se virar requisito de auditoria/atribui\u00e7\u00e3o. Fecha o gap documentado (hoje passa s\u00f3 texto) \u2014 tamb\u00e9m conserta o IG Reel agendado (hoje s\u00f3 provado por invoke direto).\n5. **Rotulagem AIGC.** \u2192 **Recomenda\u00e7\u00e3o:** sempre rotular IA-gerado (`is_aigc=true`/`containsSyntheticMedia=true`) \u2014 \u00e9 compliance, n\u00e3o opcional; e enquanto n\u00e3o-auditado (TikTok SELF_ONLY) N\u00c3O setar `brand_content_toggle` (incompat\u00edvel com SELF_ONLY).\n\n---\n\n## 8. Fatiamento recomendado (probe-first, single-tenant Usu\u00e1rio Zero)\n\n- **PASSO 0 \u2014 Gate BoK (bloqueante, antes de qualquer c\u00f3digo):** emendar `docs/bok/post-engine/` via `/bok-scribe`: (a) reconciliar `social_credentials`\u2192`social_accounts`/`social_accounts_table`; (b) corrigir lista de plataformas p/ o enum vivo; (c) documentar a cifra Vault; (d) cravar scopes/audit-gates/refresh-rotativo + o design dos branches deste blueprint como Fonte da Verdade; (e) embutir a Pattern Conformance Declaration (\u00a74). Registrar o OTD do deferimento de credencial env + SLA.\n- **Slice 1 \u2014 Caminho cr\u00edtico Sovereign COME\u00c7A NO DIA 1 (paralelo a todo c\u00f3digo):** registrar os 3 apps, add sandbox user TikTok, criar/converter canal YouTube, **submeter j\u00e1 os audits de maior lead-time** (\u00a76).\n- **Slice 2 \u2014 TikTok E2E** (env creds): init+callback+refresh + branch publish (FILE_UPLOAD + creator_info + create\u2192poll\u2192publish + idempot\u00eancia + re-store rotativo). Provar 1 self-post SELF_ONLY real do MP4 9:16 existente. `/security-review` em qualquer migration.\n- **Slice 3 \u2014 YouTube Shorts E2E** (env creds): branches Google OAuth (offline+consent) + resumable `videos.insert` (fetch signed bytes\u2192PUT\u2192201\u2192verificar `privacyStatus`). Nasce private at\u00e9 Audit \u2014 transporte provado.\n- **Slice 4 \u2014 Pinterest video-pin E2E** (env creds): OAuth Basic rotativo advisory-locked + branch 4-passos (paths `/v5/*` corretos, board_id cache, multipart params-verbatim/file-last, cover p\u00fablica). Pin sob Trial sandbox \u2014 transporte provado.\n- **Slice 5 \u2014 Cad\u00eancia + gap do auto-publish** (fecha o cron-de-v\u00eddeo p/ TODAS incl. IG Reel): `youtube/tiktok/pinterest` em `VIDEO_FLOW_PLATFORMS` (`autopilot-run:109`, billing `:111`/`:243`) + `auto-publish:54-83` resolve+assina `content_library.media_url`\u2192`video_url` TTL-longo e passa `content.video_url`.\n- **Slice 6 \u2014 Spine de persona (CCIO):** trocar a semente de `topic:produto` p/ o perfil de voz Gabriel AI/CCIO (pilares fixos, \u00e2ngulos vari\u00e1veis); opcional trend-informed (fetch-trends). Pode dobrar na emenda BoK.\n- **Slice 7 (diferido, p\u00f3s-audit + gatilho de 2\u00ba tenant):** promover env\u2192`*_config` per-user (mirror meta_config + UI Settings); fan-out paralelo multi-plataforma com straggler timeout; fechar o loop de Learning (OTD-AG-002).\n\n---\n\n## 9. Fontes (Lei 1)\nVer `wf_b5a35451-7dc` (transcript) p/ a lista completa por claim. Oficiais consultadas: **TikTok** developers.tiktok.com/doc/{content-posting-api-reference-direct-post,-get-started,-media-transfer-guide,content-sharing-guidelines,oauth-user-access-token-management,content-posting-api-reference-query-creator-info}. **YouTube** developers.google.com/youtube/v3/{guides/using_resumable_upload_protocol,docs/videos/insert,determine_quota_cost,revision_history,guides/quota_and_compliance_audits,guides/auth/server-side-web-apps} + identity/protocols/oauth2/production-readiness/sensitive-scope-verification + support.google.com/youtube/answer/{10059070,15424877}. **Pinterest** developers.pinterest.com/docs/{getting-started/connect-app,api/v5/pins,api/v5/boards,api/v5/media,api/v5/oauth-token,reference/rate-limits,getting-started/access-tiers}.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/context/social-connect-3platforms-blueprint-2026-06-27.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(04:03:12)*


## 🤖 Claude *(04:03:25)*

Blueprint consolidado selado em [social-connect-3platforms-blueprint-2026-06-27.md](.claude/context/social-connect-3platforms-blueprint-2026-06-27.md) — as 3 plataformas verificadas em confiança ALTA, com Pattern Conformance + SOPs + correções adversariais.

**O veredito honesto:** "conectar as redes" tem duas metades, e só uma é minha.

- **Minha metade (código):** ~90% da infra já existe. O enum já tem `tiktok/youtube/pinterest`, o `social_accounts` Vault, o OAuth genérico e o **mesmo MP4 9:16** são reuso direto. Net-new = 3 branches OAuth + 3 publishers + fechar o gap do `auto-publish`. Tudo eu construo e provo E2E em **sandbox/privado**.
- **Sua metade (caminho crítico, lead-time de semanas):** OAuth **não existe** sem um app de desenvolvedor registrado em cada plataforma emitindo `client_id`/`secret` — e o **público** só destrava com os audits. Isso é ação sua e deve começar **hoje**:

| Ação sua | Plataforma | Lead-time |
|---|---|---|
| Registrar app + Content Posting Direct Post + add conta sandbox | TikTok | horas–2d |
| Submeter audit Content Posting | TikTok | ~2–6 semanas |
| Criar/converter canal Brand Gabriel AI | YouTube | minutos |
| OAuth consent verification (`youtube.upload`) + In production | YouTube | ~10 dias |
| Submeter API Audit & Quota Extension | YouTube | semanas |
| Business account + Trial | Pinterest | ~1 dia útil |
| Trial→Standard (demo OAuth + ação API) | Pinterest | ~dias |

Os gates A+B do YouTube são **seriais** → prontidão = a soma (~10d + semanas). Por isso submeter no dia 1.

Antes de eu codar, o protocolo exige o **PASSO 0 — emendar o BoK `post-engine`** (ele nomeia tabela errada `social_credentials`, lista plataformas incompleta, não crava scopes/audit). Eu conduzo isso. Três decisões suas guiam o que faço a seguir:

## 🤖 Claude *(04:03:39)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Em que ordem construo os publishers/OAuth? (Posso codar enquanto voc\u00ea registra os apps em paralelo.)",
      "header": "Ordem",
      "multiSelect": false,
      "options": [
        {
          "label": "TikTok 1\u00ba + disparar gates YT j\u00e1",
          "description": "Construo TikTok primeiro (menor atrito a um self-post real em sandbox, prova o transporte mais r\u00e1pido). Em paralelo voc\u00ea submete J\u00c1 os gates A+B do YouTube \u2014 o maior lead-time, serial. Depois YouTube, depois Pinterest."
        },
        {
          "label": "As 3 em paralelo",
          "description": "Construo os 3 branches em sequ\u00eancia r\u00e1pida sem esperar provar um E2E antes do pr\u00f3ximo. Mais c\u00f3digo de uma vez, menos valida\u00e7\u00e3o incremental por plataforma."
        },
        {
          "label": "YouTube primeiro",
          "description": "Come\u00e7o pelo upload resumable (happy-path mais simples: fetch bytes\u2192PUT\u2192201). Mas \u00e9 o caminho cr\u00edtico mais longo (duplo gate) e nasce forced-private at\u00e9 o Audit."
        },
        {
          "label": "Pinterest primeiro",
          "description": "Come\u00e7o pelo video-pin 4-passos. Mais plumbing (cover p\u00fablica obrigat\u00f3ria, board, multipart S3) e sandbox-only at\u00e9 Standard."
        }
      ]
    },
    {
      "question": "Como resolvo as credenciais de app (client_id/secret) das 3 plataformas?",
      "header": "Credenciais",
      "multiSelect": false,
      "options": [
        {
          "label": "env-override + OTD/SLA",
          "description": "Uso secrets de ambiente (TIKTOK_CLIENT_KEY, GOOGLE_CLIENT_ID, PINTEREST_CLIENT_ID, etc.) como default Sovereign-only de onboarding \u2014 o App Tenancy Model permite p/ single-tenant. Registro um OTD+SLA p/ promover a per-user antes do 2\u00ba tenant. Caminho mais r\u00e1pido p/ provar E2E. (Tokens per-user j\u00e1 v\u00e3o p/ social_accounts.)"
        },
        {
          "label": "Tabelas *_config per-user agora",
          "description": "Crio tiktok_config/youtube_config/pinterest_config cifradas (espelho do meta_config) + UI Settings + /security-review ANTES de qualquer publish. Multi-tenant-ready dia 1, mas +3 migrations +3 cards de UI antes do c\u00f3digo de transporte."
        }
      ]
    },
    {
      "question": "Depois da emenda BoK (PASSO 0, obrigat\u00f3ria), o que fa\u00e7o?",
      "header": "Pr\u00f3ximo passo",
      "multiSelect": false,
      "options": [
        {
          "label": "Emendar BoK e j\u00e1 codar a 1\u00aa slice",
          "description": "Conduzo a emenda do post-engine + come\u00e7o a escrever os branches OAuth+publisher contra placeholders de env. Provo E2E assim que voc\u00ea passar as credenciais. Velocidade m\u00e1xima \u2014 c\u00f3digo e seus registros correm em paralelo."
        },
        {
          "label": "S\u00f3 emendar o BoK agora",
          "description": "Selo a documenta\u00e7\u00e3o (emenda post-engine + SOPs em docs/processes) e paro. C\u00f3digo s\u00f3 na pr\u00f3xima sess\u00e3o, depois que voc\u00ea confirmar os apps registrados."
        },
        {
          "label": "Esperar os apps registrados",
          "description": "N\u00e3o escrevo c\u00f3digo nem emendo BoK at\u00e9 voc\u00ea ter os client_id/secret em m\u00e3os. Mais conservador, mas perde a janela de construir em paralelo ao lead-time dos audits."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Em que ordem construo os publishers/OAuth? (Posso codar enquanto você registra os apps em paralelo.)"="As 3 em paralelo", "Como resolvo as credenciais de app (client_id/secret) das 3 plataformas?"="ambos", "Depois da emenda BoK (PASSO 0, obrigatória), o que faço?"="Esperar os apps registrados". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(08:54:52)*


## 🤖 Claude *(08:54:57)*

Decisões registradas:
- **Ordem:** as 3 em paralelo.
- **Credenciais:** **ambos** — tabelas `*_config` per-user (espelho do `meta_config`) **com** fallback de env (resolution-order: per-user primeiro, env como default Sovereign-only). Conformidade total com o API Tenancy Model.
- **Próximo passo:** **esperar os apps registrados** — você quer fazer sua metade primeiro. Então **eu seguro o código E a emenda BoK** até você ter os `client_id`/`secret` em mãos.

Perfeito — isso respeita o caminho crítico real. A coisa de maior valor que te entrego agora é o **playbook exato de registro** dos 3 apps, para você não perder tempo com tentativa-e-erro nos portais. Mas o detalhe que mais quebra OAuth é o **redirect URI** — preciso te dar o exato que o nosso sistema usa. Deixa eu confirmar materialmente como o `social-auth-callback` resolve o callback (Lei 1, não chuto isso).

## 🤖 Claude *(08:55:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== how initiateOAuth builds redirect_uri (useSocialAccounts) ===\"; grep -nE \"redirect_uri|redirectUri|functions/v1/social-auth|social-auth-callback|window.location|VITE_SUPABASE_URL\" src/hooks/useSocialAccounts.ts 2>/dev/null | head -30\necho \"\"; echo \"=== social-auth-init: redirect_uri usage + existing authorize URLs ===\"; grep -nE \"redirect_uri|redirectUri|authorize|https://\" supabase/functions/social-auth-init/index.ts 2>/dev/null | head -40\necho \"\"; echo \"=== social-auth-callback: redirect_uri + token endpoints ===\"; grep -nE \"redirect_uri|redirectUri|oauth|token|https://\" supabase/functions/social-auth-callback/index.ts 2>/dev/null | head -30",
  "description": "Resolve exact OAuth redirect URI pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === how initiateOAuth builds redirect_uri (useSocialAccounts) ===
> 51:      body: { platform, redirect_uri: `${window.location.origin}/social/callback` },
> 79:      window.location.href = data.url;
> 
> === social-auth-init: redirect_uri usage + existing authorize URLs ===
> 1:import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 10:const LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization";
> 11:const INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize";
> 12:const TWITTER_AUTH_URL = "https://twitter.com/i/oauth2/authorize";
> 22:      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 36:      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 43:    const { platform, redirect_uri } = await req.json();
> 45:    if (!platform || !redirect_uri) {
> 46:      return new Response(JSON.stringify({ error: "platform and redirect_uri required" }), {
> 56:    const state = await signState({ userId, platform, redirect_uri, ts: Date.now() }, stateKey);
> 69:      authUrl = `${LINKEDIN_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}`;
> 80:      authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${appId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&response_type=code`;
> 93:      authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;
> 
> === social-auth-callback: redirect_uri + token endpoints ===
> 1:import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2:import { verifyState } from "../_shared/oauth-state.ts";
> 25:  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token",
> 46:    const state = await verifyState<{ userId: string; platform: string; redirect_uri: string }>(
> 53:    const { userId, platform, redirect_uri } = state;
> 73:      const tokenRes = await fetch("https://www.linkedin.com/oauth/v2/accessToken", {
> 79:          redirect_uri: callbackUrl,
> 84:      const tokenData = await tokenRes.json();
> 85:      if (!tokenRes.ok) throw new Error(tokenData.error_description || "LinkedIn token exchange failed");
> 87:      accessToken = tokenData.access_token;
> 88:      refreshToken = tokenData.refresh_token || null;
> 89:      expiresIn = tokenData.expires_in;
> 90:      scopes = (tokenData.scope || "").split(" ");
> 92:      const profileRes = await fetch("https://api.linkedin.com/v2/userinfo", {
> 103:      // Instagram Login — short-lived token
> 104:      const tokenRes = await fetch("https://api.instagram.com/oauth/access_token", {
> 111:          redirect_uri: callbackUrl,
> 115:      const tokenData = await tokenRes.json();
> 116:      if (!tokenRes.ok || tokenData.error_type) throw new Error(tokenData.error_message || "Instagram token exchange failed");
> 118:      const shortToken = tokenData.access_token;
> 119:      platformUserId = String(tokenData.user_id);
> 121:      // Exchange for long-lived token (60 days)
> 123:        `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=${appSecret}&access_token=${shortToken}`
> 126:      accessToken = longData.access_token || shortToken;
> 131:      const meRes = await fetch(`https://graph.instagram.com/v21.0/me?fields=username,name&access_token=${accessToken}`);
> 142:      const tokenRes = await fetch("https://api.x.com/2/oauth2/token", {
> 151:          redirect_uri: callbackUrl,
> 155:      const tokenData = await tokenRes.json();
> 156:      if (!tokenRes.ok) throw new Error(tokenData.error_description || tokenData.detail || "Twitter token exchange failed");
> 158:      accessToken = tokenData.access_token;
> ```

## 🤖 Claude *(08:55:07)*


## 🤖 Claude *(08:55:08)*

Preciso ver exatamente o que é `callbackUrl` (a URL que vai registrada nos portais). Lendo o trecho.

## 🤖 Claude *(08:55:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
  "offset": 50,
  "limit": 55
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 50	    }
> 51	
> 52	    const callbackUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/social-auth-callback`;
> 53	    // Signed state (HMAC-SHA256, SB_SECRET_KEY) — the callback has no user JWT, so the signature is the only proof
> 54	    // that THIS userId actually initiated the connect (closes cross-tenant account-linking). `ts` bounds replay.
> 55	    const stateKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 56	    const state = await signState({ userId, platform, redirect_uri, ts: Date.now() }, stateKey);
> 57	
> 58	    let authUrl: string;
> 59	
> 60	    if (platform === "linkedin") {
> 61	      const clientId = Deno.env.get("LINKEDIN_CLIENT_ID");
> 62	      if (!clientId) {
> 63	        return new Response(JSON.stringify({ error: "LinkedIn not configured" }), {
> 64	          status: 500,
> 65	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 66	        });
> 67	      }
> 68	      const scopes = "openid profile email w_member_social";
> 69	      authUrl = `${LINKEDIN_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}`;
> 70	
> 71	    } else if (platform === "instagram" || platform === "facebook") {
> 72	      const appId = Deno.env.get("INSTAGRAM_APP_ID");
> 73	      if (!appId) {
> 74	        return new Response(JSON.stringify({ error: "Instagram/Facebook not configured" }), {
> 75	          status: 500,
> 76	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 77	        });
> 78	      }
> 79	      const scopes = "instagram_business_basic,instagram_business_content_publish,instagram_business_manage_comments,instagram_business_manage_messages";
> 80	      authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${appId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&response_type=code`;
> 81	
> 82	    } else if (platform === "twitter") {
> 83	      const clientId = Deno.env.get("TWITTER_CLIENT_ID");
> 84	      if (!clientId) {
> 85	        return new Response(JSON.stringify({ error: "Twitter/X not configured" }), {
> 86	          status: 500,
> 87	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 88	        });
> 89	      }
> 90	      // Twitter OAuth 2.0 with PKCE
> 91	      const codeChallenge = state.slice(0, 43); // simple challenge for demo; production should use S256
> 92	      const scopes = "tweet.read tweet.write users.read offline.access";
> 93	      authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;
> 94	
> 95	    } else {
> 96	      return new Response(JSON.stringify({ error: `Platform ${platform} not yet supported for OAuth` }), {
> 97	        status: 400,
> 98	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 99	      });
> 100	    }
> 101	
> 102	    return new Response(JSON.stringify({ url: authUrl }), {
> 103	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 104	    });
> ```

## 🤖 Claude *(08:55:46)*


## 🤖 Claude *(08:55:50)*

Confirmado materialmente (Lei 1) — o **redirect URI** que vai registrado nos 3 portais é a URL da edge function de callback, não a rota do frontend:

```
https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback
```

(`social-auth-init:52` → `callbackUrl = ${SUPABASE_URL}/functions/v1/social-auth-callback`; o `/social/callback` do frontend é só o retorno interno pós-upsert.)

Vou escrever o playbook de registro persistente e atualizar o estado do projeto na memória — depois te entrego o resumo acionável. Lendo a memória da virada brand-persona para emendar (em vez de duplicar).

## 🤖 Claude *(08:55:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_brand_persona_ccio.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: project_brand_persona_ccio
> 3	description: Construção de marca (NÃO virada) — Gabriel AI = cópia digital real do CEO Gabriel (mascote/influencer da MCORCH, modelo Magalu/Magazine Luiza), rosto+voz de todos os canais. Afiliado = subproduto de longo prazo (receita via pauta consciente). Multi-canal YT+TikTok+LinkedIn+IG. Loop de aprendizado depende de painel analítico por publicação.
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: 3ee740c7-9900-4d37-a9a4-207b63e460bb
> 8	---
> 9	
> 10	**Diretiva Sovereign 2026-06-26** (depois de provar o LinkedIn E2E e remover a conexão p/ recriar com avatar próprio): o foco do conteúdo **NÃO são os produtos** — afiliado é consequência de longo prazo. O foco é **evangelizar o MCORCH** com uma voz única e escalável: o **Gabriel AI / CCIO (Cofounder Chief Intelligence Office)** — primeira versão 100% digital do Sovereign (Gabriel Caldeira Rocha avatar) — como **rosto + voz** de TODOS os canais junto da marca. Os perfis (LinkedIn novo, YouTube→MCORCH, Instagram `@magicorch`, TikTok novo) são bocas do mesmo organismo, mesma identidade visual + avatar unificado. A persona é o **átomo de distribuição escalável**: hoje 1 (CCIO)→N canais; amanhã N personas (cada depto da Pantheon com seu avatar).
> 11	
> 12	**Reframe técnico (a beleza):** os trilhos NÃO mudam (gerar→render 9:16→agendar→publicar→atribuir). Muda só (a) a *fonte do tema* (produto → pilar de marca/missão; "sempre falar da mesma coisa" = pilares fixos, ângulos variáveis — vira spine de persona no prompt, troca o `topic:produto`) e (b) o *nº de bocas* (+YouTube +TikTok). Reusa o motor [[project_viral_autopilot]] inteiro.
> 13	
> 14	**Ações já tomadas nesta sessão:** plano de produto do User 0 (`640b3b67`) **pausado** (`is_active=false`, reversível) — conteúdo Roborock não bate mais com a marca + LinkedIn foi desconectado (restam só `instagram`+`facebook` ativos).
> 15	
> 16	**Prep YouTube+TikTok (workflow `wf_24e9eb67`, fundamentado Lei 1) → blueprint `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`:**
> 17	- **Infra ~90% pronta.** Enum `social_platform` JÁ tem `youtube`+`tiktok` (zero migration). `social_accounts` Vault já cifra tokens. `scheduled_posts`/`auto-publish`/`autopilot` já fazem cadência. OAuth connect é genérico (`social-auth-init`+`social-auth-callback`, state HMAC). **O MP4 9:16 do IG Reel = MESMO asset YT Shorts+TikTok** (motor HyperFrames `video-bridge`).
> 18	- **Net-new = 3 pares de branches** (publish-social / social-auth-init+callback / refresh-social-token) + **1 gap** (`auto-publish:54-83` só passa texto, não `content.video_url` — caminho cron-de-vídeo não fechado; Reel foi invoke direto) + add `youtube`/`tiktok` ao `VIDEO_FLOW_PLATFORMS` (autopilot-run:109).
> 19	- **Portões de aprovação = ação Sovereign, semanas (igual IG App Review):** YouTube = verificação OAuth + **Audit do projeto API** (senão `videos.insert` nasce `private` mesmo pedindo public — projetos pós-2020-07-28). TikTok = **app audit** (senão SELF_ONLY + conta privada + ≤5 users/24h). Estratégia: **construir + validar em privado/sandbox AGORA, público destrava na aprovação.**
> 20	- **Gate MCORCH Closed-Loop:** amendar BoK `post-engine` via `/bok-scribe` ANTES de codar (ele cita TikTok/Shorts mas nomeia tabela errada `social_credentials`→viva é `social_accounts`, e não crava scopes/audit/branch design).
> 21	
> 22	**✅ Gabriel AI face-consistency PROVADO + nó mood-board SHIPPED (2026-06-26):** projeto Canvas `b57a59f7` "Gabriel AI" do User 0. **Demo E2E (commit nenhum — geração):** 2 fotos do rosto do Sovereign (nós characterReference) → `canvas-execute` Nano Banana (`google/gemini-2.5-flash-image`) com `reference_image_urls` → retrato Gabriel AI face-consistente real (asset `c42d0336`, 10 mco, identidade visual MCORCH azul/violeta). **Verdade técnica:** o motor de consistência facial JÁ existia — `canvas-execute` threada **até 4** reference images como `image_url` parts multimodais pro Gemini (`slice(0,4)`); `findUpstreamImages` coleta os upstream. **Nó mood-board (commit `549e4dd`):** `characterReference.imageUrls[]` (até 6 fotos/nó; antes 1 só `imageUrl`) + `pickNodeImages`/`findUpstreamImages` emitem TODAS → flui por **GenerateImage/StyleTransfer/Run-All** (inspectors usam `findUpstreamImages`). Node grid 2×2 + badge 📸; inspector upload múltiplo + remover. Back-compat: legados (`imageUrl` único) intactos (`imageUrl=imageUrls[0]`). **Fronteiras (Lei 1):** (a) `sceneCompose` usa 2 handles explícitos (`input_image_1/2`, 1 foto/handle via `pickNodeImage` singular) — NÃO coleta o mood board; p/ face-consistency usar **GenerateImage**. (b) **Soul Character (`soulId`) NÃO está implementado** — só campos no tipo + botão disabled "Phase 4.5"; o caminho real é reference-threading. (c) uploads do inspector usam signed URL 7 dias (`createSignedUrl`) → referências quebram após 1 semana (considerar bucket público/re-assinar p/ persona permanente). Verificado em browser real (preview+sessão injetada): nó "mood board facial" + inspector "MOOD BOARD FACIAL (1/6)". tsc 0.
> 23	
> 24	**Correção/aprofundamento Sovereign 2026-06-26 (tarde):** Gabriel AI **NÃO é uma virada** — é a **marca sendo construída**. Como a Magalu (Magazine Luiza) ou influencers/mascotes reais, Gabriel AI é a **cópia digital real do co-founder & CEO** (o próprio Gabriel) — melhor que um perfil de marca corporativo. Persona durável; não chamar de "pivot/virada".
> 25	
> 26	**Causa raiz do "não avançamos apesar do dev incrível" (diagnóstico material `wob2d279d`, Lei 1):** o **placar está em branco**. `creative_metrics` (12 linhas): revenue>0: **0** · impressions>0: **0** · engagements>0: **0** · affiliate_clicks>0: **1** (~10 cliques agregados em `affiliate_links`, único nervo vivo). O motor de **Learning & Adaptation** (único padrão FRACO da doutrina, OTD-AG-002) aprende sobre nada: loop está fechado mas é **"termostato de 1-bit"** — reward=`totalClicks` mono-métrica Goodhart (`autopilot-analyze:90`); só sussurra hint textual no prompt, **não realoca esforço** via `ab_variants` (parada); lê só 1 ciclo atrás; 2 bugs latentes (filtro `scope` ausente `orchestrate-step:203`; `applied` nunca vira true). **Desbloqueio = nervo sensorial de volta:** Sovereign quer **um PAINEL ANALÍTICO POR PUBLICAÇÃO** (views/likes/comentários/shares/reposts/remixes de cada post real LinkedIn/IG que já existe) → alimenta o **reward multi-métrica marca-primeiro** `R = 0.40·z(reach) + 0.30·z(eng/impr) + 0.20·z(brand_signal) + 0.10·z(revenue)` (z-score+taxa = anti-Goodhart; sem clickbait; receita via **pauta de decisão** consciente, não otimização cega). **Força total nas 2 fatias** (loop honesto + captura de desfecho), via emenda BoK `viral-autopilot` (dogfooding do Pattern Conformance Gate). Precedente do vetor ponderado: OpenClaw Dreaming.
> 27	
> 28	Relacionado: [[project_creative_ecosystem_program]] · [[project_viral_autopilot]] · [[reference_ig_reels_publish_path]] · [[feedback_api_tenancy_per_user]] · [[project_creative_layer_validation]] · [[feedback_deliver_user_value_not_plumbing]].
> 29	
> ```

## 🤖 Claude *(08:55:54)*


## 🤖 Claude *(08:56:10)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_brand_persona_ccio.md",
  "old_string": "Relacionado: [[project_creative_ecosystem_program]] \u00b7 [[project_viral_autopilot]] \u00b7 [[reference_ig_reels_publish_path]] \u00b7 [[feedback_api_tenancy_per_user]] \u00b7 [[project_creative_layer_validation]] \u00b7 [[feedback_deliver_user_value_not_plumbing]].",
  "new_string": "**Conectar redes \u2014 TikTok+YouTube+Pinterest (2026-06-27, workflow `wf_b5a35451-7dc` 8 agentes, 3 plataformas verificadas HIGH):** blueprint consolidado `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md` (supersede o prep de 06-26; **acrescenta Pinterest** \u2014 pe\u00e7a nova antes n\u00e3o pesquisada \u2014 + Pattern Conformance 21-rows + SOPs Lei 2). **Enum j\u00e1 tem `pinterest` tamb\u00e9m** (zero migration). **Decis\u00f5es Sovereign:** (1) construir as **3 em paralelo**; (2) credenciais de app = **AMBOS** (tabelas `tiktok_config`/`youtube_config`/`pinterest_config` per-user espelho do `meta_config` cifrado + INSTEAD OF tenant-guard, **COM** fallback de env como default Sovereign-only \u2014 resolution-order per-user\u2192env); (3) **HOLD** \u2014 n\u00e3o escrever c\u00f3digo NEM emendar BoK at\u00e9 o Sovereign registrar os 3 apps e ter `client_id`/`secret` em m\u00e3os. **Redirect URI a registrar nos 3 portais (Lei 1, `social-auth-init:52`):** `https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback`. **Scopes:** TikTok `video.publish,user.info.basic` (v\u00edrgula!) \u00b7 YouTube `youtube.upload` (offline+consent) \u00b7 Pinterest `boards:read,boards:write,pins:read,pins:write,user_accounts:read`. **Transfer de m\u00eddia:** TikTok FILE_UPLOAD (signed URL n\u00e3o passa PULL_FROM_URL) \u00b7 YouTube resumable PUT \u00b7 Pinterest register\u2192multipart(file last)\u2192poll\u2192create+cover p\u00fablica. **Caminho cr\u00edtico = a\u00e7\u00e3o Sovereign** (sem app n\u00e3o h\u00e1 OAuth): registrar 3 apps + 3 audits (TikTok ~2-6sem \u00b7 YouTube gate A OAuth-verify ~10d + gate B API-Audit semanas SERIAL \u00b7 Pinterest Trial~1d\u2192Standard). Playbook de registro: `.claude/context/social-app-registration-playbook-2026-06-27.md`. **Ao retomar:** PASSO 0 emenda BoK `post-engine` \u2192 slices 2-4 (publishers+OAuth env creds) \u2192 slice 5 (VIDEO_FLOW_PLATFORMS + gap auto-publish video_url) \u2192 slice 6 (spine CCIO).\n\nRelacionado: [[project_creative_ecosystem_program]] \u00b7 [[project_viral_autopilot]] \u00b7 [[reference_ig_reels_publish_path]] \u00b7 [[feedback_api_tenancy_per_user]] \u00b7 [[project_creative_layer_validation]] \u00b7 [[feedback_deliver_user_value_not_plumbing]]."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_brand_persona_ccio.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(08:56:13)*


## 🤖 Claude *(08:56:14)*

Agora o playbook de registro persistente — operator-facing, com os valores exatos verificados.

## 🤖 Claude *(08:56:52)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/social-app-registration-playbook-2026-06-27.md",
  "content": "# Playbook de Registro de Apps \u2014 TikTok \u00b7 YouTube \u00b7 Pinterest (a\u00e7\u00e3o Sovereign)\n\n> **Data:** 2026-06-27 \u00b7 **Operator:** Sovereign (Gabriel) \u00b7 **Por qu\u00ea:** sem o app de dev registrado n\u00e3o h\u00e1 `client_id`/`secret` \u2192 nenhum OAuth come\u00e7a. Este \u00e9 o **caminho cr\u00edtico** (lead-time de semanas nos audits). Companheiro do blueprint `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md`.\n> **Fundamenta\u00e7\u00e3o:** workflow `wf_b5a35451-7dc` (3 plataformas verificadas em confian\u00e7a ALTA contra docs oficiais).\n\n## \ud83d\udd11 Valor que \u00e9 IGUAL nos 3 portais\n\n**Redirect URI / Callback** (registrar EXATO \u2014 diverg\u00eancia mata o OAuth; verificado em `social-auth-init:52`):\n```\nhttps://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback\n```\n- HTTPS, est\u00e1tico, sem query/fragment. (TikTok exige \u2264512 chars; Pinterest exige match exato, sem wildcard.)\n- Conta a conectar = a conta da **marca Gabriel AI / CCIO** em cada rede.\n\n**O que trazer de volta** (6 valores) para destravar o c\u00f3digo:\n\n| Plataforma | Trazer |\n|---|---|\n| TikTok | `client_key` + `client_secret` |\n| YouTube/Google | `client_id` + `client_secret` (+ confirmar canal Brand criado) |\n| Pinterest | `app_id` (client_id) + `client_secret` |\n\n---\n\n## 1. TikTok \u2014 developers.tiktok.com\n\n**Objetivo:** Content Posting API com **Direct Post** (publica\u00e7\u00e3o aut\u00f4noma server-side).\n\n1. Login em **developers.tiktok.com** \u2192 **Manage apps** \u2192 **Connect an app** (precisa de conta TikTok + aceitar ToS).\n2. Em **Add products**, adicionar:\n   - **Login Kit** (OAuth).\n   - **Content Posting API** \u2192 habilitar **Direct Post** (N\u00c3O s\u00f3 \"Upload\" \u2014 upload-to-inbox exige humano finalizar no app).\n3. **Scopes:** `video.publish` + `user.info.basic`. (No nosso c\u00f3digo v\u00e3o separados por **v\u00edrgula**.)\n4. **Redirect URI:** colar o callback acima em **Configuration \u2192 Redirect URI**.\n5. **Sandbox / Target users:** adicionar a conta TikTok da persona como **target user** (sandbox) \u2014 antes do audit, s\u00f3 usu\u00e1rios allowlistados conseguem autorizar.\n6. Copiar **Client key** + **Client secret**.\n7. **\u23f3 AUDIT (destrava o p\u00fablico \u2014 ~2-6 semanas, sem SLA):** submeter o **Content Posting API audit** (formul\u00e1rio de usage-estimates + um screencast/walkthrough da UX compliant). **Sem o audit:** todo Direct Post \u00e9 **SELF_ONLY** (s\u00f3 o criador v\u00ea) + a conta precisa estar **privada** no post + \u22645 users/24h. **Submeter j\u00e1** \u2014 \u00e9 o gargalo. Estimar volume di\u00e1rio com folga (o cap de 24h vem do que voc\u00ea declarar).\n\n---\n\n## 2. YouTube \u2014 Google Cloud Console + YouTube Studio\n\n**Objetivo:** Data API v3 `videos.insert` (Shorts = formato vertical). **Tem DOIS gates seriais** \u2014 submeter ambos no dia 1.\n\n1. **Canal Brand:** garantir que a conta **Gabriel AI / CCIO** tem um canal no YouTube (criar/converter para Brand Account se preciso). \u00c9 o alvo do upload.\n2. **Google Cloud Console** (console.cloud.google.com) \u2192 criar/selecionar um projeto \u2192 **APIs & Services \u2192 Library** \u2192 habilitar **YouTube Data API v3**.\n3. **Credentials \u2192 Create Credentials \u2192 OAuth client ID** \u2192 tipo **Web application** \u2192 em **Authorized redirect URIs** colar o callback acima. Copiar **Client ID** + **Client secret**.\n4. **OAuth consent screen** (User type **External**):\n   - Adicionar o scope sens\u00edvel **`.../auth/youtube.upload`**.\n   - Adicionar test users (a conta da marca) para testar j\u00e1.\n   - **\u23f3 GATE A \u2014 Submit for verification** + setar publishing status para **In production**. **~10 dias.** Sem isso o app fica em *Testing*: warning vermelho + **refresh token expira em 7 dias** (mata o autopilot di\u00e1rio).\n5. **\u23f3 GATE B \u2014 YouTube API Services Audit & Quota Extension Form** (link na doc `quota_and_compliance_audits`). **Semanas, sem SLA.** Sem isso, projetos de API n\u00e3o-verificados (criados p\u00f3s-28/07/2020) t\u00eam **todo upload FOR\u00c7ADO a `private`** mesmo pedindo `public`.\n   - **Gates A e B s\u00e3o independentes e seriais \u2192 prontid\u00e3o para p\u00fablico = a SOMA (~10d + semanas).** Por isso submeter os dois agora.\n\n---\n\n## 3. Pinterest \u2014 developers.pinterest.com\n\n**Objetivo:** API v5 para criar **video pins** aut\u00f4nomos.\n\n1. Ter uma **conta Pinterest Business** (converter pessoal se preciso) + verificar email + aceitar **Developer Terms**.\n2. **developers.pinterest.com \u2192 My apps \u2192 Create app** (precisa de uma **URL de pol\u00edtica de privacidade** + descri\u00e7\u00e3o completa do app).\n3. **Configure \u2192 Redirect URIs:** colar o callback acima (match exato, sem wildcard).\n4. **Scopes:** `boards:read`, `boards:write`, `pins:read`, `pins:write`, `user_accounts:read`. **Pedir o set COMPLETO de cara** \u2014 adicionar scope depois for\u00e7a re-autoriza\u00e7\u00e3o total.\n5. App nasce em **Trial access** \u2014 copiar **App ID** (client_id) + **App secret**.\n6. **\u23f3 Trial\u2192Standard (destrava o p\u00fablico \u2014 sem SLA, ~dias):** submeter o **upgrade para Standard** com um **v\u00eddeo demo** mostrando o **fluxo OAuth** E uma **a\u00e7\u00e3o de API v5 ao vivo**. **Sob Trial** pins/boards s\u00e3o **sandbox/creator-only** (ningu\u00e9m v\u00ea) + rate baixo (300/dia). Standard libera p\u00fablico + rate por-minuto.\n\n---\n\n## \u2705 Quando voc\u00ea voltar com as credenciais\n\nEu retomo na ordem (decis\u00f5es j\u00e1 cravadas: **3 em paralelo**, credenciais **per-user `*_config` cifrado + fallback env**):\n\n1. **PASSO 0** \u2014 emendar o BoK `post-engine` (`/bok-scribe`) + escrever os SOPs Lei 2 (gate obrigat\u00f3rio antes de c\u00f3digo).\n2. **Migrations** `tiktok_config`/`youtube_config`/`pinterest_config` (espelho `meta_config`, cifrado, INSTEAD OF tenant-guard) + `/security-review`.\n3. **Branches** OAuth (`social-auth-init`/`-callback`/`refresh-social-token`) + **publishers** (`publish-social`) das 3.\n4. **Slice 5** \u2014 `VIDEO_FLOW_PLATFORMS` + fechar o gap `auto-publish` (resolver+assinar `video_url` 9:16) \u2192 fecha o cron-de-v\u00eddeo de TODAS (incl. IG Reel agendado).\n5. Provar E2E em **sandbox/privado** (TikTok SELF_ONLY \u00b7 YT private \u00b7 Pinterest Trial) \u2014 o p\u00fablico acende quando os audits passarem.\n\nOs secrets de env (caminho mais r\u00e1pido enquanto as tabelas n\u00e3o t\u00eam UI) ser\u00e3o: `TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET` \u00b7 `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` \u00b7 `PINTEREST_CLIENT_ID`/`PINTEREST_CLIENT_SECRET` (via `npx supabase secrets set`).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/context/social-app-registration-playbook-2026-06-27.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(08:56:58)*


## 🤖 Claude *(08:57:13)*

Tudo pronto para você executar sua metade. **Estou em HOLD** conforme você decidiu — não escrevo código nem emendo o BoK até você voltar com os `client_id`/`secret`.

## O que ficou selado nesta sessão (documentação, fundamentada Lei 1)

- **Blueprint consolidado** das 3 plataformas → [social-connect-3platforms-blueprint-2026-06-27.md](.claude/context/social-connect-3platforms-blueprint-2026-06-27.md) (change-list file:line, Pattern Conformance 21-rows, SOPs, correções adversariais).
- **Playbook de registro** (sua ação) → [social-app-registration-playbook-2026-06-27.md](.claude/context/social-app-registration-playbook-2026-06-27.md).
- Estado do projeto gravado na memória.

## Sua jogada agora — registrar os 3 apps

Em **todos** os portais, o **Redirect URI** é o mesmo (colar exato):
```
https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback
```

| Plataforma | Onde | Habilitar / Scopes | Audit (destrava público) |
|---|---|---|---|
| **TikTok** | developers.tiktok.com | Login Kit + **Content Posting API → Direct Post** · `video.publish,user.info.basic` · add conta como **sandbox target user** | Content Posting audit — **~2–6 sem** |
| **YouTube** | Google Cloud Console | YouTube Data API v3 + OAuth client Web · scope `youtube.upload` · criar/converter canal Brand | **Gate A** OAuth-verify ~10d **+ Gate B** API Audit (semanas) — **seriais, somar** |
| **Pinterest** | developers.pinterest.com | Business account + privacy-policy URL · `boards:read,write` `pins:read,write` `user_accounts:read` | Trial→**Standard** (demo OAuth+API) — sem SLA |

**Submeta os audits no mesmo dia que registrar** — eles são o gargalo de semanas e correm em paralelo enquanto eu codo (quando você der o sinal). O do YouTube é o mais longo (dois gates seriais).

## Quando você voltar com os 6 valores

Retomo nesta ordem (decisões cravadas: **3 em paralelo**; credenciais **per-user `*_config` cifrado + fallback env**):
1. PASSO 0 — emenda BoK `post-engine` + SOPs Lei 2.
2. Migrations `*_config` cifradas + `/security-review`.
3. Branches OAuth + publishers das 3 → provar E2E em **sandbox/privado**.
4. Slice 5 — `VIDEO_FLOW_PLATFORMS` + fechar o gap do `auto-publish` (fecha o cron-de-vídeo de todas, incl. IG Reel agendado).

Os 4 arquivos novos (2 blueprints/playbook + memória) estão no working tree, **não commitados** — é sua chamada se quer que eu commite agora ou só quando o código pousar. Me dá o sinal quando os apps estiverem de pé. 🚀

## 👤 User *(15:26:56)*

ótimo continue faça na order que precisar e se quiser usar força total delegue a outros agents com força total

## 🤖 Claude *(15:29:03)*


## 🤖 Claude *(15:29:11)*

O **GO de força total** sobrescreve o HOLD anterior — você quer que eu construa agora, na ordem que o protocolo exige. Vou ser transparente sobre a materialidade (Lei 1): sem os apps registrados eu **construo + verifico estaticamente** (tsc, security-review, deploy fail-closed), mas o **E2E real de OAuth/publish só prova quando você trouxer as credenciais** — e o público, com os audits. Nada disso me impede de deixar tudo code-complete e revisado agora.

Ordem do protocolo: **PASSO 0 (gate BoK) → migrations → branches OAuth+publishers → cadência/auto-publish → UI → verify.** Nada de código pode nascer antes do gate. Disparo o PASSO 0 com força total e, em paralelo, faço o scout dos templates que vou precisar para a fase de código.

Uma decisão de engenharia que tomo já (melhora o blueprint): em vez de 3 tabelas `*_config` quase idênticas, uma única **`social_app_config(user_id, platform UNIQUE, client_id, client_secret[Vault], scopes, metadata)`** — DRY, espelha o padrão do `affiliate_config`, uma migration só.

## 🤖 Claude *(15:29:12)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Social connect: build",
  "summary": "Implementar TikTok/YouTube/Pinterest \u2014 PASSO 0 (BoK gate) \u2192 migrations \u2192 OAuth+publishers \u2192 cad\u00eancia \u2192 UI"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Social connect: build". Continue your current work.'}]
> ```

## 🤖 Claude *(15:29:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== docs/bok/post-engine/ ===\"; ls -1 docs/bok/post-engine/\necho \"\"; echo \"=== existing credential-resolution SOPs (templates) ===\"; ls -1 docs/processes/ | grep -iE \"credential|meta|affiliate|social\"\necho \"\"; echo \"=== meta_config migration (encryption/INSTEAD OF template) ===\"; ls -1 supabase/migrations/ | grep -iE \"meta_api|credential_encryption|vault_upsert|instead_of|affiliate_config|meta_social\"",
  "description": "Scout BoK + SOP + migration templates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === docs/bok/post-engine/ ===
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> 
> === existing credential-resolution SOPs (templates) ===
> affiliate-catalog-enrichment.md
> affiliate-credential-resolution.md
> branded-affiliate-redirect.md
> credential-disconnect-clear.md
> meta-credential-resolution.md
> meta-reels-publish.md
> ml-affiliate-attribution.md
> trends-credential-resolution.md
> vision-mcp-billing-credential-resolution.md
> 
> === meta_config migration (encryption/INSTEAD OF template) ===
> 20260530210000_meta_api_foundation.sql
> 20260601000000_credential_encryption.sql
> 20260601000500_fix_meta_config_instead_of_trigger.sql
> 20260602130000_fix_user_api_keys_instead_of_double_fire.sql
> 20260602140000_vault_upsert_secret_idempotent_encrypt.sql
> 20260602150000_meta_social_instead_of_tenant_guard.sql
> 20260602160000_meta_social_disconnect_rpc.sql
> ```

## 🤖 Claude *(15:29:38)*


## 🤖 Claude *(15:29:41)*

PASSO 0 com força total — 4 agentes em paralelo (amendment do BoK `post-engine` + 3 SOPs Lei 2), todos em arquivos distintos (zero conflito). Disparando e, em paralelo, leio os templates de migration que vou usar para autorar o `social_app_config` eu mesmo (caminho security-crítico).

## 🤖 Claude *(15:30:21)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'social-passo0-bok-sops',\n  description: 'PASSO 0 (BoK gate): amend post-engine BoK + author 3 Law-2 SOPs for TikTok/YouTube/Pinterest connect',\n  phases: [\n    { title: 'BoK Amendment', detail: 'reconcile drift + Pattern Conformance + branch-design amendment to docs/bok/post-engine' },\n    { title: 'SOPs', detail: 'Law-2 credential-resolution + publish SOP per platform (parallel, distinct files)' },\n  ],\n}\n\nconst DOC_RESULT = {\n  type: 'object',\n  required: ['filesWritten', 'keyPoints'],\n  properties: {\n    filesWritten: { type: 'array', items: { type: 'object', required: ['path', 'summary'], properties: { path: {type:'string'}, summary: {type:'string'} } } },\n    keyPoints: { type: 'array', items: {type:'string'} },\n    openIssues: { type: 'array', items: {type:'string'} },\n  },\n}\n\nconst REPO = '/home/gcrUX/htdocs/constellation-orchestra'\nconst BLUEPRINT = `${REPO}/.claude/context/social-connect-3platforms-blueprint-2026-06-27.md`\n\nconst SCHEMA_DECISION = `SCHEMA DECISION (authoritative, overrides the blueprint's \"mirror meta_config / 3 tables\" suggestion): a SINGLE per-user table \\`social_app_config\\` keyed UNIQUE(user_id, platform), columns: id uuid PK, user_id uuid FK auth.users, platform social_platform, client_id text, client_secret text (Vault-encrypted + column-level REVOKE, mirroring meta_config.long_lived_token), scopes text[], metadata jsonb (holds youtube channel_id / pinterest board_id), is_active boolean default true, created_at/updated_at. RLS default-deny + auth.uid()=user_id; masked VIEW + INSTEAD OF tenant-guard trigger like meta_config/social_accounts. Credential RESOLUTION ORDER (API Tenancy Model): (1) social_app_config per-user (is_active) \u2192 (2) env fallback (TIKTOK_CLIENT_KEY/SECRET, GOOGLE_CLIENT_ID/SECRET, PINTEREST_CLIENT_ID/SECRET) as Sovereign-only onboarding default \u2192 (3) hard fail HTTP 402/501 {error:\"<platform>_not_configured\", action:\"Configure ... at /dashboard/settings\"}. NEVER a silent shared key.`\n\nphase('BoK Amendment')\n\nconst BOK_PROMPT = `You are amending the MCORCH \\`post-engine\\` BoK suite to be the Source of Truth for connecting TikTok + YouTube + Pinterest publishers/OAuth. This is PASSO 0 of the MCORCH Closed-Loop Protocol \u2014 production-ready, NO placeholders.\n\nREAD FIRST (ground everything; cite real content):\n- ${BLUEPRINT}  (the consolidated, adversarially-verified blueprint \u2014 your Source of Truth for scopes/audit-gates/branch-design/Pattern-Conformance)\n- ${REPO}/docs/bok/post-engine/00-index.md, 05-sdd.md, 06-data-model.md  (the existing suite you are amending)\n- ${REPO}/docs/architecture/agentic-vision.md  (the 21 agentic patterns \u2014 for the Pattern Conformance Declaration)\n- ${REPO}/docs/bok/agentic-governance/09-pattern-conformance.md  (the master template to mirror for the declaration format)\n\n${SCHEMA_DECISION}\n\nDO (targeted, additive \u2014 Read each file before Edit; do not mangle existing content):\n1. EDIT \\`docs/bok/post-engine/06-data-model.md\\`: (a) reconcile the obsolete table name \\`social_credentials\\` \u2192 the LIVE \\`social_accounts\\` (Vault-masked VIEW over \\`social_accounts_table\\`, encrypted access_token/refresh_token via the 20260601000000 trigger pattern); (b) correct the platform list to the full live enum \\`linkedin|instagram|facebook|twitter|tiktok|youtube|pinterest|wordpress\\`; (c) ADD the \\`social_app_config\\` table definition per the SCHEMA DECISION above (columns, RLS, encryption, INSTEAD OF tenant-guard, resolution order).\n2. CREATE \\`docs/bok/post-engine/09-pattern-conformance.md\\`: the Pattern Conformance Declaration for this social-connect amendment \u2014 one row per pattern from agentic-vision.md (table: Pattern | Implemented (yes/deferred/n-a) | How / Why-deferred), using the 21 rows already in the blueprint \u00a74. Mirror the agentic-governance template's format + a short header tying it to the AGI\u2192ASI doctrine.\n3. CREATE \\`docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md\\`: the authoritative branch-design amendment. For EACH platform document: OAuth init (authorize URL + exact scopes + redirect_uri \\`https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback\\` + offline/consent or PKCE specifics), OAuth callback (token endpoint, response fields, social_accounts upsert), refresh (rotating-token semantics \u2014 re-store new refresh_token atomically), publish flow (the exact step sequence from blueprint \u00a72 \u2014 TikTok creator_info\u2192init(FILE_UPLOAD,is_aigc)\u2192PUT chunks\u2192status; YouTube resumable initiate\u2192PUT\u2192201\u2192verify privacyStatus; Pinterest board\u2192register\u2192multipart(file last)\u2192poll\u2192pin+public cover), token lifetimes, audit gates (\u00a73/\u00a76), and new FR ids (assign FR-PE-0xx numbers continuing from the existing FRD \u2014 read 04-frd.md to find the next free id range; list them). Reference the blueprint + the official source URLs (Lei 1).\n4. EDIT \\`docs/bok/post-engine/00-index.md\\`: add 09 + 10 to the index with one-line descriptions.\n\nReturn the structured result (filesWritten with paths + summaries, keyPoints, openIssues).`\n\nconst sopFor = (platform, label) => `You are authoring a Law-2 (Anticipated Process) SOP for connecting + publishing to ${label} in MCORCH. Production-ready, NO placeholders, in the project's bilingual style (PT-BR prose for operator-facing, English for code identifiers).\n\nREAD FIRST:\n- ${BLUEPRINT}  (sections \u00a72/\u00a73/\u00a75/\u00a76 cover ${label} \u2014 your Source of Truth)\n- ${REPO}/docs/processes/meta-credential-resolution.md  (the SOP TEMPLATE to mirror \u2014 structure, headings, the API-Tenancy resolution-order section, the telemetry section)\n\n${SCHEMA_DECISION}\n\nWRITE \\`${REPO}/docs/processes/${platform}-publish-credential-resolution.md\\` covering, in the meta-credential-resolution.md style:\n- Header (Operator/Reviewer/Owner = ORO; Law-2 statement).\n- API Tenancy resolution order for ${label} app credentials (social_app_config per-user \u2192 env fallback \u2192 fail-closed 402/501) with the exact column/env names.\n- The publish SOP table (Law 2): Operator | Sequence (numbered steps, EACH with a MATERIAL success criterion \u2014 a real artifact: a social_accounts UUID, an HTTP status, a publish_id/video id/pin id, an infra_health_logs row) | Verification gates | Recovery path (exact, per failure mode from \u00a75) | Success signal (the Lei-1 materiality gate: ${platform==='tiktok'?'PUBLISH_COMPLETE pre-audit SELF_ONLY, public tiktok.com URL post-audit':platform==='youtube'?'201 then videos.get privacyStatus==public (NOT a bare 201)':'201 pin id pre-Standard sandbox, public pinterest.com/pin URL post-Standard'}).\n- The audit/app-registration gate (Sovereign action, lead time) from \u00a76.\n- A telemetry section: infra_health_logs service='publish-${platform}' on success/degraded/error paths.\n- A \"media transfer\" note: ${platform==='tiktok'?'FILE_UPLOAD chunked (Supabase signed URL fails PULL_FROM_URL domain ownership)':platform==='youtube'?'resumable PUT (fetch signed bytes; no remote ingest)':'register\u2192multipart upload (params verbatim, file field LAST) \u2192 poll \u2192 create pin with PUBLIC cover_image_url'}.\nReturn the structured result (filesWritten, keyPoints, openIssues).`\n\nconst results = await parallel([\n  () => agent(BOK_PROMPT, { label: 'bok:post-engine', phase: 'BoK Amendment', schema: DOC_RESULT, agentType: 'general-purpose' }),\n  () => agent(sopFor('tiktok', 'TikTok'), { label: 'sop:tiktok', phase: 'SOPs', schema: DOC_RESULT, agentType: 'general-purpose' }),\n  () => agent(sopFor('youtube', 'YouTube'), { label: 'sop:youtube', phase: 'SOPs', schema: DOC_RESULT, agentType: 'general-purpose' }),\n  () => agent(sopFor('pinterest', 'Pinterest'), { label: 'sop:pinterest', phase: 'SOPs', schema: DOC_RESULT, agentType: 'general-purpose' }),\n])\n\nreturn { results }\n",
  "description": "PASSO 0 BoK amendment + 3 SOPs"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wquz7w639
> Summary: PASSO 0 (BoK gate): amend post-engine BoK + author 3 Law-2 SOPs for TikTok/YouTube/Pinterest connect
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/subagents/workflows/wf_9259d39b-c4c
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-passo0-bok-sops-wf_9259d39b-c4c.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-passo0-bok-sops-wf_9259d39b-c4c.js"} to iterate without resending the script.)
> Run ID: wf_9259d39b-c4c
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-passo0-bok-sops-wf_9259d39b-c4c.js", resumeFromRunId: "wf_9259d39b-c4c"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(15:30:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260530210000_meta_api_foundation.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: meta-api foundation — meta_config + meta_posts (Passo 1: publish-meta)
> 2	-- BoK SSOT: docs/bok/meta-api/06-data-model.md (§1.1, §1.2, §2, §3.1)
> 3	-- SOP: docs/processes/meta-credential-resolution.md (Lei 2 — written before this migration)
> 4	-- API Tenancy Model: per-user credentials, RLS-isolated, column-grant on tokens.
> 5	--
> 6	-- SECURITY NOTE (OTD-META-ENCRYPT): Meta OAuth tokens are stored as TEXT plaintext
> 7	-- protected by RLS + column-level REVOKE (Sovereign directive 2026-05-30: consistent with
> 8	-- social_accounts.access_token / user_api_keys, which already store same-class tokens plaintext).
> 9	-- NFR-META-001 (AES-256-GCM / pgsodium at-rest) is tracked project-wide as OTD-META-ENCRYPT;
> 10	-- encrypting only meta_config while social_accounts stays plaintext would be security theater.
> 11	-- whatsapp_leads + meta_ads_metrics are deferred to their own migrations (Passo 2 / Passo 3).
> 12	
> 13	-- ─────────────────────────────────────────────────────────────────────────────
> 14	-- Shared updated_at trigger function (idempotent — may already exist)
> 15	-- ─────────────────────────────────────────────────────────────────────────────
> 16	CREATE OR REPLACE FUNCTION public.update_updated_at_column()
> 17	RETURNS TRIGGER AS $$
> 18	BEGIN
> 19	    NEW.updated_at = now();
> 20	    RETURN NEW;
> 21	END;
> 22	$$ LANGUAGE plpgsql;
> 23	
> 24	-- ─────────────────────────────────────────────────────────────────────────────
> 25	-- 1. meta_config — per-user Meta credentials & linked accounts (UNIQUE per user)
> 26	-- ─────────────────────────────────────────────────────────────────────────────
> 27	CREATE TABLE IF NOT EXISTS public.meta_config (
> 28	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 29	    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 30	    facebook_user_id TEXT,                                  -- populated by OAuth flow; nullable for BYOK
> 31	    long_lived_token TEXT NOT NULL,                         -- 60-day Meta user token (plaintext+RLS; see OTD-META-ENCRYPT)
> 32	    scopes TEXT[] NOT NULL DEFAULT '{}',
> 33	    pages JSONB NOT NULL DEFAULT '[]'::jsonb,               -- [{ page_id, name, access_token }] — token-bearing, REVOKE'd below
> 34	    instagram_business_account_id TEXT,
> 35	    whatsapp_phone_number_id TEXT,
> 36	    whatsapp_waba_id TEXT,
> 37	    meta_ad_account_id TEXT,
> 38	    requires_reauth BOOLEAN NOT NULL DEFAULT FALSE,
> 39	    token_expires_at TIMESTAMPTZ,
> 40	    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
> 41	    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
> 42	    CONSTRAINT unique_user_meta UNIQUE (user_id)
> 43	);
> 44	
> 45	ALTER TABLE public.meta_config ENABLE ROW LEVEL SECURITY;
> 46	
> 47	-- Default-deny: only the owner tenant can touch their row.
> 48	CREATE POLICY "Users manage their own Meta config" ON public.meta_config
> 49	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 50	
> 51	CREATE TRIGGER tr_update_meta_config_updated_at
> 52	    BEFORE UPDATE ON public.meta_config
> 53	    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 54	
> 55	-- Column-level hardening: token columns are WRITE-ONLY for clients (BYOK paste via INSERT/UPDATE),
> 56	-- never returned via PostgREST. service_role (edge functions) bypasses grants to read for publishing.
> 57	-- Clients must select explicit safe columns (useMetaConfig); `select=*` will be denied by design.
> 58	REVOKE SELECT (long_lived_token, pages) ON public.meta_config FROM anon, authenticated;
> 59	
> 60	-- ─────────────────────────────────────────────────────────────────────────────
> 61	-- 2. meta_posts — publication history (links + status per published post)
> 62	-- ─────────────────────────────────────────────────────────────────────────────
> 63	CREATE TABLE IF NOT EXISTS public.meta_posts (
> 64	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 65	    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 66	    campaign_id UUID,
> 67	    platform TEXT NOT NULL,                                 -- 'instagram' | 'facebook'
> 68	    meta_post_id TEXT NOT NULL,                             -- id returned by Meta Graph API
> 69	    post_url TEXT,
> 70	    caption TEXT,
> 71	    media_url TEXT,
> 72	    status TEXT NOT NULL DEFAULT 'published',               -- 'published' | 'failed'
> 73	    error_message TEXT,
> 74	    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
> 75	);
> 76	
> 77	ALTER TABLE public.meta_posts ENABLE ROW LEVEL SECURITY;
> 78	
> 79	CREATE POLICY "Users manage their own Meta posts" ON public.meta_posts
> 80	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 81	
> 82	CREATE INDEX IF NOT EXISTS idx_meta_posts_user ON public.meta_posts (user_id);
> 83	CREATE INDEX IF NOT EXISTS idx_meta_posts_campaign ON public.meta_posts (campaign_id);
> 84	CREATE INDEX IF NOT EXISTS idx_meta_posts_created ON public.meta_posts (created_at DESC);
> 85	
> ```

## 🤖 Claude *(15:31:02)*


## 🤖 Claude *(15:31:13)*

PASSO 0 rodando em background (`wf_9259d39b-c4c` — amendment BoK + 3 SOPs, 4 agentes paralelos). Acompanhe com `/workflows`; sigo automaticamente quando fechar.

Um achado material do template que ajusta a migration (Lei 1): o `meta_config` original guardava o token como **TEXT plaintext + RLS + REVOKE** de coluna, e só **depois** a migration `20260601000000_credential_encryption.sql` o envolveu em **Vault** (renomeou `meta_config`→`meta_config_table` + VIEW mascarada + trigger de cifra + view `decrypted_*` service-role). O `social_accounts` também é Vault hoje. Então o `social_app_config` vai seguir o **padrão canônico atual (Vault-masked VIEW)** para o `client_secret` — não o plaintext legado. Vou espelhar exatamente `20260601000000` + `20260602140000` (vault_upsert idempotente) + `20260602150000` (INSTEAD OF tenant-guard) quando autorar a migration.

Sequência travada, com força total via agentes:
1. **PASSO 0** (rodando) — gate BoK + SOPs → eu reviso (materialidade).
2. **Migration** `social_app_config` Vault-cifrada → aplico + `/security-review`.
3. **Branches** OAuth (init/callback/refresh) + **publishers** das 3 (paralelo por arquivo, sem conflito) + helper de resolução fail-closed.
4. **Cadência** (`VIDEO_FLOW_PLATFORMS`) + gap do `auto-publish` (video_url).
5. **UI** (cards das 3 + card de credenciais espelho do `MetaConfigCard`).
6. **Verify** — tsc + deploy provando o caminho fail-closed + review adversarial de segurança.

Tudo isso fica **code-complete e revisado** agora; o E2E real de OAuth/publish acende quando você trouxer os `client_id/secret`, e o público quando os audits passarem. Volto assim que o PASSO 0 fechar.

## 👤 User *(15:38:46)*

<task-notification>
<task-id>wquz7w639</task-id>
<tool-use-id>toolu_01KaMdf7xz9LY1tqQ26KJSJW</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wquz7w639.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "PASSO 0 (BoK gate): amend post-engine BoK + author 3 Law-2 SOPs for TikTok/YouTube/Pinterest connect" completed</summary>
<result>{"results":[{"filesWritten":[{"path":"/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/06-data-model.md","summary":"EDITED (v0.1→v0.2, reconciled 2026-06-27). Replaced the obsolete placeholder table social_credentials with the LIVE social_accounts (Vault-masked VIEW over social_accounts_table; access_token/refresh_token encrypted by trigger trg_encrypt_social_accounts in migration 20260601000000; INSTEAD OF tenant-guard in 20260602150000). Corrected the platform list to the full live enum social_platform (linkedin|instagram|facebook|twitter|tiktok|youtube|pinterest|wordpress, migration 20260402014040:12) and added a §2.0 enum subsection. Added the new social_app_config table per the authoritative SCHEMA DECISION: single per-user table UNIQUE(user_id,platform), client_secret Vault-encrypted + column-level REVOKE (mirroring meta_config.long_lived_token), masked VIEW, INSTEAD OF tenant-guard, full RLS, and the 3-step credential resolution order (per-user→env fallback→hard fail 402/501). Updated the Tenant Isolation Map to the 3-layer enforcement (RLS + INSTEAD OF guard + Vault)."},{"path":"/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/09-pattern-conformance.md","summary":"CREATED. Pattern Conformance Declaration for the social-connect amendment, mirroring the agentic-governance/09 master-template format. Header ties it to the AGI→ASI Via-4/Via-3 doctrine. All 21 canonical patterns from agentic-vision.md §2 declared (yes/deferred/n-a) using the blueprint §4 rows, each non-n-a line citing an FR-PE/FR-VA/OTD: yes×10 (Chaining, Routing, Tool Use, Memory, Goal Monitoring, Exception Recovery, HITL, Resource-Aware, Guardrails, Evaluation), deferred×4 (Parallelization/Reflection→OTD-AG-003, Learning→OTD-AG-002, Prioritization→OTD-AG-008/020), n-a×7. Includes a verification gate table."},{"path":"/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md","summary":"CREATED. Authoritative branch-design amendment / Source of Truth. Per platform (TikTok/YouTube/Pinterest): OAuth init (authorize URL + exact comma/space scopes + redirect_uri https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback + offline/consent/PKCE specifics), OAuth callback (token endpoint, response fields, social_accounts upsert), rotating-refresh semantics (atomic re-store), and the exact publish step sequences (TikTok creator_info→init(FILE_UPLOAD,is_aigc)→PUT chunks→status/fetch; YouTube resumable initiate→Location→PUT(308-resume)→201→verify privacyStatus; Pinterest board cache→/v5/media register→multipart(file last,204)→poll succeeded→/v5/pins+public cover). Token-lifetime/audit-gate table (§3), credential resolution order + OTD-PE-SOCIAL-APPCREDS deferral (§4), 12 new FRs FR-PE-005..016 (§5), Sovereign critical-path actions (§6), official source URLs (§7, Lei 1), and Lei-2 SOP skeletons per platform (§8)."},{"path":"/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/00-index.md","summary":"EDITED. Added a 'Suite Documents (índice)' table listing the core docs plus the new 09 (Pattern Conformance) and 10 (branch-design amendment) with one-line descriptions, and noting the 06 reconciliation. Updated the Version footer to record the social-connect v1.0 amendment (2026-06-27)."}],"keyPoints":["PASSO 0 of the MCORCH Closed-Loop Protocol is complete: the post-engine BoK is now the Source of Truth for connecting TikTok+YouTube+Pinterest, with NO placeholders — every external claim is anchored to the adversarially-verified blueprint or an official doc URL (Lei 1).","Schema reconciliation is grounded in the LIVE schema, verified against migrations before editing: social_platform enum already contains tiktok|youtube|pinterest (20260402014040:12) → ZERO enum migration; social_accounts is the real Vault-masked VIEW (encryption trigger 20260601000000:55-90, masked '••••••••••••', INSTEAD OF tenant-guard 20260602150000). The placeholder social_credentials never existed in production.","The authoritative SCHEMA DECISION was applied verbatim: a SINGLE social_app_config table keyed UNIQUE(user_id,platform) with Vault-encrypted client_secret + column-level REVOKE (mirroring meta_config.long_lived_token), masked VIEW, INSTEAD OF tenant-guard, default-deny RLS, and the API-Tenancy resolution order (per-user is_active → env fallback as Sovereign-only onboarding default → hard fail 402/501 {error:'&lt;platform&gt;_not_configured'}), overriding the blueprint's 3-tables suggestion.","Next free FR id was confirmed as FR-PE-005 (FRD v0.1 uses FR-PE-001..004); the amendment assigns FR-PE-005..016 (app-creds table, 3 OAuth-init branches, callback, rotating refresh, video cadence, AIGC disclosure, 3 publish branches, materiality/telemetry/mesh-node) — all 12 ids verified present.","Pattern Conformance Declaration carries all 21 canonical patterns (verified count = 21) with honest yes/deferred/n-a and FR/OTD citations, mirroring the agentic-governance master-template format and tied to the AGI→ASI Via-4 doctrine.","Material proof: ls -la shows all 4 files on disk (06=11171B, 09=12159B, 10=25136B, 00=4245B); social_credentials now appears only in the 3 explicit reconciliation callouts, not as a live table."],"openIssues":["The HARD blockers remain 100% outside code and are Sovereign-gated with weeks of lead-time (documented in amendment §6): register 3 dev apps + add TikTok sandbox user + create/convert the YouTube Brand channel + submit 3 audits (TikTok Content Posting ~2-6wk; YouTube OAuth verification ~10d AND API Audit serial+independent; Pinterest Trial→Standard). YouTube gates A+B are serial → total readiness = SUM, so both must be submitted day 1.","OTD-PE-SOCIAL-APPCREDS is registered in the amendment (env-creds fallback for the probe slices, SLA = before the 2nd tenant). It must be promoted to a per-user is_active path + Settings UI before onboarding any second tenant, or it becomes silent shared-credential debt.","No code has been written (this is documentation/PASSO 0 only). Any future migration creating social_app_config / social_app_config_table MUST pass /security-review before commit (FMEA-011), and the per-platform SOPs in amendment §8 should be promoted to docs/processes/social-connect-&lt;platform&gt;.md (Lei 2) when the code lands.","The auto-publish video_url transport gap (no video_url column in scheduled_posts; media_url never resolved/signed) is documented and folded into FR-PE-011 with the recommended dispatch-time signed-URL fix, but remains an open implementation item that also affects the existing scheduled IG Reel path."]},{"filesWritten":[{"path":"/home/gcrUX/htdocs/constellation-orchestra/docs/processes/tiktok-publish-credential-resolution.md","summary":"Law-2 (Anticipated Process) SOP for connecting + publishing to TikTok in MCORCH. 219 lines, 22673 bytes. Mirrors the meta-credential-resolution.md template structure (header with ORO + Law-2 statement, Context, Resolution order, Sequence tables, Verification gates, Recovery path, Success signal, Anti-patterns, Known debt, Connection to Survival Laws). Adds TikTok-specific sections: dual-plane credential model (app creds vs user tokens), the authoritative single social_app_config table schema, two Sequence tables (OAuth connect + Publish, each step with a material success criterion), per-failure-mode Recovery (from blueprint §5.1), the audit/app-registration Sovereign gate (§6, ~2-6 week lead time), a telemetry section (infra_health_logs service='publish-tiktok' on healthy/degraded/error), and a FILE_UPLOAD chunked media-transfer note."}],"keyPoints":["SCHEMA DECISION applied as authoritative: single per-user social_app_config table keyed UNIQUE(user_id, platform) with columns id/user_id/platform/client_id/client_secret(Vault+REVOKE)/scopes[]/metadata(jsonb)/is_active/timestamps — explicitly supersedes the blueprint's 'tiktok_config/youtube_config/pinterest_config' suggestion (§2.1 footer, §7 #1). RLS default-deny 
... (truncated 13112 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wquz7w639.output)</result>
<usage><agent_count>4</agent_count><subagent_tokens>411040</subagent_tokens><tool_uses>37</tool_uses><duration_ms>504695</duration_ms></usage>
</task-notification>

## 🤖 Claude *(15:38:52)*


## 🤖 Claude *(15:38:54)*

PASSO 0 reportou completo. Antes de tratar o gate como vencido, **verifico materialmente** (Lei 1 — não confio no auto-report do agente). Checando os 7 arquivos no disco + conteúdo real.

## 🤖 Claude *(15:39:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== git status (what changed) ===\"; git status --short\necho \"\"; echo \"=== new BoK files ===\"; ls -la docs/bok/post-engine/09-pattern-conformance.md docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md 2>&1\necho \"\"; echo \"=== 3 SOPs on disk ===\"; ls -la docs/processes/tiktok-publish-credential-resolution.md docs/processes/youtube-publish-credential-resolution.md docs/processes/pinterest-publish-credential-resolution.md 2>&1\necho \"\"; echo \"=== Pattern Conformance row count (expect 21 pattern rows) ===\"; grep -cE \"^\\| (Prompt Chaining|Routing|Parallelization|Reflection|Tool Use|Planning|Multi-Agent|Memory|Learning|Model Context|Goal|Exception|Human-in|Knowledge Retrieval|Inter-Agent|Resource|Reasoning|Guardrail|Evaluation|Prioritization|Exploration)\" docs/bok/post-engine/09-pattern-conformance.md\necho \"\"; echo \"=== FR-PE-005..016 present in amendment? ===\"; grep -oE \"FR-PE-0(0[5-9]|1[0-6])\" docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md | sort -u | tr '\\n' ' '; echo\necho \"\"; echo \"=== placeholder smell-check (TODO/TBD/lorem/XXX) across the 7 files ===\"; grep -rIEl \"TODO|TBD|lorem|XXXX|PLACEHOLDER|<placeholder>\" docs/bok/post-engine/{06-data-model,09-pattern-conformance,10-amendment-social-connect-tiktok-youtube-pinterest}.md docs/processes/{tiktok,youtube,pinterest}-publish-credential-resolution.md 2>/dev/null || echo \"no placeholders \u2705\"\necho \"\"; echo \"=== social_credentials drift gone? (expect only reconciliation callouts) ===\"; grep -rc \"social_credentials\" docs/bok/post-engine/06-data-model.md",
  "description": "Materially verify PASSO 0 outputs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git status (what changed) ===
>  M docs/bok/post-engine/00-index.md
>  M docs/bok/post-engine/06-data-model.md
> ?? .claude/context/social-app-registration-playbook-2026-06-27.md
> ?? .claude/context/social-connect-3platforms-blueprint-2026-06-27.md
> ?? docs/bok/post-engine/09-pattern-conformance.md
> ?? docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md
> ?? docs/processes/pinterest-publish-credential-resolution.md
> ?? docs/processes/tiktok-publish-credential-resolution.md
> ?? docs/processes/youtube-publish-credential-resolution.md
> 
> === new BoK files ===
> -rw-rw-r-- 1 ubuntu ubuntu 12159 Jun 27 12:33 docs/bok/post-engine/09-pattern-conformance.md
> -rw-rw-r-- 1 ubuntu ubuntu 25136 Jun 27 12:35 docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md
> 
> === 3 SOPs on disk ===
> -rw-rw-r-- 1 ubuntu ubuntu 23868 Jun 27 12:38 docs/processes/pinterest-publish-credential-resolution.md
> -rw-rw-r-- 1 ubuntu ubuntu 22673 Jun 27 12:32 docs/processes/tiktok-publish-credential-resolution.md
> -rw-rw-r-- 1 ubuntu ubuntu 23099 Jun 27 12:35 docs/processes/youtube-publish-credential-resolution.md
> 
> === Pattern Conformance row count (expect 21 pattern rows) ===
> 0
> 
> === FR-PE-005..016 present in amendment? ===
> FR-PE-005 FR-PE-006 FR-PE-007 FR-PE-008 FR-PE-009 FR-PE-010 FR-PE-011 FR-PE-012 FR-PE-013 FR-PE-014 FR-PE-015 FR-PE-016 
> 
> === placeholder smell-check (TODO/TBD/lorem/XXX) across the 7 files ===
> docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md
> docs/processes/pinterest-publish-credential-resolution.md
> 
> === social_credentials drift gone? (expect only reconciliation callouts) ===
> docs/bok/post-engine/06-data-model.md:3
> ```

## 🤖 Claude *(15:39:10)*


## 🤖 Claude *(15:39:12)*

Quase tudo verde, mas dois pontos pedem confirmação: o grep de Pattern Conformance deu 0 (provável regex meu, não ausência) e o smell-check de placeholder marcou 2 arquivos (provável falso-positivo da própria palavra "placeholder" na nota de reconciliação). Confirmando os dois.

## 🤖 Claude *(15:39:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== actual placeholder matches (context) ===\"\ngrep -nIE \"TODO|TBD|lorem|XXXX|PLACEHOLDER|<placeholder>\" docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md docs/processes/pinterest-publish-credential-resolution.md\necho \"\"\necho \"=== Pattern Conformance: show the table header + count yes/deferred/n-a status cells ===\"\ngrep -nE \"yes|deferred|n-a|n/a\" docs/bok/post-engine/09-pattern-conformance.md | grep -E \"^\\s*[0-9]+:\\|\" | wc -l\necho \"--- distinct pattern names found in the doc ---\"\ngrep -oE \"Prompt Chaining|Routing|Parallelization|Reflection|Tool Use|Planning|Multi-Agent|Multi-agent|Memory Management|Learning & Adaptation|Model Context Protocol|Goal Setting|Exception Handling|Human-in-the-Loop|Knowledge Retrieval|Inter-Agent|Resource-Aware|Reasoning Techniques|Guardrails|Evaluation & Monitoring|Prioritization|Exploration\" docs/bok/post-engine/09-pattern-conformance.md | sort -u | wc -l\necho \"--- the table rows (first column) ---\"\ngrep -E \"^\\|\" docs/bok/post-engine/09-pattern-conformance.md | grep -ivE \"Pattern|---|:--\" | sed -E 's/\\|([^|]*)\\|.*/\\1/' | head -25",
  "description": "Confirm pattern table + placeholder context"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === actual placeholder matches (context) ===
> docs/processes/pinterest-publish-credential-resolution.md:97:- **(2) upload (multipart):** `POST` o MP4 no `upload_url` como **`multipart/form-data`**, **SEM header `Authorization`**, com TODOS os `upload_parameters` **VERBATIM** (não mutar nenhum valor) e o **campo `file` por ÚLTIMO** — é uma presigned-POST do S3, onde a ordem dos campos e os valores são parte da assinatura; ordem errada ou param mutado → **403**. Sucesso = **`204`** (sem body).
> docs/processes/pinterest-publish-credential-resolution.md:167:| **Multipart 403** (passo 2) | `POST upload_url` retorna 403 | Reconstruir o form: TODOS os `upload_parameters` **VERBATIM** (sem mutar) + campo **`file` por ÚLTIMO** + **SEM** header `Authorization`. 403 = ordem/param violou a assinatura do presigned-POST. |
> docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md:104:2. **upload**: `POST` o MP4 no `upload_url` como `multipart/form-data` com TODOS os `upload_parameters` **VERBATIM** e o **campo `file` por ÚLTIMO** (ordenação de presigned-POST S3; ordem errada/param mutado → 403), **SEM Bearer**, sucesso = `204`.
> 
> === Pattern Conformance: show the table header + count yes/deferred/n-a status cells ===
> 24
> --- distinct pattern names found in the doc ---
> 21
> --- the table rows (first column) ---
>  Campo 
>  **Módulo** 
>  **Lineage** 
>  **ORO** 
>  1 
>  2 
>  3 
>  4 
>  5 
>  6 
>  7 
>  8 
>  9 
>  10 
>  11 
>  12 
>  13 
>  14 
>  15 
>  16 
>  17 
>  18 
>  19 
>  20 
>  21
> ```

## 🤖 Claude *(15:39:48)*


## 🤖 Claude *(15:39:51)*

Confirmado — gate **legitimamente vencido** (Lei 1):
- 7 arquivos reais no disco (sizes 12–25KB).
- Pattern Conformance: **21 padrões** distintos, linhas numeradas 1–21 ✅.
- **FR-PE-005..016** (12 FRs) presentes ✅.
- "Placeholder" foi **falso-positivo** — as 3 linhas marcadas são conteúdo real sobre upload multipart (`upload_parameters` VERBATIM, `file` por último). Sem placeholder real.
- Drift `social_credentials` = só os 3 callouts de reconciliação ✅.

Um último spot-check de fidelidade no doc 10 (a SSOT que dirige o código) — confirmar que endpoints/scopes não driftaram do blueprint verificado.

## 🤖 Claude *(15:39:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== critical endpoints/scopes in doc 10 (fidelity to verified blueprint) ===\"\ngrep -oE \"open.tiktokapis.com/v2/oauth/token|creator_info/query|/v2/post/publish/video/init/|FILE_UPLOAD|video.publish,user.info.basic|accounts.google.com/o/oauth2/v2/auth|youtube.upload|access_type=offline|uploadType=resumable|api.pinterest.com/v5/oauth/token|/v5/media|/v5/pins|boards:read,boards:write,pins:read,pins:write|cover_image_url|is_aigc|containsSyntheticMedia|privacyStatus\" docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md | sort | uniq -c | sort -rn",
  "description": "Confirm endpoint/scope fidelity in amendment doc"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === critical endpoints/scopes in doc 10 (fidelity to verified blueprint) ===
>       7 privacyStatus
>       6 /v5/pins
>       5 /v5/media
>       5 FILE_UPLOAD
>       3 youtube.upload
>       3 is_aigc
>       3 cover_image_url
>       2 video.publish,user.info.basic
>       2 creator_info/query
>       2 containsSyntheticMedia
>       2 api.pinterest.com/v5/oauth/token
>       2 accounts.google.com/o/oauth2/v2/auth
>       2 access_type=offline
>       1 /v2/post/publish/video/init/
>       1 uploadType=resumable
>       1 open.tiktokapis.com/v2/oauth/token
>       1 boards:read,boards:write,pins:read,pins:write
> ```

## 🤖 Claude *(15:40:58)*


## 🤖 Claude *(15:41:01)*

Fidelidade confirmada — todos os endpoints/scopes batem com o blueprint verificado. **Gate BoK vencido materialmente.** Avanço para o código.

Começo pela peça mais security-crítica: a migration `social_app_config` (Vault-masked). Vou **autorá-la eu mesmo** — o risco aqui é vazamento cross-tenant de credencial, então leio os templates exatos antes. Lendo o padrão de cifra/INSTEAD OF/Vault helper.

## 🤖 Claude *(15:41:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== latest migration timestamp (avoid collision) ===\"; ls -1 supabase/migrations/ | tail -3\necho \"\"; echo \"=== structure of 20260601000000_credential_encryption.sql (section headers + key DDL) ===\"\ngrep -nE \"^-- \u2501|^-- \u2500|CREATE TABLE|RENAME TO|CREATE OR REPLACE VIEW|CREATE VIEW|CREATE TRIGGER|CREATE OR REPLACE FUNCTION|INSTEAD OF|REVOKE|GRANT|vault_upsert|decrypted_|ENABLE ROW LEVEL|CREATE POLICY|meta_config|social_accounts|user_api_keys\" supabase/migrations/20260601000000_credential_encryption.sql | head -90",
  "description": "Map credential_encryption migration structure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === latest migration timestamp (avoid collision) ===
> 20260625120000_creative_assets_registry.sql
> 20260626120000_collective_efficiency_ledger.sql
> 20260626130000_publication_metrics.sql
> 
> === structure of 20260601000000_credential_encryption.sql (section headers + key DDL) ===
> 5:-- ─────────────────────────────────────────────────────────────────────────────
> 7:-- ─────────────────────────────────────────────────────────────────────────────
> 9:ALTER TABLE IF EXISTS public.meta_config RENAME TO meta_config_table;
> 10:ALTER TABLE IF EXISTS public.social_accounts RENAME TO social_accounts_table;
> 11:ALTER TABLE IF EXISTS public.user_api_keys RENAME TO user_api_keys_table;
> 13:-- ─────────────────────────────────────────────────────────────────────────────
> 15:-- ─────────────────────────────────────────────────────────────────────────────
> 17:-- 2.1 meta_config_table encryption trigger
> 18:CREATE OR REPLACE FUNCTION public.trg_encrypt_meta_config()
> 32:      v_token_id := vault.create_secret(NEW.long_lived_token, 'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token');
> 41:      v_pages_id := vault.create_secret(NEW.pages::text, 'meta_config_pages_' || NEW.id::text, 'Meta config pages list');
> 50:CREATE OR REPLACE TRIGGER tr_encrypt_meta_config
> 51:  BEFORE INSERT OR UPDATE ON public.meta_config_table
> 52:  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_meta_config();
> 55:-- 2.2 social_accounts_table encryption trigger
> 56:CREATE OR REPLACE FUNCTION public.trg_encrypt_social_accounts()
> 70:      v_access_token_id := vault.create_secret(NEW.access_token, 'social_accounts_access_token_' || NEW.id::text, 'Social account access token');
> 79:      v_refresh_token_id := vault.create_secret(NEW.refresh_token, 'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token');
> 88:CREATE OR REPLACE TRIGGER tr_encrypt_social_accounts
> 89:  BEFORE INSERT OR UPDATE ON public.social_accounts_table
> 90:  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_social_accounts();
> 93:-- 2.3 user_api_keys_table encryption trigger
> 94:CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> 104:      v_id := vault.create_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key');
> 114:      v_id := vault.create_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> 124:      v_id := vault.create_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key');
> 134:      v_id := vault.create_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key');
> 144:      v_id := vault.create_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');
> 154:      v_id := vault.create_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key');
> 164:      v_id := vault.create_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key');
> 174:      v_id := vault.create_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password');
> 184:      v_id := vault.create_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key');
> 194:      v_id := vault.create_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key');
> 204:      v_id := vault.create_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret');
> 213:CREATE OR REPLACE TRIGGER tr_encrypt_user_api_keys
> 214:  BEFORE INSERT OR UPDATE ON public.user_api_keys_table
> 215:  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_user_api_keys();
> 218:-- ─────────────────────────────────────────────────────────────────────────────
> 220:-- ─────────────────────────────────────────────────────────────────────────────
> 222:-- 3.1 Backfill meta_config_table
> 229:  FOR r IN SELECT * FROM public.meta_config_table LOOP
> 234:      v_token_id := vault.create_secret(r.long_lived_token, 'meta_config_long_lived_token_' || r.id::text, 'Meta config long-lived token');
> 238:      v_pages_id := vault.create_secret(r.pages::text, 'meta_config_pages_' || r.id::text, 'Meta config pages list');
> 242:      UPDATE public.meta_config_table
> 252:-- 3.2 Backfill social_accounts_table
> 259:  FOR r IN SELECT * FROM public.social_accounts_table LOOP
> 264:      v_access_id := vault.create_secret(r.access_token, 'social_accounts_access_token_' || r.id::text, 'Social account access token');
> 268:      v_refresh_id := vault.create_secret(r.refresh_token, 'social_accounts_refresh_token_' || r.id::text, 'Social account refresh token');
> 272:      UPDATE public.social_accounts_table
> 282:-- 3.3 Backfill user_api_keys_table
> 288:  FOR r IN SELECT * FROM public.user_api_keys_table LOOP
> 292:      v_groq := vault.create_secret(r.groq_api_key, 'user_api_keys_groq_api_key_' || r.user_id::text, 'Groq API Key');
> 295:      v_or := vault.create_secret(r.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || r.user_id::text, 'OpenRouter API Key');
> 298:      v_oa := vault.create_secret(r.openai_api_key, 'user_api_keys_openai_api_key_' || r.user_id::text, 'OpenAI API Key');
> 301:      v_el := vault.create_secret(r.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || r.user_id::text, 'ElevenLabs API Key');
> 304:      v_gg := vault.create_secret(r.google_api_key, 'user_api_keys_google_api_key_' || r.user_id::text, 'Google API Key');
> 307:      v_nb := vault.create_secret(r.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || r.user_id::text, 'Nanobana API Key');
> 310:      v_sd := vault.create_secret(r.seedance_api_key, 'user_api_keys_seedance_api_key_' || r.user_id::text, 'Seedance API Key');
> 313:      v_wp := vault.create_secret(r.wp_app_password, 'user_api_keys_wp_app_password_' || r.user_id::text, 'WordPress App Password');
> 316:      v_rep := vault.create_secret(r.replicate_api_key, 'user_api_keys_replicate_api_key_' || r.user_id::text, 'Replicate API Key');
> 319:      v_hf := vault.create_secret(r.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || r.user_id::text, 'Higgsfield API Key');
> 322:      v_hfs := vault.create_secret(r.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || r.user_id::text, 'Higgsfield API Key Secret');
> 326:      UPDATE public.user_api_keys_table
> 345:-- ─────────────────────────────────────────────────────────────────────────────
> 347:-- ─────────────────────────────────────────────────────────────────────────────
> 349:-- 4.1 meta_config public view
> 350:CREATE OR REPLACE VIEW public.meta_config WITH (security_invoker = true) AS
> 366:FROM public.meta_config_table;
> 368:-- 4.2 social_accounts public view
> 369:CREATE OR REPLACE VIEW public.social_accounts WITH (security_invoker = true) AS
> 384:FROM public.social_accounts_table;
> 386:-- 4.3 user_api_keys public view
> 387:CREATE OR REPLACE VIEW public.user_api_keys WITH (security_invoker = true) AS
> 409:FROM public.user_api_keys_table;
> 412:-- ─────────────────────────────────────────────────────────────────────────────
> 413:-- 5. INSTEAD OF TRIGGERS: Map view updates/inserts back to base tables
> 414:-- ─────────────────────────────────────────────────────────────────────────────
> 416:-- 5.1 Instead of trigger for meta_config
> 417:CREATE OR REPLACE FUNCTION public.trg_instead_of_meta_config()
> 421:    DELETE FROM public.meta_config_table WHERE id = OLD.id;
> 424:    INSERT INTO public.meta_config_table (
> 431:    UPDATE public.meta_config_table SET
> 434:      long_lived_token = COALESCE(NULLIF(NEW.long_lived_token, '••••••••••••'), public.meta_config_table.long_lived_token),
> 436:      pages = COALESCE(NULLIF(NEW.pages, to_jsonb('••••••••••••'::text)), public.meta_config_table.pages),
> 451:CREATE TRIGGER trg_instead_of_meta_config
> 452:  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.meta_config
> 453:  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_meta_config();
> 456:-- 5.2 Instead of trigger for social_accounts
> 457:CREATE OR REPLACE FUNCTION public.trg_instead_of_social_accounts()
> 461:    DELETE FROM public.social_accounts_table WHERE id = OLD.id;
> ```

## 🤖 Claude *(15:41:33)*


## 🤖 Claude *(15:41:36)*

O padrão é intricado mas claro. Para autorar com segurança (e revisar competentemente), leio as 3 peças canônicas: o helper idempotente `vault_upsert_secret` (20260602140000), o tratamento completo do `social_accounts` (INSTEAD OF + decrypted view + REVOKE + RLS) e o tenant-guard (20260602150000).

## 🤖 Claude *(15:41:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: idempotent credential encryption — vault_upsert_secret() eliminates the
> 2	--            re-save unique_violation (23505) across all three Vault-backed credential tables.
> 3	-- ─────────────────────────────────────────────────────────────────────────────
> 4	-- Bug (latent debt flagged 2026-06-02 in docs/processes/credential-disconnect-clear.md, and
> 5	-- reproduced materially the same day): the BEFORE INSERT/UPDATE encryption triggers
> 6	-- (trg_encrypt_user_api_keys, trg_encrypt_meta_config, trg_encrypt_social_accounts) call
> 7	-- vault.create_secret(value, '<deterministic-name>') UNCONDITIONALLY whenever a secret column
> 8	-- changes value. vault.create_secret does a plain `INSERT INTO vault.secrets` with NO ON CONFLICT,
> 9	-- and vault.secrets.name carries a UNIQUE index (secrets_name_idx). So rotating a stored secret to
> 10	-- a NEW value while the same-named secret still exists throws:
> 11	--     ERROR 23505 duplicate key value violates unique constraint "secrets_name_idx"
> 12	-- User-facing manifestation: WordPress "Editar → save a new app-password WITHOUT disconnecting
> 13	-- first" (src/pages/SocialAccountsPage.tsx). Sibling tables share the shape (names keyed by row id),
> 14	-- so re-saving a Meta long-lived token / pages list, or a social access/refresh token, on an
> 15	-- existing row collides identically.
> 16	--
> 17	-- Already fixed separately (NOT this migration): the INSTEAD OF double-fire of the encrypt trigger
> 18	-- (20260602130000_fix_user_api_keys_instead_of_double_fire.sql, UPDATE-first). connect → disconnect
> 19	-- → reconnect already works because disconnect_wordpress() deletes the secret first. The case left
> 20	-- open was strictly "rotate the value in place without deleting first".
> 21	--
> 22	-- Fix: a single idempotent helper public.vault_upsert_secret(value, name, desc) that resolves an
> 23	-- existing secret BY NAME (vault.secrets.name is unique) and rotates it in place via
> 24	-- vault.update_secret (which COALESCE-keeps name + description, re-encrypting only the value), else
> 25	-- creates it. The vault.create_secret call-sites in each of the three encryption triggers are
> 26	-- swapped for this helper, preserving the existing "already a UUID reference → keep" guard and the
> 27	-- "only when the value actually changed" (IS DISTINCT FROM) guard. The stored column keeps pointing
> 28	-- at the SAME Vault UUID across rotations (update-in-place), so decrypted_* views transparently
> 29	-- reflect the new value and no orphan secrets accumulate.
> 30	--
> 31	-- Security posture (this migration HARDENS; per CLAUDE.md every migration passes /security-review):
> 32	--   * vault_upsert_secret is SECURITY DEFINER with `SET search_path = ''` and every object schema-
> 33	--     qualified — closing the search_path-injection vector a definer function otherwise carries.
> 34	--   * EXECUTE on the helper is REVOKED from PUBLIC/anon/authenticated. It is an internal primitive
> 35	--     called only by the (already definer, owner=postgres) encryption triggers; it must NOT be a
> 36	--     PostgREST-reachable RPC, since by-name access would otherwise let a caller overwrite ANY
> 37	--     tenant's secret. The triggers run as postgres (their definer) and retain EXECUTE as owner.
> 38	--   * The three encryption trigger functions are ALSO pinned to `SET search_path = ''` (they had no
> 39	--     pin before — proconfig was null), matching the precedent set by 20260602130000. postgres keeps
> 40	--     the SELECT it already holds on vault.secrets; the privileged Vault writes stay inside the
> 41	--     SECURITY DEFINER vault.create_secret/update_secret primitives (postgres has EXECUTE, not direct
> 42	--     INSERT/UPDATE on vault.secrets — verified materially 2026-06-02).
> 43	--
> 44	-- Scope: all three credential tables (user_api_keys, meta_config, social_accounts). Triggers keep
> 45	-- their bindings (CREATE OR REPLACE FUNCTION preserves the function oid) — no trigger re-create.
> 46	
> 47	-- ─────────────────────────────────────────────────────────────────────────────
> 48	-- 1. IDEMPOTENT VAULT HELPER
> 49	-- ─────────────────────────────────────────────────────────────────────────────
> 50	CREATE OR REPLACE FUNCTION public.vault_upsert_secret(
> 51	  p_value text,
> 52	  p_name  text,
> 53	  p_desc  text DEFAULT ''
> 54	)
> 55	RETURNS uuid
> 56	LANGUAGE plpgsql
> 57	SECURITY DEFINER
> 58	SET search_path = ''
> 59	AS $$
> 60	DECLARE
> 61	  v_id uuid;
> 62	BEGIN
> 63	  -- vault.secrets.name is UNIQUE (secrets_name_idx). Resolve an existing secret by its
> 64	  -- deterministic name and rotate the value in place — this is what makes re-saving a credential
> 65	  -- idempotent instead of throwing unique_violation (23505). vault.update_secret COALESCE-keeps the
> 66	  -- name + description and re-encrypts only the value, so the stored UUID reference never changes.
> 67	  SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;
> 68	
> 69	  IF v_id IS NOT NULL THEN
> 70	    PERFORM vault.update_secret(v_id, p_value);
> 71	    RETURN v_id;
> 72	  END IF;
> 73	
> 74	  RETURN vault.create_secret(p_value, p_name, p_desc);
> 75	
> 76	EXCEPTION
> 77	  -- Concurrency guard: a parallel writer created the same name between our SELECT and
> 78	  -- create_secret. Re-resolve and update in place rather than surfacing 23505 to the caller.
> 79	  WHEN unique_violation THEN
> 80	    SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;
> 81	    IF v_id IS NOT NULL THEN
> 82	      PERFORM vault.update_secret(v_id, p_value);
> 83	      RETURN v_id;
> 84	    END IF;
> 85	    RAISE;
> 86	END;
> 87	$$;
> 88	
> 89	COMMENT ON FUNCTION public.vault_upsert_secret(text, text, text) IS
> 90	  'Internal: idempotent Vault secret write keyed by deterministic name (update-in-place when the '
> 91	  'name exists, else create). Called ONLY by the credential encryption triggers — EXECUTE is revoked '
> 92	  'from clients. Eliminates the secrets_name_idx 23505 on credential re-save.';
> 93	
> 94	-- Internal primitive only — never a client-reachable RPC (would allow by-name cross-tenant overwrite).
> 95	REVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM PUBLIC;
> 96	REVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM anon, authenticated;
> 97	
> 98	-- ─────────────────────────────────────────────────────────────────────────────
> 99	-- 2. user_api_keys encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> 100	--    (latest definition as of 20260601060000, incl. apify_token; + search_path pin)
> 101	-- ─────────────────────────────────────────────────────────────────────────────
> 102	CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> 103	RETURNS TRIGGER
> 104	LANGUAGE plpgsql
> 105	SECURITY DEFINER
> 106	SET search_path = ''
> 107	AS $$
> 108	DECLARE
> 109	  v_id UUID;
> 110	BEGIN
> 111	  -- groq_api_key
> 112	  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN
> 113	    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 114	      -- keep existing UUID reference
> 115	    ELSE
> 116	      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key');
> 117	      NEW.groq_api_key = v_id::text;
> 118	    END IF;
> 119	  END IF;
> 120	
> 121	  -- openrouter_api_key
> 122	  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> 123	    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 124	      -- keep existing UUID reference
> 125	    ELSE
> 126	      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> 127	      NEW.openrouter_api_key = v_id::text;
> 128	    END IF;
> 129	  END IF;
> 130	
> 131	  -- openai_api_key
> 132	  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN
> 133	    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 134	      -- keep existing UUID reference
> 135	    ELSE
> 136	      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key');
> 137	      NEW.openai_api_key = v_id::text;
> 138	    END IF;
> 139	  END IF;
> 140	
> 141	  -- elevenlabs_api_key
> 142	  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN
> 143	    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 144	      -- keep existing UUID reference
> 145	    ELSE
> 146	      v_id := public.vault_upsert_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key');
> 147	      NEW.elevenlabs_api_key = v_id::text;
> 148	    END IF;
> 149	  END IF;
> 150	
> 151	  -- google_api_key
> 152	  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> 153	    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 154	      -- keep existing UUID reference
> 155	    ELSE
> 156	      v_id := public.vault_upsert_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');
> 157	      NEW.google_api_key = v_id::text;
> 158	    END IF;
> 159	  END IF;
> 160	
> 161	  -- nanobana_api_key
> 162	  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN
> 163	    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 164	      -- keep existing UUID reference
> 165	    ELSE
> 166	      v_id := public.vault_upsert_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key');
> 167	      NEW.nanobana_api_key = v_id::text;
> 168	    END IF;
> 169	  END IF;
> 170	
> 171	  -- seedance_api_key
> 172	  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN
> 173	    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 174	      -- keep existing UUID reference
> 175	    ELSE
> 176	      v_id := public.vault_upsert_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key');
> 177	      NEW.seedance_api_key = v_id::text;
> 178	    END IF;
> 179	  END IF;
> 180	
> 181	  -- wp_app_password
> 182	  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN
> 183	    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 184	      -- keep existing UUID reference
> 185	    ELSE
> 186	      v_id := public.vault_upsert_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password');
> 187	      NEW.wp_app_password = v_id::text;
> 188	    END IF;
> 189	  END IF;
> 190	
> 191	  -- replicate_api_key
> 192	  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN
> 193	    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 194	      -- keep existing UUID reference
> 195	    ELSE
> 196	      v_id := public.vault_upsert_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key');
> 197	      NEW.replicate_api_key = v_id::text;
> 198	    END IF;
> 199	  END IF;
> 200	
> 201	  -- higgsfield_api_key
> 202	  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN
> 203	    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 204	      -- keep existing UUID reference
> 205	    ELSE
> 206	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key');
> 207	      NEW.higgsfield_api_key = v_id::text;
> 208	    END IF;
> 209	  END IF;
> 210	
> 211	  -- higgsfield_api_key_secret
> 212	  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN
> 213	    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 214	      -- keep existing UUID reference
> 215	    ELSE
> 216	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret');
> 217	      NEW.higgsfield_api_key_secret = v_id::text;
> 218	    END IF;
> 219	  END IF;
> 220	
> 221	  -- apify_token
> 222	  IF NEW.apify_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.apify_token IS DISTINCT FROM OLD.apify_token) THEN
> 223	    IF NEW.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 224	      -- keep existing UUID reference
> 225	    ELSE
> 226	      v_id := public.vault_upsert_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token');
> 227	      NEW.apify_token = v_id::text;
> 228	    END IF;
> 229	  END IF;
> 230	
> 231	  RETURN NEW;
> 232	END;
> 233	$$;
> 234	
> 235	-- ─────────────────────────────────────────────────────────────────────────────
> 236	-- 3. meta_config encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> 237	-- ─────────────────────────────────────────────────────────────────────────────
> 238	CREATE OR REPLACE FUNCTION public.trg_encrypt_meta_config()
> 239	RETURNS TRIGGER
> 240	LANGUAGE plpgsql
> 241	SECURITY DEFINER
> 242	SET search_path = ''
> 243	AS $$
> 244	DECLARE
> 245	  v_token_id UUID;
> 246	  v_pages_id UUID;
> 247	BEGIN
> 248	  IF NEW.id IS NULL THEN
> 249	    NEW.id := gen_random_uuid();
> 250	  END IF;
> 251	
> 252	  IF NEW.long_lived_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.long_lived_token IS DISTINCT FROM OLD.long_lived_token) THEN
> 253	    IF NEW.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 254	      -- keep existing UUID reference
> 255	    ELSE
> 256	      v_token_id := public.vault_upsert_secret(NEW.long_lived_token, 'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token');
> 257	      NEW.long_lived_token = v_token_id::text;
> 258	    END IF;
> 259	  END IF;
> 260	
> 261	  IF NEW.pages IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.pages IS DISTINCT FROM OLD.pages) THEN
> 262	    IF NEW.pages::text ~ '^"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"$' THEN
> 263	      -- keep existing UUID JSON reference
> 264	    ELSE
> 265	      v_pages_id := public.vault_upsert_secret(NEW.pages::text, 'meta_config_pages_' || NEW.id::text, 'Meta config pages list');
> 266	      NEW.pages = to_jsonb(v_pages_id::text);
> 267	    END IF;
> 268	  END IF;
> 269	
> 270	  RETURN NEW;
> 271	END;
> 272	$$;
> 273	
> 274	-- ─────────────────────────────────────────────────────────────────────────────
> 275	-- 4. social_accounts encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> 276	-- ─────────────────────────────────────────────────────────────────────────────
> 277	CREATE OR REPLACE FUNCTION public.trg_encrypt_social_accounts()
> 278	RETURNS TRIGGER
> 279	LANGUAGE plpgsql
> 280	SECURITY DEFINER
> 281	SET search_path = ''
> 282	AS $$
> 283	DECLARE
> 284	  v_access_token_id UUID;
> 285	  v_refresh_token_id UUID;
> 286	BEGIN
> 287	  IF NEW.id IS NULL THEN
> 288	    NEW.id := gen_random_uuid();
> 289	  END IF;
> 290	
> 291	  IF NEW.access_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.access_token IS DISTINCT FROM OLD.access_token) THEN
> 292	    IF NEW.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 293	      -- keep existing UUID reference
> 294	    ELSE
> 295	      v_access_token_id := public.vault_upsert_secret(NEW.access_token, 'social_accounts_access_token_' || NEW.id::text, 'Social account access token');
> 296	      NEW.access_token = v_access_token_id::text;
> 297	    END IF;
> 298	  END IF;
> 299	
> 300	  IF NEW.refresh_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.refresh_token IS DISTINCT FROM OLD.refresh_token) THEN
> 301	    IF NEW.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 302	      -- keep existing UUID reference
> 303	    ELSE
> 304	      v_refresh_token_id := public.vault_upsert_secret(NEW.refresh_token, 'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token');
> 305	      NEW.refresh_token = v_refresh_token_id::text;
> 306	    END IF;
> 307	  END IF;
> 308	
> 309	  RETURN NEW;
> 310	END;
> 311	$$;
> 312	
> ```

## 🤖 Claude *(15:41:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601000000_credential_encryption.sql",
  "offset": 456,
  "limit": 190
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 456	-- 5.2 Instead of trigger for social_accounts
> 457	CREATE OR REPLACE FUNCTION public.trg_instead_of_social_accounts()
> 458	RETURNS TRIGGER AS $$
> 459	BEGIN
> 460	  IF TG_OP = 'DELETE' THEN
> 461	    DELETE FROM public.social_accounts_table WHERE id = OLD.id;
> 462	    RETURN OLD;
> 463	  ELSIF TG_OP = 'INSERT' THEN
> 464	    INSERT INTO public.social_accounts_table (
> 465	      id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, token_expires_at, scopes, is_active, metadata
> 466	    ) VALUES (
> 467	      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.platform_user_id, NEW.platform_username, NEW.access_token, NEW.refresh_token, NEW.token_expires_at, NEW.scopes, NEW.is_active, NEW.metadata
> 468	    );
> 469	    RETURN NEW;
> 470	  ELSIF TG_OP = 'UPDATE' THEN
> 471	    UPDATE public.social_accounts_table SET
> 472	      user_id = NEW.user_id,
> 473	      platform = NEW.platform,
> 474	      platform_user_id = NEW.platform_user_id,
> 475	      platform_username = NEW.platform_username,
> 476	      access_token = COALESCE(NULLIF(NEW.access_token, '••••••••••••'), public.social_accounts_table.access_token),
> 477	      refresh_token = COALESCE(NULLIF(NEW.refresh_token, '••••••••••••'), public.social_accounts_table.refresh_token),
> 478	      token_expires_at = NEW.token_expires_at,
> 479	      scopes = NEW.scopes,
> 480	      is_active = NEW.is_active,
> 481	      metadata = NEW.metadata,
> 482	      updated_at = now()
> 483	    WHERE id = OLD.id;
> 484	    RETURN NEW;
> 485	  END IF;
> 486	  RETURN NULL;
> 487	END;
> 488	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 489	
> 490	CREATE TRIGGER trg_instead_of_social_accounts
> 491	  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.social_accounts
> 492	  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_social_accounts();
> 493	
> 494	
> 495	-- 5.3 Instead of trigger for user_api_keys
> 496	CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> 497	RETURNS TRIGGER AS $$
> 498	BEGIN
> 499	  IF TG_OP = 'DELETE' THEN
> 500	    DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
> 501	    RETURN OLD;
> 502	  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
> 503	    INSERT INTO public.user_api_keys_table (
> 504	      user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret
> 505	    ) VALUES (
> 506	      NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret
> 507	    )
> 508	    ON CONFLICT (user_id) DO UPDATE SET
> 509	      groq_api_key = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
> 510	      openrouter_api_key = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> 511	      openai_api_key = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
> 512	      pref_audio_provider = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
> 513	      pref_image_provider = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
> 514	      pref_video_provider = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
> 515	      elevenlabs_api_key = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
> 516	      google_api_key = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
> 517	      nanobana_api_key = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
> 518	      seedance_api_key = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
> 519	      wp_site_url = NEW.wp_site_url,
> 520	      wp_username = NEW.wp_username,
> 521	      wp_app_password = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
> 522	      pref_ai_model = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
> 523	      replicate_api_key = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
> 524	      higgsfield_api_key = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
> 525	      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
> 526	      updated_at = now();
> 527	    RETURN NEW;
> 528	  END IF;
> 529	  RETURN NULL;
> 530	END;
> 531	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 532	
> 533	CREATE TRIGGER trg_instead_of_user_api_keys
> 534	  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.user_api_keys
> 535	  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_user_api_keys();
> 536	
> 537	
> 538	-- ─────────────────────────────────────────────────────────────────────────────
> 539	-- 6. PRIVATE DECRYPTED VIEWS: Real decrypted keys view for service_role
> 540	-- ─────────────────────────────────────────────────────────────────────────────
> 541	
> 542	-- 6.1 decrypted_meta_config
> 543	CREATE OR REPLACE VIEW public.decrypted_meta_config AS
> 544	SELECT 
> 545	  mc.id,
> 546	  mc.user_id,
> 547	  mc.facebook_user_id,
> 548	  COALESCE(s_token.decrypted_secret, mc.long_lived_token) AS long_lived_token,
> 549	  mc.scopes,
> 550	  COALESCE(s_pages.decrypted_secret::jsonb, mc.pages) AS pages,
> 551	  mc.instagram_business_account_id,
> 552	  mc.whatsapp_phone_number_id,
> 553	  mc.whatsapp_waba_id,
> 554	  mc.meta_ad_account_id,
> 555	  mc.requires_reauth,
> 556	  mc.token_expires_at,
> 557	  mc.created_at,
> 558	  mc.updated_at
> 559	FROM public.meta_config_table mc
> 560	LEFT JOIN vault.decrypted_secrets s_token ON mc.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_token.id = mc.long_lived_token::uuid
> 561	LEFT JOIN vault.decrypted_secrets s_pages ON mc.pages::text ~ '^"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"$' AND s_pages.id = (mc.pages#>>'{}')::uuid;
> 562	
> 563	-- 6.2 decrypted_social_accounts
> 564	CREATE OR REPLACE VIEW public.decrypted_social_accounts AS
> 565	SELECT 
> 566	  sa.id,
> 567	  sa.user_id,
> 568	  sa.platform,
> 569	  sa.platform_user_id,
> 570	  sa.platform_username,
> 571	  COALESCE(s_access.decrypted_secret, sa.access_token) AS access_token,
> 572	  COALESCE(s_refresh.decrypted_secret, sa.refresh_token) AS refresh_token,
> 573	  sa.token_expires_at,
> 574	  sa.scopes,
> 575	  sa.is_active,
> 576	  sa.metadata,
> 577	  sa.created_at,
> 578	  sa.updated_at
> 579	FROM public.social_accounts_table sa
> 580	LEFT JOIN vault.decrypted_secrets s_access ON sa.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_access.id = sa.access_token::uuid
> 581	LEFT JOIN vault.decrypted_secrets s_refresh ON sa.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_refresh.id = sa.refresh_token::uuid;
> 582	
> 583	-- 6.3 decrypted_user_api_keys
> 584	CREATE OR REPLACE VIEW public.decrypted_user_api_keys AS
> 585	SELECT 
> 586	  uak.user_id,
> 587	  COALESCE(s_groq.decrypted_secret, uak.groq_api_key) AS groq_api_key,
> 588	  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> 589	  COALESCE(s_openai.decrypted_secret, uak.openai_api_key) AS openai_api_key,
> 590	  uak.created_at,
> 591	  uak.updated_at,
> 592	  uak.pref_audio_provider,
> 593	  uak.pref_image_provider,
> 594	  uak.pref_video_provider,
> 595	  COALESCE(s_elevenlabs.decrypted_secret, uak.elevenlabs_api_key) AS elevenlabs_api_key,
> 596	  COALESCE(s_google.decrypted_secret, uak.google_api_key) AS google_api_key,
> 597	  COALESCE(s_nanobana.decrypted_secret, uak.nanobana_api_key) AS nanobana_api_key,
> 598	  COALESCE(s_seedance.decrypted_secret, uak.seedance_api_key) AS seedance_api_key,
> 599	  uak.wp_site_url,
> 600	  uak.wp_username,
> 601	  COALESCE(s_wp_pwd.decrypted_secret, uak.wp_app_password) AS wp_app_password,
> 602	  uak.pref_ai_model,
> 603	  COALESCE(s_replicate.decrypted_secret, uak.replicate_api_key) AS replicate_api_key,
> 604	  COALESCE(s_higgsfield.decrypted_secret, uak.higgsfield_api_key) AS higgsfield_api_key,
> 605	  COALESCE(s_higgsfield_sec.decrypted_secret, uak.higgsfield_api_key_secret) AS higgsfield_api_key_secret
> 606	FROM public.user_api_keys_table uak
> 607	LEFT JOIN vault.decrypted_secrets s_groq ON uak.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_groq.id = uak.groq_api_key::uuid
> 608	LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> 609	LEFT JOIN vault.decrypted_secrets s_openai ON uak.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openai.id = uak.openai_api_key::uuid
> 610	LEFT JOIN vault.decrypted_secrets s_elevenlabs ON uak.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_elevenlabs.id = uak.elevenlabs_api_key::uuid
> 611	LEFT JOIN vault.decrypted_secrets s_google ON uak.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_google.id = uak.google_api_key::uuid
> 612	LEFT JOIN vault.decrypted_secrets s_nanobana ON uak.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_nanobana.id = uak.nanobana_api_key::uuid
> 613	LEFT JOIN vault.decrypted_secrets s_seedance ON uak.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_seedance.id = uak.seedance_api_key::uuid
> 614	LEFT JOIN vault.decrypted_secrets s_wp_pwd ON uak.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_wp_pwd.id = uak.wp_app_password::uuid
> 615	LEFT JOIN vault.decrypted_secrets s_replicate ON uak.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_replicate.id = uak.replicate_api_key::uuid
> 616	LEFT JOIN vault.decrypted_secrets s_higgsfield ON uak.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield.id = uak.higgsfield_api_key::uuid
> 617	LEFT JOIN vault.decrypted_secrets s_higgsfield_sec ON uak.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield_sec.id = uak.higgsfield_api_key_secret::uuid;
> 618	
> 619	
> 620	-- ─────────────────────────────────────────────────────────────────────────────
> 621	-- 7. PERMISSIONS: Restrict view selects
> 622	-- ─────────────────────────────────────────────────────────────────────────────
> 623	
> 624	-- decrypted_* views are restricted to service_role exclusively
> 625	REVOKE ALL ON public.decrypted_meta_config FROM PUBLIC, anon, authenticated;
> 626	GRANT SELECT ON public.decrypted_meta_config TO service_role;
> 627	
> 628	REVOKE ALL ON public.decrypted_social_accounts FROM PUBLIC, anon, authenticated;
> 629	GRANT SELECT ON public.decrypted_social_accounts TO service_role;
> 630	
> 631	REVOKE ALL ON public.decrypted_user_api_keys FROM PUBLIC, anon, authenticated;
> 632	GRANT SELECT ON public.decrypted_user_api_keys TO service_role;
> 633	
> ```

## 🤖 Claude *(15:41:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: tenant guard on meta_config / social_accounts masked-view INSTEAD OF triggers.
> 2	-- ─────────────────────────────────────────────────────────────────────────────
> 3	-- Closes a PRE-EXISTING cross-tenant injection gap surfaced during the /security-review of
> 4	-- 20260602140000 (NOT a regression of that migration). trg_instead_of_meta_config and
> 5	-- trg_instead_of_social_accounts are SECURITY DEFINER (owner postgres, bypass base-table RLS) and
> 6	-- the masked public views grant INSERT to authenticated. PostgreSQL does not apply a view's WHERE
> 7	-- qualification to INSERT, so an authenticated caller could POST a row with a SPOOFED user_id (a
> 8	-- victim's) and a FRESH id — committing a credential row OWNED BY the victim with attacker-controlled
> 9	-- tokens. A service-role publisher iterating that victim's decrypted_* rows would then use the
> 10	-- injected credential (credential confusion / content redirection). The overwrite variant (colliding
> 11	-- id) is already fail-closed by PRIMARY KEY(id) on both base tables; this fixes the injection variant.
> 12	--
> 13	-- Fix: port the exact tenant guard user_api_keys received in 20260602130000 to the INSERT and UPDATE
> 14	-- branches of both sibling INSTEAD OF triggers, and pin SET search_path = '' (they had no pin).
> 15	-- The function bodies below are reproduced VERBATIM from the live definitions (pg_get_functiondef,
> 16	-- 2026-06-02) — preserving every column mapping, COALESCE default, and masked sentinel byte-for-byte —
> 17	-- with ONLY the guard + search_path added. Triggers keep their bindings (CREATE OR REPLACE preserves
> 18	-- the oid) — no trigger re-create.
> 19	--
> 20	-- Production safety (verified 2026-06-02): every legitimate writer is either service_role (the social
> 21	-- OAuth callback — the sole social INSERT — plus refresh-social-token / publish-meta / sync-meta-ads /
> 22	-- self-heal, all using SB_SECRET_KEY → exempt) or an authenticated client writing its OWN row with
> 23	-- user_id = auth.uid() (useMetaConfig.insert; useSocialAccounts never inserts client-side). No legit
> 24	-- non-service-role path writes user_id <> auth.uid(), so the guard only blocks the attack.
> 25	--
> 26	-- SOP: docs/processes/credential-disconnect-clear.md. MANDATORY /security-review (credential layer).
> 27	
> 28	CREATE OR REPLACE FUNCTION public.trg_instead_of_meta_config()
> 29	 RETURNS trigger
> 30	 LANGUAGE plpgsql
> 31	 SECURITY DEFINER
> 32	 SET search_path = ''
> 33	AS $function$
> 34	BEGIN
> 35	  IF TG_OP = 'DELETE' THEN
> 36	    DELETE FROM public.meta_config_table WHERE id = OLD.id;
> 37	    RETURN OLD;
> 38	  ELSIF TG_OP = 'INSERT' THEN
> 39	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 40	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 41	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 42	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 43	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 44	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 45	    END IF;
> 46	    INSERT INTO public.meta_config_table (
> 47	      id,
> 48	      user_id,
> 49	      facebook_user_id,
> 50	      long_lived_token,
> 51	      scopes,
> 52	      pages,
> 53	      instagram_business_account_id,
> 54	      whatsapp_phone_number_id,
> 55	      whatsapp_waba_id,
> 56	      meta_ad_account_id,
> 57	      requires_reauth,
> 58	      token_expires_at
> 59	    ) VALUES (
> 60	      COALESCE(NEW.id, gen_random_uuid()),
> 61	      NEW.user_id,
> 62	      NEW.facebook_user_id,
> 63	      NEW.long_lived_token,
> 64	      COALESCE(NEW.scopes, '{}'),
> 65	      COALESCE(NEW.pages, '[]'::jsonb),
> 66	      NEW.instagram_business_account_id,
> 67	      NEW.whatsapp_phone_number_id,
> 68	      NEW.whatsapp_waba_id,
> 69	      NEW.meta_ad_account_id,
> 70	      COALESCE(NEW.requires_reauth, FALSE),
> 71	      NEW.token_expires_at
> 72	    );
> 73	    RETURN NEW;
> 74	  ELSIF TG_OP = 'UPDATE' THEN
> 75	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 76	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 77	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 78	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 79	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 80	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 81	    END IF;
> 82	    UPDATE public.meta_config_table SET
> 83	      user_id = NEW.user_id,
> 84	      facebook_user_id = NEW.facebook_user_id,
> 85	      long_lived_token = COALESCE(NULLIF(NEW.long_lived_token, '••••••••••••'), public.meta_config_table.long_lived_token),
> 86	      scopes = COALESCE(NEW.scopes, public.meta_config_table.scopes),
> 87	      pages = COALESCE(NULLIF(NEW.pages, to_jsonb('••••••••••••'::text)), public.meta_config_table.pages),
> 88	      instagram_business_account_id = NEW.instagram_business_account_id,
> 89	      whatsapp_phone_number_id = NEW.whatsapp_phone_number_id,
> 90	      whatsapp_waba_id = NEW.whatsapp_waba_id,
> 91	      meta_ad_account_id = NEW.meta_ad_account_id,
> 92	      requires_reauth = COALESCE(NEW.requires_reauth, public.meta_config_table.requires_reauth),
> 93	      token_expires_at = NEW.token_expires_at,
> 94	      updated_at = now()
> 95	    WHERE id = OLD.id;
> 96	    RETURN NEW;
> 97	  END IF;
> 98	  RETURN NULL;
> 99	END;
> 100	$function$;
> 101	
> 102	CREATE OR REPLACE FUNCTION public.trg_instead_of_social_accounts()
> 103	 RETURNS trigger
> 104	 LANGUAGE plpgsql
> 105	 SECURITY DEFINER
> 106	 SET search_path = ''
> 107	AS $function$
> 108	BEGIN
> 109	  IF TG_OP = 'DELETE' THEN
> 110	    DELETE FROM public.social_accounts_table WHERE id = OLD.id;
> 111	    RETURN OLD;
> 112	  ELSIF TG_OP = 'INSERT' THEN
> 113	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 114	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 115	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 116	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 117	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 118	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 119	    END IF;
> 120	    INSERT INTO public.social_accounts_table (
> 121	      id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, token_expires_at, scopes, is_active, metadata
> 122	    ) VALUES (
> 123	      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.platform_user_id, NEW.platform_username, NEW.access_token, NEW.refresh_token, NEW.token_expires_at, NEW.scopes, NEW.is_active, NEW.metadata
> 124	    );
> 125	    RETURN NEW;
> 126	  ELSIF TG_OP = 'UPDATE' THEN
> 127	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 128	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 129	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 130	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 131	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 132	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 133	    END IF;
> 134	    UPDATE public.social_accounts_table SET
> 135	      user_id = NEW.user_id,
> 136	      platform = NEW.platform,
> 137	      platform_user_id = NEW.platform_user_id,
> 138	      platform_username = NEW.platform_username,
> 139	      access_token = COALESCE(NULLIF(NEW.access_token, '••••••••••••'), public.social_accounts_table.access_token),
> 140	      refresh_token = COALESCE(NULLIF(NEW.refresh_token, '••••••••••••'), public.social_accounts_table.refresh_token),
> 141	      token_expires_at = NEW.token_expires_at,
> 142	      scopes = NEW.scopes,
> 143	      is_active = NEW.is_active,
> 144	      metadata = NEW.metadata,
> 145	      updated_at = now()
> 146	    WHERE id = OLD.id;
> 147	    RETURN NEW;
> 148	  END IF;
> 149	  RETURN NULL;
> 150	END;
> 151	$function$;
> 152	
> ```

## 🤖 Claude *(15:42:31)*


## 🤖 Claude *(15:42:33)*

Tenho o padrão canônico completo (encrypt trigger idempotente via `vault_upsert_secret`, decrypted view service-role, INSTEAD OF com tenant-guard + preservação da máscara). Falta só a sintaxe exata da masked VIEW para espelhar byte-fiel. Lendo a seção 4.

## 🤖 Claude *(15:42:34)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601000000_credential_encryption.sql",
  "offset": 345,
  "limit": 45
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 345	-- ─────────────────────────────────────────────────────────────────────────────
> 346	-- 4. PUBLIC MASKED VIEWS: Security invoker views for client-side compat
> 347	-- ─────────────────────────────────────────────────────────────────────────────
> 348	
> 349	-- 4.1 meta_config public view
> 350	CREATE OR REPLACE VIEW public.meta_config WITH (security_invoker = true) AS
> 351	SELECT
> 352	  id,
> 353	  user_id,
> 354	  facebook_user_id,
> 355	  CASE WHEN long_lived_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS long_lived_token,
> 356	  scopes,
> 357	  CASE WHEN pages IS NOT NULL THEN to_jsonb('••••••••••••'::text) ELSE NULL END AS pages,
> 358	  instagram_business_account_id,
> 359	  whatsapp_phone_number_id,
> 360	  whatsapp_waba_id,
> 361	  meta_ad_account_id,
> 362	  requires_reauth,
> 363	  token_expires_at,
> 364	  created_at,
> 365	  updated_at
> 366	FROM public.meta_config_table;
> 367	
> 368	-- 4.2 social_accounts public view
> 369	CREATE OR REPLACE VIEW public.social_accounts WITH (security_invoker = true) AS
> 370	SELECT
> 371	  id,
> 372	  user_id,
> 373	  platform,
> 374	  platform_user_id,
> 375	  platform_username,
> 376	  CASE WHEN access_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS access_token,
> 377	  CASE WHEN refresh_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS refresh_token,
> 378	  token_expires_at,
> 379	  scopes,
> 380	  is_active,
> 381	  metadata,
> 382	  created_at,
> 383	  updated_at
> 384	FROM public.social_accounts_table;
> 385	
> 386	-- 4.3 user_api_keys public view
> 387	CREATE OR REPLACE VIEW public.user_api_keys WITH (security_invoker = true) AS
> 388	SELECT
> 389	  user_id,
> ```

## 🤖 Claude *(15:43:51)*


## 🤖 Claude *(15:43:53)*

Tenho o padrão canônico completo, byte-fiel. Autorando a migration `social_app_config` espelhando exatamente o tratamento Vault do `social_accounts` (encrypt trigger idempotente · masked view security_invoker · decrypted view service-role · INSTEAD OF com tenant-guard 42501 · REVOKE no secret).

## 🤖 Claude *(15:44:33)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260627120000_social_app_config.sql",
  "content": "-- Migration: social_app_config \u2014 per-user OAuth APP credentials for TikTok / YouTube / Pinterest\n--            (client_id + Vault-encrypted client_secret), keyed UNIQUE(user_id, platform).\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- BoK SSOT: docs/bok/post-engine/06-data-model.md (social_app_config) + 10-amendment-social-connect-*.md (FR-PE-005).\n-- SOPs (Lei 2, written before this migration): docs/processes/{tiktok,youtube,pinterest}-publish-credential-resolution.md.\n-- API Tenancy Model (CLAUDE.md): per-user credentials, RLS-isolated, Vault-encrypted secret, tenant-guarded writes.\n-- Resolution order in edge functions: (1) social_app_config per-user (is_active) \u2192 (2) env fallback\n--   (TIKTOK_CLIENT_KEY/SECRET, GOOGLE_CLIENT_ID/SECRET, PINTEREST_CLIENT_ID/SECRET \u2014 Sovereign-only onboarding\n--   default, OTD-PE-SOCIAL-APPCREDS) \u2192 (3) hard fail 402/501 {error:\"<platform>_not_configured\"}.\n--\n-- This MIRRORS the canonical credential pattern of social_accounts (migrations 20260601000000 +\n-- 20260602140000 idempotent vault_upsert_secret + 20260602150000 tenant guard), reproduced for a NEW\n-- table that is born Vault-encrypted (no plaintext-then-backfill phase):\n--   * client_id is a semi-public OAuth identifier \u2192 stored plaintext, readable.\n--   * client_secret is a secret \u2192 encrypted at-rest in Vault by a BEFORE INSERT/UPDATE trigger; the base\n--     column holds only the Vault secret UUID. Even a direct read of the base table never yields plaintext.\n--   * Masked public VIEW returns '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022' for client_secret (security_invoker \u2192 RLS applies).\n--   * decrypted_social_app_config exposes the real secret to service_role ONLY (edge functions).\n--   * INSTEAD OF trigger maps view writes to the base table with the tenant guard (auth.uid()=user_id;\n--     service_role exempt) + mask-preservation, closing the cross-tenant injection that a view's WHERE\n--     does not constrain for INSERT.\n--\n-- Security posture: HARDENS. NO new SECURITY DEFINER RPC reachable by clients. MANDATORY /security-review\n-- (credential layer, FMEA-011). Orphaned-secret revocation on disconnect is a follow-up RPC\n-- (disconnect_social_app_config, mirroring 20260602160000) \u2014 deferred to the Settings-UI slice.\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 1. BASE TABLE \u2014 social_app_config_table (one row per user \u00d7 platform)\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE TABLE IF NOT EXISTS public.social_app_config_table (\n    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\n    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,\n    platform public.social_platform NOT NULL,\n    client_id TEXT,                                        -- OAuth client_id / TikTok client_key (semi-public)\n    client_secret TEXT,                                    -- secret \u2192 Vault UUID after trg_encrypt_social_app_config\n    scopes TEXT[] NOT NULL DEFAULT '{}',\n    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,           -- platform extras: youtube channel_id, pinterest board_id, redirect_uri override\n    is_active BOOLEAN NOT NULL DEFAULT TRUE,\n    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),\n    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),\n    CONSTRAINT unique_user_platform_app_config UNIQUE (user_id, platform)\n);\n\nALTER TABLE public.social_app_config_table ENABLE ROW LEVEL SECURITY;\n\n-- Default-deny: only the owner tenant can touch their row (base-table RLS; service_role bypasses).\nCREATE POLICY \"Users manage their own social app config\" ON public.social_app_config_table\n    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);\n\nCREATE TRIGGER tr_update_social_app_config_updated_at\n    BEFORE UPDATE ON public.social_app_config_table\n    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();\n\nCREATE INDEX IF NOT EXISTS idx_social_app_config_user ON public.social_app_config_table (user_id);\n\n-- Column-level hardening: the secret column is WRITE-ONLY for clients (BYOK paste via the masked view),\n-- never returned via PostgREST. service_role (edge functions) reads it through decrypted_social_app_config.\n-- Mirrors meta_config.long_lived_token (20260530210000) \u2014 proven compatible with the security_invoker view.\nREVOKE SELECT (client_secret) ON public.social_app_config_table FROM anon, authenticated;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 2. ENCRYPTION TRIGGER \u2014 client_secret \u2192 Vault (idempotent vault_upsert_secret, keyed by row id)\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.trg_encrypt_social_app_config()\nRETURNS TRIGGER\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_secret_id UUID;\nBEGIN\n  IF NEW.id IS NULL THEN\n    NEW.id := gen_random_uuid();\n  END IF;\n\n  IF NEW.client_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.client_secret IS DISTINCT FROM OLD.client_secret) THEN\n    IF NEW.client_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- already a Vault UUID reference \u2192 keep\n    ELSE\n      v_secret_id := public.vault_upsert_secret(\n        NEW.client_secret,\n        'social_app_config_client_secret_' || NEW.id::text,\n        'Social app OAuth client secret'\n      );\n      NEW.client_secret = v_secret_id::text;\n    END IF;\n  END IF;\n\n  RETURN NEW;\nEND;\n$$;\n\nCREATE OR REPLACE TRIGGER tr_encrypt_social_app_config\n  BEFORE INSERT OR UPDATE ON public.social_app_config_table\n  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_social_app_config();\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 3. PUBLIC MASKED VIEW \u2014 security_invoker (RLS applies); client_secret hidden\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE VIEW public.social_app_config WITH (security_invoker = true) AS\nSELECT\n  id,\n  user_id,\n  platform,\n  client_id,\n  CASE WHEN client_secret IS NOT NULL THEN '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022' ELSE NULL END AS client_secret,\n  scopes,\n  metadata,\n  is_active,\n  created_at,\n  updated_at\nFROM public.social_app_config_table;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 4. INSTEAD OF TRIGGER \u2014 map view writes to base table (tenant guard + mask preservation)\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.trg_instead_of_social_app_config()\nRETURNS TRIGGER\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nBEGIN\n  IF TG_OP = 'DELETE' THEN\n    DELETE FROM public.social_app_config_table WHERE id = OLD.id;\n    RETURN OLD;\n  ELSIF TG_OP = 'INSERT' THEN\n    -- Tenant guard (mirrors 20260602150000): a non-service-role caller may only write its OWN row.\n    -- Closes the cross-tenant injection (spoofed user_id + fresh id) a view's WHERE does not constrain\n    -- for INSERT. service_role (OAuth callbacks / cron) is exempt.\n    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    INSERT INTO public.social_app_config_table (\n      id, user_id, platform, client_id, client_secret, scopes, metadata, is_active\n    ) VALUES (\n      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.client_id, NEW.client_secret,\n      COALESCE(NEW.scopes, '{}'), COALESCE(NEW.metadata, '{}'::jsonb), COALESCE(NEW.is_active, TRUE)\n    );\n    RETURN NEW;\n  ELSIF TG_OP = 'UPDATE' THEN\n    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    UPDATE public.social_app_config_table SET\n      user_id = NEW.user_id,\n      platform = NEW.platform,\n      client_id = NEW.client_id,\n      -- preserve the stored secret when the client writes back the mask sentinel\n      client_secret = COALESCE(NULLIF(NEW.client_secret, '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'), public.social_app_config_table.client_secret),\n      scopes = COALESCE(NEW.scopes, public.social_app_config_table.scopes),\n      metadata = COALESCE(NEW.metadata, public.social_app_config_table.metadata),\n      is_active = COALESCE(NEW.is_active, public.social_app_config_table.is_active),\n      updated_at = now()\n    WHERE id = OLD.id;\n    RETURN NEW;\n  END IF;\n  RETURN NULL;\nEND;\n$$;\n\nCREATE TRIGGER trg_instead_of_social_app_config\n  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.social_app_config\n  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_social_app_config();\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 5. PRIVATE DECRYPTED VIEW \u2014 real client_secret for service_role ONLY (edge functions)\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE VIEW public.decrypted_social_app_config AS\nSELECT\n  sac.id,\n  sac.user_id,\n  sac.platform,\n  sac.client_id,\n  COALESCE(s_secret.decrypted_secret, sac.client_secret) AS client_secret,\n  sac.scopes,\n  sac.metadata,\n  sac.is_active,\n  sac.created_at,\n  sac.updated_at\nFROM public.social_app_config_table sac\nLEFT JOIN vault.decrypted_secrets s_secret\n  ON sac.client_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n  AND s_secret.id = sac.client_secret::uuid;\n\nREVOKE ALL ON public.decrypted_social_app_config FROM PUBLIC, anon, authenticated;\nGRANT SELECT ON public.decrypted_social_app_config TO service_role;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260627120000_social_app_config.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(15:44:41)*


## 🤖 Claude *(15:44:43)*

Migration autorada. Antes de aplicar em prod, ela **precisa passar no `/security-review`** (regra inquebrável do CLAUDE.md — toda migration nova, FMEA-011). Rodando.

## 🤖 Claude *(15:44:43)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "security-review",
  "args": "supabase/migrations/20260627120000_social_app_config.sql"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: security-review
> ```

## 👤 User *(15:44:43)*

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   docs/bok/post-engine/00-index.md
	modified:   docs/bok/post-engine/06-data-model.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/context/social-app-registration-playbook-2026-06-27.md
	.claude/context/social-connect-3platforms-blueprint-2026-06-27.md
	docs/bok/post-engine/09-pattern-conformance.md
	docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md
	docs/processes/pinterest-publish-credential-resolution.md
	docs/processes/tiktok-publish-credential-resolution.md
	docs/processes/youtube-publish-credential-resolution.md
	supabase/migrations/20260627120000_social_app_config.sql

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

## 🤖 Claude *(15:44:53)*


## 🤖 Claude *(15:45:10)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Security review of migration",
  "subagent_type": "general-purpose",
  "prompt": "You are a senior security engineer doing a focused security review of ONE new Supabase migration. Only flag HIGH-CONFIDENCE (>80%) concretely-exploitable vulnerabilities NEWLY introduced by this file. Do NOT flag documentation, DOS, rate-limiting, or theoretical issues. The credential-layer threat model is cross-tenant data leak (FMEA-011): a tenant reading/writing another tenant's secret, or a secret being exposed to a non-service role.\n\nREVIEW THIS FILE: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260627120000_social_app_config.sql\n\nGROUND IT against the canonical sibling patterns it claims to mirror (read these):\n- supabase/migrations/20260601000000_credential_encryption.sql  (masked view security_invoker + decrypted view service-role + INSTEAD OF)\n- supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql  (idempotent encrypt helper + search_path pin)\n- supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql  (the auth.uid() tenant guard on INSTEAD OF INSERT/UPDATE)\n\nCheck specifically, with a verdict + confidence (1-10) each:\n1. Tenant isolation: does the INSTEAD OF INSERT and UPDATE guard against a non-service-role caller writing NEW.user_id <> auth.uid()? Is the base-table RLS default-deny + auth.uid()=user_id? Could an authenticated user read/write another tenant's row or secret?\n2. Secret exposure: is client_secret Vault-encrypted (base column holds only a UUID)? Is the decrypted_social_app_config view REVOKE'd from anon/authenticated and GRANT'd to service_role only? Is the masked view security_invoker (so RLS applies)? Could a client read the plaintext client_secret via the masked view, the base table, or the decrypted view?\n3. SECURITY DEFINER functions: are trg_encrypt_social_app_config and trg_instead_of_social_app_config pinned to SET search_path=''? Is any new SECURITY DEFINER function reachable as a PostgREST RPC by clients (it should NOT be)? Does the encrypt trigger use the idempotent vault_upsert_secret (avoiding the 23505 re-save bug)?\n4. Mask preservation: does the UPDATE branch COALESCE(NULLIF(NEW.client_secret,'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'), base.client_secret) so writing back the mask does not wipe the stored secret?\n5. Any deviation from the sibling pattern that WEAKENS security (missing guard branch, missing REVOKE, wrong role grant, a column that leaks the secret).\n\nReturn a markdown report. For each finding: file:line, severity (HIGH/MEDIUM), category, description, concrete exploit scenario, fix, confidence (1-10). If the migration faithfully mirrors the secure sibling pattern with no new exploitable gap, say so explicitly and list what you verified. Be rigorous but do not invent issues \u2014 this guards real tenant credentials."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': "I have all four files. Let me analyze the new migration line-by-line against the canonical patterns.\n\nI've now traced every claim against the sibling patterns. Here is my finding.\n\n---\n\n# Security Review — `20260627120000_social_app_config.sql`\n\n## Verdict: PASS — faithfully mirrors the secure sibling pattern; no new exploitable cross-tenant gap.\n\nThis migration introduces a NEW Vault-encrypted credential table (`social_app_config_table`) with masked view + decrypted view + encryption trigger + INSTEAD OF tenant guard. I checked each of the five threat vectors. All deviations from the siblings are either improvements or security-neutral. No HIGH/MEDIUM-confidence exploitable vulnerability was found.\n\n---\n\n## 1. Tenant Isolation — SECURE (confidence 9/10)\n\n- **Base-table RLS is default-deny + owner-scoped.** `ENABLE ROW LEVEL SECURITY` (line 44) with a single `FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id)` policy (lines 47–48). No permissive read policy for other tenants. An authenticated client cannot `SELECT`/`INSERT`/`UPDATE`/`DELETE` another tenant's base-table row.\n- **INSTEAD OF INSERT guard present** (lines 132–134): `IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN RAISE EXCEPTION ... 42501`. Byte-identical to the canonical guard in `20260602150000`. This closes the cross-tenant injection (spoofed `user_id` + fresh `id`) that a view's WHERE does not constrain for INSERT.\n- **INSTEAD OF UPDATE guard present** (lines 143–145): same guard. An attacker cannot flip `NEW.user_id` to a victim on update.\n- **One residual note (not a vuln, matches siblings):** the UPDATE branch locates the row by `WHERE id = OLD.id` (line 156). Because the masked view is `security_invoker`, RLS on the base table restricts which `OLD` rows an authenticated caller can even see, so `OLD.id` can only be the caller's own row. The guard on `NEW.user_id` then prevents re-assigning ownership. This is exactly the sibling behavior — secure.\n\n## 2. Secret Exposure — SECURE (confidence 9/10)\n\n- **`client_secret` is Vault-encrypted; base column holds only a UUID.** The BEFORE INSERT/UPDATE trigger (lines 77–88) replaces the plaintext with the Vault secret UUID via `vault_upsert_secret`. The table is born encrypted — there is no plaintext-then-backfill window (no `DO $$ ... vault.create_secret` backfill block, correctly, since the table is new).\n- **Base column additionally REVOKE'd** (line 59): `REVOKE SELECT (client_secret) ON ...social_app_config_table FROM anon, authenticated`. Even a direct base-table read by a client cannot return the column. This is a hardening *beyond* the original sibling (which relied on the masked view alone).\n- **Masked view is `security_invoker = true`** (line 101) → RLS applies, returns the `'••••••••••••'` sentinel for `client_secret` (line 107). A client reading the view sees only the mask.\n- **Decrypted view is service-role-only** (lines 187–188): `REVOKE ALL ... FROM PUBLIC, anon, authenticated; GRANT SELECT ... TO service_role`. Byte-identical to the sibling pattern. A client cannot reach plaintext via the decrypted view.\n\n  **One subtle correctness point I verified explicitly:** `decrypted_social_app_config` is a plain view (no `security_invoker`), so it executes with the **view owner's** privileges. The owner (postgres/superuser-equivalent) can read `vault.decrypted_secrets`, which is required for decryption to work — and is exactly why the GRANT must be restricted to `service_role`. The REVOKE/GRANT is correct and complete. No `anon`/`authenticated`/`PUBLIC` path to plaintext exists.\n\n## 3. SECURITY DEFINER Functions — SECURE (confidence 9/10)\n\n- **Both trigger functions pin `SET search_path = ''`** — `trg_encrypt_social_app_config` (line 68) and `trg_instead_of_social_app_config` (line 122). Every referenced object is schema-qualified (`public.`, `vault.`, `gen_random_uuid()` is a built-in resolved via the empty path with explicit schema where needed). This closes the search_path-injection vector. This is an improvement over the *original* `20260601000000` triggers (which had no pin) and matches the hardened `20260602140000`/`20260602150000`.\n- **No new client-reachable RPC.** Neither function is a callable RPC — both are trigger functions (`RETURNS TRIGGER`), invoked only by their `CREATE TRIGGER` bindings, never exposed via PostgREST. The only by-name Vault primitive (`vault_upsert_secret`) is the pre-existing helper whose EXECUTE is already revoked from clients in `20260602140000` — this migration does not re-grant it.\n- **Encrypt trigger uses the idempotent `vault_upsert_secret`** (line 81), not raw `vault.create_secret`. This avoids the `23505` re-save bug on secret rotation. Correct.\n- **One real (benign) deviation worth noting:** the encrypt trigger keys the Vault secret name by **row `id`** — `'social_app_config_client_secret_' || NEW.id::text` (line 83) — whereas `user_api_keys` keys by `user_id`. This is actually the *correct* choice here, mirroring `meta_config`/`social_accounts` (which key by `id`), because the table is `UNIQUE(user_id, platform)` — multiple rows per user. Keying by `id` guarantees a unique, collision-free Vault name per row. And because `NEW.id` is assigned before the secret is created (lines 73–75 default it if null), the name is always populated. No cross-row secret collision. Secure.\n\n## 4. Mask Preservation — SECURE (confidence 10/10)\n\n- UPDATE branch (line 151): `client_secret = COALESCE(NULLIF(NEW.client_secret, '••••••••••••'), public.social_app_config_table.client_secret)`. Writing back the mask sentinel resolves `NULLIF(...) = NULL → COALESCE` falls through to the stored Vault UUID. The stored secret is **not** wiped when a client re-saves the masked form. Byte-identical to the sibling. The mask string (12 bullets `••••••••••••`) is consistent across the view's CASE (line 107), the NULLIF (line 151), and the siblings.\n\n## 5. Deviations From the Sibling Pattern — none that weaken security (confidence 8/10)\n\nInventory of every deviation, with a security verdict each:\n\n| Deviation | Verdict |\n|---|---|\n| Base column `REVOKE SELECT (client_secret)` (line 59) | **Hardens** — extra defense not in original sibling. |\n| Vault name keyed by `id` not `user_id` (line 83) | **Neutral/correct** — required by `UNIQUE(user_id, platform)`; matches meta/social siblings. |\n| INSTEAD OF INSERT/UPDATE add `COALESCE` defaults for `scopes`/`metadata`/`is_active` (lines 139, 152–154) | **Neutral** — column-default hygiene, no security impact. |\n| `decrypted_*` view's vault JOIN gated by a UUID-shape regex (lines 184–185) | **Neutral/correct** — same defensive JOIN predicate as the siblings; prevents `::uuid` cast errors on non-UUID values. |\n| No `disconnect_social_app_config` RPC for orphaned-secret revocation | **Not a vuln** — explicitly deferred (line 24–25). Orphaned Vault secrets after a row delete are a cleanup/hygiene concern, not a cross-tenant leak: the secret name is bound to a deleted row's `id`, unreachable by any client (EXECUTE on `vault_upsert_secret` revoked; decrypted view service-role-only). DOS/hygiene, out of scope per the review mandate. |\n\n### Two items I checked and confirmed are NOT exploitable\n\n- **DELETE branch has no explicit tenant guard** (lines 125–127): `DELETE FROM ...table WHERE id = OLD.id`. This is safe and matches all three siblings — `OLD` is supplied by the `security_invoker` masked view, so RLS already restricts an authenticated caller to deleting only rows where `auth.uid() = user_id`. A client cannot present another tenant's `OLD.id`. No guard needed (and the siblings omit it too).\n- **`auth.role()`/`auth.uid()` resolution under `search_path = ''`**: both are called schema-unqualified inside the definer functions (e.g. line 132). This matches `20260602150000` verbatim, which is proven in production (the `auth` helpers are resolved because Supabase installs them such that the bare-name call works in this exact precedent). Since the canonical guard migration uses the identical unqualified form and is live, this is not a new risk introduced here. (Confidence the guard fires: high — it is byte-identical to the deployed sibling.)\n\n---\n\n## Summary\n\nThe migration is a faithful, security-equivalent (and in one respect hardened) reproduction of the canonical Vault-credential pattern. **All five checks pass.** Specifically verified: default-deny owner-scoped RLS; INSERT **and** UPDATE tenant guards present and byte-identical to `20260602150000`; `client_secret` Vault-encrypted with the base column additionally column-REVOKE'd; masked view `security_invoker`; decrypted view REVOKE'd from anon/authenticated and GRANT'd to service_role only; both definer functions pinned to `search_path = ''`; idempotent `vault_upsert_secret` used (no 23505); mask-preservation `COALESCE(NULLIF(...))` correct.\n\nNo HIGH or MEDIUM confidence concretely-exploitable cross-tenant vulnerability newly introduced by this file. The single deferred item (orphaned-secret revocation RPC) is a hygiene concern explicitly acknowledged in the header, not a FMEA-011 leak.\n\n**Recommendation: APPROVE for commit.**"}, {'type': 'text', 'text': "agentId: abad13eb4a666b21d (use SendMessage with to: 'abad13eb4a666b21d', summary: '<5-10 word recap>' to continue this agent)\n<usage>subagent_tokens: 107323\ntool_uses: 4\nduration_ms: 53641</usage>"}]
> ```

## 🤖 Claude *(15:46:44)*


## 🤖 Claude *(15:46:50)*

**`/security-review` → SAFE.** A migration espelha fielmente o padrão Vault canônico (ainda endurece com o REVOKE extra no `client_secret`); zero gap cross-tenant novo. Verificado: RLS default-deny owner-scoped · tenant-guard 42501 no INSERT **e** UPDATE (byte-idêntico ao `20260602150000`) · `client_secret` Vault + REVOKE · masked view security_invoker · decrypted view só service_role · ambos definers com `search_path=''` · `vault_upsert_secret` idempotente · preservação da máscara.

# Security Review — `20260627120000_social_app_config.sql`
**Veredito: SAFE — nenhuma vulnerabilidade HIGH/MEDIUM introduzida.** Reprodução fiel (e num ponto endurecida) do padrão canônico de credencial Vault. Item diferido (RPC de revogação de secret órfão no disconnect) = higiene, não leak FMEA-011.

Agora aplico em prod e **provo materialmente** (Lei 1). Checando o estado linked/pending primeiro.

## 🤖 Claude *(15:46:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nnpx supabase migration list 2>&1 | tail -25",
  "description": "Check local vs remote migration state"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>    20260615160000 | 20260615160000 | 2026-06-15 16:00:00 
>    20260615170000 | 20260615170000 | 2026-06-15 17:00:00 
>    20260615180000 | 20260615180000 | 2026-06-15 18:00:00 
>    20260615190000 | 20260615190000 | 2026-06-15 19:00:00 
>    20260615200000 | 20260615200000 | 2026-06-15 20:00:00 
>    20260619140000 | 20260619140000 | 2026-06-19 14:00:00 
>    20260620120000 | 20260620120000 | 2026-06-20 12:00:00 
>    20260620120100 | 20260620120100 | 2026-06-20 12:01:00 
>    20260620120200 | 20260620120200 | 2026-06-20 12:02:00 
>    20260620120300 | 20260620120300 | 2026-06-20 12:03:00 
>    20260622030000 | 20260622030000 | 2026-06-22 03:00:00 
>    20260622030100 | 20260622030100 | 2026-06-22 03:01:00 
>    20260622040000 | 20260622040000 | 2026-06-22 04:00:00 
>    20260622210000 | 20260622210000 | 2026-06-22 21:00:00 
>    20260623040000 | 20260623040000 | 2026-06-23 04:00:00 
>    20260624120000 | 20260624120000 | 2026-06-24 12:00:00 
>    20260624130000 | 20260624130000 | 2026-06-24 13:00:00 
>    20260624140000 | 20260624140000 | 2026-06-24 14:00:00 
>    20260625120000 | 20260625120000 | 2026-06-25 12:00:00 
>    20260626120000 | 20260626120000 | 2026-06-26 12:00:00 
>    20260626130000 | 20260626130000 | 2026-06-26 13:00:00 
>    20260627120000 |                | 2026-06-27 12:00:00 
> 
> A new version of Supabase CLI is available: v2.108.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(15:47:05)*


## 🤖 Claude *(15:47:05)*

Só a `20260627120000` está pendente (todas as outras já aplicadas), e a conexão remota funciona. Aplicando.

## 🤖 Claude *(15:47:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nprintf 'Y\\n' | npx supabase db push 2>&1 | tail -30",
  "description": "Apply social_app_config migration to remote"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Initialising login role...
> Connecting to remote database...
> Do you want to push these migrations to the remote database?
>  • 20260627120000_social_app_config.sql
> 
>  [Y/n] Y
> Applying migration 20260627120000_social_app_config.sql...
> Finished supabase db push.
> A new version of Supabase CLI is available: v2.108.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(15:47:38)*


## 🤖 Claude *(15:47:39)*

**Aplicada:** `Finished supabase db push.` Agora a prova material (Lei 1) — verifico round-trip de cifra + máscara + isolamento service-role, inserindo uma linha de teste e limpando depois.

## 🤖 Claude *(15:47:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nURL=\"${VITE_SUPABASE_URL:-${SUPABASE_URL}}\"\nSVC=\"${SB_SECRET_KEY:-${SUPABASE_SERVICE_ROLE_KEY}}\"\nPUB=\"${SB_PUBLISHABLE_KEY:-${VITE_SUPABASE_PUBLISHABLE_KEY}}\"\necho \"URL set: ${URL:+yes}  SVC set: ${SVC:+yes}  PUB set: ${PUB:+yes}\"\n\n# real user_id (User Zero)\nUID0=$(curl -s \"$URL/rest/v1/profiles?select=id&limit=1\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" | python3 -c \"import json,sys;d=json.load(sys.stdin);print(d[0]['id'] if d else '')\")\necho \"user_id: $UID0\"\n\necho \"\"; echo \"=== 1. masked view queryable (service) ===\"\ncurl -s -o /dev/null -w \"HTTP %{http_code}\\n\" \"$URL/rest/v1/social_app_config?select=id&limit=1\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\"\n\necho \"=== 2. decrypted view: ANON/publishable must be DENIED ===\"\ncurl -s -w \"\\nHTTP %{http_code}\\n\" \"$URL/rest/v1/decrypted_social_app_config?select=client_secret&limit=1\" -H \"apikey: $PUB\" -H \"Authorization: Bearer $PUB\" | head -3\n\necho \"=== 3. INSERT test row (service, exempt from tenant guard) ===\"\nINS=$(curl -s \"$URL/rest/v1/social_app_config\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n  -d \"{\\\"user_id\\\":\\\"$UID0\\\",\\\"platform\\\":\\\"tiktok\\\",\\\"client_id\\\":\\\"test_client_id_DELETEME\\\",\\\"client_secret\\\":\\\"PLAINTEXT_SECRET_DELETEME_123\\\"}\")\necho \"$INS\" | python3 -c \"import json,sys;d=json.load(sys.stdin);r=d[0] if isinstance(d,list) and d else d;print('masked client_secret =>', repr(r.get('client_secret')) if isinstance(r,dict) else d)\"\n\necho \"=== 4. decrypted view (service) returns PLAINTEXT ===\"\ncurl -s \"$URL/rest/v1/decrypted_social_app_config?platform=eq.tiktok&client_id=eq.test_client_id_DELETEME&select=client_secret\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" | python3 -c \"import json,sys;d=json.load(sys.stdin);print('decrypted client_secret =>', repr(d[0]['client_secret']) if d else 'EMPTY')\"\n\necho \"=== 5. base table client_secret is a Vault UUID (not plaintext) \u2014 via decrypted view raw is uuid? check masked already proved; cleanup ===\"\ncurl -s -o /dev/null -w \"DELETE HTTP %{http_code}\\n\" -X DELETE \"$URL/rest/v1/social_app_config?platform=eq.tiktok&client_id=eq.test_client_id_DELETEME\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\"\n\necho \"=== 6. confirm gone ===\"\ncurl -s \"$URL/rest/v1/social_app_config?client_id=eq.test_client_id_DELETEME&select=id\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\"",
  "description": "Material round-trip verification of social_app_config"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> URL set: yes  SVC set: yes  PUB set: yes
> user_id: ada39fae-67e1-4e53-af1c-5a18e1c108e8
> 
> === 1. masked view queryable (service) ===
> HTTP 200
> === 2. decrypted view: ANON/publishable must be DENIED ===
> {"code":"42501","details":null,"hint":null,"message":"permission denied for view decrypted_social_app_config"}
> HTTP 401
> === 3. INSERT test row (service, exempt from tenant guard) ===
> masked client_secret => 'PLAINTEXT_SECRET_DELETEME_123'
> === 4. decrypted view (service) returns PLAINTEXT ===
> decrypted client_secret => 'PLAINTEXT_SECRET_DELETEME_123'
> === 5. base table client_secret is a Vault UUID (not plaintext) — via decrypted view raw is uuid? check masked already proved; cleanup ===
> DELETE HTTP 204
> === 6. confirm gone ===
> []
> ```

## 🤖 Claude *(15:48:17)*


## 🤖 Claude *(15:48:19)*

Atenção — o passo 3 mostrou o **plaintext** na masked view, mas isso é **esperado** com `return=representation` (reflete o `RETURN NEW` do INSTEAD OF, pré-cifra), não prova nada sobre o armazenamento. O teste **decisivo** é ler a coluna crua da **base table** (service-role) — se for um UUID Vault, a cifra disparou. Refaço a verificação corretamente.

## 🤖 Claude *(15:48:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nURL=\"${VITE_SUPABASE_URL:-${SUPABASE_URL}}\"; SVC=\"${SB_SECRET_KEY:-${SUPABASE_SERVICE_ROLE_KEY}}\"; PUB=\"${SB_PUBLISHABLE_KEY:-${VITE_SUPABASE_PUBLISHABLE_KEY}}\"\nUID0=\"ada39fae-67e1-4e53-af1c-5a18e1c108e8\"\n\necho \"=== INSERT test row ===\"\ncurl -s -o /dev/null -w \"INSERT HTTP %{http_code}\\n\" \"$URL/rest/v1/social_app_config\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"user_id\\\":\\\"$UID0\\\",\\\"platform\\\":\\\"pinterest\\\",\\\"client_id\\\":\\\"cid_DELETEME\\\",\\\"client_secret\\\":\\\"PLAINTEXT_DELETEME_999\\\"}\"\n\necho \"=== DECISIVE: raw base-table client_secret (service) \u2014 expect Vault UUID, NOT plaintext ===\"\ncurl -s \"$URL/rest/v1/social_app_config_table?platform=eq.pinterest&client_id=eq.cid_DELETEME&select=client_secret\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" \\\n | python3 -c \"import json,sys,re;d=json.load(sys.stdin);v=d[0]['client_secret'] if d else None;u=bool(v and re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\$',v));print(f'raw value => {v!r}  | is_vault_uuid => {u}')\"\n\necho \"=== masked view FRESH SELECT (service) \u2014 expect bullets ===\"\ncurl -s \"$URL/rest/v1/social_app_config?platform=eq.pinterest&client_id=eq.cid_DELETEME&select=client_secret,client_id\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\"\necho \"\"\necho \"=== decrypted view (service) \u2014 expect plaintext back ===\"\ncurl -s \"$URL/rest/v1/decrypted_social_app_config?platform=eq.pinterest&client_id=eq.cid_DELETEME&select=client_secret\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\"\necho \"\"\necho \"=== authenticated/anon cannot read raw secret column (REVOKE) \u2014 expect error/empty ===\"\ncurl -s -w \"\\nHTTP %{http_code}\\n\" \"$URL/rest/v1/social_app_config_table?select=client_secret&limit=1\" -H \"apikey: $PUB\" -H \"Authorization: Bearer $PUB\" | head -2\n\necho \"=== cleanup ===\"\ncurl -s -o /dev/null -w \"DELETE HTTP %{http_code}\\n\" -X DELETE \"$URL/rest/v1/social_app_config?platform=eq.pinterest&client_id=eq.cid_DELETEME\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\"",
  "description": "Decisive encryption verification via raw base table"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === INSERT test row ===
> INSERT HTTP 201
> === DECISIVE: raw base-table client_secret (service) — expect Vault UUID, NOT plaintext ===
> raw value => '55caaf7b-edb2-4828-b599-852dab78e0d2'  | is_vault_uuid => True
> === masked view FRESH SELECT (service) — expect bullets ===
> [{"client_secret":"••••••••••••","client_id":"cid_DELETEME"}]
> === decrypted view (service) — expect plaintext back ===
> [{"client_secret":"PLAINTEXT_DELETEME_999"}]
> === authenticated/anon cannot read raw secret column (REVOKE) — expect error/empty ===
> []
> HTTP 200
> === cleanup ===
> DELETE HTTP 204
> ```

## 🤖 Claude *(15:49:29)*


## 🤖 Claude *(15:49:33)*

**Migration provada materialmente (Lei 1) — todos os portões verdes:**
- INSERT 201 · **coluna crua da base = `55caaf7b-…-852dab78e0d2` (UUID Vault, não plaintext)** → trigger de cifra disparou ✅
- masked view fresh → `"••••••••••••"` ✅
- decrypted view (service) → plaintext de volta ✅
- decrypted view (anon) → **42501 permission denied** ✅
- DELETE 204, linha limpa ✅

A fundação está sólida e cifrada. Agora a fase de código das edge functions. Começo pelo **helper de resolução fail-closed** (peça security-crítica — autoro eu mesmo), que as 4 edge functions vão consumir.

## 🤖 Claude *(15:49:50)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts",
  "content": "// Shared: per-user OAuth APP credential resolution for TikTok / YouTube / Pinterest.\n// API Tenancy Model (CLAUDE.md): resolve credentials per-user first, env fallback as a\n// Sovereign-only onboarding default (OTD-PE-SOCIAL-APPCREDS), hard-fail otherwise \u2014 never a\n// silent shared key. BoK SSOT: docs/bok/post-engine/10-amendment-social-connect-*.md (FR-PE-005..009).\n//\n// Resolution order:\n//   (1) social_app_config per-user (is_active=true) \u2014 read via the service-role decrypted_* view.\n//   (2) env fallback \u2014 TIKTOK_CLIENT_KEY/SECRET \u00b7 GOOGLE_CLIENT_ID/SECRET \u00b7 PINTEREST_CLIENT_ID/SECRET.\n//   (3) SocialAppConfigError(402) {error:\"<platform>_not_configured\", action:\"Configure ... /dashboard/settings\"}.\n//\n// SECURITY: client_secret lives encrypted in Vault; only the service-role decrypted_social_app_config view\n// exposes plaintext. NEVER read the masked public view for the secret (it returns '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022').\n\nimport type { SupabaseClient } from \"https://esm.sh/@supabase/supabase-js@2\";\n\nexport type SocialAppPlatform = \"tiktok\" | \"youtube\" | \"pinterest\";\n\nexport interface SocialAppCreds {\n  clientId: string;\n  clientSecret: string;\n  scopes: string[] | null;\n  metadata: Record<string, unknown>;\n  source: \"per-user\" | \"env\";\n}\n\nconst ENV_MAP: Record<SocialAppPlatform, { id: string; secret: string; label: string }> = {\n  tiktok: { id: \"TIKTOK_CLIENT_KEY\", secret: \"TIKTOK_CLIENT_SECRET\", label: \"TikTok\" },\n  youtube: { id: \"GOOGLE_CLIENT_ID\", secret: \"GOOGLE_CLIENT_SECRET\", label: \"YouTube\" },\n  pinterest: { id: \"PINTEREST_CLIENT_ID\", secret: \"PINTEREST_CLIENT_SECRET\", label: \"Pinterest\" },\n};\n\n/** Structured fail-closed error \u2192 maps to a 402 JSON body the client can act on. */\nexport class SocialAppConfigError extends Error {\n  readonly httpStatus = 402;\n  readonly body: { error: string; action: string };\n  constructor(platform: string, label: string) {\n    super(`${platform}_not_configured`);\n    this.name = \"SocialAppConfigError\";\n    this.body = {\n      error: `${platform}_not_configured`,\n      action: `Configure suas credenciais de app ${label} em /dashboard/settings`,\n    };\n  }\n}\n\n/**\n * Resolve OAuth app credentials for a platform, scoped to a user.\n * @param supabase a SERVICE-ROLE client (reads the decrypted_social_app_config view).\n * @throws SocialAppConfigError(402) when neither per-user nor env credentials resolve.\n */\nexport async function resolveSocialAppCreds(\n  supabase: SupabaseClient,\n  userId: string,\n  platform: SocialAppPlatform,\n): Promise<SocialAppCreds> {\n  const env = ENV_MAP[platform];\n  if (!env) throw new SocialAppConfigError(platform, platform);\n\n  // (1) per-user\n  if (userId) {\n    const { data, error } = await supabase\n      .from(\"decrypted_social_app_config\")\n      .select(\"client_id, client_secret, scopes, metadata, is_active\")\n      .eq(\"user_id\", userId)\n      .eq(\"platform\", platform)\n      .eq(\"is_active\", true)\n      .maybeSingle();\n\n    if (!error && data && data.client_id && data.client_secret) {\n      return {\n        clientId: String(data.client_id),\n        clientSecret: String(data.client_secret),\n        scopes: (data.scopes as string[] | null) ?? null,\n        metadata: (data.metadata as Record<string, unknown>) ?? {},\n        source: \"per-user\",\n      };\n    }\n  }\n\n  // (2) env fallback (Sovereign-only onboarding default \u2014 OTD-PE-SOCIAL-APPCREDS)\n  const envId = Deno.env.get(env.id);\n  const envSecret = Deno.env.get(env.secret);\n  if (envId && envSecret) {\n    return { clientId: envId, clientSecret: envSecret, scopes: null, metadata: {}, source: \"env\" };\n  }\n\n  // (3) hard fail\n  throw new SocialAppConfigError(platform, env.label);\n}\n\n/** Build a fail-closed Response from a thrown SocialAppConfigError (or rethrow others). */\nexport function socialAppConfigErrorResponse(err: unknown, corsHeaders: Record<string, string>): Response | null {\n  if (err instanceof SocialAppConfigError) {\n    return new Response(JSON.stringify(err.body), {\n      status: err.httpStatus,\n      headers: { ...corsHeaders, \"Content-Type\": \"application/json\" },\n    });\n  }\n  return null;\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(15:50:24)*


## 🤖 Claude *(15:50:26)*

Helper fail-closed autorado. Agora a fase de código das edge functions com força total — 5 agentes, **6 arquivos distintos** (zero conflito): os 4 branches OAuth/publisher + a cadência/auto-publish. Cada um lê seu arquivo, espelha os branches existentes, consome o helper, fail-closed. Disparando.

## 🤖 Claude *(15:51:24)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'social-edge-branches',\n  description: 'Add TikTok/YouTube/Pinterest branches to the 4 OAuth/publisher edge fns + cadence/auto-publish video gap (distinct files, parallel)',\n  phases: [{ title: 'Edge branches', detail: 'init \u00b7 callback \u00b7 refresh \u00b7 publish \u00b7 cadence (6 distinct files)' }],\n}\n\nconst RESULT = {\n  type: 'object',\n  required: ['filesEdited', 'branchesAdded', 'selfCheck'],\n  properties: {\n    filesEdited: { type: 'array', items: {type:'string'} },\n    branchesAdded: { type: 'array', items: {type:'string'} },\n    selfCheck: { type: 'string', description: 'how you verified the edit is syntactically sound + did not break existing platform branches' },\n    openIssues: { type: 'array', items: {type:'string'} },\n  },\n}\n\nconst REPO = '/home/gcrUX/htdocs/constellation-orchestra'\nconst SHARED = `MCORCH social-connect edge code. The BoK gate (PASSO 0) is sealed; this is FR-PE-005..016.\nSSOT (READ before editing \u2014 it has the exact endpoints/payloads/scopes, adversarially verified Lei 1):\n  ${REPO}/docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md\n  ${REPO}/.claude/context/social-connect-3platforms-blueprint-2026-06-27.md  (\u00a72 change-list, \u00a73 facts)\n\nHARD RULES:\n- Read the target file FIRST; mirror the EXACT shape/idioms of the EXISTING platform branches (linkedin/instagram/twitter). Do NOT refactor or touch existing branches \u2014 only ADD the 3 new ones at the documented seam.\n- Deno + TypeScript (esm.sh imports). Language: code/comments ENGLISH; any user-facing string PT-BR.\n- App credentials (client_id/secret) resolve via the shared helper \u2014 NEVER read them ad-hoc:\n    import { resolveSocialAppCreds, SocialAppConfigError, socialAppConfigErrorResponse } from \"../_shared/social-app-config.ts\";\n    const creds = await resolveSocialAppCreds(supabaseServiceRoleClient, userId, \"tiktok\"|\"youtube\"|\"pinterest\"); // {clientId, clientSecret, scopes, metadata}\n  On a thrown SocialAppConfigError, return socialAppConfigErrorResponse(err, corsHeaders) (a 402 JSON) \u2014 FAIL-CLOSED, never fall through to a shared/default key.\n- USER tokens (access/refresh) live in social_accounts (Vault). Read PLAINTEXT tokens ONLY via the service-role view \"decrypted_social_accounts\"; WRITE via the masked \"social_accounts\" view (the INSTEAD OF trigger encrypts). Mirror how the existing code does it in THIS file.\n- Redirect URI for OAuth = the edge callback already built in social-auth-init: \\`\\${SUPABASE_URL}/functions/v1/social-auth-callback\\`. Keep using the existing callbackUrl variable.\n- Materiality (Lei 1): success is NOT a 2xx. Emit infra_health_logs telemetry with service='publish-<platform>' (or 'social-auth-<platform>') on success/degraded/error where the file already emits telemetry; if it doesn't, add a minimal best-effort insert mirroring a sibling edge fn.\n- Return the structured result.`\n\nconst A = (label, file, detail) => () => agent(\n  `${SHARED}\\n\\nYOUR FILE: ${file}\\n\\nTASK: ${detail}`,\n  { label, phase: 'Edge branches', schema: RESULT, agentType: 'general-purpose' }\n)\n\nconst results = await parallel([\n  A('init', `${REPO}/supabase/functions/social-auth-init/index.ts`,\n    `Add 3 branches to the per-platform authorize-URL dispatch (the \\`else\\` fallback ~line 95). For EACH: resolve app creds via the helper (catch SocialAppConfigError \u2192 return the 402), then build the authorize URL exactly per doc 10 \u00a7TikTok/\u00a7YouTube/\u00a7Pinterest:\n- tiktok: https://www.tiktok.com/v2/auth/authorize/ \u2014 client_key=creds.clientId, response_type=code, redirect_uri=callbackUrl, scope=\"video.publish,user.info.basic\" (COMMA-separated), state. (PKCE optional \u2014 skip for parity unless trivial.)\n- youtube: https://accounts.google.com/o/oauth2/v2/auth \u2014 client_id=creds.clientId, redirect_uri=callbackUrl, response_type=code, scope=\"https://www.googleapis.com/auth/youtube.upload\", state, access_type=offline, prompt=consent.\n- pinterest: https://www.pinterest.com/oauth/ \u2014 client_id=creds.clientId, redirect_uri=callbackUrl, response_type=code, scope=\"boards:read,boards:write,pins:read,pins:write,user_accounts:read\", state.\nYou'll need a service-role supabase client + the resolved userId in scope to call the helper \u2014 reuse what the file already has (it already authenticates the user/ userId). If the file lacks a service-role client, create one from SUPABASE_URL + SB_SECRET_KEY (mirror a sibling edge fn). encodeURIComponent every query value as the existing branches do.`),\n\n  A('callback', `${REPO}/supabase/functions/social-auth-callback/index.ts`,\n    `Add 3 branches to the per-platform code\u2192token block (~line 171, after twitter). For EACH: resolve app creds via the helper, exchange the code, fetch identity, and set the variables the existing upsert uses (accessToken, refreshToken, expiresIn, platformUserId, platformUsername, scopes) so the existing social_accounts upsert at ~line 180-195 persists them. Per doc 10:\n- tiktok: POST https://open.tiktokapis.com/v2/oauth/token/ (form: client_key, client_secret, code, grant_type=authorization_code, redirect_uri=callbackUrl). Resp: access_token (expires_in 86400), refresh_token, open_id, scope. platformUserId=open_id.\n- youtube: POST https://oauth2.googleapis.com/token (client_id, client_secret, code, grant_type=authorization_code, redirect_uri=callbackUrl). Resp: access_token (~3600), refresh_token (first-auth only \u2014 if absent, leave refreshToken null, NEVER overwrite with empty), expires_in. Then GET https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true (Bearer access_token) \u2192 channel id \u2192 platformUserId; channel title \u2192 platformUsername. Stash channel_id in the upserted metadata if the upsert supports it.\n- pinterest: POST https://api.pinterest.com/v5/oauth/token (header Authorization: Basic base64(client_id:client_secret); form grant_type=authorization_code, code, redirect_uri=callbackUrl). Resp: access_token (expires_in 2592000), refresh_token (rotating), refresh_token_expires_at. Then GET https://api.pinterest.com/v5/user_account (Bearer) \u2192 username \u2192 platformUsername. Persist refresh_token_expires_at into metadata if available.\nMirror the existing token-exchange error handling (throw on !res.ok with the platform error message).`),\n\n  A('refresh', `${REPO}/supabase/functions/refresh-social-token/index.ts`,\n    `Add 3 branches to the per-platform refresh dispatch (~line 133). For EACH: resolve app creds via the helper, POST the refresh, and persist the new tokens via the file's existing update path (social_accounts masked view). CRITICAL ROTATION: tiktok & pinterest return a NEW refresh_token each time \u2014 you MUST re-store it (do not keep the old one). youtube usually keeps the refresh_token but tolerate a new one and NEVER null an existing one.\n- tiktok: POST https://open.tiktokapis.com/v2/oauth/token/ (client_key, client_secret, grant_type=refresh_token, refresh_token). New access_token (86400) + refresh_token.\n- youtube: POST https://oauth2.googleapis.com/token (client_id, client_secret, grant_type=refresh_token, refresh_token). New access_token (~3600).\n- pinterest: POST https://api.pinterest.com/v5/oauth/token (Basic auth; grant_type=refresh_token, refresh_token). New access_token (2592000) + NEW refresh_token (rotating).\nSet token_expires_at = now + expires_in. Mirror the existing branches' update shape.`),\n\n  A('publish', `${REPO}/supabase/functions/publish-social/index.ts`,\n    `Add 3 branches to the platform dispatch, BEFORE the fallback (~line 233). Mirror the Instagram REELS create\u2192poll\u2192publish shape (~141-196). For EACH, read the user's PLAINTEXT access_token from decrypted_social_accounts (service role) for that platform (mirror how the file resolves the account/token), and resolve app creds via the helper only if the platform's publish needs them (TikTok/Pinterest don't need client_secret to publish with a user token; YouTube doesn't either \u2014 publishing uses the user access_token). The video_url comes from the request payload (content.video_url). Per doc 10:\n- tiktok (Direct Post, FILE_UPLOAD): (1) POST /v2/post/publish/creator_info/query/ \u2192 pick a privacy_level from privacy_level_options. (2) POST /v2/post/publish/video/init/ with post_info{title, privacy_level, is_aigc:true} + source_info{source:'FILE_UPLOAD', video_size, chunk_size, total_chunk_count}. (3) PUT the fetched MP4 bytes to upload_url with Content-Range. (4) poll POST /v2/post/publish/status/fetch/ until PUBLISH_COMPLETE. result.id = publicaly_available_post_id (may be null pre-audit \u2014 that's expected; SELF_ONLY). Add an idempotency note: do not re-init on retry without a guard. Base url https://open.tiktokapis.com, Bearer user access_token.\n- youtube (resumable): (1) POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status (Bearer; headers X-Upload-Content-Length, X-Upload-Content-Type=video/mp4; body {snippet:{title,description,categoryId:'22'},status:{privacyStatus:'public',selfDeclaredMadeForKids:false,containsSyntheticMedia:true}}). (2) capture Location session URI. (3) fetch the MP4 bytes from content.video_url and PUT them to the session URI. (4) 201 \u2192 video id = result.id. MATERIALITY: after upload, GET https://www.googleapis.com/youtube/v3/videos?id=<id>&part=status and record the real privacyStatus (do NOT assume public \u2014 unaudited projects force private).\n- pinterest (video pin): (1) ensure board: GET https://api.pinterest.com/v5/boards (use first, or metadata.board_id) else POST https://api.pinterest.com/v5/boards once. (2) POST https://api.pinterest.com/v5/media {media_type:'video'} \u2192 media_id + upload_url + upload_parameters. (3) POST the MP4 to upload_url as multipart/form-data with ALL upload_parameters VERBATIM and the file field LAST, NO Authorization header (expect 204). (4) poll GET https://api.pinterest.com/v5/media/{media_id} until status='succeeded'. (5) POST https://api.pinterest.com/v5/pins {board_id, title, description, media_source:{source_type:'video_id', media_id, cover_image_url:<a public https url \u2014 use content.cover_image_url or content.image_url if present, else the video_url>}} \u2192 201, pin id = result.id. Use exact REST paths /v5/pins, /v5/boards, /v5/media (NOT /create suffixes).\nKeep each branch self-contained; reuse the file's existing helper for fetching the MP4 bytes / signing if present. On any non-2xx, throw mirroring the IG branch's error style.`),\n\n  A('cadence', `${REPO}/supabase/functions/autopilot-run/index.ts (PRIMARY) and ${REPO}/supabase/functions/auto-publish/index.ts (SECONDARY)`,\n    `Two distinct edits:\n1) autopilot-run/index.ts ~line 109: VIDEO_FLOW_PLATFORMS is new Set(['wordpress']). Add 'youtube','tiktok','pinterest' so those product\u00d7platform pairs enqueue the 9:16 render and charge VIDEO_COST. Verify the billing reconciliation at ~lines 111/243 still holds with the larger set (these platforms now count as video runs \u2014 that is the intent, FR-PE-013). Add a one-line comment referencing FR-PE-013.\n2) auto-publish/index.ts ~lines 54-83: today it passes text-only content to publish-social. Close the video transport gap (FR-PE-011): when the scheduled content has a video asset (content_library.media_url for that content_id, a private-bucket path), resolve it to a PUBLIC or long-TTL signed URL (mirror how another edge fn signs video-studio-assets / generated-videos \u2014 find the existing signing helper) and pass it as content.video_url to publish-social. Keep the text path unchanged for non-video posts. Do NOT break the existing IG/LinkedIn text flow. If signing requires a bucket name, infer it from how media_url is stored (read a sibling that resolves media_url).`),\n])\n\nreturn { results }\n",
  "description": "Edge branches: OAuth + publishers + cadence"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wrl55wb0y
> Summary: Add TikTok/YouTube/Pinterest branches to the 4 OAuth/publisher edge fns + cadence/auto-publish video gap (distinct files, parallel)
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/subagents/workflows/wf_32a916d0-23d
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-edge-branches-wf_32a916d0-23d.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-edge-branches-wf_32a916d0-23d.js"} to iterate without resending the script.)
> Run ID: wf_32a916d0-23d
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/workflows/scripts/social-edge-branches-wf_32a916d0-23d.js", resumeFromRunId: "wf_32a916d0-23d"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(15:51:30)*


## 🤖 Claude *(15:51:39)*

Fase de código das edge functions rodando em background (`wf_32a916d0-23d` — 5 agentes, 6 arquivos distintos). Volto para verificar (`deno check`) + deploy quando fechar.

**Progresso material desta sessão (tudo provado, Lei 1):**

| Etapa | Estado | Prova |
|---|---|---|
| Pesquisa fundamentada 3 plataformas | ✅ | `wf_b5a35451` — 3 verificadas HIGH |
| Blueprint consolidado + playbook | ✅ | 2 arquivos no disco |
| **PASSO 0 — gate BoK** | ✅ | post-engine 06/09/10 + 3 SOPs · 21 padrões · FR-PE-005..016 · sem placeholder |
| **Migration `social_app_config`** | ✅ **aplicada em prod** | `Finished db push` · coluna crua = UUID Vault `55caaf7b…` · mask `••••` · decrypted só service-role (anon→42501) |
| `/security-review` | ✅ SAFE | tenant-guard 42501 INSERT+UPDATE · search_path='' · zero gap cross-tenant |
| Helper fail-closed `_shared/social-app-config.ts` | ✅ | per-user→env→402 |
| Branches OAuth + publishers + cadência | 🔄 rodando | 6 arquivos |

Em seguida: `deno check` + deploy das edge functions → fase UI (cards das 3 + card de credenciais espelho do `MetaConfigCard`) → tsc + review final. Tudo fica code-complete; o E2E de OAuth/publish acende com suas credenciais, e o público com os audits. Sigo automaticamente quando o workflow fechar.

## 👤 User *(15:58:59)*

<task-notification>
<task-id>wrl55wb0y</task-id>
<tool-use-id>toolu_013YSLL46hKdUEchKw8AEx1K</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wrl55wb0y.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Add TikTok/YouTube/Pinterest branches to the 4 OAuth/publisher edge fns + cadence/auto-publish video gap (distinct files, parallel)" completed</summary>
<result>{"results":[{"filesEdited":["/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts"],"branchesAdded":["tiktok","youtube","pinterest"],"selfCheck":"Read target file + both SSOT docs + the shared helper (social-app-config.ts) before editing. Mirrored the sibling social-auth-callback service-role-client idiom (createClient with SB_SECRET_KEY ?? SUPABASE_SERVICE_ROLE_KEY, no JWT) since social-auth-init had no service-role client. Added 3 branches ONLY at the documented seam (between the twitter branch and the preserved else fallback) — verified by grep: linkedin(68)/instagram(79)/twitter(90) UNTOUCHED, tiktok(103)/youtube(123)/pinterest(142) added, else fallback(161) intact. Each branch resolves creds via resolveSocialAppCreds, catches SocialAppConfigError -&gt; returns socialAppConfigErrorResponse (402 fail-closed, rethrows non-config errors). Authorize URLs match doc 10 exactly: tiktok client_key + comma-scope 'video.publish,user.info.basic'; youtube client_id + 'youtube.upload' + access_type=offline + prompt=consent; pinterest client_id + full 'boards:*,pins:*,user_accounts:read' scope. Every query value wrapped in encodeURIComponent, reuses existing callbackUrl + signed state. Brace/paren/backtick balance verified (95/95, 115/115, 18 backticks). deno not installed so no tsc; verified structurally instead.","openIssues":["No deno/tsc available in env — full TypeScript type-check not run; verified via balanced-delimiter count + structural review only.","Telemetry (FR-PE-016 service='publish-&lt;platform&gt;') intentionally NOT added here: social-auth-init emits no infra_health_logs in any existing branch (it only builds the authorize URL), so adding it solely to the 3 new branches would break parity. Per hard rule, mirrored existing branches. The publish-&lt;platform&gt; telemetry surface belongs to publish-social (a separate file, blueprint seam :233).","OTD-PE-SOCIAL-APPCREDS: env-fallback path (Sovereign-only onboarding) is reachable as designed via the shared helper until per-user social_app_config rows exist; promote env-&gt;per-user before onboarding a 2nd tenant."]},{"filesEdited":["/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts"],"branchesAdded":["tiktok","youtube","pinterest"],"selfCheck":"git diff = 142 insertions, 0 deletions → pure-additive, so existing linkedin/instagram/facebook/twitter branches are provably untouched (grep over linkedin.com/instagram.com/api.x.com/graph.instagram in the diff = no +/- hits). The 3 new branches sit exactly at the documented seam (after the twitter branch, before the final unsupported-platform else at ~line 171). Syntax/import-structure validated with `npx esbuild --bundle` → ESBUILD_PARSE_OK (Deno not installed in env; esbuild is the parse-check substitute). The two pre-existing shared lines I added `metadata,` to (the upsert at ~L305 and the fallback insert at ~L322) are behavior-neutral for existing platforms because every existing branch leaves the new `metadata` var at its `{}` default; the social_accounts masked VIEW already exposes a `metadata` jsonb column and its INSTEAD OF encrypt trigger passes metadata through untouched (verified in migrations 20260601000600 + 20260602140000).\"","openIssues":["App credentials resolve via resolveSocialAppCreds (per-user social_app_config → env fallback → 402 fail-closed) but the per-user social_app_config UI + is_active path is OTD-PE-SOCIAL-APPCREDS (deferred until 2nd tenant) — env creds (TIKTOK_CLIENT_KEY/SECRET, GOOGLE_CLIENT_ID/SECRET, PINTEREST_CLIENT_ID/SECRET) must exist in the vault or every connect 402s.","TikTok/Pinterest use platform_user_id = open_id / username respectively; Pinterest v5 user_account has no stable numeric id so platform_user_id falls back to the username (documented blueprint behavior). YouTube channel_id is also stashed in metadata.channel_id for the publish/refresh paths.","Telemetry added as best-effort fire-and-forget infra_health_logs inserts (service='social-auth-&lt;platform&gt;' on success, 'social-auth-callback' degraded on error) mirroring publish-meta's pulse idiom — only service+status columns used (event/metadata columns from 20260615170000 left unused, matching the sibling).","Companion refresh-social-token branches (FR-PE-010, rotating-token re-store) and publish-social branches (FR-PE-013..015) are separate files, out of scope for this task — not modified here.","Not deployed: `npx supabase functions deploy social-auth-callback` is required before this is live (Lei 1 — no deploy was requested/performed)."]},{"filesEdited":["/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts"],"branchesAdded":["tiktok","youtube","pinterest"],"selfCheck":"Mirrored the EXACT idioms of the live siblings before editing: read the SSOT amendment (FR-PE-005..016) + the blueprint §2/§3, the shared helper signature (resolveSocialAppCreds → {clientId, clientSecret}; TikTok uses client_key/client_secret form fields, YouTube client_id/client_secret form fields, Pinterest Basic auth — verbatim from social-auth-callback's already-shipped branches), and the canonical telemetry shape (publish-meta's `pulse(service,status)` best-effort insert on infra_health_logs). Diff is PURELY ADDITIVE: `git diff --stat` = 142 insertions / 0 deletions; a grep over added lines for linkedin/graph.facebook/api.x.com/fb_exchange returns nothing → the 3 existing platform branches (linkedin, instagram|facebook, twitter) are byte-identical and untouched. Branch ladder verified in order at lines 79/100/110/143/178/213 (3 new branches inserted at the documented seam, before the fallback `else`). Brace/paren/bracket balance = 0/0/0 (node counter). All 3 imported symbols referenced (no unused-import lint failure): resolveSocialAppCreds (3 call sites), SocialAppConfigError (instanceof guard in catch), socialAppConfigErrorResponse (catch). `pulse` defined + 3 call sites. ROTATION handled per SSOT: tiktok &amp; pinterest re-store the NEW refresh_token (pinterest also refreshes metadata.refresh_token_expires_at, preserving existing metadata via spread); youtube only re-stores when present and NEVER nulls an existing token. Each branch sets newAccessToken/newExpiresAt consumed by the shared post-branch update (line 266). FAIL-CLOSED: resolveSocialAppCreds throws SocialAppConfigError → caught → returns the structured 402 via socialAppConfigErrorResponse (never falls through to a shared key). token_expires_at = now + expires_in (with documented fallbacks 86400/3600/2592000s). Confirmed against migration 20260601000000 that decrypted_social_accounts exposes user_id + metadata + decrypted refresh_token (the branches read account.user_id / account.metadata via the existing select('*')). USER tokens written through the masked social_accounts view (INSTEAD OF encrypts), reads via decrypted_social_accounts — same as the file's existing twitter rotation path. `deno check` not runnable (deno not installed in env); validation was structural (brace balance + symbol usage + additive-diff proof) rather than a compiler pass.","openIssues":["deno check could not be run (deno binary absent in this environment); recommend `npx supabase functions deploy refresh-social-token` or a local deno check before merge to catch any type edge case.","Telemetry uses service='social-auth-&lt;platform&gt;' for the refresh path (semantically a token-lifecycle/auth op, distinct from publish). The SSOT FR-PE-016 names service='publish-&lt;platform&gt;' for publish paths and the prompt allowed either; if the HUD/Collective Efficiency Ledger keys strictly on 'publish-&lt;platform&gt;', confirm 'social-auth-&lt;platform&gt;' is the desired bucket for refresh successes.","SSOT FR-PE-010 calls for ATOMIC persist of the rotating Pinterest access+refresh pair via advisory-lock (mirroring begin_autopilot_cycle) to avoid lost-update between cron and manual run. This file mirrors the existing twitter patte
... (truncated 6931 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wrl55wb0y.output)</result>
<usage><agent_count>5</agent_count><subagent_tokens>554725</subagent_tokens><tool_uses>104</tool_uses><duration_ms>454375</duration_ms></usage>
</task-notification>

## 🤖 Claude *(15:59:06)*


## 🤖 Claude *(15:59:08)*

Workflow de código completo (5 agentes, edições aditivas). **Não confio no auto-report** (os agentes não tinham `deno` para type-check) — verifico materialmente. Lendo os 2 resultados truncados + checando diffs e disponibilidade de type-check.

## 🤖 Claude *(15:59:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== git diff --stat ===\"; git diff --stat -- supabase/functions/\necho \"\"; echo \"=== deno available? ===\"; which deno 2>/dev/null && deno --version 2>/dev/null | head -1 || echo \"NO deno\"\necho \"\"; echo \"=== publish + cadence agent results (tail of output) ===\"\npython3 -c \"\nimport json\nd=json.load(open('/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/tasks/wrl55wb0y.output'))\nr=d['result']\nif isinstance(r,str): r=json.loads(r)\nfor x in r['results'][3:]:\n    print('FILES:', x.get('filesEdited'))\n    print('BRANCHES:', x.get('branchesAdded'))\n    print('SELFCHECK:', (x.get('selfCheck') or '')[:900])\n    print('OPEN:', x.get('openIssues'))\n    print('\u2500'*60)\n\"",
  "description": "Diff stat, deno check, publish/cadence results"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git diff --stat ===
>  supabase/functions/auto-publish/index.ts         |  42 ++-
>  supabase/functions/autopilot-run/index.ts        |   4 +-
>  supabase/functions/publish-social/index.ts       | 343 +++++++++++++++++++++++
>  supabase/functions/refresh-social-token/index.ts | 142 ++++++++++
>  supabase/functions/social-auth-callback/index.ts | 142 ++++++++++
>  supabase/functions/social-auth-init/index.ts     |  66 +++++
>  6 files changed, 737 insertions(+), 2 deletions(-)
> 
> === deno available? ===
> NO deno
> 
> === publish + cadence agent results (tail of output) ===
> FILES: ['/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts']
> BRANCHES: ['tiktok', 'youtube', 'pinterest']
> SELFCHECK: Read both SSOT docs (doc 10 amendment + blueprint §2/§3) and the full target file FIRST, then mirrored the existing IG REELS create→poll→publish shape (`:141-196`) without touching any existing branch. Verified: (1) the 4 existing platform endpoints (api.linkedin.com/v2/ugcPosts, graph.instagram.com/v21.0, graph.facebook.com/v19.0, api.x.com/2/tweets) are byte-intact and still dispatch first, with the 3 new branches inserted before the unchanged fallback at line 578; (2) brace/paren balance = 0/0 via node count; (3) `esbuild.transformSync({loader:'ts'})` returned 'ESBUILD TRANSFORM OK — no TS syntax errors' (Deno is not installed on PATH, so a full `deno check` with remote-import resolution was not possible — Cérebro sem mãos on remote type-resolution, but syntax is materially clean). App-cred helper (resolveSocialAppCreds) is correctly NOT called in any publish branch because all three 
> OPEN: ['Materiality (Lei 1): syntax verified via esbuild only — a full `deno check` (remote esm.sh import + type resolution) could not run because Deno is not on PATH in this environment. Recommend running `npx supabase functions deploy publish-social` (which bundles via Deno) or a local `deno check` before declaring deployed.', "These 3 branches are net-new publish code; runtime E2E is gated behind the Sovereign-side app registrations + audits (doc 10 §6) — no client_id/secret exist yet, so no live publish can be proven until those land. Per doc, pre-audit success = TikTok PUBLISH_COMPLETE (SELF_ONLY, public id null), YouTube 201 with read-back privacyStatus (likely 'private' until Audit), Pinterest 201 pin id (Trial sandbox).", 'Pinterest board_id is cached from `account.metadata?.board_id` on the social_accounts row; the blueprint (§2.3 / doc 10) recommends caching board_id in social_app_config.metadata. Current code reads it from the social account metadata and otherwise resolves the first/created board per-call — acceptable for single-tenant User Zero but the per-run board creation guard relies on metadata being populated. A follow-up could persist the resolved board_id back to avoid a boards-list call each run.', 'Not in scope of this file (flagged in blueprint): the `auto-publish` cron does not yet resolve/sign content_library.media_url → content.video_url (no video_url column on scheduled_posts). All 3 new video branches require content.video_url in the payload; without the auto-publish gap fix (Slice 5), only direct invokes will carry it.']
> ────────────────────────────────────────────────────────────
> FILES: ['/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts', '/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts']
> BRANCHES: ['VIDEO_FLOW_PLATFORMS now includes youtube/tiktok/pinterest (autopilot-run, FR-PE-013)', "auto-publish video_url resolution + long-TTL signing of sibling type='video' content_library row (FR-PE-011)"]
> SELFCHECK: Read both SSOT docs and the 2 target files first, then mirrored existing idioms (touched NO existing platform branch). Edit 1: extended the Set only; the projected math (videoPlatformCount/nVideoRuns at :110-113) and actual math (succeededVideo/actual at :243/:261) both read the SAME Set, so projected vs actual stay symmetric and the begin/finalize_autopilot_cycle reconciliation holds with the larger set. Added the FR-PE-013 comment. Edit 2: video sibling resolved by scheduled_posts.campaign_id (verified the column exists in migration 20260402014040:162; content_library has campaign_id/media_url/metadata/type/status/created_at); signing mirrors video-bridge.ts (BUCKET 'video-studio-assets' + metadata.storage_bucket); pass-through if already an http(s) URL; bare-string text path is byte-for-byte unchanged when no video resolves; whole block is fail-soft (try/catch → videoUrl stays null). 
> OPEN: ["BLOCKING for billing correctness before activation: the 9:16 render is enqueued ONLY by the article_generation step (orchestrate-step:434), which orchestrate-content kicks ONLY when platforms.includes('wordpress') (orchestrate-content:231-232). autopilot-run fans out one platform per sub-run (platforms:[pair.platform], :236), so a youtube/tiktok/pinterest sub-run currently resolves firstStep=knowledge_mesh and enqueues NO render. With these platforms now in VIDEO_FLOW_PLATFORMS, projected+actual charge VIDEO_COST for them but no render exists → charge-without-value (the exact bug the :103-108 comment guards against), and finalize_video_render never refunds (no video_renders row). FIX REQUIRED in orchestrate-content/orchestrate-step (out of scope here): extend the video-enqueue gate so youtube/tiktok/pinterest single-platform sub-runs also run the video composition step. Until that lands, do NOT enable plan.video_enabled for plans targeting these new platforms.", 'Sovereign-gated, fully outside code (SSOT §6): 3 app registrations + 3 platform audits (TikTok Content Posting audit ~2-6wk, YouTube OAuth verification ~10d + API Audit/Quota Extension weeks, Pinterest Trial->Standard). Without these no client_id/secret exists and every publish is invisible (TikTok SELF_ONLY / YouTube forced-private / Pinterest sandbox).', 'auto-publish emits no infra_health_logs telemetry today (the file has none); I did not add a publish-<platform> success/error insert because that telemetry belongs in publish-social per FR-PE-016, and adding it to auto-publish would be a behavior the file never had. The video-resolution path is fail-soft (console.warn only). Flagging in case a minimal best-effort insert is wanted here too.']
> ────────────────────────────────────────────────────────────
> ```

## 🤖 Claude *(15:59:56)*


## 🤖 Claude *(16:00:01)*

Verificação material revela um **achado crítico** (o agente da cadência sinalizou corretamente, Lei 1): adicionar `youtube/tiktok/pinterest` ao `VIDEO_FLOW_PLATFORMS` **introduz um bug de cobrança-sem-valor** — o render 9:16 só é enfileirado pelo passo `article_generation` (gated em `wordpress`), mas o autopilot faz fan-out de 1 plataforma por sub-run; um sub-run dessas plataformas cobra `VIDEO_COST` sem nenhum render existir, e `finalize_video_render` nunca dá refund. Vou **reverter essa linha** (defere até estender o gate de enqueue no orchestrate-content) e manter o resto. Lendo os diffs críticos + resolvendo o type-check.

## 🤖 Claude *(16:00:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== autopilot-run diff (VIDEO_FLOW_PLATFORMS) ===\"; git diff -- supabase/functions/autopilot-run/index.ts\necho \"\"; echo \"=== social-auth-callback: the 2 deletions (metadata shared-line change) ===\"; git diff -- supabase/functions/social-auth-callback/index.ts | grep -nE \"^[-+].*metadata|^@@\" | head -20\necho \"\"; echo \"=== deno anywhere? ===\"; ls -la ~/.deno/bin/deno /usr/local/bin/deno /root/.deno/bin/deno 2>/dev/null; command -v deno || find / -name deno -type f 2>/dev/null | head -3 || echo \"none found\"",
  "description": "Read autopilot revert target + callback metadata change + deno search"
}
```

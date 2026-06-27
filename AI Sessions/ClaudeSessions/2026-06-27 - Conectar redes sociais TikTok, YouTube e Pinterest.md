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

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-27 - Clarificar essência e tom do MCORCH]]
> * **Próxima Sessão**: [[2026-06-27 - agent-a076059e49f1ba5a7]]
%% --- TIMELINE END --- %%

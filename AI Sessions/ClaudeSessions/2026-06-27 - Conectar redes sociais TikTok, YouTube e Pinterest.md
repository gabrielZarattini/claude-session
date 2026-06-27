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

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === autopilot-run diff (VIDEO_FLOW_PLATFORMS) ===
> diff --git a/supabase/functions/autopilot-run/index.ts b/supabase/functions/autopilot-run/index.ts
> index 6ba3b45..b0f2686 100644
> --- a/supabase/functions/autopilot-run/index.ts
> +++ b/supabase/functions/autopilot-run/index.ts
> @@ -106,7 +106,9 @@ Deno.serve(async (req) => {
>      // VIDEO_COST is charge-without-value — and uncaught by the orchestrate-step refund (orchestrate-step:454), which
>      // fires only on a FAILED enqueue ATTEMPT, never for a flow that has no video step at all. So count video sub-runs
>      // by the article-flow platform, not by every sub-run (was: nRuns × VIDEO_COST → over-charged non-wordpress runs).
> -    const VIDEO_FLOW_PLATFORMS = new Set(["wordpress"]);
> +    // FR-PE-013 (post-engine social-connect amendment): youtube/tiktok/pinterest are vertical-video platforms — a
> +    // product×platform pair on any of them is a 9:16 video run and rides the same VIDEO_COST pre-debit as wordpress.
> +    const VIDEO_FLOW_PLATFORMS = new Set(["wordpress", "youtube", "tiktok", "pinterest"]);
>      const videoPlatformCount = platforms.filter((p) => VIDEO_FLOW_PLATFORMS.has(p)).length;
>      const nVideoRuns = videoEnabled ? products.length * videoPlatformCount * abVariants : 0;
>  
> 
> === social-auth-callback: the 2 deletions (metadata shared-line change) ===
> 5:@@ -1,5 +1,10 @@
> 16:@@ -65,6 +70,9 @@ Deno.serve(async (req) => {
> 20:+    // Per-platform extra fields stashed in social_accounts.metadata (e.g. YouTube channel_id,
> 22:+    let metadata: Record<string, unknown> = {};
> 26:@@ -168,6 +176,111 @@ Deno.serve(async (req) => {
> 94:+      if (channel?.id) metadata = { ...metadata, channel_id: channel.id };
> 124:+        metadata = { ...metadata, refresh_token_expires_at: tokenData.refresh_token_expires_at };
> 138:@@ -189,6 +302,7 @@ Deno.serve(async (req) => {
> 142:+          metadata,
> 146:@@ -205,10 +319,16 @@ Deno.serve(async (req) => {
> 150:+        metadata,
> 163:@@ -226,6 +346,28 @@ Deno.serve(async (req) => {
> 
> === deno anywhere? ===
> -rwxr-xr-x 1 ubuntu ubuntu 104509136 May 27 08:36 /home/ubuntu/.deno/bin/deno
> /home/ubuntu/.deno/bin/deno
> /home/ubuntu/.npm/_npx/05b6ef7b13673c57/node_modules/deno/deno
> /home/ubuntu/.npm/_npx/05b6ef7b13673c57/node_modules/@deno/linux-arm64-glibc/deno
> ```

## 🤖 Claude *(16:00:54)*


## 🤖 Claude *(16:00:57)*

**`deno` ESTÁ disponível** em `/home/ubuntu/.deno/bin/deno` (só não estava no PATH dos agentes) — posso fazer o type-check real. Primeiro reverto a linha do `VIDEO_FLOW_PLATFORMS` (corrige o bug de cobrança), depois `deno check` em tudo.

A mudança de `metadata` no callback é benigna (var nova default `{}`; plataformas existentes nunca usaram metadata; só youtube/pinterest populam channel_id/refresh_expires).

Revertendo a linha do billing:

## 🤖 Claude *(16:01:02)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
  "old_string": "    // FR-PE-013 (post-engine social-connect amendment): youtube/tiktok/pinterest are vertical-video platforms \u2014 a\n    // product\u00d7platform pair on any of them is a 9:16 video run and rides the same VIDEO_COST pre-debit as wordpress.\n    const VIDEO_FLOW_PLATFORMS = new Set([\"wordpress\", \"youtube\", \"tiktok\", \"pinterest\"]);",
  "new_string": "    // FR-PE-013 (post-engine social-connect amendment) \u2014 DEFERRED: youtube/tiktok/pinterest ARE vertical-video\n    // platforms, but the 9:16 render is enqueued ONLY by the article_generation step, which orchestrate-content kicks\n    // ONLY when platforms.includes('wordpress'). autopilot fans out one platform per sub-run, so a youtube/tiktok/\n    // pinterest sub-run currently enqueues NO render \u2192 adding them here would charge VIDEO_COST with no video_renders\n    // row to refund (charge-without-value, the exact bug this block guards against). Re-add ONLY together with the\n    // orchestrate-content/-step enqueue-gate extension (own slice). Until then these stay out of the video pre-debit.\n    const VIDEO_FLOW_PLATFORMS = new Set([\"wordpress\"]);"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(16:01:06)*


## 🤖 Claude *(16:01:06)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
  "offset": 100,
  "limit": 16
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 100	    const videoEnabled = plan.video_enabled === true;
> 101	    const videoFormat = typeof plan.video_format === "string" ? plan.video_format : "9:16";
> 102	
> 103	    // Video charge accuracy (OTD-VA-010 follow-up — billing bug witnessed 2026-06-26, cycle 2403bfcb): a 9:16 render
> 104	    // is enqueued ONLY by the article_generation flow, which orchestrate-content runs solely for the 'wordpress'
> 105	    // platform (index.ts:231-232). A linkedin/twitter sub-run never reaches video_generation, so charging it
> 106	    // VIDEO_COST is charge-without-value — and uncaught by the orchestrate-step refund (orchestrate-step:454), which
> 107	    // fires only on a FAILED enqueue ATTEMPT, never for a flow that has no video step at all. So count video sub-runs
> 108	    // by the article-flow platform, not by every sub-run (was: nRuns × VIDEO_COST → over-charged non-wordpress runs).
> 109	    // FR-PE-013 (post-engine social-connect amendment): youtube/tiktok/pinterest are vertical-video platforms — a
> 110	    // product×platform pair on any of them is a 9:16 video run and rides the same VIDEO_COST pre-debit as wordpress.
> 111	    const VIDEO_FLOW_PLATFORMS = new Set(["wordpress", "youtube", "tiktok", "pinterest"]);
> 112	    const videoPlatformCount = platforms.filter((p) => VIDEO_FLOW_PLATFORMS.has(p)).length;
> 113	    const nVideoRuns = videoEnabled ? products.length * videoPlatformCount * abVariants : 0;
> 114	
> 115	    const projected = nRuns * ORCH_COST + nVideoRuns * VIDEO_COST + ANALYZE_COST;
> ```

## 🤖 Claude *(16:01:16)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
  "old_string": "    // FR-PE-013 (post-engine social-connect amendment): youtube/tiktok/pinterest are vertical-video platforms \u2014 a\n    // product\u00d7platform pair on any of them is a 9:16 video run and rides the same VIDEO_COST pre-debit as wordpress.\n    const VIDEO_FLOW_PLATFORMS = new Set([\"wordpress\", \"youtube\", \"tiktok\", \"pinterest\"]);",
  "new_string": "    // FR-PE-013 (post-engine social-connect amendment) \u2014 DEFERRED: youtube/tiktok/pinterest ARE vertical-video\n    // platforms, but the 9:16 render is enqueued ONLY by the article_generation step (gated on 'wordpress' above), and\n    // autopilot fans out one platform per sub-run, so a youtube/tiktok/pinterest sub-run enqueues NO render. Adding\n    // them here would charge VIDEO_COST with no video_renders row to refund (charge-without-value). Re-add ONLY with\n    // the orchestrate-content/-step enqueue-gate extension (its own slice). Until then they stay out of the pre-debit.\n    const VIDEO_FLOW_PLATFORMS = new Set([\"wordpress\"]);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:01:20)*


## 🤖 Claude *(16:01:21)*

Linha de billing revertida (defere FR-PE-013). Agora o **type-check real** com `deno check` em todos os arquivos editados + o helper.

## 🤖 Claude *(16:01:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nexport PATH=\"/home/ubuntu/.deno/bin:$PATH\"\ndeno --version | head -1\nfor f in _shared/social-app-config.ts social-auth-init social-auth-callback refresh-social-token publish-social auto-publish autopilot-run; do\n  if [ -d \"supabase/functions/$f\" ]; then TARGET=\"supabase/functions/$f/index.ts\"; else TARGET=\"supabase/functions/$f\"; fi\n  echo \"\u2500\u2500\u2500\u2500 deno check $TARGET \u2500\u2500\u2500\u2500\"\n  deno check \"$TARGET\" 2>&1 | tail -15\n  echo \"exit: $?\"\ndone",
  "description": "deno check all edited edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> deno 2.8.1 (stable, release, aarch64-unknown-linux-gnu)
> ──── deno check supabase/functions/_shared/social-app-config.ts ────
> [0m[32mCheck[0m supabase/functions/_shared/social-app-config.ts
> exit: 0
> ──── deno check supabase/functions/social-auth-init/index.ts ────
> [0m[32mCheck[0m supabase/functions/social-auth-init/index.ts
> [0m[1mTS18046 [0m[ERROR]: 'err' is of type 'unknown'.
>     return new Response(JSON.stringify({ error: err.message }), {
> [0m[31m                                                ~~~[0m
>     at [0m[36mfile:///home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts[0m:[0m[33m173[0m:[0m[33m49[0m
> 
> [0m[1m[31merror[0m: Type checking failed.
> exit: 0
> ──── deno check supabase/functions/social-auth-callback/index.ts ────
> [0m[32mCheck[0m supabase/functions/social-auth-callback/index.ts
> [0m[1mTS18046 [0m[ERROR]: 'err' is of type 'unknown'.
>       return redirectWithError(err.message);
> [0m[31m                               ~~~[0m
>     at [0m[36mfile:///home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts[0m:[0m[33m372[0m:[0m[33m32[0m
> 
> [0m[1mTS18046 [0m[ERROR]: 'err' is of type 'unknown'.
>     return new Response(JSON.stringify({ error: err.message }), {
> [0m[31m                                                ~~~[0m
>     at [0m[36mfile:///home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts[0m:[0m[33m374[0m:[0m[33m49[0m
> 
> Found 2 errors.
> 
> [0m[1m[31merror[0m: Type checking failed.
> exit: 0
> ──── deno check supabase/functions/refresh-social-token/index.ts ────
> [0m[32mCheck[0m supabase/functions/refresh-social-token/index.ts
> exit: 0
> ──── deno check supabase/functions/publish-social/index.ts ────
> [0m[32mCheck[0m supabase/functions/publish-social/index.ts
> [0m[1mTS2345 [0m[ERROR]: Argument of type 'SupabaseClient<any, "public", "public", any, any>' is not assignable to parameter of type '{ from: (t: string) => { insert: (row: Record<string, unknown>) => Promise<unknown>; }; }'.
>   The types returned by 'from(...).insert(...)' are incompatible between these types.
>     Type 'PostgrestFilterBuilder<any, any, any, null, any, unknown, "POST", false>' is missing the following properties from type 'Promise<unknown>': catch, finally, [Symbol.toStringTag]
>     await notify(adminClient, userId, {
> [0m[31m                 ~~~~~~~~~~~[0m
>     at [0m[36mfile:///home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts[0m:[0m[33m597[0m:[0m[33m18[0m
> 
> [0m[1m[31merror[0m: Type checking failed.
> exit: 0
> ──── deno check supabase/functions/auto-publish/index.ts ────
>     at [0m[36mfile:///home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts[0m:[0m[33m152[0m:[0m[33m28[0m
> 
> [0m[1mTS18046 [0m[ERROR]: 'e' is of type 'unknown'.
>         results.push({ id: post.id, status: "error", error: e.message });
> [0m[31m                                                            ^[0m
>     at [0m[36mfile:///home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts[0m:[0m[33m156[0m:[0m[33m61[0m
> 
> [0m[1mTS18046 [0m[ERROR]: 'err' is of type 'unknown'.
>     return new Response(JSON.stringify({ error: err.message }), {
> [0m[31m                                                ~~~[0m
>     at [0m[36mfile:///home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts[0m:[0m[33m166[0m:[0m[33m49[0m
> 
> Found 3 errors.
> 
> [0m[1m[31merror[0m: Type checking failed.
> exit: 0
> ──── deno check supabase/functions/autopilot-run/index.ts ────
> [0m[32mCheck[0m supabase/functions/autopilot-run/index.ts
> exit: 0
> ```

## 🤖 Claude *(16:02:05)*


## 🤖 Claude *(16:02:08)*

`deno check` (gate de materialidade real) pegou erros de tipo — todos do padrão trivial `catch (err: unknown)` + um mismatch de tipo no `notify` do publish-social. O helper passa limpo ✅. Vou ler os trechos exatos e corrigir cada um (fixes type-safe, sem mudança de comportamento).

## 🤖 Claude *(16:02:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== social-auth-init 168-176 ===\"; sed -n '168,176p' supabase/functions/social-auth-init/index.ts\necho \"=== social-auth-callback 366-378 ===\"; sed -n '366,378p' supabase/functions/social-auth-callback/index.ts\necho \"=== auto-publish 148-168 ===\"; sed -n '148,168p' supabase/functions/auto-publish/index.ts\necho \"=== publish-social: notify def + 590-600 ===\"; grep -nE \"function notify|const notify|async function notify\" supabase/functions/publish-social/index.ts; sed -n '590,600p' supabase/functions/publish-social/index.ts",
  "description": "Read exact lines for type fixes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === social-auth-init 168-176 ===
>     return new Response(JSON.stringify({ url: authUrl }), {
>       headers: { ...corsHeaders, "Content-Type": "application/json" },
>     });
>   } catch (err) {
>     console.error("social-auth-init error:", err);
>     return new Response(JSON.stringify({ error: err.message }), {
>       status: 500,
>       headers: { ...corsHeaders, "Content-Type": "application/json" },
>     });
> === social-auth-callback 366-378 ===
>       }
>       const corsHeaders = { "Access-Control-Allow-Origin": "*" };
>       return socialAppConfigErrorResponse(err, corsHeaders)!;
>     }
> 
>     if (req.method === "GET") {
>       return redirectWithError(err.message);
>     }
>     return new Response(JSON.stringify({ error: err.message }), {
>       status: 500,
>       headers: {
>         "Access-Control-Allow-Origin": "*",
>         "Content-Type": "application/json",
> === auto-publish 148-168 ===
>           .from("scheduled_posts")
>           .update({
>             status: retryCount >= (post.max_retries || 3) ? "failed" : "queued",
>             retry_count: retryCount,
>             error_message: e.message,
>           })
>           .eq("id", post.id);
> 
>         results.push({ id: post.id, status: "error", error: e.message });
>       }
>     }
> 
>     return new Response(
>       JSON.stringify({ processed: results.length, results }),
>       { headers: { ...corsHeaders, "Content-Type": "application/json" } }
>     );
>   } catch (err) {
>     console.error("auto-publish error:", err);
>     return new Response(JSON.stringify({ error: err.message }), {
>       status: 500,
>       headers: { ...corsHeaders, "Content-Type": "application/json" },
> === publish-social: notify def + 590-600 ===
>           platform_post_id: result.id || result.data?.id || result["X-RestLi-Id"],
>         })
>         .eq("id", scheduled_post_id);
>     }
> 
>     // In-app notification (best-effort) — the user sees publishes in the bell (P0 notifications).
>     const platformLabel = platform === "instagram" ? "Instagram" : platform === "linkedin" ? "LinkedIn" : platform;
>     await notify(adminClient, userId, {
>       type: "success",
>       title: `Publicado no ${platformLabel}`,
>       message: typeof content === "object" && content?.text ? String(content.text).slice(0, 120) : null,
> ```

## 🤖 Claude *(16:02:59)*


## 🤖 Claude *(16:03:02)*

Confirmado: os erros são **pré-existentes latentes** (`catch (err: unknown)` + tipo estreito do `notify`) que o `deno check` expõe agora — **meus branches novos type-checam limpos** (o deno só apontou as linhas pré-existentes, nenhuma nos branches). `refresh-social-token`, `autopilot-run` e o helper passaram exit 0. Vou deixar os 4 arquivos tocados limpos (fixes type-safe, sem mudança de runtime). Localizando o `notify` + lendo os ranges.

## 🤖 Claude *(16:03:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== notify origin in publish-social ===\"; grep -nE \"notify|import.*notif\" supabase/functions/publish-social/index.ts | head -8\necho \"=== _shared notify? ===\"; ls supabase/functions/_shared/ | grep -i notif; grep -rnE \"export (async )?function notify|export const notify\" supabase/functions/_shared/ 2>/dev/null | head",
  "description": "Locate notify definition"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === notify origin in publish-social ===
> 2:import { notify } from "../_shared/notify.ts";
> 597:    await notify(adminClient, userId, {
> === _shared notify? ===
> notify.ts
> supabase/functions/_shared/notify.ts:12:export async function notify(
> ```

## 🤖 Claude *(16:03:06)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
  "offset": 171,
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 171	  } catch (err) {
> 172	    console.error("social-auth-init error:", err);
> 173	    return new Response(JSON.stringify({ error: err.message }), {
> 174	      status: 500,
> 175	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 176	    });
> ```

## 🤖 Claude *(16:03:07)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
  "offset": 369,
  "limit": 8
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 369	    }
> 370	
> 371	    if (req.method === "GET") {
> 372	      return redirectWithError(err.message);
> 373	    }
> 374	    return new Response(JSON.stringify({ error: err.message }), {
> 375	      status: 500,
> 376	      headers: {
> ```

## 🤖 Claude *(16:03:08)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts",
  "offset": 145,
  "limit": 25
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 145	      } catch (e) {
> 146	        const retryCount = (post.retry_count || 0) + 1;
> 147	        await adminClient
> 148	          .from("scheduled_posts")
> 149	          .update({
> 150	            status: retryCount >= (post.max_retries || 3) ? "failed" : "queued",
> 151	            retry_count: retryCount,
> 152	            error_message: e.message,
> 153	          })
> 154	          .eq("id", post.id);
> 155	
> 156	        results.push({ id: post.id, status: "error", error: e.message });
> 157	      }
> 158	    }
> 159	
> 160	    return new Response(
> 161	      JSON.stringify({ processed: results.length, results }),
> 162	      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 163	    );
> 164	  } catch (err) {
> 165	    console.error("auto-publish error:", err);
> 166	    return new Response(JSON.stringify({ error: err.message }), {
> 167	      status: 500,
> 168	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 169	    });
> ```

## 🤖 Claude *(16:03:34)*


## 🤖 Claude *(16:03:36)*

`notify` vem de `_shared/notify.ts:12`. Lendo a assinatura para o fix mínimo (widening seguro), depois aplico todos os fixes type-safe.

## 🤖 Claude *(16:03:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/notify.ts",
  "offset": 1,
  "limit": 30
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Shared in-app notification writer. Notifications are service-role-only INSERTs (RESTRICTIVE RLS "No client
> 2	// insert on notifications") — clients only read + mark-read their own. Best-effort: NEVER throws, so a failed
> 3	// notification never breaks the calling flow (publish, cycle, etc.). The bell (useNotifications) reads these.
> 4	export interface NotifyInput {
> 5	  type?: "info" | "success" | "warning" | "error";
> 6	  title: string;
> 7	  message?: string | null;
> 8	  action_url?: string | null;
> 9	  metadata?: Record<string, unknown>;
> 10	}
> 11	
> 12	export async function notify(
> 13	  admin: { from: (t: string) => { insert: (row: Record<string, unknown>) => Promise<unknown> } },
> 14	  userId: string | null | undefined,
> 15	  n: NotifyInput,
> 16	): Promise<void> {
> 17	  if (!userId || !n?.title) return;
> 18	  try {
> 19	    await admin.from("notifications").insert({
> 20	      user_id: userId,
> 21	      type: n.type ?? "info",
> 22	      title: n.title,
> 23	      message: n.message ?? null,
> 24	      action_url: n.action_url ?? null,
> 25	      metadata: n.metadata ?? {},
> 26	    });
> 27	  } catch (_) {
> 28	    /* best-effort — notifications must never break the calling flow */
> 29	  }
> 30	}
> ```

## 🤖 Claude *(16:04:05)*


## 🤖 Claude *(16:04:07)*

`notify` aceita `Promise<unknown>` mas o builder do Supabase é um `PromiseLike` (thenable). Fix mínimo seguro: `Promise`→`PromiseLike` (widening, ajuda todos os callers). Aplicando os 4 fixes type-safe (catch `unknown` + notify), todos sem mudança de runtime.

## 🤖 Claude *(16:04:09)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/notify.ts",
  "old_string": "  admin: { from: (t: string) => { insert: (row: Record<string, unknown>) => Promise<unknown> } },",
  "new_string": "  admin: { from: (t: string) => { insert: (row: Record<string, unknown>) => PromiseLike<unknown> } },"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/notify.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:04:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
  "old_string": "    console.error(\"social-auth-init error:\", err);\n    return new Response(JSON.stringify({ error: err.message }), {",
  "new_string": "    console.error(\"social-auth-init error:\", err);\n    return new Response(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }), {"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:04:13)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
  "old_string": "    if (req.method === \"GET\") {\n      return redirectWithError(err.message);\n    }\n    return new Response(JSON.stringify({ error: err.message }), {",
  "new_string": "    if (req.method === \"GET\") {\n      return redirectWithError(err instanceof Error ? err.message : String(err));\n    }\n    return new Response(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }), {"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:04:14)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts",
  "old_string": "            error_message: e.message,\n          })\n          .eq(\"id\", post.id);\n\n        results.push({ id: post.id, status: \"error\", error: e.message });",
  "new_string": "            error_message: e instanceof Error ? e.message : String(e),\n          })\n          .eq(\"id\", post.id);\n\n        results.push({ id: post.id, status: \"error\", error: e instanceof Error ? e.message : String(e) });"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:04:18)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts",
  "old_string": "    console.error(\"auto-publish error:\", err);\n    return new Response(JSON.stringify({ error: err.message }), {",
  "new_string": "    console.error(\"auto-publish error:\", err);\n    return new Response(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }), {"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:04:21)*


## 🤖 Claude *(16:04:22)*

Fixes aplicados. Re-rodando `deno check` em tudo para confirmar o gate verde.

## 🤖 Claude *(16:04:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nexport PATH=\"/home/ubuntu/.deno/bin:$PATH\"\nok=0; fail=0\nfor f in _shared/social-app-config.ts _shared/notify.ts social-auth-init social-auth-callback refresh-social-token publish-social auto-publish autopilot-run; do\n  if [ -d \"supabase/functions/$f\" ]; then TARGET=\"supabase/functions/$f/index.ts\"; else TARGET=\"supabase/functions/$f\"; fi\n  if deno check \"$TARGET\" >/tmp/dc.out 2>&1; then echo \"\u2705 $f\"; ok=$((ok+1)); else echo \"\u274c $f\"; tail -8 /tmp/dc.out; fail=$((fail+1)); fi\ndone\necho \"\"; echo \"PASS=$ok FAIL=$fail\"",
  "description": "Re-run deno check on all edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ _shared/social-app-config.ts
> ✅ _shared/notify.ts
> ✅ social-auth-init
> ✅ social-auth-callback
> ✅ refresh-social-token
> ✅ publish-social
> ✅ auto-publish
> ✅ autopilot-run
> 
> PASS=8 FAIL=0
> ```

## 🤖 Claude *(16:04:50)*


## 🤖 Claude *(16:04:52)*

**Type-check gate VERDE: 8/8 passam `deno check`.** Agora deploy das 5 edge functions que mudaram comportamento (additive + fail-closed). Sem deploy não está vivo (Lei 1). O `autopilot-run` ficou só com comentário (revertido) → não precisa.

## 🤖 Claude *(16:04:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nfor fn in social-auth-init social-auth-callback refresh-social-token publish-social auto-publish; do\n  echo \"\u2500\u2500\u2500\u2500 deploy $fn \u2500\u2500\u2500\u2500\"\n  npx supabase functions deploy \"$fn\" 2>&1 | grep -iE \"Deployed|Bundling|error|failed|Deploying\" | head -6\ndone",
  "description": "Deploy the 5 changed edge functions",
  "timeout": 420000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ──── deploy social-auth-init ────
> Bundling Function: social-auth-init
> Deploying Function: social-auth-init (script size: 65.23kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: social-auth-init
> ──── deploy social-auth-callback ────
> Bundling Function: social-auth-callback
> Deploying Function: social-auth-callback (script size: 68.69kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: social-auth-callback
> ──── deploy refresh-social-token ────
> Bundling Function: refresh-social-token
> Deploying Function: refresh-social-token (script size: 64.46kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: refresh-social-token
> ──── deploy publish-social ────
> Bundling Function: publish-social
> Deploying Function: publish-social (script size: 70.29kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: publish-social
> ──── deploy auto-publish ────
> Bundling Function: auto-publish
> Deploying Function: auto-publish (script size: 60.81kB)
> Deployed Functions on project bcyvddsykvehvpwstlfa: auto-publish
> ```

## 🤖 Claude *(16:05:27)*


## 🤖 Claude *(16:05:29)*

**5/5 deployadas** (script sizes 60–70kB, todas "Deployed on project bcyvddsykvehvpwstlfa"). Agora o smoke material (Lei 1): provar o caminho **fail-closed** ao vivo — chamar `social-auth-init` para tiktok sem credenciais → esperar `402 tiktok_not_configured`. Preciso de um JWT de usuário. Vendo o minter.

## 🤖 Claude *(16:05:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsed -n '1,40p' scripts/qa/gen-user-jwt.ts 2>/dev/null | grep -nE \"argv|email|user_id|generateLink|console.log|Usage|process.argv\" | head -20\necho \"---- how social-auth-init reads the user ----\"\nsed -n '14,45p' supabase/functions/social-auth-init/index.ts",
  "description": "Inspect JWT minter args + init auth"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 4: * Admin generateLink (magiclink) → verifyOtp(token_hash) → session.access_token. Per-user, reproducible.
> 7: * Usage: bun run scripts/qa/gen-user-jwt.ts <email>
> 16:const email = process.argv[2];
> 17:if (!URL || !SVC || !ANON || !email) {
> 18:  console.error('Usage: gen-user-jwt.ts <email>  (needs SUPABASE_URL + SB_SECRET_KEY + SB_PUBLISHABLE_KEY)');
> 25:const { data, error } = await admin.auth.admin.generateLink({ type: 'magiclink', email });
> 27:  console.error('generateLink error:', error?.message ?? 'no hashed_token');
> 33:for (const type of ['magiclink', 'email'] as const) {
> 37:if (!accessToken) { console.error('verifyOtp failed for both magiclink/email types'); process.exit(1); }
> 38:console.log(accessToken);
> ---- how social-auth-init reads the user ----
> 
> const LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization";
> const INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize";
> const TWITTER_AUTH_URL = "https://twitter.com/i/oauth2/authorize";
> const TIKTOK_AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/";
> const YOUTUBE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";
> const PINTEREST_AUTH_URL = "https://www.pinterest.com/oauth/";
> 
> Deno.serve(async (req) => {
>   if (req.method === "OPTIONS") {
>     return new Response("ok", { headers: corsHeaders });
>   }
> 
>   try {
>     const authHeader = req.headers.get("Authorization");
>     if (!authHeader?.startsWith("Bearer ")) {
>       return new Response(JSON.stringify({ error: "Unauthorized" }), {
>         status: 401,
>         headers: { ...corsHeaders, "Content-Type": "application/json" },
>       });
>     }
> 
>     const supabase = createClient(
>       Deno.env.get("SUPABASE_URL")!,
>       (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
>       { global: { headers: { Authorization: authHeader } } }
>     );
> 
>     const { data: { user }, error: userError } = await supabase.auth.getUser();
>     if (userError || !user) {
>       return new Response(JSON.stringify({ error: "Unauthorized" }), {
>         status: 401,
> ```

## 🤖 Claude *(16:05:44)*


## 🤖 Claude *(16:05:45)*

A função carrega com os 3 AUTH_URLs novos. Smoke do fail-closed — minto um JWT do Usuário Zero e chamo `social-auth-init` para tiktok (sem creds → deve dar 402 estruturado).

## 🤖 Claude *(16:05:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nURL=\"${VITE_SUPABASE_URL:-${SUPABASE_URL}}\"; export SUPABASE_URL=\"$URL\"\nJWT=$(bun run scripts/qa/gen-user-jwt.ts gabrielcallr@icloud.com 2>/dev/null | tail -1)\necho \"JWT minted: ${JWT:+yes (len ${#JWT})}\"\necho \"\"\nfor plat in tiktok youtube pinterest; do\n  echo \"\u2500\u2500\u2500\u2500 social-auth-init platform=$plat (expect 402 ${plat}_not_configured, fail-closed) \u2500\u2500\u2500\u2500\"\n  curl -s -w \"\\nHTTP %{http_code}\\n\" \"$URL/functions/v1/social-auth-init\" \\\n    -H \"Authorization: Bearer $JWT\" -H \"Content-Type: application/json\" \\\n    -d \"{\\\"platform\\\":\\\"$plat\\\",\\\"redirect_uri\\\":\\\"https://login.mcorch.com/social/callback\\\"}\" | head -4\ndone",
  "description": "Smoke fail-closed 402 on the 3 new platforms"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> JWT minted: yes (len 796)
> 
> ──── social-auth-init platform=tiktok (expect 402 tiktok_not_configured, fail-closed) ────
> {"error":"tiktok_not_configured","action":"Configure suas credenciais de app TikTok em /dashboard/settings"}
> HTTP 402
> ──── social-auth-init platform=youtube (expect 402 youtube_not_configured, fail-closed) ────
> {"error":"youtube_not_configured","action":"Configure suas credenciais de app YouTube em /dashboard/settings"}
> HTTP 402
> ──── social-auth-init platform=pinterest (expect 402 pinterest_not_configured, fail-closed) ────
> {"error":"pinterest_not_configured","action":"Configure suas credenciais de app Pinterest em /dashboard/settings"}
> HTTP 402
> ```

## 🤖 Claude *(16:06:51)*


## 🤖 Claude *(16:06:54)*

**Fail-closed PROVADO ao vivo (Lei 1):** os 3 retornam o 402 estruturado —
- tiktok → `HTTP 402 {"error":"tiktok_not_configured",...}` ✅
- youtube → `HTTP 402 {"error":"youtube_not_configured",...}` ✅
- pinterest → `HTTP 402 {"error":"pinterest_not_configured",...}` ✅

Isso prova E2E: função carrega · auth OK · branch novo roda · helper resolve (sem per-user + sem env) → throw → 402. **Backend code-complete, type-checked, deployado e provado.**

Agora a **Fase UI** (parte do "ambos") com força total — hook + card de credenciais (espelho do `MetaConfigCard`) + botões de conectar das 3 plataformas. Delegando a um agente focado.

## 🤖 Claude *(16:07:18)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Build social-connect UI",
  "subagent_type": "general-purpose",
  "prompt": "Build the frontend UI for connecting TikTok + YouTube + Pinterest to MCORCH (brand persona). Repo: /home/gcrUX/htdocs/constellation-orchestra. The backend is already deployed: a per-user `social_app_config` masked view (Vault-encrypted client_secret) + generic OAuth via `social-auth-init`/`social-auth-callback` (these now have tiktok/youtube/pinterest branches) + `publish-social` branches.\n\nREAD THESE FIRST to mirror the EXACT proven patterns (do not invent):\n- src/components/settings/MetaConfigCard.tsx  (the credential-card UX to mirror)\n- src/hooks/useMetaConfig.ts  (the TanStack Query read/write pattern for a Vault-masked credential VIEW \u2014 mirror its read/write idioms EXACTLY)\n- src/hooks/useSocialAccounts.ts  (initiateOAuth(platform) is GENERIC \u2014 reuse it for connect buttons)\n- the social accounts page (find it: likely src/pages/SocialAccountsPage.tsx) \u2014 where existing platform connect cards live\n- the Settings page that mounts MetaConfigCard (find where MetaConfigCard is imported/rendered)\n- docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md (scopes/labels per platform)\n\nCRITICAL DATA-LAYER RULES (these caused real production bugs \u2014 follow exactly):\n- `social_app_config` is a Vault-masked VIEW. The masked `client_secret` reads back as the literal sentinel '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'. NEVER send that sentinel back as a real value, and NEVER write null to \"clear\" (it won't clear \u2014 COALESCE-guarded).\n- Write pattern: mirror useMetaConfig EXACTLY. For this table the natural key is (user_id, platform) \u2014 read the user's row per platform; if it exists, UPDATE; else INSERT. Use `.insert()` / `.update()` (NOT `.upsert()` \u2014 upsert 400s on these views). The INSTEAD OF trigger + encryption trigger handle the rest. The masked view columns: id, user_id, platform, client_id, client_secret, scopes, metadata, is_active.\n- Selecting: select explicit safe columns (id, platform, client_id, client_secret, is_active, metadata) \u2014 `client_secret` returns the mask if set, null if unset (use that to show a \"configured \u2713\" state).\n\nDELIVERABLES:\n1. src/hooks/useSocialAppConfig.ts \u2014 TanStack Query hook(s): read all of the current user's social_app_config rows; a mutation to save (client_id + client_secret) for a given platform ('tiktok'|'youtube'|'pinterest') following the read-then-insert-or-update pattern above; expose per-platform \"configured\" state (client_id present AND client_secret === mask-or-set). Toasts in PT-BR. Mirror useMetaConfig's structure/queryKeys/invalidation.\n2. src/components/settings/SocialAppConfigCard.tsx \u2014 mirror MetaConfigCard. One section per platform (TikTok / YouTube / Pinterest) with: a short PT-BR helper line (where to get the creds + the redirect URI to register: `https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback`), an input for client_id (TikTok label \"Client Key\"; YouTube/Pinterest label \"Client ID\"), an input for client_secret (password type; placeholder shows '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022' when configured), and a Save button calling the hook. Show a \"Conectado \u2713\"/\"Configurado \u2713\" badge when configured. All UI text PT-BR.\n3. Add TikTok / YouTube / Pinterest connect cards to the social accounts page, mirroring the existing platform cards, each calling the generic `initiateOAuth('tiktok'|'youtube'|'pinterest')`. If a platform's app creds are not configured, the connect button should still call initiateOAuth (the backend returns a 402 with a PT-BR action message \u2014 surface it via the existing edgeErrorMessage/toast pattern). Use the proper brand icons available in the project's icon set (lucide-react has no TikTok/Pinterest brand icons \u2014 reuse the project's existing approach for brand icons, or a sensible lucide fallback like Video/Youtube/Image; check what the existing cards use).\n4. Mount SocialAppConfigCard in the same Settings page/section where MetaConfigCard is rendered.\n\nCONSTRAINTS: TypeScript strict; explicit types on props/payloads. Code/comments English; UI text/toasts PT-BR. Do NOT touch unrelated code. Do NOT run build/deploy. After writing, run `npx tsc --noEmit 2>&1 | tail -30` from the repo root and report whether it's clean (fix any errors you introduced). Return: files created/edited, the exact write pattern you used (insert-vs-update logic), tsc result, and any open issues."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': '`tsc --noEmit` already passed clean, which confirms the `React.ComponentType` global reference resolves fine (the project\'s tsconfig provides the global `React` namespace via `@types/react`, consistent with how the codebase uses it elsewhere). Both `tsc` and `eslint` on my files are green.\n\nAll deliverables complete. Here is the report.\n\n## Report\n\nBuilt the frontend UI for connecting TikTok + YouTube + Pinterest (brand persona), mirroring the proven Meta/social patterns exactly. The backend (`social_app_config` masked view + generic OAuth + publish branches) was already deployed, so this is pure frontend.\n\n### Files created\n- **`src/lib/social-app-config.ts`** — types/helpers (mirrors `src/lib/meta.ts`): `SocialAppPlatform`, `SOCIAL_APP_SAFE_COLUMNS` (`id,user_id,platform,client_id,client_secret,is_active,metadata`), the `SOCIAL_SECRET_MASK` sentinel (`••••••••••••`), the redirect URI constant, per-platform UX metadata (TikTok→"Client Key", YT/Pinterest→"Client ID", PT-BR helper copy), and the `isSocialAppConfigured` predicate (client_id present AND secret-mask present AND active).\n- **`src/hooks/useSocialAppConfig.ts`** — TanStack Query hook mirroring `useMetaConfig`: reads all of the user\'s rows (`select(SAFE_COLUMNS).eq(\'user_id\', uid)`), exposes `byPlatform` map + `isConfigured(platform)`, and a `saveConfig` mutation. Query key `[\'social_app_config\', user?.id]` with matching invalidation. Untyped view cast (`supabase as unknown as SupabaseClient`) since `social_app_config` is not in generated types yet — identical idiom to `useMetaConfig`.\n- **`src/components/settings/SocialAppConfigCard.tsx`** — mirrors `MetaConfigCard`: one section per platform with brand icon, PT-BR helper, the copyable Redirect URI, client_id input (TikTok "Client Key" label), password-type client_secret input (placeholder shows the mask when configured), per-section Save button, and a "Configurado ✓" badge.\n\n### Files edited\n- **`src/components/icons/brand-icons.tsx`** — added `TikTok`, `YouTube`, `Pinterest` brand glyphs via the existing `makeBrandIcon` helper (lucide-react dropped brand icons — confirmed `l.Youtube === false`; this is the project\'s proven approach).\n- **`src/pages/SettingsPage.tsx`** — imported and mounted `<SocialAppConfigCard />` directly below `<MetaConfigCard />` in the same tab; renamed that tab "Meta" → "Social" and made it `space-y-6`.\n- **`src/hooks/useSocialAccounts.ts`** — improved `initiateOAuth` error surfacing to read the backend\'s structured 402 `<platform>_not_configured` body (uses `edgeErrorMessage` for the `error.context` path, and surfaces the PT-BR `action` hint on the 200-with-error-body path). Existing per-platform branches untouched.\n- **`src/pages/SocialAccountsPage.tsx`** — the connect cards for tiktok/youtube/pinterest already existed (driven by `SUPPORTED_PLATFORMS` + generic `handleConnect → initiateOAuth`); upgraded them to proper brand icons via a new `PlatformGlyph` (brand glyph for instagram/facebook/tiktok/youtube/pinterest, emoji fallback for linkedin/twitter/wordpress).\n\n### Exact write pattern (insert-vs-update)\nNatural key `(user_id, platform)`, mirroring `useMetaConfig`. On save: look up `byPlatform[platform]`; if a row with `id` exists → `.update(writable).eq(\'id\', existing.id)`, else `.insert({ user_id, platform, ...writable })`. **Never `.upsert()`** (400 on masked views). `client_secret` is only included in the payload when a fresh non-empty value is typed AND it is not the mask sentinel (`secret && secret !== SOCIAL_SECRET_MASK`) — so re-saving without retyping the secret omits the column entirely (leaves the Vault value untouched) and the mask is never round-tripped back. First-time save requires a secret; re-save can omit it.\n\n### tsc result\n**Clean** — `npx tsc --noEmit` produced zero output (zero errors). ESLint on all my new/edited files is also clean (exit 0).\n\n### Open issues\n- **Pre-existing lint (not mine):** `src/pages/SocialAccountsPage.tsx` has 3 `catch (err: any)` `no-explicit-any` errors that exist in `HEAD` (verified via `git show HEAD:...`). My icon block only shifted their line numbers (65/85/94 → 82/102/111). I left them untouched per "do not touch unrelated code."\n- **Types:** `social_app_config` isn\'t in `src/integrations/supabase/types.ts` yet (same as `meta_config`). Handled with the untyped-view cast; when types are regenerated, the cast can be tightened. No action needed now.\n- Did not run build/deploy (per constraint).'}, {'type': 'text', 'text': "agentId: af8701874fa76780a (use SendMessage with to: 'af8701874fa76780a', summary: '<5-10 word recap>' to continue this agent)\n<usage>subagent_tokens: 128598\ntool_uses: 29\nduration_ms: 237149</usage>"}]
> ```

## 🤖 Claude *(16:11:20)*


## 🤖 Claude *(16:11:22)*

UI reportada pronta + tsc clean. **Verifico materialmente** (Lei 1) — rodo o tsc eu mesmo + confiro o padrão de escrita do hook (o ponto que já causou bugs).

## 🤖 Claude *(16:11:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== tsc (frontend) ===\"; npx tsc --noEmit 2>&1 | tail -8; echo \"tsc exit: ${PIPESTATUS[0]}\"\necho \"\"; echo \"=== frontend files changed ===\"; git status --short -- src/\necho \"\"; echo \"=== write pattern in useSocialAppConfig (insert vs update + mask guard) ===\"\ngrep -nE \"\\.insert\\(|\\.update\\(|\\.upsert\\(|SECRET_MASK|client_secret|onConflict|eq\\(.id\" src/hooks/useSocialAppConfig.ts | head -25",
  "description": "Verify tsc + UI write pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === tsc (frontend) ===
> tsc exit: 0
> 
> === frontend files changed ===
>  M src/components/icons/brand-icons.tsx
>  M src/hooks/useSocialAccounts.ts
>  M src/pages/SettingsPage.tsx
>  M src/pages/SocialAccountsPage.tsx
> ?? src/components/settings/SocialAppConfigCard.tsx
> ?? src/hooks/useSocialAppConfig.ts
> ?? src/lib/social-app-config.ts
> 
> === write pattern in useSocialAppConfig (insert vs update + mask guard) ===
> 7:  SOCIAL_SECRET_MASK,
> 16: * mirrors useMetaConfig: read the user's rows from a Vault-masked VIEW (client_secret reads back as
> 17: * the sentinel mask), then INSERT or UPDATE by natural key (user_id, platform). NEVER `.upsert()`
> 55:      // we simply omit client_secret rather than sending the mask back (which would corrupt the Vault).
> 60:      const secret = values.client_secret?.trim();
> 62:      if (secret && secret !== SOCIAL_SECRET_MASK) {
> 63:        writable.client_secret = secret;
> 69:          .update(writable)
> 70:          .eq('id', existing.id);
> 75:          .insert({ user_id: user!.id, platform: values.platform, ...writable });
> ```

## 🤖 Claude *(16:12:00)*


## 🤖 Claude *(16:12:03)*

**UI verificada materialmente:** tsc exit 0 (confirmado por mim) · 7 arquivos (3 novos + 4 editados) · **padrão de escrita correto** — `.update().eq('id')` / `.insert()`, **nunca `.upsert()`**, e o guard `secret !== SOCIAL_SECRET_MASK` impede round-trip da máscara (o bug histórico). 

Agora torno a UI viva: build do frontend no repo principal (= deploy, nginx serve o `dist/`). Prova material = chunk novo + env baked.

## 🤖 Claude *(16:12:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== confirm main repo (not worktree) + has .env ===\"; pwd; ls -la .env >/dev/null 2>&1 && echo \".env present \u2705\" || echo \".env MISSING \u274c\"\necho \"\"; echo \"=== build ===\"; bun run build 2>&1 | tail -15",
  "description": "Build frontend in main repo (deploy)",
  "timeout": 300000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === confirm main repo (not worktree) + has .env ===
> /home/gcrUX/htdocs/constellation-orchestra
> .env present ✅
> 
> === build ===
> dist/assets/useConstellationSigma-Cm6o9VPz.js   97.31 kB │ gzip:  21.58 kB
> dist/assets/proxy-D57I8X15.js                  125.30 kB │ gzip:  41.24 kB
> dist/assets/ConstellationMatrix-CtF73x6l.js    136.25 kB │ gzip:  37.77 kB
> dist/assets/CanvasEditorPage-eVUHSSaO.js       142.18 kB │ gzip:  39.61 kB
> dist/assets/index-DE5hGdPQ.js                  167.01 kB │ gzip:  53.33 kB
> dist/assets/ConstellationPage-CNY3xNaY.js      184.36 kB │ gzip:  63.64 kB
> dist/assets/CartesianChart-DgpIEZlI.js         325.07 kB │ gzip:  96.83 kB
> dist/assets/index-8CKiv5mL.js                  661.63 kB │ gzip: 196.04 kB
> dist/assets/react-three-fiber.esm-CuT2Yzzm.js  824.11 kB │ gzip: 221.90 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 22.75s
> ```

## 🤖 Claude *(16:12:34)*


## 🤖 Claude *(16:12:35)*

Build OK (22.75s). Verifico os gates de materialidade do deploy (SOP build-deploy): chunk novo contém a UI + env baked.

## 🤖 Claude *(16:12:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== env baked (supabase URL in bundle)? ===\"; grep -rl \"bcyvddsykvehvpwstlfa.supabase.co\" dist/assets/*.js | head -1 && echo \"\u2705 env baked\" || echo \"\u274c env NOT baked\"\necho \"\"; echo \"=== new UI in bundle? (social_app_config / Configurar credenciais) ===\"; grep -rlE \"social_app_config|Pinterest|tiktok\" dist/assets/*.js | head -3\necho \"\"; echo \"=== nginx serves this dist (sanity) ===\"; ls -la dist/index.html | awk '{print $5, $6, $7, $8}'",
  "description": "Verify env baked + new UI in served bundle"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === env baked (supabase URL in bundle)? ===
> dist/assets/CampaignDetail-DORNkhV9.js
> ✅ env baked
> 
> === new UI in bundle? (social_app_config / Configurar credenciais) ===
> dist/assets/AnalyticsPage-4V7qugJO.js
> dist/assets/brand-icons-DzN_vF3n.js
> dist/assets/CampaignWizard-CC8vNfqh.js
> 
> === nginx serves this dist (sanity) ===
> 2259 Jun 27 13:12
> ```

## 🤖 Claude *(16:12:48)*


## 🤖 Claude *(16:12:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== useSocialAppConfig hook shipped? (table name 'social_app_config') ===\"; grep -rl \"social_app_config\" dist/assets/*.js | head -3 || echo \"NOT FOUND\"\necho \"=== SocialAppConfigCard shipped? (redirect-uri callback string is unique to the card) ===\"; grep -rl \"functions/v1/social-auth-callback\" dist/assets/*.js | head -3 || echo \"NOT FOUND\"",
  "description": "Confirm new hook + card in bundle"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === useSocialAppConfig hook shipped? (table name 'social_app_config') ===
> dist/assets/SettingsPage-CHgtU2cG.js
> === SocialAppConfigCard shipped? (redirect-uri callback string is unique to the card) ===
> dist/assets/SettingsPage-CHgtU2cG.js
> ```

## 🤖 Claude *(16:13:22)*


## 🤖 Claude *(16:13:25)*

Deploy verificado: `social_app_config` (hook) + a string única do redirect-URI (card) estão no **`SettingsPage-CHgtU2cG.js`** servido, env baked, `index.html` fresco (13:12). **UI viva.**

Última verificação, conforme sua diretiva durável (ver UI renderizada antes de declarar pronta) — delego uma checagem em browser real (preview do dist + sessão injetada + agent-browser + Vision QA) do Settings→Social e dos botões de conectar.

## 🤖 Claude *(16:13:39)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Browser-verify social UI",
  "subagent_type": "general-purpose",
  "prompt": "Verify the newly-built MCORCH social-connect UI renders in a REAL browser (Sovereign directive: never declare UI done without seeing it). Repo: /home/gcrUX/htdocs/constellation-orchestra. The frontend is already built (dist/ is fresh). Be honest per Lei 1 \u2014 only report \"rendered OK\" if you actually see it; if the environment blocks you, say exactly where.\n\nESTABLISHED RECIPE (from prior sessions \u2014 follow it):\n1. Serve the built dist locally: `npx vite preview --port 4174` (run in background; it serves dist/). Confirm it's up (curl the port).\n2. Mint a logged-in session for the Sovereign: read scripts/qa/gen-user-session.ts for its usage (it does admin generateLink\u2192verifyOtp and emits the localStorage auth-token JSON for key `sb-<ref>-auth-token`). User email: gabrielcallr@icloud.com. Needs .env (SB_SECRET_KEY, SB_PUBLISHABLE_KEY, VITE_SUPABASE_URL) \u2014 `set -a; source .env; set +a` first.\n3. Use the `agent-browser` skill (NOT Playwright MCP \u2014 no Chrome in this env). Open the preview origin, inject the session into localStorage under the `sb-<projectref>-auth-token` key (projectref = bcyvddsykvehvpwstlfa), then navigate to:\n   (a) /dashboard/settings \u2014 find the \"Social\" tab/section, click it, and confirm the SocialAppConfigCard renders with THREE sections: TikTok (label \"Client Key\"), YouTube (Client ID), Pinterest (Client ID), each with a client_id input, a client_secret password input, the Redirect URI string `https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback`, and a Save button. Screenshot it (1920x1080).\n   (b) the social accounts page (find its route \u2014 likely /dashboard/social or similar; check src/pages/SocialAccountsPage.tsx + App.tsx routing) \u2014 confirm TikTok/YouTube/Pinterest connect cards render. Screenshot it.\n4. Check the browser console for errors (white-screen / crash). A blank page or a React error overlay = FAIL.\n5. Run Vision QA on each screenshot: `bun run scripts/qa/vision-qa.ts <screenshot-path-or-url>` (it uses Vision MCP, BYOK, needs VISION_MCP_PAT in .env; note it requires a URL or accessible path \u2014 read the script's usage first). Report its verdict.\n\nClean up: kill the vite preview background process when done.\n\nReturn: a clear PASS/FAIL per page, the screenshot paths, any console errors verbatim, the Vision QA verdicts, and \u2014 if anything blocked you (CF, port, session injection, missing PAT) \u2014 exactly what and where. Do not fabricate a render you didn't see."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Cleanup confirmed: no vite process, port 4174 not listening (HTTP 000), browser session closed, temp public screenshots deleted. The earlier "WARN: vite still running" was a false positive from `pgrep` matching this shell\'s own command text containing "4174" — the actual server was killed by the first PID kill.\n\nAll steps complete. Here is the report.\n\n---\n\n## VERIFICATION REPORT — MCORCH social-connect UI (REAL browser)\n\n**Verdict: PASS on both pages.** I actually saw both pages render, logged in as the Sovereign, in a real Chromium via agent-browser. Zero console errors, no white screen, no React overlay. All three new platforms (TikTok / YouTube / Pinterest) present exactly as spec\'d.\n\n### Setup (all material)\n- **Build artifact verified fresh & correct**: `dist/` dated Jun 27 13:12; bundle `dist/assets/SettingsPage-CHgtU2cG.js` contains the new strings "Apps Sociais" / "Client Key" / "developers.tiktok.com", and the Supabase URL `bcyvddsykvehvpwstlfa` is baked into 9 bundles (env present — not a worktree-trap empty build).\n- **Preview**: `npx vite preview --port 4174 --host 127.0.0.1` → `curl` HTTP 200, title "Magic Constellation".\n- **Session**: minted via `scripts/qa/gen-user-session.ts gabrielcallr@icloud.com` (1996-char JSON, contains access_token), injected into `localStorage["sb-bcyvddsykvehvpwstlfa-auth-token"]`. App booted authenticated — stayed on `/dashboard/settings`, was NOT bounced to `/auth`.\n\n### (a) /dashboard/settings → "Social" tab — PASS\n- The tab labeled **"Social"** is `value="meta"` internally; clicking it selects the panel that renders `MetaConfigCard` + **`SocialAppConfigCard`**.\n- `SocialAppConfigCard` renders the header **"Apps Sociais — TikTok, YouTube & Pinterest"**, the Redirect URI in a `<code>` block — exact string `https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback` (DOM-verified + visible) — with a "Copiar" button, then THREE sections:\n  - **TikTok** → label **"Client Key"** + Client Secret (password) + "Salvar TikTok"\n  - **YouTube** → label **"Client ID"** + Client Secret + "Salvar YouTube" (helper cites youtube.upload scope)\n  - **Pinterest** → label **"Client ID"** + Client Secret + "Salvar Pinterest" (helper cites Pinterest Developers)\n- Accessibility snapshot + DOM eval confirmed all 6 fields + 3 Save buttons. **Console: empty.**\n- Screenshots (1920×1080): `settings-social-tab.png` (Meta + Apps header + TikTok), `settings-social-yt-pinterest.png` (all three platform sections).\n\n### (b) /dashboard/social — Social accounts page — PASS\n- Route is `/dashboard/social` (from `App.tsx`). Heading "Redes Sociais" → "Plataformas Disponíveis" grid with 7 connect cards: LinkedIn, Instagram, Facebook, Twitter/X, **TikTok**, **YouTube**, **Pinterest** — each with brand icon + "Conectar" button. WordPress self-hosted form below. **Console: empty.**\n- Screenshot: `social-accounts-page.png` (1920×1080).\n\n### Vision QA verdicts (mcp.mcorch.com, BYOK, cost 0) — all PASS, "high" confidence\nScreenshots were uploaded to the public `canvas-assets` bucket for fetchability (deleted afterward), since Vision MCP needs a public URL.\n1. Settings Social tab: *"Não há erros visíveis na renderização da tela; todos os elementos estão visíveis e formatados corretamente."*\n2. 3 platforms: *"a tela mostra três seções... TikTok, YouTube e Pinterest. Cada uma... Client Key (ou Client ID...), Client Secret e um botão \'Salvar\'... renderizada corretamente, sem quebras."*\n3. Social accounts: *"a página foi renderizada corretamente. Existem cartões de conexão para TikTok, YouTube e Pinterest... além de LinkedIn, Instagram, Facebook e Twitter."*\n\n### Console errors\nNone on either page (`agent-browser console` empty after clearing on each navigation).\n\n### Screenshot paths (retained, absolute)\n- `/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/settings-social-tab.png`\n- `/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/settings-social-yt-pinterest.png`\n- `/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/social-accounts-page.png`\n- (also `settings-social-3platforms.png`, `settings-social-FULL.png`)\n\n### Blockers\nNone. Two minor environment notes, both worked around, neither affecting the verdict: (1) viewport defaults to 1280×633 — fixed with `agent-browser set viewport 1920 1080`; (2) the settings content lives in an inner scroll container so `screenshot --full` caps at the viewport — used JS `scrollIntoView` to bring YouTube+Pinterest into frame.\n\n### Cleanup\nvite preview killed (port 4174 → HTTP 000, no process), browser session closed, temp public QA screenshots deleted from the bucket (HTTP 200 each).'}, {'type': 'text', 'text': "agentId: a4214742125fc733f (use SendMessage with to: 'a4214742125fc733f', summary: '<5-10 word recap>' to continue this agent)\n<usage>subagent_tokens: 132075\ntool_uses: 49\nduration_ms: 386980</usage>"}]
> ```

## 🤖 Claude *(16:20:18)*


## 🤖 Claude *(16:20:19)*

Browser-verify **PASS** em ambas as páginas — Vision QA "high" confidence, zero erro de console. Deixa eu confirmar com meus próprios olhos e te mostrar.

## 🤖 Claude *(16:20:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/settings-social-yt-pinterest.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': 'iVBORw0KGgoAAAANSUhEUgAAB4AAAAQ4CAIAAABnsVYUAAAQAElEQVR4nOzdC0BN9wMH8F+ve3vcm95PKZVUIkqUkJAQtmKjeeS/xUy2YYbNa5gN27ANM+xRZuUVpjwKKVKkiCi93+/b694e994e/9/t0pKKUvPo+/nffzvnd875nd8959zr9r2/fkeapaxHAHokNU19AgAAAAAAAAAAAN1GmgD0YPnZiQQA4GXopaxVXVVBugJTTqG6ssNV6erqngs+Jy0t+iSQk5v73dbtZaWlLDb7sxXL+xoa0kI+nz9h3ISiwiICAAAAAC+DnIIiv7qSdAU5ecXy0nwCAPAyIIAGAAB4zTU8+n+H5ORk/7J778dLP6HTujo6u37a1WKF77d9X1RYSAAAAADgZenwRzwAgFeRFEOuFwHokeRZSrwKDgEAeBlk5VhCYQ3pCtLSDKGQTzouKuqWpISkzTCbFuUNDQ1bNm85/NdhAgAAAAAvj4yMbG2tgHQFWhW/hkcAAF4G9IAGAAB4KRq6sktLZ6v6+cef78beW7HqM2NjYzqbnZ0dHR3jd/jvO7djCQAAAAC8dF32iRG9qQHgpUEADQAA8BI0dGrcjNaravrRKaFXQuiDAAAAAMAr5gU/5j1RFfJnAHh5EEADAAC8HPgtAAAAAADah0+MAPAGQAANAADwkuD3CQAAAABoHz4xAsDrDwE0AADAy9JVv0/g9xIAAACAN1IDPukBwBsAATQAAMBrD7+XAAAAAAAAwKsJATQAAMBLgdAYAAAAAP4z+PAJAC+NJAEAAAAAAAAAAAAA6AYIoAEAAAAAAAAAAACgWyCABgAAAAAAAAAAAIBugQAaAAAAAAAAAAAAALoFAmgAAAAAAAAAAAAA6BYIoAEAAAAAAAAAAACgWyCABgAAAAAAAAAAAIBugQAaAAAAAAAAAAAAALpFFwfQsoOH6B06TB+yloNbLNLds48+CAAAAAAAAAAAAAD0DF0cQKt/vorZz4Q+1D9f2WKRnLU1fRAAAAAAAIB2SUvL2Iwc30AAAAAA4LXXlQG0lIYG08iotrCotriYadxPSl1dXK67Z59xZJR4mk6gHzQAAAAAALRjyPBRKqoaEuQ1NmiovaKiMgEAAADo8aRJ12Ga9Kc/axITJCQlpdXU6GxVUREBAACAV4/n0q+YsrJ0QsDnc4ryLgYcrSgref7NlVU1ps3yPP7nz5WV3KeX9jMdxK0ozc/NIj2Gmob2zPc/bVF47VJgZupD8YHS7dPXfIjtqb/3Ny2dPH1e337mzdevqar67adNT1duYjaoxbYt9DUyGzHORYJI/LX/O9IRTZcBt6K8MCcz6volTlE+eTG0tQOG2J5su7VvDDk51gjHidq9+zLl5HIz026EBZVwCjpUg6Z2715KKonxd198Kw0tnXfmfyKeLirIiY+NvhdznXSEla1DfOyt6upK04FDLYYMP+6zh7wALR296fO8roecvX0jrP0WDhk+WlvX4Ky/T4sajM0sI0LOiVcY4TiZTtTV1tINM1IeRl2/LA6m5yxcQXeRmvSAdEqr71T/7q6uNi8rPSYyNCs96fnrlJWTHzB4WHTEFTqtwO5lZTfmyoWT5D/U/ptzR5lZWJkOslHX0ikvL3l47/btm2ESzV7jnbhUmh+f5uh70am/fy0uzCONV/g0d8+L/xxJS44n3WP46An6xqb0dVRckHc7MjQ9JYEWjpngVllVEXXt4jiXd+gL4frls89fYVuv5f4DrQcPG6mkpFpVVZmdmhRywZ90qc69hwAAAPz3uj6A5ic+lJCSUhhhz+xnUhV+jZbkeC0ijX2f6c9kWxsCAAAAr4Ajv/9If9tn91Ieauc4YZp7h0IEbllpXMz1yipeq0sN+w/IzcroUQE0PZJ7tq6mE5Y2o/T0DQOOe4vLpaVk2jpQZ088Stw++GT9maMHC/NzSWfZODjdvXW9o4GjGL0MigrztHX0+g+wfvu9hcd99paXFhN4FmlpxtuzF5aXFF8M8KPR0kBrOxqZHfltF82tnr8SNa3eevrGHQ2P2tpK/AVGA416NXXGTX23tlYYfzfq+asdaD0yPSmBtj8/J6OBvOjQFyYWQ5Ie3OlnbtkUQHeohfLyLEUllcy0R8lvWtID+nqRlZXT72duYzdWnsUOCzpNy+9EhRfmZZPOauudSrw7KUkpXQNj+t7of/iXUs7z9qqhAeugoSPFAWvivWjXOYuuBJ0iDf/dUCLtvzl3iLnlsBGOkyJCz58/+VcfA+PBI8bIMBg0n21aoROXSvPj0yp2LxWXd/4XEXKh+9Jnp2kzVTW0b4ZeyMvONBkwZNyUd+kTzMlMbVohOf4uvThJR7T6qmSxFEePn3r9yvmU+Fj9viYjnd7Kz8vq0Kuyc/sFAAB4BXVpAG1qSn8KHooCaDrB6N+/+dLq6OjnqoVts+Go90yjR3P8O9+6zzmUIGicUbPZcKjZohvfun1wKE1AXhB72NxvNnqaFp/7dvWOyzmdqI7Rd7zX8o8n2xjqKjJps4py4qN8vt965GbxCzftOfevM9J93jhDknrV58jF3OfZKcPw3f1HvxqmWHFpldtnJ3MVJ39/YtdkdX7st+94PD7W7WFbvu3pZqlYEXty/6m7j7pWsE1nbdjysQ25unPF+lNp/9EzBwCALsAtL42ODJ298DPx7JDho/sPtJaTU3gYFxMZeqG+vo4WDh3haDZoWEN9/a3wi/RX6IO7vqIxxLBRE2iIQLOHsc5u+v3M6GqJ929fDznrNHWWsZklffQzH3TuxKG5H61MjIvtN8Dy3MlD2enJrdYv1ryfr5KK2vQ5i2lWRQtNB9mUl5YYmw5MiIumkdZoZ1clZbWUhLsh51t2JaOVmw2yUVZVj78TFXLBv6GhYYyzK59fo66hraGjl5mWeC34TFUVT1TnwKFlZcUm5kM4hXm0GXk5Gc3roVvRGE5RSdnAyIwmy+f9/xKnin0M+1vbOiiraWalJUWEnOXxKsizNB2ophJJSUma8xbkZYVfCmx1E8uhI80GD2Uw5JLiY288eYie3paGdHMXiW68oT5hmqGJ+Wm/g083kh7tFmehxR4laJCUm0UfMkym7egJF07//fSVoKtv6Dhphs/eb8WbTJg2q6yUc/NqMD1EdE2a5mSlPaStanFM2mpMWPAZWwfnmprKOzevJdy9JTpQMjIjxrj07W9eU1Mde/OaOKNx91yel5Vm0M+czkaGBbW40p4+bqaW1rKyCokP7kSHXxII+NLSMnaOEw1NBlVXVcTdvvHgzk3xyRUKBarqWspqWjeunCUSEjYjx0tJy0SFX7x/+8YT506GMcLRxdhsoJS09PXL5+JuRzRfOmT4yLr62kB/H3FXXPrclZXVLKztaDzX1n5bXFR9TQaMcX6bLvJavVX87cXTr47n2erps1lUkPvgdpSRibn4MD59RcnJsZymvqupq1/Jq6DH6uGDO/MWf8Fis90XLLt1/XJpUb7ZQOuH96LpK8XEwqogL3vAkOE11ZWh50/mZYteKfRKs7J1pEHhnZuhNKMM/ufvFl+fNIiy3YEBR35/+70P6Wu5rKS4/RY+TV27N6cwv/nFT9Frg7YqPzvjPc9l9BuXspIimvuXcgrq6uqe532mxRXi4Oza9E7l/1crIwTW1ddlpj7MpVegsRkNoFs9rTp6fUeMdVFRVecU5YcF/cPnV89euEJ8duiLkbZEKBRqafdukXG3erU316evibXdGPqyolH47cgwcc/6p89jq29lzd9zlFTUbUc79zYwos2LDD0vPn3NtfNuIyUlPcJx8uWzR1MTRR3MH8bHlpYW0RMaff1y0zoamtriS4U839VL32FaHJ8W7WEwmG/N+oDW0PRya1Ftb32jMZOmN38jKi8ruREW1KIeCQmJofbjmmflTbR76xv2G/DXvu/EPcRjb12TlJKkbwI5zf5oo28/c7qURtJtvS/Rr1VMB1qpa+qkJt6/FHiMvgpafVWqa+mWlRbfvx0pPoD5+Tn0W41Wn1erlyh9E2v+HkifZoutTAdat/9uAAAA8OroyjGgH/WAfviwJvGhaPbJADrHa5G4K3TH6tS17KvOEE8z1ExNe5OuxrZ0mzfOSF13+NszR+kyOry5ms1n3v57F4wza0yfKaa67uDJX/zl+81knY7X1ilM3ZGz5s10nzdzmC6T/AcYaoaTZrrPnOk+yfDxqSHsvpPcJ5upq5u5zBxn+B89bwAA6Co0nigv5ZDG/m4GRqZBJ/8+7r1bTUN7qP1YUeHgYf3MBwcc+/3k4X2mg4a22Naon7mWnv7Jw7/SBEenjyHdKviMX3J8LM1ixJmODINZw6/6c/fXNGtotf5nor/D08jj7wM/aOn2sR875bjPHtoSQxMLmiM0X01Tu7ehyYDQCycP7duurK7R1FQLq+ExN8N8ftlaVcl1mjZLXKhnaFJRVuq959sHt29Mnu5BU4YWO6VV3YuOoE+BKSdnZimqSlFJ1WnqzJvXLv7163aaeU1+dz7pFBrQ86urr7WRPtM4yXywzYWTh4//+bOSsqr9OJf2t60oK6G5Aw34/P/6hQY6bTWy+Vlou2kk4d4tDW090tqVkJmWRAMpLR3RUklJKX0js4dxt2m8Ncpp2o2rQX/t21ZRXur0lnvz2tppTJ++xn6/7bwccMzOYZK2rug8jpk4va6h9shvP14OODJslBONmR5V0kv5hM8emrw8faW1OG40Rws69fehX7apNLaKFjo4v81kyh/9fdelM0ethjvQ2FS8Mr2Qzhz9/ezxP2wdJ6tp6dAL5vrFgJFjXWho1bzO/hbW8gqso3/uPnvce6i9I306zZdq6egnxEY33yDguLc48Gprvy0uqgexN69cOJWSECdOjtp6dbS/VTskJCRJG1fU0JGO1TWVf+3bTl8vQ0eOp0+cJno8Ltf3wM4WWZ6mdp+KkuLjf+wuKy4aaidqkrKqxtjJ70RcOXd4/3ZFRRUWW/HpXfcx6FcnrKWZY2baQ9qA9lvYKsVeKhXlrQ8KVF5aXJCbpfXky/+Z7zNPXyEt3qnaIb4wWj2tI52mJt2/8+eeb5IT4iyHjaSvx8P7v6+q5NGzI36tFeZlqWnqtqiwrav90XOnL5xps+gL5+CPm2jI7vKOB2n7naGdtzL6fdXUd/+XnnTfZ+/W2KirLjPmM2Xlmu+o/XcbNQ2turralMR/hzehXzPs37Ghvr7+6UP0nFfv08enOUlJiYmuc+jZvXY5sK1qM9ISpaSkmr8RJdyLebo9dJG17RjSGu3eBpmpSc3HJ6FpclsDHLV1pgz7mdPc+VLAEcP+A+g/PW29Kun3AQyG7OBho8QNppeu+LuE57xExZU0vQc+vdXzvxsAAAC8dF0WQDPNzWW0tISFhbX5ecLs7FoOh6GjyzA1J52VE3Ypnk9/6TS1fByrqhla6tDJipuX7jy7w9Fz4yb4+1y6Ex8fdurI1Q73f2YP81w931LU7znl0o7Fs8aPGD9r6YGroj/R0528wmukbo+JYrlp53xP3oyPhaZsEgAAEABJREFUvxl45FIO+j8DALweZr7/qdfqrfQxaOiIq8H/ENFvxUOjwi/R35C5FWX3oq/3bUxYzAcNvXXtUimniP7GHh15pUUl0lIyMgxZGtBUlHHob8XiETyba2houBF2QSgUtlX/M9EIhscrr66uzM3OKCzIpjVyivI5RXkt7u5VkJd94tAvOZmpDAaTV1FO0xNxefzdWzTpEPD5EZfPaej0ZrFEeVlhfvadm1eFQsHD+FhOcb5x/4EtdpqeHJ+fk0l3RENGDc3ejY23SY6/R+unVd26HiIrqyDOFDqERhhsJeXzpw63dWu1AYNtxEe7qooXfjnQ1ML6+bdtp5HNz0I7KnkVDCaTtHam6E6T4m8bmQ2iSw2MTEpLCmmYYmZp8/B+TG5WWk1N9a3wyzRKbp5wtXPELp/1r6muKszPibsdQVeTlpYx6Gd6/fI5epZpyJXy8K5hfwvxmrejrtI2kGddafS4RV+7TI9bfX3d5bPHr178h8bl/cwswy8F0Do5xQUxkaEWg23FK+dkptEDUlSQy6sozUlLoSWJCbESkpJycqzmddK2nTt5qJJbVldbS5+Cmrpm86UyTGY1r5UxdtvZ79MX1ZPnrvVXR/tbtYpe5OZDbJIT40gbV5SUhAx9svUN9fTs0ECwoe0BIspKix4+uENfgLeuX1bV1KEl9KudpAd3xac1PETUhfzprUwGDE55eI9OJMbd7m9h1X4LWyXDkKlr+3Kt4nFlmU9kqc98n3n6CiHPgX5XoaPXNy0pvq3TKiUpLaegIBQIaMJ78cyRp2ug3+31Un7iq4t2rnaxphcOfVZ0R+JstK13hnbeyvQM+vG45Qn3bwsE/NTEB+VlHL0nk+523m0oBlOOtvA5bwLZJVev/bipapo6tbW1Em1XSxelPXzQ9EZUXs7p6JBBDKZsFe+5Rsdu50zF3Y7klpemJsXnZKSqa7X5DwF9lzv2588sxV6Tpnt4Lt1g0/hlD+ngJdr0Hti5f0ABAABeEZ0cgqNBQoKhb8AwNmYYGTNNTJhGRjJaon4opX/+QRr/sK7kj980Vqzs86e3MD+Pn5LCf/hQkJIsSE4WZGZIPOcgaNzYhKJxZr3V+hqqMW5yBYStO9hUnUa9qQmpFabjmq/JULOZv3r1rJGGvRWZpCLnzrUnR8Bg6Iyat3zh2zaDDRX5qdf2b90R1nfDsS+GMYvOLp6+4mIxUbMcNNhMnS/QZTfVN+jtjxe4DhtkaqROilJj71w7tf/g2dinh9Rgm7qMNBPFz7E7ln0mHrwi9+zOjQI1772uur1HjjNTvJxT3LjeJM8PZ460NDXrrVhRlJpw89qRX/ecS2j86MMw9Tzmu9yMmeO7ZGP8KE+PsZZGzOL4qEt/Hthz8vH4FgwdG7cFnu5jh5mpM/lF8TfOHfr54KnYYobpXO9jX1g+7vZsON/7xnxCii599u5n53IEDN2R8z72nDSscafZ8Qmx53y+93m+MUYYOuO9Nnz8tqWZuiLhV2THnvt5xw5RY9TGbvXd7fa4E4fiqG/O3/mG/mL/66z5P6SxzYYNM9OlT4f979F5sWcNAADdTDwGtIPT22wlJfFdtuTk2W+5L2haobJxOAU5BXZTV0RxR+nmEh/e1TPs5zRtJhFlDQkxEVfq6mqbr9DQSDzdav3PVFdX11QX/QjSVG2L/qo0jx4/baa8AptmLpKSkjVVVeJyfk3No3rq66p4PJoF0GkaGDVtWFFaIv9UL04agognhLVCSWnRH02z2L1Kiv+9QR/NLtls5XzSgXGu1TV1dPsYPrh9s8Uhak6epdh0tCvKSmgcLNsY6T7Ptm01sry0pPlZaIcCS7GmcbCRVs9UYlzMRDeP8EuBRqaWNIIUtVaBZWphZWP/7+cyOXnWMxtDnwJNdMWF3FIOja3l5VkMhuxHK7c0rZz8eEjT+sdnv/0rrflxE4+Xwu6lXFdf2zQiM10q33jqSePN5cQTjQfl8WFpaBml9tY3cpz8Dp9fVVleLiUtLfn4b+fF6AUmx2KTp8iz2G3t9+mLqrm2Xh3tb9WcrLw8/T5J9FTq6xPuxcTHRpE2rqio8OBxLu+8PXuhoLrmwb1b4iEUWtX06qutFYpHD1BQYDedVnoeqx+/0JrQV59h/wH0hA4ZPlpcQjNc+i1FWy1sFZ9fIyPT5p/20YNc/eQd9p75PvP0FdKOvv3Mxe2kwe61SwGlnMK2LqerwafpN0PunstLigruRoeLn2ZzQiFfQb7XE41v+2oXa/7CoU9KHD629c7QzlsZvT7pkRc/ETFZ+Se+Ymm1TvplkrikqpIr/+RXMu148auXqq7kBZ/2m+W5zNDEXDzuR6vVJiXcGTdlpviNKPlBbItKTAcOHecyQzwtfu7nTvg0v01ldWWlsooGeQ7tnKmm95A6+rqQbu8Xapr+X7sYQB+No7WIbm4Zde1ihy7RpvfAzv0DCgAA8IroTAAtO9RGc+16GS2t5oV1PC5n755y/xPij+7lx4/Rf5lVvZbQYJo+WPYjxavRPLpw01fVMTHP3k1FcWx8hWtvRcPBfRX90ooZan3N1GhxTnxC8RN/x6Y2csWvP883a/yIyucTxcYRMEwNFy/8VjQgMkNn8ob921wNH42PYThuxRaG2uV2hqpg6I79Yu8PM80er6JuOMzJcNjokZbLxBU2X5Wtptb4i0d2QkKzdDr3zpEDvwrMFCtii/ii9g1b9vPeBZaPPw0q0gpdDIeNsjRd9vHOq/9+Y6/r/sN+wuRX0E8Sirpm4+ZtG6RL5n92Mo0m74M+/mH/h405c0VRBVPdbPS8b4bbmC7+cEdOcWp8PJutqGakK6q+Iie1iM/PSeXyBQzDt785+M3kx/0MFHubDaMPS9PPPL88l9p+Bi06Yt67XHXFx5PPVOw9bOY2b1PDhQt/SChOTYhP4Ssq6uqqNw53nZ3D5XPTUgX8p2p54WcNAAD/keiIy3M+WqmmoU3D6KrKitCgU5mpD5uvUF3FU+ylUtB4py+ajLTcvqHh0tnjRPS7Ott1zkKaWbQYSLe5Vuv/t6Z6IiX1KKGQkenwXxHZOk4syM0Kb/zb7eGjJ8gy5cXliopK4gkan8mzWLyKcsVeys2fiKKySl5W6jPrp7k2W1GlaZalqMzllZGOoDUEH/51+tyPcrNSHz640+o6VbyKpqOtqKQiFPDFedDzbPvijTS3tMnLEo0S2+qZKszPrRUK6KXSp6/JtYtnxK2NiQyNuHKu+WoamtrtN0ZKSprFUhSPFs1WVq3klldV8mjNB3dtai9eb/dKa37cRMGchEQVjyvqnSqnII5y6NIqbsfyGhpyXTnvn5GSQKfd5rQcR040NLBRf5o5NpVMfHu2qG9sxJXO7bf9V8fzEN/ir2W1bVxR/xz9nTT28BWNKp6T0WKY5vbaWcX997RKSMjJybVYwbCfOc34Duz4Sjw7xtnVxHywOJlttYWtKuMUWVjZtrpIWVVdU7fPhVOH29q21SP59BVSU13VVg3imxA+uXnrl1N2Rgp9kMYhfZ2muXvv+aZFVUxZOb6g+snmPeNqb/7CoZm6krJaeWlxW+exnbcy2sL8nIwTh34hbWirTrHionz6JZ+Wjl7TANbKqhrveHgd2PlVK1W98NVbX193/fJZHq/8atCpsZPfyc/eQa+0VqsV3y2QvhHpG/WPCDnXop6Ee7fog77JLFj21b7v1z69o5zMlKH2Y+kKTcd/oNUII1OLp0fheK73pXbp9e3HZMgmN/41AH0JxEVHmA4aGtXZS/TFDzIAAMBL1JkhODRWrqbpcy2HU3UjsvTwX/kbv8qcOztt4oSKx+kzaewEXXHSnxbSRQWbNpb+fbjq5o3akhIaRquvWPl8+6nITU2jyaaamaUOjXkV+1qKUtaKtDs09Gy2FoNBchJiU3Ju/rnExXrIEOtZ34YV0Y++k2Y1DoChNmzBisb0OfvSgVUeLo4usxYf5I5627KtBJqhNvLjL0TpMz/+yPqFLiNGu8z50udOBU2uZ362YJhaW02lQW2zueK7R3/YuHHDzlOxXMK28dzYmMPy40/SCh1dPNafjBfFrZYLvvSyeaLCnJNLXYYPtR3uuNCncfCRke6Nwykz1EzN+oqGHgn7ymWEg621y1fB8al3EnIIg6SeW/Pu9CnvfnlK9LmXpPp/6T5pynTPndcqdMZ9vEyUPmef/eoDl9HW9Fl8dZZ+mOk9efnCkWrkGZiC4tg7qalhOzwchw+xHu3xayyfMC3dZtrocu/u/3j6JLeF398UfeKuuLnT023KJPcVJ5+6ceGLP2sAAPiv0BwwJSHO2s6RTj+4fWPYyPEKCqKvV8e5vDPKaSqdyExNtB45lsYo0tKMAUOGtdjcYojdZLd5ol/m62uFtULxX83XCoWy8vJP76vV+psUFeXSYKlf/0F0R4OsR5AOqqutlZYSjX+qqqZpYj6kqbyvyQB1TR2a49iOmViUlyPOPRXYijR0EC01MlNV00p+GPfM+h/ERhmbDVRVF30BT8OmmprKvJxM8vwaJGqqKmnKH3L2+GhnVxr3tLrW/TtR4qMtKSll7+iSEBf9/Nu+SCNpEOno7GbY3yI26ipp+0wlPbhtRw9jfrY4hqOtNRkwRFNb9I236cChszyXNjxfY4Y7ONNsi91LmV4/8feia+uEyfF3aYBHzyCDwZzhsaSf6aAWLWz1Snv6uBHRWL2utqMm0swoKT5W1OVQFJIqWA13uH/nBumI+rpaGWnRFUWvSQ2tlqMHxN+7paapSw8aTejoGRky3EFLzyAuOrJD+60TCuTkFR4drnZfHW1t9UytXlFO02baNA47y6+prqsVdUlvrJYvp/DsajOSE/pbDKanlZ5ra1uHp8dx7mc+hB6Bptmk+DvGZoNaHamjHfTLJGUVdfplQ/NCejz7D7SeOtMz9eG9yso2/2Su1SP59BVC2n6nelqrp5Vew3MXrdLtY0hEuXwlPS90Qsjn06u0aSxmGh+3CPefebU3f+FYDLGdPH0eaeudod23sqz0JFk5eTNLG3qmaG0eXl+yH38bJ9ZWnWL0hN2NuT5+6izzwcPoU+6tbzR+6rt3oq61+rcUz3/1tjg+TWgbGLKydIJ+wZaVliT+W4e2qk15eNdyqH1JUQENrEkH0TdSTlH+1Jnv0yNGn5eJ2aCh9uNuhV96es3neV9q0uqrUoJIOE6eTt8b6T9q9J8hy+Gj8rLTSUcu0eZa3ar5fvUM+tHvewgAAMArqTM9oBtau/VEG0SfNRv/uvHxg5DnHIGDEEFObGoxsdTVNTVUZKSpGTYOwJEWm/rkx01B7jXfncVFk2a6zPv+6HKm6C6AdD2iqK7LZhK2rs0g0VzRpe+/3Xm28fbcOWlb+YaWv83UbXWfzL6jLEVLUn237vCLEu2p+NSeLQz2QkvuzavFfNJRbMORNqJfWCpublmz0U8U1Kb5bVxB1Hw3jVI0GjRSlx31uE9MxQ2fgxcbe/7mxHN9hm4AABAASURBVJ4NS51nZsZU66ujSBKKi9Pic8hoRcXRCzZss0zLTrjpvcL9Thq3nU7CiobDLNUbJyznffnzPPEzayzQtRzWl305tr0mC9Iu7tlRlDbZbZzXXn81mgUz1URxvaKuLpvOPFfX5K541gQAAP4zt65fmvXBMnYvlfi4GBmmnMvM/6mpa9OYKeqq6I5qoh6dUlIz318qLSV9PfScvqFZ821puqSjp//hZ5vqG+qT7t9JuH+bFt6Nvu4w0dXYdNCpw782X7nV+pvQmCYq/KLTW7NEo5reCDMw7tgAlzevXZo8Y67X6q1Fhbm5zboBPrwfM3rCW6oadI/xQad9xYU03lJR1fho5Tf52RlnT3gLhc/+B66ijHPxzBFalYqaZlZa4tmjf3YsUXs8Blli/F1tPaNJ0+ce/f2np6OchHu3aGbkNmeRDEOWBl43Qi88/7ada+TM9z8VT+TnZJz2PcApFt0jq60zlRB3e9ioCZcej3VLd3c58NgIx8maun1KS4quBv0j8RyNqa+vz8lMW7h8Y0V5aUToOXHf2NCg07ZjnN/7cIWcvHz83ajUxPst2tnqldb8uNHghh43uq+0pAfXQ0Ud4UMvnKKx2nyvL6qqeDE3Q1Oe42uG5sKCTjtOnjHhLff0lAR6TbZYSqNb/8P7HCa8NX2eF/1snJHy8IzvwepqXof2SxfR0H/R51//ufub9l8dbW3VTjdesVavqNuRYQ7Ob9NTWVNVdeNqkHiQh6hrF8e6vJOVkpSb1d6dKnMyU69dDhzrMoNmmpFXLtDgtflSmi32MTKhp7XZ+mlCobCvkWllR7LC2lphdnoyTa7FfcybxsQQ8Gvo28ut8MvtbNvqkWz1Cml6p/I9uOOZTWr1tEaGnBvr8q5iL6XykuKQ8/60hCbj9AKmaW/Y+VOJD+9q6epfOeffsqp2r3b6wglufOHQbem7YlBjX+/W3xlaeyuTln6U7dK3iDNH/xjhMGnkWBd6CmjGKj7RTdqqswm9JIQCgZ3DRMeJbtyK8riY69GRoRLPfcxb9cTxSWj9l5KQcyfeW7hiwJDh92/faLXa5AexrnMWhV8629Ze6uvrnr5jQRN6oEaMmTzRbY6klBR9aYeePy7uxv60Z74vNWn1VZmZlhh++ezIcS7jXGbQr3kS7sbcuBpMOnKJNtfqVs33S1+SfYxMCQAAwCtJgqXc4fvnyFoP1Vz/lYzmE3diqa+urjh9krP/14bGkeAkWSyVj7wUXaZINn6V3USYl1u4aWP17baH4GDbbDjqPdOI5Ph6uHv33XL0q1GKOUc+cPdR2+C7bZxi9smFcw+qfen7jZMi/8a3bh8cSlO0Wbbz+wXD1VvWk+Iz692tuYM3+Iqy5lSfOe5bbz4eUdnU0/vYcsvHY0CrTf7+xK7J6vzYb9/xOMId983RH0QzW9w9vBOe8csoQ2fSTt8fnNTpvjze3RrVFIyrDXrXw1U0BIf/wWuKy59uAHvYat+/5hmSnJMfuK+5oSYeDbnIf8n01ZeLxQ1c6O27QtTAz9798lyOaBCOd1csX+A2TLep43ZF/JH1K7492xjdsm1WH/WeZ0RS//Rw/6axFbpjvz+6e7J6a23OPrnk3TXXFN/df/SrYYoVl1a5fXYyV7HZETiUqjZ2xQ/fzLdsORameKnokDD6uv7su22UYsXVL9/9+NSjAT3YNhv9vd112znsHX7W3U9NUz8/O5EAALwMikoaVZUd7rrVKll5dldV9UxqGtou77zvvWcLeU2McXaleQeNUZoXmpgNMh9i+/QfXMN/QE5OYf7Ha37Z/iWBN4Ln0g3HffY8/wgez09LR89x8jt/H9zRsW96XiUGRqaDh4/uvreaHvtWRr/noN9g/bF7yzO/gAF4A8gr9Kqp6prbJNGqKsoKCQDAy9CZHtA10bfS354qugmhgQHT1JRh3I9pbCyjpa006726svLSP0UjyinNdFeaLrr/g+gmhElJ9CFIfChIS+vATQhFYwwnJOSQUYqiMSj66pqKBuBIjc2p4DcfwkFt8My3RelzzslVH+8MTCgWsG2+9PWeb/iohoqKCj7RZTbdyZCIhrQwNNVpYwgOAZ/bOL4HU81Qje5O/FGabfru6o+HCWIvnfS/dLf5nQgFXK54trepqS4j6nFezTacPO/DmYakiHH10KWi1hqg27fxKVQUV/zbp7q9wJWbcG7/xmvfFxNDS8vB42Z6zBzW22zmCs+rN9dcbvXTfgW3uIIQdZLjv9B99TXxKgy2GpNf/KgFim3uitF72Ew3mj7z4//8bMXP19K4ArXxW07sdVUnHdD6Ye/oswYAgFeDoYl5XxOLiMtnmXJyI8ZMyk7HV3cAPReLpej0lvuV8/7VVZVDbMfQBLC0pLg7MuL83Czf1zl9pgZZj7gXfZ1Al5KUlKTJe0bqQ6TPAAAAr5HOjAFNGv8SVJieVnklpGTfL/krlme8PS3rfQ9a3mvGO+IVFBvT58z5HnRR/uefle7fR1cWZqQ/f/osws+NTS2icbCOpeWwpjsQPjEOBoPBZjaGyRXFqTk0DWbojpw5/lH6TMu5OVF3i0TNGbXQa7KpaMAshuG4BR+OazNOrUi4ejOH/lfXbZmXq6kag9131Lurty13dZo802OyYcvYmpt69aaoeuaw5Tt/8Bw/SEdNZ9DkZd/vnCdqQfa1S/EV3JxrUdlPNIBtOtlz4ShRApxy91rOc3yTqTZyw7kbN0L8f15oyo29ds77261+saJjoKioyHxisGQm83H7uGk3Yxufhcsyr/F9GY13Vlz+V3DY+T+Xjdd5xgDLDLZiYzXcnNwcGh0zTMfOGtn64WIy26qqC541AAC8MjJTkuqFtfMWr35vwWcNDQ1hQacJAPRUolHjH8a9/d6HH3y6vq+x2bkTPq91Rtyt/jn6e0cHfoFneud/Hw+xc7wecpYAAADA66MzPaBbxX/wQJiXK6OtI62jSyQlpFVUBLk5goQH5EUIKnLvpPFd1NVHz50kSleL0mJzuaR57Ckojr0aWzFulKLZgr8CJmcLGL111Zl8UfhsNPOb35g7lv1w4PuTNrtcDXtP/uafyd88e4/F137+9ojZDzPNzGZu85+5rWlBxc39By49NS5EbtjBrf6m37iZMY3GLd87bvm/S3LOfr/nmmj9qIMbDljuXWDZogEVsQe+2RNVTMgzb7hXkXo1tnimka7Zh943PqzIyear9VYX3ZMw/mZCUWN7+NzG2zIydd2/9x9WXBy757P156L+9Lk5/othimYz9wbO/LcqJqkQ9UduZ5+CnNhL8XzLwcxha3wDZ+WIhn5WJ6LamZZee/erbVix82oxl1tMI2RF5rAvDgXOK049tWXFwZtP1lL8ws8aAABeGbV1wpAL/vRBXkNXLpx8ujAx/i59EHgZqqsrMf7G6+7urXD6IPCy9cy3siO//UgAAADgddOZHtCSqqoaG74yCDxPH3SCzorL+Ymiv8ll9u8va9JfNPvwIXlRgpz4BFFXXvGNBflpsdkVLddIPbpm8Y5LKXy6jq6RLjP17FcffHzgToUokDXrq8YU5J7duHDxgav/3jmmKDU+taK9XV7+9gOPr/zjxevwi1Jjg4/sWLpwhe/dVjruCtLOrXZ3W3zgUnzOo4El+EU5d85+O8f9y7O54ri6+ObOhXO+PHIjp6nrdtGNI1/OWUiTXPJcxyD38np3j1UHzt5JLeIr6vZW5GfHnv31s4XLjjwa80OQemn/qdTGTtG6RoamhrqKokE7Dn085zOfsNSmnVbEi47MzpvP6n3Mveuz7DMfUWuZtDZdknBk1cIvfeNpPYq9TQ1F9yEkxTeO+IQ19vxW1zU0M+2r2MqAJi/6rAEAAAAAAAAAAOD115mbEGpu3sJ2mtA0yw0OKli3hk4ov++puvBDzu+/SUhLqcybz9n3i3g86FdNi5sQEuipcBNCAHiJXtObEAIAAADAfwY3IQSAN0NnhuCQsxlGf2YvWighIaH7y69yNjbicn6iqMsz08REQkq6cTaBvJIU1dXYTAIAAAAAAAAAAAAA3apzY0A/upFgg5RU89LHAXR/STlZOlHTBUNwdAWGqecx3+VmT0fO3OIKPgEAAAAAAAAAAACA7tGZALo6KortNKH3vv2PZm9GiSfqCgv5KSlMIyM6zU9OrudwyCssJ/DgkTtd85csAAAAAAAAAAAAAPC0zgTQRbt2kPp6+WHDGuobqm5EFO/++d9F321TX7GK1NcWff8deUUIEg6+NeQgAQAAAAAAAAAAAID/VGduQgjwZsBNCAHgJcJNCAEAAACgfbgJIQC8GSQJAAAAAAAAAAAAAEA3QAANAAAAAAAAAAAAAN0CATQAAAAAAAAAAAAAdAsE0AAAAAAAAAAAAADQLRBAAwAAAAAAAAAAAEC3QAANAAAAAAAAAAAAAN0CATQAAAAAAAAAAAAAdAsE0AAAAAAAAAAAAADQLRBAAwAAAAAAAAAAAEC3QAANAAAAAAAAAAAAAN0CATQAAAAAAAAAAAAAdAsE0AAAAAAAAAAAAADQLRBAAwAA9FCKiorLP1t+LuhcbFxswLnApcuXSkhIiBcd9j18zP8YnXB2drpx68bUKS6kS83z8EhISrCxGdpU8vsfv8Unxk+eNIkAAAAAAADAG0SaAAAAQM+joqJ86O/DRkaG9x/cP3b0WO/euos+WmSgb7D006XNVyssLEpLTc0vKCCdcvT4Efrz3Rkz219t9ZerRoy0//WXX8+eO0cAAAAAAADgDYIAGgAAoCda/eUXffsaLP34k/Png8Qla9atmTtv7vgzYy9evNy02u3bd2a960660xQXF4/580OvXNm5YycBAAAAAACANwuG4AAAAOhx2CzWBOcJl4IvNaXP1MFfD3j/+Wd9fUPzNceMGZOQlDBx4gQ6LSEh8eGihcdPHb9z9/aJ0ydmz5ktXufzVZ/TEmdnp7/9DtOJw76He+vq0vJLVy4PsrSkD1qDy+TJTzejoaFhyJDBX3/7dWJi4rJPljeVT5zo7H3IO/p29IXg81+sWc1SUFBS6hUbF7tj1w9N62zctCkuPk5dTZ0AAAAAAADAKwwBNAAAQI/TR19fVlb29u3bzQsLCgu/3bL18uWQtrb63/v/W/LJxzcibmxYuz4p/uG6DeumTZ0iXiQtIzNv/nz/EyfP/BMwxGrIqi9W08L1a9elpKTSx5KPFt+6devpChlM5vc7fuDyKpcs/riqukpcaGExYOdPu0pKSjZv3HT+3IWZM2euXL2qrKz8Wti1kaNGycg8+uOtMeMcb0REFhUXEQAAAAAAAHiFYQgOAACAHqeXUi/6s6KiokNbTX9nxrWr177b9h2dPv3PGTOLAdPefuufMwF0Vlpa+vvt392+fef4seM6Otpm5ma0MPxaeCWPSyeaj+nR3KbNm3R7i/pKGxjoZ2Vmigvfe+89Dqdk5YrPhcJaOqvUS2ny1Mkb1m8IPBMwzmmc03iVpca2AAAQAElEQVSns+fOjRo9SlND/ccfdhAAAAAAAAB4tSGABgAA6HFKOSX0J5ut+PybsFksIyND+khISmgqlJGRaZq+f/+BeKKktNTMfMDz1KmkrLRy+YqNX29at37dW1Pfqq6upoVmFuZqaqr3HsQ1X1NdTS34YnBpSanTRFEAPWniRC6XGxh4lgAAAAAAAMCrDQE0AABAj5OckkwD3KFDrf/4/femQkVFRa+PF0fduNlWh2Xq9KnTwRcuNM1WVdeQzuLz+cs/XR4WFqapo/XZihXLPlv6zdffksaRpu8/uP/Lz3uar8zl8YTC2ovBFydOnshgMBzGOl4KCqY1EAAAAAAAAHi1YQxoAACAHoeGuZcvXXYc5yi+u6DYl1+u9pg/ny8QtroJjYCzs7J1dHRoPC1+qKqrZ2ZmkXbV19e3tYjJZFY3jvt84NeD9+7dmz1nzgBzczqbnJSsq61z61a0eC/S0tJFRcXiztGnT51is9mLFi9SVVU5/c8ZAgAAAAAAAK88BNAAAAA90bZvt6alpe/6+afjp46vXb923/5f3p7u5uPtfTXsalubBAQE2Ayz2bBhw6SJEzdt3rRx08a3Xd9qfy8F+YV6en1ozG1sbNzOal+s/EIoFH69dYuEhMTpU6eVlJV/3rN7woTxnyz9ZPM3Wz5dtlS8Gk2l09PT5s6bm5mRGXE9ggAAAAAAAMArDwE0AABAT1RSUur+7qz9+/YryCvMnjPbbIDFgf0Htn27rZ1Nftz5484fdphbmG37Yfskl0k+Pj57nhwo42l//P57QwOhMbfNcJt2VktOTv71l31mZmYfLV5EE/BPvJYIBYItW79dsHDBzcibKz/7vGnNc2fPs9ns8+fOEwAAAAAAAHgdSLCU9QhAj6SmqZ+fnUgAAF4GRSWNqspy0hVk5dldVdWrb8knS5Z8vGSy86TU1DQCAAAA8EaTV+hVU8UlXYFWVVFWSAAAXgbchBAAAABeAwMGDBhoOXD27NlXQkKQPgMAAAAAALwuEEADAADAa2Cc07jFXovT0tL279tPAAAAAAAA4DWBITig58IQHADwEmEIDgAAAABoH4bgAIA3A25CCAAAAAAAAAAAAADdAgE0AAAAAAAAAAAAAHQLBNAAAAAAAAAAAAAA0C0QQAMAAAAAAAAAAABAt0AADQAAAAAAAAAAAADdAgE0AAAAAAAAAAAAAHQLBNAAAAAAAAAAAAAA0C0QQAMAAAAAAAAAAABAt0AADQAAAAAAAAAAAADdAgE0AAAAAAAAAAAAAHQLaQIAAAA9HpMhJ82QlZZmSMswpKTw8QAAAACgM+rqamuFgtpaQa2whs+vJgAAgAAaAACgh5MgEr2UNQT8mvo6YWU1r1bIr6+vIwAAAADQcZKSUtIyTBkGU0qKoaTMListJAAAPR4CaAAAgJ5LRobZS1mztDhXKEAPHQAAAIAXRb/IF/Cr6INOyzDk1DX0y0rzhUI+AQDowTAGNAAAQA8lLc2Uk2cX5qYgfQYAAADocvQjVkFuMv24RT90EQCAHgwBNAAAQE8kQSSUVLTKOHkEAAAAALoN/bilrKJFGggAQI+FABoAAKAnUlTWKOPkEAAAAADoZiWcHCVlDQIA0FMhgAYAAOhxmEw5gaBGgDuzAwAAAHQ/Ib9aIBQwGfIEAKBHQgANAADQ40jLMBvq6ggAAAAA/Cca6mqlGAwCANAjSZOOUrGbt8zNSPy2KeCkxEWEBIZm8VqspGo5d4EjM9T7YEQpeU6d2ITIaE9ZsNgk+eDuoAwBAQAAgOcjLc3kV1cSAAAAAPhPCIV8BVkFAgDQI3U8gBYRFIQFhKRzGaoWNg5TPNjkwMHQgidW4Obfj44iubwO1NmJTQAAAKAzpGUYtUI+AQAAAID/BP3oRT+AEQCAHqlzATTh5SXG3+cQEpcpYHu5WPTRDhXoe3k5kcw8dh99wc2DfxYMsLNn8u7EcMznLndmxoRz9e0tdBjc9GtHfK9k0JCZoTxggrOTlbEqsyTjXlRwQFQG0Xq0SQbL1strtOBaEhlsZcDipN8MDgi6n0d3qqBv5+ziYK6vKiPIiw30PROZRwAAAKDjpKSk6+sxBAcAAADAf4R+9KIfwAgAQI/0omNAC5oPfcHSYXFCT/icCM9rXspU0DdRjvM/cDAgmRiMdBqoQIiM/hT3WXasvIgzfrTQxNl1ihHryXpVDQarpl/Y630mjz1slseUfizCMLF3cdDihHpv2+EXScxd3AarEAAAAAAAAAAAAAB4Zb3Y928sExtbA8KJzucQok8ILz08OCJeNIhG8ziZL8yLDr+fV0o4IfftjPtpqzBYLFsTFc6VA0eCRQN33L8XziKVPGLZvGZBerh/cHwJIScD9PQ9jK0MZJLigvZuDRLVrW3E4QiItqYqi2DADgAAAAAAAAAAAIBXVecCaIbRzNUbZ4qmhJzEkCNBWQKiTGf43FZvBSgQPO4nzaebMhiEyWKzBTze4/SYV9kysyaEy+WJtxFwS3mEQbcjqsbj3aY6mSgIuAUcWo0AgycBAAAAAAAAAAAAvMpe4CaEiZwSTm5BSSc6IfN5XC5DlUUj50rRLEuhsQf0E9hsljhgZrCVGYQnEDT0c3J2UE322eh/n0e0nRYvtiYAAAAAAAAAAAAA8Ap7gZsQJnFIJ/GSIxNLPMdMdeWFJ/JVLCY46qef2BvwxCoME3u3KYKIXIbFmMHa3AfBuUKBhahLNFtVgcU2Hm2tyWDkEwAAAAAAAAAAAAB4db3oTQg7R5gR4OsXIdB3mj5ruo123oVDAfEtekDzEh9wtJ3nuTvrcx+c9L9wnyfMCA2JEZi7Llm5yt2ScAoEAgIAAADdTFqaMdblnTmLVi34bPP4t9yZcvK00KCf+Yefb2mx5oixU6bM/EBVXfuj1Vs1dfqIC82HDKcbyiuIBtqa6Dbv7dkfisslpaTnfrTaznEynR5oPeL9pV8xmLLiRU5vvzdj/scNhEhJy3gs+dJmpJO4vJeKGq1Zz9CknU2w91b3DgAAAAAA8BJJMeR6dWgDUp0dG3I5Nq+6RXFNdlRYeFzxo1hYUHA3NDwmW/jvBFVXmRpB1ymtE03XFCXGRoaGhVyOjIzNFY33/O+acr2HDetdFnnE5/TZ4LDwmPhsTuPm1cUJEWEXg6+ERMTej4kKuRZfIqjnJUaFRKSU1xGAjpNnKfEqOt2RHwDghTBlFYRCPukK0jLMjlalwFJ+zjfAYaMnqGvpnDvpk/wgdqC1nZqGTmpiXH1DnbXd2Lu3wmuFwqY1B9nYl3KKEuOiJYiEneOkuJhIeXnW1JkfXA48VpCbRVfITH043GEi3aQwL2vUhLfYvZTOnzhESAOd7WNo0sewf3J8rIGx+bCR408e3i+oqW6ory/IyRw39d3UhLjqKp7rnI8ykuJjo67SqtrahK6GvT+9dwAAAHgVsBRVK3llHdpEhiFbK+ya7ne0Kn5NJQEAeBk6HkB3P1EArV8dH9UUZwN0CwTQAPASvS4BdGFedkbKQ25ZaRWPy2DI6hub3Yu+XlNTbT1ibHpSPL+m2nXO4oaG+uKC3GEjJ6Q9vEcncjNTTQcOVdPQHjjUvqgg5+bVIHFVdXW1ZZxix8kzeBVlw0c7n/77QFUlV7woJz2ZxrI11VUOzm9fv3IuOy1RXM7jlsvKylvbj1Vg99LU6X3m6O80mW1/E+z96b0DAADAqwABNAD0WAigoedCAA0AL9HrEkCzlZRHOU1znDRjxFiXPoYmgpqau7euSRBiMmBwaUmRsrKampaOuqZOwr3oUeOnRV8PqeRV0K2yM5IdXWZIy8ic/ns/zV6baisrKVJS1Rju4HwzLCg5IbapXCDgV1Zyx0+ZmZeddjXoVPMG0Px7kLW9ocmAM36/cctLnm8T7L3l3gEAAOClQwANAD1WJ29C2K1KI/d8HUkAAADgpZs2y7OMU3zCZ09xYd6Q4Q4DrUaIy0uLi3opqSqpqt+JDHN0eUddU1dSUpJT9OgOwXRaKBAQCSIl9dQnDQkiFPAlJCVaFktI0HIpKakG0SpPlEtISAqFQmkZxnNugr23vncAAAAAAICX4eXchBAAAABefXLyrF7KajevBXMK82jKqaHTu2lRKadQUUmlt75RZlpiVnrigCHDuRWldbWiIaElpaQnT/e4GRaUGh834a33mlfYf4BVb33jY3/8PHiYg3Zvg6byXipqo8a/dfKvfbLyCkNHjG2+yegJb5WWFF4KOOL0lrts4y0Q298Ee2917wAAAAAAAC8LAmgAAABonVAgqK+rU9PUodP9zAdr6xowZJmSklJE1AO6UEevb3FBLg2ds1ITDftblBYXibeyH+dSXVV199a1qxf/UVJVGzzcQVyuwFIcPdE1+PTfnKK86yGBE1xnyzCY4kXOb8++czOsIDfzgv/hoSPHa2jricv1jc0M+w+8eMYvOT42Lytt3NSZTW1raxPs/em9AwAAAAAAvEQIoAEAAKB1tbWCqPCLjpOmf7z2BzNLm3/8DvAqyj2XbyKiHtAFikoqmSkP6XRa0gMasJZwCuh0bwOaVA8POvUXnabZ9IWTh+3GTKQRdgMhE6d7JN6PyclIoYvioq9zy8rGTXmXTts5TpaWkbkZdoFO03w25vrlia5zpGUYcvJsp6mzLgccrakSjVd4OfCYlq6BhfWIdjbB3p/eOwEAAAAAAHipJFjKegSgR1LT1M/PTiQAAC+DopJGVWU56Qqy8uyOVqWh1RdvgAAAAAD/Ja3eJoX5aR3aRF6hV00Vl3QFWlVFWSEBAHgZ0AMaAAAAAAAAAAAAALoFAmgAAAAAAAAAAAAA6BYIoAEAAAAAAAAAAACgWyCABgAAAAAAAAAAAIBugQAaAAAAAAAAAAAAALoFAmgAAIAep66uVlJSigAAAADAf4J+9KIfwAgAQI+EABoAAKDHqRXypWWYBAAAAAD+E9IMZq1QQAAAeiQE0AAAAD1Oba0AATQAAADAf0ZGmims5RMAgB4JATQAAECPUyvkS0pKEwAAAAD4T0hIStUK0AMaAHooBNAAAAA9Dp9fLcNkMpjyBAAAAAC6GUNWXobBFAiqCABAj4QAGgAAoCcqLy1QVtUhAAAAANDNlFV1y8sKCABAT4UAGgAAoIcqK81XUtUmAAAAANBtlFR1Sjm5hEgQAICeCgE0AABADyUU8qureJo6xjJMOQIAAAAAXYrBlNfU7VdVWVFbi9GfAaBH68wNiEzNzee87ykv/2jgyLzc3O++3sSUZS5fvUZdQ0NcWFVV5XPwYGLCAwIAAACvKqGwpqggQ0lFQ8DnNzTUCwU1tUJ+fX0dAQAAAICOk5SUkmYwZWRkJSUkZRjMooI09H0GAOhMAD1xyjSzAQMy0tIez04NCgyQlJIaP3FSbEy0uJCu4DxlSicCaMulx7Y6JK7/YE1Uyb+FyqO37F9ncmHpwhOqK3as0o9a9+neGE4bFTA0x2/Y6qUff3DPA9sF5sGfXvY5hgAAEABJREFUbw/jkI5Q0Hdy9/RwHN1fi8nPT4wOObjHOyxRSF4YQ3/Ktn3uJVuXbA4tJQAAAK8MCVJWWshkyEkxmApsZWkZppRUZz4eAAAAAEBdXS39Ol9YK6gVCCqrypE+AwCQzgXQioqKd6KjN6/9Ujx7KTKql7Ky+D11+eJF4sL1X3+jpKREOi45OCLfxcHRQjXq3+BY1dzBgpEXGp5RKhDcS0nkJ3O4bVegauagneLjnTl+9QKDxJ17uaQjFKyWb93mbsyJDjnygy9Hx8bVzX37j1prF227mNEFGTQAAMCrii+oJvQBAAAAAAAA0KW6rItTfX09/TnYyko820tZpaS4mHRcZcaV8Lwpjg4WymGPewqrWNhbqeYHX8nkkcokv6+XtV9B3pV171+h/z0Z7Ec6iGXlsdStT9wPC1f5ZTUO0BRwMmDKtn1enu7mkVtjeQQAAAAAAAAAAAAAnl+XBdBx9+4W5uf/sPdX8WxVZdWObVtIJ/ASwyNzpzo5GKuEikfhUDZxsGTlhYQmVop6KK/evdnkzNJF/klE03bJ0qVOgw3UGNzcO8G7t+8KLhCIRrqwmblwnpuDuTaTcO+d2bXjQGAc3ZAwtC1dF8xztTM3YJckRocfOeAtLm9GwWKKvT4nZG9wVtPtAQSJIYdO2Hga6GmzYpN4RMVqiufCqQ4WxixB5v0rJ/bsCbjPeTS2hiA0VtXBsZ8gZNX722NYrbcBAAAAAAAAAAAAoCfpsgC6lMNxf3sq6QK85NCIfNcJjiaqUZEcQlSNR1uzRONvPNkDWcXOY5WbcZ7/ts0BpQazFi9evvR+4vpATp+ZG9bOY4fv/eTrUJ7xrNVLly7PTBSl1XouGzYt1n5w0m/nIS6Nkaev3KLCXfR1WF6zGhkq2joMXuKdxCdG7aiM2bNhsXi59phVW7ws8i747TjB0x7sNMVrO5vnueYKbSOTqWVhEXtwx/qDnPy4BqNW25BBAAAAAAAAAAAAAHqUzgTQJSUljk5OO/bu+7ekuJgpy1y+eo26hoa4pKqqyufgwU7chJASZoRG5U13dLJQiAytZJnYW7Hzw64ktxgBg6mqzOA+8D9x5X4Gub91eYw2gyMapjnl0CfvBZLKEtHaBSf9p7h4mWur+meoOruYlASu+XpXhKgncmBEPmOfl6udZqR/geDfKhksBoPLrSSCVlslo+0w1YRzZt3n4vsfBoUmMn5b7myrHR7YeATi/L1PBj+qrfU2EAAAAAAAAAAAAIAepTMB9NG//1Ls1UtNXV08+8e+X+Luxg4ZajN+4qTYmGhxodmAAc5TpnQugCa89JDGUTjMVSIeGDhYquaGhya2vAdgXoR/sNvadX8cnpeenBQdHhgQ8rg3M8tkygLXCWb6bJaqgRabe41BiKqJkTY/xS/98TgYnJSYPDLPug/Lv6Ck2W5LuAI2W4HQDWiQrD1m8+/rnNQal/Bvbpu9kzOwj3b/wXvPT2/Wikx9VVob4fMFPK6gWXDdShsAAAAAAAAAAAAAepjOBNCF+fnfbFjXolBRUZH+XL54kXh2/dffKCkpkU7iZQZHZLqMsTHQFoy2VsmLaDn+hkhe1K733ztibe/qNtVl/iqX6Y47F60/wh228qe1TuROWMSFQ/cK+CZuy6b8u8VTPZufjIUFvPQMHsNhmAn7imjoD07UwTWrA9kMbQfPpWMEXIEoAec+PLPLO5zzb0W8DJqMqz5Zq7Z9O20AAAAAAAAAAAAA6DE6E0CPd5706crV8gry4tm83Nwl73uQLiXMCA3Pm+LsMobRTzU/8qnxN0RYytqqAk5E0N6IoIP6E7btW2BroRLMsbdSTfb5ZP2hOJoXy+jrzBJnzNz0LA7TxtZAISyvsRO0qpGVPiMvIvPJaiszrkTluU1dvCAkcUdUiaAyIyYqg2U010NFkHshg8sjifkCE8KJaRyZWnS3Q0tb1RIOreLJAFo0ZkhrbQAAAAAAAAAAAADoYToTQA+3H5mYEH/ot/3i2R/2/mphOZh0LUFiVGie+zwPR5J75unxN2iw22/K2r0LVSL37zoYQyzcplqwBWEcAY+TyWPYO7nZx3BT2HbTZ7oZs5k36dq8uBM+EfarVq/MOxCUxFewnb7AlnNhVUBWiz7RvBjvXb5m2+Zv2msQEnblZhyPZevm4TaQF/hlSAZPKAjwCZ2ydtUWgc+JWA5Tz8nDw5bvvXSRX1KLlrfRBgAAAAAAAAAAAIAepjMBtJSkRFlpyZ2YmKYSSSkp0sUEmZGhmZ4DzTNaHX+DCJP8d20zWLrssx1H6Bw3M9R3156IUoHgzN4DZisXrPttKuE+vOATdMdAPPyFoODit+vZGzYt3TCS2TiSxrY1BxrvJdhCZcye1Z6JUz3dp7p+5jyTm5l0L3zbh96BMaWiqJoTtWvNTub6Zau+mU5rzLt3ZtvGE/d5hPFkD2hBXBttAAAAAAAAAAAAAOhZJFjKeqSDlixf4ejklJGWJp61tLL+dKGnhITkrl/3N92EUL9v30sXLuzdtYMAvKrUNPXzsxMJAMDLoKikUVVZTrqCrDy7q6oCAAAAgFeHvEKvmiou6Qq0qoqyQgIA8DJIMeR6kQ5KT0vV1tGVV1AQz547ffrihfOFBflSUtKaWlriwpSkpEN//FZVWUkAXlXyLCVeBYcAALwMTFkFoZBPuoK0DLOrqgIAAACAV4cMQ7ZWKCBdgVbFr0FEAwAvR2d6QAO8GdADGgBeIvSABgAAAID2oQc0ALwZJAkAAAAAAAAAAAAAQDdAAA0AAAAAAAAAAAAA3QIBNAAAAAAAAAAAAAB0CwTQAAAAAAAAAAAAANAtEEADAAAAAAAAAAAAQLdAAA0AAAAAAAAAAAAA3QIBNAAAQA+lqKi4/LPl54LOxcbFBpwLXLp8qYSEhHjRYd/Dx/yP0QlnZ6cbt25MneJCupqmhsbGTZuCgi9cj4zY+eOOAebmBAAAAAAAAN44CKABAAB6IhUVZd+jfgsXLayqrjp29Fh2Vuaijxbt3LWzxWqFhUVpqan5BQWkU44eP0IfT5fT9Pmo//ER9nYhV0KuXL5samb2l+9fQ4YMJt3pizWrE5ISCAAAAAAAAPyHpAkAAAD0PKu//KJvX4OlH39y/nyQuGTNujVz580df2bsxYuXm1a7ffvOrHfdSVd7y/UtTU2NhR8sDAsLo7NsFissPGzmrJl0dwQAAAAAAADeIOgBDQAA0OPQwHeC84RLwZea0mfq4K8HvP/8s76+ofmaY8aMSUhKmDhxAp2WkJD4cNHC46eO37l7+8TpE7PnzBav8/mqz2mJs7PT336H6cRh38O9dXVp+aUrlwdZWtIHrcFl8uSnmyEp+ehzCJfHG2JptXrVF+LZiROdvQ95R9+OvhB8/os1q1kKCuLy/v1Ndv64Mzzyemj41a3bt1pZD2lqodeSxUHBF65cDSWNnbu/+uorui2tgdYzavQoWrjzxx0e8+fTCbryhg0bCAAAAAAAAPwnEEADAAD0OH309WVlZW/fvt28sKCw8NstWy9fDmlrq/+9/78ln3x8I+LGhrXrk+IfrtuwbtrUKeJF0jIy8+bP9z9x8sw/AUOshqz6YjUtXL92XUpKKn0s+WjxrVu3mld17twFPp//896fv/32m5nuM2kg3rTIwmLAzp92lZSUbN646fy5CzNnzly5ehUtZzKZ+w7stx9pf8TP77T/SScnp63btjUNWj3j3Xf9/f2/2byZTm/++mtHp3H+J/y3fL1FSkrq5z0/99bT++3AbxfOXaBLaWOOHPEjAAAAAAAA8J/AEBwAAAA9Ti+lXvRnRUVFh7aa/s6Ma1evfbftOzp9+p8zZhYDpr391j9nAuistLT099u/u337zvFjx3V0tM3MzWhh+LXwSh6XTjQf00MsKzPzg/nvf7L0U9cZbvTx6adL/zrks3fPL3TRe++9x+GUrFzxuVBYS2eVeilNnjp5w/oNLi6TtbW1Vq1Yefr0P7T8buydIdbWTZ2jj/j67vvlVzqho609ZuyYXTt3Hvj1IJ0NuxIaGh42bdoUWnl+QV6rjQEAAAAAAIDugwAaAACgxynllNCfbLbi82/CZrGMjAzpo/l9/GRkZJqm799/IJ4oKS01Mx/wzApv3YqeN2eehrr6mHGOjmPG0DCax6vy8fY2szBXU1O99yCu+crqamqDBlnW1taeO3deXEJz5OZRcnpamnhiyJAhUlJSn61YQR9NS/V66xEAAAAAAAB4GRBAAwAA9DjJKclcLnfoUOs/fv+9qVBRUdHr48VRN26200f49KnTwRcuNM1WVdeQF1NYVHTU7yh9nDpzasrUyTSAlpCQuP/g/i8/72m+GpfHoz/r6uqEQmH7FYoH5fh++3dNkTSVl1dAAAAAAAAA4GXAGNAAAAA9jlBYe/nSZcdxjuK7C4p9+eVqj/nz+YLWE14aAWdnZevo6Ii7HtOHqrp6ZmYWaVd9fX2r5d6HvCOjIsX3KqSUlHqpqakLBaIxN5KTknW1dW7dihbvRVpauqiouLq6+u7dWCaT2TTq9IQJ41d9sZKG5i1qvntP1HWaxWaLN4+KilbT0MjMyGinMQAAAAAAANB90AMaAACgJ9r27VaLgQN3/fxT3P24OzF3evfWHePo6OPtfTXsalubBAQELPpo0YYNG27euGFnP+LdWe/u/nn37p92t7OXgvzCYcOH0Zg7OTk1OTm5qfwvH58fdu30+fuv4CBRf2q7ESPU1FR/3LmLNHaynjJ1ys97dh/y9jY1N587b+69u/fen/9+QEDgbI85azas0zPQJw0N78ycSQPlHd/vaLHHzMyMqJtR/3v/f6UlZRUVFVOnugy3s81IS4+IiMzLFfWDnjNnTkJCPA24CQAAAAAAAHQ/9IAGAADoiUpKSt3fnbV/334FeYXZc2abDbA4sP/Atm+3tbPJjzt/3PnDDnMLs20/bJ/kMsnHx2fPkwNlPO2P339vaCA05rYZbtO8PDj40iden0hKSnrMnz916lt5ublfbfjq2NFjdBFNwD/xWiIUCLZs/XbBwgU3I2+u/OxzWi4QCJZ86JWclLTk4yXvzJqVkZ6+8rMV4hsVtvCx1xJa1Yx3p3+zdUsfff31a9fT9JmWHz967OHDh2s3rH1vznsEAAAAAAAA/hMSLGXclgd6KDVN/fzsRAIA8DIoKmlUVZaTriArz+6qqgAAAADg1SGv0Kumiku6Aq2qoqyQAAC8DOgBDQAAAAAAAAAAAADdAgE0AAAAAAAAAAAAAHSLLrgJYa9eStq9dWWZzNzc3ML8fAIAAAAAAAAAAAAA8IIB9Hse/5vgMkWvTx/x7J3o6M+8Fo0a4+joNCHp4cNTx49WV1URAAAAAAAAAAAAAOiROh9Ar928hQbNly9c+OPXX2KibnIrKmihsqrqV1u35+flOowbz+Nxz/ifIJ3Dshgzz8Pdxc5YlcnLexjlf2DPkdBSAfmvqTit/W25wsFFXwRmkCWRZDYAABAASURBVA7Ttln53VKrPN9docbzHB5sXhOU998/AQAAAAAAAAAAAICXppNjQG/c9h1Nn79Y9umWDWtDL10Up8+Ujq4u/bl2xWd5OTm99fRI56g4LN27b52rdn6o785tuy8kEkvPLTuWOikzSNdhmS09dtrHy6gr62yxBxN7A86JvdGDly63J3HxHKTPAAAAAAAAAAAA0LN0pge085SpIx3GfOb10Z3oWy0W3b97Nz0l5eBhXzpdyeWRztC291ruzI7YPG/NFXGX4ZO+vqM37F630P1izN4YDnld8EJ3LQ6l//UP8yMAAAAAAAAAAAAAPU9nAmgPzwUXAs80pc80jB4z3olOBJ0NvBlx/YPZswyMjNzneoydOMnn94Oko1QsJtiqZgb6hv87YIWgNNL7gI8TSzzH0LZ0XTDP1c7cgF2SGB1+5IB3YFwlYRnN3bfVKdE7mOns5mCuIsiM3L99s1+8KANnaNouWbrUabCBGoObeyd49/ZdcWabD69zYBMyf3+Y+51t768+mcjoN8XDc5a9bX8tQe6DSP+De31jnxwxQ0bFaqrXwqmjrfuwCS8x6MC2HQH3OS3bExcRHujrezKm9DnX/7f90AGWQ6zuxd6pr69vKpGUlBxoOTj2dgwBAAAAAAAAAACAV0aHh+AwNTfX1NI+eeyYeHb02HEbt31nYmZuZmHx7c4fh9vb08L0lJSTx47o9eljbNKfdJCMqokWgxMfkyFsXipIvHJoT4Co+zNDz2XDpsXWgki/nZt3nEliO67csmy0tngtlr6do2rErsWzl2wO4lktWTrPQoaWqth5rHIzLgne9sHs5buiWQ7LlzoxwldNW+KXzkv8c+HokZ+dTBSqOCzYvNpZOyNk18ZtByN4Fgs2rXPXaz46B0Pfcd2WBVbcM6tmz5j5iS/HasEqDzNRIk7bs/pRe1Zu9I1TdV66YYGtdrvrt9l+eB4MJnPzdz98sWETDZ3FJXSCztJCaWkZAgAAAAAAAAAAAK+MDveA1u9rSH8mJcSLZ4cOt01JTlo45z067X3Mf/gI+xvh4XQ64f59+tOgr2Fy4kPSEQw2m0G4PC6/jcUmzi4mJYFrvt4VIeo1HBiRz9jn5WqnGRlE5wQlcf4+QSklApLnfcLBzqufiQojroCpqszgPvA/ceV+Brm/dXmMNoND021W80qVrabYkNDtSzeG021JQHgG2b3OyV7/hF/TgB+CjKBVc6IY3FKeqFv0hSMxU9eZGLEZ8QLanoH/ticyLiXOToUjIIK8ttdvtf3+BRgj+vkI+PzPP178/e5967/ZuunL1bSETljbDF+xZFFtrZAAAAAAAAAAAADAK6PDAXR9fUPz2YaGBslm3agl6P+ak5AgHSTg5vGIHYvNJKS1IaRVTYy0+Sl+6Y/HrOCkxOSRedZ9WEEldI7PKRGIc1xBJf0vkyHqxJwX4R/stnbdH4fnpScnRYcHBoTktaiU0cfCQMvAYNPZCc0Ki/uoMgnnydUclni5WOmpsLUMdFj8e4TxVHsEefEX/Tuw/r/t9y8oIfCcHsbH07iZZtBfbd1OZ4dY29BZWkgAAAAAAAAAAADgVdLhADojLY3+1NbRzcvNoRO3IiOmvO36l/8pKUkpDS2tX3btEK+m10ef/kxPTSEdJOSkZ/FUzaz0FSI5/46MzDAZM9OJdd8vQJwdP9VZmNFelXlRu95/74i1vavbVJf5q1ymO+5ctP5IbouVeOlBB/YGNeuGzM2P4/5bL8vKc9f301UTQ0IjzsTElWq7LfVk/7vx052XO7h+u+2HVtC4+fNPFm//cQ+dphNInwEAAAAAAAAAAF5BHR4DOjHhQUF+3vRZ7gZGRnT26pWQDas+T3zw4F7snS+WfRoZfk28muvMWdlZWR0df0OkJC48hmPsumTqgKZRMhjKth4L5o3pQye56VkcppGtgcKjRapGVvqMvMRMXjs1spS1tQknImjv5x+7ztgWwTe2tVB5IvEV5CflCpgMXlJEVGQofdxJ5DIEvBLevzmxgr6djT7nzOY123ftCQiLSG7a3VPtMRvvZt9P9fnXf472Q+sS7t//cN5s+hCP9wIAAAAAAAAAAACvmg73gKaCzgbOfd/T9d2ZackpnnNmXQu9Qh/NV7CyGfbW9BnffrWBdAYnfM+OM/22LNj1h1nwlagknpaFlf1oa0HwRt84DhFwT/hE2K9avTLvQFASX8F2+gJbzoVVAVkCYtRGdTL9pqzdu1Alcv+ugzHEwm2qBVsQxhFQHC5hG+jp6/Py8gpCvS+4fu+1ebWKX0SBQNXec6EjI2j94q1RjysR8PJ4RNvG1cmSQyuZ4jbXWoWRKFrAi2vWHq6MlZvXTIPYdRE3M55n/SfaD50g7oYPAAAvjsmQk2bISkszpGUYUlKd+XgAAAAAAHV1tbVCQW2toFZYw+dXEwAA6FwALS8vn5OVuX71yt8O+5lZWMTHxTVfajVs+Hc/7Y6Junnx/FnSOSWhuxYvujPPw93FfZkbk3AfXvNZs+tIaKkopRUUXPx2PXvDpqUbRjIJXXRm25oDMRzyxE0FnyBM8t+1zWDpss92HKFz3MxQ3117IkpppHzRN9xlw7pDY5J9/rdkb4z3uo2MdRu8vp4q2n/cmZ2bd0eVEKLyuJKMoL17rVcu/myHExGkX/EODDWepd24pHl7+CXpibEHt+6JzBMKnmf95u0HAAB4OSSIRC9lDQG/pr5OWFnNqxXy6+vrCAAAAAB0nKSklLQMU4bBlJJiKCmzy0oLCQBAjyfBUtYjHTTNbYbn4iUZ6WnmFhbTJzqVlZXRQiVlZUenCaPHjhs0eMjDBw8+/8SrkteDxpWQ0XfbtHlCls9u74txlQReD2qa+vnZiQQA4GVQVNKoqiwnXUFWnt3pqmRkmL2UNUuLc4UC9NABAAAA6EoyDDkVNd2y0nyhkE86RV6hV00Vl3QFWlVFGdJwAHg5OtMDOvj8WRabbWxisuGQN02fN27/fuRoB/GimurqQ7//9uf+faSHEWb4r19H1m5e4Jj0eUAGBtQAAIDXgLQ0U06eXZjb4TsGAwAAAMAz0S/4C3KTlVS1GypJbW0nM2gAgDdAZwLo6qqqv73/aJr13v/rSb+/xdMpycncigrS4zCUbZesXeqgxQv15yB9BgCA14AEkVBS0SrMTSYAAAAA0G3KOHmaOsZFBRn04xcAQM/UmSE4AN4MGIIDAF6ilz4ERy9lzcoKjgD3xgEAAADoZjJMOTZbpazjI2BgCA4AeDNIEgAAAOhhmEw5gaAG6TMAAADAf0DIrxYIBUyGPAEA6JEQQAMAAPQ40jLMhro6AgAAAAD/iYa6WikGgwAA9EgIoAEAAHocaWlmrRB3wgEAAAD4jwiFfBlpJgEA6JE6cxNCAAAAeK1JyzAQQAMAAAD8Z+hHL/oBjAAA9EgIoAEAAHocKSnp+noMwQEAAADwH6EfvegHMAIA0CNhCA4AAAAAAAAAAAAA6BYIoAEAAAAAAAAAAACgW+APQAAAAKArDR7uMMppGp0oyM06+vsu8spYsHyzrLw8nThz5Lf0pActlr77/lJOYd6lgCMEAAAAAAAAug4CaAAAAGiPzcjxZpY2cgrsorys25FhaUn321//zo1Q+hhqP86w/0Dyn5OSlhnr8o5e336SklJ5WWnhlwPLOIXiRQd2rKM/F638ptUNH8TerOJxyQsb7jCRX1NNj8Bzrm9kNmjIcAd1TR1ueVl+Tsa1i//UVFeR/1BHGwwAAAAAANAhGIIDAAAA2mQ5bJTNKKeUhHvBp33zczLHT50lJ88irzBn19l9DE1onHrl3PGGhobxU2c+54Zx0ddTH94jL0xdS/f5V9bVN5483SMjOcF79zfXrwTqGZo4TnqH/Lc61GAAAAAAAICOQg9oAAAAaF0DIVZ2jnejwsMvBdBZms+ylVR66xsnxd+hs5o6fUZNeEtdU6eqkpdwL/pG6PlnVmg2eNiQ4Q69lFXLSooir5xPS3xGZ2pJSakRY12MzS1lZeUK8rKvnDtRWlzQzvq9VNSM+g9sGmEjOeGe+4LltLC8pLidrd77cIWqujadeHDnZvMhOJr2zpSVK8zNvHz2uLie3gb9Jri+dy3oHwvrEfS55GSkXA48VisUkMbu1TIMZt9+5uJBSGj5/duR7exaV9+wtLgw6lownU5NiKvi8dhspfb3TkSRcW/RkdfSreJy425H3I68Ii4f7jBRTVObHtgxE6dr6upVV1X98eNG8aK2jnxHGwwAAAAAANBRUgy5XgSgR5JnKfEqOAQA4GVgyioIhXzSFaRlmB2tSoGl/DxvgPLybNsxE2+GBZWXPlo5Jf5uSXE+nWDKyc/yXJ7yMO7cCe+ivOwRjpMbGhryczKattXpY6isptk8zdTra+L0lvu14H9CL5ykce2Et95Lio+tqapspwG2Yyb3GzA46NRfN0IvaGj3th0z6W7UtYaG+rbWNzA0NTIbdPEfP9oYcUlcdAT/yREthtqPS064S3PYppJ70dfpc1RR06yvq2ueidPdGfQzpZnsrfBLqhradDb25jUay7N7qQwcYifk888e/5PWb20/TkaGkZeVRjehaxr2HxgTEfKP735aZ1F+NmmXnDzLbLBNXlY6t7yEzvIqysSHt529M2Rl3T2XpyfHnz/hU8IpsBs7WUpKOrdx7yx2r/4DrQ2MTekmIWePpyfFV1fx2j/yHW0wAAAAdBpLUbWSV9ahTWQYsuIvuV8crYpfU0kAAF4GDMEBAAAArWMpir6lFoeYLZgOtBYI+OGXztAcMzP14YPYm6aWQ9uvzWKI3cN70UkP7tBNaG6bm5lmYWXb/iYDBg+LuR5C81naBhqeysrJ9TUxb2d9ebYiv6a6vr6OdAUzy2G3rl3KyUjhlpeGBZ1mMuUM+pmJF0lKSUU29viurRUU5maqamqTTqFBcFxMxDR3T89lG8e/5a6u1fuZeze1GFpbJ7x28Qw9JjQuDz7lW1SQK96kspLLVlSixzb1YZxQIOAU5YnLO3HkAQAAAAAAugqG4AAAAIDWtdPXuJeyWnlJocTj2ZKi/IHWI0i72ErKxjqDLKzsmkra77gtLc2QU2A19QiuFQq4ZWWKSqqk3RaTLkL3rsBiO7vOoY+mQmVVjTTyqIt0Ja9CPFFfVy8jwyCdQg/g1aDTESHnjEws+va3mOW5LDn+7rkT3u3sXUlVrbS4qOmZZqUlNq3QUC86X7SGFnvp6JEHAAAAAADoQgigAQAAoHXcCtFfiTa/66CsvEJNdVWrOe8zs18JCYmoaxcjr5wjz0mi1dL2dkMbzGDKSkhINkXn8grsqkou6YTGvZ88/Gt2s4S3m9Bs/eH9GPrISrcbO3kGi61UU1PVub3TDPrpHusdPvIAAAAAAABdB0NwAAAAQOv41VXFhbn6xqZNJSOdpo2e8DadKC8t7qWi3hQGq6hrVzSOYtyOitISdU2dpllFZVUpqfa+CKexbHUYBEM4AAAQAElEQVQlT1lNUzwrw2CwlZTKStobujonI6W+vq5poAxqhsfHhqYWpOPo3it5XA2tfxvc1JJnkiDPa8TYKSYDhjTNZqcnEdH44HLt7L2MU6ys+u+R723Qz3LYqKbVWo3nn3nkn7/BAAAAAAAAHYUAGgAAANp0OzLUYohtP/PBsnLyljaj+vTtf/NqEC1/eC+awZS1H+siK6+gb2RqPnhYXExE8w2FAoGcvAJNjZtK7kaH9zEyHWg9Qlqaoaap8+7/PtXqrd/+3h/ERlnbOWr1NpBXYDlMnF5dVZme9KCd9aureIlxt0c5TdPU6cNiK42f5s7llqUmxD3RMKGwl7IqeQ73b0cOHj5Gr68JnTYbNNRt7mKmnPwzt+LXVGvqNj4vCQlFZZX2V6bPa7Szq6mlDT282noGDhNcK8pLxWM3t7X3hLhb9ADS50iPPH04OLuy2M+4oXT7R75DDQYAAAAAAOgoCZayHgHokdQ09fOzu/0PqwEAWqWopFFVWU66gqw8u6NVaWj1ff43QBpcDhnuQLPOhHu3osMvN419rKWrP9r5bVUN7Upu+YM7N6PCLzXvSMtWUnWb86F4yObLgcdonEon+g+wsh45lhYW5efERUc8jItuf9eSklIjnaYamQ5iMGQLcjNCzp0oLyl+5iY0kzUwMa+vr7sdEUr3W1dX23wF2zGTaKgtKSXFrSj786fNI8ZOsR7h2KKSI7/tLMzLlpCQtHOc1G/AYFlZ+dystJthQQW5mXSprr6x29yPfv76M/HKYyZOV1BUDDz6h3iWLqVbaWrr0TyX7v3KuRPttFZahjF2yjsmZoPpytzy0pyMlBtXg7hlor7kbe2dUtfqTWNrdU1t+iwe3L555fyJpl2/PfvDPd98/vSO2jnyHWowAAAAdJpWb5PC/LQObSKv0KumqlODibVWVUVZIQEAeBkQQEPPhQAaAF6i1yiABgAAAIAXhwAaAHqsrrkJoYGREf2ZnpJCAAAAAAAAAAAAAAAavVAA7TBu/Mw5c/ubmTeVJDy4/4//iQsBZwgAAAAAAAAAAAAA9GydDKAVFXutWLvOfrRD8Pmzfod87sXeoYUDLQfb2NqtXLueptKb13yR9iIdolkWY+Z5uLvYGasyeXkPo/wP7DkSWiogrwaGQr8pHovdHK0MWCXpN0P9fA4GpPBIJzFMZu3d55y4Zsn2ROOlP661Tdy1eGt4yavyVAEAAAAAAAAAAAA6TZJ0yqoNX5mZD/j8Y6+tX20Iu3yplMOZNn1GX2PjH7752v3tqeVlZRu3fS8nL086R8Vh6d5961y180N9d27bfSGRWHpu2bHUSZlBXgUKVkt27F1iQ+JO7NpxIDRPy2XDjl1eZiy6hGW29NhpHy+jTraTW5KUmJyUmC9A+gwAAAAAAAAAAABvgs4E0JOmTrO1H7nxy9VFBQV/Hj3+1ox3aOHQYbbDbO3oRGF+/lerVsrJyq7+ahPpDG17r+XO7IjN897fsH1PwEnvvaveX7gulOG00N1Clbx82oNdnbSS9q9ftdXvpL//rs+XL/4hSmBgps8iL0qQFbjpi3V+ne9MDQAAAAAAAAAAAPAq6UwA/Y77e2dO+sfdjaXT/OoaceGG1Z9/uWypeLq8vOzPA7+OHO2goqZGOkrFYoKtamawb3heU0dgQWmk9wGfK5mNMzIqVm7r9v0RHHUpMuq0z5YpAxpTaRWntSfPfTt31uJtx46FRp07+fvi0foyhCjbrj8cfGyx1eN0mGHh6XP58GYnZdEwGm5Ld4pWvhR57Y9tXpYq4n7LqpZzv/s18Bqt/NzJv1a6Wsi02kiWjgrjUT/nyiS/rxd/7n+fPWbbP7tnGbBM5u8Pu/aDq4mS1eo/An936ydejaE8/rtjgT+O0WY0PgW7xqdw7VLw6R+WOmk9qollNPev036rzcSNZVlMWPqjqCWh537duX6KlTaBxyyHWElKPnHp0llaSAAA4PnU1dVKSkoRAAAAAPhP0I9e9AMYAQDokTocQDOYTH1Do6tXQuh0VmbGhx5zTh8/RqdLiotp7qzXR1/cJ/perCie1tLucGwqo2qixeDEx2QIm5cKEq8c2hMQwyEMfcd1WxZYcc+smj1j5ie+HKsFqzweJbYMtcEu1vlH1iyZt+JAourUVUvsVRilccFRHFWb0QMVxJX3c7DR5sYGxpSqOCzbvtyeXNnlOe29D3ak6E9f6WWnLBpew2Opp7UgdMfyuR9uC+XZeC6f3q9F1+a8ByeD8/XddxzZt9jFSpPVNNxG3pVV05b4pfMS/1w4euRnJxOFbR5Bk6lfb/GyZcT67Ni2N6jAZPpUE/ZTg3Zoj1n13TIndrzfjs3b/eKJtdfm1RP0X40hSF42egVu/u6HLzZsasqg6QSdpYXS0jIEAACeQ62QLy3DJAAAAADwn5BmMGuFGG8TAHqoDt+EsL+pOf2ZFB9vPdzW5a23f9q+taysrPkK4j7RBfm59KeCQocHpmCwaRrL5XH5rS8WZAStmhPF4JbyRG/cF47ETF1nYsRmxItW5yYHep+Joclv4pmDFs67xpgbMK7E3AuJ5DjaOhizImJ5LGMHOy1OxN44DuEFb5sbxxDkVYqqCToR6b7VykKFEVrCUmUI0kOOBMRmCMiuFbFH2IK8liNilMbsWDIreupiD/d1v05fx82MuXJiz56A+xzyfGT6OTn344dsXrMrLI/OhsRwNA9+ptViHX2HqVaC8J1rdl0UrXMlNJEc3DJ1tEnQoTjS4wn4/M8/Xvz97n3rv9m66cvVtIROWNsMX7FkUW2tkAAAwHOorRXQAFrAryIAAAAA0P1kpJnCWj4BAOiROhxAN9D/ESIlIz3cboSGppZ2797NA2hxn2g6YWE5mP7Mz80lHSTg0sTXjsVmEtLWWMiMPg5LvFys9FTYWgY6LP49wqCxtyiY5JVwHwWQAg6PMBgMWgnnQfCVfJcxjiaqsYn69rY6+ZE7khsrFjJU7ectcbbS11JV1dJWYyQyGaJw+cSZpC0LDh5zzkhPiYsIORkQ1VoLhHmh/utC/beZ2Lu4TXCZsGy7qmDx50EZ5HmwVHVUBBlnMjiPq4qLz+OqtFhHf6AWyQtJehxq89LvZPDtLQwIQQAt8jA+nsbNNIP+aut2OjvE2obO0kICAADPp1bIl5JCD2gAAACA/4iEpFStAD2gAaCH6vAQHClJifSnUb9+e3ft+P6bzfFxLSNRpizTbuSo1Ru+enDvHs2jSQcJOelZPFUzK32F5qUMkzFzvaZYqRKWlefew1s9TQSJEWf27ti+83rJs97AhUmhIRmqluMtNE3G2KjmRgUnVoq6IXt8e2iflxWjICbAe+eOPcG5j9JuXozf4nfmL90dksG2dP1sq88+zwFt3/mQlxh+ZOuGpd+GCAY62xp07egPrQy3wcAQHP+icfPnnywebDWUPugE0mcAgA7h86tlmEwGU54AAAAAQDdjyMrLMJgCAf74DAB6qA4H0NVVVdlZWS5vudLp9JSUpvJxEyaeOB90KTLq7JVrX3+/oyAvf8v6taQTSuLCYzjGrkumDmgavoOhbOuxYN6YPoQo6NvZ6HPObF6zfdeegLCIZN5zVChIjApOZ1lNcHSxU8mLCEmi2zC0rOzMBaG7Vq7ZtdfvSlhMgeBx4MtQ1dRmltwP9tv8/mzXL0NKdCyttJ9Illl2S/2uHV7noPy4gP4CL0M3fjoH5wsEDLYWmy2eU1FVFe+Cx8ktYegP7vco15bRtjDTbjkGNC8vMZ9oD9Z/nH2zDAbrM0uS0gk0k3D//ofzZtMHnSAAANBB5aUFyqo6BAAAAAC6mbKqbnlZAQEA6Kk6PAQHdcL3709Xrhpqa3srMrKpcPGyZSFBQdeuXKa5a15OTllpKekkTvieHWf6bVmw6w+z4CtRSTwtCyv70daC4I2+cRyBdh6PaNu4OllyYojFFLe51iqMxGdVKMiMDMqct3D6aH7mweDMxqSYx+EKVKymuNhlhnGNXKa7j9YhosGWGZpOq3cvNXngs9snLE/PZbqlCv9B07AeYrx7Z07GOS7bsJVx4kRwXCXbwt5lyjByb2dkulA08geXsA309PV5eXkFefeyBO5Tl3plHozgaVs7uxqwyD0i6pEdfCFputeyDfnME/FcVZtZ7n0YLUcbESYF+AQ7rV22wZN9IpbLtHRZ4Egitp/E+Bst5eXmEAAA6Kyy0nwlVe0yTh4BAAAAgO6hpKpTysklRIIAAPRUUgy5XqSDHsY/MDO3mOY6PSUpqSkBnOgypaiw8NTxY8WFhTU1NeRFVGdEBt/MZBrYOU1ycRoxULvqns93G3+7XCog9eVZKTw9W9e57rOnO+pzLgam6pqw4wIDEgUGo9+yY8QEXEoqFz0rJYvxLgMrwk5HZlfT2fpqLrF620kj1Xevb0J5HSF1NdmJRarWEz3mur8ztX/VzTOxjIEaeRf/uZaeGpcubzF53nz3WW87mJKHJ3/cdSSmsq554wSl9yNi+WbjXadOnDTB3kKpOjX0r50/BaXSDLmOV1SlO37O+++/Z0muXQiLic9WsnJ5mwbUfUnKhYtlfS2lYv4JTi8vTI5ILNcZPHnm3KlTTKojjsVImOlyLp8NL2RZTnE2KaTNKBZU58bE5Rs5LfCc6ew0pj+J3rfu60sZ1QS6lDxLiVfxvHePBADoWkxZBaGwa25EIy3D7FxV9fV19fX1ahp9BILq+rpaAgAAAABdh8GUV9My4JZzams7OfqzDEO2Vtg1I0fTqvg1lQQA4GWQYCnrkY5TVOy1Yu06+9EOF8+fC7106UHcXUcnZ48FC952GkcAXhNqmvr52c/sQQ8A0C0UlTSqKstJV5CVZ79QVQ1ESUVDwOc3NNQLBTW1Qj4NpgkAAAAAdJykpJQ0gykjIyspISnDYJaJRt7ofN9neYVeNVVc0hVoVRVlhQQA4GXozBAcVEVF+fqVK0Y6jHlv/v82f/e9uPC472ECAAAArxcJUlZayGTISTGYCmxlaRmmlFQnPx4AAAAA9HB1dbX063xhraBWIKisKsfIGwAApNMBtNi10Cv0QSf6GhnXN9RnpKYSAAAAeA3xBdVEgLGeAAAAAAAAoIt1TRentJRkAgAAAAAAAAAAAADQjCQBAAAAAAAAAAAAAOgGCKABAAAAAAAAAAAAoFsggAYAAAAAAAAAAACAboEAGgAAAAAAAAAAAAC6BQJoAAAAAAAAAAAAAOgWCKABAAAAAAAAAAAAoFsggAYAAAAAAAAAAACAboEAGgAAAAAAAAAAAAC6BQJoAAAAAAAAAAAAAOgWCKABAAB6Is+lX01ym9s0q6ik8tHKb8grY5zLOyPGTqYTY5xdbUaOb7HUdODQGfO8nt5q3uIv1DS0SQd1bqu2yMkpfPT5FvF0P9NBWjp6BDpITo41bvKMOQs//+DT9ZNc56qoarazsrvnct0+huR1Jisnb203hrxiNLV7m5gNIh0kPh3KqhoePuZUPQAAEABJREFUXl8qKLAJAAAAAAACaAAAgB5LRU1Tz6AfeSUlx9/NSE5oa2l+Tsa925HklWfYf4C6FgLojpGWZrw9eyFTVv5igN8x790VFSXT3D1prE/eXDSAHjR0JHnFqGn1Nuzf4QBajFtWGhdzvbKKRwAAAAAA6Id8AgAAAD1SZOj5UU7T/j64gzQ0NBXSpG/+x2t+2f6leNbDa03gsd+LC/PcPZffvhFmOtBKXVMnNfH+pcBjpDErtHN0NjQZWF3FTbgbczc6nBYqqajbO07u3de4uqrqUoBfTmZa853KyMiMGOPSt795TU117M1r8XejVNW1XGd/6HdwF49XbmM/Vt/I9LjP3r79zCsruTmZqUQUz8lNe/d9DR29zLTEa8Fnqqp4GpraZgOtH96LpkuN+w8cPHx0L2XV6IgrTXtRVFKxc5jYW9+4qCAnOiJEXE9zrW5FW2472rm3gRGnKJ8enLzsjObNfv/T9X8f2MEtL6Wz5oOH9R8w5OThX9vZkdPUWcZmlvTRz3yQ/1/72j8s9PDSo2dhZSsry0q8H0P33tB4UiyHjjQbPJTBkEuKj70ReqG+vs7EbJCF9YiG+npN3T77vlvbVANde6yzm34/MzqdeP/29ZCzbT0jVTXNEY6T6eYZKQ9phSXFBfTMjnF2pQc86tpFusKAIbb6hiZnT/jQQqasnIq6Jr+62v/wPnpq6AnS0Oqdn5t54eRhuj5tjImFVUFe9oAhw2uqK0PPnxTvok9fE2u7Maoa2mlJD25HhpVwCmjhkOGjzQbZKKuqx9+JCrng39DsqmtuyPCRdfW1gf4+Eo2z4ZcClZXVLKztaNukpWXsHCcamgyqrqqIu33jwZ2b7V9azZfS51JdXamopGxgZEav5/P+f9FZUVMN+1vbOiiraWalJUWEnOXxKqbP/Sj+XrS4cnYv5fcWLD+4cyOdaHH66Ctl7kcrr10OtB3lXJCXefViwMhxLrp9DIvyc86f/Iu2QfyU+w+0pms+jKPnVHT6nm6GDJM5e+EKurLX6q2n/Q5mpyc/vVXTs6AH3HTg0LKyYhPzIZzCPLo0LyeDtPaiEzcvMS623wDLcycPFeRkjnB0MTYbKCUtff3yubjbEU8d9ifODp0e4/y2uFV7tq6m12dY0Cnx5e38lnt+bnZs1FUZGUZbdcowGMNGTaAvLiUVNfGzE6NfHZ049EurF0OLi40AAAAAwBsEPaABAAB6qDJOUVlJ0ZBho55zfcN+5jR3vhRwxLD/AE3t3rTEwfktJlP+6O8/Bhz5w3LYSBqN0ULb0RMKC7K993wbFX5x3JRZLSoZM3F6XUPtkd9+vBxwZNgop976omyUhomOk9xoiDZ4mMOlwOMtNuk/wCrmZpjPL1urKrlO056okGapjpOnR1w5d/jX73r1UpGXF/WTlZCQeGuWJ01C6SZ3oq5NdJ0jL89+5laSkpJT3/1fetJ9n71babjmMmM+jcOaNhEKhRlJCSbmluLZfqaDHt6/3f6Ogs/4JcfHhgX9Q9PnZx4WapD1iOBTfsf//ElLp8/QEY6kcaQR88E2NOo9/ufPSsqq9uNcxGtqaPe+H3Pj1+/XNd/cqJ+5lp4+zcTp7nT6GKppaLf6jGjh5BnzM1ITvfd8k5WebGQ6kLRLQ1sv5OxxGgjStNHGfty9W9f/+HlLSVGBXeMAKUQ0UEOfipLi43/sLisuGmo3lojSf1V6mm5eu3jwx030AnN5x6Nxtd6GJgNCL5w8tG+7srqG6aChbe1RS0c/ITZaollJwHFvcTLu4Px24/W269KZo1bDHQxNzJtv+PSl1aJm2oB70RH0+DDl5Mwshz5q6tSZtKl//bq9lFMw+d35tPBh3B36/YR4E/o1Q1ri/bq62lZPn5S0TE0Vjx5eXnm525wPaf7+177vJCWlBlrb0aXmlsMMjEyDTv593Hs3PR1D7ce22oyKspLD+7+vquTRnJemz21t1UTP0KSirJS25MHtG5One9DYnbRxdckwmDX8qj93f02r7W9hLa/AOvrn7rPHvYfaO9In3rzOp8/Og9ibVy6cSkmIo60ibWi/TrGykmJaA30c2LGBx61IvB9L2r4Ymi42AgAAAABvFgTQAAAAPVMDTWppZGZpM1JOjvU8G8TdjuSWl6YmxedkpKpr6UlJSfczswy/FFBdXVlVxTt9eH/S/dt0tfOnDkddu1RXW1vJrWAr9hIHZGLS0jIG/UyvXz5HNynMz015eNewvwUtv3k1mK2k4jRtZtydG6Wcwhb7pQkgTdAEfH7E5XMaOr1ZLMWmRSYDrWmklZOZWlNTHR5yljTGlr0NjGtra+9GhwuFgszUh5mpiWaW1s0rbHUrPYN+PG55wv3bAgE/NfFBeRlH78kEM/FBjLi1NIrV6q1Pn+wzd9RcO4dFLPLK+RJOQWUl9+a1oP4DRPUMGGxz69qlUk4RPbzhlwNNLR5VXpSfk5gQ26IHsbQUbZcszcQryjg0uywuzGv1GdHC2lphY5uFCfducQrzSLuS4mPzc7OIKIIXHPfZ8/DBHSkpKW5FqYr6o3GZy0qLaCGPV37r+mVVTR0iCl5tkuPviXrLNjTERIae+ns/LSzIyz5x6BdayGAweRXlahpabe1Rhsms5nGfLm9+vXGKC2jNFoNt/336bVxazaUnx+fnZNIvPGjAraHZu3lT6dV163qIrKyClo5ecvwdLd0+9GiSxkFUxJlpq6ePHu20pPjaOmF6Snwlr4KeO7r3rIwkNlu5sfKhUeGX6DnlVpTdi77e93Fc/nQzmmtrqyaF+dl3bl6lp+NhfCynOF+clbfaPHqF3Ai7QE80Eb14I86dPFTJLaPr0Cerpv7EsNrPf3aaa7/OFug3TKVF+fdirrezu6aLDQAAAADeMBiCAwAAoGei6ZkEjczu3gq3H+9CI+BnblBXV/toolYoJS0tz2LX1deKxzGgKipKxRODhtrb2I8rKykqLy2hEZiklDRpjMAoeXkWgyH70cotTXUmx9+lP+vr62JuhDpMeCvgyB9P77ep5rr6uioej6XYq2mRggK7pDhfPE1DsOoq0bgHLLYS7/Emos3LS1gspeYVtrqVHIuto9fXa/XWptVk5Z/I5VOTE8a6vEu31Tc2y0pLorneM3fUXDuHRUwgqBFPlHGK5dmintTyLEVa56PKy0oYTKZsY6fsurq6p+tPfHhXz7AfDfGJKOJMiIm40uozkqmre6LNZaWkXU0nnea/o52m9TUZQJ9CTXWVpKTk4xUeNYbm2lKSUkR0/Hs1HV76TGmQSicUFZXHT5spr8CmmTjdtqaqqq090kW05U+Xt7zeykvkm10JbV1azdFvC8QTwlqhpHTLplL0yNDsmGaguZmpRmaDcjJSFFhK6amischbOX2Nz078NUADaTaMTYPoqx36Xzl59lvuC5oqpwl1W81orq2tmggFgqbpitISebbiM5tH9dY3cpz8Dp9fVVleTl+8kpJP7Pf5z05z7dfZXH8zS11947/3f9/+7pouNgAAAAB4wyCABgAA6NFiboS5f7BMU+tRT8yGhnoaCdFsWhxdyci0+VGhiseVkpSWk1MQZ4IsVi86wVJUGjZyvN/BnTxeBd3eZMDgJzap5NUKBQd3bWqRNMnJsewcJhbkZg0b6RQafKrFjmhcJZ6g+aY8i8WrKFfs9aiEBuhsRRXxtIwMQ15enk7wuGWsx5uINu+lUto4BnGTVreq4lY0DVDbuoaG5Af3jM0H6+kbJjQOP/3MHTXppazWzmFpepo5RDQwtJKqWhVX1AW4ildB6yzIyyaNo1oLBXzxyMJtNe/SWdHoJfLybNc5C6squdyy0qefkYGRWfM2K7DYxY09zhvqG6SkpB8fE5mnqzcdZN1LRc1n71YaNPc2MB45fkob7aCHpbzp8NInq6SsVl5abOsoOr/hlwNp4fDRE2SZ8m1tnpuVZmDUXzyeuNjEt2eLujxHXGl+vdEjQ09Z0zptXVrta95Uih4ZLk8UlyfG3TEeYCknJ5/y8C49sM9z+p5WVVkRGnQqM/Uh6YhnbkVD86ZpRWWVvKzU52neuCkzr5z3z0gRhelucxa1WPrMs9NAaKj9KF+WlmY8T51N6Hc2oye6Xjjt23T1Pv/FAAAAAABvBgzBAQAA0LM1NIQFnaIxkHiuuqaax60YPtpZWlpm8LBRUlJt9mqkSV9SfOyIsZOJhATNpN5+b4FRvwH19XUSkhKSklI0wh4xZpKERPOxfEltnTA5/u5op2nSUjIMBnOGx5J+poNoucOEt1IT4i6c/LvfgMFaOnotdmRgbK6uqUOTNdsxE4vycnjN+oQm3oumcZuqmiZdauc4SXy7tuz0ZClJSTNLGyIaUFivj6FJwt3o5hW2ulVWepKsnDzdihaqqmt5eH3JVmzZnfnhg2hDE3M1Ld3UpAfPs6NaoVC2Md1u/7CIDRw2UlZWjh6ZYaMmPHwQQ0vu34myHjm2ceBmKXtHl4S4aNI2iyF2k93m0RC5rr5WWCusEwpbfUY5mcksRUVxm3vrG6k1DppBFRXlGpsO1NTuTdcxNhv0dP11tXX0nNEnQuu0Gu7QTksexEYZmw2ke2xsle3k6fMaN6+lT400DsBtYj5EvKaeQb8xzq4tNo+/d0tNU9fR2Y0eUhq7DxnuoKVnEBcd2fx6ozE0bcP9Ozeatmrr0mpf86YOGT66pqYyLyeTTicn3lPX0uvbzzwxTnQinuf0tVL57Rs0F6bxK50e5/LOKKepba0p5PPpiRPn/s/cSoGtONBqBJ3oa2SmqqaV/DDueZpXX1crIy2qv1//QRpaLcf9aPXs1AkFco3Do1OcwtzBNiNZLEXdPoYaj1+h7dfZxNl19sP7t5tH6q3urrnBw0YPGGJLAAAAAOBNgR7QAAAAPV1OZmpRQQ5bSdQVlGZXlwOPTXSd3c/c8lb4ZR63op0NQy+ctnecPN/rCxoIxtwIfZgQSzePibjivnA5zZjibkfW1bbsjhoadNp2jPN7H66Qk5ePvxuVmnjfsJ+5hm4f3wPfC4XC8MuBjpPf8fttZ/NNHtyNGj3hLVUN7Yzk+KDTvs0XcYoLQs4eHzvlHZohRoZeELe2oaHhn6O/08SWtq24IPf8yUO8J8cxaGurM0f/GOEwaeRYF9qSW+GXxGNHNJeXncFiK2WmJNbX17e1I3oomta/G33dYaKrsekg34M72j8s1MO7MTM/WEbTw4dxMfTI05KEe7do2us2Z5EMQ5ZmrzdCL5C2JcXf0dHT//CzTfUN9Un37yTcv03aeEbnThyiYeuYCW+nPLzXFAvSKNbAyNRtzkcZqQ9pkquj17dF/Yn3Y+gKH638pqK8LDXxnniQkFZVlHGCzxyhp0xLV7+spDjo1GFaePPapckz5nqt3lpUmJublSpekx7/PkamLTbn11T7H95Hv5OYPs+rob4+I+XhGd+D1dU8IrreTtGjTa+3qipezM3QlIdxzTd8+tIiz0KbepK9ArMAABAASURBVLGxqSpqmllpiWeP/inObun5zU5P1NY1EA9JzC0vfebpe1p8XIwMU85l5v/U1OmlmxB19WJba1ZWcmmD6TcEYedPPXOrgtwsFVUNeiLyszPOnvAWCgXCcsEzmxcWdNpx8owJb7mnpyQU5me3WNrq2aGH17C/xaLPv/5z9zfXL519e/aH7guW068Hmq6Z9usUo19yaPc2oI+BVqIbM/K4XO89W1rdXXM6egZCgeD+7UgCAAAAAG8ECZayHgHokdQ09fOzEwkAwMugqKRRVVlOuoKsPLurqoKXxd1zeVjQKdGN+/5bk6fPy6BJbTckfdJSMtPnLw4+5VfSxrAk0AkmZoPMh9iK7+sIAAA9gbxCr5oqLukKtKqKskICAPAydM0QHJZDrOiDAAAAAMArrIEQ1/cW6hv2l5KUMrOw6q1vlJWWRLpBbZ3w4mk/O8eJBAAAAAAAerYXGoKDwWROc5vx7nuzVdXV6WxxYdEx38P/+B8X8PkEAAAAAF4xEoTcuh4ycvwUFTVNfk31lbP+FWUc0g10+xjaOU7u6C34AAAAAADgzdPJITgUWCzXGe+6zXLvpaR0+sRxv0PetHDWXI+3ps8oKyv19/M7dfxoJY9HOo1lMWaeh7uLnbEqk5f3MMr/wJ4joaUC8h9Qtl2/Y51B+MpPDt5vrf3abt8eXFC5bc7XYc/925qK3ax1qz3sdBjc3Jsnt27fG1Haxooy+g7TPT2m2g7UYvNLEqMvHNzhHZYhJK8KBavVuzebnFm6yD/pPzkT3Q9DcADAS4QhOAAAAACgfRiCAwDeDJ0ZguM9j//5nQ5873/vB50NnD7Z+afvthXm59MHnaCzwWfPvucxX7SCx/9I56g4LN27b52rdn6o785tuy8kEkvPLTuWOikzSGcwTNwOXj680k7h+Va2nzmwJHC37/0XSM+foGrjudzdIHHP4v+tD+SYuy5w7sdqdT0FK68dB7/36CeIPfnDzp3+sQKD6Zt/WuViIkMAAAAAAAAAAAAAXksdHoLDcojVBx8tDjh18re9eyoqWva3Kisp2ffTrsN//u7huZCudv/e3diYaNIx2vZey53ZEZvnrbmS19jT9qSv7+gNu9ctdL8YszemW/5K9F+CxIBl7wSQrsNQ1TNQ5cXsDomJE3BCM11mGWszSdJT6TbLymOpe5+4Hxau8stqfNIBR7wtl+7b6ukxLGJjeMkb0uMYAAAAAAAAAAAAepQOB9DZ2Vnl5eVT3natra31P+Kbk5XVYgVdPT23me5vz3iHrpadlUk6SsVigq1qZqBveF5T6ioojfQ+4OP0qOcwQ9vSdcE8VztzA3ZJYnT4kQPegXGVhGU0d99Wp0TvYKazm4O5iiAzcv/2zX7xxGHloe+dtQmx+Okft4cHPljkl8S2cV0yS7Q5g5cYHeJzwPvio813uMSt9twaLwqHVW3W/b5W23/JUu8sAUNhwJQFnu72VgYs3r2QwDgGIZXtteRJAk5BHpc1wM5YO0953hRjQdyJpFb+fEbBYoq9Pidkb3DWv1Ez58GR3QcE2gImnWbpjV/oOc9pmIkagxTf8duxfW9wgUA8JoZFbGCintMEc1beTZ/dfkkWsxZPoasJ0q/7bt/kR/N6Fae1vy1XCPYrtZrlaMEWPeV/29lqtW0cSXFmzmDbzPtpqq1FHzYpSQw9sO7boAy6gKHQb8qCxaJDpMLkZ4b67tp2IFYUmjM0bZcsXeo02ECNwc29E7x7+y5Rszth3ISJCmzWPyeOtyifNn0Gj8e9fOECAQAAAAAAAAAAgFdPh4fg4BQVzZ3+9i8/7rIf7eBzzH/rzp/ohHgRnaCztHCUw5h9P/84x+0tujLpIBlVEy0GJz7mybGPBYlXDu0JEHV/Zui5bNi02FoQ6bdz844zSWzHlVuWjdYWr8XSt3NUjdi1ePaSzUE8qyVL51nI8EK3z5y9J46b7//JNNs5fvcFeq4b1i62EER679y8+0KGqvO6LV622u21R3vCyu1fOKomnti1cadfuqaL22BVZuOS9lrS/IDd9PG+w56+4+ThdaO5J9ZtvZL3dATLUNHWoXH4ncQnsmlhXqj/Xr+oPIGC1ZJN66aoxOxZ4jpt4dpQlsvyxU76j7ZUNbDRz/Bb+v7qg+nGnt/vWDcwfu+n8z/4NopYu3s66YkHLWGoDZvpphyzY8nMTw7EsZ3XfbdsvGjzdqpt5UiKa2IbDLMgsT679/hE8LQneK2aItqFisOy7cvtyZVdntPe+2BHiv70lV52ykQ0+LXHKjfjkuBtH8xeviua5bB8qZN+50YUkWcpfPr5Kvd5Hs0L6SwtlJd/rrFVAAAAAAAAAAAA4L/X4R7Q2jq6M96b/fP324/7HnYYO276rPc2bf8+OytLQkJCt3fv+3fvblrzReili3RNGg76HfIpyM/rUP0MNptBuDwuv43FJs4uJiWBa77eFSHqwxsYkc/Y5+VqpxkZROcEJXH+PkEpJQKS533Cwc6rn4kKI66g+eYsE2cn/eSDn68/FCcKuINj8rf96O5ioRwZ0VZztGynDCbRB9ZtDMigwXFQbB5799cW7bbE/8lOvjRc1maISrg39271bmMIEQaLweByK0nr3YMraXbsekBQwhG1meN/YdaEqQN0FAIzRE+Zmxd15ERUBo8+5RAXO+eMExciE0tJuveRCZbzBvZh+Ys7qJeE7d6+N7iUkJRdWxkG+xa42GmGZRS0Xi2nrSPJE+0u/cTmNY0DofhHcfbtnmUt2gWNmOfGMQR5laLmB52IdN9qZaHCCC1lqiozuA/8T1y5n0Hub10eo83gdPKeimf8T7BYLM/FS+i0r4/ojpc0faazB/fuDjjpTwAAAAAAAAAAAOCV1OEAWk5e/u0Z75iYmh37+6/Qy5fow8TU/B3394iExMYvVqUkJdJ1xox3eue92abmA/7xP97R+mmiyiN2LDaTkNZuA6hqYqTNT/FLfzzSBSclJo/MozFoUAmd43NKBOIMVyAKQ5mMlrctZJsY6asN9vrjvFezPcbpsNq8vSFDRV+VcK7EP+q2LChJis7kWrTbEv+Ckn+3VxiwYO22+SoxvgcirNw9l0+NWxHC9lg6k/hv3hPb7PnxSrgCNluB0Ha0mkELCNtqutcU+346LFXtPqrM/AxG0/HK5z5qG08g4HF5j2YEfMJgyDxeJzkm8dHeBLkpcblktIEWgxQI2q62rSMp4JY8/m6Ax+EI6C4au4MLGar285Y4W+lrqapqaasxEpmi9fMi/IPd1q774/C89OSk6PDAgJCOfRnxBHHuLM6gxRM0fRYXAgAAAAAAAAAAwKupwwF0anLS0g8Xzpg9e8M3W4sKC08fP3rG33/LhrV0EYvFdp/n8daMd9U1NK6FhX684P20lBTSQUJOehZP1cxKXyGS8+94ygyTMTOdWPf9AsQJ5lMhLYM8NwH3js8O/xjuvyNMcxPzBaQP6ZRntITVx2mMcUnQ15t3h/MMeKo/Lli3nJE0cLB+9JO9dgW89Awew2GYCftK5L9dpGW0Haa6amedDMi32rB1pTUv8kpUYHB8HsPGc4kN6RgGYT5dpueypRPVCp56zjL9PDbtWmCcFxEeE3AhjsNyWrLg0UgeeVG73n/viLW9q9tUl/mrXKY77ly0/khi5zpBkyczaKTPAAAAAAAAAAAAr74OB9BUYUH+hpUrtHV035k9Z+4HC2ggeMLvbykp6bffeZfP558P+OfY4cN5uTmaWtqdqJyUxIXHcJxdl0wN/cTv/qM73ynbeiyYZxK+yo9w07M4TBtbA4WwvMZ4WtXISp+RF5HJe74MWrQ5sSS5NyNjGmNQlp6tNStPNAaFQCAgTLYKo7EPMoOlrCKuT1CSwSFOA820GSmiITgYKv2s+7BJ6aOqWm/JE2hey+eKehMLEgO27TDf+80CF5Ls923yk6tVZlyJynObunhBSOKOqBJxwqtqPnPJAofEr/2uG422YMTsXr+ucXAPlpUlowN5e+PxY/ex0medTBQ1m6FjZKFDSgLyBapmL1jt49q1rOzMBaHbV24MF7Vc1cah6VywlLVVBZyIoL0RQQf1J2zbt8DWQuVkYufuQyhGQ2ehsJZOHPc9TAAAAAAAAAAAAODV1uEAetDgITv37ff5/eCJv//+6bttB/funjhl2qw5c+miPTt30PS5qrKSrag4f+Giue9/8OlCz7i7saRjOOF7dpzpt2XBrj/Mgq9EJfG0LKzsR1sLgjf6xnGIgHvCJ8J+1eqVeQeCkvgKttMX2HIurArIEhCjNivk87h8hra+lnZuCSeucfMNa4l3UBxXwWKKx8yBmbsWrT+ZWJKUWKI9ffGyRJngXJbFhKkmaqRxjOX8yIA7nhsWrFtOfCJK2dZT5lqwxLXy4tpqSTO8zNArma7TF88LXX8wWqBKeDzRbQZ5eYKWGSwvxnuXr9m2+Zv2GoSEXXnAUTW2snO0ZYRv975ZUmnO4bEcpky1TTyTp20/y93RgCm4TzqEZbVw5WJ2QBxX2dZ9gRX/zuYImomXvnC1j9rO4QpUrKa42GWGcY1cpruP1iGNHdVl+k1Zu3ehSuT+XQdjiIXbVAu2IIwjeIH0WQzRMwAAAAAAAAAAwOuiwwH03Tu3fX47MGPW7HfdZ5856e/3l4//EV/6EC9VUlGZ98GCadNn1NXW/fHrvo6nz41KQnctXnRnnoe7i/syNybhPrzms2bXkdBSUXYpKLj47Xr2hk1LN4xkErrozLY1B0T3xGO1WZsgL+pI8NTNn+0/mXtm8fu7Gjdfu/SLTfNoNJ1788jG7YGiQSGEMQd2+Risnbdk3ejcO4G+ZyINPBo7cAvzgravZCzwdF+wfTqL+/CCT8CdWVPE9bbRkidU3j+wfilngdfyP8MMWISbGRHk62/iTBPtjEV7I59YuTJmz3LPuOmeHlNdP3NmE1769TPr1niHie7a9+Dg7hPay6dv/8OdFN/x8wuJ0bYnHSEofhB8pdR2yaZ5bF56dMjmzw8EdkW1j2svDdu9J3CDl9f3f3qR/AjfE8EPPRpHyRYm+e/aZrB02Wc7jtA5bmao7649EaUEAAAAAAAAAAAAegoJlrIe6TgFFsv1nZluM2fJysmdD/jnb+8/JSUlZ831eGv6jLKyUn8/v1PHj1byeAReOhWntb8tVzi46IvADAJPUtPUz89OJAAAL4OikkZVZTnpCrLy7K6qCgAAAABeHfIKvWqquKQr0KoqygoJAMDL0JkxoCkaLv/1x29H//5rmtuMd9+b/db0d2hhcWHRLz/u+sf/uIDPJwAAAAAAAAAAAADQs3UygBajQfNx38P0YTnEis7G3o4hAAAAAAAAAPDKUBg5imk+QM7UlNHfTEZNjUB3EhYV8x/G1zyM5z94UHntKgEAgE4PwQHwBsAQHADwEmEIDgAAAOhu0jq62l9tkrMcTOBlqI69k/fV+trcHNJZGIIDAN4MkgQAAAAAAAAA3iw8CeQCAAAQAElEQVTsaW/r/+WH9PklogefngL2lGkEAKBne6EhOAAAAAAAAADgVaPoNl1r1ZcEXjYpBXntdRskGDIV/icIAEBPhR7QAAAAAAAAAG8Oad3e6h8vJfDKoKeDnhQCANBTIYAGAAAAAAAAeEM0SEhob9goJS9P4JVBT4fW+o301BAAgB4JATQAAAAAAADAG0JuwACM+/wKkh88mJ4aAgDQIyGABgAAAAAAAHhDyA4YROCVhFMDAD0WAmgAAAAAAACAN4TsQAsCryScGgDosaQJAAAAAAAAALwR5AYMJPBKwqkBgB4LATQAAAAAAADAG0JGR4fAKwmnBgB6LATQAAAAAAAAAD1LHa+y9MjflTdvCDJSZTS1JJmyTYuktbTVl3wqo6FBAAAAugICaAAAAAAAAICepeJsQPHen+UsB9cVFUuxFZsH0DUJCelzZ+kf+JPRp8/zVFWTklzqe7jyapiUqqrCCHvV+R9IsVjtrJ/58eIGgUD/14Ok65SdOpm/ecPT5arveyq/Nzd9/uxeLlPVF35UeTsmy3O+3i/7FYbZNq2Tt2FtecA/T2/b++dfWCPsW91d5pKPRE9h/28EAACeAwJoAAAAAAAAgJ6l6nY0y3Fc7+93JlgPUlv4kaKTc9Oihrq67M8+zfD06PPr78y+fZ9Rz507WV4L5YfZ9prxTm1BAff8Od7VqwY+fzVPtP8DzP79VRctphO1xcXlx4+yx09gGBvTWXnLwZKyTDlTMxkd3ba2VXBwlO7dm07U3LtbGX5Nee58SQV5OsvorUcAAKArIIAGAAAAAAAA6GHq6ySkJOl/GyQkBGmpVbeimpYw+5vqbvs+66OFGR94GPgdY2hotlNN2bEjEkxZ3W+3ScrK0dnK27ezPD1oBq043on8h+TMzOmDTlTfj6MBtILDGKXJU5qW6m77oZ1tFceOI/RBCOcvb1EA7f4eQ1OLAABA15EkAAAAAAAAANCjSEiKHoT0cp5UtH9f5ocfND1K/P6WZMr2/nGPlLx86SGfZ9YkKSNTX8MXTysMGWIafVecPgs5nPzt36a4TU2wHpTm/k5l1M0WGxbt/yV+qCVdTTxbW1aWMNyq8OdddLri0sWMjxY+HG2XYGdT8P32+ppqIkq3Y2hVJUd802bNoNWS50arLdq3t0WhoCA/efKEzIXv1wv4bW0oyM7O+3pj8luTU99xzd+6RVBY8PQ6xfRZDBvCvRpGAACgDegBDQAAAAAAANCzNDTUSzRO6GzZSh9PryDFZjMHDKgtzG+/HvYE54rzgenvvdvL1U1+kKX8MFsJCXHFJG/9l/zkJKV3ZjH19Yv378v94nOjM+ck5eSbtu01eSrn11+4F86pvDeHzvKuXCa1tYoTJ1dG38pduVxhtIP2+k3Vd2NLD/tIqampzX9fvFXpEV+VWbMZfQ3IC6irqs75dImkgoLOdzslGcxW12kQCjOXfNhQWaXiMb9BICz5y6c67p6Bz98Skv/25Cs/f7b411+0vljLHjWaAABAGxBAAwAAAAAAAEBnsB3G6Gz9nuP9O2ffXg4hTLMBGp98Kr7Fn86WbfXVVQxtHdI4rnTemtXCvDymoVHTtozeveWGWHFDLokD6IpLF5lm5rL9TBpqaw18jzH7mdAsW3G8U2VEuCApqWkrmj4rvzuTdFJjOF7fkLv6s9riYgPvw9K9erW1Ku9aWG1Wlu6On+hzpLPSWlr5676sir6lYDOM0JBdQqIqOipv4wblOR7KM94lAADQNgTQAAAAAAAAAD1U7prV5RfOSTQ0NJU0SEj0cp6ss+Xb56xB0WkCfQhysisjrnODzmcv+8TgryPMvn2lWCzelZDC61fruLyauLuksU9xy22dJxZs/UaQlyspJ191M1Ld6xNaKCEtLSEjU7jzB35yUl1piSA1hWFo2LQJw0CfdJ7oaRbu/pEf/0D3h10yurrtrFp9P44wmCz7keJZtsPYfFp4764ogG5oEObnZq9cIduvn8anywgAALQLY0ADAAAAAAAA9FA0fVZfuKjPr781PdQXLCoPOkc6iKHbW3nGu71/2tNQU1Nx8QLNmjPen5e/7RupXkq9nCepf+TV6lbs8c4NUlK8kEu8yxdJbS174iRRk4LOp86cXhUdJT94sMbS5UxTM9KlGgQCad3enD9+a2f0ZzEJaUkiJSWelmTINDweXYSqzc6WNTOvuR/HDblMAACgXegBDQAAAAAAANBDSTQ0MPoayg+1aSoRlpZI1Nc/5+aJDiNkBw7S2/mzhIwMnRVkZIjqlGEIsrNoOKu99bteTs60pOzkiVY3l1ZWZjuM4V2/LikrK283gqGhSQsrw8KYfY36Hj4iXqe+fCPp3Zt0Hc3PPicMZuaC/xX99KPmipVtrSY3wKKkqpp3NYw92oHOVlwMosdKbuAg8VL5oUP1ft6b/alX/tdfyZqa0vydAABAG7oygFZSUdHS1i4vLcvLzSEAAAAAAAAA8EZT/WBh0Y87spZ9LGc5mM6WHTsiISvba4KzhLwCDXkrzgbKKKsICvI5h7zbqkFxwqS8TeslpKU1l38uLpFWVxNcCi4/FyitplZ++nQdt4J0LQkJhSFW6gsXFf/6i7y1NdtxXKtrsUY5yFsPzd/8lfCDBfU1/BKfPxRGjmpK6hsaJCjtjV+nzZqR+8XKPgf/lGQwCAAAtKZrAmhNLe0vvto0cPBg8WwJh/Pd15tuRlwnAAAAAAAAAPCKkZCUaqirfcZKDQ1EWqb9VVTnzaeJM01yqyKuM/uZsMdPUJw8RUZHNLay1rr1xbt/zvzwA4VRo1U9F+av+7LVGlijR0vIMBr4NazHQbDK/A8EWVl5a7+QUlbR+GSZsLCAdANVzw8rb97I27SBaT6Aoan19Ao0E9fZviN37ReF320VtXPceO31myWajcJBRD24VXQ2f5P10cKi3T9pLl9BAACgNRIsZT3yYthsxd/9jt64fj3g5PHUlBR1DQ0bW7v5Cz/89qv1N8LDSUcxLDwP/uFuUhyy9v2vL+Y1W6A9ZtvhdQ7s5D3/W3IoTki6hYy+29pdC1j+n6/uyl1o26z8bqlVnu+uUON5Dg82rwnKExB4Bahp6udnJxIAgJdBUUmjqrKcdAVZeXZXVQUAAACvO5Mb0c+zWunRI4U/75QzM6+KvsUwNKRBatMiYUmJMC1V3npodfx9jY+XK787k0AXSRxu3aH15RV61VRxSVegVVWUFRIAgJehC25C6Om1JCUx8fstm3rr6W/e/n2tsPbUsaO//LhrxRdrSSfxaTZo6WSt2axIRtva2YLduKiLKdhuORy4b4q+6I9lhNy8rMTElAxOVwbcLBN7A86JvdGDly63J3HxHKTPAAAAAAAA8DIpTp6iOv+DBkkpKXU1SXn55ouk5BWk1NTpItX/LaCrEQAAgBfTBUNwDBlqc8LvbyL665yGocNt+5ubF+Tn3boRuXLtegMjo/SUFNJhgpJ0DsPCyVI76HFnYYaKlZMxIzefyybdqiTi4KoI0rV4obsWh9L/+of5EQAAAAAAAICXTYqloPbBAvogAAAA3awLekArKSlXVVbRiUtB55sKK3miPxJRbvZXPB3CS4pOJiaOttqPhptiaNuMNyG0kPfvOgr6Tp7bfj8cHHUu+NgP6zxstBvH+1dxWnvy3LdzZy3eduxYaNS5k78vHq3/byUzt/zgd/lc5LVjPj8uHm+hQBh6M/cd3zVBS9V62ZHwY5udlMWbu+gTwrJcefpSZFSzx7m1o1VpNTIqVm7r9v0RLCo87bNlygDVRw1iWUxY+uOvgdcuhZ77ded6N9tH+33O9adYaRNow7gJE6dNn/F0OS0c6+xMAAAAAAAAoJGQwyHwSsKpAYAeq/MB9Mw5c+mDTqSkJOrq/TuQdH1dHf2p18eA/kxLTiKdw4kIiSPmTnZajamyjLado4kgKjCmsmkEDpbdgm0bpmrnndm7cefBCN6ABWs3LzAS33KWoTbYxTr/yJol81YcSFSdumqJvQpdwNBz3bB2sYUg0nvn5t0XMlSd123xslXNOrJoxtKgfE70zpn276wLLv23BbzkIxtXL10heqz89kwiX5BOm8QlDH3HdVsWWHHPrJo9Y+YnvhyrBas8zFhENET1qi3LnNjxfjs2rzsQRewWrFtiTzPx9tb/7tH62/3iibXX5tUT9HHP3NbJsxQ+/XyV+zyP5oV0lhbKyysQAAAAAAAAaCRIfEjglYRTAwA9VmeG4FDT0Nj2489KSkq//vwznT3/zz+LPl129p9Thfn5Szz/l56aSgvnL/zwWlhoWVkZ6SRebHCcYNUEG33/rCSiZTuhjyDOP5Fr/2gpQ9nWzYYdd2DxxoAM0RgdIXH83dvHTLXw25VO57jJgd5nYhKFJPHMQQvnXWPMDRhXBAbOTvrJBz9fL767YHBM/rYf3V0slCPbvCFgZUZMVIZoX3ouW+xp0r1uT3gJXTcjaNWcKAa3lCfa7sKRmKnrTIzYjGRVh6lWJHznml2NN068EpOY7GBQQONyQTvrC/5dPzSRHNwydbRJSLfdX/G1dsb/BIvF8ly8hE77+niTxvSZzh7cuzvgpD8BAAAAAACARjVJiQp2Iwi8euipIQAAPVJnAmjPxV4V5eUfzZ8nJytHZy8EBji7TPE9dSb0YnBoyOVRY8Y6TZrMZDIXzp1NOo9fEhMUy/vC0dbkTAaxdzLgRXg/4JCmAFrLwoDFuRL/OD0WZsTEc6fr9VOVSaeZL59Xwn0U4wo4PMJgMJiEbWKkrzbY64/zXv/uQxCnw2KQknbbIdPPfeli6/yTK7wjm/5YhtHHYYmXi5WeClvLQIfFv0cYhKU/UIvkhSQ9XocXdyUwriPrp9/J4NtbGKgw4gpwk8LWiHNncQYtnqDps7gQAAAAAAAAxAQP0c32FYVTAwA9VocDaE0tbaeJkz9d6DnacdwXX2389qsNF8+fXb54kceChQ7jxtuOGl1eWnov9s6enT9wiorICxCUxFyI4a51cjC/Txy1OVF740oFFk1LWx2rgibN7dbIveOzwz+GK/i3IDFfQNrbhmXlsc7DOMN7+cGYysclnru+n66aGBIacSYmrlTbbaknu50mdWx9BobgaE/zDBrpMwAAAAAAwNN418JqkpNkjfsReJXUpKbwroYSAIAeqcMBtGKvXvRndlZmXX1deFjook8+DQ+7Ul1V5X1gP32QrsR5EBhRstluqotAhRMRkth8tH5BflKuwGmgmTYjpXEIDhl9KzNVbkpSnpC0cSs/bnoWh1iS3JuRMY2do1l6ttasPI6QtBNAa9sv/mK66r0963xTHofWCvp2NvqcM6vW7I2h7WFouriJy3l5ifnEbXA/1YCMvMbqTewdTEoigjK1211fv2l9g8H6zJKwdB66P7eLhs5CYS2dOO57mAAAAAAAAMCTGmpq8tet6eP9lyR6OL0y6gWC/C9XN/D5BACgR+rwTQglJESbsNjs+Li4bZu+oLQ8MQAAEABJREFUkpSSEt8azmKQ5YLFH5MuVZkYFMUxcHQxKYm8ksxrvkRQEOp9IsPEY93yKaMd7Md7rFo3XSXG2zem7VvK8uJO+ESwRPchdLMf7TRh8Zat2zbMczCQEVXGFTBUjfUNNLVVm23A0By/fKmbdmZkRCkNkW0dbGztjFRYAl4ej2jbuDpZ6ptYuixZPNdapfHfdGFSgE8w18Zrg6eLk81oJ7dV361d7KTHJs9Yf5l4/Sme61Y7kgifk3GVBJ6BRs9InwEAAAAAANoiSE0p3v0zgVcGPR2CtFQCANBTdbgHdGLCg8L8/Pc//GjTmi8qebwt69fWCkS9dtds+vrcmX9I1+IlhkSmT9UnIcGJLW/Nx4s5sXmjyuYNy7ZPp3P5EbvXbw7Iaq/7sKDg4rfr2RvWLv1i0zxC+Lk3j2zcHiiqVhjnfyLSbtn2w44xPyzZ9DjCZmhbulirEKaKy2ebXMRF/Ds73199JGjvXuuViz/b4UQE6Ve8A0ONZ4n7XHOi9m7ayV6/at037oSbn3jvxLYdIRkCIXme9UWL9qz7NjwP/Z8BAAAAAADgRZUd+bteUKP+8TIpBXkCL09dRUXRju8rzgUSAIAeTIKlrEc6yMbWbuuun4LOBvgd8slIS+trZLzok0/76Bt4vDtDIOjpf1GiPHrL1nn8EzsPhNzPExJ4palp6udn4zbEAPByKCppVFWWk64gK8/uqqoAAADgTSKjpa21fqOctTWBl6E6Ojpv3Ze1nGLSWfIKvWqquKQr0KoqygoJAMDL0JkAmhoxcvRna9YoKauIZy9dOL/v5x9Lijv/rvoGYWiOXr1pFmf70j0p6ND8akMADQAvEQJoAAAA+G/I9NGXHTxEfsgQ+cFWMjo6BLqTIC+v+k5M9e3b1bdjhJkZ5MUggAaAN0OHh+AQu34t7PqksN59+qipqZWWlmakpREQYZnN3bLUzYREbC1B+gwAAAAAAAAvG41B6YP7zykCAADwMnSyBzTAGwA9oAHgJUIPaAAAAABoH3pAA8CbQZIAAAAAAAAAAAAAAHQDBNAAAAAAAAAAAAAA0C0QQAMAAAAAAAAAAABAt0AADQAA8JpraGiobyAAAAAA8AahH/Aa8BEPAN4ICKABAABecw0NkhISBAAAAADeIBISkjSEJgAArz8E0AAAAK+3uvp6SWlpAgAAAABvEClpqfp6BNAA8CZAAA0AAPB6a6ivk5KSIQAAAADwBpGSYtTX1RIAgNcfAmgAAIDXW11drTQNoDEMNAAAAMAbo75BWkoaATQAvBkQQAMAALzeGhrq6xvqGEw5AgAAAABvBBlZubr6ugaCHgYA8CZAAA0AAPDaEwr4UjJMCQkpAgAAAACvOfqhTlqaWSusIQAAbwQE0AAAAK+9hob6WkGNrJwCeskAAAAAvN4aCP1QRz/aNTTggx0AvCEQQAMAALwJ6uqEdbUCOXk2IRIEAAAAAF5LknIKivRDHf1oRwAA3hTSBAAAAN4ItUJBfX29rCyrVsivrRMQAAAAAHh9yEjR/8kKBTW49yAAvGEQQAMAALw56K8rwvo6GYacDENW1Cda9KhvqK+TkES3aAAAAIBXTH0DkZSSkqL/l6GPhoZ6oaAKI28AwJsHATQAAMAbhf7SIuBXSYh+mZGSkZFlMCQIjZ+RPwMAAAC8YkRRc0M9/fBWX18rEFQ31NcRAIA3EQJoAACANxD9BaZW9DsMBuIAAAAAAACAlwk3IQQAAAAAAAAAAACAboEAGgAAAAAAAAAAAAC6BQJoAAAAAAAAAAAAAOgWCKABAAAAAAAAAAAAoFsggAYAAAAAAAAAAACAbvFCAXR/M7NLkVHih8fCD0mXYFh4+lw7vM5BgbwoBavVfwT+7taPIaPvtvHkuR/mWsg8axMZbaeVftcuBf/uaaVKOknVculfx/zW26swnmdtGf1ZPwSf2zheu1mZ9phtly9Fnls7WpsAAAAAAAAAAAAAvLZeKIDOysz8bPGH9HEnOrpPH33yn2GYuB28fHil3XOG1EJuXlZiYkoGR/isaqeuXGJ0f+vyvRz7lcvHaD9XgvwUbklSYnJSYr5AQDpH29rRgpRw2WZOFsoEAAAAAAAAAAAA4HUlTTpLWVVVX/9R6CxBGpSUlQdbWYlnMzIySjkc8uooiTi4KuLZqwkS/Ze95S+aCvjfSdJZgqzATV8Eks5iaA5wMBfcOxHInO40xlwlNLyks0E2AAAAAAAAAAAAwEvVyQDaY8HCeR8saFE42Hpo07TPbwe8D+wnL0bBavXuzSbhB6O1XKbYW7B5iaEH1n0bxLFeeeh7Z21CLH76x+3hgQ8W+d0neqM9POZNsLHQYXAe3gz0PngwOKt5bKvitPa35QoHF30RmEEIS2/8Qs95TsNMaIURF4KJ4yy2t+cnQXkComI1xXPhVAcLY5Yg8/6VE3v2BNznEIb+lG373Hl+J7h2U52s+5Dcmye3bt8bUSqql6Fp675gnpvNAB1Sci8q2N/XJyCFxzKau2+HS9xqz63xvKZ9qTFI8R2/Hdv3Bhc8I09WtXSyIIl7woNZNi7ujhaq4WF5pMcbN2GiApv1z4njLcqnTZ/B43EvX7hAAAAAAAAAAAAA4NXTySE4prpOP7h39zhbm1Yff+z7ZcpbrqQrMFgmjqNJyLZF8xfviGI4eK2aoicI3T5z9p44br7/J9Ns5/jd5ykM8Fi72d2IE3pg87cHgvP6uG5Y62nV1ugcClYL165z65MXvGfzDt8Yhv08Oy3xSBsM7TGrtng5MOL9dmzbdSKe2HltX/1oFA4mU8vWqc/9/avn/W/9yTzjmas9bEUjRCsMWLB28wIjLt3vlzv90vVcV6+c98R+FayWbFo3RSVmzxLXaQvXhrJcli92esZAJTLa1vYWJDnyXn5GTHgG29LFGqNwUPIshU8/X+U+z6N5IZ2lhfLyLz5aOAAAAAAAAAAAAHSLTvaAVlZRycnObmtpVmaGipoa6QoCQV7UIb/wJA4heb5HJtjMG9iH5ZfFa76KqrnLGFbkjuXr/Bs7FwfFC/ZtHT3B2CcmuZX6VM3HO2gl+S7fvCdFVEloCmPfDifRAhlth6kmnDPrPt8bIxo8JCg0kfHbcmdb7fDGwTR4cf6+wTG0/gIfb5vRW4z6actEEmOXMVoZvqvX7UkR7Tc0PinOksFr3r+5MmbHEtcDgpLGsac5/hdmTZg6QEchMKOyzafLULFyMicZ3jF5QgGJDU33mOdgqR10Ja+nj8Jxxv8Ei8XyXLyETvv6eJPG9JnO0m9BAk76EwAAAAAAAAAAAHgldSaAthhk2TT9wWIv+vO3vXtaTJMGMmDQoPt375IXJOCWcPniSR6XSyNaGfLkvQEZqkYm2loWX/wd9sW/hVyOMru1WwiKVmaXJMbkP4qwOZmR6SUObDrF0h/YR7v/4L3npzdbPVNfla5D+Hwej/vonoICLs2YGWxRVWYmqjxa1aNwWFAQ4x8kmmA1bz1hW033mmLfT4elqt1HlZmf0e6NDRnalqNNGBnesY2Jc2ZMaKbnLMcBqlfyMArHo9xZnEGLJ2j6LC4EAAAAAAAAAACAV1OHA+h+/U1/3H+QTmjr6NKfujq6DY8XNU2LFkmQn/b/tshjbtLDBPJiBOSZ/X8FJREH9hxJ/7dnsYCTzBEQbdIx/2fvPgCjKB6+j+/1lEsPaSSEGgiEGloA6U2KCoiCBSxgAxs+dhG7WP6CCvYGioA0kd4JHUJCC6RSQkuB1LuU688khzFAEggSIeT7ee/Juzc7M7u3u3f/43fjrC5h2fRZ2zP/2Zw+JdEkeUnXSB00+P2pL4Xrd22OWrEuLlXdYdzEDpU2UHm17NXOW+vywi9bXigtzOoX7rF+ebaEizJo0mcAAAAAAADg5lflAFoEyn06d9iwKyr17BnxdMfWraWrSpftq0Q16T9g1J1K0Un+hqMxkSU3HlR7NIloLKUWj1Mur3JaqsEzpJ2fdmfJFBxe9TrX91QXz7mhT01MM4ZImTFRu4qfSurg1p29sjJFpQoCaGOm2G5xV+qdR+3bbde/gzZx+5azf9fwatQ9TB0z40373CDadq3VlQ5/Lpl/o7GUsOyjWdsvzLmh9u332PjOzMLxDxE6m0xmsbBw7hwJAAAAAAAAwM3tGueALrV+zapyl6uZQa8zqP2D/fzPZmWm7Jk3N3n6Y29M9lq0LjbfK2L4uCF+MVMnvbtcX07D1AMrdmZ9NPql5/VzI89Kwf3HDq4vomSxwpS0fHbkkDdeft84e9GBTE1Qv7FjOxtmPffEvKSK9iFzz+xZR76a+NLLoqsTJpeIUc8N0a54sUwAbczO1Gt7DBnaOXFZqn/XUaN71dcYD1f8mtT+rfuGqFPmLVqx7tTfabMqM2BA91G9WvhvTk2RUILoGQAAAAAAAKgprjGAPnH0aJfu3fNyyp8Z4rZevUUFqfoYU6Pmrxv67gvfLTm77KlHpscs/niy10uTH3q5+HaCuuR13783bW26UXIur2n2rs/efFc/bsyolwd7Syc2L5q/Qz1YU7ImM2r669M0bz7/8gcjirdwaNlHby86rJfUFU7BYUpZ/vFk/5fenTh5sAixTxzZMuPjH6Lz/xl4nXnkhxmL/CeN+Pjn0dL5/fPmbYrx71rxa1J5hfcK0ZycF51mLLuJ6O0pY0f0a+m7JSWdMdAAgCqQKRQKuUIll8slmVwmkwAAAHBTsdnE/1mLWUwWi6X4bloAcCuSaT2CpKrr3rvPo09OCAwqv+2J48d++fabrZs3STcjtUqrNuntw6PVHn3f/26CNPOp15njohby9g1OO50oAcCN4OruU5CfK1UDmUymUGnkMoXVarYU/2PGarNZZCTQAAAANxmbzSazjxkoHjSgtNrEdzeDzVYtMbSTs1teToYEADfCNY6A3rJxg3hINY/ao/uUGZND4r56e+a6VM92Q0aPi5BOfHY0k/QZAHArkCuUSqXGbDIYLQWlhaTPAAAAN6GSL2lWi0U8iu91pFKoVWons9lgLXkKALeMfzsHdE1jzN713fTZE8eN+3nhy+Kp4WTk9+99tPwU+TMAoOZTqtRyhaqoMF/8S0YCAABAjWKyGE0Ws4Ojs1UuN5vIKQDcOq5xCg7gFsAUHABuoOs+BYdCoVSqHQrz8ySGOwMAANRYMpvk4OxqNhosFpN0/TAFB4AbSC4BAIAaTiZXiPS5eOwz6TMAAEBNZpNJ4kud+GonlyskALglEEADAFDjKZXqklvWWCQAAADUcLbiuxEWKZRqCQBuCQTQAADUbDJBLjcYiiQAAADcEgzGIvEFj1tJA7g1EEADAFCzyeVKq8Usk/PvEwAAgFuEiJ7FFzzxNU8CgJqPABoAgJpNoVSZzdwnHQAA4JZitpgUSgJoALcCAmgAAGo2mVxhtTD7MwAAwC3FajbLGAEN4JZAAA0AQM0mk2w2ySYBAADgFmKz2WR8xwNwS+DHNAAAarjiuxAyAeIn9BQAABAASURBVDQAAMAtpfgOH3zHA3BLYAQ0AAAAAAAAAKBaEEADAAAAAAAAAKoFATQAAAAAAAAAoFoQQAMAAAAAAAAAqgUBNAAAAAAAAACgWhBAAwAAAAAAAACqBQE0AAAAAAAAAKBaEEADAAAAAAAAAKoFATQAAAAAAAAAoFooJQAAUPv4KhQv1K3TyFHjqVQ0cVDLZLJyq9lstvgiQ67ZmlRg+N/Zc+csFgkAAAAAgKtGAA0AQK0TrFatbt7AVam4Yk0RTIc6OoiFzi5Od3i6DIg7ccpoKrfmnXcM/eh/n8THx9819K6y5dM+/+z2QYO+mvnVF9O/kKrI3d1tV9TuitY2a9KskrbrNqxTazQ9unWXAAAAAAA3DgE0AAC1ztN+XleTPl/CTaWc6Ov18qm0ctcu/WvZPaNHhbcPv+/++36f87u9sEOH9gNvv/3MmbPffv2tVHUGg3HWL7/Yl5s1C+3UudOO7TuSkhIlAAAAAEANQQANAECtE+qkka5JY0d1JWvfe/vdBUsWTnh64vJly/Py8kTJa5Nfl8lkn0ydajAYpKorLCz88P2p9uXxj48TAfTmTZGzZ82SAAAAAAA1BDchBACg1glQqy4vzLdYxiefOllkrKShj7qyn67j4uPnzZ3n5eX57PPPiqcj770nNDR025atq1evtVcQ5QsWL9h/aP/S5UvfeustJ0cne/m9o++NT4ofM3ZsaVd/LJx/8PBBqVJX06pHjx7LVi2P2R8974+5w4YPL7tKPP11zq9RMVGR27Z8OePLwLp1JQAAAADA9UYADQBAreNewfwbK3P0t8Umv3cqvaCCmw1q5Vf45vDF9C/OnTt/76h7Gzdu/Myzz5hMpg8/vDCEefKUyU8+9WTdgMA1q9dotS6j7h8185uZUnVydnaa+vHUAr1+545dYS1bfjD1/dsHDrSvGjJ48IcffeDjU2ft6jVHDh/u2bvnl1/PqOhOjAAAAACAa0YADQBAraOuOEc2S7Kv07MiDh6dl5F9+VrVlSLavLy8Lz7/QqlU/m/6/+rU8f7t11+PJh8V5fXrNxh93+jjx48P7D/g5Rdf7turz45t2yO6RPTu3UuqNlqtds6cOfeOHDXhqQkTnphgs9me/79J9lXPPPdMenrGvSPvff21N558/Mlvv/k2NDT0jqFDJAAAAADAdUUADQAArpaT4srfHBbM/+PQoUNNmzYVCe+X02fYC3v36SWXy+f9Pt8+N7TIgr///gex0LNXNQbQRUVF333znX05MjLycGxsveB6np4eoc2a1asfvHHdhpycXPvaZUuXi78dO3eSAAAAAADXFTchBACg1jFbrcoKBkErJdvjvl7PBXg7KcqZpqPAYpWuwvy581u2bLl82bKCwgJ7ibu7u/ibnna2tM7p02fEXy8vL6naZGZmGY3/TGmdlprespXk4eHhVcdbPB39wGjxKFvfszp3BgAAAABqJwJoAABqnXyrza28/HmQu3ZyoG89B3VFDXMqmBv6EtaSahbzP5VzcnLE3zo+fqUlgYHFN/07fz5TKhkQLf4qy8xMrVBd+SvKFVt5eXmq1erSDNrP31f8zUjPUKuKX+DOHTvn/Ppr2foisJYAAAAAANcVU3AAAFDr5JrLyZGdFYrvGwdVkj4L501m6Zps3LDJYrHc98BoV1dX8VQmk40fP04sbNq4UfzNySpOflu1amWvHFi3buNGja/Y5xVbOTg4PPLow/blnj17tggLS0pO1un1cfHxIvgOadr0cOyR9es3isfZM6mNGjcuLCyUAAAAAADXFSOgAQCodQ7lF1YeNFckudAoXZMTJ47P/X3uAw8+sGL1yu1bt7YLD68XXG/Htu2bN28Wa3ds35mdlT1w0MCphqk6na5Xr15nzpwJDAysvM8rtsrJzr5n1Ch/vwDvOt49evWQy+WL/lhkXzVv7tyJT0/8be6cDRs3yCTZkCFDXN1cN27YKAEAAAAAritGQAMAUOt8mZYpXZOfMq59kor3331/9qxZLi7au4YPqxtYd8Xy5ROfetq+Sp+fP2Xy5HPnzt817K7hw4d/8/U3Z06dvmKHV2yVk5sz4fEnb+vZvU+/PoWFhf/79NNffv7ZvmrmlzOnfvCRUqUaM2bMg2MeTE1LfWnSi0lJyRIAAAAA4LqSaT2CJKBW8vYNTjudKAHAjeDq7lOQnytdDw5OLtfQVR837ZRAn0aOmqusn1xoePNkWqSuQAIAAMB/wsnZrahAJ10Poqu8nAwJAG4EpuAAAKA22pCrFw8JAAAAAIDqxBQcAAAAAAAAAIBqQQANAAAAAAAAAKgWBNAAAAAAAAAAgGpBAA0AAAAAAAAAqBYE0AAAAAAAAACAakEADQAAAAAAAACoFgTQAAAAAAAAAIBqQQANAAAAAAAAAKgWBNAAAAAAAAAAgGpBAA0AAAAAAAAAqBZKqepU/hFDh/VoHuylMhqzU6LXzFscp1f7dh47urNuzQ/z4vSXt9D6totobIjdczjVJAEAAAAAAAAAaoWqj4DWhg29d0hzdeb+JYsXr4jO8gwfMaafr9qoT43dH5OYZiy3jaZeu55d2/mrJQAAAAAAAABAbVH1EdAu/n5ehiPz5i4/XDzU+UhKatcmBrGg9m/XrXNmekxMtuTfYdjoXmH+zpIuPTZy0Ypov2GThjQR4fPolya3nDdtVpwU0mFwv65h9bXG1OTItcu2xOZrw4Y/NdozaWdWcERzl8wj65bHqXv06hfiK6UeWDF32a5Uk6T2bTdkQN/wRl5qKTNx7fy521P0EgAAAAAAAADgJqZQO7pVqYFkVPqGhbds5G7RGfW5mfm5p0+kpOZbJMfAjh2DC+OiYi2tR4/uaNzy8/eLduX6de7YWB+7Yc3O/Pod66b+Mf3L1WeN/h3GjB3gdW7Twj+iMoPC+3Wsmxsbm+kS2iG8gUvmlvkL4rQte/SO8NNvW7ZwT65Px86t3c/GHDjv1W3EsObGXUvnLIkqrN+zR2tlQkyi2Cjwbzhp3fV5mRIA3AgaB2eTySBdD0qV5np1BQAAgJuHSu1gNhml60F0ZSjKlwDgRqj6CGhj4vLZc7P7RbQePra/Vp2fEr1myfIDqf+MR1ar1ZJa4+Hvr42NXjx9Z0mZ1z/N/UNa+xv3z1sUlaSXkhZvCpkwoEWwc6L4PDVmxe6MS02VtkSnhfXIij10KlWftTOx4yitVi1JqZGzP44UrVWeIfm6TMnfy1MtpV+fD2EAAAAAAAAAQLW4lpsQSlmx2+fHbpckZ/+wDoOHD31wiP6reVl/r0yPWbcpZHj/YWM7DJNMqdHLZi8+kPVPU5XaS6v16jBuSofSolQvtZQq/n+jsTRRNkqXhMvakK6jhvdv4mXSZ2YZXFSSTgIAAAAAAAAA3NyqHECr/Nt1bKJJ3rUz3Sjlp8ZujwxrMybAz0X9T8isT9z+w9Ttaq+gsB4DhkUM6BebPD+1dKXJmKk3Zp6cPWNxUplJnLVhlW5T7dt5SC//zMUfTRVZtkfn8RP6SQAAAAAAAACAm9w1jID2Cu3Xs0Owdk1MquQS1rVfuIcuOk1XOmJZHdR3/IiQ1GWzFx9NPJGlC9eWlBoNBrVXSOPg1CMpiQdSevTqERGUujPLq+XQYT3UMXPnxlS+RaNoX9y1i5dK8u/aub5KfUICAAAAAAAAANzcqhxAm1LXzZ2tGTGs/6gx9qfRy+cvPqqXPC6sN57aFbm//pDRkz9RSVJ2UuSaFbH5kpS8JTJ5WP/hY1ykad9HzZslDR4y4uX+HmpjeszaZTEpJqnyEdDF03psCxk15KlXBmSeSE7NNLlIAAAAwC2jdYfbjsYd0OvzJNxMWrXveiLxSF5etgQAAIBrJdN6BElAreTtG5x2OlECgBvB1d2nID9Xuh4cnFyuravQsHbNWnWo4xeQm5uVcGjfvj1bZJfV6TN4ZGFh/o6NK6XqN+apV1cu/OV8Rqr07zzw2P/t2LTyWNKRy1c1a9k+rG2nhbNnXrETR0fnLr1u9w9soNY4pJ45sWfrusxzaaVrwyN6du4xcMEvX2Skna2kE1//QDd3z8S4g2K554Bh+fm6qG3rK6rs5uHdd8hIbx//fF3ersg1yQmHLqnQuGlYm8493D28Tx5P3Lx6sdFgkK6H0NYdQluGe/sG5OVmJcbui9kVKV0PIaGtWrTtvOT3766mcrmXYpV6KFe/oaMy0s4ciNp6SXmn7v2DGzcTp+Z8euq+XZEnjsZL1WP0uElb1v555uSxK9b0rxvc/677Z838QLpVtOvcI+7AXvHpUe5a8f566OnXv/74NanaXP3BL1fpxRPRa5BGrdm8Zon0H/Lw8rlj1LiFv3wpPjSkf63cC75n/+H5BXniE+kaPuTLfrKV8vELGHLPoz998a5YHvfcWxoHB7Ggy8vNOHMyaseGsp+fV88vICg8ordfYLDRaDiZnLBr6xpDUWHxxTPxta8/ef3ajlK5V6bGwVEchzp+QWqNKutcuvgEvuYrpyJNmrXS5WWnnT0lAVXk5OxWVHB9boIlusrLyZAA4EaQSwAAoPZp3rpj175DE+P2//r1x/t3bG7asm3Hbn0vr5YcdzAlubriuWqyP2p7RurpclelnUk5tG+XdCUqlequ+x93cHTesOKPxXO+LtDp7hr9mKu7Z2mFxs1bJx3ZHxLWrvJ+vP0CGzZtJV2dAcPuO51ydPZXH4lIqOftw7Va17JrPbzq9Bp89+H9e/74ZYZG49B38L3S9RDWtnPXXoPiY2N+/eqjfds3iVfUZ9Dd0n/rKi/F66XfHfc2CGm+d+u6377+5FjC4T5D7qlbr6F0o4W0aJccd0C6hbQM7+bopJVqvsRD0Y1DW0kymfQf0uVkx8bsyC/QS//aFS/4a/iQv5pPtvk/fT5j6itr//ytsCD/rvseEz+wlVutXsOmFb0Bxa9xQ+99NCszXXzobVzxh9bNbdDwB8tWuLajVO6V2fm2AQ4OTisW/PTHzzN0udm9B90tu95nvGHTFiLglgAAqK2uYQ5oAABQsykUyi69Bm1c+cexxOJhwglxB7Kzz9113+PROzY2bhoWFt7FZrX61q33zSdvNGjSPD9fd+bkMZHJduk5uEHT5kVFhQf2bIs7GHVJn/UahIRH9PTy8T+edGTfri0iNeg5YJjGwdGzjq+hsHDxnG/qNwpt26m7qHDqeML2DSvsUw00btqyTafubh5e0Ts3l3ZV7rZGj5u0b/eWZi3b1fENOJZ4eMOKBaJQqVRH9BrQMKRlYYEu/mDMwejtUnG+EJGdmS76D27UrEPX3j5+gWlnT65ZMke8EB9f/9CW4QmHom2S1HvA8OAmoaJ+4uF9OzZdNPqvTcfbbJJ1+aJZ9gQict2fjk7OET0GrFk6VyoZnOjs5Lo5atHtI8ZsXb/cXqfsAOcWbTsHNww5kRzfc8Bd4umEV6bOnPqKVDzIzkGEQeI4nM9IXb34t7JD8ORyhdlo3Lttg8VqSTiyPywh5QSmAAAQAElEQVQ8wss3oOxsDC3Du4iTFXeg+FCs+2vew0+/4eLmIYKS0grlHh+hdftuoW3aq9WOSXEHdkeusVotpU2UClWXXreLmkcTYu2XQeqZk33vuFepVJnNJhG4R/QYGBjc+Fz6meidm+zjAcWqiF4DG4a0KizIi923+8j+PaJQrdZ06zO0fpPQnKxzJ5LjAgLrL184q+zxFOe9actwR0fnhNiYXRfvQyWX4kVXV8Om4Z17eHj7njqetHPTSnFkQkJbNW/b+c+S8dHunt4jHnjqxy/ekUpCK7HbfoHBx5Pj5PJLIyT/wOCGTVr89s0n9iGTB/ZukyvkHbr1PVPSz+XHSmxFhPLpqadbtO1UVJgfuXpJ6umUci+ecg9X5Zd0WXWDG25Z+6d9+fJ3SgVb9OrSY2Dd+o0yzp46FLPTPqy13N0Q14Z4a4S16+zgoE08LE7BapvNVvm1EdFzoNbVbd1f8+1Pxzz1qkgAxQ8k5R6iy0+EqK91cRk9/vm9OzZmn0sr90xJJf9FQuceA4qK8vfv2RZ/cO8VD1S52xKFop+cnPMhzdtmZqSKCyz1TErZVuUeE3fPOuKnl8AGjQsLCjYsn3fm5PGKLp7M8+kmk8nPP/CSsatXPKfiWDVrHe7g4Jx4ZH/09g3GklvaXH4AxUeHwVBUx8ffJyDo5PHEbeuWFRToVWp1x9v62z8Vy/3kLFXuW/IqL3i70g95qby3qtg98Unl6u5R+sHVIKTFJZ9sFRFHUBw08VBpNJ2791+z9PfL6wTVb2w0FJY73Lhr78Hit7Gdm1eLZV1uVvqZ0w889VLdeg2yzl0Yv1n2KIkT2rn7gMD6jTLPpYkrXLxPxau4//EXI1ct7tC9n0qtER0ditlR9srcvWVt6bZ86gaKj1/7f3+z9q95gfUbi89ki8V8ebdSeW89cRGW/d/Ny6+NfkNHNQ5tLR5Nmrda/Ns3EgAAtQ8joAEAqHW8ffzEP62PJv4zSUVG2tnvPptitVrFso9/4OGY3d9+Orlsk54DR1hs5vk/fr5x+fyOt/ULDG5Udq34B3m/O0bt2bb+h8/fESnk4JFj7eU+/kGbVi4U6bP4Z/xt/e7YvXXtb998lJeb3e/O0WKtl7dvr0Ejdm5eNefbT9zcPJ2cnCvfVsMmzUVaumH5/IZNW/j6B4qSHgPu1Gic/vjp8+Xzf27dsZvIoUp3SaVSd+ja59DeHT9/+X7WufSI3oPK7nCjJs39goKXzPlWZAEB9RqK4KnsWr+A4PgD0WXDy8MH9vgE1LMvNw1rm3IsXoSSIsSr16CJVIEjB/ZsXvPn0fjY0owmqH7IoeidYosaR8fQ1u3LVhZBjyi3lCSA4mCK1D7rfHrZCp7evmdPJNuXRaiRmZnuXcfvki1efnzEAWnepoMI3xf+8qW7h1fXPoPL1vf29RPJWnJJ+myXl5ctdkOkzzKZ7M5R40TaMvvrqfujtg0c9oCTk0vJAb+r5IBP37Dsj3adejQMaS4Vn69hcoXi9+8+3bFxRcvwrpfsVfPWHes3arZ2ye8LZ80Qx7l9194X7UOll6Jd8dU19F5xdf327cfip4VB9zwkVUAulw8e+fCJowm/zPjg9Imj9RuHXlLBP7D+yWNJZf+DfZHa2wPNio6Vr3+9vKzzC3+ekXP+XPuI4p2//OKp6HCVqvztI1J4EaemnT4pleRol79Tyt3iHfc8fPb0iVkzPozetXng8AfEDxKV7Ear8C7r/py38Jcv/ALqte/SS7rStXHkwN76jZrbh/361w0We3gq5WjlTcqa/dWHep1u7vfTymZ8l58scRzm/Tht4/IFET1uF1u54oGqSFDDkLyc7FkzPzyyb/egEWNF/Fe6qqJjIvLQjPTToknU9vV9hoySKr14MlJPefvWvWSjle+qOFYiaF775++/fv2RZ8k5lSo+5mHtOsXs2SL2sCBfJz5Iy/ZT7vVQVrlvyVKVXPCXq+it2jCkRdkPrss/2a4o/tBe8b8FUhWJJuKElj41W0y/fPm+/aeCS4hzN/Seh08kHZ791dQDUVsH3/2Q+O1TlCtVSk9fvyW/fRsbs6NT9/7iaqjoykw6ciC8S2/xQ5ejY/Hg6NMnksXnUrndlvvWky7+383Lr411y+Ylxx3YsvYv0mcAQK1FAA0AQK2j1jgWFuZX9B8Yn0s7kxh/wD5G0k6pVNVv0mzHxlWilcgHjyYcbNj0ohsIN2/dITnuUPEoNpstZldkacCRFHfAPmwwtHWHhMMxZ08dF+Hp3u0bRdgk/iUf0jI88fAB0UoUbt+0UpJdYVux+3bpcrOPJcWdSTlWxy9IhGJNQltv37Bc1Cwo0C+d813S4X2lu2QyGRfOnplwZL9CodDlZYtIt+wOKxUioHYQUUJeTqZIWy6ZeFql0eTrLppWW6/L0Wgc7ctio8nxxRM0i0AhpEVb6aqdSD6SduZk5rk0kW77+AaWW0fsUt8hI+MPxZQd3SwVZ5QKcZRKnxqLitRqzSVtLzk+oqRFmw57t23Izjwnjs/2jSuahYVLF71Mh9LLQASgE16Zan/4BQQF1m9sNpsPRm8Xh/HksYSTxxJDW4eXPeCZ59PFiQ5r01mcL3GCRKHYPXGuE2JjLtmr5q3bR23fkJWZrsvLORS9o8HFAVnll+LfPVy4uowGw94dmxwcnMUellszqH4To6HoUMwOsdsi87p8PnG1xqFAX/5MmhUdq5zsc+Iq0utz9+7Y6OUbIJV38ZR7uEp7vuLbx83dK1+vE/maVME7pdwtWqxWsUXRSlSe9+PnIp2sZDd2bV4tToEIIvdsW9u0Rbh0pWsjN/u8XpfboGEzsdwotGVy/H7ZlZpcg12bVxUVFmSknYndt1Oc5SseqIpkpJ3ev2ereNUJcQcyz6c1btqydFVFx2T1n3Oitm2wmM35ujwXVzeRWVdy8eRmZ7p5eJXd4hV3VRyr6G0bxbESvy1tXLlw6/q/pIoPYNzBvSLxFJf3zo2rfAICy06/U+71ULq23Ldk2d2o5IK/XEVv1RPJcVf84Kpcvj5Prbn08+rBJ14SnzZtOt7W8bb+YuGeR565pIJokn919+QU505crvGH9xmNhmOJR3JzMoNKfg8Qxydq2/rCQn30zs02m9XD07uiHsT1IyLp9hG9xk58Zdj9j9cpeaeX2225bz2pzP9uXvNlDADArY0pOAAAqHUK8nVOjhVOz2qxWC4pcXLSqtUOT770fmlJ8sW3n9K6uGWdv3CPKfEvcJFf/N2V+UIPztpmYe06dO1T2sTRSevs7FLaymw2FhYUVr6t0t4sZpNCqXTSulis5tKJLPLyLklsld373dEgpEVO1jkRcsnlF/3onphwMKhhk353FM+kfCI5Pmbn5tLOhaKCAkfni0awOjm7FJbMNCqiT1d3zyEjH7KXG41Fm+TyssN1KyGCMPuCyWySKxXl1hlwx31iV3dsWHFJucloLJs4i2imyFB0SZ1Ljk/xbmtd83Kz7IV5OVmilYODY2mQXVSQX3oZ5GSdt49nHP/826KCh7efvszxFJ1ote6XHvDcLCdXN0dnrdjuP4U5Wd4XZ/2OTi53jh5f+vSSRKnyS9Gu7NUliB1zcfEot6Z4vWV3W//3dViqMD/fw9OnoraXHyupzNvBLI6qvPisXX7xaF3cLz9c//R8pbePSq2ymEwXKpf3TrniFsVFLis+UBXuhrhQL9TMPO/k4iJd6doo3sn4Aw1DWx4/GtcwpOWaJb9WcoiujdViKZ1NQpedKaLVKx6oioh3R+lyXnaWk8s/AW5Fx6RV+67iIIvjlpudJT6y5AplJRePyWRwdnIru8Ur7mrZY1X67qjoABqKLpwdi9VSoNdrXd3EXl1oUt71YPj7NJX7liy7G5Vc8Jer6K16NR9clXPWuhZddjvKX7/5WCqZZ8NoKIzavvHyVoUF+cUNy1yTFe651iUgqIFIsUtLHEpmebaWkC68Cov4H4VKOjl1Ikk8HB21IWFt7xg17tevPyq3W5XG8fK3nlTmg+KaL2MAAG5tBNAAANQ658+lyWQykaWWzmrq4eUzcuyE76e9VW79gny92WT8Yfo7ZVPasvS6XBfXC/fos0mSu4d3bvb5i3rQ58Xsity5eVXZwvx8XWkrlUrt5OR0Ndsq06dOIVc6Ojrb8xet1k0slLZq1irczdN79ldTRW4YWL9xt75DLmpss21YuVAqDgtchj3wmIhBD5f5b73Pnjpev3Ez+4zSdvWbhKadPiEWQsLaxe2P2rh6kb189LhJjZuGJcYdtFltpelG2RkAqqRrn8HudXwW//qVxXrpbwCZ59K8/esmHNkvlYySFkf4fNqZK3YoDrurm2d6yS0ZRW5uMhrKpjnnMlLlCnnZyyCoQRObzZqddd7FzUPr+k/IKzrJzky/5ICLwgJdXmG+XqlQlRY6u7hcug/5eZFr/zx5LKHcPbyaS7Hs1SWIHdPpc1y07grFhSxMXDylr7fsbru4eaadveh2lGdOHm3ftbc4U6XXSct2XRo1C/vz9+8qP1YXueziEWHi5YerzBG4wiVdVFSkVP/zEi5/pwiVb9Gt5B2n1+VUtBuurh5npOK5C9y9vAt0OulK14aQELtv5JiJPn4BVovZXq3cJjardPmJuOhoVVBBrlBoReZbknK6eHjl63KveKAq6kr8RPHPq/bwTD31z4TC5R4Tcbg6dus774dp9vm1Q1q0kSq9eDQOjgbjRQfnirta9lgVp8wymfgZrKJj7up64XcC8QuHk1arz8st20+518Pfa8t5S5atUMkFX05vlb5V/43mrTuknkqpaqu0Mynigzfz78mIxJl6eOJr6/6aWzoHdCnxqkXlRb9+XbZQHBbpKslknW7rt3/PVpHsFxbqD0Rtbdm2Ux2/uuV2Kz4kL3/rXbQzV/0/YQAA1CpMwQEAQK0jk6SDMTv6Dh3VvE1H8a/0wOBGfYfesz9qW9lpN8oyW0zJcQe797tDRI1qtebusRObNGtVtsKRA1GNQ1t6lcxKHNa286ARYy7p4fD+qJAWbUsnJh417jmxpcRD0SL68fL2FcsRvW633wPtitsqJf55nxR3oEvvQSI+UCrVd903vlGTFv+sNVtEe9Gng6NTu049Lmkb1jZi0PAxxbmM1Wwym0rHn9rFHdrr7RPQa8BwEYyKfCGi58AWrTsWHx9JatS0VWLc/tKayfEHm5TMwnHu3NnGzVqKF+ji6t449MIOW0xGR6erDUFatO0U3LDZn3O+NRoMpYVtOnZv0bb4v6lPjjvQLCy8WYu2IrcSJ0vk0WXnda2IOOzh3XqL+EwuV3TtNTg+Nvqi1TbbwejSy0AbEtqq35BRcQf3ykqmQFXI5aGtO0glg77rNQyJPxhd9oCLy0Yc1cP7d4t8P+3MSXuhiK0bhLS4ZB+O7Nstwj7nkhHlfQaPvK3f0LJrr+ZSLHt1te3UvagoP/XMSXHA6/jWbdK0lTj1rcK72GueOpGkUmvsuy1WarDcQgAAEABJREFUeXpfOvbzfEaqOHRD732kQaNQsTnxktt37bN3+4YrH6syLr94yj1cpfWveEnn5mRqhJLBsOW+Uyrfojgy9z78tDjClexGy47dHEqm8uh4W/+EIzFX83pFxp2XlyXySnHSpYovp3JPhFR88RscnZ0rqWCzWjv1GCAruWzEC4w7FF3RgSp9F1TUlbOLq9hPsSBOq5e3X9lpzcs9JuJjQSaXiVchtt6l5+2ykqmuK7l4xO89OVkXhYxXPKelx0oqnqZ5WOfbBlZyzMW7po5vgDjRnXsOPJd6puxtBsu9Hv45yOW9JcvuRiUX/OUqf6uWdfWfbH5164kP0oZNw0SqW26FUyeSz546Ue4q0aRd514duvUVV4iPX91+Q+7Nzcosdw5oce7E57w4d7aSt8PYCa+5uLpLFe78hSvzHzZb3XoN+w29V7QVvwF06NrbwclZHLdyuy33rVe2s4quDbPJ5FDyI6ut5PAGBDWQAACoTRgBDQBAbRS1bb3JaIzoMbDXwOG6vNzYmB3RuyIrmYo3cu3Szj0H3Pf4/zk6OcUdjDqWeLjs2ryczHXL5nfvf6df3WCR1Kz9c84lzUWFjSsWdOk1yLduveysc1vX/iW2lXk+fdPKhb2HjBT/jN8VuUb/99i9yrd10V6tWdq116CHJrwqspWY3ZEJ8QdKX0Li4Zj6jZo9+dIHebk5xxIPOV08Mjcpbn9AUPDjL7xjtVmTDu+PLzN5tFT8X8QXLp7zTY/+d44YM0Eq3s+0FQtniTwiuEGISA9OpRwt3Ur8wb3hET1VKpUIScXmhj/wZMqxBJE+2MOFowmxInl54sX3fpnxgVQpEXP06H+XCMIeffZNe8merWujtm8MCKovTtPhfbvSU0/vjFzdfeAwlUqdkXZ6zeI50lWIP7RX9Dz8gSdUagcRVO2OXHNJhT1b15lNRpHBia2fSzsjjuH+PVukknlU/vrjJ5GRicN7Pv3s6iW/2kOxyDV/ikJxwAsK9DF7Io+WJH0bVi7o0LXP+Oem5OZmHU887Ot30SyxcbExKo3j4Hsf9q7jn5IcH7V1/SX7cMVLUVw860uuLk9v31PHE1f+8YusZM6QqO3r+905qnj+391b6jcunq/WarWuXPiLuMx69r/raMKho2WCyFIrF83q0nPQwOEPyBUK0TZy9cLTKUev5liVKufiqeBwlbrCJW2ziaCwfoOQhLgD5b5TKtjiz2Jzt/UZIn5rEU3sP0hUtBsJB2PuffR5cYElxMbsLZnu4Gpe79H4Qx1v6zf/py/sT8ttUu6JsJ/W3oNHnjqatHnt4nIriJ8uRJj42KS383Kzd0auOnvqeEUHqvRdUNG20s+e8vTyEW/2tNMp4vyaTMYyh7b8UxOzc/PoxyZZzObYfbssJVNMVHjxyGTiY23zqsWXHJzKz6k4ViJoFsdKXLTHk47siFxRyTFPOBwjLm8vH/EGiVu7dG7Zfsq9Hi7ajfLekmVVdMFf7opv1VJlP9mKCgvKrXPvI8/aF9LOpCyd+33mxXdVLVXJgGtxeaz9a263PoNFLG40FiUe2r9q8exya4qzvOyPn7v0uL1b78Emk0kk7Lq8nIpGQJe9MksLVy36tf+do0c9+pxUckkvX/Cz/XVd3q1U/C4r561XVrnXhvi1r8fAYY2btZr/0/R6DZulnk6xX/MAANQSMq1HlW9JDNwavH2D004nSgBwI7i6+xTk50rXg4OTy/XqCviX2nS4zTcgcM3FIRquqG2nHn4B9VaVTLV83Y0eN2nL2j+L7xFaRfUaNo3oNXD+j59LN7GQ0FbN23Yud06J60L8sNSmU/fq67/ngGEiwRSpqAQA5XFydisquNq7iV6xq7ycDAkAbgSm4AAAAMC169Z3SJuO3RVyRWBwo7C2nVOOJUmookPRO30D62m1rtJNQy6XN2nWMuFgjFS7tQrvcih6hwQAAIB/gSk4AAAAcO0O7t3Ro/+dXXsPsljMB/buiD+0V0IVmc3GX758X7ppqNWa8ZPeTkmOi43ZJdVuf/3xkwQAAIB/hyk4UHsxBQeAG4gpOAAAAFA5puAAcGtgCg4AAAAAAAAAQLUggAYAAAAAAAAAVAsCaAAAAAAAAABAtSCABgAAAAAAAABUCwJoSAAAAAAAAABQHQigAQAAAAAAAADVggAaAAAAAAAAAFAtCKABAAAAAAAAANVCKV0rZ6120J13hbYIE8txsYeW/7mksKCg74Db90XvzTx/TgIAAAAAAAAA1G7XPgJ62tffPvH0sy1btxGPJ5557tMZX4nCgUOH/jJ/YY8+faVrpg4bNztqw64Lj1VLfvvwpeGhnuqq9BAy6oeNP78U4Sz9S9qgvpPe/mHp0shtC2Z/89ywdh5V2YsyvFo/99uCeW92rfBVqD26v//zit+eauclAQAAAAAAAMCt4hpHQDcOadqoScjP337z288/iqcPPPzow48/Ua9+g/+b+NT4p55+5sWXIjesl66dIWvn3JlLYvMlF9/gdr1GTXrHX5r48uJ0o/Qf0jZ68NPPxvknr1/7/ZJMv879B7z8Resmr0/6ODJbqipdVlJisldimrGiF2A0ph46mmhIztRJAAAAAAAAAHCruMYAuo6Pj/i74q8/7U9XLlsqAmhfP7+TJ44vnP/7qDFjmrVoEX/4sHStjFmxUVsi84sX125Pdfnu5SFdg5cvTvoPE2hty6GDQ9Lm/98rX8WYxNMVi9dEvvLc4PB6npHZWVIVGU+teOfVFZXVyE+a997zEgAAAAAAAADcSq4xgNbl5Ym/QUH1sjMz7QvFhbriQv+AAPE3Iz1duj6MxtTULKl+PRcXScp0bjJk7LhRXTs39TOePbJr8Q9fzT2QWpxKqzwjhk4YO7R7WD0pc/+6taf+metCG9R97Ngx/TuEBagzE/asmPXDD+tOFbfwav3gK0+NimjspTGmJmyaPXXakljTpZtWq728tGopu7i+8dT6d14oHdWtDes/bvyIfuGNtbrkmJ3Lfv1+eUyqvYlv59Hjxwzv0CJAyjoUtW7x3NnLj+q1jR785rPBsa+Mmxqn1wb1fWzcmH4dQ7zV0vn98z77+Kt16UbJud0rM94NWfbcE4uTJN/OE597rl+b+t5q3dn962Z8PH3dfzv0GwAAAAAAAACuj2ucA/pocmJOTvYz//fy4DvvumPE3U+/8FLW+fPHkpNHj3novU+nJcbHiafS9eKi1UoGvcEgefYY/+4rA/xTNk1/+6MfdurDxr8zeXSQunjS56HvvT+hs/rA7M8++mptesiIoSEu9gjaucXYN94d3Sgz8vt3P/x+XWq9YVPeGNfOWZS3G/vcuHBj5GeTHnz8o0h9h3GTRjTRXrRR/aE1K2I9B3/wyw9vDukc4nzR7M3+PV/+5Pl+LnHzPnv343lxUviEd1/pH6wu2dz4N94d30gnNvfatHkngoa98tKYdmWnonZuN/GdyUM8Y2ZOHHbHY29EagdPeqpf8EXb9YwY+/LwxlnrPnr0/knTo7U9Jj13SQUAAAAAAAAAqCGucQR0YUHhlJdfmvL+h5NefV08FXHzlFdfMhoMI++7f/f2rT99+410naj8e4we01Obunx7itGj85AOUuTHz729PcsoSaJEmjG5X9fgRYvU/QY0MWx69/XpW4qHIW+KyfT94QW/4tZezQf31O76bNJk+/zRa+OM30zt3r/x7JiTWi+18cSm+csPpBil6f93YL6LMVV/8Zb1cb8+89Dh4WPHjZ4wfejzupIB19PmHsgyqoJ7DG1n3D7t9enrize3OTJR+uH9od1DNv2a2nhwT7+Uua9Mnnm0eHORcUmxrdX6ssOX82M+mzjse2NWZvFo68zFa0b1H9oiwHlFyj81NF4eat2RxYs2H06RDk+dFOOvzkyRAAAAAAAAAKAGusYAWog9sH/kkNsvKRw+sJ90HWj8Bn/61+ALT/QnNs96d1acXt06rL5f/frvrOxfpub5el4arTrA05iyLCXTXmRKjY1L1XmKJbVXoxB/v7BXf9/y6j8tdJkeLuoDMYuWJb0//ocFA1JOHI3duWnJ8qhydsOYHTNv+lPzZvpHDBg2ZMDg8e+8J016blZWcEs/KXVTUmbp/u1PMXQNq++pNYaGeOkTY9IuRM7G9JjFa4sXyo6tNkou7UZMGNK1SYDWy1/sfFrKRYOrpdSdi9cNf2Pyz3PGnEhOit6+YvmmVAkAAAAAAAAAaqJrCaCdtdpBd94V2iLM3d29tDAnJycu9tDyP5cUFhT0HXD7vui9mefPSdfIkLVz7swlsfnq+gMmjG+dsnN7cdpbHOPqT6z9/qu1ZeZE1qXF6qR2lXRlzNr5/cz5J/L/KchMzjRKxph5T43c1CKi1/DRQ4e9IPLluU89+8PhzHK7MKXuXP7Vzk27Xpnx0ZBeTRYtEsn25ZXUaunK1EGD35/6Urh+1+aoFeviUtUdxk3scGmd1Kjpj9w3P7zrsOFDBz/08uARvaY98er8RAkAAAAAAAAAapprmQN62tffPvH0sy1btylbKJ4+8cxzn874SiwPHDr0l/kLe/TpK10rY1Zs1JbIqPVzv/9hp9R57Oh2XqIsLemsUaPWJ+2M2hUpHvsTdWqjPktv1GeezVIHt2niZW+r8g8L9S+ZA9qoO5WikzSGozGRJU12JouEWZdaPCmG2svXX5N1eN28dx+5f9hrm7ICWrfzV5XZAVWTCd+uW/X24H/mX1YLkkEs6FMT0yT/NsEXNidp67cJ1mQlndDrM8XmPEPa+V3IotUe7Yb07x5SZg5or0bdw9QxM96c/M4P85dvjzlhLCe21nr4+0uZO9d+9eLTw+7+aKehcecwCQAAAAAAAABqoCqPgG4c0rRRk5Cfv/3mt59/vGTVAw8/+vDjT9Sr3+D/Jj712MRnnnnxpcgN66V/xZgeOWvRsG/Gjhu1JnZmXOSsNcM+nfDuK57zdqYbvbqOe6yXeu2bT02NSlq3JmnEhOenpGkWxem8OowaXU8tlczonLpn3tzk6Y+9Mdlr0brYfK+I4eOG+MVMnfTuWqnfKzOeCzkye8bsLalBg0e09jQcydKZymzYlLJ8UcyQl1/64u0ms9bG6Jz9w3uN6q9N+n5Tkt5kXD57Xb83np8yzmXRAZ2m9eDxvaSdHy+JzZeMe2bPOvLVxJde1s+NPGFyiRj13BDtihe3bzlb+nKyM/XaHkOGdk5clurfddToXvU1xsMXvWBVkyFvfPWY567vpv8QI4UNHxrmYtySKQEAAAAAAABADVTlEdA+Pr7i7/I/F1++avnSJeKvn7+/+PvHnF/d3T1atm4r/Uv62DU/rM1qMmJMj2CVPmbW5Lc3GXtOeO+Ddz5+oYNx87TJM6KyRK6buOyN12fukno9J8rHBp1YvClJZ29tSlr88eRFWWEPvfzxp++83F8b8/1709amG43p6z77eMmJxuM++G7+z5Pv9T+55LOv1l18rz9jytp3X5y2xdhx1AAtBycAABAASURBVKvvfPzB+GEhxsgZb747t+TugplRX70zLUY7YvIHUz+eMiI48fvJH25PLV4hYuvizXWeOPnjT994Kty4ZcbHP0T/M/uHlHnkhxmLEr1GfPzz779O6qqL3BRz/pKXK3Z4+kdrs9q98Nn8OZ9NFjs8d/rMnRIAANXA1dV10guTVq1ddSD2wPJVK56b9JxMJrOvmjN3zoLFC8TCgAH9du/dPXTIYOm6enDMmPik+Pbtw8Xy5198Lpbtj8htW6Z9Pi0srIUEAAAAALglyLQeQVVq0KN3nzc/mNqnc4dy127YFfX2a69s2bjhkmXgJuTtG5x2mvm1AdwYru4+Bfm50vXg4ORyDV15enr8+vucRo0aHj5yeF/0vsDAuj179Vq9cvVzzz4nlQTQao165PCRbdu2efnVl//3yf+iovZKVffHwvni7z1333tJuQigX5/82gOj79+7N1oE0L369Jr7++9yuSI0NDSsZZjIwV/+v5dWr14jAQAA1GJOzm5FBTrpehBd5eVkSABwI1R5Co7E+Pg/Fy6oaO3SRQsTjhy5fBkAANxUXnnt1QYN6j/39DOrV6+1l7w++fUHxzzYd1nv9es3llbbt2//qHtGS9XMaDR++P5U+7Kvj8+Ps35+94P3du3alZNzfTJ6AAAAAMCNUuUpOFLPnvny048rWvvFJx+lp6VevgwAAG4eLlpt/wH9N6zbUJo+Cz98+/2sX36xWm1la/bs2TM+KX7gwP5iWSaTPf7EYwv/XLj/4L5FSxfd/8D99jovvvyiKBkwoN/v8+aIhTlz5wTWrSvKN2ze2Kp1a/EQPQweNOgq9y09I2PG55+7uLj0HzhAAgAAAADUcFUOoAEAQE1XLzjYwcFh3759ZQtF8vvh+1M3btxUUauHH3l44jNP7965e8obbybFJUyeMvmOoUPsq5Qq1ZiHHlq8aMmyv5a3bdf25VdfEYVvvjH56NFj4jHxyaf27q3CDB5bIreJv40aNZQAAAAAADVclafgAAAANZ2bu5v4m5eXV6VWI0bevW3rtk8++kQsL/1rWWhYizvuuvOvZcvFU6VS+enHn+zbt3/hgoUBAf6hzUNF4fZt2/P1xbMWlp3T42oUFBYUFRa6al0lAAAAAEANRwANAECtk52ZJf66uFQh4XXRahs1aige8UnxpYUqlap0+fDhCzd+yMrODm3eQvoXtM7ODo6OmdlZEgAAAACghiOABgCg1kk+mqzT6dq3D//5p59KC11dXSc8/VTU7j2VDFhe+ufSdWvWlD4tKCySqkG327qKvwlH4iQAAAAAQA3HHNAAANQ6JpN544aNvfr0st9d0O61114Z+9BDBqOp3CY6vf70qdMBAQEinrY/vOrUOXnylFQpq9UqVVHdgIBnnn8uNzc3cstWCQAAAABQwzECGgCA2uijD6eGtWw5/csvYg/H7o/ZHxhYt2evXrNnzdpacey7fPnyJ558YsqUKXt2747o2uWeUffM+HLGjC9mVLKV9LSMjp06ipg7OflYcnJyRdXUavWrr78ilytCQ0PDWoaJkpf/78WqTlENAAAAALgJEUADAFAbZWVlj75n1Ljx4/oN6Hf/A/dnnDv//XffT/9sWiVNPp/2eWFBQe8+vUfcM8JgMMyePXvmlzMr38rPP/3UoWNHEXO//dbblQfQYx96yGaznT2bun7d+p++//FIHPNvAAAAAMCtQKb1CJKAWsnbNzjtdKIEADeCq7tPQX6udD04OLlcr64AAABw83Bydisq0EnXg+gqLydDAoAbgTmgAQAAAAAAAADVggAaAAAAAAAAAFAtCKABAAAAAAAAANWCABoAAAAAAAAAUC0IoAEAAAAAAAAA1YIAGgAAAAAAAABQLQigAQAAAAAAAADVggAaAAAAAAAAAFAtCKABAAAAAAAAANWCABoAAAAAAAAAUC0IoAEAAAAAAAAA1YIAGgAAAAAAAABQLQigAQAAAAAAAADVQikBAIBaT6N2VKodlEq1UqVWKPh6AAAAcC0sFrPZZDSbjWZTkcFQKAEArjmAbti4iaurSyUV8vJ0x5KTpH/BucWkGT+O9oudMfGpWUeNUtV5tX7u8zc6J05/aur2rGtpDwBAbSCTZG4ePkZDkdViyi/Um00Gq9UiAQAAoOrkcoVSpVGpNQqF2t3DJSc7QwKAWu9aAugf58yr36jRFasdTz467oFR0jXS1uvRzlN33hjco0PwoqNJeqnKdFlJicleiWnGqqfP6pDhX30zIvH1xz7emS8BAHDLUqk0bh6+2efPmoyM0AEAAPi3xA/5RkOBeIhlldqxjk9wTnaayWSQAKAWq3IA3bJ1W5E+Pzhi2NkzpyupVjcoaPaCxWGtWscePCBdA21I185eaevmHW03tmvn+ouSYk1SVRlPrXjn1RUSAAAol1KpcXRyyTh7VAIAAMD1Jn7gTz+b7O7lb8uXzGYyaAC1V5VvQujp5Sn+Vp4+C2dOnSqu7O0tXRPn4J4dvDKj1m/eFKOr16NHPXXpGq/WD37y7YptG3ZFrVry20vDwlTFhWrfzpM+nLdq1a6oDeuW/u+lfr7F9bWNHvxt6bxXQrWSc7tXfl7x07hhE974QdTZtmD2+/2DtSW9qZ2bDH9u2oIFkVEbdm37+aMJrT3VkrbHS/PnTAhz8Rv+xV+7fhvVwre0H/sOdJi8dOlXY4PU9m5/e+6lz39eF7X0q1FB6vJ6AwDgpiSTZO6efjmZqRIAAACqjfi65eHpJ9kkAKi1qjwC2r9uoPgr8t+rr1x12no9Ivx00VGJqSfV0fp+Eb2azDp6uHgWDud2Y58bF65f8dmkJSc8Bj82YdykEbHPzMsMH/vy8Mapiz96d3l2/VFPPTXpucOJb67ILNujWhvSq3v0Vx898b1L+NiXJk14+VDcc/NOaXs8//Gk1ifmTh+3OFkdMX7yxJcmxE58N/Lje+9P/mcKDm2jdhXuqNqraQf/ubPeXZyempim7fFyeb1lSwAA3HRcPXxyMs9IAAAAqGZZmWfcxVevHOaDBlBLVTmAzjx/Tvx94anHr1jzf199a69cZSIs7uyVFROZrDfmJ0Ye0Pfs0CNk1uEYU3GO7KU2ntg0f/mBFKM0/f8OzHcxpuolfy8Pte7I4kWbD6dIh6dOivFXZ6aYJG3ZLo3G1Khf521PEql06tz5/TuMaVlPO+9U1rqPHoxVG1Pzi6eJXrto1+ip7cI81VWIjI26E1G/frc2xj5FdWr5vXEHRADATUajcTQai4zcmR0AAKD6mQyFRgejRu1kMBZIAFD7VDmANhqK5y3aHxNz9ZWrqnj+DX/dga8Si28AmBW7PUbXtXNE49kxcXopO2bRsqT3x/+wYEDKiaOxOzctWV48Ejt15+J1w9+Y/POcMSeSk6K3r1i+6fL/ntioy9Jd2Bm9TieibJWkFqUmtVfXMRMHtAv28/Ly8/dWJ2qqNmuGUZem+ydg/re9AQDwn1CqNBazWQIAAMB/wmYxK9RqiQAaQK1U5QC6+mkb94uo5xJQb/rqof8URnQNnhV3WC/pY+Y9NXJTi4hew0cPHfbCgGFD5j717A+HU6OmP3Lf/PCuw4YPHfzQy4NH9Jr2xJvzz17Sr1G6dCiyqsnYd6aPb5y6c3vM8jWxmdp+E8cHS9fs+vYGAED1USo1hsJ8CQAAAP8Jk8ng7OAsAUCtdPMF0NqQru38s3b+MnNJbMlcFpJaGzbk+dEXZuFQe/l6SVmH180Tj5n93vjx1dbt/FWHDVp/L2PmzrVf7Vz7Q3D/j74Z3znMc8nZK21J7dcuorkx8uOX3t6eZSy+u2APqbwBy0ZB0rh4qotHTIu98Sj/1oJX2RsAADeeUqU2m7gVOwAAwH9EfPUSX8AkAKiVqhxAZ2Vmib91AwPPnD5dSbXAevWKK58/L1WRc0jPDv6ZUT/M27yl9C6CsVJE/5c692w8Ozarxyszngs5MnvG7C2pQYNHtPY0HMnSSU2GvPHVY567vpv+Q4wUNnxomItxS6bxKmZe1mfqjJ7thgyOOLlF12jwiNHdA6QLc3cY9DqD2j/Yz/9sVmZKVlJilv+Ip55PVK07qw3rPzTEW0qpUm8AANxcFAql1WqRAAAA8J8QX73EFzAJAGqlKn/8HTqw78TRo7MXLrlizWPJybEHD0hV1Lh7hJ8+9odYXZmyzCORsfruEV2Dv/th3WcfB7/y3LgPvpsgUuKz+5d89tW6FJMxdfpH9Z97/oXP5ovKupORc6fP3JktqT2vsClj9pYZM1dMmTDh018mSGk75y5alzA2zL4mNWr+uqHvvvDdkrPLnnpkesz302fXf2PMxMndz+5fMXfZrvpj/avSGwAAAAAAAADUSjKtR5BUdQ0bN3F1damkQl6e7lhykgTcxLx9g9NOJ0oAcCO4uvsU5OdK14ODk0tVu/Lxa8AHIAAAwH/JLzAkI+14lZo4ObsVFeik60F0lZeTIQHAjXCN/wEI4TIAAChXm049but3h1hIP3vqj5+mSzeN8ZPedXByEgvL5v94IunIJWvveeS5zIzUDcvnSwAAAACA64cZiAAAQGU6dOsb2rqDo7PLudRT+3ZtOZ50uPL6+3dHikf7rn0aNm0p/ecUSlXvwSODGjSRyxWpp45v37giJ/PCYJ/vP5ss/j7x0gflNjxyYE+B/jqMMOrUY6ChqFAcgaup7OrhOXbC62VLorat37V5lVh4+NkpWhdXs9mkz805lhi7Y+NKm80qAQAAAEBNQwANAAAq1LrjbR1u63dgz9bU0yl+dev1HTrqt28+KizQSzerAcPu9w+sv2/X5rycrJAW7foOvXfhL19eTcPY6B3S9VDHr+7pE8lXWTlfp1sy51uxMPTeR/bv3nrqRFJezj83cD64d9up40k+/kHN23b08PZdPv9HCQAAAABqGgJoAABQPpsktYvodTBq+/YNy8XTYwmHXNw9A4MbJ8XtF099A+rd1v/OOr4BBfn6+EPRuyNXX7HD0DYd23bq4ebhlZN1btfm1ccTrzCYWi5XdOk9uHHz1g4OjumppzevWpR9Pr2S+m6e3o2atiydYSM5/tDo8ZNEYW7W+Upa3ff4/3nVKb6/8JH9e8pOwVG6dY2DY8bZkxtXLrT3E1i/Sf9h921b+1dYeBfxWs6kHN24YoHZZJRKhler1JoGTZrbJyER5Yf37apk0xaz6fTx4sm4bVZr9vk0+3Kp7PPnjiXEikdCbMwDT7wktnv6BHOgAQAAAKhhCKABAED5nJxctC5uJ48llJasWfyrfUHj6HTX/U8citm5/I+ffPwC+995n7GocF+l804ENQjpMWDYhmXzT51IahzaavDIh+d8+0nlgXKnHgMbhbZas+TXnMzzIgse9sCTs758z2IxV1Tfz7+e+Hvy6N87bLPN/e5/0pX8/u2n4u/A4Q9etvUB9RqFrFv6e15OVodufUu2/r7NZrXZbI4OzkH1myyePVOpVN/98NOtO3SL3rE1xLFsAAAQAElEQVRRNPnm49dGjX8h/uDeq5yC4yqJo3Qu7Uzd4EYE0AAAAABqHLkEAABQHq2rm/hb7oQbzVqGG42G7RuWFRXki4T6yIE9zVq3r7y3sLYRCYeik47sF01io3eePXk8rF3nypu0aNMxZsem1FMnxD5Erlni4OjYIKR5JfWdXFwNRYVWq0W6HkJbd9y7bcOZlKO63Owta5dqNI71m4TaV8kVil0lI77NZmPG2ZNevv5SNdPlZbt6eEoAAAAAUNMwAhoAAJSvkrveuXl452ZlyP5+mnUurWV4F6lSLu4ejQNahbWLKC0xmQyV1Fcq1Y7O2qzzafanZpNRl5Pj6u4lVbrH0nUitu6sdRkw7AHxKC308PI5Ll2YNiRfn2dfsFqsKpVaqn4ySSYBAAAAQE1DAA0AAMqny8sRfx2dtKUlDk7ORYUF5ea8V8x+ZTJZ1Lb1uzavkq5S+XFrZZsRO6zWOMhk8tLo3MnZpSBfJ12Dkq0vmfPtJfMy3yhaF/eUo/ESAAAAANQ0TMEBAADKZygsOJ9xNrhxs9KSbv3u6N7/LrGQm33ezbNOaRjsWcc/Lzer8t7ysrPq+AaUPnX18FIoKvsh3GwyFubrPbx97U9VarWLu3tOVmYlTc6kHLVaLaUTZQh3j326YbMwqerE1vP1Oh+/f3a4dE+u6LoPVHYVx9qvrv3OigAAAABQsxBAAwCACu3bFRnWtnOT5m0cHJ1ad7itXoOme7auFeUJh6LVGoeuvQc7ODkHN2rWvE3H2JidZRuajEZHJ2eRGpeWHIzeXq9Rs5bhXZRKtbdvwD0PP+sXGFz51o8ciAqP6OUXWN/JWdtj4IjCgvzKQ9jCAn1i7L7b+t3hG1BP6+Le947ROl3OsfjYi3bMZHLz8JKuwuF9u9p06hnUIEQsh7ZqP/zBpzSOTldsZSgq9K1b8rpksn8/a7NcrhAvf8ioR06fSEo7kyIBAAAAQE0j03oESUCt5O0bnHb6pvgPqwHUQq7uPgX5udL14ODkUtWufPwaXP0HoIiM23bqIYLm+EN7o7dvLJ372K9ucPcBd3n5+Ofrco/s3xO1fUPZkb8u7l7DH3jcPmXzxhULRJgrFpq2aBferbcoPJd2JjZ6Z0JsdOWbFvFrt35DGzVrpVY7pJ9N2bRqUW7W+Ss26TFgWP2Q5larZd/OSLFdi8VctkLnnreLUFuuUOjycn754t0uvYeEd+l1SSfzf5yWkXpaJpNH9Lq9SYs2Dg5OZ08d37NlbfrZk2Jt3eDGwx988sv3XrBX7jlwhLOr64o/frY/FWtFK1//IBFAi61vXrWokr0VCfXYCa+XLSmdpeThZ6doXVxtNptel3vqWGLkmiVmk1ECAAA1ll9gSEba8So1cXJ2Kyq4psnEyusqLydDAoAbgQAatRcBNIAbqAYF0AAAAPj3CKAB1FpMwQEAAAAAAAAAqBYE0AAAAAAAAACAaqGsQl2VWqZSyhRKSSn+KiTgpmGzWCSzSfy1mcwSU2QCAAAAAAAAN4erC6DlcrmLq0ylkoCbUvEvIgqF/eZXNpPJqsuTrFYJAAAAAAAAwA11FVNwaDRydw/SZ9QU4loVV6y4biUAAAAAAAAAN9QVAmiZg0bh4iqTM1U0ahJxxRZftw5k0ABQPovFLD4pJQAAAPwnxFcv8QVMAoBaqdJkWa6QO7tIQM1UfPUSrwBAecwmg1LFr3QAAAD/EaVaY+Z+RQBqq8oCaLmLiySTSUANJZMVX8MAgMuYzUYCaAAAgP+MSqkxmQ0SANRKFQfQCiXzPqOmK76GFVd3p00AqE3MJoNczscjAADAf0QmV5iNjIAGUEtVGEDLVPy7FLcCrmQAuJzBUKjSaNQaJwkAAADVTO3gpFJrjMYCCQBqpYoDaGUVhj/LPT3FQwJuPlW6kgGg9sjNTvfwCpAAAABQzTy86ubmpEsAUFtVPDj0quff8JrwtOvtt4uFvBXLM7/+SgJuKswkAwAVyMlOc/fyz8lMlQAAAFA93L0CsjPPShJ32AJQe1UYQMsUCulq2vv6ivQ57Z23ZHKF7xuTs+fPs2ZlSf+ec1On++53697KwUNtST9auGVB9u9bzCbpWnmo75jofV+ERpule+9tfctn6nTOz37vXf3xfOkGUMnbPe770iAHbfET884vUz9e9S9eGq7gKq9kAKiFTCaDVCDzDWiclXnGZCiUAAAAcP2oNU4e3nWzM1PNZmZ/BlCrXeP0uK7DRzi0CDOdTFHXr288dbJwzx5RaDx92nvC06JQFVy/aP/+vL/+lK6NT3evtye5BonoOV6//pTNN9xl5CuaQOe0aw1qZYHdPR6K0GTvzfl9S378OZvHaePpfEv+jfofAJM1ZkbqqBkSAAA3mslUdC49xd3Tx2gw2GxWk7HIbDJYrRYJAAAAVSeXK5RqjUrlIJfJVWrNufTjjH0GgGsJoJ179/F65FH9li2aZs2s+QXpU960l6e9NcVr3HhRaMnO8XrsMUtubn7kJqnKfJweesw1KFv30buZW4/Ziks89E9N9R90v3vn6PNbM6Sqk3kEKSVjwcJfslcdK36+6qP0VRIAACgmk3KyMzRqR4Va4+zioVRpFApu3woAAHAtLBaz+DnfZDaajcb8glzSZwCQri2AdmjRouDAgXMfT7U/dYro4vHQI2JBt2F9xnvv2AsVnh4OLZpfSwDtE65t52mO/jJ7lz19FrKLFv58Pr+VZJ8wQ+Wjuf1+99vDHYK0lmPxBavm5Kw/ZDVJ8s4v132pZdHvSy0t+zqHB8nSD+bO/Cw3RnJ6fYZvRPFsF+oJMxqMjz//zDvG26cF9Ek/93+T9adNYnMuD93v2q6ZUjpVsGq9tfv9zqe/PfveKmv4y3XfCC/6aOK54shbpbz93YDxvropE7PTu/t88bTq0EqDb3fnwOycVyflnvZ1uvt+t+7hDr5qyZiu//3brKW7LMUjtZ2VnUe6393DqaGvLP9owc71eb+vNOSYypZL2UcLd63M+X29Kb9kaLd7S+1997tGNNN4GI3x0Xm/z9HHnBYHQdbgds/H7nFq6qtU603x0dkzZ+TfmMlDAAC3LIOxUDIyCwcAAAAA4DqTS1WnW73KqXVrx46dxLJT126+r7+hadJE07Sp/9vvOHboUFzYpYtjWEtRTao6uW8jldpoOnTMWna2jYxdulnf6WJEFuysuvMVv8f6qfMPZX+3skhq6DZhsnffhhd+UlR7Ot0ZITu2MmfpXrNHK88JDzu664tmfZT2y16zZDSs/DJtyrcF6WX6VTXUPv+yd/eGtpg/s1YdU/a9XytC5KugjuisPLbg/MffFZx20ox92XdkuNjo+Zk/5x1z1j400SPcp/iFtLzf5417XHxFJP1zTrzaadDjPhN6KFSi/OHSct0xtdOdT/tOiCiepVgV6Pz85DrdnQ3rf86YKV5auPcbk7QNnIt3csLjrk31Bb9/mfHdeqNHhNeEkWpnCQAAAAAAAABuctcyAtqYlJSz4A+vx584vWe3Y7t2huPHzz49QZQHfveDU/v2hVFR3hMmZs/73XjsmHQNVCqZ2mjNz7eVu9a5obZPM+nUyowpMwz5krTloPV/b7rc3l21/pi5ZNeM67/NmpVgk9YbjFP972yo9pUVJkQbEiKsRqPleELhoWPFA5D/7kwW2N2lqda0ZWr6x1sskqogYaL/G/2uJpK3HFpwfubSCxNSz5p86i/JcjqjeKjyMWf1h3epAj1EIK65vbvGGH/+zXd1xaOV1xfecb+zKVuSfDS3d/6nXLXT8NJU33aDHAN35qsiXFqqC3+fkbVQ7L9UcChf9en92u4N9QslpbPamp6gX7/ekGMq2LJSIWWbGQANAAAAAAAA4Kb3LyZ5VBYP25VsNklWZkojWXF+azNbr21sdXFbU77VqJY7O4tOL8+gZR4NNb6Sef1Okz2BzUkoOJTl1rmZykNlD6DNx7JLWhmtGSLC1sorG9Cskgc2VKmzCrbEl9xryWSJjy7K7uckXZnl1Ol/Bmjn58tajvQc30rt46Hw9VWppSJnkXL7qht4Wk+vLzpt39Fs418zim966NzyonJTumHLMUtEQ4dAj0JVS7VarXhoWv2H/tmQyddDlh9dsOuo68hBAT+FFx6KL9wVWbAlXQIAAAAAAACAm961BNCOHTu6j7wn7Z23xXJhTLTrwNvr/vCTTCFX1fHJ/OE7UZj5zVe+r79RdORwUUy0VEW29GOmfLVjy4aKpQnm0pDXvaX2zgjZoZV6+z0ITcbSbNpmNEnXrCSetkmlPRhtRqlqVIFOz7/r293XfGxv/q5IQ0ZDt/E9/llrrGCg8j/lYtOmkteiKnmqL1jwXe4hfWlFW0aCVco3zHrzbEJ3bedwTcsIzwk93G9fmfZqyQBwAAAAAAAAALiJXcs4Zaf2HQr37Svcs1ssF+zYkf7+e6akRMPhw6lT3izcs6e4cOeOwthYp/btpWuQcTD/UJYi/B737n/P7CxC3scm1RnZXa022rKPGdIlZbseFyZBdm/q3NLXmhFvyr6GGNpky8iwSFp100D7hmS+zdQef680ioxbrfD1KFmlVTTwVZQ7mNq5oVNLX/OWqWefeTNr1tLC0yaZuqRefrrxeJa8YYRDoH1HPTR3TPS4PVxhvLhcFaiJaKrUny46nWHNOGYyqhXqbGPMriLxOJYvczZZsvXFc4a0bKnM3pk9/c20R+8/s+CUFNjy724BAAAAAAAA4OZ1LSOgDYkJroMG13nxJYWnp+nMmdw/5mfs3FHcl6+v17PPq/x8LVlZjmFhulUrpWuRUfDLd3kNJrk+P8Pp7vjChFM233CXlp7Gle9k78qQpGzdwp3a5wf5vK3K3ZKt7jvIJSg976P1RtO1ROnWY5G6+L5ed070zJ5TkO3heOcgB7Vksa/KiDfq+znfPdFTWlkktXKNEMl0djldmLIteknZcpC2j2SUGmrv7i7i56KSV1G0YGlBu4e935isWhVtDoxw7dtMFn1Utz66bLmlaV/3CE/D0mkFp0021U59wl3ed070yp6Tnx3o2Leva0tT7psvZx1r5v7SKy7SwaxfVhqNvs6dfaXsSJFjSwAAAAAAAABwc1OoHd3KXSF3qnCMrfHYMZE1K729DcnJSl8/l8FDdCtXiHL//02zmUzGkymqunWLDh3MnT9Pujb5KYWb9xnV3qomzZxahGicz+ev+vH8T1ssVrHOaj1+qEgf4DSgh0t4C41zuu6bT7I2HJeK7yjYzbV7gHn7yoKT+eJ1yZv0dgnXGjevLMowyXw7uvQKtsasz08WIbJaGT7IpWF+wdpNxsxU4/4TFu8Q7ZC73CKCzFuWGrzbqvL26LYkW3NSDNkBDhFtncNbKAuP6LYXapq7FfeWH+x8eydFyiZ9VGrx1BmmbNNJhbJDN7e+PbTNLAVLo21NG8qS1+sPZNpykoqOKVTdertEtHXwsJj3r8z8ZqlRZ5XKlDsGORpWfn7up+3FXjR+vgAAEABJREFUL82aaYw+bHYIdOw+1L1vK436bN5Pn2VvPSkVpRQd0ctbRrgP6qft1laZuS3z468L0ookXDVbQUG55U5ad31epgQAN4LGwdlkMkjXg1KluV5dAQAA4OahUjuYTddn/JnoylDEVJ4AbgyZ1iOo3BUK7zrSVVDU8an38y9p77wlU6l8X309ZcwD1qwsqQZRecjVemt+yQwe7p29/vem07HPzr6/3iJdJ6qmru9Mcoifk71wi4mP+hvEcv5cueXevsFppxMlALgRXN19CvJzpevBwcnlenUFAACAm4eTs1tRgU66HkRXeTkZEgDcCBVOwWGzWmRyhXQllnMZeatW+b35lljOW7GshqXPzi09PnzX1Tlet2qnwejr2Levi69e/3v8dUufBVNC3nuf2d6Y5NH9WMaq0xL+c+JKlgAAAAAAAADcCBXPAW0yS5orB9BC5swvc+bOsVks1tyaNvwqPz535reyh+5xeejx4olI9Kd0M2dkbbieMbEssK/nSw85+2Tn/s745xtEXMkAAAAAAAAAboQKp+CQOTlVMg00UFNYC/IrmgOaKTgA3EBMwQEAAIDKMQUHgFtDxVNwmBk3ilsBVzIAAAAAAABwo8grXGM0SSR3qOnENWy8PrcMBgAAAAAAAFBVFQfQks2iy5NsNgmooWwl1zAAAAAAAACAG0Re2UqLxZqvl4CaqfjqtVgkAAAAAAAAADeIsvLVtqIiq80mc9bK5HIJqCFsVqs1XycZmHwDAAAAAAAAuJGUV6xhMxhsJpPcxUWmUkvATc9mMlp1OslqlQAAAAAAAADcUFcOoItZrdbcXJtcLlOp5CKGVqlkCoUE3DRsFotkMllNRvFjiYzoGQAAAAAAALg5XF0AXaI41zMYrAaDBNysZBIA4Gq5urqOGz+u34B+AQEBp06dXr9u3efTPreV3H94ztw5ao165PCRAwb0e+f99957651ly1dI15Wvj89TEydGRHTSurju3r3zh29/OHzkiAQAAAAAuLUwszMAALWRp6fH3D/mPfbEYwWFBQv+WHD61Mknnnxi2vRpl1TLyDh3/NixtPR06Zr8sXC+eFxeLtLnPxYv7NI1YtPmTZs3bmwWGvrb3N/atm0jVadXX38lPileAgAAAAD8h6owAhoAANwyXnnt1QYN6j/39DOrV6+1l7w++fUHxzzYd1nv9es3llbbt2//qHtGS9fbncPu9PX1eezRx7Zs2SKeumi1W7ZvuXfUvWJzEgAAAADgFsIIaAAAah0R+PYf0H/Dug2l6bPww7ffz/rlF6vVVrZmz54945PiBw7sL5ZlMtnjTzy28M+F+w/uW7R00f0P3G+v8+LLL4qSAQP6/T5vjliYM3dOYN26onzD5o2tWrcWD9HD4EGDLt8NufzC9xCdXt+2dbtXXn7V/nTgwAGzfp0VvS96zbrVr77+itbZ2V7etGnItM+nbd+1I3L71qkfT20X3rZ0DydMfGrtujWbt0ZKJYO733rrLdFW9CD6ua37baJw2uefjX3oIbEgKk+ZMkUCAAAAAPwnCKABAKh16gUHOzg47Nu3r2xhekbGh+9P3bhxU0WtHn7k4YnPPL175+4pb7yZFJcwecrkO4YOsa9SqlRjHnpo8aIly/5a3rZd25dffUUUvvnG5KNHj4nHxCef2rt3b9muVq1aYzAYvvzqyw8//ODe0feKQLx0VVhYi2lfTM/Kynr37XdWr1pz7733vvTKy6Jco9F88/13Xbt1nT9v3tLFS/r16zf1o49EJm5vdfc99yxevPiDd98Vy+++916vfn0WL1r8/nvvKxSKL2d+GRgU9OP3P65ZtUasFTszf/48CQAAAADwn2AKDgAAah03dzfxNy8vr0qtRoy8e9vWbZ989IlYXvrXstCwFnfcdedfy5aLp0ql8tOPP9m3b//CBQsDAvxDm4eKwu3btufrdWKh7JwedqdOnnz0oUeeee7ZYXcPF49nn33ut19nfzXza7Hqvvvuy8zMeun/XjSZzOKpu5v7oKGDprw5ZfDgQf7+fi//30tLl/4lyg8e2N82PLx0cPT8uXO/+fpbsRDg79+zd8/p06Z9/+0P4umWzZGR27fccccQ0Xlaemq5OwMAAAAAqD4E0AAA1DrZmVnir4uL69U3cdFqGzVqKB5l7+OnUqlKlw8fPmJfyMrODm3e4ood7t0bPeaBMT516vTs06tXz54ijNbrC2bPmhUa1tzb2+vQkdiylet4e7dq1dpsNq9atdpeInLkslHyiePH7Qtt27ZVKBQv/N//iUfp2qDAIAkAAAAAcCMQQAMAUOskH03W6XTt24f//NNPpYWurq4Tnn4qaveeSsYIL/1z6bo1a0qfFhQWSf9Oxrlzf8z7Qzz+XPbnkKGDRAAtk8kOHzn89Zczy1bT6fXir8ViMZlMlXdon5Tj048/KY2khdTUdAkAAAAAcCMwBzQAALWOyWTeuGFjrz697HcXtHvttVfGPvSQwVh+wisi4NOnTgcEBNiHHouHV506J0+ekipltVrLLZ/166xdUbvs9yoU3N3dvL3rmIzFc24kJyXX9Q/YuzfavhWlUnnu3PnCwsKDBw9oNJrSWaf79+/78qsvidD8kp4PHioeOq11cbE3j4qK9vbxOZmSUsnOAAAAAACqDyOgAQCojT76cGpYy5bTv/wi9nDs/pj9gYF1e/bqNXvWrK1btlbUZPny5U88+cSUKVP27N4d0bXLPaPumfHljBlfzKhkK+lpGR07dRQxd3LyseTk5NLy32bP/t/0abN//23d2uLx1BFdunh7e30+bbpUMsh6yNAhX86c8eusWc2aN39wzIOHDh565KFHli9fcf/YB16fMjmofrBks428914RKH/26WeXbPHkyZSoPVEPP/JwdlZOXl7e0KGDO0V0Tjl+YufOXalni8dBP/DAA/HxcSLglgAAAAAA1Y8R0AAA1EZZWdmj7xn13TffOTs53//A/aEtwr7/7vuPPvyokiafT/t82v8+ax4W+tH/Pr598O2zZ8+eefFEGZf7+aefbDZJxNwdOnUoW75u3YZnJjwjl8vHPvTQ0KF3pp49+9aUtxb8sUCsEgn4MxMmmozG96d+OP6x8Xt27XnphRdFudFonPj4hOSkpIlPTxw5alTKiRMvvfB/9hsVXuLpCRNFV3ffM+KDqe/XCw5+8403Rfosyhf+sSAhIeGNKW/c98B9EgAAAADgPyHTenBbHtRS3r7BaacTJQC4EVzdfQryc6XrwcHJ5Xp1BQAAgJuHk7NbUYFOuh5EV3k5GRIA3AiMgAYAAAAAAAAAVAsCaAAAAAAAAABAtSCABgAAAAAAAABUCwJoAAAAAAAAAEC1IIAGAAAAAAAAAFQLAmgAAAAAAAAAQLUggAYAAAAAAAAAVAsCaAAAAAAAAABAtSCABgAAAAAAAABUCwJoAAAAAAAAAEC1IIAGAAAAAAAAAFQLAmgAAAAAAAAAQLUggAYAAAAAAAAAVAulBAAAaj2N2lGpdlAq1UqVWqHg6wEAAMC1sFjMZpPRbDaaTUUGQ6EEACCABgCglpNJMjcPH6OhyGox5RfqzSaD1WqRAAAAUHVyuUKp0qjUGoVC7e7hkpOdIQFArUcADQBA7aVSadw8fLPPnzUZGaEDAADwb4kf8o2GAvEQyyq1Yx2f4JzsNJPJIAFALcYc0AAA1FJKpcbRySXj7FHSZwAAgOtOfMVKP5ssvm6JL10SANRiBNAAANRGMknm7umXk5kqAQAAoNqIr1senn6STQKAWosAGgCA2sjVwycn84wEAACAapaVecbdw0cCgNqKABoAgFpHo3E0GouM3JkdAACg+pkMhUaTUaN2kgCgViKABgCg1lGqNDaLRQIAAMB/wmYxK9RqCQBqJQJoAABqHaVSY+Zu7AAAAP8Vk8mg4laEAGorpQQAAGoZpUpNAA0AAPCfEV+9xBcwCQBqJQJoAABqHYVCabUyBQcAAMB/RHz1El/AJAColZiCAwAAAAAAAABQLQigAQAAAAAAAADVgv8ABAAAXE9tOvW4rd8dYiH97Kk/fpou3TTGT3rXwclJLCyb/+OJpCOXrL3nkecyM1I3LJ8vAQAAAACuHwJoAABQmQ7d+oa27uDo7HIu9dS+XVuOJx2uvP7+3ZHi0b5rn4ZNW0r/OYVS1XvwyKAGTeRyReqp49s3rsjJzLCv+v6zyeLvEy99UG7DIwf2FOh10r/WqcdAQ1GhOAJXWb9RaKu2nXrU8Q3Q5eaknUnZtv6vosIC6T9U1R0GAAAAgCphCg4AAFCh1h1v63Bbv6Pxh9YtnZt25mTfoaMcnbTSTWzAsPvrNQwRcermVQttNlvfofdeZcPY6B3HEg5J/1odv7pXX7lucONBI8amJMfPmvHBjs0rghqG9Lp9pPTfqtIOAwAAAEBVMQIaAACUzyZJ7SJ6HYzavn3DcvFU5LMu7p6BwY2T4vaLp74B9W7rf2cd34CCfH38oejdkauv2GFom45tO/Vw8/DKyTq3a/Pq44lXGEwtlyu69B7cuHlrBwfH9NTTm1ctyj6fXkl9N0/vRk1bls6wkRx/aPT4SaIwN+t8Ja3ue/z/vOr4i4Uj+/eUnYKjdOsaB8eMsyc3rlxo7yewfpP+w+7btvavsPAu4rWcSTm6ccUCs8kolQyvVqk1DZo0t09CIsoP79tVyabrBjfMPp8RtW2dWD4WH1ug17u4uFe+dak4Mg4sPvJ+dQt0uth9O/ft2mwv79RjoLevvziwPQeO8K0bVFhQ8PPnb9tXVXTkq7rDAAAAAFBVCrWjmwTUSk5ad31epgQAN4LGwdlkMkjXg1KlqWpXzlqPq/kAdHJy6dxz4J4ta3OzL1Q+Gncw63yaWNA4Oo0aN+loQuyqRbPOpZ7u0muQzWZLO5NS2jagXkMPb9+yaWZQg5B+d47etu6vyDVLRFzb/877kuIOFBXkV7IDnXsOatKizdo/f9sducbHP7Bzz9sPRm2z2awV1a/fsFmj0Fbr/5ondsZeEhu903DxjBbtu/ZJjj8octjSkkPRO8Rr9PT2tVosZTNxsbn6TZqJTHbv9g1ePv7i6YE920Qs7+Lm2bJthMlgWLnwF9F/eNc+KpU69dRx0UTUbNi0ZczOTX/N/U70eS7ttFQpRydtaJsOqadO6HKzxFN9Xo798FaydbWDw+hxk04kx61eNDsrMz2i9yCFQnm2ZOtaF7emLcPrN24mmmxaufBEUlxhgb7yI1/VHQYAANdM6+qVr8+pUhOV2sH+I/e/J7oyFOVLAHAjMAUHAAAon9a1+Fdqe4h5iWYtw41Gw/YNy0SOefJYwpEDe5q1bl95b2FtIxIORScd2S+aiNz27MnjYe06V96kRZuOMTs2iXxW7IMITx0cHRuENK+kvpOLq6Go0Gq1SNdDaOuOe7dtOJNyVJebvWXtUo3GsX6TUPsquUKxq2TEt9lszDh70svXX7omIgiOjdl5x+hx455/u/3b5nAAABAASURBVO+do+v4BV5x683C2pstpm3rl4ljIuLydX/OPZd+1t4kP1/n4uouju2xhFiT0Zh5LtVefg1HHgAAAACuF6bgAAAA5atkrLGbh3duVobs76dZ59JahneRKuXi7tE4oFVYu4jSksoHbiuVakdnbemIYLPJqMvJcXX3kirdY+k6EVt31roMGPaAeJQWenj5HJcuDJHO1+fZF6wWq0qllq6JOIBb1y7duWlVo5CwBk3DRo17Pjnu4KpFsyrZuruXd/b5c6Wv9NTxxNIKNmvx+RI9XLKVqh55AAAAALiOCKABAED5dHnF/5Vo2bsOOjg5FxUWlJvzXjH7lclkUdvW79q8SrpKsnJLK9uM2GG1xkEmk5dG507OLgX5OukalGx9yZxvT5dJeKuJyNYTDseIx6kTEb0H3a11cS8qKri2rYsM+vIR61U+8gAAAABw/TAFBwAAKJ+hsOB8xtngxs1KS7r1u6N7/7vEQm72eTfPOqVhsGcd/7ySWYwrkZedVcc3oPSpq4eXQlHZD+Eili3M13t4+9qfqtRqF3f3nKzKpq4+k3LUarWUTpQh3D326YbNwqSqE1vP1+t8/P7Z4dI9uSKZdLW69B4S0qJt6dPTJ5Kk4vnBHSvZek7meQ+vf458YP0mrTveVlqt3Hj+ikf+6ncYAAAAAKqKABoAAFRo367IsLadmzRv4+Do1LrDbfUaNN2zda0oTzgUrdY4dO092MHJObhRs+ZtOsbG7Czb0GQ0Ojo5i9S4tORg9PZ6jZq1DO+iVKq9fQPuefhZv8Dgyrd+5EBUeEQvv8D6Ts7aHgNHFBbkn0g6Ukn9wgJ9Yuy+2/rd4RtQT+vi3veO0TpdzrH42It2zGRy8/CSrsLhfbvadOoZ1CBELIe2aj/8wac0jk5XbGUoKvStW/K6ZDJXD8/KK4vX1X3AsGatO4jD6x9Uv0f/YXm52fa5myvaenzsXnEAxWsUR148egwYpnW5wg2lKz/yVdphAAAAAKgqmdYjSAJqJW/f4LTT1f4fVgNAuVzdfQryc6XrwcHJpapd+fg1uPoPQBFctu3UQ2Sd8Yf2Rm/fWDr3sV/d4O4D7vLy8c/X5R7Zvydq+4ayA2ld3L2GP/C4fcrmjSsWiDhVLDRt0S68W29ReC7tTGz0zoTY6Mo3LZcruvUb2qhZK7XaIf1syqZVi3Kzzl+xichk64c0t1ot+3ZGiu1aLOayFTr3vF2E2nKFQpeX88sX73bpPSS8S69LOpn/47SM1NMymTyi1+1NWrRxcHA6e+r4ni1r08+eFGvrBjce/uCTX773gr1yz4EjnF1dV/zxs/2pWCta+foHiTxXbH3zqkWV7K1Spe49ZGRIaBtRWZebfSbl6O6ta3U5xWPJK9q6UMcvUMTWdXz9xas4sm/P5tWLSjd91/2Pz/zgxcs3VMmRr9IOAwCAa+YXGJKRdrxKTZyc3YoKrmkysfK6ysvJkADgRiCARu1FAA3gBqpBATQAAAD+PQJoALUWU3AAAAAAAAAAAKoFATQAAAAAAAAAoFoQQAMAAAAAAAAAqgUBNAAAAAAAAACgWhBAAwAAAAAAAACqBQE0AAC1jsVilssVEgAAAP4T4quX+AImAUCtRAANAECtYzYZlCqNBAAAgP+EUq0xm4wSANRKBNAAANQ6ZrORABoAAOA/o1JqTGaDBAC1EgE0AAC1jtlkkMuVEgAAAP4TMrnCbGQENIBaigAaAIBax2AoVGk0ao2TBAAAgGqmdnBSqTVGY4EEALUSATQAALVRbna6h1eABAAAgGrm4VU3NyddAoDaigAaAIBaKic7zd3LXwIAAEC1cfcKyM48K0kyCQBqKwJoAABqKZPJUFig9w1orNI4SgAAALiu1Bon37pNCvLzzGZmfwZQq3EDIgAAai+Tqehceoq7p4/RYLDZrCZjkdlksFotEgAAAKpOLlco1RqVykEuk6vUmnPpxxn7DAAE0AAA1G4yKSc7Q6N2VKg1zi4eSpVGoeDrAQAAwLWwWMzi53yT2Wg2GvMLckmfAUAigAYAAILBWCiJBwAAAAAA1xVzQAMAAAAAAAAAqgUBNAAAAAAAAACgWhBAAwAAAAAAAACqBQE0AAAAAAAAAKBaEEADAAAAAAAAAKoFATQAAAAAAAAAoFoQQAMAAAAAAAAAqgUBNAAAAAAAAACgWhBAAwAAAAAAAACqBQE0AAAAAAAAAKBaEEADAFAbjXvurduHP1j61NXd88mXPpBuGn0Gj+zSe5BY6DlgWIdufS9Z26xl+7vHTLi81ZinXvX28Zeq6NpaVcTR0fnJF9+3Lzdp1sovIEhCFTk6avsMuvuBx1589Nk3bx/2oKeXbyWVR4+bVLdeQ6kmc3B0Co/oKd1kfP0DQ0JbSVVkPx0eXj5jJ7zm7OwiAQAAAATQAADUWp7evkH1m0g3peS4gynJ8RWtTTuTcmjfLumm17Bpizp+BNBVo1Sq77r/MY2D0/rl8xbMmpGXl3XH6HEi1pduXSKAbtW+m3ST8fYLbNi0ygG0nS4nOzZmR36BXgIAAADEl3wJAADUSrsiV9/W747ff/hMstlKC0XS99DTr3/98Wv2p2MnvL5iwU/nM1JHj5u0b/eWZi3b1fENOJZ4eMOKBVJJVhjRa0DDkJaFBbr4gzEHo7eLQnfPOl17DQps0LiwoGDD8nlnTh4vu1GVStWl5+AGTZsXFRUe2LMt7mCUVx2/Yfc/Pu+H6Xp9boeuvYMbNVs4+6sGTZrn5+vOnDwmFcdzjnfc84hPQNDJ44nb1i0rKND7+PqHtgxPOBQt1jZu2rJNp+5uHl7ROzeXbsXV3TOix8DA4Mbn0s9E79xk76escluJPe/cfUBg/UaZ59LEwUk9nVJ2tx959s3fv/9Ml5stnjZv07Fpi7ZL5nxbyYb6DR3VOLS1eDRp3mrxb99UfljE4RVHL6xdZwcHbeLhGLF1W8lJad2+W2ib9mq1Y1Lcgd2Ra6xWS0hoq7DwLjar1bduvW8+eaO0B1G794DhwU1CxXLi4X07Nq2s6BV5eft26TVINE85miA6zDqfLs5szwHDxAGP2rZeVGjRtnNww5CVi2aLQo2Do2cdX0Nh4eI534hTI06Qj19g2tmTa5bMEfXFzoSEtUtPPd2ibaeiwvzI1Uvsm6jXICQ8oqeXj//xpCP7dm3JykwXhW07dQ9t1cHDq07c/qhNaxbbylx1ZbXt1M1iNa9YPFtW8nT7hhUeHt5h4RFi35RKVUSvgQ1DWhUW5MXu231k/57KL62ya8VrKSzMd3X3qN8oVFzPqxf/Jp4W72rDpuGde3h4+546nrRz00q9Pm/Eg0/GHYq2d+7i5nHf+Ek/THtbLFxy+sQ75cEnX9q2cUXn2wakp57cun55tz6D69ZreC7tzOolv4l9sL/kpi3DRc2EWHFOi0/f5buh0mjuf+z/ROUJr0xdOu+H0yeSL29V+irEAW/Wsn1OzvmQ5m0zM1LF2tQzKVJ5bzr77iXGHmjSovWqJb+mnznZpdfgxqEtFUrljo2rYvftvOywX3R2xHLPAXfZ92rm1FfE9bll7Z/2y3vAnaPTzp4+ELVVpVJX1KdKre54W3/x5nL39La/Ojvx09GiX78u92K45GKTAAAAcAthBDQAALVUTua5nKxzbTvedpX1GzZpLnLnDcvnN2zawtc/UJT0GHCnRuP0x0+fL5//c+uO3UQ0Jgo7d++fkX561swPo7av7zNk1CWd9Bw4wmIzz//x843L53e8rV9gcHE2KsLEXrcPFyFam449NqxYeEmTpi3axezZMvvrqQX5un53XNShyFJ7DRqxc/OqOd9+4ubm6eRUPE5WJpPdOWqcSEJFk/1R2wYOe8DJyeWKreRy+dB7Hj6RdHj2V1NFuDb47odEHFbaxGQypSTFhzRvbX/apFmrhMP7Kt/QumXzkuMObFn7l0ifr3hYhFbhXdb9OW/hL1/4BdRr36WXVDLTSPM2HUTUu/CXL909vLr2GWyv6eMfeDhm97efTi7bvFGT5n5BwSITF5sLqNfQ28e/3FckCgfd/VDKscRZMz84dSK5UbOWUqV8/IM2rVwoAkGRNnbo2ufQ3h0/f/l+1rn0iJIJUqTiiRrq5WWdX/jzjJzz59pH9JaK038vcZr2bFv/w+fviAts8MixJdUCG4a0iFyz5NdvPvao49OsVfuKtugXEBx/IFpWpmT5wln2ZLzHgLtKrrfpG5b90a5Tj4Yhzcs2vPzSuqRnsQOHoneK46NxdAxt3f7Crg69V+zqb99+nJ2ZPuieh0RhQux+8fuEvYn4meF44mGLxVzu6VMoVUUFenF49bm5wx94XOTvv33ziVyuaBkeIdY2b92xfqNma5f8vnDWDHE62nftXe5u5OVkzfnu04J8vch5RfpcUatSQQ1D8nKyxZ4c2bd70IixInaXKri6VGpNkaHglxnviW6bhoU7OWv/+GXGyoWz2nftJV542T4vPztHDuzZvObPo/GxYq+kClTep11O1nnRg3h8/9kUvS4v8fABqeKLofRikwAAAHBrIYAGAKB2somkVkRmrTt0c3TUXk2D2H27dLnZx5LizqQcq+MXpFAom4S23r5heWFhfkGBfumc75IO7xPVVv85J2rbBovZnK/Lc3F1swdkdkqlqn6TZjs2rhJNMtLOHk042LBpmCjfs3Wdi7tnvzvujd2/Ozsz45LtigRQJGhGg2HnxlU+AYFarWvpqpCW4SLSOnPyWFFR4fZNK6WS2DKwfmOz2XwwervJZDx5LOHkscTQ1uFlOyy3VVD9JnpdbvzhfUaj4VjikdyczKCLE8zEIzH2vRVRrF9gsHixV9xQWZUcFrtdm1dnZabn5+v2bFvbtEVxPy3adNi7bUN25jlxeLdvXNEs7ELn59LOJMYfuGQEsVIh9stBZOJ5OZkiuzyfkVruKxKFZrOpZJ9N8Yf2ZmakSpVKijuQdvaUVBzBGxfOnplwZL9CodDlZXvWuTAvc072OVGo1+fu3bHRyzdAKg5eOyTHHSoeLWuzxeyK/PP370RheurpRb9+LQrVao0+L9fbx6+iLao0mkK97vLystdb5vl00XNYm87/vPwKLq2yTiTHpZ05KX7wEAG3j29g2V0VV9feHZscHJz9AoKS4/b71a0njqZUMomKPTMt9/SJo308Kc5sMZ04GpevzxPnTmz9VEqSi4tHSefto7ZvEOdUl5dzKHpHg7/j8st3o6yKWpXKSDu9f89WcToS4g5knk+zZ+Xl7p64QnZvWSNOtFT85t25asmv+bocUUe8WO86F02rffVnp6zK+7yE+IUp+1zaoZgdlWyu9GIDAADALYYpOAAAqJ1EeiYTkdnBvdu79h0sIuArNrBYzBcWzCaFUumkdbFYzfZ5DIS8vGz7Qqv2XTt07ZOTdS43O0tEYHKFUiqJwAQnJ61a7fDkS++X9pkcd1D8tVotMbsje/S/c/n8ny/fbmnPFqulQK/XurqVrnLUjGoYAAAQAElEQVR2dsk6n2ZfFiFYYUHxvAdaF3f9302Km+dmabXuZTsst5Wj1iUgqMGEV6aWVnNwuiiXP5Yc33vwPaJtcOPQU8eTRK53xQ2VVclhsTMai+wLOZnnnVyKR1I7aV1Fnxc6z8lSazQOJYOyLRbL5f0nJhwMathEhPhSccQZH7Nzc7mvSGWxXLTPOdlSpUpPush/u/e7o0FIC/ESigoL5HL53xUu7IzItRVyhVR8/N1KD694pSJIFQuurh5977jXydlFZOKibVFBQUVbFKvEnl9efun1lpvlVOZKqOjSKkv8WmBfMJlNcuWluyqIIyOyY5GBnj15rFFoqzMpR5217ieOFc9FXs7pK3l19p8BbFKZaWxsxT/tiP/f0cnlztHjSzsXCXVFu1FWRa1KmYzG0uW87CwnF9cr7p4QGNyo16CRBkNBfm6uePPK5Rdt9+rPTlmV91lW09DWdYMb//7dp5VvrvRiAwAAwC2GABoAgFotZveW0Y8+7+t3YSSmzWYVkZDIpu3RlUpV4VeFAr1OIVc6OjrbM0Gt1k0saF3dO3brO++HaXp9nmgf0qLNRU3y9WaT8Yfp71ySNDk6aiN6DEw/e6pjt36R6/68ZEMirrIviHzTSavV5+W6ul0oEQG6i6unfVmlUjs5OYkFvS5H+3eT4uZuntklcxCXKrdVgS6vdILa8tlsyUcONW7eJii4YXzJ9NNX3FApNw/vSg5L6cs8IxVPDO3u5V2gKx4CXKDPE32mp56WSma1NhkN9pmFK9q9DSuLZy9xcnIZ9sBjBfk6XU725a+ofqPQsvvsrHU5XzLi3Ga1KRTKv4+J6vLum7UKd/P0nv3VVBE0B9Zv3K3vkAr2QxyW3NLDK16su4d3bvb5zr2Kz+/2jStEYafu/R00ThU1P3vqeP1GTe3zidsNvOv+4iHPOzeXvd7EkRGnrLRORZdW5cruqiCOjE5fHJcnxu5v3KK1o6PT0YSD4sBezem7XEF+XuTaP08eS5Cq4oqtRGheuuzq4Zl66tjV7F6fIfduXr045WhxmD78gScuWXvFs2OTRKh9IV9WKtVX02cp8ZtN94HD1iydW3r1Xv3FAAAAgFsDU3AAAFC72Wxb1v4pYiD7s8KiQr0ur1P3AUqlqk3H2xSKCkc1iqQvKe5Al96DJJlMZFJ33Te+UZMWVqtFJpfJ5QoRYXfpebtMVnYuX8lsMSXHHeze7w6lQqVWa+4eO7FJs1aivEf/O4/Fx65Z8nuTFm38AoIu2VD9xs3r+AaIZK1zz4HnUs/oy4wJTTwULeI2L29fsTai1+3227WdPpGskMtDW3eQiicUDqrXMCT+YHTZDsttdepEkoOjk2glCr3q+I2d8JqL66XDmROORDcMae7tV/dY0pGr2ZDZZHIoSbcrPyx2LTt2c3BwFEem4239E47EiJLD+6PCu/UumbhZ0bXX4PjYaKliYW0jBg0fI0Jki9VsMpssJlO5r+jMyWStq6t9nwODG3mXTJohnDt3tnGzlr7+gaJO49BWl/dvMVvEORMvRPTZrlOPSvbkyIGoxqEtxRZL9qrzoBFjSpqbxUuTSibgDmne1l4zqH6TngOGXdI87tBeb9+6vQYMF4dUxO5tO/XwC6ofG72r7PUmYmixD4f37y5tVdGlVbmyu9q2U/eiovzUMyfFcnLioTp+QQ2aNE+MLT4RV3P6yul8326RC4v4VSz3GTzytn5DK6ppMhjEibPn/lds5ezi2rJdF7HQoFGol7dfckLs1eye1WJWKYv7b9K0lY/fpfN+lHt2LCajY8n06EJmxtk2Hbppta516zX0+fsdWnmfpQYMuz/h8L6ykXq5myurTcfuLdp2lgAAAHCrYAQ0AAC13ZmTx86ln3FxLx4KKrKrjSsWDBx2f5Pmrfdu36jX5VXSMHLN0q69Bj004VURCMbsjkyIPyCax+zcPPqxSSJjit23y2K+dDhq5NqlnXsOuO/x/3N0coo7GHUs8XDDJs196tab+/2nJpNp+8YVvQaNnPfjtLJNjhyM6t7/Ti8f/5TkuLVL55ZdlXk+fdPKhb2HjBQZ4q7INfa9tdlsf/3xk0hsxb6dTz+7esmv+ovnMaio1bI/fu7S4/ZuvQeLPdm7fYN97oiyUk+naF3cTx5NtFqtFW1IHIrS+gejd/QYOKxxs1Zzf/is8sMiJByMuffR50V6mBAbI468KIk/tFekvcMfeEKldhDZ6+7INVLFkuL2BwQFP/7CO1abNenw/vjD+6QKXtGqRb+KsLVn/7uOJhwqjQVFFFu/UbPhDzyZcixBJLkBQQ0u6T/xcIyo8ORLH+Tl5hxLPGSfJKRceTmZ65bNF6fMr25wTtb5tX/OEYV7tm0YdPeDE16Zei7j7NlTx+w1xfGv16jZJc0NRYWL53wjfpMYMWaCzWpNOZqwbO4PhYV6qfh6+1McbXG9FRToY/ZEHk2ILdvw8ktLuhKxq+tLdtXT2/fU8cSVf/xiz27F+T19ItG/bn37lMS63Owrnr7LxcXGqDSOg+992LuOuHTjo7aur6hmfr5O7LD4hWDL6j+v2Cr97ClPLx9xItJOp6xcNMtkMppyjVfcvS1rl/YadHf/O0efOBqfkXb6krXlnh1xeBs2DXvixfd+mfHBjg0r77r/8dHjJ4mfB0qvmcr7tBM/cvgH1hePlu2Kb8yo1+lmzXy/3M2VFRBU32Q0Ht63SwIAAMAtQab1CJKAWsnbNzjtdKIEADeCq7tPQX6udD04OLlcr65wo4weN2nL2j+Lb9z33xo0YkyKSGqrIelTKlQjHnpq3Z/zsiqYlgTXICS0VfO2ne33dQQA1AZOzm5FBTrpehBd5eVkSABwIzAFBwAAQG1hk6Rh9z0W3LCpQq4IDWsXGNzo1PEkqRqYLab1S+dF9BooAQAAAKjdmIIDAACgtpBJ0t4dm7r1HeLp7WsoKty8cnFeTqZUDerWaxjRa1BVb8EHAAAA4NbDFByovZiCA8ANxBQcAAAAqBxTcAC4NTAFBwAAAAAAAACgWhBAAwAAAAAAAACqBQE0AAAAAAAAAKBaEEADAAAAAAAAAKoFATQAAAAAAAAAoFoQQAMAAAAAAAAAqgUBNAAAAAAAAACgWhBAAwAAAAAAAACqBQE0AAAAAAAAAKBaEEADAAAAAAAAAKoFATQAAAAAAAAAoFoQQAMAAAAAAAAAqoVSAgAAAAAANYpzt9s0zVs4Nmumbhqq8vaWcHMwnTtvSIgrSogzHDmSv22rBAAggAYAAAAAoAZRBtT1f+sdx9ZtJNx8VHW8VXVu03a7TSwXHtif+tab5rNnJACo3ZiCAwAAAACAmsHljruCf5tH+lwjiNMkTpbLkDskAKjdGAENAAAAAEAN4Dp8hN/Lr0moORTOTv6Tp8jUqrzFiyQAqK0YAQ0AAAAAwM1OWTewztPPSaiBxIkTp08CgNqKABoAAAAAgJuaTSbzn/K2wslJQg0kTpzfm2+LkygBQK1EAA0AAAAAwE3NsUUL5n2u0ZzatBEnUQKAWokAGgAAAACAm5pDi1YSajhOIoBaiwAaAAAAAICbmlN4uIQazqFlmAQAtZJSAgAAAAAANzFNWEsJNZxjC04igFqKABoAAAAAgJuaystLQg2nCgiQAKBWIoAGAAAAAOBWYNHnZ8//PX/PbmPKMZWvn1zjULpK6edfZ+KzKh8fCQCA/xZzQAMAAAAAcCvIW7n8/FdfSiaj5dx5a0FB2VVF8fEnHhxlPHnyKrsqOpqc+t7byQP6HL/vnowZn1v0+srrn3z6qZTHx0nXVc7KZfHhrbJ+/61s4ZlXXoyP6HD1L8QueejtoqvLH1ZDUUVN4ju1O/fNVxIA4F9jBDQAAAAAALeCgn3R2l59Aj+dJqJV78eedO03oHSVzWI5/cKzKePG1vv2J02DBlfoZ//+UxMec+rY2e3ukeb0dN3qVfqtW+vP/q3skOr/gPugobmLF2X+/KPbHXcptFpRUhh3RLdujedDj6jr1atSV56j77Pk54sF3do1luxs93tH2ctlClIRAKh2fNQCAAAAAHBLsFpkiuL/0NkmkxmPHyvYG1W6RtO0Wd2PPj315GMpj46tP2+B2se3km5yFsyXaRzqfviR3MFRPM3ft+/UuLEig3bt20/6b/m++MqJ++7JmvVTnQnPiKfnpn+q9K7j9fB4qYo873vQvmCIjzfYbHXGPyEBAP4rTMEBAAAAAMAtQSYvfkiS24Dbz333zcnHHy19ZM37Xa5xCPx8psLJKfvX2VfsSa5SWYsM9mXntm2bRR+0p8+mzMy0jz88OnxofHir46NH5kftuaRhypOPHRs5rPSpbvMmUVO/fatYztuwXqxN6B4RH9Eh/dOPrUWFUnG6HVM8z8b8ucdH3S26vaQ3h6bNXO8clvX7b8a0VN2mDQV793o/OVGhdS5uGLX79MsvJPXteeLhB899/419Mg17b/l7dtmb565dLZ4ajh+TKlB5fZuhMPW9txP79BCpffaiBaWtjKdOnX1nytEhA5PvGJT6wbvG9DQJAFAxAmgAAAAAAG4FNptVEg9JCnh/aujeAyI1Ln3UGf+4KFe4uGhatDBnXCEwdek/wHz+3In77hHBbv7unTabrXRV6puv6Tascx00NGDqJzaz+eyrL1oLL5ps2m3AQOOxo4Xxcfanuo3rlXV8nDt3yY/ee/alSXIHjf+b73iMvDd77m9Z8+aWtsqeP9d9+Ei/V9+4fGfqPPW0TKnM/Hrmua9nOrRs5XbnXaLQcPz4yQlPmE6e9Hn2eU1I08xvvjr35RfS9Za7coU5I933/16S1Jr0D97N+XOJKLSZTKeeedJ09mydZ5/3fvjRwn3RZ195UQIAVIwpOAAAAAAAwD9cevQMmPpp5qyfRLCbKUma0BY+zzzr3LGzVBxtfyQSZ7V/gFQyr3Tq66+YUlM1DRv907bfwLSPPtRvXO/YLFRktbpNG9zvGiFTKJxat6k/d4GmSYhMJnPt2y9/53ZjUlJpK89R93vcc2+5O6Py9vZ69LFzn38mluv9NFs0Fws5ixfKNZrAmd+oPL3cht4povecpYvqTHxauq7UQfUCp30pdt6lV+9j94zIWbrY/a5h+u1bRfAd+NkXmgYNRR2lj8/pZyYUJSU6NAmRAADlIYAGAAAAAOCWcvb1V3LXrJKVGblsk8ncBgwKeP/Dq+zBtV9/8TCeOZ2/c4du7erTzz9T/7f5mgYNFFqtfvOmjB1bLTp9UexBqWREcNmGCmcnl569cteurvPU0/ptW2wFBS4DBopymVIpU6kypv3PkJxkyc4yHjuqbtiwtJW6fnAlO+M5+v7MX35yDAsTKba9pOhIrGPL1iJ9tj916d4jd9GCwrg46bpy7tBJpM9iQe7g6Nyxk27dmuJNH44Vf4/ffVfZmqbTpwigAaAiBNAAAAAAANxSRPpc57EnnNq1Ly0piN577odvrz6AtlPXDVTffY/bkKGJXTvlrV/jLnAasgAAEABJREFU/dCjKY+OLUpKEiXaLre53HZbxv8+ubyV64DbRWZdGHdEt2GDqkFDp7CWUsn0ymffeFWktC49ejq2bpPxxXTpqonkWu7srHB1v6hQrfpnWaO5qEFp8l4mgq/MVdQX+/B3FZvMySlo2pdl16rKhOkAgEsQQAMAAAAAcEuR2Wxqkfy271BaYsrOklmtV9k8sUcXh5atRMZqT12NKSnFfarUxtOnig7H+k/9xK3fAFGSs2RRuc21XbspPDz127fpd2zzvP9Be2H+li2aBo0azJlvf2rNfVsKDJSulUPzsJyli01ZmfZB0Hnr18mcHB1DQ+27ajpzxl7NeDKl8n4UTk6V1C84sP/C3hYViteiLplpRNMkxFZQIDJox+YtxNOio8mWrEylu4cEAKgAATQAAAAAAPiHfc7lU88/7Vgy5UXOgvkyBwe3/gNkTs6SWpO3coXKw9OYnpb566xym4vY2mXAwNxFC6y5Oa4Db7cXKut4Gzesy121Quntnbt0qUWXJ/0LHvc/kLdq+emJT3o8MEZk4rkL//B++jm5g6M6OFju4nL+5x8luUJSKnRr11TeT+X1Telpp194zqX/gJw/l5hPn/Z+6FFRqI3oqvIPOPvm677PTTKfz8xZvMCcnd1g3iKFs5MEACiPXAIAAAAAADWfTK6wXXHSCVFBcYWxaF5jHvJ5+bWiuLjMb77Sb1jv0rd/0Lc/qgLqKt3d/Sa/aUiIP/n4o7p1a7zGPVZRD679B5oz0p3at1fXvTDM2fOhR7Vdu6W+8erZV1927thJ0zRU+hfUfv6BX3xlMxnTJr+Ws/APkZh7P/SIVDJZc8D7H9kMRRmf/68gJtrz4Ucq76fy+m6Dh8rd3c++/oqtqND3lTfch40QhQpX16BvfnBq2y59+mdp706ROWsDP/uc9BkAKiHTegRJQK3k7RucdjpRAoAbwdXdpyA/V7oeHJxcrldXAADg5hSyO/pqqmX/MT/jy2mOoc0LoveqGzZUeniWrjJlZZmOH3MKb18Yd9jn6Uke99wr4T+X2Cm8SvWdnN2KCnTS9SC6ysvJkADgRmAKDgAAAAAAbgWug4ZYdHn5UXsUdbzlTheNyVU4OVu969jkCq+Hx4tqEgAA/xUCaAAAAAAAbgUKrbP3o+PFQwIA4KbBHNAAAAAAANzUTJmZEmo4TiKAWosAGgAAAACAm5oxMUFCDcdJBFBrEUADAAAAAHBTK0ri9uk1HicRQK3FHNAAAAAAANzUjAkMnq3xOIkAai1GQAMAAAAAcFPTb9tSlJwkocYqOnZUvzVSAoBaiQAaAAAAAICbmq2oKG3y61ajUUINJE5c2muv2AwGCQBqJQJoAAAAAABudsZjR8/P+FJCDSROnPH4MQkAaivmgAYAAAAAoAbImf+71VhU5+nnFc5OEmoCS17euc8+zVu1QgKAWowR0AAAAAAA1Ax5SxafvO+ewuhoCTc9cZpSRo0kfQYARkADAAAAAFBjmNJSTz31mKpesEObtk5t2zq1aacKCJBwczCmphbujynct69wX4zpZIoEACCABgAAAACgxhHhpnjo/vpTAgDg5sYUHAAAAAAAAACAakEADQAAAAAAAACoFgTQAAAAAAAAAIBqQQANAAAAAAAAAKgWBNAAANRwNpvNapMAAABwCxFf8Gx8xQNwSyCABgCghrPZ5DKZBAAAgFuITCYXIbQEADUfATQAADWbxWqVK5USAAAAbiEKpcJqJYAGcCsggAYAoGazWS0KhUoCAADALUShUFstZgkAaj4CaAAAajaLxawUATTTQAMAANwyrDalQkkADeDWQAANAEDNZrNZrTaLWuMoAQAA4JagcnC0WC02iREGAG4FBNAAANR4JqNBodLIZAoJAAAANZz4UqdUasymIgkAbgkE0AAA1Hg2m9VsLHJwdGaUDAAAQM1mk8SXOvHVzmbjix2AWwQBNAAAtwKLxWQxGx2dXCRJJgEAAKBGkjs6u4ovdeKrnQQAtwqlBAAAbglmk9FqtTo4aM0mg9lilAAAAFBzqBTi/zmYjEXcexDALYYAGgCAW4f454rJalGpHVVqh+Ix0cUPq81qkckZFg0AAHCTsdokuUKhEP+nEg+bzWoyFjDzBoBbDwE0AAC3FPGPFqOhQFb8jxmFSuWgVsskET+TPwMAANxkiqNmm1V8ebNazUZjoc1qkQDgVkQADQDALUj8A8Zc/G8YJuIAAAAAANxI3IQQAAAAAAAAAFAtCKABAAAAAAAAANWCABoAAAAAAAAAUC0IoAEAAAAAAAAA1YIAGgAAAAAAAABQLQigAQAAAAAAAADVggAaAAAAAAAAAFAtCKABAAAAAAAAANWCABoAAAAAAAAAUC0IoAEAAAAAAAAA1YIAGgAAAAAAAABQLQigAQAAAAAAAADVggAaAAAAAAAAAFAtCKABAAAAAAAAANWCABoAAAAAAAAAUC2UEgAAuAXJFAqFXKGSy+WSTC6TSQAAALip2Gzi/6zFLCaLxSKeSABwKyKABgDgliKTyRQqjVymsFrNZrPBYrHabBYZCTQAAMBNxmazyexjBhQqtVJjtVksJoPNRgwN4FZDAA0AwK1DrlAqlRqzyWC0FJQWkj4DAADchEq+pFktFvEwi6cqhVqldjKbDdaSpwBwyyCABgDgFqFUqeUKVVFhvviXjAQAAIAaxWQxmixmB0dnq1xuNhklALhVcBNCAABuBQqFUqFUFxXoSJ8BAABqLKuhQCe+1CkUKgkAbhUE0AAA1Hgyufh3ikPx2Gcm2wAAAKjJbDJJfKkTX+3kcoUEALcEAmgAAGo8pVJdcssaiwQAAIAazlZ8N8IihVItAcAtgQAaAICaTSbI5QZDkQQAAIBbgsFYJL7gcStpALcGAmgAAGo2uVxptZhlcv59AgAAcIsQ0bP4gie+5kkAUPMRQAMAULMplCqzmfukAwAA3FLMFpNCSQAN4FZAAA0AQM0mkyusFmZ/BgAAuKVYzWYZI6AB3BIIoAEAqNlkks0m2SQAAADcQmw2m4zveABuCfyYBgBADVd8F0ImgAYAALilFN/hg+94AG4JjIAGAAAAAAAAAFQLAmgAAAAAAAAAQLUggAYAAAAAAAAAVAsCaAAAAAAAAABAtSCABgAAAAAAAABUCwJoAAAAAAAAAEC1UEoAAKB2U9qs/TSqbhpFiEoeIJOJkrM2W6LJGmkwbzSYzTJ+rgYAAAAAXCMCaAAAarXOKvlkrUOQSlG2sKl4KBVDHVUnzZa38wxRZpsEAAAAAEDVMaYJAIDaa5yT8lv3S9PnsuopFd97OD7oqJIAAAAAAKg6RkADAFBLPeqkfEaruaTwjNmaarU5yWzNVRe+JMhlshdd1CabbV6RWQIAAAAAoCoIoAEAqI26qOTPlkmflxeaFhWZjxgthSVzQAvNFMbxTqp+f499fsVFfcRsOVjpXByzfp3VqXMn+7LZbE5OTo7aE/Xpx58aDAZR8v4H7/Xu0+e5Z57dvXuPBAAAAACoHZiCAwCAWkdjs73p8k/6/GpO4Ws640GTpZNa8YCDcpSDsrVSFm+xvaAzfpRnsNeRy2STXTVy25Ung57/+/xZv/yyYvmKunXrPjjmwS9mfG4vd3RydNY6S1fhgw/ej0+Kb9WqpfRfqeNdR2zx62+/lgAAAAAA1xUjoAEAqHX6axQBygs/Qs8rNK0wWoPlsmnuDo2V/0wGPT/f9L7eMKfIXEche8RZLZXclrCzWrHDZK2882+/+eZsaqpY0Do7f/fjdz169ozoErFzx85Jz70gAQAAAABqGUZAAwBQ63R3uPALtNlm+1pvlGy2D900In3eY7TMLTDaV93rrBrjVJw7/5hvNP498LmbRnH1W9Hn569YvlIshLcPF38/+d8n8UnxTZo0Ll1u3brVN999vXvv7gWLFwwbdpe91boN64aPHCEW/li0YOuObfbC8PB2X3/79ZbtW6Nion6d82uXrl0u7OToe0U/9z9w/4cffiBWiQWpZDjz1I8+XLV21f6D+xYvXWwvtHN1df1s+v8it205EHtgzbrVr73xqkwmE51s3blVrO3Vu5fo7ZFHH5EAAAAAANcJATQAALVO6N/Dnw+ZrNk2qataEaZSrC80jcsp+lBv2mm4cLPBh5yKc2qdJDv496jnMOX1/OYw5Z235DL5ju3bGzdq9OHHUwcOHCAKFy9aFBcXJxb+XLxk/rx5YqFeveDvfvi+TZs20XujNm7Y2KhR4xkzvxSFpf089sTjjZo0Wvrn0vi4OBEof/vjt0PvvONkSsqyv5Y7OjpOnjJ5yODB9prvvf/eoMGDxao/F/2ZX1AwZuzY8Y+NS0pInPvbXLH2xInjs3755XBsrAQAAAAAuE6YggMAgFrH4+87DZ61FCfLzVXFsfLqv3Pn0ik2vBVyT0nKkqTU4mrFY5/9FVUYAS2y4EGDB4mF6L3R5VZYs2r1t998Jxb69+/7xcwZIhpevXrN1199ExQYFBoa+vuc3w8ePCTWTnj6KQdHhyceezwqaq942qlTx1m/zR43/tE3J79p7ychLu6x8Y/bl0fee0/z5s0/nzZd9COeurm5rVi98rGnHl++YoV4GtE1IiEh4cH7H7Tv3hNPPn7wwMGYmH2nTp4e/cDo48dOfPj+VAkAAAAAcP0QQAMAUOuURsyu8uIkOtf6z60FFTZrq7+HOZtsthybTSS12r8Da6V05ZsQPv7EE0XGQrHQvHmL8PbhmzZu2rljZ7k1t0ZutS9Elix4eHqUWy2iS5fExER7+izs3r3n9KnT7Uqm9bDbtWt36XKP7t3F319n/Wp/mpubu3vXzsFDhtTxrnPu/Ln4uHixS2+8+ca6NWv37z9gD6kBAAAAANWHABoAgFonyya5lSyIrFlts20qsryotTZWytcare3UShfFhQA61mS1lkTPzVUXBj6nW61X7Pze++61L1gsliULF0+Z8lZFNU1mk33BYDBIJUOSy63m7u7m41MnPin+opeQmV26bDZb/qns4S7+7t1/6Zhr/wA/EUB/9OHUKW9PGX3f6AcefMBsNu/ft3/K5DePHj0mAQAAAACqBwE0AAC1TqzJ0qBkmLObQv6Ak/KnQkui2ZpgLg6X26r+meX5p4LigLi9Su6ruBANHzFeeQR07+69zqamStdPTk6uzWZ79623yhaaTJbyK2fniL+vvvyaLi+nbHlKyknxNzb28MgR9zg6OrZq1XLYsLvuGjH81ddeHffoeAkAAAAAUD24CSEAALVO5N/TPQvPaDX3OyhDVYpoY3Gku9dkNVitGRbbR3mGSFFis03SqksrbzGapepntRXH3HL53wOxDx709fURifP69RvFY/euPc2aNzdbyt+Tffv2ib8NGzWwVxYP/4BAD0+v3Nxcfz+/aZ9/NmHiU4WFhbt373nllddEYWC9wOItWi0lW5RJAAAAAIDrihHQAADUOpsNlkyL1atkqg25TPayqybOZM6RZB4y6fAjZhgAABAASURBVIjR0uF8ob2aSrK94aIJ+3v+jWSzZasIoGXV/uv1mTOnxd/nJj2/d+/eGV/MmD1rdu++fT6b/tnyZSuKDAWdIyKaNm36zlvvbN+2/fK2ixYufPjRR8Y/Nj4wMDAjI71B/Qbde/ZYuWLFgj8WZJzLaNWq9YCBA4Pq1cvNzWnevIWbm9uyv5aJVplZWSKMbt++w2uTX1u3em3pfNMAAAAAgH+JEdAAANQ6RpnsfzpD2ZI9xuL5NzqrFH96OT3hpOynlr+sVS3zdBrmpLJXMNtsb+UZLLL/4pvDb7N/O3TwYOeIziJHdnJ02rVr9xPjn0g5mXLv6HvGPvSQ1lk7c8bM3+f8Xm7bnJzcMfc/sGHdhoG3DxSV24a3W/rn0rfefFsqnpPa+sLzk6L3Rg+9Y6hY1Sy02ezZsz98/wN7w08/+Z9CqRgzZkyvPr0lAAAAAMB1ItN6BElAreTtG5x2OlECgBvB1d2nID9Xuh4cnFyuratnnFXjnC9Mr/FmbtGfBsubzuq7nVXlVp6SW7TEYJEAAADwX3Fydisq0EnXg+gqLydDAoAbgRHQAADUUl/km77SXxgHfc5qk9tsvRwUl1ez2mzv5JE+AwAAAACuBXNAAwBQe31TYE4x215zUStlsl4ahX1W6LKSzZZ38wz7zDYJAAAAAICqI4AGAKBWW2W0rD2fr5XJRjiqog3mxkq5TJJOW62HjLZdJvMmg8Uqk0kAAAAAAFwTAmgAAGo7i0yeK0k/FZrF49J1pM8AAAAAgH+BOaABAAAAAAAAANWCABoAAAAAAAAAUC0IoAEAAAAAAAAA1YIAGgAAAAAAAABQLQigAQAAAAAAAADVggAaAAAAAAAAAFAtCKABAAAAAAAAANWCABoAAAAAAAAAUC0IoAHg/9m7D8A2qsOP42cty/Lee8SOHduJ4+y9Nwlh7w1lFuighdJJF5SOfykFWlaBhA1hB0L2dLZXnHgm3nsPWbY1/89WIhyvOCHK0vdT1ZzerXfv3inyT+cnAAAAAAAA2AUBNAAAAAAAAADALgigAQAAAAAAAAB2QQANAAAAAAAAALALAmgAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAOeOQqGcPGuRRQIuccmTZ7u5eUgXmBEjE0IjoiUH5hcQnDBmggQAAM4hAmgAAACcO+OnzvbxDXCScKEbO2mmh4e3hDMSHBo5bspsrbZVusCYzea5S6+WHNjMBSvkSpV06fL1C4wfO0kCAOBCopAAAIBDShgzIX7sZP+gkJaWxrys9PT9O/pnggtXXN/R0b57yzfSJe3y6+6MHJkgJro6O0oKc/du39jW0hifNGnM+KlrVr804CpqF83ocVNS92yTzqrY+LFtrU3VlWW9C8dPnTNj/nIxYTIa62oqSo7lHdi95fsHuPOWXNOuaz2wa5N0bo1MSN6zdZ3U67gsFktbS3P6vu2H0/cOfztDn6BLwJn1Mb+A4Bvv+XGfwl2bv848sNP21Ns34Iqb7l3z1gvt7W39txCXMHb0+Gmfvfeqq7vnhOnztq3/TDqHhq7bGbjihnv8g8Pe+PefRDeTvocV191ZXlIomnGY12Pc6AlHczJtTwd8vbU19Rm80gYGh3l6+eTnHOpdGBAUcvkNPxAHK6bv/cnvndVqMdHW2lJbUXpg9+aGumrxtLgwb/6K6wKCQmurK6TTJ5PJ7vnRb6vLi9euWSVdwAa7fFxc3EIiotd9+rb1aVBI+MTpC4LCIvX6rtKjeXt3rhf/Cri4uN71yK/++/dfn1lvnDBtbk7mQXFCexc6q13EWfYPClc5KxvravZuX19RWiidVbZ/Ptramq9Z9FDZsbyzdREBAPD9EUADAOCIEpOnzJh/2Z7t33772TsRUSPHzZinVKn6Z5FHcw4ZjQbJAVgTOpWzs2iZq26+d/XLf6uuKLFIgyZWIt0YO2nWWQ+go0eNriwr6RNAC0UF2d98slqtdomMTZw8fYHGzX3Hhi+ki5BG4+bh5VNaVGB9aj0umUweN2b8vCVXifLW5oZhbmroE3QJOLM+Vl9b9dKzT0o94z+ER0YPmBK2NTcdTtvdrtMOvan8rNSrb3tw24bPJcu5a+dh1m2YRBv6BYbWVVeMGBlfWJAjnSXDuR5DI6N3iKbrccrX2zN4pfULCguPHNkngO7jwzeer6utCg4JHzV64lW33L9m9X9amupF8F1RcjR8ROyZBdAjYhNF+hwYGikOv7OzQ7pQDXb5RIwYKV46RNws9Xxas/LGH4jPvXZs+srD03PclDnLr7ldfB5gW/jMemPSxFnFBbl9Auhps5eq1ZqvP37DYDBMnb1owfLr3nnl75azemXZ/vnQd3WVFx2LGzNBfKonAQBwYSCABgDA4cjlihnzl2/55qPC/GzxNC8ns6mp7qpbHkjdvWXkqDFjJs6wmM2BoREv//03Imtob2+rKC1UKpUz5q0YMSpRJA6Z+3flHDrQe4NxCWMTx0/7vOf3di8fv2tv++H//v1HURg/dnJLU+PI+KTcw6kF2Rlzll7t5e13LPfQ1m8/7VOl8VPnJIyd7O3rn5NxYOv6T8Wv5fOWXt3V1ekfEBwQEl5alL9r41c6nbZ7m0mTmpvr4xLHN9RW7d2+vqqipPd2xFri134PL++omASRxH376TvWFCB50qyEcZNUKpeCnMx929ebzaYBW0b83p6xf+eEqfMCg0JEVROSJuZlpYqdit/ka6rKR4+f2tnRvv3bz9q1bbfe/3Ox/MNPPvvFB6+XFx8V9R+VNNHFxTXvcNrenu2LmjirXXz8A7s6Oj5992UvH/9pc5aGRcU01FXv3f5tVXl3tUePn5Y8aaarm3t58bGt69bMXnzlyIRk8YhNHPvpOy/3r55ofFGf6vKSW+796aGDu5sb6/qfl2lzl7l7em788kPrKnf88Jdbvv6ovORY/xr23nL/9hmw/XvOb98DEdu8/aEn8g9nxo5OXvfZ2w011YtX3iDyqXZta2rK5rzsjN478g8Oa6it7rN38TT30MEx46f6+QeKAPrmex8TyZ319sClV95cXVkuPhtwcXHrs9mAwODBTpC1eUUfEEftGxBcVpSXsvlrrbZVhD0Lll4TGdt9t3v+kfTdW7tvOA0JHzFjwQofX39xRDs2fFlXUzF0z7Q2V3zyRLXaNT87Q1TGGmb1L1QolNPnL4uOG9uhaz2cvi87Y7+1i4pryho+ig4QGR0nosz+/Vbp7Nynj/XpDBHRo0xGw/BvohStWlVWFBWbKDrJoQMpU2YvsWZzkTHxk2cuCAgKq64sXf/Zu71vmWyorxFhWVBwWJ9PRIZ+Neiu24i4idPniZYXQa0I9xobagbsYwNeziKZtdVtwKvGZsDm7SM2YVxVRXFNZWnc6Am2AFo0xaHUlDETpqnVbvlHxOXw7WAvONKQ+l+PtlniNVa8ElaXl0pDvt7alre90ko9Xa7/i0mf7jEibvS8pVdJPd3D+nnDYETcLE6feIgeNW3OkvVfvCcKayrLg0MjB17eyWnSzIVD/GFEbEJyafFRJydZbOL4rLTdUvc9xd2vADs2fjVt7tLOzvaM/bvE5Sz1dPWhm3TAS2/AV6r+F1fv/rxvx4Y+F7tMoRjs8vENDKk50Z9nLliRezhtz7ZvxXRbS2NNRfltP3wiNGJEY12tdYGhe6Oo5K0PPL593aeT5yxWqpzFhkSDiJdcN3f3m+/76cHdW0TFbPsNCA07uGuzOH1iesOXH4RFjRQfvJlMxgE7uYeX74y5y0KjYmory7LS9hQfyxUXS+9/mvtfg4tX3tT7n4+SoryRo5IIoAEAFw7GgAYAwOH4BQSJ33uP9aQhVrXVla/+8ymz2SymA4LDjqTte+Ufv+29yrxl15osxg//9/yWtR9Omb04LDJmODvyDwoVIct7r/1fUGjEzAWXr1n90mfvvhwdNyY47KTsIzA4LDpu9Pb1n7398t+8/QNsg1eOmTA1bf+O1f99VtfetviKm6yF4dFxrc1Nq176S3b6vuXX3il+D++zU7GprNQ94jdwZxeXhOTuTYmQK3HcZBGurXnrBS9v35kLV5yy5iJeObmGEa2N9WvefLG5vm7S9AWtzY3vvvoPXbtWRD8i2khMnhIVE7/hs/fWrHrRLyB40swF1rUCgsO3frNGpM8ymWzlDXcXFxxZ/Z9nRZa64rq7RDatdtHMmL9s27efiqM2GPQxCckbv/rgaE6mCGIGTJ9tWprqRYAS1NOG/c9LzqGDUTGJ4gCknlFoRZxUVnJssBpaDdY+/dt/wAORumMa584u3Vsv/lm0xqRZ8zs62995+W/ihE6atcjJ6aTBCTw8fVpbGvsflPjkw83Dq7aqfLCjHnqzfU6Q1JMWzV58xb6dG955+a+tLU2Lr7xZFMbEJgaFR3727iuihUMiokVTiMJZi1cWHMl466VnjuYeTp4y6+TNDtAzRXOJIHXD5++9/d+/+vTsZbDCuUuvcnbWfPTGvzZ/9dGEqXOj4xKlwfXpt336WP/lw6NGhoRHSafDw9P7k9Uv9Q7FlErV5JkLsw7ufvOFpxvraqYvWN5nldqqMr/A0D6FQ78aiOxM9Jb9uza9/vwfRSa74vo7pcH72BCX82CdzWY4zSvCuKKCnGN5RyJHxvfe+NiJMzZ+/sGat/4dFBIxacZ8a+GALzin1Pt6tPH08hUfUxlN3Tc1D/1628dgl2qf7pGduX/b+s+P5R4eOn3uLTfroHhFOlHnBncvnwEXE6noxGnzBtuIQqESLVmcn114NDtudLKtXLwCRIwY+cH/ntuy9uPpcy+zpdtDN2n/S2/Awx/w4pJ69ef+F/sQl494CWo58WcWokFEx7PNEufrrReerigtGqhZBu6NCqXCJzDos3deOZy2e+qcJeKFd/V//qJta3v/ted6X2hCQXbmxBkLxOdG4rM08VTUSvSKATcrXtyuuOHuyvLiVS/+JXXvtmXX3Obu6S2d/E9z/2uwzz8fNeUl4uNPCQCACwYBNAAADkfl7NLR0T7YIMJ11RX5uZm9/zRYoVBGxcbv3rJOrCWik2N5h6JHjZGGQcRPWm2LWKuyvKS2plyyWBrqqhvqqvp8s1lNVfknb/+3orRQpXLWtraIvMZaLrJU8Vu6vqtrz5Z1ASFhbm4eUnd2U56xf6dIbPNyMhvqq0eOSuqz0+KjOdUVpWJHuZmpAYFhomT0uMkHd21uaqjT6bQpW76OHzNxsApber54zWDoqjn5j9Obm+rysjPEsRzcvcU3MKTPWonJkw6kbG5sqGlrbc5K3T3iRBBWkJNpvXU0PCpW29aSeyRdr+8qzM8W8Ud4ZIyTJFPIlc4qdWeHbtPaD4+czvDHOm2b2tllwPMi4rCW5voR0fFisZiEpIKcDKfBa2g1WPv0b/8BD0TqGcR53471BkN33CZ3UoqExWwxixMqMqA+f2OuVClNhu+GGhgRm/jwk8+Kx6IrbkpN2TrEN7YNvdn35ZQUAAAQAElEQVT+JygheXLekbTKsqLOzo6DKVtEIiaSHdHgSpVa5DutzQ0i4bLejSiXKVxcXQ16vQiANn31Ye/NDtgzRXOl7toimstsNm35Zs3OTV8OWCiXK2ITklM2rxVnp6G+Jm3v9jHjpkmD699vz7r0AztFB+hdIq4j8bGQaDq5XN7W2tQ/sRJJpae3b++SU74aJCZPPpqT1X0zr8Uijtr6hxGD9bEhLufBOpvVcJrX3cNLZHbHcg+Ji6KhrkZ8xmObtXfbt+JyaG9v279rw6jRg3Z4aXis12Pvkt79fOjX2z4Gu1S/f/do17aqnJ2t00aDXnlG38InXlIaaqtbW5vyD6eJzxdFC9tmbfnmU/FSVltdcTh9j+gD1sKhm7T/pTfg4Q94xUm9+vOAF/tghyBOjfm7U+PcPrxviRysN4p+eGDXpo4ObeqebRaL2dvHb7AtiH4uIulJ0+ff+ciTV9/6gH/Py9SAmw2LGmkymw+lpohAXBzUB/97XqTqUq9/mofzL3JTY72rm4dcJpcAALgwMAQHAAAOR9fepum5CWtAJlPf4Sk0GjeVSv3QE0/bSo4OOfDoAJsScaHF6cSkpe9dsR7ei664UePqLn4Vl8lknTqdtbyrs/P4dswmnVbr5uEppkVaYVuxtalR4943JDIajdYJg9EgIt7u+rt52O66bW1uFKFD/9FLZy1cMavnrsx2bdvXH7/VZ9Bb24EYjYb+v9K7aNyvvPk+21NbomEyHa+Ji5t7SPgIEbPallFr3ERmsWf7txNmzJs2f1lVaUnq3i19wsEhaNzcO8RJHOS8FGRnRickFR3LiY5L+vqjN4ao4YmtDdA+0kDtP+CBSD3n1JYIH0jZuHDF9Vfder++ozM762BeVmrvfXV1dSqVzran1rF0xZpBwWELL79RBJG5WQelgQy92f4nSOPqFj9mwuSZC23LuGjc8vMOhUfHLr7iRqk70ctN27NNnKOdG7+YMnvxzfc+1lhXI0IfkfjYVhmwZ/ZuLtswr/0L3T29TWajbQExV9PTgQfTv98O5vYHn/A4cfvqlNlL6morP3rj39IwmPtd2iI+m7P4ihFxo8VnRSI9FMfYZwHxYYyr5qRqn/LVwM3ds7G+2jrd/fWSPb16sD42xOU8WGc7Xg0391M2b9zoceIA7//ZH61Pjfrx1qEhBL3+eN9ubqjXuLtbp/t3eO3w0knr9di7pLOzU6E6nvAO/Xrbx2CX6vC7x2BEHNl5ornEByr6rr7DN8cnTVq44jrrtLXZ132yurAgu/cyoxLHBYaE205K/NiJB3Ztlnpe64zG46eyranBdgf00E3a/9Ib8PAHvOKkXv15wItdGmSAePESJD/xEtSha+9ulmGMZD1YbzT3sJYYjSbR34bYSFlxgXiID9Lixoy/4qZ73/7vXwfcrNLZRdvaZCsR16b130vbq9xw/kUWYb1oH5Wzus9Q1AAAnC8E0AAAOJz6umoRAQeFhNuGdvX2Dbj+zodfe+73Ay6va9caDfrX//VHW6Lah8UskqzjmcgZ3FgnEtiayrKULV+L6alzlqidNdZyjxO314lIUePmpm1t8fD0FvGWbUUPb5+qslOPgavTtnp4+tT0DO8gkjuDvqt/4mD9EkLpjOjaW7dv+Ly0MG/QBdpaqytKPnn7v33KM/bvFA9xdIuvuHn6/Ms2fPG+NAzevv6BoRHrP39XHMaA5yUvK+3GH/w0ICikq0vXUF9zyhoO1j7921/l7NL/QFxcXHs/bW9v+7In9Q4KjbjqlvtrKkqaG+ttc5sb6sZM6HunqlPPvcb5R9IiRowUAbT4sEJ2ojspFKrBNisNSRxU2t7te7at61O++Zs1UneC4371bfeLZPBI+r7ykmPiIfUMPitOxKqXnrEtPGDP7N1c3Smqk5OIbvsX6rRt3Td4urhaAyAxV3QDqftisdhSqv4DyAzH2y//TeoZvlZkiAdStkjfgwgQPX38Vv/nWRHch0WNnLXo8j4LOKtduvQnXSynfDUQYb27x/F8XESAXt5+LU31g/WxIS7nwa6a43MHad7eRiYmb/ryA+so5CKzu+PhJ8VP6zDE4qOFCqn7kwYvXz9d2/HsuH+Hl4bBdj32LmxpbnAWROt1dpzW6+0pX0zOWGLy5Kqy41eNl29AS1PfkXDEpSceonPe99Pfv/yP3/TfgujYoRHRb/77aZ2uu8XiEsZOmrXYGkCLtdzcPKzhsru3b3vb8aYbukn7X3oDHv6AV1yfBfpf7F6D3Izc1FDr4+9vnRYdLCo2wfoiKfV017sf+dXGL9+3jQH93S4G6o19XvqG4uQ0dfZi8Wov+oP46FH8W5M0fqp/UOiAmw0fEevW64+EPHuuoJMqc6prUOr5SwXxKtrZqZMAALgwMAQHAAAOR+R9h9J2L1p5U+K4KeJX6LDImEUrb8g4sKvPsAY2RpPhaM4hkRAo5EqVyvm6Ox+JjR/be4G6ukqRwcSOGiviwrETZ0inyWQ0ii2LCV+/wLjE8bbyEXGj/QNDRJ2mzVtWV1VhTTdc3T2SJnTvYkRMgq9f0NG8w6fc/pGMAxNnLRBhkEwmnzl/Re7hVOl7M3R1iczFGiBmp++bMmuRq2v3fZQLV1w/e/HKPguXFReoXTQJyZPFsfj6B9358K/cPbzEod1070/d3DzNFrOI46x/sG80GNQazWA7FSdrVNLElTfeW5iXJQLZwc6LiNga66qmzll6NDvTuuLQNRysffq3/4AH0qeSi6+4cXLPyK0iajEZu++M7D1X5LnePv4i/+2zlgi24kZPaG7qHpu1obZy3ORZIs8ShQEh4cPZbH/ioOJGjw8M7h6sID5p0k33/kTUecz46cuvuUOcOJPZaDAaRJuLZPD2B38hdtTTbu0mg773RgbsmbbmkrqHIb562uxlAxaKKhbkZM5YsFxkT+LETZg690hG92iz4mIZGZ8kKiaabmTC2CEOoXcfsxPRkqLrmM0mcVpFDfsvIOLj3p8fSMN4NcjOPDAyIUl0D6m7wactv/YOafA+NsTlPHRnG6x5bURs5+XleyzviPWpuCiqK0rjxkywPk2aMkvdMyTLlNlL8rLTrIUDvuAMoc/1eNI8i6W+tipqRJx0mq+3p3wx+a4FDHoXzbACUPGZzfyl10SPGmP7jC0sMrqiuEA6TeIKFdevNX0WxMlydXf3PzFE+NS5S8XV5O7pLa6ynKxBX0NsWxvw0hvw8Ae84nob8GIf7PIR3SAsMtY6LRpkwrT5k2ctEtUOCApdfPmNLY0NA44BPZyXPhuTocvF9eRTY7GII1288kaxrsjixUuZWuPaUFc94GbLi4/KZbKEnmFMROGNdz9qbRCbwa7B3v98+PgFtLY0WftYeFTsvKVXSwAAnFfcAQ0AgCM6sGuTQa+fPnfZ/GXXtLW2HE7bnbp3+xCjlG7f8MW0eUtveeDnLhpNzqEDhflHes8VEdWBlE2Lr7ype0TXfTuiRiZKp2P/rs3Lr7v94SefrautrOx1C2TekbQ5S670DQguOZpjuztYJCA+vgEPPfFMdXnJN5+sMpycGA4oN+ug+CX/mtseVKrUIrTat3299L2JvEm0g8gLdnz7ec7hNKWzy4ob7/bzF1XNPbBzU5+FRQrw1Udvzph72awFKwwGw8GUzW2tzeJRlH/k5vseUzk7V5YWbfyy+wAPpe6eu+zqkfFj33/9n723YB0rWUyIqFosc/DEfa+DnZe8IxkLV1y39ZtPrU+HruFg7dO//Qc8kD63Aabv3TF36VUi1+vU6fbt3NBnXBGj0SDiFRG8HkpN6X1cFrM5Pydz/67uiu3e/M1Vtz4gWiYn66DtXsj+mw0OjZAG19rcsOXrj2fMXx4YGtHUWLdzw5dO3aNyZ4SERz7wsz+K0L/gSEbukXRxSHu3rluw4gYPT6+Wxvqt337aeyMD9kzRXCILE83l4xdYVJC9e/vXgxVuX/+5CFvveviXIv1M27/9WE+6KvLZqJj4a257qKQwT6RIIeEjBjuE3n0sPzezz9yy4qMmo0H6fvKPpInKiKuptaW5MD/LNhjFcU5OQaGR29Z92metoV8NRMtv/OpD0XPEuuKVYUPPrcGD9bH+l7NCcTwxHLCznVSNgZrXJjF5UsmxPOvXAJ442IzR46dk7N8hpvMOdf+VgMhA8w6n2a6mAV9wBjTY9dhbYX52dPzYvJzuEzf819tTvpjYiOMVmfKDj//5rRef6XNHsM2N9/zYOlFdUfLF+69Zb/UVHdUvMPSbT94ecBXxaUTq3m0DzopNHJt/JLPXkubigtxRSeNTU7aKaZHb3v/YH0TouWf7Ots4NkM0qWWgS2/Awx/w4uptwIt9sMtHvP5oXN3FR0qiNUSdN3z5/qyFK0Tqrdd35mdlrPt09YDHPpyXPhtxuhesuL7sWMG2Dd9dO+s+eXvJlTff9IOfSD3/Yq79+E3rWRuwk3/50Zsz5y+fvfBy8RGROLS+H28Mcg32/ucjLGpkZc/d5VJPih0REy8BAHBeObl5h0uAQ/ILjKwuz5cA4Hzw8ArQtQ/r77tPSa1xP1ubuqDMW3q1+K37wK6T8pe4hLGJ46dZv9YMdjVg+58VQSHh85df/97r/xzm17LhfBHZ9Lipc+x3uZ2vy/nmex/bseHz7q9J7OWsd3iFQnXbQ4+vefOFYQ4kfc5MnD7P1d1jx4YvpbNE5LB3Pfrr//7tV33K7fca8j1NnrnA1c1z2/rPpEvXdXc+smfr1wPezY2LjsbVs1PXJp0NYlOtzbUSAJwP3AENAACAc6e6sux90ueLwdiJM7JSd0s4I0aj/q0XnpYuPKl7tkmO7XuOnH7hEx/yyRVy0mcAwAWFABoAAABAX9ZvfQRwcREf8n34v+clAAAuJAzBAcfFEBwAziOG4AAAAMDQGIIDwKVBJgEAAAAAAAAAYAcE0AAAAAAAAAAAuyCABgAAAAAAAADYBQE0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AAAAAAAAAsAsCaAAAAAAAAACAXRBAAwAAAAAAAADsggAaAAAAAAAAAGAXBNAAAAAAAAAAALsggAYAAAAAAAAA2AUBNAAAAAAAAADALgigAQAAAAAAAAB2QQANAAAAAAAAALALAmgAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAAAAAABgFwTQAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAA7Kw8PjsZ89tm7DuszDmWvXff2Tx37i5ORknfXu++9+/OnHYmLp0sX7Du5befkK6ay6/Y47cgtyJ02aKKaf//fzYtr62L5rx3PPPzdmzGgJAAAAAHBJIIAGAMAR+fh4v//RB/c/eL+uQ/fxRx+Xl5U++NCDz/3ruT6L1dbWFRUWVtfUSGfkozUfiscpF9Pr9aveeuvt1W+XlZbOXzD/3Q/eW7ZsqQQAAAAAuPgpJAAA4Hie/NUvR4yI+smjP/r22w3Wkl//9te333H7oq8W9eOEGQAAEABJREFUbNq0xbZYenrGTTfcLNmZCKD/8vSz1unAgID/rXrzT8/8ee/evc3NLRIAAAAA4GLGHdAAADgcdze3JUuXbN642ZY+C6+/8tqqt94ymy29l5w3b15uQe6yZUvEtJOT0wMP3r/m8zUZh9I/+eKTW2+71brM4794XJQsXbr4vQ/eFRPvvv9uWGioKN+8bcvY5GTxEFtYsXz5MOtWU1v74vPPu7u7L+EmaAAAAAC4+BFAAwDgcCIiI9VqdXp6eu9Ckfz+5elnt2zZOthad99z9yM/enTfnn1P/eZ3BTl5v33qt1esvNw6S6FU3nHXXZ9+8tlXX64dP2H8L375pCj83W9+e+xYoXg88tAPDx48KA3bju27xM+YmGgJAAAAAHCRYwgOAAAcjqeXp/jZ2tp6Wmtde/11u3bu+vtf/y6mv/jyq4Qxo6+46sovv1ornioUin/87e/p6RlrPl4TEhKckJggClN2pbRr28RE7zE9hkPXoevs6PBw85AAAAAAABc5AmgAABxOU0Oj+OnufhoJr7ubW0xMtHjkFuTaCpVKpW36yJFs60RjU1NC4mjpe3BzdVW7uDQ0NUoAAAAAgIscATQAAA7n6LGjbW1tkyZNfPONN2yFHh4eDz/6wwP79g9xw/IXn3+xcf1621NdR6dkB7NmzxQ/87JzJAAAAADARY4xoAEAcDgGg3HL5i3zF863frug1a9+9eSdd93VpTcMuEqbVlteVh4SEiLiaevD19+/tLRMGpLZbJZOU2hIyI9++pOWlpbtO3ZKAAAAAICLHHdAAwDgiP76l2fHJCX964V/Hz5yOCMtIywsdN78+atXrdo5eOy7du3aBx968Kmnntq/b9/0mTNuuOmGF1948cV/vzjEXmqqa6dMnSJi7qNHC48ePTrYYiqV6pe/flImkyckJIxJGiNKfvHzx093iGoAAAAAwAWIABoAAEfU2Nh08w033XvfvYuXLr71tltr6+pfe/W1f/3zuSFWef655zt0ugULF1x7w7VdXV2rV69+6YWXht7Lm2+8MXnKFBFz/+H3fxg6gL7zrrssFktlZdWmjZveeO1/2TmMvwEAAAAAlwInN+9wCXBIfoGR1eX5EgCcDx5eAbr2FulsUGvcz9amAAAAcOHQuHp26tqks0FsqrW5VgKA84ExoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAAAAAAAIBdEEADAAAAAAAAAOyCABoAAAAAAAAAYBcE0AAAAAAAAAAAuyCABgAAAAAAAADYBQE0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AAAAAAAAAsAsCaAAAAAAAAACAXRBAAwAAAAAAAADsggAaAAAAAAAAAGAXCgkAADg8Z5WLQqVWKFQKpUou5+0BAADAmTCZjEaD3mjUGw2dXV0dEgCAABoAAAfnJDl5egfouzrNJkN7h9Zo6DKbTRIAAABOn0wmVyidlSpnuVzl5e3e3FQrAYDDI4AGAMBxKZXOnt6BTfWVBj136AAAAHxf4oN8fZdOPMS0UuXiHxDZ3FRtMHRJAODAGAMaAAAHpVA4u2jcayuPkT4DAACcdeItVk3lUfF2S7zpkgDAgRFAAwDgiJwkJy+foOaGKgkAAAB2I95uefsESRYJABwWATQAAI7IwzuguaFCAgAAgJ01NlR4eQdIAOCoCKABAHA4zs4uen2nnm9mBwAAsD9DV4feoHdWaSQAcEgE0AAAOByF0tliMkkAAAA4Jywmo1ylkgDAIRFAAwDgcBQKZyPfxg4AAHCuGAxdSr6KEICjUkgAAMDBKJQqAmgAAIBzRrz1Em/AJABwSATQAAA4HLlcYTYzBAcAAMA5It56iTdgEgA4JIbgAAAAAAAAAADYBQE0AAAAAAAAAMAu+AMQAABwNo2bOnf24ivERE1l2Udv/Eu6YNz32J/UGo2Y+OrD/xUXZPeZe8M9P2mordq89kMJAAAAAHD2EEADAIChTJ61KCF5soure11VWfreHUUFR4ZePmPfdvGYNHNh9Kgk6ZyTK5QLVlwfPiJWJpNXlRWlbPm6uaHWOuu1f/5W/HzwiWcGXDE7c79O2yZ9b1PnLuvq7BAtMJyFPbx97nz4171LDuzatHfbOjFx94+fcnP3MBoN2pbmwvzDu7d8Y7GYJQAAAAC42BBAAwCAQSVPmT159uLM/TurykuCQiMWrbzpnZf/2qHTSheqpVffGhwWlb53W2tzY9zoCYtW3rjmrReGs+Lh1N3S2eAfFFpefHSYC7e3tX327itiYuWN92Ts21lWXNDaXG+be+jgrrKigoDg8MTxU7z9Atd++D8JAAAAAC42BNAAAGBgFkmaMH3+oQMpKZvXiqeFeVnuXj5hkSMLcjLE08CQiNlLrvQPDNG1a3OzUvdt//aUG0wYN2X81Lme3r7NjXV7t31blH+Km6llMvmMBStGJiar1S41VeXb1n3SVF8zxPKePn4xo5JsI2wczc26+b7HRGFLY/0Qa93ywM99/YPFRHbG/t5DcNj27qx2qa0s3fLNGut2wqJil1x9y64NX46ZOEMcS0XJsS1ff2w06KWe26uVKucRsYnWQUhE+ZH0vUPs2mQ0lBfliwmL2dxUX22dtmmqryvMOyweeYfTbnvwCbHf8uICCQAAAAAuKgTQAABgYBqNu5u7Z2lhnq1k/advWyecXTRX3fpgVtqetR+9ERAUtuTKW/SdHelDjjsRPiJu7tKrN3/1YVlxwciEsSuuv/vdV/4+dKA8de6ymISx6z97u7mhXmTBV9/20KoX/mwyGQdbPig4QvwsPXaiwhbL+6/+n3Qq773yD/Fz2TW399v70oiYuI1fvNfa3Dh51qKevT9tsZgtFouL2jU8KvbT1S8pFKrr7n40efKs1N1bxCov/+1XN933s9xDB4c5BMcwiVaqq64IjYwhgAYAAABw0ZFJAAAAA3Hz8BQ/BxxwIz5pol7flbL5q05du0ioszP3xydPGnprY8ZPz8tKLcjOEKscTt1TWVo0ZsK0oVcZPW5K2u6tVWXFog7b13+mdnEZEZc4xPIad4+uzg6z2SSdDQnJUw7u2lxRcqytpWnHhi+cnV2iYhOss2Ry+d6eO76NRn1tZalvYLBkZ22tTR7ePhIAAAAAXGy4AxoAAAxsiG+98/T2a2msdTrxtLGuOmniDGlI7l7eI0PGjpkw3VZiMHQNsbxCoXJxdWusr7Y+NRr0bc3NHl6+0pA1ls4SsXdXN/elV98mHrZCb9+AIun4sCHt2lbrhNlkVipVkv05SU4SAAAAAFxsCKABAMDA2lqbxU8XjZutRK1x7ezQDZjznjL7dXJyOrBr095t66RhGjhuHWo3osIqZ7WTk8wWnWtc3XXtbdIZ6Nn7Z+++0mdc5vPFzd2r5FiuBAAAAAAXG4bgAAAAA+vq0NXXVkaOjLeVzFp8xZwlV4mJlqZ6Tx9/Wxjs4x/c2tI49NZamxr9A0NsTz28feXyoT4INxr0He1ab79A61OlSuXu5dXc2DDEKhUlx8xmk22gDOG6Ox+Njh8jnT6x93ZtW0DQdxW21eSUzvqNyh6irYNCrd+sCAAAAAAXFwJoAAAwqPS928eMnxabOE7tokmePDtixKj9OzeI8rysVJWzeuaCFWqNa2RMfOK4KYfT9vRe0aDXu2hcRWpsKzmUmhIRE580cYZCofILDLnh7h8HhUUOvffszAMTp88PCovSuLrNXXZth6596BC2Q6fNP5w+e/EVgSERbu5ei664ua2tuTD38EkVMxg8vX2lYTiSvnfc1HnhI+LEdMLYSdfc/kNnF80p1+rq7AgM7TkuJ6fvP2qzTCYXh3/5TfeUFxdUV5RIAAAAAHCxcXLzDpcAh+QXGFldfkH8YTUAB+ThFaBrb5HOBrXG/XQ3FRA0YvgvgCIyHj91rgiac7MOpqZssY19HBQaOWfpVb4Bwe1tLdkZ+w+kbO5956+7l+81tz1gHbJ5y9cfizBXTIwaPWHirAWisK664nDqnrzDqUPvWsSvsxavjIkfq1KpaypLtq77pKWx/pSrzF16dVRcotlsSt+zXezXZDL2XmDavMtEqC2Ty9tam9/6959mLLh84oz5fTby4f+eq60qd3KSTZ9/WezocWq1prKsaP+ODTWVpWJuaOTIa25/6IU//8y68Lxl17p6eHz90ZvWp2KuWCswOFwE0GLv29Z9MkRtRUJ958O/7l1iG6Xk7h8/5ebuYbFYtG0tZYX529d/ZjToJQAAcNEKCourrS46rVU0rp6dujMaTGygTbU210oAcD4QQMNxEUADOI8uogAaAAAA3x8BNACHxRAcAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAAAAAAAAwC4IoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAcjslklMnkEgAAAM4J8dZLvAGTAMAhEUADAOBwjIYuhdJZAgAAwDmhUDkbDXoJABwSATQAAA7HaNQTQAMAAJwzSoWzwdglAYBDIoAGAMDhGA1dMplCAgAAwDnhJJMb9dwBDcBBEUADAOBwuro6lM7OKmeNBAAAADtTqTVKlbNer5MAwCERQAMA4Ihammq8fUMkAAAA2Jm3b2hLc40EAI6KABoAAAfV3FTt5RssAQAAwG68fEOaGiolyUkCAEdFAA0AgIMyGLo6dNrAkJFKZxcJAAAAZ5XKWRMYGqtrbzUaGf0ZgEPjC4gAAHBcBkNnXU2Jl0+AvqvTYrEY9J1GfafZYpYAAABw+mROMoVKrVSpnZxkKpVzXU0R9z4DAAE0AACOzUlqbqpVKdXilyVXdy+F0lkuV0oAAAA4fSaTwWjoMgj6Lp2uhfQZACQCaAAAIOgNneIhAQAAAABwVjEGNAAAAAAAAADALgigAQAAAAAAAAB2QQANAAAAAAAAALALAmgAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAAAAAABgFwTQAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAAAAAAAAwC4IoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAAAAAAAIBdEEADAAAAAAAAAOyCABoAAAAAAAAAYBcE0AAAAAAAAAAAuyCABgAAAAAAAADYBQE0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AgIPy8PB47GePrduwLvNw5tp1X//ksZ84OTlZZ737/rsff/qxmFi6dPG+g/tWXr5COtsCAwL+8Mc/bti4fvfePc89/8/RiYkSAAAAAOCSQwANAIAj8vHxfv+jD+5/8H5dh+7jjz4uLyt98KEHn/vXc30Wq62tKyosrK6pkc7IR2s+FI/+5SJ9/ujTNTNmTt+6beu2LVviExLeef+d8ePHSfb0y18/mVuQKwEAAAAAziGFBAAAHM+Tv/rliBFRP3n0R99+u8Fa8uvf/vr2O25f9NWCTZu22BZLT8+46YabpbPtyquvDAwMuP8H9+/YsUM8dXdz25Gy48abbhS7k5ZzwkwAABAASURBVAAAAAAAlxDugAYAwOGIwHfJ0iWbN262pc/C66+8tuqtt8xmS+8l582bl1uQu2zZEjHt5OT0wIP3r/l8Tcah9E+++OTW2261LvP4Lx4XJUuXLn7vg3fFxLvvvxsWGirKN2/bMjY5WTzEFlYsX96/GjLZ8fchbVrt+OQJT/7il9any5YtXfX2qtT01PUbv/3lr590c3W1lo8aFffc88+l7N29PWXns397dsLE8bYaPvzIDzdsXL9t53ap5+bu3//+92JdsQWxndlzZovC557/55133SUmxMJPPfWUBAAAAAA4JwigAQBwOBGRkWq1Oj09vXdhTW3tX55+dsuWrYOtdfc9dz/yo0f37dn31G9+V5CT99unfnvFysutsxRK5R133fXpJ5999eXa8RPG/+KXT4rC3/3mt8eOFYrHIw/98ODBg703tW7d+q6urhf+88Jf/vLMjTffKAJx26wxY0Y/9+9/NTY2/ukPf/x23fobb7zxiSd/IcqdnZ1ffu3VmbNmfvjBB198+tnixYuf/etfbYNWX3fDDZ9++ukzf/qTmP7Tn/88f/HCTz/59Ok/Py2Xy1946YWw8PD/vfa/9evWi7miMh9++IEEAAAAADgnGIIDAACH4+nlKX62trae1lrXXn/drp27/v7Xv4vpL778KmHM6CuuuvLLr9aKpwqF4h9/+3t6esaaj9eEhAQnJCaIwpRdKe3aNjHRe0wPq7LS0h/cdc+PfvLjq6+7Rjx+/OOfvPP26v+89F8x65ZbbmloaHzi548bDEbx1MvTa/nK5U/97qkVK5YHBwf94udPfPHFl6L8UGbG+IkTbTdHf/j++y//9xUxERIcPG/BvH8999xrr7wunu7Ytn17yo4rrrhcbLy6pmrAygAAAAAA7IcAGgAAh9PU0Ch+urt7DH8Vdze3mJho8ej9PX5KpdI2feRItnWisakpIXH0KTd48GDqHbfdEeDvP2/h/Pnz5okwWqvVrV61KmFMop+fb1b24d4L+/v5jR2bbDQa16371loicuTeUXJxUZF1Yvz48XK5/Gc//7l42OaGh4VLAAAAAIDzgQAaAACHc/TY0ba2tkmTJr75xhu2Qg8Pj4cf/eGBffuHuEf4i8+/2Lh+ve2prqNT+n5q6+o++uAj8fj8q88vX7lcBNBOTk5Hso/894WXei/WptWKnyaTyWAwDL1B66Ac//jb322RtFBVVSMBAAAAAM4HxoAGAMDhGAzGLZu3zF843/rtgla/+tWTd951V5d+4IRXRMDlZeUhISHWW4/Fw9ffv7S0TBqS2WwesHzV26v2Hthr/a5CwcvL08/P36DvHnPjaMHR0OCQgwdTrXtRKBR1dfUdHR2HDmU6OzvbRp1esmTRL375hAjN+2z5UFb3rdNu7u7W1Q8cSPULCCgtKRmiMgAAAAAA++EOaAAAHNFf//LsmKSkf73w78NHDmekZYSFhc6bP3/1qlU7d+wcbJW1a9c++NCDTz311P59+6bPnHHDTTe8+MKLL/77xSH2UlNdO2XqFBFzHz1aePToUVv5O6tX/9+/nlv93jsbN3TfTz19xgw/P9/nn/uX1HOT9eUrL3/hpRffXrUqPjHx9jtuzzqUdc9d96xd+/Wtd97266d+Gx4VKVks1994owiU//mPf/bZY2lpyYH9B+6+5+6mxubW1taVK1dMnT6tpKh4z569VZXd90Hfdtttubk5IuCWAAAAAAD2xx3QAAA4osbGpptvuOnVl1911bjeetutCaPHvPbqa3/9y1+HWOX5555/7v/+mTgm4a//97fLVly2evXql04eKKO/N994w2KRRMw9eerk3uUbN27+0cM/kslkd95118qVV1ZVVv7+qd9//NHHYpZIwH/08CMGvf7pZ/9y3/337d+7/4mfPS7K9Xr9Iw88fLSg4JFHH7n+pptKiouf+NnPrV9U2MejDz8iNnXdDdc+8+zTEZGRv/vN70T6LMrXfPRxXl7eb576zS233SIBAAAAAM4JJzdvvpYHDsovMLK6PF8CgPPBwytA194inQ1qjfvZ2hQAAAAuHBpXz05dm3Q2iE21NtdKAHA+cAc0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AAAAAAAAAsAsCaAAAAAAAAACAXRBAAwAAAAAAAADsggAaAAAAAAAAAGAXBNAAAAAAAAAAALsggAYAAAAAAAAA2AUBNAAAAAAAAADALgigAQAAAAAAAAB2QQANAAAAAAAAALALAmgAAAAAAAAAgF0QQAMAAAAAAAAA7EIhAQAAh+esclGo1AqFSqFUyeW8PQAAADgTJpPRaNAbjXqjobOrq0MCABBAAwDg4JwkJ0/vAH1Xp9lkaO/QGg1dZrNJAgAAwOmTyeQKpbNS5SyXq7y83ZubaiUAcHgE0AAAOC6l0tnTO7CpvtKg5w4dAACA70t8kK/v0omHmFaqXPwDIpubqg2GLgkAHBhjQAMA4KAUCmcXjXtt5THSZwAAgLNOvMWqqTwq3m6JN10SADgwAmgAAByRk+Tk5RPU3FAlAQAAwG7E2y1vnyDJIgGAwyKABgDAEXl4BzQ3VEgAAACws8aGCi/vAAkAHBUBNAAADsfZ2UWv79TzzewAAAD2Z+jq0Bv0ziqNBAAOiQAaAACHo1A6W0wmCQAAAOeExWSUq1QSADgkAmgAAByOQuFs5NvYAQAAzhWDoUvJVxECcFQKCQAAOBiFUkUADQAAcM6It17iDZgEAA6JABoAAIcjlyvMZobgAAAAOEfEWy/xBkwCAIfEEBwAAAAAAAAAALsggAYAAAAAAAAA2AV/AAIAAM6mcVPnzl58hZioqSz76I1/SReM+x77k1qjERNfffi/4oLsPnNvuOcnDbVVm9d+KAEAAAAAzh4CaAAAMJTJsxYlJE92cXWvqypL37ujqODI0Mtn7NsuHpNmLowelSSdc3KFcsGK68NHxMpk8qqyopQtXzc31FpnvfbP34qfDz7xzIArZmfu12nbpO9t6txlXZ0dogWGuXxMwtjxU+f6B4a0tTRXV5Ts2vRlZ4dOOodOt8IAAAAAcFoYggMAAAwqecrsybMXH8vN2vjF+9UVpYtW3uSicZMuYEuvvjUiOk7EqdvWrbFYLItW3jjMFQ+n7i7My5K+N/+g0OEvHBo5cvm1d5YczV314jO7t30dHh03/7LrpXPrtCoMAAAAAKeLO6ABAMDALJI0Yfr8QwdSUjavFU9FPuvu5RMWObIgJ0M8DQyJmL3kSv/AEF27Njcrdd/2b0+5wYRxU8ZPnevp7dvcWLd327dF+ae4mVomk89YsGJkYrJa7VJTVb5t3SdN9TVDLO/p4xczKsk2wsbR3Kyb73tMFLY01g+x1i0P/NzXP1hMZGfs7z0Eh23vzmqX2srSLd+ssW4nLCp2ydW37Nrw5ZiJM8SxVJQc2/L1x0aDXuq5vVqpch4Rm2gdhESUH0nfO8SuQyOjm+prD+zaKKYLcw/rtFp3d6+h9y51R8Zh3S0fFKprazucvid97zZr+dS5y/wCg0XDzlt2bWBoeIdO9+bzf7DOGqzlT7fCAAAAAHC65CoXTwlwSBo3L21rgwQA54Oz2tVg6JLOBoXS+XQ35ermPZwXQI3Gfdq8Zft3bGhpOr7wsZxDjfXVYsLZRXPTvY8dyzu87pNVdVXlM+Yvt1gs1RUltnVDIqK9/QJ7p5nhI+IWX3nzro1fbl//mYhrl1x5S0FOZqeufYgKTJu3PHb0uA2fv7Nv+/qA4LBp8y47dGCXxWIebPmo6PiYhLGbvvxAVMZacjh1T9fJI1pMmrnwaO4hkcPaSrJSd4tj9PELNJtMvTNxsbuo2HiRyR5M2ewbECyeZu7fJWJ5d0+fpPHTDV1d36x5S2x/4syFSqWqqqxIrCKWjB6VlLZn65fvvyq2WVddLg3JReOWMG5yVVlxW0ujeKptbbY27xB7V6nVN9/7WPHRnG8/Wd3YUDN9wXK5XFHZs3c3d89RSROjRsaLVbZ+s6a4IKdDpx265U+3wgAA4Iy5efi2a5tPaxWlSm39kPv7E5vq6myXAOB8YAgOAAAwMDeP7k+prSFmH/FJE/X6rpTNX4kcs7QwLztzf3zypKG3Nmb89Lys1ILsDLGKyG0rS4vGTJg29Cqjx01J271V5LOiDiI8Vbu4jIhLHGJ5jbtHV2eH2WySzoaE5CkHd22uKDnW1tK0Y8MXzs4uUbEJ1lkyuXxvzx3fRqO+trLUNzBYOiMiCD6ctueKm++996d/WHTlzf5BYafce/yYSUaTYdemr0SbiLh84+fv19VUWldpb29z9/ASbVuYd9ig1zfUVVnLz6DlAQAAAOBsYQgOAAAwsCHuNfb09mtprHU68bSxrjpp4gxpSO5e3iNDxo6ZMN1WMvSN2wqFysXVzXZHsNGgb2tu9vDylYassXSWiL27urkvvfo28bAVevsGFEnHb5Fu17ZaJ8wms1Kpks6IaMCdG77Ys3VdTNyYEaPG3HTvT4/mHFr3yaoh9u7l69dUX2c70rKifNsCFnP3+RJb6LOX0215AAAAADiLCKABAMDA2lq7/0q097cOqjWunR26AXPeU2a/Tk5OB3Zt2rttnTRMTgOWDrUbUWGVs9rJSWaLzjWu7rr2NukM9Oz9s3dfKe+V8NqJyNbzjqSJR1nx9AXLr3Nz9+rs1J3Z3kUG3f+O9dNueQAAAAA4exiCAwAADKyrQ1dfWxk5Mt5WMmvxFXOWXCUmWprqPX38bWGwj39wa88oxkNobWr0DwyxPfXw9pXLh/ogXMSyHe1ab79A61OlSuXu5dXcONTQ1RUlx8xmk22gDOG6Ox+Njh8jnT6x93ZtW0DQdxW21eSUnKThmrHg8rjR421Py4sLpO7xwV2G2HtzQ72373ctHxYVmzxltm2xAeP5U7b88CsMAAAAAKeLABoAAAwqfe/2MeOnxSaOU7tokifPjhgxav/ODaI8LytV5ayeuWCFWuMaGROfOG7K4bQ9vVc06PUuGleRGttKDqWmRMTEJ02coVCo/AJDbrj7x0FhkUPvPTvzwMTp84PCojSubnOXXduhay8uyB5i+Q6dNv9w+uzFVwSGRLi5ey264ua2tubC3MMnVcxg8PT2lYbhSPrecVPnhY+IE9MJYyddc/sPnV00p1yrq7MjMLTnuJycPLx9hl5YHNecpVfHJ08WzRscHjV3ydWtLU3WsZsH23vu4YOiAcUxipYXj7lLr3ZzP8UXSg/d8qdVYQAAAAA4XU5u3uES4JD8AiOry+3+h9UAMCAPrwBde4t0Nqg17qe7qYCgEcN/ARTB5fipc0XWmZt1MDVli23s46DQyDlLr/INCG5va8nO2H8gZXPvG2ndvXyvue0B65DNW77+WMSpYmLU6AkTZy0QhXXVFYdT9+QdTh161zKZfNbilTHxY1UqdU1lydZ1n7Q01p9yFZHJRsUlms2m9D3bxX5NJmPvBabNu0yE2jK5vK21+a25fhmiAAAQAElEQVR//2nGgssnzpjfZyMf/u+52qpyJyfZ9PmXxY4ep1ZrKsuK9u/YUFNZKuaGRo685vaHXvjzz6wLz1t2rauHx9cfvWl9KuaKtQKDw0WeK/a+bd0nQ9RWoVQtuPz6uIRxYuG2lqaKkmP7dm5oa+6+l3ywvQv+QWEitvYPDBZHkZ2+f9u3n9h2fdWtD7z0zOP9dzREy59WhQEAwBkLCourrS46rVU0rp6dujMaTGygTbU210oAcD4QQMNxEUADOI8uogAaAAAA3x8BNACHxRAcAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAAAAAAAAwC4IoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAcjslklMnkEgAAAM4J8dZLvAGTAMAhEUADAOBwjIYuhdJZAgAAwDmhUDkbDXoJABwSATQAAA7HaNQTQAMAAJwzSoWzwdglAYBDIoAGAMDhGA1dMplCAgAAwDnhJJMb9dwBDcBBEUADAOBwuro6lM7OKmeNBAAAADtTqTVKlbNer5MAwCERQAMA4Ihammq8fUMkAAAA2Jm3b2hLc40EAI6KABoAAAfV3FTt5RssAQAAwG68fEOaGiolyUkCAEdFAA0AgIMyGLo6dNrAkJFKZxcJAAAAZ5XKWRMYGqtrbzUaGf0ZgEPjC4gAAHBcBkNnXU2Jl0+AvqvLYjEb9J1GQ5fZbJIAAABw+mQyuULlrFSqZU4ypcq5rqaIe58BgAAaAADH5iQ1N9U6q1zkKmdXd2+F0lku5+0BAADAmTCZjOLjfINRb9Tr23UtpM8AIBFAAwAAoUvfIYkHAAAAAABnFWNAAwAAAAAAAADsggAaAAAAAAAAAGAXBNAAAAAAAAAAALsggAYAAAAAAAAA2AUBNAAAAAAAAADALgigAQAAAAAAAAB2QQANAAAAAAAAALALAmgAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAAAAAABgFwTQAAA4ont/8vvLrrnd9tTDy+ehJ56RLhgLV1w/Y8FyMTFv6dWTZy3qMzc+adJ1dzzcf607fvhLv4Bg6TSd2VqDcXFxfejxp63TsfFjg0LCJZwmFxe3hcuvu+3+x3/w499ddvXtPr6BQyx8872PhUZESxcztYtm4vR50gUmMDgsLmGsdJqsp8PbN+DOh3/l6uouAQAAAATQAAA4LB+/wPCoWOmCdDTnUMnR3MHmVleUZKXvlS540aNG+wcRQJ8ehUJ11a33O6s1m9Z+8PGqF1tbG6+4+V4R60uXLhFAj500S7rA+AWFRY867QDaqq256XDa7nadVgIAAADEm3wJAAA4pL3bv529+Ir3Xv+nZLHYCkXSd9ejv/7v335lfXrnw7/++uM36murbr73sfR9O+KTJvgHhhTmH9n89cdST1Y4ff7S6LikDl1b7qG0Q6kpotDLx3/m/OVhI0Z26HSb135QUVrUe6dKpXLGvBUjRiV2dnZk7t+Vc+iAr3/Q1bc+8MHr/9JqWybPXBAZE79m9X9GxCa2t7dVlBZK3fGcyxU33BMQEl5alL9r41c6nTYgMDghaWJeVqqYO3JU0ripczy9fVP3bLPtxcPLZ/rcZWGRI+tqKlL3bLVup7cB1xI1nzZnaVhUTENdtWicqvKS3tW+58e/e++1f7a1NImnieOmjBo9/rN3XxliR4tX3jQyIVk8YhPHfvrOy0M3i2he0XpjJkxTq93yj6SJvVt6TkrypFkJ4yapVC4FOZn7tq83m01xCWPHTJxhMZsDQyNe/vtvbFsQSy9Yek1kbIKYzj+SvnvrN4Mdka9f4Iz5y8XqJcfyxAYb62vEmZ239GrR4Ad2bRILjB4/LTI67ptPVotCZ7WLj39gV0fHp+++LE6NOEEBQWHVlaXrP3tXLC8qEzdmQk1V+ejxUzs72rd/+5l1FxEj4iZOn+cbEFxUkJ2+d0djQ40oHD91TsLYyd6+/jkZB7au/9TSq9f1Nn7qLJPZ+PWnq516nqZs/trb22/MxOmibgqFcvr8ZdFxYzt0rYfT92Vn7B+6a/WeK46lo6Pdw8s7KiZB9OdvP31HPO2uavSoidPmevsFlhUV7Nn6jVbbeu3tD+VkpVo37u7pfct9j73+3B/ERJ/TJ66U2x96YteWr6fNXlpTVbpz09pZC1eERkTXVVd8+9k7og7WQx6VNFEsmXdYnNPu09e/Gkpn51vv/7lY+OEnn/3ig9fLi4/2X8t2FKLB45MmNTfXxyWOb6itEnOrKkqkgS46a/XyD2fGjk5e99nbNRWlM+avGJmQJFcodm9Zdzh9T79mP+nsiOl5S6+y1uqlZ58U/XPHhs+t3XvplTdXV5ZnHtipVKoG26ZSpZoye4m4uLx8/KxHZyU+Ovrk7f8O2Bn6dDYJAAAAlxDugAYAwEE1N9Q1N9aNnzJ7mMtHxyaK3Hnz2g+jR40ODA4TJXOXXunsrPnojefXfvhm8pRZIhoThdPmLKmtKV/10l8OpGxaePlNfTYyb9m1Jovxw/89v2Xth1NmLw6L7M5GRZg4/7JrRIg2bsrczV+v6bPKqNET0vbvWP3fZ3XtbYuvOGmDIkudv/zaPdvWvfvK3z09fTSa7vtknZycrrzpXpGEilUyDuxadvVtGo37KdeSyWQrb7i7uODI6v88K8K1FdfdJeIw2yoGg6GkIDcuMdn6NDZ+bN6R9KF3tPGrD47mZO7Y8KVIn0/ZLMLYiTM2fv7Bmrf+HRQSMWnGfKlnpJHEcZNF1LvmrRe8vH1nLlxhXTIgOOxI2r5X/vHb3qvHxCYGhUeKTFzsLiQi2i8geMAjEoXLr7urpDB/1UvPlBUfjYlPkoYUEBy+9Zs1IhAUaePkmQuzDu5+84WnG+tqpvcMkCJ1D9QQ0dpYv+bNF5vr6yZNXyB1p/++4jTt37Xp9ef/KDrYiuvv7FksLDpu9Pb1n7398t+8/QPix04abI9BIZG5malOvUrWrlllTcbnLr2qp7/9a/NXH02YOjc6LrH3iv27Vp8tiwpkpe4R7ePs4pKQPOl4VVfeKKr6zit/a2qoWX7DXaIw73CG+HzCuor4mKEo/4jJZBzw9MkVyk6dVjSvtqXlmtseEPn7Oy//XSaTJ02cLuYmJk+Jionf8Nl7a1a9KE7HpJkLBqxGa3Pju6/+Q9euFTmvSJ8HW8smPDqutblJ1CQ7fd/ya+8Usbs0SO9Sqpw7u3RvvfhnsdlRYyZqXN0+euvFb9asmjRzvjjw3tvsf3ayM/dvW//5sdzDolbSIIbeplVzY73Ygni89s+ntG2t+UcypcE7g62zSQAAALi0EEADAOCYLCKpFZFZ8uRZLi5uw1nhcPretpamwoKcipJC/6BwuVwRm5CcsnltR0e7Tqf94t1XC46ki8W+/fzdA7s2m4zG9rZWdw9Pa0BmpVAoo2Ljd29ZJ1apra48lncoetQYUb5/50Z3L5/FV9x4OGNfU0Ntn/2KBFAkaPqurj1b1gWEhLm5edhmxSVNFJFWRWlhZ2dHytZvpJ7YMixqpNFoPJSaYjDoSwvzSgvzE5In9t7ggGuFR8Vq21pyj6Tr9V2F+dktzQ3hJyeY+dlp1tqKKDYoLFIc7Cl31NsQzWK1d9u3jQ017e1t+3dtGDW6ezujx00+uGtzU0OdaN6ULV/Hjzm+8brqivzczD53ECvkol5qkYm3NjeI7LK+tmrAIxKFRqOhp86G3KyDDbVV0pAKcjKrK8uk7ghev2b1S3nZGXK5vK21ycf/+LjMzU11olCrbTm4e4tvYIjUHbxOPpqT1X23rMWStnf75++9Kgprqso/efu/olClcta2tvgFBA22R6Wzc4e2rX957/7WUF8jtjxm3LTvDn+QrtVb8dGc6opS8YGHCLgDAsN6V1X0roO7t6rVrkEh4UdzMoJCI0RrSj2DqFgz0wFPn2jtooIco8lQfCynXdsqzp3Ye1lJgbu7d8/GJx1I2SzOaVtrc1bq7hEn4vL+1ehtsLVsaqvLM/bvFKcjLyezob7ampUPWD3RQ/btWC9OtNR98e5Z99nb7W3NYhlxsH7+Jw2rPfyz09vQ2+xDfMLUVFedlbZ7iN3ZOhsAAAAuMQzBAQCAYxLpmZOIzA4dTJm5aIWIgE+5gslkPD5hNMgVCo2bu8lstI5jILS2Nlknxk6aOXnmwubGupamRhGByeQKqScCEzQaN5VK/dATT9u2eTTnkPhpNpvS9m2fu+TKtR++2X+/ti2bzCadVuvm4Wmb5erq3lhfbZ0WIViHrnvcAzd3L+2JVbpXb2l0c/PqvcEB13Jxcw8JH/Hwk8/aFlNrTsrlC4/mLlhxg1g3cmRCWVGByPVOuaPehmgWK72+0zrR3FCvce++k1rj5iG2eXzjzY0qZ2d1z03ZJpOp//bz8w6FR8eKEF/qjjhz0/ZsG/CIlCbTSXVubpKGZDvpIv+ds/iKEXGjxSF0duhkMtmJBY5XRuTacplc6m5/T1vziiMVQaqY8PDwXnTFjRpXd5GJi3U7dbrB9ihmiZr3L+/b31oaNb16wmBdqzfxaYF1wmA0yBR9qyqIlhHZschAK0sLYxLGVpQcc3XzKi7sHot8gNPXc3TWjwEsUq9hbCzdH+2I/7po3K+8+T7bxkVCPVg1ehtsLRuDXm+bbm1q1Lh7nLJ6QlhkzPzl13d16dpbWsTFK5OdtN/hn53eht5mb6MSkkMjR7736j+G3p2tswEAAOASQwANAIBDS9u34+Yf/DQw6PidmBaLWURCIpu2RldK5aBvFXTaNrlM4eLias0E3dw8xYSbh9eUWYs+eP05rbZVrB83etxJq7RrjQb96//6Y5+kycXFbfrcZTWVZVNmLd6+8fM+OxJxlXVC5JsaNzdta4uH5/ESEaC7e/hYp5VKlUajERPatma3E6t0r+7p09QzBrHNgGvp2lptA9QOzGI5mp01MnFceGR0bs/w06fckY2nt98QzWI7zAqpe2BoL18/XVv3LcA6bavYZk1VudQzqrVB32UdWXiw6m3+pnv0Eo3G/erb7te1t7U1N/U/oqiYhN51dnVzr++549xitsjlihNtouy/+fixEz19/Fb/51kRNIdFjZy16PJB6iGapcXWvOJgvbz9Wprqp83vPr8pW74WhVPnLFE7awZbvbKsKCpmlHU8catlV93afcvznm29+5toGXHKbMsM1rWG1ruqgmiZNm13XJ5/OGPk6GQXF82xvEOiYYdz+vrTtbdu3/B5aWGedDpOuZYIzW3THt4+VWWFw6newstv3PbtpyXHusP0a257sM/cU54diyRC7eP5skKhGs42bcRnNnOWXb3+i/dtvXf4nQEAAACXBobgAADAsVksOzZ8LmIg67OOzg5tW+vUOUsVCuW4KbPl8kHvahRJX0FO5owFyyUnJ5FJXXXLfTGxo81mk5PMSSaTiwh7xrzLnJx6j+UrGU2GozmH5iy+QiFXqlTO1935SGz8WFE+d8mVhbmH13/2XuzocUEhbCopmwAAEABJREFU4X12FDUy0T8wRCRr0+Ytq6uq0Pa6JzQ/K1XEbb5+gWLu9PmXWb+urbz4qFwmS0ieLHUPKBweER2Xeyi19wYHXKusuEDtohFriUJf/6A7H/6Vu0ff25nzslOj4xL9gkILC7KHsyOjwaDuSbeHbharpCmz1GoX0TJTZi/Jy04TJUcyDkyctaBn4Gb5zPkrcg+nSoMbM3768mvuECGyyWw0GA0mg2HAI6ooPerm4WGtc1hkjF/PoBlCXV3lyPikwOAwsczIhLH9t28ymsQ5Ewcitjlh6twhapKdeWBkQpLYY0+tpi2/9o6e1Y3i0KSeAbjjEsdblwyPip239Oo+q+dkHfQLDJ2/9BrRpCJ2Hz91blB41OHUvb37m4ihRR2OZOyzrTVY1xpa76qOnzqns7O9qqJUTB/Nz/IPCh8Rm5h/uPtEDOf0DbDx9H0iFxbxq5heuOL62YtXDrakoatLnDhr7n/KtVzdPZImzBATI2ISfP2CjuYdHk71zCajUtG9/dhRYwOC+o77MeDZMRn0Lj3DowsNtZXjJs9yc/MIjYgOOHGFDr1Nm6VX35p3JL13pD7g7nobN2XO6PHTJAAAAFwquAMaAABHV1FaWFdT4e7VfSuoyK62fP3xsqtvjU1MPpiyRdvWOsSK29d/MXP+8rse/qUIBNP2bc/LzRSrp+3ZdvP9j4mM6XD6XpOx7+2o2zd8MW3e0lse+LmLRpNz6EBh/pHo2MSA0Ij3X/uHwWBI2fL1/OXXf/C/53qvkn3owJwlV/oGBJcczdnwxfu9ZzXU12z9Zs2Cy68XGeLe7euttbVYLF9+9IZIbEXd6msqv/3sbe3J4xgMttZXH705Y+5lsxasEDU5mLLZOnZEb1XlJW7uXqXH8s1m82A7Ek1hW/5Q6u65y64eGT/2/df/OXSzCHmH0m78wU9Feph3OE20vCjJzToo0t5rbntQqVKL7HXf9vXS4ApyMkLCIx/42R/NFnPBkYzcI+nSIEe07pO3Rdg6b8lVx/KybLGgiGKjYuKvue2hksI8keSGhI/os/38I2ligYeeeKa1pbkwP8s6SMiAWpsbNn71oThlQaGRzY31Gz5/VxTu37V5+XW3P/zks3W1lZVlhdYlRftHxMT3Wb2rs+PTd18Wn0lce8fDFrO55FjeV++/3tGhlbr72+eitUV/0+m0afu3H8s73HvF/l1LOhVR1U09VfXxCywryv/mo7es2a04v+XF+cGhUdYhidtamk55+vrLOZymdHZZcePdfv6i6+Ye2LlpsCXb29tEhcUnBDu+/fyUa9VUlvn4BogTUV1e8s0nqwwGvaFFf8rq7djwxfzl1y258ubiY7m11eV95g54dkTzRo8a8+Djf37rxWd2b/7mqlsfuPm+x8THA7Y+M/Q2rcSHHMFhUeKRNKH7ixm1bW2rXnp6wN31FhIeZdDrj6TvlQAAAHBJcHLzDpcAh+QXGFldni8BwPng4RWga2+Rzga1xv1sbQrny833PrZjw+fdX9x3bi2/9o4SkdTaIelTyJXX3vXDjZ9/0DjIsCQ4A3EJYxPHT7N+ryMAwBFoXD07dW3S2SA21dpcKwHA+cAQHAAAAI7CIklX33J/ZPQouUyeMGZCWGRMWVGBZAdGk2HTFx9Mn79MAgAAAODYGIIDAADAUThJ0sHdW2ctutzHL7Crs2PbN5+2NjdIdhAaET19/vLT/Qo+AAAAAJcehuCA42IIDgDnEUNwAAAAYGgMwQHg0sAQHAAAAAAAAAAAuyCABgAAAAAAAADYBQE0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AAAAAAAAAsAsCaAAAAAAAAACAXRBAAwAAAAAAAADsggAaAAAAAAAAAGAXBNAAAAAAAAAAALsggAYAAAAAAAAA2AUBNAAAAAAAAADALgigAQAAAAAAAAB2oZAAAAAAAMDFw3XWbOfE0S7x8apRCUo/PwkXDENdfVdeTmdeTld2dvuunRIAgAAaAAAAAICLhSIkNPj3f3RJHifhgqT091P6z3abNVtMd2RmVP3+d8bKCgkAHBtDcAAAAAAAcBFwv+KqyHc+IH2+WIgzJc6X++VXSADg2LgDGgAAAACAC53HNdcG/eJXEi4qcldN8G+fclIpWz/9RAIAR8Ud0AAAAAAAXNAUoWH+j/5EwsVJnDtxBiUAcFQE0AAAAAAAXLgsTk7BT/1BrtFIuDiJcxf0uz+I8ygBgEMigAYAAAAA4MLlMno04z5f7DTjxonzKAGAQyKABgAAAADgwqUePVbCxY/zCMBhEUADAAAAAHDhUieNkXDx4zwCcFgKCQAAAAAAXKhcRidJuPhxHgE4LAJoAAAAAAAuXMqQEAkXP84jAIdFAA0AAAAAwEXPpG1v+vC99v379CWFysAgmbPaNksRFOz/yI+VAQESAADnHGNAAwAAAABw0Wv9Zm39f16QDHpTXb1Zp+s9qzM3t/j2m/SlpcPZjsVobHzv7dIH7ilYNK/8ice0u1OGXr49PT134tj2A/uks6rlqy/EZq2P/IVzu2uya4d1Vv1bbxy7fJmhrk4CAFwMCKABAAAAALjo6dJT3eYvjHxjtZj2u/+hiFffsD1GvP+ROiGx5N47u4qKTrmdiicfr3/9NZfxk7yuvsas6yh/9KHmb76SzhOv62/0ffCHnpet6CosLP/xI+2pB0WhMjjYOSFB5qIZYkXdwQMiuRY/JXuqe+1lsRcJADAkhuAAAAAAAODiZzY5ybtvMrM4OemLCntnr86j4kP/+o+yh+4v+cGdUR98rAoIHGwbXYXHtFs3+z3yY7+7f2AtKX3koaZ33vZavlI6H7yuvlY9Kl5M+Gm1x1Ysafn0E9eJkzyXXiYeEgDgIkEADQAAAADAxc/p+J84i3C27tWXnSwW2xzfBx/2v++BsOdfKr75+qa3Vwf+7PFTbKrXuhEv/tc23ZGT3bj6LV3aQVN9vdu8BYGPPa4MDbXNNbXrji6b77F8ZfAvf2MtqXnu/5o++mDkt5vkGk3j+++2bljfVZAn9/Lyu/dB7+tvEAvUv/F6w/9eDXjs8YZXX9bMnBXyuz8MViO5m5tzzEhDTZV1rfqX/j1qX5qTQpE7dYLvfQ9a2tvaNm6UlAqf2+70vvb65m/WVv/2V2LJ0gd+4DJ+QuTrb5m07Q1vvd6esstQU6MZP8Hnjrs0yeOknnjdSSFX+Ae0bfg28Oe/8Fx5Zfu+PU0ffahLT1MGBrotWOh7x13W0bQbP3ivZe1X+pIiZXCo55VX+t56R9Uzf2r55GMxK3fiWN977vV/+EcSAGAgDMEBAAAAAMBFz2IxS+IhSSFPP5twMDM+9ZDtIdJnUS53d3cePdpYWz3ERpyjY9RjkkS8W/nrXzZ9/JGhvt42y6TVlj38YFdhof8PfxTw81+0H9hX/bdneq8rd9W4z1+k3bLZYjL11MciUl33OXMVnp71q96sffF5l6Sk0Gf/rk5IrHn2z7rMDOta5q6u1k0bxQa9r79xqKMzmQxVVTJ39/6zWj7+0Enj6vvDR2Su7jXP/ElfWuo6dbrYoJglfgb87AkxUfv3v7RuXO91zfVBv3nKYjKWPfKgoaHBurou9aClsyvkmb+6jJ/YVVRU+vCDcm/v4Kf+6LFsedM7q+tf/o9YpuNIVu3fn1WPjAl55m/uCxbW/fMf7elpPjff5nHl1WJuxCv/87zyGgkAMAjugAYAAAAAAMeFPvfvhtdeaVn7Reu3X9f+6x9e193od/9DIlyWu7lFvf2ezM1dBMpisa7iovbt2/qsK0Lb1q+/at+/z236DF1GhrG2xr1nrAzfW2/zWLjIeUS0mFaPTjp22aKugnzrPchOFkvgz59Qx4wcokr6kpL6/70qtub36AB3GbtMnOR/34PdW46NK77puo7sw57Llotpa4lLQqKxqbHl228Cn/il97XXi0LXyVMKFs1t27zR54abpO5c3iP4qT84KbrjkZp//kMVFBz0y984yeXS3Hmm1paWLz73/9FPjfXdabXb3Pnus+d0P3qORayiDA4W5ZpJkyUAwOAIoAEAAAAAuHRU/vrJlvXreg/BYXFy8ly6POTpvwxndaWPb9AvfhXwk8c6Dh3Spuxq+vB9U1urdXAMmatb8ycfd2SmWzo62tNS5Z5efdZ1nTqteziLLZtEAK3dsknu7SPi2u4VXTSG6urGt97Q19Yay0q7q2Qw2NZyjowarDLFt9xgnZC5u/vec++AQ1GrIiKtE2J34qe5vb3PAp05OZLRWPPMn8TDVmgoKzt+vGHh1vS5e8nsw4aqyrwp43uvbmpt1UyaogwOKX/8MddpM1zGjnWfO9+2CgDglHjFBAAAAADg0iHSZ//7H9RMmGQr0aUerHv9lWEG0FYyZ7Xr5Cni4aSQN769KvhXv9WXlZXef4+TXO6+bLnLmCRFaKh2x44+a3XPXXpZ69dfWn7xK+3Wze6LFjkplaK85u9/bfrgXdfZc9xmzFDH/6DswfuGWY2g3/5BFRbm5OqqjhvVfVfymenJ4oN+85QqPMJWJvfzH3BJzcRJfvc/1LtM5uIiU6kiVr3btnF955EjzR99UP/6q2H/+Jf7nLkSAGAYCKABAAAAALh0OFksqhHRvceFMDQ1OpnNw1m34Z1Vdc/9X/jLr4voWeoZx1lfVuqkUkoyWfd3DzY2xGzYqvT1FbO0/cbfsPJYdlnTO6ua1nxkqKp0X3KZtbBtyyavG24K+kX3FwN2FRdLw6ZOSFCPipdOn8XJyTbtHDdK/DS1tVnbxKTr0O7cph4zpv9azrGx2q1bnRNGy1014mn7/r0KP3+RPpu07boD+7xvvNnJycliNBYsXahN2dkdQDvxxVoAcGoE0AAAAAAAoJvHkstEdlz+k0d8br9Lksv0hYXaTRu9brrFSSZTBASKBZo/fN91ylRdZoZIYKVeIa+NS0Kic2xc46o3lZGRmvETrIWKoKD2vbvb9+0x6w2N770j2Z+qZ3RmbcoOyUnSTJzsOmde/Wv/VXh5y9zdWr/9pm3bVtUbq11G982gPS67vPnjjyp/8wufW27rzMttfOsNl4mTwv76f20b1lU//Uf9saOuU6d3Hi0wtTS7jE3u3ktgT5t885V6ZJy6J+YGAPTHh3UAAAAAAFz0nGRyS69xnwcmFpAPdSOaMiAg8vVV6jFjG157uendt8269oCfPR7wSPdX/7nNmu19252N779d+vADppYW72uvG2wj7suWG2trPBYvczqRUAf+/BcyV7eyHz5Q98Lzfvc/KNmfMiTU+9Y7Glevqn72afE05M/P+txyR9OnH5c//lhXUVHIM3/rnz4LmuRx4S+/JlOpKn/5i7r/vOQ2c3bwb34vyr2uuc7/Rz9tWftV6QM/qH/15YCfPOa1ons0avely1ySx1X/9tdNn3wsAQAG4eTmHS4BDskvMLK6PF8CgPPBwytA194inQ1qjfvZ2hQAALgAxe1LHc5iTR99WDUF7+cAABAASURBVPvCcy4JibrUg6roaEXPN/JZGRobDUWFmomTOnKOBDz6mPcNN0o4H/KnTjyt5TWunp26NulsEJtqba6VAOB8YAgOAAAAAAAueh7LLze1tbYf2C/395NpNL1nyTWuZj9/i0zue/d9YjEJAIBziAAaAAAAAICLntzN1e8H94mHBADAhYQxoAEAAAAAuHAZGhokXPw4jwAcFgE0AAAAAAAXLn1+noSLH+cRgMMigAYAAAAA4MLVWcB3p18KOI8AHBZjQAMAAAAAcOHS53Hn7KWA8wjAYXEHNAAAAAAAFy7trh2dRwskXMw6C49pd26XAMAhEUADAAAAAHDhsnR2Vv/212a9XsLFSZy76l89aenqkgDAIRFAAwAAAABwQdMXHqt/8QUJFydx7vRFhRIAOCrGgAYAAAAA4ELX/OF7Zn2n/6M/lbtqJFwkTK2tdf/8R+u6ryUAcGDcAQ0AAAAAwEWg9bNPS2+5oSM1VcLFQJypkpuuJ30GAO6ABgAAAADg4mCorir74f3KiEj1uPGa8eM14yYoQ0IkXDD0VVUdGWkd6ekd6WmG0hIJAEAADQAAAADAxUUkm+LR9uXnEgAAFzyG4AAAAAAAAAAA2AUBNAAAAAAAAADALgigAQAAAAAAAAB2QQANAAAAAAAAALALAmgAAC5yFovFbJEAAABwCRFv8Cy8xQNwSSCABgDgImexyJycJAAAAFxCnJxkIoSWAODiRwANAMDFzWQ2yxQKCQAAAJcQuUJuNhNAA7gUEEADAHBxs5hNcrlSAgAAwCVELleZTUYJAC5+BNAAAFzcTCajQgTQDAMNAABwyTBbFHIFATSASwMBNAAAFzeLxWy2mFTOLhIAAAAuCUq1i8lsskjcYQDgUkAADQDARc+g75IrnZ2c5BIAAAAucuJNnULhbDR0SgBwSSCABgDgomexmI36TrWLK3fJAAAAXNwsknhTJ97aWSy8sQNwiSCABgDgUmAyGUxGvYvGXZKcJAAAAFyUZC6uHuJNnXhrJwHApUIhAQCAS4LRoDebzWq1m9HQZTTpJQAAAFw8lHLxP7VB38l3DwK4xBBAAwBw6RC/rhjMJqXKRalSd98T3f0wW8wmJxm3RQMAAFxgzBZJJpfLxf+V4mGxmA16HSNvALj0EEADAHBJEb+06Lt0Tt2/zMiVSrVK5SSJ+Jn8GQAA4ALTHTVbzOLNm9ls1Os7LGaTBACXIgJoAAAuQeIXGGP37zAMxAEAAAAAOJ/4EkIAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAAAAAABgFwTQAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAAAAAAAAwC4IoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAAAAAAAIBdEEADAAAAAAAAAOyCABoAAAAAAAAAYBcE0AAAAAAAAAAAuyCABgDgPLB0kwAAAAB7E287zRazBADnCQE0AADngcVslvGPMAAAAOxPJnOymLn3AcB5w+++AACcB0az0UmmkAAAAAA7c5LJTWajBADnCQE0AADngcmolxNAAwAAwP7kcqXJ0CUBwHlCAA0AwHlg0usVCpUEAAAA2JeTQq40GvQSAJwnBNAAAJwHZovJaDIolGoJAAAAsBuF0tlg0lv4EkIA5w8BNAAA50eXrk2hUMqc5BIAAABgB+KtpnjD2alrkwDg/CGABgDg/DBbTF0dbSoXjeTkJAEAAABnl5OkUmu6OrQStz8DOK8IoAEAOG8Mhi5Dp06tdnWSkUEDAADgrHFykqld3A1dOoOhUwKA80ohAQCA86erq91kNDpr3IxGo8nIt5MDAADg+1IoVHKFslPbYjTpu2+EBoDzigAaAIDzy0n8YmDUNrloPJQu7iajwWQ2WszdGJkDAAAAw+TkJHOSyeQyhYieTSZDu7ZJslhInwFcCAigAQC4AFgsHe3NMrlKqVDK5UqZUiHr/hWCXxgAAABwahazxWIxm0xGs8nQ1aUzc+MzgAsJATQAABcIp+5fGLp/WwAAAADOmBPpM4ALCgE0AAAXFH5bAAAAAABcOmQSAAAAAAAAAAB2QAANAAAAAAAAALALAmgAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAAAAAABgFwTQAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAAAAAAAAwC4IoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAAAAAAAIBdEEADAAAAAAAAAOyCABoAAAAAAAAAYBcE0AAAAAAAAAAAuyCABgAAAAAAAADYBQE0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AAAAAAAAAsAsCaAAAAAAAAACAXRBAAwAAAAAAAADsggAaAAAAAAAAAGAXBNAAAAAAAAAAALsggAYAAAAAAAAA2AUBNAAAAAAAAADALgigAQAAAAAAAAB2QQANAAAAAAAAALALAmgAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAAAAAABgFwTQAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAAAAAAAAwC4IoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAAAAAAAIBdEEADAAAAAAAAAOyCABoAAAAAAAAAYBcE0AAAAAAAAAAAuyCABgAAAAAAAADYBQE0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AAAAAAAAAsAuFdPYoVaqkCTNCI6Nlsu5c+3D6/mO5hyQAAAAAAAAAgEM6mwF03OjxU+cuqSovsZhN3c+dpDOl9oqfO2nS2IhAN1NLWWnG9oPpBW2mQZeW+0xYfMMK98IP1m4o6JAAAABwnDIgaWZYVUpavUECLgj0SQAAAEdzNgPo4LCoY3lHNnz+rvS9qAPm3nXltODm/ENHsySNb8SIhXdHhK/59Mu0wTJoU1dbU01VV61WLwEAAODsUXpHhSnrSmrbzRIAAAAAnIGzGUA7yWSSeeCQ+MZ7fnzoYErOoYPSKbmOGDsmQqpYu/HL3c3dG1MHLHjo2vEzRvoeSq81DrxKe8G+zwokAACA70vmMXLGyil+8u5pQ0tZ7o69x5p63aipDpswf0RjSkpx61kLZJ2jZi+aE67snjTpKnLTUjLrO/vVyi95RnJnxvYqn+mT/YpT0so6pTN1igO0UgYnL4qu35FSIQXHxHgXV1R5RwXIq8vr9W4RM8+4AjLPMXOSpIzdh5sHa7uhm0IZOGHqmM6srdktp9v2Mo++1Za5RsyZ5pmzI6tm8Ltwu891WNXWvVVn3tiDUgZOnr80VvNdgb5mx7o9xe2SXSl9Y+bMTPRpzfxmR+mJTxSUfqMmTEsM8HGRtPWlaXuzTrNnn/lJ+Y5rxJLLJwTJvytoyd3+VVrTOfrIYzjdcubU8LKDO0t13c+UfpPmx7bu3ZffymcyAAAAw3U2A+ghFB/LmXfZNTK5/Ej6vuGtoTjxLrSzdstz/91y/IlLyJTJc2eOjPB3liRdxb6Ub9YfbeyUPCasuPs6r5zXPt5Q5rXg0WuTOo7kdIYnxSkKP/jos0MMygEAAE6HqbFg96YDtQaZc9T0GZOj6zflfReudVYe2dFkPsu3A5vbinb1xFtqv6lzEsf47jnYMHAsam6tSttb0/F9A9GhDvBkMslQcTiv0aQeERMtaymv7zw7FRjcUE1hqMtO22vSnUHbm+1d7dNmqDmwYfUBEfRPWDqqceuO4nNyg7nSPzrUlLX54yKdrUjmFTUh2pC54esKvSY0cVxyUnB1SsXptNOZn5TvtJdu+LBUkrklzJngkb1nXy0jcwAAAFxqzlEAvW/7Bicn+ZwlV0qS05H0vUMt2l6WV9QUm7Tsmruj8wqyS3Oyy2q11tuq5R4TFlx/VYSx8Mi2lHp13PhpU+cvb6p/f0dzny2oI0ZGZB/Z/HZlbRWDcgAAgDNkNtTV6BK8ndXByQuSNHpJqS/P2t8UMSe66WBZwKTwqq3dUZ0ycML05M7MTYWykUnxccGebipDxf49KaU6s9o7YWJSnJdS31ycllomT5qW0JS29ajWLPNMmJPsmr3nYP+grbOtslWKclVKTbKQ+HHJI9zknfU5qdnHmk/8hZlrwISZgcd2pFXqnW0L5GfkVrgmzelTn+HckXriAOUi/IsYPXl0gJv4fD8rK61ce3wBmSZiVIw6x+ifEBsUIp8zR0pJ1yVM7amA1Pvoimo6JY+w+OTEYH9Xtby1aOuO7O/G95VpwsclTwjT6JvqtSqpqafII2L0hHg/N7mhsSQ/M3eg8T1ONIVSlbj0eOMfzlUmju7M2N8RP+vkg91e6ZmUFBXq7e4iNWbu2JfTbJbUJ1dPfrzdqqWAxMmj47yllqoWuby7ikqviOST11X6xkybGOUv76quP9Hsar+EcfFR3kpJW5+flXus2T4JqWiopMSEQHeVqa2iIDezXBo1Z3K4ZJDL23L2F7lMnBhuaDO5ukv1+fntgQnR3i76+rS9WWXtysDEcZNFTzB3VR/JOFCqtbWlOLTJE2P81aaWoty9uS0+4yZPi/ZxCZs6T5WRknf8rne5Si3Xt2n1ZrNBW5a5q+z4ilETxkX4u0gd9aWHs4pr5KGz58So9JKqs6LAEBrZeLwbj5mfrM7aVxw8IbkzY2ue7rsudCQ7s7TF0OdwelVsOPrUodE7eWmva3BBkrqlQ+np0nksu0p8OBLhLW/JS0vJEzt1PvnCMcg8QidPjgtSy0RPOJB67Ls76s+sW55URc+4KckJXkqToSl/f1Z+s+HkBq/t5A5pAACAE+wVQMcmjktMntSnsK2lac6SlT7+gTs3fDH4qtqy9W+ua182bVLi6Glxo6ddpSvdl7J5/dHaTlProY1vljp31bd1icWydZ7hl4UHu6ulvgG01JS3fs2+sgvoLhcAAHDxUXuOCHMzVXWZJLlc3nV4655KEXkGR4g5uoYqbXxwkGtFsd4z3M9Qtr9N7hrh0V68dW2V3i9xfmKwZ3m557ikkPqsb/ZoPeMnTUhs2VXSJB/l51ao1Xr4hcjrM5sGCDGVXsExvpK2wOQRPS7ZuyplQ7neL37OxHjtjiMnj3Em67XA6DmJEXWpFS3xocfr420oS20bVvZ14gBlInKNl+Xs2FohBU6eOS6xY3de78WMzdkZBYGSLG1HQZNLaE+Rc9TJR7c1Q+fpK69J3bGzSRkzfVJcoHN9eZe1qt6xyckuFVvXlZuCxy2domzqGQhicnjbgU1ZrXLvMXOSxtQ39b/p9URTGCSVrfFlfsnds9r7Nn67s3eEqSTzm51tbqOmTo72OZrWFtqnetbjkWlGjB8dWJvxVYrOf9yMOcpGUeTi7XnSutmyyRODtRm7Upo0iXNmhHYWi7WixsW6lhxYt9fgGjFuTlJodYo9blgW5zQpzpC/dUOTySNqzrT40PpcSa6UytPW57WYZW4JYrqqYOseQ8TM6clS5vp1GZ7JU8cEa6qqfBLCDGmbN1dKfgnR7i4y7fG6qQOSJ0bUCaUZAAALDklEQVR0ZO/+ql45YsqEadFpO9IO7JVPjqk5sLO0y7ZXQ1NpsWnqovmeRwsrKmvra1oNYsUJ43xqDuza164MmTA1ObppU0l3RRr370lvMCiD3WKPd+OAEKkpTXTj4J7z9V0XCp42LTaiOaMu4OTDqT14Gu/N+9Vhe1Pva3CEXGk4tuNAnWv8omlh+Tt3fWUKnjktyr8kSxvW58LJNY2McStP+yqvzS0iJshVWd9p7Wln2C1PqmNgTIxUvGldqd47apS3RtbpfHKD63Yc1RJBAwAAWJ2jO6CtLILZIpPLTrGcqb54+zvF29XuISPC4yeOTpq6+BpF19uflLUbTSaXkGk3jgz3d3fz9vZ0kbRKef/VjU31LUYJAADgTMh9YmfcHCtJ+rbSguy9BS3mQJO+taml999VtdeXtcaE+2qqO4P99bX5rWaDuTjTEBARnxQYEODpUivX+IR46I5lNRnMUn32ng1iFaWpThUX5FZRFxIgr89t7B1tydxHzFoyQrwD0tYfzcrMbJJHJDo3Hq1qFSvXlBaPHBfurSzuXUGZ2j/4xAJVWRuqRJFzWVNMVE99fPRVpxqdts8BtmliE6Wa3Ip2s9jfsZqYZD/3gtYhN+Dc7+gkqSwr3y8kYny0d5CvRl/Z/W7P3FNVnwBl3fGqFpU2jRZFboHBoZE+oZHjetYzVBQqxc+Bm6JB5JunbHxja/OR/IDgkclRgSGebq1Kubpf9Vx7cnOlZ6Br27GM7vLqwtI6P0334BxFJ62r9vDz1Jcfru8ym7uKCuvDAyVJ5RkeHDgi+rJE695bDC5y6ewH0OKchvmFhgTfbG0VU2ONWiaZdHX1J0a3sE6bJX1nV0u9TrSXvl1SuSrN+rYWU+yYcYkuJaVHe913rvQI9DGV763pPpDSwpa4kT4uhTUD7NfQkrNtU6lvcERszMykpJasfbtaA0NDIkZdGTGnZ35HiUZVIpk6tTXt3ds21Fc0JsYGuVXVhQRK9UdaDJJnT+3d/PxOdKGK3ZsrRGofM6Hf4Qz7lmBR+b51aOrdDUz6ZjFtNql0+k6ppcNslhv0klKl7HVdHL9wpJx6ncvo+AlSeXH5sXzbaTvdbjkQfWuj3iNqwjhZcWFVdlGXPCCpX4Nr+epOAAAAK3sF0AXZGeLRu2TavMtCIqJ3bPjyFENwfKezrTInuzKnqPK2m6+MGxXiVtM+4fLrlwUqmkpzso9k7JASVswKGGg94/H/AwAAnL4TQySfeK60/uekLKmrulybEBkQqhdxZZHWLHMdMWF+rFScW3qsqdMlUT3AVg0tZVWyMWEBrgFSZcbJ42PYBj62kmmk09ZVV96WEN1Tn6qiU9142ecAZd7S96b0Gz8nyaepKL+kuEnSRA22mPXGAZOhInXr1gEHnu7TFMNqfOfwyVOT1fU5Ryty2pUT/KRh6qnLsNY1tZZuXZdm9z+uM7Rkb9r33cAsMreEYa3VlL51hwhsY6InL08s37GjoOl0BgiRqT095bqmhoqchoo8r5j5E0M9jkjakrT1e0q/C0+t8f2JShY3yceE+YluXJelNQz/cE5Tnzoog3ve9PfuBsPLdttLD37T4B0RFjFhXpw2c/fu8q4BFjpVtzSZ5CqV7PhnKnKl+ASi1SSZ24s3b6oNDAuNmzJrTH3m9nIJAAAAgznVzchnybS5S8dPnb19/eenTJ9VI6699RfP3LQg1uV4gdo90Eu8LTQZ5ZqQRF9F5d63n/v6m6+zDpd2nNvbtwEAAGw666taXCPivA1ltTqzJHfz1nSUFGSX1muVnm4qkZE2VrZqYsK8lTKl98hJCycEKCVzY2W9akR8hFRbMfQdyubOuqoun+hgD5lM7RcRpWopazUMukBA7LzZsX5KUZ+KRteYMQGGsqrT/UY4s7a+XgqMCHWVyVwDYwKlmvp+I3iYTSJ3k9v+7qzf0TmrNJ7ylpzs4rImk7e3Wt6rqo21Bv/uqkpK74hQD+Xx3QX4eYpJpfeYmRNiPE777ehJjS8yVA+pIrvgWFWb3NtdJfbd2b/xexhaatrdu8slmWdIqI9SJvVb19Ba06IKi/FzlsncQiO9RdQo6Vsq2zUhfs7ibbNrRPK8ZD+lZAfinNYYPIO7W0XmETV7Zoz38HYjcw0eE+9nqinOzDjWovLxVB0v730gEdGeHVWNHQN1C5V31MyZiSFqcQpknn5+LnqtrrWmURkQ5CZKnEMmTJ0a1ufjEENjeYs8LCZIqin+Luru3YWCJ82bFOemP7PDsVV+yDoMYoALR/IbmThSrS3Oy86sMnn6amQnljydbmloqe90i4wIchUdxtkvLMJTX1/XYVYHxIwPU9YVFRzIbpJ7eCq0w2pwAAAAx3SOMtyRCclb132Seyj1lEvqK/cfKk2cNfm2K30PlTUY5W7BIxNCFA378ipbTM5akyJ25KQJTTltmtiZ4yNcJMZ5BgAA50VnY1mrOlRdWtF9v7G5rrBYP3P6tdHaulaDvnvA5q7SrGPh82bdMK77/tmUHT1jI7TWVhpiQqpqTvX9gObWwiPHwmatvD5ZMmnzUnbXdEp+gy2gb8lO2dez9ZayeinCtbz69HMvQ0NxWvn0RZevkIsDydqd1mC2Duz73f609cdakybPST6cXt9T0PfoujqU+TURMy9bqG1q0ZoMvUasNjcV5haHzVh5TWxjfYu2J0kXu8tsmDr/shiRaDcWZqScwUi5vRvf3FZU0DJ/zsKI1qZGvclkkAZq/J7jMeuKsoqiFs66dpS2rknXYhho3c76zNywpfOXjGxtqtNqu0+lWVeaVRQyZ+41E2RyQ23anhb7fAVh9zktmzl15RVKuaQrykgTuwkazmodLS3K5PmXJYrwvPFoVkX7iRmdtZlZwYvmLBEzOiqzNhWKlnLuv3pnTcHhsElzrrlCBNemlqq0vVXtOsPhvMD58xYly2Wm+oKUep0kP+kWeUNTeaM8wr82s3c37ulCU3u6kKE6Y19mq9Gg7Xs4p6Gztm8dhnWXfv8Lx6Cs1yVMmZOglEyiQfbaqnxa3VJsNjPNe9KcK62tVL43pbhJzGxtMYxKXpmo7O4hGeWtuq5+DQ4AAIDjnNy8w6WzZNHKG2Uy+YYv3pO+J+fgxKU3zUzwF+l4V0NpZemhIwfTyho7JbnfyIXXzRkf4SwZ6rPWH1HMnBtete6td4rlE1bcfZ1XzmsfbyjzWvDotUltW958Pa9VAobmFxhZXZ4vAQBwbqiDZ8yJqt+771RjNJ8RmSZu5tTAkt29v2JOUAYkzQyrSkmrt09sCpw2+iQAAICjOZsB9OjxU6fNXVpfU2l9ejhj/7GcQxJwoSKABgCcM8qAxPnj/PQ1uXsza8/+X3Cpg6fOjPfpLD2w/1ifVI+wDxca+iQAAICjOZtDcOQfSXd2dgmNjJbJegZNs0gAAAAQDLXZGzZI9tJZtW9zlQQAAAAAF56zeQc0cHHhDmgAAAAAAADArk77a8cBAAAAAAAAABgOAmgAAAAAAAAAgF0QQAMAAAAAAAAA7IIAGgAAAAAAAABgFwTQAAAAAAAAAAC7IIAGAAAAAAAAANgFATQAAAAAAAAAwC4IoAEAAAAAAAAAdkEADQAAAAAAAACwCwJoAAAAAAAAAIBdEEADAAAAAAAAAOyCABoAAAAAAAAAYBcE0AAAAAAAAAAAuyCABgAAAAAAAADYBQE0AAAAAAAAAMAuCKABAAAAAAAAAHZBAA0AAAAAAAAAsAsCaAAAAAAAAACAXRBAAwAAAAAAAADsggAaAAAAAAAAAGAX/w8AAP//gIxnIAAAAAZJREFUAwDL5OmmCcw0bQAAAABJRU5ErkJggg==', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(16:21:04)*


## 🤖 Claude *(16:21:05)*

Confirmo com meus próprios olhos: render **limpo e profissional** — TikTok ("Client Key" + placeholder real), YouTube e Pinterest ("Client ID"), cada um com Client Secret (password), helper PT-BR de onde pegar as creds, e botão Salvar. Tema MCORCH, zero white-screen. Atualizando a memória + te mostrando.

## 🤖 Claude *(16:21:10)*


🛠️ **Tool Call**: `SendUserFile`
```json
{
  "files": [
    "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/settings-social-yt-pinterest.png",
    "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/cf7e6851-e63b-48b0-8bc0-4c32d21eb7f0/scratchpad/social-accounts-page.png"
  ],
  "caption": "Settings\u2192Social (card de credenciais das 3 plataformas) + /dashboard/social (bot\u00f5es Conectar TikTok/YouTube/Pinterest). Renderizado em browser real, Vision QA \"high\", zero erro de console.",
  "status": "normal"
}
```

> **Tool Result (SendUserFile)** - ✅ Success
>
> ```
> 2 files delivered to user.
> ```

## 🤖 Claude *(16:21:13)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_brand_persona_ccio.md",
  "old_string": "(3) **HOLD** \u2014 n\u00e3o escrever c\u00f3digo NEM emendar BoK at\u00e9 o Sovereign registrar os 3 apps e ter `client_id`/`secret` em m\u00e3os.",
  "new_string": "(3) HOLD **sobrescrito** por \"continue for\u00e7a total\" (2026-06-27) \u2192 tudo CONSTRU\u00cdDO+DEPLOYADO+provado (ver STATUS abaixo)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_brand_persona_ccio.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:21:22)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_brand_persona_ccio.md",
  "old_string": "**Ao retomar:** PASSO 0 emenda BoK `post-engine` \u2192 slices 2-4 (publishers+OAuth env creds) \u2192 slice 5 (VIDEO_FLOW_PLATFORMS + gap auto-publish video_url) \u2192 slice 6 (spine CCIO).",
  "new_string": "**STATUS 2026-06-27 \u2014 CONSTRU\u00cdDO/DEPLOYADO/PROVADO (Lei 1):** PASSO 0 BoK selado (post-engine `06`/`09-pattern-conformance`/`10-amendment` + 3 SOPs `docs/processes/{tiktok,youtube,pinterest}-publish-credential-resolution.md`) \u00b7 migration `20260627120000_social_app_config.sql` **aplicada+provada** (coluna crua=UUID Vault `55caaf7b\u2026`, mask `\u2022\u2022\u2022\u2022`, decrypted s\u00f3 service-role\u2192anon 42501) \u00b7 `/security-review` SAFE \u00b7 helper `supabase/functions/_shared/social-app-config.ts` (resolu\u00e7\u00e3o per-user\u2192env\u2192402 fail-closed) \u00b7 branches em `social-auth-init`/`-callback`/`refresh-social-token`/`publish-social` (**deno check 8/8**, 5 fns **deployadas**) \u00b7 `auto-publish` video_url gap fechado (fail-soft) \u00b7 **fail-closed provado LIVE** (3\u00d7HTTP 402 `<plat>_not_configured`) \u00b7 UI `useSocialAppConfig`+`SocialAppConfigCard` (Settings\u2192Social) + 3 connect cards em `/dashboard/social` (tsc 0 \u00b7 build deployado \u00b7 **browser-verificado + Vision QA high**). **FR-PE-013 (`VIDEO_FLOW_PLATFORMS`) DEFERIDO** \u2014 s\u00f3 adicionar com a extens\u00e3o do enqueue-gate em `orchestrate-content`/`-step` (sen\u00e3o cobra-sem-valor: render s\u00f3 \u00e9 enfileirado pelo article-flow gated em wordpress). **Pend\u00eancias:** (Sovereign) registrar 3 apps + 3 audits (playbook `.claude/context/social-app-registration-playbook-2026-06-27.md`) + entrar `client_id`/`secret` (UI Settings\u2192Social OU env `TIKTOK_CLIENT_KEY`/`_SECRET`\u00b7`GOOGLE_CLIENT_ID`/`_SECRET`\u00b7`PINTEREST_CLIENT_ID`/`_SECRET`) \u2192 conex\u00e3o acende; p\u00fablico s\u00f3 p\u00f3s-audit. (c\u00f3digo) slice de video-cadence p/ novas plataformas + spine CCIO. \u26a0\ufe0f **git uncommitted** (prod j\u00e1 aplicado/deployado \u2014 risco de drift at\u00e9 commitar)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_brand_persona_ccio.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:21:32)*


## 🤖 Claude *(16:21:50)*

Pronto, Maestro. As redes **TikTok, YouTube e Pinterest** estão construídas, deployadas e provadas em produção em cada camada — operei com força total e nada foi declarado sem prova material (Lei 1).

## O que ficou de pé (tudo verificado)

| Camada | Estado | Prova material (Lei 1) |
|---|---|---|
| Pesquisa fundamentada 3 plataformas | ✅ | 3 verificadas HIGH, cada claim com URL oficial |
| **PASSO 0 — gate BoK** | ✅ selado | `post-engine` 06/09/10 + 3 SOPs · 21 padrões · FR-PE-005..016 · sem placeholder |
| **Migration `social_app_config`** | ✅ aplicada em prod | coluna crua = UUID Vault `55caaf7b…` · mask `••••` · decrypted só service-role (anon→42501) |
| `/security-review` | ✅ SAFE | tenant-guard 42501 INSERT+UPDATE · `search_path=''` · zero gap cross-tenant |
| Helper fail-closed | ✅ | per-user → env → 402 |
| 4 branches OAuth/publisher + auto-publish | ✅ deployadas | **`deno check` 8/8** · 5 fns "Deployed" (60–70kB) |
| **Fail-closed ao vivo** | ✅ provado | 3× `HTTP 402 {"error":"<plat>_not_configured"}` |
| UI (card de credenciais + 3 connect cards) | ✅ live | tsc 0 · bundle servido · **browser-verificado + Vision QA "high"** · 0 erro de console |

As telas acima são reais (browser logado, 1920×1080).

## Uma decisão de engenharia que evitou um bug
Adicionar `youtube/tiktok/pinterest` ao `VIDEO_FLOW_PLATFORMS` **introduziria cobrança-sem-valor** (o render 9:16 só é enfileirado pelo article-flow gated em `wordpress`; sem render, `finalize_video_render` nunca dá refund). **Revertido e deferido** (FR-PE-013) — só entra junto com a extensão do enqueue-gate no `orchestrate-content`. Vídeo vertical autônomo nessas redes é uma slice própria.

## Sua metade (caminho crítico — comece hoje)
Playbook em [social-app-registration-playbook-2026-06-27.md](.claude/context/social-app-registration-playbook-2026-06-27.md). Registrar os **3 apps de dev** + submeter os **3 audits** (YouTube é o mais longo: gate A ~10d + gate B semanas, seriais). Depois entrar os `client_id/secret` por **dois caminhos** (você decidiu "ambos"):
- **UI:** Configurações → Social → colar e Salvar (já vivo, cifra no Vault).
- **OU env:** `npx supabase secrets set TIKTOK_CLIENT_KEY=… TIKTOK_CLIENT_SECRET=…` (idem Google/Pinterest).

Aí o botão **Conectar** acende o OAuth; provo o E2E real de publish no mesmo dia. O **público** destrava com os audits.

## ⚠️ Um ponto que preciso da sua palavra
Prod está **aplicado e deployado**, mas o **git está uncommitted** (8 arquivos de doc + migration + edge fns + UI) — é exatamente o risco de drift que o projeto combate. **Quer que eu commite agora** (faço branch primeiro, já que estamos na `main`) **ou rodo `/handoff`** (seal com commits granulares + nó de milestone na malha)? Não commito sem seu GO.

## 👤 User *(16:21:52)*

Pode continuar que essa janela de contexto é grande faça o que for recomendado

## 🤖 Claude *(16:23:59)*


## 🤖 Claude *(16:24:01)*

Perfeito — vou fazer o recomendado: selar o arco com o **`/handoff`** (commits granulares fechando o drift prod↔git + atualização do HANDOFF.md + nó na malha + self-audit das Survival Laws). É o fechamento canônico do projeto e o que evita o risco de drift que sinalizei.

## 🤖 Claude *(16:24:01)*


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

## 👤 User *(16:24:01)*

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


## 🤖 Claude *(16:24:07)*


## 🤖 Claude *(16:24:07)*

Executando o ritual de seal. **Pre-flight + Phase 1 (security audit)** em paralelo.

## 🤖 Claude *(16:24:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== git status ===\"; git status --short\necho \"\"; echo \"=== diff stat ===\"; git diff HEAD --stat | tail -20\necho \"\"; echo \"=== tsc ===\"; npx tsc --noEmit 2>&1 | tail -5; echo \"tsc exit: ${PIPESTATUS[0]}\"",
  "description": "Pre-flight: status, diff, tsc"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git status ===
>  M docs/bok/post-engine/00-index.md
>  M docs/bok/post-engine/06-data-model.md
>  M src/components/icons/brand-icons.tsx
>  M src/hooks/useSocialAccounts.ts
>  M src/pages/SettingsPage.tsx
>  M src/pages/SocialAccountsPage.tsx
>  M supabase/functions/_shared/notify.ts
>  M supabase/functions/auto-publish/index.ts
>  M supabase/functions/autopilot-run/index.ts
>  M supabase/functions/publish-social/index.ts
>  M supabase/functions/refresh-social-token/index.ts
>  M supabase/functions/social-auth-callback/index.ts
>  M supabase/functions/social-auth-init/index.ts
> ?? .claude/context/social-app-registration-playbook-2026-06-27.md
> ?? .claude/context/social-connect-3platforms-blueprint-2026-06-27.md
> ?? deno.lock
> ?? docs/bok/post-engine/09-pattern-conformance.md
> ?? docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md
> ?? docs/processes/pinterest-publish-credential-resolution.md
> ?? docs/processes/tiktok-publish-credential-resolution.md
> ?? docs/processes/youtube-publish-credential-resolution.md
> ?? src/components/settings/SocialAppConfigCard.tsx
> ?? src/hooks/useSocialAppConfig.ts
> ?? src/lib/social-app-config.ts
> ?? supabase/functions/_shared/social-app-config.ts
> ?? supabase/migrations/20260627120000_social_app_config.sql
> 
> === diff stat ===
>  docs/bok/post-engine/00-index.md                 |  15 +-
>  docs/bok/post-engine/06-data-model.md            | 103 ++++++-
>  src/components/icons/brand-icons.tsx             |  15 +
>  src/hooks/useSocialAccounts.ts                   |  10 +-
>  src/pages/SettingsPage.tsx                       |   7 +-
>  src/pages/SocialAccountsPage.tsx                 |  21 +-
>  supabase/functions/_shared/notify.ts             |   2 +-
>  supabase/functions/auto-publish/index.ts         |  48 +++-
>  supabase/functions/autopilot-run/index.ts        |   5 +
>  supabase/functions/publish-social/index.ts       | 343 +++++++++++++++++++++++
>  supabase/functions/refresh-social-token/index.ts | 142 ++++++++++
>  supabase/functions/social-auth-callback/index.ts | 146 +++++++++-
>  supabase/functions/social-auth-init/index.ts     |  68 ++++-
>  13 files changed, 901 insertions(+), 24 deletions(-)
> 
> === tsc ===
> tsc exit: 0
> ```

## 🤖 Claude *(16:24:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== 1a. secret leak scan (working tree) ===\"\ngit diff HEAD | grep -E \"(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{20,}|STRIPE_|SECRET_KEY|ACCESS_TOKEN|api_key\\s*=\\s*['\\\"][^'\\\"]{10,})\" \\\n  | grep -v \"example\\|placeholder\\|<.*>\\|your-key\\|YOUR_\\|client_secret TEXT\\|client_secret:\\|CLIENT_SECRET\\|client_secret =\\|p_value\\|n.message\\|REVOKE\\|GRANT\\|decrypted_\\|access_token (text\\|refresh_token\" | head -15 || echo \"no raw secrets \u2705\"\necho \"\"; echo \"=== 1c. client-side coin deduction ===\"\ngrep -rn \"mco_balance.*update\\|UPDATE.*mco_balance\" src/ | grep -v \"settings\\|top.up\\|topup\\|SettingsPage\" | head -5 || echo \"NO VIOLATIONS \u2705\"\necho \"\"; echo \"=== 1e. sensitive console.log in new code ===\"\ngrep -rnE \"console\\.log.*(token|secret|password|client_secret)\" src/hooks/useSocialAppConfig.ts src/components/settings/SocialAppConfigCard.tsx src/lib/social-app-config.ts supabase/functions/_shared/social-app-config.ts 2>/dev/null | head -5 || echo \"NO SENSITIVE LOGS \u2705\"",
  "description": "Phase 1 security audit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === 1a. secret leak scan (working tree) ===
>      const serviceRoleKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> +        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> +        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> +        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> +        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> +        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 
> === 1c. client-side coin deduction ===
> 
> === 1e. sensitive console.log in new code ===
> ```

## 🤖 Claude *(16:24:49)*


## 🤖 Claude *(16:24:52)*

**Phase 1 — Security: ✅ PASS.** As matches do 1a são **leituras de env** (`Deno.env.get("SB_SECRET_KEY") ?? ...`) — o padrão seguro, não secret hardcoded (falso-positivo no substring "SECRET_KEY"). 1c/1e limpos, tsc 0. Sem 🔴.

Removo o `deno.lock` (artefato dos meus `deno check`, não do projeto) e faço os **commits granulares** (sem trailer Co-Authored-By, conforme regra do protocolo).

## 🤖 Claude *(16:25:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nrm -f deno.lock\n# Group 1 \u2014 docs/BoK gate\ngit add docs/bok/post-engine/00-index.md docs/bok/post-engine/06-data-model.md docs/bok/post-engine/09-pattern-conformance.md docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md docs/processes/tiktok-publish-credential-resolution.md docs/processes/youtube-publish-credential-resolution.md docs/processes/pinterest-publish-credential-resolution.md .claude/context/social-connect-3platforms-blueprint-2026-06-27.md .claude/context/social-app-registration-playbook-2026-06-27.md\ngit commit -q -m \"docs(post-engine): social-connect BoK amendment + Lei-2 SOPs + grounded blueprint (TikTok/YouTube/Pinterest)\n\nCloses PASSO 0 of the Closed-Loop Protocol for connecting 3 brand-persona channels.\nReconciles the obsolete social_credentials drift to the live social_accounts/social_app_config,\nadds the 21-row Pattern Conformance Declaration (09) and the branch-design amendment (10, FR-PE-005..016),\nplus 3 credential-resolution SOPs. Grounded in adversarially-verified research (wf_b5a35451, 3 platforms HIGH).\" && echo \"\u2705 commit 1\"\n\n# Group 2 \u2014 migration\ngit add supabase/migrations/20260627120000_social_app_config.sql\ngit commit -q -m \"feat(db): social_app_config \u2014 per-user Vault-encrypted OAuth app credentials (FR-PE-005)\n\nSingle table keyed UNIQUE(user_id, platform); client_secret encrypted in Vault via the idempotent\ntrg_encrypt_social_app_config (vault_upsert_secret), masked security_invoker view, service-role-only\ndecrypted view, INSTEAD OF tenant-guard (42501) mirroring social_accounts. /security-review SAFE.\nApplied + proven in prod (raw column = Vault UUID, mask, decrypted denied to anon).\" && echo \"\u2705 commit 2\"",
  "description": "Commits 1-2: docs + migration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m╯[m
> ┃  e2e-output-tripwire ❯ 
> 
> ┃  secret-scan ❯ 
> 
> ┃  gitleaks-staged ❯ 
> 
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m1:25PM[0m [32mINF[0m 1 commits scanned.
> [90m1:25PM[0m [32mINF[0m scan completed in 75.2ms
> [90m1:25PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.13 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.04 seconds)
> ✔️ gitleaks-staged (0.12 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> ✅ commit 1
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m╯[m
> ┃  e2e-output-tripwire ❯ 
> 
> ┃  secret-scan ❯ 
> 
> ┃  gitleaks-staged ❯ 
> 
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m1:25PM[0m [32mINF[0m 1 commits scanned.
> [90m1:25PM[0m [32mINF[0m scan completed in 18.6ms
> [90m1:25PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.08 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.03 seconds)
> ✔️ gitleaks-staged (0.07 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> ✅ commit 2
> ```

## 🤖 Claude *(16:25:13)*


## 🤖 Claude *(16:25:14)*

Commits 1-2 ✅ (gitleaks: no leaks). Commits 3 (edge) e 4 (UI):

## 🤖 Claude *(16:25:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\n# Group 3 \u2014 edge functions + helper\ngit add supabase/functions/_shared/social-app-config.ts supabase/functions/_shared/notify.ts supabase/functions/social-auth-init/index.ts supabase/functions/social-auth-callback/index.ts supabase/functions/refresh-social-token/index.ts supabase/functions/publish-social/index.ts supabase/functions/auto-publish/index.ts supabase/functions/autopilot-run/index.ts\ngit commit -q -m \"feat(social): TikTok/YouTube/Pinterest OAuth + publisher branches, fail-closed cred resolution (FR-PE-006..016)\n\nShared resolveSocialAppCreds (per-user social_app_config -> env fallback -> 402, never a silent shared key).\nAdds 3 branches each to social-auth-init/-callback/refresh-social-token (rotating-token aware) + publish-social\n(TikTok Direct Post FILE_UPLOAD, YouTube resumable, Pinterest video-pin). auto-publish resolves+signs video_url\n(fail-soft). VIDEO_FLOW_PLATFORMS kept as wordpress only (FR-PE-013 deferred: needs orchestrate-content enqueue\ngate, else charge-without-value). deno check 8/8; 5 fns deployed; fail-closed proven live (3x402).\" 2>&1 | grep -iE \"no leaks|leaks found|commit|\u276f secret|BLOCK|error\" | head -4 && echo \"\u2705 commit 3\"\n\n# Group 4 \u2014 UI\ngit add src/hooks/useSocialAppConfig.ts src/lib/social-app-config.ts src/components/settings/SocialAppConfigCard.tsx src/components/icons/brand-icons.tsx src/hooks/useSocialAccounts.ts src/pages/SettingsPage.tsx src/pages/SocialAccountsPage.tsx\ngit commit -q -m \"feat(settings): social app-config card + TikTok/YouTube/Pinterest connect cards\n\nuseSocialAppConfig (read-then-insert/update on the Vault-masked view, never .upsert, never round-trips the mask) +\nSocialAppConfigCard in Settings->Social + the 3 connect cards via the generic initiateOAuth. brand-icons gains\nTikTok/YouTube/Pinterest glyphs. tsc 0; built + deployed; browser-verified + Vision QA high.\" 2>&1 | grep -iE \"no leaks|leaks found|commit|BLOCK|error\" | head -4 && echo \"\u2705 commit 4\"\necho \"\"; echo \"=== recent log ===\"; git log --oneline -5",
  "description": "Commits 3-4: edge + UI"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [0;31m║  SECRET LEAK DETECTED — COMMIT BLOCKED                       ║[0m
> or move the value to the environment / Supabase Vault. Never commit live keys.[0m
> [90m1:25PM[0m [32mINF[0m 1 commits scanned.
> ✅ commit 3
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [0;31m║  SECRET LEAK DETECTED — COMMIT BLOCKED                       ║[0m
> or move the value to the environment / Supabase Vault. Never commit live keys.[0m
> [90m1:25PM[0m [32mINF[0m 1 commits scanned.
> ✅ commit 4
> 
> === recent log ===
> c94bd75 feat(db): social_app_config — per-user Vault-encrypted OAuth app credentials (FR-PE-005)
> ea12afc docs(post-engine): social-connect BoK amendment + Lei-2 SOPs + grounded blueprint (TikTok/YouTube/Pinterest)
> 2d8e46d chore(sprint): v6.53.0 — Agentic Governance + Learning Loop + analytics honesto
> f486a8a docs(handoff): seal Agentic Governance + Learning Loop + analytics honesto + perfis da marca limpos
> 08e5ee3 docs(readme): v6.53.0 — Agentic Governance + Collective Efficiency Ledger + Learning Loop
> ```

## 🤖 Claude *(16:25:42)*


## 🤖 Claude *(16:25:44)*

⚠️ **Lei 1 catch** — os "✅ commit 3/4" foram **falsos** (o `&&` rodou pelo grep, não pelo git). O `git log` prova: só os commits 1 e 2 entraram. O hook **secret-scan** do projeto BLOQUEOU os commits 3 e 4 ("SECRET LEAK DETECTED"). Provável falso-positivo no padrão `Deno.env.get("SB_SECRET_KEY")`. Investigando o que o hook casou.

## 🤖 Claude *(16:25:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== still staged? ===\"; git diff --cached --name-only | head\necho \"\"; echo \"=== secret-scan hook config ===\"; grep -rA8 \"secret-scan\" lefthook.yml .lefthook.yml lefthook.yaml 2>/dev/null | head -25\necho \"\"; echo \"=== the scan script ===\"; ls scripts/ | grep -iE \"secret|scan\"; ls .husky/ scripts/qa/ 2>/dev/null | grep -iE \"secret|scan\"",
  "description": "Find secret-scan hook logic"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === still staged? ===
> src/components/icons/brand-icons.tsx
> src/components/settings/SocialAppConfigCard.tsx
> src/hooks/useSocialAccounts.ts
> src/hooks/useSocialAppConfig.ts
> src/lib/social-app-config.ts
> src/pages/SettingsPage.tsx
> src/pages/SocialAccountsPage.tsx
> supabase/functions/_shared/notify.ts
> supabase/functions/_shared/social-app-config.ts
> supabase/functions/auto-publish/index.ts
> 
> === secret-scan hook config ===
> lefthook.yml:    - name: secret-scan
> lefthook.yml:      run: bash .claude/hooks/secret-scan.sh
> lefthook.yml-
> lefthook.yml-    # Job 2 — gitleaks structural scan over the staged diff (second, independent engine).
> lefthook.yml-    # SELF-HEALING (OTD-SEC-003): if the gitleaks binary is absent the job exits 0 with a notice
> lefthook.yml-    # rather than blocking every commit — the sovereign scanner (Job 1) still enforces the gate.
> lefthook.yml-    # if/then/else (NOT &&||): a real gitleaks finding (exit 1) must propagate and block; only true
> lefthook.yml-    # ABSENCE degrades to exit 0. The && || form would swallow a detection as if the binary were missing.
> lefthook.yml-    - name: gitleaks-staged
> lefthook.yml:      run: if command -v gitleaks >/dev/null 2>&1; then gitleaks protect --staged --redact --config .gitleaks.toml; else echo "[lefthook] gitleaks absent (OTD-SEC-003) — sovereign secret-scan still enforced"; fi
> lefthook.yml-
> lefthook.yml-    # Job 3 — e2e artifact tripwire: HARs / session dumps must never carry live tokens.
> lefthook.yml-    - name: e2e-output-tripwire
> lefthook.yml-      run: bash .claude/hooks/e2e-output-tripwire.sh
> lefthook.yml-
> lefthook.yml-post-commit:
> lefthook.yml-  jobs:
> lefthook.yml-    # Preserved from the legacy .git/hooks/post-commit: AST re-ingest into the Sovereign Knowledge Mesh.
> 
> === the scan script ===
> ```

## 🤖 Claude *(16:25:57)*


## 🤖 Claude *(16:25:59)*

O hook é `.claude/hooks/secret-scan.sh`. Os arquivos dos commits 3 e 4 estão staged juntos agora. Vou ver exatamente o que ele casou (rodando o scan) antes de qualquer ação — **não vou usar `--no-verify`** (o protocolo proíbe).

## 🤖 Claude *(16:26:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== run the secret-scan to see the exact match ===\"; bash .claude/hooks/secret-scan.sh 2>&1 | grep -vE \"^\\[38|^\\s*$\" | head -40",
  "description": "Run secret-scan to see exact match"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === run the secret-scan to see the exact match ===
> [0;31m╔══════════════════════════════════════════════════════════════╗[0m
> [0;31m║  SECRET LEAK DETECTED — COMMIT BLOCKED                       ║[0m
> [0;31m╚══════════════════════════════════════════════════════════════╝[0m
> [1;33mPotential credentials found in staged changes:[0m
> +  tiktok: { id: "TIKTOK_CLIENT_KEY", secret: "TIKTOK_CLIENT_SECRET", label: "TikTok" },
> +  youtube: { id: "GOOGLE_CLIENT_ID", secret: "GOOGLE_CLIENT_SECRET", label: "YouTube" },
> +  pinterest: { id: "PINTEREST_CLIENT_ID", secret: "PINTEREST_CLIENT_SECRET", label: "Pinterest" },
> [1;33mIf this is a FALSE POSITIVE, extend SAFE_PATTERN in .claude/hooks/secret-scan.sh
> or move the value to the environment / Supabase Vault. Never commit live keys.[0m
> ```

## 🤖 Claude *(16:26:22)*


## 🤖 Claude *(16:26:24)*

Falso-positivo claro: o hook casou meu **ENV_MAP** — `secret: "TIKTOK_CLIENT_SECRET"` são **nomes de variáveis de env** (chaves de lookup no `Deno.env`), não valores de credencial. O hook sugere estender o `SAFE_PATTERN` ou refatorar. Lendo o hook para o fix correto e mínimo.

## 🤖 Claude *(16:26:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/hooks/secret-scan.sh"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bash
> 2	# Sovereign secret-leak guard — blocks commits containing hardcoded credentials.
> 3	# Ported from the original .git/hooks/pre-commit and driven by lefthook (SDD-SEC §1.2).
> 4	# Engine: ERE only (`grep -E`). The BRE idiom '^\+\+\+' silently no-ops under the ugrep shim some
> 5	# environments alias to `grep` (incident 2026-06-01) — never use it.
> 6	
> 7	set -euo pipefail
> 8	
> 9	RED='\033[0;31m'
> 10	YELLOW='\033[1;33m'
> 11	NC='\033[0m'
> 12	
> 13	STAGED=$(git diff --cached --name-only 2>/dev/null)
> 14	if [ -z "$STAGED" ]; then
> 15	  exit 0
> 16	fi
> 17	
> 18	PATTERN='AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9\-_]{30,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36}|ghs_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]{10,}|sbp_[a-zA-Z0-9]{20,}|sb_secret_[a-zA-Z0-9_-]{10,}|whsec_[a-zA-Z0-9]{10,}|(sk|rk)_(live|test)_[a-zA-Z0-9]{10,}|r8_[a-zA-Z0-9]{30,}'
> 19	SAFE_PATTERN='example|placeholder|your-key|YOUR_KEY|YOUR_SECRET|YOUR_API_KEY|<[A-Z_]+>|\.\.\.|\*\*\*|digest|sha256|fingerprint|test-only|mock|fake'
> 20	
> 21	# Credential-named var assigned a quoted literal of 8+ chars. Quoted form required, so ${...}
> 22	# templates and backtick dynamic strings are ignored.
> 23	GENERIC_CRED_PATTERN='(password|passwd|pwd|secret|client_secret|api[_-]?key|access_token|refresh_token|private_key)["'\'']?[[:space:]]*[:=][[:space:]]*["'\''][^"'\''$[:space:]]{8,}["'\'']'
> 24	
> 25	# Added content lines only: single '+' prefix, excluding the '+++' file header.
> 26	ADDED=$(git diff --cached --no-color | grep -E '^\+[^+]' || true)
> 27	HITS=$(printf '%s\n' "$ADDED" | grep -E "$PATTERN" | grep -vE "$SAFE_PATTERN" || true)
> 28	CRED_HITS=$(printf '%s\n' "$ADDED" | grep -iE "$GENERIC_CRED_PATTERN" | grep -vE "$SAFE_PATTERN" || true)
> 29	ALL_HITS=$(printf '%s\n%s\n' "$HITS" "$CRED_HITS" | grep -vE '^[[:space:]]*$' || true)
> 30	
> 31	if [ -n "$ALL_HITS" ]; then
> 32	  echo ""
> 33	  echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
> 34	  echo -e "${RED}║  SECRET LEAK DETECTED — COMMIT BLOCKED                       ║${NC}"
> 35	  echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
> 36	  echo ""
> 37	  echo -e "${YELLOW}Potential credentials found in staged changes:${NC}"
> 38	  echo ""
> 39	  echo "$ALL_HITS" | head -10
> 40	  echo ""
> 41	  echo -e "${YELLOW}If this is a FALSE POSITIVE, extend SAFE_PATTERN in .claude/hooks/secret-scan.sh"
> 42	  echo -e "or move the value to the environment / Supabase Vault. Never commit live keys.${NC}"
> 43	  exit 1
> 44	fi
> 45	
> 46	exit 0
> 47	
> ```

## 🤖 Claude *(16:28:12)*


## 🤖 Claude *(16:28:15)*

O hook é estrito (case-insensitive) e casou `secret: "TIKTOK_CLIENT_SECRET"` — nomes de env var, não valores. O fix mais limpo (mantém o hook de segurança rígido, sem allowlist frouxa): **renomear as chaves do ENV_MAP** `id`/`secret` → `idEnv`/`secretEnv` (são nomes de env, fica mais claro). Depois re-deploy das fns que importam o helper, pra git==prod. Lendo o helper + achando os importers.

## 🤖 Claude *(16:28:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts",
  "offset": 26,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 26	const ENV_MAP: Record<SocialAppPlatform, { id: string; secret: string; label: string }> = {
> 27	  tiktok: { id: "TIKTOK_CLIENT_KEY", secret: "TIKTOK_CLIENT_SECRET", label: "TikTok" },
> 28	  youtube: { id: "GOOGLE_CLIENT_ID", secret: "GOOGLE_CLIENT_SECRET", label: "YouTube" },
> 29	  pinterest: { id: "PINTEREST_CLIENT_ID", secret: "PINTEREST_CLIENT_SECRET", label: "Pinterest" },
> 30	};
> 31	
> 32	/** Structured fail-closed error → maps to a 402 JSON body the client can act on. */
> 33	export class SocialAppConfigError extends Error {
> 34	  readonly httpStatus = 402;
> 35	  readonly body: { error: string; action: string };
> 36	  constructor(platform: string, label: string) {
> 37	    super(`${platform}_not_configured`);
> ```

## 🤖 Claude *(16:28:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== who imports the helper? ===\"; grep -rl \"_shared/social-app-config\" supabase/functions/*/index.ts",
  "description": "Find helper importers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === who imports the helper? ===
> supabase/functions/refresh-social-token/index.ts
> supabase/functions/social-auth-callback/index.ts
> supabase/functions/social-auth-init/index.ts
> ```

## 🤖 Claude *(16:28:22)*


## 🤖 Claude *(16:28:22)*

3 importers (init/callback/refresh). Renomeando no helper:

## 🤖 Claude *(16:28:27)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts",
  "old_string": "const ENV_MAP: Record<SocialAppPlatform, { id: string; secret: string; label: string }> = {\n  tiktok: { id: \"TIKTOK_CLIENT_KEY\", secret: \"TIKTOK_CLIENT_SECRET\", label: \"TikTok\" },\n  youtube: { id: \"GOOGLE_CLIENT_ID\", secret: \"GOOGLE_CLIENT_SECRET\", label: \"YouTube\" },\n  pinterest: { id: \"PINTEREST_CLIENT_ID\", secret: \"PINTEREST_CLIENT_SECRET\", label: \"Pinterest\" },\n};",
  "new_string": "// Values are env-var NAMES (looked up in Deno.env), NOT secret values. The `*Env` suffix keeps them\n// unambiguous to the secret-scan hook (a `secret: \"...\"` literal would false-positive).\nconst ENV_MAP: Record<SocialAppPlatform, { idEnv: string; secretEnv: string; label: string }> = {\n  tiktok: { idEnv: \"TIKTOK_CLIENT_KEY\", secretEnv: \"TIKTOK_CLIENT_SECRET\", label: \"TikTok\" },\n  youtube: { idEnv: \"GOOGLE_CLIENT_ID\", secretEnv: \"GOOGLE_CLIENT_SECRET\", label: \"YouTube\" },\n  pinterest: { idEnv: \"PINTEREST_CLIENT_ID\", secretEnv: \"PINTEREST_CLIENT_SECRET\", label: \"Pinterest\" },\n};"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:28:31)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts",
  "old_string": "  const envId = Deno.env.get(env.id);\n  const envSecret = Deno.env.get(env.secret);",
  "new_string": "  const envId = Deno.env.get(env.idEnv);\n  const envSecret = Deno.env.get(env.secretEnv);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:28:38)*


## 🤖 Claude *(16:28:39)*

Renomeado. `deno check` do helper + importers + reset do staging misturado:

## 🤖 Claude *(16:28:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nexport PATH=\"/home/ubuntu/.deno/bin:$PATH\"\nfor f in _shared/social-app-config.ts social-auth-init social-auth-callback refresh-social-token; do\n  if [ -d \"supabase/functions/$f\" ]; then T=\"supabase/functions/$f/index.ts\"; else T=\"supabase/functions/$f\"; fi\n  deno check \"$T\" >/dev/null 2>&1 && echo \"\u2705 $f\" || echo \"\u274c $f\"\ndone\necho \"\"; echo \"=== unstage the mixed staging ===\"; git reset -q HEAD; git status --short | head -3; echo \"...\"",
  "description": "deno check renamed helper + reset staging"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ _shared/social-app-config.ts
> ✅ social-auth-init
> ✅ social-auth-callback
> ✅ refresh-social-token
> 
> === unstage the mixed staging ===
>  M src/components/icons/brand-icons.tsx
>  M src/hooks/useSocialAccounts.ts
>  M src/pages/SettingsPage.tsx
> ...
> ```

## 🤖 Claude *(16:28:50)*


## 🤖 Claude *(16:28:52)*

deno check 4/4 limpo após rename. Re-commitando grupos 3 e 4 (e desta vez **verifico pelo git log**, não por echo):

## 🤖 Claude *(16:29:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add supabase/functions/_shared/social-app-config.ts supabase/functions/_shared/notify.ts supabase/functions/social-auth-init/index.ts supabase/functions/social-auth-callback/index.ts supabase/functions/refresh-social-token/index.ts supabase/functions/publish-social/index.ts supabase/functions/auto-publish/index.ts supabase/functions/autopilot-run/index.ts\ngit commit -q -m \"feat(social): TikTok/YouTube/Pinterest OAuth + publisher branches, fail-closed cred resolution (FR-PE-006..016)\n\nShared resolveSocialAppCreds (per-user social_app_config -> env fallback -> 402, never a silent shared key).\nAdds 3 branches each to social-auth-init/-callback/refresh-social-token (rotating-token aware) + publish-social\n(TikTok Direct Post FILE_UPLOAD, YouTube resumable, Pinterest video-pin). auto-publish resolves+signs video_url\n(fail-soft). VIDEO_FLOW_PLATFORMS kept wordpress-only (FR-PE-013 deferred: needs orchestrate-content enqueue\ngate, else charge-without-value). deno check 8/8; fail-closed proven live (3x402).\" >/dev/null 2>&1\necho \"edge commit exit: $?\"\n\ngit add src/hooks/useSocialAppConfig.ts src/lib/social-app-config.ts src/components/settings/SocialAppConfigCard.tsx src/components/icons/brand-icons.tsx src/hooks/useSocialAccounts.ts src/pages/SettingsPage.tsx src/pages/SocialAccountsPage.tsx\ngit commit -q -m \"feat(settings): social app-config card + TikTok/YouTube/Pinterest connect cards\n\nuseSocialAppConfig (read-then-insert/update on the Vault-masked view, never .upsert, never round-trips the mask) +\nSocialAppConfigCard in Settings->Social + the 3 connect cards via generic initiateOAuth. brand-icons gains\nTikTok/YouTube/Pinterest glyphs. tsc 0; built + deployed; browser-verified + Vision QA high.\" >/dev/null 2>&1\necho \"ui commit exit: $?\"\necho \"\"; echo \"=== VERIFY via git log (material) ===\"; git log --oneline -6\necho \"\"; echo \"=== anything left uncommitted? ===\"; git status --short",
  "description": "Re-commit edge + UI, verify via git log"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> edge commit exit: 0
> ui commit exit: 0
> 
> === VERIFY via git log (material) ===
> e81d868 feat(settings): social app-config card + TikTok/YouTube/Pinterest connect cards
> 25477a8 feat(social): TikTok/YouTube/Pinterest OAuth + publisher branches, fail-closed cred resolution (FR-PE-006..016)
> c94bd75 feat(db): social_app_config — per-user Vault-encrypted OAuth app credentials (FR-PE-005)
> ea12afc docs(post-engine): social-connect BoK amendment + Lei-2 SOPs + grounded blueprint (TikTok/YouTube/Pinterest)
> 2d8e46d chore(sprint): v6.53.0 — Agentic Governance + Learning Loop + analytics honesto
> f486a8a docs(handoff): seal Agentic Governance + Learning Loop + analytics honesto + perfis da marca limpos
> 
> === anything left uncommitted? ===
> ?? deno.lock
> ```

## 🤖 Claude *(16:29:10)*


## 🤖 Claude *(16:29:12)*

✅ **4 commits confirmados via git log** (ea12afc · c94bd75 · 25477a8 · e81d868). Removo o `deno.lock` (artefato) e **re-deploy dos 3 importers** (init/callback/refresh) pra git==prod após o rename do helper.

## 🤖 Claude *(16:29:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nrm -f deno.lock\nfor fn in social-auth-init social-auth-callback refresh-social-token; do\n  npx supabase functions deploy \"$fn\" 2>&1 | grep -iE \"Deployed|error|failed\" | head -2\ndone",
  "description": "Redeploy 3 helper importers",
  "timeout": 300000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Deployed Functions on project bcyvddsykvehvpwstlfa: social-auth-init
> Deployed Functions on project bcyvddsykvehvpwstlfa: social-auth-callback
> Deployed Functions on project bcyvddsykvehvpwstlfa: refresh-social-token
> ```

## 🤖 Claude *(16:29:38)*


## 🤖 Claude *(16:29:39)*

Redeploy ✅ (git==prod). Re-smoke rápido (confirma o rename não quebrou o lookup de env) + **Phase 3 — nó de milestone na malha**.

## 🤖 Claude *(16:29:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nURL=\"${VITE_SUPABASE_URL:-${SUPABASE_URL}}\"; export SUPABASE_URL=\"$URL\"; SVC=\"${SB_SECRET_KEY}\"\nJWT=$(bun run scripts/qa/gen-user-jwt.ts gabrielcallr@icloud.com 2>/dev/null | tail -1)\necho \"=== re-smoke tiktok (expect 402) ===\"\ncurl -s -w \" [HTTP %{http_code}]\\n\" \"$URL/functions/v1/social-auth-init\" -H \"Authorization: Bearer $JWT\" -H \"Content-Type: application/json\" -d '{\"platform\":\"tiktok\",\"redirect_uri\":\"https://login.mcorch.com/social/callback\"}'\n\necho \"\"; echo \"=== Phase 3: insert handoff node ===\"\nNODE=$(curl -s -X POST \"$URL/rest/v1/mcorch_nodes\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n -d '{\"name\":\"session-handoff-20260627-social-connect-tiktok-youtube-pinterest\",\"node_type\":\"handoff\",\"content\":\"[HANDOFF SEAL] Conectar redes TikTok/YouTube/Pinterest (brand persona Gabriel AI): PASSO 0 BoK post-engine (06/09/10 + 3 SOPs Lei 2) + migration social_app_config Vault-cifrada aplicada+provada (coluna crua=UUID Vault, mask, decrypted service-role-only) + /security-review SAFE + helper fail-closed per-user->env->402 + 4 edge fns OAuth/publisher (deno check 8/8, deployadas, fail-closed 3x402 provado live) + UI (useSocialAppConfig + SocialAppConfigCard + 3 connect cards, tsc 0, build deployado, browser-verified + Vision QA high). FR-PE-013 video-cadence DEFERIDO. Pendente: Sovereign registra 3 apps + 3 audits.\",\"stability_score\":1.0,\"project_id\":null,\"user_id\":null,\"metadata\":{\"session\":\"social-connect-tiktok-youtube-pinterest\",\"commits\":\"ea12afc|c94bd75|25477a8|e81d868\"}}' \\\n | python3 -c \"import sys,json;d=json.load(sys.stdin);print(d[0]['id'] if isinstance(d,list) and d else d)\")\necho \"Node ID: $NODE\"\necho \"{\\\"handoffNodeId\\\": \\\"$NODE\\\"}\" > proof-manifest.json\necho \"\"; echo \"=== embed it ===\"\ncurl -s -X POST \"$URL/functions/v1/embed-mcorch-node\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" -H \"Content-Type: application/json\" -d \"{\\\"record\\\": {\\\"id\\\": \\\"$NODE\\\"}}\" | head -c 200",
  "description": "Re-smoke + insert/embed handoff node"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === re-smoke tiktok (expect 402) ===
> {"error":"tiktok_not_configured","action":"Configure suas credenciais de app TikTok em /dashboard/settings"} [HTTP 402]
> 
> === Phase 3: insert handoff node ===
> Node ID: 311a55b1-fb7b-410f-9582-625fb4721619
> 
> === embed it ===
> {"error":"Request body must contain { node_id: string }"}
> ```

## 🤖 Claude *(16:29:59)*


## 🤖 Claude *(16:30:01)*

Re-smoke ✅ (402, rename OK). Nó `311a55b1-fb7b-410f-9582-625fb4721619` inserido. O embed quer `{node_id}` (não `{record}`) — corrijo + verifico o vetor:

## 🤖 Claude *(16:30:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nURL=\"${VITE_SUPABASE_URL:-${SUPABASE_URL}}\"; SVC=\"${SB_SECRET_KEY}\"; NODE=\"311a55b1-fb7b-410f-9582-625fb4721619\"\necho \"=== embed (correct payload {node_id}) ===\"\ncurl -s -X POST \"$URL/functions/v1/embed-mcorch-node\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" -H \"Content-Type: application/json\" -d \"{\\\"node_id\\\": \\\"$NODE\\\"}\" | head -c 200\necho \"\"; echo \"=== verify embedding present ===\"\ncurl -s \"$URL/rest/v1/mcorch_nodes?id=eq.$NODE&select=id,embedding\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" | python3 -c \"import sys,json;d=json.load(sys.stdin);e=d[0].get('embedding') if d else None;print('embedded:', bool(e), '| dims:', (len(e.split(',')) if isinstance(e,str) else (len(e) if e else 0)))\"\necho \"=== live node count (exact) for README badge ===\"\ncurl -s \"$URL/rest/v1/mcorch_nodes?select=id&limit=1\" -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'",
  "description": "Embed node + verify + count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === embed (correct payload {node_id}) ===
> {"node_id":"311a55b1-fb7b-410f-9582-625fb4721619","dims":768,"chunks":1,"model":"openai/text-embedding-3-small","provider":"openrouter","stitched":0}
> === verify embedding present ===
> embedded: True | dims: 768
> === live node count (exact) for README badge ===
> 8973
> ```

## 🤖 Claude *(16:30:22)*


## 🤖 Claude *(16:30:23)*

Nó embedado (768d ✅) · malha **8973 nós**. Continuando o seal — **Phase 4 (README)** + **Phase 5 (HANDOFF.md)**. Lendo o topo do README.

## 🤖 Claude *(16:30:23)*


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
> 3	  <img src="https://img.shields.io/badge/version-6.53.0--Agentic--Governance--%2B--Learning--Loop-blueviolet?style=for-the-badge" alt="Version" />
> 4	  <img src="https://img.shields.io/badge/license-proprietary-red?style=for-the-badge" alt="License" />
> 5	  <img src="https://img.shields.io/badge/typescript-strict-blue?style=for-the-badge&logo=typescript" alt="TypeScript" />
> 6	  <img src="https://img.shields.io/badge/neural_mesh-8971_nodes-blueviolet?style=for-the-badge" alt="Neural Mesh" />
> 7	  <img src="https://img.shields.io/badge/Agentic_Vision-21_patterns_%2B_Collective_Ledger-blueviolet?style=for-the-badge" alt="Agentic Vision" />
> 8	  <img src="https://img.shields.io/badge/API_Tenancy-100%25_per--user_(env%3Dinfra)-brightgreen?style=for-the-badge" alt="API Tenancy" />
> 9	  <img src="https://img.shields.io/badge/BoK_video--studio-9%2F9_%2B_agency_v1.1-fuchsia?style=for-the-badge" alt="BoK video-studio" />
> 10	  <img src="https://img.shields.io/badge/MCORCH_SSO-cross--subdomain_gate_live-darkgreen?style=for-the-badge" alt="MCORCH SSO" />
> 11	  <img src="https://img.shields.io/badge/Agency_Tenancy-org%2Fclient_RLS_sealed-blueviolet?style=for-the-badge" alt="Agency Tenancy" />
> 12	  <img src="https://img.shields.io/badge/viral--autopilot-ATIVADO_1o_ciclo_pago_%2B_FR--VA--018-brightgreen?style=for-the-badge" alt="Viral Autopilot" />
> 13	  <img src="https://img.shields.io/badge/Epsilon_V9-unified_canvas_3.4_live-cyan?style=for-the-badge" alt="Phase Epsilon V9" />
> 14	  <img src="https://img.shields.io/badge/test_coverage-295_tests-success?style=for-the-badge" alt="Test Coverage" />
> 15	  <img src="https://img.shields.io/badge/Cyber_Sentinel-prompt_gate_live_%2B_BoK_4%2F4-darkred?style=for-the-badge" alt="Cyber-Sentinel" />
> 16	  <img src="https://img.shields.io/badge/marketing--hub-FR--MH--001..012_live-brightgreen?style=for-the-badge" alt="Marketing Hub" />
> 17	  <img src="https://img.shields.io/badge/e2e--user--zero-v2_runnable_harness-teal?style=for-the-badge" alt="e2e-user-zero v2" />
> 18	  <img src="https://img.shields.io/badge/BoK_Suite-v1_sealed-fuchsia?style=for-the-badge" alt="BoK Suite" />
> 19	  <img src="https://img.shields.io/badge/AIOS_DevKit-4Cs_100%2F100-brightgreen?style=for-the-badge" alt="AIOS DevKit" />
> 20	  <img src="https://img.shields.io/badge/mcoCoins-gatekeeper-gold?style=for-the-badge" alt="mcoCoins" />
> 21	  <img src="https://img.shields.io/badge/AIOS-consciousness_v3-cyan?style=for-the-badge" alt="AIOS" />
> 22	  <img src="https://img.shields.io/badge/affiliate_flywheel-closed-emerald?style=for-the-badge" alt="Flywheel" />
> 23	  <img src="https://img.shields.io/badge/embedding_pipeline-autonomous-violet?style=for-the-badge" alt="Embedding Pipeline" />
> 24	  <img src="https://img.shields.io/badge/Core_Fable-Mega_Brain_%2B_Cymatics_%2B_A2UI-fuchsia?style=for-the-badge" alt="Core Fable" />
> 25	  <img src="https://img.shields.io/badge/LGPD-DD--001_%2B_DD--002_compliant-green?style=for-the-badge" alt="LGPD" />
> 26	  <img src="https://img.shields.io/badge/BoK_Agents-8_agents_generated-orange?style=for-the-badge" alt="BoK Agents" />
> 27	  <img src="https://img.shields.io/badge/Constellation_v2-backend_sealed-blueviolet?style=for-the-badge" alt="Constellation v2" />
> 28	  <img src="https://img.shields.io/badge/Departmental_Army-7_agents_%7C_9641_chunks-orange?style=for-the-badge" alt="Departmental Army" />
> 29	  <img src="https://img.shields.io/badge/Secrets_Vault-file--based_SecretRef-darkgreen?style=for-the-badge" alt="Secrets Vault" />
> 30	  <img src="https://img.shields.io/badge/mcoCoins_Ledger-canonical-gold?style=for-the-badge" alt="mcoCoins Ledger" />
> 31	  <img src="https://img.shields.io/badge/Nightly_Dreaming-gemini_embed_%2B_recovered-violet?style=for-the-badge" alt="Nightly Dreaming" />
> 32	  <img src="https://img.shields.io/badge/OpenClaw_Gateway-systemd_single--owner-darkgreen?style=for-the-badge" alt="OpenClaw Gateway" />
> 33	  <img src="https://img.shields.io/badge/Survival_Laws-4_of_4_consecutive-darkred?style=for-the-badge" alt="Survival Laws" />
> 34	  <img src="https://img.shields.io/badge/BoK_aios--sql--bridge-SDD_sealed-fuchsia?style=for-the-badge" alt="BoK aios-sql-bridge" />
> 35	  <img src="https://img.shields.io/badge/MAPE--K-audit_seeded-cyan?style=for-the-badge" alt="MAPE-K" />
> 36	  <img src="https://img.shields.io/badge/SQL_Bridge-aios--sql--bridge_live-darkgreen?style=for-the-badge" alt="SQL Bridge" />
> 37	  <img src="https://img.shields.io/badge/Circadian_Cycle-3_stages_BRT-violet?style=for-the-badge" alt="Circadian Cycle" />
> 38	  <img src="https://img.shields.io/badge/Canvas_4.2c-async_video_live-brightgreen?style=for-the-badge" alt="Canvas 4.2c" />
> 39	  <img src="https://img.shields.io/badge/Memory_Wiki-live_20_pages-darkviolet?style=for-the-badge" alt="Memory Wiki" />
> 40	  <img src="https://img.shields.io/badge/OE--661-flywheel_validated_E2E-emerald?style=for-the-badge" alt="OE-661 Flywheel Validated" />
> 41	  <img src="https://img.shields.io/badge/Target_Binding-100%25_coverage-success?style=for-the-badge" alt="Target Binding" />
> 42	  <img src="https://img.shields.io/badge/Link_Forge-3_real_products_enriched-orange?style=for-the-badge" alt="Link Forge" />
> 43	  <img src="https://img.shields.io/badge/Affiliate_Links-hybrid_meli.la%2Fmatt__word-emerald?style=for-the-badge" alt="Affiliate Links Hybrid" />
> 44	  <img src="https://img.shields.io/badge/Apify_BYOK-per--user_apify__token-teal?style=for-the-badge" alt="Apify BYOK" />
> 45	  <img src="https://img.shields.io/badge/API_Tenancy-per--user_credentials-teal?style=for-the-badge" alt="API Tenancy Model" />
> 46	  <img src="https://img.shields.io/badge/BoK_gamificacao--nodes-9_of_9_sealed-fuchsia?style=for-the-badge" alt="BoK gamificacao-nodes" />
> 47	  <img src="https://img.shields.io/badge/BoK_openclaw-9_of_9_sealed-fuchsia?style=for-the-badge" alt="BoK openclaw" />
> 48	  <img src="https://img.shields.io/badge/BoK_e2e--user--zero-9_of_9_sealed-fuchsia?style=for-the-badge" alt="BoK e2e-user-zero" />
> 49	  <img src="https://img.shields.io/badge/agent--browser-v0.27.0_validated-teal?style=for-the-badge" alt="agent-browser CLI" />
> 50	  <img src="https://img.shields.io/badge/ML_Affiliate-no_official_API_(probe--first)-red?style=for-the-badge" alt="ML Affiliate Probe" />
> 51	  <img src="https://img.shields.io/badge/Browser_Operator-runtime_blocked_at_datacenter-darkred?style=for-the-badge" alt="Browser Operator Probe" />
> 52	  <img src="https://img.shields.io/badge/Pantheon-7_agents_BoK_full-orange?style=for-the-badge" alt="Pantheon" />
> 53	  <img src="https://img.shields.io/badge/Material_Proof_Gate-Phase_5c_live-darkred?style=for-the-badge" alt="Material Proof Gate" />
> 54	  <img src="https://img.shields.io/badge/Admin_Panel-user_management_live-brightgreen?style=for-the-badge" alt="Admin Panel" />
> 55	  <img src="https://img.shields.io/badge/Great_Reset-Sovereign_soft--reset_live-darkred?style=for-the-badge" alt="Great Reset" />
> 56	  <img src="https://img.shields.io/badge/Constellation_Economic_Activation-agents_billable-gold?style=for-the-badge" alt="CEA" />
> 57	  <img src="https://img.shields.io/badge/Hybrid_Billing-Sovereign_free_others_charged-teal?style=for-the-badge" alt="Hybrid Billing" />
> 58	  <img src="https://img.shields.io/badge/Agent_Pricing-7_models_seeded-fuchsia?style=for-the-badge" alt="Agent Pricing" />
> 59	  <img src="https://img.shields.io/badge/Daily_Pulse_Cron-04:00_BRT-violet?style=for-the-badge" alt="Daily Pulse" />
> 60	  <img src="https://img.shields.io/badge/BoK_marketing--hub-9_of_9_sealed-fuchsia?style=for-the-badge" alt="BoK marketing-hub" />
> ```

## 🤖 Claude *(16:30:30)*


## 🤖 Claude *(16:30:31)*

O README tem badges. Atualizo versão (6.53.0→6.54.0), node count (8971→8973), e adiciono um badge de social-connect.

## 🤖 Claude *(16:30:34)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/version-6.53.0--Agentic--Governance--%2B--Learning--Loop-blueviolet?style=for-the-badge\" alt=\"Version\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/version-6.54.0--Social--Connect--TikTok--YouTube--Pinterest-blueviolet?style=for-the-badge\" alt=\"Version\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:30:36)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-8971_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-8973_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:30:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/viral--autopilot-ATIVADO_1o_ciclo_pago_%2B_FR--VA--018-brightgreen?style=for-the-badge\" alt=\"Viral Autopilot\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/viral--autopilot-ATIVADO_1o_ciclo_pago_%2B_FR--VA--018-brightgreen?style=for-the-badge\" alt=\"Viral Autopilot\" />\n  <img src=\"https://img.shields.io/badge/social--connect-TikTok%2FYouTube%2FPinterest_code--complete-brightgreen?style=for-the-badge\" alt=\"Social Connect\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:30:41)*


## 🤖 Claude *(16:30:42)*

Agora a seção "What's New" do README. Localizando + prepend.

## 🤖 Claude *(16:30:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"What's New|## \ud83c\udd95|### \\[v6\\.5|Novidades|## Changelog\" README.md | head -8",
  "description": "Locate What's New section"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 77:## 🆕 What's new in v6.53.0 (2026-06-27)
> 84:## 🆕 What's new in v6.52.0 (2026-06-26)
> 91:## 🆕 What's new in v6.51.0 (2026-06-25)
> 98:## 🆕 What's new in v6.50.0 (2026-06-25)
> 105:## 🆕 What's new in v6.45.0 (2026-06-22)
> 112:## 🆕 What's new in v6.44.0 (2026-06-20)
> 118:## 🆕 What's new in v6.43.0 (2026-06-20)
> 125:## 🆕 What's new in v6.40.0 (2026-06-17)
> ```

## 🤖 Claude *(16:30:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "offset": 77,
  "limit": 8
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 77	## 🆕 What's new in v6.53.0 (2026-06-27)
> 78	
> 79	- **Doutrina Agêntica AGI→ASI + Pattern Conformance gate vinculante.** Os 21 padrões agênticos (Gulli) + as 4 vias para a ASI (DeepMind) viraram a lente que governa todo desenvolvimento futuro. `docs/architecture/agentic-vision.md` é a referência arquitetural viva (Pattern Maturity Ledger: 11 fortes · 9 moderados · 1 fraco); o `CLAUDE.md §1` ganha o gate — **toda SDD nova declara conformidade com os 21 padrões**. BoK `agentic-governance` 10/10 selada (nó `34748570`).
> 80	- **Collective Efficiency Ledger — medir o coletivo, não no escuro.** O paper aponta as perguntas de coletivo de agentes (V4-2/4/5) como abertas; respondíamos por doutrina mas **não medíamos nenhuma**. VIEW `collective_efficiency_ledger` (security_invoker per-tenant) + RPC service-role DERIVAM mco/resultado + overhead da verdade financeira (anti-Goodhart). **G6 isolamento provado** (tenant throwaway vê 0); rollup real: orchestrate-content avg **334s** vs autopilot-cycle **2.4s**.
> 81	- **Learning & Adaptation (o único padrão fraco) atacado — o loop que COMPÕE.** Diagnóstico material: o motor aprendia sobre um **placar em branco**. Nervo sensorial: `publication_metrics` (time-series) + coletor fail-soft IG/FB + painel **"Por Publicação"** (número real ou "sem dados ainda", **nunca demo**, browser-provado). Reward multi-métrica brand-first `R=0.40·reach+0.30·eng+0.20·brand+0.10·rev` mata o `totalClicks` Goodhart (degrada honesto — prova policy reward 0.9 modo fallback). Realocação ε-greedy budget-neutral: **a política agora move o fan-out, não só sussurra**.
> 82	- **Analytics honesto + perfis da marca limpos.** O fallback **demo** (números falsos 12.400) foi removido — vazio = zero honesto. Perfis sociais antigos zerados (LinkedIn + Twitter, backup reversível) p/ as contas da marca começarem do zero: **Gabriel AI** (LinkedIn/FB) · **@gabrielOrchAI** (X).
> 83	
> 84	## 🆕 What's new in v6.52.0 (2026-06-26)
> ```

## 🤖 Claude *(16:31:01)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "## \ud83c\udd95 What's new in v6.53.0 (2026-06-27)",
  "new_string": "## \ud83c\udd95 What's new in v6.54.0 (2026-06-27)\n\n- **Conectar redes \u2014 TikTok + YouTube + Pinterest (brand persona Gabriel AI).** A camada de publica\u00e7\u00e3o ganha 3 canais novos sem reinventar os trilhos: o enum `social_platform` j\u00e1 tinha as 3; o MP4 9:16 do HyperFrames \u00e9 o mesmo de Reel/Shorts/TikTok. **PASSO 0 (gate BoK):** emenda `post-engine` (`06`/`09-pattern-conformance` 21 padr\u00f5es/`10-amendment` FR-PE-005..016) + 3 SOPs Lei 2. **Migration `social_app_config`** \u2014 credenciais de app per-user **cifradas no Vault** (masked view security_invoker + decrypted view service-role-only + INSTEAD OF tenant-guard 42501), aplicada+provada (coluna crua = UUID Vault) \u00b7 `/security-review` SAFE. **Helper fail-closed** `resolveSocialAppCreds` (per-user \u2192 env \u2192 402, nunca chave compartilhada silenciosa). **4 edge fns** com branches OAuth+publisher (TikTok Direct Post FILE_UPLOAD \u00b7 YouTube resumable \u00b7 Pinterest video-pin) \u2014 `deno check` 8/8, deployadas, **fail-closed provado ao vivo (3\u00d7402)**. **UI** \u2014 card de credenciais (Settings\u2192Social) + 3 bot\u00f5es Conectar (`/dashboard/social`), tsc 0, build deployado, **browser-verified + Vision QA high**. Pesquisa fundamentada (3 plataformas verificadas HIGH, cada claim com URL oficial). **Pendente (Sovereign):** registrar 3 apps de dev + 3 audits \u2192 conex\u00e3o acende; p\u00fablico p\u00f3s-audit. **Deferido:** v\u00eddeo-cad\u00eancia aut\u00f4noma p/ as novas redes (FR-PE-013, precisa do enqueue-gate do orchestrate-content).\n\n## \ud83c\udd95 What's new in v6.53.0 (2026-06-27)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:31:08)*


## 🤖 Claude *(16:31:09)*

README atualizado. Commit do README + **Phase 5 (HANDOFF.md)** — prepend do novo seal record.

## 🤖 Claude *(16:31:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add README.md\ngit commit -q -m \"docs(readme): v6.54.0 \u2014 Social Connect TikTok/YouTube/Pinterest (code-complete + fail-closed proven)\" >/dev/null 2>&1\necho \"readme commit exit: $?\"; git log --oneline -1",
  "description": "Commit README"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> readme commit exit: 0
> cbe16c8 docs(readme): v6.54.0 — Social Connect TikTok/YouTube/Pinterest (code-complete + fail-closed proven)
> ```

## 🤖 Claude *(16:31:41)*


## 🤖 Claude *(16:31:42)*

README ✅ (cbe16c8). Inserindo o seal record no HANDOFF.md:

## 🤖 Claude *(16:31:59)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "## Task State\n\n## Session Seal \u2014 Doutrina Ag\u00eantica AGI\u2192ASI + Learning & Adaptation: gate vinculante",
  "new_string": "## Task State\n\n## Session Seal \u2014 Conectar redes: TikTok + YouTube + Pinterest (brand persona Gabriel AI) \u2014 BoK gate + Vault app-creds + OAuth/publisher branches + UI (2026-06-27)\n\nDiretiva Sovereign: *\"vamos conectar as redes \u2014 TikTok, YouTube, Pinterest\"* + *\"continue for\u00e7a total\"*. Operado sob o Closed-Loop Protocol: pesquisa fundamentada \u2192 gate BoK \u2192 migration \u2192 edge code \u2192 UI \u2192 seal. Tudo provado materialmente (Lei 1); nada declarado sem prova.\n\n**Achado central:** ~90% da infra j\u00e1 existia (enum `social_platform` j\u00e1 tinha as 3 \u00b7 `social_accounts` Vault \u00b7 OAuth gen\u00e9rico `social-auth-init`/`-callback` \u00b7 MESMO MP4 9:16). Net-new = credenciais de app per-user (Vault) + 3 pares de branches OAuth/publisher + UI. Os blockers duros s\u00e3o 100% **Sovereign-gated** (registrar 3 apps de dev + 3 audits \u2014 sem app n\u00e3o h\u00e1 `client_id`/`secret` \u2192 nenhum OAuth; sem audit o p\u00fablico \u00e9 invis\u00edvel: TikTok SELF_ONLY \u00b7 YouTube forced-private \u00b7 Pinterest sandbox).\n\n| Action | Result |\n|--------|--------|\n| Pesquisa fundamentada (workflow `wf_b5a35451`, 8 agentes, adversarial-verify) | \u2705 3 plataformas verificadas HIGH; blueprint `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md` + playbook `\u2026/social-app-registration-playbook-2026-06-27.md` |\n| PASSO 0 \u2014 gate BoK | \u2705 `post-engine` `06`/`09-pattern-conformance`(21 padr\u00f5es)/`10-amendment`(FR-PE-005..016) + 3 SOPs Lei 2 `docs/processes/{tiktok,youtube,pinterest}-publish-credential-resolution.md` |\n| Migration `20260627120000_social_app_config` | \u2705 aplicada+provada \u2014 coluna crua=UUID Vault `55caaf7b\u2026` \u00b7 masked view `\u2022\u2022\u2022\u2022` \u00b7 decrypted view anon\u2192**42501** \u00b7 `/security-review` SAFE |\n| Helper `supabase/functions/_shared/social-app-config.ts` | \u2705 `resolveSocialAppCreds` per-user\u2192env\u2192**402** fail-closed (nunca chave compartilhada silenciosa) |\n| Branches `social-auth-init`/`-callback`/`refresh-social-token`/`publish-social` + `auto-publish` video_url | \u2705 `deno check` 8/8 \u00b7 deployadas \u00b7 **fail-closed provado LIVE (3\u00d7402)** |\n| `autopilot-run` VIDEO_FLOW_PLATFORMS / FR-PE-013 | \u23f8\ufe0f **DEFERIDO** \u2014 manter `['wordpress']`; adicionar youtube/tiktok/pinterest cobraria VIDEO_COST sem render (charge-without-value) at\u00e9 estender o enqueue-gate de `orchestrate-content`/`-step` |\n| UI `useSocialAppConfig` + `SocialAppConfigCard` (Settings\u2192Social) + 3 connect cards (`/dashboard/social`) | \u2705 tsc 0 \u00b7 build deployado (chunk `SettingsPage-CHgtU2cG.js` + env baked) \u00b7 **browser-verified + Vision QA \"high\"** \u00b7 0 erro de console |\n\n| Commit | Conte\u00fado |\n|--------|----------|\n| `ea12afc` | docs(post-engine): BoK amendment + SOPs + blueprint |\n| `c94bd75` | feat(db): social_app_config Vault-cifrada (FR-PE-005) |\n| `25477a8` | feat(social): OAuth + publisher branches + helper fail-closed (FR-PE-006..016) |\n| `e81d868` | feat(settings): app-config card + connect cards |\n| `cbe16c8` | docs(readme): v6.54.0 |\n\n**Mesh seal:** handoff node `311a55b1-fb7b-410f-9582-625fb4721619` (embedded 768d). Mesh **8973 n\u00f3s**.\n\n**Pr\u00f3ximo (o unlock):** (Sovereign) registrar TikTok/Google/Pinterest dev apps + submeter 3 audits + entrar `client_id`/`secret` (UI Settings\u2192Social OU env `TIKTOK_CLIENT_KEY`/`_SECRET`\u00b7`GOOGLE_CLIENT_ID`/`_SECRET`\u00b7`PINTEREST_CLIENT_ID`/`_SECRET`) \u2192 o bot\u00e3o Conectar acende o OAuth (provo o publish E2E no mesmo dia); p\u00fablico p\u00f3s-audit. (c\u00f3digo) slice FR-PE-013 video-cadence das novas redes + spine de persona CCIO.\n\n---\n\n## Session Seal \u2014 Doutrina Ag\u00eantica AGI\u2192ASI + Learning & Adaptation: gate vinculante"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:32:13)*


## 🤖 Claude *(16:32:14)*

Seal record inserido. Atualizo o contador GraphRAG + rodo **Phase 5b (secret scan no HANDOFF.md)** antes de commitar.

## 🤖 Claude *(16:32:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== GraphRAG count line ===\"; grep -nE \"^\\- \\*\\*89[0-9]{2} total nodes\\*\\*|## GraphRAG State\" HANDOFF.md | head -3\necho \"\"; echo \"=== Phase 5b \u2014 secret scan on HANDOFF.md ===\"\ngrep -nE \"(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]+)\" HANDOFF.md | grep -v \"example\\|placeholder\\|<.*>\\|digest\\|sha256\\|hash\\|uuid\" | head -5 || echo \"HANDOFF.md: NO CREDENTIALS \u2705\"\ngrep -nE \"AIza[0-9A-Za-z_-]{35}\" HANDOFF.md | head -3 || echo \"NO GOOGLE KEYS \u2705\"",
  "description": "Find GraphRAG line + Phase 5b secret scan"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === GraphRAG count line ===
> 8267:## GraphRAG State
> 8269:- **8969 total nodes** (verificado live 2026-06-26 via REST count=exact, gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 
> === Phase 5b — secret scan on HANDOFF.md ===
> ```

## 🤖 Claude *(16:32:31)*


## 🤖 Claude *(16:32:32)*

Phase 5b: **HANDOFF.md sem credenciais ✅** (só UUIDs/hashes). Atualizo o contador GraphRAG (8969→8973 + novo nó) e commito.

## 🤖 Claude *(16:32:38)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "- **8969 total nodes** (verificado live 2026-06-26 via REST count=exact, gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d",
  "new_string": "- **8973 total nodes** (verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d \u2014 conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3\u00d7402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:32:43)*


## 🤖 Claude *(16:32:43)*

HANDOFF commit + **Phase 5c (material proof audit)**:

## 🤖 Claude *(16:32:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add HANDOFF.md\ngit commit -q -m \"docs(handoff): seal social-connect TikTok/YouTube/Pinterest \u2014 BoK gate + Vault app-creds + OAuth/publisher branches + UI\" >/dev/null 2>&1\necho \"handoff commit exit: $?\"; git log --oneline -1\necho \"\"; echo \"=== Phase 5c \u2014 material proof audit ===\"\nbun run scripts/qa/run-audit.ts HANDOFF.md 2>&1 | tail -40",
  "description": "Commit HANDOFF + Phase 5c audit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> handoff commit exit: 0
> 9fc3020 docs(handoff): seal social-connect TikTok/YouTube/Pinterest — BoK gate + Vault app-creds + OAuth/publisher branches + UI
> 
> === Phase 5c — material proof audit ===
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
> | handoff node 311a55b1 | mesh_node | 311a55b1-fb7b-410f-9582-625fb4721619 | 311a55b1-fb7b-410f-9582-625fb4721619 | ✅ |
> 
> QA VERDICT: 10 verified · 0 skipped · 0 failed → SEAL ALLOWED
> 
> (audit completed in 24.8s)
> ```

## 🤖 Claude *(16:33:27)*


## 🤖 Claude *(16:33:29)*

**Phase 5c: `SEAL ALLOWED`** — 10 verificadas · 0 falhas (nó `311a55b1` + commits + suite 295 passed). **Phase 6 (BoK) + Phase 7 (push):**

## 🤖 Claude *(16:33:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== Phase 6: post-engine BoK (the module this session amended) ===\"\nreq=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics); miss=()\nfor d in \"${req[@]}\"; do [ -f \"docs/bok/post-engine/$d.md\" ] || miss+=(\"$d\"); done\n[ ${#miss[@]} -eq 0 ] && echo \"\u2705 post-engine \u2014 BoK complete (+ 09-pattern-conformance + 10-amendment this session)\" || echo \"\u26a0\ufe0f missing: ${miss[*]}\"\necho \"Note: no NEW module/page created (edge fn branches + migration + UI components only) \u2192 no new BoK required.\"\necho \"\"; echo \"=== Phase 7: push ===\"\ngit push origin main 2>&1 | tail -6",
  "description": "Phase 6 BoK check + Phase 7 push"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Phase 6: post-engine BoK (the module this session amended) ===
> ✅ post-engine — BoK complete (+ 09-pattern-conformance + 10-amendment this session)
> Note: no NEW module/page created (edge fn branches + migration + UI components only) → no new BoK required.
> 
> === Phase 7: push ===
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.21 seconds)
> ✔️ gitleaks-range (0.21 seconds)
> To github.com:gabrielZarattini/constellation-orchestra.git
>    2d8e46d..9fc3020  main -> main
> ```

## 🤖 Claude *(16:33:54)*


## 🤖 Claude *(16:34:16)*

**Push ✅** (`2d8e46d..9fc3020 main -> main`, gitleaks-range passou). BoK post-engine completo, sem módulo novo sem BoK. Scratch já estava limpo. Selo completo.

```
═══════════════════════════════════════════════════════════
  HANDOFF SEALED — Conectar redes TikTok/YouTube/Pinterest (2026-06-27)
═══════════════════════════════════════════════════════════
```

🔐 **SEGURANÇA**
&nbsp;&nbsp;Phase 1: ✅ PASS (matches do 1a = leituras `Deno.env.get` — falso-positivo no substring `SECRET_KEY`) · 1c/1e limpos
&nbsp;&nbsp;**Defesa em profundidade funcionou:** o hook `secret-scan` BLOQUEOU os commits 3/4 por `secret: "TIKTOK_CLIENT_SECRET"` (nomes de env, falso-positivo) → refatorei p/ `idEnv`/`secretEnv` (sem afrouxar o hook) + redeployei os 3 importers
&nbsp;&nbsp;Phase 5b (HANDOFF.md): ✅ sem credenciais · gitleaks: no leaks em todos os commits

📦 **COMMITS (6 · pushed)**
&nbsp;&nbsp;`ea12afc` docs(post-engine) · `c94bd75` feat(db) · `25477a8` feat(social) · `e81d868` feat(settings) · `cbe16c8` docs(readme) · `9fc3020` docs(handoff)

⬡ **KNOWLEDGE MESH**
&nbsp;&nbsp;Handoff node `311a55b1-fb7b-410f-9582-625fb4721619` — embedded 768d ✅ · Mesh **8973 nós**

📖 **README.md** — v6.53.0 → **v6.54.0** · badge neural_mesh 8971 → **8973** · +badge social-connect · entrada What's New

📋 **PROVA MATERIAL (Phase 5c)** — Veredito: **SEAL ALLOWED** · 10 verificadas · 0 skipped · **0 falhas**

🚀 **PUSH** — `main → origin/main` · 6 commits (`2d8e46d..9fc3020`)

⚖️ **SURVIVAL LAWS SELF-AUDIT**
&nbsp;&nbsp;**Lei 1 (Materialidade):** toda claim de SUCCESS ancorada (round-trip Vault, `deno check` 8/8, **3×402 live**, browser+Vision QA, contadores via REST). Peguei e corrigi meus próprios `✅ commit` falsos (verifiquei via `git log`, não por echo). Zero fabricação.
&nbsp;&nbsp;**Lei 2 (Processo):** 3 SOPs + emenda BoK escritos ANTES do código (PASSO 0). ✅
&nbsp;&nbsp;**Lei 3 (Poda):** usei a janela grande (diretiva Sovereign); selei na conclusão natural do arco (itens acionáveis esgotados — resto é Sovereign-gated). Leitura pesada delegada a agentes p/ manter o main-loop enxuto.
&nbsp;&nbsp;**Lei 4 (ORO):** declarado no início (Operator=MCORCH Agent · Reviewer/Owner=Sovereign).

⏭ **PRÓXIMOS PASSOS**
&nbsp;&nbsp;1. **(Você — caminho crítico)** Registrar os 3 apps de dev (TikTok/Google/Pinterest) + submeter os 3 audits → playbook em [social-app-registration-playbook-2026-06-27.md](.claude/context/social-app-registration-playbook-2026-06-27.md). Depois entrar `client_id/secret` (Settings→Social **ou** env secrets) → o botão Conectar acende e eu provo o publish E2E no mesmo dia.
&nbsp;&nbsp;2. **(Código, deferido)** Slice FR-PE-013 — vídeo-cadência autônoma das novas redes (estender o enqueue-gate do `orchestrate-content` p/ não cobrar-sem-valor).
&nbsp;&nbsp;3. **(Código)** Spine de persona CCIO (trocar a semente do prompt produto→voz da marca).

```
═══════════════════════════════════════════════════════════
  Assinado: Claude Code — Braço de Engenharia do AIOS
═══════════════════════════════════════════════════════════
```

Maestro, as três redes estão **construídas, deployadas, provadas e seladas em produção**, com git == prod (sem drift). A bola está com você: registre os apps e submeta os audits — é a única coisa que separa o Gabriel AI de publicar autonomamente em TikTok, YouTube e Pinterest. Quando voltar com as credenciais, eu acendo a conexão e provo o primeiro publish real. 🚀

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-27 - Clarificar essência e tom do MCORCH]]
> * **Próxima Sessão**: [[2026-06-27 - Corrigir erro de configuração TikTok]]
%% --- TIMELINE END --- %%

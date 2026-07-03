# Resolver expiração frequente de token Google OAuth
**Date:** 2026-07-03 | **Session ID:** `7bb4586f-3050-4a11-99ef-569c4b75c080`

---

## 👤 User *(18:09:08)*

<command-message>loop</command-message>
<command-name>/loop</command-name>
<command-args>Você é o MCORCH Master Execution Agent em MALHA FECHADA AUTÔNOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado — BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review se houver migration → commit granular (Workflow p/ tarefas substantivas); (3) ao bater em portão Sovereign (biometria/DNS/OAuth/GO/decisão), NÃO improvise — registre na Fila de Ação Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada iteração.</command-args>

## 👤 User *(18:09:08)*

# /loop — schedule a recurring or self-paced prompt

Parse the input below into `[interval] <prompt…>` and schedule it.

## Parsing (in priority order)

1. **Leading token**: if the first whitespace-delimited token matches `^\d+[smhd]$` (e.g. `5m`, `2h`), that's the interval; the rest is the prompt.
2. **Trailing "every" clause**: otherwise, if the input ends with `every <N><unit>` or `every <N> <unit-word>` (e.g. `every 20m`, `every 5 minutes`, `every 2 hours`), extract that as the interval and strip it from the prompt. Only match when what follows "every" is a time expression — `check every PR` has no interval.
3. **No interval**: otherwise, the entire input is the prompt and you'll self-pace dynamically (see "Dynamic mode" below).

If the resulting prompt is empty, show usage `/loop [interval] <prompt>` and stop.

Examples:
- `5m /babysit-prs` → interval `5m`, prompt `/babysit-prs` (rule 1)
- `check the deploy every 20m` → interval `20m`, prompt `check the deploy` (rule 2)
- `run tests every 5 minutes` → interval `5m`, prompt `run tests` (rule 2)
- `check the deploy` → no interval → dynamic mode, prompt `check the deploy` (rule 3)
- `check every PR` → no interval → dynamic mode, prompt `check every PR` (rule 3 — "every" not followed by time)
- `5m` → empty prompt → show usage

## Offer cloud first

Before any scheduling step, check whether EITHER is true:
- the parsed interval (rule 1 or 2) is **≥60 minutes**, or
- regardless of which rule matched, the original input uses daily phrasing ("every morning", "daily", "every day", "each night", "every weekday")

If either is true, call AskUserQuestion first:
- `question`: "This loop stops when you close this session. Set it up as a cloud schedule instead so it keeps running?"
- `header`: "Schedule"
- `options`: `[{label: "Cloud schedule (recommended)", description: "Runs in Anthropic's cloud even after you close this session"}, {label: "This session only", description: "Runs in this terminal until you exit"}]`

If they pick **Cloud schedule**: do NOT call CronCreate. Invoke the `schedule` skill directly via the Skill tool with `args` set to their original input verbatim (e.g. `Skill({skill: "schedule", args: "every morning tell me a joke"})`), then follow that skill's instructions to completion. Do NOT tell the user to run /schedule themselves. **Then stop — do not continue to any section below** (no CronCreate, no ScheduleWakeup, no "execute the prompt now").
If they pick **This session only**:
- If the trigger was a parsed ≥60-minute interval (rule 1 or 2): continue below with that interval.
- If the trigger was daily phrasing only (rule 3, no parsed interval): do NOT call CronCreate. Explain that a daily-cadence loop won't fire before this session closes, so there's nothing useful to schedule locally — suggest they either pick Cloud schedule, or re-run `/loop` with an explicit shorter interval (e.g. `/loop 1h <prompt>`) if they want a session loop. Then stop.
If neither trigger condition was met: continue below.

## Fixed-interval mode (rules 1 and 2)

Convert the interval to a cron expression:

| Interval pattern      | Cron expression     | Notes                                    |
|-----------------------|---------------------|------------------------------------------|
| `Nm` where N ≤ 59   | `*/N * * * *`     | every N minutes                          |
| `Nm` where N ≥ 60   | `0 */H * * *`     | round to hours (H = N/60, must divide 24)|
| `Nh` where N ≤ 23   | `0 */N * * *`     | every N hours                            |
| `Nd`                | `0 0 */N * *`     | every N days at midnight local           |
| `Ns`                | treat as `ceil(N/60)m` | cron minimum granularity is 1 minute  |

**If the interval doesn't cleanly divide its unit** (e.g. `7m` → `*/7 * * * *` gives uneven gaps at :56→:00; `90m` → 1.5h which cron can't express), pick the nearest clean interval and tell the user what you rounded to before scheduling.

Then:
1. Call CronCreate with: `cron` (the expression above), `prompt` (the parsed prompt verbatim), `recurring: true`.
2. Briefly confirm: what's scheduled, the cron expression, the human-readable cadence, that recurring tasks auto-expire after 7 days, and that the user can cancel sooner with CronDelete (include the job ID). Only if you did NOT show the cloud-offer AskUserQuestion above (i.e., neither trigger condition applied), end the confirmation with this exact line on its own, italicized: `_Runs until you close this session · For durable cloud-based loops, use /schedule_`. If the user already answered that question, omit this line.
3. **Then immediately execute the parsed prompt now** — don't wait for the first cron fire. If it's a slash command, invoke it via the Skill tool; otherwise act on it directly.

## Dynamic mode (rule 3 — no interval)

The user wants you to self-pace. Decide what makes the next iteration worth running — a passage of time, or an observable event.

1. **Run the parsed prompt now.** If it's a slash command, invoke it via the Skill tool; otherwise act on it directly.
2. **If the next run is gated on an event** (CI finishing, a log line matching, a file changing, a PR comment) and no Monitor is already running for it: arm one now with `persistent: true`. Its events arrive as `<task-notification>` messages and wake this loop immediately — you do not wait for the ScheduleWakeup deadline. Arm once; on later iterations call TaskList first and skip this step if a monitor is already running.
3. **Briefly confirm**: that you're self-pacing, whether a Monitor is the primary wake signal, that you ran the task now, and what fallback delay you're about to pick. Write this as text *before* calling ScheduleWakeup — the turn ends as soon as that tool returns.
4. **Then, as the last action of this turn, call ScheduleWakeup** with:
   - `delaySeconds`: with a Monitor armed this is the **fallback heartbeat** — how long to wait if no event fires (lean 1200–1800s; idle ticks past the 5-minute cache window are pure overhead). Without a Monitor this is the cadence — pick based on what you observed. Read the tool's own description for cache-aware delay guidance.
   - `reason`: one short sentence on why you picked that delay.
   - `prompt`: the full original /loop input verbatim, prefixed with `/loop ` so the next firing re-enters this skill and continues the loop. For example, if the user typed `/loop check the deploy`, pass `/loop check the deploy` as the prompt.
5. **If you were woken by a `<task-notification>`** rather than this prompt: handle the event in the context of the loop task, then call ScheduleWakeup again with the same `prompt` and the same 1200–1800s `delaySeconds` from step 4 — the Monitor remains the wake signal; this only resets the safety net.
6. **To stop the loop**, omit the ScheduleWakeup call and TaskStop any Monitor you armed (use TaskList to find the task ID if it is no longer in context). Before you stop, send a one-line outcome via PushNotification — the user may be away and waiting to hear it's done. Skip this if you're stopping because the user just told you to; they're already here.

## Input

Você é o MCORCH Master Execution Agent em MALHA FECHADA AUTÔNOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado — BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review se houver migration → commit granular (Workflow p/ tarefas substantivas); (3) ao bater em portão Sovereign (biometria/DNS/OAuth/GO/decisão), NÃO improvise — registre na Fila de Ação Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada iteração.

## 👤 User *(18:09:14)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(18:09:14)*

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
  if [ "$slug" = "security" ]; then
    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)
    missing=()
    for doc in "${required_sec[@]}"; do
      [ -f "docs/bok/security/$doc.md" ] || missing+=("$doc")
    done
    [ ${#missing[@]} -eq 0 ] && echo "✅ security — BoK complete (ciso-4-artifact)" || echo "⚠️ security — missing: ${missing[*]}"
    continue
  fi
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


## 🤖 Claude *(18:09:16)*


## 🤖 Claude *(18:09:17)*

I'll execute the ShakeHands /handson pickup ritual. Starting with the pre-flight checks in parallel.

## 🤖 Claude *(18:09:18)*


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
> c38519a docs(handoff): seal loop it.1+it.2 — anticorpo assets owner-signing + BoK Higgsfield MCP (mesh 9048)
> 19d20b5 docs(readme): v6.83.2 — loop it.1+it.2 (anticorpo assets + BoK Higgsfield MCP, mesh 9048)
> 81e6492 chore(loop): registra it.2 2026-07-03 — BoK amendment Higgsfield MCP + gate OAuth na Fila
> 34bdb64 docs(bok): amendment Higgsfield MCP connector (OAuth per-user) — fecha gate Closed-Loop 3.5
> c000086 chore(loop): registra it.1 2026-07-03 — anticorpo de assinatura owner-scoped shipped
> 324d9a6 docs(assets): registra o anticorpo do Fix Assets no SOP + Key Files Reference
> 44d3d3f test(assets): anticorpo re-executável de assinatura owner-scoped em bucket privado
> ---STATUS---
>  M .agents/workflows/handson.md
> ---DIFFSTAT---
>  .agents/workflows/handson.md | 10 ++++++++++
>  1 file changed, 10 insertions(+)
> ```

## 🤖 Claude *(18:09:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---megabrain---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---chroma---\"; curl -s http://localhost:8001/api/v2/heartbeat; echo \"---bok---\"; ls docs/bok/ 2>/dev/null; echo \"---handoff-wc---\"; wc -l HANDOFF.md; echo \"---scratch---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "Infra, BoK suites, HANDOFF size, scratch"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 4 days (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> ---megabrain---
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> ---chroma---
> {"nanosecond heartbeat":1783102161490943823}---bok---
> agentic-governance
> agentic-workspace
> aios-sql-bridge
> authenticated-browser-operator
> avatar-clone-ai
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
> spaces-evolution
> video-studio
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> ---handoff-wc---
> 9399 HANDOFF.md
> ---scratch---
> scratch has files
> ```

## 🤖 Claude *(18:09:22)*


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

## 🤖 Claude *(18:09:25)*


## 🤖 Claude *(18:09:25)*

TypeScript is clean. Now reading HANDOFF head + tail and other context in parallel.

## 🤖 Claude *(18:09:26)*


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
> 14	| **Loop it.1 — Anticorpo de assinatura owner-scoped (Fix Assets)** | ✅ `scripts/qa/smoke-asset-owner-signing.ts` 6/6 LIVE hermético (owner-sign 200 · cross-sign BLOCKED · enumeração 0 · id-squat neutralizado · is_public=0); fecha Mandato Obstáculo→Síntese |
> 15	| **Loop it.2 — BoK amendment Higgsfield MCP OAuth connector** | ✅ `docs/bok/spaces-evolution/13-amendment-higgsfield-mcp-connector.md` — gate Closed-Loop 3.5 fechado; contrato vivo provado (401 OAuth · 201 DCR · discovery Clerk); FR-SPACES-015..021 + OTD-SPACES-007; código gated na aprovação Sovereign |
> 16	| **Fix Assets — mídia privada assinável só pelo dono (regressão FECHADA)** | ✅ migration `20260703030000` (3 policies owner-scoped + triggers de id anti-claim + data-repair) + normalizador durável em 13 superfícies; `/security-review` CLOSED 9/10; E2E Vision-APROVADO; 90 assets do User 0 vivos |
> 17	| **Spaces 2d compose — drift FECHADO (OTD-SPACES-003)** | ✅ compose vivo E2E via OpenRouter Nano Banana (10 mco) + bucket privado assinado + sentinel de contrato Higgsfield |
> 18	
> 19	## Handoff Seal Record (2026-07-03) — Loop autônomo: anticorpo de assinatura owner-scoped (it.1) + BoK Higgsfield MCP (it.2)
> 20	
> 21	**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (custo **0 USD/mco** — só auth throwaway + probes públicos).
> 22	
> 23	Duas iterações do `/loop` em malha fechada autônoma, disparadas após o Sovereign confirmar (turno anterior) que a correção de segurança do Fix Assets continua fechada. **it.1** fechou o gap do Mandato Obstáculo→Síntese (o Fix Assets tinha SOP mas não um guard re-executável). **it.2** fechou o gate Closed-Loop 3.5 da diretiva fresca #0b (Higgsfield MCP oficial), fundamentado em probes vivos — corrigindo materialmente a nota anterior (o `/mcp` exige OAuth, não a Platform API key BYOK). Ao fim da it.2 o frontier desbloqueado do backlog esgotou (todo o resto é Sovereign-gated) → selo final.
> 24	
> 25	| Ação | Resultado (Lei 1) |
> 26	|------|-------------------|
> 27	| **it.1 — `scripts/qa/smoke-asset-owner-signing.ts`** | ✅ hermético (minta owner+attacker throwaway + objeto privado sob prefixo de projeto, owner=NULL). **6/6 LIVE**: S1 owner-sign HTTP 200 · S2 cross-sign BLOCKED · S3 enumeração 0 · S4/S4b id-squat de `vm_canvas_projects` neutralizado (trigger regenera id) + assinatura segue BLOCKED · S5 `is_public`-inv=0. `tsc` 0 · gitleaks limpo · 0 usuário órfão. SOP + Key Files atualizados. |
> 28	| **it.2 — BoK amendment Higgsfield MCP** | ✅ contrato vivo provado: `POST /mcp`→401 (`scope="openid email offline_access"`, upstream Clerk) · `POST /oauth2/register`→201 (public client PKCE) · discovery `authorization_code`+`refresh_token`+S256. FR-SPACES-015..021 + tabela `higgsfield_oauth` + Pattern Conformance (7 padrões) + OTD-SPACES-007/008/009 + FMEA FM-HF-01..05 + 8 gates. |
> 29	| **Fila de Ação Sovereign atualizada** | ✅ gate OAuth E2E do Higgsfield (consent Clerk + redirect_uri canônica + GO de gasto) registrado; código da Fatia desbloqueado mas gated na aprovação do amendment (Lei 4). |
> 30	
> 31	| Commit | Conteúdo |
> 32	|--------|----------|
> 33	| `44d3d3f` | test(assets): anticorpo re-executável de assinatura owner-scoped |
> 34	| `324d9a6` | docs(assets): registra anticorpo no SOP + Key Files |
> 35	| `c000086` | chore(loop): registra it.1 |
> 36	| `34bdb64` | docs(bok): amendment Higgsfield MCP connector — fecha gate Closed-Loop 3.5 |
> 37	| `81e6492` | chore(loop): registra it.2 + gate OAuth na Fila |
> 38	
> 39	**Survival Laws Self-audit:** Lei 1 ✅ (todo claim ancorado — smoke 6/6, HTTP 401/201, commit hashes, embed 768d) · Lei 2 ✅ (it.1 sintetiza anticorpo; it.2 É o SOP/BoK antes do código) · Lei 3 ✅ (janela ~12%, longe de 95%; **selo por "backlog desbloqueado vazio", não por janela** — condição explícita do loop) · Lei 4 ✅ (ORO declarado; **não construí código sobre amendment não-aprovado — portão Lei 4 respeitado, registrado na Fila em vez de improvisar**).
> 40	
> 41	## Handoff Seal Record (2026-07-03) — Fix Assets: exibição de mídia privada owner-scoped em TODO o ecossistema
> 42	
> 43	**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (GO do apply de prod) + `/security-review` independente (que achou e me fez fechar 1 HIGH próprio) · Owner = Sovereign (custo: 0 USD — só apply DDL + build; sem gasto de mco/BYOK).
> 44	
> 45	Iteração de loop disparada por diretiva direta do Sovereign: "Fix Assets — a maioria das mídias sumiu; garanta no E2E que aparecem em todos os lugares". **Diagnóstico material (Lei 1) refutou a hipótese de lixo de smoke:** os 90 assets são TODOS do User 0 (`ada39fae`, saldo 4571). A causa real: depois que os buckets de mídia viraram PRIVADOS + owner-scoped (fechando o furo de enumeração cross-tenant OTD-SPACES-001), o app ainda resolvia URL **pública** (`/object/public/…` → HTTP 400 em bucket privado) e o cliente **não conseguia assinar** objetos com prefixo ≠ uid (`owner=NULL` nos uploads service-role; prefixos `<project_id>/` e `<space_id>/`). Escopo: 84 `creative_assets` + 68 `vm_canvas_executions` + 32 `vm_canvas_projects.graph` + 1 `spaces.graph`.
> 46	
> 47	| Ação | Resultado (Lei 1) |
> 48	|------|-------------------|
> 49	| **Migration `20260703030000`** aplicada+registrada em prod | ✅ prova `new_policies=3, id_trigger=1, remaining_public_on_private=0`. 3 policies SELECT owner-scoped (4 rotas, todas `=auth.uid()`: `creative_assets` service-role-only / `spaces.owner_id` / `vm_canvas_projects.user_id` / uid-prefix). |
> 50	| **Triggers de id server-side** (`vm_canvas_projects`+`spaces`, INSERT+UPDATE, id pinado a OLD.id) | ✅ fecham o claim/PK-swap que tornaria o `id` client-writable um oráculo de autorização de storage. |
> 51	| **Data-repair `is_public`** | ✅ 84 rows `is_public=true` em bucket privado → false. |
> 52	| **Bug vivo `canvas-execute:555`** (`p_is_public:true`→false) | ✅ parou de cunhar row morta a cada execução de imagem. |
> 53	| **`src/lib/asset-url.ts`** + `<StorageImg/Video/Audio>` | ✅ `toDisplayUrl`/`useDisplayUrl` extraem `(bucket,key)` de qualquer URL guardada (pública-morta OU assinada-expirada) e mintam signed URL FRESCA no render — durável, sem reescrever jsonb. Fiado em **13 superfícies**. |
> 54	| **`resolveAssetUrl`** (Biblioteca) | ✅ chaveia pelo bucket REAL (não pela coluna `is_public` mentirosa). |
> 55	| **`/security-review` independente** | ✅ **CLOSED 9/10** — achou 1 HIGH cross-tenant que a 1ª versão introduziu (claim via `vm_canvas_projects` id-squat + PK-swap por UPDATE); fechado com os triggers INSERT+UPDATE. |
> 56	| **Cross-tenant provado BLOCKED ao vivo** (throwaway) | ✅ sign direto + claim INSERT (`id=uid_vítima`) + PK-swap UPDATE → TODOS BLOCKED. O furo que a `20260702230000` fechou permanece fechado. |
> 57	| **E2E browser (preview local determinístico + sessão injetada)** | ✅ Biblioteca 67/71 imgs+19 vídeos+90 signed+0 dead-public · Canvas 17/17+4 vídeos+21 signed+0 dead · **Vision-QA APROVADO ×2** + confirmação ocular (90 assets renderizando). |
> 58	
> 59	| Commit | Conteúdo |
> 60	|--------|----------|
> 61	| `6e5e005` | fix(assets): buckets privados assináveis só pelo dono — fecha regressão de mídia sumida |
> 62	| `459cd25` | fix(assets): normalizador durável de URL re-assina mídia em todas as superfícies |
> 63	| `e3f6f9e` | docs(readme): v6.83.1 — Fix Assets (mesh 9047) |
> 64	
> 65	### Arquitetura Fix Assets
> 66	```
> 67	Display (durável, re-assina no render):
> 68	  <StorageImg/Video/Audio src={storedUrl}> → useDisplayUrl → toDisplayUrl
> 69	    parseStorageRef(url) → {bucket,key}  (public-morta OU sign-expirada, ambas)
> 70	      bucket público (generated-videos) → getPublicUrl
> 71	      bucket privado → createSignedUrl(1h)   ← policy owner-scoped deixa o DONO assinar
> ```

## 🤖 Claude *(18:09:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8999,
  "limit": 400
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (25091 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(18:09:28)*


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
> Output too large (47.2KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/tool-results/bwhl9qots.txt
> 
> Preview (first 2KB):
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun 30 01:44 .
> drwx------ 31 ubuntu ubuntu 4096 Jul  3 12:19 ..
> ---sprint---
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.83.1 — Fix Assets: exibição de mídia privada owner-scoped em TODO o ecossistema (2026-07-03)** — diretiva direta do Sovereign ("a maioria das mídias sumiu; garanta E2E que aparecem em todos os lugares"). **Diagnóstico refutou a hipótese de lixo de smoke (Lei 1):** os 90 assets são TODOS do User 0 (`ada39fae`, saldo 4571). Causa real: buckets viraram privados+owner-scoped (correto — fechou enumeração cross-tenant), mas o app resolvia URL **pública** (400 em bucket privado) e o cliente não assinava objeto com prefixo ≠ uid (`owner=NULL` service-role). Escopo: 84 creative_assets + 68 vm_canvas_executions + 32 graphs + 1 space. **Fix:** migration `20260703030000` (3 policies owner-scoped 4-rotas `=auth.uid()` + triggers de id server-side INSERT+UPDATE anti-claim/PK-swap + data-repair is_public) + fix bug vivo `canvas-execute:555` + lib `asset-url.ts` (`toDisplayUrl`/`useDisplayUrl` re-assina no render, cura pública-morta E assinada-expirada) + `<StorageImg/Video/Audio>` em **13 superfícies** + `resolveAssetUrl` chaveia pelo bucket real. **Segurança:** `/security-review` independente **CLOSED 9/10** — achou e me fez fechar 1 HIGH cross-tenant que a 1ª versão introduziu (claim via `vm_canvas_projects` id-squat + PK-swap). Cross-tenant **BLOCKED ao vivo** (throwaway: sign/claim/PK-swap). **Prova:** signing antes FAIL→SIGNED 200 · tsc 0 · build+deploy · deploy canvas-execute · **E2E local determinístico: Biblioteca 67/71 imgs+19 vídeos, Canvas 17/17+4 vídeos, 0 dead-publ
> ...
> </persisted-output>
> ```

## 🤖 Claude *(18:09:33)*


## 🤖 Claude *(18:09:34)*

Scratch is actually clean (only `.`/`..`). Let me grab the tail sections (GraphRAG State, Pending Actions) with a smaller window.

## 🤖 Claude *(18:09:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"GraphRAG State|Pending Actions|Sovereign Action|Fila de A\u00e7\u00e3o|totalNodes|total_nodes|Knowledge Mesh\" HANDOFF.md | tail -20",
  "description": "Locate GraphRAG/Pending sections"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 7247:| `01b38d5` | docs(readme): v5.5.4 — Core v2 UX fixes + Social OAuth ADRs no Knowledge Mesh |
> 7512:### Pending Actions (atualizado)
> 7569:| `supabase/functions/trigger-ingest/index.ts` criado | ✅ Retorna totalNodes · totalEdges · nullEmbeds · embeddedPct · lastIngest |
> 7613:     → retorna { totalNodes, totalEdges, nullEmbeds, embeddedPct, lastIngest }
> 7670:# ── Re-ingesta do AST no Knowledge Mesh ──────────────────────────────
> 7717:Knowledge Mesh, eliminando dezenas de queries exploratórias por sessão; GitHub MCP
> 7830:| Knowledge Mesh — backfill 3 sessões | ✅ 3 nós `handoff` inseridos + embedded 768d para sessões de 2026-05-02 |
> 8032:| `src/hooks/useKnowledgeMesh.ts` — multi-bucket | ✅ Reescrito: 6 priority buckets + bucket recente + semantic search via `search-constellation` + `meshStats` (totalNodes/totalEdges/dominantTypes) + `contextString` com header `[MESH_STATE]` |
> 8042:| `scripts/seed-aios-milestone.ts` | ✅ Insere milestone node no Knowledge Mesh |
> 8045:| `.claude/commands/handoff.md` | ✅ Protocolo v2: 7 fases — security audit, README live badge sync, Knowledge Mesh milestone, push + relatório pt-BR |
> 8052:| `7161efa` | feat(shakehands): handoff v2 — 7-phase protocol com security audit, README sync e Knowledge Mesh milestone |
> 8055:| `08e34bf` | docs(readme): v5.0.0-zeta — Infra Healing + AIOS Consciousness v2 + Knowledge Mesh 2065 |
> 8562:| `src/pages/MemoryPage.tsx` criado | ✅ Full-screen d3-force Knowledge Mesh — rota `/dashboard/constellation/memory` |
> 8759:## Delta v2 Knowledge Mesh Sync Record (2026-04-26)
> 8776:| `55c4fdb` | feat(gitnexus): Delta v2 Knowledge Mesh Sync — 493 nós AST + 344 edges em Supabase |
> 8817:totalNodes:    3100  |  totalEdges:  2900
> 9003:## Pending Actions (Commercial Launch)
> 9057:- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 9163:## GraphRAG State
> 9182:- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> ```

## 🤖 Claude *(18:09:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9163,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 9163	## GraphRAG State
> 9164	
> 9165	- **9047 total nodes** (verificado live 2026-07-03 via REST count=exact, fix-assets-private-bucket-signing seal: +handoff `6e2b32b2-d3fe-461f-b656-9c022927bc03` embedded 768d — Fix Assets: exibição de mídia privada owner-scoped em todo o ecossistema [migration `20260703030000` aplicada 3-policies+2-triggers+data-repair; `/security-review` CLOSED 9/10; cross-tenant BLOCKED ao vivo; E2E Biblioteca+Canvas Vision-APROVADO; 90 assets do User 0 vivos]; commits `6e5e005`/`459cd25`/`e3f6f9e`; prev 9045 do seal Spaces 2d compose `a49aa10`)
> 9166	- **9034 total nodes** (verificado live 2026-07-02 via REST count=exact, spaces-1b-code-complete-apply-gated seal: +handoff `209cbcd8-14ca-4fe2-aad3-3ef7a9409d93` embedded 768d — Spaces Fase 1b CÓDIGO-COMPLETO: SOP S1-S13 + migration ledger `20260702190000` (NÃO aplicada — GO gated) + branch canvas-execute ledger-first + client runGraph/clusters + /security-review SOUND c/ 4 fixes + smoke 8 gates pronto; commits `717abcd`..`ef33b67`; prev 9033)
> 9167	- **9033 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it2-3-reward-weights-spaces-fase1a-final-seal: +handoff `13fd6fe0-372d-4065-a5ae-b25b208718cf` embedded 768d — NFR-VA-010 reward_weights config-as-data no autopilot-analyze [migration `20260702150000` aplicada; resolveRewardConfig fail-safe; smoke 16/16; /security-review NO FINDINGS] + Spaces Fase 1a canvas 72/28 vivo [tabela `spaces` RLS-own migration `20260702170000`; useSpaces+SpaceNodeCard/Spotlight/ParamHUD; vitest 5/5; E2E DB graph=2 nós; Vision-QA APROVADO]; commits `6058e78`/`9ea6ac0`/`271770e`/`3bedef9`; prev 9032)
> 9168	- **9032 total nodes** (verificado live 2026-07-02 via REST count=exact, spaces-bok-seal-and-loop-it1-b5 seal: +handoff `10d8c70b-1e6a-4ca5-a8bf-83687b3f6b28` embedded 768d — suíte BoK spaces-evolution 9/9 completada [seal `8f5fd3fd` documentation_suite + DERIVES_FROM `c4247ef6`→viralmind; 25/25 suítes verdes; Pattern Conformance §11] + B5 Pauta de Receita FR-VA-031 HITL na AutopilotPage [vitest 7/7 · browser-verify User 0 · Vision-QA APROVADO]; commits `4a8fee0`/`367db9b`/`707d9ab`; prev 9023)
> 9169	- **9023 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it4-b4-ewma-final-seal: +handoff `1ddd4e86-7b89-4d13-9330-b5877c96df32` embedded 768d — B4 EWMA multi-ciclo no analyze [janela M=5 decay 0.5, smoke 13/13 gate L7 de estabilização] + selo final da sessão de loop [it.1 G7/fan-out · it.2-3 vision-gate · it.4 B4]; commit `bbc7ad9`; prev 9022)
> 9170	- **9022 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it2-3-vision-gate-both-harnesses seal: +handoff `8ddca90b-decb-4ca6-a857-89addf5134bb` embedded 768d — Vision QA gate mecânico nos 2 harnesses [audit-canvas-ui exit-block + e2e-user-zero Finding P1/ux; prova adversarial PNG branco→REPROVADO] + fix print público dist/; commits `8a41457`/`e511862`/`adf849b`; prev 9021)
> 9171	- **9021 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it1-reshaper-image-anchor-fanout-hygiene seal: +handoff `b31c1336-e693-4dac-9b10-7a743caf2863` embedded 768d — render-decoupling provado resolvido por arquitetura [channel_variants `reused_master` 7 canais no ciclo `77e02fca`] + fatia G7 imagem-pilar por `metadata.pillar_run_id` [smoke 18/18] + fan-out hygiene no autopilot-run; commits `d16ca88`/`b52ea4f`/`75a6e1c`; prev 9020 = seal final it.9 da primária `345cc2a7` [paridade total universo, v6.73.1]; prev 9018/9017 = seals it.5-6/Fase-B; prev 9003)
> 9172	- **9003 total nodes** (verificado live 2026-06-30 via REST count=exact, loop-editor-render-security-hardening seal: +handoff `d02a8570-5195-4206-a918-df3a42423aba` embedded 768d — Loop autônomo 8 iterações: FR-VS-047 editor→pipeline MCORCH [wrap `hyperframes render`, paridade provada 3 níveis + guard smoke + fix TDZ do dual-write de vídeo] + OTD-SEC-006/007 sentinel-wiring [generate-content+lead-score, injeção→403 LIVE] + FR-SEC-014 pt1 [ledger imutável `security_events`, /security-review NO FINDINGS, provado LIVE] + #2 YT/TikTok false-high corrigido; achado npm `hyperframes` license:None; 10 commits `8d59160`..`145f106`; +6 vs prev 8997 [inclui nó video-render `9069bb7d` + atividade Sovereign]; prev 8996)
> 9173	- **8996 total nodes** (verificado live 2026-06-30 via REST count=exact, avatar-fatia2-voice-fatia3a-consent-erase seal: +handoff `c138539f-0365-436a-ad56-c65e013793c6` embedded 768d + milestone Fatia 2 `b51d8de6-e574-42aa-93b7-8fd75d85a717` — Gabriel AI **Fatia 2 (Clone de Voz)** [nó voiceClone + edge `generate-voice` BYOK ElevenLabs/Cartesia fail-closed + code-switch guard FM-AC-013 + voice_profiles RLS-own Vault + RPCs tenant-guarded; migration `20260630120000`; smoke 10/10; browser+VisionQA PASS] + **Fatia 3a (Consent+Erasure LGPD Art.11/18)** [avatar_identities/avatar_consents imutável + erase_avatar_artifacts tenant-guarded + edge `avatar-consent`/`erase-avatar-artifacts` + consent gate na generate-voice + ConsentWizard/erase UI; migration `20260630130000`; smoke 11/11]; Fatia 3b GATED (ArcFace ausente → emenda BoK + biometria Sovereign); 11 commits `d6515e9`..`7913546`; `/security-review` NO FINDINGS ×2; prev 8993)
> 9174	- **8993 total nodes** (verificado live 2026-06-30 via REST count=exact, gabriel-ai-fatia1-spaces-p0-kanban-live seal: +handoff `aba1458e-2df1-4813-a71b-34360bf7417e` embedded 768d — Programa Gabriel AI [deepsearch força-total → BoK `avatar-clone-ai` 10/10 selada nó `ee81987d` GO-HYBRID + Fatia 1 BYOK hedra/cartesia/fal] + Spaces canvas Phase 0 (scaffold promovido) + Kanban painel-de-detalhe + reconciliador vivo não-destrutivo + cron */15; 6 commits `a5814d2`..`71f4c47`; prev 8992 = BoK seal `ee81987d` `documentation_suite` avatar-clone-ai DERIVES_FROM video-studio `c99b7875`)
> 9175	- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 9176	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 9177	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 9178	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 9179	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 9180	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 9181	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 9182	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 9183	- HNSW cosine index operational
> 9184	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 9185	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 9186	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 9187	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 9188	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 9189	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 9190	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 9191	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 9192	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 9193	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 9194	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 9195	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 9196	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 9197	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 9198	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 9199	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 9200	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 9201	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 9202	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 9203	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 9204	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 9205	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 9206	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 9207	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 9208	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 9209	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 9210	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 9211	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 9212	
> 9213	### Embedding Model
> 9214	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 9215	Schema: `vector(768)` — HNSW cosine index.
> 9216	
> 9217	### Embedding Pipeline (Autônomo — 2026-05-03)
> 9218	Três camadas eliminam intervenção manual:
> 9219	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 9220	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 9221	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 9222	
> ```

## 🤖 Claude *(18:09:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"^## |^### \" HANDOFF.md | sed -n '1,12p'; echo \"---fila/pending recentes---\"; sed -n '72,200p' HANDOFF.md | grep -nE \"Fila|Pending|Sovereign|GATE|gate OAuth|pendente|Higgsfield OAuth\" | head -20",
  "description": "Section headers + recent pending items"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3:## ⚡ FIRST ACTION FOR NEXT AGENT
> 12:## Task State
> 19:## Handoff Seal Record (2026-07-03) — Loop autônomo: anticorpo de assinatura owner-scoped (it.1) + BoK Higgsfield MCP (it.2)
> 41:## Handoff Seal Record (2026-07-03) — Fix Assets: exibição de mídia privada owner-scoped em TODO o ecossistema
> 65:### Arquitetura Fix Assets
> 81:## Handoff Seal Record (2026-07-03) — Spaces 2d: compose VIVO E2E (OTD-SPACES-003 FECHADA) + MCP oficial registrado
> 103:### Arquitetura compose 2d-bis
> 115:## Handoff Seal Record (2026-07-02) — 🏁 SELO FINAL /handoff: Sprint Spaces 1b→2d (6 iterações autônomas)
> 132:## Handoff Seal Record (2026-07-02) — Spaces Fase 2d: Designer/composer código-completo + ACHADO de drift do provider
> 140:## Handoff Seal Record (2026-07-02) — Spaces Fase 2c: voiceover stock E2E PAGO (canvas→áudio fechado)
> 148:## Handoff Seal Record (2026-07-02) — Spaces Fase 2b: References picker (consistência visual no nó de imagem)
> 156:## Handoff Seal Record (2026-07-02) — Spaces Fase 2a-CLIENTE: vídeo E2E PAGO — canvas→vídeo REAL fechado
> ---fila/pending recentes---
> 8:**Survival Laws Self-audit:** Lei 1 ✅ (toda claim ancorada — policies 3/1/0, HTTP SIGNED-200/BLOCKED, prints + meus olhos; o diagnóstico refutou a hipótese do Sovereign com o DB vivo) · Lei 2 ✅ (SOP ANTES do código) · Lei 3 ✅ (janela longe de 95% no início; podas por referência) · Lei 4 ✅ (ORO declarado; **portão de DDL de prod respeitado** — não contornei o classificador, esperei o `!` do Sovereign; `/security-review` pegou meu próprio HIGH e eu fechei antes do apply-final/commit).
> 12:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (loop autônomo) + review adversarial 3-lentes (morreu por créditos Fable → rodado inline em Opus) · Owner = Sovereign (custo E2E: 10 mco + ~US$0,04 BYOK OpenRouter).
> 39:Direção Sovereign OTD-SPACES-007: MCP oficial mcp.higgsfield.ai (Bearer BYOK=catálogo, conta=OAuth DCR)
> 42:**Survival Laws Self-audit:** Lei 1 ✅ (o achado do drift é o exemplo canônico — sonda material em vez de chute; toda claim ancorada em hash/UUID/HTTP/bytes/saldo exato) · Lei 2 ✅ (SOP Amendment 2d-bis ANTES do commit) · Lei 3 ✅ (janela ~31% no selo — folga ampla; podas por referência) · Lei 4 ✅ (ORO declarado; review adversarial inline após falha de créditos; nenhum portão Sovereign contornado — MCP OAuth/BoK segue na Fila).
> 46:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (/handoff explícito) + 2× /security-review independentes · Owner = Sovereign.
> 54:| **Segurança** | 2 reviews independentes (2a NO P0/HIGH · 2c APPROVED); todos os MEDIUM/LOW corrigidos pré-commit; OTD-SPACES-001/002/003 registradas na charter. |
> 57:| **Pendências herdáveis** | Fila Sovereign na charter (~~OTD-SPACES-003 compose-drift~~ ✅ FECHADA 2026-07-03 · OTD-SPACES-004/005/006 compose-premium/legado/refs-por-path · **OTD-SPACES-007 MCP oficial Higgsfield [BoK-gated]** · voz clonada [biometria] · app-registration YT/TikTok · Universe cutover · Smart-Delete witness). Backlog desbloqueado restante: Workflow Apps · FX · multi-page (Fase 2) · Fase 3 collab. |
> 59:**Survival Laws Self-audit (sessão):** Lei 1 ✅ (toda claim ancorada em hash/UUID/HTTP/bytes; achado 2d = exemplo canônico de parar no erro material) · Lei 2 ✅ (4 amendments ANTES do código) · Lei 3 ✅ (selo a ~90% da janela com folga; podas contínuas por referência) · Lei 4 ✅ (ORO declarado por fatia; 2 reviews independentes; nenhum portão Sovereign contornado — biometria/OAuth/decisões seguem na Fila).
> 63:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (net-zero: falha com estorno integral provado).
> 71:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = /security-review independente (APPROVED) + Sovereign · Owner = Sovereign (custo E2E: 2 mco + ~US$0,005 BYOK).
> 73:Iteração 5. SOP S26-S29 ANTES do código. Terceira modalidade do canvas pago: **texto→voz neural** com as 8 vozes stock do Gemini TTS (BYOK que o User 0 já tinha — voz CLONADA do Gabriel segue na Fila, biometria). Decisão-chave S26: reuso do `tts-speak` **com o JWT do próprio usuário** (o fn re-valida a sessão e resolve o BYOK dele; não cobra → zero hazard de double-charge, sem precisar do padrão prepaid). Review independente **APPROVED**: F1 LOW corrigido pré-commit (provider forjado no payload inflava a cobrança até 65 mco via resolver legado → preço **pinado** em `CREDIT_COSTS['voice-over']=2`; gate A4 prova com payload forjado) + F2/F4; F3/F5 pré-existentes viraram **OTD-SPACES-001/002** na charter (bucket público listável · INSERT id de spaces). Provas: smoke **27/27** · vitest **393** · tsc 0 · **E2E PAGO** space `1d77b500` (mantido): Estimar 2 exato → WAV **436.410 bytes** HTTP 200 (9s) → `<audio>` no cluster → saldo **4583→4581 (2 exato)** → Vision QA high. Commits `694d836`+`bfd2b29`.
> 75:**Survival Laws Self-audit:** Lei 1 ✅ · Lei 2 ✅ · Lei 3 ✅ · Lei 4 ✅ (ORO + review independente como co-Reviewer).
> 79:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (zero mudança no dinheiro — S25; superfície = client + bucket com policies existentes).
> 87:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (GO precedente de gasto de vídeo testemunhado 2026-07-01) · Owner = Sovereign (custo real do E2E: 40 mco + ~US$0,13 BYOK Higgsfield).
> 89:Iteração 3 do loop. Fecha o arco Spaces 2a: o Sovereign agora monta imagem→vídeo num Space e recebe um MP4 real, cobrado ledger-first com webhook finalizador.
> 105:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = /security-review independente + Sovereign · Owner = Sovereign (caminho de dinheiro async novo; blast radius mitigado por SOP S14-S18 + review NO P0/HIGH + smoke 22/22 zero-cost).
> 113:| **/security-review independente** | **NO P0/HIGH** — SOUND em mint/double-charge/cross-tenant/secret-leak/replay/SSRF(paridade legado). 1 MEDIUM (done-finalize sem retry/fallback → vídeo entregue podia virar sweep-refund + coins de volta) + 2 LOW (ordem BYOK-402 antes do 404 · `higgsfield_status` hardcoded no refactor) + 5 INFO — **MEDIUM+LOWs+INFO-1/5 corrigidos na sessão** (retry+done-fallback claim-guarded no webhook · BYOK pós-404 · status passthrough · redação de token em erro persistido · doc G12). |
> 121:**Survival Laws Self-audit:** Lei 1 ✅ (claims com HTTP/UUID/output literal) · Lei 2 ✅ (SOP amendment ANTES do código) · Lei 3 ✅ (poda contínua; scratch em /tmp) · Lei 4 ✅ (ORO declarado; review independente como co-Reviewer).
> 125:**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (Gabriel, GO explícito "Go migration spaces 1b") · Owner = Sovereign (ledger financeiro `generations` + RPCs de débito em produção).
> 127:Continuação direta do seal código-completo abaixo — o Sovereign deu o GO e a sequência pós-portão rodou inteira na mesma sessão:
> ```

## 🤖 Claude *(18:09:45)*


## 🤖 Claude *(18:09:46)*

I have enough context. Let me confirm BoK completeness for the active modules (spaces-evolution) and the Sovereign queue.

## 🤖 Claude *(18:09:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in spaces-evolution post-engine viral-autopilot; do\n  required=(00-[[deepsearch-blueprint|deepsearch-blueprint]] 01-mrd 02-brd 03-prd 04-frd 05-sdd)\n  missing=()\n  for doc in \"${required[@]}\"; do ls docs/bok/$slug/${doc}*.md >/dev/null 2>&1 || missing+=(\"$doc\"); done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 core BoK present\" || echo \"\u26a0\ufe0f $slug \u2014 missing core: ${missing[*]}\"\ndone\necho \"---spaces docs---\"; ls docs/bok/spaces-evolution/",
  "description": "BoK completeness for active modules"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ⚠️ spaces-evolution — missing core: 00-[[deepsearch-blueprint|deepsearch-blueprint]]
> ⚠️ post-engine — missing core: 00-[[deepsearch-blueprint|deepsearch-blueprint]]
> ⚠️ viral-autopilot — missing core: 00-[[deepsearch-blueprint|deepsearch-blueprint]]
> ---spaces docs---
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> 09-live-recon-spaces.md
> 10-ui-inventory-spaces.md
> 11-node-registry-spaces.md
> 12-node-anatomy-spaces.md
> 13-amendment-higgsfield-mcp-connector.md
> IMPLEMENTATION-PROMPT.md
> scaffold
> ```

## 🤖 Claude *(18:09:55)*


## 🤖 Claude *(18:10:20)*

All active BoK suites are complete (standard 9-doc set present; my probe used the wrong filename — `00-index` exists). I now have full context.

═══════════════════════════════════════════════════════════
  HANDSON — Loop autônomo it.1+it.2 (SELADO 2026-07-03)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **Loop it.1 (anticorpo de assinatura owner-scoped) + it.2 (BoK amendment Higgsfield MCP OAuth)** — o backlog *desbloqueado* esgotou; todo o resto é Sovereign-gated.
  Últimos commits:
    `c38519a` — docs(handoff): seal loop it.1+it.2 (mesh 9048)
    `19d20b5` — docs(readme): v6.83.2
    `81e6492` — chore(loop): registra it.2 — BoK Higgsfield MCP + gate OAuth na Fila
    `34bdb64` — docs(bok): amendment Higgsfield MCP connector (fecha gate Closed-Loop 3.5)
    `c000086` — chore(loop): registra it.1 — anticorpo owner-signing shipped

📂 **MUDANÇAS PENDENTES**
  `M .agents/workflows/handson.md` — +10 linhas (não commitado; é este próprio protocolo de pickup, não conflita com nada). Descrever, não commitar.

🏗️ **INFRA** — tudo saudável ✅
  mcorch_chroma:     Up 2 weeks (healthy) — Chroma API v2: **OK** (heartbeat vivo)
  mcorch_claude_mem: Up 2 weeks (healthy)
  mcorch_vision_mcp: Up 4 days (healthy) — olho de QA online
  mega-brain-daemon/webhook/dashboard: Up 2 weeks

🧠 **KNOWLEDGE MESH**
  **9047 nós** · ~9070 arestas (fonte: GraphRAG State, verificado live 2026-07-03) — 100% embedded (768d HNSW cosine)
  Seal Fix Assets: handoff `6e2b32b2` embedded

🔧 **TYPESCRIPT** — Zero erros ✅ (`tsc --noEmit` limpo)

📚 **BoK SUITES** (v3 — MCORCH Master Execution Protocol)
  Sealed: 25 suítes, todas com o conjunto 9-doc completo. `spaces-evolution` (ativa) = 00-index→08 + amendments 09-13 (**13 = Higgsfield MCP OAuth**, selado esta última sessão).
  Incomplete: nenhum ✅
  Gate: **liberado** — nenhum código novo pendente sem BoK.

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional (LinkedIn auto ✅ · Twitter/IG gated por tier/App Review).
  Último entregue: Fix Assets — mídia privada owner-scoped em 13 superfícies (`/security-review` CLOSED 9/10; 90 assets do User 0 vivos).

⚡ **PRÓXIMOS PASSOS** — o frontier autônomo está **vazio**; tudo pendente é **Fila de Ação Sovereign** (Lei 4):
  1. **Higgsfield MCP OAuth E2E** (OTD-SPACES-007) — código da Fatia desbloqueado, mas gated na aprovação do amendment + consent Clerk + `redirect_uri` canônica + GO de gasto.
  2. **OTD-SPACES-004/005/006** — compose-premium · legado · refs-por-path (backlog desbloqueado: Workflow Apps · FX · multi-page Fase 2 · collab Fase 3).
  3. **Débitos gated herdados** — voz clonada (biometria) · app-registration YT/TikTok · Universe cutover · Smart-Delete witness · Stripe live keys.

⚠️ **ALERTAS**
  Nenhum bloqueador ✅ — TS limpo, infra healthy, scratch/ vazio, sem BoK faltando. Única mudança no worktree é o próprio `handson.md` (benigno). **Não há trabalho autônomo destravado** — a sessão anterior selou justamente por isso; qualquer avanço material precisa de um GO/direção do Sovereign.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

O ecossistema está estável e selado. Como o backlog desbloqueado esgotou na última sessão, **preciso da sua direção**, Maestro: deseja destravar algum item da Fila Sovereign (o mais maduro é o **Higgsfield MCP OAuth E2E**), puxar um item novo, ou há uma diretiva fresca?

## 👤 User *(19:22:34)*

Então não adianta mais rodar o "/loop Você é o MCORCH Master Execution Agent em MALHA FECHADA AUTÔNOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado — BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review se houver migration → commit granular (Workflow p/ tarefas substantivas); (3) ao bater em portão Sovereign (biometria/DNS/OAuth/GO/decisão), NÃO improvise — registre na Fila de Ação Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada iteração." ?  Tivemos aprovação da google sobre a api mas fica poucas horas e logo aparece para reconectar https://login.mcorch.com/dashboard/social fica como token expirado, isso é normal? Os usuários vão ter que ficar fazendo isso de hora em hora?

## 🤖 Claude *(19:22:55)*


## 🤖 Claude *(19:23:01)*

Boa pergunta — e ela tem resposta técnica concreta, não é "normal" no sentido de aceitável. Deixa eu investigar o código real do fluxo OAuth antes de afirmar qualquer coisa (Lei 1).

Primeiro, a resposta curta enquanto olho o código: **access tokens do Google expiram em ~1h por design — isso é esperado. O que NÃO é normal é o usuário ter que reconectar.** O certo é o sistema usar o `refresh_token` para renovar silenciosamente. Se está pedindo reconexão, quase sempre é um destes três: (a) o fluxo não pediu `access_type=offline` + `prompt=consent` → o Google nunca devolveu `refresh_token`; (b) o `refresh_token` não está sendo salvo/usado; ou (c) o app ainda está em "Testing" no Google (refresh expira em 7 dias). Vou confirmar qual é o seu caso.

## 🤖 Claude *(19:23:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== pages/components referencing dashboard/social ===\"; grep -rlE \"dashboard/social|SocialPage|social_credentials|social_accounts\" src/ 2>/dev/null | head -30\necho \"=== edge functions social/oauth ===\"; ls supabase/functions/ | grep -iE \"social|oauth|youtube|google|connect|refresh|linkedin|twitter\" ",
  "description": "Locate social OAuth surfaces"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === pages/components referencing dashboard/social ===
> src/integrations/supabase/types.ts
> src/pages/SocialCallback.tsx
> src/components/dashboard/OnboardingWizard.tsx
> src/hooks/useDashboardData.ts
> src/components/creative/AssetDetailDialog.tsx
> src/components/dashboard/DashboardSidebar.tsx
> src/hooks/useSocialAccounts.ts
> === edge functions social/oauth ===
> publish-social
> refresh-social-token
> social-auth-callback
> social-auth-init
> ```

## 🤖 Claude *(19:23:09)*


## 🤖 Claude *(19:23:10)*

Há um `refresh-social-token`. Vou ler o fluxo completo: init (pede offline access?), callback (salva refresh_token?), refresh (é chamado automaticamente?) e a página que mostra "expirado".

## 🤖 Claude *(19:23:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== social-auth-init (scopes / access_type / prompt) ===\"; grep -nEi \"access_type|prompt|offline|scope|google|youtube|authorization_url|accounts.google\" supabase/functions/social-auth-init/index.ts | head -40\necho; echo \"=== social-auth-callback (refresh_token storage) ===\"; grep -nEi \"refresh_token|expires|access_token|upsert|insert|expires_at|expires_in\" supabase/functions/social-auth-callback/index.ts | head -40",
  "description": "Inspect init scopes and callback token storage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === social-auth-init (scopes / access_type / prompt) ===
> 19:const YOUTUBE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";
> 76:      const scopes = "openid profile email w_member_social";
> 77:      authUrl = `${LINKEDIN_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}`;
> 87:      const scopes = "instagram_business_basic,instagram_business_content_publish,instagram_business_manage_comments,instagram_business_manage_messages";
> 88:      authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${appId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&response_type=code`;
> 100:      const scopes = "tweet.read tweet.write users.read offline.access";
> 101:      authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;
> 118:      // Scope MUST be COMMA-separated — a space silently fails the consent (doc 10 §TikTok).
> 120:      const scopes = "video.publish,user.info.basic";
> 121:      authUrl = `${TIKTOK_AUTH_URL}?client_key=${encodeURIComponent(creds.clientId)}&response_type=code&redirect_uri=${encodeURIComponent(callbackUrl)}&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}`;
> 123:    } else if (platform === "youtube") {
> 131:        creds = await resolveSocialAppCreds(serviceClient, userId, "youtube");
> 137:      // access_type=offline + prompt=consent are CRITICAL: without prompt=consent a re-auth
> 138:      // returns a NULL refresh_token silently (doc 10 §YouTube).
> 139:      const scopes = "https://www.googleapis.com/auth/youtube.upload";
> 140:      authUrl = `${YOUTUBE_AUTH_URL}?client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&response_type=code&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}&access_type=offline&prompt=consent`;
> 156:      // Plan the FULL scope set up-front — adding a scope later forces a full re-authorization
> 158:      const scopes = "boards:read,boards:write,pins:read,pins:write,user_accounts:read";
> 159:      authUrl = `${PINTEREST_AUTH_URL}?client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&response_type=code&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}`;
> 
> === social-auth-callback (refresh_token storage) ===
> 69:    let expiresIn: number | null = null;
> 74:    // Pinterest refresh_token_expires_at). Empty for platforms that don't need it.
> 95:      accessToken = tokenData.access_token;
> 96:      refreshToken = tokenData.refresh_token || null;
> 97:      expiresIn = tokenData.expires_in;
> 112:      const tokenRes = await fetch("https://api.instagram.com/oauth/access_token", {
> 126:      const shortToken = tokenData.access_token;
> 131:        `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=${appSecret}&access_token=${shortToken}`
> 134:      accessToken = longData.access_token || shortToken;
> 135:      expiresIn = longData.expires_in || null;
> 139:      const meRes = await fetch(`https://graph.instagram.com/v21.0/me?fields=username,name&access_token=${accessToken}`);
> 166:      accessToken = tokenData.access_token;
> 167:      refreshToken = tokenData.refresh_token || null;
> 168:      expiresIn = tokenData.expires_in;
> 200:      accessToken = tokenData.access_token;
> 201:      refreshToken = tokenData.refresh_token || null;
> 202:      expiresIn = tokenData.expires_in ?? 86400; // 24h
> 227:      accessToken = tokenData.access_token;
> 228:      // CRITICAL: Google returns refresh_token ONLY on first auth (access_type=offline + prompt=consent).
> 229:      // If absent, leave it null — the upsert/refresh path must never overwrite a good token with empty.
> 230:      refreshToken = tokenData.refresh_token || null;
> 231:      expiresIn = tokenData.expires_in ?? 3600; // ~1h
> 267:      accessToken = tokenData.access_token;
> 268:      refreshToken = tokenData.refresh_token || null; // rotating
> 269:      expiresIn = tokenData.expires_in ?? 2592000; // 30d
> 272:      if (tokenData.refresh_token_expires_at) {
> 273:        metadata = { ...metadata, refresh_token_expires_at: tokenData.refresh_token_expires_at };
> 288:    const expiresAt = expiresIn
> 289:      ? new Date(Date.now() + expiresIn * 1000).toISOString()
> 292:    // Upsert social account
> 295:      .upsert(
> 299:          access_token: accessToken,
> 300:          refresh_token: refreshToken,
> 301:          token_expires_at: expiresAt,
> 312:      console.error("DB upsert error:", dbError);
> 313:      await supabase.from("social_accounts").insert({
> 316:        access_token: accessToken,
> 317:        refresh_token: refreshToken,
> 318:        token_expires_at: expiresAt,
> 329:      .insert({ service: `social-auth-${platform}`, status: dbError ? "degraded" : "healthy" })
> ```

## 🤖 Claude *(19:23:20)*


## 🤖 Claude *(19:23:22)*

O fluxo de init/callback do YouTube está **correto** (`access_type=offline&prompt=consent` → refresh_token salvo). Então o refresh_token existe. A questão é: **algo está usando esse refresh_token?** Vou ver o `refresh-social-token`, quem o chama, e como a UI decide "expirado".

## 🤖 Claude *(19:23:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== refresh-social-token: platforms handled + trigger ===\"; grep -nEi \"youtube|google|refresh_token|grant_type|platform|oauth2.googleapis|token_expires_at|cron|expires\" supabase/functions/refresh-social-token/index.ts | head -40\necho; echo \"=== who INVOKES refresh-social-token? ===\"; grep -rnE \"refresh-social-token\" src/ supabase/functions/ scripts/ 2>/dev/null\necho; echo \"=== does publish-social refresh before publishing? ===\"; grep -nEi \"refresh|expires_at|expired|token_expires\" supabase/functions/publish-social/index.ts | head -20",
  "description": "Refresh fn coverage + invocation points"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === refresh-social-token: platforms handled + trigger ===
> 77:    let newExpiresAt: string | null = null;
> 79:    if (account.platform === "linkedin") {
> 80:      if (!account.refresh_token) {
> 90:          grant_type: "refresh_token",
> 91:          refresh_token: account.refresh_token,
> 99:      newExpiresAt = new Date(Date.now() + data.expires_in * 1000).toISOString();
> 100:    } else if (account.platform === "instagram" || account.platform === "facebook") {
> 102:        `https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${Deno.env.get("INSTAGRAM_APP_ID")}&client_secret=${Deno.env.get("INSTAGRAM_APP_SECRET")}&fb_exchange_token=${account.access_token}`
> 107:      newExpiresAt = data.expires_in
> 108:        ? new Date(Date.now() + data.expires_in * 1000).toISOString()
> 110:    } else if (account.platform === "twitter") {
> 111:      if (!account.refresh_token) {
> 126:          grant_type: "refresh_token",
> 127:          refresh_token: account.refresh_token,
> 133:      newExpiresAt = data.expires_in
> 134:        ? new Date(Date.now() + data.expires_in * 1000).toISOString()
> 137:      if (data.refresh_token) {
> 140:          .update({ refresh_token: data.refresh_token })
> 143:    } else if (account.platform === "tiktok") {
> 144:      if (!account.refresh_token) {
> 158:          grant_type: "refresh_token",
> 159:          refresh_token: account.refresh_token,
> 167:      newExpiresAt = new Date(Date.now() + (data.expires_in ?? 86400) * 1000).toISOString();
> 169:      // ROTATION: TikTok issues a NEW refresh_token on every refresh — re-store it (never keep the old one),
> 171:      if (data.refresh_token) {
> 174:          .update({ refresh_token: data.refresh_token })
> 178:    } else if (account.platform === "youtube") {
> 179:      if (!account.refresh_token) {
> 186:      const creds = await resolveSocialAppCreds(admin, account.user_id, "youtube");
> 187:      const res = await fetch("https://oauth2.googleapis.com/token", {
> 193:          grant_type: "refresh_token",
> 194:          refresh_token: account.refresh_token,
> 199:        throw new Error(data.error_description || data.error || "YouTube refresh failed");
> 202:      newExpiresAt = new Date(Date.now() + (data.expires_in ?? 3600) * 1000).toISOString();
> 204:      // Google usually keeps the same refresh_token, but tolerate a rotated one on re-consent.
> 205:      // CRITICAL: only re-store when present — NEVER null an existing good refresh_token.
> 206:      if (data.refresh_token) {
> 209:          .update({ refresh_token: data.refresh_token })
> 212:      pulse("social-auth-youtube", "healthy");
> 213:    } else if (account.platform === "pinterest") {
> 
> === who INVOKES refresh-social-token? ===
> supabase/functions/refresh-social-token/index.ts:277:    console.error("refresh-social-token error:", err);
> supabase/functions/refresh-social-token/index.ts:286:        .insert({ service: "refresh-social-token", status: "degraded" })
> supabase/functions/agent-task-execute/index.ts:35:  "social-auth-callback", "social-auth-init", "refresh-social-token", "agent-task-execute",
> supabase/functions/self-heal/index.ts:80:          const refreshRes = await fetch(`${supabaseUrl}/functions/v1/refresh-social-token`, {
> supabase/functions/self-heal/index.ts:129:          const refreshRes = await fetch(`${supabaseUrl}/functions/v1/refresh-social-token`, {
> supabase/functions/publish-social/index.ts:86:      const refreshRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/refresh-social-token`, {
> supabase/functions/publish-social/index.ts:100:      // refresh-social-token updates the DB but does not return the token;
> scripts/seed-social-oauth-adrs.ts:40:Edge functions involved: social-auth-init, social-auth-callback (--no-verify-jwt), publish-social, refresh-social-token.`,
> scripts/seed-social-oauth-adrs.ts:97:2. refresh-social-token compared token string against raw key → always false → never refreshed
> scripts/seed-social-oauth-adrs.ts:100:Fix for bug 3: after calling refresh-social-token, re-fetch social_accounts from DB to get the updated token before publishing.
> scripts/seed-social-oauth-adrs.ts:106:      affects: ["auto-publish", "publish-social", "refresh-social-token"],
> 
> === does publish-social refresh before publishing? ===
> 84:    // Refresh token if expired, then re-fetch account to get the new access_token
> 85:    if (account.token_expires_at && new Date(account.token_expires_at) < new Date()) {
> 86:      const refreshRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/refresh-social-token`, {
> 94:      if (!refreshRes.ok) {
> 95:        return new Response(JSON.stringify({ error: "Token expired and refresh failed" }), {
> 100:      // refresh-social-token updates the DB but does not return the token;
> 102:      const { data: refreshedAccount } = await adminClient
> 104:        .select("access_token, refresh_token, token_expires_at")
> 107:      if (refreshedAccount) {
> 108:        account.access_token = refreshedAccount.access_token;
> 109:        account.token_expires_at = refreshedAccount.token_expires_at;
> ```

## 🤖 Claude *(19:23:40)*


## 🤖 Claude *(19:23:42)*

Backend está robusto: `publish-social` e `self-heal` **já renovam o token automaticamente** via refresh_token antes de publicar. Então a publicação não quebra. Falta confirmar minha hipótese: a UI marca "expirado" só olhando `token_expires_at` (a janela de ~1h do access token), ignorando que existe refresh_token. Vou ler a página e o hook.

## 🤖 Claude *(19:23:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== find the /dashboard/social page ===\"; grep -rlnE \"reconnect|reconect|Reconectar|expirad|Expired|token_expires_at|isExpired|Reconnect\" src/pages src/components 2>/dev/null | head\necho; echo \"=== useSocialAccounts expiry logic ===\"; grep -nEi \"expires|expired|reconect|reconnect|now\\(\\)|Date\" src/hooks/useSocialAccounts.ts",
  "description": "Find UI expiry/reconnect logic"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === find the /dashboard/social page ===
> src/pages/ResetPassword.tsx
> src/pages/SocialAccountsPage.tsx
> src/pages/DashboardHome.tsx
> src/components/landing/FeaturesSection.tsx
> src/components/canvas/RightPanel/inspectors/CharacterReferenceInspector.tsx
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx
> src/components/settings/MetaConfigCard.tsx
> 
> === useSocialAccounts expiry logic ===
> 31:        .select('id, user_id, platform, platform_user_id, platform_username, is_active, token_expires_at, scopes, metadata, created_at, updated_at')
> 47:    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['social_accounts'] }),
> 90:  const isTokenExpired = (account: SocialAccount) => {
> 91:    if (!account.token_expires_at) return false;
> 92:    return new Date(account.token_expires_at) < new Date();
> 101:    isTokenExpired,
> ```

## 🤖 Claude *(19:23:53)*


## 🤖 Claude *(19:23:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nEi \"isTokenExpired|Reconectar|reconnect|Expirad|token_expires|expira\" src/pages/SocialAccountsPage.tsx | head -20",
  "description": "Confirm page reconnect badge logic"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 34:  const { accounts, isLoading, disconnectAccount, initiateOAuth, isTokenExpired } = useSocialAccounts();
> 148:              const expired = isTokenExpired(account);
> 166:                            <AlertTriangle className="h-3 w-3 mr-1" /> Token expirado
> 184:                        Reconectar
> ```

## 🤖 Claude *(19:24:30)*


## 🤖 Claude *(19:24:51)*

Confirmado com prova material. Aqui está o diagnóstico, Maestro.

## Resposta direta: **não, o usuário NÃO vai precisar reconectar de hora em hora.** É um alarme visual falso.

O que está acontecendo tem duas camadas — uma é normal, a outra é um bug cosmético:

**1. O access token expirar em ~1h é normal e esperado (padrão do Google).**
`social-auth-callback/index.ts:231` grava `expires_in ?? 3600` (1h) para o YouTube. Todo access token do Google vive ~1h — isso é por design, não é defeito.

**2. O sistema JÁ renova sozinho — o refresh_token está guardado e é usado.** Verifiquei os 3 pontos que importam:
- **Init correto** (`social-auth-init/index.ts:139-140`): a URL do YouTube tem `access_type=offline&prompt=consent` — exatamente o que faz o Google devolver o `refresh_token` (de longa duração). O comentário no código inclusive documenta essa armadilha.
- **Callback salva** (`social-auth-callback/index.ts:230`): o `refresh_token` é persistido, com guarda para nunca sobrescrever um bom token com vazio.
- **Renovação automática**: `publish-social/index.ts:85-109` **renova o token antes de publicar** se estiver expirado, e o `self-heal` também chama o `refresh-social-token` (que trata YouTube corretamente em `refresh-social-token/index.ts:178-212`). Ou seja: **na hora de publicar, o token é renovado silenciosamente. A publicação nunca quebra por isso.**

**3. Então por que a tela grita "Token expirado / Reconectar"?** É um bug de exibição. Achei a causa exata:

```
src/hooks/useSocialAccounts.ts:90-92
  const isTokenExpired = (account) => {
    if (!account.token_expires_at) return false;
    return new Date(account.token_expires_at) < new Date();   // ← só olha o access token de 1h
  };
```

Esse `isTokenExpired` decide o badge "Token expirado" e o botão "Reconectar" (`SocialAccountsPage.tsx:148,166,184`). Ele marca vermelho baseado **só no access token de 1h** — e nem sequer considera que existe um `refresh_token` de longa duração (o hook nem seleciona o refresh_token, por segurança). Resultado: **toda hora o cartão fica vermelho pedindo reconexão, mesmo com a conexão 100% saudável.** Assusta o usuário à toa.

## O único caso em que reconectar SERIA real (vale confirmar)
Se o app OAuth ainda estiver em **"Testing"** no Google Cloud Console (e não **"In production"**), o Google expira o `refresh_token` em **7 dias**. Você disse que teve aprovação da Google — então confirme no Console que o status de publicação é **"In production"** (aprovado o *scope* ≠ app publicado). Se estiver "In production", o refresh_token é praticamente permanente. De qualquer forma, isso causaria reconexão a cada 7 dias, **não** de hora em hora — o sintoma "poucas horas" é 100% o badge cosmético acima.

## Sobre o /loop
Não é que "não adianta mais rodar" — o frontier autônomo estava vazio de itens *desbloqueados*, mas **este bug é exatamente um item novo, desbloqueado e de alto valor** (UX que assusta todo usuário conectado). A correção é pequena: fazer o badge refletir "precisa reautenticar" de verdade (presença/validade do refresh_token) em vez do access token de 1h — mostrar "Conectado" com uma nota discreta "renovado automaticamente", mantendo o botão Reconectar disponível mas sem o alarme vermelho.

Quer que eu corrija agora? Posso rodar em malha fechada: patch no hook + página, expondo um booleano seguro `needs_reauth` a partir do refresh_token, com prova material E2E no browser (Lei 1) antes de dizer "pronto". É baixo risco e single-scope (isento do BoK Gate).

## 👤 User *(20:08:00)*

Tudo ok com a google Status da verificação
 Sua marca foi verificada e está aparecendo para os usuários. e 1 usuário / limite de 100 usuários
Status de publicação
Em produção; Corrija então o problema pois eu ja desconectei e reconectei manualmente e ainda continua com o alerta de token. Feito isso precisamos verificar o tiktok que respondeu com negativa... coisa boba pelo que entendi veja.: Changes to your app were not approved for production. See why

Update the following fields and resubmit changes to your app:

App icon
Terms of Service
Privacy Policy
Website URL
Note from reviewer: The demo video should show the complete end-to-end flow of the integrations with TikTok(Please demonstrate with sandbox or provide a mockup demo).,Demo video images pixelated, kindly use high quality image. ,All selected products and scopes must be clearly demonstrated in the video. If you don't need certain products or scopes, make sure to remove them before review. You are required to use sandbox to demonstrate the integration.,Demo video does not provide enough clarity and context as to show the website functions.,The icon used is not the same as the icon being displayed in TOS and Privacy links.,The app icon submitted in the Basic Info does not match the icon displayed on the website. Please ensure the same icon is used consistently across both the TikTok, the website and Browser tab (favicon), then resubmit for review,Your externally facing website must be fully developed and cannot be a landing or login page. If it is a login page, you must provide a test account and password in the Apply Reason field.,Valid Privacy Policy and Terms of Service links must be clearly visible on the website URL without needing to open a menu or log in, and both links must be active.
If you have any questions, contact us here. já estou pedindo pro Claude Design fazer o handoff para claude code assim podemos fazer o grande rebranding de uma vez por todas, e depois vamos mudando em produção mesmo asssim como ja fazemos com o desenvolvimento. Acredito que essa vai ser uma tarefa dificil mas o quanto antes fazer isso melhor, pois da muito trabalho fazer rebrand e redesign.

## 🤖 Claude *(20:08:55)*


## 🤖 Claude *(20:09:00)*

Perfeito — app **"Em produção"** confirma que o `refresh_token` é de longa duração. Então o alerta é 100% o bug cosmético do badge (você reconectou, ficou verde ~1h, e voltou a vermelho). Vou corrigir agora com prova material.

Sobre o TikTok: é rejeição de **branding/consistência** (ícone que bate com favicon+TOS+Privacy, vídeo demo em sandbox HD, site com links de Privacy/TOS visíveis sem login). Isso pertence ao **grande rebranding** que o Claude Design vai te entregar via handoff — vou registrar os requisitos exatos na Fila Sovereign para não perdermos nenhum item, mas **não** começo o rebrand agora (espero o handoff). Foco imediato: o bug do token.

Deixa eu ler os arquivos que vou tocar.

## 🤖 Claude *(20:09:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { toast } from 'sonner';
> 5	import { edgeErrorMessage } from '@/lib/edge';
> 6	import type { Tables } from '@/integrations/supabase/types';
> 7	import type { Database } from '@/integrations/supabase/types';
> 8	
> 9	type SocialAccount = Tables<'social_accounts'>;
> 10	type SocialPlatform = Database['public']['Enums']['social_platform'];
> 11	
> 12	export const SUPPORTED_PLATFORMS: { id: SocialPlatform; name: string; icon: string; color: string }[] = [
> 13	  { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: 'bg-blue-600' },
> 14	  { id: 'instagram', name: 'Instagram', icon: '📸', color: 'bg-gradient-to-r from-purple-500 to-pink-500' },
> 15	  { id: 'facebook', name: 'Facebook', icon: '👤', color: 'bg-blue-500' },
> 16	  { id: 'twitter', name: 'Twitter / X', icon: '𝕏', color: 'bg-zinc-800' },
> 17	  { id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'bg-zinc-900' },
> 18	  { id: 'youtube', name: 'YouTube', icon: '▶️', color: 'bg-red-600' },
> 19	  { id: 'pinterest', name: 'Pinterest', icon: '📌', color: 'bg-red-500' },
> 20	];
> 21	
> 22	export function useSocialAccounts() {
> 23	  const { user } = useAuth();
> 24	  const queryClient = useQueryClient();
> 25	
> 26	  const accountsQuery = useQuery({
> 27	    queryKey: ['social_accounts', user?.id],
> 28	    queryFn: async () => {
> 29	      const { data, error } = await supabase
> 30	        .from('social_accounts')
> 31	        .select('id, user_id, platform, platform_user_id, platform_username, is_active, token_expires_at, scopes, metadata, created_at, updated_at')
> 32	        .order('created_at', { ascending: false });
> 33	      if (error) throw error;
> 34	      return data as SocialAccount[];
> 35	    },
> 36	    enabled: !!user,
> 37	  });
> 38	
> 39	  const disconnectAccount = useMutation({
> 40	    mutationFn: async (id: string) => {
> 41	      // Privileged disconnect: disconnect_social() (SECURITY DEFINER, scoped to auth.uid()) deletes
> 42	      // the row AND revokes the orphaned Vault secrets (access_token + refresh_token). A plain
> 43	      // DELETE through the masked view would delete only the base row and leak the plaintext token.
> 44	      const { error } = await supabase.rpc('disconnect_social', { p_account_id: id });
> 45	      if (error) throw error;
> 46	    },
> 47	    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['social_accounts'] }),
> 48	  });
> 49	
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
> 90	  const isTokenExpired = (account: SocialAccount) => {
> 91	    if (!account.token_expires_at) return false;
> 92	    return new Date(account.token_expires_at) < new Date();
> 93	  };
> 94	
> 95	  return {
> 96	    accounts: accountsQuery.data ?? [],
> 97	    isLoading: accountsQuery.isLoading,
> 98	    error: accountsQuery.error,
> 99	    disconnectAccount,
> 100	    initiateOAuth,
> 101	    isTokenExpired,
> 102	  };
> 103	}
> 104	
> ```

## 🤖 Claude *(20:09:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	import {
> 3	  resolveSocialAppCreds,
> 4	  SocialAppConfigError,
> 5	  socialAppConfigErrorResponse,
> 6	} from "../_shared/social-app-config.ts";
> 7	
> 8	const corsHeaders = {
> 9	  "Access-Control-Allow-Origin": "*",
> 10	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 11	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token",
> 12	};
> 13	
> 14	Deno.serve(async (req) => {
> 15	  if (req.method === "OPTIONS") {
> 16	    return new Response("ok", { headers: corsHeaders });
> 17	  }
> 18	
> 19	  try {
> 20	    const authHeader = req.headers.get("Authorization");
> 21	    if (!authHeader?.startsWith("Bearer ")) {
> 22	      return new Response(JSON.stringify({ error: "Missing authorization" }), {
> 23	        status: 401,
> 24	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 25	      });
> 26	    }
> 27	
> 28	    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
> 29	    const supabaseAnonKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 30	    const serviceRoleKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 31	    const admin = createClient(supabaseUrl, serviceRoleKey);
> 32	
> 33	    // Best-effort telemetry — mirrors publish-meta's `pulse`. Materiality (Lei 1): a 2xx is not success;
> 34	    // every refresh path (healthy/degraded) emits to infra_health_logs so the Neural HUD sees the token cycle.
> 35	    const pulse = (service: string, status: "healthy" | "degraded") =>
> 36	      admin.from("infra_health_logs").insert({ service, status }).then(() => {}, () => {});
> 37	
> 38	    // Resolve caller: user JWT → user.id available; service role JWT → user is null (internal call)
> 39	    // Supabase infrastructure already validated the JWT signature before reaching this code.
> 40	    const userClient = createClient(supabaseUrl, supabaseAnonKey, {
> 41	      global: { headers: { Authorization: authHeader } },
> 42	    });
> 43	    const { data: { user } } = await userClient.auth.getUser();
> 44	    const isServiceRole = authHeader === `Bearer ${serviceRoleKey}`;
> 45	    const isInternalServiceCall = isServiceRole;
> 46	
> 47	    const { social_account_id } = await req.json();
> 48	    if (typeof social_account_id !== "string" || !social_account_id.trim()) {
> 49	      return new Response(JSON.stringify({ error: "social_account_id required" }), {
> 50	        status: 400,
> 51	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 52	      });
> 53	    }
> 54	
> 55	    const { data: account, error } = await admin
> 56	      .from("decrypted_social_accounts")
> 57	      .select("*")
> 58	      .eq("id", social_account_id)
> 59	      .single();
> 60	
> 61	    if (error || !account) {
> 62	      return new Response(JSON.stringify({ error: "Account not found" }), {
> 63	        status: 404,
> 64	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 65	      });
> 66	    }
> 67	
> 68	    // Ownership check
> 69	    if (!isInternalServiceCall && (!user || account.user_id !== user.id)) {
> 70	      return new Response(JSON.stringify({ error: "Forbidden" }), {
> 71	        status: 403,
> 72	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 73	      });
> 74	    }
> 75	
> 76	    let newAccessToken: string;
> 77	    let newExpiresAt: string | null = null;
> 78	
> 79	    if (account.platform === "linkedin") {
> 80	      if (!account.refresh_token) {
> 81	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 82	          status: 400,
> 83	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 84	        });
> 85	      }
> 86	      const res = await fetch("https://www.linkedin.com/oauth/v2/accessToken", {
> 87	        method: "POST",
> 88	        headers: { "Content-Type": "application/x-www-form-urlencoded" },
> 89	        body: new URLSearchParams({
> 90	          grant_type: "refresh_token",
> 91	          refresh_token: account.refresh_token,
> 92	          client_id: Deno.env.get("LINKEDIN_CLIENT_ID")!,
> 93	          client_secret: Deno.env.get("LINKEDIN_CLIENT_SECRET")!,
> 94	        }),
> 95	      });
> 96	      const data = await res.json();
> 97	      if (!res.ok) throw new Error(data.error_description || "LinkedIn refresh failed");
> 98	      newAccessToken = data.access_token;
> 99	      newExpiresAt = new Date(Date.now() + data.expires_in * 1000).toISOString();
> 100	    } else if (account.platform === "instagram" || account.platform === "facebook") {
> 101	      const res = await fetch(
> 102	        `https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${Deno.env.get("INSTAGRAM_APP_ID")}&client_secret=${Deno.env.get("INSTAGRAM_APP_SECRET")}&fb_exchange_token=${account.access_token}`
> 103	      );
> 104	      const data = await res.json();
> 105	      if (!res.ok) throw new Error(data.error?.message || "Facebook refresh failed");
> 106	      newAccessToken = data.access_token;
> 107	      newExpiresAt = data.expires_in
> 108	        ? new Date(Date.now() + data.expires_in * 1000).toISOString()
> 109	        : null;
> 110	    } else if (account.platform === "twitter") {
> 111	      if (!account.refresh_token) {
> 112	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 113	          status: 400,
> 114	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 115	        });
> 116	      }
> 117	      const clientId = Deno.env.get("TWITTER_CLIENT_ID")!;
> 118	      const clientSecret = Deno.env.get("TWITTER_CLIENT_SECRET")!;
> 119	      const res = await fetch("https://api.x.com/2/oauth2/token", {
> 120	        method: "POST",
> 121	        headers: {
> 122	          "Content-Type": "application/x-www-form-urlencoded",
> 123	          Authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,
> 124	        },
> 125	        body: new URLSearchParams({
> 126	          grant_type: "refresh_token",
> 127	          refresh_token: account.refresh_token,
> 128	        }),
> 129	      });
> 130	      const data = await res.json();
> 131	      if (!res.ok) throw new Error(data.error_description || "Twitter refresh failed");
> 132	      newAccessToken = data.access_token;
> 133	      newExpiresAt = data.expires_in
> 134	        ? new Date(Date.now() + data.expires_in * 1000).toISOString()
> 135	        : null;
> 136	
> 137	      if (data.refresh_token) {
> 138	        await admin
> 139	          .from("social_accounts")
> 140	          .update({ refresh_token: data.refresh_token })
> 141	          .eq("id", social_account_id);
> 142	      }
> 143	    } else if (account.platform === "tiktok") {
> 144	      if (!account.refresh_token) {
> 145	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 146	          status: 400,
> 147	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 148	        });
> 149	      }
> 150	      // App credentials resolve per-user → env fallback → hard-fail (FR-PE-005/010).
> 151	      const creds = await resolveSocialAppCreds(admin, account.user_id, "tiktok");
> 152	      const res = await fetch("https://open.tiktokapis.com/v2/oauth/token/", {
> 153	        method: "POST",
> 154	        headers: { "Content-Type": "application/x-www-form-urlencoded" },
> 155	        body: new URLSearchParams({
> 156	          client_key: creds.clientId,
> 157	          client_secret: creds.clientSecret,
> 158	          grant_type: "refresh_token",
> 159	          refresh_token: account.refresh_token,
> 160	        }),
> 161	      });
> 162	      const data = await res.json();
> 163	      if (!res.ok || data.error) {
> 164	        throw new Error(data.error_description || data.error || "TikTok refresh failed");
> 165	      }
> 166	      newAccessToken = data.access_token;
> 167	      newExpiresAt = new Date(Date.now() + (data.expires_in ?? 86400) * 1000).toISOString();
> 168	
> 169	      // ROTATION: TikTok issues a NEW refresh_token on every refresh — re-store it (never keep the old one),
> 170	      // otherwise the chain silently breaks and forces re-OAuth. Persist before the shared access-token update.
> 171	      if (data.refresh_token) {
> 172	        await admin
> 173	          .from("social_accounts")
> 174	          .update({ refresh_token: data.refresh_token })
> 175	          .eq("id", social_account_id);
> 176	      }
> 177	      pulse("social-auth-tiktok", "healthy");
> 178	    } else if (account.platform === "youtube") {
> 179	      if (!account.refresh_token) {
> 180	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 181	          status: 400,
> 182	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 183	        });
> 184	      }
> 185	      // App credentials resolve per-user → env fallback → hard-fail (FR-PE-005/010).
> 186	      const creds = await resolveSocialAppCreds(admin, account.user_id, "youtube");
> 187	      const res = await fetch("https://oauth2.googleapis.com/token", {
> 188	        method: "POST",
> 189	        headers: { "Content-Type": "application/x-www-form-urlencoded" },
> 190	        body: new URLSearchParams({
> 191	          client_id: creds.clientId,
> 192	          client_secret: creds.clientSecret,
> 193	          grant_type: "refresh_token",
> 194	          refresh_token: account.refresh_token,
> 195	        }),
> 196	      });
> 197	      const data = await res.json();
> 198	      if (!res.ok || data.error) {
> 199	        throw new Error(data.error_description || data.error || "YouTube refresh failed");
> 200	      }
> 201	      newAccessToken = data.access_token;
> 202	      newExpiresAt = new Date(Date.now() + (data.expires_in ?? 3600) * 1000).toISOString();
> 203	
> 204	      // Google usually keeps the same refresh_token, but tolerate a rotated one on re-consent.
> 205	      // CRITICAL: only re-store when present — NEVER null an existing good refresh_token.
> 206	      if (data.refresh_token) {
> 207	        await admin
> 208	          .from("social_accounts")
> 209	          .update({ refresh_token: data.refresh_token })
> 210	          .eq("id", social_account_id);
> 211	      }
> 212	      pulse("social-auth-youtube", "healthy");
> 213	    } else if (account.platform === "pinterest") {
> 214	      if (!account.refresh_token) {
> 215	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 216	          status: 400,
> 217	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 218	        });
> 219	      }
> 220	      // App credentials resolve per-user → env fallback → hard-fail (FR-PE-005/010).
> 221	      const creds = await resolveSocialAppCreds(admin, account.user_id, "pinterest");
> 222	      // Pinterest v5: client creds go in HTTP Basic auth, not the form body.
> 223	      const res = await fetch("https://api.pinterest.com/v5/oauth/token", {
> 224	        method: "POST",
> 225	        headers: {
> 226	          "Content-Type": "application/x-www-form-urlencoded",
> 227	          Authorization: `Basic ${btoa(`${creds.clientId}:${creds.clientSecret}`)}`,
> 228	        },
> 229	        body: new URLSearchParams({
> 230	          grant_type: "refresh_token",
> 231	          refresh_token: account.refresh_token,
> 232	        }),
> 233	      });
> 234	      const data = await res.json();
> 235	      if (!res.ok || data.error) {
> 236	        throw new Error(data.error_description || data.message || data.error || "Pinterest refresh failed");
> 237	      }
> 238	      newAccessToken = data.access_token;
> 239	      newExpiresAt = new Date(Date.now() + (data.expires_in ?? 2592000) * 1000).toISOString();
> 240	
> 241	      // ROTATION: Pinterest returns a NEW refresh_token on every refresh — re-store it (never keep the old one)
> 242	      // to keep the 60d-from-last-use chain alive. Also refresh the rotating refresh-token expiry in metadata.
> 243	      if (data.refresh_token) {
> 244	        const nextMeta: Record<string, unknown> = {
> 245	          ...((account.metadata as Record<string, unknown> | null) ?? {}),
> 246	        };
> 247	        if (data.refresh_token_expires_at) {
> 248	          nextMeta.refresh_token_expires_at = data.refresh_token_expires_at;
> 249	        }
> 250	        await admin
> 251	          .from("social_accounts")
> 252	          .update({ refresh_token: data.refresh_token, metadata: nextMeta })
> 253	          .eq("id", social_account_id);
> 254	      }
> 255	      pulse("social-auth-pinterest", "healthy");
> 256	    } else {
> 257	      return new Response(JSON.stringify({ error: `Refresh not supported for ${account.platform}` }), {
> 258	        status: 400,
> 259	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 260	      });
> 261	    }
> 262	
> 263	    await admin
> 264	      .from("social_accounts")
> 265	      .update({
> 266	        access_token: newAccessToken,
> 267	        token_expires_at: newExpiresAt,
> 268	        is_active: true,
> 269	      })
> 270	      .eq("id", social_account_id);
> 271	
> 272	    // Don't return the access token — callers should read it server-side
> 273	    return new Response(JSON.stringify({ success: true, expires_at: newExpiresAt }), {
> 274	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 275	    });
> 276	  } catch (err) {
> 277	    console.error("refresh-social-token error:", err);
> 278	    // Best-effort degraded telemetry — `admin` is scoped to the try block, so build a throwaway service-role
> 279	    // client here (mirrors sibling crons). Materiality (Lei 1): the error path is a monitored signal too.
> 280	    try {
> 281	      createClient(
> 282	        Deno.env.get("SUPABASE_URL")!,
> 283	        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 284	      )
> 285	        .from("infra_health_logs")
> 286	        .insert({ service: "refresh-social-token", status: "degraded" })
> 287	        .then(() => {}, () => {});
> 288	    } catch (_telemetryErr) {
> 289	      // never let telemetry mask the original error
> 290	    }
> 291	    // FAIL-CLOSED (FR-PE-005/010): unresolved app credentials → structured 402 JSON the client can act on;
> 292	    // never fall through to a shared/default key. Mirrors social-auth-callback's SocialAppConfigError handling.
> 293	    if (err instanceof SocialAppConfigError) {
> 294	      const configResponse = socialAppConfigErrorResponse(err, corsHeaders);
> 295	      if (configResponse) return configResponse;
> 296	    }
> 297	    return new Response(JSON.stringify({ error: "Token refresh failed" }), {
> 298	      status: 500,
> 299	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 300	    });
> 301	  }
> 302	});
> 303	
> ```

## 🤖 Claude *(20:09:36)*


## 🤖 Claude *(20:09:41)*

Agora tenho o quadro completo. O `refresh-social-token` já seta `is_active: true` no sucesso (linha 268), mas **não sinaliza nada quando o refresh falha de verdade** (token revogado) — só emite telemetria. E a UI decide o alarme pelo relógio de 1h. 

Minha correção (verdadeira, não maquiagem):
- **UI**: o badge "Reconectar" passa a refletir falha real (`is_active=false` ou `metadata.needs_reauth`), não o access token de 1h.
- **Backend**: `refresh-social-token` marca `needs_reauth` só quando o refresh falha por auth (token revogado); limpa no sucesso. E o callback limpa ao reconectar.

Vou ver o trecho do upsert do callback para garantir que uma reconexão limpa o flag.

## 🤖 Claude *(20:09:43)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
  "offset": 283,
  "limit": 50
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 283	
> 284	    } else {
> 285	      throw new Error(`Unsupported platform: ${platform}`);
> 286	    }
> 287	
> 288	    const expiresAt = expiresIn
> 289	      ? new Date(Date.now() + expiresIn * 1000).toISOString()
> 290	      : null;
> 291	
> 292	    // Upsert social account
> 293	    const { error: dbError } = await supabase
> 294	      .from("social_accounts")
> 295	      .upsert(
> 296	        {
> 297	          user_id: userId,
> 298	          platform,
> 299	          access_token: accessToken,
> 300	          refresh_token: refreshToken,
> 301	          token_expires_at: expiresAt,
> 302	          platform_user_id: platformUserId,
> 303	          platform_username: platformUsername,
> 304	          scopes,
> 305	          metadata,
> 306	          is_active: true,
> 307	        },
> 308	        { onConflict: "user_id,platform" }
> 309	      );
> 310	
> 311	    if (dbError) {
> 312	      console.error("DB upsert error:", dbError);
> 313	      await supabase.from("social_accounts").insert({
> 314	        user_id: userId,
> 315	        platform,
> 316	        access_token: accessToken,
> 317	        refresh_token: refreshToken,
> 318	        token_expires_at: expiresAt,
> 319	        platform_user_id: platformUserId,
> 320	        platform_username: platformUsername,
> 321	        scopes,
> 322	        metadata,
> 323	        is_active: true,
> 324	      });
> 325	    }
> 326	
> 327	    // Materiality (Lei 1) — best-effort telemetry: a connect that persisted tokens is the success signal.
> 328	    supabase.from("infra_health_logs")
> 329	      .insert({ service: `social-auth-${platform}`, status: dbError ? "degraded" : "healthy" })
> 330	      .then(() => {}, () => {});
> 331	
> 332	    // Redirect back to frontend
> ```

## 🤖 Claude *(20:10:36)*


## 🤖 Claude *(20:10:39)*

`is_active` já é restaurado no sucesso (linha 268) e na reconexão (callback linha 306). Isso me dá o design mais limpo: **usar `is_active` como o sinal de verdade** — o refresh marca `is_active=false` só quando o token é genuinamente revogado; a UI mostra "Reconectar" por `is_active===false`, não pelo relógio de 1h. Deixa eu confirmar como `is_active` é usado hoje (pra não esconder a conta nem quebrar o auto-publish).

## 🤖 Claude *(20:10:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== is_active usages ===\"; grep -rnE \"is_active\" src/pages/SocialAccountsPage.tsx src/hooks/useSocialAccounts.ts supabase/functions/publish-social/index.ts supabase/functions/auto-publish/index.ts supabase/functions/self-heal/index.ts 2>/dev/null\necho; echo \"=== how SocialAccountsPage renders accounts (connected vs not) ===\"; sed -n '120,200p' src/pages/SocialAccountsPage.tsx",
  "description": "Check is_active dependencies + page render"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === is_active usages ===
> src/hooks/useSocialAccounts.ts:31:        .select('id, user_id, platform, platform_user_id, platform_username, is_active, token_expires_at, scopes, metadata, created_at, updated_at')
> supabase/functions/self-heal/index.ts:68:    .select("id, platform, platform_username, token_expires_at, refresh_token, is_active")
> supabase/functions/self-heal/index.ts:70:    .eq("is_active", true);
> supabase/functions/self-heal/index.ts:95:            await admin.from("social_accounts").update({ is_active: false }).eq("id", account.id);
> supabase/functions/self-heal/index.ts:116:        await admin.from("social_accounts").update({ is_active: false }).eq("id", account.id);
> supabase/functions/self-heal/index.ts:222:        .eq("is_active", true)
> supabase/functions/publish-social/index.ts:70:      .eq("is_active", true);
> 
> === how SocialAccountsPage renders accounts (connected vs not) ===
>       await disconnectAccount.mutateAsync(id);
>       toast({ title: 'Desconectado', description: `${name} foi desconectado com sucesso.` });
>     } catch {
>       toast({ title: 'Erro', description: 'Não foi possível desconectar.', variant: 'destructive' });
>     }
>   };
> 
>   const connectedPlatforms = new Set(accounts.map((a) => a.platform));
> 
>   return (
>     <div className="space-y-6">
>       <div>
>         <h1 className="text-2xl font-heading font-bold text-foreground">Redes Sociais</h1>
>         <p className="text-muted-foreground mt-1">
>           Conecte suas contas para publicar conteúdo diretamente pela plataforma.
>         </p>
>       </div>
> 
>       {/* Connected accounts */}
>       {accounts.length > 0 && (
>         <Card className="border-border/50 bg-card/50 backdrop-blur">
>           <CardHeader>
>             <CardTitle className="text-lg">Contas Conectadas</CardTitle>
>             <CardDescription>Gerencie suas redes sociais vinculadas</CardDescription>
>           </CardHeader>
>           <CardContent className="space-y-3">
>             {accounts.map((account) => {
>               const platformInfo = SUPPORTED_PLATFORMS.find((p) => p.id === account.platform);
>               const expired = isTokenExpired(account);
>               return (
>                 <div
>                   key={account.id}
>                   className="flex items-center justify-between p-3 rounded-lg border border-border/50 bg-background/50"
>                 >
>                   <div className="flex items-center gap-3">
>                     <PlatformGlyph platform={account.platform} emoji={platformInfo?.icon} />
>                     <div>
>                       <p className="font-medium text-foreground">
>                         {platformInfo?.name}
>                         {account.platform_username && (
>                           <span className="text-muted-foreground ml-1">@{account.platform_username}</span>
>                         )}
>                       </p>
>                       <div className="flex items-center gap-2 mt-0.5">
>                         {expired ? (
>                           <Badge variant="outline" className="text-amber-400 border-amber-400/30 text-xs">
>                             <AlertTriangle className="h-3 w-3 mr-1" /> Token expirado
>                           </Badge>
>                         ) : (
>                           <Badge variant="outline" className="text-emerald-400 border-emerald-400/30 text-xs">
>                             Ativa
>                           </Badge>
>                         )}
>                       </div>
>                     </div>
>                   </div>
>                   <div className="flex items-center gap-2">
>                     {expired && (
>                       <Button
>                         size="sm"
>                         variant="outline"
>                         onClick={() => handleConnect(account.platform)}
>                         disabled={connectingPlatform === account.platform}
>                       >
>                         Reconectar
>                       </Button>
>                     )}
>                     <Button
>                       size="sm"
>                       variant="ghost"
>                       className="text-destructive hover:text-destructive"
>                       onClick={() => handleDisconnect(account.id, platformInfo?.name ?? account.platform)}
>                     >
>                       <Unlink className="h-4 w-4" />
>                     </Button>
>                   </div>
>                 </div>
>               );
>             })}
>           </CardContent>
>         </Card>
> ```

## 🤖 Claude *(20:10:51)*


## 🤖 Claude *(20:10:54)*

**Descoberta importante:** o `self-heal` (linha 95, 116) **já seta `is_active=false` quando o refresh falha de verdade**, e o `refresh-social-token`/callback setam `is_active=true` no sucesso/reconexão. Ou seja, o sinal de verdade (`is_active`) **já existe e já é mantido corretamente pelo backend**. O bug é **puramente na UI**, que ignora `is_active` e usa o relógio de 1h. Isso torna o fix UI-only — risco mínimo, sem deploy de edge/migration. Deixa eu confirmar a semântica de falha do self-heal.

## 🤖 Claude *(20:10:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/self-heal/index.ts",
  "offset": 60,
  "limit": 75
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 60	  }
> 61	
> 62	  // 2. Expired tokens
> 63	  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
> 64	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 65	
> 66	  const { data: accounts } = await admin
> 67	    .from("decrypted_social_accounts")
> 68	    .select("id, platform, platform_username, token_expires_at, refresh_token, is_active")
> 69	    .eq("user_id", userId)
> 70	    .eq("is_active", true);
> 71	
> 72	  for (const account of accounts || []) {
> 73	    if (!account.token_expires_at) continue;
> 74	    const expiresAt = new Date(account.token_expires_at);
> 75	    const now = new Date();
> 76	
> 77	    if (expiresAt < now) {
> 78	      if (account.refresh_token) {
> 79	        try {
> 80	          const refreshRes = await fetch(`${supabaseUrl}/functions/v1/refresh-social-token`, {
> 81	            method: "POST",
> 82	            headers: { "Content-Type": "application/json", Authorization: `Bearer ${serviceKey}` },
> 83	            body: JSON.stringify({ social_account_id: account.id }),
> 84	          });
> 85	          if (refreshRes.ok) {
> 86	            healingResults.push({
> 87	              issue_type: "expired_token",
> 88	              issue_details: `Token ${account.platform} (@${account.platform_username}) expirado`,
> 89	              action_taken: "Token renovado automaticamente",
> 90	              success: true,
> 91	              related_resource_id: account.id,
> 92	              related_resource_type: "social_account",
> 93	            });
> 94	          } else {
> 95	            await admin.from("social_accounts").update({ is_active: false }).eq("id", account.id);
> 96	            healingResults.push({
> 97	              issue_type: "expired_token",
> 98	              issue_details: `Token ${account.platform} (@${account.platform_username}) expirado`,
> 99	              action_taken: `Refresh falhou. Conta desativada — reconecte manualmente.`,
> 100	              success: false,
> 101	              related_resource_id: account.id,
> 102	              related_resource_type: "social_account",
> 103	            });
> 104	          }
> 105	        } catch (e) {
> 106	          healingResults.push({
> 107	            issue_type: "expired_token",
> 108	            issue_details: `Token ${account.platform} expirado`,
> 109	            action_taken: `Erro ao renovar: ${e instanceof Error ? e.message : "unknown"}`,
> 110	            success: false,
> 111	            related_resource_id: account.id,
> 112	            related_resource_type: "social_account",
> 113	          });
> 114	        }
> 115	      } else {
> 116	        await admin.from("social_accounts").update({ is_active: false }).eq("id", account.id);
> 117	        healingResults.push({
> 118	          issue_type: "expired_token_no_refresh",
> 119	          issue_details: `Token ${account.platform} (@${account.platform_username}) expirado sem refresh token`,
> 120	          action_taken: "Conta desativada — reconecte manualmente",
> 121	          success: false,
> 122	          related_resource_id: account.id,
> 123	          related_resource_type: "social_account",
> 124	        });
> 125	      }
> 126	    } else if (expiresAt.getTime() - now.getTime() < 24 * 60 * 60 * 1000) {
> 127	      if (account.refresh_token) {
> 128	        try {
> 129	          const refreshRes = await fetch(`${supabaseUrl}/functions/v1/refresh-social-token`, {
> 130	            method: "POST",
> 131	            headers: { "Content-Type": "application/json", Authorization: `Bearer ${serviceKey}` },
> 132	            body: JSON.stringify({ social_account_id: account.id }),
> 133	          });
> 134	          if (refreshRes.ok) {
> ```

## 🤖 Claude *(20:11:24)*


## 🤖 Claude *(20:11:27)*

Semântica confirmada e é a ideal: `self-heal` só desativa (`is_active=false`) em **falha real** de refresh (linha 95) ou ausência de refresh_token (linha 116) — erro transitório (catch, linha 105) **não** desativa. Então `is_active` é o sinal verdadeiro de "esta conta consegue publicar", e já é mantido corretamente. **O fix é 100% UI.**

Confirmando que `isTokenExpired` não é usado em nenhum outro lugar antes de renomear:

## 🤖 Claude *(20:11:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -rnE \"isTokenExpired\" src/ 2>/dev/null; echo \"---is_active type---\"; grep -nE \"is_active\" src/integrations/supabase/types.ts | head -3",
  "description": "Confirm isTokenExpired consumers + is_active type"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/pages/SocialAccountsPage.tsx:34:  const { accounts, isLoading, disconnectAccount, initiateOAuth, isTokenExpired } = useSocialAccounts();
> src/pages/SocialAccountsPage.tsx:148:              const expired = isTokenExpired(account);
> src/hooks/useSocialAccounts.ts:90:  const isTokenExpired = (account: SocialAccount) => {
> src/hooks/useSocialAccounts.ts:101:    isTokenExpired,
> ---is_active type---
> 61:          is_active: boolean
> 78:          is_active?: boolean
> 95:          is_active?: boolean
> ```

## 🤖 Claude *(20:11:34)*


## 🤖 Claude *(20:11:35)*

Só 2 consumidores e `is_active: boolean`. Aplicando o fix.

## 🤖 Claude *(20:11:41)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts",
  "old_string": "  const isTokenExpired = (account: SocialAccount) => {\n    if (!account.token_expires_at) return false;\n    return new Date(account.token_expires_at) < new Date();\n  };\n\n  return {\n    accounts: accountsQuery.data ?? [],\n    isLoading: accountsQuery.isLoading,\n    error: accountsQuery.error,\n    disconnectAccount,\n    initiateOAuth,\n    isTokenExpired,\n  };",
  "new_string": "  // A connection needs a manual reconnect ONLY when its refresh chain is genuinely broken \u2014\n  // never merely because the ~1h OAuth access token has elapsed. The access token is renewed\n  // silently on demand (publish-social) and proactively (self-heal cron) via the stored\n  // refresh_token, so `token_expires_at < now` is normal and expected, not a failure.\n  // `is_active` is the truthful signal: self-heal flips it to false only when a real refresh\n  // fails or no refresh_token exists (self-heal:95/116); refresh-social-token (on success) and\n  // the OAuth callback (on connect) flip it back to true. Keying the \"Reconectar\" prompt off the\n  // 1h clock produced a false \"Token expirado\" alarm every hour on perfectly healthy accounts.\n  const needsReauth = (account: SocialAccount) => account.is_active === false;\n\n  return {\n    accounts: accountsQuery.data ?? [],\n    isLoading: accountsQuery.isLoading,\n    error: accountsQuery.error,\n    disconnectAccount,\n    initiateOAuth,\n    needsReauth,\n  };"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:11:44)*

Agora a página — badge e botão passam a refletir `needsReauth`, com estado saudável calmo:

## 🤖 Claude *(20:11:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "  const { accounts, isLoading, disconnectAccount, initiateOAuth, isTokenExpired } = useSocialAccounts();",
  "new_string": "  const { accounts, isLoading, disconnectAccount, initiateOAuth, needsReauth } = useSocialAccounts();"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:11:50)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "              const platformInfo = SUPPORTED_PLATFORMS.find((p) => p.id === account.platform);\n              const expired = isTokenExpired(account);",
  "new_string": "              const platformInfo = SUPPORTED_PLATFORMS.find((p) => p.id === account.platform);\n              const reconnect = needsReauth(account);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:11:55)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "                        {expired ? (\n                          <Badge variant=\"outline\" className=\"text-amber-400 border-amber-400/30 text-xs\">\n                            <AlertTriangle className=\"h-3 w-3 mr-1\" /> Token expirado\n                          </Badge>\n                        ) : (\n                          <Badge variant=\"outline\" className=\"text-emerald-400 border-emerald-400/30 text-xs\">\n                            Ativa\n                          </Badge>\n                        )}",
  "new_string": "                        {reconnect ? (\n                          <Badge variant=\"outline\" className=\"text-amber-400 border-amber-400/30 text-xs\">\n                            <AlertTriangle className=\"h-3 w-3 mr-1\" /> Reconex\u00e3o necess\u00e1ria\n                          </Badge>\n                        ) : (\n                          <Badge variant=\"outline\" className=\"text-emerald-400 border-emerald-400/30 text-xs\">\n                            Ativa\n                          </Badge>\n                        )}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:11:59)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "                    {expired && (\n                      <Button\n                        size=\"sm\"\n                        variant=\"outline\"\n                        onClick={() => handleConnect(account.platform)}\n                        disabled={connectingPlatform === account.platform}\n                      >\n                        Reconectar\n                      </Button>\n                    )}",
  "new_string": "                    {reconnect && (\n                      <Button\n                        size=\"sm\"\n                        variant=\"outline\"\n                        onClick={() => handleConnect(account.platform)}\n                        disabled={connectingPlatform === account.platform}\n                      >\n                        Reconectar\n                      </Button>\n                    )}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:12:02)*


## 🤖 Claude *(20:12:02)*

Código aplicado. Agora as provas materiais (Lei 1): tsc + lint.

## 🤖 Claude *(20:12:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== tsc ===\"; npx tsc --noEmit 2>&1 | tail -15; echo \"tsc exit: ${PIPESTATUS[0]}\"\necho \"=== eslint (touched files) ===\"; npx eslint src/hooks/useSocialAccounts.ts src/pages/SocialAccountsPage.tsx 2>&1 | tail -20; echo \"eslint exit: ${PIPESTATUS[0]}\"",
  "description": "tsc + eslint on touched files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === tsc ===
> tsc exit: 0
> === eslint (touched files) ===
> 
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx
>    82:19  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   102:19  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
> 
> ✖ 2 problems (2 errors, 0 warnings)
> 
> eslint exit: 1
> ```

## 🤖 Claude *(20:12:12)*


## 🤖 Claude *(20:12:13)*

Os 2 erros de eslint são em linhas 82/102 — fora do meu escopo (minhas edições foram em ~34/148/166/184). Vou confirmar que são pré-existentes:

## 🤖 Claude *(20:12:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== git stash check: are 82/102 pre-existing? ===\"; git stash >/dev/null 2>&1 && npx eslint src/pages/SocialAccountsPage.tsx 2>&1 | grep -E \"82:|102:|problems\" ; git stash pop >/dev/null 2>&1; echo \"restored\"",
  "description": "Confirm eslint errors pre-exist my change"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git stash check: are 82/102 pre-existing? ===
>    82:19  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
>   102:19  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
> ✖ 2 problems (2 errors, 0 warnings)
> restored
> ```

## 🤖 Claude *(20:12:22)*


## 🤖 Claude *(20:12:23)*

Confirmado pré-existentes (aparecem no HEAD limpo) — meu diff introduz **zero** lint novo. Agora build (repo principal = deploy direto pro nginx).

## 🤖 Claude *(20:12:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nls -la .env >/dev/null 2>&1 && echo \".env present \u2705 (build=deploy)\" || echo \"\u26a0\ufe0f no .env\"\necho \"=== build ===\"; bun run build 2>&1 | tail -15",
  "description": "Production build (deploys to nginx dist)",
  "timeout": 240000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> .env present ✅ (build=deploy)
> === build ===
> dist/assets/useNodeIntelligence-BQkxuKG4.js     98.78 kB │ gzip:  22.16 kB
> dist/assets/proxy-hVwjfQ7Y.js                  125.30 kB │ gzip:  41.24 kB
> dist/assets/ConstellationMatrix-BoA015nI.js    135.13 kB │ gzip:  37.39 kB
> dist/assets/CanvasEditorPage-CwHhFDYa.js       148.64 kB │ gzip:  39.40 kB
> dist/assets/index-DTZwms3u.js                  167.01 kB │ gzip:  53.33 kB
> dist/assets/ConstellationPage-iuKJyAP1.js      184.36 kB │ gzip:  63.63 kB
> dist/assets/CartesianChart-CpS0mCNN.js         325.07 kB │ gzip:  96.83 kB
> dist/assets/index-CtFzetnu.js                  663.83 kB │ gzip: 196.69 kB
> dist/assets/react-three-fiber.esm-wXgrre89.js  824.11 kB │ gzip: 221.90 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 29.27s
> ```

## 🤖 Claude *(20:12:59)*


## 🤖 Claude *(20:13:01)*

Build ✓ 29.27s → dist/ servido pelo nginx. Prova material de que o chunk novo entrou (não é falso-sucesso de deploy):

## 🤖 Claude *(20:13:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== new label present in shipped bundle? ===\"; grep -rl \"Reconex\u00e3o necess\u00e1ria\" dist/assets/ 2>/dev/null && echo \"\u2705 NEW label in dist\" || echo \"\u274c not found\"\necho \"=== old label gone from SocialAccounts chunk? ===\"; grep -rl \"Token expirado\" dist/assets/ 2>/dev/null && echo \"\u26a0\ufe0f old label still present somewhere\" || echo \"\u2705 old label absent\"\necho \"=== env baked (supabase URL in bundle)? ===\"; grep -rlE \"supabase\\.co\" dist/assets/ 2>/dev/null | head -1 && echo \"\u2705 env baked\" || echo \"\u274c no env\"",
  "description": "Verify new label shipped + env baked"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === new label present in shipped bundle? ===
> dist/assets/SocialAccountsPage-CglpbKCn.js
> ✅ NEW label in dist
> === old label gone from SocialAccounts chunk? ===
> dist/assets/SettingsPage-B7n2T7Hq.js
> ⚠️ old label still present somewhere
> === env baked (supabase URL in bundle)? ===
> dist/assets/AIOSTerminal-ZxlJZEBd.js
> ✅ env baked
> ```

## 🤖 Claude *(20:13:12)*


## 🤖 Claude *(20:13:13)*

Novo label no chunk de SocialAccountsPage ✅ e env baked ✅. Mas "Token expirado" ainda aparece em **SettingsPage** — preciso checar se é o mesmo bug de social account (mesma correção) ou algo não relacionado.

## 🤖 Claude *(20:13:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"Token expirado|token_expires_at|isTokenExpired|new Date\\(.*expires|social\" src/pages/SettingsPage.tsx | head -20",
  "description": "Check SettingsPage token expired context"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 538:      {/* TikTok / YouTube / Pinterest — BYOK app credentials (social_app_config) */}
> ```

## 🤖 Claude *(20:13:18)*


## 🤖 Claude *(20:13:19)*

"Token expirado" não está no SettingsPage diretamente — está num componente que o chunk dele agrupa. Vou localizar na fonte:

## 🤖 Claude *(20:13:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -rnE \"Token expirad\" src/ 2>/dev/null",
  "description": "Find remaining Token expirado in source"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/components/settings/MetaConfigCard.tsx:92:              Token expirado ou revogado. Gere um novo token de longa duração e cole abaixo para reconectar.
> src/hooks/useSocialAccounts.ts:97:  // 1h clock produced a false "Token expirado" alarm every hour on perfectly healthy accounts.
> ```

## 🤖 Claude *(20:13:25)*


## 🤖 Claude *(20:13:26)*

O restante é `MetaConfigCard.tsx:92` — fluxo **diferente** (Meta BYOK com token de longa duração colado manualmente, não o OAuth `social_accounts`). Vou checar se sofre do mesmo bug do relógio ou se é legítimo:

## 🤖 Claude *(20:13:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/settings/MetaConfigCard.tsx",
  "offset": 70,
  "limit": 30
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 70	  return (
> 71	    <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
> 72	      <CardHeader>
> 73	        <CardTitle className="flex items-center gap-2">
> 74	          <Share2 className="h-5 w-5 text-blue-500" />
> 75	          Meta — Facebook & Instagram
> 76	          {connected && (
> 77	            <span className="ml-2 inline-flex items-center gap-1 rounded-full bg-emerald-500/15 px-2 py-0.5 text-xs text-emerald-400">
> 78	              <CheckCircle2 className="h-3 w-3" /> Conectado{expiringSoon ? " · expira em breve" : ""}
> 79	            </span>
> 80	          )}
> 81	        </CardTitle>
> 82	        <CardDescription>
> 83	          Conecte sua conta Meta para publicar no Facebook Page e Instagram Business pelo pipeline.
> 84	          Cole o <strong>token de longa duração</strong> (60 dias) gerado no Graph API Explorer / Business Suite.
> 85	        </CardDescription>
> 86	      </CardHeader>
> 87	      <CardContent className="space-y-4">
> 88	        {needsReauth && (
> 89	          <div className="flex items-start gap-2 rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm text-destructive">
> 90	            <AlertTriangle className="h-4 w-4 mt-0.5 shrink-0" />
> 91	            <span>
> 92	              Token expirado ou revogado. Gere um novo token de longa duração e cole abaixo para reconectar.
> 93	            </span>
> 94	          </div>
> 95	        )}
> 96	
> 97	        {isLoading ? (
> 98	          <div className="flex justify-center p-6">
> 99	            <Loader2 className="h-6 w-6 animate-spin text-primary" />
> ```

## 🤖 Claude *(20:13:34)*


## 🤖 Claude *(20:13:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"needsReauth|expiringSoon|expires_at|token_expires|new Date|connected\" src/components/settings/MetaConfigCard.tsx | head -20\necho \"=== hook that provides these ===\"; grep -nE \"needsReauth|expiringSoon|expires|connected\" src/hooks/useMetaConfig.ts 2>/dev/null | head",
  "description": "MetaConfigCard reauth/expiry logic"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 18:  const { status, isLoading, upsertConfig, disconnect, connected, needsReauth, expiringSoon } = useMetaConfig();
> 26:    token_expires_at: "",
> 36:      token_expires_at: status.token_expires_at ? status.token_expires_at.slice(0, 10) : "",
> 52:        token_expires_at: form.token_expires_at ? new Date(form.token_expires_at).toISOString() : undefined,
> 76:          {connected && (
> 78:              <CheckCircle2 className="h-3 w-3" /> Conectado{expiringSoon ? " · expira em breve" : ""}
> 88:        {needsReauth && (
> 133:              <Label htmlFor="meta_token_expires">Expiração do Token (opcional)</Label>
> 135:                id="meta_token_expires" name="meta_token_expires" type="date"
> 136:                value={form.token_expires_at}
> 137:                onChange={(e) => setForm((p) => ({ ...p, token_expires_at: e.target.value }))}
> === hook that provides these ===
> 50:        token_expires_at: values.token_expires_at ?? null,
> 91:    connected: isMetaConnected(status),
> 92:    needsReauth: metaNeedsReauth(status),
> 93:    expiringSoon: metaTokenExpiringSoon(status),
> ```

## 🤖 Claude *(20:13:41)*


## 🤖 Claude *(20:13:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"metaNeedsReauth|metaTokenExpiringSoon|isMetaConnected|token_expires_at|Date|days|expira\" src/lib/meta.ts | head -30",
  "description": "Meta expiry thresholds"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 13:/** Days before token_expires_at at which the UI should nudge re-auth (FR-META-010 spirit). */
> 20:  'requires_reauth,token_expires_at,created_at,updated_at';
> 33:  token_expires_at: string | null;
> 45:  token_expires_at?: string;
> 54:export function isMetaConnected(status: MetaConfigStatus | null | undefined, now: Date = new Date()): boolean {
> 57:  if (status!.token_expires_at && new Date(status!.token_expires_at) <= now) return false;
> 62:export function metaNeedsReauth(status: MetaConfigStatus | null | undefined, now: Date = new Date()): boolean {
> 65:  if (status!.token_expires_at && new Date(status!.token_expires_at) <= now) return true;
> 69:/** Token still valid but within the reauth window (≤ N days) → soft nudge. */
> 70:export function metaTokenExpiringSoon(
> 72:  now: Date = new Date(),
> 75:  if (!isMetaConfigured(status) || !status!.token_expires_at) return false;
> 76:  const expiresAt = new Date(status!.token_expires_at);
> 77:  if (expiresAt <= now) return false; // already expired → metaNeedsReauth handles it
> ```

## 🤖 Claude *(20:13:59)*


## 🤖 Claude *(20:14:02)*

MetaConfigCard é **legítimo e diferente** — token Meta de 60 dias colado manualmente (sem refresh OAuth silencioso), então "Token expirado" ali é verdadeiro. Não precisa mexer. Meu fix está corretamente escopado ao fluxo OAuth `social_accounts` (a página `/dashboard/social`).

Agora a prova material do estado real (Lei 1): vou consultar a conta do User 0 no DB para provar que, sob a nova lógica, a linha do YouTube (is_active=true, token_expires_at no passado) renderiza **"Ativa"** em vez de "Token expirado".

## 🤖 Claude *(20:14:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nURL=$(grep -E \"^VITE_SUPABASE_URL=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\nKEY=$(grep -E \"^SB_SECRET_KEY=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\n[ -z \"$KEY\" ] && KEY=$(grep -E \"^SUPABASE_SERVICE_ROLE_KEY=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\necho \"URL set: $([ -n \"$URL\" ] && echo yes || echo NO) \u00b7 KEY set: $([ -n \"$KEY\" ] && echo yes || echo NO)\"\necho \"=== social_accounts (platform, is_active, expired-by-clock?) ===\"\ncurl -s \"$URL/rest/v1/social_accounts?select=platform,is_active,token_expires_at,platform_username\" \\\n  -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" | \\\n  python3 -c \"import sys,json,datetime;\nrows=json.load(sys.stdin);\nnow=datetime.datetime.now(datetime.timezone.utc)\nprint(f'{len(rows)} account(s):')\n[print(f\\\"  {r['platform']:10} is_active={r['is_active']!s:5} clock_expired={ (r['token_expires_at'] is not None and datetime.datetime.fromisoformat(r['token_expires_at'].replace('Z','+00:00'))<now) } exp={r['token_expires_at']}  -> OLD badge={'Token expirado' if (r['token_expires_at'] and datetime.datetime.fromisoformat(r['token_expires_at'].replace('Z','+00:00'))<now) else 'Ativa'} | NEW badge={'Reconex\u00e3o necess\u00e1ria' if r['is_active']==False else 'Ativa'}\\\") for r in rows]\"",
  "description": "Query real social_accounts state to prove badge outcome"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> URL set: yes · KEY set: yes
> === social_accounts (platform, is_active, expired-by-clock?) ===
> 6 account(s):
>   instagram  is_active=True  clock_expired=False exp=2026-08-31T04:21:08.14+00:00  -> OLD badge=Ativa | NEW badge=Ativa
>   linkedin   is_active=True  clock_expired=False exp=2026-08-25T19:53:13.817+00:00  -> OLD badge=Ativa | NEW badge=Ativa
>   facebook   is_active=True  clock_expired=False exp=2026-08-26T03:00:18.485+00:00  -> OLD badge=Ativa | NEW badge=Ativa
>   youtube    is_active=True  clock_expired=True exp=2026-07-03T00:06:54.725+00:00  -> OLD badge=Token expirado | NEW badge=Ativa
>   twitter    is_active=True  clock_expired=True exp=2026-07-03T01:07:08.343+00:00  -> OLD badge=Token expirado | NEW badge=Ativa
>   tiktok     is_active=True  clock_expired=True exp=2026-07-03T04:20:46.473+00:00  -> OLD badge=Token expirado | NEW badge=Ativa
> ```

## 🤖 Claude *(20:14:34)*


## 🤖 Claude *(20:14:39)*

**Prova material decisiva** — contra os dados REAIS de produção do User 0 (6 contas, todas `is_active=true`/saudáveis):

| Conta | is_active | Relógio expirado? | Badge ANTES | Badge DEPOIS |
|-------|-----------|-------------------|-------------|--------------|
| **youtube** | ✅ true | sim (1h) | ❌ "Token expirado" | ✅ **Ativa** |
| **twitter** | ✅ true | sim | ❌ "Token expirado" | ✅ **Ativa** |
| **tiktok** | ✅ true | sim | ❌ "Token expirado" | ✅ **Ativa** |
| instagram/linkedin/facebook | ✅ true | não (60d) | Ativa | Ativa |

Exatamente o seu sintoma: o YouTube (Google) saudável mostrava "Token expirado" à toa → agora mostra "Ativa". Nenhuma conta genuinamente quebrada é escondida (todas `is_active=true`). Vou fazer a verificação em browser real (Lei 1 / diretiva permanente) antes de commitar.

## 🤖 Claude *(20:14:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nls scripts/qa/gen-user-session.ts scripts/qa/gen-user-jwt.ts 2>/dev/null\necho \"--- agent-browser / playwright available? ---\"; ls scripts/qa/vision-qa.ts 2>/dev/null && echo \"vision-qa present\"\necho \"--- is a preview already running on common ports? ---\"; (curl -s -o /dev/null -w \"4173:%{http_code}\\n\" http://localhost:4173 2>/dev/null; curl -s -o /dev/null -w \"8080:%{http_code}\\n\" http://localhost:8080 2>/dev/null) || true",
  "description": "Check browser verification tooling"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> scripts/qa/gen-user-jwt.ts
> scripts/qa/gen-user-session.ts
> --- agent-browser / playwright available? ---
> scripts/qa/vision-qa.ts
> vision-qa present
> --- is a preview already running on common ports? ---
> 4173:000
> 8080:302
> ```

## 🤖 Claude *(20:14:50)*


## 🤖 Claude *(20:14:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsed -n '1,40p' scripts/qa/gen-user-session.ts | grep -nE \"usage|Usage|argv|preview|localStorage|storage|inject|console.log|port|4173|8080\" | head; echo \"--- what's on 8080 ---\"; curl -s -I http://localhost:8080 2>/dev/null | head -5",
  "description": "Understand session helper usage + 8080 server"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3: * Mint a REAL Supabase browser session (the full localStorage value) for logged-in UI E2E
> 7: * `sb-<ref>-auth-token`. Inject it into localStorage and the app boots already authenticated.
> 9: * Usage: bun run scripts/qa/gen-user-session.ts <email>
> 10: *   → prints ONLY the localStorage value (JSON) on stdout, or an error on stderr + exit 1.
> 14: *   localStorage.setItem('sb-<ref>-auth-token', SESSION) then reload → logged in.
> 17:import { createClient } from '@supabase/supabase-js';
> 22:const email = process.argv[2];
> 24:  console.error('Usage: gen-user-session.ts <email>  (needs SUPABASE_URL + SB_SECRET_KEY + SB_PUBLISHABLE_KEY)');
> --- what's on 8080 ---
> HTTP/1.1 302 Found
> Server: nginx
> Date: Fri, 03 Jul 2026 20:14:55 GMT
> Content-Type: text/html; charset=UTF-8
> Connection: keep-alive
> ```

## 🤖 Claude *(20:15:05)*


## 🤖 Claude *(20:15:07)*

Port 8080 = nginx direto servindo meu dist novo (sem CF, então acessível localmente). Vou: descobrir o email do dono das contas, mintar sessão real, injetar e abrir `/dashboard/social` no browser.

## 🤖 Claude *(20:15:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nURL=$(grep -E \"^VITE_SUPABASE_URL=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\nKEY=$(grep -E \"^SB_SECRET_KEY=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\n[ -z \"$KEY\" ] && KEY=$(grep -E \"^SUPABASE_SERVICE_ROLE_KEY=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\nUID=$(curl -s \"$URL/rest/v1/social_accounts?select=user_id&platform=eq.youtube&limit=1\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" | python3 -c \"import sys,json;print(json.load(sys.stdin)[0]['user_id'])\")\necho \"owner user_id: $UID\"\nEMAIL=$(curl -s \"$URL/auth/v1/admin/users?page=1&per_page=200\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" | python3 -c \"import sys,json;\nd=json.load(sys.stdin); us=d.get('users',d) if isinstance(d,dict) else d;\nprint(next((u['email'] for u in us if u['id']=='$UID'),'NOT_FOUND'))\")\necho \"owner email: $EMAIL\"",
  "description": "Resolve social account owner email"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /bin/bash: line 14: UID: readonly variable
> owner user_id: 1001
> owner email: NOT_FOUND
> ```

## 🤖 Claude *(20:15:18)*


## 🤖 Claude *(20:15:18)*

`UID` é readonly no bash — vou usar outro nome:

## 🤖 Claude *(20:15:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nURL=$(grep -E \"^VITE_SUPABASE_URL=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\nKEY=$(grep -E \"^SB_SECRET_KEY=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\n[ -z \"$KEY\" ] && KEY=$(grep -E \"^SUPABASE_SERVICE_ROLE_KEY=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r')\nOWNER=$(curl -s \"$URL/rest/v1/social_accounts?select=user_id&platform=eq.youtube&limit=1\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" | python3 -c \"import sys,json;print(json.load(sys.stdin)[0]['user_id'])\")\necho \"owner user_id: $OWNER\"\ncurl -s \"$URL/auth/v1/admin/users?page=1&per_page=300\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" | python3 -c \"import sys,json;\nd=json.load(sys.stdin); us=d.get('users',d) if isinstance(d,dict) else d;\nu=next((x for x in us if x['id']=='$OWNER'),None);\nprint('owner email:', u['email'] if u else 'NOT_FOUND')\"",
  "description": "Resolve owner email (fixed var name)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> owner user_id: ada39fae-67e1-4e53-af1c-5a18e1c108e8
> owner email: gabrielcall@gmail.com
> ```

## 🤖 Claude *(20:15:27)*


## 🤖 Claude *(20:15:28)*

Dono = `gabrielcall@gmail.com` (User 0). Mintando sessão real e abrindo no browser:

## 🤖 Claude *(20:15:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSESSION=$(bun run scripts/qa/gen-user-session.ts gabrielcall@gmail.com 2>/tmp/sess.err)\nif [ -z \"$SESSION\" ]; then echo \"FAILED:\"; cat /tmp/sess.err; else\n  echo \"session minted: ${#SESSION} chars\"\n  # storage key ref\n  REF=$(grep -E \"^VITE_SUPABASE_URL=\" .env | cut -d= -f2- | tr -d '\"'\"'\"' \\r' | sed -E 's#https://([a-z0-9]+)\\.supabase\\.co#\\1#')\n  echo \"storage key: sb-$REF-auth-token\"\n  echo \"$SESSION\" > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad/social_session.json\n  echo \"sb-$REF-auth-token\" > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad/social_storage_key.txt\n  echo \"saved to scratchpad\"\nfi",
  "description": "Mint real browser session for User 0"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> session minted: 3332 chars
> storage key: sb-bcyvddsykvehvpwstlfa-auth-token
> saved to scratchpad
> ```

## 🤖 Claude *(20:15:39)*


## 🤖 Claude *(20:15:40)*

Sessão mintada. Abrindo browser (playwright), injetando sessão e navegando pra `/dashboard/social`:

## 🤖 Claude *(20:15:43)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:mcp__playwright__browser_navigate,mcp__playwright__browser_evaluate,mcp__playwright__browser_snapshot,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_console_messages",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_navigate'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_evaluate'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_snapshot'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_take_screenshot'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_console_messages'}]
> ```

## 🤖 Claude *(20:15:46)*


🛠️ **Tool Call**: `mcp__playwright__browser_navigate`
```json
{
  "url": "http://localhost:8080/"
}
```

> **Tool Result (mcp__playwright__browser_navigate)** - ❌ Error
>
> ```
> ### Error
> Error: async initializeServer: Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome
> Run "npx playwright install chrome"
> ```

## 🤖 Claude *(20:15:59)*


## 🤖 Claude *(20:16:00)*

Chrome não está instalado pro playwright MCP. Vou tentar o driver de browser do próprio projeto (agent-browser, usado pelo vision-qa):

## 🤖 Claude *(20:16:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nwhich agent-browser 2>/dev/null; ls ~/.cache/ms-playwright/ 2>/dev/null | head; echo \"---chrome bins---\"; ls /opt/google/chrome/chrome 2>/dev/null; which google-chrome chromium chromium-browser 2>/dev/null; echo \"---vision-qa header usage---\"; sed -n '1,25p' scripts/qa/vision-qa.ts | grep -nE \"usage|Usage|argv|browser|agent-browser|screenshot|URL\"",
  "description": "Locate any available browser engine"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser
> b
> chromium-1217
> chromium-1226
> chromium_headless_shell-1217
> chromium_headless_shell-1226
> ffmpeg-1011
> mcp-chrome-6d4d142
> mcp-chrome-8a5edab
> mcp-chrome-dc082d7
> mcp-chrome-for-testing-8a5edab
> ---chrome bins---
> ---vision-qa header usage---
> 15: *   VISION_MCP_URL overrides endpoint (default public https://mcp.mcorch.com/mcp).
> 21:const URL = process.env.VISION_MCP_URL ?? "https://mcp.mcorch.com/mcp";
> 24:const mode = process.argv[2];
> ```

## 🤖 Claude *(20:16:11)*


## 🤖 Claude *(20:16:12)*

`agent-browser` existe + chromium instalado. Vou ver a interface do agent-browser:

## 🤖 Claude *(20:16:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "agent-browser --help 2>&1 | head -40",
  "description": "agent-browser CLI interface"
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

## 🤖 Claude *(20:16:17)*


## 🤖 Claude *(20:16:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "agent-browser --help 2>&1 | sed -n '40,90p'",
  "description": "agent-browser more commands (eval/storage)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   screenshot [path]          Take screenshot
>   pdf <path>                 Save as PDF
>   snapshot                   Accessibility tree with refs (for AI)
>   eval <js>                  Run JavaScript
>   connect <port|url>         Connect to browser via CDP
>   close [--all]              Close browser (--all closes every session)
> 
> Navigation:
>   back                       Go back
>   forward                    Go forward
>   reload                     Reload page
> 
> Get Info:  agent-browser get <what> [selector]
>   text, html, value, attr <name>, title, url, count, box, styles, cdp-url
> 
> Check State:  agent-browser is <what> <selector>
>   visible, enabled, checked
> 
> Find Elements:  agent-browser find <locator> <value> <action> [text]
>   role, text, label, placeholder, alt, title, testid, first, last, nth
> 
> Mouse:  agent-browser mouse <action> [args]
>   move <x> <y>, down [btn], up [btn], wheel <dy> [dx]
> 
> Browser Settings:  agent-browser set <setting> [value]
>   viewport <w> <h>, device <name>, geo <lat> <lng>
>   offline [on|off], headers <json>, credentials <user> <pass>
>   media [dark|light] [reduced-motion]
> 
> Network:  agent-browser network <action>
>   route <url> [--abort|--body <json>] [--resource-type <csv>]
>   unroute [url]
>   requests [--clear] [--filter <pattern>]
>   har <start|stop> [path]
> 
> Storage:
>   cookies [get|set|clear]    Manage cookies (set supports --url, --domain, --path, --httpOnly, --secure, --sameSite, --expires)
>                              Or:  cookies set --curl <file> [--domain <host>] (auto-detects JSON/cURL/Cookie-header files)
>   storage <local|session>    Manage web storage
> 
> Tabs:
>   tab [new|list|close|<n>]   Manage tabs
> 
> Diff:
>   diff snapshot              Compare current vs last snapshot
>   diff screenshot --baseline Compare current vs baseline image
>   diff url <u1> <u2>         Compare two pages
> 
> Debug:
>   trace start|stop [path]    Record Chrome DevTools trace
>   profiler start|stop [path] Record Chrome DevTools profile
> ```

## 🤖 Claude *(20:16:28)*


## 🤖 Claude *(20:16:30)*

`eval` + `screenshot` disponíveis. Executando a verificação visual (viewport 1080p, injeta sessão, abre `/dashboard/social`):

## 🤖 Claude *(20:16:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad\nKEY=$(cat $SP/social_storage_key.txt)\nSESSION_B64=$(base64 -w0 $SP/social_session.json)\nagent-browser set viewport 1920 1080 >/dev/null 2>&1\nagent-browser open \"http://localhost:8080/\" 2>&1 | tail -1\nagent-browser eval \"localStorage.setItem('$KEY', atob('$SESSION_B64')); 'set:'+('$KEY')\" 2>&1 | tail -1\nagent-browser open \"http://localhost:8080/dashboard/social\" 2>&1 | tail -1\nsleep 2\nagent-browser open \"http://localhost:8080/dashboard/social\" 2>&1 | tail -1\necho \"=== page text (badges) ===\"\nagent-browser get text body 2>&1 | grep -iE \"Reconex|Token expirad|Ativa|YouTube|Twitter|TikTok|Redes Sociais|Contas Conectadas|@\" | head -30",
  "description": "Inject session, open social page, read badges"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   https://gcrux.com/
> "set:sb-bcyvddsykvehvpwstlfa-auth-token"
>   https://gcrux.com/
>   https://gcrux.com/
> === page text (badges) ===
> contato@gcrux.com
> ```

## 🤖 Claude *(20:17:09)*


## 🤖 Claude *(20:17:11)*

Port 8080 é o vhost do gcrux.com (landing), não o app. Vou subir o `vite preview` do meu dist e apontar o browser pra lá (receita documentada de E2E logado):

## 🤖 Claude *(20:17:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -E '\"preview\"|\"dev\"' package.json",
  "description": "Check preview script"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>     "dev": "vite",
>     "preview": "vite preview",
> ```

## 🤖 Claude *(20:17:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nnohup npx vite preview --port 4173 --strictPort >/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad/preview.log 2>&1 &\necho \"preview pid $!\"",
  "description": "Start vite preview of dist on 4173",
  "run_in_background": true
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Command running in background with ID: b9jz0tm19. Output is being written to: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/tasks/b9jz0tm19.output. You will be notified when it completes. To check interim output, use Read on that file path.
> ```

## 🤖 Claude *(20:17:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nfor i in 1 2 3 4 5; do curl -s -o /dev/null -w \"%{http_code}\" http://localhost:4173/ 2>/dev/null && break; sleep 1; done\necho \" <- preview status\"",
  "description": "Wait for preview to be ready"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 200 <- preview status
> ```

## 🤖 Claude *(20:17:25)*


## 🤖 Claude *(20:17:26)*

Preview servindo 200. Injetando sessão e abrindo a página no preview:

## 🤖 Claude *(20:17:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad\nKEY=$(cat $SP/social_storage_key.txt)\nSESSION_B64=$(base64 -w0 $SP/social_session.json)\nagent-browser open \"http://localhost:4173/\" 2>&1 | tail -1\nagent-browser eval \"localStorage.setItem('$KEY', atob('$SESSION_B64')); 'injected'\" 2>&1 | tail -1\nagent-browser open \"http://localhost:4173/dashboard/social\" 2>&1 | tail -1\nsleep 3\necho \"=== url now ===\"; agent-browser get url 2>&1 | tail -1\necho \"=== badges/text ===\"\nagent-browser get text body 2>&1 | grep -iE \"Reconex|Token expirad|Ativa|YouTube|Twitter|TikTok|Instagram|LinkedIn|Facebook|Redes Sociais|Contas Conectadas\" | head -30",
  "description": "Inject session + open social page on preview"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   http://localhost:4173/
> "injected"
>   http://localhost:4173/dashboard/social
> === url now ===
> http://localhost:4173/dashboard/social
> === badges/text ===
> Redes Sociais
> Redes Sociais
> Redes Sociais
> Contas Conectadas
> Gerencie suas redes sociais vinculadas
> Twitter / X@gabrielOrchAI
> Ativa
> YouTube
> Ativa
> Instagram@gabrielorchai
> Ativa
> TikTok@-000_YIbtWK1DgoGB7hArg1_s0DU8NqSWOHo
> Ativa
> Facebook@gabrielorchai
> Ativa
> LinkedIn@Gabriel AI
> Ativa
> Conecte novas redes sociais à sua conta
> LinkedIn
> Instagram
> Facebook
> Twitter / X
> TikTok
> YouTube
> ```

## 🤖 Claude *(20:17:41)*


## 🤖 Claude *(20:17:42)*

Confirmação visual E2E (logado como User 0): **todas as 6 contas mostram "Ativa"** — incluindo YouTube, Twitter e TikTok (as três que estavam com relógio expirado e antes gritavam "Token expirado"). **Zero** badges de "Token expirado". Capturando o screenshot pro registro:

## 🤖 Claude *(20:17:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad\nagent-browser screenshot \"$SP/social-page-fixed.png\" 2>&1 | tail -1\nls -la \"$SP/social-page-fixed.png\" 2>/dev/null\necho \"=== assert: no expired badge, count of Ativa ===\"\nagent-browser get text body 2>&1 | grep -c \"Ativa\"\necho \"expired-count:\"; agent-browser get text body 2>&1 | grep -ciE \"Token expirad|Reconex\"",
  "description": "Screenshot + assert zero expired badges"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad/social-page-fixed.png
> -rw-rw-r-- 1 ubuntu ubuntu 131071 Jul  3 17:17 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad/social-page-fixed.png
> === assert: no expired badge, count of Ativa ===
> 6
> expired-count:
> 0
> ```

## 🤖 Claude *(20:17:55)*


## 🤖 Claude *(20:17:56)*

6× "Ativa", 0× expirado. Vou ver o screenshot com meus próprios olhos (Lei 1) pra confirmar que renderizou de verdade:

## 🤖 Claude *(20:17:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7bb4586f-3050-4a11-99ef-569c4b75c080/scratchpad/social-page-fixed.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(20:18:13)*


## 🤖 Claude *(20:18:15)*

Confirmação visual completa (Lei 1 — meus olhos): render limpo, logado como User 0 (4571 mcoCoins), **as 6 contas com badge verde "Ativa"** — Twitter, YouTube, Instagram, TikTok, Facebook, LinkedIn. Zero "Token expirado". O bug está corrigido e provado E2E.

Limpando o ambiente e commitando:

## 🤖 Claude *(20:18:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nagent-browser close --all >/dev/null 2>&1; echo \"browser closed\"\ngit status --short",
  "description": "Close browser + check git status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> browser closed
>  M .agents/workflows/handson.md
>  M src/hooks/useSocialAccounts.ts
>  M src/pages/SocialAccountsPage.tsx
> ```

## 🤖 Claude *(20:18:23)*


## 🤖 Claude *(20:18:24)*

dist/ é gitignored (nginx serve direto). `handson.md` é modificação pré-existente (não minha). Commitando só meus 2 arquivos:

## 🤖 Claude *(20:18:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\npkill -f \"vite preview\" 2>/dev/null; echo \"preview stopped\"\ngit add src/hooks/useSocialAccounts.ts src/pages/SocialAccountsPage.tsx\ngit commit -q -m \"fix(social): badge de conex\u00e3o reflete sa\u00fade real, n\u00e3o o rel\u00f3gio de 1h do access token\n\nContas OAuth (YouTube/Google, Twitter, TikTok) apareciam como 'Token expirado'\na cada hora mesmo saud\u00e1veis: a UI decidia o alerta por token_expires_at < now,\nmas o access token do OAuth vive ~1h por design e \u00e9 renovado silenciosamente\nvia refresh_token (publish-social sob demanda + self-heal proativo). O sinal de\nverdade \u00e9 is_active, que o backend j\u00e1 mant\u00e9m \u2014 self-heal s\u00f3 desativa em falha\nreal de refresh (revoga\u00e7\u00e3o/sem refresh_token). O badge/Reconectar agora keia por\nis_active; usu\u00e1rio n\u00e3o reconecta mais de hora em hora.\n\nProvado E2E contra produ\u00e7\u00e3o (User 0, 6 contas is_active=true): YouTube/Twitter/\nTikTok migram de 'Token expirado' \u2192 'Ativa'; nenhuma conta saud\u00e1vel escondida.\" && git log --oneline -1",
  "description": "Commit the social badge fix"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 144
> ```

## 🤖 Claude *(20:18:38)*


## 🤖 Claude *(20:18:39)*

Exit 144 pode ter sido o `pkill` atingindo o próprio processo. Vou verificar se o commit entrou:

## 🤖 Claude *(20:18:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit log --oneline -3; echo \"--- status ---\"; git status --short",
  "description": "Verify commit landed"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> c38519a docs(handoff): seal loop it.1+it.2 — anticorpo assets owner-signing + BoK Higgsfield MCP (mesh 9048)
> 19d20b5 docs(readme): v6.83.2 — loop it.1+it.2 (anticorpo assets + BoK Higgsfield MCP, mesh 9048)
> 81e6492 chore(loop): registra it.2 2026-07-03 — BoK amendment Higgsfield MCP + gate OAuth na Fila
> --- status ---
>  M .agents/workflows/handson.md
>  M src/hooks/useSocialAccounts.ts
>  M src/pages/SocialAccountsPage.tsx
> ```

## 🤖 Claude *(20:18:46)*


## 🤖 Claude *(20:18:47)*

Commit não entrou (o `pkill` no mesmo comando abortou o shell). Arquivos intactos. Refazendo o commit isolado:

## 🤖 Claude *(20:18:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add src/hooks/useSocialAccounts.ts src/pages/SocialAccountsPage.tsx\ngit commit -q -m \"fix(social): badge de conex\u00e3o reflete sa\u00fade real, n\u00e3o o rel\u00f3gio de 1h do access token\n\nContas OAuth (YouTube/Google, Twitter, TikTok) apareciam como 'Token expirado' a\ncada hora mesmo saud\u00e1veis: a UI decidia o alerta por token_expires_at < now, mas o\naccess token do OAuth vive ~1h por design e \u00e9 renovado silenciosamente via\nrefresh_token (publish-social sob demanda + self-heal proativo). O sinal de verdade\n\u00e9 is_active, que o backend ja mantem \u2014 self-heal so desativa em falha real de\nrefresh (revogacao/sem refresh_token). O badge/Reconectar agora keia por is_active;\nusuario nao reconecta mais de hora em hora.\n\nProvado E2E contra producao (User 0, 6 contas is_active=true): YouTube/Twitter/TikTok\nmigram de 'Token expirado' -> 'Ativa'; nenhuma conta saudavel escondida.\"\ngit log --oneline -1",
  "description": "Re-commit the social badge fix cleanly"
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
> [90m5:18PM[0m [32mINF[0m 1 commits scanned.
> [90m5:18PM[0m [32mINF[0m scan completed in 9.18ms
> [90m5:18PM[0m [32mINF[0m no leaks found
> 
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
> 4f4b709 fix(social): badge de conexão reflete saúde real, não o relógio de 1h do access token
> ```

## 🤖 Claude *(20:19:07)*


## 🤖 Claude *(20:19:10)*

Commit **`4f4b709`** selado (lefthook: gitleaks limpo, secret-scan ✅; post-commit mesh-reingest disparado). E o dist/ que buildei já está no ar em login.mcorch.com — basta **Ctrl+Shift+R** que você verá as 6 contas "Ativa".

Agora vou sintetizar o aprendizado (Mandato Obstáculo→Síntese) e registrar os requisitos exatos do TikTok pra Fila Sovereign, já que o rebrand virá pelo handoff do Claude Design.

## 🤖 Claude *(20:19:22)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/reference_social_oauth_badge_health_signal.md",
  "content": "---\nname: reference_social_oauth_badge_health_signal\ndescription: UI de conex\u00e3o social N\u00c3O deve alarmar pelo rel\u00f3gio de 1h do access token \u2014 is_active \u00e9 o sinal de verdade\nmetadata:\n  type: reference\n---\n\n2026-07-03 (`4f4b709`): a p\u00e1gina `/dashboard/social` mostrava \"Token expirado / Reconectar\" **a cada hora** em contas OAuth saud\u00e1veis (YouTube/Google, Twitter, TikTok). Falso alarme.\n\n**Causa:** `useSocialAccounts.isTokenExpired` decidia o badge por `token_expires_at < now`. O access token OAuth vive **~1h por design** (`social-auth-callback` grava `expires_in ?? 3600` p/ YouTube) \u2014 expirar \u00e9 normal, n\u00e3o \u00e9 falha.\n\n**Verdade:** o token \u00e9 renovado silenciosamente via `refresh_token`:\n- `publish-social` renova sob demanda antes de publicar (`index.ts:85-109`).\n- `self-heal` renova proativamente e **s\u00f3 seta `is_active=false` em falha REAL** de refresh / aus\u00eancia de refresh_token (`self-heal:95,116`); erro transit\u00f3rio (catch) n\u00e3o desativa.\n- `refresh-social-token` (sucesso) e o callback OAuth (conex\u00e3o) setam `is_active=true`.\n\n**Regra:** o badge/Reconectar deve keiar por **`account.is_active === false`**, nunca pelo rel\u00f3gio do access token. `is_active` j\u00e1 \u00e9 o sinal de sa\u00fade mantido pelo backend. Init do YouTube est\u00e1 correto (`access_type=offline&prompt=consent` \u2192 refresh_token de longa dura\u00e7\u00e3o; app **em produ\u00e7\u00e3o** no Google = refresh ~permanente).\n\n**Nuance:** `MetaConfigCard` (Meta BYOK, token colado de 60d, sem refresh OAuth) \u00e9 caso diferente e leg\u00edtimo \u2014 ali \"Token expirado\" reflete expiry real de 60d. N\u00e3o confundir com o fluxo `social_accounts`.\n\nProvado E2E (vite preview do dist + sess\u00e3o injetada gen-user-session.ts, ver [[reference_loggedin_e2e_local_preview]]): User 0, 6 contas is_active=true \u2192 todas \"Ativa\", 0 \"Token expirado\".\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/reference_social_oauth_badge_health_signal.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:19:39)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_tiktok_review_rebrand_requirements.md",
  "content": "---\nname: project_tiktok_review_rebrand_requirements\ndescription: TikTok app review REPROVADO \u2014 checklist de branding/consist\u00eancia; resolver junto ao grande rebranding (handoff do Claude Design)\nmetadata:\n  type: project\n---\n\n2026-07-03: TikTok recusou a publica\u00e7\u00e3o do app (\"Changes to your app were not approved for production\"). **N\u00e3o \u00e9 bug t\u00e9cnico \u2014 \u00e9 branding/consist\u00eancia.** O Sovereign vai atacar junto ao **grande rebranding** que vir\u00e1 por handoff do Claude Design \u2192 Claude Code (rebrand + redesign, aplicar em produ\u00e7\u00e3o como j\u00e1 se faz no dev).\n\n**Checklist exato do revisor TikTok (resolver antes de resubmeter):**\n1. **App icon consistente** \u2014 o \u00edcone no TikTok Basic Info deve ser ID\u00caNTICO ao exibido no site, nos links de TOS/Privacy e no **favicon** do browser. Hoje divergem.\n2. **Terms of Service + Privacy Policy** \u2014 links **v\u00e1lidos, ativos e vis\u00edveis** na URL do site **sem precisar abrir menu nem logar**.\n3. **Website URL** \u2014 site externo **totalmente desenvolvido**; n\u00e3o pode ser landing nem p\u00e1gina de login. Se for login, fornecer conta+senha de teste no campo \"Apply Reason\".\n4. **V\u00eddeo demo** \u2014 mostrar o fluxo **end-to-end completo** da integra\u00e7\u00e3o TikTok (usar **sandbox** ou mockup). Imagens **HD** (as enviadas estavam pixeladas). **Todos** os produtos/escopos selecionados devem aparecer no v\u00eddeo; remover escopos n\u00e3o usados antes do review. Usar sandbox obrigatoriamente.\n\n**Escopos atuais do app:** `video.publish,user.info.basic` (ver `social-auth-init` \u00a7TikTok \u2014 scope COMMA-separated, ver [[reference_tiktok_unaudited_private_account]]).\n\n**Gate:** rebrand \u00e9 tarefa grande e Sovereign-driven (aguarda handoff do Claude Design). O item TikTok fica na **Fila de A\u00e7\u00e3o Sovereign** at\u00e9 o rebrand entregar \u00edcone/favicon/TOS/Privacy consistentes + site desenvolvido. Depois: regravar v\u00eddeo demo sandbox HD e resubmeter.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_tiktok_review_rebrand_requirements.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:19:42)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Memory Index
> 2	
> 3	- [Buckets de mídia privados → signed URL owner-scoped, nunca assar URL](reference_private_bucket_asset_signing.md) — 2026-07-03: normalizador re-assina no render (asset-url.ts/StorageMedia); policy 4-rotas =auth.uid; PK client-writable (vm_canvas_projects.id) = oráculo de auth → trigger force_server_id INSERT+UPDATE. Mídia sumida era do dono, não smoke.
> 4	
> 5	- [Contrato REAL da API Higgsfield + MCP oficial (sonda 2026-07-03)](reference_higgsfield_provider_contract.md) — soul/{mode} path-literal, compose nunca existiu; refs = custom_reference_id async (minutos); sentinel smoke-higgsfield-schema.ts pina tudo; MCP BYOK só catálogo, conta = OAuth (DCR ok).
> 6	- [Doutrina open-source-first / USD=0 / equity + Gabriel AI co-executivo](feedback_opensource_first_zero_cost_equity.md) — 2026-06-30: tudo self-hostável vira microserviço próprio (equity); custo USD externo=0 é gate de GO; Gabriel AI = co-CAI→co-CTI.
> ```

## 🤖 Claude *(20:19:50)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "# Memory Index\n\n- [Buckets de m\u00eddia privados \u2192 signed URL owner-scoped, nunca assar URL](reference_private_bucket_asset_signing.md)",
  "new_string": "# Memory Index\n\n- [Badge de conex\u00e3o social = is_active, n\u00e3o o rel\u00f3gio de 1h do access token](reference_social_oauth_badge_health_signal.md) \u2014 2026-07-03 `4f4b709`: \"/dashboard/social\" gritava \"Token expirado\" a cada hora em contas OAuth saud\u00e1veis; token renova sozinho (publish-social/self-heal via refresh_token). is_active \u00e9 o sinal de verdade. MetaConfigCard (60d BYOK) \u00e9 caso leg\u00edtimo \u00e0 parte.\n- [TikTok app review REPROVADO \u2014 checklist branding, resolver no rebrand](project_tiktok_review_rebrand_requirements.md) \u2014 2026-07-03: n\u00e3o \u00e9 bug; \u00edcone/favicon/TOS/Privacy consistentes + site desenvolvido + v\u00eddeo demo sandbox HD end-to-end. Gate: grande rebranding (handoff Claude Design). Fila Sovereign.\n- [Buckets de m\u00eddia privados \u2192 signed URL owner-scoped, nunca assar URL](reference_private_bucket_asset_signing.md)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:19:57)*


## 🤖 Claude *(20:20:14)*

Pronto, Maestro. Resumo executivo:

## ✅ Bug do token — corrigido, provado e no ar
**`4f4b709`** — `fix(social): badge de conexão reflete saúde real, não o relógio de 1h do access token`

- **Resposta à sua pergunta:** não, o usuário **não** vai reconectar de hora em hora. O access token do Google expira em ~1h por design, mas o sistema **já renova sozinho** via `refresh_token` (no publish e no self-heal). O alarme era só a UI decidindo "expirado" pelo relógio de 1h em vez do sinal de saúde real (`is_active`).
- **Correção:** o badge/"Reconectar" agora reflete `is_active` (que o backend só desativa em falha REAL de refresh/token revogado), não o relógio.
- **Provado E2E** contra a produção do User 0 (6 contas, `is_active=true`): YouTube, Twitter e TikTok migraram de "Token expirado" → **"Ativa"**; confirmação visual no browser (screenshot: as 6 verdes, zero alertas). Já está buildado no dist/ que o nginx serve → **Ctrl+Shift+R** em login.mcorch.com/dashboard/social e você vê. Como você já reconectou manualmente, não precisa fazer nada.

## 📋 TikTok — não é bug, é branding (fica pro rebrand)
A recusa é 100% consistência de marca. Registrei o **checklist exato do revisor** na Fila Sovereign / memória:
1. **Ícone idêntico** em TikTok + site + links TOS/Privacy + **favicon**.
2. **TOS + Privacy** válidos, ativos e **visíveis sem menu/login** na URL do site.
3. **Site desenvolvido** (não landing/login) — se for login, dar conta de teste no "Apply Reason".
4. **Vídeo demo** end-to-end em **sandbox**, **HD** (o enviado estava pixelado), mostrando **todos** os escopos (`video.publish,user.info.basic`) — remover escopo não usado antes de resubmeter.

Concordo: **quanto antes o rebranding, melhor** — ele destrava o TikTok e o resto. Aguardo o handoff do Claude Design; quando chegar, eu executo o rebrand+redesign em produção como fazemos no dev.

## Sobre o `/loop`
Ainda **adianta** — este bug era exatamente um item novo desbloqueado que o loop pegaria. O que está "vazio" é só o frontier *autônomo*: os próximos grandes passos (rebrand, OAuth Higgsfield, apps YT/TikTok) são **Sovereign-gated** — precisam de você/Claude Design. Enquanto o rebrand não chega, me manda bugs/ajustes assim e eu fecho em malha curta com prova material, como este.

Quer que eu já comece a **preparar o terreno do rebrand** (auditar onde ícone/favicon/nome "Magic Constellation" vs "MCORCH"/"Gabriel AI" aparecem hoje, pra o handoff do Claude Design cair num mapa pronto)? Isso é trabalho desbloqueado e adianta o gargalo real.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-03 - Resolver alertas de produção e migrations]]
> * **Próxima Sessão**: [[2026-07-03 - Verificar segurança após correção de assets]]
%% --- TIMELINE END --- %%

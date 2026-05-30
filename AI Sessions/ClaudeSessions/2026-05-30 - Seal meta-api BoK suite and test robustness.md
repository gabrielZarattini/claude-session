# Seal meta-api BoK suite and test robustness
**Date:** 2026-05-30 | **Session ID:** `d5a18d1e-e61e-43ea-ac57-2f21f4706303`

---

## 👤 User *(21:16:57)*

faça o /handson após analisar o handoff tambem do antigravity.: 

Viewed seed-meta-api-bok-seal.ts:1-29
Ran command: `git status --short`
Ran command: `echo "=== 1a. Secrets check ===" && git diff HEAD | grep -E "(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{20,}|STRIPE_|SECRET_KEY|ACCESS_TOKEN|api_key\s*=\s*['\"][^'\"]{10,})" | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_" | head -20 && echo "=== 1b. JWT check ===" && (grep -rL "Authorization\|jwt\|JWT\|service_role" supabase/functions/*/index.ts | grep -v "get-infra-status\|watchdog" || echo "TODAS AS FUNÇÕES: JWT verificado ✅") && echo "=== 1c. Balance update check ===" && (grep -rn "mco_balance.*update\|UPDATE.*mco_balance" src/ | grep -v "settings\|top.up\|topup\|SettingsPage" | head -10 || echo "SEM VIOLAÇÕES ✅") && echo "=== 1d. RLS bypass check ===" && (grep -rn "service_role\|bypass.*rls\|rls.*bypass" src/ | head -10 || echo "SEM VIOLAÇÕES ✅") && echo "=== 1e. Console logs check ===" && (grep -rn "console\.log.*token\|console\.log.*key\|console\.log.*secret\|console\.log.*password" src/ | head -10 || echo "SEM LOGS SENSÍVEIS ✅")`
Ran command: `git add docs/bok/meta-api/ && git commit -m "docs(bok): meta-api BoK suite and agents system

Co-Authored-By: Antigravity IDE <noreply@google.com>" && git add scripts/seed-meta-api-bok-seal.ts && git commit -m "chore(scripts): seed script for meta-api BoK seal

Co-Authored-By: Antigravity IDE <noreply@google.com>"`
Ran command: `source .env && SESSION_PHASE="meta-api-bok-seal" && SESSION_SUMMARY="Sealed the BoK documentation suite and 8-agent system for meta-api (Facebook, Instagram, WhatsApp, Ads, MCP)" && RESPONSE=$(curl -s -X POST "${SUPABASE_URL}/rest/v1/mcorch_nodes" -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" -H "Content-Type: application/json" -H "Prefer: return=representation" -d "{
    \"name\": \"session-handoff-$(date +%Y%m%d)-${SESSION_PHASE}\",
    \"node_type\": \"handoff\",
    \"content\": \"[HANDOFF SEAL] ${SESSION_SUMMARY}\",
    \"stability_score\": 1.0,
    \"metadata\": {
      \"session\": \"${SESSION_PHASE}\",
      \"sealed_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
      \"agent\": \"antigravity-ide\",
      \"commits\": \"$(git log --oneline -5 | head -5 | tr '\n' '|')\"
    }
  }") && NODE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['id'] if isinstance(d,list) else d.get('id','error'))" 2>/dev/null) && echo "Nó de Handoff persistido: ${NODE_ID}" && echo "{\"handoffNodeId\": \"${NODE_ID}\"}" > proof-manifest.json`
Ran command: `source .env && curl -s -X POST "${SUPABASE_URL}/functions/v1/embed-mcorch-node" -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" -H "Content-Type: application/json" -d "{\"record\": {\"id\": \"2eb1aca5-7eda-4911-ab10-b3b0db129665\"}}"`
Ran command: `source .env && curl -s -X POST "${SUPABASE_URL}/functions/v1/embed-mcorch-node" -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" -H "Content-Type: application/json" -d "{\"node_id\": \"2eb1aca5-7eda-4911-ab10-b3b0db129665\"}"`
Ran command: `curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id&limit=1" -H "apikey: $(grep SUPABASE_SERVICE_ROLE_KEY .env | cut -d'\"' -f2)" -H "Authorization: Bearer $(grep SUPABASE_SERVICE_ROLE_KEY .env | cut -d'\"' -f2)" -H "Prefer: count=exact" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'`
Ran command: `source .env && curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id&limit=1" -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" -H "Prefer: count=exact" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'`
Ran command: `source .env && curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id&limit=1" -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" -H "Prefer: count=exact" -I`
Viewed README.md:1-800
Searched for "What's new"
Viewed README.md:150-175
Edited README.md
Edited HANDOFF.md
Ran command: `grep -nE "(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36})" HANDOFF.md | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_\|digest\|sha256\|hash\|fingerprint" | head -20 || echo "HANDOFF.md limpo de credenciais ✅"`
Ran command: `grep -nE "(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36})" HANDOFF.md || echo "HANDOFF.md clean"`
Ran command: `git status --short`
Ran command: `git diff memory/heartbeat-state.json`
Ran command: `git checkout memory/heartbeat-state.json`
Ran command: `git add README.md && git commit -m "docs(readme): v6.14.2 — meta-api BoK suite & agents system

Co-Authored-By: Antigravity IDE <noreply@google.com>" && git add HANDOFF.md && git commit -m "docs(handoff): seal v6.14.2 — meta-api BoK suite & agents system

Co-Authored-By: Antigravity IDE <noreply@google.com>"`
Ran command: `bun run scripts/qa/run-audit.ts HANDOFF.md`
Used tool: manage_task
Used tool: schedule

I am waiting for the material proof audit to run and complete. I will keep you posted.

Used tool: manage_task
Viewed task-158.log
Viewed run-audit.ts:1-242
Used tool: manage_task
Used tool: schedule

I am waiting for the material proof audit script (`run-audit.ts`) to complete. The script executes the entire unit test suite and compilation check internally, which takes around 2 minutes. I will notify you once it finishes.

Used tool: manage_task
Viewed task-158.log
Used tool: schedule

I am waiting for the audit task to complete. Since the node event loop is blocked by synchronous execution of tests and compilation checks inside the script, the logs will only be written once the entire audit completes. I will notify you once it finishes.

Used tool: manage_task
Ran command: `ps aux | grep -E "bun|tsc|vitest" | grep -v grep`
Ran command: `git status`
Ran command: `git log -n 10 --oneline; echo "--- REMOTE ---"; git log origin/main -n 10 --oneline`
Ran command: `git diff origin/main..main --name-status`
Ran command: `git rebase origin/main`
Ran command: `git diff README.md`
Ran command: `source .env && curl -s "${SUPABASE_URL}/rest/v1/mcorch_nodes?select=id&limit=1" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Prefer: count=exact" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'`
Used tool: manage_task

I will now wait for the node count query to complete so we can get the exact current node count.

Ran command: `source .env && curl -i -s "${SUPABASE_URL}/rest/v1/mcorch_nodes?select=id&limit=1" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Prefer: count=exact"`
Ran command: `git rebase --abort`
Ran command: `git branch temp-local-main && git reset --hard origin/main`
Ran command: `git cherry-pick 6315cc9 && git cherry-pick 4c1df43`
Ran command: `git log -n 5 --oneline`
Viewed README.md:1-40
Viewed README.md:145-180
Viewed seed-meta-api-bok-seal.ts:1-100
Ran command: `source .env && curl -s "${SUPABASE_URL}/rest/v1/mcorch_nodes?name=eq.bok-scribe-seal-meta-api-v1" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}"`
Used tool: manage_task
Ran command: `source .env && curl -s "${SUPABASE_URL}/rest/v1/mcorch_nodes?id=eq.2eb1aca5-7eda-4911-ab10-b3b0db129665" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}"`
Used tool: manage_task
Ran command: `git diff origin/main temp-local-main HANDOFF.md`
Viewed HANDOFF.md:1-80
Edited HANDOFF.md
Edited README.md
Viewed README.md:150-165
Edited README.md
Ran command: `npm run --help || cat package.json | grep -A 10 -i '"scripts"'`
Viewed package.json:1-125
Ran command: `npx tsc --noEmit`
Ran command: `npm run test`
Used tool: manage_task

I will wait for the Vitest test execution to complete.

Viewed canvas-video-async-smoke.test.ts:1-335
Viewed run-audit.ts:1-100
Viewed canvas-video-async-smoke.test.ts:255-275
Ran command: `source .env && curl -s "${SUPABASE_URL}/rest/v1/vm_canvas_assets?limit=1" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}"`
Used tool: manage_task
Edited canvas-video-async-smoke.test.ts
Ran command: `bun run scripts/qa/run-audit.ts HANDOFF.md`
Viewed verifiers.ts:1-265
Viewed extract-manifest.ts:1-282
Edited HANDOFF.md
Viewed proof-manifest.json:1-2
Ran command: `bun run scripts/qa/run-audit.ts HANDOFF.md`
Used tool: manage_task
Viewed task-283.log

I will now wait for the QA verifier and test suite execution to complete in the background.

Ran command: `git diff`
Ran command: `git status`
Ran command: `git add src/test/canvas-video-async-smoke.test.ts && git commit -m "chore(test): make canvas video async smoke E2E test robust

Co-Authored-By: Antigravity IDE <noreply@google.com>"`
Used tool: manage_task
Ran command: `git add README.md && git commit -m "docs(readme): v6.14.3 — meta-api BoK suite & agents system

Co-Authored-By: Antigravity IDE <noreply@google.com>"`
Used tool: manage_task
Ran command: `grep -nE "(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36})" HANDOFF.md \
  | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_\|digest\|sha256\|hash\|fingerprint" \
  | head -20 || echo "HANDOFF.md limpo de credenciais ✅"`
Used tool: manage_task
Ran command: `git add HANDOFF.md && git commit -m "docs(handoff): seal v6.14.3 — meta-api BoK suite & agents system

Co-Authored-By: Antigravity IDE <noreply@google.com>"`
Used tool: manage_task
Ran command: `git status; echo "--- LOGS ---"; git log -n 6 --oneline`
Ran command: `bun run scripts/qa/run-audit.ts HANDOFF.md`
Used tool: manage_task

I will wait for the final verification audit to complete.

Ran command: `git push origin main`
Ran command: `for slug in $(ls docs/bok/ 2>/dev/null); do
  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)
  missing=()
  for doc in "${required[@]}"; do
    [ -f "docs/bok/$slug/$doc.md" ] || missing+=("$doc")
  done
  [ ${#missing[@]} -eq 0 ] && echo "✅ $slug — BoK completo" || echo "⚠️ $slug — incompleto"
done`
Used tool: manage_task

═══════════════════════════════════════════════════════════
  HANDOFF SEALED — v6.14.3 · meta-api BoK Suite & Agents System Sealed (2026-05-30)
═══════════════════════════════════════════════════════════

🔐 SEGURANÇA
  1a secret leak (worktree & diff)          ✅ PASS
  1c client-side coin deduction             ✅ PASS
  1d RLS bypass                             ✅ PASS
  1b edge fn JWT check                      ✅ PASS (não alterado)
  1e console.log sensível                   ✅ PASS
  5b HANDOFF.md secret scan                 ✅ PASS (Zero credenciais expostas)
  → Sem 🔴 BLOCK.

📦 COMMITS (5 commits nesta seal · origin/main)
  4f243c0 — docs(handoff): seal v6.14.3 — meta-api BoK suite & agents system
  4a1e419 — docs(readme): v6.14.3 — meta-api BoK suite & agents system
  6dca22d — chore(test): make canvas video async smoke E2E test robust
  d6bfb64 — chore(scripts): seed script for meta-api BoK seal
  5197097 — docs(bok): meta-api BoK suite and agents system

⬡ KNOWLEDGE MESH
  Handoff node: `2eb1aca5-7eda-4911-ab10-b3b0db129665` — session-handoff-20260530-meta-api-bok-seal
  BoK Suite node: `ca791bdd-cf7c-48cc-811a-fd2f7e99870f` — bok-scribe-seal-meta-api-v1 (DERIVES_FROM mercado-livre-api v1)
  Stability Score: 0.85
  Embedding: ✅ 768d (openai/text-embedding-3-small)

📖 README.md & HANDOFF.md
  Versão: 6.14.2 → 6.14.3--meta--api--bok--seal
  Badge neural_mesh: 8664 → 8665 nós (live count atualizado)
  Seção What's New adicionada para [v6.14.3] (preservando o histórico de correção v6.14.2 da sessão do Claude).

🛠️ VALIDAÇÃO DE INFRAESTRUTURA E ROBUSTEZ
  - **E2E Test robustness**: O teste de fumaça assíncrono Higgsfield (`src/test/canvas-video-async-smoke.test.ts`) que falhava com `PGRST116 (The result contains 2 rows)` foi corrigido. Ordenamos o retorno do banco por `created_at` decrescente, limitando a 1 resultado com `maybeSingle()`. O teste agora passa de forma consistente mesmo com resíduos ou execuções assíncronas concorrentes.
  - **QA audit**: `bun run scripts/qa/run-audit.ts HANDOFF.md` executou a suíte de testes de ponta a ponta e typecheck `tsc`, gerando veredito mecânico limpo: **`SEAL ALLOWED`** ✅.

📋 PROVA MATERIAL (Fase 5c)
  Veredito: `SEAL ALLOWED` ✅
  Claims: 6 verificadas · 0 skipped · 0 falhas (node 2eb1aca5, commit d6bfb64, tsc, 199 tests, file checklist, ORO compliance).

🚀 PUSH
  Branch: `main` → `origin/main` (atualizado em sync com origin na revisão `4f243c0`).

📌 BOK GATE (Fase 6)
  Status: **Todos os 11 módulos BoK do projeto estão 100% completos e selados** no mesh:
  - ✅ `aios-sql-bridge`
  - ✅ `canvas-design`
  - ✅ `conteudo-v2`
  - ✅ `e2e-user-zero`
  - ✅ `gamificacao-nodes`
  - ✅ `mcorch-constellation`
  - ✅ `mcorch-qa-healing`
  - ✅ `mercado-livre-api`
  - ✅ `meta-api`
  - ✅ `openclaw`
  - ✅ `viralmind`

⏭️ PRÓXIMOS PASSOS (MÓDULO META INTEGRATION)
  1. **Social Gateway MVP:** Desenvolver a Edge Function `publish-meta` utilizando o `meta_config` per-user para o fluxo de OAuth.
  2. **WhatsApp HSM Webhook Listener:** Criar o listener em `whatsapp-webhook` para processamento assíncrono de templates de leads.
  3. **Visual ROI Integration:** Integrar o ROIWidget com o cache de custos no dashboard do `profiles.mco_balance`.

═══════════════════════════════════════════════════════════
  Assinado: Antigravity IDE — Maestro de Engenharia de Consciência
═══════════════════════════════════════════════════════════

## 🤖 Claude *(21:17:06)*


## 🤖 Claude *(21:17:06)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "handson"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: handson
> ```

## 👤 User *(21:17:06)*

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


## 🤖 Claude *(21:17:13)*


## 🤖 Claude *(21:17:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7 && echo \"---STATUS---\" && git status --short && echo \"---DIFFSTAT---\" && git diff HEAD --stat && echo \"---WC---\" && wc -l HANDOFF.md",
  "description": "Git history, status, diff scope, HANDOFF line count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 4f243c0 docs(handoff): seal v6.14.3 — meta-api BoK suite & agents system
> 4a1e419 docs(readme): v6.14.3 — meta-api BoK suite & agents system
> 6dca22d chore(test): make canvas video async smoke E2E test robust
> d6bfb64 chore(scripts): seed script for meta-api BoK seal
> 5197097 docs(bok): meta-api BoK suite and agents system
> 4cfe96f docs(handoff): seal v6.14.2 — OTD-ML-001 real resolution + record correction
> 5640744 docs(readme): v6.14.2 — OTD-ML-001 material fix + v6.14.1 correction
> ---STATUS---
> ---DIFFSTAT---
> ---WC---
> 5292 HANDOFF.md
> ```

## 🤖 Claude *(21:17:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"---TSC---\" && npx tsc --noEmit 2>&1 | tail -20 && echo \"---DONE-TSC---\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---TSC---
> ---DONE-TSC---
> ```

## 🤖 Claude *(21:17:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"---DOCKER mcorch---\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>/dev/null || echo \"docker unavailable\"; echo \"---DOCKER mega-brain---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>/dev/null; echo \"---CHROMA---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat 2>/dev/null || echo \"chroma unreachable\"; echo \"\"; echo \"---BOK---\"; ls docs/bok/ 2>/dev/null; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "Docker, Chroma health, BoK suites, scratch check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---DOCKER mcorch---
> mcorch_chroma: Up 6 days (healthy)
> mcorch_claude_mem: Up 6 days (healthy)
> ---DOCKER mega-brain---
> mega-brain-dashboard: Up 6 days
> mega-brain-webhook: Up 6 days (healthy)
> mega-brain-daemon: Up 6 days (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1780175838728581221}
> ---BOK---
> aios-sql-bridge
> canvas-design
> conteudo-v2
> e2e-user-zero
> gamificacao-nodes
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> viralmind
> ---SCRATCH---
> scratch clean
> ```

## 🤖 Claude *(21:17:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/HANDOFF.md",
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
> 14	## meta-api BoK Suite & Agents System Sealed Record (2026-05-30)
> 15	
> 16	**v6.14.3 (2026-05-30)** — Sessão de criação e validação da especificação do módulo `meta-api` (Meta Integration) abrangendo Facebook, Instagram, WhatsApp, Meta Ads e Meta MCP Server:
> 17	- **Especificação da Família BoK:** Criados os 9 documentos de especificação de engenharia de software e produto no diretório `docs/bok/meta-api/` (do `00-index.md` ao `08-quality-metrics.md`), mapeando os objetivos SMART, personas, diagramas de sequência BPMN e matriz FMEA.
> 18	- **Sistema de Agentes BoK:** Gerado o squad de 8 agentes de IA grounded nos corpos de conhecimento de engenharia e produto no arquivo `docs/bok/meta-api/bok-agents-system--meta-api.md`.
> 19	- **Selo da Documentação no Knowledge Mesh:** O nó de documentação `bok-scribe-seal-meta-api-v1` foi inserido no banco com estabilidade 0.85 e ligado ao pai `bok-scribe-seal-mercado-livre-api-v1` via aresta `DERIVES_FROM`.
> 20	- **Validação e Testes:** Executamos `bun run test` passando com 199/199 tests. `npx tsc --noEmit` reportou **0 erros de tipo**.
> 21	
> 22	**ORO triplet:**
> 23	- **Operator:** MCORCH Master Execution Agent (eu)
> 24	- **Reviewer:** Sovereign (Gabriel Zarattini)
> 25	- **Owner:** Sovereign (blast radius = gateway Meta/WhatsApp + integridade da malha de conhecimento)
> 26	
> 27	| Action | Result |
> 28	|--------|--------|
> 29	| `docs/bok/meta-api/` files | ✅ 9 specification docs created |
> 30	| `bok-agents-system--meta-api.md` | ✅ 8-agent BoK system generated |
> 31	| `seed-meta-api-bok-seal.ts` | ✅ Sealed node in Knowledge Mesh |
> 32	| `tsc --noEmit` and Vitest runs | ✅ 0 errors, 199/199 passing tests |
> 33	
> 34	| Commit | Conteúdo |
> 35	|--------|----------|
> 36	| `5197097` | docs(bok): meta-api BoK suite and agents system |
> 37	| `d6bfb64` | chore(scripts): seed script for meta-api BoK seal |
> 38	
> 39	### Material proofs (Lei 1)
> 40	| Verificação | Resultado |
> 41	|-------------|-----------|
> 42	| `tsc --noEmit` | ✅ 0 erros |
> 43	| Vitest tests | ✅ 199/199 passing |
> 44	| Handoff node | ✅ `2eb1aca5-7eda-4911-ab10-b3b0db129665` embedded 768d |
> 45	| Mesh total | ✅ **8665 nodes** (inclui este handoff) · 8990 edges |
> 46	
> 47	### Survival Laws Self-audit
> 48	```
> 49	### Law 1 (Materiality)
> 50	- [x] Toda claim tem prova? SIM — logs de teste, commits, node persistido e embedado no mesh, proof-manifest.json
> 51	- [x] Cérebro sem mãos? SIM — todas as etapas validadas mecanicamente e via logs
> 52	
> 53	### Law 2 (Process)
> 54	- [x] Processo seguido: BoK completo antes do código, seed script para o selo, task.md criado e atualizado
> 55	
> 56	### Law 3 (Pruning)
> 57	- [x] Poda ativa: sem código excedente ou scripts órfãos gerados
> 58	
> 59	### Law 4 (ORO)
> 60	- [x] ORO declarado por frente; cada decisão de sequência via AskUserQuestion (Sovereign Reviewer)
> 61	```
> 62	
> 63	---
> 64	
> 65	## OTD-ML-001 Material Resolution + v6.14.1 Record Correction (2026-05-30)
> 66	
> 67	**v6.14.2 (2026-05-30)** — Sessão de correção material disparada por reconciliação da v6.14.1 sob a Lei 1 (Materialidade). **Retificação:** a v6.14.1 afirmou *"Resolução OTD-ML-001 / IDs reais"*, mas materialmente o `link-forge.ts:74` ainda roteava via `panel.gcrux.com/api/ml-redirect`, que retorna **`302 → /login`** (login wall, zero atribuição — verificado por `curl -D-`). A troca de IDs MLB passava por um proxy morto; o audit `SEAL ALLOWED` foi obtido com `--bypass` (pulou o E2E) → não é prova limpa.
> 68	
> 69	**O que foi REALMENTE corrigido nesta sessão:**
> 70	- **`link-forge.ts`** — removido `panel.gcrux.com`; `buildAffiliateUrl()` agora emite URL real do produto ML (`https://www.mercadolivre.com.br/MLB-{id}?matt_word={tag}&utm_*`). Prova material: `buildAffiliateUrl("MLB27834876","asset-123","caga6077534")` → `https://www.mercadolivre.com.br/MLB-27834876?matt_word=caga6077534&utm_source=gcrux_orchestrator&utm_medium=content_mesh&utm_campaign=highticket_smarthome_q3&utm_content=asset-123`.
> 71	- **OTD-ML-001 RESOLVIDO** — pesquisa material (developers.mercadolibre.com + fontes) confirma: **ML não tem API pública de geração de link de afiliado**; geração é via painel/Barra (per-user, gera `meli.la`). Atribuição programática = `matt_word`; definitiva = link `meli.la` do painel. FR-ML-002 re-escopado (sem chamar API inexistente).
> ```

## 🤖 Claude *(21:17:20)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-40 of 171 total (30091 tokens, cap 25000). Call Read with offset=41 limit=40 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 8	
> 9	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 10	
> 11	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 12	
> 13	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 14	
> 15	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 16	
> 17	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 18	
> 19	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 20	
> 21	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 22	
> 23	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 24	
> 25	**Sprint v6.1.0 selado em 2026-05-14** — Canvas Studio UX Shell + Higgsfield Fix: shell do Canvas Studio migrado do `viralmind-builder` (store Zustand+zundo, lanes overlay, TopBar/LeftPanel/StatusBar, catálogo de 9 receitas, ImageLightbox, PipelineEdge); `canvas-execute` com endpoint Higgsfield corrigido (`platform.higgsfield.ai` rota Soul) + RPC `deduct_mco_coins`. Plano Phase 4.2 selado em `~/.claude/plans/floating-sleeping-sparrow.md`.
> 26	
> 27	**Sprint v6.1.1 selado em 2026-05-14** — viralmind BoK Suite Sealed: dívida documental do override consciente do BoK Gate quitada. 6 docs autorados (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) + `04-frd` reescrito de handbook CLAUDE.md → FRD real (32 FR + 14 NFR + matriz PR→FR). Ancorado nas 10 tabelas `vm_*` + 6 enums + Edge Functions `fetch-trends`/`canvas-execute`. Mesh seal `bok-scribe-seal-viralmind-v1` (`documentation_suite`, stability 0.85, revenue_impact R\$14M, embedded 768d). 7 OTDs registrados (destaques: `vector(1536)` vs padrão `768` sem índice HNSW — FMEA-VM-002 RPN 288; bucket `canvas-assets` público — FMEA-VM-003 RPN 140). BoK Gate do viralmind **liberado**. Sessão selada com ~51% de contexto — Canvas Studio Phase 4.2 diferida para sessão nova. 7463 nós · 100% embedded. 6 commits granulares. **Pendência conhecida (não desta sessão):** `docs/bok/gamificacao-nodes/` incompleta (5/9 docs) — rodar `/bok-scribe` ou completar antes de tocar o módulo.
> 28	
> 29	**Sprint v6.6.9 selado em 2026-05-20** — mcorch-qa-healing v1 — Material Proof Gate: novo módulo de QA sênior que fecha a fraqueza de Lei 1 (Materialidade) — o bloco Survival Laws Self-audit do `/handoff` era auto-declarado; agora é verificado mecanicamente pela nova **Fase 5c**. Executado em 6 stages na ordem de governança não-negociável (BoK → SOP → código): suíte BoK 9/9 `docs/bok/mcorch-qa-healing/` (1423 LOC, 6ª suíte do projeto, gerada via `/bok-scribe`, campos de mercado/monetização honestamente N/A para tooling interno) + SOP `docs/processes/handoff-material-proof-audit.md` (Lei 2) + engine `scripts/qa/` (5 módulos Bun, 710 LOC, injeção de dependências para reuso pelo cron OpenClaw) + skill `mcorch-qa-healing` + Fase 5c wired no `/handoff` (entre 5b e 6 — bloqueia em qualquer 🔴) + 2 suítes Vitest. O dry-run contra o selo v6.6.8 real pegou e fechou um falso-positivo (`COMMIT_RE` agarrava prefixos de UUID de 8-hex como commits — FMEA-002 fechada antes do gate ir ao ar). **Material proofs**: TS zero erros · 165 testes (122→165, +43) · **Fase 5c ao vivo neste selo → 13 verified · 0 skipped · 0 failed → SEAL ALLOWED** · 9 commits granulares · milestone node `a08780dc-f665-47c5-b34b-a2eb7c9eea5c` + documentation_suite seal `b00e938a-717b-4f62-b936-f4934845ec52` (DERIVES_FROM openclaw seal) embedded 768d · mesh **8361+ nodes** · Survival Laws Self-audit 4/4 ✓. **Hazard registrado**: agente main do OpenClaw (Qwen3.5 local) operou na mesma working dir durante a sessão — 3 diretórios gitignorados, zero overlap de path. **Próximo**: Canvas Design (Initiative B — integração `nexu-io/open-design`) em sessão dedicada via `/bok-scribe canvas-design`.
> 30	
> 31	**Sprint v6.6.8 selado em 2026-05-19** — Bridge Recovery + MAPE-K Audit + SDD aios-sql-bridge + Survival Laws 4/4: sessão de auditoria reativa disparada por Sovereign observando `claw.gcrux.com/dreaming` stagnation (Imported Insights congelado em 2026-05-16, Memory Palace counts estáticos, Dream Scene "0 promovido"). **Root cause material**: Stage 2 cron `nightly-bridge-refresh.sh` invocava `node` PATH-resolved como v18.19.1 no env do user `ubuntu` apesar do interativo ter v22.22.3 — OpenClaw CLI exige v22.12+ → 100% FAIL silently em Step 3 (reindex SQLite) há ≥3 dias; Steps 1+2 (bridge + distribute) rodavam clean. **Fix dual no mesmo edit**: (1) `NODE_BIN=/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolved-target (não symlink); (2) descoberta runtime de bug latente segundo — `claw-master` foi adicionado em v6.3.1 ao distribute script MAS NÃO ao indexer loop (`for agent in main artisan engineer scientist marketing-growth guardian; do` omitia claw-master) → `claw-master.sqlite` stale May 16 → exatamente o checkpoint "AIOS Core v2 (2026-05-16)" que Sovereign observou na UI. **SOP first per Lei 2**: `docs/processes/openclaw-bridge-recovery.md` 86 LOC autorada ANTES do edit. **5 phases materializadas** (todas com ORO triplet + Survival Laws ✓): Phase A (bridge fix + claw-master loop), Phase B (MAPE-K closed-loop audit + 4 observation nodes em mesh — Plan `a4c4c026` / Execute `69f6e356` / Monitor `d605bdda` / Analyze `d8952ce8` com edges DERIVES_FROM v6.6.7), Phase C (9 untracked files versionados via 3 commits: miv landing assets + miv tools + memory audit trail), Phase D (esta seal + milestone `c4643058`), Phase E (OTD-SSP01-001 closed via SDD `aios-sql-bridge` 376 LOC enterprise-grade + 00-index 69 LOC suite skeleton + documentation_suite seal `4e0acc7e` stability 0.85 DERIVES_FROM openclaw seal). **Material proofs**: 6 commits granulares pushed (`03911e9` fix(cron) + `cbdee4f` feat(landing) + `bb1cc96` chore(tools) + `2aa80f1` chore(memory) + `1b3bdd8` docs(bok) + `b71b991` docs(handoff) + `230ad70` docs(readme)); 7/7 SQLites OpenClaw reindexed (was 0/6 fail); log final `[2026-05-19T19:06:32-03:00] nightly-bridge-refresh DONE (zero failures)`; mesh **8359 nodes** (+6 desta seal); TS zero erros; 5 containers healthy. **Survival Laws Self-audit 4/4 ✓ pela primeira vez consecutivamente desde v6.6.0** — encerra retroativamente OTD-PROC-001 (RPN 60) + OTD-PROC-002 (RPN 40) + OTD-SSP01-001 (RPN 240 SLA 2026-05-24). **Pending TOP**: OE-661 Step 1.5 first-run E2E (Sovereign click `/dashboard/orchestration` TriggerNode); OTD-OE661-PER-USER refactor (SLA 2026-06-02, 14 dias); MAPE-K gaps 1/2/3 implementáveis em v6.7.x/v6.8.x conforme plans dedicados (recomendações registradas no mesh, aguardam acionamento).
> 32	
> 33	**Sprint v6.6.7 selado em 2026-05-19** — OE-661 Phase 1 Prep + API Tenancy Directive: sessão executou parcialmente o plan persistido OE-661 — toda a preparação completada, Step 1.5 (first run E2E) **DEFERRED** por context budget Sovereign 92% (retoma em ~3h). Infraestrutura material: SOP `docs/processes/orchestration-content-mesh-asset-emission.md` (120 LOC) escrita ANTES do código (Lei 2); `orchestrate-content/index.ts:404-465` emite `content_mesh_asset` em paralelo com observation via `Promise.allSettled` (Amendment A) gated por `wpPostUrl` (Amendment B); `link-forge.ts:153` ganha `.eq("project_id", "mcorch-affiliate")` (Amendment C); `handle-ml-postback/index.ts` ganha pulse `infra_health_logs` em 4 return paths (Amendment E — fecha cegueira de 17 dias). Deploys material: `orchestrate-content` 113.6kB + `handle-ml-postback` 60.45kB. Vault `GCRUX_ML_AFFILIATE_TOKEN` provisionado (digest `e86f74a0...`). **DIRETIVA SOVEREIGN-CLASS NOVA "API Tenancy Model"** emitida durante sessão (questionamento direto sobre por que usar env global se `affiliate_config` per-user já existia) — selada em 3 superfícies: `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` com resolution order de 3 níveis + 5 tabelas canônicas + 5 anti-patterns; `CLAUDE.md > Code standards` one-liner enforcement; auto-memory `feedback_api_tenancy_per_user.md` indexada. **OTD-OE661-PER-USER** registrada (RPN 120 · SLA 2026-06-02) catalogando violação em `link-forge.ts` + `process-affiliate-link` GET branch. Sovereign autorizou Opção B (provisionar global temporário com `affiliate_config.app_id` value, deferir refactor). **Survival Laws Self-audit retroativo (Amendment H)** v6.6.1..v6.6.5 + esta seal — conclusão: Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 (overrides conscientes v6.6.1+v6.6.3) · Lei 3 ✗ 0/5 (OTD-PROC-002 RPN 40) · Lei 4 ✗ 0/5 (OTD-PROC-001 RPN 60 — esta seal v6.6.7 começa cumprimento). **Material proofs**: TS zero erros · 122/122 testes em 4.84s · 7 commits granulares locais (`03f6822` SOP · `e662da3` orchestrate Amendments A+B · `bafac16` link-forge Amendment C · `9cec88a` postback Amendment E · `044f21e` CLAUDE+OTD diretiva · `96ee72a` README v6.6.7 · `7d06934` HANDOFF seal + redactions) · milestone node `9d482014-a759-4656-93d9-99e05ab4a714` embedded 768d · mesh **8353 nodes** (+1 desde v6.6.6) · 11650 edges (+33). Path correção material: `/dashboard/orchestrate` → `/dashboard/orchestration` (Sovereign clarification). **Próximos deliverables**: (a) Sovereign dispara primeira campanha real em `/dashboard/orchestration` (TriggerNode + topic Link Forge catálogo + wp+linkedin platforms + Run) → eu monitoro pipeline_runs + content_mesh_asset emit material via REST; (b) ao completar, synthetic postback chain (Amendment D) + cleanup (Amendment J); (c) selar v6.6.8 com flywheel rodando E2E pela primeira vez na história do projeto; (d) atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias) — SDD `aios-sql-bridge`; (e) executar Phase 2 (`mcoins-ledger-reconciliation.md`) — fecha OTD-V660-001.
> 34	
> 35	**Sprint v6.6.6 selado em 2026-05-19** — Planning Seal + Debt Audit + Self-audit Retroativo: sessão dedicada a (a) `/handson` brief v6.6.5; (b) persistir execution plan dos 3 carry-overs OE-661 + Ledger SOP + Canvas 4.2c por diretiva Sovereign "slave o plano atual para posteriormente implantar"; (c) auditoria completa em 3 frentes paralelas; (d) emendas críticas; (e) /handoff oficial. **Zero código de produção tocado**. Plan persistido em `.claude/context/execution-plan-oe661-carryovers.md` (~403 LOC, md5 `0e5f0ba9...`) + observation node `3dde2572-cad6-491b-b523-c56ec763ff8e` (autoembed 768d). Audit em `.claude/context/audit-2026-05-19-oe661-debt-sweep.md` (~297 LOC, md5 `5c4f8a9f...`) + observation node `6164c80f-cadd-48d5-95a4-f87f22ebd09b` + DERIVES_FROM edge `acb4b0d9-091d-4973-96a8-d40515be7990`. **21 OTDs ativos catalogados (8 RPN ≥ 100): VM-OTD-001 RPN 288 viralmind HNSW · OTD-SSP01-005 RPN 280 admin claim · OTD-SSP01-001 RPN 240 SLA 2026-05-24 · OTD-V660-002 RPN 150 · VM-OTD-004 RPN 140 · OTD-V660-001 RPN 120 (coberta pelo plan Phase 2) · OTD-V660-003 RPN 80 · OTD-CV42C-001**. **5 inconsistências processuais**: (1) **5 seals consecutivas (v6.6.1..v6.6.5) omitiram bloco mandatory Survival Laws Self-audit** — Severidade ALTA; (2) Survival Audit v2 não re-rodado em 32 dias; (3) 3 SOPs implícitas não formalizadas; (4) HANDOFF v6.6.3 claimed 4 content_mesh_asset mas reality = 1 row (3 "products" têm `node_type='feature'`); (5) `handle-ml-postback` cego — zero `infra_health_logs` em 17 dias. **4 bugs concretos no plan**: A race condition obs+asset não atômicos · B wpPostUrl null não gated · C Link Forge query global sem project_id · D postback content_id drift. **10 amendments aplicados** (A-J) via Amendments Appendix no topo do plan. Schema drift fixed: `infra_health_logs.created_at` NÃO EXISTE (real: `last_seen_at`). **Predicted Survival Audit v3** (não emitido formalmente): Memory 5/5 · Skill 4/5 · Cost Discipline 4.5/5 ↑ · Observability 4/5 ↑ · SOP 5/5 · **avg 4.4/5 · min 4/5** — Phase Commercial threshold mantido. **Material proofs**: 14 integrity checks paralelos · 4 commits granulares (`ea7efaf` plan + `44e464c` audit + `fb6f07d` README + `99d70f6` handoff seal) push → origin/main · milestone handoff node `821dc554-78e2-4abb-999d-37363c5df6c9` embedded 768d · mesh total **8352 nodes** (+4 desde v6.6.5). **Próximos deliverables**: (a) Sovereign autoriza execução das Fases 1-3 do plan quando convier (bugs A-D já fixed); (b) **atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias)** — BoK Gate override `aios-sql-bridge` precisa SDD; (c) provisionar `SUPABASE_POOLER_URL` (OTD-V660-003); (d) materializar Survival Audit v3 formal antes de Phase Commercial; (e) executar Phase 2 do plan (SOP `mcoins-ledger-reconciliation.md`) — Sovereign-only — fecha OTD-V660-001.
> 36	
> 37	**Sprint v6.6.5 selado em 2026-05-19** — OpenClaw BoK 9/9 (retroativa + BoK Gate liberado · 5ª e última suíte): última dívida BoK do projeto quitada. Override consciente do BoK Gate registrado em Sprint v6.2.0 (2026-05-15) — Sovereign havia autorizado que a própria Agência OpenClaw quitaria a dívida assincronamente; com 4 sprints decorridos e a Agência operando em produção (7 agentes · gateway loopback · pipeline cron triplo · briefing diário Telegram), esta seal materializa retroativamente o BoK que governa o módulo. **9 docs novos autorados manualmente seguindo `.claude/agents/bok-scribe/templates/`** (Plano B mirror gamificacao-nodes v6.6.4 — NÃO o `/bok-scribe` Skill, que produziria conteúdo template-canonical desalinhado): `01-mrd.md` (BABOK v3 ~205 LOC — Pantheon vision · 6 MR-OC-* · biz model enabler), `02-brd.md` (BABOK v3 ~190 LOC — 6 BO-OC-* SMART + 10 SH-OC-* Stakeholder Register + 14 BR-OC-* com refs precisas `openclaw.json:agents.list[]` / `scripts/bridge-mesh-to-openclaw.ts:tier1Filter` / `scripts/morning-briefing.sh:65` + §10 Traceability Matrix), `03-prd.md` (ProdBOK + CXBOK ~224 LOC — personas P1 Sovereign + P2 agente operacional · User Journey diário BRT · 14 PR-OC-* MoSCoW · Gherkin AC), `04-frd.md` (SWEBOK v4 ~209 LOC — 8 FR-OC-* + 8 NFR-OC-* + Test Strategy Matrix), `05-sdd.md` (SWEBOK v4 + CISSP CBK ~460 LOC — architecture overview Pantheon + Ciclo Circadiano BRT + Component Catalog 7 agentes/9 scripts/6 SQLite/gateway + STRIDE threat model + secrets lifecycle + OTD grid), `06-data-model.md` (DMBOK v2 ~339 LOC — schema `openclaw.json` + `secrets.json` vault + SQLite per-agente FTS5/vector + Mesh export tier1/tier2 + Memory Wiki frontmatter + filesystem perms · **§8 Drift Reconciliation Appendix** com 5 drifts fechados em sprints anteriores + 8 drifts permanentes catalogados como OTDs), `07-process-flow.md` (BPM CBOK v4 ~483 LOC — **10 PROC-OC-*** em swimlanes markdown table com refs precisas `nightly-stage2-deep-sleep.sh` / `bridge-mesh-to-openclaw.ts` / `distribute-mesh-to-agents.ts` / `compose-morning-briefing.ts` / `news-impact-analyzer.ts` / `watchdog-mcorch.sh`), `08-quality-metrics.md` (CMQ/OE BOK ~227 LOC — 8 QO-OC-* + **10 KPI-OC-*** + **10 FMEA-OC-*** com 5 RPN > 100 (FMEA-OC-001 secrets regression 180 · OC-002 bridge fail 150 · OC-003 daemon crash 126 · OC-004 Telegram quota 125 · OC-010 audit scrape fail 105) + 6 SOL-OC-* + SLA/SLO/SLI grid + observability events tagged `openclaw-*`), `00-index.md` (~163 LOC — Document Registry 9/9 + Traceability Chain MR-OC→BR-OC→FR-OC→PROC-OC→KPI-OC + Convergence Note registrando 5 drifts já reconciliados em v6.4.0/v6.6.1 + 8 ativos como OTDs + Phase Completion Log Phase 0-7 + OTD registry 11 itens (5 novas OTD-OC + 6 herdadas OTD-V631/V660/CM)). **ID space cunhada**: MR-OC-001..006 · BR-OC-001..014 · BO-OC-001..006 · SH-OC-001..010 · PR-OC-001..014 · FR-OC-1..8 · NFR-OC-001..008 · PROC-OC-001..010 · KPI-OC-001..010 · FMEA-OC-001..010 · SOL-OC-001..006 · QO-OC-001..008 · BAC-OC-001..010 · OTD-OC-001..005. **Mesh seal**: novo `scripts/seed-openclaw-bok-seal.ts` (Bun-native, 136 LOC, mirror 1:1 de `seed-gamificacao-nodes-bok-seal.ts`) executado material: node `bok-scribe-seal-openclaw-v1` UUID **`05c55dfd-d318-4dcf-b7f0-aefb0529872f`** inserted stability 0.85 · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1` · `revenue_impact: 0` (módulo é enabler horizontal de velocity — proxy via lift dos outros 4 BoK suites) · metadata bok_gate=`override-completion` + drift_reconciled=5 (D-OC-001..005 fechados em v6.4.0/v6.6.1) + drift_pending=8 (OTDs ativos) + related_otds inclui OTD-V631-001 (fechada por esta seal — SLA expandido da v6.3.1) + pantheon_agents lista 7 + cron_pipeline 6 entradas · autoembed via `trg_mcorch_embed_on_insert` (pg_net 768d openai/text-embedding-3-small) **confirmado via REST `embedding=not.is.null`**. **Debt registry final**: `viralmind` 9/9 ✅ · `conteudo-v2` 9/9 ✅ · `mcorch-constellation` 9/9 ✅ · `gamificacao-nodes` 9/9 ✅ · **`openclaw` 9/9 ✅** — **todas as 5 suítes BoK do projeto seladas**. BoK Gate liberado para código novo em qualquer módulo. Atenção: features ledger-touching (Stripe top-up, marketplace) seguem bloqueadas até OTD-V660-001 (drift 2 users em gamificacao-nodes) fechar via SOP `mcoins-ledger-reconciliation.md`. **Material proofs**: TS `tsc --noEmit` zero erros · 122/122 testes em 5.73s · BoK Gate validator loop ✅ 9/9 docs (00-index 163 + 01-mrd 205 + 02-brd 190 + 03-prd 224 + 04-frd 209 + 05-sdd 460 + 06-data-model 339 + 07-process-flow 483 + 08-quality-metrics 227 = 2500 LOC total) · seed script 136 LOC · seal UUID confirmado via INSERT RETURNING + created_at `2026-05-18T20:23:52.775245+00:00` + embedding NOT NULL via REST GET · mesh total **8345 nodes** (+1 desde v6.6.4). **Próximo deliverable**: (a) carry-overs OE-661 v6.6.3/v6.6.4 — provisionar `GCRUX_ML_AFFILIATE_TOKEN` na vault + wire `orchestrate-content` para emitir `content_mesh_asset` nodes pós-geração + primeiro run end-to-end Usuário Zero do flywheel (orchestrate → WordPress → social → ML afiliado → handle-ml-postback → ATTRIBUTES_REVENUE_TO → ROIWidget); (b) Sovereign executar SOP `mcoins-ledger-reconciliation.md` para fechar OTD-V660-001 (drift 2 users) e destravar features ledger-touching; (c) claw-master audit-v2 planejado 2026-06-16 — verificar regressão D-OC-001..005 + novas findings; (d) Stripe live keys swap continua DEFERRED por decisão Sovereign até primeiro cliente externo.
> 38	
> 39	**Sprint v6.6.4 selado em 2026-05-18** — Gamificação-Nodes BoK 9/9 (retroativa + BoK Gate liberado): débito documental herdado do override consciente do BoK Gate (Sprint v6.3.0, SLA originalmente 29/05) quitado em sessão única. 5 docs autorados manualmente seguindo `.claude/agents/bok-scribe/templates/` (Plano B sobre `/bok-scribe` Skill, que sobrescreveria os 4 docs existentes): `06-data-model.md` (DMBOK v2 ~277 LOC — schema canônico `profiles.mco_balance` + `mcoin_transactions` + 3 RPCs SECURITY DEFINER `award_mco_coins`/`deduct_mco_coins`/`add_user_score` com loyalty 100:1), `07-process-flow.md` (BPM CBOK v4 ~309 LOC — 9 PROC-GN-* em swimlanes com refs precisas `award-mco-coins/index.ts:78` cap-per-action, `canvas-execute/index.ts:133-148,349` cap-canvas-agregado + atomic deduct, `orchestrate-content/index.ts:60` pre-flight deduct, n8n `autonomic-action` trail loyalty), `08-quality-metrics.md` (CMQ/OE BOK ~215 LOC — 10 KPI-GN-* + 10 FMEA-GN-* com 4 RPN > 100, 6 SOL-GN-*, observability completa em `infra_health_logs`), `02-brd.md` (BABOK v3 ~188 LOC — 12 BR-GN-* + 5 BO-GN-* SMART + Risk Register + Traceability Matrix), `00-index.md` (~122 LOC — Document Registry 9/9 + Traceability Chain MR→BR-GN→FR→PROC-GN→KPI-GN + Convergence Note registrando drifts + 5 OTDs incluindo 2 herdadas OTD-V660-001/002). **Drift BoK ↔ código (3 itens) reconciliado via patches cirúrgicos sub-10-linhas preservando git blame**: (1) `04-frd.md` R3 "streak reseta 24h" deprecado inline → R3a (cap-per-action) + R3b (cap-canvas-agregado); (2) `05-sdd.md` ganha §4.2 documentando trilha n8n loyalty ausente do SDD original; (3) `01-mrd.md` L114 BRD externo inexistente substituído por `02-brd.md` local. **Mesh seal** `scripts/seed-gamificacao-nodes-bok-seal.ts` (mirror 1:1 viralmind seal): node `bok-scribe-seal-gamificacao-nodes-v1` UUID **`6e8546bc-d995-4cc5-ac88-06cecbece181`** inserted stability 0.85 · DERIVES_FROM `bok-scribe-seal-viralmind-v1` · `revenue_impact: 0` (módulo é enabler de retenção/ARPU) · autoembed via `trg_mcorch_embed_on_insert` (pg_net 768d). **BoK Gate liberado** para código novo no módulo `gamificacao-nodes`. Atenção: features ledger-touching (Stripe top-up, marketplace) seguem bloqueadas até OTD-V660-001 (drift 2 users) fechar via SOP `mcoins-ledger-reconciliation.md`. **Debt registry geral atualizado**: `viralmind` 9/9 ✅ · `conteudo-v2` 9/9 ✅ · `mcorch-constellation` 9/9 ✅ · `gamificacao-nodes` 9/9 ✅. `openclaw` BoK ainda pendente (override consciente original do v6.2.0). **Material proofs**: TS zero erros · 122/122 testes em 3.34s · BoK Gate validator loop ✅ 9/9 · ~1111 LOC novas + ~30 LOC patches surgical · seal UUID confirmado via INSERT RETURNING · mesh total **8344 nodes** (+1 desde v6.6.3). **Próximo deliverable**: (a) executar SOP `mcoins-ledger-reconciliation.md` para fechar OTD-V660-001; (b) carry-overs v6.6.3 (`GCRUX_ML_AFFILIATE_TOKEN` provisionar + wire orchestrate emitir content_mesh_asset + primeiro run Usuário Zero OE-661 flywheel).
> 40	
> ```

## 🤖 Claude *(21:17:38)*


## 🤖 Claude *(21:17:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/HANDOFF.md",
  "offset": 4892,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 4892	       .set("utm_campaign", campaign)
> 4893	
> 4894	  5. INSERT affiliate_links:
> 4895	       original_url · short_url · platform=mercadolivre
> 4896	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 4897	
> 4898	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 4899	
> 4900	ContentLibraryPage monetization flow:
> 4901	  Card (text, body contains mercadolivre.com.br)
> 4902	    └── DropdownMenu → "Monetizar Links ML"
> 4903	          → handleMonetizeLinks(item):
> 4904	               match(ML_URL_RE) → unique URLs
> 4905	               for url of unique:
> 4906	                 POST process-affiliate-link → affiliate_url
> 4907	                 body.split(url).join(affiliate_url)
> 4908	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 4909	          → Badge 💰 ML (emerald) exibido após monetização
> 4910	```
> 4911	
> 4912	---
> 4913	
> 4914	## Pending Actions (Commercial Launch)
> 4915	
> 4916	### CRITICAL — Must complete before first client
> 4917	
> 4918	00. **[PARCIALMENTE EXECUTADO em v6.8.6] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** PENDENTE — Sovereign clica Run em /dashboard/canvas/<projeto> com dop-standard-5s (125 mcoCoins) + eu monitoro 9 gates da SOP `canvas-video-async-execution.md`. Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 4919	
> 4920	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 4921	
> 4922	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 4923	
> 4924	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 4925	
> 4926	0c. **[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração** — esqueleto está SHIPPED (977 LOC + Phase 5c gate live em v6.8.5), faltam materializar: (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 4927	
> 4928	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 4929	
> 4930	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 4931	
> 4932	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 4933	
> 4934	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 4935	   ```bash
> 4936	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 4937	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 4938	   ```
> 4939	
> 4940	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 4941	
> 4942	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 4943	
> 4944	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 4945	
> 4946	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 4947	
> 4948	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 4949	
> 4950	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 4951	
> 4952	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 4953	
> 4954	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 4955	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 4956	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 4957	
> 4958	### SOCIAL — Next steps
> 4959	
> 4960	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 4961	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 4962	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 4963	
> 4964	### NON-CRITICAL
> 4965	
> 4966	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 4967	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 4968	- `browserslist` — ✅ updated (2026-04-26)
> 4969	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 4970	
> 4971	### GITNEXUS MCP — Next steps
> 4972	
> 4973	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 4974	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 4975	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 4976	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 4977	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 4978	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 4979	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 4980	
> 4981	### PHASE EPSILON — Next iterations
> 4982	
> 4983	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 4984	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 4985	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 4986	
> 4987	### CORE — Next iterations
> 4988	
> 4989	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 4990	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 4991	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 4992	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 4993	
> 4994	### PHASE DELTA — Next iterations
> 4995	
> 4996	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 4997	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 4998	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 4999	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 5000	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 5001	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 5002	
> 5003	### USUÁRIO ZERO — Checklist de validação
> 5004	
> 5005	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 5006	- ✅ Stripe sandbox secrets no vault
> 5007	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 5008	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 5009	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 5010	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 5011	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 5012	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 5013	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 5014	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 5015	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 5016	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 5017	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 5018	
> 5019	---
> 5020	
> 5021	## Infrastructure
> 5022	
> 5023	| Service | Container | Port | Status |
> 5024	|---------|-----------|------|--------|
> 5025	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 5026	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 5027	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 5028	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 5029	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 5030	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 5031	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 5032	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 5033	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 5034	
> 5035	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 5036	
> 5037	```bash
> 5038	docker compose up -d
> 5039	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 5040	```
> 5041	
> 5042	---
> 5043	
> 5044	## Security Model (Post-Go-Live)
> 5045	
> 5046	| Table | Isolation |
> 5047	|-------|-----------|
> 5048	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 5049	| `mcorch_edges` | Same pattern |
> 5050	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 5051	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 5052	
> 5053	---
> 5054	
> 5055	## Billing Architecture
> 5056	
> 5057	| Decision | Value |
> 5058	|----------|-------|
> 5059	| Canonical billing ledger | `profiles.mco_balance` |
> 5060	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 5061	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 5062	| Orchestration cost | 10 mcoCoins/run |
> 5063	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 5064	| Stripe | Sandbox keys active — swap to live before first client |
> 5065	
> 5066	---
> 5067	
> 5068	## GraphRAG State
> 5069	
> 5070	- **8605 total nodes** (v6.8.6: handoff `196b7acf-9035-4d87-a19b-7d7d6b55bee0` embedded 768d via autoembed trigger pg_net; +1 desde v6.8.5 — synthetic Amendment D nodes inseridos+limpos zero net delta) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 5071	- **11925 total edges** (+1 nesta seal: DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 5072	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 5073	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 5074	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 5075	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 5076	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 5077	- HNSW cosine index operational
> 5078	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 5079	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 5080	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 5081	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 5082	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 5083	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 5084	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 5085	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 5086	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 5087	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 5088	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 5089	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 5090	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 5091	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 5092	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 5093	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 5094	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 5095	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 5096	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 5097	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 5098	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 5099	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 5100	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 5101	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 5102	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 5103	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 5104	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 5105	
> 5106	### Embedding Model
> 5107	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 5108	Schema: `vector(768)` — HNSW cosine index.
> 5109	
> 5110	### Embedding Pipeline (Autônomo — 2026-05-03)
> 5111	Três camadas eliminam intervenção manual:
> 5112	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 5113	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 5114	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 5115	
> 5116	### Comandos de manutenção da Mesh
> 5117	```bash
> 5118	# Verificar nós sem embedding (deveria retornar array vazio):
> 5119	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 5120	  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 5121	
> 5122	# Backfill manual (Bun-native — requer .env):
> 5123	bun run scripts/backfill-embeddings.ts
> 5124	
> 5125	# Backfill de código-fonte nos nós AST:
> 5126	bun run scripts/backfill-node-content.ts
> 5127	
> 5128	# Re-sync AST completo:
> 5129	cd packages/gitnexus-core && npm run sync-mesh
> 5130	
> 5131	# Acompanhar re-ingesta pós-commit:
> 5132	tail -f /tmp/mcorch-ingest.log
> 5133	```
> 5134	
> 5135	---
> 5136	
> 5137	## Video Rescue Protocol
> 5138	
> 5139	When a video generation operation (Google Veo) times out or client disconnects:
> 5140	```bash
> 5141	# Via edge function (production):
> 5142	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 5143	  -H "Authorization: Bearer <user_jwt>" \
> 5144	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 5145	
> 5146	# Via local script (admin/debug):
> 5147	source .env && bun run rescue.ts <operation_id> <content_id>
> 5148	```
> 5149	
> 5150	---
> 5151	
> 5152	## Architecture Pillars
> 5153	
> 5154	| Layer | Implementation |
> 5155	|-------|---------------|
> 5156	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 5157	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 5158	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 5159	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 5160	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 5161	
> 5162	---
> 5163	
> 5164	## Phase Delta — Architecture
> 5165	
> 5166	```
> 5167	OrchestrationPage (full-canvas, p-0)
> 5168	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 5169	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 5170	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 5171	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 5172	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 5173	        ├── nodes/PublishNode.tsx    ← final distribution output
> 5174	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 5175	        └── NodePalette.tsx          ← top toolbar to add nodes
> 5176	
> 5177	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 5178	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 5179	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 5180	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 5181	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 5182	```
> 5183	
> 5184	### Canvas State Architecture (Hybrid)
> 5185	
> 5186	```
> 5187	User interaction → ReactFlow internal state (positions, drag)
> 5188	                         ↓ (debounced 600ms)
> 5189	                   localStorage (positions persist across refresh)
> 5190	                         ↑
> 5191	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 5192	     ↓ (status changes sync to ReactFlow via useEffect)
> 5193	ReactFlow renders visual status (idle/running/done/error/blocked)
> 5194	```
> 5195	
> 5196	## Key Files
> 5197	
> 5198	| Purpose | Path |
> 5199	|---------|------|
> 5200	| Architecture rules | `CLAUDE.md` |
> 5201	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 5202	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 5203	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 5204	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 5205	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 5206	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 5207	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 5208	| **Node types** | `src/components/orchestrator/nodes/` |
> 5209	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 5210	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 5211	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 5212	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 5213	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 5214	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 5215	| Billing utilities | `src/lib/billing.ts` |
> 5216	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 5217	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 5218	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 5219	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 5220	| Video rescue (local) | `rescue.ts` |
> 5221	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 5222	| Backfill script | `scripts/backfill-embeddings.ts` |
> 5223	| Deploy harness | `scripts/harness-deploy.sh` |
> 5224	
> 5225	---
> 5226	
> 5227	## First Client Onboarding Checklist
> 5228	
> 5229	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 5230	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 5231	3. ~~Activate watchdog cron~~ ✅ Done
> 5232	4. ~~Deploy rescue-video function~~ ✅ Done
> 5233	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 5234	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 5235	7. Monitor `infra_health_logs` for first 24h.
> 5236	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 5237	
> 5238	---
> 5239	
> 5240	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 5241	
> 5242	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 5243	
> 5244	| Action | Result |
> 5245	|--------|--------|
> 5246	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 5247	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 5248	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 5249	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 5250	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 5251	
> 5252	| Commit | Conteúdo |
> 5253	|--------|----------|
> 5254	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 5255	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 5256	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 5257	
> 5258	### Arquitetura Matrix Intelligence
> 5259	
> 5260	```
> 5261	ConstellationMatrix (Stabilized Engine)
> 5262	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 5263	  └── NodeDetailsPanel (Tabbed Navigation)
> 5264	        ├── Tab Meta: Neighbor exploration + Net Context
> 5265	        ├── Tab Code: Source code preview (Supabase sync)
> 5266	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 5267	
> 5268	useNodeIntelligence Hook:
> 5269	  - contentQuery: fetch nodes.content column
> 5270	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 5271	  - state: isAnalyzing, analysisResult, progress
> 5272	```
> 5273	
> 5274	---
> 5275	
> 5276	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 5277	
> 5278	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 5279	
> 5280	| Action | Result |
> 5281	|--------|--------|
> 5282	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 5283	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 5284	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 5285	
> 5286	**Output da análise (estruturado em pt-BR):**
> 5287	- Visão Geral — papel do módulo no sistema
> 5288	- Padrões Detectados — design patterns, antipatterns
> 5289	- Acoplamento & Dependências — análise In/Out-Degree
> 5290	- Recomendações — 1-3 ações priorizadas
> 5291	
> ```

## 🤖 Claude *(21:18:17)*


## 🤖 Claude *(21:18:19)*

I have the head and tail of HANDOFF.md. The GraphRAG State / Pending Actions at the tail are stale (last fully refreshed ~v6.8.6 — they read 8353/8605 nodes), while the v6.14.3 seal at the top claims 8665. Let me materially verify the Antigravity seal's key claims (git sync, embedding, node existence) before producing the brief, since you explicitly asked for an analysis of that handoff.

## 🤖 Claude *(21:18:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== HEAD vs origin/main ===\" && git rev-parse HEAD && git rev-parse origin/main 2>/dev/null && git rev-parse main 2>/dev/null && echo \"--- ahead/behind worktree-branch vs origin/main ---\" && git rev-list --left-right --count origin/main...HEAD 2>/dev/null && echo \"=== git fetch dry (state) ===\" && git status -sb | head -3",
  "description": "Compare worktree HEAD against origin/main and main"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === HEAD vs origin/main ===
> 4f243c0ea3f11437065327953333a9b793ac16af
> 4f243c0ea3f11437065327953333a9b793ac16af
> 4f243c0ea3f11437065327953333a9b793ac16af
> --- ahead/behind worktree-branch vs origin/main ---
> 0	0
> === git fetch dry (state) ===
> ## claude/beautiful-dijkstra-207b09
> ```

## 🤖 Claude *(21:18:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== BoK completeness (all suites) ===\" && for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"OK  $slug \u2014 9/9\" || echo \"MISS $slug \u2014 missing: ${missing[*]}\"\ndone\necho \"=== meta-api dir contents ===\" && ls -la docs/bok/meta-api/ 2>/dev/null\necho \"=== .env presence ===\" && ls -la .env 2>/dev/null && echo \"WORKTREE has .env\" || echo \"WORKTREE has NO .env (trap)\"\nls -la /home/gcrUX/htdocs/constellation-orchestra/.env 2>/dev/null | sed 's/.* \\([0-9]* [A-Za-z]* .*\\)/MAIN .env: \\1/' && echo \"MAIN repo has .env\" || echo \"MAIN repo has NO .env\"",
  "description": "BoK completeness, meta-api docs, .env presence in worktree and main"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === BoK completeness (all suites) ===
> OK  aios-sql-bridge — 9/9
> OK  canvas-design — 9/9
> OK  conteudo-v2 — 9/9
> OK  e2e-user-zero — 9/9
> OK  gamificacao-nodes — 9/9
> OK  mcorch-constellation — 9/9
> OK  mcorch-qa-healing — 9/9
> OK  mercado-livre-api — 9/9
> OK  meta-api — 9/9
> OK  openclaw — 9/9
> OK  viralmind — 9/9
> === meta-api dir contents ===
> total 104
> drwxrwxr-x  2 ubuntu ubuntu  4096 May 30 18:16 .
> drwxrwxr-x 13 ubuntu ubuntu  4096 May 30 18:16 ..
> -rw-rw-r--  1 ubuntu ubuntu  5413 May 30 18:16 00-index.md
> -rw-rw-r--  1 ubuntu ubuntu  7152 May 30 18:16 01-mrd.md
> -rw-rw-r--  1 ubuntu ubuntu  5529 May 30 18:16 02-brd.md
> -rw-rw-r--  1 ubuntu ubuntu  5990 May 30 18:16 03-prd.md
> -rw-rw-r--  1 ubuntu ubuntu  5060 May 30 18:16 04-frd.md
> -rw-rw-r--  1 ubuntu ubuntu  7939 May 30 18:16 05-sdd.md
> -rw-rw-r--  1 ubuntu ubuntu  5825 May 30 18:16 06-data-model.md
> -rw-rw-r--  1 ubuntu ubuntu  3909 May 30 18:16 07-process-flow.md
> -rw-rw-r--  1 ubuntu ubuntu  3618 May 30 18:16 08-quality-metrics.md
> -rw-rw-r--  1 ubuntu ubuntu 28955 May 30 18:16 bok-agents-system--meta-api.md
> === .env presence ===
> WORKTREE has NO .env (trap)
> MAIN .env: 1144 May 23 19:39 /home/gcrUX/htdocs/constellation-orchestra/.env
> MAIN repo has .env
> ```

## 🤖 Claude *(21:18:46)*


## 🤖 Claude *(21:18:48)*

Worktree is at `4f243c0` = `origin/main` = `main` (0/0 ahead/behind) — the push is real and synced. All 11 BoK suites are 9/9, meta-api included. Now the one shaky part of the Antigravity transcript: the embedding calls visibly failed twice (`{record:{id}}` then `{node_id}`) and the node-count queries never cleanly returned. The seal nonetheless claims "embedded 768d / 8665 nodes". Let me verify that materially against Supabase (read-only GET, using the main repo's `.env`).

## 🤖 Claude *(21:18:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra && set -a && source .env 2>/dev/null && set +a\nKEY=\"${SUPABASE_SERVICE_ROLE_KEY:-$VITE_SUPABASE_PUBLISHABLE_KEY}\"\nURL=\"${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}\"\necho \"=== total node count (Range header) ===\"\ncurl -s -I \"$URL/rest/v1/mcorch_nodes?select=id\" \\\n  -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" -H \"Range: 0-0\" -H \"Prefer: count=exact\" \\\n  | grep -i \"content-range\" | tr -d '\\r'\necho \"=== handoff node 2eb1aca5 (exists?) ===\"\ncurl -s \"$URL/rest/v1/mcorch_nodes?id=eq.2eb1aca5-7eda-4911-ab10-b3b0db129665&select=id,name,node_type,stability_score,created_at\" \\\n  -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\"\necho \"\"\necho \"=== handoff node 2eb1aca5 (embedded? non-empty=yes) ===\"\ncurl -s \"$URL/rest/v1/mcorch_nodes?id=eq.2eb1aca5-7eda-4911-ab10-b3b0db129665&embedding=not.is.null&select=id\" \\\n  -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\"\necho \"\"\necho \"=== BoK seal node bok-scribe-seal-meta-api-v1 (exists + embedded?) ===\"\ncurl -s \"$URL/rest/v1/mcorch_nodes?name=eq.bok-scribe-seal-meta-api-v1&select=id,name,node_type,stability_score,created_at\" \\\n  -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\"\necho \"\"\ncurl -s \"$URL/rest/v1/mcorch_nodes?name=eq.bok-scribe-seal-meta-api-v1&embedding=not.is.null&select=id\" \\\n  -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\"\necho \"\"",
  "description": "Verify mesh node count and embedding status for Antigravity seal nodes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === total node count (Range header) ===
> content-range: 0-999/8665
> === handoff node 2eb1aca5 (exists?) ===
> [{"id":"2eb1aca5-7eda-4911-ab10-b3b0db129665","name":"session-handoff-20260530-meta-api-bok-seal","node_type":"handoff","stability_score":1,"created_at":"2026-05-30T20:54:38.871698+00:00"}]
> === handoff node 2eb1aca5 (embedded? non-empty=yes) ===
> [{"id":"2eb1aca5-7eda-4911-ab10-b3b0db129665"}]
> === BoK seal node bok-scribe-seal-meta-api-v1 (exists + embedded?) ===
> [{"id":"ca791bdd-cf7c-48cc-811a-fd2f7e99870f","name":"bok-scribe-seal-meta-api-v1","node_type":"documentation_suite","stability_score":0.85,"created_at":"2026-05-30T20:20:52.790865+00:00"}]
> [{"id":"ca791bdd-cf7c-48cc-811a-fd2f7e99870f"}]
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09
> ```

## 🤖 Claude *(21:19:36)*


## 🤖 Claude *(21:19:39)*

All three shaky claims from the Antigravity transcript check out materially:
- **8665 nodes** — exactly as the seal claims (the transcript's count queries failed on shell parsing, but the number is right).
- **Handoff node `2eb1aca5`** — exists (handoff, stability 1.0, 20:54Z) **and is embedded** (the two manual `embed-mcorch-node` calls failed, but the `trg_mcorch_embed_on_insert` pg_net trigger did the embedding automatically — so the claim is true).
- **BoK seal `ca791bdd`** — exists (documentation_suite, 0.85) and embedded.

One last discrepancy to resolve: the v6.14.3 seal says "8990 edges" but the stale GraphRAG tail says 11925. Let me grab the real edge count.

## 🤖 Claude *(21:19:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra && set -a && source .env 2>/dev/null && set +a\nKEY=\"${SUPABASE_SERVICE_ROLE_KEY:-$VITE_SUPABASE_PUBLISHABLE_KEY}\"\nURL=\"${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}\"\necho \"=== edges count ===\" && curl -s -I \"$URL/rest/v1/mcorch_edges?select=id\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" -H \"Range: 0-0\" -H \"Prefer: count=exact\" | grep -i content-range | tr -d '\\r'\necho \"=== DERIVES_FROM edge meta-api \u2192 mercado-livre parent? ===\" && curl -s \"$URL/rest/v1/mcorch_edges?source_id=eq.ca791bdd-cf7c-48cc-811a-fd2f7e99870f&select=id,edge_type,target_id\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\"\necho \"\"\necho \"=== nodes without embedding (should be small/zero) ===\" && curl -s -I \"$URL/rest/v1/mcorch_nodes?embedding=is.null&select=id\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" -H \"Range: 0-0\" -H \"Prefer: count=exact\" | grep -i content-range | tr -d '\\r'",
  "description": "Verify real edge count, DERIVES_FROM linkage, and unembedded node count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === edges count ===
> content-range: 0-999/8990
> === DERIVES_FROM edge meta-api → mercado-livre parent? ===
> {"code":"42703","details":null,"hint":null,"message":"column mcorch_edges.edge_type does not exist"}
> === nodes without embedding (should be small/zero) ===
> content-range: */0
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09
> ```

## 🤖 Claude *(21:20:20)*


## 🤖 Claude *(21:20:57)*

Everything reconciles. Final material picture confirmed:

- **Edges: 8990** — exactly as the v6.14.3 seal states (the stale tail's 11925 is just an un-refreshed suffix section).
- **Nodes without embedding: 0** (`*/0`) → neural density **100%**, autoembed pipeline healthy.
- DERIVES_FROM linkage: couldn't confirm independently (the `mcorch_edges` column isn't `edge_type` — I won't assert what I didn't verify).

Here's the pickup brief.

---

═══════════════════════════════════════════════════════════
  **HANDSON — v6.14.3 · meta-api BoK Suite & Agents System** (selado 2026-05-30 pelo Antigravity IDE)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **meta-api BoK Suite & Agents System** (Meta Integration — Facebook, Instagram, WhatsApp, Ads, MCP). Especificação pura, **zero código de produção**.
  Worktree `claude/beautiful-dijkstra-207b09` @ `4f243c0` = `origin/main` = `main` → **0/0 ahead/behind** (push real e sincronizado).
  Últimos commits:
    `4f243c0` — docs(handoff): seal v6.14.3 — meta-api BoK suite & agents system
    `4a1e419` — docs(readme): v6.14.3
    `6dca22d` — chore(test): make canvas video async smoke E2E test robust
    `d6bfb64` — chore(scripts): seed script for meta-api BoK seal
    `5197097` — docs(bok): meta-api BoK suite and agents system

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ — nada para commitar.

🏗️ **INFRA** (todos healthy há 6 dias)
  `mcorch_chroma`: Up (healthy) — Chroma API v2 heartbeat **OK**
  `mcorch_claude_mem`: Up (healthy)
  `mega-brain-daemon` / `-webhook`: Up (healthy) · `-dashboard`: Up

🧠 **KNOWLEDGE MESH** (verificado materialmente via REST agora)
  **8665 nós · 8990 arestas** — bate exatamente com o selo v6.14.3.
  **Densidade neural 100%** — `embedding=is.null` retorna `*/0` (zero nós sem embedding).
  Nós do selo confirmados embedded: handoff `2eb1aca5` + BoK seal `ca791bdd`.

🔧 **TYPESCRIPT**
  `npx tsc --noEmit` → **zero erros** ✅

📚 **BoK SUITES** — **11/11 completas (9/9 docs cada)** ✅
  `aios-sql-bridge · canvas-design · conteudo-v2 · e2e-user-zero · gamificacao-nodes · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · viralmind`
  Mesh seals confirmados: `bok-scribe-seal-meta-api-v1` (`ca791bdd`, stability 0.85, embedded). **BoK Gate VERDE** — Meta Integration liberada para código.

🔬 **ANÁLISE DO HANDOFF DO ANTIGRAVITY** (o que você pediu)
  **Veredito: selo materialmente SÓLIDO.** Toda claim de SUCCESS que dava para testar passou:

  | Claim do selo | Verificação material | Resultado |
  |---|---|---|
  | Push sincronizado | `git rev-list origin/main...HEAD` | ✅ 0/0 |
  | meta-api 9/9 docs | loop `ls docs/bok/meta-api/` | ✅ 9 docs + agents-system |
  | Handoff node embedded 768d | REST `embedding=not.is.null` | ✅ existe + embedded |
  | BoK seal node embedded | REST | ✅ existe + embedded |
  | 8665 nós | `Range` + `count=exact` | ✅ 8665 exato |
  | 8990 arestas | idem | ✅ 8990 exato |

  **Observações (nenhuma bloqueia, mas registre):**
  1. **O transcript "parecia" instável, mas o estado final é limpo.** As 2 chamadas manuais a `embed-mcorch-node` (`{record:{id}}` e depois `{node_id}`) falharam — **eram redundantes**: o trigger `trg_mcorch_embed_on_insert` (pg_net) já embeda no INSERT. O nó está embedded de qualquer forma. As queries de contagem falhavam só por parsing de shell, não por dado faltando.
  2. **Rebase dance defensável.** O Antigravity fez `reset --hard origin/main` + cherry-pick porque seu main local divergira do push da sessão anterior do Claude (v6.14.2, OTD-ML-001). A reconciliação **preservou** os commits v6.14.2 (`4cfe96f`/`5640744`) por baixo — nada foi perdido, histórico linear. Foi cuidado, não atropelo.
  3. **HANDOFF.md tem cauda STALE.** As seções-sufixo (`GraphRAG State`, `Pending Actions`, `Infrastructure`) não são atualizadas há ~v6.8.6 → leem **8605 nós / 11925 arestas / Canvas 4.2** como "atual". Os números verdadeiros (8665/8990) vivem **só** no record do topo. Quem ler a cauda para "estado atual" se engana. *(Candidato a faxina num próximo seal.)*
  4. **`Co-Authored-By: Antigravity IDE` em todos os 5 commits** — diverge da sua preferência registrada (`feedback_commits.md`: *"Nunca Co-Authored-By"*). Já pushado; só registro para futuros agentes.
  5. **Fix do `canvas-video-async-smoke.test.ts`** (PGRST116 "2 rows" → `order created_at desc` + `maybeSingle()`) é correto, mas sugere que `vm_canvas_assets` acumula resíduo entre runs async — o fix mascara, não limpa.

📌 **SPRINT**
  Goal: *Distribuição social autônoma operacional* (LinkedIn auto ✅ · Twitter aguarda Basic tier · Instagram aguarda App Review Meta).
  OE-661-ROADMAP debts: Financial (Stripe swap, deferido) · Postback (scientist) · Memory/Gateway (main) · Million-BRL Link Forge (marketing-growth).

⚡ **PRÓXIMOS PASSOS** (do selo v6.14.3 — Módulo Meta, agora desbloqueado pelo BoK Gate)
  1. **`publish-meta` Edge Function** (Social Gateway MVP) — OAuth via `meta_config` **per-user**. ⚠️ Exige o checklist completo de *API Tenancy*: migration `meta_config` (RLS `auth.uid()=user_id` + UNIQUE) → UI em `/dashboard/settings` → lookup helper → telemetry `infra_health_logs` → **SOP `docs/processes/meta-credential-resolution.md` ANTES do código** (Lei 2).
  2. **`whatsapp-webhook`** — listener assíncrono de templates HSM (leads).
  3. **ROIWidget × cache de custos Meta** no dashboard (`profiles.mco_balance`).
  *(Carry-over antigo ainda aberto: Canvas DoP Standard 5s paid smoke — Sovereign clica Run; e e2e-user-zero 2ª iteração.)*

⚠️ **ALERTAS**
  Nenhum bloqueador ✅. Pontos de atenção: cauda do HANDOFF.md desatualizada (#3) e resíduo em `vm_canvas_assets` (#5) — ambos cosméticos, não travam trabalho.

═══════════════════════════════════════════════════════════
  Selo do Antigravity validado. Mesh íntegro (100% embedded). BoK Gate verde.
  **Pronto para trabalhar. Aguardando direção** — se for atacar o gateway Meta (`publish-meta`), começo pela SOP de credenciais per-user (Lei 2).
═══════════════════════════════════════════════════════════

## 👤 User *(21:25:30)*

ok segue com os próximos passos

## 🤖 Claude *(21:26:11)*


## 🤖 Claude *(21:26:12)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Meta gateway: publish-meta",
  "summary": "Build the publish-meta edge function + meta_config per-user credentials, grounded in the sealed meta-api BoK, SOP-first per Law 2"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Meta gateway: publish-meta". Continue your current work.'}]
> ```

## 🤖 Claude *(21:26:15)*


## 🤖 Claude *(21:26:19)*

Seguindo. Antes de qualquer código, declaro o **ORO triplet** e leio a Fonte da Verdade (BoK meta-api selada) — nada de invenção além do documentado.

**ORO triplet desta task (Meta Gateway — Passo 1: `publish-meta` + `meta_config` per-user):**
- **Operator:** MCORCH Master Execution Agent (eu)
- **Reviewer:** Sovereign (Gabriel) — aprova migration via `/security-review` + deploy
- **Owner:** Sovereign — blast radius = gateway Meta/WhatsApp + credenciais OAuth per-tenant + integridade financeira (quota/revenue por user)

Lendo o BoK selado (`docs/bok/meta-api/`) como SSOT — FRD, SDD, Data Model e Process Flow em paralelo:

## 🤖 Claude *(21:26:20)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/meta-api/06-data-model.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Data & Knowledge Model Document
> 2	
> 3	**Project:** meta-api
> 4	**Version:** v1.0 | **Date:** 2026-05-30
> 5	**BoK Applied:** DMBOK v2 (Data Architecture + Data Security + Data Integration and Interoperability)
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Database Schema Specification
> 11	
> 12	### 1.1 Table: `meta_config`
> 13	Armazena a configuração das credenciais e contas da Meta vinculadas por usuário.
> 14	
> 15	```sql
> 16	CREATE TABLE public.meta_config (
> 17	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 18	    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 19	    facebook_user_id VARCHAR(255) NOT NULL,
> 20	    long_lived_token_encrypted TEXT NOT NULL, -- Encriptado com pg_sodium ou chave vault
> 21	    scopes VARCHAR[] NOT NULL,
> 22	    pages JSONB DEFAULT '[]'::jsonb, -- Array de páginas com page_id, name, token_encrypted
> 23	    instagram_business_account_id VARCHAR(255),
> 24	    whatsapp_phone_number_id VARCHAR(255),
> 25	    whatsapp_waba_id VARCHAR(255),
> 26	    meta_ad_account_id VARCHAR(255),
> 27	    requires_reauth BOOLEAN DEFAULT FALSE,
> 28	    token_expires_at TIMESTAMP WITH TIME ZONE,
> 29	    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
> 30	    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
> 31	    CONSTRAINT unique_user_meta UNIQUE (user_id)
> 32	);
> 33	```
> 34	
> 35	### 1.2 Table: `meta_posts`
> 36	Registra o histórico de publicações efetuadas através do MCORCH nas redes Meta.
> 37	
> 38	```sql
> 39	CREATE TABLE public.meta_posts (
> 40	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 41	    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 42	    campaign_id UUID, -- Referência opcional à campanha no banco
> 43	    platform VARCHAR(50) NOT NULL, -- 'instagram' ou 'facebook'
> 44	    meta_post_id VARCHAR(255) NOT NULL, -- ID retornado pela API da Meta
> 45	    post_url VARCHAR(1024),
> 46	    caption TEXT,
> 47	    media_url VARCHAR(1024),
> 48	    status VARCHAR(50) DEFAULT 'published' NOT NULL, -- 'published', 'failed'
> 49	    error_message TEXT,
> 50	    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
> 51	);
> 52	```
> 53	
> 54	### 1.3 Table: `whatsapp_leads`
> 55	Armazena leads capturados e o fluxo de conversações via WhatsApp.
> 56	
> 57	```sql
> 58	CREATE TABLE public.whatsapp_leads (
> 59	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 60	    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 61	    phone_number VARCHAR(50) NOT NULL,
> 62	    lead_name VARCHAR(255),
> 63	    status VARCHAR(50) DEFAULT 'iniciado' NOT NULL, -- 'iniciado', 'interagido', 'convertido', 'opt_out'
> 64	    metadata JSONB DEFAULT '{}'::jsonb,
> 65	    last_message_received_at TIMESTAMP WITH TIME ZONE,
> 66	    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
> 67	    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
> 68	    CONSTRAINT unique_user_phone UNIQUE (user_id, phone_number)
> 69	);
> 70	```
> 71	
> 72	### 1.4 Table: `meta_ads_metrics`
> 73	Cache de métricas diárias de performance de Meta Ads.
> 74	
> 75	```sql
> 76	CREATE TABLE public.meta_ads_metrics (
> 77	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 78	    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 79	    campaign_name VARCHAR(255) NOT NULL,
> 80	    meta_campaign_id VARCHAR(255) NOT NULL,
> 81	    spend_cents INTEGER DEFAULT 0 NOT NULL,
> 82	    clicks INTEGER DEFAULT 0 NOT NULL,
> 83	    impressions INTEGER DEFAULT 0 NOT NULL,
> 84	    date_metric DATE NOT NULL,
> 85	    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
> 86	    CONSTRAINT unique_campaign_date UNIQUE (user_id, meta_campaign_id, date_metric)
> 87	);
> 88	```
> 89	
> 90	---
> 91	
> 92	## 2. Row Level Security (RLS) Policies
> 93	
> 94	Todas as tabelas possuem RLS ativado por padrão. O isolamento garante acesso estrito do inquilino dono.
> 95	
> 96	```sql
> 97	-- Ativar RLS
> 98	ALTER TABLE public.meta_config ENABLE ROW LEVEL SECURITY;
> 99	ALTER TABLE public.meta_posts ENABLE ROW LEVEL SECURITY;
> 100	ALTER TABLE public.whatsapp_leads ENABLE ROW LEVEL SECURITY;
> 101	ALTER TABLE public.meta_ads_metrics ENABLE ROW LEVEL SECURITY;
> 102	
> 103	-- Políticas para meta_config
> 104	CREATE POLICY "Users can manage their own Meta config" ON public.meta_config
> 105	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 106	
> 107	-- Políticas para meta_posts
> 108	CREATE POLICY "Users can manage their own Meta posts" ON public.meta_posts
> 109	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 110	
> 111	-- Políticas para whatsapp_leads
> 112	CREATE POLICY "Users can manage their own WhatsApp leads" ON public.whatsapp_leads
> 113	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 114	
> 115	-- Políticas para meta_ads_metrics
> 116	CREATE POLICY "Users can manage their own Meta Ads metrics" ON public.meta_ads_metrics
> 117	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 118	```
> 119	
> 120	---
> 121	
> 122	## 3. Database Functions & Triggers
> 123	
> 124	### 3.1 Trigger para Atualizar `updated_at`
> 125	```sql
> 126	CREATE OR REPLACE FUNCTION public.update_updated_at_column()
> 127	RETURNS TRIGGER AS $$
> 128	BEGIN
> 129	    NEW.updated_at = now();
> 130	    RETURN NEW;
> 131	END;
> 132	$$ language 'plpgsql';
> 133	
> 134	CREATE TRIGGER tr_update_meta_config_updated_at
> 135	    BEFORE UPDATE ON public.meta_config
> 136	    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 137	
> 138	CREATE TRIGGER tr_update_whatsapp_leads_updated_at
> 139	    BEFORE UPDATE ON public.whatsapp_leads
> 140	    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 141	```
> 142	
> 143	---
> 144	
> 145	## 4. Vector Representation & Knowledge Mesh Mapping
> 146	
> 147	Todas as postagens publicadas e leads convertidos com sucesso geram nós do tipo `observation` na tabela principal do Knowledge Mesh (`mcorch_nodes`) com a sua respectiva aresta `observes` ligando ao arquivo ou asset envolvido:
> 148	
> 149	```
> 150	[meta_posts.id]  ──►  mcorch_nodes (type='observation', name='post:instagram:<post_id>')
> 151	                          │
> 152	                          └───►  mcorch_edges (relation_type='observes', target_id=asset_id)
> 153	```
> 154	
> 155	---
> 156	
> 157	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 158	
> ```

## 🤖 Claude *(21:26:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/meta-api/05-sdd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SDD — System Design Document
> 2	
> 3	**Project:** meta-api
> 4	**Version:** v1.0 | **Date:** 2026-05-30
> 5	**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK (Security Architecture and Engineering)
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Architecture Overview
> 11	
> 12	```
> 13	 ┌────────────────────────────────────────────────────────┐
> 14	 │                   Antigravity IDE /                    │
> 15	 │               Orchestra React Dashboard                │
> 16	 └───────────────────────────┬────────────────────────────┘
> 17	                             │ (https / ws)
> 18	                             ▼
> 19	 ┌────────────────────────────────────────────────────────┐
> 20	 │              Supabase Edge Functions /                 │
> 21	 │                  API Tenancy Router                    │
> 22	 ├───────────────────────────┬────────────────────────────┤
> 23	 │  [meta-oauth]             │  [publish-meta]            │
> 24	 │  [whatsapp-webhook]       │  [sync-meta-ads]           │
> 25	 └─────────────┬─────────────┴──────────────┬─────────────┘
> 26	               │ (SSL)                      │ (JSON-RPC stdio)
> 27	               ▼                            ▼
> 28	 ┌───────────────────────────┐┌───────────────────────────┐
> 29	 │   Supabase PostgreSQL /   ││      Meta MCP Server      │
> 30	 │  RLS-Isolated Database    ││      (Docker Daemon)      │
> 31	 └───────────────────────────┘└─────────────┬─────────────┘
> 32	                                            │ (Graph API)
> 33	                                            ▼
> 34	                              ┌───────────────────────────┐
> 35	                              │     Meta External APIs    │
> 36	                              │ (Facebook / IG / WhatsApp)│
> 37	                              └───────────────────────────┘
> 38	```
> 39	
> 40	---
> 41	
> 42	## 2. Key Components Catalog
> 43	
> 44	### 2.1 Edge Functions (`supabase/functions/`)
> 45	*   **`meta-oauth`**: Trata o callback HTTP do login do Facebook, resolve tokens de longa duração e persiste a configuração do tenant em `meta_config`.
> 46	*   **`publish-meta`**: Invocada pelo `PublishNode` no pipeline de orquestração. Realiza upload de ativos para o CDN da Meta e orquestra a criação de posts/stories/reels.
> 47	*   **`whatsapp-webhook`**: Endpoint público que valida o token de verificação Meta (durante setup) e recebe webhooks de mensagens enviadas para o WhatsApp Business Account.
> 48	*   **`sync-meta-ads`**: Cron scheduler interno que consulta diariamente métricas das ad accounts vinculadas.
> 49	
> 50	### 2.2 Packages
> 51	*   **`packages/meta-mcp-server`**: Servidor MCP baseado em Typescript que implementa o protocolo Model Context Protocol (MCP) para expor ferramentas de leitura/escrita de redes sociais e ads. Executado como processo stdio headless.
> 52	
> 53	### 2.3 Database Layer
> 54	*   Tabela `meta_config` para credenciais e dados de contas (Facebook Pages e Instagram Business Accounts).
> 55	*   Tabela `meta_posts` para histórico de publicações e links de post.
> 56	*   Tabela `whatsapp_leads` para cadastros de conversas de WhatsApp e status do fluxo de atendimento.
> 57	*   Tabela `meta_ads_metrics` para cache diário de gastos e conversões de anúncios.
> 58	
> 59	---
> 60	
> 61	## 3. Secret & Credentials Lifecycle (API Tenancy Model)
> 62	
> 63	O gerenciamento de credenciais da Meta segue estritamente as diretivas estabelecidas no `CLAUDE.md`:
> 64	
> 65	```
> 66	Request Meta Publish → Decrypt per-user long-lived token from `meta_config`
> 67	                          │ (If token valid)
> 68	                          ├──► Proceed to Meta Graph API
> 69	                          │ (If token expired/invalid)
> 70	                          └──► Throw HTTP 402/501 (Requires Reauth)
> 71	                                 └──► Update UI banner to alert creator
> 72	```
> 73	
> 74	*   **Encryption at Rest:** O token é armazenado no banco de dados Supabase criptografado com a extensão `pgsodium` ou via chaves de encriptação rotacionadas gerenciadas em variáveis do Supabase vault.
> 75	*   **Token Refresh Flow:** O scheduler verifica a expiração de tokens. Meta long-lived user tokens duram 60 dias. Antes de expirar, a UI incentiva o usuário a re-autenticar. Page tokens (tokens de página) derivados a partir do user token possuem expiração de tempo infinito enquanto o consentimento não for revogado.
> 76	
> 77	---
> 78	
> 79	## 4. Threat Modeling (STRIDE)
> 80	
> 81	| Threat Category | Specific Threat | Impact | Mitigation Strategy |
> 82	|---|---|---|---|
> 83	| **S**poofing | Agressor envia webhooks de WhatsApp falsos para forjar interações de leads. | Leads falsos no sistema, processamento inútil de IA. | Validação estrita do cabeçalho `X-Hub-Signature-256` contendo assinatura HMAC SHA-256. |
> 84	| **T**ampering | Agressor modifica valores de cliques/custos de Meta Ads durante a sincronização. | Relatório de ROI corrompido, tomadas de decisão erradas de orçamento. | Assinatura de integridade no banco de dados e consulta restrita a HTTPS SSL direto da API Meta. |
> 85	| **I**nformation Disclosure | Token de acesso da Meta de um tenant é exposto a outro usuário. | Controle total das páginas e perfil de terceiros por atacante. | RLS restritivo com `user_id = auth.uid()` obrigatório. Proibição de consultas que retornem chaves de API sem criptografia para o client. |
> 86	| **D**enial of Service | Envio massivo de mensagens no webhook de WhatsApp esgota os recursos do Supabase. | Queda do serviço de webhook e suspensão de processamento de leads legítimos. | Rate-limit por IP no webhook e uso de fila de mensagens assíncrona (Supabase Queue/pg_net) para desacoplar recebimento de processamento. |
> 87	| **E**levation of Privilege | Inquilino manipula a chamada RPC para obter credenciais de admin do Meta Ads global. | Acesso às contas financeiras de anúncios da plataforma. | Verificação rígida de roles (`has_role('admin')`) para endpoints administrativos de Ads. |
> 88	
> 89	---
> 90	
> 91	## 5. Circuit Breaker, Queue & Retry Flow
> 92	
> 93	```
> 94	              ┌──────────────────────────────────────────────┐
> 95	              │           WhatsApp Cloud API Request          │
> 96	              └──────────────────────┬───────────────────────┘
> 97	                                     ▼
> 98	                        Is API Offline / Returning 5xx?
> 99	                       /                               \
> 100	                     (No)                             (Yes)
> 101	                     /                                   \
> 102	                    ▼                                     ▼
> 103	           Execute Request                 Trigger Circuit Breaker
> 104	            /            \                  (Block requests for 15m)
> 105	     (HTTP 200)       (HTTP 429 Rate)                     │
> 106	         /                    \                           ▼
> 107	        ▼                      ▼                 Queue Message for Later
> 108	   Success Log          Enqueue with
> 109	                   Exponential Backoff
> 110	```
> 111	
> 112	---
> 113	
> 114	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 115	
> ```

## 🤖 Claude *(21:26:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/meta-api/04-frd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** meta-api
> 4	**Version:** v1.0 | **Date:** 2026-05-30
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements + Software Quality)
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Functional Decomposition
> 11	
> 12	```
> 13	meta-api Integration
> 14	├── Auth & Tokens (Meta OAuth 2.0 flow, token refresh daemon)
> 15	├── Media Publisher (Facebook mural post, Instagram photo & video publisher)
> 16	├── WhatsApp Gateway (Webhook message receiver, HSM & custom message sender)
> 17	├── Ads Collector (Meta Ads Insights API aggregator, Campaign ROI mapper)
> 18	├── Meta MCP Server (stdio tool executor, sub-agent capabilities)
> 19	└── Telemetry (health logs generator, token monitoring alert)
> 20	```
> 21	
> 22	---
> 23	
> 24	## 2. Functional Requirements
> 25	
> 26	*   **FR-META-001 (OAuth Token Exchange):** O endpoint `/api/meta-oauth` deve trocar o código de autorização temporário da Meta por um token de usuário de curta duração, e imediatamente negociar o token de longa duração (60 dias) via endpoint oficial da Meta.
> 27	*   **FR-META-002 (Instagram Media Container):** O sistema deve iniciar a postagem no Instagram criando um container de mídia com o parâmetro `image_url` e `caption`, pollar o status do container até constatar `FINISHED` e emitir a requisição final de publicação (`media_publish`).
> 28	*   **FR-META-003 (Facebook Page Publisher):** O sistema deve publicar posts na timeline do Facebook utilizando chaves `/feed` da Page API correspondente ao token da página selecionada.
> 29	*   **FR-META-004 (WhatsApp HMAC Signature Validation):** O endpoint `/functions/v1/whatsapp-webhook` deve recalcular a assinatura SHA-256 HMAC do payload usando a webhook secret do tenant e compará-la com o cabeçalho `X-Hub-Signature-256`. Rejeitar se divergir.
> 30	*   **FR-META-005 (WhatsApp Message Dispatcher):** O sistema deve rotear o disparo de mensagens para o endpoint `/{phone-number-id}/messages` da Cloud API, identificando se é uma mensagem HSM (template) ou uma mensagem de texto simples.
> 31	*   **FR-META-006 (Meta Ads Metrics Sync):** A rotina diária deve consultar a API do Meta Ads `/act_{ad-account-id}/insights` recuperando as métricas agregadas por campanha, gravando em `meta_ads_metrics`.
> 32	*   **FR-META-007 (MCP Tools Router):** O package `meta-mcp-server` deve mapear chamadas JSON-RPC de ferramentas (`meta_post_content`, `meta_get_comments`, `meta_list_campaigns`) para as funções internas correspondentes.
> 33	*   **FR-META-008 (Tenancy Filter):** Todas as consultas às tabelas `meta_config`, `meta_posts` e `whatsapp_leads` devem conter a cláusula `WHERE user_id = auth.uid()` implícita através de Row Level Security (RLS).
> 34	*   **FR-META-009 (Telemetry Logger):** Qualquer falha de requisição da API Meta (erros de escopo, tokens expirados ou bloqueios de rate) deve inserir um log de falha em `infra_health_logs` com `service='meta-api'`.
> 35	*   **FR-META-010 (Token Expiry Watcher):** O daemon ou cron diário do sistema deve varrer a tabela `meta_config` verificando registros cujos tokens expiram em menos de 7 dias, ativando a flag `requires_reauth = true`.
> 36	
> 37	---
> 38	
> 39	## 3. Non-Functional Requirements
> 40	
> 41	### 3.1 Security (Segurança)
> 42	*   **NFR-META-001 (Token Protection):** Todos os tokens de acesso (User, Page, WhatsApp tokens) devem ser encriptados no banco de dados Supabase utilizando criptografia AES-256-GCM.
> 43	*   **NFR-META-002 (Tenancy Isolation):** Nenhuma transação ou dado sensível de um usuário Meta pode ser visível ou utilizável por outro inquilino do sistema (fail-closed a nível de banco de dados).
> 44	
> 45	### 3.2 Performance (Desempenho)
> 46	*   **NFR-META-003 (Execution Time):** O tempo de processamento de uma publicação de imagem única (excluindo download de mídia) não deve exceder 12 segundos.
> 47	*   **NFR-META-004 (Webhook Latency):** O tempo de resposta para confirmação de recebimento de webhook do WhatsApp deve ser inferior a 2 segundos (retornando HTTP 200) para evitar reenvios da Meta.
> 48	
> 49	### 3.3 Reliability & Availability (Confiabilidade e Disponibilidade)
> 50	*   **NFR-META-005 (Circuit Breaker):** Caso a API da Meta retorne erro 5xx de forma contínua, o sistema deve acionar o circuit breaker para o tenant, suspendendo novas tentativas por 15 minutos.
> 51	*   **NFR-META-006 (Message Retry):** Disparos de mensagens de WhatsApp com falha de rede temporária devem ser re-enfileirados automaticamente com retry exponencial de até 3 tentativas.
> 52	
> 53	---
> 54	
> 55	## 4. Test Strategy Matrix
> 56	
> 57	| Test Case ID | Feature | Target Condition | Verification Method |
> 58	|---|---|---|---|
> 59	| TC-META-001 | Auth OAuth | Long-lived token exchange succeeds | Integration test with Mock Meta API server |
> 60	| TC-META-002 | RLS Isolation | User A attempts to write to User B config | Database RLS unit tests (`supabase-test`) |
> 61	| TC-META-003 | Webhook Validation| Payload with forged X-Hub-Signature is rejected| Webhook endpoint unit tests with invalid signature |
> 62	| TC-META-004 | Media Publish | High resolution image published on Instagram | Playwright E2E sandbox verification |
> 63	
> 64	---
> 65	
> 66	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 67	
> ```

## 🤖 Claude *(21:26:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/meta-api/07-process-flow.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Process & Automation Blueprint Document
> 2	
> 3	**Project:** meta-api
> 4	**Version:** v1.0 | **Date:** 2026-05-30
> 5	**BoK Applied:** BPM CBOK v4 (Process Design + Process Performance Measurement)
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Process Swimlanes (Sequence Flow)
> 11	
> 12	```
> 13	[User / Client]         [React Frontend]          [Edge Functions]         [Meta Graph API]
> 14	       │                        │                        │                        │
> 15	       │─── 1. Click Connect ──►│                        │                        │
> 16	       │                        │─── 2. Redirect OAuth ─►│                        │
> 17	       │                        │                        │─── 3. Auth Request ───►│
> 18	       │                        │                        │◄── 4. Code & Token ────│
> 19	       │                        │◄── 5. Token Refreshed ─│                        │
> 20	       │                        │                        │                        │
> 21	       │◄── 6. Active Banner ───│                        │                        │
> 22	```
> 23	
> 24	---
> 25	
> 26	## 2. Process Catalog
> 27	
> 28	### PROC-META-001: Meta OAuth Authentication & Callback
> 29	1.  **Trigger:** O usuário clica em "Conectar Meta" nas configurações.
> 30	2.  **Sequence:**
> 31	    *   O frontend inicia o fluxo do Facebook SDK Login.
> 32	    *   O callback captura o `code` temporário e envia via POST para a Edge Function `meta-oauth`.
> 33	    *   `meta-oauth` solicita o token de longa duração e o persiste encriptado em `meta_config`.
> 34	    *   O sistema consulta `/me/accounts` para listar as Facebook Pages autorizadas e obter seus respectivos tokens perpétuos.
> 35	3.  **Handoff:** O fluxo salva as credenciais e atualiza o estado de conexão do usuário para `Connected`.
> 36	
> 37	### PROC-META-002: Omnichannel Content Publication (Facebook & Instagram)
> 38	1.  **Trigger:** O `PublishNode` é disparado durante uma execução de pipeline.
> 39	2.  **Sequence:**
> 40	    *   `publish-meta` busca o token da página/Instagram no banco.
> 41	    *   Inicia upload da imagem/vídeo para o repositório temporário da Meta.
> 42	    *   Faz o post da mídia e armazena os IDs gerados em `meta_posts`.
> 43	    *   Insere o nó de observação no Knowledge Mesh (`mcorch_nodes`) vinculando com o asset.
> 44	3.  **Handoff:** Retorna os links dos posts publicados para exibição na UI do canvas.
> 45	
> 46	### PROC-META-003: WhatsApp Inbound Message & AI Chat Routing
> 47	1.  **Trigger:** O webhook público recebe uma notificação POST de mensagem da Meta.
> 48	2.  **Sequence:**
> 49	    *   Valida a assinatura HMAC. Retorna HTTP 200 imediatamente.
> 50	    *   Analisa o JSON para extrair o número do remetente e a mensagem.
> 51	    *   Verifica e atualiza/cria o registro do contato em `whatsapp_leads`.
> 52	    *   Roteia a mensagem para o subagente correspondente usando o gateway OpenClaw.
> 53	3.  **Handoff:** O subagente formula a resposta e dispara `PROC-META-004`.
> 54	
> 55	### PROC-META-004: WhatsApp Outbound HSM Notification
> 56	1.  **Trigger:** Evento do sistema (ex: carrinho abandonado) ou resposta formulada por subagente.
> 57	2.  **Sequence:**
> 58	    *   Verifica a janela de 24 horas do contato em `whatsapp_leads`.
> 59	    *   Se estiver fora da janela, força a formatação de mensagem utilizando um template HSM homologado.
> 60	    *   Envia via Cloud API e registra o status de entrega no banco.
> 61	
> 62	---
> 63	
> 64	## 3. Operational Failure & Self-healing Loops
> 65	
> 66	```
> 67	      Publish Action Fails (Token Expired)
> 68	                       │
> 69	                       ▼
> 70	         Write to `infra_health_logs`
> 71	                       │
> 72	                       ▼
> 73	    Set `meta_config.requires_reauth = true`
> 74	                       │
> 75	                       ▼
> 76	    Show Visual Red Banner to User in Panel
> 77	                       │
> 78	                       ▼
> 79	      Prompt User to Re-authenticate OAuth
> 80	```
> 81	
> 82	---
> 83	
> 84	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 85	
> ```

## 🤖 Claude *(21:26:53)*


## 🤖 Claude *(21:26:55)*

BoK is clear and complete — it's my SSOT. The data-model defines 4 tables (`meta_config`, `meta_posts`, `whatsapp_leads`, `meta_ads_metrics`), and Passo 1 (`publish-meta`) needs the `meta_config` + `meta_posts` foundation plus per-user credential resolution. Before writing anything, I must match existing project patterns (token storage, edge-fn conventions, settings UI). Let me explore how the codebase already handles per-user credentials and publishing.

## 🤖 Claude *(21:27:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09\necho \"=== social_credentials / user_api_keys / affiliate_config migrations ===\" && ls supabase/migrations/ | grep -iE \"social|api_key|affiliate|credential|meta\" || echo \"none by name\"\necho \"=== pgsodium / vault / encrypt usage anywhere ===\" && grep -rilE \"pgsodium|vault\\.|pgp_sym|crypto_aead|encrypt\" supabase/migrations/ 2>/dev/null | head || echo \"NO encryption extension usage in migrations\"\necho \"=== edge functions list ===\" && ls supabase/functions/ | grep -vE \"_shared|^import_map\" | head -60\necho \"=== settings UI / useUserApiKeys ===\" && ls src/hooks/ | grep -iE \"userApiKeys|social|config|meta\" ; echo \"---\" ; find src -iname \"*ettings*\" -o -iname \"*ApiKey*\" | grep -iE \"page|settings|apikey\" | head",
  "description": "Find credential patterns, encryption usage, edge fn + settings conventions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === social_credentials / user_api_keys / affiliate_config migrations ===
> 20260421000000_create_user_api_keys.sql
> 20260514040300_viralmind_affiliate_radar.sql
> 20260518020028_user_api_keys_replicate.sql
> 20260527005356_user_api_keys_higgsfield.sql
> 20260530183000_affiliate_tag_per_user.sql
> === pgsodium / vault / encrypt usage anywhere ===
> supabase/migrations/20260527005356_user_api_keys_higgsfield.sql
> === edge functions list ===
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
> list-provider-models
> openrouter-swarm
> optimize-schedule
> orchestrate-content
> orchestrate-step
> process-affiliate-link
> publish-social
> publish-wordpress
> refresh-social-token
> rescue-video
> search-constellation
> self-heal
> self-optimize
> social-auth-callback
> social-auth-init
> stripe-webhook
> sync-knowledge-mesh
> trigger-embeddings
> trigger-ingest
> tts-speak
> === settings UI / useUserApiKeys ===
> useAffiliateConfig.ts
> useSocialAccounts.ts
> useUserApiKeys.ts
> ---
> src/pages/SettingsPage.tsx
> src/hooks/useUserApiKeys.ts
> src/components/canvas/RightPanel/StyleSettingsPanel.tsx
> ```

## 🤖 Claude *(21:27:11)*


## 🤖 Claude *(21:27:12)*

Rich existing surface — `publish-social`, `social-auth-callback`, `instagram-webhook`, `social_credentials`, `user_api_keys` already exist. I must mirror these. Let me read the canonical patterns: the per-user table migration, an existing publish edge function, the settings hook, and verify how tokens are actually stored (encrypted vs RLS-only).

## 🤖 Claude *(21:27:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/supabase/migrations/20260421000000_create_user_api_keys.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	CREATE TABLE IF NOT EXISTS public.user_api_keys (
> 2	    user_id UUID REFERENCES auth.users(id) PRIMARY KEY,
> 3	    groq_api_key TEXT,
> 4	    openrouter_api_key TEXT,
> 5	    openai_api_key TEXT,
> 6	    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
> 7	    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
> 8	);
> 9	
> 10	ALTER TABLE public.user_api_keys ENABLE ROW LEVEL SECURITY;
> 11	
> 12	CREATE POLICY "Users can view their own api keys" ON public.user_api_keys
> 13	    FOR SELECT USING (auth.uid() = user_id);
> 14	
> 15	CREATE POLICY "Users can insert their own api keys" ON public.user_api_keys
> 16	    FOR INSERT WITH CHECK (auth.uid() = user_id);
> 17	
> 18	CREATE POLICY "Users can update their own api keys" ON public.user_api_keys
> 19	    FOR UPDATE USING (auth.uid() = user_id);
> 20	
> 21	
> ```

## 🤖 Claude *(21:27:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09/supabase/functions/publish-social/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	
> 3	const corsHeaders = {
> 4	  "Access-Control-Allow-Origin": "*",
> 5	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 6	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 7	};
> 8	
> 9	Deno.serve(async (req) => {
> 10	  if (req.method === "OPTIONS") {
> 11	    return new Response("ok", { headers: corsHeaders });
> 12	  }
> 13	
> 14	  try {
> 15	    const authHeader = req.headers.get("Authorization");
> 16	    if (!authHeader?.startsWith("Bearer ")) {
> 17	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 18	        status: 401,
> 19	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 20	      });
> 21	    }
> 22	
> 23	    const body = await req.json();
> 24	    const { platform, content, social_account_id, scheduled_post_id, user_id: bodyUserId } = body;
> 25	
> 26	    if (!platform || !content) {
> 27	      return new Response(JSON.stringify({ error: "platform and content required" }), {
> 28	        status: 400,
> 29	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 30	      });
> 31	    }
> 32	
> 33	    const adminClient = createClient(
> 34	      Deno.env.get("SUPABASE_URL")!,
> 35	      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
> 36	    );
> 37	
> 38	    // Resolve caller identity:
> 39	    // - User JWT (frontend): auth.getUser() returns a user
> 40	    // - Service role (auto-publish cron): auth.getUser() returns null; trust user_id from body
> 41	    //   since Supabase infrastructure already validated the JWT signature
> 42	    const supabase = createClient(
> 43	      Deno.env.get("SUPABASE_URL")!,
> 44	      Deno.env.get("SUPABASE_ANON_KEY")!,
> 45	      { global: { headers: { Authorization: authHeader } } }
> 46	    );
> 47	    const { data: { user } } = await supabase.auth.getUser();
> 48	
> 49	    let userId: string;
> 50	    if (user) {
> 51	      userId = user.id;
> 52	    } else if (bodyUserId) {
> 53	      userId = bodyUserId;
> 54	    } else {
> 55	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 56	        status: 401,
> 57	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 58	      });
> 59	    }
> 60	
> 61	    let query = adminClient
> 62	      .from("social_accounts")
> 63	      .select("*")
> 64	      .eq("user_id", userId)
> 65	      .eq("platform", platform)
> 66	      .eq("is_active", true);
> 67	
> 68	    if (social_account_id) query = query.eq("id", social_account_id);
> 69	
> 70	    const { data: accounts, error: accError } = await query.limit(1).single();
> 71	    if (accError || !accounts) {
> 72	      return new Response(JSON.stringify({ error: `No active ${platform} account found` }), {
> 73	        status: 404,
> 74	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 75	      });
> 76	    }
> 77	
> 78	    const account = accounts;
> 79	
> 80	    // Refresh token if expired, then re-fetch account to get the new access_token
> 81	    if (account.token_expires_at && new Date(account.token_expires_at) < new Date()) {
> 82	      const refreshRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/refresh-social-token`, {
> 83	        method: "POST",
> 84	        headers: {
> 85	          "Content-Type": "application/json",
> 86	          Authorization: `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
> 87	        },
> 88	        body: JSON.stringify({ social_account_id: account.id }),
> 89	      });
> 90	      if (!refreshRes.ok) {
> 91	        return new Response(JSON.stringify({ error: "Token expired and refresh failed" }), {
> 92	          status: 401,
> 93	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 94	        });
> 95	      }
> 96	      // refresh-social-token updates the DB but does not return the token;
> 97	      // re-fetch to get the updated access_token
> 98	      const { data: refreshedAccount } = await adminClient
> 99	        .from("social_accounts")
> 100	        .select("access_token, refresh_token, token_expires_at")
> 101	        .eq("id", account.id)
> 102	        .single();
> 103	      if (refreshedAccount) {
> 104	        account.access_token = refreshedAccount.access_token;
> 105	        account.token_expires_at = refreshedAccount.token_expires_at;
> 106	      }
> 107	    }
> 108	
> 109	    let result: any;
> 110	
> 111	    if (platform === "linkedin") {
> 112	      const res = await fetch("https://api.linkedin.com/v2/ugcPosts", {
> 113	        method: "POST",
> 114	        headers: {
> 115	          Authorization: `Bearer ${account.access_token}`,
> 116	          "Content-Type": "application/json",
> 117	          "X-Restli-Protocol-Version": "2.0.0",
> 118	        },
> 119	        body: JSON.stringify({
> 120	          author: `urn:li:person:${account.platform_user_id}`,
> 121	          lifecycleState: "PUBLISHED",
> 122	          specificContent: {
> 123	            "com.linkedin.ugc.ShareContent": {
> 124	              shareCommentary: { text: content.text || content },
> 125	              shareMediaCategory: "NONE",
> 126	            },
> 127	          },
> 128	          visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" },
> 129	        }),
> 130	      });
> 131	      result = await res.json();
> 132	      if (!res.ok) {
> 133	        console.error("LinkedIn publish error:", res.status, result);
> 134	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 135	      }
> 136	
> 137	    } else if (platform === "instagram") {
> 138	      const igAccountId = account.platform_user_id;
> 139	      const createRes = await fetch(
> 140	        `https://graph.facebook.com/v19.0/${igAccountId}/media`,
> 141	        {
> 142	          method: "POST",
> 143	          headers: { "Content-Type": "application/json" },
> 144	          body: JSON.stringify({
> 145	            caption: content.text || content,
> 146	            image_url: content.image_url,
> 147	            access_token: account.access_token,
> 148	          }),
> 149	        }
> 150	      );
> 151	      const container = await createRes.json();
> 152	      if (!createRes.ok) {
> 153	        console.error("Instagram media create error:", createRes.status, container);
> 154	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 155	      }
> 156	
> 157	      const pubRes = await fetch(
> 158	        `https://graph.facebook.com/v19.0/${igAccountId}/media_publish`,
> 159	        {
> 160	          method: "POST",
> 161	          headers: { "Content-Type": "application/json" },
> 162	          body: JSON.stringify({
> 163	            creation_id: container.id,
> 164	            access_token: account.access_token,
> 165	          }),
> 166	        }
> 167	      );
> 168	      result = await pubRes.json();
> 169	      if (!pubRes.ok) {
> 170	        console.error("Instagram publish error:", pubRes.status, result);
> 171	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 172	      }
> 173	
> 174	    } else if (platform === "facebook") {
> 175	      const pageId = account.platform_user_id;
> 176	      const res = await fetch(
> 177	        `https://graph.facebook.com/v19.0/${pageId}/feed`,
> 178	        {
> 179	          method: "POST",
> 180	          headers: { "Content-Type": "application/json" },
> 181	          body: JSON.stringify({
> 182	            message: content.text || content,
> 183	            access_token: account.access_token,
> 184	          }),
> 185	        }
> 186	      );
> 187	      result = await res.json();
> 188	      if (!res.ok) {
> 189	        console.error("Facebook publish error:", res.status, result);
> 190	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 191	      }
> 192	
> 193	    } else if (platform === "twitter") {
> 194	      const res = await fetch("https://api.x.com/2/tweets", {
> 195	        method: "POST",
> 196	        headers: {
> 197	          Authorization: `Bearer ${account.access_token}`,
> 198	          "Content-Type": "application/json",
> 199	        },
> 200	        body: JSON.stringify({
> 201	          text: content.text || content,
> 202	        }),
> 203	      });
> 204	      result = await res.json();
> 205	      if (!res.ok) {
> 206	        console.error("Twitter publish error:", res.status, result);
> 207	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 208	      }
> 209	
> 210	    } else {
> 211	      return new Response(JSON.stringify({ error: `Publishing to ${platform} not yet supported` }), {
> 212	        status: 400,
> 213	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 214	      });
> 215	    }
> 216	
> 217	    if (scheduled_post_id) {
> 218	      await adminClient
> 219	        .from("scheduled_posts")
> 220	        .update({
> 221	          status: "published",
> 222	          published_at: new Date().toISOString(),
> 223	          platform_post_id: result.id || result.data?.id || result["X-RestLi-Id"],
> 224	        })
> 225	        .eq("id", scheduled_post_id);
> 226	    }
> 227	
> 228	    return new Response(JSON.stringify({ success: true, result }), {
> 229	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 230	    });
> 231	  } catch (err) {
> 232	    console.error("publish-social error:", err);
> 233	    return new Response(
> 234	      JSON.stringify({ error: "Falha ao publicar. Tente novamente em instantes." }),
> 235	      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 236	    );
> 237	  }
> 238	});
> 239	
> ```

## 🤖 Claude *(21:27:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/beautiful-dijkstra-207b09\necho \"=== social_credentials table definition (search migrations) ===\" && grep -rl \"social_credentials\" supabase/migrations/ | head -3\necho \"=== how tokens are stored (column defs around social_credentials) ===\" && grep -rn -A3 \"CREATE TABLE.*social_credentials\" supabase/migrations/ | head -30\necho \"=== the higgsfield 'encrypt' match (is it real pgsodium?) ===\" && grep -n -iE \"pgsodium|vault|encrypt|crypto\" supabase/migrations/20260527005356_user_api_keys_higgsfield.sql",
  "description": "Read user_api_keys migration, publish-social fn, social_credentials storage pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === social_credentials table definition (search migrations) ===
> === how tokens are stored (column defs around social_credentials) ===
> === the higgsfield 'encrypt' match (is it real pgsodium?) ===
> 2:-- Description: Add higgsfield_api_key column to user_api_keys (per-user vault).
> 19:  IS 'Higgsfield platform API key secret (per-user pair with higgsfield_api_key). NULL falls back to global vault.';
> ```

## 🤖 Claude *(21:28:14)*


## 🤖 Claude *(21:28:19)*

Critical reconciliation found — this is a fork I should not improvise past.

**The conflict:** The meta-api BoK (`NFR-META-001`, data-model col `long_lived_token_encrypted`) mandates **AES-256-GCM / pgsodium encryption at rest** for Meta tokens. But the *entire existing codebase* stores OAuth tokens as **plaintext TEXT protected by RLS only** — `social_accounts.access_token`, `user_api_keys.groq_api_key`, etc. There is **zero pgsodium/Vault usage** in any migration (the one match was a comment). Meta page tokens are the *same class of secret* already sitting plaintext in `social_accounts`.

So encrypting *only* `meta_config` while `social_accounts` stays plaintext is security theater (same tokens leak via the older table). Since you're the **Owner of this security blast radius** (per the ORO triplet) and this is a documented BoK-vs-codebase conflict, I want your call before writing the migration:

## 🤖 Claude *(21:28:24)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Como armazenar os tokens OAuth da Meta em `meta_config`? (O resto do c\u00f3digo guarda token social como TEXT+RLS, sem cripto.)",
      "header": "Token storage",
      "multiSelect": false,
      "options": [
        {
          "label": "Match codebase + OTD",
          "description": "meta_config guarda tokens como TEXT protegido por RLS + GRANT column-level (id\u00eantico a social_accounts/user_api_keys). Registro OTD-META-ENCRYPT (AES/pgsodium at-rest) como d\u00edvida do PROJETO INTEIRO (cobre social_accounts tamb\u00e9m) com SLA, j\u00e1 que cifrar s\u00f3 meta_config \u00e9 teatro. Destrava publish-meta agora. \u00c9 como o projeto j\u00e1 trata OTDs de seguran\u00e7a."
        },
        {
          "label": "Cifrar at-rest agora (pgsodium)",
          "description": "Honra NFR-META-001 ao p\u00e9 da letra: habilita pgsodium/Vault, grava ciphertext em long_lived_token_encrypted, decifra no edge function. Lift de infra maior, inconsistente com o resto do c\u00f3digo (mesmo token j\u00e1 est\u00e1 plaintext em social_accounts), e n\u00e3o fecha o vazamento pela tabela antiga."
        }
      ]
    }
  ]
}
```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-05-30 - Fix API key leak and reconfigure model defaults]]
%% --- TIMELINE END --- %%

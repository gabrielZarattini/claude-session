# Refactor Core-v2 to Core-Fable
**Date:** 2026-06-10 | **Session ID:** `240db21b-cd40-4765-a3f4-345f03d2fc33`

---

## 👤 User *(01:40:53)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(01:40:53)*

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


## 🤖 Claude *(01:41:02)*


## 🤖 Claude *(01:41:02)*

Executando o ritual /handson — pre-flight em paralelo.

## 🤖 Claude *(01:41:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7 && echo \"---STATUS---\" && git status --short && echo \"---DIFFSTAT---\" && git diff HEAD --stat | tail -5 && echo \"---HANDOFF-LINES---\" && wc -l HANDOFF.md",
  "description": "Git history, status, diff stat, HANDOFF.md line count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> fe3bb5c docs(handoff): seal Cyber-Sentinel security — BoK 4/4 + prompt gate live + infra hardening
> f58bc52 docs(readme): v6.34.0 — Cyber-Sentinel: BoK segurança 4/4 + gate de prompt live + hardening de infra
> 6f2f75a feat(security): Cyber-Sentinel — gate de prompt em produção + hardening de infra
> cf682b8 chore(sprint): registra v6.33.1 hotfix Kanban ScrollArea + E2E + diretiva CISO deferida
> ea7704b docs(handoff): seal kanban-scrollarea-fix + E2E a prova de Cloudflare
> e5b172b docs(readme): v6.33.1 — hotfix Kanban ScrollArea + E2E logado a prova de Cloudflare
> 6b1571a docs(bok): adiciona blueprint de hardening de seguranca (diretiva CISO deferida)
> ---STATUS---
> ---DIFFSTAT---
> ---HANDOFF-LINES---
> 7545 HANDOFF.md
> ```

## 🤖 Claude *(01:41:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20; echo \"TSC_EXIT=$?\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> TSC_EXIT=0
> ```

## 🤖 Claude *(01:41:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat || echo \"CHROMA_UNREACHABLE\"",
  "description": "Docker mesh containers + Chroma heartbeat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_claude_mem: Up 19 minutes (healthy)
> mcorch_chroma: Up 19 minutes (healthy)
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1781055665702974861}
> ```

## 🤖 Claude *(01:41:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch clean\"; echo \"---BOK-GATE---\"; for slug in $(ls docs/bok/ 2>/dev/null); do required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics); missing=(); for doc in \"${required[@]}\"; do [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\"); done; [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"; done",
  "description": "BoK suites completeness check + scratch dir"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
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
> viral-daily-canvas
> viralmind
> ---SCRATCH---
> ⚠️ scratch/ has files
> ---BOK-GATE---
> ✅ agentic-workspace — BoK complete
> ✅ aios-sql-bridge — BoK complete
> ✅ authenticated-browser-operator — BoK complete
> ✅ canvas-design — BoK complete
> ✅ constellation-v2 — BoK complete
> ✅ conteudo-v2 — BoK complete
> ✅ e2e-user-zero — BoK complete
> ✅ gamificacao-nodes — BoK complete
> ✅ identity-fabric — BoK complete
> ✅ marketing-hub — BoK complete
> ✅ mcorch-constellation — BoK complete
> ✅ mcorch-qa-healing — BoK complete
> ✅ mercado-livre-api — BoK complete
> ✅ meta-api — BoK complete
> ✅ openclaw — BoK complete
> ✅ post-engine — BoK complete
> ⚠️ security — missing: 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> ✅ viral-daily-canvas — BoK complete
> ✅ viralmind — BoK complete
> ```

## 🤖 Claude *(01:41:09)*


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
> 14	## Session Seal — Cyber-Sentinel Security: BoK 4/4 + Prompt Gate Live + Infra Hardening (2026-06-10)
> 15	
> 16	Diretiva CISO ("MCORCH Cyber-Sentinel") executada em duas fases na mesma sessão: **Fase 1** gerou a suíte BoK de segurança 4/4 a partir do blueprint `00-deepsearch-blueprint.md` (semente de v6.33.1); **Fase 2** aplicou os patches no ecossistema vivo — com **review adversarial** antes de qualquer deploy quente, que pegou 4 bugs reais. O gate fail-closed contra prompt injection / bypass de billing está **materialmente ativo em produção**.
> 17	
> 18	**O que foi entregue:**
> 19	1. **BoK de segurança 4/4 (`docs/bok/security/`)** — `01-brd` (12 BR-SEC + Risk Ledger em R$ + Brand Protection Yachtmax/OKEAN), `02-srs` (15 FR-SEC + matriz RLS canônica integral + pooling `SET LOCAL`), `03-sdd` (lefthook+gitleaks · Husky monorepo · Arcjet · sentinel Deno · Dockerfile UID 1001 · compose `cap_drop` — tudo integral), `04-fmea` (12 modos de falha com RPN AIOS; FM-04/FM-05/FM-08 ancorados em incidentes reais deste repo).
> 20	2. **Sentinel LIVE em `orchestrate-content` (prod v52, `6f2f75a`)** — `_shared/sentinel.ts` (L1 estrutura · L2 injeção léxica/ANSI · L3 rate opt-out p/ fan-out targets) inspeciona o tópico **depois da identidade, antes do `deduct_mco_coins`**. Provado em produção: exploit com JWT real → `HTTP 403 {"layer":"sentinel"}` score=3, débito inalcançável (zero mcoCoins). 11 testes do sentinel + suíte total **295 passed**.
> 21	3. **Infra recriada e endurecida** — `mcorch_claude_mem` → `uid 1001 + read_only + 8 caps + 512M` (healthy, lock do bootstrap presente sob read_only); `mcorch_chroma` → caps conservadoras + `no-new-privileges` + 1G (heartbeat vivo, healthy); imagem `gitnexus` multi-stage não-root buildada (uid 1001/npm stripped/tini). Env `SUPABASE_SERVICE_ROLE_KEY` (revogada no cutover 2026-06-01) removida do compose (FM-04). O `name:` que orfanaria os containers foi removido após dry-run de verificação.
> 22	4. **Gate git dual-engine** — `lefthook` (devDep) + `gitleaks` (ARM64 em `/usr/local/bin`) no pre-commit/pre-push, com `secret-scan.sh` soberano portado + tripwire e2e + `.gitleaks.toml`. Degradação graciosa quando gitleaks falta (OTD-SEC-003). Provado: bloqueia segredo plantado (exit 1), passa árvore limpa (exit 0).
> 23	
> 24	**Review adversarial (4 bugs reais capturados antes de deploy):** (a) rate-limiter L3 falsava o fan-out paralelo de `campaign-run`/`intent-execute` → `rateLimit:false` para targets; (b) `cap_drop SETUID/SETGID` via âncora quebraria o `chroma` de terceiros (root) → perfil conservador; (c) regex de 1 qualificador deixava "ignore all previous instructions" passar → qualificadores encadeados; (d) guard `&&||` do gitleaks engolia a detecção → `if/then/else`.
> 25	
> 26	**ORO:** Operator=MCORCH Agent (Cyber-Sentinel) · Reviewer=Sovereign (GO no sentinel + "verificar corretamente os 2 pontos") · Owner=Sovereign (path de billing prod + malha soberana + containers).
> 27	
> 28	| Verificação | Resultado |
> 29	|---|---|
> 30	| Commits | `6f2f75a` (security patch) · `f58bc52` (readme) · handoff (este) |
> 31	| Deploy | ✅ `orchestrate-content` v51→**v52** (112.2kB, exit 0) |
> 32	| G4 exploit prod | ✅ `403 layer=sentinel score=3`, zero mcoCoins gasto |
> 33	| Containers | ✅ claude_mem (uid1001/read_only/8caps) + chroma (3 caps conservadoras) healthy |
> 34	| Gate git | ✅ bloqueia segredo (exit 1, dual-engine) · árvore limpa exit 0 |
> 35	| tsc / Suíte | ✅ 0 erros · **295 passed** · 2 skipped |
> 36	| Handoff node | ✅ `0a9865a9-202c-4aae-ab42-d1500cdbc261` (embedded 768d) · mesh **8861** |
> 37	
> 38	### Arquitetura do gate
> 39	```
> 40	orchestrate-content (verify_jwt=false)
> 41	  getUser() [identidade ES256] → topic parse
> 42	    └── inspectPrompt(topic, user.id, {rateLimit:false})   ← FR-SEC-002, fail-closed
> 43	          allow=false → logSentinelBlock + 403 {layer:sentinel}   (zero LLM, zero débito)
> 44	          allow=true  → deduct_mco_coins (10) → pipeline
> 45	```
> 46	
> 47	**Pendências/Próximos:**
> 48	- **FM-10 (gitnexus root):** imagem endurecida buildada e pronta; aplicar quando o gitnexus for containerizado (hoje roda em stdio). OTD-SEC-005.
> 49	- **OTD-SEC-001:** `middleware.ts` Arcjet aguarda superfície Next/BFF (hoje Vite/nginx); a camada viva é o sentinel Deno (§3.2).
> 50	- **OTD-SEC-006/007:** fiar sentinel + migration `security_events`/quarentena (<50ms) nas demais funções pagas; promover lefthook a hook canônico em todas as máquinas.
> 51	
> 52	### Survival Laws Self-audit
> 53	```
> 54	Law 1 (Materiality): ✅ Tudo ancorado — deploy v51→v52 literal (112.2kB exit 0); G4 prod 403 layer=sentinel score=3 (JWT real, zero gasto); containers inspecionados (uid/caps/heartbeat literais); suíte 295 passed; node 0a9865a9 embedded 768d. Bugs do review provados por teste antes/depois (suíte 295). NÃO rodei orchestrate pago benigno (cobraria) — pass-through provado só local (declarado).
> 55	Law 2 (Process): ✅ BoK 4/4 ANTES da aplicação (Master Protocol). SOPs OTD-SEC-001..007 registradas no SDD/FMEA. Dois bugs viraram correção+doc-sync na mesma sessão (anti-drift FM-03).
> 56	Law 3 (Pruning): ✅ Verificação read-only antes de cada ação destrutiva (dry-run dos containers, pre-scan do gate). Janela usada densamente; seal puxado só após GO A>B do Sovereign.
> 57	Law 4 (ORO): ✅ Triplet declarado; Owner=Sovereign (billing prod + containers + malha).
> 58	```
> 59	
> 60	---
> 61	
> 62	## Session Seal — Kanban ScrollArea Hotfix + E2E à Prova de Cloudflare (2026-06-09)
> 63	
> 64	`/handson` → bug report do Sovereign no `/dashboard/kanban`: `ReferenceError: ScrollArea is not defined` que começou **depois de criar uma coluna**. Diagnóstico → fix → E2E completo → incidente de concorrência resolvido.
> 65	
> 66	**O que foi entregue:**
> 67	1. **Fix do crash do Kanban (`e55ce70`)** — `KanbanPage.tsx` usava `<ScrollArea>` (área scrollável de tarefas, linha 369) mas **nunca importava o componente**. Por isso só quebrava *depois* de criar a 1ª coluna: o empty-state não chega a renderizar o `ScrollArea`; assim que `columns.map` rende uma coluna → `ReferenceError` → derruba a árvore React. Fix de **uma linha**: `import { ScrollArea } from "@/components/ui/scroll-area"`. Deploy material verificado (repo principal, build=deploy): chunk novo `KanbanPage-CW7WBYjZ.js` ≠ `KanbanPage-Cc6x-1KC.js` (o do stack trace), `import "./scroll-area-CoDzX65f.js"` baked, env Supabase presente (9 arquivos). **Confirmado em produção pelo print do Sovereign** (coluna renderiza, zero crash).
> 68	2. **E2E completo do Workspace Kanban** — Cloudflare Turnstile barra o `agent-browser` de IP de datacenter **até no `login.mcorch.com`** (não só portal ML), e o `action_link` do magic-link dá `otp_expired` no challenge. Solução: E2E contra **preview local do `dist`** (mesmo artefato, sem CF) + sessão real injetada no `localStorage`. Exercitado: carregar (sem crash, `scrollAreaViewports` montados) → criar coluna (a ação que quebrava) → criar tarefa → **drag-drop bidirecional**. Persistência **provada pelo banco** (3× `PATCH 200` + SELECT ground-truth: `in_progress`/`todo` + `column_id` corretos), nunca pelo DOM.
> 69	3. **Helper `gen-user-session.ts` (`761ea6f`)** — minter de sessão Supabase (`Admin generateLink`→`verifyOtp`) que emite o valor de `localStorage` injetável; contorna o trap magic-link-single-use + Turnstile. Estende a linhagem `gen-magiclink`/`gen-user-jwt`.
> 70	4. **Blueprint CISO de segurança (`6b1571a`)** — `docs/bok/security/00-deepsearch-blueprint.md` commitado como semente da suíte BoK de hardening. **Diretiva interrompida pelo Sovereign em favor deste seal → geração dos 4 artefatos (01-brd/02-srs/03-sdd/04-fmea) DEFERIDA.**
> 71	
> ```

## 🤖 Claude *(01:41:10)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-65 of 213 total (47670 tokens, cap 25000). Call Read with offset=66 limit=65 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.33.1 — Hotfix Kanban ScrollArea + E2E à Prova de Cloudflare (2026-06-09)** — bug report do Sovereign no `/dashboard/kanban`: `ReferenceError: ScrollArea is not defined` ao criar coluna. **Causa:** `KanbanPage.tsx` usava `<ScrollArea>` (área scrollável de tarefas) sem importar — só quebrava *depois* da 1ª coluna (empty-state não exercita o componente). **Fix de 1 linha** (`e55ce70`): import `@/components/ui/scroll-area`; deploy material (chunk novo `KanbanPage-CW7WBYjZ.js` ≠ o do stack trace, import scroll-area + env baked); **confirmado em prod pelo print do Sovereign**. **E2E completo** via preview local do `dist` + sessão injetada (CF Turnstile barra agent-browser do datacenter até no `login.mcorch.com`): CRUD + drag-drop bidirecional **provado pelo DB** (3× PATCH 200 + SELECT, não pelo DOM). Helper `gen-user-session.ts` (`761ea6f`) p/ E2E logado à prova de CF. **Incidente de concorrência** (Sovereign mexendo em prod junto) resolvido sem perda de dado — board/coluna intactos, a "divergência" da 1ª rodada era o Sovereign movendo o mesmo card. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8860** · handoff `fd20b125`. **Lição:** E2E mutável vai em board descartável, nunca no dado real do Sovereign; DB-prod é compartilhado. **Diretiva CISO de hardening DEFERIDA** (blueprint `6b1571a` commitado; 4 artefatos BoK de segurança p/ sessão dedicada).
> 8	
> 9	**Sprint v6.33.0 — ML Attribution Fix + Browser Operator BoK (2026-06-08)** — o teste **real** do Sovereign no branded link expôs o flywheel emitindo link **MORTO**. **(1) Fix do auto-monetize** (`34d7ef0`): `_shared/affiliate.ts` `buildMlProductUrl` montava o formato BARE `mercadolivre.com.br/MLB-<id>` (404) com 2/3 ids stale → agora resolve `vm_affiliate_products.product_url` real (fonte única Apify), fail-open `/p/`; **reconcilia "ML não conta clique"** (era 404, não falha do matt_word — o painel ML já contara matt_word em produto VÁLIDO em 2026-06-04); provado E2E `7993c6a4` 302 → `/p/MLB27834876`; deploy `orchestrate-step` 122.8kB. **(2) BoK 9/9 do Operador de Browser Autenticado** (`/bok-scribe`, `24ba435`): suíte 756 LOC MR→SDD+STRIDE+FMEA; **gate pagou** — o link oficial é per-user → nova `user_affiliate_links` (não a `vm_affiliate_products.affiliate_template_url` COMPARTILHADA, que vazaria entre tenants — OTD-ABO-003); runtime residencial cravado (datacenter **403** reprovado em produto real `/p/`, bare e `/afiliados/hub`); mesh seal `31323fe3` + DERIVES_FROM edge `9ea18d26` → mercado-livre-api. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8852** · handoff `630509e2`. **Top Gap:** **BUILD do Operador** (gate ABERTO; runtime residencial = Sovereign roda `agent-browser` logado no ML) · domínio Resend · conversão ML real. **Lição:** o teste por **mão do Sovereign** (clicks 0→4) achou o link morto que meu curl-403 do datacenter mascarava; o BoK-first pegou o vazamento cross-tenant **antes** do código.
> 10	
> 11	**Sprint — Stored-XSS Hardening + Antibody (2026-06-08)** — `/security-review` (v6.28.0) havia flagado stored-XSS em `DashboardHome` (`content_library.body` cru via `dangerouslySetInnerHTML`); fechado **ponta-a-ponta** nesta sessão. Sanitização `DOMPurify.sanitize` (já shipada via Antigravity em `da9da4c`/`e5a661a`) + guarda de regressão **6 testes** (`dashboard-html-sanitize.test.ts`: preserva `<a href>` de afiliado + tags de artigo, remove `<script>`/`onerror`/`javascript:`) + **antibody ESLint `no-restricted-syntax`** (`2522e71`, sem dep nova — `eslint-plugin-react` ausente) que faz todo `dangerouslySetInnerHTML` futuro acusar no lint até ser sanitizado+justificado (sink cru plantado → **pego** material; 2 sinks legítimos justificados: DashboardHome DOMPurify · chart.tsx CSS shadcn) + limpeza dos **7 `no-explicit-any`** do data-layer de DashboardHome (`3129369`). Handoff node `e12ed58e` + obs antibody `505fb670` (embedded 768d). tsc 0 · suíte verde · mesh **8849**. **Anticorpo Permanente cumprido** — reincidência do sink barrada no lint. **Top gaps restantes (herdados de v6.28.0, gated no Sovereign):** domínio `RESEND_FROM` (entrega Resend real) · branded redirect `login.mcorch.com/go` · 2 rascunhos WP de teste · atribuição de compra ML.
> 12	
> 13	**Sprint v6.32.x — arco Core-v2 Black Hole (2026-06-07, via Antigravity)** — sessões conduzidas no Antigravity, seladas e versionadas no git, registradas aqui retroativamente a partir dos records do HANDOFF.md (não reauditadas em detalhe — Lei 1): **v6.32.6** Unified Relativistic Black Hole & Cymatics (fusão dos visualizadores num único shader WebGL Schwarzschild — raymarching + disco de acreção + Doppler beaming + ondas de cymatics; layout 30/70; `CymaticsLayer` removido; 284 testes; handoff `ec6204a4`; mesh 8847); **v6.32.5** Model Selector Fix & Reacting Black Hole (fix case-collision dos hooks `useAiosTerminalChat`/`useAiosWorkspaceChat`; persistência do modelo selecionado em `user_api_keys`; redesign MegaBrainVisualizer + CymaticsLayer; 260 testes; handoff `8627661a`; mesh 8839); **v6.32.2** Gemini 3.1 Live Mode (Live API → Gemini 3.1 Flash Live audio-only + Gemini Docs MCP + API Skills; handoff `5acba7aa`; mesh 8818). Os seals intermediários (v6.29–v6.32.4) existem em HANDOFF.md/README mas não foram back-filled aqui.
> 14	
> 15	**Sprint v6.28.0 selado em 2026-06-04** — **Quatro next-steps fechados numa sessão (probe-first)**. Diretiva Sovereign "ataque os 4 pontos numa sessão só, não pare até terminar; o ponto 4 do link não funcionou a contabilidade de clicks" (+ screenshot ML com 1 clique). Cada gap verificado **no código** antes de tocar. **(1) OTD-INTENT-DISPATCH-REFUND FECHADA:** `orchestrate-content` estorna os 10 em falha pós-débito (`!runId` ou erro do kick `async_orchestrate_step`) + marca run `error` — estende o contrato refund da v6.27.2 ao núcleo do flywheel. **(2) nurture-dispatch entrega Resend real (FR-MH-008):** resolve `resend_api_key` per-user (BYOK) + `leads.contact` → POST Resend quando email+chave+endereço; senão `gated`; send `failed` estorna. Live a inbox real ainda gated em `RESEND_FROM` (domínio Sovereign). **(3) Click ledger in-system (OTD-ML-CLICKS):** links publicados passam pelo redirect `process-affiliate-link` GET, que registra o clique atômico (RPC `record_affiliate_click` service-role-only, atribuído ao dono) + 302 pro ML; `link-forge` emite o redirect; **ROIWidget já soma `affiliate_links.clicks`** → "Cliques Totais" reflete cliques reais antes de compra; migration 120000 + fix 130000 (`content_id` UUID). **(4) 1º dispatch pago E2E agentic:** intent→policy→execute→orchestrate-content WP **draft**, run `43048d8e` **done**, **delta 10 exato** (valida ponto 1 em prod), HITL gate provado, blast-radius wordpress-only. **Prova:** `/security-review` independente **SAFE** · drift audit **exit 0** · smoke-affiliate-click **10/10** + smoke-nurture **10/10** · suíte **269** · tsc 0 · deploys 107.9/83.72/87.96kB · Phase 5c **SEAL ALLOWED** (7 verified) · Mesh **8783**. 6 commits. **Novo Top Gap:** entrega Resend a inbox real (domínio `RESEND_FROM` — Sovereign) · branded redirect domain (`login.mcorch.com/go` proxy nginx — link limpo+rastreado) · 2 rascunhos WP de teste a limpar · atribuição de compra ML (aguardando conversão). **Lição:** probe-first economizou retrabalho (ROIWidget já somava clicks → zero UI nova; `resend_api_key` já existia → só o canal) e pegou o bug 22P02 do RPC (content_id UUID) no smoke antes de declarar — corrigi via migration na mesma sessão (regra hotfix→migration). **Follow-up (mesma sessão, "continue com os próximos"):** click ledger estendido ao caminho **interativo** de monetização — POST `process-affiliate-link` retorna redirect rastreável `?link_id` (migration `20260604140000` + RPC `record_affiliate_click_by_link`). O smoke estendido (G8) expôs um insert de `affiliate_links` quebrado há tempo (`campaign_id` UUID vs slug `"ai_orchestration"` → 22P02 silencioso, nenhuma linha de afiliado nunca persistida) + o `/security-review` independente pegou um **open-redirect** no branch novo (302 pro `short_url` tenant-writável) — ambos corrigidos (gate de domínio ML + UUID-só); smoke **9/9** (G9 prova o open-redirect bloqueado), commit `b2c39f6`. **Follow-up 2 ("faça todos os 3"):** (A) **auto-monetização** no `orchestrate-step` — o artigo gerado embute o redirect rastreável `?link_id` per-owner (`_shared/affiliate.ts`), o flywheel monetiza+rastreia automático; provado E2E pago run `cee55b11` (Roborock → link rastreável no `content_mesh_asset`). (B) **matt_tool** per-user (coluna `affiliate_config` + threading GET/POST/orchestrate + UI `AffiliatesPage`; caveat honesto: efeito na atribuição ML não-verificável, mas aditivo). (C) **campaign-run assíncrono** p/ >8 passos (`EdgeRuntime.waitUntil`, batches; pequenas seguem síncronas). `/security-review` independente **SAFE** (flagou XSS **pré-existente** `DashboardHome:677` dangerouslySetInnerHTML → tarefa spawned). Smokes click **G1-G9+G1b** · campaign **A-H** · e2e auto-monetize ✅ · tsc 0 · drift exit 0. 4 commits (`9bb5bba`/`bb999c1`/`7cbd036`/`b468c98`).
> 16	
> 17	**Sprint v6.27.2 selado em 2026-06-04** — **Refund-on-failure: charge-without-value fechado (OTD-AEO-REFUND)**. Diretiva Sovereign "continue com os próximos passos". Probe-first material elegeu o item de **menor blast radius e maior valor seguro** dos 3 next-steps (refund protege saldo do usuário, zero ação outward); os outros 2 dependem do Sovereign (nurturing externo precisa de domínio Resend verificado — **zero refs RESEND no código**; 1º pago E2E precisa de GO econômico). **OTD-AEO-REFUND FECHADA:** `aeo-audit` debitava 5 mco na entrada e, se o persist falhasse, devolvia 500 **sem estornar** (charge-without-value, verificado no código). Helper compartilhado **`refundMco`** (`_shared/billing.ts` → `add_mco_coins`, service-role-only, simétrico a deduct, guarda `p_amount>0`, nunca lança); `aeo-audit` (5) e `lead-score` (1) rastreiam `charged` e estornam em qualquer falha pós-cobrança (persist-fail + catch). **Prova:** smoke `smoke-aeo-refund.ts` **6/6 LIVE** (deduct 5→15 / add 5→20 restaurado · guarda nega -10 · net-zero) + unit `_shared/billing.test.ts` **4/4** + regressão aeo-audit intacta. **Honestidade Lei 1:** persist-fail não é forçável por input → fiação coberta por unit+code, não por falha forçada (declarado). Contrato refund-on-failure no billing SSOT (`mcoin-cost-calibration.md`). Deploys 86.69/85.62kB · tsc 0 · suíte **269** (265→269) · Phase 5c **SEAL ALLOWED** (8 verified) · Mesh **8774** (1 órfão `aeo:` podado). 3 commits. **Novo Top Gap:** entrega externa de nurturing (bloqueada por domínio Resend — Sovereign) · 1º pago E2E (GO econômico) · **OTD-INTENT-DISPATCH-REFUND** = aplicar `refundMco` ao gap pós-débito do `orchestrate-content` (flywheel, sessão dedicada). **Lição:** probe-first descartou 2 dos 3 next-steps (dependência externa) e leu o código pra confirmar que o gap de refund era REAL (linha 56 débito → 118 persist-fail sem refund) antes de construir — não assumi o bug, verifiquei.
> 18	
> 19	**Sprint v6.27.1 selado em 2026-06-03** — **Intent executor un-gated: dispatch outward REAL + OTD-INTENT-TRANSITION-GUARD**. Diretiva Sovereign "ACTIVATE AGENTIC OUTWARD EXECUTION" (Step 1 guard ANTES do Step 2 dispatch). **(1) OTD-INTENT-TRANSITION-GUARD (migration `20260603270000`):** trigger `tr_guard_intent_plan_transition` (`SECURITY DEFINER`/`search_path=''`) deixa **só `service_role`** colocar uma linha em `status='approved'`/`'executed'`. **O `/security-review` (subagente independente) pegou que meu guard inicial era BEFORE UPDATE-only → vetor INSERT aberto** (tenant `POST intent_plans {status:'approved'}` pulava o HITL e cavalgava a re-validação até dispatch). Estendi p/ **BEFORE INSERT OR UPDATE** + endureci a RLS `insert_own` (`status IN proposed/auto_approved/pending_hitl`) + `tr_validate_intent_plan_bindings` (binding = mesmo tenant). **Prova material before/after**: INSERT `status='approved'` por JWT de tenant → **201 ANTES / 403+42501 DEPOIS**. **(2) Dispatch outward REAL (un-gate):** `intent-execute` pós-`executed` roteia por precedência — `campaign_id`→campaign-run · `enrollment_id`→nurture-dispatch · senão canais content/social/affiliate→orchestrate-content — encaminhando o **JWT do chamador** (cascata self-bila o mesmo tenant). Kill-switch `INTENT_OUTWARD_DISPATCH_ENABLED=false`→governança-only. Idempotência: marca executed 1º (re-execute=already, sem dobro de dispatch/cobrança). `db push` Finished · types regen · deploy 83.01kB. **Smoke 28/28 LIVE throwaway** (guard INSERT+UPDATE 42501 · golden rule · dispatch REAL provado por **downstream guard a saldo 0**: orchestrate-content **402** + campaign-run **422**, zero gasto · binding foreign rejeitado). tsc 0 · eslint 0 · suíte **265** · drift audit **exit 0**. BoK patcheada (SDD + data-model) + SOP reescrita (gates 4/5/6 + OTD-INTENT-DISPATCH-REFUND). **Novo Top Gap:** entrega externa real de nurturing (gated; `resend_api_key` pronto) · **OTD-INTENT-DISPATCH-REFUND** (refund pós-dispatch-fail) · 1º dispatch pago E2E real (gated em GO Sovereign — UI HITL + guard já armados). **Lição:** o `/security-review` independente pegou o furo INSERT que o self-review (focado no PATCH) deixou passar — exatamente o vetor que a diretiva mandava fechar; provar before/after material (201→403) separa "guard escrito" de "guard que funciona" (Lei 1).
> 20	
> 21	**Sprint v6.27.0 selado em 2026-06-03** — **Marketing-Hub: rosto + executor + AEO (FR-MH-009/010)**. `/handson` → `/goal` Sovereign com os 3 próximos passos ("backend pronto, falta o rosto"). **(1) Executor de `intent_plans` (FR-MH-009 HITL):** edge fn `intent-execute` (approve/reject/execute) na máquina `proposed→pending_hitl→approved|rejected→executed`; **golden rule** = o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** (gate compartilhado `_shared/intent-policy.ts`) e recusa `409 hitl_required` todo outward sem aprovação humana — **nunca confia em `auto_approved`**; tenant-guard 404; `/security-review` SAFE → adotada **fail-closed** em plano não-array; smoke **17/17**. **(2) AEO (FR-MH-010 — última FR):** `aeo_audits` (RLS) + `aeo-audit` (JWT · 5 mco atômico · provider **degradado documentado** OTD-MH-003 LLM-as-answer-engine · 1 snapshot/query); `db push` Finished; smoke **12/12** (RLS cross-tenant leaked=0). **(3) UI follows:** `useIntentOrchestrator`/`useAEO` + `IntentOrchestratorPanel`/`HITLApprovalCard`/`AEOAuditPanel` + enroll de nurturing no Customer 360 → `/dashboard/marketing`; **+8 testes (257→265)**; **UI logada verificada** (magic link Usuário Zero + agent-browser, chunk novo, zero crash). tsc 0 · eslint 0 (tocados) · build 22.88s deploy nginx. 5 commits. **Novo Top Gap:** dispatch outward real do executor (hoje gated) + **OTD-INTENT-TRANSITION-GUARD** (CHECK de transição antes de ligar o envio real) · entrega externa de nurturing (gated; credencial pronta) · **OTD-AEO-REFUND** (refund pós-débito). **Marketing-hub: TODAS as FRs backend+UI entregues** (001..012). **Lição:** probe-first viu que o gate de policy já existia inline no orchestrate → extraí p/ `_shared` em vez de duplicar (o `execute` re-roda **o mesmo** gate, não uma cópia); o `/security-review` independente pegou o fail-open que o self-review deixaria passar.
> 22	
> 23	**Sprint v6.26.0 selado em 2026-06-03** — **Drift audit + P0 ledger + 3 FRs marketing-hub**. `/handson` → diretiva Sovereign "🔴 auditar drift deployado↔migrations" (irmãos do hotfix `async_orchestrate_step`) → "faça 2+3+4". **(1) Drift audit:** 9 superfícies via Management API read-only (ledger 96==96 · contrato RPC 12/12 · verify_jwt edge 23==23 · 34 triggers · RLS toda-tabela · pg_net siblings) → **incidente ISOLADO**; único drift real `rls_auto_enable` (event-trigger out-of-band benigno que liga RLS em tabela nova) **capturado** + 6 SECURITY DEFINER `search_path` travado + trigger pg_net morto (kong:8000) dropado. Anticorpo `scripts/qa/audit-schema-drift.sh` (8 checagens, exit 0) + SOP `schema-drift-audit.md`. **(2) 🔴 P0 ledger:** os 3 RPCs (award/add_user_score/deduct) davam EXECUTE a anon/authenticated + confiavam `p_user_id` → cunhagem de mcoCoins via PostgREST direto; REVOKE (edge-only) + guardas em deduct (sinal + posse NULL-safe); **exploits provados BLOQUEADOS** em prod (erro/42501/permission denied). **(3) functionName 13/13** fallback LLM. **(4) FR-MH-008 cron** (`nurture-cron`+pg_cron `*/15`, modo service-role em nurture-dispatch; smoke 5/5+USER 10/10). **(5) FR-MH-012 BYOK** (`resend_api_key` per-tenant Vault — defs VIVAS verbatim — +Settings; round-trip 8/8). **(6) FR-MH-009 Intent+HITL backend** (`intent_plans`+`intent-orchestrate`: policy auto/HITL canal-outward-fail-safe + rationale XAI; smoke 8/8). 9 commits · 3 migrations · 4 deploys · `/security-review` independente por migration (todas SAFE) · Phase 5c **SEAL ALLOWED** (11 verified) · Mesh **8770** (orphan de smoke limpo) · Survival Laws **4/4**. **Novo Top Gap:** UI follows (enroll nurturing — hook já existe — + `useIntentOrchestrator`/`HITLApprovalCard`) · executor de `intent_plans` (re-validar ação outward no execute) · entrega externa nurturing (gated; credencial pronta) · FR-MH-010 AEO (última FR). **Lição:** probe-first viu que a metade-IA do FR-MH-012 já existia (só a metade-canal era nova) + evitou o trap do template stale de credenciais (reproduzir defs VIVAS, não migration antiga); o drift audit virou anticorpo reexecutável.
> 24	
> 25	**Sprint v6.25.0 selado em 2026-06-03** — **Flywheel ressuscitado + calibração mcoCoins**. `/handson` → diretiva Sovereign ("o que falta pro 1º run pago E2E + já calibrar o COIN_COST?"). Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados): **OTD-MCOIN-CALIBRATION FECHADA** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso=Enterprise); surpresa honesta — `10` (orchestrate) e `125` (canvas vídeo) **já** eram ~4× sobre custo real, único furo `IMAGE_GENERATION 3→9` (`CONTENT_GENERATION 5→2`). O **1º run pago E2E então expôs que o flywheel de conteúdo estava MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo run preso em `running`: **#1** `orchestrate-step` faltava no `config.toml` (`verify_jwt=true` → gateway **401** na chave opaca `sb_secret_` do pg_net); **#2** `async_orchestrate_step` hotfixada em prod **sem migration** (`p_service_jwt_legacy`≠`p_service_key` → **PGRST202** → auto-chain morto) → migration `20260603190000` realinha + `GRANT service_role`, `/security-review` SAFE, RPC **204**; **#3** `wp_site_url` não-www → **301 → POST vira GET** → WP devolve LISTA de posts → `publish-wordpress` endurecido (valida `id`, 502 honesto) + `wp_site_url→www`. **Provado E2E**: run `89f18bea` **auto-completou 6/6 passos sem kick** → rascunho WP `?p=14` + `content_mesh_asset` done. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8769**. Survival Laws **4/4**. 7 commits. **Novo Top Gap:** auditar **drift deployado↔migrations** (outras RPCs/fns hotfixadas em prod?) · limpar artefatos de teste (5 posts parqueados 2027 + 2 rascunhos WP) · FR-MH-009/010/012 + Nurturing follow-up · functionName nas 9 fns. **Lição:** o 1º run pago **não "falhou"** — fez seu trabalho: expôs 3 P0s silenciosos no coração do produto (falha sem erro visível, sem auto-refund); calibrar **antes** do run foi a decisão certa (transação econômica honesta).
> 26	
> 27	**Sprint v6.24.0 selado em 2026-06-03** — **Sessão de alta densidade** (diretiva Sovereign: selar a 45% é desperdício → usar a janela 1M inteira, selar só a ~95%; **Lei 3 recalibrada** em survival.md: poda≠selar). Resposta ao "faça os três, foco em endurecer o flywheel": 5 entregas pós-v6.23.0, cada uma com **smoke LIVE throwaway**. **(1) MVP-5 Atribuição (FR-MH-007)**: `handle-ml-postback`→`marketing_attribution` (campaign_id FK-safe, fail-soft) + `useCampaignAttribution`+card "Receita Atribuída"; smoke DB 4/4 (FK 23503 + de-linked). **(2) Hardening+observabilidade (FOCO)**: `eslint .` **honesto** (Deno `supabase/functions`+tailwind excluídos — ~3716 erros falsos, exit mascarado por `| tail`) + functionName telemetry no flywheel + smoke integração lead→score→campaign→attribution 5/5. **(3) Customer 360 (FR-MH-011)**: VIEW `security_invoker` RLS-safe + `useCustomer360`+drawer; /security-review SAFE + **isolation smoke 4/4** (B não vaza p/ A). **(4) Nurturing (FR-MH-008)**: engine `sequences`+`sequence_enrollments` (FK composta CASCADE) + `nurture-dispatch` **consent-gated** (envio gated) + `useNurturing`+`NurturingPanel`; /security-review SAFE + **consent-gate smoke 10/10**. 2 migrations /security-review SAFE (subagentes independentes) · tsc 0 · suíte **259** · eslint exit 0 honesto · 4 deploys · 5 smokes LIVE. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8761** (orphan obs de smoke limpo + smoke vacinado). Survival Laws **4/4**. 8 commits. **Novo Top Gap:** 1º run pago E2E (gated GO) · Nurturing follow-up (entrega externa real + cron + UI enroll/dispatch) · OTD-MCOIN-CALIBRATION · FRs restantes FR-MH-009/010/012. **Lição:** densidade máxima por sessão (5 frentes numa só) sem perda de materialidade — cada uma provada por smoke LIVE; o gate de lint estava mentindo (exit mascarado) — fix de raiz restaura honestidade da Lei 1.
> 28	
> 29	**Sprint v6.23.0 selado em 2026-06-03** — Marketing Hub backend completo + **MVP-4 UI live**: `campaign-run` (FR-MH-004) fechou o backend, depois o módulo inteiro ganhou rosto em `/dashboard/marketing` **absorvendo a UI v1** (não duplicando). **(1) campaign-run** JWT + débito atômico do FEE `CAMPAIGN_RUN` (10) → dispatch **paralelo** (`Promise.allSettled`) dos passos p/ `orchestrate-content` (self-bila 10) = **cascata fiel 10+10×N**; `email`→blocked; cap 8; smoke **13/13 zero-custo** (guards + isolamento de tenant + email-blocked + débito atômico 100→90 + cleanup); deploy 80.92kB; cascata paga **gated em GO**. **(2) MVP-4 UI**: `/dashboard/marketing` (LeadBoard 5 colunas + Pontuar/`lead-score` + overview campanhas; nav Target) + absorção v1 (`CampaignWizard` +Intenção/passo **Passos** composer→persiste `campaign_steps`; `CampaignDetail` +card **Passos & Execução** status vivo + `CampaignRunButton`). **(3) Hooks**: `useLeads`/`useLeadScore`/`useCampaignSteps`/`useCampaignRun`/`createCampaignWithSteps` + `src/lib/edge.ts`. tsc 0 · **11 testes** (suíte **255/257**) · eslint limpo nos tocados · build 22.32s deploy nginx · **UI LOGADA verificada** (magic link + agent-browser: `/dashboard/marketing` + wizard 6-passos/Passos renderizam, 0 erros console, zero mutação prod). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8760**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** 1º run pago E2E (Sovereign cria campanha→Rodar, gated em GO) · OTD-MCOIN-CALIBRATION ($) · OTD-CAMPAIGN-RUN-ASYNC (fila p/ campanha grande) · MVP-5 attribution→ROIWidget · **dívida de lint repo-wide** (~3716 erros pré-existentes em `supabase/functions` Deno, exit mascarado por `| tail` — não introduzidos nesta sessão). **Lição:** a diretiva Sovereign de calibração de contexto (1M/Max → não adiar por "contexto" antes de ~400k) destravou rodar o MVP-4 completo numa sessão; probe-first pegou a UI v1 existente ANTES de codar (absorver, não duplicar); a11y do agent-browser estava stale na transição framer-motion → li o stepper-text em vez de fabricar (Lei 1).
> 30	
> 31	**Sprint v6.22.0 selado em 2026-06-03** — Campaign Core + LLM Fallback + Lead Scoring: 4 entregas materiais via `/handson`→ação nos alertas→próximos priores. **(1) Alerta meta_config** verificado **VAZIO** (0 linhas · `auth.users` 1==`profiles` 1 — não fabriquei limpeza inexistente, Lei 1). **(2) MVP-2 Campaign Core LIVE** (migration `20260603025256`): `campaigns` **ABSORVIDA** via `ALTER` (+intent/channels/mesh_node_id + `UNIQUE(id,user_id)`) + `campaign_steps` (FK composta tenant-`CASCADE`, espelha lead_events) + `marketing_attribution` (FK simples `SET NULL` + RLS `WITH CHECK`, espelha consents); tenant-FK provado **comportamental** (23503 + 42501 autenticado + 201 + zero-resíduo); `/security-review` **SAFE** (subagente independente); mesh `7628892b`. **(3) OTD-LLM-FALLBACK FECHADA cedo** (SLA 06-07, owner engineer): probe-first achou o helper já live em 11 fns → fechei o gap de observabilidade do SOP (telemetria `infra_health_logs` autossuficiente em Deno) + **1º teste de edge-helper do projeto** (6 casos) + 11 fns redeploy; mesh `6061a6d2`. **(4) lead-score LIVE** (FR-MH-003): JWT + 1 mco atômico + IA per-user→sistema fail-soft; **smoke E2E** 200 · score=80 (`source=ai`) · débito 100→99 · zero-resíduo. **Calibração mcoCoins**: `COIN_COSTS` centralizado + dívida **OTD-MCOIN-CALIBRATION** (o `10` é redondo, não $-calibrado; `orchestrate` cobra 10 flat < soma dos componentes 18; vídeo é o maior custo real). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8759**. Survival Laws **4/4**. 6 commits. **Novo Top Gap:** `campaign-run` cascata fiel (**ADIADA por decisão Sovereign** — código financeiro + contexto saturado, Lei 3) + OTD-MCOIN-CALIBRATION (preços $ por-modelo/vídeo) · MVP-4 hooks+UI `/dashboard/marketing` · MVP-5 attribution. **Lição:** probe-first pegou a OTD já 80% pronta (zero retrabalho) e a divergência `campaigns`/`campaign_metrics` já-existentes; decisão financeira de `campaign-run` **registrada ao Sovereign em vez de improvisada** (Master Protocol).
> 32	
> 33	**Sprint v6.21.0 selado em 2026-06-03** — Marketing Hub (v2): BoK 9/9 + 11 agentes + MVP-1 Lead Core LIVE. Novo **módulo soberano** criado do zero seguindo o Master Execution Protocol (BoK-first), dirigido pela diretiva Sovereign de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). `/bok-scribe` selou a **suíte BoK 9/9** (1732 LOC, `docs/bok/marketing-hub/`, traceability **0 órfãos**, mesh seal `d5163fed` DERIVES_FROM meta-api) — módulo nasce como **v2 de consolidação** que **absorve e escala** o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**), natureza **Ambos** (interno Usuário Zero + comercial per-tenant). `/bok-agents-generator` produziu o **sistema de 11 agentes** (8 BoK + AEO/Intent-Orchestration/Demand-gen + Pantheon Reconciliation). Após revisão Sovereign ("aprovado"), **MVP-1 Lead Core** foi ao ar: migration `20260603000000` (`leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` LGPD SECURITY DEFINER), aplicada via `db push`. O `/security-review` (subagente **independente**) pegou **1 cross-tenant MEDIUM** (FK de tabela-filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta tenant-escopada `(lead_id,user_id)→leads(id,user_id)`** + provado **material** (23503 no ataque, 201 no legítimo, cleanup zero-resíduo). Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8755**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** MVP-2 Campaign Core deve **ABSORVER** a `campaigns` já existente (colisão real achada por probe-first), NÃO criar nova; + MVP-3 edge fns (`lead-score`/`campaign-run`) · MVP-4 hooks+UI (`/dashboard/marketing`) · MVP-5 attribution. **Lição:** probe-first do schema ANTES de codar pegou 2 divergências doc↔realidade (`campaigns` existe, `projects` não) que quebrariam o apply; e o `/security-review` por subagente independente (não auto-avaliação) pegou o furo de tenant que o self-review deixou passar.
> 34	
> 35	**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 36	
> 37	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 38	
> 39	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 40	
> 41	**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 42	
> 43	**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> 44	
> 45	**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 46	
> 47	**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 48	
> 49	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 50	
> 51	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 52	
> 53	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 54	
> 55	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 56	
> 57	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 58	
> 59	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 60	
> 61	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 62	
> 63	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 64	
> 65	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> ```

## 🤖 Claude *(01:41:22)*


## 🤖 Claude *(01:41:22)*

Pre-flight base OK. Agora a cauda do HANDOFF.md (Pending Actions + GraphRAG State) e detalhes complementares.

## 🤖 Claude *(01:41:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7145,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7145	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 7146	
> 7147	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 7148	
> 7149	ContentLibraryPage monetization flow:
> 7150	  Card (text, body contains mercadolivre.com.br)
> 7151	    └── DropdownMenu → "Monetizar Links ML"
> 7152	          → handleMonetizeLinks(item):
> 7153	               match(ML_URL_RE) → unique URLs
> 7154	               for url of unique:
> 7155	                 POST process-affiliate-link → affiliate_url
> 7156	                 body.split(url).join(affiliate_url)
> 7157	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7158	          → Badge 💰 ML (emerald) exibido após monetização
> 7159	```
> 7160	
> 7161	---
> 7162	
> 7163	## Pending Actions (Commercial Launch)
> 7164	
> 7165	### CRITICAL — Must complete before first client
> 7166	
> 7167	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7168	
> 7169	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7170	
> 7171	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7172	
> 7173	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7174	
> 7175	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7176	
> 7177	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7178	
> 7179	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7180	
> 7181	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7182	
> 7183	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7184	
> 7185	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7186	   ```bash
> 7187	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7188	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7189	   ```
> 7190	
> 7191	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7192	
> 7193	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7194	
> 7195	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7196	
> 7197	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7198	
> 7199	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7200	
> 7201	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7202	
> 7203	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7204	
> 7205	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7206	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7207	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7208	
> 7209	### SOCIAL — Next steps
> 7210	
> 7211	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7212	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7213	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7214	
> 7215	### NON-CRITICAL
> 7216	
> 7217	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7218	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7219	- `browserslist` — ✅ updated (2026-04-26)
> 7220	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7221	
> 7222	### GITNEXUS MCP — Next steps
> 7223	
> 7224	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7225	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7226	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7227	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7228	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7229	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7230	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7231	
> 7232	### PHASE EPSILON — Next iterations
> 7233	
> 7234	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7235	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7236	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7237	
> 7238	### CORE — Next iterations
> 7239	
> 7240	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7241	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7242	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7243	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7244	
> 7245	### PHASE DELTA — Next iterations
> 7246	
> 7247	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7248	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7249	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7250	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7251	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7252	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7253	
> 7254	### USUÁRIO ZERO — Checklist de validação
> 7255	
> 7256	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7257	- ✅ Stripe sandbox secrets no vault
> 7258	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7259	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7260	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7261	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7262	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7263	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7264	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7265	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7266	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7267	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7268	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7269	
> 7270	---
> 7271	
> 7272	## Infrastructure
> 7273	
> 7274	| Service | Container | Port | Status |
> 7275	|---------|-----------|------|--------|
> 7276	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7277	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7278	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7279	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7280	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7281	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7282	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7283	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7284	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7285	
> 7286	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7287	
> 7288	```bash
> 7289	docker compose up -d
> 7290	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7291	```
> 7292	
> 7293	---
> 7294	
> 7295	## Security Model (Post-Go-Live)
> 7296	
> 7297	| Table | Isolation |
> 7298	|-------|-----------|
> 7299	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 7300	| `mcorch_edges` | Same pattern |
> 7301	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 7302	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 7303	
> 7304	---
> 7305	
> 7306	## Billing Architecture
> 7307	
> 7308	| Decision | Value |
> 7309	|----------|-------|
> 7310	| Canonical billing ledger | `profiles.mco_balance` |
> 7311	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 7312	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 7313	| Orchestration cost | 10 mcoCoins/run |
> 7314	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 7315	| Stripe | Sandbox keys active — swap to live before first client |
> 7316	
> 7317	---
> 7318	
> 7319	## GraphRAG State
> 7320	
> 7321	- **8861 total nodes** (2026-06-10 cyber-sentinel-security seal: +handoff `0a9865a9-202c-4aae-ab42-d1500cdbc261` embedded 768d; prev 8860 em v6.33.1 kanban-scrollarea-fix +handoff `fd20b125`; 8852 em v6.33.0 ml-attribution +handoff `630509e2` + BoK seal `31323fe3` authenticated-browser-operator; was 8818 em v6.32.2 +handoff `5acba7aa`)
> 7322	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 7323	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 7324	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 7325	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 7326	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 7327	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 7328	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 7329	- HNSW cosine index operational
> 7330	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 7331	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 7332	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 7333	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 7334	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 7335	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 7336	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 7337	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 7338	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 7339	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 7340	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 7341	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 7342	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 7343	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 7344	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 7345	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 7346	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 7347	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 7348	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 7349	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 7350	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 7351	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 7352	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 7353	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 7354	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 7355	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 7356	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 7357	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 7358	
> 7359	### Embedding Model
> 7360	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 7361	Schema: `vector(768)` — HNSW cosine index.
> 7362	
> 7363	### Embedding Pipeline (Autônomo — 2026-05-03)
> 7364	Três camadas eliminam intervenção manual:
> 7365	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 7366	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 7367	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 7368	
> 7369	### Comandos de manutenção da Mesh
> 7370	```bash
> 7371	# Verificar nós sem embedding (deveria retornar array vazio):
> 7372	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 7373	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 7374	
> 7375	# Backfill manual (Bun-native — requer .env):
> 7376	bun run scripts/backfill-embeddings.ts
> 7377	
> 7378	# Backfill de código-fonte nos nós AST:
> 7379	bun run scripts/backfill-node-content.ts
> 7380	
> 7381	# Re-sync AST completo:
> 7382	cd packages/gitnexus-core && npm run sync-mesh
> 7383	
> 7384	# Acompanhar re-ingesta pós-commit:
> 7385	tail -f /tmp/mcorch-ingest.log
> 7386	```
> 7387	
> 7388	---
> 7389	
> 7390	## Video Rescue Protocol
> 7391	
> 7392	When a video generation operation (Google Veo) times out or client disconnects:
> 7393	```bash
> 7394	# Via edge function (production):
> 7395	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 7396	  -H "Authorization: Bearer <user_jwt>" \
> 7397	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 7398	
> 7399	# Via local script (admin/debug):
> 7400	source .env && bun run rescue.ts <operation_id> <content_id>
> 7401	```
> 7402	
> 7403	---
> 7404	
> 7405	## Architecture Pillars
> 7406	
> 7407	| Layer | Implementation |
> 7408	|-------|---------------|
> 7409	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 7410	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 7411	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 7412	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 7413	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 7414	
> 7415	---
> 7416	
> 7417	## Phase Delta — Architecture
> 7418	
> 7419	```
> 7420	OrchestrationPage (full-canvas, p-0)
> 7421	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 7422	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 7423	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 7424	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 7425	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 7426	        ├── nodes/PublishNode.tsx    ← final distribution output
> 7427	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 7428	        └── NodePalette.tsx          ← top toolbar to add nodes
> 7429	
> 7430	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 7431	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 7432	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 7433	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 7434	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 7435	```
> 7436	
> 7437	### Canvas State Architecture (Hybrid)
> 7438	
> 7439	```
> 7440	User interaction → ReactFlow internal state (positions, drag)
> 7441	                         ↓ (debounced 600ms)
> 7442	                   localStorage (positions persist across refresh)
> 7443	                         ↑
> 7444	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 7445	     ↓ (status changes sync to ReactFlow via useEffect)
> 7446	ReactFlow renders visual status (idle/running/done/error/blocked)
> 7447	```
> 7448	
> 7449	## Key Files
> 7450	
> 7451	| Purpose | Path |
> 7452	|---------|------|
> 7453	| Architecture rules | `CLAUDE.md` |
> 7454	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 7455	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 7456	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 7457	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 7458	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 7459	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 7460	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 7461	| **Node types** | `src/components/orchestrator/nodes/` |
> 7462	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 7463	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 7464	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 7465	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 7466	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 7467	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 7468	| Billing utilities | `src/lib/billing.ts` |
> 7469	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 7470	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 7471	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 7472	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 7473	| Video rescue (local) | `rescue.ts` |
> 7474	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 7475	| Backfill script | `scripts/backfill-embeddings.ts` |
> 7476	| Deploy harness | `scripts/harness-deploy.sh` |
> 7477	
> 7478	---
> 7479	
> 7480	## First Client Onboarding Checklist
> 7481	
> 7482	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 7483	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 7484	3. ~~Activate watchdog cron~~ ✅ Done
> 7485	4. ~~Deploy rescue-video function~~ ✅ Done
> 7486	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 7487	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 7488	7. Monitor `infra_health_logs` for first 24h.
> 7489	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 7490	
> 7491	---
> 7492	
> 7493	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 7494	
> 7495	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 7496	
> 7497	| Action | Result |
> 7498	|--------|--------|
> 7499	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 7500	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 7501	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 7502	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 7503	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 7504	
> 7505	| Commit | Conteúdo |
> 7506	|--------|----------|
> 7507	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 7508	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 7509	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 7510	
> 7511	### Arquitetura Matrix Intelligence
> 7512	
> 7513	```
> 7514	ConstellationMatrix (Stabilized Engine)
> 7515	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 7516	  └── NodeDetailsPanel (Tabbed Navigation)
> 7517	        ├── Tab Meta: Neighbor exploration + Net Context
> 7518	        ├── Tab Code: Source code preview (Supabase sync)
> 7519	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 7520	
> 7521	useNodeIntelligence Hook:
> 7522	  - contentQuery: fetch nodes.content column
> 7523	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 7524	  - state: isAnalyzing, analysisResult, progress
> 7525	```
> 7526	
> 7527	---
> 7528	
> 7529	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 7530	
> 7531	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 7532	
> 7533	| Action | Result |
> 7534	|--------|--------|
> 7535	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 7536	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 7537	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 7538	
> 7539	**Output da análise (estruturado em pt-BR):**
> 7540	- Visão Geral — papel do módulo no sistema
> 7541	- Padrões Detectados — design patterns, antipatterns
> 7542	- Acoplamento & Dependências — análise In/Out-Degree
> 7543	- Recomendações — 1-3 ações priorizadas
> 7544	
> ```

## 🤖 Claude *(01:41:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"---SPRINT-V634---\"; grep -n \"v6.34\" .claude/context/sprint-priorities.md | head -5; echo \"---BOK-SECURITY---\"; ls docs/bok/security/",
  "description": "List scratch files, check sprint-priorities for v6.34, list security BoK docs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 29 ubuntu ubuntu 4096 Jun  9 22:38 ..
> ---SPRINT-V634---
> ---BOK-SECURITY---
> 00-deepsearch-blueprint.md
> 01-brd-security.md
> 02-srs-secure-spec.md
> 03-sdd-hardening-architecture.md
> 04-fmea-security.md
> ```

## 🤖 Claude *(01:42:09)*


## 🤖 Claude *(01:42:10)*

Tudo coletado — contexto completo. Brief:

═══════════════════════════════════════════════════════════
  **HANDSON — CYBER-SENTINEL SECURITY (selada 2026-06-10)**
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **Cyber-Sentinel — BoK segurança 4/4 + gate de prompt LIVE em produção + hardening de infra** (v6.34.0)
  Últimos commits:
  - `fe3bb5c` — docs(handoff): seal Cyber-Sentinel security
  - `f58bc52` — docs(readme): v6.34.0 Cyber-Sentinel
  - `6f2f75a` — feat(security): gate de prompt em produção + hardening de infra

  Destaques do seal: sentinel fail-closed (`_shared/sentinel.ts` L1/L2/L3) ativo no `orchestrate-content` v52 — exploit com JWT real → `403 layer=sentinel`, zero débito; containers `claude_mem`/`chroma` endurecidos (uid 1001, read_only, caps); gate git dual-engine lefthook+gitleaks; review adversarial pegou 4 bugs reais antes do deploy.

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (zero arquivos M/??)

🏗️ **INFRA**
  mcorch_chroma:     Up 19 min (healthy) — Chroma API v2: **OK** (heartbeat respondendo)
  mcorch_claude_mem: Up 19 min (healthy) — recém-recriado endurecido (esperado, parte do seal)
  mega-brain-*:      daemon + webhook healthy · dashboard up (2 semanas)

🧠 **KNOWLEDGE MESH**
  **8861 nós** · **9070 arestas** (fonte: GraphRAG State; arestas verificadas live em 2026-06-01)
  Handoff node do seal: `0a9865a9-202c-4aae-ab42-d1500cdbc261` (embedded 768d)

🔧 **TYPESCRIPT**
  Zero erros ✅ (exit 0) · Suíte no seal: **295 passed / 2 skipped**

📚 **BoK SUITES**
  Sealed (9/9 docs): 18 suítes completas — agentic-workspace · aios-sql-bridge · authenticated-browser-operator · canvas-design · constellation-v2 · conteudo-v2 · e2e-user-zero · gamificacao-nodes · identity-fabric · marketing-hub · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · post-engine · viral-daily-canvas · viralmind
  `security`: o checker padrão acusa "missing 9 docs", mas é **falso positivo** — a suíte segue o formato da diretiva CISO (blueprint + 01-brd + 02-srs + 03-sdd + 04-fmea = **4/4 completa e selada**), não a família 9-doc.

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional (LinkedIn auto ✅ · Twitter gated em tier API · IG gated em App Review)
  Top gap: **OTD-SEC-006/007** — estender o sentinel às demais funções pagas + migration `security_events`/quarentena (<50ms)

⚡ **PRÓXIMOS PASSOS (prioridade)**
  1. **OTD-SEC-006/007 — fiar o sentinel nas demais funções pagas** (`campaign-run`, `intent-execute`, `lead-score`, `aeo-audit`, `canvas-execute`...) + migration `security_events`/quarentena. É o follow-up direto do seal: hoje só `orchestrate-content` está protegido contra prompt injection → billing bypass. Inclui promover lefthook a hook canônico em todas as máquinas (OTD-SEC-003 degradação).
  2. **BUILD do Operador de Browser Autenticado** — BoK 9/9 selada em v6.33.0, gate ABERTO; runtime obrigatoriamente residencial (datacenter 403 provado) → execução envolve o Sovereign rodando `agent-browser` logado no ML. Destrava atribuição definitiva ML (`matt_tool`/`meli.la`).
  3. **Gated no Sovereign** (sem código até GO): domínio `RESEND_FROM` (entrega real de nurturing) · atribuição de compra ML (aguardando 1ª conversão) · limpar 2 rascunhos WP de teste · FM-10 gitnexus (imagem endurecida pronta, aplicar quando containerizado).

⚠️ **ALERTAS**
  - **`sprint-priorities.md` está 1 seal atrás**: última entrada é v6.33.1 — falta registrar o sprint v6.34.0 Cyber-Sentinel (o seal foi commitado no HANDOFF/README mas não no sprint file). Correção de 1 entrada, posso fazer quando autorizado.
  - `scratch/` existe mas está **vazio** — sem ação necessária.
  - Nenhum container unhealthy, nenhum erro TS, worktree limpo ✅

═══════════════════════════════════════════════════════════
  **Pronto para trabalhar. Aguardando direção.**
═══════════════════════════════════════════════════════════

## 👤 User *(01:45:18)*

Refatore todo o nosso Core-v2 para Core-Fable - https://login.mcorch.com/dashboard/core-v2

## 👤 User *(01:45:20)*

[Request interrupted by user]

## 👤 User *(01:45:25)*

Refatore todo o nosso Core-v2 para Core-Fable - https://login.mcorch.com/dashboard/core-v2

## 🤖 Claude *(01:46:10)*


## 🤖 Claude *(01:46:12)*

**ORO triplet desta task:**
- Operator: MCORCH Master Execution Agent (refactor Core-v2 → Core-Fable)
- Reviewer: Sovereign (Gabriel)
- Owner: Sovereign (módulo Core em produção — `/dashboard/core-v2`)

Primeiro vou mapear materialmente a superfície do Core-v2 (probe-first) antes de tocar qualquer arquivo.

## 🤖 Claude *(01:46:13)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Probe do m\u00f3dulo Core-v2",
  "summary": "Mapeamento da superf\u00edcie Core-v2 antes do refactor para Core-Fable"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Probe do módulo Core-v2". Continue your current work.'}]
> ```

## 🤖 Claude *(01:46:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn -iE \"core-?v2\" src/ --include=\"*.tsx\" --include=\"*.ts\" -l | sort; echo \"---ROUTES---\"; grep -n -iE \"core\" src/App.tsx | head -30",
  "description": "Find all files referencing core-v2 and core routes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/App.tsx
> src/components/dashboard/DashboardLayout.tsx
> src/components/dashboard/DashboardSidebar.tsx
> src/pages/CoreV2Page.tsx
> ---ROUTES---
> 37:const CoreV2Page = lazy(() => import("./pages/CoreV2Page.tsx"));
> 113:                <Route path="core" element={<Navigate to="/dashboard/core-v2" replace />} />
> 114:                <Route path="core-v2" element={<CoreV2Page />} />
> ```

## 🤖 Claude *(01:46:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls src/pages/ | grep -iE \"core\"; echo \"---COMPONENTS---\"; ls src/components/ | head -40; ls src/components/core* 2>/dev/null; ls src/components/aios 2>/dev/null; echo \"---HOOKS---\"; ls src/hooks/ | grep -iE \"aios|core|terminal|workspace\"",
  "description": "List core pages, components and AIOS hooks"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> CoreV2Page.tsx
> ---COMPONENTS---
> admin
> ads
> blocks
> canvas
> core
> core-v2
> dashboard
> gestures
> graph
> HUD.tsx
> icons
> landing
> Legend.tsx
> marketing
> NavLink.tsx
> orchestrator
> panels
> settings
> ui
> src/components/core:
> AIOSTerminal.tsx
> ConversationTimeline.tsx
> VibrationalWaves.tsx
> 
> src/components/core-v2:
> A2UIRenderer.tsx
> MegaBrainVisualizer.tsx
> ---HOOKS---
> useAIOSConversations.ts
> useAiosKanban.ts
> useAiosTerminalChat.ts
> useAiosWorkspaceChat.ts
> ```

## 🤖 Claude *(01:46:27)*


## 🤖 Claude *(01:46:27)*


## 🤖 Claude *(01:46:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l src/pages/CoreV2Page.tsx src/components/core-v2/*.tsx src/components/core/*.tsx src/hooks/useAiosTerminalChat.ts src/hooks/useAiosWorkspaceChat.ts src/hooks/useAIOSConversations.ts src/hooks/useAiosKanban.ts 2>/dev/null; echo \"---EDGE-FNS---\"; ls supabase/functions/ | grep -iE \"aios|chat|core\"; echo \"---TESTS---\"; grep -rln -iE \"corev2|core-v2|aios\" src/test/ src/**/*.test.ts 2>/dev/null | sort -u",
  "description": "Size core-v2 files, find AIOS edge functions and tests"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>    296 src/pages/CoreV2Page.tsx
>    274 src/components/core-v2/A2UIRenderer.tsx
>    322 src/components/core-v2/MegaBrainVisualizer.tsx
>   1210 src/components/core/AIOSTerminal.tsx
>    267 src/components/core/ConversationTimeline.tsx
>    192 src/components/core/VibrationalWaves.tsx
>    221 src/hooks/useAiosTerminalChat.ts
>    162 src/hooks/useAiosWorkspaceChat.ts
>    287 src/hooks/useAIOSConversations.ts
>    193 src/hooks/useAiosKanban.ts
>   3424 total
> ---EDGE-FNS---
> aios-chat
> aios-chat-gateway
> aios-chat-stream
> aios-live-proxy
> aios-sql-bridge
> lead-score
> ---TESTS---
> src/test/agentic-workspace.test.ts
> src/test/aios-sql-bridge-smoke.test.ts
> src/test/phase-zeta.test.tsx
> ```

## 🤖 Claude *(01:46:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn -iE '\"Core ?v?2|Core v2|CoreV2|core_v2' src/ --include=\"*.tsx\" --include=\"*.ts\" | grep -vE \"^\\S+:[0-9]+:\\s*//\" | head -40; echo \"---MODEL-WIRING---\"; grep -rn -E \"pref_ai_model|selected_model|aios_model|model.*select\" src/hooks/useAiosTerminalChat.ts src/hooks/useAiosWorkspaceChat.ts 2>/dev/null | head -20",
  "description": "Find Core v2 naming references and model selection wiring"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/App.tsx:37:const CoreV2Page = lazy(() => import("./pages/CoreV2Page.tsx"));
> src/App.tsx:114:                <Route path="core-v2" element={<CoreV2Page />} />
> src/pages/CoreV2Page.tsx:25:export default function CoreV2Page() {
> src/pages/CoreV2Page.tsx:86:              Core v2 — Mega Brain
> src/pages/CampaignDetail.tsx:223:      {/* Passos & Execução (Campaign Core v2 — FR-MH-004/005) */}
> ---MODEL-WIRING---
> ```

## 🤖 Claude *(01:47:03)*


## 🤖 Claude *(01:47:03)*


## 🤖 Claude *(01:47:37)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'understand-core-v2',\n  description: 'Map the full Core-v2 module surface before refactor to Core-Fable',\n  phases: [\n    { title: 'Read', detail: 'parallel readers over Core-v2 subsystems' },\n    { title: 'Sweep', detail: 'completeness critic for missed references' },\n  ],\n}\n\nconst SCHEMA = {\n  type: 'object',\n  required: ['summary', 'namingRefs', 'modelWiring', 'risks'],\n  properties: {\n    summary: { type: 'string', description: 'Dense technical summary of what was read' },\n    namingRefs: {\n      type: 'array',\n      description: 'Every occurrence of Core v2 / CoreV2 / core-v2 / core_v2 / Mega Brain branding or identifiers that a rename to Core-Fable would touch',\n      items: {\n        type: 'object',\n        required: ['file', 'line', 'text', 'kind'],\n        properties: {\n          file: { type: 'string' },\n          line: { type: 'number' },\n          text: { type: 'string' },\n          kind: { type: 'string', description: 'route|import|component-name|ui-string|localStorage-key|db-column|test|comment|css-class|other' },\n        },\n      },\n    },\n    modelWiring: {\n      type: 'array',\n      description: 'Every place an AI model/provider is selected, defaulted, persisted, or invoked (model ids, provider fallbacks, user_api_keys columns, edge fn calls)',\n      items: {\n        type: 'object',\n        required: ['file', 'detail'],\n        properties: { file: { type: 'string' }, line: { type: 'number' }, detail: { type: 'string' } },\n      },\n    },\n    risks: { type: 'array', items: { type: 'string' }, description: 'Things a rename/refactor could break (lazy imports, localStorage persistence, DB rows, test snapshots, deep links)' },\n  },\n}\n\nphase('Read')\nconst READERS = [\n  {\n    key: 'page-routing',\n    prompt: `Read these files in the repo /home/gcrUX/htdocs/constellation-orchestra COMPLETELY:\n- src/pages/CoreV2Page.tsx (296 LOC)\n- src/App.tsx (focus: lazy imports + routes for core/core-v2)\n- src/components/dashboard/DashboardLayout.tsx (grep for core/Core references and read surrounding context)\n- src/components/dashboard/DashboardSidebar.tsx (same)\nReport: page structure (what components it composes, layout), ALL naming references to \"Core v2\"/\"CoreV2\"/\"core-v2\"/\"Mega Brain\" (exact file:line:text), how navigation/menu labels work, any localStorage keys, and what a route rename core-v2\u2192core-fable would affect (deep links, Navigate redirects).`,\n  },\n  {\n    key: 'hooks-datalayer',\n    prompt: `Read these hook files in /home/gcrUX/htdocs/constellation-orchestra COMPLETELY:\n- src/hooks/useAiosTerminalChat.ts (221 LOC)\n- src/hooks/useAiosWorkspaceChat.ts (162 LOC)\n- src/hooks/useAIOSConversations.ts (287 LOC)\n- src/hooks/useAiosKanban.ts (193 LOC)\nReport: which edge functions each hook invokes (exact function names + payload shape), how the AI model is selected/persisted (look for pref_ai_model, user_api_keys columns, model ids like gemini-*, claude-*, gpt-*), DB tables touched (aios_conversations etc.), TanStack Query keys, any Core v2/Mega Brain naming, and localStorage keys.`,\n  },\n  {\n    key: 'components-visual',\n    prompt: `Read these component files in /home/gcrUX/htdocs/constellation-orchestra COMPLETELY:\n- src/components/core-v2/A2UIRenderer.tsx (274 LOC)\n- src/components/core-v2/MegaBrainVisualizer.tsx (322 LOC)\n- src/components/core/AIOSTerminal.tsx (1210 LOC \u2014 read it ALL, it is the biggest piece)\n- src/components/core/ConversationTimeline.tsx (267 LOC)\n- src/components/core/VibrationalWaves.tsx (192 LOC)\nReport: which of these CoreV2Page actually uses (vs legacy CorePage leftovers), component props/exports, ALL naming references to Core v2/Mega Brain (file:line:text), model selector UI (what models are listed, exact model id strings, where selection is persisted), edge function invocations, WebGL shader identity (black hole/cymatics), and any hardcoded strings shown to the user (PT-BR UI text).`,\n  },\n  {\n    key: 'edge-functions',\n    prompt: `Read these Supabase edge functions in /home/gcrUX/htdocs/constellation-orchestra COMPLETELY:\n- supabase/functions/aios-chat/index.ts\n- supabase/functions/aios-chat-gateway/index.ts\n- supabase/functions/aios-chat-stream/index.ts\n- supabase/functions/aios-live-proxy/index.ts\nAlso check supabase/config.toml for their verify_jwt entries, and supabase/functions/_shared/ for any helper they import (e.g. llm fallback helper).\nReport: for EACH function \u2014 provider(s) used (OpenRouter/Gemini/Groq/OpenAI direct?), exact model id strings + fallback chains, how per-user API keys are resolved (user_api_keys / decrypted_user_api_keys columns), JWT handling, mcoCoins billing if any, which one(s) the Core-v2 frontend actually calls, and whether Anthropic/Claude models are reachable through the existing provider paths (e.g. OpenRouter model ids like anthropic/claude-*).`,\n  },\n  {\n    key: 'blast-radius',\n    prompt: `In /home/gcrUX/htdocs/constellation-orchestra, sweep for the blast radius of renaming the Core-v2 module to Core-Fable:\n1. grep -rn for: CoreV2, core-v2, core_v2, \"Core v2\", \"Mega Brain\", MegaBrain, megabrain \u2014 across src/, supabase/, scripts/, docs/, e2e/, README.md, index.html (NOT HANDOFF.md, NOT .claude/, NOT node_modules, NOT dist).\n2. Read src/test/phase-zeta.test.tsx and src/test/agentic-workspace.test.ts fully \u2014 do they reference Core v2 components/hooks?\n3. Check supabase/migrations/ for any table/column named with core/aios model prefs (grep -l \"pref_ai_model\\\\|aios_\" supabase/migrations/*.sql and read matching lines).\n4. Check localStorage usage: grep -rn \"localStorage\" src/pages/CoreV2Page.tsx src/components/core/ src/components/core-v2/ src/hooks/useAios*.\n5. Check vite/playwright configs and e2e flows (scripts/qa/e2e-user-zero/flows/) for core-v2 routes.\nReport every hit with file:line:text and classify kind.`,\n  },\n]\n\nconst results = await parallel(READERS.map(r => () =>\n  agent(r.prompt, { label: `read:${r.key}`, phase: 'Read', schema: SCHEMA })\n))\n\nphase('Sweep')\nconst found = results.filter(Boolean)\nconst critic = await agent(\n  `You are a completeness critic for a refactor mapping of the Core-v2 module in /home/gcrUX/htdocs/constellation-orchestra (rename + rebrand to \"Core-Fable\", route /dashboard/core-v2 \u2192 likely /dashboard/core-fable, possibly switching default AI model to Anthropic Claude Fable 5).\nHere is what 5 parallel readers found (JSON): ${JSON.stringify(found.map(f => ({ summary: f.summary, namingRefCount: f.namingRefs.length, modelWiring: f.modelWiring, risks: f.risks }))).slice(0, 12000)}\nYour job: find what they MISSED. Check materially (run greps/reads yourself):\n- Any remaining \"CoreV2|core-v2|Mega Brain\" refs outside the mapped files (src/, index.html, public/, nginx-served assets)?\n- Does anything else import from src/components/core-v2/ or src/components/core/ or the useAios* hooks (e.g. other pages reusing AIOSTerminal)?\n- Is there an old CorePage in .archive/ that could confuse the rename?\n- Any Supabase DB values (not schema) storing the route or page name?\n- Anything in src/integrations/supabase/types.ts relevant to model prefs?\nReturn JSON.`,\n  { label: 'critic:completeness', phase: 'Sweep', schema: SCHEMA }\n)\n\nreturn { readers: found, critic }"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wr6vzsvto
> Summary: Map the full Core-v2 module surface before refactor to Core-Fable
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/240db21b-cd40-4765-a3f4-345f03d2fc33/subagents/workflows/wf_83d99598-82f
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/240db21b-cd40-4765-a3f4-345f03d2fc33/workflows/scripts/understand-core-v2-wf_83d99598-82f.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/240db21b-cd40-4765-a3f4-345f03d2fc33/workflows/scripts/understand-core-v2-wf_83d99598-82f.js"} to iterate without resending the script.)
> Run ID: wf_83d99598-82f
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/240db21b-cd40-4765-a3f4-345f03d2fc33/workflows/scripts/understand-core-v2-wf_83d99598-82f.js", resumeFromRunId: "wf_83d99598-82f"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(01:47:45)*


## 🤖 Claude *(01:47:45)*


## 🤖 Claude *(01:47:45)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "claude-api"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: claude-api
> ```

## 👤 User *(01:47:45)*

Base directory for this skill: /tmp/claude-1001/bundled-skills/2.1.170/6d19fd6839b2e00e4eeec5033f0cf4df/claude-api

# Building LLM-Powered Applications with Claude

This skill helps you build LLM-powered applications with Claude. Choose the right surface based on your needs, detect the project language, then read the relevant language-specific documentation.

## Before You Start

Scan the target file (or, if no target file, the prompt and project) for non-Anthropic provider markers — `import openai`, `from openai`, `langchain_openai`, `OpenAI(`, `gpt-4`, `gpt-5`, file names like `agent-openai.py` or `*-generic.py`, or any explicit instruction to keep the code provider-neutral. If you find any, stop and tell the user that this skill produces Claude/Anthropic SDK code; ask whether they want to switch the file to Claude or want a non-Claude implementation. Do not edit a non-Anthropic file with Anthropic SDK calls.

## Output Requirement

When the user asks you to add, modify, or implement a Claude feature, your code must call Claude through one of:

1. **The official Anthropic SDK** for the project's language (`anthropic`, `@anthropic-ai/sdk`, `com.anthropic.*`, etc.). This is the default whenever a supported SDK exists for the project.
2. **Raw HTTP** (`curl`, `requests`, `fetch`, `httpx`, etc.) — only when the user explicitly asks for cURL/REST/raw HTTP, the project is a shell/cURL project, or the language has no official SDK.

Never mix the two — don't reach for `requests`/`fetch` in a Python or TypeScript project just because it feels lighter. Never fall back to OpenAI-compatible shims.

**Never guess SDK usage.** Function names, class names, namespaces, method signatures, and import paths must come from explicit documentation — either the `{lang}/` files in this skill or the official SDK repositories or documentation links listed in `shared/live-sources.md`. If the binding you need is not explicitly documented in the skill files, WebFetch the relevant SDK repo from `shared/live-sources.md` before writing code. Do not infer Ruby/Java/Go/PHP/C# APIs from cURL shapes or from another language's SDK.

## Defaults

Unless the user requests otherwise:

For the Claude model version, please use Claude Opus 4.8, which you can access via the exact model string `claude-opus-4-8`. Please default to using adaptive thinking (`thinking: {type: "adaptive"}`) for anything remotely complicated. And finally, please default to streaming for any request that may involve long input, long output, or high `max_tokens` — it prevents hitting request timeouts. Use the SDK's `.get_final_message()` / `.finalMessage()` helper to get the complete response if you don't need to handle individual stream events

---

## Subcommands

If the User Request at the bottom of this prompt is a bare subcommand string (no prose), search every **Subcommands** table in this document — including any in sections appended below — and follow the matching Action column directly. This lets users invoke specific flows via `/claude-api <subcommand>`. If no table in the document matches, treat the request as normal prose.

| Subcommand | Action |
|---|---|
| `migrate` | Migrate existing Claude API code to a newer model. **Read `shared/model-migration.md` immediately** and follow it in order: Step 0 (confirm scope — ask which files/directories before any edit), Step 1 (classify each file), then the per-target breaking-changes section. Do not summarize the guide — execute it. If the user did not name a target model, ask which model to migrate to in the same turn as the scope question. |

---

## Language Detection

Before reading code examples, determine which language the user is working in:

1. **Look at project files** to infer the language:

   - `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` → **Python** — read from `python/`
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` → **TypeScript** — read from `typescript/`
   - `*.js`, `*.jsx` (no `.ts` files present) → **TypeScript** — JS uses the same SDK, read from `typescript/`
   - `*.java`, `pom.xml`, `build.gradle` → **Java** — read from `java/`
   - `*.kt`, `*.kts`, `build.gradle.kts` → **Java** — Kotlin uses the Java SDK, read from `java/`
   - `*.scala`, `build.sbt` → **Java** — Scala uses the Java SDK, read from `java/`
   - `*.go`, `go.mod` → **Go** — read from `go/`
   - `*.rb`, `Gemfile` → **Ruby** — read from `ruby/`
   - `*.cs`, `*.csproj` → **C#** — read from `csharp/`
   - `*.php`, `composer.json` → **PHP** — read from `php/`

2. **If multiple languages detected** (e.g., both Python and TypeScript files):

   - Check which language the user's current file or question relates to
   - If still ambiguous, ask: "I detected both Python and TypeScript files. Which language are you using for the Claude API integration?"

3. **If language can't be inferred** (empty project, no source files, or unsupported language):

   - Use AskUserQuestion with options: Python, TypeScript, Java, Go, Ruby, cURL/raw HTTP, C#, PHP
   - If AskUserQuestion is unavailable, default to Python examples and note: "Showing Python examples. Let me know if you need a different language."

4. **If unsupported language detected** (Rust, Swift, C++, Elixir, etc.):

   - Suggest cURL/raw HTTP examples from `curl/` and note that community SDKs may exist
   - Offer to show Python or TypeScript examples as reference implementations

5. **If user needs cURL/raw HTTP examples**, read from `curl/`.

### Language-Specific Feature Support

| Language   | Tool Runner | Managed Agents | Notes                                 |
| ---------- | ----------- | -------------- | ------------------------------------- |
| Python     | Yes (beta)  | Yes (beta)     | Full support — `@beta_tool` decorator |
| TypeScript | Yes (beta)  | Yes (beta)     | Full support — `betaZodTool` + Zod    |
| Java       | Yes (beta)  | Yes (beta)     | Beta tool use with annotated classes  |
| Go         | Yes (beta)  | Yes (beta)     | `BetaToolRunner` in `toolrunner` pkg  |
| Ruby       | Yes (beta)  | Yes (beta)     | `BaseTool` + `tool_runner` in beta    |
| C#         | Yes (beta)  | Yes (beta)     | `BetaToolRunner` + raw JSON schema    |
| PHP        | Yes (beta)  | Yes (beta)     | `BetaRunnableTool` + `toolRunner()`   |
| cURL       | N/A         | Yes (beta)     | Raw HTTP, no SDK features             |

> **Managed Agents code examples**: dedicated language-specific READMEs are provided for Python, TypeScript, Go, Ruby, PHP, Java, and cURL (`{lang}/managed-agents/README.md`, `curl/managed-agents.md`). Read your language's README plus the language-agnostic `shared/managed-agents-*.md` concept files. **Agents are persistent — create once, reference by ID.** Store the agent ID returned by `agents.create` and pass it to every subsequent `sessions.create`; do not call `agents.create` in the request path. The Anthropic CLI (`ant`) is one convenient way to create agents and environments from version-controlled YAML — see `shared/anthropic-cli.md`. If a binding you need isn't shown in the README, WebFetch the relevant entry from `shared/live-sources.md` rather than guess. C# has beta Managed Agents support via `client.Beta.Agents` and related namespaces.

---

## Which Surface Should I Use?

> **Start simple.** Default to the simplest tier that meets your needs. Single API calls and workflows handle most use cases — only reach for agents when the task genuinely requires open-ended, model-driven exploration.

| Use Case                                        | Tier            | Recommended Surface       | Why                                                          |
| ----------------------------------------------- | --------------- | ------------------------- | ------------------------------------------------------------ |
| Classification, summarization, extraction, Q&A  | Single LLM call | **Claude API**            | One request, one response                                    |
| Batch processing or embeddings                  | Single LLM call | **Claude API**            | Specialized endpoints                                        |
| Multi-step pipelines with code-controlled logic | Workflow        | **Claude API + tool use** | You orchestrate the loop                                     |
| Custom agent with your own tools                | Agent           | **Claude API + tool use** | Maximum flexibility                                          |
| Server-managed stateful agent with workspace    | Agent           | **Managed Agents**        | Anthropic runs the loop and hosts the tool-execution sandbox |
| Persisted, versioned agent configs              | Agent           | **Managed Agents**        | Agents are stored objects; sessions pin to a version         |
| Long-running multi-turn agent with file mounts  | Agent           | **Managed Agents**        | Per-session containers, SSE event stream, Skills + MCP       |

> **Note:** Managed Agents is the right choice when you want Anthropic to run the agent loop *and* host the container where tools execute — file ops, bash, code execution all run in the per-session workspace. If you want to host the compute yourself or run your own custom tool runtime, Claude API + tool use is the right choice — use the tool runner for automatic loop handling, or the manual loop for fine-grained control (approval gates, custom logging, conditional execution).

> **Cloud-provider access.** **Claude Platform on AWS** is Anthropic-operated with same-day API parity — Managed Agents and every feature in this skill work there, **except self-hosted sandboxes** (see `shared/claude-platform-on-aws.md`). **Amazon Bedrock**, **Google Vertex AI**, and **Microsoft Foundry** do **not** support Managed Agents or Anthropic server-side tools; use **Claude API + tool use** on those.

### Decision Tree

```
What does your application need?

0. Which provider?
   ├── First-party API or Claude Platform on AWS → continue (full surface available).
   └── Amazon Bedrock, Google Vertex AI, or Microsoft Foundry → Claude API (+ tool use for agents); Managed Agents not available there.

1. Single LLM call (classification, summarization, extraction, Q&A)
   └── Claude API — one request, one response

2. Do you want Anthropic to run the agent loop and host a per-session
   container where Claude executes tools (bash, file ops, code)?
   └── Yes → Managed Agents — server-managed sessions, persisted agent configs,
       SSE event stream, Skills + MCP, file mounts.
       Examples: "stateful coding agent with a workspace per task",
                 "long-running research agent that streams events to a UI",
                 "agent with persisted, versioned config used across many sessions"

3. Workflow (multi-step, code-orchestrated, with your own tools)
   └── Claude API with tool use — you control the loop

4. Open-ended agent (model decides its own trajectory, your own tools, you host the compute)
   └── Claude API agentic loop (maximum flexibility)
```

### Should I Build an Agent?

Before choosing the agent tier, check all four criteria:

- **Complexity** — Is the task multi-step and hard to fully specify in advance? (e.g., "turn this design doc into a PR" vs. "extract the title from this PDF")
- **Value** — Does the outcome justify higher cost and latency?
- **Viability** — Is Claude capable at this task type?
- **Cost of error** — Can errors be caught and recovered from? (tests, review, rollback)

If the answer is "no" to any of these, stay at a simpler tier (single call or workflow).

---

## Architecture

Everything goes through `POST /v1/messages`. Tools and output constraints are features of this single endpoint — not separate APIs.

**User-defined tools** — You define tools (via decorators, Zod schemas, or raw JSON), and the SDK's tool runner handles calling the API, executing your functions, and looping until Claude is done. For full control, you can write the loop manually.

**Server-side tools** — Anthropic-hosted tools that run on Anthropic's infrastructure. Code execution is fully server-side (declare it in `tools`, Claude runs code automatically). Computer use can be server-hosted or self-hosted.

**Structured outputs** — Constrains the Messages API response format (`output_config.format`) and/or tool parameter validation (`strict: true`). The recommended approach is `client.messages.parse()` which validates responses against your schema automatically. Note: the old `output_format` parameter is deprecated; use `output_config: {format: {...}}` on `messages.create()`.

**Supporting endpoints** — Batches (`POST /v1/messages/batches`), Files (`POST /v1/files`), Token Counting (`POST /v1/messages/count_tokens` — see `shared/token-counting.md`), and Models (`GET /v1/models`, `GET /v1/models/{id}` — live capability/context-window discovery) feed into or support Messages API requests.

---

## Current Models (cached: 2026-05-26)

| Model             | Model ID            | Context        | Input $/1M | Output $/1M |
| ----------------- | ------------------- | -------------- | ---------- | ----------- |
| Claude Fable 5    | `claude-fable-5`      | 1M             | $10.00     | $50.00      |
| Claude Opus 4.8   | `claude-opus-4-8`   | 1M             | $5.00      | $25.00      |
| Claude Opus 4.7   | `claude-opus-4-7`   | 1M             | $5.00      | $25.00      |
| Claude Opus 4.6   | `claude-opus-4-6`   | 1M             | $5.00      | $25.00      |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M             | $3.00      | $15.00      |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00      | $5.00       |

**ALWAYS use `claude-opus-4-8` unless the user explicitly names a different model.** This is non-negotiable. Do not use `claude-sonnet-4-6`, `claude-sonnet-4-5`, or any other model unless the user literally says "use sonnet" or "use haiku". Never downgrade for cost — that's the user's decision, not yours.

**CRITICAL: Use only the exact model ID strings from the table above — they are complete as-is. Do not append date suffixes.** For example, use `claude-sonnet-4-6`, never `claude-sonnet-4-6-20251114` or any other date-suffixed variant you might recall from training data. If the user requests an older model not in the table (e.g., "opus 4.5", "sonnet 3.7"), read `shared/models.md` for the exact ID — do not construct one yourself.

A note: if any of the model strings above look unfamiliar to you, that's to be expected — that just means they were released after your training data cutoff. Rest assured they are real models; we wouldn't mess with you like that.

**Live capability lookup:** The table above is cached. When the user asks "what's the context window for X", "does X support vision/thinking/effort", or "which models support Y", query the Models API (`client.models.retrieve(id)` / `client.models.list()`) — see `shared/models.md` for the field reference and capability-filter examples.

---

## Thinking & Effort (Quick Reference)

**Fable 5 / Opus 4.8 / 4.7 — Adaptive thinking only:** Use `thinking: {type: "adaptive"}`. `thinking: {type: "enabled", budget_tokens: N}` returns a 400 — adaptive is the only on-mode. On Opus 4.8 and 4.7, `{type: "disabled"}` and omitting `thinking` both work; on Fable 5, an explicit `{type: "disabled"}` returns a 400 — omit the `thinking` param entirely instead. Sampling parameters (`temperature`, `top_p`, `top_k`) are also removed and will 400. Opus 4.8 keeps the same request surface as 4.7 (no new breaking changes) — see `shared/model-migration.md` → Migrating to Opus 4.8 for the behavioral re-tuning, and → Migrating to Opus 4.7 for the full breaking-change list when coming from 4.6 or earlier. Note: with `thinking` disabled, Opus 4.8 may write longer reasoning into the visible response — leave adaptive thinking on, or add a final-answer-only instruction (see the migration guide).
**Opus 4.6 — Adaptive thinking (recommended):** Use `thinking: {type: "adaptive"}`. Claude dynamically decides when and how much to think. No `budget_tokens` needed — `budget_tokens` is deprecated on Opus 4.6 and Sonnet 4.6 and should not be used for new code. Adaptive thinking also automatically enables interleaved thinking (no beta header needed). **When the user asks for "extended thinking", a "thinking budget", or `budget_tokens`: always use Fable 5, Opus 4.8, 4.7, or 4.6 with `thinking: {type: "adaptive"}`. The concept of a fixed token budget for thinking is deprecated — adaptive thinking replaces it. Do NOT use `budget_tokens` for new 4.6/4.7/4.8 code and do NOT switch to an older model.** *Gradual-migration carve-out:* `budget_tokens` is still functional on Opus 4.6 and Sonnet 4.6 as a transitional escape hatch — if you're migrating existing code and need a hard token ceiling before you've tuned `effort`, see `shared/model-migration.md` → Transitional escape hatch. Note: this carve-out does **not** apply to Fable 5, Opus 4.7 or 4.8 — `budget_tokens` is fully removed there.
**Effort parameter (GA, no beta header):** Controls thinking depth and overall token spend via `output_config: {effort: "low"|"medium"|"high"|"max"}` (inside `output_config`, not top-level). Default is `high` (equivalent to omitting it). `max` is supported on Fable 5, Opus 4.6 and later, and Sonnet 4.6 (not Haiku or earlier Sonnets). Opus 4.7 added `"xhigh"` (between `high` and `max`) — the best setting for most coding and agentic use cases on Fable 5 / Opus 4.7/4.8, and the default in Claude Code; use a minimum of `high` for most intelligence-sensitive work. Works on Fable 5, Opus 4.5, Opus 4.6, Opus 4.7, Opus 4.8, and Sonnet 4.6. Will error on Sonnet 4.5 / Haiku 4.5. On Fable 5, Opus 4.7 and 4.8, effort matters more than on any prior Opus — re-tune it when migrating, and run long-horizon/agentic tasks at `high`/`xhigh` with the full task spec given up front. Combine with adaptive thinking for the best cost-quality tradeoffs. Lower effort means fewer and more-consolidated tool calls, less preamble, and terser confirmations — `high` is often the sweet spot balancing quality and token efficiency; use `max` when correctness matters more than cost; use `low` for subagents or simple tasks.

**Fable 5 / Opus 4.8 / 4.7 — thinking content omitted by default:** `thinking` blocks still stream but their text is empty unless you opt in with `thinking: {type: "adaptive", display: "summarized"}` (default is `"omitted"`). Silent change — no error. If you stream reasoning to users, the default looks like a long pause before output; set `"summarized"` to restore visible progress.

**Task Budgets (beta, Fable 5 / Opus 4.7 / 4.8):** `output_config: {task_budget: {type: "tokens", total: N}}` tells the model how many tokens it has for a full agentic loop — it sees a running countdown and self-moderates (minimum 20,000; beta header `task-budgets-2026-03-13`). Distinct from `max_tokens`, which is an enforced per-response ceiling the model is not aware of. See `shared/model-migration.md` → Task Budgets.

**Sonnet 4.6:** Supports adaptive thinking (`thinking: {type: "adaptive"}`). `budget_tokens` is deprecated on Sonnet 4.6 — use adaptive thinking instead.

**Older models (only if explicitly requested):** If the user specifically asks for Sonnet 4.5 or another older model, use `thinking: {type: "enabled", budget_tokens: N}`. `budget_tokens` must be less than `max_tokens` (minimum 1024). Never choose an older model just because the user mentions `budget_tokens` — use Opus 4.8 with adaptive thinking instead.

---

## Compaction (Quick Reference)

**Beta, Fable 5, Opus 4.8, Opus 4.7, Opus 4.6, and Sonnet 4.6.** For long-running conversations that may exceed the 1M context window, enable server-side compaction. The API automatically summarizes earlier context when it approaches the trigger threshold (default: 150K tokens). Requires beta header `compact-2026-01-12`.

**Critical:** Append `response.content` (not just the text) back to your messages on every turn. Compaction blocks in the response must be preserved — the API uses them to replace the compacted history on the next request. Extracting only the text string and appending that will silently lose the compaction state.

See `{lang}/claude-api/README.md` (Compaction section) for code examples. Full docs via WebFetch in `shared/live-sources.md`.

---

## Prompt Caching (Quick Reference)

**Prefix match.** Any byte change anywhere in the prefix invalidates everything after it. Render order is `tools` → `system` → `messages`. Keep stable content first (frozen system prompt, deterministic tool list), put volatile content (timestamps, per-request IDs, varying questions) after the last `cache_control` breakpoint.

**Mid-conversation operator instructions** (beta header `mid-conversation-system-2026-04-07`, on supporting models): append `{"role": "system", ...}` to `messages[]` instead of editing top-level `system`. Preserves the cached history prefix and is the prompt-injection-safe operator channel. See `shared/prompt-caching.md` § Mid-conversation system messages.

**Top-level auto-caching** (`cache_control: {type: "ephemeral"}` on `messages.create()`) is the simplest option when you don't need fine-grained placement. Max 4 breakpoints per request. Minimum cacheable prefix is ~1024 tokens — shorter prefixes silently won't cache.

**Verify with `usage.cache_read_input_tokens`** — if it's zero across repeated requests, a silent invalidator is at work (`datetime.now()` in system prompt, unsorted JSON, varying tool set).

For placement patterns, architectural guidance, and the silent-invalidator audit checklist: read `shared/prompt-caching.md`. Language-specific syntax: `{lang}/claude-api/README.md` (Prompt Caching section).

---

## Managed Agents (Beta)

**Managed Agents** is a third surface: server-managed stateful agents with Anthropic-hosted tool execution. You create a persisted, versioned Agent config (`POST /v1/agents`), then start Sessions that reference it. Each session provisions a container as the agent's workspace — bash, file ops, and code execution run there; the agent loop itself runs on Anthropic's orchestration layer and acts on the container via tools. The session streams events; you send messages and tool results back.

**Managed Agents is available on the first-party API and Claude Platform on AWS.** It is **not** available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry — for agents there, use Claude API + tool use.

**Mandatory flow:** Agent (once) → Session (every run). `model`/`system`/`tools` live on the agent, never the session. See `shared/managed-agents-overview.md` for the full reading guide, beta headers, and pitfalls.

**Beta headers:** `managed-agents-2026-04-01` — the SDK sets this automatically for all `client.beta.{agents,environments,sessions,vaults,memory_stores}.*` calls. Skills API uses `skills-2025-10-02` and Files API uses `files-api-2025-04-14`, but you don't need to explicitly pass those in for endpoints other than `/v1/skills` and `/v1/files`.

**Subcommands** — invoke directly with `/claude-api <subcommand>`:

| Subcommand | Action |
|---|---|
| `managed-agents-onboard` | Walk the user through setting up a Managed Agent from scratch. **Read `shared/managed-agents-onboarding.md` immediately** and follow its interview script: mental model → know-or-explore branch → template config → session setup → **pre-flight viability check** → emit code. The viability check (reconcile the stated job against configured tools/credentials/data) catches under-resourced setups — missing a tool, credential, or data access — before the agent burns budget. Do not summarize — run the interview. |

**Reading guide:** Start with `shared/managed-agents-overview.md`, then the topical `shared/managed-agents-*.md` files (core, environments, tools, events, outcomes, multiagent, webhooks, memory, client-patterns, onboarding, api-reference). For Python, TypeScript, Go, Ruby, PHP, and Java, read `{lang}/managed-agents/README.md` for code examples. For cURL, read `curl/managed-agents.md`. **Agents are persistent — create once, reference by ID.** Store the agent ID returned by `agents.create` and pass it to every subsequent `sessions.create`; do not call `agents.create` in the request path. The Anthropic CLI (`ant`) is one convenient way to create agents and environments from version-controlled YAML — see `shared/anthropic-cli.md`. If a binding you need isn't shown in the language README, WebFetch the relevant entry from `shared/live-sources.md` rather than guess. C# has beta Managed Agents support via `client.Beta.Agents` and related namespaces.

**When the user wants to set up a Managed Agent from scratch** (e.g. "how do I get started", "walk me through creating one", "set up a new agent"): read `shared/managed-agents-onboarding.md` and run its interview — same flow as the `managed-agents-onboard` subcommand.

**When the user asks "how do I write the client code for X":** reach for `shared/managed-agents-client-patterns.md` — covers lossless stream reconnect, `processed_at` queued/processed gate, interrupt, `tool_confirmation` round-trip, the correct idle/terminated break gate, post-idle status race, stream-first ordering, file-mount gotchas, keeping credentials host-side via custom tools, etc.

---

## Reference Documentation

The relevant documentation for your detected language is included below in `<doc>` tags. Each tag has a `path` attribute showing its original file path. Use this to find the right section:

### Quick Task Reference

**Single text classification/summarization/extraction/Q&A:**
→ Refer to `typescript/claude-api/README.md`

**Chat UI or real-time response display:**
→ Refer to `typescript/claude-api/README.md` + `typescript/claude-api/streaming.md`

**Long-running conversations (may exceed context window):**
→ Refer to `typescript/claude-api/README.md` — see Compaction section

**Migrating to a newer model or replacing a retired model:**
→ Refer to `shared/model-migration.md`

**Prompt caching / optimize caching / "why is my cache hit rate low":**
→ Refer to `shared/prompt-caching.md` + `typescript/claude-api/README.md` (Prompt Caching section)

**Count tokens in a file / prompt / diff ("how many tokens is X"):**
→ Refer to `shared/token-counting.md` — use `messages.count_tokens`, never `tiktoken`

**Function calling / tool use / agents:**
→ Refer to `typescript/claude-api/README.md` + `shared/tool-use-concepts.md` + `typescript/claude-api/tool-use.md`

**Batch processing (non-latency-sensitive):**
→ Refer to `typescript/claude-api/README.md` + `typescript/claude-api/batches.md`

**File uploads across multiple requests:**
→ Refer to `typescript/claude-api/README.md` + `typescript/claude-api/files-api.md`

**Agent design (tool surface, context management, caching strategy):**
→ Refer to `shared/agent-design.md`

**Anthropic CLI (`ant`) — terminal access, version-controlled agent/environment YAML, scripting:**
→ Refer to `shared/anthropic-cli.md`

**Managed Agents (server-managed stateful agents):**
→ Refer to `shared/managed-agents-overview.md` and the rest of the `shared/managed-agents-*.md` files. For Python, TypeScript, and cURL, language-specific code examples live in `typescript/managed-agents/README.md`. Java, Go, Ruby, and PHP also support the API — translate the calls using your SDK's patterns from `typescript/claude-api.md`. C# does not currently have Managed Agents support; use raw HTTP from `curl/managed-agents.md` as a reference.

**Error handling:**
→ Refer to `shared/error-codes.md`

**Latest docs via WebFetch:**
→ Refer to `shared/live-sources.md` for URLs

---

## Included Documentation

<doc path="shared/agent-design.md">
# Agent Design Patterns

This file covers decision heuristics for building agents on the Claude API: which primitives to reach for, how to design your tool surface, and how to manage context and cost over long runs. For per-tool mechanics and code examples, see `tool-use-concepts.md` and the language-specific folders.

---

## Model Parameters

| Parameter | When to use it | What to expect |
| --- | --- | --- |
| **Adaptive thinking** (`thinking: {type: "adaptive"}`) | When you want Claude to control when and how much to think. | Claude determines thinking depth per request and automatically interleaves thinking between tool calls. No token budget to tune. |
| **Effort** (`output_config: {effort: ...}`) | When adjusting the tradeoff between thoroughness and token efficiency. | Lower effort → fewer and more-consolidated tool calls, less preamble, terser confirmations. `medium` is often a favorable balance. Use `max` when correctness matters more than cost. |

See `SKILL.md` §Thinking & Effort for model support and parameter details.

---

## Designing Your Tool Surface

### Bash vs. dedicated tools

Claude doesn't know your application's security boundary, approval policy, or UX surface. Claude emits tool calls; your harness handles them. The shape of those tool calls determines what the harness can do.

A **bash tool** gives Claude broad programmatic leverage — it can perform almost any action. But it gives the harness only an opaque command string, the same shape for every action. Promoting an action to a **dedicated tool** gives the harness an action-specific hook with typed arguments it can intercept, gate, render, or audit.

**When to promote an action to a dedicated tool:**

- **Security boundary.** Actions that require gating are natural candidates. Reversibility is a useful criterion: hard-to-reverse actions (external API calls, sending messages, deleting data) can be gated behind user confirmation. A `send_email` tool is easy to gate; `bash -c "curl -X POST ..."` is not.
- **Staleness checks.** A dedicated `edit` tool can reject writes if the file changed since Claude last read it. Bash can't enforce that invariant.
- **Rendering.** Some actions benefit from custom UI. Claude Code promotes question-asking to a tool so it can render as a modal, present options, and block the agent loop until answered.
- **Scheduling.** Read-only tools like `glob` and `grep` can be marked parallel-safe. When the same actions run through bash, the harness can't tell a parallel-safe `grep` from a parallel-unsafe `git push`, so it must serialize.

**Rule of thumb:** Start with bash for breadth. Promote to dedicated tools when you need to gate, render, audit, or parallelize the action.

---

## Anthropic-Provided Tools

| Tool | Side | When to use it | What to expect |
| --- | --- | --- | --- |
| **Bash** | Client | Claude needs to execute shell commands. | Claude emits commands; your harness executes them. Reference implementation provided. |
| **Text editor** | Client | Claude needs to read or edit files. | Claude views, creates, and edits files via your implementation. Reference implementation provided. |
| **Computer use** | Client or Server | Claude needs to interact with GUIs, web apps, or visual interfaces. | Claude takes screenshots and issues mouse/keyboard commands. Can be self-hosted (you run the environment) or Anthropic-hosted. |
| **Code execution** | Server | Claude needs to run code in a sandbox you don't want to manage. | Anthropic-hosted container with built-in file and bash sub-tools. No client-side execution. |
| **Web search / fetch** | Server | Claude needs information past its training cutoff (news, current events, recent docs) or the content of a specific URL. | Claude issues a query or URL; Anthropic executes it and returns results with citations. |
| **Memory** | Client | Claude needs to save context across sessions. | Claude reads/writes a `/memories` directory. You implement the storage backend. |

**Client-side** tools are defined by Anthropic (name, schema, Claude's usage pattern) but executed by your harness. Anthropic provides reference implementations. **Server-side** tools run entirely on Anthropic infrastructure — declare them in `tools` and Claude handles the rest.

---

## Composing Tool Calls: Programmatic Tool Calling

With standard tool use, each tool call is a round trip: Claude calls the tool, the result lands in Claude's context, Claude reasons about it, then calls the next tool. Three sequential actions (read profile → look up orders → check inventory) means three round trips. Each adds latency and tokens, and most of the intermediate data is never needed again.

**Programmatic tool calling (PTC)** lets Claude compose those calls into a script instead. The script runs in the code execution container. When the script calls a tool, the container pauses, the call is executed (client-side or server-side), and the result returns to the running code — not to Claude's context. The script processes it with normal control flow (loops, filters, branches). Only the script's final output returns to Claude.

| When to use it | What to expect |
| --- | --- |
| Many sequential tool calls, or large intermediate results you want filtered before they hit the context window. | Claude writes code that invokes tools as functions. Runs in the code execution container. Token cost scales with final output, not intermediate results. |

---

## Scaling the Tool and Instruction Set

| Feature | When to use it | What to expect |
| --- | --- | --- |
| **Tool search** | Many tools available, but only a few relevant per request. Don't want all schemas in context upfront. | Claude searches the tool set and loads only relevant schemas. Tool definitions are appended, not swapped — preserves cache (see Caching below). |
| **Skills** | Task-specific instructions Claude should load only when relevant. | Each skill is a folder with a `SKILL.md`. The skill's description sits in context by default; Claude reads the full file when the task calls for it. |

Both patterns keep the fixed context small and load detail on demand.

---

## Long-Running Agents: Managing Context

| Pattern | When to use it | What to expect |
| --- | --- | --- |
| **Context editing** | Context grows stale over many turns (old tool results, completed thinking). | Tool results and thinking blocks are cleared based on configurable thresholds. Keeps the transcript lean without summarizing. |
| **Compaction** | Conversation likely to reach or exceed the context window limit. | Earlier context is summarized into a compaction block server-side. See `SKILL.md` §Compaction for the critical `response.content` handling. |
| **Memory** | State must persist across sessions (not just within one conversation). | Claude reads/writes files in a memory directory. Survives process restarts. |

**Choosing between them:** Context editing and compaction operate within a session — editing prunes stale turns, compaction summarizes when you're near the limit. Memory is for cross-session persistence. Many long-running agents use all three.

---

## Caching for Agents

**Read `prompt-caching.md` first.** It covers the prefix-match invariant, breakpoint placement, the silent-invalidator audit, and why changing tools or models mid-session breaks the cache. This section covers only the agent-specific workarounds for those constraints.

| Constraint (from `prompt-caching.md`) | Agent-specific workaround |
| --- | --- |
| Editing the system prompt mid-session invalidates the cache. | Append a `{"role": "system", ...}` message to `messages[]` instead (beta, on supporting models — see `prompt-caching.md` § Mid-conversation system messages). The cached prefix stays intact, and the model treats it as an operator-authority instruction rather than user text. On models that don't support it, fall back to a `<system-reminder>` text block in the user turn. |
| Switching models mid-session invalidates the cache. | Spawn a **subagent** with the cheaper model for the sub-task; keep the main loop on one model. Claude Code's Explore subagents use Haiku this way. |
| Adding/removing tools mid-session invalidates the cache. | Use **tool search** for dynamic discovery — it appends tool schemas rather than swapping them, so the existing prefix is preserved. |

For multi-turn breakpoint placement, use top-level auto-caching — see `prompt-caching.md` §Placement patterns.

---

For live documentation on any of these features, see `live-sources.md`.
</doc>

<doc path="shared/anthropic-cli.md">
# Anthropic CLI (`ant`)

The `ant` CLI exposes every Claude API resource as a shell subcommand. Compared to `curl`: request bodies are built from typed flags or piped YAML instead of hand-written JSON, `@path` inlines file contents into any string field, `--transform` extracts fields with a GJSON path (no `jq`), list endpoints auto-paginate (cap total results with `--max-items N`; `--limit` only sets the server page size), and the `beta:` prefix auto-sets the right `anthropic-beta` header.

## When to use the CLI vs the SDK

**CLI for the control plane, SDK for the data plane.** Agents and environments are relatively static resources you define, configure, and debug with `ant` — check the YAML into your repo, apply from CI, inspect from a terminal. Sessions are dynamic and driven by your application through the SDK — create per task, stream events, react to tool calls, integrate into your product. Both hit the same API; the split is about where the call lives, not what's possible.

| | Control plane → `ant` | Data plane → SDK |
|---|---|---|
| Resources | agents, environments, skills, vaults, files | sessions, events |
| Cadence | Once per deploy / ad-hoc | Every task / every turn |
| Lives in | `*.yaml` in your repo + CI + terminal | Application code |
| Typical calls | `create < agent.yaml`, `update --version N`, `list`, `retrieve`, `archive`, `--debug` | `sessions.create()`, `events.stream()`, `events.send()` |

## Install and auth

```sh
# macOS
brew install anthropics/tap/ant
xattr -d com.apple.quarantine "$(brew --prefix)/bin/ant"

# Linux / WSL — pick the release from github.com/anthropics/anthropic-cli/releases
curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_$(uname -s | tr A-Z a-z)_$(uname -m | sed -e s/x86_64/amd64/ -e s/aarch64/arm64/).tar.gz" \
  | sudo tar -xz -C /usr/local/bin ant

# Or from source (Go 1.22+)
go install github.com/anthropics/anthropic-cli/cmd/ant@latest
```

**Auth** — the CLI resolves credentials the same way the SDKs do (first match wins): explicit flags, then `ANTHROPIC_API_KEY`, then `ANTHROPIC_AUTH_TOKEN`, then the `ANTHROPIC_PROFILE`-selected or active profile, then Workload Identity Federation env vars, then the default profile on disk. Override the host with `ANTHROPIC_BASE_URL` or `--base-url`.

- **API key**: set `ANTHROPIC_API_KEY` in the environment.
- **OAuth profile** (no static key to manage): `ant auth login` opens a browser, exchanges for a short-lived token, and stores a profile under `$ANTHROPIC_CONFIG_DIR` (default `~/.config/anthropic/` on Linux/macOS, `%APPDATA%\Anthropic` on Windows — `configs/<profile>.json` for settings, `credentials/<profile>.json` for tokens). Subsequent `ant` (and SDK) calls pick it up automatically — a bare `Anthropic()` client works after login, but scripts that read `ANTHROPIC_API_KEY` directly do not. Claude Code and the Claude Agent SDK honor the same profile resolution. `ant auth status` shows which credential source and profile won (it reports status only — don't script against its exit code as a health check); `ant auth logout` clears the active profile (`--all` for every profile). On a remote host without a browser, `ant auth login --no-browser` prints the authorize URL and accepts the code back in the terminal.
- **Non-interactive workloads** (CI, servers, containers): interactive login is for development on your own machine — use Workload Identity Federation instead (see the authentication docs via `shared/live-sources.md`).

> **The #1 auth trap:** profiles are only consulted when no API key is set. A stale exported `ANTHROPIC_API_KEY` silently overrides every profile — requests hit whatever org/workspace that key is scoped to. `ant auth status` shows which source won; unset the key (or per-command: `env -u ANTHROPIC_API_KEY ant …`) before relying on a profile. Truly **unset** it — an empty `ANTHROPIC_API_KEY=""` still wins its precedence slot and authenticates with an empty key. The same shadowing applies in reverse to Claude Code: after `ant auth login`, Claude Code may warn about an auth conflict between the profile and its own `/login` credential — keep one (use the profile and `/logout` in Claude Code, or `ant auth logout` to keep Claude Code's own login).

**Named profiles** — an interactive-login token is bound to a single org+workspace, and the API only shows resources belonging to that workspace. If an agent, session, or file you created "disappears", the usual cause is a token scoped to a different workspace than the one that created it (`ant auth status` shows the active workspace). Multi-workspace work means one profile per workspace:

```sh
ant auth login --profile <name>                  # creates the profile if it doesn't exist; org/workspace picker in browser
ant auth login --profile <name> --workspace-id wrkspc_01...   # bind directly, skip the picker
ant profile activate <name>                      # switch the default profile
ant --profile <name> models list                 # one-off; equivalent: ANTHROPIC_PROFILE=<name> ant models list
ant profile list                                 # inspect
ant profile set workspace_id wrkspc_01... --profile <name>    # edit config keys (workspace_id, base_url, organization_id, …)
```

`ant profile set` edits an existing profile's config — it never creates one, and it does **not** rebind already-issued credentials; run `ant auth login` again under that profile to mint a token for the new target. Pointing `ANTHROPIC_PROFILE` at a profile that doesn't exist is an error, not a fall-through. Refresh tokens eventually hard-expire (they don't slide with use) — when a previously working profile starts failing auth, re-run `ant auth login` before debugging anything else.

**Scopes** — a profile's OAuth scope set is requested at login (`--scope`) and persists on the profile (`scope` is also a `profile set` config key; like other config edits, changing it requires a fresh `ant auth login` to take effect). Privileged scopes — e.g. `org:admin` for organization-administration endpoints — are **not** in the default scope set: pass the full set you want explicitly (`ant auth login --profile admin --scope "... org:admin"`), and the server grants a privileged scope only if your role actually has it. Because the scope set rides on every token the profile mints, keep privileged work on a dedicated profile (`admin` vs `default`) and do day-to-day inference on the unprivileged one, switching with `--profile`/`ANTHROPIC_PROFILE`. Check `ant auth login --help` for the current scope list, and `ant auth status` to see what the active token carries.

To hand the active credential to a subprocess or raw-HTTP script:

```sh
# Bare access token — for curl's Authorization header
curl https://api.anthropic.com/v1/messages \
  -H "Authorization: Bearer $(ant auth print-credentials --access-token)" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: oauth-2025-04-20" \
  -H "content-type: application/json" \
  -d '{"model": "claude-opus-4-8", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello"}]}'

# .env format — sets ANTHROPIC_AUTH_TOKEN (and ANTHROPIC_BASE_URL if the profile has one).
# Output is bare KEY=value (no `export`), so use `set -a` to auto-export for child processes:
set -a; eval "$(ant auth print-credentials --env)"; set +a
python my_script.py   # SDK picks up ANTHROPIC_AUTH_TOKEN
```

OAuth tokens go on `Authorization: Bearer` (not `x-api-key:`) **plus the `anthropic-beta: oauth-2025-04-20` header** — converting a raw curl/httpx script from an API key is a header change, not a key swap. The beta header requirement is endpoint-dependent (some endpoints happen to work without it; `/v1/messages` does not) — always send it so requests don't break when you switch endpoints. The token is short-lived and not auto-refreshed when passed via env var, so re-run `print-credentials` before it expires for long-running scripts (`print-credentials` itself refreshes the token if needed). If both `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` are set, the SDKs send both and the API rejects the request — unset `ANTHROPIC_API_KEY` before `eval`ing the `--env` output.

**Foot-gun:** `ant auth print-credentials` with **no flags** prints the entire credentials JSON, not the bare token — putting that in an `Authorization` header yields an empty response or HTTP/2 protocol error. Always use `--access-token` for headers (it always reads the named/active profile; a set `ANTHROPIC_API_KEY` doesn't override credential printing).

## Command structure

```
ant <resource>[:<subresource>] <action> [flags]
```

Beta resources (agents, sessions, environments, deployments, skills, vaults, memory stores) live under `beta:` — the CLI auto-sends the right `anthropic-beta` header, so don't pass it yourself unless overriding with `--beta <header>`. For self-hosted environments, `ant beta:worker poll/run` and `ant beta:environments:work stats/stop` drive and monitor the work queue — see `shared/managed-agents-self-hosted-sandboxes.md`.

```sh
ant models list
ant messages create --model claude-opus-4-8 --max-tokens 1024 --message '{role: user, content: "Hello"}'
ant beta:agents retrieve --agent-id agent_01...
ant beta:sessions:events list --session-id session_01...
```

`ant --help` lists resources; append `--help` to any subcommand for its flags.

## Global flags

| Flag | Purpose |
| --- | --- |
| `--format` | `auto` (default: pretty if TTY, compact if piped), `json`, `jsonl`, `yaml`, `pretty`, `raw`, `explore` (interactive TUI) |
| `--transform` | GJSON path applied to the response (per-item on list endpoints). Not applied when `--format raw`. |
| `-r`, `--raw-output` | If the transformed result is a string, print it without quotes (jq semantics). Pair with `--transform` for scalar capture. |
| `--max-items` | Cap total results returned from auto-paginating list endpoints (distinct from `--limit`, which is the server page size). |
| `--format-error` / `--transform-error` | Same as `--format`/`--transform`, applied to error responses. `-r` does not apply to the error path — use `--format-error yaml` for unquoted error scalars. |
| `--base-url` | Override API host |
| `--debug` | Print full HTTP request + response to stderr (API key redacted) |

## Output — `--transform` + `--format`

`--transform` takes a [GJSON path](https://github.com/tidwall/gjson/blob/master/SYNTAX.md). On list endpoints it runs **per item**, not on the envelope.

```sh
ant beta:agents list --transform '{id,name,model}' --format jsonl
```

**Extract a scalar for shell use:** pair `--transform` with `-r` (`--raw-output` — prints strings unquoted, jq-style):

```sh
AGENT_ID=$(ant beta:agents create --name "My Agent" --model '{id: claude-sonnet-4-6}' \
  --transform id -r)
```

## Input — flags, stdin, `@file`

**Flags** — scalar fields map directly. Structured fields accept relaxed-YAML syntax (unquoted keys) or strict JSON. Repeatable flags build arrays (each `--tool`, `--event`, `--message` appends one element):

```sh
ant beta:agents create \
  --name "Research Agent" \
  --model '{id: claude-opus-4-8}' \
  --tool '{type: agent_toolset_20260401}' \
  --tool '{type: custom, name: search_docs, input_schema: {type: object, properties: {query: {type: string}}}}'
```

**Stdin** — pipe a full JSON or YAML body. Merged with flags; flags win on conflict (for array fields, any flag **replaces** the stdin array entirely — it does not append). Quote the heredoc delimiter (`<<'YAML'`) to disable shell expansion inside the body:

```sh
ant beta:agents create <<'YAML'
name: Research Agent
model: claude-opus-4-8
system: |
  You are a research assistant. Cite sources for every claim.
tools:
  - type: agent_toolset_20260401
YAML
```

**`@file` references** — inline a file's contents into any string-valued field. Inside structured flag values, quote the path. Binary files are auto-base64'd; force with `@file://` (text) or `@data://` (base64). Escape a literal leading `@` as `\@`.

```sh
ant beta:agents create --name "Researcher" --model '{id: claude-sonnet-4-6}' --system @./prompts/researcher.txt

ant messages create --model claude-opus-4-8 --max-tokens 1024 \
  --message '{role: user, content: [
    {type: document, source: {type: base64, media_type: application/pdf, data: "@./scan.pdf"}},
    {type: text, text: "Extract the text from this scanned document."}
  ]}' \
  --transform 'content.0.text' -r
```

Flags that natively take a file path (e.g. `--file` on `beta:files upload`) accept a bare path without `@`.

## Version-controlled Managed Agents resources

This is the recommended flow for defining agents and environments — check the YAML into your repo and sync via `create` (first time) / `update` (thereafter). See `shared/managed-agents-core.md` for the field reference.

```yaml
# summarizer.agent.yaml
name: Summarizer
model: claude-sonnet-4-6
system: |
  You are a helpful assistant that writes concise summaries.
tools:
  - type: agent_toolset_20260401
```

```sh
# Create (once) — capture the ID
AGENT_ID=$(ant beta:agents create < summarizer.agent.yaml --transform id -r)

# Update (CI) — needs ID + current version (optimistic lock)
ant beta:agents update --agent-id "$AGENT_ID" --version 1 < summarizer.agent.yaml
```

Same pattern for environments (`ant beta:environments create|update < env.yaml`), then start a session with both IDs:

```sh
ant beta:sessions create --agent "$AGENT_ID" --environment-id "$ENV_ID" --title "Task"
ant beta:sessions:events send --session-id "$SID" \
  --event '{type: user.message, content: [{type: text, text: "Summarize X"}]}'
ant beta:sessions:events list --session-id "$SID" --transform 'content.0.text' -r
ant beta:sessions:events stream --session-id "$SID"   # live event stream
```

### Interactive session loop (stream-before-send)

`ant beta:sessions:events stream` only delivers events emitted *after* the stream opens — so open it **before** sending the kickoff to avoid missing early events. Use process substitution to hold the stream on a file descriptor, send, then read:

```sh
exec {stream}< <(ant beta:sessions:events stream --session-id "$SID" \
  --transform '{type,text:content.#(type=="text").text,err:error.message}' --format yaml)

ant beta:sessions:events send --session-id "$SID" > /dev/null <<'YAML'
events:
  - type: user.message
    content:
      - type: text
        text: Summarize the repo README
YAML

type=
while IFS= read -r -u "$stream" line; do
  case "$line" in
    type:\ session.status_idle) break ;;
    type:\ session.error)
      IFS= read -r -u "$stream" next || next=
      case "$next" in err:\ *) msg=${next#err: } ;; *) msg=unknown ;; esac
      printf '\n[Error: %s]\n' "$msg"; break ;;
    type:\ *) type=${line#type: } ;;
    text:*)
      [[ $type == agent.message ]] || continue
      val=${line#text: }
      case "$val" in '|-'|'|') ;; *) printf '%s' "$val" ;; esac ;;
    \ \ *)
      if [[ $type == agent.message ]]; then printf '%s\n' "${line#  }"; fi ;;
  esac
done
exec {stream}<&-
```

This works for interactive exploration and demos. For application code that needs to react to `agent.tool_use` / `agent.custom_tool_use` events, reconnect after drops, or dedup against `events.list`, use the SDK — see `shared/managed-agents-client-patterns.md`.

## Scripting patterns

`--transform id -r` on a list endpoint emits one bare ID per line — compose with `xargs`, or use `--max-items N` to bound the result set without piping through `head`:

```sh
FIRST=$(ant beta:agents list --transform id -r --max-items 1)
ant beta:agents:versions list --agent-id "$FIRST" --transform '{version,created_at}' --format jsonl
```

Error shaping mirrors the success path (note: `-r` does not apply to error output — use `--format-error yaml` for an unquoted scalar here):

```sh
ant beta:agents retrieve --agent-id bogus --transform-error error.message --format-error yaml 2>&1
```

Shell completion: `ant @completion {zsh|bash|fish|powershell}`.

For the full, always-current reference (including per-endpoint flags), WebFetch the **Anthropic CLI** URL in `shared/live-sources.md`.
</doc>

<doc path="shared/claude-platform-on-aws.md">
# Claude Platform on AWS

**Anthropic-operated** access to the Claude Developer Platform through AWS infrastructure — SigV4 authentication, AWS IAM access control, and AWS Marketplace billing. Because Anthropic operates it, **the API surface matches first-party with same-day parity**: Managed Agents, server-side tools, batches, Files, and every feature in this skill work the same way (**except self-hosted sandboxes** — `config:{type:"self_hosted"}` is not available here; use `cloud`). Model IDs are the bare first-party strings (`claude-opus-4-8`, `claude-sonnet-4-6`) — **no provider prefix**.

> **Not the same as Amazon Bedrock.** Bedrock is partner-operated (AWS runs the service; release schedules vary, feature subset, `anthropic.`-prefixed model IDs). Claude Platform on AWS and Bedrock coexist; pick by whether you need AWS-native IAM/billing with full Anthropic API parity (this page) vs. Bedrock's own ecosystem.

---

## Client & install

| Language | Install | Client |
|---|---|---|
| Python | `pip install -U "anthropic[aws]"` | `from anthropic import AnthropicAWS` → `AnthropicAWS()` |
| TypeScript | `npm install @anthropic-ai/aws-sdk` | `import AnthropicAws from "@anthropic-ai/aws-sdk"` → `new AnthropicAws()` |
| Go | `go get github.com/anthropics/anthropic-sdk-go` | `import anthropicaws "github.com/anthropics/anthropic-sdk-go/aws"` → `anthropicaws.NewClient(ctx, anthropicaws.ClientConfig{})` |
| C# | `dotnet add package Anthropic.Aws` | `new AnthropicAwsClient()` |
| Java | See SDK repo in `shared/live-sources.md` | See SDK repo in `shared/live-sources.md` |
| Ruby | `gem install anthropic aws-sdk-core` | See SDK repo in `shared/live-sources.md` |
| PHP | `composer require anthropic-ai/sdk aws/aws-sdk-php` | See SDK repo in `shared/live-sources.md` |

After construction, **use the client exactly as you would `Anthropic()`** — `client.messages.create(...)`, `client.beta.sessions.*`, etc., with bare model IDs.

```python
from anthropic import AnthropicAWS

client = AnthropicAWS()  # region + workspace_id from env; see below
client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
```

---

## Required configuration

Two values must be available (constructor args or environment) — **there is no default fallback** for either:

| Value | Env var | Notes |
|---|---|---|
| AWS region | `AWS_REGION` | Required. Unlike `AnthropicBedrock`, there is no `us-east-1` fallback. |
| Workspace ID | `ANTHROPIC_AWS_WORKSPACE_ID` | Required. Routes requests to your Claude workspace. |

Endpoint pattern: `https://aws-external-anthropic.{region}.api.aws/v1/...`. Requests are SigV4-signed with service name `aws-external-anthropic`.

## Authentication

The client resolves AWS credentials via the standard precedence chain: explicit constructor args → environment (`AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_SESSION_TOKEN`) → shared profile → assumed role / instance metadata.

**Short-term API keys** are also supported for cases where SigV4 isn't practical (e.g., browser, simple scripts). Mint one with the per-language token-generator package; pass it as `api_key` on the client. Lifetime is the **lesser of** the requested duration, the underlying credential's expiry, and **12 hours**. For package names and IAM details, WebFetch the Claude Platform on AWS page in `shared/live-sources.md`.

---

## What to tell users

- Treat it as first-party: every section of this skill applies unchanged. Do **not** apply Bedrock's feature-availability mask.
- Model IDs are bare (`claude-opus-4-8`). Do **not** add an `anthropic.` prefix.
- A missing region or `workspace_id` throws at client-construction time (no request is sent). A **403** means the request reached the server — check for a **wrong** `workspace_id` or a missing IAM action on the principal. See the IAM actions reference in `shared/live-sources.md`.
</doc>

<doc path="shared/error-codes.md">
# HTTP Error Codes Reference

This file documents HTTP error codes returned by the Claude API, their common causes, and how to handle them. For language-specific error handling examples, see the `python/` or `typescript/` folders.

## Error Code Summary

| Code | Error Type              | Retryable | Common Cause                         |
| ---- | ----------------------- | --------- | ------------------------------------ |
| 400  | `invalid_request_error` | No        | Invalid request format or parameters |
| 401  | `authentication_error`  | No        | Invalid or missing API key           |
| 403  | `permission_error`      | No        | API key lacks permission             |
| 404  | `not_found_error`       | No        | Invalid endpoint or model ID         |
| 413  | `request_too_large`     | No        | Request exceeds size limits          |
| 429  | `rate_limit_error`      | Yes       | Too many requests                    |
| 500  | `api_error`             | Yes       | Anthropic service issue              |
| 529  | `overloaded_error`      | Yes       | API is temporarily overloaded        |

## Detailed Error Information

### 400 Bad Request

**Causes:**

- Malformed JSON in request body
- Missing required parameters (`model`, `max_tokens`, `messages`)
- Invalid parameter types (e.g., string where integer expected)
- Empty messages array
- Messages not alternating user/assistant

**Example error:**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "messages: roles must alternate between \"user\" and \"assistant\""
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

**Fix:** Validate request structure before sending. Check that:

- `model` is a valid model ID
- `max_tokens` is a positive integer
- `messages` array is non-empty and alternates correctly

---

### 401 Unauthorized

**Causes:**

- Missing `x-api-key` header or `Authorization` header
- Invalid API key format
- Revoked or deleted API key
- OAuth bearer token sent via `x-api-key` instead of `Authorization: Bearer`
- Both `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` set — the SDK sends both headers and the API rejects the request

**Fix:** Set `ANTHROPIC_API_KEY`, or run `ant auth login` and leave the client constructor empty. For raw HTTP with an OAuth token, use `Authorization: Bearer <token>` (not `x-api-key:`).

---

### 403 Forbidden

**Causes:**

- API key doesn't have access to the requested model
- Organization-level restrictions
- Attempting to access beta features without beta access

**Fix:** Check your API key permissions in the Console. You may need a different API key or to request access to specific features.

---

### 404 Not Found

**Causes:**

- Typo in model ID (e.g., `claude-sonnet-4.6` instead of `claude-sonnet-4-6`)
- Using deprecated model ID
- Invalid API endpoint

**Fix:** Use exact model IDs from the models documentation. You can use aliases (e.g., `claude-opus-4-8`).

---

### 413 Request Too Large

**Causes:**

- Request body exceeds maximum size
- Too many tokens in input
- Image data too large

**Fix:** Reduce input size — truncate conversation history, compress/resize images, or split large documents into chunks.

---

### 400 Validation Errors

Some 400 errors are specifically related to parameter validation:

- `max_tokens` exceeds model's limit
- Invalid `temperature` value (must be 0.0-1.0)
- `budget_tokens` >= `max_tokens` in extended thinking
- Invalid tool definition schema

**Model-specific 400s on Fable 5 / Opus 4.8 / 4.7:**

- `temperature`, `top_p`, `top_k` are removed — sending any of them returns 400. Delete the parameter; see `shared/model-migration.md` → Per-SDK Syntax Reference.
- `thinking: {type: "enabled", budget_tokens: N}` is removed — sending it returns 400. Use `thinking: {type: "adaptive"}` instead.
- **Fable 5 only:** an explicit `thinking: {type: "disabled"}` returns 400 (it is accepted on Opus 4.8/4.7). Omit the `thinking` param entirely instead.

**Common mistake with extended thinking on older models (Opus 4.6 and earlier):**

```
# Wrong: budget_tokens must be < max_tokens
thinking: budget_tokens=10000, max_tokens=1000  → Error!

# Correct
thinking: budget_tokens=10000, max_tokens=16000
```

---

### 429 Rate Limited

**Causes:**

- Exceeded requests per minute (RPM)
- Exceeded tokens per minute (TPM)
- Exceeded tokens per day (TPD)

**Headers to check:**

- `retry-after`: Seconds to wait before retrying
- `x-ratelimit-limit-*`: Your limits
- `x-ratelimit-remaining-*`: Remaining quota

**Fix:** The Anthropic SDKs automatically retry 429 and 5xx errors with exponential backoff (default: `max_retries=2`). For custom retry behavior, see the language-specific error handling examples.

---

### 500 Internal Server Error

**Causes:**

- Temporary Anthropic service issue
- Bug in API processing

**Fix:** Retry with exponential backoff. If persistent, check [status.anthropic.com](https://status.anthropic.com).

---

### 529 Overloaded

**Causes:**

- High API demand
- Service capacity reached

**Fix:** Retry with exponential backoff. Consider using a different model (Haiku is often less loaded), spreading requests over time, or implementing request queuing.

---

## Common Mistakes and Fixes

| Mistake                         | Error            | Fix                                                     |
| ------------------------------- | ---------------- | ------------------------------------------------------- |
| `temperature`/`top_p`/`top_k` on Fable 5 / Opus 4.8 / 4.7 | 400 | Remove the parameter (see `shared/model-migration.md`)  |
| `budget_tokens` on Fable 5 / Opus 4.8 / 4.7 | 400  | Use `thinking: {type: "adaptive"}`                      |
| `thinking: {type: "disabled"}` on Fable 5 | 400    | Omit the `thinking` param entirely (accepted on Opus 4.8/4.7) |
| `budget_tokens` >= `max_tokens` (older models) | 400 | Ensure `budget_tokens` < `max_tokens`                  |
| Typo in model ID                | 404              | Use valid model ID like `claude-opus-4-8`               |
| First message is `assistant`    | 400              | First message must be `user`                            |
| Consecutive same-role messages  | 400              | Alternate `user` and `assistant`                        |
| API key in code                 | 401 (leaked key) | Use environment variable                                |
| Custom retry needs              | 429/5xx          | SDK retries automatically; customize with `max_retries` |

## Typed Exceptions in SDKs

**Always use the SDK's typed exception classes** instead of checking error messages with string matching. Each HTTP error code maps to a specific exception class:

| HTTP Code | TypeScript Class                  | Python Class                      |
| --------- | --------------------------------- | --------------------------------- |
| 400       | `Anthropic.BadRequestError`       | `anthropic.BadRequestError`       |
| 401       | `Anthropic.AuthenticationError`   | `anthropic.AuthenticationError`   |
| 403       | `Anthropic.PermissionDeniedError` | `anthropic.PermissionDeniedError` |
| 404       | `Anthropic.NotFoundError`         | `anthropic.NotFoundError`         |
| 413       | `Anthropic.RequestTooLargeError`  | `anthropic.RequestTooLargeError`  |
| 429       | `Anthropic.RateLimitError`        | `anthropic.RateLimitError`        |
| 500+      | `Anthropic.InternalServerError`   | `anthropic.InternalServerError`   |
| 529       | `Anthropic.OverloadedError`       | `anthropic.OverloadedError`       |
| Any       | `Anthropic.APIError`              | `anthropic.APIError`              |

```typescript
// ✅ Correct: use typed exceptions
try {
  const response = await client.messages.create({...});
} catch (error) {
  if (error instanceof Anthropic.RateLimitError) {
    // Handle rate limiting
  } else if (error instanceof Anthropic.APIError) {
    console.error(`API error ${error.status}:`, error.message);
  }
}

// ❌ Wrong: don't check error messages with string matching
try {
  const response = await client.messages.create({...});
} catch (error) {
  const msg = error instanceof Error ? error.message : String(error);
  if (msg.includes("429") || msg.includes("rate_limit")) { ... }
}
```

All exception classes extend `Anthropic.APIError`, which has a `status` property. Use `instanceof` checks from most specific to least specific (e.g., check `RateLimitError` before `APIError`).

### Error `.type` Field

All `APIStatusError` subclasses now expose a `.type` property (Python: `.type`, TypeScript: `.type`, Java: `.errorType()`, Go: `.Type()`, Ruby: `.type`, PHP: `.type`) that returns the API error type string (e.g., `"invalid_request_error"`, `"authentication_error"`, `"rate_limit_error"`, `"overloaded_error"`). Use this for programmatic error classification when you need finer granularity than the HTTP status code — for example, distinguishing `"billing_error"` from `"permission_error"` (both map to 403).

```python
except anthropic.APIStatusError as e:
    if e.type == "rate_limit_error":
        # handle rate limiting
    elif e.type == "overloaded_error":
        # handle overload
```
</doc>

<doc path="shared/live-sources.md">
# Live Documentation Sources

This file contains WebFetch URLs for fetching current information from platform.claude.com and Agent SDK repositories. Use these when users need the latest data that may have changed since the cached content was last updated.

## When to Use WebFetch

- User explicitly asks for "latest" or "current" information
- Cached data seems incorrect
- User asks about features not covered in cached content
- User needs specific API details or examples

## Claude API Documentation URLs

### Models & Pricing

| Topic           | URL                                                                          | Extraction Prompt                                                               |
| --------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Models Overview | `https://platform.claude.com/docs/en/about-claude/models/overview.md`        | "Extract current model IDs, context windows, and pricing for all Claude models" |
| Migration Guide | `https://platform.claude.com/docs/en/about-claude/models/migration-guide.md` | "Extract breaking changes, deprecated parameters, and per-model migration steps when moving to a newer Claude model" |
| Pricing         | `https://platform.claude.com/docs/en/pricing.md`                             | "Extract current pricing per million tokens for input and output"               |

### Core Features

| Topic             | URL                                                                          | Extraction Prompt                                                                      |
| ----------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Extended Thinking | `https://platform.claude.com/docs/en/build-with-claude/extended-thinking.md` | "Extract extended thinking parameters, budget_tokens requirements, and usage examples" |
| Adaptive Thinking | `https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md` | "Extract adaptive thinking setup, effort levels, and Claude Opus 4.8 usage examples"         |
| Effort Parameter  | `https://platform.claude.com/docs/en/build-with-claude/effort.md`            | "Extract effort levels, cost-quality tradeoffs, and interaction with thinking"        |
| Tool Use          | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md`  | "Extract tool definition schema, tool_choice options, and handling tool results"       |
| Streaming         | `https://platform.claude.com/docs/en/build-with-claude/streaming.md`         | "Extract streaming event types, SDK examples, and best practices"                      |
| Prompt Caching    | `https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md`    | "Extract cache_control usage, pricing benefits, and implementation examples"           |

### Media & Files

| Topic       | URL                                                                    | Extraction Prompt                                                 |
| ----------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Vision      | `https://platform.claude.com/docs/en/build-with-claude/vision.md`      | "Extract supported image formats, size limits, and code examples" |
| PDF Support | `https://platform.claude.com/docs/en/build-with-claude/pdf-support.md` | "Extract PDF handling capabilities, limits, and examples"         |

### API Operations

| Topic            | URL                                                                         | Extraction Prompt                                                                                       |
| ---------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Batch Processing | `https://platform.claude.com/docs/en/build-with-claude/batch-processing.md` | "Extract batch API endpoints, request format, and polling for results"                                  |
| Files API        | `https://platform.claude.com/docs/en/build-with-claude/files.md`            | "Extract file upload, download, and referencing in messages, including supported types and beta header" |
| Token Counting   | `https://platform.claude.com/docs/en/build-with-claude/token-counting.md`   | "Extract token counting API usage and examples"                                                         |
| Rate Limits      | `https://platform.claude.com/docs/en/api/rate-limits.md`                    | "Extract current rate limits by tier and model"                                                         |
| Errors           | `https://platform.claude.com/docs/en/api/errors.md`                         | "Extract HTTP error codes, meanings, and retry guidance"                                                |
| Amazon Bedrock   | `https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock.md` | "Extract the AnthropicBedrockMantle client per language, `anthropic.`-prefixed model IDs, auth paths, feature availability, and regions" |
| Claude Platform on AWS | `https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws.md` | "Extract the AnthropicAWS client per language, SigV4 auth, credential precedence, short-term API keys, workspace_id, and region requirements" |
| Claude Platform on AWS — IAM actions | `https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions.md` | "Extract the IAM action names, resource ARNs, and policy examples required for each API capability" |

### Tools

| Topic          | URL                                                                                    | Extraction Prompt                                                                        |
| -------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Code Execution | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md` | "Extract code execution tool setup, file upload, container reuse, and response handling" |
| Computer Use   | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use.md`        | "Extract computer use tool setup, capabilities, and implementation examples"             |
| Bash Tool      | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool.md`           | "Extract bash tool schema, reference implementation, and security considerations"        |
| Text Editor    | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool.md`    | "Extract text editor tool commands, schema, and reference implementation"                |
| Memory Tool    | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md`         | "Extract memory tool commands, directory structure, and implementation patterns"         |
| Tool Search    | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool.md`    | "Extract tool search setup, when to use, and cache interaction"                          |
| Programmatic Tool Calling | `https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling.md` | "Extract PTC setup, script execution model, and tool invocation from code"    |
| Skills         | `https://platform.claude.com/docs/en/agents-and-tools/skills.md`                       | "Extract skill folder structure, SKILL.md format, and loading behavior"                  |

### Advanced Features

| Topic              | URL                                                                           | Extraction Prompt                                   |
| ------------------ | ----------------------------------------------------------------------------- | --------------------------------------------------- |
| Structured Outputs | `https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md` | "Extract output_config.format usage and schema enforcement"                           |
| Compaction         | `https://platform.claude.com/docs/en/build-with-claude/compaction.md`         | "Extract compaction setup, trigger config, and streaming with compaction"             |
| Context Editing    | `https://platform.claude.com/docs/en/build-with-claude/context-editing.md`    | "Extract context editing thresholds, what gets cleared, and configuration"            |
| Citations          | `https://platform.claude.com/docs/en/build-with-claude/citations.md`          | "Extract citation format and implementation"        |
| Context Windows    | `https://platform.claude.com/docs/en/build-with-claude/context-windows.md`    | "Extract context window sizes and token management" |

### Managed Agents

Use these when a managed-agents binding, behavior, or wire-level detail isn't covered in the cached `shared/managed-agents-*.md` concept files or in `{lang}/managed-agents/README.md`.

| Topic                 | URL                                                                              | Extraction Prompt                                                                               |
| --------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Overview              | `https://platform.claude.com/docs/en/managed-agents/overview.md`                 | "Extract the high-level architecture and how agents/sessions/environments/vaults fit together" |
| Quickstart            | `https://platform.claude.com/docs/en/managed-agents/quickstart.md`               | "Extract the minimal end-to-end agent → environment → session → stream code path"              |
| Agent Setup           | `https://platform.claude.com/docs/en/managed-agents/agent-setup.md`              | "Extract agent create/update/list-versions/archive lifecycle and parameters"                   |
| Define Outcomes       | `https://platform.claude.com/docs/en/managed-agents/define-outcomes.md`          | "Extract outcome definitions, evaluation hooks, and success criteria configuration"             |
| Sessions              | `https://platform.claude.com/docs/en/managed-agents/sessions.md`                 | "Extract session lifecycle, status transitions, idle/terminated semantics, and resume rules"    |
| Environments          | `https://platform.claude.com/docs/en/managed-agents/environments.md`             | "Extract environment config (cloud/networking), management endpoints, and reuse model"          |
| Self-Hosted Sandboxes | `https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes.md`    | "Extract config:{type:self_hosted}, ANTHROPIC_ENVIRONMENT_KEY, EnvironmentWorker.run/run_one, beta_agent_toolset, ant beta:worker poll/run, webhook-driven wake" |
| Self-Hosted Sandboxes — Security | `https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security.md` | "Extract what the customer owns (hardening, egress, key custody, trust boundaries) vs what Anthropic cannot do" |
| Events and Streaming  | `https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md`     | "Extract event stream types, stream-first ordering, reconnect/dedupe, and steering patterns"    |
| Tools                 | `https://platform.claude.com/docs/en/managed-agents/tools.md`                    | "Extract built-in toolset, custom tool definitions, and tool result wire format"                |
| Files                 | `https://platform.claude.com/docs/en/managed-agents/files.md`                    | "Extract file upload, mount paths, session resources, and listing/downloading session outputs"  |
| Permission Policies   | `https://platform.claude.com/docs/en/managed-agents/permission-policies.md`      | "Extract permission policy types (allow/deny/confirm) and per-tool config"                     |
| Multi-Agent           | `https://platform.claude.com/docs/en/managed-agents/multi-agent.md`              | "Extract multi-agent composition patterns, sub-agent invocation, and result handoff"            |
| Observability         | `https://platform.claude.com/docs/en/managed-agents/observability.md`            | "Extract logging, tracing, and usage telemetry exposed by managed agents"                       |
| Webhooks              | `https://platform.claude.com/docs/en/managed-agents/webhooks.md`                 | "Extract webhook endpoint registration, HMAC signature verification, supported event types, and delivery semantics" |
| GitHub                | `https://platform.claude.com/docs/en/managed-agents/github.md`                   | "Extract github_repository resource shape, multi-repo mounting, and token rotation"             |
| MCP Connector         | `https://platform.claude.com/docs/en/managed-agents/mcp-connector.md`            | "Extract MCP server declaration on agents and vault-based credential injection at session"     |
| Vaults                | `https://platform.claude.com/docs/en/managed-agents/vaults.md`                   | "Extract vault create, credential add/rotate, OAuth refresh shape, and archive"                 |
| Skills                | `https://platform.claude.com/docs/en/managed-agents/skills.md`                   | "Extract skill packaging and loading model for managed agents"                                  |
| Memory                | `https://platform.claude.com/docs/en/managed-agents/memory.md`                   | "Extract memory resource shape, scoping, and lifecycle"                                         |
| Onboarding            | `https://platform.claude.com/docs/en/managed-agents/onboarding.md`               | "Extract first-run setup, prerequisites, and account/region requirements"                      |
| Cloud Containers      | `https://platform.claude.com/docs/en/managed-agents/cloud-containers.md`         | "Extract cloud container runtime, image config, and network/storage knobs"                     |
| Migration             | `https://platform.claude.com/docs/en/managed-agents/migration.md`                | "Extract migration paths from earlier APIs/preview shapes to GA managed agents"                 |

### Anthropic CLI

The `ant` CLI provides terminal access to the Claude API. Every API resource is exposed as a subcommand. It is one convenient way to create agents, environments, sessions, and other resources from version-controlled YAML, and to inspect responses interactively.

| Topic         | URL                                                     | Extraction Prompt                                                                                  |
| ------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Anthropic CLI | `https://platform.claude.com/docs/en/api/sdks/cli.md`   | "Extract CLI install, authentication, command structure, and the beta:agents/environments/sessions commands" |
| Authentication overview | `https://platform.claude.com/docs/en/manage-claude/authentication.md` | "Extract the credential options (API keys, interactive OAuth login, Workload Identity Federation) and when to use each" |
| WIF reference | `https://platform.claude.com/docs/en/manage-claude/wif-reference.md`  | "Extract credential precedence order, the profile configuration file schema, and the configuration directory layout" |

---

## Claude API SDK Repositories

WebFetch these when a binding (class, method, namespace, field) isn't covered in the cached `{lang}/` skill files or in the managed-agents docs above. The SDKs include beta managed-agents support for `/v1/agents`, `/v1/sessions`, `/v1/environments`, and related resources — search the repo for `BetaManagedAgents`, `beta.agents`, `beta.sessions`, or the equivalent namespace for that language.

| SDK        | URL                                                      | Extraction Prompt                                                                                                       |
| ---------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Python     | `https://github.com/anthropics/anthropic-sdk-python`     | "Extract beta managed-agents namespaces, classes, and method signatures (`client.beta.agents`, `client.beta.sessions`)" |
| TypeScript | `https://github.com/anthropics/anthropic-sdk-typescript` | "Extract beta managed-agents namespaces, classes, and method signatures (`client.beta.agents`, `client.beta.sessions`)" |
| Java       | `https://github.com/anthropics/anthropic-sdk-java`       | "Extract beta managed-agents classes, builders, and method signatures (`client.beta().agents()`, `BetaManagedAgents*`)" |
| Go         | `https://github.com/anthropics/anthropic-sdk-go`         | "Extract beta managed-agents types and method signatures (`client.Beta.Agents`, `BetaManagedAgents*` event types)"      |
| Ruby       | `https://github.com/anthropics/anthropic-sdk-ruby`       | "Extract beta managed-agents methods and parameter shapes (`client.beta.agents`, `client.beta.sessions`)"               |
| C#         | `https://github.com/anthropics/anthropic-sdk-csharp`     | "Extract beta managed-agents classes and method signatures (NuGet package, `BetaManagedAgents*` types)"                 |
| PHP        | `https://github.com/anthropics/anthropic-sdk-php`        | "Extract beta managed-agents classes and method signatures (`$client->beta->agents`, `BetaManagedAgents*` params)"      |

---

## Fallback Strategy

If WebFetch fails (network issues, URL changed):

1. Use cached content from the language-specific files (note the cache date)
2. Inform user the data may be outdated
3. Suggest they check platform.claude.com or the GitHub repos directly
</doc>

<doc path="shared/managed-agents-api-reference.md">
# Managed Agents — Endpoint Reference

All endpoints require `x-api-key` and `anthropic-version: 2023-06-01` headers. Managed Agents endpoints additionally require the `anthropic-beta` header.

## Beta Headers

```
anthropic-beta: managed-agents-2026-04-01
```

The SDK adds this header automatically for all `client.beta.{agents,environments,sessions,vaults,memory_stores}.*` calls. Skills endpoints use `skills-2025-10-02`; Files endpoints use `files-api-2025-04-14`.

---

## SDK Method Reference

All resources are under the `beta` namespace. Python and TypeScript share identical method names.

| Resource | Python / TypeScript (`client.beta.*`) | Go (`client.Beta.*`) |
| --- | --- | --- |
| Agents | `agents.create` / `retrieve` / `update` / `list` / `archive` | `Agents.New` / `Get` / `Update` / `List` / `Archive` |
| Agent Versions | `agents.versions.list` | `Agents.Versions.List` |
| Environments | `environments.create` / `retrieve` / `update` / `list` / `delete` / `archive` | `Environments.New` / `Get` / `Update` / `List` / `Delete` / `Archive` |
| Environment Work (self-hosted) | `environments.work.poller` / `stats` / `stop` | See `shared/managed-agents-self-hosted-sandboxes.md` |
| Sessions | `sessions.create` / `retrieve` / `update` / `list` / `delete` / `archive` | `Sessions.New` / `Get` / `Update` / `List` / `Delete` / `Archive` |
| Session Events | `sessions.events.list` / `send` / `stream` | `Sessions.Events.List` / `Send` / `StreamEvents` |
| Session Threads | `sessions.threads.list` / `retrieve` / `archive`; `sessions.threads.events.list` / `stream` | `Sessions.Threads.List` / `Get` / `Archive`; `Sessions.Threads.Events.List` / `StreamEvents` |
| Session Resources | `sessions.resources.add` / `retrieve` / `update` / `list` / `delete` | `Sessions.Resources.Add` / `Get` / `Update` / `List` / `Delete` |
| Vaults | `vaults.create` / `retrieve` / `update` / `list` / `delete` / `archive` | `Vaults.New` / `Get` / `Update` / `List` / `Delete` / `Archive` |
| Credentials | `vaults.credentials.create` / `retrieve` / `update` / `list` / `delete` / `archive` / `mcp_oauth_validate` | `Vaults.Credentials.New` / `Get` / `Update` / `List` / `Delete` / `Archive` / `McpOauthValidate` |
| Memory Stores | `memory_stores.create` / `retrieve` / `update` / `list` / `delete` / `archive` | `MemoryStores.New` / `Get` / `Update` / `List` / `Delete` / `Archive` |
| Memories | `memory_stores.memories.create` / `retrieve` / `update` / `list` / `delete` | `MemoryStores.Memories.New` / `Get` / `Update` / `List` / `Delete` |
| Memory Versions | `memory_stores.memory_versions.list` / `retrieve` / `redact` | `MemoryStores.MemoryVersions.List` / `Get` / `Redact` |

**Naming quirks to watch for:**
- Agents and Session Threads have **no delete** — only `archive`. Archive is **permanent**: the agent becomes read-only, new sessions cannot reference it, and there is no unarchive. Confirm with the user before archiving a production agent. Environments, Sessions, Vaults, Credentials, and Memory Stores have both `delete` and `archive`; Session Resources, Files, Skills, and Memories are `delete`-only; Memory Versions have neither — only `redact`.
- Session resources use `add` (not `create`).
- Go's event stream is `StreamEvents` (not `Stream`).
- The self-hosted worker is **not** under `client.beta.*` — it's `EnvironmentWorker` from `anthropic.lib.environments` / `@anthropic-ai/sdk/helpers/beta/environments`; only `environments.work.poller/stats/stop` are client methods.

**Agent shorthand:** `agent` on session create accepts either a bare string (`agent="agent_abc123"` — uses latest version) or the full reference object (`{type: "agent", id: "agent_abc123", version: 123}`).

**Model shorthand:** `model` on agent create accepts either a bare string (`model="claude-opus-4-8"` — uses `standard` speed) or the full config object (`{id: "claude-opus-4-6", speed: "fast"}`). Note: `speed: "fast"` is only supported on Opus 4.6.

---

## Agents

**Step one of every flow.** Sessions require a pre-created agent — there is no inline agent config under `managed-agents-2026-04-01`.

| Method   | Path                                             | Operation        | Description                              |
| -------- | ------------------------------------------------ | ---------------- | ---------------------------------------- |
| `GET` | `/v1/agents` | ListAgents | List agents |
| `POST` | `/v1/agents` | CreateAgent | Create a saved agent configuration |
| `GET` | `/v1/agents/{agent_id}` | GetAgent | Get agent details |
| `POST` | `/v1/agents/{agent_id}` | UpdateAgent | Update agent configuration |
| `POST` | `/v1/agents/{agent_id}/archive` | ArchiveAgent | Archive an agent. Makes it **read-only**; existing sessions continue, new sessions cannot reference it. No unarchive — this is the terminal state. |
| `GET` | `/v1/agents/{agent_id}/versions` | ListAgentVersions | List agent versions |

## Sessions

| Method   | Path                                             | Operation        | Description                              |
| -------- | ------------------------------------------------ | ---------------- | ---------------------------------------- |
| `GET` | `/v1/sessions` | ListSessions | List sessions (paginated) |
| `POST` | `/v1/sessions` | CreateSession | Create a new session |
| `GET` | `/v1/sessions/{session_id}` | GetSession | Get session details |
| `POST` | `/v1/sessions/{session_id}` | UpdateSession | Update session `metadata`/`title`, or `agent.tools`/`agent.mcp_servers`/`vault_ids` (session-local override; session must be `idle`). See `shared/managed-agents-core.md` → Updating the agent configuration mid-session. |
| `DELETE` | `/v1/sessions/{session_id}` | DeleteSession | Delete a session |
| `POST` | `/v1/sessions/{session_id}/archive` | ArchiveSession | Archive a session |

## Events

| Method   | Path                                             | Operation        | Description                              |
| -------- | ------------------------------------------------ | ---------------- | ---------------------------------------- |
| `GET` | `/v1/sessions/{session_id}/events` | ListEvents | List events (polling, paginated) |
| `POST` | `/v1/sessions/{session_id}/events` | SendEvents | Send events (user message, tool result) |
| `GET` | `/v1/sessions/{session_id}/events/stream` | StreamEvents | Stream events via SSE |

## Session Threads

Per-subagent event streams in multiagent sessions. See `shared/managed-agents-multiagent.md`.

| Method   | Path                                             | Operation        | Description                              |
| -------- | ------------------------------------------------ | ---------------- | ---------------------------------------- |
| `GET` | `/v1/sessions/{session_id}/threads` | ListThreads | List threads (paginated) |
| `GET` | `/v1/sessions/{session_id}/threads/{thread_id}` | GetThread | Retrieve one thread (carries `agent` snapshot, `status`, `parent_thread_id`, `stats`, `usage`) |
| `POST` | `/v1/sessions/{session_id}/threads/{thread_id}/archive` | ArchiveThread | Archive a thread |
| `GET` | `/v1/sessions/{session_id}/threads/{thread_id}/events` | ListThreadEvents | List past events for one thread (paginated) |
| `GET` | `/v1/sessions/{session_id}/threads/{thread_id}/stream` | StreamThreadEvents | Stream one thread via SSE (SDK: `threads.events.stream`) |

## Session Resources

| Method   | Path                                                    | Operation        | Description                              |
| -------- | ------------------------------------------------------- | ---------------- | ---------------------------------------- |
| `GET` | `/v1/sessions/{session_id}/resources` | ListResources | List resources attached to session |
| `POST` | `/v1/sessions/{session_id}/resources` | AddResource | Attach `file` or `github_repository` resource (SDK method: `add`, not `create`). `memory_store` resources attach at session-create time only. |
| `GET` | `/v1/sessions/{session_id}/resources/{resource_id}` | GetResource | Get a single resource |
| `POST` | `/v1/sessions/{session_id}/resources/{resource_id}` | UpdateResource | Update resource |
| `DELETE` | `/v1/sessions/{session_id}/resources/{resource_id}` | DeleteResource | Remove resource from session |

## Environments

| Method   | Path                                                             | Operation            | Description                         |
| -------- | ---------------------------------------------------------------- | -------------------- | ----------------------------------- |
| `POST`   | `/v1/environments`                                     | CreateEnvironment    | Create environment                  |
| `GET`    | `/v1/environments`                                     | ListEnvironments     | List environments                   |
| `GET`    | `/v1/environments/{environment_id}`                    | GetEnvironment       | Get environment details             |
| `POST`   | `/v1/environments/{environment_id}`                    | UpdateEnvironment    | Update environment                  |
| `DELETE` | `/v1/environments/{environment_id}`                    | DeleteEnvironment    | Delete environment. Returns 204. |
| `POST`   | `/v1/environments/{environment_id}/archive`            | ArchiveEnvironment   | Archive environment. Makes it **read-only**; existing sessions continue, new sessions cannot reference it. No unarchive — this is the terminal state. |
| `GET`    | `/v1/environments/{environment_id}/work/stats`         | WorkQueueStats       | Self-hosted work-queue depth/pending/workers. `x-api-key` auth. See `shared/managed-agents-self-hosted-sandboxes.md`. |
| `POST`   | `/v1/environments/{environment_id}/work/{work_id}/stop` | StopWork            | Self-hosted: stop a claimed work item. `x-api-key` auth. |

For `type: "self_hosted"`, `config` is the bare `{"type": "self_hosted"}` — `networking` and `packages` do not apply.

## Vaults

Vaults store MCP credentials that Anthropic manages on your behalf — OAuth credentials with auto-refresh, or static bearer tokens. Attach to sessions via `vault_ids`. See `managed-agents-tools.md` §Vaults for the conceptual guide and credential shapes.

| Method   | Path                                             | Operation        | Description                              |
| -------- | ------------------------------------------------ | ---------------- | ---------------------------------------- |
| `POST`   | `/v1/vaults`                                     | CreateVault      | Create a vault                           |
| `GET`    | `/v1/vaults`                                     | ListVaults       | List vaults                              |
| `GET`    | `/v1/vaults/{vault_id}`                          | GetVault         | Get vault details                        |
| `POST`   | `/v1/vaults/{vault_id}`                          | UpdateVault      | Update vault                             |
| `DELETE` | `/v1/vaults/{vault_id}`                          | DeleteVault      | Delete vault                             |
| `POST`   | `/v1/vaults/{vault_id}/archive`                  | ArchiveVault     | Archive vault                            |

## Credentials

Credentials are individual secrets stored inside a vault.

| Method   | Path                                                              | Operation          | Description                  |
| -------- | ----------------------------------------------------------------- | ------------------ | ---------------------------- |
| `POST`   | `/v1/vaults/{vault_id}/credentials`                               | CreateCredential   | Create a credential          |
| `GET`    | `/v1/vaults/{vault_id}/credentials`                               | ListCredentials    | List credentials in vault    |
| `GET`    | `/v1/vaults/{vault_id}/credentials/{credential_id}`               | GetCredential      | Get credential metadata      |
| `POST`   | `/v1/vaults/{vault_id}/credentials/{credential_id}`               | UpdateCredential   | Update credential            |
| `DELETE` | `/v1/vaults/{vault_id}/credentials/{credential_id}`               | DeleteCredential   | Delete credential            |
| `POST`   | `/v1/vaults/{vault_id}/credentials/{credential_id}/archive`       | ArchiveCredential  | Archive credential           |
| `POST`   | `/v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate` | McpOauthValidate | Validate an MCP OAuth credential |

## Memory Stores

Workspace-scoped persistent memory that survives across sessions. Attach to a session via a `{"type": "memory_store", "memory_store_id": ...}` entry in `resources[]` (session-create time only). See `shared/managed-agents-memory.md` for the conceptual guide, the FUSE-mount agent interface, preconditions, and versioning.

| Method   | Path                                             | Operation          | Description                              |
| -------- | ------------------------------------------------ | ------------------ | ---------------------------------------- |
| `POST`   | `/v1/memory_stores`                              | CreateMemoryStore  | Create a store (`name`, `description`, `metadata`) |
| `GET`    | `/v1/memory_stores`                              | ListMemoryStores   | List stores (`include_archived`, `created_at_{gte,lte}`) |
| `GET`    | `/v1/memory_stores/{memory_store_id}`            | GetMemoryStore     | Get store details                        |
| `POST`   | `/v1/memory_stores/{memory_store_id}`            | UpdateMemoryStore  | Update store                             |
| `DELETE` | `/v1/memory_stores/{memory_store_id}`            | DeleteMemoryStore  | Delete store                             |
| `POST`   | `/v1/memory_stores/{memory_store_id}/archive`    | ArchiveMemoryStore | Archive store. Makes it **read-only**; existing sessions continue, new sessions cannot reference it. No unarchive. |

## Memories

Individual text documents inside a store (≤ 100KB each). `create` creates at a `path` and returns `409` (`memory_path_conflict_error`, with `conflicting_memory_id`) if the path is occupied; `update` mutates by `mem_...` ID (rename and/or content). Only `update` accepts a `precondition` (`{"type": "content_sha256", "content_sha256": ...}`) — on mismatch returns `409` (`memory_precondition_failed_error`). List endpoints accept `view: "basic"|"full"` (controls whether `content` is populated; `retrieve` defaults to `full`).

| Method   | Path                                                              | Operation      | Description                              |
| -------- | ----------------------------------------------------------------- | -------------- | ---------------------------------------- |
| `GET`    | `/v1/memory_stores/{memory_store_id}/memories`                    | ListMemories   | Returns `Memory \| MemoryPrefix`; filter by `path_prefix`, `depth`, `order_by`/`order` |
| `POST`   | `/v1/memory_stores/{memory_store_id}/memories`                    | CreateMemory   | Create at `path` (SDK: `memories.create`); `409 memory_path_conflict_error` if occupied |
| `GET`    | `/v1/memory_stores/{memory_store_id}/memories/{memory_id}`        | GetMemory      | Read one memory (defaults to `view="full"`) |
| `PATCH`  | `/v1/memory_stores/{memory_store_id}/memories/{memory_id}`        | UpdateMemory   | Change `content`, `path`, or both by ID; optional `precondition` |
| `DELETE` | `/v1/memory_stores/{memory_store_id}/memories/{memory_id}`        | DeleteMemory   | Delete (optional `expected_content_sha256`) |

## Memory Versions

Immutable per-mutation snapshots (`memver_...`) — the audit and rollback surface. `operation` ∈ `created` / `modified` / `deleted`.

| Method   | Path                                                                          | Operation             | Description                              |
| -------- | ----------------------------------------------------------------------------- | --------------------- | ---------------------------------------- |
| `GET`    | `/v1/memory_stores/{memory_store_id}/memory_versions`                         | ListMemoryVersions    | Newest-first; filter by `memory_id`, `operation`, `session_id`, `api_key_id`, `created_at_{gte,lte}` |
| `GET`    | `/v1/memory_stores/{memory_store_id}/memory_versions/{version_id}`            | GetMemoryVersion      | List fields + full `content`             |
| `POST`   | `/v1/memory_stores/{memory_store_id}/memory_versions/{version_id}/redact`     | RedactMemoryVersion   | Clear `content`/`content_sha256`/`content_size_bytes`/`path`; preserve actor + timestamps |

## Files

| Method   | Path                                             | Operation        | Description                              |
| -------- | ------------------------------------------------ | ---------------- | ---------------------------------------- |
| `POST`   | `/v1/files`                            | UploadFile       | Upload a file                            |
| `GET`    | `/v1/files`                            | ListFiles        | List files                               |
| `GET`    | `/v1/files/{file_id}`                  | GetFile          | Get file metadata (SDK method: `retrieve_metadata`) |
| `GET`    | `/v1/files/{file_id}/content`          | DownloadFile     | Download file content                    |
| `DELETE` | `/v1/files/{file_id}`                  | DeleteFile       | Delete a file                            |

## Skills

| Method   | Path                                                            | Operation          | Description                  |
| -------- | --------------------------------------------------------------- | ------------------ | ---------------------------- |
| `POST`   | `/v1/skills`                                          | CreateSkill        | Create a skill               |
| `GET`    | `/v1/skills`                                          | ListSkills         | List skills                  |
| `GET`    | `/v1/skills/{skill_id}`                               | GetSkill           | Get skill details            |
| `DELETE` | `/v1/skills/{skill_id}`                               | DeleteSkill        | Delete a skill               |
| `POST`   | `/v1/skills/{skill_id}/versions`                      | CreateVersion      | Create skill version         |
| `GET`    | `/v1/skills/{skill_id}/versions`                      | ListVersions       | List skill versions          |
| `GET`    | `/v1/skills/{skill_id}/versions/{version}`            | GetVersion         | Get skill version            |
| `DELETE` | `/v1/skills/{skill_id}/versions/{version}`            | DeleteVersion      | Delete skill version         |

---

## Request/Response Schema Quick Reference

### CreateAgent Request Body

**Always start here.** `model`, `system`, `tools`, `mcp_servers`, `skills` are top-level fields on this object — they do NOT go on the session.

```json
{
  "name": "string (required, 1-256 chars)",
  "model": "claude-opus-4-8 (required — bare string, or {id, speed} object)",
  "description": "string (optional, up to 2048 chars)",
  "system": "string (optional, up to 100,000 chars)",
  "tools": [
    { "type": "agent_toolset_20260401" }
  ],
  "skills": [
    { "type": "anthropic", "skill_id": "xlsx" },
    { "type": "custom", "skill_id": "skill_abc123", "version": "1" }
  ],
  "mcp_servers": [
    {
      "type": "url",
      "name": "github",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  ],
  "multiagent": {
    "type": "coordinator",
    "agents": [
      "agent_abc123",
      { "type": "agent", "id": "agent_def456", "version": 4 },
      { "type": "self" }
    ]
  },
  "metadata": {
    "key": "value (max 16 pairs, keys ≤64 chars, values ≤512 chars)"
  }
}
```

> Limits: `tools` max 128, `skills` max 20, `mcp_servers` max 20 (unique names). `multiagent.agents` 1–20 entries (string ID | `{type:"agent",id,version?}` | `{type:"self"}`) — see `shared/managed-agents-multiagent.md`.

### CreateSession Request Body

```json
{
  "agent": "agent_abc123 (required — string shorthand for latest version, or {type: \"agent\", id, version} object)",
  "environment_id": "env_abc123 (required)",
  "title": "string (optional)",
  "resources": [
    {
      "type": "github_repository",
      "url": "https://github.com/owner/repo (required)",
      "authorization_token": "ghp_... (required)",
      "mount_path": "/workspace/repo (optional — defaults to /workspace/<repo-name>)",
      "checkout": { "type": "branch", "name": "main" }
    }
  ],
  "vault_ids": ["vlt_abc123 (optional — MCP credentials with auto-refresh)"],
  "metadata": {
    "key": "value"
  }
}
```

> The `agent` field accepts only a string ID or `{type: "agent", id, version}` — `model`/`system`/`tools` live on the agent, not here.
>
> **`checkout`** accepts `{type: "branch", name: "..."}` or `{type: "commit", sha: "..."}`. Omit for the repo's default branch.

### CreateEnvironment Request Body

```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "config": {
    "type": "cloud | self_hosted",
    "networking": {
      "type": "unrestricted | limited (union — see SDK types)"
    },
    "packages": { }
  },
  "metadata": { "key": "value" }
}
```

### SendEvents Request Body

```json
{
  "events": [
    {
      "type": "user.message",
      "content": [
        {
          "type": "text",
          "text": "Hello"
        }
      ]
    }
  ]
}
```

### Define Outcome Event

```json
{
  "type": "user.define_outcome",
  "description": "Build a DCF model for Costco in .xlsx",
  "rubric": { "type": "file", "file_id": "file_01..." },
  "max_iterations": 5
}
```

> `rubric` is required: `{type: "text", content}` or `{type: "file", file_id}`. `max_iterations` default 3, max 20. Echoed back with `outcome_id` + `processed_at`. See `shared/managed-agents-outcomes.md`.

### Tool Result Event

```json
{
  "type": "user.custom_tool_result",
  "custom_tool_use_id": "sevt_abc123",
  "content": [{ "type": "text", "text": "Result data" }],
  "is_error": false
}
```

---

## Error Handling

Managed Agents endpoints use the standard Anthropic API error format. Errors are returned with an HTTP status code and a JSON body containing `type`, `error`, and `request_id`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Description of what went wrong"
  },
  "request_id": "req_011CRv1W3XQ8XpFikNYG7RnE"
}
```

Include the `request_id` when reporting issues to Anthropic — it lets us trace the request end-to-end. The inner `error.type` is one of the following:

| Status | Error type | Description |
|---|---|---|
| 400 | `invalid_request_error` | The request was malformed or missing required parameters |
| 401 | `authentication_error` | Invalid or missing API key |
| 403 | `permission_error` | The API key doesn't have permission for this operation |
| 404 | `not_found_error` | The requested resource doesn't exist |
| 409 | `invalid_request_error` | The request conflicts with the resource's current state (e.g., sending to an archived session) |
| 413 | `request_too_large` | The request body exceeds the maximum allowed size |
| 429 | `rate_limit_error` | Too many requests — check rate limit headers for retry timing |
| 500 | `api_error` | An internal server error occurred |
| 529 | `overloaded_error` | The service is temporarily overloaded — retry with backoff |

Note that `409 Conflict` carries `error.type: "invalid_request_error"` (there is no separate `conflict_error` type); inspect both the HTTP status and the `message` to distinguish conflicts from other invalid requests.

---

## Rate Limits

Managed Agents endpoints have per-organization request-per-minute (RPM) limits, separate from your [Messages API token limits](https://platform.claude.com/docs/en/api/rate-limits). Model inference inside a session still draws from your organization's standard ITPM/OTPM limits.

| Endpoint group | Scope | RPM | Max concurrent |
|---|---|---|---|
| Create operations (Agents, Sessions, Vaults) | organization | 300 | — |
| All other operations (Agents, Sessions, Vaults) | organization | 600 | — |
| All operations (Environments) | organization | 60 | 5 |

Files and Skills endpoints use the standard tier-based [rate limits](https://platform.claude.com/docs/en/api/rate-limits).

When a limit is exceeded the API returns `429` with a `rate_limit_error` (see [Error Handling](#error-handling) for the response envelope) and a `retry-after` header indicating how many seconds to wait before retrying. The Anthropic SDK reads this header and retries automatically.
</doc>

<doc path="shared/managed-agents-client-patterns.md">
# Managed Agents — Common Client Patterns

Patterns you'll write on the client side when driving a Managed Agent session, grounded in working SDK examples.

Code samples are TypeScript — Python and cURL follow the same shape; see `python/managed-agents/README.md` and `curl/managed-agents.md` for equivalents.

---

## 1. Lossless stream reconnect

**Problem:** SSE has no replay. If the connection drops mid-session, a naive reconnect re-opens the stream from "now" and you silently miss every event emitted in between.

**Solution:** on reconnect, fetch the full event history via `events.list()` *before* consuming the live stream, and dedupe on event ID as the live stream catches up.

```ts
const seenEventIds = new Set<string>()
const stream = await client.beta.sessions.events.stream(session.id)

// Stream is now open and buffering server-side. Read history first.
for await (const event of client.beta.sessions.events.list(session.id)) {
  seenEventIds.add(event.id)
  handle(event)
}

// Tail the live stream. Dedupe only gates handle() — terminal checks must run
// even for already-seen events, or a terminal event that was in the history
// response gets skipped by `continue` and the loop never exits.
for await (const event of stream) {
  if (!seenEventIds.has(event.id)) {
    seenEventIds.add(event.id)
    handle(event)
  }
  if (event.type === 'session.status_terminated') break
  if (event.type === 'session.status_idle' && event.stop_reason.type !== 'requires_action') break
}
```

---

## 2. `processed_at` — queued vs processed

Every event on the stream carries `processed_at` (ISO 8601). For client-sent events (`user.message`, `user.interrupt`, `user.tool_confirmation`, `user.custom_tool_result`) it's `null` when the event has been queued but not yet picked up by the agent, and populated once the agent processes it. The same event appears on the stream twice — once with `processed_at: null`, once with a timestamp.

```ts
for await (const event of stream) {
  if (event.type === 'user.message') {
    if (event.processed_at == null) onQueued(event.id)
    else onProcessed(event.id, event.processed_at)
  }
}
```

Use this to drive pending → acknowledged UI state for anything you send. How you map a locally-rendered optimistic message to the server-assigned `event.id` is application-specific (typically via the return value of `events.send()` or FIFO ordering).

---

## 3. Interrupt a running session

Send `user.interrupt` as a normal event. The session keeps running until it reaches a safe boundary, then goes idle.

```ts
await client.beta.sessions.events.send(session.id, {
  events: [{ type: 'user.interrupt' }],
})

// Drain until the session is truly done — see Pattern 5 for the full gate.
for await (const event of stream) {
  if (event.type === 'session.status_terminated') break
  if (
    event.type === 'session.status_idle' &&
    event.stop_reason.type !== 'requires_action'
  ) break
}
```

Reference: `interrupt.ts` — sends the interrupt the moment it sees `span.model_request_start`, drains to idle, then verifies via `sessions.retrieve()`.

---

## 4. `tool_confirmation` round-trip

When the agent has `permission_policy: { type: 'always_ask' }`, any call to that tool fires an `agent.tool_use` event with `evaluated_permission === 'ask'` and the session goes idle waiting for a decision. Respond with `user.tool_confirmation`.

```ts
for await (const event of stream) {
  if (event.type === 'agent.tool_use' && event.evaluated_permission === 'ask') {
    await client.beta.sessions.events.send(session.id, {
      events: [{
        type: 'user.tool_confirmation',
        tool_use_id: event.id,         // not a toolu_ id — use event.id
        result: 'allow',               // or 'deny'
        // deny_message: '...',        // optional, only with result: 'deny'
      }],
    })
  }
}
```

Key points:
- `tool_use_id` is `event.id` (typically `sevt_...`), **not** a `toolu_...` ID.
- `result` is `'allow' | 'deny'`. Use `deny_message` to tell the model *why* you denied — it gets surfaced back to the agent.
- Multiple pending tools: respond once per `agent.tool_use` event with `evaluated_permission === 'ask'`.

Reference: `tool-permissions.ts`.

---

## 5. Correct idle-break gate

Do not break on `session.status_idle` alone. The session goes idle transiently — e.g. between parallel tool executions, while waiting for a `user.tool_confirmation`, or while awaiting a `user.custom_tool_result`. Break when idle with a terminal `stop_reason`, or on `session.status_terminated`.

```ts
for await (const event of stream) {
  handle(event)
  if (event.type === 'session.status_terminated') break
  if (event.type === 'session.status_idle') {
    if (event.stop_reason.type === 'requires_action') continue // waiting on you — handle it
    break // end_turn or retries_exhausted — both terminal
  }
}
```

`stop_reason.type` values on `session.status_idle`:
- `requires_action` — agent is waiting on a client-side event (tool confirmation, custom tool result). Handle it, don't break.
- `retries_exhausted` — terminal failure. Break, then check `sessions.retrieve()` for the error state.
- `end_turn` — normal completion.

---

## 6. Post-idle status-write race

The SSE stream emits `session.status_idle` slightly before the session's queryable status reflects it. Clients that break on idle and immediately call `sessions.delete()` or `sessions.archive()` will intermittently 400 with "cannot delete/archive while running."

Poll before cleanup:

```ts
let s
for (let i = 0; i < 10; i++) {
  s = await client.beta.sessions.retrieve(session.id)
  if (s.status !== 'running') break
  await new Promise(r => setTimeout(r, 200))
}
if (s?.status !== 'running') {
  await client.beta.sessions.archive(session.id)
} // else: still running after 2s — don't archive, let it settle or escalate
```

---

## 7. Stream-first, then send

Always open the stream **before** sending the kickoff event. Otherwise the agent may process the event and emit the first events before your consumer is attached, and you'll miss them.

```ts
const stream = await client.beta.sessions.events.stream(session.id)
await client.beta.sessions.events.send(session.id, {
  events: [{ type: 'user.message', content: [{ type: 'text', text: 'Hello' }] }],
})
for await (const event of stream) { /* ... */ }
```

The `Promise.all([stream, send])` shape works too, but stream-first is simpler and has the same effect — the stream starts buffering the moment it's opened.

---

## 8. File-mount gotchas

**The mounted resource has a different `file_id` than the file you uploaded.** Session creation makes a session-scoped copy.

```ts
const uploaded = await client.beta.files.upload({ file, purpose: 'agent_resource' })
// uploaded.id         → the original file
const session = await client.beta.sessions.create({
  /* ... */
  resources: [{ type: 'file', file_id: uploaded.id, mount_path: '/workspace/data.csv' }],
})
// session.resources[0].file_id !== uploaded.id  ← different IDs
```

Delete the original via `files.delete(uploaded.id)`; the session-scoped copy is garbage-collected with the session. `mount_path` must be absolute — see `shared/managed-agents-environments.md`.

---

## 9. Secrets for non-MCP APIs and CLIs — keep them host-side via custom tools

**Problem:** you want the agent to call a third-party API or run a CLI that needs a secret (API key, token, service-account credential), but there is currently no way to set environment variables inside the session container, and vaults currently hold MCP credentials only — they are not exposed to the container's shell. So `curl`, installed CLIs, or SDK clients running via the `bash` tool have no first-class place to read a secret from.

**Solution:** move the authenticated call to your side. Declare a custom tool on the agent; when the agent emits `agent.custom_tool_use`, your orchestrator (the process reading the SSE stream) executes the call with its own credentials and responds with `user.custom_tool_result`. The container never sees the key.

```ts
// Agent template: declare the tool, no credentials
tools: [{ type: 'custom', name: 'linear_graphql', input_schema: { /* query, vars */ } }]

// Orchestrator: handle the call with host-side creds
for await (const event of stream) {
  if (event.type === 'agent.custom_tool_use' && event.name === 'linear_graphql') {
    const result = await linear.request(event.input.query, event.input.vars) // host's key
    await client.beta.sessions.events.send(session.id, {
      events: [{ type: 'user.custom_tool_result', tool_use_id: event.id, result }],
    })
  }
}
```

Same shape works for `gh` CLI, local eval scripts, or anything else that needs host-side auth or binaries.

**Security note:** this does not expose a public endpoint. `agent.custom_tool_use` arrives on the SSE stream your orchestrator already holds open with your Anthropic API key, and `user.custom_tool_result` goes back via `events.send()` under the same key. Your orchestrator is a client, not a server — nothing unauthenticated is listening.

**Do not embed API keys in the system prompt or user messages as a workaround.** Prompts and messages are stored in the session's event history, returned by `events.list()`, and included in compaction summaries — a secret placed there is durably persisted and readable via the API for the life of the session.
</doc>

<doc path="shared/managed-agents-core.md">
# Managed Agents — Core Concepts

## Architecture

Managed Agents is built around four core concepts:

| Concept | Endpoint | What it is |
|---|---|---|
| **Agent** | `/v1/agents` | A persisted, versioned object defining the agent's capabilities and persona: model, system prompt, tools, MCP servers, skills. **Must be created before starting a session.** See the Agents section below. |
| **Session** | `/v1/sessions` | A stateful interaction with an agent. References a pre-created agent by ID + an environment + initial instructions. Produces an event stream. |
| **Environment** | `/v1/environments` | A template defining the configuration for container provisioning. |
| **Container** | N/A | An isolated compute instance where the agent's **tools** execute (bash, file ops, code). The agent loop does not run here — it runs on Anthropic's orchestration layer and acts on the container via tool calls. |

```
                       ┌─────────────────────────────────────┐
                       │  Anthropic orchestration layer      │
Agent (config) ───────▶│  (agent loop: Claude + tool calls)  │
                       └──────────────┬──────────────────────┘
                                      │ tool calls
                                      ▼
Environment (template) ──▶ Container (tool execution workspace)
                                 │
                         Session ─┤
                                 ├── Resources (files, repos, memory stores — attached at startup)
                                 ├── Vault IDs (MCP credential references)
                                 └── Conversation (event stream in/out)
```

> **Agent creation is a prerequisite.** Sessions reference a pre-created agent by ID — `model`/`system`/`tools` live on the agent object, never on the session. Every flow starts with `POST /v1/agents`.

---

## Session Lifecycle

```
rescheduling → running ↔ idle → terminated
```

| Status         | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `idle` | Agent has finished the current task, and is awaiting input. It's either waiting for input to continue working via a `user.message` or blocked awaiting a `user.custom_tool_result` or `user.tool_confirmation`. The `stop_reason` attached contains more information about why the Agent has stopped working. |
| `running` | Session has starting running, and the Agent is actively doing work. |
| `rescheduling` | Session is (re)scheduling after a retryable error has occurred, ready to be picked up by the orchestration system. |
| `terminated` | Session has terminated, entering an irreversible and unusable state.  |

- Events can be sent when the session is `running` or `idle`. Messages are queued and processed in order.
- The agent transitions `idle → running` when it receives a new event, then back to `idle` when done.
- Errors surface as `session.error` events in the stream, not as a status value.

### Built-in session features

- **Context compaction** — if you approach max context, the API automatically condenses session history to keep the interaction going
- **Prompt caching** — historical repeated tokens are cached, reducing processing time and cost
- **Extended thinking** — on by default, returned as `agent.thinking` events

### Session operations

| Operation | Notes |
|---|---|
| List / fetch | Paginated list or single resource by ID |
| Update | Only `title` is updatable |
| Archive | Session becomes **read-only**. Not reversible. |
| Delete | Permanently deletes session, event history, container, and checkpoints. |

These are ops/inspection calls — typically made from a terminal, not application code. From the shell (see `shared/anthropic-cli.md`):

```sh
ant beta:sessions list --transform '{id,title,status,created_at}' --format jsonl
ant beta:sessions retrieve --session-id "$SID"
ant beta:sessions:events stream --session-id "$SID"   # watch events live
ant beta:sessions archive  --session-id "$SID"
ant beta:sessions delete   --session-id "$SID"
```

---

## Sessions

A session is a running agent instance inside an environment.

### Session Object

Key fields returned by the API:

| Field           | Type     | Description                                         |
| --------------- | -------- | --------------------------------------------------- |
| `type` | string | Always `"session"` |
| `id` | string | Unique session ID |
| `title` | string | Human-readable title |
| `status` | string | `idle`, `running`, `rescheduling`, `terminated` |
| `created_at` | string | ISO 8601 timestamp |
| `updated_at` | string | ISO 8601 timestamp |
| `archived_at` | string | ISO 8601 timestamp (nullable) |
| `environment_id` | string | Environment ID |
| `agent` | object | Agent configuration |
| `resources` | array | Attached files, repos, and memory stores |
| `metadata` | object | User-provided key-value pairs (max 8 keys) |
| `usage` | object | Token usage statistics |

### Creating a session

**A session is meaningless without an agent.** Sessions reference a pre-created agent by ID. Create the agent first via `agents.create()`, then reference it:

```ts
// 1. Create the agent (reusable, versioned)
const agent = await client.beta.agents.create(
  {
    name: "Coding Assistant",
    model: "claude-opus-4-8",
    system: "You are a helpful coding agent.",
    tools: [{ type: "agent_toolset_20260401"}],
  },
);

// 2. Start a session that references it
const session = await client.beta.sessions.create(
  {
    agent: agent.id,  // string shorthand → latest version. Or: { type: "agent", id: agent.id, version: agent.version }
    environment_id: environmentId,
    title: "Hello World Session",
  },
);
```

> 💡 **Watch it live in Console.** While developing, print a link so you can click through to the session UI instead of parsing the event stream: `https://platform.claude.com/workspaces/{workspace}/sessions/{session.id}`. Use `default` for the workspace slug unless you created the session in a non-default workspace; the sessions list for your workspace is at `https://platform.claude.com/workspaces/default/sessions`. Include this `print`/`console.log` in code you generate for users who are iterating locally.

**Session creation parameters:**

| Field           | Type     | Required | Description                                    |
| --------------- | -------- | -------- | ---------------------------------------------- |
| `agent`         | string or object | **Yes** | String shorthand `"agent_abc123"` (latest version) or `{type: "agent", id, version}` |
| `environment_id`| string   | **Yes**  | Environment ID                                 |
| `title`         | string   | No       | Human-readable name (appears in logs/dashboards) |
| `resources`     | array    | No       | Files, GitHub repos, or memory stores, attached to the container at startup. Memory stores are session-create-only (not addable via `resources.add()`). |
| `vault_ids`     | array    | No       | Vault IDs (`vlt_*`) — MCP credentials with auto-refresh. See `shared/managed-agents-tools.md` → Vaults. |
| `metadata`      | object   | No       | User-provided key-value pairs                  |

**Agent configuration fields** (passed to `agents.create()`, not `sessions.create()`):

| Field         | Type     | Required | Description                                    |
| ------------- | -------- | -------- | ---------------------------------------------- |
| `name`        | string   | **Yes**  | Human-readable name (1-256 chars)              |
| `model`       | string or object | **Yes** | Claude model ID (bare string, or `{id, speed}` object). All Claude 4.5+ models supported. |
| `system`      | string   | No       | System prompt — defines the agent's behavior (up to 100K chars) |
| `tools`       | array    | No       | Encompasses three kinds: (1) pre-built Claude Agent tools (`agent_toolset_20260401`), (2) MCP tools (`mcp_toolset`), and (3) custom client-side tools. Max 128. |
| `mcp_servers` | array    | No       | MCP server connections — standardized third-party capabilities (e.g. GitHub, Asana). Max 20, unique names. See `shared/managed-agents-tools.md` → MCP Servers. |
| `skills`      | array    | No       | Customized "best-practices" context with progressive disclosure. Max 20. See `shared/managed-agents-tools.md` → Skills. |
| `description` | string   | No       | Description of the agent (up to 2048 chars)    |
| `multiagent`  | object   | No       | `{type: "coordinator", agents: [...]}` — roster this agent may delegate to. See `shared/managed-agents-multiagent.md`. |
| `metadata`    | object   | No       | Arbitrary key-value pairs (max 16, keys ≤64 chars, values ≤512 chars) |

---

## Agents

**This is where every Managed Agents flow begins.** The agent object is a persisted, versioned configuration — you create it once, then reference it by ID every time you start a session. No agent → no session.

### Agent Object

The API is **flat** — `model`, `system`, `tools` etc. are top-level fields, not wrapped in an `agent:{}` sub-object.

| Field              | Type     | Required | Description                                        |
| ------------------ | -------- | -------- | -------------------------------------------------- |
| `name`             | string   | Yes      | Human-readable name                                |
| `model`            | string   | Yes      | Claude model ID                                    |
| `system`           | string   | No       | System prompt                                      |
| `tools`            | array    | No       | Agent toolset / MCP toolset / custom tools         |
| `mcp_servers`      | array    | No       | MCP server connections                             |
| `skills`           | array    | No       | Skill references (max 20)                          |
| `description`      | string   | No       | Description of the agent                           |
| `multiagent`       | object   | No       | Coordinator roster — see `shared/managed-agents-multiagent.md` |
| `metadata`         | object   | No       | Arbitrary key-value pairs                          |

### Lifecycle: create once, run many, update in place

The agent is a **persistent resource**, not a per-run parameter. The intended pattern:

```
┌─ setup (once) ─────────┐     ┌─ runtime (every invocation) ─┐
│ agents.create()        │     │ sessions.create(             │
│   → store agent_id     │ ──→ │   agent={type:..., id: ID}   │
│     in config/env/db   │     │ )                            │
└────────────────────────┘     └──────────────────────────────┘
```

**Anti-pattern:** calling `agents.create()` at the top of every script run. This accumulates orphaned agent objects, pays create latency on every invocation, and defeats the versioning model. If you see `agents.create()` in a function that's called per-request or per-cron-tick, that's wrong — hoist it to one-time setup and persist the ID.

> **Recommended — define agents and environments as YAML + apply via the `ant` CLI.** The split is **CLI for the control plane, SDK for the data plane**: agents and environments are relatively static resources you manage with `ant` (version-controlled YAML, applied from CI); sessions are dynamic and driven by your application through the SDK. See `shared/anthropic-cli.md` → *Version-controlled Managed Agents resources* for the `ant beta:agents create < agent.yaml` / `update --version N` flow. The SDK `agents.create()` call shown elsewhere in this doc is the in-code equivalent — use it when you need to provision programmatically, but prefer the YAML flow for anything a human maintains.

### Versioning

Each `POST /v1/agents/{id}` (update) creates a new immutable version (numeric timestamp, e.g. `1772585501101368014`). The agent's history is append-only — you can't edit a past version.

**Why version:**
- **Reproducibility** — pin a session to a known-good config: `{type: "agent", id, version: 3}`
- **Safe iteration** — update the agent without breaking sessions already running on the old version
- **Rollback** — if a new system prompt regresses, pin new sessions back to the prior version while you debug

**`version` is optional.** Omit it (or use the string shorthand `agent="agent_abc123"`) to get the latest version at session-creation time. Pass it explicitly (`{type: "agent", id, version: N}`) to pin for reproducibility.

**Getting the version to pin:** `agents.create()` and `agents.update()` both return `version` in the response. Store it alongside `agent_id`. To fetch the current latest for an existing agent: `GET /v1/agents/{id}` → `.version`.

**When to update vs create new:** Update (`POST /v1/agents/{id}`) when it's conceptually the same agent with tweaked behavior (better prompt, extra tool). Create a new agent when it's a different persona/purpose. Rule of thumb: if you'd give it the same `name`, update.

### Agent Endpoints

| Operation        | Method   | Path                                  |
| ---------------- | -------- | ------------------------------------- |
| Create           | `POST`   | `/v1/agents`                          |
| List             | `GET`    | `/v1/agents`                          |
| Get              | `GET`    | `/v1/agents/{id}`                     |
| Update           | `POST`   | `/v1/agents/{id}`                     |
| Archive          | `POST`   | `/v1/agents/{id}/archive`             |

> ⚠️ **Archive is permanent.** Archiving makes the agent read-only: existing sessions continue to run, but **new sessions cannot reference it**, and there is no unarchive. Since agents have no `delete`, this is the terminal lifecycle state. Never archive a production agent as routine cleanup — confirm with the user first.

### Using an Agent in a Session

Reference the agent by string ID (latest version) or by object with an explicit version:

```python
# String shorthand — uses the agent's latest version
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment_id,
)

# Or pin to a specific version (int)
session = client.beta.sessions.create(
    agent={"type": "agent", "id": agent.id, "version": agent.version},
    environment_id=environment_id,
)
```

### Updating the agent configuration mid-session

`sessions.update()` can change `agent.tools`, `agent.mcp_servers` (including permission policies), and `vault_ids` on an **existing** session. This is a **session-local override** — it does not create a new agent version and does not propagate back to the agent object. The provided arrays are **full replacements**; to append one tool, `GET` the session, modify, and `POST` back. The session must be `idle` — interrupt first if running.

```python
client.beta.sessions.update(
    session.id,
    agent={
        "tools": [
            {"type": "agent_toolset_20260401"},
            {"type": "mcp_toolset", "mcp_server_name": "linear"},
        ],
        "mcp_servers": [{"type": "url", "name": "linear", "url": "https://mcp.linear.app/sse"}],
    },
    vault_ids=["vlt_..."],
)
```
</doc>

<doc path="shared/managed-agents-environments.md">
# Managed Agents — Environments & Resources

## Environments

Creating a session requires an `environment_id`. Environments are **reusable configuration templates** for spinning up containers in Anthropic's infrastructure — you might create different environments for different use cases (e.g. data visualization vs web development, with different package sets). Anthropic handles scaling, container lifecycle, and work orchestration.

**Environment names must be unique.** Creating an environment with an existing name returns 409.

### Networking

| Network Policy   | Description                                                   |
| ---------------- | ------------------------------------------------------------- |
| `unrestricted`   | Full egress (except legal blocklist)                          |
| `limited`        | Deny-by-default; opt in via `allowed_hosts` / `allow_package_managers` / `allow_mcp_servers` |

```json
{
  "networking": {
    "type": "limited",
    "allow_package_managers": true,
    "allow_mcp_servers": true,
    "allowed_hosts": ["api.example.com"]
  }
}
```

All three `limited` fields are optional. `allow_package_managers` (default `false`) permits PyPI/npm/etc.; `allow_mcp_servers` (default `false`) permits the agent's configured MCP server endpoints without listing them in `allowed_hosts`.

**MCP caveat:** Under `limited` networking, either set `allow_mcp_servers: true` or add each MCP server domain to `allowed_hosts`. Otherwise the container can't reach them and tools silently fail.

### Creating an environment

The SDK adds `managed-agents-2026-04-01` automatically. TypeScript:

```ts
const env = await client.beta.environments.create({
  name: "my_env",
  config: {
    type: "cloud",
    networking: { type: "unrestricted" },
  },
});
```

### Self-hosted sandboxes

To run tool execution in **your own infrastructure** instead of Anthropic's, set `config: {type: "self_hosted"}` — the agent loop stays on Anthropic's side, but `bash` / file ops / code execute in a container you control via an outbound-polling worker. The `networking` block does not apply (you control egress). Resource mounting (`file`, `github_repository`) and memory stores behave differently — see `shared/managed-agents-self-hosted-sandboxes.md` for the worker, credentials, and cloud-vs-self-hosted comparison.

### Environment CRUD

| Operation        | Method   | Path                                       | Notes |
| ---------------- | -------- | ------------------------------------------ | ----- |
| Create           | `POST`   | `/v1/environments`                         | |
| List             | `GET`    | `/v1/environments`                         | Paginated (`limit`, `after_id`, `before_id`) |
| Get              | `GET`    | `/v1/environments/{id}`                    | |
| Update           | `POST`   | `/v1/environments/{id}`                    | Changes apply only to **new** containers; existing sessions keep their original config |
| Delete           | `DELETE` | `/v1/environments/{id}`                    | Returns 204. |
| Archive          | `POST`   | `/v1/environments/{id}/archive`            | Makes it **read-only**; existing sessions continue, new sessions cannot reference it. No unarchive — terminal state. |

---

## Resources

Attach files, GitHub repositories, and memory stores to a session. **Session creation blocks until all resources are mounted** — the container won't go `running` until every file and repo is in place. Max **999 file resources** per session. Multiple GitHub repositories per session are supported. For `type: "memory_store"` resources (persistent cross-session memory — max 8 per session), see `shared/managed-agents-memory.md`.

### File Uploads (input — host → agent)

Upload a file first via the Files API, then reference by `file_id` + `mount_path`:

```ts
// 1. Upload
const file = await client.beta.files.upload({
  file: fs.createReadStream("data.csv"),
  purpose: "agent",
});

// 2. Attach as a session resource
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: envId,
  resources: [
    { type: "file", file_id: file.id, mount_path: "/workspace/data.csv" }
  ],
});
```

**`mount_path` is required** and must be absolute. Parent directories are created automatically. Agent working directory defaults to `/workspace`. Files are mounted read-only — the agent writes modified versions to new paths.

### Session outputs (output — agent → host)

The agent can write files to `/mnt/session/outputs/` during a session. These are automatically captured by the Files API and can be listed and downloaded afterwards:

```ts
// After the turn completes, list output files scoped to this session:
for await (const f of client.beta.files.list({
  scope_id: session.id,
  betas: ["managed-agents-2026-04-01"],
})) {
  console.log(f.filename, f.size_bytes);
  const resp = await client.beta.files.download(f.id);
  const text = await resp.text();
}
```

**Requirements:**
- The `write` tool (or `bash`) must be enabled for the agent to create output files.
- Session-scoped `files.list` / `files.download` captures outputs written to `/mnt/session/outputs/`.
- The filter parameter is **`scope_id`** (REST query param `?scope_id=<session_id>`). The SDK's files resource auto-adds only the `files-api-2025-04-14` header, so pass `betas: ["managed-agents-2026-04-01"]` explicitly (or both headers on raw HTTP) — without it the API may reject `scope_id` as an unknown field. Requires `@anthropic-ai/sdk` ≥ 0.88.0 / `anthropic` (Python) ≥ 0.92.0 — older versions don't type `scope_id`. The `ant` CLI does **not** expose this flag yet; use the SDK or curl.
- Pass the session ID returned by `sessions.create()` verbatim (e.g. `sesn_011CZx...`) — the API validates the prefix.
- There's a brief indexing lag (~1–3s) between `session.status_idle` and output files appearing in `files.list`. Retry once or twice if empty.

> **Fallback when `scope_id` filtering is unavailable** (older SDK, or endpoint returns an error): send a follow-up `user.message` asking the agent to `read` each file under `/mnt/session/outputs/` and return the contents. The agent streams the file bodies back as `agent.message` text. This works for text files only and costs output tokens — use it to unblock, not as the primary path.

This gives you a bidirectional file bridge: upload reference data in, download agent artifacts out.

### GitHub Repositories

Clones a GitHub repository into the session container during initialization, before the agent begins execution. The agent can read, edit, commit, and push via `bash` (`git`). Multiple repositories per session are supported — add one `resources` entry per repo. Repositories are cached, so future sessions that use the same repository start faster.

Repositories are attached for the lifetime of the session — to change which repositories are mounted, create a new session. You **can** rotate a repository's `authorization_token` on a running session via `client.beta.sessions.resources.update(resource_id, {session_id, authorization_token})`; the resource `id` is returned at session creation and by `resources.list()`.

**Fields:**

| Field | Required | Notes |
|---|---|---|
| `type` | ✅ | `"github_repository"` |
| `url` | ✅ | The GitHub repository URL |
| `authorization_token` | ✅ | GitHub Personal Access Token with repository access. **Never echoed in API responses.** |
| `mount_path` | ❌ | Path where the repository will be cloned. Defaults to `/workspace/<repo-name>`. |
| `checkout` | ❌ | `{type: "branch", name: "..."}` or `{type: "commit", sha: "..."}`. Defaults to the repo's default branch. |

**Token permission levels** (fine-grained PATs):
- `Contents: Read` — clone only
- `Contents: Read and write` — push changes and create pull requests

**How auth works:** `authorization_token` is never placed inside the container. `git pull` / `git push` and GitHub REST calls against the attached repository are routed through an Anthropic-side git proxy that injects the token after the request leaves the sandbox. Code running in the container — including anything the agent writes — cannot read or exfiltrate it.

> ‼️ **To generate pull requests** you also need GitHub **MCP server** access — the `github_repository` resource gives filesystem + git access only. See `shared/managed-agents-tools.md` → MCP Servers. The PR workflow is: edit files in the mounted repo → push branch via `bash` (authenticated via the git proxy using `authorization_token`) → create PR via the MCP `create_pull_request` tool (authenticated via the vault).

**TypeScript:**

```ts
// 1. Create the agent — declare GitHub MCP (no auth here)
const agent = await client.beta.agents.create(
  {
    name: 'GitHub Agent',
    model: 'claude-opus-4-8',
    mcp_servers: [
      { type: 'url', name: 'github', url: 'https://api.githubcopilot.com/mcp/' },
    ],
    tools: [
      { type: 'agent_toolset_20260401', default_config: { enabled: true } },
      { type: 'mcp_toolset', mcp_server_name: 'github' },
    ],
  },
);

// 2. Start a session — attach vault for MCP auth + mount the repo
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: envId,
  vault_ids: [vaultId],  // vault contains the GitHub MCP OAuth credential
  resources: [
    {
      type: 'github_repository',
      url: 'https://github.com/owner/repo',
      authorization_token: process.env.GITHUB_TOKEN,  // repo clone token (≠ MCP auth)
      checkout: { type: 'branch', name: 'main' },
    },
  ],
});
```

**Python:**

```python
import os

agent = client.beta.agents.create(
    name="GitHub Agent",
    model="claude-opus-4-8",
    mcp_servers=[{
        "type": "url",
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp/",
    }],
    tools=[
        {"type": "agent_toolset_20260401", "default_config": {"enabled": True}},
        {"type": "mcp_toolset", "mcp_server_name": "github"},
    ],
)

session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=env_id,
    vault_ids=[vault_id],  # vault contains the GitHub MCP OAuth credential
    resources=[{
        "type": "github_repository",
        "url": "https://github.com/owner/repo",
        "authorization_token": os.environ["GITHUB_TOKEN"],  # repo clone token (≠ MCP auth)
        "checkout": {"type": "branch", "name": "main"},
    }],
)
```

---

## Files API

Upload and manage files for use as session resources, and download files the agent wrote to `/mnt/session/outputs/`.

| Operation        | Method   | Path                                  | SDK |
| ---------------- | -------- | ------------------------------------- | --- |
| Upload           | `POST`   | `/v1/files`                           | `client.beta.files.upload({ file })` |
| List             | `GET`    | `/v1/files?scope_id=...`              | `client.beta.files.list({ scope_id, betas: ["managed-agents-2026-04-01"] })` |
| Get Metadata     | `GET`    | `/v1/files/{id}`                      | `client.beta.files.retrieveMetadata(id)` |
| Download         | `GET`    | `/v1/files/{id}/content`              | `client.beta.files.download(id)` → `Response` |
| Delete           | `DELETE` | `/v1/files/{id}`                      | `client.beta.files.delete(id)` |

The `scope_id` filter on List scopes the results to files written to `/mnt/session/outputs/` by that session. Without the filter, you get all files uploaded to your account.
</doc>

<doc path="shared/managed-agents-events.md">
# Managed Agents — Events & Steering

## Events

### Sending Events

Send events to a session via `POST /v1/sessions/{id}/events`.

| Event Type                | When to Send                                        |
| ------------------------- | --------------------------------------------------- |
| `user.message`            | Send a user message |
| `user.interrupt`          | Interrupt the agent while it's running |
| `user.tool_confirmation`  | Approve/deny a tool call (when `always_ask` policy) |
| `user.custom_tool_result` | Provide result for a custom tool call |
| `user.define_outcome`     | Start a rubric-graded iterate loop — see `shared/managed-agents-outcomes.md` |

### Receiving Events

Three methods:

1. **Streaming (SSE)**: `GET /v1/sessions/{id}/events/stream` — real-time Server-Sent Events. **Long-lived** — the server sends periodic heartbeats to keep the connection alive.
2. **Polling**: `GET /v1/sessions/{id}/events` — paginated event list (query params: `limit` default 1000, `page`). **Returns immediately** — this is a plain paginated GET, not a long-poll.
3. **Webhooks**: Anthropic POSTs session state transitions to your HTTPS endpoint — thin payloads (IDs only), HMAC-signed, Console-registered. See `shared/managed-agents-webhooks.md`.

All received events carry `id`, `type`, and `processed_at` (ISO 8601; `null` if not yet processed by the agent).

> ⚠️ **Robust polling (raw HTTP).** If you bypass the SDK and roll your own poll loop, don't rely on `requests` or `httpx` timeouts as wall-clock caps — they're **per-chunk** read timeouts, reset every time a byte arrives. A trickling response (heartbeats, a wedged chunked-encoding body, a misbehaving proxy) can keep the call blocked indefinitely even with `timeout=(5, 60)` or `httpx.Timeout(120)`. Neither library has a "total wall-clock" timeout built in. For a hard deadline: track `time.monotonic()` at the loop level and break/cancel if a single request exceeds your budget (e.g. via a watchdog thread, or `asyncio.wait_for()` around async httpx). **Prefer the SDK** — `client.beta.sessions.events.stream()` and `client.beta.sessions.events.list()` handle timeout + retry sanely.
>
> If `GET /v1/sessions/{id}/events` (paginated) ever hangs after headers, you've likely hit `GET /v1/sessions/{id}/events` by mistake or a server-side stall — report it; don't treat it as a client-config problem.

### Event Types (Received)

Event types use dot notation, grouped by namespace:

| Event Type | Description |
| --- | --- |
| `agent.message` | Agent text output |
| `agent.thinking` | Extended thinking blocks |
| `agent.tool_use` | Agent used a built-in tool (`agent_toolset_20260401`) |
| `agent.tool_result` | Result from a built-in tool |
| `agent.mcp_tool_use` | Agent used an MCP tool |
| `agent.mcp_tool_result` | Result from an MCP tool |
| `agent.custom_tool_use` | Agent invoked a custom tool — session goes idle, you respond with `user.custom_tool_result` |
| `agent.thread_context_compacted` | Conversation context was compacted |
| `session.status_idle` | Agent has finished the current task, and is awaiting input. It's either waiting for input to continue working via a `user.message` or blocked awaiting a `user.custom_tool_result` or `user.tool_confirmation`. The `stop_reason` attached contains more information about why the Agent has stopped working. |
| `session.status_running` | Session has starting running, and the Agent is actively doing work. |
| `session.status_rescheduled` | Session is (re)scheduling after a retryable error has occurred, ready to be picked up by the orchestration system. |
| `session.status_terminated` | Session has terminated, entering an irreversible and unusable state.  |
| `session.error` | Error occurred during processing |
| `span.model_request_start` | Model inference started |
| `span.model_request_end` | Model inference completed |
| `span.outcome_evaluation_start` / `_ongoing` / `_end` | Grader progress for outcome-oriented sessions — see `shared/managed-agents-outcomes.md` |
| `session.thread_created` | Subagent thread spawned (multiagent) — see `shared/managed-agents-multiagent.md` |
| `session.thread_status_running` / `_idle` / `_rescheduled` / `_terminated` | Subagent thread status transitions (multiagent). `_idle` carries `stop_reason`. |
| `agent.thread_message_sent` / `_received` | Cross-thread message, carries `to_session_thread_id` / `from_session_thread_id` (multiagent) |

The stream also echoes back user-sent events (`user.message`, `user.interrupt`, `user.tool_confirmation`, `user.custom_tool_result`, `user.define_outcome`).

---

## Steering Patterns

Practical patterns for driving a session via the events surface.

### Stream-first ordering

**Open the stream before sending events.** The stream only delivers events that occur *after* it's opened — it does not replay current state or historical events. If you send a message first and open the stream second, early events (including fast status transitions) arrive buffered in a single batch and you lose the ability to react to them in real time.

```ts
// ✅ Correct — stream and send concurrently
const [response] = await Promise.all([
  streamEvents(sessionId),   // opens SSE connection
  sendMessage(sessionId, text),
]);

// ❌ Wrong — events before stream opens arrive as a single buffered batch
await sendMessage(sessionId, text);
const response = await streamEvents(sessionId);
```

**For full history,** use `GET /v1/sessions/{id}/events` (paginated list) — the stream only gives you live events from connection onward.

### Reconnecting after a dropped stream

**The SSE stream has no replay.** If your connection drops (httpx read timeout, network blip) and you reconnect, you only get events emitted *after* reconnection. Any events emitted during the gap are lost from the stream.

**The consolidation pattern:** on every (re)connect, overlap the stream with a history fetch and dedupe by event ID:

```python
def connect_with_consolidation(client, session_id):
    # 1. Open the SSE stream first
    stream = client.beta.sessions.events.stream(session_id=session_id)

    # 2. Fetch history to cover any gap
    history = client.beta.sessions.events.list(
        session_id=session_id,
    )

    # 3. Yield history first, then stream — dedupe by event.id
    seen = set()
    for ev in history.data:
        seen.add(ev.id)
        yield ev
    for ev in stream:
        if ev.id not in seen:
            seen.add(ev.id)
            yield ev
```

### Message queuing

**You don't have to wait for a response before sending the next message.** User events are queued server-side and processed in order. This is useful for chat bridges where the user sends rapid follow-ups:

```ts
// All three go into one session; agent processes them in order
await sendMessage(sessionId, "Summarize the README");
await sendMessage(sessionId, "Actually also check the CONTRIBUTING guide");
await sendMessage(sessionId, "And compare the two");
// Stream once — agent responds to all three as a coherent turn
```

Events can be sent up to the Session at any time. There is no need to wait on a specific session status to enqueue new events via `client.beta.sessions.events.send()`

### Interrupt

An `interrupt` event **jumps the queue** (ahead of any pending user messages) and forces the session into `idle`. Use this for "stop" / "nevermind" / "cancel" commands:

```ts
await client.beta.sessions.events.send(sessionId, {
  events: [{ type: 'interrupt' }],
});
```

The agent stops mid-task. It does not see the interrupt as a message — it just halts. Send a follow-up `user` event to explain what to do instead. If an outcome is active, the interrupt also marks `span.outcome_evaluation_end.result: "interrupted"` (see `shared/managed-agents-outcomes.md`).

> **Note**: Interrupt events may have empty IDs in the current implementation. When troubleshooting, use the `processed_at` timestamp along with surrounding event IDs.

### Event payloads

some events carry useful metadata beyond the status change itself:

`session.status_idle` — includes a `stop_reason` field which elaborates on why the session stopped and what type of further action is required by the user.
```json
{
  "id": "sevt_456",
  "processed_at": "2026-04-07T04:27:43.197Z",
  "stop_reason": {
    "event_ids": [
      "sevt_123"
    ],
    "type": "requires_action"
  },
  "type": "status_idle"
}
```

`span.model_request_end` contains a `model_usage` field for cost tracking and efficiency analysis:

```json
{
  "type": "span.model_request_end",
  "id": "sevt_456",
  "is_error": false,
  "model_request_start_id": "sevt_123",
  "model_usage": {
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 6656,
    "input_tokens": 3571,
    "output_tokens": 727
  },
  "processed_at": "2026-04-07T04:11:32.189Z"
}
```

**`agent.thread_context_compacted`** — emitted when the conversation history was summarized to fit context. Includes `pre_compaction_tokens` so you know how much was squeezed:

```json
{
  "id": "sevt_abc123",
  "processed_at": "2026-03-24T14:05:15.787Z",
  "type": "agent.thread_context_compacted"
}
```

### Archive

When done with a session, archive it to free resources:

```ts
await client.beta.sessions.archive(sessionId);
```

> Archiving a **session** is routine cleanup — sessions are per-run and disposable. **Do not generalize this to agents or environments**: those are persistent, reusable resources, and archiving them is permanent (no unarchive; new sessions cannot reference them). See `shared/managed-agents-overview.md` → Common Pitfalls.
</doc>

<doc path="shared/managed-agents-memory.md">
# Managed Agents — Memory Stores

> **Public beta.** Memory stores ship under the `managed-agents-2026-04-01` beta header; the SDK sets it automatically on all `client.beta.memory_stores.*` calls. If `client.beta.memory_stores` is missing, upgrade to the latest SDK release.

Sessions are ephemeral by default — when one ends, anything the agent learned is gone. A **memory store** is a workspace-scoped collection of small text documents that persists across sessions. When a store is attached to a session (via `resources[]`), it is mounted into the container as a filesystem directory; the agent reads and writes it with the ordinary file tools, and a system-prompt note tells it the mount is there.

Every mutation to a memory produces an immutable **memory version** (`memver_...`), giving you an audit trail and point-in-time rollback/redact.

## Object model

| Object | ID prefix | Scope | Notes |
| --- | --- | --- | --- |
| Memory store | `memstore_...` | Workspace | Attach to sessions via `resources[]` |
| Memory | `mem_...` | Store | One text file, addressed by `path` (≤ 100KB each — prefer many small files) |
| Memory version | `memver_...` | Memory | Immutable snapshot per mutation; `operation` ∈ `created` / `modified` / `deleted` |

## Create a store

`description` is passed to the agent so it knows what the store contains — write it for the model, not for humans.

```python
store = client.beta.memory_stores.create(
    name="User Preferences",
    description="Per-user preferences and project context.",
)
print(store.id)  # memstore_01Hx...
```

Other SDKs: TypeScript `client.beta.memoryStores.create({...})`; Go `client.Beta.MemoryStores.New(ctx, ...)`. See `shared/managed-agents-api-reference.md` → SDK Method Reference for the full per-language table.

Stores support `retrieve` / `update` / `list` (with `include_archived`, `created_at_{gte,lte}` filters) / `delete` / **`archive`**. Archive makes the store read-only — existing session attachments continue, new sessions cannot reference it; no unarchive.

### Seed with content (optional)

Pre-load reference material before any session runs. `memories.create` creates a memory at the given `path`; if a memory already exists there the call returns `409` (`memory_path_conflict_error`, with the `conflicting_memory_id`). The store ID is the first positional argument.

```python
client.beta.memory_stores.memories.create(
    store.id,
    path="/formatting_standards.md",
    content="All reports use GAAP formatting. Dates are ISO-8601...",
)
```

## Attach to a session

Memory stores go in the session's `resources[]` array alongside `file` and `github_repository` resources (see `shared/managed-agents-environments.md` → Resources). Memory stores attach at **session create time only** — `sessions.resources.add()` does not accept `memory_store`.

```python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    resources=[
        {
            "type": "memory_store",
            "memory_store_id": store.id,
            "access": "read_write",  # or "read_only"; default is "read_write"
            "instructions": "User preferences and project context. Check before starting any task.",
        }
    ],
)
```

| Field | Required | Notes |
| --- | --- | --- |
| `type` | ✅ | `"memory_store"` |
| `memory_store_id` | ✅ | `memstore_...` |
| `access` | — | `"read_write"` (default) or `"read_only"` — enforced at the filesystem level on the mount |
| `instructions` | — | Session-specific guidance for this store, in addition to the store's `name`/`description`. ≤ 4,096 chars. |

**Max 8 memory stores per session.** Attach multiple when different slices of memory have different owners or lifecycles — e.g. one read-only shared-reference store plus one read-write per-user store, or one store per end-user/team/project sharing a single agent config.

### How the agent sees it (FUSE mount)

Each attached store is mounted in the session container at `/mnt/memory/<store-name>/`. The agent interacts with it using the standard file tools (`bash`, `read`, `write`, `edit`, `glob`, `grep`) — there are no dedicated memory tools. `access: "read_only"` makes the mount read-only at the filesystem level; `"read_write"` allows the agent to create, edit, and delete files under it. A short description of each mount (name, path, `instructions`, access) is automatically injected into the system prompt so the agent knows the store exists without you having to mention it.

Writes the agent makes under the mount are persisted back to the store and produce memory versions just like host-side `memories.update` calls.

## Manage memories directly (host-side)

Use these for review workflows, correcting bad memories, or seeding stores out-of-band.

### List

Returns `Memory | MemoryPrefix` entries — a `MemoryPrefix` (`type: "memory_prefix"`, just a `path`) is a directory-like node when listing hierarchically. Use `path_prefix` to scope (include a trailing slash: `"/notes/"` matches `/notes/a.md` but not `/notes_backup/old.md`) and `depth` to bound the tree walk. `order_by` / `order` sort the result. Pass `view="full"` to include `content` in each item; the default `"basic"` returns metadata only.

```python
for m in client.beta.memory_stores.memories.list(store.id, path_prefix="/"):
    if m.type == "memory":
        print(f"{m.path}  ({m.content_size_bytes} bytes, sha={m.content_sha256[:8]})")
    else:  # "memory_prefix"
        print(f"{m.path}/")
```

### Read

```python
mem = client.beta.memory_stores.memories.retrieve(memory_id, memory_store_id=store.id)
print(mem.content)
```

`retrieve` defaults to `view="full"` (content included); `view` matters mainly on list endpoints.

### Create vs. update

| Operation | Addressed by | Semantics |
| --- | --- | --- |
| `memories.create(store_id, path=..., content=...)` | **Path** | Create at `path`. `409` (`memory_path_conflict_error`, includes `conflicting_memory_id`) if the path is already occupied. |
| `memories.update(mem_id, memory_store_id=..., path=..., content=...)` | **`mem_...` ID** | Mutate existing memory. Change `content`, `path` (rename), or both. Renaming onto an occupied path returns the same `409 memory_path_conflict_error`. |

```python
mem = client.beta.memory_stores.memories.create(
    store.id,
    path="/preferences/formatting.md",
    content="Always use tabs, not spaces.",
)

client.beta.memory_stores.memories.update(
    mem.id,
    memory_store_id=store.id,
    path="/archive/2026_q1_formatting.md",  # rename
)
```

### Optimistic concurrency (precondition on `update`)

`memories.update` accepts a `precondition` so you can read → modify → write back without clobbering a concurrent writer. The only supported type is `content_sha256`. On mismatch the API returns `409` (`memory_precondition_failed_error`) — re-read and retry against fresh state.

```python
client.beta.memory_stores.memories.update(
    mem.id,
    memory_store_id=store.id,
    content="CORRECTED: Always use 2-space indentation.",
    precondition={"type": "content_sha256", "content_sha256": mem.content_sha256},
)
```

### Delete

```python
client.beta.memory_stores.memories.delete(mem.id, memory_store_id=store.id)
```

Pass `expected_content_sha256` for a conditional delete.

## Audit and rollback — memory versions

Every mutation creates an immutable `memver_...` snapshot. Versions accumulate for the lifetime of the parent memory; `memories.retrieve` always returns the current head, the version endpoints give you history.

| Operation that triggers it | `operation` field on the version |
| --- | --- |
| `memories.create` at a new path | `"created"` |
| `memories.update` changing `content`, `path`, or both (or an agent-side write to the mount) | `"modified"` |
| `memories.delete` | `"deleted"` |

Each version also records `created_by` — an actor object with `type` ∈ `session_actor` / `api_actor` / `user_actor` — and, after redaction, `redacted_at` + `redacted_by`.

### List versions

Newest-first, paginated. Filter by `memory_id`, `operation`, `session_id`, `api_key_id`, or `created_at_gte` / `created_at_lte`. Pass `view="full"` to include `content`; default is metadata-only.

```python
for v in client.beta.memory_stores.memory_versions.list(store.id, memory_id=mem.id):
    print(f"{v.id}: {v.operation}")
```

### Retrieve a version

```python
version = client.beta.memory_stores.memory_versions.retrieve(
    version_id, memory_store_id=store.id
)
print(version.content)
```

### Redact a version

Scrubs content from a historical version while preserving the audit trail (actor + timestamps). Clears `content`, `content_sha256`, `content_size_bytes`, and `path`; everything else stays. Use for leaked secrets, PII, or user-deletion requests.

```python
client.beta.memory_stores.memory_versions.redact(version_id, memory_store_id=store.id)
```

## Endpoint reference

See `shared/managed-agents-api-reference.md` → Memory Stores / Memories / Memory Versions for the full HTTP method/path tables. Raw HTTP base path:

```
POST   /v1/memory_stores
POST   /v1/memory_stores/{memory_store_id}/archive
GET    /v1/memory_stores/{memory_store_id}/memories
PATCH  /v1/memory_stores/{memory_store_id}/memories/{memory_id}
GET    /v1/memory_stores/{memory_store_id}/memory_versions
POST   /v1/memory_stores/{memory_store_id}/memory_versions/{version_id}/redact
```

For cURL examples and the CLI (`ant beta:memory-stores ...`), WebFetch the Memory URL in `shared/live-sources.md` → Managed Agents.
</doc>

<doc path="shared/managed-agents-multiagent.md">
# Managed Agents — Multiagent Sessions

A coordinator agent can delegate to other agents within one session. All agents **share the container and filesystem**; each runs in its own **thread** — a context-isolated event stream with its own conversation history, model, system prompt, tools, MCP servers, and skills (from that agent's own config). Threads are persistent: the coordinator can send a follow-up to a subagent it called earlier and that subagent retains its prior turns.

The SDK sets the `managed-agents-2026-04-01` beta header automatically on all `client.beta.{agents,sessions}.*` calls; no additional header is required for multiagent.

---

## Declare the roster on the coordinator

`multiagent` is a **top-level field** on `agents.create()` / `agents.update()` — **not** a `tools[]` entry. `agents` lists 1–20 roster entries. Nothing changes on `sessions.create()` — the roster is resolved from the coordinator's config.

```python
orchestrator = client.beta.agents.create(
    name="Engineering Lead",
    model="claude-opus-4-8",
    system="You coordinate engineering work. Delegate code review to the reviewer and test writing to the test agent.",
    tools=[{"type": "agent_toolset_20260401"}],
    multiagent={
        "type": "coordinator",
        "agents": [
            reviewer.id,                                            # bare string — latest version
            {"type": "agent", "id": test_writer.id, "version": 4},  # pinned version
            {"type": "self"},                                       # the coordinator itself
        ],
    },
)

session = client.beta.sessions.create(agent=orchestrator.id, environment_id=env.id)
```

| Roster entry | Shape | Notes |
|---|---|---|
| String shorthand | `"agent_abc123"` | References the latest version of a stored agent. |
| Agent reference | `{type: "agent", id, version?}` | Omit `version` to pin the latest at coordinator save time. |
| Self | `{type: "self"}` | The coordinator can spawn copies of itself. |

Up to **20 unique agents** in the roster; the coordinator may spawn **multiple copies** of each. **One level of delegation only** — depth > 1 is ignored.

---

## Threads

The session-level event stream is the **primary thread** — it shows the coordinator's trace plus a condensed view of subagent activity (thread status transitions and cross-thread messages, not every subagent tool call). Drill into a specific subagent via the per-thread endpoints:

| Operation | HTTP | SDK (`client.beta.sessions.threads.*`) |
|---|---|---|
| List threads | `GET /v1/sessions/{sid}/threads` | `.list(session_id)` |
| Retrieve one | `GET /v1/sessions/{sid}/threads/{tid}` | `.retrieve(thread_id, session_id=...)` |
| Archive | `POST /v1/sessions/{sid}/threads/{tid}/archive` | `.archive(thread_id, session_id=...)` |
| List thread events | `GET /v1/sessions/{sid}/threads/{tid}/events` | `.events.list(thread_id, session_id=...)` |
| Stream thread events | `GET /v1/sessions/{sid}/threads/{tid}/stream` | `.events.stream(thread_id, session_id=...)` |

Each `SessionThread` carries `id`, `status` (`running` | `idle` | `rescheduling` | `terminated`), `agent` (a resolved snapshot of the agent config — `id`, `name`, `model`, `system`, `tools`, `skills`, `mcp_servers`, `version`), `parent_thread_id` (null for the primary thread, which is included in the list), `archived_at`, and optional `stats`/`usage`. **Session status aggregates thread statuses** — if any thread is `running`, `session.status` is `running`. Max **25 concurrent threads**. When draining a per-thread stream, break on `session.thread_status_idle` (and check its `stop_reason` as you would for the session-level idle).

---

## Multiagent events (on the session stream)

| Event | Payload highlights | Meaning |
|---|---|---|
| `session.thread_created` | `session_thread_id`, `agent_name` | A new thread was created. |
| `session.thread_status_running` | `session_thread_id`, `agent_name` | Thread started activity. |
| `session.thread_status_idle` | `session_thread_id`, `agent_name`, **`stop_reason`** | Thread is awaiting input. Inspect `stop_reason` (same shape as `session.status_idle.stop_reason`). |
| `session.thread_status_rescheduled` | `session_thread_id`, `agent_name` | Thread is rescheduling after a retryable error. |
| `session.thread_status_terminated` | `session_thread_id`, `agent_name` | Thread was archived or hit a terminal error. |
| `agent.thread_message_sent` | `to_session_thread_id`, `to_agent_name`, `content` | Coordinator sent a follow-up to another thread. |
| `agent.thread_message_received` | `from_session_thread_id`, `from_agent_name`, `content` | An agent delivered its result to the coordinator. |

---

## Tool permissions and custom tools from subagent threads

When a subagent needs your client (an `always_ask` confirmation, or a custom tool result), the request is **cross-posted to the primary thread** with `session_thread_id` identifying the originating thread — so you only need to watch the session stream. Reply with `user.tool_confirmation` (carrying `tool_use_id`) or `user.custom_tool_result` (carrying `custom_tool_use_id`), and **echo the `session_thread_id` from the originating event** (the SDK param type and docstring expect it). The server also routes by the tool-use ID, so the echo is belt-and-suspenders rather than load-bearing — but include it.

```python
for event_id in stop.event_ids:
    pending = events_by_id[event_id]
    confirmation = {
        "type": "user.tool_confirmation",
        "tool_use_id": event_id,
        "result": "allow",
    }
    if pending.session_thread_id is not None:
        confirmation["session_thread_id"] = pending.session_thread_id
    client.beta.sessions.events.send(session.id, events=[confirmation])
```

The same pattern applies to `user.custom_tool_result`.

---

## Pitfalls

- **Don't put the roster on `sessions.create()` or in `tools[]`.** `multiagent` is a top-level agent field; update the coordinator, then start a session that references it.
- **Don't assume shared context.** Threads share the filesystem but not conversation history or tools. If the coordinator needs a subagent to act on something, it must say so in the delegated message (or write it to disk).
- **Depth > 1 is ignored.** A subagent's own `multiagent` roster (if any) doesn't cascade — only the session's coordinator delegates.

For per-language bindings beyond Python, WebFetch `https://platform.claude.com/docs/en/managed-agents/multi-agent.md` (see `shared/live-sources.md`).
</doc>

<doc path="shared/managed-agents-onboarding.md">
# Managed Agents — Onboarding Flow

> **Invoked via `/claude-api managed-agents-onboard`?** You're in the right place. Run the interview below — don't summarize it back to the user, ask the questions.

Use this when a user wants to set up a Managed Agent from scratch: **branch on know-vs-explore → configure the template → set up the session → pre-flight viability check → emit working code.** The pre-flight check (§3) is not optional — a setup missing a tool, credential, or data access it needs will fail mid-run, and the gap is usually visible at setup time.

> Read `shared/managed-agents-core.md` alongside this — it has full detail for each knob. This doc is the interview script, not the reference.

---

Claude Managed Agents is a hosted agent: Anthropic runs the agent loop on its orchestration layer and provisions a sandboxed container per session where the agent's tools execute (or, with a `self_hosted` environment, your own worker runs the tools — see `shared/managed-agents-self-hosted-sandboxes.md`). You supply the agent config and the environment config; the harness — event stream, sandbox orchestration, prompt caching, context compaction, and extended thinking — is handled for you.

**What you supply:**
- **An agent config** — tools, skills, model, system prompt. Reusable and versioned.
- **An environment config** — the sandbox your agent's tools execute in (`cloud`: networking, packages; or `self_hosted`: your own infra). Reusable across agents.

Each run of the agent is a **session**.

---

## 1. Know or explore?

Ask the user:

> Do you already know the agent you want to build, or would you like to explore some common patterns first?

### Explore path — show the patterns

Four shapes, same runtime code path (`sessions.create()` → `sessions.events.send()` → stream). Only the trigger and sink differ.

| Pattern | Trigger | Example |
|---|---|---|
| Event-triggered | Webhook | GitHub PR push → CMA (GitHub tool) → Slack |
| Scheduled | Cron | Daily brief: browser + GitHub + Jira → CMA → Slack |
| Fire-and-forget PR | Human | Slack slash-command → CMA (GitHub tool) → PR passing CI |
| Research + dashboard | Human | Topic → CMA (web search + `frontend-design` skill) → HTML dashboard |

Ask which shape fits, then continue with the Know path using it as the reference.

### Know path — configure template

Three rounds. Batch the questions in each round; don't ask them one at a time.

**Round A — Tools.** Start here; it's the most concrete part. Three types; ask which the user wants (any combination):

| Type | What it is | How to guide |
|---|---|---|
| **Prebuilt Claude Agent tools** (`agent_toolset_20260401`) | Ready-to-use: `bash`, `read`, `write`, `edit`, `glob`, `grep`, `web_fetch`, `web_search`. Enable all at once, or individually via `enabled: true/false`. | Recommend enabling the full toolset. List the 8 tools so the user knows what they're getting. Full detail: `shared/managed-agents-tools.md` → Agent Toolset. |
| **MCP tools** | Third-party integrations (GitHub, Linear, Asana, etc.) via `mcp_toolset`. Credentials live in a vault, not inline. | Ask which services. For each, walk through MCP server URL + vault credentials. Full detail: `shared/managed-agents-tools.md` → MCP Servers + Vaults. |
| **Custom tools** | The user's own app handles these tool calls — agent fires `agent.custom_tool_use`, the app sends a result message back. | Ask for each tool: name, description, input schema. The app code that handles the event is *their* code — don't generate it. Full detail: `shared/managed-agents-tools.md` → Custom Tools. |

**Round B — Skills, files, and repos.** What the agent has on hand when it starts.

*Skills* — two types; both work the same way — Claude auto-uses them when relevant. Max 20 per agent.
- [ ] **Pre-built Agent Skills**: `xlsx`, `docx`, `pptx`, `pdf`. Reference by name.
- [ ] **Custom Skills**: skills uploaded to the user's org via the Skills API. Reference by `skill_id` + optional `version`. If the skill doesn't exist yet, walk the user through `POST /v1/skills` + `POST /v1/skills/{id}/versions` (beta header `skills-2025-10-02`). Full detail: `shared/managed-agents-tools.md` → Skills + Skills API.

*GitHub repositories* — any repos the agent needs on-disk? For each:
- [ ] Repo URL (`https://github.com/org/repo`)
- [ ] `authorization_token` (PAT or GitHub App token scoped to the repo)
- [ ] Optional `mount_path` (defaults to `/workspace/<repo-name>`) and `checkout` (branch or SHA)

Emit as `resources: [{type: "github_repository", url, authorization_token, ...}]`. Full detail: `shared/managed-agents-environments.md` → GitHub Repositories.

> ‼️ **PR creation needs the GitHub MCP server too.** `github_repository` gives filesystem access only — to open PRs, also attach the GitHub MCP server in Round A and credential it via a vault. The workflow is: edit files in the mounted repo → push branch via `bash` → create PR via the MCP `create_pull_request` tool.

*Files* — any local files to seed the session with? For each:
- [ ] Upload via the Files API → persist `file_id`
- [ ] Choose a `mount_path` — absolute, e.g. `/workspace/data.csv` (parents auto-created; files mount read-only)

Emit as `resources: [{type: "file", file_id, mount_path}]`. Max 999 file resources. Agent working directory defaults to `/workspace`. Full detail: `shared/managed-agents-environments.md` → Files API.

**Round C — Identity, success criteria, environment:**
- [ ] Name?
- [ ] Job (one or two sentences — becomes the system prompt)?
- [ ] **What does "done" look like?** Push for concrete, checkable success criteria — not "a good report" but "a CSV with a numeric `price` column per SKU." Explicit criteria give the agent a clear target and let you verify the result; vague ones leave it guessing what "done" means. If they're gradeable, plan to wire an **Outcome** in §2 so the harness grades-and-revises against them. See `shared/managed-agents-outcomes.md`.
- [ ] Networking: unrestricted internet from the container, or lock egress to specific hosts? (If locked, MCP server domains must be in `allowed_hosts` or tools silently fail.)
- [ ] Model? (default `claude-opus-4-8`)

---

## 2. Set up the session

Per-run. Points at the agent + environment, attaches credentials, kicks off.

**Vault credentials** (if the agent declared MCP servers):
- [ ] Existing vault, or create one? (`client.beta.vaults.create()` + `vaults.credentials.create()`)

Credentials are write-only, matched to MCP servers by URL, auto-refreshed. See `shared/managed-agents-tools.md` → Vaults.

**Kickoff — pick one:**
- [ ] **Conversational:** a first `user.message` to the agent.
- [ ] **Outcome-graded** (recommended when §Round C produced checkable criteria): send a `user.define_outcome` with a rubric *instead of* a `user.message` — the harness iterates and grades against the rubric until satisfied. Don't send both. See `shared/managed-agents-outcomes.md`.

Session creation blocks until all resources mount. Open the event stream before sending the kickoff. Stream is SSE; break on `session.status_terminated`, or on `session.status_idle` with a terminal `stop_reason` — i.e. anything except `requires_action`, which fires transiently while the session waits on a tool confirmation or custom-tool result (see `shared/managed-agents-client-patterns.md` Pattern 5). Usage lands on `span.model_request_end`. Agent-written artifacts end up in `/mnt/session/outputs/` — download via `files.list({scope_id: session.id, betas: ["managed-agents-2026-04-01"]})`.

**Console escape hatch.** In the runtime block you emit, print the session's Console URL right after `sessions.create()` so the user can watch it in the UI while iterating: `print(f"Watch in Console: https://platform.claude.com/workspaces/default/sessions/{session.id}")` (swap `default` for the user's workspace slug if they named one).

---

## 3. Pre-flight viability check — reconcile the job against the resources

**Do this before emitting any code.** A common, avoidable failure is an under-resourced run: the ask is clear, but the agent is missing a tool, a credential, data access, or the context to act. The agent discovers the gap a few turns in, flails, and gives up — burning the budget to produce nothing. The gap is usually visible at setup time. Catch it here, not after the session fails.

Walk the stated job clause by clause. For each action the agent must take, confirm a resource covers it — and name the gap out loud if one doesn't:

| Gap class | Check | If missing |
|---|---|---|
| **Tool / integration** (most catchable upfront — config is statically inspectable) | Every verb in the job maps to an enabled tool or MCP server. "Triage tickets" → a ticketing MCP server; "open a PR" → GitHub MCP server (a `github_repository` mount alone can't open PRs); "search the web" → `web_search` enabled in the toolset. | Add the tool/MCP server in §Round A, or cut the ask from the job. |
| **Credential / access** | Every MCP server has a vault credential attached (§2). Every external host the job touches is reachable — networking `unrestricted`, or the host is in `allowed_hosts`. | Create/attach the vault; widen `allowed_hosts`. These don't fail until runtime — the smoke-test in §4 is how you surface them cheaply. |
| **Data** | Every file, dataset, or repo the job references is mounted as a `resource` (file, `github_repository`, or memory store). | Upload + mount it in §Round B, or tell the agent where to fetch it from. |
| **Prompt quality / criteria** | The job is specific enough to act on, and "done" is checkable (§Round C). | Tighten the job; wire an Outcome. |

State any unmet gaps to the user and resolve them before generating code. Don't emit a config you already know is under-resourced — an agent can't complete a task it lacks the tools, credentials, or data for.

---

## 4. Emit the code

Go straight from the last interview answer to the code — no preamble about the setup-vs-runtime split, no "the critical thing to internalize…", no lecture about `agents.create()` being one-time. The two-block structure below already shows that; don't narrate it. Generate **two clearly-separated blocks**:

**Block 1 — Setup (run once, store the IDs).** Prefer emitting this as **YAML files + `ant` CLI commands** — agents and environments are version-controlled definitions, and the CLI flow is what users should check into their repo and run from CI. Fall back to SDK code only if the user explicitly wants setup in-language or the `ant` CLI is unavailable.

Emit:
1. `<name>.agent.yaml` with everything from §Round A–C (flat: `name`, `model`, `system`, `tools`, `mcp_servers`, `skills`)
2. `<name>.environment.yaml` with §Round C networking
3. The apply commands:
   ```sh
   AGENT_ID=$(ant beta:agents create < <name>.agent.yaml --transform id -r)
   ENV_ID=$(ant beta:environments create < <name>.environment.yaml --transform id -r)
   # CI sync: ant beta:agents update --agent-id "$AGENT_ID" --version N < <name>.agent.yaml
   ```

See `shared/anthropic-cli.md` for the full CLI reference. If emitting SDK code instead, label it `# ONE-TIME SETUP — run once, save the IDs to config/.env` and call `environments.create()` → `agents.create()`.

**Block 2 — Runtime (run on every invocation).** This is SDK code in the detected language (Python/TS/cURL — see SKILL.md → Language Detection). The runtime path needs to react programmatically to events (tool confirmations, custom tool results, reconnect), which is SDK territory — don't emit shell loops here.
1. Load `env_id` + `agent_id` from config/env
2. `sessions.create(agent=AGENT_ID, environment_id=ENV_ID, resources=[...], vault_ids=[...])` — this blocks until resources mount, so a bad file/repo mount surfaces *here*, before any tokens are spent.
3. **Smoke-test first when the job depends on MCP servers, credentials, or reachable hosts.** Credential and MCP-connectivity failures don't surface at `sessions.create()` — only when the agent first tries to use them. Send one cheap probe turn ("Confirm you can reach <service> and list 1–2 items; don't start the task yet"), check it succeeded, *then* send the real kickoff. A few hundred tokens here beats a runaway session that flails on a missing credential and gives up. Skip for agents with no external dependencies.
4. Open stream, `events.send()` the kickoff (a `user.message`, or a `user.define_outcome` if §2 chose the outcome-graded path), loop until `session.status_terminated` or `session.status_idle && stop_reason.type !== 'requires_action'` (see `shared/managed-agents-client-patterns.md` Pattern 5 for the full gate — do not break on bare `session.status_idle`)

> ⚠️ **Never emit `agents.create()` and `sessions.create()` in the same unguarded block.** That teaches the user to create a new agent on every run — the #1 anti-pattern. If they need a single script, wrap agent creation in `if not os.getenv("AGENT_ID"):`.

Pull exact syntax from `python/managed-agents/README.md`, `typescript/managed-agents/README.md`, or `curl/managed-agents.md`. Don't invent field names.
</doc>

<doc path="shared/managed-agents-outcomes.md">
# Managed Agents — Outcomes

An **outcome** elevates a session from *conversation* to *work*: you state what "done" looks like, and the harness runs an iterate → grade → revise loop until the artifact meets the rubric, hits `max_iterations`, or is interrupted. A separate **grader** (independent context window) scores each iteration against your rubric and feeds per-criterion gaps back to the agent.

The SDK sets the `managed-agents-2026-04-01` beta header automatically on all `client.beta.sessions.*` calls; no additional header is required for outcomes.

---

## The `user.define_outcome` event

Outcomes are not a field on `sessions.create()`. You create a normal session, then send a `user.define_outcome` event. The agent starts working on receipt — **do not also send a `user.message`** to kick it off.

```python
session = client.beta.sessions.create(
    agent=AGENT_ID,
    environment_id=ENVIRONMENT_ID,
    title="Financial analysis on Costco",
)

client.beta.sessions.events.send(
    session_id=session.id,
    events=[
        {
            "type": "user.define_outcome",
            "description": "Build a DCF model for Costco in .xlsx",
            "rubric": {"type": "text", "content": RUBRIC_MD},
            # or: "rubric": {"type": "file", "file_id": rubric.id}
            "max_iterations": 5,  # optional; default 3, max 20
        }
    ],
)
```

| Field | Type | Notes |
|---|---|---|
| `type` | `"user.define_outcome"` | |
| `description` | string | The task. This is what the agent works toward — no separate `user.message` needed. |
| `rubric` | `{type: "text", content}` \| `{type: "file", file_id}` | **Required.** Markdown with explicit, independently gradeable criteria. Upload once via `client.beta.files.upload(...)` (beta `files-api-2025-04-14`) to reuse across sessions. |
| `max_iterations` | int | Optional. Default **3**, max **20**. |

The event is echoed back on the stream with a server-assigned `outcome_id` and `processed_at`.

> **Writing rubrics.** Use explicit, gradeable criteria ("CSV has a numeric `price` column"), not vibes ("data looks good") — the grader scores each criterion independently, so vague criteria produce noisy loops. If you don't have a rubric, have Claude analyze a known-good artifact and turn that analysis into one.

---

## Outcome-specific events

These appear on the standard event stream (`sessions.events.stream` / `.list`) alongside the usual `agent.*` / `session.*` events.

| Event | Payload highlights | Meaning |
|---|---|---|
| `span.outcome_evaluation_start` | `outcome_id`, `iteration` (0-indexed) | Grader began scoring iteration *N*. |
| `span.outcome_evaluation_ongoing` | `outcome_id` | Heartbeat while the grader runs. Grader reasoning is opaque — you see *that* it's working, not *what* it's thinking. |
| `span.outcome_evaluation_end` | `outcome_evaluation_start_id`, `outcome_id`, `iteration`, `result`, `explanation`, `usage` | Grader finished one iteration. `result` drives what happens next (table below). |

### `span.outcome_evaluation_end.result`

| `result` | Next |
|---|---|
| `satisfied` | Session → `idle`. Terminal for this outcome. |
| `needs_revision` | Agent starts another iteration. |
| `max_iterations_reached` | No further grader cycles. Agent may run one final revision, then session → `idle`. |
| `failed` | Session → `idle`. Rubric fundamentally doesn't match the task (e.g. description and rubric contradict). |
| `interrupted` | Only emitted if `_start` had already fired before a `user.interrupt` arrived. |

```json
{
  "type": "span.outcome_evaluation_end",
  "id": "sevt_01jkl...",
  "outcome_evaluation_start_id": "sevt_01def...",
  "outcome_id": "outc_01a...",
  "result": "satisfied",
  "explanation": "All 12 criteria met: revenue projections use 5 years of historical data, ...",
  "iteration": 0,
  "usage": { "input_tokens": 2400, "output_tokens": 350, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 1800 },
  "processed_at": "2026-03-25T14:03:00Z"
}
```

---

## Checking status & retrieving deliverables

**Status** — either watch the stream for `span.outcome_evaluation_end`, or poll the session and read `outcome_evaluations`:

```python
session = client.beta.sessions.retrieve(session.id)
for ev in session.outcome_evaluations:
    print(f"{ev.outcome_id}: {ev.result}")  # outc_01a...: satisfied
```

**Deliverables** — the agent writes to `/mnt/session/outputs/`. Once idle, fetch via the Files API with `scope_id=session.id`. This is the same session-outputs mechanism documented in `shared/managed-agents-environments.md` → Session outputs (including the dual-beta-header requirement on `files.list`).

---

## Interaction rules & pitfalls

- **One outcome at a time.** Chain by sending the next `user.define_outcome` only after the previous one's terminal `span.outcome_evaluation_end` (`satisfied` / `max_iterations_reached` / `failed` / `interrupted`). The session retains history across chained outcomes.
- **Steering is allowed but optional.** You *may* send `user.message` events mid-outcome to nudge direction, but the agent already knows to keep working until terminal — don't send "keep going" prompts.
- **`user.interrupt` pauses the current outcome** — it marks `result: "interrupted"` and leaves the session `idle`, ready for a new outcome or conversational turn.
- **After terminal, the session is reusable** — continue conversationally or define a new outcome.
- **Outcome ≠ session-create field.** Don't put `outcome`, `rubric`, or `description` on `sessions.create()` — outcomes are always sent as a `user.define_outcome` event.
- **Idle-break gate is unchanged.** In your drain loop, keep using `event.type === 'session.status_idle' && event.stop_reason?.type !== 'requires_action'` — do **not** gate on `span.outcome_evaluation_end` alone (on `needs_revision` the session keeps running). See `shared/managed-agents-client-patterns.md` Pattern 5.

For the raw HTTP shapes and per-language SDK bindings beyond Python, WebFetch `https://platform.claude.com/docs/en/managed-agents/define-outcomes.md` (see `shared/live-sources.md`).
</doc>

<doc path="shared/managed-agents-overview.md">
# Managed Agents — Overview

Managed Agents provisions a container per session as the agent's workspace. The agent loop runs on Anthropic's orchestration layer; the container is where the agent's *tools* execute — bash commands, file operations, code. You create a persisted **Agent** config (model, system prompt, tools, MCP servers, skills), then start **Sessions** that reference it. The session streams events back to you; you send user messages and tool results in.

## ⚠️ THE MANDATORY FLOW: Agent (once) → Session (every run)

**Why agents are separate objects: versioning.** An agent is a persisted, versioned config — every update creates a new immutable version, and sessions pin to a version at creation time. This lets you iterate on the agent (tweak the prompt, add a tool) without breaking sessions already running, roll back if a change regresses, and A/B test versions side-by-side. None of that works if you `agents.create()` fresh on every run.

Every session references a pre-created `/v1/agents` object. Create the agent once, store the ID, and reuse it across runs.

| Step | Call | Frequency |
|---|---|---|
| 1 | `POST /v1/agents` — `model`, `system`, `tools`, `mcp_servers`, `skills` live here | **ONCE.** Store `agent.id` **and** `agent.version`. |
| 2 | `POST /v1/sessions` — `agent: "agent_abc123"` or `{type: "agent", id, version}` | **Every run.** String shorthand uses latest version. |

If you're about to write `sessions.create()` with `model`, `system`, or `tools` on the session body — **stop**. Those fields live on `agents.create()`. The session takes a *pointer* only.

**When generating code, separate setup from runtime.** `agents.create()` belongs in a setup script (or a guarded `if agent_id is None:` block), not at the top of the hot path. If the user's code calls `agents.create()` on every invocation, they're accumulating orphaned agents and paying the create latency for nothing. The correct shape is: create once → persist the ID (config file, env var, secrets manager) → every run loads the ID and calls `sessions.create()`.

**To change the agent's behavior, use `POST /v1/agents/{id}` — don't create a new one.** Each update bumps the version; running sessions keep their pinned version, new sessions get the latest (or pin explicitly via `{type: "agent", id, version}`). See `shared/managed-agents-core.md` → Agents → Versioning. To change `tools`/`mcp_servers`/`vault_ids` on **one running session** without touching the agent object, use `sessions.update()` — see `shared/managed-agents-core.md` → Updating the agent configuration mid-session.

## Beta Headers

Managed Agents is in beta. The SDK sets required beta headers automatically:

| Beta Header                    | What it enables                                      |
| ------------------------------ | ---------------------------------------------------- |
| `managed-agents-2026-04-01`    | Agents, Environments, Sessions, Events, Session Resources, Session Threads, Outcomes, Multiagent, Vaults, Credentials, Memory Stores |
| `skills-2025-10-02`            | Skills API (for managing custom skill definitions)   |
| `files-api-2025-04-14`         | Files API for file uploads                           |

**Which beta header goes where:** The SDK sets `managed-agents-2026-04-01` automatically on `client.beta.{agents,environments,sessions,vaults,memory_stores}.*` calls, and `files-api-2025-04-14` / `skills-2025-10-02` automatically on `client.beta.files.*` / `client.beta.skills.*` calls. You do NOT need to add the Skills or Files beta header when calling Managed Agents endpoints. **Exception — session-scoped file listing:** `client.beta.files.list({scope_id: session.id})` is a Files endpoint that takes a Managed Agents parameter, so it needs **both** headers. Pass `betas: ["managed-agents-2026-04-01"]` explicitly on that call (the SDK adds the Files header; you add the Managed Agents one). See `shared/managed-agents-environments.md` → Session outputs.


## Reading Guide

| User wants to...                       | Read these files                                        |
| -------------------------------------- | ------------------------------------------------------- |
| **Get started from scratch / "help me set up an agent"** | `shared/managed-agents-onboarding.md` — guided interview (WHERE→WHO→WHAT→WATCH), then emit code |
| Understand how the API works           | `shared/managed-agents-core.md`                         |
| See the full endpoint reference        | `shared/managed-agents-api-reference.md`                |
| **Create an agent** (required first step) | `shared/managed-agents-core.md` (Agents section) + language file |
| Update/version an agent                | `shared/managed-agents-core.md` (Agents → Versioning) — update, don't re-create |
| Create a session                       | `shared/managed-agents-core.md` + `{lang}/managed-agents/README.md` |
| Configure tools and permissions        | `shared/managed-agents-tools.md`                        |
| Set up MCP servers                     | `shared/managed-agents-tools.md` (MCP Servers section)  |
| Stream events / handle tool_use        | `shared/managed-agents-events.md` + language file       |
| Get notified of session state changes via webhook (no polling) | `shared/managed-agents-webhooks.md` — Console-registered endpoint, HMAC verify, thin payload + fetch |
| Define an outcome / rubric-graded iterate loop | `shared/managed-agents-outcomes.md` — `user.define_outcome` event, grader, `span.outcome_evaluation_*` events |
| Coordinate multiple agents / subagents / threads | `shared/managed-agents-multiagent.md` — `multiagent: {type: "coordinator", agents: [...]}` on the agent, session threads, cross-posted tool confirmations |
| Set up environments                    | `shared/managed-agents-environments.md` + language file |
| Run tool execution in your own infra / VPC (self-hosted sandbox) | `shared/managed-agents-self-hosted-sandboxes.md` — `config:{type:"self_hosted"}`, `ANTHROPIC_ENVIRONMENT_KEY`, `EnvironmentWorker.run()` / `ant beta:worker poll` |
| Upload files / attach repos            | `shared/managed-agents-environments.md` (Resources)     |
| Give agents persistent memory across sessions | `shared/managed-agents-memory.md` — memory stores, `memory_store` session resource, preconditions, versions/redact |
| Define agents/environments as version-controlled YAML; drive the API from the shell | `shared/anthropic-cli.md` — `ant beta:agents create < agent.yaml`, `--transform`, `@file` inlining |
| Store MCP credentials                  | `shared/managed-agents-tools.md` (Vaults section)       |
| Call a non-MCP API / CLI that needs a secret | `shared/managed-agents-client-patterns.md` Pattern 9 — no container env vars; vaults are MCP-only; keep the secret host-side via a custom tool |

## Common Pitfalls

- **Agent FIRST, then session — NO EXCEPTIONS** — the session's `agent` field accepts **only** a string ID or `{type: "agent", id, version}`. `model`, `system`, `tools`, `mcp_servers`, `skills` are **top-level fields on `POST /v1/agents`**, never on `sessions.create()`. If the user hasn't created an agent, that is step zero of every example.
- **Agent ONCE, not every run** — `agents.create()` is a setup step. Store the returned `agent_id` and reuse it; don't call `agents.create()` at the top of your hot path. If the agent's config needs to change, `POST /v1/agents/{id}` — each update creates a new version, and sessions can pin to a specific version for reproducibility.
- **MCP auth goes through vaults** — the agent's `mcp_servers` array declares `{type, name, url}` only (no auth). Credentials live in vaults (`client.beta.vaults.credentials.create`) and attach to sessions via `vault_ids`. Anthropic auto-refreshes OAuth tokens using the stored refresh token.
- **Reconcile resources before the first run** — a session with a clear ask but a missing tool, credential, data mount, or context will discover the gap mid-run, then flail and give up. Before creating the session, check that every action in the task maps to a configured tool/MCP server, every MCP server has a vault credential, and every referenced file/host is mounted/reachable. When helping a user set one up, run the reconciliation in `shared/managed-agents-onboarding.md` → §3 Pre-flight viability check.
- **Stream to get events** — `GET /v1/sessions/{id}/events/stream` is the primary way to receive agent output in real-time.
- **SSE stream has no replay — reconnect with consolidation** — if the stream drops while a `agent.tool_use`, `agent.mcp_tool_use`, or `agent.custom_tool_use` is pending resolution (`user.tool_confirmation` for the first two, `user.custom_tool_result` for the last one), the session deadlocks (client disconnects → session idles → reconnect happens → no client resolution happens). On every (re)connect: open stream with `GET /v1/sessions/{id}/events/stream` , fetch `GET /v1/sessions/{id}/events`, dedupe by event ID, then proceed. See `shared/managed-agents-events.md` → Reconnecting after a dropped stream.
- **Don't trust HTTP-library timeouts as wall-clock caps** — `requests` `timeout=(c, r)` and `httpx.Timeout(n)` are *per-chunk* read timeouts; they reset every byte, so a trickling connection can block indefinitely. For a hard deadline on raw-HTTP polling, track `time.monotonic()` at the loop level and bail explicitly. Prefer the SDK's `sessions.events.stream()` / `session.events.list()` over hand-rolled HTTP. See `shared/managed-agents-events.md` → Receiving Events.
- **Messages queue** — you can send events while the session is `running` or `idle`; they're processed in order. No need to wait for a response before sending the next message.
- **Environment `config.type` is `"cloud"` or `"self_hosted"`** — `cloud` runs the container on Anthropic's infrastructure; `self_hosted` moves tool execution to your own (see `shared/managed-agents-self-hosted-sandboxes.md`).
- **Archive is permanent on every resource** — archiving an agent, environment, session, vault, credential, or memory store makes it read-only with no unarchive. For agents, environments, and memory stores specifically, archived resources cannot be referenced by new sessions (existing sessions continue). Do not call `.archive()` on a production agent, environment, or memory store as cleanup — **always confirm with the user before archiving**.
</doc>

<doc path="shared/managed-agents-self-hosted-sandboxes.md">
# Managed Agents — Self-Hosted Sandboxes

With `config.type: "self_hosted"`, the **agent loop stays on Anthropic's orchestration layer** but **tool execution moves to infrastructure you control** — bash, file ops, and code run inside your container, so filesystem contents and network egress never leave your environment. Contrast with `config.type: "cloud"`, where Anthropic runs the container. Connectivity is **outbound-only**: your worker long-polls Anthropic's work queue; Anthropic never dials into your network.

## Flow

```
1. Create environment:      config: {type: "self_hosted"}        → env_...
2. Generate environment key (Console, on the environment page)   → sk-ant-oat01-...  as ANTHROPIC_ENVIRONMENT_KEY
3. Run a worker:            EnvironmentWorker.run()  or  ant beta:worker poll
4. Sessions reference       environment_id=env_... exactly as for cloud
```

## Create the environment

```python
client = anthropic.Anthropic()

environment = client.beta.environments.create(
    name="self-hosted", config={"type": "self_hosted"}
)
```

`{"type": "self_hosted"}` is the entire config — there are no pool, capacity, or networking sub-fields; you control those on your side.

## Run a worker — SDK (primary path)

`EnvironmentWorker` wraps the poll → dispatch → tool-execute loop. `.run()` is the always-on loop; `.run_one()` / `.runOne()` handles one work item (for webhook-driven wake).

**Python — always-on:**

```python
import asyncio
import os
from anthropic import AsyncAnthropic
from anthropic.lib.environments import EnvironmentWorker


async def main() -> None:
    environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
    environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
    async with AsyncAnthropic(auth_token=environment_key) as client:
        await EnvironmentWorker(
            client,
            environment_id=environment_id,
            environment_key=environment_key,
            workdir="/workspace",
        ).run()


asyncio.run(main())
```

**TypeScript — always-on:**

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";

const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
const client = new Anthropic({ authToken: environmentKey });
const ctrl = new AbortController();
process.once("SIGTERM", () => ctrl.abort());

await new EnvironmentWorker({
  client,
  environmentId,
  environmentKey,
  workdir: "/workspace",
  signal: ctrl.signal
}).run();
```

**Customizing tools.** `EnvironmentWorker` runs the built-in toolset by default. To add or replace tools, use `AgentToolContext(workdir=, client=, session_id=)` with `beta_agent_toolset(env)` / `betaAgentToolset(env)` and pass the resulting tools to the lower-level `tool_runner()`. Skills attached to the agent are downloaded into `{workdir}/skills/<name>/` before tool calls begin (`AgentToolContext` handles this when given `client` and `session_id`). Downloaded skill files are marked executable automatically by the CLI and SDK; if you implement skills download yourself, you set permissions.

> **Runtime deps:** the SDK helpers require `/bin/bash` at that exact path. The TypeScript SDK additionally requires `unzip`, `tar`, and Node.js 22+. These are resolved at fixed paths and do **not** respect `PATH` overrides.

## Run a worker — `ant` CLI (fixed tools)

The `ant` CLI ships a worker with the fixed built-in toolset (`bash`, `read`, `write`, `edit`, `glob`, `grep`). Install per `shared/anthropic-cli.md`, then:

```sh
export ANTHROPIC_ENVIRONMENT_KEY=sk-ant-oat01-...
ant beta:worker poll --environment-id env_... --workdir /workspace
```

- `--workdir` is the directory tools operate in (default `.`); tool calls are sandboxed to it.
- `--environment-key` overrides the env var.
- `--on-work <script>` runs your script per work item (e.g. to spin a fresh container per session — see Container orchestration below).
- `--unrestricted-paths`, `--max-idle` (default `60s`), `--log-format` — see `ant beta:worker poll --help`.
- Flags fall back to env vars (`ANTHROPIC_ENVIRONMENT_ID`, `ANTHROPIC_ENVIRONMENT_KEY`).
- Exits cleanly on SIGTERM/SIGINT after draining in-flight work.
- **Fixed toolset** — for custom tools, use the SDK worker above.

Inside an `--on-work` container, run `ant beta:worker run --workdir <dir>` as the entrypoint.

## Webhook-driven wake (instead of always-on)

Register a webhook for `session.status_run_started` (see `shared/managed-agents-webhooks.md`), verify the delivery, then drain one work item with `.run_one()`:

```python
import os
import anthropic
from anthropic.lib.environments import EnvironmentWorker

environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
client = anthropic.AsyncAnthropic(
    auth_token=environment_key,
)  # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env for webhooks.unwrap()


async def handle(raw: bytes, headers: dict[str, str]) -> dict:
    event = client.beta.webhooks.unwrap(raw.decode(), headers=headers)
    if event.data.type != "session.status_run_started":
        return {"status": "ignored"}
    await EnvironmentWorker(
        client,
        environment_id=environment_id,
        environment_key=environment_key,
        workdir="/workspace",
    ).run_one()
    return {"status": "ok"}
```

TypeScript: same shape with `client.beta.webhooks.unwrap(body, {headers})` and `new EnvironmentWorker({...}).runOne()`.

## Container orchestration (mid-level)

`EnvironmentWorker.run()` polls and executes tools in the same process. To run each session in its **own** container, use the mid-level poller in a thin orchestrator — Python `client.beta.environments.work.poller(environment_id=, environment_key=, drain=, block_ms=, reclaim_older_than_ms=, auto_stop=)`; TypeScript `new WorkPoller({client, environmentId, environmentKey, autoStop})` from `@anthropic-ai/sdk/helpers/beta/environments` — and, for each yielded `work` item, start a fresh container with these env vars injected, whose entrypoint runs `ant beta:worker run` or an `EnvironmentWorker(...).run_one()`. `block_ms` is 1–999 (or `None` for non-blocking); `reclaim_older_than_ms` re-claims items leased to a dead worker; `drain` stops once the queue is empty; `auto_stop` posts a stop signal after the iterator exits (set `False` when the launched container owns the stop call). **Go's poller has no `auto_stop` opt-out** — it calls `work.Stop` when the handler returns, so block in the handler until the session completes rather than detaching.

| Env var | Value |
|---|---|
| `ANTHROPIC_SESSION_ID` | `work.data.id` |
| `ANTHROPIC_WORK_ID` | `work.id` |
| `ANTHROPIC_ENVIRONMENT_ID` | `work.environment_id` |
| `ANTHROPIC_ENVIRONMENT_KEY` | pass through |
| `ANTHROPIC_BASE_URL` | pass through |

Skip items where `work.data.type != "session"`.

## Monitoring & control

These are **control-plane** calls — authenticate with `x-api-key` (not the environment key); `managed-agents-2026-04-01` beta header. **Call them from outside the worker host** — setting `ANTHROPIC_API_KEY` on the worker host exposes an organization-scoped credential to agent tool calls.

| SDK (`client.beta.environments.work.*`) | REST | CLI | Returns |
|---|---|---|---|
| `stats(environment_id)` | `GET /v1/environments/{id}/work/stats` | `ant beta:environments:work stats` | `{type:"work_queue_stats", depth, pending, oldest_queued_at, workers_polling}` |
| `stop(work_id, environment_id=)` | `POST /v1/environments/{id}/work/{work_id}/stop` | `ant beta:environments:work stop` | `work.state` |

## What changes vs `cloud`

| Concern | `cloud` | `self_hosted` |
|---|---|---|
| Container lifecycle, hardening, networking | Anthropic | **You** — run non-root, read-only rootfs, drop caps; egress is whatever your VPC/firewall allows |
| `file` / `github_repository` resource mounting | Anthropic mounts into the container | **You** — pass pointers via `sessions.create(metadata={...})` and have your orchestrator fetch/clone before dispatch |
| `memory_store` resources | Supported | **Not yet supported** |
| Built-in tools | Via `agent_toolset_20260401` | Supplied by your worker (`EnvironmentWorker` default / `beta_agent_toolset(env)` / `ant` CLI fixed set) |
| Skills download | Automatic | `EnvironmentWorker` / `AgentToolContext` fetch into `{workdir}/skills/` (needs `client` + `session_id`) |
| Claude Platform on AWS | Supported | **Not available** |
| SDK worker helpers | All SDKs | **Python, TypeScript, Go only** (`EnvironmentWorker` / poller not in Java, Ruby, PHP, or C#) — use one of those three or the `ant` CLI |

## Credentials

| Credential | Format | Scope |
|---|---|---|
| `ANTHROPIC_ENVIRONMENT_KEY` | `sk-ant-oat01-...` | One environment's work queue. Generate in Console ("Generate environment key"). Pass as `auth_token=` / `authToken` on the client **and** as `environment_key=` / `environmentKey` on `EnvironmentWorker`. Store in a secrets manager; rotate on exposure. |
| `ANTHROPIC_WEBHOOK_SIGNING_KEY` | `whsec_...` | Webhook signature verification (if using webhook-driven wake). The SDK reads this env var automatically for `client.beta.webhooks.unwrap()`. |

## Security — what you own

Container hardening; egress restriction (there is no default); `ANTHROPIC_ENVIRONMENT_KEY` custody and rotation; one workspace + environment per trust boundary when running untrusted code; least-privilege for the tool process; log retention and redaction. **Anthropic cannot**: fast-revoke a leaked environment key, verify your image or supply chain, sandbox tool execution inside your container, or enforce retention after tool output reaches your infrastructure. See the Self-Hosted Sandboxes Security page in `shared/live-sources.md` for the full checklist.
</doc>

<doc path="shared/managed-agents-tools.md">
# Managed Agents — Tools & Skills

## Tools

### Server tools vs client tools

| Type | Who runs it | How it works |
|---|---|---|
| **Prebuilt Claude Agent tools** (`agent_toolset_20260401`) | Anthropic, on the session's container (for `cloud` envs; for `self_hosted`, **your** worker supplies and runs them — see `shared/managed-agents-self-hosted-sandboxes.md`) | File ops, bash, web search, etc. Enable all at once or configure individually with `enabled: true/false`. |
| **MCP tools** (`mcp_toolset`) | Anthropic's orchestration layer | Capabilities exposed by connected MCP servers. Grant access per-server via the toolset. |
| **Custom tools** | **You** — your application handles the call and returns results | Agent emits a `agent.custom_tool_use` event, session goes `idle`, you send back a `user.custom_tool_result` event. |

**Recommendation:** Enable all prebuilt tools via `agent_toolset_20260401`, then disable individually as needed.

**Versioning:** The toolset is a versioned, static resource. When underlying tools change, a new toolset version is created (hence `_20260401`) so you always know exactly what you're getting.

### Agent Toolset

The `agent_toolset_20260401` provides these built-in tools:

| Tool                   | Description                              |
| ---------------------- | ---------------------------------------- |
| `bash` | Execute bash commands in a shell session |
| `read` | Read a file from the local filesystem, including text, images, PDFs, and Jupyter notebooks |
| `write` | Write a file to the local filesystem |
| `edit` | Perform string replacement in a file |
| `glob` | Fast file pattern matching using glob patterns |
| `grep` | Text search using regex patterns |
| `web_fetch` | Fetch content from a URL |
| `web_search` | Search the web for information |

Enable the full toolset:

```json
{
  "tools": [
    { "type": "agent_toolset_20260401" }
  ]
}
```

### Per-Tool Configuration

Override defaults for individual tools. This example enables everything except bash:

```json
{
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "default_config": { "enabled": true },
      "configs": [
        { "name": "bash", "enabled": false }
      ]
    }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `type` | ✅ | `"agent_toolset_20260401"` |
| `default_config` | ❌ | Applied to all tools. `{ "enabled": bool, "permission_policy": {...} }` |
| `configs` | ❌ | Per-tool overrides: `[{ "name": "...", "enabled": bool, "permission_policy": {...} }]` |

### Permission Policies

Control when server-executed tools (agent toolset + MCP) run automatically vs wait for approval. Does not apply to custom tools.

| Policy | Behavior |
|---|---|
| `always_allow` | Tool executes automatically (default) |
| `always_ask` | Session emits `session.status_idle` and pauses until you send a `tool_confirmation` event |

```json
{
  "type": "agent_toolset_20260401",
  "default_config": {
    "enabled": true,
    "permission_policy": { "type": "always_allow" }
  },
  "configs": [
    { "name": "bash", "permission_policy": { "type": "always_ask" } }
  ]
}
```

**Responding to `always_ask`:** Send a `user.tool_confirmation` event with `tool_use_id` from the triggering `agent_tool_use`/`mcp_tool_use` event:

```json
{ "type": "tool_confirmation", "tool_use_id": "sevt_abc123", "result": "allow" }
{ "type": "tool_confirmation", "tool_use_id": "sevt_def456", "result": "deny", "message": "Read .env.example instead" }
```

The optional `message` on a deny is delivered to the agent so it can adjust its approach.

To enable only specific tools, flip the default off and opt-in per tool:

```json
{
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "default_config": { "enabled": false },
      "configs": [
        { "name": "bash", "enabled": true },
        { "name": "read", "enabled": true }
      ]
    }
  ]
}
```

### Custom Tools (Client-Side)

Custom tools are executed by **your application**, not Anthropic. The flow:

1. Agent decides to use the tool → session emits a `agent.custom_tool_use` event with inputs
2. Session goes `idle` waiting for you
3. Your application executes the tool
4. You send back a `user.custom_tool_result` event with the output
5. Session resumes `running`

No permission policy needed — you're the one executing.

```json
{
  "tools": [
    {
      "type": "custom",
      "name": "get_weather",
      "description": "Fetch current weather for a city.",
      "input_schema": {
        "type": "object",
        "properties": {
          "city": { "type": "string", "description": "City name" }
        },
        "required": ["city"]
      }
    }
  ]
}
```

### MCP Servers

MCP (Model Context Protocol) servers expose standardized third-party capabilities (e.g. Asana, GitHub, Linear). **Configuration is split across agent and vault:**

1. **Agent creation** declares which servers to connect to (`type`, `name`, `url` — no auth). The agent's `mcp_servers` array has no auth field.
2. **Vault** stores the OAuth credentials. Attach via `vault_ids` on session create.

This keeps secrets out of reusable agent definitions. Each vault credential is tied to one MCP server URL; Anthropic matches credentials to servers by URL.

**Agent side — declare servers (no auth):**

| Field | Required | Description |
|---|---|---|
| `type` | ✅ | `"url"` |
| `name` | ✅ | Unique name — referenced by `mcp_toolset.mcp_server_name` |
| `url` | ✅ | The MCP server's endpoint URL (Streamable HTTP transport) |

```json
{
  "mcp_servers": [
    { "type": "url", "name": "linear", "url": "https://mcp.linear.app/mcp" }
  ],
  "tools": [
    { "type": "mcp_toolset", "mcp_server_name": "linear" }
  ]
}
```

**Session side — attach vault:**

```json
{
  "agent": "agent_abc123",
  "environment_id": "env_abc123",
  "vault_ids": ["vlt_abc123"]
}
```

> 💡 **Per-tool enablement (empirical):** `mcp_toolset` has been observed accepting `default_config: {enabled: false}` + `configs: [{name, enabled: true}]` for an allowlist pattern. The API ref shows only the minimal `{type, mcp_server_name}` form.

> 💡 **Changing tools/MCP servers on a running session:** `sessions.update()` can replace `agent.tools`, `agent.mcp_servers`, and `vault_ids` while the session is `idle` — a session-local override that doesn't touch the agent object. See `shared/managed-agents-core.md` → Updating the agent configuration mid-session.

**Large MCP tool outputs.** If an MCP tool returns more than **100K tokens**, the output is automatically offloaded to a file in the sandbox — the agent receives a truncated preview plus the file path and can `read` the full content. No configuration required.

**Invalid vault credentials don't block session creation.** If a vault credential is invalid for a declared MCP server, the session still creates successfully; a `session.error` event describes the MCP auth failure, and auth retries on the next `session.status_idle` → `session.status_running` transition.

> ⚠️ **MCP auth tokens ≠ REST API tokens.** Hosted MCP servers (`mcp.notion.com`, `mcp.linear.app`, etc.) typically require **OAuth bearer tokens**, not the service's native API keys. A Notion `ntn_` integration token authenticates against Notion's REST API but will **not** work as a vault credential for the Notion MCP server. These are different auth systems.

### Vaults — the MCP credential store

**Vaults** store OAuth credentials (access token + refresh token) that Anthropic auto-refreshes on your behalf via standard OAuth 2.0 `refresh_token` grant. This is the only way to authenticate MCP servers in the launch SDK.

#### Credentials and the sandbox

Vaults store credentials; those credentials **never enter the sandbox**. This is a deliberate security boundary — code running in the sandbox (including anything the agent writes) cannot read or exfiltrate a vaulted credential, even under prompt injection. Instead, credentials are injected by Anthropic-side proxies **after** a request leaves the sandbox:

- **MCP tool calls** are routed through an Anthropic-side proxy that fetches the credential from the vault and adds it to the outbound request.
- **Git operations on attached GitHub repositories** (`git pull`, `git push`, GitHub REST calls) are routed through a git proxy that injects the `github_repository` resource's `authorization_token` the same way.

**Not yet supported:** running other authenticated CLIs (e.g. `aws`, `gcloud`, `stripe`) directly inside the sandbox. There is currently no way to set container environment variables or expose vault credentials to arbitrary processes. If you need one of these today:

- **Prefer an MCP server** for that service if one exists — it gets the same vault-backed injection.
- **Otherwise, register a custom tool:** the agent emits `agent.custom_tool_use`, your orchestrator (which already holds the credential) executes the call and returns `user.custom_tool_result` over the same authenticated event stream. No public endpoint is exposed; the sandbox never sees the secret. See `shared/managed-agents-client-patterns.md` → Pattern 9.

**Do not put API keys in the system prompt or user messages as a workaround** — they persist in the session's event history.

> Formerly known internally as TATs (Tool/Tenant Access Tokens).

**Flow:**

1. Create a vault (`client.beta.vaults.create(...)`) — one per tenant/user, or one shared, depending on your model
2. Add MCP credentials to it (`client.beta.vaults.credentials.create(...)`) — each credential is tied to one MCP server URL
3. Reference the vault on session create via `vault_ids: ["vlt_..."]`
4. Anthropic auto-refreshes tokens before they expire; the agent uses the current access token when calling MCP tools

**Credential shape**:

```json
{
  "display_name": "Notion (workspace-foo)",
  "auth": {
    "type": "mcp_oauth",
    "mcp_server_url": "https://mcp.notion.com/mcp",
    "access_token": "<current access token>",
    "expires_at": "2026-04-02T14:00:00Z",
    "refresh": {
      "refresh_token": "<refresh token>",
      "client_id": "<your OAuth client_id>",
      "token_endpoint": "https://api.notion.com/v1/oauth/token",
      "token_endpoint_auth": { "type": "none" }
    }
  }
}
```

The `refresh` block is what enables auto-refresh — `token_endpoint` is where Anthropic posts the `refresh_token` grant. `token_endpoint_auth` is a discriminated union:

| `type` | Shape | Use when |
|---|---|---|
| `"none"` | `{type: "none"}` | Public OAuth client (no secret) |
| `"client_secret_basic"` | `{type: "client_secret_basic", client_secret: "..."}` | Confidential client, secret via HTTP Basic auth |
| `"client_secret_post"` | `{type: "client_secret_post", client_secret: "..."}` | Confidential client, secret in request body |

Omit `refresh` entirely if you only have an access token with no refresh capability — it'll work until it expires, then the agent loses access.

> 💡 **Getting an OAuth token.** How you obtain the initial access and refresh tokens depends on the MCP server — consult its documentation. Once you have them, store them in a vault credential using the shape above; Anthropic auto-refreshes via the `refresh.token_endpoint` from there.

**Scoping:** Vaults are workspace-scoped. Anyone with developer+ role in the API workspace can create, read (metadata only — secrets are write-only), and attach vaults. `vault_ids` can be set at session **create** time but not via session update (the SDK docstring says "Not yet supported; requests setting this field are rejected").

---

## Skills

Skills are reusable, filesystem-based resources that provide your agent with domain-specific expertise: workflows, context, and best practices that transform general-purpose agents into specialists. Unlike prompts (conversation-level instructions for one-off tasks), skills load on-demand and eliminate the need to repeatedly provide the same guidance across multiple conversations.

Two types — both work the same way; the agent automatically uses them when relevant to the task at hand:

| Type | What it is |
|---|---|
| **Pre-built Anthropic skills** | Common document tasks (PowerPoint, Excel, Word, PDF). Reference by name (e.g. `xlsx`). |
| **Custom skills** | Skills you've created in your organization via the Skills API. Reference by `skill_id` + optional `version`. |

**Max 20 skills per agent.** Agent creation uses `managed-agents-2026-04-01`; the separate Skills API (for managing custom skill definitions) uses `skills-2025-10-02`.

### Enabling skills on a session

Skills are attached to the **agent** definition via `agents.create()`:

```ts
const agent = await client.beta.agents.create(
  {
    name: "Financial Agent",
    model: "claude-opus-4-8",
    system: "You are a financial analysis agent.",
    skills: [
      { type: "anthropic", skill_id: "xlsx" },
      { type: "custom", skill_id: "skill_abc123", version: "latest" },
    ],
  }
);
```

Python:

```python
agent = client.beta.agents.create(
    name="Financial Agent",
    model="claude-opus-4-8",
    system="You are a financial analysis agent.",
    skills=[
        {"type": "anthropic", "skill_id": "xlsx"},
        {"type": "custom", "skill_id": "skill_abc123", "version": "latest"},
    ]
)
```

**Skill reference fields:**

| Field | Anthropic skill | Custom skill |
|---|---|---|
| `type` | `"anthropic"` | `"custom"` |
| `skill_id` | Skill name (e.g. `"xlsx"`, `"docx"`, `"pptx"`, `"pdf"`) | Skill ID from Skills API (e.g. `"skill_abc123"`) |
| `version` | — | `"latest"` or a specific version number |

### Skills API

| Operation             | Method   | Path                                            |
| --------------------- | -------- | ----------------------------------------------- |
| Create Skill          | `POST`   | `/v1/skills`                                    |
| List Skills           | `GET`    | `/v1/skills`                                    |
| Get Skill             | `GET`    | `/v1/skills/{id}`                               |
| Delete Skill          | `DELETE` | `/v1/skills/{id}`                               |
| Create Version        | `POST`   | `/v1/skills/{id}/versions`                      |
| List Versions         | `GET`    | `/v1/skills/{id}/versions`                      |
| Get Version           | `GET`    | `/v1/skills/{id}/versions/{version}`            |
| Delete Version        | `DELETE` | `/v1/skills/{id}/versions/{version}`            |
</doc>

<doc path="shared/managed-agents-webhooks.md">
# Managed Agents — Webhooks

Anthropic can POST to your HTTPS endpoint when a Managed Agents resource changes state — an alternative to holding an SSE stream or polling. Payloads are **thin** (event type + resource IDs only); on receipt, fetch the resource for current state. Every delivery is HMAC-signed.

> **Direction matters.** This page covers *Anthropic → you* notifications about session/vault state. It does **not** cover *third-party → you* webhooks that *trigger* a session (e.g. a GitHub push handler that calls `sessions.create()`) — that's ordinary application code on your side with no Anthropic-specific wire format.

---

## Register an endpoint (Console only)

Console → **Manage → Webhooks**. There is no programmatic endpoint-management API yet. Secret rotation is supported from the same page.

| Field | Constraint |
|---|---|
| URL | HTTPS on port 443, publicly resolvable hostname |
| Event types | Subscribe per `data.type` — you only receive subscribed types (plus test events) |
| Signing secret | `whsec_`-prefixed, 32 bytes, **shown once at creation** — store it |

---

## Verify the signature

Every delivery is HMAC-signed. **Use the SDK's `client.beta.webhooks.unwrap()`** — it verifies the signature, rejects payloads more than ~5 minutes old, and returns the parsed event. It reads the `whsec_` secret from `ANTHROPIC_WEBHOOK_SIGNING_KEY`.

```python
import anthropic
from flask import Flask, request

client = anthropic.Anthropic()  # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        event = client.beta.webhooks.unwrap(
            request.get_data(as_text=True),
            headers=dict(request.headers),
        )
    except Exception:
        return "invalid signature", 400

    if event.id in seen_event_ids:  # dedupe retries — id is per-event, not per-delivery
        return "", 204
    seen_event_ids.add(event.id)

    match event.data.type:
        case "session.status_idled":
            session = client.beta.sessions.retrieve(event.data.id)
            notify_user(session)
        case "vault_credential.refresh_failed":
            alert_oncall(event.data.id)

    return "", 204
```

Pass the **raw request body** to `unwrap()` — frameworks that re-serialize JSON (Express `.json()`, Flask `.get_json()`) change the bytes and break the MAC. For other languages, look up the `beta.webhooks.unwrap` binding in the SDK repo (`shared/live-sources.md`); don't hand-roll verification.

---

## Payload envelope

```json
{
  "type": "event",
  "id": "event_01ABC...",
  "created_at": "2026-03-18T14:05:22Z",
  "data": {
    "type": "session.status_idled",
    "id": "session_01XYZ...",
    "organization_id": "8a3d2f1e-...",
    "workspace_id": "c7b0e4d9-..."
  }
}
```

Switch on `data.type`, fetch the resource by `data.id`, return any **2xx** to acknowledge. `created_at` is when the *state transition* happened, not when the webhook fired.

---

## Supported `data.type` values

| `data.type` | Fires when |
|---|---|
| `session.status_scheduled` | Session created and ready to accept events |
| `session.status_run_started` | Agent execution kicked off (every transition to `running`) |
| `session.status_idled` | Agent awaiting input (tool approval, custom tool result, or next message) |
| `session.status_terminated` | Session hit a terminal error |
| `session.thread_created` | Multiagent: coordinator opened a new subagent thread |
| `session.thread_idled` | Multiagent: a subagent thread is waiting for input |
| `session.outcome_evaluation_ended` | Outcome grader finished one iteration |
| `vault.archived` | Vault was archived |
| `vault.created` | Vault was created |
| `vault.deleted` | Vault was deleted |
| `vault_credential.archived` | Vault credential was archived |
| `vault_credential.created` | Vault credential was created |
| `vault_credential.deleted` | Vault credential was deleted |
| `vault_credential.refresh_failed` | MCP OAuth vault credential failed to refresh |

> These are **webhook** `data.type` values — a separate namespace from SSE event types (`session.status_idle`, `span.outcome_evaluation_end`, etc. in `shared/managed-agents-events.md`). Don't reuse SSE constants in webhook handlers.

---

## Delivery behavior & pitfalls

- **No ordering guarantee.** `session.status_idled` may arrive before `session.outcome_evaluation_ended` even if the evaluation finished first. Sort by envelope `created_at` if order matters.
- **Retries carry the same `event.id`.** At least one retry on non-2xx. Dedupe on `event.id`.
- **3xx is failure.** Redirects are not followed — update the URL in Console if your endpoint moves.
- **Auto-disable** after ~20 consecutive failed deliveries, or immediately if the hostname resolves to a private IP or returns a redirect. Re-enable manually in Console.
- **Thin payload is intentional.** Don't expect `stop_reason`, `outcome_evaluations`, credential secrets, etc. on the webhook body — fetch the resource.
</doc>

<doc path="shared/model-migration.md">
# Model Migration Guide

> **If you arrived via `/claude-api migrate`:** this is the right file. Execute the steps below in order — do not summarize them back to the user. Start with Step 0 (confirm scope) before touching any file.

How to move existing code to newer Claude models. Covers breaking changes, deprecated parameters, and drop-in replacements for retired models.

For the latest, authoritative version (with code samples in every supported language), WebFetch the **Migration Guide** URL from `shared/live-sources.md`. Use this file for the consolidated, skill-resident reference; fall back to the live docs whenever a model launch or breaking change may have shifted the picture.

**This file is large.** Use the section names below to jump (or `Grep` this file for the heading text). Read Step 0 and Step 1 first — they apply to every migration. Then read only the per-target section for the model you are migrating to.

| Section | When you need it |
|---|---|
| Step 0: Confirm the migration scope | Always — before any edits |
| Step 1: Classify each file | Always — decides whether to swap, add-alongside, or skip |
| Per-SDK Syntax Reference | Translate the Python examples in this guide to TypeScript / Go / Ruby / Java / C# / PHP |
| Destination Models / Retired Model Replacements | Picking a target model |
| Breaking Changes by Source Model | Migrating to Opus 4.6 / Sonnet 4.6 |
| Migrating to Opus 4.7 | Migrating to Opus 4.7 (breaking changes, silent defaults, behavioral shifts) |
| Opus 4.7 Migration Checklist | The required vs optional items for 4.7, tagged `[BLOCKS]` / `[TUNE]` |
| Migrating to Opus 4.8 | Migrating to Opus 4.8 (no new breaking changes; mid-session system prompts; behavioral re-tuning) |
| Opus 4.8 Migration Checklist | The required vs optional items for 4.8, tagged `[BLOCKS]` / `[TUNE]` |
| Verify the Migration | After edits — runtime spot-check |

**TL;DR:** Change the model ID string. If you were using `budget_tokens`, switch to `thinking: {type: "adaptive"}`. If you were using assistant prefills, they 400 on both Opus 4.6 and Sonnet 4.6 — switch to one of the prefill replacements (most often `output_config.format`; see the table in Breaking Changes by Source Model). If you're moving from Sonnet 4.5 to Sonnet 4.6, set `effort` explicitly — 4.6 defaults to `high`. Remove the `effort-2025-11-24` and `fine-grained-tool-streaming-2025-05-14` beta headers (GA on 4.6); remove `interleaved-thinking-2025-05-14` once you're on adaptive thinking (keep it only while using the transitional `budget_tokens` escape hatch). Then drop back from `client.beta.messages.create` to `client.messages.create`. Dial back any aggressive "CRITICAL: YOU MUST" tool instructions; 4.6 follows the system prompt much more closely.

---

## Step 0: Confirm the migration scope

**Before any Write, Edit, or MultiEdit call, confirm the scope.** If the user's request does not explicitly name a single file, a specific directory, or an explicit file list, **ask first — do not start editing**. This is non-negotiable: even imperative-sounding requests like "migrate my codebase", "move my project to X", "upgrade to Sonnet 4.6", or bare "migrate to Opus 4.7" leave the scope ambiguous and require a clarifying question. Phrases like "my project", "my code", "my codebase", "the whole thing", "everywhere", or "across the repo" are **ambiguous, not directive** — they tell you *what* to do but not *where*. Ask before doing.

Offer the common scopes explicitly and wait for the answer before touching any file:

1. The entire working directory
2. A specific subdirectory (e.g. `src/`, `app/`, `services/billing/`)
3. A specific file or a list of files

Surface this as a single clarifying question so the user can answer in one turn. **Proceed without asking only when the scope is already unambiguous** — the user named an exact file ("migrate `extract.py` to Sonnet 4.6"), pointed at a specific directory ("migrate everything under `services/billing/` to Opus 4.6"), listed specific files ("update `a.py` and `b.py`"), or already answered the scope question in an earlier turn. If you can answer the question "which files is this change going to touch?" with a precise list from the prompt alone, proceed. If not, ask.

**Worked example.** If the user says *"Move my project to Opus 4.6. I want adaptive thinking everywhere it makes sense."* you do not know whether "my project" means the whole working directory, just `src/`, just the production code, or something else — the `everywhere` makes the intent clear (update every call site *within scope*) but the scope itself is still not defined. Do not start editing. Respond with:

> Before I start editing, can you confirm the scope? I can migrate:
> 1. Every `.py` file in the working directory
> 2. Just the files under `src/` (production code)
> 3. A specific subdirectory or list of files you name
>
> Which one?

Then wait for the answer. The same applies to *"Migrate to Opus 4.7"* and bare *"Help me upgrade to Sonnet 4.6"* — ask before editing.

**Sizing the scope question (large repos).** Before asking, get a per-directory count so the user can pick concretely:

```sh
rg -l "<old-model-id>" --type-not md | cut -d/ -f1 | sort | uniq -c | sort -rn
```

Present the breakdown in your scope question (e.g. *"Found 217 references across 3 directories: api/ (130), api-go/ (62), routing/ (25). Which to migrate?"*). Also confirm `git status` is clean before surveying — unexpected modifications mean a concurrent process; stop and investigate before proceeding.

---

## Step 1: Classify each file

Not every file that contains the old model ID is a **caller** of the API. Before editing, classify each file into one of these buckets — the right action differs:

| # | Bucket | What it looks like | Action |
|---|---|---|---|
| 1 | **Calls the API/SDK** | `client.messages.create(model=…)`, `anthropic.Anthropic()`, request payloads | Swap the model ID **and** apply the breaking-change checklist for the target version (below). |
| 2 | **Defines or serves the model** | Model registries, OpenAPI specs, routing/queue configs, model-policy enums, generated catalogs | The old entry **stays** (the model is still served). Ask whether to (a) add the new model alongside, (b) leave alone, or (c) retire the old model — never blind-replace. **If you can't ask, default to (a): add the new model alongside and flag it** — replacing would de-register a model that's still in production. |
| 3 | **References the ID as an opaque string** | UI fallback constants, capability-gate substring checks, generic test fixtures, label parsers, env defaults | Usually swap the string and verify any parser/regex/substring match handles the new ID — but check the sub-cases below first. |
| 4 | **Suffixed variant ID** | `claude-<model>-<suffix>` like `-fast`, `-1024k`, `-200k`, `[1m]`, dated snapshots | These are deployment/routing identifiers, not the public model ID. **Do not assume a new-model equivalent exists.** Verify in the registry first; if absent, leave the string alone and flag it. |

**Bucket 3 sub-cases — before swapping a string reference, check:**

- **Capability gate** (e.g. `if 'opus-4-6' in model_id:` enables a feature) → **add the new ID alongside**, don't replace. The old model is still served and still has the capability, so replacing would silently disable the feature for any old-model traffic that still flows through. If you know no old-model traffic will hit this gate (single-caller codebase fully migrating), replacing is fine; if unsure, add alongside.
- **Registry-assert test** (e.g. `assert "claude-X" in supported_models`, `test_X_has_N_clusters`) → **add an assertion for the new model alongside; keep the old one.** The old model is still served, so its assertion stays valid — but the registry should also include the new model, so assert that too. Heuristic: if the test references multiple model versions in a list, it's a registry test; if one model in a struct compared only to itself, it's a generic fixture.
- **Frozen / generated snapshot** → **regenerate**, don't hand-edit.
- **Coupled to a definer** (e.g. an integration test that passes model authorization via a shared `conftest` seed list, or asserts on a billing-tier / rate-limit-group enum or a generated SKU/pricing catalog) → **verify the definer has a new-model entry first.** If not, add a seed entry (reusing the nearest existing tier as a placeholder); if you can't confidently do that, ask the user how to populate the definer. **Do not skip the test.** Swapping without populating the definer will make the test fail at runtime.

When migrating tests specifically: breaking parameters (`temperature`, `top_p`, `budget_tokens`) are usually absent — test fixtures rarely set sampling params on placeholder models. The breaking-change scan is still required, but expect mostly clean results.

**Find intentionally-flagged sync points first.** Many codebases tag spots that must change at every model launch with comment markers like `MODEL LAUNCH`, `KEEP IN SYNC`, `@model-update`, or similar. Grep for whatever convention the repo uses *before* the broad model-ID grep — those markers point at the load-bearing changes.

---

## Per-SDK Syntax Reference

Code examples in this guide are Python. **The same fields exist in every official Anthropic SDK** — Stainless generates all 7 from the same OpenAPI spec, so JSON field names map 1:1 with only case-convention differences. Use the rows below to translate the Python examples to the SDK you are migrating.

> **Verify type and method names against the SDK source before writing them into customer code.** WebFetch the relevant repository from the SDK source-code table in `shared/live-sources.md` (one row per SDK) and confirm the exact symbol — particularly for typed SDKs (Go, Java, C#) where union/builder names can differ from the JSON shape. Do not guess type names that aren't in the table below or in `<lang>/claude-api/README.md`.


### `thinking` — `budget_tokens` → adaptive

| SDK | Before | After |
|---|---|---|
| Python | `thinking={"type": "enabled", "budget_tokens": N}` | `thinking={"type": "adaptive"}` |
| TypeScript | `thinking: { type: 'enabled', budget_tokens: N }` | `thinking: { type: 'adaptive' }` |
| Go | `Thinking: anthropic.ThinkingConfigParamOfEnabled(N)` | `Thinking: anthropic.ThinkingConfigParamUnion{OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{}}` |
| Ruby | `thinking: { type: "enabled", budget_tokens: N }` | `thinking: { type: "adaptive" }` |
| Java | `.thinking(ThinkingConfigEnabled.builder().budgetTokens(N).build())` | `.thinking(ThinkingConfigAdaptive.builder().build())` |
| C# | `Thinking = new ThinkingConfigEnabled { BudgetTokens = N }` | `Thinking = new ThinkingConfigAdaptive()` |
| PHP | `thinking: ['type' => 'enabled', 'budget_tokens' => N]` | `thinking: ['type' => 'adaptive']` |

### Sampling parameters — `temperature` / `top_p` / `top_k`

(Remove the field entirely on Opus 4.7; on Claude 4.x keep at most one of `temperature` or `top_p`.)

| SDK | Field(s) to remove |
|---|---|
| Python | `temperature=…`, `top_p=…`, `top_k=…` |
| TypeScript | `temperature: …`, `top_p: …`, `top_k: …` |
| Go | `Temperature: anthropic.Float(…)`, `TopP: anthropic.Float(…)`, `TopK: anthropic.Int(…)` |
| Ruby | `temperature: …`, `top_p: …`, `top_k: …` |
| Java | `.temperature(…)`, `.topP(…)`, `.topK(…)` |
| C# | `Temperature = …`, `TopP = …`, `TopK = …` |
| PHP | `temperature: …`, `topP: …`, `topK: …` |

### Prefill replacement — structured outputs via `output_config.format`

| SDK | Remove (last assistant turn) | Add |
|---|---|---|
| Python | `{"role": "assistant", "content": "…"}` | `output_config={"format": {"type": "json_schema", "schema": SCHEMA}}` |
| TypeScript | `{ role: 'assistant', content: '…' }` | `output_config: { format: { type: 'json_schema', schema: SCHEMA } }` |
| Go | trailing `anthropic.MessageParam{Role: "assistant", …}` | `OutputConfig: anthropic.OutputConfigParam{Format: anthropic.JSONOutputFormatParam{…}}` |
| Ruby | `{ role: "assistant", content: "…" }` | `output_config: { format: { type: "json_schema", schema: SCHEMA } }` |
| Java | trailing `Message.builder().role(ASSISTANT)…` | `.outputConfig(OutputConfig.builder().format(JsonOutputFormat.builder()…build()).build())` |
| C# | trailing `new Message { Role = "assistant", … }` | `OutputConfig = new OutputConfig { Format = new JsonOutputFormat { … } }` |
| PHP | trailing `['role' => 'assistant', 'content' => '…']` | `outputConfig: ['format' => ['type' => 'json_schema', 'schema' => $SCHEMA]]` |

### `thinking.display` — opt back into summarized reasoning (Opus 4.7)

| SDK | Add |
|---|---|
| Python | `thinking={"type": "adaptive", "display": "summarized"}` |
| TypeScript | `thinking: { type: 'adaptive', display: 'summarized' }` |
| Go | `Thinking: anthropic.ThinkingConfigParamUnion{OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized}}` |
| Ruby | `thinking: { type: "adaptive", display: "summarized" }` (or `display_:` when constructing the model class directly) |
| Java | `.thinking(ThinkingConfigAdaptive.builder().display(ThinkingConfigAdaptive.Display.SUMMARIZED).build())` |
| C# | `Thinking = new ThinkingConfigAdaptive { Display = Display.Summarized }` |
| PHP | `thinking: ['type' => 'adaptive', 'display' => 'summarized']` |

For any field not in these tables, the JSON key in the Python example translates directly: `snake_case` for Python/TypeScript/Ruby, `camelCase` named args for PHP, `PascalCase` struct fields for Go/C#, `camelCase` builder methods for Java.

---

## Explain every change you make

Migration edits often look arbitrary to a user who hasn't read the release notes — a removed `temperature`, a deleted prefill, a rewritten system-prompt sentence. **For each edit, tell the user what you changed and why**, tied to the specific API or behavioral change that motivates it. Do this in your summary as you work, not just at the end.

Be especially explicit about **system-prompt edits**. Users are rightly protective of their prompts, and prompt-tuning changes are judgment calls (not hard API requirements). For any prompt edit:

- Quote the before and after text.
- State the behavioral shift that motivates it (e.g. *"Opus 4.7 calibrates response length to task complexity, so I added an explicit length instruction"*, or *"4.6 follows instructions more literally, so 'CRITICAL: YOU MUST use the search tool' will now overtrigger — softened to 'Use the search tool when…'"*).
- Make clear which prompt edits are **optional tuning** (tone, length, subagent guidance) versus which code edits are **required to avoid a 400** (sampling params, `budget_tokens`, prefills). Never present an optional prompt change as mandatory.

If you're applying several prompt-tuning edits at once, offer them as a short list the user can accept or decline item-by-item rather than silently rewriting their system prompt.

---

## Before You Migrate

1. **Confirm the target model ID.** Use only the exact strings from `shared/models.md` — do not append date suffixes to aliases (`claude-opus-4-6`, not `claude-opus-4-6-20251101`). Guessing an ID will 404.
2. **Check which features your code uses** with this checklist:
   - `thinking: {type: "enabled", budget_tokens: N}` → migrate to adaptive thinking on Opus 4.6 / Sonnet 4.6 (still functional but deprecated)
   - Assistant-turn prefills (`messages` ending with `role: "assistant"`) → must change on Opus 4.6 / Sonnet 4.6 (returns 400)
   - `output_format` parameter on `messages.create()` → must change on all models (deprecated API-wide)
   - `max_tokens > ~16000` → must stream on any model (above ~16K risks SDK HTTP timeouts). When streaming, Sonnet 4.6 / Haiku 4.5 cap at 64K and Opus 4.6 caps at 128K
   - Beta headers `effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14`, `interleaved-thinking-2025-05-14` → GA on 4.6, remove them and switch from `client.beta.messages.create` to `client.messages.create`
   - Moving Sonnet 4.5 → Sonnet 4.6 with no `effort` set → 4.6 defaults to `high`, which may change your latency/cost profile
   - System prompts with `CRITICAL`, `MUST`, `If in doubt, use X` language → likely to overtrigger on 4.6 (see Prompt-Behavior Changes)
   - Coming from 3.x / 4.0 / 4.1: also check sampling params (`temperature` + `top_p`), tool versions (`text_editor_20250728`), `refusal` + `model_context_window_exceeded` stop reasons, trailing-newline tool-param handling
3. **Test on a single request first.** Run one call against the new model, inspect the response, then roll out.

---

## Destination Models (recommended targets)

| If you're on…                         | Migrate to         | Why                                               |
| ------------------------------------- | ------------------ | ------------------------------------------------- |
| Opus 4.7                              | `claude-opus-4-8`  | Most capable model; same API surface as 4.7 (no new breaking changes) — mostly prompt re-tuning; see Migrating to Opus 4.8 |
| Opus 4.6                              | `claude-opus-4-8`  | Apply the Opus 4.7 breaking changes, then the 4.8 re-tuning |
| Opus 4.0 / 4.1 / 4.5 / Opus 3         | `claude-opus-4-8`  | Apply 4.6 → 4.7 → 4.8 in order (adaptive thinking, drop sampling params, then re-tune) |
| Sonnet 4.0 / 4.5 / 3.7 / 3.5          | `claude-sonnet-4-6`| Best speed / intelligence balance; adaptive thinking; 64K output |
| Haiku 3 / 3.5                         | `claude-haiku-4-5` | Fastest and most cost-effective                   |

Default to the latest Opus for the caller's tier unless they explicitly chose otherwise. The Opus migrations layer: if you're on Opus 4.6 or older, apply each version's section in order up to your target (e.g. 4.5 → 4.8 means the 4.6, 4.7, and 4.8 sections in sequence). A 4.7 → 4.8 move has no new breaking changes — see Migrating to Opus 4.8 below.

---

## Retired Model Replacements

These models return 404 — update immediately:

| Retired model                 | Retired       | Drop-in replacement  |
| ----------------------------- | ------------- | -------------------- |
| `claude-3-7-sonnet-20250219`  | Feb 19, 2026  | `claude-sonnet-4-6`  |
| `claude-3-5-haiku-20241022`   | Feb 19, 2026  | `claude-haiku-4-5`   |
| `claude-3-opus-20240229`      | Jan 5, 2026   | `claude-opus-4-8`    |
| `claude-3-5-sonnet-20241022`  | Oct 28, 2025  | `claude-sonnet-4-6`  |
| `claude-3-5-sonnet-20240620`  | Oct 28, 2025  | `claude-sonnet-4-6`  |
| `claude-3-sonnet-20240229`    | Jul 21, 2025  | `claude-sonnet-4-6`  |
| `claude-2.1`, `claude-2.0`    | Jul 21, 2025  | `claude-sonnet-4-6`  |

## Deprecated Models (retiring soon)

| Model                         | Retires       | Replacement          |
| ----------------------------- | ------------- | -------------------- |
| `claude-3-haiku-20240307`     | Apr 19, 2026  | `claude-haiku-4-5`   |
| `claude-opus-4-20250514`      | June 15, 2026 | `claude-opus-4-8`    |
| `claude-sonnet-4-20250514`    | June 15, 2026 | `claude-sonnet-4-6`  |

---

## Breaking Changes by Source Model

### Migrating from Sonnet 4.5 to Sonnet 4.6 (effort default change)

Sonnet 4.5 had no `effort` parameter; Sonnet 4.6 defaults to `high`. If you just switch the model string and do nothing else, you may see noticeably higher latency and token usage. Set `effort` explicitly.

**Recommended starting points:**

| Workload                                          | Start at       | Notes                                                                                                    |
| ------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------- |
| Chat, classification, content generation          | `low`          | With `thinking: {"type": "disabled"}` you'll see similar or better performance vs. Sonnet 4.5 no-thinking |
| Most applications (balanced)                      | `medium`       | The default sweet spot for quality vs. cost                                                              |
| Agentic coding, tool-heavy workflows              | `medium`       | Pair with adaptive thinking and a generous `max_tokens` (up to 64K with streaming — Sonnet 4.6's ceiling) |
| Autonomous multi-step agents, long-horizon loops  | `high`         | Scale down to `medium` if latency/tokens become a concern                                                 |
| Computer-use agents                               | `high` + adaptive | Sonnet 4.6's best computer-use accuracy is on adaptive + high                                          |

For non-thinking chat workloads specifically:

```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "disabled"},
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "..."}],
)
```

**When to use Opus 4.6 instead:** hardest and longest-horizon problems — large code migrations, deep research, extended autonomous work. Sonnet 4.6 wins on fast turnaround and cost efficiency.

### Migrating to Opus 4.6 / Sonnet 4.6 (from any older model)

**1. Manual extended thinking is deprecated — use adaptive thinking.**

`thinking: {type: "enabled", budget_tokens: N}` (manual extended thinking with a fixed token budget) is deprecated on Opus 4.6 and Sonnet 4.6. Replace it with `thinking: {type: "adaptive"}`, which lets Claude decide when and how much to think. Adaptive thinking also enables interleaved thinking automatically (no beta header needed).

```python
# Old (still works on older models, deprecated on 4.6)
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[...]
)

# New (Opus 4.6 / Sonnet 4.6)
response = client.messages.create(
    model="claude-opus-4-6",  # or "claude-sonnet-4-6"
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # optional: low | medium | high | max
    messages=[...]
)
```

Adaptive thinking is the long-term target, and on internal evaluations it outperforms manual extended thinking. Move when you can.

**Transitional escape hatch:** manual extended thinking is still *functional* on Opus 4.6 and Sonnet 4.6 (deprecated, will be removed in a future release). If you need a hard ceiling while migrating — for example, to bound token spend on a runaway workload before you've tuned `effort` — you can keep `budget_tokens` around alongside an explicit `effort` value, then remove it in a follow-up. `budget_tokens` must be strictly less than `max_tokens`:

```python
# Transitional only — deprecated, plan to remove
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 8192},  # must be < max_tokens
    output_config={"effort": "medium"},
    messages=[...],
)
```

If the user asks for a "thinking budget" on 4.6, the preferred answer is `effort` — use `low`, `medium`, `high`, or `max` (Opus-tier only — not Sonnet or Haiku) rather than a token count.

**2. Effort parameter (Opus 4.5, Opus 4.6, Sonnet 4.6 only).**

Controls thinking depth and overall token spend. Goes inside `output_config`, not top-level. Default is `high`. `max` is Opus-tier only (Opus 4.6 and later — not Sonnet or Haiku). Errors on Sonnet 4.5 and Haiku 4.5.

```python
output_config={"effort": "medium"}  # often the best cost / quality balance
```

### Migrating to the 4.6 family (Opus 4.6 and Sonnet 4.6)

**3. Assistant-turn prefills return 400 (Opus 4.6 and Sonnet 4.6).**

Prefilled responses on the final assistant turn are no longer supported on either Opus 4.6 or Sonnet 4.6 — both return a 400. Adding assistant messages *elsewhere* in the conversation (e.g., for few-shot examples) still works. Pick the replacement that matches what the prefill was doing:

| Prefill was used for                               | Replacement                                                                                                                               |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Forcing JSON / YAML / schema output                | `output_config.format` with a `json_schema` — see example below                                                                           |
| Forcing a classification label                     | Tool with an enum field containing valid labels, or structured outputs                                                                    |
| Skipping preambles (`Here is the summary:\n`)      | System prompt instruction: *"Respond directly without preamble. Do not start with phrases like 'Here is...' or 'Based on...'."*           |
| Steering around bad refusals                       | Usually no longer needed — 4.6 refuses far more appropriately. Plain user-turn prompting is sufficient.                                   |
| Continuing an interrupted response                 | Move continuation into the user turn: *"Your previous response was interrupted and ended with `[last text]`. Continue from there."*     |
| Injecting reminders / context hydration            | Inject into the user turn instead. For complex agent harnesses, expose context via a tool call or during compaction.                      |

```python
# Old (fails on Opus 4.6 / Sonnet 4.6) — prefill forcing JSON shape
messages=[
    {"role": "user", "content": "Extract the name."},
    {"role": "assistant", "content": "{\"name\": \""},
]

# New — structured outputs replace the prefill
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    output_config={"format": {"type": "json_schema", "schema": {...}}},
    messages=[{"role": "user", "content": "Extract the name."}],
)
```

**4. Stream for `max_tokens > ~16K` (all models); Opus 4.6 alone reaches 128K.**

Non-streaming requests hit SDK HTTP timeouts at high `max_tokens`, regardless of model — stream for anything above ~16K output. The streamable ceiling differs by model: Sonnet 4.6 and Haiku 4.5 cap at 64K, and Opus 4.6 alone goes up to 128K.

```python
with client.messages.stream(model="claude-opus-4-6", max_tokens=64000, ...) as stream:
    message = stream.get_final_message()
```

**5. Tool-call JSON escaping may differ (Opus 4.6 and Sonnet 4.6).**

Both 4.6 models can produce tool call `input` fields with Unicode or forward-slash escaping. Always parse with `json.loads()` / `JSON.parse()` — never raw-string-match the serialized input.

### All models

**6. `output_format` → `output_config.format` (API-wide).**

The old top-level `output_format` parameter on `messages.create()` is deprecated. Use `output_config.format` instead. This is not 4.6-specific — applies to every model.

---

## Beta Headers to Remove on 4.6

Several beta headers that were required on 4.5 are now GA on 4.6 and should be removed. Leaving them in is harmless but misleading; removing them also lets you move from `client.beta.messages.create(...)` back to `client.messages.create(...)`.

| Header                                    | Status on 4.6                                              | Action                                                  |
| ----------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| `effort-2025-11-24`                       | Effort parameter is GA                                     | Remove                                                  |
| `fine-grained-tool-streaming-2025-05-14`  | GA                                                         | Remove                                                  |
| `interleaved-thinking-2025-05-14`         | Adaptive thinking enables interleaved thinking automatically | Remove when using adaptive thinking; still functional on Sonnet 4.6 *with* manual extended thinking, but that path is deprecated |
| `token-efficient-tools-2025-02-19`        | Built in to all Claude 4+ models                           | Remove (no effect)                                      |
| `output-128k-2025-02-19`                  | Built in to Claude 4+ models                               | Remove (no effect)                                      |

Once you remove all of these and finish moving to adaptive thinking, you can switch the SDK call site from the beta namespace back to the regular one:

```python
# Before
response = client.beta.messages.create(
    model="claude-opus-4-5",
    betas=["interleaved-thinking-2025-05-14", "effort-2025-11-24"],
    ...
)

# After
response = client.messages.create(
    model="claude-opus-4-6",
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    ...
)
```

---

## Additional Changes When Coming from 3.x / 4.0 / 4.1 → 4.6

If you're jumping from Opus 4.1, Sonnet 4, Sonnet 3.7, or an older Claude 3.x model directly to 4.6, apply everything above *plus* the items in this section. Users already on Opus 4.5 / Sonnet 4.5 can skip this.

**1. Sampling parameters: `temperature` OR `top_p`, not both.**

Passing both will error on every Claude 4+ model:

```python
# Old (3.x only — errors on 4+)
client.messages.create(temperature=0.7, top_p=0.9, ...)

# New
client.messages.create(temperature=0.7, ...)  # or top_p, not both
```

**2. Update tool versions.**

Legacy tool versions are not supported on 4+. **Both the `type` and the `name` field change** — `text_editor_20250728` and `str_replace_based_edit_tool` are a pair; updating one without the other 400s. Also remove the `undo_edit` command from your text-editor integration:

| Old                                               | New                                                     |
| ------------------------------------------------- | ------------------------------------------------------- |
| `text_editor_20250124` + `str_replace_editor`     | `text_editor_20250728` + `str_replace_based_edit_tool`  |
| `code_execution_*` (earlier versions)             | `code_execution_20250825`                               |
| `undo_edit` command                               | *(no longer supported — delete call sites)*             |

```python
# Before
tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

# After — BOTH fields change
tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
```

**3. Handle the `refusal` stop reason.**

Claude 4+ can return `stop_reason: "refusal"` on the response. If your code only handles `end_turn` / `tool_use` / `max_tokens`, add a branch:

```python
if response.stop_reason == "refusal":
    # Surface the refusal to the user; do not retry with the same prompt
    ...
```

**4. Handle the `model_context_window_exceeded` stop reason (4.5+).**

Distinct from `max_tokens`: it means the model hit the *context window* limit, not the requested output cap. Handle both:

```python
if response.stop_reason == "model_context_window_exceeded":
    # Context window exhausted — compact or split the conversation
    ...
elif response.stop_reason == "max_tokens":
    # Requested output cap hit — retry with higher max_tokens or stream
    ...
```

**5. Trailing newlines preserved in tool call string parameters (4.5+).**

4.5 and 4.6 preserve trailing newlines that older models stripped. If your tool implementations do exact string matching against tool-call `input` values (e.g., `if name == "foo"`), verify they still match when the model sends `"foo\n"`. Normalizing with `.rstrip()` on the receiving side is usually the simplest fix.

**6. Haiku: rate limits reset between generations.**

Haiku 4.5 has its own rate-limit pool separate from Haiku 3 / 3.5. If you're ramping traffic as you migrate, check your tier's Haiku 4.5 limits at [API rate limits](https://platform.claude.com/docs/en/api/rate-limits) — a quota that comfortably served Haiku 3.5 traffic may need a tier bump for the same volume on 4.5.

---

## Prompt-Behavior Changes (Opus 4.5 / 4.6, Sonnet 4.6)

These don't break your code, but prompts that worked on 4.5-and-earlier may over- or under-trigger on 4.6. Tune as needed.

**1. Aggressive instructions cause overtriggering.** Opus 4.5 and 4.6 follow the system prompt much more closely than earlier models. Prompts written to *overcome* the old reluctance are now too aggressive:

| Before (worked on 4.0 / 4.5)                | After (use on 4.6)                        |
| ------------------------------------------- | ----------------------------------------- |
| `CRITICAL: You MUST use this tool when...`  | `Use this tool when...`                   |
| `Default to using [tool]`                   | `Use [tool] when it would improve X`      |
| `If in doubt, use [tool]`                   | *(delete — no longer needed)*             |

If the model is now overtriggering a tool or skill, the fix is almost always to dial back the language, not to add more guardrails.

**2. Overthinking and excessive exploration (Opus 4.6).** At higher `effort` settings, Opus 4.6 explores more before answering. If that burns too many thinking tokens, lower `effort` first (`medium` is often the sweet spot) before adding prose instructions to constrain reasoning.

**3. Overeager subagent spawning (Opus 4.6).** Opus 4.6 has a strong preference for delegating to subagents. If you see it spawning a subagent for something a direct `grep` or `read` would solve, add guidance: *"Use subagents only for parallel or independent workstreams. For single-file reads or sequential operations, work directly."*

**4. Overengineering (Opus 4.5 / 4.6).** Both models may add extra files, abstractions, or defensive error handling beyond what was asked. If you want minimal changes, prompt for it explicitly: *"Only make changes directly requested. Don't add helpers, abstractions, or error handling for scenarios that can't happen."*

**5. LaTeX math output (Opus 4.6).** Opus 4.6 defaults to LaTeX (`\frac{}{}`, `$...$`) for math and technical content. If you need plain text, instruct it explicitly: *"Format all math as plain text — no LaTeX, no `$`, no `\frac{}{}`. Use `/` for division and `^` for exponents."*

**6. Skipped verbal summaries (4.6 family).** The 4.6 models are more concise and may skip the summary paragraph after a tool call, jumping straight to the next action. If you rely on those summaries for visibility, add: *"After completing a task that involves tool use, provide a brief summary of what you did."*

**7. "Think" as a trigger word (Opus 4.5 with thinking disabled).** When `thinking` is off, Opus 4.5 is particularly sensitive to the word *think* and may reason more than you want. Use `consider`, `evaluate`, or `reason through` instead.

---

## Model-ID Rename Quick Reference

| Old string (migration source)  | New string         |
| ------------------------------ | ------------------ |
| `claude-opus-4-7`              | `claude-opus-4-8`  |
| `claude-opus-4-6`              | `claude-opus-4-8`  |
| `claude-opus-4-5`              | `claude-opus-4-8`  |
| `claude-opus-4-1`              | `claude-opus-4-8`  |
| `claude-opus-4-0`              | `claude-opus-4-8`  |
| `claude-sonnet-4-5`            | `claude-sonnet-4-6`|
| `claude-sonnet-4-0`            | `claude-sonnet-4-6`|

Older aliases (`claude-opus-4-7`, `claude-opus-4-6`, `claude-opus-4-5`, `claude-sonnet-4-5`, etc.) are still active and can be pinned if you need time before upgrading — see `shared/models.md` for the full legacy list.

### Amazon Bedrock model IDs

If the code uses the `AnthropicBedrockMantle` client (Python `anthropic[bedrock]`, TypeScript `@anthropic-ai/bedrock-sdk`, Java `BedrockMantleBackend`, Go `bedrock.NewMantleClient`, etc.) or targets `https://bedrock-mantle.{region}.api.aws/anthropic`, it is running on **Claude in Amazon Bedrock**. All breaking changes in this guide apply unchanged there — it serves the same Messages API shape — but model IDs carry an `anthropic.` provider prefix:

| First-party ID | Bedrock ID |
|---|---|
| `claude-opus-4-8` | `anthropic.claude-opus-4-8` |
| `claude-opus-4-7` | `anthropic.claude-opus-4-7` |
| `claude-haiku-4-5` | `anthropic.claude-haiku-4-5` |

When migrating a Bedrock file, apply the same rename-table row as first-party, then keep/add the `anthropic.` prefix. Do **not** generate a first-party `claude-*` ID for a Bedrock client — it will 400.

**Skip for Bedrock:** the `code_execution_*` tool-version checklist item and the **Task Budgets** section — both are first-party-only features (Bedrock does not support server-side Anthropic tools or the `task-budgets-2026-03-13` beta). Everything else in this guide — `effort`, adaptive/extended thinking, `output_config.format`, `thinking.display`, fine-grained tool streaming, token counting — is available on Bedrock.

> **Out of scope:** the legacy Amazon Bedrock integration (`InvokeModel` / `Converse` APIs with ARN-versioned IDs like `anthropic.claude-3-5-sonnet-20241022-v2:0`) uses a different request shape and model-ID format. This guide does not cover it; WebFetch the Bedrock page in `shared/live-sources.md` if the user is migrating between the two Bedrock integrations.

### Claude Platform on AWS

If the code uses `AnthropicAWS` / `AnthropicAws` / `anthropicaws.NewClient` / `AnthropicAwsClient` (or targets `https://aws-external-anthropic.{region}.api.aws`), it is running on **Claude Platform on AWS** — Anthropic-operated, same-day API parity. Model IDs are **bare first-party** strings; apply the rename table above **verbatim** and every breaking-change section in this guide unchanged. There is nothing to skip. Do **not** add an `anthropic.` prefix (that's Amazon Bedrock, a separate offering). See `shared/claude-platform-on-aws.md` for client/auth details.

---

## Migration Checklist

Every item is tagged: **`[BLOCKS]`** items cause a 400 error, infinite loop, silent timeout, or wrong tool selection if missed — apply these as code edits, not as suggestions. **`[TUNE]`** items are quality/cost adjustments.

For each file that calls `messages.create()` / equivalent SDK method:

- [ ] **[BLOCKS]** Update the `model=` string to the new alias
- [ ] **[BLOCKS]** Replace `budget_tokens` with `thinking={"type": "adaptive"}` (deprecated on Opus 4.6 / Sonnet 4.6)
- [ ] **[BLOCKS]** Move `format` from top-level `output_format` into `output_config.format`
- [ ] **[BLOCKS]** Remove any assistant-turn prefills if targeting Opus 4.6 or Sonnet 4.6 (see the prefill replacement table)
- [ ] **[BLOCKS]** Switch to streaming if `max_tokens > ~16000` (otherwise SDK HTTP timeout)
- [ ] **[TUNE]** Verify tool-input handling parses JSON rather than raw-string-matching the serialized input (4.6 may escape Unicode / forward slashes differently; most SDKs already expose `block.input` as a parsed object)
- [ ] **[TUNE]** Set `output_config={"effort": "..."}` explicitly — especially when moving Sonnet 4.5 → Sonnet 4.6 (4.6 defaults to `high`)
- [ ] **[TUNE]** Remove GA beta headers: `effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14`, `token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`; remove `interleaved-thinking-2025-05-14` once on adaptive thinking
- [ ] **[TUNE]** Switch `client.beta.messages.create(...)` → `client.messages.create(...)` once all betas are removed
- [ ] **[TUNE]** Review system prompt for aggressive tool language (`CRITICAL:`, `MUST`, `If in doubt`) and dial it back

**Extra items when coming from 3.x / 4.0 / 4.1:**
- [ ] **[BLOCKS]** Remove either `temperature` or `top_p` (passing both 400s on Claude 4+)
- [ ] **[BLOCKS]** Update text-editor tool `type` to `text_editor_20250728`
- [ ] **[BLOCKS]** Update text-editor tool `name` to `str_replace_based_edit_tool` — **changing only the `type` and keeping `name: "str_replace_editor"` returns a 400**
- [ ] **[BLOCKS]** Update code-execution tool to `code_execution_20250825`
- [ ] **[BLOCKS]** Delete any `undo_edit` command call sites
- [ ] **[TUNE]** Add handling for `stop_reason == "refusal"`
- [ ] **[TUNE]** Add handling for `stop_reason == "model_context_window_exceeded"` (4.5+)
- [ ] **[TUNE]** Verify tool-param string matching tolerates trailing newlines (preserved on 4.5+)
- [ ] **[TUNE]** If moving to Haiku 4.5: review rate-limit tier (separate pool from Haiku 3.x)

**Verification:**
- [ ] Run one test request and inspect `response.stop_reason`, `response.usage`, and whether tool-use / thinking behavior matches expectations

For cached prompts: the render order and hash inputs did not change, so existing `cache_control` breakpoints keep working. However, **changing the model string invalidates the existing cache** — the first request on the new model will write the cache fresh.

---

## Migrating to Opus 4.7

> **Model ID `claude-opus-4-7` is authoritative as written here.** When the user asks to migrate to Opus 4.7, write `model="claude-opus-4-7"` exactly. Do **not** WebFetch to verify — this guide is the source of truth for migration target IDs. The corresponding entry exists in `shared/models.md`.

Claude Opus 4.7 was Anthropic's most capable model at its launch and is now the previous-generation Opus (Opus 4.8 is current — see Migrating to Opus 4.8 below). It is highly autonomous and performs exceptionally well on long-horizon agentic work, knowledge work, vision tasks, and memory tasks. This section summarizes everything that was new at the 4.7 launch and remains the layered breaking-change path for callers coming from Opus 4.6 or older. It is layered on top of the 4.6 migration above — if the caller is jumping from Opus 4.5 or older, apply the 4.6 changes first, then this section, then the 4.8 section.

**TL;DR for someone already on Opus 4.6:** update the model ID to `claude-opus-4-7`, strip any remaining `budget_tokens` and sampling parameters (both 400 on Opus 4.7), give `max_tokens` extra headroom and re-baseline with `count_tokens()` against the new model, opt back into `thinking.display: "summarized"` if reasoning is surfaced to users, and re-tune `effort` — it matters more on 4.7 than on any prior Opus.

### Breaking changes (will 400 on Opus 4.7)

**Extended thinking removed.**

`thinking: {type: "enabled", budget_tokens: N}` is no longer supported on Claude Opus 4.7 or later models and returns a 400 error. Switch to adaptive thinking (`thinking: {type: "adaptive"}`) and use the effort parameter to control thinking depth. Adaptive thinking is **off by default** on Claude Opus 4.7: requests with no `thinking` field run without thinking, matching Opus 4.6 behavior. Set `thinking: {type: "adaptive"}` explicitly to enable it.

```python
# Before (Opus 4.6)
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    messages=[{"role": "user", "content": "..."}],
)

# After (Opus 4.7)
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
    messages=[{"role": "user", "content": "..."}],
)
```

If the caller wasn't using extended thinking, no change is required — thinking is off by default, or can be set explicitly with `thinking={"type": "disabled"}`.

Delete `budget_tokens` plumbing entirely. For the replacement `effort` value, see **Choosing an effort level on Opus 4.7** below — there is no exact 1:1 mapping from `budget_tokens`.

**Sampling parameters removed.**

The `temperature`, `top_p`, and `top_k` parameters are no longer accepted on Claude Opus 4.7. Requests that include them return a 400 error. Remove these fields from your request payloads. Prompting is the recommended way to guide model behavior on Claude Opus 4.7. If you were using `temperature = 0` for determinism, note that it never guaranteed identical outputs on prior models.

```python
# Before — errors on Opus 4.7
client.messages.create(temperature=0.7, top_p=0.9, ...)

# After
client.messages.create(...)  # no sampling params
```

- **If the intent was determinism** — use `effort: "low"` with a tighter prompt.
- **If the intent was creative variance** — the prompt replacement depends on the use case; **ask the user** how they want variance elicited. If you can't ask, add a use-case-appropriate instruction along the lines of *"choose something off-distribution and interesting"* — e.g. for text generation, *"Vary your phrasing and structure across responses"*; for frontend/design, use the propose-4-directions approach under **Design and frontend coding** below.

### Choosing an effort level on Opus 4.7

`budget_tokens` controlled how much to *think*; `effort` controls how much to think *and* act, so there is no exact 1:1 mapping. **Use `xhigh` for best results in coding and agentic use cases, and a minimum of `high` for most intelligence-sensitive use cases.** Experiment with other levels to further tune token usage and intelligence:

| Level | Use when | Notes |
| --- | --- | --- |
| `max` | Intelligence-demanding tasks worth testing at the ceiling | Can deliver gains in some use cases but may show diminishing returns from increased token usage; can be prone to overthinking |
| `xhigh` | **Most coding and agentic use cases** | The best setting for these; used as the default in Claude Code |
| `high` | Intelligence-sensitive use cases generally | Balances token usage and intelligence; recommended minimum for most intelligence-sensitive work |
| `medium` | Cost-sensitive use cases that need to reduce token usage while trading off intelligence | |
| `low` | Short, scoped tasks and latency-sensitive workloads that are not intelligence-sensitive | |

### Silent default changes (no error, but behavior differs)

**Thinking content omitted by default.**

Thinking blocks still appear in the response stream on Claude Opus 4.7, but their `thinking` field is empty unless you explicitly opt in. This is a silent change from Claude Opus 4.6, where the default was to return summarized thinking text. To restore summarized thinking content on Claude Opus 4.7, set `thinking.display` to `"summarized"`. **The block-field name is unchanged** — it is still `block.thinking` on a `thinking`-type block; do not rename it.

**Detect this:** any code that reads `block.thinking` (or equivalent) from a `thinking`-type block and renders it in a UI, log, or trace. **The fix is the request parameter, not the response handling** — add `display: "summarized"` to the `thinking` parameter:

```python
thinking={"type": "adaptive", "display": "summarized"}  # "display" is new on Opus 4.7; values: "omitted" (default) | "summarized"
```

The default is `"omitted"` on Claude Opus 4.7. If thinking content was never surfaced anywhere, no change needed. If your product streams reasoning to users, the new default appears as a long pause before output begins; set `display: "summarized"` to restore visible progress during thinking.

**Updated token counting.**

Claude Opus 4.7 and Claude Opus 4.6 count tokens differently. The same input text produces a higher token count on Claude Opus 4.7 than on Claude Opus 4.6, and `/v1/messages/count_tokens` will return a different number of tokens for Claude Opus 4.7 than it did for Claude Opus 4.6. The token efficiency of Claude Opus 4.7 can vary by workload shape. Prompting interventions, `task_budget`, and `effort` can help control costs and ensure appropriate token usage. Keep in mind that these controls may trade off model intelligence. **Update your `max_tokens` parameters to give additional headroom, including compaction triggers.** Claude Opus 4.7 provides a 1M context window at standard API pricing with no long-context premium.

What else to check:

- Client-side token estimators (tiktoken-style approximations) calibrated against 4.6
- Cost calculators that multiply tokens by a fixed per-token rate
- Rate-limit retry thresholds keyed to measured token counts

Re-baseline by re-running `client.messages.count_tokens()` against `claude-opus-4-7` on a representative sample of the caller's prompts. Do not apply a blanket multiplier. For cost-sensitive workloads, consider reducing `effort` by one level (e.g. `high` → `medium`). For agentic loops, consider adopting Task Budgets (below).

### New feature: Task Budgets (beta)

Opus 4.7 introduces **task budgets** — tell Claude how many tokens it has for a full agentic loop (thinking + tool calls + final output). The model sees a running countdown and uses it to prioritize work and wrap up gracefully as the budget is consumed.

This is a **suggestion the model is aware of**, not a hard cap. It is distinct from `max_tokens`, which remains the enforced per-response limit and is *not* surfaced to the model. Use `task_budget` when you want the model to self-moderate; use `max_tokens` as a hard ceiling to cap usage.

Requires beta header `task-budgets-2026-03-13`:

```python
client.beta.messages.create(
    betas=["task-budgets-2026-03-13"],
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 128000},
    },
    messages=[...],
)
```

Set a generous budget for open-ended agentic tasks and tighten it for latency-sensitive ones. **Minimum `task_budget.total` is 20,000 tokens.** If the budget is too restrictive for the task, the model may complete it less thoroughly, referencing its budget as the constraint. **Do not add `task_budget` during a migration unless you are sure the budget value is right** — if you can run the workload and measure, do so; otherwise ask the user for the value rather than guessing. This is the primary lever for offsetting the token-counting shift on agentic workloads.

### Capability improvements

**High-resolution vision.** Opus 4.7 is the first Claude model with high-resolution image support. Maximum image resolution is **2576 pixels on the long edge** (up from 1568px on Opus 4.6 and prior). This unlocks gains on vision-heavy workloads, especially computer use and screenshot/artifact/document understanding. Coordinates returned by the model now map 1:1 to actual image pixels, so no scale-factor math is needed.

High-res support is **automatic on Opus 4.7** — no beta header, no client-side opt-in required. The model accepts larger inputs and returns pixel-accurate coordinates out of the box.

**Token cost.** Full-resolution images on Opus 4.7 can use up to ~3× more image tokens than on prior models (up to ~4784 tokens per image, vs. the previous ~1,600-token cap). If the extra fidelity isn't needed, downsample client-side before sending to control cost — but **do not add downsampling by default during a migration**. If you're not sure whether the pipeline needs the fidelity, ask the user rather than guessing. Use `count_tokens()` on representative images on Opus 4.7 to re-baseline before reacting to any measured cost shift.

Beyond resolution, Opus 4.7 also improves on low-level perception (pointing, measuring, counting) and natural-image bounding-box localization and detection.

**Knowledge work.** Meaningful gains on tasks where the model visually verifies its own output — `.docx` redlining, `.pptx` editing, and programmatic chart/figure analysis (e.g. pixel-level data transcription via image-processing libraries). If prompts have scaffolding like *"double-check the slide layout before returning"*, try removing it and re-baselining.

**Memory.** Opus 4.7 is better at writing and using file-system-based memory. If an agent maintains a scratchpad, notes file, or structured memory store across turns, that agent should improve at jotting down notes to itself and leveraging its notes in future tasks.

**User-facing progress updates.** Opus 4.7 provides more regular, higher-quality interim updates during long agentic traces. If the system prompt has scaffolding like *"After every 3 tool calls, summarize progress"*, try removing it to avoid excessive user-facing text. If the length or contents of Opus 4.7's updates are not well-calibrated to your use case, explicitly describe what these updates should look like in the prompt and provide examples.

### Real-time cybersecurity safeguards

Requests that involve prohibited or high-risk topics may lead to refusals.

### Fast Mode: not available on Opus 4.7

Opus 4.7 does not have a Fast Mode variant. **Opus 4.6 Fast remains supported**. Only surface this if the caller's code actually uses a Fast Mode model string (e.g. `claude-opus-4-6-fast`); if the word "fast" does not appear in the code, say nothing about Fast Mode.

When you see `model="claude-opus-4-6-fast"` (or similar), **the migration edit is**:

```python
# Opus 4.7 has no Fast Mode — keeping on 4.6 Fast (caller's choice to switch to standard Opus 4.7).
model="claude-opus-4-6-fast",
```

That is: leave the model string **unchanged**, add the comment above it, and tell the user their two options — (a) stay on Opus 4.6 Fast, which remains supported, or (b) move latency-tolerant traffic to standard Opus 4.7 for the intelligence gain. Do **not** rewrite the model string to `claude-opus-4-7` yourself; that silently trades latency for intelligence, which is the caller's decision.

### Behavioral shifts (prompt-tunable)

These don't break anything, but prompts tuned for Opus 4.6 may land differently. Opus 4.7 is more steerable than 4.6, so small prompt nudges usually close the gap.

**More literal instruction following.** Claude Opus 4.7 interprets prompts more literally and explicitly than Claude Opus 4.6, particularly at lower effort levels. It will not silently generalize an instruction from one item to another, and it will not infer requests you didn't make. The upside of this literalism is precision and less thrash. It generally performs better for API use cases with carefully tuned prompts, structured extraction, and pipelines where you want predictable behavior. A prompt and harness review may be especially helpful for migration to Claude Opus 4.7.

**Verbosity calibrates to task complexity.** Opus 4.7 scales response length to how complex it judges the task to be, rather than defaulting to a fixed verbosity — shorter answers on simple lookups, much longer on open-ended analysis. If the product depends on a particular length or style, tune the prompt explicitly. To reduce verbosity:

> *"Provide concise, focused responses. Skip non-essential context, and keep examples minimal."*

If you see specific kinds of over-verbosity (e.g. over-explaining), add instructions targeting those. Positive examples showing the desired level of concision tend to be more effective than negative examples or instructions telling the model what not to do. Do **not** assume existing "be concise" instructions should be removed — test first.

**Tone and writing style.** Opus 4.7 is more direct and opinionated, with less validation-forward phrasing and fewer emoji than Opus 4.6's warmer style. As with any new model, prose style on long-form writing may shift. If the product relies on a specific voice, re-evaluate style prompts against the new baseline. If a warmer or more conversational voice is wanted, specify it:

> *"Use a warm, collaborative tone. Acknowledge the user's framing before answering."*

**`effort` matters more than on any prior Opus.** Opus 4.7 respects `effort` levels more strictly, especially at the low end. At `low` and `medium` it scopes work to what was asked rather than going above and beyond — good for latency and cost, but on moderate tasks at `low` there is some risk of under-thinking.

- If shallow reasoning shows up on complex problems, raise `effort` to `high` or `xhigh` rather than prompting around it.
- If `effort` must stay `low` for latency, add targeted guidance: *"This task involves multi-step reasoning. Think carefully through the problem before responding."*
- **At `xhigh` or `max`, set a large `max_tokens`** so the model has room to think and act across tool calls and subagents. Start at 64K and tune from there. (`xhigh` is a new effort level on Opus 4.7, between `high` and `max`.)

Adaptive-thinking triggering is also steerable. If the model thinks more often than wanted — which can happen with large or complex system prompts — add: *"Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multi-step reasoning. When in doubt, respond directly."*

**Uses tools less often by default.** Opus 4.7 tends to use tools less often than 4.6 and to use reasoning more. This produces better results in most cases, but for products that rely on tools (search/retrieval, function-calling, computer-use steps), it can drop tool-use rate. Two levers:

- **Raise `effort`** — `high` or `xhigh` show substantially more tool usage in agentic search and coding, and are especially useful for knowledge work.
- **Prompt for it** — be explicit in tool descriptions or the system prompt about when and how to use the tool, and encourage the model to err on the side of using it more often:

> *"When the answer depends on information not present in the conversation, you MUST call the `search` tool before answering — do not answer from prior knowledge."*

**Fewer subagents by default.** Opus 4.7 tends to spawn fewer subagents than 4.6. This is steerable — give explicit guidance on when delegation is desirable. For a coding agent, for example:

> *"Do NOT spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see). Spawn multiple subagents in the same turn when fanning out across items or reading multiple files."*

**Design and frontend coding.** Opus 4.7 has stronger design instincts than 4.6, with a consistent default house style: warm cream/off-white backgrounds (around `#F4F1EA`), serif display type (Georgia, Fraunces, Playfair), italic word-accents, and a terracotta/amber accent. This reads well for editorial, hospitality, and portfolio briefs, but will feel off for dashboards, dev tools, fintech, healthcare, or enterprise apps — and it appears in slide decks as well as web UIs.

The default is persistent. Generic instructions ("don't use cream," "make it clean and minimal") tend to shift the model to a different fixed palette rather than producing variety. Two approaches work reliably:

1. **Specify a concrete alternative.** The model follows explicit specs precisely — give exact hex values, typefaces, and layout constraints.
2. **Have the model propose options before building.** This breaks the default and gives the user control:

   > *"Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction."*

If the caller previously relied on `temperature` for design variety, use approach (2) — it produces meaningfully different directions across runs.

Opus 4.7 also requires less frontend-design prompting than previous models to avoid generic "AI slop" aesthetics. Where earlier models needed a lengthy anti-slop snippet, Opus 4.7 generates distinctive, creative frontends with a much shorter nudge. This snippet works well alongside the variety approaches above:

> *"NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions."*

**Interactive coding products.** Opus 4.7's token usage and behavior can differ between autonomous, asynchronous coding agents with a single user turn and interactive, synchronous coding agents with multiple user turns. Specifically, it tends to use more tokens in interactive settings, primarily because it reasons more after user turns. This can improve long-horizon coherence, instruction following, and coding capabilities in long interactive coding sessions, but also comes with more token usage. To maximize both performance and token efficiency in coding products, use `effort: "xhigh"` or `"high"`, add autonomous features (like an auto mode), and reduce the number of human interactions required from users.

When limiting required user interactions, specify the task, intent, and relevant constraints upfront in the first human turn. Well-specified, clear, and accurate task descriptions upfront help maximize autonomy and intelligence while minimizing extra token usage after user turns — because Opus 4.7 is more autonomous than prior models, this usage pattern helps to maximize performance. In contrast, ambiguous or underspecified prompts conveyed progressively over multiple user turns tend to reduce token efficiency and sometimes performance.

**Code review.** Opus 4.7 is meaningfully better at finding bugs than prior models, with both higher recall and precision. However, if a code-review harness was tuned for an earlier model, it may initially show *lower* recall — this is likely a harness effect, not a capability regression. When a review prompt says "only report high-severity issues," "be conservative," or "don't nitpick," Opus 4.7 follows that instruction more faithfully than earlier models did: it investigates just as thoroughly, identifies the bugs, and then declines to report findings it judges to be below the stated bar. Precision rises, but measured recall can fall even though underlying bug-finding has improved.

Recommended prompt language:

> *"Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage — a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them."*

This can be used without an actual second step, but moving confidence filtering out of the finding step often helps. If the harness has a separate verification/dedup/ranking stage, tell the model explicitly that its job at the finding stage is coverage, not filtering. If single-pass self-filtering is wanted, be concrete about the bar rather than using qualitative terms like "important" — e.g. *"report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences."* Iterate on prompts against a subset of evals to validate recall or F1 gains.

**Computer use.** Computer use works across resolutions up to the new 2576px / 3.75MP maximum. Sending images at **1080p** provides a good balance of performance and cost. For particularly cost-sensitive workloads, **720p** or **1366×768** are lower-cost options with strong performance. Test to find the ideal settings for the use case; experimenting with `effort` can also help tune behavior.

---

## Opus 4.7 Migration Checklist

Every item is tagged: **`[BLOCKS]`** items cause a 400 error, infinite loop, silent truncation, or empty output if missed — apply these as code edits, not as suggestions. **`[TUNE]`** items are quality/cost adjustments — surface them to the user as recommendations.

`[BLOCKS]` items prefixed with **"If…"** or **"At…"** are conditional. Before working through the list, **scan the file** for the conditions: does it surface thinking text to a UI/log? Does it set `output_config.effort` to `"x-high"` or `"max"`? Is it a security workload? Is it a multi-turn agentic loop? Apply only the items whose condition matches.

- [ ] **[BLOCKS]** Replace `thinking: {type: "enabled", budget_tokens: N}` with `thinking: {type: "adaptive"}` + `output_config.effort`; delete `budget_tokens` plumbing entirely
- [ ] **[BLOCKS]** Strip `temperature`, `top_p`, `top_k` from request construction
- [ ] **[BLOCKS]** If thinking content is surfaced to users or stored in logs: add `thinking.display: "summarized"` (otherwise the rendered text is empty)
- [ ] **[BLOCKS]** At `output_config.effort` of `xhigh` or `max`: set `max_tokens` ≥ 64000 (otherwise output truncates mid-thought)
- [ ] **[TUNE]** Give `max_tokens` and compaction triggers extra headroom; re-run `count_tokens()` against `claude-opus-4-7` on representative prompts to re-baseline (no blanket multiplier)
- [ ] **[TUNE]** Re-baseline cost and rate-limit dashboards *before* reacting to measured shifts
- [ ] **[TUNE]** Re-evaluate `effort` per route — use `xhigh` for coding/agentic and a minimum of `high` for most intelligence-sensitive work; it matters more on 4.7 than any prior Opus
- [ ] **[TUNE]** Multi-turn agentic loops: adopt the API-native Task Budgets (`output_config.task_budget`, beta `task-budgets-2026-03-13`, minimum 20k tokens) — this is for capping *cumulative* spend across a loop; per-turn depth is `effort`
- [ ] **[TUNE]** Check for ambiguous or underspecified instructions that relied on 4.6 generalizing intent, and update them to be clearer or more precise — 4.7 follows them literally
- [ ] **[TUNE]** Tool-use workloads: add explicit when/how-to-use guidance to tool descriptions (4.7 reaches for tools less often)
- [ ] **[TUNE]** Verbosity: test existing length instructions before changing them — 4.7 calibrates length to task complexity, so tune for the desired output rather than assuming a direction
- [ ] **[TUNE]** Remove forced-progress-update scaffolding (*"after every N tool calls…"*)
- [ ] **[TUNE]** Remove knowledge-work verification scaffolding (*"double-check the slide layout…"*) and re-baseline
- [ ] **[TUNE]** Add tone instruction if a warmer / more conversational voice is needed; re-evaluate style prompts on writing-heavy routes
- [ ] **[TUNE]** Subagent tool present: add explicit spawn / don't-spawn guidance
- [ ] **[TUNE]** Frontend/design output: specify a concrete palette/typeface, or have the model propose 4 visual directions before building (the default cream/serif house style is persistent)
- [ ] **[TUNE]** Interactive coding products: use `effort: "xhigh"` or `"high"`, add autonomous features (e.g. an auto mode) to reduce human interactions, and specify task/intent/constraints upfront in the first turn
- [ ] **[TUNE]** Code-review harnesses: remove or loosen "only report high-severity" / "be conservative" filters and have the model report every finding with confidence + severity; move filtering to a downstream step (4.7 follows severity filters more literally, which can depress measured recall)
- [ ] **[TUNE]** Vision-heavy pipelines (screenshots, charts, document understanding): leave images at native resolution up to 2576px long edge for the accuracy gain; remove any scale-factor math from coordinate handling (coords are now 1:1 with pixels). No beta header / opt-in needed — high-res is automatic on Opus 4.7.
- [ ] **[TUNE]** Computer-use pipelines: send screenshots at 1080p for a good performance/cost balance (720p or 1366×768 for cost-sensitive workloads); experiment with `effort` to tune behavior
- [ ] **[TUNE]** Cost-sensitive image pipelines: full-res images on 4.7 use up to ~4784 tokens vs ~1,600 on prior models (~3×). Downsampling client-side before upload avoids the increase, but **do not downsample by default** — if you're unsure whether fidelity is needed, ask the user. Re-baseline with `count_tokens()` on representative images before reacting to cost shifts.

---

## Migrating to Opus 4.8

> **Model ID `claude-opus-4-8` is authoritative as written here.** When the user asks to migrate to Opus 4.8, write `model="claude-opus-4-8"` exactly. Do **not** WebFetch to verify — this guide is the source of truth for migration target IDs. The corresponding entry exists in `shared/models.md`.

Claude Opus 4.8 is our most capable generally available model to date — highly autonomous, with state-of-the-art long-horizon agentic execution, knowledge work, and memory. It is layered on top of the Opus 4.7 migration above. If the caller is jumping from Opus 4.6 or older, apply the 4.6 and 4.7 sections first, then this one.

**No new breaking changes.** Opus 4.8 keeps the same request surface as Opus 4.7. The same calls that already work on 4.7 work unchanged on 4.8 — adaptive thinking only (`thinking: {type: "enabled", budget_tokens: N}` still 400s; use `{type: "adaptive"}`), sampling parameters (`temperature`, `top_p`, `top_k`) still rejected, last-assistant-turn prefills still 400, `thinking.display` still defaults to `"omitted"`, and the `low`/`medium`/`high`/`xhigh`/`max` effort levels, Task Budgets (beta), and high-resolution vision all behave as on 4.7. A 4.7 → 4.8 migration is therefore **the model-ID swap plus prompt re-tuning** — there is no required code edit beyond the model string.

**TL;DR for someone already on Opus 4.7:** swap the model ID to `claude-opus-4-8`. Nothing else is required to avoid an error. Then re-tune prompts for the behavioral shifts: 4.8 narrates *more* than 4.7 (add a silence-default if you want 4.7-like terseness), writes in a warmer, less hedged voice, is more deliberate and asks more often (add autonomy guidance to claw back ask-rate), and is more conservative about reaching for search, subagents, file-based memory, and custom tools (add explicit "when to use this" triggering). For long-horizon agentic work, give the full task specification up front in one well-specified turn and run at high effort.

### No new API breaking changes (inherited from 4.7)

These all carry over from Opus 4.7 unchanged — apply them only if the caller is coming from Opus 4.6 or earlier (see the **Migrating to Opus 4.7** section above for the before/after and the SDK-specific syntax):

- `thinking: {type: "enabled", budget_tokens: N}` → 400. Use `thinking: {type: "adaptive"}` + `output_config.effort`.
- `temperature`, `top_p`, `top_k` → 400. Remove them; steer with prompting.
- Last-assistant-turn prefills → 400. Use `output_config.format` (structured outputs) or a system-prompt instruction.
- `thinking.display` defaults to `"omitted"`; set `"summarized"` if you surface reasoning to users.

If the caller is already on Opus 4.7 and these are clean, there is nothing to change here.

### New API feature: mid-session system prompts

You can deliver trusted instructions partway through a session by placing `{"role": "system", ...}` entries directly in the `messages` array — without editing the top-level system prompt and invalidating your prompt cache. Use it for things the application learns mid-session: the user delivered async context, a mode toggled (auto-approve enabled), files changed on disk, the remaining token budget dropped.

```python
messages=[
    {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "...", "content": "..."}]},
    {"role": "system", "content": "This project's codebase is Go. Write code in Go."},
]
```

Phrase these as **context, not commands**. State the fact and let Claude act on it; avoid override-style language ("ignore what the user said", "regardless of the user's request", "disregard the previous instruction"). Claude is trained to protect users from instructions that appear to work against them, and that protection applies to the system role too. This is a beta (`anthropic-beta: mid-conversation-system-2026-04-07`) and is available from Opus 4.7 onward, not 4.8-exclusive. For cache-placement details and the older-model `<system-reminder>` fallback, see `shared/prompt-caching.md` and `shared/agent-design.md`.

### Capability improvements

**Long-horizon agentic execution.** Opus 4.8 is state-of-the-art at long, autonomous agentic work — complex refactors and overnight coding runs that complete without human correction. To get the most out of it, **give the full task specification up front in a single well-specified initial turn and run at high effort** (`effort: "high"` or `"xhigh"`). Its long-horizon coherence comes partly from reasoning more at each step; combined with a clear up-front goal, that more-intelligent planning often produces more efficient *and* more accurate output than prior frontier models. The "clear goal up front" principle maps to two product surfaces: in Claude Code, `/goal` sets direction for the run; with **Managed Agents (CMA)**, state what "done" looks like via an **Outcome** (`user.define_outcome` with a gradeable rubric — the harness runs an iterate → grade → revise loop), see `shared/managed-agents-outcomes.md`.

**Effort is a dimension to test, not a fixed setting.** On prior models many reached for `xhigh` reflexively to maximize intelligence. Opus 4.8 has a higher intelligence ceiling, so **start at `high` as the default and iterate** rather than defaulting to `xhigh`. Sweep `medium`, `high`, and `xhigh` on your own eval set and weigh the intelligence ↔ latency ↔ cost tradeoff per route — the relationship isn't monotonic: higher effort up front often *reduces* turn count and total cost on agentic work, while for some tasks `medium` delivers equally good results in less time. Reserve `max` for extremely hard, latency-insensitive cases. The per-level effort table in the **Migrating to Opus 4.7** section above applies unchanged on 4.8.

**Writing voice and clarity.** Testers consistently describe 4.8's prose as clearer, warmer, and less hedged than prior models, with fewer measurable AI vocal tics — especially at higher effort, where it approaches expert-level prose and structure. This is roughly the **opposite** direction from the 4.7 shift (4.7 was more clipped, direct, and less validation-forward). If you added style prompts to counter 4.7's terseness or to inject warmth, re-evaluate them against the new baseline before keeping them — they may now overcorrect. 4.8 is also a stronger thought partner: more thoughtful, more willing to push back, and more likely to infer the right answer from context.

**Code review and debugging.** Stronger real-bug finding and clearer explanations than 4.7 — one-shot fixes where 4.7 needed more, and correctly identifying intermittent flakes rather than declaring "fixed" after one clean run. The 4.7 caveat still applies: if a review harness says "only report high-severity issues" or "be conservative", 4.8 follows it literally and measured recall can drop even though underlying bug-finding improved. Tell the model to report everything and filter downstream (or review a second time) — see the **Code review** guidance in the 4.7 section for the recommended prompt.

### Behavioral shifts (prompt-tunable)

None of these break code, but prompts tuned for Opus 4.7 may land differently. 4.8 follows instructions well, so small, explicit nudges close the gap.

**Tool triggering is surface-dependent (search & knowledge).** 4.8's tool-triggering is more surface-dependent than in prior models: with a system prompt present it is high-precision / low-recall — web search triggers slightly more often but runs fewer rounds per trigger, while knowledge-retrieval tools (Drive, project knowledge, connected files) trigger *less* often. It searches when it's confident search is needed and otherwise answers from context, which can lower research depth on tasks that need it. Recover should-search rate with an explicit search-first instruction:

> ```
> <search_first>
> For questions where current information would change the answer (recent events, current roles or prices, version-specific behavior, or anything the user flags as time-sensitive) search before answering rather than answering from memory. For open-ended research requests, begin searching immediately; do not ask a scoping question first unless the request is genuinely ambiguous about what to research.
> </search_first>
> ```

**Under-utilization of subagents, memory, and custom tools.** Separately from search, 4.8 is conservative about reaching for capabilities that need an explicit "decide to use this" step — file-based memory, subagent delegation, custom tools. It won't reach for complex or expensive capabilities unless reasonably sure they're needed. This is steerable since 4.8 follows instructions well — say *when* each capability applies, not just that it exists:

> *"Before any task longer than a few turns, check your memory file for relevant prior context and write new findings to it as you go. When a task fans out across independent items (many files to read, many tests to run, many candidates to check), delegate to subagents rather than iterating serially."*

The same lever works at the **tool-description** level, not just the system prompt: prescriptive descriptions that state *when* to call a tool (e.g. "Call this when the user asks about current prices or recent events") give meaningful lift on 4.8 over descriptions that only state what the tool does. Make the trigger condition part of each capability's own `description`.

**More user-facing narration.** 4.8 narrates more than 4.7 — more text between tool calls in long tool-calling sessions, and longer, more detailed end-of-task wrap-ups by default. If you previously added scaffolding to force interim status ("after every 3 tool calls, summarize progress"), **remove it** — 4.8 does this on its own. If the narration is too verbose for a coding agent, an explicit silence-default makes it behave like 4.7 with no loss of quality:

> *"Default to silence between tool calls. Only write text when you find something, change direction, or hit a blocker — one sentence each. Do not narrate routine actions ('Now I'll...', 'Let me check...', 'Looking at...'). When done: one or two sentences on the outcome. Do not recap every file or test — the user has been following along."*

For knowledge-work deliverables (reports, analysis readouts), verbosity responds very well to instructions in user preferences or the user turn — expose a verbosity preference rather than hard-coding a length.

**More deliberate — asks more often.** 4.8 is more deliberate than prior Opus models. On minor decisions it would previously just make (a variable name, a default value, which of two equivalent approaches), it tends to pause and ask, and it often closes a completed task with "Want me to also…?" rather than doing the obvious next step or stopping cleanly. This is preferred for high-stakes or unfamiliar codebases, but bugs users when uncalibrated. Grant autonomy on the small stuff while keeping caution where it matters (in Claude Code testing this cut ask-rate by ~12 percentage points with no increase in over-reach):

> *"For minor choices (naming, formatting, default values, which approach among equivalents), pick a reasonable option and note it rather than asking. For scope changes or destructive actions, still ask first."*

**Verbose reasoning when thinking is disabled.** With `thinking: {type: "disabled"}`, 4.8 occasionally writes longer explanations of its reasoning into the visible response, which reads as verbose when the user wants a fast, quick answer. The simplest fix is to leave adaptive thinking on — set `thinking: {type: "adaptive"}` (the recommended setting; it adjusts how much to think per task). Note adaptive is **not** on when the field is omitted — like Opus 4.7, a request with no `thinking` field runs without thinking, so set it explicitly. If you need thinking off for latency or cost, scope it in the system prompt:

> *"Respond only with your final answer. Do not include exploratory reasoning, intermediate drafts, diffs you considered but rejected, or meta-commentary about your process."*

### Opus 4.8 Migration Checklist

Every item is tagged: **`[BLOCKS]`** items cause a 400 error if missed; **`[TUNE]`** items are quality/cost adjustments — surface them to the user as recommendations.

For a caller **already on Opus 4.7**, only the first item is required; everything else is `[TUNE]`. The conditional `[BLOCKS]` item applies only when coming from Opus 4.6 or earlier.

- [ ] **[BLOCKS]** Update the `model=` string to `claude-opus-4-8`
- [ ] **[BLOCKS]** *(only if coming from Opus 4.6 or earlier)* Apply the **Migrating to Opus 4.7** breaking changes first — `budget_tokens` → adaptive thinking, strip `temperature`/`top_p`/`top_k`, remove last-assistant-turn prefills. These already 400 on 4.7 and continue to 400 on 4.8.
- [ ] **[TUNE]** Long-horizon / agentic work: put the full task spec in one well-specified first turn and run at `high` or `xhigh` effort (Claude Code: `/goal`; Managed Agents: an Outcome with a gradeable rubric)
- [ ] **[TUNE]** Effort: sweep `medium` / `high` / `xhigh` on your eval set and pick per route by the intelligence ↔ latency ↔ cost tradeoff (default `high`, `xhigh` for coding/agentic)
- [ ] **[TUNE]** Research depth & tool use: add a search-first instruction; add explicit triggering guidance for subagents, file-based memory, and custom tools (4.8 under-reaches for these by default) — in the system prompt *and* in each tool's own `description` (prescriptive "call this when…" descriptions give measurable lift)
- [ ] **[TUNE]** Narration: remove forced-progress scaffolding (*"after every N tool calls…"*); add a silence-default if a coding agent is too chatty
- [ ] **[TUNE]** Autonomy: add small-decisions-don't-ask guidance to cut ask-rate, while keeping caution on scope changes / destructive actions
- [ ] **[TUNE]** Writing voice: re-evaluate style prompts added to counter 4.7's directness — 4.8 is warmer and less hedged by default; re-baseline before keeping them
- [ ] **[TUNE]** Code-review harnesses: keep the report-everything-filter-downstream pattern (4.8 follows "only high-severity" / "be conservative" filters literally, which can depress measured recall)
- [ ] **[TUNE]** Thinking-disabled paths: add a final-answer-only instruction if reasoning leaks into the visible response
- [ ] **[TUNE]** Consider mid-session system messages (`role:"system"` in `messages`, beta `mid-conversation-system-2026-04-07`) for context the app learns mid-session, instead of rebuilding the top-level system prompt and invalidating the cache

---

## Verify the Migration

After updating, spot-check that the new model is actually being used. Replace `YOUR_TARGET_MODEL` with the model string you migrated to (e.g. `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`) and keep the assertion prefix in sync:

```python
YOUR_TARGET_MODEL = "claude-opus-4-8"  # or "claude-opus-4-7", "claude-sonnet-4-6", "claude-haiku-4-5"
response = client.messages.create(model=YOUR_TARGET_MODEL, max_tokens=64, messages=[...])
assert response.model.startswith(YOUR_TARGET_MODEL), response.model
```

For rate-limit headroom changes, pricing, or capability deltas (vision, structured outputs, effort support), query the Models API:

```python
m = client.models.retrieve(YOUR_TARGET_MODEL)
m.max_input_tokens, m.max_tokens
m.capabilities["effort"]["max"]["supported"]
```

See `shared/models.md` for the full capability lookup pattern.
</doc>

<doc path="shared/models.md">
# Claude Model Catalog

**Only use exact model IDs listed in this file.** Never guess or construct model IDs — incorrect IDs will cause API errors. Use aliases wherever available. For the latest information, WebFetch the Models Overview URL in `shared/live-sources.md`, or query the Models API directly (see Programmatic Model Discovery below).

## Programmatic Model Discovery

For **live** capability data — context window, max output tokens, feature support (thinking, vision, effort, structured outputs, etc.) — query the Models API instead of relying on the cached tables below. Use this when the user asks "what's the context window for X", "does model X support vision/thinking/effort", "which models support feature Y", or wants to select a model by capability at runtime.

```python
m = client.models.retrieve("claude-opus-4-8")
m.id                 # "claude-opus-4-8"
m.display_name       # "Claude Opus 4.8"
m.max_input_tokens   # context window (int)
m.max_tokens         # max output tokens (int)

# capabilities is an untyped nested dict — bracket access, check ["supported"] at the leaf
caps = m.capabilities
caps["image_input"]["supported"]                       # vision
caps["thinking"]["types"]["adaptive"]["supported"]     # adaptive thinking
caps["effort"]["max"]["supported"]                     # effort: max (also low/medium/high)
caps["structured_outputs"]["supported"]
caps["context_management"]["compact_20260112"]["supported"]

# filter across all models — iterate the page object directly (auto-paginates); do NOT use .data
[m for m in client.models.list()
 if m.capabilities["thinking"]["types"]["adaptive"]["supported"]
 and m.max_input_tokens >= 200_000]
```

Top-level fields (`id`, `display_name`, `max_input_tokens`, `max_tokens`) are typed attributes. `capabilities` is a dict — use bracket access, not attribute access. The API returns the full capability tree for every model with `supported: true/false` at each leaf, so bracket chains are safe without `.get()` guards. TypeScript SDK: same method names, also auto-paginates on iteration.

### Raw HTTP

```bash
curl https://api.anthropic.com/v1/models/claude-opus-4-8 \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

```json
{
  "id": "claude-opus-4-8",
  "display_name": "Claude Opus 4.8",
  "max_input_tokens": 1000000,
  "max_tokens": 128000,
  "capabilities": {
    "image_input": {"supported": true},
    "structured_outputs": {"supported": true},
    "thinking": {"supported": true, "types": {"enabled": {"supported": false}, "adaptive": {"supported": true}}},
    "effort": {"supported": true, "low": {"supported": true}, …, "max": {"supported": true}},
    …
  }
}
```

## Current Models (recommended)

| Friendly Name     | Alias (use this)    | Full ID                       | Context        | Max Output | Status |
|-------------------|---------------------|-------------------------------|----------------|------------|--------|
| Claude Fable 5    | `claude-fable-5`      | —                             | 1M             | 128K       | Active |
| Claude Opus 4.8   | `claude-opus-4-8`   | —                             | 1M             | 128K       | Active |
| Claude Opus 4.7   | `claude-opus-4-7`   | —                             | 1M             | 128K       | Active |
| Claude Opus 4.6   | `claude-opus-4-6`   | —                             | 1M             | 128K       | Active |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | -                             | 1M             | 64K        | Active |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | `claude-haiku-4-5-20251001`   | 200K           | 64K        | Active |

### Model Descriptions
- **Claude Fable 5** — Our most powerful, most intelligent model. New tier above Opus. Same API surface as Opus 4.7/4.8 (see `shared/model-migration.md`) with one new breaking change: an explicit `thinking: {type: "disabled"}` returns a 400 (omit the `thinking` param instead); $10/$50 per MTok.
- **Claude Opus 4.8** — The most capable Opus-tier model — highly autonomous, state-of-the-art on long-horizon agentic work, knowledge work, and memory; clearer, warmer writing. Same API surface as Opus 4.7 (adaptive thinking only; sampling parameters and `budget_tokens` removed). 1M context window at standard API pricing (no long-context premium). See `shared/model-migration.md` → Migrating to Opus 4.8 — a 4.7 → 4.8 move is a model-ID swap plus prompt re-tuning, no new breaking changes.
- **Claude Opus 4.7** — Previous-generation Opus. Highly autonomous; strong on long-horizon agentic work, knowledge work, vision, and memory. Adaptive thinking only; sampling parameters and `budget_tokens` removed. 1M context window. See `shared/model-migration.md` → Migrating to Opus 4.7.
- **Claude Opus 4.6** — Older Opus. Supports adaptive thinking (recommended), 128K max output tokens (requires streaming for large outputs). 1M context window.
- **Claude Sonnet 4.6** — Our best combination of speed and intelligence. Supports adaptive thinking (recommended). 1M context window. 64K max output tokens.
- **Claude Haiku 4.5** — Fastest and most cost-effective model for simple tasks.

## Legacy Models (still active)

| Friendly Name     | Alias (use this)    | Full ID                       | Status |
|-------------------|---------------------|-------------------------------|--------|
| Claude Opus 4.5   | `claude-opus-4-5`   | `claude-opus-4-5-20251101`    | Active |
| Claude Opus 4.1   | `claude-opus-4-1`   | `claude-opus-4-1-20250805`    | Active |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | `claude-sonnet-4-5-20250929`  | Active |

## Deprecated Models (retiring soon)

| Friendly Name     | Alias (use this)    | Full ID                       | Status     | Retires      |
|-------------------|---------------------|-------------------------------|------------|--------------|
| Claude Sonnet 4   | `claude-sonnet-4-0` | `claude-sonnet-4-20250514`    | Deprecated | TBD          |
| Claude Opus 4     | `claude-opus-4-0`   | `claude-opus-4-20250514`      | Deprecated | TBD          |
| Claude Haiku 3    | —                   | `claude-3-haiku-20240307`     | Deprecated | Apr 19, 2026 |

## Retired Models (no longer available)

| Friendly Name     | Full ID                       | Retired     |
|-------------------|-------------------------------|-------------|
| Claude Sonnet 3.7 | `claude-3-7-sonnet-20250219`  | Feb 19, 2026 |
| Claude Haiku 3.5  | `claude-3-5-haiku-20241022`   | Feb 19, 2026 |
| Claude Opus 3     | `claude-3-opus-20240229`      | Jan 5, 2026 |
| Claude Sonnet 3.5 | `claude-3-5-sonnet-20241022`  | Oct 28, 2025 |
| Claude Sonnet 3.5 | `claude-3-5-sonnet-20240620`  | Oct 28, 2025 |
| Claude Sonnet 3   | `claude-3-sonnet-20240229`    | Jul 21, 2025 |
| Claude 2.1        | `claude-2.1`                  | Jul 21, 2025 |
| Claude 2.0        | `claude-2.0`                  | Jul 21, 2025 |

## Resolving User Requests

When a user asks for a model by name, use this table to find the correct model ID:

| User says...                              | Use this model ID              |
|-------------------------------------------|--------------------------------|
| "fable"                                   | `claude-fable-5`                 |
| "most powerful"                           | `claude-fable-5`                 |
| "opus"                                    | `claude-opus-4-8`              |
| "opus 4.8"                                | `claude-opus-4-8`              |
| "opus 4.7"                                | `claude-opus-4-7`              |
| "opus 4.6"                                | `claude-opus-4-6`              |
| "opus 4.5"                                | `claude-opus-4-5`              |
| "opus 4.1"                                | `claude-opus-4-1`              |
| "opus 4", "opus 4.0"                      | `claude-opus-4-0` (deprecated — suggest `claude-opus-4-8`) |
| "sonnet", "balanced"                      | `claude-sonnet-4-6`            |
| "sonnet 4.6"                              | `claude-sonnet-4-6`            |
| "sonnet 4.5"                              | `claude-sonnet-4-5`            |
| "sonnet 4", "sonnet 4.0"                  | `claude-sonnet-4-0` (deprecated — suggest `claude-sonnet-4-6`) |
| "sonnet 3.7"                              | Retired — suggest `claude-sonnet-4-6` |
| "sonnet 3.5"                              | Retired — suggest `claude-sonnet-4-6` |
| "haiku", "fast", "cheap"                  | `claude-haiku-4-5`             |
| "haiku 4.5"                               | `claude-haiku-4-5`             |
| "haiku 3.5"                               | Retired — suggest `claude-haiku-4-5` |
| "haiku 3"                                 | Deprecated — suggest `claude-haiku-4-5` |
</doc>

<doc path="shared/prompt-caching.md">
# Prompt Caching — Design & Optimization

This file covers how to design prompt-building code for effective caching. For language-specific syntax, see the `## Prompt Caching` section in each language's README or single-file doc.

## The one invariant everything follows from

**Prompt caching is a prefix match. Any change anywhere in the prefix invalidates everything after it.**

The cache key is derived from the exact bytes of the rendered prompt up to each `cache_control` breakpoint. A single byte difference at position N — a timestamp, a reordered JSON key, a different tool in the list — invalidates the cache for all breakpoints at positions ≥ N.

Render order is: `tools` → `system` → `messages`. A breakpoint on the last system block caches both tools and system together.

Design the prompt-building path around this constraint. Get the ordering right and most caching works for free. Get it wrong and no amount of `cache_control` markers will help.

---

## Workflow for optimizing existing code

When asked to add or optimize caching:

1. **Trace the prompt assembly path.** Find where `system`, `tools`, and `messages` are constructed. Identify every input that flows into them.
2. **Classify each input by stability:**
   - Never changes → belongs early in the prompt, before any breakpoint
   - Changes per-session → belongs after the global prefix, cache per-session
   - Changes per-turn → belongs at the end, after the last breakpoint
   - Changes per-request (timestamps, UUIDs, random IDs) → **eliminate or move to the very end**
3. **Check rendered order matches stability order.** Stable content must physically precede volatile content. If a timestamp is interpolated into the system prompt header, everything after it is uncacheable regardless of markers.
4. **Place breakpoints at stability boundaries.** See placement patterns below.
5. **Audit for silent invalidators.** See anti-patterns table.

---

## Placement patterns

### Large system prompt shared across many requests

Put a breakpoint on the last system text block. If there are tools, they render before system — the marker on the last system block caches tools + system together.

```json
"system": [
  {"type": "text", "text": "<large shared prompt>", "cache_control": {"type": "ephemeral"}}
]
```

### Multi-turn conversations

Put a breakpoint on the last content block of the most-recently-appended turn. Each subsequent request reuses the entire prior conversation prefix. Earlier breakpoints remain valid read points, so hits accrue incrementally as the conversation grows.

```json
// Last content block of the last user turn
messages[-1].content[-1].cache_control = {"type": "ephemeral"}
```

### Shared prefix, varying suffix

Many requests share a large fixed preamble (few-shot examples, retrieved docs, instructions) but differ in the final question. Put the breakpoint at the end of the **shared** portion, not at the end of the whole prompt — otherwise every request writes a distinct cache entry and nothing is ever read.

```json
"messages": [{"role": "user", "content": [
  {"type": "text", "text": "<shared context>", "cache_control": {"type": "ephemeral"}},
  {"type": "text", "text": "<varying question>"}  // no marker — differs every time
]}]
```

### Mid-conversation system messages

**Beta, model-gated.** When an operator instruction arrives mid-conversation — a mode switch, updated context, dynamically injected state — send it as `{"role": "system", "content": "..."}` appended to `messages[]`, rather than editing top-level `system`. Editing top-level `system` changes the prefix ahead of the entire conversation history, so every cached turn is re-processed uncached; a `role: "system"` message sits after the history and leaves the cached prefix intact.

```json
// Top-level system stays byte-identical; new instruction goes after the cached history
"system": [{"type": "text", "text": "<stable core>", "cache_control": {"type": "ephemeral"}}],
"messages": [
  ...history,
  {"role": "user", "content": "..."},
  {"role": "system", "content": "Terse mode enabled — keep responses under 40 words."}
]
```

This is also the prompt-injection-safe replacement for embedding operator instructions as text inside a user turn (the `<system-reminder>` pattern): both have the same caching profile, but `role: "system"` is the non-spoofable operator channel, whereas text inside user/tool content can be forged by anything that writes to user-visible input.

Requires `anthropic-beta: mid-conversation-system-2026-04-07`. Must follow a `role: "user"` message (or an assistant message ending in a server tool result); cannot be `messages[0]` — use top-level `system` for the initial prompt. Content is text-only. Model-gated — unsupported models return a 400 (`BadRequestError`: `role 'system' is not supported on this model`); catch that error and fall back to putting the instruction in a user-turn `<system-reminder>` block.

### Prompts that change from the beginning every time

Don't cache. If the first 1K tokens differ per request, there is no reusable prefix. Adding `cache_control` only pays the cache-write premium with zero reads. Leave it off.

---

## Architectural guidance

These are the decisions that matter more than marker placement. Fix these first.

**Keep the system prompt frozen.** Don't interpolate "current date: X", "mode: Y", "user name: Z" into the system prompt — those sit at the front of the prefix and invalidate everything downstream. Inject dynamic context later in `messages` instead — as a `{"role": "system", ...}` message where supported (see § Mid-conversation system messages above), or as text in a user message otherwise. A message at turn 5 invalidates nothing before turn 5.

**Don't change tools or model mid-conversation.** Tools render at position 0; adding, removing, or reordering a tool invalidates the entire cache. Same for switching models (caches are model-scoped). If you need "modes", don't swap the tool set — give Claude a tool that records the mode transition, or pass the mode as message content. Serialize tools deterministically (sort by name).

**Fork operations must reuse the parent's exact prefix.** Side computations (summarization, compaction, sub-agents) often spin up a separate API call. If the fork rebuilds `system` / `tools` / `model` with any difference, it misses the parent's cache entirely. Copy the parent's `system`, `tools`, and `model` verbatim, then append fork-specific content at the end.

---

## Silent invalidators

When reviewing code, grep for these inside anything that feeds the prompt prefix:

| Pattern | Why it breaks caching |
|---|---|
| `datetime.now()` / `Date.now()` / `time.time()` in system prompt | Prefix changes every request |
| `uuid4()` / `crypto.randomUUID()` / request IDs early in content | Same — every request is unique |
| `json.dumps(d)` without `sort_keys=True` / iterating a `set` | Non-deterministic serialization → prefix bytes differ |
| f-string interpolating session/user ID into system prompt | Per-user prefix; no cross-user sharing |
| Conditional system sections (`if flag: system += ...`) | Every flag combination is a distinct prefix |
| `tools=build_tools(user)` where set varies per user | Tools render at position 0; nothing caches across users |

Fix by moving the dynamic piece after the last breakpoint, making it deterministic, or deleting it if it's not load-bearing.

---

## API reference

```json
"cache_control": {"type": "ephemeral"}              // 5-minute TTL (default)
"cache_control": {"type": "ephemeral", "ttl": "1h"} // 1-hour TTL
```

- Max **4** `cache_control` breakpoints per request.
- Goes on any content block: system text blocks, tool definitions, message content blocks (`text`, `image`, `tool_use`, `tool_result`, `document`).
- Top-level `cache_control` on `messages.create()` auto-places on the last cacheable block — simplest option when you don't need fine-grained placement.
- Minimum cacheable prefix is model-dependent. Shorter prefixes silently won't cache even with a marker — no error, just `cache_creation_input_tokens: 0`:

| Model | Minimum |
|---|---:|
| Opus 4.8, Opus 4.7, Opus 4.6, Opus 4.5, Haiku 4.5 | 4096 tokens |
| Fable 5, Sonnet 4.6, Haiku 3.5, Haiku 3 | 2048 tokens |
| Sonnet 4.5, Sonnet 4.1, Sonnet 4, Sonnet 3.7 | 1024 tokens |

A 3K-token prompt caches on Sonnet 4.5 and Fable 5 but silently won't on Opus 4.8.

**Economics:** Cache reads cost ~0.1× base input price. Cache writes cost **1.25× for 5-minute TTL, 2× for 1-hour TTL**. Break-even depends on TTL: with 5-minute TTL, two requests break even (1.25× + 0.1× = 1.35× vs 2× uncached); with 1-hour TTL, you need at least three requests (2× + 0.2× = 2.2× vs 3× uncached). The 1-hour TTL keeps entries alive across gaps in bursty traffic, but the doubled write cost means it needs more reads to pay off.

---

## Verifying cache hits

The response `usage` object reports cache activity:

| Field | Meaning |
|---|---|
| `cache_creation_input_tokens` | Tokens written to cache this request (you paid the ~1.25× write premium) |
| `cache_read_input_tokens` | Tokens served from cache this request (you paid ~0.1×) |
| `input_tokens` | Tokens processed at full price (not cached) |

If `cache_read_input_tokens` is zero across repeated requests with identical prefixes, a silent invalidator is at work — diff the rendered prompt bytes between two requests to find it.

**`input_tokens` is the uncached remainder only.** Total prompt size = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. If your agent ran for hours but `input_tokens` shows 4K, the rest was served from cache — check the sum, not the single field.

Language-specific access: `response.usage.cache_read_input_tokens` (Python/TS/Ruby), `$message->usage->cacheReadInputTokens` (PHP), `resp.Usage.CacheReadInputTokens` (Go/C#), `.usage().cacheReadInputTokens()` (Java).

---

## Invalidation hierarchy

Not every parameter change invalidates everything. The API has three cache tiers, and changes only invalidate their own tier and below:

| Change | Tools cache | System cache | Messages cache |
|---|:---:|:---:|:---:|
| Tool definitions (add/remove/reorder) | ❌ | ❌ | ❌ |
| Model switch | ❌ | ❌ | ❌ |
| `speed`, web-search, citations toggle | ✅ | ❌ | ❌ |
| System prompt content | ✅ | ❌ | ❌ |
| `tool_choice`, images, `thinking` enable/disable | ✅ | ✅ | ❌ |
| Message content | ✅ | ✅ | ❌ |

Implication: you can change `tool_choice` per-request or toggle `thinking` without losing the tools+system cache. Don't over-worry about these — only tool-definition and model changes force a full rebuild.

---

## 20-block lookback window

Each breakpoint walks backward **at most 20 content blocks** to find a prior cache entry. If a single turn adds more than 20 blocks (common in agentic loops with many tool_use/tool_result pairs), the next request's breakpoint won't find the previous cache and silently misses.

Fix: place an intermediate breakpoint every ~15 blocks in long turns, or put the marker on a block that's within 20 of the previous turn's last cached block.

---

## Concurrent-request timing

A cache entry becomes readable only after the first response **begins streaming**. N parallel requests with identical prefixes all pay full price — none can read what the others are still writing.

For fan-out patterns: send 1 request, await the first streamed token (not the full response), then fire the remaining N−1. They'll read the cache the first one just wrote.

## Pre-warming the cache

To eliminate the cache-miss latency on the *first* real request, send a **`max_tokens: 0`** request at startup (or on an interval). The API runs prefill — writing the cache at your `cache_control` breakpoint — and returns immediately with `content: []`, `stop_reason: "max_tokens"`, and a populated `usage` block (zero output tokens billed; normal cache-write charge on `cache_creation_input_tokens`).

**When to pre-warm** — pre-warming trades a cache-write charge *now* for lower TTFT on the *next* real request. It's worth it when all three hold: (a) first-request latency is user-visible (chat/voice/interactive — not background jobs), (b) the shared prefix is large enough that a cold write is noticeably slow, and (c) there's a moment *before* traffic to fire it — app startup, worker boot, post-deploy, start of a scheduled window.

| Skip pre-warming when… | Because |
|---|---|
| Traffic is continuous (requests ≤ TTL apart) | The first real request warms the cache and every subsequent one hits it; a separate warm call is a pure extra write |
| The prefix is small or below the cacheable minimum | The cold-write penalty is negligible |
| The prefix varies per request/user | Nothing shared to pre-warm |
| You'd pre-warm many distinct prefixes speculatively | Each is a ~1.25× write; cost can exceed the latency you save |

**Scheduled re-warms:** only needed when traffic has gaps longer than the TTL. If real requests arrive more often than every 5 minutes, they keep the cache warm on their own — don't add an interval re-warm. For bursty traffic with long idle gaps, either re-warm just under the TTL or switch to `ttl: "1h"` and re-warm less often.

```python
client.messages.create(
    model="claude-opus-4-8",
    max_tokens=0,
    system=[{
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": "warmup"}],
)
```

**Breakpoint placement:** put `cache_control` on the **last block shared with the real request** (the system prompt or tool definitions) — **not** on the placeholder user message, and **not** via top-level automatic caching (which would key the cache to the placeholder). The placeholder can be any non-whitespace string; it's read during prefill but never answered.

**Rejected combinations:** `max_tokens: 0` is an `invalid_request_error` with `stream: true`, `thinking.type: "enabled"`, `output_config.format`, `tool_choice` of `{"type":"tool"}` or `{"type":"any"}`, or inside a Message Batches request.

**TTL still applies** — re-warm at least every 5 minutes for the default cache, or use the 1-hour TTL. This replaces the older `max_tokens: 1` workaround (no single-token reply to discard, no output tokens billed, intent is unambiguous).
</doc>

<doc path="shared/token-counting.md">
# Token Counting

Use the `count_tokens` endpoint (`POST /v1/messages/count_tokens`) for accurate
token counts against Claude models. Token counts are **model-specific** — pass
the same model ID you'll use for inference.

**Do not use `tiktoken`.** It's OpenAI's tokenizer. It undercounts Claude
tokens by ~15–20% on typical text, and by much more on code or non-English
input. Any estimate from `tiktoken`, `gpt-tokenizer`, or similar is wrong for
Claude.

## Count a file or string

```python
from anthropic import Anthropic

client = Anthropic()
resp = client.messages.count_tokens(
    model="claude-opus-4-8",
    messages=[{"role": "user", "content": open("CLAUDE.md").read()}],
)
print(resp.input_tokens)
```

TypeScript: `await client.messages.countTokens({model, messages})` →
`.input_tokens`. See `{lang}/claude-api/README.md` for other SDKs.

## CLI

```sh
ant messages count-tokens --model claude-opus-4-8 \
  --message '{role: user, content: "@./CLAUDE.md"}' \
  --transform input_tokens -r
```

## Diffing a file across two versions

The endpoint is stateless — count each version separately and subtract:

```python
from anthropic import Anthropic
import subprocess

client = Anthropic()
def count(text: str) -> int:
    return client.messages.count_tokens(
        model="claude-opus-4-8",
        messages=[{"role": "user", "content": text}],
    ).input_tokens

before = subprocess.check_output(["git", "show", "HEAD:CLAUDE.md"], text=True)
after = open("CLAUDE.md").read()
print(count(after) - count(before))
```

Full docs: see the Token Counting entry in `shared/live-sources.md`.
</doc>

<doc path="shared/tool-use-concepts.md">
# Tool Use Concepts

This file covers the conceptual foundations of tool use with the Claude API. For language-specific code examples, see the `python/`, `typescript/`, or other language folders. For decision heuristics on which tools to expose, how to manage context in long-running agents, and caching strategy, see `agent-design.md`.

## User-Defined Tools

### Tool Definition Structure

> **Note:** When using the Tool Runner (beta), tool schemas are generated automatically from your function signatures (Python), Zod schemas (TypeScript), annotated classes (Java), `jsonschema` struct tags (Go), or `BaseTool` subclasses (Ruby). The raw JSON schema format below is for the manual approach — including PHP's `BetaRunnableTool`, which wraps a run closure around a hand-written schema — or SDKs without tool runner support.

Each tool requires a name, description, and JSON Schema for its inputs:

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City and state, e.g., San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "Temperature unit"
      }
    },
    "required": ["location"]
  }
}
```

**Best practices for tool definitions:**

- Use clear, descriptive names (e.g., `get_weather`, `search_database`, `send_email`)
- Write detailed descriptions — Claude uses these to decide when to use the tool. Be **prescriptive about *when* to call it**, not just what it does (e.g. "Call this when the user asks about current prices or recent events"). On recent Opus models, which reach for tools more conservatively, trigger conditions in the description give measurable lift in should-call rate.
- Include descriptions for each property
- Use `enum` for parameters with a fixed set of values
- Mark truly required parameters in `required`; make others optional with defaults

---

### Tool Choice Options

Control when Claude uses tools:

| Value                             | Behavior                                      |
| --------------------------------- | --------------------------------------------- |
| `{"type": "auto"}`                | Claude decides whether to use tools (default) |
| `{"type": "any"}`                 | Claude must use at least one tool             |
| `{"type": "tool", "name": "..."}` | Claude must use the specified tool            |
| `{"type": "none"}`                | Claude cannot use tools                       |

Any `tool_choice` value can also include `"disable_parallel_tool_use": true` to force Claude to use at most one tool per response. By default, Claude may request multiple tool calls in a single response.

---

### Tool Runner vs Manual Loop

**Tool Runner (Recommended):** The SDK's tool runner handles the agentic loop automatically — it calls the API, detects tool use requests, executes your tool functions, feeds results back to Claude, and repeats until Claude stops calling tools. Available in Python, TypeScript, Java, Go, Ruby, and PHP SDKs (beta). The Python SDK also provides MCP conversion helpers (`anthropic.lib.tools.mcp`) to convert MCP tools, prompts, and resources for use with the tool runner — see `python/claude-api/tool-use.md` for details.

**Manual Agentic Loop:** Use when you need fine-grained control over the loop (e.g., custom logging, conditional tool execution, human-in-the-loop approval). Loop until `stop_reason == "end_turn"`, always append the full `response.content` to preserve tool_use blocks, and ensure each `tool_result` includes the matching `tool_use_id`.

**Stop reasons for server-side tools:** When using server-side tools (code execution, web search, etc.), the API runs a server-side sampling loop. If this loop reaches its default limit of 10 iterations, the response will have `stop_reason: "pause_turn"`. To continue, re-send the user message and assistant response and make another API request — the server will resume where it left off. Do NOT add an extra user message like "Continue." — the API detects the trailing `server_tool_use` block and knows to resume automatically.

```python
# Handle pause_turn in your agentic loop
if response.stop_reason == "pause_turn":
    messages = [
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": response.content},
    ]
    # Make another API request — server resumes automatically
    response = client.messages.create(
        model="claude-opus-4-8", messages=messages, tools=tools
    )
```

Set a `max_continuations` limit (e.g., 5) to prevent infinite loops. For the full guide, see: `https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons`

> **Security:** The tool runner executes your tool functions automatically whenever Claude requests them. For tools with side effects (sending emails, modifying databases, financial transactions), validate inputs within your tool functions and consider requiring confirmation for destructive operations. Use the manual agentic loop if you need human-in-the-loop approval before each tool execution.

---

### Handling Tool Results

When Claude uses a tool, the response contains a `tool_use` block. You must:

1. Execute the tool with the provided input
2. Send the result back in a `tool_result` message
3. Continue the conversation

**Error handling in tool results:** When a tool execution fails, set `"is_error": true` and provide an informative error message. Claude will typically acknowledge the error and either try a different approach or ask for clarification.

**Multiple tool calls:** Claude can request multiple tools in a single response. Handle them all before continuing — send all results back in a single `user` message.

---

## Server-Side Tools: Code Execution

The code execution tool lets Claude run code in a secure, sandboxed container. Unlike user-defined tools, server-side tools run on Anthropic's infrastructure — you don't execute anything client-side. Just include the tool definition and Claude handles the rest.

### Key Facts

- Runs in an isolated container (1 CPU, 5 GiB RAM, 5 GiB disk)
- No internet access (fully sandboxed)
- Python 3.11 with data science libraries pre-installed
- Containers persist for 30 days and can be reused across requests
- Free when used with web search/web fetch tools; otherwise $0.05/hour after 1,550 free hours/month per organization

### Tool Definition

The tool requires no schema — just declare it in the `tools` array:

```json
{
  "type": "code_execution_20260120",
  "name": "code_execution"
}
```

Claude automatically gains access to `bash_code_execution` (run shell commands) and `text_editor_code_execution` (create/view/edit files).

### Pre-installed Python Libraries

- **Data science**: pandas, numpy, scipy, scikit-learn, statsmodels
- **Visualization**: matplotlib, seaborn
- **File processing**: openpyxl, xlsxwriter, pillow, pypdf, pdfplumber, python-docx, python-pptx
- **Math**: sympy, mpmath
- **Utilities**: tqdm, python-dateutil, pytz, sqlite3

Additional packages can be installed at runtime via `pip install`.

### Supported File Types for Upload

| Type   | Extensions                         |
| ------ | ---------------------------------- |
| Data   | CSV, Excel (.xlsx/.xls), JSON, XML |
| Images | JPEG, PNG, GIF, WebP               |
| Text   | .txt, .md, .py, .js, etc.          |

### Container Reuse

Reuse containers across requests to maintain state (files, installed packages, variables). Extract the `container_id` from the first response and pass it to subsequent requests.

### Response Structure

The response contains interleaved text and tool result blocks:

- `text` — Claude's explanation
- `server_tool_use` — What Claude is doing
- `bash_code_execution_tool_result` — Code execution output (check `return_code` for success/failure)
- `text_editor_code_execution_tool_result` — File operation results

> **Security:** Always sanitize filenames with `os.path.basename()` / `path.basename()` before writing downloaded files to disk to prevent path traversal attacks. Write files to a dedicated output directory.

---

## Server-Side Tools: Web Search and Web Fetch

Web search and web fetch let Claude search the web and retrieve page content. They run server-side — just include the tool definitions and Claude handles queries, fetching, and result processing automatically.

### Tool Definitions

```json
[
  { "type": "web_search_20260209", "name": "web_search" },
  { "type": "web_fetch_20260209", "name": "web_fetch" }
]
```

### Dynamic Filtering (Fable 5 / Opus 4.8 / Opus 4.7 / Opus 4.6 / Sonnet 4.6)

The `web_search_20260209` and `web_fetch_20260209` versions support **dynamic filtering** — Claude writes and executes code to filter search results before they reach the context window, improving accuracy and token efficiency. Dynamic filtering is built into these tool versions and activates automatically; you do not need to separately declare the `code_execution` tool or pass any beta header.

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "web_fetch_20260209", "name": "web_fetch" }
  ]
}
```

Without dynamic filtering, the previous `web_search_20250305` version is also available.

> **Note:** Only include the standalone `code_execution` tool when your application needs code execution for its own purposes (data analysis, file processing, visualization) independent of web search. Including it alongside `_20260209` web tools creates a second execution environment that can confuse the model.

---

## Server-Side Tools: Programmatic Tool Calling

With standard tool use, each tool call is a round trip: Claude calls, the result enters Claude's context, Claude reasons, then calls the next tool. Chained calls accumulate latency and tokens — most of that intermediate data is never needed again.

Programmatic tool calling lets Claude compose those calls into a script. The script runs in the code execution container; when it invokes a tool, the container pauses, the call executes, and the result returns to the running code (not to Claude's context). The script processes it with normal control flow. Only the final output returns to Claude. Use it when chaining many tool calls or when intermediate results are large and should be filtered before reaching the context window.

For full documentation, use WebFetch:

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling`

---

## Server-Side Tools: Tool Search

The tool search tool lets Claude dynamically discover tools from large libraries without loading all definitions into the context window. Use it when you have many tools but only a few are relevant to any given request. Discovered tool schemas are appended to the request, not swapped in — this preserves the prompt cache (see `agent-design.md` §Caching for Agents).

For full documentation, use WebFetch:

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool`

---

## Skills

Skills package task-specific instructions that Claude loads only when relevant. Each skill is a folder containing a `SKILL.md` file. The skill's short description sits in context by default; Claude reads the full file when the current task calls for it. Use skills to keep specialized instructions out of the base system prompt without losing discoverability.

For full documentation, use WebFetch:

- URL: `https://platform.claude.com/docs/en/agents-and-tools/skills`

---

## Tool Use Examples

You can provide sample tool calls directly in your tool definitions to demonstrate usage patterns and reduce parameter errors. This helps Claude understand how to correctly format tool inputs, especially for tools with complex schemas.

For full documentation, use WebFetch:

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use`

---

## Server-Side Tools: Computer Use

Computer use lets Claude interact with a desktop environment (screenshots, mouse, keyboard). It can be Anthropic-hosted (server-side, like code execution) or self-hosted (you provide the environment and execute actions client-side).

For full documentation, use WebFetch:

- URL: `https://platform.claude.com/docs/en/agents-and-tools/computer-use/overview`

---

## Context Editing

Context editing clears stale tool results and thinking blocks from the transcript as a long-running agent accumulates turns. Unlike compaction (which summarizes), context editing prunes — the cleared content is removed, not replaced. Use it when old tool outputs are no longer relevant and you want to keep the transcript lean without losing the conversation structure. Thresholds for what to clear are configurable.

For full documentation, use WebFetch:

- URL: `https://platform.claude.com/docs/en/build-with-claude/context-editing`

---

## Server-Side Tools: Advisor (Beta)

The advisor tool lets Claude consult a secondary model during a conversation. The advisor runs its own API call with a model you specify and returns its analysis to the primary model. Use it when you want a second opinion, specialized expertise, or cross-model verification without managing the orchestration yourself.

### Tool Definition

```json
{
  "type": "advisor_20260301",
  "name": "advisor",
  "model": "claude-sonnet-4-6"
}
```

The `model` parameter is required — it specifies which model the advisor uses for its own inference. Optional fields: `caching`, `max_uses`, `allowed_callers`, `defer_loading`, `strict`.

**Beta header required:** `advisor-tool-2026-03-01`. The SDK sets this automatically when using `client.beta.messages.create()` with advisor tools.

---

## Client-Side Tools: Memory

The memory tool enables Claude to store and retrieve information across conversations through a memory file directory. Claude can create, read, update, and delete files that persist between sessions.

### Key Facts

- Client-side tool — you control storage via your implementation
- Supports commands: `view`, `create`, `str_replace`, `insert`, `delete`, `rename`
- Operates on files in a `/memories` directory
- The Python, TypeScript, and Java SDKs provide helper classes/functions for implementing the memory backend

> **Security:** Never store API keys, passwords, tokens, or other secrets in memory files. Be cautious with personally identifiable information (PII) — check data privacy regulations (GDPR, CCPA) before persisting user data. The reference implementations have no built-in access control; in multi-user systems, implement per-user memory directories and authentication in your tool handlers.

For full implementation examples, use WebFetch:

- Docs: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md`

---

## Structured Outputs

Structured outputs constrain Claude's responses to follow a specific JSON schema, guaranteeing valid, parseable output. This is not a separate tool — it enhances the Messages API response format and/or tool parameter validation.

Two features are available:

- **JSON outputs** (`output_config.format`): Control Claude's response format
- **Strict tool use** (`strict: true`): Guarantee valid tool parameter schemas

**Supported models:** Claude Fable 5, Claude Opus 4.8, Claude Sonnet 4.6, and Claude Haiku 4.5. Legacy models (Claude Opus 4.5, Claude Opus 4.1) also support structured outputs.

> **Recommended:** Use `client.messages.parse()` which automatically validates responses against your schema. When using `messages.create()` directly, use `output_config: {format: {...}}`. The `output_format` convenience parameter is also accepted by some SDK methods (e.g., `.parse()`), but `output_config.format` is the canonical API-level parameter.

### JSON Schema Limitations

**Supported:**

- Basic types: object, array, string, integer, number, boolean, null
- `enum`, `const`, `anyOf`, `allOf`, `$ref`/`$def`
- String formats: `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`
- `additionalProperties: false` (required for all objects)

**Not supported:**

- Recursive schemas
- Numerical constraints (`minimum`, `maximum`, `multipleOf`)
- String constraints (`minLength`, `maxLength`)
- Complex array constraints
- `additionalProperties` set to anything other than `false`

The Python and TypeScript SDKs automatically handle unsupported constraints by removing them from the schema sent to the API and validating them client-side.

### Important Notes

- **First request latency**: New schemas incur a one-time compilation cost. Subsequent requests with the same schema use a 24-hour cache.
- **Refusals**: If Claude refuses for safety reasons (`stop_reason: "refusal"`), the output may not match your schema.
- **Token limits**: If `stop_reason: "max_tokens"`, output may be incomplete. Increase `max_tokens`.
- **Incompatible with**: Citations (returns 400 error), message prefilling.
- **Works with**: Batches API, streaming, token counting, extended thinking.

---

## Tips for Effective Tool Use

1. **Provide detailed descriptions**: Claude relies heavily on descriptions to understand when and how to use tools
2. **Use specific tool names**: `get_current_weather` is better than `weather`
3. **Validate inputs**: Always validate tool inputs before execution
4. **Handle errors gracefully**: Return informative error messages so Claude can adapt
5. **Limit tool count**: Too many tools can confuse the model — keep the set focused
6. **Test tool interactions**: Verify Claude uses tools correctly in various scenarios

For detailed tool use documentation, use WebFetch:

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview`
</doc>

<doc path="typescript/claude-api/README.md">
# Claude API — TypeScript

## Installation

```bash
npm install @anthropic-ai/sdk
```

## Client Initialization

```typescript
import Anthropic from "@anthropic-ai/sdk";

// Default — resolves credentials from the environment:
// ANTHROPIC_API_KEY, or ANTHROPIC_AUTH_TOKEN, or an `ant auth login` profile.
// Prefer this for local dev; don't hardcode a key.
const client = new Anthropic();

// Explicit API key (only when you must inject a specific key)
const client = new Anthropic({ apiKey: "your-api-key" });
```

---

## Basic Message Request

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [{ role: "user", content: "What is the capital of France?" }],
});
// response.content is ContentBlock[] — a discriminated union. Narrow by .type
// before accessing .text (TypeScript will error on content[0].text without this).
for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

---

## System Prompts

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  system:
    "You are a helpful coding assistant. Always provide examples in Python.",
  messages: [{ role: "user", content: "How do I read a JSON file?" }],
});
```

### Mid-conversation system messages (beta, model-gated)

For operator instructions that arrive mid-conversation (mode switches, injected state), append `{role: "system", ...}` to `messages` instead of editing top-level `system` — this preserves the cached prefix and carries operator authority. Must follow a user message; cannot be `messages[0]`. Unsupported models return a 400 (`role 'system' is not supported on this model`). See `shared/prompt-caching.md` for when to use this vs. top-level `system`.

```typescript
// SDK types for role:"system" in messages are pending — pass the beta header
// directly until the SDK updates, then switch to client.beta.messages.create
// with betas: ["mid-conversation-system-2026-04-07"].
const response = await client.messages.create(
  {
    model: MODEL_ID, // must support mid-conversation system messages
    max_tokens: 16000,
    system: [
      { type: "text", text: STABLE_SYSTEM, cache_control: { type: "ephemeral" } },
    ],
    messages: [
      ...history,
      { role: "user", content: userMessage },
      // @ts-expect-error — role:"system" pending SDK types
      { role: "system", content: "Terse mode enabled — keep responses under 40 words." },
    ],
  },
  { headers: { "anthropic-beta": "mid-conversation-system-2026-04-07" } },
);
```

---

## Vision (Images)

### URL

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: { type: "url", url: "https://example.com/image.png" },
        },
        { type: "text", text: "Describe this image" },
      ],
    },
  ],
});
```

### Base64

```typescript
import fs from "fs";

const imageData = fs.readFileSync("image.png").toString("base64");

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: { type: "base64", media_type: "image/png", data: imageData },
        },
        { type: "text", text: "What's in this image?" },
      ],
    },
  ],
});
```

---

## Prompt Caching

**Caching is a prefix match** — any byte change anywhere in the prefix invalidates everything after it. For placement patterns, architectural guidance (frozen system prompt, deterministic tool order, where to put volatile content), and the silent-invalidator audit checklist, read `shared/prompt-caching.md`.

### Automatic Caching (Recommended)

Use top-level `cache_control` to automatically cache the last cacheable block in the request:

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  cache_control: { type: "ephemeral" }, // auto-caches the last cacheable block
  system: "You are an expert on this large document...",
  messages: [{ role: "user", content: "Summarize the key points" }],
});
```

### Manual Cache Control

For fine-grained control, add `cache_control` to specific content blocks:

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  system: [
    {
      type: "text",
      text: "You are an expert on this large document...",
      cache_control: { type: "ephemeral" }, // default TTL is 5 minutes
    },
  ],
  messages: [{ role: "user", content: "Summarize the key points" }],
});

// With explicit TTL (time-to-live)
const response2 = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  system: [
    {
      type: "text",
      text: "You are an expert on this large document...",
      cache_control: { type: "ephemeral", ttl: "1h" }, // 1 hour TTL
    },
  ],
  messages: [{ role: "user", content: "Summarize the key points" }],
});
```

### Verifying Cache Hits

```typescript
console.log(response.usage.cache_creation_input_tokens); // tokens written to cache (~1.25x cost)
console.log(response.usage.cache_read_input_tokens);     // tokens served from cache (~0.1x cost)
console.log(response.usage.input_tokens);                // uncached tokens (full cost)
```

If `cache_read_input_tokens` is zero across repeated identical-prefix requests, a silent invalidator is at work — `Date.now()` or a UUID in the system prompt, non-deterministic key ordering, or a varying tool set. See `shared/prompt-caching.md` for the full audit table.

---

## Extended Thinking

> **Fable 5, Opus 4.8, Opus 4.7, Opus 4.6, and Sonnet 4.6:** Use adaptive thinking. `budget_tokens` is removed on Fable 5, Opus 4.8, and 4.7 (400 if sent); deprecated on Opus 4.6 and Sonnet 4.6.
> **Older models:** Use `thinking: {type: "enabled", budget_tokens: N}` (must be < `max_tokens`, min 1024).

```typescript
// Fable 5 / Opus 4.8 / 4.7 / 4.6: adaptive thinking (recommended)
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  output_config: { effort: "high" }, // low | medium | high | max
  messages: [
    { role: "user", content: "Solve this math problem step by step..." },
  ],
});

for (const block of response.content) {
  if (block.type === "thinking") {
    console.log("Thinking:", block.thinking);
  } else if (block.type === "text") {
    console.log("Response:", block.text);
  }
}
```

---

## Error Handling

Use the SDK's typed exception classes — never check error messages with string matching:

```typescript
import Anthropic from "@anthropic-ai/sdk";

try {
  const response = await client.messages.create({...});
} catch (error) {
  if (error instanceof Anthropic.BadRequestError) {
    console.error("Bad request:", error.message);
  } else if (error instanceof Anthropic.AuthenticationError) {
    console.error("Invalid API key");
  } else if (error instanceof Anthropic.RateLimitError) {
    console.error("Rate limited - retry later");
  } else if (error instanceof Anthropic.APIError) {
    console.error(`API error ${error.status}:`, error.message);
  }
}
```

All classes extend `Anthropic.APIError` with a typed `status` field. Check from most specific to least specific. See [shared/error-codes.md](../../shared/error-codes.md) for the full error code reference.

---

## Multi-Turn Conversations

The API is stateless — send the full conversation history each time. Use `Anthropic.MessageParam[]` to type the messages array:

```typescript
const messages: Anthropic.MessageParam[] = [
  { role: "user", content: "My name is Alice." },
  { role: "assistant", content: "Hello Alice! Nice to meet you." },
  { role: "user", content: "What's my name?" },
];

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: messages,
});
```

**Rules:**

- Consecutive same-role messages are allowed — the API combines them into a single turn
- First message must be `user`
- Use SDK types (`Anthropic.MessageParam`, `Anthropic.Message`, `Anthropic.Tool`, etc.) for all API data structures — don't redefine equivalent interfaces

---

### Compaction (long conversations)

> **Beta, Fable 5, Opus 4.8, Opus 4.7, Opus 4.6, and Sonnet 4.6.** When conversations approach the 200K context window, compaction automatically summarizes earlier context server-side. The API returns a `compaction` block; you must pass it back on subsequent requests — append `response.content`, not just the text.

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const messages: Anthropic.Beta.BetaMessageParam[] = [];

async function chat(userMessage: string): Promise<string> {
  messages.push({ role: "user", content: userMessage });

  const response = await client.beta.messages.create({
    betas: ["compact-2026-01-12"],
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages,
    context_management: {
      edits: [{ type: "compact_20260112" }],
    },
  });

  // Append full content — compaction blocks must be preserved
  messages.push({ role: "assistant", content: response.content });

  const textBlock = response.content.find(
    (b): b is Anthropic.Beta.BetaTextBlock => b.type === "text",
  );
  return textBlock?.text ?? "";
}

// Compaction triggers automatically when context grows large
console.log(await chat("Help me build a Python web scraper"));
console.log(await chat("Add support for JavaScript-rendered pages"));
console.log(await chat("Now add rate limiting and error handling"));
```

---

## Stop Reasons

The `stop_reason` field in the response indicates why the model stopped generating:

| Value           | Meaning                                                         |
| --------------- | --------------------------------------------------------------- |
| `end_turn`      | Claude finished its response naturally                          |
| `max_tokens`    | Hit the `max_tokens` limit — increase it or use streaming       |
| `stop_sequence` | Hit a custom stop sequence                                      |
| `tool_use`      | Claude wants to call a tool — execute it and continue           |
| `pause_turn`    | Model paused and can be resumed (agentic flows)                 |
| `refusal`       | Claude refused for safety reasons — check `stop_details`        |

### Structured Stop Details

When `stop_reason` is `"refusal"`, the response includes a `stop_details` object with structured information about the refusal:

```typescript
if (response.stop_reason === "refusal" && response.stop_details) {
  console.log(`Category: ${response.stop_details.category}`); // "cyber" | "bio" | null
  console.log(`Explanation: ${response.stop_details.explanation}`);
}
```

---

## Cost Optimization Strategies

### 1. Use Prompt Caching for Repeated Context

```typescript
// Automatic caching (simplest — caches the last cacheable block)
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  cache_control: { type: "ephemeral" },
  system: largeDocumentText, // e.g., 50KB of context
  messages: [{ role: "user", content: "Summarize the key points" }],
});

// First request: full cost
// Subsequent requests: ~90% cheaper for cached portion
```

### 2. Use Token Counting Before Requests

```typescript
const countResponse = await client.messages.countTokens({
  model: "claude-opus-4-8",
  messages: messages,
  system: system,
});

const estimatedInputCost = countResponse.input_tokens * 0.000005; // $5/1M tokens
console.log(`Estimated input cost: $${estimatedInputCost.toFixed(4)}`);
```
</doc>

<doc path="typescript/claude-api/batches.md">
# Message Batches API — TypeScript

The Batches API (`POST /v1/messages/batches`) processes Messages API requests asynchronously at 50% of standard prices.

## Key Facts

- Up to 100,000 requests or 256 MB per batch
- Most batches complete within 1 hour; maximum 24 hours
- Results available for 29 days after creation
- 50% cost reduction on all token usage
- All Messages API features supported (vision, tools, caching, etc.)

---

## Create a Batch

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const messageBatch = await client.messages.batches.create({
  requests: [
    {
      custom_id: "request-1",
      params: {
        model: "claude-opus-4-8",
        max_tokens: 16000,
        messages: [
          { role: "user", content: "Summarize climate change impacts" },
        ],
      },
    },
    {
      custom_id: "request-2",
      params: {
        model: "claude-opus-4-8",
        max_tokens: 16000,
        messages: [
          { role: "user", content: "Explain quantum computing basics" },
        ],
      },
    },
  ],
});

console.log(`Batch ID: ${messageBatch.id}`);
console.log(`Status: ${messageBatch.processing_status}`);
```

---

## Poll for Completion

```typescript
let batch;
while (true) {
  batch = await client.messages.batches.retrieve(messageBatch.id);
  if (batch.processing_status === "ended") break;
  console.log(
    `Status: ${batch.processing_status}, processing: ${batch.request_counts.processing}`,
  );
  await new Promise((resolve) => setTimeout(resolve, 60_000));
}

console.log("Batch complete!");
console.log(`Succeeded: ${batch.request_counts.succeeded}`);
console.log(`Errored: ${batch.request_counts.errored}`);
```

---

## Retrieve Results

```typescript
for await (const result of await client.messages.batches.results(
  messageBatch.id,
)) {
  switch (result.result.type) {
    case "succeeded":
      console.log(
        `[${result.custom_id}] ${result.result.message.content[0].text.slice(0, 100)}`,
      );
      break;
    case "errored":
      if (result.result.error.type === "invalid_request") {
        console.log(`[${result.custom_id}] Validation error - fix and retry`);
      } else {
        console.log(`[${result.custom_id}] Server error - safe to retry`);
      }
      break;
    case "expired":
      console.log(`[${result.custom_id}] Expired - resubmit`);
      break;
  }
}
```

---

## Cancel a Batch

```typescript
const cancelled = await client.messages.batches.cancel(messageBatch.id);
console.log(`Status: ${cancelled.processing_status}`); // "canceling"
```
</doc>

<doc path="typescript/claude-api/files-api.md">
# Files API — TypeScript

The Files API uploads files for use in Messages API requests. Reference files via `file_id` in content blocks, avoiding re-uploads across multiple API calls.

**Beta:** Pass `betas: ["files-api-2025-04-14"]` in your API calls (the SDK sets the required header automatically).

## Key Facts

- Maximum file size: 500 MB
- Total storage: 100 GB per organization
- Files persist until deleted
- File operations (upload, list, delete) are free; content used in messages is billed as input tokens
- Not available on Amazon Bedrock or Google Vertex AI

---

## Upload a File

```typescript
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const client = new Anthropic();

const uploaded = await client.beta.files.upload({
  file: await toFile(fs.createReadStream("report.pdf"), undefined, {
    type: "application/pdf",
  }),
  betas: ["files-api-2025-04-14"],
});

console.log(`File ID: ${uploaded.id}`);
console.log(`Size: ${uploaded.size_bytes} bytes`);
```

---

## Use a File in Messages

### PDF / Text Document

```typescript
const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content: [
        { type: "text", text: "Summarize the key findings in this report." },
        {
          type: "document",
          source: { type: "file", file_id: uploaded.id },
          title: "Q4 Report",
          citations: { enabled: true },
        },
      ],
    },
  ],
  betas: ["files-api-2025-04-14"],
});

console.log(response.content[0].text);
```

---

## Manage Files

### List Files

```typescript
const files = await client.beta.files.list({
  betas: ["files-api-2025-04-14"],
});
for (const f of files.data) {
  console.log(`${f.id}: ${f.filename} (${f.size_bytes} bytes)`);
}
```

### Delete a File

```typescript
await client.beta.files.delete("file_011CNha8iCJcU1wXNR6q4V8w", {
  betas: ["files-api-2025-04-14"],
});
```

### Download a File

```typescript
const response = await client.beta.files.download(
  "file_011CNha8iCJcU1wXNR6q4V8w",
  { betas: ["files-api-2025-04-14"] },
);
const content = Buffer.from(await response.arrayBuffer());
await fs.promises.writeFile("output.txt", content);
```
</doc>

<doc path="typescript/claude-api/streaming.md">
# Streaming — TypeScript

## Quick Start

```typescript
const stream = client.messages.stream({
  model: "claude-opus-4-8",
  max_tokens: 64000,
  messages: [{ role: "user", content: "Write a story" }],
});

for await (const event of stream) {
  if (
    event.type === "content_block_delta" &&
    event.delta.type === "text_delta"
  ) {
    process.stdout.write(event.delta.text);
  }
}
```

---

## Handling Different Content Types

> **Fable 5 / Opus 4.8 / Opus 4.7 / Opus 4.6:** Use `thinking: {type: "adaptive"}`. On older models, use `thinking: {type: "enabled", budget_tokens: N}` instead.

```typescript
const stream = client.messages.stream({
  model: "claude-opus-4-8",
  max_tokens: 64000,
  thinking: { type: "adaptive" },
  messages: [{ role: "user", content: "Analyze this problem" }],
});

for await (const event of stream) {
  switch (event.type) {
    case "content_block_start":
      switch (event.content_block.type) {
        case "thinking":
          console.log("\n[Thinking...]");
          break;
        case "text":
          console.log("\n[Response:]");
          break;
      }
      break;
    case "content_block_delta":
      switch (event.delta.type) {
        case "thinking_delta":
          process.stdout.write(event.delta.thinking);
          break;
        case "text_delta":
          process.stdout.write(event.delta.text);
          break;
      }
      break;
  }
}
```

---

## Streaming with Tool Use (Tool Runner)

Use the tool runner with `stream: true`. The outer loop iterates over tool runner iterations (messages), the inner loop processes stream events:

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const getWeather = betaZodTool({
  name: "get_weather",
  description: "Get current weather for a location",
  inputSchema: z.object({
    location: z.string().describe("City and state, e.g., San Francisco, CA"),
  }),
  run: async ({ location }) => `72°F and sunny in ${location}`,
});

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-8",
  max_tokens: 64000,
  tools: [getWeather],
  messages: [
    { role: "user", content: "What's the weather in Paris and London?" },
  ],
  stream: true,
});

// Outer loop: each tool runner iteration
for await (const messageStream of runner) {
  // Inner loop: stream events for this iteration
  for await (const event of messageStream) {
    switch (event.type) {
      case "content_block_delta":
        switch (event.delta.type) {
          case "text_delta":
            process.stdout.write(event.delta.text);
            break;
          case "input_json_delta":
            // Tool input being streamed
            break;
        }
        break;
    }
  }
}
```

---

## Getting the Final Message

```typescript
const stream = client.messages.stream({
  model: "claude-opus-4-8",
  max_tokens: 64000,
  messages: [{ role: "user", content: "Hello" }],
});

for await (const event of stream) {
  // Process events...
}

const finalMessage = await stream.finalMessage();
console.log(`Tokens used: ${finalMessage.usage.output_tokens}`);
```

---

## Stream Event Types

| Event Type            | Description                 | When it fires                     |
| --------------------- | --------------------------- | --------------------------------- |
| `message_start`       | Contains message metadata   | Once at the beginning             |
| `content_block_start` | New content block beginning | When a text/tool_use block starts |
| `content_block_delta` | Incremental content update  | For each token/chunk              |
| `content_block_stop`  | Content block complete      | When a block finishes             |
| `message_delta`       | Message-level updates       | Contains `stop_reason`, usage     |
| `message_stop`        | Message complete            | Once at the end                   |

## Best Practices

1. **Always flush output** — Use `process.stdout.write()` for immediate display
2. **Handle partial responses** — If the stream is interrupted, you may have incomplete content
3. **Track token usage** — The `message_delta` event contains usage information
4. **Use `finalMessage()`** — Get the complete `Anthropic.Message` object even when streaming. Don't wrap `.on()` events in `new Promise()` — `finalMessage()` handles all completion/error/abort states internally
5. **Buffer for web UIs** — Consider buffering a few tokens before rendering to avoid excessive DOM updates
6. **Use `stream.on("text", ...)` for deltas** — The `text` event provides just the delta string, simpler than manually filtering `content_block_delta` events
7. **For agentic loops with streaming** — See the [Streaming Manual Loop](./tool-use.md#streaming-manual-loop) section in tool-use.md for combining `stream()` + `finalMessage()` with a tool-use loop

## Raw SSE Format

If using raw HTTP (not SDKs), the stream returns Server-Sent Events:

```
event: message_start
data: {"type":"message_start","message":{"id":"msg_...","type":"message",...}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn"},"usage":{"output_tokens":12}}

event: message_stop
data: {"type":"message_stop"}
```
</doc>

<doc path="typescript/claude-api/tool-use.md">
# Tool Use — TypeScript

For conceptual overview (tool definitions, tool choice, tips), see [shared/tool-use-concepts.md](../../shared/tool-use-concepts.md).

## Tool Runner (Recommended)

**Beta:** The tool runner is in beta in the TypeScript SDK.

Use `betaZodTool` with Zod schemas to define tools with a `run` function, then pass them to `client.beta.messages.toolRunner()`:

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const client = new Anthropic();

const getWeather = betaZodTool({
  name: "get_weather",
  description: "Get current weather for a location",
  inputSchema: z.object({
    location: z.string().describe("City and state, e.g., San Francisco, CA"),
    unit: z.enum(["celsius", "fahrenheit"]).optional(),
  }),
  run: async (input) => {
    // Your implementation here
    return `72°F and sunny in ${input.location}`;
  },
});

// The tool runner handles the agentic loop and returns the final message
const finalMessage = await client.beta.messages.toolRunner({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  tools: [getWeather],
  messages: [{ role: "user", content: "What's the weather in Paris?" }],
});

console.log(finalMessage.content);
```

**Key benefits of the tool runner:**

- No manual loop — the SDK handles calling tools and feeding results back
- Type-safe tool inputs via Zod schemas
- Tool schemas are generated automatically from Zod definitions
- Iteration stops automatically when Claude has no more tool calls

---

## Manual Agentic Loop

Use this when you need fine-grained control (custom logging, conditional tool execution, streaming individual iterations, human-in-the-loop approval):

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const tools: Anthropic.Tool[] = [...]; // Your tool definitions
let messages: Anthropic.MessageParam[] = [{ role: "user", content: userInput }];

while (true) {
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    tools: tools,
    messages: messages,
  });

  if (response.stop_reason === "end_turn") break;

  // Server-side tool hit iteration limit; append assistant turn and re-send to continue
  if (response.stop_reason === "pause_turn") {
    messages.push({ role: "assistant", content: response.content });
    continue;
  }

  const toolUseBlocks = response.content.filter(
    (b): b is Anthropic.ToolUseBlock => b.type === "tool_use",
  );

  messages.push({ role: "assistant", content: response.content });

  const toolResults: Anthropic.ToolResultBlockParam[] = [];
  for (const tool of toolUseBlocks) {
    const result = await executeTool(tool.name, tool.input);
    toolResults.push({
      type: "tool_result",
      tool_use_id: tool.id,
      content: result,
    });
  }

  messages.push({ role: "user", content: toolResults });
}
```

### Streaming Manual Loop

Use `client.messages.stream()` + `finalMessage()` instead of `.create()` when you need streaming within a manual loop. Text deltas are streamed on each iteration; `finalMessage()` collects the complete `Message` so you can inspect `stop_reason` and extract tool-use blocks:

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const tools: Anthropic.Tool[] = [...];
let messages: Anthropic.MessageParam[] = [{ role: "user", content: userInput }];

while (true) {
  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 64000,
    tools,
    messages,
  });

  // Stream text deltas on each iteration
  stream.on("text", (delta) => {
    process.stdout.write(delta);
  });

  // finalMessage() resolves with the complete Message — no need to
  // manually wire up .on("message") / .on("error") / .on("abort")
  const message = await stream.finalMessage();

  if (message.stop_reason === "end_turn") break;

  // Server-side tool hit iteration limit; append assistant turn and re-send to continue
  if (message.stop_reason === "pause_turn") {
    messages.push({ role: "assistant", content: message.content });
    continue;
  }

  const toolUseBlocks = message.content.filter(
    (b): b is Anthropic.ToolUseBlock => b.type === "tool_use",
  );

  messages.push({ role: "assistant", content: message.content });

  const toolResults: Anthropic.ToolResultBlockParam[] = [];
  for (const tool of toolUseBlocks) {
    const result = await executeTool(tool.name, tool.input);
    toolResults.push({
      type: "tool_result",
      tool_use_id: tool.id,
      content: result,
    });
  }

  messages.push({ role: "user", content: toolResults });
}
```

> **Important:** Don't wrap `.on()` events in `new Promise()` to collect the final message — use `stream.finalMessage()` instead. The SDK handles all error/abort/completion states internally.

> **Error handling in the loop:** Use the SDK's typed exceptions (e.g., `Anthropic.RateLimitError`, `Anthropic.APIError`) — see [Error Handling](./README.md#error-handling) for examples. Don't check error messages with string matching.

> **SDK types:** Use `Anthropic.MessageParam`, `Anthropic.Tool`, `Anthropic.ToolUseBlock`, `Anthropic.ToolResultBlockParam`, `Anthropic.Message`, etc. for all API-related data structures. Don't redefine equivalent interfaces.

---

## Handling Tool Results

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  tools: tools,
  messages: [{ role: "user", content: "What's the weather in Paris?" }],
});

for (const block of response.content) {
  if (block.type === "tool_use") {
    const result = await executeTool(block.name, block.input);

    const followup = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 16000,
      tools: tools,
      messages: [
        { role: "user", content: "What's the weather in Paris?" },
        { role: "assistant", content: response.content },
        {
          role: "user",
          content: [
            { type: "tool_result", tool_use_id: block.id, content: result },
          ],
        },
      ],
    });
  }
}
```

---

## Tool Choice

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  tools: tools,
  tool_choice: { type: "tool", name: "get_weather" },
  messages: [{ role: "user", content: "What's the weather in Paris?" }],
});
```

---

## Server-Side Tools

Version-suffixed `type` literals; `name` is fixed per interface. Pass plain object literals — the `ToolUnion` type is satisfied structurally. **The `name`/`type` pair must match the interface**: mixing `str_replace_based_edit_tool` (20250728 name) with `text_editor_20250124` (which expects `str_replace_editor`) is a TS2322.

**Don't type-annotate as `Tool[]`** — `Tool` is just the custom-tool variant. Let structural typing infer from the `tools` param, or annotate as `Anthropic.Messages.ToolUnion[]` if you must:

```typescript
// ✓ let inference work — no annotation
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  tools: [
    { type: "text_editor_20250728", name: "str_replace_based_edit_tool" },
    { type: "bash_20250124", name: "bash" },
    { type: "web_search_20260209", name: "web_search" },
    { type: "code_execution_20260120", name: "code_execution" },
  ],
  messages: [{ role: "user", content: "..." }],
});

// ✗ this is a TS2352 — Tool is the CUSTOM tool variant only
// const tools: Anthropic.Tool[] = [{ type: "text_editor_20250728", ... }]
```

| Interface | `name` | `type` |
|---|---|---|
| `ToolTextEditor20250124` | `str_replace_editor` | `text_editor_20250124` |
| `ToolTextEditor20250429` | `str_replace_based_edit_tool` | `text_editor_20250429` |
| `ToolTextEditor20250728` | `str_replace_based_edit_tool` | `text_editor_20250728` |
| `ToolBash20250124` | `bash` | `bash_20250124` |
| `WebSearchTool20260209` | `web_search` | `web_search_20260209` |
| `WebFetchTool20260209` | `web_fetch` | `web_fetch_20260209` |
| `CodeExecutionTool20260120` | `code_execution` | `code_execution_20260120` |

**Don't mix beta and non-beta types**: if you call `client.beta.messages.create()`, the response `content` is `BetaContentBlock[]` — you cannot pass that to a non-beta `ContentBlockParam[]` without narrowing each element.

---


## Code Execution

### Basic Usage

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content:
        "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
    },
  ],
  tools: [{ type: "code_execution_20260120", name: "code_execution" }],
});
```

### Reading Local Files (ESM note)

`__dirname` doesn't exist in ES modules. For script-relative paths use `import.meta.url`:

```typescript
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const pdfBytes = readFileSync(join(__dirname, "sample.pdf"));
```

Or use a CWD-relative path if the script runs from a known directory: `readFileSync("./sample.pdf")`.

### Upload Files for Analysis

```typescript
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import { createReadStream } from "fs";

const client = new Anthropic();

// 1. Upload a file
const uploaded = await client.beta.files.upload({
  file: await toFile(createReadStream("sales_data.csv"), undefined, {
    type: "text/csv",
  }),
  betas: ["files-api-2025-04-14"],
});

// 2. Pass to code execution
// Code execution is GA; Files API is still beta (pass via RequestOptions)
const response = await client.messages.create(
  {
    model: "claude-opus-4-8",
    max_tokens: 16000,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "Analyze this sales data. Show trends and create a visualization.",
          },
          { type: "container_upload", file_id: uploaded.id },
        ],
      },
    ],
    tools: [{ type: "code_execution_20260120", name: "code_execution" }],
  },
  { headers: { "anthropic-beta": "files-api-2025-04-14" } },
);
```

### Retrieve Generated Files

```typescript
import path from "path";
import fs from "fs";

const OUTPUT_DIR = "./claude_outputs";
await fs.promises.mkdir(OUTPUT_DIR, { recursive: true });

for (const block of response.content) {
  if (block.type === "bash_code_execution_tool_result") {
    const result = block.content;
    if (result.type === "bash_code_execution_result" && result.content) {
      for (const fileRef of result.content) {
        if (fileRef.type === "bash_code_execution_output") {
          const metadata = await client.beta.files.retrieveMetadata(
            fileRef.file_id,
          );
          const downloadResponse = await client.beta.files.download(fileRef.file_id);
          const fileBytes = Buffer.from(await downloadResponse.arrayBuffer());
          const safeName = path.basename(metadata.filename);
          if (!safeName || safeName === "." || safeName === "..") {
            console.warn(`Skipping invalid filename: ${metadata.filename}`);
            continue;
          }
          const outputPath = path.join(OUTPUT_DIR, safeName);
          await fs.promises.writeFile(outputPath, fileBytes);
          console.log(`Saved: ${outputPath}`);
        }
      }
    }
  }
}
```

### Container Reuse

```typescript
// First request: set up environment
const response1 = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content: "Install tabulate and create data.json with sample user data",
    },
  ],
  tools: [{ type: "code_execution_20260120", name: "code_execution" }],
});

// Reuse container
// container is nullable — set only when using server-side code execution
const containerId = response1.container!.id;

const response2 = await client.messages.create({
  container: containerId,
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content: "Read data.json and display as a formatted table",
    },
  ],
  tools: [{ type: "code_execution_20260120", name: "code_execution" }],
});
```

---

## Memory Tool

### Basic Usage

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content: "Remember that my preferred language is TypeScript.",
    },
  ],
  tools: [{ type: "memory_20250818", name: "memory" }],
});
```

### SDK Memory Helper

Use `betaMemoryTool` with a `MemoryToolHandlers` implementation:

```typescript
import {
  betaMemoryTool,
  type MemoryToolHandlers,
} from "@anthropic-ai/sdk/helpers/beta/memory";

const handlers: MemoryToolHandlers = {
  async view(command) { ... },
  async create(command) { ... },
  async str_replace(command) { ... },
  async insert(command) { ... },
  async delete(command) { ... },
  async rename(command) { ... },
};

const memory = betaMemoryTool(handlers);

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  tools: [memory],
  messages: [{ role: "user", content: "Remember my preferences" }],
});

for await (const message of runner) {
  console.log(message);
}
```

For full implementation examples, use WebFetch:

- `https://github.com/anthropics/anthropic-sdk-typescript/blob/main/examples/tools-helpers-memory.ts`

---

## Structured Outputs

### JSON Outputs (Zod — Recommended)

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

const ContactInfoSchema = z.object({
  name: z.string(),
  email: z.string(),
  plan: z.string(),
  interests: z.array(z.string()),
  demo_requested: z.boolean(),
});

const client = new Anthropic();

const response = await client.messages.parse({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content:
        "Extract: Jane Doe (jane@co.com) wants Enterprise, interested in API and SDKs, wants a demo.",
    },
  ],
  output_config: {
    format: zodOutputFormat(ContactInfoSchema),
  },
});

// parsed_output is null if parsing failed — assert or guard
console.log(response.parsed_output!.name); // "Jane Doe"
```

### Strict Tool Use

```typescript
const response = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 16000,
  messages: [
    {
      role: "user",
      content: "Book a flight to Tokyo for 2 passengers on March 15",
    },
  ],
  tools: [
    {
      name: "book_flight",
      description: "Book a flight to a destination",
      strict: true,
      input_schema: {
        type: "object",
        properties: {
          destination: { type: "string" },
          date: { type: "string", format: "date" },
          passengers: {
            type: "integer",
            enum: [1, 2, 3, 4, 5, 6, 7, 8],
          },
        },
        required: ["destination", "date", "passengers"],
        additionalProperties: false,
      },
    },
  ],
});
```
</doc>

<doc path="typescript/managed-agents/README.md">
# Managed Agents — TypeScript

> **Bindings not shown here:** This README covers the most common managed-agents flows for TypeScript. If you need a class, method, namespace, field, or behavior that isn't shown, WebFetch the TypeScript SDK repo **or the relevant docs page** from `shared/live-sources.md` rather than guess. Do not extrapolate from cURL shapes or another language's SDK.

> **Agents are persistent — create once, reference by ID.** Store the agent ID returned by `agents.create` and pass it to every subsequent `sessions.create`; do not call `agents.create` in the request path. The Anthropic CLI is one convenient way to create agents and environments from version-controlled YAML — its URL is in `shared/live-sources.md`. The examples below show in-code creation for completeness; in production the create call belongs in setup, not in the request path.

## Installation

```bash
npm install @anthropic-ai/sdk
```

## Client Initialization

```typescript
import Anthropic from "@anthropic-ai/sdk";

// Default — resolves credentials from the environment:
// ANTHROPIC_API_KEY, or ANTHROPIC_AUTH_TOKEN, or an `ant auth login` profile.
// Prefer this for local dev; don't hardcode a key.
const client = new Anthropic();

// Explicit API key (only when you must inject a specific key)
const client = new Anthropic({ apiKey: "your-api-key" });
```

---

## Create an Environment

```typescript
const environment = await client.beta.environments.create(
  {
    name: "my-dev-env",
    config: {
      type: "cloud",
      networking: { type: "unrestricted" },
    },
  },
);
console.log(environment.id); // env_...
```

---

## Create an Agent (required first step)

> ⚠️ **There is no inline agent config.** `model`/`system`/`tools` live on the agent object, not the session. Always start with `agents.create()` — the session only takes `agent: { type: "agent", id: agent.id }`.

### Minimal

```typescript
// 1. Create the agent (reusable, versioned)
const agent = await client.beta.agents.create(
  {
    name: "Coding Assistant",
    model: "claude-opus-4-8",
    tools: [{ type: "agent_toolset_20260401", default_config: { enabled: true } }],
  },
);

// 2. Start a session
const session = await client.beta.sessions.create(
  {
    agent: { type: "agent", id: agent.id, version: agent.version },
    environment_id: environment.id,
  },
);
console.log(session.id, session.status);
```

### With system prompt and custom tools

```typescript
const agent = await client.beta.agents.create(
  {
    name: "Code Reviewer",
    model: "claude-opus-4-8",
    system: "You are a senior code reviewer.",
    tools: [
      { type: "agent_toolset_20260401", default_config: { enabled: true } },
      {
        type: "custom",
        name: "run_tests",
        description: "Run the test suite",
        input_schema: {
          type: "object",
          properties: {
            test_path: { type: "string", description: "Path to test file" },
          },
          required: ["test_path"],
        },
      },
    ],
  },
);

const session = await client.beta.sessions.create(
  {
    agent: { type: "agent", id: agent.id, version: agent.version },
    environment_id: environment.id,
    title: "Code review session",
    resources: [
      {
        type: "github_repository",
        url: "https://github.com/owner/repo",
        mount_path: "/workspace/repo",
        authorization_token: process.env.GITHUB_TOKEN,
        branch: "main",
      },
    ],
  },
);
```

---

## Send a User Message

```typescript
await client.beta.sessions.events.send(
  session.id,
  {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "Review the auth module" }],
      },
    ],
  },
);
```

> 💡 **Stream-first:** Open the stream *before* (or concurrently with) sending the message. The stream only delivers events that occur after it opens — stream-after-send means early events arrive buffered in one batch. See [Steering Patterns](../../shared/managed-agents-events.md#steering-patterns).

---

## Stream Events (SSE)

```typescript
// Stream-first: open stream and send concurrently
const [events] = await Promise.all([
  collectStream(session.id),
  client.beta.sessions.events.send(
    session.id,
    { events: [{ type: "user.message", content: [{ type: "text", text: "..." }] }] },
  ),
]);

// Standalone stream iteration:
const stream = await client.beta.sessions.events.stream(
  session.id,
);

for await (const event of stream) {
  switch (event.type) {
    case "agent.message":
      for (const block of event.content) {
        if (block.type === "text") {
          process.stdout.write(block.text);
        }
      }
      break;
    case "agent.custom_tool_use":
      // Custom tool invocation — session is now idle
      console.log(`\nCustom tool call: ${event.name}`);
      console.log(`Input: ${JSON.stringify(event.input)}`);
      break;
    case "session.status_idle":
      console.log("\n--- Agent idle ---");
      break;
    case "session.status_terminated":
      console.log("\n--- Session terminated ---");
      break;
  }
}
```

---

## Provide Custom Tool Result

```typescript
await client.beta.sessions.events.send(
  session.id,
  {
    events: [
      {
        type: "user.custom_tool_result",
        custom_tool_use_id: "sevt_abc123",
        content: [{ type: "text", text: "All 42 tests passed." }],
      },
    ],
  },
);
```

---

## Poll Events

```typescript
const events = await client.beta.sessions.events.list(
  session.id,
);
for (const event of events.data) {
  console.log(`${event.type}: ${event.id}`);
}
```

---

## Full Streaming Loop with Custom Tools

```typescript
function runCustomTool(toolName: string, toolInput: unknown): string {
  if (toolName === "run_tests") {
    // Your tool implementation here
    return "All tests passed.";
  }
  return `Unknown tool: ${toolName}`;
}

async function runSession(client: Anthropic, sessionId: string) {
  while (true) {
    const stream = await client.beta.sessions.events.stream(
      sessionId,
    );

    const toolCalls: Anthropic.Beta.Sessions.BetaManagedAgentsAgentCustomToolUseEvent[] = [];

    for await (const event of stream) {
      if (event.type === "agent.message") {
        for (const block of event.content) {
          if (block.type === "text") {
            process.stdout.write(block.text);
          }
        }
      } else if (event.type === "agent.custom_tool_use") {
        toolCalls.push(event);
      } else if (event.type === "session.status_idle") {
        break;
      } else if (event.type === "session.status_terminated") {
        return;
      }
    }

    if (toolCalls.length === 0) break;

    // Process custom tool calls
    const results = toolCalls.map((call) => ({
      type: "user.custom_tool_result" as const,
      custom_tool_use_id: call.id,
      content: [{ type: "text" as const, text: runCustomTool(call.name, call.input) }],
    }));

    await client.beta.sessions.events.send(
      sessionId,
      { events: results },
    );
  }
}
```

---

## Upload a File

```typescript
import fs from "fs";

const file = await client.beta.files.upload({
  file: fs.createReadStream("data.csv"),
  purpose: "agent",
});

// Use in a session
const session = await client.beta.sessions.create(
  {
    agent: { type: "agent", id: agent.id, version: agent.version },
    environment_id: environment.id,
    resources: [{ type: "file", file_id: file.id, mount_path: "/workspace/data.csv" }],
  },
);
```

---

## List and Download Session Files

List files the agent wrote to `/mnt/session/outputs/` during a session, then download them.

```typescript
import fs from "fs";

// List files associated with a session
const files = await client.beta.files.list({
  scope_id: session.id,
  betas: ["managed-agents-2026-04-01"],
});
for (const f of files.data) {
  console.log(f.filename, f.size_bytes);

  // Download and save to disk
  const resp = await client.beta.files.download(f.id);
  const buffer = Buffer.from(await resp.arrayBuffer());
  fs.writeFileSync(f.filename, buffer);
}
```

> 💡 There's a brief indexing lag (~1–3s) between `session.status_idle` and output files appearing in `files.list`. Retry once or twice if the list is empty.

---

## Session Management

```typescript
// Get session details
const session = await client.beta.sessions.retrieve("sesn_011CZxAbc123Def456");
console.log(session.status, session.usage);

// List sessions
const sessions = await client.beta.sessions.list();

// Delete a session
await client.beta.sessions.delete("sesn_011CZxAbc123Def456");

// Archive a session
await client.beta.sessions.archive("sesn_011CZxAbc123Def456");
```

---

## MCP Server Integration

```typescript
// Agent declares MCP server (no auth here — auth goes in a vault)
const agent = await client.beta.agents.create({
  name: "MCP Agent",
  model: "claude-opus-4-8",
  mcp_servers: [
    { type: "url", name: "my-tools", url: "https://my-mcp-server.example.com/sse" },
  ],
  tools: [
    { type: "agent_toolset_20260401", default_config: { enabled: true } },
    { type: "mcp_toolset", mcp_server_name: "my-tools" },
  ],
});

// Session attaches vault(s) containing credentials for those MCP server URLs
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: [vault.id],
});
```

See `shared/managed-agents-tools.md` §Vaults for creating vaults and adding credentials.
</doc>

## When to Use WebFetch

Use WebFetch to get the latest documentation when:

- User asks for "latest" or "current" information
- Cached data seems incorrect
- User asks about features not covered here

Live documentation URLs are in `shared/live-sources.md`.

## Common Pitfalls

- Don't truncate inputs when passing files or content to the API. If the content is too long to fit in the context window, notify the user and discuss options (chunking, summarization, etc.) rather than silently truncating.
- **Fable 5 / Opus 4.8 / 4.7 thinking:** Adaptive only. `thinking: {type: "enabled", budget_tokens: N}` returns 400 — `budget_tokens` is fully removed (along with `temperature`, `top_p`, `top_k`). Use `thinking: {type: "adaptive"}`. Opus 4.8 inherits this surface from 4.7 with no new breaking changes; Fable 5 adds one — an explicit `thinking: {type: "disabled"}` returns a 400 (accepted on 4.7/4.8); omit the param instead.
- **Opus 4.6 / Sonnet 4.6 thinking:** Use `thinking: {type: "adaptive"}` — do NOT use `budget_tokens` for new 4.6 code (deprecated on both Opus 4.6 and Sonnet 4.6; for gradual migration of existing code, see the transitional escape hatch in `shared/model-migration.md` — note this carve-out does not apply to Fable 5, Opus 4.7 or 4.8). For older models, `budget_tokens` must be less than `max_tokens` (minimum 1024). This will throw an error if you get it wrong.
- **Prefill removed (Fable 5 and the 4.6/4.7/4.8 family):** Assistant message prefills (last-assistant-turn prefills) return a 400 error on Fable 5, Opus 4.6, Opus 4.7, Opus 4.8, and Sonnet 4.6. Use structured outputs (`output_config.format`) or system prompt instructions to control response format instead.
- **Confirm migration scope before editing:** When a user asks to migrate code to a newer Claude model without naming a specific file, directory, or file list, **ask which scope to apply first** — the entire working directory, a specific subdirectory, or a specific set of files. Do not start editing until the user confirms. Imperative phrasings like "migrate my codebase", "move my project to X", "upgrade to Sonnet 4.6", or bare "migrate to Opus 4.8" are **still ambiguous** — they tell you what to do but not where, so ask. Proceed without asking only when the prompt names an exact file, a specific directory, or an explicit file list ("migrate `app.py`", "migrate everything under `services/`", "update `a.py` and `b.py`"). See `shared/model-migration.md` Step 0.
- **`max_tokens` defaults:** Don't lowball `max_tokens` — hitting the cap truncates output mid-thought and requires a retry. For non-streaming requests, default to `~16000` (keeps responses under SDK HTTP timeouts). For streaming requests, default to `~64000` (timeouts aren't a concern, so give the model room). Only go lower when you have a hard reason: classification (`~256`), cost caps, deliberately short outputs, or **`max_tokens: 0`** for cache pre-warming (see `shared/prompt-caching.md` → Pre-warming).
- **128K output tokens:** Fable 5, Opus 4.6, Opus 4.7, and Opus 4.8 support up to 128K `max_tokens`, but the SDKs require streaming for values that large to avoid HTTP timeouts. Use `.stream()` with `.get_final_message()` / `.finalMessage()`.
- **Tool call JSON parsing (Fable 5 and the 4.6/4.7/4.8 family):** Fable 5, Opus 4.6, Opus 4.7, Opus 4.8, and Sonnet 4.6 may produce different JSON string escaping in tool call `input` fields (e.g., Unicode or forward-slash escaping). Always parse tool inputs with `json.loads()` / `JSON.parse()` — never do raw string matching on the serialized input.
- **Structured outputs (all models):** Use `output_config: {format: {...}}` instead of the deprecated `output_format` parameter on `messages.create()`. This is a general API change, not 4.6-specific.
- **Don't reimplement SDK functionality:** The SDK provides high-level helpers — use them instead of building from scratch. Specifically: use `stream.finalMessage()` instead of wrapping `.on()` events in `new Promise()`; use typed exception classes (`Anthropic.RateLimitError`, etc.) instead of string-matching error messages; use SDK types (`Anthropic.MessageParam`, `Anthropic.Tool`, `Anthropic.Message`, etc.) instead of redefining equivalent interfaces.
- **Don't define custom types for SDK data structures:** The SDK exports types for all API objects. Use `Anthropic.MessageParam` for messages, `Anthropic.Tool` for tool definitions, `Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam` for tool results, `Anthropic.Message` for responses. Defining your own `interface ChatMessage { role: string; content: unknown }` duplicates what the SDK already provides and loses type safety.
- **Report and document output:** For tasks that produce reports, documents, or visualizations, the code execution sandbox has `python-docx`, `python-pptx`, `matplotlib`, `pillow`, and `pypdf` pre-installed. Claude can generate formatted files (DOCX, PDF, charts) and return them via the Files API — consider this for "report" or "document" type requests instead of plain stdout text.

## 🤖 Claude *(01:48:09)*


## 🤖 Claude *(01:48:09)*


## 🤖 Claude *(01:48:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s --max-time 20 \"https://openrouter.ai/api/v1/models\" | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nmodels=[m['id'] for m in d.get('data',[])]\nfable=[m for m in models if 'fable' in m.lower()]\nclaude=[m for m in models if 'anthropic' in m.lower()][:15]\nprint('FABLE matches:', fable)\nprint('Sample anthropic models:', claude)\nprint('total models:', len(models))\n\"",
  "description": "Check OpenRouter catalog for Claude Fable 5 availability"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> FABLE matches: ['~anthropic/claude-fable-latest', 'anthropic/claude-fable-5']
> Sample anthropic models: ['~anthropic/claude-fable-latest', 'anthropic/claude-fable-5', 'anthropic/claude-opus-4.8-fast', 'anthropic/claude-opus-4.8', 'anthropic/claude-opus-4.7-fast', '~anthropic/claude-haiku-latest', '~anthropic/claude-sonnet-latest', '~anthropic/claude-opus-latest', 'anthropic/claude-opus-4.7', 'anthropic/claude-opus-4.6-fast', 'anthropic/claude-sonnet-4.6', 'anthropic/claude-opus-4.6', 'anthropic/claude-opus-4.5', 'anthropic/claude-haiku-4.5', 'anthropic/claude-sonnet-4.5']
> total models: 339
> ```

## 🤖 Claude *(01:48:26)*


## 🤖 Claude *(01:48:26)*


## 🤖 Claude *(01:48:26)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskOutput,TaskCreate,TaskUpdate",
  "max_results": 3
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskOutput'}, {'type': 'tool_reference', 'tool_name': 'TaskCreate'}, {'type': 'tool_reference', 'tool_name': 'TaskUpdate'}]
> ```

## 🤖 Claude *(01:48:37)*


🛠️ **Tool Call**: `TaskOutput`
```json
{
  "task_id": "wr6vzsvto",
  "block": true,
  "timeout": 300000
}
```

> **Tool Result (TaskOutput)** - ✅ Success
>
> ```
> <retrieval_status>timeout</retrieval_status>
> 
> <task_id>wr6vzsvto</task_id>
> 
> <task_type>local_workflow</task_type>
> 
> <status>running</status>
> ```

## 🤖 Claude *(01:53:42)*


🛠️ **Tool Call**: `TaskOutput`
```json
{
  "task_id": "wr6vzsvto",
  "block": true,
  "timeout": 300000
}
```

> **Tool Result (TaskOutput)** - ✅ Success
>
> ```
> <retrieval_status>timeout</retrieval_status>
> 
> <task_id>wr6vzsvto</task_id>
> 
> <task_type>local_workflow</task_type>
> 
> <status>running</status>
> ```

## 🤖 Claude *(01:58:47)*


🛠️ **Tool Call**: `TaskOutput`
```json
{
  "task_id": "wr6vzsvto",
  "block": true,
  "timeout": 600000
}
```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-10 - Generate security BoK documentation suite]]
> * **Próxima Sessão**: [[2026-06-10 - agent-a8758d5129a625779]]
%% --- TIMELINE END --- %%

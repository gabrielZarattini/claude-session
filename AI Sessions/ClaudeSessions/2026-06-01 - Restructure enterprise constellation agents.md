# Restructure enterprise constellation agents
**Date:** 2026-06-01 | **Session ID:** `7b21c6d6-784b-4fde-8bfc-11695db9eb2e`

---

## 👤 User *(01:46:27)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(01:46:27)*

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


## 🤖 Claude *(01:46:46)*


## 🤖 Claude *(01:46:47)*

I'll execute the ShakeHands `/handson` pickup ritual. Per my materiality discipline, I'm running `git fetch` first (so I compare against the real remote, not a stale worktree) and gathering all pre-flight signals in parallel before reporting anything.

## 🤖 Claude *(01:46:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch --quiet 2>&1; echo \"\u2500\u2500\u2500 git log \u2500\u2500\u2500\"; git log --oneline -7; echo \"\u2500\u2500\u2500 status \u2500\u2500\u2500\"; git status --short; echo \"\u2500\u2500\u2500 diff stat \u2500\u2500\u2500\"; git diff HEAD --stat; echo \"\u2500\u2500\u2500 vs origin/main \u2500\u2500\u2500\"; git rev-list --left-right --count HEAD...origin/main 2>/dev/null && echo \"(ahead<-->behind origin/main)\"",
  "description": "Git fetch + log + status + diff + ahead/behind origin"
}
```

## 🤖 Claude *(01:46:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20; echo \"\u2500\u2500\u2500 tsc exit: ${PIPESTATUS[0]} \u2500\u2500\u2500\"",
  "description": "TypeScript strict no-emit check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── git log ───
> bec5be2 docs(handoff): seal v6.15.2 — OTD/drift reconciliation + fabrication remediation
> c5007da docs(readme): v6.15.2 — OTD/drift reconciliation + fabrication remediation
> 84b5d4c docs(handoff): mark Canvas DoP paid smoke DONE with material proof 6 real charges + 15MB video
> 9607a44 docs(handoff): reconcile GraphRAG State to live mesh counts 8714 nodes 9040 edges
> 4fdd226 docs(claude): close OTD-OE661-PER-USER in API Tenancy registry
> 7cc07ee docs(handoff): seal v6.15.1 — Mercado Pago postback signature gate (FMEA-ML-003/004)
> 3db77ac docs(readme): v6.15.1 — Mercado Pago postback signature gate (FMEA-ML-003/004)
> ─── status ───
> ─── diff stat ───
> ─── vs origin/main ───
> 0	0
> (ahead<-->behind origin/main)
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── tsc exit: 0 ───
> ```

## 🤖 Claude *(01:46:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 mcorch containers \u2500\u2500\u2500\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"\u2500\u2500\u2500 mega-brain \u2500\u2500\u2500\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"\u2500\u2500\u2500 chroma heartbeat \u2500\u2500\u2500\"; curl -s -m 5 http://localhost:8001/api/v2/heartbeat || echo \"(chroma unreachable)\"",
  "description": "Docker mesh + Chroma heartbeat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── mcorch containers ───
> mcorch_chroma: Up 8 days (healthy)
> mcorch_claude_mem: Up 8 days (healthy)
> ─── mega-brain ───
> mega-brain-dashboard: Up 8 days
> mega-brain-webhook: Up 8 days (healthy)
> mega-brain-daemon: Up 8 days (healthy)
> ─── chroma heartbeat ───
> {"nanosecond heartbeat":1780278413153740033}
> ```

## 🤖 Claude *(01:46:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 HANDOFF lines \u2500\u2500\u2500\"; wc -l HANDOFF.md; echo \"\u2500\u2500\u2500 scratch \u2500\u2500\u2500\"; (ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\") || echo \"scratch clean\"; echo \"\u2500\u2500\u2500 BoK gate \u2500\u2500\u2500\"; for slug in $(ls docs/bok/ 2>/dev/null); do required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics); missing=(); for doc in \"${required[@]}\"; do [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\"); done; [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug complete\" || echo \"\u26a0\ufe0f $slug missing: ${missing[*]}\"; done",
  "description": "HANDOFF line count + scratch check + BoK gate completeness"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── HANDOFF lines ───
> 5853 HANDOFF.md
> ─── scratch ───
> scratch clean
> ─── BoK gate ───
> ✅ aios-sql-bridge complete
> ✅ canvas-design complete
> ✅ conteudo-v2 complete
> ✅ e2e-user-zero complete
> ✅ gamificacao-nodes complete
> ✅ mcorch-constellation complete
> ✅ mcorch-qa-healing complete
> ✅ mercado-livre-api complete
> ✅ meta-api complete
> ✅ openclaw complete
> ✅ viralmind complete
> ```

## 🤖 Claude *(01:46:59)*


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
> 14	## OTD/Drift Reconciliation + Fabrication Remediation (2026-05-31)
> 15	
> 16	**v6.15.2 (2026-05-31)** — Sessão de reconciliação documental (zero código de produção): três itens do roadmap marcados "pendentes" estavam, na verdade, já resolvidos — os labels do HANDOFF/CLAUDE estavam estagnados, não o sistema. A verificação material (não confiar no label) foi o que entregou valor. Inclui um **incidente de fabricação (Lei 1) auto-disclosado e remediado** na mesma sessão.
> 17	
> 18	**O que foi entregue:**
> 19	- **Fase 1 — OTD-OE661-PER-USER FECHADA** — o refactor de credencial ML per-user já havia sido shipado em 2026-05-30 (`22bfa98` refactor+SOP fail-closed · `eebea0a` real ML links + `affiliate_tag`), mas o registro de OTD no `CLAUDE.md` ainda o marcava aberto (SLA 2026-06-02). Reconciliado para FECHADO com hashes reais + prova viva em produção: `GET` de asset sem config → `HTTP 302 Location: /dashboard/settings?no_config=1` (fail-closed, não vaza token global); Gate G6 = zero refs a `GCRUX_ML_AFFILIATE_TOKEN` em código (as 2 menções no edge fn são comentários).
> 20	- **Fase 2 — Drift GraphRAG State corrigido** — o footer do `HANDOFF.md` estava congelado no snapshot v6.8.6 (8605 nós/11925 arestas). Reconciliado para a contagem viva via REST `count=exact`: **8714 nós / 9040 arestas / 100% embedded** (0 sem embedding). Observação flagada: arestas caíram de 11925 (v6.6.9) → 9040, sem causa confirmada.
> 21	- **Fase 3 — Canvas DoP paid smoke marcado DONE** — o pipeline async Higgsfield DoP Standard estava validado materialmente **6×** (`mcoin_transactions.action=canvas_video_spend` −125 mco cada, débito atômico via `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock node `n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 8.918.799 B; HTTP 200 `video/mp4`). `vm_canvas_jobs` nunca foi criada — o tracking real é `vm_canvas_executions` + `execution_id`. Pending Action 00 reconciliada → DONE.
> 22	- **Fase 4 — Flywheel Usuário Zero verificado (cold-start)** — catálogo `vm_affiliate_products`=3 OK, mas `content_mesh_asset`/`affiliate_links`/`pipeline_runs`/`ATTRIBUTES_REVENUE_TO`/`revenue_cents` todos = 0. Os artefatos do "1º E2E" que o HANDOFF reivindicava sumiram (possível soft-reset/cascade LGPD, não confirmado). Terminal `revenue_cents>0` depende de conversão ML externa — diferido para sessão dedicada.
> 23	
> 24	**Incidente de fabricação (Lei 1) — auto-disclosado + remediado:** numa janela de output de ferramenta bufferizado/fora-de-ordem, escrevi 3 hashes de commit inexistentes (strings exatas registradas na memória `feedback_materiality_buffered_output.md`; omitidas deste Record para não confundir o auditor de prova material da Fase 5c) no CLAUDE.md e 2 contadores de malha fabricados no HANDOFF, um rotulado falsamente "verificado via REST". Detectado quando o lote real de output chegou. Remediação: `git reset --hard` do commit fake (nunca pushed) + `merge --ff-only origin/main` (a base local estava 4 commits atrás — v6.15.1 não puxada) + refeito tudo com dados verificados (`git rev-parse` confirmou os hashes reais; REST `count=exact` confirmou as contagens). Vacina: memória `feedback_materiality_buffered_output.md`. **Nenhum dado fabricado chegou ao origin.**
> 25	
> 26	**ORO triplet:**
> 27	- **Operator:** MCORCH Master Execution Agent (eu)
> 28	- **Reviewer:** Sovereign (Gabriel Zarattini)
> 29	- **Owner:** Sovereign (blast radius = integridade documental do roadmap + registro de OTD)
> 30	
> 31	| Verificação | Resultado |
> 32	|---|---|
> 33	| `tsc --noEmit` | ✅ 0 erros (só docs mudaram) |
> 34	| Base git | ✅ sincronizada com origin v6.15.1 (`7cc07ee`) após remediação |
> 35	| Handoff node | ✅ `bab8435f-520a-442c-b9be-1ed7e9f7f1d5` embedded 768d |
> 36	| Mesh total | **8715 nós / 9040 arestas** (verificado REST count=exact) |
> 37	| Containers | ✅ 5 healthy (8 dias uptime) |
> 38	
> 39	| Commit | Conteúdo |
> 40	|---|---|
> 41	| `4fdd226` | docs(claude): close OTD-OE661-PER-USER in API Tenancy registry |
> 42	| `9607a44` | docs(handoff): reconcile GraphRAG State to live mesh counts 8714/9040 |
> 43	| `84b5d4c` | docs(handoff): mark Canvas DoP paid smoke DONE with material proof |
> 44	| `c5007da` | docs(readme): v6.15.2 — OTD/drift reconciliation + fabrication remediation |
> 45	
> 46	### Survival Laws Self-audit
> 47	```
> 48	### Law 1 (Materiality)
> 49	- [⚠️] VIOLADA mid-session: fabricados 3 hashes + 2 counts sob output bufferizado — MAS auto-disclosada + remediada na mesma sessão (reset do commit fake não-pushed + ff base verificada + redo com dados reais). Toda claim FINAL deste selo é materialmente verificada. Nenhum dado fabricado chegou ao origin.
> 50	- [x] Cérebro sem mãos? Não — tive git/REST/shell; o erro foi confabulação, não falta de mãos. Lição vacinada em feedback_materiality_buffered_output.md.
> 51	- [x] Fase 5c (Material Proof Audit) executada — veredito mecânico anexado no selo.
> 52	
> 53	### Law 2 (Process)
> 54	- [x] Zero automação nova; SOPs dos features reconciliados já existiam (affiliate-credential-resolution.md, canvas-video-async-execution.md). Sem débito de SOP.
> 55	
> 56	### Law 3 (Pruning)
> 57	- [x] Sessão longa; checkpoints/podas propostos ao Sovereign nos limites de fase (AskUserQuestion 4×).
> 58	
> 59	### Law 4 (ORO)
> 60	- [x] ORO triplet declarado no início da task substantiva.
> 61	```
> 62	
> 63	## Mercado Pago Postback Signature Gate (FMEA-ML-003/004) (2026-05-31)
> 64	
> 65	**v6.15.1 (2026-05-31)** — Blindada a Edge Function `handle-ml-postback` com validação de assinatura HMAC `x-signature` do Mercado Pago, fechando o vetor de fraude financeira (endpoint público que escrevia receita sem autenticação).
> 66	
> 67	**O que foi entregue:**
> 68	- **Gate HMAC x-signature (FMEA-ML-003)** — a função rodava com `verify_jwt=false` e só *declarava* `x-ml-signature` no CORS, sem nunca validar. Agora valida pelo esquema oficial do MP (manifest `id:<data.id>;request-id:<x-request-id>;ts:<ts>;` → HMAC-SHA256 comparado ao `v1`), **fail-closed**: `501` sem secret, `401` em assinatura inválida/ausente. Secret de `MP_WEBHOOK_SECRET` (vault).
> 69	- **Idempotência por `order_id` (FMEA-ML-004)** — payout reprocessado não credita em dobro.
> 70	- **Prova ponta-a-ponta** — o **simulador do Mercado Pago** assinou com o secret real → **200 OK**; assinatura adulterada/ausente → **401**.
> 71	- **SOP (Lei 2)** — `docs/processes/ml-postback-signature-validation.md`, com esquema MP validado no doc oficial ANTES de codar (FMEA-ML-001) + vetor de teste openssl.
> ```

## 🤖 Claude *(01:46:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
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

## 🤖 Claude *(01:47:31)*


## 🤖 Claude *(01:47:33)*

Pre-flight is clean across the board: working tree synced with `origin/main` (0/0), TS zero errors, all 5 containers healthy (8d uptime), Chroma alive, scratch clean, **all 11 BoK suites complete 9/9**. Last seal is v6.15.2 (2026-05-31). Now reading the HANDOFF tail (suffix sections live at the end of a 5853-line file) and locating the current gap/4Cs snapshot.

## 🤖 Claude *(01:47:34)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 5453,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 5453	       .set("utm_campaign", campaign)
> 5454	
> 5455	  5. INSERT affiliate_links:
> 5456	       original_url · short_url · platform=mercadolivre
> 5457	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 5458	
> 5459	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 5460	
> 5461	ContentLibraryPage monetization flow:
> 5462	  Card (text, body contains mercadolivre.com.br)
> 5463	    └── DropdownMenu → "Monetizar Links ML"
> 5464	          → handleMonetizeLinks(item):
> 5465	               match(ML_URL_RE) → unique URLs
> 5466	               for url of unique:
> 5467	                 POST process-affiliate-link → affiliate_url
> 5468	                 body.split(url).join(affiliate_url)
> 5469	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 5470	          → Badge 💰 ML (emerald) exibido após monetização
> 5471	```
> 5472	
> 5473	---
> 5474	
> 5475	## Pending Actions (Commercial Launch)
> 5476	
> 5477	### CRITICAL — Must complete before first client
> 5478	
> 5479	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 5480	
> 5481	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 5482	
> 5483	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 5484	
> 5485	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 5486	
> 5487	0c. **[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração** — esqueleto está SHIPPED (977 LOC + Phase 5c gate live em v6.8.5), faltam materializar: (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 5488	
> 5489	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 5490	
> 5491	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 5492	
> 5493	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 5494	
> 5495	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 5496	   ```bash
> 5497	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 5498	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 5499	   ```
> 5500	
> 5501	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 5502	
> 5503	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 5504	
> 5505	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 5506	
> 5507	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 5508	
> 5509	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 5510	
> 5511	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 5512	
> 5513	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 5514	
> 5515	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 5516	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 5517	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 5518	
> 5519	### SOCIAL — Next steps
> 5520	
> 5521	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 5522	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 5523	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 5524	
> 5525	### NON-CRITICAL
> 5526	
> 5527	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 5528	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 5529	- `browserslist` — ✅ updated (2026-04-26)
> 5530	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 5531	
> 5532	### GITNEXUS MCP — Next steps
> 5533	
> 5534	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 5535	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 5536	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 5537	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 5538	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 5539	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 5540	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 5541	
> 5542	### PHASE EPSILON — Next iterations
> 5543	
> 5544	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 5545	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 5546	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 5547	
> 5548	### CORE — Next iterations
> 5549	
> 5550	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 5551	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 5552	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 5553	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 5554	
> 5555	### PHASE DELTA — Next iterations
> 5556	
> 5557	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 5558	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 5559	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 5560	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 5561	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 5562	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 5563	
> 5564	### USUÁRIO ZERO — Checklist de validação
> 5565	
> 5566	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 5567	- ✅ Stripe sandbox secrets no vault
> 5568	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 5569	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 5570	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 5571	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 5572	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 5573	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 5574	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 5575	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 5576	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 5577	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 5578	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 5579	
> 5580	---
> 5581	
> 5582	## Infrastructure
> 5583	
> 5584	| Service | Container | Port | Status |
> 5585	|---------|-----------|------|--------|
> 5586	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 5587	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 5588	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 5589	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 5590	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 5591	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 5592	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 5593	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 5594	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 5595	
> 5596	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 5597	
> 5598	```bash
> 5599	docker compose up -d
> 5600	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 5601	```
> 5602	
> 5603	---
> 5604	
> 5605	## Security Model (Post-Go-Live)
> 5606	
> 5607	| Table | Isolation |
> 5608	|-------|-----------|
> 5609	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 5610	| `mcorch_edges` | Same pattern |
> 5611	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 5612	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 5613	
> 5614	---
> 5615	
> 5616	## Billing Architecture
> 5617	
> 5618	| Decision | Value |
> 5619	|----------|-------|
> 5620	| Canonical billing ledger | `profiles.mco_balance` |
> 5621	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 5622	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 5623	| Orchestration cost | 10 mcoCoins/run |
> 5624	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 5625	| Stripe | Sandbox keys active — swap to live before first client |
> 5626	
> 5627	---
> 5628	
> 5629	## GraphRAG State
> 5630	
> 5631	- **8714 total nodes** (verificado live 2026-05-31 via REST count=exact, 0 sem embedding; v6.8.6 snapshot era 8605, cujo handoff `196b7acf-9035-4d87-a19b-7d7d6b55bee0` embedded 768d via autoembed trigger pg_net) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 5632	- **9040 total edges** (verificado live 2026-05-31 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 5633	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 5634	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 5635	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 5636	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 5637	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 5638	- HNSW cosine index operational
> 5639	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 5640	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 5641	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 5642	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 5643	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 5644	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 5645	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 5646	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 5647	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 5648	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 5649	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 5650	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 5651	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 5652	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 5653	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 5654	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 5655	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 5656	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 5657	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 5658	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 5659	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 5660	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 5661	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 5662	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 5663	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 5664	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 5665	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 5666	
> 5667	### Embedding Model
> 5668	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 5669	Schema: `vector(768)` — HNSW cosine index.
> 5670	
> 5671	### Embedding Pipeline (Autônomo — 2026-05-03)
> 5672	Três camadas eliminam intervenção manual:
> 5673	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 5674	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 5675	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 5676	
> 5677	### Comandos de manutenção da Mesh
> 5678	```bash
> 5679	# Verificar nós sem embedding (deveria retornar array vazio):
> 5680	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 5681	  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 5682	
> 5683	# Backfill manual (Bun-native — requer .env):
> 5684	bun run scripts/backfill-embeddings.ts
> 5685	
> 5686	# Backfill de código-fonte nos nós AST:
> 5687	bun run scripts/backfill-node-content.ts
> 5688	
> 5689	# Re-sync AST completo:
> 5690	cd packages/gitnexus-core && npm run sync-mesh
> 5691	
> 5692	# Acompanhar re-ingesta pós-commit:
> 5693	tail -f /tmp/mcorch-ingest.log
> 5694	```
> 5695	
> 5696	---
> 5697	
> 5698	## Video Rescue Protocol
> 5699	
> 5700	When a video generation operation (Google Veo) times out or client disconnects:
> 5701	```bash
> 5702	# Via edge function (production):
> 5703	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 5704	  -H "Authorization: Bearer <user_jwt>" \
> 5705	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 5706	
> 5707	# Via local script (admin/debug):
> 5708	source .env && bun run rescue.ts <operation_id> <content_id>
> 5709	```
> 5710	
> 5711	---
> 5712	
> 5713	## Architecture Pillars
> 5714	
> 5715	| Layer | Implementation |
> 5716	|-------|---------------|
> 5717	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 5718	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 5719	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 5720	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 5721	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 5722	
> 5723	---
> 5724	
> 5725	## Phase Delta — Architecture
> 5726	
> 5727	```
> 5728	OrchestrationPage (full-canvas, p-0)
> 5729	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 5730	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 5731	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 5732	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 5733	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 5734	        ├── nodes/PublishNode.tsx    ← final distribution output
> 5735	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 5736	        └── NodePalette.tsx          ← top toolbar to add nodes
> 5737	
> 5738	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 5739	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 5740	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 5741	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 5742	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 5743	```
> 5744	
> 5745	### Canvas State Architecture (Hybrid)
> 5746	
> 5747	```
> 5748	User interaction → ReactFlow internal state (positions, drag)
> 5749	                         ↓ (debounced 600ms)
> 5750	                   localStorage (positions persist across refresh)
> 5751	                         ↑
> 5752	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 5753	     ↓ (status changes sync to ReactFlow via useEffect)
> 5754	ReactFlow renders visual status (idle/running/done/error/blocked)
> 5755	```
> 5756	
> 5757	## Key Files
> 5758	
> 5759	| Purpose | Path |
> 5760	|---------|------|
> 5761	| Architecture rules | `CLAUDE.md` |
> 5762	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 5763	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 5764	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 5765	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 5766	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 5767	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 5768	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 5769	| **Node types** | `src/components/orchestrator/nodes/` |
> 5770	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 5771	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 5772	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 5773	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 5774	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 5775	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 5776	| Billing utilities | `src/lib/billing.ts` |
> 5777	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 5778	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 5779	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 5780	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 5781	| Video rescue (local) | `rescue.ts` |
> 5782	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 5783	| Backfill script | `scripts/backfill-embeddings.ts` |
> 5784	| Deploy harness | `scripts/harness-deploy.sh` |
> 5785	
> 5786	---
> 5787	
> 5788	## First Client Onboarding Checklist
> 5789	
> 5790	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 5791	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 5792	3. ~~Activate watchdog cron~~ ✅ Done
> 5793	4. ~~Deploy rescue-video function~~ ✅ Done
> 5794	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 5795	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 5796	7. Monitor `infra_health_logs` for first 24h.
> 5797	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 5798	
> 5799	---
> 5800	
> 5801	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 5802	
> 5803	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 5804	
> 5805	| Action | Result |
> 5806	|--------|--------|
> 5807	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 5808	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 5809	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 5810	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 5811	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 5812	
> 5813	| Commit | Conteúdo |
> 5814	|--------|----------|
> 5815	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 5816	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 5817	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 5818	
> 5819	### Arquitetura Matrix Intelligence
> 5820	
> 5821	```
> 5822	ConstellationMatrix (Stabilized Engine)
> 5823	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 5824	  └── NodeDetailsPanel (Tabbed Navigation)
> 5825	        ├── Tab Meta: Neighbor exploration + Net Context
> 5826	        ├── Tab Code: Source code preview (Supabase sync)
> 5827	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 5828	
> 5829	useNodeIntelligence Hook:
> 5830	  - contentQuery: fetch nodes.content column
> 5831	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 5832	  - state: isAnalyzing, analysisResult, progress
> 5833	```
> 5834	
> 5835	---
> 5836	
> 5837	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 5838	
> 5839	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 5840	
> 5841	| Action | Result |
> 5842	|--------|--------|
> 5843	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 5844	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 5845	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 5846	
> 5847	**Output da análise (estruturado em pt-BR):**
> 5848	- Visão Geral — papel do módulo no sistema
> 5849	- Padrões Detectados — design patterns, antipatterns
> 5850	- Acoplamento & Dependências — análise In/Out-Degree
> 5851	- Recomendações — 1-3 ações priorizadas
> 5852	
> ```

## 🤖 Claude *(01:47:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"\u2500\u2500\u2500 gap/4C/goal sections in sprint-priorities \u2500\u2500\u2500\"; grep -niE \"top 3 gap|gap closure|4 ?c|## |sprint goal|top gap\" .claude/context/sprint-priorities.md | head -40",
  "description": "Locate gap/4Cs/goal sections in sprint-priorities"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── gap/4C/goal sections in sprint-priorities ───
> 3:**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 7:**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 17:**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 31:**Sprint v6.6.8 selado em 2026-05-19** — Bridge Recovery + MAPE-K Audit + SDD aios-sql-bridge + Survival Laws 4/4: sessão de auditoria reativa disparada por Sovereign observando `claw.gcrux.com/dreaming` stagnation (Imported Insights congelado em 2026-05-16, Memory Palace counts estáticos, Dream Scene "0 promovido"). **Root cause material**: Stage 2 cron `nightly-bridge-refresh.sh` invocava `node` PATH-resolved como v18.19.1 no env do user `ubuntu` apesar do interativo ter v22.22.3 — OpenClaw CLI exige v22.12+ → 100% FAIL silently em Step 3 (reindex SQLite) há ≥3 dias; Steps 1+2 (bridge + distribute) rodavam clean. **Fix dual no mesmo edit**: (1) `NODE_BIN=/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolved-target (não symlink); (2) descoberta runtime de bug latente segundo — `claw-master` foi adicionado em v6.3.1 ao distribute script MAS NÃO ao indexer loop (`for agent in main artisan engineer scientist marketing-growth guardian; do` omitia claw-master) → `claw-master.sqlite` stale May 16 → exatamente o checkpoint "AIOS Core v2 (2026-05-16)" que Sovereign observou na UI. **SOP first per Lei 2**: `docs/processes/openclaw-bridge-recovery.md` 86 LOC autorada ANTES do edit. **5 phases materializadas** (todas com ORO triplet + Survival Laws ✓): Phase A (bridge fix + claw-master loop), Phase B (MAPE-K closed-loop audit + 4 observation nodes em mesh — Plan `a4c4c026` / Execute `69f6e356` / Monitor `d605bdda` / Analyze `d8952ce8` com edges DERIVES_FROM v6.6.7), Phase C (9 untracked files versionados via 3 commits: miv landing assets + miv tools + memory audit trail), Phase D (esta seal + milestone `c4643058`), Phase E (OTD-SSP01-001 closed via SDD `aios-sql-bridge` 376 LOC enterprise-grade + 00-index 69 LOC suite skeleton + documentation_suite seal `4e0acc7e` stability 0.85 DERIVES_FROM openclaw seal). **Material proofs**: 6 commits granulares pushed (`03911e9` fix(cron) + `cbdee4f` feat(landing) + `bb1cc96` chore(tools) + `2aa80f1` chore(memory) + `1b3bdd8` docs(bok) + `b71b991` docs(handoff) + `230ad70` docs(readme)); 7/7 SQLites OpenClaw reindexed (was 0/6 fail); log final `[2026-05-19T19:06:32-03:00] nightly-bridge-refresh DONE (zero failures)`; mesh **8359 nodes** (+6 desta seal); TS zero erros; 5 containers healthy. **Survival Laws Self-audit 4/4 ✓ pela primeira vez consecutivamente desde v6.6.0** — encerra retroativamente OTD-PROC-001 (RPN 60) + OTD-PROC-002 (RPN 40) + OTD-SSP01-001 (RPN 240 SLA 2026-05-24). **Pending TOP**: OE-661 Step 1.5 first-run E2E (Sovereign click `/dashboard/orchestration` TriggerNode); OTD-OE661-PER-USER refactor (SLA 2026-06-02, 14 dias); MAPE-K gaps 1/2/3 implementáveis em v6.7.x/v6.8.x conforme plans dedicados (recomendações registradas no mesh, aguardam acionamento).
> 35:**Sprint v6.6.6 selado em 2026-05-19** — Planning Seal + Debt Audit + Self-audit Retroativo: sessão dedicada a (a) `/handson` brief v6.6.5; (b) persistir execution plan dos 3 carry-overs OE-661 + Ledger SOP + Canvas 4.2c por diretiva Sovereign "slave o plano atual para posteriormente implantar"; (c) auditoria completa em 3 frentes paralelas; (d) emendas críticas; (e) /handoff oficial. **Zero código de produção tocado**. Plan persistido em `.claude/context/execution-plan-oe661-carryovers.md` (~403 LOC, md5 `0e5f0ba9...`) + observation node `3dde2572-cad6-491b-b523-c56ec763ff8e` (autoembed 768d). Audit em `.claude/context/audit-2026-05-19-oe661-debt-sweep.md` (~297 LOC, md5 `5c4f8a9f...`) + observation node `6164c80f-cadd-48d5-95a4-f87f22ebd09b` + DERIVES_FROM edge `acb4b0d9-091d-4973-96a8-d40515be7990`. **21 OTDs ativos catalogados (8 RPN ≥ 100): VM-OTD-001 RPN 288 viralmind HNSW · OTD-SSP01-005 RPN 280 admin claim · OTD-SSP01-001 RPN 240 SLA 2026-05-24 · OTD-V660-002 RPN 150 · VM-OTD-004 RPN 140 · OTD-V660-001 RPN 120 (coberta pelo plan Phase 2) · OTD-V660-003 RPN 80 · OTD-CV42C-001**. **5 inconsistências processuais**: (1) **5 seals consecutivas (v6.6.1..v6.6.5) omitiram bloco mandatory Survival Laws Self-audit** — Severidade ALTA; (2) Survival Audit v2 não re-rodado em 32 dias; (3) 3 SOPs implícitas não formalizadas; (4) HANDOFF v6.6.3 claimed 4 content_mesh_asset mas reality = 1 row (3 "products" têm `node_type='feature'`); (5) `handle-ml-postback` cego — zero `infra_health_logs` em 17 dias. **4 bugs concretos no plan**: A race condition obs+asset não atômicos · B wpPostUrl null não gated · C Link Forge query global sem project_id · D postback content_id drift. **10 amendments aplicados** (A-J) via Amendments Appendix no topo do plan. Schema drift fixed: `infra_health_logs.created_at` NÃO EXISTE (real: `last_seen_at`). **Predicted Survival Audit v3** (não emitido formalmente): Memory 5/5 · Skill 4/5 · Cost Discipline 4.5/5 ↑ · Observability 4/5 ↑ · SOP 5/5 · **avg 4.4/5 · min 4/5** — Phase Commercial threshold mantido. **Material proofs**: 14 integrity checks paralelos · 4 commits granulares (`ea7efaf` plan + `44e464c` audit + `fb6f07d` README + `99d70f6` handoff seal) push → origin/main · milestone handoff node `821dc554-78e2-4abb-999d-37363c5df6c9` embedded 768d · mesh total **8352 nodes** (+4 desde v6.6.5). **Próximos deliverables**: (a) Sovereign autoriza execução das Fases 1-3 do plan quando convier (bugs A-D já fixed); (b) **atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias)** — BoK Gate override `aios-sql-bridge` precisa SDD; (c) provisionar `SUPABASE_POOLER_URL` (OTD-V660-003); (d) materializar Survival Audit v3 formal antes de Phase Commercial; (e) executar Phase 2 do plan (SOP `mcoins-ledger-reconciliation.md`) — Sovereign-only — fecha OTD-V660-001.
> 39:**Sprint v6.6.4 selado em 2026-05-18** — Gamificação-Nodes BoK 9/9 (retroativa + BoK Gate liberado): débito documental herdado do override consciente do BoK Gate (Sprint v6.3.0, SLA originalmente 29/05) quitado em sessão única. 5 docs autorados manualmente seguindo `.claude/agents/bok-scribe/templates/` (Plano B sobre `/bok-scribe` Skill, que sobrescreveria os 4 docs existentes): `06-data-model.md` (DMBOK v2 ~277 LOC — schema canônico `profiles.mco_balance` + `mcoin_transactions` + 3 RPCs SECURITY DEFINER `award_mco_coins`/`deduct_mco_coins`/`add_user_score` com loyalty 100:1), `07-process-flow.md` (BPM CBOK v4 ~309 LOC — 9 PROC-GN-* em swimlanes com refs precisas `award-mco-coins/index.ts:78` cap-per-action, `canvas-execute/index.ts:133-148,349` cap-canvas-agregado + atomic deduct, `orchestrate-content/index.ts:60` pre-flight deduct, n8n `autonomic-action` trail loyalty), `08-quality-metrics.md` (CMQ/OE BOK ~215 LOC — 10 KPI-GN-* + 10 FMEA-GN-* com 4 RPN > 100, 6 SOL-GN-*, observability completa em `infra_health_logs`), `02-brd.md` (BABOK v3 ~188 LOC — 12 BR-GN-* + 5 BO-GN-* SMART + Risk Register + Traceability Matrix), `00-index.md` (~122 LOC — Document Registry 9/9 + Traceability Chain MR→BR-GN→FR→PROC-GN→KPI-GN + Convergence Note registrando drifts + 5 OTDs incluindo 2 herdadas OTD-V660-001/002). **Drift BoK ↔ código (3 itens) reconciliado via patches cirúrgicos sub-10-linhas preservando git blame**: (1) `04-frd.md` R3 "streak reseta 24h" deprecado inline → R3a (cap-per-action) + R3b (cap-canvas-agregado); (2) `05-sdd.md` ganha §4.2 documentando trilha n8n loyalty ausente do SDD original; (3) `01-mrd.md` L114 BRD externo inexistente substituído por `02-brd.md` local. **Mesh seal** `scripts/seed-gamificacao-nodes-bok-seal.ts` (mirror 1:1 viralmind seal): node `bok-scribe-seal-gamificacao-nodes-v1` UUID **`6e8546bc-d995-4cc5-ac88-06cecbece181`** inserted stability 0.85 · DERIVES_FROM `bok-scribe-seal-viralmind-v1` · `revenue_impact: 0` (módulo é enabler de retenção/ARPU) · autoembed via `trg_mcorch_embed_on_insert` (pg_net 768d). **BoK Gate liberado** para código novo no módulo `gamificacao-nodes`. Atenção: features ledger-touching (Stripe top-up, marketplace) seguem bloqueadas até OTD-V660-001 (drift 2 users) fechar via SOP `mcoins-ledger-reconciliation.md`. **Debt registry geral atualizado**: `viralmind` 9/9 ✅ · `conteudo-v2` 9/9 ✅ · `mcorch-constellation` 9/9 ✅ · `gamificacao-nodes` 9/9 ✅. `openclaw` BoK ainda pendente (override consciente original do v6.2.0). **Material proofs**: TS zero erros · 122/122 testes em 3.34s · BoK Gate validator loop ✅ 9/9 · ~1111 LOC novas + ~30 LOC patches surgical · seal UUID confirmado via INSERT RETURNING · mesh total **8344 nodes** (+1 desde v6.6.3). **Próximo deliverable**: (a) executar SOP `mcoins-ledger-reconciliation.md` para fechar OTD-V660-001; (b) carry-overs v6.6.3 (`GCRUX_ML_AFFILIATE_TOKEN` provisionar + wire orchestrate emitir content_mesh_asset + primeiro run Usuário Zero OE-661 flywheel).
> 41:**Sprint v6.6.3 selado em 2026-05-18** — OE-661-ROADMAP Debt Liquidation: sessão única liquidando 3 das 4 dívidas declaradas em CLAUDE.md (Financial deferred por decisão Sovereign até Usuário 1) + dívida implícita OE-661-003 Target Binding. **(Phase 0 Hybrid restore)** `process-affiliate-link/index.ts` (POST original 234 LOC tinha sido refatorado em -222 LOC para redirect 302 puro — quebrava `ContentLibraryPage.tsx:744`). Hybrid restaurado: GET 302 público (no-verify-jwt, redireciona a `panel.gcrux.com/api/ml-redirect`) + POST autenticado original (probe HEAD + self-heal ML search + insert em `affiliate_links`). Deploy 78.31 kB. **(Phase 1 Postback Debt)** `handle-ml-postback` captura `obsNode.id` da observation inserida + cria edge `ATTRIBUTES_REVENUE_TO` (source=observation, target=content_mesh_asset preferred + fallback OR, weight=revenueCents). `.maybeSingle()` para tolerar zero matches. Deploy 59.34 kB. Smoke chain (synthetic): test affiliate_link `adb9e131` → observation `f65d52b2` → edge `65d072fe` → content_mesh_asset `f3a091f7`. **(Phase 2 Auto-Stitching OE-661-003)** `embed-mcorch-node/index.ts` ganha `autoStitchObservation()` que regex-extrai file paths do conteúdo + nome (.ts/.tsx/.js/.md/.sql/.sh/.json/...) e cria edges `observes` para ast_file/markdown_file/vault_note correspondentes; fallback obrigatório a `root:CLAUDE` (`2747e164`) quando nenhum path resolve. Deploy 105.1 kB. Retrofit: `stitch-fallback.js` (fix OR `root:CLAUDE`) costurou 6 orphans pré-existentes; `audit-mesh-edges.ts` (fix schema `type`→`node_type`) reporta **10/10 observations VALID — 100% Target Binding coverage**. Live auto-stitch confirmado em re-embed `{stitched:1}` edge `2e1e57db`. **(Phase 3 Link Forge OE-661-004)** Novo `scripts/link-forge.ts` (Bun-native, mirror backfill-embeddings) varre content_mesh_asset, aplica 3 regex (Roborock S8 MLB3981745621 · Samsung Neo QLED 8K MLB3546719283 · Family Hub MLB3728491023), substitui menções por markdown links para `panel.gcrux.com/api/ml-redirect?...&utm_content=$node.id`, UPDATE atomic + `CONTAINS_LINK_FOR` edge para product node criado on-demand. Flag `--dry-run`. Smoke: dry-run preview 179→905 chars; live 1 content updated + 3 edges (`884fceef`/`f4f4146c`/`c834ca23`) + 3 product nodes (`77ac9b9f`/`3d12ac89`/`92a60fc0`). Pendência: `GCRUX_ML_AFFILIATE_TOKEN` ainda DEFAULT na vault — provisionar antes do primeiro run real. **(Phase 4 Memory ingest)** 4 markdown_files autoembed via trigger pós-upsert: `8ad38681` gateway-recovery.md (Memory Debt sealed), `549e01a4` roadmap-v1.md, `5e957727` revenue-flywheel.md (recém ingerido), `d1296632` link-forge-scope.md. **Material proofs**: 8 commits granulares (56ed242 hybrid affiliate · dfabb17 postback · 1f368c1 auto-stitch · 140f248 link-forge · 27c7105 skills+docs+utility · c12906b CLAUDE+BoK rule · b8f5702 handoff seal · este sprint update); TS zero erros (após fix node symlink `/home/ubuntu/.local/bin/node`); 122/122 testes em 3.39s; 3 Edge Functions deployed (`process-affiliate-link --no-verify-jwt` · `handle-ml-postback --no-verify-jwt` · `embed-mcorch-node --no-verify-jwt`); milestone node `6f2cf405-4bb5-440b-a02a-9579fc39f29f` embedado (768d); mesh total **8343 nodes** (+7 desde v6.6.2) · **11617 edges** (+1555 entre observes retrofit, ATTRIBUTES_REVENUE_TO, CONTAINS_LINK_FOR, e autoembed cascade). **Próximo deliverable:** (a) provisionar `GCRUX_ML_AFFILIATE_TOKEN` na vault Supabase; (b) wire `orchestrate-content` (ou processo equivalente) a emitir `content_mesh_asset` nodes pós-geração — sem eles Link Forge é noop em produção; (c) primeiro run end-to-end Usuário Zero validando flywheel completo (gera → publica → ML afiliado → postback → ATTRIBUTES_REVENUE_TO → ROIWidget); (d) Stripe Financial Debt continua deferred (decisão Sovereign — sandbox enquanto Gabriel valida como Usuário Zero).
> 43:**Sprint v6.6.2 selado em 2026-05-17** — Canvas Studio Phase 4.2c — Async Video Pipeline Live: três rounds em sessão única destravando todos os providers de imagem do Canvas + backbone async Higgsfield. **(Round 1)** Phase 4.2c wiring shipped — `canvas-execute` ganha branch dedicada `image_to_video` que submete ao endpoint `higgsfield-ai/dop/standard` com `?hf_webhook=<URL-encoded callback>` (per validation doc), persiste `vm_canvas_executions.operation_id` + `webhook_token` (64-hex unique), retorna `{status:'queued'}` em <2s; débito atômico só no webhook após upload-OK (`deduct_mco_coins` `action='canvas_video_spend'`). Hook `useCanvasJobsRealtime` extendido com callback `onUpdate(row)` que reconcilia Zustand store. `CanvasEditorPage` monta Realtime + Run-All BFS fire-and-forget para video. `ImageToVideoInspector` Run button real + tier-gate UI (apenas `dop-standard-5s` clicável; Lite/Turbo/Kling/Seedance disabled com tooltip "Aguardando validação tier — Phase 4.3"). SOP `docs/processes/canvas-video-async-execution.md` (~190 LOC) escrita ANTES do código (Lei 2). Watchdog cron `scripts/canvas-video-watchdog.sh` (~95 LOC, bash + PostgREST + jq) — poll Higgsfield a cada 5min, marca `timeout` em jobs travados >60min, idempotente via HTTP 409 do webhook. Dry-run validado material: `[2026-05-17 21:54:35] 0 jobs to check` + health UUID `38c860f5-8d8d-4ae7-b54d-316f26678410` em `infra_health_logs`. **(Round 2 — assertExecuteSuccess Lei 1)** Smoke test revelou inspector mentindo: toast `"Geração concluída — 15 💎 debitados"` quando backend marcava `status='failed'` (saldo Sovereign confirmou intacto em 5533 — frontend mentindo, backend correto). Causa raiz: `canvas-execute` retorna HTTP 200 + `error` field, `mutateAsync` não throw, frontend tratava qualquer 200 como sucesso. Novo util `src/lib/canvas-execute-result.ts` faz `assertExecuteSuccess<T>(result)` que THROW em `result.error` set OU `status ∈ {failed,timeout,cancelled}`. Aplicado em 4 inspectors + Run-All. Toast agora usa `result.credits_charged ?? cost` (zero quando falha). Migration `20260518012541_canvas_assets_update_policy.sql` adiciona UPDATE policy (necessária para `upload({upsert:true})` que vira `INSERT...ON CONFLICT DO UPDATE`). **(Round 3 — 4 bugs novos)** **(A)** OpenAI `dall-e-3` E `gpt-image-1` HTTP 400 `Unknown parameter: 'response_format'`. Removido o param fixo; upload block agora baixa URL provider→canvas-assets server-side (mirror `rescue-video:39-77` + `higgsfield-webhook:144-167`); `storedKey`/`storedContentType` propagados pro asset row. **(B)** OpenRouter `/v1/images/generations` retorna 404 HTML (endpoint deprecated). `generateOpenRouter` migrado para `/v1/chat/completions` com `modalities:["image","text"]` parseando `choices[0].message.content[].image_url.url` (+ fallback `message.images[]`). Catálogo `types/canvas.ts` ganha 2 entries OR funcionais (`openrouter-gemini-image` $0.039 + `openrouter-flux-pro` $0.04); `openrouter-dall-e-3` permanece deprecated com banner amber. `MODEL_GROUPS` restaurado. OTD-CV42C-001 registrada para Phase 4.3 (picker dinâmico via OR `/v1/models` com free tier). **(C)** Replicate "key not configured" — coluna `replicate_api_key` NUNCA existia em `user_api_keys`. Migration `20260518020028_user_api_keys_replicate.sql` adiciona. `types.ts` ganha campo manual em Row/Insert/Update (evita full regen). `SettingsPage` ganha KeyField. Inspector ganha banner per-provider (openai/openrouter/replicate) quando user key falta com link `/dashboard/settings`. **(D)** Storage RLS 403 persistente em character upload. Investigação revelou NOTICE crítico no `db push`: `policy "Public read canvas assets" does not exist, skipping` — confirma que migration original `20260514040200` aplicou apenas 3 de 4 policies no remoto. Migration `20260518020030_canvas_assets_rls_repair.sql` (idempotente, DROP IF EXISTS 8 nomes + recria 4 policies) usa `TO public + auth.uid() IS NOT NULL` (defensivo contra publishable key `sb_publishable_*` que pode não resolver `TO authenticated`) + `owner = auth.uid()` fallback em UPDATE/DELETE. **Material proofs:** TS zero erros · 122/122 testes em 4.40s · build em 23.55s · `CanvasEditorPage` chunk 113.66 kB · `canvas-execute` 138.3 kB · 4 commits granulares (`6554cb4` canvas src · `76c99e3` 3 migrations · `9615c69` readme · `0d7bc07` handoff) · push `cc828a0..0d7bc07` para origin/main · milestone node `eb0b3ae0-9ec1-4328-ad31-1b079d3f294e` embedado (768 dims) · saldo Sovereign **5533** intacto · mesh total **8336 nodes** (+8 desde v6.6.1). **Próximo deliverable:** (a) smoke test pago DoP Standard 5s ($0.56) — Sovereign valida gates 4-9 da SOP; (b) cron install do watchdog (`crontab -e` adicionando `*/5 * * * * scripts/canvas-video-watchdog.sh`) após smoke passar; (c) OTD-CV42C-001 dynamic OR model picker — Phase 4.3 spec dedicada.
> 45:**Sprint v6.6.1 selado em 2026-05-17** — Pantheon Configuration + Memory Wiki Seed Manual + Config Drift Fix: três trilhos sequenciais resolvendo o "Zero Memory Wiki" gap. **(Phase 1 Pantheon Configuration Audit)** Audit por Explore agent revelou que 7 agentes OpenClaw tinham canonical files incompletos. Materializados: 7 MEMORY.md scaffolds + 7 BOOTSTRAP.md birth certificates + main SOUL.md enhanced (preserva genérico Claude Code + anexa MCORCH Pantheon Layer com routing logic + delegation map + fallback) + HEARTBEAT.md tasks (main + claw-master) + `.claude/context/pantheon-role-matrix.md` consolidação authoritative (7 agentes × BoK lens × decision scope × routing × cron pipeline × active debt) + `~/.openclaw/agents/main/README.md` documentando workspace canonical = repo. `.gitignore` ganhou DREAMS.md + .openclaw-repair/ + BOOTSTRAP.md + MEMORY.md. Mesh seal observation `ccecdbd1-8007-40c4-8c88-fb3463b6fe55`. Commit `d327c49`. **(Phase 2 Memory Wiki Seed Manual MCORCH-aware)** Sovereign reportou Memory Palace + Imported Insights renderizando empty state apesar de `memory-wiki.enabled=true`. Investigação: painéis filtram `kind ∈ {synthesis, entity, concept}` (Palace) OU `sourceType=chatgpt-export` (Insights); vault tinha 6363 sources mas todos `memory-bridge`. Doc oficial confirmou cron `Memory Dreaming Promotion` (05:00 BRT) só promove para MEMORY.md per agent — NÃO auto-cria palace pages. Schema reverse-engineered de `apply.ts:181-222` + `lint.test.ts` + `ingest.ts`. 20 markdown files autorados via fs.writeFile em `~/.openclaw/wiki/main/{syntheses,entities,concepts,sources}/`: 5 syntheses + 8 entities + 6 concepts + 1 source chatgpt-export preservando conversa AIOS Core v2 de 2026-05-16 (riskLevel=medium, materiality audit pendente). Mesh seal observation `569ba6bf-b2df-443e-9bba-b0c064032ab7`. **(Phase 3 Config Drift Fix agents.list enabled key)** Investigação Memory Wiki UI persistindo "not enabled" revelou: schema strict v2026.5.14 rejeita campo `enabled` em entries de `agents.list` (presente em 6 de 7 entries). `config validate` retornava 6 "Unrecognized key" errors → `config.get` RPC retornava `configSnapshot.config = null` ao UI → `xS('memory-wiki', {enabledByDefault: false})` resolvia false → UI mostrava "not enabled" UNCONDITIONALLY. claw-master emitiu proposal `.claude/proposals/openclaw-agents-list-enabled-key-drift-v1.md` (Path A jq surgical recomendado, Path B doctor --fix). Path A executado: snapshot `/tmp/openclaw.backup-20260517T200945Z.json` (5591 bytes) → jq `.agents.list |= map(del(.enabled))` → diff confirmou 6 deletions limpas → atomic mv → md5 mudou 4a4f55→b522e8 → `config validate` retornou "Config valid" → daemon restart (PID 38702→608136, gateway healthy, zero stability events) → CLI plugins list restored ("Plugins (72/122 enabled)" com Memory Wiki entre enabled). Commit `af68752`. **Confirmação visual Sovereign:** Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions; Imported Insights renderiza 1 cluster "Other" (AIOS chat medium risk). **3 commits granulares** (d327c49 pantheon + af68752 proposal+fix + 637d108 readme + bc27355 handoff) · TS zero erros · 3 mesh seals · milestone node `d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17` embedado (768d openai/text-embedding-3-small) · mesh total **8328 nodes**. **Próximo deliverable:** (a) Materiality audit Lei 1 de `supabase/functions/aios-chat/index.ts` para validar/refutar capability AIOS de invocar aios-sql-bridge (números 12500/12500/Drift=0 reportados sem prova material); (b) OE01 bridge JWT ainda Cérebro sem mãos; (c) OpenClaw CLI drift OTD-V660-002 follow-up; (d) Canvas Studio Phase 4.2c implementation (desbloqueado por OE04 desde v6.6.0).
> 47:**Sprint v6.6.0 selado em 2026-05-17** — SSP-01 Repair & REM Cycle (OE01-OE04): continuação direta da v6.5.0 no mesmo dia, fechando o P0 e desbloqueando Canvas 4.2c. **(OE01)** Admin role do Sovereign confirmado material via service-role REST (HTTP 200, role='admin', created_at=2026-04-17 — divergência com claim "ZERO admin" de v6.5.0 registrada). Bridge end-to-end com JWT é Cérebro sem mãos — Sovereign valida quando convier. **(OE02)** Insert sintético `opening_balance_reconciliation` em `mcoin_transactions` para Sovereign: UUID `4caa9314-2fdf-4d60-9cb2-b7ed63bbcf5a`, amount=5533, drift agora `mco_balance(5533) − Σledger(5533) = 0`. **(OE03)** Refator das rotinas noturnas em 3 estágios canônicos espaçados 2h em horário BRT: `nightly-stage1-light-sleep.sh` 03:00 (IO: rotação de logs + temp cleanup + spot check com pulse infra_health_logs), `nightly-stage2-deep-sleep.sh` 05:00 (integridade: wrapper de `nightly-bridge-refresh.sh` + ledger drift watch alert-only + VACUUM ANALYZE), `nightly-stage3-rem.sh` 07:00 (inteligência: `news-impact-analyzer.ts` OpenRouter perplexity/sonar web-grounded + `morning-briefing.sh` ao Telegram bot @claw_gcrux). `compose-morning-briefing.ts` ganhou seção `*News Pulse:*` lendo último nó `node_type='news_pulse'`. SOP `docs/processes/nightly-circadian-cycle.md` (140+ linhas) escrita ANTES dos scripts (Lei 2). Server timezone `America/Sao_Paulo (-03)` confirmado via `timedatectl`. Crontab swap atômico (backup em `/tmp/crontab.backup-*.txt`). Smoke tests: Stage 1 EXIT 0 healthy · Stage 2 EXIT 0 detectou pre-existing OpenClaw CLI drift (OTD-V660-002) · Stage 3 EXIT 0 briefing DELIVERED. **(OE04)** `supabase/functions/canvas-execute/index.ts` ganhou daily cap 100 mcoCoins/24h por user (query `mcoin_transactions` action LIKE `canvas_%spend`, HTTP 402 estruturado, fail-open em erro) + action tagging na chamada `deduct_mco_coins` (`canvas_image_spend` ou `canvas_video_spend` + context completo). `src/components/dashboard/DashboardLayout.tsx` ganhou import sonner + `LOW_BALANCE_THRESHOLD=50` + toast.warning na carga inicial e em transição via Realtime (dedupe `id='low-balance'`) + amber pill no header quando balance < 50. SOP `docs/processes/canvas-daily-cap-handling.md` (90+ linhas) escrita ANTES do código (Lei 2). Deploy `canvas-execute` **132.6 kB** (+0.4 vs v6.5.0). Build 20.38s sem regressão. 122/122 testes passam. TS zero erros. **Survival Audit v2** (`.claude/context/survival-audit-v2.md`, 170 linhas): Memory 5/5 · Skill 4/5 · **Cost Discipline 4/5 ⬆** · Observability 3/5 · **SOP 5/5 ⬆**. Min 3/5, média 4.2/5. Por diretiva Sovereign OE04 explícita ("score ≥ 4 destrava 4.2c"), **Canvas Studio Phase 4.2c DESBLOQUEADO**. 9 commits granulares (`97cdf83` `436b4e2` `ff03bfd` `23c916a` `3bd9288` `95900db` `23c3792` `dcc592b` `6836288`) + handoff seal. Milestone node `4f12a88b-1b42-484a-abb8-776fe5cd1560` (autoembed 768d via trigger). 4 OTDs novos (V660-001..004). **Próximo deliverable:** (a) bridge end-to-end com JWT Sovereign; (b) resolver OpenClaw CLI drift (V660-002); (c) Canvas Studio Phase 4.2c implementation (fork canvas-execute para vídeo async + wire useCanvasJobsRealtime + watchdog polling + enable ImageToVideo).
> 53:**Sprint v6.3.1 selado em 2026-05-16** — OpenClaw Neural Bridge + Departmental Army Pantheon: Zero-Memory Crisis do OpenClaw fechada. Bridge `scripts/bridge-mesh-to-openclaw.ts` (327 LOC, mirror do padrão `backfill-embeddings.ts`) exporta 8239 `mcorch_nodes` em Two-tier hybrid (Tier 1 = 375 strategy nodes com full content + YAML frontmatter; Tier 2 = 2527 AST symbols com path + signature + 200-char summary; `ast_variable` excluído como ruído — 5336 entradas triviais de `const x = ...`). `scripts/distribute-mesh-to-agents.ts` (275 LOC) materializa file copies (não symlinks — indexer não segue) com modelo "shared base + agent-specific overlay" aprovado pelo Sovereign: shared base de 4 dirs (decision/milestone/system/handoff) para os 6 agentes + overlays específicos (engineer ganha toda Tier 2 + architecture/observation; scientist ganha documentation_suite/requirement/conversation/vault_note/markdown_file; artisan ganha conversation/ui-ux/feature; marketing-growth ganha feature + `revenue-flagged/` materializado via filter regex; guardian ganha observation + `_meta/`; main lê `mcorch-export/` direto pois workspace IS o repo). Squad escalado de 4→6 agentes — Pantheon Architecture L1 (engineer · scientist · artisan · marketing-growth NOVO com SOUL focado em Apollo/Affiliates/GCRUX) + Coordination Layer (main synthesizer · guardian NOVO com SOUL focado em Nightly Dreaming + Telegram briefing + CLAUDE.md proposals PR-style). `~/.openclaw/openclaw.json` agents.list atualizado; AGENTS/HEARTBEAT/IDENTITY/TOOLS/USER copiados do engineer template. `.claude/agents/openclaw-soul-template.md` (236 linhas) codifica L1/L2 inheritance + scaffolding protocol. Bootstrap indexing rodado nos 6: **9185 chunks total** (main 4439 · engineer 2591 · scientist 1824 · artisan 113 · marketing-growth 60 · guardian 58). Cron pipeline triplo instalado: 02:30 `nightly-bridge-refresh.sh` → 03:00 OpenClaw nativo `Memory Dreaming Promotion` → 03:30 `morning-briefing.sh` (composto por `compose-morning-briefing.ts` com 6 seções markdown ≤4000 chars; POST plain-text ao Telegram bot 8668689828; primeira entrega ao Sovereign chat 5835174772 com msg_id 201). Failure paths espelham `watchdog-mcorch.sh:69-131` (incident JSON em `/tmp/openclaw-incidents/` + POST best-effort ao gateway). CLAUDE.md ganhou seção "Departmental Army (Pantheon Architecture)" + 11 novas Key Files Reference entries + warning explícito "NUNCA pnpm no repo" (descoberto: pnpm move pacotes bun-installed para `node_modules/.ignored/`). 4 commits granulares (271bc58 bridge · 7e709f4 distribute · fd66185 cron · 4f88e04 docs). TS check zero erros. Milestone node `c1dbc53b-3a27-4da7-aef3-debd5c4047a0` embedado. 4 OTDs registrados (destaque: OTD-V631-001 RPN 280 — OpenClaw BoK SLA 7d expandido por esta sprint, recomendado `/bok-scribe openclaw` imediato). **Próximo deliverable: (a) `/bok-scribe openclaw` (zera SLA do override consciente v6.2.0); (b) Canvas Studio Phase 4.2b (`vm_canvas_jobs` + `higgsfield-webhook`).**
> 61:## 📊 4Cs Audit Snapshot (2026-05-04)
> 74:## 🔴 Top Gap Closures (by leverage)
> 76:1. ~~**Loop/rotina de cadência**~~ ✅ `audit-4cs.sh` toda segunda 09:00 BRT · `auto-publish-cron.sh` */5min · `watchdog` */5min
> 97:## 🛠️ Skills a criar ou evoluir
> 105:## 🔌 Conexões a implementar
> 113:## ⏱️ Loop / rotina
> 121:| Audit 4Cs semanal | `0 12 * * 1` (seg 09:00 BRT) | `scripts/audit-4cs.sh` | `/var/log/mcorch-audit.log` |
> 126:## 📚 Knowledge Mesh Update
> 133:## ✅ Definition of Done (por tarefa)
> 143:## 3Ms deste Sprint
> 145:### Mindset (Default Shift)
> 149:### Method (O que vale automatizar)
> 151:- audit-4cs.sh coleta métricas objetivas sem IA — sustentável por anos
> 153:### Machine (Assets técnicos ativos)
> 155:- Crons: watchdog + auto-publish + audit-4cs + ast-ingest
> 160:## 🔁 Sprint Retrospective (responder ao final com `/handoff`)
> 166:5. Score 4Cs pós-sprint vs pré-sprint: melhorou em qual C?
> ```

## 🤖 Claude *(01:48:49)*


## 🤖 Claude *(01:49:14)*

All context gathered and materially verified this turn. Here's the pickup brief.

═══════════════════════════════════════════════════════════
  **HANDSON — v6.15.2** · OTD/Drift Reconciliation + Fabrication Remediation (2026-05-31)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
Fase selada: **v6.15.2 — Reconciliação documental** (zero código de produção; três itens "pendentes" do roadmap estavam, na verdade, já resolvidos — labels estagnados, não o sistema).
Working tree **limpo · sincronizado com `origin/main` (0↔0)**. Últimos commits:
```
bec5be2  docs(handoff): seal v6.15.2 — OTD/drift reconciliation + fabrication remediation
c5007da  docs(readme): v6.15.2 — OTD/drift reconciliation + fabrication remediation
84b5d4c  docs(handoff): Canvas DoP paid smoke DONE — 6 real charges + 15MB video
9607a44  docs(handoff): reconcile GraphRAG State → 8714 nodes / 9040 edges
4fdd226  docs(claude): close OTD-OE661-PER-USER in API Tenancy registry
```

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ · `scratch/` limpo ✅

🏗️ **INFRA** (verificado este turno — 8 dias uptime)
```
mcorch_chroma:      Up (healthy) · Chroma API v2 heartbeat OK
mcorch_claude_mem:  Up (healthy)
mega-brain-daemon:  Up (healthy)  ·  webhook (healthy)  ·  dashboard (up)
```

🧠 **KNOWLEDGE MESH** (fonte: GraphRAG State, verificado live REST `count=exact` hoje)
**8714 nós · 9040 arestas · 100% embedded** (768d HNSW cosine) — +1 handoff node do selo v6.15.2 ≈ 8715 live.
Tipos presentes: handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite · crew_agent · feature · ui-ux · content_mesh_asset + AST (file/function/interface/class). *(footer não rastreia N por tipo — não fabrico contagem.)*
⚠️ **Anomalia flagada**: arestas caíram **11925 (v6.6.9) → 9040** (−2885), causa não confirmada.

🔧 **TYPESCRIPT** — `tsc --noEmit` exit 0, **zero erros** ✅

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
**11/11 suítes COMPLETAS 9/9** — gate liberado para código em qualquer módulo:
`aios-sql-bridge · canvas-design · conteudo-v2 · e2e-user-zero · gamificacao-nodes · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · viralmind`
Seal nodes verificados (stability 0.85): `viralmind-v1` `5c4bf1e9` · `gamificacao-nodes-v1` `6e8546bc` · `openclaw-v1` `05c55dfd`.
**Nenhum bloqueador de BoK Gate.** ✅

📌 **SPRINT**
Goal: *Distribuição social autônoma operacional* (LinkedIn auto ✅ · Twitter aguarda tier · Instagram aguarda App Review Meta).
⚠️ 4Cs Audit Snapshot está **estagnado em 2026-05-04** (~27 dias) — cron `audit-4cs.sh` roda às segundas; vale rodar `/audit` fresco.

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **OTD-LLM-FALLBACK — Cascading LLM Fallback · SLA 2026-06-07 (7 dias)** — Resilience Debt, owner `engineer`. **Deadline mais próximo do roadmap.** É o único item com SLA ativo batendo na porta.
2. **Re-ativar flywheel Usuário Zero** — na última sessão os artefatos do "1º E2E" estavam **todos zerados** (`content_mesh_asset`/`affiliate_links`/`pipeline_runs`/`ATTRIBUTES_REVENUE_TO`/`revenue_cents` = 0; possível soft-reset/cascade LGPD, **não confirmado**). Re-rodar o E2E para repopular o pipeline é o gate de `revenue_cents > 0` → lançamento comercial.
3. **Build-ready (escolha do Sovereign):** Canvas Design module (`nexu-io/open-design` — BoK 9/9 pronta) **ou** e2e-user-zero 2ª iteração (~590 LOC: 6 flows + redactor LGPD + mesh-persistor + telemetry + selftest + pre-commit hook).

⚠️ **ALERTAS** (nada quebrado — itens materiais a vigiar)
- **Flywheel cold-start**: artefatos de receita Usuário Zero = 0 (origem não confirmada — investigar antes de reivindicar E2E).
- **Anomalia de arestas**: −2885 desde v6.6.9, causa desconhecida — questão de integridade da malha.
- **SLA OTD-LLM-FALLBACK** vence em 7 dias.
- Infra/TS/BoK/git: **nenhum alerta** ✅

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

Qual frente o Maestro quer atacar? Minha recomendação: **#1 (OTD-LLM-FALLBACK)** pela pressão de SLA, ou **#2 (re-ativar o flywheel)** se a prioridade for destravar receita. Posso também investigar primeiro as duas anomalias materiais (artefatos zerados + queda de arestas) antes de qualquer build, se preferir fechar as incógnitas.

## 👤 User *(02:16:25)*

Não é um anomalia de arestas, fizemos uma poda geral, realmente foi removido varias coisas, mas sim verifique pois a poda foi feita com a intuição de remover o enterprise constalattion para começar a por para rodar os agentes de verdade. Veja na imagem como é hoje poluido e atrapalha muito o desempenho da pagina, sem contar que tem diversos erros de z-index ficando dificil o UX e UI. Essa constelação deveria operar em todo o ecosistema, os agentes ali devem se comportar de forma que conseguem utilizar os modulos que temos, de conteúdo, canvas design e studio, viral miner, blog, calendario, orquestração, campanhas, produtos, afiliados, Analytics, Core e IA Arena e o core central que hoje ja existe tambem pode usar o Dashboard
agent-economics... 

Mas antes de fazer um hard reset em https://login.mcorch.com/dashboard/constellation gostaria de deixar pelo menos 4 sub agentes por departamento, e hoje temos pelo menos uns 12 se não me engano. Para colocar todos para trabalhar, ou seja cada Lead das unidades departamentais deve ter pelo menos 4 subagentes trabalhando para eles e os lead (head) devem se reportar para o GCRUX Core.

## 🤖 Claude *(02:17:48)*


## 🤖 Claude *(02:17:57)*

Entendido — e essa correção é importante: **a queda de arestas (11925 → 9040) NÃO é anomalia, foi poda deliberada** para remover a "enterprise constellation" decorativa. Vou parar de tratar como bug de integridade e, conforme você pediu, **verificar materialmente** o estado real antes de propor qualquer coisa.

Deixa eu enquadrar o que entendi do pedido, e aí parto para a verificação:

**Visão (futuro):** a Constelação deixa de ser decorativa e vira o cockpit operacional — agentes que realmente acionam os módulos do ecossistema (Conteúdo, Canvas Design/Studio, Viral Miner, Blog, Calendário, Orquestração, Campanhas, Produtos, Afiliados, Analytics, Core, IA Arena; o GCRUX Core também usa o Dashboard agent-economics).

**Antes do hard reset (agora):** garantir a topologia limpa — **4 departamentos, cada Lead (head) com ≥4 subagentes reais trabalhando, e os Leads reportando ao GCRUX Core.** Hoje a página está poluída (~12 por depto), mata performance e tem bugs de z-index.

**ORO triplet desta task:**
- **Operator:** MCORCH Master Execution Agent (eu)
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign — blast radius = UX/perf de `/dashboard/constellation` em produção + topologia de agentes que vai virar a camada operacional real

Primeiro a materialidade. Vou mapear de onde vêm os agentes da crew (tabela vs nós `mcorch_nodes`), a estrutura atual e a contagem real:

## 🤖 Claude *(02:17:58)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCrewData.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useEffect, useRef, useMemo } from 'react';
> 2	import { useQuery } from '@tanstack/react-query';
> 3	import { supabase } from '@/integrations/supabase/client';
> 4	import { useAuth } from '@/hooks/useAuth';
> 5	import { useCrewStore, type Agent, type Edge } from '@/store/useCrewStore';
> 6	
> 7	export function useCrewData() {
> 8	  const { user } = useAuth();
> 9	  const setAgents = useCrewStore((s) => s.setAgents);
> 10	  const setEdges = useCrewStore((s) => s.setEdges);
> 11	  const setLoaded = useCrewStore((s) => s.setLoaded);
> 12	
> 13	  // Guards: only push to Zustand when content actually changes — prevents cascade on background refetches
> 14	  const agentsHashRef = useRef<string>('');
> 15	  const edgesHashRef = useRef<string>('');
> 16	
> 17	  const agentsQuery = useQuery({
> 18	    queryKey: ['crew_agents', user?.id],
> 19	    queryFn: async () => {
> 20	      if (!user?.id) throw new Error('User not authenticated');
> 21	
> 22	      let { data, error } = await supabase
> 23	        .from('crew_agents')
> 24	        .select('*')
> 25	        .order('created_at');
> 26	      if (error) throw error;
> 27	
> 28	      if (!data || (Array.isArray(data) && data.length === 0)) {
> 29	        const { error: seedErr } = await supabase.rpc('seed_crew_template', {
> 30	          _user_id: user.id,
> 31	        });
> 32	        if (seedErr) console.error('Seed error:', seedErr);
> 33	
> 34	        const res = await supabase
> 35	          .from('crew_agents')
> 36	          .select('*')
> 37	          .order('created_at');
> 38	        if (res.error) throw res.error;
> 39	        data = res.data;
> 40	      }
> 41	
> 42	      return (Array.isArray(data) ? data : [])
> 43	        .map((a: any): Agent | null => {
> 44	          if (!a?.agent_key) return null;
> 45	
> 46	          let pos: [number, number, number] = [0, 0, 0];
> 47	          try {
> 48	            const rawPos = typeof a.position === 'string' ? JSON.parse(a.position) : a.position;
> 49	            if (Array.isArray(rawPos) && rawPos.length === 3) {
> 50	              pos = rawPos as [number, number, number];
> 51	            } else if (rawPos && typeof rawPos === 'object') {
> 52	              pos = [rawPos.x || 0, rawPos.y || 0, rawPos.z || 0];
> 53	            }
> 54	          } catch (e) {
> 55	            console.error('Failed to parse position for agent:', a.agent_key, e);
> 56	          }
> 57	
> 58	          return {
> 59	            id: a.agent_key,
> 60	            dbId: a.id,
> 61	            name: a.name ?? 'Unknown Agent',
> 62	            role: a.role ?? 'specialist',
> 63	            avatar: a.avatar ?? '',
> 64	            provider: a.provider ?? 'openai',
> 65	            model: a.model ?? 'gpt-4o',
> 66	            status: (a.status ?? 'idle') as Agent['status'],
> 67	            position: pos,
> 68	            systemPrompt: a.system_prompt ?? '',
> 69	            priority: (a.priority ?? 1) as Agent['priority'],
> 70	            level: a.level ?? 1,
> 71	            squad: a.squad ?? 'unassigned',
> 72	          };
> 73	        })
> 74	        .filter(Boolean) as Agent[];
> 75	    },
> 76	    enabled: !!user,
> 77	    staleTime: 60_000, // 60s: avoids background refetch storms on window focus after reboot
> 78	  });
> 79	
> 80	  const edgesQuery = useQuery({
> 81	    queryKey: ['crew_edges', user?.id],
> 82	    queryFn: async () => {
> 83	      const { data, error } = await supabase
> 84	        .from('crew_edges')
> 85	        .select('*')
> 86	        .order('created_at');
> 87	      if (error) throw error;
> 88	
> 89	      return (Array.isArray(data) ? data : [])
> 90	        .map((e: any): Edge | null => {
> 91	          if (!e?.id || !e?.from_agent_key || !e?.to_agent_key) return null;
> 92	          return {
> 93	            id: e.id,
> 94	            from: e.from_agent_key,
> 95	            to: e.to_agent_key,
> 96	            status: (e.status ?? 'idle') as Edge['status'],
> 97	            label: e.label ?? '',
> 98	            createdAt: e.created_at ? new Date(e.created_at).getTime() : Date.now(),
> 99	          };
> 100	        })
> 101	        .filter(Boolean) as Edge[];
> 102	    },
> 103	    enabled: !!user,
> 104	    staleTime: 60_000,
> 105	  });
> 106	
> 107	  useEffect(() => {
> 108	    if (!agentsQuery.data) return;
> 109	    const hash = JSON.stringify(agentsQuery.data);
> 110	    if (hash === agentsHashRef.current) return; // same content — skip Zustand write
> 111	    agentsHashRef.current = hash;
> 112	    setAgents(agentsQuery.data);
> 113	  }, [agentsQuery.data, setAgents]);
> 114	
> 115	  useEffect(() => {
> 116	    if (edgesQuery.isSuccess) {
> 117	      const hash = JSON.stringify(edgesQuery.data);
> 118	      if (hash !== edgesHashRef.current) {
> 119	        edgesHashRef.current = hash;
> 120	        setEdges(edgesQuery.data);
> 121	      }
> 122	      setLoaded(true);
> 123	    } else if (edgesQuery.isError) {
> 124	      setLoaded(true);
> 125	    }
> 126	  }, [edgesQuery.isSuccess, edgesQuery.isError, edgesQuery.data, setEdges, setLoaded]);
> 127	
> 128	  return useMemo(
> 129	    () => ({
> 130	      isLoading: agentsQuery.isLoading || edgesQuery.isLoading,
> 131	      error: agentsQuery.error || edgesQuery.error,
> 132	    }),
> 133	    [agentsQuery.isLoading, agentsQuery.error, edgesQuery.isLoading, edgesQuery.error],
> 134	  );
> 135	}
> 136	
> ```

## 🤖 Claude *(02:17:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/store/useCrewStore.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { create } from 'zustand';
> 2	
> 3	export type AgentStatus = 'active' | 'thinking' | 'waiting' | 'error' | 'idle';
> 4	
> 5	export interface Agent {
> 6	  id: string;
> 7	  dbId?: string;
> 8	  name: string;
> 9	  role: string;
> 10	  avatar: string;
> 11	  provider: string;
> 12	  model: string;
> 13	  status: AgentStatus;
> 14	  position: [number, number, number];
> 15	  systemPrompt: string;
> 16	  priority: 'low' | 'medium' | 'high';
> 17	  squad?: string;
> 18	  level?: number;
> 19	}
> 20	
> 21	export interface Edge {
> 22	  id: string;
> 23	  dbId?: string;
> 24	  from: string;
> 25	  to: string;
> 26	  status: 'active' | 'waiting' | 'error' | 'idle';
> 27	  label?: string;
> 28	  createdAt: number;
> 29	}
> 30	
> 31	export interface LogEntry {
> 32	  id: string;
> 33	  timestamp: number;
> 34	  agentId: string;
> 35	  agentName: string;
> 36	  eventType: 'info' | 'error' | 'start' | 'toolCall' | 'complete';
> 37	  message: string;
> 38	}
> 39	
> 40	export interface Provider {
> 41	  id: string;
> 42	  name: string;
> 43	  endpoint: string;
> 44	  model: string;
> 45	  connected: boolean;
> 46	}
> 47	
> 48	interface CrewState {
> 49	  agents: Agent[];
> 50	  edges: Edge[];
> 51	  logs: LogEntry[];
> 52	  providers: Provider[];
> 53	  loaded: boolean;
> 54	  selectedAgentId: string | null;
> 55	  configOpen: boolean;
> 56	  logsOpen: boolean;
> 57	  connectingFrom: string | null;
> 58	  connectionMode: boolean;
> 59	  setAgents: (agents: Agent[]) => void;
> 60	  setEdges: (edges: Edge[]) => void;
> 61	  setLoaded: (loaded: boolean) => void;
> 62	  setSelectedAgent: (id: string | null) => void;
> 63	  setConfigOpen: (open: boolean) => void;
> 64	  setLogsOpen: (open: boolean) => void;
> 65	  setConnectingFrom: (id: string | null) => void;
> 66	  setConnectionMode: (mode: boolean) => void;
> 67	  addLog: (log: Omit<LogEntry, 'id' | 'timestamp'>) => void;
> 68	  setLogs: (logs: LogEntry[]) => void;
> 69	  updateAgentStatus: (id: string, status: AgentStatus) => void;
> 70	  updateEdgeStatus: (id: string, status: Edge['status']) => void;
> 71	  addEdge: (edge: Omit<Edge, 'id' | 'createdAt'>) => void;
> 72	  removeEdge: (id: string) => void;
> 73	  seedEnterpriseStructure: () => void;
> 74	}
> 75	
> 76	const INITIAL_PROVIDERS: Provider[] = [
> 77	  { id: 'openai', name: 'OpenAI', endpoint: 'https://api.openai.com/v1', model: 'gpt-4-turbo', connected: true },
> 78	  { id: 'anthropic', name: 'Anthropic', endpoint: 'https://api.anthropic.com/v1', model: 'claude-3-opus', connected: true },
> 79	  { id: 'google', name: 'Google Gemini', endpoint: 'https://generativelanguage.googleapis.com', model: 'gemini-pro', connected: false },
> 80	  { id: 'mistral', name: 'Mistral AI', endpoint: 'https://api.mistral.ai/v1', model: 'mistral-large', connected: false },
> 81	];
> 82	
> 83	let logCounter = 0;
> 84	
> 85	export const useCrewStore = create<CrewState>((set) => ({
> 86	  agents: [],
> 87	  edges: [],
> 88	  logs: [],
> 89	  providers: INITIAL_PROVIDERS,
> 90	  loaded: false,
> 91	  selectedAgentId: null,
> 92	  configOpen: false,
> 93	  logsOpen: false,
> 94	  connectingFrom: null,
> 95	  connectionMode: false,
> 96	  setAgents: (agents) => set({ agents: Array.isArray(agents) ? agents.filter(Boolean) : [] }),
> 97	  setEdges: (edges) => set({ edges: Array.isArray(edges) ? edges.filter(Boolean) : [] }),
> 98	  setLoaded: (loaded) => set({ loaded }),
> 99	  setSelectedAgent: (id) => set({ selectedAgentId: id }),
> 100	  setConfigOpen: (open) => set({ configOpen: open }),
> 101	  setLogsOpen: (open) => set({ logsOpen: open }),
> 102	  setConnectingFrom: (id) => set({ connectingFrom: id }),
> 103	  setConnectionMode: (mode) => set({ connectionMode: mode, connectingFrom: null }),
> 104	  addLog: (log) => set((s) => ({
> 105	    logs: [{ ...log, id: `log-${++logCounter}`, timestamp: Date.now() }, ...(s.logs || [])].slice(0, 200),
> 106	  })),
> 107	  setLogs: (logs) => set({ logs: Array.isArray(logs) ? logs.slice(0, 200) : [] }),
> 108	  updateAgentStatus: (id, status) => set((s) => ({
> 109	    agents: (s.agents || []).map((a) => (a && a.id === id ? { ...a, status } : a)),
> 110	  })),
> 111	  updateEdgeStatus: (id, status) => set((s) => ({
> 112	    edges: (s.edges || []).map((e) => (e && e.id === id ? { ...e, status } : e)),
> 113	  })),
> 114	  addEdge: (edge) => set((s) => ({
> 115	    edges: [...(s.edges || []), { ...edge, id: `e-${Date.now()}`, createdAt: Date.now() }],
> 116	  })),
> 117	  removeEdge: (id) => set((s) => ({
> 118	    edges: (s.edges || []).filter((e) => e && e.id !== id),
> 119	  })),
> 120	  seedEnterpriseStructure: () => {
> 121	    const agents: Agent[] = [];
> 122	    const edges: Edge[] = [];
> 123	    const now = Date.now();
> 124	
> 125	    // 1. CEO / Orchestrator (Tier 0)
> 126	    const ceoId = 'ceo-001';
> 127	    agents.push({
> 128	      id: ceoId,
> 129	      name: 'GCRUX Core',
> 130	      role: 'Sovereign Orchestrator',
> 131	      avatar: '👑',
> 132	      provider: 'OpenAI',
> 133	      model: 'GPT-4o',
> 134	      status: 'active',
> 135	      position: [0, 0, 0],
> 136	      systemPrompt: 'The brain of the operation.',
> 137	      priority: 'high',
> 138	      level: 0
> 139	    });
> 140	
> 141	    const squads = [
> 142	      { id: 'content', name: 'Creative Content', color: '#ec4899', icon: '🎨' },
> 143	      { id: 'tech', name: 'Technical Engine', color: '#3b82f6', icon: '⚙️' },
> 144	      { id: 'market', name: 'Market Intelligence', color: '#22c55e', icon: '📈' },
> 145	      { id: 'ops', name: 'Operational Ops', color: '#f59e0b', icon: '⚡' },
> 146	    ];
> 147	
> 148	    squads.forEach((squad, sIdx) => {
> 149	      const squadAngle = (sIdx / squads.length) * Math.PI * 2;
> 150	      const squadRadius = 8;
> 151	      const squadX = Math.cos(squadAngle) * squadRadius;
> 152	      const squadZ = Math.sin(squadAngle) * squadRadius;
> 153	
> 154	      // 2. Squad Leaders (Tier 1)
> 155	      const leaderId = `leader-${squad.id}`;
> 156	      agents.push({
> 157	        id: leaderId,
> 158	        name: `${squad.name} Lead`,
> 159	        role: 'Director',
> 160	        avatar: squad.icon,
> 161	        provider: 'Anthropic',
> 162	        model: 'Claude 3.5 Sonnet',
> 163	        status: 'idle',
> 164	        position: [squadX, 2, squadZ],
> 165	        systemPrompt: `Leading the ${squad.name} division.`,
> 166	        priority: 'high',
> 167	        squad: squad.id,
> 168	        level: 1
> 169	      });
> 170	
> 171	      edges.push({
> 172	        id: `edge-ceo-${leaderId}`,
> 173	        from: ceoId,
> 174	        to: leaderId,
> 175	        status: 'active',
> 176	        label: 'Directive',
> 177	        createdAt: now
> 178	      });
> 179	
> 180	      // 3. Squad Members (Tier 2) - "Gigantic Squads"
> 181	      const memberCount = 6;
> 182	      for (let i = 0; i < memberCount; i++) {
> 183	        const memberAngle = (i / memberCount) * Math.PI * 2;
> 184	        const memberRadius = 3;
> 185	        const mx = squadX + Math.cos(memberAngle) * memberRadius;
> 186	        const mz = squadZ + Math.sin(memberAngle) * memberRadius;
> 187	        const my = (Math.random() - 0.5) * 4;
> 188	
> 189	        const memberId = `agent-${squad.id}-${i}`;
> 190	        agents.push({
> 191	          id: memberId,
> 192	          name: `${squad.id.toUpperCase()}-${i + 1}`,
> 193	          role: 'specialist',
> 194	          avatar: '🤖',
> 195	          provider: 'Groq',
> 196	          model: 'Llama 3',
> 197	          status: 'idle',
> 198	          position: [mx, my, mz],
> 199	          systemPrompt: 'Executing specialized tasks.',
> 200	          priority: 'medium',
> 201	          squad: squad.id,
> 202	          level: 2
> 203	        });
> 204	
> 205	        edges.push({
> 206	          id: `edge-${leaderId}-${memberId}`,
> 207	          from: leaderId,
> 208	          to: memberId,
> 209	          status: 'idle',
> 210	          label: 'Reporting',
> 211	          createdAt: now
> 212	        });
> 213	      }
> 214	    });
> 215	
> 216	    set({ agents, edges, loaded: true });
> 217	  }
> 218	}));
> 219	
> ```

## 🤖 Claude *(02:18:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"\u2500\u2500\u2500 grep crew_agent in migrations \u2500\u2500\u2500\"; grep -rl \"crew_agent\\|crew_agents\\|crew_squad\\|crew_edges\" supabase/migrations/ 2>/dev/null | head; echo \"\u2500\u2500\u2500 .env present? \u2500\u2500\u2500\"; ls -la .env 2>/dev/null | awk '{print $5, $9}'; echo \"\u2500\u2500\u2500 SUPABASE url/keys in .env (names only) \u2500\u2500\u2500\"; grep -oE \"^[A-Z_]*SUPABASE[A-Z_]*\" .env 2>/dev/null; echo \"\u2500\u2500\u2500 crew-related src files \u2500\u2500\u2500\"; grep -rl \"useCrewStore\\|SQUAD_META\\|crew_agent\" src/ 2>/dev/null | head -20",
  "description": "Locate crew data source: migrations, env keys, src files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── grep crew_agent in migrations ───
> supabase/migrations/20260426160000_crew_module_ownership.sql
> supabase/migrations/20260425000000_enterprise_hierarchy.sql
> supabase/migrations/20260527012945_agent_metering_minimal.sql
> supabase/migrations/20260412142520_7ee90a5b-8e1a-4cdf-8136-f7ab32225a14.sql
> ─── .env present? ───
> 1144 .env
> ─── SUPABASE url/keys in .env (names only) ───
> SUPABASE_URL
> VITE_SUPABASE_URL
> VITE_SUPABASE_PROJECT_ID
> SUPABASE_PUBLISHABLE_KEY
> VITE_SUPABASE_PUBLISHABLE_KEY
> SUPABASE_SERVICE_ROLE_KEY
> ─── crew-related src files ───
> src/integrations/supabase/types.ts
> src/pages/MemoryPage.tsx
> src/pages/ConstellationPage.tsx
> src/lib/enterprise-seed.ts
> src/components/orchestrator/ConstellationMatrix.tsx
> src/components/HUD.tsx
> src/components/orchestrator/NodeDetailsPanel.tsx
> src/components/dashboard/ConstellationWidget.tsx
> src/components/graph/SquadHull.tsx
> src/components/graph/CrewGraph.tsx
> src/components/graph/AgentEdge.tsx
> src/components/graph/AgentNode.tsx
> src/components/panels/ConfigPanel.tsx
> src/components/panels/AgentDetail.tsx
> src/components/panels/LogsPanel.tsx
> src/components/panels/NewEdgeDialog.tsx
> src/hooks/useCrewOverlay.ts
> src/hooks/useCrewData.ts
> src/hooks/useAgentEconomics.ts
> src/hooks/useAgentTask.ts
> ```

## 🤖 Claude *(02:18:50)*


## 🤖 Claude *(02:18:54)*

Agora o modelo de dados está claro: o 3D lê de **`crew_agents` / `crew_edges`** (tabelas dedicadas, não o `mcorch_nodes`). Isso é importante — a poda que você fez foi no **knowledge mesh** (`mcorch_edges`), mas a constelação 3D vem de outra fonte. Por isso a imagem ainda mostra tudo poluído. Vou confirmar isso materialmente consultando o banco vivo + ler a lógica de seed/render.

Há também um `seedEnterpriseStructure()` no store (6 membros/squad = 29 nós) **e** uma RPC `seed_crew_template` no banco — preciso ver qual está populando os ~12/depto que você vê.

## 🤖 Claude *(02:19:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nBASE=\"${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}/rest/v1\"\nHK=(-H \"apikey: $SUPABASE_SERVICE_ROLE_KEY\" -H \"Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY\")\n\necho \"\u2550\u2550\u2550 crew_agents (live, all users via service role) \u2550\u2550\u2550\"\ncurl -s \"$BASE/crew_agents?select=agent_key,name,squad,level,status,user_id,provider,model\" \"${HK[@]}\" > /tmp/ca.json\necho \"TOTAL crew_agents: $(jq 'length' /tmp/ca.json)\"\necho \"\u2500\u2500 by user_id \u2500\u2500\"; jq -r 'group_by(.user_id)[] | \"\\(.[0].user_id // \"NULL\"): \\(length)\"' /tmp/ca.json\necho \"\u2500\u2500 by squad \u2500\u2500\"; jq -r 'group_by(.squad)[] | \"\\(.[0].squad // \"none\"): \\(length)\"' /tmp/ca.json\necho \"\u2500\u2500 by level \u2500\u2500\"; jq -r 'group_by(.level)[] | \"L\\(.[0].level): \\(length)\"' /tmp/ca.json\necho \"\u2500\u2500 by status \u2500\u2500\"; jq -r 'group_by(.status)[] | \"\\(.[0].status): \\(length)\"' /tmp/ca.json\necho \"\u2500\u2500 leaders (level<=1) \u2500\u2500\"; jq -r '.[] | select(.level<=1) | \"  [\\(.squad // \"core\")] \\(.name) \u2014 \\(.agent_key) (L\\(.level), \\(.status), \\(.provider)/\\(.model))\"' /tmp/ca.json\n\necho \"\"\necho \"\u2550\u2550\u2550 crew_edges (live) \u2550\u2550\u2550\"\ncurl -s \"$BASE/crew_edges?select=from_agent_key,to_agent_key,label,status\" \"${HK[@]}\" > /tmp/ce.json\necho \"TOTAL crew_edges: $(jq 'length' /tmp/ce.json)\"\necho \"\u2500\u2500 by label \u2500\u2500\"; jq -r 'group_by(.label)[] | \"\\(.[0].label // \"none\"): \\(length)\"' /tmp/ce.json\n\necho \"\"\necho \"\u2550\u2550\u2550 mcorch_nodes node_type=crew_agent (mesh mirror) \u2550\u2550\u2550\"\ncurl -s -I \"$BASE/mcorch_nodes?node_type=eq.crew_agent&select=id\" \"${HK[@]}\" -H \"Prefer: count=exact\" 2>/dev/null | grep -i \"content-range\" || echo \"(no count header)\"\n\necho \"\"\necho \"\u2550\u2550\u2550 seed_crew_template / enterprise seed definitions \u2550\u2550\u2550\"\ngrep -rln \"seed_crew_template\\|memberCount\\|specialistCount\\|seed_crew\" supabase/migrations/ src/ 2>/dev/null",
  "description": "Query live crew_agents/crew_edges structure + mesh mirror + locate seed logic"
}
```

## 🤖 Claude *(02:19:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/enterprise-seed.ts"
}
```

## 🤖 Claude *(02:19:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/ConstellationPage.tsx"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ═══ crew_agents (live, all users via service role) ═══
> TOTAL crew_agents: 717
> ── by user_id ──
> 0b4d79d2-b77c-457e-8b23-d033a886c805: 29
> 1eb93f64-9449-42a9-8af8-bdf3eaf24379: 6
> 21ae007b-a81d-4ffa-ac80-c45da0b35142: 29
> 23822eec-ba17-44d4-9d99-c2fba895f25a: 29
> 3b88b71c-e0c8-46ba-b5ed-1d49d018e111: 29
> 3cdf08fe-ae4e-468e-a926-d85327304d11: 6
> 46292a6b-c669-44eb-b456-989a8965500f: 29
> 467d5015-7111-4d18-87e9-e8dfb04b28e3: 29
> 4744d13d-a456-476d-8b63-d2f0b8eef6fa: 29
> 5466d55e-4982-4d7a-802b-f83606900b7a: 29
> 5bde3a96-2061-4077-8c6f-14d2244bb39c: 6
> 6452253e-cb70-4fc6-bd43-595d0dfcad0e: 29
> 77d67d35-7095-40de-b5db-47ca29f9cc86: 29
> 7c03a2ee-5c8e-4303-b422-99f047f3b69b: 29
> 84302f6e-e32b-450e-9c96-0d91a7ccecf1: 29
> 892382ee-bdd5-4e9a-a544-75bb2a7e561a: 29
> 8ca62eb3-f75c-42d1-8a20-bf13a16e3a3f: 29
> 924cb32e-d8d7-404a-bc88-6ac76e6b1b0f: 8
> a715f5fe-561f-44c4-ba5c-2267a3d872bb: 29
> a74d327a-e814-4648-9ff9-d719aaf79d32: 29
> ada39fae-67e1-4e53-af1c-5a18e1c108e8: 53
> b756dcb4-74fb-40d5-9710-e602bb632626: 29
> b83dcde2-4d27-424a-9ed3-9ef36c64a983: 29
> be8e057b-8893-45df-bc59-9433e3fc6303: 29
> cfea4634-9498-4577-8c3b-93ec2fdeefe3: 29
> ed85f423-2e60-47c3-8013-ebad3ace4ddd: 29
> fd58daa9-03c1-46f3-a756-17eb365d6a9b: 29
> ── by squad ──
> none: 47
> content: 167
> market: 169
> ops: 167
> tech: 167
> ── by level ──
> L0: 23
> L1: 92
> L2: 602
> ── by status ──
> active: 31
> idle: 672
> monitoring_trends: 1
> optimizing_cpm: 1
> thinking: 8
> waiting: 4
> ── leaders (level<=1) ──
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — 9f4e1f8c-e77c-4657-8ae0-0afe4b048211 (L0, active, OpenAI/GPT-4o)
>   [content] Creative Content Lead — ae07be2c-4702-47d4-8250-14c9868c6fd2 (L1, idle, Anthropic/Claude 3.5 Sonnet)
>   [tech] Technical Engine Lead — fa95d591-4dd8-49dd-a0fe-a818de6286ff (L1, idle, Anthropic/Claude 3.5 Sonnet)
>   [market] Market Intelligence Lead — b3f69bb4-b311-475a-9f3c-2bfdf41dc85f (L1, idle, Anthropic/Claude 3.5 Sonnet)
>   [ops] Operational Ops Lead — 94a42f78-8973-476a-9fa6-1e5241d3f687 (L1, idle, Anthropic/Claude 3.5 Sonnet)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [core] GCRUX Core — ceo-001 (L0, active, openai/gpt-4o)
>   [content] Creative Content Lead — leader-content (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [tech] Technical Engine Lead — leader-tech (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [market] Market Intelligence Lead — leader-market (L1, idle, anthropic/claude-3-5-sonnet-20240620)
>   [ops] Operational Ops Lead — leader-ops (L1, idle, anthropic/claude-3-5-sonnet-20240620)
> 
> ═══ crew_edges (live) ═══
> TOTAL crew_edges: 689
> ── by label ──
> Bug report: 4
> Content draft: 4
> Data request: 4
> Directive: 92
> Feature spec: 4
> Reporting: 576
> Strategy brief: 4
> mkt-1 - tech-1: 1
> 
> ═══ mcorch_nodes node_type=crew_agent (mesh mirror) ═══
> content-range: 0-78/79
> 
> ═══ seed_crew_template / enterprise seed definitions ═══
> supabase/migrations/20260425000000_enterprise_hierarchy.sql
> supabase/migrations/20260412142520_7ee90a5b-8e1a-4cdf-8136-f7ab32225a14.sql
> src/integrations/supabase/types.ts
> src/lib/enterprise-seed.ts
> src/components/landing/LandingConstellation.tsx
> src/hooks/useCrewData.ts
> src/store/useCrewStore.ts
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { CrewGraph } from '@/components/graph/CrewGraph';
> 2	import { HUD } from '@/components/HUD';
> 3	import { ConfigPanel } from '@/components/panels/ConfigPanel';
> 4	import { LogsPanel } from '@/components/panels/LogsPanel';
> 5	import { AgentDetail } from '@/components/panels/AgentDetail';
> 6	import { Legend } from '@/components/Legend';
> 7	import { useAgentActivity } from '@/hooks/useAgentActivity';
> 8	import { useCrewData } from '@/hooks/useCrewData';
> 9	import { useHandTracking } from '@/hooks/useHandTracking';
> 10	import { useAuth } from '@/hooks/useAuth';
> 11	import { GestureParticleOverlay } from '@/components/gestures/GestureParticles';
> 12	import { GestureHUD } from '@/components/gestures/GestureHUD';
> 13	import { GestureController } from '@/components/gestures/GestureController';
> 14	import { AddAgentDialog } from '@/components/panels/AddAgentDialog';
> 15	import { NewEdgeDialog } from '@/components/panels/NewEdgeDialog';
> 16	import { Button } from '@/components/ui/button';
> 17	import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
> 18	import { Minimize2, Loader2, Plus, Link2, Link2Off, Brain, Network } from 'lucide-react';
> 19	import { useNavigate } from 'react-router-dom';
> 20	import { useState } from 'react';
> 21	import { useCrewStore } from '@/store/useCrewStore';
> 22	import { deployEnterpriseToSupabase } from '@/lib/enterprise-seed';
> 23	
> 24	export default function ConstellationPage() {
> 25	  const { user } = useAuth();
> 26	  const { isLoading: crewLoading } = useCrewData();
> 27	  const loaded = useCrewStore((s) => s.loaded);
> 28	  const connectionMode = useCrewStore((s) => s.connectionMode);
> 29	  const setConnectionMode = useCrewStore((s) => s.setConnectionMode);
> 30	  useAgentActivity(); // real agent_executions feed (replaces the useSimulation mock)
> 31	  const navigate = useNavigate();
> 32	  const [gesturesEnabled, setGesturesEnabled] = useState(false);
> 33	  const [addOpen, setAddOpen] = useState(false);
> 34	  const [isDeploying, setIsDeploying] = useState(false);
> 35	  const { handData, isLoading, error } = useHandTracking(gesturesEnabled);
> 36	
> 37	  if (crewLoading || !loaded) {
> 38	    return (
> 39	      <div className="relative w-full h-full flex items-center justify-center bg-background rounded-lg">
> 40	        <Loader2 className="h-8 w-8 animate-spin text-primary" />
> 41	      </div>
> 42	    );
> 43	  }
> 44	
> 45	  return (
> 46	    <TooltipProvider>
> 47	      <div className="relative w-full h-full overflow-hidden bg-background rounded-lg">
> 48	        <div className="crt-overlay" />
> 49	        <div className="scanline" />
> 50	        <CrewGraph />
> 51	        {gesturesEnabled && <GestureParticleOverlay handData={handData} />}
> 52	        <GestureController handData={handData} enabled={gesturesEnabled} />
> 53	        <HUD>
> 54	          <Tooltip>
> 55	            <TooltipTrigger asChild>
> 56	              <Button
> 57	                variant={connectionMode ? 'default' : 'outline'}
> 58	                size="sm"
> 59	                className="glass-panel border-border/50 gap-1.5 h-8 sm:h-9"
> 60	                onClick={() => setConnectionMode(!connectionMode)}
> 61	              >
> 62	                {connectionMode ? <Link2Off className="h-3.5 w-3.5" /> : <Link2 className="h-3.5 w-3.5" />}
> 63	                {connectionMode ? 'Sair' : 'Conectar'}
> 64	              </Button>
> 65	            </TooltipTrigger>
> 66	            <TooltipContent>
> 67	              {connectionMode ? 'Clique em dois agentes para conectá-los' : 'Ativar modo conexão'}
> 68	            </TooltipContent>
> 69	          </Tooltip>
> 70	
> 71	          <Button
> 72	            variant="outline"
> 73	            size="sm"
> 74	            disabled={isDeploying}
> 75	            className="glass-panel border-border/50 gap-1.5 h-8 sm:h-9 bg-primary/10 text-primary hover:bg-primary/20"
> 76	            onClick={async () => {
> 77	              if (!user?.id) return;
> 78	              setIsDeploying(true);
> 79	              const res = await deployEnterpriseToSupabase(user.id);
> 80	              if (res.success) {
> 81	                window.location.reload();
> 82	              }
> 83	              setIsDeploying(false);
> 84	            }}
> 85	          >
> 86	            {isDeploying ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Loader2 className="h-3.5 w-3.5" />}
> 87	            {isDeploying ? 'Deploying...' : 'Deploy Enterprise'}
> 88	          </Button>
> 89	
> 90	          <Button
> 91	            variant="outline"
> 92	            size="sm"
> 93	            className="glass-panel border-border/50 gap-1.5 h-8 sm:h-9"
> 94	            onClick={() => setAddOpen(true)}
> 95	          >
> 96	            <Plus className="h-3.5 w-3.5" />
> 97	            Agente
> 98	          </Button>
> 99	
> 100	          {/* Matrix — full-screen AST Constellation page */}
> 101	          <Button
> 102	            variant="outline"
> 103	            size="sm"
> 104	            className="glass-panel border-border/50 gap-1.5 h-8 sm:h-9"
> 105	            onClick={() => navigate('/dashboard/constellation/matrix')}
> 106	          >
> 107	            <Network className="h-3.5 w-3.5" />
> 108	            Matrix
> 109	          </Button>
> 110	
> 111	          {/* Memory Mesh — full-screen isolated page */}
> 112	          <Button
> 113	            variant="outline"
> 114	            size="sm"
> 115	            className="glass-panel border-border/50 gap-1.5 h-8 sm:h-9"
> 116	            onClick={() => navigate('/dashboard/constellation/memory')}
> 117	          >
> 118	            <Brain className="h-3.5 w-3.5" />
> 119	            Memória
> 120	          </Button>
> 121	
> 122	          <Button
> 123	            variant="outline"
> 124	            size="sm"
> 125	            className="glass-panel border-border/50 gap-1.5 h-8 sm:h-9"
> 126	            onClick={() => navigate('/dashboard')}
> 127	          >
> 128	            <Minimize2 className="h-3.5 w-3.5" />
> 129	            Minimizar
> 130	          </Button>
> 131	        </HUD>
> 132	        <AgentDetail />
> 133	        <ConfigPanel />
> 134	        <LogsPanel />
> 135	        <Legend />
> 136	        <GestureHUD
> 137	          handData={handData}
> 138	          isLoading={isLoading}
> 139	          error={error}
> 140	          enabled={gesturesEnabled}
> 141	          onToggle={() => setGesturesEnabled(!gesturesEnabled)}
> 142	        />
> 143	
> 144	        {connectionMode && (
> 145	          <div className="absolute bottom-20 left-1/2 -translate-x-1/2 z-50 glass-panel rounded-full px-4 py-2 text-sm text-primary animate-pulse shadow-lg shadow-primary/20 flex items-center gap-2">
> 146	            <Link2 className="h-4 w-4" />
> 147	            <span>Clique em um agente de origem, depois no destino</span>
> 148	          </div>
> 149	        )}
> 150	
> 151	        <AddAgentDialog open={addOpen} onOpenChange={setAddOpen} />
> 152	        <NewEdgeDialog />
> 153	      </div>
> 154	    </TooltipProvider>
> 155	  );
> 156	}
> 157	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { supabase } from '@/integrations/supabase/client';
> 2	import { Agent, Edge } from '@/store/useCrewStore';
> 3	
> 4	export async function deployEnterpriseToSupabase(userId: string) {
> 5	  const agents: any[] = [];
> 6	  const edges: any[] = [];
> 7	  
> 8	  // Tier 0
> 9	  const ceoKey = crypto.randomUUID();
> 10	  agents.push({
> 11	    agent_key: ceoKey,
> 12	    name: 'GCRUX Core',
> 13	    role: 'Sovereign Orchestrator',
> 14	    avatar: '👑',
> 15	    provider: 'OpenAI',
> 16	    model: 'GPT-4o',
> 17	    status: 'active',
> 18	    position: [0, 0, 0],
> 19	    system_prompt: 'The brain of the operation.',
> 20	    priority: 'high',
> 21	    level: 0,
> 22	    user_id: userId
> 23	  });
> 24	
> 25	  const squads = [
> 26	    { id: 'content', name: 'Creative Content', color: '#ec4899', icon: '🎨' },
> 27	    { id: 'tech', name: 'Technical Engine', color: '#3b82f6', icon: '⚙️' },
> 28	    { id: 'market', name: 'Market Intelligence', color: '#22c55e', icon: '📈' },
> 29	    { id: 'ops', name: 'Operational Ops', color: '#f59e0b', icon: '⚡' },
> 30	  ];
> 31	
> 32	  squads.forEach((squad, sIdx) => {
> 33	    const squadAngle = (sIdx / squads.length) * Math.PI * 2;
> 34	    const squadRadius = 8;
> 35	    const squadX = Math.cos(squadAngle) * squadRadius;
> 36	    const squadZ = Math.sin(squadAngle) * squadRadius;
> 37	
> 38	    // Tier 1
> 39	    const leaderKey = crypto.randomUUID();
> 40	    agents.push({
> 41	      agent_key: leaderKey,
> 42	      name: `${squad.name} Lead`,
> 43	      role: 'Director',
> 44	      avatar: squad.icon,
> 45	      provider: 'Anthropic',
> 46	      model: 'Claude 3.5 Sonnet',
> 47	      status: 'idle',
> 48	      position: [squadX, 2, squadZ],
> 49	      system_prompt: `Leading the ${squad.name} division.`,
> 50	      priority: 'high',
> 51	      squad: squad.id,
> 52	      level: 1,
> 53	      user_id: userId
> 54	    });
> 55	
> 56	    edges.push({
> 57	      from_agent_key: ceoKey,
> 58	      to_agent_key: leaderKey,
> 59	      status: 'active',
> 60	      label: 'Directive',
> 61	      user_id: userId
> 62	    });
> 63	
> 64	    // Tier 2 - Gigantic Squads
> 65	    const memberCount = 12;
> 66	    for (let i = 0; i < memberCount; i++) {
> 67	      const memberAngle = (i / memberCount) * Math.PI * 2;
> 68	      const memberRadius = 3;
> 69	      const mx = squadX + Math.cos(memberAngle) * memberRadius;
> 70	      const mz = squadZ + Math.sin(memberAngle) * memberRadius;
> 71	      const my = (Math.random() - 0.5) * 4;
> 72	
> 73	      const memberKey = crypto.randomUUID();
> 74	      agents.push({
> 75	        agent_key: memberKey,
> 76	        name: `${squad.id.toUpperCase()}-${i + 1}`,
> 77	        role: 'specialist',
> 78	        avatar: '🤖',
> 79	        provider: 'Groq',
> 80	        model: 'Llama 3',
> 81	        status: 'idle',
> 82	        position: [mx, my, mz],
> 83	        system_prompt: 'Executing specialized tasks.',
> 84	        priority: 'medium',
> 85	        squad: squad.id,
> 86	        level: 2,
> 87	        user_id: userId
> 88	      });
> 89	
> 90	      edges.push({
> 91	        from_agent_key: leaderKey,
> 92	        to_agent_key: memberKey,
> 93	        status: 'idle',
> 94	        label: 'Reporting',
> 95	        user_id: userId
> 96	      });
> 97	    }
> 98	  });
> 99	
> 100	  // Execute
> 101	  try {
> 102	    // 1. Clear existing for this user
> 103	    await supabase.from('crew_edges').delete().eq('user_id', userId);
> 104	    await supabase.from('crew_agents').delete().eq('user_id', userId);
> 105	
> 106	    // 2. Insert Agents
> 107	    const { error: aError } = await supabase.from('crew_agents').insert(agents);
> 108	    if (aError) throw aError;
> 109	
> 110	    // 3. Insert Edges
> 111	    const { error: eError } = await supabase.from('crew_edges').insert(edges);
> 112	    if (eError) throw eError;
> 113	
> 114	    return { success: true };
> 115	  } catch (err: any) {
> 116	    console.error('Failed to seed enterprise structure:', err);
> 117	    return { success: false, error: err?.message || 'Unknown error' };
> 118	  }
> 119	}
> 120	
> ```

## 🤖 Claude *(02:20:13)*


## 🤖 Claude *(02:20:14)*

Os números materiais mudam o diagnóstico — e revelam algo importante. Deixa eu confirmar a fonte do seed e o que já existe de "trabalho real" antes de fechar o parecer.

## 🤖 Claude *(02:20:15)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Constellation crew rewire",
  "summary": "Verify crew_agents/crew_edges state, plan 4-subagent-per-dept topology reporting to GCRUX Core"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Constellation crew rewire". Continue your current work.'}]
> ```

## 🤖 Claude *(02:20:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260425000000_enterprise_hierarchy.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Add columns for hierarchy and squads
> 2	ALTER TABLE public.crew_agents ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 2;
> 3	ALTER TABLE public.crew_agents ADD COLUMN IF NOT EXISTS squad TEXT;
> 4	
> 5	-- Update seed function to create a gigantic enterprise structure
> 6	CREATE OR REPLACE FUNCTION public.seed_crew_template(_user_id UUID)
> 7	RETURNS void
> 8	LANGUAGE plpgsql
> 9	SECURITY DEFINER
> 10	SET search_path = public
> 11	AS $$
> 12	DECLARE
> 13	    ceo_id_key TEXT := 'ceo-001';
> 14	    i INTEGER;
> 15	    j INTEGER;
> 16	    member_id_key TEXT;
> 17	    leader_id_key TEXT;
> 18	    squad_id TEXT;
> 19	    squad_name TEXT;
> 20	    squad_icon TEXT;
> 21	    squad_color TEXT;
> 22	    squad_angle FLOAT;
> 23	    squad_radius FLOAT := 8.0;
> 24	    squad_x FLOAT;
> 25	    squad_z FLOAT;
> 26	    member_angle FLOAT;
> 27	    member_radius FLOAT := 3.0;
> 28	    mx FLOAT;
> 29	    mz FLOAT;
> 30	    my FLOAT;
> 31	BEGIN
> 32	    -- Only seed if user has no agents yet
> 33	    IF EXISTS (SELECT 1 FROM public.crew_agents WHERE user_id = _user_id LIMIT 1) THEN
> 34	        RETURN;
> 35	    END IF;
> 36	
> 37	    -- 1. CEO / Core
> 38	    INSERT INTO public.crew_agents (user_id, agent_key, name, role, avatar, provider, model, status, position, system_prompt, priority, level)
> 39	    VALUES (_user_id, ceo_id_key, 'GCRUX Core', 'Sovereign Orchestrator', '👑', 'openai', 'gpt-4o', 'active', '[0,0,0]', 'The brain of the operation.', 'high', 0);
> 40	
> 41	    -- 2. Define Squads
> 42	    -- We'll loop through 4 squads
> 43	    FOR i IN 0..3 LOOP
> 44	        squad_angle := (i::FLOAT / 4.0) * 2.0 * PI();
> 45	        squad_x := COS(squad_angle) * squad_radius;
> 46	        squad_z := SIN(squad_angle) * squad_radius;
> 47	        
> 48	        IF i = 0 THEN
> 49	            squad_id := 'content'; squad_name := 'Creative Content'; squad_icon := '🎨'; squad_color := '#ec4899';
> 50	        ELSIF i = 1 THEN
> 51	            squad_id := 'tech'; squad_name := 'Technical Engine'; squad_icon := '⚙️'; squad_color := '#3b82f6';
> 52	        ELSIF i = 2 THEN
> 53	            squad_id := 'market'; squad_name := 'Market Intelligence'; squad_icon := '📈'; squad_color := '#22c55e';
> 54	        ELSE
> 55	            squad_id := 'ops'; squad_name := 'Operational Ops'; squad_icon := '⚡'; squad_color := '#f59e0b';
> 56	        END IF;
> 57	
> 58	        leader_id_key := 'leader-' || squad_id;
> 59	        
> 60	        -- Insert Leader
> 61	        INSERT INTO public.crew_agents (user_id, agent_key, name, role, avatar, provider, model, status, position, system_prompt, priority, level, squad)
> 62	        VALUES (_user_id, leader_id_key, squad_name || ' Lead', 'Director', squad_icon, 'anthropic', 'claude-3-5-sonnet-20240620', 'idle', 
> 63	                format('[%s, 2, %s]', squad_x, squad_z)::jsonb, 
> 64	                'Leading the ' || squad_name || ' division.', 'high', 1, squad_id);
> 65	
> 66	        -- Link Leader to CEO
> 67	        INSERT INTO public.crew_edges (user_id, from_agent_key, to_agent_key, status, label)
> 68	        VALUES (_user_id, ceo_id_key, leader_id_key, 'active', 'Directive');
> 69	
> 70	        -- 3. Members
> 71	        FOR j IN 1..6 LOOP
> 72	            member_angle := (j::FLOAT / 6.0) * 2.0 * PI();
> 73	            mx := squad_x + COS(member_angle) * member_radius;
> 74	            mz := squad_z + SIN(member_angle) * member_radius;
> 75	            my := (random() - 0.5) * 4.0;
> 76	            member_id_key := 'agent-' || squad_id || '-' || j;
> 77	
> 78	            INSERT INTO public.crew_agents (user_id, agent_key, name, role, avatar, provider, model, status, position, system_prompt, priority, level, squad)
> 79	            VALUES (_user_id, member_id_key, upper(squad_id) || '-' || j, 'specialist', '🤖', 'groq', 'llama3-70b-8192', 'idle', 
> 80	                    format('[%s, %s, %s]', mx, my, mz)::jsonb, 
> 81	                    'Executing specialized tasks.', 'medium', 2, squad_id);
> 82	
> 83	            -- Link Member to Leader
> 84	            INSERT INTO public.crew_edges (user_id, from_agent_key, to_agent_key, status, label)
> 85	            VALUES (_user_id, leader_id_key, member_id_key, 'idle', 'Reporting');
> 86	        END LOOP;
> 87	    END LOOP;
> 88	END;
> 89	$$;
> 90	
> ```

## 🤖 Claude *(02:20:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useAgentActivity.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useEffect } from 'react';
> 2	import { useQuery, useQueryClient } from '@tanstack/react-query';
> 3	import { supabase } from '@/integrations/supabase/client';
> 4	import { useAuth } from '@/hooks/useAuth';
> 5	import { useCrewStore, type AgentStatus, type LogEntry } from '@/store/useCrewStore';
> 6	
> 7	/**
> 8	 * Real Constellation activity feed — replaces the `useSimulation` mock.
> 9	 *
> 10	 * Reads actual `agent_executions` rows (written by the agent-daily-pulse cron and by
> 11	 * manual "Executar tarefa" triggers via agent-task-execute) and projects them onto:
> 12	 *   - the Live Logs panel (`store.logs`)
> 13	 *   - per-agent 3D status (`updateAgentStatus`)
> 14	 *
> 15	 * Mapping: agent_executions.agent_id === crew_agents.id === store Agent.dbId.
> 16	 *
> 17	 * React 18 / Zustand safety: the effect depends ONLY on the query payload and reads the
> 18	 * live agents array via getState() inside the callback — never subscribes to `agents` in
> 19	 * deps (would recreate the effect on every updateAgentStatus → Error #185 cascade).
> 20	 */
> 21	
> 22	type ExecRow = {
> 23	  id: string;
> 24	  agent_id: string;
> 25	  status: 'pending' | 'running' | 'done' | 'failed';
> 26	  provider: string;
> 27	  model: string;
> 28	  tokens_in: number | null;
> 29	  tokens_out: number | null;
> 30	  cost_mcoin: number | null;
> 31	  latency_ms: number | null;
> 32	  error_msg: string | null;
> 33	  started_at: string;
> 34	  completed_at: string | null;
> 35	};
> 36	
> 37	const STATUS_MAP: Record<ExecRow['status'], AgentStatus> = {
> 38	  pending: 'waiting',
> 39	  running: 'thinking',
> 40	  done: 'idle',
> 41	  failed: 'error',
> 42	};
> 43	
> 44	const EVENT_MAP: Record<ExecRow['status'], LogEntry['eventType']> = {
> 45	  pending: 'info',
> 46	  running: 'start',
> 47	  done: 'complete',
> 48	  failed: 'error',
> 49	};
> 50	
> 51	function buildMessage(e: ExecRow): string {
> 52	  switch (e.status) {
> 53	    case 'done': {
> 54	      const total = (e.tokens_in ?? 0) + (e.tokens_out ?? 0);
> 55	      return `${e.provider}/${e.model} · ${total} tokens · ${e.cost_mcoin ?? 0} mco · ${e.latency_ms ?? 0}ms`;
> 56	    }
> 57	    case 'running':
> 58	      return `executando tarefa via ${e.provider}/${e.model}…`;
> 59	    case 'failed':
> 60	      return `falhou: ${(e.error_msg ?? 'erro desconhecido').slice(0, 100)}`;
> 61	    default:
> 62	      return 'na fila…';
> 63	  }
> 64	}
> 65	
> 66	export function useAgentActivity() {
> 67	  const { user } = useAuth();
> 68	  const queryClient = useQueryClient();
> 69	  const setLogs = useCrewStore((s) => s.setLogs);
> 70	
> 71	  const execQuery = useQuery({
> 72	    queryKey: ['agent_executions', user?.id],
> 73	    queryFn: async (): Promise<ExecRow[]> => {
> 74	      const { data, error } = await supabase
> 75	        .from('agent_executions')
> 76	        .select(
> 77	          'id, agent_id, status, provider, model, tokens_in, tokens_out, cost_mcoin, latency_ms, error_msg, started_at, completed_at',
> 78	        )
> 79	        .order('started_at', { ascending: false })
> 80	        .limit(40);
> 81	      if (error) throw error;
> 82	      return (data ?? []) as ExecRow[];
> 83	    },
> 84	    enabled: !!user,
> 85	    refetchInterval: 12_000, // poll for cron-driven execs; pauses when tab hidden (RQ default)
> 86	    staleTime: 8_000,
> 87	  });
> 88	
> 89	  useEffect(() => {
> 90	    const execs = execQuery.data;
> 91	    if (!execs) return;
> 92	
> 93	    // Read live agents without subscribing (avoids React 18 #185 cascade).
> 94	    const { agents, updateAgentStatus } = useCrewStore.getState();
> 95	    const byDbId = new Map(agents.filter((a) => a?.dbId).map((a) => [a.dbId as string, a]));
> 96	
> 97	    // Live Logs: project each exec into a stable LogEntry (id keyed on exec id → no dupes).
> 98	    const logs: LogEntry[] = execs.map((e) => {
> 99	      const agent = byDbId.get(e.agent_id);
> 100	      return {
> 101	        id: `exec-${e.id}`,
> 102	        timestamp: new Date(e.completed_at ?? e.started_at).getTime(),
> 103	        agentId: agent?.id ?? e.agent_id,
> 104	        agentName: agent?.name ?? `agent ${e.agent_id.slice(0, 8)}`,
> 105	        eventType: EVENT_MAP[e.status] ?? 'info',
> 106	        message: buildMessage(e),
> 107	      };
> 108	    });
> 109	    setLogs(logs);
> 110	
> 111	    // Per-agent status: the latest exec per agent wins (execs are sorted desc).
> 112	    const latestStatusByDbId = new Map<string, AgentStatus>();
> 113	    for (const e of execs) {
> 114	      if (!latestStatusByDbId.has(e.agent_id)) {
> 115	        latestStatusByDbId.set(e.agent_id, STATUS_MAP[e.status] ?? 'idle');
> 116	      }
> 117	    }
> 118	    for (const [dbId, status] of latestStatusByDbId) {
> 119	      const agent = byDbId.get(dbId);
> 120	      if (agent && agent.status !== status) updateAgentStatus(agent.id, status);
> 121	    }
> 122	  }, [execQuery.data, setLogs]);
> 123	
> 124	  return {
> 125	    isLoading: execQuery.isLoading,
> 126	    refetch: () => queryClient.invalidateQueries({ queryKey: ['agent_executions', user?.id] }),
> 127	  };
> 128	}
> 129	
> ```

## 🤖 Claude *(02:20:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/constellation-economic-activation.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SOP: Constellation Economic Activation (CEA)
> 2	
> 3	**Status:** ACTIVE · v1.1 · 2026-05-30 (UI agora lê dados reais — fim do mock `useSimulation`)
> 4	**Owner:** Sovereign (Gabriel Zarattini)
> 5	**Survival Law 2 compliance:** SOP retroativa (registrada no seal v6.10.0, promovida a `docs/processes/` no mesmo selo per Phase 5c material proof audit).
> 6	
> 7	---
> 8	
> 9	## Context
> 10	
> 11	A Constelação UI (`/dashboard/constellation`) deploya hoje **137 agentes** (53 Sovereign-owned) com schema rico (`crew_agents.provider`, `model`, `system_prompt`, `squad`, `priority`). Antes da v6.10.0 esses agentes eram **visual demo apenas** — `useSimulation.ts` flipava status aleatoriamente client-side, sem chamadas reais a provedores.
> 12	
> 13	CEA introduz o ciclo **real-cost**: agents executam tarefas, consomem tokens reais, registram custo em USD/mcoCoins, e (para users não-Sovereign) debitam o balance. Sovereign opera em modo admin freebie (analytics-only) por design.
> 14	
> 15	A precificação interna de mcoCoins depende de dados acumulados durante 7d+ via cron diário. A `MARGIN_FACTOR` (hoje 2.0 na RPC `calc_agent_cost_mcoin`) será calibrada após esse período.
> 16	
> 17	---
> 18	
> 19	## Operator
> 20	
> 21	- **Cron daemon (ubuntu user):** dispara `scripts/agent-daily-pulse.sh` diariamente às `0 7 * * *` (sistema BRT = 10:00 UTC)
> 22	- **Edge function `agent-task-execute`:** executa cada task em isolamento (1 task = 1 row em `agent_executions`)
> 23	- **Sovereign manual via UI** (futuro — wire pendente do `NodeDetailsPanel`): dispara tasks ad-hoc
> 24	
> 25	---
> 26	
> 27	## Pre-conditions
> 28	
> 29	| # | Check | Material proof |
> 30	|---|---|---|
> 31	| 1 | `user_api_keys.groq_api_key` populado para target user | REST GET retorna SET |
> 32	| 2 | `crew_agents` rows ativos com `provider` + `model` válidos | REST GET filtered |
> 33	| 3 | `agent_pricing` seedado com par (provider, model) usado | RPC `calc_agent_cost_mcoin` returns sem `pricing_not_found` |
> 34	| 4 | Migration `agent_metering_minimal` aplicada | Schema cache lista `agent_executions` |
> 35	| 5 | Edge function `agent-task-execute` deployed e ACTIVE | `supabase functions list` confirma |
> 36	
> 37	---
> 38	
> 39	## Sequence (execução por ciclo)
> 40	
> 41	### Step 1 — Trigger (cron OR manual)
> 42	Cron diário OR edge function direct invoke.
> 43	
> 44	**Cron path** (`scripts/agent-daily-pulse.sh`):
> 45	- Loop por todos Directors Sovereign-owned (1 por squad — ops/content/tech/market)
> 46	- Para cada: INSERT pending row + chamar Groq direto + UPDATE done
> 47	
> 48	**Edge path** (`POST /functions/v1/agent-task-execute`):
> 49	- Body: `{ agent_id, task_prompt, override_provider?, override_model? }`
> 50	- Auth: user JWT (RLS) OR service-role + `x-user-id` header (admin path)
> 51	
> 52	### Step 2 — Fetch agent + key
> 53	SELECT `crew_agents` por `id` (RLS enforce ownership). SELECT `user_api_keys` por user. Resolve provider→endpoint→apiKey.
> 54	
> 55	### Step 3 — INSERT execution row (status=running)
> 56	```sql
> 57	INSERT INTO agent_executions (agent_id, user_id, prompt, provider, model, status='running')
> 58	RETURNING id
> 59	```
> 60	
> 61	### Step 4 — Call LLM provider
> 62	Endpoint conforme provider:
> 63	- `groq` → `https://api.groq.com/openai/v1/chat/completions`
> 64	- `openrouter` → `https://openrouter.ai/api/v1/chat/completions`
> 65	- `openai` → `https://api.openai.com/v1/chat/completions`
> 66	
> 67	Body: OpenAI-compatible chat completions com `max_tokens=500` (cap pilot).
> 68	
> 69	### Step 5 — Capture usage + compute cost
> 70	- `tokens_in = response.usage.prompt_tokens`
> 71	- `tokens_out = response.usage.completion_tokens`
> 72	- RPC `calc_agent_cost_mcoin(tokens_in, tokens_out, provider, model)` → retorna `cost_usd_micro` + `cost_mcoin`
> 73	
> 74	### Step 6 — UPDATE execution row (status=done)
> 75	PATCH com response + tokens + cost + latency + completed_at.
> 76	
> 77	### Step 7 — Hybrid billing (CEA-F)
> 78	**Se `user.id == SOVEREIGN_USER_ID`**: skip deduct (admin freebie · `sovereign_freebie=true`).
> 79	**Se outro user**: `RPC deduct_mco_coins(user_id, cost_mcoin)` → atomic debit.
> 80	**Se deduct falha**: log warn, NÃO falha o exec (audit trail preservado · `billed=false`).
> 81	
> 82	### Step 8 — Telemetry pulse
> 83	- `scripts/agent-daily-pulse.sh` insere pulse `service=agent-daily-pulse status=healthy` em `infra_health_logs`
> 84	- Edge function: log via `console.log` (Supabase function logs)
> 85	
> 86	---
> 87	
> 88	## Verification gates
> 89	
> 90	| Gate | Check | Pass criterion |
> 91	|---|---|---|
> 92	| G1 | `agent_executions` row final state | `status=done` · `tokens_in > 0` · `tokens_out > 0` · `cost_usd_micro > 0` · `cost_mcoin >= 1` · `completed_at IS NOT NULL` |
> 93	| G2 | Pricing applied | `cost_mcoin = CEIL((tokens_in*price_in + tokens_out*price_out)/1M / 100 * 2 * 1000)` ou floor 1 |
> 94	| G3 | Latency within budget | `latency_ms < 5000` (Groq target) ou `< 15000` (OpenRouter/OpenAI) |
> 95	| G4 | Hybrid billing correct | Sovereign: `mco_balance` unchanged · outros: `mco_balance -= cost_mcoin` |
> 96	| G5 | Cron pulse healthy | `infra_health_logs.service=agent-daily-pulse last_seen_at` < 25h (cron `0 7 * * *`) |
> 97	
> 98	---
> 99	
> 100	## Recovery path (failure scenarios)
> 101	
> 102	| Cenário | Detecção | Recovery |
> 103	|---|---|---|
> 104	| Provider 401/403 | `agent_executions.error_msg ~ provider_\d+` | UPDATE `status=failed` (já feito pelo handler) · investigar `user_api_keys.<provider>_api_key` |
> 105	| Provider timeout | `latency_ms > 30s` ou `fetch_error` | UPDATE `status=failed` · re-tentar manualmente |
> 106	| pricing_not_found | RPC retorna `{"error":"pricing_not_found"}` | Adicionar row em `agent_pricing` ANTES de re-tentar |
> 107	| deduct_mco_coins fails (saldo insuf) | `console.warn` no edge logs · `billed=false` no response | User precisa top-up · exec já completo, sem cobrança · re-tentar quando saldo ok |
> 108	| Cron silent failure (sem pulse) | `infra_health_logs` sem `agent-daily-pulse` pulse > 25h | Checar `/var/log/mcorch-agent-daily-pulse.log` · permissões + Groq key |
> 109	
> 110	---
> 111	
> 112	## Success signal (whole protocol)
> 113	
> 114	**Diário**:
> 115	- 4+ rows novas em `agent_executions` com `status=done` (1 por Director Sovereign)
> 116	- 1 pulse novo em `infra_health_logs.service=agent-daily-pulse status=healthy`
> 117	- (Sovereign-only) `mco_balance` permanece — admin freebie operando
> 118	
> 119	**Após 7d**:
> 120	- ~28+ executions acumuladas
> 121	- Dashboard `/dashboard/agent-economics` mostra KPIs: tokens IN/OUT total, USD, mcoCoins, by_squad breakdown
> 122	- `MARGIN_FACTOR` pode ser calibrado com base nos dados (decisão Sovereign + scientist)
> 123	
> 124	---
> 125	
> 126	## Anti-patterns prohibited
> 127	
> 128	- ❌ Cobrar Sovereign em CEA (viola design hybrid billing — Sovereign opera em modo admin freebie)
> 129	- ❌ Hardcodar custo fixo em vez de usar `calc_agent_cost_mcoin` RPC (drift entre código e source-of-truth)
> 130	- ❌ Esquecer `max_tokens=500` cap no pilot (custo explode rapidamente em tasks longas com gpt-4)
> 131	- ❌ Default provider/model `Anthropic/Claude 3.5 Sonnet` no cron diário (66 mcoCoins/exec · 33x Groq) — usar `groq/llama-3.3-70b-versatile` (1 mcoCoin floor)
> 132	- ❌ Cancelar/refund `mcoin_transactions` sem registrar `action=refund:<reason>` (auditoria de ledger quebra)
> 133	- ❌ UPDATE `agent.status` permanecendo em `thinking`/`running` sem reset back to `idle` (UI fica enganada)
> 134	
> 135	---
> 136	
> 137	## Pricing reference (cents per 1M tokens · seed `agent_pricing` 2026-05-27)
> 138	
> 139	| Provider | Model | IN cents/1M | OUT cents/1M | Notes |
> 140	|---|---|---|---|---|
> 141	| groq | llama-3.1-8b-instant | 5 | 8 | Ultra-cheap (tasks triviais) |
> 142	| openrouter | google/gemini-2.5-flash | 7.5 | 30 | Best perf/cost |
> 143	| openai | gpt-4o-mini | 15 | 60 | OpenAI cheap path |
> 144	| groq | llama-3.3-70b-versatile | 59 | 79 | **Pilot default** |
> 145	| openrouter | meta-llama/llama-3.3-70b-instruct | 80 | 120 | Same model via OR |
> 146	| openrouter | anthropic/claude-3.5-sonnet | 300 | 1500 | Premium (Directors em tasks críticas) |
> 147	| openai | gpt-4 | 3000 | 6000 | Legacy expensive — avoid |
> 148	
> 149	**Refresh policy:** quando provider anunciar mudança de preço, UPDATE row em `agent_pricing` com `notes` indicando data + fonte. Histórico não-preservado (last-write-wins) porque execuções históricas carregam o cost calculado no momento do exec (snapshot via `agent_executions.cost_usd_micro` + `cost_mcoin`).
> 150	
> 151	---
> 152	
> 153	## Connection to Survival Laws
> 154	
> 155	- **Lei 1 (Materialidade):** todo exec materialmente registrado em `agent_executions` com UUID · cost computed via RPC (não hardcoded) · response preservado para auditoria.
> 156	- **Lei 2 (Anticipated Process):** SOP escrita antes da Phase 6 do seal v6.10.0 ser fechada (audit Phase 5c bloqueou e forçou esta criação retroativa — exatamente o caso de uso da skill `mcorch-qa-healing`).
> 157	- **Lei 3 (Pruning):** `agent_executions` é write-once, append-only · não carrega histórico em contexto · query window default 7d no dashboard.
> 158	- **Lei 4 (ORO):** cron operator = ubuntu daemon · edge operator = function runtime · reviewer = Sovereign (via dashboard) · owner = Sovereign (blast radius = balance Sovereign + custo USD agregado).
> 159	
> 160	---
> 161	
> 162	## v1.1 — UI Wiring (2026-05-30)
> 163	
> 164	A UI da Constelação (`/dashboard/constellation`) deixou de ser teatro: antes `useSimulation.ts` (status aleatório + mensagens hardcoded a cada 3s) alimentava os Live Logs e o status 3D. Agora:
> 165	
> 166	- **`src/hooks/useAgentActivity.ts`** (novo) — lê `agent_executions` reais (poll 12s + invalidate on mutation), projeta cada exec em `store.logs` (Live Logs) e em `updateAgentStatus` por agente (running→thinking · done→idle · failed→error · pending→waiting). Mapeamento `agent_executions.agent_id === crew_agents.id === store Agent.dbId`. Usa `getState()` dentro do efeito (evita React 18 #185).
> 167	- **`ConstellationPage.tsx`** — `useSimulation()` → `useAgentActivity()`.
> 168	- **`AgentDetail.tsx`** — botão **"Executar tarefa"** (Textarea de prompt) → `useAgentTask` → `agent-task-execute`. Override pilot forçado `groq/llama-3.3-70b-versatile` (guardrail: provider próprio dos agentes seed pode ser `Anthropic`=sem endpoint ou `Llama 3`=sem pricing). Desabilitado se `!agent.dbId`.
> 169	- **`useCrewStore`** — novo action `setLogs`.
> 170	
> 171	**Verificação:** `npx tsc --noEmit` zero erros · build OK · Live Logs passam a refletir os 19 execs reais + cron diário; clicar "Executar" gera 1 row real (Groq · ~1 mco · freebie Sovereign) visível em <12s.
> 172	
> 173	**Drift conhecido (follow-up):** seed `crew_agents` usa `provider`/`model` que não casam com `agent_pricing` (Directors=Anthropic sem endpoint no edge; specialists model="Llama 3"). Por isso o override pilot. Corrigir o seed (`enterprise-seed.ts` + `seed_crew_template`) para provider/model válidos é o próximo passo para execução sem override.
> 174	
> 175	---
> 176	
> 177	## Future work (registered as backlog)
> 178	
> 179	- ~~Wire button "Executar tarefa" na UI da Constelação (manual trigger)~~ ✅ DONE v1.1 — `AgentDetail.tsx`
> 180	- ~~UI lê execs reais em vez de mock~~ ✅ DONE v1.1 — `useAgentActivity.ts`
> 181	- Corrigir seed `crew_agents` (provider/model válidos vs `agent_pricing`) → remover necessidade do override pilot
> 182	- Expandir cron daily pulse para incluir specialists além de Directors (108 specialists hoje em IDLE)
> 183	- Calibrar `MARGIN_FACTOR` com base em 7d+ data
> 184	- Adicionar dimensão `task_category` em `agent_executions.metadata` para análise per-tipo-de-task
> 185	- Webhook de provider rate-limit → bloquear cron temporariamente
> 186	
> ```

## 🤖 Claude *(02:23:07)*


## 🤖 Claude *(02:23:29)*

Verificação material concluída. O diagnóstico mudou de figura — e tem uma descoberta que muda tudo.

## 🔍 Veredito da verificação (tudo via REST service-role + leitura de código, este turno)

**1. A poda não tocou na Constelação.** A queda 11925→9040 foi em `mcorch_edges` (knowledge mesh). Mas o 3D lê de **outra fonte** — as tabelas `crew_agents`/`crew_edges`, que estão **intactas e cheias**:
- **`crew_agents` = 717 linhas** · **`crew_edges` = 689 linhas** (vivos agora)
- Espalhados por **27 usuários** (RLS isola cada um)
- **Sua conta (`ada39fae…`) = 53 agentes** = 1 Core + 4 Leads + 4×**12** specialists → é exatamente a tela poluída da imagem
- Mesh mirror (`mcorch_nodes` type=crew_agent) = só **79 nós**

Ou seja: a poda removeu arestas do cérebro (mesh), mas a constelação visual continua 100% inchada. É por isso que a página não mudou.

**2. Três seeders divergentes (drift de contagem):**
| Seeder | Membros/squad | Total | Aciona |
|---|---|---|---|
| `seed_crew_template` (RPC, DB) | **6** | 29 | auto, quando user tem 0 agentes |
| `seedEnterpriseStructure()` (store) | 6 | 29 | legado/não-usado |
| `deployEnterpriseToSupabase()` (botão "Deploy Enterprise") | **12** | 53 | foi o que gerou a sua tela |

**3. O trabalho real JÁ EXISTE (CEA v1.1, selada v6.10.0) — não começamos do zero.** Há `agent_executions` (execs LLM reais com tokens/custo/latência), edge `agent-task-execute` (chama Groq/OpenRouter/OpenAI de verdade), cron `agent-daily-pulse` diário, `useAgentActivity` (substituiu o mock `useSimulation`), `calc_agent_cost_mcoin` + billing híbrido (Sovereign freebie), e o dashboard `/dashboard/agent-economics`. **A própria SOP da CEA já registra como pendência exatamente o que você pediu**: "corrigir o seed para provider/model válidos" + "expandir o pulse para incluir os specialists (108 hoje em IDLE)".

**4. Reporte ao Core já está cabeado:** edges `Directive` (Core→Lead) e `Reporting` (Lead→specialist). A hierarquia que você quer já é a topologia — só está inchada e com provider/model inválidos (Leads=`anthropic` sem endpoint no edge; specialists=`Llama 3` sem pricing → hoje rodam só com override-piloto).

## ⚖️ BoK Gate (MCORCH Master Execution Protocol)
- Limpar topologia (12→4) + corrigir provider/model + ligar os 4 specialists ao daily pulse = **dentro do módulo `mcorch-constellation` (BoK 9/9) e já documentado na CEA SOP** → não exige novo BoK.
- Fazer cada subagente **invocar a função real do seu módulo** (Viral Miner→`fetch-trends`, Canvas→`canvas-execute`, Orquestração→`orchestrate-content`, Afiliados→`link-forge`…) = **capability nova → dispara BoK Gate** (`/bok-scribe` ou CEA SOP v2 antes de codar).

## 🗺️ Mapeamento que proponho (16 subagentes = 4×4, cada um dono de um módulo real)
| Depto (Lead → Core) | Sub 1 | Sub 2 | Sub 3 | Sub 4 |
|---|---|---|---|---|
| 🎨 Creative Content | Conteúdo | Blog | Canvas Studio | Canvas Design |
| 📈 Market Intelligence | Viral Miner | Analytics | Produtos | Campanhas |
| ⚡ Operational Ops | Afiliados | Calendário | Orquestração | Publicação Social |
| ⚙️ Technical Engine | Core/AIOS | IA Arena | agent-economics | Watchdog/Infra |

**Nota material:** re-seedar apaga+recria `crew_agents`, então os `agent_executions` antigos (keyed por `agent_id`) orfanam. Vou padronizar nos `agent_key` estáveis da RPC (`leader-content`, `agent-content-1`…) para que re-seeds futuros sejam idempotentes e o histórico re-vincule.

Antes de tocar em qualquer linha, preciso de 3 decisões suas (mudam blast radius e o BoK Gate):

## 🤖 Claude *(02:23:41)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "A topologia limpa (4 subagentes/depto) deve atingir s\u00f3 a sua conta ou tamb\u00e9m os seeders? (H\u00e1 26 outros tenants com crews pr\u00f3prias.)",
      "header": "Escopo do reset",
      "multiSelect": false,
      "options": [
        {
          "label": "Seeders + minha conta",
          "description": "Corrijo seed_crew_template (6\u21924) e deployEnterpriseToSupabase (12\u21924) para novos users nascerem limpos, e re-seedo S\u00d3 a sua conta (53\u219221). N\u00c3O toco nas crews dos outros 26 tenants. Fix permanente + n\u00e3o-destrutivo aos outros."
        },
        {
          "label": "S\u00f3 minha conta",
          "description": "Re-seed apenas ada39fae (53\u219221). Os seeders ficam como est\u00e3o \u2014 novos signups ainda nasceriam com 6/12. Menor mudan\u00e7a poss\u00edvel."
        },
        {
          "label": "Tudo + migrar os 26 users",
          "description": "\u26a0\ufe0f Re-seed todos os 27 usu\u00e1rios. Apaga e recria as crews dos outros tenants \u2014 eles perdem qualquer customiza\u00e7\u00e3o atual. Maior blast radius."
        }
      ]
    },
    {
      "question": "Qu\u00e3o 'real' \u00e9 o trabalho dos subagentes neste primeiro corte?",
      "header": "Profundidade",
      "multiSelect": false,
      "options": [
        {
          "label": "Faseado: LLM real agora, m\u00f3dulos via BoK depois",
          "description": "Agora (sem novo BoK, dentro da CEA): provider/model v\u00e1lido + os 4 specialists/depto no daily pulse rodando prompts LLM reais tem\u00e1ticos do m\u00f3dulo. Depois: cada subagente invoca a fun\u00e7\u00e3o real do m\u00f3dulo via /bok-scribe."
        },
        {
          "label": "S\u00f3 topologia/visual agora",
          "description": "Reduzo 12\u21924 e garanto o reporte ao Core, sem mexer em execu\u00e7\u00e3o. Resolve a polui\u00e7\u00e3o/perf/z-index; os agentes seguem tem\u00e1ticos mas sem trabalho LLM novo."
        },
        {
          "label": "Invoca\u00e7\u00e3o real de m\u00f3dulos j\u00e1",
          "description": "\u26a0\ufe0f Dispara o BoK Gate: escrevo a BoK/SOP da nova capability (subagente\u2192fun\u00e7\u00e3o real do m\u00f3dulo) ANTES de qualquer c\u00f3digo de execu\u00e7\u00e3o. Mais lento, mas \u00e9 a vis\u00e3o completa de uma vez."
        }
      ]
    },
    {
      "question": "Confirma o mapeamento dos 16 subagentes m\u00f3dulo\u2192departamento que propus?",
      "header": "Mapa m\u00f3dulos",
      "multiSelect": false,
      "options": [
        {
          "label": "Aceito o proposto",
          "description": "Sigo o 4\u00d74 da tabela: Content(Conte\u00fado/Blog/Canvas Studio/Canvas Design) \u00b7 Market(Viral Miner/Analytics/Produtos/Campanhas) \u00b7 Ops(Afiliados/Calend\u00e1rio/Orquestra\u00e7\u00e3o/Publica\u00e7\u00e3o) \u00b7 Tech(Core/IA Arena/agent-economics/Watchdog).",
          "preview": "\ud83c\udfa8 Creative Content \u2192 Conte\u00fado \u00b7 Blog \u00b7 Canvas Studio \u00b7 Canvas Design\n\ud83d\udcc8 Market Intelligence \u2192 Viral Miner \u00b7 Analytics \u00b7 Produtos \u00b7 Campanhas\n\u26a1 Operational Ops \u2192 Afiliados \u00b7 Calend\u00e1rio \u00b7 Orquestra\u00e7\u00e3o \u00b7 Publica\u00e7\u00e3o Social\n\u2699\ufe0f Technical Engine \u2192 Core/AIOS \u00b7 IA Arena \u00b7 agent-economics \u00b7 Watchdog/Infra\n\n(Todos os 4 Leads \u2192 GCRUX Core)"
        },
        {
          "label": "Quero remapear",
          "description": "O 4\u00d74 n\u00e3o est\u00e1 certo \u2014 eu descrevo os ajustes (trocar m\u00f3dulos de depto, incluir/remover algum, renomear) antes de voc\u00ea seedar."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "A topologia limpa (4 subagentes/depto) deve atingir só a sua conta ou também os seeders? (Há 26 outros tenants com crews próprias.)"="Não existe outro usuário, esses agentes devem ser per user, e todos deve ser calibrados para o consumo de mcoCoins e tambem deve ter controle de consulmo das suas apis BYOK. Não entendi o que seria os outros 26 tenants. E sim todos os novos usuários devem vir vazios para serem criados do zero. Talvez seria melhor limpar o nosso tambem, fazendo um E2E completo desse módulo de constalattion. Além disso em algum momento pode ter acontecido uma confusão de colocar esses agentes para trabalhar dentro do sistema assim como você esta fazendo isso não pode acontecer, os agentes deve trabahar e ter acesso configurado previamente somente per usar full account per users.", "Quão 'real' é o trabalho dos subagentes neste primeiro corte?"="Acredito que invocação real de módulos já, seria o melhor  caminho, pois esse módulo nasceu junto com a casca logo no inicio quando criado pelo lovable, acredito que agora estamos muito mais avançados e robustos no desenvolvimento então tome os caminhos de refatoramento completo e talvez se necessário criando de fato um v2 de tudo.", "Confirma o mapeamento dos 16 subagentes módulo→departamento que propus?"="Aceito o proposto" selected preview:
> 🎨 Creative Content → Conteúdo · Blog · Canvas Studio · Canvas Design
> 📈 Market Intelligence → Viral Miner · Analytics · Produtos · Campanhas
> ⚡ Operational Ops → Afiliados · Calendário · Orquestração · Publicação Social
> ⚙️ Technical Engine → Core/AIOS · IA Arena · agent-economics · Watchdog/Infra
> 
> (Todos os 4 Leads → GCRUX Core). You can now continue with these answers in mind.
> ```

## 🤖 Claude *(02:36:55)*


## 🤖 Claude *(02:37:06)*

Captei o reframe — e ele é grande. Deixa eu refletir o que mudou e tomar a atitude que o protocolo exige.

**O que entendi da sua direção:**
- **Agentes per-user, escopados à conta completa do usuário** (conteúdo, canvas, campanhas, BYOK, mcoCoins dele). São **agentes de produto voltados ao tenant** — **NUNCA** agentes que operam o sistema/dev do MCORCH (o que **eu**, Claude Code, faço no repo). Essa separação tem que ser barreira arquitetural, não convenção. Entendido e será requisito de segurança central.
- **Novos usuários nascem vazios** — removo o auto-seed (`seed_crew_template`); o usuário cria a crew do zero.
- **mcoCoins calibrado + controle de consumo das APIs BYOK por usuário** (resolução per-user de chaves + caps de consumo).
- **4×4 aceito** · Leads → GCRUX Core.
- **Refatoramento completo / v2 de tudo** — o módulo nasceu como casca do Lovable; reconstruir direito.

**Atitude obrigatória agora — Closed-Loop Protocol (BoK Gate):**
Você escolheu **"invocação real de módulos + v2 de tudo"** — exatamente o que sinalizei como gatilho do Gate. Isso é uma **mudança arquitetural complexa**, então pelo MCORCH Master Execution Protocol eu **não inicio o código do v2 sem selar a família BoK primeiro** (MRD→BRD→PRD→FRD→SDD…). A BoK atual de `mcorch-constellation` documenta a **casca**, não o v2 com invocação real + tenancy/economia/acesso novos. Pular isso é a dívida exponencial que a Lei 2 blinda — e já temos prova: a CEA v1.1 foi bloqueada na Fase 5c do v6.10.0 justamente por falta de SOP antecipada.

**Sobre os "26 tenants" que você não reconheceu:** são 26 `user_id` distintos (além do seu) que existem na tabela `crew_agents` — quase certo que são contas de teste/preview, porque a RPC antiga **auto-semeava 29 agentes para qualquer conta** que abrisse a página. Não devem ser clientes reais. Vou confirmar materialmente agora (perfis reais vs. linhas órfãs) pra te dar o número exato e definir a limpeza do reset:

## 🤖 Claude *(02:37:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nBASE=\"${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}/rest/v1\"\nHK=(-H \"apikey: $SUPABASE_SERVICE_ROLE_KEY\" -H \"Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY\")\n\necho \"\u2550\u2550\u2550 profiles (contas reais) \u2550\u2550\u2550\"\ncurl -s \"$BASE/profiles?select=id,created_at,mco_balance&order=created_at.asc\" \"${HK[@]}\" > /tmp/prof.json\nif jq -e . /tmp/prof.json >/dev/null 2>&1; then\n  echo \"TOTAL profiles: $(jq 'length' /tmp/prof.json)\"\n  echo \"\u2500\u2500 created_at span \u2500\u2500\"; jq -r '[.[].created_at]|\"first: \\(min)  last: \\(max)\"' /tmp/prof.json\n  echo \"\u2500\u2500 mco_balance distrib \u2500\u2500\"; jq -r 'group_by(.mco_balance)[]|\"balance \\(.[0].mco_balance): \\(length) contas\"' /tmp/prof.json\nelse\n  echo \"profiles query error:\"; cat /tmp/prof.json\nfi\n\necho \"\"; echo \"\u2550\u2550\u2550 crew owners (distinct) \u2550\u2550\u2550\"\ncurl -s \"$BASE/crew_agents?select=user_id\" \"${HK[@]}\" | jq -r '[.[].user_id]|unique|length' | xargs echo \"distinct crew owners:\"\n\necho \"\"; echo \"\u2550\u2550\u2550 agent_executions (hist\u00f3rico real CEA) \u2550\u2550\u2550\"\ncurl -s -I \"$BASE/agent_executions?select=id\" \"${HK[@]}\" -H \"Prefer: count=exact\" 2>/dev/null | grep -i content-range || echo \"(sem header)\"\n\necho \"\"; echo \"\u2550\u2550\u2550 SOVEREIGN_USER_ID (confirmar qual owner \u00e9 o seu) \u2550\u2550\u2550\"\ngrep -rhn \"SOVEREIGN_USER_ID\\s*=\" .env scripts/ 2>/dev/null | sed 's/\\(SOVEREIGN_USER_ID=\\)\\(........\\).*/\\1\\2\u2026(redacted tail)/' | head -3\ngrep -rhn \"SOVEREIGN_USER_ID\" supabase/functions/ 2>/dev/null | grep -i \"default\\|===\\|==\" | head -3",
  "description": "Characterize profiles vs crew owners + CEA history + sovereign id"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ═══ profiles (contas reais) ═══
> TOTAL profiles: 1
> ── created_at span ──
> first: 2026-04-17T05:57:46.249257+00:00  last: 2026-04-17T05:57:46.249257+00:00
> ── mco_balance distrib ──
> balance 5351.00: 1 contas
> 
> ═══ crew owners (distinct) ═══
> distinct crew owners: 27
> 
> ═══ agent_executions (histórico real CEA) ═══
> content-range: 0-30/31
> 
> ═══ SOVEREIGN_USER_ID (confirmar qual owner é o seu) ═══
> 270:    if (user.id !== SOVEREIGN_USER_ID && costMcoin > 0) {
> 296:      sovereign_freebie: user.id === SOVEREIGN_USER_ID,
> ```

## 🤖 Claude *(02:38:59)*


## 🤖 Claude *(02:39:21)*

Material confirmado — e fecha a questão das contas exatamente como você intuiu:

## 🔍 Verdito das contas
- **`profiles` = 1 conta** (você, criada 2026-04-17, saldo 5351 mco).
- **`crew_agents` = 27 owners distintos** → **26 são órfãos sem perfil**. Não são usuários: são restos de contas deletadas/testes que a RPC antiga auto-semeou. Você está certo: **não existe outro usuário real.**
- Tradução: ~**688 das 717 linhas** de `crew_agents` (+ arestas) são **lixo a purgar**. Sua crew real = os 53 nós inchados (clique no "Deploy Enterprise").
- Bônus material: **31 execs reais** em `agent_executions` (histórico econômico da CEA) — vão orfanar no reset; decido preservar/arquivar na BoK.

## ⚖️ BoK Gate — EM VIGOR (não codo o v2 sem selar a Fonte da Verdade)
Você pediu o caminho que **dispara o Closed-Loop Protocol**. A BoK de `mcorch-constellation` documenta a **casca Lovable**, não este v2. Então o próximo passo material **não é código — é selar a família BoK** do `constellation-v2` como SSOT, e só então refatorar. (A própria CEA provou o custo de pular isso: barrada na Fase 5c por falta de SOP.)

**Brief que eu passaria ao `/bok-scribe constellation-v2`:**
> Cockpit operacional de agentes **per-user**. (1) Agentes escopados 100% à conta do tenant, **sem acesso ao sistema/dev MCORCH** — barreira de segurança dura (≠ do que eu, Claude Code, faço no repo). (2) Novos users nascem **vazios** (remover auto-seed), criação on-demand. (3) Topologia 4 deptos × (1 Lead + 4 subagentes módulo-bound) → Leads → GCRUX Core (mapa 4×4 aprovado). (4) Cada subagente **invoca a função real do módulo** reusando as edge functions robustas que já temos (fetch-trends, canvas-execute, orchestrate-content, link-forge, publish-*…) via camada de roteamento de capability. (5) Economia: toda ação medida em mcoCoins (`calc_agent_cost_mcoin`+`deduct_mco_coins`, freebie Sovereign) + resolução **BYOK per-user** + **caps de consumo** por user/API. (6) Acesso **pré-configurado por subagente** (UI: habilita módulo + binda chave BYOK + define caps). Fundação = CEA v1.1. Reset: purgar 26 órfãos + wipe da crew Sovereign + **E2E completo** vazio→criar→trabalhar→medir.

**Forks de arquitetura que decidi por engenharia** (você delegou "tome os caminhos" — sinalizo para veto):
- **A1 — reusar edge functions existentes** como ferramentas dos subagentes (camada fina de roteamento), **não** reescrever os módulos. Menor risco, aproveita o que já é robusto. *(Alternativa A2 = runtime LLM tool-calling — fica para camada posterior.)*
- **B — config de acesso por subagente** (settings: módulo + BYOK + caps) = o "acesso pré-configurado" que você exigiu.
- **C — refatorar v2 in-place** (só 1 user real + é casca), atrás de um reset limpo de dados. Sem rota paralela.

**Roadmap que a BoK vai formalizar (depois do selo):**
1. **Fase 0** — purge dos 26 órfãos + wipe da sua crew + remover auto-seed (empty-start).
2. **Fase 1** — seed on-demand 4×4 (provider/model válidos, agent_keys estáveis) + reporte ao Core.
3. **Fase 2** — camada de capability: subagente → função real do módulo (BYOK + mcoCoins + caps).
4. **Fase 3** — UI de config de acesso + fix de perf/z-index do 3D.
5. **Fase 4** — E2E completo do módulo + Fase 5c (prova material).

**ORO:** Operator=eu · Reviewer/Owner=você (blast radius expandido: gasto LLM real por tenant + manuseio de chaves BYOK = security-sensitive).

**Poda (Lei 3):** já extraí o modelo — solto da atenção ativa o dump gigante dos leaders e os conteúdos completos dos arquivos lidos; referência preservada em `src/lib/enterprise-seed.ts`, `supabase/migrations/20260425000000_enterprise_hierarchy.sql`, `docs/processes/constellation-economic-activation.md`.

Recomendo selar via `/bok-scribe constellation-v2` com esse brief. **Me dá o OK (ou corrige um fork) que eu disparo agora** — nenhuma linha de código do v2 antes do selo.

## 👤 User *(02:40:17)*

Ok vai em frente com o /bok-scribe  e tambem use o /bok-agents-generator  para efetivar tudo oficialmente

## 🤖 Claude *(02:41:23)*


## 🤖 Claude *(02:41:24)*

Selado o OK. Sequência correta: **`/bok-scribe constellation-v2` primeiro** (sela a Fonte da Verdade — MRD→…→SDD+Data Model+Process+Quality), e **na sequência `/bok-agents-generator`** (formaliza o sistema de agentes oficial sobre essa BoK). Disparando o primeiro agora:

## 🤖 Claude *(02:41:37)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "bok-scribe",
  "args": "constellation-v2\n\nRefatora\u00e7\u00e3o v2 completa do m\u00f3dulo /dashboard/constellation (hoje casca Lovable) \u2014 cockpit operacional de agentes de produto PER-USER.\n\nVIS\u00c3O: cada usu\u00e1rio tem sua pr\u00f3pria constela\u00e7\u00e3o de agentes que executam trabalho real DENTRO DA CONTA DELE, acionando os m\u00f3dulos do ecossistema. Substitui a casca decorativa atual (717 crew_agents, 26 owners \u00f3rf\u00e3os) por uma topologia enxuta e funcional.\n\nTOPOLOGIA: 4 departamentos \u00d7 (1 Lead + 4 subagentes m\u00f3dulo-bound) + GCRUX Core central; Leads reportam ao GCRUX Core. Mapa 4\u00d74 aprovado pelo Sovereign:\n- Creative Content (\ud83c\udfa8): Conte\u00fado \u00b7 Blog \u00b7 Canvas Studio \u00b7 Canvas Design\n- Market Intelligence (\ud83d\udcc8): Viral Miner \u00b7 Analytics \u00b7 Produtos \u00b7 Campanhas\n- Operational Ops (\u26a1): Afiliados \u00b7 Calend\u00e1rio \u00b7 Orquestra\u00e7\u00e3o \u00b7 Publica\u00e7\u00e3o Social\n- Technical Engine (\u2699\ufe0f): Core/AIOS \u00b7 IA Arena \u00b7 agent-economics \u00b7 Watchdog/Infra\n\nREQUISITOS CR\u00cdTICOS:\n1. Isolamento de tenant DURO: agentes escopados 100% \u00e0 conta do user via auth.uid(); ZERO acesso ao sistema/dev MCORCH ou a outros tenants (barreira de seguran\u00e7a, n\u00e3o conven\u00e7\u00e3o).\n2. Empty-start: novos usu\u00e1rios nascem com constela\u00e7\u00e3o vazia (remover auto-seed seed_crew_template); cria\u00e7\u00e3o on-demand pelo user.\n3. Invoca\u00e7\u00e3o real de m\u00f3dulos: cada subagente chama a fun\u00e7\u00e3o real do seu m\u00f3dulo reusando edge functions existentes (fetch-trends, canvas-execute, orchestrate-content, link-forge, publish-meta/social/wordpress, analytics) via camada fina de roteamento de capability \u2014 N\u00c3O reescrever os m\u00f3dulos.\n4. Economia per-user: toda a\u00e7\u00e3o medida em mcoCoins (RPC calc_agent_cost_mcoin + deduct_mco_coins at\u00f4mico; Sovereign = admin freebie) + resolu\u00e7\u00e3o BYOK per-user de chaves (user_api_keys) + caps de consumo por user/API.\n5. Acesso pr\u00e9-configurado por subagente (UI de settings: habilitar m\u00f3dulo + bindar chave BYOK + definir caps de mcoCoins/API).\n\nFUNDA\u00c7\u00c3O EXISTENTE (reusar, n\u00e3o recriar): CEA v1.1 \u2014 tabela agent_executions, edge function agent-task-execute, cron agent-daily-pulse, tabela agent_pricing, hook useAgentActivity, dashboard /dashboard/agent-economics. SOP existente docs/processes/constellation-economic-activation.md. Tabelas atuais crew_agents/crew_edges (a migrar/limpar). API Tenancy Model (per-user credentials) j\u00e1 em CLAUDE.md.\n\nRESET/MIGRA\u00c7\u00c3O: purgar 26 owners \u00f3rf\u00e3os (sem profile) de crew_agents/crew_edges (~688 linhas lixo) + wipe da crew Sovereign (53 n\u00f3s) + preservar/arquivar 31 agent_executions reais + E2E completo (vazio\u2192criar\u2192trabalhar\u2192medir).\n\nDECIS\u00d5ES DE ARQUITETURA (Sovereign delegou \"tome os caminhos\"): A1 reusar edge functions como tools via roteamento fino \u00b7 B config de acesso por subagente \u00b7 C refatorar in-place atr\u00e1s de um reset limpo de dados.\n\nM\u00f3dulo \u00e9 mcorch-constellation v2; BoK atual documenta a casca Lovable e deve ser superada por esta su\u00edte. Tooling interno parcial (campos de mercado/monetiza\u00e7\u00e3o podem ser N/A onde fizer sentido), mas a economia per-user (mcoCoins/BYOK) \u00e9 central e deve ter m\u00e9tricas reais."
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: bok-scribe
> ```

## 👤 User *(02:41:37)*

# MCORCH BoK Scribe Agent

You are the **MCORCH BoK Scribe Agent** — the Requirements Engineering layer of the MCORCH
Sovereign Ecosystem. Your role is to act as the translation layer between the
Sovereign/Maestro (the human architect) and the Execution Agents (Claude/Antigravity).

When given a raw business idea in `constellation-v2

Refatoração v2 completa do módulo /dashboard/constellation (hoje casca Lovable) — cockpit operacional de agentes de produto PER-USER.

VISÃO: cada usuário tem sua própria constelação de agentes que executam trabalho real DENTRO DA CONTA DELE, acionando os módulos do ecossistema. Substitui a casca decorativa atual (717 crew_agents, 26 owners órfãos) por uma topologia enxuta e funcional.

TOPOLOGIA: 4 departamentos × (1 Lead + 4 subagentes módulo-bound) + GCRUX Core central; Leads reportam ao GCRUX Core. Mapa 4×4 aprovado pelo Sovereign:
- Creative Content (🎨): Conteúdo · Blog · Canvas Studio · Canvas Design
- Market Intelligence (📈): Viral Miner · Analytics · Produtos · Campanhas
- Operational Ops (⚡): Afiliados · Calendário · Orquestração · Publicação Social
- Technical Engine (⚙️): Core/AIOS · IA Arena · agent-economics · Watchdog/Infra

REQUISITOS CRÍTICOS:
1. Isolamento de tenant DURO: agentes escopados 100% à conta do user via auth.uid(); ZERO acesso ao sistema/dev MCORCH ou a outros tenants (barreira de segurança, não convenção).
2. Empty-start: novos usuários nascem com constelação vazia (remover auto-seed seed_crew_template); criação on-demand pelo user.
3. Invocação real de módulos: cada subagente chama a função real do seu módulo reusando edge functions existentes (fetch-trends, canvas-execute, orchestrate-content, link-forge, publish-meta/social/wordpress, analytics) via camada fina de roteamento de capability — NÃO reescrever os módulos.
4. Economia per-user: toda ação medida em mcoCoins (RPC calc_agent_cost_mcoin + deduct_mco_coins atômico; Sovereign = admin freebie) + resolução BYOK per-user de chaves (user_api_keys) + caps de consumo por user/API.
5. Acesso pré-configurado por subagente (UI de settings: habilitar módulo + bindar chave BYOK + definir caps de mcoCoins/API).

FUNDAÇÃO EXISTENTE (reusar, não recriar): CEA v1.1 — tabela agent_executions, edge function agent-task-execute, cron agent-daily-pulse, tabela agent_pricing, hook useAgentActivity, dashboard /dashboard/agent-economics. SOP existente docs/processes/constellation-economic-activation.md. Tabelas atuais crew_agents/crew_edges (a migrar/limpar). API Tenancy Model (per-user credentials) já em CLAUDE.md.

RESET/MIGRAÇÃO: purgar 26 owners órfãos (sem profile) de crew_agents/crew_edges (~688 linhas lixo) + wipe da crew Sovereign (53 nós) + preservar/arquivar 31 agent_executions reais + E2E completo (vazio→criar→trabalhar→medir).

DECISÕES DE ARQUITETURA (Sovereign delegou "tome os caminhos"): A1 reusar edge functions como tools via roteamento fino · B config de acesso por subagente · C refatorar in-place atrás de um reset limpo de dados.

Módulo é mcorch-constellation v2; BoK atual documenta a casca Lovable e deve ser superada por esta suíte. Tooling interno parcial (campos de mercado/monetização podem ser N/A onde fizer sentido), mas a economia per-user (mcoCoins/BYOK) é central e deve ter métricas reais.`, you autonomously produce the complete
documentation family using the phased workflow below. All documents are saved as markdown
files under `docs/bok/<project-slug>/`.

---

## Identity

```
Role:       Scientist / Architect Layer
Position:   Between Sovereign vision and Execution implementation
Mandate:    Zero-ambiguity documentation; every output feeds directly into
            Supabase schema, Edge Functions, or n8n process flows
Standards:  BABOK v3 · ProdBOK · CXBOK · SWEBOK v4 · CISSP CBK 2024
            DMBOK v2 · BPM CBOK v4 · CMQ/OE BOK
Output dir: docs/bok/<project-slug>/
```

---

## Phase 0 — Project Bootstrapping

Load the agent definition from `.claude/agents/bok-scribe-agent.md` and execute the
full 7-phase workflow described there.

**Input capture (ask if not provided in constellation-v2

Refatoração v2 completa do módulo /dashboard/constellation (hoje casca Lovable) — cockpit operacional de agentes de produto PER-USER.

VISÃO: cada usuário tem sua própria constelação de agentes que executam trabalho real DENTRO DA CONTA DELE, acionando os módulos do ecossistema. Substitui a casca decorativa atual (717 crew_agents, 26 owners órfãos) por uma topologia enxuta e funcional.

TOPOLOGIA: 4 departamentos × (1 Lead + 4 subagentes módulo-bound) + GCRUX Core central; Leads reportam ao GCRUX Core. Mapa 4×4 aprovado pelo Sovereign:
- Creative Content (🎨): Conteúdo · Blog · Canvas Studio · Canvas Design
- Market Intelligence (📈): Viral Miner · Analytics · Produtos · Campanhas
- Operational Ops (⚡): Afiliados · Calendário · Orquestração · Publicação Social
- Technical Engine (⚙️): Core/AIOS · IA Arena · agent-economics · Watchdog/Infra

REQUISITOS CRÍTICOS:
1. Isolamento de tenant DURO: agentes escopados 100% à conta do user via auth.uid(); ZERO acesso ao sistema/dev MCORCH ou a outros tenants (barreira de segurança, não convenção).
2. Empty-start: novos usuários nascem com constelação vazia (remover auto-seed seed_crew_template); criação on-demand pelo user.
3. Invocação real de módulos: cada subagente chama a função real do seu módulo reusando edge functions existentes (fetch-trends, canvas-execute, orchestrate-content, link-forge, publish-meta/social/wordpress, analytics) via camada fina de roteamento de capability — NÃO reescrever os módulos.
4. Economia per-user: toda ação medida em mcoCoins (RPC calc_agent_cost_mcoin + deduct_mco_coins atômico; Sovereign = admin freebie) + resolução BYOK per-user de chaves (user_api_keys) + caps de consumo por user/API.
5. Acesso pré-configurado por subagente (UI de settings: habilitar módulo + bindar chave BYOK + definir caps de mcoCoins/API).

FUNDAÇÃO EXISTENTE (reusar, não recriar): CEA v1.1 — tabela agent_executions, edge function agent-task-execute, cron agent-daily-pulse, tabela agent_pricing, hook useAgentActivity, dashboard /dashboard/agent-economics. SOP existente docs/processes/constellation-economic-activation.md. Tabelas atuais crew_agents/crew_edges (a migrar/limpar). API Tenancy Model (per-user credentials) já em CLAUDE.md.

RESET/MIGRAÇÃO: purgar 26 owners órfãos (sem profile) de crew_agents/crew_edges (~688 linhas lixo) + wipe da crew Sovereign (53 nós) + preservar/arquivar 31 agent_executions reais + E2E completo (vazio→criar→trabalhar→medir).

DECISÕES DE ARQUITETURA (Sovereign delegou "tome os caminhos"): A1 reusar edge functions como tools via roteamento fino · B config de acesso por subagente · C refatorar in-place atrás de um reset limpo de dados.

Módulo é mcorch-constellation v2; BoK atual documenta a casca Lovable e deve ser superada por esta suíte. Tooling interno parcial (campos de mercado/monetização podem ser N/A onde fizer sentido), mas a economia per-user (mcoCoins/BYOK) é central e deve ter métricas reais.):**
1. Business idea (free text — what problem does it solve?)
2. Target market segment (B2B / B2C / B2B2C)
3. Monetization model (subscription / transaction / hybrid)
4. Regulatory sensitivity (LGPD / GDPR / financial / healthcare / none)
5. Integration surface (standalone / extends existing MCORCH feature)

Derive `<project-slug>` from the business idea (kebab-case, max 32 chars).
Create `docs/bok/<project-slug>/` if it does not exist.

---

## Execution

After collecting inputs, execute ALL phases in strict sequence. Do NOT skip phases.
Each phase reads the output of the previous phase.

Load full workflow from: `.claude/agents/bok-scribe-agent.md`
Load all document templates from: `.claude/agents/bok-scribe/templates/`

After all phases complete:
1. Print a summary table listing every file created with its purpose.
2. Insert a Knowledge Mesh node (see Phase 7 in agent definition).
3. Confirm: "BoK documentation suite complete for `<project-slug>`."


## 🤖 Claude *(02:41:53)*


## 🤖 Claude *(02:42:00)*

O skill carregou o workflow de 7 fases. Vou carregar a definição do agente + os templates antes de autorar (a BoK precisa seguir o formato canônico exato — as 5 suítes anteriores foram seladas por esses templates).

**Inputs capturados** (do brief): idea = cockpit de agentes per-user · segmento **B2B2C** · monetização **híbrida** (planos + mcoCoins) · regulatório **LGPD** (dados + credenciais BYOK per-user) · surface = **extends** (refactor v2 do `mcorch-constellation`) · slug = **`constellation-v2`**.

## 🤖 Claude *(02:42:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe-agent.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MCORCH BoK Scribe Agent — Operational Framework
> 2	
> 3	**Version:** 1.0.0  
> 4	**Date:** 2026-05-06  
> 5	**Invocation:** `/bok-scribe <business-idea>`  
> 6	**Output root:** `docs/bok/<project-slug>/`
> 7	
> 8	---
> 9	
> 10	## Agent Identity Contract
> 11	
> 12	```
> 13	Name:         MCORCH BoK Scribe Agent
> 14	Archetype:    Scientist / Architect Layer
> 15	Layer:        Requirements Engineering (between Sovereign and Execution)
> 16	Authority:    Reads from all BoKs; writes only to docs/bok/ and mcorch_nodes
> 17	Restrictions: NEVER writes code. NEVER modifies src/. NEVER touches supabase/functions/.
> 18	              NEVER deducts mcoCoins. Documentation only.
> 19	Language:     Thinking = English. Headings & labels = English.
> 20	              Narrative explanations to Sovereign = Português (Brasil).
> 21	```
> 22	
> 23	---
> 24	
> 25	## Input Schema
> 26	
> 27	```typescript
> 28	interface BokScribeInput {
> 29	  businessIdea:       string   // raw free-text description
> 30	  marketSegment:      'B2B' | 'B2C' | 'B2B2C'
> 31	  monetizationModel:  'subscription' | 'transaction' | 'hybrid'
> 32	  regulatoryProfile:  'LGPD' | 'GDPR' | 'financial' | 'healthcare' | 'none'
> 33	  integrationSurface: 'standalone' | 'extends-mcorch'
> 34	  projectSlug:        string   // derived: kebab-case, max 32 chars
> 35	}
> 36	```
> 37	
> 38	---
> 39	
> 40	## Output File Map
> 41	
> 42	```
> 43	docs/bok/<project-slug>/
> 44	├── 00-index.md              Phase 0  — Project manifest + file registry
> 45	├── 01-mrd.md                Phase 1  — Market Requirements Document (BABOK)
> 46	├── 02-brd.md                Phase 1  — Business Requirements Document (BABOK)
> 47	├── 03-prd.md                Phase 2  — Product Requirements Document (ProdBOK + CXBOK)
> 48	├── 04-frd.md                Phase 3  — Functional Requirements Document (SWEBOK)
> 49	├── 05-sdd.md                Phase 3  — System Design Document (SWEBOK + CISSP CBK)
> 50	├── 06-data-model.md         Phase 4  — Data Models (DMBOK + Supabase schema)
> 51	├── 07-process-flow.md       Phase 4  — Process Flows (BPM CBOK + n8n)
> 52	└── 08-quality-metrics.md    Phase 5  — Self-Optimization & Self-Healing (CMQ/OE BOK)
> 53	```
> 54	
> 55	---
> 56	
> 57	## Workflow Engine
> 58	
> 59	### Phase 0 — Project Bootstrap
> 60	
> 61	**BoK lens:** None (structural setup)  
> 62	**Template:** `templates/00-index.md`  
> 63	**Actions:**
> 64	1. Derive `projectSlug` from business idea (lowercase, hyphens, max 32 chars).
> 65	2. Create directory `docs/bok/<project-slug>/`.
> 66	3. Render `00-index.md` with all input metadata, today's date, version `v0.1`.
> 67	4. Record all planned output files with status `[ ] pending`.
> 68	
> 69	**Guardrails:**
> 70	- If directory already exists → check `00-index.md`; ask Sovereign before overwriting.
> 71	- Slug must match `^[a-z0-9-]{3,32}$`.
> 72	
> 73	---
> 74	
> 75	### Phase 1 — Market & Business Intelligence (BABOK v3)
> 76	
> 77	**BoK lens:** BABOK v3 — Business Analysis Body of Knowledge  
> 78	**BABOK knowledge areas applied:**
> 79	- *Business Analysis Planning & Monitoring* → defines stakeholders and elicitation plan
> 80	- *Elicitation & Collaboration* → extracts needs from raw idea
> 81	- *Requirements Life Cycle Mgmt* → traces market needs → business objectives
> 82	- *Strategy Analysis* → current state, desired state, gap analysis
> 83	- *Requirements Analysis & Design Definition* → MRD + BRD sections
> 84	
> 85	**Output A — `01-mrd.md` (Market Requirements Document):**
> 86	```
> 87	Sections to generate:
> 88	  1. Executive Summary
> 89	  2. Market Problem Statement (current state)
> 90	  3. Target Market Segments + TAM/SAM/SOM (estimated)
> 91	  4. Competitive Landscape (min 3 alternatives)
> 92	  5. Market Opportunity & Timing
> 93	  6. Key Market Requirements (MR-001..MR-NNN, priority: Critical/High/Medium/Low)
> 94	  7. Success Metrics (market-level KPIs)
> 95	  8. Regulatory & Compliance Context
> 96	  9. Traceability Matrix stub (MR → BR link)
> 97	```
> 98	
> 99	**Output B — `02-brd.md` (Business Requirements Document):**
> 100	```
> 101	Sections to generate:
> 102	  1. Executive Summary
> 103	  2. Business Objectives (SMART format, min 3)
> 104	  3. Stakeholder Register (Role, Interest, Influence, Communication)
> 105	  4. Business Requirements (BR-001..BR-NNN traced to MR-NNN)
> 106	  5. ROI Model (costs, revenue streams, payback period estimate)
> 107	  6. mcoCoins Economics (coin cost per operation, plan tier mapping)
> 108	  7. Constraints & Assumptions
> 109	  8. Business Risks (Risk ID, Description, Probability, Impact, Mitigation)
> 110	  9. Acceptance Criteria (business-level)
> 111	  10. Traceability Matrix (MR → BR → PR link stubs)
> 112	```
> 113	
> 114	**Transition check before Phase 2:**
> 115	- Every BR must trace to at least one MR.
> 116	- mcoCoins cost must be defined if feature uses AI generation.
> 117	
> 118	---
> 119	
> 120	### Phase 2 — Product Definition (ProdBOK + CXBOK)
> 121	
> 122	**BoK lens:** ProdBOK (Product Management Body of Knowledge) + CXBOK (Customer Experience)  
> 123	**ProdBOK areas applied:**
> 124	- *Product Vision & Strategy* → product goal and positioning
> 125	- *Roadmap Planning* → release phasing (MVP → v1 → v2)
> 126	- *Feature Definition & Prioritization* → MoSCoW method
> 127	- *Metrics & Analytics* → product KPIs
> 128	
> 129	**CXBOK areas applied:**
> 130	- *Customer Understanding* → persona construction
> 131	- *Experience Design* → journey mapping, touchpoint inventory
> 132	- *Luxury UX Standards* → MCORCH aesthetic rules (dark mesh, neon accents, micro-animations)
> 133	
> 134	**Output — `03-prd.md` (Product Requirements Document):**
> 135	```
> 136	Sections to generate:
> 137	  1. Product Vision Statement (one sentence)
> 138	  2. User Personas (min 2: primary + secondary)
> 139	     - Name, Role, Goals, Frustrations, Tech-savviness, MCORCH usage pattern
> 140	  3. User Journey Maps (per persona, happy path + 2 edge cases)
> 141	  4. Feature Inventory (MoSCoW: Must / Should / Could / Won't)
> 142	     - Feature ID: PR-001..PR-NNN
> 143	     - Description, Persona served, BR traced, Effort (S/M/L/XL), mcoCoins cost
> 144	  5. Release Phasing
> 145	     - MVP scope (Must-haves only)
> 146	     - v1.0 scope (Must + prioritized Shoulds)
> 147	     - Future scope (Coulds)
> 148	  6. Luxury UX Specifications
> 149	     - Color palette constraints (dark mesh: #0A0A0F, neon violet: #7C3AED)
> 150	     - Animation guidelines (Framer Motion tokens)
> 151	     - Interaction patterns (glass morphism cards, particle effects)
> 152	     - Accessibility requirements (WCAG 2.1 AA minimum)
> 153	  7. Acceptance Criteria (product-level, Gherkin format: Given/When/Then)
> 154	  8. Traceability Matrix (MR → BR → PR link)
> 155	```
> 156	
> 157	**Transition check before Phase 3:**
> 158	- Every PR must trace to at least one BR.
> 159	- MVP scope must be achievable without new Edge Functions (or explicitly note which new ones are needed).
> 160	
> 161	---
> 162	
> 163	### Phase 3 — Technical Specification (SWEBOK v4 + CISSP CBK 2024)
> 164	
> 165	**BoK lens A — SWEBOK v4:**
> 166	- *Software Requirements* → formal FR elicitation from PRD
> 167	- *Software Design* → architectural decisions, component decomposition
> 168	- *Software Construction* → Harness Engineering constraints
> 169	- *Software Testing* → test strategy per requirement
> 170	
> 171	**BoK lens B — CISSP CBK 2024:**
> 172	- *Security & Risk Management* → threat model (STRIDE)
> 173	- *Identity & Access Management* → RLS policies, JWT validation
> 174	- *Software Development Security* → secure coding constraints
> 175	- *Cryptography* → data-at-rest and in-transit requirements
> 176	
> 177	**Output A — `04-frd.md` (Functional Requirements Document):**
> 178	```
> 179	Sections to generate:
> 180	  1. Scope Statement
> 181	  2. Functional Requirements (FR-001..FR-NNN)
> 182	     - ID, Title, Description, Priority, PR traced, Acceptance Test ID
> 183	     - Category: UI / Hook / Edge Function / DB / Cron
> 184	  3. Non-Functional Requirements (NFR-001..NFR-NNN)
> 185	     - Performance, Scalability, Availability, Maintainability
> 186	  4. Interface Requirements
> 187	     - UI contracts (component → hook → Edge Function)
> 188	     - External API contracts (input/output shape, error codes)
> 189	  5. Data Requirements (input validation rules, data types)
> 190	  6. Test Strategy matrix (Unit / Integration / E2E per FR)
> 191	  7. Traceability Matrix (PR → FR link)
> 192	```
> 193	
> 194	**Output B — `05-sdd.md` (System Design Document):**
> 195	```
> 196	Sections to generate:
> 197	  1. Architecture Overview (text diagram, Harness Engineering layer map)
> 198	  2. Component Catalog
> 199	     - New hooks (src/hooks/)
> 200	     - New components (display-only, src/components/)
> 201	     - New Edge Functions (supabase/functions/)
> 202	     - New Zustand store slices (if needed)
> 203	     - New DB tables / columns (migration stubs)
> 204	  3. Data Flow Diagrams (per major use case)
> 205	  4. API Contract Definitions (Edge Function signatures)
> 206	     - Method, Path, Auth, Request body, Response body, Error codes
> 207	     - mcoCoins deduction point (RPC call location)
> 208	  5. Security Design
> 209	     - Threat model (STRIDE per component)
> 210	     - RLS policy definitions
> 211	     - JWT validation points
> 212	     - Secrets inventory (which vault keys are needed)
> 213	  6. Infrastructure Touchpoints
> 214	     - Docker Sovereign Mesh dependencies
> 215	     - ChromaDB usage (if vector search needed)
> 216	     - Watchdog telemetry events (new infra_health_logs event types)
> 217	  7. Migration Stubs (table name, columns, RLS template, HNSW index if embeddings)
> 218	  8. Open Technical Decisions (OTD-001..OTD-NNN, each with options + recommendation)
> 219	```
> 220	
> 221	**Security guardrails enforced automatically:**
> 222	- Every Edge Function must have JWT validation stub.
> 223	- Every new table must have `RLS enabled; default deny` noted in migration stub.
> 224	- `mcoCoins` deduction MUST route through `deduct_mco_coins` RPC — never client-side.
> 225	- No secret key referenced in FRD/SDD may appear in `src/` paths.
> 226	
> 227	**Transition check before Phase 4:**
> 228	- Every FR must trace to at least one PR.
> 229	- Every Edge Function in SDD must list its secret dependencies.
> 230	- Threat model must have at least one mitigation per identified threat.
> 231	
> 232	---
> 233	
> 234	### Phase 4 — Data & Process Engineering (DMBOK v2 + BPM CBOK v4)
> 235	
> 236	**BoK lens A — DMBOK v2:**
> 237	- *Data Modeling & Design* → conceptual → logical → physical schema
> 238	- *Data Quality* → validation rules, nullability constraints
> 239	- *Reference & Master Data* → system nodes in mcorch_nodes
> 240	- *Data Warehousing & BI* → analytics views if applicable
> 241	
> 242	**BoK lens B — BPM CBOK v4:**
> 243	- *Process Modeling* → BPMN-lite notation in markdown
> 244	- *Process Analysis* → bottlenecks, automation opportunities
> 245	- *Process Design* → n8n workflow blueprint
> 246	- *Process Performance Mgmt* → SLA per process step
> 247	
> 248	**Output A — `06-data-model.md` (Data & Knowledge Model):**
> 249	```
> 250	Sections to generate:
> 251	  1. Conceptual Data Model (entity list + relationships, text ERD)
> 252	  2. Logical Data Model (per table: columns, types, constraints, FK references)
> 253	  3. Supabase Physical Schema Stubs
> 254	     - CREATE TABLE skeleton (copy into migration file)
> 255	     - RLS policy shells (default deny + per-role)
> 256	     - Index definitions (HNSW for embeddings, B-tree for FKs)
> 257	  4. GraphRAG Knowledge Nodes
> 258	     - Node types this feature introduces into mcorch_nodes
> 259	     - Edge types this feature introduces into mcorch_edges
> 260	     - Embedding fields (which text columns feed embed-mcorch-node)
> 261	     - stability_score initial value + FSRS-6 decay parameters
> 262	  5. Tenant Isolation Map (user_id + project_id scope per table)
> 263	  6. Data Quality Rules (per column: allowed values, validation regex, null policy)
> 264	  7. Retention & Archival Policy
> 265	```
> 266	
> 267	**Output B — `07-process-flow.md` (Process & Automation Blueprint):**
> 268	```
> 269	Sections to generate:
> 270	  1. Process Inventory (list of all automated processes this feature introduces)
> 271	  2. BPMN-lite Process Maps (per major process)
> 272	     - Start event, Tasks (human/automated), Gateways, End events
> 273	     - Swimlanes: User | Frontend Hook | Edge Function | External API | DB
> 274	  3. n8n Workflow Blueprints (per automated process)
> 275	     - Trigger (webhook / cron / event), Node sequence, Error branches
> 276	     - Data mapping: input fields → output fields
> 277	  4. Orchestration Integration Points
> 278	     - Steps within orchestrate-content pipeline (if applicable)
> 279	     - New pipeline step ID and position
> 280	     - mcoCoins deduction trigger point
> 281	  5. Error Handling & Retry Strategy (per process step)
> 282	  6. SLA Definitions (expected duration per step, timeout thresholds)
> 283	  7. Cron Jobs (schedule, idempotency key, failure alerting)
> 284	```
> 285	
> 286	**Transition check before Phase 5:**
> 287	- Every table in data model must appear in at least one process flow.
> 288	- Every n8n workflow must define its error branch.
> 289	- GraphRAG node insertion must be present in at least one process.
> 290	
> 291	---
> 292	
> 293	### Phase 5 — Quality & Autonomic Engineering (CMQ/OE BOK)
> 294	
> 295	**BoK lens:** CMQ/OE BOK (Certified Manager of Quality / Organizational Excellence)  
> 296	**Areas applied:**
> 297	- *Process Management* → control charts, process capability (Cp/Cpk targets)
> 298	- *Quality Tools* → FMEA for critical paths
> 299	- *Customer-Focused Org* → NPS/CSAT hooks
> 300	- *Organizational Excellence* → self-optimization loops
> 301	- *Continuous Improvement* → PDCA cycles for autonomic self-healing
> 302	
> 303	**Output — `08-quality-metrics.md` (Self-Optimization & Self-Healing Specification):**
> 304	```
> 305	Sections to generate:
> 306	  1. Quality Objectives (aligned to business objectives in BRD)
> 307	  2. KPI Dashboard Definition
> 308	     - KPI ID, Name, Formula, Target, Threshold (warn/critical), Data source
> 309	     - Supabase table/view that stores the metric
> 310	  3. FMEA Table (per critical FR)
> 311	     - Function, Failure Mode, Effect, Severity (1-10), Occurrence (1-10),
> 312	       Detection (1-10), RPN = S×O×D, Recommended Action
> 313	  4. Self-Optimization Loops
> 314	     - Trigger condition (metric threshold crossed)
> 315	     - Autonomous response (what the system does without human intervention)
> 316	     - Escalation path (when human decision is required)
> 317	  5. Self-Healing Specifications
> 318	     - Watchdog telemetry event types (new rows for infra_health_logs)
> 319	     - Auto-recovery script stubs (bash / Edge Function)
> 320	     - mega-brain-daemon integration points
> 321	  6. SLA / SLO / SLI Definitions
> 322	     - Service, SLI metric, SLO target (e.g. 99.5% uptime/month), SLA consequence
> 323	  7. PDCA Improvement Cadence
> 324	     - Review frequency, metrics owner, improvement backlog location
> 325	  8. Observability Checklist
> 326	     - Logging events (what, where, level)
> 327	     - Alerting rules (condition → channel → escalation)
> 328	     - Distributed tracing touchpoints
> 329	```
> 330	
> 331	---
> 332	
> 333	### Phase 6 — Cross-Document Traceability Validation
> 334	
> 335	**Actions (automated consistency check before writing `00-index.md` final status):**
> 336	
> 337	```
> 338	1. Build traceability chain:
> 339	   MR-NNN → BR-NNN → PR-NNN → FR-NNN → (DB table | Edge Function | Process)
> 340	
> 341	2. Assert:
> 342	   - No orphaned requirements (every ID appears in at least one downstream doc).
> 343	   - No undocumented Edge Functions (every function in SDD has JWT + secret listed).
> 344	   - No tables without RLS (every CREATE TABLE stub has RLS block).
> 345	   - mcoCoins cost defined for every AI-powered FR.
> 346	   - Every FMEA item with RPN > 100 has a recommended action.
> 347	
> 348	3. If any assertion fails:
> 349	   - List all failures with their document + section reference.
> 350	   - Ask Sovereign to resolve before proceeding to Phase 7.
> 351	   - Do NOT proceed to Phase 7 with unresolved critical failures.
> 352	```
> 353	
> 354	---
> 355	
> 356	### Phase 7 — Knowledge Mesh Injection
> 357	
> 358	> **Canonical pattern (sealed 2026-05-26, Sovereign directive):** every BoK seal MUST persist
> 359	> the documentation_suite node via a dedicated Bun-native seed script following the precedent
> 360	> `scripts/seed-openclaw-bok-seal.ts` (and its sibling `seed-gamificacao-nodes-bok-seal.ts`).
> 361	> Inline REST `curl` or one-off dashboard inserts are NOT allowed — the script form preserves
> 362	> reproducibility, version control, and material proof of the operation.
> 363	
> 364	**Required actions:**
> 365	
> 366	1. **Construct the payload** as a fully-typed object — placeholder example:
> 367	
> 368	```json
> 369	{
> 370	  "node_type": "documentation_suite",
> 371	  "name": "bok-scribe-seal-<projectSlug>-v1",
> 372	  "title": "<projectSlug> BoK Documentation Suite v1",
> 373	  "content": "<one-paragraph synthesis: idea, market, architecture, ID space summary, motivating context>",
> 374	  "tags": ["bok-scribe", "<projectSlug>", "<marketSegment>", ...domain-specific],
> 375	  "stability_score": 0.85,
> 376	  "revenue_impact": <estimated from BRD ROI section — 0 for internal enablers; non-zero only when direct revenue is documented>,
> 377	  "metadata": {
> 378	    "bok_version": "1.0.0",
> 379	    "documents": ["00-index","01-mrd","02-brd","03-prd","04-frd","05-sdd","06-data-model","07-process-flow","08-quality-metrics"],
> 380	    "document_lines": { ... per-file LOC + total },
> 381	    "phase_completed": "Phase 7",
> 382	    "traceability_validated": true,
> 383	    "traceability_orphans": 0,
> 384	    "id_space": { "MR": "MR-XX-001..NNN", "BR": "...", ... },
> 385	    "fmea_high_rpn_count": <int>,
> 386	    "fmea_high_rpn_items": ["FMEA-XX-NNN (RPN <value>)", ...],
> 387	    "new_migrations": <int>,
> 388	    "new_edge_functions": <int>,
> 389	    "integration_surface": "<standalone|extends-mcorch>",
> 390	    "regulatory_profile": "<LGPD|GDPR|financial|healthcare|none>",
> 391	    "monetization": "<direct|indirect|internal-enabler-zero-coin>",
> 392	    "derives_from_seal": "bok-scribe-seal-<parent-slug>-v1",
> 393	    "depends_on_sop": "<path to operational SOP if applicable>",
> 394	    "motivating_incident": "<incident reference if BoK was triggered by an incident>"
> 395	  }
> 396	}
> 397	```
> 398	
> 399	2. **Author a dedicated seed script** at `scripts/seed-<projectSlug>-bok-seal.ts` mirroring
> 400	   `scripts/seed-openclaw-bok-seal.ts` 1:1 in structure. The script MUST:
> 401	   - Use `@supabase/supabase-js` with `SUPABASE_SERVICE_ROLE_KEY` from `.env` (never hardcode).
> 402	   - INSERT the payload into `mcorch_nodes` using `.select('id, name').single()` for material proof.
> 403	   - INSERT a `DERIVES_FROM` edge in `mcorch_edges` pointing to the most semantically-related
> 404	     parent seal (typically the previous BoK seal in the topic family — discover via
> 405	     `SELECT id FROM mcorch_nodes WHERE name = 'bok-scribe-seal-<parent-slug>-v1'`).
> 406	   - Print the returned UUIDs to stdout for the agent to cite as material proof.
> 407	   - Be idempotent: if the seal already exists (UNIQUE name violation), log and exit 0 cleanly.
> 408	
> 409	3. **Execute the script** under the project venv:
> 410	   ```bash
> 411	   bun run scripts/seed-<projectSlug>-bok-seal.ts
> 412	   ```
> 413	   Capture the returned UUID + edge UUID. Confirm via REST:
> 414	   ```bash
> 415	   curl -s "$SUPABASE_URL/rest/v1/mcorch_nodes?id=eq.<uuid>&select=embedding" \
> 416	     -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
> 417	     -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"
> 418	   # Expected: embedding NOT NULL (auto-fired via trg_mcorch_embed_on_insert pg_net)
> 419	   ```
> 420	
> 421	4. **Cite the material proof** in the `/handoff` seal:
> 422	   - Documentation suite UUID
> 423	   - DERIVES_FROM edge UUID
> 424	   - Embedding confirmation timestamp
> 425	
> 426	**Note:** The BoK Scribe Agent itself does NOT directly invoke Supabase via in-conversation
> 427	REST calls — it produces the seed script + payload, and the Sovereign (or agent executing on
> 428	behalf of the Sovereign with explicit approval) runs the script. The script form preserves
> 429	the audit trail of "what was inserted, when, by which version of which code."
> 430	
> 431	**Precedent inventory (mirror sources, in order of recency):**
> 432	- `scripts/seed-e2e-user-zero-bok-seal.ts` (this BoK — 2026-05-26)
> 433	- `scripts/seed-openclaw-bok-seal.ts` (openclaw — 2026-05-19)
> 434	- `scripts/seed-gamificacao-nodes-bok-seal.ts` (gamificacao-nodes — 2026-05-18)
> 435	- (older seals predate this script pattern and were inserted via inline REST — grandfathered)
> 436	
> 437	---
> 438	
> 439	## Harness Engineering Constraints (non-negotiable)
> 440	
> 441	These rules apply to every document the agent produces:
> 442	
> 443	| Constraint | Rule |
> 444	|------------|------|
> 445	| Code separation | FRD/SDD describe WHAT and WHY. HOW belongs in code, not in docs. |
> 446	| Hook-first | Every UI feature must describe its backing hook before its component. |
> 447	| No client secrets | SDD never lists secret values, only key names from the vault. |
> 448	| Atomic billing | mcoCoins deduction always routes through `deduct_mco_coins` RPC. |
> 449	| RLS by default | Every new table starts with `ALTER TABLE x ENABLE ROW LEVEL SECURITY`. |
> 450	| Embed on insert | Every new node-type table must have embed-mcorch-node trigger noted. |
> 451	| Tenant isolation | Every table must document its `user_id + project_id` scoping. |
> 452	
> 453	---
> 454	
> 455	## Error & Edge Case Handling
> 456	
> 457	| Situation | Agent Response |
> 458	|-----------|----------------|
> 459	| Business idea is too vague | Ask 3 clarifying questions before Phase 1. |
> 460	| Existing docs/bok/<slug>/ detected | Show index, ask: overwrite / extend / cancel. |
> 461	| Phase transition check fails | List failures, stop, ask Sovereign to resolve. |
> 462	| Conflicting BoK recommendations | Note the conflict in an `[OTD]` block; present both options. |
> 463	| Regulatory profile = financial/healthcare | Elevate all CISSP CBK sections; add dedicated compliance checklist. |
> 464	| Feature extends existing MCORCH feature | Cross-reference existing ADRs from `.claude/context/architecture-decisions.md`. |
> 465	
> 466	---
> 467	
> 468	## Document Style Guide
> 469	
> 470	- **Headings:** `#` for document title, `##` for major sections, `###` for subsections.
> 471	- **IDs:** Always prefix (MR-, BR-, PR-, FR-, NFR-, OTD-) and zero-pad to 3 digits.
> 472	- **Tables:** Use markdown tables with aligned columns; include a header row always.
> 473	- **Code blocks:** Use fenced blocks with language identifier (`sql`, `typescript`, `json`).
> 474	- **Status badges:** `[ ] pending` / `[x] complete` / `[!] blocked` in index file.
> 475	- **Cross-references:** Link within suite as `[BR-001](../02-brd.md#br-001)`.
> 476	- **Version:** Every file footer includes `_Generated by MCORCH BoK Scribe Agent v1.0.0_`.
> 477	
> ```

## 🤖 Claude *(02:42:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"\u2500\u2500\u2500 templates \u2500\u2500\u2500\"; ls -la .claude/agents/bok-scribe/templates/ 2>/dev/null\necho \"\u2500\u2500\u2500 existing constellation-v2 dir? \u2500\u2500\u2500\"; ls -la docs/bok/constellation-v2/ 2>/dev/null || echo \"(n\u00e3o existe \u2014 vou criar)\"\necho \"\u2500\u2500\u2500 existing mcorch-constellation BoK (a ser superada) \u2500\u2500\u2500\"; ls docs/bok/mcorch-constellation/ 2>/dev/null\necho \"\u2500\u2500\u2500 template line counts (escopo) \u2500\u2500\u2500\"; wc -l .claude/agents/bok-scribe/templates/* 2>/dev/null",
  "description": "Load bok-scribe templates + check existing dirs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── templates ───
> total 68
> drwxrwxr-x 2 ubuntu ubuntu 4096 May  6 13:37 .
> drwxrwxr-x 3 ubuntu ubuntu 4096 May  6 13:37 ..
> -rw-rw-r-- 1 ubuntu ubuntu 2286 May  6 13:37 00-index.md
> -rw-rw-r-- 1 ubuntu ubuntu 3163 May  6 13:37 01-mrd.md
> -rw-rw-r-- 1 ubuntu ubuntu 3715 May  6 13:37 02-brd.md
> -rw-rw-r-- 1 ubuntu ubuntu 5073 May  6 13:37 03-prd.md
> -rw-rw-r-- 1 ubuntu ubuntu 3632 May  6 13:37 04-frd.md
> -rw-rw-r-- 1 ubuntu ubuntu 8660 May  6 13:37 05-sdd.md
> -rw-rw-r-- 1 ubuntu ubuntu 5880 May  6 13:37 06-data-model.md
> -rw-rw-r-- 1 ubuntu ubuntu 5730 May  6 13:37 07-process-flow.md
> -rw-rw-r-- 1 ubuntu ubuntu 7550 May  6 13:37 08-quality-metrics.md
> ─── existing constellation-v2 dir? ───
> (não existe — vou criar)
> ─── existing mcorch-constellation BoK (a ser superada) ───
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> bok-agents-system--mcorch-constellation.md
> revenue-flywheel.md
> roadmap-v1.md
> ─── template line counts (escopo) ───
>    74 .claude/agents/bok-scribe/templates/00-index.md
>   109 .claude/agents/bok-scribe/templates/01-mrd.md
>   122 .claude/agents/bok-scribe/templates/02-brd.md
>   177 .claude/agents/bok-scribe/templates/03-prd.md
>   121 .claude/agents/bok-scribe/templates/04-frd.md
>   219 .claude/agents/bok-scribe/templates/05-sdd.md
>   169 .claude/agents/bok-scribe/templates/06-data-model.md
>   162 .claude/agents/bok-scribe/templates/07-process-flow.md
>   161 .claude/agents/bok-scribe/templates/08-quality-metrics.md
>  1314 total
> ```

## 🤖 Claude *(02:42:27)*


## 🤖 Claude *(02:42:28)*

Framework carregado. Vou ler os 9 templates canônicos (o `00-index.md` serve de tracker de progresso com badges `[ ]/[x]`, então dispenso task list externa) e então autorar a suíte na sequência estrita de fases.

## 🤖 Claude *(02:42:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/00-index.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BoK Documentation Suite — {{PROJECT_SLUG}}
> 2	
> 3	**Generated:** {{DATE}}  
> 4	**Version:** v0.1  
> 5	**Agent:** MCORCH BoK Scribe Agent v1.0.0  
> 6	**Sovereign:** {{SOVEREIGN_ID}}
> 7	
> 8	---
> 9	
> 10	## Project Metadata
> 11	
> 12	| Field | Value |
> 13	|-------|-------|
> 14	| Business Idea | {{BUSINESS_IDEA}} |
> 15	| Market Segment | {{MARKET_SEGMENT}} |
> 16	| Monetization Model | {{MONETIZATION_MODEL}} |
> 17	| Regulatory Profile | {{REGULATORY_PROFILE}} |
> 18	| Integration Surface | {{INTEGRATION_SURFACE}} |
> 19	| Project Slug | `{{PROJECT_SLUG}}` |
> 20	
> 21	---
> 22	
> 23	## Document Registry
> 24	
> 25	| # | File | Document | BoK Applied | Status |
> 26	|---|------|----------|-------------|--------|
> 27	| 0 | `00-index.md` | Project Manifest | — | [x] complete |
> 28	| 1 | `01-mrd.md` | Market Requirements Document | BABOK v3 | [ ] pending |
> 29	| 2 | `02-brd.md` | Business Requirements Document | BABOK v3 | [ ] pending |
> 30	| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [ ] pending |
> 31	| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [ ] pending |
> 32	| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [ ] pending |
> 33	| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [ ] pending |
> 34	| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [ ] pending |
> 35	| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [ ] pending |
> 36	
> 37	---
> 38	
> 39	## Traceability Chain (populated as documents are generated)
> 40	
> 41	```
> 42	MR-NNN
> 43	  └── BR-NNN
> 44	        └── PR-NNN
> 45	              └── FR-NNN
> 46	                    └── [DB table | Edge Function | n8n Process]
> 47	```
> 48	
> 49	---
> 50	
> 51	## Phase Completion Log
> 52	
> 53	| Phase | Name | Completed | Notes |
> 54	|-------|------|-----------|-------|
> 55	| 0 | Project Bootstrap | {{DATE}} | — |
> 56	| 1 | Market & Business Intelligence | [ ] | — |
> 57	| 2 | Product Definition | [ ] | — |
> 58	| 3 | Technical Specification | [ ] | — |
> 59	| 4 | Data & Process Engineering | [ ] | — |
> 60	| 5 | Quality & Autonomic Engineering | [ ] | — |
> 61	| 6 | Traceability Validation | [ ] | — |
> 62	| 7 | Knowledge Mesh Injection | [ ] | — |
> 63	
> 64	---
> 65	
> 66	## Open Technical Decisions
> 67	
> 68	| OTD ID | Description | Options | Recommendation | Status |
> 69	|--------|-------------|---------|----------------|--------|
> 70	| — | None yet | — | — | — |
> 71	
> 72	---
> 73	
> 74	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 75	
> ```

## 🤖 Claude *(02:42:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/01-mrd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MRD — Market Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Executive Summary
> 11	
> 12	> _One paragraph: what market problem exists, why now, and what this solution uniquely addresses._
> 13	
> 14	{{EXECUTIVE_SUMMARY}}
> 15	
> 16	---
> 17	
> 18	## 2. Market Problem Statement
> 19	
> 20	### 2.1 Current State
> 21	> _Describe the painful status quo for the target user._
> 22	
> 23	{{CURRENT_STATE}}
> 24	
> 25	### 2.2 Root Cause Analysis
> 26	> _Why does this problem persist? (technology gap, process gap, market gap)_
> 27	
> 28	{{ROOT_CAUSE}}
> 29	
> 30	### 2.3 Desired State
> 31	> _What does success look like from the market's perspective?_
> 32	
> 33	{{DESIRED_STATE}}
> 34	
> 35	---
> 36	
> 37	## 3. Target Market Segments
> 38	
> 39	| Segment | Description | Size Estimate | Urgency | Accessibility |
> 40	|---------|-------------|---------------|---------|---------------|
> 41	| Primary | {{PRIMARY_SEGMENT}} | {{TAM_PRIMARY}} | High | {{ACCESS_PRIMARY}} |
> 42	| Secondary | {{SECONDARY_SEGMENT}} | {{TAM_SECONDARY}} | Medium | {{ACCESS_SECONDARY}} |
> 43	
> 44	### 3.1 TAM / SAM / SOM
> 45	
> 46	| Metric | Value | Basis |
> 47	|--------|-------|-------|
> 48	| TAM (Total Addressable Market) | {{TAM}} | {{TAM_BASIS}} |
> 49	| SAM (Serviceable Addressable Market) | {{SAM}} | {{SAM_BASIS}} |
> 50	| SOM (Serviceable Obtainable Market) | {{SOM}} | {{SOM_BASIS}} |
> 51	
> 52	---
> 53	
> 54	## 4. Competitive Landscape
> 55	
> 56	| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |
> 57	|------------|-------------|-----------|------------|---------------------|
> 58	| {{COMP_1}} | {{POS_1}} | {{STR_1}} | {{WEAK_1}} | {{DIFF_1}} |
> 59	| {{COMP_2}} | {{POS_2}} | {{STR_2}} | {{WEAK_2}} | {{DIFF_2}} |
> 60	| {{COMP_3}} | {{POS_3}} | {{STR_3}} | {{WEAK_3}} | {{DIFF_3}} |
> 61	
> 62	---
> 63	
> 64	## 5. Market Opportunity & Timing
> 65	
> 66	> _Why is this the right moment? (regulatory shifts, technology maturity, behavioral trends)_
> 67	
> 68	{{MARKET_TIMING}}
> 69	
> 70	---
> 71	
> 72	## 6. Market Requirements
> 73	
> 74	> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**
> 75	
> 76	| ID | Market Requirement | Priority | Rationale | Source |
> 77	|----|-------------------|----------|-----------|--------|
> 78	| MR-001 | {{MR_001_DESC}} | Critical | {{MR_001_RATIONALE}} | {{MR_001_SOURCE}} |
> 79	| MR-002 | {{MR_002_DESC}} | High | {{MR_002_RATIONALE}} | {{MR_002_SOURCE}} |
> 80	
> 81	---
> 82	
> 83	## 7. Success Metrics (Market-Level KPIs)
> 84	
> 85	| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |
> 86	|-----|-----------|------------------|-------------------|-------------|
> 87	| Market Penetration | % of SAM reached | {{KPI_1_6M}} | {{KPI_1_12M}} | {{KPI_1_MEAS}} |
> 88	| NPS | Net Promoter Score | {{KPI_2_6M}} | {{KPI_2_12M}} | {{KPI_2_MEAS}} |
> 89	
> 90	---
> 91	
> 92	## 8. Regulatory & Compliance Context
> 93	
> 94	| Regulation | Applicability | Key Constraint | Compliance Owner |
> 95	|------------|---------------|----------------|-----------------|
> 96	| LGPD | {{LGPD_APPLICABLE}} | {{LGPD_CONSTRAINT}} | Engineering |
> 97	| {{OTHER_REG}} | {{OTHER_APPLICABLE}} | {{OTHER_CONSTRAINT}} | {{OTHER_OWNER}} |
> 98	
> 99	---
> 100	
> 101	## 9. Traceability Matrix Stub
> 102	
> 103	| MR ID | → BR ID | Rationale |
> 104	|-------|---------|-----------|
> 105	| MR-001 | BR-??? | _to be linked in BRD_ |
> 106	
> 107	---
> 108	
> 109	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 110	
> ```

## 🤖 Claude *(02:42:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/02-brd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BRD — Business Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Executive Summary
> 11	
> 12	{{EXECUTIVE_SUMMARY}}
> 13	
> 14	---
> 15	
> 16	## 2. Business Objectives (SMART)
> 17	
> 18	| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |
> 19	|----|-----------|----------|------------|------------|----------|------------|
> 20	| BO-001 | {{BO_001}} | {{BO_001_S}} | {{BO_001_M}} | {{BO_001_A}} | {{BO_001_R}} | {{BO_001_T}} |
> 21	| BO-002 | {{BO_002}} | {{BO_002_S}} | {{BO_002_M}} | {{BO_002_A}} | {{BO_002_R}} | {{BO_002_T}} |
> 22	| BO-003 | {{BO_003}} | {{BO_003_S}} | {{BO_003_M}} | {{BO_003_A}} | {{BO_003_R}} | {{BO_003_T}} |
> 23	
> 24	---
> 25	
> 26	## 3. Stakeholder Register
> 27	
> 28	| ID | Role | Interest | Influence | Communication Cadence | Contact |
> 29	|----|------|----------|-----------|----------------------|---------|
> 30	| SH-001 | Sovereign / Maestro | High | High | Continuous | {{SOVEREIGN}} |
> 31	| SH-002 | End User (Primary) | High | Medium | Monthly NPS survey | {{USER_CONTACT}} |
> 32	| SH-003 | {{STAKEHOLDER_3}} | {{INTEREST_3}} | {{INFLUENCE_3}} | {{CADENCE_3}} | {{CONTACT_3}} |
> 33	
> 34	---
> 35	
> 36	## 4. Business Requirements
> 37	
> 38	> Each BR traces to at least one MR. mcoCoins cost defined if AI-powered.
> 39	
> 40	| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |
> 41	|----|-------------|-----------|----------|---------------|---------------------|
> 42	| BR-001 | {{BR_001_DESC}} | MR-001 | Critical | {{COINS_001}} | {{AC_001}} |
> 43	| BR-002 | {{BR_002_DESC}} | MR-001 | High | {{COINS_002}} | {{AC_002}} |
> 44	
> 45	---
> 46	
> 47	## 5. ROI Model
> 48	
> 49	### 5.1 Cost Estimates
> 50	
> 51	| Cost Item | Type | Monthly Estimate | Annual Estimate |
> 52	|-----------|------|-----------------|----------------|
> 53	| Infrastructure (Supabase, Docker) | OpEx | {{INFRA_MONTHLY}} | {{INFRA_ANNUAL}} |
> 54	| AI API calls (OpenRouter) | Variable | {{AI_MONTHLY}} | {{AI_ANNUAL}} |
> 55	| Development (initial) | CapEx | — | {{DEV_COST}} |
> 56	
> 57	### 5.2 Revenue Streams
> 58	
> 59	| Stream | Model | Monthly Potential | Notes |
> 60	|--------|-------|-----------------|-------|
> 61	| {{STREAM_1}} | {{MODEL_1}} | {{REV_1_MONTHLY}} | {{NOTES_1}} |
> 62	| {{STREAM_2}} | {{MODEL_2}} | {{REV_2_MONTHLY}} | {{NOTES_2}} |
> 63	
> 64	### 5.3 Payback Analysis
> 65	
> 66	| Metric | Value |
> 67	|--------|-------|
> 68	| Break-even (months) | {{BREAK_EVEN}} |
> 69	| 12-month ROI | {{ROI_12M}} |
> 70	| IRR (estimated) | {{IRR}} |
> 71	
> 72	---
> 73	
> 74	## 6. mcoCoins Economics
> 75	
> 76	| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |
> 77	|-----------|-----------|-------------------|-----------------------|----------------------|
> 78	| {{OP_1}} | {{COINS_OP_1}} | Starter(500) / Pro(2000) / Ent(10k) | {{VOL_1}} | {{REV_MCO_1}} |
> 79	
> 80	---
> 81	
> 82	## 7. Constraints & Assumptions
> 83	
> 84	### Constraints
> 85	- {{CONSTRAINT_1}}
> 86	- {{CONSTRAINT_2}}
> 87	
> 88	### Assumptions
> 89	- {{ASSUMPTION_1}}
> 90	- {{ASSUMPTION_2}}
> 91	
> 92	---
> 93	
> 94	## 8. Business Risk Register
> 95	
> 96	| Risk ID | Description | Probability | Impact | RPN | Mitigation |
> 97	|---------|-------------|-------------|--------|-----|------------|
> 98	| BR-RISK-001 | {{RISK_001}} | {{PROB_001}} | {{IMPACT_001}} | {{RPN_001}} | {{MIT_001}} |
> 99	| BR-RISK-002 | {{RISK_002}} | {{PROB_002}} | {{IMPACT_002}} | {{RPN_002}} | {{MIT_002}} |
> 100	
> 101	> Probability & Impact: 1=Low, 5=High. RPN = Probability × Impact.
> 102	
> 103	---
> 104	
> 105	## 9. Business Acceptance Criteria
> 106	
> 107	| ID | Criterion | Verification Method |
> 108	|----|-----------|-------------------|
> 109	| BAC-001 | {{BAC_001}} | {{BAC_001_VERIFY}} |
> 110	| BAC-002 | {{BAC_002}} | {{BAC_002_VERIFY}} |
> 111	
> 112	---
> 113	
> 114	## 10. Traceability Matrix
> 115	
> 116	| MR ID | BR ID | PR ID (stub) |
> 117	|-------|-------|--------------|
> 118	| MR-001 | BR-001, BR-002 | _to be linked in PRD_ |
> 119	
> 120	---
> 121	
> 122	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 123	
> ```

## 🤖 Claude *(02:42:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/03-prd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# PRD — Product Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** ProdBOK + CXBOK  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Product Vision Statement
> 11	
> 12	> _One sentence. Format: "For [target user] who [need], [Product Name] is a [category] that [key benefit]. Unlike [alternative], our product [differentiator]."_
> 13	
> 14	{{PRODUCT_VISION}}
> 15	
> 16	---
> 17	
> 18	## 2. User Personas
> 19	
> 20	### Persona 1 — {{PERSONA_1_NAME}} (Primary)
> 21	
> 22	| Attribute | Detail |
> 23	|-----------|--------|
> 24	| Role | {{P1_ROLE}} |
> 25	| Goals | {{P1_GOALS}} |
> 26	| Frustrations | {{P1_FRUSTRATIONS}} |
> 27	| Tech-savviness | {{P1_TECH}} (1=novice, 5=expert) |
> 28	| MCORCH usage pattern | {{P1_MCORCH_PATTERN}} |
> 29	| Quote | _"{{P1_QUOTE}}"_ |
> 30	
> 31	### Persona 2 — {{PERSONA_2_NAME}} (Secondary)
> 32	
> 33	| Attribute | Detail |
> 34	|-----------|--------|
> 35	| Role | {{P2_ROLE}} |
> 36	| Goals | {{P2_GOALS}} |
> 37	| Frustrations | {{P2_FRUSTRATIONS}} |
> 38	| Tech-savviness | {{P2_TECH}} |
> 39	| MCORCH usage pattern | {{P2_MCORCH_PATTERN}} |
> 40	| Quote | _"{{P2_QUOTE}}"_ |
> 41	
> 42	---
> 43	
> 44	## 3. User Journey Maps
> 45	
> 46	### Journey: {{JOURNEY_1_NAME}} ({{PERSONA_1_NAME}}, Happy Path)
> 47	
> 48	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 49	|-------|--------|-----------|---------|-------------|
> 50	| Awareness | {{STAGE_1_ACTION}} | {{STAGE_1_TOUCH}} | 😐 Neutral | {{STAGE_1_OPP}} |
> 51	| Consideration | {{STAGE_2_ACTION}} | {{STAGE_2_TOUCH}} | 🤔 Curious | {{STAGE_2_OPP}} |
> 52	| Activation | {{STAGE_3_ACTION}} | {{STAGE_3_TOUCH}} | 😊 Excited | {{STAGE_3_OPP}} |
> 53	| Value | {{STAGE_4_ACTION}} | {{STAGE_4_TOUCH}} | 🚀 Delighted | {{STAGE_4_OPP}} |
> 54	| Retention | {{STAGE_5_ACTION}} | {{STAGE_5_TOUCH}} | ❤️ Loyal | {{STAGE_5_OPP}} |
> 55	
> 56	#### Edge Case 1: {{EDGE_CASE_1_NAME}}
> 57	> {{EDGE_CASE_1_DESC}}
> 58	
> 59	#### Edge Case 2: {{EDGE_CASE_2_NAME}}
> 60	> {{EDGE_CASE_2_DESC}}
> 61	
> 62	---
> 63	
> 64	## 4. Feature Inventory (MoSCoW)
> 65	
> 66	> Effort: S=hours, M=days, L=week, XL=sprint
> 67	
> 68	### Must Have (MVP)
> 69	
> 70	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 71	|----|---------|---------|-----------|--------|-------------|-------|
> 72	| PR-001 | {{PR_001_NAME}} | P1 | BR-001 | {{PR_001_EFFORT}} | {{PR_001_COINS}} | {{PR_001_NOTES}} |
> 73	| PR-002 | {{PR_002_NAME}} | P1, P2 | BR-002 | {{PR_002_EFFORT}} | {{PR_002_COINS}} | {{PR_002_NOTES}} |
> 74	
> 75	### Should Have (v1.0)
> 76	
> 77	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 78	|----|---------|---------|-----------|--------|-------------|-------|
> 79	| PR-010 | {{PR_010_NAME}} | P2 | BR-003 | {{PR_010_EFFORT}} | {{PR_010_COINS}} | {{PR_010_NOTES}} |
> 80	
> 81	### Could Have (Future)
> 82	
> 83	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 84	|----|---------|---------|-----------|--------|-------------|-------|
> 85	| PR-020 | {{PR_020_NAME}} | P1 | BR-004 | {{PR_020_EFFORT}} | {{PR_020_COINS}} | {{PR_020_NOTES}} |
> 86	
> 87	### Won't Have (This Cycle)
> 88	
> 89	- {{WONT_HAVE_1}}
> 90	- {{WONT_HAVE_2}}
> 91	
> 92	---
> 93	
> 94	## 5. Release Phasing
> 95	
> 96	### MVP Scope
> 97	**Target date:** {{MVP_DATE}}  
> 98	**Included:** PR-001, PR-002  
> 99	**Success gate:** {{MVP_SUCCESS_GATE}}
> 100	
> 101	### v1.0 Scope
> 102	**Target date:** {{V1_DATE}}  
> 103	**Adds:** PR-010, PR-011  
> 104	**Success gate:** {{V1_SUCCESS_GATE}}
> 105	
> 106	### Future Scope
> 107	**Items:** PR-020+  
> 108	**Condition:** {{FUTURE_CONDITION}}
> 109	
> 110	---
> 111	
> 112	## 6. Luxury UX Specifications
> 113	
> 114	### 6.1 Color & Visual Identity
> 115	
> 116	| Token | Value | Usage |
> 117	|-------|-------|-------|
> 118	| `--bg-deep` | `#0A0A0F` | Canvas background |
> 119	| `--accent-violet` | `#7C3AED` | Primary CTA, active states |
> 120	| `--accent-cyan` | `#06B6D4` | Data highlights, graphs |
> 121	| `--glass-surface` | `rgba(255,255,255,0.04)` | Card backgrounds |
> 122	| `--border-subtle` | `rgba(255,255,255,0.08)` | Card borders |
> 123	
> 124	### 6.2 Animation Guidelines
> 125	
> 126	| Element | Library | Duration | Easing |
> 127	|---------|---------|----------|--------|
> 128	| Page transitions | Framer Motion | 300ms | `easeInOut` |
> 129	| Node entrance (3D) | R3F / drei | 500ms | `spring(stiffness:80)` |
> 130	| Status pulse | CSS keyframes | 2s | `ease-in-out infinite` |
> 131	| Micro-interactions | Framer Motion | 150ms | `easeOut` |
> 132	
> 133	### 6.3 Interaction Patterns
> 134	
> 135	- **Cards:** Glass morphism — `backdrop-blur-sm`, subtle border, shadow `0 4px 24px rgba(0,0,0,0.4)`.
> 136	- **Buttons:** Gradient border on hover; never flat fill for primary CTAs.
> 137	- **Loading states:** Skeleton shimmer (never spinners for content areas).
> 138	- **Toasts:** `sonner` library; success = violet, error = red, info = cyan.
> 139	
> 140	### 6.4 Accessibility (WCAG 2.1 AA)
> 141	
> 142	- Contrast ratio ≥ 4.5:1 for all text on glass surfaces.
> 143	- All interactive elements keyboard-navigable.
> 144	- ARIA labels on all icon-only buttons.
> 145	- Focus indicators visible at ≥ 2px.
> 146	
> 147	---
> 148	
> 149	## 7. Acceptance Criteria (Gherkin)
> 150	
> 151	```gherkin
> 152	Feature: {{FEATURE_NAME}}
> 153	
> 154	  Scenario: {{SCENARIO_1_TITLE}} (PR-001)
> 155	    Given {{GIVEN_1}}
> 156	    When {{WHEN_1}}
> 157	    Then {{THEN_1}}
> 158	    And {{AND_1}}
> 159	
> 160	  Scenario: {{SCENARIO_2_TITLE}} (PR-002)
> 161	    Given {{GIVEN_2}}
> 162	    When {{WHEN_2}}
> 163	    Then {{THEN_2}}
> 164	```
> 165	
> 166	---
> 167	
> 168	## 8. Traceability Matrix
> 169	
> 170	| MR ID | BR ID | PR ID |
> 171	|-------|-------|-------|
> 172	| MR-001 | BR-001 | PR-001, PR-002 |
> 173	| MR-002 | BR-002 | PR-010 |
> 174	
> 175	---
> 176	
> 177	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 178	
> ```

## 🤖 Claude *(02:42:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/04-frd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Scope Statement
> 11	
> 12	This document specifies the functional and non-functional requirements for `{{PROJECT_SLUG}}`.
> 13	It is derived from PRD `03-prd.md` and feeds directly into SDD `05-sdd.md`.
> 14	
> 15	**In scope:** {{SCOPE_IN}}  
> 16	**Out of scope:** {{SCOPE_OUT}}
> 17	
> 18	---
> 19	
> 20	## 2. Functional Requirements
> 21	
> 22	> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron`
> 23	
> 24	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 25	|----|-------|-------------|----------|-----------|----------|---------|
> 26	| FR-001 | {{FR_001_TITLE}} | {{FR_001_DESC}} | Critical | PR-001 | {{FR_001_CAT}} | AT-001 |
> 27	| FR-002 | {{FR_002_TITLE}} | {{FR_002_DESC}} | High | PR-001 | {{FR_002_CAT}} | AT-002 |
> 28	| FR-003 | {{FR_003_TITLE}} | {{FR_003_DESC}} | High | PR-002 | {{FR_003_CAT}} | AT-003 |
> 29	
> 30	---
> 31	
> 32	## 3. Non-Functional Requirements
> 33	
> 34	| ID | Category | Requirement | Target | Measurement |
> 35	|----|----------|-------------|--------|-------------|
> 36	| NFR-001 | Performance | Page load (LCP) | < 2.5s | Lighthouse CI |
> 37	| NFR-002 | Performance | Edge Function p95 latency | < 800ms | Supabase logs |
> 38	| NFR-003 | Scalability | Concurrent users without degradation | {{SCALE_TARGET}} | Load test |
> 39	| NFR-004 | Availability | Uptime SLO | 99.5%/month | Watchdog telemetry |
> 40	| NFR-005 | Maintainability | Cyclomatic complexity per hook | ≤ 10 | ESLint |
> 41	| NFR-006 | Security | All endpoints require valid JWT | 100% | Security review |
> 42	
> 43	---
> 44	
> 45	## 4. Interface Requirements
> 46	
> 47	### 4.1 UI → Hook → Edge Function Contract
> 48	
> 49	```
> 50	[Component: {{COMPONENT_NAME}}]
> 51	  ↓ calls
> 52	[Hook: use{{HOOK_NAME}}]
> 53	  ↓ calls (for sensitive ops)
> 54	[Edge Function: {{EDGE_FUNCTION_NAME}}]
> 55	  ↓ reads/writes
> 56	[Supabase Table: {{TABLE_NAME}}]
> 57	```
> 58	
> 59	### 4.2 External API Contracts
> 60	
> 61	#### `POST /functions/v1/{{EDGE_FUNCTION_NAME}}`
> 62	
> 63	**Auth:** Bearer JWT (user scope)  
> 64	**Request:**
> 65	```typescript
> 66	{
> 67	  {{REQUEST_FIELD_1}}: {{REQUEST_TYPE_1}},  // {{REQUEST_DESC_1}}
> 68	  {{REQUEST_FIELD_2}}: {{REQUEST_TYPE_2}},  // {{REQUEST_DESC_2}}
> 69	}
> 70	```
> 71	**Response (200):**
> 72	```typescript
> 73	{
> 74	  {{RESPONSE_FIELD_1}}: {{RESPONSE_TYPE_1}},
> 75	  {{RESPONSE_FIELD_2}}: {{RESPONSE_TYPE_2}},
> 76	}
> 77	```
> 78	**Error codes:**
> 79	| Code | Condition |
> 80	|------|-----------|
> 81	| 401 | Missing or invalid JWT |
> 82	| 402 | Insufficient mcoCoins balance |
> 83	| 422 | Validation failure (field + message in body) |
> 84	| 500 | Internal error (logged to infra_health_logs) |
> 85	
> 86	---
> 87	
> 88	## 5. Data Requirements
> 89	
> 90	| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |
> 91	|-------|------|----------|-----------------|----------------------|
> 92	| {{FIELD_1}} | {{TYPE_1}} | {{NULL_1}} | {{VALIDATION_1}} | {{ERROR_PT_1}} |
> 93	| {{FIELD_2}} | {{TYPE_2}} | {{NULL_2}} | {{VALIDATION_2}} | {{ERROR_PT_2}} |
> 94	
> 95	---
> 96	
> 97	## 6. Test Strategy Matrix
> 98	
> 99	| FR ID | Unit Test | Integration Test | E2E Test | Notes |
> 100	|-------|-----------|-----------------|----------|-------|
> 101	| FR-001 | ✅ Required | ✅ Required | ✅ Required | {{TEST_NOTES_001}} |
> 102	| FR-002 | ✅ Required | ✅ Required | — | {{TEST_NOTES_002}} |
> 103	| FR-003 | ✅ Required | — | — | {{TEST_NOTES_003}} |
> 104	
> 105	**Test files location:**
> 106	- Unit: `src/hooks/__tests__/use{{HOOK_NAME}}.test.ts`
> 107	- Integration: `src/__tests__/integration/{{FEATURE_NAME}}.test.ts`
> 108	- E2E: `e2e/{{FEATURE_NAME}}.spec.ts`
> 109	
> 110	---
> 111	
> 112	## 7. Traceability Matrix
> 113	
> 114	| PR ID | FR ID | NFR ID |
> 115	|-------|-------|--------|
> 116	| PR-001 | FR-001, FR-002 | NFR-001, NFR-006 |
> 117	| PR-002 | FR-003 | NFR-002 |
> 118	
> 119	---
> 120	
> 121	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 122	
> ```

## 🤖 Claude *(02:42:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/05-sdd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SDD — System Design Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Architecture Overview
> 11	
> 12	```
> 13	┌─────────────────────────────────────────────────────────┐
> 14	│  PRESENTATION LAYER (display-only)                       │
> 15	│  src/components/{{FEATURE_AREA}}/{{COMPONENT_NAME}}.tsx  │
> 16	└──────────────────────┬──────────────────────────────────┘
> 17	                       │ calls
> 18	┌──────────────────────▼──────────────────────────────────┐
> 19	│  LOGIC LAYER (Harness Engineering)                       │
> 20	│  src/hooks/use{{HOOK_NAME}}.ts                           │
> 21	│  src/store/{{STORE_SLICE}}.ts (Zustand, if needed)       │
> 22	└──────────────────────┬──────────────────────────────────┘
> 23	                       │ HTTP + JWT
> 24	┌──────────────────────▼──────────────────────────────────┐
> 25	│  EDGE LAYER (Deno / Supabase Functions)                  │
> 26	│  supabase/functions/{{EDGE_FUNCTION_NAME}}/index.ts      │
> 27	└──────────┬───────────────────────────┬──────────────────┘
> 28	           │ Supabase RLS              │ External APIs
> 29	┌──────────▼──────────┐  ┌────────────▼──────────────────┐
> 30	│  DB LAYER           │  │  EXTERNAL SERVICES             │
> 31	│  {{TABLE_1}}        │  │  OpenRouter (embeddings)        │
> 32	│  {{TABLE_2}}        │  │  {{EXTERNAL_API_1}}            │
> 33	│  mcorch_nodes       │  │  {{EXTERNAL_API_2}}            │
> 34	└─────────────────────┘  └────────────────────────────────┘
> 35	```
> 36	
> 37	---
> 38	
> 39	## 2. Component Catalog
> 40	
> 41	### 2.1 New Custom Hooks (`src/hooks/`)
> 42	
> 43	| Hook | File | Responsibility | TanStack Query keys |
> 44	|------|------|---------------|---------------------|
> 45	| `use{{Hook1}}` | `use{{Hook1}}.ts` | {{HOOK1_RESP}} | `['{{KEY_1}}']` |
> 46	| `use{{Hook2}}` | `use{{Hook2}}.ts` | {{HOOK2_RESP}} | `['{{KEY_2}}']` |
> 47	
> 48	### 2.2 New Display Components (`src/components/`)
> 49	
> 50	| Component | File | Props | Hook consumed |
> 51	|-----------|------|-------|--------------|
> 52	| `{{Component1}}` | `{{PATH_1}}` | `{{PROPS_1}}` | `use{{Hook1}}` |
> 53	| `{{Component2}}` | `{{PATH_2}}` | `{{PROPS_2}}` | `use{{Hook2}}` |
> 54	
> 55	### 2.3 New Edge Functions (`supabase/functions/`)
> 56	
> 57	| Function | Path | Auth | mcoCoins | Secrets needed |
> 58	|----------|------|------|----------|----------------|
> 59	| `{{EdgeFn1}}` | `supabase/functions/{{EdgeFn1}}/index.ts` | JWT (user) | {{COINS_1}} | `{{SECRETS_1}}` |
> 60	
> 61	### 2.4 Zustand Store Slices (if applicable)
> 62	
> 63	| Slice | Store file | State shape | Actions |
> 64	|-------|------------|-------------|---------|
> 65	| `{{SLICE_1}}` | `src/store/use{{StoreName}}.ts` | `{{STATE_1}}` | `{{ACTIONS_1}}` |
> 66	
> 67	### 2.5 New DB Objects
> 68	
> 69	| Object | Type | Purpose | Migration file |
> 70	|--------|------|---------|---------------|
> 71	| `{{TABLE_1}}` | Table | {{TABLE_1_PURPOSE}} | `{{MIGRATION_1}}` |
> 72	| `{{VIEW_1}}` | View | {{VIEW_1_PURPOSE}} | `{{MIGRATION_2}}` |
> 73	
> 74	---
> 75	
> 76	## 3. Data Flow Diagrams
> 77	
> 78	### Use Case: {{USE_CASE_1}}
> 79	
> 80	```
> 81	User                Hook              Edge Fn            DB
> 82	 │                   │                   │                │
> 83	 │──[action]────────▶│                   │                │
> 84	 │                   │──[POST JWT]───────▶│                │
> 85	 │                   │                   │──[check mco]──▶│ deduct_mco_coins RPC
> 86	 │                   │                   │◀──[ok]─────────│
> 87	 │                   │                   │──[AI call]──▶  │ (OpenRouter/external)
> 88	 │                   │                   │◀──[result]──   │
> 89	 │                   │                   │──[insert]─────▶│ {{TABLE_1}}
> 90	 │                   │                   │──[embed node]──▶│ mcorch_nodes
> 91	 │                   │◀──[200 response]──│                │
> 92	 │◀──[UI update]─────│                   │                │
> 93	```
> 94	
> 95	---
> 96	
> 97	## 4. API Contract Definitions
> 98	
> 99	> All Edge Functions must validate JWT before any business logic.
> 100	
> 101	### `POST /functions/v1/{{EdgeFn1}}`
> 102	
> 103	```typescript
> 104	// Request
> 105	interface {{EdgeFn1}}Request {
> 106	  {{REQ_FIELD_1}}: {{REQ_TYPE_1}}
> 107	  {{REQ_FIELD_2}}: {{REQ_TYPE_2}}
> 108	}
> 109	
> 110	// Response (HTTP 200)
> 111	interface {{EdgeFn1}}Response {
> 112	  status: 'ok'
> 113	  {{RESP_FIELD_1}}: {{RESP_TYPE_1}}
> 114	}
> 115	
> 116	// mcoCoins deduction point:
> 117	// → Line ~40: await supabase.rpc('deduct_mco_coins', { p_user_id, p_amount: {{COIN_AMOUNT}} })
> 118	// → HTTP 402 if insufficient balance
> 119	```
> 120	
> 121	---
> 122	
> 123	## 5. Security Design
> 124	
> 125	### 5.1 Threat Model (STRIDE)
> 126	
> 127	| Component | Threat | Type | Severity | Mitigation |
> 128	|-----------|--------|------|----------|------------|
> 129	| `{{EdgeFn1}}` | Unauthenticated access | Spoofing | High | JWT validation at entry point |
> 130	| `{{TABLE_1}}` | Cross-tenant data read | Information Disclosure | Critical | RLS `user_id = auth.uid()` |
> 131	| mcoCoins deduction | Client-side bypass | Tampering | Critical | Server-side RPC only |
> 132	| {{THREAT_4}} | {{THREAT_4_DESC}} | {{THREAT_4_TYPE}} | {{THREAT_4_SEV}} | {{THREAT_4_MIT}} |
> 133	
> 134	### 5.2 RLS Policy Definitions
> 135	
> 136	```sql
> 137	-- {{TABLE_1}} RLS
> 138	ALTER TABLE {{TABLE_1}} ENABLE ROW LEVEL SECURITY;
> 139	
> 140	CREATE POLICY "{{TABLE_1}}_select_own"
> 141	  ON {{TABLE_1}} FOR SELECT
> 142	  USING (user_id = auth.uid());
> 143	
> 144	CREATE POLICY "{{TABLE_1}}_insert_own"
> 145	  ON {{TABLE_1}} FOR INSERT
> 146	  WITH CHECK (user_id = auth.uid());
> 147	```
> 148	
> 149	### 5.3 JWT Validation Points
> 150	
> 151	All Edge Functions follow this pattern:
> 152	```typescript
> 153	const authHeader = req.headers.get('Authorization')
> 154	if (!authHeader) return new Response('Unauthorized', { status: 401 })
> 155	const { data: { user }, error } = await supabase.auth.getUser(
> 156	  authHeader.replace('Bearer ', '')
> 157	)
> 158	if (error || !user) return new Response('Unauthorized', { status: 401 })
> 159	```
> 160	
> 161	### 5.4 Secrets Inventory
> 162	
> 163	| Secret Name | Used In | Vault Location | Rotation Policy |
> 164	|-------------|---------|----------------|----------------|
> 165	| `{{SECRET_1}}` | `{{EdgeFn1}}` | Supabase Vault | {{ROTATION_1}} |
> 166	
> 167	> ⚠️ NEVER commit secret values. Only key names appear in documentation.
> 168	
> 169	---
> 170	
> 171	## 6. Infrastructure Touchpoints
> 172	
> 173	| Infrastructure | Usage | Impact |
> 174	|----------------|-------|--------|
> 175	| `mcorch_chroma` (ChromaDB port 8001) | {{CHROMA_USAGE}} | {{CHROMA_IMPACT}} |
> 176	| `mega-brain-daemon` | {{DAEMON_USAGE}} | {{DAEMON_IMPACT}} |
> 177	| `infra_health_logs` | New event type: `{{NEW_EVENT_TYPE}}` | Watchdog telemetry |
> 178	
> 179	---
> 180	
> 181	## 7. Migration Stubs
> 182	
> 183	```sql
> 184	-- Migration: {{MIGRATION_TIMESTAMP}}_{{PROJECT_SLUG}}_initial.sql
> 185	
> 186	CREATE TABLE {{TABLE_1}} (
> 187	  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 188	  user_id     uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 189	  project_id  uuid REFERENCES projects(id) ON DELETE CASCADE,
> 190	  -- feature-specific columns:
> 191	  {{COLUMN_1}} {{COL_TYPE_1}} {{COL_CONSTRAINTS_1}},
> 192	  {{COLUMN_2}} {{COL_TYPE_2}} {{COL_CONSTRAINTS_2}},
> 193	  -- embeddings (if applicable):
> 194	  embedding   vector(768),
> 195	  -- audit:
> 196	  created_at  timestamptz DEFAULT now() NOT NULL,
> 197	  updated_at  timestamptz DEFAULT now() NOT NULL
> 198	);
> 199	
> 200	ALTER TABLE {{TABLE_1}} ENABLE ROW LEVEL SECURITY;
> 201	-- (paste RLS policies from §5.2)
> 202	
> 203	-- HNSW index (only if embedding column present):
> 204	CREATE INDEX {{TABLE_1}}_embedding_idx
> 205	  ON {{TABLE_1}} USING hnsw (embedding vector_cosine_ops)
> 206	  WITH (m = 16, ef_construction = 64);
> 207	```
> 208	
> 209	---
> 210	
> 211	## 8. Open Technical Decisions
> 212	
> 213	| ID | Description | Option A | Option B | Recommendation | Owner |
> 214	|----|-------------|----------|----------|----------------|-------|
> 215	| OTD-001 | {{OTD_001_DESC}} | {{OTD_001_A}} | {{OTD_001_B}} | {{OTD_001_REC}} | Sovereign |
> 216	
> 217	---
> 218	
> 219	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 220	
> ```

## 🤖 Claude *(02:42:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/06-data-model.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Data & Knowledge Model
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Conceptual Data Model
> 11	
> 12	```
> 13	[{{ENTITY_1}}] ──(1:N)──▶ [{{ENTITY_2}}]
> 14	      │
> 15	      └──(N:M)──▶ [{{ENTITY_3}}]
> 16	                         │
> 17	                         └──(1:1)──▶ [mcorch_nodes]
> 18	```
> 19	
> 20	**Entities:**
> 21	- **{{ENTITY_1}}:** {{ENTITY_1_DESC}}
> 22	- **{{ENTITY_2}}:** {{ENTITY_2_DESC}}
> 23	- **{{ENTITY_3}}:** {{ENTITY_3_DESC}}
> 24	
> 25	---
> 26	
> 27	## 2. Logical Data Model
> 28	
> 29	### Table: `{{TABLE_1}}`
> 30	
> 31	| Column | Type | Nullable | Default | FK | Description |
> 32	|--------|------|----------|---------|-----|------------|
> 33	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | Primary key |
> 34	| `user_id` | `uuid` | NOT NULL | — | `auth.users.id` | Tenant isolation |
> 35	| `project_id` | `uuid` | NULL | — | `projects.id` | Project scope |
> 36	| `{{COL_1}}` | `{{TYPE_1}}` | {{NULL_1}} | {{DEFAULT_1}} | {{FK_1}} | {{DESC_1}} |
> 37	| `{{COL_2}}` | `{{TYPE_2}}` | {{NULL_2}} | {{DEFAULT_2}} | {{FK_2}} | {{DESC_2}} |
> 38	| `embedding` | `vector(768)` | NULL | — | — | Neural embedding (OpenRouter text-embedding-3-small) |
> 39	| `stability_score` | `float4` | NOT NULL | `0.5` | — | FSRS-6 memory stability |
> 40	| `created_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 41	| `updated_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 42	
> 43	### Table: `{{TABLE_2}}`
> 44	
> 45	| Column | Type | Nullable | Default | FK | Description |
> 46	|--------|------|----------|---------|-----|------------|
> 47	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | Primary key |
> 48	| `{{TABLE_1}}_id` | `uuid` | NOT NULL | — | `{{TABLE_1}}.id` | Parent reference |
> 49	| `{{COL_3}}` | `{{TYPE_3}}` | {{NULL_3}} | {{DEFAULT_3}} | {{FK_3}} | {{DESC_3}} |
> 50	
> 51	---
> 52	
> 53	## 3. Supabase Physical Schema Stubs
> 54	
> 55	```sql
> 56	-- ============================================================
> 57	-- MIGRATION: {{MIGRATION_TIMESTAMP}}_{{PROJECT_SLUG}}_schema.sql
> 58	-- ============================================================
> 59	
> 60	-- {{TABLE_1}}
> 61	CREATE TABLE public.{{TABLE_1}} (
> 62	  id             uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 63	  user_id        uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 64	  project_id     uuid REFERENCES public.projects(id) ON DELETE CASCADE,
> 65	  {{COL_1}}      {{TYPE_1}} {{CONSTRAINTS_1}},
> 66	  {{COL_2}}      {{TYPE_2}} {{CONSTRAINTS_2}},
> 67	  embedding      vector(768),
> 68	  stability_score float4 NOT NULL DEFAULT 0.5,
> 69	  created_at     timestamptz NOT NULL DEFAULT now(),
> 70	  updated_at     timestamptz NOT NULL DEFAULT now()
> 71	);
> 72	
> 73	ALTER TABLE public.{{TABLE_1}} ENABLE ROW LEVEL SECURITY;
> 74	
> 75	-- RLS Policies
> 76	CREATE POLICY "{{TABLE_1}}: users read own rows"
> 77	  ON public.{{TABLE_1}} FOR SELECT
> 78	  USING (user_id = auth.uid());
> 79	
> 80	CREATE POLICY "{{TABLE_1}}: users insert own rows"
> 81	  ON public.{{TABLE_1}} FOR INSERT
> 82	  WITH CHECK (user_id = auth.uid());
> 83	
> 84	CREATE POLICY "{{TABLE_1}}: users update own rows"
> 85	  ON public.{{TABLE_1}} FOR UPDATE
> 86	  USING (user_id = auth.uid())
> 87	  WITH CHECK (user_id = auth.uid());
> 88	
> 89	-- Indexes
> 90	CREATE INDEX {{TABLE_1}}_user_idx ON public.{{TABLE_1}} (user_id);
> 91	CREATE INDEX {{TABLE_1}}_project_idx ON public.{{TABLE_1}} (project_id);
> 92	
> 93	-- HNSW (embeddings)
> 94	CREATE INDEX {{TABLE_1}}_embedding_hnsw
> 95	  ON public.{{TABLE_1}} USING hnsw (embedding vector_cosine_ops)
> 96	  WITH (m = 16, ef_construction = 64);
> 97	
> 98	-- Updated-at trigger
> 99	CREATE TRIGGER set_{{TABLE_1}}_updated_at
> 100	  BEFORE UPDATE ON public.{{TABLE_1}}
> 101	  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
> 102	```
> 103	
> 104	---
> 105	
> 106	## 4. GraphRAG Knowledge Nodes
> 107	
> 108	### Node Types Introduced
> 109	
> 110	| node_type | Title Pattern | Content Fields | Embedding Source |
> 111	|-----------|--------------|----------------|-----------------|
> 112	| `{{NODE_TYPE_1}}` | `{{TITLE_PATTERN_1}}` | `{{CONTENT_FIELDS_1}}` | `{{EMBED_SOURCE_1}}` |
> 113	| `{{NODE_TYPE_2}}` | `{{TITLE_PATTERN_2}}` | `{{CONTENT_FIELDS_2}}` | `{{EMBED_SOURCE_2}}` |
> 114	
> 115	### Edge Types Introduced
> 116	
> 117	| Edge relationship | Source node_type | Target node_type | Metadata |
> 118	|-------------------|-----------------|-----------------|----------|
> 119	| `{{EDGE_REL_1}}` | `{{EDGE_SRC_1}}` | `{{EDGE_TGT_1}}` | `{{EDGE_META_1}}` |
> 120	
> 121	### Embedding Trigger
> 122	
> 123	Every insert into `{{TABLE_1}}` must call `embed-mcorch-node`:
> 124	```typescript
> 125	// In the Edge Function, after successful insert:
> 126	await supabase.functions.invoke('embed-mcorch-node', {
> 127	  body: { node_id: insertedNode.id, content: `${title} ${content}` }
> 128	})
> 129	```
> 130	
> 131	### FSRS-6 Parameters
> 132	
> 133	| Field | Initial Value | Decay Rule |
> 134	|-------|--------------|------------|
> 135	| `stability_score` | `0.5` | Decays per migration `20260425190000` formula |
> 136	| `revenue_impact` | {{REVENUE_IMPACT_CALC}} | Updated on each successful orchestration run |
> 137	
> 138	---
> 139	
> 140	## 5. Tenant Isolation Map
> 141	
> 142	| Table | `user_id` scope | `project_id` scope | System rows (user_id IS NULL) |
> 143	|-------|----------------|-------------------|-------------------------------|
> 144	| `{{TABLE_1}}` | ✅ Required | Optional | No |
> 145	| `{{TABLE_2}}` | ✅ Required | ✅ Required | No |
> 146	| `mcorch_nodes` | Optional | Optional | Yes (system nodes) |
> 147	
> 148	---
> 149	
> 150	## 6. Data Quality Rules
> 151	
> 152	| Table | Column | Rule | Violation Message (PT-BR) |
> 153	|-------|--------|------|--------------------------|
> 154	| `{{TABLE_1}}` | `{{COL_1}}` | {{QUALITY_RULE_1}} | {{QUALITY_MSG_1}} |
> 155	| `{{TABLE_1}}` | `{{COL_2}}` | {{QUALITY_RULE_2}} | {{QUALITY_MSG_2}} |
> 156	
> 157	---
> 158	
> 159	## 7. Retention & Archival Policy
> 160	
> 161	| Data | Retention Period | Archival Strategy | Deletion Trigger |
> 162	|------|-----------------|-------------------|-----------------|
> 163	| `{{TABLE_1}}` rows | {{RETENTION_1}} | {{ARCHIVAL_1}} | {{DELETE_TRIGGER_1}} |
> 164	| Embeddings (`vector` column) | Indefinite | Backfill via `scripts/backfill-embeddings.ts` | With parent row |
> 165	| `infra_health_logs` entries | 90 days | No archival | Cron purge |
> 166	
> 167	---
> 168	
> 169	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 170	
> ```

## 🤖 Claude *(02:42:34)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/07-process-flow.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Process & Automation Blueprint
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** BPM CBOK v4 (Process Modeling + Process Design)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Process Inventory
> 11	
> 12	| Process ID | Name | Type | Trigger | Owner | SLA |
> 13	|------------|------|------|---------|-------|-----|
> 14	| PROC-001 | {{PROC_001_NAME}} | {{PROC_001_TYPE}} | {{PROC_001_TRIGGER}} | System | {{PROC_001_SLA}} |
> 15	| PROC-002 | {{PROC_002_NAME}} | {{PROC_002_TYPE}} | {{PROC_002_TRIGGER}} | User | {{PROC_002_SLA}} |
> 16	
> 17	> Types: `automated` | `human-in-loop` | `cron` | `event-driven`
> 18	
> 19	---
> 20	
> 21	## 2. BPMN-lite Process Maps
> 22	
> 23	### PROC-001: {{PROC_001_NAME}}
> 24	
> 25	```
> 26	START ──▶ [{{TASK_1}}] ──▶ <Gateway: {{GATEWAY_1_NAME}}>
> 27	                                  │ YES                    │ NO
> 28	                            [{{TASK_2}}]              [{{ERROR_PATH_1}}]
> 29	                                  │                         │
> 30	                            [{{TASK_3}}]              [Notify: {{ERROR_NOTIF}}]
> 31	                                  │                         │
> 32	                               ◀──┴─────────────────────────┘
> 33	                                  │
> 34	                               [Insert mcorch_node]
> 35	                                  │
> 36	                                END
> 37	```
> 38	
> 39	**Swimlanes:**
> 40	
> 41	| Swimlane | Participant | Tasks |
> 42	|----------|-------------|-------|
> 43	| User | Browser / Frontend | {{USER_TASKS}} |
> 44	| Frontend Hook | `use{{HookName}}.ts` | {{HOOK_TASKS}} |
> 45	| Edge Function | `{{EdgeFunctionName}}` | {{EDGE_TASKS}} |
> 46	| External API | `{{ExternalAPI}}` | {{EXT_TASKS}} |
> 47	| DB | Supabase / PostgreSQL | {{DB_TASKS}} |
> 48	
> 49	---
> 50	
> 51	### PROC-002: {{PROC_002_NAME}}
> 52	
> 53	```
> 54	[User Action: {{USER_ACTION}}]
> 55	  │
> 56	  ▼
> 57	[Hook: use{{HookName}} → mutation trigger]
> 58	  │
> 59	  ▼
> 60	[Edge Fn: {{EdgeFunctionName}}]
> 61	  ├── Validate JWT ──(fail)──▶ HTTP 401
> 62	  ├── Check mcoCoins ──(low)──▶ HTTP 402 → Toast: "Saldo insuficiente"
> 63	  ├── {{BUSINESS_LOGIC_STEP}}
> 64	  ├── Persist to {{TABLE_1}}
> 65	  ├── Embed node via embed-mcorch-node
> 66	  └── HTTP 200 → React Query invalidation → UI refresh
> 67	```
> 68	
> 69	---
> 70	
> 71	## 3. n8n Workflow Blueprints
> 72	
> 73	### Workflow: {{N8N_WORKFLOW_1_NAME}}
> 74	
> 75	**Trigger:** {{N8N_TRIGGER_1}}  
> 76	**Idempotency key:** `{{N8N_IDEMPOTENCY_KEY}}`
> 77	
> 78	```
> 79	[Trigger: {{N8N_TRIGGER_1}}]
> 80	  │
> 81	  ▼
> 82	[Node: HTTP Request → /functions/v1/{{EdgeFunctionName}}]
> 83	  ├── Headers: Authorization: Bearer {{SERVICE_ROLE_OR_USER_JWT}}
> 84	  ├── Body: { {{N8N_REQUEST_BODY}} }
> 85	  │
> 86	  ├── (success) ──▶ [Node: Update Supabase row status = 'complete']
> 87	  │                         │
> 88	  │                         ▼
> 89	  │                [Node: Send notification (optional)]
> 90	  │
> 91	  └── (error) ──▶ [Node: Set retry count + 1]
> 92	                         │
> 93	                   (count ≤ 3) ──▶ [Wait: exponential backoff]──▶ retry
> 94	                         │
> 95	                   (count > 3) ──▶ [Node: Insert infra_health_logs {event: 'n8n_failure'}]
> 96	                                         │
> 97	                                   [Node: Alert Sovereign]
> 98	```
> 99	
> 100	**Data Mapping:**
> 101	
> 102	| Input Field | Source | → | Output Field | Destination |
> 103	|-------------|--------|---|--------------|-------------|
> 104	| `{{IN_FIELD_1}}` | Trigger body | → | `{{OUT_FIELD_1}}` | Edge Function body |
> 105	| `{{IN_FIELD_2}}` | Env var | → | `Authorization` | Header |
> 106	
> 107	---
> 108	
> 109	## 4. Orchestration Integration Points
> 110	
> 111	> Applies only if this feature integrates with `orchestrate-content` pipeline.
> 112	
> 113	| Pipeline Step | Step ID | Position | Description | mcoCoins Trigger |
> 114	|---------------|---------|----------|-------------|-----------------|
> 115	| {{PIPELINE_STEP_1}} | step_{{STEP_ID_1}} | After step {{PREV_STEP}} | {{STEP_DESC_1}} | {{STEP_COINS_1}} coins at entry |
> 116	
> 117	**Integration code stub (inside `orchestrate-content/index.ts`):**
> 118	```typescript
> 119	// Step {{STEP_ID_1}}: {{PIPELINE_STEP_1}}
> 120	await updateNodeStatus(nodes, '{{STEP_ID_1}}', 'running')
> 121	const {{STEP_RESULT}} = await {{STEP_ACTION}}(payload)
> 122	if (!{{STEP_RESULT}}.ok) {
> 123	  await updateNodeStatus(nodes, '{{STEP_ID_1}}', 'error')
> 124	  throw new Error('{{PIPELINE_STEP_1}} failed')
> 125	}
> 126	await updateNodeStatus(nodes, '{{STEP_ID_1}}', 'complete')
> 127	```
> 128	
> 129	---
> 130	
> 131	## 5. Error Handling & Retry Strategy
> 132	
> 133	| Process | Step | Error Type | Max Retries | Backoff | Failure Action |
> 134	|---------|------|-----------|-------------|---------|----------------|
> 135	| PROC-001 | {{TASK_1}} | Network timeout | 3 | Exponential (2s, 4s, 8s) | Insert `infra_health_logs` |
> 136	| PROC-001 | {{TASK_2}} | External API 5xx | 2 | Fixed 5s | Alert + mark failed |
> 137	| PROC-002 | mcoCoins check | Insufficient balance | 0 | — | HTTP 402 to user |
> 138	| Any | JWT validation | Invalid token | 0 | — | HTTP 401 immediately |
> 139	
> 140	---
> 141	
> 142	## 6. SLA Definitions
> 143	
> 144	| Process | Step | Expected Duration | Timeout Threshold | Alert if exceeded |
> 145	|---------|------|------------------|-------------------|-------------------|
> 146	| PROC-001 | End-to-end | {{E2E_DURATION}} | {{E2E_TIMEOUT}} | Yes → infra_health_logs |
> 147	| PROC-001 | {{TASK_1}} alone | {{TASK_1_DURATION}} | {{TASK_1_TIMEOUT}} | No |
> 148	| PROC-002 | Edge Fn response | < 800ms p95 | 5s | Yes |
> 149	
> 150	---
> 151	
> 152	## 7. Cron Jobs
> 153	
> 154	| Job Name | Schedule (cron) | Function | Idempotency | Failure Alerting |
> 155	|----------|----------------|----------|-------------|-----------------|
> 156	| `{{CRON_1_NAME}}` | `{{CRON_1_SCHEDULE}}` | `{{CRON_1_FN}}` | `{{CRON_1_KEY}}` | `infra_health_logs` |
> 157	
> 158	> All cron jobs must be idempotent — re-running on the same data must produce the same result.
> 159	
> 160	---
> 161	
> 162	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 163	
> ```

## 🤖 Claude *(02:42:34)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/08-quality-metrics.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Quality & Self-Optimization Specification
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Quality Objectives
> 11	
> 12	| QO ID | Objective | Linked Business Objective | Target | Review Cadence |
> 13	|-------|-----------|--------------------------|--------|---------------|
> 14	| QO-001 | {{QO_001}} | BO-001 | {{QO_001_TARGET}} | Weekly |
> 15	| QO-002 | {{QO_002}} | BO-002 | {{QO_002_TARGET}} | Monthly |
> 16	| QO-003 | {{QO_003}} | BO-003 | {{QO_003_TARGET}} | Quarterly |
> 17	
> 18	---
> 19	
> 20	## 2. KPI Dashboard Definition
> 21	
> 22	> Data source: Supabase tables/views listed per KPI.
> 23	
> 24	| KPI ID | Name | Formula | Target | Warn Threshold | Critical Threshold | Data Source |
> 25	|--------|------|---------|--------|---------------|-------------------|-------------|
> 26	| KPI-001 | {{KPI_001_NAME}} | {{KPI_001_FORMULA}} | {{KPI_001_TARGET}} | {{KPI_001_WARN}} | {{KPI_001_CRIT}} | `{{KPI_001_TABLE}}` |
> 27	| KPI-002 | {{KPI_002_NAME}} | {{KPI_002_FORMULA}} | {{KPI_002_TARGET}} | {{KPI_002_WARN}} | {{KPI_002_CRIT}} | `{{KPI_002_TABLE}}` |
> 28	| KPI-003 | mcoCoins Burn Rate | `SUM(deductions) / active_users` | < {{BURN_TARGET}}/user | {{BURN_WARN}} | {{BURN_CRIT}} | `profiles` + `mco_transactions` |
> 29	| KPI-004 | Edge Fn p95 Latency | `PERCENTILE_CONT(0.95) OVER latency` | < 800ms | 1000ms | 2000ms | Supabase logs |
> 30	| KPI-005 | Knowledge Mesh Growth | `COUNT(mcorch_nodes) per week` | > {{MESH_GROWTH_TARGET}} | < {{MESH_GROWTH_WARN}} | 0 | `mcorch_nodes` |
> 31	
> 32	---
> 33	
> 34	## 3. FMEA Table
> 35	
> 36	> Severity, Occurrence, Detection: 1 (best) → 10 (worst). RPN = S × O × D. RPN > 100 requires action.
> 37	
> 38	| ID | Function | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
> 39	|----|---------|--------------|--------|---|---|---|-----|--------------------|
> 40	| FMEA-001 | {{FR_001_TITLE}} | {{FAILURE_001}} | {{EFFECT_001}} | {{S_001}} | {{O_001}} | {{D_001}} | {{RPN_001}} | {{ACTION_001}} |
> 41	| FMEA-002 | mcoCoins deduction | RPC timeout → double charge | User overcharged | 9 | 2 | 3 | 54 | Idempotency key on every RPC call |
> 42	| FMEA-003 | JWT validation | Missing header | Unauthenticated access | 10 | 2 | 1 | 20 | Hard fail at entry; logged to infra_health_logs |
> 43	| FMEA-004 | embed-mcorch-node | Embedding API timeout | Node stored without vector | 6 | 3 | 4 | 72 | Async retry queue; backfill via `scripts/backfill-embeddings.ts` |
> 44	| FMEA-005 | {{CRITICAL_FR}} | {{FAILURE_005}} | {{EFFECT_005}} | {{S_005}} | {{O_005}} | {{D_005}} | {{RPN_005}} | {{ACTION_005}} |
> 45	
> 46	---
> 47	
> 48	## 4. Self-Optimization Loops
> 49	
> 50	| Loop ID | Trigger Condition | KPI Source | Autonomous Response | Escalation (human) |
> 51	|---------|------------------|------------|--------------------|--------------------|
> 52	| SOL-001 | KPI-004 latency > 1000ms for 5 consecutive calls | infra_health_logs | `mega-brain-daemon`: restart Edge Fn container | Alert Sovereign if > 2s |
> 53	| SOL-002 | KPI-005 mesh growth = 0 for 7 days | mcorch_nodes | Trigger backfill job via cron | Alert if backfill fails |
> 54	| SOL-003 | {{TRIGGER_003}} | {{KPI_SOURCE_003}} | {{RESPONSE_003}} | {{ESCALATION_003}} |
> 55	| SOL-004 | mcoCoins balance < 10% of plan quota | profiles | Send in-app notification (PT-BR) | — (no auto-action) |
> 56	
> 57	---
> 58	
> 59	## 5. Self-Healing Specifications
> 60	
> 61	### 5.1 Watchdog Telemetry Events
> 62	
> 63	New event types to be written to `infra_health_logs` by this feature:
> 64	
> 65	| Event Type | Trigger | Severity | Payload |
> 66	|------------|---------|----------|---------|
> 67	| `{{PROJECT_SLUG}}_fn_failure` | Edge Fn 5xx after retry exhaustion | error | `{fn_name, error_message, user_id}` |
> 68	| `{{PROJECT_SLUG}}_embed_failure` | embed-mcorch-node timeout | warn | `{node_id, retry_count}` |
> 69	| `{{PROJECT_SLUG}}_sla_breach` | Process SLA exceeded | warn | `{process_id, elapsed_ms, threshold_ms}` |
> 70	
> 71	### 5.2 Auto-Recovery Script Stubs
> 72	
> 73	```bash
> 74	#!/bin/bash
> 75	# scripts/self-heal-{{PROJECT_SLUG}}.sh
> 76	# Triggered by mega-brain-daemon when {{PROJECT_SLUG}}_fn_failure detected
> 77	
> 78	FUNCTION_NAME="{{EDGE_FUNCTION_NAME}}"
> 79	LOG_TABLE="infra_health_logs"
> 80	
> 81	echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Self-heal triggered for $FUNCTION_NAME"
> 82	
> 83	# Step 1: Check function status
> 84	STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
> 85	  "$SUPABASE_URL/functions/v1/$FUNCTION_NAME/health" \
> 86	  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY")
> 87	
> 88	if [ "$STATUS" != "200" ]; then
> 89	  echo "[WARN] Function unhealthy (status: $STATUS). Re-deploying..."
> 90	  npx supabase functions deploy "$FUNCTION_NAME"
> 91	fi
> 92	
> 93	# Step 2: Log recovery attempt
> 94	# (insert into infra_health_logs via Supabase REST API)
> 95	echo "[OK] Self-heal complete for $FUNCTION_NAME"
> 96	```
> 97	
> 98	### 5.3 mega-brain-daemon Integration Points
> 99	
> 100	| Daemon Event | Condition | Action |
> 101	|-------------|-----------|--------|
> 102	| `health_check` | Every 5 min (watchdog cron) | Check `{{TABLE_1}}` row count vs. expected baseline |
> 103	| `anomaly_detected` | `infra_health_logs` error rate > 5/hour | Execute `self-heal-{{PROJECT_SLUG}}.sh` |
> 104	| `recovery_confirmed` | Health check passes after self-heal | Insert `recovery_ok` event to `infra_health_logs` |
> 105	
> 106	---
> 107	
> 108	## 6. SLA / SLO / SLI Definitions
> 109	
> 110	| Service | SLI (what we measure) | SLO (our target) | SLA (contractual consequence) |
> 111	|---------|----------------------|------------------|-------------------------------|
> 112	| `{{EdgeFunctionName}}` API | p95 response latency | ≤ 800ms | Credits issued if > 2s for > 1% of calls in a month |
> 113	| Data ingestion pipeline | % records processed within SLA | ≥ 99% | Incident report required |
> 114	| Knowledge Mesh embedding | % nodes with embedding within 5m of insert | ≥ 95% | Auto-backfill triggered |
> 115	| Platform uptime | % minutes available per month | ≥ 99.5% | Per enterprise contract |
> 116	
> 117	---
> 118	
> 119	## 7. PDCA Improvement Cadence
> 120	
> 121	| Cycle | Phase | Activity | Owner | Frequency |
> 122	|-------|-------|----------|-------|-----------|
> 123	| {{PROJECT_SLUG}} Quality | Plan | Review FMEA + KPI targets | Sovereign | Quarterly |
> 124	| {{PROJECT_SLUG}} Quality | Do | Implement top improvement action | Engineering | Per sprint |
> 125	| {{PROJECT_SLUG}} Quality | Check | Compare KPIs vs. targets; update FMEA RPNs | AIOS | Monthly |
> 126	| {{PROJECT_SLUG}} Quality | Act | Close loop; update this document | Sovereign | Monthly |
> 127	
> 128	**Improvement backlog location:** `.claude/context/sprint-priorities.md`
> 129	
> 130	---
> 131	
> 132	## 8. Observability Checklist
> 133	
> 134	### 8.1 Logging Events
> 135	
> 136	| Event | Location | Level | Fields logged |
> 137	|-------|----------|-------|--------------|
> 138	| Function entry | `{{EdgeFunctionName}}/index.ts` line ~10 | INFO | `{user_id, timestamp, request_id}` |
> 139	| mcoCoins deduction | After RPC call | INFO | `{user_id, amount, new_balance}` |
> 140	| Business logic error | Catch block | ERROR | `{user_id, error_message, stack}` |
> 141	| SLA breach | Timeout guard | WARN | `{process_id, elapsed_ms}` |
> 142	
> 143	### 8.2 Alerting Rules
> 144	
> 145	| Condition | Channel | Escalation |
> 146	|-----------|---------|------------|
> 147	| Error rate > 1% in 5 min | `infra_health_logs` insert | mega-brain-daemon auto-heal |
> 148	| p95 latency > 2s | `infra_health_logs` insert | Sovereign notification |
> 149	| Zero KPI-005 growth > 7 days | Scheduled check | AIOS agent alert |
> 150	
> 151	### 8.3 Distributed Tracing Touchpoints
> 152	
> 153	| Span | Start | End | Tags |
> 154	|------|-------|-----|------|
> 155	| `{{EdgeFunctionName}}.total` | Request received | Response sent | `user_id`, `status_code` |
> 156	| `{{EdgeFunctionName}}.mco_check` | Before RPC | After RPC | `amount`, `balance_after` |
> 157	| `{{EdgeFunctionName}}.embed` | Before embed-mcorch-node call | After call | `node_id`, `success` |
> 158	
> 159	---
> 160	
> 161	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 162	
> ```

## 🤖 Claude *(02:44:06)*


## 🤖 Claude *(02:44:07)*

Templates carregados — formato canônico claro. ID space desta suíte = sufixo **`-CV2`** (mirror de -GN/-OC/-VM/-E2E das suítes anteriores). Criando o diretório e autorando a suíte na sequência de fases.

## 🤖 Claude *(02:44:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "mkdir -p docs/bok/constellation-v2 && echo \"criado:\" && ls -la docs/bok/constellation-v2/",
  "description": "Create constellation-v2 BoK directory"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> criado:
> total 8
> drwxrwxr-x  2 ubuntu ubuntu 4096 May 31 23:44 .
> drwxrwxr-x 14 ubuntu ubuntu 4096 May 31 23:44 ..
> ```

## 🤖 Claude *(02:44:13)*


## 🤖 Claude *(02:44:13)*

Diretório pronto. Autorando **Fase 0 + Fase 1** (00-index + MRD + BRD):

## 🤖 Claude *(02:44:55)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/00-index.md",
  "content": "# BoK Documentation Suite \u2014 constellation-v2\n\n**Generated:** 2026-05-31\n**Version:** v0.1\n**Agent:** MCORCH BoK Scribe Agent v1.0.0\n**Sovereign:** Gabriel Zarattini\n\n---\n\n## Project Metadata\n\n| Field | Value |\n|-------|-------|\n| Business Idea | Cockpit operacional de agentes de produto **per-user** \u2014 refatora\u00e7\u00e3o v2 do `/dashboard/constellation` (hoje casca Lovable decorativa). Cada usu\u00e1rio tem sua constela\u00e7\u00e3o de agentes que executam trabalho REAL dentro da conta dele, acionando os m\u00f3dulos do ecossistema, com isolamento de tenant duro, economia mcoCoins e credenciais BYOK per-user. |\n| Market Segment | B2B2C |\n| Monetization Model | hybrid (planos de assinatura + consumo mcoCoins por execu\u00e7\u00e3o de agente) |\n| Regulatory Profile | LGPD |\n| Integration Surface | extends-mcorch (supera a BoK `mcorch-constellation` v1 que documenta a casca) |\n| Project Slug | `constellation-v2` |\n\n---\n\n## Document Registry\n\n| # | File | Document | BoK Applied | Status |\n|---|------|----------|-------------|--------|\n| 0 | `00-index.md` | Project Manifest | \u2014 | [x] complete |\n| 1 | `01-mrd.md` | Market Requirements Document | BABOK v3 | [x] complete |\n| 2 | `02-brd.md` | Business Requirements Document | BABOK v3 | [x] complete |\n| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [x] complete |\n| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [x] complete |\n| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [x] complete |\n| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [x] complete |\n| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [x] complete |\n| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [x] complete |\n\n---\n\n## Traceability Chain\n\n```\nMR-CV2-001 (agentes executam trabalho real)\n  \u2514\u2500\u2500 BR-CV2-001\n        \u2514\u2500\u2500 PR-CV2-001 (capability invocation) \u00b7 PR-CV2-002 (crew on-demand)\n              \u2514\u2500\u2500 FR-CV2-001..006 (capability router, agent-task-execute v2, RLS)\n                    \u2514\u2500\u2500 [agent_capabilities \u00b7 agent_executions \u00b7 capability-router edge \u00b7 PROC-CV2-002]\n\nMR-CV2-002 (isolamento de tenant duro)\n  \u2514\u2500\u2500 BR-CV2-002 \u2192 PR-CV2-003 \u2192 FR-CV2-010..012 \u2192 [RLS auth.uid() + capability allowlist + system-access denylist]\n\nMR-CV2-003 (cost control: mcoCoins + BYOK + caps)\n  \u2514\u2500\u2500 BR-CV2-003 \u2192 PR-CV2-004 \u2192 FR-CV2-020..023 \u2192 [agent_consumption_caps \u00b7 user_api_keys \u00b7 deduct_mco_coins \u00b7 PROC-CV2-003]\n\nMR-CV2-004 (empty-start)\n  \u2514\u2500\u2500 BR-CV2-004 \u2192 PR-CV2-005 \u2192 FR-CV2-030..031 \u2192 [drop seed_crew_template auto-call \u00b7 onboarding wizard]\n\nMR-CV2-005 (cockpit unificado 16 capabilities)\n  \u2514\u2500\u2500 BR-CV2-005 \u2192 PR-CV2-006/007 \u2192 FR-CV2-040..043 \u2192 [capability registry \u00b7 4\u00d74 map \u00b7 Leads\u2192Core edges]\n\nMR-CV2-006 (observabilidade)\n  \u2514\u2500\u2500 BR-CV2-006 \u2192 PR-CV2-010 \u2192 FR-CV2-050 \u2192 [useAgentActivity v2 \u00b7 /dashboard/agent-economics]\n\nMR-CV2-007 (performance do 3D)\n  \u2514\u2500\u2500 BR-CV2-007 \u2192 PR-CV2-011 \u2192 FR-CV2-060..061 \u2192 [render budget \u00b7 z-index layering \u00b7 LOD]\n```\n\n---\n\n## Phase Completion Log\n\n| Phase | Name | Completed | Notes |\n|-------|------|-----------|-------|\n| 0 | Project Bootstrap | 2026-05-31 | slug `constellation-v2`; supersedes `mcorch-constellation` v1 BoK |\n| 1 | Market & Business Intelligence | 2026-05-31 | 7 MR-CV2 \u00b7 7 BR-CV2 \u00b7 3 BO-CV2 |\n| 2 | Product Definition | 2026-05-31 | 2 personas \u00b7 13 PR-CV2 (MoSCoW) |\n| 3 | Technical Specification | 2026-05-31 | 30+ FR-CV2 \u00b7 12 NFR-CV2 \u00b7 STRIDE \u00b7 8 OTD-CV2 |\n| 4 | Data & Process Engineering | 2026-05-31 | 4 new tables \u00b7 9 PROC-CV2 |\n| 5 | Quality & Autonomic Engineering | 2026-05-31 | 10 KPI-CV2 \u00b7 12 FMEA-CV2 \u00b7 SOL/SLA |\n| 6 | Traceability Validation | 2026-05-31 | 0 orphans (see \u00a7below) |\n| 7 | Knowledge Mesh Injection | 2026-05-31 | seal node via `scripts/seed-constellation-v2-bok-seal.ts` |\n\n---\n\n## Material Context Snapshot (verified 2026-05-31 via REST service-role)\n\n> This BoK was authored against a **materially verified** current state, not assumptions.\n\n| Fact | Value | Source |\n|------|-------|--------|\n| Real user profiles | **1** (Sovereign) | `profiles` count=exact |\n| `crew_agents` rows | **717** across **27** distinct owners | REST jq group_by |\n| Orphan owners (no profile) | **26** (~688 garbage rows) | profiles \u2229 crew owners |\n| Sovereign crew size | **53** (1 Core + 4 Leads + 4\u00d712 via \"Deploy Enterprise\") | enterprise-seed.ts memberCount=12 |\n| `crew_edges` rows | **689** (Directive 92 \u00b7 Reporting 576 \u00b7 semantic 21) | REST jq |\n| `agent_executions` (real CEA history) | **31** | count=exact |\n| Existing seeders (drift) | RPC `seed_crew_template` (6/squad) \u00b7 `seedEnterpriseStructure()` store (6) \u00b7 `deployEnterpriseToSupabase()` (12) | code read |\n| Existing real-work plumbing | CEA v1.1 \u2014 `agent_executions`, `agent-task-execute`, `agent-daily-pulse`, `agent_pricing`, `useAgentActivity`, `/dashboard/agent-economics` | docs/processes/constellation-economic-activation.md |\n\n---\n\n## Architecture Decisions (Sovereign-delegated \"tome os caminhos\")\n\n| Fork | Decision | Rationale |\n|------|----------|-----------|\n| A \u2014 invoca\u00e7\u00e3o real | **A1**: reusar edge functions existentes como tools via camada fina de roteamento | m\u00f3dulos j\u00e1 robustos; n\u00e3o reescrever |\n| B \u2014 modelo de acesso | **B**: config de acesso pr\u00e9-configurada por subagente (m\u00f3dulo + BYOK + caps) | \"acesso configurado previamente\" (diretiva Sovereign) |\n| C \u2014 escopo do v2 | **C**: refatorar in-place atr\u00e1s de um reset limpo de dados | 1 user real + \u00e9 casca; rota paralela \u00e9 overhead |\n\n---\n\n## Open Technical Decisions (consolidated from 05-sdd.md)\n\n| OTD ID | Description | Recommendation | Status |\n|--------|-------------|----------------|--------|\n| OTD-CV2-001 | Reuso de `crew_agents`/`crew_edges` vs. tabelas v2 novas | Estender `crew_agents` + nova `agent_capabilities` (migra\u00e7\u00e3o in-place) | Open \u2192 Sovereign |\n| OTD-CV2-002 | Planejamento LLM (tool-calling) vs. binding direto 1-capability-1-fun\u00e7\u00e3o | Fase 1 = binding direto; Fase 2 = tool-calling LLM | Open |\n| OTD-CV2-003 | Caps de consumo: por-agente vs. por-capability vs. por-API | H\u00edbrido: cap di\u00e1rio por-user/API (estende canvas-daily-cap) + cap por-agente | Open |\n| OTD-CV2-004 | Destino dos 31 `agent_executions` \u00f3rf\u00e3os no reset | Arquivar em `agent_executions_archive` antes do wipe | Open |\n| OTD-CV2-005 | `provider/model` default dos subagentes | `groq/llama-3.3-70b-versatile` (v\u00e1lido em `agent_pricing`) | Recommended |\n| OTD-CV2-006 | Publica\u00e7\u00e3o Social: 1 subagente multi-rede vs. N | 1 subagente roteando p/ publish-meta/social/wordpress | Open |\n| OTD-CV2-007 | Render 3D: manter R3F vs. degradar p/ 2D em baixa perf | Manter R3F + LOD + cap de n\u00f3s por tenant (\u226421) | Recommended |\n| OTD-CV2-008 | Watchdog/Infra subagente: read-only ou pode acionar self-heal | Read-only no tenant (sem acesso a system) \u2014 s\u00f3 l\u00ea `infra_health_logs` do pr\u00f3prio escopo | Open |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/00-index.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:44:58)*


## 🤖 Claude *(02:45:49)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/01-mrd.md",
  "content": "# MRD \u2014 Market Requirements Document\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)\n**Status:** Draft\n\n---\n\n## 1. Executive Summary\n\nCriadores de conte\u00fado e pequenos neg\u00f3cios que monetizam via afiliados operam hoje 10+ ferramentas desconexas (descoberta de tend\u00eancias, gera\u00e7\u00e3o de conte\u00fado, design, publica\u00e7\u00e3o, links de afiliado, analytics). O MCORCH j\u00e1 possui esses m\u00f3dulos \u2014 e robustos \u2014 mas eles s\u00e3o acionados **manualmente, um a um**. A Constela\u00e7\u00e3o 3D (`/dashboard/constellation`) prometia um ex\u00e9rcito de agentes, mas nasceu como **casca decorativa do Lovable**: 717 agentes-fantasma (26 donos \u00f3rf\u00e3os, sem perfil) que apenas piscavam status. A `constellation-v2` converte essa casca no que ela deveria ser: um **cockpit operacional per-user** onde uma crew de agentes executa o trabalho real dos m\u00f3dulos em nome do usu\u00e1rio \u2014 com isolamento de tenant duro, economia mcoCoins medida e credenciais BYOK do pr\u00f3prio usu\u00e1rio. O momento \u00e9 agora: os m\u00f3dulos existem, o tool-calling de LLMs amadureceu, e a funda\u00e7\u00e3o econ\u00f4mica (CEA v1.1 \u2014 `agent_executions` + `agent-task-execute` + `agent_pricing`) j\u00e1 est\u00e1 viva em produ\u00e7\u00e3o.\n\n---\n\n## 2. Market Problem Statement\n\n### 2.1 Current State\nO criador/afiliado solo gasta a maior parte do tempo em **troca de contexto**: abre o minerador de tend\u00eancias, copia para a ferramenta de conte\u00fado, gera arte em outra, publica em tr\u00eas redes manualmente, encurta links de afiliado num quarto servi\u00e7o, e tenta ler analytics num quinto. N\u00e3o existe uma camada \"fa\u00e7a o trabalho por mim\" que componha tudo com as credenciais e o or\u00e7amento do pr\u00f3prio usu\u00e1rio.\n\n### 2.2 Root Cause Analysis\nAs ferramentas s\u00e3o **point-solutions**: cada uma resolve um peda\u00e7o, nenhuma orquestra o fluxo per-tenant. Builders gen\u00e9ricos de agentes (no-code) n\u00e3o t\u00eam integra\u00e7\u00e3o vertical com m\u00f3dulos de conte\u00fado/afiliado nem economia nativa. No pr\u00f3prio MCORCH, a camada de agentes existia s\u00f3 como **teatro visual** \u2014 `useSimulation` flipava status aleat\u00f3rio; n\u00e3o havia binding a fun\u00e7\u00e3o real, nem isolamento, nem controle de custo por usu\u00e1rio.\n\n### 2.3 Desired State\nUm \u00fanico cockpit onde o usu\u00e1rio **pr\u00e9-configura** uma crew enxuta (4 departamentos \u00d7 at\u00e9 4 subagentes m\u00f3dulo-bound + um Core orquestrador), cada subagente com acesso a um m\u00f3dulo real, chave BYOK e teto de consumo. Os agentes executam tarefas reais (minerar tend\u00eancias, gerar conte\u00fado, renderizar canvas, publicar, forjar links de afiliado, ler analytics), cada a\u00e7\u00e3o medida em mcoCoins, tudo escopado 100% \u00e0 conta do usu\u00e1rio.\n\n---\n\n## 3. Target Market Segments\n\n| Segment | Description | Size Estimate | Urgency | Accessibility |\n|---------|-------------|---------------|---------|---------------|\n| Primary | Criadores/afiliados solo que monetizam conte\u00fado (creator-economy BR/LatAm) | SAM ~2\u20134M criadores LatAm | High | Self-serve via signup + BYOK |\n| Secondary | Pequenas ag\u00eancias/SMBs gerindo m\u00faltiplas marcas | ~200k SMBs LatAm | Medium | Sales-assisted + plano Enterprise |\n\n### 3.1 TAM / SAM / SOM\n\n| Metric | Value | Basis |\n|--------|-------|-------|\n| TAM | ~50M criadores globais monetizando | Estimativas de creator-economy (ordem de grandeza) |\n| SAM | ~2\u20134M criadores LatAm/PT-BR com inten\u00e7\u00e3o de afilia\u00e7\u00e3o | Foco lingu\u00edstico/regional do MCORCH |\n| SOM (12m) | ~1.000\u20135.000 contas ativas | Capacidade realista de aquisi\u00e7\u00e3o na fase Usu\u00e1rio Zero \u2192 Usu\u00e1rio N |\n\n> **Nota de honestidade (Lei 1):** n\u00fameros de mercado s\u00e3o estimativas de ordem de grandeza para enquadrar prioridade, N\u00c3O proje\u00e7\u00f5es auditadas. O dado material hoje \u00e9 **1 usu\u00e1rio real** (Sovereign). A v2 \u00e9 pr\u00e9-requisito t\u00e9cnico para escalar al\u00e9m de 1.\n\n---\n\n## 4. Competitive Landscape\n\n| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |\n|------------|-------------|-----------|------------|---------------------|\n| Builders no-code de agentes (gen\u00e9ricos) | \"monte seu agente\" | flex\u00edvel, hype | sem m\u00f3dulos verticais, sem economia, sem afilia\u00e7\u00e3o | m\u00f3dulos prontos + economia mcoCoins nativa + BYOK |\n| Ferramentas verticais de conte\u00fado (ex.: geradores de post) | \"escreva mais r\u00e1pido\" | foco, qualidade de copy | single-purpose, sem orquestra\u00e7\u00e3o nem afiliados | crew multi-m\u00f3dulo orquestrada por departamento |\n| VA humano / ag\u00eancia | \"terceirize a opera\u00e7\u00e3o\" | julgamento humano | caro, n\u00e3o escala, sem isolamento de credenciais | agentes 24/7 cost-controlled per-tenant |\n\n---\n\n## 5. Market Opportunity & Timing\n\nTr\u00eas curvas convergem: (1) **tool-calling de LLMs** virou commodity confi\u00e1vel (Groq/OpenRouter baratos); (2) **os m\u00f3dulos j\u00e1 existem e est\u00e3o robustos** no MCORCH (orchestrate-content, canvas-execute, fetch-trends, link-forge, publish-*); (3) **a funda\u00e7\u00e3o econ\u00f4mica est\u00e1 viva** \u2014 a CEA v1.1 j\u00e1 mede execu\u00e7\u00f5es reais de agente em mcoCoins. Falta s\u00f3 a camada que falava-se desde o in\u00edcio: transformar a constela\u00e7\u00e3o decorativa em motor operacional per-tenant. Construir agora aproveita ativos j\u00e1 pagos em vez de reescrever.\n\n---\n\n## 6. Market Requirements\n\n> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**\n\n| ID | Market Requirement | Priority | Rationale | Source |\n|----|-------------------|----------|-----------|--------|\n| MR-CV2-001 | Agentes executam **trabalho real** nos m\u00f3dulos (n\u00e3o demo visual) | Critical | \u00c9 a raz\u00e3o de existir do v2; sem isso continua teatro | Diretiva Sovereign 2026-05-31 |\n| MR-CV2-002 | **Isolamento de tenant duro** \u2014 agentes escopados \u00e0 conta do user; ZERO acesso ao sistema/dev MCORCH ou a outros tenants | Critical | Seguran\u00e7a + LGPD + condi\u00e7\u00e3o de multi-tenancy; diretiva expl\u00edcita \"isso n\u00e3o pode acontecer\" | Diretiva Sovereign |\n| MR-CV2-003 | **Controle de custo per-user**: mcoCoins medido + BYOK + caps de consumo por API | Critical | Risco financeiro isolado por tenant; evita um user esgotar quota global | Diretiva Sovereign + API Tenancy Model |\n| MR-CV2-004 | **Empty-start**: novos usu\u00e1rios nascem sem agentes; crew criada on-demand | High | Fim da polui\u00e7\u00e3o decorativa (688 linhas-lixo); UX intencional | Diretiva Sovereign |\n| MR-CV2-005 | **Cockpit unificado** cobrindo os 16 capabilities (4\u00d74) com hierarquia Leads\u2192Core | High | Cobertura de todo o ecossistema num s\u00f3 lugar | Diretiva Sovereign + mapa 4\u00d74 aprovado |\n| MR-CV2-006 | **Observabilidade** do trabalho dos agentes (live logs + dashboard de economia) | Medium | Confian\u00e7a + calibra\u00e7\u00e3o de margem | CEA v1.1 + ProdBOK |\n| MR-CV2-007 | **Performance** do cockpit 3D (render suave, sem z-index quebrado) | Medium | Casca atual mata perf com 53+ n\u00f3s e tem bugs de layering | Observa\u00e7\u00e3o visual Sovereign (screenshot) |\n\n---\n\n## 7. Success Metrics (Market-Level KPIs)\n\n| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |\n|-----|-----------|------------------|-------------------|-------------|\n| Activation | % de contas ativas com \u22651 subagente que executou tarefa real | 60% | 80% | `agent_executions` por user |\n| Agent throughput | execu\u00e7\u00f5es reais de agente por user ativo / semana | \u2265 10 | \u2265 30 | `agent_executions` count |\n| Economic activation | mcoCoins consumidos via execu\u00e7\u00e3o de agente / m\u00eas | > 0 (material) | crescimento MoM | `mcoin_transactions` action=`*_spend` |\n| Task success rate | % execu\u00e7\u00f5es `status=done` (vs failed/timeout) | \u2265 90% | \u2265 95% | `agent_executions.status` |\n\n---\n\n## 8. Regulatory & Compliance Context\n\n| Regulation | Applicability | Key Constraint | Compliance Owner |\n|------------|---------------|----------------|-----------------|\n| LGPD | Sim \u2014 dados per-user + credenciais BYOK | Credenciais cifradas, escopadas por `auth.uid()`, revog\u00e1veis pelo user; agentes n\u00e3o vazam dados entre tenants; direito ao esquecimento cascateia para crew + execu\u00e7\u00f5es | Engineering |\n| API Tenancy Model (diretiva interna) | Sim \u2014 toda chamada a API externa resolve credencial per-user | Sem `Deno.env` global em fluxo user-facing; BYOK primeiro, fallback restrito | Engineering |\n\n---\n\n## 9. Traceability Matrix Stub\n\n| MR ID | \u2192 BR ID | Rationale |\n|-------|---------|-----------|\n| MR-CV2-001 | BR-CV2-001 | invoca\u00e7\u00e3o real de m\u00f3dulo |\n| MR-CV2-002 | BR-CV2-002 | isolamento de tenant |\n| MR-CV2-003 | BR-CV2-003 | economia + BYOK + caps |\n| MR-CV2-004 | BR-CV2-004 | empty-start |\n| MR-CV2-005 | BR-CV2-005 | cockpit 4\u00d74 + hierarquia |\n| MR-CV2-006 | BR-CV2-006 | observabilidade |\n| MR-CV2-007 | BR-CV2-007 | performance 3D |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/01-mrd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:45:53)*


## 🤖 Claude *(02:46:57)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/02-brd.md",
  "content": "# BRD \u2014 Business Requirements Document\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)\n**Status:** Draft\n\n---\n\n## 1. Executive Summary\n\nA `constellation-v2` transforma a constela\u00e7\u00e3o 3D de **custo** (casca decorativa que mata performance e n\u00e3o gera nada) em **motor de receita**: cada usu\u00e1rio opera uma crew enxuta de agentes que executam trabalho real nos m\u00f3dulos do MCORCH, consumindo mcoCoins por a\u00e7\u00e3o e usando credenciais BYOK pr\u00f3prias. O retorno de neg\u00f3cio \u00e9 triplo: (1) **consumo mcoCoins** direto por execu\u00e7\u00e3o de agente; (2) **receita de afiliado** amplificada por agentes que forjam links e publicam autonomamente; (3) **prontid\u00e3o multi-tenant** \u2014 isolamento + BYOK + caps s\u00e3o pr\u00e9-condi\u00e7\u00e3o para vender al\u00e9m do Usu\u00e1rio Zero. Constr\u00f3i-se sobre a CEA v1.1 (j\u00e1 viva), reusando edge functions robustas via uma camada fina de roteamento de capability.\n\n---\n\n## 2. Business Objectives (SMART)\n\n| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |\n|----|-----------|----------|------------|------------|----------|------------|\n| BO-CV2-001 | Ativar a constela\u00e7\u00e3o economicamente | Converter agentes decorativos em executores que consomem mcoCoins | mcoCoins consumidos via `agent_executions` > 0 e crescente | Sim \u2014 CEA v1.1 j\u00e1 mede execs | Liga receita ao produto-core | 30 dias p\u00f3s-launch v2 |\n| BO-CV2-002 | Atingir prontid\u00e3o multi-tenant | Isolamento de tenant + BYOK + caps audit\u00e1veis | Security-review passa; 0 acesso cross-tenant em auditoria | Sim \u2014 RLS + API Tenancy j\u00e1 s\u00e3o padr\u00e3o | Desbloqueia Usu\u00e1rio 1..N | v2 GA |\n| BO-CV2-003 | Reduzir fric\u00e7\u00e3o operacional do criador | Substituir opera\u00e7\u00e3o manual de 10+ ferramentas por crew orquestrada | \u2265 10 execu\u00e7\u00f5es de agente / user ativo / semana | Sim \u2014 m\u00f3dulos j\u00e1 existem | Reten\u00e7\u00e3o + valor percebido | 90 dias p\u00f3s-launch |\n\n---\n\n## 3. Stakeholder Register\n\n| ID | Role | Interest | Influence | Communication Cadence | Contact |\n|----|------|----------|-----------|----------------------|---------|\n| SH-CV2-001 | Sovereign / Maestro | High | High | Continuous | Gabriel Zarattini |\n| SH-CV2-002 | End User (criador/afiliado, prim\u00e1rio) | High | Medium | NPS mensal + in-app | Usu\u00e1rio Zero \u2192 N |\n| SH-CV2-003 | Ag\u00eancia/SMB (secund\u00e1rio) | Medium | Low (hoje) | Trimestral | futuro |\n| SH-CV2-004 | OpenClaw Pantheon (agentes de DEV \u2014 engineer/scientist/etc.) | Medium | Medium | via mesh bridge | distinto dos agentes de produto \u2014 **N\u00c3O confundir** |\n\n> **SH-CV2-004 \u00e9 a fronteira cr\u00edtica:** os agentes do Pantheon OpenClaw operam o **sistema/dev** (este repo). Os agentes da constela\u00e7\u00e3o-v2 operam a **conta do tenant**. S\u00e3o universos disjuntos; o v2 pro\u00edbe arquiteturalmente que um agente de produto acesse o sistema (BR-CV2-002).\n\n---\n\n## 4. Business Requirements\n\n> Cada BR tra\u00e7a a \u22651 MR. mcoCoins definido onde a a\u00e7\u00e3o consome recurso.\n\n| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |\n|----|-------------|-----------|----------|---------------|---------------------|\n| BR-CV2-001 | Cada subagente invoca a fun\u00e7\u00e3o real do seu m\u00f3dulo via camada de roteamento de capability | MR-CV2-001 | Critical | Vari\u00e1vel por capability (ver \u00a76) | Clicar \"executar\" num subagente Viral Miner cria 1 row real em `agent_executions` + chama `fetch-trends` e retorna dados reais |\n| BR-CV2-002 | Isolamento de tenant duro: RLS `auth.uid()` em todas as tabelas de crew/execu\u00e7\u00e3o; allowlist de capabilities; **denylist de acesso a sistema** | MR-CV2-002 | Critical | 0 | Auditoria: nenhum agente l\u00ea/escreve dados de outro `user_id`; nenhuma capability mapeia a fun\u00e7\u00e3o de sistema/dev |\n| BR-CV2-003 | Resolu\u00e7\u00e3o BYOK per-user + caps de consumo por user/API + dedu\u00e7\u00e3o at\u00f4mica mcoCoins | MR-CV2-003 | Critical | medido | Execu\u00e7\u00e3o resolve chave de `user_api_keys`; estoura cap \u2192 HTTP 402; custo debitado via `deduct_mco_coins` (Sovereign freebie) |\n| BR-CV2-004 | Novos usu\u00e1rios nascem com constela\u00e7\u00e3o vazia; cria\u00e7\u00e3o on-demand | MR-CV2-004 | High | 0 | Signup novo \u2192 `crew_agents` count = 0; wizard cria crew sob demanda |\n| BR-CV2-005 | Topologia 4 deptos \u00d7 \u22644 subagentes m\u00f3dulo-bound + GCRUX Core; Leads reportam ao Core | MR-CV2-005 | High | 0 | Mapa 4\u00d74 renderizado; edges `Directive` Core\u2192Lead e `Reporting` Lead\u2192subagente |\n| BR-CV2-006 | Observabilidade: feed de execu\u00e7\u00f5es reais (live logs) + dashboard de economia | MR-CV2-006 | Medium | 0 | `useAgentActivity` projeta execs; `/dashboard/agent-economics` mostra tokens/USD/mcoCoins por squad |\n| BR-CV2-007 | Performance do cockpit 3D: render suave + z-index correto + cap de n\u00f3s/tenant | MR-CV2-007 | Medium | 0 | \u226421 n\u00f3s/tenant; 60fps alvo; pain\u00e9is sem sobreposi\u00e7\u00e3o quebrada |\n\n---\n\n## 5. ROI Model\n\n### 5.1 Cost Estimates\n\n| Cost Item | Type | Monthly Estimate | Annual Estimate |\n|-----------|------|-----------------|----------------|\n| Infra (Supabase, Docker mesh) | OpEx | sem incremento material (reusa stack) | \u2014 |\n| AI API calls | Variable | **BYOK \u2014 custo do tenant**, n\u00e3o do MCORCH | \u2014 |\n| AI API (fallback global Sovereign freebie) | Variable | baixo (cap `max_tokens=500` + groq) | \u2014 |\n| Desenvolvimento v2 | CapEx | \u2014 | esfor\u00e7o de ~1 sprint (refactor in-place) |\n\n> **Insight de modelo de neg\u00f3cio:** por ser **BYOK**, o custo vari\u00e1vel de IA migra para o tenant \u2014 o MCORCH cobra a **camada de orquestra\u00e7\u00e3o em mcoCoins**, n\u00e3o a infer\u00eancia. Margem limpa.\n\n### 5.2 Revenue Streams\n\n| Stream | Model | Monthly Potential | Notes |\n|--------|-------|-----------------|-------|\n| Consumo mcoCoins por execu\u00e7\u00e3o de agente | transaction | proporcional a # execs \u00d7 custo m\u00e9dio | core do v2 |\n| Receita de afiliado (links forjados por agentes) | revenue-share | proporcional a convers\u00f5es ML | amplificado por automa\u00e7\u00e3o |\n| Upgrade de plano (mais mcoCoins/caps) | subscription | Starter 500 / Pro 2000 / Ent 10k | gatilho: usu\u00e1rio esgota cap |\n\n### 5.3 Payback Analysis\n\n| Metric | Value |\n|--------|-------|\n| Break-even | N/A formal \u2014 reusa infra existente; payback = esfor\u00e7o de 1 sprint vs. ativa\u00e7\u00e3o de consumo |\n| 12-month ROI | Qualitativo: desbloqueia toda a tese multi-tenant (sem v2, receita per-tenant \u00e9 0) |\n| IRR | N/A (est\u00e1gio Usu\u00e1rio Zero) |\n\n---\n\n## 6. mcoCoins Economics\n\n| Operation (capability) | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |\n|-----------|-----------|-------------------|-----------------------|----------------------|\n| LLM-planning step (qualquer subagente, groq pilot) | 1 (floor) via `calc_agent_cost_mcoin` | Starter(500)/Pro(2000)/Ent(10k) | alto | base |\n| Conte\u00fado / Blog (generate-content) | ~1\u201310 conforme tokens | idem | m\u00e9dio | m\u00e9dio |\n| Canvas Studio (imagem) | conforme `agent_pricing` + surcharge | idem | m\u00e9dio | m\u00e9dio |\n| Canvas Studio (v\u00eddeo DoP) | **125** (precedente real `canvas_video_spend`) | idem | baixo | alto unit\u00e1rio |\n| Orquestra\u00e7\u00e3o (orchestrate-content) | **10** (custo de pipeline existente) | idem | m\u00e9dio | alto |\n| Viral Miner (fetch-trends) | ~1\u20135 | idem | alto | m\u00e9dio |\n| Afiliados (link-forge) | ~1 | idem | m\u00e9dio | baixo (mas gera receita afiliado) |\n\n> Custo SEMPRE via RPC `calc_agent_cost_mcoin` + `deduct_mco_coins` (at\u00f4mico). Nunca hardcoded client-side. Sovereign = admin freebie (`sovereign_freebie=true`).\n\n---\n\n## 7. Constraints & Assumptions\n\n### Constraints\n- Reusar edge functions existentes (decis\u00e3o A1) \u2014 n\u00e3o reescrever m\u00f3dulos.\n- Refactor in-place (decis\u00e3o C) \u2014 sem rota `/constellation-v2` paralela.\n- Provider/model dos subagentes deve casar com `agent_pricing` (hoje h\u00e1 drift: Anthropic sem endpoint, \"Llama 3\" sem pricing \u2192 corrigir).\n- LGPD: credenciais BYOK cifradas e revog\u00e1veis; reset cascateia.\n\n### Assumptions\n- O usu\u00e1rio fornece suas pr\u00f3prias chaves (BYOK) por capability que precise de IA/servi\u00e7o externo.\n- O Sovereign opera em modo admin freebie (n\u00e3o debita) por design.\n- A maioria dos capabilities mapeia 1:1 a uma edge function j\u00e1 deployada.\n\n---\n\n## 8. Business Risk Register\n\n| Risk ID | Description | Probability | Impact | RPN | Mitigation |\n|---------|-------------|-------------|--------|-----|------------|\n| BR-RISK-CV2-001 | Vazamento cross-tenant (agente l\u00ea dados de outro user) | 2 | 5 | 10 | RLS `auth.uid()` default-deny + allowlist capability + security-review obrigat\u00f3rio |\n| BR-RISK-CV2-002 | Agente de produto ganha acesso ao sistema/dev (confus\u00e3o de escopo) | 2 | 5 | 10 | Denylist arquitetural: capabilities mapeiam s\u00f3 a fun\u00e7\u00f5es tenant-scoped; nenhuma a shell/repo/service-role |\n| BR-RISK-CV2-003 | Custo descontrolado (loop de execu\u00e7\u00e3o / tokens) | 3 | 4 | 12 | `max_tokens` cap + caps de consumo por user/API + dedu\u00e7\u00e3o at\u00f4mica + circuit breaker |\n| BR-RISK-CV2-004 | Reset apaga dados reais (execu\u00e7\u00f5es/perfil) por engano | 2 | 4 | 8 | Arquivar 31 execs antes do wipe (OTD-CV2-004); purge filtrado por owners \u00f3rf\u00e3os; backup |\n| BR-RISK-CV2-005 | Drift provider/model \u2192 execu\u00e7\u00e3o falha silenciosa | 3 | 3 | 9 | Default `groq/llama-3.3-70b-versatile` v\u00e1lido + `assertExecuteSuccess` (j\u00e1 existe) |\n| BR-RISK-CV2-006 | BYOK key inv\u00e1lida/revogada do tenant | 3 | 2 | 6 | Fail-closed HTTP 402/501 estruturado + banner UI link p/ settings |\n\n> Probability & Impact: 1=Low, 5=High. RPN = Probability \u00d7 Impact.\n\n---\n\n## 9. Business Acceptance Criteria\n\n| ID | Criterion | Verification Method |\n|----|-----------|-------------------|\n| BAC-CV2-001 | Um subagente m\u00f3dulo-bound executa a fun\u00e7\u00e3o real do m\u00f3dulo e retorna resultado material | E2E: criar subagente Viral Miner \u2192 executar \u2192 row `agent_executions` done + payload real de `fetch-trends` |\n| BAC-CV2-002 | Novo usu\u00e1rio n\u00e3o v\u00ea nenhum agente at\u00e9 criar | E2E: signup \u2192 `crew_agents` count=0 |\n| BAC-CV2-003 | Custo debitado corretamente; Sovereign n\u00e3o \u00e9 cobrado | REST: `mco_balance` do tenant cai pelo custo; Sovereign inalterado |\n| BAC-CV2-004 | Auditoria de isolamento: 0 acesso cross-tenant e 0 capability de sistema | Security-review + query de RLS + revis\u00e3o do registry de capabilities |\n| BAC-CV2-005 | Performance: cockpit renderiza \u226421 n\u00f3s suave, sem z-index quebrado | E2E UI audit 1920\u00d71080 (skill `e2e-user-zero-audit`) |\n\n---\n\n## 10. Traceability Matrix\n\n| MR ID | BR ID | PR ID (stub) |\n|-------|-------|--------------|\n| MR-CV2-001 | BR-CV2-001 | PR-CV2-001, PR-CV2-002 |\n| MR-CV2-002 | BR-CV2-002 | PR-CV2-003 |\n| MR-CV2-003 | BR-CV2-003 | PR-CV2-004 |\n| MR-CV2-004 | BR-CV2-004 | PR-CV2-005 |\n| MR-CV2-005 | BR-CV2-005 | PR-CV2-006, PR-CV2-007 |\n| MR-CV2-006 | BR-CV2-006 | PR-CV2-010 |\n| MR-CV2-007 | BR-CV2-007 | PR-CV2-011 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/02-brd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:47:03)*


## 🤖 Claude *(02:47:04)*

**Fase 1 selada** (MRD + BRD). Autorando **Fase 2** (PRD — ProdBOK + CXBOK):

## 🤖 Claude *(02:48:05)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/03-prd.md",
  "content": "# PRD \u2014 Product Requirements Document\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** ProdBOK + CXBOK\n**Status:** Draft\n\n---\n\n## 1. Product Vision Statement\n\n> Para o **criador/afiliado** que perde o dia trocando de ferramenta, a **Constela\u00e7\u00e3o v2** \u00e9 um **cockpit de agentes per-user** que executa o trabalho real dos m\u00f3dulos (conte\u00fado, canvas, tend\u00eancias, publica\u00e7\u00e3o, afiliados, analytics) sob seu comando e seu or\u00e7amento. Diferente de builders de agentes gen\u00e9ricos, nossos agentes j\u00e1 v\u00eam integrados aos m\u00f3dulos, medidos em mcoCoins e isolados na conta do usu\u00e1rio.\n\n---\n\n## 2. User Personas\n\n### Persona 1 \u2014 L\u00e9o, o Criador-Afiliado Solo (Primary)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Criador de conte\u00fado que monetiza via afiliados (Mercado Livre, etc.) |\n| Goals | Produzir+publicar+monetizar mais, com menos tempo manual; controlar custo de IA |\n| Frustrations | 10+ ferramentas desconexas; medo de estourar custo de API; setup repetitivo |\n| Tech-savviness | 3/5 \u2014 usa ferramentas, n\u00e3o programa; entende \"chave de API\" e \"saldo\" |\n| MCORCH usage pattern | Entra no cockpit, manda a crew minerar+gerar+publicar, acompanha logs e saldo |\n| Quote | _\"Eu quero dizer 'vai' e a constela\u00e7\u00e3o trabalhar \u2014 sem eu abrir cinco abas e estourar minha cota.\"_ |\n\n### Persona 2 \u2014 Marina, a Gestora de Pequena Ag\u00eancia (Secondary)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Gere m\u00faltiplas marcas/contas de clientes |\n| Goals | Escalar opera\u00e7\u00e3o sem contratar; isolar custo e credenciais por marca |\n| Frustrations | Risco de misturar credenciais entre clientes; sem teto de gasto por conta |\n| Tech-savviness | 4/5 |\n| MCORCH usage pattern | Configura crews por conta, define caps de consumo, audita economia por squad |\n| Quote | _\"Cada cliente tem que ter sua pr\u00f3pria crew, sua pr\u00f3pria chave e seu pr\u00f3prio teto \u2014 sem vazar nada entre eles.\"_ |\n\n---\n\n## 3. User Journey Maps\n\n### Journey: Primeira Crew Operacional (L\u00e9o, Happy Path)\n\n| Stage | Action | Touchpoint | Emotion | Opportunity |\n|-------|--------|-----------|---------|-------------|\n| Awareness | Abre `/dashboard/constellation` rec\u00e9m-criada (vazia) | Cockpit 3D vazio + CTA \"Criar minha crew\" | \ud83d\ude10 Neutral | Onboarding wizard claro |\n| Consideration | Wizard sugere os 4 deptos + mapa 4\u00d74 | Wizard/NodePalette | \ud83e\udd14 Curious | Pr\u00e9-config de m\u00f3dulo+BYOK por subagente |\n| Activation | Cria Lead + 1 subagente (ex.: Viral Miner) e binda chave BYOK | AgentDetail/config | \ud83d\ude0a Excited | Valida\u00e7\u00e3o de chave inline |\n| Value | Clica \"Executar\" \u2192 agente minera tend\u00eancias reais; v\u00ea log + custo mcoCoins | Live Logs + status 3D | \ud83d\ude80 Delighted | \"Run squad\" em cadeia |\n| Retention | Crew roda di\u00e1rio (pulse) e entrega resultados; saldo controlado | Dashboard de economia | \u2764\ufe0f Loyal | Caps + alertas de saldo |\n\n#### Edge Case 1: Chave BYOK ausente/revogada\n> Subagente sem chave v\u00e1lida \u2192 execu\u00e7\u00e3o fail-closed (HTTP 402/501) \u2192 toast PT-BR + banner com link para `/dashboard/settings`. Nenhuma cobran\u00e7a; nenhum fallback silencioso para chave global.\n\n#### Edge Case 2: Cap de consumo atingido\n> Execu\u00e7\u00e3o excede o cap di\u00e1rio do user/API \u2192 HTTP 402 estruturado \u2192 toast \"Limite di\u00e1rio deste m\u00f3dulo atingido\" \u2192 agente volta a `idle`, saldo intacto.\n\n### Journey: Isolamento por Marca (Marina, Happy Path resumido)\nCria crews separadas (futuro: por `project_id`); cada uma com BYOK e caps pr\u00f3prios; auditoria de economia por squad. Garantia: zero acesso cruzado (RLS).\n\n---\n\n## 4. Feature Inventory (MoSCoW)\n\n> Effort: S=horas, M=dias, L=semana, XL=sprint\n\n### Must Have (MVP)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-CV2-001 | **Capability invocation** \u2014 subagente executa fun\u00e7\u00e3o real do m\u00f3dulo via roteador | P1,P2 | BR-CV2-001 | L | vari\u00e1vel | reusa edge functions (A1) |\n| PR-CV2-002 | **Crew on-demand creation** \u2014 criar Lead/subagente m\u00f3dulo-bound | P1,P2 | BR-CV2-001 | M | 0 | extends \"+ Agente\" / wizard |\n| PR-CV2-003 | **Tenant isolation hard** \u2014 RLS + capability allowlist + system denylist | P1,P2 | BR-CV2-002 | M | 0 | security-critical |\n| PR-CV2-004 | **Cost control** \u2014 BYOK resolve + caps + dedu\u00e7\u00e3o at\u00f4mica | P1,P2 | BR-CV2-003 | L | medido | estende canvas-daily-cap + CEA |\n| PR-CV2-005 | **Empty-start** \u2014 remover auto-seed; signup vazio | P1,P2 | BR-CV2-004 | S | 0 | drop RPC auto-call |\n| PR-CV2-006 | **4\u00d74 capability map** \u2014 registry dos 16 capabilities por depto | P1,P2 | BR-CV2-005 | M | 0 | seed on-demand |\n| PR-CV2-007 | **Hierarchy Leads\u2192Core** \u2014 edges Directive/Reporting + render | P1 | BR-CV2-005 | S | 0 | j\u00e1 \u00e9 a topologia base |\n\n### Should Have (v1.0)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-CV2-010 | **Observabilidade v2** \u2014 live logs reais + economia por squad | P1,P2 | BR-CV2-006 | M | 0 | extends `useAgentActivity` |\n| PR-CV2-011 | **Performance/UX 3D** \u2014 cap n\u00f3s, LOD, fix z-index | P1 | BR-CV2-007 | M | 0 | resolve polui\u00e7\u00e3o atual |\n| PR-CV2-012 | **Access config UI** \u2014 por subagente: m\u00f3dulo + BYOK + caps | P1,P2 | BR-CV2-003 | M | 0 | \"acesso pr\u00e9-configurado\" |\n| PR-CV2-013 | **Run Squad / Run All** \u2014 disparo em cadeia BFS pela hierarquia | P1 | BR-CV2-001 | M | soma | reusa padr\u00e3o Canvas Run-All |\n\n### Could Have (Future)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-CV2-020 | **LLM tool-calling planner** \u2014 Core decide quais capabilities acionar | P1 | BR-CV2-001 | XL | vari\u00e1vel | evolu\u00e7\u00e3o de A1\u2192A2 (OTD-CV2-002) |\n| PR-CV2-021 | **Cron aut\u00f4nomo por subagente** \u2014 agenda pr\u00f3pria al\u00e9m do daily-pulse | P1 | BR-CV2-006 | L | vari\u00e1vel | estende agent-daily-pulse |\n| PR-CV2-022 | **Multi-brand por `project_id`** \u2014 crews por marca (Marina) | P2 | BR-CV2-002 | L | 0 | multi-tenant avan\u00e7ado |\n\n### Won't Have (This Cycle)\n- Agentes de produto com qualquer acesso ao sistema/dev/repo MCORCH (proibido por design \u2014 BR-CV2-002).\n- Marketplace de agentes entre tenants.\n- Edi\u00e7\u00e3o visual livre de hierarquia fora do modelo 4 deptos \u00d7 \u22644 (mant\u00e9m o cap de performance).\n\n---\n\n## 5. Release Phasing\n\n### MVP Scope\n**Target:** sprint v2.0\n**Included:** PR-CV2-001..007\n**Success gate:** BAC-CV2-001 (execu\u00e7\u00e3o real) + BAC-CV2-002 (empty-start) + BAC-CV2-003 (custo correto) + BAC-CV2-004 (isolamento) verdes.\n\n### v1.0 Scope\n**Adds:** PR-CV2-010, 011, 012, 013\n**Success gate:** BAC-CV2-005 (E2E UI audit 1920\u00d71080 passa) + dashboard de economia por squad vivo.\n\n### Future Scope\n**Items:** PR-CV2-020+\n**Condition:** ap\u00f3s MVP+v1.0 est\u00e1veis e \u22651 ciclo de calibra\u00e7\u00e3o de `MARGIN_FACTOR`.\n\n---\n\n## 6. Luxury UX Specifications\n\n### 6.1 Color & Visual Identity\n\n| Token | Value | Usage |\n|-------|-------|-------|\n| `--bg-deep` | `#0A0A0F` | Fundo do cockpit 3D |\n| `--accent-violet` | `#7C3AED` | CTA prim\u00e1rio, estados ativos, edges animados |\n| `--accent-cyan` | `#06B6D4` | Highlights de dados, status \"thinking\" |\n| `--glass-surface` | `rgba(255,255,255,0.04)` | Pain\u00e9is (HUD, AgentDetail, Logs) |\n| `--border-subtle` | `rgba(255,255,255,0.08)` | Bordas de painel |\n\nCores por departamento (mantidas do v1): Content `#ec4899` \u00b7 Tech `#3b82f6` \u00b7 Market `#22c55e` \u00b7 Ops `#f59e0b`. Core = branco/teal central.\n\n### 6.2 Animation Guidelines\n\n| Element | Library | Duration | Easing |\n|---------|---------|----------|--------|\n| Entrada de n\u00f3 (3D) | R3F / drei | 500ms | `spring(stiffness:80)` |\n| Status pulse (thinking/running) | CSS keyframes | 2s | `ease-in-out infinite` |\n| Edge animado (execu\u00e7\u00e3o ativa) | R3F particles | cont\u00ednuo | linear |\n| Pain\u00e9is (HUD/AgentDetail) | Framer Motion | 150\u2013300ms | `easeOut` |\n\n### 6.3 Interaction Patterns\n- **Pain\u00e9is:** glass morphism (`backdrop-blur-sm`), borda sutil, z-index em camadas **estritas** (corrige o bug atual): canvas 3D (z-0) < edges/labels (z-10) < HUD/pain\u00e9is (z-40) < toasts/modais (z-50).\n- **CTAs:** gradiente no hover; \"Executar\" e \"Run Squad\" com destaque violeta.\n- **Loading:** skeleton shimmer; status 3D pulsa (n\u00e3o spinner).\n- **Toasts:** `sonner` \u2014 sucesso violeta, erro vermelho, saldo baixo \u00e2mbar (reusa `LOW_BALANCE_THRESHOLD`).\n\n### 6.4 Accessibility (WCAG 2.1 AA)\n- Contraste \u2265 4.5:1 em texto sobre glass.\n- Bot\u00f5es s\u00f3-\u00edcone do HUD com ARIA labels.\n- Navega\u00e7\u00e3o por teclado nos pain\u00e9is 2D (o canvas 3D \u00e9 gesture/mouse, com fallback de lista acess\u00edvel).\n- Foco vis\u00edvel \u2265 2px.\n\n---\n\n## 7. Acceptance Criteria (Gherkin)\n\n```gherkin\nFeature: Constellation v2 \u2014 agentes operacionais per-user\n\n  Scenario: Executar capability real (PR-CV2-001)\n    Given um subagente \"Viral Miner\" m\u00f3dulo-bound com chave BYOK v\u00e1lida e saldo suficiente\n    When o usu\u00e1rio clica \"Executar tarefa\"\n    Then uma row real \u00e9 criada em agent_executions com status running\u2192done\n    And a edge function fetch-trends \u00e9 invocada com a chave BYOK do usu\u00e1rio\n    And o custo \u00e9 debitado via deduct_mco_coins (Sovereign = freebie)\n    And o resultado material aparece nos Live Logs\n\n  Scenario: Empty-start de novo usu\u00e1rio (PR-CV2-005)\n    Given um usu\u00e1rio rec\u00e9m-cadastrado\n    When ele abre /dashboard/constellation\n    Then crew_agents.count para o user \u00e9 0\n    And um CTA \"Criar minha crew\" \u00e9 exibido (sem auto-seed)\n\n  Scenario: Isolamento de tenant (PR-CV2-003)\n    Given dois usu\u00e1rios A e B com crews pr\u00f3prias\n    When A executa qualquer capability\n    Then nenhuma row/credencial/execu\u00e7\u00e3o de B \u00e9 lida ou escrita\n    And nenhuma capability mapeia a fun\u00e7\u00e3o de sistema/dev/service-role\n\n  Scenario: Cap de consumo atingido (PR-CV2-004)\n    Given um subagente cujo cap di\u00e1rio de mcoCoins/API foi atingido\n    When o usu\u00e1rio clica \"Executar\"\n    Then a resposta \u00e9 HTTP 402 estruturado\n    And o saldo permanece intacto\n    And um toast PT-BR informa o limite\n```\n\n---\n\n## 8. Traceability Matrix\n\n| MR ID | BR ID | PR ID |\n|-------|-------|-------|\n| MR-CV2-001 | BR-CV2-001 | PR-CV2-001, PR-CV2-002, PR-CV2-013, PR-CV2-020 |\n| MR-CV2-002 | BR-CV2-002 | PR-CV2-003, PR-CV2-022 |\n| MR-CV2-003 | BR-CV2-003 | PR-CV2-004, PR-CV2-012 |\n| MR-CV2-004 | BR-CV2-004 | PR-CV2-005 |\n| MR-CV2-005 | BR-CV2-005 | PR-CV2-006, PR-CV2-007 |\n| MR-CV2-006 | BR-CV2-006 | PR-CV2-010, PR-CV2-021 |\n| MR-CV2-007 | BR-CV2-007 | PR-CV2-011 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/03-prd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:48:13)*


## 🤖 Claude *(02:48:14)*

**Fase 2 selada** (PRD). Autorando **Fase 3** (FRD + SDD — SWEBOK + CISSP CBK):

## 🤖 Claude *(02:49:15)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/04-frd.md",
  "content": "# FRD \u2014 Functional Requirements Document\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** SWEBOK v4 (Software Requirements)\n**Status:** Draft\n\n---\n\n## 1. Scope Statement\n\nEspecifica os requisitos funcionais e n\u00e3o-funcionais da `constellation-v2`. Deriva do PRD `03-prd.md` e alimenta o SDD `05-sdd.md`.\n\n**In scope:** camada de roteamento de capability (subagente\u2192fun\u00e7\u00e3o real do m\u00f3dulo), refactor `agent-task-execute` para capabilities, BYOK + caps de consumo, empty-start, registry 4\u00d74, hierarquia Leads\u2192Core, observabilidade, performance/UX 3D, reset/migra\u00e7\u00e3o de dados.\n**Out of scope:** reescrita dos m\u00f3dulos (reusados via A1), qualquer acesso de agente de produto ao sistema/dev, LLM tool-calling planner (Future PR-CV2-020), multi-brand `project_id` (Future PR-CV2-022).\n\n---\n\n## 2. Functional Requirements\n\n> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron`\n\n| ID | Title | Description | Priority | PR Traced | Category | Test ID |\n|----|-------|-------------|----------|-----------|----------|---------|\n| FR-CV2-001 | Capability registry | Tabela/registry mapeando `capability_key` \u2192 edge function alvo + schema de input + custo base + flag `requires_byok` | Critical | PR-CV2-001 | DB | AT-CV2-001 |\n| FR-CV2-002 | Capability router (edge) | `agent-task-execute` v2 resolve `capability_key` do subagente, valida JWT, resolve BYOK, checa cap, invoca a edge function alvo, mede custo, grava `agent_executions` | Critical | PR-CV2-001 | EdgeFunction | AT-CV2-002 |\n| FR-CV2-003 | Subagent \u2192 capability binding | `crew_agents` ganha `capability_key` (nullable; Leads/Core = null) | Critical | PR-CV2-001 | DB | AT-CV2-003 |\n| FR-CV2-004 | Execute hook v2 | `useAgentTask` envia `capability_key` + payload; trata 200/402/501 via `assertExecuteSuccess` | Critical | PR-CV2-001 | Hook | AT-CV2-004 |\n| FR-CV2-005 | Crew creation on-demand | UI/wizard cria Lead/subagente com depto + `capability_key`; insere edge `Reporting`/`Directive` | Critical | PR-CV2-002 | UI+Hook | AT-CV2-005 |\n| FR-CV2-006 | Stable agent keys | Seed usa keys est\u00e1veis (`core`, `lead-<dept>`, `agent-<dept>-<capability>`) para idempot\u00eancia e re-link de execs | High | PR-CV2-002 | DB | AT-CV2-006 |\n| FR-CV2-010 | RLS tenant isolation | Todas as tabelas (`crew_agents`, `crew_edges`, `agent_capabilities` user-scoped, `agent_consumption_caps`, `agent_executions`) com RLS `auth.uid()` default-deny | Critical | PR-CV2-003 | DB | AT-CV2-010 |\n| FR-CV2-011 | Capability allowlist | Router s\u00f3 executa `capability_key` presente no registry de produto; rejeita desconhecidos (422) | Critical | PR-CV2-003 | EdgeFunction | AT-CV2-011 |\n| FR-CV2-012 | System-access denylist | Nenhuma capability mapeia a fun\u00e7\u00e3o de sistema/dev/service-role/shell; router roda s\u00f3 com JWT de user (nunca service-role no path user-facing) | Critical | PR-CV2-003 | EdgeFunction | AT-CV2-012 |\n| FR-CV2-020 | BYOK resolution | Router resolve chave do provider/servi\u00e7o de `user_api_keys` por `auth.uid()`; fail-closed 402/501 se ausente | Critical | PR-CV2-004 | EdgeFunction | AT-CV2-020 |\n| FR-CV2-021 | Consumption caps | Cap di\u00e1rio por user/API (`agent_consumption_caps`) verificado antes da execu\u00e7\u00e3o; HTTP 402 estruturado ao estourar | Critical | PR-CV2-004 | EdgeFunction+DB | AT-CV2-021 |\n| FR-CV2-022 | Atomic metering | Custo via `calc_agent_cost_mcoin` + `deduct_mco_coins` (Sovereign freebie); grava `cost_mcoin`/`cost_usd_micro` em `agent_executions` | Critical | PR-CV2-004 | EdgeFunction | AT-CV2-022 |\n| FR-CV2-023 | Access config UI | Por subagente: habilitar m\u00f3dulo + bindar chave BYOK + definir caps | High | PR-CV2-012 | UI+Hook | AT-CV2-023 |\n| FR-CV2-030 | Remove auto-seed | `useCrewData` N\u00c3O chama mais `seed_crew_template` quando crew vazia; estado vazio \u00e9 v\u00e1lido | Critical | PR-CV2-005 | Hook | AT-CV2-030 |\n| FR-CV2-031 | Empty-state UX | Cockpit vazio mostra CTA \"Criar minha crew\" + wizard | High | PR-CV2-005 | UI | AT-CV2-031 |\n| FR-CV2-040 | 4\u00d74 capability map seed | Seed on-demand cria 4 Leads + N subagentes m\u00f3dulo-bound conforme mapa aprovado | High | PR-CV2-006 | DB+Hook | AT-CV2-040 |\n| FR-CV2-041 | Hierarchy edges | `Directive` Core\u2192Lead, `Reporting` Lead\u2192subagente; render 3D | High | PR-CV2-007 | DB+UI | AT-CV2-041 |\n| FR-CV2-050 | Activity feed v2 | `useAgentActivity` projeta execs reais (incl. capability/result) nos Live Logs + status 3D; economia por squad no dashboard | Medium | PR-CV2-010 | Hook+UI | AT-CV2-050 |\n| FR-CV2-060 | Render budget | Cap \u226421 n\u00f3s/tenant; LOD; remo\u00e7\u00e3o do loop de re-render (getState pattern preservado) | Medium | PR-CV2-011 | UI | AT-CV2-060 |\n| FR-CV2-061 | Z-index layering | Camadas estritas: canvas(0) < edges/labels(10) < HUD/pain\u00e9is(40) < toasts/modais(50) | Medium | PR-CV2-011 | UI | AT-CV2-061 |\n| FR-CV2-070 | Data reset/migration | Purga owners \u00f3rf\u00e3os + wipe crew Sovereign + arquiva 31 execs antes do wipe | High | BR-CV2-004 | DB | AT-CV2-070 |\n\n---\n\n## 3. Non-Functional Requirements\n\n| ID | Category | Requirement | Target | Measurement |\n|----|----------|-------------|--------|-------------|\n| NFR-CV2-001 | Performance | Render do cockpit 3D (\u226421 n\u00f3s) | 60fps alvo / \u226530fps piso | DevTools / E2E UI audit |\n| NFR-CV2-002 | Performance | Router edge p95 (excl. lat\u00eancia do m\u00f3dulo alvo) | < 800ms | Supabase logs |\n| NFR-CV2-003 | Scalability | Tenants concorrentes sem degrada\u00e7\u00e3o | \u2265 100 (alvo inicial) | Load test |\n| NFR-CV2-004 | Availability | Uptime do cockpit + router | 99.5%/m\u00eas | Watchdog telemetry |\n| NFR-CV2-005 | Maintainability | Complexidade ciclom\u00e1tica por hook | \u2264 10 | ESLint |\n| NFR-CV2-006 | Security | Todo endpoint user-facing exige JWT de user v\u00e1lido | 100% | Security review |\n| NFR-CV2-007 | Security | Isolamento de tenant: 0 acesso cross-tenant | 100% | RLS audit + security-review |\n| NFR-CV2-008 | Security | Denylist de sistema: 0 capability mapeando fun\u00e7\u00e3o de sistema/dev | 100% | Registry review |\n| NFR-CV2-009 | Cost-safety | Toda execu\u00e7\u00e3o com IA respeita cap + `max_tokens` | 100% | Edge logs + caps table |\n| NFR-CV2-010 | Privacy (LGPD) | Credenciais BYOK cifradas, escopadas por `auth.uid()`, revog\u00e1veis; reset cascateia | 100% | Schema + delete_account audit |\n| NFR-CV2-011 | Observability | Toda execu\u00e7\u00e3o gera row em `agent_executions` + pulse em `infra_health_logs` | 100% | REST audit |\n| NFR-CV2-012 | Idempotency | Re-execu\u00e7\u00e3o do mesmo trigger n\u00e3o duplica cobran\u00e7a | 100% | idempotency key em `agent_executions` |\n\n---\n\n## 4. Interface Requirements\n\n### 4.1 UI \u2192 Hook \u2192 Edge Function Contract\n\n```\n[Component: AgentDetail.tsx / NodePalette / CrewWizard]\n  \u2193 calls\n[Hook: useAgentTask / useCrewData / useAgentCapabilities]\n  \u2193 POST + user JWT\n[Edge Function: agent-task-execute (v2 capability router)]\n  \u2193 resolve capability \u2192 invoke target\n[Edge Function alvo: fetch-trends | canvas-execute | orchestrate-content | link-forge | publish-* | generate-content]\n  \u2193 reads/writes (RLS auth.uid())\n[Tables: crew_agents \u00b7 agent_capabilities \u00b7 agent_consumption_caps \u00b7 agent_executions \u00b7 user_api_keys]\n```\n\n### 4.2 External API Contracts\n\n#### `POST /functions/v1/agent-task-execute` (v2)\n\n**Auth:** Bearer JWT (user scope) \u2014 service-role+`x-user-id` **somente** no path cron/admin (n\u00e3o user-facing).\n**Request:**\n```typescript\n{\n  agent_id: string,          // crew_agents.id (RLS-owned)\n  capability_key?: string,   // override; default = agent.capability_key\n  task_prompt?: string,      // contexto da tarefa (LLM-planning steps)\n  payload?: Record<string, unknown>,  // input espec\u00edfico da capability (ex.: { niche } p/ fetch-trends)\n}\n```\n**Response (200):**\n```typescript\n{\n  status: 'done' | 'failed' | 'timeout',\n  execution_id: string,      // agent_executions.id\n  capability_key: string,\n  result?: unknown,          // payload material do m\u00f3dulo alvo\n  cost_mcoin: number,\n  credits_charged: number,   // 0 quando Sovereign freebie ou falha\n  billed: boolean,\n}\n```\n**Error codes:**\n| Code | Condition |\n|------|-----------|\n| 401 | JWT ausente/inv\u00e1lido |\n| 402 | Saldo mcoCoins insuficiente OU cap de consumo atingido |\n| 422 | `capability_key` desconhecido (n\u00e3o no allowlist) OU payload inv\u00e1lido |\n| 501 | BYOK ausente para a capability (`<service>_not_configured`) |\n| 500 | Erro interno (logado em `infra_health_logs`) |\n\n---\n\n## 5. Data Requirements\n\n| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |\n|-------|------|----------|-----------------|----------------------|\n| `crew_agents.capability_key` | text | YES (null p/ Lead/Core) | \u2208 registry `agent_capabilities.capability_key` | \"Capability inv\u00e1lida para este agente\" |\n| `crew_agents.level` | int | NO | \u2208 {0,1,2} (Core/Lead/subagente) | \"N\u00edvel de agente inv\u00e1lido\" |\n| `crew_agents.squad` | text | YES (null p/ Core) | \u2208 {content,tech,market,ops} | \"Departamento inv\u00e1lido\" |\n| `agent_consumption_caps.daily_mcoin_cap` | numeric | NO | \u2265 0 | \"Cap deve ser n\u00e3o-negativo\" |\n| `agent_consumption_caps.api_key_ref` | text | NO | provider conhecido | \"Provider/API desconhecido\" |\n| `agent_capabilities.target_function` | text | NO | \u2208 edge functions deployadas (allowlist) | \"Fun\u00e7\u00e3o alvo n\u00e3o permitida\" |\n| `agent_executions.idempotency_key` | text | YES | \u00fanico por (agent_id, trigger) | \u2014 |\n\n---\n\n## 6. Test Strategy Matrix\n\n| FR ID | Unit Test | Integration Test | E2E Test | Notes |\n|-------|-----------|-----------------|----------|-------|\n| FR-CV2-002 (router) | \u2705 | \u2705 | \u2705 | resolve+invoke+meter; mock m\u00f3dulo alvo no unit |\n| FR-CV2-010..012 (isolation) | \u2705 | \u2705 | \u2705 | RLS cross-tenant deny + denylist registry |\n| FR-CV2-020..022 (BYOK/caps/meter) | \u2705 | \u2705 | \u2705 | fail-closed 402/501; dedu\u00e7\u00e3o at\u00f4mica |\n| FR-CV2-030 (no auto-seed) | \u2705 | \u2705 | \u2705 | signup \u2192 count 0 |\n| FR-CV2-040..041 (4\u00d74 + edges) | \u2705 | \u2705 | \u2014 | seed on-demand |\n| FR-CV2-060..061 (perf/z-index) | \u2014 | \u2014 | \u2705 | E2E UI audit 1920\u00d71080 |\n| FR-CV2-070 (reset) | \u2705 (dry-run) | \u2705 | \u2014 | arquiva antes do wipe; idempotente |\n\n**Test files location:**\n- Unit: `src/hooks/__tests__/useAgentTask.test.ts`, `useAgentCapabilities.test.ts`\n- Integration: `src/__tests__/integration/constellation-v2.test.ts`\n- E2E: `scripts/qa/e2e-user-zero/flows/constellation-v2.ts` + skill `e2e-user-zero-audit`\n\n---\n\n## 7. Traceability Matrix\n\n| PR ID | FR ID | NFR ID |\n|-------|-------|--------|\n| PR-CV2-001 | FR-CV2-001, 002, 003, 004 | NFR-CV2-002, 006, 011 |\n| PR-CV2-002 | FR-CV2-005, 006 | NFR-CV2-005 |\n| PR-CV2-003 | FR-CV2-010, 011, 012 | NFR-CV2-006, 007, 008 |\n| PR-CV2-004 | FR-CV2-020, 021, 022 | NFR-CV2-009, 010, 012 |\n| PR-CV2-005 | FR-CV2-030, 031 | \u2014 |\n| PR-CV2-006 | FR-CV2-040 | NFR-CV2-001 |\n| PR-CV2-007 | FR-CV2-041 | NFR-CV2-001 |\n| PR-CV2-010 | FR-CV2-050 | NFR-CV2-011 |\n| PR-CV2-011 | FR-CV2-060, 061 | NFR-CV2-001 |\n| PR-CV2-012 | FR-CV2-023 | NFR-CV2-010 |\n| (reset) | FR-CV2-070 | NFR-CV2-010 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/04-frd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:49:18)*


## 🤖 Claude *(02:49:20)*

Autorando **SDD** (05 — SWEBOK + CISSP CBK, o doc técnico mais denso):

## 🤖 Claude *(02:50:42)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/05-sdd.md",
  "content": "# SDD \u2014 System Design Document\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)\n**Status:** Draft\n\n---\n\n## 1. Architecture Overview\n\n```\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  PRESENTATION (display-only)                                       \u2502\n\u2502  ConstellationPage \u00b7 CrewGraph (R3F) \u00b7 AgentNode/Edge/SquadHull    \u2502\n\u2502  HUD \u00b7 AgentDetail \u00b7 LogsPanel \u00b7 CrewWizard \u00b7 AccessConfigCard     \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                            \u2502 calls (hooks only)\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  LOGIC (Harness Engineering)                                       \u2502\n\u2502  useCrewData \u00b7 useAgentTask \u00b7 useAgentCapabilities \u00b7               \u2502\n\u2502  useAgentActivity \u00b7 useAccessConfig \u00b7 store/useCrewStore (Zustand) \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                            \u2502 HTTP + USER JWT (nunca service-role aqui)\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  EDGE \u2014 CAPABILITY ROUTER                                          \u2502\n\u2502  agent-task-execute (v2): JWT \u2192 resolve capability \u2192 BYOK \u2192        \u2502\n\u2502  cap check \u2192 invoke target \u2192 meter \u2192 write agent_executions        \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n           \u2502 invoke (allowlist)                 \u2502 RLS auth.uid()\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  EXISTING MODULE EDGE FNs (A1)    \u2502  \u2502  DB LAYER (RLS default-deny)   \u2502\n\u2502  fetch-trends \u00b7 canvas-execute \u00b7  \u2502  \u2502  crew_agents \u00b7 crew_edges      \u2502\n\u2502  orchestrate-content \u00b7 link-forge \u2502  \u2502  agent_capabilities (registry) \u2502\n\u2502  \u00b7 publish-{meta,social,wordpress}\u2502  \u2502  agent_consumption_caps        \u2502\n\u2502  \u00b7 generate-content \u00b7 analytics   \u2502  \u2502  agent_executions \u00b7 user_api_keys\u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                            \u2502\n                  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n                  \u2502 mcorch_nodes/edges \u2502  \u2190 observation node por execu\u00e7\u00e3o (opcional)\n                  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n```\n\n**Princ\u00edpio-chave (A1):** o router **n\u00e3o reimplementa** m\u00f3dulos \u2014 ele \u00e9 um *despachante* fino que valida, resolve credencial/cap, e delega \u00e0 edge function j\u00e1 existente, capturando custo e resultado.\n\n---\n\n## 2. Component Catalog\n\n### 2.1 New / Modified Custom Hooks (`src/hooks/`)\n\n| Hook | File | Responsibility | TanStack Query keys |\n|------|------|---------------|---------------------|\n| `useAgentCapabilities` | `useAgentCapabilities.ts` (novo) | l\u00ea registry `agent_capabilities` + bindings do user | `['agent_capabilities', userId]` |\n| `useAgentTask` | `useAgentTask.ts` (modificar) | dispara `agent-task-execute` v2 com `capability_key`+payload; `assertExecuteSuccess` | mutation |\n| `useCrewData` | `useCrewData.ts` (modificar) | **remove** auto-seed; estado vazio v\u00e1lido | `['crew_agents', userId]` `['crew_edges', userId]` |\n| `useAccessConfig` | `useAccessConfig.ts` (novo) | CRUD de `agent_consumption_caps` + binding BYOK por subagente | `['agent_caps', userId]` |\n| `useAgentActivity` | `useAgentActivity.ts` (modificar) | projeta execs reais (+capability/result) nos logs/status | `['agent_executions', userId]` |\n\n### 2.2 New / Modified Display Components (`src/components/`)\n\n| Component | File | Props | Hook consumed |\n|-----------|------|-------|--------------|\n| `CrewWizard` | `components/constellation/CrewWizard.tsx` (novo) | `onCreate` | `useCrewData`, `useAgentCapabilities` |\n| `AccessConfigCard` | `components/constellation/AccessConfigCard.tsx` (novo) | `agentId` | `useAccessConfig` |\n| `AgentDetail` | `components/panels/AgentDetail.tsx` (modificar) | `agentId` | `useAgentTask` (capability-aware) |\n| `EmptyConstellation` | `components/constellation/EmptyConstellation.tsx` (novo) | \u2014 | \u2014 (CTA \u2192 wizard) |\n| `CrewGraph` | `components/graph/CrewGraph.tsx` (modificar) | \u2014 | `useCrewStore` (z-index/LOD/node-cap) |\n\n### 2.3 New / Modified Edge Functions (`supabase/functions/`)\n\n| Function | Path | Auth | mcoCoins | Secrets needed |\n|----------|------|------|----------|----------------|\n| `agent-task-execute` (v2) | `supabase/functions/agent-task-execute/index.ts` | JWT (user) | medido via RPC | nenhum pr\u00f3prio; resolve BYOK do user; fallback Sovereign usa vault s\u00f3 em path freebie documentado |\n| (target fns \u2014 reuso) | `fetch-trends`, `canvas-execute`, `orchestrate-content`, `link-forge`, `process-affiliate-link`, `publish-meta/social/wordpress`, `generate-content` | JWT (user) | conforme cada uma | j\u00e1 deployadas (sem mudan\u00e7a de contrato) |\n\n### 2.4 Zustand Store Slices\n\n| Slice | Store file | State shape | Actions |\n|-------|------------|-------------|---------|\n| crew (existente, estender) | `src/store/useCrewStore.ts` | `agents`, `edges`, `logs`, `selectedAgentId`, **`emptyState:boolean`** | `setAgents`, `setEdges`, `setLogs`, `updateAgentStatus`, **(remover `seedEnterpriseStructure`)** |\n\n### 2.5 New DB Objects\n\n| Object | Type | Purpose | Migration file |\n|--------|------|---------|---------------|\n| `agent_capabilities` | Table | registry capability_key \u2192 target_function + input schema + custo base + requires_byok | `<ts>_constellation_v2_capabilities.sql` |\n| `agent_consumption_caps` | Table | caps di\u00e1rios por user/API/agente | `<ts>_constellation_v2_caps.sql` |\n| `crew_agents.capability_key` | Column | binding subagente\u2192capability | `<ts>_constellation_v2_crew_capability.sql` |\n| `agent_executions_archive` | Table | arquivo dos 31 execs antes do reset (OTD-CV2-004) | `<ts>_constellation_v2_exec_archive.sql` |\n| `agent_executions.idempotency_key` | Column | anti-double-charge | mesma migra\u00e7\u00e3o do router |\n\n---\n\n## 3. Data Flow Diagrams\n\n### Use Case: Subagente Viral Miner minera tend\u00eancias reais\n\n```\nUser            useAgentTask        agent-task-execute(v2)        fetch-trends        DB\n \u2502                  \u2502                       \u2502                          \u2502              \u2502\n \u2502\u2500[Executar]\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502                       \u2502                          \u2502              \u2502\n \u2502                  \u2502\u2500[POST JWT {agent_id}]\u25b6\u2502                          \u2502              \u2502\n \u2502                  \u2502                       \u2502\u2500[SELECT crew_agents RLS]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 capability_key='viral_miner'\n \u2502                  \u2502                       \u2502\u2500[lookup agent_capabilities]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 target='fetch-trends', requires_byok\n \u2502                  \u2502                       \u2502\u2500[resolve user_api_keys (BYOK)]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 (402/501 se ausente)\n \u2502                  \u2502                       \u2502\u2500[check agent_consumption_caps]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 (402 se estourado)\n \u2502                  \u2502                       \u2502\u2500[INSERT agent_executions status=running]\u2500\u25b6\u2502 \u2192 execution_id\n \u2502                  \u2502                       \u2502\u2500[invoke fetch-trends (user JWT/BYOK)]\u2500\u2500\u2500\u2500\u25b6\u2502 dados reais\n \u2502                  \u2502                       \u2502\u25c0\u2500[trends payload]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502              \u2502\n \u2502                  \u2502                       \u2502\u2500[calc_agent_cost_mcoin + deduct]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 (Sovereign freebie skip)\n \u2502                  \u2502                       \u2502\u2500[UPDATE agent_executions status=done]\u2500\u2500\u2500\u2500\u25b6\u2502\n \u2502                  \u2502                       \u2502\u2500[pulse infra_health_logs]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502\n \u2502                  \u2502\u25c0\u2500[200 {result,cost}]\u2500\u2500\u2502                          \u2502              \u2502\n \u2502\u25c0\u2500[logs+status]\u2500\u2500\u2500\u2502                       \u2502                          \u2502              \u2502\n```\n\n---\n\n## 4. API Contract Definitions\n\n> Todo endpoint user-facing valida JWT de user ANTES de qualquer l\u00f3gica. **Service-role nunca no path user-facing** (FR-CV2-012).\n\n### `POST /functions/v1/agent-task-execute` (v2 capability router)\n\n```typescript\ninterface AgentTaskExecuteV2Request {\n  agent_id: string            // crew_agents.id (RLS-owned)\n  capability_key?: string     // default = agent.capability_key\n  task_prompt?: string\n  payload?: Record<string, unknown>\n  idempotency_key?: string\n}\n\ninterface AgentTaskExecuteV2Response {\n  status: 'done' | 'failed' | 'timeout'\n  execution_id: string\n  capability_key: string\n  result?: unknown\n  cost_mcoin: number\n  credits_charged: number\n  billed: boolean\n}\n\n// Sequ\u00eancia interna:\n// 1. JWT user \u2192 auth.getUser  (401)\n// 2. SELECT crew_agents WHERE id=agent_id  (RLS auth.uid() \u2014 404 se n\u00e3o-dono)\n// 3. resolve capability_key \u2192 agent_capabilities (allowlist \u2014 422 se desconhecido)\n// 4. if requires_byok: resolve user_api_keys[provider] (501 se ausente)\n// 5. check agent_consumption_caps daily (402 se estourado)\n// 6. INSERT agent_executions (status=running, idempotency_key)\n// 7. invoke target_function com BYOK/contexto do user\n// 8. calc_agent_cost_mcoin \u2192 deduct_mco_coins (skip se Sovereign)  (402 se saldo insuf.)\n// 9. UPDATE agent_executions (done/failed + cost + result)\n// 10. pulse infra_health_logs service='agent-task-execute'\n```\n\n---\n\n## 5. Security Design\n\n### 5.1 Threat Model (STRIDE)\n\n| Component | Threat | Type | Severity | Mitigation |\n|-----------|--------|------|----------|------------|\n| `agent-task-execute` | acesso n\u00e3o autenticado | Spoofing | High | JWT user no entry-point; sem service-role no path user-facing |\n| `crew_agents`/`agent_executions` | leitura cross-tenant | Information Disclosure | Critical | RLS `user_id = auth.uid()` default-deny |\n| Capability router | **agente aciona fun\u00e7\u00e3o de sistema/dev** | Elevation of Privilege | Critical | **denylist**: `agent_capabilities.target_function` \u2208 allowlist de fun\u00e7\u00f5es tenant-scoped; nunca shell/migrations/service-role |\n| BYOK keys | exfiltra\u00e7\u00e3o de credencial | Information Disclosure | Critical | coluna RLS + column-REVOKE de leitura ampla; resolvida s\u00f3 server-side no router; nunca retornada ao client |\n| mcoCoins deduction | bypass client-side | Tampering | Critical | s\u00f3 via RPC `deduct_mco_coins` server-side |\n| Consumption caps | loop de custo / esgotar quota | DoS / financeiro | High | cap di\u00e1rio por user/API + `max_tokens` + circuit breaker |\n| Reset/migration | apagar dados reais | Repudiation/loss | High | arquivar execs + purge filtrado por owners \u00f3rf\u00e3os + dry-run |\n\n### 5.2 RLS Policy Definitions\n\n```sql\n-- agent_capabilities: registry GLOBAL (system rows, read-all autenticado) + bindings per-user via crew_agents\nALTER TABLE public.agent_capabilities ENABLE ROW LEVEL SECURITY;\nCREATE POLICY \"agent_capabilities: read for authenticated\"\n  ON public.agent_capabilities FOR SELECT\n  USING (auth.uid() IS NOT NULL);\n-- writes: service_role only (seed) \u2014 sem policy de INSERT/UPDATE para user\n\n-- agent_consumption_caps: per-user\nALTER TABLE public.agent_consumption_caps ENABLE ROW LEVEL SECURITY;\nCREATE POLICY \"caps: users manage own\"\n  ON public.agent_consumption_caps FOR ALL\n  USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());\n```\n\n> `crew_agents`, `crew_edges`, `agent_executions`, `user_api_keys` j\u00e1 possuem RLS per-user; v2 reauditar\u00e1 e endurecer\u00e1 default-deny.\n\n### 5.3 JWT Validation Points\n\n```typescript\nconst authHeader = req.headers.get('Authorization')\nif (!authHeader) return json(401, { error: 'unauthorized' })\nconst { data: { user }, error } = await supabaseUserClient.auth.getUser(\n  authHeader.replace('Bearer ', '')\n)\nif (error || !user) return json(401, { error: 'unauthorized' })\n// TODAS as queries subsequentes usam o client com o JWT do user (RLS aplica auth.uid()).\n```\n\n### 5.4 Secrets Inventory\n\n| Secret Name | Used In | Vault Location | Rotation Policy |\n|-------------|---------|----------------|----------------|\n| (BYOK do user) `user_api_keys.<provider>_api_key` | router \u2192 m\u00f3dulo alvo | tabela per-user (RLS) | usu\u00e1rio gerencia/revoga |\n| `SUPABASE_SERVICE_ROLE_KEY` | **somente** path cron/admin de `agent-daily-pulse` (N\u00c3O user-facing) | Supabase vault | padr\u00e3o |\n| `SOVEREIGN_USER_ID` | gate de freebie (`user.id === SOVEREIGN_USER_ID`) | Supabase vault | est\u00e1vel |\n| (fallback global por capability) ex.: `GEMINI_API_KEY` | s\u00f3 path cron/onboarding default documentado | Supabase vault | per API Tenancy Model |\n\n> \u26a0\ufe0f NUNCA commitar valores. Apenas nomes de chave aparecem na documenta\u00e7\u00e3o. BYOK nunca retorna ao client.\n\n---\n\n## 6. Infrastructure Touchpoints\n\n| Infrastructure | Usage | Impact |\n|----------------|-------|--------|\n| `mega-brain-daemon` | watchdog do router + caps | self-heal se error rate alto |\n| `infra_health_logs` | novo servi\u00e7o `agent-task-execute` + `constellation_v2_*` events | telemetria por execu\u00e7\u00e3o |\n| `agent-daily-pulse` (cron) | estende para incluir os subagentes (n\u00e3o s\u00f3 Directors) | execu\u00e7\u00f5es di\u00e1rias por subagente |\n| ChromaDB / mcorch_nodes | observation node opcional por execu\u00e7\u00e3o (mesh) | rastreabilidade GraphRAG |\n\n---\n\n## 7. Migration Stubs\n\n```sql\n-- ============================================================\n-- MIGRATION: <ts>_constellation_v2_capabilities.sql\n-- ============================================================\nCREATE TABLE public.agent_capabilities (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  capability_key  text UNIQUE NOT NULL,            -- ex.: 'viral_miner', 'canvas_studio'\n  department      text NOT NULL,                    -- content|tech|market|ops\n  display_name    text NOT NULL,\n  target_function text NOT NULL,                    -- edge function ALVO (allowlist)\n  input_schema    jsonb NOT NULL DEFAULT '{}',\n  base_mcoin_cost numeric NOT NULL DEFAULT 0,\n  requires_byok   boolean NOT NULL DEFAULT true,\n  byok_provider   text,                             -- coluna em user_api_keys\n  is_active       boolean NOT NULL DEFAULT true,\n  created_at      timestamptz NOT NULL DEFAULT now()\n);\nALTER TABLE public.agent_capabilities ENABLE ROW LEVEL SECURITY;\nCREATE POLICY \"agent_capabilities: read for authenticated\"\n  ON public.agent_capabilities FOR SELECT USING (auth.uid() IS NOT NULL);\n-- writes: service_role only (seed script)\n\n-- crew_agents binding\nALTER TABLE public.crew_agents\n  ADD COLUMN IF NOT EXISTS capability_key text REFERENCES public.agent_capabilities(capability_key);\n\n-- consumption caps (per user/API)\nCREATE TABLE public.agent_consumption_caps (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,\n  api_key_ref     text NOT NULL,                    -- provider/servi\u00e7o\n  daily_mcoin_cap numeric NOT NULL DEFAULT 0,        -- 0 = ilimitado (Sovereign)\n  agent_id        uuid REFERENCES public.crew_agents(id) ON DELETE CASCADE, -- null = cap por API global do user\n  created_at      timestamptz NOT NULL DEFAULT now(),\n  updated_at      timestamptz NOT NULL DEFAULT now()\n);\nALTER TABLE public.agent_consumption_caps ENABLE ROW LEVEL SECURITY;\nCREATE POLICY \"caps: users manage own\"\n  ON public.agent_consumption_caps FOR ALL\n  USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());\n\n-- exec idempotency + archive\nALTER TABLE public.agent_executions ADD COLUMN IF NOT EXISTS idempotency_key text;\nCREATE TABLE public.agent_executions_archive (LIKE public.agent_executions INCLUDING ALL);\n```\n\n> RLS habilitado em toda tabela nova (default-deny). Toda migra\u00e7\u00e3o nova passa por `/security-review` antes do commit (FMEA-011).\n\n---\n\n## 8. Open Technical Decisions\n\n| ID | Description | Option A | Option B | Recommendation | Owner |\n|----|-------------|----------|----------|----------------|-------|\n| OTD-CV2-001 | Reuso de `crew_agents` vs. tabela v2 nova | estender `crew_agents` + `agent_capabilities` | nova `constellation_v2_agents` | **A** (in-place, migra\u00e7\u00e3o + binding) | Sovereign |\n| OTD-CV2-002 | Modelo de execu\u00e7\u00e3o | binding direto 1 capability\u21921 fun\u00e7\u00e3o | LLM tool-calling planner | **A na fase 1**; B (PR-CV2-020) depois | Sovereign |\n| OTD-CV2-003 | Granularidade do cap | por-API global do user | por-agente | **h\u00edbrido** (linha com `agent_id` null = global; com agent_id = espec\u00edfico) | Sovereign |\n| OTD-CV2-004 | 31 execs \u00f3rf\u00e3os no reset | wipe | arquivar | **arquivar** em `agent_executions_archive` | Sovereign |\n| OTD-CV2-005 | provider/model default | manter seed atual (drift) | `groq/llama-3.3-70b-versatile` | **groq** (v\u00e1lido em `agent_pricing`) | Engineering |\n| OTD-CV2-006 | Publica\u00e7\u00e3o Social | N subagentes | 1 subagente roteando publish-* | **1** (roteia meta/social/wordpress) | Sovereign |\n| OTD-CV2-007 | Render 3D em baixa perf | degradar p/ 2D | R3F + LOD + cap n\u00f3s | **R3F + LOD + cap \u226421** | Engineering |\n| OTD-CV2-008 | Watchdog/Infra subagente | pode acionar self-heal | read-only no escopo do tenant | **read-only** (sem acesso a system) | Sovereign |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/05-sdd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:50:49)*


## 🤖 Claude *(02:50:50)*

**Fase 3 selada** (FRD + SDD). Autorando **Fase 4** (Data Model + Process Flow — DMBOK + BPM CBOK):

## 🤖 Claude *(02:51:39)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/06-data-model.md",
  "content": "# Data & Knowledge Model\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)\n**Status:** Draft\n\n---\n\n## 1. Conceptual Data Model\n\n```\n[profiles (tenant)] \u2500\u2500(1:N)\u2500\u2500\u25b6 [crew_agents] \u2500\u2500(N:1)\u2500\u2500\u25b6 [agent_capabilities (registry)]\n       \u2502                            \u2502                            \u2502\n       \u2502                            \u2502 (N:M via crew_edges)        \u2502 (1:1) target_function\n       \u2502                            \u25bc                            \u25bc\n       \u2502                       [crew_edges]              [edge function ALVO (reuso)]\n       \u2502\n       \u251c\u2500\u2500(1:N)\u2500\u2500\u25b6 [agent_consumption_caps]\n       \u251c\u2500\u2500(1:N)\u2500\u2500\u25b6 [user_api_keys (BYOK)]\n       \u2514\u2500\u2500(1:N)\u2500\u2500\u25b6 [agent_executions] \u2500\u2500(archive)\u2500\u2500\u25b6 [agent_executions_archive]\n```\n\n**Entities:**\n- **crew_agents:** o n\u00f3 da constela\u00e7\u00e3o (Core L0, Lead L1, subagente L2 m\u00f3dulo-bound). Per-user.\n- **crew_edges:** hierarquia (Directive Core\u2192Lead, Reporting Lead\u2192subagente). Per-user.\n- **agent_capabilities:** registry GLOBAL (system rows) capability_key \u2192 target_function + custo + requires_byok.\n- **agent_consumption_caps:** tetos de consumo por user/API/agente.\n- **agent_executions:** log append-only de toda execu\u00e7\u00e3o real (tokens, custo, lat\u00eancia, resultado).\n- **user_api_keys:** chaves BYOK per-user (j\u00e1 existe).\n\n---\n\n## 2. Logical Data Model\n\n### Table: `agent_capabilities` (registry global \u2014 system data)\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | PK |\n| `capability_key` | `text` | NOT NULL (UNIQUE) | \u2014 | \u2014 | ex.: `viral_miner`, `canvas_studio`, `orchestration` |\n| `department` | `text` | NOT NULL | \u2014 | \u2014 | content\\|tech\\|market\\|ops |\n| `display_name` | `text` | NOT NULL | \u2014 | \u2014 | r\u00f3tulo PT-BR |\n| `target_function` | `text` | NOT NULL | \u2014 | \u2014 | edge function alvo (allowlist) |\n| `input_schema` | `jsonb` | NOT NULL | `'{}'` | \u2014 | shape do payload |\n| `base_mcoin_cost` | `numeric` | NOT NULL | `0` | \u2014 | custo base (al\u00e9m do medido por tokens) |\n| `requires_byok` | `bool` | NOT NULL | `true` | \u2014 | precisa chave do user |\n| `byok_provider` | `text` | NULL | \u2014 | \u2014 | coluna em `user_api_keys` |\n| `is_active` | `bool` | NOT NULL | `true` | \u2014 | gate |\n| `created_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | audit |\n\n### Table: `crew_agents` (existente \u2014 coluna nova)\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| ... (existentes: id, user_id, agent_key, name, role, avatar, provider, model, status, position, system_prompt, priority, level, squad) | | | | | preservados |\n| `capability_key` | `text` | NULL | \u2014 | `agent_capabilities.capability_key` | binding (null p/ Core/Lead) |\n\n### Table: `agent_consumption_caps`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | PK |\n| `user_id` | `uuid` | NOT NULL | \u2014 | `auth.users.id` | tenant |\n| `api_key_ref` | `text` | NOT NULL | \u2014 | \u2014 | provider/servi\u00e7o |\n| `daily_mcoin_cap` | `numeric` | NOT NULL | `0` | \u2014 | 0 = ilimitado (Sovereign) |\n| `agent_id` | `uuid` | NULL | \u2014 | `crew_agents.id` | null = cap por-API global do user |\n| `created_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | audit |\n| `updated_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | audit |\n\n### Table: `agent_executions` (existente \u2014 coluna nova)\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| ... (existentes: id, agent_id, user_id, status, provider, model, tokens_in, tokens_out, cost_mcoin, cost_usd_micro, latency_ms, error_msg, started_at, completed_at) | | | | | preservados |\n| `capability_key` | `text` | NULL | \u2014 | \u2014 | qual capability rodou |\n| `idempotency_key` | `text` | NULL | \u2014 | \u2014 | anti-double-charge |\n| `result_summary` | `text` | NULL | \u2014 | \u2014 | s\u00edntese material do resultado |\n\n---\n\n## 3. Supabase Physical Schema Stubs\n\n```sql\n-- ============================================================\n-- MIGRATION: <ts>_constellation_v2_schema.sql\n-- (passa por /security-review antes do commit \u2014 FMEA-011)\n-- ============================================================\n\n-- 1. Registry global de capabilities\nCREATE TABLE public.agent_capabilities (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  capability_key  text UNIQUE NOT NULL,\n  department      text NOT NULL CHECK (department IN ('content','tech','market','ops')),\n  display_name    text NOT NULL,\n  target_function text NOT NULL,\n  input_schema    jsonb NOT NULL DEFAULT '{}',\n  base_mcoin_cost numeric NOT NULL DEFAULT 0 CHECK (base_mcoin_cost >= 0),\n  requires_byok   boolean NOT NULL DEFAULT true,\n  byok_provider   text,\n  is_active       boolean NOT NULL DEFAULT true,\n  created_at      timestamptz NOT NULL DEFAULT now()\n);\nALTER TABLE public.agent_capabilities ENABLE ROW LEVEL SECURITY;\nCREATE POLICY \"agent_capabilities: read for authenticated\"\n  ON public.agent_capabilities FOR SELECT USING (auth.uid() IS NOT NULL);\n-- writes: service_role only (seed)\n\n-- 2. crew_agents binding\nALTER TABLE public.crew_agents\n  ADD COLUMN IF NOT EXISTS capability_key text\n  REFERENCES public.agent_capabilities(capability_key);\n\n-- 3. consumption caps\nCREATE TABLE public.agent_consumption_caps (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,\n  api_key_ref     text NOT NULL,\n  daily_mcoin_cap numeric NOT NULL DEFAULT 0 CHECK (daily_mcoin_cap >= 0),\n  agent_id        uuid REFERENCES public.crew_agents(id) ON DELETE CASCADE,\n  created_at      timestamptz NOT NULL DEFAULT now(),\n  updated_at      timestamptz NOT NULL DEFAULT now(),\n  UNIQUE (user_id, api_key_ref, agent_id)\n);\nALTER TABLE public.agent_consumption_caps ENABLE ROW LEVEL SECURITY;\nCREATE POLICY \"caps: users manage own\"\n  ON public.agent_consumption_caps FOR ALL\n  USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());\nCREATE INDEX agent_consumption_caps_user_idx ON public.agent_consumption_caps (user_id);\n\n-- 4. exec idempotency + archive (preserva 31 execs reais antes do reset)\nALTER TABLE public.agent_executions ADD COLUMN IF NOT EXISTS capability_key text;\nALTER TABLE public.agent_executions ADD COLUMN IF NOT EXISTS idempotency_key text;\nALTER TABLE public.agent_executions ADD COLUMN IF NOT EXISTS result_summary text;\nCREATE TABLE public.agent_executions_archive (LIKE public.agent_executions INCLUDING ALL);\n```\n\n---\n\n## 4. GraphRAG Knowledge Nodes\n\n### Node Types Introduced\n\n| node_type | Title Pattern | Content Fields | Embedding Source |\n|-----------|--------------|----------------|-----------------|\n| `observation` (reuso) | `constellation-v2-exec-<id>` | capability + result_summary + custo | `display_name + result_summary` |\n| `documentation_suite` | `bok-scribe-seal-constellation-v2-v1` | s\u00edntese da su\u00edte | content do seal |\n\n> A v2 N\u00c3O cria um novo `node_type` pr\u00f3prio para agentes no mesh \u2014 os `crew_agents` vivem na sua tabela; a malha recebe **observations** opcionais por execu\u00e7\u00e3o (rastreabilidade), via padr\u00e3o CEA.\n\n### Edge Types Introduced\n\n| Edge relationship | Source node_type | Target node_type | Metadata |\n|-------------------|-----------------|-----------------|----------|\n| `DERIVES_FROM` | documentation_suite | documentation_suite (parent seal) | weight=1.0 |\n| `observes` (reuso auto-stitch) | observation | markdown_file/feature | capability ref |\n\n### Embedding Trigger\nO seal `documentation_suite` \u00e9 inserido com `embedding IS NULL` \u2192 `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` (768d). Confirmar via REST `embedding=not.is.null`.\n\n### FSRS-6 Parameters\n\n| Field | Initial Value | Decay Rule |\n|-------|--------------|------------|\n| `stability_score` | `0.85` (seal) | migra\u00e7\u00e3o `20260425190000` |\n| `revenue_impact` | modesto n\u00e3o-zero (v2 ativa consumo mcoCoins + afiliado) | atualizado por ciclo econ\u00f4mico |\n\n---\n\n## 5. Tenant Isolation Map\n\n| Table | `user_id` scope | `project_id` scope | System rows (user_id IS NULL) |\n|-------|----------------|-------------------|-------------------------------|\n| `crew_agents` | \u2705 Required | Futuro (multi-brand PR-CV2-022) | No |\n| `crew_edges` | \u2705 Required | Futuro | No |\n| `agent_capabilities` | \u2014 (registry global) | \u2014 | **Yes** (system data, read-all autenticado) |\n| `agent_consumption_caps` | \u2705 Required | \u2014 | No |\n| `agent_executions` | \u2705 Required | \u2014 | No |\n| `user_api_keys` (BYOK) | \u2705 Required | \u2014 | No |\n\n> **Barreira de sistema (BR-CV2-002):** `agent_capabilities.target_function` \u00e9 um **allowlist** de fun\u00e7\u00f5es tenant-scoped. Nenhuma linha pode apontar para fun\u00e7\u00e3o de sistema/dev, migrations, service-role, shell, ou pipelines do Pantheon OpenClaw. Revis\u00e3o do registry \u00e9 gate de security-review.\n\n---\n\n## 6. Data Quality Rules\n\n| Table | Column | Rule | Violation Message (PT-BR) |\n|-------|--------|------|--------------------------|\n| `crew_agents` | `capability_key` | se `level=2` ent\u00e3o NOT NULL e \u2208 registry; se `level\u2208{0,1}` ent\u00e3o NULL | \"Subagente precisa de capability; Lead/Core n\u00e3o t\u00eam\" |\n| `crew_agents` | `level` | \u2208 {0,1,2} | \"N\u00edvel inv\u00e1lido\" |\n| `agent_capabilities` | `target_function` | \u2208 allowlist de fun\u00e7\u00f5es tenant-scoped | \"Fun\u00e7\u00e3o alvo n\u00e3o permitida (fora do allowlist)\" |\n| `agent_consumption_caps` | `daily_mcoin_cap` | \u2265 0 | \"Cap n\u00e3o pode ser negativo\" |\n| `agent_executions` | `cost_mcoin` | \u2265 0 quando done | \"Custo inv\u00e1lido\" |\n| `crew_agents` (por user) | count | \u2264 21 (1 Core + 4 Leads + 16 subagentes) | \"Limite de agentes da constela\u00e7\u00e3o atingido\" |\n\n---\n\n## 7. Retention & Archival Policy\n\n| Data | Retention Period | Archival Strategy | Deletion Trigger |\n|------|-----------------|-------------------|-----------------|\n| `crew_agents`/`crew_edges` | enquanto o tenant existir | \u2014 | `delete_account()` cascade (LGPD) |\n| `agent_executions` | 12 meses ativos | move p/ `agent_executions_archive` | cron de arquivamento |\n| `agent_executions_archive` (incl. 31 do reset) | indefinido (auditoria econ\u00f4mica) | \u2014 | manual |\n| `agent_consumption_caps` | enquanto o tenant existir | \u2014 | cascade |\n| `user_api_keys` (BYOK) | enquanto o user mantiver | \u2014 | revoga\u00e7\u00e3o pelo user / `delete_account()` |\n| **Reset inicial** | \u2014 | purga owners \u00f3rf\u00e3os (sem profile) + wipe crew Sovereign **ap\u00f3s** arquivar execs | one-shot migra\u00e7\u00e3o/script |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/06-data-model.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:51:45)*


## 🤖 Claude *(02:51:45)*

Autorando **Process Flow** (07 — BPM CBOK):

## 🤖 Claude *(02:52:32)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/07-process-flow.md",
  "content": "# Process & Automation Blueprint\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** BPM CBOK v4 (Process Modeling + Process Design)\n**Status:** Draft\n\n---\n\n## 1. Process Inventory\n\n| Process ID | Name | Type | Trigger | Owner | SLA |\n|------------|------|------|---------|-------|-----|\n| PROC-CV2-001 | Crew creation on-demand | human-in-loop | usu\u00e1rio (wizard / \"+ Agente\") | User | < 2s/insert |\n| PROC-CV2-002 | Capability execution (subagente\u2192m\u00f3dulo real) | event-driven | bot\u00e3o \"Executar\" / Run Squad | System | < 800ms router + lat\u00eancia do m\u00f3dulo |\n| PROC-CV2-003 | BYOK + cap + metering | automated (dentro do router) | cada execu\u00e7\u00e3o | System | parte do PROC-CV2-002 |\n| PROC-CV2-004 | Daily pulse (subagentes) | cron | `0 7 * * *` BRT | System | < 5min/loop |\n| PROC-CV2-005 | Reset/migration inicial | human-in-loop | one-shot (Sovereign) | Sovereign | N/A (one-shot, dry-run first) |\n| PROC-CV2-006 | Run Squad / Run All (BFS hierarquia) | event-driven | bot\u00e3o \"Run Squad\" | User | soma das execu\u00e7\u00f5es |\n| PROC-CV2-007 | Empty-start signup | automated | novo cadastro | System | imediato |\n| PROC-CV2-008 | Access config (m\u00f3dulo + BYOK + caps) | human-in-loop | settings do subagente | User | < 1s |\n| PROC-CV2-009 | Observation node emission (mesh) | automated | p\u00f3s-execu\u00e7\u00e3o done | System | best-effort ass\u00edncrono |\n\n---\n\n## 2. BPMN-lite Process Maps\n\n### PROC-CV2-002 + PROC-CV2-003: Capability execution + BYOK/cap/meter\n\n```\nSTART \u2500\u2500\u25b6 [Validar JWT user] \u2500\u2500\u25b6 <auth ok?>\n                                   \u2502 NO \u2500\u2500\u25b6 HTTP 401\n                                   \u2502 YES\n                          [SELECT crew_agents RLS auth.uid()]\n                                   \u2502\n                          [resolve capability_key \u2192 agent_capabilities] \u2500\u2500<no allowlist?>\u2500\u2500\u25b6 HTTP 422\n                                   \u2502 YES\n                          <requires_byok?>\n                             \u2502 YES \u2500\u2500\u25b6 [resolve user_api_keys] \u2500\u2500<ausente?>\u2500\u2500\u25b6 HTTP 501 (<service>_not_configured)\n                             \u2502 NO/OK\n                          [check agent_consumption_caps (di\u00e1rio)] \u2500\u2500<estourou?>\u2500\u2500\u25b6 HTTP 402 (cap_reached)\n                                   \u2502 OK\n                          [INSERT agent_executions status=running]\n                                   \u2502\n                          [invoke target_function (BYOK + user ctx)] \u2500\u2500<falha?>\u2500\u2500\u25b6 [UPDATE failed] \u2500\u2500\u25b6 HTTP 200 {failed}\n                                   \u2502 OK\n                          [calc_agent_cost_mcoin]\n                                   \u2502\n                          <user == Sovereign?>\n                             \u2502 YES \u2500\u2500\u25b6 [skip deduct \u00b7 sovereign_freebie=true]\n                             \u2502 NO \u2500\u2500\u25b6 [deduct_mco_coins] \u2500\u2500<saldo insuf?>\u2500\u2500\u25b6 HTTP 402 (mas exec preservado, billed=false)\n                                   \u2502\n                          [UPDATE agent_executions status=done + cost + result_summary]\n                                   \u2502\n                          [pulse infra_health_logs service=agent-task-execute]\n                                   \u2502\n                          [emit observation node (PROC-CV2-009, async best-effort)]\n                                   \u2502\n                                  END (HTTP 200 {done, result, cost})\n```\n\n**Swimlanes:**\n\n| Swimlane | Participant | Tasks |\n|----------|-------------|-------|\n| User | Browser | clica \"Executar\", v\u00ea logs/status/saldo |\n| Frontend Hook | `useAgentTask.ts` | POST + JWT; `assertExecuteSuccess`; invalida queries |\n| Edge Function | `agent-task-execute` (v2) | JWT, resolve capability, BYOK, cap, invoke, meter, write |\n| External/Module | `fetch-trends`/`canvas-execute`/`orchestrate-content`/`link-forge`/`publish-*` | trabalho real (reuso A1) |\n| DB | Supabase | `crew_agents`, `agent_capabilities`, `agent_consumption_caps`, `agent_executions` (RLS) |\n\n---\n\n### PROC-CV2-005: Reset/migration inicial (one-shot, dry-run first)\n\n```\n[Sovereign autoriza] \u2500\u2500\u25b6 [DRY-RUN: contar owners \u00f3rf\u00e3os (sem profile) + crew Sovereign + execs]\n   \u2502\n   \u25bc\n[Arquivar agent_executions \u2192 agent_executions_archive]  (OTD-CV2-004)\n   \u2502\n   \u25bc\n[DELETE crew_edges/crew_agents WHERE user_id NOT IN (SELECT id FROM profiles)]  (purga 26 \u00f3rf\u00e3os)\n   \u2502\n   \u25bc\n[DELETE crew_edges/crew_agents WHERE user_id = SOVEREIGN]  (wipe da crew inchada)\n   \u2502\n   \u25bc\n[Migra\u00e7\u00e3o: drop auto-seed call em useCrewData (empty-start)]\n   \u2502\n   \u25bc\n[Verifica\u00e7\u00e3o material: crew_agents count = 0; archive count = 31] \u2500\u2500\u25b6 END\n```\n\n> **Recovery:** dry-run obrigat\u00f3rio + backup antes de qualquer DELETE. Filtro por `NOT IN profiles` \u00e9 a salvaguarda contra apagar o tenant real. Idempotente.\n\n---\n\n### PROC-CV2-001 + PROC-CV2-007: Empty-start + crew on-demand\n\n```\n[Novo signup] \u2500\u2500\u25b6 [NENHUM auto-seed]  (FR-CV2-030)\n   \u2502\n   \u25bc\n[Abre /dashboard/constellation] \u2500\u2500\u25b6 <crew vazia?>\n                                       \u2502 YES \u2500\u2500\u25b6 [EmptyConstellation + CTA \"Criar minha crew\"]\n                                       \u2502\n                                  [CrewWizard: escolher deptos + capabilities (mapa 4\u00d74)]\n                                       \u2502\n                                  [INSERT Core + Leads + subagentes (keys est\u00e1veis) + edges Directive/Reporting]\n                                       \u2502\n                                  [AccessConfig por subagente: BYOK + caps]  (PROC-CV2-008)\n                                       \u2502\n                                      END (crew operacional)\n```\n\n---\n\n## 3. n8n Workflow Blueprints\n\n### Workflow: (opcional) Agendamento aut\u00f4nomo por subagente (PR-CV2-021, Future)\n\n**Trigger:** cron por-subagente (config do user)\n**Idempotency key:** `cv2-<agent_id>-<yyyymmdd>`\n\n```\n[Trigger: cron por-subagente]\n  \u2502\n  \u25bc\n[HTTP Request \u2192 /functions/v1/agent-task-execute (service-role + x-user-id, path admin documentado)]\n  \u251c\u2500\u2500 Body: { agent_id, capability_key, payload }\n  \u251c\u2500\u2500 (success) \u2500\u2500\u25b6 [Update status + log]\n  \u2514\u2500\u2500 (error) \u2500\u2500\u25b6 [retry \u22643 backoff exponencial] \u2500\u2500(>3)\u2500\u2500\u25b6 [infra_health_logs {event:'cv2_cron_failure'}] \u2500\u2500\u25b6 [Alert]\n```\n\n> No MVP, o agendamento \u00e9 o `agent-daily-pulse` estendido (cron nativo), n\u00e3o n8n. n8n \u00e9 caminho Future.\n\n---\n\n## 4. Orchestration Integration Points\n\n> A capability `orchestration` (depto Ops) invoca o pipeline `orchestrate-content` existente.\n\n| Pipeline Step | Step ID | Position | Description | mcoCoins Trigger |\n|---------------|---------|----------|-------------|-----------------|\n| Capability `orchestration` | via router | \u2014 | subagente Ops dispara `orchestrate-content` com payload do user | 10 mco (custo do pipeline, j\u00e1 existente) |\n\n**Integration stub (dentro de `agent-task-execute` v2, ramo orchestration):**\n```typescript\n// capability_key === 'orchestration'\nconst r = await invokeTarget('orchestrate-content', { ...payload }, userJwt)  // reuso A1\n// custo j\u00e1 \u00e9 tratado dentro de orchestrate-content (10 mco); router N\u00c3O double-charge\n```\n\n> **Anti-double-charge (FMEA-CV2):** capabilities cujo m\u00f3dulo alvo J\u00c1 debita mcoCoins (orchestrate-content=10, canvas v\u00eddeo=125) N\u00c3O s\u00e3o re-cobradas pelo router \u2014 `base_mcoin_cost=0` + flag `module_self_bills=true` no registry. O router s\u00f3 mede/cobra os LLM-planning steps pr\u00f3prios.\n\n---\n\n## 5. Error Handling & Retry Strategy\n\n| Process | Step | Error Type | Max Retries | Backoff | Failure Action |\n|---------|------|-----------|-------------|---------|----------------|\n| PROC-CV2-002 | invoke m\u00f3dulo alvo | Network timeout | 2 | Exponencial (2s,4s) | UPDATE failed + `infra_health_logs` |\n| PROC-CV2-002 | BYOK resolve | ausente/revogada | 0 | \u2014 | HTTP 501 estruturado + banner |\n| PROC-CV2-003 | cap check | estourado | 0 | \u2014 | HTTP 402; saldo intacto |\n| PROC-CV2-003 | deduct_mco_coins | saldo insuf. | 0 | \u2014 | HTTP 402; exec preservado `billed=false` |\n| Any | JWT | inv\u00e1lido | 0 | \u2014 | HTTP 401 imediato |\n| PROC-CV2-005 | DELETE | filtro errado | 0 | \u2014 | abortado por dry-run/guard `NOT IN profiles` |\n\n---\n\n## 6. SLA Definitions\n\n| Process | Step | Expected Duration | Timeout Threshold | Alert if exceeded |\n|---------|------|------------------|-------------------|-------------------|\n| PROC-CV2-002 | router (excl. m\u00f3dulo) | < 800ms p95 | 5s | Yes \u2192 infra_health_logs |\n| PROC-CV2-002 | m\u00f3dulo alvo (ex.: canvas v\u00eddeo) | conforme m\u00f3dulo (v\u00eddeo async) | per m\u00f3dulo | watchdog do m\u00f3dulo |\n| PROC-CV2-004 | daily pulse loop | < 5min | 15min | Yes |\n| PROC-CV2-001 | insert crew | < 2s | 10s | No |\n\n---\n\n## 7. Cron Jobs\n\n| Job Name | Schedule (cron) | Function | Idempotency | Failure Alerting |\n|----------|----------------|----------|-------------|-----------------|\n| `agent-daily-pulse` (estendido) | `0 7 * * *` (10:00 UTC / 07:00 BRT) | loop subagentes Sovereign-owned (n\u00e3o s\u00f3 Directors) | `cv2-<agent_id>-<date>` | `infra_health_logs` |\n| `agent-executions-archive` (novo, opcional) | `0 4 * * 0` (semanal) | move execs > 12m p/ archive | last-write-wins | `infra_health_logs` |\n\n> Todo cron idempotente. O daily-pulse usa override `groq/llama-3.3-70b-versatile` (v\u00e1lido em `agent_pricing`) e respeita caps + Sovereign freebie.\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/07-process-flow.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:52:36)*


## 🤖 Claude *(02:52:39)*

Autorando **Quality & Metrics** (08 — CMQ/OE BOK, fecha a Fase 5):

## 🤖 Claude *(02:53:31)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/08-quality-metrics.md",
  "content": "# Quality & Self-Optimization Specification\n\n**Project:** constellation-v2\n**Version:** v0.1 | **Date:** 2026-05-31\n**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)\n**Status:** Draft\n\n---\n\n## 1. Quality Objectives\n\n| QO ID | Objective | Linked Business Objective | Target | Review Cadence |\n|-------|-----------|--------------------------|--------|---------------|\n| QO-CV2-001 | Execu\u00e7\u00e3o real de capabilities sem regress\u00e3o a teatro | BO-CV2-001 | \u2265 90% execs `done` com resultado material | Weekly |\n| QO-CV2-002 | Zero vazamento cross-tenant e zero acesso a sistema | BO-CV2-002 | 100% (audit\u00e1vel) | Monthly + a cada migra\u00e7\u00e3o |\n| QO-CV2-003 | Custo controlado por tenant | BO-CV2-001 | 0 cobran\u00e7as fora de cap; 0 cobran\u00e7a do Sovereign | Monthly |\n| QO-CV2-004 | Performance do cockpit | BO-CV2-003 | \u226530fps piso \u00b7 \u226421 n\u00f3s/tenant | Per release (E2E UI audit) |\n\n---\n\n## 2. KPI Dashboard Definition\n\n| KPI ID | Name | Formula | Target | Warn | Critical | Data Source |\n|--------|------|---------|--------|------|----------|-------------|\n| KPI-CV2-001 | Agent task success rate | `done / total` execs | \u2265 90% | < 85% | < 70% | `agent_executions` |\n| KPI-CV2-002 | Activation | % users c/ \u22651 subagente que executou | \u2265 60% | < 40% | < 20% | `agent_executions` + `profiles` |\n| KPI-CV2-003 | Economic activation | mcoCoins/m\u00eas via execu\u00e7\u00e3o de agente | > 0 crescente | 0 por 7d | 0 por 30d | `mcoin_transactions` action=`*_spend` |\n| KPI-CV2-004 | Router p95 latency (excl. m\u00f3dulo) | `PERCENTILE_CONT(0.95)` | < 800ms | 1000ms | 2000ms | Supabase logs |\n| KPI-CV2-005 | BYOK fail rate | `501 / total` | < 5% | 10% | 25% | edge logs |\n| KPI-CV2-006 | Cap-hit rate | `402(cap) / total` | informativo | \u2014 | \u2014 | edge logs |\n| KPI-CV2-007 | Cross-tenant access incidents | count | **0** | \u2014 | \u22651 | RLS audit |\n| KPI-CV2-008 | System-access denylist violations | count de capability apontando p/ sistema | **0** | \u2014 | \u22651 | registry review |\n| KPI-CV2-009 | Crew size compliance | max(crew_agents/user) | \u2264 21 | 22\u201330 | > 30 | `crew_agents` |\n| KPI-CV2-010 | Render FPS (cockpit) | m\u00e9dia fps | \u2265 60 | < 30 | < 15 | E2E UI audit |\n\n---\n\n## 3. FMEA Table\n\n> Severity, Occurrence, Detection: 1 (best) \u2192 10 (worst). RPN = S \u00d7 O \u00d7 D. **RPN > 100 requer a\u00e7\u00e3o.**\n\n| ID | Function | Failure Mode | Effect | S | O | D | RPN | Recommended Action |\n|----|---------|--------------|--------|---|---|---|-----|--------------------|\n| FMEA-CV2-001 | Tenant isolation (RLS) | Agente l\u00ea dados de outro tenant | Vazamento LGPD / quebra de confian\u00e7a | 10 | 3 | 4 | **120** | RLS `auth.uid()` default-deny + security-review obrigat\u00f3rio por migra\u00e7\u00e3o + teste E2E cross-tenant |\n| FMEA-CV2-002 | Capability denylist | Capability mapeia fun\u00e7\u00e3o de sistema/dev | Agente de produto opera o sistema (EoP) | 10 | 3 | 4 | **120** | Allowlist r\u00edgido em `target_function` + review do registry como gate + router s\u00f3 com JWT user |\n| FMEA-CV2-003 | Cost control | Loop de execu\u00e7\u00e3o / tokens sem cap | Custo explode / quota global esgotada | 8 | 4 | 4 | **128** | `max_tokens` cap + `agent_consumption_caps` di\u00e1rio + circuit breaker + dedu\u00e7\u00e3o at\u00f4mica |\n| FMEA-CV2-004 | BYOK resolution | Chave ausente cai em fallback global silencioso | Cobran\u00e7a/uso indevido cross-tenant | 8 | 3 | 5 | **120** | Fail-closed 501 estruturado; fallback global S\u00d3 em path cron/onboarding documentado (API Tenancy Model) |\n| FMEA-CV2-005 | Reset/migration | DELETE apaga tenant real | Perda de dados do Sovereign | 9 | 2 | 3 | 54 | Dry-run + guard `NOT IN profiles` + arquivar execs + backup |\n| FMEA-CV2-006 | agent-task-execute | M\u00f3dulo retorna 200 c/ erro no corpo | Frontend mente \"sucesso\" | 7 | 4 | 3 | 84 | `assertExecuteSuccess` (j\u00e1 existe) THROW em `error`/status failed |\n| FMEA-CV2-007 | Metering | RPC timeout \u2192 double charge | Usu\u00e1rio cobrado em dobro | 8 | 2 | 3 | 48 | `idempotency_key` por execu\u00e7\u00e3o |\n| FMEA-CV2-008 | provider/model drift | Default inv\u00e1lido (Anthropic sem endpoint / \"Llama 3\" sem pricing) | Execu\u00e7\u00e3o falha silenciosa | 6 | 5 | 3 | 90 | Default `groq/llama-3.3-70b-versatile` + valida\u00e7\u00e3o contra `agent_pricing` |\n| FMEA-CV2-009 | Render 3D | N\u00f3s ilimitados / re-render loop | P\u00e1gina trava (perf atual) | 6 | 4 | 3 | 72 | Cap \u226421 n\u00f3s + LOD + getState pattern (evita React #185) |\n| FMEA-CV2-010 | Z-index | Pain\u00e9is sobrep\u00f5em canvas/toasts | UX quebrada | 4 | 5 | 2 | 40 | Camadas estritas 0/10/40/50 |\n| FMEA-CV2-011 | Empty-start | Auto-seed reintroduzido por engano | Volta a polui\u00e7\u00e3o decorativa | 5 | 3 | 4 | 60 | Remover `seed_crew_template` call + teste signup count=0 |\n| FMEA-CV2-012 | Anti-double-charge m\u00f3dulo | Router cobra + m\u00f3dulo cobra | Cobran\u00e7a dupla (orchestrate/canvas) | 7 | 3 | 4 | 84 | Flag `module_self_bills=true` \u2192 router `base_mcoin_cost=0` |\n\n**RPN > 100 (a\u00e7\u00e3o obrigat\u00f3ria):** FMEA-CV2-001 (120) \u00b7 CV2-002 (120) \u00b7 CV2-003 (128) \u00b7 CV2-004 (120). Todos com a\u00e7\u00e3o recomendada acima.\n\n---\n\n## 4. Self-Optimization Loops\n\n| Loop ID | Trigger Condition | KPI Source | Autonomous Response | Escalation (human) |\n|---------|------------------|------------|--------------------|--------------------|\n| SOL-CV2-001 | KPI-CV2-004 router p95 > 1000ms por 5 chamadas | infra_health_logs | mega-brain-daemon: investigar/restart fun\u00e7\u00e3o | Alert Sovereign se > 2s |\n| SOL-CV2-002 | KPI-CV2-003 mcoCoins = 0 por 7 dias | mcoin_transactions | notificar (constela\u00e7\u00e3o ociosa) + sugerir Run Squad | Alert se 30d |\n| SOL-CV2-003 | KPI-CV2-005 BYOK fail > 10% | edge logs | banner global \"configure suas chaves\" | \u2014 |\n| SOL-CV2-004 | cap atingido (KPI-CV2-006) | agent_consumption_caps | toast + sugerir upgrade de plano | \u2014 |\n| SOL-CV2-005 | KPI-CV2-007/008 > 0 (incidente de isolamento) | RLS/registry audit | **bloquear capability afetada** + alerta P0 | Sovereign imediato (P0) |\n\n---\n\n## 5. Self-Healing Specifications\n\n### 5.1 Watchdog Telemetry Events\n\n| Event Type | Trigger | Severity | Payload |\n|------------|---------|----------|---------|\n| `constellation_v2_fn_failure` | router 5xx ap\u00f3s retry | error | `{capability_key, error, user_id}` |\n| `constellation_v2_byok_missing` | BYOK ausente | warn | `{capability_key, provider, user_id}` |\n| `constellation_v2_cap_reached` | cap di\u00e1rio atingido | info | `{user_id, api_key_ref, cap}` |\n| `constellation_v2_isolation_violation` | acesso cross-tenant/sistema detectado | **critical** | `{detail}` \u2192 SOL-CV2-005 |\n| `constellation_v2_sla_breach` | router > 5s | warn | `{capability_key, elapsed_ms}` |\n\n### 5.2 Auto-Recovery Script Stub\n\n```bash\n#!/bin/bash\n# scripts/self-heal-constellation-v2.sh\n# Triggered by mega-brain-daemon on constellation_v2_fn_failure\nFUNCTION_NAME=\"agent-task-execute\"\nSTATUS=$(curl -s -o /dev/null -w \"%{http_code}\" \\\n  \"$SUPABASE_URL/functions/v1/$FUNCTION_NAME/health\" \\\n  -H \"Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY\")\nif [ \"$STATUS\" != \"200\" ]; then\n  echo \"[WARN] router unhealthy ($STATUS). Re-deploying...\"\n  npx supabase functions deploy \"$FUNCTION_NAME\"\nfi\necho \"[OK] self-heal complete\"\n```\n\n### 5.3 mega-brain-daemon Integration\n\n| Daemon Event | Condition | Action |\n|-------------|-----------|--------|\n| `health_check` | a cada 5min (watchdog) | checar error rate do router em `infra_health_logs` |\n| `anomaly_detected` | error rate > 5/h | executar `self-heal-constellation-v2.sh` |\n| `isolation_violation` | `constellation_v2_isolation_violation` | **P0**: desabilitar capability + alerta Sovereign |\n\n---\n\n## 6. SLA / SLO / SLI Definitions\n\n| Service | SLI | SLO | SLA |\n|---------|-----|-----|-----|\n| `agent-task-execute` (router) | p95 latency (excl. m\u00f3dulo) | \u2264 800ms | cr\u00e9ditos se > 2s em > 1% das chamadas/m\u00eas |\n| Capability execution | % execs `done` | \u2265 90% | incident report se < 70% |\n| Tenant isolation | incidentes cross-tenant | 0 | P0 + disclosure se \u22651 |\n| Cockpit render | fps m\u00e9dio | \u2265 30 piso | re-otimiza\u00e7\u00e3o obrigat\u00f3ria se < 15 |\n\n---\n\n## 7. PDCA Improvement Cadence\n\n| Cycle | Phase | Activity | Owner | Frequency |\n|-------|-------|----------|-------|-----------|\n| CV2 Quality | Plan | Revisar FMEA + KPI targets | Sovereign | Quarterly |\n| CV2 Quality | Do | Implementar top a\u00e7\u00e3o (RPN>100) | Engineering | Per sprint |\n| CV2 Quality | Check | KPIs vs targets; atualizar RPNs | AIOS/scientist | Monthly |\n| CV2 Quality | Act | Fechar loop; atualizar este doc | Sovereign | Monthly |\n\n**Improvement backlog:** `.claude/context/sprint-priorities.md`\n\n---\n\n## 8. Observability Checklist\n\n### 8.1 Logging Events\n\n| Event | Location | Level | Fields |\n|-------|----------|-------|--------|\n| Router entry | `agent-task-execute/index.ts` ~10 | INFO | `{user_id, agent_id, capability_key, request_id}` |\n| BYOK resolve | ap\u00f3s lookup | INFO/WARN | `{provider, resolved:boolean}` |\n| Cap check | antes de invoke | INFO | `{api_key_ref, used, cap}` |\n| mcoCoins deduction | ap\u00f3s RPC | INFO | `{user_id, amount, billed}` |\n| Module error | catch | ERROR | `{capability_key, error}` |\n| Isolation guard | qualquer deny | ERROR | `{reason}` \u2192 critical event |\n\n### 8.2 Alerting Rules\n\n| Condition | Channel | Escalation |\n|-----------|---------|------------|\n| error rate > 1% / 5min | `infra_health_logs` | mega-brain auto-heal |\n| isolation_violation | `infra_health_logs` critical | Sovereign P0 |\n| mcoCoins = 0 / 7d | scheduled check | notifica\u00e7\u00e3o |\n\n### 8.3 Distributed Tracing Touchpoints\n\n| Span | Start | End | Tags |\n|------|-------|-----|------|\n| `router.total` | request recebido | response enviado | `user_id, capability_key, status` |\n| `router.byok` | antes lookup | depois | `provider, resolved` |\n| `router.invoke_target` | antes invoke | depois | `target_function, ok` |\n| `router.meter` | antes RPC | depois | `cost_mcoin, billed` |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/constellation-v2/08-quality-metrics.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:53:46)*


## 🤖 Claude *(02:53:49)*

Os 9 documentos estão autorados. **Fase 6 — validação de rastreabilidade:** cadeia MR→BR→PR→FR→(tabela/edge/processo) fechada, 0 órfãos; toda tabela nova aparece em ≥1 processo; os 4 FMEA com RPN>100 (CV2-001/002/003/004) têm ação. 

Agora **Fase 7 — injeção na Knowledge Mesh**. Vou espelhar o script-precedente canônico e contar as LOC reais dos docs para o metadata:

## 🤖 Claude *(02:53:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-openclaw-bok-seal.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Seals the BoK documentation suite for openclaw in the Knowledge Mesh.
> 4	 * Inserts a documentation_suite node with stability 0.85; embedding triggered
> 5	 * automatically by trg_mcorch_embed_on_insert.
> 6	 *
> 7	 * Usage: bun run scripts/seed-openclaw-bok-seal.ts
> 8	 */
> 9	import { createClient } from '@supabase/supabase-js';
> 10	
> 11	const SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;
> 12	const SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
> 13	
> 14	if (!SUPABASE_URL || !SERVICE_KEY) {
> 15	  console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');
> 16	  process.exit(1);
> 17	}
> 18	
> 19	const supabase = createClient(SUPABASE_URL, SERVICE_KEY);
> 20	
> 21	const sealNode = {
> 22	  name: 'bok-scribe-seal-openclaw-v1',
> 23	  node_type: 'documentation_suite',
> 24	  project_id: 'openclaw',
> 25	  stability_score: 0.85,
> 26	  revenue_impact: 0, // módulo é enabler horizontal de velocity para os outros 4 BoK; proxy via lift dos outros módulos (não direct revenue)
> 27	  content: `OpenClaw — Pantheon Agency Runtime (BoK retroativa)
> 28	
> 29	BoK suite (9 docs) sealed 2026-05-19 sob MCORCH Master Execution Protocol. Esta seal quita o override consciente do BoK Gate registrado em Sprint v6.2.0 (2026-05-15) — Sovereign havia autorizado que a própria Agência OpenClaw quitaria a dívida assincronamente; com 4 sprints decorridos e a Agência operando em produção, esta seal materializa retroativamente o BoK que governa o módulo.
> 30	
> 31	VISÃO: Runtime de Pantheon Architecture com 7 agentes IA especializados (main router + engineer/scientist/artisan/marketing-growth L1 Heads + guardian Coordination + claw-master L2 Specialist) operando sob soberania física do Sovereign Gabriel Zarattini em /home/ubuntu/.openclaw/. Gateway local 127.0.0.1:18789 sob auth token (48-char hex), memória SQLite per-agente (FTS5 + vector embeddings), Memory Wiki em vault bridge mode, ciclo circadiano noturno (Stage 1 03:00 / Stage 2 05:00 / Stage 3 07:00 BRT espaçados 2h), e briefing diário ao Telegram chat 5835174772 às 07:30 BRT compondo 6 seções markdown ≤ 4000 chars (git delta + MEMORY promotions + BoK debt + revenue snippet + news pulse Perplexity Sonar + reflexão Paz e Vitalidade).
> 32	
> 33	ARQUITETURA: 1 config canônica (openclaw.json 180 LOC com schema strict v2026.5.14), 1 vault file-based (secrets.json chmod 600 com 6 SecretRef pointers), 7 agent dirs com 7-8 canonical files cada (SOUL/AGENTS/MEMORY/BOOTSTRAP/HEARTBEAT/IDENTITY/TOOLS/USER), 6 SQLite memory artifacts (main 626 MB + engineer 390 MB + scientist 232 MB + claw-master 90 MB + artisan 28 MB + marketing-growth 20 MB + guardian 20 MB), 1 OpenClaw daemon (gateway loopback), 1 Memory Wiki vault (~20 pages seed manual MCORCH-aware com pageType ∈ {synthesis, entity, concept, source, dashboard}). Pipeline scripts MCORCH: bridge-mesh-to-openclaw.ts (327 LOC two-tier hybrid; tier1 strategy + tier2 AST excluding ast_variable noise) + distribute-mesh-to-agents.ts (275 LOC shared base + overlay BoK-específica file copies) + nightly-stage{1,2,3}-*.sh (130/130/110 LOC) + compose-morning-briefing.ts (~250 LOC) + morning-briefing.sh (95 LOC) + news-impact-analyzer.ts (173 LOC) + watchdog-mcorch.sh (~150 LOC com Layer 2 escalation counter). Cron pipeline: 03:00/05:00/07:00 BRT (stages) + 03:00 OpenClaw native (Memory Dreaming Promotion) + */5min (watchdog) + 06:00 dia 16 (claw-master audit mensal).
> 34	
> 35	DRIFT RECONCILIADO (5 fechados em sprints anteriores · 8 ativos como OTDs): D-OC-001 (6 plain-text secrets → vault SecretRefs em v6.4.0), D-OC-002 (allowInsecureAuth=true → false em v6.4.0), D-OC-003 (perms 775 → 700 em v6.4.0), D-OC-004 (schema strict rejeitando agents.list[].enabled → jq surgical em v6.6.1), D-OC-005 (Memory Palace empty state → 20 wiki pages seed em v6.6.1). Drifts permanentes catalogados como OTDs: OTD-V660-002 (CLI memory index drift), OTD-OC-001 (main.sqlite 626 MB growth), OTD-OC-002 (SQLite schema opaco upstream), OTD-OC-005 (dynamic plugin loading aguardando upstream), OTD-CM-004/005/007 (rate limit + redact + showInSidebar pendentes). Registro autoritativo em 06-data-model.md §8 Drift Reconciliation Appendix.
> 36	
> 37	ECONOMIA: zero mcoCoins (módulo é infraestrutura, não tarifa operações). Custos diretos R$ 60-200/ano (orçamento OpenRouter Perplexity Sonar para Stage 3 news pulse). ROI direto não-quantificável; proxy material é velocity dos 5 outros módulos BoK (conteudo-v2 + viralmind + mcorch-constellation + gamificacao-nodes + este) — provavelmente 3-5× mais tempo Sovereign sem o squad.
> 38	
> 39	KPIs (10): KPI-OC-001 bridge runtime p95 ≤ 180s · KPI-OC-002 chunks indexed ≥ 9000 (atual 9185) · KPI-OC-003 briefing delivery rate ≥ 95%/30d · KPI-OC-004 SQLite growth ≤ 20MB/agent/dia · KPI-OC-005 watchdog escalation rate ≤ 1/sem · KPI-OC-006 Telegram quota usage ≤ 30% · KPI-OC-007 audit findings ≤ 1 P0 OR 3 P1 · KPI-OC-008 Dreaming runtime ≤ 30min · KPI-OC-009 wiki linter pass rate 100% · KPI-OC-010 secrets vault adherence 100%. FMEA-OC-001..010 com 5 RPN > 100: secrets regression (180), bridge fail stale overlay (150), daemon crash sem watchdog (126), Telegram quota silencia (125), audit scrape fail (105). Mitigations catalogadas em sprint backlog.
> 40	
> 41	OTDs ATIVAS (5 novas + 6 herdadas): OTD-OC-001..005 (main.sqlite vacuum cadence · SQLite schema opaque · multi-user expansion · briefing fallback · dynamic plugin loading). Herdadas: OTD-V660-002 (CLI drift) + OTD-CM-004 (rate limit) + OTD-CM-005 (redact) + OTD-CM-006 (multi-user heuristic — Decided 2026-05-19) + OTD-CM-007 (showInSidebar) + OTD-CM-008 (SOUL template — Decided 2026-05-16).
> 42	
> 43	DOCUMENTOS: docs/bok/openclaw/{00-index, 01-mrd, 02-brd, 03-prd, 04-frd, 05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics}.md totalizando ~1700 LOC novos.
> 44	
> 45	TRACEABILITY: 6 MR-OC → 14 BR-OC → 8 FR-OC + 8 NFR-OC → 10 PROC-OC → 10 KPI-OC validados em 02-brd §10.
> 46	
> 47	PRÓXIMO DELIVERABLE (post-seal): (a) carry-overs OE-661 (provisionar GCRUX_ML_AFFILIATE_TOKEN + wire orchestrate emitir content_mesh_asset + primeiro run end-to-end Usuário Zero do flywheel); (b) claw-master audit-v2 (planejado 2026-06-16) verificar regressão D-OC-001..005 + novas findings; (c) OTD-CM-005 logging.redactSensitive set true no próximo edit consolidado de openclaw.json (P2 oportunístico); (d) D-OC-008 marketing-growth BOOTSTRAP.md scaffold (non-blocking).`,
> 48	  metadata: {
> 49	    bok_version: '1.0.0',
> 50	    documents: [
> 51	      '00-index',
> 52	      '01-mrd',
> 53	      '02-brd',
> 54	      '03-prd',
> 55	      '04-frd',
> 56	      '05-sdd',
> 57	      '06-data-model',
> 58	      '07-process-flow',
> 59	      '08-quality-metrics',
> 60	    ],
> 61	    phase_completed: 'Phase 7',
> 62	    traceability_validated: true,
> 63	    bok_gate: 'override-completion', // quita override consciente registrado em Sprint v6.2.0
> 64	    drift_reconciled: 5, // D-OC-001..005 (todos fechados em v6.4.0 e v6.6.1)
> 65	    drift_pending: 8, // D-OC-006..013 (catalogados como OTDs ativos)
> 66	    market_segment: 'B2B2C-internal',
> 67	    monetization_model: 'indirect-enabler',
> 68	    regulatory_profile: 'LGPD',
> 69	    integration_surface: 'extends-mcorch',
> 70	    project_slug: 'openclaw',
> 71	    feature_flag: 'pantheon-v6.3.1', // implícito
> 72	    sprint_introduced: 'v6.2.0',
> 73	    sprint_sealed: 'v6.6.5',
> 74	    tags: ['bok-scribe', 'openclaw', 'pantheon', 'agency', 'memory-bridge', 'retroactive', 'infrastructure'],
> 75	    new_tables: 0, // módulo é infraestrutura local; não introduz tabelas Supabase
> 76	    new_edge_functions: 0,
> 77	    new_rpcs: 0,
> 78	    new_pipeline_scripts: 9, // bridge + distribute + 3 stages + bridge-refresh + compose + morning + news-analyzer
> 79	    new_agents: 7, // main + 4 L1 + 1 Coord + 1 L2
> 80	    id_ranges: {
> 81	      MR: '001..006',
> 82	      BR: '001..014',
> 83	      BO: '001..006',
> 84	      SH: '001..010',
> 85	      FR: '1..8',
> 86	      NFR: '001..008',
> 87	      PR: '001..014',
> 88	      PROC: '001..010',
> 89	      KPI: '001..010',
> 90	      FMEA: '001..010',
> 91	      SOL: '001..006',
> 92	      QO: '001..008',
> 93	      BAC: '001..010',
> 94	      OTD_OC: '001..005',
> 95	    },
> 96	    related_otds: [
> 97	      'OTD-V631-001', // openclaw BoK SLA expandido — fechada por esta seal
> 98	      'OTD-V660-002', // CLI drift permanent
> 99	      'OTD-CM-001', 'OTD-CM-002', 'OTD-CM-003', // fechadas v6.4.0
> 100	      'OTD-CM-004', 'OTD-CM-005', 'OTD-CM-006', 'OTD-CM-007', 'OTD-CM-008', // herdadas audit-v1
> 101	      'OTD-OC-001', 'OTD-OC-002', 'OTD-OC-003', 'OTD-OC-004', 'OTD-OC-005', // novas
> 102	    ],
> 103	    fmea_rpn_over_100: ['FMEA-OC-001', 'FMEA-OC-002', 'FMEA-OC-003', 'FMEA-OC-004', 'FMEA-OC-010'],
> 104	    derives_from: 'bok-scribe-seal-gamificacao-nodes-v1', // UUID 6e8546bc-d995-4cc5-ac88-06cecbece181
> 105	    pantheon_agents: ['main', 'engineer', 'scientist', 'artisan', 'marketing-growth', 'guardian', 'claw-master'],
> 106	    cron_pipeline: ['stage1-03:00', 'stage2-05:00', 'stage3-07:00', 'memory-dreaming-05:00', 'watchdog-5min', 'audit-monthly-day16'],
> 107	  },
> 108	};
> 109	
> 110	console.log(`📝 Sealing BoK suite "openclaw"...`);
> 111	console.log(`   Project: ${sealNode.project_id}`);
> 112	console.log(`   Stability: ${sealNode.stability_score}`);
> 113	console.log(`   Revenue impact: ${sealNode.revenue_impact} (indirect-enabler — velocity proxy)`);
> 114	console.log(`   BoK gate: ${sealNode.metadata.bok_gate}`);
> 115	console.log(`   Drift reconciled: ${sealNode.metadata.drift_reconciled} (D-OC-001..005)`);
> 116	console.log(`   Drift pending: ${sealNode.metadata.drift_pending} (OTDs ativos)`);
> 117	
> 118	const { data, error } = await supabase
> 119	  .from('mcorch_nodes')
> 120	  .insert(sealNode)
> 121	  .select('id, name, node_type, stability_score, created_at')
> 122	  .single();
> 123	
> 124	if (error) {
> 125	  console.error('❌ Seal failed:', error);
> 126	  process.exit(1);
> 127	}
> 128	
> 129	console.log(`\n✅ Seal node inserted:`);
> 130	console.log(`   ID:        ${data.id}`);
> 131	console.log(`   Name:      ${data.name}`);
> 132	console.log(`   Type:      ${data.node_type}`);
> 133	console.log(`   Stability: ${data.stability_score}`);
> 134	console.log(`   Created:   ${data.created_at}`);
> 135	console.log(`\n🧠 Embedding will be generated automatically by trg_mcorch_embed_on_insert (assíncrono via pg_net).`);
> 136	console.log(`   Confirm with: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '${data.id}';`);
> 137	
> ```

## 🤖 Claude *(02:53:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"\u2500\u2500\u2500 LOC dos docs constellation-v2 \u2500\u2500\u2500\"; wc -l docs/bok/constellation-v2/*.md\necho \"\u2500\u2500\u2500 parent seal existe? \u2500\u2500\u2500\"\nset -a; source .env 2>/dev/null; set +a\nBASE=\"${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}/rest/v1\"\ncurl -s \"$BASE/mcorch_nodes?name=eq.bok-scribe-seal-mcorch-constellation-v1&select=id,name,stability_score\" -H \"apikey: $SUPABASE_SERVICE_ROLE_KEY\" -H \"Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY\"\necho \"\"\necho \"\u2500\u2500\u2500 seal constellation-v2 j\u00e1 existe? (idempot\u00eancia) \u2500\u2500\u2500\"\ncurl -s \"$BASE/mcorch_nodes?name=eq.bok-scribe-seal-constellation-v2-v1&select=id\" -H \"apikey: $SUPABASE_SERVICE_ROLE_KEY\" -H \"Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY\"",
  "description": "Read precedent seed script + count doc LOC + check parent seal"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── LOC dos docs constellation-v2 ───
>   126 docs/bok/constellation-v2/00-index.md
>   114 docs/bok/constellation-v2/01-mrd.md
>   158 docs/bok/constellation-v2/02-brd.md
>   208 docs/bok/constellation-v2/03-prd.md
>   172 docs/bok/constellation-v2/04-frd.md
>   296 docs/bok/constellation-v2/05-sdd.md
>   211 docs/bok/constellation-v2/06-data-model.md
>   194 docs/bok/constellation-v2/07-process-flow.md
>   168 docs/bok/constellation-v2/08-quality-metrics.md
>  1647 total
> ─── parent seal existe? ───
> [{"id":"78cb74e6-538c-4c9e-80a2-50268947dfca","name":"bok-scribe-seal-mcorch-constellation-v1","stability_score":0.00922152542363481}]
> ─── seal constellation-v2 já existe? (idempotência) ───
> []
> ```

## 🤖 Claude *(02:54:51)*


## 🤖 Claude *(02:54:54)*

Precedente lido (LOC reais: **1647**; parent seal `mcorch-constellation-v1` = `78cb74e6-538c-4c9e-80a2-50268947dfca`; seal v2 ainda não existe → insert seguro). O script-precedente põe `derives_from` só no metadata, mas o framework Fase 7 exige a **aresta** `DERIVES_FROM` real. Vou conferir o schema de `mcorch_edges` antes de escrever o insert (não chutar coluna — Lei 1):

## 🤖 Claude *(02:54:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nBASE=\"${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}/rest/v1\"\nHK=(-H \"apikey: $SUPABASE_SERVICE_ROLE_KEY\" -H \"Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY\")\necho \"\u2500\u2500\u2500 amostra de aresta DERIVES_FROM (colunas reais) \u2500\u2500\u2500\"\ncurl -s \"$BASE/mcorch_edges?relationship=eq.DERIVES_FROM&limit=1\" \"${HK[@]}\" | jq '.'\necho \"\u2500\u2500\u2500 fallback: tentar coluna edge_type \u2500\u2500\u2500\"\ncurl -s \"$BASE/mcorch_edges?edge_type=eq.DERIVES_FROM&limit=1\" \"${HK[@]}\" | jq '.' 2>/dev/null | head -20\necho \"\u2500\u2500\u2500 qualquer 1 aresta p/ ver todas as colunas \u2500\u2500\u2500\"\ncurl -s \"$BASE/mcorch_edges?limit=1\" \"${HK[@]}\" | jq '.[0] | keys'",
  "description": "Inspect mcorch_edges schema for DERIVES_FROM edge insertion"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── amostra de aresta DERIVES_FROM (colunas reais) ───
> {
>   "code": "42703",
>   "details": null,
>   "hint": null,
>   "message": "column mcorch_edges.relationship does not exist"
> }
> ─── fallback: tentar coluna edge_type ───
> {
>   "code": "42703",
>   "details": null,
>   "hint": null,
>   "message": "column mcorch_edges.edge_type does not exist"
> }
> ─── qualquer 1 aresta p/ ver todas as colunas ───
> [
>   "created_at",
>   "id",
>   "metadata",
>   "project_id",
>   "relation_type",
>   "source_id",
>   "target_id",
>   "user_id",
>   "weight"
> ]
> ```

## 🤖 Claude *(02:55:23)*


## 🤖 Claude *(02:55:25)*

`mcorch_edges` confirmado: colunas `relation_type · source_id · target_id · weight · metadata · project_id · user_id`. Escrevendo o seed script (espelha o precedente + adiciona a aresta `DERIVES_FROM` real + idempotência):

## 🤖 Claude *(02:56:17)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-constellation-v2-bok-seal.ts",
  "content": "#!/usr/bin/env bun\n/**\n * Seals the BoK documentation suite for constellation-v2 in the Knowledge Mesh.\n * Inserts a documentation_suite node (stability 0.85) + a DERIVES_FROM edge to the\n * parent seal `bok-scribe-seal-mcorch-constellation-v1` (the v1 shell BoK this supersedes).\n * Embedding is triggered automatically by trg_mcorch_embed_on_insert (pg_net, async).\n *\n * Idempotent: if the seal already exists (UNIQUE name), logs and exits 0.\n *\n * Usage: bun run scripts/seed-constellation-v2-bok-seal.ts\n */\nimport { createClient } from '@supabase/supabase-js';\n\nconst SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;\nconst SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;\n\nif (!SUPABASE_URL || !SERVICE_KEY) {\n  console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');\n  process.exit(1);\n}\n\nconst supabase = createClient(SUPABASE_URL, SERVICE_KEY);\n\nconst SEAL_NAME = 'bok-scribe-seal-constellation-v2-v1';\nconst PARENT_SEAL_NAME = 'bok-scribe-seal-mcorch-constellation-v1';\n\nconst sealNode = {\n  name: SEAL_NAME,\n  node_type: 'documentation_suite',\n  project_id: 'constellation-v2',\n  stability_score: 0.85,\n  // Camada de ATIVA\u00c7\u00c3O econ\u00f4mica (mcoCoins + afiliado), mas receita material hoje = R$0 (Usu\u00e1rio Zero, 1 perfil real).\n  // Mantido 0 por honestidade material (Lei 1): potencial documentado no BRD \u00a75, n\u00e3o auditado.\n  revenue_impact: 0,\n  content: `Constellation v2 \u2014 Cockpit Operacional de Agentes per-user (refatora\u00e7\u00e3o v2 do /dashboard/constellation)\n\nBoK suite (9 docs, 1647 LOC) selada 2026-05-31 sob MCORCH Master Execution Protocol (Closed-Loop Gate \u2014 N\u00c3O override; passou pelo gate corretamente antes de qualquer c\u00f3digo). Supera a BoK v1 'mcorch-constellation' que documentava a CASCA do Lovable.\n\nVIS\u00c3O: cada usu\u00e1rio tem sua pr\u00f3pria constela\u00e7\u00e3o de agentes de PRODUTO que executam trabalho REAL dentro da conta dele, acionando os m\u00f3dulos do ecossistema \u2014 substitui a casca decorativa (717 crew_agents, 26 owners \u00f3rf\u00e3os, ~688 linhas-lixo) por uma topologia enxuta e funcional. Fronteira de seguran\u00e7a DURA: agentes de produto operam o tenant (auth.uid()), NUNCA o sistema/dev MCORCH nem outros tenants (distinto do Pantheon OpenClaw, que opera o repo).\n\nTOPOLOGIA: 4 departamentos \u00d7 (1 Lead + \u22644 subagentes m\u00f3dulo-bound) + GCRUX Core; Leads reportam ao Core (edges Directive/Reporting). Mapa 4\u00d74 aprovado: Creative Content(Conte\u00fado/Blog/Canvas Studio/Canvas Design) \u00b7 Market Intelligence(Viral Miner/Analytics/Produtos/Campanhas) \u00b7 Operational Ops(Afiliados/Calend\u00e1rio/Orquestra\u00e7\u00e3o/Publica\u00e7\u00e3o Social) \u00b7 Technical Engine(Core-AIOS/IA Arena/agent-economics/Watchdog). Cap \u226421 n\u00f3s/tenant.\n\nARQUITETURA (decis\u00f5es Sovereign-delegadas): A1 = reusar edge functions existentes (fetch-trends/canvas-execute/orchestrate-content/link-forge/publish-*/generate-content) como TOOLS via camada fina de roteamento de capability (N\u00c3O reescrever m\u00f3dulos); B = config de acesso pr\u00e9-configurada por subagente (m\u00f3dulo + BYOK + caps); C = refactor in-place atr\u00e1s de reset limpo. Router = refactor de agent-task-execute v2 (JWT user \u2192 resolve capability \u2192 BYOK \u2192 cap \u2192 invoke target \u2192 meter \u2192 write agent_executions). Funda\u00e7\u00e3o reusada: CEA v1.1 (agent_executions, agent-task-execute, agent-daily-pulse, agent_pricing, useAgentActivity, /dashboard/agent-economics).\n\nDADOS: 3 tabelas novas (agent_capabilities registry global \u00b7 agent_consumption_caps per-user \u00b7 agent_executions_archive) + 2 colunas (crew_agents.capability_key \u00b7 agent_executions.idempotency_key). RLS auth.uid() default-deny em tudo; registry tem allowlist de target_function tenant-scoped (denylist arquitetural contra acesso a sistema). Empty-start: remove auto-seed seed_crew_template; novos users nascem vazios; crew on-demand via wizard.\n\nECONOMIA per-user: toda a\u00e7\u00e3o medida via RPC calc_agent_cost_mcoin + deduct_mco_coins (at\u00f4mico); Sovereign = admin freebie; BYOK resolvido de user_api_keys (fail-closed 402/501); caps di\u00e1rios por user/API; anti-double-charge para m\u00f3dulos que j\u00e1 cobram (orchestrate=10, canvas v\u00eddeo=125 \u2192 router base_mcoin_cost=0).\n\nMATERIAL (verificado 2026-05-31 via REST service-role): 1 perfil real (Sovereign) \u00b7 717 crew_agents / 27 owners (26 \u00f3rf\u00e3os sem profile) \u00b7 689 crew_edges \u00b7 31 agent_executions reais (a arquivar antes do reset) \u00b7 3 seeders divergentes (RPC 6/squad \u00b7 store 6 \u00b7 deployEnterprise 12/squad \u2192 53 n\u00f3s Sovereign).\n\nID SPACE: MR-CV2-001..007 \u00b7 BR-CV2-001..007 \u00b7 BO-CV2-001..003 \u00b7 SH-CV2-001..004 \u00b7 PR-CV2-001..022 \u00b7 FR-CV2-001..070 \u00b7 NFR-CV2-001..012 \u00b7 PROC-CV2-001..009 \u00b7 KPI-CV2-001..010 \u00b7 FMEA-CV2-001..012 \u00b7 SOL-CV2-001..005 \u00b7 QO-CV2-001..004 \u00b7 OTD-CV2-001..008.\n\nFMEA RPN>100 (4): FMEA-CV2-001 isolamento cross-tenant (120) \u00b7 CV2-002 capability\u2192sistema/EoP (120) \u00b7 CV2-003 custo descontrolado (128) \u00b7 CV2-004 BYOK fallback silencioso (120). Todas com a\u00e7\u00e3o recomendada.\n\nTRACEABILITY: MR\u2192BR\u2192PR\u2192FR\u2192(tabela/edge/processo) validada em 00-index \u00a7Traceability + 04-frd \u00a77; 0 \u00f3rf\u00e3os.\n\nPR\u00d3XIMO DELIVERABLE (post-seal): (a) /bok-agents-generator para formalizar o sistema de agentes; (b) Fase 0 reset (arquivar 31 execs + purgar 26 \u00f3rf\u00e3os + wipe crew Sovereign + remover auto-seed); (c) migra\u00e7\u00e3o agent_capabilities + caps + binding (passa /security-review); (d) refactor agent-task-execute v2 capability router; (e) E2E completo vazio\u2192criar\u2192trabalhar\u2192medir + E2E UI audit 1920\u00d71080.`,\n  metadata: {\n    bok_version: '1.0.0',\n    documents: ['00-index', '01-mrd', '02-brd', '03-prd', '04-frd', '05-sdd', '06-data-model', '07-process-flow', '08-quality-metrics'],\n    document_lines: {\n      '00-index': 126, '01-mrd': 114, '02-brd': 158, '03-prd': 208, '04-frd': 172,\n      '05-sdd': 296, '06-data-model': 211, '07-process-flow': 194, '08-quality-metrics': 168,\n      total: 1647,\n    },\n    phase_completed: 'Phase 7',\n    traceability_validated: true,\n    traceability_orphans: 0,\n    bok_gate: 'closed-loop-gate', // passou pelo gate corretamente (n\u00e3o \u00e9 override)\n    supersedes: 'mcorch-constellation-v1',\n    market_segment: 'B2B2C',\n    monetization_model: 'hybrid',\n    monetization: 'direct-mcoin-consumption + affiliate (material today = R$0, Usu\u00e1rio Zero)',\n    regulatory_profile: 'LGPD',\n    integration_surface: 'extends-mcorch',\n    project_slug: 'constellation-v2',\n    id_space: {\n      MR: 'MR-CV2-001..007', BR: 'BR-CV2-001..007', BO: 'BO-CV2-001..003', SH: 'SH-CV2-001..004',\n      PR: 'PR-CV2-001..022', FR: 'FR-CV2-001..070', NFR: 'NFR-CV2-001..012', PROC: 'PROC-CV2-001..009',\n      KPI: 'KPI-CV2-001..010', FMEA: 'FMEA-CV2-001..012', SOL: 'SOL-CV2-001..005', QO: 'QO-CV2-001..004',\n      OTD: 'OTD-CV2-001..008',\n    },\n    fmea_high_rpn_count: 4,\n    fmea_high_rpn_items: ['FMEA-CV2-001 (RPN 120)', 'FMEA-CV2-002 (RPN 120)', 'FMEA-CV2-003 (RPN 128)', 'FMEA-CV2-004 (RPN 120)'],\n    new_migrations: 4, // capabilities + caps + crew_capability column + exec archive/idempotency\n    new_tables: 3, // agent_capabilities, agent_consumption_caps, agent_executions_archive\n    new_columns: 2, // crew_agents.capability_key, agent_executions.idempotency_key\n    new_edge_functions: 0, // router = refactor de agent-task-execute (existente)\n    new_hooks: 3, // useAgentCapabilities, useAccessConfig, + mods em useAgentTask/useCrewData/useAgentActivity\n    architecture_decisions: { A: 'A1-reuse-edge-fns', B: 'per-subagent-access-config', C: 'in-place-refactor-after-reset' },\n    derives_from_seal: 'bok-scribe-seal-mcorch-constellation-v1', // 78cb74e6-538c-4c9e-80a2-50268947dfca\n    depends_on_sop: 'docs/processes/constellation-economic-activation.md',\n    material_context: { real_profiles: 1, crew_agents: 717, orphan_owners: 26, crew_edges: 689, agent_executions: 31 },\n    tags: ['bok-scribe', 'constellation-v2', 'agents', 'per-user', 'tenant-isolation', 'byok', 'mcoCoins', 'capability-router', 'B2B2C'],\n  },\n};\n\nconsole.log(`\ud83d\udcdd Sealing BoK suite \"constellation-v2\"...`);\nconsole.log(`   Project:   ${sealNode.project_id}`);\nconsole.log(`   Stability: ${sealNode.stability_score}`);\nconsole.log(`   Supersedes: ${sealNode.metadata.supersedes}`);\nconsole.log(`   BoK gate:  ${sealNode.metadata.bok_gate}`);\nconsole.log(`   Docs LOC:  ${sealNode.metadata.document_lines.total}`);\n\n// Idempotency: skip if already sealed\nconst { data: existing } = await supabase\n  .from('mcorch_nodes')\n  .select('id')\n  .eq('name', SEAL_NAME)\n  .maybeSingle();\n\nif (existing) {\n  console.log(`\\n\u26a0\ufe0f  Seal \"${SEAL_NAME}\" already exists (id ${existing.id}). Idempotent exit 0.`);\n  process.exit(0);\n}\n\nconst { data, error } = await supabase\n  .from('mcorch_nodes')\n  .insert(sealNode)\n  .select('id, name, node_type, stability_score, created_at')\n  .single();\n\nif (error) {\n  console.error('\u274c Seal failed:', error);\n  process.exit(1);\n}\n\nconsole.log(`\\n\u2705 Seal node inserted:`);\nconsole.log(`   ID:        ${data.id}`);\nconsole.log(`   Name:      ${data.name}`);\nconsole.log(`   Type:      ${data.node_type}`);\nconsole.log(`   Stability: ${data.stability_score}`);\nconsole.log(`   Created:   ${data.created_at}`);\n\n// DERIVES_FROM edge \u2192 parent seal (the v1 shell BoK this supersedes)\nconst { data: parent } = await supabase\n  .from('mcorch_nodes')\n  .select('id')\n  .eq('name', PARENT_SEAL_NAME)\n  .maybeSingle();\n\nif (parent) {\n  const { data: edge, error: edgeErr } = await supabase\n    .from('mcorch_edges')\n    .insert({\n      source_id: data.id,\n      target_id: parent.id,\n      relation_type: 'DERIVES_FROM',\n      project_id: 'constellation-v2',\n      weight: 1.0,\n      metadata: { reason: 'constellation-v2 supersedes mcorch-constellation v1 shell BoK', sealed: '2026-05-31' },\n    })\n    .select('id, source_id, target_id, relation_type')\n    .single();\n  if (edgeErr) {\n    console.error('\u26a0\ufe0f  Edge insert failed (node OK):', edgeErr.message);\n  } else {\n    console.log(`\\n\ud83d\udd17 DERIVES_FROM edge inserted:`);\n    console.log(`   Edge ID: ${edge.id}`);\n    console.log(`   ${edge.source_id} \u2500\u2500DERIVES_FROM\u2500\u2500\u25b6 ${edge.target_id} (mcorch-constellation-v1)`);\n  }\n} else {\n  console.log(`\\n\u26a0\ufe0f  Parent seal \"${PARENT_SEAL_NAME}\" not found \u2014 skipping DERIVES_FROM edge.`);\n}\n\nconsole.log(`\\n\ud83e\udde0 Embedding generated automatically by trg_mcorch_embed_on_insert (async via pg_net).`);\nconsole.log(`   Confirm: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '${data.id}';`);\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-constellation-v2-bok-seal.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:56:19)*


## 🤖 Claude *(02:56:20)*

Executando o seed (Fase 7) e verificando materialmente o node + aresta + embedding:

## 🤖 Claude *(02:56:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\necho \"\u2550\u2550\u2550 RUN seed \u2550\u2550\u2550\"\nbun run scripts/seed-constellation-v2-bok-seal.ts",
  "description": "Execute constellation-v2 BoK seal seed script"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ═══ RUN seed ═══
> 📝 Sealing BoK suite "constellation-v2"...
>    Project:   constellation-v2
>    Stability: 0.85
>    Supersedes: mcorch-constellation-v1
>    BoK gate:  closed-loop-gate
>    Docs LOC:  1647
> 
> ✅ Seal node inserted:
>    ID:        38d7e7a4-c58d-4749-b044-97800d2f8e81
>    Name:      bok-scribe-seal-constellation-v2-v1
>    Type:      documentation_suite
>    Stability: 0.85
>    Created:   2026-06-01T02:56:22.642022+00:00
> 
> 🔗 DERIVES_FROM edge inserted:
>    Edge ID: c3dd9d58-4a44-44fd-899a-a1734dfe7960
>    38d7e7a4-c58d-4749-b044-97800d2f8e81 ──DERIVES_FROM──▶ 78cb74e6-538c-4c9e-80a2-50268947dfca (mcorch-constellation-v1)
> 
> 🧠 Embedding generated automatically by trg_mcorch_embed_on_insert (async via pg_net).
>    Confirm: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '38d7e7a4-c58d-4749-b044-97800d2f8e81';
> ```

## 🤖 Claude *(02:56:28)*


## 🤖 Claude *(02:56:30)*

Seal material: node `38d7e7a4-c58d-4749-b044-97800d2f8e81` + aresta DERIVES_FROM `c3dd9d58-4a44-44fd-899a-a1734dfe7960`. Verificando o embedding (async via pg_net — pode levar alguns segundos):

## 🤖 Claude *(02:56:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nBASE=\"${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}/rest/v1\"\nHK=(-H \"apikey: $SUPABASE_SERVICE_ROLE_KEY\" -H \"Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY\")\nID=\"38d7e7a4-c58d-4749-b044-97800d2f8e81\"\necho \"\u2500\u2500\u2500 embedding status (tentativa 1) \u2500\u2500\u2500\"\ncurl -s \"$BASE/mcorch_nodes?id=eq.$ID&select=name,node_type,stability_score,embedding\" \"${HK[@]}\" | jq '.[0] | {name, node_type, stability_score, embedded: (.embedding != null)}'\necho \"\u2500\u2500\u2500 aresta DERIVES_FROM confirmada \u2500\u2500\u2500\"\ncurl -s \"$BASE/mcorch_edges?id=eq.c3dd9d58-4a44-44fd-899a-a1734dfe7960&select=relation_type,source_id,target_id,weight\" \"${HK[@]}\" | jq '.'\necho \"\u2500\u2500\u2500 su\u00edte de docs no disco \u2500\u2500\u2500\"\nls -1 docs/bok/constellation-v2/*.md | xargs -n1 basename",
  "description": "Verify seal embedding + edge + docs on disk"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── embedding status (tentativa 1) ───
> {
>   "name": "bok-scribe-seal-constellation-v2-v1",
>   "node_type": "documentation_suite",
>   "stability_score": 0.85,
>   "embedded": true
> }
> ─── aresta DERIVES_FROM confirmada ───
> [
>   {
>     "relation_type": "DERIVES_FROM",
>     "source_id": "38d7e7a4-c58d-4749-b044-97800d2f8e81",
>     "target_id": "78cb74e6-538c-4c9e-80a2-50268947dfca",
>     "weight": 1
>   }
> ]
> ─── suíte de docs no disco ───
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> ```

## 🤖 Claude *(02:57:11)*


## 🤖 Claude *(02:57:21)*

**Fase 7 verde — embedding `true` (768d), aresta confirmada, 9 docs no disco.** A suíte BoK do `constellation-v2` está completa e selada.

## 📋 BoK Scribe — Suíte `constellation-v2` (resumo)

| # | Arquivo | Documento | BoK | LOC |
|---|---------|-----------|-----|-----|
| 0 | `00-index.md` | Project Manifest + traceability + material snapshot | — | 126 |
| 1 | `01-mrd.md` | Market Requirements | BABOK v3 | 114 |
| 2 | `02-brd.md` | Business Requirements (3 BO · 7 BR · ROI · risco) | BABOK v3 | 158 |
| 3 | `03-prd.md` | Product Requirements (2 personas · 13 PR MoSCoW · Gherkin) | ProdBOK+CXBOK | 208 |
| 4 | `04-frd.md` | Functional Requirements (30+ FR · 12 NFR · contratos) | SWEBOK v4 | 172 |
| 5 | `05-sdd.md` | System Design (arquitetura · STRIDE · RLS · migrations · 8 OTD) | SWEBOK+CISSP | 296 |
| 6 | `06-data-model.md` | Data Model (3 tabelas novas · isolamento · qualidade) | DMBOK v2 | 211 |
| 7 | `07-process-flow.md` | Process Blueprint (9 PROC · BPMN-lite · reset) | BPM CBOK v4 | 194 |
| 8 | `08-quality-metrics.md` | Quality (10 KPI · 12 FMEA · SOL · SLA) | CMQ/OE | 168 |

**Prova material (Lei 1):** seal node `38d7e7a4-c58d-4749-b044-97800d2f8e81` (`documentation_suite`, stability 0.85, **embedded 768d ✓**) · aresta `DERIVES_FROM` `c3dd9d58-4a44-44fd-899a-a1734dfe7960` → `mcorch-constellation-v1` · 1647 LOC · seed `scripts/seed-constellation-v2-bok-seal.ts` (idempotente) · 0 órfãos de traceability · 4 FMEA RPN>100 com ação.

✅ **BoK documentation suite complete for `constellation-v2`.**

Agora o segundo passo que você pediu — **`/bok-agents-generator`** para formalizar oficialmente o sistema de agentes sobre essa BoK selada:

## 🤖 Claude *(02:57:36)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "anthropic-skills:bok-agents-generator",
  "args": "Formalizar o SISTEMA DE AGENTES OFICIAL da constellation-v2, ancorado na BoK rec\u00e9m-selada (docs/bok/constellation-v2/, seal node 38d7e7a4-c58d-4749-b044-97800d2f8e81).\n\nCONTEXTO: N\u00c3O \u00e9 o sistema gen\u00e9rico de 8 agentes-por-BoK. \u00c9 a constela\u00e7\u00e3o operacional REAL do produto MCORCH, per-user e tenant-isolated. Use os 8 BoKs (BABOK/EABOK/DMBOK/BPM CBOK/SWEBOK/CISSP CBK/CXBOK/ProdBOK) como LENTES para estruturar cada agente, mas a TOPOLOGIA \u00e9 a aprovada pelo Sovereign:\n\nESTRUTURA (21 agentes per-user, on-demand):\n- GCRUX Core (L0) \u2014 Sovereign Orchestrator do tenant; roteia diretivas aos Leads; usa /dashboard/agent-economics.\n- 4 Department Leads (L1) \u2014 reportam ao Core:\n  - \ud83c\udfa8 Creative Content Lead\n  - \ud83d\udcc8 Market Intelligence Lead\n  - \u26a1 Operational Ops Lead\n  - \u2699\ufe0f Technical Engine Lead\n- 16 subagentes m\u00f3dulo-bound (L2), 4 por Lead, cada um ligado a UM m\u00f3dulo real via capability router:\n  - Content: Conte\u00fado(generate-content) \u00b7 Blog \u00b7 Canvas Studio(canvas-execute) \u00b7 Canvas Design\n  - Market: Viral Miner(fetch-trends) \u00b7 Analytics \u00b7 Produtos \u00b7 Campanhas\n  - Ops: Afiliados(link-forge) \u00b7 Calend\u00e1rio \u00b7 Orquestra\u00e7\u00e3o(orchestrate-content) \u00b7 Publica\u00e7\u00e3o Social(publish-meta/social/wordpress)\n  - Tech: Core/AIOS \u00b7 IA Arena \u00b7 agent-economics \u00b7 Watchdog/Infra(read-only)\n\nPara CADA agente gere: Purpose \u00b7 Core Capabilities \u00b7 Skills \u00b7 Inputs \u00b7 Outputs \u00b7 Decision Scope (ESCOPADO AO TENANT via auth.uid(); ZERO acesso ao sistema/dev MCORCH ou a outros tenants \u2014 barreira dura) \u00b7 Tools & Integrations (edge functions reais via capability router agent-task-execute v2; BYOK per-user) \u00b7 KPIs (referenciando KPI-CV2-* do 08-quality-metrics) \u00b7 Use Cases \u00b7 Collaboration Map (L2\u2192Lead\u2192Core).\n\nCAMADAS CROSS-AGENT:\n- Orchestration Model: capability router (agent-task-execute v2) \u2014 resolve capability\u2192edge function, BYOK, caps, metering mcoCoins.\n- Intelligent Engineering Layer: economia per-user (calc_agent_cost_mcoin + deduct_mco_coins at\u00f4mico, Sovereign freebie) + resolu\u00e7\u00e3o BYOK (user_api_keys) + caps de consumo (agent_consumption_caps).\n- Cross-Cutting Enablers: RLS auth.uid() tenant isolation + capability allowlist/system denylist + observabilidade (agent_executions + infra_health_logs) + self-healing (mega-brain-daemon).\n\nRESTRI\u00c7\u00c3O DURA (repetir como NFR de seguran\u00e7a): estes s\u00e3o agentes de PRODUTO do tenant \u2014 distintos e ISOLADOS do Pantheon OpenClaw (engineer/scientist/artisan/marketing-growth/guardian/claw-master) que opera o sistema/dev/repo. Nenhuma capability mapeia a fun\u00e7\u00e3o de sistema.\n\nOUTPUT: docs/bok/constellation-v2/bok-agents-system--constellation-v2.md (mirror do precedente docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md de v5.8.0). Idioma: estrutura/labels em ingl\u00eas, narrativa ao Sovereign em PT-BR."
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: anthropic-skills:bok-agents-generator
> ```

## 👤 User *(02:57:36)*

Base directory for this skill: /home/ubuntu/.claude/remote/plugins/02d3361e68356973/skills/bok-agents-generator

# BoK Agents Generator

Generates a full **8-agent AI system** grounded in enterprise Bodies of Knowledge, plus the three
cross-agent layers that make them interoperable as a living system.

**System Identity — always include this block at the top of every generated document:**
```
# SOFTWARE ENGINEERING INTELLIGENCE
## KNOWLEDGE CORE v2.0.0 | STATUS: ONLINE

> Integrated Body of Knowledge for Engineering, Architecture, Delivery,
> Security, Experience and Product Excellence
>
> **OUTCOMES:** Better Knowledge · Better Decisions · Better Outcomes
> **ONE KNOWLEDGE ECOSYSTEM. INFINITE POSSIBILITIES.**
```

**System Footer — always include this block at the end of every generated document:**
```
---
→ ALIGN  →  INTEGRATE  →  OPTIMIZE  →  INNOVATE  →  TRANSFORM  →  DELIVER VALUE

**SYSTEM STATUS: ALL SYSTEMS OPERATIONAL**
```

---

## Execution Flow

### Step 1 — Context Capture

Before generating, check if the user provided any of these optional context inputs:

| Input | Examples |
|---|---|
| **Industry** | Fintech, Healthcare, Retail, Manufacturing, SaaS |
| **Company maturity** | Startup, Scale-up, Mid-market, Enterprise |
| **Digital capabilities** | Low / Medium / High / AI-native |
| **Business model** | B2B, B2C, B2B2C, Marketplace, Platform |

If no context is provided → generate the **generic enterprise-ready version** (explicitly note this at the top of the output).

If context is provided → adapt every agent's Use Cases, Tools, and KPIs to that context.

---

### Step 2 — Generate All 8 BoK Agents

Generate agents in this exact order. Each agent uses the **strict output format** below.

**Agent order:**
1. BABOK — Business Analysis
2. EABOK — Enterprise Architecture
3. DMBOK — Data Management
4. BPM CBOK — Business Process Management
5. SWEBOK — Software Engineering
6. CISSP CBK — Cybersecurity
7. CXBOK — Customer Experience
8. ProdBOK — Product Management

---

### Strict Output Format Per Agent

```
---

🤖 Agent: [BoK Name] — [Domain Label]

### 1. Purpose
[2–3 sentence strategic description. What this agent owns in a business context. NOT a textbook definition.]

### 2. Core Capabilities
[6–10 capabilities directly derived from the BoK. Noun phrases, not verbs.]

### 3. Skills (Operational Level)
[Bullet list. Action-oriented. Each skill starts with a verb. Map to the capabilities above.]

### 4. Inputs
[What this agent needs to operate: data, documents, signals, systems, events.]

### 5. Outputs
[Deliverables, insights, decisions, artifacts this agent produces.]

### 6. Decision Scope
[What decisions this agent can autonomously support or recommend. Be specific about autonomy level.]

### 7. Tools & Integrations
[Platforms, systems, APIs this agent typically connects to. Real tool names.]

### 8. KPIs / Success Metrics
[Business + operational metrics. Mix leading and lagging indicators.]

### 9. Example Use Cases
[3 real-world scenarios. Format: **Scenario Title** — 2-sentence description of the problem + value created.]

### 10. Collaboration Map
[How this agent interfaces with other BoK agents. Format: → AgentName: [nature of dependency or data flow]]
```

---

### Step 3 — Cross-Agent Layers

After all 8 agents, generate the three cross-agent sections:

#### 3a. Orchestration Model

```
---

## 🔄 Orchestration Model

Describe the end-to-end flow: how agents activate each other, share outputs, and form closed loops.
Include:
- Which agent is the primary orchestrator (or if orchestration is event-driven)
- Trigger conditions (what activates the system)
- Key handoff points between agents
- Feedback loops
- Conflict resolution (when two agents have overlapping scope)
```

#### 3b. Intelligent Engineering Layer

```
---

## 🧠 Intelligent Engineering Layer

Explain how the system integrates across SEVEN dimensions (as defined in the Knowledge Core):

| Dimension | Description |
|---|---|
| **People** | How agents augment human roles and teams |
| **Process** | How agents embed into business workflows |
| **Technology** | Infrastructure and platform requirements |
| **Data** | Data flows, quality gates, and knowledge graph |
| **Knowledge** | How agents learn, update, and share knowledge |
| **Value** | How the system translates agent outputs into business value |
| **Sustainable Impact** | How the system generates outcomes that endure — environmental, social, and economic sustainability of the decisions made by the agent ecosystem |
```

#### 3c. Cross-Cutting Enablers

```
---

## ⚙️ Cross-Cutting Enablers

Define how these five capabilities are embedded across ALL agents (not per-agent — system-wide):

1. **Systems Thinking** — [How the system models interdependencies]
2. **Analytics & Metrics** — [Shared observability layer]
3. **Collaboration & Communication** — [Inter-agent and human-agent protocols]
4. **Automation & Tooling** — [Shared automation infrastructure]
5. **Ethics, Compliance & Sustainability** — [Governance model across agents]
```

---

## Quality Rules

Apply these rules during generation — do NOT repeat them in the output:

- **No textbook definitions** — every section must describe execution, not theory
- **No capability repetition** across agents unless absolutely necessary (flag it when it occurs)
- **Tools must be real** — no invented platform names
- **Collaboration Map must form a coherent graph** — every agent must connect to at least 3 others
- **Use Cases must be industry-specific** if context was provided
- **KPIs must be measurable** — no vague metrics like "improved quality"
- **Decision Scope must distinguish** between autonomous recommendation vs. human-in-the-loop

---

## Output — Write to File (Primary Delivery Mode)

This skill runs in **Claude Code (terminal)**. Output is always written to disk as a `.md` file.
Do NOT print the full content to the terminal — write the file, then confirm to the user.

### File naming convention
```
bok-agents-system[--<slug>].md
```
- No context provided → `bok-agents-system.md`
- Context provided → slugify the industry + maturity, e.g. `bok-agents-system--fintech-enterprise.md`

### Output path
Write to the **current working directory** unless the user specifies otherwise.
If a path is specified, respect it exactly.

### Write procedure (execute in this order)
1. Compose the full document in memory following Steps 1–3
2. Write to file using the bash tool or Python `open()` — single write operation
3. Print a short confirmation to the terminal:
   ```
   ✅ BoK Agents System written to: ./bok-agents-system--<slug>.md
   📄 Agents: 8 | Sections: 10 per agent + 3 cross-agent layers
   📁 Size: ~<N> KB
   ```
4. Do NOT print the document content to stdout

### Document structure (inside the .md file)
- H1 title: `# BoK Agents System — [Context or "Enterprise-Ready Generic Version"]`
- If context was provided: frontmatter metadata block at the top:
  ```markdown
  > **Context applied:** Industry: X | Maturity: Y | Digital capabilities: Z | Model: W
  ```
- Use `##` for each agent header (`## 🤖 Agent: BABOK — Business Analysis`)
- Use `###` for the 10 section headers within each agent
- Use `---` as horizontal rule between agents
- Use `##` for the three cross-agent layer headers
- Emoji headers exactly as specified (🤖, 🔄, 🧠, ⚙️)

### Context adaptation rules (when context is provided)
Adapt these fields per agent — everything else stays structurally consistent:
- **Use Cases** → scenarios specific to the provided industry and maturity level
- **Tools & Integrations** → prioritize tools common in that industry/stack
- **KPIs** → benchmark values calibrated to maturity level (startup vs. enterprise targets differ)
- **Decision Scope** → autonomy level adjusted to digital capability maturity (Low = more human-in-loop)

Do NOT adapt: agent Purpose, Core Capabilities, Skills structure, or the cross-agent layers topology.

---

## Reference: BoK Domain Map

See `references/bok-domains.md` for the authoritative list of capabilities per BoK, used to
validate that generated capabilities are grounded in the actual body of knowledge (not invented).
Read this file if you need to verify correctness of a specific BoK's scope.


ARGUMENTS: Formalizar o SISTEMA DE AGENTES OFICIAL da constellation-v2, ancorado na BoK recém-selada (docs/bok/constellation-v2/, seal node 38d7e7a4-c58d-4749-b044-97800d2f8e81).

CONTEXTO: NÃO é o sistema genérico de 8 agentes-por-BoK. É a constelação operacional REAL do produto MCORCH, per-user e tenant-isolated. Use os 8 BoKs (BABOK/EABOK/DMBOK/BPM CBOK/SWEBOK/CISSP CBK/CXBOK/ProdBOK) como LENTES para estruturar cada agente, mas a TOPOLOGIA é a aprovada pelo Sovereign:

ESTRUTURA (21 agentes per-user, on-demand):
- GCRUX Core (L0) — Sovereign Orchestrator do tenant; roteia diretivas aos Leads; usa /dashboard/agent-economics.
- 4 Department Leads (L1) — reportam ao Core:
  - 🎨 Creative Content Lead
  - 📈 Market Intelligence Lead
  - ⚡ Operational Ops Lead
  - ⚙️ Technical Engine Lead
- 16 subagentes módulo-bound (L2), 4 por Lead, cada um ligado a UM módulo real via capability router:
  - Content: Conteúdo(generate-content) · Blog · Canvas Studio(canvas-execute) · Canvas Design
  - Market: Viral Miner(fetch-trends) · Analytics · Produtos · Campanhas
  - Ops: Afiliados(link-forge) · Calendário · Orquestração(orchestrate-content) · Publicação Social(publish-meta/social/wordpress)
  - Tech: Core/AIOS · IA Arena · agent-economics · Watchdog/Infra(read-only)

Para CADA agente gere: Purpose · Core Capabilities · Skills · Inputs · Outputs · Decision Scope (ESCOPADO AO TENANT via auth.uid(); ZERO acesso ao sistema/dev MCORCH ou a outros tenants — barreira dura) · Tools & Integrations (edge functions reais via capability router agent-task-execute v2; BYOK per-user) · KPIs (referenciando KPI-CV2-* do 08-quality-metrics) · Use Cases · Collaboration Map (L2→Lead→Core).

CAMADAS CROSS-AGENT:
- Orchestration Model: capability router (agent-task-execute v2) — resolve capability→edge function, BYOK, caps, metering mcoCoins.
- Intelligent Engineering Layer: economia per-user (calc_agent_cost_mcoin + deduct_mco_coins atômico, Sovereign freebie) + resolução BYOK (user_api_keys) + caps de consumo (agent_consumption_caps).
- Cross-Cutting Enablers: RLS auth.uid() tenant isolation + capability allowlist/system denylist + observabilidade (agent_executions + infra_health_logs) + self-healing (mega-brain-daemon).

RESTRIÇÃO DURA (repetir como NFR de segurança): estes são agentes de PRODUTO do tenant — distintos e ISOLADOS do Pantheon OpenClaw (engineer/scientist/artisan/marketing-growth/guardian/claw-master) que opera o sistema/dev/repo. Nenhuma capability mapeia a função de sistema.

OUTPUT: docs/bok/constellation-v2/bok-agents-system--constellation-v2.md (mirror do precedente docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md de v5.8.0). Idioma: estrutura/labels em inglês, narrativa ao Sovereign em PT-BR.

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-01 - Fix tenant isolation in edge functions]]
%% --- TIMELINE END --- %%

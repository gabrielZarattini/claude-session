# Próximos passos do projeto
**Date:** 2026-06-20 | **Session ID:** `cdba5e5b-0613-433e-84ae-1ff6e559e8c5`

---

## 👤 User *(02:11:36)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(02:11:36)*

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


## 🤖 Claude *(02:11:41)*


## 🤖 Claude *(02:11:42)*

I'll execute the ShakeHands /handson pick-up ritual. Starting with pre-flight checks in parallel.

## 🤖 Claude *(02:11:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin 2>&1 | tail -3; echo \"---LOG---\"; git log --oneline -7; echo \"---STATUS---\"; git status --short; echo \"---DIFFSTAT---\"; git diff HEAD --stat; echo \"---BEHIND---\"; git rev-list --count HEAD..origin/main 2>/dev/null",
  "description": "Git fetch + history + status + drift vs origin"
}
```

## 🤖 Claude *(02:11:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20; echo \"---TSC-DONE---\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---LOG---
> a8f14a3 chore(sprint): registra v6.42.0 — Viral Autopilot BoK 9/9 (motor de conteúdo viral autônomo)
> 0613899 docs(handoff): seal Viral Autopilot BoK 9/9 — motor de conteúdo viral autônomo (R1-R4)
> 2c56211 docs(readme): v6.42.0 — Viral Autopilot BoK 9/9 (motor de conteúdo viral autônomo)
> 8da7a58 docs(bok): sela viral-autopilot — motor de conteúdo viral autônomo (R1-R4)
> 776687f chore(sprint): registra v6.41.0 — Unified Sensorial Canvas (Epsilon V9) Fases 3.1-3.4
> d84b806 docs(handoff): seal Unified Sensorial Canvas (Epsilon V9) — AGI→ASI ref + emenda BoK + Fases 3.1-3.4
> 08b36eb docs(readme): v6.41.0 — Unified Sensorial Canvas (Epsilon V9) Code+Memory+Black Hole R3F
> ---STATUS---
> ---DIFFSTAT---
> ---BEHIND---
> 0
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---TSC-DONE---
> ```

## 🤖 Claude *(02:11:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat; echo \"\"; echo \"---BOK---\"; ls docs/bok/ 2>/dev/null; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"; echo \"---HANDOFF-LINES---\"; wc -l HANDOFF.md",
  "description": "Docker containers, Chroma health, BoK suites, scratch, HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 2 days (healthy)
> mcorch_claude_mem: Up 4 days (healthy)
> mcorch_chroma: Up 4 days (healthy)
> ---
> mega-brain-dashboard: Up 4 days
> mega-brain-webhook: Up 4 days (healthy)
> mega-brain-daemon: Up 4 days (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1781921508412088783}
> ---BOK---
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
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> ---SCRATCH---
> scratch has files
> ---HANDOFF-LINES---
> 8060 HANDOFF.md
> ```

## 🤖 Claude *(02:11:49)*


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
> 14	## Session Seal — Viral Autopilot BoK 9/9: motor de conteúdo viral autônomo monetizado por afiliado ML (R1-R4) (2026-06-17)
> 15	
> 16	`/handson` → diretiva do Sovereign de **retomar o objetivo-núcleo de receita**: alimentar contas de redes sociais com conteúdo viral gerado automaticamente e agendado (tudo de uma vez OU a cada N dias), que a cada ciclo analisa o desempenho anterior para melhorar os próximos criativos — monetizado com afiliado do Mercado Livre. Arco Closed-Loop respeitado de ponta a ponta: **auditoria material → 4 decisões soberanas → BoK 9/9 → validação adversarial → seal**. Nenhum código de produto foi escrito (BoK-only); o BoK Gate está agora ABERTO.
> 17	
> 18	**O que foi entregue:**
> 19	1. **Auditoria material (workflow 7 agentes, prova path:linha):** o pipeline existente é um gerador de blog/social B2B genérico com receita ML madura — **R1/R4 parciais e vivos** (`orchestrate-content`→`orchestrate-step` gera texto; `affiliate_config`/click-ledger/`handle-ml-postback` per-user provados), mas **R2 (recorrência a cada 3 dias) e R3 (loop auto-melhorável) AUSENTES**: `campaign_metrics` sem writer, `optimization_policy` nunca lida por gerador, `self-optimize` sem cron; monetização só no artigo (3 SKUs hardcoded por regex), `affiliate_url` da UI dropado, `fetch-trends` desconectado.
> 20	2. **4 decisões soberanas (AskUserQuestion):** suite-mãe NOVO `viral-autopilot` (não emenda nem override) · MVP texto+imagem nas redes atuais (WP/LinkedIn/X; vídeo+TikTok/IG/YT fase 2) · sinal R3 **combo** (cliques afiliado + engajamento orgânico + receita postback) · 3 SKUs semente (Roborock S8 / Samsung Neo QLED 8K / Family Hub).
> 21	3. **BoK 9/9 selada (1889 LOC)** em `docs/bok/viral-autopilot/` (MR/BR-VA-001..008 · PR-VA-001..022 · **FR-VA-001..021** · 8 NFR · 8 OTD · 12 FMEA com 4 RPN>100). Unifica R1-R4 e é dona explícita do orquestrador do ciclo.
> 22	4. **Validação Fase 6 — 4 rodadas adversariais** (workflow 4 críticos/rodada) + grep determinístico: R1 NO_GO (2 blockers+7 high) → R2 NO_GO (2 blockers, **1 que eu introduzi**: refund por `deduct` negativo viola o RPC anti-mint `20260603220000:45`) → R3 GO_WITH_FIXES → R4 GO_WITH_FIXES (síntese caiu por session-limit; críticos OK). Pegou um **buraco de segurança real**: cron `verify_jwt=false` confiava no header `x-autopilot-user-id` sem provar service-role in-function → drenaria saldo de vítima.
> 23	5. **Design final cravado pela validação:** cron prova service-role in-function (`Bearer SB_SECRET_KEY`, padrão `orchestrate-step:50-53`) ANTES de confiar no header · RPCs `begin_autopilot_cycle` (advisory-lock anti-TOCTOU do cap diário + pré-débito atômico) + `finalize_autopilot_cycle` (refund **crédito positivo** via `add_mco_coins` ledgered) · `N_runs = produtos×redes×ab_variants` (imagem no bundle de 10) · FK COMPOSTA tenant-escopada · `campaign_metrics` deprecada → `creative_metrics` canônica · `optimization_policy` com `scope='viral_autopilot:<plan_id>'`.
> 24	
> 25	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (4 decisões via AskUserQuestion + GO de seal) + 4 rodadas de validação adversarial independente · Owner=Sovereign (blast radius = conteúdo autônomo publicado + gasto de carteira do tenant).
> 26	
> 27	| Verificação (material) | Resultado |
> 28	|---|---|
> 29	| BoK 9/9 selada | ✅ `docs/bok/viral-autopilot/` 9 docs · 1889 LOC (wc -l) |
> 30	| Seal node na malha | ✅ `documentation_suite` `b3398294-aa75-4810-845b-3a15cfe802e7` · embedding **NOT NULL 768d** |
> 31	| DERIVES_FROM edge | ✅ `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed` |
> 32	| Validação adversarial | ✅ 4 rodadas (9→4→4→2 high; 0 blocker desde R3) + grep determinístico limpo |
> 33	| tsc | ✅ zero erros |
> 34	| Commits | `8da7a58` (BoK suite+seed) · `2c56211` (readme) · (handoff) |
> 35	
> 36	### Survival Laws Self-audit
> 37	```
> 38	Law 1 (Materiality): ✅ Auditoria com prova path:linha (não auto-declarada); BoK validada em 4 rodadas adversariais independentes + grep determinístico; seal node UUID + embedding 768d verificados por REST real; NÃO fabriquei número de janela de contexto (admiti "sem medidor preciso, estima-se por volume"). Refund-negativo (que EU introduzi) pego pela validação e corrigido. Fase 5c a executar abaixo.
> 39	Law 2 (Process): ✅ Closed-Loop respeitado — auditoria + BoK ANTES de qualquer código; SOP `autopilot-cron-identity.md` registrado como gate Lei 2 (OTD-VA-008) ANTES da fatia de cadência. BoK-only seal (zero código de produto).
> 40	Law 3 (Pruning): ✅ Sessão empacotada inteira (handson→audit→BoK→4 validações→seal) sob GO explícito do Sovereign; outputs de workflow referenciados por path, não recarregados.
> 41	Law 4 (ORO): ✅ Triplet declarado; 4 decisões de escopo + GO de seal pelo Sovereign; validação adversarial independente como Reviewer mecânico.
> 42	```
> 43	
> 44	## Session Seal — Unified Sensorial Canvas (Phase Epsilon V9): AGI→ASI ref + emenda BoK + Fases 3.1-3.4 (2026-06-17)
> 45	
> 46	`/handson` → conversa estratégica (Model Council; plugin `claude-code-setup`; paper *From AGI to ASI*) → diretiva arquitetural **Unified Core Sensorial Canvas**. Sessão de alta densidade em arco Closed-Loop: fundamentação (AGI→ASI) → auditoria material dos clusters → gate BoK → 4 fases de implementação R3F → verificação ocular E2E. Nada foi codado antes de (a) auditar os clusters e (b) selar a emenda BoK.
> 47	
> 48	**O que foi entregue:**
> 49	1. **Referência AGI→ASI + checklist Via 4:** paper DeepMind (arXiv 2606.12683, Legg/Hutter/Leibo et al.) lido inteiro (57p, extração PyMuPDF) + selado como nó `architecture` **`a576216e`** (edge `INFORMS` → `bok-scribe-seal-openclaw-v1` **`d2827191`**) + checklist de design da **Via 4** (`.claude/context/agi-asi-via4-design-checklist.md`) + plano de trabalho (`.claude/context/unified-core-sensorial-canvas-plan.md`). Tese: o MCORCH é a Via 4 (formação de grupo de agentes) instanciada na camada de aplicação.
> 50	2. **Auditoria de clusters (Lei 1):** Louvain clustering = **REAL/VIVO** (client-side `graphology-communities-louvain@2.0.2` em `useConstellationSigma.ts:227`, 8.5k nós / 8.8k arestas); squad-territory coloring = **MORTO** (`crew_module_ownership` = 0 linhas → fallback sempre cai no Louvain) + heurístico (`inferSquad` keyword-match). **Decisão B = PODAR** (Louvain é o esquema oficial; `OTD-SQUAD-OWNERSHIP-REVIVAL` registra revival por sinal real).
> 51	3. **Emenda BoK (gate Sovereign-eleito sobre override):** `mcorch-constellation` PRD/FRD/SDD estendidos — **PR-025 + FR-043..049 + NFR-023/024 + SDD §9** (reconciliação Sigma→R3F = graphology cérebro / R3F corpo; OTDs SQUAD-OWNERSHIP-REVIVAL/SYNAPSE-EMBEDDING/UCANVAS-PERF).
> 52	4. **Fases 3.1-3.4 (R3F, commits granulares, não-quebrante, 3 páginas legadas preservadas):** scaffold rota `/dashboard/universe` + `useUnifiedCanvasStore` + shell 72/28 · **Code Network** `InstancedMesh` colorido pelas comunidades Louvain reais (plano equatorial) · **Memory Network** GraphRAG como casca cymatics (fibonacci, glow aditivo) · **Black Hole** (`MegaBrainVisualizer`) herdado como backdrop compartilhado (z-0) atrás do Canvas de redes transparente (z-10).
> 53	5. **E2E ocular (à prova de CF):** build → `vite preview` local → sessão do Usuário Zero injetada (`gen-user-session.ts`) → agent-browser nos **3 modos** (Universo/Matrix/Memória). Telemetria real conferida (8.560 nós / 8.816 arestas / ~733 comunidades / 159 pensamentos). A "esfera órfã" foi **desmistificada = spinner de loading** (`Loader2`, `.animate-spin` 1→0 ao carregar), não bug; glow fraco da memória corrigido (blending aditivo).
> 54	
> 55	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (escolheu **emenda BoK** sobre override; autorizou commit direto na `main`) · Owner=Sovereign (3 páginas de produção; legados intactos como backup até paridade — passo 3.9).
> 56	
> 57	| Verificação (material) | Resultado |
> 58	|---|---|
> 59	| Auditoria de clusters | ✅ Louvain VIVO (`useConstellationSigma.ts:227`) · `crew_module_ownership` 0 rows (REST count) |
> 60	| Emenda BoK | ✅ PR-025/FR-043..049/NFR-023-024/SDD §9 nos 3 docs (grep) |
> 61	| Fases 3.1-3.4 | ✅ tsc 0 em cada passo · build chunk `UnifiedCanvasPage-BY8dIJXM.js` 8635B |
> 62	| E2E ocular | ✅ autenticado em `/dashboard/universe` · Black Hole + Code(8.560) + Memory(159) · 3 modos · spinner identificado |
> 63	| Commits (8) | `4f97ebf` AGI ref · `19a7b83` BoK · `210b90d` 3.1 · `d832084` 3.2 · `4940b4d` 3.3 · `38d9760` fix · `769acb1` 3.4 · `08b36eb` readme |
> 64	| Mesh | ✅ AGI ref `a576216e` + handoff `5225ff03` (ambos 768d) |
> 65	
> 66	### Survival Laws Self-audit
> 67	```
> 68	Law 1 (Materiality): ✅ Auditoria provada por REST count (0 rows) + grep de código (:227); E2E ocular real (screenshots, não auto-declarado) — a "esfera órfã" identificada como spinner via `.animate-spin` 1→0, não fabriquei explicação. Fase 5c executada. Embed do handoff via `{node_id}` (record-drift conhecido) → 768d OK.
> 69	Law 2 (Process): ✅ Auditoria material ANTES de codar; emenda BoK (gate) ANTES da Fase 3; plano documentado. Canvas = alteração de UI → gate E2E aplicado.
> 70	Law 3 (Pruning): ✅ Sessão longa empacotada (conversa→ref→audit→gate→4 fases→E2E) sem selar cedo (calibração 1M); Decisão B = poda do squad-coloring morto.
> 71	Law 4 (ORO): ✅ Triplet declarado; gate de governança decidido pelo Sovereign (emenda vs override); commit-na-main autorizado explicitamente.
> ```

## 🤖 Claude *(02:11:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"OK $slug \u2014 BoK complete\" || echo \"INCOMPLETE $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK Gate completeness check per slug"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> OK agentic-workspace — BoK complete
> OK aios-sql-bridge — BoK complete
> OK authenticated-browser-operator — BoK complete
> OK canvas-design — BoK complete
> OK constellation-v2 — BoK complete
> OK conteudo-v2 — BoK complete
> OK e2e-user-zero — BoK complete
> OK gamificacao-nodes — BoK complete
> OK identity-fabric — BoK complete
> OK marketing-hub — BoK complete
> OK mcorch-constellation — BoK complete
> OK mcorch-qa-healing — BoK complete
> OK mercado-livre-api — BoK complete
> OK meta-api — BoK complete
> OK openclaw — BoK complete
> OK post-engine — BoK complete
> INCOMPLETE security — missing: 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> OK viral-autopilot — BoK complete
> OK viral-daily-canvas — BoK complete
> OK viralmind — BoK complete
> OK vision-mcp — BoK complete
> ```

## 🤖 Claude *(02:11:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-42 of 238 total (58634 tokens, cap 25000). Call Read with offset=43 limit=42 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.42.0 — Viral Autopilot BoK 9/9: motor de conteúdo viral autônomo (R1-R4) (2026-06-17)** — `/handson` → diretiva Sovereign de **retomar o objetivo-núcleo de receita** (= o próprio Sprint Goal "distribuição social autônoma operacional"): alimentar redes com conteúdo viral auto-gerado/agendado (tudo de uma vez OU a cada N dias), que a cada ciclo analisa o anterior p/ melhorar os próximos criativos, monetizado c/ afiliado ML. Arco Closed-Loop puro (zero código de produto): **(1) Auditoria material** (workflow 7 agentes, prova path:linha) — R1/R4 parciais vivos, **R2 (recorrência) e R3 (loop auto-melhorável) AUSENTES** (`campaign_metrics` sem writer, `optimization_policy` nunca lida, `self-optimize` sem cron); **(2) 4 decisões soberanas** (AskUserQuestion: suite NOVO · MVP texto+imagem · sinal R3 combo · 3 SKUs); **(3) BoK 9/9** (1889 LOC, FR-VA-001..021, 12 FMEA 4×RPN>100); **(4) Validação Fase 6 em 4 rodadas adversariais** (4 críticos/rodada) + grep determinístico — pegou buraco de segurança real (cron `verify_jwt=false` sem prova service-role in-function) + anti-mint (refund por deduct negativo, que EU introduzi); **(5) seal** (node `b3398294` embedded 768d, DERIVES_FROM marketing-hub). **Prova:** tsc 0 · 3 commits pushed · Phase 5c **SEAL ALLOWED** (10) · mesh **8928** · handoff `496ec17c`. **BoK Gate ABERTO.** Pending: fatia 1 (product-aware + monetize, NÃO depende do cron) + SOP `autopilot-cron-identity.md` (Lei 2/OTD-VA-008) antes da cadência. **Lição:** verificação adversarial multi-rodada foi essencial — cada "fix" meu deixava um resíduo que a rodada seguinte pegava; não auto-declarar GO (Lei 1).
> 8	
> 9	**Sprint v6.41.0 — Unified Sensorial Canvas (Phase Epsilon V9): AGI→ASI ref + emenda BoK + Fases 3.1-3.4 (2026-06-17)** — `/handson` → conversa estratégica (Model Council; plugin `claude-code-setup`; paper *From AGI to ASI* DeepMind) → diretiva arquitetural **Unified Core Sensorial Canvas** (fundir Core-Fable + Matrix + Memória num canvas 3D R3F). Arco Closed-Loop: **(1) Fundamentação** — arXiv 2606.12683 (Legg/Hutter/Leibo) lido inteiro (57p) + selado como nó `architecture` `a576216e` (edge INFORMS→openclaw) + checklist Via 4 (`.claude/context/agi-asi-via4-design-checklist.md`); tese: o MCORCH é a Via 4 (group agent formation) instanciada na app layer. **(2) Auditoria de clusters (Lei 1)** — Louvain = REAL/VIVO (`useConstellationSigma.ts:227`, graphology client-side); squad-coloring = MORTO (`crew_module_ownership` 0 rows → fallback Louvain) + heurístico (`inferSquad`) → **Decisão B = PODAR** (Louvain oficial; OTD-SQUAD-OWNERSHIP-REVIVAL). **(3) Emenda BoK** (gate Sovereign-eleito sobre override) — `mcorch-constellation` +PR-025/FR-043..049/NFR-023-024/SDD §9 (reconciliação Sigma→R3F: graphology cérebro / R3F corpo). **(4) Fases 3.1-3.4** (R3F, commits granulares, 3 páginas legadas preservadas) — scaffold rota `/dashboard/universe`/store/shell 72-28 + Code Network InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop (memória corrigida: glow aditivo). **(5) E2E ocular** (preview local à prova de CF + sessão injetada) nos 3 modos — telemetria real (8.560 nós/8.816 arestas/~733 comun./159 pensamentos); "esfera órfã" desmistificada = **spinner de loading**. **Prova:** tsc 0 em cada fase · 9 commits pushed · Phase 5c **SEAL ALLOWED** (handoff `5225ff03` verificado) · mesh **8926**. **Restam (Pending):** 3.5 Sinapses (arestas REAIS de `mcorch_edges`) · 3.6 fly-to · 3.7 layout/perf (**OTD-UCANVAS-PERF** — query do código ~30s c/ 2 canvases) · 3.8 poda · 3.9 paridade+gate E2E 1920×1080 · 3.10 seal. **Lição:** auditar materialmente ANTES de codar (Louvain vivo vs squad morto) + emenda BoK ANTES da Fase 3 manteve o Closed-Loop; o E2E ocular pegou que a "esfera órfã" era o spinner — não fabriquei explicação (Lei 1).
> 10	
> 11	**Sprint v6.40.0 — Vision MCP Fatia 3 remainder: PAT UI + install Claude Code + Plugin/Registry + caps de custo (2026-06-17)** — `/handson` → Sovereign puxou as 3 frentes do roadmap ("continue"). Closed-Loop: mapeei o contrato BoK vivo (FR-VM-003/011 · DD-VM-003 · OTD-VM-024/025) antes de codar. **Entregue (até o limite NÃO-gated):** **(1) PAT UI (FR-VM-003)** — `useMcpTokens` gera PAT 100% client-side (CSPRNG 32B→SHA-256, só o hash persiste byte-idêntico ao verifier; plaintext uma vez), lista/revoga RLS-own; `McpConnectorsCard` em Settings→Connectors; `.mcp.json` wired (`Bearer ${VISION_MCP_PAT}`); types regen. **Install no Claude Code provado por handshake MCP+PAT REAL pela URL pública** (`initialize`+`tools/list`7+`mesh_search` tenant-scoped); **(2) Plugin Zip + MCP Registry (FR-VM-011)** — `packages/vision-mcp-plugin/`→`public/plugins/…zip` + 3 skills PT-BR; manifesto `server.json` `com.mcorch/vision-mcp` (schema oficial 2025-12-11, remote streamable-http) + runbook (publish **gated** no DNS TXT Sovereign); **(3) OTD-VM-024** — blueprint §8-A sela motor dual (Firecrawl scrape + Gemini grounding run, fundamentado ai.google.dev) → FECHADA; **(4) caps (DD-VM-003/OTD-VM-025)** — `deepsearch.run` cap per-plano 10/25/50 + diário 25/100/500 (BYOK bypassa, fail-open em count error, throw antes do deduct); `validation_failed` ganha field+message (FRD §4.4). Anticorpo Lei 2: SOP `vision-mcp-connector-install.md`. **Prova:** pkg **55/55** · tsc 0 · smoke-vision-cost-caps **3/3 LIVE** zero-cost · origem serve plugin 200 byte-idêntico · `/security-review` independente **SAFE** · container `7710b832` · 8 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8922** · handoff `c21c53db`. **Top Gap restante (tudo gated/Sovereign-side):** OAuth browser-flow (1º tenant externo) · `mistral`/`vision.ocr` (deferidos) · publish no MCP Registry (DNS challenge) · Stripe live · domínio Resend · atribuição compra ML. **Lição:** mapear o contrato BoK vivo antes de codar mostrou que per-plan+daily caps fechavam OTD-VM-025 na mesma sessão; e provar o install pelo handshake REAL da URL pública (não loopback/browser) é o que valida "Claude Code conecta" (Lei 1).
> 12	
> 13	**Sprint v6.39.1 — Vision MCP público: mcp.mcorch.com LIVE pelo Cloudflare (OTD-VM-013 fechada) (2026-06-16)** — ativação do vhost (último item Sovereign-side da Fatia 3). Split: Sovereign cuidou do Cloudflare (A record `mcp`→137.131.243.179 proxy **laranja** + SSL **Full** + **WAF Custom Rule Skip** por host), eu do nginx/origem (vhost `sites-enabled` SSE-tuned + cert **self-signed**, CF Full aceita) + verificação. **`mcp.mcorch.com` LIVE ponta-a-ponta** — Vision MCP saiu do loopback, consumível por hosts MCP externos. **DESCOBERTA crítica (gravada na BoK + memória):** CF laranja **desafia clientes não-browser** por padrão (`cf-mitigated: challenge` "Just a moment") → browser passa o JS mas SDK/curl/Claude-connector NÃO → **WAF skip por host é OBRIGATÓRIA** pra qualquer endpoint MCP/API atrás de CF laranja. Provado material (do datacenter, pelo CF público): `/health` 200, `/mcp` sem token 401, **handshake MCP real+JWT → mesh_search tenant-scoped 200**, sem-token rejeitado. Caveat: self-signed só em Full (não strict). 3 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8921** · handoff `0632e1f8`. **OTD-VM-013 FECHADA.** **Lição:** browser ≠ cliente programático — só declarei LIVE após o handshake MCP+JWT do datacenter (não o `/health` no navegador do Sovereign), que é o que pegou o challenge bloqueando os clientes reais (Lei 1).
> 14	
> 15	**Sprint v6.39.0 — Vision MCP Fatia 3 core: PAT external auth + LGPD erasure + nginx vhost (2026-06-15)** — próximos passos, Sovereign escolheu "Fatia 3 core + vhost config" (de 4 opções). Closed-Loop: mapeei o contrato BoK (data-model §2.1/§2.3 + SDD §5.2/§5.3/§7) antes de codar. **Entregue:** (1) **PAT** (FR-VM-003) — `mcp_access_tokens` (SHA-256 + **allowlist de scopes no DB** + teto 365d + RLS own) + `auth/pat.ts` + **dispatch PAT-vs-JWT** em `verifyBearer` (JWT→ALL_SCOPES; PAT→subset) + **scope-gate por tool** (`requireScope` → 403, default-deny); (2) **erase LGPD** (FR-VM-009) — `vision_artifacts` + `erase_vision_artifacts` (cascade **re-escopo `user_id` por DELETE**, sem primitiva cross-tenant) + retention-sweep diário; (3) **nginx** `mcp.mcorch.com.conf` SSE-tuned + runbook (ativação = DNS Sovereign). **Correção apply-reality OTD-VM-026:** `storage.objects` storage-admin-owned → deleção via Storage API pelo caller (RPC retorna `storage_paths`); bucket privado + RLS bucket-scoped default-deny já isolam. `mistral_api_key`/`vision.ocr` deferidos. 3 migrations aplicadas+registradas (Management API) · `/security-review` independente **SAFE** (0≥8) · smoke **7/7** LIVE (PAT scope-gate/revoke/expiry + erase zero-residue + cross-tenant guard) · pkg **50/50** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8920** · handoff `e0695dad` · 6 commits · container `fda2784f`. OTD-VM-020 marcada **PAT-first IMPLEMENTADA**. **Top Gap novo:** ativação do vhost (DNS Cloudflare — Sovereign) · OTD-VM-024 emenda BoK do engine + per-plan `planned_units` (DD-VM-003) + cap diário per-tenant (OTD-VM-025) · resto Fatia 3 (OAuth 2.1 browser-flow + Plugin Zip + UI de emissão de PAT + `mistral_api_key`/`vision.ocr`). **Lição:** o 42501 do `DELETE storage.objects` (SECURITY DEFINER não-owner) só apareceu no smoke contra o DB servido — testar o artefato servido pegou um defeito de realidade-de-apply do stub SDD (corrigido + OTD-VM-026); o mapeamento do contrato BoK antes de codar evitou improviso (Lei 2).
> 16	
> 17	**Sprint v6.38.0 — Vision MCP `deepsearch.run`/`poll` async (FR-VM-007 · job→poll→partial-refund §4.5) (2026-06-15)** — `/handson` → Sovereign puxou o item #1 do roadmap vision-mcp. Closed-Loop: workflow de **mapeamento (5 readers)** leu contrato selado + schema vivo + wiring ANTES do código — e **pegou que minha premissa contradizia a BoK** (a SDD sela **Firecrawl**, não "google/gemini"). Surfaceei; Sovereign decidiu (custom): *"não pagar Firecrawl agora; usar chaves já disponíveis"* → motor = **Gemini Google-Search grounding** (chave `google` já provisionada; BYOK→plataforma→402), **desvio consciente OTD-VM-024** (débito de emenda BoK); contrato job/refund/state 100% fiel à BoK. **Entregue:** `deepsearch.run` (3 mco, débito-na-entrada→`job_id`→worker in-process→refund parcial §4.5 floor-a-favor-do-tenant) + `deepsearch.poll` (grátis, tenant-bound, **self-heal de órfão**); `vision_jobs` (SELECT-own RLS) + **RPC atômico `finalize_vision_job`** (service-role-only, terminal+refund 1×/job); menores (`infra_health_logs` event/metadata + OTD-VM-023 orphan-sub). **Reviews:** workflow adversarial 5-lentes (2 HIGH: charge-without-value + refund-atomicity → fechados com finalize+reconcile) + **recuperação dos 3 verify mortos por session-limit** dos transcripts (achado novo: sem teto GLOBAL da chave-plataforma → **OTD-VM-025** semáforo; bucket era só per-sub) + allowlist de telemetria (side-channel cross-tenant) + erro de provider opaco + sentinel no `source_allowlist` + URLs http(s) + CHECK `refunded_mco≤charged_mco`. `/security-review` independente **SAFE** (0≥8). pkg **46/46** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8918** · handoff `fc0b5efc` · 6 commits · container `b24360c8` smoke **10/10** LIVE. **Top Gap novo:** Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 (root Sovereign) · cap diário per-tenant + rate-limiter compartilhado (OTD-VM-014/025) · emenda BoK do engine (OTD-VM-024) · per-plan `planned_units` (DD-VM-003). **Lição:** o workflow de mapeamento pré-código pegou a contradição Firecrawl-vs-Gemini ANTES de eu codar a coisa errada (Lei 2); e recuperar findings órfãos de transcript (em vez de re-rodar) achou 1 HIGH novo de custo que o /security-review (classe DoS excluída) não pegaria.
> 18	
> 19	**Sprint v6.37.0 — Vision MCP Fatia 2: 4 Billable Tools + BYOK Foundation (+ Fatia 1 handshake/interop close) (2026-06-15)** — diretiva começou em "fechar a última ponta não-provada da Fatia 1 (mesh.search E2E com JWT)" e o Sovereign mandou seguir até a Fatia 2 inteira ("algo completo", "você escolhe a ordem"). **(1) mesh.search E2E fechado + bug crítico de Fatia 1:** o E2E com cliente MCP real pegou que o servidor reusava **um** `StreamableHTTPServerTransport` stateless (SDK proíbe reuso → `notifications/initialized` **500**, nenhum cliente completava handshake) → fix fresh-per-request; provado **7/7** + adversarial **6/6** (forja ES256 ×3 + injeção PostgREST ×7). **(2) Interop de protocolo** (achado pelo `/security-review` independente): gate aceitava só `2025-11-25`, 400-ando clientes 3rd-party → ampliado p/ `SUPPORTED_PROTOCOL_VERSIONS`; cliente cru heterogêneo **8/8** (`2025-03-26`/`2025-06-18`). **(3) Fatia 2 — fundação** (SOP Lei 2 + `infra/billing.ts` + `auth/credentials.ts` + `safety/duty-of-care.ts`: BYOK→plataforma→402 · deduct-on-entry+refund-on-failure · sentinel · duty-of-care) + **4 tools billable provados:** `vision.describe_image` (FR-VM-018, 7/7), `vision.analyze_video` (FR-VM-024 Gemini — **não Higgsfield** — cobrança/min, 7/7), `deepsearch.scrape` (FR-VM-007 Firecrawl BYOK-only, 4/4), `mesh.consolidate_reference` (FR-VM-021 escrita tenant-escopada, 5/5). **(4)** migration `firecrawl_api_key` Vault (`/security-review` limpo · aplicada+registrada) + UI Settings **deployada** + SSRF redirect-fix (achado do review). pkg **34/34** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8917** · handoff `7a45d8ef` · 7 commits. **Top Gap novo:** `deepsearch.run` async (a metade "google/gemini" — FR-VM-007 job/poll) · Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 · OTD orphan-sub. **Lição:** o `/security-review` independente pagou de novo (achou o SSRF por redirect + o defeito de interop de protocolo que o cliente do mesmo-SDK mascarava); testar contra o ARTEFATO SERVIDO pegou o bug de handshake.
> 20	
> 21	**Sprint v6.36.2 — Vision MCP: OTD Gates Closed + Fatia 1 Built & Deployed ON (2026-06-15)** — diretiva Sovereign "ambos em sequência" (gates por pesquisa → código). **(1) Gates OTD pré-GA** (workflow `wf_0040a939-232`, 3 lentes verify adversarial): **OTD-VM-004 CLOSEABLE** (grade mcoCoins 4×-floor sobrevive — custo fonteado por provider, nenhuma sub-margem; `segment` cost-aware obrigatório; SOP `vision-mcp-cost-calibration.md`); **OTD-VM-001 CLOSEABLE** (corrigiu 2 erros factuais do blueprint — UEyes/Imp1k EXISTEM, SOTA=**SUM**/MIT self-hostável não DeepGaze; recall≥0.95 fundamentado); **OTD-VM-006 CLOSEABLE** (14 licenças verdes LICENSE-fetched + 3 minas banidas; SpikingJelly não-MIT); **OTD-VM-005 PARTIAL** (SCCs-ANPD inviável; Res. 32/2026 UE adequada; Mistral=default candidato). **(2) Fatia 1 construída + DEPLOYADA ON** (`packages/vision-mcp-core/` → container `mcorch_vision_mcp` Sovereign Mesh, restart=unless-stopped, UID1001, read-only, `127.0.0.1:3200`): Streamable HTTP + ES256 JWKS fail-closed + Origin/protocol gates + sentinel + `mesh.search` tenant-safe. Provado material **contra o container**: health 200/401+WWW-Authenticate RFC9728/403/400 + row infra_health_logs + 14/14 testes. **2 bugs que só o deploy pegou:** bind `0.0.0.0` (port-map do bridge) + schema real de `infra_health_logs` (sem `metadata` — o padrão do sentinel edge falha silencioso). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8916** · handoff `98fa83d7` · 4 commits. **Top Gap novo:** mesh.search E2E com JWT (handshake MCP) · vhost nginx `mcp.mcorch.com` (OTD-VM-013, root Sovereign) · Fatia 2 (foveal billable + per-user creds) · migration `infra_health_logs ADD metadata jsonb` (telemetria rica). **Lição:** testar o ARTEFATO SERVIDO (container), não o node local — Lei 1 pegou 2 bugs + 1 schema drift que unit/local não veriam.
> 22	
> 23	**Sprint v6.36.1 — Vision MCP: BoK 9/9 + 8-Agent System + Adversarial Validation (2026-06-15)** — diretiva Sovereign (ref. sandcastles.ai): MCP Interno nativo de **percepção visual + deepsearch fundamentado** ("Essência Humana"), interno + ecossistemas externos. Closed-Loop BoK-first em 3 atos: **(1) Blueprint-semente v0.2.0** (workflow ultracode 19 agentes · 140 refs · verify adversarial — 5 pilares CV/Motion/Neuromorphic/Peripheral/**Cognitive** + vertical **Tecnologia Assistiva** beachhead demand-provado); **(2) Suíte BoK 9/9** (`/bok-scribe`) selada na malha (node `318862b7`, DERIVES_FROM mcorch-constellation, embedding 768d) — runtime container `mcorch_vision_mcp` Sovereign Mesh, **0 edge fns**; **(3) Sistema de 8 agentes BoK** (`/bok-agents-generator`) com Pantheon Reconciliation (eleva, não recria). **Validação adversarial independente (3 lentes) = SUITE VALIDATED** após pegar+corrigir **1 blocker cross-tenant real** (`erase_vision_artifacts` cascade DELETE sem re-escopar `user_id`) + hardening (scopes allowlist física, expiry CHECK, Storage policy DDL, colisão OTD-VM-020→021, FMEA-VM-004 RPN175→OTD-VM-022). Anticorpo **`deepsearch-blueprint`** (skill+agent+SOP) — padrão rodou 2× (Cyber-Sentinel+Vision MCP). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8915** · handoff `b73d141d` · README badge `6.36.0-vision-mcp`. 4 workflows mortos por cota recuperados (resumeFromRunId/main loop) — zero perda. **Top Gap novo:** Fatias MVP do vision-mcp (BoK gate ABERTO) — Fatia 1 esqueleto MCP autenticado internal · gates OTD-VM-001 (recall Tier1) / -004 (unit economics) / -005 (DPA) / -013 (nginx vhost) / -020 (OAuth AS). **Lição:** validação adversarial por agente que NÃO escreveu a suíte pega o que self-review não pega (vetor cross-tenant que minha mão + 1ª lente deixaram passar).
> 24	
> 25	**Sprint v6.36.0 — Native OpenDesign Integration + MIV Redesign Backlog (2026-06-14)** — Configuração do OpenDesign de forma nativa e inclusão da meta de redesign completo baseada no MIV (Manual de Identidade Visual) no roadmap. **(1) Nativização do OpenDesign** (`CanvasDesignPage.tsx`): o editor foi simplificado para renderizar o iframe do OpenDesign em tela cheia na rota `/dashboard/canvas/design`, removendo o controle local antigo e as abas redundantes, criando uma experiência 100% nativa. **(2) Backlog de Redesign MIV**: adicionado o OTD-MIV-REDESIGN na lista de Top Gaps e no roadmap do Canvas Studio.
> 26	
> 27	**Sprint v6.35.0 — Core-Fable: Fable 5 Flagship + Metering + Mega Brain Interstellar (2026-06-10)** — Diretiva Sovereign "Refatore todo o nosso Core-v2 para Core-Fable" em 3 arcos: **(1) Rebrand** (`914f8dd`): rota `/dashboard/core-fable` (+redirects compat), `CoreFablePage`/`components/core-fable/`, Claude Fable 5 (`anthropic/claude-fable-5` via OpenRouter, verificado live no catálogo) como default do Core; seletor de chat **desacoplado** do `pref_ai_model` (localStorage) — 1 clique não re-modela o flywheel pago. **(2) Review adversarial pré-deploy confirmou 4 P1 econômicos** (`997b307`): aios-chat OpenRouter nascia SEM metering (billing bypass na chave-plataforma) → `_shared/agent-metering.ts` compartilhado fiado nos 2 paths; `agent_pricing` sem rows novas → under-billing 133-167× via fallback flash → migration `20260610010000` seeda fable-5 1000/5000 + sonnet-4.6 300/1500 + dropa id morto; `/security-review` SAFE. Provado live: probe `{"output":"Claude"}` + ledger correto + `calc_agent_cost_mcoin`=120. **(3) Mega Brain Interstellar** (`3b15e41`→`47f9316`): loop iterativo de 8 screenshots dirigido por referência visual do Sovereign — câmera quase equatorial + 210 steps adaptativos = arco lensado contínuo sobre a sombra; **raios capturados = preto** (matou anel de névoa + bola branca do glow artificial — críticos precisam ~310 steps/órbita); disco blackbody edge-on, reação por energia (surge/spin/shimmer). tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8865** · handoff `4728b8aa`. **Top Gap novo:** OTD-FABLE-MARGIN (margem 2.0 do calc < 4×-floor p/ chat premium) · fallback `pricing_not_found` silencioso (fail-caro + telemetria). **Lição:** o screenshot-loop com sessão real no preview local (sem tocar o dist servido) pegou 2 bugs visuais que tsc/testes jamais veriam (GLSL só falha em runtime); e o review adversarial pagou de novo — 4 P1 econômicos numa feature "só de rename".
> 28	
> 29	**Sprint v6.34.0 — Cyber-Sentinel: Security BoK 4/4 + Prompt Gate Live + Infra Hardening (2026-06-10)** — diretiva CISO executada em 2 fases na mesma sessão. **(1) BoK de segurança 4/4** (`docs/bok/security/`, schema CISO 01-brd/02-srs/03-sdd/04-fmea — 12 BR-SEC + Risk Ledger · 15 FR-SEC + matriz RLS canônica + `SET LOCAL` · SDD lefthook/Arcjet/sentinel/Dockerfile UID1001/compose cap_drop integrais · FMEA 12 modos RPN AIOS). **(2) Aplicação no ecossistema vivo** (`6f2f75a`): **Sentinel LIVE** em `orchestrate-content` (prod **v52**) — `_shared/sentinel.ts` barra injeção/bypass/ANSI **depois da identidade, antes do `deduct_mco_coins`**; provado em prod com JWT real (`HTTP 403 layer=sentinel` score=3, **zero mcoCoins**). Infra recriada e endurecida: `claude_mem` uid1001+read_only+8caps (healthy), `chroma` caps conservadoras+no-new-privileges (heartbeat vivo), `gitnexus` imagem não-root buildada; env `SUPABASE_SERVICE_ROLE_KEY` revogada removida do compose (FM-04). Gate git **dual-engine** lefthook+gitleaks (pre-commit/pre-push, degrada sem gitleaks — OTD-SEC-003). **Review adversarial pegou 4 bugs reais ANTES de qualquer deploy quente**: rate-limiter falsava o fan-out paralelo de `campaign-run`; `cap_drop SETUID/SETGID` quebraria o `chroma` de terceiros; regex de 1 qualificador; guard `&&||` do gitleaks engolia a detecção. tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8862** · handoff `0a9865a9` + BoK seal `424f0fe4`. **Próximos:** FM-10 gitnexus (imagem pronta, roda stdio) · OTD-SEC-006/007 (fiar sentinel + migration `security_events`/quarentena <50ms nas demais fns pagas) · Arcjet aguarda superfície Next/BFF. **Lição:** verificar **materialmente** (dry-run dos containers, exploit real em prod) antes de declarar — pegou o `name:` que orfanaria os containers e os 4 bugs do review.
> 30	
> 31	**Sprint v6.33.1 — Hotfix Kanban ScrollArea + E2E à Prova de Cloudflare (2026-06-09)** — bug report do Sovereign no `/dashboard/kanban`: `ReferenceError: ScrollArea is not defined` ao criar coluna. **Causa:** `KanbanPage.tsx` usava `<ScrollArea>` (área scrollável de tarefas) sem importar — só quebrava *depois* da 1ª coluna (empty-state não exercita o componente). **Fix de 1 linha** (`e55ce70`): import `@/components/ui/scroll-area`; deploy material (chunk novo `KanbanPage-CW7WBYjZ.js` ≠ o do stack trace, import scroll-area + env baked); **confirmado em prod pelo print do Sovereign**. **E2E completo** via preview local do `dist` + sessão injetada (CF Turnstile barra agent-browser do datacenter até no `login.mcorch.com`): CRUD + drag-drop bidirecional **provado pelo DB** (3× PATCH 200 + SELECT, não pelo DOM). Helper `gen-user-session.ts` (`761ea6f`) p/ E2E logado à prova de CF. **Incidente de concorrência** (Sovereign mexendo em prod junto) resolvido sem perda de dado — board/coluna intactos, a "divergência" da 1ª rodada era o Sovereign movendo o mesmo card. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8860** · handoff `fd20b125`. **Lição:** E2E mutável vai em board descartável, nunca no dado real do Sovereign; DB-prod é compartilhado. **Diretiva CISO de hardening DEFERIDA** (blueprint `6b1571a` commitado; 4 artefatos BoK de segurança p/ sessão dedicada).
> 32	
> 33	**Sprint v6.33.0 — ML Attribution Fix + Browser Operator BoK (2026-06-08)** — o teste **real** do Sovereign no branded link expôs o flywheel emitindo link **MORTO**. **(1) Fix do auto-monetize** (`34d7ef0`): `_shared/affiliate.ts` `buildMlProductUrl` montava o formato BARE `mercadolivre.com.br/MLB-<id>` (404) com 2/3 ids stale → agora resolve `vm_affiliate_products.product_url` real (fonte única Apify), fail-open `/p/`; **reconcilia "ML não conta clique"** (era 404, não falha do matt_word — o painel ML já contara matt_word em produto VÁLIDO em 2026-06-04); provado E2E `7993c6a4` 302 → `/p/MLB27834876`; deploy `orchestrate-step` 122.8kB. **(2) BoK 9/9 do Operador de Browser Autenticado** (`/bok-scribe`, `24ba435`): suíte 756 LOC MR→SDD+STRIDE+FMEA; **gate pagou** — o link oficial é per-user → nova `user_affiliate_links` (não a `vm_affiliate_products.affiliate_template_url` COMPARTILHADA, que vazaria entre tenants — OTD-ABO-003); runtime residencial cravado (datacenter **403** reprovado em produto real `/p/`, bare e `/afiliados/hub`); mesh seal `31323fe3` + DERIVES_FROM edge `9ea18d26` → mercado-livre-api. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8852** · handoff `630509e2`. **Top Gap:** **BUILD do Operador** (gate ABERTO; runtime residencial = Sovereign roda `agent-browser` logado no ML) · domínio Resend · conversão ML real. **Lição:** o teste por **mão do Sovereign** (clicks 0→4) achou o link morto que meu curl-403 do datacenter mascarava; o BoK-first pegou o vazamento cross-tenant **antes** do código.
> 34	
> 35	**Sprint — Stored-XSS Hardening + Antibody (2026-06-08)** — `/security-review` (v6.28.0) havia flagado stored-XSS em `DashboardHome` (`content_library.body` cru via `dangerouslySetInnerHTML`); fechado **ponta-a-ponta** nesta sessão. Sanitização `DOMPurify.sanitize` (já shipada via Antigravity em `da9da4c`/`e5a661a`) + guarda de regressão **6 testes** (`dashboard-html-sanitize.test.ts`: preserva `<a href>` de afiliado + tags de artigo, remove `<script>`/`onerror`/`javascript:`) + **antibody ESLint `no-restricted-syntax`** (`2522e71`, sem dep nova — `eslint-plugin-react` ausente) que faz todo `dangerouslySetInnerHTML` futuro acusar no lint até ser sanitizado+justificado (sink cru plantado → **pego** material; 2 sinks legítimos justificados: DashboardHome DOMPurify · chart.tsx CSS shadcn) + limpeza dos **7 `no-explicit-any`** do data-layer de DashboardHome (`3129369`). Handoff node `e12ed58e` + obs antibody `505fb670` (embedded 768d). tsc 0 · suíte verde · mesh **8849**. **Anticorpo Permanente cumprido** — reincidência do sink barrada no lint. **Top gaps restantes (herdados de v6.28.0, gated no Sovereign):** domínio `RESEND_FROM` (entrega Resend real) · branded redirect `login.mcorch.com/go` · 2 rascunhos WP de teste · atribuição de compra ML.
> 36	
> 37	**Sprint v6.32.x — arco Core-v2 Black Hole (2026-06-07, via Antigravity)** — sessões conduzidas no Antigravity, seladas e versionadas no git, registradas aqui retroativamente a partir dos records do HANDOFF.md (não reauditadas em detalhe — Lei 1): **v6.32.6** Unified Relativistic Black Hole & Cymatics (fusão dos visualizadores num único shader WebGL Schwarzschild — raymarching + disco de acreção + Doppler beaming + ondas de cymatics; layout 30/70; `CymaticsLayer` removido; 284 testes; handoff `ec6204a4`; mesh 8847); **v6.32.5** Model Selector Fix & Reacting Black Hole (fix case-collision dos hooks `useAiosTerminalChat`/`useAiosWorkspaceChat`; persistência do modelo selecionado em `user_api_keys`; redesign MegaBrainVisualizer + CymaticsLayer; 260 testes; handoff `8627661a`; mesh 8839); **v6.32.2** Gemini 3.1 Live Mode (Live API → Gemini 3.1 Flash Live audio-only + Gemini Docs MCP + API Skills; handoff `5acba7aa`; mesh 8818). Os seals intermediários (v6.29–v6.32.4) existem em HANDOFF.md/README mas não foram back-filled aqui.
> 38	
> 39	**Sprint v6.28.0 selado em 2026-06-04** — **Quatro next-steps fechados numa sessão (probe-first)**. Diretiva Sovereign "ataque os 4 pontos numa sessão só, não pare até terminar; o ponto 4 do link não funcionou a contabilidade de clicks" (+ screenshot ML com 1 clique). Cada gap verificado **no código** antes de tocar. **(1) OTD-INTENT-DISPATCH-REFUND FECHADA:** `orchestrate-content` estorna os 10 em falha pós-débito (`!runId` ou erro do kick `async_orchestrate_step`) + marca run `error` — estende o contrato refund da v6.27.2 ao núcleo do flywheel. **(2) nurture-dispatch entrega Resend real (FR-MH-008):** resolve `resend_api_key` per-user (BYOK) + `leads.contact` → POST Resend quando email+chave+endereço; senão `gated`; send `failed` estorna. Live a inbox real ainda gated em `RESEND_FROM` (domínio Sovereign). **(3) Click ledger in-system (OTD-ML-CLICKS):** links publicados passam pelo redirect `process-affiliate-link` GET, que registra o clique atômico (RPC `record_affiliate_click` service-role-only, atribuído ao dono) + 302 pro ML; `link-forge` emite o redirect; **ROIWidget já soma `affiliate_links.clicks`** → "Cliques Totais" reflete cliques reais antes de compra; migration 120000 + fix 130000 (`content_id` UUID). **(4) 1º dispatch pago E2E agentic:** intent→policy→execute→orchestrate-content WP **draft**, run `43048d8e` **done**, **delta 10 exato** (valida ponto 1 em prod), HITL gate provado, blast-radius wordpress-only. **Prova:** `/security-review` independente **SAFE** · drift audit **exit 0** · smoke-affiliate-click **10/10** + smoke-nurture **10/10** · suíte **269** · tsc 0 · deploys 107.9/83.72/87.96kB · Phase 5c **SEAL ALLOWED** (7 verified) · Mesh **8783**. 6 commits. **Novo Top Gap:** entrega Resend a inbox real (domínio `RESEND_FROM` — Sovereign) · branded redirect domain (`login.mcorch.com/go` proxy nginx — link limpo+rastreado) · 2 rascunhos WP de teste a limpar · atribuição de compra ML (aguardando conversão). **Lição:** probe-first economizou retrabalho (ROIWidget já somava clicks → zero UI nova; `resend_api_key` já existia → só o canal) e pegou o bug 22P02 do RPC (content_id UUID) no smoke antes de declarar — corrigi via migration na mesma sessão (regra hotfix→migration). **Follow-up (mesma sessão, "continue com os próximos"):** click ledger estendido ao caminho **interativo** de monetização — POST `process-affiliate-link` retorna redirect rastreável `?link_id` (migration `20260604140000` + RPC `record_affiliate_click_by_link`). O smoke estendido (G8) expôs um insert de `affiliate_links` quebrado há tempo (`campaign_id` UUID vs slug `"ai_orchestration"` → 22P02 silencioso, nenhuma linha de afiliado nunca persistida) + o `/security-review` independente pegou um **open-redirect** no branch novo (302 pro `short_url` tenant-writável) — ambos corrigidos (gate de domínio ML + UUID-só); smoke **9/9** (G9 prova o open-redirect bloqueado), commit `b2c39f6`. **Follow-up 2 ("faça todos os 3"):** (A) **auto-monetização** no `orchestrate-step` — o artigo gerado embute o redirect rastreável `?link_id` per-owner (`_shared/affiliate.ts`), o flywheel monetiza+rastreia automático; provado E2E pago run `cee55b11` (Roborock → link rastreável no `content_mesh_asset`). (B) **matt_tool** per-user (coluna `affiliate_config` + threading GET/POST/orchestrate + UI `AffiliatesPage`; caveat honesto: efeito na atribuição ML não-verificável, mas aditivo). (C) **campaign-run assíncrono** p/ >8 passos (`EdgeRuntime.waitUntil`, batches; pequenas seguem síncronas). `/security-review` independente **SAFE** (flagou XSS **pré-existente** `DashboardHome:677` dangerouslySetInnerHTML → tarefa spawned). Smokes click **G1-G9+G1b** · campaign **A-H** · e2e auto-monetize ✅ · tsc 0 · drift exit 0. 4 commits (`9bb5bba`/`bb999c1`/`7cbd036`/`b468c98`).
> 40	
> 41	**Sprint v6.27.2 selado em 2026-06-04** — **Refund-on-failure: charge-without-value fechado (OTD-AEO-REFUND)**. Diretiva Sovereign "continue com os próximos passos". Probe-first material elegeu o item de **menor blast radius e maior valor seguro** dos 3 next-steps (refund protege saldo do usuário, zero ação outward); os outros 2 dependem do Sovereign (nurturing externo precisa de domínio Resend verificado — **zero refs RESEND no código**; 1º pago E2E precisa de GO econômico). **OTD-AEO-REFUND FECHADA:** `aeo-audit` debitava 5 mco na entrada e, se o persist falhasse, devolvia 500 **sem estornar** (charge-without-value, verificado no código). Helper compartilhado **`refundMco`** (`_shared/billing.ts` → `add_mco_coins`, service-role-only, simétrico a deduct, guarda `p_amount>0`, nunca lança); `aeo-audit` (5) e `lead-score` (1) rastreiam `charged` e estornam em qualquer falha pós-cobrança (persist-fail + catch). **Prova:** smoke `smoke-aeo-refund.ts` **6/6 LIVE** (deduct 5→15 / add 5→20 restaurado · guarda nega -10 · net-zero) + unit `_shared/billing.test.ts` **4/4** + regressão [[aeo-audit|aeo-audit]] intacta. **Honestidade Lei 1:** persist-fail não é forçável por input → fiação coberta por unit+code, não por falha forçada (declarado). Contrato refund-on-failure no billing SSOT (`mcoin-cost-calibration.md`). Deploys 86.69/85.62kB · tsc 0 · suíte **269** (265→269) · Phase 5c **SEAL ALLOWED** (8 verified) · Mesh **8774** (1 órfão `aeo:` podado). 3 commits. **Novo Top Gap:** entrega externa de nurturing (bloqueada por domínio Resend — Sovereign) · 1º pago E2E (GO econômico) · **OTD-INTENT-DISPATCH-REFUND** = aplicar `refundMco` ao gap pós-débito do `orchestrate-content` (flywheel, sessão dedicada). **Lição:** probe-first descartou 2 dos 3 next-steps (dependência externa) e leu o código pra confirmar que o gap de refund era REAL (linha 56 débito → 118 persist-fail sem refund) antes de construir — não assumi o bug, verifiquei.
> 42	
> ```

## 🤖 Claude *(02:12:00)*


## 🤖 Claude *(02:12:00)*

TypeScript clean, containers healthy. Now reading the HANDOFF tail (suffix sections: GraphRAG state, infra, pending actions) and checking scratch.

## 🤖 Claude *(02:12:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"---GRAPHRAG-GREP---\"; grep -n \"GraphRAG State\\|Knowledge Mesh\\|totalNodes\\|Pending Actions\\|## Infrastructure\" HANDOFF.md | tail -20",
  "description": "Inspect scratch files and locate suffix sections in HANDOFF"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 17 20:29 ..
> ---GRAPHRAG-GREP---
> 6183:### Pending Actions (atualizado)
> 6240:| `supabase/functions/trigger-ingest/index.ts` criado | ✅ Retorna totalNodes · totalEdges · nullEmbeds · embeddedPct · lastIngest |
> 6284:     → retorna { totalNodes, totalEdges, nullEmbeds, embeddedPct, lastIngest }
> 6341:# ── Re-ingesta do AST no Knowledge Mesh ──────────────────────────────
> 6388:Knowledge Mesh, eliminando dezenas de queries exploratórias por sessão; GitHub MCP
> 6501:| Knowledge Mesh — backfill 3 sessões | ✅ 3 nós `handoff` inseridos + embedded 768d para sessões de 2026-05-02 |
> 6703:| `src/hooks/useKnowledgeMesh.ts` — multi-bucket | ✅ Reescrito: 6 priority buckets + bucket recente + semantic search via `search-constellation` + `meshStats` (totalNodes/totalEdges/dominantTypes) + `contextString` com header `[MESH_STATE]` |
> 6713:| `scripts/seed-aios-milestone.ts` | ✅ Insere milestone node no Knowledge Mesh |
> 6716:| `.claude/commands/handoff.md` | ✅ Protocolo v2: 7 fases — security audit, README live badge sync, Knowledge Mesh milestone, push + relatório pt-BR |
> 6723:| `7161efa` | feat(shakehands): handoff v2 — 7-phase protocol com security audit, README sync e Knowledge Mesh milestone |
> 6726:| `08e34bf` | docs(readme): v5.0.0-zeta — Infra Healing + AIOS Consciousness v2 + Knowledge Mesh 2065 |
> 7233:| `src/pages/MemoryPage.tsx` criado | ✅ Full-screen d3-force Knowledge Mesh — rota `/dashboard/constellation/memory` |
> 7430:## Delta v2 Knowledge Mesh Sync Record (2026-04-26)
> 7447:| `55c4fdb` | feat(gitnexus): Delta v2 Knowledge Mesh Sync — 493 nós AST + 344 edges em Supabase |
> 7488:totalNodes:    3100  |  totalEdges:  2900
> 7674:## Pending Actions (Commercial Launch)
> 7728:- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7787:## Infrastructure
> 7834:## GraphRAG State
> 7843:- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> ```

## 🤖 Claude *(02:12:23)*


## 🤖 Claude *(02:12:46)*

Tudo coletado. Worktree limpo, tsc zero, containers saudáveis, scratch limpo. Segue o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Viral Autopilot BoK 9/9 (selada 2026-06-17 · v6.42.0)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
**Fase selada:** Viral Autopilot — BoK 9/9 do motor de conteúdo viral autônomo monetizado por afiliado ML (R1-R4). Arco Closed-Loop puro, **zero código de produto** (BoK-only). O BoK Gate está **ABERTO**.
```
a8f14a3 — chore(sprint): registra v6.42.0 — Viral Autopilot BoK 9/9
0613899 — docs(handoff): seal Viral Autopilot BoK 9/9
2c56211 — docs(readme): v6.42.0 — Viral Autopilot BoK 9/9
8da7a58 — docs(bok): sela viral-autopilot (R1-R4)
```
Sincronizado com `origin/main` (0 commits atrás).

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ · `scratch/` limpo ✅

🏗️ **INFRA**
```
mcorch_chroma:      Up 4 days (healthy) — Chroma API v2: OK (heartbeat vivo)
mcorch_claude_mem:  Up 4 days (healthy)
mcorch_vision_mcp:  Up 2 days (healthy)
mega-brain-daemon:  Up 4 days (healthy) · webhook (healthy) · dashboard up
```

🧠 **KNOWLEDGE MESH**
~8.928 nós (fonte: seal v6.42.0). Último handoff node `496ec17c`. Seal da BoK: `documentation_suite` **`b3398294`** (embedded 768d) · DERIVES_FROM → marketing-hub `d5163fed`.

🔧 **TYPESCRIPT**
Zero erros ✅

📚 **BoK SUITES**
**Sealed (9/9):** 20 suítes completas — incl. `viral-autopilot` (recém-selada, 1889 LOC), `vision-mcp`, `marketing-hub`, `mcorch-constellation`, `constellation-v2`, etc.
**Incomplete:** `security` — mas é **falso positivo**: usa o schema CISO (`01-brd`/`02-srs`/`03-sdd`/`04-fmea`), não o schema padrão de 9 docs. Cyber-Sentinel foi selada em v6.34.0. ✅ Não é bloqueador.
**Sem GATE alert** — a sessão atual ainda não tocou módulo; e o módulo da vez (`viral-autopilot`) já tem BoK selada.

📌 **SPRINT**
**Goal:** Distribuição social autônoma operacional — pipeline publica automaticamente, analisa desempenho a cada ciclo e melhora os criativos, monetizado com afiliado ML. (O Viral Autopilot é exatamente este objetivo-núcleo de receita.)
**Top gap:** Fatia 1 do Viral Autopilot — gerador *product-aware* + monetização (não depende do cron).

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **Fatia 1 — Viral Autopilot (product-aware + monetize):** primeiro corte de código sobre a BoK aberta. Endereça os buracos R1/R4 que a auditoria pegou (monetização só no artigo via 3 SKUs hardcoded por regex; `affiliate_url` da UI dropado). **Não depende do cron** → menor blast radius para arrancar.
2. **SOP `docs/processes/autopilot-cron-identity.md`** (Lei 2 / OTD-VA-008) — gate obrigatório **antes** da fatia de cadência (R2/recorrência). O design já está cravado: cron prova service-role *in-function* (`Bearer SB_SECRET_KEY`) ANTES de confiar no header `x-autopilot-user-id` (a validação adversarial pegou aqui um buraco de segurança real que drenaria saldo de vítima).
3. **Unified Sensorial Canvas (Epsilon V9) — Fases 3.5-3.10** (sprint anterior, ainda aberto): sinapses reais de `mcorch_edges` · fly-to · layout/perf (**OTD-UCANVAS-PERF**: query do código ~30s com 2 canvases) · poda dos legados · paridade + gate E2E 1920×1080 · seal.

⚠️ **ALERTAS**
Nenhum alerta ✅ — tsc limpo, containers saudáveis, worktree limpo, scratch limpo, em dia com origin.

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

Recomendação: o caminho de maior valor e menor risco é a **Fatia 1 do Viral Autopilot** (passo 1) — ataca diretamente o Sprint Goal de receita, opera sobre BoK já selada e não toca a cadência/cron (que exige o SOP da Lei 2 primeiro). Quer que eu arranque por ela, ou prefere fechar as fases pendentes do Unified Sensorial Canvas antes?

## 👤 User *(02:13:33)*

<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

## 👤 User *(02:13:33)*

<command-name>/goal</command-name>
            <command-message>goal</command-message>
            <command-args></command-args>

## 👤 User *(02:13:48)*

então ok vamos aos próximos passos

## 🤖 Claude *(02:14:22)*


## 🤖 Claude *(02:14:25)*

O Sovereign autorizou seguir. Próximo passo recomendado: **Fatia 1 do Viral Autopilot** (gerador *product-aware* + monetização cross-surface, sem depender do cron). O BoK Gate está aberto (suíte 9/9 selada), então posso codar — mas a Lei 2 e o Closed-Loop exigem que eu mapeie o **contrato exato do BoK** + o **estado material do código** antes de escrever uma linha.

Vou rodar um workflow de **mapeamento** (readers paralelos sobre a BoK + o código vivo) para cravar o escopo da Fatia 1 com precisão.

## 🤖 Claude *(02:14:26)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Viral Autopilot \u2014 Fatia 1",
  "summary": "Implementar a primeira fatia do motor de conte\u00fado viral: gerador product-aware + monetiza\u00e7\u00e3o cross-surface (sem cron)"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Viral Autopilot — Fatia 1". Continue your current work.'}]
> ```

## 🤖 Claude *(02:14:29)*


## 🤖 Claude *(02:15:21)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'viral-autopilot-fatia1-map',\n  description: 'Map the viral-autopilot BoK contract for Fatia 1 + the live code state to scope the first slice precisely',\n  phases: [\n    { title: 'Map BoK', detail: 'parallel readers over the 9 BoK docs to extract the Fatia 1 contract' },\n    { title: 'Map Code', detail: 'parallel readers over the live generation + monetization pipeline' },\n    { title: 'Synthesize', detail: 'one agent fuses BoK contract + code state into a precise Fatia 1 scope + plan' },\n  ],\n}\n\nconst BOK = 'docs/bok/viral-autopilot'\n\nconst BOK_FINDINGS = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    summary: { type: 'string', description: 'one-paragraph summary of what this doc says about Fatia 1 (product-aware generation + cross-surface monetization, NO cron)' },\n    relevant_ids: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        properties: {\n          id: { type: 'string', description: 'e.g. FR-VA-003, PR-VA-007, DD-VA-002, OTD-VA-008' },\n          title: { type: 'string' },\n          requirement: { type: 'string', description: 'verbatim-ish requirement text, what MUST be built' },\n          belongs_to_fatia1: { type: 'boolean', description: 'true if this is product-aware generation OR cross-surface monetization and does NOT need the cron/cadence' },\n          surface: { type: 'string', description: 'which surface/layer: generator | monetization | data-model | rpc | ui | other' },\n        },\n        required: ['id', 'title', 'requirement', 'belongs_to_fatia1', 'surface'],\n      },\n    },\n    data_model: { type: 'array', items: { type: 'string' }, description: 'tables/columns/RPCs Fatia 1 reads or writes (creative_metrics, optimization_policy, affiliate_config, vm_affiliate_products, begin/finalize RPCs, FK composta) with notes on scope' },\n    seed_skus: { type: 'array', items: { type: 'string' }, description: 'the 3 seed SKUs the BoK fixed, if mentioned here' },\n    constraints: { type: 'array', items: { type: 'string' }, description: 'security/tenancy/anti-mint/FMEA constraints Fatia 1 must honor (e.g. per-user affiliate, fail-closed, no negative deduct)' },\n    open_questions: { type: 'array', items: { type: 'string' }, description: 'ambiguities that would force a return to bok-scribe or a Sovereign decision' },\n  },\n  required: ['summary', 'relevant_ids', 'data_model', 'seed_skus', 'constraints', 'open_questions'],\n}\n\nconst CODE_FINDINGS = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    summary: { type: 'string', description: 'what this slice of code does today re: generation + monetization' },\n    locations: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        properties: {\n          path: { type: 'string' },\n          lines: { type: 'string', description: 'line range, e.g. 120-145' },\n          what: { type: 'string', description: 'what happens here \u2014 be specific (e.g. \"3 SKUs hardcoded via regex\", \"affiliate_url dropped\", \"per-user affiliate_config lookup\")' },\n        },\n        required: ['path', 'lines', 'what'],\n      },\n    },\n    reuse_helpers: { type: 'array', items: { type: 'string' }, description: 'existing helpers/functions Fatia 1 should reuse (path:symbol) instead of reinventing' },\n    gaps: { type: 'array', items: { type: 'string' }, description: 'precise gaps Fatia 1 must close, anchored to a path:line' },\n    pitfalls: { type: 'array', items: { type: 'string' }, description: 'traps to avoid (e.g. config.toml verify_jwt, encrypted views .insert not .upsert, UUID vs slug 22P02)' },\n  },\n  required: ['summary', 'locations', 'reuse_helpers', 'gaps', 'pitfalls'],\n}\n\nphase('Map BoK')\nconst bokDocs = [\n  { f: '04-frd.md', lens: 'Extract ALL FR-VA-* functional requirements. Mark which belong to Fatia 1 = product-aware content generation (use chosen products, not hardcoded regex SKUs) AND cross-surface monetization (affiliate link in ALL outputs, not just the article; thread affiliate_url from the UI). EXCLUDE anything that needs the cron/cadence (R2 recurrence) or the self-improving loop reading optimization_policy at generation time (R3) UNLESS the generator merely WRITES creative_metrics.' },\n  { f: '05-sdd.md', lens: 'Extract the System Design: the generator design, the monetization design, the creative_metrics + optimization_policy schema, begin_autopilot_cycle/finalize_autopilot_cycle RPCs, FK composta tenant-scoped, N_runs formula. Identify what Fatia 1 (no cron) actually implements vs defers.' },\n  { f: '06-data-model.md', lens: 'Extract the full data model: every new table/column/RPC. Flag which Fatia 1 must create via migration (creative_metrics canonical, optimization_policy scope) and which already exist (affiliate_config, vm_affiliate_products).' },\n  { f: '03-prd.md', lens: 'Extract product requirements + the 3 seed SKUs + the MVP surfaces (WP/LinkedIn/X text+image). What is the product-aware generation supposed to feel like for Fatia 1?' },\n  { f: '07-process-flow.md', lens: 'Extract the process flow for a single autopilot generation cycle (the part that runs WITHOUT cron \u2014 a manual/triggered run). What steps, what order, what writes creative_metrics?' },\n  { f: '02-brd.md', lens: 'Extract BR-VA-* business rules + the R1-R4 mapping + any anti-mint/security/tenancy rules that gate Fatia 1.' },\n]\nconst bok = await parallel(bokDocs.map(d => () =>\n  agent(`Read ${BOK}/${d.f} in full. ${d.lens}\\n\\nThis is for scoping Fatia 1 of the Viral Autopilot module (product-aware generator + cross-surface monetization, NO cron/cadence). Return ONLY what the doc actually says \u2014 cite IDs verbatim. Do not invent requirements not in the doc.`,\n    { label: `bok:${d.f}`, phase: 'Map BoK', schema: BOK_FINDINGS }))).then(r => r.filter(Boolean))\n\nphase('Map Code')\nconst codeReaders = [\n  { label: 'orchestrate-content', lens: 'Read supabase/functions/orchestrate-content/index.ts in full. Map: the full campaign pipeline, where mcoCoins are deducted, where it kicks orchestrate-step, how topic/platforms/affiliate_url flow in. Where does product-awareness enter (or not)? Where is affiliate_url received and is it dropped?' },\n  { label: 'orchestrate-step', lens: 'Read supabase/functions/orchestrate-step/index.ts in full. Map: where the article/LinkedIn/X text is generated, where the 3 SKUs are hardcoded via regex, where affiliate links are attached (and to WHICH surfaces \u2014 only article?), how _shared/affiliate.ts is used.' },\n  { label: 'affiliate-shared', lens: 'Read supabase/functions/_shared/affiliate.ts in full + grep how buildMlProductUrl / the redirect link is built. Map the per-user affiliate resolution (affiliate_config, vm_affiliate_products, record_affiliate_click). What is the canonical way to build a tracked monetized link today?' },\n  { label: 'ui-trigger-affiliate', lens: 'Find where the UI sends affiliate_url / products / topic into the pipeline: src/components/orchestrator/nodes/TriggerNode.tsx, src/store/useOrchestrationStore.ts, src/hooks/useOrchestrationGraph.ts. Show exactly where affiliate_url is set in the UI and where it gets dropped before reaching the edge function.' },\n  { label: 'affiliate-products-data', lens: 'Map the per-user product source: src/hooks/useAffiliateProducts.ts + vm_affiliate_products table + AffiliateProductsPage.tsx + affiliate_config. How does a user pick which products to monetize? What columns exist (product_url, affiliate_template_url, sku)?' },\n]\nconst code = await parallel(codeReaders.map(c => () =>\n  agent(`${c.lens}\\n\\nThis is for scoping Fatia 1 of the Viral Autopilot module. Be precise with path:line. Goal: make the generator product-aware (use the user's chosen products) and monetize EVERY surface (not just the article), threading the UI's affiliate_url. Return the live state + exact gaps. Do not propose code yet.`,\n    { label: `code:${c.label}`, phase: 'Map Code', schema: CODE_FINDINGS }))).then(r => r.filter(Boolean))\n\nphase('Synthesize')\nconst SCOPE = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    fatia1_scope_statement: { type: 'string', description: 'a crisp 3-5 sentence definition of exactly what Fatia 1 delivers, anchored to FR-VA-* IDs' },\n    in_scope_frs: { type: 'array', items: { type: 'string' }, description: 'FR-VA-* IDs that Fatia 1 implements' },\n    deferred_frs: { type: 'array', items: { type: 'string' }, description: 'FR-VA-* IDs explicitly deferred to later slices (cron/cadence/self-improve) with one-line why' },\n    migrations_needed: { type: 'array', items: { type: 'string' }, description: 'new migrations required (table/column/RPC) or \"none \u2014 Fatia 1 is edge+UI only\"' },\n    files_to_touch: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        properties: {\n          path: { type: 'string' },\n          change: { type: 'string', description: 'what changes and why, anchored to a gap' },\n          risk: { type: 'string', enum: ['low', 'medium', 'high'] },\n        },\n        required: ['path', 'change', 'risk'],\n      },\n    },\n    implementation_steps: { type: 'array', items: { type: 'string' }, description: 'ordered, each with a material success criterion' },\n    sovereign_decisions: { type: 'array', items: { type: 'string' }, description: 'genuine decisions only the Sovereign can make (scope/UX/economic), or empty if none' },\n    risks: { type: 'array', items: { type: 'string' }, description: 'security/tenancy/economic risks + the FMEA/OTD id each maps to' },\n    verification_plan: { type: 'array', items: { type: 'string' }, description: 'how Fatia 1 will be MATERIALLY proven (Lei 1): tsc, smoke, E2E paid run, deploy chunk diff' },\n  },\n  required: ['fatia1_scope_statement', 'in_scope_frs', 'deferred_frs', 'migrations_needed', 'files_to_touch', 'implementation_steps', 'sovereign_decisions', 'risks', 'verification_plan'],\n}\nconst scope = await agent(\n  `You are the MCORCH Master Execution Agent scoping Fatia 1 of the Viral Autopilot module (BoK sealed at docs/bok/viral-autopilot/, gate OPEN).\\n\\n` +\n  `Fatia 1 = the first code slice: make the content generator PRODUCT-AWARE (use the user's chosen products instead of 3 hardcoded regex SKUs) and MONETIZE EVERY OUTPUT SURFACE (article + LinkedIn + X, not just the article), threading the UI's affiliate_url that is currently dropped. It does NOT depend on the cron/cadence (R2) and does NOT need to read optimization_policy at generation time (R3) \u2014 though it MAY write creative_metrics so the future self-improve loop has data.\\n\\n` +\n  `BoK contract findings:\\n${JSON.stringify(bok, null, 2)}\\n\\n` +\n  `Live code findings:\\n${JSON.stringify(code, null, 2)}\\n\\n` +\n  `Produce a precise, buildable Fatia 1 scope. Honor: per-user credential resolution (auth.uid()), fail-closed, no negative deduct (anti-mint RPC), encrypted-views write pattern, config.toml verify_jwt for pg_net paths, hotfix\u2192migration same session. Keep Fatia 1 as small and safe as possible while closing the real R1/R4 gaps the audit found. Flag ONLY genuine Sovereign decisions \u2014 pick sensible defaults for everything else.`,\n  { label: 'synthesize:fatia1-scope', phase: 'Synthesize', schema: SCOPE })\n\nreturn { bok, code, scope }\n",
  "description": "Map Viral Autopilot Fatia 1 contract + code"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wpwte070v
> Summary: Map the viral-autopilot BoK contract for Fatia 1 + the live code state to scope the first slice precisely
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cdba5e5b-0613-433e-84ae-1ff6e559e8c5/subagents/workflows/wf_f6bfec39-d04
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cdba5e5b-0613-433e-84ae-1ff6e559e8c5/workflows/scripts/viral-autopilot-fatia1-map-wf_f6bfec39-d04.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cdba5e5b-0613-433e-84ae-1ff6e559e8c5/workflows/scripts/viral-autopilot-fatia1-map-wf_f6bfec39-d04.js"} to iterate without resending the script.)
> Run ID: wf_f6bfec39-d04
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/cdba5e5b-0613-433e-84ae-1ff6e559e8c5/workflows/scripts/viral-autopilot-fatia1-map-wf_f6bfec39-d04.js", resumeFromRunId: "wf_f6bfec39-d04"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(02:15:28)*


## 🤖 Claude *(02:15:34)*

Workflow de mapeamento rodando em background (`wpwte070v`) — 6 readers da BoK + 5 readers do código vivo → síntese do escopo da Fatia 1. Serei notificado quando concluir; aí trago o escopo cravado (FRs in/out, migrations, arquivos a tocar, decisões que são suas) antes de codar.

Enquanto isso, o que esse mapeamento vai resolver, alinhado à auditoria que selou a BoK:
- **R1/R4 — gerador product-aware:** trocar os 3 SKUs hardcoded por regex pelos produtos que o usuário escolheu (`vm_affiliate_products`/`affiliate_config` per-user).
- **R1/R4 — monetização cross-surface:** hoje o link de afiliado entra só no artigo; a Fatia 1 leva o link rastreável para LinkedIn + X também, e costura o `affiliate_url` da UI que hoje é dropado antes de chegar na edge function.
- **Sem cron:** a cadência (R2) e o loop auto-melhorável que lê `optimization_policy` (R3) ficam para fatias seguintes — mas o gerador já pode *escrever* `creative_metrics` para alimentar o futuro loop.

Aguardando o resultado.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-20 - Estratégia de lucro em mixed, trend e outros]]
> * **Próxima Sessão**: [[2026-06-20 - agent-a14f2aab56c8204d1]]
%% --- TIMELINE END --- %%

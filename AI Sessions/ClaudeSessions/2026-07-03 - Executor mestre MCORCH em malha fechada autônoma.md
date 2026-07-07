# [[2026-07-02 - Executor mestre MCORCH em malha fechada autônoma|Executor mestre MCORCH em malha fechada autônoma]]
**Date:** 2026-07-03 | **Session ID:** `0c1ad55a-1aef-4790-9a42-92684bcd77d2`

---

## 👤 User *(02:53:35)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(02:53:35)*

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


## 🤖 Claude *(02:53:41)*


## 🤖 Claude *(02:53:41)*

Executando o ritual /handson — pre-flight em paralelo.

## 🤖 Claude *(02:53:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7 && echo \"---STATUS---\" && git status --short && echo \"---DIFFSTAT---\" && git diff HEAD --stat | tail -5",
  "description": "Show recent commits and working tree status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> e7d987d docs(handoff): fix path claim — src/lib/universe-layout.ts (5c audit caught the imprecision)
> 067cd02 docs(handoff): seal loop it.5-6 — editor público LIVE + universe sinapses/fly-to
> 75c6963 docs(readme): v6.72.0 — Universe 3.5+3.6 (sinapses reais + fly-to) + video.mcorch.com LIVE — mesh 9018
> 5d35ae1 docs(loop): charter — 3.5 sinapses + 3.6 fly-to shipped (25 sinapses reais, Vision-QA high)
> 645a16e feat(universe): 3.5 real inter-network synapses + 3.6 click-to-select camera fly-to
> 869de0f docs(loop): charter — achado 3.5 (7 arestas cross-partition reais) + pausa por session limit até 23:10
> c849f41 docs(loop): charter — OTD-VS-015 verificada LIVE (editor público SSO-gated E2E provado)
> ---STATUS---
> ---DIFFSTAT---
> ```

## 🤖 Claude *(02:53:43)*


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

## 🤖 Claude *(02:53:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; curl -s -m 5 http://localhost:8001/api/v2/heartbeat; echo; ls docs/bok/ 2>/dev/null; echo \"---WC---\"; wc -l HANDOFF.md; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"",
  "description": "Check containers, Chroma health, BoK suites, HANDOFF size, scratch"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 2 days (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> {"nanosecond heartbeat":1782960826818303392}
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
> ---WC---
> 9070 HANDOFF.md
> ⚠️ scratch/ has files
> ```

## 🤖 Claude *(02:53:47)*


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
> 14	## Handoff Seal Record (2026-07-01) — Loop Autônomo it.5-6: Editor Público LIVE + Universe Sinapses/Fly-to
> 15	
> 16	Selo (`/handoff` explícito do Sovereign = stop do loop) das iterações 5-6 pós-seal-2b. **ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (Gabriel) · Owner = Sovereign (canvas novo é rota paralela — 3 páginas legadas intactas até paridade 3.9; editor público é SSO-gated).
> 17	
> 18	| Fatia | Prova material (Lei 1) | Commits |
> 19	|-------|------------------------|---------|
> 20	| **it.5 — OTD-VS-015 VERIFICADA LIVE** (Fila destravada por descoberta oportunista) | Cadeia pública E2E: CF SSL válido → nginx origem (302 gate sem cookie) → sso-auth-gate ES256 (cookie=JWT User 0 mintado via generateLink→verifyOtp) → `127.0.0.1:3210` nosso host — `/healthz {ok,ui:true}` + `/api/projects` (2 projetos) + SPA **"MCORCH Studio"** (rebranding `sub_filter` no vhost; logo HeyGen oculto — Apache-2.0 §6). **Editor billável acessível ao Sovereign** | `c849f41` |
> 21	| **it.6 — Universe 3.5 Sinapses REAIS + 3.6 Fly-to** | Sinapses = arestas reais `mcorch_edges` ancoradas por membership dos 2 sets renderizados (**25 vivas**; censo por node_type=7 — ambos honestos, membership = verdade do render); fetch escopado DERIVES_FROM/observes; `src/lib/universe-layout.ts` = fonte única de projeção; CameraRig easing + click-to-select nas 2 redes (getState em handler/useFrame — guarda Error #185). **Browser-verified** (preview+sessão injetada: 8.599 nós/8.816 arestas/775 comun.; clique sintético → `memory · af33a839…` + câmera voou; **0 erros console**) · **Vision-QA confidence high** · tsc 0 · **deployado** (`UnifiedCanvasPage-oTw8MRCw.js`) | `645a16e` |
> 22	| **Anticorpo — session limit** | ~20:20 subagentes rejeitados (reset 23:10) matou Workflow `wf_4674cd50-64c` → adaptação honesta: probe SQL barato ANTES da pausa (achado: partição `ast_*` ~8.2k; `mcorch_edges` = `source_id`/`target_id`/`relation_type`; 7 cross-partition por node_type), pausa registrada, retomada pós-reset com understand solo | `869de0f` |
> 23	
> 24	Handoff node `5a67187d-3f9d-4f73-819e-01601017d698` inserido + embedado (768d). Mesh **9018 nós** (count=exact). **Universe restante:** 3.7 perf (query ~30s OTD-UCANVAS-PERF) · 3.8 poda ownership-query morta · 3.9 paridade + gate E2E + cutover (confirmar com Sovereign) · 3.10 seal.
> 25	
> 26	## Handoff Seal Record (2026-07-01) — Loop Autônomo (retomada): HyperFrames Nativo + Fase B Editor Billável VIVO
> 27	
> 28	Selo incremental (`/handoff`, ritual passo 6 — fronteira de Fatia) da **retomada do loop autônomo** pós-pausa Sovereign (gate temporal 1:51). **3 iterações fechadas** (`c422de7 → 53ff56d`, 7 commits + este seal), cada uma com prova material (Lei 1) e commit granular. tsc **0** em todos os passos. Nenhuma migration nesta sessão (sem `/security-review` requerido; path-safety re-provada por smoke).
> 29	
> 30	**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (Gabriel) · Owner = Sovereign (risco = render do editor quebrar — mitigado por wrap-rollback `STUDIO_RENDER_ENGINE=cli` + rollback do service no unit file; ROI = equity/exclusividade + limpeza de licença do pipeline billável).
> 31	
> 32	| Fatia | Prova material (Lei 1) | Commits |
> 33	|-------|------------------------|---------|
> 34	| **HyperFrames nativo (FR-VS-050/OTD-VS-020)** — render studio-project em `@hyperframes/core` Apache-2.0 (CLI license-None fora do default; elimina HF_CLI/HF_NODE/trap ARM64) | Licença verificada na fonte (CLI tarball **sem** LICENSE/campo; core **com**; runtime byte-idêntico `1bc431f0…`) · frame-diff sha-distinto t=1s/t=6s · byte-determinismo `c721f8f4…` 386.795B · **A/B SSIM 0.9934** vs ref CLI · Vision-QA **high** · guard 4/4 · worker E2E `020e9bef` done→bucket byte-idêntico · Workflow 4-lentes `wf_bbc8402d-096` · SDD §VS-UI-C v0.6 | `c422de7` (BoK) + `2ce09b3` (feat) |
> 35	| **Fase B 2a — Studio Host + McorchAdapter + FR-VS-048 (A)** — `createStudioApi(mcorchAdapter)` 13 métodos; seam startRender minta JWT User 0 → `video-render` (chokepoint único de billing) → observa `video_renders` → materializa MP4 | **E2E PAGO testemunhado**: 202 → row `b25838a0` (12 mco, 4636→4624) → worker nativo → done → `renders/*.mp4` 386.795B sha `c721f8f4` (4º byte-idêntico) → download 200 → SSE complete · smoke **6/6** zero-cost · SOP Lei 2 `video-studio-host-fase-b.md` ANTES do código · **Achado: `VIDEO_HYPERFRAMES_WEBHOOK=poll://` já ativo** (Fila stale corrigida) | `2123a79` |
> 36	| **Fase B 2c — EDITOR BILLÁVEL VIVO NO 3210** — SPA pré-buildado do `@hyperframes/studio` (React 19 bundlado, Apache-2.0, telemetria só same-origin) servido pelo nosso host; `video-studio.service` swapado (vanilla license-None fora do serving; rollback comentado no unit) | Browser-verify 3210 `#project/mcorch-video` (hash real = `#project/<id>`, blueprint corrigido) → file-tree + preview 9:16 + timeline **Glow/Brand/Hook** + **0 erros console** · **Vision-QA confidence high "Aprovado"** · multi-projeto (upgrade) · systemd active + **self-healed** pós-kill · carrier isolado `packages/video-studio-host-ui/` (react@19 nunca no SPA React 18) | `e8979e2` |
> 37	
> 38	| **Fase B 2b — FR-VS-049 durabilidade Storage↔volume (it.4, pós-seal)** — sweep write-back periódico+SIGTERM p/ bucket privado `video-studio-projects` + materialização staging+rename atômico no `resolveProject` (negative-cache 60s); FS local segue canônico (§B.4) | Migration `20260701120000` aplicada via Management API (`public:false` verificado) · smoke **7/7** (round-trip sha256-igual · `renders/` excluído · ghost honesto) · journal `[sync] uploaded 14 files` · `mcorch-video` espelhado · **/security-review NO FINDINGS** + guard `..` anticorpo · tsc 0 | `4fd9b89` |
> 39	
> 40	Milestone/handoff nodes `835c8a43-59dc-4de4-bd61-f6ed83681a18` + `03a26786-4bb5-4b5a-b6e4-b68b1041ae91` (2b) inseridos + embedados (768d). Mesh **9017 nós** (count=exact live). **Fase B core COMPLETA** (FR-VS-050 nativo · 2a chokepoint pago · 2c editor vivo 3210 · 2b durability). **Restante:** deletar wrap CLI + desinstalar `hyperframes` global (pós uso real do editor pelo Sovereign) · vhost cert `video.mcorch.com` (Fila OTD-VS-015).
> 41	
> 42	## Handoff Seal Record (2026-07-01) — Loop Autônomo Multi-Ciclo: Arco de Segurança + Smart-Delete MVP + Observability zero-USD
> 43	
> 44	Selo formal (`/handoff`, GO explícito do Sovereign) de uma **sessão-maratona de loop autônomo** (`6bea97b → c2cb715`, ~10 iterações, cada Fatia committada+pushed incrementalmente). Os records por-Fatia abaixo têm o detalhe; este é o wrap. Suíte de testes: **340 passed / 0 failed** (tsc 0). Commits-chave: `78a59e1` (seal) · `c5614f7` (streaming observability) · `b711cdb` (P0 anon RPC) · `9fe1e36` (P0 mint profiles).
> 45	
> 46	**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (Gabriel) + `/security-review` independente por migration (todos CLEAN) · Owner = Sovereign (risco financeiro/irreversível dos 3 P0s de ledger-tamper e das ações destrutivas do Smart-Delete).
> 47	
> 48	**Entregas (dois arcos completos + 1 feature + 1 observability arc):**
> 49	1. **Smart-Delete MVP** — `check-post-existence` (FR-SD-001) + `delete-remote-post` (FR-SD-002, idempotente WP/X/Pinterest, golden-rule) + UI 3-ramos no calendário (FR-SD-003, browser+Vision-QA). Workflow adversarial pegou 1 HIGH de false-success destrutivo.
> 50	2. **Observability zero-USD 100%** — custo LLM MEDIDO nas 3 vias: `llm_usage` texto não-streaming (it.9) + `image_usage` (it.4) + **streaming** (`generate-content` tee, E2E provado, `{fn:generate-content, total_tokens:208}`).
> 51	3. **🔴 Segurança — ledger-tamper (3 P0s reais, provados LIVE):** (a) `profiles.mco_balance` — user logado cunhava próprio saldo → guard-trigger `current_user`; (b) 2 colunas server-owned (`marketing_attribution.revenue_cents` + `agent_executions` metering) → guard-triggers; (c) **o pior:** `anon` (chave publishable **pública**) cunhava (10→1.000.009) e **apagava** contas via `add_mco_coins`/`soft_reset_account` (grant-drift deixou `anon`) → REVOKE→service_role-only.
> 52	4. **🔴 Segurança — cross-tenant RLS:** baseline forte (0 tabelas RLS-off; `USING(true)` são catálogos compartilhados) + `infra_health_logs` leak de user_id fechado (admin-only).
> 53	
> 54	**Anticorpos permanentes:** `scripts/qa/audit-privileged-rpc-grants.sh` + queries de auditoria RLS/coluna + smokes zero-cost (`smoke-check-post-existence` 9/9 · `smoke-delete-remote-post` 8/8 · `smoke-economic-freeze` 11/11 · `smoke-financial-column-guards` 8/8 · `smoke-privileged-rpc-lockdown` 4/4 · `smoke-infra-health-rls` 2/2). **Todas as migrations passaram `/security-review` independente CLEAN.** tsc 0. Handoff node `d00f0ae2-c088-432b-a4df-6ba50f2c9c01` (embedded 768d).
> 55	
> 56	> **Marco:** a superfície de **mint/wipe/leak** do produto está fechada `anon` **E** `authenticated` — pré-requisito de segurança para onboarding de clientes pagantes. Custo LLM 100% mensurável (GO $0).
> 57	
> 58	## Session Seal — Loop Autônomo: Auditoria de Cobertura RLS (baseline limpa + 1 leak cross-tenant fechado) (2026-07-01)
> 59	
> 60	Fecha o arco de segurança com a classe **cross-tenant leak (FMEA-011)**: cobertura RLS. **Baseline FORTE:** 0 tabelas em `public` com RLS desabilitado; os 12 `USING(true)` de SELECT client são **catálogos compartilhados por design** (`agent_pricing`/`vm_trends`/`vm_niches`/`vm_affiliate_products`/`pantheon_global_configs`/`system_milestones`) — sem vazamento.
> 61	
> 62	**Único leak real:** `infra_health_logs` (global-read `USING true`) carregava `user_id` per-tenant no metadata (11 rows: sentinel prompt-injection · quarantine freeze · avatar-consent) → qualquer authenticated lia os user_ids + eventos de segurança/consentimento de outros tenants (info-disclosure LGPD-adjacent). **Fix (commit `d79d228`, migration `20260701040000`):** SELECT → **admin-only** `has_role('admin')` (espelha `security_events`; defense-in-depth). Nenhum cliente lê a tabela direto (a Neural HUD usa a edge fn service-role `get-infra-status`, `useInfraStatus.ts:28`). **Prova (Lei 1):** aplicada HTTP 201 · smoke `smoke-infra-health-rls.ts` **2/2** (non-admin→0 rows, service-role→54844, HUD intacta) · **`/security-review` CLEAN**. Milestone `b4e25b30-1959-4a8c-be2a-2503b9dc9df0`.
> 63	
> 64	> **Arco de segurança da sessão COMPLETO** — ledger-tamper (3 P0s: `profiles.mco_balance` mint · colunas financeiras · **anon RPC grant-drift** mint/wipe) + cross-tenant RLS (baseline limpa + `infra_health_logs`). Superfície de mint/wipe/leak coberta anon **e** authenticated. Anticorpos reexecutáveis: `audit-privileged-rpc-grants.sh` + a query de auditoria RLS.
> 65	
> 66	## Session Seal — Loop Autônomo: P0 CATASTRÓFICO — anon cunhava/zerava contas via RPC (grant-drift) (2026-07-01)
> 67	
> 68	Extensão do sweep de segurança para a **classe irmã**: RPCs SECURITY DEFINER callable por cliente que mutam estado privilegiado. Uma enumeração (`has_function_privilege('anon', fn, 'EXECUTE')`) achou o **pior achado da sessão**.
> 69	
> 70	**🔴🔴 P0 (provado LIVE):** `add_mco_coins(user,amount)` e `soft_reset_account(user,balance)` tinham EXECUTE para o role **`anon`** (um REVOKE passado tirou `authenticated` mas deixou `anon`/PUBLIC). A chave publishable é **pública** (bundle do frontend) → um atacante **SEM LOGIN** fazia:
> 71	- `POST /rpc/add_mco_coins {p_amount:999999}` → **cunhava saldo de qualquer user** (provado: vítima 10 → 1.000.009)
> ```

## 🤖 Claude *(02:53:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-56 of 256 total (67062 tokens, cap 25000). Call Read with offset=57 limit=56 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.53.0 — Doutrina Agêntica AGI→ASI + Learning & Adaptation + analytics honesto (2026-06-27)** — sessão-maratona multi-arco. **7 commits.** **(1)** Doutrina `agentic-vision.md` (21 padrões × maturidade + tese Via 4-produto/Via 3-micro) + **Pattern Conformance gate vinculante** no CLAUDE.md §1 + BoK `agentic-governance` 10/10 (seal `34748570`) + 2 docs stale deprecados. **(2)** **Collective Efficiency Ledger** (`81210ab`) — VIEW security_invoker + RPC service-role medem mco/resultado anti-Goodhart (G6 isolamento provado; rollup real 334s vs 2.4s). **(3)** **Learning & Adaptation** (o único padrão fraco) atacado: nervo sensorial (`publication_metrics` + coletor fail-soft IG/FB + painel "Por Publicação" browser-provado) + reward multi-métrica brand-first (mata `totalClicks` Goodhart, prova policy `7d9856d0`) + realocação ε-greedy (`1371094`/`47474ac`). **(4)** Analytics honesto — demo-kill (`b6abff1`) + zeramento dos perfis sociais antigos (marca **Gabriel AI**/**@gabrielOrchAI** começam do zero). **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8971** · handoff `326949f1`. **Pending:** re-OAuth IG insights (destrava o payoff visível) · B4 EWMA · B5 pauta de receita · V4-2 experimento · postback ML · emenda BoK post-engine (YT/TikTok). **Lição:** "não avançamos apesar do dev incrível" = o motor aprendia sobre **placar em branco**; medir o desfecho real é o que faz capacidade virar avanço.
> 8	
> 9	**Sprint v6.52.0 — Gabriel AI mood board + Vision QA gate + 1º ciclo pago de vídeo 9:16 witnessed + billing/CTA fixes + virada brand-persona (2026-06-26)** — sessão-maratona "faça tudo", Usuário 00 sobre Usuário 0. **6 commits.** **(1)** Ciclo pago de vídeo 9:16 witnessed E2E (render real `8b0787e0` 1080×1920) + 2 bugs de receita (`df7505b`): billing cobrava vídeo por sub-run mas só article-flow renderiza → fix por `nVideoRuns`+refund; CTA-leak `mcorch.com` texto-puro → guard bare-text nos 2 formatos. **LinkedIn cadence E2E** (post real `urn:li:share:7476089362896732160`). **(2)** Virada **brand-persona Gabriel AI/CCIO** (plano produto pausado) + blueprint fundamentado YouTube/TikTok (`58e0389`, infra ~90% reusável, gates audit Sovereign). **(3)** Nó `characterReference` vira **mood-board multi-foto** (`549e4dd`) + mood board Gabriel AI gerado E2E (4 retratos face-consistentes Vision-QA-gated + 2 animações DoP) no projeto `b57a59f7`. **(4)** **Vision QA** gate visual sempre-on + canvas `prompt.length` hardening (`a482132`). **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8969** · handoff `5501a101`. **Pending:** emenda BoK post-engine + 3 branches OAuth YT/TikTok (audit = ação Sovereign) · URLs referência 7-dias→públicas (persona durável) · wirar Vision QA dentro de `audit-canvas-ui.ts`/e2e · animações DoP finalizam async · postback ML real. **Lição:** o witness de um ciclo pago expôs 2 bugs de billing/atribuição invisíveis no código estático — rodar o fluxo real (Lei 1) é o melhor detector.
> 10	
> 11	**Sprint v6.51.0 — Fatia 2 vídeo→Instagram Reel PROVADO E2E + Notificações P0 + malha criativa cross-módulo + receita destravada (2026-06-25)** — sessão-maratona "força total pelo primeiro R$", Usuário 00 sobre Usuário 0. **9 commits.** **(1) Receita** (`1ad04c5`): cron auto-publish morto (`/var/log` inacessível)→durável+telemetria; link **meli.la assinado** publicado (sale-attributable, Roborock+Family Hub); CTA-leak fechado; 2 posts injection removidos do LinkedIn. **(2) Canvas white-screen fix** (`46f18ca`): `MODEL_INFO[id].coinCost` em modelId fora do catálogo → `getImageModelInfo`/`getVideoModelInfo` com fallback; **verificação por browser real** (agent-browser+preview+sessão injetada) virou diretiva durável. **(3) Malha cross-módulo:** asset clicável→handoff Canvas (`8c00f88`); white-label HyperFrames nginx sub_filter (`5d58b15`); Biblioteca scroll+filtro-data+metadados (`8fdb435`); starter MCORCH 9:16 **lint 0/0** substitui demo HeyGen (`3efbe75`, AskUserQuestion). **(4) Fatia 2 — vídeo→Reel PROVADO E2E** (`9d9ec03`/`3be06ee`): User 0 **já conectado** (IG `magicorch` MEDIA_CREATOR); `publish-social` IG via `graph.instagram.com`+REELS+id do `/me` (stored id app-scoped rejeitava 100/33). **Reel real: `instagram.com/reel/DaBtVAQkiuz`.** **(5) P0 Notificações** (`bfb0ba3`): sino era placeholder morto (badge "3" hardcoded) + nada escrevia na tabela → `useNotifications`+`NotificationBell`+`_shared/notify.ts`+seed 4 eventos; browser badge "5". **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8962** · handoff `468c15dc`. **Pending:** camada **push** (browser/OS — sem infra) · **Fatia 3 faceless long-form** (filosofia Sovereign: vender mostrando produto útil no momento certo, redes=entretenimento não venda) · CF público liberado (404=challenge caiu) mas WP posts são draft + Autopilot dormente → flip wp_status+ativar cadência (GO de gasto) · FB Reel (precisa Page). **Lição:** checar a conexão REAL (Lei 1) revelou que o IG já publicava — o publisher só apontava pro lugar errado.
> 12	
> 13	**Sprint v6.50.0 — HyperFrames editor LIVE + creative_assets spine (Fatia 1 bidirecional) + auth gating + Canvas bug fix (2026-06-25)** — `/handson` → editor HyperFrames → pedidos do Sovereign, sob **ultracode**. **4 arcos:** **(1) Editor HyperFrames VIVO** (`video.mcorch.com`): o servidor oficial `hyperframes preview` (NLE multi-camada) roda como serviço host systemd `video-studio.service` (node v22; achado: `hyperframes preview` é processo standalone → conflito React 19/18 some sem Docker) atrás do vhost SSO-gated, módulo iframe `/dashboard/canvas/video`; contrato `/api` selado dos `.d.ts` (SDD §VS-UI v0.4 + SOP); Sovereign fez os 2 sudo (cert+symlink), provado pela screenshot dele. **(2) Auth gating `?devLogin`** (público só email/senha; param libera Google+Cadastrar). **(3) Bug de perda de nós do Canvas** (race load/save → guard empty-over-nonempty no `useSaveCanvasGraph`) + projeto `63d406fe` recuperado das execuções. **(4) `creative_assets` SPINE** (diretiva "poder das saídas" bidirecional): tabela canônica fina + RPC `register_creative_asset` (SECURITY DEFINER service-role-only idempotente, guard cross-tenant); /security-review SAFE; smoke 5/5; dual-write em video-bridge/canvas-execute/generate-image; backfill 73 assets; UI Biblioteca de Assets `/dashboard/canvas/assets`. **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8960** · handoff `8eb84bce` · 11 commits. **Decisão arquitetural (AskUserQuestion):** híbrido bidirecional (Canvas autora · HyperFrames renderiza [FFmpeg long-form, n8n fez 51s] · Meta/Orquestra publica). **Ordem das fatias decidida:** ~~Fatia 1 creative_assets~~ ✅ → Fatia 2 vídeo→Meta Reels → Fatia 3 faceless long-form nativo (receita n8n 51s, `.claude/context/faceless-pipeline-reference-2026-06-25.md`) → Fatia 4 handoff Canvas↔HyperFrames (`onSelect` da galeria pronto). **Pending:** Fatia 2-4 + produtor `design-bridge` · ⚠️ Sovereign rotacionar chave Gemini + token Telegram do n8n colado. **Lição:** Management API bane UA Python-urllib (1010) → curl; `hyperframes preview` standalone elimina o Docker do plano original.
> 14	
> 15	**Sprint v6.49.0/v6.49.1 — Vídeo viral 9:16 autônomo + motor HyperFrames vivo → Studio blueprint + gap de billing fechado (2026-06-24)** — `/handson` → "fichar o vídeo 9:16 com a UI editor do hyperframer assim como o open design" → sob **ultracode**. **v6.49.0:** decisão Sovereign (AskUserQuestion) = motor HyperFrames + worker single-tenant, alvo Autopilot-primeiro → BoK gate (Amendment v0.2, FR-VA-022..026 + SOP) → **motor HyperFrames VIVO** (`render-core.ts` Playwright+FFmpeg → MP4 9:16 1080×1920 sha256-idêntico NFR-VS-016; worker `video-bridge.ts` systemd active; bucket; edge `poll://`) → integração Autopilot (custo no pré-débito do ciclo OTD-VA-010; E2E real "Roborock S8…" render 9:16, saldo intacto). **v6.49.1:** **(1)** deepsearch do HyperFrames Studio (`ae8b94c5`, Apache-2.0) → flip OTD-VS-005 A→C **módulo-container** (StudioApp zero-props + seam `StudioApiAdapter`; embed in-SPA inviável React 19 vs 18); blueprint `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`. **(2)** gap de billing OTD-VA-010 fechado: crédito compensatório idempotente `refund_autopilot_video_enqueue` (migration `20260624140000`) no fail-open do enqueue (actual otimista contava 12 sem linha → cobrança-sem-valor); smoke **8/8** net-debit-exclui-12. **Prova:** `/security-review` SAFE (motor + billing) · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8959** · handoff `b42e89f9`. **Pending (próxima):** **Fatia VS-UI** editor Studio módulo-container (API `/api` → container React 19 → `McorchAdapter` → vhost `studio.mcorch.com` [DNS Sovereign] → render-parity gate) · 1º ciclo pago de vídeo witnessed · Unified Canvas 3.5-3.10 · postback ML real · Security BoK suite (diferida). **Lição:** o achado material (orchestrate-content é async → autopilot-run finaliza ANTES dos enqueues) inviabilizou a Option 1 do diretivo e decidiu o design do fix; o deepsearch pré-código achou o seam zero-props que evita forkar a UI HeyGen.
> 16	
> 17	**Sprint v6.48.0 — Viral Autopilot ATIVADO + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR (2026-06-23)** — `/handson` → "vamos com os próximos passos" → "continue" (×N) sob **ultracode** (4 workflows adversariais). 3 arcos. **(1) Viral Autopilot ATIVADO:** heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** (cycle `947ef8b5` completed, débito 22/refund 2, saldo 5096→5076, 2 sub-runs `done`) — GO Sovereign respeitado; trap material: produto resolve por `external_id`, não UUID. **(2) FR-VA-018** trend-informed angle: `autopilot-run` lê `vm_trends` (fonte global não-confiável) → gate `sanitizeTrendTitle` (whitelist destrói URLs/payloads + reject de verbos) → DADO inerte; red-team `wf_6cc97c75` pegou MEDIUM (sentinel English-only → injection pt-BR cross-tenant), hardened. **(3) Segurança social-auth** (auditoria per-user): state OAuth **HMAC** fail-closed + janela ts 10min (`_shared/oauth-state.ts`) + `instagram-webhook` **X-Hub-Signature-256**; 8/8 gates. **(4) OTD-VA-018-SENTINEL-PTBR:** 7 famílias pt-BR no Cyber-Sentinel, **0 FP real** em 58 amostras (loop `wf_0459e1c1` → tunei f3/f4/f5), live 403 `score=2` sem regressão do inglês. **Prova:** `/security-review` SAFE múltiplo · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8954** · handoff `bc175ac9` · 6 commits. **Pending (próxima):** Unified Canvas 3.5-3.10 (gate visual 1920×1080) · mídia viral 9:16 · postback ML real · Security BoK suite (diferida). **Lição:** o sentinel é TRIAGE score≥2 — single-intent passa por design (=inglês), defesa cross-tenant é o gate de fonte; testar FP contra copy real é o make-or-break ao tocar o pipeline vivo.
> 18	
> 19	**Sprint v6.47.0 — Per-user 100% (env = só infra) + CF WP unblock + sweep per-user FECHADO (2026-06-22)** — `/handson` → "resolver CF WAF + secrets, depois os próximos passos". **(1) CF WP unblock RESOLVIDO:** o componente de skip que faltava no Cloudflare era **"Nível de segurança"** (challenge por reputação de IP de **datacenter** Oracle AS31898, não bot/UA) — diagnosticado via Security→Events (a regra Skip já disparava `Ignorar`, mas o Nível de segurança desafiava por cima). Regra CF header-gated + secrets `WP_PUBLISH_SECRET`/`_HOST`; E2E `publish-wordpress`→`post_id 18`. SOPs `wordpress-cf-publish-unblock.md` (atualizada) + `wordpress-cf-per-user-publish.md` (multi-tenant). **(2) Diretiva Sovereign env=só-infra:** auditoria per-user (workflow `wf_102ef5ac`, 49 fns; 30 per-user · 11 fallback-ok · 4 remediadas) → removido `|| Deno.env.get(<provider>)` de **25 fns user-facing** (47 ocorrências) → per-user PURO fail-closed; 2 fns de sistema (`embed-mcorch-node`/`search-constellation`) → `MESH_EMBED_*` dedicadas; secrets antigos mantidos (seed source) + `.env` anotado. **(3) Sweep per-user FECHADO:** #1 openrouter-swarm · #2 canvas-execute Higgsfield · #3 fetch-trends (migration `rapidapi_key` + UI + 402 provado) · + `aios-chat-gateway` token vazado fail-closed. BYOK do User 0 seedado do `.env`. **Prova:** `/security-review` SAFE 2× · 27 fns deployadas 0 falhas · embedding pós-rename 200 · OpenRouter autenticou com chave per-user do User 0 · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8947** · handoff `4e57bf72`. **Pending (próxima):** segurança `social-auth-callback` HMAC + `instagram-webhook` signature · **C** 1º ciclo pago (CF desbloqueado!) · BYOK imagem opt-in · impl WP-CF per-user. **Lição:** o E2E "falhou bonito" (OpenRouter 404-de-modelo + `user_id`) PROVOU a chave per-user; o approach atômico do Higgsfield pegou o trap do row null/secret antes do deploy; o "Nível de segurança" só apareceu no Security→Events (não chutei checkbox).
> 20	
> 21	**Sprint v6.44.0 — Viral Autopilot Fatia 2: cadência R2 + loop R3 auto-melhorável + UI (2026-06-20)** — `/handson` → "vamos aos próximos passos"; 4 GOs Sovereign (AskUserQuestion: migration · edge fns · R3 · selar). Closed-Loop por fatia (mapeamento do contrato vivo → SOP Lei 2 → código → /security-review → deploy → smoke zero-cost → seal). **Motor autônomo R1+R2+R3+R4 COMPLETO, zero gasto do Sovereign.** **(1) Fundação** (`686bae3`): SOP `autopilot-cron-identity.md` (OTD-VA-008, 10 gates) + migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant-escopada + RPCs `begin_autopilot_cycle` [cap+pré-débito ÚNICO sob `pg_advisory_xact_lock` anti-TOCTOU] / `finalize_autopilot_cycle` [refund crédito-positivo idempotente, espelha `finalize_vision_job`], service-role-only) + smoke RPC 11/11 (`0c59e4d`). **(2) Edge fns** (`54ac2a9`): `autopilot-run` (executor identidade 2-caminhos → begin → fan-out `orchestrate-content` prepaid → finalize → re-arma; dry_run) + `autopilot-cadence-cron` (driver pg_cron, espelha nurture-cron, 403 sem service-key) + orchestrate-content FR-VA-016 prepaid (user-path intacto); smoke 9/9. **(3) R3 loop** (`35554da`): `autopilot-analyze` (FR-VA-010, ranqueia `creative_metrics`→`optimization_policy`, tenant da linha) + `autopilot-collect` (FR-VA-008, ledger→métricas) + orchestrate-step FR-VA-011 (injeta diretiva nos 3 prompts); smoke loop 11/11. **(4) UI** (`bfd178b`): `useAutopilot`+`AutopilotPage` (`/dashboard/autopilot`) + rota + nav; types.ts regen additive. **Prova:** `/security-review` SAFE **3×** · 3 smokes zero-cost (**31 gates**) · 6 edge fns deployadas · migrations via Management API · render ocular (preview local à prova de CF) · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8935** · handoff `280e94d7`. **Pending (ação Sovereign):** ativar `pg_cron` + 1º ciclo **PAGO** real (gated nos 2 blockers: CF WAF `/wp-json` + OpenAI image) · `fetch-trends`→pauta (FR-VA-018, último autônomo). **Lição:** mapear o contrato vivo antes de cada fatia pegou correções materiais (analyze lê `creative_metrics` não `affiliate_links`; cost-model prepaid); `/security-review` independente 3× confirmou o caminho de dinheiro fechado; selei ao esgotar o roadmap autônomo (resto Sovereign-side).
> 22	
> 23	**Sprint v6.43.0 — Viral Autopilot Fatias 1 + 1b: gerador product-aware + monetização cross-surface + imagem (2026-06-20)** — `/handson` → "vamos aos próximos passos" sobre o roadmap do Viral Autopilot (BoK gate ABERTO). Closed-Loop por fatia (mapeamento workflow → escopo → SOP Lei 2 → código → /security-review → deploy → E2E pago → seal). **(1) Fatia 1** (`4af8b8b`): gerador product-aware (FR-VA-003, prompts virais featuring o produto escolhido; fallback B2B backward-compat) + monetização nas **3 superfícies** (FR-VA-004, `affiliate_links.content_id` antes-null **FECHADO**) + threading `product_ids` sanitizado pelo sentinel (FR-VA-016) + tabela `creative_metrics` (FR-VA-009, RLS provada) + picker na TriggerNode. **(2) Fatia 1b** (`ba5d281`): imagem product-referenced (FR-VA-013) DENTRO do article_generation, **fail-open** (`skipped`, nunca quebra a geração), PATH durável em `content_library.media_url`, dual-path auth na generate-image; sem migration/frontend/cobrança extra. **(3) fix generate-image** (`803f946`): bug universal `response_format` (OpenAI removeu o param) → removido + tratamento url/b64 + surfacing. **(4) Diagnóstico saída visível** (Sovereign pediu "destravar"): WP=Cloudflare challenge no /wp-json (ação: WAF Skip como mcp.mcorch.com), nanobana=DNS morto, openai=chave-projeto sem acesso a modelo de imagem (config OpenAI). **Prova:** 2 E2E pagos (`158ba7fc`/`46a98963`, delta 10 cada · 3/3 content_id NON-NULL · fail-open) · UI ocular 1920×1080 · /security-review SAFE 2× · tsc 0 · 295 testes · Phase 5c **SEAL ALLOWED** (10) · mesh **8934** · handoff `385d3dd5`. **Pending:** Fatia 2 cron/cadência R2 (SOP `autopilot-cron-identity.md` Lei 2/OTD-VA-008) · loop R3 · anexo imagem no publish-layer · **2 ações Sovereign** (CF WAF skip /wp-json + OpenAI image model access). **Lição:** mapear o contrato vivo ANTES de codar pegou 3 correções materiais (imagem text-only, dual-path auth, response_format); diagnóstico por status/headers reais cravou as causas; não fabriquei imagem visível (providers do tenant quebrados = config, declarado).
> 24	
> 25	**Sprint v6.42.0 — Viral Autopilot BoK 9/9: motor de conteúdo viral autônomo (R1-R4) (2026-06-17)** — `/handson` → diretiva Sovereign de **retomar o objetivo-núcleo de receita** (= o próprio Sprint Goal "distribuição social autônoma operacional"): alimentar redes com conteúdo viral auto-gerado/agendado (tudo de uma vez OU a cada N dias), que a cada ciclo analisa o anterior p/ melhorar os próximos criativos, monetizado c/ afiliado ML. Arco Closed-Loop puro (zero código de produto): **(1) Auditoria material** (workflow 7 agentes, prova path:linha) — R1/R4 parciais vivos, **R2 (recorrência) e R3 (loop auto-melhorável) AUSENTES** (`campaign_metrics` sem writer, `optimization_policy` nunca lida, `self-optimize` sem cron); **(2) 4 decisões soberanas** (AskUserQuestion: suite NOVO · MVP texto+imagem · sinal R3 combo · 3 SKUs); **(3) BoK 9/9** (1889 LOC, FR-VA-001..021, 12 FMEA 4×RPN>100); **(4) Validação Fase 6 em 4 rodadas adversariais** (4 críticos/rodada) + grep determinístico — pegou buraco de segurança real (cron `verify_jwt=false` sem prova service-role in-function) + anti-mint (refund por deduct negativo, que EU introduzi); **(5) seal** (node `b3398294` embedded 768d, DERIVES_FROM marketing-hub). **Prova:** tsc 0 · 3 commits pushed · Phase 5c **SEAL ALLOWED** (10) · mesh **8928** · handoff `496ec17c`. **BoK Gate ABERTO.** Pending: fatia 1 (product-aware + monetize, NÃO depende do cron) + SOP `autopilot-cron-identity.md` (Lei 2/OTD-VA-008) antes da cadência. **Lição:** verificação adversarial multi-rodada foi essencial — cada "fix" meu deixava um resíduo que a rodada seguinte pegava; não auto-declarar GO (Lei 1).
> 26	
> 27	**Sprint v6.41.0 — Unified Sensorial Canvas (Phase Epsilon V9): AGI→ASI ref + emenda BoK + Fases 3.1-3.4 (2026-06-17)** — `/handson` → conversa estratégica (Model Council; plugin `claude-code-setup`; paper *From AGI to ASI* DeepMind) → diretiva arquitetural **Unified Core Sensorial Canvas** (fundir Core-Fable + Matrix + Memória num canvas 3D R3F). Arco Closed-Loop: **(1) Fundamentação** — arXiv 2606.12683 (Legg/Hutter/Leibo) lido inteiro (57p) + selado como nó `architecture` `a576216e` (edge INFORMS→openclaw) + checklist Via 4 (`.claude/context/agi-asi-via4-design-checklist.md`); tese: o MCORCH é a Via 4 (group agent formation) instanciada na app layer. **(2) Auditoria de clusters (Lei 1)** — Louvain = REAL/VIVO (`useConstellationSigma.ts:227`, graphology client-side); squad-coloring = MORTO (`crew_module_ownership` 0 rows → fallback Louvain) + heurístico (`inferSquad`) → **Decisão B = PODAR** (Louvain oficial; OTD-SQUAD-OWNERSHIP-REVIVAL). **(3) Emenda BoK** (gate Sovereign-eleito sobre override) — `mcorch-constellation` +PR-025/FR-043..049/NFR-023-024/SDD §9 (reconciliação Sigma→R3F: graphology cérebro / R3F corpo). **(4) Fases 3.1-3.4** (R3F, commits granulares, 3 páginas legadas preservadas) — scaffold rota `/dashboard/universe`/store/shell 72-28 + Code Network InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop (memória corrigida: glow aditivo). **(5) E2E ocular** (preview local à prova de CF + sessão injetada) nos 3 modos — telemetria real (8.560 nós/8.816 arestas/~733 comun./159 pensamentos); "esfera órfã" desmistificada = **spinner de loading**. **Prova:** tsc 0 em cada fase · 9 commits pushed · Phase 5c **SEAL ALLOWED** (handoff `5225ff03` verificado) · mesh **8926**. **Restam (Pending):** 3.5 Sinapses (arestas REAIS de `mcorch_edges`) · 3.6 fly-to · 3.7 layout/perf (**OTD-UCANVAS-PERF** — query do código ~30s c/ 2 canvases) · 3.8 poda · 3.9 paridade+gate E2E 1920×1080 · 3.10 seal. **Lição:** auditar materialmente ANTES de codar (Louvain vivo vs squad morto) + emenda BoK ANTES da Fase 3 manteve o Closed-Loop; o E2E ocular pegou que a "esfera órfã" era o spinner — não fabriquei explicação (Lei 1).
> 28	
> 29	**Sprint v6.40.0 — Vision MCP Fatia 3 remainder: PAT UI + install Claude Code + Plugin/Registry + caps de custo (2026-06-17)** — `/handson` → Sovereign puxou as 3 frentes do roadmap ("continue"). Closed-Loop: mapeei o contrato BoK vivo (FR-VM-003/011 · DD-VM-003 · OTD-VM-024/025) antes de codar. **Entregue (até o limite NÃO-gated):** **(1) PAT UI (FR-VM-003)** — `useMcpTokens` gera PAT 100% client-side (CSPRNG 32B→SHA-256, só o hash persiste byte-idêntico ao verifier; plaintext uma vez), lista/revoga RLS-own; `McpConnectorsCard` em Settings→Connectors; `.mcp.json` wired (`Bearer ${VISION_MCP_PAT}`); types regen. **Install no Claude Code provado por handshake MCP+PAT REAL pela URL pública** (`initialize`+`tools/list`7+`mesh_search` tenant-scoped); **(2) Plugin Zip + MCP Registry (FR-VM-011)** — `packages/vision-mcp-plugin/`→`public/plugins/…zip` + 3 skills PT-BR; manifesto `server.json` `com.mcorch/vision-mcp` (schema oficial 2025-12-11, remote streamable-http) + runbook (publish **gated** no DNS TXT Sovereign); **(3) OTD-VM-024** — blueprint §8-A sela motor dual (Firecrawl scrape + Gemini grounding run, fundamentado ai.google.dev) → FECHADA; **(4) caps (DD-VM-003/OTD-VM-025)** — `deepsearch.run` cap per-plano 10/25/50 + diário 25/100/500 (BYOK bypassa, fail-open em count error, throw antes do deduct); `validation_failed` ganha field+message (FRD §4.4). Anticorpo Lei 2: SOP `vision-mcp-connector-install.md`. **Prova:** pkg **55/55** · tsc 0 · smoke-vision-cost-caps **3/3 LIVE** zero-cost · origem serve plugin 200 byte-idêntico · `/security-review` independente **SAFE** · container `7710b832` · 8 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8922** · handoff `c21c53db`. **Top Gap restante (tudo gated/Sovereign-side):** OAuth browser-flow (1º tenant externo) · `mistral`/`vision.ocr` (deferidos) · publish no MCP Registry (DNS challenge) · Stripe live · domínio Resend · atribuição compra ML. **Lição:** mapear o contrato BoK vivo antes de codar mostrou que per-plan+daily caps fechavam OTD-VM-025 na mesma sessão; e provar o install pelo handshake REAL da URL pública (não loopback/browser) é o que valida "Claude Code conecta" (Lei 1).
> 30	
> 31	**Sprint v6.39.1 — Vision MCP público: mcp.mcorch.com LIVE pelo Cloudflare (OTD-VM-013 fechada) (2026-06-16)** — ativação do vhost (último item Sovereign-side da Fatia 3). Split: Sovereign cuidou do Cloudflare (A record `mcp`→137.131.243.179 proxy **laranja** + SSL **Full** + **WAF Custom Rule Skip** por host), eu do nginx/origem (vhost `sites-enabled` SSE-tuned + cert **self-signed**, CF Full aceita) + verificação. **`mcp.mcorch.com` LIVE ponta-a-ponta** — Vision MCP saiu do loopback, consumível por hosts MCP externos. **DESCOBERTA crítica (gravada na BoK + memória):** CF laranja **desafia clientes não-browser** por padrão (`cf-mitigated: challenge` "Just a moment") → browser passa o JS mas SDK/curl/Claude-connector NÃO → **WAF skip por host é OBRIGATÓRIA** pra qualquer endpoint MCP/API atrás de CF laranja. Provado material (do datacenter, pelo CF público): `/health` 200, `/mcp` sem token 401, **handshake MCP real+JWT → mesh_search tenant-scoped 200**, sem-token rejeitado. Caveat: self-signed só em Full (não strict). 3 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8921** · handoff `0632e1f8`. **OTD-VM-013 FECHADA.** **Lição:** browser ≠ cliente programático — só declarei LIVE após o handshake MCP+JWT do datacenter (não o `/health` no navegador do Sovereign), que é o que pegou o challenge bloqueando os clientes reais (Lei 1).
> 32	
> 33	**Sprint v6.39.0 — Vision MCP Fatia 3 core: PAT external auth + LGPD erasure + nginx vhost (2026-06-15)** — próximos passos, Sovereign escolheu "Fatia 3 core + vhost config" (de 4 opções). Closed-Loop: mapeei o contrato BoK (data-model §2.1/§2.3 + SDD §5.2/§5.3/§7) antes de codar. **Entregue:** (1) **PAT** (FR-VM-003) — `mcp_access_tokens` (SHA-256 + **allowlist de scopes no DB** + teto 365d + RLS own) + `auth/pat.ts` + **dispatch PAT-vs-JWT** em `verifyBearer` (JWT→ALL_SCOPES; PAT→subset) + **scope-gate por tool** (`requireScope` → 403, default-deny); (2) **erase LGPD** (FR-VM-009) — `vision_artifacts` + `erase_vision_artifacts` (cascade **re-escopo `user_id` por DELETE**, sem primitiva cross-tenant) + retention-sweep diário; (3) **nginx** `mcp.mcorch.com.conf` SSE-tuned + runbook (ativação = DNS Sovereign). **Correção apply-reality OTD-VM-026:** `storage.objects` storage-admin-owned → deleção via Storage API pelo caller (RPC retorna `storage_paths`); bucket privado + RLS bucket-scoped default-deny já isolam. `mistral_api_key`/`vision.ocr` deferidos. 3 migrations aplicadas+registradas (Management API) · `/security-review` independente **SAFE** (0≥8) · smoke **7/7** LIVE (PAT scope-gate/revoke/expiry + erase zero-residue + cross-tenant guard) · pkg **50/50** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8920** · handoff `e0695dad` · 6 commits · container `fda2784f`. OTD-VM-020 marcada **PAT-first IMPLEMENTADA**. **Top Gap novo:** ativação do vhost (DNS Cloudflare — Sovereign) · OTD-VM-024 emenda BoK do engine + per-plan `planned_units` (DD-VM-003) + cap diário per-tenant (OTD-VM-025) · resto Fatia 3 (OAuth 2.1 browser-flow + Plugin Zip + UI de emissão de PAT + `mistral_api_key`/`vision.ocr`). **Lição:** o 42501 do `DELETE storage.objects` (SECURITY DEFINER não-owner) só apareceu no smoke contra o DB servido — testar o artefato servido pegou um defeito de realidade-de-apply do stub SDD (corrigido + OTD-VM-026); o mapeamento do contrato BoK antes de codar evitou improviso (Lei 2).
> 34	
> 35	**Sprint v6.38.0 — Vision MCP `deepsearch.run`/`poll` async (FR-VM-007 · job→poll→partial-refund §4.5) (2026-06-15)** — `/handson` → Sovereign puxou o item #1 do roadmap vision-mcp. Closed-Loop: workflow de **mapeamento (5 readers)** leu contrato selado + schema vivo + wiring ANTES do código — e **pegou que minha premissa contradizia a BoK** (a SDD sela **Firecrawl**, não "google/gemini"). Surfaceei; Sovereign decidiu (custom): *"não pagar Firecrawl agora; usar chaves já disponíveis"* → motor = **Gemini Google-Search grounding** (chave `google` já provisionada; BYOK→plataforma→402), **desvio consciente OTD-VM-024** (débito de emenda BoK); contrato job/refund/state 100% fiel à BoK. **Entregue:** `deepsearch.run` (3 mco, débito-na-entrada→`job_id`→worker in-process→refund parcial §4.5 floor-a-favor-do-tenant) + `deepsearch.poll` (grátis, tenant-bound, **self-heal de órfão**); `vision_jobs` (SELECT-own RLS) + **RPC atômico `finalize_vision_job`** (service-role-only, terminal+refund 1×/job); menores (`infra_health_logs` event/metadata + OTD-VM-023 orphan-sub). **Reviews:** workflow adversarial 5-lentes (2 HIGH: charge-without-value + refund-atomicity → fechados com finalize+reconcile) + **recuperação dos 3 verify mortos por session-limit** dos transcripts (achado novo: sem teto GLOBAL da chave-plataforma → **OTD-VM-025** semáforo; bucket era só per-sub) + allowlist de telemetria (side-channel cross-tenant) + erro de provider opaco + sentinel no `source_allowlist` + URLs http(s) + CHECK `refunded_mco≤charged_mco`. `/security-review` independente **SAFE** (0≥8). pkg **46/46** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8918** · handoff `fc0b5efc` · 6 commits · container `b24360c8` smoke **10/10** LIVE. **Top Gap novo:** Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 (root Sovereign) · cap diário per-tenant + rate-limiter compartilhado (OTD-VM-014/025) · emenda BoK do engine (OTD-VM-024) · per-plan `planned_units` (DD-VM-003). **Lição:** o workflow de mapeamento pré-código pegou a contradição Firecrawl-vs-Gemini ANTES de eu codar a coisa errada (Lei 2); e recuperar findings órfãos de transcript (em vez de re-rodar) achou 1 HIGH novo de custo que o /security-review (classe DoS excluída) não pegaria.
> 36	
> 37	**Sprint v6.37.0 — Vision MCP Fatia 2: 4 Billable Tools + BYOK Foundation (+ Fatia 1 handshake/interop close) (2026-06-15)** — diretiva começou em "fechar a última ponta não-provada da Fatia 1 (mesh.search E2E com JWT)" e o Sovereign mandou seguir até a Fatia 2 inteira ("algo completo", "você escolhe a ordem"). **(1) mesh.search E2E fechado + bug crítico de Fatia 1:** o E2E com cliente MCP real pegou que o servidor reusava **um** `StreamableHTTPServerTransport` stateless (SDK proíbe reuso → `notifications/initialized` **500**, nenhum cliente completava handshake) → fix fresh-per-request; provado **7/7** + adversarial **6/6** (forja ES256 ×3 + injeção PostgREST ×7). **(2) Interop de protocolo** (achado pelo `/security-review` independente): gate aceitava só `2025-11-25`, 400-ando clientes 3rd-party → ampliado p/ `SUPPORTED_PROTOCOL_VERSIONS`; cliente cru heterogêneo **8/8** (`2025-03-26`/`2025-06-18`). **(3) Fatia 2 — fundação** (SOP Lei 2 + `infra/billing.ts` + `auth/credentials.ts` + `safety/duty-of-care.ts`: BYOK→plataforma→402 · deduct-on-entry+refund-on-failure · sentinel · duty-of-care) + **4 tools billable provados:** `vision.describe_image` (FR-VM-018, 7/7), `vision.analyze_video` (FR-VM-024 Gemini — **não Higgsfield** — cobrança/min, 7/7), `deepsearch.scrape` (FR-VM-007 Firecrawl BYOK-only, 4/4), `mesh.consolidate_reference` (FR-VM-021 escrita tenant-escopada, 5/5). **(4)** migration `firecrawl_api_key` Vault (`/security-review` limpo · aplicada+registrada) + UI Settings **deployada** + SSRF redirect-fix (achado do review). pkg **34/34** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8917** · handoff `7a45d8ef` · 7 commits. **Top Gap novo:** `deepsearch.run` async (a metade "google/gemini" — FR-VM-007 job/poll) · Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 · OTD orphan-sub. **Lição:** o `/security-review` independente pagou de novo (achou o SSRF por redirect + o defeito de interop de protocolo que o cliente do mesmo-SDK mascarava); testar contra o ARTEFATO SERVIDO pegou o bug de handshake.
> 38	
> 39	**Sprint v6.36.2 — Vision MCP: OTD Gates Closed + Fatia 1 Built & Deployed ON (2026-06-15)** — diretiva Sovereign "ambos em sequência" (gates por pesquisa → código). **(1) Gates OTD pré-GA** (workflow `wf_0040a939-232`, 3 lentes verify adversarial): **OTD-VM-004 CLOSEABLE** (grade mcoCoins 4×-floor sobrevive — custo fonteado por provider, nenhuma sub-margem; `segment` cost-aware obrigatório; SOP `vision-mcp-cost-calibration.md`); **OTD-VM-001 CLOSEABLE** (corrigiu 2 erros factuais do blueprint — UEyes/Imp1k EXISTEM, SOTA=**SUM**/MIT self-hostável não DeepGaze; recall≥0.95 fundamentado); **OTD-VM-006 CLOSEABLE** (14 licenças verdes LICENSE-fetched + 3 minas banidas; SpikingJelly não-MIT); **OTD-VM-005 PARTIAL** (SCCs-ANPD inviável; Res. 32/2026 UE adequada; Mistral=default candidato). **(2) Fatia 1 construída + DEPLOYADA ON** (`packages/vision-mcp-core/` → container `mcorch_vision_mcp` Sovereign Mesh, restart=unless-stopped, UID1001, read-only, `127.0.0.1:3200`): Streamable HTTP + ES256 JWKS fail-closed + Origin/protocol gates + sentinel + `mesh.search` tenant-safe. Provado material **contra o container**: health 200/401+WWW-Authenticate RFC9728/403/400 + row infra_health_logs + 14/14 testes. **2 bugs que só o deploy pegou:** bind `0.0.0.0` (port-map do bridge) + schema real de `infra_health_logs` (sem `metadata` — o padrão do sentinel edge falha silencioso). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8916** · handoff `98fa83d7` · 4 commits. **Top Gap novo:** mesh.search E2E com JWT (handshake MCP) · vhost nginx `mcp.mcorch.com` (OTD-VM-013, root Sovereign) · Fatia 2 (foveal billable + per-user creds) · migration `infra_health_logs ADD metadata jsonb` (telemetria rica). **Lição:** testar o ARTEFATO SERVIDO (container), não o node local — Lei 1 pegou 2 bugs + 1 schema drift que unit/local não veriam.
> 40	
> 41	**Sprint v6.36.1 — Vision MCP: BoK 9/9 + 8-Agent System + Adversarial Validation (2026-06-15)** — diretiva Sovereign (ref. sandcastles.ai): MCP Interno nativo de **percepção visual + deepsearch fundamentado** ("Essência Humana"), interno + ecossistemas externos. Closed-Loop BoK-first em 3 atos: **(1) Blueprint-semente v0.2.0** (workflow ultracode 19 agentes · 140 refs · verify adversarial — 5 pilares CV/Motion/Neuromorphic/Peripheral/**Cognitive** + vertical **Tecnologia Assistiva** beachhead demand-provado); **(2) Suíte BoK 9/9** (`/bok-scribe`) selada na malha (node `318862b7`, DERIVES_FROM mcorch-constellation, embedding 768d) — runtime container `mcorch_vision_mcp` Sovereign Mesh, **0 edge fns**; **(3) Sistema de 8 agentes BoK** (`/bok-agents-generator`) com Pantheon Reconciliation (eleva, não recria). **Validação adversarial independente (3 lentes) = SUITE VALIDATED** após pegar+corrigir **1 blocker cross-tenant real** (`erase_vision_artifacts` cascade DELETE sem re-escopar `user_id`) + hardening (scopes allowlist física, expiry CHECK, Storage policy DDL, colisão OTD-VM-020→021, FMEA-VM-004 RPN175→OTD-VM-022). Anticorpo **`deepsearch-blueprint`** (skill+agent+SOP) — padrão rodou 2× (Cyber-Sentinel+Vision MCP). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8915** · handoff `b73d141d` · README badge `6.36.0-vision-mcp`. 4 workflows mortos por cota recuperados (resumeFromRunId/main loop) — zero perda. **Top Gap novo:** Fatias MVP do vision-mcp (BoK gate ABERTO) — Fatia 1 esqueleto MCP autenticado internal · gates OTD-VM-001 (recall Tier1) / -004 (unit economics) / -005 (DPA) / -013 (nginx vhost) / -020 (OAuth AS). **Lição:** validação adversarial por agente que NÃO escreveu a suíte pega o que self-review não pega (vetor cross-tenant que minha mão + 1ª lente deixaram passar).
> 42	
> 43	**Sprint v6.36.0 — Native OpenDesign Integration + MIV Redesign Backlog (2026-06-14)** — Configuração do OpenDesign de forma nativa e inclusão da meta de redesign completo baseada no MIV (Manual de Identidade Visual) no roadmap. **(1) Nativização do OpenDesign** (`CanvasDesignPage.tsx`): o editor foi simplificado para renderizar o iframe do OpenDesign em tela cheia na rota `/dashboard/canvas/design`, removendo o controle local antigo e as abas redundantes, criando uma experiência 100% nativa. **(2) Backlog de Redesign MIV**: adicionado o OTD-MIV-REDESIGN na lista de Top Gaps e no roadmap do Canvas Studio.
> 44	
> 45	**Sprint v6.35.0 — Core-Fable: Fable 5 Flagship + Metering + Mega Brain Interstellar (2026-06-10)** — Diretiva Sovereign "Refatore todo o nosso Core-v2 para Core-Fable" em 3 arcos: **(1) Rebrand** (`914f8dd`): rota `/dashboard/core-fable` (+redirects compat), `CoreFablePage`/`components/core-fable/`, Claude Fable 5 (`anthropic/claude-fable-5` via OpenRouter, verificado live no catálogo) como default do Core; seletor de chat **desacoplado** do `pref_ai_model` (localStorage) — 1 clique não re-modela o flywheel pago. **(2) Review adversarial pré-deploy confirmou 4 P1 econômicos** (`997b307`): aios-chat OpenRouter nascia SEM metering (billing bypass na chave-plataforma) → `_shared/agent-metering.ts` compartilhado fiado nos 2 paths; `agent_pricing` sem rows novas → under-billing 133-167× via fallback flash → migration `20260610010000` seeda fable-5 1000/5000 + sonnet-4.6 300/1500 + dropa id morto; `/security-review` SAFE. Provado live: probe `{"output":"Claude"}` + ledger correto + `calc_agent_cost_mcoin`=120. **(3) Mega Brain Interstellar** (`3b15e41`→`47f9316`): loop iterativo de 8 screenshots dirigido por referência visual do Sovereign — câmera quase equatorial + 210 steps adaptativos = arco lensado contínuo sobre a sombra; **raios capturados = preto** (matou anel de névoa + bola branca do glow artificial — críticos precisam ~310 steps/órbita); disco blackbody edge-on, reação por energia (surge/spin/shimmer). tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8865** · handoff `4728b8aa`. **Top Gap novo:** OTD-FABLE-MARGIN (margem 2.0 do calc < 4×-floor p/ chat premium) · fallback `pricing_not_found` silencioso (fail-caro + telemetria). **Lição:** o screenshot-loop com sessão real no preview local (sem tocar o dist servido) pegou 2 bugs visuais que tsc/testes jamais veriam (GLSL só falha em runtime); e o review adversarial pagou de novo — 4 P1 econômicos numa feature "só de rename".
> 46	
> 47	**Sprint v6.34.0 — Cyber-Sentinel: Security BoK 4/4 + Prompt Gate Live + Infra Hardening (2026-06-10)** — diretiva CISO executada em 2 fases na mesma sessão. **(1) BoK de segurança 4/4** (`docs/bok/security/`, schema CISO 01-brd/02-srs/03-sdd/04-fmea — 12 BR-SEC + Risk Ledger · 15 FR-SEC + matriz RLS canônica + `SET LOCAL` · SDD lefthook/Arcjet/sentinel/Dockerfile UID1001/compose cap_drop integrais · FMEA 12 modos RPN AIOS). **(2) Aplicação no ecossistema vivo** (`6f2f75a`): **Sentinel LIVE** em `orchestrate-content` (prod **v52**) — `_shared/sentinel.ts` barra injeção/bypass/ANSI **depois da identidade, antes do `deduct_mco_coins`**; provado em prod com JWT real (`HTTP 403 layer=sentinel` score=3, **zero mcoCoins**). Infra recriada e endurecida: `claude_mem` uid1001+read_only+8caps (healthy), `chroma` caps conservadoras+no-new-privileges (heartbeat vivo), `gitnexus` imagem não-root buildada; env `SUPABASE_SERVICE_ROLE_KEY` revogada removida do compose (FM-04). Gate git **dual-engine** lefthook+gitleaks (pre-commit/pre-push, degrada sem gitleaks — OTD-SEC-003). **Review adversarial pegou 4 bugs reais ANTES de qualquer deploy quente**: rate-limiter falsava o fan-out paralelo de `campaign-run`; `cap_drop SETUID/SETGID` quebraria o `chroma` de terceiros; regex de 1 qualificador; guard `&&||` do gitleaks engolia a detecção. tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8862** · handoff `0a9865a9` + BoK seal `424f0fe4`. **Próximos:** FM-10 gitnexus (imagem pronta, roda stdio) · OTD-SEC-006/007 (fiar sentinel + migration `security_events`/quarentena <50ms nas demais fns pagas) · Arcjet aguarda superfície Next/BFF. **Lição:** verificar **materialmente** (dry-run dos containers, exploit real em prod) antes de declarar — pegou o `name:` que orfanaria os containers e os 4 bugs do review.
> 48	
> 49	**Sprint v6.33.1 — Hotfix Kanban ScrollArea + E2E à Prova de Cloudflare (2026-06-09)** — bug report do Sovereign no `/dashboard/kanban`: `ReferenceError: ScrollArea is not defined` ao criar coluna. **Causa:** `KanbanPage.tsx` usava `<ScrollArea>` (área scrollável de tarefas) sem importar — só quebrava *depois* da 1ª coluna (empty-state não exercita o componente). **Fix de 1 linha** (`e55ce70`): import `@/components/ui/scroll-area`; deploy material (chunk novo `KanbanPage-CW7WBYjZ.js` ≠ o do stack trace, import scroll-area + env baked); **confirmado em prod pelo print do Sovereign**. **E2E completo** via preview local do `dist` + sessão injetada (CF Turnstile barra agent-browser do datacenter até no `login.mcorch.com`): CRUD + drag-drop bidirecional **provado pelo DB** (3× PATCH 200 + SELECT, não pelo DOM). Helper `gen-user-session.ts` (`761ea6f`) p/ E2E logado à prova de CF. **Incidente de concorrência** (Sovereign mexendo em prod junto) resolvido sem perda de dado — board/coluna intactos, a "divergência" da 1ª rodada era o Sovereign movendo o mesmo card. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8860** · handoff `fd20b125`. **Lição:** E2E mutável vai em board descartável, nunca no dado real do Sovereign; DB-prod é compartilhado. **Diretiva CISO de hardening DEFERIDA** (blueprint `6b1571a` commitado; 4 artefatos BoK de segurança p/ sessão dedicada).
> 50	
> 51	**Sprint v6.33.0 — ML Attribution Fix + Browser Operator BoK (2026-06-08)** — o teste **real** do Sovereign no branded link expôs o flywheel emitindo link **MORTO**. **(1) Fix do auto-monetize** (`34d7ef0`): `_shared/affiliate.ts` `buildMlProductUrl` montava o formato BARE `mercadolivre.com.br/MLB-<id>` (404) com 2/3 ids stale → agora resolve `vm_affiliate_products.product_url` real (fonte única Apify), fail-open `/p/`; **reconcilia "ML não conta clique"** (era 404, não falha do matt_word — o painel ML já contara matt_word em produto VÁLIDO em 2026-06-04); provado E2E `7993c6a4` 302 → `/p/MLB27834876`; deploy `orchestrate-step` 122.8kB. **(2) BoK 9/9 do Operador de Browser Autenticado** (`/bok-scribe`, `24ba435`): suíte 756 LOC MR→SDD+STRIDE+FMEA; **gate pagou** — o link oficial é per-user → nova `user_affiliate_links` (não a `vm_affiliate_products.affiliate_template_url` COMPARTILHADA, que vazaria entre tenants — OTD-ABO-003); runtime residencial cravado (datacenter **403** reprovado em produto real `/p/`, bare e `/afiliados/hub`); mesh seal `31323fe3` + DERIVES_FROM edge `9ea18d26` → mercado-livre-api. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8852** · handoff `630509e2`. **Top Gap:** **BUILD do Operador** (gate ABERTO; runtime residencial = Sovereign roda `agent-browser` logado no ML) · domínio Resend · conversão ML real. **Lição:** o teste por **mão do Sovereign** (clicks 0→4) achou o link morto que meu curl-403 do datacenter mascarava; o BoK-first pegou o vazamento cross-tenant **antes** do código.
> 52	
> 53	**Sprint — Stored-XSS Hardening + Antibody (2026-06-08)** — `/security-review` (v6.28.0) havia flagado stored-XSS em `DashboardHome` (`content_library.body` cru via `dangerouslySetInnerHTML`); fechado **ponta-a-ponta** nesta sessão. Sanitização `DOMPurify.sanitize` (já shipada via Antigravity em `da9da4c`/`e5a661a`) + guarda de regressão **6 testes** (`dashboard-html-sanitize.test.ts`: preserva `<a href>` de afiliado + tags de artigo, remove `<script>`/`onerror`/`javascript:`) + **antibody ESLint `no-restricted-syntax`** (`2522e71`, sem dep nova — `eslint-plugin-react` ausente) que faz todo `dangerouslySetInnerHTML` futuro acusar no lint até ser sanitizado+justificado (sink cru plantado → **pego** material; 2 sinks legítimos justificados: DashboardHome DOMPurify · chart.tsx CSS shadcn) + limpeza dos **7 `no-explicit-any`** do data-layer de DashboardHome (`3129369`). Handoff node `e12ed58e` + obs antibody `505fb670` (embedded 768d). tsc 0 · suíte verde · mesh **8849**. **Anticorpo Permanente cumprido** — reincidência do sink barrada no lint. **Top gaps restantes (herdados de v6.28.0, gated no Sovereign):** domínio `RESEND_FROM` (entrega Resend real) · branded redirect `login.mcorch.com/go` · 2 rascunhos WP de teste · atribuição de compra ML.
> 54	
> 55	**Sprint v6.32.x — arco Core-v2 Black Hole (2026-06-07, via Antigravity)** — sessões conduzidas no Antigravity, seladas e versionadas no git, registradas aqui retroativamente a partir dos records do HANDOFF.md (não reauditadas em detalhe — Lei 1): **v6.32.6** Unified Relativistic Black Hole & Cymatics (fusão dos visualizadores num único shader WebGL Schwarzschild — raymarching + disco de acreção + Doppler beaming + ondas de cymatics; layout 30/70; `CymaticsLayer` removido; 284 testes; handoff `ec6204a4`; mesh 8847); **v6.32.5** Model Selector Fix & Reacting Black Hole (fix case-collision dos hooks `useAiosTerminalChat`/`useAiosWorkspaceChat`; persistência do modelo selecionado em `user_api_keys`; redesign MegaBrainVisualizer + CymaticsLayer; 260 testes; handoff `8627661a`; mesh 8839); **v6.32.2** Gemini 3.1 Live Mode (Live API → Gemini 3.1 Flash Live audio-only + Gemini Docs MCP + API Skills; handoff `5acba7aa`; mesh 8818). Os seals intermediários (v6.29–v6.32.4) existem em HANDOFF.md/README mas não foram back-filled aqui.
> 56	
> ```

## 🤖 Claude *(02:53:55)*


## 🤖 Claude *(02:53:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8670,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8670	          → handleMonetizeLinks(item):
> 8671	               match(ML_URL_RE) → unique URLs
> 8672	               for url of unique:
> 8673	                 POST process-affiliate-link → affiliate_url
> 8674	                 body.split(url).join(affiliate_url)
> 8675	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8676	          → Badge 💰 ML (emerald) exibido após monetização
> 8677	```
> 8678	
> 8679	---
> 8680	
> 8681	## Pending Actions (Commercial Launch)
> 8682	
> 8683	### CRITICAL — Must complete before first client
> 8684	
> 8685	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8686	
> 8687	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8688	
> 8689	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8690	
> 8691	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8692	
> 8693	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8694	
> 8695	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8696	
> 8697	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8698	
> 8699	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8700	
> 8701	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8702	
> 8703	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8704	
> 8705	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8706	
> 8707	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8708	   ```bash
> 8709	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8710	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8711	   ```
> 8712	
> 8713	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8714	
> 8715	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8716	
> 8717	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8718	
> 8719	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8720	
> 8721	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8722	
> 8723	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8724	
> 8725	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8726	
> 8727	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8728	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8729	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8730	
> 8731	### SOCIAL — Next steps
> 8732	
> 8733	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8734	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8735	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8736	
> 8737	### NON-CRITICAL
> 8738	
> 8739	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8740	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8741	- `browserslist` — ✅ updated (2026-04-26)
> 8742	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8743	
> 8744	### GITNEXUS MCP — Next steps
> 8745	
> 8746	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8747	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8748	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8749	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8750	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8751	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8752	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8753	
> 8754	### PHASE EPSILON — Next iterations
> 8755	
> 8756	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8757	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8758	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8759	
> 8760	### CORE — Next iterations
> 8761	
> 8762	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8763	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8764	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8765	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8766	
> 8767	### PHASE DELTA — Next iterations
> 8768	
> 8769	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8770	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8771	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8772	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8773	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8774	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8775	
> 8776	### USUÁRIO ZERO — Checklist de validação
> 8777	
> 8778	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8779	- ✅ Stripe sandbox secrets no vault
> 8780	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8781	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8782	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8783	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8784	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8785	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8786	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8787	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8788	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8789	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8790	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8791	
> 8792	---
> 8793	
> 8794	## Infrastructure
> 8795	
> 8796	| Service | Container | Port | Status |
> 8797	|---------|-----------|------|--------|
> 8798	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8799	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8800	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8801	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8802	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8803	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8804	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8805	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8806	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8807	
> 8808	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8809	
> 8810	```bash
> 8811	docker compose up -d
> 8812	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8813	```
> 8814	
> 8815	---
> 8816	
> 8817	## Security Model (Post-Go-Live)
> 8818	
> 8819	| Table | Isolation |
> 8820	|-------|-----------|
> 8821	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8822	| `mcorch_edges` | Same pattern |
> 8823	| `infra_health_logs` | **Admin-only read** (`has_role('admin')`, migration `20260701040000`) — was read-all-authenticated but writers leaked per-tenant `user_id`; the HUD reads via the service-role `get-infra-status` edge fn; write only service_role |
> 8824	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8825	
> 8826	---
> 8827	
> 8828	## Billing Architecture
> 8829	
> 8830	| Decision | Value |
> 8831	|----------|-------|
> 8832	| Canonical billing ledger | `profiles.mco_balance` |
> 8833	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8834	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8835	| Orchestration cost | 10 mcoCoins/run |
> 8836	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8837	| Stripe | Sandbox keys active — swap to live before first client |
> 8838	
> 8839	---
> 8840	
> 8841	## GraphRAG State
> 8842	
> 8843	- **9003 total nodes** (verificado live 2026-06-30 via REST count=exact, loop-editor-render-security-hardening seal: +handoff `d02a8570-5195-4206-a918-df3a42423aba` embedded 768d — Loop autônomo 8 iterações: FR-VS-047 editor→pipeline MCORCH [wrap `hyperframes render`, paridade provada 3 níveis + guard smoke + fix TDZ do dual-write de vídeo] + OTD-SEC-006/007 sentinel-wiring [generate-content+lead-score, injeção→403 LIVE] + FR-SEC-014 pt1 [ledger imutável `security_events`, /security-review NO FINDINGS, provado LIVE] + #2 YT/TikTok false-high corrigido; achado npm `hyperframes` license:None; 10 commits `8d59160`..`145f106`; +6 vs prev 8997 [inclui nó video-render `9069bb7d` + atividade Sovereign]; prev 8996)
> 8844	- **8996 total nodes** (verificado live 2026-06-30 via REST count=exact, avatar-fatia2-voice-fatia3a-consent-erase seal: +handoff `c138539f-0365-436a-ad56-c65e013793c6` embedded 768d + milestone Fatia 2 `b51d8de6-e574-42aa-93b7-8fd75d85a717` — Gabriel AI **Fatia 2 (Clone de Voz)** [nó voiceClone + edge `generate-voice` BYOK ElevenLabs/Cartesia fail-closed + code-switch guard FM-AC-013 + voice_profiles RLS-own Vault + RPCs tenant-guarded; migration `20260630120000`; smoke 10/10; browser+VisionQA PASS] + **Fatia 3a (Consent+Erasure LGPD Art.11/18)** [avatar_identities/avatar_consents imutável + erase_avatar_artifacts tenant-guarded + edge `avatar-consent`/`erase-avatar-artifacts` + consent gate na generate-voice + ConsentWizard/erase UI; migration `20260630130000`; smoke 11/11]; Fatia 3b GATED (ArcFace ausente → emenda BoK + biometria Sovereign); 11 commits `d6515e9`..`7913546`; `/security-review` NO FINDINGS ×2; prev 8993)
> 8845	- **8993 total nodes** (verificado live 2026-06-30 via REST count=exact, gabriel-ai-fatia1-spaces-p0-kanban-live seal: +handoff `aba1458e-2df1-4813-a71b-34360bf7417e` embedded 768d — Programa Gabriel AI [deepsearch força-total → BoK `avatar-clone-ai` 10/10 selada nó `ee81987d` GO-HYBRID + Fatia 1 BYOK hedra/cartesia/fal] + Spaces canvas Phase 0 (scaffold promovido) + Kanban painel-de-detalhe + reconciliador vivo não-destrutivo + cron */15; 6 commits `a5814d2`..`71f4c47`; prev 8992 = BoK seal `ee81987d` `documentation_suite` avatar-clone-ai DERIVES_FROM video-studio `c99b7875`)
> 8846	- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8847	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8848	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8849	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8850	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8851	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8852	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8853	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8854	- HNSW cosine index operational
> 8855	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8856	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8857	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8858	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8859	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8860	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8861	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8862	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8863	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8864	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8865	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8866	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8867	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8868	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8869	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8870	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8871	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8872	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8873	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8874	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8875	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8876	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8877	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8878	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8879	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8880	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8881	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8882	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8883	
> 8884	### Embedding Model
> 8885	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8886	Schema: `vector(768)` — HNSW cosine index.
> 8887	
> 8888	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8889	Três camadas eliminam intervenção manual:
> 8890	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8891	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8892	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8893	
> 8894	### Comandos de manutenção da Mesh
> 8895	```bash
> 8896	# Verificar nós sem embedding (deveria retornar array vazio):
> 8897	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8898	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8899	
> 8900	# Backfill manual (Bun-native — requer .env):
> 8901	bun run scripts/backfill-embeddings.ts
> 8902	
> 8903	# Backfill de código-fonte nos nós AST:
> 8904	bun run scripts/backfill-node-content.ts
> 8905	
> 8906	# Re-sync AST completo:
> 8907	cd packages/gitnexus-core && npm run sync-mesh
> 8908	
> 8909	# Acompanhar re-ingesta pós-commit:
> 8910	tail -f /tmp/mcorch-ingest.log
> 8911	```
> 8912	
> 8913	---
> 8914	
> 8915	## Video Rescue Protocol
> 8916	
> 8917	When a video generation operation (Google Veo) times out or client disconnects:
> 8918	```bash
> 8919	# Via edge function (production):
> 8920	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8921	  -H "Authorization: Bearer <user_jwt>" \
> 8922	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8923	
> 8924	# Via local script (admin/debug):
> 8925	source .env && bun run rescue.ts <operation_id> <content_id>
> 8926	```
> 8927	
> 8928	---
> 8929	
> 8930	## Architecture Pillars
> 8931	
> 8932	| Layer | Implementation |
> 8933	|-------|---------------|
> 8934	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8935	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8936	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8937	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8938	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8939	
> 8940	---
> 8941	
> 8942	## Phase Delta — Architecture
> 8943	
> 8944	```
> 8945	OrchestrationPage (full-canvas, p-0)
> 8946	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8947	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8948	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8949	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8950	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8951	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8952	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8953	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8954	
> 8955	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8956	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8957	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8958	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8959	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8960	```
> 8961	
> 8962	### Canvas State Architecture (Hybrid)
> 8963	
> 8964	```
> 8965	User interaction → ReactFlow internal state (positions, drag)
> 8966	                         ↓ (debounced 600ms)
> 8967	                   localStorage (positions persist across refresh)
> 8968	                         ↑
> 8969	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8970	     ↓ (status changes sync to ReactFlow via useEffect)
> 8971	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8972	```
> 8973	
> 8974	## Key Files
> 8975	
> 8976	| Purpose | Path |
> 8977	|---------|------|
> 8978	| Architecture rules | `CLAUDE.md` |
> 8979	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8980	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8981	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8982	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8983	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8984	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8985	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8986	| **Node types** | `src/components/orchestrator/nodes/` |
> 8987	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8988	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8989	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8990	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8991	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8992	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8993	| Billing utilities | `src/lib/billing.ts` |
> 8994	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8995	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8996	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8997	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8998	| Video rescue (local) | `rescue.ts` |
> 8999	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 9000	| Backfill script | `scripts/backfill-embeddings.ts` |
> 9001	| Deploy harness | `scripts/harness-deploy.sh` |
> 9002	
> 9003	---
> 9004	
> 9005	## First Client Onboarding Checklist
> 9006	
> 9007	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 9008	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 9009	3. ~~Activate watchdog cron~~ ✅ Done
> 9010	4. ~~Deploy rescue-video function~~ ✅ Done
> 9011	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 9012	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 9013	7. Monitor `infra_health_logs` for first 24h.
> 9014	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 9015	
> 9016	---
> 9017	
> 9018	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 9019	
> 9020	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 9021	
> 9022	| Action | Result |
> 9023	|--------|--------|
> 9024	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 9025	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 9026	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 9027	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 9028	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 9029	
> 9030	| Commit | Conteúdo |
> 9031	|--------|----------|
> 9032	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 9033	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 9034	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 9035	
> 9036	### Arquitetura Matrix Intelligence
> 9037	
> 9038	```
> 9039	ConstellationMatrix (Stabilized Engine)
> 9040	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 9041	  └── NodeDetailsPanel (Tabbed Navigation)
> 9042	        ├── Tab Meta: Neighbor exploration + Net Context
> 9043	        ├── Tab Code: Source code preview (Supabase sync)
> 9044	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 9045	
> 9046	useNodeIntelligence Hook:
> 9047	  - contentQuery: fetch nodes.content column
> 9048	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 9049	  - state: isAnalyzing, analysisResult, progress
> 9050	```
> 9051	
> 9052	---
> 9053	
> 9054	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 9055	
> 9056	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 9057	
> 9058	| Action | Result |
> 9059	|--------|--------|
> 9060	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 9061	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 9062	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 9063	
> 9064	**Output da análise (estruturado em pt-BR):**
> 9065	- Visão Geral — papel do módulo no sistema
> 9066	- Padrões Detectados — design patterns, antipatterns
> 9067	- Acoplamento & Dependências — análise In/Out-Degree
> 9068	- Recomendações — 1-3 ações priorizadas
> 9069	
> ```

## 🤖 Claude *(02:54:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  if [ \"$slug\" = \"security\" ]; then\n    required_sec=(00-[[deepsearch-blueprint|deepsearch-blueprint]] 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)\n    missing=()\n    for doc in \"${required_sec[@]}\"; do [ -f \"docs/bok/security/$doc.md\" ] || missing+=(\"$doc\"); done\n    [ ${#missing[@]} -eq 0 ] && echo \"\u2705 security \u2014 BoK complete (ciso-4-artifact)\" || echo \"\u26a0\ufe0f security \u2014 missing: ${missing[*]}\"\n    continue\n  fi\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\"); done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone; echo \"---SCRATCH---\"; ls -la scratch/ 2>/dev/null | head -20",
  "description": "Check BoK suite completeness and scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ agentic-governance — BoK complete
> ✅ agentic-workspace — BoK complete
> ✅ aios-sql-bridge — BoK complete
> ✅ authenticated-browser-operator — BoK complete
> ✅ avatar-clone-ai — BoK complete
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
> ✅ security — BoK complete (ciso-4-artifact)
> ⚠️ spaces-evolution — missing: 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> ✅ video-studio — BoK complete
> ✅ viral-autopilot — BoK complete
> ✅ viral-daily-canvas — BoK complete
> ✅ viralmind — BoK complete
> ✅ vision-mcp — BoK complete
> ---SCRATCH---
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun 30 01:44 .
> drwx------ 31 ubuntu ubuntu 4096 Jul  1 23:52 ..
> ```

## 🤖 Claude *(02:54:38)*


## 🤖 Claude *(02:54:38)*

Contexto completo coletado. Brief:

═══════════════════════════════════════════════════════════
  **HANDSON — Loop Autônomo it.5-6: Editor Público LIVE + Universe Sinapses/Fly-to (2026-07-01)**
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **Loop it.5-6** — OTD-VS-015 verificada LIVE (editor HyperFrames público SSO-gated em `video.mcorch.com`) + Universe 3.5 sinapses reais (25 vivas de `mcorch_edges`) + 3.6 click-to-select fly-to. Fase B do video-studio **COMPLETA** (render nativo license-clean FR-VS-050 + editor billável no 3210 + durabilidade Storage FR-VS-049).
  Últimos commits:
  - `e7d987d` — docs(handoff): fix path claim `src/lib/universe-layout.ts` (5c audit)
  - `067cd02` — docs(handoff): seal loop it.5-6
  - `645a16e` — feat(universe): 3.5 sinapses inter-rede reais + 3.6 fly-to

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (status vazio, diff vazio)

🏗️ **INFRA**
  mcorch_chroma: Up 2 weeks (healthy) — Chroma API v2: **OK** (heartbeat respondeu)
  mcorch_claude_mem: Up 2 weeks (healthy)
  mcorch_vision_mcp: Up 2 days (healthy)
  mega-brain-daemon/webhook/dashboard: Up 2 weeks (healthy/up)

🧠 **KNOWLEDGE MESH**
  **9018 nós** (count=exact, seal it.5-6) · 9070+ arestas (snapshot 2026-06-01 — número de edges está stale no HANDOFF)
  Handoff node do último seal: `5a67187d-3f9d-4f73-819e-01601017d698` (embedado 768d)

🔧 **TYPESCRIPT**
  Zero erros ✅ (`npx tsc --noEmit` limpo)

📚 **BoK SUITES**
  Sealed: **24/25 completas** (agentic-governance · avatar-clone-ai · video-studio · viral-autopilot · vision-mcp · post-engine · security [ciso-4] · marketing-hub · e demais)
  Incomplete: ⚠️ **`spaces-evolution`** — só existe parcial (faltam 01-mrd..08-quality-metrics). Se a sessão tocar o módulo Spaces além do scaffold Phase 0, o BoK Gate bloqueia → `/bok-scribe spaces-evolution` antes de código.
  Mesh seal nodes recentes: avatar-clone-ai → `ee81987d` · viral-autopilot → `b3398294` · vision-mcp → `318862b7` · agentic-governance → `34748570`

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional — LinkedIn auto ✅, Twitter gated (API tier), Instagram gated (App Review).
  Top gap: o motor aprende sobre placar — payoff visível gated em **re-OAuth IG insights** + postback ML real.

⚡ **PRÓXIMOS PASSOS (prioridade)**
  1. **Unified Canvas 3.7 — perf** (`OTD-UCANVAS-PERF`): query do código ~30s com 2 canvases — candidatos: Louvain em Web Worker / streaming do grafo / lazy do backdrop. É o bloqueador técnico antes da paridade.
  2. **Unified Canvas 3.8 — poda** da ownership-query morta (`OTD-SQUAD-OWNERSHIP-REVIVAL`) — rápido, destrava 3.9.
  3. **Unified Canvas 3.9 — paridade + gate E2E 1920×1080 + cutover de nav** — ⚠️ cutover requer confirmação Sovereign (3 páginas legadas matrix/memory/core-fable são backup até aqui) → depois 3.10 seal.
  4. Pós-uso real do editor pelo Sovereign: deletar wrap CLI + desinstalar `hyperframes` global (limpeza de licença).
  5. Fila Sovereign de fundo: postback ML real · re-OAuth IG insights · emenda BoK post-engine YT/TikTok (runbook `.claude/context/sovereign-queue-runbook-2026-06-30.md`).

⚠️ **ALERTAS**
  - `spaces-evolution` BoK incompleta (gate ativo se o módulo avançar).
  - `MEMORY.md` do agente estourou o limite de índice (29.6KB > 24.4KB) — só parte carrega por sessão; vale compactar entradas.
  - Edges da malha sem contagem fresca desde 2026-06-01 no HANDOFF (nós estão atualizados; arestas não re-verificadas).
  - scratch/ limpo ✅ · containers todos healthy ✅ · git limpo ✅

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

## 👤 User *(02:55:01)*

<command-message>loop</command-message>
<command-name>/loop</command-name>
<command-args>Você é o MCORCH Master Execution Agent em MALHA FECHADA AUTÔNOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md, e CONTINUE de onde a charter está. A cada iteração: (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado — BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review se houver migration → commit granular (Workflow p/ tarefas substantivas); (3) ao bater em portão Sovereign (biometria/DNS/OAuth/GO/decisão), NÃO improvise — registre na Fila de Ação Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada iteração.</command-args>

## 👤 User *(02:55:01)*

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

Você é o MCORCH Master Execution Agent em MALHA FECHADA AUTÔNOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md, e CONTINUE de onde a charter está. A cada iteração: (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado — BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review se houver migration → commit granular (Workflow p/ tarefas substantivas); (3) ao bater em portão Sovereign (biometria/DNS/OAuth/GO/decisão), NÃO improvise — registre na Fila de Ação Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada iteração.

## 👤 User *(02:55:07)*

[Request interrupted by user]

## 🤖 Claude *(22:39:23)*

No response requested.

## 👤 User *(22:40:16)*

<system-reminder>
The user named this session "[Handson] -CONTINUAR". This may indicate the session's focus or intent.
</system-reminder>

## 🤖 Claude *(23:00:17)*

No response requested.

## 👤 User *(23:00:21)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(23:00:21)*

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
    required_sec=(00-[[deepsearch-blueprint|deepsearch-blueprint]] 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)
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


## 🤖 Claude *(23:00:22)*

You're out of usage credits. Run /usage-credits to keep using Fable 5 or /model to switch models.

## 👤 User *(23:00:49)*

<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

## 👤 User *(23:00:49)*

<command-name>/model</command-name>
            <command-message>model</command-message>
            <command-args></command-args>

## 👤 User *(23:00:49)*

<local-command-stdout>Set model to [1mOpus 4.8 (1M context)[22m and saved as your default for new sessions</local-command-stdout>

## 👤 User *(23:00:51)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(23:00:51)*

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
    required_sec=(00-[[deepsearch-blueprint|deepsearch-blueprint]] 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)
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


## 🤖 Claude *(23:00:58)*


## 🤖 Claude *(23:00:59)*

Re-executando o pickup rápido para confirmar estado atual (troca de modelo não altera o repo, mas confirmo materialmente).

## 🤖 Claude *(23:01:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch --quiet 2>&1 | tail -2; echo \"---LOCAL vs ORIGIN---\"; git rev-parse --short HEAD; git rev-parse --short @{u} 2>/dev/null || echo \"no upstream\"; echo \"---STATUS---\"; git status --short; echo \"---AHEAD/BEHIND---\"; git rev-list --left-right --count @{u}...HEAD 2>/dev/null || echo \"n/a\"",
  "description": "Fetch and compare local vs origin, working tree status"
}
```

## 🤖 Claude *(23:01:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la .claude/context/autonomous-loop-charter.md 2>/dev/null && echo \"CHARTER EXISTS\" || echo \"no charter file\"",
  "description": "Check for autonomous loop charter file"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---LOCAL vs ORIGIN---
> 54c699f
> c38519a
> ---STATUS---
>  M .agents/workflows/handson.md
> ---AHEAD/BEHIND---
> 0	4
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu 55078 Jul  3 11:40 .claude/context/autonomous-loop-charter.md
> CHARTER EXISTS
> ```

## 🤖 Claude *(23:01:40)*


## 🤖 Claude *(23:01:43)*

Detectei uma **discrepância material** que preciso reconciliar antes de fechar o brief (Lei 1): o HEAD atual é `54c699f` (rebrand), mas o primeiro pre-flight desta sessão retornou um histórico totalmente diferente (`e7d987d` loop it.5-6). O estado do git mudou no meio da sessão. Vou apurar a verdade do repo agora.

## 🤖 Claude *(23:01:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== BRANCH ATUAL ===\"; git branch --show-current; echo \"=== git log HEAD -8 ===\"; git log --oneline -8; echo \"=== TODAS AS BRANCHES (recentes) ===\"; git for-each-ref --sort=-committerdate refs/heads --format='%(refname:short) %(committerdate:relative) %(objectname:short)' | head -12",
  "description": "Ground truth: current branch, HEAD history, all local branches"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === BRANCH ATUAL ===
> main
> === git log HEAD -8 ===
> 54c699f feat(brand): rebrand minimalista MCORCH — landing verdadeira em / + favicon/ícone do sigilo
> d5d6cfa chore(miv): atualiza pasta miv com o handoff de design MCORCH (2026-07-03)
> 8d907d5 feat(landing): rebrand MCORCH Landing V2 em React (preview /lp)
> 4f4b709 fix(social): badge de conexão reflete saúde real, não o relógio de 1h do access token
> c38519a docs(handoff): seal loop it.1+it.2 — anticorpo assets owner-signing + BoK Higgsfield MCP (mesh 9048)
> 19d20b5 docs(readme): v6.83.2 — loop it.1+it.2 (anticorpo assets + BoK Higgsfield MCP, mesh 9048)
> 81e6492 chore(loop): registra it.2 2026-07-03 — BoK amendment Higgsfield MCP + gate OAuth na Fila
> 34bdb64 docs(bok): amendment Higgsfield MCP connector (OAuth per-user) — fecha gate Closed-Loop 3.5
> === TODAS AS BRANCHES (recentes) ===
> main 72 minutes ago 54c699f
> claude/dreamy-blackburn-2dd6e7 5 weeks ago 7cc07ee
> claude/beautiful-dijkstra-207b09 5 weeks ago 88670b2
> claude/gallant-blackwell-594b5a 5 weeks ago 60bf7cb
> temp-local-main 5 weeks ago e330538
> claude/youthful-poincare-565e7c 5 weeks ago 4cfe96f
> claude/eager-brown-6ef0f1 5 weeks ago 02c39eb
> claude/wizardly-allen-2a03a9 5 weeks ago cf121c1
> claude/stoic-bose-9b72f5 5 weeks ago 9a0f60f
> agent/engineer/enforce-dop-standard-5s-model 5 weeks ago 7bf0617
> agent/guardian/verify-all-10-gates-from-docs 5 weeks ago 7bf0617
> agent/scientist/add-node_id-and-input_asset_id 5 weeks ago 7bf0617
> ```

## 🤖 Claude *(23:01:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== reflog -12 (o que moveu o HEAD) ===\"; git reflog -12; echo \"=== HANDOFF.md head no commit atual ===\"; git show HEAD:HANDOFF.md 2>/dev/null | sed -n '12,20p'",
  "description": "Reflog to see what moved HEAD, and current HANDOFF head"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === reflog -12 (o que moveu o HEAD) ===
> 54c699f HEAD@{0}: commit: feat(brand): rebrand minimalista MCORCH — landing verdadeira em / + favicon/ícone do sigilo
> d5d6cfa HEAD@{1}: commit: chore(miv): atualiza pasta miv com o handoff de design MCORCH (2026-07-03)
> 8d907d5 HEAD@{2}: commit: feat(landing): rebrand MCORCH Landing V2 em React (preview /lp)
> 4f4b709 HEAD@{3}: commit: fix(social): badge de conexão reflete saúde real, não o relógio de 1h do access token
> c38519a HEAD@{4}: reset: moving to HEAD
> c38519a HEAD@{5}: commit: docs(handoff): seal loop it.1+it.2 — anticorpo assets owner-signing + BoK Higgsfield MCP (mesh 9048)
> 19d20b5 HEAD@{6}: commit: docs(readme): v6.83.2 — loop it.1+it.2 (anticorpo assets + BoK Higgsfield MCP, mesh 9048)
> 81e6492 HEAD@{7}: commit: chore(loop): registra it.2 2026-07-03 — BoK amendment Higgsfield MCP + gate OAuth na Fila
> 34bdb64 HEAD@{8}: commit: docs(bok): amendment Higgsfield MCP connector (OAuth per-user) — fecha gate Closed-Loop 3.5
> c000086 HEAD@{9}: commit: chore(loop): registra it.1 2026-07-03 — anticorpo de assinatura owner-scoped shipped
> 324d9a6 HEAD@{10}: commit: docs(assets): registra o anticorpo do Fix Assets no SOP + Key Files Reference
> 44d3d3f HEAD@{11}: commit: test(assets): anticorpo re-executável de assinatura owner-scoped em bucket privado
> === HANDOFF.md head no commit atual ===
> ## Task State
> 
> | **Loop it.1 — Anticorpo de assinatura owner-scoped (Fix Assets)** | ✅ `scripts/qa/smoke-asset-owner-signing.ts` 6/6 LIVE hermético (owner-sign 200 · cross-sign BLOCKED · enumeração 0 · id-squat neutralizado · is_public=0); fecha Mandato Obstáculo→Síntese |
> | **Loop it.2 — BoK amendment Higgsfield MCP OAuth connector** | ✅ `docs/bok/spaces-evolution/13-amendment-higgsfield-mcp-connector.md` — gate Closed-Loop 3.5 fechado; contrato vivo provado (401 OAuth · 201 DCR · discovery Clerk); FR-SPACES-015..021 + OTD-SPACES-007; código gated na aprovação Sovereign |
> | **Fix Assets — mídia privada assinável só pelo dono (regressão FECHADA)** | ✅ migration `20260703030000` (3 policies owner-scoped + triggers de id anti-claim + data-repair) + normalizador durável em 13 superfícies; `/security-review` CLOSED 9/10; E2E Vision-APROVADO; 90 assets do User 0 vivos |
> | **Spaces 2d compose — drift FECHADO (OTD-SPACES-003)** | ✅ compose vivo E2E via OpenRouter Nano Banana (10 mco) + bucket privado assinado + sentinel de contrato Higgsfield |
> 
> ## Handoff Seal Record (2026-07-03) — Loop autônomo: anticorpo de assinatura owner-scoped (it.1) + BoK Higgsfield MCP (it.2)
> ```

## 🤖 Claude *(23:02:22)*


## 🤖 Claude *(23:02:25)*

Reconciliado. A discrepância se explica pelo reflog: o HEAD atual (`54c699f`, 72 min atrás) é a linha **History B** — loop it.1+it.2 de **2026-07-03** (rebrand + Higgsfield MCP BoK + anticorpo de assets). O primeiro pre-flight desta sessão leu um estado anômalo (History A / loop it.5-6 de 07-01, que **não aparece no reflog** — não é o HEAD real). A verdade material agora é `54c699f`. Vou ler a charter (fonte de verdade do loop) e o topo real do HANDOFF para refazer o brief correto.

## 🤖 Claude *(23:02:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "limit": 90
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Autonomous Loop Charter — MCORCH Malha Fechada
> 2	
> 3	> Fonte da verdade do `/loop` auto-ritmado. Lida no início de CADA iteração.
> 4	> Atualizada pelo loop ao fechar cada Fatia (marcar ✅ / mover item pra Fila Sovereign).
> 5	> Criada 2026-06-30 a partir do estado selado (handoff `c138539f`, mesh 8996).
> 6	
> 7	---
> 8	
> 9	## Identidade & Leis (não-negociável)
> 10	- Opero como **MCORCH Master Execution Agent**. Penso em inglês, reporto em **PT-BR**.
> 11	- **Protocolo de Malha Fechada:** módulo novo/feature/integração ⇒ BoK Gate (`docs/bok/<slug>/`) + Pattern Conformance Declaration ANTES de código.
> 12	- **Survival Laws:** Lei 1 prova material · Lei 2 SOP antes de código · Lei 3 poda+selo a ~95% · Lei 4 ORO declarado.
> 13	- **Reviewer = Sovereign (Gabriel).** Nada que precise do físico dele (dado/credencial/DNS/GO/decisão arquitetural) é improvisado — vai pra **Fila de Ação Sovereign**.
> 14	- **Doutrina open-source-first (Diretiva Sovereign 2026-06-30):** tudo que dá pra construir open-source/self-hosted **DENTRO do MCORCH** vira microserviço/módulo/menu/página da infra própria (não SaaS pago externo) — cada peça agrega **equity**. Default = open-source/self-hosted/BYOK-grátis; SaaS pago só com **OTD** justificando. **Custo USD real ao Sovereign = 0** é meta de projeto. Aplica direto a `OTD-AC-015` (preferir InsightFace self-host no Mesh a API paga) e ao gate do GO de gasto. (memória `feedback_opensource_first_zero_cost_equity`)
> 15	
> 16	## Ritual por iteração
> 17	1. `git fetch` + reler **Pending Actions** do `HANDOFF.md` + esta charter.
> 18	2. Escolher o item de MAIOR valor **DESBLOQUEADO** (pular Sovereign-gated; registrá-los na Fila).
> 19	3. Ciclo fechado: **BoK Gate → SOP Lei 2 → código → prova material Lei 1 (UUID/hash/curl/build/test) → `/security-review` se houver migration → commit granular.**
> 20	4. Ao bater num portão físico: registrar na **Fila de Ação Sovereign** com o destravador exato, e seguir pro próximo desbloqueado.
> 21	5. **Survival Laws self-audit** (1/2/3/4).
> 22	6. `/handoff` incremental ao fechar cada Fatia. **Selo final + PARAR** quando: janela ~95% · OU backlog desbloqueado vazio · OU GO/stop do Sovereign.
> 23	
> 24	## Padrão de execução
> 25	- Tarefa substantiva ⇒ **Workflow** (ultracode on): decompor + verificar adversarialmente antes de commitar.
> 26	- Mecânico/trivial ⇒ solo.
> 27	- Sempre Vision QA (`scripts/qa/vision-qa.ts`) em print de inspeção + criativo antes de declarar pronto.
> 28	- UI ⇒ browser-verify real (vite preview do dist + sessão injetada) antes de "pronto".
> 29	
> 30	---
> 31	
> 32	## Backlog (ordem de valor — só DESBLOQUEADOS executam)
> 33	
> 34	### ✅ Fix Assets — mídia privada assinável pelo dono em TODO o ecossistema — SHIPPED E2E (loop 2026-07-03)
> 35	- **Regressão diagnosticada (Lei 1):** os buckets de mídia são PRIVADOS (correto), mas o app resolvia URL **pública** (`/object/public/…` → 400) e o cliente não conseguia **assinar** objetos com prefixo ≠ uid (owner NULL nos uploads service-role). 84 creative_assets + 68 vm_canvas_executions + 32 graphs + 1 space com URL morta — **TODOS do User 0** (não era lixo de throwaway; hipótese do Sovereign refutada no DB).
> 36	- **Fix:** migration `20260703030000` (3 policies owner-scoped, 4 rotas `=auth.uid()`: creative_assets/spaces/vm_canvas_projects/uid-prefix + **2 triggers de id server-side INSERT+UPDATE** fechando claim/PK-swap + data-repair `is_public`) · fix bug vivo `canvas-execute:555` (`is_public:true`→false, cunhava row morta a cada exec) · lib `asset-url.ts` (`toDisplayUrl`/`useDisplayUrl` re-assina no render — cura pública-morta E assinada-expirada, sem reescrever jsonb) · `<StorageImg/Video/Audio>` fiado em **13 superfícies** (Biblioteca, 5 nós, LeftPanel, Spaces cluster+refs, 3 inspectors, VideoEditor) · `resolveAssetUrl` chaveia pelo bucket real (não pela coluna `is_public` mentirosa). SOP `docs/processes/private-bucket-asset-signing.md`.
> 37	- **Provas (Lei 1):** `/security-review` **CLOSED 9/10** (achou+fechou 1 HIGH cross-tenant que EU introduzi) · migration aplicada (3/1/0) · signing re-provado (antes FAIL→SIGNED 200) · **cross-tenant BLOCKED ao vivo** (sign/claim/PK-swap) · tsc 0 · build+deploy · **E2E local determinístico: Biblioteca 67/71 imgs+19 vídeos, Canvas 17/17+4 vídeos, 0 dead-public, Vision APROVADO ×2, confirmação ocular (90 assets)**.
> 38	- **Herança:** Spaces cluster só renderiza com nó selecionado (wiring idêntico ao Canvas, provado). content_library/affiliate = keys/external (não afetados).
> 39	- ✅ **Anticorpo re-executável SHIPPED (loop 2026-07-03 it.1, commits `44d3d3f`+`324d9a6`):** o Fix Assets tinha SOP mas não um guard automático (gap do Mandato Obstáculo→Síntese). `scripts/qa/smoke-asset-owner-signing.ts` (hermético, minta owner+attacker throwaway + objeto privado sob prefixo de projeto, owner=NULL) prova **6/6 LIVE**: S1 dono assina→HTTP 200 · S2 cross-sign BLOCKED · S3 enumeração 0 · S4/S4b id-squat de `vm_canvas_projects` neutralizado (trigger regenera id) + assinatura segue BLOCKED · S5 invariante `is_public`=0. tsc 0 · gitleaks limpo · 0 usuário órfão. SOP+Key Files atualizados. **RODAR antes de qualquer mudança em storage RLS.** Disparado por pergunta direta do Sovereign ("a correção de segurança ainda está corrigida e estamos seguros?") → verificado ao vivo + vacinado.
> 40	
> 41	
> 42	### ✅ Smart-Delete MVP — SHIPPED (loop it.1-3, 2026-07-01) — gate BoK selado `33fadb0`
> 43	- ✅ **FR-SD-001 `check-post-existence`** (commit `174d30c`): edge fn read-only, resolve id das 2 fontes, `deletable_via_api` derivado no SERVIDOR (Matriz), sinal correto por API (X data-vs-errors, YT items=[], WP/Pin 200/404, FB/IG code 100). Per-user fail-closed (501 deletáveis) / honestidade non-deletable. WP per-user PURO (o smoke pegou o probe cross-tenant do fallback global → corrigido). deno check · deployed 63.65kB · smoke **9/9** zero-cost · /security-review **NO FINDINGS**.
> 44	- ✅ **FR-SD-002 `delete-remote-post`** (commit `358d825`): destrutivo, golden-rule (zero flag do cliente), DELETE idempotente WP(force=false Trash)/X/Pinterest, nó Mesh no 1º delete, NÃO apaga local (502 mantém âncora). **Workflow adversarial 4-lentes `wf_ad2b6722` pegou HIGH false-success** (X devolve errors[] p/ 401/403/429 → reportava deleted com tweet no ar) → classificadores puros `_shared/smart-delete-classify.ts` **deno test 15/15** (inclui a regressão 403). deployed 64.57kB · smoke **8/8** zero-cost NÃO-destrutivo.
> 45	- ✅ **FR-SD-003 UI 3-ramos** (commit `edc27df`): `useSmartDelete` (hook) + `SmartDeleteDialog` (display) + `smart-delete.ts` (branchFor/labels). Fiado nos 2 call-sites do calendário. tsc 0 · eslint 0 novo · build ok · branchFor **7/7** · **browser-verified** (dist servido, sessão User 0 injetada — ramo transparência LinkedIn correto) · **Vision QA confidence high** (sem tela branca/quebra).
> 46	- 🔒 **Fila Sovereign:** E2E destrutivo REAL (deletar post vivo WP/X/Pinterest + re-verify `exists=false`) — irreversível, Owner=Sovereign, precisa post descartável real + GO. · OTD-SD-001/002 (re-OAuth FB/YT p/ delete) · OTD-SD-006 (WP force=true permanente).
> 47	
> 48	### ✅ B4 EWMA multi-ciclo no analyze — SHIPPED (loop 2026-07-02 it.4, commit `bbc7ad9`)
> 49	- FRD v0.3 "fixes embarcados" implementado: reward sobre janela dos últimos M=5 ciclos do plano, peso `0.5^idade` (anti-thrash); semântica documentada (janela lembra; plano virgem → `has_real_data=false`); auditoria `reward_vector.ewma`. Provas: deno check · deployado · **smoke 13/13** (L7: WIN 2+10·0,5=7 vence NEW=3 — single-cycle teria flipado). **Restam do arco Learning:** ~~B5 pauta de receita~~ ✅ · V4-2 experimento · coluna `reward_weights` config-as-data (NFR-VA-010).
> 50	
> 51	### ✅ Spaces Fase 1b — execução runGraph + ledger `generations` — SHIPPED LIVE (GO Sovereign 2026-07-02, apply+E2E na mesma sessão)
> 52	- **GO recebido e executado:** migration `20260702190000` aplicada via Management API (HTTP 201) + registrada no ledger (RETURNING version) + **prova material 8/8** (16 cols · 2 policies · svc-only grants, client=0 · 5 idx · trigger · RLS on · anchor). **Drift do ledger FECHADO junto:** 11 locais sem registro → 10 provadas aplicadas por sonda de assinatura DDL e registradas (146→156); `20260630140000` gate_mode deixada de fora DE PROPÓSITO (pendência legítima do GO 3b). `audit-schema-drift.sh` **exit 0 NO DRIFT**. `db push` seguro de novo.
> 53	- **Fix pós-smoke (commit `4753119`):** smoke expôs inversão de ordem de guards — dispatch do branch Spaces estava DEPOIS dos pré-checks 402 legados (payload inválido c/ saldo 0 → 402 em vez de 422/404). Corrigido: dispatch antes; teto diário extraído p/ `enforceDailyCanvasCap` compartilhado; branch Spaces faz saldo+cap próprios PÓS-validação (ordem canônica 401→422→404→402). deno check ✓ · redeploy 160.2kB.
> 54	- **Provas (Lei 1):** smoke **13/13** (T1-T8 contra prod real: atômicos begin/dup/rollback/refund-clamp + RLS + 42501) · types regen (+`generations`+2 RPCs, tsc 0) · vitest **375 passed** · **E2E browser User 0 PAGO**: space `059fe777` → nó prompt-generator via Spotlight → Estimar ("1 mco projetado, sem débito" G7) → Rodar → **`generations 7add79b2` done, mco_charged=1, saldo 4624→4623 exato, latency 2400ms, result.enhanced_prompt real** → nó mesh `5f9c870b` (`spaces-first-run-…`) → **Vision QA APROVADO high cost 0**. Space de teste deletado (cascade ok, trilha `mcoin_transactions` preservada). Canvas→conteúdo pago **FECHADO**.
> 55	- **Restam do Spaces:** Fase 2 restante (Workflow Apps · FX · multi-page · voz CLONADA [Fila: biometria] · **OTD-SPACES-003** composer provider-drift) · Fase 3 (collab).
> 56	
> 57	### ✅ Spaces Fase 2d — Designer/composer — **FUNCIONANDO E2E (OTD-SPACES-003 FECHADA, loop 2026-07-03)**
> 58	- **SOP S30-S32 ANTES:** scene_compose SYNC via generateHiggsfield legado; custo 18 PINADO (classe F1); guards prompt+≥1 imagem; cap 2 = verdade do server; `NODE_PORTS.composer` declarado (image-1/image-2/prompt, threading ordenado); picker parametrizado (designer=2, imagem=4); skip no-op.
> 59	- **ACHADO MATERIAL (E2E pago it.6):** Higgsfield rejeita `mode='compose'` — o compose LEGADO do Canvas Studio estava igualmente quebrado; slice falhava honesto com estorno integral.
> 60	- **✅ 2d-bis (2026-07-03) — provider truth por sondagem 422 zero-custo:** `soul/compose` NUNCA existiu (`mode` é literal de PATH ∈ reference|character|standard); refs exigem `custom_reference_id` cunhado async em `/v1/custom-references` (fila de MINUTOS — incompatível com a janela sync). **Fix shipado:** engine do compose = **OpenRouter Nano Banana multimodal** (caminho de refs da 2b já provado), custo re-pinado **10** (4×-floor, o 18 precificava ficção), BYOK openrouter fail-closed (C4 novo), `model_key='openrouter/scene-compose'`, AR enum do Soul corrigido (4:5/5:4 mortos). **+ Achado colateral P1 consertado:** `canvas-assets` é PRIVADO desde a criação — 3 call-sites `getPublicUrl` (legacy image/voice WAV/spaces image) + `useReferenceUpload` produziam URLs 400 mortas → server assina 7d, refs do cliente 365d (S33). **+ Anticorpo permanente:** sentinel `smoke-higgsfield-schema.ts` 7/7 pina o contrato vivo (drift = exit 1). SOP Amendment 2d-bis + OTD-SPACES-004/005/006/007.
> 61	- **Provas (Lei 1):** smoke **31/31** (C4 402 pré-débito zero-row · C3 pinado 10 com provider forjado) · sentinel 7/7 · vitest **398** · tsc 0 · deno check · deploy 167.9kB · **E2E PAGO: space `4909d024` "E2E 2d compose" (MANTIDO) → generation `cc789ada` done 12,1s → PNG 919.943B URL ASSINADA HTTP 200 → saldo 4581→4571 (10 exato) → Vision QA high custo 0**.
> 62	
> 63	### ✅ Spaces Fase 2c — voice_over (voiceover stock) — SHIPPED E2E PAGO (loop 2026-07-02 it.5, commits `694d836`+`bfd2b29`)
> 64	- **SOP S26-S29 ANTES:** motor = `tts-speak` reusado COM O JWT DO USUÁRIO (re-valida, BYOK google, devolve WAV, **não cobra** — zero double-charge sem precisar de prepaid); custo declarado **2 mco** (4×-floor); guards 422 pré-débito; WAV → bucket → `finalize(done, result.audio_url)`; falha → refund total na mesma request. Voz CLONADA (Gabriel) segue **Fila Sovereign** (biometria).
> 65	- **/security-review independente: APPROVED** (SOUND em double-charge/mint/JWT-forward/guard-order/output-parity/DoS/legacy). LOW **F1 corrigido** (provider forjado inflava a cobrança até 65 → PINADA em `CREDIT_COSTS['voice-over']`; gate A4 prova) + F2 typeof + F4 telemetria. **F3/F5 registrados como OTDs** (abaixo).
> 66	- **Provas:** smoke **27/27** (A1/A1b/A2/A3 chave fake→refund/A4 pinned) · vitest **393** (+G15) · tsc 0 · **E2E PAGO**: space `1d77b500` "E2E 2c voice" (MANTIDO) → Estimar 2 exato → Rodar → **WAV 436.410 bytes audio/wav HTTP 200 (9s de fala)** → `<audio>` player no cluster → saldo **4583→4581 (2 exato)** → Vision QA high. Custo real: 2 mco + ~US$0,005 BYOK.
> 67	- **OTD-SPACES-001 (do review, pré-existente):** `canvas-assets` é bucket público com SELECT anônimo em `storage.objects` ⇒ lista+leitura mundial de imagens/vídeos/WAVs de todos os tenants. Fix = bucket privado + signed URLs em todo o slice (imagem/vídeo/voz) OU restringir list. Não-bloqueante desta fatia; herdado do legado.
> 68	- **OTD-SPACES-002 (do review, pré-existente):** INSERT policy de `spaces` não constrange `id` do cliente (poluição de namespace de prefixo no storage; sem leitura/overwrite cross-tenant alcançável). Hardening: id server-side.
> 69	
> 70	### ✅ Spaces Fase 2b — References picker — SHIPPED (loop 2026-07-02 it.4, commit `4abddf7`)
> 71	- **SOP S23-S25 ANTES:** refs em `node.data.references` (schema 1a); upload client-side ao `canvas-assets` `<uid>/spaces-refs/` (policies existentes exigem prefixo — zero migration/zero server novo); **cap ativo 4 = verdade do server** (`generateOpenRouter` anexa slice(0,4) multimodal; divergência do BoK 8 declarada); refs nunca cobram.
> 72	- **Provas (Lei 1):** `mergeReferenceUrls` explícitas+upstream dedupe cap 4 — **G14 vitest 4 novos (388 total)** · tsc 0 · eslint limpo · **browser-verify**: upload REAL (URL do bucket com prefixo do uid = policy provada) → chip → `graph.references` persistido no DB → reload hidrata → contador honesto "1/4 ativas no run · referências não são cobradas" → **Vision QA confidence high**. Placeholder "chegam na Fase 2" morto.
> 73	
> 74	### ✅ Spaces Fase 2a-CLIENTE — vídeo E2E PAGO PROVADO (loop 2026-07-02 it.3, commits `ea5a4b9`+`54b404a`)
> 75	- **SOP S19-S22 ANTES do código:** poller 5s/12min lê a própria row e flipa o nó (runState = dispatch-completo); threading imagem→handle `first-frame` → `input_asset_url` (skip honesto sem imagem); **batch de vídeo forçado 1** (×8 acidental = 1.280 mco); custo HUD = espelho 1:1 (mirror-parity mecânico parseando o fonte do edge fn — S22/G13).
> 76	- **Código:** `video-generator` em EXECUTABLE_TYPES · payload `image_to_video` higgsfield duration 5 · ParamHUD com 5 modelos precificados inline · GenerationCluster renderiza `<video>` de `result.video_url`. vitest **384** (+9 G13) · tsc 0 · eslint limpo.
> 77	- **E2E PAGO REAL (User 0, GO precedente de vídeo):** space `51b229cf` "E2E 2a video" (MANTIDO vivo p/ o Sovereign abrir) — grafo imagem→vídeo via UI (Spotlight + params; edge injetada no graph persistido, hidratação zod ok) → **Estimar 40 exato** (10+30, G7) → Rodar → imagem done 10 mco → vídeo 202/queued, `operation_id` Higgsfield real + token hash na row → **webhook REAL finalizou `done`**: MP4 **11.292.652 bytes video/mp4 HTTP 200** em `canvas-assets/51b229cf…/3e120f3d….mp4` → **poller flipou o nó `done` na UI + `<video>` no cluster** → saldo **4623→4583 (40 exato)** · `canvas_video_spend=0` (S16 provado com webhook real) · **Vision QA no VÍDEO: APROVADO high cost 0** ("robô aspirador futurista, câmera orbital suave, íntegro"). Custo real: 40 mco + ~US$0,13 BYOK Higgsfield.
> 78	- **Gotcha de E2E anotado:** refs do agent-browser ficam stale depois de toast (clique em "Rodar" acertou "Estimar" — sempre re-snapshot antes de clicar pós-toast).
> 79	
> 80	### ✅ Spaces Fase 2a-SERVER — vídeo async no slice — SHIPPED (loop 2026-07-02 it.2, commits `9db732b`+`df41d1d`+`7b0742d`)
> 81	- **Lei 2 ANTES do código:** SOP Amendment S14-S18 + gates G8-G12 (`spaces-graph-execution.md`) — ledger-first no submit; correlação webhook por **SHA-256-only** na row (plaintext vazaria ao próprio dono via RLS SELECT-own → forjaria failure-callback p/ refund + vídeo grátis; precedente PAT vision-mcp); supressão TOTAL do deduct legado no webhook (classe OTD-VA-010); sweep S17; guards S18 preço-declarado-only.
> 82	- **Migration `20260702210000`** (webhook_token_hash + operation_id + UNIQUE parcial) aplicada+registrada+provada (new_cols=2, idx=1). **/security-review independente: NO P0/HIGH** (1 MEDIUM done-fallback no webhook + 2 LOW ordem-BYOK/status-passthrough — **TODOS corrigidos**; SOUND em mint/double-charge/cross-tenant/secret-leak/replay/SSRF-parity).
> 83	- **Código:** `canvas-execute` image_to_video no slice (422 allowlist/input/duração + BYOK fail-closed 402 pós-404 + begin output_type=video + refund total em submit-fail com redação de token) + `higgsfieldSubmit` extraído/compartilhado c/ legado · `higgsfield-webhook` branch `?spaces_token=` (falha→refund; sucesso→download/validate/upload→done+result.video_url com **retry+done-fallback claim-guarded**; replay no-op; ZERO deduct legado). deno check ✓ · deployados 163.7kB+85.37kB · types regen (tsc 0).
> 84	- **Prova (Lei 1):** smoke **22/22 ×3** contra prod (13 gates 1b + V1-V4 guards + W1-W5 ciclo webhook SIMULADO zero-Higgsfield; W5 = submit real com chave fake → 401 → refund na mesma request, G8 E2E) · vitest 375 passed · vacina de orphan (chave vault do W5 bloqueava deleteUser — limpeza da base table no finally).
> 85	- **Notas honestas:** E2E pago real (dop-lite ~30 mco + ~$0.13 BYOK Higgsfield) fica p/ 2a-cliente. INFO-3 do review (legado retorna webhook_token plaintext ao cliente — pré-existente, candidato a retrofit do design hash) + INFO-2 (canvas-assets é bucket público desde o legado) registrados como follow-ups não-bloqueantes.
> 86	
> 87	### 🗄️ Spaces Fase 1b — histórico código-completo (referência)
> 88	- **Mapeamento**: Workflow `wf_b4abf175-410` (6 readers + síntese; 24 contradições resolvidas, corte de fatia selado). **SOP Lei 2** `docs/processes/spaces-graph-execution.md` (decisões S1-S13 + gates G1-G7) ANTES do código.
> 89	- **Entregue (working tree, NÃO commitado — commit gated no apply)**: migration `20260702190000_spaces_generations_ledger.sql` (tabela `generations` stub BoK verbatim + hardening D1/D2/D3/D8 + RPCs `begin_space_generation` [ledger-first: row running + deduct MESMA tx, ON CONFLICT idempotente] / `finalize_space_generation` [claim first-finalizer-wins, refund clamped + row simétrica `spaces.node.refund`], service-role-only) · branch Spaces no `canvas-execute` (extensão aditiva `space_id`+`node_run_id`, exclusivo do caminho legado; 422 guards pré-débito; teto diário estendido p/ `spaces.node.run` via IN-list; retry provider 1×/5s; refund total em falha; `finalizeWithRetry` + done-fallback + resposta honesta `refund_pending`; observation node first-run fail-open) · client `useGenerationLedger` (runGraph camadas Kahn + BFS blocked + batch=N runs + threading S11) / `useSpaceSession` / `spaces-execution.ts` lib pura / `GenerationCluster` (lazy ≤24, cursor created_at) / botões Estimar+Rodar / serializer reseta status transitório (S9) / estimate=cobrança (G7) · `scripts/self-heal-spaces.sh` (sweep on-demand, só estorna rows SEM valor entregue).
> 90	- **Provas até aqui (Lei 1)**: deno check ✓ · vitest lib pura **14/14** · eslint 0 · **/security-review independente**: núcleo do dinheiro SOUND (zero mint/double-charge/cross-tenant/cap-bypass), 1 MEDIUM + 2 LOW + 1 INFO **TODOS corrigidos** (finalize retry + refund_pending honesto + done-fallback + sweep guard + frozen→403 genérico + dup lookup tenant-filtrado).
> ```

## 🤖 Claude *(23:02:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 80
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
> 72	Signing capability (migration 20260703030000):
> 73	  storage.objects SELECT owner-scoped, 4 rotas =auth.uid():
> 74	    creative_assets(bucket,key) [service-role-write only] · spaces.id=folder[1] · vm_canvas_projects.id=folder[1] · folder[1]=uid
> 75	  id triggers (INSERT: gen_random_uuid · UPDATE: pin OLD.id) → id não-forjável (fecha claim/PK-swap)
> 76	SOP: docs/processes/private-bucket-asset-signing.md
> 77	```
> 78	
> 79	**Survival Laws Self-audit:** Lei 1 ✅ (toda claim ancorada — policies 3/1/0, HTTP SIGNED-200/BLOCKED, prints + meus olhos; o diagnóstico refutou a hipótese do Sovereign com o DB vivo) · Lei 2 ✅ (SOP ANTES do código) · Lei 3 ✅ (janela longe de 95% no início; podas por referência) · Lei 4 ✅ (ORO declarado; **portão de DDL de prod respeitado** — não contornei o classificador, esperei o `!` do Sovereign; `/security-review` pegou meu próprio HIGH e eu fechei antes do apply-final/commit).
> 80	
> ```

## 🤖 Claude *(23:02:59)*


## 🤖 Claude *(23:03:00)*

Agora tenho a verdade material. Vou checar o conteúdo real da BoK `spaces-evolution` (módulo ativo do backlog) e confirmar a contagem da malha ao vivo antes de fechar o brief.

## 🤖 Claude *(23:03:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== docs/bok/spaces-evolution/ ===\"; ls -1 docs/bok/spaces-evolution/ 2>/dev/null; echo \"=== mesh count LIVE ===\"; source .env 2>/dev/null; curl -s -m 10 \"https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" -H \"Prefer: count=exact\" -H \"Range: 0-0\" -I 2>/dev/null | grep -i \"content-range\" || echo \"count query falhou (sem chave/rede)\"",
  "description": "List spaces-evolution BoK docs and get live mesh node count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === docs/bok/spaces-evolution/ ===
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
> === mesh count LIVE ===
> content-range: 0-999/9048
> ```

## 🤖 Claude *(23:03:22)*


## 🤖 Claude *(23:03:24)*

BoK `spaces-evolution` está na verdade **completa** (00–08 + recon 09–13) no HEAD atual — o alerta do primeiro pre-flight foi contra o estado anômalo (History A). Malha ao vivo = **9048 nós** (bate com o seal it.1+it.2). Como o HEAD atual traz código de rebrand que não existia no primeiro `tsc`, revalido o TypeScript no estado real:

## 🤖 Claude *(23:03:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -15 && echo \"=== EXIT: $? (vazio acima = 0 erros) ===\"",
  "description": "Re-verify TypeScript strict on current HEAD (rebrand code)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === EXIT: 0 (vazio acima = 0 erros) ===
> ```

## 🤖 Claude *(23:03:56)*


## 🤖 Claude *(23:04:25)*

Estado reconciliado e revalidado no HEAD real. Aqui está o brief correto — o primeiro brief desta sessão foi contra um estado de git que **não é** o HEAD atual, então este o substitui.

═══════════════════════════════════════════════════════════
  **HANDSON — Loop it.1+it.2: Anticorpo assets + BoK Higgsfield MCP (2026-07-03)**
═══════════════════════════════════════════════════════════

⚠️ **RECONCILIAÇÃO (Lei 1) — leia primeiro**
O primeiro pre-flight desta sessão leu um estado anômalo (History A / "loop it.5-6 · Universe 3.5-3.6", `e7d987d`) que **não consta no reflog nem é o HEAD**. Verdade material apurada via reflog + rev-parse + `git show HEAD:HANDOFF.md`: o HEAD real é **`54c699f`** (linha do rebrand, 72 min atrás). Aquele primeiro brief está **descartado**. Corroboração: a BoK `spaces-evolution` aparecia "incompleta" no primeiro check e no HEAD real está **completa** (00–08 + recon) — confirma que o primeiro check rodou noutro estado.

🏁 **ESTADO ATUAL**
  Fase selada (Task State): **Loop it.1 + it.2** (2026-07-03) — anticorpo re-executável de assinatura owner-scoped (`smoke-asset-owner-signing.ts` 6/6) + BoK amendment Higgsfield MCP OAuth connector (gate Closed-Loop 3.5 fechado).
  Últimos commits (HEAD → trás):
    `54c699f` — feat(brand): rebrand minimalista MCORCH — landing verdadeira em `/` + favicon
    `d5d6cfa` — chore(miv): pasta miv com handoff de design MCORCH
    `8d907d5` — feat(landing): rebrand MCORCH Landing V2 em React (preview /lp)
    `4f4b709` — fix(social): badge de conexão reflete saúde real
    `c38519a` — docs(handoff): **seal loop it.1+it.2** (mesh 9048)
  ⚠️ **Os 4 commits de rebrand (`4f4b709`→`54c699f`) estão ACIMA do último seal** — trabalho ainda **não selado** no Task State do HANDOFF.

📂 **MUDANÇAS PENDENTES**
  `M .agents/workflows/handson.md` — é o próprio arquivo do skill /handson (mesmo do snapshot de início de sessão). Não conflita; descrever apenas, não commitar.
  Local está **4 commits à frente** de `origin/main` (`c38519a`) — rebrand não foi pushed.

🏗️ **INFRA** (confirmado nesta sessão)
  mcorch_chroma: Up 2 weeks (healthy) — Chroma API v2: **OK** (heartbeat respondeu)
  mcorch_claude_mem: Up 2 weeks (healthy) · mcorch_vision_mcp: Up 2 days (healthy)
  mega-brain-daemon/webhook/dashboard: healthy/up

🧠 **KNOWLEDGE MESH**
  **9048 nós** (verificado LIVE agora via REST count=exact — bate com o seal it.1+it.2)

🔧 **TYPESCRIPT**
  Zero erros ✅ (re-rodado no HEAD real, já com o código do rebrand)

📚 **BoK SUITES**
  Sealed: **25/25 completas** — incluindo `spaces-evolution` (9/9 + recon 09-13 + amendment Higgsfield). `security` no schema CISO 4-artefato.
  Incomplete: **nenhuma** ✅ (o alerta anterior era do estado anômalo).

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional (LinkedIn auto ✅; Twitter/IG gated).
  Estado do loop: o seal it.1+it.2 **declarou o frontier desbloqueado esgotado** — todo o restante do backlog é Sovereign-gated.

⚡ **PRÓXIMOS PASSOS** (fonte: charter + Fila de Ação Sovereign)
  1. **Selar o rebrand** — os 4 commits `4f4b709`→`54c699f` (Landing V2 + swap `/` + favicon) estão sem `/handoff` no Task State e não-pushed. Item mais concreto e desbloqueado.
  2. **Higgsfield MCP OAuth E2E** — código da Fatia desbloqueado mas **gated** no físico do Sovereign (consent Clerk + `redirect_uri` canônica + GO de gasto). BoK amendment pronto (`13-amendment-...`).
  3. **Fila Sovereign** (todos gated): voz CLONADA Spaces (biometria) · Smart-Delete E2E destrutivo real (GO + post descartável) · re-OAuth IG insights · postback ML real · próximos estágios do rebrand (Three.js/GSAP app-wide).

⚠️ **ALERTAS**
  - **Estado de git mudou no meio da sessão** (History A→B). Se o Sovereign esperava continuar a linha "Universe 3.5-3.6", ela **não está no HEAD atual** — confirmar qual linha é a canônica antes de qualquer loop autônomo.
  - Rebrand não-pushed e não-selado (4 commits à frente de origin).
  - Containers healthy ✅ · scratch/ limpo ✅ · tsc 0 ✅ · BoK 25/25 ✅.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

Nota: você trocou para **Opus 4.8 (1M context)** e renomeou a sessão para "[Handson] -CONTINUAR". O `/loop` autônomo que você havia iniciado foi interrompido antes de rodar. Quer que eu (a) sele o rebrand com `/handoff` incremental, (b) retome o `/loop` de malha fechada de onde a charter está, ou (c) confirme primeiro qual linha de git é a canônica dado o salto History A→B?

## 👤 User *(23:10:39)*

estranho eu estava em uma sessão e não estou mais encontrando ela no claude --resume estava fazendo todo o redesign e rebrand que baixamos do claude deisgn para implatanar aqui no claude code. A Landing page ficou muito reduzida quero deixar igual a original com os mesmos efeitos sem mudar nada porem otimizado para abrir rapido e tambem com a explosão de loading. Ja existe essa tal explozão no hero principal do original porem ele abre junto com tudo o resto. Precisamos orquestrar todos os elementos fazendo com que eles abrem na velocidade em que os olhos humanos acompanha para ler, tornando os movimentos sutis.

## 🤖 Claude *(23:10:56)*


## 🤖 Claude *(23:10:57)*

Entendi o objetivo. Antes de mexer, preciso ver o estado real dos três artefatos: a landing atual em `/` (a "reduzida"), a Landing V2 rica (`/lp`) e o HTML original do Claude Design (pasta miv). Deixa eu mapear.

## 🤖 Claude *(23:11:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== ROTAS / e /lp no App.tsx ===\"; grep -nE 'path=\"/\"|path=\"/lp\"|Landing|lazy\\(' src/App.tsx | head -30\necho \"\"\necho \"=== commit do rebrand 54c699f \u2014 o que mudou ===\"; git show 54c699f --stat | head -40",
  "description": "Find landing routes and what the rebrand commit changed"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === ROTAS / e /lp no App.tsx ===
> 14:const Landing = lazy(() => import("./pages/Landing.tsx"));
> 15:const LandingV2 = lazy(() => import("./pages/LandingV2.tsx"));
> 16:const Auth = lazy(() => import("./pages/Auth.tsx"));
> 17:const ResetPassword = lazy(() => import("./pages/ResetPassword.tsx"));
> 18:const NotFound = lazy(() => import("./pages/NotFound.tsx"));
> 19:const DashboardHome = lazy(() => import("./pages/DashboardHome.tsx"));
> 20:const ConstellationPage = lazy(() => import("./pages/ConstellationPage.tsx"));
> 21:const VideoEditorPage = lazy(() => import("./pages/VideoEditorPage.tsx"));
> 22:const AnalyticsPage = lazy(() => import("./pages/AnalyticsPage.tsx"));
> 23:const CampaignsPage = lazy(() => import("./pages/CampaignsPage.tsx"));
> 24:const CampaignWizard = lazy(() => import("./pages/CampaignWizard.tsx"));
> 25:const CampaignDetail = lazy(() => import("./pages/CampaignDetail.tsx"));
> 26:const MarketingPage = lazy(() => import("./pages/MarketingPage.tsx"));
> 27:const AutopilotPage = lazy(() => import("./pages/AutopilotPage.tsx"));
> 28:const VideoStudioPage = lazy(() => import("./pages/VideoStudioPage.tsx"));
> 29:const SocialAccountsPage = lazy(() => import("./pages/SocialAccountsPage.tsx"));
> 30:const SocialCallback = lazy(() => import("./pages/SocialCallback.tsx"));
> 31:const ContentLibraryPage = lazy(() => import("./pages/ContentLibraryPage.tsx"));
> 32:const CalendarPage = lazy(() => import("./pages/CalendarPage.tsx"));
> 33:const BlogEditorPage = lazy(() => import("./pages/BlogEditorPage.tsx"));
> 34:const AdminPage = lazy(() => import("./pages/AdminPage.tsx"));
> 35:const OrchestrationPage = lazy(() => import("./pages/OrchestrationPage.tsx"));
> 36:const MemoryPage = lazy(() => import("./pages/MemoryPage.tsx"));
> 37:const MatrixPage = lazy(() => import("./pages/MatrixPage.tsx"));
> 38:const AffiliatesPage = lazy(() => import("./pages/AffiliatesPage.tsx"));
> 39:const AffiliateProductsPage = lazy(() => import("./pages/AffiliateProductsPage.tsx"));
> 40:const ModelArenaPage = lazy(() => import("./pages/ModelArenaPage.tsx"));
> 41:const CoreFablePage = lazy(() => import("./pages/CoreFablePage.tsx"));
> 42:const PrivacyPolicy = lazy(() => import("./pages/PrivacyPolicy.tsx"));
> 43:const TermsOfService = lazy(() => import("./pages/TermsOfService.tsx"));
> 
> === commit do rebrand 54c699f — o que mudou ===
> commit 54c699ffde926c0b370c204ac11b83d1a6c9cedd
> Author: Gabriel Zarattini <gabrielcall@gmail.com>
> Date:   Fri Jul 3 18:49:41 2026 -0300
> 
>     feat(brand): rebrand minimalista MCORCH — landing verdadeira em / + favicon/ícone do sigilo
>     
>     Diretiva Sovereign: NAO o prototipo pesado. Minimalista, legivel, honesto — o
>     produto e exclusivo e personalizado por operacao; posiciona com sobriedade, nao
>     com hype. Removidas TODAS as metricas/escassez/precos fabricados do prototipo
>     (3.4x, 68%, 17/24 vagas, cohort, uptime, +40, Signal/Harness/Sovereign R$).
>     
>     Landing (14 -> 5 secoes sobrias): hero calmo · A Orquestra (CEO/PMO/PMI, sem
>     stamps) · Para Quem (lista enxuta) · Ativar (exclusividade, sem preco de
>     prateleira) · footer (Privacidade/Termos visiveis — gate TikTok). Legibilidade:
>     lede maior, line-height 1.85, mais respiro (minimal.css).
>     
>     Marca (sigilo cyan/gold, consistente site=favicon=app-icon — gate TikTok):
>     - public/favicon.svg ANIMADO (nos orbitam o nucleo dourado + breathing).
>     - public/favicon-48.png + apple-touch-icon.png (fallback) + app-icon-1024.png
>       (1024x1024 PNG p/ app stores, <5MB) rasterizados do sigil-simple.
>     - index.html: titulo/descricao/OG da marca + <link rel=icon> + rodape MCORCH.
>     
>     / agora serve a nova landing (LandingV2); antiga preservada em /legacy (rollback).
>     Prova: tsc 0 · build ok · E2E browser / e secoes — render fiel, 0 claim fabricado
>     (grep), favicon 200, dist com icones + titulo novo.
> 
>  index.html                                      |  20 +-
>  public/app-icon-1024.png                        | Bin 0 -> 226789 bytes
>  public/apple-touch-icon.png                     | Bin 0 -> 16228 bytes
>  public/favicon-48.png                           | Bin 0 -> 2565 bytes
>  public/favicon.svg                              |  11 +
>  src/App.tsx                                     |   4 +-
>  src/components/landing-v2/LandingV2Sections.tsx | 588 ++++--------------------
>  src/pages/LandingV2.tsx                         |  60 +--
>  src/styles/mcorch/minimal.css                   |  45 ++
>  9 files changed, 163 insertions(+), 565 deletions(-)
> ```

## 🤖 Claude *(23:11:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== pasta miv (original Claude Design) ===\"; ls -la miv/ 2>/dev/null | head -30\necho \"\"\necho \"=== componentes de landing existentes ===\"; find src -iname \"*landing*\" -o -iname \"*hero*\" 2>/dev/null | grep -iE \"landing|hero\" | head -30\necho \"\"\necho \"=== dir da landing V2 (.mcorch-lp) ===\"; grep -rl \"mcorch-lp\" src --include=\"*.tsx\" --include=\"*.css\" 2>/dev/null | head",
  "description": "Find original Claude Design HTML and landing components"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === pasta miv (original Claude Design) ===
> total 12068
> drwxrwxr-x 16 gcrUX  gcrUX     4096 Jul  3 18:04 .
> drwx------ 31 ubuntu ubuntu    4096 Jul  3 18:49 ..
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 artboards
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 audit
> -rw-rw-r--  1 ubuntu ubuntu   48181 Jul  3 18:04 design-canvas.jsx
> -rw-rw-r--  1 ubuntu ubuntu      65 Jul  3 18:04 .design-canvas.state.json
> drwxrwxr-x  6 ubuntu ubuntu    4096 Jul  3 18:04 design_handoff_mcorch
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 dist
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 flagship
> -rw-rw-r--  1 ubuntu ubuntu    1607 Jul  3 18:04 HANDOFF-README.md
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 landing
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 landing-v2
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 linkedin
> -rw-rw-r--  1 ubuntu ubuntu   10964 Jul  3 18:04 MCORCH 404.html
> -rw-r--r--  1 gcrUX  gcrUX  9995334 Jul  3 17:46 MCORCH-handoff.zip
> -rw-rw-r--  1 ubuntu ubuntu   11122 Jul  3 18:04 MCORCH.html
> -rw-rw-r--  1 ubuntu ubuntu    5274 Jul  3 18:04 MCORCH Identity.html
> -rw-rw-r--  1 ubuntu ubuntu    5843 Jul  3 18:04 MCORCH Identity & Theater.html
> -rw-rw-r--  1 ubuntu ubuntu 2050254 Jul  3 18:04 MCORCH Landing.html
> -rw-rw-r--  1 ubuntu ubuntu   21944 Jul  3 18:04 MCORCH MIV.html
> -rw-rw-r--  1 ubuntu ubuntu    7763 Jul  3 18:04 MCORCH MIV II.html
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 miv
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 miv2
> drwxrwxr-x  5 ubuntu ubuntu    4096 Jul  3 18:04 miv-assets-svg
> -rw-rw-r--  1 ubuntu ubuntu   25640 Jul  3 18:04 miv.css
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 miv-sections
> -rw-rw-r--  1 ubuntu ubuntu   18561 Jul  3 18:04 particles.jsx
> drwxrwxr-x  2 ubuntu ubuntu    4096 Jul  3 18:04 screenshots
> -rw-rw-r--  1 ubuntu ubuntu   14802 Jul  3 18:04 styles.css
> 
> === componentes de landing existentes ===
> src/pages/Landing.tsx
> src/pages/LandingV2.tsx
> src/components/landing
> src/components/landing-v2
> src/styles/mcorch/landing.css
> src/components/landing/LandingConstellation.tsx
> src/components/landing/HeroSection.tsx
> src/components/landing-v2/LandingV2Sections.tsx
> src/components/blocks/hero-section.tsx
> 
> === dir da landing V2 (.mcorch-lp) ===
> src/styles/mcorch/system.css
> src/styles/mcorch/minimal.css
> src/styles/mcorch/landing.css
> src/pages/LandingV2.tsx
> ```

## 🤖 Claude *(23:11:38)*


## 🤖 Claude *(23:11:40)*

Agora o quadro está claro. O que aconteceu: o commit `54c699f` **enxugou de propósito** a Landing V2 (14 seções → 5 "sóbrias", −565 linhas) por uma diretiva anterior sua ("minimalista, sem métricas/preços fabricados"). Agora você quer o caminho inverso — a riqueza visual do original de volta, mas com carregamento orquestrado. Deixa eu ver os artefatos exatos antes de propor.

## 🤖 Claude *(23:11:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== LandingV2Sections.tsx ATUAL (gutted) \u2014 tamanho ===\"; wc -l src/components/landing-v2/LandingV2Sections.tsx\necho \"=== vers\u00e3o PR\u00c9-corte (antes de 54c699f) \u2014 tamanho ===\"; git show 54c699f^:src/components/landing-v2/LandingV2Sections.tsx 2>/dev/null | wc -l\necho \"\"\necho \"=== LandingV2.tsx atual (rota /) ===\"; sed -n '1,80p' src/pages/LandingV2.tsx",
  "description": "Compare gutted vs pre-cut LandingV2Sections, read current LandingV2 page"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === LandingV2Sections.tsx ATUAL (gutted) — tamanho ===
> 196 src/components/landing-v2/LandingV2Sections.tsx
> === versão PRÉ-corte (antes de 54c699f) — tamanho ===
> 630
> 
> === LandingV2.tsx atual (rota /) ===
> // MCORCH Landing V2 — the rebrand landing (design_handoff_mcorch, 2026-07-03).
> // Minimalist & truthful cut (Sovereign directive): sober, readable, honest —
> // exclusivity over hype. Scoped under `.mcorch-lp` so brand CSS never leaks.
> import { useEffect } from 'react';
> import { Helmet } from 'react-helmet-async';
> import '@/styles/mcorch/system.css';
> import '@/styles/mcorch/landing.css';
> import '@/styles/mcorch/minimal.css';
> import { Nav, Hero, Orchestra, Audience, Activation, LandingFooter } from '@/components/landing-v2/LandingV2Sections';
> 
> export default function LandingV2() {
>   // Sticky-nav glass past the fold (progressive enhancement — usable without it).
>   useEffect(() => {
>     const nav = document.getElementById('lp-nav');
>     if (!nav) return;
>     const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 40);
>     onScroll();
>     window.addEventListener('scroll', onScroll, { passive: true });
>     return () => window.removeEventListener('scroll', onScroll);
>   }, []);
> 
>   const jsonLd = {
>     '@context': 'https://schema.org',
>     '@type': 'Organization',
>     name: 'MCORCH',
>     alternateName: 'Magic Constellation Orchestra',
>     url: 'https://login.mcorch.com',
>     description:
>       'MCORCH ativa uma agência inteira operada por IA — um CEO, um PMO e um PMI dedicados à sua operação e integrados ao seu stack. Exclusivo e personalizado para cada operação.',
>   };
> 
>   return (
>     <>
>       <Helmet>
>         <title>MCORCH — A agência autônoma · CEO · PMO · PMI dedicados a você</title>
>         <meta
>           name="description"
>           content="Um CEO, um PMO e um PMI orquestrados por IA, dedicados à sua operação e integrados às ferramentas que você já usa. Exclusivo e personalizado para cada operação."
>         />
>         <meta property="og:title" content="MCORCH — A agência autônoma" />
>         <meta
>           property="og:description"
>           content="Um CEO, um PMO e um PMI orquestrados por IA — dedicados à sua operação, integrados ao seu stack."
>         />
>         <meta property="og:type" content="website" />
>         <link rel="canonical" href="https://login.mcorch.com" />
>         <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
>       </Helmet>
> 
>       <div className="mcorch-lp">
>         <Nav />
>         <Hero />
>         <Orchestra />
>         <Audience />
>         <Activation />
>         <LandingFooter />
>       </div>
>     </>
>   );
> }
> ```

## 🤖 Claude *(23:11:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== efeitos no HTML original (MCORCH Landing.html 2MB) \u2014 buscar explos\u00e3o/part\u00edculas/anima\u00e7\u00e3o ===\"\ngrep -oiE 'explos[a-z]*|particle[s]?|canvas|requestAnimationFrame|@keyframes [a-z-]+|IntersectionObserver|gsap|three\\.|animation:|reveal|stagger' \"miv/MCORCH Landing.html\" 2>/dev/null | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -rn | head -30",
  "description": "Inventory effects in the original Claude Design HTML"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === efeitos no HTML original (MCORCH Landing.html 2MB) — buscar explosão/partículas/animação ===
>      28 gsap
>       8 reveal
>       5 animation:
>       3 stagger
>       3 requestanimationframe
>       1 @keyframes mc-pulse
>       1 @keyframes mc-glow
>       1 @keyframes mc-drift
>       1 @keyframes mc-caret
>       1 @keyframes lp-shimmer
>       1 @keyframes lp-pulse
>       1 canvas
> ```

## 🤖 Claude *(23:12:52)*


## 🤖 Claude *(23:12:58)*

O quadro técnico está claro:

- **Original** (`miv/MCORCH Landing.html`): GSAP (28 usos) para reveals + stagger, um `<canvas>` de partículas (a "explosão"), tudo animando ao mesmo tempo no load.
- **React V2 pré-corte** (`54c699f^`, 630 linhas, 14 seções): reconstrução fiel das seções — mas os efeitos GSAP/canvas eram "próximo estágio gated" (memória confirma), então provavelmente **não** foram portados.
- **Atual em `/`** (196 linhas, 5 seções): o corte minimalista.

Então o trabalho real é: restaurar as 14 seções ricas (base = versão pré-corte) **+** portar a explosão de partículas e os reveals — mas orquestrados (stagger em ritmo de leitura, sutil) em vez de tudo de uma vez, e com carregamento otimizado.

Só há **uma decisão que é genuinamente sua** e que muda o que eu construo — o resto (base de restauração, técnica de reveal leve, coreografia da explosão) eu decido e executo:

## 🤖 Claude *(23:13:04)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "O commit anterior cortou a landing de prop\u00f3sito e removeu n\u00fameros/escassez/pre\u00e7os marcados como fabricados (3.4x, 68%, 17/24 vagas, cohort, uptime, pre\u00e7os em R$). \"Igual ao original sem mudar nada\" traz esses de volta a um site p\u00fablico. Como quer o CONTE\u00daDO?",
      "header": "Conte\u00fado",
      "multiSelect": false,
      "options": [
        {
          "label": "S\u00f3 visual + efeitos",
          "description": "Restauro TODA a riqueza visual, se\u00e7\u00f5es e anima\u00e7\u00f5es do original, mas mantenho o texto honesto atual \u2014 sem os n\u00fameros/escassez/pre\u00e7os inventados. Fidelidade de forma, sem republicar claim falso."
        },
        {
          "label": "Original 100% fiel",
          "description": "Restauro exatamente como o original, incluindo os n\u00fameros, escassez e pre\u00e7os do prot\u00f3tipo. Assumo que s\u00e3o intencionais/aspiracionais e v\u00e3o ao ar como est\u00e3o."
        },
        {
          "label": "Visual + n\u00fameros reais",
          "description": "Restauro tudo com a riqueza visual, mas voc\u00ea me passa os n\u00fameros verdadeiros (ex.: ROI, uptime, vagas) para substituir os fabricados antes de publicar."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "O commit anterior cortou a landing de propósito e removeu números/escassez/preços marcados como fabricados (3.4x, 68%, 17/24 vagas, cohort, uptime, preços em R$). "Igual ao original sem mudar nada" traz esses de volta a um site público. Como quer o CONTEÚDO?"="Só visual + efeitos". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(23:24:08)*


## 🤖 Claude *(23:24:11)*

Perfeito — **só visual + efeitos, texto honesto atual preservado** (sem números fabricados). Isso me dá a regra clara: forma do original, conteúdo honesto de agora.

Agora preciso ver o código real: a cópia honesta atual (fonte de verdade do texto), a estrutura rica pré-corte (forma a restaurar) e o mecanismo da explosão. Vou mapear a estrutura de forma barata antes de ler o que importa por inteiro.

## 🤖 Claude *(23:24:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== SE\u00c7\u00d5ES exportadas \u2014 ATUAL (honesto, 5) ===\"; grep -nE 'export function|export const|function [A-Z][a-zA-Z]+\\(' src/components/landing-v2/LandingV2Sections.tsx\necho \"\"\necho \"=== SE\u00c7\u00d5ES exportadas \u2014 PR\u00c9-CORTE (rico, 14) ===\"; git show 54c699f^:src/components/landing-v2/LandingV2Sections.tsx 2>/dev/null | grep -nE 'export function|export const|function [A-Z][a-zA-Z]+\\('\necho \"\"\necho \"=== particles.jsx \u2014 cabe\u00e7alho/mecanismo ===\"; sed -n '1,40p' miv/particles.jsx",
  "description": "Structural overview of both section files and particles mechanism"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === SEÇÕES exportadas — ATUAL (honesto, 5) ===
> 10:export const Nav = () => (
> 26:export const Hero = () => (
> 63:export const Orchestra = () => (
> 107:export const Audience = () => (
> 139:export const Activation = () => (
> 160:export const LandingFooter = () => (
> 
> === SEÇÕES exportadas — PRÉ-CORTE (rico, 14) ===
> 21:export const Nav = () => (
> 39:export const Hero = () => (
> 83:export const TrustStrip = () => (
> 94:export const ProblemSection = () => (
> 147:export const AudienceSection = () => (
> 184:export const SolutionSection = () => (
> 251:export const HowSection = () => (
> 286:export const DemoSection = () => (
> 326:export const ResultsSection = () => (
> 349:export const ChampionshipOffer = () => (
> 503:export const GuaranteeSection = () => (
> 524:export const FAQSection = () => (
> 560:export const FinalCTA = () => (
> 589:export const LandingFooter = () => (
> 
> === particles.jsx — cabeçalho/mecanismo ===
> // MCORCH — particle & wave systems
> // Pure canvas; no external libs. All systems honor density / intensity from props.
> 
> // ------------------------------------------------------------------
> // useCanvas — DPR-aware canvas hook
> // Pauses RAF when the canvas leaves the viewport (huge perf win when
> // 8-12 canvases live on one page) and when the tab is hidden.
> // ------------------------------------------------------------------
> const useCanvas = (drawFn, deps = []) => {
>   const ref = React.useRef(null);
>   const rafRef = React.useRef(0);
>   React.useEffect(() => {
>     const c = ref.current;if (!c) return;
>     const ctx = c.getContext('2d', { alpha: true, desynchronized: true });
>     let w = 0,h = 0;
>     let visible = false;
>     let running = false;
>     let t0 = performance.now();
> 
>     const dprCap = Math.min(window.devicePixelRatio || 1, 1.5); // 1.5 cap saves 30-50% paint cost vs 2
> 
>     const resize = () => {
>       const cr = c.getBoundingClientRect();
>       const parent = c.parentElement;
>       const pr = parent ? parent.getBoundingClientRect() : cr;
>       // Clamp to parent box to defuse the intrinsic-grow loop (the
>       // intrinsic `c.width` attribute is what we write to; a runaway
>       // would only happen if the canvas had no CSS-controlled size and
>       // we kept multiplying it. The clamp keeps us bounded.).
>       const nw = Math.max(1, Math.floor(Math.min(cr.width || pr.width, (pr.width || cr.width) * 1.1)));
>       const nh = Math.max(1, Math.floor(Math.min(cr.height || pr.height, (pr.height || cr.height) * 1.5)));
>       if (nw === w && nh === h) return;
>       w = nw;h = nh;
>       c.width = w * dprCap;c.height = h * dprCap;
>       // DO NOT write c.style.width/height — that pins the canvas to whatever
>       // the FIRST getBoundingClientRect returned (often before layout has
>       // settled under inline % heights), permanently locking it at 300×150
>       // or similar. Let CSS keep authority over the box size.
>       c.style.display = 'block';
>       ctx.setTransform(dprCap, 0, 0, dprCap, 0, 0);
> ```

## 🤖 Claude *(23:24:54)*


## 🤖 Claude *(23:24:58)*

Decisão de engenharia que tomo eu (alinhada ao seu "otimizado para abrir rápido"): **sem GSAP** — replico os mesmos efeitos (fade+rise, stagger, easing) com IntersectionObserver + CSS (peso ~zero) e a explosão com o `<canvas>` puro do `particles.jsx` (que já é DPR-aware e pausa fora da viewport). Fidelidade do efeito, sem o peso da lib.

Vou ler os artefatos essenciais com fidelidade total (contexto 1M permite). Primeiro despejo a versão pré-corte no scratch e puxo o mecanismo GSAP do HTML:

## 🤖 Claude *(23:25:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSP=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad\"\ngit show 54c699f^:src/components/landing-v2/LandingV2Sections.tsx > \"$SP/precut-sections.tsx\" 2>/dev/null && echo \"pr\u00e9-corte dumped: $(wc -l < \"$SP/precut-sections.tsx\") linhas\"\ngit show 54c699f^:src/pages/LandingV2.tsx > \"$SP/precut-LandingV2.tsx\" 2>/dev/null && echo \"pr\u00e9-corte page dumped: $(wc -l < \"$SP/precut-LandingV2.tsx\") linhas\"\necho \"\"\necho \"=== HTML original: contexto GSAP/canvas/explos\u00e3o (linhas ao redor) ===\"\ngrep -niE 'gsap|explos|canvas|requestAnimationFrame|stagger|@keyframes' \"miv/MCORCH Landing.html\" 2>/dev/null | grep -viE 'base64|data:' | head -50",
  "description": "Dump pre-cut sections to scratch, extract GSAP/explosion context from original HTML"
}
```

## 🤖 Claude *(23:25:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/LandingV2Sections.tsx"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (457.8KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/tool-results/b2smbaz52.txt
> 
> Preview (first 2KB):
> pré-corte dumped: 630 linhas
> pré-corte page dumped: 90 linhas
> 
> === HTML original: contexto GSAP/canvas/explosão (linhas ao redor) ===
> A8UB+P/WzfpFA1wEcCwwgYSK9hZycEqq9ExsazH5YrH3RbbbCchs4vCHnspHRDoIA2tUGF0osWKE++U04xMUqRKk+5TZtmuylPouhI33Vbpjmo1an3hkaeea/SV195q9a0Onbr8oFe/n/zsv/5n1JgJk/5khr9Y4KMAcQgOsUGICAlZITvZy1FOchZDTLHEFkcbtUl8uUsgoTwlklgSSSWTXD5SyE/+CpBSKqkVpGBpFCKtQhWmcJ2cUbgneQ9zBnUGzu9av8w9uD3p3X/v/nYQx0KMn8aYRpnaqChTBCgEU0y+Yb7kyXM+t/mYfRiTKZNJVyuPKoMSZU1Thil2K9o1Z8VK7Lb3MKbGxOgT6CzKRtPQaDQaeQ1pQE4jfCRTWA8AX4WfwlZYAfPll+TPEXFr5PmzKT5Y3F5cI7sn65d1yFiyKOkJaRuskTyQDKnZfkmHJFECHSpKfupf0sfiMYk4mqccofvU3r1Ld/ZuI/u3VjxyNRfxVq6wdavdxEKmkLold035E34fuXffPQXcZ9qjcalFHJ8LoQfNvX2un+3dFqeMST9axolPxxg1Bv03PIwObUPwINnM53X0j/rQXtXLu56uZZvuVJ1URe2dtrDluzI/6cbcmBCHm8id3hCRI0yCy3Xc0Fo31MpaVgs4A1Vn9apSVl88mq4f5G+5mgvZrWXDI8NmsvGOvS7pLKHIheFCYt0szJeX5bjO0nRdCc2mnHX2zLI8X02YEiZfEp7VZDeXODbULxOv5THa0+epLvVPFpKxJDdJSxITMn0uzoiNYy6JMZtOdG6Mage+s9iZ6/1/2BhWfzpCTxpb6aAoSGv9vsWfYK8mP2ajrlrwxtxGT7fYcc4dsRrcEDJB+r1BDvEkyBlyup23jtoRrnxl19mSla47Oqwmq4bZiKg0u1ozx6TbQdXlRgKexANHRdiItWgS9ehbDqWheEQnE5c3xmWxIuaRmotlxYCiYNlwoa0QXBARx6LOyBSF5afxzXxaPipvT1iEi3OGHI2A2tRni7LyLBffl2nO6DIN5x8uhEOhKQwLyem5dFXanPZM01N1qdyUJMUK5oPxIMAtpqfZFd5SqhM7nmPYyAObtKKnjD0CCFguw3DDeSgkcGQFfZ8wLyQR0FMdQvad0h9OuiSswQ0aLARWRqBC4M1doD0gnL4InXQqMGg3vzbWaw5L4rBiSBlfBsokUpN9FKXpotJ1SRn6VJnmLhpkJVvATd/RNtV6OCUa3g4K2v9AcGTKFjc8G9l+wTYq8n5aSgcfATPH66QSdEqJOq0kL/cWkCAYFwmMrc7z07UVFCQlAssuCtzCsf0aAhdyWLySsE5jtBgKlesgvgog0iJnHsJup0LA+aNFfF2lgzGmrIlUKg3a5EmEbnpOuj9HKqGSr5N1XF+xilS3kXHH2CegiRcCMrlnfAOYr7rVqZZARNYTmwFtmSwHsYmL9fiT/rSJE8EE/2WCmOQtd4d7SqHlzxMLefDI+IlJTwA6ub8tDLSunPTn99uC2Gg8Ryd9mmE+1A1wtO8HjwNm0u9osxMwtls1HJ6I1iYdov8f7taCSf1dfS2twaTdvj4yazApJxP+zwbd/3qyiPLxDNufZjlaCvWa4zVRGZQrPa/Glqlp4RVng26/nszLtLGDVfKU0wkJVALFMS+YtyWKK4JRN+jS5DRBb/7MyKSQb68GciAAzEvY97+1lWPrOUZn9iYj4wH2xlAhXRE2CvWFa3MVuRzdST1ZkZik/blCAbBmJ3LSLrae7/EwLmAaEc5lY9MJ9TThqNj+429RAQfkhUPBHrgbB9DPLgAGYGT0HSZAxosj4JaZHbjbcqD7HbyDbEDf83CrtalGgUuzQUfoabAhMfu
> ...
> </persisted-output>
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// MCORCH Landing V2 — minimalist & truthful cut.
> 2	// Sovereign directive (2026-07-03): NOT the heavy prototype. Minimal, readable,
> 3	// honest — no fabricated metrics, scarcity or shelf-price tiers. The product is
> 4	// exclusive and personalized per operation; it positions with quiet confidence,
> 5	// it does not hard-sell. Brand tokens: src/styles/mcorch/system.css.
> 6	import { Link } from 'react-router-dom';
> 7	import { Wordmark, SigilMark, Cta, PillarIcon, HeroBackdrop } from './Brand';
> 8	
> 9	// ---------------------------------------------------------------- NAV
> 10	export const Nav = () => (
> 11	  <header className="lp-nav" id="lp-nav">
> 12	    <a href="#top" style={{ display: 'flex', alignItems: 'center', gap: 14, textDecoration: 'none' }}>
> 13	      <SigilMark />
> 14	      <Wordmark size={13} />
> 15	    </a>
> 16	    <nav className="links">
> 17	      <a href="#orquestra">A Orquestra</a>
> 18	      <a href="#paraquem">Para Quem</a>
> 19	      <a href="#ativar">Ativar</a>
> 20	    </nav>
> 21	    <Cta href="#ativar" variant="primary">Ativar minha agência</Cta>
> 22	  </header>
> 23	);
> 24	
> 25	// ---------------------------------------------------------------- HERO
> 26	export const Hero = () => (
> 27	  <section className="lp-hero" id="top">
> 28	    <HeroBackdrop />
> 29	    <div className="lp-hero-vignette" />
> 30	    <div className="lp-hero-inner">
> 31	      <div className="lp-eyebrow" style={{ justifyContent: 'center', marginBottom: 30 }}>
> 32	        MCORCH · A agência autônoma
> 33	      </div>
> 34	
> 35	      <h1>
> 36	        <span className="word"><span>A agência</span></span>{' '}
> 37	        <span className="word"><span><em className="mc-display-i mc-cyan">inteira</em>.</span></span>
> 38	        <br />
> 39	        <span className="word"><span>Dedicada</span></span>{' '}
> 40	        <span className="word"><span>a <em className="mc-display-i mc-gold">você</em>.</span></span>
> 41	      </h1>
> 42	
> 43	      <p className="sub">
> 44	        Um CEO, um PMO e um PMI orquestrados por IA — dedicados à sua operação e integrados às
> 45	        ferramentas que você já usa. Cada orquestra é desenhada para o seu negócio. Você cria; ela
> 46	        cuida do resto.
> 47	      </p>
> 48	
> 49	      <div className="cta-row">
> 50	        <Cta href="#ativar" variant="primary">Ativar minha agência</Cta>
> 51	        <Cta href="#orquestra" variant="ghost">Conhecer a orquestra</Cta>
> 52	      </div>
> 53	    </div>
> 54	
> 55	    <div className="lp-hero-scroll-hint">
> 56	      <span>Role para a orquestra</span>
> 57	      <div className="line" />
> 58	    </div>
> 59	  </section>
> 60	);
> 61	
> 62	// ---------------------------------------------------------------- A ORQUESTRA (CEO · PMO · PMI)
> 63	export const Orchestra = () => (
> 64	  <section className="lp-section" id="orquestra">
> 65	    <span className="num">A orquestra</span>
> 66	
> 67	    <div style={{ maxWidth: 760, marginBottom: 84, marginTop: 8 }}>
> 68	      <h2 className="lp-h2">
> 69	        Três executivos.<br />
> 70	        Uma <em className="mc-display-i mc-cyan">operação</em> só.
> 71	      </h2>
> 72	      <p className="lp-lede">
> 73	        Não é mais uma ferramenta. É a operação da sua agência, conduzida por três papéis
> 74	        dedicados — e integrada ao ecossistema que você já tem.
> 75	      </p>
> 76	    </div>
> 77	
> 78	    <div className="lp-pillars">
> 79	      {[
> 80	        {
> 81	          icon: 'ceo' as const, title: 'CEO', role: 'Direção',
> 82	          body: 'Lê a operação inteira, define prioridades e protege a sua margem. Decide o rumo — e o que não vale a pena fazer.',
> 83	        },
> 84	        {
> 85	          icon: 'pmo' as const, title: 'PMO', role: 'Orquestração',
> 86	          body: 'Planeja, aloca e acompanha cada projeto. O escritório que mantém prazo, briefing e padrão de entrega no lugar.',
> 87	        },
> 88	        {
> 89	          icon: 'pmi' as const, title: 'PMI', role: 'Integração',
> 90	          body: 'Executa o dia a dia e conecta o seu stack — design, vídeo, social, tráfego, CRM. Nada solto; tudo no lugar certo.',
> 91	        },
> 92	      ].map((p, i) => (
> 93	        <div key={i} className="lp-pillar">
> 94	          <div className="pill-icon"><PillarIcon kind={p.icon} /></div>
> 95	          <h3 className="lp-h3" style={{ display: 'flex', alignItems: 'baseline', gap: 12, marginBottom: 12 }}>
> 96	            {p.title}
> 97	            <span style={{ fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '0.18em', textTransform: 'uppercase', color: 'var(--bone-3)' }}>{p.role}</span>
> 98	          </h3>
> 99	          <p style={{ fontFamily: 'var(--mono)', fontSize: 13, lineHeight: 1.8, color: 'var(--bone-2)', margin: 0 }}>{p.body}</p>
> 100	        </div>
> 101	      ))}
> 102	    </div>
> 103	  </section>
> 104	);
> 105	
> 106	// ---------------------------------------------------------------- PARA QUEM
> 107	export const Audience = () => (
> 108	  <section className="lp-section" id="paraquem" style={{ borderTop: '1px solid var(--silver-2)' }}>
> 109	    <span className="num">Para quem</span>
> 110	
> 111	    <div style={{ maxWidth: 760, marginBottom: 56, marginTop: 8 }}>
> 112	      <h2 className="lp-h2">
> 113	        Para quem vive de <em className="mc-display-i mc-cyan">entregar</em>.
> 114	      </h2>
> 115	      <p className="lp-lede">
> 116	        Se o seu trabalho é criativo e a sua rotina virou gestão, a orquestra assume a operação —
> 117	        e devolve o seu foco à criação.
> 118	      </p>
> 119	    </div>
> 120	
> 121	    <ul className="lp-audience">
> 122	      {[
> 123	        'Estúdios de design',
> 124	        'Video makers',
> 125	        'Social media',
> 126	        'Copywriters',
> 127	        'Web designers',
> 128	        'Tráfego · Google & Meta Ads',
> 129	      ].map((k) => (
> 130	        <li key={k}>
> 131	          <span className="mk">◆</span> {k}
> 132	        </li>
> 133	      ))}
> 134	    </ul>
> 135	  </section>
> 136	);
> 137	
> 138	// ---------------------------------------------------------------- ATIVAR (honest, no shelf pricing)
> 139	export const Activation = () => (
> 140	  <section className="lp-section lp-activate" id="ativar" style={{ borderTop: '1px solid var(--silver-2)', textAlign: 'center' }}>
> 141	    <div style={{ maxWidth: 760, margin: '0 auto' }}>
> 142	      <span className="num" style={{ position: 'static', display: 'block', marginBottom: 24 }}>Ativar</span>
> 143	      <h2 className="lp-h2" style={{ marginBottom: 20 }}>
> 144	        Não é um plano de<br />prateleira. É a <em className="mc-display-i mc-gold">sua</em>.
> 145	      </h2>
> 146	      <p className="lp-lede" style={{ margin: '0 auto 40px' }}>
> 147	        Cada orquestra é desenhada para a sua operação — exclusiva e personalizada. Sem tarifa de
> 148	        catálogo e sem promessa de esteira. Você ativa, nós montamos a agência à sua volta, e você
> 149	        decide o nível de autonomia — de "só sugere" a "executa e me avisa".
> 150	      </p>
> 151	      <div style={{ display: 'inline-flex', gap: 16, flexWrap: 'wrap', justifyContent: 'center' }}>
> 152	        <Cta variant="primary">Ativar minha agência</Cta>
> 153	        <Cta href="#orquestra" variant="ghost">Ver a orquestra</Cta>
> 154	      </div>
> 155	    </div>
> 156	  </section>
> 157	);
> 158	
> 159	// ---------------------------------------------------------------- FOOTER
> 160	export const LandingFooter = () => (
> 161	  <footer className="lp-footer">
> 162	    <div className="row">
> 163	      <div style={{ maxWidth: 340 }}>
> 164	        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 18 }}>
> 165	          <SigilMark size={22} />
> 166	          <Wordmark size={12} />
> 167	        </div>
> 168	        <p style={{ fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.75, color: 'var(--bone-3)', margin: 0 }}>
> 169	          A agência autônoma. Um CEO, um PMO e um PMI dedicados e integrados ao seu ecossistema.
> 170	        </p>
> 171	      </div>
> 172	
> 173	      <div className="col">
> 174	        <h5>A Orquestra</h5>
> 175	        <a href="#orquestra">CEO · PMO · PMI</a>
> 176	        <a href="#paraquem">Para Quem</a>
> 177	        <a href="#ativar">Ativar</a>
> 178	      </div>
> 179	      <div className="col">
> 180	        <h5>Conta</h5>
> 181	        <Link to="/auth">Entrar</Link>
> 182	        <Link to="/auth">Ativação</Link>
> 183	      </div>
> 184	      <div className="col">
> 185	        <h5>Legal</h5>
> 186	        <a href="mailto:contato@mcorch.com">contato@mcorch.com</a>
> 187	        <Link to="/privacy">Privacidade</Link>
> 188	        <Link to="/terms">Termos</Link>
> 189	      </div>
> 190	    </div>
> 191	    <div className="bottom">
> 192	      <span>© 2026 MCORCH · A agência autônoma</span>
> 193	      <span>Vol. I · 2026</span>
> 194	    </div>
> 195	  </footer>
> 196	);
> 197	
> ```

## 🤖 Claude *(23:25:23)*


## 🤖 Claude *(23:25:25)*

O grep do HTML retornou base64 (o arquivo é 2MB, quase tudo asset embutido). Vou filtrar por comprimento de linha para achar o script GSAP real, e ler os artefatos-chave: `Brand.tsx` (onde vive o `HeroBackdrop`), a estrutura pré-corte, `particles.jsx` e o CSS.

## 🤖 Claude *(23:25:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== GSAP orchestration no HTML (s\u00f3 linhas curtas < 200 chars, sem base64) ===\"\nawk 'length < 220' \"miv/MCORCH Landing.html\" | grep -niE 'gsap|timeline|stagger|\\.from\\(|\\.to\\(|ScrollTrigger|ease:|duration:|delay:' | head -60\necho \"\"\necho \"=== arquivos landing-v2 ===\"; ls -la src/components/landing-v2/\necho \"\"\necho \"=== CSS sizes ===\"; wc -l src/styles/mcorch/*.css",
  "description": "Extract GSAP timeline from HTML filtering base64, list landing-v2 files and CSS sizes"
}
```

## 🤖 Claude *(23:25:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/Brand.tsx"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === GSAP orchestration no HTML (só linhas curtas < 200 chars, sem base64) ===
> 138:    const dead = Array.from(document.scripts);
> 
> === arquivos landing-v2 ===
> total 24
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jul  3 18:45 .
> drwxrwxr-x 25 ubuntu ubuntu 4096 Jul  3 17:56 ..
> -rw-rw-r--  1 ubuntu ubuntu 5412 Jul  3 17:56 Brand.tsx
> -rw-rw-r--  1 ubuntu ubuntu 7982 Jul  3 18:45 LandingV2Sections.tsx
> 
> === CSS sizes ===
>   656 src/styles/mcorch/landing.css
>    45 src/styles/mcorch/minimal.css
>   450 src/styles/mcorch/system.css
>  1151 total
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// MCORCH brand primitives — ported faithfully from design_handoff_mcorch/landing-v2
> 2	// (2026-07-03). Source treated as spec (README §2-3): reconstructed as real React,
> 3	// NOT the Babel-in-browser JSX. Design tokens live in src/styles/mcorch/system.css.
> 4	import { Link } from 'react-router-dom';
> 5	import type { CSSProperties, ReactNode } from 'react';
> 6	
> 7	// The app login lives at /auth on this same host — the designer's placeholder
> 8	// `https://login.mcorch.com` CTA resolves here (DEPLOY.md §4 "CTA a resolver").
> 9	const APP_CTA = '/auth';
> 10	
> 11	export const Wordmark = ({ size = 14 }: { size?: number }) => (
> 12	  <div className="mc-wordmark" style={{ fontSize: size }}>
> 13	    M<span className="dot">·</span>C<span className="dot">·</span>O<span className="dot">·</span>R
> 14	    <span className="dot">·</span>C<span className="dot">·</span>H
> 15	  </div>
> 16	);
> 17	
> 18	export const SigilMark = ({ size = 22 }: { size?: number }) => (
> 19	  <svg width={size} height={size} viewBox="0 0 20 20" style={{ filter: 'drop-shadow(0 0 6px rgba(0,242,255,0.55))' }}>
> 20	    <circle cx="10" cy="10" r="2.6" fill="#D4AF37" />
> 21	    <circle cx="10" cy="10" r="7.6" stroke="#00F2FF" strokeWidth="0.6" fill="none" />
> 22	    <circle cx="17.6" cy="10" r="0.9" fill="#00F2FF" />
> 23	    <circle cx="2.4" cy="10" r="0.9" fill="#00F2FF" />
> 24	  </svg>
> 25	);
> 26	
> 27	type CtaProps = { children: ReactNode; variant?: 'primary' | 'ghost'; href?: string; style?: CSSProperties };
> 28	
> 29	// Anchors (#…) scroll within the page; everything else routes to the app login.
> 30	export const Cta = ({ children, variant = 'primary', href = '#planos', style }: CtaProps) => {
> 31	  const isAnchor = href.startsWith('#');
> 32	  const cls = `lp-cta lp-cta-${variant}`;
> 33	  const inner = (
> 34	    <>
> 35	      <span>{children}</span>
> 36	      <span className="arrow">→</span>
> 37	    </>
> 38	  );
> 39	  if (isAnchor) {
> 40	    return (
> 41	      <a href={href} className={cls} style={style}>
> 42	        {inner}
> 43	      </a>
> 44	    );
> 45	  }
> 46	  return (
> 47	    <Link to={APP_CTA} className={cls} style={style}>
> 48	      {inner}
> 49	    </Link>
> 50	  );
> 51	};
> 52	
> 53	export const PillarIcon = ({ kind }: { kind: 'ceo' | 'pmo' | 'pmi' }) => {
> 54	  if (kind === 'ceo')
> 55	    return (
> 56	      <svg viewBox="0 0 60 60" width="56" height="56" fill="none">
> 57	        <circle cx="30" cy="30" r="22" stroke="#00F2FF" strokeWidth="0.8" opacity="0.4" />
> 58	        <circle cx="30" cy="30" r="12" stroke="#00F2FF" strokeWidth="0.8" opacity="0.7" />
> 59	        <circle cx="30" cy="30" r="4" fill="#D4AF37" />
> 60	        <circle cx="52" cy="30" r="1.6" fill="#00F2FF" />
> 61	        <circle cx="8" cy="30" r="1.6" fill="#00F2FF" />
> 62	        <circle cx="42" cy="12" r="1.2" fill="#D4AF37" />
> 63	      </svg>
> 64	    );
> 65	  if (kind === 'pmo')
> 66	    return (
> 67	      <svg viewBox="0 0 60 60" width="56" height="56" fill="none">
> 68	        <g stroke="#00F2FF" strokeWidth="0.7" opacity="0.6">
> 69	          <line x1="10" y1="10" x2="50" y2="30" />
> 70	          <line x1="10" y1="30" x2="50" y2="10" />
> 71	          <line x1="10" y1="50" x2="50" y2="30" />
> 72	          <line x1="10" y1="30" x2="50" y2="50" />
> 73	          <line x1="10" y1="10" x2="10" y2="50" />
> 74	          <line x1="50" y1="10" x2="50" y2="50" />
> 75	        </g>
> 76	        <circle cx="10" cy="10" r="2.4" fill="#00F2FF" />
> 77	        <circle cx="50" cy="10" r="2.4" fill="#00F2FF" />
> 78	        <circle cx="10" cy="50" r="2.4" fill="#00F2FF" />
> 79	        <circle cx="50" cy="50" r="2.4" fill="#00F2FF" />
> 80	        <circle cx="10" cy="30" r="2.4" fill="#D4AF37" />
> 81	        <circle cx="50" cy="30" r="2.4" fill="#D4AF37" />
> 82	      </svg>
> 83	    );
> 84	  return (
> 85	    <svg viewBox="0 0 60 60" width="56" height="56" fill="none">
> 86	      <path d="M 8 50 L 28 14 L 38 32 L 52 10" stroke="#00F2FF" strokeWidth="1.2" fill="none" />
> 87	      <circle cx="28" cy="14" r="3" fill="#D4AF37" />
> 88	      <circle cx="52" cy="10" r="2.4" fill="#D4AF37" />
> 89	      <line x1="8" y1="50" x2="52" y2="50" stroke="#00F2FF" strokeWidth="0.5" opacity="0.4" />
> 90	      <line x1="8" y1="50" x2="8" y2="8" stroke="#00F2FF" strokeWidth="0.5" opacity="0.4" />
> 91	    </svg>
> 92	  );
> 93	};
> 94	
> 95	// On-brand animated hero backdrop — CSS/SVG approximation of the handoff's WebGL
> 96	// sound-wave field (HeroThree). Faithful port of the Three.js scene is a follow-up
> 97	// (OTD noted in HANDOFF); this keeps the hero alive and on-palette meanwhile.
> 98	export const HeroBackdrop = () => (
> 99	  <div className="lp-hero-backdrop" aria-hidden="true">
> 100	    <svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" width="100%" height="100%">
> 101	      <defs>
> 102	        <linearGradient id="mcw" x1="0" y1="0" x2="1" y2="0">
> 103	          <stop offset="0" stopColor="rgba(0,242,255,0)" />
> 104	          <stop offset="0.5" stopColor="rgba(0,242,255,0.5)" />
> 105	          <stop offset="1" stopColor="rgba(77,0,255,0)" />
> 106	        </linearGradient>
> 107	        <radialGradient id="mcglow" cx="50%" cy="46%" r="60%">
> 108	          <stop offset="0" stopColor="rgba(0,242,255,0.10)" />
> 109	          <stop offset="1" stopColor="rgba(0,0,0,0)" />
> 110	        </radialGradient>
> 111	      </defs>
> 112	      <rect width="1440" height="900" fill="url(#mcglow)" />
> 113	      {Array.from({ length: 9 }).map((_, i) => (
> 114	        <path
> 115	          key={i}
> 116	          className="lp-wave"
> 117	          style={{ animationDelay: `${i * -1.6}s`, opacity: 0.14 + i * 0.03 }}
> 118	          d={`M -100 ${330 + i * 34} C 300 ${300 + i * 20}, 560 ${470 - i * 12}, 780 ${400 + i * 8} S 1240 ${300 + i * 22}, 1560 ${380 + i * 10}`}
> 119	          fill="none"
> 120	          stroke="url(#mcw)"
> 121	          strokeWidth="1.1"
> 122	        />
> 123	      ))}
> 124	    </svg>
> 125	  </div>
> 126	);
> 127	
> ```

## 🤖 Claude *(23:26:05)*


## 🤖 Claude *(23:26:07)*

O `HeroBackdrop` atual é uma **aproximação SVG** das ondas (o próprio código admite: "Faithful port of the Three.js scene is a follow-up"). A explosão de partículas real está em `particles.jsx` e nunca foi portada — é exatamente o efeito que você quer. Vou ler o mecanismo da explosão, a estrutura rica pré-corte e o CSS de reveal existente.

## 🤖 Claude *(23:26:08)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/miv/particles.jsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// MCORCH — particle & wave systems
> 2	// Pure canvas; no external libs. All systems honor density / intensity from props.
> 3	
> 4	// ------------------------------------------------------------------
> 5	// useCanvas — DPR-aware canvas hook
> 6	// Pauses RAF when the canvas leaves the viewport (huge perf win when
> 7	// 8-12 canvases live on one page) and when the tab is hidden.
> 8	// ------------------------------------------------------------------
> 9	const useCanvas = (drawFn, deps = []) => {
> 10	  const ref = React.useRef(null);
> 11	  const rafRef = React.useRef(0);
> 12	  React.useEffect(() => {
> 13	    const c = ref.current;if (!c) return;
> 14	    const ctx = c.getContext('2d', { alpha: true, desynchronized: true });
> 15	    let w = 0,h = 0;
> 16	    let visible = false;
> 17	    let running = false;
> 18	    let t0 = performance.now();
> 19	
> 20	    const dprCap = Math.min(window.devicePixelRatio || 1, 1.5); // 1.5 cap saves 30-50% paint cost vs 2
> 21	
> 22	    const resize = () => {
> 23	      const cr = c.getBoundingClientRect();
> 24	      const parent = c.parentElement;
> 25	      const pr = parent ? parent.getBoundingClientRect() : cr;
> 26	      // Clamp to parent box to defuse the intrinsic-grow loop (the
> 27	      // intrinsic `c.width` attribute is what we write to; a runaway
> 28	      // would only happen if the canvas had no CSS-controlled size and
> 29	      // we kept multiplying it. The clamp keeps us bounded.).
> 30	      const nw = Math.max(1, Math.floor(Math.min(cr.width || pr.width, (pr.width || cr.width) * 1.1)));
> 31	      const nh = Math.max(1, Math.floor(Math.min(cr.height || pr.height, (pr.height || cr.height) * 1.5)));
> 32	      if (nw === w && nh === h) return;
> 33	      w = nw;h = nh;
> 34	      c.width = w * dprCap;c.height = h * dprCap;
> 35	      // DO NOT write c.style.width/height — that pins the canvas to whatever
> 36	      // the FIRST getBoundingClientRect returned (often before layout has
> 37	      // settled under inline % heights), permanently locking it at 300×150
> 38	      // or similar. Let CSS keep authority over the box size.
> 39	      c.style.display = 'block';
> 40	      ctx.setTransform(dprCap, 0, 0, dprCap, 0, 0);
> 41	    };
> 42	
> 43	    const ro = new ResizeObserver(resize);
> 44	    // Observe BOTH parent and canvas: parent for layout-driven growth
> 45	    // (esp. inline % heights that depend on parent dims), canvas for
> 46	    // explicit CSS size changes from React re-renders.
> 47	    ro.observe(c.parentElement || c);
> 48	    ro.observe(c);
> 49	    resize();
> 50	
> 51	    const loop = (t) => {
> 52	      if (!running) {rafRef.current = 0;return;}
> 53	      const dt = (t - t0) / 1000;t0 = t;
> 54	      drawFn(ctx, w, h, t / 1000, dt);
> 55	      rafRef.current = requestAnimationFrame(loop);
> 56	    };
> 57	
> 58	    const start = () => {
> 59	      if (running) return;
> 60	      running = true;
> 61	      t0 = performance.now();
> 62	      rafRef.current = requestAnimationFrame(loop);
> 63	    };
> 64	    const stop = () => {
> 65	      running = false;
> 66	      if (rafRef.current) cancelAnimationFrame(rafRef.current);
> 67	      rafRef.current = 0;
> 68	    };
> 69	
> 70	    // Viewport visibility — only animate while the canvas is in view.
> 71	    const io = new IntersectionObserver(
> 72	      ([entry]) => {
> 73	        visible = entry.isIntersecting;
> 74	        if (visible && !document.hidden) start();else stop();
> 75	      },
> 76	      { rootMargin: '200px 0px' } // start slightly before scroll-in for smooth entry
> 77	    );
> 78	    io.observe(c);
> 79	
> 80	    // Tab visibility — pause when user switches tabs.
> 81	    const onVis = () => {
> 82	      if (document.hidden) stop();else
> 83	      if (visible) start();
> 84	    };
> 85	    document.addEventListener('visibilitychange', onVis);
> 86	
> 87	    return () => {
> 88	      stop();
> 89	      ro.disconnect();
> 90	      io.disconnect();
> 91	      document.removeEventListener('visibilitychange', onVis);
> 92	    };
> 93	    // eslint-disable-next-line react-hooks/exhaustive-deps
> 94	  }, deps);
> 95	  return ref;
> 96	};
> 97	
> 98	// ------------------------------------------------------------------
> 99	// ConstellationCanvas — n-body star graph with light filaments
> 100	// ------------------------------------------------------------------
> 101	const ConstellationCanvas = ({
> 102	  density = 1, // multiplier on node count
> 103	  count, // explicit count override
> 104	  showFilaments = true,
> 105	  showClusters = true,
> 106	  palette = 'spectrum', // spectrum | cyan
> 107	  className,
> 108	  style,
> 109	  interactive = true,
> 110	  highlightIds = []
> 111	}) => {
> 112	  const nodesRef = React.useRef(null);
> 113	  const mouseRef = React.useRef({ x: -9999, y: -9999, active: false });
> 114	
> 115	  const ref = useCanvas((ctx, w, h, t) => {
> 116	    if (!nodesRef.current || nodesRef.current.w !== w || nodesRef.current.h !== h) {
> 117	      const targetCount = count ?? Math.floor(w * h / 9000 * density);
> 118	      const N = Math.max(40, Math.min(220, targetCount));
> 119	      const clusters = showClusters ?
> 120	      Array.from({ length: 5 }, () => ({
> 121	        x: Math.random() * w,
> 122	        y: Math.random() * h,
> 123	        r: 80 + Math.random() * 140
> 124	      })) :
> 125	      [];
> 126	      const nodes = [];
> 127	      for (let i = 0; i < N; i++) {
> 128	        let x, y;
> 129	        if (clusters.length && Math.random() < 0.7) {
> 130	          const c = clusters[Math.random() * clusters.length | 0];
> 131	          const a = Math.random() * Math.PI * 2;
> 132	          const r = Math.pow(Math.random(), 1.6) * c.r;
> 133	          x = c.x + Math.cos(a) * r;
> 134	          y = c.y + Math.sin(a) * r;
> 135	        } else {
> 136	          x = Math.random() * w;
> 137	          y = Math.random() * h;
> 138	        }
> 139	        const tier = Math.random();
> 140	        const role = tier > 0.95 ? 'gold' : tier > 0.82 ? 'nebula' : 'cyan';
> 141	        const importance = tier > 0.95 ? 3 : tier > 0.82 ? 2 : 1;
> 142	        nodes.push({
> 143	          x, y,
> 144	          vx: (Math.random() - 0.5) * 0.06,
> 145	          vy: (Math.random() - 0.5) * 0.06,
> 146	          r: 0.6 + Math.pow(Math.random(), 2) * 1.6 * importance,
> 147	          phase: Math.random() * Math.PI * 2,
> 148	          freq: 0.3 + Math.random() * 0.8,
> 149	          role,
> 150	          imp: importance,
> 151	          ox: x, oy: y
> 152	        });
> 153	      }
> 154	      nodesRef.current = { w, h, nodes };
> 155	    }
> 156	    const { nodes } = nodesRef.current;
> 157	
> 158	    ctx.clearRect(0, 0, w, h);
> 159	
> 160	    // Filaments — connect nearby nodes
> 161	    if (showFilaments) {
> 162	      const max = 95;
> 163	      for (let i = 0; i < nodes.length; i++) {
> 164	        const a = nodes[i];
> 165	        for (let j = i + 1; j < nodes.length; j++) {
> 166	          const b = nodes[j];
> 167	          const dx = a.x - b.x,dy = a.y - b.y;
> 168	          const d2 = dx * dx + dy * dy;
> 169	          if (d2 < max * max) {
> 170	            const k = 1 - Math.sqrt(d2) / max;
> 171	            const alpha = k * k * 0.25;
> 172	            ctx.strokeStyle = `rgba(0, 242, 255, ${alpha})`;
> 173	            ctx.lineWidth = 0.6;
> 174	            ctx.beginPath();
> 175	            ctx.moveTo(a.x, a.y);
> 176	            ctx.lineTo(b.x, b.y);
> 177	            ctx.stroke();
> 178	          }
> 179	        }
> 180	      }
> 181	    }
> 182	
> 183	    // Mouse-reactive ripple connections
> 184	    if (interactive && mouseRef.current.active) {
> 185	      const mx = mouseRef.current.x,my = mouseRef.current.y;
> 186	      for (const n of nodes) {
> 187	        const dx = n.x - mx,dy = n.y - my;
> 188	        const d = Math.hypot(dx, dy);
> 189	        if (d < 160) {
> 190	          const k = 1 - d / 160;
> 191	          ctx.strokeStyle = `rgba(212, 175, 55, ${k * 0.4})`;
> 192	          ctx.lineWidth = 0.6;
> 193	          ctx.beginPath();
> 194	          ctx.moveTo(mx, my);
> 195	          ctx.lineTo(n.x, n.y);
> 196	          ctx.stroke();
> 197	        }
> 198	      }
> 199	    }
> 200	
> 201	    // Nodes
> 202	    for (const n of nodes) {
> 203	      // drift
> 204	      n.x += n.vx;n.y += n.vy;
> 205	      // soft return
> 206	      n.x += (n.ox - n.x) * 0.0008;
> 207	      n.y += (n.oy - n.y) * 0.0008;
> 208	      if (n.x < -20) n.x = w + 20;
> 209	      if (n.x > w + 20) n.x = -20;
> 210	      if (n.y < -20) n.y = h + 20;
> 211	      if (n.y > h + 20) n.y = -20;
> 212	
> 213	      const twinkle = 0.6 + 0.4 * Math.sin(t * n.freq * 2 + n.phase);
> 214	      const color =
> 215	      palette === 'cyan' ? `0, 242, 255` :
> 216	      n.role === 'gold' ? `212, 175, 55` :
> 217	      n.role === 'nebula' ? `140, 90, 255` :
> 218	      `0, 242, 255`;
> 219	      // halo
> 220	      const haloR = n.r * (4 + n.imp * 1.5) * twinkle;
> 221	      const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, haloR);
> 222	      grad.addColorStop(0, `rgba(${color}, ${0.45 * twinkle})`);
> 223	      grad.addColorStop(0.4, `rgba(${color}, ${0.12 * twinkle})`);
> 224	      grad.addColorStop(1, `rgba(${color}, 0)`);
> 225	      ctx.fillStyle = grad;
> 226	      ctx.beginPath();
> 227	      ctx.arc(n.x, n.y, haloR, 0, Math.PI * 2);
> 228	      ctx.fill();
> 229	      // core
> 230	      ctx.fillStyle = `rgba(${color}, ${0.9 * twinkle})`;
> 231	      ctx.beginPath();
> 232	      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
> 233	      ctx.fill();
> 234	      // gold/nebula gets a hairline cross
> 235	      if (n.imp >= 2) {
> 236	        ctx.strokeStyle = `rgba(${color}, ${0.5 * twinkle})`;
> 237	        ctx.lineWidth = 0.5;
> 238	        const cr = n.r * 4;
> 239	        ctx.beginPath();
> 240	        ctx.moveTo(n.x - cr, n.y);ctx.lineTo(n.x + cr, n.y);
> 241	        ctx.moveTo(n.x, n.y - cr);ctx.lineTo(n.x, n.y + cr);
> 242	        ctx.stroke();
> 243	      }
> 244	    }
> 245	  }, [density, count, showFilaments, showClusters, palette, interactive]);
> 246	
> 247	  const onMove = (e) => {
> 248	    if (!interactive) return;
> 249	    const r = ref.current.getBoundingClientRect();
> 250	    mouseRef.current.x = e.clientX - r.left;
> 251	    mouseRef.current.y = e.clientY - r.top;
> 252	    mouseRef.current.active = true;
> 253	  };
> 254	  const onLeave = () => {mouseRef.current.active = false;};
> 255	
> 256	  return <canvas ref={ref} className={className} style={style} onMouseMove={onMove} onMouseLeave={onLeave} />;
> 257	};
> 258	
> 259	// ------------------------------------------------------------------
> 260	// CymaticsCanvas — layered waveforms (3 frequencies stacked)
> 261	// ------------------------------------------------------------------
> 262	const CymaticsCanvas = ({
> 263	  density = 1, // wave count multiplier (controls layer count + sample fidelity)
> 264	  intensity = 1, // amplitude multiplier
> 265	  active = true,
> 266	  className,
> 267	  style,
> 268	  variant = 'horizon' // horizon | radial | spectrum
> 269	}) => {
> 270	  const ref = useCanvas((ctx, w, h, t) => {
> 271	    ctx.clearRect(0, 0, w, h);
> 272	    if (!w || !h) return;
> 273	
> 274	    if (variant === 'radial') {
> 275	      // Radial cymatics — concentric pulse rings.
> 276	      // Base radial wash so the box never reads as a dark void between
> 277	      // pulses (was the "background not covering" complaint on splash).
> 278	      const cx = w / 2,cy = h / 2;
> 279	      const maxR = Math.hypot(w, h) * 0.6;
> 280	      const wash = ctx.createRadialGradient(cx, cy, 0, cx, cy, maxR);
> 281	      wash.addColorStop(0, 'rgba(0, 242, 255, 0.10)');
> 282	      wash.addColorStop(0.6, 'rgba(0, 242, 255, 0.025)');
> 283	      wash.addColorStop(1, 'rgba(0, 0, 0, 0)');
> 284	      ctx.fillStyle = wash;
> 285	      ctx.fillRect(0, 0, w, h);
> 286	
> 287	      const layers = Math.max(3, Math.floor(6 * density));
> 288	      for (let i = 0; i < layers; i++) {
> 289	        const phase = (t * 0.6 + i * 0.45) % 2.4;
> 290	        // Pulse out to corner (hypot/2 instead of min/2) so rings actually
> 291	        // fill a non-square box AND reach the corners on square ones.
> 292	        const r = phase * Math.hypot(w, h) * 0.5;
> 293	        const alpha = Math.max(0, 1 - phase / 2.4) * 0.55 * intensity;
> 294	        ctx.strokeStyle = `rgba(0, 242, 255, ${alpha})`;
> 295	        ctx.lineWidth = 1.2;
> 296	        ctx.beginPath();
> 297	        ctx.arc(cx, cy, r, 0, Math.PI * 2);
> 298	        ctx.stroke();
> 299	      }
> 300	      return;
> 301	    }
> 302	
> 303	    if (variant === 'spectrum') {
> 304	      // Vertical bars — spectrogram
> 305	      const bars = Math.floor(80 * density);
> 306	      const bw = w / bars;
> 307	      for (let i = 0; i < bars; i++) {
> 308	        const f = i / bars;
> 309	        const v = (
> 310	        0.5 + 0.5 * Math.sin(t * 1.4 + f * 12) * (
> 311	        0.6 + 0.4 * Math.sin(t * 3.1 + f * 30))) *
> 312	        intensity;
> 313	        const bh = v * h * 0.8;
> 314	        const grad = ctx.createLinearGradient(0, h - bh, 0, h);
> 315	        grad.addColorStop(0, 'rgba(0, 242, 255, 0.0)');
> 316	        grad.addColorStop(0.4, 'rgba(0, 242, 255, 0.5)');
> 317	        grad.addColorStop(1, 'rgba(0, 242, 255, 0.9)');
> 318	        ctx.fillStyle = grad;
> 319	        ctx.fillRect(i * bw + bw * 0.15, h - bh, bw * 0.7, bh);
> 320	      }
> 321	      return;
> 322	    }
> 323	
> 324	    // Horizon — layered waveforms (default for the Vibrational Horizon)
> 325	    const layers = [
> 326	    { freq: 0.6, amp: 0.30, color: `rgba(0, 242, 255, ${0.85 * (active ? 1 : 0.3)})`, sw: 1.6, phaseSpeed: 0.9 },
> 327	    { freq: 1.4, amp: 0.18, color: `rgba(0, 242, 255, 0.45)`, sw: 1.0, phaseSpeed: 1.4 },
> 328	    { freq: 2.6, amp: 0.10, color: `rgba(140, 90, 255, 0.55)`, sw: 0.8, phaseSpeed: 2.1 },
> 329	    { freq: 5.1, amp: 0.06, color: `rgba(212, 175, 55, 0.40)`, sw: 0.6, phaseSpeed: 3.2 },
> 330	    { freq: 9.0, amp: 0.03, color: `rgba(255, 255, 255, 0.30)`, sw: 0.5, phaseSpeed: 5.0 }];
> 331	
> 332	    const layerCount = Math.max(2, Math.min(layers.length, Math.round(layers.length * density)));
> 333	    const cy = h * 0.55;
> 334	
> 335	    // Filled base layer for body
> 336	    ctx.save();
> 337	    const grad = ctx.createLinearGradient(0, 0, 0, h);
> 338	    grad.addColorStop(0, 'rgba(0, 242, 255, 0)');
> 339	    grad.addColorStop(1, 'rgba(0, 242, 255, 0.10)');
> 340	    ctx.fillStyle = grad;
> 341	    ctx.beginPath();
> 342	    ctx.moveTo(0, h);
> 343	    const samples = Math.max(120, Math.floor(w / 3));
> 344	    for (let i = 0; i <= samples; i++) {
> 345	      const x = i / samples * w;
> 346	      let y = cy;
> 347	      for (let l = 0; l < layerCount; l++) {
> 348	        const L = layers[l];
> 349	        y += Math.sin(x / w * Math.PI * 2 * L.freq + t * L.phaseSpeed) * h * L.amp * intensity;
> 350	      }
> 351	      ctx.lineTo(x, y);
> 352	    }
> 353	    ctx.lineTo(w, h);ctx.lineTo(0, h);
> 354	    ctx.closePath();
> 355	    ctx.fill();
> 356	    ctx.restore();
> 357	
> 358	    // Stroke each layer separately
> 359	    for (let l = 0; l < layerCount; l++) {
> 360	      const L = layers[l];
> 361	      ctx.strokeStyle = L.color;
> 362	      ctx.lineWidth = L.sw;
> 363	      ctx.beginPath();
> 364	      for (let i = 0; i <= samples; i++) {
> 365	        const x = i / samples * w;
> 366	        let y = cy;
> 367	        for (let k = 0; k <= l; k++) {
> 368	          const K = layers[k];
> 369	          y += Math.sin(x / w * Math.PI * 2 * K.freq + t * K.phaseSpeed) * h * K.amp * intensity;
> 370	        }
> 371	        if (i === 0) ctx.moveTo(x, y);else ctx.lineTo(x, y);
> 372	      }
> 373	      ctx.stroke();
> 374	    }
> 375	
> 376	    // Vertical scan markers
> 377	    ctx.strokeStyle = 'rgba(0, 242, 255, 0.10)';
> 378	    ctx.lineWidth = 1;
> 379	    const markers = 8;
> 380	    for (let i = 0; i < markers; i++) {
> 381	      const phase = (t * 0.2 + i / markers) % 1;
> 382	      const x = phase * w;
> 383	      ctx.beginPath();
> 384	      ctx.moveTo(x, 0);
> 385	      ctx.lineTo(x, h);
> 386	      ctx.stroke();
> 387	    }
> 388	  }, [density, intensity, active, variant]);
> 389	
> 390	  return <canvas ref={ref} className={className} style={style} />;
> 391	};
> 392	
> 393	// ------------------------------------------------------------------
> 394	// AgentCloud — particle-cloud avatar with distinct shape language
> 395	// ------------------------------------------------------------------
> 396	const AgentCloud = ({
> 397	  archetype = 'architect', // architect | coder | guardian
> 398	  size = 180,
> 399	  className,
> 400	  style
> 401	}) => {
> 402	  const seedsRef = React.useRef(null);
> 403	  const ref = useCanvas((ctx, w, h, t) => {
> 404	    if (!seedsRef.current) {
> 405	      const N = 220;
> 406	      const seeds = [];
> 407	      for (let i = 0; i < N; i++) {
> 408	        seeds.push({
> 409	          a: Math.random() * Math.PI * 2,
> 410	          r: Math.random(),
> 411	          o: Math.random() * Math.PI * 2,
> 412	          s: 0.4 + Math.random() * 1.6
> 413	        });
> 414	      }
> 415	      seedsRef.current = seeds;
> 416	    }
> 417	    const seeds = seedsRef.current;
> 418	    ctx.clearRect(0, 0, w, h);
> 419	    const cx = w / 2,cy = h / 2;
> 420	    const R = Math.min(w, h) * 0.42;
> 421	
> 422	    for (let i = 0; i < seeds.length; i++) {
> 423	      const s = seeds[i];
> 424	      let x, y, color, sz;
> 425	      const tt = t + s.o;
> 426	
> 427	      if (archetype === 'architect') {
> 428	        // Crystalline lattice — particles snap to a hex grid that slowly rotates
> 429	        const ring = Math.floor(s.r * 5);
> 430	        const slot = Math.floor(s.a / (Math.PI * 2) * (6 + ring * 6));
> 431	        const angle = slot / (6 + ring * 6) * Math.PI * 2 + t * 0.15;
> 432	        const rad = ring / 5 * R + Math.sin(tt * 0.8) * 1.5;
> 433	        x = cx + Math.cos(angle) * rad;
> 434	        y = cy + Math.sin(angle) * rad;
> 435	        color = ring >= 4 ? '212, 175, 55' : '0, 242, 255';
> 436	        sz = (ring === 0 ? 2.2 : 1.0) * s.s;
> 437	      } else if (archetype === 'coder') {
> 438	        // Code rivers — particles stream in vertical filaments, recycle top→bottom
> 439	        const cols = 14;
> 440	        const col = Math.floor(s.a / (Math.PI * 2) * cols);
> 441	        const colX = col / cols * w + (s.r * 0.4 + 0.3) * (w / cols);
> 442	        const speed = 0.4 + s.s * 0.3;
> 443	        const yPhase = (t * speed * 60 + s.o * 100) % h;
> 444	        x = colX;
> 445	        y = yPhase;
> 446	        const dx = x - cx,dy = y - cy;
> 447	        const inField = Math.hypot(dx, dy) < R * 1.2;
> 448	        if (!inField) continue;
> 449	        color = Math.floor(s.o * 7) % 9 === 0 ? '140, 90, 255' : '0, 242, 255';
> 450	        sz = 0.6 * s.s;
> 451	      } else {
> 452	        // guardian — orbital shield — concentric counter-rotating rings + a denser core
> 453	        const ring = Math.floor(s.r * 3);
> 454	        const dir = ring % 2 === 0 ? 1 : -1;
> 455	        const angle = s.a + t * (0.25 + ring * 0.15) * dir;
> 456	        const rad = (ring + 1) / 3 * R + Math.sin(tt * 1.2) * 2;
> 457	        x = cx + Math.cos(angle) * rad;
> 458	        y = cy + Math.sin(angle) * rad;
> 459	        color = ring === 2 ? '212, 175, 55' : ring === 0 ? '140, 90, 255' : '0, 242, 255';
> 460	        sz = (ring === 0 ? 1.6 : 1.0) * s.s;
> 461	      }
> 462	
> 463	      const tw = 0.55 + 0.45 * Math.sin(tt * 2);
> 464	      const grad = ctx.createRadialGradient(x, y, 0, x, y, sz * 4);
> 465	      grad.addColorStop(0, `rgba(${color}, ${0.7 * tw})`);
> 466	      grad.addColorStop(1, `rgba(${color}, 0)`);
> 467	      ctx.fillStyle = grad;
> 468	      ctx.beginPath();
> 469	      ctx.arc(x, y, sz * 4, 0, Math.PI * 2);
> 470	      ctx.fill();
> 471	      ctx.fillStyle = `rgba(${color}, ${0.9 * tw})`;
> 472	      ctx.beginPath();
> 473	      ctx.arc(x, y, sz, 0, Math.PI * 2);
> 474	      ctx.fill();
> 475	    }
> 476	
> 477	    // Center sigil — different per archetype
> 478	    ctx.save();
> 479	    ctx.translate(cx, cy);
> 480	    ctx.strokeStyle = 'rgba(255,255,255,0.5)';
> 481	    ctx.lineWidth = 1;
> 482	    if (archetype === 'architect') {
> 483	      // hexagon
> 484	      ctx.beginPath();
> 485	      for (let k = 0; k < 6; k++) {
> 486	        const a = k / 6 * Math.PI * 2 + t * 0.1;
> 487	        const x = Math.cos(a) * 14,y = Math.sin(a) * 14;
> 488	        if (k === 0) ctx.moveTo(x, y);else ctx.lineTo(x, y);
> 489	      }
> 490	      ctx.closePath();ctx.stroke();
> 491	    } else if (archetype === 'coder') {
> 492	      // angle bracket pair
> 493	      ctx.beginPath();
> 494	      ctx.moveTo(-12, -8);ctx.lineTo(-18, 0);ctx.lineTo(-12, 8);
> 495	      ctx.moveTo(12, -8);ctx.lineTo(18, 0);ctx.lineTo(12, 8);
> 496	      ctx.stroke();
> 497	    } else {
> 498	      // shield arc
> 499	      ctx.beginPath();
> 500	      ctx.arc(0, 0, 14, Math.PI * 0.15, Math.PI * 0.85);
> 501	      ctx.moveTo(0, -14);ctx.lineTo(0, 14);
> 502	      ctx.stroke();
> 503	    }
> 504	    ctx.restore();
> 505	  }, [archetype]);
> 506	
> 507	  return <canvas ref={ref} className={className} style={{ width: size, height: size, ...style }} />;
> 508	};
> 509	
> 510	// Export to window for cross-script babel files
> 511	Object.assign(window, { useCanvas, ConstellationCanvas, CymaticsCanvas, AgentCloud });
> ```

## 🤖 Claude *(23:26:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/precut-sections.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// MCORCH Landing V2 — all sections, ported faithfully from
> 2	// design_handoff_mcorch/landing-v2/{01,02,03}.jsx (2026-07-03) as real React.
> 3	// Counters render their final values (no count-up dependency); scroll-scrub /
> 4	// GSAP motion from the handoff is a progressive-enhancement follow-up.
> 5	import type { CSSProperties } from 'react';
> 6	import { Link } from 'react-router-dom';
> 7	import { Wordmark, SigilMark, Cta, PillarIcon, HeroBackdrop } from './Brand';
> 8	
> 9	const card: CSSProperties = {
> 10	  display: 'grid',
> 11	  gridTemplateColumns: '120px 1fr',
> 12	  gap: 24,
> 13	  alignItems: 'baseline',
> 14	  padding: '22px 26px',
> 15	  borderRadius: 14,
> 16	  border: '1px solid var(--silver-2)',
> 17	  background: 'linear-gradient(180deg, rgba(255,255,255,0.025), rgba(255,255,255,0.005))',
> 18	};
> 19	
> 20	// ---------------------------------------------------------------- NAV
> 21	export const Nav = () => (
> 22	  <header className="lp-nav" id="lp-nav">
> 23	    <a href="#top" style={{ display: 'flex', alignItems: 'center', gap: 14, textDecoration: 'none' }}>
> 24	      <SigilMark />
> 25	      <Wordmark size={13} />
> 26	    </a>
> 27	    <nav className="links">
> 28	      <a href="#orquestra">A Orquestra</a>
> 29	      <a href="#como">Como Funciona</a>
> 30	      <a href="#paraquem">Para Quem</a>
> 31	      <a href="#planos">Planos</a>
> 32	      <a href="#faq">FAQ</a>
> 33	    </nav>
> 34	    <Cta href="#planos" variant="primary">Ativar minha agência</Cta>
> 35	  </header>
> 36	);
> 37	
> 38	// ---------------------------------------------------------------- HERO
> 39	export const Hero = () => (
> 40	  <section className="lp-hero" id="top">
> 41	    <HeroBackdrop />
> 42	    <div className="lp-hero-vignette" />
> 43	    <div className="lp-hero-inner">
> 44	      <div className="lp-eyebrow" style={{ justifyContent: 'center', marginBottom: 28 }}>
> 45	        A agência autônoma · Operada por IA · Vol. I 2026
> 46	      </div>
> 47	
> 48	      <h1>
> 49	        <span className="word"><span>A agência</span></span>{' '}
> 50	        <span className="word"><span><em className="mc-display-i mc-cyan">inteira</em>.</span></span>
> 51	        <br />
> 52	        <span className="word"><span>Dedicada</span></span>{' '}
> 53	        <span className="word"><span>a <em className="mc-display-i mc-gold">você</em>.</span></span>
> 54	      </h1>
> 55	
> 56	      <p className="sub">
> 57	        MCORCH coloca um <b style={{ color: 'var(--bone)' }}>CEO, um PMO e um PMI</b> — orquestrados por IA —
> 58	        100% dedicados à sua operação e integrados às ferramentas que você já usa. Você cria e fecha negócio.
> 59	        A orquestra cuida do resto.
> 60	      </p>
> 61	
> 62	      <div className="cta-row">
> 63	        <Cta href="#planos" variant="primary">Ativar minha agência</Cta>
> 64	        <Cta href="#orquestra" variant="ghost">Ver a orquestra</Cta>
> 65	      </div>
> 66	
> 67	      <div className="trust">
> 68	        <span>◆ <b>CEO · PMO · PMI</b> dedicados</span>
> 69	        <span>◆ Integra com <b>seu stack</b></span>
> 70	        <span>◆ Operação <b>24/7</b></span>
> 71	        <span>◆ Setup em <b>1 sessão</b></span>
> 72	      </div>
> 73	    </div>
> 74	
> 75	    <div className="lp-hero-scroll-hint">
> 76	      <span>Role para a orquestra</span>
> 77	      <div className="line" />
> 78	    </div>
> 79	  </section>
> 80	);
> 81	
> 82	// ---------------------------------------------------------------- TRUST STRIP
> 83	export const TrustStrip = () => (
> 84	  <div className="lp-trust-strip">
> 85	    <div className="item"><span className="v cyan">03</span><span>Executivos<br />dedicados</span></div>
> 86	    <div className="item"><span className="v">+40</span><span>Ferramentas<br />integráveis</span></div>
> 87	    <div className="item"><span className="v gold">3.4×</span><span>Capacidade<br />de entrega</span></div>
> 88	    <div className="item"><span className="v">24/7</span><span>Operação<br />orquestrada</span></div>
> 89	    <div className="item"><span className="v cyan">42 min</span><span>Setup<br />completo</span></div>
> 90	  </div>
> 91	);
> 92	
> 93	// ---------------------------------------------------------------- 01 PROBLEM
> 94	export const ProblemSection = () => (
> 95	  <section className="lp-section" id="sintoma">
> 96	    <span className="num">01 / O GARGALO</span>
> 97	    <div className="lp-bignum" style={{ right: '8vw', top: '40px' }}>01</div>
> 98	
> 99	    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 80, alignItems: 'center', marginTop: 40 }}>
> 100	      <div>
> 101	        <div className="lp-eyebrow lp-reveal">O preço de fazer tudo sozinho</div>
> 102	        <h2 className="lp-h1 lp-reveal">
> 103	          Você virou o<br />
> 104	          <em className="mc-display-i mc-cyan">gargalo</em> do<br />
> 105	          próprio estúdio.
> 106	        </h2>
> 107	        <p className="lp-lede lp-reveal" style={{ marginBottom: 28 }}>
> 108	          Todo briefing passa por você. Todo prazo depende de você. Cada ferramenta fala uma língua
> 109	          diferente e nenhuma conversa com a outra. Você abriu um estúdio pra criar — e virou gerente de
> 110	          projeto, atendimento e financeiro de você mesmo.
> 111	        </p>
> 112	        <p className="lp-lede lp-reveal" style={{ color: 'var(--bone-3)' }}>
> 113	          Enquanto isso, o trabalho que te trouxe até aqui — a criação — fica pra depois. Esse é o gargalo.
> 114	        </p>
> 115	      </div>
> 116	
> 117	      <div className="lp-reveal" style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
> 118	        {[
> 119	          { v: '68%', l: 'Do dia gasto em coordenação, não em criação', c: 'gold' },
> 120	          { v: '5+', l: 'Ferramentas que não conversam entre si', c: 'cyan' },
> 121	          { v: '0', l: 'Pessoas cuidando da operação enquanto você cria', c: 'gold' },
> 122	          { v: '∞', l: 'Mensagens de cliente que moram na sua cabeça', c: 'cyan' },
> 123	        ].map((row, i) => (
> 124	          <div key={i} style={card}>
> 125	            <span
> 126	              className="mc-num"
> 127	              style={{
> 128	                fontSize: 56,
> 129	                lineHeight: 1,
> 130	                color: row.c === 'gold' ? 'var(--gold)' : 'var(--cyan)',
> 131	                fontStyle: row.c === 'gold' ? 'italic' : 'normal',
> 132	              }}
> 133	            >
> 134	              {row.v}
> 135	            </span>
> 136	            <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--bone-2)', letterSpacing: '0.04em', lineHeight: 1.5 }}>
> 137	              {row.l}
> 138	            </span>
> 139	          </div>
> 140	        ))}
> 141	      </div>
> 142	    </div>
> 143	  </section>
> 144	);
> 145	
> 146	// ---------------------------------------------------------------- 02 AUDIENCE
> 147	export const AudienceSection = () => (
> 148	  <section className="lp-section" id="paraquem" style={{ borderTop: '1px solid var(--silver-2)' }}>
> 149	    <span className="num">02 / PARA QUEM</span>
> 150	    <div className="lp-bignum" style={{ right: '8vw', top: '40px' }}>02</div>
> 151	
> 152	    <div style={{ maxWidth: 920, marginBottom: 64, marginTop: 40 }}>
> 153	      <div className="lp-eyebrow lp-reveal">Feito para quem vive de entregar</div>
> 154	      <h2 className="lp-h2 lp-reveal">
> 155	        A operação por trás<br />
> 156	        de cada <em className="mc-display-i mc-cyan">entrega</em>.
> 157	      </h2>
> 158	      <p className="lp-lede lp-reveal">
> 159	        Se o seu trabalho é criativo e a sua rotina virou gestão, a orquestra é pra você. Ela assume a
> 160	        operação de quem entrega — e devolve o foco à criação.
> 161	      </p>
> 162	    </div>
> 163	
> 164	    <div className="lp-pillars">
> 165	      {[
> 166	        { k: 'Estúdios de design', d: 'Briefings, versões e aprovações orquestrados. Mais projetos entregues sem você virar gerente.' },
> 167	        { k: 'Video makers', d: 'Da pauta ao render: roteiro, cronograma e entregas no prazo, sincronizados ao seu editor.' },
> 168	        { k: 'Social media', d: 'Calendário, aprovação e publicação em fluxo. O ritmo é do PMO; a integração é do PMI.' },
> 169	        { k: 'Copywriters', d: 'Pautas, revisões e versionamento sob controle. Cada peça no tom, no prazo e no lugar.' },
> 170	        { k: 'Web designers', d: 'Escopo, sprint e handoff de dev orquestrados. Menos retrabalho, mais sites no ar.' },
> 171	        { k: 'Tráfego · Google & Meta Ads', d: 'Verba, criativos e relatórios acompanhados de perto. O CEO lê o ROI; o PMI ajusta a campanha.' },
> 172	      ].map((a, i) => (
> 173	        <div key={i} className="lp-pillar lp-reveal" style={{ padding: '26px 24px 28px' }}>
> 174	          <div className="pill-num" style={{ marginBottom: 14 }}>◆ Vertical {String(i + 1).padStart(2, '0')}</div>
> 175	          <h3 className="lp-h3" style={{ fontSize: 22, marginBottom: 10 }}>{a.k}</h3>
> 176	          <p style={{ fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.65, color: 'var(--bone-2)', margin: 0 }}>{a.d}</p>
> 177	        </div>
> 178	      ))}
> 179	    </div>
> 180	  </section>
> 181	);
> 182	
> 183	// ---------------------------------------------------------------- 03 SOLUTION
> 184	export const SolutionSection = () => (
> 185	  <section className="lp-section" id="orquestra">
> 186	    <span className="num">03 / A ORQUESTRA</span>
> 187	    <div className="lp-bignum" style={{ right: '8vw', top: '40px' }}>03</div>
> 188	
> 189	    <div style={{ maxWidth: 960, marginBottom: 80 }}>
> 190	      <div className="lp-eyebrow lp-reveal">A agência que trabalha por dentro</div>
> 191	      <h2 className="lp-h1 lp-reveal">
> 192	        Não é um app.<br />
> 193	        É a sua <em className="mc-display-i mc-cyan">agência</em><br />
> 194	        operando <em className="mc-display-i mc-gold">sozinha</em>.
> 195	      </h2>
> 196	      <p className="lp-lede lp-reveal">
> 197	        Três executivos orquestrados por IA, 100% dedicados à sua operação e integrados ao seu ecossistema.
> 198	        Você não contrata uma equipe — você ativa uma agência inteira.
> 199	      </p>
> 200	    </div>
> 201	
> 202	    <div className="lp-pillars">
> 203	      {[
> 204	        {
> 205	          n: '§01', icon: 'ceo' as const, title: 'CEO', role: 'Direção',
> 206	          body: 'Lê a sua operação inteira, define prioridades e toma as decisões de rumo. Protege a sua margem, distribui a energia da equipe e diz não pelo que não vale a pena.',
> 207	          stamp: 'Direção · Sempre on',
> 208	        },
> 209	        {
> 210	          n: '§02', icon: 'pmo' as const, title: 'PMO', role: 'Orquestração',
> 211	          body: 'O escritório de projetos que nunca perde um prazo nem um briefing. Planeja, aloca, acompanha cada cliente e garante o padrão de entrega — projeto por projeto.',
> 212	          stamp: 'Orquestração · Zero atraso',
> 213	        },
> 214	        {
> 215	          n: '§03', icon: 'pmi' as const, title: 'PMI', role: 'Integração',
> 216	          body: 'Executa o dia a dia e conecta tudo ao seu ecossistema: Figma, Drive, Notion, editor de vídeo, Meta e Google Ads, CRM, WhatsApp. Nada solto — tudo no lugar certo.',
> 217	          stamp: 'Integração · Seu stack',
> 218	        },
> 219	      ].map((p, i) => (
> 220	        <div key={i} className="lp-pillar lp-reveal">
> 221	          <div className="pill-num">{p.n} · {p.role}</div>
> 222	          <div className="pill-icon"><PillarIcon kind={p.icon} /></div>
> 223	          <h3 className="lp-h3" style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
> 224	            {p.title}
> 225	            <span style={{ fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '0.18em', textTransform: 'uppercase', color: 'var(--bone-3)' }}>{p.role}</span>
> 226	          </h3>
> 227	          <p style={{ fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.7, color: 'var(--bone-2)', margin: '0 0 24px' }}>{p.body}</p>
> 228	          <div
> 229	            style={{
> 230	              paddingTop: 18,
> 231	              borderTop: '1px solid var(--silver-2)',
> 232	              display: 'flex',
> 233	              justifyContent: 'space-between',
> 234	              fontFamily: 'var(--mono)',
> 235	              fontSize: 9,
> 236	              letterSpacing: '0.22em',
> 237	              textTransform: 'uppercase',
> 238	              color: 'var(--bone-3)',
> 239	            }}
> 240	          >
> 241	            <span>{p.stamp}</span>
> 242	            <span className="mc-cyan">◆ 100% dedicado</span>
> 243	          </div>
> 244	        </div>
> 245	      ))}
> 246	    </div>
> 247	  </section>
> 248	);
> 249	
> 250	// ---------------------------------------------------------------- 04 HOW
> 251	export const HowSection = () => (
> 252	  <section className="lp-section" id="como">
> 253	    <span className="num">04 / ATIVAÇÃO</span>
> 254	    <div className="lp-bignum" style={{ right: '8vw', top: '40px' }}>04</div>
> 255	
> 256	    <div style={{ maxWidth: 920, marginBottom: 80 }}>
> 257	      <div className="lp-eyebrow lp-reveal">Como funciona</div>
> 258	      <h2 className="lp-h2 lp-reveal">
> 259	        Da <em className="mc-display-i mc-cyan">ativação</em> à operação autônoma,<br />
> 260	        em <em className="mc-display-i mc-gold">42 minutos</em>.
> 261	      </h2>
> 262	      <p className="lp-lede lp-reveal">
> 263	        Uma ativação guiada. Quatro fases. Nenhuma delas pede que você vire especialista em nada.
> 264	      </p>
> 265	    </div>
> 266	
> 267	    <div className="lp-steps">
> 268	      {[
> 269	        { ph: 'Fase 01', title: 'Diagnóstico', body: 'Você responde 12 perguntas sobre seu estúdio, seus serviços e seus clientes. O CEO calibra prioridades; o PMO mapeia como você trabalha hoje.' },
> 270	        { ph: 'Fase 02', title: 'Integração', body: 'Conectamos as ferramentas que você já usa — design, vídeo, social, tráfego, CRM. 42 minutos, uma única sessão. Sem código, sem configuração manual.' },
> 271	        { ph: 'Fase 03', title: 'Modo Sombra', body: 'A orquestra opera em sombra por 7 dias. Você vê cada decisão, cada briefing e cada entrega que ela faria — sem ainda perder o controle.' },
> 272	        { ph: 'Fase 04', title: 'Autônomo', body: 'Você aprova. A agência assume a operação. A partir daqui sua função volta a ser uma só: criar e fechar negócio.' },
> 273	      ].map((s, i) => (
> 274	        <div key={i} className="lp-step lp-reveal">
> 275	          <div className="knot" />
> 276	          <div className="ph">{s.ph}</div>
> 277	          <h3 className="lp-h3" style={{ fontSize: 26 }}>{s.title}</h3>
> 278	          <p style={{ fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.7, color: 'var(--bone-2)', margin: 0 }}>{s.body}</p>
> 279	        </div>
> 280	      ))}
> 281	    </div>
> 282	  </section>
> 283	);
> 284	
> 285	// ---------------------------------------------------------------- 05 DEMO
> 286	export const DemoSection = () => (
> 287	  <section className="lp-section" id="demo" style={{ borderTop: '1px solid var(--silver-2)' }}>
> 288	    <span className="num">05 / UM DIA</span>
> 289	    <div className="lp-bignum" style={{ right: '8vw', top: '40px' }}>05</div>
> 290	
> 291	    <div className="lp-demo-grid" style={{ marginTop: 40 }}>
> 292	      <div className="lp-reveal">
> 293	        <div className="lp-eyebrow">Live · Orquestra ativa</div>
> 294	        <h2 className="lp-h2">
> 295	          Uma terça-feira<br />operada <em className="mc-display-i mc-cyan">sozinha</em>.
> 296	        </h2>
> 297	        <p className="lp-lede" style={{ marginBottom: 32 }}>
> 298	          Um recorte do dia da sua agência sem você no meio. O CEO prioriza, o PMO orquestra, o PMI executa e
> 299	          integra. Três clientes atendidos, uma campanha reajustada, zero prazo perdido. Você criou. A operação
> 300	          andou.
> 301	        </p>
> 302	        <Cta href="#planos">Ativar minha agência</Cta>
> 303	      </div>
> 304	
> 305	      <div className="lp-term lp-reveal">
> 306	        <div className="head">
> 307	          <span className="dot" style={{ background: '#ff5f57' }} />
> 308	          <span className="dot" style={{ background: '#febc2e' }} />
> 309	          <span className="dot" style={{ background: '#28c840' }} />
> 310	          <span className="label">mcorch · orquestra · live</span>
> 311	        </div>
> 312	        <div><span className="fg">› 09:14</span> <span className="pr">ceo</span> · prioridade <span className="fg">→</span> <span className="gl">campanha Zaffari</span> · deadline 48h</div>
> 313	        <div><span className="fg">› 09:14</span> <span className="pr">pmo</span> · aloca · briefing gerado <span className="fg">→</span> time de design</div>
> 314	        <div><span className="fg">› 09:15</span> <span className="pr">pmi</span> · sincroniza <span className="nb">Figma ↔ Drive ↔ Notion</span> <span className="ok">ok</span></div>
> 315	        <div><span className="fg">› 11:02</span> <span className="pr">pmi</span> · Meta Ads · verba realocada p/ criativo #4 <span className="ok">CTR 3.1%</span></div>
> 316	        <div><span className="fg">› 11:03</span> <span className="pr">pmo</span> · QA · peça revisada · dentro do padrão <span className="ok">✓</span></div>
> 317	        <div><span className="fg">› 14:20</span> <span className="pr">ceo</span> · margem do projeto projetada <span className="gl">38%</span></div>
> 318	        <div><span className="fg">› 14:21</span> <span className="pr">pmi</span> · entrega enviada ao cliente via WhatsApp <span className="ok">ok</span></div>
> 319	        <div><span className="fg">› 18:40</span> <span className="pr">pmo</span> · amanhã · 3 entregas agendadas · 0 conflitos<span className="mc-caret" /></div>
> 320	      </div>
> 321	    </div>
> 322	  </section>
> 323	);
> 324	
> 325	// ---------------------------------------------------------------- 06 RESULTS
> 326	export const ResultsSection = () => (
> 327	  <section className="lp-section" id="provas" style={{ paddingTop: 60 }}>
> 328	    <span className="num">06 / EVIDÊNCIA</span>
> 329	    <div className="lp-bignum" style={{ right: '8vw', top: '40px' }}>06</div>
> 330	
> 331	    <div style={{ maxWidth: 920, marginBottom: 60, marginTop: 40 }}>
> 332	      <div className="lp-eyebrow lp-reveal">Projeções · cohort piloto Vol. I</div>
> 333	      <h2 className="lp-h2 lp-reveal">
> 334	        O que muda quando<br />
> 335	        a operação <em className="mc-display-i mc-gold">sai das suas costas</em>.
> 336	      </h2>
> 337	    </div>
> 338	
> 339	    <div className="lp-results lp-reveal">
> 340	      <div className="cell gold"><div className="v">3.4×</div><div className="l">Capacidade de entrega · 90 dias</div></div>
> 341	      <div className="cell cyan"><div className="v">2.4k</div><div className="l">Tarefas orquestradas / mês</div></div>
> 342	      <div className="cell"><div className="v">−68%</div><div className="l">Horas em coordenação</div></div>
> 343	      <div className="cell gold"><div className="v">99.9%</div><div className="l">Uptime da operação</div></div>
> 344	    </div>
> 345	  </section>
> 346	);
> 347	
> 348	// ---------------------------------------------------------------- OFFER (vision + plans)
> 349	export const ChampionshipOffer = () => (
> 350	  <section id="oferta" style={{ position: 'relative', borderTop: '1px solid var(--silver-2)' }}>
> 351	    <div className="lp-vision" id="lp-vision">
> 352	      <div className="lp-vision-pin">
> 353	        <div className="lp-vision-ambient" />
> 354	        <div className="lp-vision-stage">
> 355	          <div className="lp-eyebrow" style={{ justifyContent: 'center', color: 'var(--gold)', marginBottom: 36 }}>
> 356	            ◆ A visão · Vol. I · 2026
> 357	          </div>
> 358	
> 359	          <div className="lp-vision-acts">
> 360	            <h3 className="lp-vision-act" data-vision-act="0">
> 361	              Imagine seu estúdio entregando o dobro—<br />
> 362	              sem você virar gerente de projeto,<br />
> 363	              atendimento e financeiro <em className="mc-display-i mc-cyan">ao mesmo tempo</em>.
> 364	            </h3>
> 365	            <h3 className="lp-vision-act" data-vision-act="1">
> 366	              Imagine um <em className="mc-display-i mc-gold">CEO</em>, um <em className="mc-display-i mc-gold">PMO</em> e um{' '}
> 367	              <em className="mc-display-i mc-gold">PMI</em><br />
> 368	              cuidando da operação enquanto você cria.<br />
> 369	              Cada prazo, cada briefing, cada ferramenta — <em className="mc-display-i mc-cyan">no lugar</em>.
> 370	            </h3>
> 371	            <h3 className="lp-vision-act" data-vision-act="2">
> 372	              Essa é a agência que trabalha por dentro.<br />
> 373	              <em className="mc-display-i mc-gold">MCORCH</em> é o primeiro corte dela.
> 374	            </h3>
> 375	          </div>
> 376	
> 377	          <div className="lp-vision-floor">
> 378	            <div className="lp-vision-progress">
> 379	              <span className="dot" data-dot="0" />
> 380	              <span className="bar" />
> 381	              <span className="dot" data-dot="1" />
> 382	              <span className="bar" />
> 383	              <span className="dot" data-dot="2" />
> 384	            </div>
> 385	          </div>
> 386	        </div>
> 387	      </div>
> 388	    </div>
> 389	
> 390	    <div className="lp-marquee-wrap">
> 391	      <div className="lp-marquee" id="offer-marquee">
> 392	        <span>A agência inteira</span><em>·</em><span>CEO · PMO · PMI</span><em>·</em>
> 393	        <span>Dedicada 100%</span><em>·</em><span>Integrada ao seu stack</span><em>·</em>
> 394	        <span>Vol. I · 2026</span><em>·</em>
> 395	        <span>A agência inteira</span><em>·</em><span>CEO · PMO · PMI</span><em>·</em>
> 396	        <span>Dedicada 100%</span><em>·</em><span>Integrada ao seu stack</span><em>·</em>
> 397	        <span>Vol. I · 2026</span><em>·</em>
> 398	      </div>
> 399	    </div>
> 400	
> 401	    <div className="lp-offer-stage" id="planos">
> 402	      <span
> 403	        className="num"
> 404	        style={{ position: 'absolute', top: 60, left: '8vw', fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '0.32em', color: 'var(--bone-3)' }}
> 405	      >
> 406	        07 / PLANOS
> 407	      </span>
> 408	
> 409	      <div className="lp-offer-hd lp-reveal">
> 410	        <h2 className="lp-h2">
> 411	          A orquestra<br />
> 412	          tem <em className="mc-display-i mc-cyan">três</em> profundidades.
> 413	        </h2>
> 414	        <p className="lp-lede" style={{ marginTop: 18 }}>
> 415	          Você não contrata uma equipe. Você ativa uma agência.<br />
> 416	          Cada plano é uma profundidade de operação. Comece onde faz sentido — a orquestra escala com você.
> 417	        </p>
> 418	      </div>
> 419	
> 420	      <div className="lp-scarcity lp-reveal">
> 421	        <div className="lp-scarcity-row">
> 422	          <span className="dot mc-pulse" />
> 423	          <span className="lbl">Cohort Vol. I · Q1 2026</span>
> 424	          <span className="sep">·</span>
> 425	          <span className="count">17<span className="of">/24</span> vagas tomadas</span>
> 426	        </div>
> 427	        <div className="lp-scarcity-bar"><div className="fill" style={{ width: '71%' }} /></div>
> 428	      </div>
> 429	
> 430	      <div className="lp-pricing">
> 431	        <div className="lp-plan lp-reveal">
> 432	          <div className="tier">§ Plano 01</div>
> 433	          <h3 className="name">Signal</h3>
> 434	          <div className="price"><span className="ccy">R$</span>1.497<span className="per">/ mês · cancele quando quiser</span></div>
> 435	          <ul>
> 436	            <li>PMO + PMI essenciais · orquestração base</li>
> 437	            <li>Até 10 integrações do seu stack</li>
> 438	            <li>Onboarding em grupo · sessões quinzenais</li>
> 439	            <li>Painel de operação</li>
> 440	            <li>Suporte por e-mail · 48h</li>
> 441	            <li className="muted">CEO dedicado</li>
> 442	            <li className="muted">QA automatizado de entregas</li>
> 443	          </ul>
> 444	          <div className="price-foot"><Cta variant="ghost">Ativar Signal</Cta></div>
> 445	        </div>
> 446	
> 447	        <div className="lp-plan is-featured lp-reveal">
> 448	          <div className="badge">A agência inteira</div>
> 449	          <div className="tier mc-cyan">§ Plano 02</div>
> 450	          <h3 className="name">Harness</h3>
> 451	          <div className="price"><span className="ccy">R$</span>4.997<span className="per">/ mês · ciclo trimestral</span></div>
> 452	          <ul>
> 453	            <li><b>CEO + PMO + PMI · 100% dedicados</b></li>
> 454	            <li>Integração total ao seu ecossistema · +40 ferramentas</li>
> 455	            <li>Setup 1:1 · 42 min com a equipe</li>
> 456	            <li>QA de entregas + relatório semanal de ROI</li>
> 457	            <li>Suporte WhatsApp · resposta em 4h</li>
> 458	            <li>Acesso ao MIV completo · Vol. I</li>
> 459	          </ul>
> 460	          <div className="price-foot"><Cta variant="primary">Ativar Harness</Cta></div>
> 461	        </div>
> 462	
> 463	        <div className="lp-plan lp-reveal">
> 464	          <div className="tier mc-gold">§ Plano 03</div>
> 465	          <h3 className="name">Sovereign</h3>
> 466	          <div className="price"><span className="ccy">R$</span>14.997<span className="per">/ mês · sob convite</span></div>
> 467	          <ul>
> 468	            <li>Tudo de Harness, sem teto</li>
> 469	            <li>Orquestra dedicada · agentes privados</li>
> 470	            <li>Integrações sob medida · até 7 exclusivas</li>
> 471	            <li>Gerente de conta humano · SLA &lt; 1h</li>
> 472	            <li>Revisão estratégica mensal 1:1</li>
> 473	            <li>Roadmap de produto co-criado</li>
> 474	          </ul>
> 475	          <div className="price-foot"><Cta variant="ghost">Solicitar convite</Cta></div>
> 476	        </div>
> 477	      </div>
> 478	
> 479	      <div className="lp-offer-close lp-reveal">
> 480	        <div className="lp-offer-stack">
> 481	          <div className="stack-row"><span className="k">◆ Garantia</span><span className="v">14 dias incondicionais · sem call de retenção</span></div>
> 482	          <div className="stack-row"><span className="k">◆ Setup</span><span className="v">42 minutos · uma única sessão de integração</span></div>
> 483	          <div className="stack-row"><span className="k">◆ Cohort</span><span className="v"><b className="mc-cyan">17/24</b> vagas tomadas · fechamento em janeiro</span></div>
> 484	          <div className="stack-row"><span className="k">◆ Acesso</span><span className="v">Vol. I · primeiro corte público da agência autônoma</span></div>
> 485	        </div>
> 486	
> 487	        <div className="lp-offer-finale">
> 488	          <p style={{ fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '0.22em', textTransform: 'uppercase', color: 'var(--bone-3)', marginBottom: 22 }}>
> 489	            Uma agência. Não mais uma ferramenta.
> 490	          </p>
> 491	          <h3 style={{ fontFamily: 'var(--display)', fontSize: 'clamp(36px, 5vw, 64px)', lineHeight: 1, letterSpacing: '-0.02em', margin: '0 0 32px' }}>
> 492	            Sua agência,<br />
> 493	            <em className="mc-display-i mc-cyan">dedicada</em> e <em className="mc-display-i mc-gold">integrada</em>.
> 494	          </h3>
> 495	          <Cta variant="primary">Ativar minha agência</Cta>
> 496	        </div>
> 497	      </div>
> 498	    </div>
> 499	  </section>
> 500	);
> 501	
> 502	// ---------------------------------------------------------------- GUARANTEE
> 503	export const GuaranteeSection = () => (
> 504	  <section className="lp-section">
> 505	    <div className="lp-guarantee lp-reveal">
> 506	      <div className="seal">14d</div>
> 507	      <div>
> 508	        <div className="lp-eyebrow" style={{ marginBottom: 16, color: 'var(--gold)' }}>Garantia · Risco reverso</div>
> 509	        <h3 className="lp-h3" style={{ fontSize: 32, marginBottom: 14 }}>
> 510	          14 dias para ver a operação rodar sozinha.<br />
> 511	          Se não vier, devolvemos tudo.
> 512	        </h3>
> 513	        <p style={{ fontFamily: 'var(--mono)', fontSize: 13, lineHeight: 1.75, color: 'var(--bone-2)', margin: 0, maxWidth: '72ch' }}>
> 514	          A primeira coisa que a gente entrega não é receita — é operação no lugar. Em 14 dias, se os seus
> 515	          prazos ainda dependem de você e as suas ferramentas continuam desconectadas, o reembolso é
> 516	          incondicional. Sem call de retenção. Sem desculpa.
> 517	        </p>
> 518	      </div>
> 519	    </div>
> 520	  </section>
> 521	);
> 522	
> 523	// ---------------------------------------------------------------- 08 FAQ
> 524	export const FAQSection = () => (
> 525	  <section className="lp-section" id="faq">
> 526	    <span className="num">08 / DÚVIDAS</span>
> 527	    <div className="lp-bignum" style={{ right: '8vw', top: '40px' }}>08</div>
> 528	
> 529	    <div style={{ maxWidth: 920, marginBottom: 50, marginTop: 40 }}>
> 530	      <div className="lp-eyebrow lp-reveal">Perguntas honestas</div>
> 531	      <h2 className="lp-h2 lp-reveal">
> 532	        O que você ainda<br />
> 533	        <em className="mc-display-i mc-cyan">precisa saber</em>.
> 534	      </h2>
> 535	    </div>
> 536	
> 537	    <div className="lp-faq lp-reveal">
> 538	      {[
> 539	        { q: 'O MCORCH substitui a minha equipe?', a: 'Não. Ele substitui a operação que sobra pra você — a gestão, a coordenação, a integração de ferramentas. Sua equipe criativa fica livre pra criar; o CEO, o PMO e o PMI cuidam de tudo que não é criação.' },
> 540	        { q: 'Preciso saber configurar ferramentas ou mexer em código?', a: 'Não. Em uma sessão de 42 minutos conectamos seu Figma, Drive, editor de vídeo, Meta e Google Ads, CRM e WhatsApp. A partir daí a orquestra opera integrada ao que você já usa.' },
> 541	        { q: 'Serve pro meu tipo de trabalho?', a: 'Funciona para estúdios de design, video makers, social media, copywriters, web designers e gestores de tráfego. Se a operação ainda depende de você para andar, é exatamente pra você.' },
> 542	        { q: 'Em quanto tempo eu sinto diferença?', a: '7 dias de modo sombra já mostram a operação rodando. Em 30 dias, cai a carga de coordenação. Em 90 dias, a meta documentada é 3.4× de capacidade de entrega — sem aumentar a equipe.' },
> 543	        { q: 'Ele publica post e roda anúncio sozinho?', a: 'Com a sua aprovação. O PMI executa e integra, o PMO garante o padrão, o CEO decide a prioridade. Você define o nível de autonomia — de "só sugere" a "executa e me avisa".' },
> 544	        { q: 'Como ficam meus dados e acessos?', a: 'Cada operação é isolada e criptografada. Você concede e revoga acessos quando quiser, e vê cada ação registrada. Nada é feito às escondidas.' },
> 545	        { q: 'O Vol. I é o lançamento. Vai mudar depois?', a: 'Sim. Vol. I é o primeiro corte público. Quem entra agora opera com tarifa de fundação e recebe as próximas versões da arquitetura. As vagas deste cohort são limitadas a 24.' },
> 546	      ].map((item, i) => (
> 547	        <details key={i}>
> 548	          <summary>
> 549	            <span>{item.q}</span>
> 550	            <span className="sign">+</span>
> 551	          </summary>
> 552	          <div className="a">{item.a}</div>
> 553	        </details>
> 554	      ))}
> 555	    </div>
> 556	  </section>
> 557	);
> 558	
> 559	// ---------------------------------------------------------------- FINAL CTA
> 560	export const FinalCTA = () => (
> 561	  <section className="lp-final" id="acessar">
> 562	    <div style={{ position: 'relative', zIndex: 2 }}>
> 563	      <div className="lp-eyebrow lp-reveal" style={{ justifyContent: 'center', color: 'var(--cyan)' }}>
> 564	        ◆ Vol. I · Ativação 2026
> 565	      </div>
> 566	      <h2 className="lp-reveal">
> 567	        <span className="cyan">Pare</span> de ser o gargalo.<br />
> 568	        <span className="gold">Ative</span> a agência.
> 569	      </h2>
> 570	      <p className="lp-lede lp-reveal" style={{ margin: '0 auto 44px', maxWidth: 620, textAlign: 'center' }}>
> 571	        Sua próxima entrega não precisa passar por você.<br />
> 572	        Precisa passar pela orquestra.
> 573	      </p>
> 574	      <div className="lp-reveal" style={{ display: 'inline-flex', gap: 16, flexWrap: 'wrap', justifyContent: 'center' }}>
> 575	        <Cta variant="primary">Ativar minha agência</Cta>
> 576	        <Cta href="#planos" variant="ghost">Ver os planos</Cta>
> 577	      </div>
> 578	      <div className="meta lp-reveal">
> 579	        <span><b>14 dias</b> de garantia</span>
> 580	        <span><b>42 min</b> de setup</span>
> 581	        <span><b>17/24</b> vagas tomadas</span>
> 582	        <span><b>Q1 2026</b> · Vol. I</span>
> 583	      </div>
> 584	    </div>
> 585	  </section>
> 586	);
> 587	
> 588	// ---------------------------------------------------------------- FOOTER
> 589	export const LandingFooter = () => (
> 590	  <footer className="lp-footer">
> 591	    <div className="row">
> 592	      <div style={{ maxWidth: 340 }}>
> 593	        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 18 }}>
> 594	          <SigilMark size={22} />
> 595	          <Wordmark size={12} />
> 596	        </div>
> 597	        <p style={{ fontFamily: 'var(--mono)', fontSize: 11, lineHeight: 1.7, color: 'var(--bone-3)', margin: 0 }}>
> 598	          Magic Constellation Orchestra · A agência autônoma.<br />
> 599	          Um CEO, um PMO e um PMI dedicados e integrados ao seu ecossistema.
> 600	        </p>
> 601	      </div>
> 602	
> 603	      <div className="col">
> 604	        <h5>A Orquestra</h5>
> 605	        <a href="#orquestra">CEO · PMO · PMI</a>
> 606	        <a href="#como">Como Funciona</a>
> 607	        <a href="#demo">Um Dia</a>
> 608	        <a href="#provas">Evidência</a>
> 609	      </div>
> 610	      <div className="col">
> 611	        <h5>Ativar</h5>
> 612	        <a href="#planos">Planos</a>
> 613	        <Link to="/auth">Ativação</Link>
> 614	        <a href="#faq">FAQ</a>
> 615	        <Link to="/auth">Login</Link>
> 616	      </div>
> 617	      <div className="col">
> 618	        <h5>Contato</h5>
> 619	        <a href="mailto:contato@mcorch.com">contato@mcorch.com</a>
> 620	        <a href="#">WhatsApp</a>
> 621	        <Link to="/terms">Termos</Link>
> 622	        <Link to="/privacy">Privacidade</Link>
> 623	      </div>
> 624	    </div>
> 625	    <div className="bottom">
> 626	      <span>© 2026 MCORCH · A agência autônoma</span>
> 627	      <span>◆ Vol. I · MIV-001 · 2026.01</span>
> 628	    </div>
> 629	  </footer>
> 630	);
> 631	
> ```

## 🤖 Claude *(23:27:25)*


## 🤖 Claude *(23:27:27)*

Agora tenho o quadro completo. Descoberta importante: o commit de corte **não tocou `landing.css`** (só `minimal.css`) — então todo o CSS rico (trust-strip, vision, pricing, terminal, results, reveal) provavelmente **ainda existe**. Restaurar as seções é muito mais viável do que parecia. Vou confirmar o estado do CSS de reveal e das classes ricas:

## 🤖 Claude *(23:27:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== .lp-reveal (come\u00e7a escondido? precisa de JS?) ===\"\ngrep -nE '\\.lp-reveal|@keyframes|prefers-reduced-motion' src/styles/mcorch/landing.css | head -40\necho \"\"\necho \"=== classes ricas presentes no landing.css? ===\"\nfor cls in lp-trust-strip lp-bignum lp-steps lp-term lp-results lp-vision lp-marquee lp-pricing lp-plan lp-scarcity lp-guarantee lp-final lp-demo-grid lp-hero-backdrop lp-wave lp-offer-stage; do\n  n=$(grep -c \"\\.$cls\" src/styles/mcorch/landing.css)\n  printf \"  %-18s %s\\n\" \"$cls\" \"$([ \"$n\" -gt 0 ] && echo \"\u2705 $n\" || echo \"\u274c AUSENTE\")\"\ndone",
  "description": "Check landing.css for reveal behavior and rich section classes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === .lp-reveal (começa escondido? precisa de JS?) ===
> 34:@keyframes lp-pulse {
> 448:.lp-reveal { will-change: transform, opacity; }
> 598:@keyframes lp-shimmer {
> 652:@keyframes lp-wave-drift {
> 656:@media (prefers-reduced-motion: reduce) { .mcorch-lp .lp-wave { animation: none; } }
> 
> === classes ricas presentes no landing.css? ===
>   lp-trust-strip     ✅ 5
>   lp-bignum          ✅ 1
>   lp-steps           ✅ 5
>   lp-term            ✅ 10
>   lp-results         ✅ 12
>   lp-vision          ✅ 15
>   lp-marquee         ✅ 5
>   lp-pricing         ✅ 2
>   lp-plan            ✅ 16
>   lp-scarcity        ✅ 9
>   lp-guarantee       ✅ 3
>   lp-final           ✅ 7
>   lp-demo-grid       ✅ 2
>   lp-hero-backdrop   ✅ 2
>   lp-wave            ✅ 2
>   lp-offer-stage     ✅ 3
> ```

## 🤖 Claude *(23:28:31)*


## 🤖 Claude *(23:28:36)*

Tudo confirmado e é uma boa notícia:
- **Todo o CSS rico ainda existe** em `landing.css` (trust-strip, vision, pricing, terminal, results, marquee — 16/16 classes presentes). O corte só apagou o JSX, não o estilo.
- `.lp-reveal` **não começa escondido** (`will-change` só) — as seções renderizam sem JS. Reveal será **aditivo** (não quebra no-JS/reduced-motion).

Então o trabalho é: (1) restaurar as 14 seções ricas com a regra de honestidade que você definiu, (2) portar a explosão de partículas (`particles.jsx`) como backdrop do hero **com ignição de load**, (3) orquestrar o reveal (IntersectionObserver + CSS, stagger em ritmo de leitura). Vou ler o `landing.css` inteiro para escrever as adições sem quebrar nada:

## 🤖 Claude *(23:28:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/styles/mcorch/landing.css"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	/* MCORCH brand — ported from design_handoff_mcorch (2026-07-03). Scoped to .mcorch-lp. Do not hand-edit tokens; source: design-system/DESIGN-SYSTEM.md */
> 2	/* MCORCH Landing — conversion-focused, AWWWARDS-caliber polish.
> 3	   Layered on top of styles.css + miv.css. */
> 4	
> 5	.mcorch-lp { background: #000; overflow-x: hidden; }
> 6	/* preloader opacity gate removed for React mount */
> 7	
> 8	/* Custom cursor (mirror MIV) */
> 9	/* custom cursor disabled */
> 10	.lp-cursor, .lp-cursor-ring {
> 11	  position: fixed; top: 0; left: 0; pointer-events: none; z-index: 99999;
> 12	  transition: width .22s, height .22s, opacity .22s, border-color .22s, background .22s;
> 13	  will-change: transform;
> 14	}
> 15	.lp-cursor {
> 16	  width: 6px; height: 6px; border-radius: 50%;
> 17	  background: var(--cyan); box-shadow: 0 0 10px rgba(0,242,255,0.7);
> 18	}
> 19	.lp-cursor-ring {
> 20	  width: 28px; height: 28px; border-radius: 50%;
> 21	  border: 1px solid rgba(0,242,255,0.55);
> 22	}
> 23	.lp-cursor-ring.is-hover { width: 46px; height: 46px; border-color: rgba(212,175,55,0.9); }
> 24	.lp-cursor.is-hover { background: var(--gold); box-shadow: 0 0 14px rgba(212,175,55,0.7); }
> 25	
> 26	/* Pre-loader */
> 27	#lp-preload {
> 28	  position: fixed; inset: 0; z-index: 9999;
> 29	  display: grid; place-items: center; background: #000;
> 30	  transition: opacity .55s ease;
> 31	}
> 32	#lp-preload.is-gone { opacity: 0; pointer-events: none; }
> 33	#lp-preload svg { animation: lp-pulse 1.6s ease-in-out infinite; }
> 34	@keyframes lp-pulse {
> 35	  0%, 100% { opacity: .35; transform: scale(.96); }
> 36	  50%      { opacity: 1;   transform: scale(1.04); }
> 37	}
> 38	
> 39	/* ----------------------------- NAV ----------------------------- */
> 40	.lp-nav {
> 41	  position: fixed; top: 0; left: 0; right: 0; z-index: 80;
> 42	  padding: 14px 28px;
> 43	  display: flex; justify-content: space-between; align-items: center;
> 44	  gap: clamp(16px, 3vw, 40px); flex-wrap: nowrap;
> 45	  transition: background .35s ease, border-color .35s ease, backdrop-filter .35s ease;
> 46	  border-bottom: 1px solid transparent;
> 47	}
> 48	.lp-nav.is-stuck {
> 49	  background: rgba(0,0,0,0.5);
> 50	  backdrop-filter: blur(22px) saturate(1.4);
> 51	  -webkit-backdrop-filter: blur(22px) saturate(1.4);
> 52	  border-bottom-color: rgba(255,255,255,0.06);
> 53	}
> 54	.lp-nav .links { display: flex; gap: 28px; align-items: center; }
> 55	.lp-nav .links a {
> 56	  font-family: var(--mono); font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
> 57	  color: var(--bone-2); text-decoration: none; transition: color .2s;
> 58	}
> 59	.lp-nav .links a:hover { color: var(--cyan); }
> 60	/* Hide the center anchor nav across the mid-width band (tablet / small laptop)
> 61	   so the wordmark and CTA never crowd it. Full nav returns above 1040px. */
> 62	@media (max-width: 1040px) { .lp-nav .links { display: none; } }
> 63	
> 64	/* ----------------------------- HERO ----------------------------- */
> 65	.lp-hero {
> 66	  position: relative; height: 100vh; min-height: 720px;
> 67	  overflow: hidden; display: flex; align-items: center; justify-content: center;
> 68	}
> 69	.lp-hero canvas { position: absolute; inset: 0; }
> 70	.lp-hero-vignette {
> 71	  position: absolute; inset: 0; pointer-events: none;
> 72	  background:
> 73	    radial-gradient(ellipse 130% 90% at 50% 45%, transparent 55%, rgba(0,0,0,0.78) 100%),
> 74	    linear-gradient(180deg, transparent 60%, rgba(0,0,0,0.6) 100%);
> 75	}
> 76	.lp-hero-inner {
> 77	  position: relative; z-index: 3; text-align: center; padding: 0 6vw;
> 78	  max-width: 1280px; width: 100%;
> 79	}
> 80	.lp-hero h1 {
> 81	  font-family: var(--display);
> 82	  font-size: clamp(56px, 9.4vw, 152px);
> 83	  line-height: 0.92; letter-spacing: -0.028em; margin: 24px 0 28px;
> 84	  text-wrap: balance;
> 85	}
> 86	.lp-hero h1 .word { display: inline-block; overflow: hidden; vertical-align: bottom; }
> 87	.lp-hero h1 .word > span { display: inline-block; will-change: transform; }
> 88	.lp-hero p.sub {
> 89	  font-family: var(--mono); font-size: clamp(13px, 1.05vw, 16px);
> 90	  line-height: 1.7; color: var(--bone-2); letter-spacing: 0.01em;
> 91	  max-width: 680px; margin: 0 auto 44px;
> 92	}
> 93	.lp-hero .cta-row { display: inline-flex; gap: 16px; flex-wrap: wrap; justify-content: center; }
> 94	.lp-hero .trust {
> 95	  margin-top: 56px; display: flex; gap: 36px; flex-wrap: wrap; justify-content: center;
> 96	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.22em; text-transform: uppercase;
> 97	  color: var(--bone-3);
> 98	}
> 99	.lp-hero .trust b { color: var(--bone); font-weight: 500; letter-spacing: 0.18em; }
> 100	.lp-hero-scroll-hint {
> 101	  position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
> 102	  font-family: var(--mono); font-size: 9px; letter-spacing: 0.32em; text-transform: uppercase;
> 103	  color: var(--bone-3); z-index: 4;
> 104	}
> 105	.lp-hero-scroll-hint .line {
> 106	  width: 1px; height: 30px; background: linear-gradient(180deg, var(--cyan), transparent);
> 107	  margin: 10px auto 0; opacity: .8;
> 108	}
> 109	
> 110	/* ----------------------------- BUTTONS (XL conversion) ----------------------------- */
> 111	.lp-cta {
> 112	  font-family: var(--mono); font-size: 12px; letter-spacing: 0.22em; text-transform: uppercase;
> 113	  font-weight: 500; padding: 18px 34px; border-radius: 999px;
> 114	  display: inline-flex; align-items: center; gap: 14px;
> 115	  cursor: pointer; border: 1px solid; transition: all .28s ease;
> 116	  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
> 117	}
> 118	.lp-cta-primary {
> 119	  border-color: var(--cyan);
> 120	  background: linear-gradient(180deg, rgba(0,242,255,0.22), rgba(0,242,255,0.06));
> 121	  color: var(--cyan);
> 122	  box-shadow: 0 0 28px rgba(0,242,255,0.22), inset 0 0 32px rgba(0,242,255,0.10);
> 123	}
> 124	.lp-cta-primary:hover {
> 125	  background: linear-gradient(180deg, rgba(0,242,255,0.38), rgba(0,242,255,0.12));
> 126	  box-shadow: 0 0 44px rgba(0,242,255,0.48), inset 0 0 36px rgba(0,242,255,0.16);
> 127	  transform: translateY(-1px);
> 128	}
> 129	.lp-cta-ghost {
> 130	  border-color: rgba(255,255,255,0.18);
> 131	  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
> 132	  color: var(--bone);
> 133	}
> 134	.lp-cta-ghost:hover { border-color: var(--cyan-line); color: var(--cyan); background: var(--cyan-veil); }
> 135	.lp-cta .arrow { transition: transform .28s ease; }
> 136	.lp-cta:hover .arrow { transform: translateX(6px); }
> 137	
> 138	/* ----------------------------- SECTION ----------------------------- */
> 139	.lp-section {
> 140	  position: relative; padding: 140px 8vw 120px;
> 141	}
> 142	.lp-section .num {
> 143	  font-family: var(--mono); font-size: 11px; letter-spacing: 0.32em;
> 144	  color: var(--bone-3); position: absolute; top: 110px; left: 8vw;
> 145	}
> 146	.lp-section .num::after {
> 147	  content: ""; display: inline-block; width: 60px; height: 1px; background: var(--silver-3);
> 148	  margin-left: 14px; vertical-align: middle;
> 149	}
> 150	.lp-h1 { font-family: var(--display); font-size: clamp(48px, 7.4vw, 120px); line-height: 0.94; letter-spacing: -0.028em; margin: 0 0 28px; text-wrap: balance; }
> 151	.lp-h2 { font-family: var(--display); font-size: clamp(36px, 5vw, 78px); line-height: 1; letter-spacing: -0.02em; margin: 0 0 24px; text-wrap: balance; }
> 152	.lp-h3 { font-family: var(--display); font-size: clamp(22px, 2.4vw, 36px); line-height: 1.12; margin: 0 0 12px; }
> 153	.lp-lede { font-family: var(--mono); font-size: clamp(14px, 1.05vw, 16px); line-height: 1.78; color: var(--bone-2); max-width: 58ch; }
> 154	.lp-eyebrow {
> 155	  display: inline-flex; align-items: center; gap: 14px; margin-bottom: 28px;
> 156	  font-family: var(--mono); font-size: 11px; letter-spacing: 0.28em; text-transform: uppercase; color: var(--cyan);
> 157	}
> 158	.lp-eyebrow::before { content: ""; width: 36px; height: 1px; background: var(--cyan); }
> 159	
> 160	/* Big chapter numeral background */
> 161	.lp-bignum {
> 162	  position: absolute; font-family: var(--display); font-style: italic;
> 163	  font-size: clamp(180px, 28vw, 460px); line-height: 0.82;
> 164	  color: rgba(255,255,255,0.035); user-select: none; pointer-events: none;
> 165	  letter-spacing: -0.04em;
> 166	}
> 167	
> 168	/* Trust strip — logos / signals */
> 169	.lp-trust-strip {
> 170	  border-top: 1px solid var(--silver-2);
> 171	  border-bottom: 1px solid var(--silver-2);
> 172	  padding: 32px 8vw;
> 173	  display: flex; justify-content: space-between; align-items: center; gap: 40px; flex-wrap: wrap;
> 174	  background: linear-gradient(180deg, rgba(255,255,255,0.012), transparent);
> 175	}
> 176	.lp-trust-strip .item {
> 177	  display: flex; align-items: center; gap: 12px;
> 178	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--bone-3);
> 179	}
> 180	.lp-trust-strip .item .v { color: var(--bone); font-family: var(--display); font-size: 28px; letter-spacing: -0.02em; }
> 181	.lp-trust-strip .item .v.gold { color: var(--gold); }
> 182	.lp-trust-strip .item .v.cyan { color: var(--cyan); }
> 183	
> 184	/* Pillar / card grid */
> 185	.lp-pillars { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
> 186	.lp-pillar {
> 187	  position: relative;
> 188	  padding: 32px 28px 36px;
> 189	  border-radius: 18px;
> 190	  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.008));
> 191	  border: 1px solid rgba(255,255,255,0.09);
> 192	  backdrop-filter: blur(20px) saturate(1.3);
> 193	  -webkit-backdrop-filter: blur(20px) saturate(1.3);
> 194	  box-shadow: inset 0 1px 0 rgba(255,255,255,0.10), 0 18px 50px rgba(0,0,0,0.35);
> 195	  overflow: hidden;
> 196	  transition: transform .35s ease, border-color .35s ease;
> 197	}
> 198	.lp-pillar:hover { transform: translateY(-4px); border-color: var(--cyan-line); }
> 199	.lp-pillar::before {
> 200	  content: ""; position: absolute; inset: 0; pointer-events: none;
> 201	  background: radial-gradient(120% 60% at 50% -10%, rgba(255,255,255,0.10), transparent 60%);
> 202	}
> 203	.lp-pillar .pill-num {
> 204	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.32em; color: var(--cyan); margin-bottom: 24px;
> 205	}
> 206	.lp-pillar .pill-icon {
> 207	  width: 56px; height: 56px; margin-bottom: 22px;
> 208	}
> 209	
> 210	/* Steps timeline */
> 211	.lp-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; position: relative; }
> 212	.lp-steps::before {
> 213	  content: ""; position: absolute; top: 32px; left: 0; right: 0; height: 1px;
> 214	  background: linear-gradient(90deg, transparent, var(--silver-3), var(--silver-3), transparent);
> 215	}
> 216	.lp-step {
> 217	  padding: 0 22px; position: relative;
> 218	}
> 219	.lp-step .knot {
> 220	  width: 14px; height: 14px; border-radius: 50%;
> 221	  background: var(--void); border: 1px solid var(--cyan);
> 222	  margin-bottom: 24px; position: relative; z-index: 2;
> 223	  box-shadow: 0 0 0 4px var(--void), 0 0 14px rgba(0,242,255,0.5);
> 224	}
> 225	.lp-step .ph {
> 226	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.28em; color: var(--bone-3); text-transform: uppercase; margin-bottom: 10px;
> 227	}
> 228	
> 229	/* Demo / terminal */
> 230	.lp-demo-grid { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 50px; align-items: center; }
> 231	.lp-term {
> 232	  font-family: var(--mono); font-size: 12px; line-height: 1.85;
> 233	  background: linear-gradient(180deg, rgba(0,0,0,0.7), rgba(0,0,0,0.5));
> 234	  border: 1px solid var(--silver-2);
> 235	  border-radius: 14px; padding: 28px 30px; color: var(--bone-2);
> 236	  position: relative; overflow: hidden;
> 237	}
> 238	.lp-term::before {
> 239	  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 32px;
> 240	  background: linear-gradient(180deg, rgba(255,255,255,0.06), transparent);
> 241	  border-bottom: 1px solid var(--silver-2);
> 242	}
> 243	.lp-term .head {
> 244	  position: relative; z-index: 1; display: flex; gap: 6px; margin: -10px -8px 14px;
> 245	  padding-bottom: 8px;
> 246	}
> 247	.lp-term .head .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--silver-4); }
> 248	.lp-term .head .label { margin-left: 14px; font-size: 10px; letter-spacing: 0.22em; color: var(--bone-4); text-transform: uppercase; }
> 249	.lp-term .pr { color: var(--cyan); }
> 250	.lp-term .ok { color: #6cf2c1; }
> 251	.lp-term .gl { color: var(--gold); }
> 252	.lp-term .nb { color: #b58cff; }
> 253	.lp-term .fg { color: var(--bone-4); }
> 254	
> 255	/* Results grid (big numbers) */
> 256	.lp-results { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; border-top: 1px solid var(--silver-2); }
> 257	.lp-results .cell {
> 258	  padding: 50px 28px; border-right: 1px solid var(--silver-2);
> 259	  position: relative;
> 260	}
> 261	.lp-results .cell:last-child { border-right: 0; }
> 262	.lp-results .cell .v {
> 263	  font-family: var(--display); font-size: clamp(56px, 6.4vw, 96px);
> 264	  line-height: 0.95; letter-spacing: -0.03em; margin-bottom: 12px;
> 265	}
> 266	.lp-results .cell .l {
> 267	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--bone-3);
> 268	}
> 269	.lp-results .cell.gold .v { color: var(--gold); font-style: italic; }
> 270	.lp-results .cell.cyan .v { color: var(--cyan); }
> 271	
> 272	/* Testimonials */
> 273	.lp-quotes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
> 274	.lp-quote {
> 275	  padding: 32px 30px; border-radius: 18px;
> 276	  background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01));
> 277	  border: 1px solid var(--silver-2);
> 278	  position: relative;
> 279	}
> 280	.lp-quote::before {
> 281	  content: "“"; position: absolute; top: -4px; left: 22px;
> 282	  font-family: var(--display); font-size: 70px; color: var(--gold); opacity: 0.55; line-height: 1;
> 283	}
> 284	.lp-quote .q {
> 285	  font-family: var(--display); font-style: italic; font-size: 22px; line-height: 1.34; color: var(--bone);
> 286	  margin: 18px 0 24px;
> 287	}
> 288	.lp-quote .author { display: flex; align-items: center; gap: 14px; }
> 289	.lp-quote .author .av {
> 290	  width: 42px; height: 42px; border-radius: 50%;
> 291	  background: linear-gradient(135deg, var(--cyan), var(--nebula));
> 292	  border: 1px solid var(--silver-3);
> 293	  display: grid; place-items: center; font-family: var(--mono); font-size: 12px; color: var(--void); font-weight: 600;
> 294	}
> 295	.lp-quote .author .meta { font-family: var(--mono); font-size: 11px; color: var(--bone-2); }
> 296	.lp-quote .author .meta .role { color: var(--bone-3); font-size: 9px; letter-spacing: 0.22em; text-transform: uppercase; margin-top: 2px; }
> 297	
> 298	/* Pricing */
> 299	.lp-pricing { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; align-items: stretch; }
> 300	.lp-plan {
> 301	  padding: 38px 30px 32px; border-radius: 22px;
> 302	  background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.008));
> 303	  border: 1px solid var(--silver-2);
> 304	  display: flex; flex-direction: column; position: relative; overflow: hidden;
> 305	}
> 306	.lp-plan.is-featured {
> 307	  border-color: var(--cyan);
> 308	  background: linear-gradient(180deg, rgba(0,242,255,0.07), rgba(0,242,255,0.015));
> 309	  box-shadow: 0 0 60px rgba(0,242,255,0.18), inset 0 1px 0 rgba(255,255,255,0.10);
> 310	  transform: scale(1.02);
> 311	}
> 312	.lp-plan .badge {
> 313	  position: absolute; top: 18px; right: 18px;
> 314	  font-family: var(--mono); font-size: 9px; letter-spacing: 0.22em; text-transform: uppercase;
> 315	  padding: 5px 10px; border-radius: 999px;
> 316	  background: var(--gold); color: var(--void); font-weight: 600;
> 317	}
> 318	.lp-plan .tier {
> 319	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.28em; text-transform: uppercase; color: var(--bone-3);
> 320	  margin-bottom: 12px;
> 321	}
> 322	.lp-plan .name { font-family: var(--display); font-size: 32px; line-height: 1; margin: 0 0 18px; }
> 323	.lp-plan .price { font-family: var(--display); font-size: 56px; letter-spacing: -0.03em; line-height: 1; margin-bottom: 6px; }
> 324	.lp-plan .price .ccy { font-size: 22px; color: var(--bone-3); margin-right: 6px; }
> 325	.lp-plan .price .per { display: block; font-family: var(--mono); font-size: 10px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--bone-3); margin-top: 6px; }
> 326	.lp-plan ul { list-style: none; padding: 0; margin: 26px 0 28px; flex: 1; display: flex; flex-direction: column; gap: 14px; }
> 327	.lp-plan ul li {
> 328	  font-family: var(--mono); font-size: 12px; line-height: 1.5; color: var(--bone-2);
> 329	  display: flex; gap: 10px;
> 330	}
> 331	.lp-plan ul li::before {
> 332	  content: "→"; color: var(--cyan); font-family: var(--mono); flex-shrink: 0;
> 333	}
> 334	.lp-plan ul li.muted { color: var(--bone-4); }
> 335	.lp-plan ul li.muted::before { content: "✗"; color: var(--bone-4); }
> 336	.lp-plan .price-foot {
> 337	  margin-top: auto; display: flex; flex-direction: column; gap: 12px;
> 338	}
> 339	
> 340	/* Founder */
> 341	.lp-founder { display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 60px; align-items: center; }
> 342	.lp-founder .photo {
> 343	  aspect-ratio: 4/5; border-radius: 18px; border: 1px solid var(--silver-2);
> 344	  background:
> 345	    radial-gradient(circle at 40% 30%, rgba(0,242,255,0.10), transparent 55%),
> 346	    repeating-linear-gradient(135deg, rgba(255,255,255,0.025) 0 1px, transparent 1px 12px),
> 347	    #050507;
> 348	  position: relative; overflow: hidden;
> 349	  display: grid; place-items: center;
> 350	}
> 351	.lp-founder .photo .placeholder {
> 352	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.32em; text-transform: uppercase; color: var(--bone-4);
> 353	}
> 354	.lp-founder .photo .corner-tag {
> 355	  position: absolute; top: 14px; left: 14px;
> 356	  font-family: var(--mono); font-size: 9px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--bone-3);
> 357	}
> 358	.lp-founder .photo .seal-tag {
> 359	  position: absolute; bottom: 14px; right: 14px;
> 360	  font-family: var(--mono); font-size: 9px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--gold);
> 361	}
> 362	
> 363	/* Guarantee */
> 364	.lp-guarantee {
> 365	  display: grid; grid-template-columns: auto 1fr; gap: 36px; align-items: center;
> 366	  padding: 44px 48px; border-radius: 22px;
> 367	  background: linear-gradient(180deg, rgba(212,175,55,0.08), rgba(212,175,55,0.02));
> 368	  border: 1px solid rgba(212,175,55,0.32);
> 369	  box-shadow: 0 0 60px rgba(212,175,55,0.10), inset 0 1px 0 rgba(255,255,255,0.06);
> 370	}
> 371	.lp-guarantee .seal {
> 372	  width: 110px; height: 110px; border-radius: 50%;
> 373	  border: 1px solid var(--gold);
> 374	  display: grid; place-items: center;
> 375	  background: radial-gradient(circle, rgba(212,175,55,0.18), transparent 70%);
> 376	  font-family: var(--display); font-style: italic; color: var(--gold);
> 377	  font-size: 36px; line-height: 1;
> 378	}
> 379	
> 380	/* FAQ */
> 381	.lp-faq { display: flex; flex-direction: column; gap: 0; border-top: 1px solid var(--silver-2); }
> 382	.lp-faq details {
> 383	  border-bottom: 1px solid var(--silver-2);
> 384	  padding: 28px 0; cursor: pointer;
> 385	}
> 386	.lp-faq details summary {
> 387	  list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 24px;
> 388	  font-family: var(--display); font-size: clamp(20px, 2vw, 28px); line-height: 1.2;
> 389	  color: var(--bone); cursor: pointer;
> 390	}
> 391	.lp-faq details summary::-webkit-details-marker { display: none; }
> 392	.lp-faq details summary .sign {
> 393	  font-family: var(--mono); font-size: 22px; color: var(--cyan); transition: transform .35s ease;
> 394	  width: 32px; height: 32px; display: grid; place-items: center;
> 395	  border: 1px solid var(--cyan-line); border-radius: 50%;
> 396	}
> 397	.lp-faq details[open] summary .sign { transform: rotate(45deg); }
> 398	.lp-faq details .a {
> 399	  font-family: var(--mono); font-size: 13px; line-height: 1.75; color: var(--bone-2);
> 400	  margin-top: 18px; max-width: 70ch;
> 401	}
> 402	
> 403	/* Final CTA */
> 404	.lp-final {
> 405	  position: relative; padding: 160px 8vw 160px;
> 406	  overflow: hidden; text-align: center;
> 407	  background: radial-gradient(ellipse 80% 70% at 50% 50%, rgba(0,242,255,0.10), transparent 60%), #000;
> 408	}
> 409	.lp-final h2 {
> 410	  font-family: var(--display); font-style: italic;
> 411	  font-size: clamp(48px, 9vw, 152px); line-height: 0.94; letter-spacing: -0.028em;
> 412	  margin: 0 0 36px; text-wrap: balance;
> 413	}
> 414	.lp-final .gold { color: var(--gold); }
> 415	.lp-final .cyan { color: var(--cyan); }
> 416	.lp-final .meta {
> 417	  display: flex; gap: 38px; justify-content: center; flex-wrap: wrap;
> 418	  margin-top: 56px;
> 419	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.28em; text-transform: uppercase; color: var(--bone-3);
> 420	}
> 421	.lp-final .meta b { color: var(--cyan); }
> 422	
> 423	/* Footer */
> 424	.lp-footer {
> 425	  border-top: 1px solid var(--silver-2);
> 426	  padding: 60px 8vw 38px;
> 427	  display: grid; gap: 40px;
> 428	}
> 429	.lp-footer .row {
> 430	  display: flex; justify-content: space-between; gap: 40px; flex-wrap: wrap;
> 431	}
> 432	.lp-footer .col h5 {
> 433	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.28em; text-transform: uppercase;
> 434	  color: var(--bone-3); margin: 0 0 14px; font-weight: 500;
> 435	}
> 436	.lp-footer .col a {
> 437	  display: block; font-family: var(--mono); font-size: 12px; color: var(--bone-2);
> 438	  text-decoration: none; padding: 4px 0; transition: color .2s;
> 439	}
> 440	.lp-footer .col a:hover { color: var(--cyan); }
> 441	.lp-footer .bottom {
> 442	  display: flex; justify-content: space-between; gap: 20px; align-items: center; flex-wrap: wrap;
> 443	  padding-top: 32px; border-top: 1px solid var(--silver-2);
> 444	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--bone-4);
> 445	}
> 446	
> 447	/* Reveal helpers */
> 448	.lp-reveal { will-change: transform, opacity; }
> 449	
> 450	/* ----------------------------- VISION PIN (Championship Offer) ----------------------------- */
> 451	.lp-vision {
> 452	  position: relative;
> 453	  /* Height = pin duration. 220vh ≈ 110vh per act for 3 acts (with overlap). */
> 454	  height: 280vh;
> 455	  background: linear-gradient(180deg, #000 0%, #060608 50%, #000 100%);
> 456	}
> 457	.lp-vision-pin {
> 458	  position: relative;
> 459	  height: 100vh;
> 460	  overflow: hidden;
> 461	  display: grid;
> 462	  place-items: center;
> 463	}
> 464	.lp-vision-ambient {
> 465	  position: absolute; inset: 0; pointer-events: none;
> 466	  background:
> 467	    radial-gradient(ellipse 70% 60% at 50% 50%, rgba(0,242,255,0.10), transparent 60%),
> 468	    radial-gradient(ellipse 50% 40% at 50% 10%, rgba(212,175,55,0.06), transparent 60%);
> 469	}
> 470	.lp-vision-stage {
> 471	  position: relative; z-index: 2; padding: 0 6vw; width: 100%; max-width: 1280px;
> 472	  text-align: center;
> 473	}
> 474	.lp-vision-acts {
> 475	  position: relative; min-height: 56vh; display: grid; place-items: center;
> 476	}
> 477	.lp-vision-act {
> 478	  position: absolute; inset: 0;
> 479	  display: grid; place-items: center;
> 480	  font-family: var(--display);
> 481	  font-size: clamp(28px, 4.4vw, 64px);
> 482	  line-height: 1.18; letter-spacing: -0.018em;
> 483	  color: var(--bone);
> 484	  opacity: 0;
> 485	  margin: 0; max-width: 1020px;
> 486	  margin-left: auto; margin-right: auto;
> 487	  text-wrap: balance;
> 488	}
> 489	.lp-vision-act[data-vision-act="0"] { opacity: 1; }
> 490	.lp-vision-floor {
> 491	  margin-top: 56px;
> 492	}
> 493	.lp-vision-progress {
> 494	  display: inline-flex; align-items: center; gap: 14px;
> 495	  padding: 12px 22px; border-radius: 999px;
> 496	  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
> 497	  border: 1px solid var(--silver-2);
> 498	  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
> 499	}
> 500	.lp-vision-progress .dot {
> 501	  width: 8px; height: 8px; border-radius: 50%;
> 502	  background: var(--bone-4); transition: background .35s, box-shadow .35s, transform .35s;
> 503	}
> 504	.lp-vision-progress .dot.is-active {
> 505	  background: var(--cyan); box-shadow: 0 0 12px rgba(0,242,255,0.7); transform: scale(1.3);
> 506	}
> 507	.lp-vision-progress .dot.is-done { background: var(--bone-2); }
> 508	.lp-vision-progress .bar { width: 32px; height: 1px; background: var(--silver-3); }
> 509	
> 510	/* ----------------------------- MARQUEE DIVIDER ----------------------------- */
> 511	.lp-marquee-wrap {
> 512	  position: relative; padding: 30px 0;
> 513	  border-top: 1px solid var(--silver-2);
> 514	  border-bottom: 1px solid var(--silver-2);
> 515	  overflow: hidden;
> 516	  background: #000;
> 517	}
> 518	.lp-marquee {
> 519	  display: flex; gap: 70px;
> 520	  font-family: var(--display); font-style: italic;
> 521	  font-size: clamp(52px, 7.4vw, 132px); line-height: 1;
> 522	  white-space: nowrap; letter-spacing: -0.03em;
> 523	  color: rgba(255,255,255,0.06);
> 524	}
> 525	.lp-marquee span { flex-shrink: 0; }
> 526	.lp-marquee em { font-style: normal; color: var(--gold); opacity: 0.4; }
> 527	
> 528	/* ----------------------------- CHAMPIONSHIP OFFER STAGE ----------------------------- */
> 529	.lp-offer-stage {
> 530	  position: relative;
> 531	  padding: 160px 8vw 140px;
> 532	  background: radial-gradient(ellipse 100% 60% at 50% 10%, rgba(0,242,255,0.05), transparent 60%), #000;
> 533	}
> 534	.lp-offer-hd { max-width: 920px; margin-bottom: 56px; }
> 535	
> 536	/* Scarcity bar */
> 537	.lp-scarcity {
> 538	  margin-bottom: 56px; padding: 22px 28px;
> 539	  border-radius: 14px;
> 540	  background: linear-gradient(180deg, rgba(212,175,55,0.08), rgba(212,175,55,0.02));
> 541	  border: 1px solid rgba(212,175,55,0.28);
> 542	  box-shadow: 0 0 40px rgba(212,175,55,0.08), inset 0 1px 0 rgba(255,255,255,0.06);
> 543	}
> 544	.lp-scarcity-row {
> 545	  display: flex; gap: 14px; align-items: center; margin-bottom: 14px;
> 546	  font-family: var(--mono); font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--bone-2);
> 547	  flex-wrap: wrap;
> 548	}
> 549	.lp-scarcity-row .dot {
> 550	  width: 9px; height: 9px; border-radius: 50%; background: var(--gold);
> 551	  box-shadow: 0 0 12px var(--gold);
> 552	}
> 553	.lp-scarcity-row .lbl { color: var(--gold); }
> 554	.lp-scarcity-row .sep { color: var(--bone-4); }
> 555	.lp-scarcity-row .count { color: var(--bone); font-family: var(--display); font-style: italic; font-size: 18px; letter-spacing: -0.01em; text-transform: none; }
> 556	.lp-scarcity-row .count .of { color: var(--bone-3); font-size: 14px; }
> 557	.lp-scarcity-bar {
> 558	  height: 4px; border-radius: 999px;
> 559	  background: rgba(255,255,255,0.06); overflow: hidden;
> 560	}
> 561	.lp-scarcity-bar .fill {
> 562	  height: 100%; background: linear-gradient(90deg, var(--gold), var(--cyan));
> 563	  box-shadow: 0 0 14px rgba(0,242,255,0.4);
> 564	  transform-origin: left center;
> 565	}
> 566	
> 567	/* Offer close — stack + finale */
> 568	.lp-offer-close {
> 569	  margin-top: 80px;
> 570	  display: grid; grid-template-columns: 0.95fr 1.05fr; gap: 60px; align-items: center;
> 571	}
> 572	.lp-offer-stack {
> 573	  border-top: 1px solid var(--silver-2);
> 574	}
> 575	.lp-offer-stack .stack-row {
> 576	  display: grid; grid-template-columns: 140px 1fr; gap: 24px;
> 577	  padding: 22px 0; border-bottom: 1px solid var(--silver-2);
> 578	  align-items: center;
> 579	}
> 580	.lp-offer-stack .stack-row .k {
> 581	  font-family: var(--mono); font-size: 10px; letter-spacing: 0.28em; text-transform: uppercase; color: var(--bone-3);
> 582	}
> 583	.lp-offer-stack .stack-row .v {
> 584	  font-family: var(--mono); font-size: 13px; line-height: 1.6; color: var(--bone-2);
> 585	}
> 586	.lp-offer-finale {
> 587	  text-align: left;
> 588	  padding: 40px;
> 589	  border-radius: 22px;
> 590	  background:
> 591	    radial-gradient(ellipse 80% 70% at 50% 100%, rgba(0,242,255,0.10), transparent 60%),
> 592	    linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.008));
> 593	  border: 1px solid rgba(0,242,255,0.32);
> 594	  box-shadow: 0 0 60px rgba(0,242,255,0.14), inset 0 1px 0 rgba(255,255,255,0.10);
> 595	}
> 596	
> 597	/* Subtle shimmer on featured plan to draw the eye */
> 598	@keyframes lp-shimmer {
> 599	  0%, 100% { box-shadow: 0 0 50px rgba(0,242,255,0.16), inset 0 1px 0 rgba(255,255,255,0.10); }
> 600	  50%      { box-shadow: 0 0 80px rgba(0,242,255,0.30), inset 0 1px 0 rgba(255,255,255,0.14); }
> 601	}
> 602	.lp-plan.is-featured { animation: lp-shimmer 3.4s ease-in-out infinite; }
> 603	
> 604	/* Counter numerals tighten with tabular nums while animating */
> 605	[data-counter] { font-variant-numeric: tabular-nums; }
> 606	
> 607	/* ----------------------------- RESPONSIVE ----------------------------- */
> 608	@media (max-width: 1100px) {
> 609	  .lp-section { padding: 110px 6vw 90px; }
> 610	  .lp-section .num { left: 6vw; }
> 611	  .lp-pillars { grid-template-columns: 1fr; gap: 18px; }
> 612	  .lp-steps { grid-template-columns: 1fr 1fr; gap: 40px 0; }
> 613	  .lp-steps::before { display: none; }
> 614	  .lp-demo-grid { grid-template-columns: 1fr; gap: 32px; }
> 615	  .lp-results { grid-template-columns: 1fr 1fr; }
> 616	  .lp-results .cell:nth-child(2) { border-right: 0; }
> 617	  .lp-results .cell { border-bottom: 1px solid var(--silver-2); }
> 618	  .lp-quotes { grid-template-columns: 1fr; gap: 16px; }
> 619	  .lp-pricing { grid-template-columns: 1fr; }
> 620	  .lp-plan.is-featured { transform: none; }
> 621	  .lp-founder { grid-template-columns: 1fr; gap: 32px; }
> 622	  .lp-offer-close { grid-template-columns: 1fr; gap: 32px; }
> 623	  .lp-offer-stage { padding: 110px 6vw 100px; }
> 624	  .lp-vision { height: 240vh; }
> 625	}
> 626	@media (max-width: 760px) {
> 627	  .lp-cursor, .lp-cursor-ring { display: none !important; }
> 628	  html, body { cursor: auto !important; }
> 629	  .lp-nav { padding: 12px 16px; }
> 630	  .lp-nav .links { display: none; }
> 631	  .lp-section { padding: 90px 5vw 60px; }
> 632	  .lp-section .num { left: 5vw; top: 60px; }
> 633	  .lp-hero h1 { font-size: clamp(42px, 12vw, 80px); }
> 634	  .lp-hero .trust { gap: 16px; flex-direction: column; }
> 635	  .lp-results { grid-template-columns: 1fr; }
> 636	  .lp-results .cell { border-right: 0; border-bottom: 1px solid var(--silver-2); }
> 637	  .lp-steps { grid-template-columns: 1fr; }
> 638	  .lp-guarantee { grid-template-columns: 1fr; padding: 28px 24px; }
> 639	  .lp-cta { padding: 15px 24px; font-size: 11px; letter-spacing: 0.18em; }
> 640	  .lp-final h2 { font-size: clamp(40px, 13vw, 64px); }
> 641	  .lp-vision-act { font-size: clamp(22px, 6vw, 36px); }
> 642	  .lp-offer-stack .stack-row { grid-template-columns: 1fr; gap: 8px; padding: 18px 0; }
> 643	  .lp-offer-finale { padding: 28px 22px; }
> 644	  .lp-offer-stage { padding: 80px 5vw 80px; }
> 645	  .lp-marquee { font-size: clamp(36px, 13vw, 72px) !important; }
> 646	}
> 647	
> 648	/* --- Hero backdrop (CSS/SVG approximation of HeroThree WebGL; scoped) --- */
> 649	.mcorch-lp .lp-hero-backdrop { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
> 650	.mcorch-lp .lp-hero-backdrop svg { position: absolute; inset: 0; width: 100%; height: 100%; }
> 651	.mcorch-lp .lp-wave { transform-origin: center; animation: lp-wave-drift 14s ease-in-out infinite alternate; }
> 652	@keyframes lp-wave-drift {
> 653	  0%   { transform: translateY(-14px) scaleY(0.96); }
> 654	  100% { transform: translateY(14px)  scaleY(1.05); }
> 655	}
> 656	@media (prefers-reduced-motion: reduce) { .mcorch-lp .lp-wave { animation: none; } }
> 657	
> ```

## 🤖 Claude *(23:29:25)*


## 🤖 Claude *(23:29:36)*

Tenho tudo o que preciso. Mapeei inclusive as lacunas que o corte deixou: o CSS rico existe todo, mas os efeitos que dependiam de GSAP **nunca foram portados** — a marquee não tem `@keyframes`, as palavras do hero não animam sozinhas, e a seção "visão" (280vh pinada, 3 atos) só mostra o ato 0 sem JS. Vou entregar tudo isso em CSS/JS puro.

**Plano de execução** (ORO: Operator=eu · Reviewer=você · Owner=você — landing pública; sem migration, sem BoK gate — é refino de feature documentada):

1. **`ConstellationField.tsx`** — porta a explosão de partículas do `particles.jsx` para React/TS **com ignição de load** (partículas nascem do centro e florescem para fora, das mais próximas às distantes = a "explosão orquestrada"), DPR-aware, pausa fora da viewport, respeita `prefers-reduced-motion`.
2. **`landing-motion.ts`** — IntersectionObserver que revela `.lp-reveal` com stagger em ritmo de leitura (~80ms, sutil) + scroll-scrub dos 3 atos da visão + choreography do hero.
3. **CSS** (append em `landing.css`) — estado inicial do reveal (aditivo, nunca esconde sem JS), animação das palavras do hero, `@keyframes` da marquee, guardas de reduced-motion.
4. **Restaurar as 14 seções** com sua regra: forma rica do original, **texto honesto** (sem 3.4×/68%/17-24 vagas/preços R$ — reaproveito a cópia honesta que você já aprovou).
5. **Verificar**: tsc 0 · build · browser real (preview + sessão) · Vision QA.

Começando pela explosão:

## 🤖 Claude *(23:30:19)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/ConstellationField.tsx",
  "content": "// MCORCH hero constellation field \u2014 the real particle explosion.\n// Faithful React/TS port of miv/particles.jsx `ConstellationCanvas`, PLUS a\n// load \"ignition\": particles bloom outward from the core (nearest first), so the\n// hero opens as an orchestrated explosion instead of appearing all at once.\n// Pure canvas \u2014 no libs. DPR-capped, RAF paused offscreen/hidden, reduced-motion\n// renders a calm static field (no ignition, no drift).\nimport { useEffect, useRef } from 'react';\n\ntype Role = 'cyan' | 'nebula' | 'gold';\ninterface Node {\n  ox: number; oy: number;   // home position (bloom target)\n  x: number; y: number;     // live position\n  vx: number; vy: number;\n  r: number;\n  phase: number; freq: number;\n  role: Role; imp: number;\n  ignite: number;           // 0..1 point on the ignition timeline this node lights at\n}\n\nconst easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);\nconst COLOR: Record<Role, string> = {\n  cyan: '0, 242, 255',\n  nebula: '140, 90, 255',\n  gold: '212, 175, 55',\n};\n\nconst IGNITION_MS = 1650; // full bloom duration\n\nexport default function ConstellationField({ className }: { className?: string }) {\n  const ref = useRef<HTMLCanvasElement | null>(null);\n  const mouse = useRef({ x: -9999, y: -9999, active: false });\n\n  useEffect(() => {\n    const c = ref.current;\n    if (!c) return;\n    const ctx = c.getContext('2d', { alpha: true, desynchronized: true });\n    if (!ctx) return;\n\n    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n    const dprCap = Math.min(window.devicePixelRatio || 1, 1.5);\n    let w = 0, h = 0;\n    let nodes: Node[] = [];\n    let visible = false, running = false;\n    let t0 = performance.now();\n    const born = performance.now();\n\n    const build = () => {\n      const N = Math.max(60, Math.min(200, Math.floor((w * h) / 9000)));\n      const cx = w / 2, cy = h * 0.46;\n      const maxD = Math.hypot(w, h) * 0.5;\n      // 5 soft clusters so the field reads as a constellation, not noise.\n      const clusters = Array.from({ length: 5 }, () => ({\n        x: Math.random() * w, y: Math.random() * h, r: 80 + Math.random() * 160,\n      }));\n      nodes = [];\n      for (let i = 0; i < N; i++) {\n        let x: number, y: number;\n        if (Math.random() < 0.7) {\n          const cl = clusters[(Math.random() * clusters.length) | 0];\n          const a = Math.random() * Math.PI * 2;\n          const r = Math.pow(Math.random(), 1.6) * cl.r;\n          x = cl.x + Math.cos(a) * r;\n          y = cl.y + Math.sin(a) * r;\n        } else {\n          x = Math.random() * w; y = Math.random() * h;\n        }\n        const tier = Math.random();\n        const role: Role = tier > 0.95 ? 'gold' : tier > 0.82 ? 'nebula' : 'cyan';\n        const imp = tier > 0.95 ? 3 : tier > 0.82 ? 2 : 1;\n        // Nearest-to-core nodes ignite first \u2192 the bloom radiates outward.\n        const d = Math.hypot(x - cx, y - cy);\n        nodes.push({\n          ox: x, oy: y, x, y,\n          vx: (Math.random() - 0.5) * 0.06,\n          vy: (Math.random() - 0.5) * 0.06,\n          r: 0.6 + Math.pow(Math.random(), 2) * 1.6 * imp,\n          phase: Math.random() * Math.PI * 2,\n          freq: 0.3 + Math.random() * 0.8,\n          role, imp,\n          ignite: Math.min(0.85, (d / maxD) * 0.7 + Math.random() * 0.12),\n        });\n      }\n    };\n\n    const resize = () => {\n      const cr = c.getBoundingClientRect();\n      const parent = c.parentElement;\n      const pr = parent ? parent.getBoundingClientRect() : cr;\n      const nw = Math.max(1, Math.floor(cr.width || pr.width));\n      const nh = Math.max(1, Math.floor(cr.height || pr.height));\n      if (nw === w && nh === h) return;\n      w = nw; h = nh;\n      c.width = w * dprCap; c.height = h * dprCap;\n      c.style.display = 'block';\n      ctx.setTransform(dprCap, 0, 0, dprCap, 0, 0);\n      build();\n    };\n\n    const draw = (t: number, dt: number) => {\n      const cx = w / 2, cy = h * 0.46;\n      const p = reduce ? 1 : easeOutCubic(Math.min(1, (performance.now() - born) / IGNITION_MS));\n\n      ctx.clearRect(0, 0, w, h);\n\n      // Core flash during the first third of the ignition (the \"explosion\").\n      if (!reduce && p < 0.55) {\n        const flash = (1 - p / 0.55);\n        const fr = Math.max(w, h) * (0.05 + p * 0.5);\n        const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, fr);\n        g.addColorStop(0, `rgba(212, 175, 55, ${0.35 * flash})`);\n        g.addColorStop(0.4, `rgba(0, 242, 255, ${0.14 * flash})`);\n        g.addColorStop(1, 'rgba(0, 0, 0, 0)');\n        ctx.fillStyle = g;\n        ctx.fillRect(0, 0, w, h);\n      }\n\n      // Per-node bloom progress: eased entry after each node's ignite point.\n      const local = (n: Node) => {\n        if (p >= 1) return 1;\n        const span = 1 - n.ignite;\n        return span <= 0 ? 1 : easeOutCubic(Math.max(0, Math.min(1, (p - n.ignite) / span)));\n      };\n\n      // Filaments (fade in with the global bloom).\n      const famAlpha = Math.max(0, (p - 0.35) / 0.65);\n      if (famAlpha > 0.01) {\n        const max = 95;\n        for (let i = 0; i < nodes.length; i++) {\n          const a = nodes[i];\n          if (local(a) < 0.5) continue;\n          for (let j = i + 1; j < nodes.length; j++) {\n            const b = nodes[j];\n            if (local(b) < 0.5) continue;\n            const dx = a.x - b.x, dy = a.y - b.y;\n            const d2 = dx * dx + dy * dy;\n            if (d2 < max * max) {\n              const k = 1 - Math.sqrt(d2) / max;\n              ctx.strokeStyle = `rgba(0, 242, 255, ${k * k * 0.22 * famAlpha})`;\n              ctx.lineWidth = 0.6;\n              ctx.beginPath();\n              ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();\n            }\n          }\n        }\n      }\n\n      // Mouse-reactive gold filaments (only once bloomed).\n      if (p > 0.9 && mouse.current.active) {\n        const mx = mouse.current.x, my = mouse.current.y;\n        for (const n of nodes) {\n          const dx = n.x - mx, dy = n.y - my;\n          const d = Math.hypot(dx, dy);\n          if (d < 160) {\n            const k = 1 - d / 160;\n            ctx.strokeStyle = `rgba(212, 175, 55, ${k * 0.38})`;\n            ctx.lineWidth = 0.6;\n            ctx.beginPath();\n            ctx.moveTo(mx, my); ctx.lineTo(n.x, n.y); ctx.stroke();\n          }\n        }\n      }\n\n      for (const n of nodes) {\n        const lp = local(n);\n        if (lp <= 0) continue;\n        // Bloom: interpolate from core to home as this node lights up.\n        const bx = cx + (n.ox - cx) * lp;\n        const by = cy + (n.oy - cy) * lp;\n        if (p >= 1 && !reduce) {\n          // settled drift + soft return home\n          n.x += n.vx; n.y += n.vy;\n          n.x += (n.ox - n.x) * 0.0008; n.y += (n.oy - n.y) * 0.0008;\n          if (n.x < -20) n.x = w + 20; if (n.x > w + 20) n.x = -20;\n          if (n.y < -20) n.y = h + 20; if (n.y > h + 20) n.y = -20;\n        } else {\n          n.x = bx; n.y = by;\n        }\n\n        const twinkle = 0.6 + 0.4 * Math.sin(t * n.freq * 2 + n.phase);\n        const color = COLOR[n.role];\n        const a = lp * twinkle;\n        // halo\n        const haloR = n.r * (4 + n.imp * 1.5) * twinkle;\n        const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, haloR);\n        grad.addColorStop(0, `rgba(${color}, ${0.45 * a})`);\n        grad.addColorStop(0.4, `rgba(${color}, ${0.12 * a})`);\n        grad.addColorStop(1, `rgba(${color}, 0)`);\n        ctx.fillStyle = grad;\n        ctx.beginPath(); ctx.arc(n.x, n.y, haloR, 0, Math.PI * 2); ctx.fill();\n        // core\n        ctx.fillStyle = `rgba(${color}, ${0.9 * a})`;\n        ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2); ctx.fill();\n        // gold/nebula hairline cross\n        if (n.imp >= 2 && lp > 0.6) {\n          ctx.strokeStyle = `rgba(${color}, ${0.5 * a})`;\n          ctx.lineWidth = 0.5;\n          const cr = n.r * 4;\n          ctx.beginPath();\n          ctx.moveTo(n.x - cr, n.y); ctx.lineTo(n.x + cr, n.y);\n          ctx.moveTo(n.x, n.y - cr); ctx.lineTo(n.x, n.y + cr);\n          ctx.stroke();\n        }\n      }\n      void dt;\n    };\n\n    const loop = (t: number) => {\n      if (!running) { return; }\n      const dt = (t - t0) / 1000; t0 = t;\n      draw(t / 1000, dt);\n      // Keep animating until bloom completes even if reduced (one frame is enough there).\n      raf = requestAnimationFrame(loop);\n    };\n    let raf = 0;\n    const start = () => {\n      if (running) return;\n      running = true; t0 = performance.now();\n      raf = requestAnimationFrame(loop);\n      if (reduce) { draw(0, 0); running = false; } // static single frame\n    };\n    const stop = () => { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; };\n\n    const ro = new ResizeObserver(resize);\n    ro.observe(c.parentElement || c);\n    ro.observe(c);\n    resize();\n\n    const io = new IntersectionObserver(\n      ([e]) => { visible = e.isIntersecting; if (visible && !document.hidden) start(); else stop(); },\n      { rootMargin: '200px 0px' },\n    );\n    io.observe(c);\n    const onVis = () => { if (document.hidden) stop(); else if (visible) start(); };\n    document.addEventListener('visibilitychange', onVis);\n\n    const onMove = (e: MouseEvent) => {\n      const r = c.getBoundingClientRect();\n      mouse.current.x = e.clientX - r.left;\n      mouse.current.y = e.clientY - r.top;\n      mouse.current.active = true;\n    };\n    const onLeave = () => { mouse.current.active = false; };\n    c.addEventListener('mousemove', onMove);\n    c.addEventListener('mouseleave', onLeave);\n\n    return () => {\n      stop(); ro.disconnect(); io.disconnect();\n      document.removeEventListener('visibilitychange', onVis);\n      c.removeEventListener('mousemove', onMove);\n      c.removeEventListener('mouseleave', onLeave);\n    };\n  }, []);\n\n  return <canvas ref={ref} className={className} aria-hidden=\"true\" />;\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/ConstellationField.tsx (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:30:49)*


## 🤖 Claude *(23:30:50)*

Agora o motor de movimento (reveal orquestrado + scrub da visão), em JS puro:

## 🤖 Claude *(23:31:05)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/landing-motion.ts",
  "content": "// MCORCH landing \u2014 motion orchestration (no GSAP; IntersectionObserver + rAF).\n// Reveals `.lp-reveal` at reading pace (subtle rise+fade, per-group stagger),\n// plays the hero on load, and scrubs the pinned 3-act \"vision\" by scroll.\n// Everything is additive: with JS off or reduced-motion, content is fully visible.\nimport { useEffect } from 'react';\n\nconst REVEAL_STEP_MS = 90; // gap between staggered siblings \u2014 reading cadence\n\nexport function useLandingMotion() {\n  useEffect(() => {\n    const root = document.querySelector<HTMLElement>('.mcorch-lp');\n    if (!root) return;\n\n    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n    root.classList.add('reveal-ready');\n\n    // --- Reveal: stagger each `.lp-reveal` within its own group ------------\n    const reveals = Array.from(root.querySelectorAll<HTMLElement>('.lp-reveal'));\n    const groupCounter = new Map<Element, number>();\n    for (const el of reveals) {\n      const group = el.closest('section, footer, .lp-offer-stage, .lp-vision-stage') || root;\n      const i = groupCounter.get(group) ?? 0;\n      groupCounter.set(group, i + 1);\n      el.style.setProperty('--i', String(i));\n    }\n\n    if (reduce) {\n      reveals.forEach((el) => el.classList.add('is-in'));\n      root.querySelector('.lp-hero')?.classList.add('is-in');\n      // still wire the vision scrub below so acts remain readable\n    } else {\n      const io = new IntersectionObserver(\n        (entries) => {\n          for (const e of entries) {\n            if (e.isIntersecting) {\n              e.target.classList.add('is-in');\n              io.unobserve(e.target);\n            }\n          }\n        },\n        { threshold: 0.15, rootMargin: '0px 0px -8% 0px' },\n      );\n      reveals.forEach((el) => io.observe(el));\n\n      // Hero plays immediately on load (above the fold) \u2014 words + children cascade.\n      const hero = root.querySelector('.lp-hero');\n      const heroRaf = requestAnimationFrame(() => hero?.classList.add('is-in'));\n\n      // --- Vision scrub: map scroll through `.lp-vision` to 3 acts ---------\n      const vision = root.querySelector<HTMLElement>('.lp-vision');\n      const acts = vision ? Array.from(vision.querySelectorAll<HTMLElement>('.lp-vision-act')) : [];\n      const dots = vision ? Array.from(vision.querySelectorAll<HTMLElement>('[data-dot]')) : [];\n      let ticking = false;\n      const applyVision = () => {\n        ticking = false;\n        if (!vision || !acts.length) return;\n        const rect = vision.getBoundingClientRect();\n        const scrollable = rect.height - window.innerHeight;\n        const progress = scrollable > 0 ? Math.min(1, Math.max(0, -rect.top / scrollable)) : 0;\n        const active = Math.min(acts.length - 1, Math.floor(progress * acts.length + 0.0001));\n        acts.forEach((a, i) => { a.style.opacity = i === active ? '1' : '0'; });\n        dots.forEach((d, i) => {\n          d.classList.toggle('is-active', i === active);\n          d.classList.toggle('is-done', i < active);\n        });\n      };\n      const onScroll = () => {\n        if (!ticking) { ticking = true; requestAnimationFrame(applyVision); }\n      };\n      if (vision) {\n        window.addEventListener('scroll', onScroll, { passive: true });\n        window.addEventListener('resize', onScroll, { passive: true });\n        applyVision();\n      }\n\n      return () => {\n        io.disconnect();\n        cancelAnimationFrame(heroRaf);\n        window.removeEventListener('scroll', onScroll);\n        window.removeEventListener('resize', onScroll);\n      };\n    }\n  }, []);\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/landing-motion.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:31:33)*


## 🤖 Claude *(23:31:34)*

CSS de orquestração (reveal aditivo, palavras do hero, marquee, pin sticky da visão, reduced-motion):

## 🤖 Claude *(23:31:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ncat >> src/styles/mcorch/landing.css << 'CSSEOF'\n\n/* ============================================================================\n   MOTION ORCHESTRATION \u2014 reveal + hero load + marquee + vision pin (no GSAP).\n   Additive: hides only once JS adds `.reveal-ready`; reduced-motion opts out.\n   ============================================================================ */\n.mcorch-lp.reveal-ready .lp-reveal { opacity: 0; transform: translateY(20px); }\n.mcorch-lp .lp-reveal.is-in {\n  opacity: 1; transform: none;\n  transition: opacity .8s cubic-bezier(.22,.61,.36,1), transform .8s cubic-bezier(.22,.61,.36,1);\n  transition-delay: calc(var(--i, 0) * 90ms);\n}\n\n/* Hero \u2014 masked word rise, played after the ignition kicks in. */\n.mcorch-lp.reveal-ready .lp-hero h1 .word > span { transform: translateY(112%); }\n.mcorch-lp .lp-hero.is-in h1 .word > span {\n  transform: none;\n  transition: transform 1s cubic-bezier(.22,.61,.36,1);\n  transition-delay: calc(var(--wi, 0) * 105ms + 320ms);\n}\n.mcorch-lp.reveal-ready .lp-hero .lp-eyebrow,\n.mcorch-lp.reveal-ready .lp-hero p.sub,\n.mcorch-lp.reveal-ready .lp-hero .cta-row,\n.mcorch-lp.reveal-ready .lp-hero .trust,\n.mcorch-lp.reveal-ready .lp-hero-scroll-hint { opacity: 0; transform: translateY(16px); }\n.mcorch-lp .lp-hero.is-in .lp-eyebrow,\n.mcorch-lp .lp-hero.is-in p.sub,\n.mcorch-lp .lp-hero.is-in .cta-row,\n.mcorch-lp .lp-hero.is-in .trust,\n.mcorch-lp .lp-hero.is-in .lp-hero-scroll-hint {\n  opacity: 1; transform: none;\n  transition: opacity .9s ease, transform .9s cubic-bezier(.22,.61,.36,1);\n}\n.mcorch-lp .lp-hero.is-in .lp-eyebrow { transition-delay: .15s; }\n.mcorch-lp .lp-hero.is-in p.sub { transition-delay: .85s; }\n.mcorch-lp .lp-hero.is-in .cta-row { transition-delay: 1s; }\n.mcorch-lp .lp-hero.is-in .trust { transition-delay: 1.15s; }\n.mcorch-lp .lp-hero.is-in .lp-hero-scroll-hint { transition-delay: 1.35s; }\n\n/* Vision \u2014 sticky pin so the 3 acts scrub across the tall scroll (was GSAP pin). */\n.mcorch-lp .lp-vision-pin { position: sticky; top: 0; }\n.mcorch-lp .lp-vision-act { transition: opacity .6s ease; }\n\n/* Marquee \u2014 pure-CSS drift (band is duplicated in markup \u2192 -50% loops seamless). */\n.mcorch-lp .lp-marquee { animation: lp-marquee-drift 38s linear infinite; }\n@keyframes lp-marquee-drift { from { transform: translateX(0); } to { transform: translateX(-50%); } }\n\n@media (prefers-reduced-motion: reduce) {\n  .mcorch-lp .lp-reveal,\n  .mcorch-lp .lp-hero .lp-eyebrow, .mcorch-lp .lp-hero p.sub,\n  .mcorch-lp .lp-hero .cta-row, .mcorch-lp .lp-hero .trust,\n  .mcorch-lp .lp-hero-scroll-hint { opacity: 1 !important; transform: none !important; }\n  .mcorch-lp .lp-hero h1 .word > span { transform: none !important; }\n  .mcorch-lp .lp-marquee { animation: none; }\n}\nCSSEOF\necho \"appended $(wc -l < src/styles/mcorch/landing.css) linhas totais em landing.css\"",
  "description": "Append motion orchestration CSS to landing.css"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> appended 710 linhas totais em landing.css
> ```

## 🤖 Claude *(23:32:51)*


## 🤖 Claude *(23:32:53)*

Agora a peça central — as 14 seções ricas com a regra de honestidade. Reaproveito a cópia honesta já aprovada e removo todo número/preço/escassez fabricado, mantendo a forma e os efeitos do original:

## 🤖 Claude *(23:34:53)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/LandingV2Sections.tsx",
  "content": "// MCORCH Landing V2 \u2014 full rich sections, honest content.\n// Form restored from the original design_handoff (14 sections + effects); content\n// kept truthful per Sovereign directive (2026-07-03): NO fabricated metrics,\n// scarcity or shelf prices. Visual richness + orchestrated motion; honest copy.\n// Motion lives in landing-motion.ts (reveal/hero/vision); the hero explosion is\n// ConstellationField. Brand tokens: src/styles/mcorch/system.css.\nimport type { CSSProperties } from 'react';\nimport { Link } from 'react-router-dom';\nimport { Wordmark, SigilMark, Cta, PillarIcon } from './Brand';\nimport ConstellationField from './ConstellationField';\n\nconst card: CSSProperties = {\n  display: 'grid',\n  gridTemplateColumns: '120px 1fr',\n  gap: 24,\n  alignItems: 'baseline',\n  padding: '22px 26px',\n  borderRadius: 14,\n  border: '1px solid var(--silver-2)',\n  background: 'linear-gradient(180deg, rgba(255,255,255,0.025), rgba(255,255,255,0.005))',\n};\n\n// CSS custom-prop helper (typed escape hatch for --wi / --i inline vars).\nconst cssVar = (vars: Record<string, string | number>): CSSProperties => vars as CSSProperties;\n\n// ---------------------------------------------------------------- NAV\nexport const Nav = () => (\n  <header className=\"lp-nav\" id=\"lp-nav\">\n    <a href=\"#top\" style={{ display: 'flex', alignItems: 'center', gap: 14, textDecoration: 'none' }}>\n      <SigilMark />\n      <Wordmark size={13} />\n    </a>\n    <nav className=\"links\">\n      <a href=\"#orquestra\">A Orquestra</a>\n      <a href=\"#como\">Como Funciona</a>\n      <a href=\"#paraquem\">Para Quem</a>\n      <a href=\"#ativar\">Ativar</a>\n      <a href=\"#faq\">FAQ</a>\n    </nav>\n    <Cta href=\"#ativar\" variant=\"primary\">Ativar minha ag\u00eancia</Cta>\n  </header>\n);\n\n// ---------------------------------------------------------------- HERO\nexport const Hero = () => (\n  <section className=\"lp-hero\" id=\"top\">\n    <ConstellationField className=\"lp-hero-field\" />\n    <div className=\"lp-hero-vignette\" />\n    <div className=\"lp-hero-inner\">\n      <div className=\"lp-eyebrow\" style={{ justifyContent: 'center', marginBottom: 28 }}>\n        A ag\u00eancia aut\u00f4noma \u00b7 Operada por IA \u00b7 Vol. I 2026\n      </div>\n\n      <h1>\n        <span className=\"word\" style={cssVar({ '--wi': 0 })}><span>A ag\u00eancia</span></span>{' '}\n        <span className=\"word\" style={cssVar({ '--wi': 1 })}><span><em className=\"mc-display-i mc-cyan\">inteira</em>.</span></span>\n        <br />\n        <span className=\"word\" style={cssVar({ '--wi': 2 })}><span>Dedicada</span></span>{' '}\n        <span className=\"word\" style={cssVar({ '--wi': 3 })}><span>a <em className=\"mc-display-i mc-gold\">voc\u00ea</em>.</span></span>\n      </h1>\n\n      <p className=\"sub\">\n        Um <b style={{ color: 'var(--bone)' }}>CEO, um PMO e um PMI</b> \u2014 orquestrados por IA \u2014 dedicados\n        \u00e0 sua opera\u00e7\u00e3o e integrados \u00e0s ferramentas que voc\u00ea j\u00e1 usa. Cada orquestra \u00e9 desenhada para o seu\n        neg\u00f3cio. Voc\u00ea cria e fecha neg\u00f3cio; a orquestra cuida do resto.\n      </p>\n\n      <div className=\"cta-row\">\n        <Cta href=\"#ativar\" variant=\"primary\">Ativar minha ag\u00eancia</Cta>\n        <Cta href=\"#orquestra\" variant=\"ghost\">Conhecer a orquestra</Cta>\n      </div>\n\n      <div className=\"trust\">\n        <span>\u25c6 <b>CEO \u00b7 PMO \u00b7 PMI</b> dedicados</span>\n        <span>\u25c6 Integra com <b>seu stack</b></span>\n        <span>\u25c6 Opera\u00e7\u00e3o <b>24/7</b></span>\n        <span>\u25c6 <b>Modo sombra</b> antes de assumir</span>\n      </div>\n    </div>\n\n    <div className=\"lp-hero-scroll-hint\">\n      <span>Role para a orquestra</span>\n      <div className=\"line\" />\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- TRUST STRIP (honest signals)\nexport const TrustStrip = () => (\n  <div className=\"lp-trust-strip\">\n    <div className=\"item\"><span className=\"v cyan\">03</span><span>Executivos<br />dedicados</span></div>\n    <div className=\"item\"><span className=\"v\">\u25c6</span><span>Seu stack<br />integrado</span></div>\n    <div className=\"item\"><span className=\"v gold\">24/7</span><span>Opera\u00e7\u00e3o<br />orquestrada</span></div>\n    <div className=\"item\"><span className=\"v cyan\">Sombra</span><span>Voc\u00ea v\u00ea<br />antes de assumir</span></div>\n    <div className=\"item\"><span className=\"v\">Voc\u00ea</span><span>Define<br />a autonomia</span></div>\n  </div>\n);\n\n// ---------------------------------------------------------------- 01 PROBLEM\nexport const ProblemSection = () => (\n  <section className=\"lp-section\" id=\"sintoma\">\n    <span className=\"num\">01 / O GARGALO</span>\n    <div className=\"lp-bignum\" style={{ right: '8vw', top: '40px' }}>01</div>\n\n    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 80, alignItems: 'center', marginTop: 40 }}>\n      <div>\n        <div className=\"lp-eyebrow lp-reveal\">O pre\u00e7o de fazer tudo sozinho</div>\n        <h2 className=\"lp-h1 lp-reveal\">\n          Voc\u00ea virou o<br />\n          <em className=\"mc-display-i mc-cyan\">gargalo</em> do<br />\n          pr\u00f3prio est\u00fadio.\n        </h2>\n        <p className=\"lp-lede lp-reveal\" style={{ marginBottom: 28 }}>\n          Todo briefing passa por voc\u00ea. Todo prazo depende de voc\u00ea. Cada ferramenta fala uma l\u00edngua\n          diferente e nenhuma conversa com a outra. Voc\u00ea abriu um est\u00fadio pra criar \u2014 e virou gerente de\n          projeto, atendimento e financeiro de voc\u00ea mesmo.\n        </p>\n        <p className=\"lp-lede lp-reveal\" style={{ color: 'var(--bone-3)' }}>\n          Enquanto isso, o trabalho que te trouxe at\u00e9 aqui \u2014 a cria\u00e7\u00e3o \u2014 fica pra depois. Esse \u00e9 o gargalo.\n        </p>\n      </div>\n\n      <div className=\"lp-reveal\" style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>\n        {[\n          { v: 'Tudo', l: 'Passa por voc\u00ea antes de andar', c: 'gold' },\n          { v: 'Solto', l: 'Cada ferramenta fala uma l\u00edngua diferente', c: 'cyan' },\n          { v: '0', l: 'Pessoas cuidando da opera\u00e7\u00e3o enquanto voc\u00ea cria', c: 'gold' },\n          { v: '\u221e', l: 'Mensagens de cliente que moram na sua cabe\u00e7a', c: 'cyan' },\n        ].map((row, i) => (\n          <div key={i} style={card}>\n            <span\n              className=\"mc-num\"\n              style={{\n                fontFamily: 'var(--display)',\n                fontSize: row.v.length > 2 ? 34 : 56,\n                lineHeight: 1,\n                color: row.c === 'gold' ? 'var(--gold)' : 'var(--cyan)',\n                fontStyle: row.c === 'gold' ? 'italic' : 'normal',\n              }}\n            >\n              {row.v}\n            </span>\n            <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--bone-2)', letterSpacing: '0.04em', lineHeight: 1.5 }}>\n              {row.l}\n            </span>\n          </div>\n        ))}\n      </div>\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- 02 AUDIENCE\nexport const AudienceSection = () => (\n  <section className=\"lp-section\" id=\"paraquem\" style={{ borderTop: '1px solid var(--silver-2)' }}>\n    <span className=\"num\">02 / PARA QUEM</span>\n    <div className=\"lp-bignum\" style={{ right: '8vw', top: '40px' }}>02</div>\n\n    <div style={{ maxWidth: 920, marginBottom: 64, marginTop: 40 }}>\n      <div className=\"lp-eyebrow lp-reveal\">Feito para quem vive de entregar</div>\n      <h2 className=\"lp-h2 lp-reveal\">\n        A opera\u00e7\u00e3o por tr\u00e1s<br />\n        de cada <em className=\"mc-display-i mc-cyan\">entrega</em>.\n      </h2>\n      <p className=\"lp-lede lp-reveal\">\n        Se o seu trabalho \u00e9 criativo e a sua rotina virou gest\u00e3o, a orquestra \u00e9 pra voc\u00ea. Ela assume a\n        opera\u00e7\u00e3o de quem entrega \u2014 e devolve o foco \u00e0 cria\u00e7\u00e3o.\n      </p>\n    </div>\n\n    <div className=\"lp-pillars\">\n      {[\n        { k: 'Est\u00fadios de design', d: 'Briefings, vers\u00f5es e aprova\u00e7\u00f5es orquestrados. Mais projetos entregues sem voc\u00ea virar gerente.' },\n        { k: 'Video makers', d: 'Da pauta ao render: roteiro, cronograma e entregas no prazo, sincronizados ao seu editor.' },\n        { k: 'Social media', d: 'Calend\u00e1rio, aprova\u00e7\u00e3o e publica\u00e7\u00e3o em fluxo. O ritmo \u00e9 do PMO; a integra\u00e7\u00e3o \u00e9 do PMI.' },\n        { k: 'Copywriters', d: 'Pautas, revis\u00f5es e versionamento sob controle. Cada pe\u00e7a no tom, no prazo e no lugar.' },\n        { k: 'Web designers', d: 'Escopo, sprint e handoff de dev orquestrados. Menos retrabalho, mais sites no ar.' },\n        { k: 'Tr\u00e1fego \u00b7 Google & Meta Ads', d: 'Verba, criativos e relat\u00f3rios acompanhados de perto. O CEO l\u00ea o ROI; o PMI ajusta a campanha.' },\n      ].map((a, i) => (\n        <div key={i} className=\"lp-pillar lp-reveal\" style={{ padding: '26px 24px 28px' }}>\n          <div className=\"pill-num\" style={{ marginBottom: 14 }}>\u25c6 Vertical {String(i + 1).padStart(2, '0')}</div>\n          <h3 className=\"lp-h3\" style={{ fontSize: 22, marginBottom: 10 }}>{a.k}</h3>\n          <p style={{ fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.65, color: 'var(--bone-2)', margin: 0 }}>{a.d}</p>\n        </div>\n      ))}\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- 03 SOLUTION\nexport const SolutionSection = () => (\n  <section className=\"lp-section\" id=\"orquestra\">\n    <span className=\"num\">03 / A ORQUESTRA</span>\n    <div className=\"lp-bignum\" style={{ right: '8vw', top: '40px' }}>03</div>\n\n    <div style={{ maxWidth: 960, marginBottom: 80 }}>\n      <div className=\"lp-eyebrow lp-reveal\">A ag\u00eancia que trabalha por dentro</div>\n      <h2 className=\"lp-h1 lp-reveal\">\n        N\u00e3o \u00e9 um app.<br />\n        \u00c9 a sua <em className=\"mc-display-i mc-cyan\">ag\u00eancia</em><br />\n        operando <em className=\"mc-display-i mc-gold\">sozinha</em>.\n      </h2>\n      <p className=\"lp-lede lp-reveal\">\n        Tr\u00eas executivos orquestrados por IA, dedicados \u00e0 sua opera\u00e7\u00e3o e integrados ao seu ecossistema.\n        Voc\u00ea n\u00e3o contrata uma equipe \u2014 voc\u00ea ativa uma ag\u00eancia inteira.\n      </p>\n    </div>\n\n    <div className=\"lp-pillars\">\n      {[\n        {\n          n: '\u00a701', icon: 'ceo' as const, title: 'CEO', role: 'Dire\u00e7\u00e3o',\n          body: 'L\u00ea a sua opera\u00e7\u00e3o inteira, define prioridades e toma as decis\u00f5es de rumo. Protege a sua margem, distribui a energia da equipe e diz n\u00e3o pelo que n\u00e3o vale a pena.',\n          stamp: 'Dire\u00e7\u00e3o \u00b7 Sempre on',\n        },\n        {\n          n: '\u00a702', icon: 'pmo' as const, title: 'PMO', role: 'Orquestra\u00e7\u00e3o',\n          body: 'O escrit\u00f3rio de projetos que n\u00e3o perde um prazo nem um briefing. Planeja, aloca, acompanha cada cliente e garante o padr\u00e3o de entrega \u2014 projeto por projeto.',\n          stamp: 'Orquestra\u00e7\u00e3o \u00b7 Sem atraso',\n        },\n        {\n          n: '\u00a703', icon: 'pmi' as const, title: 'PMI', role: 'Integra\u00e7\u00e3o',\n          body: 'Executa o dia a dia e conecta tudo ao seu ecossistema: Figma, Drive, Notion, editor de v\u00eddeo, Meta e Google Ads, CRM, WhatsApp. Nada solto \u2014 tudo no lugar certo.',\n          stamp: 'Integra\u00e7\u00e3o \u00b7 Seu stack',\n        },\n      ].map((p, i) => (\n        <div key={i} className=\"lp-pillar lp-reveal\">\n          <div className=\"pill-num\">{p.n} \u00b7 {p.role}</div>\n          <div className=\"pill-icon\"><PillarIcon kind={p.icon} /></div>\n          <h3 className=\"lp-h3\" style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>\n            {p.title}\n            <span style={{ fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '0.18em', textTransform: 'uppercase', color: 'var(--bone-3)' }}>{p.role}</span>\n          </h3>\n          <p style={{ fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.7, color: 'var(--bone-2)', margin: '0 0 24px' }}>{p.body}</p>\n          <div\n            style={{\n              paddingTop: 18,\n              borderTop: '1px solid var(--silver-2)',\n              display: 'flex',\n              justifyContent: 'space-between',\n              fontFamily: 'var(--mono)',\n              fontSize: 9,\n              letterSpacing: '0.22em',\n              textTransform: 'uppercase',\n              color: 'var(--bone-3)',\n            }}\n          >\n            <span>{p.stamp}</span>\n            <span className=\"mc-cyan\">\u25c6 100% dedicado</span>\n          </div>\n        </div>\n      ))}\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- 04 HOW\nexport const HowSection = () => (\n  <section className=\"lp-section\" id=\"como\">\n    <span className=\"num\">04 / ATIVA\u00c7\u00c3O</span>\n    <div className=\"lp-bignum\" style={{ right: '8vw', top: '40px' }}>04</div>\n\n    <div style={{ maxWidth: 920, marginBottom: 80 }}>\n      <div className=\"lp-eyebrow lp-reveal\">Como funciona</div>\n      <h2 className=\"lp-h2 lp-reveal\">\n        Da <em className=\"mc-display-i mc-cyan\">ativa\u00e7\u00e3o</em> \u00e0 opera\u00e7\u00e3o aut\u00f4noma,<br />\n        em uma <em className=\"mc-display-i mc-gold\">\u00fanica sess\u00e3o</em>.\n      </h2>\n      <p className=\"lp-lede lp-reveal\">\n        Uma ativa\u00e7\u00e3o guiada. Quatro fases. Nenhuma delas pede que voc\u00ea vire especialista em nada.\n      </p>\n    </div>\n\n    <div className=\"lp-steps\">\n      {[\n        { ph: 'Fase 01', title: 'Diagn\u00f3stico', body: 'Voc\u00ea responde algumas perguntas sobre seu est\u00fadio, seus servi\u00e7os e seus clientes. O CEO calibra prioridades; o PMO mapeia como voc\u00ea trabalha hoje.' },\n        { ph: 'Fase 02', title: 'Integra\u00e7\u00e3o', body: 'Conectamos as ferramentas que voc\u00ea j\u00e1 usa \u2014 design, v\u00eddeo, social, tr\u00e1fego, CRM. Uma \u00fanica sess\u00e3o guiada, sem c\u00f3digo e sem configura\u00e7\u00e3o manual.' },\n        { ph: 'Fase 03', title: 'Modo Sombra', body: 'A orquestra opera em sombra por 7 dias. Voc\u00ea v\u00ea cada decis\u00e3o, cada briefing e cada entrega que ela faria \u2014 sem ainda perder o controle.' },\n        { ph: 'Fase 04', title: 'Aut\u00f4nomo', body: 'Voc\u00ea aprova. A ag\u00eancia assume a opera\u00e7\u00e3o. A partir daqui sua fun\u00e7\u00e3o volta a ser uma s\u00f3: criar e fechar neg\u00f3cio.' },\n      ].map((s, i) => (\n        <div key={i} className=\"lp-step lp-reveal\">\n          <div className=\"knot\" />\n          <div className=\"ph\">{s.ph}</div>\n          <h3 className=\"lp-h3\" style={{ fontSize: 26 }}>{s.title}</h3>\n          <p style={{ fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.7, color: 'var(--bone-2)', margin: 0 }}>{s.body}</p>\n        </div>\n      ))}\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- 05 DEMO (illustrative)\nexport const DemoSection = () => (\n  <section className=\"lp-section\" id=\"demo\" style={{ borderTop: '1px solid var(--silver-2)' }}>\n    <span className=\"num\">05 / UM DIA</span>\n    <div className=\"lp-bignum\" style={{ right: '8vw', top: '40px' }}>05</div>\n\n    <div className=\"lp-demo-grid\" style={{ marginTop: 40 }}>\n      <div className=\"lp-reveal\">\n        <div className=\"lp-eyebrow\">Exemplo \u00b7 Um dia orquestrado</div>\n        <h2 className=\"lp-h2\">\n          Uma ter\u00e7a-feira<br />operada <em className=\"mc-display-i mc-cyan\">sozinha</em>.\n        </h2>\n        <p className=\"lp-lede\" style={{ marginBottom: 32 }}>\n          Um recorte de como um dia da sua ag\u00eancia andaria sem voc\u00ea no meio. O CEO prioriza, o PMO\n          orquestra, o PMI executa e integra. Clientes atendidos, uma campanha reajustada, prazos no lugar.\n          Voc\u00ea criou. A opera\u00e7\u00e3o andou.\n        </p>\n        <Cta href=\"#ativar\">Ativar minha ag\u00eancia</Cta>\n      </div>\n\n      <div className=\"lp-term lp-reveal\">\n        <div className=\"head\">\n          <span className=\"dot\" style={{ background: '#ff5f57' }} />\n          <span className=\"dot\" style={{ background: '#febc2e' }} />\n          <span className=\"dot\" style={{ background: '#28c840' }} />\n          <span className=\"label\">mcorch \u00b7 orquestra \u00b7 exemplo</span>\n        </div>\n        <div><span className=\"fg\">\u203a 09:14</span> <span className=\"pr\">ceo</span> \u00b7 prioridade <span className=\"fg\">\u2192</span> <span className=\"gl\">campanha do cliente varejo</span> \u00b7 deadline 48h</div>\n        <div><span className=\"fg\">\u203a 09:14</span> <span className=\"pr\">pmo</span> \u00b7 aloca \u00b7 briefing gerado <span className=\"fg\">\u2192</span> time de design</div>\n        <div><span className=\"fg\">\u203a 09:15</span> <span className=\"pr\">pmi</span> \u00b7 sincroniza <span className=\"nb\">Figma \u2194 Drive \u2194 Notion</span> <span className=\"ok\">ok</span></div>\n        <div><span className=\"fg\">\u203a 11:02</span> <span className=\"pr\">pmi</span> \u00b7 Meta Ads \u00b7 verba realocada p/ criativo #4 <span className=\"ok\">ok</span></div>\n        <div><span className=\"fg\">\u203a 11:03</span> <span className=\"pr\">pmo</span> \u00b7 QA \u00b7 pe\u00e7a revisada \u00b7 dentro do padr\u00e3o <span className=\"ok\">\u2713</span></div>\n        <div><span className=\"fg\">\u203a 14:20</span> <span className=\"pr\">ceo</span> \u00b7 margem do projeto revisada <span className=\"gl\">ok</span></div>\n        <div><span className=\"fg\">\u203a 14:21</span> <span className=\"pr\">pmi</span> \u00b7 entrega enviada ao cliente via WhatsApp <span className=\"ok\">ok</span></div>\n        <div><span className=\"fg\">\u203a 18:40</span> <span className=\"pr\">pmo</span> \u00b7 amanh\u00e3 \u00b7 3 entregas agendadas \u00b7 0 conflitos<span className=\"mc-caret\" /></div>\n      </div>\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- 06 RESULTS (qualitative)\nexport const ResultsSection = () => (\n  <section className=\"lp-section\" id=\"resultados\" style={{ paddingTop: 60 }}>\n    <span className=\"num\">06 / O QUE MUDA</span>\n    <div className=\"lp-bignum\" style={{ right: '8vw', top: '40px' }}>06</div>\n\n    <div style={{ maxWidth: 920, marginBottom: 60, marginTop: 40 }}>\n      <div className=\"lp-eyebrow lp-reveal\">O que a orquestra tira das suas costas</div>\n      <h2 className=\"lp-h2 lp-reveal\">\n        O que muda quando<br />\n        a opera\u00e7\u00e3o <em className=\"mc-display-i mc-gold\">sai das suas costas</em>.\n      </h2>\n    </div>\n\n    <div className=\"lp-results lp-reveal\">\n      <div className=\"cell gold\"><div className=\"v\">Foco</div><div className=\"l\">De volta na cria\u00e7\u00e3o</div></div>\n      <div className=\"cell cyan\"><div className=\"v\">Prazo</div><div className=\"l\">Orquestrado, n\u00e3o na sua cabe\u00e7a</div></div>\n      <div className=\"cell\"><div className=\"v\">Stack</div><div className=\"l\">Conectado ponta a ponta</div></div>\n      <div className=\"cell gold\"><div className=\"v\">Sombra</div><div className=\"l\">Voc\u00ea v\u00ea antes de assumir</div></div>\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- VISION + ACTIVATION (honest, no shelf price)\nexport const ChampionshipOffer = () => (\n  <section id=\"oferta\" style={{ position: 'relative', borderTop: '1px solid var(--silver-2)' }}>\n    <div className=\"lp-vision\" id=\"lp-vision\">\n      <div className=\"lp-vision-pin\">\n        <div className=\"lp-vision-ambient\" />\n        <div className=\"lp-vision-stage\">\n          <div className=\"lp-eyebrow\" style={{ justifyContent: 'center', color: 'var(--gold)', marginBottom: 36 }}>\n            \u25c6 A vis\u00e3o \u00b7 Vol. I \u00b7 2026\n          </div>\n\n          <div className=\"lp-vision-acts\">\n            <h3 className=\"lp-vision-act\" data-vision-act=\"0\">\n              Imagine seu est\u00fadio entregando mais\u2014<br />\n              sem voc\u00ea virar gerente de projeto,<br />\n              atendimento e financeiro <em className=\"mc-display-i mc-cyan\">ao mesmo tempo</em>.\n            </h3>\n            <h3 className=\"lp-vision-act\" data-vision-act=\"1\">\n              Imagine um <em className=\"mc-display-i mc-gold\">CEO</em>, um <em className=\"mc-display-i mc-gold\">PMO</em> e um{' '}\n              <em className=\"mc-display-i mc-gold\">PMI</em><br />\n              cuidando da opera\u00e7\u00e3o enquanto voc\u00ea cria.<br />\n              Cada prazo, cada briefing, cada ferramenta \u2014 <em className=\"mc-display-i mc-cyan\">no lugar</em>.\n            </h3>\n            <h3 className=\"lp-vision-act\" data-vision-act=\"2\">\n              Essa \u00e9 a ag\u00eancia que trabalha por dentro.<br />\n              <em className=\"mc-display-i mc-gold\">MCORCH</em> \u00e9 o primeiro corte dela.\n            </h3>\n          </div>\n\n          <div className=\"lp-vision-floor\">\n            <div className=\"lp-vision-progress\">\n              <span className=\"dot is-active\" data-dot=\"0\" />\n              <span className=\"bar\" />\n              <span className=\"dot\" data-dot=\"1\" />\n              <span className=\"bar\" />\n              <span className=\"dot\" data-dot=\"2\" />\n            </div>\n          </div>\n        </div>\n      </div>\n    </div>\n\n    <div className=\"lp-marquee-wrap\">\n      <div className=\"lp-marquee\" id=\"offer-marquee\">\n        <span>A ag\u00eancia inteira</span><em>\u00b7</em><span>CEO \u00b7 PMO \u00b7 PMI</span><em>\u00b7</em>\n        <span>Dedicada a voc\u00ea</span><em>\u00b7</em><span>Integrada ao seu stack</span><em>\u00b7</em>\n        <span>Vol. I \u00b7 2026</span><em>\u00b7</em>\n        <span>A ag\u00eancia inteira</span><em>\u00b7</em><span>CEO \u00b7 PMO \u00b7 PMI</span><em>\u00b7</em>\n        <span>Dedicada a voc\u00ea</span><em>\u00b7</em><span>Integrada ao seu stack</span><em>\u00b7</em>\n        <span>Vol. I \u00b7 2026</span><em>\u00b7</em>\n      </div>\n    </div>\n\n    <div className=\"lp-offer-stage\" id=\"ativar\">\n      <span\n        className=\"num\"\n        style={{ position: 'absolute', top: 60, left: '8vw', fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '0.32em', color: 'var(--bone-3)' }}\n      >\n        07 / ATIVAR\n      </span>\n\n      <div className=\"lp-offer-hd lp-reveal\">\n        <h2 className=\"lp-h2\">\n          A orquestra tem<br />\n          <em className=\"mc-display-i mc-cyan\">tr\u00eas</em> profundidades.\n        </h2>\n        <p className=\"lp-lede\" style={{ marginTop: 18 }}>\n          Voc\u00ea n\u00e3o contrata uma equipe. Voc\u00ea ativa uma ag\u00eancia \u2014 exclusiva e personalizada para a sua\n          opera\u00e7\u00e3o. N\u00e3o \u00e9 um plano de prateleira: cada profundidade \u00e9 montada \u00e0 sua volta. Comece onde\n          faz sentido; a orquestra escala com voc\u00ea.\n        </p>\n      </div>\n\n      <div className=\"lp-pricing\">\n        <div className=\"lp-plan lp-reveal\">\n          <div className=\"tier\">\u00a7 Profundidade 01</div>\n          <h3 className=\"name\">Signal</h3>\n          <div className=\"price\"><span className=\"per\" style={{ marginTop: 0 }}>Orquestra\u00e7\u00e3o essencial</span></div>\n          <ul>\n            <li>PMO + PMI \u00b7 orquestra\u00e7\u00e3o base da opera\u00e7\u00e3o</li>\n            <li>Integra\u00e7\u00e3o do seu stack principal</li>\n            <li>Ativa\u00e7\u00e3o guiada \u00b7 onboarding acompanhado</li>\n            <li>Painel de opera\u00e7\u00e3o</li>\n            <li>Suporte por e-mail</li>\n            <li className=\"muted\">CEO dedicado</li>\n            <li className=\"muted\">QA automatizado de entregas</li>\n          </ul>\n          <div className=\"price-foot\"><Cta variant=\"ghost\">Falar sobre ativa\u00e7\u00e3o</Cta></div>\n        </div>\n\n        <div className=\"lp-plan is-featured lp-reveal\">\n          <div className=\"badge\">A ag\u00eancia inteira</div>\n          <div className=\"tier mc-cyan\">\u00a7 Profundidade 02</div>\n          <h3 className=\"name\">Harness</h3>\n          <div className=\"price\"><span className=\"per\" style={{ marginTop: 0 }}>Opera\u00e7\u00e3o completa</span></div>\n          <ul>\n            <li><b>CEO + PMO + PMI \u00b7 dedicados \u00e0 sua opera\u00e7\u00e3o</b></li>\n            <li>Integra\u00e7\u00e3o total ao seu ecossistema</li>\n            <li>Ativa\u00e7\u00e3o 1:1 com a equipe</li>\n            <li>QA de entregas + acompanhamento de ROI</li>\n            <li>Suporte priorit\u00e1rio</li>\n            <li>Modo sombra antes de assumir</li>\n          </ul>\n          <div className=\"price-foot\"><Cta variant=\"primary\">Ativar minha ag\u00eancia</Cta></div>\n        </div>\n\n        <div className=\"lp-plan lp-reveal\">\n          <div className=\"tier mc-gold\">\u00a7 Profundidade 03</div>\n          <h3 className=\"name\">Sovereign</h3>\n          <div className=\"price\"><span className=\"per\" style={{ marginTop: 0 }}>Sob medida \u00b7 por convite</span></div>\n          <ul>\n            <li>Tudo de Harness, sem teto</li>\n            <li>Orquestra dedicada \u00b7 agentes privados</li>\n            <li>Integra\u00e7\u00f5es sob medida</li>\n            <li>Acompanhamento humano dedicado</li>\n            <li>Revis\u00e3o estrat\u00e9gica recorrente</li>\n            <li>Roadmap co-criado</li>\n          </ul>\n          <div className=\"price-foot\"><Cta variant=\"ghost\">Solicitar convite</Cta></div>\n        </div>\n      </div>\n\n      <div className=\"lp-offer-close lp-reveal\">\n        <div className=\"lp-offer-stack\">\n          <div className=\"stack-row\"><span className=\"k\">\u25c6 Sombra</span><span className=\"v\">7 dias em modo sombra \u00b7 voc\u00ea v\u00ea cada decis\u00e3o antes de aprovar</span></div>\n          <div className=\"stack-row\"><span className=\"k\">\u25c6 Ativa\u00e7\u00e3o</span><span className=\"v\">Uma sess\u00e3o guiada \u00b7 sem c\u00f3digo, sem configura\u00e7\u00e3o manual</span></div>\n          <div className=\"stack-row\"><span className=\"k\">\u25c6 Autonomia</span><span className=\"v\">Voc\u00ea define o n\u00edvel \u2014 de \"s\u00f3 sugere\" a \"executa e me avisa\"</span></div>\n          <div className=\"stack-row\"><span className=\"k\">\u25c6 Vol. I</span><span className=\"v\">Primeiro corte p\u00fablico da ag\u00eancia aut\u00f4noma</span></div>\n        </div>\n\n        <div className=\"lp-offer-finale\">\n          <p style={{ fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '0.22em', textTransform: 'uppercase', color: 'var(--bone-3)', marginBottom: 22 }}>\n            Uma ag\u00eancia. N\u00e3o mais uma ferramenta.\n          </p>\n          <h3 style={{ fontFamily: 'var(--display)', fontSize: 'clamp(36px, 5vw, 64px)', lineHeight: 1, letterSpacing: '-0.02em', margin: '0 0 32px' }}>\n            Sua ag\u00eancia,<br />\n            <em className=\"mc-display-i mc-cyan\">dedicada</em> e <em className=\"mc-display-i mc-gold\">integrada</em>.\n          </h3>\n          <Cta variant=\"primary\">Ativar minha ag\u00eancia</Cta>\n        </div>\n      </div>\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- GUARANTEE \u2192 Modo Sombra (honest risk-reversal)\nexport const GuaranteeSection = () => (\n  <section className=\"lp-section\">\n    <div className=\"lp-guarantee lp-reveal\">\n      <div className=\"seal\">07d</div>\n      <div>\n        <div className=\"lp-eyebrow\" style={{ marginBottom: 16, color: 'var(--gold)' }}>Modo sombra \u00b7 Risco reverso</div>\n        <h3 className=\"lp-h3\" style={{ fontSize: 32, marginBottom: 14 }}>\n          7 dias vendo a opera\u00e7\u00e3o rodar sozinha \u2014<br />\n          antes de voc\u00ea entregar o controle.\n        </h3>\n        <p style={{ fontFamily: 'var(--mono)', fontSize: 13, lineHeight: 1.75, color: 'var(--bone-2)', margin: 0, maxWidth: '72ch' }}>\n          Antes de assumir de fato, a orquestra opera em sombra: voc\u00ea v\u00ea cada decis\u00e3o, cada briefing e cada\n          entrega que ela faria \u2014 sem perder o controle. S\u00f3 quando fizer sentido pra voc\u00ea, ela assume. Voc\u00ea\n          decide o n\u00edvel de autonomia, e revoga quando quiser.\n        </p>\n      </div>\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- 08 FAQ\nexport const FAQSection = () => (\n  <section className=\"lp-section\" id=\"faq\">\n    <span className=\"num\">08 / D\u00daVIDAS</span>\n    <div className=\"lp-bignum\" style={{ right: '8vw', top: '40px' }}>08</div>\n\n    <div style={{ maxWidth: 920, marginBottom: 50, marginTop: 40 }}>\n      <div className=\"lp-eyebrow lp-reveal\">Perguntas honestas</div>\n      <h2 className=\"lp-h2 lp-reveal\">\n        O que voc\u00ea ainda<br />\n        <em className=\"mc-display-i mc-cyan\">precisa saber</em>.\n      </h2>\n    </div>\n\n    <div className=\"lp-faq lp-reveal\">\n      {[\n        { q: 'O MCORCH substitui a minha equipe?', a: 'N\u00e3o. Ele substitui a opera\u00e7\u00e3o que sobra pra voc\u00ea \u2014 a gest\u00e3o, a coordena\u00e7\u00e3o, a integra\u00e7\u00e3o de ferramentas. Sua equipe criativa fica livre pra criar; o CEO, o PMO e o PMI cuidam de tudo que n\u00e3o \u00e9 cria\u00e7\u00e3o.' },\n        { q: 'Preciso saber configurar ferramentas ou mexer em c\u00f3digo?', a: 'N\u00e3o. Em uma sess\u00e3o de ativa\u00e7\u00e3o guiada conectamos seu Figma, Drive, editor de v\u00eddeo, Meta e Google Ads, CRM e WhatsApp. A partir da\u00ed a orquestra opera integrada ao que voc\u00ea j\u00e1 usa.' },\n        { q: 'Serve pro meu tipo de trabalho?', a: 'Funciona para est\u00fadios de design, video makers, social media, copywriters, web designers e gestores de tr\u00e1fego. Se a opera\u00e7\u00e3o ainda depende de voc\u00ea para andar, \u00e9 exatamente pra voc\u00ea.' },\n        { q: 'Em quanto tempo eu sinto diferen\u00e7a?', a: 'O modo sombra de 7 dias j\u00e1 mostra a opera\u00e7\u00e3o rodando por dentro. A partir da\u00ed, a carga de coordena\u00e7\u00e3o sai das suas costas e volta pra cria\u00e7\u00e3o \u2014 no ritmo que voc\u00ea aprovar.' },\n        { q: 'Ele publica post e roda an\u00fancio sozinho?', a: 'Com a sua aprova\u00e7\u00e3o. O PMI executa e integra, o PMO garante o padr\u00e3o, o CEO decide a prioridade. Voc\u00ea define o n\u00edvel de autonomia \u2014 de \"s\u00f3 sugere\" a \"executa e me avisa\".' },\n        { q: 'Como ficam meus dados e acessos?', a: 'Cada opera\u00e7\u00e3o \u00e9 isolada e criptografada. Voc\u00ea concede e revoga acessos quando quiser, e v\u00ea cada a\u00e7\u00e3o registrada. Nada \u00e9 feito \u00e0s escondidas.' },\n        { q: 'O Vol. I \u00e9 o lan\u00e7amento. Vai mudar depois?', a: 'Sim. Vol. I \u00e9 o primeiro corte p\u00fablico da ag\u00eancia aut\u00f4noma. Quem entra agora opera junto e acompanha as pr\u00f3ximas vers\u00f5es da arquitetura.' },\n      ].map((item, i) => (\n        <details key={i}>\n          <summary>\n            <span>{item.q}</span>\n            <span className=\"sign\">+</span>\n          </summary>\n          <div className=\"a\">{item.a}</div>\n        </details>\n      ))}\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- FINAL CTA\nexport const FinalCTA = () => (\n  <section className=\"lp-final\" id=\"acessar\">\n    <div style={{ position: 'relative', zIndex: 2 }}>\n      <div className=\"lp-eyebrow lp-reveal\" style={{ justifyContent: 'center', color: 'var(--cyan)' }}>\n        \u25c6 Vol. I \u00b7 Ativa\u00e7\u00e3o 2026\n      </div>\n      <h2 className=\"lp-reveal\">\n        <span className=\"cyan\">Pare</span> de ser o gargalo.<br />\n        <span className=\"gold\">Ative</span> a ag\u00eancia.\n      </h2>\n      <p className=\"lp-lede lp-reveal\" style={{ margin: '0 auto 44px', maxWidth: 620, textAlign: 'center' }}>\n        Sua pr\u00f3xima entrega n\u00e3o precisa passar por voc\u00ea.<br />\n        Precisa passar pela orquestra.\n      </p>\n      <div className=\"lp-reveal\" style={{ display: 'inline-flex', gap: 16, flexWrap: 'wrap', justifyContent: 'center' }}>\n        <Cta variant=\"primary\">Ativar minha ag\u00eancia</Cta>\n        <Cta href=\"#ativar\" variant=\"ghost\">Ver as profundidades</Cta>\n      </div>\n      <div className=\"meta lp-reveal\">\n        <span><b>CEO \u00b7 PMO \u00b7 PMI</b> dedicados</span>\n        <span><b>Integra</b> ao seu stack</span>\n        <span><b>Modo sombra</b> antes de assumir</span>\n        <span><b>Vol. I</b> \u00b7 2026</span>\n      </div>\n    </div>\n  </section>\n);\n\n// ---------------------------------------------------------------- FOOTER\nexport const LandingFooter = () => (\n  <footer className=\"lp-footer\">\n    <div className=\"row\">\n      <div style={{ maxWidth: 340 }}>\n        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 18 }}>\n          <SigilMark size={22} />\n          <Wordmark size={12} />\n        </div>\n        <p style={{ fontFamily: 'var(--mono)', fontSize: 11, lineHeight: 1.7, color: 'var(--bone-3)', margin: 0 }}>\n          Magic Constellation Orchestra \u00b7 A ag\u00eancia aut\u00f4noma.<br />\n          Um CEO, um PMO e um PMI dedicados e integrados ao seu ecossistema.\n        </p>\n      </div>\n\n      <div className=\"col\">\n        <h5>A Orquestra</h5>\n        <a href=\"#orquestra\">CEO \u00b7 PMO \u00b7 PMI</a>\n        <a href=\"#como\">Como Funciona</a>\n        <a href=\"#demo\">Um Dia</a>\n        <a href=\"#resultados\">O Que Muda</a>\n      </div>\n      <div className=\"col\">\n        <h5>Ativar</h5>\n        <a href=\"#ativar\">Profundidades</a>\n        <Link to=\"/auth\">Ativa\u00e7\u00e3o</Link>\n        <a href=\"#faq\">FAQ</a>\n        <Link to=\"/auth\">Login</Link>\n      </div>\n      <div className=\"col\">\n        <h5>Contato</h5>\n        <a href=\"mailto:contato@mcorch.com\">contato@mcorch.com</a>\n        <Link to=\"/terms\">Termos</Link>\n        <Link to=\"/privacy\">Privacidade</Link>\n      </div>\n    </div>\n    <div className=\"bottom\">\n      <span>\u00a9 2026 MCORCH \u00b7 A ag\u00eancia aut\u00f4noma</span>\n      <span>\u25c6 Vol. I \u00b7 MIV-001 \u00b7 2026.01</span>\n    </div>\n  </footer>\n);\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/LandingV2Sections.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:35:08)*


## 🤖 Claude *(23:35:09)*

Agora a página, montando as 14 seções + o motor de movimento:

## 🤖 Claude *(23:35:21)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/LandingV2.tsx",
  "content": "// MCORCH Landing V2 \u2014 the rebrand landing. Rich form restored from the original\n// design_handoff (14 sections + orchestrated motion + hero particle explosion);\n// content kept honest (no fabricated metrics/scarcity/shelf prices). Motion is\n// pure CSS + IntersectionObserver (no GSAP) \u2014 see landing-motion.ts. Brand CSS is\n// scoped under `.mcorch-lp` so it never leaks into the app.\nimport { useEffect } from 'react';\nimport { Helmet } from 'react-helmet-async';\nimport '@/styles/mcorch/system.css';\nimport '@/styles/mcorch/landing.css';\nimport '@/styles/mcorch/minimal.css';\nimport {\n  Nav, Hero, TrustStrip, ProblemSection, AudienceSection, SolutionSection,\n  HowSection, DemoSection, ResultsSection, ChampionshipOffer, GuaranteeSection,\n  FAQSection, FinalCTA, LandingFooter,\n} from '@/components/landing-v2/LandingV2Sections';\nimport { useLandingMotion } from '@/components/landing-v2/landing-motion';\n\nexport default function LandingV2() {\n  // Orchestrated reveal + hero ignition + pinned vision scrub (no GSAP).\n  useLandingMotion();\n\n  // Sticky-nav glass past the fold (progressive enhancement \u2014 usable without it).\n  useEffect(() => {\n    const nav = document.getElementById('lp-nav');\n    if (!nav) return;\n    const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 40);\n    onScroll();\n    window.addEventListener('scroll', onScroll, { passive: true });\n    return () => window.removeEventListener('scroll', onScroll);\n  }, []);\n\n  const jsonLd = {\n    '@context': 'https://schema.org',\n    '@type': 'Organization',\n    name: 'MCORCH',\n    alternateName: 'Magic Constellation Orchestra',\n    url: 'https://login.mcorch.com',\n    description:\n      'MCORCH ativa uma ag\u00eancia inteira operada por IA \u2014 um CEO, um PMO e um PMI dedicados \u00e0 sua opera\u00e7\u00e3o e integrados ao seu stack. Exclusivo e personalizado para cada opera\u00e7\u00e3o.',\n  };\n\n  return (\n    <>\n      <Helmet>\n        <title>MCORCH \u2014 A ag\u00eancia aut\u00f4noma \u00b7 CEO \u00b7 PMO \u00b7 PMI dedicados a voc\u00ea</title>\n        <meta\n          name=\"description\"\n          content=\"Um CEO, um PMO e um PMI orquestrados por IA, dedicados \u00e0 sua opera\u00e7\u00e3o e integrados \u00e0s ferramentas que voc\u00ea j\u00e1 usa. Exclusivo e personalizado para cada opera\u00e7\u00e3o.\"\n        />\n        <meta property=\"og:title\" content=\"MCORCH \u2014 A ag\u00eancia aut\u00f4noma\" />\n        <meta\n          property=\"og:description\"\n          content=\"Um CEO, um PMO e um PMI orquestrados por IA \u2014 dedicados \u00e0 sua opera\u00e7\u00e3o, integrados ao seu stack.\"\n        />\n        <meta property=\"og:type\" content=\"website\" />\n        <link rel=\"canonical\" href=\"https://login.mcorch.com\" />\n        <script type=\"application/ld+json\">{JSON.stringify(jsonLd)}</script>\n      </Helmet>\n\n      <div className=\"mcorch-lp\">\n        <Nav />\n        <Hero />\n        <TrustStrip />\n        <ProblemSection />\n        <AudienceSection />\n        <SolutionSection />\n        <HowSection />\n        <DemoSection />\n        <ResultsSection />\n        <ChampionshipOffer />\n        <GuaranteeSection />\n        <FAQSection />\n        <FinalCTA />\n        <LandingFooter />\n      </div>\n    </>\n  );\n}\n"
}
```

> **Tool Result (Write)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(23:35:29)*


## 🤖 Claude *(23:35:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/LandingV2.tsx",
  "limit": 15
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// MCORCH Landing V2 — the rebrand landing (design_handoff_mcorch, 2026-07-03).
> 2	// Minimalist & truthful cut (Sovereign directive): sober, readable, honest —
> 3	// exclusivity over hype. Scoped under `.mcorch-lp` so brand CSS never leaks.
> 4	import { useEffect } from 'react';
> 5	import { Helmet } from 'react-helmet-async';
> 6	import '@/styles/mcorch/system.css';
> 7	import '@/styles/mcorch/landing.css';
> 8	import '@/styles/mcorch/minimal.css';
> 9	import { Nav, Hero, Orchestra, Audience, Activation, LandingFooter } from '@/components/landing-v2/LandingV2Sections';
> 10	
> 11	export default function LandingV2() {
> 12	  // Sticky-nav glass past the fold (progressive enhancement — usable without it).
> 13	  useEffect(() => {
> 14	    const nav = document.getElementById('lp-nav');
> 15	    if (!nav) return;
> ```

## 🤖 Claude *(23:42:09)*

API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.

## 👤 User *(23:47:35)*

Agora a página, montando as 14 seções + o motor de movimento:

● Write(src/pages/LandingV2.tsx)
Error writing file

  Read 1 file

● API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.

✻ Sautéed for 20m 51s

※ recap: You're running the MCORCH autonomous loop; I re-did the handson and found the git HEAD is on the rebrand line (54c699f, 4 commits unsealed and unpushed), not the Universe line. Next: tell me whether to seal the rebrand, resume the loop, or confirm which git line is canonical. (disable recaps in /config)

## 🤖 Claude *(23:49:14)*

No response requested.

## 👤 User *(23:49:34)*

Agora a página, montando as 14 seções + o motor de movimento:

● Write(src/pages/LandingV2.tsx)
Error writing file

  Read 1 file

● API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.

✻ Sautéed for 20m 51s

※ recap: You're running the MCORCH autonomous loop; I re-did the handson and found the git HEAD is on the rebrand line (54c699f, 4 commits unsealed and unpushed), not the Universe line. Next: tell me whether to seal the rebrand, resume the loop, or confirm which git line is canonical. (disable recaps in /config)

## 🤖 Claude *(23:52:23)*

Retomando — a escrita da página falhou por sobrecarga do servidor. Já reli o arquivo; vou reescrevê-lo agora.

🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/LandingV2.tsx",
  "content": "// MCORCH Landing V2 \u2014 the rebrand landing. Rich form restored from the original\n// design_handoff (14 sections + orchestrated motion + hero particle explosion);\n// content kept honest (no fabricated metrics/scarcity/shelf prices). Motion is\n// pure CSS + IntersectionObserver (no GSAP) \u2014 see landing-motion.ts. Brand CSS is\n// scoped under `.mcorch-lp` so it never leaks into the app.\nimport { useEffect } from 'react';\nimport { Helmet } from 'react-helmet-async';\nimport '@/styles/mcorch/system.css';\nimport '@/styles/mcorch/landing.css';\nimport '@/styles/mcorch/minimal.css';\nimport {\n  Nav, Hero, TrustStrip, ProblemSection, AudienceSection, SolutionSection,\n  HowSection, DemoSection, ResultsSection, ChampionshipOffer, GuaranteeSection,\n  FAQSection, FinalCTA, LandingFooter,\n} from '@/components/landing-v2/LandingV2Sections';\nimport { useLandingMotion } from '@/components/landing-v2/landing-motion';\n\nexport default function LandingV2() {\n  // Orchestrated reveal + hero ignition + pinned vision scrub (no GSAP).\n  useLandingMotion();\n\n  // Sticky-nav glass past the fold (progressive enhancement \u2014 usable without it).\n  useEffect(() => {\n    const nav = document.getElementById('lp-nav');\n    if (!nav) return;\n    const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 40);\n    onScroll();\n    window.addEventListener('scroll', onScroll, { passive: true });\n    return () => window.removeEventListener('scroll', onScroll);\n  }, []);\n\n  const jsonLd = {\n    '@context': 'https://schema.org',\n    '@type': 'Organization',\n    name: 'MCORCH',\n    alternateName: 'Magic Constellation Orchestra',\n    url: 'https://login.mcorch.com',\n    description:\n      'MCORCH ativa uma ag\u00eancia inteira operada por IA \u2014 um CEO, um PMO e um PMI dedicados \u00e0 sua opera\u00e7\u00e3o e integrados ao seu stack. Exclusivo e personalizado para cada opera\u00e7\u00e3o.',\n  };\n\n  return (\n    <>\n      <Helmet>\n        <title>MCORCH \u2014 A ag\u00eancia aut\u00f4noma \u00b7 CEO \u00b7 PMO \u00b7 PMI dedicados a voc\u00ea</title>\n        <meta\n          name=\"description\"\n          content=\"Um CEO, um PMO e um PMI orquestrados por IA, dedicados \u00e0 sua opera\u00e7\u00e3o e integrados \u00e0s ferramentas que voc\u00ea j\u00e1 usa. Exclusivo e personalizado para cada opera\u00e7\u00e3o.\"\n        />\n        <meta property=\"og:title\" content=\"MCORCH \u2014 A ag\u00eancia aut\u00f4noma\" />\n        <meta\n          property=\"og:description\"\n          content=\"Um CEO, um PMO e um PMI orquestrados por IA \u2014 dedicados \u00e0 sua opera\u00e7\u00e3o, integrados ao seu stack.\"\n        />\n        <meta property=\"og:type\" content=\"website\" />\n        <link rel=\"canonical\" href=\"https://login.mcorch.com\" />\n        <script type=\"application/ld+json\">{JSON.stringify(jsonLd)}</script>\n      </Helmet>\n\n      <div className=\"mcorch-lp\">\n        <Nav />\n        <Hero />\n        <TrustStrip />\n        <ProblemSection />\n        <AudienceSection />\n        <SolutionSection />\n        <HowSection />\n        <DemoSection />\n        <ResultsSection />\n        <ChampionshipOffer />\n        <GuaranteeSection />\n        <FAQSection />\n        <FinalCTA />\n        <LandingFooter />\n      </div>\n    </>\n  );\n}\n"
}
```

> **Tool Result (Write)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(23:52:35)*


## 🤖 Claude *(23:52:36)*

The partial read didn't register. Let me read the full file, then write.

## 🤖 Claude *(23:52:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/LandingV2.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// MCORCH Landing V2 — the rebrand landing (design_handoff_mcorch, 2026-07-03).
> 2	// Minimalist & truthful cut (Sovereign directive): sober, readable, honest —
> 3	// exclusivity over hype. Scoped under `.mcorch-lp` so brand CSS never leaks.
> 4	import { useEffect } from 'react';
> 5	import { Helmet } from 'react-helmet-async';
> 6	import '@/styles/mcorch/system.css';
> 7	import '@/styles/mcorch/landing.css';
> 8	import '@/styles/mcorch/minimal.css';
> 9	import { Nav, Hero, Orchestra, Audience, Activation, LandingFooter } from '@/components/landing-v2/LandingV2Sections';
> 10	
> 11	export default function LandingV2() {
> 12	  // Sticky-nav glass past the fold (progressive enhancement — usable without it).
> 13	  useEffect(() => {
> 14	    const nav = document.getElementById('lp-nav');
> 15	    if (!nav) return;
> 16	    const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 40);
> 17	    onScroll();
> 18	    window.addEventListener('scroll', onScroll, { passive: true });
> 19	    return () => window.removeEventListener('scroll', onScroll);
> 20	  }, []);
> 21	
> 22	  const jsonLd = {
> 23	    '@context': 'https://schema.org',
> 24	    '@type': 'Organization',
> 25	    name: 'MCORCH',
> 26	    alternateName: 'Magic Constellation Orchestra',
> 27	    url: 'https://login.mcorch.com',
> 28	    description:
> 29	      'MCORCH ativa uma agência inteira operada por IA — um CEO, um PMO e um PMI dedicados à sua operação e integrados ao seu stack. Exclusivo e personalizado para cada operação.',
> 30	  };
> 31	
> 32	  return (
> 33	    <>
> 34	      <Helmet>
> 35	        <title>MCORCH — A agência autônoma · CEO · PMO · PMI dedicados a você</title>
> 36	        <meta
> 37	          name="description"
> 38	          content="Um CEO, um PMO e um PMI orquestrados por IA, dedicados à sua operação e integrados às ferramentas que você já usa. Exclusivo e personalizado para cada operação."
> 39	        />
> 40	        <meta property="og:title" content="MCORCH — A agência autônoma" />
> 41	        <meta
> 42	          property="og:description"
> 43	          content="Um CEO, um PMO e um PMI orquestrados por IA — dedicados à sua operação, integrados ao seu stack."
> 44	        />
> 45	        <meta property="og:type" content="website" />
> 46	        <link rel="canonical" href="https://login.mcorch.com" />
> 47	        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
> 48	      </Helmet>
> 49	
> 50	      <div className="mcorch-lp">
> 51	        <Nav />
> 52	        <Hero />
> 53	        <Orchestra />
> 54	        <Audience />
> 55	        <Activation />
> 56	        <LandingFooter />
> 57	      </div>
> 58	    </>
> 59	  );
> 60	}
> 61	
> ```

## 🤖 Claude *(23:52:49)*

Agora reescrevo a página com as 14 seções + o motor de movimento:

## 🤖 Claude *(23:53:01)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/LandingV2.tsx",
  "content": "// MCORCH Landing V2 \u2014 the rebrand landing. Rich form restored from the original\n// design_handoff (14 sections + orchestrated motion + hero particle explosion);\n// content kept honest (no fabricated metrics/scarcity/shelf prices). Motion is\n// pure CSS + IntersectionObserver (no GSAP) \u2014 see landing-motion.ts. Brand CSS is\n// scoped under `.mcorch-lp` so it never leaks into the app.\nimport { useEffect } from 'react';\nimport { Helmet } from 'react-helmet-async';\nimport '@/styles/mcorch/system.css';\nimport '@/styles/mcorch/landing.css';\nimport '@/styles/mcorch/minimal.css';\nimport {\n  Nav, Hero, TrustStrip, ProblemSection, AudienceSection, SolutionSection,\n  HowSection, DemoSection, ResultsSection, ChampionshipOffer, GuaranteeSection,\n  FAQSection, FinalCTA, LandingFooter,\n} from '@/components/landing-v2/LandingV2Sections';\nimport { useLandingMotion } from '@/components/landing-v2/landing-motion';\n\nexport default function LandingV2() {\n  // Orchestrated reveal + hero ignition + pinned vision scrub (no GSAP).\n  useLandingMotion();\n\n  // Sticky-nav glass past the fold (progressive enhancement \u2014 usable without it).\n  useEffect(() => {\n    const nav = document.getElementById('lp-nav');\n    if (!nav) return;\n    const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 40);\n    onScroll();\n    window.addEventListener('scroll', onScroll, { passive: true });\n    return () => window.removeEventListener('scroll', onScroll);\n  }, []);\n\n  const jsonLd = {\n    '@context': 'https://schema.org',\n    '@type': 'Organization',\n    name: 'MCORCH',\n    alternateName: 'Magic Constellation Orchestra',\n    url: 'https://login.mcorch.com',\n    description:\n      'MCORCH ativa uma ag\u00eancia inteira operada por IA \u2014 um CEO, um PMO e um PMI dedicados \u00e0 sua opera\u00e7\u00e3o e integrados ao seu stack. Exclusivo e personalizado para cada opera\u00e7\u00e3o.',\n  };\n\n  return (\n    <>\n      <Helmet>\n        <title>MCORCH \u2014 A ag\u00eancia aut\u00f4noma \u00b7 CEO \u00b7 PMO \u00b7 PMI dedicados a voc\u00ea</title>\n        <meta\n          name=\"description\"\n          content=\"Um CEO, um PMO e um PMI orquestrados por IA, dedicados \u00e0 sua opera\u00e7\u00e3o e integrados \u00e0s ferramentas que voc\u00ea j\u00e1 usa. Exclusivo e personalizado para cada opera\u00e7\u00e3o.\"\n        />\n        <meta property=\"og:title\" content=\"MCORCH \u2014 A ag\u00eancia aut\u00f4noma\" />\n        <meta\n          property=\"og:description\"\n          content=\"Um CEO, um PMO e um PMI orquestrados por IA \u2014 dedicados \u00e0 sua opera\u00e7\u00e3o, integrados ao seu stack.\"\n        />\n        <meta property=\"og:type\" content=\"website\" />\n        <link rel=\"canonical\" href=\"https://login.mcorch.com\" />\n        <script type=\"application/ld+json\">{JSON.stringify(jsonLd)}</script>\n      </Helmet>\n\n      <div className=\"mcorch-lp\">\n        <Nav />\n        <Hero />\n        <TrustStrip />\n        <ProblemSection />\n        <AudienceSection />\n        <SolutionSection />\n        <HowSection />\n        <DemoSection />\n        <ResultsSection />\n        <ChampionshipOffer />\n        <GuaranteeSection />\n        <FAQSection />\n        <FinalCTA />\n        <LandingFooter />\n      </div>\n    </>\n  );\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/LandingV2.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:53:17)*


## 🤖 Claude *(23:53:18)*

Falta a acessibilidade de reduced-motion na seção "visão" (3 atos empilhados em vez de scrub). Ajusto o hook e adiciono o CSS:

## 🤖 Claude *(23:53:21)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/landing-motion.ts",
  "old_string": "    if (reduce) {\n      reveals.forEach((el) => el.classList.add('is-in'));\n      root.querySelector('.lp-hero')?.classList.add('is-in');\n      // still wire the vision scrub below so acts remain readable\n    } else {",
  "new_string": "    if (reduce) {\n      reveals.forEach((el) => el.classList.add('is-in'));\n      root.querySelector('.lp-hero')?.classList.add('is-in');\n      // No scrub under reduced motion \u2014 stack the 3 vision acts so all stay readable.\n      root.querySelector('.lp-vision')?.classList.add('reduce-stack');\n    } else {"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/landing-v2/landing-motion.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:53:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ncat >> src/styles/mcorch/landing.css << 'CSSEOF'\n\n/* Reduced-motion: vision can't scrub, so stack the 3 acts and let the section\n   collapse to content height (all acts readable, no empty 280vh pin). */\n.mcorch-lp .lp-vision.reduce-stack { height: auto; }\n.mcorch-lp .lp-vision.reduce-stack .lp-vision-pin { position: static; height: auto; padding: 90px 0; }\n.mcorch-lp .lp-vision.reduce-stack .lp-vision-acts { display: block; min-height: 0; }\n.mcorch-lp .lp-vision.reduce-stack .lp-vision-act { position: relative; inset: auto; opacity: 1 !important; margin: 0 auto 48px; }\nCSSEOF\necho \"landing.css agora com $(wc -l < src/styles/mcorch/landing.css) linhas\"",
  "description": "Append reduced-motion vision stacking CSS"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> landing.css agora com 717 linhas
> ```

## 🤖 Claude *(23:53:59)*

Agora a prova material (Lei 1): tsc + build.

## 🤖 Claude *(23:54:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== tsc ===\"; npx tsc --noEmit 2>&1 | tail -25; echo \"tsc exit: ${PIPESTATUS[0]}\"",
  "description": "TypeScript strict check on new landing code"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === tsc ===
> tsc exit: 0
> ```

## 🤖 Claude *(23:54:22)*


## 🤖 Claude *(23:54:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== build ===\"; bun run build 2>&1 | tail -25",
  "description": "Production build"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === build ===
> dist/assets/core.esm-CnK3VuAE.js                43.21 kB │ gzip:  14.35 kB
> dist/assets/CampaignWizard-Dy29_x-K.js          44.70 kB │ gzip:  13.96 kB
> dist/assets/hands-IHRRN789.js                   45.32 kB │ gzip:  17.07 kB
> dist/assets/AffiliateProductsPage-BlTUhe3p.js   46.31 kB │ gzip:  13.81 kB
> dist/assets/SettingsPage-BiYZ13HA.js            48.89 kB │ gzip:  13.63 kB
> dist/assets/useSpaces-BalSseDL.js               59.36 kB │ gzip:  14.30 kB
> dist/assets/SpaceCanvasPage-BzRcHSxx.js         62.74 kB │ gzip:  21.65 kB
> dist/assets/AIOSTerminal-I6K5PDw4.js            70.57 kB │ gzip:  21.94 kB
> dist/assets/Vignette-1VYLdr4n.js                70.87 kB │ gzip:  17.39 kB
> dist/assets/DashboardHome-eF8QrfkP.js           73.60 kB │ gzip:  22.76 kB
> dist/assets/useNodeIntelligence-zGRT_vd9.js     98.78 kB │ gzip:  22.16 kB
> dist/assets/proxy-DH3odrWn.js                  125.30 kB │ gzip:  41.24 kB
> dist/assets/ConstellationMatrix-CYhgEiLD.js    135.13 kB │ gzip:  37.39 kB
> dist/assets/CanvasEditorPage-CvUuFU2I.js       148.64 kB │ gzip:  39.40 kB
> dist/assets/index-ConZQ2AX.js                  167.01 kB │ gzip:  53.33 kB
> dist/assets/ConstellationPage-Dha1LYKU.js      184.36 kB │ gzip:  63.64 kB
> dist/assets/CartesianChart-B24tG9hC.js         325.07 kB │ gzip:  96.83 kB
> dist/assets/index-B9N_D6CJ.js                  664.03 kB │ gzip: 196.77 kB
> dist/assets/react-three-fiber.esm-BNgX5C8J.js  824.11 kB │ gzip: 221.90 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 27.29s
> ```

## 🤖 Claude *(23:55:11)*


## 🤖 Claude *(23:55:13)*

Build ok (27.3s). Vou provar materialmente que os números fabricados sumiram do bundle e que o conteúdo honesto entrou, depois verifico no browser real.

## 🤖 Claude *(23:55:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nCHUNK=$(ls -t dist/assets/LandingV2-*.js 2>/dev/null | head -1)\necho \"chunk: $CHUNK ($(wc -c < \"$CHUNK\" 2>/dev/null) bytes)\"\necho \"\"\necho \"=== fabricados que DEVEM ter sumido (esperado: 0 cada) ===\"\nfor pat in '3.4' 'R\\$' '17.*24 vagas' '1.497' '4.997' '14.997' '99.9%' '68%' '2.4k'; do\n  n=$(grep -oE \"$pat\" \"$CHUNK\" 2>/dev/null | wc -l)\n  printf \"  %-16s %s\\n\" \"$pat\" \"$([ \"$n\" -eq 0 ] && echo \"\u2705 0\" || echo \"\u274c $n ainda presente\")\"\ndone\necho \"\"\necho \"=== honesto/rico que DEVE existir (esperado: >0) ===\"\nfor pat in 'Modo Sombra' 'ConstellationField\\|Constella' 'profundidades' 'Signal' 'Harness' 'Sovereign' 'lp-vision-act' 'Perguntas honestas'; do\n  n=$(grep -oiE \"$pat\" \"$CHUNK\" 2>/dev/null | wc -l)\n  printf \"  %-20s %s\\n\" \"$pat\" \"$([ \"$n\" -gt 0 ] && echo \"\u2705 $n\" || echo \"\u274c ausente\")\"\ndone",
  "description": "Prove fabricated content gone and honest content present in built chunk"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> chunk: dist/assets/LandingV2-B_foapQ_.js (40941 bytes)
> 
> === fabricados que DEVEM ter sumido (esperado: 0 cada) ===
>   3.4              ✅ 0
>   R\$              ✅ 0
>   17.*24 vagas     ✅ 0
>   1.497            ✅ 0
>   4.997            ✅ 0
>   14.997           ✅ 0
>   99.9%            ✅ 0
>   68%              ✅ 0
>   2.4k             ✅ 0
> 
> === honesto/rico que DEVE existir (esperado: >0) ===
>   Modo Sombra          ✅ 7
>   ConstellationField\|Constella ❌ ausente
>   profundidades        ✅ 3
>   Signal               ✅ 1
>   Harness              ✅ 2
>   Sovereign            ✅ 1
>   lp-vision-act        ✅ 5
>   Perguntas honestas   ✅ 1
> ```

## 🤖 Claude *(23:55:45)*


## 🤖 Claude *(23:55:47)*

Todos os fabricados = 0, honesto presente. O grep de "ConstellationField" falhou só porque o minificador renomeia o componente — vou confirmar que o canvas de partículas está no bundle por strings literais que sobrevivem à minificação, e subo o preview para verificar no browser:

## 🤖 Claude *(23:55:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nCHUNK=$(ls -t dist/assets/LandingV2-*.js | head -1)\necho \"=== assinaturas do canvas de part\u00edculas no bundle ===\"\nfor s in 'prefers-reduced-motion' 'desynchronized' 'createRadialGradient' 'requestAnimationFrame' 'lp-marquee-drift\\|lp-hero-field' 'visibilitychange'; do\n  n=$(grep -oiE \"$s\" \"$CHUNK\" | wc -l)\n  printf \"  %-24s %s\\n\" \"$s\" \"$([ \"$n\" -gt 0 ] && echo \"\u2705 $n\" || echo \"\u2014\")\"\ndone\necho \"\"\necho \"=== canvas element renderizado no chunk? ===\"\ngrep -oE 'lp-hero-field|createElement\\(\"canvas\"\\)|\"canvas\"' \"$CHUNK\" | sort | uniq -c | head",
  "description": "Confirm particle canvas code bundled via surviving literals"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === assinaturas do canvas de partículas no bundle ===
>   prefers-reduced-motion   ✅ 2
>   desynchronized           ✅ 1
>   createRadialGradient     ✅ 2
>   requestAnimationFrame    ✅ 4
>   lp-marquee-drift\|lp-hero-field —
>   visibilitychange         ✅ 2
> 
> === canvas element renderizado no chunk? ===
>       1 "canvas"
>       1 lp-hero-field
> ```

## 🤖 Claude *(23:55:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\n# preview do dist na 4174 (landing \u00e9 p\u00fablica \u2014 sem sess\u00e3o)\n(npx vite preview --port 4174 --host 127.0.0.1 >/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/preview.log 2>&1 &) ; sleep 4\ncurl -s -o /dev/null -w \"preview / \u2192 HTTP %{http_code}\\n\" http://127.0.0.1:4174/\nhead -8 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/preview.log",
  "description": "Start vite preview of dist and check it responds"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> preview / → HTTP 200
>   ➜  Local:   http://127.0.0.1:4174/
> ```

## 🤖 Claude *(23:56:13)*


## 🤖 Claude *(23:56:14)*

Canvas de partículas confirmado no bundle (`lp-hero-field`, `createRadialGradient`, `requestAnimationFrame`, `desynchronized`) e preview respondendo 200. Agora verificação visual real com Playwright:

## 🤖 Claude *(23:56:16)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:mcp__playwright__browser_navigate,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_evaluate,mcp__playwright__browser_console_messages,mcp__playwright__browser_resize,mcp__playwright__browser_wait_for",
  "max_results": 6
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_navigate'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_take_screenshot'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_evaluate'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_console_messages'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_resize'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_wait_for'}]
> ```

## 🤖 Claude *(23:57:02)*


🛠️ **Tool Call**: `mcp__playwright__browser_resize`
```json
{
  "width": 1920,
  "height": 1080
}
```

> **Tool Result (mcp__playwright__browser_resize)** - ❌ Error
>
> ```
> ### Error
> Error: async initializeServer: Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome
> Run "npx playwright install chrome"
> ```

## 🤖 Claude *(23:57:27)*


## 🤖 Claude *(23:57:28)*

Playwright MCP quer o canal `chrome` (ausente). O caminho documentado do projeto é o `agent-browser`. Deixa eu checar o que está disponível para o screenshot:

## 🤖 Claude *(23:57:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== agent-browser? ===\"; command -v agent-browser || ls -la node_modules/.bin/agent-browser 2>/dev/null || echo \"no agent-browser bin\"\necho \"=== playwright chromium instalado? ===\"; ls ~/.cache/ms-playwright/ 2>/dev/null | head; ls node_modules/.bin/playwright 2>/dev/null && echo \"playwright cli ok\"\necho \"=== chromium do sistema ===\"; command -v chromium chromium-browser google-chrome 2>/dev/null || echo \"nenhum chromium no PATH\"",
  "description": "Check for agent-browser and chromium availability"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === agent-browser? ===
> /home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser
> === playwright chromium instalado? ===
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
> node_modules/.bin/playwright
> playwright cli ok
> === chromium do sistema ===
> nenhum chromium no PATH
> ```

## 🤖 Claude *(23:57:50)*

`agent-browser` está disponível (caminho documentado). Vou capturar o hero (explosão), a seção de planos honesta e a visão, via preview local:

## 🤖 Claude *(23:57:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSP=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad\"\nagent-browser --help 2>&1 | head -40 || echo \"---\"; echo \"=== subcomandos ===\"; agent-browser 2>&1 | head -30",
  "description": "Discover agent-browser CLI interface"
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
> === subcomandos ===
> 
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
> ```

## 🤖 Claude *(23:58:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSP=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad\"\nexport PLAYWRIGHT_BROWSERS_PATH=~/.cache/ms-playwright\necho \"=== viewport 1920x1080 + open ===\"\nagent-browser viewport 1920 1080 2>&1 | tail -2\nagent-browser open \"http://127.0.0.1:4174/\" 2>&1 | tail -5\nsleep 3   # deixa a explos\u00e3o de igni\u00e7\u00e3o assentar (~1.65s) + fontes\necho \"=== console errors ===\"\nagent-browser console 2>&1 | grep -iE 'error|warn' | head -20 || echo \"sem erros no console\"\necho \"=== screenshot HERO (p\u00f3s-explos\u00e3o) ===\"\nagent-browser screenshot \"$SP/lp-1-hero.png\" 2>&1 | tail -3\nls -la \"$SP\"/lp-1-hero.png 2>/dev/null",
  "description": "Open preview, check console, screenshot hero after ignition"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === viewport 1920x1080 + open ===
> Unknown command: viewport
> ✓ MCORCH — A agência autônoma
>   http://127.0.0.1:4174/
> === console errors ===
> === screenshot HERO (pós-explosão) ===
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/lp-1-hero.png
> -rw-rw-r-- 1 ubuntu ubuntu 126439 Jul  3 20:58 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/lp-1-hero.png
> ```

## 🤖 Claude *(23:58:39)*


## 🤖 Claude *(23:58:40)*

Sem erros no console, hero capturado. Vou ver a imagem:

## 🤖 Claude *(23:58:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/lp-1-hero.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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EIQVCbEAC8stU6ZMWWeddZL32W233YYMGSKhsIQEOhyof+lyIEEQhJ7w7d2Swl+985aoX0EQBJAiQVguOOSQQ9LpAlHNoX4PPPBAEgRBEITljx2/nbT12SdJEARBEAEsLB/U1tbuvvvuxPPbJ1l3Lcvaf//9SRAEQRCWMzbcmFYan7TDYw+RIAiCIAJYWD7Yd999hw0bhpULLrggOWbvZpttljxOWBAEQRAGH7vuyRGP41i8mF55kQRBEAQRwMLywYEHHgjr7rx58+66666nn346Yc90On344YeTIAiCICxP7LxL0tb/PL38T/8rCIJQHCKAhUHPmmuuueWWW2Llvvvu6+zsvOeee5L332effSorK0kQBEEQlg9qamizLZN2WHEmQBIEQSiECGBh0AOLbiaTyeVyt9xyC74+8sgj33zzTcL+I0eO3HPPPUkQBEEQlg++syeVl8dutW16+AESBEEQHEQAC4ObdDr93e9+FyuvvPLKZ599Rs40Ng88kPSX3rKsgw46iARBEARh+eDbuxeYAOmbr0kQBEFwkHmAhcENbLljxozByj333AMjsEr8xz/+cdxxxyUcNXXq1JVXXvmrr74iYTll9dVXX2uttdZee+3VVluttrb2M4fHH3882TtAEARhULLzrklbn3uKjcCCIAiCg0WCMJi59dZbd91114aGhk033bSxsVElplKpJ554YsMNN4w7yrbt3/3ud5dddhktv6y//vrbbrvtSiutVFVVVV1dXeUA63dLS0uzw5IlS959990XXngBpUf9DjK28cYbjx49esSIESNHjqyvrx82bFhbW9vixYuhUbFcuHDh7NmzkT0qkb322uu0006DAE47oDLgrrPZLPpHcObrrrvuL3/5C/US6zusscYaQ4cOHeKAyyHnCxYsUMsvvvji9ddfp2VHSR0948aNmzRp0oQJE8aPH491PCMUYFNTE2oLlp9//vlTTz01cLqNtthiC7zjyK0qfHRz4EEvdUCV/vLLL995550333yT+hd0uEyfPp36DNzptGnTcOO4a/1eV1RUdHR0qPcaT2rOnDl4cd577z0a1FRX05bb0ISJNHoMNTfRZ5/SZx/TlzOot6ipodXWoJUn0SqT2Xb68Yf08Qf01ZfUW6y7Po2fSBNXoZEjafEimj+PPvuEPuibh7LpFvT0y0khoHffgV54jpY5a69LE1am8RP4mX69gAsEn3lzqYeMHEVbbkVjVuKiXjCfpn9C775DDUuoF5m2Iz/KMWOpaSlXFTxH5L/brLUO17pVJlHtUPrkA/rwA/r8M+p1UCyo4autzvUQPb+fftSdOrDrHvTOmzR3DgnCYKZ22MRAiliAhUEMGug77rgjVh5++GGtfgGkzn333ZcggNWEwJdffrm9fHWKQ0busssu22yzzZQpU8aOHZvJZFJOk8hyXOPUUt2y7QBZ2NXVBZ3w4osv3nzzzfPnz6c+BhnDI0MOoRshrpAlJVAV5FI+UQAAABAASURBVDw72wPrUOnI27PPPgvpBUmZfHIY9s844wzoIqUHkIIVtQlFgSXE0nnnnTd58uSf/OQn1F3q6ur23nvv3Xfffb311oMa0Rpb34LKuS5hCJL3HV599dXHHnuM+hjkCqZv6H90CW2wwQZ/+9vffvOb3xQ86sQTTzzkkENQMikH9VxU5VE3ghXcywUXXPDxxx8/99xz6Eco+Dj6AhT44Ycfvttuu+E2zQ4Os/B15UGGIQg/+OADVJ6777570aJF1Aeg+2bdddddc801Ueyo3uor9Tabb775zjvvjLq9ySaboDKrd8d8r8l4Urh3vNfof3nttdcefPDBRx8dbNGPTjiZdtuLttwa7y2LOivF1stcFjfGDfHb/k5/+wv1pNtuzbXprPNptz0pnebzK92YzVI2xzrkuqvplr9R9xg6lA44jPbalzab4pzcolSa1TXyb+f4/KiEzz9N1/6R3u7VrhmolOQJkF4quSexd0BRH/t92mIKjR6Hv0+UTrkFzs/UKRA81nfepisvoacfp1IZPoJO+iHt+C1aZz1KZ7i09WnxNN95i267kW7/O/WEAw6l7x7E+R8yxFcVcf43/0d//h098mAJZ1t5FTrlDDrsaKccnLqHuoFT4YQfvk9nnEzvvk09pKqKjj6B9tqfVl3NzbO6kCoWdDf86hf04H2xh09ejUX+5FVpzXVo3Q1ok834HVxtDAnCcodYgIVBzFlnnQUlg/YfGsQBOxtMi2+88YbWP2HQRjzqqKP6QZD0D2gcQ9Jvv/32SpJp6QuVAmsYZIAyscJKFj5WyWD0INx///3XXHMNTGfUB/zwhz+ExEKfRcYBmdSbPv30U9gVYbaCUWvMmDEbbbQRjFpqExr0XQ6dnZ0vvfTSlVde+dZbb0We/4orrjj44IPxxFtbW2+99dZ//etfeLhW1KA4aOOjjz76ySefpBKBaD/55JMh4FGMZWVlSoSoTcp2jdKGPJ440dfRqGSwAka5X/3qVxCQVAqQnXi4ENKwbeIxYYl1dA2gGFFiuKJe4ikrTZj2SPZ0QI/Ascceu88++6DY1R0VzIyqLbCl33LLLddeey1yQv0CTNMnnHACzPvDhw8PZBWZQRVa5IBNqjRg+saD0L08eOh44tdffz00YTGX++yzz3A2ZU/GPTY64D3C+4VCHuqgyhxmWC3F8UTa29txaeol8L5897vfxQNaY4011F2rrhxVAUBlZSXyA9UdPlZ1AeDFeffdd2+88caC4fEHBPsfQmecQ2usSWVllInqoIcGRt/WVzNo1+1oYenDGWB2O+s82u8gqqyksqiQUVAjHe1079108jFUEquvSWeeS3t9lyNRxWWenGBUnZ18ict/Tn+4korknAtp66lJO6y9Po0bF7sVnQVvvErF89D99NerqYccdhQdchRttgWVV3Bp4KcSf5JmfsUlP2q0b89sF35A6T/PcpkvKq5bDX8gTjmdTjiFTb6ZMor84cJp2zvo2afokL2pG2yyOV18GfsgqKcZ/lPShfO301k/oNtuKnw2SN8fncfVu7KCCyQit1lqaaELz6bru+ugVFdHx51Ex36Pxoyj8jK354Wcpz/rK/Z0gB7GVdrb6LKL6fe/zh948920xlrcm1BVzcrccnooUKTq859naK+dSRAGOWELsAhgYRADRQRLF2xrO+20kx4ArIAygUnzO9/5TsLhDzzwwPHHH0+DHAiY4447Dm398vJyNI5h7HrzzTc///xzSIIvvvhCG8SUvWjcuHHKAAvBHOgdwD5oK6P5/sc//hGqiXoPdE+cc845q666KnKY8pspHnnkkZtuugmm0ZyDMjxC4Rx00EGwSY4YMcLcGTIGOvOOO+6ADA6YH//85z9DJOD80C2nnnoqqsSRRx6ZIPxgE8MOVApQoShnFBoK2dTVMDDecMMN9913n7I6qlvYYYcdUPcOPPDAwEkgSHALUGKwyn744YdFXvrSSy+F9rNDWH7Icf4PHPvb3/42shzGjx9/9tln77nnnig0KKtUqrSAiLg6JOVHH32EjM2YMYP6EpT5D37wA7yqEJzIqln46A258847UfgtLS3a/qlKA3eEqn7AAQfgx0FNe4bq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H4Y61Y2nWrVq7dq1wyg2+L0uXALLVdqvQOcMmj3EmPrkjAnMYuhfmezXlQOwc0IY4K0TzJ6zZs0yZUCZATcOtRpcHwGLK1TZjBkzfAuJc6hwvMOCORGWQPOphUhg1USthral0CwVFTFJZwskK6LCo8bX8vGgRu1Nnz497ZbRMaRtfll1upgs4fUBbiveG/oqJKrT5QAesMiAMpITQvKE6nX8C0AogAkhfyQTJkzYsmWLmkRHSCh43+ETwPkGFEja+aWEFBO7svldeOGFrVq1gt4WQggpIoICuPR97IQQUpb4/fffX3rppbwVNiQT1KLKyZMnF/kOT6WF8uXLo+xTpkwRQnY5u6z53XnnnbDSv/XWW2rPZ0IIKRIqVvF/95EWYEIIIYQQQgghZZCgBZi7QBNCCCGEEEIIyQsogAkhhBBCCCGE5AUUwIQQQgghhBBC8gIKYEIIIYQQQggheQEFMCGEEEIIIYSQvIACmBBCCCGEEEJIXkABTAghhBBCCCEkL6AAJoQQQgghhBCSF1AAE0IIIYQQQgjJC8oJISSfOOSQQ5o0aTJv3jzJb8qVK3faaadZlrV48WIhJEDfvn2POOKIWbNmbdmyJcNLqlatesIJJ2zcuHHVqlW+UwMHDtx9993nzJkjhHjp06dP9+7df/rpJyGEEFIMVKxSy+dDCzAh+cV5DhkGbtiwIQJXrFhR/jig2K+55hopanbs2DF79uyrr766efPmstNUrlx58ODBd91118iRIy+44AIphZSEe11y+NOf/oTawFuSe+65BzWT4VV77bXXGWecAa3r8z/ssMNOPvnkqVOnSsmmd+/e995775gxY9AvGjRokNW1N998c69evaRsgbvZunVrKU46dOhwySWXTJ8+XbJkV1b4vvvue/fdd0uuFNMznBBCcqa8EELyiREjRhQWFmYYeLfddjvuuOOeffbZrVu3yh9E3bp1W7VqJcXA559/vnLlygoVKshOc+KJJw4YMGD06NGbNm1avXq1lEJKwr0uIUD3Ll269PLLL1+yZEmnTp1q1KgBRyYXfvvtt9ddd93PP//s81++fPmVV165YsUKKcHADjls2DCo33feeWf//ff/5z//ef7552d+eZs2bWrVqiVli2OOOea333779ddfpdjA0xivG2bNmiVZsisrHF2gXbt2kivF9wwnhJDcoAAmJF84/vjj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hBBCCCEkL6AAJoQQQgghhBCSF1AAE0IIIYQQQgjJC8oJIYQQhz59+nTv3v2nn37KJHDDhg0HDhy4ePHijRs3SsmmRo0aQ4YMqVOnzm+//SbFQ8WKFY8//vgdO3asWLFCSJHSunVr1O2MGTO2b9+eSfhDDjmkSZMm8+bNE1KqKEWPFEIIKUVUrFLL50MLMCGEJOjQocMll1wyffr0DMMfdNBBp59++gEHHCBFTbly5e677759991X+5x//vknn3yy5ETdunXvvPPOatWqDRo0KOdI0tKyZcuzzjrrhBNOkF1O5cqVBw8efNddd40cOfKCCy6QnBg2bNhRRx0lJY+aNWted911S5Ys2bRpU4aXnOcgJBpITVQR3tpISSLtI+Xmm2/u1auX7DR4RXLNNddIyeCMM87AKx4hhJBdSHkhhBAiUlhYePXVV8+aNSvD8GPHjp0/f/7XX38tRQ3sqNDAPXr0+O6775RPv379nnjiCcmJWrVqPf7441OmTIEFeK+99sKgf+vWrVLUzJw5c/jw4agQ2eWceOKJAwYMGD16NCTi6tWrJSf22GOPZcuWScmjevXqEPa4fZlfMmLECDRmIdHstttuxx133LPPPlscfSFn0j5S2rRpg+4sOw1eirVq1UpKBsccc8xvv/3266+/CiGE7CoogAkhGdGkSRNIMtij5s2b9/HHH6cNX7Vq1Z49e+LV/qJFiyZMmLBq1Sp9qk+fPjAYrl+//ptvvtETNU866SSMgSZPngx3x44dYf98/vnnY+LHAA6ycMyYMQcffDCG+x9++OHmzZvVKVg7kUTjxo2XLl36+eefr127Vl/Vu3dvJA1PSEGE//TTT1ZR1coAABAASURBVJU/Utx7770hO6E3tOwEiASlxqDzewed9GGHHabcCxYsMFWfmfQXX3yxZs0ayYkff/wRWVLutm3botq/+uor9TPqRsAQCgvS7rvvPnv2bCQNFa38MbhElk477TRV4ZmM+KNK3bdv33fffRepICokrWySqLSzzz5bhYG69k2BRik6d+6MW4CqXrduXdqkdenmzp37ySefSAZAzMyZM+ejjz7y+Yc2M4Bbv88++yDbqCXfPOFOnTqh4X377bfmNHhkpnv37qjYH374wWwboajaQC21aNECZUEtwXirz+pmNm3atKlTp2r/9u3b77fffojftm24X375ZV9t1K5dO5N7ffzxx9evXx8OdDrfdHedNJqWrxTHHnss/N98881MZDNucZcuXZBJNHvc00wuCb0RsHOigaHLo+C41+iSOjzMs+ja6EHI6p///Gc8B3AtegEuefrpp1WYQYMGoRQIEJNEQUFBt27dcLu3bdv2v//9D41E3M6LKoUb5lbkH3X+2GOPSXQLz63UyC2efsuXL//yyy/1cyDqKRfzSMG97t+/f4UKFdAdzHRzyBKqAhUyffp03WAUWT3bdQvfc8890fWQKzQ2fTaq0+H2IWmUBc8T9TZHPzdQEDzDERvciFZdVVQPUkIICYVrgAkh6WnWrNm9996LMT1GTjC4YcCEAWX8JQ8++CDGWytXrsSw+8wzz4R+U4OY888//4wzzoAWwuAP43WIDaWNL7nkEgyboAHg7tWr18CBA19//fWY+KFVEC1Gz5UqVcLY8ZBDDoEG3r59O0aKd9xxx4EHHgjRBX+MaCGN1OLJiy++GENeDGox4sd4CxeqUmC8e+ONN2IchvHcqaeeCgmnzBGq1BjFYgA9ePDgBg0aTJw4Ef6oh8MPPxxKA6nAR4//zKQRAAM4nXS2YHSIykEN4HIMf2G8fe2112JuBJK+8847URBU8tFHH40BJQamyHZMhUcRVWpUOOLBGwQIhkMPPRRGV5QOcrp8+fJQI6gNDMdhgDXF1bnnnjtkyBDc1v333/+UU05BPObLiKikmzdvjtKdcMIJEHjxzeyCCy5A/O3atUMmUe1HHnkkBt8YeceUGlV00003YSAOSYn2g/ap7vVRRx0FIzDaKvzxsgD+ai4AhuCPPPIIGgaaB/whEhBVTJZwI/75z3+i5UPFQWZD8CA/Omk0M1QX7G+oWN3McH/hD7WG1NHyUZy33nort3uNUsBIqJTJ+++/r3MV1cIBqu7222+HwodOi28Y4kjKu+++G4Hx8gidCBoPesmnpnyoG7FhwwbcCNxTfSNg90P3RMbQwlFLaG9KA+Pu49GBaoc8Vp3o7bffVpejmelXA1dcccXixYtnzpwZc68vvPBC1BvcqHA0RVj48VJAdd569eqhT6E4aLdwv/feexLdwnMr9VlnnYVsd+3a9S9/+QsUb/xTLuqRUqVKlZEjR0KdopZQNDyy8N4ELTOHLKFtXHfddSgamhlqG1HhlYdk/2xXLRxVjRuElobmBE0LnR9zI/AQvuGGG1BwZBvPAaSI/x3o5wbqH/7od3CjZnCbivBBSgghErYGmBZgQkh6IC0waP773/8ON17k33zzzU8++WTMdFMMLiFFMB5SVhdcogboGM9hyI4BN2zC+AkHfmK8KzmBMRzGSTCYYIAL0xDEMMbQGBRCyUCrYPAEnfPMM89gRDt+/HiMsTCWuv/+++HGtY8//riO57jjjoPl4aGHHoIboghGJzUgRqkxgFPLSjFqxIjzxRdfhEUCGu/SSy+F5zvvvGPmB0nDkgONjatgwfjPf/6jkpbsQRIw6aDeYP3AuFyNmCX6RiBpDGqReZxF0k899RR00X//+98cKjyq1OJY9YcOHQp7HRyqdFBZuLOqNu677z5fVBidX3/99UproXqR9L/+9a/4pKFqVGxIGjIPBYlpZjAWoZYQEvlRi7fRGCS2meFejxs3btSoUXBDhWI4ru61iu22224TRzhBniGYONbIMWPGvPLKK+JYt0aMGIGCp12Oi2pR6uLhhx+GjoKEVknD89///rdKWjczBEB46By4Ub0dOnTQtZHVvUYwKBkcYVhT9jRNVAsHuLOIAWpEddV4oFVmzJiB8Ljp0D/PPvssOh2Uc1R4dSPuueceNdUCbclsfkgUKhFRQS+hI0Oco0RQnjiqNcxQyL6CRCUReq/xAuLVV19VChOWUmg/cXoWGhgqGc11+PDhvu2mQlt4bqXGvVDWVGQJahBljylFzCMF7wKgKvFGBq8qRo8erfyzzZI4zQmRo0GK08zwVNH+WT3bFYhq7NixcODGQVr/9NNPMTcC0eI1EELCjd6EF1tw6OcGOhfyryfjSJE+SAkhJBQKYEJIejA2VdICYOAFMdmoUaOYQRIGLgsXLsQodprDlClT1Aw9xIO3+xjTYEAjjkDCSE5yBcYZlSuMDmENg+oWZ2gIw4se3sHsgIGjOEthkbSelaeLI45c13MOYSPSmyEht9ofpYBQic8PkkY2lNEDeViyZIlKOreioZ4xgocA7tix4wcffKCzFHojVNJq+jGShq7T4bOt8JhSI1fQBnBANnz99ddKUcSAkSsEpEoal+A9RdqkEUyFhw08bTNTagHDaNiOlLDU8USVGvdat4HnHPRVv//+u3Kghnv27KncUCaQ1hjB421L9erVLctCVGmXOusAiBOmLZ20OJPwxTGl6izBqqyTxoVaAGd7r2OIauEKbVZNC9Qy6hkNUq1Exc1CJmPCqxuhJ2Oj5tUMbQVedqj3YjMdUL0oFKoLjw6dVUlHzL3+5ZdfoMEQIWoPjyC9RCKG0BaeW6m1jf3qq6+WXEHmca/xfFPZ0IsIss2SOM1MNyc0Bv2EzPbZrlC1BGDcVi085kYgWryUwftQ3JFvHeIjL8IHKSGEhEIBTAhJD8b92q0GhRgnxV9y4403nnrqqRASJ5xwAoZrw4YNwyhNxQOrjlqJihHwzmybZAow7UYSFStWhFVQ/cQo9ueffw69RINLtD8curBmqTPBjCe3GEwgPnv06IG6gh1bTeuV6BsRTNoMn1WFx+TZTOKuu+6SWGBDg80HqkYJCYzU046qkTQG0/rewXaXdlJuVDwSUeqoihKjdGYAmIJhMp00aRJyAhuXZEbUvWjSpIn+6bP1RZXCjDD+XsdHFdrCswV2VPTrOQ7izIaVdOmKt2LN54b2h0VdGQMlrNSZJBF6r2F4P+200/AW6ZBDDkEnuv7669N+4Sy0he9kqXcG373W7myzJOkeEWb8aZ/tYuREvz2JuRHvvvtujRo1YKPu0qXL5ZdfjvsS3/iL9kFKCCFBKIAJIenBmAZKRrnxjh/HLVu2xF8Ca4+a8wbr04MPPnj44YePHTtWXfXGG28EP1KKU3oYB2tbJuaaqKziWtMeqIBJAeamFi1aKMtM06ZN9WgY/khRuTFQ1ttEmaWG/+mnn/7aa6/F7BWM8OaHVXZyv2XYHk8++WQM3yHg9ZzbqBvhS/qkk06CsQUxxFR4TCmyKnUU+++/f+PGjQcPHqzyMGLEiLSXIGkMmoP3LltiSm3e67Zt2/bq1Qtm6pioYEJEu3322WfFWZ6adhZADEgati/kyue/du1aNSlUnAWZ2j/bex2fdGgLz5YjjjgCikubNA888MD48CrDSFH9RB7SJr1jx47y5cvrrGp/dGpf51KdIuZew3j46KOPijObAHLx+OOPv/XWWyV7drLUffv2xasTNec826ccasMstb6J2WZJnF3u9eXaITk920OJf9S87ADHXx3iBXDRPkgJISQIvwNMCEnPDz/80Llz50MPPRQmrLPOOmvFihXxsxNbtmw5cuRIiDdxVvrpI0zBCxcu7NevnzirK//xj3/86U9/UpcgwoMPPhgmgo4dOx522GGzZ8+WnEBWYUVEPOIonDvvvFNtp4zx3/vvvw9DE5QYhsVq7qUCSrh///777rsvzBfHHnusFsaICp7IDEZgEPAIE78ZKcJjKDlkyBAUDdoVqsaUJZ06dRozZgwG4pIZP/74I8aUBxxwgF4ALNE3QiUNWyUMre3atUMeVAFjKjymFFmVOgrYcDDuR0sQpz2kXcypkkabUTMnked77rknty+1xpQaNxeF6tq1K3TICSecAEta2tige5ENhNf79OYGksZLAUSFaoFl8rLLLlP+48aNg5653UFVlyLbex2fdGgLV4waNeqll16CSpR04J7Wr19fTWVHb037SR7ciEWLFp166qmoQ+jAnj17Tps2Le0lyKSa8gqbofaHyIdlEvWAU3irUrNmTbUDVsy9VotvxRHAMCFqXQ3Upk16o/UiLzWyhPuCUuP136BBg/Rk4GyfcrCj4mmm6qFPnz76HmWbJYB3WGrLQDQ/Pf9Zsn+2x5c69Eacf/75l1xyierLuAu+lrZ69Wo8qE2f+Afpcccd9+qrr6JWhRBCcoUWYEJIejBGx9AcQ3bIgCVLltx2223xX93AEAqqSc8hxPBF70mLUelVV10FIwDcn3/+uf7qxgsvvIBBIc6Ks3Iy/htIMSxYsAAGZ9hGMESG3QBDJf2tFAz0YYJr1arViy++iDG0vgQmR6hiZa/G2EvtE6NKjSHsxRdfPGzYMFiTHnnkEWWIQGCM5lUYZVP6/vvvUSgkDdl/zjnnYHCmrE++j1vCKJT5NFoYfyBUunfvrsyPOkuhNwJJ33fffeedd94pp5yCC998801d6qgKjyKq1FEMHDhQ7aADOnTogAxAt2PsO2HCBOi9+++/H8NiyA9z0XVM0ijd6NGjUbqVK1fivuRs+YkqNeKEP+4asgRtltYkiMwMHTpUWYnT7nwej2pmanMsyLkHHnhA+X/44Yewe/fo0QO3u0WLFtrInO29hvXY3NpNbeI1fPhw9L6oFi7Ojk3oEbByx+8hrEBvwiuDp59+etWqVeikSkbGgxpGHh577DHE/8EHHwQN4D5QnN69e6sKN+2E0G/oCOi2sHgjqv/7v//Tlsaoez116tSzzz773HPPFee7UKr4Cqg11M/NN9+s3HgfIUVaatysK6+8Un1dCdlQW7hL9FMu6pGC59X48eNVPr/88ku9ZVcOWUKVIhXUPyzn6Jt6VW22z/YYom7EpEmTrrvuOrXyHI8U3054sAzjveSJJ54INx6e6AvxD1JIaFiqM3lfQwghUXBZBSHkDwBGHpgaghNrW7dujXHYjBkzZOfA8AhiDAYWjJ9CA8AyPGfOHDVDMh4MtmCggDjJbWagCWwsGG2ntdflDEoN2w7ePgS/NhRV4VEUValhw4ERLKsbCuMPRuS4ZOcrKqrUGP3DgIbSZfjlW7SlWbNmrV+/XnYaVAhezUAAh56FEoOZDm8f0sYTc6+zAroLogVC0fyaazzq82bm942LHNw4KHMUDVoddaI2IRenWcLojdoL3otsW3i25FBq9CAUIXhJtk85PDfQCIOG2WyzBPMvau/nn3/e+UdZDMV9I8SZlJHxPnfSAAAQAElEQVT5mg5CCKlep5nPhwKYEJIv1KtXD4YIccQDxpQ33ngjzCxCyB8NmqWaJQsL8HPPPae+urRruPDCCxs1aqT6RUkDQtEngAkhhJBsCQpgToEmhOQLW7duVV+Lhfnok08+0d+eIeSPBeZlaDy0zyeeeCLtKtmiZfz48TtpQy4+1qxZ8/rrr/s+1UsIIYTsJLQAE0IIIYQQQggpgwQtwNwFmhBCCCGEEEJIXkABTAghhBBCCCEkL6AAJoQQQgghhBCSF1AAE0IIIYQQQgjJCyiACSGEEEIIIYTkBRTAhBBCCCGEEELyAgpgQgghhBBCCCF5AQUwIYQQQgghhJC8gAKYEEIIIYQQQkheQAFMCCGEEEIIISQvoAAmhBBCCCGEEJIXUAATQgghhBBCCMkLKIAJIYQQQgghhOQFFMCEEEIIIYQQQvICCmBCCCGEEEIIIXkBBTAhhBBCCCGEkLyAApgQQgghhBBCSF5AAUwIIYQQQgghJC+gACaEEEIIIYQQkhdQABNCCCGEEEIIyQvKCyGEFAeWJYSUTGxbCCGEEJKXUAATQnKFEpeUUuKbLuUxIYQQUnahACaEZAblLskTgk2dkpgQQggpK1AAE0KioeglRLwdgWKYEEIIKc1QABNCvBSV6KV4JiWWnRGxFMOEEEJIaYYCmBDikJtepcolpZGYdpuVptXxUAkTQgghpQQKYELynsxFbNZyN3t5TEFNsiIX4Rl7TW4LgNVVlMGEEEJIiYcCmJA8JkNBmyaY5fuXkF1HLq0uKHFDXEbwjM28lMGEEEJIiYcCmJC8JK30jQtg6UOGiRVhKEJCyFRyRoSzAi47LHyGq38pgwkhhJASDAUwIXlGjtI3XvQWhxGYgpjE4JOmkhlWbEx2IKBleIeJYcpgQgghpLRBAUxI3hAvfaN0b/hF0f6Z+RGyc+TUqkLVqGWHxGkbof1i2NTJ6WZHUwYTQgghJQwKYELygxj1G3IqVN8GPTMx/FoxvwgpdkztaUmYCLYCIW3Hz/Q3xXC0Eo6RwdTAhBBCSMmAApiQsk4W0jc4z9nnE6V4M5sgTciux9P67LhZ0D5TcOqXHTIXWilh3+zoGBlMUzAhhBBSMqAAJqRMk6n6DZO+VoZnvefSq13qYbLL8AnOiP2frbDrTD3sUchWyvyrLrQtI65Yey9NwYQQQsgfDQUwIWWXKPUbNPxaEW6RuFMiOyGDswtHSMb4Jz3HhbICP4KS2PZJX59N2DZkcGamYGpgQggh5I+DApiQMkqo+s1c+mbi9v7r/xG6ipiQYifUnhvwsMJ+2KYkdiWu5XNLyghsRbiTGbGogQkhhJCSBgUwIWWR9OrXO4c5dcpK7XmrHSKZmog9yYnE/iakZGAFFHKM+vW6PdLXtzZY/YwwBVMDE0IIIX8QFMCElDmyU79hijdOAwfcwZ+hPhlCmUyyIiMVafmvscIutIMzn6Pcrvr1yGDv2mDfjGhqYEIIIaRkQAFMSNkijfrNXvpmJIZDZz5Ha1mqXFJUxLQlO+YavXBX+zhqNk6QBkRvjCM4I5oamBBCCCkZUAATUobIWv0aCjZc8XolbrhDvKbgCEWSiTAmpAhJNDRXXtoh55x/bf+eWXbqn9S1VtDhE712yuprmn89bmpgQggh5I+HApiQskLm6jfp6fr4fmrpGyJ3AyZfy2f7DeTBp5AJ2aWYr2YcnRlUwikNbBqFtb8VaUr2yOCUl0cVCzUwIYQQUrKgACakTJCp+o1QufHS1+8ZZu8Nql9r50TvTl5Oyja5KEZjzoLtNfuadmAr7OPBKR87oWb9S4UNGax+Jk3BxnRoamBCCCGkZEABTEjppwjUb4TKDR5TPyXcDhyaH6pZUrTk0KJMhenfnNlp+XaU7ddUwFbKkhy0+tqW5yhR86KpgQkhhJA/DApgQsoikeo3dNpz6DFKDEvADpyxDA7kUggpFiK+vps8aYf7pCSouYI3dX3A07UGB9Wv6+s1CKfTwIQQQggpfiiACSnlxJlbY9RvrPRVYTK3CYcn6smT719CihOjndkBV0r3il+Oastw0sejgH2/gr/dSPV0aFf0ZqiBqYoJIYSQ4ocCmJDSTFGq33Q/JWIutAS315JAHkKyLoQUI1ruah/L9TZPGdLXPCWuHDWPIUkYWtoKGoSpgQkhhJASBwUwIWWSzNVvmEMk7KepezP8ULCRH6HmJbuSoBHYncCcUsISvlWVTwwHp0ankgiIVf906HQamBBCCCG7FgpgQkotMeZfwwxsHL3q1/PTdHgVr2VFT372qmvx2p99OTFyKYTsIrToFa/udWSq8lQCVYLrdb322CgZrK4S4+tHyjdEAxuXphw0AhNCCCG7FApgQsoKIeLTkL9p1G+E7rW816qfTZtLz17Sdk9p0DDx17CRNGgk1asLIaWX9etl6WJZsliWLkn8/TJDJv5PFswTn3INV6eWsTW0/k5SQAOLNi/7ttoqGsVbqVKlWrVqVaxYsUKFCuUd4CgoKBBCSi2FhYXbtm3bvn27Om7dunX16tU4CiGE7AQ0xRBSOok0/4ZNfo5Sv0lHtAXYDLlvN+l/hBx+tFSsIOPeke3bZNVKWbVKVq6QNatl8ybvvkHm+kl3VyG/v+X3lwh/i/70j/a3Mg8vfn+tSCtXkdq1pc5uUqeO1KkrFSrIEcfIls3y/rvy4Tj5fnIijJoXbbt/Iq7DOZVymyEleTb4U4wFyUEBnLEkrly5cr169erWrQvFu27dOmgDrRaA7WC5jwu66S5dbqDf5uCI9zs1atRA817hsGXLFiGEkHRUr9PM50MBTEjpxLLCfyYdgW2uLMs/4dnS+jYggC2vBj7pVDl6oNSqLV9/JZP+JwsX+Fcv2pE/ItY5coYn2QVYGfhZkafws0lz6b6/9NxfVq6Sd8bKqy+GqN9wAez6RKnfoPT1Kd4MBHCdOnWaNm0KnbB+/Xolfb0RpLQE/elflvyVDAawDy9cuHAV3sMSQkg0FMCElAmi1K+Ym11JhOE3A/Wrzx5xlIy4Ub77Vv7zlGzamAhWqE28dlLGJo2+dmpZo88n9FgocWd55HEnjwUxZ62UW7S/5fWxPPFUrSqnnyOdOsut18uH74kYduCMNHDAFCziHpP/pXw00Rq4Zs2azZo1g4F3yZIlO3bsUNqARx7z7ViuXLmGDRvCMrxgwYI1a9YIIYSEQQFMSJkgc/Ov1sCm+pWA1vWZfPG3Vye5435ZsVz+83hiSaQ5FDfH5UrlijOGt8XdWMjQG2IqDTvlNv3pprtY3bbl8bd8YVQH0eGNzpXsF274ho3ltLMTc6SvuFh++dkrgBGmMKWBfapYoudFi2RlBK5atWqLFi3ggPTlSkhCxDEIQwZDEs+fP3/Dhg1CCCFeKIAJKf1kZP419qwyf3qsvl71qzbLUT//fKIceay88arMnpVcJ2kbq3lFb5xr+CuJUKjXVTohLVc6aLdthfvTTXcxuSXCv1Dctqr9xQgvyfAFPn9bWrdLdJCxr8jbY1Pqt7AwcQzXwF71KxL4mfwvecrE+3N3h99//33dunVCCDGoWbNmkyZN0DsWLlwohBBiQAFMSOkn3vzrPxpzniUofeHn6N6k+nWOI26U3ZvIqHtF7x+bMlWlfntH7SoDvrG7EFJC8f2vz7a8nsZOcil/43NfkLuXXSlzZsudtziXFyY9JUwDmxZg7RYJOUqkAC4oKGjZsiWG+HPnzqXhl5BQKlWq1KJFizVr1vz222+Fqj8SQggFMCFlAVMApzH/hkrfgClYq1+M3Z9/TSZ/I/99wzlruyt1XcWbWvdrrPgVY46oDm+Y3wz/mKMde5ZHHtMerTRhQlYFW35/T3u2XLfRuZLhnRDHHi8dO8nppyT7TpThV0tiCZ0IbSc7l07e1MCOu0KFCu3bt7dte968ebZDnq/85JHHqCNQawRmzpy5bds2IYQQCmBCSj2Zmn8DGli5C5RP8K9AdmyXR5+Szz9NfPElgat1/Q49XjeeH7bnH6/T8CTkj8fy/Zv64WvPlnvKMgN4HV16yH495NLzpFx5vwbWSrjQq4dDZbBIlBG4erVqbdu2hVFr6dKlzsnEKN8NSDfddIe4GzZsWKtWLWjgjRs3CiEk7wkK4HJCCClFhAvgzM2/0X/PvyrvvSdTJxtzMq2E6dZ2jqLH5c46Xv3l1cSa3sKUf2qep7gywgzpDcMjj8V7FE+rSxl53Rauz/p81FrflL+kWrhuz4rFCxPuK66RN16RjPqveDqsGNOqw95HFxQUQP2uXbtWqV9CSCZs2LBBbRC9fPly27aFEJLfVKxSy+dDAUxIqcIUwJbX/CvezZ9TGrgg5WOafM2fV98g8+fJlx87UtcRD5ZjubLFqxncUbpSF5adUhpip1SBksxKh4ik9LAlnjB6WOIVJq50oZvuzNyhbSnpdoMqty1JJZwMY/q7PmLEoOORgPrV6S76XerWlQP6yoTPvZf5YjGisySYQMrT6OOtW7WCXWvRokVCCMkGaOCaNWvCDrxy5UohhEheQwFMSGmmaM2/Ba4G/vOJsk8XeW60s1LXNo5e/VBoKlU7GUa7tSYRRzkrbexTtkl1bSfDBN0WjzxmfwxtSym3bnvJ7pK6VmzD3zaUre1/U2O5jdg21rerngL3zJ9kwDGJl0q/zExeZUep3yyMwI0bN65dq9bcuXOFEJI9a9euhRG4oKBg/fr1QgjJYyiACSnNxAngKPNvtNVX+XToJIPPkPtuT470TTuY+mnZpkfKX2ndlMXM9vzUOll8fwFsHnksumPIPGJvC9Qq13fW1irX2wtsrwa2vUnabgf53xfyt/Pll59k+QozdiMVkwgjsEGVKlVa7rEHN7MlZGdYt25d8+bNV69evX37diGE5CtBAVwghJDSSGr+s+kp3j1+LO+fca3l7gh9x33y+svJSaGFakxf6ExgLkyO9W3XelaoJjyrLW31fj/O119SbjVx2pkAnfoejPIXV3vYSX8Rj4VZ6KZ7p92hbaxQkvP5k/5u+yy0DX/bacmu22znql+oWf3ixqD6iE4LvDFGbrvf89YphbcnmiZfX6ikw2rerNnChQsxalcrGHnkkcccjtu2bUM/ggYWQggxoAWYkNJDyALg2PnP8ebfggLpf6S0bCVvvp4c2ScOpo3LwXZnRGtP2076ix3iFnd2qHbbmblt16eQbrqzdKujZNzefDOiVTwhbssTXn9pKdlHjD200KFWLJce+8PklPg+sG30oCRBn8hZ0HVq165Tp+7ixYu1DyEkN7Zs2dKgQYPNmzfDIYSQvCRoAeb/WQkpJWQ9/znd0l/8ffK1XDVUli1xdawhJmxjlWOh+L8A7PFxZ4Hqq4LH1HeA7cgwPPJYLEdXtRZEh0m2Xv06yXEnw1teH8uIx3z95Bwb7y433Sn9eznC2DYmR4T9iXY7Pcc9Ipp9OnX6/feF3i+42EIIyYlq1ao1atRo2rRpQgjJS/gZJEJKLaECw95XQwAAEABJREFU2JTBPtuvaMUbZgSGDD7xr1KunHz8oRODMQr37WhlJ12Gw075WLZnkbCJLalRvug/QnYxbttLtcYwLKcxi7EA2DZnWYundyS7nel2jjD/tmwlVavKjOnehAJ9xDJclse/ccOGFSpUXL58uRBCioJt27bVrl27oKBgw4YNQgjJP7gGmJAygV8MJ/9LOdS/lv5lGf6OAMbo/Mhj5cl/OcN0ZzGkOlqFyb1zlY/tHm13ZW9hYcpypSahFgYsWgnDV6G70tIOOdruVYVGeB553Nmjt12Ftj1R63sLU+ZZs02K0eBTrb0w1eBT/cU2+kthqr888agcNdARz+YyYP1yytMXPerXcZQvX373xo3V5GfbkNB00033zrgXLVrUtGlT9C8hhBAKYELKItomZYVIX3Vq365Su7ao1+HJPa6coxo2mLv+mF/03eH6a0taoRF+h7gqwhvPDufnDq/iFdtQ2oF0o/JDf/rH+XvblW5vO5wdrXaEhU+clUBsKgbHvcP1sSW5Y1Z8ftavl3oNZO993XdSARmc6pJey69DtapVt23brhYrWsZ7Lrrppntn3Js3b4YduEqVKkIIIRTAhJRmrGi/gInYMmWwSP8BMuHzxM+kHcy1cRXqUX6ha5t1jztMXeFEpTWtcpuWMRVeaQ8pTCkTHT6lfulP/13g77TDHY7td4cvfKGnbWs9bNups7a7R7SnX9jJYImrC1NvdtCz+h/hlbcR3z0K9OBaNWuuW7fuD9kvl0cey/YRPatWLf80SEJIfsI1wISUEsxpz+bS39QxagGwd+mvctx0hzw3WtauEb2yUeEMFSKP6mAZIZNX2Sm38vb5xGDzWIKPFSrKuRdKw0by84zSkeewl0IBgiuB9Ypf5TYbudcn5qjDrF8nZ5wjzz/txm17E3Kd5kRo19GsSZNly5bxm6WEFDk7duyoX7/+0qVLhRCSZwTXAHM5BCFlAp/h1xLvUkPl6f5u2lwqVJD58xIBCu3UUWlac+dn3/7PGu1vXqtjsMXjo4/JvaDt8LM8lrRjQTm55yGpWVNO+ItUqSJj/q8U5LnQ5+N84Dp8/2c72VVS19qJF0a2avlWcoKUG8rw9x7VXtCFbuq4as5sqV4jsSP0wt8lsqu6MauonUPlypUqVqq0efNmIYQUNZs2bapQoULlypXZxQghtAATUhrIZAto3y7QVoTtF56HHylLl8iP05x9qix3G2c7NTYPcTthCm03UWUxs0RrY+Vv2ym39k/qatsY+gfC0F0C3XXqyqKF8uhI+e8biQ3D588vrWVRs52T30PyhklgpcKnwrj+qTZvGdeGuS3DXaG8VK2W2AvalbluWskfYuJmp369eoU7dqxbt04IIcVApUqVypUrt379eiGE5BO0ABNS5tAjdeO3c7Qiw7drn5ilaWvd6w7I7ULDbTsq1+uvtIHtBiosTEVrG9NKla5WoeCGjrrvYZk3V264yqOrmzSRW+7x5G3JEhl+WernrfckzGia806XrVuT8V9wGcYy8sBdyUQffVqefVImfOaJ/+wL5IC+8sgDMukrj//JpyZ2wAabNsv0afLvUbJtm0ef6PyL+P0ffUYWzJNbr0986mbUEzJ5kjx0Xyr8bfd6M3yabN2WdHfpLhdfLm+PlVdfkg4dZOgIOXtQKv6OneQf18jFZ8v6DXLQIXLKYPn73/z5ueMBadhQLjxL9OdhY/IpXh0bWv+gWQv56xBp2SbxLejnRjvznI14RtwkdevKORckf27ekiivir9rj1RxkPmhVyeKY6Z74l+k+/5SrVrikqf+5Um394FyzoWpVD4YJ//3jCfd2rXlvkecDA/P9L5k5K+arjbXuv6p1zeOv9bAttuN0M6Tr5yM+C0jfsvoNcofLQq9zPJLXQNLxHi15PhUqVxZffvXtm3Lsor12L59+zPOOKNNmzZLly598sknJ0+ebJ498sgjjznmmAYNGvzyyy9PPfXUrFmz9Nk+ffpcccUVr7766jPPPNO9e/drrrnmz3/+sz57+umn9+zZ84ILLoAbwapXr3799dfrs1ddddUBBxygq+Ddd9995JFH9NmaNWviwn322QcGujfffPONN94w84xs1KtXT1979913f/bZZ/oswqt6W7hw4UsvvfTJJ59kVRuPP/54o0aNhgwZsnr16syvqlu3LjLcqVMnCKovvvgCFWKefeutt3SWXn755fHjx5tnGzZsOHTo0NatWy9evBipT5061VfDxx9//Pbt2/v163fJJZeYNXzssceec845uh5mz5596aWXmjGfeeaZJ598cosWLd5///0bb7xRl6hVq1YjR440myCSRlSZ1+FRRx2F8r733nsPPfRQcbfPYjqif3EfLEKIcBMsQkofliXZYnmvbdBIli9PSgJxvwGjRvy23hDLOIovZKFxifnpI288hW7IHr1l96Yy4JiETcy8ZMNGmfJN4q+J84FyOCBHzQA//Sg/TEtsqLtoUeLsjh2p+CHgj/5T8udeHWW/nvLLTDf/7t8RRyfS7dPP79+ocSJFRDh/rvzpBBl+Q6A4ElJA5d9+L+l3mNSoKQf2k2bNpWVrT3h/ho06qVVLOnWWE/6acFevKXt39sRcvUbiqnLlE+7d6knHffzpQsT2P0IaN5HuPTPKp/kzqv7xB2Hc+yD5cJw0aChPPJ+oFvMsKnbjpuQ9wt+qlan4PcWp4RbHTfeIY+Sq62XDOpk4QU4/R6652RPtihWJ2CpUlIaNnbswz5+rHge4Ga6a6X3Jwr/Q3bkq2HrN9m84EtgigX4R/BNXZq9YluhlYvRWK7RDeihfvvyOHTuci5Lj9eJz//vf/z7ooIMgQSH8XnjhhXbt2ukw8IHCgfodN25c//7977rrLvPaOnXqdO7cedCgxOsbSNZ9993XjL9p06Z77bWXcrds2RIC27wWPrVq1frWZe7cuea1kMoQbxMnTly5cuWoUaOg4sxr9957b6gXfe2KFSvMa5GN5cuXT5kypX79+tCTvnTj3U2aNBkwYACOEOdZ1eGVV14JzYwMb9u27ZZbboFYNcOoLOHNArL02GOPtW3b1rwWkrh3796of9QY3KhzfS1qGNfCUAk3NL+qYX0t7gteXuh6mD59upk3SGW8knjnnXeQH7yJwBsHfe2mTZsQ/ptvvmnWLPG8hXvatGlZ1eGhhx6K3B599NG7oH0Wkxv9i19CIoQILcCElEWswC+vD9TOyhWJ8bpex6vWN9qmTdg96hmhqTWWttfeJf4wvrP79ZCJX0rvvgmT4KcfpsKsWiEP3J1w9+qTEELKba7SfOYJDLcTJsq3XpMvP/OcnfiFXHqFtGotv86SbvslFlsuXey5tnbdhDp99inp1iMkbyuWy8i7E+65v8nfzoetM2yNaNixQgX5eoIcerjs10um/5ASPOrsf56QWk6G33xN/veZf8XpksUJ7d2ylbduDbuiMq2HnBXp2VsWLJBfZyYE8KcfZZrb+PqvVDFRRSOGyrj/yn/HyiOjBaNwvBQwr53wqTw7OiROMYrj3u/U2Y4dZdbPctOIZMjW7TxnZ/yYeFNw7c3Stl3yLvjiVxnu1Vf2218+/jCLkmZ6tD2W25DSuR2nMGz9sK9z2e48fzMMRH7DRv6guuMYF5u/MTSHlLKTklu0o8jdVatWhe0RFshXXnkFttznnnuucePGP//8swrTtWvXihUrwtYHOQTBAEGlrtJHWA4hFyF0TX8ziWCK2ufXX3+FWVLC6NChA4yQykoJMx20n+9amHwffvhhiQAW19deew2O77///ogjjoDtWjKrkwMPPHD+/PkzZ87cf//9IR3ThtduaHIk+sADD8DdrVu3/fbb7+OPPzbDBLOk/HfffXfYY88++2xYUxEGIhmX66SDteqrf0jZmDqcN28e3l/AvWbNGtxWfdWiRYvUVSgvZPBNN90kWdYhDP64QTDy4y0GDMvF1z6Lz71169aCAhp+CCG0ABNSlrDiz7qnMTSHABZ3+J369qmktGvqbIR/mjDGcd9uCbvoj9MSdtr4eDJ3z5gh69YlVCjo3E2mfOsPA1G9bKl88G7CZlu9emQ8sDSqdwEZpgsg3mBV7tJdfv4pMkyof8WKCe16zHHhYZI+waPzD3QvdOO07xPpZltXUfUPGyxY66w4hTX+9FOcueIZ34tEcT5MFCcYpnxF2bQx6cZbjOuvCgkj0fGrDE+flih15vmJcdeqHfC3/WEKc4q/MOh2jsuXJd4OKOKnbBgnK5Qvn9j/2ZKQP8O181SqVAlHtdgYMunYY4/99NNP9dnKlSsnSrB8OY5r165VP00gjz/44IMTTzxRihTof70488ILL4zRujHAQFqjRo2sdvqFpfTHH3+cOnUqFKxkA+pBZxgVFTW3NpglFRIaEsdly5bhLUO1atWkKJg0aRJebQwbNqxFixZQ1E888YRkT2gdwvYL0Q5jNeR3nz59ZKeBnRlWbtm1oH9VwEtMQkjeQwFMSJkmdMDcAAJ4eWKobs4FTbj1xE6f2zxGhTHchYa7dm3Zo5V8M1GmfeeIt7DwCn1tofuFVeUWCff/9utEhHB37pJwF3rDQOz9MDWho7ZsSehk81rE1qSZPP2yPPNSQr89dJ//2hg3mPpdwjL5269SsZKTsbAwduBa+BSUk7ffSHyBWX+BNhXGqYHxX8nkmXLNP52z3ji7dpfvJsu338ieHRILa9PmU7trOfU/ya1/Tz24dXv4kXLJFYm/9h081+Lc5cMTWZr8s7w93l+HieK86RTHybyZbvKWxebNjggDE3oqw/ulL2PaNgmDz4OPS8e9/f6ZXJtyS/Jeh4ZJ+SsZXJjoXw0bZ9ofXaAHSsUHkKBUx44dO2DAgNCzbdq0me9wzDHHBM/2799/vgukmmTD8OHD1YVfffVV8Oyll14KAyZMlDCoquWsGQLD5pQpUyAdYT6tU6eOFB05ZymeunXr6jo844wzzFN4MQEzL2zLX3zxxYcffgjVKtkQk+G+ffvijYl6U9CrVy/ZaWBhVmuJZRdCAUwIUXAKNCF5iSk+/TYx099O2etS5q8IO57WsrbhPuAg2bxZ6jdI7F/Vtr1Urybr9A6ctj8/vmvNXPn84YZGGvI3ad5S6u4mX3zqWl/dMLAifvet7H+A/L4gYUj88D3PtZs2JTZnOv4UGfO8fPR+SH4i3c6vC86UVasS33rVOfSU3SiO6Y+h3ldfJgyne3Y0LlTnHPdBPWT1qsT2UUOv8pS3QUNpvkdC8tWokfjZo7dRnHR5jql/X92iMn+ZKdN/9MRz7+3yn6ckiG0bxekgvnowW1R8PoNhPBlul7Der1ufPh6f++BDnZntLqi3h56UYw4Ob3uZu+2YMFZ0uTKl0NxVrgQD0fLxxx/D/tmpU6fg2VmzZqnVsI8++mitWv6NN6HKzjzzTMmJO+64I8Ys/Ouvv0Lb7LnnntDYmX/nplmzZi1btkTN16xZUxyZ98Ybb0gRkVuW0sE0F3gAABAASURBVLJy5crOnTtHnR09evRLL7100EEHXXfddTfccIO5Y1ZaYjLco0ePuXPnQrUidbwykJx48sknYV7WP9u3b3/VVVfhtsoupLT0MkJIsUILMCFlmtBx+NLFiSWytl736xxNtxg7+kiYf/zRvKrH/rJhvZx3UUKT7Ngh+x8YdpXKqnuh5Tsqu1nAf+IXiTWrA4+TuXNlySLP2caNpMUe0qadnH9RYrPobvt5zoqzBviBO+X1l2Xg8VKxQiDF6KM4y4C//1bmzpZyVmQYkQh/O7Hj1AF9ku7g2aAbR4THYHTAUXL2+QmFjCrNMLc49nTq/3y3/nsdmDq7zdlSG8Uf97Y8eLeT5nZ/zYtEx++UURfHPIuEYB9W7r4Hy+AzwmojIs/BDKe5I2EtcPoPic29/zUqeZwzWz7/ODFnfifbdlSK/n4EI109Wbww0/7osm37djUp1Lfms8iPStuotAoKCiCTlJRVZ7dtS2xdrqZJq325QuMZN24cVFYR5goJqZ2f4IZsgwE57WpY8+zbb78NAybkjTKKZpjuwQcfjNo4+uijzz///FWrVinbZobXIi19v/A6QFnvzTCwpl522WUoFzS/6a9C4hJV/0DVuTq71dnrXhkqzWXhmdQDpClu5YYNG959913I4C5duoTWVQ51uN9++1WrVu3CCy9s1apVu3btdttttxzu8jPPPDNq1CgYfnF88cUXYVL+6KOPiqr9ZHJU9SmEkLyHApiQMoQdf9Y9vWRxwmpq+mi3HXBb2m1FhpGgv5V079tdnn9ahpwkQ05MTGpVq3aD8YTmAcJVhd+rQ8IwaBV4wvzyc0LHHjVQpkzyXwvVtHGjnHpcIt1brnUsn9VD0hr9mNSsJSedGlmuDPOp3V27Sw8nwx06JjadKigIufadsdK5a0g8RkV63AjTvYdj7nbq8JUXE58gSptP7Y6p/81bZPEiOXmQNG0mfx+a+NLvzBn+eJrvkah5lAXHOnVD4n/njWRxTP85s6T9nnL40YkF2FdcK13388RZr0EitvoNpVr1xB7UaidtfW0qwyclM5zJffG50cK/+ES+/DQxNeCrL+TXX+Saf4S3T4lpw9ptRYaRCDf6F/IQPBvEOKnmZ9qFzoeYbGfXLMedOCY6X2HyY0xh33fJyn/Tpk2LFy8eMmQIxMzVV1999tlnO9lMhle7Yf3jH/9o3br1X/7ylzlz5oTGM3bsWGWHDE3RPJpn69atO2DAgMMPPxxHvV+0ComEYHiEhPvTn/40fPjwpk2bmjHAsccee+hrGzVqZMas8g/jJHJ11llnQVtmWD89e/acOHEixPbAgQMhyZB65vX522+/IcOohFNPPRVmZLXHlS/kihUrYFL+29/+VrlyZX12wYIF69evhyeuuvbaa+H5448/6qt++OEHtAQoZ9T/SSedNHPmTF89oJHoeujdu7eZw0GDBkFb1q9fH2GgfpcvXx7MvyLUP1iHKmRzh8svvxy1dOyxxyJ7eHGQQzv89NNP33//fbw6wRE6/6KLLpo0adLOt+fM/VEtpWKVASGkuKEAJqSsY4v4lPFSRwAnR/mJ9Yvul35tSVqxHP/UvtDm92Dc8JbX3xOPcju7bTVrnlgArPy/n5yQiMHwYofHc/1tcveDCcdFw+SRJxO2Sh2/Cj/lW9m9SWLrJp9/t/0TK2ZVPInlwYVywMGe+FWFrFwu774pp5/tKFVv/iPL5Vam55vJbvgbbnczfLk88pRUKG/E4171w9TEDkmmj3jrWcSfbpf9ZOrk5KnJE6VN28RM5vh8Kv+09X/HTdKipbzzsfxliDzxaGLrZs99ETnpr4maR1lwTCzh1vEnzyc0qiqOme7YV2T8B4mvIr/8lqxZI4/c78lnz96J2Pr2k9ZtEw68gND5adAgkeHEDXXCqwxncl9i/DHeTew1HdbOQ+tft/9EIYPxKxuv2f4lJF30r6WuAHZrR/xC2P8bkkB9o8V2UW7zWFT+N910E/QkBMngwYMfffTRadOm6fAzZsx45JFH4P/JJ59AZ95+++2h8UC6qI2yskq3a9euTzzxxJNPPokjkjDDjxw5EhFCfcGBjD333HNmPABqXF8Lg6QZc7JCbRtlqVOnjhlzfH66des2efJk5f7mm29g28TlGdYnpCaMxrCa3nbbbTiq/ZOD4VWW1IejlD802PXXXw9T7WeffQZbN+KBytXh58+fj0vgj/pv27btvffe66uHGjVq6HpAPGaK99xzD15toCCzZ89u2LCh76wZSYy/WYeKfv36waqMioJ7y5YtkOgwlWd134P+L7/88oQJEzIPXyT+6F/KwE4IyXN26fYDhJAc8e0U4lqC3KPlbBCrHMpd4DjcvwIr5QOxd/WNsnqlvPayV5tFHBWp0X/0l5AKbf8XZXTI3L9Yw2PxHzt2SkhfjAuLNuYataRePZn9awkrrxXyZaMC8ztGqluZIS1/H/R3wMARqr5qVbnrltSGcJ4PZatdtdQx8Z8S0k13b7xj+/aVK1ZKCLYUA5B/P/3008aNG4OnqlatCgvtt99+K7sWSNA1a9YsWbJESgkdOnRYunSpeheQLbCjPvbYY6McfKdgxW3Tps2UKVNyWDwM6bvbbrtNnz5diJd69erBFAwLvBBC8onqdZr5fHb1HvSEkFyIEcBa/ZpK2HGmBLBYHnejxlK7TuKbOpad1KhxxzDFq7Wu9onSwMEwPJa049KlidW2RR7z1s2ycmVJKqnqNRmqX/GqX93CM0tr364ye5b8NF20cDVfJ4nt+ns8y5crV71aNfV1Ih+2d/5qUfkvWrRIrz71hYc/zhZTujH+K1asgLFx16ebsz+kb/ANQobxzJkzp2LFiuedd96LL764adMmMyTihE7DXcghn6jAZcuW5ZCfMu9ft25d9C9fVRNCyjwVq/h3ZOQUaEJKA57Rs/aM/Zn0Co6/7cTmvcedlLokuR7Sq1fFcFsSWDNphdmHHbXgu1ahtXpw7SXddBej23KataReIfnbtuVvq0m35Y/Hikgr1Wus1NnjT0n0MvXDtj29L9hRXY916zfUVBt9B7AivhZD/9Lu//DDD1922WWwt2cYnv4741+jRo3QF0yEkHyDApiQMoHt+Sc5zPaNtPUofMG8xNdxmzV3fnjXOiZ9rKSP5c7VFL3u0XbDW571tKkwVjKMZz2wG3Ny/15HNFiSFBCpGdd0071zbt2ukm3MbNu+NqnUr3ctetJtuWvdjfXAasayFegjqV7jprVHS1m7RhaF7QLtJmL0TVsfYO7bsnVrlSpVQlcz8lgmj7BGvvfee/PmzcvzetgFR7xlQG1zF2hCiHAKNCGlhuASRLHE0j99E6GNCc9OQPen62jQMLH379TvU7M6o462e1RKw/TXPj53lA+PPJaIo9spwn2028pxFvQxf07sOz1xQuIqZ/DtkFzom8IOuuyKFSpUrlx5w4YNQggpUnbbbTcI4PXr1wshJM/gFGhCyhJ2tJ/t99QDcTUK/+g96dPPGZRLasVv0L3DHdOLdxfcQltFmvAJum33aLkZKJSUvxmGbrp3kdvtCFayPxhhJNViTXeynevwWv1G9xfVzvseIh++51xkezpdsKP6PWXN2rU1a9YUQkhRU6NGjbVr1wohhFAAE1IWMUbtyT/lodci2vL9FFm9KrFRrT6vxuhaA9iuWrDNkbr2t9wLnUB6fK/9zXhEXCVsGWGs5PrMYPiY/NCf/nH+3nal25uJL7x+SZPwT77sSfrbyRPhfSEqP9VryrIl8uNUNyo7JYP9XdKWABs2bixfvlylSpWEEFJ0VK5cuXz58pxbQQhRUAATUgqxvUNnW4yBu53y1CNtw5Uakf/3zcTnav3rfi3P+kZx1wDr0b+KyuPjXferLGyWXpkZ+I5uMkxhcn2mDi/etcEeH/rTPxN/b7vytbpUOzTCm+uBRZ8V7zefXR9bUv0itL8gzCWXy9tveDqa2QE9vdL5bfscsnjJkkaNGqVCGJ2dbrrpzs3dsGHDxYt9n+YmhOQvFMCElGZsn9sO90/+GSNyOF4fI917yu67p6xY+ijuMbH5rakBdKRhq3+1vw4v2v5mpUL60uKRx+I9BqzBlvdsykd/D8nWU/8NHzXV2Ur1jmB7btZcOnWWt15L+ST/xKt7JUwDJ38tXbascuVKeltgcz9buummOwd3tWrVYAFeunSpEEKIAzfBIqT0YPyvPSUsUzrT3QdL9HeAzT+9LZYRw/x5cuZ5ifXAiSG4nTwWGm7RAkAMxev6pxwKYyBvu6ogiCs6/BRKZHj60z/e34puV+H+lj74fyq1rF/oWEaAVFSWka4K4xyv+ac8fL/MnZPUvf58eP/sYEaTjsLCwgYNGqxcuTLsLCEkO1q0aLFkyZLg55oJIXkCN8EipIwRMCrZhqdnvG2n/pJnbfn4A6nfUNrv5Rqp3L18TD1suZsJqUtEL300k9P+bkJi7IDly4PYnszoP8sOEQlCf/pn4B/TriTMAKuvSvobPy1JuU2HTtoWz9Fye0SHvaVWbfnsY08XCxqBbSMPts+R7FHLV6woV66gRo3qEpZ1Qkjm1KxZ07bt5cuXCyGEuFAAE1I6SQ2yfUfT36cTjGv1oPzKS2XIWVK4IxWLLZ4vvhiXGXNERYIzn5VysPRsZzetpL8KaPmPYobnkcedO4a2Md0CbbeFJ1uyZfi7Ie1AOzf7jv/bYG6chYUy+Ey56jKnq9kBC7DtleuGvy9U0mEvXLSoSZMm5cuXF0JIrqAHoR8tXLhQCCHEgFOgCSk9WFbYz5hZ0PpTwFZyfO+7HH6rVybG7mdfIJ98ZA7q3TDuWF//8PsYsdlGGH3SMpSJT0ukruWRxyI6hmCcTulhbxtO9SzddyTpEMNhu/6pC13HLXfL2DEy+Rv3LZIdbv5NEjP/OcnmzZurVK5cv379VatWCSEkeyzLatWq1fr165csWSKEkDyGU6AJKc2Er6q1jX/dwbe4li5bn7P91mA9Oh/3tvy+QP46JKV+bUmZqlJToN2pnpYxcdQyZj5bttfOLCFzm02VEnTbhgCnm+4M3SKx7cq9wDLkaArt74TSk5xtSfmr37rl6586E0POlF9nOd/+NW2/duDPyLCYs6yNzBjMmz9/27ZtTZs2TZxw4uSRRx4zPzZr1gw9aN68eUIIIV5oASakVJG1ETgZLvDnZcLn8vfLZP06mTfHHeJLanReIO7A3VGwhW4AHUaloOdLW8aY3hKPSrHdy1JuoZvu4nFbHn8JhrGSbm3TtV27rnKnupVDsi/oMI7joEOlbz+59h9OgIhFv8k/12WLF93dJBmJy+o1axo2bFiuXLmNGzdiTK92tcWRbrrpjnfXr1+/WrVqs2bNsm1/fyOE5BtBCzAFMCGlinAB7DpSx7AdoUWCyte9vEDGviLnXiTbtyc0sKW+7xL8Koxa6+uun1RuFW9SRXjXAKfC2AG3kVu66S4Wd6DtJY4FIWFMH3HDFLjh3W7AiQM8AAAMNElEQVRghFRhbDn4UOnVRy49P/nTDt2CyxDByaG44UgRMkzH2H3N6tUwAhcUFGzYsEEIIRnQoEGDOnXq/PLLLzt27BBCSN4TFMCWEEJKF5YV5o5dCSzuN5As79pgy/zDCL5QRr8gEyfI8884cbnDdCu4VY8d4hYJG9aHe0j2IQiJxcr+vBXwt4yfVsBurMM7Gvi0s2XfbnLO4GTfCepe21014PEUv0N8fcrsUAl3hQoVWrVqtX379nnz5tGcRUgMeFXUvHlzHGfPno0uI4QQIlK9TjOfD9cAE1KaSY2GA6Yk27U4JcfWofvx2KlIMILHOP5vg6RGLfnnnYmf4khfS38bxr3Qcofstm24RcyoLQkk5Px51gObbiP7dNOdiztdGzOCuNcahtnUux7vex/bjd92u4M4neXWe6VSJTnvtKT6FUmpXPFOe7Z9qZiLhDVh6tdl27ZtsGVhNN+mTRuIYSGEhIHegT6CnqL6ixBCSAScAk1IacOyIn6GGoG1wUpSE6GNi1MTRLXH/76Q8uXlgktlwXxZtjTpWag1htYPtsffcsfw6qxt7AWt9YYV+IoMjzwW97EgrB3a4s5ndn3E9Skw3D5/1cI77iPDr5e3x8rzT3utvuKqXK8pWHybabndRMQw/6YhMRd6zZpy5co1a9YM7k2bNgkhxGC33XZD71i6dCk/ekQI8cEp0ISUCaI0sOUO5y33GDIRWlyH909drv/atU/YuJYvk/vvlPnzkppWrKSyLdQrKiW5ijLpU+hZbynm2svAWR553EXHAo+PhJ0t8K4HTvqIEV6k+R4y9CqpU0eGD5Xffk1KXFtPYy4MUb/KR0InP0tS+9quAra9UtgOUcZVq1Zt3LhxpUqVFixYoHfG4pHHfD5Wq1atSZMmW7ZsWbRoETqFEEKIl+AUaApgQkohVoQAFu++tZYVJoZDlwFLiCoG/Q6TETfKN1/LA3fI2nUp+1UCn/HK9v0b/CGZnSGkCLAyO2cFXFbwpyU1a8mw4dK5m9x+g/PFbK/QNbWu7V3u61e/kvwppvk3CwGsqF69+u67775t2zYYuzjVk+Qt5cuXR0eoUKECOsL69euFEELCoAAmpKxgZWwE9pmCM9TAYhiEjztZBhwtdXeT8R/Ipx/J7F+MmczGlE7TR884DZ/zbO/qebA85uPRCvEviA4jXh+EbN0usc9zv8MTawHGvSVvvOo1+dohP8W7/ZVEGH7VUV2lyFj9amrXrl2/fn0YwdatW7d27dqtW7cKIXlAxYoVa9asWaNGDZh/ly5dumbNGiGEkGgogAkpK1hWhI/eujZK/Ro/owSwii2lkJ2f+3SRQw6Tw46UatXkpedl8yZZvlSWLUtoA/xtdieeFRrPlaSusA23xLkLMwhDN90+d0Hm4a3IaytXlQYNpF4DqV9f6jeUypXllMGydq18OC7x3mfad945zEHRK37br4QZfv3qV/wyWJOBAFbA/AUlAD1QqVKlDRs2bNmyZbsD7MM42hnHQ0gJBBIXZl408vIOaOTVqlXbvHmzeunD6Q+EkEygACakDJHhROh4DSxhVl8Rv6d5bZPm0rOXtNtT6jeQBg2lYSNp2FiqVxdCSi/r18vihbJ0SfLvlxny1f9k4Xy/ghXJQABLnPoV2ZnJz/FUr169SpUqlStXhk6o7ADNoNZJuhHTTXdpckPibnbAmx0cN23axKnOhJBsoQAmpAwRaQQOOEJ1rPgMvyISrYRDojLiEfGanVO/I54xfPKQXYAd6+ezwbqefpnqPYY7vBOePTJYPMpZH0MdqazRbEsIIYQUDUEBXF4IIaWU5Ja2oadcjWmbyx1td4mj7R7Fkaw+RyAWO7izrju3WcUjklw5KW5UYqcyIOIVyRKuTAgpJmzPPyE+UXOSw49a5Uo26tebhZgeQPVLCCGEFCcUwISUIVKS2DYUqVa8URrYH4vXQmuHGWzVLlaWNyFxLcB6xK8NwoYGSEE7MCkm7NgzdvhPn/qVzKVvqO4Vr/oNW/orlLuEEELIroYCmJDSTNAInJ0GFo87iZUapnusx14jcCotLYbNRMX9qeP0/Js8S0hxY4e4jF/RE5JtO7Nj9MeNclC/1MOEEEJIMUMBTEgpJ3cNLCmt670+NWM5yj7s18C+RN2wqYzZvn8lmQAhxUGsjIyRnX6H25jTSN/AUYTqlxBCCCmZUAATUhaJ08CSMuxatn86tDIImxbglEtJX726OEwDK7TuDfp4cymE7DLSCs40MtgUw3bKgBwUulGiN179EkIIIWSXQAFMSOkndDesSA0sXoNwUBibtl87fAGwZ4st16QsXt1rZim34b5FEzEJY+fVoz8G2zNT2g51eGVwtibftOqXkpgQQgjZJVAAE1ImyEIDm5tX2SnjbnAXaNMaLD4trK3BWgMbbp26iP+rSNkWipAiQwvRgH+o+tWBfdOho2y8IaLX6DtUv4QQQkjJgAKYkLJCphpYjbajrL4+GWyH7AhtB/eyMjWweGWw+4/nEpp2yS7ADnX6A9ihP6PtwCKRWjfoL1S/hBBCSMmCApiQMkTmGlgC86J9qjjy48CpeJNiWHx2YHGH+5Y/uMbiiJ8UP3YG50JsvxKphEViNbBQ/RJCCCElHwpgQsoW6TWwpL7WG651I9SvlVZRuBo4GT5MBuuwMdA8TDIkF/Hos/qGenoFsERo2sylr1D9EkIIISUFCmBCyhxpNLAETMGS+pyvKXpTijcrJexP2HBnJm0pCkgRY6fzCBPAkoEtN8rAS/VLCCGElFQogAkpi0RpYJEwU7Ce/2z4qzAiXvUbpn3TbBlNyB9OvAC2A047+qcd5p+l9BWqX0IIIeQPgwKYkDJKqAaWoClYvNLXtQYnPJxgpvq19OjfVcgeRWz8CLcShw76qZlJEZKxsEyjgSXaDiwhE56DP4XqlxBCCCmJUAATUnaJ0cAi/hnRIoY1WELkbvAjSZKV+vVdmcqNEFJc2BmftAOn4i3D0WclVuJS/RJCCCF/KBTAhJRpojSwBEzBIp5J0RJq+JVwMawkrzcy71lPwkLIH4Md622n8bQljU5OelL9EkIIISUXCmBCyjp+e2/8Ke/a4JSPpGZKi1cMq9+RVl/vCc53JrsYO83vMO9MVK5Q+hJCCCGlEQpgQvKDeFOwhMpgiVDCkrIDGydT/t7YPd5UAeSPws74hB19gR3lHz/Xmu2eEEIIKSlQABOSN8SYgsUYo0cpYRGPGBbx62HxSmJP5JITtBeTUIpUT9ohrrAA2eteofQlhBBCShwUwITkGfEyODJAcBlw4KzEzILOgJBQFA8kMzJtKdnuEb0T2zhT+hJCCCElEgpgQvKSDGWwIk4Mi0e5hseXmRKgXiB/CDGrf/0hM2zJbMqEEEJIyYUCmJA8Jq0MNoMprIhVvgGnvkCyhROfSYbkojSzvCYrNUvpSwghhJR4KIAJyXvCV/+mC5zpJdlLAooI8geSg4il7iWEEEJKDxTAhBCXDA3CwUtCsWjJJSWVIpGs1L2EEEJIKYQCmBDiJc2E55ziIaTMwIZNCCGElGYogAkh0RSVGCakVEPRSwghhJQVKIAJIZkR1ACUxKRMQrlLCCGElF0ogAkhuRKvEyiPSYmFEpcQQgjJVyiACSHFAzUGIYQQQggpYRQIIYQQQgghhBCSB1AAE0IIIYQQQgjJCyiACSGEEEIIIYTkBRTAhBBCCCGEEELyAgpgQgghhBBCCCF5AQUwIYQQQgghhJC8gAKYEEIIIYQQQkheQAFMCCGEEEIIISQvoAAmhBBCCCGEEJIXUAATQgghhBBCCMkLKIAJIYQQQgghhOQFFMCEEEIIIYQQQvICCmBCCCGEEEIIIXkBBTAhhBBCCCGEkLyAApgQQgghhBBCSF5AAUwIIYQQQgghJC+gACaEEEIIIYQQkhdQABNCCCGEEEIIyQsogAkhhBBCCCGE5AUUwIQQQgghhBBC8gIKYEIIIYQQQggheQEFMCGEEEIIIYSQvIACmBBCCCGEEEJIXkABTAghhBBCCCEkL6AAJoQQQgghhBCSF1AAE0IIIYQQQgjJCyiACSGEEEIIIYTkBRTAhBBCCCGEEELyAgpgQgghhJRoqlSp0qtXLxw7d+4shBBCyE5AAUwIIYSQEk3Tpk0tyzr44IPr1q0rfwQtW7Y88MADhRBCSOnn/wEAAP//k37SjgAAAAZJREFUAwDegloJq9BnUAAAAABJRU5ErkJggg==', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(23:59:22)*


## 🤖 Claude *(23:59:24)*

Hero excelente — a **explosão de partículas** (constelação + filamentos) renderiza no topo, headline com Playfair (cyan "inteira" / gold "você"), nav completa, 0 erros de console. Vou capturar as seções-chave, sobretudo a de "Ativar" (prova visual de que não há preços R$):

## 🤖 Claude *(23:59:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSP=\"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad\"\n# scroll para a se\u00e7\u00e3o A ORQUESTRA (pilares CEO/PMO/PMI)\nagent-browser scrollintoview \"#orquestra\" 2>&1 | tail -1; sleep 1.2\nagent-browser screenshot \"$SP/lp-2-orquestra.png\" 2>&1 | tail -1\n# scroll para ATIVAR (planos honestos, sem R$)\nagent-browser scrollintoview \"#ativar\" 2>&1 | tail -1; sleep 1.2\nagent-browser screenshot \"$SP/lp-3-ativar.png\" 2>&1 | tail -1\n# canvas dims (confirmar full-hero)\nagent-browser eval \"(() => { const c=document.querySelector('.lp-hero-field'); const r=c?.getBoundingClientRect(); return JSON.stringify({w:Math.round(r?.w||r?.width),h:Math.round(r?.height), nodesVisibleHint: !!c}); })()\" 2>&1 | tail -3",
  "description": "Screenshot orchestra pillars and honest activation section, check canvas dims"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Done
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/lp-2-orquestra.png
> ✓ Done
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/0c1ad55a-1aef-4790-9a42-92684bcd77d2/scratchpad/lp-3-ativar.png
> "{\"w\":300,\"h\":150,\"nodesVisibleHint\":true}"
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-03 - Executar loop autônomo MCORCH com charter]]
> * **Próxima Sessão**: [[2026-07-03 - Resolver alertas de produção e migrations]]
%% --- TIMELINE END --- %%

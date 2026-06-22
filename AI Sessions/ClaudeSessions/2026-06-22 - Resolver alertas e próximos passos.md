# Resolver alertas e próximos passos
**Date:** 2026-06-22 | **Session ID:** `f232593a-1ef8-4045-8b83-67389d10213f`

---

## 👤 User *(12:49:44)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(12:49:44)*

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


## 🤖 Claude *(12:49:48)*


## 🤖 Claude *(12:49:49)*

I'll execute the ShakeHands pick-up protocol. Starting with the pre-flight gathering in parallel.

## 🤖 Claude *(12:49:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7",
  "description": "Recent commit history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> b76f1d5 docs(handoff): seal camada criativa + módulo Vídeo (BoK 9/9 + agência v1.1) + SSO + tenancy
> a1d7303 docs(readme): v6.45.0 — camada criativa + módulo Vídeo (BoK 9/9 + agência v1.1) + SSO + tenancy
> 96079a5 chore: gitignore public/canvas-design (assets runtime do worker design-bridge)
> bcd85ce feat(video-studio): fundação de tenancy de agência (org/client + RLS anti-recursão)
> 6eca4bc feat(sso): gate de auth cross-subdomínio MCORCH p/ apps isolados (R3)
> f003e32 docs(bok): video-studio BoK 9/9 + emenda v1.1 (camada de alavancagem de agência)
> 04aa683 feat(canvas-design): editor via design.mcorch.com + SOP deploy/provision
> ```

## 🤖 Claude *(12:49:50)*


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

## 🤖 Claude *(12:49:51)*


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

## 🤖 Claude *(12:49:51)*


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

## 🤖 Claude *(12:49:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker mesh status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 5 days (healthy)
> mcorch_claude_mem: Up 6 days (healthy)
> mcorch_chroma: Up 6 days (healthy)
> ---
> mega-brain-dashboard: Up 6 days
> mega-brain-webhook: Up 6 days (healthy)
> mega-brain-daemon: Up 6 days (healthy)
> ```

## 🤖 Claude *(12:49:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat",
  "description": "Chroma API v2 health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1782132593822283595}
> ```

## 🤖 Claude *(12:49:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "BoK suites + scratch check"
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
> video-studio
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> ---SCRATCH---
> scratch has files
> ```

## 🤖 Claude *(12:49:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l HANDOFF.md",
  "description": "HANDOFF.md total lines"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 8158 HANDOFF.md
> ```

## 🤖 Claude *(12:49:59)*


## 🤖 Claude *(12:50:00)*

Clean tree, zero TS errors, all containers healthy. Now reading HANDOFF head/tail and context files in parallel.

## 🤖 Claude *(12:50:01)*


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
> 14	## Session Seal — Camada Criativa + Módulo Vídeo (BoK video-studio 9/9 + emenda agência v1.1) + SSO cross-subdomínio + Fundação de Tenancy de Agência (2026-06-22)
> 15	
> 16	`/handson` → diretiva Sovereign multi-parte: **(1)** validar/reparar a camada criativa (Studio Design + Canvas Studio — "sem criativo só texto funciona"); **(2)** integrar o módulo Vídeo (estúdio faceless `/home/gcrUX/studio` + editor HyperFrames) como **app isolado sob MCORCH** (auth + mcoCoins + BYOK per-user). Arco: probe-first → BoK gate (Sovereign escolheu `/bok-scribe`) → **revisão adversarial da BoK pela lente de alavancagem de agência** → emenda v1.1 → implementação **R3 (SSO)** + **fundação de tenancy** com `/security-review`.
> 17	
> 18	**O que foi entregue (7 commits granulares):**
> 19	1. **Camada criativa validada+reparada (`2a217eb`/`dd5c749`/`04aa683`).** `generate-image` tinha **todas** as rotas mortas (nanobana DNS · openrouter `/v1/images` deprecado 404 · openai images sem acesso) → portado o path provado do `canvas-execute` (OpenRouter chat-completions multimodal Gemini + Replicate FLUX + OpenAI fallback), preservando auth dual-path + contrato `path/image_url`. **Olho criativo** Vision MCP (`scripts/qa/vision-qa.ts` — describe/analyze/compare, BYOK grátis) + SOP `creative-qa-vision-gate.md` (portão de consistência frame-A↔frame-B antes do crédito de vídeo). Canvas Studio E2E pago: imagem (10mco) · **vídeo DoP Higgsfield real** (mp4 6.4MB, −125mco atômico, `analyze_video` aprovou) · áudio TTS (WAV 24kHz). **Canvas Design (open-design) de não-funcional a headless funcional** (worker systemd `design-bridge.service` + provider provisionado + geração real 1.27MB via OpenRouter + nó `design_artifact` na malha); SOP `canvas-design-deploy-and-provision.md` (achado OTD-003: `od` é cliente fino → daemon compartilhado → config global single-tenant).
> 20	2. **Módulo Vídeo — BoK `video-studio` 9/9 + emenda v1.1 (`f003e32`).** Estúdio faceless (n8n `e7e3beeb` → Gemini/Pollinations/VoxCPM/Remotion:8088/LTX/FFmpeg/QA) + editor HyperFrames (Apache-2.0, React NLE) como app isolado. Recon material (5 agentes) ancorou cada fato. Revisão adversarial (11 agentes) achou que a v1.0 (solo-creator) **não cobria a alavancagem de agência** → emenda superset **v1.1**: hierarquia `organizations`→`clients`, white-label, wholesale mcoCoins, erasure per-cliente, RBAC/seats, posicionamento "agência de conteúdo em caixa". Selos na malha: `e5e16090` (v1) + `c99b7875` (v1.1, DERIVES_FROM viral-autopilot).
> 21	3. **R3 — SSO cross-subdomínio (`6eca4bc`).** `design`/`video.mcorch.com` agora exigem login MCORCH: cookie `.mcorch.com` (`sb-mcorch-session`, sincronizado pelo SPA) + gate `sso-auth-gate.service` (bun, JWKS ES256, systemd) + nginx `auth_request` → `302 login.mcorch.com/auth?return_to` se anônimo. `return_to` anti-open-redirect (só `*.mcorch.com`).
> 22	4. **Fundação de tenancy de agência (`bcd85ce`).** Migrations `20260622030000` (+hotfix `030100`): `organizations`/`organization_members`/`clients` + helpers SECURITY DEFINER **anti-recursão** (`is_org_member`/`org_role` — o stub do BoK tinha subquery auto-referente que loopava) + RPC `create_organization` (bootstrap atômico).
> 23	
> 24	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (GOs via AskUserQuestion) + `/security-review` independente (Ultracode finder→verificadores≥8) · Owner=Sovereign (blast radius = apps isolados públicos + carteira wholesale + isolamento multi-tenant).
> 25	
> 26	| Verificação (material) | Resultado |
> 27	|---|---|
> 28	| `generate-image` reparado | ✅ deploy 129.4kB · img real 963KB PNG · olho criativo `high` |
> 29	| Vídeo DoP E2E | ✅ mp4 6.466.887 B · ledger −125 `canvas_video_spend` · saldo 5241→5096 |
> 30	| Canvas Design headless | ✅ job real `complete` · PNG 1024² 1.27MB · nó `design_artifact` `58fd73ae` |
> 31	| BoK video-studio | ✅ 9/9 (2536 linhas) · selos `e5e16090` (v1) + `c99b7875` (v1.1) embedded · 0 FR-VS órfãos |
> 32	| R3 SSO | ✅ sem cookie→302 login · JWT válido→200 · gate systemd `active` |
> 33	| `/security-review` | ✅ 3 HIGH achados (conf 9) **todos fechados** + re-provados (mint→403, saldo 0) |
> 34	| Tenancy migration | ✅ `db push` exit 0 · 3 tabelas · helpers anti-recursão · create_organization RPC |
> 35	| tsc · commits | ✅ 0 erros · 7 commits granulares |
> 36	
> 37	### Survival Laws Self-audit
> 38	```
> 39	Law 1 (Materiality): ✅ Toda claim provada NESTE arco — generate-image via 963KB PNG + olho criativo; vídeo via ledger −125 + asset 6.4MB; Canvas Design via job complete + nó; BoK via UUIDs de selo + embedding NOT NULL; SSO via 302/200 reais; security via mint→403 + saldo 0. O teste material PEGOU o fix de GRANT aditivo falho (não confiei na estrutura). Fase 5c mecânica abaixo.
> 40	Law 2 (Process): ✅ SOPs antecipados ([[creative-qa-vision-gate|creative-qa-vision-gate]] · [[canvas-design-deploy-and-provision|canvas-design-deploy-and-provision]]) ANTES da automação; BoK 9/9 + emenda v1.1 antes de código do módulo Vídeo (Master Protocol).
> 41	Law 3 (Pruning): ✅ Sessão longa empacotada (criativo→BoK→review→emenda→R3→tenancy) sob GOs explícitos; recon/review referenciados por path; selada a pedido do Sovereign (/handoff).
> 42	Law 4 (ORO): ✅ Triplet declarado; múltiplos GOs via AskUserQuestion; /security-review como Reviewer mecânico independente.
> 43	```
> 44	
> 45	## Session Seal — Viral Autopilot Fatia 2: cadência R2 + loop R3 auto-melhorável + UI (FR-VA-002/005/007/008/010/011/014/016/021) (2026-06-20)
> 46	
> 47	`/handson` → diretiva Sovereign "vamos aos próximos passos" sobre o roadmap do Viral Autopilot (BoK gate ABERTO). Arco Closed-Loop por fatia (mapeamento do contrato vivo → escopo → SOP Lei 2 → código → /security-review → deploy → smoke zero-cost → seal), 4 GOs soberanos via AskUserQuestion. **Motor de conteúdo viral autônomo COMPLETO (R1+R2+R3+R4), tudo provado materialmente sem gastar 1 centavo do Sovereign.**
> 48	
> 49	**O que foi entregue (5 commits granulares):**
> 50	1. **Fundação (`686bae3`) — gate Lei 2 + tabelas + RPCs de dinheiro.** SOP antecipado `docs/processes/autopilot-cron-identity.md` (OTD-VA-008, 10 gates: identidade cron server-trusted + atomicidade pré-débito/refund). Migrations `20260620120000..120300`: `autopilot_plans`/`autopilot_cycles` (FK composta tenant-escopada `(plan_id,user_id)`, RESTRICTIVE no-delete, fecha a FK composta pendente de `creative_metrics`) + `begin_autopilot_cycle` (cap diário+ciclo+saldo + pré-débito ÚNICO sob `pg_advisory_xact_lock` anti-TOCTOU, service-role-only) + `finalize_autopilot_cycle` (refund crédito-positivo idempotente claim-once, espelha `finalize_vision_job`; nunca deduct negativo).
> 51	2. **Smoke RPC (`0c59e4d`) — 11/11 zero-cost.** `smoke-autopilot-budget.ts`: pré-débito exato · cap diário/ciclo/saldo abortam sem deduzir · refund idempotente · clamp anti-mint · FK CASCADE.
> 52	3. **Edge functions (`54ac2a9`) — executor + driver + caminho prepaid.** `autopilot-run` (identidade 2-caminhos service-role+header OU user-JWT+load tenant-scoped → begin → fan-out `orchestrate-content` prepaid → finalize → re-arma `next_run_at`; dry_run zero-cost) · `autopilot-cadence-cron` (driver pg_cron, espelha nurture-cron, 403 sem service-key) · `orchestrate-content` FR-VA-016 (caminho cron prepaid pula o débito SEM tocar sentinel/produtos/kick; user-path 100% intacto). `verify_jwt=false` no config.toml.
> 53	4. **R3 loop (`35554da`) — auto-melhorável.** `autopilot-analyze` (FR-VA-010: tenant da linha do ciclo, ranqueia `creative_metrics`→`optimization_policy`; 2mco só standalone+real-data; não inventa) · `autopilot-collect` (FR-VA-008: `affiliate_links`→`creative_metrics`; orgânico fail-soft) · `orchestrate-step` FR-VA-011 (lê policy do tenant → injeta diretiva vencedora nos 3 prompts + taggeia `cycle_id`; hint sanitizado).
> 54	5. **UI (`bfd178b`) — usável.** `useAutopilot` (hook harness CRUD + ciclos + run-now/Simular + pause/activate) + `AutopilotPage` (`/dashboard/autopilot`: empty-state + cards + dialog de criação) + rota lazy + nav. types.ts regen (additive).
> 55	
> 56	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (4 GOs AskUserQuestion) + `/security-review` independente **SAFE 3×** (migrations 6-vetores · edge fns 6-vetores · R3 7-classes) · Owner=Sovereign (blast radius = carteira do tenant gasta autonomamente).
> 57	
> 58	| Verificação (material) | Resultado |
> 59	|---|---|
> 60	| Migrations | ✅ `db push` exit 0 + Management API (2 tabelas · RLS 2/2 · 6 policies · 2 RPCs · 5 constraints · grants anon/auth=false svc=true) |
> 61	| Prova comportamental RPC | ✅ anon→401 `42501 permission denied` · service `projected=0`→`22023` guard antes de débito |
> 62	| Edge fns deployadas | ✅ orchestrate-content 114.8 · autopilot-run 63.1 · cadence-cron 59.52 · analyze 60.92 · collect 59.72 · orchestrate-step 132 kB |
> 63	| `/security-review` | ✅ SAFE 3× (0 findings ≥ High) |
> 64	| Smokes zero-cost (31 gates) | ✅ budget 11/11 · run 9/9 · loop 11/11 (usuário descartável) |
> 65	| UI render (ocular) | ✅ `/dashboard/autopilot` heading+empty-state+nav+HUD 5241 (preview local à prova de CF, sessão injetada, sem redirect /auth) |
> 66	| tsc | ✅ 0 erros |
> 67	| Commits | `686bae3` · `0c59e4d` · `54ac2a9` · `35554da` · `bfd178b` · readme · handoff |
> 68	
> 69	### Survival Laws Self-audit
> 70	```
> 71	Law 1 (Materiality): ✅ Toda claim provada NESTE turno — migrations via Management API real, RPCs via curl 401/22023, smokes via SELECT real (delta saldo, idempotência), UI via DOM text + screenshot ocular. NÃO fabriquei: o 1º ciclo PAGO real foi declarado gated (Sovereign + 2 blockers CF/OpenAI), não simulado. Fase 5c mecânica abaixo.
> ```

## 🤖 Claude *(12:50:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7758,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7758	ContentLibraryPage monetization flow:
> 7759	  Card (text, body contains mercadolivre.com.br)
> 7760	    └── DropdownMenu → "Monetizar Links ML"
> 7761	          → handleMonetizeLinks(item):
> 7762	               match(ML_URL_RE) → unique URLs
> 7763	               for url of unique:
> 7764	                 POST process-affiliate-link → affiliate_url
> 7765	                 body.split(url).join(affiliate_url)
> 7766	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7767	          → Badge 💰 ML (emerald) exibido após monetização
> 7768	```
> 7769	
> 7770	---
> 7771	
> 7772	## Pending Actions (Commercial Launch)
> 7773	
> 7774	### CRITICAL — Must complete before first client
> 7775	
> 7776	🎯. **[Fatias 1/1b/2 SHIPPED — pendente: ativação Sovereign + trends] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 7777	
> 7778	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 7779	
> 7780	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7781	
> 7782	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7783	
> 7784	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7785	
> 7786	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7787	
> 7788	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7789	
> 7790	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7791	
> 7792	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7793	
> 7794	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7795	
> 7796	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7797	
> 7798	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7799	   ```bash
> 7800	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7801	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7802	   ```
> 7803	
> 7804	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7805	
> 7806	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7807	
> 7808	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7809	
> 7810	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7811	
> 7812	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7813	
> 7814	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7815	
> 7816	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7817	
> 7818	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7819	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7820	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7821	
> 7822	### SOCIAL — Next steps
> 7823	
> 7824	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7825	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7826	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7827	
> 7828	### NON-CRITICAL
> 7829	
> 7830	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7831	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7832	- `browserslist` — ✅ updated (2026-04-26)
> 7833	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7834	
> 7835	### GITNEXUS MCP — Next steps
> 7836	
> 7837	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7838	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7839	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7840	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7841	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7842	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7843	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7844	
> 7845	### PHASE EPSILON — Next iterations
> 7846	
> 7847	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7848	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7849	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7850	
> 7851	### CORE — Next iterations
> 7852	
> 7853	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7854	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7855	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7856	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7857	
> 7858	### PHASE DELTA — Next iterations
> 7859	
> 7860	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7861	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7862	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7863	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7864	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7865	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7866	
> 7867	### USUÁRIO ZERO — Checklist de validação
> 7868	
> 7869	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7870	- ✅ Stripe sandbox secrets no vault
> 7871	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7872	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7873	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7874	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7875	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7876	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7877	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7878	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7879	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7880	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7881	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7882	
> 7883	---
> 7884	
> 7885	## Infrastructure
> 7886	
> 7887	| Service | Container | Port | Status |
> 7888	|---------|-----------|------|--------|
> 7889	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7890	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7891	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7892	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7893	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7894	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7895	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7896	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7897	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7898	
> 7899	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7900	
> 7901	```bash
> 7902	docker compose up -d
> 7903	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7904	```
> 7905	
> 7906	---
> 7907	
> 7908	## Security Model (Post-Go-Live)
> 7909	
> 7910	| Table | Isolation |
> 7911	|-------|-----------|
> 7912	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 7913	| `mcorch_edges` | Same pattern |
> 7914	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 7915	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 7916	
> 7917	---
> 7918	
> 7919	## Billing Architecture
> 7920	
> 7921	| Decision | Value |
> 7922	|----------|-------|
> 7923	| Canonical billing ledger | `profiles.mco_balance` |
> 7924	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 7925	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 7926	| Orchestration cost | 10 mcoCoins/run |
> 7927	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 7928	| Stripe | Sandbox keys active — swap to live before first client |
> 7929	
> 7930	---
> 7931	
> 7932	## GraphRAG State
> 7933	
> 7934	- **8935 total nodes** (verificado live 2026-06-20 via REST count=exact, viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 7935	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 7936	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 7937	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 7938	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 7939	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 7940	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 7941	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 7942	- HNSW cosine index operational
> 7943	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 7944	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 7945	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 7946	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 7947	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 7948	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 7949	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 7950	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 7951	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 7952	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 7953	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 7954	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 7955	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 7956	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 7957	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 7958	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 7959	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 7960	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 7961	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 7962	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 7963	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 7964	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 7965	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 7966	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 7967	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 7968	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 7969	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 7970	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 7971	
> 7972	### Embedding Model
> 7973	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 7974	Schema: `vector(768)` — HNSW cosine index.
> 7975	
> 7976	### Embedding Pipeline (Autônomo — 2026-05-03)
> 7977	Três camadas eliminam intervenção manual:
> 7978	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 7979	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 7980	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 7981	
> 7982	### Comandos de manutenção da Mesh
> 7983	```bash
> 7984	# Verificar nós sem embedding (deveria retornar array vazio):
> 7985	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 7986	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 7987	
> 7988	# Backfill manual (Bun-native — requer .env):
> 7989	bun run scripts/backfill-embeddings.ts
> 7990	
> 7991	# Backfill de código-fonte nos nós AST:
> 7992	bun run scripts/backfill-node-content.ts
> 7993	
> 7994	# Re-sync AST completo:
> 7995	cd packages/gitnexus-core && npm run sync-mesh
> 7996	
> 7997	# Acompanhar re-ingesta pós-commit:
> 7998	tail -f /tmp/mcorch-ingest.log
> 7999	```
> 8000	
> 8001	---
> 8002	
> 8003	## Video Rescue Protocol
> 8004	
> 8005	When a video generation operation (Google Veo) times out or client disconnects:
> 8006	```bash
> 8007	# Via edge function (production):
> 8008	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8009	  -H "Authorization: Bearer <user_jwt>" \
> 8010	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8011	
> 8012	# Via local script (admin/debug):
> 8013	source .env && bun run rescue.ts <operation_id> <content_id>
> 8014	```
> 8015	
> 8016	---
> 8017	
> 8018	## Architecture Pillars
> 8019	
> 8020	| Layer | Implementation |
> 8021	|-------|---------------|
> 8022	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8023	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8024	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8025	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8026	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8027	
> 8028	---
> 8029	
> 8030	## Phase Delta — Architecture
> 8031	
> 8032	```
> 8033	OrchestrationPage (full-canvas, p-0)
> 8034	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8035	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8036	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8037	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8038	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8039	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8040	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8041	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8042	
> 8043	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8044	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8045	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8046	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8047	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8048	```
> 8049	
> 8050	### Canvas State Architecture (Hybrid)
> 8051	
> 8052	```
> 8053	User interaction → ReactFlow internal state (positions, drag)
> 8054	                         ↓ (debounced 600ms)
> 8055	                   localStorage (positions persist across refresh)
> 8056	                         ↑
> 8057	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8058	     ↓ (status changes sync to ReactFlow via useEffect)
> 8059	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8060	```
> 8061	
> 8062	## Key Files
> 8063	
> 8064	| Purpose | Path |
> 8065	|---------|------|
> 8066	| Architecture rules | `CLAUDE.md` |
> 8067	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8068	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8069	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8070	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8071	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8072	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8073	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8074	| **Node types** | `src/components/orchestrator/nodes/` |
> 8075	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8076	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8077	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8078	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8079	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8080	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8081	| Billing utilities | `src/lib/billing.ts` |
> 8082	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8083	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8084	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8085	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8086	| Video rescue (local) | `rescue.ts` |
> 8087	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8088	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8089	| Deploy harness | `scripts/harness-deploy.sh` |
> 8090	
> 8091	---
> 8092	
> 8093	## First Client Onboarding Checklist
> 8094	
> 8095	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8096	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8097	3. ~~Activate watchdog cron~~ ✅ Done
> 8098	4. ~~Deploy rescue-video function~~ ✅ Done
> 8099	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8100	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8101	7. Monitor `infra_health_logs` for first 24h.
> 8102	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8103	
> 8104	---
> 8105	
> 8106	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8107	
> 8108	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8109	
> 8110	| Action | Result |
> 8111	|--------|--------|
> 8112	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8113	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8114	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8115	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8116	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8117	
> 8118	| Commit | Conteúdo |
> 8119	|--------|----------|
> 8120	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8121	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8122	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8123	
> 8124	### Arquitetura Matrix Intelligence
> 8125	
> 8126	```
> 8127	ConstellationMatrix (Stabilized Engine)
> 8128	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8129	  └── NodeDetailsPanel (Tabbed Navigation)
> 8130	        ├── Tab Meta: Neighbor exploration + Net Context
> 8131	        ├── Tab Code: Source code preview (Supabase sync)
> 8132	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8133	
> 8134	useNodeIntelligence Hook:
> 8135	  - contentQuery: fetch nodes.content column
> 8136	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8137	  - state: isAnalyzing, analysisResult, progress
> 8138	```
> 8139	
> 8140	---
> 8141	
> 8142	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8143	
> 8144	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8145	
> 8146	| Action | Result |
> 8147	|--------|--------|
> 8148	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8149	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8150	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8151	
> 8152	**Output da análise (estruturado em pt-BR):**
> 8153	- Visão Geral — papel do módulo no sistema
> 8154	- Padrões Detectados — design patterns, antipatterns
> 8155	- Acoplamento & Dependências — análise In/Out-Degree
> 8156	- Recomendações — 1-3 ações priorizadas
> 8157	
> ```

## 🤖 Claude *(12:50:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null",
  "description": "List scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 22 00:47 ..
> ```

## 🤖 Claude *(12:50:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -80 || echo \"NO sprint-priorities.md\"",
  "description": "Sprint priorities"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (63.7KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/f232593a-1ef8-4045-8b83-67389d10213f/tool-results/b03oxgw3l.txt
> 
> Preview (first 2KB):
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.44.0 — Viral Autopilot Fatia 2: cadência R2 + loop R3 auto-melhorável + UI (2026-06-20)** — `/handson` → "vamos aos próximos passos"; 4 GOs Sovereign (AskUserQuestion: migration · edge fns · R3 · selar). Closed-Loop por fatia (mapeamento do contrato vivo → SOP Lei 2 → código → /security-review → deploy → smoke zero-cost → seal). **Motor autônomo R1+R2+R3+R4 COMPLETO, zero gasto do Sovereign.** **(1) Fundação** (`686bae3`): SOP `autopilot-cron-identity.md` (OTD-VA-008, 10 gates) + migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant-escopada + RPCs `begin_autopilot_cycle` [cap+pré-débito ÚNICO sob `pg_advisory_xact_lock` anti-TOCTOU] / `finalize_autopilot_cycle` [refund crédito-positivo idempotente, espelha `finalize_vision_job`], service-role-only) + smoke RPC 11/11 (`0c59e4d`). **(2) Edge fns** (`54ac2a9`): `autopilot-run` (executor identidade 2-caminhos → begin → fan-out `orchestrate-content` prepaid → finalize → re-arma; dry_run) + `autopilot-cadence-cron` (driver pg_cron, espelha nurture-cron, 403 sem service-key) + orchestrate-content FR-VA-016 prepaid (user-path intacto); smoke 9/9. **(3) R3 loop** (`35554da`): `autopilot-analyze` (FR-VA-010, ranqueia `creative_metrics`→`optimization_policy`, tenant da linha) + `autopilot-collect` (FR-VA-008, ledger→métricas) + orchestrate-step FR-VA-011 (injeta diretiva nos 3 prompts); smoke loop 11/11. **(4) UI** (`bfd178b`): `useAutopilot`+`AutopilotPage` (`/dashboard/autopilot`) + rota + nav; types.ts regen additive. **Prova:** `/security-review` SAFE **3×** · 3 smokes zero-cost (**31 gates**) · 
> ...
> </persisted-output>
> ```

## 🤖 Claude *(12:50:08)*


## 🤖 Claude *(12:50:09)*

Let me verify BoK suite completeness across all slugs.

## 🤖 Claude *(12:50:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug\" || echo \"\u26a0\ufe0f  $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK suite completeness loop"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ agentic-workspace
> ✅ aios-sql-bridge
> ✅ authenticated-browser-operator
> ✅ canvas-design
> ✅ constellation-v2
> ✅ conteudo-v2
> ✅ e2e-user-zero
> ✅ gamificacao-nodes
> ✅ identity-fabric
> ✅ marketing-hub
> ✅ mcorch-constellation
> ✅ mcorch-qa-healing
> ✅ mercado-livre-api
> ✅ meta-api
> ✅ openclaw
> ✅ post-engine
> ⚠️  security — missing: 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> ✅ video-studio
> ✅ viral-autopilot
> ✅ viral-daily-canvas
> ✅ viralmind
> ✅ vision-mcp
> ```

## 🤖 Claude *(12:50:25)*


## 🤖 Claude *(12:50:51)*

All pre-flight gathered. Here's the brief.

═══════════════════════════════════════════════════════════
  **HANDSON — Camada Criativa + Módulo Vídeo** (seal 2026-06-22)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
Fase selada: **Camada Criativa validada/reparada + BoK `video-studio` 9/9 (emenda agência v1.1) + SSO cross-subdomínio + Fundação de Tenancy de Agência**
Últimos commits:
```
b76f1d5 docs(handoff): seal camada criativa + módulo Vídeo (BoK 9/9 + agência v1.1) + SSO + tenancy
a1d7303 docs(readme): v6.45.0 — idem
96079a5 chore: gitignore public/canvas-design (assets runtime do design-bridge)
bcd85ce feat(video-studio): fundação de tenancy de agência (org/client + RLS anti-recursão)
6eca4bc feat(sso): gate de auth cross-subdomínio MCORCH p/ apps isolados (R3)
```

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ — nada para commitar.

🏗️ **INFRA**
- `mcorch_chroma`: Up 6 days (healthy) — Chroma API v2: **OK** (`heartbeat` respondeu)
- `mcorch_claude_mem`: Up 6 days (healthy)
- `mcorch_vision_mcp`: Up 5 days (healthy) — *olho criativo / deepsearch async*
- `mega-brain-daemon` / `-webhook` / `-dashboard`: Up 6 days ✅

🧠 **KNOWLEDGE MESH**
~**8935+ nós** · 100% embedded (768d HNSW cosine). Fonte: GraphRAG State (8935 verificado 2026-06-20 no seal viral-autopilot-fatia2). O seal criativo de 2026-06-22 adicionou nós novos (BoK video-studio + handoff + `design_artifact`) — total recomputado não está documentado, então cito o último número selado.
Selos da fase nova: `e5e16090` (video-studio v1) + `c99b7875` (v1.1, DERIVES_FROM viral-autopilot) · Canvas Design `design_artifact` `58fd73ae`.

🔧 **TYPESCRIPT**
Zero erros ✅ (`tsc --noEmit` limpo)

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
- **Sealed (21/22):** agentic-workspace · aios-sql-bridge · authenticated-browser-operator · canvas-design · constellation-v2 · conteudo-v2 · e2e-user-zero · gamificacao-nodes · identity-fabric · marketing-hub · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · post-engine · **video-studio (9/9 — nova)** · viral-autopilot · viral-daily-canvas · viralmind · vision-mcp
- **Incomplete:** `security` — usa naming alternativo; só o `00-deepsearch-blueprint.md` commitado (`6b1571a`). **DEFERIDA por diretiva CISO** (não é bloqueio acidental).
- **Gate de código:** BoK `video-studio` selada → **gate ABERTO** para implementar as fatias do módulo Vídeo.

📌 **SPRINT**
Goal: *Distribuição social autônoma operacional* — pipeline publica LinkedIn auto; Twitter ao subir tier; Instagram pós App Review.
Top item vivo: ativação do Viral Autopilot (motor R1+R2+R3+R4 já completo e provado zero-cost).

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **Viral Autopilot — ativação (CRITICAL, gated em GO Sovereign):** ligar o **`pg_cron`** que chama `autopilot-cadence-cron` + rodar o **1º ciclo PAGO real**. Bloqueado por 2 itens de saída visível: **CF WAF skip `/wp-json/*`** + **acesso ao modelo de imagem OpenAI**. Falta autônomo restante: `fetch-trends`→pauta (FR-VA-018).
2. **Módulo Vídeo — implementação (gate recém-aberto):** BoK 9/9 selada (v1.1 com camada de alavancagem de agência). Próximo: primeira fatia do estúdio faceless / editor HyperFrames como app isolado (auth+mcoCoins+BYOK já fundados via SSO R3 + tabelas `organizations/clients`).
3. **Unified Sensorial Canvas — Fases 3.5–3.10:** sinapses inter-rede reais, fly-to, perf (`OTD-UCANVAS-PERF` ~30s query), poda squad-coloring, paridade + gate E2E 1920×1080, seal.

⚠️ **ALERTAS**
Nenhum alerta crítico ✅ — worktree limpo, TS zero erros, containers todos healthy.
- ℹ️ `security` BoK incompleta **por design** (deferida CISO) — não bloquear por isso.
- ℹ️ Ativação do Autopilot e 1º ciclo pago dependem de **2 blockers externos (CF WAF + OpenAI image)** + GO Sovereign — não são acionáveis sem decisão.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

Qual frente seguimos? Minha leitura: a **ativação do Viral Autopilot** é o de maior ROI mas depende de você (GO + os 2 blockers); o **módulo Vídeo** acabou de ter o BoK gate aberto e é 100% acionável agora. Me diga onde apontar.

## 👤 User *(12:59:43)*

ok vamos avante primeiro resolvendo os alertas depois os próximos passos

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-21 - e7003282-79e7-4c59-a5db-de911c1e290a]]
> * **Próxima Sessão**: [[2026-06-22 - Resolver dois pontos pendentes]]
%% --- TIMELINE END --- %%

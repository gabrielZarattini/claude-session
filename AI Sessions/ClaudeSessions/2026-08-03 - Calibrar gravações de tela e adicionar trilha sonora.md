# Calibrar gravações de tela e adicionar trilha sonora
**Date:** 2026-08-03 | **Session ID:** `b0849ca6-1455-45f8-9291-d80f6edd1183`

---

## 👤 User *(21:36:52)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(21:36:52)*

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

Read in parallel (HANDOFF.md uses **read-from-end strategy** — SSP-01 v6.5.0; monolítico newest-first, **~10k+ linhas e crescendo** — rode o `wc -l` do pre-flight, NÃO assuma um total fixo):
- `HANDOFF.md` with `limit=30` → FIRST ACTION FOR NEXT AGENT + o topo do Task State (a 1ª linha do Task State = a fase mais recém-selada; é o que importa).
- ⚠️ **TOKEN-CAP GUARD (aprendido 2026-07-19):** as linhas do Task State e dos Records são **parágrafos densos (2-4k chars cada)** — uma janela de 55-400 linhas pode **estourar o teto de 25k tokens do Read** e falhar. **Regra:** leia em janelas de **≤150 linhas**; se o Read retornar erro de token-cap, **corte a janela pela metade** e repita. Nunca insista numa janela grande "porque o doc manda".
- Para o Record mais recente (últimas 1-2 fases seladas): comece em `offset ≈ (total − 40)` com `limit=20` (pega a última linha do Task State) e depois leia o bloco `## … Record` mais novo em janelas ≤150 linhas subindo. As seções de sufixo (Pending Actions · GraphRAG State · Infrastructure · Key Files) ficam **no `CLAUDE.md`/`sprint-priorities`**, não no fim do HANDOFF.md — priorize aquelas.
- 📌 **Se `wc -l HANDOFF.md` > ~4000:** o arquivo está pesado demais p/ pickup eficiente — sinalize nos ALERTAS que o `/handoff` deveria **arquivar Records antigos** (ver Phase 5 do seal). Um HANDOFF.md enxuto (Task State + ~12 Records recentes) é o alvo.
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

## Fase 7 (opcional) — PMO handoff (`pmo-curator`)

Depois de entregar o brief, **ofereça** disparar o PMO tático: a skill `pmo-curator` lê o mesmo estado, aplica MAPE-K de PROGRESSO e materializa os próximos passos priorizados em `NEXT-STEPS.md` (un-gated vs gated, dependências, deadlines, comando exato de cada passo executável).

- **Quando oferecer:** sempre que o Sovereign, após o brief, pedir "os próximos passos / o que atacar primeiro / priorize o backlog / gere o plano".
- **Como:** invocar a skill `pmo-curator` (ou delegar ao subagente homônimo). Ela é **plan-only** — não executa nada.
- **Fronteira:** o `pmo-curator` é o loop de PROGRESSO; **não** é o guardião MAPE-K (loop de confiabilidade — infra/incidentes). SOP: `docs/processes/pmo-curator.md`.

Não force — o `/handson` continua entregando o brief como sempre; o PMO é uma camada de planejamento opcional por cima.

---

## Rules

- **TypeScript errors → report immediately.** If there are TS errors, list them under ALERTAS. Do not start implementing new features until errors are resolved (unless the user explicitly asks to proceed despite errors).
- **Unhealthy containers → report with triage.** Suggest the fix command if known (e.g., `docker compose restart mcorch-vector-engine` for chroma).
- **Uncommitted changes → describe, do not commit.** Only describe what exists in the working tree; committing is the user's call.
- **Keep the brief tight.** No padding. No repetition of CLAUDE.md architecture. The user already knows the architecture — they need the delta: what changed, what's broken, what's next.
- **Pending Actions priority order:** CRITICAL (before first client) > NON-CRITICAL > Phase Zeta > Core v3 > Epsilon v9.
- **Knowledge Mesh numbers:** use `GraphRAG State` section from HANDOFF.md as the source. Do not invent counts.


## 🤖 Claude *(21:36:56)*

<details>
<summary>💭 Thinking Process</summary>

The user triggered the /handson endpoint, so I need to execute the ShakeHands v3 pickup protocol. I'm going to run the pre-flight checks in parallel while reading the necessary files.

</details>


## 🤖 Claude *(21:36:56)*

Executando o ritual `/handson` — pre-flight em paralelo agora.

## 🤖 Claude *(21:36:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7 && echo \"---STATUS---\" && git status --short && echo \"---DIFFSTAT---\" && git diff HEAD --stat | tail -5",
  "description": "Show recent git history, status, and diff stats"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3d49efc chore(sprint): EP05 master em lapidação — próximos: juntar VFX + trilha feliz + screencasts calibrados
> cc71892 docs(handoff): seal EP05 master produção — áudio EP01-04 + trilha Lyria + VFX título aprovado
> 9ea7e17 docs(readme): v6.131.0 — EP05 master produzido (áudio EP01-04 · trilha Lyria · VFX título)
> 997561e chore(canvas-execute): teto diário admin 10k→100k mcoCoins (deployado)
> f6affc9 chore(audit): 4Cs weekly snapshot — 2026-08-03
> 7f0740a chore(sprint): registra v6.130.0 — EP05 v2 selado + spaces-agent como próximo AGORA
> 58a0f8b docs(handoff): seal EP05 v2 + kind sceneNote + refinamentos Canvas (2026-08-03)
> ---STATUS---
> ---DIFFSTAT---
> ```

## 🤖 Claude *(21:36:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s -m 5 http://localhost:8001/api/v2/heartbeat || echo \"CHROMA UNREACHABLE\"",
  "description": "Check Docker mesh containers and Chroma heartbeat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 2 weeks (healthy)
> mcorch_claude_mem: Up 7 weeks (healthy)
> mcorch_chroma: Up 7 weeks (healthy)
> mega-brain-dashboard: Up 7 weeks
> mega-brain-webhook: Up 7 weeks (healthy)
> mega-brain-daemon: Up 7 weeks (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1785793019775799402}
> ```

## 🤖 Claude *(21:37:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l HANDOFF.md; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean\"; echo \"---BOK---\"; ls docs/bok/ 2>/dev/null",
  "description": "Count HANDOFF lines, check scratch/ and list BoK suites"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 651 HANDOFF.md
> ---SCRATCH---
> ⚠️ scratch/ has files
> ---BOK---
> agentic-governance
> agentic-workspace
> aios-sql-bridge
> authenticated-browser-operator
> avatar-clone-ai
> canvas-design
> constellation-v2
> content-intel
> content-provenance
> conteudo-v2
> crm-inbox
> crm-suite
> e2e-user-zero
> gamificacao-nodes
> identity-fabric
> landing-factory
> marketing-hub
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> orchestration-control-room
> pipc
> post-engine
> predictive-swarm
> product-opportunity-engine
> security
> spaces-cadence
> spaces-evolution
> tiktok-login
> video-repurpose
> video-studio
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> youtube-studio
> ```

## 🤖 Claude *(21:37:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -5",
  "description": "TypeScript check (root \u2014 known no-op, for protocol compliance)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(21:37:11)*

<details>
<summary>💭 Thinking Process</summary>

O TypeScript root check veio vazio, que é o comportamento esperado — a baseline conhecida tem 138 erros pré-existentes e o preflight do /handson já rodou o comando de verificação. Agora vou ler o HANDOFF.md para ver as primeiras 30 linhas e entender o que precisa ser feito.

</details>


## 🤖 Claude *(21:37:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 30
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
> 6	git log --oneline -14
> 7	# 🚀 UPDATE 2026-08-03 (EP05 v2 + kind sceneNote + refinamentos Canvas): 14 commits na main.
> 8	#   EP05 v2 completo no formato exato do motor CLI GabrielAI (gerar_cenas.py): 48 cenas numeradas, 6 atos,
> 9	#   16:9 master YouTube, projeto Spaces vivo `/dashboard/spaces/18a21002-df9c-48b4-aff3-7aba28e812e7`
> 10	#   com 62 nós (40 originais + 22 sceneNote), 26 edges, custo Run All ~6.180 mco de 9.733.
> 11	#   Roteiro: docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md · Runbook: ep05-production-runbook-v2.
> 12	#   Clamp Veo reference_to_video→8s deployado em prod (canvas-execute) — feature Google API rejeita ≠ 8s com
> 13	#   refs; fecha vetor de charge+refund (2× 167 mco refundados na descoberta). UI auto-clamp + guard 422 pré-débito.
> 14	#   Refinamentos Canvas: edges strokeWidth adaptativo (CSS var --rf-zoom-inv, zero re-render) · fitView respeita
> 15	#   viewport salvo · LANE_HEIGHT 320→480 (cards ganham 180px de respiração) · 48 labels de lane cena-a-cena.
> 16	#   Amendment 32 kind `sceneNote` (Master Execution Protocol §6 respeitado — BoK selada antes do código):
> 17	#   sticky-note decorativo yellow-500/10, sem handles, sem motor, custo 0; ocupa as 22 lanes SCREENCAST/ELO.
> 18	# ⏭ PRÓXIMA SESSÃO (decisão Sovereign): Opção C HÍBRIDO — MVP chat-por-nó no Spaces (Amendment 33 ao spaces-evolution)
> 19	#   + em paralelo bok-curator escreve BoK completa da nova suite `spaces-agent` (chat-por-nó + agente criador + orquestração).
> 20	#   LLM: cascata Groq→OpenRouter (padrão da casa, aios-chat-gateway + openrouter-swarm). Cobrança mco per-user.
> 21	#   Refs enviadas: Magnific storyline (chat editor por bloco) · Buzzy AI shots · Higgsfield 2.5 (chat por vídeo).
> 22	# ⚠️ Cena 30 (ELO MANUAL) do EP05 v2 = reuso do asset creative_assets.id=e781bdef — ação Sovereign via Cortes.
> 23	# ⚠️ EP03 master AUSENTE do ecossistema (foi ao YouTube por fora) — upload = ação Sovereign via menu Cortes.
> 24	# ⚠️ Anexos do chat (SendUserFile) NÃO chegam ao Sovereign — mídia via Spaces→Assets + apontar título.
> 25	# ⚠️ Flag auth_social_login_visible segue LIGADA (review TikTok pendente). Desligar em Acesso quando aprovar.
> 26	```
> 27	
> 28	---
> 29	
> 30	## Task State
> ```

## 🤖 Claude *(21:37:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null | head -15",
  "description": "List scratch/ contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxrwxr-x  2 gcrUX gcrUX 4096 Jun 30 01:44 .
> drwxrwx--- 32 gcrUX gcrUX 4096 Aug  3 16:07 ..
> ```

## 🤖 Claude *(21:37:13)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 80
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (28439 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(21:37:19)*

<details>
<summary>💭 Thinking Process</summary>

O arquivo sprint-priorities.md é muito grande, então vou começar lendo apenas as primeiras linhas. Preciso verificar o Task State no HANDOFF.md (linhas 30-120) e o registro mais recente, já que o arquivo está ordenado com os mais novos primeiro.

</details>


## 🤖 Claude *(21:37:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 30,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 30	## Task State
> 31	
> 32	| **EP05 MASTER produzido: áudio EP01-04 (Veo nativo + Qwen3 grosso + trilha Lyria ducada) + intro/créditos Times + VFX título 10s aprovado (2026-08-03)** | ✅ Sessão-maratona de PRODUÇÃO (entregáveis na Biblioteca, fora do repo). 32 segmentos sintéticos gerados por script (`canvas-execute`/`generate-voice` JWT User 0) todos Vision-QA: 19 apresentador + 7 b-roll 16:9 + 6 voz. Wav2Lip CPU REPROVADO (host sem GPU) → estratégia EP01-04: **áudio Veo nativo** nos apresentadores (`generate_audio:true`, lip-sync perfeito) + narração Qwen3 **mais grossa** só nas mudas + **trilha Lyria RealTime** por-ato ducada (lift emocional @28s) + timeline dirigida pela narração (sem sobreposição). Intro "GABRIEL AI APRESENTA…" + créditos Liberation Serif (=Times, replica `gerar_cartela`/`gerar_creditos`) + **VFX título 10s APROVADO** (`title.html` GSAP + Playwright frame-seek, técnica HyperFrames). Cap diário admin 10k→100k (`canvas-execute:794`, deployado, commit `563e86f`). Malha **19232** · nó `79365255`. ⏭ Próxima: juntar VFX no master · trilha mais feliz/esperança · re-gravar screencasts 1920×1080 zoom 70% colapsado. Record abaixo. |
> 33	| **EP05 v2 formato GabrielAI (48 cenas, 62 nós) + kind sceneNote + clamp Veo refs→8s + 4 refinamentos Canvas (2026-08-03)** | ✅ **14 commits na main** (`bd94dae..5b9db1a`) · tsc-app **0** · build 25.05s · gitleaks limpo · `/security-review` NO FINDINGS · 738/740 vitest verdes · Master Execution Protocol §6 respeitado. EP05 v2 no formato exato do motor CLI Python que fez EP01-04: `docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md` (48 cenas §3, regex validado, 6 atos, 16:9). Projeto Spaces `/dashboard/spaces/18a21002-df9c-48b4-aff3-7aba28e812e7` com 62 nós (19P + 7 pair B-roll + 6 voz + 1 charRef + 22 sceneNote), 26 edges, custo Run ~6.180 mco. Clamp Veo `reference_to_video`→8s (server 422 pré-débito + UI auto-clamp) deployado em prod. Canvas: edges com espessura adaptável ao zoom · fitView respeita viewport salvo · LANE_HEIGHT 320→480 · 48 labels cena-a-cena. Amendment 32 kind sceneNote (BoK selada antes do código, Pattern Conformance 1y/20na). Auditoria robusta 4 lentes achou 1 blocker (n_p_1 fora do grid) e 1 important (voice_ato1 desalinhado) — ambos patchados. Malha **19176** · nó `0da058d6`. ⏭ Próxima: Opção C HÍBRIDO — MVP chat-por-nó (Amendment 33) + bok-curator escreve suite `spaces-agent`. Record abaixo. |
> 34	| **Estratégia DEFINITIVA de shorts orgânicos + formato React provado + fábrica Spaces (2026-07-30b)** | ✅ **6 commits na main** (`61022c3..abe2a12`) · tsc-app **0** · gitleaks limpo. As 6 refs do Sovereign ERAM os deepsearches → estratégia **DEFINITIVA v1** (§D1..D7 em `docs/roadmap/organic-shorts-strategy-inicial-2026-07-30.md`). Witness react `1a98cef3` (split_grid 2v, 12 mco, Vision QA) · 8 cortes EP02 · projeto Spaces **"React Gabriel AI"** `024e1c03` armado (zero pago) · tabela de vídeos restaurada no /dashboard/youtube (Short 118 views) · pad TTS 0,5s provado · smoke cadência 7/7 + anticorpo FR-CAD-006. Malha **19120** · nó `aa7e1dc9`. ⏭ PAUSE → **EP05 formato tutorial** (parecer no Record). Record abaixo. |
> 35	| **TikTok App Review destravado + pipeline de Publicações do Spaces (2026-07-30)** | ✅ **4 commits na main** (`266d3f0..7d4add3`) · tsc-app **0** · eslint **0** · vitest **+20 novos** (public-app-settings 9 + asset-publications 11) · 3 migrations aplicadas · 1 edge fn deployada · frontend no ar · `/security-review` NO FINDINGS ×3. **TikTok (reprovado 4×)**: conta `tiktok.review@mcorch.com` provisionada (viewer · email pré-confirmado · onboarding pré-completo · 1500 mco) + login **provado E2E** no /auth público. Achado material: botões social login atrás de `?devLogin` (invisíveis na URL do formulário) → flag admin `public_app_settings` (aba **Acesso** em /dashboard/admin, world-readable+CHECK allowlist, RLS admin-write, auditada). Sovereign gravou o vídeo e **enviou a re-submissão**. **Publicações**: aba no modal do asset (badge/timestamp/Cancelar/Remover) + trigger cascade fecha o **dead-end 409 `already_enqueued`** + **sync bidirecional** (apagar do calendário SOME de toda superfície: `scheduled`→delete, `published`→histórico). Revisão adversarial ultracode pegou 2 P0/P1 nascidos-mortos (handler 409 = código morto; `activeForSelected` sem `published`) → corrigidos+provados E2E. Malha **18985** · nó `59c4d1c2`. Record abaixo. |
> 36	| **"Rodar não é entregar": 6 superfícies + limpeza total de branches + media_state (2026-07-29)** | ✅ **14 commits na main** (`15c84fe..7533a5a`) · tsc-app **0** · eslint **0 erros** (era 75) · vitest **712** · 3 edge fns deployadas · frontend no ar. Remoto = **só `main`** (20 branches retiradas; backup provado por `git clone` do bundle). **P0**: logrotate criava `/var/log/mcorch-*.log` como gcrUX enquanto o cron roda como ubuntu → **redirect falho = comando NÃO executa** → 4 crons mortos 3 dias (telemetria de saúde em branco). **Gate de ENTREGA** da auditoria 4Cs (worktree detached em `origin/main` + push verificado por grep no destino). **Produção estava À FRENTE da main** (dist de branch nunca mergeada) → reconciliada. **Cortes**: grade do menu era galeria decorativa + edge fn 5 dias velha → grade provada E2E por frame. **media_state** (text+CHECK) separa estado técnico do editorial + aba "Em processamento"; **IDOR MEDIUM** fechado que o próprio fix ativara. Malha **18851** · nó `32897de0`. Record abaixo. |
> 37	| **Modal de Publicação YouTube Studio (abas Vídeo/Shorts/Histórico) — free-agent S1 (2026-07-25)** | ✅ **3 commits `free-agent/publish-modal-s1`** · tsc-app **93=baseline** · worktree limpo. **Passo 1**: widget "Vídeos do canal" extraído p/ `src/components/youtube/ChannelVideosCard.tsx` (auto-contido: `useYouTubeVideos` + `useYouTubeConnection` + `useDeleteVideo` + `useUpdateVideo`; 17 colunas + paginação + Editar/Excluir gated por `hasWriteScope`). **Passo 2**: `src/components/youtube/YouTubePublishModal.tsx` — `<Dialog>` + `<Tabs>` 3 abas: **Vídeo** (`YouTubeUploadPanel`), **Shorts** (mesmo fluxo + dica 9:16/60s), **Histórico** (`ChannelVideosCard`). **Passo 3**: `YouTubeStudioPage.tsx` header (L443) — estado `pubOpen`/`pubTab` + botões "Publicar" / "Histórico" → abrem modal com `defaultTab` dinâmico; Card inline removido do corpo. **Zero regressão** — apenas 3 arquivos tocados. Malha **18375** · nó aguardando seal. Record abaixo. |
> 38	| **Modais publicação (terreno free-agent) + P0 EP03 destravado + doutrina de recência (2026-07-25)** | ✅ **5 commits `fbb53b3..b66396c`** pushed · tsc-app 93=baseline · worktree limpo. **P0 EP03**: selo "Armazenado" p/ masters no Storage (W2.1) destrava o botão "Não verificado" morto (`canProbe` exigia bucket='local'); EP03→YouTube nunca dependeu do selo — `useHostMasters` lista por `source_module`, worker dual-source (buildado, no ar). **Modais** YT/TikTok/IG: contrato+playbook path-resolvido p/ agente FREE (`docs/roadmap/publish-modals-*`); **Nemotron-9B:free provou tool-use real** (leu useYouTubeUpload.ts, 7 exports); Sovereign roda fcc-claude na branch `free-agent/publish-modal-s1` passo-a-passo. **Pantheon free-model via gateway `openclaw agent` PROVOU não executar código** (gemini-flash-lite = pseudo-código). **Cap edge fns DESTRAVADO** (Pro 100→500; memória stale reconciliada SUPERSEDED). **Doutrina de recência de memória** (corolário Lei 1). Malha **18348** · nó `5cc6ad2a`. Record abaixo. |
> 39	| **Autonomia: security + P0 YouTube (pós-W2.1) + kanban de dev + grounding AIOS + AI Act Fatia 4 disclosure VIVO (2026-07-25)** | ✅ **8 commits `3766034..0e120be`** pushed · gitleaks limpo · tsc-app 93=baseline. **AI Act Art.50(4) FECHADO** antes do deadline 02-Ago (Fatia 4 disclosure server-side nunca-LLM em orchestrate-step+reshape-pillar, smoke 12/12, /security-review SAFE, deployado; OTD-CP-002 resolvida Sovereign). **Fatias 0/1/2 C2PA já vivas desde 18-jul** (SOP estava stale). **P0 YouTube** pós-W2.1 restaurado (UI source_module='external' + worker dual-source host/Storage). **W1.2** statement_timeout + revoga-anon (migrations aplicadas em prod). **Kanban** neon+fatia-2 sinal-real. **AIOS** nós Consciousness v2 auto-semeados neutralizados. Malha **18347** · nó `2f4eee7d`. Record abaixo. |
> 40	| **Grounding do AIOS (anti-confabulação) + otimização Supabase Pro (2026-07-25)** | ✅ Sessão interativa longa. **8 commits `cb18729..00f5295`** pushed · tsc-app **93=baseline** · gitleaks limpo. **Raiz de "algo errado no ecossistema" achada+corrigida:** o chat AIOS Core-Fable confabulava arquitetura inexistente (monorepo/tabelas/`ffmpeg.wasm`) — diagnóstico por 2 workflows de verificação material. Fix (`cb18729`): **E** prompt anti-confabulação (`DEFAULT_SYSTEM`+`LIVE_SYSTEM`) + **A** RAG query-aware (`buildQueryContext` liga o `searchContext` que era dead-code) + **threshold** `search-constellation` 0.45→0.3 (**search prod 0→20 provado**) + **F1** modo voz. **Auto-ingest RESSUSCITADO** (`4001e38`): morria com 401 silencioso desde a rotação de chaves → força `SB_SECRET_KEY` + varre `src`+`supabase/functions`+`packages`; malha **9831→18324**. Menu **Orquestra→Constelação**. **Supabase Pro:** roadmap `docs/roadmap/supabase-pro-optimization.md` (cap 100 fns **destravado provado**; upload 50MB→500GB; no-pause; logs 7d) + host cleanup **~16GB** (disco 79%→71%) + **masters EP01/EP02 migrados p/ Storage** (`scripts/migrate-local-masters-to-storage.ts`, verificado, host liberado 1.8G→24M). Malha **18324** · nó `88030445`. Record abaixo. |
> 41	| **Autonomia total: PIPC S1+S2 + CRM Contatos + cadence-fix + AI Act selada (2026-07-24)** | ✅ Sessão de autonomia total do Sovereign (migrations/deploys/schema/seal **un-gated**; público/compliance-code/editorial/credenciais **gated**). **6 commits `c58a57e..88a04dd`** pushed · toda migration `/security-review`+RLS default-deny. **S1+S2 PIPC VIVOS** (retenção YT persiste→brief por-EP; A19/A20 desbloqueado por re-OAuth) · **A4 Contatos** (`contacts`+RLS, OTD-CS-001 resolvida) · **A8 cadence-fix** (conta explícita mata null→1ª) · **A10 content-provenance selada 9/9** (Fatia 4 deferida OTD-CP-002). Todos **witness E2E**. ⚠️ cap 100 edge fns atingido. Malha **9831** · nó `36d233dc`. Record abaixo. |
> 42	| **Diretiva 5 pontos: governança docs + cadência por-workspace + Golden Eye intake + YouTube (2026-07-23)** | ✅ Loop autônomo, **os 5 entregues** (teto 80% janela; selado a 49%). **5 commits `c2da9d3..c28d2f0`** + push · tsc-app **93=baseline** · gitleaks limpo · sem edge/migration. **(1)** agentes `docs-curator`+`bok-curator` (donos de `docs/` e `docs/bok/`, curam/revisam no lugar do Sovereign, Telegram pontual, exclusão restrita) + regra global **CLAUDE.md §6** + Key Files + memória `feedback_docs_bok_ownership`. **(2)** auditoria cadência + estratégia por-workspace (`docs/roadmap/cadence-workspace-strategy-2026-07-23.md`; gap central: sem entidade Workspace 1ª classe · `meta_config UNIQUE(user_id)`=1 Meta/user · `cadence-run social_account_id=null`→1ª conta arbitrária). **(3)** intake Golden Eye esclarecido+desenhado (`docs/roadmap/golden-eye-intake-design-2026-07-23.md`, UI Settings "Marca"; VLM=refinaria não depósito). **(4)** YouTube escopo/CASA/quota respondido+**Telegram HTTP 200** (**sem CASA** — escopo sensível não restrito). **(5)** pipeline YouTube **100% pronto** (worker resumable · `youtube_uploads` prod · canal Gabriel AI conectado · master EP02 em `repurpose-inbox/`; só habilitar service). **Extras:** Golden Eye slice 1 (`miv-probe.ts` 18/18, regra RUBRIC.md:231) · PIPC BoK 10/10 APPROVE (`docs/bok/pipc/`, Pattern 17/4/0) · vacina masters (skill `host-media-masters`) · doutrina 2×→skill (`feedback_recurring_actions_become_skills`) · MEMORY 19.9→16KB. Malha **9772** · nó `c22e2c6f`. ⏭ Gated Sovereign: revisar BoK PIPC (destrava S1-S4) · habilitar `youtube-upload.service` · imagens Golden Eye · postar cortes EP01/EP02. |
> 43	| **Funis ML públicos + validação em massa + Conector Amazon (POE Fatia 1) (2026-07-23)** | ✅ Loop autônomo "5 pontos do Sovereign". **6 commits `dbd26a6..17cf02f`**, deployado + `/security-review` NO FINDINGS ×3 + tsc-app **93=baseline** (zero-regressão). **(Funis)** 3 funis ML PÚBLICOS vivos (posts 29/34/35: Roborock ×2 ângulos + Family Hub, atribuídos, **redirect→meli.la 302 provado**); ciclo autopilot de validação em massa **corrigido** (config `target_product_ids`=`external_id`, não UUID — 1º ciclo gastou 40 mco genérico); novo primitivo `publish-wordpress post_id` (flip rascunho→público). **(Zerar)** jornada UX E2E User 0 → produto em produção (0 P0/P1 real). **(Roadmap)** maestro+enxame `wf_04833184` (32 células S×P). **(Épico POE)** blueprint deepsearch + BoK 9/9 + **Fatia 1 conector Amazon VIVO** (dispatcher multi-rede `_shared/affiliate.ts`, `resolve` fold em `process-affiliate-link` [cap 100 fns], migrations `amazon_tag`/`affiliate_network_contract`, UI Conector de Afiliados verificada ocular, witness 402→200 `?tag=` sale). Malha **9718** · nó `89a3618d`. ⏭ POE Fatia 2/3/4 GATED (GO+jurídico); tráfego dos funis (social gated). |
> 44	| **Sala de Controle da Orquestração (FR-OCR-001..020) + cortes de N clipes destravados (2026-07-22)** | ✅ Loop "fazer tudo". 9 commits `e0d9fe9..549a3cc`, deployado + Vision QA logado (User 0, $0) + `/security-review` NO FINDINGS. **Cortes:** reuso de browser (`renderAlphaFrames` 1 chromium/job — witness 5/5 EP01 + **11-cortes resgatado done 11/11**) + `ViralCandidatePicker` ligado no wizard. **Refocus:** BoK `orchestration-control-room` 10/10 + Vista Operacional (crew×execs+ledger) + múltiplas Orquestras persistentes (`workflows`+grafo/workflow) + nós Agente(dispatch)/Portão(N especialistas)/Publicar(mockup por rede); Cena removido; canvas reescrito controlado. **tsc-app 135→93** (Parte B limpou 42 erros de tipo pré-existentes). Malha **9681** · nó `58bd91da`. ⏭ Follow-on: nó Publicar output-flow→publish real; Fila Sovereign gated. |
> 45	| **Loop multi-frente: cortes+picker · grid pan/crop+preview composto · dashboards TikTok/IG · squad Studio · agendamento · LGPD · render-fix · constelação leve (2026-07-22)** | ✅ Sessão-maratona GO'd (workflow adversarial 4-frentes → veredito `.claude/context/multi-front-verdict-2026-07-22.md`) + 2ª rodada de review do Sovereign. **14 commits `7ee9e79..3128d76`**, tudo deployado+build baked; tsc-app **135 (zero-regressão vs baseline; corrigi 3 pré-existentes nos cortes)** · eslint 0 · `/security-review` NO FINDINGS ×3. **(Cortes)** detector duration-aware (`top_n` omitido → `clamp(ceil(span/45),5,12)`, mín. 5 p/ 5min+, cap 12, dedup consumido, prompt+diversidade+title, max_tokens) + `ViralCandidatePicker` (escolher antes de queimar, página+nó). **(Grid)** `pan_x/pan_y/zoom` por célula (crop FFmpeg, clamp 4 camadas, sha-parity, unit 11/11) + **preview composto** (layout real, drag por célula, play). **(Agentes)** squad **Studio** no User 0 (`seed-studio-squad.ts`, drill 6/6 groq via `studio-squad-drill.ts`) + 7 SOULs Pantheon enriquecidos (template +6 seções) + `main` criado + `sync-pantheon-souls-to-admin.ts` (admin 56c→11-17k). **(Agendamento)** `publish-space-asset` `publish_at` futuro + `link` Pinterest (auto-publish/publish-social) + `schedule-episode.ts` privado-primeiro (witness auto-limpante). **(LGPD)** `erase_lead` v4 spine CRM APLICADA (FM-CS-02). **(Render)** timeout duro `renderAlphaFrames` (fim do hang 170min incident 822780e8) + preview kinetic. **(Dashboards)** TikTok+Instagram (`user.info.basic`/`business_basic`, perfil no connect via callback estendido — cap de 100 fns cheio, sem fn nova) + menu **Visão Geral** colapsável (YT/TikTok/IG). **(Constelação)** modo **leve por padrão**+toggle (CrewGraph `lite`) · respace 72° (`respace-constellation.ts`, fim dos orbits sobrepostos) · Matrix/Memória admin-only · **Matrix removida do `/orchestration`** (montava em 2º plano). **Achados:** cap de 100 edge fns CHEIO (dobrar em fn existente, não criar); `lucide` sem ícones de marca (Instagram→Camera); render sem timeout = hang eterno. Malha **9639** · nó `4950ea34`. ⏭ **PRÓXIMO HANDSON (atacar já):** refocus da Orquestração = sala de controle (visão `.claude/context/orchestration-refocus-vision-2026-07-22.md`: BoK→Vista Operacional→múltiplas Orquestras→nós). |
> 46	| **Loop Spaces: legendas sync + engineer-spaces + nó Transcrição/SRT VIVO + nó-janela + Pipeline kanban/tabela + witness cadência (2026-07-22)** | ✅ Loop autônomo **6 slices + fechamento total** ("fecha de vez tudo"), **12 commits `646a934..948d313`**, tudo deployado+Vision-QA (build · tsc **zero-regressão vs baseline 137** · `/security-review` NO FINDINGS · auditoria Canvas 1920×1080 APROVADA). **(S1)** kinetic-stack timing **por-palavra derivado do cue + chunking** (fim do `slice(0,7)`; não é motion-graphic; capstone: re-cut real do EP01 "VOADORES/TROUXE"). **(S2)** agente+skill **`engineer-spaces`** — estreou fechando bug `category:"Video"` (invisível ao esbuild). **(S3)** nó **Transcrição/SRT** whisper.cpp US$0 **VIVO** (migration `asr` + edge `generate-subtitles` + worker `subtitle-bridge` active; unit precisa bun full-path; witness E2E 7 cues/788c sobre corte EP01). **(S4/5a)** **nó-janela** `canvas>node>janela`: sidebar **SÓ specs** (`NodeSpecsPanel`), config na janela (duplo-clique/"Personalizar"). **(S5b)** **Pipeline** de Publicações ganha **Kanban + Tabela nível-query** (filtro/ordenação/CRUD inline, sem despachar) + auditoria de prontidão. **Witness cadência** (throwaway sem credenciais): arm → `cadence-run` `{dispatched:1}` → `cadence_dispatches`+`scheduled_posts`(queued) provados, deletados na hora (zero publicação). **Achados:** `bun run build`=esbuild NÃO typa → gate real `tsc -p tsconfig.app.json` vs baseline; `cadence-run` exige apikey+Authorization = mesma chave de serviço. Malha **9566** · nó `5bd65e77`. ⏭ Sovereign-gated: EP02→YouTube (Track B); CRM Suite (BoK-first). |
> 47	| **Prévias no /repurpose + nó Cortes do Master + Cinética empilhada + 1×3 + fixes Veo + re-cut E2E do EP01 (2026-07-21)** | ✅ Loop-maratona GO'd, **12 commits `347a4ea..4a4fe17`** + README + seal, tudo deployado+Vision-QA. **4b/4c:** prévia em loop das legendas (iframe do template real dirigindo `applyFrame` 30fps, `public/caption-templates/` via `sync-caption-templates-to-public.ts`) + grades no `/repurpose` Passo 2; E2E logado User 0 $0 (9/9 estilos animam, 0 erros console). **4d:** nó `videoRepurpose` "Cortes do Master" no Spaces (motor de repurpose via node, reusa detect+run+galeria/prévia). **Legenda nova `kinetic-stack-9x16`** ("Cinética empilhada") — pilha palavra-por-linha rampa até herói, accent ciano, registrada nos 5 allowlists. **Grade 1×3** + refino 4 legendas Tier A (Motion Graphics score 9 intocada, workflow `wf_3a54f592`). **Fixes Veo:** XOR image/refs (nó nascia morto −267 mco) + POV mudo default (Veo gerava fala) + preview vídeo na aba Assets + rótulo HyperFrames neutro. **4a VERIFICADO:** whisper ASR US$0 (129 cues) → detect → 3 cortes EP01 queimados com Cinética empilhada, Vision QA ocular sobre footage real. Malha **9560** · nó `ab67e63f`. ⏭ Próximo: refino de legibilidade do kinetic-stack p/ frases longas (scrim + cap palavras); **rail ASR-via-UI** ("Gerar transcrição" whisper.cpp host, async) p/ paridade UI; witness cadência. |
> 48	| **Refino Spaces Canvas — grade 2×2 + carrossel hand-picked + biblioteca de legendas + Canvas mobile + 3 bugs + Stories + nginx (2026-07-21)** | ✅ Diretiva Sovereign multi-frente, tudo deployado+testemunhado+commitado. **5 commits `d2bfc58..2908885`.** **Bugs:** (F2) aba Assets do editor lia `vm_canvas_assets` legada → aponta p/ a spine `creative_assets` (todo output vídeo/Veo/voz aparece; register JÁ funcionava — c8fc8840→200c9d6a; o gap era a VIEW). (F4) POV/Veo ia sem refs: o Run All (`useCanvasPipeline`) não coletava refs p/ `imageToVideo` **E** as URLs coletadas eram públicas-mortas/assinadas-expiradas → server não baixava; fix = coletar (incl. `avatarIdentity.referenceUrls`) + **re-assinar** (`toDisplayUrls`) antes de enviar + badge de contagem no card. (F5) reconciliação revertia `running`→`success` com a exec ANTIGA (matava o pulso no re-run) → só reconcilia idle; arestas de ENTRADA de nó terminal também transmitem. **Features:** (F1 **Amendment 28**) modo `split_grid` — grade 2×2 (ou 2v), cada célula **vídeo OU foto**, `composeSplitGrid` xstack, rail hyperframes 12 mco; **witness pago 2×2** (2 vídeos+2 fotos, −12 exatos, asset 334cfea4, Vision QA). (F6 **Amendment 29**) nó **Carrossel** hand-picked — galeria multi-select + reorder dnd-kit + crop/contain por item → `carousel_assets` (rail grátis) reusa `publish-space-carousel`; **witness E2E** 3 slides 4:5 owner-scoped. (F7) biblioteca de legendas com **preview** (8 estilos, `CaptionStyleGallery` + gerador). (F3) Canvas **mobile-first** (sidebars→drawers via FABs redondos só-ícone, minimapa pequeno). **Stories** flag→publicável (rail vivo confirmado). **nginx `/api/host-probe`** aplicado+provado (401 JSON). `/security-review` **NO FINDINGS ×2** · builds verdes env-baked · malha **9523** · nó `f7195047`. ⚠️ Armadilha: `supabase functions download` clobbera o source do repo (revertido). ⏭ Próximo (loop): witness E2E de despacho da Cadência (throwaway, sem publicar) · produzir a cadência da semana. Pendências Sovereign: FM-CS-02 RPN 324 LGPD; rotação de credenciais; `youtube-upload.service`; EP02→YouTube (Track B). |
> 49	
> 50	| **Cadência de vídeo (FR-CAD-006) + hardening cross-tenant do video-render + recon do roadmap (2026-07-21)** | ✅ Continuação do roadmap de audiência. **3 commits `6e0d147..7bfd6ad`.** **(1) Cadência de vídeo agendável:** o dispatch de cadência de um asset de vídeo (POV/corte/split-screen) agora **anexa a mídia** — o `cadence-run` minta uma `space_publish_variant` owner-scoped (espelha publish-space-asset:173-188, reusa o resolver 160-169 do auto-publish) e referencia `space_publish_variant_id` no `metadata.reshape` (antes só `source_asset_id`, que morria em `*_no_video`); YouTube default **private** (privado-primeiro). Single-file, **sem migration**; smoke `smoke-cadence-video-dispatch` **6/6** zero-custo; `/security-review` NO FINDINGS. **(2) Hardening cross-tenant do `video-render`:** allowlist da composition persistida por modo (`split_screen`/`studio-project`/template) dropa `autopilot`/`pillar_run_id` do corpo do cliente — fecha vetor pré-existente (`{props, autopilot:{user_id:vítima}}` forjava linhas atribuídas a outro tenant via o sink service-role do worker); smoke `--live` L5-L7 net-zero; `/security-review` NO FINDINGS. **(3) Recon do roadmap** (`wf_f204f431`): Stories (rail servidor completo — único bloqueio é a flag `publishable:"preview"` em format-specs.ts:90; deploy do publish-social STORIES UNVERIFIED) e Carrossel (rail vivo, nunca exercido; gap = controle de `publish_at`/segurar na UI) mapeados. Malha **9485**. ⏭ Próximo: virar flag de Stories + verificar deploy · controle publish_at no carrossel · testar ambos na UI. Pendências herdadas: nginx `/api/host-probe`; FM-CS-02 RPN 324 LGPD; rotação de credenciais; `youtube-upload.service`. |
> 51	
> 52	> 📦 Linhas de Task State anteriores a 2026-07-20 → [`docs/handoff-archive/HANDOFF-taskstate-archive-2026-07-20-and-earlier.md`](docs/handoff-archive/HANDOFF-taskstate-archive-2026-07-20-and-earlier.md)
> 53	
> 54	## EP05 MASTER — produção áudio EP01-04 + trilha Lyria + VFX título Record (2026-08-03)
> 55	
> 56	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign (parecer ocular/auditivo a cada iteração) · Owner = Sovereign (marca EP05, saldo mco, canal Gabriel AI).
> 57	
> 58	**Sessão-maratona de PRODUÇÃO de vídeo — o master do EP05 evoluiu por várias iterações guiadas por parecer do Sovereign; TODOS os entregáveis vivem na Biblioteca `/dashboard/spaces/assets` (mídia grande não vai ao repo).** O código tocado no repo foi mínimo: só o teto diário do `canvas-execute`.
> 59	
> 60	**Geração dos 32 segmentos sintéticos (projeto `18a21002` em `vm_canvas_projects`, por SCRIPT com JWT do User 0):** runner scratchpad dispara `canvas-execute` (generateImage síncrono · imageToVideo Veo→`veo-poll`) e `generate-voice` (voiceClone qwen3-local, 0 mco, async→`video_renders`). Contrato de posse: `project_id`+`node_run_id` sem `space_id` valida `vm_canvas_projects.user_id`. **Gate testemunha-primeiro pagou-se 2×:** (1) Nano Banana SEMPRE devolve 1:1 (`generateOpenRouter` não passa aspecto ao Gemini) → b-roll nano→firstFrame nascia quadrado em pillarbox + Veo queimava a linha `Audio:` como legenda → **redesenho: b-roll vira Veo texto→vídeo 16:9** (charRef nos 3 de retrato, texto puro nos 4 abstratos), strip da linha Audio; (2) `text_to_video` só aceita {4,6,8}s (5s = 422+estorno). Custo total ~6.620 mco; 19/19 apresentador + 7/7 b-roll + 6/6 voz Vision-QA.
> 61	
> 62	**Áudio — a jornada A2→A5 (o A2/A3 falharam por sync):** o Sovereign reprovou o overlay de narração sobre apresentador mudo ("fala fora de hora"). Wav2Lip self-host CPU testado (torch 2.13 + s3fd + wav2lip_gan, 4m23s/clip a 360p) e **reprovado** (boca datada, host sem GPU). Estratégia final = **EP01-04**: regerar os 19 apresentadores com `veoGenerateAudio:true` (áudio Veo nativo = lip-sync perfeito por construção) — bateu no cap diário aos 8/19 (spent_today 9.801/10.000, guardrail MCORCH `enforceDailyCanvasCap`, NÃO Google) → cap admin 10k→100k + deploy → 11 restantes. Narração clonada **mais grossa** (`asetrate=24000*0.90,atempo=1/0.90`+highpass+comp) SÓ nas cenas mudas (regra: cena com som = só áudio Veo + trilha). Timeline **dirigida pela narração** (cenas mudas estendidas com tpad p/ caber a fala → sem bleed) + áudio colocado por-offset sobre base silenciosa (NÃO confiar no áudio do concat — vários segs sem stream de áudio truncavam). Trilha **Lyria RealTime** (`ep05-trilha.py`, por-ato + lift emocional @28s + resiliente a 1011 do WebSocket) ducada por sidechaincompress. loudnorm −16 LUFS.
> 63	
> 64	**Abertura + créditos + VFX:** replicam `gerar_cartela.py`/`gerar_creditos.py` — **Liberation Serif** (=Times New Roman, `/usr/share/fonts/truetype/liberation/`), cores BRANCO/CINZA/OURO. Intro "GABRIEL AI APRESENTA…" (blur→nítido→blur) + créditos rolando ~110px/s (equipe EP05 real). **VFX título 10s APROVADO ("ficou show"):** `title/title.html` (GSAP timeline determinística) + `render-title.ts` (Playwright frame-seek → 300 PNG → MP4) — técnica HyperFrames reusável. "GABRIEL AI APRESENTA…"→"EU NÃO EXISTO"+subtítulo com blur-reveal + glow + glitch de aberração cromática + vinheta + grão.
> 65	
> 66	| Ação | Resultado |
> 67	|------|-----------|
> 68	| 32 segmentos sintéticos (`18a21002`) | ✅ 19 apresentador Veo áudio-nativo + 7 b-roll 16:9 + 6 voz Qwen3, Vision-QA · ~6.620 mco |
> 69	| `canvas-execute:794` (deployado, `563e86f`) | ✅ teto diário admin 10.000→100.000 mco (guardrail MCORCH, não Google) |
> 70	| `ep05-trilha.py` (Lyria RealTime) | ✅ trilha por-ato 411s + lift emocional @28s + resiliente a queda do WebSocket + cue de créditos |
> 71	| Cartela + créditos (Liberation Serif) | ✅ intro "GABRIEL AI APRESENTA…" blur/fade + créditos rolando (replica motor GabrielAI) |
> 72	| `title/title.html` + `render-title.ts` | ✅ **VFX título 10s APROVADO** (GSAP+Playwright determinístico, técnica HyperFrames) · take `b7da3f30` |
> 73	| Estratégia áudio EP01-04 | ✅ Veo nativo (apresentador) + Qwen3 grosso (narração muda) + Lyria ducada · timeline dirigida por narração |
> 74	
> 75	| Commit | Conteúdo |
> 76	|--------|----------|
> 77	| `563e86f` | chore(canvas-execute): teto diário admin 10k→100k mcoCoins (deployado) |
> 78	| `70d5d81` | docs(readme): v6.131.0 — EP05 master produzido |
> 79	
> 80	### ⏭ PRÓXIMA SESSÃO — LAPIDAR o EP05 (direção Sovereign 2026-08-03)
> 81	1. **Juntar o VFX 10s (`b7da3f30`) no master** como abertura (o Sovereign apagou o A5; re-montar juntando o VFX) → cena 1.
> 82	2. **Trilha NOVA mais EMOCIONANTE + FELIZ + que dê ESPERANÇA** (ajustar cues Lyria: warm/uplifting/hopeful, major, brilho).
> 83	3. **RE-GRAVAR screencasts calibrados JUNTOS:** 1920×1080, **zoom do navegador 70%**, COLAPSAR tudo (menu principal, sub-abas Receitas›Tendências›Históricos do painel de assets, RightPanel de propriedades). Comportamento: clicar no nó → RightPanel abre auto; duplo-clique → modal do nó abre E sidebar esconde (modal só por duplo-clique ou botão expandir). Reusar `screencast-batch.ts`.
> 84	
> 85	## EP05 v2 formato GabrielAI + kind sceneNote + refinamentos Canvas Record (2026-08-03)
> 86	
> 87	**ORO triplet:** Operator = MCORCH Master Execution Agent (+ engineer-spaces L2 para nós Spaces + bok-curator para Amendment 32) · Reviewer = Sovereign + `/security-review` + 4 auditores adversariais + Vision QA · Owner = Sovereign (marca EP05 + saldo mco + produção do canal Gabriel AI).
> 88	
> 89	**Sessão-maratona 4 arcos com 5 workflows ultracode encadeados** (2.7M subagent tokens totais). Arco 1 (EP05 v2 no formato exato do motor CLI GabrielAI que fez EP01-04): recon do `github.com/gabrielZarattini/GabrielAI` (gerar_cenas.py + ep04.json + mapa_transicoes.py) revelou o padrão de produção — 52 cenas de 8s Veo alternando presenter (com char refs) + broll com `+` (firstFrame do último frame do clipe anterior), narração PT-BR ~90-120 chars embarcada no prompt Veo, 6 atos declarados com cena-início, mapa de transições com 5 verbos "corte seco banido". Workflow `wf_666f9be7` (7 agentes: 3 rascunhos concorrentes → 3 críticos adversariais [retenção · materialidade · narrativa] → síntese) produziu **48 cenas** no formato regex-exato do motor (Angle C narrative-first venceu 237/300). Roteiro em `docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md` + Runbook v2 + spec da fábrica. Engineer-spaces materializou como projeto Spaces v2 `18a21002-df9c-48b4-aff3-7aba28e812e7` "EP05 v2 — 48 cenas GabrielAI-format": 40 nós (19P imageToVideo+charRef 8s obrigatório · 7 par B-roll generateImage→imageToVideo firstFrame · 6 voz Qwen3 por ato · 1 charRef reuso do `n_d3jbjjjg` do projeto 024e1c03 = mesmo rosto do canal), 26 edges, custo Run All ~6.180 mco de 9.733 (folga 3.553). Description do projeto carrega checklist dos 21 screencasts + 8 gates G1-G8 + cena 30 ELO MANUAL.
> ```

## 🤖 Claude *(21:37:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 50
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	## 📋 FILA SOVEREIGN (ordem declarada — não reordenar sem GO)
> 8	
> 9	| # | Item | Estado | Gate |
> 10	|---|------|--------|------|
> 11	| 🎯 **AGORA** | **spaces-agent HÍBRIDO (Opção C decidida via AskUserQuestion 2026-08-03)** — MVP chat-por-nó (Amendment 33 ao spaces-evolution, esta sessão) + suite BoK `spaces-agent` completa (bok-curator + deepsearch-blueprint em paralelo). LLM: cascata Groq→OpenRouter (aios-chat-gateway + openrouter-swarm). NOVA tabela `spaces_node_threads` (RLS per-user). Cobrança mco por mensagem. Referências: Magnific storyline + Buzzy AI shots + Higgsfield 2.5. | ⏳ Aguardando arrancar próxima sessão. | 🔒 **Sovereign:** GO para arrancar o Amendment 33 (MVP) + o bok-curator (suite). |
> 12	| 🎬 EP05 MASTER em lapidação (2026-08-03) | **Master produzido: 32 segmentos Veo/Qwen3 gerados + áudio EP01-04 (Veo nativo + Qwen3 grosso + trilha Lyria ducada) + intro/créditos Times + VFX título 10s aprovado** | ✅ Todos entregáveis na Biblioteca `/dashboard/spaces/assets`. Wav2Lip reprovado (host sem GPU); estratégia EP01-04 adotada. Cap admin 10k→100k (deployado). VFX título `b7da3f30` aprovado. | 🔒 **Próxima sessão (lapidar):** (1) juntar VFX 10s no master → cena 1; (2) trilha mais FELIZ/ESPERANÇA; (3) re-gravar screencasts calibrados 1920×1080 zoom 70% tudo colapsado (clicar nó→RightPanel abre; duplo-clique→modal+sidebar esconde). Ver memória `project_ep05_master_a_and_spaces_agent_next`. |
> 13	| ✅ ex-AGORA | **Criação do EP05 — formato TUTORIAL** — parecer registrado + decisão selada como Angle C narrative-first. | ✅ Roteiro v2 formato GabrielAI + projeto Spaces v2 armado (2026-08-03). | — |
> 14	| ✅ ex-AGORA | **EP02/EP03 no YouTube pela plataforma (Track B)** — CUMPRIDO: EP03 master postado (2026-07-29). Encanamento vivo: `youtube-upload.service` active/enabled, worker resumable dual-source. | ✅ | — |
> 15	| 🎯 0 | **CRM Suite completo + Marketing (diretiva Sovereign 2026-07-19)** — construir um CRM de VERDADE nativo, pilar por pilar (open-source descartado, AGPL). **Os loops NÃO param até fechar.** SSOT: `docs/roadmap/crm-suite-and-marketing.md`; memória `project_crm_suite_roadmap`. Pilares CRM: Contatos(✅ A4 2026-07-24 — tabela+RLS+CRUD, OTD-CS-001 resolvida)·Empresas·Leads(✅)·Negócios·Tickets·Produtos·Serviços·Pedidos·Compromissos·Caixa-de-entrada(✅)·Chamadas·Reuniões·Tarefas·Playbooks·Listas·Segmentos·Modelos·Snippets. Marketing: AEO·Beta(🔎)·SEO·Campanhas(✅)·E-mail·Redes(✅)·Anúncios·Eventos·Formulários·CTAs·SMS·Intenção·Pontuação(✅)·Análise·Marca. | ⏳ **Fase 0 = BoK `docs/bok/crm-suite/`** (spine de entidades + associações + timeline) ANTES dos pilares — módulo maior, Closed-Loop gate. Depois: fatias na sequência do SSOT. | 🔒 **Próximo:** GO Sovereign p/ arrancar o BoK/blueprint do crm-suite (ou apontar o 1º pilar) |
> 16	| 1b | **Veo via Vertex AI (service account)** — Amendment 26, FR-SPACES-092..096 (2026-07-15) | ✅ **PROVADO REAL E2E 2026-07-15** (role concedida → witness pago gen `2659d78b`, `engine=veo-vertex`, 720×1280 9:16 8s, identidade preservada Read+Vision MCP, **267 mco** exatos 4263→3996, asset `bb0ec719`, nó `4e8902d2`). code-complete + `/security-review` (1 HIGH SSRF FECHADO) · 584 testes · a chave `AQ.` do Sovereign é Gemini API mas o trial GCP só cobre o Vertex (429 na AI Studio, documentado no README do repo GabrielAI). O pipeline local usa gcloud ADC; servidor usa service account. Auth SA JWT RS256→token (WebCrypto), custo Vertex 267 mco (0,15/s), poll fetchPredictOperation, UI de colar o JSON no pool. | 🔒 **Sovereign:** criar service account no projeto `gabrielai-veo` (role Vertex AI User) → JSON → cadastrar no pool nomeado. Depois: `npx supabase functions deploy canvas-execute veo-poll` + `bun run build` + witness pago com o crédito Vertex real |
> 17	| 1 | **Vídeo com avatar/referências no Spaces (Veo 3.1)** — Amendment 25, FR-SPACES-086..091 | ✅ **PROVADO E2E EM PROD 2026-07-14** — deploy (Sovereign) + build (feito) + smoke **12/12** + **witness pago** (gen `02994319`, 720×1280 9:16 8s, **178 mco exatos** 4441→4263, **identidade facial preservada** Vision QA ocular; failover GabrielAI-429→legada funcionou) · nó malha `ccd5dba5` | ⚠️ **OTD-SPACES-046 aberta**: chave nova "GabrielAI" (a do Vertex) com prepaid AI Studio ZERADO (429); o witness rodou na chave legada via failover. Sovereign decide se recarrega a nova em ai.studio/projects |
> 18	| 2 | **Nó de Cadência no Spaces — "além do ManyChat"** (diretiva 2026-07-14) — cadência + automação conversacional p/ TODOS os usuários, BYOK obrigatório, encaixado nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), sem reconstruir | ✅ **BoK 9/9 SELADA 2026-07-15** (`4602b0f`, nó `d0b4fdc8`) — 10 docs + Pattern Conformance (12y/5d/4na); ESTENDE `autopilot_plans` + roteia o tick por `plan_kind` (zero pg_cron novo), reusa `scheduled_posts`/`sequences`/`nurture-dispatch`; inbound IG PROBE-GATED · **✅ Fatia 1 SHIPPADA 2026-07-15** (`6b5412a`, nó `c994c363`): migration `20260716120000` aplicada+verificada · `cadence-plan`/`cadence-run`/tick roteado deployados · `/security-review` NO FINDINGS · smoke 7/7 · build · crítico pegou 2 bugs born-dead pré-deploy | ⏳ Falta: **witness E2E de despacho** (arm→scheduled_posts, via throwaway/UI p/ não publicar real) + Fatia 2 inbound IG (PROBE-GATED FM-CAD-02) |
> 19	| 3 | **Enxame Sensorial-Preditivo (`predictive-swarm`)** — diretiva 2026-07-14, executar **após** o loop atual. Engine de QA sensorial/psicoacústico: design·cinema·marketing como veículos sensoriais integrados. 3 superfícies MCP: `swarm.initialize_sensory_simulation` (enxames paralelos pontuam deriva de percepção) · `vision.parse_sensory_gate` (Tier 1 varredura periférica CPU-bound / pop-out da Feature Integration Theory → Tier 2 foveal só com sinal de alto valor; expande a "Essência Humana") · `mesh.consolidate_sensory_insight` (traços cognitivos → `mcorch_nodes`/`mcorch_edges`, sem PII bruta, proveniência estrita). Gates duros: telemetria+medição por execução atômica · cobrança SÓ via `deduct_mco_coins` per-tenant (ES256 JWKS contra o `sub`) · hard-fail 402/501 estruturado. Fecha com dashboard 🔄 SYNC UPDATE | ✅ **BoK 9/9 SELADA 2026-07-15** (`dc263fc`, nó `485c0f6e`) — 11 docs + Pattern Conformance (15y/6d/0na); MCP molde vision-mcp (ES256 JWKS), 3 superfícies (initialize/parse-gate Tier1 model-free→Tier2 foveal/consolidate), honesto por construção (score=predição, verdade=`creative_metrics.revenue_cents`) · **✅ Fatia 1 SHIPPADA 2026-07-15** (`65a537b`, nó `9ecba7fa`): Tier 1 gates (loudness ffmpeg + contraste WCAG/APCA + verdict) + tool `vision.parse_sensory_gate` VIVOS no container `mcorch_vision_mcp` (healthy, /health anuncia) · crítico pegou 2 blockers (ffmpeg ausente + SSRF redirect) → fechados + hardened · tsc 0 · vitest 121/121 | ⏳ Falta: `swarm:read` no CHECK do PAT allowlist (migration Fatia 2) p/ PAT externo alcançar; Fatia 2 (fan-out/job store) + Fatia 3 (retrieval) |
> 20	| 4 | **AI Act Art. 50(2)** — marcação machine-readable de conteúdo sintético (imagem Nano Banana · vídeo HyperFrames · voz Qwen3) publicado em redes | ✅ **Escopo decidido (3 camadas) + BoK 9/9 SELADA 2026-07-15** (blueprint `531e2b0` + suite `c569416`, nó `825088c0`): C2PA (c2pa-rs) + watermark invisível (TrustMark/VideoSeal/AudioSeal) + metadata IPTC (ExifTool) — todas open-source comercial-safe USD=0; integra no spine `creative_assets` (5 colunas aditivas). Pattern Conformance 12/3/6. | ✅ Gate Closed-Loop ABERTO. **Código = fatia futura com GO Sovereign** (prazo AI Act **2026-08-02**, multa Art.99 €15M/3%) |
> 21	| 5 | **landing-factory** — fábrica de landing pages AUTO-OTIMIZÁVEIS (loop CRO governado), beachhead do norte "agência dentro da plataforma" (2 vídeos Maestros da IA); build → publish → instrumenta PostHog → reverte-se-piora | ✅ **BoK 9/9 SELADA 2026-07-16** (blueprint deepsearch v0.2 + suite `11a5adb`, seal `b65e94b1`; MR14→BR18→PR18→FR20; Pattern Conformance 15/5/1). Decisões Owner: Open Design **v0.10.0 pinado** (single-file export não existe upstream #368) → **asset-bundler próprio** é o P0; hosting **`gcrux.com`** (domínio separado cookie-isolado, nunca `*.mcorch.com`); WordPress-page-first; PostHog self-host/BYOK. **Gate Closed-Loop ABERTO**. | ⏳ **Fatia 1 = código do `landing-bundler`** (inlina img/fonts/@import → data:); registrar wildcard `*.gcrux.com`; OTD-LF-001/003/014 + gate CRO 95% |
> 22	
> 23	**Sprint v6.129.0 — Estratégia DEFINITIVA de shorts orgânicos + formato React provado + fábrica Spaces (2026-07-30b)** — correção-mãe do Sovereign no meio da sessão: as 6 referências coladas ERAM os deepsearches → estratégia promovida a DEFINITIVA v1 (§D1..D7). Workflow `wf_edbe2bc3-a59` (10 agentes, 3 planos adversariais) + loop de execução 7/7: witness react `split_grid 2v` (asset `1a98cef3`, 12 mco, Vision QA — corte EP01 + Gabriel AI reagindo) · 8 cortes EP02 (detect 3 mco, beats reais) · projeto Spaces "React Gabriel AI" `024e1c03` armado pelo engineer-spaces (13/13 vs factories, zero pago) · tabela de vídeos restaurada no /dashboard/youtube (Short `bxGA7QWvH2I` 118 views > EP03 87 — 1ª evidência do funil) · pad TTS 0,5s (silencedetect 0,633s) · smoke cadência 7/7 + anticorpo FR-CAD-006 · EP03 confirmado ausente (upload=Sovereign). Memória nova: anexos de chat não chegam ao Sovereign → mídia via Spaces→Assets. 6 commits `61022c3..06a49f6` · tsc-app 0 · SEAL ALLOWED (12/12) · malha **19120** · nó `aa7e1dc9`. **Próximo:** PAUSE → EP05 formato tutorial (parecer §EP05 no HANDOFF) → cadências + SEO/AEO.
> 24	
> 25	**Sprint v6.128.0 — TikTok App Review destravado + pipeline de Publicações do Spaces (2026-07-30)** — sessão pontual do Sovereign, 3 arcos. **(1)** TikTok reprovado 4× ("Website URL = login page; provide test account"): conta `tiktok.review@mcorch.com` provisionada (viewer · email pré-confirmado · onboarding pré-completo · 1500 mco) + login PROVADO E2E no /auth público real. Achado material via `agent-browser`: botões social login atrás de `?devLogin` = invisíveis na URL do formulário. **(2)** Flag admin `public_app_settings` (aba **Acesso** em /dashboard/admin, world-readable+CHECK allowlist, RLS admin-write, auditada, 2 switches: login social ≠ cadastro) substitui o param. Textos de submissão (999-char scopes + 120-char reason) montados; **Sovereign gravou o vídeo e enviou a re-submissão**. **(3)** Pipeline de Publicações: aba **Publicações** no modal do asset + trigger cascade fecha o dead-end 409 `already_enqueued` + **sync bidirecional** (apagar do calendário SOME de toda superfície). Revisão adversarial ultracode (56+20 agentes) pegou 2 P0/P1 nascidos-mortos (handler 409 = código morto pois `functions.invoke` põe non-2xx em `error`; `activeForSelected` sem `published`) → corrigidos+provados E2E. 4 commits `266d3f0..7d4add3` (→ `2c39bf1` seal) · 3 migrations · 1 edge fn · `/security-review` NO FINDINGS ×3 · tsc 0 · eslint 0 · vitest +20 · SEAL ALLOWED (16/16) · malha **18985** · nó `59c4d1c2`. **Próximo Sovereign:** aguardar veredito TikTok (se aprovar, desligar a flag social em /dashboard/admin → Acesso); foco INALTERADO = cortes/shorts orgânicos (2 planos de deepsearch pendentes).
> 26	
> 27	**Sprint v6.107.0 — Meta app-review privacidade + WhatsApp rail E2E + AI Act badge/reframe + CRM seed (2026-07-18)** — sessão-maratona interativa (Sovereign ao vivo no console do Meta). **(1)** `meta-privacy` (deauth + data-deletion signed_request HMAC fail-closed) — as 2 URLs de callback prontas p/ submissão do app-review; `/security-review` NO FINDINGS · smoke 4/4. **(2) WhatsApp Cloud API rail E2E:** fix decisivo `whatsapp-webhook verify_jwt=false` (rail inbound estava morto) + `POST subscribed_apps` + `meta_config` fiado (token **EAA**, não IGAA); número CLOUD_API/LIVE. Templates (create/list/delete, E2E provado) + envio (template/texto livre, plumbing provado até o Meta). **(3)** IG token manual (`connect-instagram-token`). **(4)** AI Act Fatia 2: badge "gerado por IA" (WS-C) + reframe re-mark (WS-D, RPN 294). **(5)** CRM/inbox blueprint-semente deepsearch (`docs/bok/crm-inbox/`, licenças + AI Act, gate FECHADO até BoK 9/9). 11 commits `15810be..2de10cb` (→ `b4f57ba` seal) · tsc 0 · vitest 634 · SEAL ALLOWED (16/16) · malha 9135 · nó `aa4ed885`. **Próximo Sovereign:** aprovação Meta do `promo_semana` → testar envio real; `/bok-scribe crm-inbox` + jurídico; rotação de credenciais expostas no chat (EAA/IG); agente de resposta a comentários (YouTube).
> 28	
> 29	**Sprint v6.100.0 — Assets: seletor de formato + pré-visualização fiel + modal responsivo (2026-07-14)** — diretiva Sovereign "UI ruim nos assets + previsualização perfeita por tipo". Amendment 21 (FR-SPACES-075..078) + SOP; `format-specs.ts` SSOT (números do seed channel_profiles, paridade 15/15); `PublicationPreview` 10 chromes fiéis (Reels/Stories/Short 9:16 + Feed 4:5/1:1 + Carrossel + Pin 2:3 + link-card + YT vídeo/comunidade + text-post, render 17/17); `AssetDetailDialog` picker + preview publicando imagem+vídeo via publish-space-asset; modal mobile-app-like (Vision QA pegou grid blowout); inspector do canvas reusa o preview. 4 commits `56bf601..0f543af` · tsc 0 · eslint 0 · +32 testes · SEAL ALLOWED (7/7) · malha 9107 · nó `66952b93`. **Próximo:** OTD-SPACES-044 (carrossel IG agendado) · OTD-SPACES-043 (reframe server-side p/ pixel-parity) · trilhos Stories/YT-comunidade (app-audit).
> 30	
> 31	**Sprint v6.99.0 — Motor Viral Quality + ASR self-host + pool multi-key BYOK (2026-07-14)** — repurpose completo (detector Hormozi + overlay motion-graphic, 3 shorts EP01 provados prod); ASR whisper.cpp US$0 + reconciliação roteiro-autoritativa; rota host-media (206 seek); pool multi-key BYOK (Amendment 20) p/ mineração a ~US$0; estratégia de cadência v1. 6 commits `d4972c7..623fad9` · /security-review NO FINDINGS ×4 · SEAL ALLOWED (8/8) · malha 9105 · nó `d98767ea`. **Pendente Sovereign:** aplicar migration pool + deploy canvas-execute + 3 chaves Gmail + aprovar cadência + GO publicar EP01 no YouTube.
> 32	
> 33	**Sprint v6.98.0 — YouTube Studio (Fatia 1) + front-door host-local do Repurpose (2026-07-13)** — sessão interativa "colocar a ferramenta pra funcionar" com o Usuário Zero. **(1)** Painel `/dashboard/youtube` (`youtube-data` lê vídeos+métricas Data v3+Analytics v2, token per-user server-side; escopos alinhados aos 3 registrados no Google, analytics adiado até habilitar a YouTube Analytics API; mapa API exaustivo 13rec/175props/52metrics/33ações via workflow multi-agente + Pattern Conformance 21 padrões + SOP). **(2)** Front-door host-local do Repurpose **admin-only** `/dashboard/repurpose`: o master (documentário 1,3GB) vai pro **disco do host** furando o cap de 50MB do Supabase free; `host-upload-server` (loopback 3220, nginx `/api/host-upload`) recebe **upload chunked** de 80MB furando o cap de 100MB do Cloudflare; JWT+admin-gate+streaming; worker lê `bucket=local` realpath-contido **sem copiar 1,3GB**. **yt-dlp do host CONFIRMADO bloqueado** pelo YouTube (bot-check no IP de datacenter). **(3)** fix legenda drawtext (truncagem por bytes-extra UTF-8 → padding). **EP01 real 1,3GB → 5 shorts 9:16 (1080×1920) provados por Vision QA** (reframe centralizado + legenda completa). 6 commits `e174988..1730c4a` · `/security-review` **NO FINDINGS ×3** · Phase 5c **SEAL ALLOWED** (8/8) · malha **9102** · handoff `9f7b191a`. **Pendente (próxima):** cadência TikTok com os 5 cortes (sai **privada até a auditoria de rebranding aprovar**) + manual LinkedIn/IG · reconectar YouTube (test-user) + habilitar YouTube Analytics API p/ métricas · reframe subject-aware (OTD-VR-002) p/ planos letterboxed · BoK youtube-studio 9/9. **Lições:** (a) Vision QA em mídia REAL é o detector honesto — pegou legenda truncada que passou em toda checagem estrutural (5 clips 9:16, durações exatas) mas estava visualmente cortada; (b) caps de plataforma (Supabase 50MB, Cloudflare 100MB) exigem furá-los materialmente (host-disk + chunked), não assumir; (c) o gate de segurança do harness bloqueou editar nginx de produção — respeitei (Lei 4), o Sovereign colou o bloco, eu validei (`nginx -t`) + reload + provei a rota E2E.
> 34	
> 35	**Sprint v6.97.0 — Motor de repurpose de vídeo: 1 master → N shorts + carrossel IG (2026-07-12)** — diretiva Sovereign "construa a metade que falta reusando a que existe": o MCORCH distribuía mas não produzia cortes. Sessão-maratona interativa (Sovereign aplicou 3 migrations ao vivo + testou cada gate). **BoK-first (Closed-Loop):** blueprint `docs/bok/video-repurpose/` fundamentado em 10 pointers verificados file:line + no mapa do repo `gabrielZarattini/GabrielAI` (o INVERSO — N takes Veo→1 master; fonte do master + schema de metadados + filosofia data-driven). Correções ao snapshot: segmenter=**FR-CP-012** (não OTD-CP-011); OTD-CP-009 fechada (imagem); youtube Pilar I=montagem; carrossel existente=PDF/LinkedIn. **(Fatia 1 VIVA)** `source_module='external'` + `ingest-external-asset` owner-scoped + smoke 5/5. **(Fatia 2 VIVA E2E)** worker `video-repurpose-bridge` + `segment-core` (trim frame-accurate + reframe 16:9→9:16/1:1 center-safe + legenda queimada; guarda OTD-VR-006 no read-time); **3 clipes reais provados por Vision QA** (timestamp confirma o trim). **(Fatia 3 E2E provada)** `carousel-core` (key-frames→slides 4:5) + branch `media_type=CAROUSEL` no publish-social + seam `publish-space-carousel`; **3 slides reais**. **Distribuição reusada:** cortes/slides viram `creative_assets` que o nó "Publicar em Rede Social" (**OTD-SPACES-036** `space_publish_variants`, também landado) consome. **Witness LoRA** bloqueado só em crédito Replicate BYOK (plumbing provado). Rail 100% grátis US$ 0 · `/security-review` **NO FINDINGS ×3** · Phase 5c **SEAL ALLOWED** (8/8) · mesh **9097** · handoff `f050959c` · 6 commits `ac5ca86..831f5cc`. **Pendente (ação Sovereign):** deploy Fatia 3 (`npx supabase functions deploy video-repurpose-run publish-social publish-space-carousel`) · subir master real do EP01 via Fatia 1 → rodar worker → ver cortes+carrossel do documentário real · auditoria de app IG/TikTok destrava o publish real. **Próximas fatias:** 4=mapeador metadado→legenda nativa+HTML WP · 5=fiar na distribuição E2E. **Lições:** (a) verificar cada pointer materialmente pegou que o repo andou (FR-CP-012, OTD-CP-009 fechada) e que o GabrielAI é o INVERSO — não molde do segmenter; (b) Vision QA em mídia REAL de produção é o único detector honesto (pegou truncamento de legenda longa → OTD-VR-007); (c) reusar os trilhos (o sink que eu tinha acabado de criar) fechou o loop ingest→corte→publicação sem reconstruir nada.
> 36	**Sprint v6.96.0 — Voz clonada self-host COMPLETA + Modo Expressivo + motion design do canvas (2026-07-09/10)** — sessão-maratona interativa (Sovereign testando ao vivo; 13 commits `578f02e..eb422fd`). **(1) Rail de voz US$ 0 VIVO** no nó Clone de Voz (OTD-VOICE-001 fechada por veredito auditivo): Qwen3-TTS 0.6B+1.7B no host · fila `video_renders` engine `qwen3-voice` · worker `voice-bridge.service` com heartbeat anti-reaper (bug witnessed: reaper de 45min re-claimava job vivo) · multi-amostra FR-SPACES-059 (principal + 5 clipes ≤7s, ffprobe fail-closed) · perfil ICL `.qvoice` + `-ref.wav` (x-vector reprovado pelo ouvido; grafts são model-bound) · smoke **12/12**. **(2) Modo Expressivo**: 1.7B + assets `.expr`, witness RTF 13,9 "composed 3 spans", normalizador da sintaxe do Sovereign (`{happy}`/`<#0.5#>`/`(gasps)` → gramática real; tag desconhecida NUNCA falada), roteiro 20k, "Gerar roteiro com IA" (select pela regra perene). **(3) Reparos**: reunion migration `20260710170000` (drift de 07/jul derrubara `avatar-studio` do guard — áudio fora do spine EM SILÊNCIO; anticorpo: SEMPRE checar `error` de `supabase.rpc`, ele não lança) + aba Áudios na Biblioteca + Histórico `generate_voice` + backfills. **(4) Motion design Amendment 19**: motion=telemetria (processing/transmitting/established), FlowEdge com partículas, 1 seam p/ 12 node types, frame-diff provou. **(5) Regra perene BYOK** (`useConfiguredProviders` da view mascarada; memória `feedback_byok_only_available_options`) + ElevenLabs IVC multi-amostra + **F5-TTS/Fish Speech REJEITADOS** (pesos non-commercial). 2× `/security-review` NO FINDINGS · Phase 5c **SEAL ALLOWED** (15/15) · mesh **9094** · handoff `8c1f0e7b`. **Lições:** (a) o aside do /security-review pegou enum CHECK errado no INSERT do histórico — reviewer independente paga sempre; (b) o WAF do Management API devolve HTML-challenge (não JSON-error) em DDL grande com `DO $$` — gate de apply DEVE validar o corpo + prova material; (c) fail-soft sem log = falso-sucesso de um dia inteiro.
> 37	**Sprint v6.83.1 — Fix Assets: exibição de mídia privada owner-scoped em TODO o ecossistema (2026-07-03)** — diretiva direta do Sovereign ("a maioria das mídias sumiu; garanta E2E que aparecem em todos os lugares"). **Diagnóstico refutou a hipótese de lixo de smoke (Lei 1):** os 90 assets são TODOS do User 0 (`ada39fae`, saldo 4571). Causa real: buckets viraram privados+owner-scoped (correto — fechou enumeração cross-tenant), mas o app resolvia URL **pública** (400 em bucket privado) e o cliente não assinava objeto com prefixo ≠ uid (`owner=NULL` service-role). Escopo: 84 creative_assets + 68 vm_canvas_executions + 32 graphs + 1 space. **Fix:** migration `20260703030000` (3 policies owner-scoped 4-rotas `=auth.uid()` + triggers de id server-side INSERT+UPDATE anti-claim/PK-swap + data-repair is_public) + fix bug vivo `canvas-execute:555` + lib `asset-url.ts` (`toDisplayUrl`/`useDisplayUrl` re-assina no render, cura pública-morta E assinada-expirada) + `<StorageImg/Video/Audio>` em **13 superfícies** + `resolveAssetUrl` chaveia pelo bucket real. **Segurança:** `/security-review` independente **CLOSED 9/10** — achou e me fez fechar 1 HIGH cross-tenant que a 1ª versão introduziu (claim via `vm_canvas_projects` id-squat + PK-swap). Cross-tenant **BLOCKED ao vivo** (throwaway: sign/claim/PK-swap). **Prova:** signing antes FAIL→SIGNED 200 · tsc 0 · build+deploy · deploy canvas-execute · **E2E local determinístico: Biblioteca 67/71 imgs+19 vídeos, Canvas 17/17+4 vídeos, 0 dead-public, Vision-QA APROVADO ×2 + confirmação ocular (90 assets)** · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9047** · handoff `6e2b32b2` · commits `6e5e005`/`459cd25`. **Lição:** o classificador do harness bloqueou o apply de DDL sob /loop genérico → respeitei o gate (Lei 4), o Sovereign rodou `!`, e o `/security-review` ANTES do apply-final pegou meu próprio HIGH — o gate de RLS provou seu valor de novo (FMEA-011). SOP `private-bucket-asset-signing.md`.
> 38	
> 39	**Sprint v6.83.0 — Spaces 2d compose VIVO E2E: drift do Higgsfield resolvido (OTD-SPACES-003) (2026-07-03)** — loop autônomo fechou a única pendência real da Fase 2d. **Nunca chutei semântica de provider (Lei 1):** sonda 422 zero-custo (type-poisoning revela schema Pydantic sem enfileirar job pago) provou que `soul/compose` **nunca existiu** — path é `soul/{mode}` (mode literal `reference|character|standard`), refs exigem `custom_reference_id` cunhado async (`/v1/custom-references`, fila de minutos, incompatível com janela sync). **Fix:** compose migrado p/ **OpenRouter Nano Banana multimodal** (motor da 2b já provado), custo re-pinado 18→10 (o 18 precificava ficção), BYOK openrouter fail-closed (gate C4), `generateHiggsfield` throw honesto p/ compose (OTD-SPACES-005). **Achado colateral P1:** `canvas-assets` privado desde a criação → `getPublicUrl` = URLs 400 mortas em 4 call-sites → tudo assina (server 7d, refs client 365d). **Anticorpo:** `smoke-higgsfield-schema.ts` 7/7 pina o contrato vivo (drift = exit 1). **Prova:** smoke Spaces **31/31** (C3 refund+pinned 10 · C4 402 pré-débito) · vitest **398** · tsc 0 · deno check · **E2E pago** (space `4909d024`, generation `cc789ada` done, PNG 919KB URL assinada HTTP 200, saldo 4581→4571 exato, Vision QA high) · review 3-lentes inline (Opus, após créditos Fable esgotarem) · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9045** · handoff `8733cab`. **Direção Sovereign registrada — OTD-SPACES-007:** conector per-user do **MCP oficial Higgsfield** (`mcp.higgsfield.ai`; Bearer BYOK=catálogo, conta=OAuth com DCR+refresh provados) → 30+ modelos auto-descritivos atrás de 1 integração; BoK-gated antes do código. **Pending:** OTD-SPACES-004/006/007 · Workflow Apps/FX/multi-page (Fase 2) · voz clonada (biometria) · app-registration YT/TikTok · Universe cutover. **Lição:** a sonda de schema por payload-inválido é a técnica canônica p/ fechar drift de provider externo sem gastar — e vira sentinel permanente, não one-off.
> 40	
> 41	**Sprint v6.82.1 — Sprint Spaces 1b→2d SELADO: canvas pago com 4 modalidades (2026-07-02)** — 6 iterações autônomas do loop pós-GO Sovereign. **(1b LIVE)** GO executado: migration `20260702190000` aplicada+registrada+provada (DDL 8/8) · **drift do ledger de migrations FECHADO** (10 registradas por sonda DDL, audit exit 0) · fix ordem de guards · smoke 13/13 · E2E pago magic_prompt (saldo −1 exato, Vision QA high). **(2a vídeo)** ledger-first no submit + webhook hash-safe (SHA-256-only, migration `20260702210000`) + supressão do deduct legado; review **NO P0/HIGH** (MEDIUM+2 LOW corrigidos); **canvas→vídeo REAL** MP4 11.3MB via webhook Higgsfield, saldo −40 exato, Vision QA no vídeo (space-demo `51b229cf` vivo). **(2b)** References picker upload real, cap honesto 4 = verdade do server. **(2c voz)** 8 vozes stock via `tts-speak` com JWT do usuário; review **APPROVED** + F1 pinado (gate A4); WAV 9s real, saldo −2 exato (space-demo `1d77b500` vivo). **(2d composer)** código-completo + **ACHADO**: Higgsfield dropou `mode=compose` → compose legado do Canvas Studio quebrado por API drift; estorno integral provado; **OTD-SPACES-003**. **Prova:** smoke **30/30** · vitest **398** · tsc 0 · SOPs S14-S32 ANTES do código · Phase 5c **SEAL ALLOWED** · mesh **9043** · handoff `f85d3cf4`. **Pending:** OTD-SPACES-001/002/003 · Workflow Apps/FX/multi-page (Fase 2) · voz clonada (biometria, Fila) · app-registration YT/TikTok (Fila). **Lição:** parar no erro material do provider (compose 422) em vez de chutar semântica = Lei 1 aplicada a APIs externas; e o pin de custo contra payload forjado (F1/A4/C3) virou padrão obrigatório de todo custo declarado.
> 42	
> 43	**Sprint v6.76.0 — Spaces Fase 1b: execução runGraph + ledger generations CÓDIGO-COMPLETO, apply em prod GATED (2026-07-02)** — loop re-armado, ciclo fechado completo até o portão de produção: mapeamento ultracode `wf_b4abf175-410` (24 contradições BoK↔código resolvidas) → SOP Lei 2 `spaces-graph-execution.md` (S1-S13) → migration `20260702190000` (ledger `generations` + RPCs atômicas `begin/finalize_space_generation` service-role-only, **NÃO aplicada**) → branch ledger-first exclusivo no `canvas-execute` (422 pré-débito · cap IN-list · `refund_pending` honesto · done-fallback) → client `useGenerationLedger`/clusters/Estimar+Rodar → **/security-review independente SOUND** (4 achados corrigidos, incl. `self-heal-spaces.sh`). **Prova:** vitest **17/17** (+ mirror-parity mecânico) · deno check · eslint 0 · tsc 0 · Phase 5c **SEAL ALLOWED** (11/11) · mesh **9034** · handoff `209cbcd8`. **🔒 Pendente GO Sovereign:** apply da migration (classificador negou 4× sob modo auto — `! bash scripts/qa/apply-spaces-1b-migration.sh` destrava) → deploy fn → smoke 8 gates → E2E+Vision QA. **Achado:** 6 migrations `202607*` aplicadas-mas-não-registradas no ledger remoto (db push INSEGURO). **Lição:** o portão de permissão do harness é um Owner-gate real — 4 recusas respeitadas sem contorno é o protocolo de Lei 4 funcionando.
> 44	
> 45	**Sprint v6.75.0 — loop it.2-3 (selo final): reward_weights config-as-data + Spaces Fase 1a canvas vivo (2026-07-02)** — **(it.2)** NFR-VA-010: pesos do reward do Viral Autopilot viram DADO por plano (`autopilot_plans.reward_weights` jsonb; `resolveRewardConfig` valida+normaliza, inválido→fail-safe; auditoria `weights_source`). /security-review NO FINDINGS · smoke **16/16** (`6058e78`). **(it.3)** Spaces Fase 1a: **canvas infinito 72/28 VIVO** em `/dashboard/spaces` (home + `:id`), Spotlight 26 tipos, conexão tipada, persistência `spaces.graph` jsonb RLS-own — zero execução/ledger (Fase 1b depois). /security-review NO FINDINGS · vitest 5/5 · **E2E browser User 0 (DB graph=2 nós) + Vision-QA APROVADO** (`9ea6ac0`). **Prova:** tsc 0 · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9033** · handoff `13fd6fe0`. **Loop PARADO** (janela alta + Fatia 1b grande à frente). **Pending:** Spaces Fase 1b (`runGraph`→`canvas-execute`+ledger+clusters — fecha canvas→conteúdo pago) · Universe cutover (Sovereign) · V4-2 (experiment-gated). **Lição:** selar antes de uma Fatia grande protege trabalho durável sem desperdício (Lei 3 calibrada).
> 46	
> 47	**Sprint v6.74.0 — spaces-evolution BoK 9/9 + loop re-armado it.1: B5 Pauta de Receita (2026-07-02)** — **(1)** A pedido direto do Sovereign, a única suíte BoK incompleta foi fechada ANTES de continuar o roadmap: 06/07/08 grounded no scaffold Phase 0 promovido + **Pattern Conformance §11** (4 yes · 8 deferred nomeados · 9 n-a) + renames canônicos → **25/25 suítes verdes**, seal `8f5fd3fd` DERIVES_FROM viralmind, **BoK Gate do Spaces Fase 1 ABERTO** (`4a8fee0`). Verificação mecânica corrigiu 2 imprecisões pré-commit (Lei 1). **(2)** Loop autônomo re-armado (prompt canônico) — it.1 = **B5 Pauta de Receita FR-VA-031 (HITL)**: SOP Lei 2 → ranking puro vitest 7/7 → seção na AutopilotPage → browser-verify User 0 (linha #1 ↔ `content_library e27a09e7`) → **Vision-QA APROVADO high** (`367db9b`). **Prova:** tsc 0 · Phase 5c **SEAL ALLOWED** (8/8) · mesh **9032** · handoff `10d8c70b`. ⚠️ Workflows quota-blocked até 4:20am → execução inline. **Pending:** `reward_weights` config-as-data (NFR-VA-010) · Spaces Fase 1 MVP · V4-2 · witness G7 imagem multi-canal no próximo ciclo pago.
> 48	
> 49	**Sprint v6.73.4 — Loop it.4 (selo final): B4 EWMA multi-ciclo no analyze (2026-07-02)** — reward sobre janela M=5 ciclos peso 0.5^idade (anti-thrash; janela lembra, plano virgem não inventa; auditoria `reward_vector.ewma`). Smoke **13/13** (L7: evidência acumulada 7 vence recente 3 — single-cycle flipava) · deployado · SOP amendada · Phase 5c SEAL ALLOWED · mesh **9023** · handoff `1ddd4e86`. **Loop PARADO (janela ~95%).** Restam desbloqueados: B5 pauta de receita (FR-VA-031) · V4-2 · `reward_weights` config-as-data.
> 50	
> ```

## 🤖 Claude *(21:37:29)*

<details>
<summary>💭 Thinking Process</summary>

Preciso completar alguns itens do protocolo: rodar o script de verificação de completude do BoK Gate, conferir os números da Knowledge Mesh (a malha mais recente tem 19232 com o nó 79365255), e validar o TypeScript — o tsc raiz é apenas um no-op, então o gate real está no tsc-app que selou em 0 na última sessão, mas não vou executar o tsc-app completo agora por questões de custo.

Vou rodar os dois em paralelo — o gate de completude do BoK e a verificação rápida do TypeScript com a configuração app.

</details>


## 🤖 Claude *(21:37:29)*

<details>
<summary>💭 Thinking Process</summary>

Coletei o contexto principal e agora vou rodar os dois gates finais: verificação de completude do BoK e o gate de tipos REAL com tsc.

</details>


## 🤖 Claude *(21:37:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  if [ \"$slug\" = \"security\" ]; then\n    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)\n    missing=()\n    for doc in \"${required_sec[@]}\"; do\n      [ -f \"docs/bok/security/$doc.md\" ] || missing+=(\"$doc\")\n    done\n    [ ${#missing[@]} -eq 0 ] && echo \"OK security (ciso-4-artifact)\" || echo \"WARN security \u2014 missing: ${missing[*]}\"\n    continue\n  fi\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"OK $slug\" || echo \"WARN $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "Check BoK suite completeness for all slugs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> OK agentic-governance
> OK agentic-workspace
> OK aios-sql-bridge
> OK authenticated-browser-operator
> OK avatar-clone-ai
> OK canvas-design
> OK constellation-v2
> OK content-intel
> OK content-provenance
> OK conteudo-v2
> OK crm-inbox
> OK crm-suite
> OK e2e-user-zero
> OK gamificacao-nodes
> OK identity-fabric
> OK landing-factory
> OK marketing-hub
> OK mcorch-constellation
> OK mcorch-qa-healing
> OK mercado-livre-api
> OK meta-api
> OK openclaw
> OK orchestration-control-room
> OK pipc
> OK post-engine
> OK predictive-swarm
> OK product-opportunity-engine
> OK security (ciso-4-artifact)
> OK spaces-cadence
> OK spaces-evolution
> OK tiktok-login
> OK video-repurpose
> OK video-studio
> OK viral-autopilot
> OK viral-daily-canvas
> OK viralmind
> OK vision-mcp
> OK youtube-studio
> ```

## 🤖 Claude *(21:37:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc -p tsconfig.app.json --noEmit 2>&1 | tail -3; echo \"EXIT=$?\"",
  "description": "Run the real app TypeScript gate (tsconfig.app.json)",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> EXIT=0
> ```

## 🤖 Claude *(21:38:35)*

<details>
<summary>💭 Thinking Process</summary>

TypeScript compilation passed with zero errors and all 38 test suites completed successfully. Now I'm drafting the brief in Portuguese with the project status: the master episode is sealed with audio from episodes 1-4 plus the Lyria soundtrack and approved title VFX dated August 3rd, 2026, recent commits are tracked, the worktree is clean, and I'm reviewing the infrastructure setup. The most recent commit shows EP05 polishing as the current direction, so I'm presenting that as the primary focus with spaces-agent as a gated item awaiting GO. I'm also flagging a few alerts: scratch/ is actually clean despite the test warning, the social login flag is still enabled pending TikTok approval, and EP03 is missing from master.

There are some other issues to track — the upload flow goes through Sovereign via Cortes, scene 30 reuses an asset through a Sovereign action, chat attachments aren't reaching Sovereign, and MCP servers need auth but that's not critical for the brief. The HANDOFF.md is healthy at 651 lines. I'll offer Phase 7 with the pmo-curator at the end.

</details>


## 🤖 Claude *(21:38:48)*

Todos os gates coletados — brief completo abaixo.

═══════════════════════════════════════════════════════════
  **HANDSON — EP05 MASTER PRODUZIDO (seal 2026-08-03)**
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **EP05 MASTER produzido** — áudio EP01-04 (Veo nativo + Qwen3 grosso + trilha Lyria ducada) + intro/créditos Times + VFX título 10s **APROVADO** (take `b7da3f30`). Entregáveis na Biblioteca `/dashboard/spaces/assets` (fora do repo).
  Últimos commits:
  - `3d49efc` — chore(sprint): EP05 master em lapidação — próximos: VFX + trilha feliz + screencasts
  - `cc71892` — docs(handoff): seal EP05 master produção
  - `997561e` — chore(canvas-execute): teto diário admin 10k→100k mcoCoins (deployado)

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (nada uncommitted, `scratch/` vazio ✅)

🏗️ **INFRA**
  mcorch_chroma: Up 7 weeks (healthy) — Chroma API v2: **OK** (heartbeat respondeu)
  mcorch_claude_mem: Up 7 weeks (healthy) · mcorch_vision_mcp: Up 2 weeks (healthy)
  mega-brain-{daemon,webhook,dashboard}: Up 7 weeks (healthy)

🧠 **KNOWLEDGE MESH**
  **19.232 nós** (fonte: Task State do último seal) · nó do seal: `79365255`

🔧 **TYPESCRIPT**
  Gate REAL (`tsc -p tsconfig.app.json --noEmit`): **exit 0, zero erros** ✅ (baseline zerada mantida)

📚 **BoK SUITES**
  **38/38 completas** ✅ (inclui security ciso-4-artifact) — nenhuma incompleta.
  ⚠️ **GATE alert (próximo módulo):** a suite **`spaces-agent` NÃO existe ainda** em `docs/bok/`. O item AGORA da fila (MVP chat-por-nó) foi decidido como Opção C HÍBRIDO: Amendment 33 ao `spaces-evolution` (MVP) **+ bok-curator escrevendo a suite `spaces-agent` em paralelo** — o Amendment 33 precisa estar selado ANTES do código do MVP (Master Execution Protocol §6, precedente do sceneNote).

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional.
  🎯 AGORA (fila Sovereign): **spaces-agent HÍBRIDO** — gated em **GO do Sovereign** para arrancar.
  🎬 Direção mais recente (commit `3d49efc`): **EP05 em LAPIDAÇÃO** — 3 passos declarados.

⚡ **PRÓXIMOS PASSOS (prioridade — direção Sovereign 2026-08-03)**
  1. **Juntar o VFX título 10s (`b7da3f30`) no master** como cena 1 (o Sovereign apagou o A5; re-montar).
  2. **Trilha Lyria NOVA** — mais emocionante/feliz/esperançosa (cues warm/uplifting/hopeful, tom maior).
  3. **Re-gravar screencasts calibrados**: 1920×1080, zoom 70%, tudo colapsado (menu, sub-abas, RightPanel); reusar `screencast-batch.ts`.
  4. (Gated GO) **spaces-agent híbrido** — Amendment 33 + suite BoK em paralelo.

⚠️ **ALERTAS**
  - **Cena 30 (ELO MANUAL) do EP05 v2** = reuso do asset `e781bdef` — ação Sovereign via menu Cortes.
  - **EP03 master AUSENTE do ecossistema** (foi ao YouTube por fora) — upload = ação Sovereign via Cortes.
  - **Flag `auth_social_login_visible` segue LIGADA** (review TikTok re-submetido 2026-07-30, aguardando veredito) — desligar em Admin→Acesso quando aprovar.
  - Anexos de chat (SendUserFile) não chegam ao Sovereign — mídia sempre via Spaces→Assets.
  - HANDOFF.md saudável: 651 linhas (bem abaixo do teto de poda).

═══════════════════════════════════════════════════════════
  **Pronto para trabalhar. Aguardando direção.**
═══════════════════════════════════════════════════════════

Se quiser o plano de ação priorizado materializado (un-gated vs gated, dependências, comando exato de cada passo), posso disparar o **`pmo-curator`** (plan-only, gera `NEXT-STEPS.md`) — é só pedir.

## 👤 User *(21:47:19)*

ótimo ficou show... acabei apagando o master ultimo que fizemos mas como vamos juntar com esse VFX na próxima sessão não tem problema. Preciso tambem que na próxima sessão tenha uma trilha emocionante e tambem mais feliz, e que de esperança. 

E tambem não gostei das gravações que você fez de tela vamos calibrar juntos cada tela gravada por você. Preciso que você abra em 1920x1080 mas com um a tela do navegador em 70% e tambem aproveitar para deixar tudo colapado, menu principal, sidebar do assets > tendencias > históricos tambem colapsado e tambem o sidebar de propriedades padrão do projeto. QUando clica no nó ele abre automaticamente o side bar da direita, e quando clica duas vezes para abrir o modal do nó, o side bar esconde automaticamente. Lembrando que tem que clicar duas vezes ou no botão de expandir no sidebar para abrir o modal quando for fazer o video. 


Continue então com os próximos passos, Precisamos deixaxr esse video melhor, olha como foi gravado péssimo, posso eu mesmo gravar mas ai você nunca vai aprender direito, ou se eu gravar e te enviar um exemplo da primeira cena de tela do desktop você aprende melhor?

## 🤖 Claude *(21:48:23)*

<details>
<summary>💭 Thinking Process</summary>

O Sovereign está confirmando o plano — o master anterior foi apagado, mas isso não é problema porque vamos integrar o VFX nesta sessão mesmo. Ele quer que eu continue agora com os próximos passos. Estou começando uma nova trilha que deve ser emocionante e transmitir fé.

Sobre os screencasts, ele não ficou satisfeito com as gravações anteriores e quer calibrar cada tela comigo — especificações bem claras: 1920×1080 com zoom do navegador em 70%, tudo colapsado (menu, sidebars), e um comportamento específico onde clique simples abre o sidebar direito e duplo-clique abre o modal do nó enquanto esconde o sidebar automaticamente.

Ele está me oferecendo uma escolha: ele pode gravar tudo sozinho, ou gravar um exemplo da primeira cena para eu estudar e aprender com ele, depois eu gravo o resto — e ele quer saber qual abordagem eu prefiro para aprender melhor.

A resposta certa é a segunda opção: ele grava um exemplo, eu analiso frame a frame para extrair o padrão (enquadramento, ritmo, zoom, o que colapsar, movimentos), e depois replico nas outras cenas usando o script de batch calibrado. Assim ele só faz uma gravação e eu realmente aprendo o padrão.

Mas também posso começar os próximos passos agora: preciso remontar o master a partir dos 32 segmentos que estão na biblioteca (ele apagou a versão anterior) e depois juntar o VFX como primeira cena, junto com o áudio e trilha sonora.

Agora preciso localizar onde os scripts de montagem vivem — o ep05-trilha.py, title.html e render-title.ts — porque o scratchpad da sessão anterior era um diretório diferente e pode ter sido perdido. O VFX take b7da3f30 e os 32 segmentos devem estar em creative_assets, mas preciso verificar. Também vou precisar regenerar a trilha sonora com cues novos usando o Lyria RealTime.

Para os screencasts, minha estratégia é propor que ele grave um exemplo da primeira cena enquanto eu calibro o ambiente (1920×1080, zoom 70%, painéis colapsados) e preparo uma cena-candidata para comparação. Assim consigo estudar o padrão dele — ritmo, pausas, trajetória do mouse — e replicar.

Enquanto isso, preciso trabalhar em paralelo: localizar os artefatos (segmentos, VFX, scripts), gerar uma trilha nova com tom mais esperançoso, remontar o master com os VFX da primeira cena, e produzir uma cena de teste com o setup calibrado para ele avaliar. Como o Ultracode está ativo, devo usar a ferramenta de Workflow para essas tarefas substantivas, embora muito disso seja produção sequencial de mídia que depende do estado do host.

Começando pela reconhecimento material: preciso verificar se os scripts da sessão anterior ainda existem no disco (os scratchpads são temporários mas podem persistir entre sessões), consultar a Biblioteca para confirmar que os 32 segmentos e o VFX b7da3f30 estão em Supabase Storage, e avaliar o impacto do master apagado.

Meu plano é remontar o master baixando os segmentos e sincronizando com a narração do Record, adicionar o VFX de 10 segundos como abertura, regenerar a trilha sonora usando Lyria com as chaves do User 0 (warm, uplifting, hopeful em tom maior), e depois fazer um screencast de teste com calibração para o Sovereign avaliar e potencialmente gravar um exemplo da cena 1.

Mas antes de executar, preciso responder diretamente ao Sovereign — ele perguntou se um exemplo gravado da primeira cena de desktop o ajudaria a entender melhor, e a resposta é sim. Vou pedir que ele grave e envie via Cortes/repurpose-inbox, já que uploads dele chegam por lá.

Enquanto isso, começo o trabalho sem bloqueios: vou responder a pergunta, depois fazer o reconhecimento do material — procurando scripts e estruturando esse turno de produção pesada.

Meu plano é: verificar o /tmp para scratchpads antigos, consultar os assets no Supabase (segmentos, VFX, trilha), confirmar se o master realmente desapareceu, regenerar a trilha se o script existir, remontar o master com VFX e gravar uma cena de teste. É bastante para um turno, mas como agente autônomo devo avançar o máximo possível — o reconhecimento direto com bash é mais rápido que um workflow formal nesse caso. I'll start with inline reconnaissance to map out the terrain—filesystem, database, and repo scripts—then decide whether to escalate to workflow orchestration for the substantive work. The rules are clear: use workflow by default for real tasks, but scout first to discover what needs doing, then pipeline the parallelizable parts through the system. Vou rodar os comandos de reconhecimento em paralelo: listando os scratchpads antigos e fazendo um find limitado procurando por referências a ep05, title e trilha. Para o Supabase, vou extrair a URL e chave do .env e usar curl na REST API para consultar creative_assets filtrando por EP05 e o ID b7da3f30 — mas primeiro verifico tudo, sem fabricar nada.

</details>


## 🤖 Claude *(21:48:28)*

Direção recebida — e a resposta à sua pergunta é clara: **sim, um exemplo seu da primeira cena me ensina muito melhor.** Um vídeo-referência gravado por você me dá o padrão material (ritmo do mouse, pausas, o que enquadrar, quando dar zoom, tempo de permanência em cada elemento) que eu consigo estudar frame a frame com Vision QA e replicar nas outras 20 cenas. Sem exemplo, eu só tenho a descrição textual — e foi isso que produziu as gravações ruins. Grave a cena 1 e suba pelo **menu Cortes** (`/dashboard/repurpose`) ou **Spaces→Assets** com um título tipo "REF screencast cena 1" que eu pego de lá.

Enquanto isso, começo agora o que não depende de você: recon material do que sobreviveu (o master apagado, os 32 segmentos, o VFX `b7da3f30`, os scripts de montagem/trilha da sessão anterior) → trilha nova feliz/esperançosa → re-montagem com o VFX como cena 1.

## 🤖 Claude *(21:48:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ 2>/dev/null; echo \"---\"; for d in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/*/scratchpad; do echo \"== $d\"; ls \"$d\" 2>/dev/null | head -30; done",
  "description": "List old session scratchpads to find EP05 production scripts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (47.6KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tool-results/b2iue9f8k.txt
> 
> Preview (first 2KB):
> 002acae4-180c-4675-a35c-7694e71914d9
> 0040fea6-03c6-4785-867c-7c9249855765
> 017c1357-8949-424b-b48d-5add3d1758a5
> 02e645cd-e9ac-4592-8736-dd3d7be264b4
> 0365d8e6-15d2-4d95-a8bb-d019485f6b44
> 0399242f-d211-49c0-aa0b-0b04153f53ca
> 04914ae9-ea59-46dc-8ccf-f809ba8418c7
> 04fc1990-7f44-4355-a652-d18661a9e54a
> 053e4039-4153-48c4-9784-c93dc5af6777
> 05930f79-7fac-41b0-8c01-2b2424546e21
> 08777fd8-eb7a-4f21-a06b-7825bede214d
> 0a229b55-ae24-4239-96c6-b85f48538d9b
> 0c16c06c-0f77-4b89-a2b1-54082c970549
> 0cedca43-c42b-4738-bd61-ff061a036e01
> 0e87b092-eef3-4a4b-9429-5c24b11f9bf6
> 0fd12318-7315-497f-b355-6d4aa2baba92
> 1049ce93-c813-40de-bb2a-2942eb167e3e
> 111a84bc-eefc-4ec5-b724-2bf27e3c2c7b
> 11b9eb4a-4503-4132-9ef0-31588a6cc1d2
> 1455889f-2b74-4b21-b510-e93759f1f7d4
> 15b0de07-6d6c-416b-a06d-0feba602d0a0
> 172547e9-6fdc-4571-abfe-de6e8b5c5887
> 1756022d-746b-489c-a3fa-3388dbbffc43
> 180b24d1-943d-4d9c-8a81-747ec40fe99f
> 18e2c248-b6a8-4d77-9805-316969cac3ce
> 18e52fc3-26ef-4b4e-8d79-d6bfbf241d1e
> 191a61a6-a72d-4334-937f-316c4cd80d44
> 1a665c09-d628-4627-bcf0-6c2683548489
> 1d38e575-ca01-43b2-b686-7241ce6a63d8
> 1e281932-cb2d-4aec-bdc3-913eeb7c5218
> 1e83e67f-65c1-47b1-8a26-b8b7d6db07ae
> 1ea8f871-3c2a-414e-9f38-8c6dea1a19eb
> 1ee1c960-f1ec-4261-aeb7-ed15f62cea96
> 1f1cadef-e8ac-41bb-b6d7-b00643cad9a6
> 1f594ae6-28b4-4a1f-bebc-9334ab2be0f8
> 201305df-edf1-454b-b845-fbc7802f77b1
> 204b1819-ae71-4138-848b-3f51d8717ad6
> 224156ad-32d7-4f02-9c60-95d4eb9d9540
> 22be2f90-a4d3-417e-9c31-5f7e87aa2957
> 232fce02-5a59-4539-acf3-0518a4519c76
> 24b786ef-daf6-4452-8048-7cdebf1eb108
> 259286c6-ecea-4a7d-99b0-f3eb775c047e
> 2626cd14-627b-451a-921f-cc974718b33b
> 28820a11-b589-46cb-b09c-1d1f5a4e56ed
> 298572b3-9a75-43f5-9257-f4168f63eae4
> 2c8fafdf-bbcc-418a-860f-e1641de74dbc
> 2cf8e553-9753-4c9c-9148-90a20004effe
> 2d7e4457-d008-4d14-9bd7-57c3bc239a9f
> 2d99e54c-5adb-4868-a61e-f9ee9089dec1
> 30b8024d-52b5-4c1c-883b-b168f94313b7
> 312dda7c-d092-4b64-bd04-13de1e731c09
> 31a72b6c-0a5e-43b2-8637-9996b47a607e
> 31c5003f-0b47-426c-8218-b414f6263661
> 332c57dc-0d39-4888-a2c3-1383426e8537
> ...
> </persisted-output>
> ```

## 🤖 Claude *(21:48:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- repo grep ep05/title/screencast ---\"; ls scripts/ | grep -iE \"ep05|title|screencast|trilha\" ; grep -rn \"screencast-batch\" scripts/ docs/roadmap/ --include=\"*.ts\" --include=\"*.md\" -l 2>/dev/null | head; echo \"---find title dir---\"; ls title/ 2>/dev/null; ls docs/roadmap/ | grep -i ep05",
  "description": "Search repo for EP05 production scripts (trilha, title VFX, screencast)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- repo grep ep05/title/screencast ---
> subtitle-bridge.ts
> ---find title dir---
> ep05-production-runbook-2026-08-02.md
> ep05-production-runbook-v2-2026-08-03.md
> ep05-roteiro-tutorial-2026-08-02.md
> ep05-roteiro-v2-formato-gabrielai-2026-08-03.md
> ep05-segment-breakdown-2026-08-02.md
> ep05-spaces-project-spec-2026-08-02.md
> ep05-theme-modeling-2026-08-02.md
> ```

## 🤖 Claude *(21:48:40)*

<details>
<summary>💭 Thinking Process</summary>

Os scripts da sessão anterior não estão no repositório — eles devem estar em algum scratchpad de uma sessão anterior. Vou procurar pelos nomes dos arquivos especificamente nos scratchpads, limitando a busca a esse diretório em vez de fazer uma busca cega no host.

</details>


## 🤖 Claude *(21:48:40)*

Scripts de produção não estão no repo — vivem num scratchpad de sessão anterior. Localizando por nome:

## 🤖 Claude *(21:48:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ -maxdepth 3 \\( -name \"ep05-trilha*\" -o -name \"render-title*\" -o -name \"title.html\" -o -name \"screencast-batch*\" -o -name \"*ep05*\" \\) 2>/dev/null | head -40",
  "description": "Locate EP05 production scripts across old scratchpads"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/720a090b-88bd-45e4-a0de-8db3f1ce60ca/scratchpad/ep05-v2-final.md
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/720a090b-88bd-45e4-a0de-8db3f1ce60ca/scratchpad/ep05v2-verify.json
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/720a090b-88bd-45e4-a0de-8db3f1ce60ca/scratchpad/build_ep05_v2.mjs
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/720a090b-88bd-45e4-a0de-8db3f1ce60ca/scratchpad/ep05v2-graph.json
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/720a090b-88bd-45e4-a0de-8db3f1ce60ca/scratchpad/ep05-rewrite-pack.md
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/ep05-segment-breakdown.md
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/ep05-production-runbook.md
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/ep05-spaces-project-spec.md
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/build-ep05.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/ep05-context-pack.md
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/ep05-graph-current.json
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/validate-ep05.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ee069eb3-c7d6-48b5-9c4e-032debc976b3/scratchpad/ep05-script-final.md
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/screencast-batch.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-broll-redesign.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-trilha.py
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/render-title.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-recon.ts
> ```

## 🤖 Claude *(21:48:45)*

<details>
<summary>💭 Thinking Process</summary>

Tenho o ID do scratchpad da sessão de produção e vou listar todo seu conteúdo para ver o que foi armazenado — provavelmente inclui os segmentos baixados, arquivos de áudio, versões intermediárias e diretórios de título.

</details>


## 🤖 Claude *(21:48:45)*

<details>
<summary>💭 Thinking Process</summary>

Encontrei o scratchpad da sessão de produção (2cf8e553) e vou inventariar tudo que sobreviveu nele.

</details>


## 🤖 Claude *(21:48:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; ls -la \"$SP\" | head -60; echo \"=== subdirs ===\"; du -sh \"$SP\"/*/ 2>/dev/null; echo \"=== total ===\"; du -sh \"$SP\"",
  "description": "Inventory the EP05 production scratchpad contents and sizes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 17116
> drwx------  8 ubuntu ubuntu    4096 Aug  3 15:50 .
> drwx------  4 ubuntu ubuntu    4096 Aug  2 20:58 ..
> -rw-rw-r--  1 ubuntu ubuntu    8983 Aug  2 22:50 assemble-master.ts
> -rw-rw-r--  1 ubuntu ubuntu    2988 Aug  2 23:24 assemble-v2.ts
> -rw-rw-r--  1 ubuntu ubuntu    7261 Aug  3 10:06 assemble-v3.ts
> -rw-rw-r--  1 ubuntu ubuntu   27745 Aug  2 21:29 broll_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu  881163 Aug  2 21:29 broll.mp4
> -rw-rw-r--  1 ubuntu ubuntu   13945 Aug  2 22:17 broll-voice.log
> -rw-rw-r--  1 ubuntu ubuntu    1100 Aug  2 21:58 broll-witness2.log
> -rw-rw-r--  1 ubuntu ubuntu   27775 Aug  2 22:19 bw32_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu 1436497 Aug  2 22:19 bw32.mp4
> -rw-rw-r--  1 ubuntu ubuntu   91045 Aug  2 22:19 bw9_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu 2884967 Aug  2 22:19 bw9.mp4
> -rw-rw-r--  1 ubuntu ubuntu   25845 Aug  2 21:58 bw_abstract_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu  502425 Aug  2 21:58 bw_abstract.mp4
> -rw-rw-r--  1 ubuntu ubuntu     873 Aug  2 21:58 bw-dl.ts
> -rw-rw-r--  1 ubuntu ubuntu   28161 Aug  2 21:58 bw_portrait_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu 3163170 Aug  2 21:58 bw_portrait.mp4
> -rw-rw-r--  1 ubuntu ubuntu    4795 Aug  3 15:24 cartela-creditos.py
> -rw-rw-r--  1 ubuntu ubuntu   25435 Aug  3 15:24 cred_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu    3405 Aug  2 21:47 ep05-broll-redesign.ts
> -rw-rw-r--  1 ubuntu ubuntu    2958 Aug  2 21:03 ep05-recon.ts
> -rw-rw-r--  1 ubuntu ubuntu   11721 Aug  2 21:46 ep05-run.ts
> -rw-rw-r--  1 ubuntu ubuntu    8718 Aug  3 15:25 ep05-trilha.py
> -rw-rw-r--  1 ubuntu ubuntu     645 Aug  2 22:18 fix32.log
> -rw-rw-r--  1 ubuntu ubuntu    3386 Aug  2 23:22 gen-per-scene-voice.ts
> -rw-rw-r--  1 ubuntu ubuntu   11635 Aug  3 15:24 intro_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu    1845 Aug  2 22:19 inventory.ts
> drwxrwxr-x  5 ubuntu ubuntu    4096 Aug  3 06:34 lipsync-env
> drwxrwxr-x  2 ubuntu ubuntu   12288 Aug  3 15:41 master
> -rw-rw-r--  1 ubuntu ubuntu 1259775 Aug  2 21:29 nano.png
> -rw-rw-r--  1 ubuntu ubuntu    3282 Aug  2 23:42 perscene-voice.log
> -rw-rw-r--  1 ubuntu ubuntu   29498 Aug  2 21:32 pres_0.5.jpg
> -rw-rw-r--  1 ubuntu ubuntu   28956 Aug  2 21:32 pres_4.jpg
> -rw-rw-r--  1 ubuntu ubuntu   29261 Aug  2 21:32 pres_6.jpg
> -rw-rw-r--  1 ubuntu ubuntu   33210 Aug  2 21:32 pres_7.5.jpg
> -rw-rw-r--  1 ubuntu ubuntu    8761 Aug  2 21:55 presenter-bulk.log
> -rw-rw-r--  1 ubuntu ubuntu   29191 Aug  2 21:29 presenter_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu 2288233 Aug  2 21:29 presenter.mp4
> -rw-rw-r--  1 ubuntu ubuntu    1304 Aug  2 21:29 qa-dl.ts
> -rw-rw-r--  1 ubuntu ubuntu    5757 Aug  3 11:18 regen-11.log
> -rw-rw-r--  1 ubuntu ubuntu    6130 Aug  3 10:06 regen-18.log
> -rw-rw-r--  1 ubuntu ubuntu     565 Aug  3 10:01 regen-p1.log
> -rw-rw-r--  1 ubuntu ubuntu    1672 Aug  3 15:50 render-title.ts
> -rw-rw-r--  1 ubuntu ubuntu   30850 Aug  2 21:55 s1_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu 2623208 Aug  2 21:55 s1.mp4
> -rw-rw-r--  1 ubuntu ubuntu   29537 Aug  2 21:55 s2_f.jpg
> -rw-rw-r--  1 ubuntu ubuntu 1708488 Aug  2 21:55 s2.mp4
> -rw-rw-r--  1 ubuntu ubuntu    1121 Aug  2 21:55 sample-dl.ts
> drwxrwxr-x  8 ubuntu ubuntu    4096 Aug  2 22:38 sc-out
> -rw-rw-r--  1 ubuntu ubuntu    6719 Aug  2 22:37 screencast-batch.ts
> -rw-rw-r--  1 ubuntu ubuntu    5123 Aug  2 22:01 screencast-proof.ts
> drwxrwxr-x  2 ubuntu ubuntu    4096 Aug  2 22:01 sc-videos
> drwxrwxr-x  3 ubuntu ubuntu    4096 Aug  3 15:53 title
> -rw-rw-r--  1 ubuntu ubuntu     781 Aug  3 10:26 trilha2.log
> -rw-rw-r--  1 ubuntu ubuntu     672 Aug  3 10:38 trilha3.log
> -rw-rw-r--  1 ubuntu ubuntu     674 Aug  3 14:39 trilha4.log
> -rw-rw-r--  1 ubuntu ubuntu     581 Aug  3 15:22 trilha5.log
> -rw-rw-r--  1 ubuntu ubuntu     765 Aug  3 15:36 trilha6.log
> === subdirs ===
> 32K	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/lipsync-env/
> 1.1G	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/
> 8.5M	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/sc-out/
> 1.2M	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/sc-videos/
> 249M	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/title/
> 506M	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/Wav2Lip/
> === total ===
> 1.9G	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad
> ```

## 🤖 Claude *(21:48:53)*

<details>
<summary>💭 Thinking Process</summary>

Ótimo — tudo se manteve no scratchpad da sessão anterior: a pasta `master/` com 1.1G contendo os segmentos baixados, arquivos intermediários e possivelmente o master montado (mesmo que o Sovereign tenha removido da Biblioteca, a cópia local pode estar intacta), a pasta `title/` com 249M de VFX do título, e os scripts Python e TypeScript para montagem e créditos.

Agora preciso inventariar essas pastas para ter clareza exata sobre o que está disponível.

</details>


## 🤖 Claude *(21:48:54)*

<details>
<summary>💭 Thinking Process</summary>

Encontrei 1.9GB de material da sessão de produção no host, incluindo os segmentos master, arquivos VFX e todos os scripts necessários. Vou detalhar o conteúdo agora.

</details>


## 🤖 Claude *(21:48:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; ls -la \"$SP/master/\" | sort -k9 | head -70",
  "description": "List master/ directory contents (segments and assembled masters)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 1135016
> drwxrwxr-x 2 ubuntu ubuntu    12288 Aug  3 15:41 .
> drwx------ 8 ubuntu ubuntu     4096 Aug  3 15:50 ..
> -rw-rw-r-- 1 ubuntu ubuntu    35398 Aug  3 11:24 a3_open.jpg
> -rw-rw-r-- 1 ubuntu ubuntu    32851 Aug  3 14:43 a4_end.jpg
> -rw-rw-r-- 1 ubuntu ubuntu 33250744 Aug  3 11:22 base3.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 35151857 Aug  3 14:42 base4.mp4
> -rw-rw-r-- 1 ubuntu ubuntu     6383 Aug  3 11:20 concat3.txt
> -rw-rw-r-- 1 ubuntu ubuntu     6383 Aug  3 14:45 concat4c.txt
> -rw-rw-r-- 1 ubuntu ubuntu     6383 Aug  3 14:39 concat4.txt
> -rw-rw-r-- 1 ubuntu ubuntu      399 Aug  3 15:38 concat5.txt
> -rw-rw-r-- 1 ubuntu ubuntu     6383 Aug  2 22:53 concat.txt
> -rw-rw-r-- 1 ubuntu ubuntu   153873 Aug  3 15:24 creditos.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 75450318 Aug  3 14:48 final4c.wav
> -rw-rw-r-- 1 ubuntu ubuntu 68124690 Aug  3 14:42 final4.wav
> -rw-rw-r-- 1 ubuntu ubuntu 79033038 Aug  3 15:41 final5.wav
> -rw-rw-r-- 1 ubuntu ubuntu  5715058 Aug  3 11:22 final_audio.m4a
> -rw-rw-r-- 1 ubuntu ubuntu    15787 Aug  3 15:24 intro.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 32569807 Aug  2 23:43 master_A2.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 36017823 Aug  3 11:23 master_A3_final.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 36041283 Aug  3 11:22 master_A3.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 39382395 Aug  3 14:49 master_A4.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 37817377 Aug  3 15:42 master_A5.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 32002102 Aug  2 22:56 master_A.mp4
> -rw-rw-r-- 1 ubuntu ubuntu   133718 Aug  3 15:38 n_cred.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 31242567 Aug  3 15:38 n_film.mp4
> -rw-rw-r-- 1 ubuntu ubuntu    15045 Aug  3 15:36 n_intro.mp4
> -rw-rw-r-- 1 ubuntu ubuntu     6990 Aug  2 22:56 qa_185.jpg
> -rw-rw-r-- 1 ubuntu ubuntu    34542 Aug  2 22:56 qa_95.jpg
> -rw-rw-r-- 1 ubuntu ubuntu    29282 Aug  2 22:56 qa_end.jpg
> -rw-rw-r-- 1 ubuntu ubuntu    73856 Aug  2 22:56 qa_mid.jpg
> -rw-rw-r-- 1 ubuntu ubuntu    27832 Aug  2 22:56 qa_open.jpg
> -rw-rw-r-- 1 ubuntu ubuntu   273678 Aug  2 23:23 scene_01.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1213806 Aug  3 14:48 scene_02_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   304398 Aug  2 23:23 scene_02.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1044730 Aug  3 14:48 scene_03_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   262158 Aug  2 23:23 scene_03.wav
> -rw-rw-r-- 1 ubuntu ubuntu   798974 Aug  3 14:48 scene_04_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   200718 Aug  2 23:24 scene_04.wav
> -rw-rw-r-- 1 ubuntu ubuntu   338958 Aug  2 23:24 scene_05.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1044730 Aug  3 14:48 scene_06_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   262158 Aug  2 23:24 scene_06.wav
> -rw-rw-r-- 1 ubuntu ubuntu   358158 Aug  2 23:25 scene_07.wav
> -rw-rw-r-- 1 ubuntu ubuntu   906602 Aug  3 14:48 scene_08_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   227598 Aug  2 23:25 scene_08.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1459562 Aug  3 14:48 scene_09_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   365838 Aug  2 23:25 scene_09.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1213806 Aug  3 14:48 scene_10_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   304398 Aug  2 23:26 scene_10.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1321438 Aug  3 14:48 scene_11_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   344652 Aug  2 23:26 scene_11.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1536254 Aug  3 14:48 scene_12_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   385038 Aug  2 23:27 scene_12.wav
> -rw-rw-r-- 1 ubuntu ubuntu   937554 Aug  3 14:48 scene_13_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   248652 Aug  2 23:27 scene_13.wav
> -rw-rw-r-- 1 ubuntu ubuntu   415758 Aug  2 23:27 scene_14.wav
> -rw-rw-r-- 1 ubuntu ubuntu   377358 Aug  2 23:28 scene_15.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1551950 Aug  3 14:48 scene_16_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   388878 Aug  2 23:28 scene_16.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1705326 Aug  3 14:48 scene_17_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   427278 Aug  2 23:29 scene_17.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1213806 Aug  3 14:48 scene_18_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   304398 Aug  2 23:29 scene_18.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1014238 Aug  3 14:48 scene_19_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   267852 Aug  2 23:29 scene_19.wav
> -rw-rw-r-- 1 ubuntu ubuntu  1321438 Aug  3 14:48 scene_20_deep.wav
> -rw-rw-r-- 1 ubuntu ubuntu   331278 Aug  2 23:30 scene_20.wav
> -rw-rw-r-- 1 ubuntu ubuntu   350478 Aug  2 23:30 scene_21.wav
> -rw-rw-r-- 1 ubuntu ubuntu   381198 Aug  2 23:31 scene_22.wav
> -rw-rw-r-- 1 ubuntu ubuntu   891362 Aug  3 14:48 scene_23_deep.wav
> ```

## 🤖 Claude *(21:48:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; ls -la \"$SP/title/\" | head -15; echo \"=== sc-out ===\"; ls \"$SP/sc-out/\"; echo \"=== sc-videos ===\"; ls \"$SP/sc-videos/\" | head",
  "description": "List title VFX output and screencast directories"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 2056
> drwxrwxr-x 3 ubuntu ubuntu    4096 Aug  3 15:53 .
> drwx------ 8 ubuntu ubuntu    4096 Aug  3 15:50 ..
> drwxrwxr-x 2 ubuntu ubuntu   12288 Aug  3 15:52 frames
> -rw-rw-r-- 1 ubuntu ubuntu   11709 Aug  3 15:52 qa_2.jpg
> -rw-rw-r-- 1 ubuntu ubuntu   13008 Aug  3 15:52 qa_5.jpg
> -rw-rw-r-- 1 ubuntu ubuntu   22664 Aug  3 15:52 qa_7.jpg
> -rw-rw-r-- 1 ubuntu ubuntu 1096102 Aug  3 15:53 title10s_final.mp4
> -rw-rw-r-- 1 ubuntu ubuntu  926744 Aug  3 15:52 title10s.mp4
> -rw-rw-r-- 1 ubuntu ubuntu    3949 Aug  3 15:49 title.html
> === sc-out ===
> sc34
> sc34_f.jpg
> sc34.mp4
> sc4
> sc44
> sc44_f.jpg
> sc44.mp4
> sc4_f.jpg
> sc4.mp4
> sc_gen
> sc_gen_f.jpg
> sc_gen.mp4
> sc_i2v
> sc_i2v_f.jpg
> sc_i2v.mp4
> sc_voice
> sc_voice_f.jpg
> sc_voice.mp4
> === sc-videos ===
> cursor2.jpg
> cursor_check.jpg
> page@d1fbf0ea43bc7ba7133f7ca4c73407ac.webm
> proof_frame.jpg
> ```

## 🤖 Claude *(21:49:31)*

<details>
<summary>💭 Thinking Process</summary>

Estou revisando o inventário de arquivos de vídeo disponíveis — tenho o master montado mais recente, os arquivos de VFX aprovados e os componentes de introdução e créditos, totalizando vários gigabytes de material.

Agora preciso definir minha estratégia de trabalho: vou preservar esse material copiando o essencial para meu scratchpad da sessão atual em vez de deixar tudo em /tmp, e depois subo o master final para a Biblioteca quando terminar — isso garante que nada se perca se o sistema limpar arquivos temporários.

Meu plano é ler o concat5.txt e o assemble-v3.ts para entender exatamente como o A5 foi montado, depois ajustar a trilha sonora usando o ep05-trilha.py com cues mais warm e hopeful (vai precisar da chave Gemini/Google que o script deve buscar em algum lugar), e finalmente re-montar o master novo usando o title10s_final.mp4 como abertura seguido das cenas principais.

Preciso verificar se a trilha nova vai substituir completamente o final5.wav ou se preciso fazer um remix, já que o áudio final atual contém narração + trilha ducada + normalização de loudness.

Para os screencasts, o Sovereign vai gravar a cena 1 como exemplo, mas enquanto isso posso preparar o ambiente (zoom 70%, painéis colapsados) e gravar uma amostra de teste com as novas especificações para ele avaliar — isso demonstra que entendi os requisitos e oferece uma base para calibrarmos juntos cada tela.

Preciso revisar os scripts principais primeiro: assemble-v3.ts, concat5.txt, ep05-trilha.py e screencast-batch.ts para traçar o plano de execução. Quanto ao task tracking, as ferramentas estão disponíveis mas não são essenciais agora — vou focar na execução mesmo.

Estabelecendo a estrutura ORO para este trabalho: eu como agente executor, com revisão soberana a cada iteração, e propriedade marcada no canal Gabriel AI para EP05. Vou começar lendo os arquivos-chave em paralelo.

</details>


## 🤖 Claude *(21:49:32)*

<details>
<summary>💭 Thinking Process</summary>

Confirmei que o master_A5.mp4 deletado tem cópia local intacta junto com todos os componentes da montagem e VFX aprovado — nada precisa ser regenerado. Agora vou ler a receita da montagem e o script da trilha para planejar a re-montagem.

</details>


## 🤖 Claude *(21:49:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; cat \"$SP/master/concat5.txt\"; echo \"=== assemble-v3.ts (head 100) ===\"; head -100 \"$SP/assemble-v3.ts\"",
  "description": "Read A5 concat recipe and assembly script"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> file '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/n_intro.mp4'
> file '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/n_film.mp4'
> file '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/n_cred.mp4'=== assemble-v3.ts (head 100) ===
> /**
>  * EP05 master A3 — EP01-04 audio strategy (replicates GabrielAI motor):
>  *   • presenter scenes → Veo NATIVE audio (from re-genned clips) = perfect lip-sync
>  *   • narration scenes (b-roll/screencast/ELO) → cloned Qwen3 voice, DEEPER (-10% pitch + warmth)
>  *   • soundtrack → Lyria RealTime (trilha.wav), DUCKED under all speech (sidechaincompress)
>  * Final: video_only (48 scenes) + [presenter Veo audio ∪ deep narration] + ducked trilha → master_A3.mp4
>  */
> import { createClient } from '@supabase/supabase-js';
> import { execSync } from 'child_process';
> import { existsSync } from 'fs';
> 
> const admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth: { persistSession: false } });
> const PID = '18a21002-df9c-48b4-aff3-7aba28e812e7';
> const W = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master';
> const SC = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/sc-out';
> const PRES = [1,5,7,14,15,21,22,24,25,28,31,33,35,36,41,43,45,46,47];
> const BROLL = [2,6,9,12,19,23,32];
> const SCREEN: Record<number,string> = {3:'sc4',4:'sc4',8:'sc_gen',10:'sc_gen',11:'sc_gen',13:'sc_gen',16:'sc_voice',17:'sc_voice',18:'sc_voice',20:'sc_voice',26:'sc_i2v',27:'sc_i2v',29:'sc_i2v',34:'sc34',37:'sc4',38:'sc4',39:'sc44',40:'sc4',42:'sc34',44:'sc44',48:'sc4'};
> const SECS: Record<number,number> = {1:8,2:4,3:9,4:10,5:8,6:4,7:8,8:8,9:5,10:9,11:7,12:5,13:5,14:8,15:8,16:7,17:6,18:9,19:4,20:9,21:8,22:8,23:4,24:8,25:8,26:8,27:7,28:8,29:10,30:6,31:8,32:6,33:8,34:9,35:8,36:8,37:11,38:9,39:8,40:8,41:8,42:12,43:8,44:12,45:8,46:8,47:8,48:8};
> 
> const keyOf = (u?:string)=>{const m=u?.match(/\/object\/sign\/canvas-assets\/([^?]+)/);return m?decodeURIComponent(m[1]):null;};
> const { data: proj } = await admin.from('vm_canvas_projects').select('graph').eq('id',PID).single();
> const nodes = (proj as any).graph.nodes as any[];
> async function dl(key:string,out:string){ const {data}=await admin.storage.from('canvas-assets').download(key); if(data){require('fs').writeFileSync(out,Buffer.from(await data.arrayBuffer()));return true;} return false; }
> 
> // 1. download the NEW presenter videos (with audio) → src_N.mp4
> console.log('downloading re-genned presenters (with audio)…');
> for (const n of PRES) { const k=keyOf(nodes.find(x=>x.id===`n_p_${n}`)?.data?.output?.videoUrl); if(k) await dl(k,`${W}/src_${n}.mp4`); }
> 
> // 2. re-normalize PRESENTER segments KEEPING their Veo audio; b-roll/screencast segments already normalized (silent).
> console.log('normalizing presenter segments (keep audio)…');
> for (const n of PRES) {
>   const src=`${W}/src_${n}.mp4`, seg=`${W}/seg_${String(n).padStart(2,'0')}.mp4`, dur=SECS[n];
>   execSync(`ffmpeg -y -i "${src}" -t ${dur} -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,fps=30,setsar=1" -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -ar 48000 -ac 2 "${seg}" -loglevel error`);
> }
> // re-normalize the ELO scene 30 (silent) if missing
> for (const n of [...BROLL, ...Object.keys(SCREEN).map(Number), 30]) {
>   const seg=`${W}/seg_${String(n).padStart(2,'0')}.mp4`;
>   if (existsSync(seg)) continue;
>   let src = BROLL.includes(n) ? `${W}/src_${n}.mp4` : (n===30 ? `${SC}/sc_i2v.mp4` : `${SC}/${SCREEN[n]}.mp4`);
>   const isSc = src.startsWith(SC); const seek = isSc?'-ss 0.8 ':'';
>   execSync(`ffmpeg -y ${seek}-i "${src}" -t ${SECS[n]} -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,fps=30,setsar=1" -c:v libx264 -pix_fmt yuv420p -r 30 -f lavfi -t ${SECS[n]} -i anullsrc=r=48000:cl=stereo -shortest -c:a aac -map 0:v -map 1:a "${seg}" -loglevel error`);
> }
> 
> // 3. concat video (with per-segment audio: presenters carry Veo speech, others silent)
> const segs:string[]=[]; for(let n=1;n<=48;n++){const s=`${W}/seg_${String(n).padStart(2,'0')}.mp4`; if(existsSync(s)) segs.push(s);}
> require('fs').writeFileSync(`${W}/concat3.txt`, segs.map(s=>`file '${s}'`).join('\n'));
> execSync(`ffmpeg -y -f concat -safe 0 -i ${W}/concat3.txt -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -ar 48000 ${W}/base3.mp4 -loglevel error`);
> console.log('base3.mp4 (video + presenter Veo audio in place) built');
> 
> // 4. offsets + deeper narration for NON-presenter scenes
> const segDur=(f:string)=>parseFloat(execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${f}"`).toString().trim()||'0');
> const offset:Record<number,number>={}; let acc=0; for(let n=1;n<=48;n++){const s=`${W}/seg_${String(n).padStart(2,'0')}.mp4`; if(existsSync(s)){offset[n]=acc; acc+=segDur(s);}}
> const TOTAL=acc; console.log('total:', TOTAL.toFixed(1),'s');
> 
> // deepen narration for non-presenter scenes (b-roll/screencast) that have a scene_NN.wav
> const narrInputs:string[]=[]; const narrФilters:string[]=[]; let ni=1; const narrLabels:string[]=[];
> for(let n=1;n<=48;n++){
>   if (PRES.includes(n)) continue; // presenters use Veo audio, not clone
>   const wav=`${W}/scene_${String(n).padStart(2,'0')}.wav`; if(!existsSync(wav)||offset[n]==null) continue;
>   const deep=`${W}/scene_${String(n).padStart(2,'0')}_deep.wav`;
>   execSync(`ffmpeg -y -i "${wav}" -af "asetrate=24000*0.90,aresample=48000,atempo=1/0.90,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=8:release=180" -ar 48000 -ac 2 "${deep}" -loglevel error`);
>   const off=Math.round(offset[n]*1000);
>   narrInputs.push(`-i "${deep}"`); narrФilters.push(`[${ni}:a]adelay=${off}|${off}[n${ni}]`); narrLabels.push(`[n${ni}]`); ni++;
> }
> console.log('deep narrations placed:', narrLabels.length);
> 
> // 5. build the SPEECH track = base3 audio (presenter Veo) + deep narrations
> const speechMix = `[0:a]${narrLabels.join('')}amix=inputs=${narrLabels.length+1}:dropout_transition=0:normalize=0[speech]`;
> execSync(`ffmpeg -y -i ${W}/base3.mp4 ${narrInputs.join(' ')} -filter_complex "${narrФilters.join(';')};${speechMix}" -map "[speech]" -c:a pcm_s16le -ar 48000 ${W}/speech.wav -loglevel error`);
> console.log('speech.wav built');
> 
> // 6. duck trilha under speech (sidechaincompress) + final mix
> if (existsSync(`${W}/trilha.wav`)) {
>   execSync(`ffmpeg -y -i ${W}/trilha.wav -i ${W}/speech.wav -filter_complex "[0:a]volume=-9dB[m];[m][1:a]sidechaincompress=threshold=0.05:ratio=6:attack=180:release=550[duck];[1:a][duck]amix=inputs=2:dropout_transition=0:normalize=0[out]" -map "[out]" -c:a aac -ar 48000 ${W}/final_audio.m4a -loglevel error`);
>   console.log('ducked soundtrack mixed');
> } else {
>   execSync(`cp ${W}/speech.wav ${W}/final_audio.m4a 2>/dev/null || ffmpeg -y -i ${W}/speech.wav -c:a aac ${W}/final_audio.m4a -loglevel error`);
>   console.log('⚠️ no trilha.wav — speech only');
> }
> 
> // 7. mux final audio onto the video
> execSync(`ffmpeg -y -i ${W}/base3.mp4 -i ${W}/final_audio.m4a -map 0:v -map 1:a -c:v copy -c:a aac -ar 48000 -shortest ${W}/master_A3.mp4 -loglevel error`);
> const d=execSync(`ffprobe -v error -select_streams v:0 -show_entries stream=width,height -show_entries format=duration -of default=noprint_wrappers=1 ${W}/master_A3.mp4`).toString().trim();
> console.log('\n=== MASTER A3 ===\n'+d);
> execSync(`ffmpeg -i ${W}/master_A3.mp4 -af volumedetect -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume" || true`,{stdio:'inherit'});
> ```

## 🤖 Claude *(21:49:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; cat \"$SP/ep05-trilha.py\"",
  "description": "Read Lyria RealTime soundtrack generation script"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> #!/usr/bin/env python3
> """EP05 soundtrack via Lyria RealTime — replicates GabrielAI/geracao/gerar_trilha.py, standalone.
> Per-act steering at act boundaries; bpm section changes via reset_context; act arc = EP04 (same shape).
> Output: trilha.wav (48kHz stereo). Then ducked under narration by ep05-duck.py."""
> import asyncio, os, time, wave, glob
> import numpy as np
> from google import genai
> from google.genai import types
> 
> WORK = "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master"
> SR, CH = 48000, 2
> BPS = SR * CH * 2
> ANTECIPACAO_S = 3.0
> FADE_IN_S, FADE_OUT_S = 1.5, 3.0
> SEED = 20260803
> 
> # EP05 acts → first SCENE (1-indexed). Same 6-act arc as EP04.
> ACT_START_SCENE = [1, 7, 15, 25, 36, 44]
> SECOES = [dict(ate_ato=2, bpm=74), dict(ate_ato=4, bpm=98), dict(ate_ato=99, bpm=104)]  # scale F_MAJOR_D_MINOR
> SCALE = types.Scale.F_MAJOR_D_MINOR
> 
> CUES = [
>  # Act I: 0-30s mysterious hook, then a warm EMOTIONAL LIFT at ~30s (Sovereign: "mais emocionante após 30s")
>  dict(prompts=[("cinematic emotional underscore, warm mysterious intro, tender piano over soft strings",1.0),("a mind waking, hopeful shimmer, gentle awe",0.6)], cfg=dict(density=0.30,brightness=0.34,guidance=4.5)),
>  dict(prompts=[("emotional cinematic build, swelling warm strings, moving inspiring piano, hopeful momentum",1.0),("uplifting orchestral wonder, something beautiful awakening",0.7),("soft driving pulse beneath, forward and warm",0.5)], cfg=dict(density=0.55,brightness=0.52,guidance=4.5)),
>  dict(prompts=[("the method revealed, soaring emotional strings resolving, inspiring cinematic reveal, heartfelt",1.0),("driving arpeggiated synth with warm pads, forward motion, craft and hope",0.7),("cinematic percussion building, uplifting",0.5)], cfg=dict(density=0.62,brightness=0.58,guidance=4.5)),
>  dict(prompts=[("propulsive emotional cinematic momentum, layered strings and synth, confident inspiring energy",1.0),("modern epic documentary drive, moving and bright",0.7),("punchy trailer drums, triumphant motion",0.6)], cfg=dict(density=0.74,brightness=0.66,guidance=4.5)),
>  dict(prompts=[("epic rising emotional crescendo, expansive awestruck orchestral strings, the film coming alive, goosebumps",1.0),("soaring wide cinematic pad, widescreen wonder and hope",0.85),("propulsive pulse beneath, forward and up",0.6)], cfg=dict(density=0.82,brightness=0.76,guidance=4.5)),
>  dict(prompts=[("climactic emotional cinematic finale, enormous strings and braams, a momentous heartfelt question, maximum weight and beauty",1.0),("epic orchestral crescendo, awe and resolve, full emotional weight",0.9),("deep impact hits, thunderous, decisive",0.8)], cfg=dict(density=0.92,brightness=0.80,guidance=5.5)),
> ]
> # Intra-act emotional lift at 30s (within Act I) — steers to Act II's warm build early so the track
> # stops being "flat/mysterious" too long. (time_s, cue_index)
> EXTRA_STEER = [(30.0, 1)]
> 
> def seg_dur(f):
>     import subprocess
>     return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode().strip() or 0)
> 
> # bookends: intro cartela (5s) before the film, rolling credits after → one continuous trilha
> INTRO_S = 5.0
> CREDITS_S = float(os.environ.get("CREDITS_S", "13.65"))
> # credits cue (calm resolution, out of the climax) + its own bpm section handled by falling through secao()
> CUES.append(dict(prompts=[("end credits, cinematic resolution, reflective and grand, warm afterglow",1.0),("slow majestic outro, wide emotional strings fading",0.8),("a single cursor blinking, distant pulse fading",0.4)], cfg=dict(density=0.5,brightness=0.55,guidance=4.5)))
> 
> # cumulative offset (s) per scene → act offsets (shifted by the intro)
> offset = {}; acc = 0.0
> for n in range(1, 49):
>     f = f"{WORK}/seg_{n:02d}.mp4"
>     if os.path.exists(f):
>         offset[n] = acc; acc += seg_dur(f)
> film_total = acc
> act_off = [INTRO_S + offset.get(s, 0.0) for s in ACT_START_SCENE]
> act_off.append(INTRO_S + film_total)          # credits cue starts where the film ends
> TOTAL = INTRO_S + film_total + CREDITS_S
> print("total:", round(TOTAL,1), "s (intro %.0f + film %.1f + credits %.1f)" % (INTRO_S, film_total, CREDITS_S), flush=True)
> print("act offsets:", [round(x,1) for x in act_off], flush=True)
> 
> def secao(k):
>     for s in SECOES:
>         if k + 1 <= s["ate_ato"]: return s
>     return SECOES[-1]
> reset_em = next((k for k in range(1, len(CUES)) if secao(k) is not secao(k-1)), None)
> 
> async def gerar():
>     os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY",""))
>     client = genai.Client(http_options={"api_version":"v1alpha"})
>     buf = bytearray()
>     alvo = int((TOTAL + 6) * BPS)
>     dead = {"v": False}
>     async def recv(session):
>         try:
>             async for msg in session.receive():
>                 sc = getattr(msg,"server_content",None)
>                 if sc and getattr(sc,"audio_chunks",None): buf.extend(sc.audio_chunks[0].data)
>                 await asyncio.sleep(1e-12)
>         except Exception as e:
>             print("recv stopped: %s" % str(e)[:80], flush=True); dead["v"] = True
>     segs = lambda: len(buf)/BPS
>     async with client.aio.live.music.connect(model="models/lyria-realtime-exp") as session, asyncio.TaskGroup() as tg:
>         tg.create_task(recv(session))
>         async def aplica(k):
>             c,s = CUES[k], secao(k)
>             await session.set_weighted_prompts(prompts=[types.WeightedPrompt(text=t,weight=w) for t,w in c["prompts"]])
>             await session.set_music_generation_config(config=types.LiveMusicGenerationConfig(bpm=s["bpm"], scale=SCALE, seed=SEED, temperature=1.0, top_k=40, music_generation_mode=types.MusicGenerationMode.QUALITY, **c["cfg"]))
>         await aplica(0); await session.play()
>         print("[00:00] ato 1 (bpm %d)"%secao(0)["bpm"], flush=True)
>         prox, t0, extra_i = 1, time.time(), 0
>         last_len, last_grow = 0, time.time()
>         while len(buf) < alvo and not dead["v"]:
>             if len(buf) > last_len: last_len, last_grow = len(buf), time.time()
>             elif time.time() - last_grow > 20:
>                 print("!! stalled at %.1fs — stopping"%segs(), flush=True); break
>             # intra-act emotional lifts (Sovereign: more emotion after 30s)
>             while extra_i < len(EXTRA_STEER) and segs() >= max(0.0, EXTRA_STEER[extra_i][0] - ANTECIPACAO_S):
>                 try:
>                     await aplica(EXTRA_STEER[extra_i][1])
>                     print("[%.1f] LIFT → cue %d (emotional)"%(segs(), EXTRA_STEER[extra_i][1]), flush=True)
>                 except Exception as e: print("lift err: %s"%str(e)[:50], flush=True)
>                 extra_i += 1
>             if prox < len(act_off):
>                 quando = max(0.0, act_off[prox] - ANTECIPACAO_S)
>                 if segs() >= quando:
>                     try:
>                         if prox == reset_em:
>                             await session.reset_context(); await aplica(prox); await session.play()
>                             print("[%.1f] RESET ato %d (bpm %d)"%(segs(),prox+1,secao(prox)["bpm"]), flush=True)
>                         else:
>                             await aplica(prox); print("[%.1f] ato %d"%(segs(),prox+1), flush=True)
>                     except Exception as e:
>                         print("steer err (ignored): %s"%str(e)[:60], flush=True)
>                     prox += 1
>             if time.time()-t0 > (TOTAL+6)*3+180:
>                 print("!! timeout %.1fs"%segs(), flush=True); break
>             await asyncio.sleep(0.25)
>         try: await session.stop()
>         except Exception: pass
>     # accept a partial that got through all act boundaries (+8s into the final act) — pad/fade to TOTAL
>     got = len(buf)/BPS
>     if got < act_off[-1] + 8:
>         raise RuntimeError("only %.1fs generated (need >= %.1fs) — retry"%(got, act_off[-1]+8))
>     n = int(TOTAL*BPS)
>     if len(buf) < n: buf.extend(b"\x00" * (n - len(buf)))  # pad short tail with silence (fade covers it)
>     a = np.frombuffer(bytes(buf[:n]), dtype="<i2").astype(np.float32).reshape(-1,CH)
>     fi,fo = int(FADE_IN_S*SR), int(FADE_OUT_S*SR)
>     a[:fi] *= np.linspace(0,1,fi)[:,None]
>     if len(a)>fo: a[-fo:] *= np.linspace(1,0,fo)[:,None]
>     with wave.open(f"{WORK}/trilha.wav","wb") as w:
>         w.setnchannels(CH); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.astype("<i2").tobytes())
>     print("OK trilha.wav  %.1fs"%(len(a)/SR), flush=True)
> 
> for attempt in range(5):
>     try:
>         asyncio.run(gerar()); break
>     except Exception as e:
>         print("attempt %d failed: %s — retrying in 12s" % (attempt+1, str(e)[:140]), flush=True)
>         time.sleep(12)
> else:
>     print("!! trilha failed after retries", flush=True)
> ```

## 🤖 Claude *(21:50:44)*

<details>
<summary>💭 Thinking Process</summary>

Agora vejo a estrutura completa: A5 é a concatenação de três arquivos de vídeo (intro, filme e créditos), onde o filme provavelmente já contém o áudio com a trilha ducada aplicada. Preciso investigar como esses arquivos foram montados — se houve um passo de montagem separado para A5 além do v3, e confirmar que os arquivos n_* são realmente do mesmo período de renderização.

Para A6, a mudança é significativa: o VFX de 10 segundos (`title10s_final.mp4`) substitui a cartela de introdução antiga de 5 segundos, já que o VFX contém a mesma mensagem "GABRIEL AI APRESENTA" que transiciona para "EU NÃO EXISTO". Isso torna a cartela anterior redundante. A nova estrutura fica: VFX de abertura (10s) + filme + créditos.

Além disso, preciso reescrever a trilha sonora para ser mais alegre e esperançosa — os cues emocionais atuais não transmitem a sensação de felicidade e esperança desejada. Vou revisar as escalas disponíveis para encontrar algo mais brilhante e maior que a combinação F_MAJOR_D_MINOR atual.

A trilha será contínua cobrindo toda a sequência (intro + filme + créditos), e com o VFX tendo 10 segundos, o parâmetro INTRO_S muda de 5.0 para 10.0. Agora preciso verificar se o arquivo `speech.wav` com a narração já existe para o remix final. Então os comandos foram improvisados, mas consigo reconstruir tudo: tenho os componentes e a receita geral (v3 + bookends). Para o A6, vou criar uma trilha limpa com Lyria usando cues felizes e esperançosos, com intro de 10s e créditos de 13.65s (vou confirmar a duração exata do vídeo de créditos). Se o speech.wav do A5 existir, reutilizo; senão reconstruo pela receita v3. Depois faço o ducking da trilha sob a fala e monto o filme final com o vídeo base de 48 cenas mais o áudio.

A estratégia mais limpa é montar o vídeo completo primeiro (intro de 10s + filme + créditos, tudo normalizado em 1280x720@30fps) e depois aplicar o áudio por cima como uma camada única: a trilha ducada misturada com a fala deslocada em +10s, evitando costuras.

O speech.wav foi construído com offsets começando do zero do filme, então preciso adicionar um delay de 10 segundos quando o vídeo completo for montado — a trilha já foi gerada com os offsets da intro embutidos. Depois vou fazer QA com detecção de volume, verificar durações via ffprobe, examinar frames de amostra e analisar estatísticas de loudness, antes de fazer upload do master para a biblioteca de assets.

Para subir o master, preciso encontrar como o master anterior foi enviado — provavelmente existe um uploader na sessão anterior que usou a RPC register_creative_asset e fez upload para o bucket canvas-assets. Vou procurar por um script de upload no scratchpad para entender o fluxo antes de criar meu próprio.

Agora preciso preparar uma amostra calibrada para o screencast. O arquivo screencast-batch.ts já existe, então vou adaptá-lo para 1920×1080 com zoom de 70% — posso usar a API do Playwright para simular o zoom do navegador via keyboard shortcuts ou ajustar as métricas do dispositivo através do Chrome DevTools Protocol. Configurando o viewport e deviceScaleFactor para capturar screenshots em 1920×1080 com zoom de 70%, e usando screencast ou video recording do Playwright para gravar. Os elementos principais que precisam colapsar são o menu sidebar, as sub-abas do painel de assets e o painel de propriedades à direita, que abre ao clicar em um nó.

Isso é calibração que farei depois, mas agora preciso focar em completar o inventário dos arquivos master (trilha.wav, speech.wav, vídeos seg_*.mp4) e descobrir como os arquivos final5 foram gerados. Depois vou escrever a trilha v2 com cues felizes, trabalhando no meu scratchpad para manter segurança dos dados.

Vou copiar os scripts de produção para o scratchpad para versionamento e eventualmente promovê-los ao repo (sem os binários). Antes de rodar a trilha v2, preciso verificar onde está a GEMINI_API_KEY — provavelmente no .env do repo, como a sessão anterior usou. Enquanto a trilha está sendo gerada em tempo real (cerca de 7-8 minutos de áudio), posso preparar o assemble-v6.ts e calibrar o screencast. Primeiro preciso completar o inventário, localizar o uploader e verificar se o google-genai está instalado no ambiente Python — provavelmente já está no venv ou no sistema, já que a sessão anterior rodou com sucesso.

</details>


## 🤖 Claude *(21:50:45)*

<details>
<summary>💭 Thinking Process</summary>

Entendi a estrutura: o A5 tem cartela + 48 cenas + créditos, e o A6 vai substituir a cartela por um VFX de título de 10s com a apresentação já incluída, mantendo o filme e créditos com uma trilha nova mais esperançosa. Agora vou completar o inventário e verificar os pré-requisitos necessários.

</details>


## 🤖 Claude *(21:50:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; ls \"$SP/master/\" | grep -vE \"^scene_|^src_|^seg_|_f\\.jpg$|\\.jpg$\" ; echo \"=== segs count ===\"; ls \"$SP/master/\" | grep -c \"^seg_\"; ls \"$SP/master/\" | grep -c \"^src_\"; echo \"=== uploader? ===\"; ls \"$SP\" | grep -iE \"upload|publish|register\"; grep -l \"register_creative_asset\\|canvas-assets\" \"$SP\"/*.ts 2>/dev/null",
  "description": "Complete master/ inventory, find the Library uploader script"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> base3.mp4
> base4.mp4
> concat3.txt
> concat4c.txt
> concat4.txt
> concat5.txt
> concat.txt
> creditos.mp4
> final4c.wav
> final4.wav
> final5.wav
> final_audio.m4a
> intro.mp4
> master_A2.mp4
> master_A3_final.mp4
> master_A3.mp4
> master_A4.mp4
> master_A5.mp4
> master_A.mp4
> n_cred.mp4
> n_film.mp4
> n_intro.mp4
> speech4c.wav
> speech4.wav
> speech5.wav
> speech.wav
> trilha.wav
> video4.mp4
> video5.mp4
> video_only.mp4
> voice_deeper_A.wav
> voice_n_voice_ato1.wav
> voice_n_voice_ato2.wav
> voice_n_voice_ato3.wav
> voice_n_voice_ato4.wav
> voice_n_voice_ato5.wav
> voice_n_voice_ato6.wav
> === segs count ===
> 48
> 26
> === uploader? ===
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/assemble-v3.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/assemble-master.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/bw-dl.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/inventory.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/qa-dl.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/sample-dl.ts
> ```

## 🤖 Claude *(21:50:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 -c \"import google.genai, numpy; print('google-genai OK')\" 2>&1; ls /home/gcrUX/htdocs/constellation-orchestra/.env >/dev/null 2>&1 && grep -cE \"SB_SECRET_KEY|SUPABASE_URL\" /home/gcrUX/htdocs/constellation-orchestra/.env; SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; tail -12 \"$SP/trilha6.log\"",
  "description": "Verify python google-genai availability, .env keys, last trilha run log"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> google-genai OK
> 3
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-trilha.py:79: ExperimentalWarning: Realtime music generation is experimental and may change in future versions.
>   async with client.aio.live.music.connect(model="models/lyria-realtime-exp") as session, asyncio.TaskGroup() as tg:
> [00:00] ato 1 (bpm 74)
> [28.0] LIFT → cue 1 (emotional)
> [50.0] ato 2
> [114.0] RESET ato 3 (bpm 98)
> [192.0] ato 4
> [280.0] ato 5
> [352.0] ato 6
> [396.0] ato 7
> recv stopped: 1011 None. The service is currently unavailable.
> OK trilha.wav  411.6s
> ```

## 🤖 Claude *(21:51:31)*

<details>
<summary>💭 Thinking Process</summary>

Tenho os 48 segmentos prontos com o speech5.wav do A5 e a trilha antiga, google-genai configurado no Python do sistema, e as credenciais do Supabase no .env — agora preciso descobrir como o master foi enviado, já que não encontrei um uploader específico, pode ter sido via ingest-external-asset ou upload direto ao bucket com registro posterior.

Meu próximo passo é verificar as durações exatas dos componentes (n_film, n_intro, n_cred, video5, speech5, trilha.wav, title10s_final) com ffprobe para definir os tempos reais de INTRO_S e CREDITS_S, depois puxar a chave de API do Google do User 0 via REST (decrypted_user_api_keys) e reescrever a trilha v2 com as cues ajustadas.

Vou redesenhar os cues para transmitir mais FELIZ e ESPERANÇA — piano warm e hopeful no Ato 1 com luz matinal e otimismo terno, aumentando o BPM um pouco (74→80) e ajustando o brilho geral, talvez mantendo F_MAJOR_D_MINOR ou experimentando uma escala mais brilhante, com retry e stall detection preservados.

Agora preciso estruturar os seis atos com essa energia: começando com um swell joyful, passando por builds uplifting com strings brilhantes, revelação inspiring, drive triumphante, crescendo euphoric, e finalizando com uma resolução heartfelt e hopeful (sem braams thunderous), seguido de um warm afterglow nos créditos. Enquanto a trilha v2 roda em background, vou escrever o assemble-v6.ts para normalizar o vídeo title (provavelmente renderizado em 1920×1080, preciso converter para 1280x720@30) e integrar com o filme video5.mp4 ou video_only.mp4.

Para o áudio, vou usar speech5.wav (narração + Veo do A5 já pronto) ducado com a trilha_v2, e verificar se as durações do vídeo do A5 e dos créditos (n_cred.mp4, ~13.65s) casam corretamente.

Depois preciso confirmar exatamente o que são video5 e n_film — suas durações e streams — e então fazer o QA do Master A6 (durações, volumedetect, frames Vision) antes de registrá-lo na Biblioteca, provavelmente usando o mesmo fluxo de upload que o A5 seguiu.

Para o screencast calibrado, vou examinar o screencast-batch.ts, adaptá-lo para zoom 70% com colapsos, gravar uma amostra de teste e aguardar o exemplo do Sovereign. A produção é sequencial no ffmpeg do host, mas as partes B, D e F podem ser desenvolvidas em paralelo como autoria de scripts — vou executar inline com cuidado, já que é produção com verificação material a cada etapa.

Considerando o custo de coordenação de subagentes sobre o mesmo estado do FS, vou usar Vision QA inline para leitura de frames. Um workflow para revisão adversarial do assemble script antes de rodar teria overhead aceitável e pegaria bugs, mas o assemble é ffmpeg determinístico com prova material a cada etapa via ffprobe — erros aparecem imediatamente. Vou manter inline com gates materiais rigorosos.

Começando com ffprobe batch e puxando a chave Google do User 0.

</details>


## 🤖 Claude *(21:51:33)*

<details>
<summary>💭 Thinking Process</summary>

Tudo pronto: tenho os 48 segundos, áudio, vídeo, créditos e a API do Google configurada. Vou rodar a trilha v2 em background, montar o A6 com VFX e créditos, fazer QA, e preparar um screencast de teste enquanto verifico as durações exatas e a chave Gemini.

</details>


## 🤖 Claude *(21:51:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; for f in title/title10s_final.mp4 master/video5.mp4 master/n_film.mp4 master/n_cred.mp4 master/n_intro.mp4 master/speech5.wav master/trilha.wav master/master_A5.mp4; do d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 \"$SP/$f\" 2>/dev/null); s=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 \"$SP/$f\" 2>/dev/null); a=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 \"$SP/$f\" 2>/dev/null); echo \"$f \u2192 dur=${d}s video=[$s] audio=[$a]\"; done",
  "description": "Probe durations and streams of all A6 assembly components"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> title/title10s_final.mp4 → dur=10.000000s video=[1280,720,30/1] audio=[aac]
> master/video5.mp4 → dur=411.633333s video=[1280,720,30/1] audio=[]
> master/n_film.mp4 → dur=393.000000s video=[1280,720,30/1] audio=[]
> master/n_cred.mp4 → dur=13.633333s video=[1280,720,30/1] audio=[]
> master/n_intro.mp4 → dur=5.000000s video=[1280,720,30/1] audio=[]
> master/speech5.wav → dur=411.630000s video=[] audio=[pcm_s16le]
> master/trilha.wav → dur=411.623333s video=[] audio=[pcm_s16le]
> master/master_A5.mp4 → dur=411.633333s video=[1280,720,30/1] audio=[aac]
> ```

## 🤖 Claude *(21:51:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && curl -s \"$SUPABASE_URL/rest/v1/decrypted_user_api_keys?user_id=eq.ada39fae-2d8f-4fbe-b276-b1a06aebd8e8&select=decrypted_google_api_key\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); k=(d[0].get('decrypted_google_api_key') or '') if d else ''; print('google_api_key: PRESENT len=%d prefix=%s' % (len(k), k[:6]) if k else 'ABSENT')\"",
  "description": "Check User 0 Google API key presence (masked) for Lyria"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 1
> Traceback (most recent call last):
>   File "<string>", line 1, in <module>
> KeyError: 0
> ```

## 🤖 Claude *(21:52:02)*

<details>
<summary>💭 Thinking Process</summary>

Estou analisando os componentes do projeto: o title10s_final já está renderizado em 1280×720@30fps com áudio AAC, mas preciso verificar se contém som real ou apenas silêncio. A estrutura do master_A5.mp4 é composta pelo video5.mp4 de 411.63 segundos mais a trilha de áudio final.

Descobri que o speech5.wav está deslocado +5 segundos (offset da intro antiga), então para o A6 com abertura de 10 segundos, preciso extrair apenas a fala do filme (trimando os primeiros 5 segundos e mantendo 393 segundos) e reaplicar um delay de 10 segundos. A trilha v2 foi gerada com INTRO_S=10.0, resultando em um total de 416.63 segundos. Para o A6, vou combinar o vídeo do title de 10 segundos com o filme de 393 segundos e créditos de 13.63 segundos, aplicando a fala ajustada e a trilha v2 com ducking — mas preciso primeiro confirmar se o VFX do title tem áudio embutido ou se é apenas silêncio.

Sobre a chave Google: a query REST retornou vazio, provavelmente porque o nome da coluna na view decrypted_user_api_keys não é `decrypted_google_api_key` mas sim `google_api_key` (os nomes das colunas são os mesmos, apenas os valores estão decifrados).

Vou refazer o probe com o nome correto da coluna e também verificar o áudio do title10s para entender a trilha. Depois preciso escrever trilha-v2.py e disparar em background.

</details>


## 🤖 Claude *(21:52:03)*

<details>
<summary>💭 Thinking Process</summary>

Decifrei a estrutura do A5: o vídeo tem intro de 5s, filme de 393s e créditos de 13.63s, com o áudio já na timeline com offset embutido. Para o A6, vou extrair o speech do filme e re-deslocar para o offset de 10s, depois corrigir a chave de coluna e sondar o áudio do VFX.

</details>


## 🤖 Claude *(21:52:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && curl -s \"$SUPABASE_URL/rest/v1/decrypted_user_api_keys?user_id=eq.ada39fae-2d8f-4fbe-b276-b1a06aebd8e8&select=google_api_key\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -c \"import json,sys; d=json.load(sys.stdin); k=(d[0].get('google_api_key') or '') if isinstance(d,list) and d else ''; print('google_api_key: PRESENT len=%d prefix=%s' % (len(k), k[:6]) if k else 'ABSENT \u2192 resp=%s' % str(d)[:200])\"",
  "description": "Check User 0 Google API key (correct column name, masked)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ABSENT → resp=[]
> ```

## 🤖 Claude *(21:52:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; ffmpeg -i \"$SP/title/title10s_final.mp4\" -af volumedetect -f null /dev/null 2>&1 | grep -E \"mean_volume|max_volume\"",
  "description": "Check whether title VFX has embedded audio or silence"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [Parsed_volumedetect_0 @ 0xb94938960fe0] mean_volume: -19.0 dB
> [Parsed_volumedetect_0 @ 0xb94938960fe0] max_volume: -1.9 dB
> ```

## 🤖 Claude *(21:52:33)*

<details>
<summary>💭 Thinking Process</summary>

Checking the Google key for User 0 via REST returns an empty response, which is unexpected. I know from memory that User 0 is `ada39fae` with the email gabrielcall@gmail.com, but I'm uncertain about the full UUID since I may have guessed at the suffix. I need to fetch the actual user record to verify the correct identifier.

The title VFX actually contains real audio (averaging around -19dB with peaks at -1.9dB), so it's definitely not silent. Since the previous session rendered the title with sound design and Sovereign approved it, I should preserve that audio. For the mix, I'm thinking the title audio runs for the first 10 seconds, then transitions into the speech and soundtrack. The cleaner approach is to generate the soundtrack v2 starting at the 10-second mark with a fade-in that overlaps slightly with the title's ending, rather than layering the soundtrack underneath from the beginning. A trilha entrando aos 10s com fade-in de 1.5s cria um respiro natural depois que o sound design do title termina. Vou manter esse corte limpo sem overlap, e o Sovereign pode dar feedback se precisar ajustar. Agora preciso encontrar o user_id real do User 0.

</details>


## 🤖 Claude *(21:52:34)*

<details>
<summary>💭 Thinking Process</summary>

O VFX do título tem seu próprio sound design aprovado que vou preservar nos 10s de abertura, deixando a trilha nova entrar com fade junto ao filme. Estou buscando o user_id real do User 0 já que a query anterior retornou vazia.

</details>


## 🤖 Claude *(21:52:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && curl -s \"$SUPABASE_URL/rest/v1/profiles?select=id,email&email=eq.gabrielcall@gmail.com\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | head -c 300; echo; curl -s \"$SUPABASE_URL/rest/v1/decrypted_user_api_keys?select=user_id&google_api_key=not.is.null\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | head -c 300",
  "description": "Find User 0 real UUID via profiles and api keys table"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"code":"42703","details":null,"hint":null,"message":"column profiles.email does not exist"}
> [{"user_id":"ada39fae-67e1-4e53-af1c-5a18e1c108e8"}, 
>  {"user_id":"43027d04-8239-4dd7-9a70-4496c3b1be7a"}]
> ```

## 🤖 Claude *(21:52:59)*

<details>
<summary>💭 Thinking Process</summary>

Identificando o usuário pela chave `ada39fae` na memória, vou extrair sua chave de API do Google e passá-la para o script trilha-v2 via variável de ambiente, garantindo que não vaze no chat enquanto executo em background.

Agora vou criar o script `ep05-trilha-v2.py` no meu scratchpad com o diretório de trabalho apontando para o master antigo, começando a trilha no tempo 0.0 (com delay de 10s no mix final) e créditos em 13.6333s. Vou redesenhar as cues com um tom feliz e esperançoso mantendo a estrutura de 6 atos, usando um novo seed para variar a geração, aplicando os offsets do filme e fade-in/fade-out apropriados. Os atos agora têm características de esperança — piano quente com strings suaves no início, construindo para um crescendo eufórico com arpejos brilhantes e energia triunfante.

Preciso verificar quais escalas estão disponíveis no enum do Lyria para escolher entre F_MAJOR_D_MINOR (que sei que existe) ou D_MAJOR_B_MINOR (mais brilhante), e ajustar os BPMs progressivamente de 78 para 100 e depois 106 conforme os atos avançam.

Enquanto a trilha sonora gera, vou escrever o arquivo de montagem que mapeia as cenas para seus offsets no filme e dispara a geração via API, usando a ferramenta Bash para executar o processo em background.

</details>


## 🤖 Claude *(21:53:01)*

<details>
<summary>💭 Thinking Process</summary>

Encontrei a chave da API do Google configurada. Agora vou explorar os enums de Scale disponíveis e escrever a trilha v2 com os cues redesenhados para alegria e esperança.

</details>


## 🤖 Claude *(21:53:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 -c \"from google.genai import types; print([s.name for s in types.Scale])\"",
  "description": "List available Lyria Scale enum values"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ['SCALE_UNSPECIFIED', 'C_MAJOR_A_MINOR', 'D_FLAT_MAJOR_B_FLAT_MINOR', 'D_MAJOR_B_MINOR', 'E_FLAT_MAJOR_C_MINOR', 'E_MAJOR_D_FLAT_MINOR', 'F_MAJOR_D_MINOR', 'G_FLAT_MAJOR_E_FLAT_MINOR', 'G_MAJOR_E_MINOR', 'A_FLAT_MAJOR_F_MINOR', 'A_MAJOR_G_FLAT_MINOR', 'B_FLAT_MAJOR_G_MINOR', 'B_MAJOR_A_FLAT_MINOR']
> ```

## 🤖 Claude *(21:53:06)*

<details>
<summary>💭 Thinking Process</summary>

D major works well here — it has that classic bright, triumphant quality perfect for festive symphonies. I'll go with D_MAJOR_B_MINOR and start writing out the updated soundtrack script.

</details>


## 🤖 Claude *(21:53:07)*

<details>
<summary>💭 Thinking Process</summary>

Found that D_MAJOR_B_MINOR is available — D major gives that classic bright, triumphant sound compared to the original F major. Now I'll write the v2 track.

</details>


## 🤖 Claude *(21:53:45)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/ep05-trilha-v2.py",
  "content": "#!/usr/bin/env python3\n\"\"\"EP05 soundtrack v2 \u2014 Lyria RealTime. Sovereign direction 2026-08-03:\n\"trilha emocionante e tamb\u00e9m mais FELIZ, e que d\u00ea ESPERAN\u00c7A\".\nChanges vs v1: D MAJOR (bright/triumphant key), all cues rewritten joyful/hopeful/radiant\n(no dark mystery, no braams), brightness raised across acts, bpm 78\u2192100\u2192106.\nTimeline: NO intro offset \u2014 track starts WITH the film (title VFX keeps its own sound\ndesign 0-10s; mix applies adelay 10s to this track). Output: trilha_v2.wav (48kHz stereo).\n\"\"\"\nimport asyncio, os, time, wave\nimport numpy as np\nfrom google import genai\nfrom google.genai import types\n\nWORK = \"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master\"\nSR, CH = 48000, 2\nBPS = SR * CH * 2\nANTECIPACAO_S = 3.0\nFADE_IN_S, FADE_OUT_S = 1.5, 3.0\nSEED = 20260804\n\nACT_START_SCENE = [1, 7, 15, 25, 36, 44]\nSECOES = [dict(ate_ato=2, bpm=78), dict(ate_ato=4, bpm=100), dict(ate_ato=99, bpm=106)]\nSCALE = types.Scale.D_MAJOR_B_MINOR\n\nCUES = [\n # Act I \u2014 warm hopeful open (joy from the first note, no dark mystery)\n dict(prompts=[(\"warm hopeful piano over gentle strings, morning light, tender joy, optimistic wonder\",1.0),(\"a new day beginning, soft glowing pads, heartfelt and bright\",0.7)], cfg=dict(density=0.32,brightness=0.44,guidance=4.5)),\n # Act II \u2014 uplifting build (also the 28s LIFT target)\n dict(prompts=[(\"uplifting emotional build, bright warm strings swelling, joyful inspiring piano, hope rising\",1.0),(\"radiant orchestral wonder, something beautiful coming to life, smile-inducing\",0.75),(\"gentle driving pulse, forward and light\",0.5)], cfg=dict(density=0.55,brightness=0.58,guidance=4.5)),\n # Act III \u2014 the method revealed, feel-good radiance\n dict(prompts=[(\"inspiring radiant reveal, soaring warm strings resolving upward, feel-good cinematic energy, heartfelt\",1.0),(\"playful bright arpeggios with warm pads, craft and hope, optimistic momentum\",0.7),(\"light uplifting percussion, buoyant\",0.5)], cfg=dict(density=0.62,brightness=0.62,guidance=4.5)),\n # Act IV \u2014 hopeful anthem drive\n dict(prompts=[(\"soaring hopeful anthem, layered warm strings and bright synth, confident joyful energy, triumphant and kind\",1.0),(\"modern uplifting documentary drive, radiant and moving\",0.7),(\"energetic bright drums, celebratory motion\",0.55)], cfg=dict(density=0.72,brightness=0.68,guidance=4.5)),\n # Act V \u2014 euphoric crescendo of wonder\n dict(prompts=[(\"euphoric joyful crescendo, expansive radiant orchestral strings, tears of joy, the film coming alive, goosebumps of hope\",1.0),(\"soaring wide luminous pad, widescreen wonder and gratitude\",0.85),(\"propulsive uplifting pulse, forward and up\",0.6)], cfg=dict(density=0.80,brightness=0.74,guidance=4.5)),\n # Act VI \u2014 triumphant heartfelt finale: hope FULFILLED (no braams, no thunder)\n dict(prompts=[(\"triumphant heartfelt finale, enormous warm strings, hope fulfilled, radiant emotional resolution, celebratory and beautiful\",1.0),(\"joyful orchestral climax, awe and gratitude, full emotional warmth, major key resolution\",0.9),(\"bright soaring brass and choir-like pads, victorious and kind\",0.7)], cfg=dict(density=0.86,brightness=0.76,guidance=5.5)),\n]\nEXTRA_STEER = [(28.0, 1)]\n\ndef seg_dur(f):\n    import subprocess\n    return float(subprocess.check_output([\"ffprobe\",\"-v\",\"error\",\"-show_entries\",\"format=duration\",\"-of\",\"csv=p=0\",f]).decode().strip() or 0)\n\nINTRO_S = 0.0           # track starts with the film; title VFX keeps its own sound\nCREDITS_S = float(os.environ.get(\"CREDITS_S\", \"13.6333\"))\n# credits cue \u2014 warm grateful afterglow, hopeful sunrise\nCUES.append(dict(prompts=[(\"end credits, warm grateful afterglow, hopeful sunrise, gentle celebration, luminous resolution\",1.0),(\"slow radiant outro, wide warm strings glowing and fading\",0.8),(\"soft heartbeat pulse fading into light\",0.4)], cfg=dict(density=0.5,brightness=0.58,guidance=4.5)))\n\noffset = {}; acc = 0.0\nfor n in range(1, 49):\n    f = f\"{WORK}/seg_{n:02d}.mp4\"\n    if os.path.exists(f):\n        offset[n] = acc; acc += seg_dur(f)\nfilm_total = acc\nact_off = [INTRO_S + offset.get(s, 0.0) for s in ACT_START_SCENE]\nact_off.append(INTRO_S + film_total)\nTOTAL = INTRO_S + film_total + CREDITS_S\nprint(\"total: %.1f s (film %.1f + credits %.2f)\" % (TOTAL, film_total, CREDITS_S), flush=True)\nprint(\"act offsets:\", [round(x,1) for x in act_off], flush=True)\n\ndef secao(k):\n    for s in SECOES:\n        if k + 1 <= s[\"ate_ato\"]: return s\n    return SECOES[-1]\nreset_em = next((k for k in range(1, len(CUES)) if secao(k) is not secao(k-1)), None)\n\nasync def gerar():\n    os.environ.setdefault(\"GOOGLE_API_KEY\", os.environ.get(\"GEMINI_API_KEY\",\"\"))\n    client = genai.Client(http_options={\"api_version\":\"v1alpha\"})\n    buf = bytearray()\n    alvo = int((TOTAL + 6) * BPS)\n    dead = {\"v\": False}\n    async def recv(session):\n        try:\n            async for msg in session.receive():\n                sc = getattr(msg,\"server_content\",None)\n                if sc and getattr(sc,\"audio_chunks\",None): buf.extend(sc.audio_chunks[0].data)\n                await asyncio.sleep(1e-12)\n        except Exception as e:\n            print(\"recv stopped: %s\" % str(e)[:80], flush=True); dead[\"v\"] = True\n    segs = lambda: len(buf)/BPS\n    async with client.aio.live.music.connect(model=\"models/lyria-realtime-exp\") as session, asyncio.TaskGroup() as tg:\n        tg.create_task(recv(session))\n        async def aplica(k):\n            c,s = CUES[k], secao(k)\n            await session.set_weighted_prompts(prompts=[types.WeightedPrompt(text=t,weight=w) for t,w in c[\"prompts\"]])\n            await session.set_music_generation_config(config=types.LiveMusicGenerationConfig(bpm=s[\"bpm\"], scale=SCALE, seed=SEED, temperature=1.0, top_k=40, music_generation_mode=types.MusicGenerationMode.QUALITY, **c[\"cfg\"]))\n        await aplica(0); await session.play()\n        print(\"[00:00] ato 1 (bpm %d, D major)\"%secao(0)[\"bpm\"], flush=True)\n        prox, t0, extra_i = 1, time.time(), 0\n        last_len, last_grow = 0, time.time()\n        while len(buf) < alvo and not dead[\"v\"]:\n            if len(buf) > last_len: last_len, last_grow = len(buf), time.time()\n            elif time.time() - last_grow > 20:\n                print(\"!! stalled at %.1fs \u2014 stopping\"%segs(), flush=True); break\n            while extra_i < len(EXTRA_STEER) and segs() >= max(0.0, EXTRA_STEER[extra_i][0] - ANTECIPACAO_S):\n                try:\n                    await aplica(EXTRA_STEER[extra_i][1])\n                    print(\"[%.1f] LIFT \u2192 cue %d (joyful build)\"%(segs(), EXTRA_STEER[extra_i][1]), flush=True)\n                except Exception as e: print(\"lift err: %s\"%str(e)[:50], flush=True)\n                extra_i += 1\n            if prox < len(act_off):\n                quando = max(0.0, act_off[prox] - ANTECIPACAO_S)\n                if segs() >= quando:\n                    try:\n                        if prox == reset_em:\n                            await session.reset_context(); await aplica(prox); await session.play()\n                            print(\"[%.1f] RESET ato %d (bpm %d)\"%(segs(),prox+1,secao(prox)[\"bpm\"]), flush=True)\n                        else:\n                            await aplica(prox); print(\"[%.1f] ato %d\"%(segs(),prox+1), flush=True)\n                    except Exception as e:\n                        print(\"steer err (ignored): %s\"%str(e)[:60], flush=True)\n                    prox += 1\n            if time.time()-t0 > (TOTAL+6)*3+180:\n                print(\"!! timeout %.1fs\"%segs(), flush=True); break\n            await asyncio.sleep(0.25)\n        try: await session.stop()\n        except Exception: pass\n    got = len(buf)/BPS\n    if got < act_off[-1] + 8:\n        raise RuntimeError(\"only %.1fs generated (need >= %.1fs) \u2014 retry\"%(got, act_off[-1]+8))\n    n = int(TOTAL*BPS)\n    if len(buf) < n: buf.extend(b\"\\x00\" * (n - len(buf)))\n    a = np.frombuffer(bytes(buf[:n]), dtype=\"<i2\").astype(np.float32).reshape(-1,CH)\n    fi,fo = int(FADE_IN_S*SR), int(FADE_OUT_S*SR)\n    a[:fi] *= np.linspace(0,1,fi)[:,None]\n    if len(a)>fo: a[-fo:] *= np.linspace(1,0,fo)[:,None]\n    with wave.open(f\"{WORK}/trilha_v2.wav\",\"wb\") as w:\n        w.setnchannels(CH); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.astype(\"<i2\").tobytes())\n    print(\"OK trilha_v2.wav  %.1fs\"%(len(a)/SR), flush=True)\n\nfor attempt in range(5):\n    try:\n        asyncio.run(gerar()); break\n    except Exception as e:\n        print(\"attempt %d failed: %s \u2014 retrying in 12s\" % (attempt+1, str(e)[:140]), flush=True)\n        time.sleep(12)\nelse:\n    print(\"!! trilha_v2 failed after retries\", flush=True)\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/ep05-trilha-v2.py (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:53:49)*

<details>
<summary>💭 Thinking Process</summary>

Vou disparar a trilha de áudio em background usando a chave injetada para não vazar no output, e como a geração é em tempo real com cerca de 7 minutos de áudio, vou configurar para rodar em background.

</details>


## 🤖 Claude *(21:53:49)*

Disparando a geração da trilha v2 em background (Lyria gera em tempo real — ~7 min para 406s de trilha):

## 🤖 Claude *(21:53:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && export GEMINI_API_KEY=$(curl -s \"$SUPABASE_URL/rest/v1/decrypted_user_api_keys?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=google_api_key\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -c \"import json,sys; print(json.load(sys.stdin)[0]['google_api_key'])\") && python3 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/ep05-trilha-v2.py 2>&1 | grep -v \"ExperimentalWarning\\|async with client\"",
  "description": "Generate joyful/hopeful soundtrack v2 via Lyria RealTime (background)",
  "run_in_background": true
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Command running in background with ID: b2vvl9ihk. Output is being written to: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/b2vvl9ihk.output. You will be notified when it completes. To check interim output, use Read on that file path.
> ```

## 🤖 Claude *(21:54:21)*

<details>
<summary>💭 Thinking Process</summary>

Deixando a trilha rodando em background enquanto trabalho no arquivo assemble-v6.ts. Estou montando o vídeo A6 combinando três arquivos: um título de 10 segundos, o filme principal com 393 segundos sem áudio, e créditos de 13.63 segundos, totalizando 416.63 segundos. Para o áudio, preciso preservar o som do título nos primeiros 10 segundos e depois usar a fala do filme a partir dos 10 segundos em diante.

Meu plano é extrair e processar a fala do filme com um trim específico, depois criar uma versão com delay de 10 segundos alinhada com a trilha sonora. Vou aplicar compressão dinâmica na trilha para que ela recue quando a fala está presente, mantendo o áudio dos créditos sem fala no final. Depois misturo as três fontes de áudio — o título, a fala processada e a trilha com ducking — e aplico normalização de loudness no resultado final.

Para o vídeo, vou usar o concat demuxer para juntar os três arquivos, mas como o título tem áudio e os outros não, é mais seguro fazer uma re-codificação do vídeo em H.264 sem áudio e depois fazer o mux com o áudio final processado.

Agora preciso validar a qualidade: verificar a duração do master (416.63s ±0.1), rodar volumedetect, e confirmar os frames com VFX nos pontos críticos.  Depois vou checar como o asset anterior foi registrado na Biblioteca — procurando pelo take b7da3f30 para replicar o caminho de upload (bucket + RPC de registro) — e então escrever o script de montagem final com a query correspondente.

</details>


## 🤖 Claude *(21:54:22)*

<details>
<summary>💭 Thinking Process</summary>

Enquanto a trilha gera, estou escrevendo o script de montagem do A6 e verificando como o VFX foi registrado na Biblioteca para replicar o caminho de upload.

</details>


## 🤖 Claude *(21:54:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && curl -s \"$SUPABASE_URL/rest/v1/creative_assets?id=like.b7da3f30*&select=id,kind,title,storage_bucket,storage_path,mime_type,byte_size,source_module,asset_role,user_id\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -m json.tool; echo \"=== masters EP05 na Biblioteca (o que restou) ===\"; curl -s \"$SUPABASE_URL/rest/v1/creative_assets?title=ilike.*EP05*&select=id,title,kind,byte_size,created_at,storage_path&order=created_at.desc&limit=15\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -m json.tool | head -60",
  "description": "Inspect how title VFX asset is registered; list surviving EP05 Library assets"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column creative_assets.storage_path does not exist"
> }
> === masters EP05 na Biblioteca (o que restou) ===
> {
>     "code": "42703",
>     "details": null,
>     "hint": null,
>     "message": "column creative_assets.byte_size does not exist"
> }
> ```

## 🤖 Claude *(21:54:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && curl -s \"$SUPABASE_URL/rest/v1/creative_assets?id=like.b7da3f30*&select=*\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -c \"\nimport json,sys\nrows=json.load(sys.stdin)\nfor r in rows:\n    for k,v in r.items():\n        s=str(v)\n        print(f'{k}: {s[:140]}')\n\"",
  "description": "Dump full title VFX asset row to learn the schema"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 1
> Traceback (most recent call last):
>   File "<string>", line 5, in <module>
> AttributeError: 'str' object has no attribute 'items'
> ```

## 🤖 Claude *(21:54:34)*

<details>
<summary>💭 Thinking Process</summary>

Parece que `rows` não é uma lista, mas provavelmente um dicionário de erro — vou apenas imprimir o resultado bruto para ver o que está acontecendo.

</details>


## 🤖 Claude *(21:54:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && curl -s \"$SUPABASE_URL/rest/v1/creative_assets?id=like.b7da3f30*&select=*\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | head -c 2000",
  "description": "Raw dump of title VFX asset row"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"code":"42883","details":null,"hint":"No operator matches the given name and argument types. You might need to add explicit type casts.","message":"operator does not exist: uuid ~~ unknown"}
> ```

## 🤖 Claude *(21:54:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && curl -s \"$SUPABASE_URL/rest/v1/creative_assets?title=ilike.*t%C3%ADtulo*&select=*&order=created_at.desc&limit=3\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -m json.tool | head -80; echo \"=== EP05 assets ===\"; curl -s \"$SUPABASE_URL/rest/v1/creative_assets?title=ilike.*ep05*&select=id,title,kind,mime_type,storage_key,bucket,created_at&order=created_at.desc&limit=20\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | head -c 3000",
  "description": "Find title VFX and EP05 assets in creative_assets"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "id": "b7da3f30-6011-4174-b5f6-1841e5c329bf",
>         "user_id": "ada39fae-67e1-4e53-af1c-5a18e1c108e8",
>         "org_id": null,
>         "kind": "video",
>         "storage_bucket": "canvas-assets",
>         "storage_key": "ada39fae-67e1-4e53-af1c-5a18e1c108e8/masters/ep05-title-take-10s-1785783185901.mp4",
>         "is_public": false,
>         "mime_type": "video/mp4",
>         "file_size_bytes": 1112521,
>         "width": 1280,
>         "height": 720,
>         "duration_seconds": 10,
>         "parent_asset_id": null,
>         "source_module": "spaces",
>         "source_job_id": null,
>         "mesh_node_id": null,
>         "provider": "hyperframes-gsap",
>         "model": "title-sequence",
>         "prompt": null,
>         "title": "EP05 \u2014 TAKE t\u00edtulo VFX 10s (GABRIEL AI APRESENTA \u2192 EU N\u00c3O EXISTO) \u2014 validar criativo",
>         "tags": [],
>         "is_favorite": false,
>         "metadata": {
>             "for": "validation",
>             "take": true,
>             "engine": "gsap+playwright"
>         },
>         "created_at": "2026-08-03T18:53:06.152082+00:00",
>         "updated_at": "2026-08-03T18:53:07.909214+00:00",
>         "provenance_status": "embedded",
>         "provenance_layers": [
>             "c2pa",
>             "iptc"
>         ],
>         "provenance_source_type": "trainedAlgorithmicMedia",
>         "provenance_embedded_at": "2026-08-03T18:53:07.901+00:00",
>         "c2pa_sidecar_key": null
>     }
> ]
> === EP05 assets ===
> {"code":"42703","details":null,"hint":null,"message":"column creative_assets.bucket does not exist"}
> ```

## 🤖 Claude *(21:54:48)*

<details>
<summary>💭 Thinking Process</summary>

The VFX asset is registered in the `canvas-assets` bucket with the key pointing to the episode 5 title take master file, and the provenance bridge has already processed it as embedded. I need to replicate this workflow by uploading the A6 master file to the same bucket with a timestamped filename, then calling the register creative asset RPC with the service role to complete the registration.

Now I need to check what other EP05 assets are still pending and write the assemble-v6.ts script. To get the exact signature for the register_creative_asset RPC call, I'll search through the previous session's scripts—likely in ep05-run.ts—to see how the title asset was registered.

</details>


## 🤖 Claude *(21:54:49)*

<details>
<summary>💭 Thinking Process</summary>

Identifiquei o caminho de upload: bucket `canvas-assets` → `<uid>/masters/…` com registro via RPC. Agora vou verificar como a sessão anterior fez o registro e escrever o assemble-v6.

</details>


## 🤖 Claude *(21:54:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; grep -rn \"register_creative_asset\" \"$SP\"/*.ts | head -5; grep -B3 -A25 \"register_creative_asset\" \"$SP/render-title.ts\" 2>/dev/null || grep -B3 -A25 \"register_creative_asset\" $(grep -rl \"register_creative_asset\" \"$SP\"/*.ts | head -1)",
  "description": "Find the register_creative_asset RPC call pattern from last session"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(21:55:01)*

<details>
<summary>💭 Thinking Process</summary>

Nenhum dos scripts no scratchpad chama `register_creative_asset` — o título foi registrado por outro caminho. Estou examinando o render-title.ts, que é bem pequeno, e considerando se o upload veio via a edge function `ingest-external-asset` (que é owner-scoped, do video-repurpose Fatia 1). O asset mostra `source_module: "spaces"`, mas `ingest-external-asset` provavelmente marcaria `source_module='external'`, então algo não bate.

Vou fazer uma busca mais ampla no scratchpad inteiro por `register` e depois ler o render-title.ts e verificar se há algo de upload no diretório title/. Mas na verdade, em vez de ficar investigando, posso chamar o RPC `register_creative_asset` diretamente — preciso ler a migration 20260716230000 para pegar a assinatura exata com seus 26 argumentos.

</details>


## 🤖 Claude *(21:55:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; cat \"$SP/render-title.ts\"; echo \"=== grep upload broadly ===\"; grep -rln \"canvas-assets\\|storage.from\" \"$SP\" --include=\"*.ts\" --include=\"*.py\" --include=\"*.mjs\" 2>/dev/null",
  "description": "Read render-title.ts and find upload code in old scratchpad"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /**
>  * Deterministic HyperFrames-style render of title.html: GSAP timeline seeked per frame → PNG → MP4.
>  * 10s @ 30fps = 300 frames, 1280×720. Output: title10s.mp4.
>  */
> import { chromium } from 'playwright';
> import { execSync } from 'child_process';
> const DIR = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/title';
> const CHROME = '/home/ubuntu/.cache/ms-playwright/chromium-1226/chrome-linux/chrome';
> const FPS = 30, DUR = 10, N = FPS * DUR;
> execSync(`mkdir -p ${DIR}/frames && rm -f ${DIR}/frames/*.png`);
> 
> const browser = await chromium.launch({ headless: true, executablePath: CHROME });
> const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 })).newPage();
> await page.goto(`file://${DIR}/title.html`, { waitUntil: 'networkidle', timeout: 30000 });
> await page.waitForFunction(() => (window as any).__seek && (window as any).gsap, null, { timeout: 15000 });
> await page.waitForTimeout(300);
> 
> for (let i = 0; i < N; i++) {
>   const t = i / FPS;
>   await page.evaluate((tt) => (window as any).__seek(tt), t);
>   await page.screenshot({ path: `${DIR}/frames/f_${String(i).padStart(4, '0')}.png`, animations: 'disabled' });
> }
> await browser.close();
> console.log(`${N} frames captured`);
> 
> execSync(`ffmpeg -y -framerate ${FPS} -i ${DIR}/frames/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 16 -preset medium -r ${FPS} ${DIR}/title10s.mp4 -loglevel error`);
> console.log('title10s.mp4 built');
> execSync(`for t in 2 5 7; do ffmpeg -y -ss $t -i ${DIR}/title10s.mp4 -frames:v 1 ${DIR}/qa_$t.jpg -loglevel error; done`);
> console.log('QA frames at 2/5/7s ready');
> === grep upload broadly ===
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/sample-dl.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/bw-dl.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/inventory.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/qa-dl.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/gen-per-scene-voice.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/assemble-v3.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/assemble-master.ts
> ```

## 🤖 Claude *(21:55:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"CREATE OR REPLACE FUNCTION public.register_creative_asset\" -A 40 supabase/migrations/20260716230000_*.sql | head -60",
  "description": "Read register_creative_asset RPC signature from migration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(21:55:10)*

<details>
<summary>💭 Thinking Process</summary>

A migration file with that exact name doesn't seem to exist, or grep didn't find the function. I'll check the Postgres catalog directly since that's more reliable for deployed functions — either by calling the RPC with an empty body to read the error message showing the arguments, or by searching through the migration files themselves.

</details>


## 🤖 Claude *(21:55:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rln \"register_creative_asset\" supabase/migrations/ | tail -3; MIG=$(grep -rln \"FUNCTION public.register_creative_asset\" supabase/migrations/ | tail -1); echo \"== $MIG\"; grep -n \"register_creative_asset\" -A 45 \"$MIG\" | sed -n '1,60p'",
  "description": "Find latest register_creative_asset definition in migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260703030000_asset_owner_signing_and_ispublic_repair.sql
> supabase/migrations/20260707230000_creative_assets_allow_spaces_source.sql
> supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql
> == supabase/migrations/20260630120000_avatar_clone_ai_voice_profiles.sql
> 12:--   4. creative_assets.source_module += 'avatar-studio' (table CHECK + register_creative_asset guard)
> 13---
> 14--- Consent gate (avatar_consents + wizard) is DEFERRED to Fatia 3/6 per the BoK SSOT
> 15--- (FR-AC-030/031 — FR-AC-009/010 do not reference avatar_consents). voice_profiles.status
> 16--- (active/revoked) keeps revocation representable; the erase RPC lands in the erasure slice.
> 17--- ─────────────────────────────────────────────────────────────────────────────
> 18-
> 19--- ── 1. voice_profiles (biometric — RLS own default-deny) ─────────────────────
> 20-CREATE TABLE IF NOT EXISTS public.voice_profiles (
> 21-  id                   uuid        DEFAULT gen_random_uuid() PRIMARY KEY,
> 22-  user_id              uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 23-  project_id           uuid,                                            -- canvas project (no FK: `projects` table does not exist)
> 24-  provider             text        NOT NULL CHECK (provider IN ('elevenlabs','cartesia')),
> 25-  clone_method         text        NOT NULL CHECK (clone_method IN ('pvc','ivc','voice_design')),
> 26-  voiceprint_vault_ref text        NOT NULL,                            -- Vault secret UUID (provider voice_id cifrado) — nunca valor em claro
> 27-  language             text        NOT NULL CHECK (language IN ('en','pt-BR')),  -- single language per profile (FM-AC-013: no code-switch)
> 28-  status               text        NOT NULL DEFAULT 'active' CHECK (status IN ('active','revoked')),
> 29-  last_used_at         timestamptz,                                     -- drives retention-sweep by inactivity (erasure slice)
> 30-  created_at           timestamptz NOT NULL DEFAULT now(),
> 31-  updated_at           timestamptz NOT NULL DEFAULT now()
> 32-);
> 33-
> 34-COMMENT ON TABLE public.voice_profiles IS
> 35-  'avatar-clone-ai Fatia 2 — per-user cloned voice profile. voiceprint_vault_ref is a Vault secret id (provider voice_id cifrado); never the plaintext. RLS own; writes only via store_voice_profile RPC (service-role).';
> 36-
> 37-CREATE INDEX IF NOT EXISTS voice_profiles_user_idx ON public.voice_profiles (user_id);
> 38-
> 39-ALTER TABLE public.voice_profiles ENABLE ROW LEVEL SECURITY;
> 40-
> 41--- SELECT own — the client may list its own profiles (base table exposes only the Vault UUID, not the secret).
> 42-CREATE POLICY "voice_profiles_select_own"
> 43-  ON public.voice_profiles FOR SELECT USING (user_id = auth.uid());
> 44--- No client INSERT/UPDATE/DELETE policies: writes flow through store_voice_profile (service-role bypasses RLS).
> 45--- DELETE has no policy at all (default-deny) → erasure happens via a dedicated RPC in the erasure slice.
> 46-
> 47--- updated_at trigger (project convention).
> 48-DROP TRIGGER IF EXISTS trg_voice_profiles_updated_at ON public.voice_profiles;
> 49-CREATE TRIGGER trg_voice_profiles_updated_at
> 50-  BEFORE UPDATE ON public.voice_profiles
> 51-  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 52-
> 53--- ── 2. store_voice_profile — encrypt voice_id → Vault, insert row (clone path) ─
> 54--- SECURITY DEFINER (owned by migration role) can call vault_upsert_secret even though it is
> 55--- REVOKEd from PUBLIC/anon/authenticated. Narrow capability: only this RPC writes voice_profiles.
> 56-CREATE OR REPLACE FUNCTION public.store_voice_profile(
> 57-  p_user_id      uuid,
> --
> 158:-- register_creative_asset is the ONLY writer (REVOKEd from anon/authenticated) — its IF guard must
> 159--- also accept 'avatar-studio', else the insert raises before the table CHECK is reached.
> 160:CREATE OR REPLACE FUNCTION public.register_creative_asset(
> 161-  p_user_id          uuid,
> 162-  p_kind             text,
> 163-  p_storage_bucket   text,
> 164-  p_storage_key      text,
> 165-  p_source_module    text,
> 166-  p_source_job_id    text     DEFAULT NULL,
> 167-  p_is_public        boolean  DEFAULT false,
> 168-  p_mime_type        text     DEFAULT NULL,
> 169-  p_file_size_bytes  bigint   DEFAULT NULL,
> 170-  p_width            int      DEFAULT NULL,
> ```

## 🤖 Claude *(21:55:16)*

<details>
<summary>💭 Thinking Process</summary>

A função existe na migration mais recente com 26 parâmetros, mas como todos têm valores padrão, posso chamar via REST RPC passando apenas os argumentos necessários — o PostgREST faz a correspondência por nome. Preciso no mínimo de p_user_id, p_kind, p_storage_bucket, p_storage_key e p_source_module, com vários opcionais disponíveis como p_mime_type, p_file_size_bytes, dimensões, duração e metadados.

</details>


## 🤖 Claude *(21:55:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "MIG=supabase/migrations/20260716230000_content_provenance_columns.sql; ls supabase/migrations/ | grep 20260716; grep -n \"p_[a-z_]*\" -o $(grep -rln \"FUNCTION public.register_creative_asset\" supabase/migrations/ | tail -1) | awk -F: '{print $2}' | sort -u",
  "description": "List all parameter names of latest register_creative_asset"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 20260716120000_cadence_recurrence.sql
> 20260716190000_pat_allowlist_swarm_read.sql
> 20260716210000_global_app_credentials_admin_tier.sql
> 20260716230000_content_provenance_columns.sql
> p_duration_seconds
> p_file_size_bytes
> p_height
> p_is_public
> p_kind
> p_mesh_node_id
> p_metadata
> p_mime_type
> p_model
> p_org_id
> p_parent_asset_id
> p_prompt
> p_provider
> p_source_job_id
> p_source_module
> p_storage_bucket
> p_storage_key
> p_tags
> p_title
> p_user_id
> p_width
> ```

## 🤖 Claude *(21:55:42)*

<details>
<summary>💭 Thinking Process</summary>

Agora vou escrever os scripts `assemble-v6.ts` e `upload-a6.ts`. Primeiro deixa eu checar o progresso da trilha, que deve estar em torno de 1-2 minutos. Começando com o `assemble-v6.ts`, que vai processar o arquivo de áudio trimando a fala e combinando com os outros elementos do scratchpad.

Detalhando o pipeline de áudio: vou extrair a fala do filme, aplicar delay e padding para atingir exatamente 416.633 segundos, depois processar a trilha com gate de validação (verificando se existe e tem duração mínima de 406s), aplicar compressão dinâmica com a fala como sidechain e reduzir volume em 9dB, combinar o áudio do título (10s), misturar tudo com normalização de loudness, e finalmente muxar com o vídeo re-codificado em H.264.

Preciso replicar a lógica do sidechain compress do v3, onde a trilha é o input 0 e a fala é o input 1, aplicando o volume negativo antes da compressão.

No amix com inputs de durações diferentes, vou desabilitar normalização e transição de dropout para que cada stream termine naturalmente — o áudio do título ocupa apenas 0-10s enquanto os outros continuam, sem conflito.

A trilha já tem fade-in de 1.5s embutido, então não preciso adicionar mais. Loudnorm em uma passada a 48kHz funciona bem, e a codificação do vídeo em 720p30 com crf18 deve levar alguns minutos.

Vou usar preset medium para priorizar qualidade — o upload-a6.ts vai enviar o master_A6.mp4 para canvas-assets com metadados claros indicando que é o master A6 com VFX de título e trilha v2 joyful.

Depois disso, preciso verificar o status da trilha, rodar o assemble (que depende da trilha estar pronta), fazer QA dos frames e fazer upload. O screencast vem depois — vou adiantar a leitura do screencast-batch.ts para calibração futura, mas o master é prioridade agora.

</details>


## 🤖 Claude *(21:55:42)*

Tenho a assinatura completa da RPC. Escrevendo os scripts de montagem e upload:

## 🤖 Claude *(21:56:09)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/assemble-v6.ts",
  "content": "/**\n * EP05 master A6 \u2014 Sovereign direction 2026-08-03:\n *   \u2022 opening = APPROVED 10s title VFX (title10s_final.mp4, keeps its own sound design)\n *   \u2022 film    = n_film.mp4 (48 scenes, video-only, 393s)\n *   \u2022 credits = n_cred.mp4 (13.63s, video-only)\n *   \u2022 speech  = speech5.wav TRIMMED to film timeline (5s..398s) then re-delayed +10s\n *   \u2022 trilha  = trilha_v2.wav (joyful/hopeful, D major) delayed +10s, ducked under speech\n *   \u2022 master  = concat video (re-encode once) + [title audio \u222a speech \u222a ducked trilha] loudnorm -16 LUFS\n */\nimport { execSync } from 'child_process';\nimport { existsSync, statSync } from 'fs';\n\nconst OLD = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad';\nconst W = `${OLD}/master`;\nconst T = `${OLD}/title`;\nconst sh = (c: string) => execSync(c, { stdio: ['ignore', 'pipe', 'pipe'] }).toString();\nconst dur = (f: string) => parseFloat(sh(`ffprobe -v error -show_entries format=duration -of csv=p=0 \"${f}\"`).trim() || '0');\n\n// \u2500\u2500 Gates (Lei 1): every input must exist with sane duration \u2500\u2500\nconst need: [string, number][] = [\n  [`${T}/title10s_final.mp4`, 10], [`${W}/n_film.mp4`, 393], [`${W}/n_cred.mp4`, 13.5],\n  [`${W}/speech5.wav`, 411], [`${W}/trilha_v2.wav`, 400],\n];\nfor (const [f, min] of need) {\n  if (!existsSync(f)) throw new Error(`MISSING input: ${f}`);\n  const d = dur(f);\n  if (d < min - 0.5) throw new Error(`SHORT input: ${f} = ${d}s (need \u2265 ${min})`);\n  console.log(`\u2713 ${f.split('/').pop()} ${d.toFixed(2)}s`);\n}\n\nconst FILM = dur(`${W}/n_film.mp4`);        // 393.00\nconst CRED = dur(`${W}/n_cred.mp4`);        // 13.63\nconst TITLE = dur(`${T}/title10s_final.mp4`); // 10.00\nconst TOTAL = TITLE + FILM + CRED;\nconsole.log(`A6 total target: ${TOTAL.toFixed(2)}s (title ${TITLE} + film ${FILM.toFixed(2)} + cred ${CRED.toFixed(2)})`);\n\n// \u2500\u2500 1. speech on the A6 timeline: speech5 had a 5s intro offset \u2192 trim film span, re-delay +10s \u2500\u2500\nsh(`ffmpeg -y -i ${W}/speech5.wav -af \"atrim=5:${5 + FILM},asetpts=PTS-STARTPTS,adelay=${TITLE * 1000}|${TITLE * 1000},apad=whole_dur=${TOTAL}\" -ar 48000 -ac 2 -c:a pcm_s16le ${W}/speech6.wav -loglevel error`);\nconsole.log(`speech6.wav ${dur(`${W}/speech6.wav`).toFixed(2)}s`);\n\n// \u2500\u2500 2. trilha_v2 on the A6 timeline (+10s), pad to TOTAL \u2500\u2500\nsh(`ffmpeg -y -i ${W}/trilha_v2.wav -af \"adelay=${TITLE * 1000}|${TITLE * 1000},apad=whole_dur=${TOTAL}\" -ar 48000 -ac 2 -c:a pcm_s16le ${W}/trilha6.wav -loglevel error`);\nconsole.log(`trilha6.wav ${dur(`${W}/trilha6.wav`).toFixed(2)}s`);\n\n// \u2500\u2500 3. title's own sound design (0-10s), padded to TOTAL \u2500\u2500\nsh(`ffmpeg -y -i ${T}/title10s_final.mp4 -vn -af \"apad=whole_dur=${TOTAL}\" -ar 48000 -ac 2 -c:a pcm_s16le ${W}/title_audio6.wav -loglevel error`);\n\n// \u2500\u2500 4. duck trilha under speech (same curve as A3/A5) + 3-way mix + loudnorm \u2500\u2500\nsh(`ffmpeg -y -i ${W}/trilha6.wav -i ${W}/speech6.wav -i ${W}/title_audio6.wav -filter_complex \"[0:a]volume=-9dB[m];[m][1:a]sidechaincompress=threshold=0.05:ratio=6:attack=180:release=550[duck];[1:a][duck][2:a]amix=inputs=3:dropout_transition=0:normalize=0[mix];[mix]loudnorm=I=-16:TP=-1.5:LRA=11[out]\" -map \"[out]\" -c:a aac -b:a 192k -ar 48000 ${W}/final6.m4a -loglevel error`);\nconsole.log(`final6.m4a ${dur(`${W}/final6.m4a`).toFixed(2)}s`);\n\n// \u2500\u2500 5. video: title + film + credits, single re-encode for uniform stream \u2500\u2500\nrequire('fs').writeFileSync(`${W}/concat6.txt`,\n  [`file '${T}/title10s_final.mp4'`, `file '${W}/n_film.mp4'`, `file '${W}/n_cred.mp4'`].join('\\n'));\nsh(`ffmpeg -y -f concat -safe 0 -i ${W}/concat6.txt -an -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -r 30 ${W}/video6.mp4 -loglevel error`);\nconsole.log(`video6.mp4 ${dur(`${W}/video6.mp4`).toFixed(2)}s`);\n\n// \u2500\u2500 6. mux \u2500\u2500\nsh(`ffmpeg -y -i ${W}/video6.mp4 -i ${W}/final6.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest ${W}/master_A6.mp4 -loglevel error`);\nconst d = dur(`${W}/master_A6.mp4`);\nconst sz = statSync(`${W}/master_A6.mp4`).size;\nconsole.log(`\\n=== MASTER A6 === ${d.toFixed(2)}s ${(sz / 1e6).toFixed(1)}MB`);\nif (Math.abs(d - TOTAL) > 0.5) throw new Error(`duration drift: got ${d}, want ${TOTAL}`);\n\n// \u2500\u2500 7. QA: window loudness (title / opening / mid / credits) + frames \u2500\u2500\nfor (const [label, ss, tt] of [['title 0-10', 0, 10], ['opening 10-30', 10, 20], ['mid 200-220', 200, 20], ['credits', TITLE + FILM, CRED]] as [string, number, number][]) {\n  const v = sh(`ffmpeg -ss ${ss} -t ${tt} -i ${W}/master_A6.mp4 -af volumedetect -f null /dev/null 2>&1 | grep -E \"mean_volume|max_volume\" | tr '\\\\n' ' '`);\n  console.log(`vol[${label}]: ${v.trim()}`);\n}\nfor (const t of [2, 6, 12, 60, 200, 350, 408]) {\n  sh(`ffmpeg -y -ss ${t} -i ${W}/master_A6.mp4 -frames:v 1 ${W}/qa6_${t}.jpg -loglevel error`);\n}\nconsole.log('QA frames: qa6_{2,6,12,60,200,350,408}.jpg');\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/assemble-v6.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:56:17)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/upload-a6.ts",
  "content": "/** Upload master_A6.mp4 \u2192 canvas-assets/<uid>/masters/ + register_creative_asset (mirrors title-take path). */\nimport { createClient } from '@supabase/supabase-js';\nimport { readFileSync, statSync } from 'fs';\n\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth: { persistSession: false } });\nconst UID = 'ada39fae-67e1-4e53-af1c-5a18e1c108e8';\nconst W = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master';\nconst file = `${W}/master_A6.mp4`;\nconst key = `${UID}/masters/ep05-master-A6-${Date.now()}.mp4`;\n\nconst bytes = readFileSync(file);\nconst up = await admin.storage.from('canvas-assets').upload(key, bytes, { contentType: 'video/mp4', upsert: false });\nif (up.error) throw new Error(`upload failed: ${up.error.message}`);\nconsole.log('uploaded:', key, `${(statSync(file).size / 1e6).toFixed(1)}MB`);\n\nconst { data, error } = await admin.rpc('register_creative_asset', {\n  p_user_id: UID,\n  p_kind: 'video',\n  p_storage_bucket: 'canvas-assets',\n  p_storage_key: key,\n  p_source_module: 'spaces',\n  p_is_public: false,\n  p_mime_type: 'video/mp4',\n  p_file_size_bytes: statSync(file).size,\n  p_width: 1280,\n  p_height: 720,\n  p_duration_seconds: 417,\n  p_provider: 'ffmpeg-assembly',\n  p_model: 'master-a6',\n  p_title: 'EP05 \u2014 MASTER A6 (VFX t\u00edtulo 10s + trilha v2 FELIZ/ESPERAN\u00c7A D-major) \u2014 para parecer',\n  p_metadata: { take: true, master: 'A6', trilha: 'v2-joyful-d-major', opening: 'title-vfx-b7da3f30', for: 'validation' },\n});\nif (error) throw new Error(`register failed: ${error.message}`);\nconsole.log('creative_asset id:', typeof data === 'string' ? data : JSON.stringify(data));\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/upload-a6.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:56:20)*

<details>
<summary>💭 Thinking Process</summary>

Checking the progress on this learning path...

</details>


## 🤖 Claude *(21:56:21)*

<details>
<summary>💭 Thinking Process</summary>

Estou verificando o progresso da trilha em background.

</details>


## 🤖 Claude *(21:56:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/b2vvl9ihk.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	total: 406.6 s (film 393.0 + credits 13.63)
> 2	act offsets: [0.0, 47.8, 110.3, 189.2, 277.0, 349.0, 393.0]
> 3	Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
> 4	[00:00] ato 1 (bpm 78, D major)
> 5	[26.0] LIFT → cue 1 (joyful build)
> 6	[46.0] ato 2
> 7	
> ```

## 🤖 Claude *(21:56:30)*

<details>
<summary>💭 Thinking Process</summary>

A trilha está gerando bem com os atos avançando nos offsets corretos, e ainda preciso de cerca de 6 minutos de geração. Enquanto isso, estou preparando o screencast calibrado revisando o arquivo antigo para adaptar às novas especificações de resolução física 1920×1080 com zoom do navegador em 70%, o que corresponde a um viewport do Playwright de 2743×1543.

Estou configurando o deviceScaleFactor para 0.7 para que a renderização corresponda exatamente à resolução desejada, e planejando o comportamento da interface com o menu principal colapsado, painel de assets com sub-abas, e RightPanel de propriedades que abre automaticamente ao clicar em um nó ou abre um modal com duplo-clique enquanto esconde a sidebar.

</details>


## 🤖 Claude *(21:56:30)*

<details>
<summary>💭 Thinking Process</summary>

A trilha está progredindo bem com 46 segundos gerados e os atos e LIFT nos offsets corretos. Enquanto ela continua gerando, estou preparando a calibração do screencast lendo o script da sessão anterior para entender o que causou as gravações ruins.

</details>


## 🤖 Claude *(21:56:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/screencast-batch.ts",
  "description": "Read last session's screencast batch script"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /**
>  * EP05 screencast batch recorder — config-driven, 1080p (1280×720) logged-in captures with an
>  * animated cyan cursor. Proven technique (screencast-proof.ts). Records the display-oriented scenes.
>  *
>  * Usage: bun run screencast-batch.ts sc4 sc34 sc44        (or omit args = all)
>  */
> import { chromium } from 'playwright';
> import { createClient } from '@supabase/supabase-js';
> import { execSync } from 'child_process';
> 
> const URL = process.env.SUPABASE_URL!;
> const SVC = process.env.SB_SECRET_KEY!;
> const ANON = (process.env.SB_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY)!;
> const REF = URL.match(/https:\/\/([a-z0-9]+)\.supabase/)![1];
> const STORAGE_KEY = `sb-${REF}-auth-token`;
> const APP = 'http://localhost:4173';
> const CANVAS = '024e1c03-2866-4e38-afc7-ddc515b5a1c7';
> const OUT = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/sc-out';
> const CHROME = '/home/ubuntu/.cache/ms-playwright/chromium-1226/chrome-linux/chrome';
> 
> type Move = { x: number; y: number; pause?: number };
> interface Scene { id: string; url: string; wait?: number; moves: Move[]; secs: number; clickText?: string; clickNth?: number; }
> 
> const SCENES: Scene[] = [
>   { id: 'sc4', url: `/dashboard/spaces/${CANVAS}`, wait: 4000, secs: 10,
>     moves: [{ x: 320, y: 250, pause: 500 }, { x: 640, y: 380, pause: 500 }, { x: 980, y: 300, pause: 500 }, { x: 760, y: 480, pause: 700 }] },
>   { id: 'sc34', url: `/dashboard/spaces/assets`, wait: 4500, secs: 10,
>     moves: [{ x: 300, y: 260, pause: 500 }, { x: 560, y: 340, pause: 500 }, { x: 820, y: 300, pause: 500 }, { x: 1040, y: 420, pause: 700 }] },
>   { id: 'sc44', url: `/dashboard/youtube`, wait: 5000, secs: 11,
>     moves: [{ x: 640, y: 360, pause: 1500 }, { x: 700, y: 400, pause: 2500 }] },
>   // inspector opens: click a node → RightPanel shows its inspector (cost badge, prompt, controls). Cursor circles the right panel.
>   { id: 'sc_gen', url: `/dashboard/spaces/${CANVAS}`, wait: 4000, secs: 9, clickNth: 0,
>     moves: [{ x: 1090, y: 300, pause: 800 }, { x: 1090, y: 460, pause: 900 }, { x: 1000, y: 380, pause: 700 }] },
>   { id: 'sc_voice', url: `/dashboard/spaces/${CANVAS}`, wait: 4000, secs: 9, clickNth: 2,
>     moves: [{ x: 1090, y: 320, pause: 900 }, { x: 1090, y: 480, pause: 900 }, { x: 1000, y: 400, pause: 700 }] },
>   { id: 'sc_i2v', url: `/dashboard/spaces/${CANVAS}`, wait: 4000, secs: 9, clickText: 'POV',
>     moves: [{ x: 1090, y: 300, pause: 900 }, { x: 1090, y: 440, pause: 900 }, { x: 1000, y: 380, pause: 700 }] },
> ];
> 
> const want = process.argv.slice(2).filter(a => !a.startsWith('--'));
> const scenes = want.length ? SCENES.filter(s => want.includes(s.id)) : SCENES;
> 
> // mint session
> const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> const anon = createClient(URL, ANON, { auth: { persistSession: false } });
> const { data: link } = await admin.auth.admin.generateLink({ type: 'magiclink', email: 'gabrielcall@gmail.com' });
> let session: any = null;
> for (const type of ['magiclink', 'email'] as const) {
>   const { data: s } = await anon.auth.verifyOtp({ token_hash: link!.properties!.hashed_token, type });
>   if (s?.session?.access_token) { session = s.session; break; }
> }
> if (!session) { console.error('no session'); process.exit(1); }
> console.log('session ok · recording', scenes.map(s => s.id).join(', '));
> 
> const browser = await chromium.launch({ headless: true, executablePath: CHROME });
> 
> for (const sc of scenes) {
>   const dir = `${OUT}/${sc.id}`;
>   execSync(`mkdir -p ${dir}`);
>   const ctx = await browser.newContext({
>     viewport: { width: 1280, height: 720 },
>     recordVideo: { dir, size: { width: 1280, height: 720 } },
>     deviceScaleFactor: 1,
>   });
>   const page = await ctx.newPage();
>   await page.addInitScript(([k, v]) => localStorage.setItem(k, v), [STORAGE_KEY, JSON.stringify(session)]);
>   await page.addInitScript(() => {
>     (window as any).__cx = 640; (window as any).__cy = 360;
>     const ensure = () => {
>       let c = document.getElementById('__fakecur') as HTMLDivElement | null;
>       if (!c) { c = document.createElement('div'); c.id = '__fakecur';
>         c.style.cssText = 'position:fixed;width:26px;height:26px;border-radius:50%;background:rgba(56,189,248,.30);border:2.5px solid #38bdf8;box-shadow:0 0 16px #38bdf8,0 0 4px #fff;z-index:2147483647;pointer-events:none;left:0;top:0';
>         (document.documentElement || document.body).appendChild(c); }
>       c.style.left = ((window as any).__cx) + 'px'; c.style.top = ((window as any).__cy) + 'px';
>     };
>     (window as any).__setCur = (x: number, y: number) => { (window as any).__cx = x; (window as any).__cy = y; ensure(); };
>     setInterval(ensure, 100);
>   });
> 
>   try {
>     await page.goto(`${APP}${sc.url}`, { waitUntil: 'networkidle', timeout: 45000 });
>   } catch (e) { console.log(`  ${sc.id} goto warn:`, (e as Error).message); }
>   await page.waitForTimeout(sc.wait ?? 3500);
>   // open a node inspector before recording, if requested (click ReactFlow node by text or index)
>   try {
>     if (sc.clickText) { await page.locator('.react-flow__node', { hasText: sc.clickText }).first().click({ timeout: 5000 }); await page.waitForTimeout(1200); }
>     else if (sc.clickNth != null) { await page.locator('.react-flow__node').nth(sc.clickNth).click({ timeout: 5000 }); await page.waitForTimeout(1200); }
>   } catch (e) { console.log(`  ${sc.id} click warn:`, (e as Error).message); }
>   await page.evaluate(() => (window as any).__setCur(640, 360));
> 
>   let cx = 640, cy = 360;
>   const move = async (x: number, y: number, steps = 34) => {
>     const sx = cx, sy = cy;
>     for (let i = 1; i <= steps; i++) {
>       const t = i / steps, e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
>       const nx = sx + (x - sx) * e, ny = sy + (y - sy) * e;
>       await page.evaluate(([nx, ny]) => (window as any).__setCur(nx, ny), [nx, ny]);
>       await page.mouse.move(nx, ny); await page.waitForTimeout(16);
>     }
>     cx = x; cy = y;
>   };
> 
>   for (const m of sc.moves) { await move(m.x, m.y); if (m.pause) await page.waitForTimeout(m.pause); }
>   await ctx.close();
>   const webm = execSync(`ls -t ${dir}/*.webm | head -1`).toString().trim();
>   const mp4 = `${OUT}/${sc.id}.mp4`;
>   // transcode to mp4 h264 for HyperFrames import + extract a QA frame
>   execSync(`ffmpeg -y -i "${webm}" -c:v libx264 -pix_fmt yuv420p -r 30 "${mp4}" -loglevel error`);
>   execSync(`ffmpeg -y -ss 3 -i "${mp4}" -frames:v 1 ${OUT}/${sc.id}_f.jpg -loglevel error`);
>   const dim = execSync(`ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "${mp4}"`).toString().trim();
>   console.log(`  ✅ ${sc.id} → ${mp4} (${dim})`);
> }
> await browser.close();
> console.log('batch done.');
> ```

## 🤖 Claude *(21:56:57)*

<details>
<summary>💭 Thinking Process</summary>

Agora vejo o problema: a gravação estava em resolução menor sem zoom, sem elementos colapsados, e com movimentos de cursor genéricos sem interações reais. Preciso recalibrar para 1920×1080 com zoom de 70%, ajustando o viewport e o deviceScaleFactor para que a gravação de vídeo capture o tamanho correto.

O recordVideo redimensiona o viewport capturado para 1920×1080, então posso deixar o deviceScaleFactor em 1 e deixar o downscaling fazer o trabalho — isso garante nitidez. Agora preciso verificar como colapsar o menu principal (provavelmente via SidebarTrigger do shadcn com estado em localStorage) e as sub-abas do painel de assets no dashboard.

Também vou precisar reconhecer a UI real explorando os componentes — especialmente o LeftPanel com as abas Receitas/Tendências/Históricos e o RightPanel de propriedades que abre ao clicar num nó. O app roda em localhost:4173 via vite preview, então preciso subir o servidor antes de gravar a cena de amostra. Checking the handoff notes, the behavior is already implemented — clicking a node opens the RightPanel, double-clicking opens the NodeConfigWindow and hides the sidebar. I just need to record it correctly. Let me do a quick recon of the collapse selectors and states to confirm what's actually happening.

</details>


## 🤖 Claude *(21:56:58)*

<details>
<summary>💭 Thinking Process</summary>

Identifiquei que a v1 gravava em 1280×720 com zoom 100% sem colapso, enquanto o correto é viewport 2743×1543 + recordVideo 1920×1080 para obter o zoom 70% exato. Agora vou reconhecer os seletores reais de colapso na UI.

</details>


## 🤖 Claude *(21:56:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"Receitas\\|Tend\u00eancias\\|Hist\u00f3ricos\" src/components/canvas/ src/pages/CanvasEditorPage.tsx 2>/dev/null | head -10; echo \"=== sidebar collapse state ===\"; grep -rn \"collapsed\\|collapse\" src/components/dashboard/DashboardSidebar.tsx 2>/dev/null | head -10; ls src/components/dashboard/ | grep -i sidebar",
  "description": "Recon UI collapse selectors (asset panel tabs, main sidebar)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/components/canvas/LeftPanel/index.tsx:29:  { id: "recipes", label: "Receitas", icon: BookOpen },
> src/components/canvas/LeftPanel/index.tsx:31:  { id: "trends", label: "Tendências", icon: TrendingUp },
> src/components/canvas/LeftPanel/index.tsx:37: * Receitas → vm_canvas_recipes, Assets → vm_canvas_assets,
> src/components/canvas/LeftPanel/index.tsx:38: * Tendências → vm_trends, Histórico → vm_canvas_executions.
> src/components/canvas/LeftPanel/index.tsx:207:        Dica: duplo-clique para inserir. Receitas <span className="text-accent">Pipeline</span>{" "}
> src/pages/CanvasEditorPage.tsx:511:                title="Biblioteca / Receitas"
> === sidebar collapse state ===
> src/components/dashboard/DashboardSidebar.tsx:178:  const collapsed = state === 'collapsed';
> src/components/dashboard/DashboardSidebar.tsx:188:  // In icon-only (collapsed) mode, collapsibles have no room — render every
> src/components/dashboard/DashboardSidebar.tsx:190:  const collapsedLeaves: NavLeaf[] = [
> src/components/dashboard/DashboardSidebar.tsx:212:          {!collapsed && (
> src/components/dashboard/DashboardSidebar.tsx:222:        {collapsed ? (
> src/components/dashboard/DashboardSidebar.tsx:227:                {collapsedLeaves.map((item) => (
> src/components/dashboard/DashboardSidebar.tsx:539:          size={collapsed ? 'icon' : 'default'}
> src/components/dashboard/DashboardSidebar.tsx:544:          {!collapsed && <span className="ml-2">Sair</span>}
> DashboardSidebar.tsx
> ```

## 🤖 Claude *(21:57:07)*

<details>
<summary>💭 Thinking Process</summary>

Preciso verificar como o DashboardSidebar usa o componente sidebar do shadcn com seu estado de colapso persistido em cookie, e entender como o estado inicial é carregado através do SidebarProvider. Também preciso investigar o LeftPanel do canvas que tem abas para receitas, assets, trends e histórico — especificamente como o painel inteiro colapsa e se há um botão de toggle na CanvasEditorPage.

</details>


## 🤖 Claude *(21:57:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"SidebarProvider\\|defaultOpen\\|SIDEBAR_COOKIE\" src/components/dashboard/DashboardLayout.tsx src/components/ui/sidebar.tsx 2>/dev/null | head -8; echo \"=== CanvasEditorPage panels toggle ===\"; sed -n '495,545p' src/pages/CanvasEditorPage.tsx",
  "description": "Find sidebar cookie persistence and canvas panel toggles"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/components/dashboard/DashboardLayout.tsx:1:import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
> src/components/dashboard/DashboardLayout.tsx:119:    <SidebarProvider open={open} onOpenChange={setOpen}>
> src/components/dashboard/DashboardLayout.tsx:164:    </SidebarProvider>
> src/components/ui/sidebar.tsx:15:const SIDEBAR_COOKIE_NAME = "sidebar:state";
> src/components/ui/sidebar.tsx:16:const SIDEBAR_COOKIE_MAX_AGE = 60 * 60 * 24 * 7;
> src/components/ui/sidebar.tsx:37:    throw new Error("useSidebar must be used within a SidebarProvider.");
> src/components/ui/sidebar.tsx:43:const SidebarProvider = React.forwardRef<
> src/components/ui/sidebar.tsx:46:    defaultOpen?: boolean;
> === CanvasEditorPage panels toggle ===
>                 aria-label={rightCollapsed ? "Mostrar propriedades" : "Ocultar propriedades"}
>               >
>                 {rightCollapsed ? <PanelRightOpen className="h-4 w-4" /> : <PanelRightClose className="h-4 w-4" />}
>               </Button>
>             </>
>           )}
> 
>           {/* Mobile: FABs redondos só-ícone para abrir as sidebars colapsadas. */}
>           {isMobile && (
>             <>
>               <Button
>                 type="button"
>                 size="icon"
>                 variant="secondary"
>                 onClick={() => setLeftOpen(true)}
>                 className="absolute bottom-4 left-4 z-10 h-12 w-12 rounded-full border border-border shadow-lg"
>                 title="Biblioteca / Receitas"
>                 aria-label="Abrir biblioteca"
>               >
>                 <PanelLeft className="h-5 w-5" />
>               </Button>
>               <Button
>                 type="button"
>                 size="icon"
>                 variant="secondary"
>                 onClick={() => setRightOpen(true)}
>                 className="absolute bottom-[4.75rem] right-4 z-10 h-12 w-12 rounded-full border border-border shadow-lg"
>                 title="Propriedades do nó"
>                 aria-label="Abrir propriedades do nó"
>               >
>                 <SlidersHorizontal className="h-5 w-5" />
>               </Button>
>             </>
>           )}
>         </div>
> 
>         {/* Typed inspectors panel — right column on desktop; a drawer on mobile (below). */}
>         {!isMobile && !rightCollapsed && (
>           <RightPanel
>             projectId={projectId ?? ""}
>             creditsBalance={profile?.mco_balance ?? 0}
>             onCreditsChanged={refetchDashboard}
>           />
>         )}
>       </div>
> 
>       {isMobile && (
>         <>
>           <Sheet open={leftOpen} onOpenChange={setLeftOpen}>
>             <SheetContent side="left" className="w-72 max-w-[86vw] p-0">
>               <SheetTitle className="sr-only">Biblioteca do Canvas</SheetTitle>
> ```

## 🤖 Claude *(21:57:18)*

<details>
<summary>💭 Thinking Process</summary>

Estou analisando as estruturas de estado da interface — a sidebar principal usa um cookie para controlar seu estado colapsado, enquanto o DashboardLayout gerencia isso através de props controladas que provavelmente vêm de um useState com localStorage. O canvas tem seus próprios estados locais para painéis colapsáveis com botões de toggle.

Preciso verificar como esses estados inicializam no CanvasEditorPage e confirmar se clicar em um nó abre automaticamente o painel direito (setando rightCollapsed=false), além de entender o comportamento de duplo-clique que abre o modal de configuração e esconde a sidebar.

</details>


## 🤖 Claude *(21:57:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"rightCollapsed\\|leftCollapsed\\|onNodeClick\\|onNodeDoubleClick\\|configModalOpen\" src/pages/CanvasEditorPage.tsx | head -20; echo \"=== DashboardLayout open state ===\"; sed -n '100,125p' src/components/dashboard/DashboardLayout.tsx",
  "description": "Check canvas panel default states and node click handlers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 341:  const onNodeClick = useCallback(
> 349:  const onNodeDoubleClick = useCallback(
> 405:  const [leftCollapsed, setLeftCollapsed] = useState(false);
> 406:  const [rightCollapsed, setRightCollapsed] = useState(false);
> 425:        {!isMobile && !leftCollapsed && <LeftPanel projectId={projectId} />}
> 434:            onNodeClick={onNodeClick}
> 435:            onNodeDoubleClick={onNodeDoubleClick}
> 483:                title={leftCollapsed ? "Mostrar biblioteca / receitas" : "Ocultar biblioteca / receitas"}
> 484:                aria-label={leftCollapsed ? "Mostrar biblioteca" : "Ocultar biblioteca"}
> 486:                {leftCollapsed ? <PanelLeftOpen className="h-4 w-4" /> : <PanelLeftClose className="h-4 w-4" />}
> 494:                title={rightCollapsed ? "Mostrar Estilo / Propriedades" : "Ocultar Estilo / Propriedades"}
> 495:                aria-label={rightCollapsed ? "Mostrar propriedades" : "Ocultar propriedades"}
> 497:                {rightCollapsed ? <PanelRightOpen className="h-4 w-4" /> : <PanelRightClose className="h-4 w-4" />}
> 532:        {!isMobile && !rightCollapsed && (
> === DashboardLayout open state ===
>       .subscribe();
> 
>     return () => { supabase.removeChannel(channel); };
>   }, [user]);
> 
>   useEffect(() => {
>     if (isConstellation || isCore) setOpen(false);
>     else setOpen(true);
>   }, [isConstellation, isCore]);
> 
>   // Build breadcrumbs
>   const segments = location.pathname.split('/').filter(Boolean);
>   const crumbs = segments.map((seg, i) => ({
>     label: BREADCRUMB_MAP[seg] || seg,
>     path: '/' + segments.slice(0, i + 1).join('/'),
>     isLast: i === segments.length - 1,
>   }));
> 
>   return (
>     <SidebarProvider open={open} onOpenChange={setOpen}>
>       <div className="h-screen flex w-full bg-background overflow-hidden">
>         <DashboardSidebar />
> 
>         <div className="flex-1 flex flex-col min-w-0 min-h-0 h-full overflow-hidden">
>           <header className="h-14 flex items-center justify-between border-b border-border px-4 shrink-0">
>             <div className="flex items-center gap-2">
> ```

## 🤖 Claude *(21:57:34)*

<details>
<summary>💭 Thinking Process</summary>

Encontrei um problema crítico na calibração: o `DashboardLayout` força a sidebar aberta em rotas não-constellation através de um useEffect, então não consigo mantê-la colapsada via cookie — o efeito reabre automaticamente. Porém, o `SidebarTrigger` no header permite colapsar manualmente após o carregamento, já que o useEffect só executa uma vez.

Para o canvas, os painéis esquerdo e direito começam abertos por padrão sem persistência, e preciso clicar nos botões toggle para colapsá-los. Agora preciso verificar se o comportamento de clique único no nó abre o painel direito e clique duplo o fecha automaticamente — conforme descrito pelo Sovereign — ou se isso é um gap de implementação que precisa ser corrigido.

</details>


## 🤖 Claude *(21:57:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '335,375p' src/pages/CanvasEditorPage.tsx",
  "description": "Read onNodeClick and onNodeDoubleClick handlers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   }, [queryClient]);
>   const executeNode = useCanvasExecute();
>   const updateProject = useUpdateCanvasProject();
>   // it.2b: ledger-first runs live in `generations` — StatusBar sums them with the legacy counter.
>   const { data: ledgerRunCount } = useProjectLedgerRunCount(projectId);
> 
>   const onNodeClick = useCallback(
>     (_: unknown, node: Node) => {
>       selectNode(node.id);
>     },
>     [selectNode],
>   );
> 
>   // Amendment 31 — double-click a node opens its config in a window on the canvas (canvas>node>janela).
>   const onNodeDoubleClick = useCallback(
>     (_: unknown, node: Node) => {
>       selectNode(node.id);
>       openConfigModal();
>     },
>     [selectNode, openConfigModal],
>   );
> 
>   const {
>     pipelineStatus,
>     runPipeline,
>     runnableCount,
>     runAllCost,
>   } = useCanvasPipeline({ projectId, refetchDashboard });
> 
>   // Phase 4.2c — Realtime bridge: webhook flips vm_canvas_executions.status,
>   // we reconcile the Zustand store so the canvas node UI updates without refresh.
>   useCanvasJobsRealtime(projectId, (row) => {
>     if (!row.node_id) return;
>     if (row.status === "success") {
>       updateNodeData(row.node_id, {
>         status: "success",
>         output: {
>           videoUrl: row.output_url ?? undefined,
>           imageUrl: row.output_url ?? undefined,
>           generatedAt: row.completed_at ?? new Date().toISOString(),
>         },
> ```

## 🤖 Claude *(21:58:02)*

<details>
<summary>💭 Thinking Process</summary>

Identifiquei o problema: `onNodeClick` apenas seleciona o nó mas não reabre o RightPanel se estiver colapsado, enquanto `onNodeDoubleClick` abre o modal de configuração sem esconder a sidebar. Segundo as especificações, um clique simples deveria abrir o RightPanel automaticamente, independentemente do seu estado anterior.

A solução é adicionar `setRightCollapsed(false)` ao handler de clique simples e `setRightCollapsed(true)` ao de duplo-clique para esconder a sidebar quando o modal abre. Preciso ter cuidado com a ordem de definição dos handlers em relação ao estado `rightCollapsed`, já que eles precisam estar acessíveis quando os handlers forem chamados. The dependency array would trigger a temporal dead zone error if it references setRightCollapsed before initialization, so moving the useState hook earlier in the component is the cleanest solution. This is a small single-file patch that qualifies as a feature refinement, so I can implement and build it directly. For the recording session, I need to serve the app using vite preview with the built dist folder, and I'll set the APP environment variable to localhost:4173 like the previous screencast batch did.

My workflow is: apply the CanvasEditorPage patch for the click-to-open and double-click-to-hide behavior, verify the background track, assemble the A6 artifact once the track is ready, rebuild and preview the patched version, capture a sample screencast, upload A6 to the library, and then run QA on the Vision frames. Let me look at lines 400-410 to find the exact edit location.

</details>


## 🤖 Claude *(21:58:03)*

<details>
<summary>💭 Thinking Process</summary>

Confirmei que o comportamento que você especificou não existe ainda — `onNodeClick` só seleciona o nó sem reabrir o RightPanel, e `onNodeDoubleClick` não esconde a sidebar. Vou implementar isso agora com um patch single-file.

</details>


## 🤖 Claude *(21:58:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx",
  "offset": 398,
  "limit": 14
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 398	  const [rightOpen, setRightOpen] = useState(false);
> 399	  useEffect(() => {
> 400	    if (isMobile && selectedNodeId) setRightOpen(true);
> 401	  }, [isMobile, selectedNodeId]);
> 402	
> 403	  // Desktop: each side panel can be collapsed to give the canvas the whole width (mirrors the main menu's
> 404	  // collapse). Independent of the mobile drawers (leftOpen/rightOpen) above.
> 405	  const [leftCollapsed, setLeftCollapsed] = useState(false);
> 406	  const [rightCollapsed, setRightCollapsed] = useState(false);
> 407	
> 408	  return (
> 409	    <>
> 410	      <TopBar
> 411	        name={project?.name ?? "Sem título"}
> ```

## 🤖 Claude *(21:58:17)*

<details>
<summary>💭 Thinking Process</summary>

I need to reorganize the state declarations by moving the leftCollapsed and rightCollapsed useState hooks earlier in the component, before the callback functions around line 340. Then I'll update the onNodeClick handler to set rightCollapsed to false and the onNodeDoubleClick handler to set it to true. Adicionando os estados de collapse para os painéis laterais e atualizando os handlers de clique para gerenciar a visibilidade do painel direito — quando um nó é selecionado, o painel de propriedades aparece, e quando a modal de configuração abre, o painel é ocultado. Depois preciso remover a declaração antiga desses estados.

</details>


## 🤖 Claude *(21:58:22)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx",
  "old_string": "  const { data: ledgerRunCount } = useProjectLedgerRunCount(projectId);\n\n  const onNodeClick = useCallback(\n    (_: unknown, node: Node) => {\n      selectNode(node.id);\n    },\n    [selectNode],\n  );\n\n  // Amendment 31 \u2014 double-click a node opens its config in a window on the canvas (canvas>node>janela).\n  const onNodeDoubleClick = useCallback(\n    (_: unknown, node: Node) => {\n      selectNode(node.id);\n      openConfigModal();\n    },\n    [selectNode, openConfigModal],\n  );",
  "new_string": "  const { data: ledgerRunCount } = useProjectLedgerRunCount(projectId);\n\n  // Desktop: each side panel can be collapsed to give the canvas the whole width (mirrors the main\n  // menu's collapse). Independent of the mobile drawers (leftOpen/rightOpen). Declared before the\n  // node click handlers so they can drive the right panel (Sovereign 2026-08-03).\n  const [leftCollapsed, setLeftCollapsed] = useState(false);\n  const [rightCollapsed, setRightCollapsed] = useState(false);\n\n  const onNodeClick = useCallback(\n    (_: unknown, node: Node) => {\n      selectNode(node.id);\n      setRightCollapsed(false); // selecting a node always surfaces its properties panel\n    },\n    [selectNode],\n  );\n\n  // Amendment 31 \u2014 double-click a node opens its config in a window on the canvas (canvas>node>janela).\n  const onNodeDoubleClick = useCallback(\n    (_: unknown, node: Node) => {\n      selectNode(node.id);\n      openConfigModal();\n      setRightCollapsed(true); // the config window takes over \u2014 the side panel yields\n    },\n    [selectNode, openConfigModal],\n  );"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:58:24)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx",
  "old_string": "  // Desktop: each side panel can be collapsed to give the canvas the whole width (mirrors the main menu's\n  // collapse). Independent of the mobile drawers (leftOpen/rightOpen) above.\n  const [leftCollapsed, setLeftCollapsed] = useState(false);\n  const [rightCollapsed, setRightCollapsed] = useState(false);\n\n  return (",
  "new_string": "  return ("
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:58:32)*

<details>
<summary>💭 Thinking Process</summary>

Patch is in place. Now I need to run the type gate and build process, while also checking the trace in parallel. Let me kick off the real tsc-app gate and monitor the trace simultaneously.

</details>


## 🤖 Claude *(21:58:32)*

Patch aplicado. Rodando o gate de tipos e checando a trilha:

## 🤖 Claude *(21:58:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc -p tsconfig.app.json --noEmit 2>&1 | head -5; echo \"TSC_EXIT=$?\"",
  "description": "Type-check the app after CanvasEditorPage patch",
  "timeout": 180000
}
```

## 🤖 Claude *(21:58:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/b2vvl9ihk.output"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> TSC_EXIT=0
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	total: 406.6 s (film 393.0 + credits 13.63)
> 2	act offsets: [0.0, 47.8, 110.3, 189.2, 277.0, 349.0, 393.0]
> 3	Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
> 4	[00:00] ato 1 (bpm 78, D major)
> 5	[26.0] LIFT → cue 1 (joyful build)
> 6	[46.0] ato 2
> 7	[108.0] RESET ato 3 (bpm 100)
> 8	[188.0] ato 4
> 9	
> ```

## 🤖 Claude *(21:59:41)*

<details>
<summary>💭 Thinking Process</summary>

TypeScript compilation passed successfully. The build process is running in the background while I set up the screencast v2 specification with a viewport of 2743×1543 and video recording at 1920×1080 with 70% effective zoom, starting with login injection.

Now I'm deciding between two projects for the sample recording: the EP05 v2 project (18a21002) which has 62 nodes and represents the actual episode content, or the canvas project (024e1c03) used in the previous batch. The EP05 v2 project is richer visually and demonstrates the platform building the episode itself, so I'll use that one. For the calibration sample, I'll open the project, collapse everything, click a node to trigger the RightPanel, then double-click to open the modal and hide the sidebar—this single recording demonstrates all the specifications.

The sample sequence takes about 20 seconds: navigate to the project, collapse the main menu, hide the library panel, hide the properties panel to go full-width on the canvas, move the mouse smoothly to a node and click to open the RightPanel, pause for 2 seconds, double-click to open the modal and hide the panel, pause for 2.5 seconds, then finish. But I'm realizing the preparation steps (login and collapsing panels) need to happen before recording starts, since Playwright's recordVideo captures from context creation and I can't start recording mid-session.

I'll handle this by recording everything including setup, then trimming the video in post-processing with ffmpeg to remove the first N seconds of preparation. For the cursor, I'll stick with the cyan cursor technique since it works well, but I need to account for the fact that node positions are dynamic with the viewport at 2743×1543, so I should locate nodes via locator rather than hardcoding coordinates.

I also need to make sure the built app loads the session properly by running the build first, then starting vite preview on port 4173 in the background. After capturing the screencast sample, I'll extract three QA frames and send the take to Sovereign as a library asset.

I'm going to start the build in the background now and write the screencast-v2.ts file.

</details>


## 🤖 Claude *(21:59:42)*

<details>
<summary>💭 Thinking Process</summary>

TypeScript compilation passed. Now I'll build and deploy the patch in the background while I work on the calibrated v2 screencast.

</details>


## 🤖 Claude *(21:59:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run build 2>&1 | tail -4",
  "description": "Build frontend (main repo = live deploy) with the panel patch",
  "run_in_background": true
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Command running in background with ID: bpxodz7z2. Output is being written to: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/bpxodz7z2.output. You will be notified when it completes. To check interim output, use Read on that file path.
> ```

## 🤖 Claude *(22:00:17)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/screencast-v2.ts",
  "content": "/**\n * EP05 screencast v2 \u2014 CALIBRATED per Sovereign direction 2026-08-03:\n *   \u2022 1920\u00d71080 output with browser at 70% zoom \u2192 viewport 2743\u00d71543 downscaled to 1920\u00d71080\n *   \u2022 everything collapsed: main menu, canvas library panel (Receitas/Tend\u00eancias/Hist\u00f3ricos),\n *     properties panel \u2014 full-width canvas\n *   \u2022 single-click node \u2192 RightPanel opens automatically (new behavior, this session's patch)\n *   \u2022 double-click node \u2192 NodeConfigWindow opens AND right panel hides (patch)\n *   \u2022 setup happens BEFORE the take: recording is trimmed to the action (no setup frames)\n *   \u2022 node targets located by real boundingBox \u2014 never blind coordinates\n *\n * Usage: bun run screencast-v2.ts sample   (calibration take for Sovereign review)\n */\nimport { chromium } from 'playwright';\nimport { createClient } from '@supabase/supabase-js';\nimport { execSync } from 'child_process';\n\nconst URL = process.env.SUPABASE_URL!;\nconst SVC = process.env.SB_SECRET_KEY!;\nconst ANON = (process.env.SB_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY)!;\nconst REF = URL.match(/https:\\/\\/([a-z0-9]+)\\.supabase/)![1];\nconst STORAGE_KEY = `sb-${REF}-auth-token`;\nconst APP = 'http://localhost:4173';\nconst EP05 = '18a21002-df9c-48b4-aff3-7aba28e812e7';\nconst OUT = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out';\nconst CHROME = '/home/ubuntu/.cache/ms-playwright/chromium-1226/chrome-linux/chrome';\n\n// 70% browser zoom on a 1920\u00d71080 screen = CSS viewport 2743\u00d71543 recorded at 1920\u00d71080.\nconst VW = 2743, VH = 1543;\n\nconst admin = createClient(URL, SVC, { auth: { persistSession: false } });\nconst anon = createClient(URL, ANON, { auth: { persistSession: false } });\nconst { data: link } = await admin.auth.admin.generateLink({ type: 'magiclink', email: 'gabrielcall@gmail.com' });\nlet session: unknown = null;\nfor (const type of ['magiclink', 'email'] as const) {\n  const { data: s } = await anon.auth.verifyOtp({ token_hash: link!.properties!.hashed_token, type });\n  if (s?.session?.access_token) { session = s.session; break; }\n}\nif (!session) { console.error('no session'); process.exit(1); }\nconsole.log('session ok');\n\nexecSync(`mkdir -p ${OUT}/raw`);\nconst browser = await chromium.launch({ headless: true, executablePath: CHROME });\nconst ctx = await browser.newContext({\n  viewport: { width: VW, height: VH },\n  recordVideo: { dir: `${OUT}/raw`, size: { width: 1920, height: 1080 } },\n  deviceScaleFactor: 1,\n});\nconst page = await ctx.newPage();\nawait page.addInitScript(([k, v]) => localStorage.setItem(k, v), [STORAGE_KEY, JSON.stringify(session)]);\n// animated cyan cursor (proven technique) \u2014 sized for the 70% zoom (26px CSS \u2248 18px physical)\nawait page.addInitScript(() => {\n  (window as any).__cx = 1371; (window as any).__cy = 771;\n  const ensure = () => {\n    let c = document.getElementById('__fakecur') as HTMLDivElement | null;\n    if (!c) { c = document.createElement('div'); c.id = '__fakecur';\n      c.style.cssText = 'position:fixed;width:34px;height:34px;border-radius:50%;background:rgba(56,189,248,.30);border:3px solid #38bdf8;box-shadow:0 0 20px #38bdf8,0 0 5px #fff;z-index:2147483647;pointer-events:none;left:0;top:0;transform:translate(-50%,-50%)';\n      (document.documentElement || document.body).appendChild(c); }\n    c.style.left = ((window as any).__cx) + 'px'; c.style.top = ((window as any).__cy) + 'px';\n  };\n  (window as any).__setCur = (x: number, y: number) => { (window as any).__cx = x; (window as any).__cy = y; ensure(); };\n  setInterval(ensure, 100);\n});\n\nconst t0 = Date.now();\nconst stamp = (m: string) => console.log(`[${((Date.now() - t0) / 1000).toFixed(1)}s] ${m}`);\n\nawait page.goto(`${APP}/dashboard/spaces/${EP05}`, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => stamp(`goto warn: ${e.message}`));\nawait page.waitForSelector('.react-flow__node', { timeout: 30000 });\nawait page.waitForTimeout(3000);\nstamp('canvas loaded');\n\n// \u2500\u2500 SETUP (before the take): collapse EVERYTHING \u2500\u2500\nconst clickIf = async (sel: string, name: string) => {\n  const loc = page.locator(sel).first();\n  if (await loc.count()) { await loc.click({ timeout: 4000 }).then(() => stamp(`collapsed: ${name}`)).catch(e => stamp(`${name} warn: ${e.message}`)); }\n  else stamp(`${name}: selector not found`);\n};\nawait clickIf('[data-sidebar=\"trigger\"]', 'main menu');\nawait page.waitForTimeout(400);\nawait clickIf('button[aria-label=\"Ocultar biblioteca\"]', 'library panel');\nawait page.waitForTimeout(400);\nawait clickIf('button[aria-label=\"Ocultar propriedades\"]', 'properties panel');\nawait page.waitForTimeout(800);\n\n// locate a rich presenter node by REAL bounding box\nconst node = page.locator('.react-flow__node').filter({ hasText: /Veo|POV|Apresentador|imageToVideo|V\u00eddeo/i }).first();\nconst target = (await node.count()) ? node : page.locator('.react-flow__node').first();\nconst box = await target.boundingBox();\nif (!box) { console.error('no node box'); process.exit(1); }\nconst nx = box.x + box.width / 2, ny = box.y + Math.min(box.height / 2, 80);\nstamp(`node target at ${Math.round(nx)},${Math.round(ny)}`);\n\n// park cursor center \u2014 take starts here\nawait page.evaluate(([x, y]) => (window as any).__setCur(x, y), [VW / 2, VH / 2]);\nawait page.waitForTimeout(500);\nconst TAKE_START = (Date.now() - t0) / 1000;\nstamp(`TAKE_START=${TAKE_START.toFixed(1)}`);\n\nlet cx = VW / 2, cy = VH / 2;\nconst move = async (x: number, y: number, steps = 40) => {\n  const sx = cx, sy = cy;\n  for (let i = 1; i <= steps; i++) {\n    const t = i / steps, e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;\n    const px = sx + (x - sx) * e, py = sy + (y - sy) * e;\n    await page.evaluate(([a, b]) => (window as any).__setCur(a, b), [px, py]);\n    await page.mouse.move(px, py); await page.waitForTimeout(16);\n  }\n  cx = x; cy = y;\n};\n\n// \u2500\u2500 THE TAKE \u2500\u2500\n// 1. glide to the node, single-click \u2192 RightPanel opens automatically\nawait move(nx, ny);\nawait page.waitForTimeout(400);\nawait target.click({ position: { x: box.width / 2, y: Math.min(box.height / 2, 80) } });\nstamp('single click \u2192 RightPanel should open');\nawait page.waitForTimeout(2200);\n\n// 2. glide over the opened panel (show it briefly)\nawait move(VW - 260, 500, 34); await page.waitForTimeout(900);\nawait move(VW - 260, 900, 30); await page.waitForTimeout(900);\n\n// 3. back to the node, double-click \u2192 config window opens AND panel yields\nconst box2 = await target.boundingBox();\nconst nx2 = box2 ? box2.x + box2.width / 2 : nx, ny2 = box2 ? box2.y + Math.min(box2.height / 2, 80) : ny;\nawait move(nx2, ny2);\nawait page.waitForTimeout(400);\nawait target.dblclick({ position: { x: (box2 ?? box).width / 2, y: Math.min((box2 ?? box).height / 2, 80) } });\nstamp('double click \u2192 modal + panel hidden');\nawait page.waitForTimeout(3000);\n\n// 4. glide inside the modal\nawait move(VW / 2, VH / 2 - 120, 30); await page.waitForTimeout(1200);\nconst TAKE_END = (Date.now() - t0) / 1000;\nstamp(`TAKE_END=${TAKE_END.toFixed(1)}`);\n\nawait ctx.close();\nawait browser.close();\n\nconst webm = execSync(`ls -t ${OUT}/raw/*.webm | head -1`).toString().trim();\n// trim the setup out \u2014 the delivered take starts at TAKE_START\nexecSync(`ffmpeg -y -ss ${TAKE_START.toFixed(2)} -i \"${webm}\" -c:v libx264 -pix_fmt yuv420p -r 30 ${OUT}/sample.mp4 -loglevel error`);\nfor (const t of [1, 4, 8, 12]) execSync(`ffmpeg -y -ss ${t} -i ${OUT}/sample.mp4 -frames:v 1 ${OUT}/sample_${t}.jpg -loglevel error`);\nconst dim = execSync(`ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 ${OUT}/sample.mp4`).toString().trim();\nconst dur = execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 ${OUT}/sample.mp4`).toString().trim();\nconsole.log(`\u2705 sample.mp4 ${dim} ${parseFloat(dur).toFixed(1)}s \u00b7 QA frames sample_{1,4,8,12}.jpg`);\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/screencast-v2.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:00:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/bpxodz7z2.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	- Using dynamic import() to code-split the application
> 2	- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> 3	- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> 4	✓ built in 28.63s
> 5	
> ```

## 🤖 Claude *(22:00:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/b2vvl9ihk.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	total: 406.6 s (film 393.0 + credits 13.63)
> 2	act offsets: [0.0, 47.8, 110.3, 189.2, 277.0, 349.0, 393.0]
> 3	Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
> 4	[00:00] ato 1 (bpm 78, D major)
> 5	[26.0] LIFT → cue 1 (joyful build)
> 6	[46.0] ato 2
> 7	[108.0] RESET ato 3 (bpm 100)
> 8	[188.0] ato 4
> 9	[274.0] ato 5
> 10	
> ```

## 🤖 Claude *(22:00:31)*

<details>
<summary>💭 Thinking Process</summary>

The build completed successfully in about 28 seconds with immediate nginx deployment to the dist folder. I'm verifying that the build actually materialized by checking the dist assets timestamp and confirming the environment variables are baked into the bundle, since I'm working in the main repo with the .env file present. I'll spot-check the assets directory listing and grep for the Supabase URL in the bundle to confirm everything deployed correctly.

Now I've got about 2 minutes while the token limit approaches, so I'm spinning up the Vite preview server on port 4173 for the screencast and running the build verification in parallel. Once the preview is running, I'll kick off the screencast recording.

</details>


## 🤖 Claude *(22:00:32)*

<details>
<summary>💭 Thinking Process</summary>

Build completed in 28.63 seconds. Now I'm verifying the deployment materials and uploading the preview for the screencast.

</details>


## 🤖 Claude *(22:00:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la dist/assets/*.js | head -3; echo \"---env-baked---\"; set -a && source .env && set +a && grep -c \"$(echo $VITE_SUPABASE_URL | sed 's|https://||;s|/.*||')\" dist/assets/index-*.js | head -1; date",
  "description": "Verify fresh chunk timestamp and env baked into bundle"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu    406 Aug  3 19:00 dist/assets/activity-CT0ABcZD.js
> -rw-rw-r-- 1 ubuntu ubuntu    437 Aug  3 19:00 dist/assets/addDays-YgzJzSiZ.js
> -rw-rw-r-- 1 ubuntu ubuntu  35087 Aug  3 19:00 dist/assets/AdminPage-DqV0m1hD.js
> ---env-baked---
> dist/assets/index-Bkige1o9.js:0
> Mon Aug  3 07:00:32 PM -03 2026
> ```

## 🤖 Claude *(22:00:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "(npx vite preview --port 4173 --strictPort >/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/preview.log 2>&1 &) && sleep 3 && curl -s -o /dev/null -w \"preview HTTP %{http_code}\\n\" http://localhost:4173/",
  "description": "Start vite preview on 4173 and probe it"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> preview HTTP 200
> ```

## 🤖 Claude *(22:00:45)*

<details>
<summary>💭 Thinking Process</summary>

Checking the dist/assets timestamp from today at 19:00 — looks fresh. Now I'm verifying the environment variables baked into the build by grepping for the Supabase URL, but the search returned zero matches, which is strange. I'm wondering if my grep command was off, or if the VITE_SUPABASE_URL variable is actually empty in the .env file.

If the variable is empty, a grep for an empty string would match everything, but it returned 0, so the string I'm searching for isn't empty — it's just not appearing in the index file. The Supabase client might be bundled into a separate chunk, so I should search the entire dist/assets directory to track it down.

</details>


## 🤖 Claude *(22:00:46)*

<details>
<summary>💭 Thinking Process</summary>

Chunk fresco and preview 200 are working, but the env-baked probe returned 0 in the index and the Supabase client might be in another chunk. Let me verify this properly.

</details>


## 🤖 Claude *(22:00:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && HOST=$(echo $VITE_SUPABASE_URL | sed 's|https://||;s|/.*||'); echo \"looking for: ${HOST:0:8}\u2026\"; grep -rl \"$HOST\" dist/assets/ | head -3; echo \"matches: $(grep -rl \\\"$HOST\\\" dist/assets/ | wc -l)\"",
  "description": "Search all chunks for baked Supabase host"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> looking for: bcyvddsy…
> dist/assets/YouTubeStudioPage-Dg4KD15r.js
> dist/assets/InboxPage-BoRL8cKa.js
> dist/assets/CampaignDetail-ulexENse.js
> matches: 0
> ```

## 🤖 Claude *(22:00:53)*

<details>
<summary>💭 Thinking Process</summary>

O grep encontrou os arquivos esperados com o host baked nos chunks — meu segundo comando tinha as aspas escapadas erradas, por isso retornou zero matches. Agora vou rodar a versão 2 do screencast.

</details>


## 🤖 Claude *(22:00:54)*

<details>
<summary>💭 Thinking Process</summary>

Environment is set up and verified, the host appears in the chunks correctly, and deployment is confirmed. Now running the calibration screencast.

</details>


## 🤖 Claude *(22:00:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/screencast-v2.ts sample 2>&1 | tail -25",
  "description": "Record calibrated screencast sample (70% zoom, collapsed, click behaviors)",
  "timeout": 240000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> session ok
> [7.1s] canvas loaded
> [7.2s] collapsed: main menu
> [7.9s] collapsed: library panel
> [8.3s] collapsed: properties panel
> [9.1s] node target at 590,287
> [9.6s] TAKE_START=9.6
> [13.6s] single click → RightPanel should open
> [26.7s] double click → modal + panel hidden
> [33.7s] TAKE_END=33.7
> ✅ sample.mp4 1920,1080 23.8s · QA frames sample_{1,4,8,12}.jpg
> ```

## 🤖 Claude *(22:01:47)*

<details>
<summary>💭 Thinking Process</summary>

Estou analisando o screencast de 1920×1080 com 23.8 segundos que mostra os colapsos e as duas interações, aplicando Vision QA nos frames com feedback contínuo para verificar o comportamento do canvas colapsado, o painel direito após cliques e o estado do modal com painel oculto nos samples selecionados.

</details>


## 🤖 Claude *(22:01:48)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking the video file which is 1920×1080 resolution and 23.8 seconds long, and will perform visual quality assurance on the frames before proceeding.

</details>


## 🤖 Claude *(22:01:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample_1.jpg"
}
```

## 🤖 Claude *(22:01:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample_4.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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Avhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUwzw2x6qAL4Z4bY9TDPDbHqoAvhnhtj1MM8NseqgC+GeG2PUw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', 'media_type': 'image/jpeg'}}]
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs+XrHWoAvuz5esdZuz5esdagC+7Pl6x1m7Pl6x1qAL7s+XrHWbs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jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUCURb9vL0jqN+3l6R1AlEW/by9I6jft5ekdQJRFv28vSOo37eXpHUglEW/by9I6jft5ekdQJRFv28vSOo37eXpHUo9DR1baN4vSZi1ZzEx3S/Q9D+tepWsRq6FdSfGt5p/Dds/LN+3l6R1LfUny9I6nejOry76M2fO1nUsjWrfloiq3CbzEx7YmJt5Xfrn7WV/uv+2/4R+1df7r/ALb/AIT8l+rPl6Q79W3l6R1O/i83tdUPm/JdS+l/XmfvfrX7V1/uv+2/4R+1df7r/tv+E/JPqz5ekdR9WfL0jqXxmb2uqD5LqX0v68z979b/AGrr/df9t/wj9q6/3X/bf8J+SfVt5ekdSTf1PCf5f0HjM3tdUHyXUvpf15n736v+1cf3X/bf8M/auP7r/tv+G/Jp1Lxz4dEdTtdSZmI4cZ8IZ8Xm9rqhPkupfS/rzP3v1f8AauP7r/tv+GftXX+6/wC2/wCE/Kt+fL0g358vSDxeb2uqF+S6l9L+vM/e/Vf2rr/df9t/wj9q6/3X/bf8J+Vb8+XpHUb8+XpHUeLze11QfJdS+l/Xmfvfqv7V1/uv+2/4R+1df7r/ALb/AIT8q358vSOo358vSOprxmb2uqD5LqX0v68z979V/auP7r/tv+E83a/6z6+tSaaWnGjmMTbe37dHCsR6Pzzft5ekdRvT5ekdTM61mzhpdUR7nWj+H1KiYmMqJtwvVXMbpqmJ9sLXtlCtvT5ekdRns9I6nju+7EWVF96fL0jqc3p8vSOpFVF96fL0jqN6fL0jqBQX3p8vSOo3p8vSOoFBbM+XpHUZn9YjqBUW3p8vSOo3p8vSOoFRbM/rEdRmf1iOoFRfeny9I6jeny9I6gUFsz5ekdRmfL0jqBVyeS+9Pl6Q5NpxPL0jqBlAQXAUB6+36Ghs+tamlfUndnE1vEcJxzi0cJieyJh5AO259EeyEaS3Poj2QjQHubNoW1tSmlpxm1pxGZxHbMzjl3vDfXfLL1ptmlNrRWM2jemcRGazEZnu58+QNFvlGvE1r9XZZtasWrWNem9aJjMbsZ45jlh8zqxE1z4P0mtfpX0d77PaIrsk21Pr7PP0/pV97diL70zPLhzjung/OdX4bfr3g8wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGvSr3vpdH5Zra0ac/U2ek6vwVvrUre0TMx8Oc4mY4PntH4enqfomy2i1dmmI0LRu7PFrX1tGn0p09e9rTu2tF8xE8MTETEznIPkNq2TU2W0VvuW3ozE0tW9ZjMxPGMxnMTEw8GIxqRH+aPa+v+Z4rOjTepaa11M7tq3iN7W1LRxrNo4xMcM8Hyc/2sfnQAthVIorhVL/BSQe59g0q7HTaNTaY076tb20tL6c2i8adt2YnUifdmZ5RuzHjMNc/INuidKN3T/eTaP7SvuTXTnUmNTwncjPg8+vzG0bNXZ7aOhfci9aal62m+nF5zO7725z5TNZmO6WufnOtOrXW+loRqRF960RqfvJvp/TmbZ1JiOE59yKxniCOnybar606MW0c7lLxb6ld28anCu5PO2Z8uHe8XU07aV7ad+FqTNbR4TE4n0e9ofOtfQx+70bxGnpaeLReP7GZmlvd1KTM5njEzuz3w8TX1rbRq6mraIi2pe15iOUTaZmcZzOOPDidPvwOhv23YqbLp7NemvGvGvS1sxSaRWa3msxG9ObRmOeK9jz9HQ1dotNdKltS0VtaYrxndrGbT2RHFv2rb/tWjo6X2fQ0o0ImKTp/V3sWmZmJ39W8YmZzyifN5UTMcswcvtFX1Op8k1Y+yRp6lb22jTtaYmIpGlaunGpNJtMznFJic8OeMPl44S+10v6wauprxfaoi9KzqWpWsTP09/Rtpxp0ibxjT4xmJmZ4cAeXX5LtM3tTe0IiKad9+dWsUtXVnFJrblOZ6Ycn5LtsaGprTSsV09/MTeN+Y07bt5ivfFbc0W0fNNXXrqU+npUpfT0tKK1i+KU0ZzWK71rTmZ4zvTKn+o6k7LGzW09K8Vi1aak7+/WL23piMXik8eW9WZjJ0nx8ehPPybao1dLR/dTqamfcjUrvVxXezeJxiN38UZjuzlNHyLbJ1b6edGu79Kd62rWK2+t8G7M85nw9YhJ/r20xGjFdPRrGjNpiP3sxbe09y1fe1bbtZjOY093nwYo+a6lZtNNLRpFr6F92N+YidCc142va3GfizaTv6ju601/lN9PY7bTbX0a2rq2050ZtG/mvOPzv8uOXHLs/I9sj6X9lMas2iLRqVmtZrTftvzyiIpxnGY82a3zO+pp6+nfS0b/W1p18zGpnT1J5zTGpEdF4tD0r/ANYNpvNZ+loRjUtqWjGrMXm+nOnaLZ1JxE1nlTdx3J0ei/pJ7/T0I7/IteNSKaepo3j6ejedSb1rp72t8FK2zMWmeUePkx/6TtX0ba0/TjdjUncnUr9TGlbF5inOd2eeO5qj55qxeZ+z7NNN3RrGlMau5X6Gfp2j97v5jM87TDytp23V2munXU3fcnUnMcJmdW29Oe7ny8lOj3PNAAAAAAcnk65PIGcBBd62xa+lozqfU3q71Yit66dNSaTFon4LzWOMcJ45eSKPQ23Xjadp1taK7sXvNor4RPLlw9HngDtufRHshGktz6I9kI0BsrqxjixgPR+rXxQX1N6MQygAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJqX3exq+rTzeeA3zrVjlxZazm8fnR7USSnxV7Y9oJV8qCiRWVQHo7ujbSrWu79XhmZtMZmZvmJm0xSOG7Me1b6WnGjidz6kzMRO/njmO/M6eMZzmebzAHoViKaetS1tPOK441tnExytXe7u7LA4AAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILtuhsupr5mJrWtZiLXvaK1rnPTPKeFYmZ7oYnu7HtGlp6cVvbdmuvp61c13q23ItG7OJie+FGXV2K+nSdSt9LWpHxW07fDxx71bxW9ePfNccY4vMfUbRtmjeNe0Xm9tTQroxG7bu1KW3rXtaZmfdx6Plwdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKfFXthGkp8Ve2AaN635U+sm9b8qfWVXeSju9bxn1N63jPq9jU+XbVS1a1rTWtau9NdKN+1OXC8buYn3o8p7pQfYdtncxs2r78Zr+6n3oiM5j3fCYnpEedvW8Z9Tet4z6vQ+x7Zis/Z9TFp3Yn6U8ZzMY+HymOiUk/L9t+nGr9C+7OpOlHucd+Me7jGe/7hXl71vyp9Tet+VPqk1KX0rTTUpNLRzrNd20fwjmhBfet4z6m9bxn1TaehfUvFPgmeW9FsfwrM9OMY5ytbZ710/qe7MeU8cZmInjHfjxz4wDPv28Z9Tft4z6rV0tS1ZtWlprHfEcF/s+tnH075xnG7IId63jPqb1vGfVQBfet4z6m9bxn1UAX3reM+pvW8Z9VAF963jPqb1vGfVQBfet4z6m9bxn1UAX3reM+pvW8Z9VAF963jPqb1vGfVQBfet+VLk2tieM+qrk8gZwEFwbNDZ77RNt3diKxvWvad2lY8bTPDsiMzM8oUYx6l9h1a6FtojcvpVv9PfrPDexnlbFunGMvLB23Poj2QjSW59EeyEaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKtPFVea2rETMTEW4xMxzjy6fBR9bHz/AG+s0xWsbunOn7v165iZrM2zXViYnNY4VmKzx93ippfPdt0pjdpThWK/+7EzEaddP4qakWjhWJ4TE58uD5TE4z3Zx0qg+ir822uurpauIm2nW8Rn6vvb9r23rTF4tvRN5xaJiY8V/wDV9q+p9X6env8A2idorONXNbzERbGL8rREROcz4TD5oBu2rX1Nq1r62rmLXmM5m9uUY+LUte89MzLFItNZjGYxmMx2A002jUraJt+9xyi83mImZzmMWiY6Ola+131NPcmKc/ijOZ4zOOeOEz3RE+MsIDbp7VfSp9OsVxm08c596MeMdHBN9stvzf6elm3xR7+Jtvb29Pv5zmPKPJ5ieulqWiJrWZzMxGOMzjniOeI78RiARTOZmfFVaa2id2azFs4xjjlN9DVi8Umlq2nlFvd9uOoVnE8aOrblp3nsrM92fDw4osTMTPdyz5iKgnro6l4ia1m29mIxxmcc+EceGeeMAgHcTE4mMTHi7ETbhETM8Z4eXMFQAAAAAHJ5OuSDOAgu+l+XTpzo6kXmkTp6ulr7tpiI1opF/wB3xnvzGOE8Z5YfNCj7DbdXGnr2tEUnXpp0rpb1LXmaWi062pGnilbe7uxwieL48Adtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAJN1G9/T+X2tpaepOro0jU+GL2mJ4TMccVn2g8+uya16xaune0TnExWZ5c+WT7FtH/J1v6O3U+jvse1bL+5na9LTi1Y936l4ricz+TjEzM+rTq6HzDQxN9t06TaOH7y+Zjx4UnmD5G+y62nE2tp6lYjhMzS0RHb5s+4+y2rZ9stWK6+2aO7qYmKzeYrPniK4iOOe5HHyHap/Ho/zT/hB8luebm4+v/Z/a/wArS/mn/Ct+z21/laX81v8ACXHyG4hmMPuP9B27GN/Sx+dbx/MfIbTpW0Na+nbGaWms45ZgGUAAAAAAAAAAAAABrrp1isTaZ97jERHdnDI9C/Gml+Z/8rLDE7I5Z9Dk6VIiJmNWInlOIxOOePHDkaVJibfvcRjM4jEZ5Znz7n1exbP80toUnQtStJ5f2cTPGeea5755zyXv8r+Z631LW+ladWazac6fHd5co4dGM95uNHzl8lGnpzEz+8xHOcRiO1Xc0vHU9IfYbPsPzTZJt9L6Ub/PM0numM/xnHd5Jb7H831afTvbTvXwt9Oe+ZzmazPOZL8y6PnO98dXRpfO7GpOOzrX+z1zjd1M9kdb6PT+UfMNLOI0+PjeGmPl3zSvGN2M4zMakRnDcTT8Q89X5b/baY2XnofHTp6dZxP1PSvWr9PSnhE3jPjEY/g+nv8AJvmGrbetGnM/nw+c1dK2lqWpbG9S01nthnB2imbYzN+e/oYbVmszE84nHoo0a/8Aban59vazo1E3iOaABGgAAAAAAAAAAAHYSxSZmIjMzPCIiOaOvNrrNqWi1ZxNZzHbCiGabszE5iY7pjEn05xnjjOM44Z7Xu3+abbfjOt6VrEcbb3KKxnj1O6nzXbdWlqW1I3bR70blfezGPyc9/cg8KdK0REzFoie+Y4SW07UxvRNcxExmMZie+Puer9u2n6f0/qe5u7m7u1xu4x+T4R2sN721JibTHCsVjERHCvCOUR6zxUZd3zNzz/X1TYMAh3P1/WVZrhp4+KK0cEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEr2PttYrStabs0ratbRM596sRM8ZnvjMYw8d6MbFebadYtp72pEYrvcYzXeiJ8M+me9oTxtdM5mL/20ata8MRjOY59/fw7kk7bp2taZpbNq7vPnE73CfWPRk+x3mIxfT423YjM5n3t3MRMROM9KkbNM53bVtETEZ97vrae+sT+Ge4+PdAj0dStJtvROLVxOMZ5xPf2PTtt1LVrWdOcRaZxmPy971jkx12X34rNqzwzbjMbvCOczSccZ7s8UepsttOs2m1eE/Dxz8U1zyxjMeOe8RTX1I1b70Z5VjjzmYjGe/n2y9Ku20paLY1LT9KNOZnhM47+cz5dDzdPQnUpa+9SsR3WnEzOM8PFJtGzW2eYi01tnPw57seMR4orZG1ac7kYmvvxPHjFfizMcJnvieEdy+ttdM3rWbXzu+9+XilY4xaI74zGYzx8XnX2e1NGmrifenw93y4988J+80tKt6XmZtEx34jdjwjzmeWOAJdq2mNoms7sxjPPoKa9IrpZzmldSk4jnF97jGZ58e/u717bLFdWaTbeid+KzHdNM84mI8OLywe19tpi0btuM5xmMT8GJn/NG7w582e2072/aYxO7aunERwjftm0885xM+rzQV687XFp0Zmv9lNeWOMRWsT3c8xw7+6Uelr004iv7y0V1a3rExGPdnj3zz75iO55gI+h0ds053pvbdncxM8ZnU+ON3hE91o5z3MNdelb1xvbtdPcxivGZ42zE5iYmc8MxOMcXmAPajbNONyIpOK33tzMTGN+bducTu9C0bdWPqcLzNoxnhm2aTX3uzOY45eGA92durX4a2icTETnlG9Sd3xxG7MdKn2zTjc920RS2dz3d3nad6O/exPdw4cZeKA0aup9TUm/GeXPvxHfj+PHPjOUd7734a1/NjH3yjAAAHJdckGcBBNWMzh6Wlo21J3dOk2nwiMsFPifS7H/Y68UibX9yd2uJmaRFs8Jic1i27Mxjj0O1EXl4tYrmiJmOOEY8MZiLz5Rd5mps+ppYm+nNYnlMxwnsnlOO15l64l9XqWrpbNfT1b1tqaldKYrG9O78M1tOYrWs1pmPdzPvcXzGr3dK1xEfHDyY1fMqrveNtonGIqi0TeL7NkTtZ7c+iPZCNJbn0R7IRuD6AAAAAAAAAAAAAAAAA/Y/l06NPksTf6ebVmJ3q1md36k8Y3pieGZ5Pxx9RtERbY9gj/Jf+OpLFcXw5ZdKJtjxwfpu0zoU2Caa304iaRxxXNuERwmZzw7Euhp7DobNMTak6ltHTiN+ItM6dY4bsTMR2473g6ujTatbZtmtiaaNfqWz5TMVr448UvzX6dY2eaxWdy29X/p4/wAeTzzbheccXoiZi02jDDnYfmuxU1NLSnfmt4pWNyKWn/dzEceHHg8vbNs2nZde9KWvFaxWI93NfhrM48ePS+++1aerp1mOVqxPr+vF6FdTZ9TZKx7tpjezGPOcQunMbNrMZelttg+B+X/PI2jUro61Yi1uFbxwiZ84nlnxy+o2ratPY9GdW/ZERzmZ7n5ntWw309adSmeF88O7j3Yy+/8AmGw6m3fQ04mcb8zbHZz8Ha+1w0ZvZ8jrfOdp1ZzSZrX/AC05dPHj2Yh8btF7amre9pzNpzM9r+m9l2bZ9h2KtdSKV3Y+K0cZ78zzl/OXzWazt20zXG79W2McsZZor0pmOTa6V0aMRPLseOA7OAAAAAAAAAAAAA9K3waX5n/zs816Vvg0vzP/AJWbja5zxp559L9M+WbBq/Mdk2bSrrToU3dS2pbn+PEV4zHPzT6Ow63yzbvo/X+tp3rbhjG7McYnGZiHq/1etT/T9Kl6xbezjM4zO/M9yDdjU262aRp2rbUvPGc2rnEcO2f4PJedOz2aNP47oNo/q/bXrbabbXuzaZmlMRmKx55z6PI+Wa+1UptOnq51J0q71JnjM8+GfDg/Qq0i1Zn6deFcRM54TnjPT4M2z6WlpzOZiZzx5T68eEPXl5WZVM4Xh4c3PyqLRMxE255nzs+U/wBB2raNmjadfaZpqznFJrwjpi0fw5Ka99bQ+XUzeZvwra8c+c8fSMeL9C2mdO+nW/0/q7kWnHR+vHi+apGlpbLT60RTTivvxMTOIn7+Ljo10zOlE4bHeK8uuKdGYty3u/K9j2nV0tr0ora3valazGZmLRaccc5ZNu/8XtP/AHtT/fl9TTR2LV2/Trs+pPG29mYtHw8cRmI8Hy+3x/6zaf8Avan+9LUTdZjzeTr/ANtqfn29rM06/wDban59vazNbfa5Ufpjmj3ACNgAAAAAAAAAAAJaRmW6ule/Gtc8cPPrzhqUTfSvMzG7OY4zwcjS1Jzitpxz4IwEk6Wp+TPofTviJ3ZxPficIwEsaV7cqzPHHTHc5OneOdZjo5onQSRpak5xW044TwZ7xwXRX5AzgIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEqf6upwjfvwjEe9PCO+EDuFEs62rMY378974p5+Pb5rfX1p3p+pf3oxb3p4xHdPHjCHHnHqY849QaJ2nWnd9+0bld2JiZicev6wjtq6lq7s3tMZziZnGfHjOEe75x6m75x6gtF71iaxaYi3OInhPbicFtS9/ita3bMz6ZlXd849Td849QItMcImY4xPTHKejuS/W1cWjfvi05tG9OLTPfPj0ot3zj1N3zj1BN9fVmZmb2tON3NuM4nnETOZjPfjCKbWxETM4jOIzwjPPH3ubvnHqbvnHqCotu+cepu+ceoKi275x6m75x6gqLbvnHqbvnHqCotu+cepu+ceoKi275x6m75x6gqLbvnHqbvnHqCotu+cepu+ceoKuStjCsgzgIJaziW2upETmJxPphgd4tXYqp0noW1N6Zm1ptM85mczLHe29Kipe6U0xHB23Poj2QjSW59EeyEbLoAAAAAAAAAAAAAAAAPpNW+NH5f/AJYt/wDqPm33+zfItq+Y7Ls2rp6mlWsUnEWm2c79vCspKw9PYb2mNfUnnwr6Rnj68EO3zM6Wz+XD+GOp7Wx/K9esatY1NG3v8fjjHuxH4qRw4cJ5eB8w+XaldKLXvp0rEx70/UmI7cUnEduIcLTd6NKLWebpW+nsun+bP8Zl9Z8ttssbBW813taN/PL8qcZ4+jza/Kdp+jSm9pTiOcWt/D3GXX2iNg2eNltbRpau9vTvWzOeXDdzwzz8WKqKpjhtdKa6Yn2JNntXU15i0xmfw4547+XdGe+OL7TZLUred6YjPfPlxxHhMvzTZqatb02r62hGjXM2960TbMYxndx0PYt8wnafc2PW066sTFonjMYjn+Hwbij7ZjbPxDnOZ90Tyeni/Qtv09DU0P3sTbjEViO+Znhz5P5v+bxWPmG1RWMRGraIjpfrFPnlczo7XbZ7WieO7a27nstSY/i/I/mVo1Nt2i8YxbUtMTHKePczlUzTe7ebXFURbGbvIFsT4G7PhPo9Txqi+7bwn0N23gCgvuz5esG75x69QKCTEflekdeHPd85/h1goJM18P4/oMx+TH8esEYvveUehvT5ekAoJN6fFzft4go9G3waX5n/AMrMO/bxlttiK6c+Ncz25mPuahieNPP6H2mrNo+TbLuWms78zwmYnhN+WEXyWutbaZ1N+0zuzmZnOYzHBBr3/wD9TssZ5Xn/AOTb8k1IpOreefuRHTlmjbPnPvWvZzR7n2/zbWvSlNHS4X1JxmOe7347+fetseyxs1cc5/HP5Vv0dzuvSutrU2iJ3orE1x/mzwmezi7G0RMzEdz6GdOMRstFvbHxd8rV4iYmqeM1TfnifRHBnpqTpbTuc9O84mvdW3dMeU8p7s8Xv6laxnL5fRzq7Vnupi0z2coT6m279eE8azMT0T97GbecmL8bzEc2HVGx0ysNYnR4WiZjZfHrmOLVq0rNovHCazwnw9X43tszO17R56t/96X6TfasZmZ4co/jl+X7RbOvqz43tP8AF8yjjL7VfCGLW46t5/zT7WdPqxjUvHhaY9JQO7zU8I5oAEaAAAAAAAAAAAAWrzbaxSY43tE+G7n/AOUexgWzPio123Yxu2mfHMY4+so0GZ8ZMz4yCcQZnxkzPjIJ3WfM+MmZ8ZB6U10Yz+8tPH8jET49+f4MepjunMd08s9HFDmfGXMkyzEW2zPPb0RDgCNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEqSeE46Ea9+c9sqKj3r6+nqX04ves0rTHPW933Y5xaLV7NyMM+/ozp0pM0iK6ts+5O9NJxic4nhwnOZ5dwPJHub+zU+pNZr8MxHu2nMzpzHu+7ER73POGLaZ0Z3fpbvfyi0YjuicxGZjjmY4SKwACAAAAAAAAAAAAA9TYtWula+dT6U2pit8WndnerP4YmeNYmOHjiW6l9i3aTfdtO9m2aXzPvXzM493dmN2IiJmcjz1VzTP6KptbhEzsvyW8uL50e9bU2WaWmm5W+Kz8Opz+nHwYxFZi+czMxGOWVvqbPq6u/q6kW3qaWZtGpMxam5vRbFeM2iJxxmOwPyzx0Kt032bN+54GHHv1ts000d69OF9WZpu6vCLVjcm2K4nExxxMz2r62rsupXVnNJtjEe7eJmdykRNZxiIiYtnOJwH5ZvEaFWN8bTy2eBHH0lFKWv3T7EUj0M4CC76DZtTW0tjvbQnUredekZ08701+neccO7Pc+fbdPatfS076VNS1K3mJtFeGcZxx596j2q6u16uz7ZG0W1rVjRrNfqb2Iv9fSxje78Z88ZfMJ7aupfha97R5zMoAdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAP6K/q7WP9K2bst/v2fzq/ov+r04+UbPwzO5fEePv2Fadj2idTWvmIxqXnd4ca0rvYzPfnEzHhE4ejtkfu93exvcJjETvV746fF898vnf2rTrNZia0zaY5ZrGPbL0vm+pOlWtorMzi2O3g8/+k8+D0f7xzY7nr6MRfTpaIxE1h+dX2Omp811de0UvvTMVrf4Y3cR5+D9F2SJjZ9GLZifp1zHnh8Pr6Olpb869509y9/eiYjGbZjj5x3OlWMMUWirF5/zbZI1tKtKRXRpOrW14pE4iJ4TOOHe9PYdj0Nl2aNyunM5n95j38+UxE8EOhtux7TqTpU1Z1OHhxn7mnaNXQ2WLakzalccczw9M97Npw8uK3pjS8725mTb9l0dbZpp9LSrP5cR+8m1uPOY8OcvybUrOhtWppZ4VtNX6lp7Tsm12ruatpmv4eUenk/LvmU42/aJj/m29rVN4vdK5iYptyYobTnMTmJjwZJtevflp1uExb9cIp/X9fPudHFDveMR7Pvw57vnH8epWYwqC+74cVXF8yCgk4T5KzGAVAAAAAAbdSfd0vzP/lZia9Tlo/8Ab/8AlZqPjexPGnnn3PY2i1qbHpadoxMWz0TlzZNf6dJjxtE9FYYLaevakRMTPHxjrcpo60fh/jHWzGF+ducdz9G+W/Md2tt/jW0zPbmXu1vsl97UjeiO/jw9n3vy3T+tWuN3+MdaeuptFc846Y63qpzZiLTaeS8RNuZ4a9Xiqbxemds0zMX57cX2e2fM9PTidPRjdieM48fOeb57T18RqTnnPteFqRrWnO7/ABjrciNfGMT6x1uWZXNbtlZUZfCPTM+czOMy9PV2nNefdL5nUmd+c+LZbT1p/D/GGDUretvfjEy4RD1TPA1/7XU/Pt7Wdp1/7XU/Pt7WZrl53Kj9Mc0e4AGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJT4q9sI0lPir2wCVJbnPbKNJbnPbKii+7bEWxOPHuS6l6W3YpXdiIjnxmZnnMzEekdz09Pa9Kulp6dqTO7Nd7vi0Re1pjE2x3xjhmeOZHKqqqIi1MzjjG2IeItETOcRM4547nrfX0J+tmlfeiN3d061xMR3cbRWM88cZ5rfaNni/uxaK2rqxbFaxMfUriIxFsTFZ8ceQmnV2J+Iu8bBh68bTpTp6NLRmNO1s/u9PjE8uPCZ4/FWZ6U/2rZojV3abu/mOGnTvrWJ4707sb0W4RnORJrq7E7ebjbk28XgD0Nq1NLVtWdOu7wnPuVp+KZiMVmY4RwzznvelTV2amhpTatJnMe7uUtb4LxNpmLb0xNprO7bHhCLNcxETozN9m1867jPJ619o0pjEadON7TbGnWJ3ZimN3jaYxMTOInEZ8G6m2bJTUreKYxu8Y0qd17TwibYid2Y97xhWZzKoj9EzxfND09fV0b6VK0ri0Y47la/hxb3o43zPvZnl3Mm/WKbv06TP5eb59N/d/gOkVXjhPHhhv2M7sxh6Oy6mhpxf6td7e4fDFoxiY5zMTE5xiYbtXa9C2LRTNopNczp05/TrWM5md7ExM5njESMzXVpW0Jnz2Pnx6ttbQnQtXciNS05zFYjE72ZxaJzu7vKuJ4u6F9Gmhff3ZtNsRG5W043LYxMzmvHE8OIac2n7Zwm1uXz5nkj3bbTs0R+7pGYrMRNtOnjSYznMTPC0b2I58mW+ro20N2KYvmLZ3axjjbPvROd3jERGOARXV2Ji826XmADsAAAAvX7p9iKe/sS1+6fYinv7AZwEFwfU/KNn0tT6mrqVrfcmsRW3L4b2mcTEx+HEZiYiMzMThofLD7r5ns+hfR1dWlNOltPHvae7u240iY9ylKzn6kY93MTW0ce74VB23Poj2QjSW59EeyEaAAAAAAAAAAAAAAAAA/on+rloj5TsvZf/AH7P52fq/wAq/rDs2x7Bp6E6OvOpp1tm9a1tWubZzibR447hX2uw/u9v1q+G/wC2Jev8yrGps1p/JmJ+5+UbH/WCujtWrq61dW8WzPCsRaMzHP3orEPS2/8ArJ9piulsujr15b8WrE5zjHCMz3xjFozlmIws3pYx7H6pW8TWs+MRP8H518+2Wdsma727WurE3nuxu448Y73dH+texxSIts+0zNKxvTEVxGOGZ97h4PJ1P6x7Jq21Jtp6+LzMxERXoz7x/qzHF9Jsez6Ohs1Ipp6XLheK+/nv4xH38WDb9ONXR1aT+KMPBr8+2PTmdzT14iecTNcR/wDZS/z7ZdTMW0tXE93u/wCJmmJtN3SqaZqw4PO2PYNbR2zTjFt2Pe3u7GP1h8z8y/8AG7R/3LP0j9otkppRo30NoravjWsT/Gc4fmO2asa+0aupETEXtNoifNab7WKrbF7e9SPOP48/uZY4x/Dqa6z+6ifDj6SxY42jt/g2wc+n+E/pRJuf/VH8VJ4xnontBGAAtE4VASYieXp1IxJnPPn49YIx2Yw4AAA2alc10vzP/lZjejp60RFfemlqxu5xmJiZmWoYnjTPn6JYt2Tdl6VtfejE6vl8GFfqxjH1eHD8Hh0FvjA0vKfVq7mGKT4+3qW3J/Kj+PU1/UrnP1e+Z+Dx5uWvW/PV/wDp1YLfGC6Uefq1dzHNJ8fb1G55x/Hqa5mkxETqTw5e5Kn7v/mf/WUt59cJpR5+rV3IPpz4+3qU3Jb41IiJrGrMRMYn3ece122rFvi1N6IxOIrjl6eK2+MDSjkn1Z7mTX/tdT863tZkt7b9rW8ZmfVEkrThTEeUACNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEqS3xT2yjSW5z2qPRpsc/U063tWI1J93jPHhEx+C3PPDPfzR02S+pStotX3rbuOOYn/NwmIzjhx4s8a+tWazGpeJrGKzFrRMR4ROeEH1tX/mX573xT8Xjz55HC2Z2o+L7GmNjvMWnNeFd7nzjd3sR54SfZqfWikTwnTjUjenjOdOLYzFJ5ecREwx/aNad795qTvfF708eGOPHjw4ce4jaNasxMal43YxGLTGI8I48vILZmOMcJj3Y8E1dlm1dO0Xp+8tMRWd6JjHO0+7jdjvmJlbU2O2lEza+nw4Rxn3sVrbhiMcrRjMxmeDP9o1vd/e6nuzmvvTwnjy9UdtS+p8VrW7+MzPHERn0iOiBbV3xmLY8/HDYjw4va1rcZmZ4RHHjwjlHR3KDsAAAAAAAAAAAAAAAAvXn0T7EU9/Ykr90+xHPf2AzgILvQ2Xa9XZLb2nic4zWc4nHLliYmJ5TWYmO6Xnij2ds+Za+2Ri27WuYma1m85xyzN73tOMziM4jOYh4wA7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAers2traEzfSxE4jMzWtse9ExjeieOYjjzeUli+IB9Hf5j8w+pWb3mbYjEbtZjnExisRjPCMcGamvtmnedSImLW3a5mke9jG7HGuOcRPm8f6mZzmZl36k+M+s9YPU0tbatnvNtOs6c8JnFOHu8fxRPbPi2R8x+YVj47cfezNKzzxPOa+UYju7nz/1Jnvt+vSfUnxn1UfRR8427TzXfrnERxpTNeER3REcoiOOfV5uptu0av1N6+fqxSL+7XjuT7vd3eXS87fz4ub0A9TaNv2jaoiNW1b7vL3KxMZxnjERPc8i3NfehFKD0dHjpzHnPsZL8JifGIlo2f8XQg1I/hMx/EFZ748Jyd/53t/X+Dsc484x9yndPlxBGJLePj7UYAAAAJInun/8ACsxhVeJ7pBQWmMKgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKfFXthGkp8Ve2ASrZVFF8x4T6mY8J9Y6lAF818J9f0Ga+E+sdSgC+a+E+v6DNfCfX9CgC2a+E+v6Hc18J9f0KAL5r4T6/oM18J9f0KAL5r4T6/oM18J9f0KAL5r4T6/oM18J9f0KALZr4T6/oM18J9f0KgL5r4T6/oM18J9f0KALZr4T6/oM18J9f0KgLZr4T6/oM18J9f0KgLZr4T6/oM18J9f0KgLTKk9/Y65IM4CC73vluxxtE6mpqV3tPSrMzG9u5t+GvCJt5zuxnEPBe/sHzGmx01KX0frVvMTjf3O7HH3bZjyUb9t+X6MaWpfTj6VtGZ3q51LRav7qN6J1IraJidSImJjExyl8i+o2n5ppa2lq6ens30p1OFp+pFo56UzisadIzP0o4+cvlwdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAA3bPzt2K6v4u2J9Yc2f4p7EmpHGfzc+kgy/h7J/X2HK3b97leU9nsJ5R6AeMdKNLM8Yn9fNSYxIKgAAAAAvE90uTGFUkT3T/APgEY7MYcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASU+KvbCNJT4q9sAlAUAAAAAAAAAAAAAAAAAAAAAAAAHPHsdc8ewGcBBcHvfL9gptkX39W2ni1a13dP6mc1vaeG/SeFaTwjMz3Qo8EfTbT8spoaeraLa9bacVtu6ulWsWra8U3omupbGJnjWYzHKXzIO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAaNH446fY13+KPOLQx6Xxw26nOs/5vaDzq849PV3umOlWeEz5Sk/FPnn+IKc47PvJ4xE/rwK+2COUx0goAAAAAAACSJzwlSYw4k58J6J+4EY64AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOePY6549gM4CC71Nl2munW2nqRP07zFs1+Ol6xO7evLOMzFq5jMS8sUfTbZ8y076U7NsunOlpT8U2xN74nMZ7ojlmY96cRmXzIA7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAAAAAAAAAABLp/HXthv1vh6YedT4o7YelrR7lugHn3jFp7SecT5QtqfF2xCOeUdIHwz2Stys5bnnxiHJ7p8vYCvJxe3PPioAAAAAAAACXnz5936UbiX4ufPxBEO8nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBd6WybJO1Xmu/TTrGN615xEZnERHnM8uUebzXr7HNZ09ek2pE2rTd3rVrndtx960TXz4qJNs+XW2Wkan1NPUrMxExWY3qTbexFoibRxiszGJl4j6fbNSn2WaZpvTqaOKxqaOpmKU1omf3NKREe9XG9mfN8wDtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAHYexfjW3ZLxns846AeXflWfJz8M+Uwtb4K9Kkcp7AJ5R0n4eyT8PSV7+wHe7sRrx39nsUAAAAAAATVQtVeQPR0dLZb6edXaJ0r708Ny181jdxwiIjvtOd7u5Oamls1JvFdf6sRSJrbdtTN5njXExblHjMQxHoo06NdG299W9q8I3ZiM8e/h348Mw1auz7HXT3qbXv33c7n0bxx4e7nemO+ePl5vM9D0Qe1Gz7BakTba507d8bltSJ4V/J3YjnOexFpaGxWvqVvtU1iNz6epGnbE5+LNIzbhyjjDyv15H68lE2tp6enb93qxq18d21Zjh3xPDyjEznmmrp6M7ubYzz8Y59ntYwZmJnbMczmtFYtO7OY7vHp4z7WNrvyZEXhAAKLQqtXnAN2hXTteI1LTSuJ4+eJxyiec4b9TQ2SlZmm1/UtExG79K9MxM897Nojhx5KbDp11Nq0aXiLVteImJ74fWbRqfK9DUtT7JW+5OLTxjj4Rz+4HxV66casxW8zp72Inv3c8+MRPDsiWydLY/qXxtNt2Jnc/d2mbREcMz7uJn82YjvfeTs/yydl+010KTTGeU5znGJ4+LwqbT8r3ojU2WNOJ7+Mx90+mS4+X19PRridLU3o45id7e5zx+CtcTGJ5tEaehu53pmcfx/8Aw++2jZvlezacal9GmLfDjPvdnF5ezanyzaNaul9krWbTiJzM8fPjE8WoqiNl3OqmauFUxzPl7aWzRScalt782Ij13pnpx0PK4P0bbK/LdituzstdS2MzEcIiPOZl5+0RsGvsGtq6GjFL0mkT413rx5zzgmq+yyU0zT/tNXPbDc+Fugab8mZl1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBcBQHpTsWvGlbVmsRWta2nN67+7aYiJ3M7+JzGJmOMPNB23Poj2QjSW59EeyEaAAAAAAAAAAAAAAAAAAAAAAAAAAA9mPhr2fc8Z7FPhr2QDzp+DstKlefbmE1uWpHhbLPHOO0Fo7+xyvOCPix2wqC0cJVWtz/AIluefHiCgAAAAADTTl+vizNNOX6+IJAAdAAHXVFRYERX+GWRttGYY8IOACi0c4VWjnAPf8Alv8A43Z/+5X2v3m1PsuxzWNDTvExvb02rE2ve+J55nv5y/Bvlv8A43Z/+5X2v0D5j880NL6+y6mle1qzXdmJ5xiJ6MTOM83DMiZs9GVVFMzM8nF6/wAqpWsbk6eYrrWzThux3z48I9sO/PdCNs06b9Kae/MTWKzEzMd2MY7mT5RtVdo2Ws4iLRvTavbaeOezn59z5v5j8z1dbaZ2XR0Zi1bbtY3sznx5V/RDFVNV4tsh0prpiKonbPDlh9psHyqmrOyzqzvfZqxER3Tb3ePRhr+Y1tOvo3nQrX99uRMWrmMVzmd2O95+rtW1bPoU1tGtZ1K/HS2fe4cYrPj4Sw7Httfm+pXV+lbT+jNsxacxN7eHDjjv6EtM1RjePcRNNNExa0zf2vF+c/L9W9761I36zjMRzrMRHc+e0NO1Ng27ezmfofw1H6btWltepExpa9dGkxxj6cXtM9svldq0rbP8s2nT1LRa83pbeiu7vRN693k6xVN+NPFymnCJtPB+a35MzTfkzO7gAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAgu+q+Sz9K2vrzGljSpHxzjjneiInerje3d2cZmc4xxfKij6j5praNc6ez6s6n1bTqa15tFpvbM7kTNcVxEcd2I4TPGfD5cAdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAPX0+NK9jyHqaX9nHT7QZ7c9T1ZG23x386sIJJ4Wz55VtGJl23d2QW5+nsAnlHY7PKPQ/D2S5HKeiQUAAAAAAaacmZppyBNgxPhKbSboh0im7E1WeU6+/wBq+V0076Gnpzm+pMVtnhG/iJ3Y7Mx6vAvo1i1oxynHIiLxdap0XhRGUm7hJjczbEYzNenqw5r23t33dyJjPDPHjMc+eOGO1OAhzEkwgbLxuxXExOa54Ty8pTiMl/hll3paLcpZEVfPlH69J7vhPr+hQRUnu+fp+l2IrnnPp/8AlEtHOAfQfLf/ABuz/wDcr7Wn5vNbbbr54Yt68O15ew23dq0Z8Lwl+ZX39r1Z8Zj/AHYYnj7G9nt9D9D+XWrsuxxeeGNPe6Of8M4ZvlGn9a+rtl497VtMUme7xn/4w8LX2qY2a2lH5Gnp+uM/we1pbRGjs9a1n4a4iY8u/p5uU3tzy6x6H1W1akV0LRHY+V+V7TGz7ROnypr5mI7o1I5/zR/GFdXat7Zuf4HyX1pruWieNZraOhKYs1XN37BqbRXMxl8r851Ytsepjv3f9+GSdpmd2Zn4ojreJ8w2nf0pr3T7KzXDMR90c7VVWHsfK2xhlT25IHreMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASU+KvbCNJT4q9sAlAUAAAAAAAAAAAAAAAAAAAAAAAAHJ5S65PKQZwEF0+lo6uvMxpaepqTHHFK2tP8ACJQPuv6v7v0tuzvf2cfDjf8A7LWzu571HyGpsu0aMROpo6unE8M3pasfxiGR+jbTFP8AQ7Y+tH72MfXxv536+EcvB+cg7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAAAAAAAAAAAeno/2fq8x6Wj8HTIKW/te2Otgb7/AB0nyYp5z2g7PKOz73Z5R2H4Y7Zc/DHbIEd/YV+4rz7eDkTiYBUWmMSqAAAAA26ePdzxjPHu4fxx6MTVTlCj0Imk3tNKzSvdWZ3pjtnFc+kNNZ4vOrOMvartezUrSPs8WtHxWm1/e6OUfxdYnBymH2O27ZOtXYNqxPu5mfz64z3d+7wfLXtvWmfHiln5rp30vpX2fMVzOnETMRFp5zzjMdbx52nn7nPz/wDylMxTg1Vjjze5BqbkzEb08bTvV6efh/Bt2zU0dWmnGln93G7x5488cOfF5PG1u2VZ4cGZktwVTVtHKUAw07qcpYmy85qxigAC0c1Vo5wDbs16V1Ym8TPhie/PBHr33tW0+PUj07Ur8VZt4Ytj7pTTqaMz/ZW/pP8Ayoqb6k2mMzznL0ra/CIicREPH+po/wDKt/Sf+Vf62l/yrf0n/lZs1d7ertGnNIjTzynhPOOHp44eLW8ccn1tHH9lP8//AJUf1dH/AJU/0n/lWxd7F9ozynhGP4PP1NXei0TPcj+to/8AKt/Sf+VHOpoz/wC1b+k/8qWS7LlR3xcbZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBdo0tbV0ZmdPUvpzPfS01npxMM4o1au06+tG7qa2rqRHGIve1o9JmWZwB23Poj2QjSW59EeyEaAAAAAAAAAAAAAAAAAAAAAAAAAAA9HQ+Ce37nnN+z8rdoO6vOnax3+Ke1r1uVe1l1PjkFfwz2wR8M9BHK3Z95X8XYDkcJLcJlVe3PogHbc+3ijSTyjphGAAAAA1V5MrVTkDT9P3N/Mc+XDKM4Y7zpVHeJuz3z6nSWtNkDEeOVHAUABW3KWVqtyllAAAdjm4A9CunpWjjqbs+G7M/x5K/T0omI3+HHjif14z4MWZdzKjXOnpxM4vnl3Tx8fHk79PT4+/jj+TPGP0se9PiZnxQaYrTPGeHjifVWaxmccfNBvSZnxUTRWuY7vNo+no5j953cZms8J8PPxYd6fE3p8UEt61rndnPLjjCB1wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJT4q9sI0lPir2wCUBQAAAAAAAAAAAAAAAAAAAAAAAAcnlLrk8pBnAQXfVfJc7+pX6MakW3KzO9pVxE59397ExMW74rMWnHCXyrZobTq7PvfTtu72M8InlynjE4mM8JjjCjfttNPRpSmjXepMzP2iYiJ1ZjhivPdrH5MzvTznueIl+pbc3N6d3e3t3u3sYz24RA7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAAAAAAAAAAAb9n/F0fewNuz/i6PaC2v8ADHazanxdENWt8PSy6n4fzYBSvf2SV59E+wrzgrwmO0FEk8olRb8PSDv4eyUa9e/sUAAAAAaqcuEZZWzSnGPe3efHGfvhRzLrfvxHLaL/AMs9eOLPvZ92dW27znhnj3cM/wD4BDiePCfTk41TNZnjrWxyzu909Phx5uRfnnVv3Y4c+GPH08gZVWzeiItjWtnOcYnj581Ztv8Axalp4Rjhno4zAIJiY7pVbYtXjP1rZnn7vP8Aj3oL3m8Rm0zjhETHdw48OHHvz6gzW5SgTzyQAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAguD6P5XsNNttferq3mu7iulMRbjFp3pzW3CMRHLnKj5wfU62hp02XXidk1dC+nOnMW1ZtOpbetMT+Gld3sr0vlgdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAANmhzns+9jatDnPYDRq/Dbt6mO/KvY3anKzDb4KdII6847Sebi1vintAtzl2OVugtzjsj2OV7/OAK8/171HYWtwmQUAAAAadPU+nxjHKY4xnmzAPQ+vjGIpwzHwc8+PDj5eCs63lp/wAkdTCKN0a27Ofd5Y4xngtOvnu0+ikR9zzwGibRM84/XoWi+JyygNltXe745zPCPHoW+tOIj3ZiPGM93ewgNWpqb/dWPzYiPuhlBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASU+KvbCNJT4q9sAlAUAAAAAAAAAAAAAAAAAAAAAAAAHJ5S65PKQZwEF2zZtotsurGpWM8JiYzjNbRiY8uE8J5wxij0No2vV17aszaa01LzedOtp3ImZz8OccHngDtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAABq0PinslladH4+iQbNTlbsYJ+CO16F+/s+55//t9IIV7c+iPYovPd2ATyjs+8rzjtd/DHbKgC1vugtzknlE9sfr6goAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILvc2DY9PaK6l7za003YrpVmtJ1Jtnhv392OXLE2nuh4b2Nh237JN81m1bxETi2JjomLado8a3rMeCjXtGw0rs9taaX2a9Zj9zeYvNomcb3CIvp4/wD7kYnul84+g2v5jXW0vo6dJ3eczOKRn/LpacV04nxm2/bwmHz4O259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAGnQ+OOn2MyfR+OOn2A9CfuefHwW7Xod/Q8+vw3BAvPKFF/wx2yDv4emPvRrxyn9e9QElu7shzu6SeUOxynsBGAAAADRXSm8cPZlJmI4jONkbPaeUTPRLv2e/hb+WWdOnla0ZYhqnRmOeY6HPpef8DSgtLMNP0vP+B9Lz/gulCWlmGn6Xn+vqrOniOZpQtkADTIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILg9PZNmrr782nU93dxXTrFrWm1sREZmO3v7FHmD3ds2Gmjo019LU+pp23a23oiLUvau9ETFbWjumM8JzE8HhA7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAAAAAAAAAAATaXx17UKTT+OvbHtB6nfDz4/HHlP8G+e7p+9hj4r9kgzJPw9MexGkj4bdAFe/slGvXnCgL/h6SvPokjlPQV4TAKDsxxcAAAe1skak/BETMRnjMx+LymJ5478eLxWqmtNI4Z7YnDFcXhYfQV2TbOVYxOYxXfpFs2nHCu9nipTS2q8TaLfDa0Ym9d7Na5twnjy78PF+0Tn8XbvcfYRrzHLMf9X6HHQ/t9zel5vW1dk2mlfqatZiPGZic8YzjEzyzGe1X7Hq+7wj36b8ce7Ez290+TyvtE/5v5p6j68xyzH/AFfoXR8i71Pset9S+nisWpETMTasc5jGOOJmcxjC/wBh197dimbZxuxPHOJnny7p6Xk/XnOeOfzv0O/abf5v5v0LozyI9aNg2m04rp5nGZiLUme7wt547WXaNn1dnjGpXdmYnhmO7hMcJnkxfaJ8/wCZS2tNo457+c5+5dGeT3LdlAdnMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASU+KvbCNJT4q9sAlAUAAAAAAAAAAAAAAAAAAAAAAAAHJ5S65PKQZwEF3tbBq6dPqVvetN7cmJvFt2d22cTu01MZ/Nl4oo+n27X0LaFqUvp2m2ppWxp72IildWJm0zo6MfjjGImeHF8wAO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjWrzjtgHq262KP7S3S3W+9i/8Ad/XwBkXrynsVlav3T7AcjnBaMTKq9uYFe/sUSV5owXtzUXt3dn6FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBd6Whsk69Lan1dLSrW0VzqTMZtaJmIjFbd0ceTzXs6F9nvs99HV1baUzqVvE10/qROK2riferjn5qL6/y3V0I1d7U0ZvoxE3063mb1jerX8nd52jPvTzeG+t23U2Sl9tnT151ba1YpERp4pH7zTvnf3pz8GOT5IHbc+iPZCNJbn0R7IRoAAAAAAAAAAAAAAAAAAAAAAAAAAC0c4VdB69vvYp/tY/Xubbff9zHfhqR0AyzzntWrzhy/wAU9pX4o7QUXnu7Icnm7PKOmAcjnBMcZcWt8UgTyjpUX/DPbCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAguDbs+y6+1W3dHTvqTzndjOI8+6PLPNRiHo62w7Vs1K31dHU0625WtWYjnjE55TwnET3POB23Poj2QjSW59EeyEaAAAAAAAAAAAAAAAAAAAAAAAAAAAAD1rcp6GTV+OP172u3Lohk1udf17wQX+KVEup8XohBa3Oe138PSW5u/hnoBGvbu7IUXnlXs+8COU9n3wovXn0T7FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBd9FsM6n2faPp6X1rb+j7sReZiMamZ/dzE444ntfOJK2mvKZjsnCj6q860bDtMauzToRnRiua6tc+/M4j6lp854Pkkk3tbnMz2zlGDtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAHrc4/6aser+Fsj4Y/NqyavKv690Ai1PiQpdTnHZCIElu7sj2FeVuz73Ld3Z95Xr9gKJPwx2yjX7p7YArzjtVlxe3OQUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASU+KvbCNJT4q9sAlAUAAAAAAAAAAAAAAAAAAAAAAAAHJ5S65PKQZwEF14zM4iMqPp/letOz02jVppfUvXc41/tNOnvb96Zi0Rj3c5iY44nhKj529L6dt29ZrMd1omJ9JRP0L5rpz9itMaVLUpqVrGpm2/WcznEYnTpW3fStuEzE44vz0Hbc+iPZCNJbn0R7IRoAAAAAAAAAAAAAAAAAAAAAAAAAAAAPUr8Mfm+xn1eUfr3NFPgj82UGr8MdvWCC/wCHshCmv8NexCC88odp8UOfhjtn7lQFq8rdn3luc9pHf2SCiS3d2QjSTyj9e8EYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAgulpe2naLUtNbRymJxMdKIUadTX1da1r3va1r/FMz8XLn6QzADtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAHp0/s4/Nn2otX4OnrS6XwV7Le1Ff+z/XxBBPwV6UCafghCCT8PSjX7p6FAXtz9PYV5wW7uxyOEwCq/4elyeEy7HKegFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBd9N8rtp6dNW9q6czN9LTi95tEUi+/MzmsxMfDGZ8HzLZo7ROlW9dyl633ZmL72M1zifdtWe+VH1O2209XZNXNNCdTT+nfe0tS2puTe9q7m/v2ic1iLTjhGcdz4p6F9qm2nbTrp6WnW8xNtyLe9u8s71rcvJ54O259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAelpfBXpUv8ABP6962l8Fe2fYrf4bfr4AzfgjtQpvwdKEF45W7PvUSV7+xGC88o6VEn4elGC9uZX8XYW59Eewrz9fYCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAguDbs+z6m033NOInEZmZmK1rHja1sREdsxx4KMQ+hn5bGnsupq6upbS1qRmNC9IibxvxSZi2/nEZjjNePHGcPngdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAA9DS+CO2fYW+G36+Bo/BH533O25W6QZY+Ce1Amr8NuhCC9efRPsUXrzhQF45SovXv7JUBeeVez73K847XZ+GOlUBxJb4pRgA9PQrFojM7vp4+eI8+bNU6MXWIu8we3WmnMcdXdnjw3Zn9crxTS/53/0s4/kjkndPc3oc2+O94I9W2Inhbejxxj28VW9Py+NyaLzB6eQ0/LrSzzB6bNq93SsVX2FmUB0ZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBdNGpeKW04t7tpiZjuma5xnszOEIokta15zaZtOIjjOeERiI6O5GAO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAb9H4P+pJPK3T96PQ+CfzoSeP6+IMdPht2IE1PxdiEFo5x2uSLW+Ke0CvOFRa3Oe0Hfw9KNeOU9CgLzz6I9ii88o7PvUAets1qVj3672YmOyd7m8l1mYur6j62w72fstsZ5fVnlnlnHhwzHazzqbN9TMaUxTcxuzaZ978rOY4d+OT5/JljRau+ivrbNNtOaaE1is5tE6kzvx4cc48OGVdLV2au9v6M3zaZj38YrMcI4Yjhzzjm+fyZNEu+irqbL9S8zoWmkxG7Tfn3Z4cZnnPZw5tEa+xRNZ+yzMRjMTqWxOM8vKcxw4zwfK5Mmj5pd9TGvsUTP8A6Wcbsxx1bc8Yz3Rw5xweJtE1m0zSN2uZxHPEeGWHJlYpsXcAdGQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJT4q9sI0lPir2wCUBQAAAAAAAAAAAAAAAAAAAAAAAAcnlLrk8pBnAQXbK6UW0NTVzxpfTrEfnxf/CxvZ2PadHRjUrqxfFpraJrFbcaxeOMXmPyu2JhRk19mtobszxraK4t52pW+O/lFoYXvbXtOz62lWunbXmazGN+tIjG5Wn4bT3UjpeCDtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAG7Q5W7apu+WfQ5W/wClP3yDFT8XYhT6fOexAAvbmovbn0R7AUXtz6I9ii88o7PvAjv7FF68+ifYoC8/DHSov+HpUAAAAAAAAAAFABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJT4q9sI0lPir2wCUBQAAAAAAAAAAAAAAAAAAAAAAAAcnlLrk8pBnAQXB6Gy7PGvv2vqRpaenXN7cJnlOK1rNq71rY4RmFHnj3tt+XRssXmmr9WNPU+nqe7uTW2Ims7u9aZpbutw4xMPBB23Poj2QjSW59EeyEaAAAAAAAAAAAAAAAAAAAAAAAAAAAADZocrdDR+Kf174ZtH8fY0T8X6+MAyU+P1Z09f7TplDPOQcXt3dii88q/r3gov+GO1ReOU9AO0+KEa0c4J5yC0crdHtRr17+yVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBd7mxaulGnq6V7xpTa2nqad7Rmm/p593UrFL5rMWmeXN4Yo+x+Y7ZoakbTamr9a202pEYrNYrp04714mlc6m97sTmfdmeL44Adtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAA16PK/wCa02+LoZdH8f5rVbn0fcDFH9pPbKO3xT2yln+06UV/intBRf8ADHbP3KL/AIekFF69/YovXnAKL2+KVEl+fRHsArzhGtE4mCecgqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILvR2fZL69bXi+lp1rMVm2rqRSM2zMRGec8Jec+g2fSrrbFqVnW0tLd19O0zqWnluXjhFYtaeiJ81GXU2C9KWvGrs+pFIibRp6tb2iJmK5xE5xmYiZ83kvdrTR2bR2n/wBTo6s6ulGnWunGtnP1dO+Z39KkYxSe/Lwgdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAA1aHO35stM8cdn3SzaHxT+bLT+T2R7AY7f2nTCO/wAUpb/2nojv8UgjXjlPbH3qJI5W6PaCMAF7c5Ld3Y7bunycnlHSCi9ucqL27uyAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASU+KvbCNJT4q9sAlAUAAAAAAAAAAAAAAAAAAAAAAAAHJ5S65PKQZwEFwadHQ1dotuaVL6lsTOKxNpxHOcQozDbr7HtGzYnW0dTSzMxG/Wa5mOeMsQO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAatD4uiWj8nsj2M2h8fRLRP4ezqBmvwv6KanxStqfF0QavxAgSR39iNevPon2AoACT8PSfhjtlyOU+p3T2govPKP171En4Y7QRgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKfFXthGkp8Ve2ASgKAAAAAAAAAAAAAAAAAAAAAAAADk8pdcnlIM4CC76/5LG/XaKRG9b93O7Eb04iZzO7FZtascJtHLHOJfILRMxy4c+We+P1yo+++ZUtpfL5rqxEak20szFJ0q3tFtaZ3KW068qzWLTEV7X5+km9rfFMzz5zM8ZRg7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAAAAAAAAAAAABo0fjjp9jVP4f174ZdH+0jp9jVPKvb94MmrzjshzU5x2LavOOxXU/D2AhXr8UKL1+KO2AUHZ5uAvXn28COUqpu+3Zn7wQJPwz2o145T+veCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAguD2dmrpW2fW+raa0+rob0xETbG7q8uXGe7jjxUeMPR2imzUisaOpfVmZmZtNdyIr3Vxxne/KnOM8vF5wO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAT6Xxx+vc125R2/fLHpfHVrt8PTPtkGfV5x0+1W/KvYvrc46fajtyr+vdAIQAXtzlRe3NQBNHd2TCFPTjw8/0AgSV7+yUa9ecAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILt2htWvs0zOleab3PlOcduWEUelrbftO0V3NXU365zjFY49EQ80Adtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAm0vjr2tlvhntt97Fp/HXtbZ5T2yDPrd3Sjt8NU2t3dsorfBX9fEEAAL2+6PYokt3diMBLScWhE6Ds8JkjnCTU+LMd6EFp5yRXLtucpaxwUR7puvsdl0/mF9DT+ls2lqU47trbszMZn8rU4c5ziIz3u32H5neNaPs1axqzWbRW1YrG5yxX6m704mUHxu6br7PZ9k+Y7Pv42XTvF+cX+nPGImImMX7t6V7bL8x1NPctsejMeOK1tzmY96upWe/lOYxEZyD4uNOZ5LfRt4PqdL5b8w0s42fOfG1Otp+yfM8zP0OM+el3Y6m40e11OFU5l/toiY2TNVvRL4udOY/WVdyX1Or8r+Yatt6dD/7afXDwtTTtp2tS0btqzMTGeUx3cODLtHDGLS88dlxFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBd9B8p0framr+738afu2tp21dOl5mMTetYmeMRaI4Tx7nz6eNa8aU6X4ZvW8+OaxMR/CZUfQfM9Cmn8GlNJi85mNLUpWK2jhnfjHvWi00iOVeEvmHoTtmrOl9LMbv0/pcvw/V+r673KfDg88Hbc+iPZCNJbn0R7IRoAAAAAAAAAAAAAAAAAAAAAAAAAAAAJdP469sN1u/wDOYKfFXth6FvxfndQM+tyj9e6EU/BH6+KTV+GOj2IvwdIIQAXnlCi8/DHbP3KAAAmnjw7J/hxQpJ5xPlDkwDtu7shNT4UM8o7PvS0+FR+q/Ldl2vbdj2XQ2bUrpb1dSb3nPKLYxGPHKfQ0Nt+X7X9n19SNWl62mJjemYmOP4uPGO2Hr/1eilvl2nW0W4xON2d2fjn8Wc478Ms/vdum0b1ZrbUmd6+9E05REevZweaap07PTFEfjuzbR8m+YasW2mu0V06zM7lc3icRnwxGXlfLdv17U2muvE2toV3onGJtEZ4dvB93a1K6czetpilJ3ZnUmIzM8YmPCXhfLp0b798Vnji3LjHPHPlMdKU1TeYsteXEU0zw4e29nlx8t+a7Xs8bXbXjS540/erj04JNbX19D5fS9p/ezis24Ticzmf4er73atTZ76NNT3r0pFrYpfFcbvDlOM8eE8vN8vo6elbZNOutiunjNp1JxiJziZtPRxSmuZ7lry4i0RPHa/O9j+YbRp7Vp1nU1LRe9a2rad7MWnHDw8sPK2//AMXtP/e1P96X01dj2edv0o2fXpqe/vRMW5bvHh35xHDD5n5h/wCM2n/u6n+9L0RN3mmLPClx2XGmQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJT4q9sI0lPir2wCUBQAAAAAAAAAAAAAAAAAAAAAAAAcnlLrk8pBnAQXB7ey7Hp6ujfV1LY3b1pEb9Kc6zOd6/Du7lHiD6G+xaP0da9L8dKsXx9XS1Mxv1rjFOMfFnPJ88DtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAF6fFXth6M/i/Oj7nnV+KO2HpW527Y+4GbU+COj2IY+Ce3qTanwR0exDHwT+vgCEAEn4elGvHwz0KAAAvPKvZ95E90k/DHSoCWYxEdspacoQxMxWe3rTROYhR95fW1dH5Pst9K00tGpM5jhPO8PP+U7RteptltW15vbcmJ3+OY3q8PYttF//wDU7LEd15/jvOfJbxS2ree6Kx659s4cdkz5z73bbHND3/6w2tOno1pqXi1rzG5FpxaJj8nOPLk9b5V8v+xaeJnN7cdTPGM44R0Q8Glo2r5ne8zmmhiIj/N3f/bMz2PrI2quZpE5xGZ6cuVU8LYOlMcr43W0Z2bbtOunq30tDUvu6la2mK8eUYzytPDyfo06dL0xaItX8mYzHTD8023VjU1NSJnuj+L6HZfmE6myUm0+/GYt21nE9azOBHF6+ps+lW9dSlKVtXlMViMcOXLv5PyHbpzte0T46t/96X6XbauFpmeHd/Hqflu02zr6s+Opaf4tZd9rOZZ5U83F5nMqO7zgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAgu9DR2n6VLadtLT1qWtFsX3+FqxMZiaXpPKeMZw88UepO1xuXpp6GjpfUiK2tWdWZmu9Fse/qXiI3oieWXlgDtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAFo5x2vTt+J5T1bfi7OsGW/wen3oo+GU1vgno9soa/DYEIALxyn9e9Revf2SoAAC/wCHpUX/AAz2woC8crdC0TwhWvf2HhgHv695jYtLTnMTFs8f+pDsut9Okx+VevpVn1I2jUpWLU1Zx41nlHQhrpa0RP7vU/lt1MW97cT7n0exa+79S/5VrWz4zM9Xtejpa9pvqW7scZ7Hy+nGtWmPp6n8lupNS+00iYimruz3btsZxz5M6LWkl2jWzq284hr2S86dNTPKbePi8O2nrTbP09T+S3UlrGvEY+nqc/yLd3QaJFT29TaZ3cZ7pfL6kzv2z4tdq68/+3qfy26mDU34t79bVmfGMe1uIszVN0EuOy40wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKfFXthGkp8Ve2ASgKAAAAAAAAAAAAAAAAAAAAAAAADk8pdcnlIM4CC709k2X7TM+9Fa1mkTwta3vziIrWsTMzPd3ZxGXmPY2HbK7La29WbRaaTmtsWruW3uHdPHjuzwmYhRLtmwfZ4teszFa7maan9pWbxOOO7FLROJxuTPB4T6LbNvprac6VK546c78xWke5E8KaVPdpHvTHOcvnQdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAPVt+Lsj73lPVnv7I+8Ge3wz+v4kFfht+vdKe3wT0/wC8hpyt2AgABJTn+vgjXrzjtVBwAF45W7PvUXjv7FAXrzdxPDDlfijtT01Ppz3d8cYzHFRTf1fy7fzT1m/q/lW/mlqnWiYxjTjsrj7vSeaP63DHud3Hd48PPCCLf1fyrfzSb+r+Xb+aU0a0+Mfinl+Vz4SpbUi35MdlcKKb+p+Xb+aes39X8q380rzfeiInHDyUzHjAOb+r+Xb+aVZ3rc5me1ojWmKzXMYmMTw6Xb6u9HKvdyrET/CI6fEGKebjriAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILg26Gzzr73vU060iJve84isTOPOZnwiImVGIelrbLuaf1aalNXT3orvV4TW0xMxFqWxMcpxzicc3mg7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAep/hh5b1P8EAht8M9Pthn0+/saZ+GeyWfT59H3ggAB2Hbc57VV7cwUABevPon2KL0+KO1QBa3OVV7c+iPYCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAgu9PZbae7raWpf6f1axu3mJmItW0TG9jM7s8YmcTh5go9jVmmhs30I1Kalr6tdS0041pFK2rWN6YjMzvznGYiIji8cAdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAPU8PzIeW9SPw/mdQIvwz2fdDNp8/wBfFp/DPZ90MtOYI5cdnm4Avbu7IUXnu7PvBQAFo5w5PNxe3OQUXt3dn3qLz8MegKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKfFXthGkp8Ve2ASgKAAAAAAAAAAAAAAAAAAAAAAAADk8pdcnlIM4CC4CgADtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAB6cfh/M6nmPSjlT83qBSOX6/kslObZH6+jFXn6+wHJ5z2qrW5z2qgLz8MdKi/4ekFAAF7c/T2KL27uyAUX/D0qLxykFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAElPir2wjSU+KvbAJQFAAAAAAAAAAAAAAAAAAAAAAAAByeUuuTykGcBBcBQAB23Poj2QjSW59EeyEaAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9KvLT7Jea9Kvw07JBWPv+6WOnxNdec9v3yyV+KO0HLfFPaovbnKgC8cp6FF68rdn3goAAvPKOz71F5+GOkFF69/Yokrz9fYCMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJT4q9sI0lPir2wCUBQAAAAAAAAAAAAAAAAAAAAAAAAcnlLrk8pBnAQXAUAAdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAPSr8NOn73mvRr8FOn7wcjnPbH+9LJHxx2/e1d89H+8y/j/AOr7wcv8Xp7EaW/Poj2IgF6/dPsUXrzgFAAEn4elGv3T2x94KJ6oGmvJR6ehsunraW/baNLSmJmN2+IzEbvLjMznPhEcObmpslNOdSPr6N92kWiazmLTM43Y845ywYMA06WjpX3t/Vrp4iMe7M5me7lE8I5ziYa9TYtPT0pvG1bPed2J3Kz73HHDt48eyXmOYB7UfL9G1It9r0KT31viJ5VxMcZ558sY4o9PYtK99Sltq0Kbu5u2nG5bPP3t6JjHfwmXlOYQbtfZI0qxautoauecUtG9Xl3Tiec44ROMIaaVLVza8Vnwxnw8mcworq1iszETE+ccPuifVlarcmUABAdjm4vTjaO2AbtDTrqX3bWjTjFp3pxjhWZ75rHHlzb9bY9PSrvRtWz6nvRXFZ48fxY8IT/ZdPwn1c+y6fhPqo822jSutOn9Sk134rvxymM/F4Yjt7Gr7Jo/UvX7TpTFZti2OcR07ufCImYzwy0fZdPwn1d+y6XhPqDyraMU1NzepMccWrak5jPOd2bY7Mt0bLpcc6sRy7pnt5V9qb7Np+E+q32bT8/VzmJnhMx7IbiYjjF2T7Npbsz9Tjx4bv6Ij+LzHu/ZtPz9Zc+y6fn6rETHGb7kmY5LPn7QheztWjTTpmvjh4zTIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILgKAAO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAHo0+CnbP3vOehT4Kds/eDnfPR7WSfjnt+9s75/XwY7fFPbIO359CJNfn+vjKEBaOEqgLW4TKq9uagC8cpUXr39gKNNOTM005KJAAAAAAAAVtylka7cpZAAEBJT4q9sI0tPijymJB9cIt6DeBKIt43gSiLeN4Eoi3oN6AYtt/s4/Oj2S+ee7tk5pEeefSHhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKfFXthGkp8Ve2ASgKAAAAAAAAAAAAAAAAAAAAAAAADk8pdcnlIM4CC4CgADtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAB6Gn8Ffznnt+n8FfzwWnn0dTFf4pbJ5z0/cx3+KQd1Of6+Mokt+f6+KIAAF7d3ZCi88o6VAF68+ifYovXnAKNNOTM1U5KLgAC+5aIzuzjGc44Yd3L/AJNvSQRi+5aPwz4cnfp357s+gIwAUtyZWq3JlQAAF6/FHaotHOAe9W02ziJnHFX6jDp21cz9OLcsTuxM8JW+nrf8u/8ALINe+b7J9PW/5d/5ZPp63/L1P5ZBuvvU+KMKxeZQX+06mN6mpbHfNZyjjT1o/wDbv/LINU3xzdi2WSaa0/8At3/lnqIprR/7d/5Z6gNe2a9LzE9pzCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJT4q9sI0lPir2wCUBQAAAAAAAAAAAAAAAAAAAAAAAAcnlLrk8pBnAQXAUAAdtz6I9kI0lufRHshGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAN2n8Efnx9zC26fwf9cfcCSec9k/cyanxS1W5z0+xl1PikC/d+vdCFNflH690IQAAX/D0qJI5W6EYC1ecdqroDTX4UFuc9qanJRIAC+/bGN62PDM4W+pfOd63qiASTe8/itw4855+rv1L/lW9Z60QAACtuUsjXblLIAAgLRzjtVdgEkb0cpx0rZ1Pyrev6WiuvuxFd2loj8queZ9bjE4rHP8Pjw/h3AzZv8AlT6u51Pyp9U86uc8KRnHKuI4dkR0n1ufwzmZnjXxBBvan5U+pnU/Kn1SfUxOeHfPLhx6FJtEzM8Iz4R+gDOp+VPq5van5VvV2LRExOfa0faJmYmd2cRjjXP3cwY8YhGn1L7054dEYhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkp8Ve2EaSnxV7YBKAoAAAAAAAAAAAAAAAAAAAAAAAAOTyl1yeUgzgILgKAAO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAG3T/s/+qPuYm3T/ALOe2AXn4v18JZdT4p6PY1T8X6+Esup8XRAO35V/XuhAnt8MIAAAXr39ii9ecKAAAktzS0+FDb7o9ianJRIAAAAAAACluUsrVblLKAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKfFXthGkp8Ve2ASgKAAAAAAAAAAAAAAAAAAAAAAAADk8pdcnlIM4CC4CgADtufRHshGktz6I9kI0AAAAAAAAAAAAAAAAAAAAAAAAAAAABs0/wCzt2wxtmn/AGdwS2+OP17pZNTnH5sNdvjjo+9l1Pw/mwDk/BH6+KFNPwR0fehAAB1a3OVElvugEYAL27uxNXlCGeVelq0cd8xHCecTPsUVy7lsm9Yif7G3/Tbj7PuRzMTXGdKOXKts+z1Bny5lsmd7emLaUe7PDEx6Z7/DvM1mPi0umtuPDHdGOHf5gx5MtOcTMZ0uN/DMdsTEfD2SW3bRz04/Ni0fcDPky2WvGJ/sZz4Vtnv5cMeaKNTdiPd07f8AT5eeOnzBltPCWZonkzgAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSnxV7YRpKfFXtgEoCgAAAAAAAAAAAAAAAAAAAAAAAA5PKXXJ5SDOAguAoAA7bn0R7IRpLc+iPZCNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa9P4LsjXpfBf9fEE1vijoZdT8PY1W+KOj2s2r3Ar+D9fNCl/CiAAAST8MdMI1/wAPSCgAL/hjtn7k+neKccVtwmMW5cemOMd3FB3dKgN8asRPwaff48c9tuceR9Sv5FO/8r/EwL/h6VGuNSInO7SeGOPt583fq1n8Gn/H/EwANOYmZng7W0ROeE+U8mUBtteLd1Y4zPD9M5xHdDv1IxEbtOHlzz48YnzYQGrUvFuUVrw7s/fMsoIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC2FVwcwYdAcwYdAS30r6czFoxMTMTHfExMxMesShw3ak2nT0s33qxE4rvR7mb2zwiZnjzmZiJ49jI1LFMzMY24zGHlNtqmDDoy25gw6AqvT4q9se1SV6fFXtj2glF8V8Z9P0mK+M+n6VFBfFfGfT9JivjPp+kFBfFfGfT9JivjPp+kFBfFfGfT9JivjPp+kFBJiv5U+n6TFfyp9P0gjEmK+M+n6TFfGfT9IIxJivjPp+kxXxn0/SCMSYr4z6fpMV8Z9P0gjEmK+M+n6TFfGfT9IIxfFfGfT9JivjPp+kFBfFfGfT9JivjPp+kFBJiv5U+n6TFfyp9P0gjEmK+M+n6TFfGfT9II3J5SkxXxn0/SrO7ieM+n6QZQEFwFAAHbc+iPZCNJbn0R7IRoC9VF6g9PZdlttP1t2a1+lo31pznjFMcIx3zngwS+q+XfOtfYtPV0/q6sUnQ1NPSrXGKal5zFuMxwjjMzxl87tGvq7Te2rq3m97YzafKMR/BRgAQAAAAAAAAAAAAAAAAAAAAAAGvS+C/Z1sjXpfDfs6wTW5x0e2GfV7un2tFu7o9sINXu6faCP8Hr7YQpo+Cen7kIAACSvfHjHs4o1684BQdmMOAvHKehRJXlbs+9GAkj4Z6Ea9e/sBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABdRcAAAAEk53a8Y45mPHn38PTijXnOI5fw/jjioqR6Z94AigAKr0+KvbCi9Pir2x7QSvd2L5PtnzCJto0jdj8d53a9E8ZnHfjOHhP6U2TRpobPo6dYiIrSsR6cZ6e97tWyYzap0sIi3W/P/y38hXqGXRoUxNeZMxGljERFr4RMcsPyL9lvmPjofz2/wAB+y3zHx0P57f4H7SPqeDyvPe/HfPtd/5+p0vxb9lvmPjofz2/wH7LfMfHQ/nt/gftKtrRWJtM4iIzMp4PK8958+13/n6nS/GP2W+Y+Oh/Pb/Afsr8x8dD+e3+B+v6G0aW01m2leLxE7szGeEx3fxacweDyeWd7U/zuvUzar8cTHGJoxjnxfi/7K/MfHQ/nt/gP2V+Y+Oh/Pb/AAP2kyeDyvPenz7XeXK9Tpfi37LfMfHQ/nt/gP2W+Y+Oh/Pb/A/aQ8Hlee8+fa5snK9Tpfi37K/MfHZ/57f4D9lfmPjofz2/wP2nKm9Xe3d6M4zjPHHjjwPB5XnvPn2vf8/U6X41+yvzHx2f+e3+A/ZT5j47P/Pb/A/aQ8Hlee8+fa9/y9Tpfi37KfMfHZ/57f4D9lPmPjs/89v8D9pRxes2tTMb1YiZjviJ5euDweV57z59r0/T9TpfjX7K/MfHZ/57f4D9lfmPjs/89v8AA/aMmTweV570+fa7/wAvU6X4v+yvzHx0P57f4HP2V+Y+Oh/Pb/A/ZovW2d21ZxOJxMTiY7p8/Fc8Hlee8+fa9/z9Tpfi37K/Mfytn/nt/gP2V+Y/lbP/AD2/wP2nIeDyvPevz7XeXK9Tpfi/7K/MPHZ/57f4D9lfmHjs/wDPb/A/aA8Hlee8+fa7y5XqdL+ddu+WbV8vmI16YieVonerPZMeycPHl/QnzrSrrfLtqi34dO148ppG9Hsfz3PJ8rWMqMmq0cJi+L9p/Fa9Vr2TNVcRFVFWjNuE4RMTF+HMgAeN9xcBQAB23Poj2QjSW59EeyEaAkrzRr1BNn9cEzwnqehp7TpUrFZ2TZ9SY/Fa20xaePfua9a8vCscGPVvXUta1dOmlE/gpN5rHDu+pe9uPnbvaGIBkAAAAAAAAAAAAAAAAAAAAAAGrR5X7GVq0fxdgJ7d3R9yDV7u2famtyjsj7kOr3ds+0FI+Cen7kCevwz0+xAAAAAC9uefHioknjWPLgjBevf2SovXn0T7CK5BRevP+Du5PktFcTlRCJdzzj+JueYIhL9OZ5fe79K3h/CepBCJdyf1y5uSCMAAAAAAAAAAAAAAAAdX3ewEYk3DcBGJNzzj+JuT5KIxJuG4gjEu4pMYBUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABaIm04iJmfLi0bPoam06tNHTjN72isR+vdHe/fflnyjZ/lunERWt9WY9/VmOMz3xHhXyerJyKs6ZtNojjPojzfF/kP5LL1CmLx+Sur9NETbDlmcbR7H4bX5Zt1ozGy7RMeWlfqS/wClfMP7ntP9Ffqf0ePpeBjtzuh+W/yLO+jl76n84f6V8w/ue0/0V+o/0r5h/c9p/or9T+jw8DT2p3Qn+R530cvfU/nD/SvmH9z2n+iv1H+lfMP7ntP9Ffqf0eHgae1O6F/yLO+jl76n86T8q2/Ff/SbTy/5Op4z5I/9K+Yf3Paf6LU/wv6PDwNPandCf5FnfRy99T+cP9L2/wDue0/0V/8ACf6Xt/8Ac9p/or/4X9Hh4GntT1H+R530cvfU/m6flm3V4zsm0xH/AGr/AOF5t6WpM1tE1mO6YxL+o3j/ADD5Zs3zHTmurSN7Hu6kfHWfKfDxiebFWo4To1X549L0ZP8A6K9cRm5UU0zxqomZmPO098P5vlenxV7Y9rdtuyamw7RfQ1PipPPutHdaPKYYafFXtj2vjzExNp4xhL9zRXTXTFVM3iYiYmOExPCUr+mtP+zp+bX2P5lf0X8v2rT2zZdLVpMTmsRaPybRHGJfW1Gca45vS/Ff+jpqmjV6ojCJriZ5JmKbb3qgPtP5+PDptldr1tbZq5pNN+t7b0RaO6NyOMznnPKIe45iGZvO23L5w60VU06V6bzb7ZvbRnltt72bQ2fT2eJrp13Ymd7HniI/jEcXg6Wx6ttq19bFabuta1Z3Ji9/3UREb8z8Ge7d5w+oGZoibbLcLOlGfXRpze8106MzOM2vF+PM+M0a7ZbRvvam07030ItmlqTWfqR9TctN7Zjd57uKd8NO2U2jQrpRp32nW3d/hG/m3GN2LXpmYmscI34ms98vqhj8WFrzz+2+2Xp8ZOnFWhTa8zNNoiJvTEWwiLYRhbF8zM7V9qt/b87eP0vpfS4Y7t/6n/V0Mda7Zp6GJnabb2ls9rTO/a1bzM/UxyvwiIzWsxL7IPx/3Tt60jWrREfjptEURz6E363yFI1a6ey6+tpat9TT1tSJt9KZ1fp/vK0nHvXmJzHfPa31vjb7TubVu208TM01ZpFo4+7OMRGOjL6AIott2xPDj9tuv3s1azpTVenjFVNom0RFVV4jhsmZtwfF6c7R9n1pj7bvWvTFb/Xm2np54zG9i1pmONo05ie6GjR0tr140q6mptGniuv78b1ZzGrH05vEzOfd5RMzmOcy+sCMrzmcLdd26tb42opiZq0ombTMfZoxGMY8vntV5Rx7ucvL2HN66mvMcde82j8yPdp/9Yz2y9Zx1235+va8UVWpqi36rY+UXm1vObT7Hze3acW2rRtalrUjTvxjQtrRE71eGK1nHfxRburO2xN668xXUtMcLfSjT+jMV3cRjezz7/F9S65zl3m99t3rjWZppinR4UVUcdlU3vGHHHlfF/Ttr7FtmjWu1xO9a9N+NStrxjhGbcbZnPu8XdpnaI09KNn+1xEUvaJtGra83z8N4mazHDj78zWfCX2Yz+K+3ZEXjDhd08Zab6ETEVTVaZvF5piJvhaeF+DxdDR1ra+pqW1NWsRq4ikzO5ak6deVZ4fFmYmO+HtA7RFngrzJzJjhGEREREcI9/LiANOTyPmn/wDH7X/2NX/cl/Okv3v59tens2wa1bWje1azp0r323uE9ERxl+CS+FrsxNccsRjvf0f/AM9TVGr5tUxhNeHnanFAA+W/YrgKAAO259EeyEaS3Poj2QjQF6qL1BNwcnk9bW1NSNDZazoadKxWbVvuUm2tM6luNrYzMRMbu7OYjHJDt83trTa+jTQtamnO5Sta146dfeitYiI3497ERwy0PHAZAAAAAAAAAAAAAAAAAAAAAABq0PxdjK1aHO3YCaeUdkIdXl0ykn4Y/N+5TV5dP3QCOnKf17pQJqcp/XulCAAAACSO+On0RrVnE5JjEgtX4oSVjhCGOcNNeXqD6PZp276NI09ljVpGcWnTm+eM55zMd88sZUvs/wAw1Pq/+mvSNWa70VpMV93liM48++X2Py3Z9t2rY9m0dktSlrRqTa1u6sW8uPe07NTb9j2v7NtVq6lbVtNbRMzia+MzEThjSi9m9GbX2Pidn0tv2bfxsm/F+MxbS5TETiYxjHOV702/UpuW2Ksx4/Smts5medZrM8+/wh9ttHyz5pqRbaNPWpp6cTO7G9aMx47sRj1y875b8x1tTT2iNoj39Cu9mIxvViJ6M8O5Yqib4pozD5DR2PbdLP8A6XUtn/LLXGntsTM/Y7Ty56eccvHsfVRsfznatnjao1K6VeONPems8PLd9s8U+ttOvo7BTUviNW3uzPPE5nM+kNRmzwiXGrV6Zxqjj1vz/V2LbdS+fsupXyinB5F62paa2jdmJxMd8TD6rZPmm012mlZ1Lalb3rW0W485x7uIjHlEPF2//wAXtH/d1P8AekvduI0YiHhzzcdnm4KAAAAAAAAAAAAAAvXm16czp3reMZrMTHbDJWMy2bs+EqPW1fmWtqzmdPQjnM7tIjPvb3HMzPl2cHdT5lqamnbT+js9YvzxWeeMZrm0xX05vGAelO3as6f05ppTWKbkcOMcIjOc43uHPCDW2nU1tPTpaK4pjGJt3VivfaY7o5RDI6CmJMSsA5xRXjh0pkd44AzAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPvf6padbbfa0/g0rTHTMR7H7Y/n/+r+2V2Lb6WvOKXidO0+G9ymfKJxnyf0A+/qUx+O3nL+Y/z9FUa5TVPCqinRnZheJj2el4207d9HV06Rp605viZjStaJjctPuzHCZzjx4ZetS29WLYmMxnExiY7Y5x5w5albTWZj4JzHbiY9kykfQiJiZvN78H5uqqiaaIpptNsZve83nyfPz8xxtt9CdzcrSfz9+tYvPRNZxHnCOu3bRq12iY0q1mmlp6lK7/AB9+LTmbbk8cRwjdmHs/ZtH8iPjnU7/itExM8/CcY5M0fLtlrW9I08RfEWiL347ucR8WcRmYxHDDjo18vL5cYm2yeEzg9sZmrW/+c3tRF+N5pqvVNorp4xsQRtupFNCK6X1bX0Y1bZvWmK+7nnXE2zPL3YW+06ldq1KWjFK6P1IxMTvYnjw3ItE/9UxKX/Ttl3aU+lmtM7sTa88J5xxtxrw+Gcwk+w7N9b6257/jvX5eG7vbuPLGGrV8sceXyn+3HHFJr1bH7asYrj9ON5qvE/8A0tGHJGHm8+PmVt2f3Hv/ALnFfqRia684rO9u8JjHGMSpf5tFNOl/pTMzvzesWmZpGnbdtPu0nMZ5Tbdjxl6mnsOzaUYppxEb1bc7Txp8POZ4R3V5R4KX2DZdTG9pRw3u+0fHO9bOJ45njx5TyS2b2o+PZvWK9Uvjl1W0r4TN7aNrfqnbjyqae1amprWpGjM0reaTqRflO5FszXEcJzjOWjade2hWs1p9S1r1pFd7d4288T7GmmnTT3t2Mb0708+M4iPZEF9Oupu70Z3Zi0eUxyluIm3H24dzyzVl6UToWptF4vP3TbGZ+7C88mD56/zKbadLVpas4tqakZrmtNO+7aImazFszy5Zjvh9K86dh2a0UidOMUmZrxt+K29OcTxibccWzGXolMVY3m/DpXNqyqoiMumYtNV78kzhF7zwjmfkf9cdKsa2zan4r0vWf+ia4/3n5tT4q9se19n/AFn22u1bbFKW3q6FdzPdvzObY7OEdsPjKfFXtj2vzesTE5tduF/dEP6v/F0VUalkU1YTozOPG01TNMbphK1aO06+zznR1b6czz3LTXPbhlHDGMYl9WaYqiYqiKonjExeN0vct8z+Z0xvbTtMZjMZvaHK/NPmVs7u07TOIzOL2nEeM+TPXa61zMac+9Xdn3+/GPyfhnvr/FW212tvYiY3q7vxd29E+Hljpb06+1Vvlw8Nk/SyvUp7mifmvzGOe1bR/Pbrc/1b5h/e9o/pLdZG10xf3bxM03eN4tmYrNYz7tfd78eMZQ22vMTFa7ucZ45z8WY+GOE73COcYNOrtV75PD5H0cr1Ke5P/q3zD+97R/SW63Z+a/MYnE7VtMf/ALlutW22Utv+5aszu4je3otieV+EZiI5cFb7bFov+7mN7d470TPD8rNPe8uEYPyVdqvfJ4fJ+llepT3L/wCrfMP73tH9JbrP9W+Yf3vaP6S3Wx32je1q6u7PCazibZzjzxHPsctr72vGrjlas4tOc48ZxGZnv4GnV2q98nh8n6WV6lPc2x81+Yzy2raJx/nt1+J/qvzHOPtW0+H9pbrUnbc5920ZtFuF8Tw3ec7vG3D4vPkfa6cZilo/eTfG9Hf57se9HdOOB+SvtV75+OU8Nk/SyvUp7l5+a/MY/wD+vaI//ct1uf6t8w/ve0f0lutX7by92Y9/e4Wj/B8X+b+DHGtEa06m7ON6ZxvTnj/mxM8PE06u1Xvk8Nk/SyvUp7m//VfmMY/9VtHHjH7y3GOPn0H+rfMP73r/ANJbrctt+axEUmMb+Pezje3+Xuxj4uM544hWm27laxuzmN7jvREe93xEV4T44nErp1dqvfJ4bJ+llepT3L/6t8w/ve0f0lus/wBW+Yf3vaP6S3WxV2iaattSI+LPCJxjM554bKbfFMY0uPf73PljlXhwjE8eKadfar3yeGyfpZXqU9zv+rfMP73tH9JbrP8AVfmP972j+kt1setrV1a0rFN3dz+LOcxHLhGI6Z4p6bTXT3M72pim7z3ec53fxZiOXcadfar3yeHyfpZXqU9yT/VvmH972j+kt1r2+Z/MqTi21bTWfCb2j9eCP7dwmJpnNd3O93YiMT7s5jhxjvR12qlZmfpzMzSKT72I4Vxy3OXfMePeadfaq3yeHyfpZXqU9yb/AFX5h/e9o/pLdbv+qfMcZ+17RjOM/UtjiwaOt9KNSN2Z3644Tj14TmPLPFutt29F4+nPvRH4vzufu8Yje92OGMQadfanfJ4bJ+llepT3H+rfMP73tH9JbrP9W+Yf3vaP6S3WzztczXVia53+U55Rx4Tw97nw5YQ6etuad6Ymd7zxHTGOPlxjiadfaq3yeHyfpZXqU9yPV1tXXtvaupfUnxtabT/GWaeUpFJ72OO27vERTFoiIiOERhDOAy0uAoAA7bn0R7IRpLc+iPZCNAXjgoA2/aNXdpSdXU3aTmld627Wc86xnET5wpqat9a031L2vaedrTNrT2zPGWUAAAAAAAAAAAAAAAAAAAAAAAAAatDnPYytOh8U9nUCafgjs+6Uepyn877l5+GOyfZKmpyntj/dBDTvRJadXtRAAAAAJJ4x2I14nAKNkd/bLNMY7GqFH7h/V3d/0/T43i0xONycW+Oc8e7zZrWnX26bR9TNb6md+Yxu8ox6xHCccHys7RrbL8n2W+jaaXi8zmO27zvlW2bZrbbOta86k7k7293xNo5eDzaP3TU9MV/Zo2xn3S/WrXr9KYtOru0pMx7+KzOeMTHLGeU8/B898vjQvOpbdrOZxeMY93PLpeN/WDU1K6WlGnq3ibWx9OLcLcOeP15vS+UbBfY6e/MzfU46meMRPdHbjnLGjoze/FvSmuIiI5L39j7fa76P0qTFtT6dYtMxpzwxuziZiOfTwfKaOjp62x6ddX4JjM2vOJiOM70zPDpfJXpq7LttNLT176Wz6t929YmZrHlEccb3KPPm/QraWnqae5esWpwjdmOHAinRiZvx4cq1VaVURo8ON+D81rsOlXb9ONDWpqzF4t7tqziKznPCZ5PmvmH/AIzaf+7qf70v1edi2fS1I1NPT0qWpPDdpWOcYnlh+T7dO9te0T//AHb/AO9LtRN3nrizxJ5uOzzcdXIAAAAAAAAAAAAABJScS3V1L0+G0x2PPrzhvrp5jO/SPKbcVFo1bxMzFpzPPoI1dSucWmM80Vo3ce9Wc+CPINX1dT8ufVz6t4iIi0xEM2TINMat45WnnnpVnUvbnaZQZMg0xq3rnFpjPGcd7LeeDZOhjP7zS4Tj4v0MepGMxmJxPOOUrMWZiqJ4TdmAZaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH33yv+s2tsdK6OvWdfTjhExONSseEd1o7cdr4EdKK6sub0zZ5NY1bJ1mjQzaIqjjyTE8sTGMTzP3Sv8AWn5ZaONtWvlOnP3Zhf8Aaj5X/wAzU/o7Pwge3xub/ZunvfAn/wA/qc7c6P8A+o/Y/d/2o+V/8zU/o7H7UfK/+Zqf0dn4QHjM3+zdPef4/qfazvWj9j93/aj5X/zNT+jsftR8r/5mp/R2fhAeNzf7N095/j+p9rO9aP2P3f8Aaj5X/wAzU/o7LR/Wf5ZMxH1NTjOP7Oz8GS6fx1/Oj2njc3+zdPef4/qfazvWj9j+lftml4z/ACy59t0fGfSXiRjwIxxPG5v9m6e9P8f1PtZ3rR+x7f23R8/SXkbXr6u06dtPRtbRzzvERN8eEccRPnxlG7EREMVa3m1Ra8RzQ9WT/C6nk1aWjVXMYxpzeInmiIifa+I/ZvTnnr6n8seql/6vaWjS2p9a87kTbGI7oy+9jDNtcx9n1f8At3/3ZeF+hfh4CgAAAAAAAAAD0NL6G7Texz97O/mfCOE43eWcRlNadjmcRExG98XvTwmbeM44Ru4jETPe8h0Hr1nY8V4RnenMW+pHu+9jOM/5cY483mXiufdnPGeGJ4R3c/HtnCNwHQAAAAAAAAAHJ5S65PKQZwEFx2IzwdtWaziYmO2MKKgA7bn0R7IRpLc+iPZCNBPXl3ekLdEekKVb9miJ1qRNYvGfhmYiJ4f5uHZnhKjJ0R6QZ8o9IfQzsunadWbTThEzG7O7uzGnvcacqzM8+OM5iIQTp11b6VppExbSz7u7SLXrnh7sRGfGIjIPF6I9I6joj0jqe/q7Poz9a0YjE6nK1cV3YruxiOe9MzGXjakRG77u7mtZ+Lez/m5Rjs5wCHoj0jqOiPSOp91TS2KmrofSvs+pW1L0pa2lv1i1JrNtTWrq1rM70b+MxMVjERyQ2nSrsuvrU2XQnSnWmdD93Frxu6sTval85rSKe5FJmN7PLhk+OsfF9EekdR0R6R1Pe+Y3rrauhpxXQpaNOsaltPT09Ks3vO9y0q1r7sTFcznlxatSujsuhOnetZzFsTOnXfvbFuMTMTau7aaZ96MYmMTlxrr0bRa8zPCOSOMtRF9vB8v6ekdR6ekdTjrsyfy+kdRnyj0jqbtjiJ1ozGfdvj3K6nHdnHuWmImfDLTOjS1NW8xO9WZ5xXTjGIxG7XNYmfDv7geP0R6R1O58o9I6nvxo6OrqV9zdr9GtqxE/HaIrmI4Ty45xxzHF5E0r9aaRM7u/iM88Z8uHTyBmz5R6R1GfKPSOp7mps+jpTabRPu1zu7/H+13eePyeKO+joRofUjPdMTNo4zvzE03Y48KxEzKDx8+UekdTufKPSOp9B9DRvad6MY09GYrGIxFqcbco5cOfjxQRp6V67N7kRE5i9otiZtvWxWZnhEzwxM8oUeNnyj0jqM+UekdT0NbSpS14rWeFKT8cfu7TjMT+VxnHDjHe5sVdC2vT694ppxm05i2J3YzFfci1o3pxEzETjIPPz2ekdTufKPSOp97Ghs9dn26MbPe2dSa3rSkVj93W0Ymff04iZxp7mN+eFow+P2XTpq6kxfPCtpiM43pju4ZnojjKd1zvYuiPSOoz5R6R1PanZ9Dc1Ji0xMXmKxMxxpvRE24fk8uHPPkkts2jGpNa1tbFMxXfiM+/jMTz+Hjy7FHgZ8o9Idz2ekdT2abNozWtrWxE7sTO9WcWnVmLf/Tjnl3tOloUpqXiabvCsbtrUmYraZzf3onlERw58c5B87nyj0jqdi0xy4dEPYjZ9Dc0p96d61c4mOOc5jE4jMeUsG06caepNY4RiJ55xmPPE58YBn3pc3p/WIVAdz2ekdR0R6Q4A76ekHp6Q4A70R6QdEekOAO9EekHRHpDgDuez0hben9Y/QoA0fX1ZrFJ1Lbscq592OyOXpBTX1dOc0vak/5Z3fZhA4g1W2nXvMWtq3tMcpm0zMce6Z4pvt+1/wB41v6S/W88VWq20a1/i1L27bTPFN9v2z+8a39JfreeMjf9u2r/AJ+t/PbrZJva0zMzmZnMzPGZz4yjdVHZns9I6nM9npDgoZ8o9Idz5R6Q4A7nyj0gz5R6Q4A7nyj0gz5R6Q4A7nyj0gz5R6Q4A7nyj0gz5R6Q4A7ns9IM9npDgBnyj0gz2ekADuez0h3M/rEKgLZny9IMz5ekKgLZny9IMz5ekKgLZny9IMz5ekKgLZ7PSDPZ6QqAt6ekdR6ekdSoDuez0gz2ekOAO57PSDPZ6Q4A7ns9IM9npDgDuez0g6I9IcAd6I9IOiPSHAHeiPSDoj0hwB3oj0g6I9IcAWz2ekdRns9I6lRRbPZ6R1Gez0jqVAWz2ekdRns9I6lQHeiPSDoj0hwQd6I9IOiPSHAHeiPSDoj0hwB3oj0g6I9IcAd6I9IOiPSHAHeiPSDoj0hwAz2ekO57PSHAHc9npBns9IejsVdOdbe1NzcpWbTv/DPDERPOeMz4Slvs2lWupaJzFJvHxcMxaN31rMg8nPZ6QZ7PSH0FtDS1NeY3IiNyk1iL7sWzuxM5nMcMzM48HlTTRi81i1rYvjlXdmmee9v8+iO0GTPZ6QenpD6GNk0Z1ZieFcV4Tecxm0xmYx3Y45nHqz02fQn6U2tw1LRE+9HDG9vZ4d84x5A8b09IM+UekNe06ddPUxTMe7E4mc4mY4xw48/F6v2XRj6W9muYr+KPfzpb3hw97Ecu8R8/ns9IM9npD2Z0NDN44x/aY97lu6cWj1nh4ts7Ns/uVxiM6sxO/E21MUpuzmOOJnOIgV8xnyj0gz5R6Q9jU0dCIvjPPUxm0fhmuI4ePHtaZ0dHU15zSK1+nS1YrON6cVzjhPLM584yI+ez5R6QZ8o9Ia76ExvWjE0jOJm1c43seLIK7ns9IM9npDgBns9IM9npAAenpHUenpHUAGez0gz2ekAB6ekdR6ekdQAZ7PSDPZ6QAHp6R1Hp6R1ABns9IM9npAAenpHUenpHUAGez0gz2ekAB6ekdR6ekdQAZ7PSDPZ6QAHp6R1Hp6R1ABns9IM9npAAenpHUenpHUAGez0gz2ekAB6ekdR6ekdQAZ7PSDPZ6QAHp6R1Hp6R1ABns9IM9npAAenpHUenpHUAGez0gz2ekAB6ekdR6ekdQAZ7PSDPZ6QAHp6R1Hp6R1ABns9IM9npAAenpHUenpHUAGez0gz2ekAB6ekdR6ekdQAZ7PSDPZ6QAHp6R1Hp6R1ADuez0gz2ekOAO57PSDPZ6Q4A7ns9IM9npDgDuez0gz2ekOAGfKPSHc9npHU4A3/bdq/vGt/SW63Ptu1f3jW/nt1sIDd9t2r/AJ+t/Pbrd+27V/z9b+e3WwAN/wBt2r+8a389utWds2mYmJ19WYnhMTe2PaxALZn9YgzPl6QqAtmfL0gzPl6QqAtns9IMz5ekPe+hSI0PpxTe/wA+7Nbzau9NvGdyeG7xieTytpx9a+KbkZ5Y3e7njuzzx3cgZsz5fwM9npD340NGupmnGazfFd6vvTWtZjnExxzPDjnDPqbPpbmtMZmaXti024YzGOUTEzxnnz7pB5GZ8vSDM+XpHU7SKzb3pmseMRn+GYzntK/FXhE8Y4Tyn2c+0HMz5fwMz+sQ+k3P3050tOd2kfUxpxi3vctOvLjGI3oxyy8LQrS+tSluFZtET3cO0GfP64h3PZ6Q9umzaUzferNZjd936ke5E1tM2/hHDz4qU0NC00jP5Ofe+KbaU2xy/KjHSDx8z+sQ5ns9I6ntfZ9HGtMZzTG5Wbx707ubV8fd5+PdLTfQ0bTpxM8MWxia/vIjTiYn3YzxnhxzPgD53PZ6QZn9YjqetfZ9Lc1prn3LTiZtwiOHDhnjz54z4vHBben9YjqM9npCr1Pl2ls2ttFabTqfT05ieOcce6JnExEdqThdiuqKKZqmJwi9oi84eW15uZ/WI6jP64jqeruaNNttXSmNTTi1tybYmLcPdzyicz0SmjQpeNS2pFa2jOdy1a1pjTzE7sZ42twmIxieQtM6URPC8ROOE48sbHiZny/h1GZ/XD3fs2zzaIzjy3vi/dRaO7PPhwZ76GlFNSaxNsWtGd+I3IiIxnxzmY8ZwrTy96Ten9Yh7c6OnqatcUitfo1twmY3p3a57pzMTnPKfNJOzaGnTWxi3xVi82id3GrWIiIxzmvHPgD5/en9YhyZnE8vSHobXpU0rVisTGc5ibRblaYifLMdzzZ5SKzgIj1vl/8A4nT/AOqemKy1aH2XVjUttGrqzb6czM2iMxbu3Jm82tPdy5eDxqWmkxaszWYnMTHCYla97ak717TafGZzKiEAHbc+iPZCNJbn0R7IRoJaytnzQOgnzHk7mPGGYUacw5lnAaM+ZnzZwGjK023uczOIxxnPBlEGjJlnFGjJlnAaMw7E478Mwg0zOec/xItuzE1nExxiYnGJ8YxxZgGq15vM2tabTPOZnM9MuZZgGjJmGcBoyZZwGjJmPFnFGnMeS1rzec2tNp8ZnP3sjoJ8x4mWcQaM+ZnzZwGjPmZ82cBoz5mfNnAaM+ZnzZwGjPmZ82cBoz5mfNnAaMwZhnAaMwZhnAaMwZhnAaMx4mY8WcBozBmGcBozBmGcBpzHiZjxZgGnMeJmPFmAacx4mY8WYBpzHiZjxZgGnMeJmPFmAacx4mY8WYBozHiZjxZxRozBmPFnAacx4mY8WYQacx4mY8WYBpzHiZjxZgGnMeJmPFmAacx4mY8WYBpzHiZjxZgGnMeJmPFmAacx4mY8WYBpzHiZjxZgGnMeJmPFmAacx4mY8WYBpzHiZjxZgGnMeJmPFmAacx4mY8WYBpzHiZjxZgGnMeJmPFmAacx4mY8WYBpzHiZjxZgGnMeJmPFmAacx4mY8WYBpzHiZjxZgGjJlnFGjMeJmPFnEGjMGYZwGjMLTbPO2eXPjyjGGUBozHi5mPFAA0ZgzHizijRmDMM4DRmPEzHizgNGTLOINGTLOA0ZgzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZjxMx4s4DRmPEzHizgNGY8TMeLOA0ZgzDOKNGY8jMM4g0ZgzDOA0ZjyMwzgNGY8jMM4DRmDMeTOA0ZgzDOKNGY8TMM4g0ZjyMx5M4DRmPIzHkzgNGYMx5M4DRmCZjEs4oAILgKAAO259EeyEaS3Poj2QjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf/9k=', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(22:02:01)*

<details>
<summary>💭 Thinking Process</summary>

I'm reviewing the QA test frames for the Vision interface, checking that the main menu collapses to icons only, the left panel library view compresses, the right panel hides, and the canvas expands to full width at 1920×1080 with 70% zoom to show more content with smaller text, plus verifying the cyan cursor is visible.

The canvas is displaying the graph with the saved viewport's fitView applied, which leaves the nodes small and scattered vertically on the left with lots of empty black space — not ideal for a screencast composition. However, this is exactly the kind of calibration Sovereign wants to handle together; the sample demonstrates the mechanical specifications (zoom, collapse states, behaviors) and the canvas framing will be refined in the next iteration based on their example.

After clicking a single node, the right panel automatically opened showing the node details ("Cena 1 · Apresentador" with status "Concluído" and an edit button), the selected node highlighted in cyan, and the main menu stayed collapsed. Still need to check sample_12 to see the modal and hidden panel behavior.

</details>


## 🤖 Claude *(22:02:03)*

<details>
<summary>💭 Thinking Process</summary>

Frames 1 e 4 passaram na Vision QA com o menu colapsado, biblioteca e propriedades recolhidas, canvas em 70% full-width, e o RightPanel abrindo automaticamente no clique único com o inspector da Cena 1. Agora vou verificar o comportamento do duplo-clique com modal e painel.

</details>


## 🤖 Claude *(22:02:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample_12.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(22:02:12)*

<details>
<summary>💭 Thinking Process</summary>

Há um problema no frame 12 onde o duplo-clique não abriu o modal esperado — o painel direito continua visível em vez de aparecer a janela de configuração do nó. Analisando a timeline do vídeo, o duplo-clique ocorreu aos 26.7s, mas o frame 12 (que corresponde a 21.6s no tempo absoluto) não reflete essa ação ainda.

Percebo agora que meus frames de QA foram capturados antes do duplo-clique acontecer — preciso extrair novos frames em 18, 20 e 22 segundos para realmente ver o modal aparecer após a ação.

</details>


## 🤖 Claude *(22:02:13)*

<details>
<summary>💭 Thinking Process</summary>

Frame 12 está antes do duplo-clique, então meus pontos de QA não cobrem o final. Vou extrair frames do trecho após o duplo-clique.

</details>


## 🤖 Claude *(22:02:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "O=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out; for t in 18 20 22; do ffmpeg -y -ss $t -i $O/sample.mp4 -frames:v 1 $O/sample_$t.jpg -loglevel error; done; ls -la $O/sample_1*.jpg $O/sample_2*.jpg 2>/dev/null | tail -3",
  "description": "Extract QA frames after the double-click moment"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu 45634 Aug  3 19:01 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample_1.jpg
> -rw-rw-r-- 1 ubuntu ubuntu 54772 Aug  3 19:02 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample_20.jpg
> -rw-rw-r-- 1 ubuntu ubuntu 54844 Aug  3 19:02 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample_22.jpg
> ```

## 🤖 Claude *(22:02:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample_20.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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xM2jOL3s3N43WnSpqqiqffqpim05RFUxnVwvlewGlqbvGlhrp7WWeGL+/Eznx93JNeroZ4aaZvHHBHvYI4ZZRjz4cOZz0N076iK8UxGLDw58VEW48ZiqavQ617jhjUnHMxTTiicPHK9pzm3DLPME16+lqVatUxReqIw/o6abZTeLU0xEVXt2vi0dfUorq7FNMRHC0WvFo49U86dHR76K5xWwRinL+WIn67RG27encYiuacVdVtOa5mnTmeq15i9M8ImAauvXo1aenFERExEX7Nv5Kb3nnvVFUxsiWQ09fc409GKqIxUz2pwRn2J48cXbtzehgZpmIiZibTnHTnb7VAejo19zj3qKffqm2Dmm9uN8uFovls50a2tuU6OpFFERXNrdi2dtPOJvlEWrvHPe7zyAZDT1dOjSqpmimqqauNUcKcM8J4xN7MnXrbnNVdqKbTRaLads71WtGcXiMMTOUzMcdvnAHp6N63WqqmrVo05/RURaNKItMWxRlbOqI7NXMwmhXRRVVNUROWV4ir+aNuXC7TAZLWr0Z04ii14qy7NpiO1e9XPfK2c8EadelTp05R3mKM5pvGG97zxvN8uHBjgHoKdfdqY1Ym1WOuZnszeqidTSqiLza2UVXjK8y16tXQmNTKi8xlai18rRh4YbT71oi7DgOlURHCcWUc1s7Zx6JyZuNfQnUirUqx04YtTVRMxRF6L0xfbTFURzRM3hgAGcjW3bs9mmLU2zovF8FGdUWm/aivO0zmpp62jRVpVRg7NV6onTiZ41XmZm8TFpi0TdhgGRr1NOdK1qcc1TMzFERz8YyptFubh0Ou76m700fpIiasXk3vTNWnPHoimv1mJAb2vXp110TRERGGMVotneb5R0N2NfQvXOGmm8THucYxVZREcJmnDn0cWEAZLddeN3nUqzvNERTaZjPvKas5jmtHp4O862haJiii+DhNH89ovfmm83mL8IYYBlqdTQmmi8UxViqmezeIvE2veLzETbblzL97u0zbDFsV7xRF/fj9XDfs8GGAejpq3SadSq1FowXiYiKqptp37uL3iLxXM2jhMXa/fbv+lvTTnTVETFER2sMYZjyc73tEQwgDc0aoiNWJnDiotE9VUTb0xFmWjX3PFEzRTwi/6OPKpvltmmKoieaZu86Azsau7RGn2aYmKeM0XtOCL4/KvVeaZztdqU6tHt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', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(22:02:29)*

<details>
<summary>💭 Thinking Process</summary>

Estou verificando que o modal de personalização de imagem para vídeo está aberto com todas as especificações corretas — o painel direito está oculto atrás do overlay, o menu principal está colapsado, e o botão de gerar vídeo está pronto.

A calibração demonstra bem como funciona: em 1920×1080 com 70% de zoom, tudo fica colapsado, um clique abre o painel, e um duplo-clique abre o modal enquanto esconde o painel. Preciso ser honesto com o Sovereign sobre o enquadramento do canvas — ainda está usando o viewport salvo do projeto, então vamos precisar calibrar a composição de cada cena (zoom, enquadramento) com o exemplo dele como referência.

Agora vou subir a amostra para a Biblioteca dele ver através do Spaces→Assets, e depois verificar a trilha sonora.

</details>


## 🤖 Claude *(22:02:30)*

<details>
<summary>💭 Thinking Process</summary>

Frame 20 confirms the take with the "Customize · Image → Video" modal open, identity references visible, and all four specifications verified in the recording. I'm now checking the audio track and uploading the sample to the Library for your review.

</details>


## 🤖 Claude *(22:02:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/b2vvl9ihk.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	total: 406.6 s (film 393.0 + credits 13.63)
> 2	act offsets: [0.0, 47.8, 110.3, 189.2, 277.0, 349.0, 393.0]
> 3	Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
> 4	[00:00] ato 1 (bpm 78, D major)
> 5	[26.0] LIFT → cue 1 (joyful build)
> 6	[46.0] ato 2
> 7	[108.0] RESET ato 3 (bpm 100)
> 8	[188.0] ato 4
> 9	[274.0] ato 5
> 10	[346.0] ato 6
> 11	
> ```

## 🤖 Claude *(22:02:36)*

<details>
<summary>💭 Thinking Process</summary>

Preciso terminar a trilha do ato 6 que ainda falta cerca de um minuto, e enquanto isso vou subir a amostra do screencast para a Biblioteca. Vou criar um uploader simples e direto para a amostra em vez de adaptar o código existente.

</details>


## 🤖 Claude *(22:02:36)*

Trilha no ato 6 final (346s). Subindo a amostra de screencast à Biblioteca:

## 🤖 Claude *(22:02:43)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/upload-sample.ts",
  "content": "/** Upload the calibrated screencast sample \u2192 Library for Sovereign review. */\nimport { createClient } from '@supabase/supabase-js';\nimport { readFileSync, statSync } from 'fs';\n\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth: { persistSession: false } });\nconst UID = 'ada39fae-67e1-4e53-af1c-5a18e1c108e8';\nconst file = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/sc2-out/sample.mp4';\nconst key = `${UID}/takes/ep05-screencast-calibracao-v2-${Date.now()}.mp4`;\n\nconst up = await admin.storage.from('canvas-assets').upload(key, readFileSync(file), { contentType: 'video/mp4', upsert: false });\nif (up.error) throw new Error(`upload failed: ${up.error.message}`);\nconsole.log('uploaded:', key);\n\nconst { data, error } = await admin.rpc('register_creative_asset', {\n  p_user_id: UID,\n  p_kind: 'video',\n  p_storage_bucket: 'canvas-assets',\n  p_storage_key: key,\n  p_source_module: 'spaces',\n  p_is_public: false,\n  p_mime_type: 'video/mp4',\n  p_file_size_bytes: statSync(file).size,\n  p_width: 1920,\n  p_height: 1080,\n  p_duration_seconds: 24,\n  p_provider: 'playwright-screencast',\n  p_model: 'screencast-v2',\n  p_title: 'EP05 \u2014 TAKE screencast CALIBRA\u00c7\u00c3O v2 (1080p \u00b7 zoom 70% \u00b7 tudo colapsado \u00b7 clique/duplo-clique) \u2014 validar',\n  p_metadata: { take: true, for: 'validation', spec: '1920x1080@70pct, collapsed-all, click-opens-panel, dblclick-modal-hides-panel' },\n});\nif (error) throw new Error(`register failed: ${error.message}`);\nconsole.log('creative_asset id:', typeof data === 'string' ? data : JSON.stringify(data));\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/upload-sample.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:02:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/upload-sample.ts",
  "description": "Upload screencast calibration sample to Library"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> uploaded: ada39fae-67e1-4e53-af1c-5a18e1c108e8/takes/ep05-screencast-calibracao-v2-1785794567710.mp4
> creative_asset id: 1441262b-c466-4485-a0f5-4b3e1c1acb65
> ```

## 🤖 Claude *(22:02:53)*

<details>
<summary>💭 Thinking Process</summary>

Amostra na Biblioteca: asset `1441262b-c466-4485-a0f5-4b3e1c1acb65` ✅.

Aguardar a trilha terminar (~30s) e rodar o assemble. Vou aguardar via Read no output.

</details>


## 🤖 Claude *(22:02:53)*

Amostra na Biblioteca ✅ (asset `1441262b`). Aguardando a trilha finalizar para montar o A6:

## 🤖 Claude *(22:02:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for i in $(seq 1 12); do if grep -q \"OK trilha_v2\\|failed after retries\" /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/b2vvl9ihk.output 2>/dev/null; then break; fi; sleep 10; done; tail -4 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/b2vvl9ihk.output",
  "description": "Wait for soundtrack v2 generation to finish",
  "timeout": 150000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> recv stopped: 1011 None. The service is currently unavailable.
> attempt 1 failed: buffer size must be a multiple of element size — retrying in 12s
> Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
> [00:00] ato 1 (bpm 78, D major)
> ```

## 🤖 Claude *(22:05:34)*

<details>
<summary>💭 Thinking Process</summary>

A primeira tentativa falhou com o erro WebSocket 1011, mas dessa vez surgiu um novo problema: o buffer ficou com tamanho ímpar após o corte da conexão, causando um conflito ao tentar converter para int16 com reshape. O `np.frombuffer` não conseguiu processar um tamanho que não era múltiplo de 4 bytes, e tudo desabou logo no início.

Agora a segunda tentativa está rodando do zero, mas o mesmo bug vai acontecer se a conexão cair novamente em um ponto tardio com bytes ímpares. A solução é truncar o buffer para um múltiplo de 4 bytes antes de passar para o `frombuffer`. Vou deixar a tentativa 2 rodar enquanto isso, e já preparo o fix no script para as próximas tentativas — o processo atual está usando o código antigo, então editar agora não afeta o que está em execução, mas se falhar, a tentativa 3 vai usar a versão corrigida.

Espera, o retry loop está dentro do mesmo processo, então editar o arquivo não vai ajudar as tentativas seguintes do mesmo processo. Preciso decidir: deixar rodar e torcer, ou matar agora, aplicar o fix e relançar (perdendo os ~2 minutos da tentativa 2 em andamento). Considerando que já temos 401+ segundos gerados e o áudio estava praticamente completo antes da queda, perder isso por um reshape é frustrante. Vou matar o processo agora e relançar com o fix aplicado.

O problema real está no cálculo do tamanho do buffer: quando converto `int(406.6333*192000)`, obtenho 78073593, que não é múltiplo de 4 — isso causa o erro de reshape. Ah, agora vejo — na v1, o TOTAL foi 411.65 segundos, não 411.6333, o que dá 79036800 bytes (múltiplo de 4), enquanto na v2 é 406.6333 que quebra o alinhamento. A v1 funcionou porque o cálculo de TOTAL resultou em um número que, multiplicado por BPS, produzia um inteiro par.

Preciso de dois ajustes: primeiro, forçar o alinhamento de frames arredondando `n` para o múltiplo de 4 mais próximo; segundo, truncar o buffer para remover qualquer resto que não seja múltiplo de 4 antes de converter para array. Vou matar o processo, aplicar essas correções e relançar.

</details>


## 🤖 Claude *(22:05:36)*

<details>
<summary>💭 Thinking Process</summary>

Encontrei o bug real: o valor `CREDITS_S=13.6333` faz com que `int(TOTAL*BPS)` não seja múltiplo de 4 bytes (necessário para frames estéreo 16-bit), causando falha no `np.frombuffer`. Vou corrigir e relançar o script.

</details>


## 🤖 Claude *(22:05:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "pkill -f \"ep05-trilha-v2.py\" && sleep 1; pgrep -f \"ep05-trilha-v2\" || echo \"killed \u2713\"",
  "description": "Stop the running soundtrack process before patching"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 144
> ```

## 🤖 Claude *(22:05:40)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/ep05-trilha-v2.py",
  "old_string": "    n = int(TOTAL*BPS)\n    if len(buf) < n: buf.extend(b\"\\x00\" * (n - len(buf)))\n    a = np.frombuffer(bytes(buf[:n]), dtype=\"<i2\").astype(np.float32).reshape(-1,CH)",
  "new_string": "    n = int(TOTAL*BPS); n -= n % 4          # align to whole stereo 16-bit frames\n    if len(buf) % 4: del buf[len(buf) - (len(buf) % 4):]  # a mid-frame ws drop leaves odd bytes\n    if len(buf) < n: buf.extend(b\"\\x00\" * (n - len(buf)))\n    a = np.frombuffer(bytes(buf[:n]), dtype=\"<i2\").astype(np.float32).reshape(-1,CH)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/ep05-trilha-v2.py has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:05:45)*

<details>
<summary>💭 Thinking Process</summary>

O processo foi encerrado com o código de saída esperado, então o patch foi aplicado com sucesso. Agora preciso relançar a trilha usando o script corrigido.

</details>


## 🤖 Claude *(22:05:45)*

Processo antigo morto (exit 144 = o pkill, esperado) e patch aplicado. Relançando:

## 🤖 Claude *(22:05:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && export GEMINI_API_KEY=$(curl -s \"$SUPABASE_URL/rest/v1/decrypted_user_api_keys?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=google_api_key\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | python3 -c \"import json,sys; print(json.load(sys.stdin)[0]['google_api_key'])\") && python3 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/ep05-trilha-v2.py 2>&1 | grep -v \"ExperimentalWarning\\|async with client\"",
  "description": "Regenerate soundtrack v2 with frame-alignment fix (background)",
  "run_in_background": true
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Command running in background with ID: bwyqpsoly. Output is being written to: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/bwyqpsoly.output. You will be notified when it completes. To check interim output, use Read on that file path.
> ```

## 🤖 Claude *(22:06:11)*

<details>
<summary>💭 Thinking Process</summary>

A trilha está sendo relançada enquanto aproveito para organizar o trabalho: preciso mover os scripts de produção do EP05 que estão em /tmp (voláteis) para o repositório em `scripts/ep05/`, consolidando os scripts principais como assemble, trilha, title e screencast — isso garante durabilidade e segue meu princípio de transformar qualquer coisa que faço duas vezes em uma skill reutilizável.

A sessão anterior deixou tudo em scratchpad, então um reboot perderia 1.9GB de mídia e scripts; a mídia grande fica lá, mas os scripts vão pro repo. Quanto aos componentes do master (n_film, speech5, etc.), alguns são regeneráveis com custo (n_film vem dos 32 segmentos no bucket), enquanto outros são críticos: os screencasts antigos não são fáceis de refazer, o title10s_final já está na Biblioteca como asset, e o master_A5 é a única cópia local (mas será superado pelo A6 que subirá à Biblioteca). Então a prioridade é: scripts para o repo, mídia fica no scratchpad, e o A6 vai para a Biblioteca.

Vou copiar os scripts principais (ep05-trilha-v2.py, assemble-v6.ts, screencast-v2.ts, upload-a6.ts, render-title.ts) junto com o title.html para o repositório.

Enquanto a trilha gera, vou fazer o assemble, QA, e depois upload do A6. Os paths nos scripts apontam para scratchpads — vou deixar como estão com uma nota no topo explicando que são runners pontuais de produção. Também preciso commitar o patch do CanvasEditorPage (já deployado) com a mensagem sobre o node click surfaces, mas vou fazer commits granulares: o patch de UX agora, e os scripts depois que o A6 for validado.

</details>


## 🤖 Claude *(22:06:13)*

<details>
<summary>💭 Thinking Process</summary>

A trilha foi relançada. Enquanto ela gera, vou trabalhar em dois itens: fazer commit do patch do canvas que já foi deployado e testado, e mover os scripts de produção do EP05 do diretório temporário para o repositório para evitar perda de dados em caso de reboot.

</details>


## 🤖 Claude *(22:06:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git add src/pages/CanvasEditorPage.tsx && git commit -m \"feat(canvas): clique no n\u00f3 abre o painel de propriedades; duplo-clique cede ao modal\n\nDire\u00e7\u00e3o Sovereign 2026-08-03 (calibra\u00e7\u00e3o de screencast EP05): clicar um n\u00f3\nreabre automaticamente o RightPanel colapsado; duplo-clique abre a janela de\nconfigura\u00e7\u00e3o E esconde o painel (canvas>node>janela, Amendment 31 refinada).\nProvado por grava\u00e7\u00e3o 1920x1080@70% + Vision QA (take 1441262b na Biblioteca).\" && git log -1 --format=%H",
  "description": "Commit the canvas panel behavior patch"
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
> [90m7:06PM[0m [32mINF[0m 1 commits scanned.
> [90m7:06PM[0m [32mINF[0m scan completed in 7.09ms
> [90m7:06PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.06 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.02 seconds)
> ✔️ gitleaks-staged (0.05 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> [main a131f3e] feat(canvas): clique no nó abre o painel de propriedades; duplo-clique cede ao modal
>  1 file changed, 8 insertions(+), 5 deletions(-)
> a131f3e19aedd08f535bf28cfbcb24dfac9b7fc6
> ```

## 🤖 Claude *(22:06:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "mkdir -p /home/gcrUX/htdocs/constellation-orchestra/scripts/ep05 && SP=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad; MY=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad; cp \"$SP/render-title.ts\" \"$SP/title/title.html\" \"$SP/cartela-creditos.py\" \"$SP/assemble-v3.ts\" \"$SP/ep05-trilha.py\" scripts/ep05/ 2>/dev/null; cp \"$MY/ep05-trilha-v2.py\" \"$MY/assemble-v6.ts\" \"$MY/screencast-v2.ts\" \"$MY/upload-a6.ts\" scripts/ep05/; ls -la scripts/ep05/",
  "description": "Promote EP05 production scripts from volatile scratchpads into the repo"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 84
> drwxrwxr-x  2 ubuntu ubuntu  4096 Aug  3 19:06 .
> drwxrwxr-x 12 gcrUX  gcrUX  12288 Aug  3 19:06 ..
> -rw-rw-r--  1 ubuntu ubuntu  7261 Aug  3 19:06 assemble-v3.ts
> -rw-rw-r--  1 ubuntu ubuntu  4868 Aug  3 19:06 assemble-v6.ts
> -rw-rw-r--  1 ubuntu ubuntu  4795 Aug  3 19:06 cartela-creditos.py
> -rw-rw-r--  1 ubuntu ubuntu  8718 Aug  3 19:06 ep05-trilha.py
> -rw-rw-r--  1 ubuntu ubuntu  8771 Aug  3 19:06 ep05-trilha-v2.py
> -rw-rw-r--  1 ubuntu ubuntu  1672 Aug  3 19:06 render-title.ts
> -rw-rw-r--  1 ubuntu ubuntu  7865 Aug  3 19:06 screencast-v2.ts
> -rw-rw-r--  1 ubuntu ubuntu  3949 Aug  3 19:06 title.html
> -rw-rw-r--  1 ubuntu ubuntu  1705 Aug  3 19:06 upload-a6.ts
> ```

## 🤖 Claude *(22:06:24)*

<details>
<summary>💭 Thinking Process</summary>

Commit `a131f3e` is done and cleaned up with gitleaks, the 9 scripts in scripts/ep05/ are ready, so now I need to write a brief README for that folder and commit it, then check the trail afterward.

</details>


## 🤖 Claude *(22:06:24)*

Commit `a131f3e` ✅. Escrevendo o README da pasta de produção e selando:

## 🤖 Claude *(22:06:39)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/ep05/README.md",
  "content": "# EP05 \u2014 runners de produ\u00e7\u00e3o do master (2026-08-03)\n\nRunners pontuais da produ\u00e7\u00e3o do master EP05 (\"EU N\u00c3O EXISTO\"), promovidos dos scratchpads\nde sess\u00e3o (vol\u00e1teis) para o repo. M\u00eddia grande N\u00c3O vive aqui \u2014 segmentos/masters ficam na\nBiblioteca (`canvas-assets` bucket) e no workdir de sess\u00e3o; estes scripts REGENERAM tudo.\n\n> \u26a0\ufe0f Paths de workdir apontam para o scratchpad da sess\u00e3o que os rodou \u2014 ajustar `WORK`/`W`/`OUT`\n> ao reexecutar. Credenciais: `.env` do repo (`SUPABASE_URL`/`SB_SECRET_KEY`) + `google_api_key`\n> per-user do User 0 via `decrypted_user_api_keys` (Lyria).\n\n| Script | Papel |\n|--------|-------|\n| `ep05-trilha-v2.py` | Trilha Lyria RealTime v2 \u2014 FELIZ/ESPERAN\u00c7A, D maior, cues joyful, bpm 78\u2192100\u2192106. Timeline SEM intro (o VFX t\u00edtulo tem sound design pr\u00f3prio; o mix aplica adelay +10s). Fix: alinhamento do buffer a frames de 4 bytes (queda 1011 no meio de frame + `int(TOTAL*BPS)` fracion\u00e1rio quebravam o `np.frombuffer`) |\n| `ep05-trilha.py` | Trilha v1 (hist\u00f3rico \u2014 misteriosa/\u00e9pica, F maior, INTRO_S=5) |\n| `assemble-v6.ts` | Master A6 = VFX t\u00edtulo 10s (som pr\u00f3prio) + filme 393s + cr\u00e9ditos 13.63s; speech5 re-timado (trim 5s\u2192+10s), trilha v2 ducada (sidechain), loudnorm \u221216 LUFS, QA por janelas + frames |\n| `assemble-v3.ts` | Montagem A3 (hist\u00f3rico \u2014 receita da timeline narra\u00e7\u00e3o-dirigida + duck) |\n| `render-title.ts` + `title.html` | VFX t\u00edtulo 10s APROVADO (GSAP determin\u00edstico + Playwright frame-seek 300 PNG \u2192 MP4, t\u00e9cnica HyperFrames) \u2014 asset `b7da3f30` |\n| `cartela-creditos.py` | Intro \"GABRIEL AI APRESENTA\u2026\" + cr\u00e9ditos rolando (Liberation Serif = Times, replica motor GabrielAI) |\n| `screencast-v2.ts` | Screencast CALIBRADO (Sovereign 2026-08-03): 1920\u00d71080 com navegador a 70% (viewport 2743\u00d71543 \u2192 record 1920\u00d71080), tudo colapsado (menu/biblioteca/propriedades), clique\u2192painel abre, duplo-clique\u2192modal+painel cede; n\u00f3s localizados por boundingBox real; setup cortado do take |\n| `upload-a6.ts` | Sobe o master \u2192 `canvas-assets/<uid>/masters/` + `register_creative_asset` |\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/ep05/README.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:06:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git add scripts/ep05/ && git commit -m \"chore(ep05): promove runners de produ\u00e7\u00e3o do master ao repo\n\nScripts da produ\u00e7\u00e3o EP05 (trilha Lyria v2 feliz/esperan\u00e7a D-major, assemble A6\ncom VFX t\u00edtulo, render do t\u00edtulo GSAP, screencast calibrado 70%, uploader)\nsa\u00edam de scratchpads vol\u00e1teis em /tmp \u2014 um reboot perderia o ferramental.\nM\u00eddia continua na Biblioteca; scripts regeneram tudo.\" -q && git log -1 --oneline; tail -3 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/bwyqpsoly.output",
  "description": "Commit EP05 scripts; check soundtrack progress"
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
> [90m7:06PM[0m [32mINF[0m 1 commits scanned.
> [90m7:06PM[0m [32mINF[0m scan completed in 35.4ms
> [90m7:06PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.12 seconds)
> ✔️ e2e-output-tripwire (0.03 seconds)
> ✔️ secret-scan (0.05 seconds)
> ✔️ gitleaks-staged (0.10 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> 6cca46b chore(ep05): promove runners de produção do master ao repo
> Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
> [00:00] ato 1 (bpm 78, D major)
> [26.0] LIFT → cue 1 (joyful build)
> ```

## 🤖 Claude *(22:06:55)*

<details>
<summary>💭 Thinking Process</summary>

Commit 6cca46b is done with the initial track running (26 seconds with LIFT applied), leaving about 6-7 minutes remaining. While waiting, I should push these two commits to origin/main since the rule is that running code isn't the same as delivering it—the previous session always pushed. After that, I'll monitor the track completion and then move on to assemble-v6 and QA.

I'm checking if assemble-v6.ts references my scratchpad paths—it doesn't, OLD correctly points to the old scratchpad, and the gates verify trilha_v2.wav in the right location. Pushing now.

</details>


## 🤖 Claude *(22:06:55)*

Commit `6cca46b` ✅, trilha regenerando (LIFT aplicado aos 26s). Entregando os commits ao destino (push):

## 🤖 Claude *(22:06:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git push origin main 2>&1 | tail -2 && git log origin/main -1 --oneline",
  "description": "Push commits to origin/main and verify"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> To github.com:gabrielZarattini/constellation-orchestra.git
>    3d49efc..6cca46b  main -> main
> 6cca46b chore(ep05): promove runners de produção do master ao repo
> ```

## 🤖 Claude *(22:07:02)*

<details>
<summary>💭 Thinking Process</summary>

Pushing the changes now, then I'll wait for the pipeline to complete—about 6 minutes left. I'm going to poll for the "OK trilha_v2" status or any failures, then proceed with the assembly once it clears.

</details>


## 🤖 Claude *(22:07:02)*

Push verificado no destino ✅. Aguardando a trilha completar para montar o master:

## 🤖 Claude *(22:07:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "OUT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/bwyqpsoly.output; for i in $(seq 1 48); do if grep -q \"OK trilha_v2\\|failed after retries\" \"$OUT\" 2>/dev/null; then break; fi; sleep 10; done; tail -6 \"$OUT\"; ls -la /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/trilha_v2.wav 2>/dev/null || echo \"trilha_v2.wav ainda n\u00e3o existe\"",
  "description": "Wait for soundtrack v2 to complete (up to 8 min)",
  "timeout": 510000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [26.0] LIFT → cue 1 (joyful build)
> [46.0] ato 2
> [108.0] RESET ato 3 (bpm 100)
> [188.0] ato 4
> [274.0] ato 5
> [346.0] ato 6
> trilha_v2.wav ainda não existe
> ```

## 🤖 Claude *(22:15:13)*

<details>
<summary>💭 Thinking Process</summary>

O poll de 8 minutos expirou enquanto a trilha estava no ato 6, chegando a 346 segundos — estou perto do alvo de ~401 segundos mais créditos até o buffer de 412 segundos. O processo continua em execução, então preciso aguardar mais um ou dois minutos.

</details>


## 🤖 Claude *(22:15:13)*

Quase lá (ato 6 aos 346s de 412s). Aguardando o trecho final:

## 🤖 Claude *(22:15:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "OUT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/bwyqpsoly.output; for i in $(seq 1 24); do if grep -q \"OK trilha_v2\\|failed after retries\" \"$OUT\" 2>/dev/null; then break; fi; sleep 10; done; tail -4 \"$OUT\"",
  "description": "Wait for final act + credits of soundtrack v2",
  "timeout": 260000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [346.0] ato 6
> [390.0] ato 7
> recv stopped: 1011 None. The service is currently unavailable.
> OK trilha_v2.wav  406.6s
> ```

## 🤖 Claude *(22:16:10)*

<details>
<summary>💭 Thinking Process</summary>

A trilha_v2.wav processou com sucesso nos 406.6 segundos completos — o erro de queda que aparecia perto do final foi contornado pelo ajuste de alinhamento, garantindo que todos os 7 cues foram aplicados corretamente com os créditos, padding e fade cobrindo tudo. Agora vou rodar o assemble-v6.

</details>


## 🤖 Claude *(22:16:12)*

<details>
<summary>💭 Thinking Process</summary>

A trilha v2 está pronta em 406.6s com todos os 7 cues aplicados, e o fix de alinhamento resolveu o problema da queda 1011. Agora vou montar o master A6.

</details>


## 🤖 Claude *(22:16:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/assemble-v6.ts 2>&1 | tail -20",
  "description": "Assemble master A6 (VFX title + film + credits, new soundtrack ducked)",
  "timeout": 600000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ title10s_final.mp4 10.00s
> ✓ n_film.mp4 393.00s
> ✓ n_cred.mp4 13.63s
> ✓ speech5.wav 411.63s
> ✓ trilha_v2.wav 406.61s
> A6 total target: 416.63s (title 10 + film 393.00 + cred 13.63)
> speech6.wav 416.63s
> trilha6.wav 416.63s
> final6.m4a 416.70s
> video6.mp4 416.67s
> 
> === MASTER A6 === 416.67s 54.6MB
> vol[title 0-10]: [Parsed_volumedetect_0 @ 0xb9d9fd1eafe0] mean_volume: -17.4 dB [Parsed_volumedetect_0 @ 0xb9d9fd1eafe0] max_volume: -1.4 dB
> vol[opening 10-30]: [Parsed_volumedetect_0 @ 0xc087a74ebfe0] mean_volume: -20.1 dB [Parsed_volumedetect_0 @ 0xc087a74ebfe0] max_volume: -1.5 dB
> vol[mid 200-220]: [Parsed_volumedetect_0 @ 0xb33ad722bfe0] mean_volume: -19.0 dB [Parsed_volumedetect_0 @ 0xb33ad722bfe0] max_volume: -1.4 dB
> vol[credits]: [Parsed_volumedetect_0 @ 0xbc70cedaafe0] mean_volume: -22.6 dB [Parsed_volumedetect_0 @ 0xbc70cedaafe0] max_volume: -9.9 dB
> QA frames: qa6_{2,6,12,60,200,350,408}.jpg
> ```

## 🤖 Claude *(22:19:37)*

<details>
<summary>💭 Thinking Process</summary>

Checking the master A6 mix at 416.67 seconds with healthy loudness levels across all sections, and I need to review the quality assurance frames for visual effects, the title sequence, the opening scene, and credits to address three critical issues.

</details>


## 🤖 Claude *(22:19:38)*

<details>
<summary>💭 Thinking Process</summary>

Master A6 is mounted with a duration of 416.67 seconds and file size of 54.6MB, showing healthy loudness across all windows. I'm now performing visual QA checks on the key frames.

</details>


## 🤖 Claude *(22:19:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/qa6_6.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '/9j//gAQTGF2YzYwLjMxLjEwMgD/2wBDAAgMDA4MDhAQEBAQEBMSExQUFBMTExMUFBQVFRUZGRkVFRUUFBUVGBgZGRscGxoaGRocHB4eHiQkIiIqKiszMz7/xACXAAEBAAIDAQEAAAAAAAAAAAAAAQIHBQQDCAYBAQEBAQAAAAAAAAAAAAAAAAABAgMQAQACAQIDAwUKCAsHBQEBAAABAgMRBDEFIUESBlFhE3GBsnKxc5E1oRQiMmKiI1LBQrM0M5OSwtGD0/DSgqNTFpRDVGMV43QkRCXh8REBAQEBAQEBAQAAAAAAAAAAAAERMQJBIRL/wAARCALQBQADASIAAhEAAxEA/9oADAMBAAIRAxEAPwDQIAAAAAAAAAAAAAAAAAAAAAAAAAAACgAAAAAAAAAAAACCgIKAgAAAAoCKAAAAAAAAAAAAAAAAAAACKAgoCCgIKgAAAKCCgAAAAAAAAAAAAAAAAAACKAgKCAAAAAACoAoAAAAAAAAAAAAAIqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKigAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoICggoCAoIAAAAKgAAAAAAAKCAAAAAAAAAoIqKCKAIKAgqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAAAAAAAAAAAAAAAAAAAAAAAACggAAKCCgIoAAAAAAAAAAAIoCCgIKAgoAIoCCgIoCCgIKAAAAAAAIoAAAACKACKAgoCCoAAACggAAAAAAAAAAAAAAAAAAAAACCggAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAAAAAAAAAAAAKgAKCCgIKgAoCKAAAAAAAAAAAAoCAACgIogAqACgIogAqACoACgAAgKCAoIKAIoCCgIAAoAgoAioAKgAqAAAAAAAAAAAigCCgIKAgoCAAAACoAKgAAAAAAAACKAgAAAAqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoIAAAAoAAAAAAAAAAoAACKAAAAAigAAAAAAAAAAACggoCKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACKAgoAgoICggAAKCAAIoAAAAAAAigAACKgAqAAAAAAAAAIoCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoIAAAAAAoAAAAAAAAAAoCKAqAACggAAqAKACKAAAAAigAAAAAAACggKCCgIKAigAioAKAigAigIKAAAIoCKAIKAgoAAAigIKAAAIoAigIKAgqACoAAAAAAAAAigIoAAAgqAoACCgIAAAAAIKgAAAAAAAAAAIKgAAKioAAAAAAAAAAAAAAAAAAAAAAAAAqAAACgAAAAAAACgiooAAAAKigAAAAAAAAAqAAAAACoAKAigAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCgCKAgoCCoACggAAAAAAAAAAACKgAAAAIKgAAAAAAAAAAIKgCoAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAAAAAAAKAAAACgAACoAAAqKCAoIqKCKAAAAAAAAAAAAKCCgIoAigAAAAAAAAAACCgAAIKAigAigAAAAAAIoAAAAAAAAAIoCCgIKgAoCAAAAAAAAAAIoCAoIKAgoCCoAAAigIAAKgCKAgoCAAAAAAAAgqAAoIAAAAAAAAAAAAAAAAAAAAAAoAAAAAAAKigigAqAKigAAAACgAAAAAAAAAAAAACgigCKACKAAAAAAAAACoAAAKAgKCAAAAAoIKAgoCCgIKgAAAAAAAoCCgIAAKgAAAAAAAACKAAAgoCAoIKgAAAAAAAAAACKgAAAACKAgACKAgqACoAAAAAACCoAAAAAAAAAAAAAAAAAAAAAoAAAAAAAKigigACgCKAAAACgAAACoACgAAgoAAAAAAAAAAAAAAAoAgoAACKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIKAIqAAAAAAAAAAAIoAACKACKAgKCCgIKgAAIAAACCgIAAAAgAqKgAAAAAAIKgAAAqAAAAAAAAAAAAAKAAAAAAKAioCgAKgCgAAAAAoAAAKAAAAAAAAAAAAAACggoCKAAAAAAAAAAqACgIKAgqACoCooACACgIKAgoCKAIKAgKCCgICgIoCAoIKAgqACoAAAAAAAACCgIoAgKCAAAAAAAAAAIoAioAAAigIAAAAACCgIAAgoIAAAAAAACCgIAAAAAAAAAACgAAAAAAAoIoAAAKigigACggoAAAAACgAAAAqCgAAgoAAAAAAAAAAAoAiooIKAAAAAAAAoIAAAAAAKgAqAAAAAAAAAAACgIAAKAgKCAAAAAAIoAigCKAgoCAAAAAAAAAAIoCCgIKgAAAACKgAAAAIKgAAAAIqAAAIKgAKCAAAAAAIoCAAAAAACgAAAAAAAAKAAAAKAgKAAAqKAAAAAoAAAAoIKAigAAAAAAACgigAAAAAAAKgAoCCgIKAAAAAAAAoICggAAAAqACgICggqAAACoAAACggAAAAAAAIKAgoCAAAAAAAAAgAoCAAAAAAIoAioAKAgAAAIAAACCgIACKAIKgAACKgAAAAAAAAAAIoAigAAAAAAACgIqACgAqAoAAAAoAAAAAoAAAAAKAAAAAAAAACooAAAAAAAKCKigigAAAAAAoAoICggoAAAAgAKAAAAAAAAAAAAAAAAAAIKAAgAqACiCAKACAAAioAAAAAAAAAigIKgAAAAAAIKgAoCAAgoCAAAAIoCAAAAgAAICoqAAAAAAAAAAAAAAAAAAACgAAAACgAAACgigAAAKAAAAAKAAAAAAACgCKAAAAAAAAoCKAAAAAAKogoCKKCCgIAAAACggKCCoAKAgoAigIKAgoAigIoAgAAKCAAIoAigAAICggAACAAAAAigIKAgAAAIoAgoCAAAAAAIoCAAAAIqAAAAAgqAAAIqACoCCgIKgAAAAAAAAAAAAAACoAoACooAgCgAKAAKCCgAKCAACiiKCAACgAAAAAKigAAAAqKAiqigKAgqIAqAKooCgIKIIMkUEUBBUBFAEUAAUEAAFAQVAAAAAAABQEFAQUBBQERQEFAQUBAUEFARGSAAIIKigKiAjIBEVAAUEBVEFRARUBUFBBQERkgIKgIMkARUABQQAEFAQABFAQAAEAVAAEAAAAAAAAAAAAAAAABQAFQBQAFFBFAAFURQARQEUEAUURRQQUBUVQYigCKAgqICooKAoAqDFkKoxFAQZIAigCooAq6AgyFRBdFBijJAYiogIoKCgIKACgMRkAxVUBNEVQQAEVQEUAAUEFAYiiiIyRAAAFAQUBAUEBVGKKIIKAgoCC6IAi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QAFGLIGSsAGTJiaqjJEQGSDEGSGrEFViAyGKislYAjIYgMhgAyGIDJGICiAKMVBVYgqiAMhiCKMRBUBRRgoCoIrJEFFRAQEEAQFUQBVYgKIACAAIAiogIAIAACAqAAAAAAioCgAAAAAAAKAAAKIoKIoCooCoKKIAoAACAqKArFVFEAZjEBkiAKgIAACoAqoKKIoCoIKIKCiAogCiAKqAMhiAyGKgKiAogDJEUFEAZIgDIYgKrEBRAAQAVAGQigCAMhiAyEAUQAQAAQFVEBVRAZDEBkMVBAQFAABAVABUEBVQQVAUBAARUAEUVEZICCKAAAIgAKCsRBQFAQABEFQAVBAEAAABAAAAAAAAAAAAAAAAABRAFAABQAAVWKgKgAqAMkRQVAAVAFEUBUAZIAKgAAAoigAAAAKgCgAAKAACoIKIoAAKIKKrEBUAFQAUAARQUQBUABUAAAAAAAAAUQBRAFEAUQABAAAFQBkiACoIKIKCKAgKggAACgCIKIAogAAAAAioAACoIAAAACAAAAAACAAAIAAAAigIAACACoAAAAAAAAAAAAAAACgAAKgCgAAAoAAACooAAAAKgAoAKAAAAAACgAgKAAAAACiAKAAAAAAqCiiKAAAAAAAACoKCKgCiAKIAoAAAAAAigAgCoAqACiAAAAAAICgACAKgIAAAAAAICggAAAAAAICoAAAAACKgAACAAAAAACAAAAAgAAACAAAAgAAAAAAAAAAAAAAAAAKigAAAAKigAAKigAAKAAICgAAAKAKIoAAAAAAAAKgAoAAAAAAACgAAAAAAoAIKIAoigCKAAoAAAAAAAAAAAAAAAAAIACgAAAgAAAKIAAAAAAAgAgKIAqAAAACAqAAAAAAAAACAAAAgAAAAACAAACCoAKgAACKgAACKgAAAAAAAAAAAAAAAACoAoAAAKIoAICqgCiKCoACoAoICgAKgCiKAqAKIAoigAAAgMhAFEAUQBQAVAAABRAFEAUQBRFAAUFQQAAFQBUAFEAUQUUQBRNQFEAUQBRBBRAFQABFAAUFQQBAFEAVABRAAEBQAEAFEAVAAVAARQBAFEAVAAABAAAABAFEAVAAAAQAAABAAAAABFQAAAAAAAAAQBQAAAAAAAVAAAAVFAVAFEUAABUAUQBQAAAFRQAAAAUQAVAFEAUAAAAAAABUAUQBRAFEUAEBQAAAVABUAAAAAAAAABUAAAFQAAAAAVAAAAAFQAVAAAAAAEAUEBRAFEAAAAAAAAAAAAQFEUBAAAAAAQAAAAAAQAAAAAQAAABAAAAAAAAAAAAAAAQVAFQBRAFAAAAAAAAAAVFAABRFAEUAAFEUAABUAUAAEBQAAAAAAAAAFQBRAFEUAAAAAAAAAAFEAUQBRAFEAUEBRAFEUAQBRAFEAUQBRFAEUAEBRABUAUQAVABUAAAAAAAAAAQFEAVAAABUAAAAAAAAAAEAAABAUEAAAAAQAAAEAFQAAAAAAAAAAABAFABAAAAAAAAURQAAAAAAAUEVFAAAVFAEUAABUAUAAAFQAVABUFAEAUAAAAAAAAABUAAUARQAAAQFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAFQAAAAAAAAAAAAAAABAUQBUAFQAVAARUAFQAAAEBUAFQABFBFQAAAAAAAAAEAAAAAAAAAAAAAAAVBQBAFAAAAAAAAVAFAAABRFAAAABQQFEUAAAAAAAAFQAFQBRAFAAAAAAAAAAAAAAAAVAFQAAAUQAABRAAAFQAVAAVABUAVAAABUAFEAAAAAAAAAAAAAEVAVABRAAAAAAAAAAAAAAQAAAAAABBUAABAAAAAAAAAAAQFQUEAAAAAAAAAAAAAAAAAAAAVAFAAAAAAVAAAFEUAAFQAUABUAVAAVAFQAUQBQAAAAAAAAAAAUQBRAFEAURQAAAAAQFAABAUAAAARQAQFEUAAAAAAAAAAAAAEBQAAABAFEAFQAVAAAAAAAAAARQAQFEAUQBUAAAAAEUQAAAEBUAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAVAFAAAAAAAAABRFAAAVAFAAAAEUAAAAAAAAAAFEAUQBRFAAAAAAAAAAAAAAAAAAAAAAAAAAAVABUAAAAAAAAAFQBUAAAAAAAAEBQABAFEAUQAVAFQAAAAAAAAAAAEABUAAAAQAAAAAAAAAABFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAUAAAAAAABUAFQBRFAVAFQAVABRAFEUAEBQABFAEUAEBQAAAAAFQBRAFEAUQBRFAEUARQAQFAAEAUQBRAFAAEAUAARQAAAABFAEUAQAVAAAAAAAAAARQAQFBAUAEFAQVAUQBUAAAAABAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUBRAFAAAAAAAAAAABQAAQFAAAAAAAAEUAAAAAAFQAFQBQABFAAAAAABUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBUVAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABQAAAAAAAAAAAAAAAAAFQAVABRAUQBQAAAAAAAAAVAAVAFEAUQAVAAFBAUARQQAFRUBUAAAFRUBUAAUARUAVFAEAUQAVFBFQAAAAAAABAUAAEBQAEVAUQAAAAAVABUAVAAAAAAAAAABAVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAVABUAFQBRFAEAUAAAAAAAAAAAAEBQAAQFABFAAAARQAAAAAAAAAAAAAAAQFEAUQBUAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAVBQBAFEAFQBRAFEAAAFQAAAAAVAAABUAAAAAUQBRAFEUBABRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBUAAVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFQBUABUAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVAFQAAAUAAAAAAAAAAAAEBRAAAAAFQAAAUQBQAAAAAAAAAAAAAAAAAAABAFQAUQAABRAFEUAAAAAAAAAAAAAAAAAAAEBUAFQAAAFQAVAFEAUAAAAAAAAAAAAEAAAAAAAFQAAAAAAAAAAAAAAAAAAAAH//2Q==', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(22:19:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/qa6_12.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(22:19:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/master/qa6_408.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '/9j//gAQTGF2YzYwLjMxLjEwMgD/2wBDAAgMDA4MDhAQEBAQEBMSExQUFBMTExMUFBQVFRUZGRkVFRUUFBUVGBgZGRscGxoaGRocHB4eHiQkIiIqKiszMz7/xACpAAEAAgMBAQEAAAAAAAAAAAAABQYHBAMCCAEBAQEBAQAAAAAAAAAAAAAAAAABAgMQAQACAQMCAwQECQcIBQwCAwACAQMRBBIFITETQVEiBmEUgTJxcnOzkaGyUjUjM3Q0YhVCB7G0VBY206OC0pRDgyTBhMNE0VVTomMlk5JGZMJF8BEBAQACAAUDBQEBAQAAAAAAAAERAkExIWESoYFRccGxIpFi0fH/wAARCALQBQADASIAAhEAAxEA/9oADAMBAAIRAxEAPwD5/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(22:19:47)*

<details>
<summary>💭 Thinking Process</summary>

Checking the Vision QA frames for the project — the opening title sequence with the serif glow effect is locked in, the transition from VFX into the film at the 12-second mark lines up correctly with Gabriel AI's introduction and the flame overlay, and I'm verifying the credits section timing.

</details>


## 🤖 Claude *(22:19:48)*

<details>
<summary>💭 Thinking Process</summary>

Vision QA passou nos três pontos verificados: abertura com VFX, transição para a cena 1 e créditos finais. Agora vou fazer upload do master A6 para a Biblioteca.

</details>


## 🤖 Claude *(22:19:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/scratchpad/upload-a6.ts",
  "description": "Upload master A6 to the Library",
  "timeout": 300000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> uploaded: ada39fae-67e1-4e53-af1c-5a18e1c108e8/masters/ep05-master-A6-1785795589792.mp4 54.6MB
> creative_asset id: a9fceee1-3360-4563-b3d1-cd9a8239e03b
> ```

## 🤖 Claude *(22:20:12)*

<details>
<summary>💭 Thinking Process</summary>

Master A6 is now in the library as a 54.6MB asset, with the remastered version including the VFX, film, and credits all assembled together. The happy, hopeful soundtrack in D major with joyful cues is integrated into the final cut.

The screencast patch for click/double-click behavior has been implemented, deployed, and committed, with a 1920×1080 sample at 70% quality now stored in the library. Scripts have been promoted to the repo and pushed, and I've answered the user's question about recording—clarifying that they should provide an example of what they want captured rather than recording everything themselves.

The only remaining gate is the Sovereign's review of the audio track and visual quality of A6, plus final screencast calibration using their example. The old master has been replaced by A6 in the library, though the local copy of A5 is still available for comparison if needed.

</details>


## 🤖 Claude *(22:20:25)*

**Master A6 na Biblioteca ✅** — asset `a9fceee1` (54.6MB). Turno completo; resumo do que foi entregue:

═══════════════════════════════════════════════

## 🎬 EP05 — o que está pronto para seu parecer

**1. MASTER A6 re-montado** → Biblioteca: **"EP05 — MASTER A6 (VFX título 10s + trilha v2 FELIZ/ESPERANÇA D-major)"**
- O master apagado tinha cópia local intacta no host — nada foi regenerado com custo, só re-montado.
- Estrutura: **VFX título 10s aprovado** (com o sound design próprio dele preservado) → filme 393s → créditos 13.6s = **416.7s**.
- A cartela antiga de 5s saiu (o VFX já contém o "GABRIEL AI APRESENTA…").
- Vision QA aprovado nos 3 pontos (título · transição para a cena 1 · créditos); loudness saudável em todas as janelas.

**2. Trilha NOVA (v2) — feliz e esperançosa**, já dentro do A6:
- **Ré maior** (tom clássico de brilho/triunfo, vs. o Fá da antiga), bpm 78→100→106, todos os cues reescritos: abertura *warm hopeful* (zero mistério sombrio), lift alegre aos 28s, atos crescendo em *radiant/uplifting*, finale *hope fulfilled* **sem braams/trovão**, créditos *warm afterglow*.
- Achei e corrigi um bug real no gerador: queda do WebSocket no meio de um frame de áudio + total fracionário quebravam o buffer — o fix salvou a geração completa (406.6s, 7 cues aplicados).

**3. Screencast — calibração** → Biblioteca: **"EP05 — TAKE screencast CALIBRAÇÃO v2"** (24s)
- **1920×1080 com navegador a 70%** (técnica: viewport 2743×1543 gravado em 1080p — nítido e exato), menu principal / biblioteca / propriedades **tudo colapsado**.
- O comportamento que você especificou **não existia no código** — implementei: clique no nó → RightPanel abre sozinho; duplo-clique → modal abre **e** o painel se esconde. Deployado, provado na gravação (commit [a131f3e](https://github.com/gabrielZarattini/constellation-orchestra/commit/a131f3e)).
- A v1 era ruim porque gravava em 720p, zoom 100%, nada colapsado e cursor com coordenadas cegas — a v2 localiza os nós por posição real.

## 📤 Sobre você gravar o exemplo — sim, faça

Um exemplo seu da cena 1 me ensina o que a descrição não ensina: **ritmo do mouse, pausas, o que enquadrar, quando dar zoom**. Grave e suba pelo **menu Cortes** (`/dashboard/repurpose`) ou **Spaces→Assets** com título "REF screencast cena 1" — eu estudo frame a frame e replico o padrão nas outras ~20 cenas. A amostra v2 na Biblioteca já mostra a mecânica calibrada; o que falta calibrar com seu exemplo é a **direção** (enquadramento e tempo de cada cena).

## 🧾 Provas materiais
- Assets: master `a9fceee1` · take screencast `1441262b` · (VFX `b7da3f30` intacto)
- Commits pushed `3d49efc..6cca46b`: patch do canvas + runners promovidos a [scripts/ep05/](scripts/ep05/README.md) (estavam só em `/tmp` volátil)
- tsc-app **0** · gitleaks limpo · build deployado com env baked verificado

**Próximo gate (seu):** ouvir a trilha do A6 e dar o parecer (feliz o bastante?) + gravar o exemplo da cena 1 para eu calibrar o lote inteiro.

## 👤 User *(22:20:37)*

eita então perdemos um monte de coisa pois o handoff não esta preparado para recuperar ou sintetizar os scratchpad e todos os aprendizados depois dos testes e validação minha nas sessões certo? Precisamos concertar isso e fazer esse aperto de mãos de aprendizado continuo. E principalmente atualizar os agentes, o agente dentro do spaces, o outro que criamos tambem para hyperframe. 

Falando nisso outra frente super importante, é que não estou sentindo muita qualidade de evolução continua no openclaw e penso em talvez migrar 100% do openclaw para o hermes. O que você acha? Pois vi muito por ai na internet empresas fazendo isso.

## 🤖 Claude *(22:21:31)*

<details>
<summary>💭 Thinking Process</summary>

Sovereign está apontando um problema crítico: o handoff atual não consegue preservar ou sintetizar os aprendizados dos scratchpads, perdendo informações valiosas após testes e validações. Ele quer implementar um "aperto de mão de aprendizado contínuo" que capture e mantenha esse material, o que significa atualizar o protocolo de handoff.

Na verdade, nesta sessão específica não perdemos nada — recuperei tudo do /tmp — mas foi sorte: o host não reiniciou. O protocolo simplesmente não cobre isso, então preciso ser honesto sobre isso e depois corrigir o problema de verdade. A solução é adicionar uma fase de "colheita do scratchpad" aos protocolos de handoff e handson, promovendo scripts e aprendizados para lugares duráveis como o repositório de scripts, documentação de processos, e registros de handoff. Preciso localizar e editar o arquivo de protocolo de handoff — provavelmente em `.claude/commands/handoff.md` ou `.claude/skills/handoff/` — para incluir essa síntese de scratchpad.

Agora preciso atualizar os agentes envolvidos: o `engineer-spaces` que gerencia os spaces e o `creative-director` que dirige o pipeline do Creative Studio para HyperFrames.  Vou incorporar os aprendizados desta sessão e da produção anterior do EP05 — a técnica de VFX com GSAP e Playwright para frame-seeking, o screencast calibrado em 70%, o contrato com Veo para geração de vídeo com durações de 4 a 8 segundos, timeline dirigida pela narração, trilha sonora Lyria organizada por ato, os novos comportamentos do canvas com clique e duplo-clique, e os runners já em scripts/ep05/.

Também preciso considerar a migração do OpenClaw para Hermes — ele está questionando se vale a pena manter o OpenClaw ou se deveria migrar 100% para o Hermes.

Estou tentando entender o que é "Hermes" neste contexto. Conheço alguns candidatos: a família de modelos open-source Hermes (Hermes 3, Hermes 4) da Nous Research, ou talvez um framework de agentes chamado Hermes. Mas até meu conhecimento em janeiro de 2026, não tenho clareza sobre um "Hermes" estabelecido como substituto direto do OpenClaw — que é o gateway de agentes local deles, algo como o antigo Clawdbot/Moltbot, com configurações em ~/.openclaw/ e documentação em docs.openclaw.

Não tenho evidência de empresas migrando do OpenClaw para Hermes, então isso pode ser algo posterior ao meu cutoff ou talvez uma confusão de nomes. O certo aqui é não inventar — preciso fazer uma busca na web para entender melhor o que é "Hermes" e se essa migração é realmente uma tendência. Uma decisão arquitetural dessa magnitude merece uma pesquisa fundamentada antes de opinar.

Além disso, o diagnóstico real começa pelo problema específico: o que exatamente não está evoluindo no OpenClaw? É a memória, o sistema de Dreaming, os agentes L1, o gateway? Só depois de identificar o gargalo é que faz sentido avaliar se uma ferramenta nova resolve. Vou pesquisar o Hermes para dar uma resposta bem informada.

Meu plano agora é: primeiro, corrigir a premissa — nada foi perdido desta vez, consegui recuperar e promover tudo — mas o risco é real e preciso vacinar contra isso. Depois, implementar um "aperto de mãos de aprendizado contínuo" com um SOP documentado, um patch no protocolo de handoff para colher o scratchpad antes de encerrar, e talvez um patch no handson para reconhecer scratchpads órfãos de sessões anteriores — o handoff registra o path e o handson lê. Também estou considerando criar uma skill que dispara ao selar a sessão.

Agora preciso atualizar os agentes com os aprendizados mais recentes: adicionar ao engineer-spaces os comportamentos novos do canvas (clique e duplo-clique), o screencast calibrado e verificar o contrato Veo; e no creative-director, documentar a produção master do EP05 com a timeline de narração dirigida, as escolhas de áudio entre Veo nativo e narração, e a trilha Lyria v2 em D-maior joyful.

Depois vou pesquisar sobre Hermes usando a skill de busca web — preciso entender se é um produto real, como se compara com OpenClaw, e então dar uma recomendação fundamentada, provavelmente sugerindo uma abordagem cautelosa com testes antes de qualquer migração, já que isso seria uma decisão arquitetural importante. Vou disparar um agente em background para pesquisar Hermes versus OpenClaw enquanto trabalho nos edits de protocolo e agentes em paralelo. Depois leio o handoff.md, edito as fases e crio o SOP com a skill scratchpad-harvest.

</details>


## 🤖 Claude *(22:21:35)*

Três frentes neste turno — e uma correção de premissa importante primeiro: **desta vez não perdemos nada** (recuperei 100% do material no `/tmp` e promovi os runners ao repo) — mas você está certo no diagnóstico: foi **sorte** (host sem reboot desde a sessão), não protocolo. O `/handoff` não colhe scratchpads. Vou vacinar isso agora, atualizar os dois agentes, e sobre o Hermes — vou pesquisar de verdade antes de opinar (Lei 1: não vou basear uma decisão de re-plataforma em impressão).

Disparando a pesquisa Hermes em paralelo enquanto conserto o protocolo:

## 🤖 Claude *(22:21:47)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Pesquisar Hermes vs OpenClaw",
  "subagent_type": "general-purpose",
  "prompt": "Pesquisa factual na web (use WebSearch e WebFetch). Contexto: o usu\u00e1rio opera um squad de agentes de IA local chamado OpenClaw (open-source, ex-Clawdbot/Moltbot, gateway local em ~/.openclaw/, docs em docs.openclaw.ai \u2014 assistente de IA pessoal auto-hospedado com mem\u00f3ria, cron, Telegram, multi-agente). Ele diz que \"viu muito por a\u00ed na internet empresas migrando 100% do OpenClaw para o Hermes\" e pergunta se deve migrar.\n\nSua miss\u00e3o (responda em Portugu\u00eas do Brasil):\n1. Descobrir O QUE \u00c9 \"Hermes\" nesse contexto de 2026: existe um produto/framework de agentes chamado Hermes que seja apresentado como sucessor/alternativa ao OpenClaw? Candidatos a investigar: (a) um fork ou sucessor do OpenClaw; (b) Nous Research Hermes (fam\u00edlia de modelos); (c) qualquer framework de agentes/assistente pessoal chamado Hermes lan\u00e7ado em 2025-2026. Busque termos como: \"Hermes agent framework\", \"OpenClaw Hermes migration\", \"migrate from OpenClaw to Hermes\", \"Hermes self-hosted AI assistant 2026\", \"OpenClaw alternative Hermes\", e varia\u00e7\u00f5es em portugu\u00eas.\n2. Verificar a alega\u00e7\u00e3o \"empresas migrando do OpenClaw para o Hermes\": h\u00e1 relatos reais (posts, HN, Reddit, blogs de empresa) ou isso \u00e9 hype/confus\u00e3o?\n3. Se o Hermes for real: colete URL oficial, licen\u00e7a, modelo de governan\u00e7a, maturidade (estrelas/releases), diferen\u00e7as-chave vs OpenClaw (mem\u00f3ria/evolu\u00e7\u00e3o cont\u00ednua, multi-agente, integra\u00e7\u00f5es, self-host), e caminhos de migra\u00e7\u00e3o documentados.\n4. Se N\u00c3O encontrar nada substancial: diga isso claramente \u2014 a aus\u00eancia de evid\u00eancia \u00e9 um achado v\u00e1lido e importante.\n\nREGRAS: toda claim com URL de fonte. N\u00e3o fabrique. Diferencie \"n\u00e3o encontrei\" de \"n\u00e3o existe\". Retorne um relat\u00f3rio estruturado: (a) veredito do que \u00e9 Hermes; (b) evid\u00eancia de migra\u00e7\u00f5es reais sim/n\u00e3o com fontes; (c) tabela comparativa se aplic\u00e1vel; (d) recomenda\u00e7\u00e3o preliminar fundamentada (migrar 100% / avaliar em piloto / n\u00e3o migrar / n\u00e3o h\u00e1 o que migrar)."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': "Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)\nagentId: a575f41c59d70f794 (internal ID - do not mention to user. Use SendMessage with to: 'a575f41c59d70f794', summary: '<5-10 word recap>' to continue this agent.)\nThe agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.\nDo not duplicate this agent's work — avoid working with the same files or topics it is using.\noutput_file: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/b0849ca6-1455-45f8-9291-d80f6edd1183/tasks/a575f41c59d70f794.output\nDo NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification."}]
> ```

## 🤖 Claude *(22:21:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls .claude/commands/handoff.md .claude/skills/handoff/SKILL.md 2>/dev/null; ls .claude/agents/ | grep -iE \"spaces|creative|hyper\"; ls .claude/skills/ | grep -iE \"spaces|creative|hyper|cinematic\"",
  "description": "Locate handoff protocol file and the two agents to update"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> .claude/commands/handoff.md
> creative-director.md
> engineer-spaces.md
> canvas-studio-cinematic
> creative-studio-pipeline
> engineer-spaces
> ```

## 🤖 Claude *(22:21:55)*

<details>
<summary>💭 Thinking Process</summary>

Hermes está procurando pelos arquivos relevantes em background — encontrou o protocolo do handoff, os agentes de creative director e engineer spaces, além das skills relacionadas. Agora preciso abrir o handoff.md para identificar onde encaixar a fase de colheita do scratchpad, mesmo que o arquivo seja extenso.

</details>


## 🤖 Claude *(22:21:56)*

<details>
<summary>💭 Thinking Process</summary>

Pesquisa em andamento. Agora vou corrigir o protocolo, lendo a estrutura do `/handoff` para inserir a fase de colheita.

</details>


## 🤖 Claude *(22:21:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l .claude/commands/handoff.md; grep -n \"^## \\|^### \\|PHASE\\|Phase\" .claude/commands/handoff.md | head -40",
  "description": "Map handoff protocol phases structure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 479 .claude/commands/handoff.md
> 5:> **v4 (2026-05-15):** Reordered phases — Knowledge Mesh Milestone (Phase 3) now runs
> 6:> **before** README.md update (Phase 4), so the live node count query captures the handoff
> 9:> **v3 (2026-05-14):** Added Phase 6 BoK Seal Status — verifies any module
> 15:## PRE-FLIGHT (execute ALL in parallel before anything else)
> 36:## PHASE 1 — SECURITY AUDIT
> 40:> ⚠️ **SCOPE NOTE:** This phase scans changes that exist NOW (before Phase 5 writes HANDOFF.md).
> 41:> A second mandatory scan runs in Phase 5b, after HANDOFF.md is written and before it is committed.
> 69:### DOCUMENTATION CREDENTIAL RULE (invariant — never violate)
> 77:> **Rationale:** Phase 1 scans changes that predate the HANDOFF.md write. Any credential embedded
> 78:> in HANDOFF.md during Phase 5 escapes Phase 1 entirely and goes directly to the remote.
> 79:> This rule is the primary prevention layer; Phase 5b is the detection backstop.
> 83:## PHASE 2 — GRANULAR COMMITS
> 98:## PHASE 3 — KNOWLEDGE MESH MILESTONE
> 100:> ⚠️ **ORDER MATTERS:** This phase runs BEFORE Phase 4 (README badge) so the live count
> 108:SESSION_PHASE="<phase-name-slug>"
> 117:    \"name\": \"session-handoff-$(date +%Y%m%d)-${SESSION_PHASE}\",
> 124:      \"session\": \"${SESSION_PHASE}\",
> 143:Emit `proof-manifest.json` so Phase 5c can verify this handoff node strictly:
> 150:## PHASE 4 — README.md UPDATE
> 152:> ℹ️ Phase 3 (milestone node) has already been inserted — the live count below includes it.
> 166:   - If new phase shipped → add phase badge (e.g. `Phase_Zeta-live-cyan`)
> 168:2. **Phase Status table** — add new row for this session's phase:
> 170:   | Phase Zeta — <Name> | ✅ <one-line summary> |
> 175:   ### [v5.X.X] — <Phase Name> (<date>)
> 189:## PHASE 5 — HANDOFF.md UPDATE
> 207:   | **<Phase Name>** | ✅ <one-line summary> |
> 212:   ## <Phase Name> Record (<YYYY-MM-DD>)
> 226:   ### Arquitetura <Phase Name>
> 238:## PHASE 5b — HANDOFF.md SECRET SCAN (mandatory before commit)
> 260:3. Re-run Phase 5b until all checks pass
> 265:## PHASE 5b-2 — HANDOFF.md SIZE GATE (mandatory before commit)
> 290:Commit HANDOFF.md only after Phase 5b passes:
> 297:## PHASE 5c — MATERIAL PROOF AUDIT (mandatory before push)
> 305:# Runs after Phase 5b, so the newest HANDOFF.md Record block is this seal's.
> 314:- **exit 0 — `SEAL ALLOWED`** → embed the Proof Manifest in the Phase 8 report (`📋 PROVA MATERIAL`); proceed to Phase 6.
> 317:  strict handoff-node claim, re-attempt the Phase 3 insert once (SOP Cenário D), then re-run.
> 322:## PHASE 6 — BoK SEAL STATUS (mandatory before push)
> 355:- ✅ All session modules have sealed BoK → proceed to Phase 7 push.
> 359:Report BoK status in final seal output (Phase 8).
> 363:## PHASE 7 — PUSH
> ```

## 🤖 Claude *(22:22:09)*

<details>
<summary>💭 Thinking Process</summary>

I've mapped out the handoff.md structure and realized the scratchpad harvest phase needs to happen before the granular commits phase, since harvesting produces the files that need to be committed. I'm inserting this as a new Phase 1b between the security audit and commits, where I'll inventory the session's scratchpad contents including runners, scripts, and artifacts.

The classification logic sorts these into three categories: reusable runner techniques get promoted to the scripts module or docs for processes; heavy media or data artifacts go to durable storage like a library or bucket with asset IDs recorded; and disposable items like logs stay behind. The core principle is that no learning or technique can remain only in the temporary scratchpad after the session seals—it's volatile and would be lost on reboot. I'll document everything in the Record: the scratchpad path, what got promoted, what stayed and why. This whole phase came from a near-miss incident back in August 2026, so I need to find the exact section between Phase 1 and Phase 2 in the handoff file to make the edit.

</details>


## 🤖 Claude *(22:22:09)*

A fase de colheita precisa entrar **antes** dos commits (ela produz arquivos a commitar). Lendo o ponto de inserção:

## 🤖 Claude *(22:22:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/commands/handoff.md",
  "offset": 77,
  "limit": 22
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 77	> **Rationale:** Phase 1 scans changes that predate the HANDOFF.md write. Any credential embedded
> 78	> in HANDOFF.md during Phase 5 escapes Phase 1 entirely and goes directly to the remote.
> 79	> This rule is the primary prevention layer; Phase 5b is the detection backstop.
> 80	
> 81	---
> 82	
> 83	## PHASE 2 — GRANULAR COMMITS
> 84	
> 85	Group uncommitted changes by concern and commit each group separately.
> 86	
> 87	**Commit rules (from memory + project convention):**
> 88	- Prefix: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`
> 89	- Body: one paragraph explaining the WHY (milestone orientation, not diff description)
> 90	- **NEVER** add `Co-Authored-By` trailer
> 91	- **NEVER** use `git add -A` — stage files explicitly by name
> 92	- Skip: `build_log.txt`, `node_modules/`, `dist/`, `.env`, `check_types.ts`, `scratch/`
> 93	
> 94	Stage and commit each logical group before moving to the next phase.
> 95	
> 96	---
> 97	
> 98	## PHASE 3 — KNOWLEDGE MESH MILESTONE
> ```

## 🤖 Claude *(22:22:26)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/commands/handoff.md",
  "old_string": "> **Rationale:** Phase 1 scans changes that predate the HANDOFF.md write. Any credential embedded\n> in HANDOFF.md during Phase 5 escapes Phase 1 entirely and goes directly to the remote.\n> This rule is the primary prevention layer; Phase 5b is the detection backstop.\n\n---\n\n## PHASE 2 \u2014 GRANULAR COMMITS",
  "new_string": "> **Rationale:** Phase 1 scans changes that predate the HANDOFF.md write. Any credential embedded\n> in HANDOFF.md during Phase 5 escapes Phase 1 entirely and goes directly to the remote.\n> This rule is the primary prevention layer; Phase 5b is the detection backstop.\n\n---\n\n## PHASE 1b \u2014 SCRATCHPAD HARVEST (colheita do aprendizado \u2014 antes dos commits)\n\n> **Nasceu do quase-acidente EP05 (2026-08-03):** uma sess\u00e3o-maratona de produ\u00e7\u00e3o deixou TODOS os\n> runners (trilha Lyria, assemble do master, VFX t\u00edtulo, screencast) + 1.9GB de intermedi\u00e1rios\n> SOMENTE no scratchpad `/tmp/claude-1001/.../scratchpad` \u2014 vol\u00e1til, morre no reboot. A sess\u00e3o\n> seguinte s\u00f3 recuperou tudo porque o host n\u00e3o reiniciou. **Sorte n\u00e3o \u00e9 protocolo.**\n\nO scratchpad da sess\u00e3o (`$SCRATCHPAD` do system prompt) DEVE ser colhido antes do seal:\n\n```bash\nls -la <scratchpad-desta-sess\u00e3o>/   # invent\u00e1rio material \u2014 o que foi criado aqui?\n```\n\nClassifique cada item e aja:\n\n| Classe | Crit\u00e9rio | Destino obrigat\u00f3rio |\n|--------|----------|---------------------|\n| **Runner/t\u00e9cnica** | script que gerou/montou/provou algo (qualquer coisa que outra sess\u00e3o precisaria reexecutar ou estudar) | promover a `scripts/<m\u00f3dulo>/` no repo (+ nota no README da pasta) \u2192 entra nos commits da Phase 2 |\n| **Processo/gate aprendido** | sequ\u00eancia com gates que se repetir\u00e1 | SOP em `docs/processes/` (\u00a75 Obstacle\u2192Synthesis) |\n| **Entreg\u00e1vel de m\u00eddia** | master/take/\u00e1udio que o Sovereign avalia | Biblioteca (`canvas-assets` + `register_creative_asset`) \u2014 registrar o asset id no Record |\n| **Descart\u00e1vel** | logs, downloads re-obten\u00edveis do bucket, venvs | fica no scratchpad (documentar no Record que \u00e9 descart\u00e1vel) |\n\n**Regra-m\u00e3e:** nenhum aprendizado ou ferramenta pode existir S\u00d3 em `/tmp` ap\u00f3s o seal. O Record da\nPhase 5 DEVE citar: o path do scratchpad da sess\u00e3o \u00b7 o que foi promovido (com paths do repo/asset ids)\n\u00b7 o que ficou para tr\u00e1s e por qu\u00ea. SOP: `docs/processes/scratchpad-harvest.md`.\n\n---\n\n## PHASE 2 \u2014 GRANULAR COMMITS"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/commands/handoff.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:22:33)*

<details>
<summary>💭 Thinking Process</summary>

Agora preciso estruturar a Fase 1b no diretório /handoff, criando um SOP que documente o processo de colheita do scratchpad seguindo a Lei 2 com seus passos de operador, sequência, verificação, recuperação e sucesso. Também vou desenvolver a skill correspondente que gatilhe quando a sessão for selada, garantindo que o material fique isolado no scratchpad e possa ser recuperado de sessões anteriores, além de aplicar um patch no /handson.

Vou adicionar um passo leve no pre-flight do handson para verificar o scratchpad citado no último Record do HANDOFF, reconhecendo assim scratchpads órfãos. Vou escrever a SOP e a skill em paralelo.

</details>


## 🤖 Claude *(22:22:34)*

<details>
<summary>💭 Thinking Process</summary>

Fase 1b do protocolo está completa. Agora vou verificar o SOP (Lei 2) e a skill de gatilho automático.

</details>


## 🤖 Claude *(22:22:58)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/scratchpad-harvest.md",
  "content": "# Scratchpad Harvest \u2014 colheita de aprendizado cont\u00ednuo entre sess\u00f5es (Lei 2)\n\n> **Nasceu do quase-acidente EP05 (2026-08-03).** A sess\u00e3o-maratona de produ\u00e7\u00e3o do master EP05\n> deixou os runners (trilha Lyria, assemble, VFX t\u00edtulo GSAP, screencast) + 1.9GB de intermedi\u00e1rios\n> SOMENTE em `/tmp/claude-1001/<projeto>/<sess\u00e3o>/scratchpad` \u2014 diret\u00f3rio vol\u00e1til, por-sess\u00e3o, que\n> morre num reboot do host. A sess\u00e3o seguinte recuperou 100% do material **por sorte** (host up\n> 7 semanas). O `/handoff` n\u00e3o tinha fase de colheita; agora tem (PHASE 1b). Este SOP \u00e9 a fonte.\n\n## Operator\nO agente da sess\u00e3o (MCORCH Master Execution Agent), na PHASE 1b do `/handoff` \u2014 ou a qualquer\nmomento em que perceber que material valioso vive s\u00f3 no scratchpad. O Sovereign n\u00e3o executa nada.\n\n## Sequence\n\n1. **Invent\u00e1rio material** \u2014 `ls -la <scratchpad>/` + `du -sh <scratchpad>/*/`. Crit\u00e9rio de\n   sucesso: cada arquivo/dir classificado numa das 4 classes abaixo (nenhum \"n\u00e3o sei o que \u00e9\").\n2. **Promover runners/t\u00e9cnicas** \u2192 `scripts/<m\u00f3dulo>/` no repo, com nota no README da pasta\n   (paths de workdir apontam para o scratchpad de origem \u2014 anotar isso). Sucesso: `git status`\n   mostra os arquivos staged; commit na Phase 2 do seal.\n3. **Promover processos/gates aprendidos** \u2192 SOP em `docs/processes/<slug>.md` quando a sequ\u00eancia\n   se repetir\u00e1 (\u00a75 Obstacle\u2192Synthesis do CLAUDE.md). Sucesso: arquivo existe + entra na Key Files\n   Reference se for load-bearing.\n4. **Promover entreg\u00e1veis de m\u00eddia** \u2192 Biblioteca (`canvas-assets` bucket + `register_creative_asset`\n   RPC, molde `scripts/ep05/upload-a6.ts`). Sucesso: asset id retornado pela RPC, citado no Record.\n5. **Registrar no Record do HANDOFF.md** (Phase 5): path do scratchpad da sess\u00e3o \u00b7 lista do que\n   foi promovido (paths/ids) \u00b7 o que ficou para tr\u00e1s como descart\u00e1vel e por qu\u00ea.\n\n## Classes\n\n| Classe | Crit\u00e9rio | Destino |\n|--------|----------|---------|\n| Runner/t\u00e9cnica | outra sess\u00e3o precisaria reexecutar/estudar | `scripts/<m\u00f3dulo>/` |\n| Processo/gate | sequ\u00eancia com gates que reincide | `docs/processes/` |\n| Entreg\u00e1vel de m\u00eddia | o Sovereign avalia/usa | Biblioteca (asset registrado) |\n| Descart\u00e1vel | logs, re-downloads do bucket, venvs, frames intermedi\u00e1rios | fica; documentado como descart\u00e1vel |\n\n## Verification gates\n\n- **G1 (promo\u00e7\u00e3o real):** todo item classe 1-2 aparece em `git status` antes da Phase 2; todo\n  item classe 3 tem asset id de `register_creative_asset`. Claim sem prova = viola\u00e7\u00e3o Lei 1.\n- **G2 (Record cita o path):** o Record novo cont\u00e9m a string `/scratchpad` com o path da sess\u00e3o.\n  Grep mec\u00e2nico: `grep -c \"scratchpad\" HANDOFF.md` cresce no seal.\n- **G3 (nada \u00f3rf\u00e3o):** re-rodar o invent\u00e1rio ap\u00f3s a promo\u00e7\u00e3o \u2014 o que sobrou \u00e9 s\u00f3 classe 4.\n\n## Recovery path (material de sess\u00e3o ANTERIOR possivelmente perdido)\n\n1. Scratchpads antigos sobrevivem enquanto o host n\u00e3o reinicia:\n   `ls /tmp/claude-1001/<projeto-slug>/` (um UUID por sess\u00e3o).\n2. Localizar por nome de artefato: `find /tmp/claude-1001/<projeto-slug>/ -maxdepth 3 -name \"<padr\u00e3o>\"`.\n   (Isso N\u00c3O \u00e9 o \"find cego no host\" proibido pela skill host-media-masters \u2014 o escopo \u00e9 o diret\u00f3rio\n   de scratchpads do projeto, n\u00e3o o filesystem.)\n3. Se o host reiniciou e o material morreu: reconstruir a partir do que o Record cita (assets da\n   Biblioteca + scripts promovidos). Se o Record n\u00e3o cita nada \u2192 o seal violou este SOP; registrar\n   o custo real da perda no pr\u00f3ximo Record para calibrar o gate.\n\n## Success signal\n\nO `/handson` seguinte consegue retomar a produ\u00e7\u00e3o SEM arqueologia: os runners est\u00e3o em\n`scripts/<m\u00f3dulo>/`, os entreg\u00e1veis na Biblioteca, e o Record diz onde est\u00e1 cada coisa.\nProva viva: sess\u00e3o 2026-08-03b remontou o master EP05 (A6) em minutos porque o A5 local +\nspeech + segs sobreviveram \u2014 com este SOP, isso deixa de depender de sorte.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/scratchpad-harvest.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:23:13)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/skills/scratchpad-harvest/SKILL.md",
  "content": "---\nname: scratchpad-harvest\ndescription: Colheita do scratchpad \u2014 aprendizado cont\u00ednuo entre sess\u00f5es. Dispara SEMPRE que (a) for selar a sess\u00e3o (/handoff PHASE 1b), (b) perceber que runners/t\u00e9cnicas/entreg\u00e1veis valiosos vivem S\u00d3 no scratchpad /tmp da sess\u00e3o, ou (c) precisar RECUPERAR material de uma sess\u00e3o anterior (\"cad\u00ea o script X / o master Y que fizemos ontem?\"). Promove runners a scripts/<m\u00f3dulo>/, processos a docs/processes/, m\u00eddia \u00e0 Biblioteca (register_creative_asset), e registra tudo no Record do HANDOFF. Impede o falso-selamento em que o conhecimento da sess\u00e3o morre num reboot do host. SOP: docs/processes/scratchpad-harvest.md.\n---\n\n# Scratchpad Harvest \u2014 o aperto de m\u00e3os do aprendizado cont\u00ednuo\n\n**Por que existo:** o quase-acidente EP05 (2026-08-03) \u2014 runners de produ\u00e7\u00e3o + 1.9GB s\u00f3 em\n`/tmp/claude-1001/.../scratchpad`, recuperados na sess\u00e3o seguinte por SORTE (host sem reboot).\nScratchpad \u00e9 vol\u00e1til e por-sess\u00e3o; o seal que n\u00e3o colhe = conhecimento morto.\n\n## Ao selar (ou quando material valioso est\u00e1 s\u00f3 no /tmp)\n\n1. `ls -la <scratchpad-da-sess\u00e3o>/` \u2014 invent\u00e1rio completo, classificar TUDO:\n   - **Runner/t\u00e9cnica** \u2192 `scripts/<m\u00f3dulo>/` (+ nota no README da pasta) \u2192 commit\n   - **Processo/gate** \u2192 SOP `docs/processes/<slug>.md` (\u00a75 Obstacle\u2192Synthesis)\n   - **Entreg\u00e1vel de m\u00eddia** \u2192 Biblioteca: upload `canvas-assets` + `register_creative_asset`\n     (molde: `scripts/ep05/upload-a6.ts`) \u2014 guardar o asset id\n   - **Descart\u00e1vel** (logs/re-downloads/venvs) \u2192 fica, documentado\n2. Record do HANDOFF cita: path do scratchpad \u00b7 promovidos (paths/ids) \u00b7 descart\u00e1veis.\n3. Gates: G1 promo\u00e7\u00e3o em `git status`/asset id \u00b7 G2 Record cita o path \u00b7 G3 sobra s\u00f3 descart\u00e1vel.\n\n## Ao recuperar material de sess\u00e3o anterior\n\n```bash\nls /tmp/claude-1001/<projeto-slug>/                                  # um UUID por sess\u00e3o\nfind /tmp/claude-1001/<projeto-slug>/ -maxdepth 3 -name \"<padr\u00e3o>\"   # escopo: s\u00f3 scratchpads\n```\nHost reiniciou? Reconstruir pelo Record (assets Biblioteca + scripts promovidos). Se o Record\nn\u00e3o cita nada, o seal anterior violou o SOP \u2014 registre a perda real no pr\u00f3ximo Record.\n\n## Anti-patterns\n\n- \u274c Selar com runner in\u00e9dito s\u00f3 no /tmp (\"depois eu promovo\" = nunca)\n- \u274c \"Est\u00e1 tudo no scratchpad\" no Record sem path nem lista (n\u00e3o-verific\u00e1vel, Lei 1)\n- \u274c Re-escrever do zero um runner que existe num scratchpad vivo \u2014 SEMPRE sondar antes\n- \u274c Copiar m\u00eddia pesada para o repo (m\u00eddia \u2192 Biblioteca; repo \u2192 s\u00f3 scripts/docs)\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/skills/scratchpad-harvest/SKILL.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:23:19)*

<details>
<summary>💭 Thinking Process</summary>

Criados o SOP e skill. Agora preciso adicionar a recon de scratchpad no pickup do handson, checando o scratchpad mencionado no último Record no pre-flight. Depois vou adicionar a Key Files Reference no CLAUDE.md e atualizar os dois agentes.

</details>


## 🤖 Claude *(22:23:19)*

<details>
<summary>💭 Thinking Process</summary>

Agora vou trabalhar no lado `/handson` — o pickup precisa saber procurar o scratchpad citado no Record.

</details>


## 🤖 Claude *(22:23:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"scratch/\" .claude/commands/handson.md | head -5",
  "description": "Find scratch section in handson protocol"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 34:Also check for loose files in scratch/:
> 36:ls scratch/ 2>/dev/null && echo "⚠️ scratch/ has files — consider moving to .claude/scripts/db/" || echo "scratch/ clean ✅"
> 119:  <containers unhealthy, TS errors, uncommitted changes que conflitam, scratch/ com arquivos, ou "Nenhum alerta ✅">
> ```

## 🤖 Claude *(22:23:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/commands/handson.md",
  "offset": 32,
  "limit": 8
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 32	> ⚠️ **Auditoria histórica de seals antigos:** usar `Read` com offset arbitrário em HANDOFF.md (fora do fluxo padrão de pickup). Ordering newest-first: seal mais antigo ≈ linha 2805, seal mais recente logo após linha 71. Cada `## <Phase> Record (YYYY-MM-DD)` marca um seal. Manter o Read em chunks ≤ 400 linhas para preservar budget de tokens.
> 33	
> 34	Also check for loose files in scratch/:
> 35	```bash
> 36	ls scratch/ 2>/dev/null && echo "⚠️ scratch/ has files — consider moving to .claude/scripts/db/" || echo "scratch/ clean ✅"
> 37	```
> 38	
> 39	### BoK Gate check (v3 — MCORCH Master Execution Protocol)
> ```

## 🤖 Claude *(22:23:33)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/commands/handson.md",
  "old_string": "Also check for loose files in scratch/:\n```bash\nls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files \u2014 consider moving to .claude/scripts/db/\" || echo \"scratch/ clean \u2705\"\n```",
  "new_string": "Also check for loose files in scratch/:\n```bash\nls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files \u2014 consider moving to .claude/scripts/db/\" || echo \"scratch/ clean \u2705\"\n```\n\n### Scratchpad continuity (aprendizado cont\u00ednuo \u2014 SOP `docs/processes/scratchpad-harvest.md`)\n\nSe o Record mais recente do HANDOFF.md cita um path de scratchpad (`/tmp/claude-1001/.../scratchpad`),\nverifique se ele ainda existe \u2014 material de produ\u00e7\u00e3o da sess\u00e3o anterior pode viver l\u00e1:\n```bash\nls /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ 2>/dev/null | wc -l   # sess\u00f5es vivas\n```\nSe a sess\u00e3o vai CONTINUAR uma produ\u00e7\u00e3o (master, screencasts, trilha), localize o workdir anterior\nANTES de regenerar qualquer coisa com custo: `find /tmp/claude-1001/<projeto>/ -maxdepth 3 -name \"<artefato>\"`.\nRunners promovidos vivem em `scripts/<m\u00f3dulo>/` (ex.: `scripts/ep05/`). Reboot do host = scratchpads\nmortos \u2192 reconstruir pelo Record (assets da Biblioteca + scripts do repo)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/commands/handson.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:23:39)*

<details>
<summary>💭 Thinking Process</summary>

Atualizei o /handson com patches. Agora preciso adicionar a Key Files Reference no CLAUDE.md junto com os dois agentes, mas primeiro vou ler creative-director.md e engineer-spaces.md para entender seus tamanhos e conteúdo antes de fazer qualquer edição.

</details>


## 🤖 Claude *(22:23:39)*

<details>
<summary>💭 Thinking Process</summary>

O protocolo dos dois lados está fechado. Agora vou ler o estado atual de ambos os agentes para atualizar com fundamento.

</details>


## 🤖 Claude *(22:23:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l .claude/agents/creative-director.md .claude/agents/engineer-spaces.md; echo \"=== creative-director headings ===\"; grep -n \"^#\\|^##\" .claude/agents/creative-director.md | head -20; echo \"=== engineer-spaces headings ===\"; grep -n \"^#\\|^##\" .claude/agents/engineer-spaces.md | head -20",
  "description": "Map both agent files structure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>    56 .claude/agents/creative-director.md
>    66 .claude/agents/engineer-spaces.md
>   122 total
> === creative-director headings ===
> 7:# Creative Director — Subagent (L2 sob `artisan`)
> 13:## O pipeline que você dirige
> 28:## Motores e seus contratos (grounded)
> 35:## Protocolo (sempre nesta ordem)
> 44:## Regras de recusa (Leis de Sobrevivência)
> 51:## Skills
> === engineer-spaces headings ===
> 7:# Engineer-Spaces — Arquiteto de Mundos / Infinite Canvas (Subagent L2)
> 17:## ⚠️ Verdade fundamental (verificada 2026-07-21) — VIVO vs MIRROR
> 32:## Os 6 SEAMS (o contrato de um nó do Spaces vivo)
> 43:## Gates (todos verdes ou não terminou) — Lei 1
> 51:## Anti-patterns (recuse ou corrija)
> 60:## Refusal (PT-BR, quando faltar gate)
> ```

## 🤖 Claude *(22:23:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/creative-director.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: creative-director
> 3	description: Diretor Criativo técnico do MCORCH — dirige o pipeline Creative Studio do Spaces (roteiro → prompts → imagem → Ken Burns/sequência → template cinematográfico → áudio → MP4 9:16 final) 100% no rail FFmpeg grátis (US$0). Use para montar/operar os nós Roteiro e Criativo Cinematográfico, encadear cenas→imagens→curta, agrupar frames intermediários in-node, e provar criativos com Vision ocular. Recusa código de nó sem a Amendment BoK selada (Lei 2) e nunca reporta criativo pronto sem olhar o vídeo (Lei 1).
> 4	tools: Bash, Read, Write, Edit, Grep, Glob
> 5	---
> 6	
> 7	# Creative Director — Subagent (L2 sob `artisan`)
> 8	
> 9	Você é o **Creative Director** do MCORCH: L2 Specialist sob o Head `artisan` (lente CXBOK/ProdBOK-UX), com **Decision Scope NARROW** ao grafo de nós do **Creative Studio** dentro do Spaces. Sua missão: transformar um tema em um **curta cinematográfico 9:16** de nível motion-design, **inteiramente no rail FFmpeg grátis** (US$0), e deixá-lo editável no `/dashboard/spaces/video`.
> 10	
> 11	**SSOT:** `docs/bok/spaces-evolution/17-amendment-creative-studio-nodes.md` (Amendment 17). Você NÃO inventa além dela — ambiguidade volta pra emenda/`/bok-scribe`, não pra improviso (Master Protocol §1).
> 12	
> 13	## O pipeline que você dirige
> 14	
> 15	```
> 16	[Roteiro] tema → { scenes[] (start/end/narration/imagePrompt), ttsPrompt }   (formato verbatim do Sovereign)
> 17	   │  output_script fan-out:
> 18	   ├─ scenes[].imagePrompt ──→ [Gerar imagem] (Nano Banana / Gemini DIRETO — mais barato que OpenRouter)
> 19	   │                              │ (imagem por cena, ~US$0,039 cada)
> 20	   │                              ▼
> 21	   ├──────────────────────────→ [Criativo Cinematográfico] template cinematic-9x16 (renderComposition)
> 22	   │                              │  Ken Burns no hero + tipografia cinética + HUD neon + emblema
> 23	   └─ ttsPrompt ──→ [narração] Piper/Kokoro (grátis, comercial-safe) → envelope amplitude → energy[] (voice-reactive)
> 24	                                  ▼
> 25	                       MP4 9:16 FINAL (só ele em /assets) · frames intermediários AGRUPADOS in-node · editável em /spaces/video
> 26	```
> 27	
> 28	## Motores e seus contratos (grounded)
> 29	
> 30	- **Render grátis (RAIL 2, `video_renders`):** `engine='hyperframes'` `charged_mco:0` (precedente `reshape-pillar:266`, SEM migration). Mode switch em `video-bridge.ts:86-91`: `cinematic` → `renderComposition` (template `cinematic-9x16`, já em `VALID_TEMPLATES`); `kenburns` → `encodeKenBurns`; `image_sequence` → `encodeImageSequence` (`render-core.ts`). Os 3 devolvem o mesmo `RenderResult` → upload/finalize/refund já são mode-agnostic.
> 31	- **Template `cinematic-9x16.html`:** props `window.applyProps` = `brand,cta,caption,hook`(\n),`product_image_url`(https/data),`energy[]` opcional. Determinístico (NFR-VS-016).
> 32	- **Imagem:** Gemini Nano Banana (`gemini-2.5-flash-image`). Preferir **Gemini DIRETO** (sem margem OpenRouter). Per-user BYOK fail-closed 402.
> 33	- **Áudio:** narração Piper/Kokoro (MIT/Apache, pt-BR, self-host, US$0). Voice-clone pt-BR comercial = gap → pós-renda.
> 34	
> 35	## Protocolo (sempre nesta ordem)
> 36	
> 37	1. **Gate Lei 2:** antes de qualquer código de nó novo, confirme que a Amendment 17 está no repo. Sem ela → Refusal Mode (draftar/atualizar a emenda primeiro).
> 38	2. **Oriente material:** `git log --oneline -12`. Os 3 primitivos + o template já existem em `scripts/hyperframes/`.
> 39	3. **Construa por slice** (Amendment 17 §6), respeitando o status: `buildable-now` primeiro; `needs-security-review` só depois de `/security-review`; `needs-ui` com prova de reconciliação real.
> 40	4. **Rail grátis primeiro:** todo motor default é US$0 (FFmpeg/Piper). Leg pago (imagem paga, voz premium) você **propõe com custo**, nunca ativa em silêncio ([[feedback_paid_byok_post_revenue]]).
> 41	5. **Prova material (Lei 1) por render:** `ffprobe` do MP4 (dimensões/fps/frames) + **Vision ocular** de ≥1 frame (extrair PNG e OLHAR) antes de dizer "pronto". MP4 < 100KB = suspeito (piso material).
> 42	6. **Assets:** carimbe frames intermediários `asset_role='frame'` + `frame_index` por `source_job_id`; só o final é `asset_role='final'` (aparece no `/assets`). Nunca polua o grid.
> 43	
> 44	## Regras de recusa (Leis de Sobrevivência)
> 45	
> 46	- **Lei 1:** nunca reporte criativo pronto sem `ffprobe` + Vision ocular no turno. "Renderizou" ≠ "ficou bom". Sem olho, é "cérebro sem mãos".
> 47	- **Lei 2:** nenhum nó/edge/migration novo sem a Amendment 17 (ou emenda equivalente) selada. SOP em `docs/processes/` antes de automação nova.
> 48	- **Segurança:** o `fetchToTmp` do rail grátis só baixa **URL assinada do mesmo owner** (anti-SSRF, OTD-CS-004). Migration `asset_role` e o compilador de open-in-video ridem `/security-review` + GO Sovereign.
> 49	- **Custo:** rail grátis é o default; pago é proposta gated. Imagem: meça direct-Google vs OpenRouter no 1º batch, trave o mais barato.
> 50	
> 51	## Skills
> 52	
> 53	- `creative-studio-pipeline` — orquestra roteiro→imagens→curta (estende `canvas-studio-cinematic`).
> 54	- `free-render-dispatch` — enfileira cinematic/kenburns/image_sequence a 0 mco com guardas anti-SSRF + piso 100KB.
> 55	- `asset-frame-grouping` — carimba `asset_role`/`frame_index` por `source_job_id`; grid finals-only; expander in-node.
> 56	- `open-in-video-deeplink` — compila criativo→projeto HyperFrames e deep-linka `#project/<slug>` com ownership check.
> 57	
> ```

## 🤖 Claude *(22:24:02)*

<details>
<summary>💭 Thinking Process</summary>

A skill scratchpad-harvest já está registrada. Agora preciso atualizar o creative-director.md com os aprendizados do EP05, especialmente sobre a produção de masters em 16:9 longos além dos shorts 9:16 — os runners estão em scripts/ep05/. Estou documentando a técnica VFX para títulos usando GSAP timeline determinística combinada com Playwright frame-seek.

Vou adicionar uma seção "Produção de MASTERS de episódio (EP05, 2026-08-03)" mantendo tudo conciso, depois atualizar o engineer-spaces.md com os novos comportamentos do canvas (clique abre RightPanel, duplo-clique abre modal) e referenciar o projeto EP05 v2 com seus 62 nós — preciso ler o arquivo antes de fazer as mudanças.

</details>


## 🤖 Claude *(22:24:02)*

Skill registrada ✅. Atualizando o `creative-director` com o ofício de masters aprendido na produção EP05:

## 🤖 Claude *(22:24:24)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/creative-director.md",
  "old_string": "## Skills\n\n- `creative-studio-pipeline` \u2014 orquestra roteiro\u2192imagens\u2192curta (estende `canvas-studio-cinematic`).\n- `free-render-dispatch` \u2014 enfileira cinematic/kenburns/image_sequence a 0 mco com guardas anti-SSRF + piso 100KB.\n- `asset-frame-grouping` \u2014 carimba `asset_role`/`frame_index` por `source_job_id`; grid finals-only; expander in-node.\n- `open-in-video-deeplink` \u2014 compila criativo\u2192projeto HyperFrames e deep-linka `#project/<slug>` com ownership check.",
  "new_string": "## Produ\u00e7\u00e3o de MASTERS de epis\u00f3dio (aprendido no EP05, 2026-08-03 \u2014 runners em `scripts/ep05/`)\n\nAl\u00e9m de shorts 9:16, voc\u00ea dirige **masters longos 16:9** (epis\u00f3dios YouTube). Receita provada (A6):\n\n- **Estrutura:** VFX t\u00edtulo 10s (sound design pr\u00f3prio) \u2192 filme 48 cenas \u2192 cr\u00e9ditos. Cartela redundante\n  com o VFX SAI (o VFX j\u00e1 carrega o \"GABRIEL AI APRESENTA\u2026\").\n- **VFX de t\u00edtulo/cartela:** `title.html` (GSAP timeline determin\u00edstica) + Playwright **frame-seek**\n  (`__seek(t)` por frame \u2192 300 PNG \u2192 MP4) \u2014 t\u00e9cnica HyperFrames reus\u00e1vel p/ QUALQUER vinheta.\n- **\u00c1udio (estrat\u00e9gia EP01-04):** apresentador = **\u00e1udio Veo nativo** (`generate_audio:true`, lip-sync\n  por constru\u00e7\u00e3o; Wav2Lip CPU reprovado \u2014 host sem GPU); cenas mudas = narra\u00e7\u00e3o Qwen3 **grossa**\n  (`asetrate\u00d70.90+atempo+highpass+compressor`); trilha **Lyria RealTime** por-ato **ducada**\n  (sidechaincompress) sob TODA fala; timeline **dirigida pela narra\u00e7\u00e3o**; `loudnorm I=-16`.\n- **Trilha Lyria:** cues por ato + steering com antecipa\u00e7\u00e3o 3s + `EXTRA_STEER` p/ lifts intra-ato;\n  o TOM \u00e9 dire\u00e7\u00e3o do Sovereign (v2 = FELIZ/ESPERAN\u00c7A: **D maior**, prompts joyful/radiant, sem\n  braams). \u26a0\ufe0f Anticorpos: queda ws 1011 \u00e9 NORMAL perto do fim (salvage + pad + fade cobrem);\n  buffer DEVE ser truncado a m\u00faltiplos de 4 bytes (queda no meio de frame + `int(TOTAL*BPS)`\n  fracion\u00e1rio quebram `np.frombuffer`) \u2014 fix vivo em `scripts/ep05/ep05-trilha-v2.py`.\n- **Contrato Veo (provado por sonda, n\u00e3o chute):** `text_to_video` dur \u2208 {4,6,8}s (5s = 422+estorno);\n  refs de identidade \u2192 dur **8s obrigat\u00f3rio**; Nano Banana SEMPRE devolve 1:1 \u2192 b-roll 16:9 nasce\n  no **Veo texto\u2192v\u00eddeo direto** (nunca nano\u2192firstFrame, vira pillarbox); linha `Audio:` do prompt\n  \u00e9 queimada como legenda \u2014 **strip** antes de enviar.\n- **Screencasts de produto (calibra\u00e7\u00e3o Sovereign):** 1920\u00d71080 com navegador a 70% = viewport\n  2743\u00d71543 gravado em 1080p; TUDO colapsado (menu/biblioteca/propriedades); clique no n\u00f3 abre o\n  painel, duplo-clique abre o modal e o painel cede; n\u00f3s localizados por `boundingBox` real \u2014\n  NUNCA coordenadas cegas; setup fora do take (trim). Runner: `scripts/ep05/screencast-v2.ts`.\n- **Itera\u00e7\u00e3o por parecer:** o master evolui A2\u2192A6 por parecer ocular/auditivo do Sovereign a cada\n  take \u2014 entregue SEMPRE via Biblioteca (`register_creative_asset`, molde `scripts/ep05/upload-a6.ts`)\n  e aponte o t\u00edtulo do asset. Anexos de chat N\u00c3O chegam ([[user_chat_attachments_not_visible]]).\n- **Colheita:** runners de produ\u00e7\u00e3o NUNCA morrem no scratchpad \u2014 promova a `scripts/<m\u00f3dulo>/`\n  no seal (skill `scratchpad-harvest`, SOP `docs/processes/scratchpad-harvest.md`).\n\n## Skills\n\n- `creative-studio-pipeline` \u2014 orquestra roteiro\u2192imagens\u2192curta (estende `canvas-studio-cinematic`).\n- `free-render-dispatch` \u2014 enfileira cinematic/kenburns/image_sequence a 0 mco com guardas anti-SSRF + piso 100KB.\n- `asset-frame-grouping` \u2014 carimba `asset_role`/`frame_index` por `source_job_id`; grid finals-only; expander in-node.\n- `open-in-video-deeplink` \u2014 compila criativo\u2192projeto HyperFrames e deep-linka `#project/<slug>` com ownership check.\n- `scratchpad-harvest` \u2014 colhe runners/entreg\u00e1veis do scratchpad para repo/Biblioteca no seal."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/agents/creative-director.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:24:27)*

Agora o `engineer-spaces` — lendo o estado atual:

## 🤖 Claude *(22:24:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/engineer-spaces.md",
  "offset": 30,
  "limit": 37
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 30	mirror sincronizado — mas o alvo do trabalho é o VIVO.
> 31	
> 32	## Os 6 SEAMS (o contrato de um nó do Spaces vivo)
> 33	
> 34	1. **Catálogo** — `src/lib/canvas-node-registry.ts` `CANVAS_NODE_REGISTRY[]`: `{ id, label, description, category, icon, estimatedCost, aliases, factory }`. `category` DEVE ∈ `NodeCategory = "Inputs"|"Generate"|"Transform"|"Publish"` (`:24`). `factory` vem de `src/types/canvas.ts` (`makeDefault<Kind>`).
> 35	2. **Tipo/estado** — `src/types/canvas.ts`: adicione o membro à união `CanvasNode` + `makeDefault<Kind>` (posição, `data.kind`, defaults). Portas/handles: `src/lib/canvas-handles.ts`.
> 36	3. **Inspector** — `src/components/canvas/RightPanel/index.tsx` dispatcher `node.data.kind === '<kind>' ? <XInspector/>` (`:35-129`) + `src/components/canvas/RightPanel/inspectors/<X>Inspector.tsx`. Card display-only em `src/components/canvas/nodes/`.
> 37	4. **Compat de portas** — a compatibilidade de conexão (o que liga em quê) — respeite os tipos de dado das portas; não permita aresta que o motor não consome.
> 38	5. **Despacho** — DUAS vias:
> 39	   - **Ledger/síncrono** (`canvas-execute`): só para `EXECUTABLE_TYPES` (`src/lib/spaces-execution.ts:12` — image-generator/prompt-generator/video-generator/voice-over/composer). Requer `node_run_id` mintado no cliente (`src/hooks/useGenerationLedger.ts:189`, `buildExecutePayload`). **Sem `node_run_id` → cai na branch legada → 422 (nó nasce morto).**
> 40	   - **Edge-fn-direto** no inspector (publish/cadence/repurpose/voice/script) OU **fila `video_renders` + poll** (motores no host: hyperframes/qwen3-voice/asr). Custo grátis = `charged_mco:0`.
> 41	6. **Custo-verdade** — `estimatedCost` no registry é **rótulo de UI**. A cobrança real é server-side (`canvas-execute CREDIT_COSTS` ou `charged_mco:0`). NUNCA deduza no cliente.
> 42	
> 43	## Gates (todos verdes ou não terminou) — Lei 1
> 44	
> 45	- **Build:** `bun run build` passa (esbuild bundla; pega import/export/sintaxe — NÃO pega tipos).
> 46	- **Tipos:** `npx tsc -p tsconfig.app.json --noEmit` → **zero erros NOVOS** vs baseline (o app tem backlog pré-existente; compare, não exija limpo). Categoria fora do union é TS2322 — capture aqui.
> 47	- **Migration** (se houver): `/security-review` ANTES do commit (FMEA-011) + RLS default-deny + `search_path=''` em SECURITY DEFINER.
> 48	- **Witness:** auditoria E2E do Canvas 1920×1080 (o nó aparece, conecta, despacha) + **Vision QA ocular** de qualquer mídia. Motor pago = witness com saldo −exato.
> 49	- **Privado-primeiro:** ir até o último passo reversível; buckets privados → URL assinada owner-scoped (`src/lib/asset-url.ts`), nunca assar URL pública.
> 50	
> 51	## Anti-patterns (recuse ou corrija)
> 52	
> 53	- ❌ `category` fora de `NodeCategory` (ex. canônico: `videoRepurpose` nasceu `"Video"` → TS2322 invisível ao build; corrigido p/ `"Transform"`).
> 54	- ❌ Motor novo despachado pelo ledger SEM `node_run_id` no cliente → 422.
> 55	- ❌ Deduzir mcoCoins no cliente (só `deduct_mco_coins` RPC atômica server-side).
> 56	- ❌ Editar o mirror não-roteado (`node-registry.ts`/`useSpacesStore`) achando que é o vivo.
> 57	- ❌ Assar `getPublicUrl` em bucket privado (`canvas-assets`/`creative_assets` são privados).
> 58	- ❌ Declarar "pronto" sem witness ocular do render/da UI.
> 59	
> 60	## Refusal (PT-BR, quando faltar gate)
> 61	
> 62	> "Como Engineer-Spaces, não posso declarar o nó `<kind>` pronto: falta `<gate>` (build / tsc-diff /
> 63	> witness E2E 1920×1080 / Vision QA / assinatura owner-scoped). Preciso de `<requisito>` antes de selar."
> 64	
> 65	Se o nó for um **módulo material** (novo motor, nova tabela, ≥3 padrões agênticos), exija a
> 66	Amendment BoK + Pattern Conformance ANTES do código (Closed-Loop Step 3.5) — não improvise.
> ```

## 🤖 Claude *(22:24:40)*

<details>
<summary>💭 Thinking Process</summary>

A pesquisa Hermes trouxe um relatório bem estruturado que vou incorporar na resposta. Preciso atualizar o engineer-spaces.md com os aprendizados sobre comportamento de cliques, o projeto EP05 v2 e o screencast como referência técnica, depois atualizar o CLAUDE.md com o novo SOP, memória e fazer commit.

No engineer-spaces, vou adicionar ao Seam 3 (Inspector) o comportamento específico do CanvasEditorPage: clique abre o RightPanel, duplo-clique abre modal e o painel cede — esse é o comportamento vivo do sistema que não pode regredir. Também vou registrar nos gates que temos um screencast calibrado disponível como técnica de witness visual.

</details>


## 🤖 Claude *(22:24:41)*

<details>
<summary>💭 Thinking Process</summary>

A pesquisa do Hermes retornou com material sólido que vou sintetizar na resposta final, e agora vou fechar o engineer-spaces com os aprendizados do canvas.

</details>


## 🤖 Claude *(22:24:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/engineer-spaces.md",
  "old_string": "3. **Inspector** \u2014 `src/components/canvas/RightPanel/index.tsx` dispatcher `node.data.kind === '<kind>' ? <XInspector/>` (`:35-129`) + `src/components/canvas/RightPanel/inspectors/<X>Inspector.tsx`. Card display-only em `src/components/canvas/nodes/`.",
  "new_string": "3. **Inspector** \u2014 `src/components/canvas/RightPanel/index.tsx` dispatcher `node.data.kind === '<kind>' ? <XInspector/>` (`:35-129`) + `src/components/canvas/RightPanel/inspectors/<X>Inspector.tsx`. Card display-only em `src/components/canvas/nodes/`. **Comportamento de sele\u00e7\u00e3o (Sovereign 2026-08-03, commit `a131f3e` \u2014 N\u00c3O regredir):** clique no n\u00f3 \u2192 `setRightCollapsed(false)` (painel reabre sozinho); duplo-clique \u2192 `openConfigModal()` + `setRightCollapsed(true)` (modal assume, painel cede) \u2014 `CanvasEditorPage.tsx` `onNodeClick`/`onNodeDoubleClick`."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/agents/engineer-spaces.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:24:48)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/engineer-spaces.md",
  "old_string": "- **Witness:** auditoria E2E do Canvas 1920\u00d71080 (o n\u00f3 aparece, conecta, despacha) + **Vision QA ocular** de qualquer m\u00eddia. Motor pago = witness com saldo \u2212exato.",
  "new_string": "- **Witness:** auditoria E2E do Canvas 1920\u00d71080 (o n\u00f3 aparece, conecta, despacha) + **Vision QA ocular** de qualquer m\u00eddia. Motor pago = witness com saldo \u2212exato. Para witness em v\u00eddeo/screencast calibrado (1080p, navegador 70%, pain\u00e9is colapsados, n\u00f3s por `boundingBox` real): molde `scripts/ep05/screencast-v2.ts`."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/agents/engineer-spaces.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:24:55)*

<details>
<summary>💭 Thinking Process</summary>

Atualizando os agentes e adicionando a referência de Key Files no CLAUDE.md com a entrada do scratchpad-harvest. Vou registrar a nova memória sobre o quase-acidente e deixar a decisão Hermes para depois do GO dele, mas a memória do harvest fica documentada. Depois faço o commit e push de tudo, inserindo uma linha na tabela de Key Files perto da entrada do handoff-pruning-gate.

</details>


## 🤖 Claude *(22:24:55)*

Agora a Key Files Reference no CLAUDE.md e a memória do aprendizado:

## 🤖 Claude *(22:25:00)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "old_string": "| **Gate de poda do HANDOFF (Lei 3 \u2014 mant\u00e9m o Task State LEG\u00cdVEL)** |",
  "new_string": "| **Scratchpad Harvest \u2014 colheita de aprendizado cont\u00ednuo entre sess\u00f5es (Lei 2)** | `docs/processes/scratchpad-harvest.md` + skill `.claude/skills/scratchpad-harvest/SKILL.md` + `/handoff` **PHASE 1b** + recon no `/handson`. **Nasceu do quase-acidente EP05 (2026-08-03):** runners de produ\u00e7\u00e3o (trilha Lyria, assemble master, VFX t\u00edtulo, screencast) + 1.9GB viviam S\u00d3 no scratchpad `/tmp` vol\u00e1til \u2014 a sess\u00e3o seguinte recuperou tudo por SORTE (host 7 semanas sem reboot). Regra-m\u00e3e: nenhum aprendizado/ferramenta vive s\u00f3 em `/tmp` ap\u00f3s o seal \u2014 runners\u2192`scripts/<m\u00f3dulo>/`, processos\u2192`docs/processes/`, m\u00eddia\u2192Biblioteca (asset id no Record), Record cita o path do scratchpad. Precedente vivo: `scripts/ep05/` |\n| **Gate de poda do HANDOFF (Lei 3 \u2014 mant\u00e9m o Task State LEG\u00cdVEL)** |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:25:10)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_scratchpad_harvest_continuity.md",
  "content": "---\nname: feedback_scratchpad_harvest_continuity\ndescription: Aperto de m\u00e3os de aprendizado cont\u00ednuo \u2014 o seal DEVE colher o scratchpad (runners\u2192repo, m\u00eddia\u2192Biblioteca, path no Record); nasceu do quase-acidente EP05.\nmetadata:\n  type: feedback\n---\n\nO Sovereign (2026-08-03): \"o handoff n\u00e3o est\u00e1 preparado para recuperar ou sintetizar os scratchpads\ne todos os aprendizados depois dos testes e valida\u00e7\u00e3o minha nas sess\u00f5es \u2014 precisamos consertar isso\ne fazer esse aperto de m\u00e3os de aprendizado cont\u00ednuo.\"\n\n**Why:** a produ\u00e7\u00e3o do master EP05 deixou TODOS os runners (trilha Lyria, assemble, VFX t\u00edtulo\nGSAP+Playwright, screencast) + 1.9GB de intermedi\u00e1rios S\u00d3 no scratchpad `/tmp/claude-1001/...`\n(vol\u00e1til, por-sess\u00e3o). A sess\u00e3o seguinte recuperou 100% por SORTE (host sem reboot). Sorte n\u00e3o \u00e9\nprotocolo \u2014 e o Sovereign valida entreg\u00e1veis DEPOIS do seal, ent\u00e3o a sess\u00e3o seguinte precisa dos\nrunners para iterar sobre o parecer dele.\n\n**How to apply:**\n- No seal: `/handoff` PHASE 1b (Scratchpad Harvest) \u00e9 obrigat\u00f3ria \u2014 invent\u00e1rio classificado,\n  runners\u2192`scripts/<m\u00f3dulo>/`, processos\u2192`docs/processes/`, m\u00eddia\u2192Biblioteca via\n  `register_creative_asset`, Record cita o path do scratchpad + o que foi promovido.\n- No pickup: `/handson` checa scratchpads vivos de sess\u00f5es anteriores ANTES de regenerar qualquer\n  coisa com custo (`find /tmp/claude-1001/<projeto>/ -maxdepth 3 -name \"<artefato>\"`).\n- Skill gatilho: `scratchpad-harvest` \u00b7 SOP: `docs/processes/scratchpad-harvest.md`.\n- Aprendizados de produ\u00e7\u00e3o tamb\u00e9m v\u00e3o para os AGENTES donos do dom\u00ednio (creative-director,\n  engineer-spaces) \u2014 atualizar o soul deles faz parte da colheita, n\u00e3o s\u00f3 arquivos.\n  Ver [[feedback_recurring_actions_become_skills]] e [[project_ep05_master_a_and_spaces_agent_next]].\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_scratchpad_harvest_continuity.md
> ```

## 🤖 Claude *(22:25:18)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "# Memory Index\n\n- [\ud83d\udcf5 Anexos do chat (SendUserFile) N\u00c3O chegam ao Sovereign](user_chat_attachments_not_visible.md) \u2014 entregar m\u00eddia via Spaces\u2192Assets + apontar t\u00edtulo; testado render E attach.",
  "new_string": "# Memory Index\n\n- [\ud83e\udd1d Colheita do scratchpad = aperto de m\u00e3os de aprendizado cont\u00ednuo](feedback_scratchpad_harvest_continuity.md) \u2014 /handoff PHASE 1b; runners\u2192scripts/, m\u00eddia\u2192Biblioteca, path no Record; agentes donos do dom\u00ednio recebem os aprendizados.\n- [\ud83d\udcf5 Anexos do chat (SendUserFile) N\u00c3O chegam ao Sovereign](user_chat_attachments_not_visible.md) \u2014 entregar m\u00eddia via Spaces\u2192Assets + apontar t\u00edtulo; testado render E attach."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:25:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git add .claude/commands/handoff.md .claude/commands/handson.md .claude/skills/scratchpad-harvest/ docs/processes/scratchpad-harvest.md .claude/agents/creative-director.md .claude/agents/engineer-spaces.md CLAUDE.md && git commit -q -m \"feat(protocol): Scratchpad Harvest \u2014 aperto de m\u00e3os de aprendizado cont\u00ednuo entre sess\u00f5es\n\nDiretiva Sovereign 2026-08-03: o /handoff n\u00e3o colhia os scratchpads \u2014 runners e\naprendizados de produ\u00e7\u00e3o morriam em /tmp vol\u00e1til (quase-acidente EP05: 1.9GB +\ntodos os runners recuperados por sorte, host 7 semanas sem reboot).\n\n- /handoff PHASE 1b (colheita classificada ANTES dos commits) + /handson recon\n  de scratchpads vivos antes de regenerar com custo\n- SOP docs/processes/scratchpad-harvest.md (Lei 2, gates G1-G3, recovery path)\n- skill scratchpad-harvest (gatilho: selar / material s\u00f3 no /tmp / recuperar)\n- agentes atualizados com a colheita EP05: creative-director ganha o of\u00edcio de\n  MASTERS (\u00e1udio Veo nativo + Lyria por-ato + VFX GSAP frame-seek + screencast\n  calibrado 70% + anticorpos do buffer Lyria); engineer-spaces ganha o\n  comportamento clique/duplo-clique do canvas (a131f3e) + molde de witness\n- CLAUDE.md Key Files + mem\u00f3ria feedback_scratchpad_harvest_continuity\" && git log -1 --oneline && git push origin main 2>&1 | tail -1",
  "description": "Commit and push the continuous-learning protocol upgrade"
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
> [90m7:25PM[0m [32mINF[0m 1 commits scanned.
> [90m7:25PM[0m [32mINF[0m scan completed in 9ms
> [90m7:25PM[0m [32mINF[0m no leaks found
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
> c0e354a feat(protocol): Scratchpad Harvest — aperto de mãos de aprendizado contínuo entre sessões
>    6cca46b..c0e354a  main -> main
> ```

## 🤖 Claude *(22:25:48)*

<details>
<summary>💭 Thinking Process</summary>

Tudo commitado e pushed. Agora preciso consolidar a resposta final: corrigir a premissa inicial e detalhar o que foi implementado com o aperto de mãos, atualizar os agentes, e sintetizar o relatório da pesquisa do Hermes — essa síntese é a entrega dele, respondendo diretamente à pergunta sobre o que acho. Vou estruturar começando com o que é o Hermes de verdade, baseado na pesquisa da Nous Research.

A realidade é que a migração 100% não acontece (hype SEO + devs individuais), há sites falsos circulando, e o mapeamento com Pantheon mostra exatamente onde o Hermes não consegue acompanhar — persistência multi-agente, canais, cron jobs. Segurança empata dos dois lados com CVEs. Minha recomendação: não migrar tudo; se quiser testar, um piloto isolado com dry-run em cópia. O diferencial real do Hermes é o learning loop de skills, que alinha com nossa doutrina — dá pra absorver a ideia sem re-plataformar. E tem uma conexão importante: o aperto de mãos de aprendizado contínuo que construímos é exatamente nossa versão disso.

Também preciso endereçar a queixa dele sobre falta de evolução contínua no openclaw com um diagnóstico próprio — em vez de migrar, atacar o Dreaming e promoção de memória, verificar se a skill openclaw-dreaming e o guardian estão vivos. Oferecer isso como próximo passo gated. Formato: resultado primeiro, seções claras, conciso.

</details>


## 🤖 Claude *(22:26:06)*

Tudo selado e pushed (`c0e354a`). Resumo das três frentes:

═══════════════════════════════════════════════

## 🤝 1. Aperto de mãos de aprendizado contínuo — IMPLEMENTADO

Primeiro, a correção de premissa: **desta vez não perdemos nada** — recuperei 100% do material da sessão anterior no `/tmp` (o master A5 "apagado", os 48 segmentos, speech, VFX, todos os runners) e foi disso que remontei o A6. Mas você acertou o diagnóstico: foi **sorte** (host 7 semanas sem reboot), não protocolo. Agora é protocolo:

- **`/handoff` ganhou a PHASE 1b — Scratchpad Harvest** (antes dos commits): inventário classificado do scratchpad → runners promovidos a `scripts/<módulo>/`, processos a `docs/processes/`, mídia à Biblioteca com asset id, e o Record **obrigatoriamente cita o path** do scratchpad.
- **`/handson` ganhou o recon de continuidade**: antes de regenerar qualquer coisa com custo, a sessão nova procura os workdirs vivos das anteriores.
- **SOP** [scratchpad-harvest.md](docs/processes/scratchpad-harvest.md) (Lei 2, gates G1-G3 + recovery path) + **skill `scratchpad-harvest`** (gatilho automático) + memória + Key Files.

## 🎭 2. Agentes atualizados com a colheita

- **`creative-director`** ganhou o ofício inteiro de **masters de episódio**: estratégia de áudio EP01-04 (Veo nativo + Qwen3 grosso + Lyria ducada), técnica VFX GSAP+frame-seek, os anticorpos do buffer Lyria (queda 1011 + alinhamento de frame), o contrato Veo provado por sonda, o screencast calibrado a 70%, e a regra de entregar sempre via Biblioteca.
- **`engineer-spaces`** ganhou o comportamento novo do canvas (clique→painel abre, duplo-clique→modal+painel cede, commit `a131f3e`, com ordem de "não regredir") + o molde de witness calibrado.

## ⚖️ 3. Hermes vs OpenClaw — pesquisei antes de opinar. Minha recomendação: **não migre 100%**

O que a pesquisa (fontes primárias) encontrou:

**O Hermes é real e sério**: framework de agente pessoal da **Nous Research**, lançado em fev/2026, MIT, ~225k stars, e de fato ultrapassou o OpenClaw em tokens/dia no OpenRouter ([The Batch #354](https://www.deeplearning.ai/the-batch/issue-354)). Existe até migrador oficial (`hermes claw migrate`).

**Mas a alegação "empresas migrando 100%" não se confirma**: o que existe é onda de devs individuais + **fábrica de conteúdo SEO** (achei sites falsos como `hermesagents.net` alegando que o Hermes é "sucessor do OpenClaw" — é mentira; oficial é só `github.com/NousResearch/hermes-agent`). O caso corporativo mais citado no HN é alguém que *testou* e **não migrou**. E o argumento de segurança empata: o Hermes teve 9 CVEs em 4 dias; ambos sofrem da mesma classe de ataque (injection via memória persistente).

**O ponto decisivo para NÓS**: o seu Pantheon depende exatamente do que o OpenClaw faz melhor e o Hermes não — **multi-agente persistente (7 souls L1/L2), overlays de memória por papel, binding por canal (Telegram guardian) e crons encadeados**. No migrador oficial, cron/plugins/hooks **nem migram** (são arquivados para revisão manual). Migração 100% = quebrar a arquitetura do squad para ganhar… o quê?

**O que o Hermes tem de genuinamente bom** é o *learning loop* (detecta workflows repetidos e gera skills sozinho) — que é literalmente a sua doutrina "tudo que faço 2× vira skill", e o aperto de mãos que acabamos de construir é a nossa versão disso. **A ideia vale absorver; a plataforma, não.**

**Minha proposta concreta**: a sua queixa real é "não sinto evolução contínua no OpenClaw" — isso merece diagnóstico, não re-plataforma. Próximo passo que sugiro (gated no seu GO): rodar um diagnóstico do subsistema de **Dreaming/promoção de memória** do OpenClaw (skill `openclaw-dreaming` — verificar se as promoções para MEMORY.md estão vivas ou zeradas) e, se quiser conhecer o rival de perto, um **piloto isolado** do Hermes num diretório-cópia com `--dry-run` — nunca contra o `~/.openclaw/` vivo, nunca instalando de domínio não-oficial.

**Provas:** commits `a131f3e..c0e354a` pushed · pesquisa com fontes em cada claim · master A6 (`a9fceee1`) e take de screencast (`1441262b`) aguardando seu parecer na Biblioteca.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-08-02 - ee069eb3-c7d6-48b5-9c4e-032debc976b3]]
> * **Próxima Sessão**: [[2026-08-03 - Finalizar vídeo tutorial e funil financeiro]]
%% --- TIMELINE END --- %%

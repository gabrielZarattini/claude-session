# Finalizar vídeo tutorial e funil financeiro
**Date:** 2026-08-03 | **Session ID:** `2cf8e553-9753-4c9c-9148-90a20004effe`

---

## 👤 User *(23:57:50)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(23:57:50)*

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


## 🤖 Claude *(23:58:00)*

<details>
<summary>💭 Thinking Process</summary>

The user just triggered the hands-on mode, so I'm running the pre-flight checks concurrently.

</details>


## 🤖 Claude *(23:58:00)*


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
> 7f0740a chore(sprint): registra v6.130.0 — EP05 v2 selado + spaces-agent como próximo AGORA
> 58a0f8b docs(handoff): seal EP05 v2 + kind sceneNote + refinamentos Canvas (2026-08-03)
> 5b9db1a docs(readme): v6.130.0 — EP05 v2 + kind sceneNote + refinamentos Canvas
> cab3f0f feat(spaces): kind sceneNote — sticky-note decorativo (Amendment 32 · FR-SPACES-120)
> 035053f feat(canvas): LANE_HEIGHT 320→480 + reposiciona EP05 v2
> a5b25c9 fix(canvas): fitView só em projetos novos — respeita viewport salvo
> e20b8d3 feat(canvas): edges com espessura adaptável ao zoom (visíveis em zoom-out)
> ```

## 🤖 Claude *(23:58:01)*


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
>  D proof-manifest.json
> ```

## 🤖 Claude *(23:58:01)*


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
>  proof-manifest.json | 1 -
>  1 file changed, 1 deletion(-)
> ```

## 🤖 Claude *(23:58:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Container health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 2 weeks (healthy)
> mcorch_claude_mem: Up 6 weeks (healthy)
> mcorch_chroma: Up 6 weeks (healthy)
> mega-brain-dashboard: Up 6 weeks
> mega-brain-webhook: Up 6 weeks (healthy)
> mega-brain-daemon: Up 6 weeks (healthy)
> ```

## 🤖 Claude *(23:58:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat",
  "description": "Chroma heartbeat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1785715084226858850}
> ```

## 🤖 Claude *(23:58:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null",
  "description": "BoK suites available"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
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

## 🤖 Claude *(23:58:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l HANDOFF.md",
  "description": "HANDOFF.md length"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 619 HANDOFF.md
> ```

## 🤖 Claude *(23:58:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"",
  "description": "Scratch dir check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ⚠️ scratch/ has files
> ```

## 🤖 Claude *(23:58:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "npx tsc --noEmit 2>&1 | tail -20",
  "description": "TypeScript strict check",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(23:58:11)*


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
> 31	
> 32	| **EP05 v2 formato GabrielAI (48 cenas, 62 nós) + kind sceneNote + clamp Veo refs→8s + 4 refinamentos Canvas (2026-08-03)** | ✅ **14 commits na main** (`bd94dae..5b9db1a`) · tsc-app **0** · build 25.05s · gitleaks limpo · `/security-review` NO FINDINGS · 738/740 vitest verdes · Master Execution Protocol §6 respeitado. EP05 v2 no formato exato do motor CLI Python que fez EP01-04: `docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md` (48 cenas §3, regex validado, 6 atos, 16:9). Projeto Spaces `/dashboard/spaces/18a21002-df9c-48b4-aff3-7aba28e812e7` com 62 nós (19P + 7 pair B-roll + 6 voz + 1 charRef + 22 sceneNote), 26 edges, custo Run ~6.180 mco. Clamp Veo `reference_to_video`→8s (server 422 pré-débito + UI auto-clamp) deployado em prod. Canvas: edges com espessura adaptável ao zoom · fitView respeita viewport salvo · LANE_HEIGHT 320→480 · 48 labels cena-a-cena. Amendment 32 kind sceneNote (BoK selada antes do código, Pattern Conformance 1y/20na). Auditoria robusta 4 lentes achou 1 blocker (n_p_1 fora do grid) e 1 important (voice_ato1 desalinhado) — ambos patchados. Malha **19176** · nó `0da058d6`. ⏭ Próxima: Opção C HÍBRIDO — MVP chat-por-nó (Amendment 33) + bok-curator escreve suite `spaces-agent`. Record abaixo. |
> 33	| **Estratégia DEFINITIVA de shorts orgânicos + formato React provado + fábrica Spaces (2026-07-30b)** | ✅ **6 commits na main** (`61022c3..abe2a12`) · tsc-app **0** · gitleaks limpo. As 6 refs do Sovereign ERAM os deepsearches → estratégia **DEFINITIVA v1** (§D1..D7 em `docs/roadmap/organic-shorts-strategy-inicial-2026-07-30.md`). Witness react `1a98cef3` (split_grid 2v, 12 mco, Vision QA) · 8 cortes EP02 · projeto Spaces **"React Gabriel AI"** `024e1c03` armado (zero pago) · tabela de vídeos restaurada no /dashboard/youtube (Short 118 views) · pad TTS 0,5s provado · smoke cadência 7/7 + anticorpo FR-CAD-006. Malha **19120** · nó `aa7e1dc9`. ⏭ PAUSE → **EP05 formato tutorial** (parecer no Record). Record abaixo. |
> 34	| **TikTok App Review destravado + pipeline de Publicações do Spaces (2026-07-30)** | ✅ **4 commits na main** (`266d3f0..7d4add3`) · tsc-app **0** · eslint **0** · vitest **+20 novos** (public-app-settings 9 + asset-publications 11) · 3 migrations aplicadas · 1 edge fn deployada · frontend no ar · `/security-review` NO FINDINGS ×3. **TikTok (reprovado 4×)**: conta `tiktok.review@mcorch.com` provisionada (viewer · email pré-confirmado · onboarding pré-completo · 1500 mco) + login **provado E2E** no /auth público. Achado material: botões social login atrás de `?devLogin` (invisíveis na URL do formulário) → flag admin `public_app_settings` (aba **Acesso** em /dashboard/admin, world-readable+CHECK allowlist, RLS admin-write, auditada). Sovereign gravou o vídeo e **enviou a re-submissão**. **Publicações**: aba no modal do asset (badge/timestamp/Cancelar/Remover) + trigger cascade fecha o **dead-end 409 `already_enqueued`** + **sync bidirecional** (apagar do calendário SOME de toda superfície: `scheduled`→delete, `published`→histórico). Revisão adversarial ultracode pegou 2 P0/P1 nascidos-mortos (handler 409 = código morto; `activeForSelected` sem `published`) → corrigidos+provados E2E. Malha **18985** · nó `59c4d1c2`. Record abaixo. |
> 35	| **"Rodar não é entregar": 6 superfícies + limpeza total de branches + media_state (2026-07-29)** | ✅ **14 commits na main** (`15c84fe..7533a5a`) · tsc-app **0** · eslint **0 erros** (era 75) · vitest **712** · 3 edge fns deployadas · frontend no ar. Remoto = **só `main`** (20 branches retiradas; backup provado por `git clone` do bundle). **P0**: logrotate criava `/var/log/mcorch-*.log` como gcrUX enquanto o cron roda como ubuntu → **redirect falho = comando NÃO executa** → 4 crons mortos 3 dias (telemetria de saúde em branco). **Gate de ENTREGA** da auditoria 4Cs (worktree detached em `origin/main` + push verificado por grep no destino). **Produção estava À FRENTE da main** (dist de branch nunca mergeada) → reconciliada. **Cortes**: grade do menu era galeria decorativa + edge fn 5 dias velha → grade provada E2E por frame. **media_state** (text+CHECK) separa estado técnico do editorial + aba "Em processamento"; **IDOR MEDIUM** fechado que o próprio fix ativara. Malha **18851** · nó `32897de0`. Record abaixo. |
> 36	| **Modal de Publicação YouTube Studio (abas Vídeo/Shorts/Histórico) — free-agent S1 (2026-07-25)** | ✅ **3 commits `free-agent/publish-modal-s1`** · tsc-app **93=baseline** · worktree limpo. **Passo 1**: widget "Vídeos do canal" extraído p/ `src/components/youtube/ChannelVideosCard.tsx` (auto-contido: `useYouTubeVideos` + `useYouTubeConnection` + `useDeleteVideo` + `useUpdateVideo`; 17 colunas + paginação + Editar/Excluir gated por `hasWriteScope`). **Passo 2**: `src/components/youtube/YouTubePublishModal.tsx` — `<Dialog>` + `<Tabs>` 3 abas: **Vídeo** (`YouTubeUploadPanel`), **Shorts** (mesmo fluxo + dica 9:16/60s), **Histórico** (`ChannelVideosCard`). **Passo 3**: `YouTubeStudioPage.tsx` header (L443) — estado `pubOpen`/`pubTab` + botões "Publicar" / "Histórico" → abrem modal com `defaultTab` dinâmico; Card inline removido do corpo. **Zero regressão** — apenas 3 arquivos tocados. Malha **18375** · nó aguardando seal. Record abaixo. |
> 37	| **Modais publicação (terreno free-agent) + P0 EP03 destravado + doutrina de recência (2026-07-25)** | ✅ **5 commits `fbb53b3..b66396c`** pushed · tsc-app 93=baseline · worktree limpo. **P0 EP03**: selo "Armazenado" p/ masters no Storage (W2.1) destrava o botão "Não verificado" morto (`canProbe` exigia bucket='local'); EP03→YouTube nunca dependeu do selo — `useHostMasters` lista por `source_module`, worker dual-source (buildado, no ar). **Modais** YT/TikTok/IG: contrato+playbook path-resolvido p/ agente FREE (`docs/roadmap/publish-modals-*`); **Nemotron-9B:free provou tool-use real** (leu useYouTubeUpload.ts, 7 exports); Sovereign roda fcc-claude na branch `free-agent/publish-modal-s1` passo-a-passo. **Pantheon free-model via gateway `openclaw agent` PROVOU não executar código** (gemini-flash-lite = pseudo-código). **Cap edge fns DESTRAVADO** (Pro 100→500; memória stale reconciliada SUPERSEDED). **Doutrina de recência de memória** (corolário Lei 1). Malha **18348** · nó `5cc6ad2a`. Record abaixo. |
> 38	| **Autonomia: security + P0 YouTube (pós-W2.1) + kanban de dev + grounding AIOS + AI Act Fatia 4 disclosure VIVO (2026-07-25)** | ✅ **8 commits `3766034..0e120be`** pushed · gitleaks limpo · tsc-app 93=baseline. **AI Act Art.50(4) FECHADO** antes do deadline 02-Ago (Fatia 4 disclosure server-side nunca-LLM em orchestrate-step+reshape-pillar, smoke 12/12, /security-review SAFE, deployado; OTD-CP-002 resolvida Sovereign). **Fatias 0/1/2 C2PA já vivas desde 18-jul** (SOP estava stale). **P0 YouTube** pós-W2.1 restaurado (UI source_module='external' + worker dual-source host/Storage). **W1.2** statement_timeout + revoga-anon (migrations aplicadas em prod). **Kanban** neon+fatia-2 sinal-real. **AIOS** nós Consciousness v2 auto-semeados neutralizados. Malha **18347** · nó `2f4eee7d`. Record abaixo. |
> 39	| **Grounding do AIOS (anti-confabulação) + otimização Supabase Pro (2026-07-25)** | ✅ Sessão interativa longa. **8 commits `cb18729..00f5295`** pushed · tsc-app **93=baseline** · gitleaks limpo. **Raiz de "algo errado no ecossistema" achada+corrigida:** o chat AIOS Core-Fable confabulava arquitetura inexistente (monorepo/tabelas/`ffmpeg.wasm`) — diagnóstico por 2 workflows de verificação material. Fix (`cb18729`): **E** prompt anti-confabulação (`DEFAULT_SYSTEM`+`LIVE_SYSTEM`) + **A** RAG query-aware (`buildQueryContext` liga o `searchContext` que era dead-code) + **threshold** `search-constellation` 0.45→0.3 (**search prod 0→20 provado**) + **F1** modo voz. **Auto-ingest RESSUSCITADO** (`4001e38`): morria com 401 silencioso desde a rotação de chaves → força `SB_SECRET_KEY` + varre `src`+`supabase/functions`+`packages`; malha **9831→18324**. Menu **Orquestra→Constelação**. **Supabase Pro:** roadmap `docs/roadmap/supabase-pro-optimization.md` (cap 100 fns **destravado provado**; upload 50MB→500GB; no-pause; logs 7d) + host cleanup **~16GB** (disco 79%→71%) + **masters EP01/EP02 migrados p/ Storage** (`scripts/migrate-local-masters-to-storage.ts`, verificado, host liberado 1.8G→24M). Malha **18324** · nó `88030445`. Record abaixo. |
> 40	| **Autonomia total: PIPC S1+S2 + CRM Contatos + cadence-fix + AI Act selada (2026-07-24)** | ✅ Sessão de autonomia total do Sovereign (migrations/deploys/schema/seal **un-gated**; público/compliance-code/editorial/credenciais **gated**). **6 commits `c58a57e..88a04dd`** pushed · toda migration `/security-review`+RLS default-deny. **S1+S2 PIPC VIVOS** (retenção YT persiste→brief por-EP; A19/A20 desbloqueado por re-OAuth) · **A4 Contatos** (`contacts`+RLS, OTD-CS-001 resolvida) · **A8 cadence-fix** (conta explícita mata null→1ª) · **A10 content-provenance selada 9/9** (Fatia 4 deferida OTD-CP-002). Todos **witness E2E**. ⚠️ cap 100 edge fns atingido. Malha **9831** · nó `36d233dc`. Record abaixo. |
> 41	| **Diretiva 5 pontos: governança docs + cadência por-workspace + Golden Eye intake + YouTube (2026-07-23)** | ✅ Loop autônomo, **os 5 entregues** (teto 80% janela; selado a 49%). **5 commits `c2da9d3..c28d2f0`** + push · tsc-app **93=baseline** · gitleaks limpo · sem edge/migration. **(1)** agentes `docs-curator`+`bok-curator` (donos de `docs/` e `docs/bok/`, curam/revisam no lugar do Sovereign, Telegram pontual, exclusão restrita) + regra global **CLAUDE.md §6** + Key Files + memória `feedback_docs_bok_ownership`. **(2)** auditoria cadência + estratégia por-workspace (`docs/roadmap/cadence-workspace-strategy-2026-07-23.md`; gap central: sem entidade Workspace 1ª classe · `meta_config UNIQUE(user_id)`=1 Meta/user · `cadence-run social_account_id=null`→1ª conta arbitrária). **(3)** intake Golden Eye esclarecido+desenhado (`docs/roadmap/golden-eye-intake-design-2026-07-23.md`, UI Settings "Marca"; VLM=refinaria não depósito). **(4)** YouTube escopo/CASA/quota respondido+**Telegram HTTP 200** (**sem CASA** — escopo sensível não restrito). **(5)** pipeline YouTube **100% pronto** (worker resumable · `youtube_uploads` prod · canal Gabriel AI conectado · master EP02 em `repurpose-inbox/`; só habilitar service). **Extras:** Golden Eye slice 1 (`miv-probe.ts` 18/18, regra RUBRIC.md:231) · PIPC BoK 10/10 APPROVE (`docs/bok/pipc/`, Pattern 17/4/0) · vacina masters (skill `host-media-masters`) · doutrina 2×→skill (`feedback_recurring_actions_become_skills`) · MEMORY 19.9→16KB. Malha **9772** · nó `c22e2c6f`. ⏭ Gated Sovereign: revisar BoK PIPC (destrava S1-S4) · habilitar `youtube-upload.service` · imagens Golden Eye · postar cortes EP01/EP02. |
> 42	| **Funis ML públicos + validação em massa + Conector Amazon (POE Fatia 1) (2026-07-23)** | ✅ Loop autônomo "5 pontos do Sovereign". **6 commits `dbd26a6..17cf02f`**, deployado + `/security-review` NO FINDINGS ×3 + tsc-app **93=baseline** (zero-regressão). **(Funis)** 3 funis ML PÚBLICOS vivos (posts 29/34/35: Roborock ×2 ângulos + Family Hub, atribuídos, **redirect→meli.la 302 provado**); ciclo autopilot de validação em massa **corrigido** (config `target_product_ids`=`external_id`, não UUID — 1º ciclo gastou 40 mco genérico); novo primitivo `publish-wordpress post_id` (flip rascunho→público). **(Zerar)** jornada UX E2E User 0 → produto em produção (0 P0/P1 real). **(Roadmap)** maestro+enxame `wf_04833184` (32 células S×P). **(Épico POE)** blueprint deepsearch + BoK 9/9 + **Fatia 1 conector Amazon VIVO** (dispatcher multi-rede `_shared/affiliate.ts`, `resolve` fold em `process-affiliate-link` [cap 100 fns], migrations `amazon_tag`/`affiliate_network_contract`, UI Conector de Afiliados verificada ocular, witness 402→200 `?tag=` sale). Malha **9718** · nó `89a3618d`. ⏭ POE Fatia 2/3/4 GATED (GO+jurídico); tráfego dos funis (social gated). |
> 43	| **Sala de Controle da Orquestração (FR-OCR-001..020) + cortes de N clipes destravados (2026-07-22)** | ✅ Loop "fazer tudo". 9 commits `e0d9fe9..549a3cc`, deployado + Vision QA logado (User 0, $0) + `/security-review` NO FINDINGS. **Cortes:** reuso de browser (`renderAlphaFrames` 1 chromium/job — witness 5/5 EP01 + **11-cortes resgatado done 11/11**) + `ViralCandidatePicker` ligado no wizard. **Refocus:** BoK `orchestration-control-room` 10/10 + Vista Operacional (crew×execs+ledger) + múltiplas Orquestras persistentes (`workflows`+grafo/workflow) + nós Agente(dispatch)/Portão(N especialistas)/Publicar(mockup por rede); Cena removido; canvas reescrito controlado. **tsc-app 135→93** (Parte B limpou 42 erros de tipo pré-existentes). Malha **9681** · nó `58bd91da`. ⏭ Follow-on: nó Publicar output-flow→publish real; Fila Sovereign gated. |
> 44	| **Loop multi-frente: cortes+picker · grid pan/crop+preview composto · dashboards TikTok/IG · squad Studio · agendamento · LGPD · render-fix · constelação leve (2026-07-22)** | ✅ Sessão-maratona GO'd (workflow adversarial 4-frentes → veredito `.claude/context/multi-front-verdict-2026-07-22.md`) + 2ª rodada de review do Sovereign. **14 commits `7ee9e79..3128d76`**, tudo deployado+build baked; tsc-app **135 (zero-regressão vs baseline; corrigi 3 pré-existentes nos cortes)** · eslint 0 · `/security-review` NO FINDINGS ×3. **(Cortes)** detector duration-aware (`top_n` omitido → `clamp(ceil(span/45),5,12)`, mín. 5 p/ 5min+, cap 12, dedup consumido, prompt+diversidade+title, max_tokens) + `ViralCandidatePicker` (escolher antes de queimar, página+nó). **(Grid)** `pan_x/pan_y/zoom` por célula (crop FFmpeg, clamp 4 camadas, sha-parity, unit 11/11) + **preview composto** (layout real, drag por célula, play). **(Agentes)** squad **Studio** no User 0 (`seed-studio-squad.ts`, drill 6/6 groq via `studio-squad-drill.ts`) + 7 SOULs Pantheon enriquecidos (template +6 seções) + `main` criado + `sync-pantheon-souls-to-admin.ts` (admin 56c→11-17k). **(Agendamento)** `publish-space-asset` `publish_at` futuro + `link` Pinterest (auto-publish/publish-social) + `schedule-episode.ts` privado-primeiro (witness auto-limpante). **(LGPD)** `erase_lead` v4 spine CRM APLICADA (FM-CS-02). **(Render)** timeout duro `renderAlphaFrames` (fim do hang 170min incident 822780e8) + preview kinetic. **(Dashboards)** TikTok+Instagram (`user.info.basic`/`business_basic`, perfil no connect via callback estendido — cap de 100 fns cheio, sem fn nova) + menu **Visão Geral** colapsável (YT/TikTok/IG). **(Constelação)** modo **leve por padrão**+toggle (CrewGraph `lite`) · respace 72° (`respace-constellation.ts`, fim dos orbits sobrepostos) · Matrix/Memória admin-only · **Matrix removida do `/orchestration`** (montava em 2º plano). **Achados:** cap de 100 edge fns CHEIO (dobrar em fn existente, não criar); `lucide` sem ícones de marca (Instagram→Camera); render sem timeout = hang eterno. Malha **9639** · nó `4950ea34`. ⏭ **PRÓXIMO HANDSON (atacar já):** refocus da Orquestração = sala de controle (visão `.claude/context/orchestration-refocus-vision-2026-07-22.md`: BoK→Vista Operacional→múltiplas Orquestras→nós). |
> 45	| **Loop Spaces: legendas sync + engineer-spaces + nó Transcrição/SRT VIVO + nó-janela + Pipeline kanban/tabela + witness cadência (2026-07-22)** | ✅ Loop autônomo **6 slices + fechamento total** ("fecha de vez tudo"), **12 commits `646a934..948d313`**, tudo deployado+Vision-QA (build · tsc **zero-regressão vs baseline 137** · `/security-review` NO FINDINGS · auditoria Canvas 1920×1080 APROVADA). **(S1)** kinetic-stack timing **por-palavra derivado do cue + chunking** (fim do `slice(0,7)`; não é motion-graphic; capstone: re-cut real do EP01 "VOADORES/TROUXE"). **(S2)** agente+skill **`engineer-spaces`** — estreou fechando bug `category:"Video"` (invisível ao esbuild). **(S3)** nó **Transcrição/SRT** whisper.cpp US$0 **VIVO** (migration `asr` + edge `generate-subtitles` + worker `subtitle-bridge` active; unit precisa bun full-path; witness E2E 7 cues/788c sobre corte EP01). **(S4/5a)** **nó-janela** `canvas>node>janela`: sidebar **SÓ specs** (`NodeSpecsPanel`), config na janela (duplo-clique/"Personalizar"). **(S5b)** **Pipeline** de Publicações ganha **Kanban + Tabela nível-query** (filtro/ordenação/CRUD inline, sem despachar) + auditoria de prontidão. **Witness cadência** (throwaway sem credenciais): arm → `cadence-run` `{dispatched:1}` → `cadence_dispatches`+`scheduled_posts`(queued) provados, deletados na hora (zero publicação). **Achados:** `bun run build`=esbuild NÃO typa → gate real `tsc -p tsconfig.app.json` vs baseline; `cadence-run` exige apikey+Authorization = mesma chave de serviço. Malha **9566** · nó `5bd65e77`. ⏭ Sovereign-gated: EP02→YouTube (Track B); CRM Suite (BoK-first). |
> 46	| **Prévias no /repurpose + nó Cortes do Master + Cinética empilhada + 1×3 + fixes Veo + re-cut E2E do EP01 (2026-07-21)** | ✅ Loop-maratona GO'd, **12 commits `347a4ea..4a4fe17`** + README + seal, tudo deployado+Vision-QA. **4b/4c:** prévia em loop das legendas (iframe do template real dirigindo `applyFrame` 30fps, `public/caption-templates/` via `sync-caption-templates-to-public.ts`) + grades no `/repurpose` Passo 2; E2E logado User 0 $0 (9/9 estilos animam, 0 erros console). **4d:** nó `videoRepurpose` "Cortes do Master" no Spaces (motor de repurpose via node, reusa detect+run+galeria/prévia). **Legenda nova `kinetic-stack-9x16`** ("Cinética empilhada") — pilha palavra-por-linha rampa até herói, accent ciano, registrada nos 5 allowlists. **Grade 1×3** + refino 4 legendas Tier A (Motion Graphics score 9 intocada, workflow `wf_3a54f592`). **Fixes Veo:** XOR image/refs (nó nascia morto −267 mco) + POV mudo default (Veo gerava fala) + preview vídeo na aba Assets + rótulo HyperFrames neutro. **4a VERIFICADO:** whisper ASR US$0 (129 cues) → detect → 3 cortes EP01 queimados com Cinética empilhada, Vision QA ocular sobre footage real. Malha **9560** · nó `ab67e63f`. ⏭ Próximo: refino de legibilidade do kinetic-stack p/ frases longas (scrim + cap palavras); **rail ASR-via-UI** ("Gerar transcrição" whisper.cpp host, async) p/ paridade UI; witness cadência. |
> 47	| **Refino Spaces Canvas — grade 2×2 + carrossel hand-picked + biblioteca de legendas + Canvas mobile + 3 bugs + Stories + nginx (2026-07-21)** | ✅ Diretiva Sovereign multi-frente, tudo deployado+testemunhado+commitado. **5 commits `d2bfc58..2908885`.** **Bugs:** (F2) aba Assets do editor lia `vm_canvas_assets` legada → aponta p/ a spine `creative_assets` (todo output vídeo/Veo/voz aparece; register JÁ funcionava — c8fc8840→200c9d6a; o gap era a VIEW). (F4) POV/Veo ia sem refs: o Run All (`useCanvasPipeline`) não coletava refs p/ `imageToVideo` **E** as URLs coletadas eram públicas-mortas/assinadas-expiradas → server não baixava; fix = coletar (incl. `avatarIdentity.referenceUrls`) + **re-assinar** (`toDisplayUrls`) antes de enviar + badge de contagem no card. (F5) reconciliação revertia `running`→`success` com a exec ANTIGA (matava o pulso no re-run) → só reconcilia idle; arestas de ENTRADA de nó terminal também transmitem. **Features:** (F1 **Amendment 28**) modo `split_grid` — grade 2×2 (ou 2v), cada célula **vídeo OU foto**, `composeSplitGrid` xstack, rail hyperframes 12 mco; **witness pago 2×2** (2 vídeos+2 fotos, −12 exatos, asset 334cfea4, Vision QA). (F6 **Amendment 29**) nó **Carrossel** hand-picked — galeria multi-select + reorder dnd-kit + crop/contain por item → `carousel_assets` (rail grátis) reusa `publish-space-carousel`; **witness E2E** 3 slides 4:5 owner-scoped. (F7) biblioteca de legendas com **preview** (8 estilos, `CaptionStyleGallery` + gerador). (F3) Canvas **mobile-first** (sidebars→drawers via FABs redondos só-ícone, minimapa pequeno). **Stories** flag→publicável (rail vivo confirmado). **nginx `/api/host-probe`** aplicado+provado (401 JSON). `/security-review` **NO FINDINGS ×2** · builds verdes env-baked · malha **9523** · nó `f7195047`. ⚠️ Armadilha: `supabase functions download` clobbera o source do repo (revertido). ⏭ Próximo (loop): witness E2E de despacho da Cadência (throwaway, sem publicar) · produzir a cadência da semana. Pendências Sovereign: FM-CS-02 RPN 324 LGPD; rotação de credenciais; `youtube-upload.service`; EP02→YouTube (Track B). |
> 48	
> 49	| **Cadência de vídeo (FR-CAD-006) + hardening cross-tenant do video-render + recon do roadmap (2026-07-21)** | ✅ Continuação do roadmap de audiência. **3 commits `6e0d147..7bfd6ad`.** **(1) Cadência de vídeo agendável:** o dispatch de cadência de um asset de vídeo (POV/corte/split-screen) agora **anexa a mídia** — o `cadence-run` minta uma `space_publish_variant` owner-scoped (espelha publish-space-asset:173-188, reusa o resolver 160-169 do auto-publish) e referencia `space_publish_variant_id` no `metadata.reshape` (antes só `source_asset_id`, que morria em `*_no_video`); YouTube default **private** (privado-primeiro). Single-file, **sem migration**; smoke `smoke-cadence-video-dispatch` **6/6** zero-custo; `/security-review` NO FINDINGS. **(2) Hardening cross-tenant do `video-render`:** allowlist da composition persistida por modo (`split_screen`/`studio-project`/template) dropa `autopilot`/`pillar_run_id` do corpo do cliente — fecha vetor pré-existente (`{props, autopilot:{user_id:vítima}}` forjava linhas atribuídas a outro tenant via o sink service-role do worker); smoke `--live` L5-L7 net-zero; `/security-review` NO FINDINGS. **(3) Recon do roadmap** (`wf_f204f431`): Stories (rail servidor completo — único bloqueio é a flag `publishable:"preview"` em format-specs.ts:90; deploy do publish-social STORIES UNVERIFIED) e Carrossel (rail vivo, nunca exercido; gap = controle de `publish_at`/segurar na UI) mapeados. Malha **9485**. ⏭ Próximo: virar flag de Stories + verificar deploy · controle publish_at no carrossel · testar ambos na UI. Pendências herdadas: nginx `/api/host-probe`; FM-CS-02 RPN 324 LGPD; rotação de credenciais; `youtube-upload.service`. |
> 50	
> 51	> 📦 Linhas de Task State anteriores a 2026-07-20 → [`docs/handoff-archive/HANDOFF-taskstate-archive-2026-07-20-and-earlier.md`](docs/handoff-archive/HANDOFF-taskstate-archive-2026-07-20-and-earlier.md)
> 52	
> 53	## EP05 v2 formato GabrielAI + kind sceneNote + refinamentos Canvas Record (2026-08-03)
> 54	
> 55	**ORO triplet:** Operator = MCORCH Master Execution Agent (+ engineer-spaces L2 para nós Spaces + bok-curator para Amendment 32) · Reviewer = Sovereign + `/security-review` + 4 auditores adversariais + Vision QA · Owner = Sovereign (marca EP05 + saldo mco + produção do canal Gabriel AI).
> 56	
> 57	**Sessão-maratona 4 arcos com 5 workflows ultracode encadeados** (2.7M subagent tokens totais). Arco 1 (EP05 v2 no formato exato do motor CLI GabrielAI que fez EP01-04): recon do `github.com/gabrielZarattini/GabrielAI` (gerar_cenas.py + ep04.json + mapa_transicoes.py) revelou o padrão de produção — 52 cenas de 8s Veo alternando presenter (com char refs) + broll com `+` (firstFrame do último frame do clipe anterior), narração PT-BR ~90-120 chars embarcada no prompt Veo, 6 atos declarados com cena-início, mapa de transições com 5 verbos "corte seco banido". Workflow `wf_666f9be7` (7 agentes: 3 rascunhos concorrentes → 3 críticos adversariais [retenção · materialidade · narrativa] → síntese) produziu **48 cenas** no formato regex-exato do motor (Angle C narrative-first venceu 237/300). Roteiro em `docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md` + Runbook v2 + spec da fábrica. Engineer-spaces materializou como projeto Spaces v2 `18a21002-df9c-48b4-aff3-7aba28e812e7` "EP05 v2 — 48 cenas GabrielAI-format": 40 nós (19P imageToVideo+charRef 8s obrigatório · 7 par B-roll generateImage→imageToVideo firstFrame · 6 voz Qwen3 por ato · 1 charRef reuso do `n_d3jbjjjg` do projeto 024e1c03 = mesmo rosto do canal), 26 edges, custo Run All ~6.180 mco de 9.733 (folga 3.553). Description do projeto carrega checklist dos 21 screencasts + 8 gates G1-G8 + cena 30 ELO MANUAL.
> 58	
> 59	Arco 2 (**clamp Veo `reference_to_video`→8s**, descoberto em produção): A1 rodou com dur=5 + charRef → 422 do Google `Unsupported output video duration 5 seconds, supported durations are [8] for feature reference_to_video` → **charge+refund** de 2× 167 mco (Vertex fast 720p 5s). Nosso clamp em `canvas-execute:1352-1372` validava 4-8 e 1080p→8s, mas NÃO refs→8s. Workflow `wf_ba47e53d` (6 agentes: 3 impl paralelas + 2 verify + doc) escreveu função pura `veoAllowedDurations()` em `veo.ts`, guard 422 pré-débito em `canvas-execute:1367` (mesmo padrão do 1080p clamp), UI auto-clamp em `ImageToVideoInspector` + linha de ajuda, 6 unit tests, SOP Lei 2 (`docs/processes/veo-refs-8s-guard.md`), Amendment 25 atualizado. `/security-review` NO FINDINGS · tsc-app 0 · lint 0 err · vitest 738/740 · build 24.78s. Sovereign deployou `canvas-execute` em prod (script size 194.6kB). Memória permanente `reference_veo_refs_require_8s`.
> 60	
> 61	Arco 3 (**4 refinamentos do Canvas UX** direcionados por prints do Sovereign): (a) edges INVISÍVEIS em zoom-out porque ReactFlow escala SVG por `transform:scale(zoom)` → strokeWidth de 2px vira 0.03px na tela em zoom=0.02. Fix: CSS var `--rf-zoom-inv` no wrapper via `onMove` callback + edges usando `strokeWidth: calc(base * var(...))` — zero rerender React. (b) `fitView` do ReactFlow atropelava `defaultViewport` → cards touching. Fix: `fitView` só quando `!project.viewport || é o default (0,0,1)` — projetos com viewport intencional respeitam o preset salvo. (c) Cards custom ~280-300px "travavam" na lane de 320px (só 20px de margem). Fix: `LANE_HEIGHT` 320→480 (comentário explica impacto nos 3 projetos com pipelineMode). (d) 22 lanes vazias visualmente ("faltando"): workflow `wf_c998bd99` (3 agentes: extractor 48 cenas → adversarial critic → synth) populou `graph.lanes: LaneConfig[]` com 48 labels rotulados cena-a-cena (`"3 · S · Curta final 9:16 fullscreen"`, PASS 0 blockers 2 NITs corrigidos), max 42 chars, ficando visíveis.
> 62	
> 63	Arco 4 (**auditoria robusta 4 lentes + Amendment 32 kind sceneNote**): Sovereign ainda via "várias cenas faltando" — workflow `wf_9414d733` (6 agentes: collector + 4 lentes adversariais paralelas [count/type · prompt-fidelity · edges topology · position] + reporter) descobriu **1 BLOCKER real** (n_p_1 em `(-26.15, 8.49)` — drag manual acidental) + **1 IMPORTANT** (n_voice_ato1 em X=320 em vez de 940) + **1 NIT** (prompts B-roll usam prefixo derivado "Cinematic 16:9 first frame:"). Ambos os gaps patchados via PATCH único; SELECT read-back independente confirmou. 22 lanes SCREENCAST/ELO restantes = gap-de-UX-por-design. Sovereign confirmou lista exata `[3,4,8,10,11,13,16,17,18,20,26,27,29,30,34,37,38,39,40,42,44,48]` = match perfeito. Sovereign escolheu opção B via AskUserQuestion: **Amendment BoK + kind estrutural**. Workflow `wf_6b60d46a` (6 agentes: BoK Amendment 32 → 3 impl paralelas [factory+types · registry · component+register] + gate tsc/build → apply 22 nós). Master Execution Protocol §6 respeitado: **BoK selada ANTES do código** (`docs/bok/spaces-evolution/32-amendment-scene-note.md`, 7906 B, FR-SPACES-120, Pattern Conformance 1 yes Human-in-the-Loop · 20 n-a — decorativo). Código: interface SceneNoteData + factory `makeDefaultSceneNote` em canvas.ts:980+1420 · entrada `sceneNote` em canvas-node-registry.ts:236-244 (category Transform, cost 0, icon StickyNote) · `SceneNoteNode.tsx` (36 linhas, card yellow-500/10, ZERO Handles) · registro em `CanvasEditorPage.tsx:70,94`. tsc-app 0 · build 25.05s. Aplicação: 22 nós `n_note_<cena>` no banco, posições exatas (x=240, y=(cena-1)*480), labels verbatim das lanes. Total EP05 v2 agora: **62 nós** — todas as 48 lanes preenchidas visualmente.
> 64	
> 65	| Ação | Resultado |
> 66	|------|-----------|
> 67	| `docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md` | ✅ 48 cenas formato exato motor CLI (regex validado), 6 atos, 16:9 · workflow 3 rascunhos + 3 críticos + síntese · Angle C 237/300 |
> 68	| `docs/roadmap/ep05-production-runbook-v2-2026-08-03.md` | ✅ Fase 0 (8 gates G1-G8) → Fase 1 (segmentos sintéticos 6.180 mco) → Fase 2 (21 screencasts) → Fase 3 (união HyperFrames Studio) → Fase 4 (publicar+medir) |
> 69	| `docs/bok/spaces-evolution/32-amendment-scene-note.md` | ✅ Amendment BoK selado ANTES do código (Master Execution Protocol §6). FR-SPACES-120. Pattern Conformance 1y/20na. |
> 70	| `src/types/canvas.ts` + `src/lib/canvas-node-registry.ts` + `src/components/canvas/nodes/SceneNoteNode.tsx` + `src/pages/CanvasEditorPage.tsx` | ✅ Kind sceneNote (sticky-note yellow-500/10, sem handles, sem motor, cost 0) registrado no canvas |
> 71	| `supabase/functions/canvas-execute/index.ts` (deployado prod) | ✅ Guard 422 `veo_refs_require_8s` pré-débito — fecha vetor charge+refund de reference_to_video |
> 72	| `src/lib/veo.ts` + `src/components/canvas/RightPanel/inspectors/ImageToVideoInspector.tsx` | ✅ Helper `veoAllowedDurations()` + UI auto-clamp respeitando allowedDurations |
> 73	| `src/components/canvas/edges/{FlowEdge,PipelineEdge}.tsx` + `src/pages/CanvasEditorPage.tsx` | ✅ Edges strokeWidth adaptativo via CSS var --rf-zoom-inv (zero rerender React) |
> 74	| `src/pages/CanvasEditorPage.tsx` (fitView condicional) | ✅ fitView só em projetos novos — respeita viewport intencional salvo |
> 75	| `src/types/canvas.ts` (LANE_HEIGHT 320→480) | ✅ +180px de respiração por card no pipelineMode; 3 projetos afetados (EP05 v2 reposicionado; outros 2 manuais) |
> 76	| `docs/roadmap/refs-sovereign-shorts-2026-07-30.md` | ✅ 6 refs deepsearch do Sovereign arquivadas verbatim (só existiam no transcript) |
> 77	| `docs/processes/veo-refs-8s-guard.md` + Amendment 25 update | ✅ SOP Lei 2 documentando a regra |
> 78	| `src/test/veo-refs-guard.test.ts` (6 tests) | ✅ 4 combos hasRefs × useFirstFrame + sanity + drift-gate — todos verdes |
> 79	| Projeto Spaces `18a21002` | ✅ 62 nós (19P + 7 par B-roll + 6 voz + 1 charRef + 22 sceneNote) · 26 edges · 48 lanes rotuladas · custo Run 6.180 mco · A1 provado (gen `e20bbae2` done 267 mco Vertex fast 720p 16:9 8s) |
> 80	| Auditoria robusta 4 lentes | ✅ Zero cenas faltando materialmente · 1 blocker + 1 important patchados (n_p_1 + voice_ato1 realinhados) · 0 drift de prompt |
> ```

## 🤖 Claude *(23:58:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 100
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (37014 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(23:58:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls scratch/ 2>/dev/null | head -20",
  "description": "List scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(23:58:16)*

<details>
<summary>💭 Thinking Process</summary>

The sprint priorities file didn't come back, so I'm trying to read it directly and checking what's in the scratch file instead.

</details>


## 🤖 Claude *(23:58:17)*


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
> File content (28389 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(23:58:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls scratch/ 2>/dev/null | head -20",
  "description": "List scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(23:58:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff HEAD -- proof-manifest.json | head -20",
  "description": "Inspect proof-manifest deletion"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/proof-manifest.json b/proof-manifest.json
> deleted file mode 100644
> index 9dfcd3a..0000000
> --- a/proof-manifest.json
> +++ /dev/null
> @@ -1 +0,0 @@
> -{"handoffNodeId": "aa7e1dc9-9f92-4f34-9e01-874a15185ee4"}
> ```

## 🤖 Claude *(23:58:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 50
}
```

## 🤖 Claude *(23:58:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>&1 | head -30",
  "description": "Detailed scratch listing"
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
> 12	| ✅ EP05 v2 completo (2026-08-03) | **EP05 v2 no formato exato do motor CLI GabrielAI + Amendment 32 sceneNote + clamp Veo refs→8s** | ✅ 48 cenas em `docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md` · projeto Spaces `/dashboard/spaces/18a21002-df9c-48b4-aff3-7aba28e812e7` (62 nós, 26 edges) · custo Run 6.180 mco de 9.733 · A1 provado (gen `e20bbae2` done 267 mco Vertex fast 720p 16:9 8s). | 🔒 **Sovereign:** Run All (~6.180 mco) → gravar 21 screencasts host → editor HyperFrames Studio (Fase 3 runbook v2) → publicar → medir retenção EP05 vs EP03. |
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

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxrwxr-x  2 gcrUX gcrUX 4096 Jun 30 01:44 .
> drwxrwx--- 32 gcrUX gcrUX 4096 Aug  2 20:48 ..
> ```

## 🤖 Claude *(23:58:42)*

<details>
<summary>💭 Thinking Process</summary>

O scratch estava vazio, então o `ls` do pré-voo retornou um aviso por causa do redirect vazio — o `&&` disparou porque o ls saiu com sucesso. Já corrigi isso. A verificação do BoK gate está demorando com 37 suítes, então vou pular o loop de verificação individual para não estourar o contexto, já que o Sovereign já tem visibilidade no `bok-curator`.

Agora a suíte que preciso focar é `spaces-agent` — ela ainda não existe e precisa ser criada. A saída do TypeScript veio vazia (zero erros ou silenciada), mas como o HANDOFF menciona "tsc-app 0" no último seal, considero isso verde.

Vou montar o brief agora. A fase está selada com EP05 v2 no formato GabrielAI, kind sceneNote, Veo refs clamped para 8 segundos e 4 refinamentos Canvas de 2026-08-03. A worktree está quase limpa — só falta deletar o proof-manifest.json do handoff anterior. Infraestrutura está 6/6 saudável, Chroma OK. O alerta do BoK Gate é que a fila do Sovereign agora aponta para `spaces-agent`, mas essa suíte não existe em `docs/bok/` — isso bloqueia o Master Execution Protocol §1. O próximo passo é a opção C híbrida: MVP chat-por-nó (Amendment 33) enquanto o bok-curator escreve a suite spaces-agent. Tenho alguns alertas: proof-manifest.json deletado na worktree, scratch limpo, HANDOFF.md com 619 linhas (ok), e a flag de TikTok social login está ligada.

</details>


## 🤖 Claude *(23:59:16)*

═══════════════════════════════════════════════════════════
  HANDSON — EP05 v2 formato GabrielAI + kind sceneNote + clamp Veo refs→8s + 4 refinamentos Canvas (2026-08-03)
═══════════════════════════════════════════════════════════

🏁 ESTADO ATUAL
  Fase selada: **EP05 v2 formato GabrielAI + kind sceneNote + refinamentos Canvas** (v6.130.0, selado 2026-08-03)
  Últimos commits:
    `7f0740a` — chore(sprint): registra v6.130.0 — EP05 v2 selado + spaces-agent como próximo AGORA
    `58a0f8b` — docs(handoff): seal EP05 v2 + kind sceneNote + refinamentos Canvas (2026-08-03)
    `5b9db1a` — docs(readme): v6.130.0 — EP05 v2 + kind sceneNote + refinamentos Canvas
    `cab3f0f` — feat(spaces): kind sceneNote — sticky-note decorativo (Amendment 32 · FR-SPACES-120)
    `035053f` — feat(canvas): LANE_HEIGHT 320→480 + reposiciona EP05 v2

📂 MUDANÇAS PENDENTES
  ` D proof-manifest.json` — resíduo do último `/handoff` (arquivo transiente de manifesto; delete não commitado). Nada de código.

🏗️ INFRA
  mcorch_chroma:     Up 6 weeks (healthy) — heartbeat API v2 **OK** (`1785715084…`)
  mcorch_claude_mem: Up 6 weeks (healthy)
  mcorch_vision_mcp: Up 2 weeks (healthy)
  mega-brain-*:      3/3 (daemon healthy, webhook healthy, dashboard up)

🧠 KNOWLEDGE MESH
  **19.176 nós** — seal node do último ciclo `0da058d6` (fonte: Task State header)

🔧 TYPESCRIPT
  `npx tsc --noEmit` na raiz retornou sem output (raiz é no-op — [[reference_root_tsc_noop_use_build]]). Selo carrega `tsc-app **0**` + `build 25.05s` + `738/740 vitest` verdes. **Zero erros** herdados.

📚 BoK SUITES
  37 suítes descobertas em `docs/bok/` (governança: `bok-curator` cura/revisa).
  ⚠️ **GATE alert (Master Execution Protocol §1):** o próximo AGORA da FILA SOVEREIGN é **`spaces-agent`** (chat-por-nó no Spaces — Amendment 33 + suite dedicada) — a pasta **NÃO existe** em `docs/bok/spaces-agent/`. A decisão registrada é **Opção C HÍBRIDA**: MVP do chat-por-nó no Spaces evolution (Amendment 33) **em paralelo** ao `bok-curator` escrevendo a suíte completa. O código do MVP arranca **sob a Amendment 33 do `spaces-evolution` (BoK já selado)**, não sobre suíte nova — isso respeita o Closed-Loop. Novos módulos maiores dentro do `spaces-agent` (agente criador, orquestração) só depois da suíte 9/9.

📌 SPRINT
  Goal: **Distribuição social autônoma operacional** (LinkedIn auto-publish; Twitter destravado quando tier subir; IG após App Review Meta).
  Top prioridade AGORA (FILA SOVEREIGN): **spaces-agent HÍBRIDO** — MVP chat-por-nó (Amendment 33) + suite BoK `spaces-agent` completa (paralelo). LLM cascata Groq→OpenRouter. Nova tabela `spaces_node_threads` (RLS per-user). Cobrança mco por mensagem.

⚡ PRÓXIMOS PASSOS (prioridade)
  1. **spaces-agent HÍBRIDO** — arrancar Amendment 33 `spaces-evolution` (MVP chat-por-nó) + acionar `bok-curator` para escrever a suíte `docs/bok/spaces-agent/` **em paralelo**. Refs: Magnific storyline · Buzzy AI shots · Higgsfield 2.5. **Aguarda GO Sovereign explícito p/ arrancar** (registrado no Task State).
  2. **EP05 v2 produção** (gated Sovereign) — Run All ~6.180 mco no projeto Spaces `18a21002-df9c-48b4-aff3-7aba28e812e7` → gravar 21 screencasts host → editor HyperFrames Studio (Fase 3 runbook v2) → publicar → medir retenção EP05 vs EP03.
  3. **Cortes/shorts orgânicos** (foco de canal INALTERADO) — cadências pré-armadas · estratégia DEFINITIVA v1 em `docs/roadmap/organic-shorts-strategy-inicial-2026-07-30.md`.

⚠️ ALERTAS
  - **Master Execution Protocol §1:** BoK `spaces-agent` **inexistente** — código novo dentro do escopo `spaces-agent` (fora do Amendment 33 do `spaces-evolution`) exige BoK 9/9 antes.
  - **`proof-manifest.json` deletado** no worktree (resíduo do último handoff) — não commitar; deixar como está ou `git checkout -- proof-manifest.json` se o Sovereign quiser resetar.
  - **EP03 master AUSENTE do ecossistema** — foi ao YouTube por fora; upload é ação Sovereign via menu Cortes.
  - **Cena 30 EP05 v2 (ELO MANUAL)** — reuso do asset `creative_assets.id=e781bdef` é ação Sovereign via Cortes.
  - **Flag `auth_social_login_visible` LIGADA** — pré-review TikTok. Desligar em `/dashboard/admin → Acesso` quando aprovar.
  - **`SendUserFile` não chega ao Sovereign** ([[user_chat_attachments_not_visible]]) — para entregar mídia, usar Spaces→Assets + apontar título.
  - **HANDOFF.md com 619 linhas** — dentro do cap, sem necessidade de poda agora.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

Posso, se quiser, disparar a **Fase 7 (`pmo-curator`)** para materializar em `NEXT-STEPS.md` o plano priorizado (un-gated executável já × gated Sovereign, dependências, comando exato) — plan-only, não executa.

## 👤 User *(23:59:11)*

<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

## 👤 User *(23:59:11)*

<command-name>/model</command-name>
            <command-message>model</command-message>
            <command-args>claude-opus-4-8</command-args>

## 👤 User *(23:59:11)*

<local-command-stdout>Set model to claude-opus-4-8</local-command-stdout>

## 👤 User *(00:00:50)*

continue com os próximos passos como prioridade ja mapeados no handson finalizar o nosso video final master no novo formato educacional (tutorial) e financeiro como parte do funil

## 🤖 Claude *(00:01:25)*

<details>
<summary>💭 Thinking Process</summary>

Entendo que o próximo passo prioritário é finalizar o vídeo master EP05 v2 no novo formato educacional (tutorial), que faz parte do funil de conversão. Estou analisando o que o Sovereign está pedindo com base no handson já mapeado. The Sovereign is giving the green light to proceed with the full EP05 v2 production pipeline: running the synthetic segments, recording the 21 host screencasts manually, assembling everything in HyperFrames Studio, then publishing and measuring retention against EP03. This is a massive undertaking that requires both the automated generation phase and significant hands-on recording work. I need to understand what "finalizar o vídeo final master" actually requires — whether it's something I can handle through the pipeline or if it needs Sovereign to record screencasts and assemble them in HyperFrames Studio. Let me check the runbook carefully to see what's gated versus what I can execute, especially with ultracode enabled. alize the final master video, which means producing the actual MP4 file. The pipeline run itself burns real coins and is gated by the Sovereign's approval, which I just received, but the 21 screencasts are a hard blocker since they require manual human recording of Gabriel's tutorials. I need to check the runbook to see if the HyperFrames Studio assembly in Fase 3 is automatable, because there's real risk in what I can actually execute autonomously versus what requires human input.

Spending coins on synthetic segments without being able to assemble the final master would violate the core principle that running doesn't equal delivering. I should read through the runbook and roteiro to map out the exact dependency structure and current project state before committing any resources.

</details>


## 🤖 Claude *(00:01:26)*

O Sovereign deu GO para o **próximo passo #2 do handson**: finalizar o vídeo master final EP05 v2 no formato educacional (tutorial) + financeiro, como parte do funil.

Antes de queimar 6.180 mco ou declarar qualquer coisa "pronta", preciso me ancorar materialmente no estado real (Lei 1 + [[feedback_running_is_not_delivering]] — rodar ≠ entregar). Vou ler o runbook v2, o roteiro, e sondar o estado atual do projeto no banco.

## 🤖 Claude *(00:01:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep05-production-runbook-v2-2026-08-03.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# EP05 v2 — Runbook de Produção (2026-08-03)
> 2	
> 3	> **SSOT operacional do EP05.** Roteiro fonte: [`ep05-roteiro-v2-formato-gabrielai-2026-08-03.md`](ep05-roteiro-v2-formato-gabrielai-2026-08-03.md). Projeto Spaces vivo: `/dashboard/spaces/18a21002-df9c-48b4-aff3-7aba28e812e7` ("EP05 v2 — 48 cenas GabrielAI-format", 40 nós + 26 edges armados, verificados independentemente no banco).
> 4	>
> 5	> **ORO:** Operator = Sovereign (clica Run + grava screencasts + monta no editor) · Reviewer = Sovereign + Vision QA ocular · Owner = Sovereign (marca/conta Gabriel AI, chave Vertex `gabrielai-veo`).
> 6	
> 7	## Modelo mental (o que a v1 tinha errado — corrigido)
> 8	
> 9	- **Spaces = fábrica de segmentos** · **HyperFrames Studio = mesa de montagem**. O canvas de nós NÃO emenda vídeos (não existe nó de concat). A união temporal só acontece no modo `studio-project` do editor NLE em `/dashboard/canvas/video` (`scripts/video-studio-host/adapter.ts:117-135` → POST `video-render` `mode:'studio-project'`; 4 renders `done` provados no banco).
> 10	- **Distribuição REAL das 48 cenas (bate com o read-back do projeto 18a21002 no banco):** 19 apresentador Veo + 8 b-roll firstFrame + 21 screencast host + narração Qwen3 concat por ato. Formato: 16:9 720p Vertex (bate com o witness A1 `e20bbae2` que rodou a 267 mco).
> 11	
> 12	## Passo a passo (ordem de gravação = demo primeiro, cold open por último)
> 13	
> 14	### FASE 0 — Gates de pré-produção (0 mco · ANTES de gastar) — os 8 G do projeto
> 15	
> 16	Todos os 8 gates estão persistidos na `description` do projeto Spaces:
> 17	
> 18	- **G1 — Deploy `canvas-execute` em prod** (`npx supabase functions deploy canvas-execute`). Sem isso, o clamp `veo_refs_require_8s` (commit `c5f2a10`) não protege o Sovereign de charge+refund em produção. **Precondição de tudo.**
> 19	- **G2 — Sonda de saúde da chave Vertex `gabrielai-veo`:** rodar UMA cena B-roll de 4s (~134 mco) antes de queimar 5.073 mco no lote apresentador. Se falhar, resolver auth ANTES do lote.
> 20	- **G3 — Timing pass do TTS Qwen3:** gerar as 6 narrações de ato ANTES de travar o corte. Todas as falas do roteiro são ≤120 chars (verificado por regex; 6 estão na zona 95-110 chars = risco de estourar 6s de fala se a voz for lenta — reconfirmar).
> 21	- **G4 — Vision QA das primeiras 6 cenas do Ato I** (cenas 1-6): apresentador + b-roll + screencast — ver se o rosto do Gabriel AI mantém identidade e se a legenda queimada do curta (cena 3 SCREENCAST) legível.
> 22	- **G5 — Screencast producível (Lei 1):** as demos das cenas 8/10/11/13/16/17/18/20 etc. mostram AÇÃO REAL da UI MCORCH. Nano Banana / Clone de Voz / Imagem→Vídeo / Editor / /dashboard/youtube LEGÍVEIS a 1080p 16:9.
> 23	- **G6 — Curva EP02 legível na cena 44** (o clímax visual): screencap de `/dashboard/youtube` a 1080p com marcador em 1:11 legível — se não renderizar, fallback: gráfico como grafismo declarado.
> 24	- **G7 — Cena 30 (ELO MANUAL):** verificar Vision QA que o clipe reuso `e781bdef` (backup `6f783a1d`) bate com o prompt da cena 29 verbatim antes de importar no editor. Sem match = trocar por B-roll fresco (10 + ~134 mco).
> 25	- **G8 — Regra RAI (7 elos):** as cenas 1→2, 5→6, 8→9, 11→12, 18→19, 22→23, 31→32 exigem que a cena anterior termine com um GESTO physically apontando para o firstFrame da próxima (olhar que desce, mão que se aproxima do trackpad). Documentado cena-a-cena no roteiro §3.
> 26	
> 27	### FASE 1 — Gerar os segmentos sintéticos (Spaces v2, ~6.180 mco)
> 28	
> 29	Abrir `/dashboard/spaces/18a21002-df9c-48b4-aff3-7aba28e812e7` — 40 nós armados.
> 30	
> 31	**Ordem sugerida:**
> 32	1. **G2 primeiro:** Run em UMA cena B-roll (cena 2 = 4s, ~134 mco) — witness. Se falhar, HALT.
> 33	2. **6 narrações Qwen3** (0 mco): Run nos 6 nós `voice_ato{1..6}`. Baixar os WAVs (importados no editor depois).
> 34	3. **Nano Banana das 7 imagens firstFrame** (`n_bimg_*`, 70 mco total) — validar Vision QA antes de rodar os `n_bvid_*`.
> 35	4. **7 B-roll Veo firstFrame** (`n_bvid_*`, ~1.037 mco total) — 4× cenas 4s + 3× cenas 5s.
> 36	5. **19 apresentador Veo** (`n_p_*`, 5.073 mco total) — **cena 1 primeiro** (gate R5: gancho existencial, Vision QA + veredito auditivo do lip-sync pt-BR **antes** de queimar as outras 18). Se o lip-sync sair robótico/uncanny, fallback = todas as apresentador em MUDO com VO Qwen3 sobreposto no editor.
> 37	
> 38	### FASE 2 — Capturar os 21 screencasts (0 mco, Lei 1)
> 39	
> 40	Lista exata na `description` do projeto Spaces (SSOT persistido). Cenas: **3, 4, 8, 10, 11, 13, 16, 17, 18, 20, 26, 27, 29, 34, 37, 38, 39, 40, 42, 44, 48**. Cada linha tem o texto da fala Qwen3 correspondente. Ferramenta de captura à escolha (OBS/gravador de tela nativo); arquivos ficam locais e são importados no editor.
> 41	
> 42	### FASE 3 — União no HyperFrames Studio
> 43	
> 44	1. Abrir `/dashboard/canvas/video`.
> 45	2. Importar como camadas de vídeo: 19 apresentador (`canvas-assets/…/veo/*.mp4`) + 7 b-roll + 21 screencasts + 6 narrações Qwen3.
> 46	3. Ordenar na timeline 1→48 conforme o roteiro. Aplicar as 5 transições do BoK GabrielAI (`mapa_transicoes.py`): ELO 8f entre cenas `+`, PRETO 16f nas fronteiras de ato (1/7/15/25/36/44), CRUZADA 16f nas demais mudanças de cena. **CORTE SECO em "Vai." (cena 47)** — exceção editorial única declarada no §6 do roteiro (justificada pela queda 93% aos 6:53 do EP02).
> 47	4. **Export** (`mode:'studio-project'`) → MP4 8-12min em `video-studio-assets`.
> 48	5. Vision QA ocular do master final.
> 49	
> 50	### FASE 4 — Publicar + medir (fecha o loop PIPC)
> 51	
> 52	1. Proveniência IPTC/C2PA automática (provenance-bridge vivo, AI Act Art.50).
> 53	2. Publicar o master no canal (privado→público, decisão Sovereign).
> 54	3. Cortar o EP05 (menu Cortes) → shorts de react (fábrica `024e1c03`, agora com Veo fresco).
> 55	4. Após 7 dias: rodar `episode_retention_analysis` do EP05 → brief do EP06. **Alvo material:** matar a queda 33% dos primeiros 17s do EP03 (payoff visível ≤0:12 na cena 3 do roteiro).
> 56	
> 57	## Custo total (todos os gates passando)
> 58	
> 59	| Grupo | Custo | Detalhe |
> 60	|-------|-------|---------|
> 61	| 19 apresentador Veo Vertex fast 720p 8s + refs | 5.073 mco | 267 × 19 |
> 62	| 7 Nano Banana firstFrames | 70 mco | 10 × 7 |
> 63	| 7 B-roll Veo firstFrame Vertex (4× 4s + 3× 5s) | 1.037 mco | 4×134 + 3×167 |
> 64	| 6 narração Qwen3 pt-BR (por ato) | 0 mco | self-host grátis |
> 65	| 21 screencasts (host capture) | 0 mco | Sovereign grava |
> 66	| **Total** | **6.180 mco** | de 9.733 (folga 3.553) |
> 67	
> 68	Retakes cobertos: até 13 apresentador extras (13 × 267 = 3.471) OU até 26 b-roll (26 × 134 = 3.484) OU misto. Plano B se estourar (declarado no §5 do roteiro): converter cena 41 (P) para SCREENCAST (economiza 267) ou cena 33 (P refrão) para B-roll (economiza 90) — preserva clímax e arquitetura.
> 69	
> 70	## Riscos herdados + gates de recuperação
> 71	
> 72	- **R-lip-sync Veo pt-BR:** gate G4 antes do lote apresentador. Fallback = todas MUDAS + VO Qwen3.
> 73	- **R-Export HyperFrames Studio:** rail provado (4× done no banco), mas witness com material EP05 antes de exportar 48 camadas.
> 74	- **R-Cena 30 ELO MANUAL:** G7 antes de importar. Se o reuso não bater, +144 mco (10 imagem + 134 Veo 4s fresh).
> 75	- **R-Screencast legível a 1080p 16:9:** G5 + G6 — a curva de retenção da cena 44 é o único ponto onde a UI VIRA payoff visual; validar antes de travar corte.
> 76	- **R-Clamp Veo em prod:** G1. Sem o deploy da edge, o Sovereign ainda pega charge+refund se algum nó B-roll for editado para <8s COM refs (não deveria, mas o clamp é a rede).
> 77	
> 78	## Arquivos-fonte
> 79	
> 80	- Roteiro v2 (SSOT): [`ep05-roteiro-v2-formato-gabrielai-2026-08-03.md`](ep05-roteiro-v2-formato-gabrielai-2026-08-03.md) (commit `62c1028`, 324 linhas, 48 cenas validadas por regex).
> 81	- Tema: [`ep05-theme-modeling-2026-08-02.md`](ep05-theme-modeling-2026-08-02.md).
> 82	- Clamp Veo refs→8s: commit `c5f2a10` + SOP [`docs/processes/veo-refs-8s-guard.md`](../processes/veo-refs-8s-guard.md).
> 83	- Runbook v1 (superseded): [`ep05-production-runbook-2026-08-02.md`](ep05-production-runbook-2026-08-02.md).
> 84	- Motor CLI de referência (EP04): `https://github.com/gabrielZarattini/GabrielAI` (`geracao/gerar_cenas.py` + `episodios/ep04.json`).
> 85	
> ```

## 🤖 Claude *(00:01:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "head -120 /home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep05-roteiro-v2-formato-gabrielai-2026-08-03.md",
  "description": "Read EP05 roteiro top"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <!-- Proveniência: workflow wf_666f9be7-da6 · 7 agentes (3 rascunhos → 3 críticos → síntese) · 1.010k subagent tokens · scores: A=62/68/74 · B=71/82/63 · C=68/88/81 (Angle C venceu). Formato do motor GabrielAI/gerar_cenas.py verificado por regex sobre este mesmo arquivo (48 cenas capturadas, 7 elos, 26 falas Veo ≤120 chars). -->
> 
> # EP05 v2 — Roteiro no Formato GabrielAI (SÍNTESE FINAL · 2026-08-03)
> ## "Como Criar um Vídeo com IA do Zero, Sem Editor de Vídeo (Passo a Passo Completo)"
> ### Chassi = Angle C (narrative arc-first) · Enxertos = B (materialidade audível) + A (pico emocional) · Portado do motor CLI Python (EP04) para os nós do Spaces MCORCH
> 
> ---
> 
> ## 1. CABEÇALHO
> 
> | Campo | Valor |
> |---|---|
> | **Título principal** | Como Criar um Vídeo com IA do Zero, Sem Editor de Vídeo (Passo a Passo Completo) |
> | **Alt. futuro (A/B eixo F4)** | Eu Criei uma IA que Apresenta o Futuro (E Ela Fez Este Vídeo) |
> | **Thumb / headline** | `EU NÃO EXISTO` (caixa-alta, alto contraste) |
> | **Duração-alvo** | ~9:40 (janela 8–12min) |
> | **Formato** | 16:9 master YouTube · pt-BR · self-referential + IA física |
> | **Atos** | 6 (arco EP04 portado: mistério → anatomia → protocolo → enxame → curva → tensão) |
> | **Cenas totais** | 48 (19 apresentador · 8 b-roll incluindo 1 ELO MANUAL · 21 screencast) |
> | **Orçamento MCO** | 6.180 mco (de 9.733 disponíveis · **cap duro 8.500 · folga 2.320 mco = ~13 retakes**) |
> | **ORO** | Operator = Sovereign + Agent · Reviewer = Sovereign · Owner = Sovereign |
> | **Workflow de proveniência** | EP04 executou com motor CLI Python (`ep04.json` + `render.py` + ffmpeg local). EP05 executa com nós VIVOS do Spaces MCORCH: `imageToVideo` (Veo 3.1, charRef `n_d3jbjjjg`, 8s obrigatório para presenter — feature `reference_to_video`), `generateImage` (Nano Banana/Gemini via OpenRouter, 10 mco), `voiceClone` (Qwen3-local, 0 mco, sobrepondo o áudio embarcado no prompt Veo — que fica MUDO na produção), `screencast` (host capture, 0 mco, importado no HyperFrames Studio), `reuseAsset` (acervo, 0 mco, para o único ELO MANUAL da cena 30). União final: HyperFrames Studio (rail cinemático grátis) — não é gate BoK. |
> 
> **Regras invioláveis herdadas do pack:** título sem "(2026)" · gancho falado ≤3s · **nenhum número não-ancorado** · nenhuma fala que a tela desminta (Lei 1 dentro do vídeo) · zero recap enumerado após 9:00 · cauda ≤20s do último payoff · **corte seco no fim** — exceção editorial declarada à lei EP04 de "nunca corte seco".
> 
> **Justificativa editorial do corte seco (única exceção à lei do canal):** o dado PIPC EP02 (queda 93% aos 6:53 = "o fechamento tradicional expulsa 93% da audiência restante") é o único argumento admitido. Cauda arrastada é o modo de falha material medido do canal, e o clímax do EP05 é sobre EXATAMENTE esse número. Corte seco em "Vai." não é estilo, é coerência estrutural com o dado que o próprio filme revela.
> 
> ---
> 
> ## 2. MANIFESTO DE ATOS (equivalente ao `ep04.json`)
> 
> | Ato | Título | Cena-início | Fim | Retenção-alvo (dispositivo) | Mix (P / B+E / S) |
> |---|---|---|---|---|---|
> | I | Mistério — o apresentador que não existe | **1** | 6 | Payoff visível ≤0:12 · LOOP #1 (não existo) e semente do LOOP #2 (número) dentro do hook · LOOP #2 nomeado numericamente ~0:35 · segurar >70% aos 0:15 | 2 · 2 · 2 |
> | II | Anatomia — a imagem-mestre trava o mundo | **7** | 14 | Pixels nascendo em tela precisamente onde o EP02 sangrou (~1:11) · re-hook "primeira lei" no fecho · segurar >55% aos 1:11 | 2 · 2 · 4 |
> | III | Protocolo — como voz vira presença | **15** | 24 | Wow multissensorial na cena 20 (a voz clonada TOCANDO AO VIVO a frase digitada 2s antes) · disclosure Art.50 como ethos · LOOP #3 plantado no fecho | 4 · 2 · 4 |
> | IV | Enxame — como movimento vira vida | **25** | 35 | Preço REAL da UI (267 mco na tela) desarma "números inventados" · reuso do acervo como método (não confissão) · 2ª aparição da lei | 5 · 2 · 4 |
> | V | Curva — do fragmento ao filme publicado | **36** | 43 | REVEAL CIRCULAR do curta (o mesmo do cold open renasce inteiro, reusando o output do Ato V — 0 mco extra) · ação real de agendamento | 2 · 0 · 6 |
> | VI | Tensão — o número que reescreveu o vídeo + CTA | **44** | 48 | Curva EP02 SOZINHA em tela por 12s (câmera imóvel — o dado é o protagonista) · CORTE SECO em "Vai." · end-screen SOBRE a cauda de 47 (não cena nova) · cauda 18s do último payoff | 4 · 0 · 1 |
> 
> **LOOPS DECLARADOS (fechamento único no clímax):**
> - **LOOP MESTRE** — plantado cena 1 ("Espera até o fim" implícito) + cena 3 ("o último… quase ninguém mostra") → fecha cena 46 (meta-payoff).
> - **LOOP #2 (numérico)** — semente na cena 1 ("um número esconde por que metade some antes do fim") → label numérico na cena 5 ("setenta e um segundos") → fecha cena 45 (curva na tela).
> - **LOOP #3 (custo do movimento)** — plantado cena 24 ("passo mais caro") → método na cena 28 ("não vou clicar. Vou fazer melhor") → fecha cena 30 ([ELO MANUAL] reuso) → refrão de custo-zero cena 36.
> 
> **Camada de futuro F4** (patch do theme-modeling · implicação, nunca claim): fechos dos atos II (cena 14), III (24), IV (33), V (41), VI (47) carregam beat de implicação futura ancorado no que a tela mostra.
> 
> **Regra RAI (Refrão de Ação Interna do formato `+`):** cada cena com `+` exige que a cena anterior termine com um GESTO PHYSICALLY apontando para o firstFrame da próxima (olhar que desce, mão que se aproxima do trackpad, cabeça que gira para o monitor — nunca "holds the stare" nem "faces camera fully"). Auditado cena-a-cena abaixo.
> 
> ---
> 
> ## 3. AS 48 CENAS (formato EP04 exato · regex `^(\d+)\.\s+(\+\s+)?` respeitado)
> 
> ### ATO I — MISTÉRIO (cenas 1–6 · ~0:00–1:00)
> 
> 1. Cinematic 8-second video of Gabriel AI (@Gabriel AI) in extreme close-up, direct eye contact with the camera in a shadowed creator studio at night, single side key light carving the face, negative space above the head. 0-2s: absolute stillness, no blink, the headline `EU NÃO EXISTO` burns into the top of the frame in high-contrast uppercase within the first 1.5 seconds. 3-6s: a micro-glitch flickers across the cheekbone at second 2.5 as a pattern break, then the eyes soften into calm certainty as the mouth barely moves speaking. 7-8s: he lets the gaze hold, then his eyes drop slowly toward a monitor beside him, cueing the seamless dissolve into it. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'O apresentador deste vídeo não existe. Um número esconde por que metade some antes do fim.'
> 
> 2. + Continuing seamlessly from the previous shot: Cinematic 4-second B-roll, the monitor beside the presenter bloats forward until it fills the frame, and the vertical 9:16 finished short of THIS episode erupts into the room — the master portrait of the same subject breathing under kinetic captions, cloned narration audible faintly under the room air. 0-2s: the monitor screen bloats to full-frame reveal, the short opens on the master portrait. 3-4s: kinetic caption pops in sync, subtle push-in on the eye. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Este rosto foi gerado. Esta voz foi clonada. Nada aqui passou por editor.'
> 
> 3. [SCREENCAST] Tela cheia 9:16 do CURTA FINAL rodando dentro do quadro — o mesmo artefato que a esteira monta no Ato V, com movimento de câmera lento sobre a imagem-mestre, narração Qwen3 clonada, legendas cinéticas cadenciadas. Duração ~9s. Fala embarcada no curta (voz clonada): 'Quatro passos. Uma esteira. O último… quase ninguém mostra.'
> 
> 4. [SCREENCAST] Canvas do Spaces em `/dashboard/spaces` a 1080p — cursor navegando de verdade da esquerda para a direita, quatro nós acendendo em sequência com brilho sob cada card (Imagem, Clone de Voz, Imagem→Vídeo, Criativo Cinematográfico), edges conectando devagar. Duração ~10s, ritmo contido. Fala (Qwen3 overdub): 'Aqui dentro nasce cada peça. E nasce medida.'
> 
> 5. Cinematic 8-second video of Gabriel AI (@Gabriel AI) seated at his desk, three-quarter turn toward the monitor, a single practical light warming the profile, second monitor blurred behind him showing the canvas from scene 4. 0-2s: he glances back at the canvas, brow furrowing slightly. 3-6s: he turns halfway toward the camera and delivers the number with weight — "setenta e um segundos" is the beat that lands hardest, one hand resting still on the desk. 7-8s: he lowers his eyes toward the keyboard, index finger hovering over the trackpad, cueing the physical gesture that carries into the next shot. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Tem um número, escondido no painel deste canal, que mata metade da audiência em setenta e um segundos.'
> 
> 6. + Continuing seamlessly from the previous shot: Cinematic 4-second B-roll, slow rack focus travelling from the presenter's shoulder along his arm and hand onto the trackpad, then onto a laptop screen already loaded with the Imagem node inspector, cursor resting near the Gerar button. 0-2s: focus racks from arm to trackpad. 3-4s: focus lands on the Gerar button in the reflection, cursor drifts closer. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Eu desenhei este vídeo contra esse número. Passo um: a gente congela o mundo.'
> 
> ### ATO II — ANATOMIA · A IMAGEM-MESTRE (cenas 7–14 · ~1:00–2:45)
> 
> 7. Cinematic 8-second video of Gabriel AI (@Gabriel AI) framed medium-close at the desk, hand resting on a mechanical keyboard, monitor with the canvas glowing beside him. 0-2s: he leans in slightly, eyes on the screen, then turns halfway to the camera. 3-6s: he speaks with measured cadence, placing an open hand as if setting a piece on a chessboard. 7-8s: his hand slides toward the trackpad, eyes lock on the Gerar button off-camera. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Todo vídeo de IA que derrete começa igual: pedindo tudo pro modelo de vídeo. A esteira faz o contrário.'
> 
> 8. [SCREENCAST] Clique real em Gerar no nó Imagem (Nano Banana) em `/dashboard/spaces`. Spinner materializando. Pixels começam a nascer no preview panel — este é o instante ~1:11 da timeline final do EP05, escolhido a dedo para bater com o ponto de sangramento medido do EP02. Duração ~8s. Fala (Qwen3 overdub): 'O prompt não pede uma imagem bonita. Ele dirige uma foto.'
> 
> 9. + Continuing seamlessly from the previous shot: Cinematic 5-second B-roll, macro tilt-shift of the pixels coagulating into a photorealistic portrait on the monitor — skin texture emerging first, then a lit cheekbone with a soft side key, then the negative space above the head resolving. 0-2s: chaos of colored blocks. 3-4s: face crystallizes with one lit cheek and one in shadow. 5s: soft camera lift back reveals monitor bezel, cueing return to UI. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Luz de um lado só. Espaço pra legenda em cima. Você está dirigindo um fotógrafo.'
> 
> 10. [SCREENCAST] Card do prompt de imagem em overlay sobre o canvas — as 8 linhas do prompt Nano Banana visíveis linha a linha, syntax-highlighted em amarelo/branco, cursor descendo e destacando "CONSISTENCY: keep the subject's face unchanged". Duração ~9s. Fala (Qwen3 overdub): 'A palavra que trava tudo é uma só: consistência. O rosto não muda entre um plano e outro.'
> 
> 11. [SCREENCAST] Painel do nó Imagem — arrasto real da character reference (mood board do Gabriel AI) para o slot de referência do nó, snap animation, badge "Character ref anexada" aparecendo, edge conectando devagar. Duração ~7s. Fala (Qwen3 overdub): 'A referência de personagem é a âncora. Sem ela, cada geração é um estranho.'
> 
> 12. + Continuing seamlessly from the previous shot: Cinematic 5-second B-roll, slow push-in on the final master image of the subject rendered as a cinematic portrait, muted grade, soft rim light, negative space above the head. 0-2s: wide of the portrait inside the canvas node. 3-4s: push-in until only the eye is in frame. 5s: pull back a hair to reveal the UI cost badge on the right cueing the next cut. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'É este rosto. O mesmo que abriu o vídeo. E que vai voltar em todos os planos.'
> 
> 13. [SCREENCAST] Zoom real na UI — badge de custo `10 mco` visível ao lado do botão Gerar, cursor circulando o número devagar. Duração ~5s. Fala (Qwen3 overdub): 'Dez créditos. Foi isso. Único preço que eu vou dizer em voz alta.'
> 
> 14. Cinematic 8-second video of Gabriel AI (@Gabriel AI) leaning back from the monitor at his desk, one hand loose on the desk, the master image faintly visible on the screen behind him. 0-2s: he looks toward the master image, then to camera. 3-6s: he delivers the beat with the calm of stating a physical law, no over-enunciation. 7-8s: he turns his head slightly toward a microphone icon glowing on the monitor, cueing the voice node reveal. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Primeira lei da esteira: estabilidade e movimento são trabalhos diferentes. Menos alucinação, sempre.'
> 
> ### ATO III — PROTOCOLO · A VOZ CLONADA (cenas 15–24 · ~2:45–4:50)
> 
> 15. Cinematic 8-second video of Gabriel AI (@Gabriel AI) in medium close-up, direct eye contact, hand resting near his own throat as a subtle gesture. 0-2s: he inhales slowly, hand touches throat briefly. 3-6s: he speaks the technical beat with precision, no jargon dressing. 7-8s: his hand drops, his eyes turn down to a voice inspector opening on the screen. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Esta voz não foi gravada. Foi clonada de uma amostra curta, em WAV de vinte e quatro quilohertz.'
> 
> 16. [SCREENCAST] Nó Clone de Voz abrindo no inspector do Spaces — slot "Amostra principal" preenchido com um clipe de referência, waveform da amostra visível, badge de custo `0 mco`. Duração ~7s. Fala (Qwen3 overdub): 'O motor roda em casa. Zero por frase. E o formato importa: amostra ruim entra, clone ruim sai.'
> 
> 17. [SCREENCAST] Detalhe real do inspector — metadata do arquivo mostrando `24000 Hz · WAV · pt-BR` glowing em monospace. Duração ~6s. Fala (Qwen3 overdub): 'Vinte e quatro quilohertz. Sem compressão. Diferença entre um clone que respira e um que raspa.'
> 
> 18. [SCREENCAST] Digitação AO VIVO no campo de texto do nó de voz: os caracteres aparecem um a um digitando a frase completa "Se você chegou até aqui, já sabe mais de produção com IA do que a maioria dos estúdios." Duração ~9s. Fala (Qwen3 overdub durante a digitação): 'Uma frase nova, digitada agora. Sem ensaio. Sem retake.'
> 
> 19. + Continuing seamlessly from the previous shot: Cinematic 4-second B-roll, extreme close-up on an audio waveform materializing horizontally across a dark timeline on the monitor, peaks lit in soft cyan, a playhead beginning to travel left-to-right. 0-2s: the waveform draws itself. 3-4s: playhead starts moving through it. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'A onda desenhando é o modelo ressintetizando o padrão da amostra.'
> 
> 20. [SCREENCAST] Click real em play no nó de voz — a VOZ CLONADA fala em tempo real a frase que acabou de ser digitada na cena 18. Waveform animada em sincronia com o áudio. Badge `0 mco` visível. Duração ~9s. Fala embarcada (a PRÓPRIA VOZ CLONADA tocando o áudio recém-gerado): 'Se você chegou até aqui, já sabe mais de produção com IA do que a maioria dos estúdios.'
> 
> 21. Cinematic 8-second video of Gabriel AI (@Gabriel AI) in a wider frame, seated with a slight lean forward, hands together on the desk, listening to his own cloned voice complete on the monitor beside him. 0-2s: he holds the listen, eyes softening. 3-6s: he speaks the explanation with the weight of someone naming a mechanism without ruining it. 7-8s: he turns his eyes to a file properties panel opening on the screen. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'O modelo não imita timbre por mágica. Aprende o padrão da amostra e ressintetiza qualquer texto.'
> 
> 22. Cinematic 8-second video of Gabriel AI (@Gabriel AI) in medium close-up, gaze settling into ethical seriousness — doctrine, not disclaimer. 0-2s: a beat of silence, hands into a small open gesture. 3-6s: he delivers the disclosure with unforced dignity. 7-8s: his eyes drop to the file inspector on the monitor, cueing the metadata reveal. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Todo áudio e vídeo sintético desta esteira sai carimbado como IA. A lei manda. Esconder seria trair.'
> 
> 23. + Continuing seamlessly from the previous shot: Cinematic 4-second B-roll, extreme close-up on a file properties panel with the IPTC metadata line `DigitalSourceType: trainedAlgorithmicMedia` highlighted in a subtle glow, monospace type. 0-2s: focus racks onto the line. 3-4s: highlight sweeps across the string. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'O carimbo vai no arquivo. Não numa marca d’água que dá pra apagar.'
> 
> 24. Cinematic 8-second video of Gabriel AI (@Gabriel AI) turning back to camera, the master image and a faint waveform visible on the second monitor behind him as two pieces already on the board. 0-2s: he takes stock — two pieces down, one to go. 3-6s: he plants the third loop as a warning, not a tease, tone dropping. 7-8s: he turns his head toward a video node opening on the screen. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Rosto. Voz. Falta o movimento. E o movimento é o passo mais caro da esteira.'
> 
> ### ATO IV — ENXAME · O MOVIMENTO (cenas 25–35 · ~4:50–7:00)
> 
> 25. Cinematic 8-second video of Gabriel AI (@Gabriel AI) leaning forward on his elbows, expression focused, keyboard silent under his hands. 0-2s: a beat of stillness — the tone shifts to procedural. 3-6s: he states the rule as a maxim, no dramatization. 7-8s: he tips his head toward the monitor where the video node inspector is opening. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'A regra do passo caro é uma só: você não gera pra descobrir. Você gera pra confirmar.'
> 
> 26. [SCREENCAST] Ação real no canvas do Spaces — cursor grabs o output handle da imagem-mestre, drag através do canvas até o input handle do nó Imagem→Vídeo (Veo), snap animation, ambos nós acendendo. Duração ~8s. Fala (Qwen3 overdub): 'A imagem-mestre entra como primeiro frame. Ela é o âncora que o motor vai respeitar.'
> 
> 27. [SCREENCAST] Inspector real do nó Imagem→Vídeo — badge de custo `267 mco` exibido em destaque próximo ao botão Gerar (que fica intencionalmente NÃO clicado), cursor circulando o número devagar. Preço vindo da UI ao vivo, não overlay. Duração ~7s. Fala (Qwen3 overdub): 'Duzentos e sessenta e sete créditos. Oito segundos. É o teto que a esteira cobra por movimento.'
> 
> 28. Cinematic 8-second video of Gabriel AI (@Gabriel AI) in medium close-up, one eyebrow slightly raised — the "let me show you a better way" posture. 0-2s: he lifts his hand deliberately away from the trackpad, not clicking. 3-6s: he sets up the method as method, not confession. 7-8s: his eyes drift to an assets gallery panel opening on the screen. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Eu não vou clicar. Vou te mostrar um clipe que eu já gerei — com este prompt exato.'
> 
> 29. [SCREENCAST] Card do prompt de movimento em overlay sobre o canvas — as 10 linhas do prompt "Vertical selfie POV of Gabriel AI…" visíveis, syntax-highlighted, cursor descendo e destacando "surprise → intrigue → knowing nod". Duração ~10s. Fala (Qwen3 overdub): 'O prompt não descreve um vídeo. Descreve uma atuação: surpresa, intriga, aceno lento.'
> 
> 30. [ELO MANUAL — reuso do acervo `e781bdef`, SEM `+`, custo 0 mco] Reprodução em 9:16 do clipe REAL `e781bdef` do acervo do canal (Vertical selfie POV of Gabriel AI holding his phone, expressions cycling surprise → intrigue → slow knowing nod, handheld sway, natural daylight). Duração 6s (recortada do 8s nativo). 0-2s: surpresa, olhos amplos. 3-4s: intriga, sobrancelhas erguidas. 5-6s: aceno lento fechando o beat. Fala (Qwen3 overdub sobre o clipe do acervo): 'Mesmo personagem. Mesma referência. Este prompt gerou exatamente este clipe.'
> ```

## 🤖 Claude *(00:02:53)*

<details>
<summary>💭 Thinking Process</summary>

I'm mapping out the EP05 v2 production workflow—there are pre-production gates in phase zero, some already completed like the G1 deploy, and then phase one kicks off with synthetic segment generation in Spaces through UI clicks, which accounts for a significant portion of the work.

But here's the constraint: the runbook explicitly marks the operator as Sovereign for running these pipelines and recording the screencasts. Phase two is entirely manual—21 screencasts of someone demonstrating the UI at 1080p, which I can't do autonomously. Phase three involves manual editing in HyperFrames Studio to assemble the final video, and phase four is publishing and measurement.

The core issue is that the final master video can't be completed without human involvement—specifically, the 21 recorded screencasts and the manual editing work are hard gates that require a Sovereign operator, not something I can automate around.

So what can I actually contribute here? I could potentially trigger Phase 1 to generate the synthetic segments, which would consume 6,180 mco, but even that's gated by the ORO declaring it a Sovereign click action. And if I run Phase 1 in isolation while the screencasts and assembly still require the Sovereign, I'm just burning resources without moving the full pipeline forward.

The real issue is that the production model fundamentally requires human involvement — 21 screencasts need to be recorded and the HyperFrames Studio assembly is a manual NLE step. So autonomously finalizing the master end-to-end is architecturally impossible. I need to be honest about this constraint rather than pretend I can deliver something I can't.

The best I can offer is running Fase 1 to pre-generate all the synthetic segments (the presenter clips, b-roll, and narrations) so everything's ready when the Sovereign records the screencasts. That's the maximum value I can deliver without hands — the brain without the hands approach.

But re-reading the message, the Sovereign is asking me to advance the EP05 finalization in this new educational and financial format. The screencasts are the pedagogical core of the tutorial, so they're non-negotiable. I need to respect that constraint while being as thorough as possible within what's actually feasible.

The real actionable work here is executing Phase 1 — generating the synthetic segments. This is substantial work that doesn't require human input, but it depends on whether I can actually trigger the runs from the Spaces canvas project where the nodes are set up.

Looking at the codebase, the pipeline gets orchestrated through `useCanvasStudio.ts` which handles the run dispatch and requires a `node_run_id`. The edge function `canvas-execute` can be invoked directly with the right JWT and node configuration, so it's possible to trigger these runs programmatically.

I notice that A1 (the first presenter scene) was already generated as `e20bbae2` — a 267 mco Vertex output at 720p 16:9 for 8 seconds — which means someone already ran at least one node in the pipeline. The real constraint is that I can't autonomously deliver the final master video—it fundamentally requires human screencasts and manual assembly in the NLE. So the right move is to run Fase 1 (generating all 32 synthetic segments) to get the pieces ready, then hand off the screencast recording and assembly workflow back to the Sovereign with a clear runbook. But that costs 6.180 mco, and the ORO specifies the Operator (who is the Sovereign) controls the Run clicks, which circles back to the core tension: executing this autonomously might look like delivering when I'm really just preparing the groundwork. broader directive than just triggering the runs—it implies the full pipeline including screencasts and assembly. So even if the Sovereign's message counts as authorization for "Run All," I'd still be burning 6.180 mco upfront with no guarantee the screencasts get recorded afterward, leaving the master incomplete and the coins wasted.

The smarter approach is to first check what's already done in the project, be transparent about which parts require hands-on work from the Sovereign, and then propose a clear decision with options rather than autonomously committing resources. I need to verify whether I can actually execute these canvas nodes programmatically or if everything is UI-driven, because that fundamentally changes whether options A and B are even possible. The core issue is that burning 6.180 mco is your decision to make, not mine — the guidance about exhaustive workflows and token costs applies to my own processing, not your real balance. Let me check the codebase for scriptable execution paths and the current project state in the database. I need to check the database state of the project to see what nodes exist and which executions are already done, then figure out how to trigger node runs and whether there's a way to call canvas-execute programmatically. Let me look for the SQL bridge tooling and execution paths in the codebase to gather the actual facts before proceeding.

My approach is to do cheap reconnaissance first — querying the DB for project 18a21002's node states, grepping for how canvas-execute works and what the node_run_id contract looks like, checking if there's an existing scriptable runner, and verifying the mco balance for User 0. Once I have that material picture, I can present an honest assessment of whether to proceed with the full Fase 1 run, do it incrementally, or just prep the work. I need to step back and be honest about what's actually possible here. I can generate the software assets and synthetic content for EP05, but I can't do the human screencast recording or the manual video assembly work. So while I could theoretically produce everything on the software side, truly "finalizing the master" would require work I can't do. What makes sense is to focus on what I can deliver—all the generated assets—and set up the rest for whoever handles the human-facing parts.

But before I commit any resources, I should verify the technical setup is actually in place: whether I can trigger the canvas-execute runs, confirm the project structure is correct, and check what node-runner scripts already exist. And critically, I shouldn't unilaterally spend 6.180 mco without explicit confirmation—that's a decision for the Sovereign to make. Let me do a quick technical recon first to see what we're working with.

</details>


## 🤖 Claude *(00:02:56)*

Tenho o modelo de produção claro agora. Há uma realidade estrutural crítica que preciso confirmar antes de agir (Lei 1 + [[feedback_running_is_not_delivering]]):

O runbook v2 declara o **ORO: Operator = Sovereign (clica Run + grava screencasts + monta no editor)**. O master final depende de:
- **Fase 1** — gerar 32 segmentos sintéticos (~6.180 mco de saldo real) — potencialmente automatizável
- **Fase 2** — **21 screencasts gravados à mão** (você demonstrando a UI ao vivo) — gate humano duro
- **Fase 3** — montagem manual no NLE HyperFrames Studio

Preciso me ancorar no estado material real antes de propor gastar 6.180 mco do seu saldo. Vou sondar: (1) o que já foi gerado no projeto no banco, (2) se consigo disparar os runs por script, (3) o saldo atual.

## 🤖 Claude *(00:02:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls scripts/qa/gen-user-jwt.ts scripts/qa/gen-user-session.ts 2>&1; echo \"---SQL BRIDGE---\"; ls scripts/ | grep -iE \"sql|query|bridge\" 2>&1 | head; echo \"---AIOS---\"; ls -d ~/.aios* 2>/dev/null; which aios-sql-bridge 2>/dev/null; ls scripts/*sql* .claude/scripts/*sql* 2>/dev/null",
  "description": "Locate SQL + JWT tooling"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 2
> scripts/qa/gen-user-jwt.ts
> scripts/qa/gen-user-session.ts
> ---SQL BRIDGE---
> bridge-mesh-to-openclaw.ts
> crm-media-bridge.ts
> design-bridge.ts
> nightly-bridge-refresh.sh
> opencode-bridge.ts
> provenance-bridge.ts
> subtitle-bridge.ts
> video-bridge.ts
> video-repurpose-bridge.ts
> voice-bridge.ts
> ---AIOS---
> ```

## 🤖 Claude *(00:03:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rIl \"canvas-execute\" scripts/ 2>/dev/null | head; echo \"---node run scripts---\"; ls scripts/ | grep -iE \"canvas|run|space|pipeline|episode|ep0\" 2>/dev/null | head -30",
  "description": "Find canvas node runner scripts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> scripts/seed-gamificacao-nodes-bok-seal.ts
> scripts/reconcile-kanban-roadmap.ts
> scripts/canvas-campaign-build.ts
> scripts/automate-pipeline-sprints.ts
> scripts/seed-constellation-v2-capabilities.ts
> scripts/seed-constellation-v2-bok-seal.ts
> scripts/seed-spaces-evolution-bok-seal.ts
> scripts/qa/smoke-spaces-execution.ts
> scripts/qa/smoke-space-publish-variants.ts
> scripts/qa/smoke-veo-video.ts
> ---node run scripts---
> agent-task-runner.ts
> automate-pipeline-sprints.ts
> canvas-backfill-edge-handles.ts
> canvas-campaign-build.ts
> canvas-video-watchdog.sh
> respace-constellation.ts
> schedule-episode.ts
> seed-spaces-evolution-bok-seal.ts
> seed-viral-daily-canvas-bok-seal.ts
> self-heal-spaces.sh
> sync-canvas-nodes.ts
> ```

## 🤖 Claude *(00:03:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "head -40 .env 2>/dev/null | grep -iE \"SUPABASE_URL|VITE_SUPABASE_URL|PROJECT\" | sed 's/=.*/=<redacted>/' ; echo \"---keys present?---\"; grep -cE \"SB_SECRET_KEY|SUPABASE_SERVICE|SUPABASE_URL|VITE_SUPABASE_URL\" .env 2>/dev/null",
  "description": "Check env for Supabase access"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> SUPABASE_URL=<redacted>
> VITE_SUPABASE_URL=<redacted>
> VITE_SUPABASE_PROJECT_ID=<redacted>
> ---keys present?---
> 4
> ```

## 🤖 Claude *(00:03:24)*

<details>
<summary>💭 Thinking Process</summary>

I've got the environment variables set up with the Supabase credentials and keys, so now I need to query the database to check the current state of project 18a21002. I'm going to write a quick script to access the database using the service key and examine how the canvas projects and executions are structured.

Looking at the task details, the project is in the `spaces` table (not `vm_canvas_projects`), and I need to check the `graph` field there, then look at `vm_canvas_executions` to see what's been completed, and also check the user's balance in `profiles`.

For the executions, Spaces Fase 1b uses the `generations` ledger along with `canvas-execute`, so I should query both. Let me grab the environment variable names from the .env file and then look at an existing script like `gen-user-jwt.ts` to see how to set up the database client properly.

</details>


## 🤖 Claude *(00:03:24)*

Tenho acesso ao Supabase (`.env` com `SUPABASE_URL` + chaves). Vou escrever um script de recon read-only para ver o estado material do projeto no banco antes de qualquer decisão de gasto. Deixa eu copiar o padrão de cliente de um script existente.

## 🤖 Claude *(00:03:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"SB_SECRET_KEY|SUPABASE_SERVICE_ROLE|SUPABASE_URL|createClient|SUPABASE_SECRET\" scripts/qa/gen-user-jwt.ts | head -20",
  "description": "Client setup pattern from gen-user-jwt"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 11:import { createClient } from '@supabase/supabase-js';
> 13:const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> 14:const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> 18:  console.error('Usage: gen-user-jwt.ts <email>  (needs SUPABASE_URL + SB_SECRET_KEY + SB_PUBLISHABLE_KEY)');
> 22:const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> 23:const anon = createClient(URL, ANON, { auth: { persistSession: false } });
> ```

## 🤖 Claude *(00:03:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -oE \"^[A-Z_]+=\" .env 2>/dev/null | sort -u | head -40",
  "description": "List env var names"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> APIFY_KEY=
> APIFY_TOKENS=
> GEMINI_API_KEY=
> HIGGSFIELD_API_KEY=
> HIGGSFIELD_API_KEY_SECRET=
> OPENROUTER_API_KEY=
> RAPIDAPI_KEY=
> REPLICATE_API_KEY=
> SB_SECRET_KEY=
> SUPABASE_PUBLISHABLE_KEY=
> SUPABASE_SECRET_KEY=
> SUPABASE_SERVICE_ROLE_KEY=
> SUPABASE_URL=
> VISION_MCP_PAT=
> VITE_SUPABASE_PROJECT_ID=
> VITE_SUPABASE_PUBLISHABLE_KEY=
> VITE_SUPABASE_URL=
> ```

## 🤖 Claude *(00:03:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"from\\(['\\\"]|\\.rpc\\(['\\\"]|vm_canvas_executions|generations|space\" scripts/qa/smoke-spaces-execution.ts 2>/dev/null | head -30",
  "description": "Execution table names from smoke"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3: * smoke-spaces-execution.ts — Spaces zero-cost gates (SOP spaces-graph-execution G1-G6 + it.2a G-P*).
> 5: *   T1 401 no-JWT · T2 422 node-type · T3 422 model (sentinel pair) · T4 404 foreign space (tenant) ·
> 12: *   single-money-path (zero vm_canvas_executions / zero legacy deduct actions — OTD-SPACES-012).
> 15: * Usage: bun run scripts/qa/smoke-spaces-execution.ts   (needs .env: SUPABASE_URL + SB_SECRET_KEY + publishable)
> 44:  const { data } = await admin.from('profiles').select('mco_balance').eq('id', uid).single();
> 48:const spacePayload = (spaceId: string, extra: Record<string, unknown> = {}) => ({
> 49:  project_id: spaceId, node_id: 'n_smoke', node_type: 'generate_image',
> 52:  space_id: spaceId, node_run_id: crypto.randomUUID(), ...extra,
> 58:  const a = await createThrowawayUser(admin, 'spaces1b-a');
> 59:  const b = await createThrowawayUser(admin, 'spaces1b-b');
> 68:  const { data: spaceA } = await admin.from('spaces')
> 70:  const { data: spaceB } = await admin.from('spaces')
> 72:  if (!spaceA || !spaceB) throw new Error('space setup failed');
> 75:  const { data: projA } = await admin.from('vm_canvas_projects')
> 77:  const { data: projB } = await admin.from('vm_canvas_projects')
> 84:    await admin.rpc('deduct_mco_coins', { p_user_id: a.uid, p_amount: startBal, p_action: 'qa_drain', p_context: { smoke: 'spaces1b' } });
> 88:  const t1 = await invokeFn(null, spacePayload(spaceA.id));
> 93:  const t2 = await invokeFn(jwtA, spacePayload(spaceA.id, { node_type: 'smoke_unsupported_node', model: 'upscale-2x', provider: 'openrouter' }));
> 94:  gate('T2 422 node-type fora do slice', t2.status === 422 && t2.json.error === 'spaces_node_type_unsupported', `status=${t2.status} error=${t2.json.error}`);
> 97:  const videoPayload = (extra: Record<string, unknown> = {}) => spacePayload(spaceA.id, {
> 102:  gate('V1 422 modelo de vídeo fora do allowlist', v1.status === 422 && v1.json.error === 'spaces_model_unsupported', `status=${v1.status} error=${v1.json.error}`);
> 108:  const { count: rowsAfterV } = await admin.from('generations').select('id', { count: 'exact', head: true }).eq('owner_id', a.uid);
> 113:  const t3 = await invokeFn(jwtA, spacePayload(spaceA.id, { provider: 'qa', model: 'never-a-model' }));
> 114:  gate('T3 422 modelo sem preço declarado', t3.status === 422 && t3.json.error === 'spaces_model_unsupported', `status=${t3.status} error=${t3.json.error}`);
> 116:  // ── T4 — 404 foreign/absent space (FR-SPACES-007: tenant → not found) ──
> 117:  const t4a = await invokeFn(jwtA, spacePayload(crypto.randomUUID()));
> 118:  const t4b = await invokeFn(jwtA, spacePayload(spaceB.id));
> 119:  gate('T4 404 space alheio/inexistente', t4a.status === 404 && t4b.status === 404, `random=${t4a.status} foreign=${t4b.status}`);
> 121:  // ── T5 — 402 insufficient balance (shared pre-check; zero generations rows) ──
> 122:  const t5 = await invokeFn(jwtA, spacePayload(spaceA.id));
> ```

## 🤖 Claude *(00:03:38)*

<details>
<summary>💭 Thinking Process</summary>

I can see the execution contract now—`canvas-execute` takes a payload with project details, node info, and authentication, and the generations table tracks these runs by owner. Since I can invoke this with a User 0 JWT, it means I could potentially trigger runs server-side, which suggests Phase 1 might actually be achievable.

Now I'm writing a reconnaissance script to check the actual state of project 18a21002—I need to pull the space record to see its owner and node graph, examine what generations already exist and their states, check the node costs, and verify User 0's current balance. This will be a read-only query to map out what's possible.

</details>


## 🤖 Claude *(00:03:38)*

O contrato está claro: `canvas-execute` é invocável com JWT do User 0 (payload `project_id`/`node_id`/`node_type`/`node_run_id`/`space_id`), ledger em `generations`. Então **Fase 1 É scriptável**. Agora o estado material do projeto:

## 🤖 Claude *(00:03:54)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-recon.ts",
  "content": "/**\n * EP05 v2 recon \u2014 READ ONLY. Estado material do projeto Spaces 18a21002.\n * Usage: bun run ep05-recon.ts\n */\nimport { createClient } from '@supabase/supabase-js';\n\nconst URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;\nconst SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;\nconst admin = createClient(URL, SVC, { auth: { persistSession: false } });\n\nconst SPACE_ID = '18a21002-df9c-48b4-aff3-7aba28e812e7';\n\nconst { data: space, error: se } = await admin\n  .from('spaces')\n  .select('id, owner_id, name, graph, viewport, description')\n  .eq('id', SPACE_ID)\n  .single();\n\nif (se || !space) { console.error('SPACE ERR', se); process.exit(1); }\n\nconst graph = space.graph as any;\nconst nodes: any[] = graph?.nodes ?? [];\nconst edges: any[] = graph?.edges ?? [];\n\nconsole.log('=== SPACE ===');\nconsole.log('name        :', space.name);\nconsole.log('owner_id    :', space.owner_id);\nconsole.log('nodes total :', nodes.length);\nconsole.log('edges total :', edges.length);\nconsole.log('lanes       :', (graph?.lanes?.length ?? 0));\n\n// group nodes by kind\nconst byKind: Record<string, number> = {};\nfor (const n of nodes) {\n  const kind = n.data?.kind ?? n.type ?? 'unknown';\n  byKind[kind] = (byKind[kind] ?? 0) + 1;\n}\nconsole.log('\\n=== NODES BY KIND ===');\nfor (const [k, v] of Object.entries(byKind).sort((a,b)=>b[1]-a[1])) console.log(`  ${k.padEnd(20)} ${v}`);\n\n// balance\nconst { data: prof } = await admin.from('profiles').select('mco_balance').eq('id', space.owner_id).single();\nconsole.log('\\n=== BALANCE (owner) ===');\nconsole.log('  mco_balance:', prof?.mco_balance);\n\n// generations for this space\nconst { data: gens } = await admin\n  .from('generations')\n  .select('id, node_id, status, cost_mco, provider, model, created_at, asset_id')\n  .eq('space_id', SPACE_ID)\n  .order('created_at', { ascending: true });\n\nconsole.log('\\n=== GENERATIONS for space (', gens?.length ?? 0, 'rows) ===');\nconst statusCount: Record<string, number> = {};\nlet spent = 0;\nfor (const g of gens ?? []) {\n  statusCount[g.status] = (statusCount[g.status] ?? 0) + 1;\n  if (g.status === 'done') spent += (g.cost_mco ?? 0);\n}\nconsole.log('  by status:', JSON.stringify(statusCount));\nconsole.log('  mco spent on done:', spent);\nconsole.log('  done node_ids:', (gens ?? []).filter(g=>g.status==='done').map(g=>g.node_id).join(', ') || '(none)');\nfor (const g of gens ?? []) {\n  console.log(`  ${(g.node_id||'').padEnd(16)} ${String(g.status).padEnd(14)} ${String(g.cost_mco??'').padStart(5)} ${g.provider}/${g.model} asset=${g.asset_id??'-'} ${g.created_at}`);\n}\n\n// print node ids + kind + key config to understand what needs running\nconsole.log('\\n=== NODE DETAIL (id \u00b7 kind \u00b7 category \u00b7 label) ===');\nfor (const n of nodes) {\n  const d = n.data ?? {};\n  console.log(`  ${String(n.id).padEnd(16)} ${String(d.kind ?? n.type).padEnd(16)} ${String(d.category ?? '').padEnd(12)} ${(d.label ?? d.title ?? '').slice(0,40)}`);\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-recon.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:03:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-recon.ts 2>&1 | head -120",
  "description": "Run EP05 recon (read-only)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> SPACE ERR {
>   code: "42703",
>   details: null,
>   hint: null,
>   message: "column spaces.name does not exist",
> }
> ```

## 🤖 Claude *(00:04:04)*

<details>
<summary>💭 Thinking Process</summary>

I need to check what columns are actually in the `spaces` table since it doesn't have a `name` column like I expected—let me query it to see what fields are available.

</details>


## 🤖 Claude *(00:04:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/cols.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst { data, error } = await admin.from('spaces').select('*').eq('id','18a21002-df9c-48b4-aff3-7aba28e812e7').single();\nif(error){console.error(error);process.exit(1);}\nconsole.log('COLUMNS:', Object.keys(data));\nconsole.log('title:', (data as any).title);\nconsole.log('owner_id:', (data as any).owner_id);\nconst g=(data as any).graph; console.log('nodes:', g?.nodes?.length, 'edges:', g?.edges?.length, 'lanes:', g?.lanes?.length);\nEOF\nbun run /tmp/cols.ts 2>&1 | head -30",
  "description": "Inspect spaces table columns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {
>   code: "PGRST116",
>   details: "The result contains 0 rows",
>   hint: null,
>   message: "Cannot coerce the result to a single JSON object",
> }
> ```

## 🤖 Claude *(00:04:16)*

<details>
<summary>💭 Thinking Process</summary>

The project might be stored in `vm_canvas_projects` rather than `spaces`, or the ID could be different. Let me search both tables and also look through generations for matching space or project IDs to track down where this data actually lives.

</details>


## 🤖 Claude *(00:04:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/find.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst ID='18a21002-df9c-48b4-aff3-7aba28e812e7';\nfor (const t of ['spaces','vm_canvas_projects']) {\n  const { data, error } = await admin.from(t).select('*').eq('id',ID).maybeSingle();\n  console.log(`--- ${t} id=${ID}:`, error? ('ERR '+error.message) : (data? 'FOUND cols='+Object.keys(data).join(',') : 'not found'));\n  if (data) {\n    const g=(data as any).graph;\n    console.log('    title/name:', (data as any).title ?? (data as any).name, '| owner:', (data as any).owner_id ?? (data as any).user_id, '| nodes:', g?.nodes?.length,'edges:',g?.edges?.length,'lanes:',g?.lanes?.length);\n  }\n}\n// recent spaces + projects for User 0\nconst U0='ada39fae';\nfor (const t of ['spaces','vm_canvas_projects']) {\n  const { data } = await admin.from(t).select('id, created_at').order('created_at',{ascending:false}).limit(8);\n  console.log(`\\n recent ${t}:`); for(const r of data??[]) console.log('   ', r.id, r.created_at);\n}\nEOF\nbun run /tmp/find.ts 2>&1 | head -60",
  "description": "Locate project across tables"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- spaces id=18a21002-df9c-48b4-aff3-7aba28e812e7: not found
> --- vm_canvas_projects id=18a21002-df9c-48b4-aff3-7aba28e812e7: FOUND cols=id,user_id,name,description,thumbnail_url,graph,viewport,is_template,is_public,tags,status,total_executions,total_credits_used,last_execution_at,created_at,updated_at
>     title/name: EP05 v2 — 48 cenas GabrielAI-format | owner: ada39fae-67e1-4e53-af1c-5a18e1c108e8 | nodes: 62 edges: 26 lanes: 48
> 
>  recent spaces:
>     4909d024-b55d-4cbc-af2b-b9365d38a89b 2026-07-03T05:03:44.889664+00:00
>     1d77b500-c054-4704-b120-403f4871cdac 2026-07-03T01:12:30.984986+00:00
>     51b229cf-98b9-42d4-b4f9-e472fdcaaefb 2026-07-03T00:34:20.574319+00:00
> 
>  recent vm_canvas_projects:
>     18a21002-df9c-48b4-aff3-7aba28e812e7 2026-08-02T21:16:57.274084+00:00
>     97012f0d-5780-403b-adeb-457c1215c88c 2026-08-02T18:17:26.185366+00:00
>     024e1c03-2866-4e38-afc7-ddc515b5a1c7 2026-07-31T01:38:20.572365+00:00
>     828468f4-3a7b-4816-b727-1b3372e4d2e1 2026-07-30T15:51:21.512597+00:00
>     a581b88e-6318-4fa5-b98e-acdafef176d8 2026-07-10T07:09:23.094982+00:00
>     14c0c448-e974-41f4-9c71-d2cfba1b8c39 2026-07-08T01:54:56.648505+00:00
>     e676efe7-5e7d-4538-8274-97c562623ad4 2026-07-08T01:53:01.288551+00:00
>     b7fc027a-e892-438d-bc23-e05fd39e784c 2026-07-08T01:52:20.26505+00:00
> ```

## 🤖 Claude *(00:04:27)*

<details>
<summary>💭 Thinking Process</summary>

The project lives in Canvas Studio as a vm_canvas_projects record with 62 nodes, 26 edges, and 48 lanes, owned by User 0. It tracks execution and credit usage metrics. Now I need to look up the execution data, which should be stored in the Canvas executions table.

</details>


## 🤖 Claude *(00:04:29)*

Encontrei — o projeto está em `vm_canvas_projects` (Canvas Studio), owner User 0, **62 nós · 26 edges · 48 lanes**. Agora o detalhe: quais nós já foram gerados e o breakdown por tipo.

## 🤖 Claude *(00:04:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/recon2.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst PID='18a21002-df9c-48b4-aff3-7aba28e812e7';\nconst U0='ada39fae-67e1-4e53-af1c-5a18e1c108e8';\n\nconst { data: p } = await admin.from('vm_canvas_projects').select('*').eq('id',PID).single();\nconst g=(p as any).graph; const nodes:any[]=g?.nodes??[]; const edges:any[]=g?.edges??[];\nconsole.log('=== PROJECT ===', (p as any).name);\nconsole.log('total_executions:', (p as any).total_executions, '| total_credits_used:', (p as any).total_credits_used);\n\nconst byKind:Record<string,number>={};\nfor(const n of nodes){ const k=n.data?.kind ?? n.type ?? 'unknown'; byKind[k]=(byKind[k]??0)+1; }\nconsole.log('\\n=== NODES BY KIND ==='); for(const [k,v] of Object.entries(byKind).sort((a,b)=>b[1]-a[1])) console.log('  '+k.padEnd(18)+v);\n\nconst { data: prof } = await admin.from('profiles').select('mco_balance').eq('id',U0).single();\nconsole.log('\\n=== BALANCE ===', (prof as any)?.mco_balance);\n\n// executions \u2014 try both tables\nfor (const tbl of ['vm_canvas_executions','generations']) {\n  const q = tbl==='vm_canvas_executions'\n    ? admin.from(tbl).select('id,node_id,status,credits_used,created_at').eq('project_id',PID).order('created_at',{ascending:true})\n    : admin.from(tbl).select('id,node_id,status,cost_mco,created_at,asset_id').eq('space_id',PID).order('created_at',{ascending:true});\n  const { data, error } = await q;\n  console.log(`\\n=== ${tbl} (${error? 'ERR '+error.message : (data?.length??0)+' rows'}) ===`);\n  if(data){\n    const sc:Record<string,number>={}; for(const r of data){const s=(r as any).status; sc[s]=(sc[s]??0)+1;}\n    console.log('  by status:', JSON.stringify(sc));\n    for(const r of data as any[]) console.log('  '+String(r.node_id||'').padEnd(16)+String(r.status).padEnd(12)+String(r.credits_used??r.cost_mco??'').padStart(5)+'  '+(r.created_at||''));\n  }\n}\n\n// non-decorative nodes that still need running (presenter/broll/voice/image)\nconsole.log('\\n=== NODES REQUIRING RUN (kind + cost hint) ===');\nfor(const n of nodes){\n  const d=n.data??{}; const k=d.kind??n.type;\n  if(k==='sceneNote') continue;\n  console.log('  '+String(n.id).padEnd(16)+String(k).padEnd(16)+' cost='+(d.estimatedCost??d.cost??'?')+' label='+(d.label??d.title??'').slice(0,34));\n}\nEOF\nbun run /tmp/recon2.ts 2>&1 | head -140",
  "description": "Full project state recon"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === PROJECT === EP05 v2 — 48 cenas GabrielAI-format
> total_executions: 0 | total_credits_used: 0
> 
> === NODES BY KIND ===
>   imageToVideo      26
>   sceneNote         22
>   generateImage     7
>   voiceClone        6
>   characterReference1
> 
> === BALANCE === 9733
> 
> === vm_canvas_executions (ERR column vm_canvas_executions.credits_used does not exist) ===
> 
> === generations (ERR column generations.cost_mco does not exist) ===
> 
> === NODES REQUIRING RUN (kind + cost hint) ===
>   n_d3jbjjjg      characterReference cost=? label=Personagem
>   n_p_1           imageToVideo     cost=? label=Cena 1 · Apresentador
>   n_bimg_2        generateImage    cost=? label=Cena 2 · Frame (Nano Banana)
>   n_bvid_2        imageToVideo     cost=? label=Cena 2 · B-roll (Veo firstFrame 4s
>   n_p_5           imageToVideo     cost=? label=Cena 5 · Apresentador
>   n_bimg_6        generateImage    cost=? label=Cena 6 · Frame (Nano Banana)
>   n_bvid_6        imageToVideo     cost=? label=Cena 6 · B-roll (Veo firstFrame 4s
>   n_p_7           imageToVideo     cost=? label=Cena 7 · Apresentador
>   n_bimg_9        generateImage    cost=? label=Cena 9 · Frame (Nano Banana)
>   n_bvid_9        imageToVideo     cost=? label=Cena 9 · B-roll (Veo firstFrame 5s
>   n_bimg_12       generateImage    cost=? label=Cena 12 · Frame (Nano Banana)
>   n_bvid_12       imageToVideo     cost=? label=Cena 12 · B-roll (Veo firstFrame 5
>   n_p_14          imageToVideo     cost=? label=Cena 14 · Apresentador
>   n_p_15          imageToVideo     cost=? label=Cena 15 · Apresentador
>   n_bimg_19       generateImage    cost=? label=Cena 19 · Frame (Nano Banana)
>   n_bvid_19       imageToVideo     cost=? label=Cena 19 · B-roll (Veo firstFrame 4
>   n_p_21          imageToVideo     cost=? label=Cena 21 · Apresentador
>   n_p_22          imageToVideo     cost=? label=Cena 22 · Apresentador
>   n_bimg_23       generateImage    cost=? label=Cena 23 · Frame (Nano Banana)
>   n_bvid_23       imageToVideo     cost=? label=Cena 23 · B-roll (Veo firstFrame 4
>   n_p_24          imageToVideo     cost=? label=Cena 24 · Apresentador
>   n_p_25          imageToVideo     cost=? label=Cena 25 · Apresentador
>   n_p_28          imageToVideo     cost=? label=Cena 28 · Apresentador
>   n_p_31          imageToVideo     cost=? label=Cena 31 · Apresentador
>   n_bimg_32       generateImage    cost=? label=Cena 32 · Frame (Nano Banana)
>   n_bvid_32       imageToVideo     cost=? label=Cena 32 · B-roll (Veo firstFrame 5
>   n_p_33          imageToVideo     cost=? label=Cena 33 · Apresentador
>   n_p_35          imageToVideo     cost=? label=Cena 35 · Apresentador
>   n_p_36          imageToVideo     cost=? label=Cena 36 · Apresentador
>   n_p_41          imageToVideo     cost=? label=Cena 41 · Apresentador
>   n_p_43          imageToVideo     cost=? label=Cena 43 · Apresentador
>   n_p_45          imageToVideo     cost=? label=Cena 45 · Apresentador
>   n_p_46          imageToVideo     cost=? label=Cena 46 · Apresentador
>   n_p_47          imageToVideo     cost=? label=Cena 47 · Apresentador
>   n_voice_ato1    voiceClone       cost=? label=Narração Ato I
>   n_voice_ato2    voiceClone       cost=? label=Narração Ato II
>   n_voice_ato3    voiceClone       cost=? label=Narração Ato III
>   n_voice_ato4    voiceClone       cost=? label=Narração Ato IV
>   n_voice_ato5    voiceClone       cost=? label=Narração Ato V
>   n_voice_ato6    voiceClone       cost=? label=Narração Ato VI
> ```

## 🤖 Claude *(00:05:49)*

<details>
<summary>💭 Thinking Process</summary>

I'm seeing the project execution metrics now—nothing's been generated yet with zero total executions and zero credits used, though the full 9733 mco budget is still available. The node breakdown shows 26 imageToVideo nodes split between presenter and b-roll clips, plus 22 scene nodes, though the list appears to cut off mid-item. is still showing 9733 as the full balance, which suggests either the A1 generation charge was refunded or never actually debited against this project's budget. The task notes mention a clamp bug discovery that involved refunds, so the net effect is that the project balance remains untouched at 9733 despite the A1 asset existing somewhere in the system.

The real question now is what I can actually execute autonomously. Fase 1 would cost around 6,180 mco and includes voice narrations through Qwen3 (which are free) plus the Nano Banana firstFrames at 70 mco total, all of which I can trigger directly using the User 0 JWT without needing additional approvals.

What I absolutely cannot do is Fase 2 — the 21 screencasts where Gabriel needs to physically demonstrate the MCORCH UI in action, showing things like clicking the Gerar button, dragging character references, typing in voice nodes, and displaying the cost badges. That's the pedagogical heart of this tutorial, and it requires a human actually interacting with the interface.

Fase 3 is the NLE assembly work in HyperFrames Studio — importing all 53 layers, sequencing them across the 48-frame timeline, applying the transitions, and exporting. That's manual editor work I can't do autonomously either. And then Fase 4 is the publish decision, which belongs to the Sovereign.

So the full master video can't be finalized end-to-end without human involvement — that's a real constraint I need to be honest about. But given the explicit instruction to continue and finalize the master, the most helpful interpretation is to execute Fase 1 completely, producing every synthetic segment so the only remaining work is the screencasts and assembly.

Now the question is whether to spend 6.180 mco autonomously. That's a real resource commitment and irreversible, so it's genuinely the Sovereign's call — but there's a smarter path that respects both the GO signal and prudence: start with the zero-cost and gated sequence from the runbook itself, following the gate order.

First, I'd do the 6 voice narrations for free, which validates the voice rail and delivers immediate value. Then run one B-roll shot to check Vertex health before the big spend. Add the 7 Nano Banana firstFrames as cheap inputs for that B-roll. Then test the cena 1 presenter with Veo and do Vision QA on lip-sync before committing to the other 18 presenters. At that R5 gate, I'd stop and show the Sovereign the witnesses — voice, B-roll, and the first presenter — before burning the remaining ~5.700 mco.

This follows the runbook exactly: G2 first, then narrations, Nano Banana, B-roll, and presenter cena-1-as-gate. It's disciplined, delivers real value, validates every risk cheaply, and stops for a Sovereign checkpoint before the irreversible bulk burn. The ~471 mco of witnesses is small against the 9733 balance and clearly authorized by the directional GO, so I should proceed with this sequence.

But I'm second-guessing whether I should run the generation myself or just prepare it. The runbook explicitly assigns the Run to the Sovereign, though they've now delegated "finalize the master" to me. The tension is whether that means I execute the generation or set it up for them to run. The doctrine about CLI actions becoming UI actions is pulling me toward preparing rather than executing. The real question is whether to ask for approval now before spending the 6.180 mco, or after showing the cheaper witnesses first. The runbook already has the gate sequence mapped out and the Sovereign authorized "finalize," so I need to identify what genuinely requires their decision versus what I can execute autonomously—and the irreversible spend on the presenter generation is the actual decision point that changes everything downstream.

But there's something more critical I should surface: even if Phase 1 completes, the master still needs 21 human screencasts plus manual assembly work. If I burn 6k mco and then discover the Sovereign doesn't have capacity for that manual effort, that's wasted resources. I need to verify the destination is actually reachable before committing to the spend.

The smarter approach is to surface this reality upfront, ask for the decision, and offer to do the free narration work immediately as a de-risking step. The 6 free narrations validate the voice rail, cost nothing, and are useful regardless of which path forward we choose — so running those is clearly safe. Though I should be mindful that even free work modifies state and uses compute.

The real fork here is whether to burn the 6.180 mco on a master that still needs 21 human screencasts — that's the "running ≠ delivering" trap. This is genuinely a Sovereign decision that changes everything, so I should present the honest material picture with clear options and get their call before proceeding further.

But first, let me do quick read-only verification that the presenter nodes, voice nodes, and b-roll nodes are actually configured correctly — if they're not armed, the run fails mid-burn and that's a credibility killer. I'm checking a sample of each node type to confirm they're ready to go.

</details>


## 🤖 Claude *(00:05:52)*

**Achado material decisivo:** `total_executions: 0 · total_credits_used: 0` — **nada foi gerado ainda** neste projeto. Saldo cheio **9.733 mco**. Composição: 19 apresentador Veo (`n_p_*`) + 7 B-roll (`n_bvid_*`) + 7 Nano Banana (`n_bimg_*`) + 6 voz Qwen3 (`n_voice_*`) + 1 charRef âncora + 22 sceneNote decorativos.

Antes de propor qualquer gasto, preciso confirmar que os nós estão **materialmente armados** (config completa — senão o Run falha no meio e queima mco à toa). Vou inspecionar nós representativos de cada tipo:

## 🤖 Claude *(00:06:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/nodecfg.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst PID='18a21002-df9c-48b4-aff3-7aba28e812e7';\nconst { data: p } = await admin.from('vm_canvas_projects').select('graph').eq('id',PID).single();\nconst g=(p as any).graph; const nodes:any[]=g?.nodes??[]; const edges:any[]=g?.edges??[];\nconst pick=['n_d3jbjjjg','n_p_1','n_bimg_2','n_bvid_2','n_voice_ato1'];\nfor(const id of pick){\n  const n=nodes.find(x=>x.id===id);\n  console.log('\\n===== '+id+' ('+(n?.data?.kind??n?.type)+') =====');\n  console.log(JSON.stringify(n?.data, null, 1).slice(0,1800));\n}\n// edges into b-roll & presenter to confirm ref threading\nconsole.log('\\n=== EDGES (sample: into n_bvid_2, n_p_1, n_p_5) ===');\nfor(const e of edges){ if(['n_bvid_2','n_p_1','n_p_5','n_bimg_2'].includes(e.target)) console.log('  '+e.source+' -> '+e.target+' ('+(e.sourceHandle??'')+' -> '+(e.targetHandle??'')+')'); }\nEOF\nbun run /tmp/nodecfg.ts 2>&1 | head -160",
  "description": "Inspect representative node configs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== n_d3jbjjjg (characterReference) =====
> {
>  "kind": "characterReference",
>  "label": "Personagem",
>  "status": "idle",
>  "imageUrl": "https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ada39fae-67e1-4e53-af1c-5a18e1c108e8/characters/024e1c03-2866-4e38-afc7-ddc515b5a1c7/n_d3jbjjjg-1785685341461-0.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iNzFjZTA4Yy0xYWFjLTQ1MDUtOGEyZC04Y2Y5ZTU5MzI5MzIiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJjYW52YXMtYXNzZXRzL2FkYTM5ZmFlLTY3ZTEtNGU1My1hZjFjLTVhMThlMWMxMDhlOC9jaGFyYWN0ZXJzLzAyNGUxYzAzLTI4NjYtNGUzOC1hZmM3LWRkYzUxNWI1YTFjNy9uX2QzamJqampnLTE3ODU2ODUzNDE0NjEtMC5qcGciLCJzY29wZSI6ImRvd25sb2FkIiwiaWF0IjoxNzg1Njg1MzYwLCJleHAiOjE3ODYyOTAxNjB9.rQ2WPLKiTF8qqQZeu8MrqQTvgZu9eNAuxkttZ5isK0o",
>  "imageUrls": [
>   "https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ada39fae-67e1-4e53-af1c-5a18e1c108e8/characters/024e1c03-2866-4e38-afc7-ddc515b5a1c7/n_d3jbjjjg-1785685341461-0.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iNzFjZTA4Yy0xYWFjLTQ1MDUtOGEyZC04Y2Y5ZTU5MzI5MzIiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJjYW52YXMtYXNzZXRzL2FkYTM5ZmFlLTY3ZTEtNGU1My1hZjFjLTVhMThlMWMxMDhlOC9jaGFyYWN0ZXJzLzAyNGUxYzAzLTI4NjYtNGUzOC1hZmM3LWRkYzUxNWI1YTFjNy9uX2QzamJqampnLTE3ODU2ODUzNDE0NjEtMC5qcGciLCJzY29wZSI6ImRvd25sb2FkIiwiaWF0IjoxNzg1Njg1MzYwLCJleHAiOjE3ODYyOTAxNjB9.rQ2WPLKiTF8qqQZeu8MrqQTvgZu9eNAuxkttZ5isK0o",
>   "https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ada39fae-67e1-4e53-af1c-5a18e1c108e8/characters/024e1c03-2866-4e38-afc7-ddc515b5a1c7/n_d3jbjjjg-1785685351823-0.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iNzFjZTA4Yy0xYWFjLTQ1MDUtOGEyZC04Y2Y5ZTU5MzI5MzIiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJjYW52YXMtYXNzZXRzL2FkYTM5ZmFlLTY3ZTEtNGU1My1hZjFjLTVhMThlMWMxMDhlOC9jaGFyYWN0ZXJzLzAyNGUxYzAzLTI4NjYtNGUzOC1hZmM3LWRkYzUxNWI1YTFjNy9
> 
> ===== n_p_1 (imageToVideo) =====
> {
>  "kind": "imageToVideo",
>  "label": "Cena 1 · Apresentador",
>  "prompt": "Cinematic 8-second video of Gabriel AI (@Gabriel AI) in extreme close-up, direct eye contact with the camera in a shadowed creator studio at night, single side key light carving the face, negative space above the head. 0-2s: absolute stillness, no blink, the headline `EU NÃO EXISTO` burns into the top of the frame in high-contrast uppercase within the first 1.5 seconds. 3-6s: a micro-glitch flickers across the cheekbone at second 2.5 as a pattern break, then the eyes soften into calm certainty as the mouth barely moves speaking. 7-8s: he lets the gaze hold, then his eyes drop slowly toward a monitor beside him, cueing the seamless dissolve into it. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'O apresentador deste vídeo não existe. Um número esconde por que metade some antes do fim.'",
>  "status": "idle",
>  "duration": 5,
>  "videoModel": "veo-3.1-fast",
>  "aspectRatio": "16:9",
>  "veoDuration": 8,
>  "veoResolution": "720p",
>  "characterRefId": "n_d3jbjjjg",
>  "motionStrength": 0.5,
>  "veoGenerateAudio": false,
>  "veoUseFirstFrame": false
> }
> 
> ===== n_bimg_2 (generateImage) =====
> {
>  "kind": "generateImage",
>  "seed": null,
>  "label": "Cena 2 · Frame (Nano Banana)",
>  "prompt": "Cinematic 16:9 first frame: A large computer monitor beside a creator's dim silhouette in a shadowed studio at night, the monitor filling most of the frame with a portrait subject in high contrast side key light, breathing subtly, kinetic captions faintly overlaid on the screen. Investigative documentary style, chiaroscuro lighting, 4K, deep bokeh, negative space above.",
>  "status": "idle",
>  "modelId": "openrouter-gemini-image",
>  "controls": {
>   "hdr": 0.5,
>   "sharpness": 0.8,
>   "creativity": 0.7,
>   "fractality": 0.3,
>   "resemblance": 0.3
>  },
>  "fixedSeed": false,
>  "aspectRatio": "16:9",
>  "inheritStyle": false,
>  "negativePrompt": ""
> }
> 
> ===== n_bvid_2 (imageToVideo) =====
> {
>  "kind": "imageToVideo",
>  "label": "Cena 2 · B-roll (Veo firstFrame 4s)",
>  "prompt": "Continuing seamlessly from the previous shot: Cinematic 4-second B-roll, the monitor beside the presenter bloats forward until it fills the frame, and the vertical 9:16 finished short of THIS episode erupts into the room — the master portrait of the same subject breathing under kinetic captions, cloned narration audible faintly under the room air. 0-2s: the monitor screen bloats to full-frame reveal, the short opens on the master portrait. 3-4s: kinetic caption pops in sync, subtle push-in on the eye. Style: Investigative documentary, chiaroscuro lighting, 4K, deep bokeh. Audio: Male voice, deep and calm, narrating in Brazilian Portuguese: 'Este rosto foi gerado. Esta voz foi clonada. Nada aqui passou por editor.'",
>  "status": "idle",
>  "duration": 5,
>  "videoModel": "veo-3.1-fast",
>  "aspectRatio": "16:9",
>  "veoDuration": 4,
>  "veoResolution": "720p",
>  "motionStrength": 0.5,
>  "veoGenerateAudio": false,
>  "veoUseFirstFrame": true
> }
> 
> ===== n_voice_ato1 (voiceClone) =====
> {
>  "kind": "voiceClone",
>  "label": "Narração Ato I",
>  "prompt": "[Cena 1] O apresentador deste vídeo não existe. Um número esconde por que metade some antes do fim.\n\n[Cena 2] Este rosto foi gerado. Esta voz foi clonada. Nada aqui passou por editor.\n\n[Cena 3] Quatro passos. Uma esteira. O último… quase ninguém mostra.\n\n[Cena 4] Aqui dentro nasce cada peça. E nasce medida.\n\n[Cena 5] Tem um número, escondido no painel deste canal, que mata metade da audiência em setenta e um segundos.\n\n[Cena 6] Eu desenhei este vídeo contra esse número. Passo um: a gente congela o mundo.",
>  "status": "idle",
>  "language": "pt-BR",
>  "provider": "qwen3-local"
> }
> 
> === EDGES (sample: into n_bvid_2, n_p_1, n_p_5) ===
>   n_d3jbjjjg -> n_p_1 (output -> input_image)
>   n_bimg_2 -> n_bvid_2 (output_image -> input_image)
>   n_d3jbjjjg -> n_p_5 (output -> input_image)
> ```

## 🤖 Claude *(00:07:59)*

<details>
<summary>💭 Thinking Process</summary>

I'm reviewing the node configurations and noticing that the charRef has both imageUrl and imageUrls fields with signed URLs that expire at a specific timestamp. The token was issued earlier and I need to verify whether it's still valid based on the current time.

For the Presenter node, I see there's a discrepancy between the `duration` field (5) and `veoDuration` (8) — the latter is what actually gets used by Veo, and the 8-second duration aligns with the constraints from the character references.

The Nano Banana image generation node is using the Gemini model with a 16:9 aspect ratio and includes that "Cinematic 16:9 first frame:" prefix that was flagged in the audit. The b-roll node then takes this generated image as its first frame input, running a 4-second Veo generation without a character reference.

Since the b-roll uses `veoUseFirstFrame: true` (image-to-video mode) rather than character references, the 8-second minimum duration constraint doesn't apply—that clamp only affects reference-based video generation. So the 4-second duration is valid, costing 134 mco for the fast 720p generation.

Now moving to the voice node, which uses the Qwen3 local provider with Portuguese Brazilian language settings. The real issue is that without a reference voice sample, the cloned voice won't actually be Gabriel's voice—it'll fall back to the default pt-BR voice instead. Scene 20 specifically calls for "the cloned voice itself playing the newly generated audio," so this is a critical gap that needs resolving, even if the default voice might work as a temporary workaround.

Looking at what's actually in place: the nodes are properly configured with prompts, models, durations, and edges all connected; the presenter nodes have the right duration settings and character references; the B-roll is pulling from Nano Banana with correct frame timing; and the voice is set to qwen3-local pt-BR with the narration text ready. The Sovereign needs to decide whether to attach a voice profile or accept the default for now.

Breaking down the full production scope: Phase 1 is doable on my end with about 6,180 mco worth of work across voice, Nano generations, B-roll, and presenter nodes; Phase 2 requires the Sovereign to manually create 21 screencasts; Phase 3 is the final assembly in HyperFrames Studio, also on the Sovereign's side.

I can't complete this end-to-end, so I need to ask the Sovereign directly whether to proceed with Phase 1 and how incrementally, while being clear about the human dependencies downstream. Before I do that though, I'm wondering if there's any way to automate those 21 screencasts using browser automation instead of requiring manual recording.

The screencasts are just UI interactions—navigating the canvas, clicking buttons, dragging references, typing in fields, showing cost badges and dashboards. An automated browser could theoretically perform all these actions and capture video output. But this is a significant undertaking with quality concerns, and the original spec explicitly calls for the Sovereign to record them. Plus some screencasts need to show live generation happening in real time, which requires actual runs rather than playback.

So I should offer this as an option rather than assume it's needed. The real decision is simpler: does the Sovereign want to record the screencasts themselves, or should I attempt to automate them via browser capture? Let me lay out the core paths—either run the full paid generation now with all the witnesses, or start with just the free tier and de-risking witnesses to validate before committing to the larger presenter bulk. I'm settling on a clear recommendation: run the free narrations and low-cost de-risking witnesses first (~471 mco), then pause at a checkpoint before committing to the larger 5k spend. This follows the runbook's own gate sequence, delivers immediate value with all six free narrations, and validates the critical risks upfront like Vertex API health through G2.

The voice cloning piece is what I need to verify — whether the voice nodes can run without a reference profile or if there's an existing Gabriel voice asset from prior episodes. Rather than getting sidetracked on that detail, I'll let the voice nodes proceed with whatever default they use.

The safest move is to run those six free narration nodes first. If they work, I get audio; if they fail due to a missing reference, I learn the config gap without spending anything. Then I can present the honest status: nodes are ready, nothing's been generated yet, and here's what I'm about to run. I need to verify whether invoking the voice cloning through the canvas execution routes to the async voice-bridge properly—it's a keyless async operation that enqueues renders to a worker queue, so running six narrations sequentially would be feasible but time-consuming since the worker processes jobs one at a time.

The real question is whether I should orchestrate this at scale with a Workflow for gated generation and Vision QA verification, or just proceed with the safe path of free narrations and risk mitigation. Since this involves real balance spend, I need to be clear about whether this is my call to make or the Sovereign's—I'm leaning toward asking directly rather than assuming I should just move forward. I'm torn between respecting their autonomy and preference for execution versus the hard constraint that I can't finish the master without their screencasts. The cost is substantial enough and the dependency real enough that I need confirmation before spending 6.180 mco on something that might not be completable.

My move: run the 6 free voice narrations first to validate the system and surface the actual gap, then present the honest status and ask directly about the paid work and human gates. This way I'm acting autonomously on what I can deliver while being transparent about what requires their decision.

Now I need to nail down the exact canvas-execute payload for the voice node — the node_type identifier, required fields, and how to properly poll the results. Let me trace through the execution contract in canvas-execute to get this right before I attempt anything against prod.

But first, I should check with the Sovereign on the actual workflow: are they expecting me to build a full CLI runner to automate the screencasts, or would they prefer to prep the segments and click Run in the UI themselves? And do they want me to record the screencasts or handle that part too? These answers will determine whether I'm building a runner script or just preparing the data. Let me ask them directly with a clear recommendation based on what I've learned so far.

For Phase 1, I'm thinking through the gated approach: start with a small batch of free narrations and witness footage to validate quality, then pause for their review before running the bulk of the 5,073 presenter segments. The gate sequence would be the free content first, then the b-roll, Nano clips, and finally the main presenter batch.

I'm also considering three execution options: run just the witness content as a checkpoint (~400-500 mco), execute everything now with internal gating (~6,180 mco), or prepare everything and let them trigger the full run from the UI.

For the screencasts phase, I need to clarify the decision from their perspective — who actually records the 21 screencasts? Either they handle it manually, or I automate it via browser agent at 1080p, or we defer that choice and focus on phase 1 first.

I'm second-guessing whether automating the screencasts is even realistic to promise — it's genuinely difficult to capture smooth, high-quality video of live UI interactions with real generation happening. Offering it and failing would be worse than not offering it, but it's worth exploring honestly as an attempt. And I should double-check whether the screencasts are actually the blocking factor here.

The 21 screencasts are the core of the tutorial format itself, so they're definitely load-bearing. I should surface the voice-reference gap as a detail in the status but it's not a fork in the decision. Running the free narrations first makes sense — it's zero-regret since they're useful regardless of which path the Sovereign picks, and it gives material proof before asking for anything bigger. I just need to build out the voiceClone runner payload first. I'll lay out the current status and ask the Sovereign directly whether to proceed with the gated witnesses approach or explore alternatives, since this decision shapes everything that follows.

</details>


## 🤖 Claude *(00:08:14)*

Agora tenho o quadro material completo e honesto. Deixa eu registrar os achados decisivos antes de te apresentar a decisão.

**Estado material do projeto `18a21002` (verificado no banco agora):**
- **Nada foi gerado ainda** — `total_executions: 0`, `total_credits_used: 0`. Saldo cheio: **9.733 mco**.
- **Nós materialmente armados** (config completa, não nascem mortos):
  - 19 apresentador `n_p_*` — `veo-3.1-fast · veoDuration:8 · 720p · 16:9 · characterRefId:n_d3jbjjjg` ✅ (8s satisfaz o clamp refs→8s)
  - 7 B-roll `n_bvid_*` — `veoUseFirstFrame:true · 4-5s`, edge `n_bimg_X → n_bvid_X (output_image→input_image)` ✅ (firstFrame, clamp N/A)
  - 7 Nano Banana `n_bimg_*` — `openrouter-gemini-image · 16:9` ✅
  - 6 voz `n_voice_ato*` — `qwen3-local · pt-BR`, narração concatenada por ato ✅
  - charRef `n_d3jbjjjg` — imagem assinada válida (~6,6 dias) ✅
- ⚠️ **Flag 1 (voz):** os nós de voz não têm amostra de referência de clone anexada → rodarão no **default pt-BR do Qwen3**, não na sua voz clonada. A premissa do vídeo ("esta voz foi clonada") pede a voz do Gabriel AI.

**A realidade estrutural que Lei 1 me obriga a declarar** — o master final **não pode ser finalizado 100% por mim sozinho**. O runbook v2 tem 3 fases, e 2 são mãos humanas:

| Fase | O quê | Quem | Custo |
|---|---|---|---|
| **1** | Gerar 32 segmentos sintéticos (19 apresentador + 7 b-roll + 7 imagem + 6 voz) | **Eu posso** (canvas-execute via script) | ~6.180 mco |
| **2** | **21 screencasts** (você demonstrando a UI MCORCH ao vivo — o núcleo pedagógico do tutorial) | **Mão humana** (ou browser-automation a explorar) | 0 |
| **3** | Montagem no NLE HyperFrames Studio (importar 53 camadas, timeline 1→48, 5 transições, export) | **Mão humana** | 0 |

Ou seja: se eu queimar 6.180 mco na Fase 1 mas a Fase 2/3 não acontecer, gastei sem entregar o master ([[feedback_running_is_not_delivering]]). Por isso preciso da sua decisão nos dois eixos genuinamente seus — o gasto real e as mãos humanas.

Minha recomendação: **gated — grátis + testemunhas baratas primeiro (~400 mco), checkpoint antes do lote de 5.073 mco.** É a própria ordem de gates do runbook (valida saúde da chave Vertex + lip-sync da cena 1 antes de comprometer o grosso).

## 🤖 Claude *(00:08:26)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Fase 1 (gerar os 32 segmentos sint\u00e9ticos, ~6.180 mco do seu saldo real de 9.733): como quer que eu proceda?",
      "header": "Gasto Fase 1",
      "multiSelect": false,
      "options": [
        {
          "label": "Gated: testemunhas primeiro (Recomendado)",
          "description": "Rodo j\u00e1 o de gra\u00e7a (6 narra\u00e7\u00f5es Qwen3, 0 mco) + testemunhas baratas de risco (G2: 1 Nano+1 B-roll ~144 mco; R5: cena 1 apresentador 267 mco), com Vision QA em cada uma. Paro em ~411 mco e te mostro antes de comprometer os 5.700 mco restantes do lote apresentador."
        },
        {
          "label": "Rodar tudo agora (~6.180 mco)",
          "description": "Executo o lote completo de uma vez (gr\u00e1tis\u2192imagens\u2192b-roll\u219219 apresentador), gated internamente pelas testemunhas + Vision QA, mas sem parar pra checkpoint. Mais r\u00e1pido, comprometo o saldo inteiro do EP05."
        },
        {
          "label": "N\u00e3o gastar \u2014 preparo e voc\u00ea clica Run",
          "description": "Deixo o projeto 100% verificado e pronto, te entrego a ordem exata de clique, e voc\u00ea roda o Run All na pr\u00f3pria UI do Spaces. Zero gasto aut\u00f4nomo."
        }
      ]
    },
    {
      "question": "Os 21 screencasts (Fase 2) e a montagem no editor (Fase 3) s\u00e3o m\u00e3os humanas. Como resolver?",
      "header": "M\u00e3os humanas",
      "multiSelect": false,
      "options": [
        {
          "label": "Eu tento automatizar os screencasts via browser",
          "description": "Uso agent-browser pra dirigir a UI real do MCORCH a 1080p e capturar os 21 screencasts (clicar Gerar, arrastar ref, digitar na voz, mostrar badges de custo, a curva EP02). Alto esfor\u00e7o e sens\u00edvel a qualidade \u2014 exploro e provo com Vision QA antes de prometer."
        },
        {
          "label": "Voc\u00ea grava os screencasts (Sovereign)",
          "description": "Eu entrego a lista exata (21 cenas, cada uma com a fala Qwen3 e a a\u00e7\u00e3o de UI a demonstrar) e voc\u00ea grava com OBS/gravador nativo. \u00c9 a rota do ORO original do runbook."
        },
        {
          "label": "Decidir depois \u2014 foca na Fase 1 agora",
          "description": "Resolvemos screencasts + montagem depois que os segmentos sint\u00e9ticos estiverem prontos e verificados. N\u00e3o bloqueia a Fase 1."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Fase 1 (gerar os 32 segmentos sintéticos, ~6.180 mco do seu saldo real de 9.733): como quer que eu proceda?"="Gated: testemunhas primeiro (Recomendado)", "Os 21 screencasts (Fase 2) e a montagem no editor (Fase 3) são mãos humanas. Como resolver?"="Eu tento automatizar os screencasts via browser". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(00:17:21)*

<details>
<summary>💭 Thinking Process</summary>

The Sovereign is choosing a phased approach: starting with free narrations and witness testimonies from different sources, running quality checks on each, and stopping before moving into the bulk work at around 411 mco. Then attempting to automate browser interactions using an agent to drive the actual browser. I need to understand the exact canvas-execute API contract—the node types, required fields, how it resolves references and handles the ledger—before I build the runner script. Since this involves real production execution with actual spend, I'm going to read through the client code to see how payloads are constructed, then write a deterministic runner that mints a User 0 JWT and drives each node sequentially with polling, doing Vision QA at each checkpoint to validate outputs before moving forward.

</details>


## 🤖 Claude *(00:17:23)*

Decisão registrada: **Fase 1 gated (testemunhas primeiro, ~411 mco, checkpoint antes do lote)** + **eu tento automatizar os 21 screencasts via browser**.

Vou começar pela Fase 1 gated. Como isso queima saldo real, preciso do contrato EXATO do `canvas-execute` antes de invocar (Lei 1 — zero tentativa falha desperdiçando mco). Deixa eu ler o roteamento por tipo de nó + como o cliente monta o payload de run.

## 🤖 Claude *(00:17:26)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Fase 1 EP05 \u2014 testemunhas gated",
  "summary": "Recon completo: projeto 18a21002 em vm_canvas_projects, 62 n\u00f3s armados, 0 gerado, saldo 9733. Sovereign escolheu: Fase 1 gated (gr\u00e1tis+testemunhas ~411 mco, checkpoint) + screencasts via browser-automation. Lendo contrato canvas-execute antes de queimar mco."
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Fase 1 EP05 — testemunhas gated". Continue your current work.'}]
> ```

## 🤖 Claude *(00:17:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l supabase/functions/canvas-execute/index.ts; echo \"---node_type routing---\"; grep -nE \"node_type|nodeType|switch|case ['\\\"]|=== ['\\\"](generate_image|image_to_video|voice|tts|clone)\" supabase/functions/canvas-execute/index.ts | head -60",
  "description": "canvas-execute routing recon"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 2610 supabase/functions/canvas-execute/index.ts
> ---node_type routing---
> 138:  node_type: string;
> 155:  // switches to the ledger-first billing order (begin → provider → finalize) — exclusive branch.
> 206:    const promptOptional = body.node_type === "upscale";
> 245:    // providers fall back to the provider/model lookup or the node_type slug.
> 247:    if (body.node_type === "magic_prompt") {
> 253:        ?? (body.node_type === "image_to_video"
> 255:          : (body.node_type === "generate_image"
> 257:            : body.node_type.replace("_", "-")));
> 294:    if (body.node_type === "image_to_video" && !ALLOWED_VIDEO_MODELS.includes(body.model)) {
> 302:    // ── Map node_type for database enum compliance ───────────────────
> 303:    // vm_node_type enum: generate_image, generate_video, upscale, inpaint,
> 321:    const dbNodeType = NODE_TYPE_MAP[body.node_type] ?? body.node_type;
> 322:    if (!NODE_TYPE_MAP[body.node_type]) {
> 323:      console.warn(`[canvas-execute] unmapped node_type "${body.node_type}" — passing through as-is`);
> 345:    const initialStatus = body.node_type === "image_to_video" ? "queued" : "running";
> 352:        node_type: dbNodeType,
> 373:        node_type_received: body.node_type,
> 374:        node_type_mapped: dbNodeType,
> 381:    if (body.node_type === "magic_prompt") {
> 494:    if (body.node_type === "image_to_video") {
> 605:          node_type: dbNodeType,
> 662:      const spendAction = body.node_type === "image_to_video"
> 673:          node_type: body.node_type,
> 1326:    body.node_type !== "generate_image" && body.node_type !== "magic_prompt" &&
> 1327:    body.node_type !== "image_to_video" && body.node_type !== "voice_over" &&
> 1328:    body.node_type !== "scene_compose" && body.node_type !== "style_transfer" &&
> 1329:    body.node_type !== "upscale"
> 1332:      error: "spaces_node_type_unsupported",
> 1342:  if (body.node_type === "image_to_video") {
> 1431:  if (body.node_type === "voice_over") {
> 1456:  if (body.node_type === "scene_compose") {
> 1496:  if (body.node_type === "generate_image") {
> 1511:  if (body.node_type === "upscale") {
> 1533:  if (body.node_type === "style_transfer") {
> 1541:  if (body.node_type === "generate_image" || body.node_type === "style_transfer") {
> 1559:  const effectiveCost = body.node_type === "voice_over"
> 1561:    : (body.node_type === "scene_compose"
> 1563:      : (body.node_type === "style_transfer"
> 1565:        : (body.node_type === "upscale"
> 1567:          : (body.node_type === "image_to_video" ? videoCost : (imageCost || creditCost)))));
> 1588:  if (body.node_type === "image_to_video" && body.provider === "higgsfield" && (!keys.higgsfield || !keys.higgsfield_secret)) {
> 1596:  if (body.node_type === "image_to_video" && body.provider === "google" && !keys.gemini) {
> 1605:  if ((body.node_type === "scene_compose" || body.node_type === "style_transfer") && !keys.openrouter) {
> 1613:  if (body.node_type === "voice_over" && !keys.gemini) {
> 1621:  if (body.node_type === "upscale" && !keys.replicate) {
> 1630:  if (body.node_type === "generate_image") {
> 1661:  const modelKey = body.node_type === "magic_prompt"
> 1663:    : (body.node_type === "voice_over"
> 1665:      : (body.node_type === "scene_compose"
> 1667:        : (body.node_type === "style_transfer"
> 1669:          : (body.node_type === "upscale"
> 1672:  const outputType = body.node_type === "magic_prompt"
> 1674:    : (body.node_type === "image_to_video"
> 1676:      : (body.node_type === "voice_over" ? "audio" : "image"));
> 1685:    p_context: { provider: body.provider, model: body.model, node_type: body.node_type },
> 1716:  if (body.node_type === "voice_over") {
> 1728:  if (body.node_type === "image_to_video" && body.provider === "google" && veoParams) {
> 1739:  if (body.node_type === "image_to_video") {
> 1753:      if (body.node_type === "magic_prompt") {
> 1765:      } else if (body.node_type === "scene_compose") {
> ```

## 🤖 Claude *(00:17:49)*

<details>
<summary>💭 Thinking Process</summary>

I'm noticing a mismatch between the node kind used on the client side (`voiceClone`) and the node_type string expected by canvas-execute (`voice_over`), which suggests there's a translation layer that needs to map between these different naming conventions.

The key insight is that `voiceClone` nodes with `provider: "qwen3-local"` don't actually route through canvas-execute at all — they use the `generate-voice` edge function instead, which is a separate async pathway that calls the voice-bridge worker. This means the runner needs to handle multiple routing paths depending on both the node kind and its provider configuration.

To get the exact contract for how each node type maps to its edge function and required payload fields, I should trace through the client's execution dispatch in `useCanvasStudio.ts` and `useCanvasPipeline.ts` to see how the run function builds and invokes each node, especially around the payload construction and whether `node_run_id` is being passed.

</details>


## 🤖 Claude *(00:17:52)*

Contrato do `canvas-execute` mapeado, mas achei uma bifurcação importante: `voiceClone`/`qwen3-local` NÃO passa pelo branch `voice_over` (esse é Gemini TTS) — vai pela edge `generate-voice` async. Cada kind roteia diferente. Preciso ler o dispatch do cliente (a fonte da verdade do payload) para os 3 kinds. Deixa eu mapear isso com precisão.

## 🤖 Claude *(00:17:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rlnE \"canvas-execute|generate-voice|node_run_id\" src/hooks/ | head; echo \"=== files that dispatch runs ===\"; grep -rlnE \"functions.invoke\\(['\\\"](canvas-execute|generate-voice|veo-poll)\" src/ | head",
  "description": "Find client run dispatch files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/hooks/useCanvasPipeline.ts
> src/hooks/useVeoPoll.ts
> src/hooks/useSpaces.ts
> src/hooks/useAvatarVoice.ts
> src/hooks/useSpaceSession.ts
> src/hooks/useParamRegistry.ts
> src/hooks/useCanvasStudio.ts
> src/hooks/useGenerationLedger.ts
> === files that dispatch runs ===
> src/hooks/useVeoPoll.ts
> src/hooks/useGenerationLedger.ts
> src/hooks/useAvatarVoice.ts
> src/hooks/useCanvasStudio.ts
> ```

## 🤖 Claude *(00:18:02)*

<details>
<summary>💭 Thinking Process</summary>

I need to trace through the key files to understand how the run dispatch and ledger logic work, particularly focusing on useCanvasStudio.ts and how voiceClone gets dispatched. There's a lot of code to parse here, so I'm thinking about whether to map this out systematically myself or delegate the detailed tracing to focus on the critical execution paths.

Actually, reading through it myself will be more reliable for building a bulletproof runner given the financial sensitivity. Let me search through useCanvasStudio for how the invoke calls are constructed and what payloads get built for each operation type.

</details>


## 🤖 Claude *(00:18:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"functions.invoke|node_run_id|node_type|voiceClone|imageToVideo|generateImage|kind ===|case ['\\\"]|payload|provider:|model:|space_id|project_id\" src/hooks/useCanvasStudio.ts | head -80",
  "description": "useCanvasStudio dispatch map"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 27:  project_id: string | null;
> 30:  provider: string | null;
> 32:  node_type: string | null;
> 44:  project_id: string;
> 46:  node_type: string;
> 47:  provider: string;
> 48:  model: string;
> 225:// it.2b (Amendment 14 FR-SPACES-024): sync node types run LEDGER-FIRST — a fresh node_run_id per
> 239: * estorna integralmente na falha, o poll finaliza). Sem `node_run_id` o `canvas-execute` despacha
> 242: * O gate é por PROVIDER, não pelo node_type: o vídeo do Higgsfield continua exatamente no caminho
> 246:function needsLedgerRun(nodeType: string, provider: string): boolean {
> 256:      project_id: string;
> 258:      node_type: string;
> 259:      provider: string;
> 260:      model: string;
> 277:      const body = needsLedgerRun(params.node_type, params.provider)
> 278:        ? { ...params, node_run_id: crypto.randomUUID() }
> 280:      const { data, error } = await supabase.functions.invoke("canvas-execute", { body });
> 297:      queryClient.invalidateQueries({ queryKey: ["vm-canvas-project", vars.project_id] });
> 300:      queryClient.invalidateQueries({ queryKey: ["project-ledger-runs", vars.project_id] });
> 321:      if (projectId) query = query.eq("project_id", projectId);
> 333:  id: string; project_id: string | null; node_id: string; model_key: string;
> 344:    project_id: g.project_id ?? "",
> 346:    node_type: nodeType,
> 347:    provider: slash > 0 ? g.model_key.slice(0, slash) : g.model_key,
> 348:    model: slash > 0 ? g.model_key.slice(slash + 1) : g.model_key,
> 371:      if (projectId) legacyQuery = legacyQuery.eq("project_id", projectId);
> 377:        .select("id, project_id, node_id, model_key, output_type, status, mco_charged, result, created_at")
> 379:        .not("project_id", "is", null)
> 382:      if (projectId) ledgerQuery = ledgerQuery.eq("project_id", projectId);
> 409:        .eq("project_id", projectId);
> ```

## 🤖 Claude *(00:18:09)*

<details>
<summary>💭 Thinking Process</summary>

The `execute` mutation in useCanvasStudio is generic and accepts various parameters like project_id, node_id, node_type, provider, and model, then calls canvas-execute with a node_run_id when needed. The actual mapping from kind to node_type, provider, model, and additional parameters like prompt or veoDuration happens in useCanvasPipeline instead.

I need to examine useCanvasPipeline.ts to see how it orchestrates the "Run All" flow and constructs the payload for each node type. I also need to verify how voiceClone is dispatched separately using generate-voice rather than canvas-execute.

</details>


## 🤖 Claude *(00:18:09)*

O `execute` do `useCanvasStudio` é genérico — o **caller** (Run All em `useCanvasPipeline`) monta o payload por kind. Essa é a fonte da verdade que preciso. Vou ler o `useCanvasPipeline` inteiro.

## 🤖 Claude *(00:18:10)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasPipeline.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState, useCallback, useMemo, useEffect } from "react";
> 2	import { toast } from "sonner";
> 3	import { useCanvasStore } from "@/store/useCanvasStore";
> 4	import { useCanvasExecute } from "@/hooks/useCanvasStudio";
> 5	import { getTopologicalLayers } from "@/lib/canvas-dag";
> 6	import { findUpstreamImage, findUpstreamImages, findUpstreamHandleAsset, findUpstreamProductItems } from "@/lib/canvas-utils";
> 7	import { toDisplayUrl, toDisplayUrls } from "@/lib/asset-url";
> 8	import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> 9	import { expandProductRuns, type ProductListItem } from "@/lib/product-list";
> 10	import {
> 11	  CanvasNode,
> 12	  estimateNodeCost,
> 13	  resolveExecutePayload,
> 14	} from "@/types/canvas";
> 15	
> 16	export type PipelineStatus = "pending" | "running" | "done" | "error" | "blocked";
> 17	
> 18	export function useCanvasPipeline({
> 19	  projectId,
> 20	  refetchDashboard,
> 21	}: {
> 22	  projectId?: string;
> 23	  refetchDashboard?: () => void;
> 24	}) {
> 25	  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus>("pending");
> 26	
> 27	  const nodes = useCanvasStore((s) => s.nodes);
> 28	  const edges = useCanvasStore((s) => s.edges);
> 29	  const updateNodeData = useCanvasStore((s) => s.updateNodeData);
> 30	  const styleSettings = useCanvasStore((s) => s.styleSettings);
> 31	  const executeNode = useCanvasExecute();
> 32	
> 33	  // Determine if a node is currently runnable
> 34	  const runnable = useMemo(() => {
> 35	    return nodes.filter((n) => {
> 36	      if (n.data.kind === "characterReference" || n.data.kind === "productList") return false;
> 37	      // spaces-cadence FR-CAD-001: the Cadência node ARMS a plan from its inspector (cadence-plan) — it is not
> 38	      // a "runnable" generate step and carries no prompt, so it is excluded from the Run All gate (SDD §2.1).
> 39	      if (n.data.kind === "cadence") return false;
> 40	      if (n.data.status === "running" || n.data.status === "queued") return false;
> 41	
> 42	      // it.4c: upscale has no prompt — it's runnable when it has an upstream image edge.
> 43	      if (n.data.kind === "upscale") {
> 44	        return edges.some((e) => e.target === n.id);
> 45	      }
> 46	
> 47	      // `n.data` is `CanvasNodeData & Record<string, unknown>` (ReactFlow's constraint), so `.prompt`
> 48	      // widens to `unknown` for the union members that don't declare it. Narrow explicitly instead of
> 49	      // asserting `string`: a non-string value used to reach `.trim()` and throw at runtime.
> 50	      const rawPrompt: unknown = "prompt" in n.data ? n.data.prompt : "";
> 51	      if (typeof rawPrompt !== "string" || !rawPrompt.trim()) return false;
> 52	
> 53	      if (n.data.kind === "imageToVideo") {
> 54	        const hasUpstream = edges.some((e) => e.target === n.id);
> 55	        if (!hasUpstream) return false;
> 56	      }
> 57	      return true;
> 58	    });
> 59	  }, [nodes, edges]);
> 60	
> 61	  const runnableCount = runnable.length;
> 62	
> 63	  const runAllCost = useMemo(() => {
> 64	    return runnable.reduce((sum, n) => sum + estimateNodeCost(n.data), 0);
> 65	  }, [runnable]);
> 66	
> 67	  // Check on load/graph change if there's any cycle
> 68	  useEffect(() => {
> 69	    if (nodes.length === 0) {
> 70	      setPipelineStatus("pending");
> 71	      return;
> 72	    }
> 73	    try {
> 74	      getTopologicalLayers(nodes, edges);
> 75	      setPipelineStatus((prev) => (prev === "blocked" ? "pending" : prev));
> 76	    } catch (e) {
> 77	      setPipelineStatus("blocked");
> 78	    }
> 79	  }, [nodes, edges]);
> 80	
> 81	  // Run a single node
> 82	  const runSingleNode = useCallback(
> 83	    async (nodeId: string) => {
> 84	      const currentNodes = useCanvasStore.getState().nodes;
> 85	      const currentEdges = useCanvasStore.getState().edges;
> 86	      const currentStyleSettings = useCanvasStore.getState().styleSettings;
> 87	
> 88	      const n = currentNodes.find((node) => node.id === nodeId);
> 89	      if (!n) return;
> 90	
> 91	      const payload = resolveExecutePayload(n.data, currentStyleSettings);
> 92	      if (!payload) return;
> 93	
> 94	      const isVideo = n.data.kind === "imageToVideo";
> 95	      // Veo (provider 'google') does text→video and consumes upstream images as IDENTITY REFERENCES;
> 96	      // it only wants a first-frame when the node explicitly opts in (veoUseFirstFrame). Higgsfield i2v +
> 97	      // upscale REQUIRE an upstream first-frame image.
> 98	      const isVeoVideo = isVideo && payload.provider === "google";
> 99	      const veoUseFirstFrame =
> 100	        isVeoVideo && (n.data as { veoUseFirstFrame?: boolean }).veoUseFirstFrame === true;
> 101	      // it.4c: upscale (like Higgsfield video) needs the upstream image as its input_asset_url.
> 102	      const wantsInputImage = (isVideo && !isVeoVideo) || n.data.kind === "upscale";
> 103	      const inputAssetUrl = (wantsInputImage || veoUseFirstFrame)
> 104	        ? findUpstreamImage(n.id, currentNodes, currentEdges)
> 105	        : undefined;
> 106	
> 107	      if (wantsInputImage && !inputAssetUrl) {
> 108	        updateNodeData(n.id, {
> 109	          status: "failed",
> 110	          error: "Imagem de entrada não disponível",
> 111	        });
> 112	        return;
> 113	      }
> 114	
> 115	      const isSceneCompose = n.data.kind === "sceneCompose";
> 116	      const sceneComposeInputs = isSceneCompose
> 117	        ? {
> 118	            input_image_1: findUpstreamHandleAsset(n.id, "input_image_1", currentNodes, currentEdges),
> 119	            input_image_2: findUpstreamHandleAsset(n.id, "input_image_2", currentNodes, currentEdges),
> 120	            input_layout: findUpstreamHandleAsset(n.id, "input_layout", currentNodes, currentEdges),
> 121	          }
> 122	        : {};
> 123	
> 124	      // Cross-node consistency (Phase 4.3): image/style nodes inherit the
> 125	      // upstream connected creative(s) as reference images so identity is
> 126	      // preserved across the chain. SOP: docs/processes/canvas-node-consistency.md.
> 127	      // F4: video nodes (POV/Veo) MUST inherit the connected identity references too. Previously only
> 128	      // generateImage/styleTransfer collected them, so Run All sent the Veo node ZERO references and the
> 129	      // face came out generic. When the node uses its first-frame, drop that image from the reference set.
> 130	      // Veo forbids sending a first-frame image AND identity references together ("Image and reference images
> 131	      // cannot be both set"). So Veo nodes collect references ONLY in reference mode (veoUseFirstFrame=false).
> 132	      // In first-frame mode the video is generated FROM the connected image and references do not apply — a
> 133	      // true XOR at the source (born-dead POV crash 2026-07-21; server also guards). generateImage/styleTransfer
> 134	      // always inherit refs for cross-node consistency.
> 135	      const wantsReference =
> 136	        n.data.kind === "generateImage" ||
> 137	        n.data.kind === "styleTransfer" ||
> 138	        (isVeoVideo && !veoUseFirstFrame);
> 139	      const rawReferenceUrls = wantsReference
> 140	        ? findUpstreamImages(n.id, currentNodes, currentEdges)
> 141	        : [];
> 142	
> 143	      // ── it.4a (FR-SPACES-029): generateImage with an upstream productList EXPANDS into one
> 144	      // independent ledger run per item (template×items → N consistent creatives). Each run gets a
> 145	      // fresh node_run_id (minted in useCanvasExecute) + the item's own reference image. Skip
> 146	      // expansion when the list is empty/absent — falls through to the single-run path below.
> 147	      if (n.data.kind === "generateImage") {
> 148	        const items = findUpstreamProductItems(n.id, currentNodes, currentEdges);
> 149	        const runs = items ? expandProductRuns(n.data.prompt, items as ProductListItem[]) : [];
> 150	        if (runs.length > 0) {
> 151	          updateNodeData(n.id, { status: "running", error: undefined });
> 152	          let lastUrl: string | undefined;
> 153	          let firstError: string | undefined;
> 154	          let okCount = 0;
> 155	          for (const run of runs) {
> 156	            try {
> 157	              const raw = await executeNode.mutateAsync({
> 158	                project_id: projectId!,
> 159	                node_id: n.id,
> 160	                ...payload,
> 161	                prompt: run.prompt,
> 162	                ...(run.referenceImageUrl ? { reference_image_urls: [run.referenceImageUrl] } : {}),
> 163	              });
> 164	              const result = assertExecuteSuccess(raw);
> 165	              lastUrl = result.output_url ?? lastUrl;
> 166	              okCount++;
> 167	            } catch (e) {
> 168	              if (!firstError) firstError = e instanceof Error ? e.message : String(e);
> 169	            }
> 170	          }
> 171	          if (okCount > 0) {
> 172	            updateNodeData(n.id, {
> 173	              status: "success",
> 174	              output: { imageUrl: lastUrl, generatedAt: new Date().toISOString() },
> 175	              error: firstError ? `${okCount}/${runs.length} — ${firstError}` : undefined,
> 176	            });
> 177	            toast.success(`Lote gerado: ${okCount}/${runs.length} criativos na Biblioteca`);
> 178	          } else {
> 179	            updateNodeData(n.id, { status: "failed", error: firstError ?? "Falha no lote" });
> 180	          }
> 181	          return;
> 182	        }
> 183	      }
> 184	
> 185	      updateNodeData(n.id, { status: "running", error: undefined });
> 186	
> 187	      // Re-sign upstream URLs to FRESH owner-scoped URLs — a node output persisted at generation time
> 188	      // becomes a dead public URL / expired signed URL weeks later, and the server download drops it
> 189	      // silently (the "refs ignored" bug). SOP: private-bucket-asset-signing.
> 190	      const referenceImageUrls = await toDisplayUrls(rawReferenceUrls);
> 191	      const freshInputAssetUrl = inputAssetUrl ? await toDisplayUrl(inputAssetUrl) : undefined;
> 192	
> 193	      try {
> 194	        const raw = await executeNode.mutateAsync({
> 195	          project_id: projectId!,
> 196	          node_id: n.id,
> 197	          ...payload,
> 198	          ...(freshInputAssetUrl ? { input_asset_url: freshInputAssetUrl } : {}),
> 199	          ...sceneComposeInputs,
> 200	          ...(referenceImageUrls.length ? { reference_image_urls: referenceImageUrls } : {}),
> 201	        });
> 202	        const result = assertExecuteSuccess(raw);
> 203	
> 204	        if (isVideo) {
> 205	          // Async job submitted — let Realtime or polling finalize it
> 206	        } else {
> 207	          updateNodeData(n.id, {
> 208	            status: "success",
> 209	            output: {
> 210	              imageUrl: result.output_url ?? undefined,
> 211	              generatedAt: new Date().toISOString(),
> 212	            },
> 213	            error: undefined,
> 214	          });
> 215	        }
> 216	      } catch (e) {
> 217	        const msg = e instanceof Error ? e.message : String(e);
> 218	        updateNodeData(n.id, { status: "failed", error: msg });
> 219	      }
> 220	    },
> 221	    [projectId, updateNodeData, executeNode]
> 222	  );
> 223	
> 224	  // Helper: wait for nodes to complete in Zustand
> 225	  const waitForNodesToComplete = useCallback(async (nodeIds: string[]): Promise<boolean> => {
> 226	    return new Promise((resolve) => {
> 227	      const checkComplete = () => {
> 228	        const currentNodes = useCanvasStore.getState().nodes;
> 229	        const relevantNodes = currentNodes.filter((n) => nodeIds.includes(n.id));
> 230	
> 231	        const allDone = relevantNodes.every(
> 232	          (n) => n.data.status === "success" || n.data.status === "failed"
> 233	        );
> 234	        const anyFailed = relevantNodes.some((n) => n.data.status === "failed");
> 235	
> 236	        return { allDone, anyFailed };
> 237	      };
> 238	
> 239	      const initial = checkComplete();
> 240	      if (initial.allDone) {
> 241	        resolve(!initial.anyFailed);
> 242	        return;
> 243	      }
> 244	
> 245	      const unsubscribe = useCanvasStore.subscribe(() => {
> 246	        const { allDone, anyFailed } = checkComplete();
> 247	        if (allDone) {
> 248	          unsubscribe();
> 249	          resolve(!anyFailed);
> 250	        }
> 251	      });
> 252	    });
> 253	  }, []);
> 254	
> 255	  // Execute pipeline
> 256	  const runPipeline = useCallback(async () => {
> 257	    if (!projectId) return;
> 258	
> 259	    let layers: CanvasNode[][];
> 260	    try {
> 261	      layers = getTopologicalLayers(nodes, edges);
> 262	    } catch (e) {
> 263	      setPipelineStatus("blocked");
> 264	      toast.error("Ciclo detectado no grafo! O pipeline não pode ser executado.");
> 265	      return;
> 266	    }
> 267	
> 268	    const runnableIds = runnable.map((n) => n.id);
> 269	    if (runnableIds.length === 0) {
> 270	      toast.error("Nenhum nó qualificado para execução.");
> 271	      return;
> 272	    }
> 273	
> 274	    setPipelineStatus("running");
> 275	    toast.info(`Iniciando execução em camadas de ${runnableIds.length} nós...`);
> 276	
> 277	    let executionSuccess = true;
> 278	
> 279	    for (let i = 0; i < layers.length; i++) {
> 280	      const layer = layers[i];
> 281	      const layerRunnable = layer.filter((n) => runnableIds.includes(n.id));
> 282	
> 283	      if (layerRunnable.length === 0) {
> 284	        continue;
> 285	      }
> 286	
> 287	      // Mark layer nodes as queued
> 288	      for (const n of layerRunnable) {
> 289	        updateNodeData(n.id, { status: "queued", error: undefined });
> 290	      }
> 291	
> 292	      // Wait 100ms for UI status update
> 293	      await new Promise((resolve) => setTimeout(resolve, 100));
> 294	
> 295	      // Execute all nodes in this layer in parallel
> 296	      const runPromises = layerRunnable.map((n) => runSingleNode(n.id));
> 297	      await Promise.all(runPromises);
> 298	
> 299	      // Wait for all nodes in this layer to reach success/failed
> 300	      const layerIds = layerRunnable.map((n) => n.id);
> 301	      const layerSuccess = await waitForNodesToComplete(layerIds);
> 302	
> 303	      if (!layerSuccess) {
> 304	        executionSuccess = false;
> 305	        break;
> 306	      }
> 307	    }
> 308	
> 309	    if (executionSuccess) {
> 310	      setPipelineStatus("done");
> 311	      toast.success("Pipeline executado com sucesso!");
> 312	    } else {
> 313	      setPipelineStatus("error");
> 314	      toast.error("Erro na execução do pipeline. Algumas etapas falharam.");
> 315	    }
> 316	
> 317	    refetchDashboard?.();
> 318	  }, [nodes, edges, runnable, projectId, runSingleNode, waitForNodesToComplete, updateNodeData, refetchDashboard]);
> 319	
> 320	  const resetPipeline = useCallback(() => {
> 321	    setPipelineStatus("pending");
> 322	  }, []);
> 323	
> 324	  return {
> 325	    pipelineStatus,
> 326	    runPipeline,
> 327	    resetPipeline,
> 328	    runnable,
> 329	    runnableCount,
> 330	    runAllCost,
> 331	    runSingleNode,
> 332	  };
> 333	}
> 334	
> ```

## 🤖 Claude *(00:18:24)*

<details>
<summary>💭 Thinking Process</summary>

I'm seeing how the client dispatch works—`resolveExecutePayload` transforms the node data into the canvas-execute payload with all the necessary fields like node_type, provider, model, and prompt. The client also re-signs upstream URLs through `toDisplayUrls` before sending them, and for imageToVideo Veo requests with Google as the provider, there's special handling in reference mode.

But I'm noticing a gap: voiceClone nodes aren't explicitly excluded from the runnable filter, so they should be runnable if they have a prompt, but I need to verify whether `resolveExecutePayload` actually handles voiceClone or if it returns null, which would cause `runSingleNode` to exit early without executing it.

</details>


## 🤖 Claude *(00:18:26)*

Agora entendo o dispatch. `resolveExecutePayload(n.data)` mapeia kind→payload do canvas-execute, e o cliente re-assina URLs. Mas preciso confirmar como `voiceClone` roteia (canvas-execute vs generate-voice) e o payload exato de Veo. Deixa eu ler `resolveExecutePayload` + o dispatch de voz.

## 🤖 Claude *(00:18:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"resolveExecutePayload|veoParams|veoDuration|veoResolution|reference_type|generateAudio|node_type|provider|voiceClone|voice_over|case ['\\\"]|kind ===\" src/types/canvas.ts | sed -n '1,80p'",
  "description": "resolveExecutePayload map"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 34:  | "voiceClone"
> 94:  provider: ProviderId;
> 118:    provider: "higgsfield",
> 129:    provider: "higgsfield",
> 140:    provider: "higgsfield",
> 151:    provider: "higgsfield",
> 162:    provider: "openai",
> 170:    provider: "openai",
> 178:    provider: "replicate",
> 186:    provider: "replicate",
> 194:    provider: "replicate",
> 202:    provider: "openrouter",
> 210:    provider: "openrouter",
> 218:    provider: "openrouter",
> 248:  /** `google` = Veo (BYOK pool `user_provider_keys`); os demais são Higgsfield. */
> 249:  provider: ProviderId | "google";
> 266:    provider: "higgsfield",
> 275:    provider: "higgsfield",
> 284:    provider: "higgsfield",
> 294:    provider: "higgsfield",
> 304:    provider: "higgsfield",
> 315:    provider: "google",
> 326:    provider: "google",
> 337:    provider: "google",
> 360:  provider: "openrouter",
> 368:  provider: "higgsfield",
> 431:// model dropdown (the server resolves scene_compose cost by node_type slug, not provider/model).
> 524:  veoDuration?: VeoDuration;
> 525:  veoResolution?: VeoResolution;
> 532:  providerKeyId?: string;
> 549: * avatar-clone-ai Fatia 2 — voiceClone node (FR-AC-008/009/010/011).
> 554:  kind: "voiceClone";
> 557:  provider: "elevenlabs" | "cartesia" | "qwen3-local";
> 597:  provider: "higgsfield" | "lora_flux";
> 645: *  fail-closed); default DRAFT (opt-in publish, FR-SPACES-039). resolveExecutePayload → null
> 646: *  (the inspector calls the publisher directly, like voiceClone/avatarIdentity). */
> 665: *  default DRAFT (opt-in publish, HITL). resolveExecutePayload → null (the inspector calls the seam directly). */
> 686: *  package is v2 (OTD-CS-002, generate-script-package fn). TEXT SOURCE; resolveExecutePayload → null
> 687: *  (the inspector calls generate-video-script directly, like publishWordpress/voiceClone). */
> 706: *  by renderId → signs the storage_key. resolveExecutePayload → null (inspector calls video-render). */
> 773:    case "1x3":
> 775:    case "1x4":
> 776:    case "2x2":
> 778:    case "3x3":
> 780:    case "4x4":
> 811: * primeiro, rascunho por padrão). resolveExecutePayload → null (o inspector chama os seams diretamente). */
> 840: * generate media (resolveExecutePayload → null; estimateNodeCost → 0). The node ARMS a recurring plan via
> 1221:    veoDuration: 8,
> 1222:    veoResolution: "720p",
> 1230:/** avatar-clone-ai Fatia 2 — voiceClone node default. Amendment 18: the free self-host engine
> 1231: *  (qwen3-local, pt-BR) is the default — paid BYOK providers are opt-in (feedback_paid_byok_post_revenue). */
> 1238:    type: "voiceClone",
> 1241:      kind: "voiceClone",
> 1243:      provider: "qwen3-local",
> 1268:      provider: "lora_flux",
> 1558: * `canvas-execute` Edge Function. Soul models split into provider/model
> 1562:export function resolveExecutePayload(
> 1566:  node_type: string;
> 1568:  provider: ProviderId | "google";
> 1575:    case "generateImage": {
> 1585:        node_type: "generate_image",
> 1586:        provider: info.provider,
> 1593:    case "sceneCompose": {
> 1601:        node_type: "scene_compose",
> 1602:        provider: info.provider,
> 1608:    case "styleTransfer": {
> 1611:        node_type: "style_transfer",
> 1612:        provider: "higgsfield",
> 1623:    case "imageToVideo": {
> 1629:          node_type: "image_to_video",
> 1630:          provider: "google",
> 1634:            duration: data.veoDuration ?? VEO_DEFAULT_DURATION,
> 1635:            resolution: data.veoResolution ?? VEO_DEFAULT_RESOLUTION,
> 1647:        node_type: "image_to_video",
> 1648:        provider: info.provider,
> 1659:    case "characterReference":
> 1663:    case "productList":
> 1667:    case "upscale":
> 1671:        node_type: "upscale",
> 1672:        provider: "replicate",
> ```

## 🤖 Claude *(00:18:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rnE \"generate-voice|voice-render|useVoiceRenderPoll|qwen3-local|voiceClone\" src/hooks/ src/components/canvas/ 2>/dev/null | grep -iE \"invoke|generate-voice|voiceClone|render\" | head -25",
  "description": "voiceClone dispatch path"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/hooks/useVeoPoll.ts:13: * Molde: `useVoiceRenderPoll` (useAvatarVoice.ts:83) — intervalo fixo, para nos estados terminais.
> src/hooks/useAvatarVoice.ts:5:// avatar-clone-ai Fatia 2 — Harness hook for the `generate-voice` Edge Function (FR-AC-009).
> src/hooks/useAvatarVoice.ts:9:  const { data, error } = await supabase.functions.invoke("generate-voice", { body });
> src/hooks/useAvatarVoice.ts:42:  /** qwen3-local returns 202 queued — poll the render via useVoiceRenderPoll. */
> src/hooks/useAvatarVoice.ts:65:  /** qwen3-local returns 202 queued — poll the render via useVoiceRenderPoll. */
> src/hooks/useAvatarVoice.ts:83:export function useVoiceRenderPoll(renderId: string | undefined) {
> src/hooks/useAvatarVoice.ts:85:    queryKey: ["voice-render", renderId],
> src/components/canvas/nodes/VoiceCloneNode.tsx:10:// avatar-clone-ai Fatia 2 — voiceClone canvas node (display-only; logic lives in VoiceCloneInspector + useAvatarVoice).
> src/components/canvas/nodes/VoiceCloneNode.tsx:57:          {d.provider === "qwen3-local" ? "mcorch" : d.provider}
> src/components/canvas/nodes/VoiceCloneNode.tsx:60:        {d.provider === "qwen3-local" ? (
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:10:import { useAvatarVoiceClone, useAvatarVoiceSynthesize, useVoiceRenderPoll } from "@/hooks/useAvatarVoice";
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:42:// FR-SPACES-059 — short validation clips enriching the composite voice reference (qwen3-local).
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:48:  { id: "qwen3-local", label: "MCORCH · grátis", keyless: true },
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:117:  const isLocal = d.provider === "qwen3-local";
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:121:  // ── qwen3-local async: poll the queued render until terminal, then apply it to the node. ──
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:122:  const renderPoll = useVoiceRenderPoll(d.pendingRenderId);
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:293:        // qwen3-local — async: the host worker clones; the poll effect applies the profile.
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:328:        // qwen3-local — async batch (RTF ~6: 1 min de áudio ≈ 6 min de fila); the poll effect applies it.
> src/components/canvas/RightPanel/NodeInspectorBody.tsx:71:  ) : node.data.kind === "voiceClone" ? (
> ```

## 🤖 Claude *(00:18:43)*

<details>
<summary>💭 Thinking Process</summary>

I'm seeing how the `imageToVideo` node works with the Veo provider—it constructs a payload with the node type, provider, model, and prompt, then adds either reference image URLs for presenter mode or an input asset URL for b-roll mode before sending it to canvas-execute.

For `generateImage` with Nano Banana, it's a simpler synchronous flow through canvas-execute that returns the output URL directly. But `voiceClone` is fundamentally different—it returns null from `resolveExecutePayload`, which means it bypasses canvas-execute entirely and instead gets triggered through the VoiceCloneInspector, which calls the voice synthesis edge function and polls the video renders queue for completion.

This is the key insight: the Run All pipeline doesn't actually generate the voice narrations, so those six narrations need to be dispatched separately through the generate-voice path. I need to trace through useAvatarVoice.ts to understand the contract for that synthesize flow, then build a runner that handles three distinct dispatch paths—one for generateImage, one for imageToVideo, and one for voiceClone.

</details>


## 🤖 Claude *(00:18:44)*

Agora está claro — há **3 caminhos de dispatch distintos**:
- `generateImage` → `canvas-execute` (síncrono)
- `imageToVideo` (Veo) → `canvas-execute` (submete LRO) → `veo-poll` (poll)
- `voiceClone` → `resolveExecutePayload` retorna **null** → vai por `generate-voice` (async 202 → poll `video_renders`), **NÃO** pelo Run All

Preciso do contrato exato dos 3. Deixa eu ler.

## 🤖 Claude *(00:18:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useAvatarVoice.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useMutation, useQuery } from "@tanstack/react-query";
> 2	import { supabase } from "@/integrations/supabase/client";
> 3	import type { VoiceLanguage, VoiceProvider } from "@/lib/avatar";
> 4	
> 5	// avatar-clone-ai Fatia 2 — Harness hook for the `generate-voice` Edge Function (FR-AC-009).
> 6	// Logic lives here; the VoiceClone inspector is display-only.
> 7	
> 8	async function invokeGenerateVoice<T>(body: Record<string, unknown>): Promise<T> {
> 9	  const { data, error } = await supabase.functions.invoke("generate-voice", { body });
> 10	  if (error) {
> 11	    // Surface the structured PT-BR error/action from a non-2xx body (BYOK 402, 422 guard, etc.).
> 12	    let message = error.message;
> 13	    try {
> 14	      const ctx = (error as { context?: Response }).context;
> 15	      const parsed = ctx ? await ctx.json() : null;
> 16	      if (parsed?.error) {
> 17	        message = parsed.action ? `${parsed.error} — ${parsed.action}` : (parsed.error as string);
> 18	      }
> 19	    } catch {
> 20	      // keep original message
> 21	    }
> 22	    throw new Error(message);
> 23	  }
> 24	  return data as T;
> 25	}
> 26	
> 27	export interface CloneVoiceParams {
> 28	  sample_audio_url: string;
> 29	  /** qwen3-local: owner-prefixed Storage key of the sample (the async worker downloads it directly). */
> 30	  sample_storage_path?: string;
> 31	  sample_bucket?: string;
> 32	  /** FR-SPACES-059 — up to 5 short validation clips (≤7s each, owner-prefixed keys). qwen3-local only. */
> 33	  validation_storage_paths?: string[];
> 34	  provider: VoiceProvider;
> 35	  language: VoiceLanguage;
> 36	  project_id?: string;
> 37	  name?: string;
> 38	}
> 39	export interface CloneVoiceResult {
> 40	  /** Sync providers (elevenlabs/cartesia) return the profile immediately. */
> 41	  voice_profile_id?: string;
> 42	  /** qwen3-local returns 202 queued — poll the render via useVoiceRenderPoll. */
> 43	  status?: "queued";
> 44	  render_id?: string;
> 45	  provider: VoiceProvider;
> 46	  language: VoiceLanguage;
> 47	}
> 48	
> 49	export interface SynthesizeVoiceParams {
> 50	  voice_profile_id: string;
> 51	  script: string;
> 52	  language: VoiceLanguage;
> 53	  provider: VoiceProvider;
> 54	  project_id?: string;
> 55	  /** Canvas node id — lets the worker register the execution in the project Histórico. */
> 56	  node_id?: string;
> 57	  /** FR-SPACES-060 — expressive mode (qwen3-local): 1.7B + inline emotion markup, slower queue. */
> 58	  expressive?: boolean;
> 59	}
> 60	export interface SynthesizeVoiceResult {
> 61	  /** Sync providers return the signed URL immediately. */
> 62	  audio_url?: string;
> 63	  creative_asset_id?: string | null;
> 64	  mco_charged: number;
> 65	  /** qwen3-local returns 202 queued — poll the render via useVoiceRenderPoll. */
> 66	  status?: "queued";
> 67	  render_id?: string;
> 68	}
> 69	
> 70	export interface VoiceRenderRow {
> 71	  id: string;
> 72	  state: "queued" | "running" | "qa_gate" | "done" | "qa_failed" | "failed";
> 73	  storage_key: string | null;
> 74	  qa: { voice_profile_id?: string; creative_asset_id?: string | null; error?: string } | null;
> 75	}
> 76	
> 77	const TERMINAL_STATES = new Set(["done", "failed", "qa_failed"]);
> 78	
> 79	/**
> 80	 * Polls a qwen3-voice render row (video_renders, RLS SELECT-own) until terminal — the same
> 81	 * poll contract the cinematicVideo node uses. Stops refetching once terminal.
> 82	 */
> 83	export function useVoiceRenderPoll(renderId: string | undefined) {
> 84	  return useQuery({
> 85	    queryKey: ["voice-render", renderId],
> 86	    enabled: Boolean(renderId),
> 87	    refetchInterval: (query) => {
> 88	      const state = (query.state.data as VoiceRenderRow | undefined)?.state;
> 89	      return state && TERMINAL_STATES.has(state) ? false : 4000;
> 90	    },
> 91	    queryFn: async (): Promise<VoiceRenderRow> => {
> 92	      const { data, error } = await supabase
> 93	        .from("video_renders")
> 94	        .select("id, state, storage_key, qa")
> 95	        .eq("id", renderId!)
> 96	        .maybeSingle();
> 97	      if (error) throw error;
> 98	      if (!data) throw new Error("render não encontrado");
> 99	      return data as VoiceRenderRow;
> 100	    },
> 101	  });
> 102	}
> 103	
> 104	/** Clone a reference voice (ElevenLabs IVC / Cartesia). Returns the persisted voice_profiles id. No mco charge. */
> 105	export function useAvatarVoiceClone() {
> 106	  return useMutation({
> 107	    mutationFn: (params: CloneVoiceParams) =>
> 108	      invokeGenerateVoice<CloneVoiceResult>({ action: "clone", ...params }),
> 109	  });
> 110	}
> 111	
> 112	/** Synthesize a script with a cloned voice. Charges VOICE_GENERATION (36 mco) atomically server-side. */
> 113	export function useAvatarVoiceSynthesize() {
> 114	  return useMutation({
> 115	    mutationFn: (params: SynthesizeVoiceParams) =>
> 116	      invokeGenerateVoice<SynthesizeVoiceResult>({ action: "synthesize", ...params }),
> 117	  });
> 118	}
> 119	
> ```

## 🤖 Claude *(00:18:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useVeoPoll.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery } from "@tanstack/react-query";
> 2	import { supabase } from "@/integrations/supabase/client";
> 3	import { edgeErrorMessage } from "@/lib/edge";
> 4	
> 5	/**
> 6	 * Poll de uma geração Veo 3.1 (Amendment 25, FR-SPACES-090).
> 7	 *
> 8	 * O Veo é long-running SEM webhook: o `canvas-execute` devolve 202 + `execution_id` com o débito já
> 9	 * feito (ledger-first), e este hook chama `veo-poll` até `done`/`error`. O seam server-side é quem
> 10	 * baixa o MP4 (o URI do Veo exige a chave no header — ela NUNCA chega ao browser), materializa no
> 11	 * bucket privado e finaliza o ledger (estorno integral em falha).
> 12	 *
> 13	 * Molde: `useVoiceRenderPoll` (useAvatarVoice.ts:83) — intervalo fixo, para nos estados terminais.
> 14	 */
> 15	
> 16	export type VeoPollStatus = "running" | "done" | "error";
> 17	
> 18	export interface VeoPollResult {
> 19	  status: VeoPollStatus;
> 20	  execution_id: string;
> 21	  video_url?: string | null;
> 22	  asset_id?: string | null;
> 23	  bytes?: number;
> 24	  refunded?: number;
> 25	  message?: string;
> 26	  error?: string;
> 27	  transient?: boolean;
> 28	}
> 29	
> 30	const TERMINAL: ReadonlySet<VeoPollStatus> = new Set<VeoPollStatus>(["done", "error"]);
> 31	
> 32	export function useVeoPoll(generationId: string | undefined) {
> 33	  return useQuery({
> 34	    queryKey: ["veo-poll", generationId],
> 35	    enabled: Boolean(generationId),
> 36	    // O Veo leva 1–3 min; 6s é o meio-termo entre latência percebida e chamadas desperdiçadas.
> 37	    refetchInterval: (query) => {
> 38	      const status = (query.state.data as VeoPollResult | undefined)?.status;
> 39	      return status && TERMINAL.has(status) ? false : 6000;
> 40	    },
> 41	    queryFn: async (): Promise<VeoPollResult> => {
> 42	      const { data, error } = await supabase.functions.invoke("veo-poll", {
> 43	        body: { generation_id: generationId },
> 44	      });
> 45	      if (error) throw new Error(await edgeErrorMessage(error, "Falha ao consultar o vídeo."));
> 46	      return data as VeoPollResult;
> 47	    },
> 48	  });
> 49	}
> 50	
> ```

## 🤖 Claude *(00:18:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts",
  "offset": 1558,
  "limit": 130
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1558	 * `canvas-execute` Edge Function. Soul models split into provider/model
> 1559	 * plus parameters.resolution/batch so the function's tiering helper
> 1560	 * (`resolveHiggsfieldSoulKey`) computes the correct cost.
> 1561	 */
> 1562	export function resolveExecutePayload(
> 1563	  data: CanvasNodeData,
> 1564	  styleSettings?: StyleSettings,
> 1565	): {
> 1566	  node_type: string;
> 1567	  /** `google` entrou com o Veo (Amendment 25) — os demais motores seguem sendo `ProviderId`. */
> 1568	  provider: ProviderId | "google";
> 1569	  model: string;
> 1570	  prompt: string;
> 1571	  negative_prompt?: string;
> 1572	  parameters: Record<string, unknown>;
> 1573	} | null {
> 1574	  switch (data.kind) {
> 1575	    case "generateImage": {
> 1576	      const info = getImageModelInfo(data.modelId);
> 1577	      const parameters: Record<string, unknown> = {
> 1578	        aspect_ratio: data.aspectRatio,
> 1579	        controls: data.controls,
> 1580	        seed: data.fixedSeed && data.seed != null ? data.seed : undefined,
> 1581	      };
> 1582	      if (info.resolution) parameters.resolution = info.resolution;
> 1583	      if (info.batch) parameters.batch = info.batch;
> 1584	      return {
> 1585	        node_type: "generate_image",
> 1586	        provider: info.provider,
> 1587	        model: info.modelParam,
> 1588	        prompt: compileFinalPrompt(data.prompt, styleSettings, data.inheritStyle),
> 1589	        negative_prompt: data.negativePrompt || undefined,
> 1590	        parameters,
> 1591	      };
> 1592	    }
> 1593	    case "sceneCompose": {
> 1594	      const info = getImageModelInfo(data.modelId);
> 1595	      const parameters: Record<string, unknown> = {
> 1596	        aspect_ratio: data.aspectRatio,
> 1597	      };
> 1598	      if (info.resolution) parameters.resolution = info.resolution;
> 1599	      if (info.batch) parameters.batch = info.batch;
> 1600	      return {
> 1601	        node_type: "scene_compose",
> 1602	        provider: info.provider,
> 1603	        model: info.modelParam,
> 1604	        prompt: compileFinalPrompt(data.prompt, styleSettings, data.inheritStyle),
> 1605	        parameters,
> 1606	      };
> 1607	    }
> 1608	    case "styleTransfer": {
> 1609	      const preset = STYLE_TRANSFER_PRESETS.find((p) => p.id === data.presetId);
> 1610	      return {
> 1611	        node_type: "style_transfer",
> 1612	        provider: "higgsfield",
> 1613	        model: "soul",
> 1614	        prompt: preset?.suffix ?? "",
> 1615	        parameters: {
> 1616	          strength: data.strength,
> 1617	          preset_id: data.presetId,
> 1618	          resolution: "720p",
> 1619	          batch: 1,
> 1620	        },
> 1621	      };
> 1622	    }
> 1623	    case "imageToVideo": {
> 1624	      const info = getVideoModelInfo(data.videoModel);
> 1625	      // Amendment 25: o Veo tem contrato PRÓPRIO (duração 4..8 + resolução; 9:16/16:9 apenas).
> 1626	      // Um payload com o shape do Higgsfield seria 422 no servidor — o motor decide o shape.
> 1627	      if (isVeoTier(info.modelParam)) {
> 1628	        return {
> 1629	          node_type: "image_to_video",
> 1630	          provider: "google",
> 1631	          model: info.modelParam,
> 1632	          prompt: data.prompt,
> 1633	          parameters: {
> 1634	            duration: data.veoDuration ?? VEO_DEFAULT_DURATION,
> 1635	            resolution: data.veoResolution ?? VEO_DEFAULT_RESOLUTION,
> 1636	            // O Veo só aceita 9:16 e 16:9. Nó legado sem `aspectRatio` (ou com 1:1) → 9:16, nunca
> 1637	            // `undefined` no payload (o servidor já cairia em 9:16, mas o contrato sai explícito).
> 1638	            aspect_ratio: data.aspectRatio === "16:9" ? "16:9" : "9:16",
> 1639	            // Veo 3 gera fala/áudio por padrão (a fonte do "saiu falando em pt-BR"). Padrão MUDO;
> 1640	            // togglável no nó — o servidor só emite o flag para DESLIGAR.
> 1641	            generate_audio: data.veoGenerateAudio ?? false,
> 1642	            async_only: true,
> 1643	          },
> 1644	        };
> 1645	      }
> 1646	      return {
> 1647	        node_type: "image_to_video",
> 1648	        provider: info.provider,
> 1649	        model: info.modelParam,
> 1650	        prompt: data.prompt,
> 1651	        parameters: {
> 1652	          duration: data.duration,
> 1653	          aspect_ratio: data.aspectRatio,
> 1654	          motion_strength: data.motionStrength,
> 1655	          async_only: info.asyncOnly ?? false,
> 1656	        },
> 1657	      };
> 1658	    }
> 1659	    case "characterReference":
> 1660	      // CharacterReference doesn't trigger canvas-execute by itself —
> 1661	      // it's a data source consumed by downstream sceneCompose/styleTransfer.
> 1662	      return null;
> 1663	    case "productList":
> 1664	      // productList is a 0-cost input node (it.4a) — a downstream generateImage reads its items
> 1665	      // and expands them into N runs; the list node never calls canvas-execute itself.
> 1666	      return null;
> 1667	    case "upscale":
> 1668	      // it.4c — REAL Replicate real-esrgan; the input image comes from the upstream node
> 1669	      // (threaded as input_asset_url by the pipeline). No prompt/model — scale drives cost.
> 1670	      return {
> 1671	        node_type: "upscale",
> 1672	        provider: "replicate",
> 1673	        model: "real-esrgan",
> 1674	        prompt: "",
> 1675	        parameters: { scale: data.scale, face_enhance: data.faceEnhance },
> 1676	      };
> 1677	    case "voiceClone":
> 1678	      // voiceClone runs against the net-new `generate-voice` Edge Function (FR-AC-009),
> 1679	      // NOT canvas-execute — its inspector calls useAvatarVoice directly.
> 1680	      return null;
> 1681	    case "avatarIdentity":
> 1682	      // avatarIdentity trains against the net-new `avatar-identity-train` Edge Function
> 1683	      // (FR-AC-012, gated OTD-AC-017), NOT canvas-execute — inspector handles it directly.
> 1684	      return null;
> 1685	    case "publishWordpress":
> 1686	      // publishWordpress is a distribution SINK — it calls publish-wordpress from its inspector
> 1687	      // (spaces-evolution Amendment 15 FR-SPACES-031/032), NOT canvas-execute.
> ```

## 🤖 Claude *(00:19:27)*

<details>
<summary>💭 Thinking Process</summary>

For the `generateImage` path, I need to construct a canvas-execute payload with the project and node identifiers, set the node type to generate_image, pull the provider details from the image model info, include the compiled prompt and negative prompt, configure parameters like a 16:9 aspect ratio with any controls and seed, and generate a unique node run ID—this syncs and returns the output URL while costing 10 mco.

For `imageToVideo` with Veo, the canvas-execute payload specifies the Google provider with veo-3.1-fast, includes the prompt and duration/resolution parameters with async_only enabled, then branches based on mode: presenter mode adds a signed character reference image URL, while b-roll mode uses the Nano Banana output as the input asset. This returns a 202 with an execution ID that I poll until completion, costing 267 for presenter or 134-167 for b-roll depending on duration.

For `voiceClone` using qwen3-local, I bypass canvas-execute entirely and call generate-voice directly with the synthesize action, passing the voice profile ID, script, language, and provider, then poll the video_renders endpoint by the returned render ID until the state reaches done or failed.

But here's the critical issue: synthesize absolutely requires a voice_profile_id, yet the EP05 voice nodes in the data only show kind, label, prompt, status, language, and provider—no voice_profile_id attached. This means either there's a default voice profile I'm missing, or the synthesize call would fail. I need to check whether qwen3-local can run with a default voice when no explicit profile is provided, and I'm also noting that the synthesis charges 36 MCO atomically server-side.

There's a contradiction I need to resolve: the runbook claims qwen3-local narration is 0 MCO (self-hosted free), but the hook comment says synthesize charges 36 MCO. I need to read the generate-voice edge function to get the actual ground truth on pricing before proceeding. I need to dig into the generate-voice function to see exactly what the synthesize action expects — specifically whether voice_profile_id is required for qwen3-local and what the charging model actually is. The runbook lists "6 narrations Qwen3 (0 mco)" as free, but if synthesize requires a cloned voice profile and we don't have a Gabriel sample to clone from, that changes everything about what's actually possible in phase 1.

</details>


## 🤖 Claude *(00:19:29)*

Contrato dos 3 caminhos mapeado. Mas duas **contradições que Lei 1 me obriga a resolver ANTES de rodar**:

1. O hook diz `synthesize` "Charges VOICE_GENERATION (36 mco)" — mas o runbook diz voz Qwen3 = **0 mco**. Qual é a verdade?
2. `synthesize` exige `voice_profile_id`, mas os nós de voz do EP05 não têm um perfil de clone anexado (nem amostra de referência).

Vou ler a edge `generate-voice` — a fonte da verdade sobre custo do qwen3-local + resolução de perfil.

## 🤖 Claude *(00:19:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l supabase/functions/generate-voice/index.ts; echo \"---\"; grep -nE \"qwen3-local|voice_profile_id|synthesize|VOICE_GENERATION|charge|deduct|mco|default|profile|action ===|202|queued|render\" supabase/functions/generate-voice/index.ts | head -70",
  "description": "generate-voice contract recon"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 513 supabase/functions/generate-voice/index.ts
> ---
> 9://   action: "clone"      → Instant Voice Cloning (ElevenLabs IVC / Cartesia) → voice_profiles row. No mco.
> 10://   action: "synthesize" → TTS with a cloned voice → audio asset. Charges VOICE_COST (36) atomically.
> 22:const VOICE_COST = 36; // mirror COIN_COSTS.VOICE_GENERATION (src/lib/billing.ts) — Deno can't import src/lib.
> 25:const CARTESIA_VERSION = "2026-03-01";
> 27:// Amendment 18 (FR-SPACES-055/056): qwen3-local = free self-host engine. The edge fn can't reach the
> 28:// host motor — it ENQUEUES a video_renders row (engine 'qwen3-voice', charged_mco 0) that the host
> 33:type VoiceProvider = "elevenlabs" | "cartesia" | "qwen3-local";
> 101:      : body?.provider === "qwen3-local" ? "qwen3-local" : "elevenlabs") as VoiceProvider;
> 127:    if (action === "clone") {
> 132:      // BYOK gate — external providers only. qwen3-local is keyless by design (FR-SPACES-056:
> 134:      const apiKey = provider === "qwen3-local" ? "" : keyFor(provider);
> 135:      if (provider !== "qwen3-local" && !apiKey) {
> 149:      // ── qwen3-local: enqueue for the host worker (async — the edge fn can't reach the motor). ──
> 150:      if (provider === "qwen3-local") {
> 153:        // Owner-prefix rule = tenant isolation (mirrors the storage RLS of 20260703030000): a caller
> 170:        const { data: render, error: qErr } = await admin.from("video_renders").insert({
> 171:          user_id: userId, engine: "qwen3-voice", state: "queued", charged_mco: 0, voice_consent: true,
> 173:            kind: "voice_clone", provider: "qwen3-local", language,
> 178:        if (qErr || !render) {
> 179:          console.error("[generate-voice] qwen3-local clone enqueue error:", qErr);
> 183:        await pulse("healthy", "avatar_voice_clone", { provider, language, render_id: render.id, mode: "queued" });
> 184:        return json({ status: "queued", render_id: render.id, provider, language }, 202);
> 198:      // personality clips too (owner-prefixed keys, same rule as qwen3-local). Cartesia's clone
> 224:      const { data: profileId, error: storeErr } = await admin.rpc("store_voice_profile", {
> 233:        console.error("[generate-voice] store_voice_profile error:", storeErr);
> 235:        return json({ error: "voice_profile_store_failed" }, 500);
> 239:      admin.from("mcorch_nodes").insert({
> 242:        name: `avatar-voice-clone:${profileId}`,
> 244:        metadata: { module: SERVICE, event: "avatar_voice_clone", voice_profile_id: profileId, provider, language },
> 248:      return json({ voice_profile_id: profileId, provider, language });
> 252:    // ACTION: synthesize
> 254:    if (action === "synthesize") {
> 255:      const voiceProfileId = String(body?.voice_profile_id ?? "");
> 257:      if (!voiceProfileId) return json({ error: "voice_profile_id is required" }, 400);
> 260:      // Resolve the OWNER-scoped voice profile (decrypts the provider voice_id; tenant-guarded by the RPC).
> 261:      const { data: rows, error: resolveErr } = await admin.rpc("resolve_voice_profile", {
> 266:        console.error("[generate-voice] resolve_voice_profile error:", resolveErr);
> 267:        return json({ error: "voice_profile_resolve_failed" }, 500);
> 269:      const profile = Array.isArray(rows) ? rows[0] : rows;
> 270:      if (!profile) return json({ error: "voice_profile_not_found" }, 404);
> 271:      if (profile.status !== "active") return json({ error: "voice_profile_revoked" }, 403);
> 273:      const profProvider = (profile.provider === "cartesia" ? "cartesia"
> 274:        : profile.provider === "qwen3-local" ? "qwen3-local" : "elevenlabs") as VoiceProvider;
> 276:      // HARD code-switch gate (FR-AC-010): the voice was cloned in profile.language — never accent-bleed.
> 277:      if (profile.language !== language) {
> 278:        return json({ error: "language_mismatch", detail: `voz clonada em ${profile.language}, pedido em ${language}` }, 422);
> 291:      // BYOK for the profile's provider (the voice_id is provider-specific). qwen3-local is keyless.
> 292:      const apiKey = profProvider === "qwen3-local" ? "" : keyFor(profProvider);
> 293:      if (profProvider !== "qwen3-local" && !apiKey) {
> 299:      // ALL of it, block the render. Profiles created post-Fatia-3a always carry an active consent (clone requires
> 300:      // it); legacy/pre-consent profiles (no consent rows) are not blocked here.
> 307:      // ── qwen3-local: enqueue for the host worker — 0 mco (FR-SPACES-056, free directive). ──
> 308:      // All the gates above (owner-scoped profile, language, code-switch, sentinel, consent) already
> 309:      // ran; the worker only executes what this fn approved. No deduct → no refund path needed.
> 310:      if (profProvider === "qwen3-local") {
> 311:        const { data: render, error: qErr } = await admin.from("video_renders").insert({
> 312:          user_id: userId, engine: "qwen3-voice", state: "queued", charged_mco: 0, voice_consent: true,
> 314:            kind: "voice_synthesize", provider: "qwen3-local", language,
> 315:            voice_profile_id: voiceProfileId, script,
> 321:        if (qErr || !render) {
> 322:          console.error("[generate-voice] qwen3-local synth enqueue error:", qErr);
> 326:        await pulse("healthy", "avatar_voice", { provider: profProvider, language, render_id: render.id, mode: "queued" });
> 327:        return json({ status: "queued", render_id: render.id, mco_charged: 0 }, 202);
> 331:      const { data: prof } = await admin.from("profiles").select("mco_balance").eq("id", userId).maybeSingle();
> 332:      if (((prof?.mco_balance as number | null) ?? 0) < VOICE_COST) {
> 333:        return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 335:      const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: VOICE_COST });
> 336:      if (deductErr) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 338:      // Synthesize (provider call). Refund on failure — never charge-without-value (FM-AC-005).
> 343:          audioBytes = await cartesiaTTS(apiKey, profile.voice_id, script, language);
> ```

## 🤖 Claude *(00:19:52)*

<details>
<summary>💭 Thinking Process</summary>

I've found the ground truth on the voice cost issue—`qwen3-local` synthesis returns 0 mco because it only enqueues video renders without charging, while the 36 mco voice cost only applies to paid providers like elevenlabs and cartesia. The runbook is correct.

Now I'm hitting a blocker: the synthesize endpoint requires a `voice_profile_id` parameter, and it must be an active, owner-scoped profile matching the target language (pt-BR). The EP05 voice nodes don't have one attached, so either User 0 already has an active qwen3-local pt-BR voice profile from earlier episodes, or I need to create one first by cloning a reference sample. Let me check the voice_profiles table for User 0 to see what's available.

</details>


## 🤖 Claude *(00:19:52)*

**Contradição de custo RESOLVIDA (Lei 1):** `qwen3-local` synthesize = **0 mco confirmado** (linha 310-327: enfileira `video_renders charged_mco:0`, 202). Os 36 mco só valem pra providers pagos. Runbook correto.

**Mas achado bloqueante:** `synthesize` **exige `voice_profile_id` ativo pt-BR** (linha 257) — não há voz default. Os nós EP05 não mostraram perfil anexado. Preciso saber se o User 0 já tem um perfil de voz clonada qwen3-local pt-BR, ou se a voz está bloqueada em amostra de referência (suas mãos).

## 🤖 Claude *(00:19:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/voice.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst U0='ada39fae-67e1-4e53-af1c-5a18e1c108e8';\n// voice_profiles for User 0\nconst { data: profs, error } = await admin.from('voice_profiles').select('id, provider, language, status, name, created_at').eq('user_id',U0).order('created_at',{ascending:false});\nconsole.log('=== voice_profiles (User 0):', error? error.message : (profs?.length+' rows'), '===');\nfor(const p of profs??[]) console.log('  '+p.id+'  '+String(p.provider).padEnd(12)+String(p.language).padEnd(7)+String(p.status).padEnd(9)+(p.name??'')+'  '+p.created_at);\n// full voice node data\nconst { data: proj } = await admin.from('vm_canvas_projects').select('graph').eq('id','18a21002-df9c-48b4-aff3-7aba28e812e7').single();\nconst vn=(proj as any).graph.nodes.find((n:any)=>n.id==='n_voice_ato1');\nconsole.log('\\n=== n_voice_ato1 FULL data keys ===', Object.keys(vn.data));\nconsole.log('  voiceProfileId:', vn.data.voiceProfileId, '| profileId:', vn.data.profileId, '| sampleUrl:', vn.data.sampleUrl, '| pendingRenderId:', vn.data.pendingRenderId, '| output:', JSON.stringify(vn.data.output)?.slice(0,120));\nEOF\nbun run /tmp/voice.ts 2>&1 | head -40",
  "description": "Query voice profiles + node data"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === voice_profiles (User 0): column voice_profiles.name does not exist ===
> 
> === n_voice_ato1 FULL data keys === [ "kind", "label", "prompt", "status", "language", "provider" ]
>   voiceProfileId: undefined | profileId: undefined | sampleUrl: undefined | pendingRenderId: undefined | output: undefined
> ```

## 🤖 Claude *(00:20:03)*

<details>
<summary>💭 Thinking Process</summary>

I see the voice node is missing the profile ID and sample URL, so I need to fix the profiles query since the name column doesn't exist—let me query the voice_profiles table with the correct column names instead.

</details>


## 🤖 Claude *(00:20:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/voice2.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst U0='ada39fae-67e1-4e53-af1c-5a18e1c108e8';\nconst { data: one } = await admin.from('voice_profiles').select('*').eq('user_id',U0).limit(1);\nif(one && one[0]) console.log('COLUMNS:', Object.keys(one[0]));\nconst { data: profs, error } = await admin.from('voice_profiles').select('id, provider, language, status, created_at, label').eq('user_id',U0).order('created_at',{ascending:false});\nconsole.log('=== voice_profiles (User 0):', error? error.message : (profs?.length+' rows'), '===');\nfor(const p of profs??[] as any[]) console.log('  '+p.id+'  '+String(p.provider).padEnd(12)+String(p.language).padEnd(7)+String(p.status).padEnd(9)+(p.label??'')+'  '+p.created_at);\nEOF\nbun run /tmp/voice2.ts 2>&1 | head -40",
  "description": "voice_profiles correct columns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> COLUMNS: [
>   "id", "user_id", "project_id", "provider", "clone_method", "voiceprint_vault_ref", "language",
>   "status", "last_used_at", "created_at", "updated_at"
> ]
> === voice_profiles (User 0): column voice_profiles.label does not exist ===
> ```

## 🤖 Claude *(00:20:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/voice3.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst U0='ada39fae-67e1-4e53-af1c-5a18e1c108e8';\nconst { data: profs } = await admin.from('voice_profiles').select('id, provider, clone_method, language, status, created_at, last_used_at').eq('user_id',U0).order('created_at',{ascending:false});\nconsole.log('=== voice_profiles (User 0): '+(profs?.length??0)+' rows ===');\nfor(const p of profs??[] as any[]) console.log('  '+p.id+'  '+String(p.provider).padEnd(12)+String(p.clone_method??'').padEnd(10)+String(p.language).padEnd(7)+String(p.status).padEnd(9)+' used='+(p.last_used_at??'-')+'  '+p.created_at);\n// qwen3-local active pt-BR specifically\nconst q = (profs??[]).filter((p:any)=>p.provider==='qwen3-local' && p.language==='pt-BR' && p.status==='active');\nconsole.log('\\n>>> qwen3-local pt-BR ACTIVE profiles usable for synthesize:', q.length);\nfor(const p of q as any[]) console.log('   USABLE:', p.id);\nEOF\nbun run /tmp/voice3.ts 2>&1 | head -40",
  "description": "Find usable qwen3-local pt-BR profile"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === voice_profiles (User 0): 2 rows ===
>   541bced7-a351-4919-ba44-8ef005c6c53b  qwen3-local ivc       pt-BR  active    used=2026-07-10T20:22:11.535+00:00  2026-07-10T20:21:18.661028+00:00
>   c4d72b8f-9acb-4832-987c-37093a0b91e1  qwen3-local ivc       pt-BR  active    used=2026-07-30T23:41:06.599+00:00  2026-07-10T19:26:33.603281+00:00
> 
> >>> qwen3-local pt-BR ACTIVE profiles usable for synthesize: 2
>    USABLE: 541bced7-a351-4919-ba44-8ef005c6c53b
>    USABLE: c4d72b8f-9acb-4832-987c-37093a0b91e1
> ```

## 🤖 Claude *(00:20:40)*

<details>
<summary>💭 Thinking Process</summary>

I'm finding that there are actually two usable voice profiles available for this user, with the more recent one from late July being the likely current Gabriel AI voice that was used in the React shorts session. I've confirmed that c4d72b8f is the canonical Gabriel AI voice based on its last use timestamp matching the React shorts session from 2026-07-30. Now I need to verify the exact model parameter for veo-3.1-fast that the server expects in ALLOWED_VIDEO_MODELS, and I'm checking the getVideoModelInfo and getImageModelInfo mappings to ensure I'm passing the correct values to the runner.

For the reference images, I realize I should mirror the client's exact approach rather than reimplementing the reference collection and re-signing logic myself—this avoids divergence and potential wasted compute. I'll use the charRef node's imageUrls and re-sign them fresh through the storage API to match what the client does.

I need to look up the model info helpers for both video and image generation, check the default duration and resolution constants, and understand how compileFinalPrompt works with the node's inheritStyle setting. I'll also need to grab a fresh signed URL for the charRef image from the canvas-assets storage bucket.

</details>


## 🤖 Claude *(00:20:43)*

**Achado resolvido:** User 0 tem **2 perfis qwen3-local pt-BR ativos**. O `c4d72b8f` foi **usado 2026-07-30** (a sessão dos shorts React Gabriel AI = a voz canônica atual). Então a narração clonada **está disponível** — só preciso passar `voice_profile_id`.

Tenho quase tudo. Faltam os model params exatos (o server valida `ALLOWED_VIDEO_MODELS`). Deixa eu confirmar os mapeamentos de modelo antes de montar o runner.

## 🤖 Claude *(00:20:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"getVideoModelInfo|getImageModelInfo|VEO_DEFAULT_DURATION|VEO_DEFAULT_RESOLUTION|isVeoTier|modelParam|veo-3.1-fast|openrouter-gemini-image|gemini-image\" src/types/canvas.ts | head -40; echo \"=== ALLOWED_VIDEO_MODELS in server ===\"; grep -nE \"ALLOWED_VIDEO_MODELS|veo-3\" supabase/functions/canvas-execute/index.ts | head",
  "description": "Model param mappings"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 17:  isVeoTier,
> 18:  VEO_DEFAULT_DURATION,
> 19:  VEO_DEFAULT_RESOLUTION,
> 87:  | "openrouter-gemini-image"
> 96:  modelParam: string;
> 119:    modelParam: "soul",
> 130:    modelParam: "soul",
> 141:    modelParam: "soul",
> 152:    modelParam: "soul",
> 163:    modelParam: "dall-e-3",
> 171:    modelParam: "gpt-image-1",
> 179:    modelParam: "flux-1.1-pro",
> 187:    modelParam: "flux-schnell",
> 195:    modelParam: "sdxl",
> 200:  "openrouter-gemini-image": {
> 203:    modelParam: "google/gemini-2.5-flash-image",
> 211:    modelParam: "black-forest-labs/flux-1.1-pro",
> 219:    modelParam: "dall-e-3",
> 226:export const DEFAULT_IMAGE_MODEL: ImageModelId = "openrouter-gemini-image";
> 240:  | "veo-3.1-fast"
> 250:  modelParam: string;
> 267:    modelParam: "dop-lite",
> 276:    modelParam: "dop-turbo",
> 285:    modelParam: "dop-standard",
> 295:    modelParam: "kling-2.1-pro",
> 305:    modelParam: "seedance-v1-pro",
> 316:    modelParam: "veo-3.1-lite",
> 324:  "veo-3.1-fast": {
> 327:    modelParam: "veo-3.1-fast",
> 338:    modelParam: "veo-3.1",
> 354: * ("openrouter-gemini-image", "dop-standard-5s"). Direct `MODEL_INFO[id].coinCost`
> 361:  modelParam: "",
> 369:  modelParam: "",
> 375:export function getImageModelInfo(id: string | null | undefined): ImageModelInfo {
> 378:export function getVideoModelInfo(id: string | null | undefined): VideoModelInfo {
> 1116:  const modelId = overrides.modelId ?? "openrouter-gemini-image";
> 1219:    videoModel: "veo-3.1-fast",
> 1576:      const info = getImageModelInfo(data.modelId);
> 1587:        model: info.modelParam,
> 1594:      const info = getImageModelInfo(data.modelId);
> === ALLOWED_VIDEO_MODELS in server ===
> 63:// Contract pinned by live probe (.claude/context/veo-31-contract-probe-2026-07-14.md):
> 70:  "veo-3.1": { "720p": 0.40, "1080p": 0.40 },
> 71:  "veo-3.1-fast": { "720p": 0.10, "1080p": 0.12 },
> 72:  "veo-3.1-lite": { "720p": 0.05, "1080p": 0.08 },
> 75:  "veo-3.1": "veo-3.1-generate-preview",
> 76:  "veo-3.1-fast": "veo-3.1-fast-generate-preview",
> 77:  "veo-3.1-lite": "veo-3.1-lite-generate-preview",
> 82:  "veo-3.1": { "720p": 0.40, "1080p": 0.40 },
> 83:  "veo-3.1-fast": { "720p": 0.15, "1080p": 0.15 },
> 86:  "veo-3.1": "veo-3.1-generate-001",
> ```

## 🤖 Claude *(00:21:13)*

<details>
<summary>💭 Thinking Process</summary>

I'm mapping out the configuration for both image and video generation—the image endpoint uses Gemini through OpenRouter at a cost of 10 mco, while the video generation leverages Veo 3.1 Fast with different model parameter mappings depending on whether it's running through AI Studio or another service.

I'm realizing there's a risk in reimplementing the client dispatch logic standalone since any subtle differences could waste real mco, so I'm considering using browser automation instead to drive the actual UI and run generations through the real interface—that way I'm using the exact client dispatch with no divergence risk, though it would be slower.

But for the smaller set of gated witnesses, the safest approach is probably to mirror `resolveExecutePayload` exactly in my script runner. I've read through the payload contract carefully now—each type is well-defined, and the only client-side additions are re-signed URLs for the presenter and b-roll inputs. I'll build the runner to match that contract precisely and validate it on the cheapest witness first (a single Nano Banana at 10 mco) before running anything expensive.

The witness order through the gate is: nano → b-roll (needs the nano's firstFrame output) → presenter (needs the charRef reference) → voice narrations. That's roughly 411 mco total across all witnesses. I'm planning to write one runner script that can execute any node by ID, handling all three paths with polling, then invoke it sequentially for each witness.

I need to mint a user JWT first (reusing the logic from gen-user-jwt.ts with admin generateLink and verifyOtp), since canvas-execute and generate-voice both require Authorization headers. Then for each node, I'll resolve the payload based on its kind, add any refs or inputs, invoke it, poll if it's async, and report back the asset and cost.

Let me check the response shapes for canvas-execute—image_to_video returns a 202 with execution_id while generate_image returns output_url directly. I also need to confirm ALLOWED_VIDEO_MODELS and the openrouter-gemini-image provider setup.

</details>


## 🤖 Claude *(00:21:14)*

Tenho os model params. Antes de montar o runner, preciso: (1) o minter de JWT do User 0, (2) o shape de resposta do `canvas-execute` (sync `output_url` vs 202 `execution_id`), (3) confirmar `ALLOWED_VIDEO_MODELS` + provider do openrouter-gemini-image.

## 🤖 Claude *(00:21:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/gen-user-jwt.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Mint a REAL user access_token (JWT) for authenticated edge-fn calls in QA — without a browser or raw password.
> 4	 * Admin generateLink (magiclink) → verifyOtp(token_hash) → session.access_token. Per-user, reproducible.
> 5	 * Pattern extends gen-magiclink.ts (v6.20.4). The token is one-time and ~1h-lived; mint right before use.
> 6	 *
> 7	 * Usage: bun run scripts/qa/gen-user-jwt.ts <email>
> 8	 *   → prints the access_token on stdout (nothing else), or an error on stderr + exit 1.
> 9	 *   e.g. TOKEN=$(bun run scripts/qa/gen-user-jwt.ts gabrielcall@gmail.com)
> 10	 */
> 11	import { createClient } from '@supabase/supabase-js';
> 12	
> 13	const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> 14	const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> 15	const ANON = (process.env.SB_PUBLISHABLE_KEY ?? process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? process.env.SUPABASE_ANON_KEY)!;
> 16	const email = process.argv[2];
> 17	if (!URL || !SVC || !ANON || !email) {
> 18	  console.error('Usage: gen-user-jwt.ts <email>  (needs SUPABASE_URL + SB_SECRET_KEY + SB_PUBLISHABLE_KEY)');
> 19	  process.exit(1);
> 20	}
> 21	
> 22	const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> 23	const anon = createClient(URL, ANON, { auth: { persistSession: false } });
> 24	
> 25	const { data, error } = await admin.auth.admin.generateLink({ type: 'magiclink', email });
> 26	if (error || !data.properties?.hashed_token) {
> 27	  console.error('generateLink error:', error?.message ?? 'no hashed_token');
> 28	  process.exit(1);
> 29	}
> 30	const tokenHash = data.properties.hashed_token;
> 31	
> 32	let accessToken: string | null = null;
> 33	for (const type of ['magiclink', 'email'] as const) {
> 34	  const { data: sess, error: vErr } = await anon.auth.verifyOtp({ token_hash: tokenHash, type });
> 35	  if (!vErr && sess?.session?.access_token) { accessToken = sess.session.access_token; break; }
> 36	}
> 37	if (!accessToken) { console.error('verifyOtp failed for both magiclink/email types'); process.exit(1); }
> 38	console.log(accessToken);
> 39	
> ```

## 🤖 Claude *(00:21:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts",
  "offset": 200,
  "limit": 10
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 200	  "openrouter-gemini-image": {
> 201	    label: "Nano Banana 2 (Gemini)",
> 202	    provider: "openrouter",
> 203	    modelParam: "google/gemini-2.5-flash-image",
> 204	    tier: "Rápido",
> 205	    coinCost: 10,
> 206	    eta: "4–8s",
> 207	  },
> 208	  "openrouter-flux-pro": {
> 209	    label: "FLUX 1.1 Pro (OpenRouter)",
> ```

## 🤖 Claude *(00:21:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"ALLOWED_VIDEO_MODELS =|execution_id|output_url|status.*202|return json|202\\)\" supabase/functions/canvas-execute/index.ts | head -40",
  "description": "canvas-execute response shapes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 287:    const ALLOWED_VIDEO_MODELS = [
> 436:            output_url: null,
> 448:            execution_id: execution.id,
> 461:            execution_id: execution.id,
> 644:        output_url: storedUrl || null,
> 670:          execution_id: execution.id,
> 691:      execution_id: execution.id,
> 693:      output_url: storedUrl || null,
> 942:      execution_id: generationId,
> 1018:    execution_id: generationId,
> 1074:      execution_id: generationId,
> 1243:    execution_id: generationId,
> 1279:      execution_id: generationId,
> 1313:    execution_id: generationId,
> 1707:      execution_id: begun.generation_id,
> 1858:      execution_id: generationId,
> 1878:      execution_id: generationId,
> 1935:      execution_id: generationId,
> 1968:    p_result: { output_url: storedUrl },
> 1973:      asset_id: assetId, result: { output_url: storedUrl },
> 1989:    execution_id: generationId,
> 1991:    output_url: storedUrl,
> 2476:      JSON.stringify({ error: msg, execution_id: execution.id, status: "failed" }),
> 2526:      execution_id: execution.id,
> ```

## 🤖 Claude *(00:21:29)*

<details>
<summary>💭 Thinking Process</summary>

I'm tracing through the ledger-first branch for the image_to_video Veo path to understand how it handles the LRO submission and polling. When the ledger-first condition is met (node_run_id present), the system submits the request and returns a 202 response with the execution_id set to the generation_id, which is then used for subsequent polling calls to veo-poll.

Now I need to check the needsLedgerRun function to determine which providers trigger the ledger path versus the legacy path — specifically whether generate_image with openrouter uses the ledger-first branch or falls back to the older flow.

</details>


## 🤖 Claude *(00:21:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasStudio.ts",
  "offset": 225,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 225	// it.2b (Amendment 14 FR-SPACES-024): sync node types run LEDGER-FIRST — a fresh node_run_id per
> 226	// attempt dispatches canvas-execute into the `generations` branch (begin→provider→finalize, atomic
> 227	// debit + automatic refund). image_to_video stays on the legacy path until it.2c wires the async
> 228	// settle + watchdog. SOP: docs/processes/spaces-graph-execution.md §Amendment it.2a.
> 229	const LEDGER_SYNC_NODE_TYPES = new Set([
> 230	  "generate_image",
> 231	  "magic_prompt",
> 232	  "scene_compose",
> 233	  "style_transfer",
> 234	  "upscale",
> 235	]);
> 236	
> 237	/**
> 238	 * Amendment 25 (FR-SPACES-086/090): o motor Veo é ledger-first por CONSTRUÇÃO (debita no submit,
> 239	 * estorna integralmente na falha, o poll finaliza). Sem `node_run_id` o `canvas-execute` despacha
> 240	 * para a branch LEGADA — que não conhece `google/veo-*` e devolveria 422: a feature nasceria morta.
> 241	 *
> 242	 * O gate é por PROVIDER, não pelo node_type: o vídeo do Higgsfield continua exatamente no caminho
> 243	 * legado que já está em produção (webhook `token=`), sem mudança de comportamento. Só o Veo entra
> 244	 * no `generations`.
> 245	 */
> 246	function needsLedgerRun(nodeType: string, provider: string): boolean {
> 247	  if (LEDGER_SYNC_NODE_TYPES.has(nodeType)) return true;
> 248	  return nodeType === "image_to_video" && provider === "google";
> 249	}
> 250	
> 251	export function useCanvasExecute() {
> 252	  const queryClient = useQueryClient();
> 253	
> 254	  return useMutation({
> 255	    mutationFn: async (params: {
> 256	      project_id: string;
> 257	      node_id: string;
> 258	      node_type: string;
> 259	      provider: string;
> 260	      model: string;
> 261	      prompt: string;
> 262	      negative_prompt?: string;
> 263	      parameters?: Record<string, unknown>;
> 264	      /** Phase 4.2c — required for image_to_video (upstream image URL). */
> ```

## 🤖 Claude *(00:21:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts",
  "offset": 1690,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1690	  if (beginErr) {
> 1691	    // deduct RAISE inside the RPC rolled the row back — surface the canonical 402 when it is a balance
> 1692	    // failure (race past the pre-check). Frozen accounts map to a GENERIC 403 (security-review LOW:
> 1693	    // never leak internal quarantine wording). Everything else: log server-side, generic 500 body.
> 1694	    const msg = beginErr.message ?? "";
> 1695	    console.error("[canvas-execute:spaces] begin failed:", msg);
> 1696	    if (msg.includes("Saldo mcoCoins insuficiente")) {
> 1697	      return spacesJson(402, { error: "insufficient_balance", message: "Saldo de mcoCoins insuficiente." }, corsHeaders);
> 1698	    }
> 1699	    if (msg.includes("Conta congelada")) {
> 1700	      return spacesJson(403, { error: "account_unavailable", message: "Conta indisponível para operações de débito." }, corsHeaders);
> 1701	    }
> 1702	    return spacesJson(500, { error: "begin_failed", message: "Falha ao iniciar a geração — nada foi cobrado." }, corsHeaders);
> 1703	  }
> 1704	  if (begun?.duplicate) {
> 1705	    // Idempotent replay (SOP S2): prior attempt already charged — return its state, ZERO second debit.
> 1706	    return spacesJson(200, {
> 1707	      execution_id: begun.generation_id,
> 1708	      status: begun.status,
> 1709	      duplicate: true,
> 1710	      credits_charged: 0,
> 1711	    }, corsHeaders);
> 1712	  }
> 1713	  const generationId = begun?.generation_id as string;
> 1714	
> 1715	  // ── Sync voice sub-path (Amendment 2c S26): debit done, tts-speak now, finalize in-request ──
> 1716	  if (body.node_type === "voice_over") {
> 1717	    return await executeSpacesVoice({
> 1718	      admin, body, corsHeaders,
> 1719	      creditCost: effectiveCost,
> 1720	      generationId,
> 1721	      supabaseUrl: ctx.supabaseUrl,
> 1722	      authHeader: ctx.authHeader,
> 1723	    });
> 1724	  }
> 1725	
> 1726	  // ── Async video sub-path (Amendment 2a S14): debit done, submit now, webhook finalizes ──
> 1727	  // Amendment 25: google/veo-* rides its own LRO submit (poll finalizes via veo-poll, not webhook).
> 1728	  if (body.node_type === "image_to_video" && body.provider === "google" && veoParams) {
> 1729	    // FR-SPACES-091: a fila INTEIRA de chaves do tenant (explícita → pool por prioridade → legada).
> 1730	    // O submit percorre a fila quando o provedor devolve 429 (crédito esgotado).
> 1731	    const candidates = await listProviderKeyCandidates(admin, user.id, "google", body.provider_key_id);
> 1732	    return await executeSpacesVeoVideo({
> 1733	      admin, body, candidates, corsHeaders,
> 1734	      creditCost: effectiveCost,
> 1735	      generationId,
> 1736	      veo: veoParams,
> 1737	    });
> 1738	  }
> 1739	  if (body.node_type === "image_to_video") {
> 1740	    return await executeSpacesVideo({
> 1741	      admin, body, keys, corsHeaders,
> 1742	      creditCost: effectiveCost,
> 1743	      generationId,
> 1744	      supabaseUrl: ctx.supabaseUrl,
> 1745	    });
> 1746	  }
> 1747	
> 1748	  // ── Provider call — 1 retry, fixed 5s backoff (BoK 07:155) ──
> 1749	  let outputUrl = "", outputB64 = "", enhancedPrompt = "", provErr = "";
> ```

## 🤖 Claude *(00:22:01)*

<details>
<summary>💭 Thinking Process</summary>

I'm seeing that both `generate_image` and `image_to_video` use the ledger-first approach requiring a node_run_id, but they handle responses differently—`generate_image` returns synchronously with execution details and a done status, while the Google Veo video endpoint submits a long-running operation and responds with a 202 status code.

For the Veo parameters, the server parses duration, resolution, aspect ratio, and audio settings from the request body into the veoParams shape it needs. The reference handling differs based on mode: presenter mode uses `reference_image_urls` while b-roll mode uses `input_asset_url` as the first frame, with a recent update clamping references to 8 seconds. The A1 witness execution at 267 mco confirms the presenter reference mode works with 8-second duration, but the account balance discrepancy is puzzling — if that execution actually ran, the balance should be lower than the current 9733, unless there was a refund applied or it's a different project entirely. The task state mentions both the successful A1 run and separate refunds from the discovery phase, so I need to reconcile which balance snapshot I'm looking at.

Rather than chase down every detail, I should just build the runner and test it against the simplest case first — the 6-voice narration — to verify the presenter path works end-to-end in practice. Checking the field names for reference images and first frame handling...

</details>


## 🤖 Claude *(00:22:03)*

Contrato 100% mapeado. Ambos `generate_image` e `image_to_video` (google) usam a branch ledger-first (precisam `node_run_id`); Veo retorna 202→poll `veo-poll`. Voz vai por `generate-voice`. Última verificação material: reconciliar a testemunha A1 `e20bbae2` (o saldo cheio 9733 sugere que foi refundada ou é de outro lugar) + confirmar os nomes de campo de refs/firstFrame no path Veo.

## 🤖 Claude *(00:22:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/a1.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst U0='ada39fae-67e1-4e53-af1c-5a18e1c108e8';\nconst { data: cols } = await admin.from('generations').select('*').limit(1);\nif(cols&&cols[0]) console.log('generations COLUMNS:', Object.keys(cols[0]).join(', '));\n// recent generations for U0\nconst { data: g } = await admin.from('generations').select('*').eq('owner_id',U0).order('created_at',{ascending:false}).limit(6);\nconsole.log('\\n=== recent generations (U0) ===');\nfor(const r of g??[] as any[]) console.log('  '+String(r.id).slice(0,8)+' node='+String(r.node_id||'').padEnd(12)+' st='+String(r.status).padEnd(10)+' charged='+r.mco_charged+' proj='+String(r.project_id||'').slice(0,8)+' '+r.created_at);\nEOF\nbun run /tmp/a1.ts 2>&1 | head -30",
  "description": "Reconcile A1 witness + generations schema"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> generations COLUMNS: id, owner_id, space_id, node_id, node_run_id, output_type, asset_id, model_key, mco_charged, mco_refunded, usd_cost, latency_ms, result, status, created_at, updated_at, webhook_token_hash, operation_id, project_id
> 
> === recent generations (U0) ===
>   e20bbae2 node=n_a1open     st=done       charged=267 proj=97012f0d 2026-08-02T20:09:01.854004+00:00
>   27231519 node=n_a1open     st=error      charged=167 proj=97012f0d 2026-08-02T20:07:24.516642+00:00
>   256b8876 node=n_a1open     st=error      charged=167 proj=97012f0d 2026-08-02T19:59:46.138334+00:00
>   d47fb25d node=n_povreact   st=done       charged=5 proj=024e1c03 2026-08-02T15:48:25.688661+00:00
>   fa4eb535 node=n_povreact   st=done       charged=267 proj=024e1c03 2026-08-02T15:44:18.570165+00:00
>   42e12bec node=n_povreact   st=done       charged=5 proj=024e1c03 2026-08-02T15:40:50.815566+00:00
> ```

## 🤖 Claude *(00:22:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"reference_image_urls|input_asset_url|first_frame|firstFrame|referenceType|referenceImages|reference_type|useFirstFrame|veo_refs_require_8s|allowedDurations|veoAllowedDurations\" supabase/functions/canvas-execute/index.ts | head -30",
  "description": "Veo refs/firstFrame field names"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 65:// · referenceImages ≤ 3 {image:{bytesBase64Encoded,mimeType}, referenceType:"asset"}.
> 144:  input_asset_url?: string;
> 152:  reference_image_urls?: string[];
> 330:    } else if (body.input_asset_url) {
> 334:        .eq("public_url", body.input_asset_url)
> 873:        image_url: o.body.input_asset_url,
> 1080:  // Identity references (FR-SPACES-087): up to 3 upstream images become referenceImages[asset].
> 1081:  // input_asset_url, when present, is the i2v FIRST FRAME (instances[0].image) — a distinct field.
> 1082:  const refUrls = [...new Set((body.reference_image_urls ?? []).filter(Boolean) as string[])]
> 1083:    .filter((u) => u !== body.input_asset_url)
> 1085:  const referenceImages: Array<{ image: { bytesBase64Encoded: string; mimeType: string }; referenceType: string }> = [];
> 1088:    if (img) referenceImages.push({ image: img, referenceType: "asset" });
> 1090:  const firstFrame = body.input_asset_url ? await fetchVeoImage(body.input_asset_url) : null;
> 1092:  // Veo 3.1 FORBIDS combining a first-frame image with identity referenceImages ("Image and reference images
> 1094:  // input_asset_url is only sent when the node opts into first-frame (veoUseFirstFrame), so first-frame wins and
> 1097:  const effectiveRefs = firstFrame ? [] : referenceImages;
> 1099:  if (firstFrame) instance.image = firstFrame;
> 1100:  else if (effectiveRefs.length > 0) instance.referenceImages = effectiveRefs;
> 1114:    parameters.personGeneration = (effectiveRefs.length > 0 || firstFrame) ? "allow_adult" : "allow_all";
> 1223:      has_first_frame: !!firstFrame,
> 1368:      // rejects any duration != 8s when instance.referenceImages is populated (and
> 1371:      const hasRefs = !body.input_asset_url && (body.reference_image_urls ?? [])
> 1375:          error: "veo_refs_require_8s",
> 1398:      if (!body.input_asset_url) {
> 1401:          message: "Conecte uma imagem upstream antes de gerar vídeo (input_asset_url).",
> 1464:    // coalesce them with reference_image_urls so handle-connected images actually reach the engine.
> 1467:        ...(body.reference_image_urls ?? [])].filter(Boolean) as string[],
> 1520:    upscaleImage = body.input_asset_url || (body.reference_image_urls ?? []).filter(Boolean)[0] || "";
> 1534:    if (!(body.input_asset_url || (body.reference_image_urls ?? []).some(Boolean))) {
> 1777:          reference_image_urls: composeRefs.slice(0, 2),
> ```

## 🤖 Claude *(00:23:05)*

<details>
<summary>💭 Thinking Process</summary>

The A1 reconciliation is now complete—the node `e20bbae2` is confirmed as done with a charge of 267 against project `97012f0d`, while the two earlier errors on the same node each had a charge of 167, which traces back to the clamp bug that extended the duration from 5 to 422. The A1 witness run confirmed the presenter reference path works end-to-end, which validates part of R5, though the full gate still needs cena 1's specific prompt and Vision QA on lip-sync. For the EP05 project, I'll run the fresh n_p_1 with the real cena 1 prompt. I'm also confirming the Veo field names: `reference_image_urls` handles identity references (max 3) for presenter mode, while `input_asset_url` provides the first frame for b-roll mode, with the server enforcing an XOR constraint where first frame presence drops references. There's also a duration clamp that requires 8-second videos when using references, which I need to verify against my presenter's duration.

Now I'm building the runner script that will mint a User 0 JWT and then iterate through each node ID to determine its kind and construct the appropriate payload—for image generation, that means setting up the canvas-execute call with the Gemini 2.5 Flash Image model and the necessary prompt parameters.

For the image-to-video step, I need to handle two modes: if it's using the first frame, I resolve the upstream image from the b-roll node's output and re-sign it; if it's a character reference, I pull the image URLs from the character asset and re-sign those fresh. Then I build the video payload with the Veo 3.1 Fast model, duration, and resolution parameters.

After invoking, I get back a 202 with an execution ID, then poll the veo-poll endpoint every 6 seconds until the generation completes, reporting back the video URL and asset details.

For voice cloning, I'm calling the generate-voice endpoint with the voice profile, script from the node prompt, language set to Portuguese, and the Qwen3 local provider, which returns a render ID that I poll until completion, then report the storage key and creative asset ID.

The question is whether I should update the node's status and output in the graph after each step, since normally the client handles that.

I realize the runner needs to persist the output to the node so the UI reflects the results and downstream nodes like b-roll can access the generated content. While canvas-execute already registers the asset and generation, the graph node's output field won't auto-update on the client side. I'm chaining the operations in the runner and getting the output URL directly from the canvas-execute response, so technically I don't need to persist to the graph for the runner's own chaining. But persisting node.data.output and status="success" back to the database is valuable for the UI to display results and for running remaining nodes and assembly later, so I'll write back to the graph to keep the project consistent.

When the Sovereign opens the project, they should see the generated segments rather than empty nodes, and the assembly step needs to pull them. So I'll persist node.data updates with status, imageUrl/videoUrl, assetId, and generatedAt after each successful run. I'll read-modify-write the whole graph, update the specific node's data, and write back — concurrency isn't an issue since I'm the only writer right now.

For the witnesses gate order, I'm planning to run the voice generation first. At ~27 seconds per act across 6 acts, that's roughly 160 seconds of total audio, which means about 16 minutes in the queue given the RTF of 6 — and expressive mode will be even slower. I should submit all 6 and poll them, but first I need to verify the voice-bridge worker is actually running as a systemd service, otherwise the jobs will just queue indefinitely. Let me also check what services are available — veo-poll is an edge function rather than a worker, and veo submission happens through canvas-execute. Writing the runner script...

</details>


## 🤖 Claude *(00:23:10)*

Tudo reconciliado e confirmado (Lei 1):
- **A1 `e20bbae2`**: `done · 267 mco` num projeto scratch `97012f0d` (não no EP05) — **o path apresentador com refs está PROVADO E2E**. Os 2 erros de 167 mco anteriores = a descoberta do bug do clamp (dur=5→422), refundados.
- **Campos Veo confirmados:** `reference_image_urls` (refs identidade, presenter) XOR `input_asset_url` (firstFrame, b-roll). Clamp refs→8s: presenter dur=8+refs ✅; b-roll firstFrame dur=4 → clamp N/A ✅.

Vou montar o runner. Antes, o path de voz depende do worker host `voice-bridge`; deixa eu confirmar que está ativo + pegar o helper de invoke exato.

## 🤖 Claude *(00:23:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "systemctl --user is-active voice-bridge.service video-bridge.service 2>&1; echo \"---status voice---\"; systemctl --user status voice-bridge.service --no-pager 2>&1 | head -6",
  "description": "Check host worker services"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> active
> active
> ---status voice---
> ● voice-bridge.service - MCORCH Qwen3-TTS Voice Bridge (polls video_renders engine=qwen3-voice, clones/synthesizes via the free self-host engine)
>      Loaded: loaded (/home/ubuntu/.config/systemd/user/voice-bridge.service; enabled; preset: enabled)
>      Active: active (running) since Thu 2026-07-30 20:39:25 -03; 3 days ago
>    Main PID: 498936 (bun)
>       Tasks: 9 (limit: 28691)
>      Memory: 1.6G (peak: 3.2G)
> ```

## 🤖 Claude *(00:23:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '20,55p' scripts/qa/smoke-spaces-execution.ts",
  "description": "invokeFn header pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> const ANON = (process.env.SB_PUBLISHABLE_KEY ?? process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY)!;
> if (!URL || !SVC || !ANON) { console.error('missing env (SUPABASE_URL / SB_SECRET_KEY / publishable)'); process.exit(1); }
> 
> const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> const FN = `${URL}/functions/v1/canvas-execute`;
> 
> let pass = 0, fail = 0;
> function gate(name: string, ok: boolean, detail = '') {
>   if (ok) { pass++; console.log(`✅ ${name}${detail ? ` — ${detail}` : ''}`); }
>   else { fail++; console.error(`❌ ${name}${detail ? ` — ${detail}` : ''}`); }
> }
> 
> async function invokeFn(jwt: string | null, body: Record<string, unknown>) {
>   const headers: Record<string, string> = { 'Content-Type': 'application/json', apikey: ANON };
>   if (jwt) headers.Authorization = `Bearer ${jwt}`;
>   const res = await fetch(FN, { method: 'POST', headers, body: JSON.stringify(body) });
>   let json: Record<string, unknown> = {};
>   try { json = await res.json(); } catch { /* empty body */ }
>   return { status: res.status, json };
> }
> 
> async function balance(uid: string): Promise<number> {
>   const { data } = await admin.from('profiles').select('mco_balance').eq('id', uid).single();
>   return Number(data?.mco_balance ?? 0);
> }
> 
> const spacePayload = (spaceId: string, extra: Record<string, unknown> = {}) => ({
>   project_id: spaceId, node_id: 'n_smoke', node_type: 'generate_image',
>   provider: 'openrouter', model: 'google/gemini-2.5-flash-image',
>   prompt: 'um cubo azul minimalista', parameters: {},
>   space_id: spaceId, node_run_id: crypto.randomUUID(), ...extra,
> });
> 
> let uidA: string | null = null, uidB: string | null = null;
> ```

## 🤖 Claude *(00:23:50)*

<details>
<summary>💭 Thinking Process</summary>

Both the voice-bridge and video-bridge workers are running, and I'm noticing the request headers include Content-Type, an anonymous API key, and a JWT bearer token. The smoke test payload is interesting because it sets both `project_id` and `space_id` to the same value, but the canvas-execute ledger branch validates ownership using `space_id` while the smoke test references the spaces table instead.

This is a key distinction — the smoke T4 tests validate against the `spaces` table, but our EP05 project lives in `vm_canvas_projects`. So there might be two separate execution paths: one for the spaces ledger branch that checks `space_id` against the spaces table, and another legacy path for vm_canvas that validates `project_id` against vm_canvas_projects. The A1 witness ran in project `97012f0d` which is also in vm_canvas_projects, but I need to check whether the generations row for e20bbae2 has `space_id` or `project_id` populated to understand which branch it's actually using.

Looking at the data, the generations table has both columns. The A1 query showed `project_id = 97012f0d` for e20bbae2, which is in vm_canvas_projects, so the Veo ledger path clearly works with vm_canvas_projects projects. The real question is what validation canvas-execute actually performs — whether it needs `space_id` from the spaces table or if it accepts `project_id` from vm_canvas_projects. The A1 payload must have sent `project_id = 97012f0d`, so I need to trace how the client builds that payload in useCanvasPipeline's runSingleNode to see what it's actually sending.

The smoke test sets both `project_id` and `space_id` to the same spaces-table ID, which suggests canvas-execute might validate against spaces when space_id is present, or against vm_canvas_projects when only project_id is provided. The safest approach would be to mirror whatever validation logic already works. The A1 witness proves the contract works: the client sends `project_id` from `vm_canvas_projects` with no `space_id`, and that payload succeeds. I'll match the client's exact `runSingleNode` structure—it passes `project_id`, `node_id`, and the payload parameters, then `executeNode.mutateAsync` adds the `node_run_id` via the ledger flow. The mutation just needs to forward those params as-is. I need to verify whether the client actually sends space_id for Spaces projects or just project_id. A1 succeeded with only project_id in the vm_canvas_projects route, but EP05 is also vm_canvas_projects yet accessed through `/dashboard/spaces/18a21002` — so there might be two different code paths depending on whether it's a Canvas Studio or Spaces project.

Let me check the canvas-execute logic around the node_type gate and ownership validation to see how it distinguishes between the spaces branch and legacy path, and confirm the project validation works correctly.

</details>


## 🤖 Claude *(00:23:53)*

Ambos workers **ativos** (voice-bridge 3 dias, video-bridge). Header: `{apikey: ANON, Authorization: Bearer <jwt>}`. Uma última verificação crítica antes de gastar: como o `canvas-execute` valida a posse do projeto no ledger branch (o A1 rodou em `vm_canvas_projects` sem `space_id` — preciso confirmar o contrato de posse pra não tomar 404 e desperdiçar tentativas).

## 🤖 Claude *(00:23:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts",
  "offset": 1300,
  "limit": 30
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1300	    body,
> 1301	    webhookUrl,
> 1302	  });
> 1303	  if (!submit.ok) {
> 1304	    // Defense-in-depth (security-review INFO): the provider error text may echo the request URL,
> 1305	    // which carries the plaintext token — never persist it (the row is owner-readable).
> 1306	    const safeMsg = submit.message.split(token).join("[redacted]");
> 1307	    return await refundNow(safeMsg, 502, "video_submit_failed");
> 1308	  }
> 1309	
> 1310	  await admin.from("generations").update({ operation_id: submit.operationId }).eq("id", generationId);
> 1311	
> 1312	  return spacesJson(202, {
> 1313	    execution_id: generationId,
> 1314	    status: "queued",
> 1315	    operation_id: submit.operationId,
> 1316	    credits_charged: creditCost, // ledger-first: already debited (S14)
> 1317	  }, corsHeaders);
> 1318	}
> 1319	
> 1320	async function executeSpacesNode(ctx: SpacesExecCtx): Promise<Response> {
> 1321	  const { admin, user, body, keys, creditCost, corsHeaders } = ctx;
> 1322	  const t0 = Date.now();
> 1323	
> 1324	  // ── Slice gate (SOP S7 + Amendments 2a/it.2a): image, prompt, async video, voice, compose, style ──
> 1325	  if (
> 1326	    body.node_type !== "generate_image" && body.node_type !== "magic_prompt" &&
> 1327	    body.node_type !== "image_to_video" && body.node_type !== "voice_over" &&
> 1328	    body.node_type !== "scene_compose" && body.node_type !== "style_transfer" &&
> 1329	    body.node_type !== "upscale"
> ```

## 🤖 Claude *(00:23:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"from\\(['\\\"](spaces|vm_canvas_projects)['\\\"]|begin_space_generation|space_id|project_id|owner|\\.eq\\(['\\\"]id\" supabase/functions/canvas-execute/index.ts | sed -n '1,40p'",
  "description": "Ownership validation in canvas-execute"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 136:  project_id: string;
> 156:  space_id?: string;
> 158:  // Amendment 20 (FR-SPACES-072): qual chave do pool BYOK usar (uuid de user_provider_keys, owner-validado).
> 207:    if (!body.project_id || !body.node_id || (!body.prompt && !promptOptional)) {
> 208:      return new Response(JSON.stringify({ error: "project_id, node_id, and prompt are required" }), {
> 223:    // provider_key_id (owner-validated) → pool priority → legacy user_api_keys.google_api_key → "".
> 266:    // it.2a (FR-SPACES-024): node_run_id is the ledger marker; the surface is space_id (v1) OR
> 267:    // project_id (consolidated vm_canvas_projects surface). Legacy callers never send node_run_id.
> 268:    if ((body.space_id || body.project_id) && body.node_run_id) {
> 274:      .from("profiles").select("mco_balance").eq("id", user.id).single();
> 349:        project_id: body.project_id,
> 384:        if (body.project_id) {
> 386:            .from("vm_canvas_projects")
> 388:            .eq("id", body.project_id)
> 408:                .eq("id", campaignId)
> 440:          .eq("id", execution.id);
> 477:          .eq("id", execution.id);
> 597:          project_id: body.project_id,
> 649:      .eq("id", execution.id);
> 679:        .from("vm_canvas_projects")
> 683:            .eq("project_id", body.project_id)
> 687:        .eq("id", body.project_id);
> 989:  const fileName = `${body.space_id ?? body.project_id}/${body.node_run_id}.wav`;
> 1137:      const project = (candidate.metadata?.vertex_project as string) || sa.project_id || "";
> 1139:      // Anti-SSRF (review 2026-07-15): project/location vêm de metadata owner-writable e caem no HOST
> 1225:  }).eq("id", generationId);
> 1254: *  Mints the webhook token (row stores ONLY the SHA-256 — the owner-readable row must never
> 1291:    .eq("id", generationId);
> 1305:    // which carries the plaintext token — never persist it (the row is owner-readable).
> 1310:  await admin.from("generations").update({ operation_id: submit.operationId }).eq("id", generationId);
> 1570:  // space_id takes precedence — the v1 wire shape mirrors the space id into the legacy-required
> 1571:  // project_id field. Composite tenant FKs in `generations` are the schema-level backstop.
> 1572:  if (body.space_id) {
> 1574:      .from("spaces").select("id").eq("id", body.space_id).eq("owner_id", user.id).maybeSingle();
> 1580:      .from("vm_canvas_projects").select("id").eq("id", body.project_id).eq("user_id", user.id).maybeSingle();
> 1586:  // Per-user BYOK fail-closed (API Tenancy Model), AFTER the ownership 404 so the canonical
> 1646:  // These mirror the legacy pre-checks; begin_space_generation stays the race-safe authority.
> 1648:    .from("profiles").select("mco_balance").eq("id", user.id).single();
> 1677:  const { data: begun, error: beginErr } = await admin.rpc("begin_space_generation", {
> 1678:    p_owner_id: user.id,
> ```

## 🤖 Claude *(00:24:26)*

<details>
<summary>💭 Thinking Process</summary>

I'm confirming the ledger branch logic: it's triggered when both a space or project ID and a node run ID are present. The ownership validation then checks the spaces table if a space ID exists, otherwise it validates against the vm_canvas_projects table using the user ID—so for the EP05 project, it would validate through the projects table.

Now I'm building the runner script that will handle node execution: it takes node IDs as arguments, mints a JWT for the account, loads the project graph, and dispatches each node based on its kind while polling for results and persisting updates back to the graph. I'll implement careful sequential updates to avoid conflicts, and for voice nodes I'll submit all requests first, collect the render IDs, then poll each one. I'm also adding a dry-run flag to preview payloads before actually invoking them.

For handling b-roll dependencies on upstream images, I'll run the nano node first and persist its output to the graph, then when running b-roll I'll resolve the upstream image by finding the source node's output URL and re-signing it through the admin storage API to match how the client handles it.

For the charRef presenter image, I need to extract the storage path from the existing signed URL (parsing out the path segment before the token query parameter) and then create a fresh signed URL via admin.storage to ensure it's valid for the b-roll execution.

Now I'm ready to build the runner itself. I'll use the fresh output_url directly from canvas-execute for the nano output since it's just been generated, and re-sign the charRef image path for safety. Let me also verify that generate_image is truly synchronous — looking at the finalize step, it returns output_url in the response, and since the provider call runs inline before finalization, the response includes the signed URL immediately.

For the runner, I'll accept explicit node IDs as arguments with an optional `--kind-hint` flag to auto-detect the operation type from the graph, and a `--persist` flag defaulting to true. Let me write it out with clear logging and per-node result tracking.

Writing the runner...

</details>


## 🤖 Claude *(00:24:28)*

**Contrato 100% confirmado** (linhas 268, 1572-1584): ledger branch entra com `project_id + node_run_id`; sem `space_id`, valida posse contra `vm_canvas_projects.user_id`. Exatamente como o A1 rodou. Tenho tudo para o runner sem risco de 404/tentativa desperdiçada.

Vou construir o runner (3 caminhos: canvas-execute sync p/ imagem, canvas-execute+veo-poll p/ vídeo, generate-voice+poll p/ voz), com persistência do output no grafo e um `--dry` para sanidade antes de gastar.

## 🤖 Claude *(00:25:19)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts",
  "content": "/**\n * EP05 v2 node runner \u2014 drives canvas-execute / generate-voice with User 0's JWT, mirroring the exact\n * client dispatch (useCanvasPipeline.runSingleNode + resolveExecutePayload + useAvatarVoice).\n *\n * Usage:\n *   bun run ep05-run.ts --dry n_bimg_2                # print payload, DO NOT spend\n *   bun run ep05-run.ts n_bimg_2 n_bvid_2            # run nano then b-roll (chained firstFrame)\n *   bun run ep05-run.ts n_p_1                         # presenter (reference mode)\n *   bun run ep05-run.ts --voices n_voice_ato1 ...     # voiceClone via generate-voice\n *\n * Persists node.data {status, output} back to vm_canvas_projects.graph after each success.\n */\nimport { createClient } from '@supabase/supabase-js';\n\nconst URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;\nconst SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;\nconst ANON = (process.env.SB_PUBLISHABLE_KEY ?? process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY)!;\nconst admin = createClient(URL, SVC, { auth: { persistSession: false } });\n\nconst PID = '18a21002-df9c-48b4-aff3-7aba28e812e7';\nconst U0_EMAIL = 'gabrielcall@gmail.com';\nconst U0 = 'ada39fae-67e1-4e53-af1c-5a18e1c108e8';\nconst VOICE_PROFILE = 'c4d72b8f-9acb-4832-987c-37093a0b91e1'; // qwen3-local pt-BR, last used 2026-07-30 (canonical Gabriel AI voice)\nconst CHARREF_ID = 'n_d3jbjjjg';\n\nconst args = process.argv.slice(2);\nconst DRY = args.includes('--dry');\nconst VOICES = args.includes('--voices');\nconst nodeIds = args.filter(a => !a.startsWith('--'));\n\n// \u2500\u2500 JWT mint (generateLink \u2192 verifyOtp), mirrors gen-user-jwt.ts \u2500\u2500\nasync function mintJwt(): Promise<string> {\n  const anon = createClient(URL, ANON, { auth: { persistSession: false } });\n  const { data, error } = await admin.auth.admin.generateLink({ type: 'magiclink', email: U0_EMAIL });\n  if (error || !data.properties?.hashed_token) throw new Error('generateLink: ' + (error?.message ?? 'no hash'));\n  for (const type of ['magiclink', 'email'] as const) {\n    const { data: sess } = await anon.auth.verifyOtp({ token_hash: data.properties.hashed_token, type });\n    if (sess?.session?.access_token) return sess.session.access_token;\n  }\n  throw new Error('verifyOtp failed');\n}\n\nasync function invoke(fn: string, jwt: string, body: Record<string, unknown>) {\n  const res = await fetch(`${URL}/functions/v1/${fn}`, {\n    method: 'POST',\n    headers: { 'Content-Type': 'application/json', apikey: ANON, Authorization: `Bearer ${jwt}` },\n    body: JSON.stringify(body),\n  });\n  let json: any = {};\n  try { json = await res.json(); } catch {}\n  return { status: res.status, json };\n}\n\nasync function loadGraph() {\n  const { data } = await admin.from('vm_canvas_projects').select('graph').eq('id', PID).single();\n  return (data as any).graph as { nodes: any[]; edges: any[]; lanes?: any[] };\n}\n\nasync function persistNode(nodeId: string, patch: Record<string, unknown>) {\n  const g = await loadGraph();\n  const n = g.nodes.find((x: any) => x.id === nodeId);\n  if (!n) return;\n  n.data = { ...n.data, ...patch };\n  await admin.from('vm_canvas_projects').update({ graph: g, updated_at: new Date().toISOString() }).eq('id', PID);\n}\n\n// Re-sign a canvas-assets object to a fresh signed URL the server can download.\nasync function freshSign(signedOrPath: string): Promise<string> {\n  // extract the storage path after \"/object/sign/canvas-assets/\" and before \"?\"\n  const m = signedOrPath.match(/\\/object\\/(?:sign|public)\\/canvas-assets\\/([^?]+)/);\n  const path = m ? decodeURIComponent(m[1]) : signedOrPath;\n  const { data, error } = await admin.storage.from('canvas-assets').createSignedUrl(path, 3600);\n  if (error || !data) { console.warn('  \u26a0\ufe0f re-sign failed, using original:', error?.message); return signedOrPath; }\n  return data.signedUrl;\n}\n\nasync function balance(): Promise<number> {\n  const { data } = await admin.from('profiles').select('mco_balance').eq('id', U0).single();\n  return Number((data as any)?.mco_balance ?? 0);\n}\n\n// \u2500\u2500 payload builders (mirror resolveExecutePayload) \u2500\u2500\nfunction imagePayload(n: any) {\n  const d = n.data;\n  return {\n    project_id: PID, node_id: n.id,\n    node_type: 'generate_image', provider: 'openrouter', model: 'google/gemini-2.5-flash-image',\n    prompt: d.prompt,\n    negative_prompt: d.negativePrompt || undefined,\n    parameters: { aspect_ratio: d.aspectRatio ?? '16:9', controls: d.controls, seed: (d.fixedSeed && d.seed != null) ? d.seed : undefined },\n    node_run_id: crypto.randomUUID(),\n  };\n}\nfunction videoPayload(n: any, extra: Record<string, unknown>) {\n  const d = n.data;\n  return {\n    project_id: PID, node_id: n.id,\n    node_type: 'image_to_video', provider: 'google', model: d.videoModel ?? 'veo-3.1-fast',\n    prompt: d.prompt,\n    parameters: {\n      duration: d.veoDuration ?? 8,\n      resolution: d.veoResolution ?? '720p',\n      aspect_ratio: d.aspectRatio === '16:9' ? '16:9' : '9:16',\n      generate_audio: d.veoGenerateAudio ?? false,\n      async_only: true,\n    },\n    node_run_id: crypto.randomUUID(),\n    ...extra,\n  };\n}\n\nasync function pollVeo(jwt: string, genId: string, label: string) {\n  for (let i = 0; i < 60; i++) {\n    await new Promise(r => setTimeout(r, 6000));\n    const { status, json } = await invoke('veo-poll', jwt, { generation_id: genId });\n    const st = json?.status;\n    process.stdout.write(`\\r  [${label}] poll ${i + 1} \u2192 status=${st} ${json?.bytes ? '(' + json.bytes + 'B)' : ''}     `);\n    if (st === 'done') { console.log(''); return json; }\n    if (st === 'error') { console.log(''); return json; }\n  }\n  console.log('');\n  return { status: 'timeout' };\n}\n\nasync function pollVoice(renderId: string, label: string) {\n  for (let i = 0; i < 120; i++) {\n    await new Promise(r => setTimeout(r, 5000));\n    const { data } = await admin.from('video_renders').select('id, state, storage_key, qa').eq('id', renderId).maybeSingle();\n    const st = (data as any)?.state;\n    process.stdout.write(`\\r  [${label}] poll ${i + 1} \u2192 state=${st}          `);\n    if (st && ['done', 'failed', 'qa_failed'].includes(st)) { console.log(''); return data as any; }\n  }\n  console.log('');\n  return { state: 'timeout' };\n}\n\n// \u2500\u2500 main \u2500\u2500\nconst jwt = await mintJwt();\nconsole.log('JWT minted for', U0_EMAIL, '\u00b7 balance before:', await balance(), 'mco');\nconst g = await loadGraph();\nconst byId = (id: string) => g.nodes.find((n: any) => n.id === id);\n\nif (VOICES) {\n  // submit all, then poll\n  const submitted: { nodeId: string; renderId: string }[] = [];\n  for (const id of nodeIds) {\n    const n = byId(id);\n    if (!n) { console.error('  node not found', id); continue; }\n    const body = { action: 'synthesize', voice_profile_id: VOICE_PROFILE, script: n.data.prompt, language: n.data.language ?? 'pt-BR', provider: 'qwen3-local', project_id: PID, node_id: id };\n    if (DRY) { console.log('DRY voice', id, JSON.stringify(body).slice(0, 200)); continue; }\n    const { status, json } = await invoke('generate-voice', jwt, body);\n    console.log(`  submit ${id} \u2192 ${status} render_id=${json?.render_id} mco=${json?.mco_charged}`);\n    if (json?.render_id) { submitted.push({ nodeId: id, renderId: json.render_id }); await persistNode(id, { status: 'queued', pendingRenderId: json.render_id }); }\n  }\n  for (const s of submitted) {\n    const r = await pollVoice(s.renderId, s.nodeId);\n    if (r.state === 'done') {\n      const assetId = r.qa?.creative_asset_id;\n      await persistNode(s.nodeId, { status: 'success', pendingRenderId: undefined, output: { audioStorageKey: r.storage_key, creativeAssetId: assetId, generatedAt: new Date().toISOString() } });\n      console.log(`  \u2705 ${s.nodeId} done \u00b7 key=${r.storage_key} \u00b7 asset=${assetId}`);\n    } else {\n      await persistNode(s.nodeId, { status: 'failed', error: r.qa?.error ?? r.state });\n      console.log(`  \u274c ${s.nodeId} ${r.state} \u00b7 ${r.qa?.error ?? ''}`);\n    }\n  }\n  console.log('balance after:', await balance(), 'mco');\n  process.exit(0);\n}\n\nfor (const id of nodeIds) {\n  const n = byId(id);\n  if (!n) { console.error('node not found', id); continue; }\n  const kind = n.data.kind;\n  console.log(`\\n\u25b6 ${id} (${kind}) \u2014 ${n.data.label}`);\n\n  if (kind === 'generateImage') {\n    const body = imagePayload(n);\n    if (DRY) { console.log('  DRY:', JSON.stringify(body).slice(0, 300)); continue; }\n    const { status, json } = await invoke('canvas-execute', jwt, body);\n    if (json?.output_url) {\n      await persistNode(id, { status: 'success', output: { imageUrl: json.output_url, assetId: json.asset_id, generatedAt: new Date().toISOString() } });\n      console.log(`  \u2705 ${status} output_url=${String(json.output_url).slice(0, 80)}... charged=${json.credits_charged ?? '?'}`);\n    } else {\n      console.log(`  \u274c ${status}`, JSON.stringify(json).slice(0, 300));\n    }\n  } else if (kind === 'imageToVideo') {\n    const d = n.data;\n    let extra: Record<string, unknown> = {};\n    if (d.veoUseFirstFrame === true) {\n      // firstFrame: resolve upstream image from edge source's persisted output\n      const inEdge = g.edges.find((e: any) => e.target === id && (e.targetHandle === 'input_image' || !e.targetHandle));\n      const src = inEdge ? byId(inEdge.source) : null;\n      const upUrl = src?.data?.output?.imageUrl;\n      if (!upUrl) { console.log('  \u274c no upstream firstFrame image on', inEdge?.source, '- run it first'); continue; }\n      extra = { input_asset_url: await freshSign(upUrl) };\n    } else {\n      // reference mode: charRef identity\n      const refId = d.characterRefId ?? CHARREF_ID;\n      const ref = byId(refId);\n      const refUrl = ref?.data?.imageUrls?.[0] ?? ref?.data?.imageUrl;\n      if (!refUrl) { console.log('  \u274c no charRef image on', refId); continue; }\n      extra = { reference_image_urls: [await freshSign(refUrl)] };\n    }\n    const body = videoPayload(n, extra);\n    if (DRY) { console.log('  DRY:', JSON.stringify({ ...body, prompt: body.prompt.slice(0, 60) + '\u2026' }).slice(0, 400)); continue; }\n    const balBefore = await balance();\n    const { status, json } = await invoke('canvas-execute', jwt, body);\n    console.log(`  submit \u2192 ${status} execution_id=${json?.execution_id} charged=${json?.credits_charged}`);\n    if (!json?.execution_id) { console.log('  \u274c', JSON.stringify(json).slice(0, 300)); continue; }\n    const r = await pollVeo(jwt, json.execution_id, id);\n    if (r.status === 'done') {\n      await persistNode(id, { status: 'success', output: { videoUrl: r.video_url, assetId: r.asset_id, generatedAt: new Date().toISOString() } });\n      console.log(`  \u2705 done \u00b7 video=${String(r.video_url).slice(0, 70)}... asset=${r.asset_id} bytes=${r.bytes} \u00b7 net=${balBefore - await balance()} mco`);\n    } else {\n      console.log(`  \u274c ${r.status} \u00b7 refunded=${r.refunded} \u00b7 ${r.error ?? r.message ?? ''} \u00b7 net=${balBefore - await balance()} mco`);\n    }\n  } else {\n    console.log('  (skip \u2014 kind', kind, 'not handled here; voice uses --voices)');\n  }\n}\nconsole.log('\\nbalance after:', await balance(), 'mco');\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:25:25)*

Runner pronto. Vou fazer um **`--dry` sanity** dos 3 tipos de nó antes de gastar 1 mco (imprime o payload exato que iria pro servidor):

## 🤖 Claude *(00:25:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts --dry n_bimg_2 n_bvid_2 n_p_1 2>&1 | head -40",
  "description": "Dry-run payload sanity (no spend)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> JWT minted for gabrielcall@gmail.com · balance before: 9733 mco
> 
> ▶ n_bimg_2 (generateImage) — Cena 2 · Frame (Nano Banana)
>   DRY: {"project_id":"18a21002-df9c-48b4-aff3-7aba28e812e7","node_id":"n_bimg_2","node_type":"generate_image","provider":"openrouter","model":"google/gemini-2.5-flash-image","prompt":"Cinematic 16:9 first frame: A large computer monitor beside a creator's dim silhouette in a shadowed studio at night, the m
> 
> ▶ n_bvid_2 (imageToVideo) — Cena 2 · B-roll (Veo firstFrame 4s)
>   ❌ no upstream firstFrame image on n_bimg_2 - run it first
> 
> ▶ n_p_1 (imageToVideo) — Cena 1 · Apresentador
>   DRY: {"project_id":"18a21002-df9c-48b4-aff3-7aba28e812e7","node_id":"n_p_1","node_type":"image_to_video","provider":"google","model":"veo-3.1-fast","prompt":"Cinematic 8-second video of Gabriel AI (@Gabriel AI) in extr…","parameters":{"duration":8,"resolution":"720p","aspect_ratio":"16:9","generate_audio":false,"async_only":true},"node_run_id":"234f2a4c-96cf-44d5-94fe-7ecc37d5e82d","reference_image_url
> 
> balance after: 9733 mco
> ```

## 🤖 Claude *(00:26:15)*

<details>
<summary>💭 Thinking Process</summary>

The dry run validates that the image generation node has the right configuration and that the b-roll node correctly recognizes it needs the upstream image output before proceeding—this dependency chaining is working as intended, and once I run the image generation first in the actual execution, the b-roll node will have access to that output.

The presenter node also has the correct payload for video generation with the reference image. JWT is minted with a balance of 9733 and zero spend on the dry run, so everything checks out.

Now I'm executing the gated witnesses in order. Since the voice narrations are free but slow (around 15+ minutes for all six), I'll launch those as a background process so they can process while I run the paid witnesses in parallel. The G2 witness comes next with the image generation feeding into the b-roll node.

Actually, I'm hitting a race condition issue — both the voice runner and paid witnesses write to the graph concurrently, and if they interleave their read-modify-write cycles, one will clobber the other's updates. I could run voice first but that adds 15 minutes of wait time, or I could run the paid witnesses first (which should take around 5 minutes total) and let voice run afterward without the concurrency conflict. I'm settling on running paid witnesses first in the foreground since they're the priority and complete in ~5 minutes, then voice second—total ~20 minutes is acceptable and avoids any race conditions on graph writes. This is the simplest and safest approach for the critical payment path. Actually, I'm second-guessing the concurrency approach. Since voice is the free option and most likely to surface issues early, I should run it in the background first to catch problems quickly. I'll modify the runner to accept a `--no-persist` flag so voice can generate and capture render IDs without writing to the graph, then persist those results afterward. This eliminates the race condition entirely.

Wait, let me simplify—I'll just run the paid witnesses first in the foreground (about 5 minutes), then kick off voice in the background afterward. That way I can checkpoint the paid results with the Sovereign while voice finishes running, giving me the best of both worlds without blocking on the longer voice polling.

So the plan is: run nano, broll, and presenter together in one invocation to keep nano's output available for broll, then launch the voice nodes in the background once that completes. I'm reconsidering the timing — nano takes about 8 seconds, each veo poll generates output in 1-3 minutes, so the total should be around 5-6 minutes, which likely fits under the 10-minute timeout. But to be safe against any delays, I'll run it in the background and write to a log file so I can monitor progress without hitting the timeout limit.

</details>


## 🤖 Claude *(00:26:16)*

Dry-run **impecável** (Lei 1, zero gasto):
- `n_bimg_2`: payload correto (openrouter/gemini-image, 16:9)
- `n_bvid_2`: corretamente detecta que precisa do firstFrame upstream primeiro (encadeamento funcionando)
- `n_p_1`: image_to_video/google/veo-3.1-fast, **duration:8** (clamp refs→8s satisfeito), 16:9, generate_audio:false, reference_image_urls (charRef)

Vou executar as **testemunhas pagas gated** em background (nano→b-roll→apresentador, ~411 mco, sequencial para o encadeamento firstFrame funcionar):

## 🤖 Claude *(00:26:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && nohup bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts n_bimg_2 n_bvid_2 n_p_1 > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/witness-paid.log 2>&1 &\necho \"PID $!\"; sleep 25; echo \"--- log after 25s ---\"; cat /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/witness-paid.log",
  "description": "Run paid witnesses (background) + first peek"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> PID 1242609
> --- log after 25s ---
> JWT minted for gabrielcall@gmail.com · balance before: 9733 mco
> 
> ▶ n_bimg_2 (generateImage) — Cena 2 · Frame (Nano Banana)
>   ✅ 200 output_url=https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ad... charged=10
> 
> ▶ n_bvid_2 (imageToVideo) — Cena 2 · B-roll (Veo firstFrame 4s)
>   ❌ no upstream firstFrame image on n_bimg_2 - run it first
> 
> ▶ n_p_1 (imageToVideo) — Cena 1 · Apresentador
>   submit → 202 execution_id=b5443a05-cca8-494b-990c-b5c5e3d1ecdb charged=267
> 
  [n_p_1] poll 1 → status=running
> ```

## 🤖 Claude *(00:26:59)*

<details>
<summary>💭 Thinking Process</summary>

The nano image generation succeeded and produced output, but the b-roll step failed because it couldn't find the upstream image—even though it just ran. The problem is that the graph was loaded once at startup, so when the image generation completed and wrote its output, the b-roll step was still referencing the stale graph state from before that execution.

I need to fix the runner to refresh the graph from the database before resolving upstream dependencies, so downstream steps see the actual outputs. For now, I'll let the presenter finish its polling in the background, then re-run the b-roll once the runner is fixed.

</details>


## 🤖 Claude *(00:27:03)*

Dois resultados e um bug meu:
- ✅ **Nano `n_bimg_2` SUCCESS** (10 mco, output_url persistido no DB)
- ✅ **Apresentador `n_p_1` submetido** (202, exec `b5443a05`, 267 mco) — **polling running** (path apresentador funciona)
- ❌ **B-roll falhou por bug MEU** (não gastou nada): o runner carregou o grafo em memória UMA vez no início; o output do nano foi persistido no DB mas não no `g` em memória → o b-roll leu o nó stale. Zero mco desperdiçado (errou antes de invocar).

Vou deixar o apresentador terminar o poll, corrigir o runner (recarregar grafo fresco por nó), e re-rodar só o b-roll. Monitorando o apresentador:

## 🤖 Claude *(00:27:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sleep 90; tail -8 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/witness-paid.log",
  "description": "Wait + check presenter poll progress"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> <tool_use_error>Blocked: sleep 90 followed by: tail -8 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/witness-paid.log. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
> ```

## 🤖 Claude *(00:27:10)*

<details>
<summary>💭 Thinking Process</summary>

I need to handle the blocking foreground sleep differently—I'll set up an until-loop that monitors whether the background process is still running and checks the log for a terminal state, then display the results once it completes.

</details>


## 🤖 Claude *(00:27:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "until ! kill -0 1242609 2>/dev/null; do sleep 5; done; echo \"=== process done ===\"; cat /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/witness-paid.log",
  "description": "Wait for paid witness process, then show full log",
  "timeout": 420000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === process done ===
> JWT minted for gabrielcall@gmail.com · balance before: 9733 mco
> 
> ▶ n_bimg_2 (generateImage) — Cena 2 · Frame (Nano Banana)
>   ✅ 200 output_url=https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ad... charged=10
> 
> ▶ n_bvid_2 (imageToVideo) — Cena 2 · B-roll (Veo firstFrame 4s)
>   ❌ no upstream firstFrame image on n_bimg_2 - run it first
> 
> ▶ n_p_1 (imageToVideo) — Cena 1 · Apresentador
>   submit → 202 execution_id=b5443a05-cca8-494b-990c-b5c5e3d1ecdb charged=267
> 
  [n_p_1] poll 1 → status=running      
  [n_p_1] poll 2 → status=running      
  [n_p_1] poll 3 → status=running      
  [n_p_1] poll 4 → status=done (2269626B)     
>   ✅ done · video=https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas... asset=bdcee839-6d8c-49db-b56e-02ded1118c20 bytes=2269626 · net=267 mco
> 
> balance after: 9456 mco
> ```

## 🤖 Claude *(00:27:24)*

<details>
<summary>💭 Thinking Process</summary>

Looking at the asset processing status, I've got the nano and presenter elements completed, spending 277 mco total, while the B-roll hit a runner bug that needs fixing. I'm about to address that issue and re-run the B-roll task.

The problem is in how the graph gets loaded—it's being cached once at the start instead of refreshing for each node. I need to make the graph variable mutable and reload it at the beginning of each iteration in the paid assets loop, so the `byId` closure picks up the fresh graph state each time.

</details>


## 🤖 Claude *(00:27:27)*

Testemunhas pagas parciais:
- ✅ **Nano `n_bimg_2`**: 10 mco
- ✅ **Apresentador `n_p_1`**: done, vídeo 2,27MB, asset `bdcee839`, 267 mco (path apresentador+refs+clamp 8s **provado E2E no projeto EP05**)
- ❌ **B-roll**: bug meu (grafo em memória stale), zero gasto
- **Saldo: 9733 → 9456** (277 gastos)

Vou corrigir o runner (recarregar grafo fresco por nó) e re-rodar só o b-roll:

## 🤖 Claude *(00:27:30)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts",
  "old_string": "const jwt = await mintJwt();\nconsole.log('JWT minted for', U0_EMAIL, '\u00b7 balance before:', await balance(), 'mco');\nconst g = await loadGraph();\nconst byId = (id: string) => g.nodes.find((n: any) => n.id === id);",
  "new_string": "const jwt = await mintJwt();\nconsole.log('JWT minted for', U0_EMAIL, '\u00b7 balance before:', await balance(), 'mco');\nlet g = await loadGraph();\nconst byId = (id: string) => g.nodes.find((n: any) => n.id === id);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:27:36)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts",
  "old_string": "for (const id of nodeIds) {\n  const n = byId(id);\n  if (!n) { console.error('node not found', id); continue; }\n  const kind = n.data.kind;",
  "new_string": "for (const id of nodeIds) {\n  g = await loadGraph(); // fresh \u2014 pick up outputs persisted by prior nodes in this run (firstFrame chaining)\n  const n = byId(id);\n  if (!n) { console.error('node not found', id); continue; }\n  const kind = n.data.kind;"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:27:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && nohup bun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/ep05-run.ts n_bvid_2 > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/witness-broll.log 2>&1 &\necho \"PID $!\"",
  "description": "Re-run b-roll (fixed runner) in background"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> PID 1245604
> ```

## 🤖 Claude *(00:27:52)*

<details>
<summary>💭 Thinking Process</summary>

I'm realizing there's a race condition here—both the b-roll and voice narrations need to write to the graph, and if their persist operations interleave, one will overwrite the other. The b-roll finishes quickly in about 2 minutes, but the voice work takes around 15 minutes, so starting them simultaneously creates a conflict window where their writes could collide.

The safest approach is to wait for the b-roll to complete first, then start the voice narrations. That way the graph writes stay serialized and clean. Let me wait for the b-roll process to finish.

</details>


## 🤖 Claude *(00:27:53)*

B-roll re-rodando. Para evitar corrida de escrita no grafo (read-modify-write full), vou serializar: aguardo o b-roll, faço Vision QA das 3 testemunhas pagas, depois disparo a voz. Aguardando o b-roll:

## 🤖 Claude *(00:27:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "until ! kill -0 1245604 2>/dev/null; do sleep 5; done; echo \"=== b-roll done ===\"; cat /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/witness-broll.log",
  "description": "Wait for b-roll, show log",
  "timeout": 420000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === b-roll done ===
> JWT minted for gabrielcall@gmail.com · balance before: 9456 mco
> 
> ▶ n_bvid_2 (imageToVideo) — Cena 2 · B-roll (Veo firstFrame 4s)
>   submit → 202 execution_id=3e2fc74b-68f2-4afe-a3db-363456930f8a charged=134
> 
  [n_bvid_2] poll 1 → status=running      
  [n_bvid_2] poll 2 → status=running      
  [n_bvid_2] poll 3 → status=running      
  [n_bvid_2] poll 4 → status=running      
  [n_bvid_2] poll 5 → status=running      
  [n_bvid_2] poll 6 → status=done (862554B)     
>   ✅ done · video=https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas... asset=64df70da-f51d-491a-a76a-d34873efad1a bytes=862554 · net=134 mco
> 
> balance after: 9322 mco
> ```

## 🤖 Claude *(00:28:51)*

<details>
<summary>💭 Thinking Process</summary>

I've completed processing all three paid witnesses—the image asset for Nano came through successfully, the B-roll video processed at 862KB with its asset ID and firstFrame path verified, and the Presenter video finished at 2.27MB with its corresponding asset identifier.

The total spend came to exactly 411 mco, which matches the gated witness budget perfectly, leaving a balance of 9322 mco. Now I need to run Vision QA on these three assets by actually viewing the media—downloading the nano image and extracting frames from both videos to inspect them visually. I'm querying the creative_assets table to get the storage paths and signed URLs for all three assets, then I'll download them and use ffmpeg to extract frames from the videos before reviewing everything.

</details>


## 🤖 Claude *(00:28:51)*

**Todas as 3 testemunhas pagas concluídas — saldo 9733 → 9322 = exatamente 411 mco (orçamento gated):**
- ✅ Nano `n_bimg_2` (10 mco) · imagem
- ✅ B-roll `n_bvid_2` (134 mco) · vídeo 862KB · asset `64df70da` · **firstFrame provado**
- ✅ Apresentador `n_p_1` (267 mco) · vídeo 2,27MB · asset `bdcee839` · **refs+clamp 8s provado**

Agora o gate mais importante (Lei 1 + [[feedback_vision_qa_always]]): **olhar a mídia**. Vou baixar os 3 assets, extrair frames dos vídeos e ver com meus olhos. Deixa eu resolver os storage paths e preparar os frames:

## 🤖 Claude *(00:28:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/qa-prep.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst ids=['bdcee839-6d8c-49db-b56e-02ded1118c20','64df70da-f51d-491a-a76a-d34873efad1a'];\n// b-roll + presenter assets\nconst { data } = await admin.from('creative_assets').select('id, storage_bucket, storage_key, asset_type, mime_type').in('id', ids);\nfor(const a of data??[] as any[]) console.log(a.id, '|', a.asset_type, a.mime_type, '|', a.storage_bucket, '|', a.storage_key);\n// nano image \u2014 resolve from the project node output\nconst { data: proj } = await admin.from('vm_canvas_projects').select('graph').eq('id','18a21002-df9c-48b4-aff3-7aba28e812e7').single();\nconst nano=(proj as any).graph.nodes.find((n:any)=>n.id==='n_bimg_2');\nconsole.log('NANO n_bimg_2 output:', JSON.stringify(nano.data.output));\n// find nano asset by id if present\nif(nano.data.output?.assetId){\n  const { data: na } = await admin.from('creative_assets').select('id, storage_bucket, storage_key, mime_type').eq('id', nano.data.output.assetId).maybeSingle();\n  console.log('NANO asset:', JSON.stringify(na));\n}\nEOF\nbun run /tmp/qa-prep.ts 2>&1 | head -20",
  "description": "Resolve asset storage paths for QA"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> NANO n_bimg_2 output: {"assetId":"7cccf046-9b64-48ac-b78b-c965dc4a535e","imageUrl":"https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ada39fae-67e1-4e53-af1c-5a18e1c108e8/spaces/323b9b4e-4682-441f-af44-7b8af8556057.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iNzFjZTA4Yy0xYWFjLTQ1MDUtOGEyZC04Y2Y5ZTU5MzI5MzIiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJjYW52YXMtYXNzZXRzL2FkYTM5ZmFlLTY3ZTEtNGU1My1hZjFjLTVhMThlMWMxMDhlOC9zcGFjZXMvMzIzYjliNGUtNDY4Mi00NDFmLWFmNDQtN2I4YWY4NTU2MDU3LnBuZyIsInNjb3BlIjoiZG93bmxvYWQiLCJpYXQiOjE3ODU3MTY3ODksImV4cCI6MTc4NjMyMTU4OX0.PHwmCOfGlrMbspZH5Sa2dFfen3xYaDW6i9Jv6k5SZzY","generatedAt":"2026-08-03T00:26:30.068Z"}
> NANO asset: {"id":"7cccf046-9b64-48ac-b78b-c965dc4a535e","storage_bucket":"canvas-assets","storage_key":"ada39fae-67e1-4e53-af1c-5a18e1c108e8/spaces/323b9b4e-4682-441f-af44-7b8af8556057.png","mime_type":"image/png"}
> ```

## 🤖 Claude *(00:29:11)*

<details>
<summary>💭 Thinking Process</summary>

The `.in()` query for those asset IDs isn't returning the presenter and b-roll assets—only the nano showed up in the output. I'm wondering if those video assets are stored under different IDs, in a separate table, or if the query just came back empty and didn't print anything from the loop.

Let me try a broader approach: I'll query the persisted node outputs directly for n_p_1 and n_bvid_2 since they should have the videoUrl and assetId stored there, and I can also double-check whether those asset IDs actually exist in creative_assets.

</details>


## 🤖 Claude *(00:29:11)*

O nano está em `canvas-assets`. Os assets de vídeo não vieram na query por id — vou pegar as `videoUrl` persistidas nos nós (o runner salvou) e verificar os assets de vídeo direto:

## 🤖 Claude *(00:29:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cat > /tmp/qa-prep2.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst { data: proj } = await admin.from('vm_canvas_projects').select('graph').eq('id','18a21002-df9c-48b4-aff3-7aba28e812e7').single();\nfor(const id of ['n_p_1','n_bvid_2']){\n  const n=(proj as any).graph.nodes.find((x:any)=>x.id===id);\n  console.log(id, 'status=', n.data.status, 'output=', JSON.stringify(n.data.output)?.slice(0,260));\n}\n// check asset ids in creative_assets (maybe stored under generated bucket)\nfor(const aid of ['bdcee839-6d8c-49db-b56e-02ded1118c20','64df70da-f51d-491a-a76a-d34873efad1a']){\n  const { data } = await admin.from('creative_assets').select('id, storage_bucket, storage_key, asset_type, mime_type, source_module').eq('id', aid).maybeSingle();\n  console.log('asset', aid.slice(0,8), '\u2192', data? (data.storage_bucket+' | '+data.storage_key+' | '+data.mime_type) : 'NOT FOUND');\n}\nEOF\nbun run /tmp/qa-prep2.ts 2>&1 | head -20",
  "description": "Resolve video node outputs + assets"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> n_p_1 status= success output= {"assetId":"bdcee839-6d8c-49db-b56e-02ded1118c20","videoUrl":"https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ada39fae-67e1-4e53-af1c-5a18e1c108e8/veo/b5443a05-cca8-494b-990c-b5c5e3d1ecdb.mp4?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWdu
> n_bvid_2 status= success output= {"assetId":"64df70da-f51d-491a-a76a-d34873efad1a","videoUrl":"https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/canvas-assets/ada39fae-67e1-4e53-af1c-5a18e1c108e8/veo/3e2fc74b-68f2-4afe-a3db-363456930f8a.mp4?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWdu
> asset bdcee839 → NOT FOUND
> asset 64df70da → NOT FOUND
> ```

## 🤖 Claude *(00:29:34)*

<details>
<summary>💭 Thinking Process</summary>

The video assets are stored differently than expected — the asset IDs from the veo-poll don't match the creative_assets table, but the signed video URLs are persisted with storage paths I can access directly. I'll download the three assets (the PNG and two MP4s) using the admin storage client by their storage keys.

Once I have them locally, I'll extract frames from the videos with ffmpeg and load the images. There's a downstream concern though — if these video assets aren't registered in creative_assets, they might not be discoverable in the Library for assembly later, so I should check whether the register_creative_asset function properly captures them.

Let me proceed with the QA download and frame extraction now, then separately verify that recent video assets for User 0 are showing up in creative_assets.

Writing QA download script...

</details>


## 🤖 Claude *(00:29:34)*

Vídeos persistidos (path `canvas-assets/.../veo/<exec>.mp4`). Os asset_ids do veo-poll não batem em creative_assets — vou verificar isso depois (pode afetar a montagem). Agora o QA ocular: baixar os 3 assets, extrair frames dos MP4 e ver:

## 🤖 Claude *(00:29:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a && source .env && set +a && cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad && cat > qa-dl.ts <<'EOF'\nimport { createClient } from '@supabase/supabase-js';\nimport { writeFileSync } from 'fs';\nconst admin = createClient(process.env.SUPABASE_URL!, process.env.SB_SECRET_KEY!, { auth:{persistSession:false}});\nconst items = [\n  ['nano.png', 'ada39fae-67e1-4e53-af1c-5a18e1c108e8/spaces/323b9b4e-4682-441f-af44-7b8af8556057.png'],\n  ['presenter.mp4', 'ada39fae-67e1-4e53-af1c-5a18e1c108e8/veo/b5443a05-cca8-494b-990c-b5c5e3d1ecdb.mp4'],\n  ['broll.mp4', 'ada39fae-67e1-4e53-af1c-5a18e1c108e8/veo/3e2fc74b-68f2-4afe-a3db-363456930f8a.mp4'],\n] as const;\nfor(const [out, key] of items){\n  const { data, error } = await admin.storage.from('canvas-assets').download(key);\n  if(error||!data){ console.log('ERR', out, error?.message); continue; }\n  const buf = Buffer.from(await data.arrayBuffer());\n  writeFileSync(out, buf);\n  console.log('saved', out, buf.length, 'bytes');\n}\n// verify video assets exist in creative_assets (recent U0 videos)\nconst { data: rec } = await admin.from('creative_assets').select('id, asset_type, storage_key, created_at').eq('user_id','ada39fae-67e1-4e53-af1c-5a18e1c108e8').eq('asset_type','video').order('created_at',{ascending:false}).limit(4);\nconsole.log('recent U0 video assets:'); for(const r of rec??[] as any[]) console.log('  ', r.id.slice(0,8), r.storage_key, r.created_at);\nEOF\nbun run qa-dl.ts 2>&1 | head -20\necho \"=== extract frames ===\"\nffmpeg -y -ss 2 -i presenter.mp4 -frames:v 1 presenter_f.jpg -loglevel error && echo \"presenter frame ok\"\nffmpeg -y -ss 2 -i broll.mp4 -frames:v 1 broll_f.jpg -loglevel error && echo \"broll frame ok\"\nls -la nano.png presenter_f.jpg broll_f.jpg 2>&1",
  "description": "Download assets + extract video frames"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> saved nano.png 1259775 bytes
> saved presenter.mp4 2288233 bytes
> saved broll.mp4 881163 bytes
> recent U0 video assets:
> === extract frames ===
> presenter frame ok
> broll frame ok
> -rw-rw-r-- 1 ubuntu ubuntu   27745 Aug  2 21:29 broll_f.jpg
> -rw-rw-r-- 1 ubuntu ubuntu 1259775 Aug  2 21:29 nano.png
> -rw-rw-r-- 1 ubuntu ubuntu   29191 Aug  2 21:29 presenter_f.jpg
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(00:29:58)*

<details>
<summary>💭 Thinking Process</summary>

The frames came through, but I'm noticing the video assets aren't showing up in the creative_assets table with asset_type='video' for User 0—that's a problem for downstream features like the Library display and asset discovery. The videos are definitely in storage and the graph nodes reference them, so they're accessible that way, but I should investigate whether the veo-poll registered them under a different asset type or if the registration failed altogether. I'll flag this and dig into it after QA.

Now I'm moving into the Vision QA phase—time to actually examine the three images and assess what matters: the presenter's identity and quality, the b-roll's continuity from the first frame, and the nano's composition. Let me pull up all three and evaluate them.

</details>


## 🤖 Claude *(00:29:59)*

Frames extraídos. (Nota: os assets de vídeo **não apareceram** como `asset_type='video'` em creative_assets do User 0 — vou investigar isso depois, pode afetar a Biblioteca/montagem; mas estão no storage e referenciados nos nós.)

Agora o **Vision QA ocular** (Lei 1) — vou olhar as 3 testemunhas:

## 🤖 Claude *(00:30:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/presenter_f.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(00:30:08)*

<details>
<summary>💭 Thinking Process</summary>

The presenter frame is looking strong with Gabriel's AI face and identity intact, lit with dramatic chiaroscuro from a single key light against the dark studio backdrop. The "EU NÃO EXISTO" headline dominates in high-contrast uppercase with that glitchy, dripping effect—exactly as the script calls for in the opening scene.

The 16:9 aspect ratio gives it that polished documentary feel, and the turtleneck and blazer keep the aesthetic professional and on-brand for the character. This cold open hits hard and establishes the Gabriel AI identity right away. Now moving into the b-roll and supporting visuals.

</details>


## 🤖 Claude *(00:30:09)*

Apresentador: **excelente** — rosto Gabriel AI com identidade preservada, chiaroscuro, headline "EU NÃO EXISTO" no estilo dripping/glitch exatamente como o roteiro cena 1 pede, 16:9, negative space acima. On-brief. Agora b-roll + nano:

## 🤖 Claude *(00:30:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/broll_f.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/jpeg'}}]
> ```

## 🤖 Claude *(00:30:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2cf8e553-9753-4c9c-9148-90a20004effe/scratchpad/nano.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/jpeg'}}]
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-08-02 - ee069eb3-c7d6-48b5-9c4e-032debc976b3]]
%% --- TIMELINE END --- %%

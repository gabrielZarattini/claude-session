# Resolver alertas e melhorar next steps dos projetos
**Date:** 2026-08-14 | **Session ID:** `863fa9e6-3ea7-490f-99e3-99a1876199e3`

---

## 👤 User *(03:23:21)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(03:23:21)*

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

### Scratchpad continuity (aprendizado contínuo — SOP `docs/processes/scratchpad-harvest.md`)

Se o Record mais recente do HANDOFF.md cita um path de scratchpad (`/tmp/claude-1001/.../scratchpad`),
verifique se ele ainda existe — material de produção da sessão anterior pode viver lá:
```bash
ls /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ 2>/dev/null | wc -l   # sessões vivas
```
Se a sessão vai CONTINUAR uma produção (master, screencasts, trilha), localize o workdir anterior
ANTES de regenerar qualquer coisa com custo: `find /tmp/claude-1001/<projeto>/ -maxdepth 3 -name "<artefato>"`.
Runners promovidos vivem em `scripts/<módulo>/` (ex.: `scripts/ep05/`). Reboot do host = scratchpads
mortos → reconstruir pelo Record (assets da Biblioteca + scripts do repo).

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


## 🤖 Claude *(03:23:25)*

I'll run the pick-up ritual now. Starting with the parallel pre-flight.

## 🤖 Claude *(03:23:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7 && echo \"---STATUS---\" && git status --short && echo \"---DIFFSTAT---\" && git diff HEAD --stat && echo \"---HANDOFF-LINES---\" && wc -l HANDOFF.md",
  "description": "Git history, status, diff scope, HANDOFF size"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 6bbe8d8 chore(sprint): registra o seal de 2026-08-13 (EP07 em MONTAR · gauntlet · cofre)
> b74fe03 docs(handoff): ORO + self-audit das 4 Leis + colheita do scratchpad no Record
> 41adebf docs(handoff): seal EP07 em MONTAR — motor v2, kit por gauntlet e a chave no cofre
> 895b461 chore(handoff): arquiva o record de 2026-08-10 — gate de tamanho com 0 folga
> adc4faa docs(readme): v6.140.0 — EP07 em MONTAR · kit por gauntlet · chave no cofre
> 4c6cf30 fix(ep07): o gráfico analítico vive DENTRO da folha — e a pilha vira leque
> 45c2627 feat(ep07): a pilha usa TODAS as variações + peças analíticas no catálogo + GO no gancho
> ---STATUS---
>  M proof-manifest.json
> ---DIFFSTAT---
>  proof-manifest.json | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> ---HANDOFF-LINES---
> 516 HANDOFF.md
> ```

## 🤖 Claude *(03:23:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---MEGABRAIN---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s -m 5 http://localhost:8001/api/v2/heartbeat || echo \"CHROMA_ERR\"",
  "description": "Docker mesh + Chroma heartbeat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 7 days (healthy)
> mcorch_claude_mem: Up 7 days (healthy)
> mcorch_chroma: Up 7 days (healthy)
> ---MEGABRAIN---
> mega-brain-dashboard: Up 7 days
> mega-brain-webhook: Up 7 days (healthy)
> mega-brain-daemon: Up 7 days (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1786677809561181111}
> ```

## 🤖 Claude *(03:23:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null && echo \"---SCRATCH---\" && (ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\") && echo \"---SESSIONS---\" && ls /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ 2>/dev/null | wc -l",
  "description": "List BoK suites, scratch, scratchpad sessions"
}
```

## 🤖 Claude *(03:23:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "timeout 300 npx tsc -p tsconfig.app.json --noEmit 2>&1 | tail -20; echo \"EXIT=$?\"",
  "description": "TypeScript app check",
  "timeout": 330000
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
> mco-monetization
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
> spaces-agent
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
> ---SCRATCH---
> scratch has files
> ---SESSIONS---
> 42
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> EXIT=0
> ```

## 🤖 Claude *(03:24:29)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking the HANDOFF.md file which is a manageable 516 lines, then reviewing the sprint priorities and scratch contents. I notice the TypeScript compiler exit code handling needs clarification — the pipe to `tail` means I'm actually getting that command's exit status rather than tsc's, so I should verify the error output was genuinely empty and consider using PIPESTATUS for accuracy.

</details>


## 🤖 Claude *(03:24:29)*


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
> 6	git log --oneline -20
> 7	# ═══════════════════════════════════════════════════════════════════════════════════════════
> 8	# 🎯 UPDATE 2026-08-11 (seal 2) — 3 COFRES BLINDADOS · INIT ENXUTO · EP07 ANCORADO E PROVADO
> 9	# ═══════════════════════════════════════════════════════════════════════════════════════════
> 10	#
> 11	# ⚡ COMECE POR AQUI (o que ESTA sessão fez — 5 commits, tsc-app 0, gitleaks limpo, malha 20.521):
> 12	#
> 13	#  1. 🛡️ OS 3 COFRES DA SECRET KEY GANHARAM DETECÇÃO CONTÍNUA (diretiva "blindar detecção 3-cofres").
> 14	#     A chave vive em .env · vault das Edge Functions · vault do Postgres, e só o 1º era provado
> 15	#     sempre. Agora: self-heal-bridge-keys.sh ganhou o GATE 1b (prova o vault das edge fns via
> 16	#     get-infra-status — 500 = chave do vault morta); mcorch-doctor.sh ganhou a §4b "Liveness dos
> 17	#     3 cofres" (a §4 só provava PRESENÇA — chave revogada-mas-presente passava verde, a armadilha
> 18	#     de 08-08); rotate-supabase-secret.sh virou ATÔMICO (encadeia sync-edge + auto-atualiza o vault
> 19	#     do Postgres com PAT + re-verifica md5). Provado agora: doctor §4b = 3 PASS. SOP v1.1.
> 20	#     ⚠️ NÃO reverter. "vault-direct" (ler a chave do vault em vez do .env) = paradoxo de bootstrap.
> 21	#
> 22	#  2. 🪶 OS ARQUIVOS DE INIT EMAGRECERAM ~192 KB (sessões arrancavam com >100k de contexto).
> 23	#     sprint-priorities.md 183 KB → 26 KB (log de 84 sprints arquivado byte-idêntico em
> 24	#     .claude/context/sprint-priorities-archive-2026-08-11.md); CLAUDE.md Key Files 89,8 → 65,6 KB
> 25	#     (39 collapses, 0 removes, verificação adversarial preservou 8 paths CLAUDE.md-only). O maior
> 26	#     ofensor era o sprint-priorities (88k tokens pelo tokenizer real, lido em todo /handson).
> 27	#
> 28	#  3. 🎯 EP07 — 12 NÚMEROS ANCORADOS + ROTEIRO v0.1 + PIPELINE DE PRODUÇÃO PROVADO. Deepsearch (10
> 29	#     agentes, adversarial): 8 supported / 2 partial / 3 not_found. Os fabricados de patrocínio
> 30	#     ("US$1000-1500/cota", "US$10k+/ep", "15-30 por show") viraram a realidade Podpah sourced
> ```

## 🤖 Claude *(03:24:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null | head -20; echo \"---SPRINT---\"; wc -l .claude/context/sprint-priorities.md 2>/dev/null; echo \"---NEXTSTEPS---\"; ls -la NEXT-STEPS.md 2>/dev/null || echo \"sem NEXT-STEPS.md\"; echo \"---TSC-REAL---\"; timeout 300 npx tsc -p tsconfig.app.json --noEmit > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/tsc.log 2>&1; echo \"TSC_EXIT=$?\"; wc -l < /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/tsc.log",
  "description": "Scratch contents, sprint file, tsc exit code real",
  "timeout": 330000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxrwxr-x  2 gcrUX gcrUX 4096 Jun 30 01:44 .
> drwxrwx--- 32 gcrUX gcrUX 4096 Aug 14 00:09 ..
> ---SPRINT---
> 154 .claude/context/sprint-priorities.md
> ---NEXTSTEPS---
> -rw-rw-r-- 1 gcrUX gcrUX 20833 Jul 29 20:05 NEXT-STEPS.md
> ---TSC-REAL---
> TSC_EXIT=0
> 0
> ```

## 🤖 Claude *(03:25:16)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking that the scratch directory is empty, then diving into the HANDOFF.md file to understand the first action and current task state, along with reviewing the sprint priorities document.

</details>


## 🤖 Claude *(03:25:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 30,
  "limit": 130
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 30	#     ("US$1000-1500/cota", "US$10k+/ep", "15-30 por show") viraram a realidade Podpah sourced
> 31	#     (nicho BR R$500-5k/ep · R$100mi/ano agregado · grupo ~100-120 pessoas/6.500m²/7 estúdios/R$9mi).
> 32	#     AdSense 45/55 e macro (R$4,94bi PIB/130k empregos/US$19,28bi) verbatim. Roteiro:
> 33	#     docs/roadmap/ep07-roteiro-2026-08-11.md · ancoragem: pauta §3-bis. Runners scripts/ep07/
> 34	#     provam o motor de PRODUÇÃO (scene-template.ts) rendendo data-viz HONESTO (split 45/55, CPM
> 35	#     18/27, beat na palavra): 4,3-4,4 Mbps · 100% frames únicos · 1080p. Antídoto do EP06 (que
> 36	#     usou um fork degradado: 41.953 bitrate, 299/4620 frames únicos).
> 37	#
> 38	#  ⏭ PRÓXIMO (maratona, próxima sessão com direção criativa decidida): produção do EP07 completo
> 39	#     (7 blocos + 2 Veo gancho/fecho ~1.460 mco GO'd + narração + montagem + QA A/V). Decidir
> 40	#     data-viz vs layers-com-asset nos blocos-herói. BoK mco-monetization: gate por-fatia correto
> 41	#     (FECHADO pendendo o SOP mcoin-topup.md + decisões OTD-MON de preço/política — mão do Sovereign).
> 42	#
> 43	# ═══════════════════════════════════════════════════════════════════════════════════════════
> 44	# 🎯 UPDATE 2026-08-11 — SEGURANÇA, AUDIÊNCIA E ANTICORPOS. Direção segue **EP07**.
> 45	# ═══════════════════════════════════════════════════════════════════════════════════════════
> 46	#
> 47	# ⚡ COMECE POR AQUI (o que mudou desde o último seal — tudo já no ar e re-provado):
> 48	#
> 49	#  1. 🔴→✅ **P0 DE SEGURANÇA FECHADO.** O `stripe-webhook` aceitava evento forjado de QUALQUER UM:
> 50	#     o guard era `if (webhookSecret && sig)` e o `else` fazia `JSON.parse(body)`. Quem OMITIA o
> 51	#     header `stripe-signature` era processado como legítimo, numa fn pública (`verify_jwt=false`).
> 52	#     Provado nos 2 sentidos: sem header → 200 · com assinatura ruim → 400. Fail-closed + deploy +
> 53	#     re-prova (agora 400 "Missing stripe-signature header"). **NÃO reverter para o guard condicional.**
> 54	#
> 55	#  2. 🔑 **A CHAVE VIVE EM TRÊS COFRES, NÃO DOIS** — a descoberta que faltava ao incidente de 08-08:
> 56	#        (1) `.env`  (2) vault das Edge Functions  (3) **vault do POSTGRES** `vault.decrypted_secrets`
> 57	#            name='sb_secret_key' — de onde o **pg_cron** lê o Bearer (migrations 20260623040000 /
> 58	#            20260603230000). O terceiro ficou para trás e matou `autopilot-cadence` + `nurture-advance`
> 59	#            por **55h** com `active=true` e ZERO alarme. Corrigido; crons batendo desde 04:00Z.
> 60	#     → `rotate-supabase-secret.sh` ganhou o passo 6: compara o md5 do cofre do Postgres e recusa
> 61	#       dizer "rotação completa" sem ele.
> 62	#
> 63	#  3. 🛡️ **SELF-HEALING NO CRON `*/5`** — `scripts/qa/self-heal-bridge-keys.sh` (SOP
> 64	#     `docs/processes/bridge-key-freshness.md`). Três portões: chave morta ⇒ **recusa reiniciar**
> 65	#     (espalharia o defeito — é gate do Sovereign); ponte iniciada antes da última mudança do `.env`
> 66	#     ⇒ reinicia e **prova** pelo `ExecMainStartTimestamp`; `pg_cron` ⇒ detecta pela **AUSÊNCIA de
> 67	#     batimento** em `infra_health_logs` (ele não aparece no `systemctl`).
> 68	#     **REGRA:** `active (running)` NÃO é prova de saúde. `youtube-upload` rodava VERDE havia 5 dias
> 69	#     segurando a chave revogada.
> 70	#
> 71	#  4. 📊 **A AUDIÊNCIA DO CANAL FOI MEDIDA** (17/17 sondas) — `docs/roadmap/ep07-calibracao-audiencia-2026-08-11.md`.
> 72	#     Público **100% masculino**, núcleo 25-54 (centro 35-44) · **100% BR** nos últimos 90 dias, e o BR
> 73	#     retém o DOBRO do US · **episódio converte 14× mais que Short** (2,41% × 0,17%) e o elo
> 74	#     `SHORTS_CONTENT_LINKS` tem **4 views em toda a história** · título com TESE converte 15-24× mais
> 75	#     que manchete · ponto ótimo **7-8 min**. **Isso calibra o roteiro do EP07 — leia antes de escrever.**
> 76	#     4 jobs de Reporting API criados (impressões/CTR + demografia por vídeo); 1º CSV em ~24-48h.
> 77	#     Runner: `bun run scripts/pipc/youtube-audience-sweep.ts`
> 78	#
> 79	#  5. ✂️ **ACERVO PODADO** — 148 → 101 vídeos (47 cortes com legenda queimada + duplicados, 419,6 MB).
> 80	#     Os 7 publicados intactos. ⚠️ **`space_publish_variants.status` NUNCA vira `published`** — quem
> 81	#     transita é o `scheduled_posts`, via `metadata.reshape.space_publish_variant_id`. Confiar na
> 82	#     leitura óbvia teria apagado mídia no ar.
> 83	#
> 84	#  6. 🎬 **FORMATO NOVO: GRID 16:9 EM 2 E 3 LINHAS** (diretiva Sovereign). `2v`, `1x3`, `reframe:'16:9'`
> 85	#     e crop por célula **JÁ EXISTEM** no motor. Falta só a **legenda alpha** — Amendment 46 selada
> 86	#     (FR-SPACES-185..188). Aritmética: `1x3` preenchendo corta só **5%** da largura; `2v` encaixando
> 87	#     abre **352px** contíguos de faixa. **Próximo passo do Sovereign: legenda alpha → pilotos.**
> 88	#
> 89	# ✅ A CRISE DA CHAVE ESTÁ ENCERRADA — AS DUAS METADES FECHADAS (re-provado em 2026-08-11 02:04):
> 90	#    HISTÓRICO: a secret key do Supabase foi **revogada em 08-08 17:18** e derrubou EM SILÊNCIO
> 91	#    as 6 pontes de render (systemd dizia "active (running)" sem pegar job), as Edge Functions e
> 92	#    todo script CLI. O app seguiu de pé porque usa a publishable — por isso ninguém viu por 2 dias.
> 93	#
> 94	#    ✅ METADE 1 (o `.env` — workers e CLI) resolvida em 2026-08-10 22:08 pelo Sovereign
> 95	#       (`bash scripts/qa/rotate-supabase-secret.sh`).
> 96	#    ✅ METADE 2 (o **vault das Edge Functions**, que NÃO lê o .env) resolvida por
> 97	#       `bash scripts/qa/sync-edge-secret.sh` — commit `7e5d45d`. **NÃO peça PAT de novo.**
> 98	#
> 99	#    → GATES RE-PROVADOS NESTA SESSÃO (2026-08-11 02:04, ambos VERDES):
> 100	#      curl -o /dev/null -w '%{http_code}' \
> 101	#        "$VITE_SUPABASE_URL/rest/v1/profiles?select=id&limit=1" -H "apikey: $SB_SECRET_KEY"
> 102	#        → **200**  (saldo 40.775 mco · malha 20.425 nós / 24.949 arestas)
> 103	#      curl -s "$VITE_SUPABASE_URL/functions/v1/get-infra-status" -H "apikey: $VITE_SUPABASE_PUBLISHABLE_KEY"
> 104	#        → **200** {"chroma":"healthy","intelligence":"healthy","checked_at":"2026-08-11T02:04:58.131Z"}
> 105	#      As 11 pontes systemd (motion · video · voice · subtitle · repurpose · provenance ·
> 106	#      youtube-upload · design · crm-media · video-studio · sso-auth-gate) estão `active (running)`.
> 107	#
> 108	#    ⚠️ LIÇÃO (Lei 1 — por que este bloco foi reescrito): a versão anterior deste mesmo bloco
> 109	#       declarava "⛔ METADE 2 PENDENTE · get-infra-status devolve HTTP 500 · Sovereign precisa
> 110	#       gerar um PAT" DEPOIS de o fix já ter sido commitado. O `/handson` seguinte quase gastou a
> 111	#       janela do Sovereign pedindo um PAT desnecessário. **Bloco de HANDOFF nunca é fonte de
> 112	#       verdade sobre estado — o gate rodado NESTE turno é.** Mesma família do `systemctl`
> 113	#       vs. cláusula-de-gate stale (provenance-bridge, subtitle-bridge, motion MONTAR).
> 114	#       Memória: reference_supabase_secret_key_rotation_silent_kill
> 115	#    ⚠️ ARMADILHA: com chave inválida o bucket CERTO também devolve "Bucket not found". Se após
> 116	#      trocar a chave o erro persistir, use o teste discriminante:
> 117	#      canvas-assets → NoSuchKey (chave OK, path errado) vs creative_assets → NoSuchBucket (é TABELA, não bucket).
> 118	#    Memória: reference_supabase_secret_key_rotation_silent_kill
> 119	#
> 120	# 🎬 A DIREÇÃO (Sovereign 2026-08-10): **vamos para o EP07**, com a MESMA estratégia de roteiro,
> 121	#    ganchos, viral e educacional dos nossos deepsearches. O EP06 NÃO é mais o alvo — é acervo.
> 122	#    A pauta do EP07 JÁ EXISTE e já vem com o gate declarado:
> 123	#      • docs/roadmap/ep07-pauta-economia-videocast-2026-08-05.md
> 124	#        "A economia secreta por trás dos videocasts brasileiros" · 3 negócios = 3 atos
> 125	#        (patrocínio · AdSense · áudio-podcast). Tese: o público desse tema É o usuário-alvo do
> 126	#        MCORCH. Fecho: 15-30 pessoas da indústria × 1 pessoa + 1 máquina que fez este vídeo.
> 127	#        ⚠️ GATE DE ANCORAGEM: 12 números SEM fonte — rodar `deepsearch-blueprint` (1 frente por
> 128	#        bloco, URL em toda claim, crítico adversarial) ANTES de virar narração. A regra é
> 129	#        "nenhum número não-ancorado" — o EP06 provou por que ela existe (imprimiu 2800000,0 tri).
> 130	#    Os 4 pilares de doutrina, todos já escritos e verificados:
> 131	#      • VIRAL/DISTRIBUIÇÃO → docs/roadmap/organic-shorts-strategy-inicial-2026-07-30.md (§D1-D7 DEFINITIVAS)
> 132	#      • GANCHOS           → docs/roadmap/hook-library-seed-2026-07-30.md (10 combos falado+headline)
> 133	#      • EDUCACIONAL       → docs/roadmap/tutorial-track-iamaimaster-template-2026-08-04.md (+7 repos OSS)
> 134	#      • ROTEIRO/MOLDE     → docs/roadmap/ep06-roteiro-producao-2026-08-07.md (notação [V]/[M:card]/[M:chart]/[M:hud])
> 135	#    Contexto editorial: 2 vídeos/semana (documentário + tutorial) · motion-first p/ gastar menos
> 136	#    com Veo · **usar o método sem anunciá-lo** (memória project_channel_two_videos_week_editorial).
> 137	#
> 138	# 🔬 A CAUSA-RAIZ DO "VÍDEO QUE NÃO SAI" — achada por auditoria de 13 agentes (wf_b78f931d-bc6):
> 139	#    **O pipeline entrega o RÓTULO da técnica sem a TÉCNICA, e nada no caminho mede a diferença.**
> 140	#    (a) O motor que renderizou o EP06 NUNCA foi o MONTAR do benchmark. Prova: em
> 141	#        scripts/ep06/render-all-scenes.ts:79 o campo é `companions: opts.companions ?? []` e
> 142	#        NENHUMA das 14 entradas de SCENES define `companions` ⇒ toda cena saiu com UM plano
> 143	#        (a imagem "hero") + texto de HUD. E `grep -c 'blur('` em montar-scene-template.mjs = **0**,
> 144	#        contra **9** no benchmark scripts/motion/layered/build-scene.mjs, que ainda tem `dof(z)`
> 145	#        (linha 326) e um mapa Z de 8 profundidades sobre 12 planos. Ou seja: era um Ken Burns
> 146	#        numa imagem de IA usando o nome "MONTAR". Nenhum ajuste de prompt/trilha/montagem
> 147	#        conserta isso — **o quadro é que está pobre**.
> 148	#    (b) O v4 (feito no Antigravity) é PIOR: **22 cartelas estáticas** de 7,000s (22×7=154,0s
> 149	#        exatos, freezedetect acusa 147s congelados) sobre uma **senoide de 110 Hz**, ZERO narração.
> 150	#        Causa material: download-and-assemble.cjs:55 baixa do bucket `creative_assets` — que é o
> 151	#        nome de uma TABELA — e o `curl -s -o` (sem `-f`) gravou o JSON de erro DENTRO dos .mp3/.mp4:
> 152	#        19 arquivos de 98 bytes, md5 idêntico, contendo {"code":"NoSuchBucket"}. O montador
> 153	#        detectou os stubs pelos próprios size-guards, degradou as 22 cenas em silêncio e imprimiu
> 154	#        "🎉 MASTER EP06 v4 CONCLUÍDO COM SUCESSO".
> 155	#    (c) Toda camada declara sucesso sem prova. Três sessões seguidas escreveram "master pronto"
> 156	#        sem abrir um frame.
> 157	#
> 158	# ⚠️ O HANDOFF ANTERIOR MENTIA (corrigido aqui, Lei 1): dizia "ep06-master-v4.mp4 (13.9 MB ·
> 159	#    151.73s) · 22 cenas · 5 camadas em Z · voz IVC Cenas 01-14". O arquivo real tem
> ```

## 🤖 Claude *(03:25:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: **EP07** ("economia dos videocasts") ancorado (12 números via deepsearch) e produzido com o motor MONTAR elevado (`dof(z)`+planos+`companions[]`); esteira de pós-produção de episódio no Spaces (Amendment 34); segurança/monetização fail-closed (3 cofres da secret key verdes); distribuição orgânica de shorts.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	## 📋 FILA SOVEREIGN (ordem declarada — não reordenar sem GO)
> 8	
> 9	| # | Item | Estado | Gate |
> 10	|---|------|--------|------|
> 11	| 🎬 **FEITO 2026-08-13** | **EP07 em MONTAR: motor v2 · kit por gauntlet · chave no cofre** — 13 commits `d379f86..b74fe03`. Motor MONTAR v2 spec-driven do benchmark `fcf91d44` (+3 correções de defeito medido: `__fatal` antes do frame 1 · ancoragem por centro · `style`/`plain`). Trupe: **5.324 linhas de Partitura** (5 blocos × 4 lentes) + Veo em **16:9 nativo**. **Gauntlet de peça** pegou 4 defeitos invisíveis a geração única. Pesquisa v2v (6 frentes + crítico): **recâmera por API não existe provada**; presenter crível = lip-sync sobre plate real; **Higgsfield não se assina** (ToS §11.5). Vazamento de chave fechado **na fonte** (6 nós da malha). Imagem migrada p/ **API Google direta**. Malha **20.823** · nó `69c02e4b`. ⚠️ **Veredito visual do Sovereign: PoC, "ainda amador"** — a régua é um link de cinema. | ✅ | — |
> 12	| 🛡️ **FEITO 2026-08-11 (seal 2)** | **3 cofres blindados · init enxuto · EP07 ancorado e pipeline provado** — 6 commits `34b7f64..1ab6ea5`. Detecção contínua dos 3 cofres da secret key (self-heal GATE 1b · doctor §4b · rotação atômica; SOP v1.1). Init **−192 KB** (sprint-priorities 183→26 KB · CLAUDE.md Key Files 89,8→65,6 KB, 0 removes). **EP07:** 12 números ancorados por deepsearch (8✅/2🟡/3❌ → fabricados viram a realidade Podpah sourced) + roteiro v0.1 + **pipeline de produção provado** (motor `scene-template.ts` → data-viz honesto 4,4 Mbps/100% frames únicos). Malha 20.521. | ✅ | — |
> 13	| 🛡️ **FEITO 2026-08-11** | **Segurança, audiência e anticorpos** — 10 commits `506ed7d..42d238d`. **P0 vivo fechado:** `stripe-webhook` aceitava evento forjado de qualquer um (omitir o header dava 200) → fail-closed, deployado, re-provado. **A chave vive em TRÊS cofres** — o do POSTGRES (`vault.decrypted_secrets`, de onde o pg_cron lê) ficou para trás e matou `autopilot-cadence`+`nurture-advance` por **55h** com `active=true`; corrigido e batendo. **Self-healing `*/5`** (`self-heal-bridge-keys.sh`). **Audiência medida** (17/17 sondas): episódio converte **14× mais que Short**; calibração em `docs/roadmap/ep07-calibracao-audiencia-2026-08-11.md`. **Reporting API** com 4 jobs (impressões/CTR). **Acervo podado** 148→101. **Amendments 28-bis/46**. Suíte de monetização com gate **FECHADO** pelos críticos. | ✅ | — |
> 14	| 🎯 **AGORA (2026-08-10)** | **EP07 — "A economia secreta por trás dos videocasts brasileiros"** (direção Sovereign: *"vamos para o EP07 seguindo a mesma estratégia… conforme nossos deepsearch"*). Pauta e os 4 pilares JÁ escritos: `docs/roadmap/ep07-pauta-economia-videocast-2026-08-05.md` · `organic-shorts-strategy-inicial-2026-07-30.md` (§D1-D7) · `hook-library-seed-2026-07-30.md` · `tutorial-track-iamaimaster-template-2026-08-04.md`. **O EP06 saiu do alvo — virou acervo** (`repurpose-inbox/<uid>/ep06-montar-harvest/`, 780 MB colhidos). | ⏳ Ordem: (1) `deepsearch-blueprint` ancorar os **12 números** da pauta; (2) **ELEVAR O MOTOR** antes de produzir — portar `dof(z)`+planos+atmosfera e popular `companions[]`, piloto de UMA cena com gate triplo; (3) montar com `assemble-master.ts` fail-closed. **(edge vault já fechado 2026-08-11 — os 3 cofres verdes, provados por `mcorch-doctor §4b`.)** | 🔒 **Sovereign:** GO para produzir o EP07. |
> 15	| ✅ **FEITO 2026-08-11** | ~~**3 regressões de `src/`**~~ — ENTREGUE (`43f5fea`): a fabricação de 7 `creative_asset` extirpada (−275 linhas, incluindo o "13.9 MB/151,73s" que 3 sessões repetiram), os 2 `if (error) throw error` restaurados, e a rota autenticada `/api/host-media` de volta — os masters respondiam **HTTP 206 a chamador anônimo**. Detalhe original: | ⚠️ **DÍVIDA** | **3 regressões de `src/`** entradas em `bd2b9df`/`0608662`: `asset-url.ts` perdeu a rota autenticada `/api/host-media` (masters EP01/EP02 → 404; mídia EP06 pública sem JWT) e `useCreativeAssets.ts` perdeu os dois `if (error) throw error` (galeria "saudável" com 7 assets falsos `user_id:'system'`, quebra o `getNextPageParam`). Nada disso falha build/tsc/lint. | ⏳ Reverter preservando o fix legítimo de `zIndex:-1` do phaseGroup. | — |
> 16	| 🎯 **AGORA-ter** | **Amendment 34 — pós-produção de episódio no Spaces (o gap CLI→UI)** — o EP05 provou a esteira completa, mas 5 elos vivem só como runner em `scripts/ep05/` e nenhum usuário alcança: **`motionScene` · `soundtrack` · `titleCard` · `episodeAssembler` · `avQaGate`** (todos de custo ZERO no host) + **design 3D Glass Neon nos cards** (FR-SPACES-136) + receita "Episódio completo". SSOT: `docs/bok/spaces-evolution/34-amendment-episode-post-production.md` (FR-SPACES-130..136 · Pattern Conformance 16y/3d/2na · OTD-EP-001..004). É [[feedback_cli_actions_must_become_ui]] aplicado: hoje o produto entrega ingredientes, não o prato. | ✅ **Amendment SELADA** (BoK antes do código, §1). Fatias: **A** `motionScene`+worker (destrava 16 das 22 cenas do EP06) → **B** 3D Glass Neon → **C** titleCard+assembler → **D** avQaGate → **E** soundtrack+receita. | 🔒 **Sovereign:** GO para arrancar a Fatia A. |
> 17	| 🎯 **AGORA** | **▶️ Rodar o EP06 na UI — Passo A + Passo B** — o projeto `a65eeb05` está **armado e verificado por pré-voo** (`bun run scripts/qa/preflight-spaces-project.ts <id>` → 0 bloqueadores). 13 cenas motion com beats/série/narração · 3 narrações em `idle` com texto v2 · 4 presenters em **`veo-3.1`/1080p** (2.848 mco) · montador com 17 clipes. O motor mudou por completo nesta sessão: contador honesto, tela que cala quando o narrador fala, selos, anel, gráfico com dado declarado, beat na palavra falada, 1080p nativo. | ⏳ **Aguardando o clique do Sovereign** (recarregar a página primeiro — build novo). Se o Veo do Google estiver sobrecarregado como em 2026-08-05, o estorno é integral e o poller novo impede nó preso. | 🔒 **Sovereign:** GO já dado para o gasto; falta executar. |
> 18	| 🎯 **AGORA-bis** | **Exportar para YouTube — witness E2E** (Amendment 41, `0a92e44`): a cadeia crf14/slow + BT.709 + grão + grade unificada está no ar, mas **nunca rodou num master real de 5 min**. Medido só em clipe curto (~9,3× tempo real). | ⏳ Depende do master do EP06 existir. | — |
> 19	| ✅ **FEITO 2026-08-06** | ~~**🐛 Poller de PÁGINA do Veo + auditoria Veo**~~ — ENTREGUE (`4b7e0e3`): alça gravada no dispatch + hook de página no molde do `useMotionRenderSync`, varredura sequencial a 12s, tie nó↔geração antes de escrever (nunca falso-sucesso, nunca falso-estorno), resgate pelo ledger para nós sem alça. 19 testes + smoke 13/13. **O que sobra:** witness E2E pago (1 geração real com o inspector FECHADO). Detalhe original: — o Run All de presenters Veo TRAVA: `useVeoPoll` só roda no inspector aberto → num Run All headless ninguém chama `veo-poll` → gerações `running` eternas + nós presos + `runSingleNode` não grava `veoGenerationId`. Fix: gravar o id no dispatch + hook de página (molde `useMotionRenderSync`) que faz poll dos imageToVideo running e reconcilia. **Auditoria Veo** (pedido Sovereign): conferir cobrança/estorno — runner `scripts/qa/recover-stuck-veo.ts <project_id>`. Contexto: os 4 presenters do EP06 v2 `a65eeb05` FALHARAM por Google 'high load' e foram **integralmente estornados** (1068 mco, saldo 44394). | ⏳ **Descoberto 2026-08-05c.** O Run All server-side de motion+master JÁ funciona (Amend 36, witness aba-fechada); só o rail PAGO (Veo) precisa do poller. | 🔒 **Sovereign:** GO p/ o poller + auditoria; re-tentar Passo A quando o Veo do Google não estiver sobrecarregado. |
> 20	| ✅ ex-AGORA | **Controles de execução do Spaces — ENTREGUE 2026-08-05c** (13 commits `333c43f..e8b489d`): Run All 100% server-side (Amend 36, fecha a aba) + aviso de sessão + execução seletiva (35) + cards de FASE com botão/resize + skip-success anti re-débito (38) + STOP na fila e nós presos + faxina de projeto (39) + motor motion v2 (37) + UX (handles verticais, painéis colapsados, full-bleed, RF oculto). | ✅ | — |
> 21	| ✅ ex-AGORA | **spaces-agent HÍBRIDO (Opção C) — ENTREGUE 2026-08-05** — MVP chat-por-nó (Amendment 33 ao spaces-evolution) + suite BoK `spaces-agent` completa (bok-curator em paralelo). LLM: cascata Groq→OpenRouter (aios-chat-gateway + openrouter-swarm). NOVA tabela `spaces_node_threads` (RLS per-user). Cobrança mco por mensagem. Referências: Magnific storyline + Buzzy AI shots + Higgsfield 2.5. **Caso de uso primário (diretiva 2026-08-04): criar por conversa TODOS os nós, prompts e roteiros de um episódio novo** — dogfood = próximo EP. | 🟢 Em execução (sessão 2026-08-04). | — |
> 22	| 🎯 **AGORA-bis** | **Pivô editorial (diretiva Sovereign 2026-08-04): 2 vídeos/semana** — (a) documentário informativo: **EP06 = compilado semanal dos daily briefs** (alvo: postar 2026-08-05); (b) educacional/tutorial estilo **@iamAImaster** — ensinar Claude Code com repositórios open-source famosos. Motion-first p/ gastar MENOS com Veo. **Usar o método, não anunciá-lo.** Memória `project_channel_two_videos_week_editorial`. | ✅ **Roteiro EP06 PRONTO**: `docs/roadmap/ep06-roteiro-compilado-semana-2026-08-04.md` (22 cenas · 4 atos · 16 motion + 4 presenters · **~1.100 mco vs 6.180 do EP05 = −82%**), fundado nos 4 daily briefs colados pelo Sovereign (`ai-briefs-semana-2026-07-29-a-08-04.md`). Projeto Spaces armado PELO agente: `d0d82aeb` (13 nós). Trilha tutorial mapeada: `tutorial-track-iamaimaster-template-2026-08-04.md` (perfil real do canal + 8 repos OSS verificados na API do GitHub). | 🔒 **Sovereign:** GO para produzir (12 narrações IVC → 4 presenters Veo 1.068 mco → 11 peças motion grátis → assemble + QA A/V → thumb ciano). |
> 23	| 🎬 EP05 A14 **GUARDADO** (2026-08-04) | **MASTER A14 COMPLETO** (asset `6e3175b3`, 488.20s, QA A/V fino verde) — veredito Sovereign: "ficou muito bom… vamos usar futuramente". **NÃO vai domingo** — anuncia o produto antes da hora; sai depois de aplicar o método com várias pessoas. | ✅ Pronto na Biblioteca, aguardando o momento editorial. Retake opcional p14 (esteira, 267 mco) fica junto. | 🔒 **Sovereign:** decidir QUANDO publicar (pós-prova social do método). |
> 24	| ✅ ex-AGORA | **Criação do EP05 — formato TUTORIAL** — parecer registrado + decisão selada como Angle C narrative-first. | ✅ Roteiro v2 formato GabrielAI + projeto Spaces v2 armado (2026-08-03). | — |
> 25	| ✅ ex-AGORA | **EP02/EP03 no YouTube pela plataforma (Track B)** — CUMPRIDO: EP03 master postado (2026-07-29). Encanamento vivo: `youtube-upload.service` active/enabled, worker resumable dual-source. | ✅ | — |
> 26	| 🎯 0 | **CRM Suite completo + Marketing (diretiva Sovereign 2026-07-19)** — construir um CRM de VERDADE nativo, pilar por pilar (open-source descartado, AGPL). **Os loops NÃO param até fechar.** SSOT: `docs/roadmap/crm-suite-and-marketing.md`; memória `project_crm_suite_roadmap`. Pilares CRM: Contatos(✅ A4 2026-07-24 — tabela+RLS+CRUD, OTD-CS-001 resolvida)·Empresas·Leads(✅)·Negócios·Tickets·Produtos·Serviços·Pedidos·Compromissos·Caixa-de-entrada(✅)·Chamadas·Reuniões·Tarefas·Playbooks·Listas·Segmentos·Modelos·Snippets. Marketing: AEO·Beta(🔎)·SEO·Campanhas(✅)·E-mail·Redes(✅)·Anúncios·Eventos·Formulários·CTAs·SMS·Intenção·Pontuação(✅)·Análise·Marca. | ⏳ **Fase 0 = BoK `docs/bok/crm-suite/`** (spine de entidades + associações + timeline) ANTES dos pilares — módulo maior, Closed-Loop gate. Depois: fatias na sequência do SSOT. | 🔒 **Próximo:** GO Sovereign p/ arrancar o BoK/blueprint do crm-suite (ou apontar o 1º pilar) |
> 27	| 1b | **Veo via Vertex AI (service account)** — Amendment 26, FR-SPACES-092..096 (2026-07-15) | ✅ **PROVADO REAL E2E 2026-07-15** (role concedida → witness pago gen `2659d78b`, `engine=veo-vertex`, 720×1280 9:16 8s, identidade preservada Read+Vision MCP, **267 mco** exatos 4263→3996, asset `bb0ec719`, nó `4e8902d2`). code-complete + `/security-review` (1 HIGH SSRF FECHADO) · 584 testes · a chave `AQ.` do Sovereign é Gemini API mas o trial GCP só cobre o Vertex (429 na AI Studio, documentado no README do repo GabrielAI). O pipeline local usa gcloud ADC; servidor usa service account. Auth SA JWT RS256→token (WebCrypto), custo Vertex 267 mco (0,15/s), poll fetchPredictOperation, UI de colar o JSON no pool. | 🔒 **Sovereign:** criar service account no projeto `gabrielai-veo` (role Vertex AI User) → JSON → cadastrar no pool nomeado. Depois: `npx supabase functions deploy canvas-execute veo-poll` + `bun run build` + witness pago com o crédito Vertex real |
> 28	| 1 | **Vídeo com avatar/referências no Spaces (Veo 3.1)** — Amendment 25, FR-SPACES-086..091 | ✅ **PROVADO E2E EM PROD 2026-07-14** — deploy (Sovereign) + build (feito) + smoke **12/12** + **witness pago** (gen `02994319`, 720×1280 9:16 8s, **178 mco exatos** 4441→4263, **identidade facial preservada** Vision QA ocular; failover GabrielAI-429→legada funcionou) · nó malha `ccd5dba5` | ⚠️ **OTD-SPACES-046 aberta**: chave nova "GabrielAI" (a do Vertex) com prepaid AI Studio ZERADO (429); o witness rodou na chave legada via failover. Sovereign decide se recarrega a nova em ai.studio/projects |
> 29	| 2 | **Nó de Cadência no Spaces — "além do ManyChat"** (diretiva 2026-07-14) — cadência + automação conversacional p/ TODOS os usuários, BYOK obrigatório, encaixado nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), sem reconstruir | ✅ **BoK 9/9 SELADA 2026-07-15** (`4602b0f`, nó `d0b4fdc8`) — 10 docs + Pattern Conformance (12y/5d/4na); ESTENDE `autopilot_plans` + roteia o tick por `plan_kind` (zero pg_cron novo), reusa `scheduled_posts`/`sequences`/`nurture-dispatch`; inbound IG PROBE-GATED · **✅ Fatia 1 SHIPPADA 2026-07-15** (`6b5412a`, nó `c994c363`): migration `20260716120000` aplicada+verificada · `cadence-plan`/`cadence-run`/tick roteado deployados · `/security-review` NO FINDINGS · smoke 7/7 · build · crítico pegou 2 bugs born-dead pré-deploy | ⏳ Falta: **witness E2E de despacho** (arm→scheduled_posts, via throwaway/UI p/ não publicar real) + Fatia 2 inbound IG (PROBE-GATED FM-CAD-02) |
> 30	| 3 | **Enxame Sensorial-Preditivo (`predictive-swarm`)** — diretiva 2026-07-14, executar **após** o loop atual. Engine de QA sensorial/psicoacústico: design·cinema·marketing como veículos sensoriais integrados. 3 superfícies MCP: `swarm.initialize_sensory_simulation` (enxames paralelos pontuam deriva de percepção) · `vision.parse_sensory_gate` (Tier 1 varredura periférica CPU-bound / pop-out da Feature Integration Theory → Tier 2 foveal só com sinal de alto valor; expande a "Essência Humana") · `mesh.consolidate_sensory_insight` (traços cognitivos → `mcorch_nodes`/`mcorch_edges`, sem PII bruta, proveniência estrita). Gates duros: telemetria+medição por execução atômica · cobrança SÓ via `deduct_mco_coins` per-tenant (ES256 JWKS contra o `sub`) · hard-fail 402/501 estruturado. Fecha com dashboard 🔄 SYNC UPDATE | ✅ **BoK 9/9 SELADA 2026-07-15** (`dc263fc`, nó `485c0f6e`) — 11 docs + Pattern Conformance (15y/6d/0na); MCP molde vision-mcp (ES256 JWKS), 3 superfícies (initialize/parse-gate Tier1 model-free→Tier2 foveal/consolidate), honesto por construção (score=predição, verdade=`creative_metrics.revenue_cents`) · **✅ Fatia 1 SHIPPADA 2026-07-15** (`65a537b`, nó `9ecba7fa`): Tier 1 gates (loudness ffmpeg + contraste WCAG/APCA + verdict) + tool `vision.parse_sensory_gate` VIVOS no container `mcorch_vision_mcp` (healthy, /health anuncia) · crítico pegou 2 blockers (ffmpeg ausente + SSRF redirect) → fechados + hardened · tsc 0 · vitest 121/121 | ⏳ Falta: `swarm:read` no CHECK do PAT allowlist (migration Fatia 2) p/ PAT externo alcançar; Fatia 2 (fan-out/job store) + Fatia 3 (retrieval) |
> 31	| 4 | **AI Act Art. 50(2)** — marcação machine-readable de conteúdo sintético (imagem Nano Banana · vídeo HyperFrames · voz Qwen3) publicado em redes | ✅ **Escopo decidido (3 camadas) + BoK 9/9 SELADA 2026-07-15** (blueprint `531e2b0` + suite `c569416`, nó `825088c0`): C2PA (c2pa-rs) + watermark invisível (TrustMark/VideoSeal/AudioSeal) + metadata IPTC (ExifTool) — todas open-source comercial-safe USD=0; integra no spine `creative_assets` (5 colunas aditivas). Pattern Conformance 12/3/6. | ✅ Gate Closed-Loop ABERTO. **Código = fatia futura com GO Sovereign** (prazo AI Act **2026-08-02**, multa Art.99 €15M/3%) |
> 32	| 5 | **landing-factory** — fábrica de landing pages AUTO-OTIMIZÁVEIS (loop CRO governado), beachhead do norte "agência dentro da plataforma" (2 vídeos Maestros da IA); build → publish → instrumenta PostHog → reverte-se-piora | ✅ **BoK 9/9 SELADA 2026-07-16** (blueprint deepsearch v0.2 + suite `11a5adb`, seal `b65e94b1`; MR14→BR18→PR18→FR20; Pattern Conformance 15/5/1). Decisões Owner: Open Design **v0.10.0 pinado** (single-file export não existe upstream #368) → **asset-bundler próprio** é o P0; hosting **`gcrux.com`** (domínio separado cookie-isolado, nunca `*.mcorch.com`); WordPress-page-first; PostHog self-host/BYOK. **Gate Closed-Loop ABERTO**. | ⏳ **Fatia 1 = código do `landing-bundler`** (inlina img/fonts/@import → data:); registrar wildcard `*.gcrux.com`; OTD-LF-001/003/014 + gate CRO 95% |
> 33	
> 34	**Sprint v6.134.0 — Spaces UX + Run All server-side + controles Veo + motor motion v2 (2026-08-05c)** — 14 commits `333c43f..dc1e53e` · tsc-app 0 · vitest 788 · `/security-review` NO FINDINGS. Run All 100% server-side (Amend 36, fecha a aba) + aviso de sessão + execução seletiva (35) + cards de FASE com botão/resize + skip-success anti re-débito (38) + STOP na fila e nós presos + faxina de projeto (39) + motor motion v2 (ícones de contexto/VFX/seed — 37) + UX (handles verticais, painéis colapsados, full-bleed, RF oculto). EP06 v2 `a65eeb05` armado; 4 presenters Veo falharam por Google high-load e foram estornados (1068 mco). Nó `330e77a3` · malha 20.068. **Pendente durável: poller de página do Veo** (Run All headless não finaliza presenters). ⚠️ **Correção de versão:** a sessão anterior selou como v6.133.0 mas não bumpou o badge do README (ficou em 6.132.0); esta é a v6.134.0.
> 35	
> 36	**Sprint v6.133.0 — Agente do Spaces + esteira do episódio ponta-a-ponta (2026-08-05)** — 19 commits `de5bdb5..9a1fac5` · tsc-app 0 · vitest 765 · `/security-review` NO FINDINGS. Pivô editorial (EP05/A14 guardado; 2 vídeos/semana) + **spaces-agent VIVO** (Amendment 33: chat que monta o canvas, BoK 10/10, sugestões contextuais de custo zero) + **Amendment 34** fechando o gap CLI→UI: nós **Cena Motion** · **Efeito Sonoro** (motor duplo, licença carimbada) · **Montar Master**, todos no `Executar tudo`, com console de execução e barra do agente flutuante. **Repertório profissional** (manual 1.485 l + guia de SFX 386 l + `cinematic-grammar.ts`, 18 regras nos agentes). EP06 com roteiro motion-first (−82% de custo) e 15 narrações IVC (3:24). 5 anticorpos novos — o mais caro: **o autosave da UI apaga escrita server-side**. **Próximo:** o clique em Executar tudo.
> 37	
> 38	**Sprint v6.132.0 — MARATONA EP05 A6→A14 + linguagem MOTION SCENES (2026-08-03/04)** — sessão-maratona iterada por parecer: MASTER A14 COMPLETO na Biblioteca (`6e3175b3`, 488s, QA A/V verde) = VFX título + 19 presenters BLOCKBUSTER (frota 19/19, débito exato 5.073+267+267; QA A/V pegou p47 muda) + 22 cenas-conceito em MOTION SCENES v6 (6 peças na Biblioteca; veredito Sovereign: motion > telas gravadas) + narração 100% voz IVC Sovereign eleven_v3 tom NOVIDADES (EL Creator, pool único provado) + trilha v2 D-major + CTA + créditos template. Síntese: skill `motion-scenes` + contratos (spaces-agent dirige · engineer-spaces executa · creative-director produz) + Scratchpad Harvest = PHASE 1b do /handoff + QA A/V sync como lei + playbook dark-channel + pivô editorial novidades + blueprint ai-news-brief (BoK-gated). Handoff node `2622eece`. **Próximo:** parecer Sovereign no A14 → thumbnail ciano → DOMINGO; retake opcional p14; poda do HANDOFF (WARN 23.8k); spaces-agent segue AGORA gated.
> 39	
> 40	> 📦 Log histórico de sprints v6.129.0 → v6.2.0 (2026-07-30 → 2026-05-04) → [.claude/context/sprint-priorities-archive-2026-08-11.md](sprint-priorities-archive-2026-08-11.md)
> 41	
> 42	---
> 43	
> 44	## 📊 4Cs Audit Snapshot (2026-05-04)
> 45	
> 46	| C            | Pontuação | Lacuna principal                                             |
> 47	|--------------|-----------|--------------------------------------------------------------|
> 48	| Context      | 25/25     | Nenhuma — developer-profile, ADRs, HANDOFF, CLAUDE.md ok    |
> 49	| Connections  | 25/25     | Nenhuma — Chroma + Docker + GitNexus + GitHub MCP ok        |
> 50	| Capabilities | 25/25     | Nenhuma — 7 skills + firecrawl global ok                    |
> 51	| Cadence      | 22/25     | sprint-priorities.md com placeholder de Loop (-3 pts)       |
> 52	
> 53	> Auditoria executada em 2026-05-04. Score total: **97/100** (↑ de 93)
> 54	
> 55	---
> 56	
> 57	## 🔴 Top Gap Closures (by leverage)
> 58	
> 59	1. ~~**Loop/rotina de cadência**~~ ✅ `audit-4cs.sh` toda segunda 09:00 BRT · `auto-publish-cron.sh` */5min · `watchdog` */5min
> 60	2. ~~**Primeiro run Usuário Zero**~~ ✅ Publicado em mcorch.com · LinkedIn + Twitter gerados · pipeline_runs persistido
> 61	3. ~~**`publish-social` realmente publicar**~~ ✅ Bug JWT corrigido · LinkedIn publicando · Twitter: CreditsDepleted (Free tier API X)
> 62	4. **Instagram App Review Meta** — verificação empresarial necessária para produção com terceiros → bloqueante para onboarding clientes (diferir até User 1)
> 63	5. **Twitter API tier upgrade** — Free tier esgotou créditos de escrita. Upgrade para Basic ($100/mês) desbloqueia publicação no X (diferir até User 1)
> 64	6. ~~**Consolidação N+1 queries**~~ ✅ issues #002/#003/#009 resolvidos (2026-05-04)
> 65	7. ~~**Settings Overhaul**~~ ✅ useUserApiKeys + pref_ai_model + mcoCoins RPC + Testar key + ConfigPanel real data (2026-05-05)
> 66	8. ~~**A2UI live em produção**~~ ✅ parseAgentMessage → AIOSTerminal.onMessage (2026-05-07) — surfaces dinâmicas spawnam automaticamente
> 67	9. ~~**Test coverage hooks críticos**~~ ✅ 66 → 122 testes (useOrchestrationGraph + useKnowledgeMesh + useSubscription) (2026-05-07)
> 68	10. ~~**BoK Scribe v1**~~ ✅ 9 docs · ~29k palavras · grounded em código real · selada na mesh (2026-05-07)
> 69	11. ~~**Phase 2 BoK enrichment**~~ ✅ 6 docs enriquecidos (+227 linhas voz estratégica) (2026-05-08)
> 70	12. ~~**Phase 3 BoK → Agents**~~ ✅ 8-agent system gerado (704 linhas) via /bok-agents-generator (2026-05-08)
> 71	13. ~~**Endurecer FMEA-008 + FMEA-011**~~ ✅ validateContent() em orchestrate-content + checklist obrigatório /migration (2026-05-08)
> 72	14. ~~**LGPD data export**~~ ✅ data-export Edge Function + useDataExport hook + UI (2026-05-08)
> 73	15. ~~**Self-service account deletion**~~ ✅ delete_account() RPC + delete-account Edge Function + useDeleteAccount + modal (2026-05-08)
> 74	16. ~~**FMEA-005** (RPN 144) — smart chunked embeddings~~ ✅ Selado 2026-05-08 — `splitChunks()` + batch API + `averageVectors()` · zero truncação silenciosa para nós grandes
> 75	17. ~~**Deploy para produção**~~ ✅ Confirmado 2026-05-08 — data-export + delete-account em produção · migration aplicada
> 76	18. **Phase Commercial** — Stripe live keys + first external user onboarding. Todos os blockers LGPD removidos.
> 77	19. **Redesign completo com base no MIV** — Alinhamento visual da plataforma com a identidade definida no MIV (Three.js, tipografia Editorial, paleta de cores harmoniosa) → OTD-MIV-REDESIGN.
> 78	
> 79	---
> 80	
> 81	## 🛠️ Skills a criar ou evoluir
> 82	
> 83	| Skill | Ação | Gatilho |
> 84	|-------|------|---------|
> 85	| `feature` | Evoluir para incluir scaffold de edge function junto | `/feature` |
> 86	
> 87	---
> 88	
> 89	## 🔌 Conexões a implementar
> 90	
> 91	- [ ] Twitter API Basic tier — upgrade no developer.twitter.com para desbloquear tweet.write
> 92	- [ ] Instagram produção — após App Review Meta (verificação empresarial)
> 93	- [ ] Facebook/Threads — secrets configurados, aguarda App Review
> 94	
> 95	---
> 96	
> 97	## ⏱️ Loop / rotina
> 98	
> 99	**Rotinas ativas no servidor (crontab):**
> 100	
> 101	| Rotina | Schedule | Script | Log |
> 102	|--------|----------|--------|-----|
> 103	| Watchdog containers | `*/5 * * * *` | `scripts/watchdog-mcorch.sh` | `/var/log/mcorch-watchdog.log` |
> 104	| Auto-publish social | `*/5 * * * *` | `scripts/auto-publish-cron.sh` | `/var/log/mcorch-auto-publish.log` |
> 105	| Audit 4Cs semanal | `0 12 * * 1` (seg 09:00 BRT) | `scripts/audit-4cs.sh` | `/var/log/mcorch-audit.log` |
> 106	| AST ingest pós-commit | `0 6 * * *` | `scripts/ingest-codebase.ts` | `/tmp/mcorch-ingest.log` |
> 107	
> 108	---
> 109	
> 110	## 📚 Knowledge Mesh Update
> 111	
> 112	- ~~[ ] Ingerir ADRs de Social OAuth (Twitter PKCE, Instagram Login API v21) como nós `decision`~~ ✅ 5 nós decision/milestone inseridos + embedados via seed-social-oauth-adrs.ts (2026-05-04)
> 113	- ~~[ ] Inserir nó `milestone` para Social OAuth v1 + Pipeline History~~ ✅ Milestone `session-handoff-20260505-settings-sovereignty` inserido e embedado (2026-05-05)
> 114	
> 115	---
> 116	
> 117	## ✅ Definition of Done (por tarefa)
> 118	
> 119	- [ ] Conexão testada com curl ou comando de lista
> 120	- [ ] Skill documentada em `.claude/commands/` com YAML front matter
> 121	- [ ] Nó de conhecimento inserido via `embed-mcorch-node`
> 122	- [ ] Nenhum segredo exposto no repositório (`.env` isolado)
> 123	- [ ] TypeScript: zero erros em `npx tsc --noEmit`
> 124	
> 125	---
> 126	
> 127	## 3Ms deste Sprint
> 128	
> 129	### Mindset (Default Shift)
> 130	- Antes de qualquer tarefa: "Como a IA pode fazer pelo menos 30% disso?"
> 131	- Perguntas de curiosidade: "Por que foi projetado assim? O que quebra se X acontecer?"
> 132	
> 133	### Method (O que vale automatizar)
> 134	- Pipeline social agendado já é autônomo — publicação LinkedIn sem intervenção manual
> 135	- audit-4cs.sh coleta métricas objetivas sem IA — sustentável por anos
> 136	
> 137	### Machine (Assets técnicos ativos)
> 138	- Edge functions: `publish-social`, `auto-publish`, `refresh-social-token`, `orchestrate-content`
> 139	- Crons: watchdog + auto-publish + audit-4cs + ast-ingest
> 140	- mcoCoins por run pipeline: 10 mcoCoins
> 141	
> 142	---
> 143	
> 144	## 🔁 Sprint Retrospective (responder ao final com `/handoff`)
> 145	
> 146	1. Qual tarefa entregou mais % de alavancagem real?
> 147	2. Onde o AIOS me perguntou algo que eu já deveria ter documentado?
> 148	3. Qual foi o maior default shift que pratiquei?
> 149	4. A cadência aumentou ou só criamos mais contexto?
> 150	5. Score 4Cs pós-sprint vs pré-sprint: melhorou em qual C?
> 151	
> 152	---
> 153	
> 154	> ⚠️ **Lembre-se:** produtividade cai antes de subir. O ganho exponencial vem da iteração, não da perfeição inicial. Comece pelo core, evolua.
> 155	
> ```

## 🤖 Claude *(03:25:25)*

<details>
<summary>💭 Thinking Process</summary>

I'm noticing a discrepancy in the HANDOFF.md file — the top block references a seal from August 11th, but the most recent commit is from August 13th, and the sprint priorities row also shows the August 13th seal. Let me trace through which version is actually current.

</details>


## 🤖 Claude *(03:25:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"^#+ .*Record|^# \ud83c\udfaf UPDATE|2026-08-13\" HANDOFF.md | head -40; echo \"---DIFF-PROOF---\"; git diff HEAD -- proof-manifest.json",
  "description": "Locate HANDOFF records and inspect proof-manifest diff"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 8:# 🎯 UPDATE 2026-08-11 (seal 2) — 3 COFRES BLINDADOS · INIT ENXUTO · EP07 ANCORADO E PROVADO
> 44:# 🎯 UPDATE 2026-08-11 — SEGURANÇA, AUDIÊNCIA E ANTICORPOS. Direção segue **EP07**.
> 186:#    5) Reverter as 3 regressões de src/ listadas no Record (asset-url + useCreativeAssets).
> 224:#      (arquivar Records antigos → docs/handoff-archive/) ANTES de adicionar o Record novo.
> 298:| **EP07 em MONTAR: motor v2 · kit por gauntlet · chave no cofre (2026-08-13)** | ✅ **10 commits `d379f86..adc4faa`** · tsc-app **0** · gitleaks limpo ×11 · malha **20.823** · nó `69c02e4b`. **Motor MONTAR v2** spec-driven portado do benchmark aprovado (`fcf91d44`) com 3 correções nascidas de defeito MEDIDO: asset quebrado vira `__fatal` **antes do frame 1** (a 1ª rodada do piloto renderizou 360 frames "verdes" com TODAS as imagens mortas — a família que produziu o master vazio do EP06), **ancoragem uniforme por centro** (metade dos kinds ancorava pelo canto e nasceria deslocada de meia-caixa; provado: 3 larguras diferentes centram com desvio 0,0 px) e `style`/`plain` por camada (VOC-ART-M-004/005 da trupe). **Trupe: 5.324 linhas de Partitura** (5 blocos × 4 lentes), com `durationSec: null` até o ffprobe — o beat cai na PALAVRA. **Gauntlet de peça**: torneio de N variações + recorte com a borda-assinatura; pegou **4 defeitos que geração única esconde** (marca fictícia "AUDIO VOID" · haste cortada pela borda · "Lorem ipsum" legível · tabela de preços em dólar). Gráfico analítico virou **conteúdo da folha** (diretiva), sempre como FORMA — zero dígito. **Pesquisa v2v** (6 frentes + crítico): **recâmera de take real por API NÃO existe provada** (`gen4_aleph` desligado 2026-07-30; Seedance ref é 480p "guide"), e o presenter crível é **lip-sync sobre plate real** — credibilidade = pixels nunca inventados. **Higgsfield: não assinar** (openapi.json com 50 paths e ZERO entrada de vídeo; ToS §11.5 proíbe pass-through). **Vazamento de chave fechado na FONTE**: 3 chaves 403-leaked, origem em **6 nós da malha** — limpar só os 16 arquivos duraria até o cron das 02:30. Credencial saiu do `.env` para o cofre `user_api_keys`; imagem migrada para a **API Google direta**. **Loop de validação em browser** (7/8) provou 22/22 imagens carregando e pegou o rótulo que anunciava "Nano Banana 2" despachando o modelo de 2025. ⚠️ **Veredito do Sovereign no visual: prova de conceito, "ainda amador"** — a régua será um link de cinema na próxima sessão. Record abaixo. |
> 333:## EP07 em MONTAR: motor v2 · kit por gauntlet · chave no cofre Record (2026-08-13)
> 401:## Blindagem 3 cofres · init enxuto · EP07 ancorado e pipeline provado Record (2026-08-11)
> 437:## Segurança, audiência e anticorpos Record (2026-08-11)
> 503:## 📦 Records arquivados
> ---DIFF-PROOF---
> diff --git a/proof-manifest.json b/proof-manifest.json
> index 743357f..ecaf261 100644
> --- a/proof-manifest.json
> +++ b/proof-manifest.json
> @@ -1 +1 @@
> -{"handoffNodeId": "e1d02d45-dde0-4eb6-86b0-1cce5bcb74af"}
> +{"handoffNodeId": "69c02e4b-297c-4eb9-a58f-3fcd518a8d93"}
> ```

## 🤖 Claude *(03:25:32)*

<details>
<summary>💭 Thinking Process</summary>

The proof-manifest.json file is an uncommitted change from the last seal operation that contains a handoff node ID matching the sealed record, so it's benign but should have been committed along with the chore commit. Now I need to examine the most recent Record and the FIRST ACTION tail section to understand the full context.

</details>


## 🤖 Claude *(03:25:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 333,
  "limit": 70
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 333	## EP07 em MONTAR: motor v2 · kit por gauntlet · chave no cofre Record (2026-08-13)
> 334	
> 335	**ORO triplet:** Operator = MCORCH Master Execution Agent (+ trupe criativa: Dramaturgo · Encenador · DoP · Diretor de Arte, 21 agentes em workflow) · Reviewer = Sovereign (gate ocular em cada peça e cena) · Owner = Sovereign — o blast radius é a MARCA do canal: um episódio com número fabricado, marca inventada ou quadro amador custa credibilidade, que é o ativo do formato documentário.
> 336	
> 337	Sessão que levou o EP07 da decisão de linguagem ao kit material — e que fechou um vazamento de credencial na fonte pelo caminho. O Sovereign selou duas decisões de marca no início (**os blocos-herói são em MONTAR**, com a peça `fcf91d44` como referência; **o recorte com borda vira assinatura do canal**, resolvendo A43 §19 D1) e uma no fim que vale mais que as outras: **o resultado visual é prova de conceito, "ainda amador"** — a régua será um link de cinema na próxima sessão.
> 338	
> 339	O fio condutor técnico foi um só: **gate mecânico verde nunca provou que o quadro está certo**. Todos os defeitos materiais desta sessão passaram por baixo de métricas verdes e só caíram no olho — o piloto renderizou 360 frames com bit_rate e frames-únicos perfeitos e **todas as imagens mortas**; a cena da pilha passou nos 4 gates e ainda assim lia como 2 objetos onde a tese pede 100 pessoas; o rótulo do modelo mentia em produção sem quebrar teste nenhum.
> 340	
> 341	| Ação | Resultado |
> 342	|--------|--------|
> 343	| `scripts/motion/montar-template-v2.mjs` | ✅ Motor MONTAR de produção: câmera por estações · planos Z nomeados · foco viajante com `dof(z)` por FOLHA · `rotateY` real (armadilha preserve-3d respeitada) · 9 kinds (slab·cutout·chip·badge·data·splitbar·timeline·counter·stamp) |
> 344	| **G5 — asset morto vira `__fatal`** | ✅ Antes do frame 1, com a lista dos assets. Nasceu de 360 frames "verdes" com `ERR_FILE_NOT_FOUND` em todas as imagens |
> 345	| **Ancoragem uniforme por centro** | ✅ Achado do Diretor de Arte: `cutout/chip/badge/counter/stamp` ancoravam pelo canto e as 4 lentes escrevem centros. Provado: larguras 61/199/193 px centram com **desvio 0,0 px** (antes 30/99/96) |
> 346	| `docs/roadmap/ep07-partituras/` | ✅ **5.324 linhas** — 5 blocos × 4 lentes + prompts Veo. `durationSec: null` até o ffprobe; zero número novo; lacunas registradas |
> 347	| `scripts/ep07/gauntlet-piece.ts` | ✅ Torneio de peça: N variações → recorte com a borda → contact sheet na Biblioteca. Pegou 4 defeitos invisíveis a geração única |
> 348	| **Gráfico analítico DENTRO da folha** | ✅ Correção de rumo do Sovereign: o gráfico é conteúdo do papel, vive no prompt de GERAÇÃO. Sempre como FORMA — zero dígito, eixo, legenda ou moeda |
> 349	| `docs/roadmap/motor-video-decisao-v2v-2026-08-12.md` | ✅ 535 linhas · 6 frentes + crítico. **Recâmera por API não existe provada**; presenter crível = lip-sync sobre plate real; Higgsfield não se assina (ToS §11.5) |
> 350	| **Vazamento de chave fechado na FONTE** | ✅ 3 chaves 403-leaked; origem em **6 nós da malha** (`vault_note` do Obsidian). Limpar só os 16 arquivos duraria até o cron das 02:30 |
> 351	| `scripts/qa/set-google-key.sh` + `probe-google-key.ts` | ✅ Grava com gate de vida + gate de IMAGEM antes de escrever, relê para conferir, limpa o `.env`. O probe cala quando o host está limpo |
> 352	| `scripts/lib/gemini-image.ts` | ✅ Imagem pela **API Google direta** (diretiva); chave lida do COFRE `user_api_keys`, `.env` só como fallback com aviso |
> 353	| `scripts/qa/e2e-session-validation.ts` | ✅ Loop em browser autenticado (7/8): 22/22 imagens carregando, URLs assinadas OK, e o **rótulo falso** pego em `src/types/canvas.ts:207` |
> 354	| **Kit colhido** | ✅ 19 recortes + 21 specs + 2 cenas → `repurpose-inbox/<uid>/ep07-kit/` (43 MB, fora do git, sobrevive a reboot) |
> 355	
> 356	| Commit | Conteúdo |
> 357	|--------|----------|
> 358	| `cea40b0` | feat(motion): motor MONTAR v2 — o benchmark aprovado vira motor de produção |
> 359	| `0bb7a67` | feat(ep07): runners de produção — piloto com gate triplo, render de cenas e gauntlet |
> 360	| `ec69911` | docs(ep07): partituras da trupe (5 blocos × 4 lentes) + as duas decisões seladas |
> 361	| `d379f86` | docs(roadmap): decisão de motor v2v — a recâmera por API não existe |
> 362	| `55de59e` | feat(image): imagem passa a sair pela API Gemini/Google direta |
> 363	| `6f3c487` | feat(security): fecha o vazamento de chave Google e move a credencial para o cofre |
> 364	| `71944f9` | test(qa): loop de validação em browser autenticado — e o rótulo que ele pegou mentindo |
> 365	| `1f57fbc` | fix(qa): grava a chave por PATCH — view mascarada não aceita upsert |
> 366	| `e6b174c` | fix(ep07): peça de papel para de vir com texto legível — não peça texto, descreva a ausência |
> 367	| `45c2627` | feat(ep07): a pilha usa TODAS as variações + peças analíticas + GO no gancho |
> 368	| `4c6cf30` | fix(ep07): o gráfico analítico vive DENTRO da folha — e a pilha vira leque |
> 369	| `adc4faa` | docs(readme): v6.140.0 |
> 370	
> 371	### Arquitetura EP07 · MONTAR ponta a ponta
> 372	
> 373	```
> 374	Partitura de Cena v1 (trupe: Dramaturgo→Encenador→DoP→Arte)
> 375	   │  vocabulário FECHADO · beat na PALAVRA · zero número novo
> 376	   ▼
> 377	gauntlet-piece.ts ── N variações (Nano Banana 2, API Google DIRETA)
> 378	   │                  prompt cirúrgico: objeto inteiro · fundo liso · luz lateral
> 379	   │                  · ZERO texto/marca · gráfico como FORMA
> 380	   ├─► matte.py u2net --stroke 12 ──► borda branca = ASSINATURA do canal (A43 D1)
> 381	   └─► contact sheet ──► Biblioteca ──► gate OCULAR do Sovereign (escolhe 1)
> 382	                                          │
> 383	   spec.json (planes Z · camera.keyframes · focus.stations · layers[])
> 384	                                          ▼
> 385	              montar-template-v2.mjs ──► __seek(t) determinístico
> 386	                                          │  G5: asset morto = fatal ANTES do frame 1
> 387	                                          ▼
> 388	              Playwright (1 chromium) ──► FFmpeg ──► MP4 1080p
> 389	                                          │
> 390	              gates: perspectiva ≥1,05 · dof ≥3 planos · bitrate ≥800k · ≥95% únicos
> 391	                                          ▼
> 392	                              gate OCULAR ← o único que reprovou nesta sessão
> 393	```
> 394	
> 395	**Scratchpad da sessão:** `/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/9b9cb2fa-663b-4f25-98b8-c32877cbffb1/scratchpad` (954 MB). **Promovido:** 6 runners (`scripts/motion/montar-template-v2.mjs`, `scripts/ep07/{pilot-adsense-montar,render-scenes-montar,gauntlet-piece,scene-estrutura-pilha,gen-photo-briefs}.ts`) + 3 ferramentas de credencial/QA (`scripts/lib/gemini-image.ts`, `scripts/qa/{set-google-key.sh,probe-google-key.ts,e2e-session-validation.ts}`) + **kit material** (19 recortes com alpha + 21 prompts + 2 cenas → `repurpose-inbox/<uid>/ep07-kit/`, 43 MB, fora do git). **Na Biblioteca** (favoritos + tag `ep07`): piloto `56af51b9` · cena da pilha `4e73a41e` · 6 gauntlets · folha de briefing `665d058c`. **Descartável:** ~900 MB de frames PNG intermediários e HTMLs de cena — regeneráveis pelos `spec.json` promovidos.
> 396	
> 397	**Survival Laws Self-audit:** Lei 1 ✅ — toda claim com prova citada (gates com número medido, UUID de asset por SELECT, hashes de commit, HTTP status). **Três vezes evitei reportar falso-sucesso:** o piloto "verde" com todas as imagens mortas (pego por probe de `naturalWidth`), o `.mp4` de 3 minutos antes que eu quase apresentei como render novo (pego por `stat` do timestamp), e o probe acusando as chaves que ele mesmo limpou. **Corrigi 2 gates MEUS que estavam errados** — `readyState>0` num player com `preload="none"` e `ERR_ABORTED` contado como falha. Lei 2 ✅ — SOP de decisão (`motor-video-decisao-v2v`) escrito ANTES de qualquer código de v2v; a diretiva de imagem virou helper canônico antes de migrar os runners. Lei 3 ✅ — 1 poda (23.568 → 19.750 tokens, byte-idêntica, G5 provado). Lei 4 ✅ — ORO declarado; nenhum gasto pago executado sem GO (os 2 Veo seguem não-gerados aguardando o gate G-VEO-1 no TTS grátis).
> 398	
> 399	**Pendências que a próxima sessão herda:** (1) o **link de cinema** do Sovereign é a régua — decompor ANTES de escrever código (planos, duração, luz, o que se move); (2) re-renderizar a pilha com o leque + as folhas com gráfico; (3) escolher 1 variação por peça; (4) gancho/fecho com Veo dizendo só a frase que precisa de rosto (GO dado); (5) `85aaca76` tem `google_api_key` inválida (tenant de QA).
> 400	
> 401	## Blindagem 3 cofres · init enxuto · EP07 ancorado e pipeline provado Record (2026-08-11)
> 402	
> ```

## 🤖 Claude *(03:25:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 160,
  "limit": 80
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 160	#    **4.675.413 bytes · 154,000s · 0 camadas · 0 narração**. Nenhum blob de 13,9 MB existe no
> 161	#    disco nem no histórico do git (único commit: 8a45d06).
> 162	#
> 163	# 🌾 ACERVO COLHIDO E SALVO (o que sobrou de bom do EP06 — reaproveitar, não refazer):
> 164	#    repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep06-montar-harvest/  (780 MB, 5.283 arq.)
> 165	#    Estava num /tmp de sessão ENCERRADA e sobreviveu por sorte. Colhido nesta sessão, verificado:
> 166	#      • clips/mot-c01..c14.mp4 — 14 cenas MONTAR reais 1920×1080 ~1 Mbps (c01=15,20s · c07=12,10s · c14=4,90s)
> 167	#      • clips/*voice*.mp3 — 12 narrações ElevenLabs REAIS (c01=14,81s / 250.848 B)
> 168	#      • clips/veo-p1.mp4 — presenter POV academia com áudio nativo (8,00s / 5.249.193 B)
> 169	#      • ep06-master.mp4 — o master v3.2 (23.572.524 B) + contact sheets de QA
> 170	#    ⚠️ NÃO mover para public/ (vira docroot público + entra no git + infla o dist a cada deploy).
> 171	#
> 172	# 🧭 ORDEM RECOMENDADA PARA A PRÓXIMA SESSÃO (do diagnóstico de 13 agentes):
> 173	#    1) Sovereign restaura a secret key (acima) — sem isso NADA de banco/render funciona.
> 174	#    2) `deepsearch-blueprint` ancora os 12 números da pauta EP07 (gate declarado na própria pauta).
> 175	#    3) ELEVAR O MOTOR antes de produzir: portar de scripts/motion/layered/build-scene.mjs para
> 176	#       scripts/ep06/montar-scene-template.mjs → a função dof(z)+focus, o mapa de planos nomeados,
> 177	#       bloom/nebula/vignette; e POPULAR `companions[]` por cena com camadas REAIS (screenshot do
> 178	#       nosso produto, PNG recortado com u2net, SVG de marca). Piloto em UMA cena antes das outras.
> 179	#       GATE TRIPLO: (a) contact sheet a olho com ≥3 planos de desfoque distinto; (b) bit_rate de
> 180	#       vídeo ≥ 800.000 (o v4 tem 41.953); (c) framemd5 com ≥95% de frames únicos (v4: 299/4620).
> 181	#       Cena aprovada legível em código: repurpose-inbox/ada39fae-motion-spike/scene.html
> 182	#    4) Montar SEMPRE com scripts/ep06/assemble-master.ts (fail-closed, SDK autenticado,
> 183	#       `process.exit(2)` em cada insumo faltante) — NUNCA com os assemblers do Antigravity.
> 184	#       GATE DE ÁUDIO: duração ≠ múltiplo exato de 7 · RMS trough ≤ -80 dB · crest ≥ 10 dB ·
> 185	#       silencedetect com ≥20 eventos (fala tem pausa; o v4 tem trough -19,35 e crest 3,3).
> 186	#    5) Reverter as 3 regressões de src/ listadas no Record (asset-url + useCreativeAssets).
> 187	#
> 188	# 🚀 UPDATE 2026-08-07 (EP06 v3.1 ARMADO · ElevenLabs + motion-promo + canvas defensivo): commits 4b7e0e3..890954a.
> 189	#   ⏭ PRÓXIMO: o Sovereign clica em Executar tudo no projeto 441a5f04-fab7-437e-8969-13cfc7c0295d.
> 190	#      Passo-a-passo abaixo:
> 191	#      1) escutar 1 narração ElevenLabs na Biblioteca ("EP06 v3.2 · c01-gancho")
> 192	#      2) gerar filme motion-promo (skill instalada) 8s/16:9 → subir na Biblioteca → anexar em C1
> 193	#      3) escolher screenshot da estrutura Agent Plugins em C4 e do slider ChatGPT em C10
> 194	#      4) clicar Executar em cada Veo (P1 gancho · P2 apresentador · P4 CTA) — ~801 mco
> 195	#      5) clicar "Executar tudo" (0 mco extra) — 14 cenas + master
> 196	#      6) intro/outro pelo HyperFrames Studio /dashboard/canvas/video
> 197	#   ✅ ENTREGUE: 12 narrações ElevenLabs (perfil 867e95b9 clonado do EP06 antigo, timbre eleven_v3);
> 198	#      skill motion-promo em .claude/skills/motion-promo/; gancho C01/C13 reescritos p/ apontar a
> 199	#      skill; 2 crashes do canvas consertados na FONTE (useCanvasStore.initialize força type=kind,
> 200	#      ImageToVideoNode.backendBadge com guard); schema Veo corrigido (videoModel/veoResolution/
> 201	#      aspectRatio/duration alinhados com v3 antigo).
> 202	#   ⚠️ AUTOSAVE DA UI clobbera escrita server-side — se for editar o grafo, FECHE a aba primeiro.
> 203	#
> 204	# 🚀 UPDATE 2026-08-05c (SPACES UX + RUN ALL SERVER-SIDE + CONTROLES VEO + MOTOR MOTION v2): commits 333c43f..e8b489d.
> 205	#   ⏭ PRÓXIMO (2 frentes, ambas do EP06 v2 `a65eeb05`):
> 206	#   1) 🐛 CORREÇÃO DURÁVEL — poller de PÁGINA do Veo. O Run All de presenters TRAVA: useVeoPoll só
> 207	#      roda no inspector aberto → num Run All headless ninguém chama veo-poll → gerações ficam
> 208	#      'running' eternas (mesmo já concluídas/falhas no Google) e os nós presos. runSingleNode (Veo)
> 209	#      TAMBÉM não grava veoGenerationId no nó. Fix: gravar o generationId no dispatch + um hook de
> 210	#      página (molde useMotionRenderSync) que faz poll dos imageToVideo running e reconcilia.
> 211	#   2) 🔎 AUDITORIA VEO (pedido do Sovereign) — conferir cobrança/estorno. Nesta sessão os 4 presenters
> 212	#      do EP06 v2 FALHARAM por Google 'high load' e foram INTEGRALMENTE ESTORNADOS (267×4=1068 mco,
> 213	#      saldo 44394 intacto). Runner: `scripts/qa/recover-stuck-veo.ts <project_id>` finaliza/estorna
> 214	#      presos. Re-tentar o Passo A quando o Veo do Google não estiver sobrecarregado.
> 215	#   ✅ ENTREGUE nesta sessão (tudo no ar): Run All 100% server-side (fecha a aba, o master monta —
> 216	#      Amend 36) + aviso de sessão p/ nós pagos + execução seletiva (Amend 35) + cards de FASE com
> 217	#      botão próprio/resize + skip-success anti re-débito (Amend 38) + STOP na fila E nos nós presos +
> 218	#      faxina de projeto (Amend 39) + motor motion v2 (ícones de contexto/VFX/seed — Amend 37) +
> 219	#      handles de fluxo vertical + painéis colapsados + full-bleed + marca RF oculta.
> 220	#   EP06 v2 `a65eeb05` = esteira limpa (P1·4 cenas·P2·3 cenas·P3·6 cenas·P4 + master centro-baixo),
> 221	#   3 narrações marcadas REGERAR (texto v2 embutido), presenters resetados a idle.
> 222	#   ⚠️ autosave da UI clobbera escrita server-side — TODO script de grafo usa guard de updated_at.
> 223	#   ⚠️ DÍVIDA: HANDOFF em 🟡 WARN (23.7k tokens, folga ~0 records) — o PRÓXIMO /handoff DEVE PODAR
> 224	#      (arquivar Records antigos → docs/handoff-archive/) ANTES de adicionar o Record novo.
> 225	#
> 226	# 🚀 UPDATE 2026-08-05 (AGENTE DO SPACES + esteira do episódio ponta-a-ponta): 19 commits de5bdb5..9a1fac5.
> 227	#   ✅ ARRANQUE DO PRÓXIMO PASSO: abrir /dashboard/spaces/d0d82aeb-8c98-4e36-b526-b6bba64a4db5,
> 228	#   dar Ctrl+Shift+R (build novo) e clicar em **EXECUTAR TUDO**. O projeto está ARMADO e AUDITADO
> 229	#   (4 gates verdes): 8 cenas motion com 3-4 beats e duração ditada pela narração (Gancho 22s ·
> 230	#   Incidentes 32s · Kimi K3 30s) · 9 nós de voz (8 com áudio IVC) · montador "Master EP06" ligado
> 231	#   às 8 cenas · fila limpa · 44.395 mco. É o 1º teste E2E do ciclo Executar tudo → MASTER.
> 232	# ⚠️ ANTES DE CLICAR: recarregue a página. O autosave da UI SOBRESCREVE escrita server-side
> 233	#   (last-write-wins, debounce 3s, sem comparar updated_at) — foi o que estragou o 1º lote de
> 234	#   renders (saíram com beats=0 e 10s). Memória reference_canvas_autosave_clobbers_server_writes.
> 235	# 🆕 NÓS NOVOS no Spaces: Cena Motion (grátis, Playwright+FFmpeg) · Efeito Sonoro (motor DUPLO:
> 236	#   síntese FFmpeg 0 mco / IA ElevenLabs 2 mco) · Montar Master (grátis) · inspector da Nota de cena.
> 237	#   Console de execução (fila·%·tempo) e barra do agente flutuante dividem o rodapé (botão Agente ↔ X).
> 238	# 📚 REPERTÓRIO: docs/processes/repertorio-producao-profissional.md (1.485 l) + biblioteca-sfx-como-farmar.md
> 239	#   (386 l) + src/lib/cinematic-grammar.ts. 18 regras injetadas no spaces-agent/motion-scenes/creative-director.
> ```

## 🤖 Claude *(03:25:39)*

<details>
<summary>💭 Thinking Process</summary>

Let me verify the mesh node count from the HANDOFF record shows 20,823 nodes, then check that the scratchpad session directory still exists with its 954 MB size and the ep07-kit. I'll also run a quick BoK gate check using the command loop since it's inexpensive.

</details>


## 🤖 Claude *(03:25:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  if [ \"$slug\" = \"security\" ]; then\n    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)\n    missing=(); for doc in \"${required_sec[@]}\"; do [ -f \"docs/bok/security/$doc.md\" ] || missing+=(\"$doc\"); done\n    [ ${#missing[@]} -eq 0 ] && echo \"OK security\" || echo \"INCOMPLETE security: ${missing[*]}\"; continue\n  fi\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=(); for doc in \"${required[@]}\"; do [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\"); done\n  [ ${#missing[@]} -eq 0 ] || echo \"INCOMPLETE $slug: ${missing[*]}\"\ndone; echo \"=== fim (s\u00f3 incompletas listadas) ===\"",
  "description": "BoK completeness gate"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> INCOMPLETE mco-monetization: 06-data-model 07-process-flow 08-quality-metrics
> OK security
> === fim (só incompletas listadas) ===
> ```

## 🤖 Claude *(03:25:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/9b9cb2fa-663b-4f25-98b8-c32877cbffb1/scratchpad 2>/dev/null | head -5 || echo \"SCRATCHPAD_ANTERIOR_MORTO\"; echo \"---KIT---\"; du -sh /home/gcrUX/htdocs/constellation-orchestra/repurpose-inbox/ada39fae-*/ep07-kit 2>/dev/null || ls -d /home/gcrUX/htdocs/constellation-orchestra/repurpose-inbox/*/ep07-kit 2>/dev/null || echo \"KIT_NAO_ENCONTRADO\"; echo \"---SCENE-SPECS---\"; ls /home/gcrUX/htdocs/constellation-orchestra/scripts/ep07/ 2>/dev/null",
  "description": "Check previous scratchpad + ep07 kit + runners"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 2172
> drwx------ 10 ubuntu ubuntu   4096 Aug 13 21:03 .
> drwx------  4 ubuntu ubuntu   4096 Aug 11 12:53 ..
> drwxrwxr-x  2 ubuntu ubuntu   4096 Aug 12 17:48 e2e-validation
> drwxrwxr-x  2 ubuntu ubuntu   4096 Aug 11 23:47 ep07-briefs
> ---KIT---
> 43M	/home/gcrUX/htdocs/constellation-orchestra/repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep07-kit
> ---SCENE-SPECS---
> gauntlet-piece.ts
> gen-photo-briefs.ts
> pilot-adsense-montar.ts
> pilot-adsense-scene.ts
> render-scenes-montar.ts
> render-scenes.ts
> scene-estrutura-pilha.ts
> ```

## 🤖 Claude *(03:25:55)*

<details>
<summary>💭 Thinking Process</summary>

The mco-monetization BoK is incomplete with only 6 of 9 items done, though the sprint notes indicate it's gated pending the SOP documentation and some OTD-MON decisions. I'm checking the gate status in the index to confirm the exact missing pieces.

</details>


## 🤖 Claude *(03:25:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/mco-monetization/; echo \"---GATE---\"; grep -iE \"gate status|gate.*fechad|gate.*abert\" docs/bok/mco-monetization/00-index.md 2>/dev/null | head -8",
  "description": "mco-monetization suite files + gate status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 09-pattern-conformance.md
> ---GATE---
> ## 1. GATE STATUS (leia isto antes de escrever qualquer linha de código)
> | [`00-index.md`](00-index.md) | 0 | — | [x] este | Manifesto · GATE STATUS · ID space · rastreabilidade mestre · escopo negativo |
> ```

## 🤖 Claude *(03:25:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '1,40p' docs/bok/mco-monetization/00-index.md",
  "description": "Read mco-monetization gate status block"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # mco-monetization — BoK Documentation Suite (00-index)
> 
> **Project slug:** `mco-monetization`
> **Version:** v1.0 · **Data:** 2026-08-11
> **Escopo:** recarga avulsa de mcoCoins (top-up) + política de preço sob BYOK
> **Market segment:** B2C prosumer não-técnico (beachhead: as duas primeiras usuárias pagantes reais)
> **Monetization:** este módulo **É** a monetização — não a consome
> **Regulatory profile:** CDC (crédito pré-pago) · LGPD (dado de pagamento e erasure) · obrigação de trilha fiscal
> **Integration surface:** `extends-mcorch` — estende `profiles.mco_balance`, `mcoin_transactions`, `stripe-webhook`, `create-checkout` e a calibração 4×-floor (`docs/processes/mcoin-cost-calibration.md`)
> 
> **ORO triplet da suíte:**
> - **Operator:** MCORCH Master Execution Agent (autoria: `bok-curator`)
> - **Reviewer:** Sovereign (Gabriel) — módulo de **dinheiro real de terceiros**, revisão não delegável
> - **Owner:** Sovereign — absorve o prejuízo material (cunhagem, chargeback, churn das duas primeiras pagantes)
> 
> ---
> 
> ## 1. GATE STATUS (leia isto antes de escrever qualquer linha de código)
> 
> > **A suíte estar 6/6 NÃO abre o gate.** O que abre o gate é o quadro abaixo, fatia a fatia.
> 
> | Fatia | Conteúdo | Gate Closed-Loop | Bloqueio |
> |---|---|:--:|---|
> | **0 — Saneamento do caminho de dinheiro** | webhook fail-closed · webhook para de SETAR saldo · 3 RPCs de refund passam a escrever ledger · reconciliador de drift · `credits` para de ser LIDO · hardening de `delete_account` | 🟡 **ABERTO CONDICIONADO** | Requer o SOP `docs/processes/mcoin-topup.md` (Lei 2 — **NÃO EXISTE**, verificado por `ls` em 2026-08-11) + `/security-review` por migration. Nenhuma decisão de negócio pendente: é conserto de defeito conhecido |
> | **1 — A recarga** | `mco_packages` · `stripe_webhook_events` · `mco_topups` · `credit_mco_topup` · `create-checkout` estendida · ramo de recarga no webhook · UI | 🔴 **FECHADO** | OTD-MON-001 (test×live), OTD-MON-002 (endpoint/eventos no painel), OTD-MON-004 (preços dos pacotes), OTD-MON-009 (semântica da renovação), OTD-MON-018 (recarga sem plano). **E** gate de saída da Fatia 0: `drift = 0` provado por query |
> | **2 — Estorno e disputa** | `reverse_mco_topup` · handlers `charge.refunded` / `charge.dispute.*` · teto por janela | 🔴 **FECHADO** | OTD-MON-006 (política de estorno + congelamento manual) |
> | **3 — Instrumentação de `key_source`** | `key_source` no `context` de toda linha de gasto (19 edge fns com fallback global) | 🟡 **ABERTO CONDICIONADO** | Sem decisão de negócio pendente — é telemetria aditiva. Requer SOP e é **pré-requisito duro** da Fatia 4 |
> | **4 — Recalibração BYOK** | `src/lib/pricing.ts` (SSOT) · fórmula tri-componente · teste de paridade genérico | 🔴 **FECHADO** | OTD-MON-010 (multiplicador 20%), OTD-MON-011 (teto de vídeo), OTD-MON-013 (os 3 caminhos que hoje zeram). **E** ≥1 ciclo de medição da Fatia 3 |
> | **5 — `fee_host`** | rails self-host saem de `charged_mco: 0` | 🔴 **FECHADO** | OTD-MON-012 — **Lei 1: nenhum rail sai do zero sem o seu bench.** 5 rails medidos, 4 não medidos |
> | **6 — Limpeza** | `credits` DROP · catálogo de preço em banco | 🔴 **FECHADO** | OTD-MON-008 (destino de `credits`), OTD-MON-015 (catálogo em banco) |
> 
> **Regra-mãe deste gate (Lei 1):** o sinal de sucesso de qualquer fatia de dinheiro é o **SALDO no banco**, nunca o HTTP 200 do webhook. O código atual responde 200 para uma compra avulsa que ele ignora inteiramente (`stripe-webhook/index.ts:117` + `:131`, verificado) — provando que 200 e dinheiro são coisas independentes nesta superfície.
> 
> ---
> 
> ## 2. Registro de arquivos
> 
> | Arquivo | Fase | Lente BoK | Status | Conteúdo |
> |---|:--:|---|:--:|---|
> | [`00-index.md`](00-index.md) | 0 | — | [x] este | Manifesto · GATE STATUS · ID space · rastreabilidade mestre · escopo negativo |
> ```

## 🤖 Claude *(03:26:16)*

<details>
<summary>💭 Thinking Process</summary>

The mco-monetization suite is intentionally scoped at 6/6, so that's not an incomplete gate issue—the index confirms it's meant to stay that way. Now I'm ready to write up the brief with the key details: the last sealed phase from August 2026 involving the motor v2 and kit setup, plus the commit reference.

Looking at the current state, I have the mesh topology at 20.823 nodes with edges last measured at 24.949 during the August 11 seal, TypeScript compiling cleanly with zero errors, and the Book of Knowledge matching expectations except for the intentional mco-monetization deviation. The sprint is tracking EP07, and the immediate blockers are the cinema reference link needed for the first item and an uncommitted proof-manifest.json file that's a leftover from the sealed node. There's also a tenant QA issue flagged with an invalid key that needs attention.

Now checking the environment — the scratch directory is actually clean despite earlier warnings, but there are 42 accumulated scratchpad sessions in /tmp that could be consuming disk space. I should verify whether this is material enough to warrant cleanup before moving forward.

</details>


## 🤖 Claude *(03:26:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "du -sh /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/ 2>/dev/null; df -h / | tail -1",
  "description": "Scratchpad disk footprint and root usage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 6.6G	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/
> /dev/sda1       193G  148G   45G  77% /
> ```

## 🤖 Claude *(03:26:19)*

<details>
<summary>💭 Thinking Process</summary>

Time to draft the brief.

</details>


## 🤖 Claude *(03:26:49)*

```
═══════════════════════════════════════════════════════════
  HANDSON — EP07 EM MONTAR: motor v2 · kit por gauntlet · chave no cofre (2026-08-13)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
Fase selada: **EP07 em MONTAR — motor v2 · kit por gauntlet · chave no cofre** (2026-08-13, nó de malha `69c02e4b`)

```
6bbe8d8 — chore(sprint): registra o seal de 2026-08-13
b74fe03 — docs(handoff): ORO + self-audit das 4 Leis + colheita do scratchpad
41adebf — docs(handoff): seal EP07 em MONTAR
895b461 — chore(handoff): arquiva o record de 2026-08-10 (gate de tamanho, 0 folga)
adc4faa — docs(readme): v6.140.0
```

📂 **MUDANÇAS PENDENTES**
`M proof-manifest.json` — 1 linha: `handoffNodeId` `e1d02d45` → `69c02e4b`. É resíduo do próprio seal (o id bate com o nó da malha do Record de 08-13); ficou de fora do commit `6bbe8d8`. Benigno, mas sujo.

🏗️ **INFRA** — tudo verde, 7 dias de uptime
```
mcorch_chroma        Up 7 days (healthy)   API v2 heartbeat: OK
mcorch_claude_mem    Up 7 days (healthy)
mcorch_vision_mcp    Up 7 days (healthy)
mega-brain-daemon    Up 7 days (healthy) · webhook (healthy) · dashboard Up
```

🧠 **KNOWLEDGE MESH**
**20.823 nós** (Record 2026-08-13). Arestas: última contagem registrada **24.949** (seal de 08-11, quando a malha tinha 20.425 nós) — o Record novo não recontou arestas.

🔧 **TYPESCRIPT**
`npx tsc -p tsconfig.app.json --noEmit` → **exit 0, zero linhas de saída** ✅ (gate real da app, não o `tsc` da raiz)

📚 **BoK SUITES** (40 suítes)
Todas com os 9 docs canônicos, **exceto uma — e por desenho**: `mco-monetization` tem 6/6 (00–05 + 09-pattern-conformance). O próprio `00-index.md` declara: *"A suíte estar 6/6 NÃO abre o gate"* — o gate é **por fatia**: Fatia 0 e 3 🟡 ABERTAS CONDICIONADAS (dependem do SOP `docs/processes/mcoin-topup.md`, que **não existe**), Fatias 1/2/4/5/6 🔴 FECHADAS por decisões OTD-MON de preço/política — **mão do Sovereign**.
Nenhum bloqueador de BoK para o trabalho de EP07 (produção de conteúdo, não módulo novo).

📌 **SPRINT**
Goal: **EP07 "economia dos videocasts"** ancorado e produzido com o motor MONTAR elevado.
Top gap: o **veredito ocular do Sovereign** — *"prova de conceito, ainda amador"*. Todos os gates mecânicos estavam verdes; o quadro é que não passou.

⚡ **PRÓXIMOS PASSOS** (herdados do Record, na ordem que ele deixou)
1. **O link de cinema é a régua** — o Sovereign ficou de mandar a referência. O Record manda **decompor antes de escrever código** (planos, duração, luz, o que se move). É a entrada bloqueante do item 2.
2. **Re-renderizar** a cena da pilha com o leque + as folhas com o gráfico analítico dentro do papel.
3. **Escolher 1 variação por peça** (os 6 gauntlets estão na Biblioteca com tag `ep07`, gate ocular).
4. **Gancho e fecho com Veo** — só a frase que precisa de rosto. GO de gasto já dado; os 2 seguem não-gerados.
5. Menor: tenant de QA `85aaca76` com `google_api_key` inválida.

**Material da sessão anterior está vivo** ✅ — kit em `repurpose-inbox/ada39fae-.../ep07-kit` (43 MB, 19 recortes + 21 specs + 2 cenas), 7 runners em [scripts/ep07/](scripts/ep07/), motor em [scripts/motion/montar-template-v2.mjs](scripts/motion/montar-template-v2.mjs). Nada precisa ser regerado com custo.

⚠️ **ALERTAS**
- 🔴 **Bloqueio de entrada:** o passo 1 depende do **link de referência do Sovereign**. Sem ele, refinar o visual é adivinhação — e o Record é explícito em que gate verde ≠ quadro certo.
- 🟡 `proof-manifest.json` sujo no worktree (não commito sem sua palavra).
- 🟡 **Disco:** `/tmp/claude-1001/<projeto>` acumulou **6,6 GB** em **42 sessões**; raiz em **77%** (148G/193G). Não é urgente, mas a colheita de scratchpad não vem acompanhada de poda.
- ℹ️ `scratch/` limpo · HANDOFF.md em **516 linhas** (a poda de 08-11 funcionou) · gitleaks foi verde no último seal.
- ℹ️ Vários conectores MCP (Figma, Linear, Slack, Notion…) pedem OAuth e esta sessão é não-interativa — autorize pelas configurações de conectores do claude.ai ou por `claude mcp` num terminal interativo, se precisar deles.

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

Se quiser, disparo o **`pmo-curator`** (MAPE-K de progresso, plan-only) para materializar o backlog priorizado em `NEXT-STEPS.md` separando o que é executável já do que precisa da sua mão — o atual está de 2026-07-29, bem defasado.

## 👤 User *(03:38:03)*

ok resolva os alertas, quando estiver rodando a analise dos link.: https://higgsfield.ai/@higgsfield.studio/projects/oneiric e https://higgsfield.ai/@higgsfield.studio/projects/cully-hill-boys

ok melhore o next steps conforme solucionando os problenas identificados nos alertas deste handson

## 🤖 Claude *(03:38:08)*

I'll resolve the alerts and analyze the two Higgsfield references in parallel.

## 🤖 Claude *(03:38:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log -1 --format='%H %s' -- proof-manifest.json && echo \"---MANIFEST-ATUAL---\" && cat proof-manifest.json && echo \"\" && echo \"---QUEM-LE---\" && grep -rn \"proof-manifest\" --include=\"*.ts\" --include=\"*.sh\" --include=\"*.md\" scripts/ .claude/ 2>/dev/null | head -10",
  "description": "Investigate proof-manifest provenance and consumers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 0813640f48949ee44f004ff7426269711c2c5e57 chore(sprint): registra o seal 2 de 2026-08-11 (3 cofres · init · EP07) + proof manifest
> ---MANIFEST-ATUAL---
> {"handoffNodeId": "69c02e4b-297c-4eb9-a58f-3fcd518a8d93"}
> 
> ---QUEM-LE---
> scripts/qa/types.ts:30:   * Set for unambiguous claims (e.g. a mesh UUID from proof-manifest.json);
> scripts/ep06/insert-handoff-node.ts:49:  writeFileSync("proof-manifest.json", JSON.stringify({ handoffNodeId: nodeId, sealedAt: new Date().toISOString() }, null, 2));
> scripts/qa/extract-manifest.ts:4:// proof-manifest.json), produce the list of ProofClaim to verify. No `node:`
> scripts/qa/extract-manifest.ts:232: * Parse an optional proof-manifest.json string (emitted by /handoff Phase 3)
> scripts/qa/extract-manifest.ts:252:      raw: `proof-manifest.json:handoffNodeId=${nodeId}`,
> scripts/qa/extract-manifest.ts:263: * `manifestJson` is the optional proof-manifest.json text (hybrid input).
> scripts/qa/run-audit.ts:206:  const manifestPath = path.resolve(REPO_ROOT, "proof-manifest.json");
> scripts/qa/verifiers.ts:95:  // Resolved in neither table. A strict claim (e.g. from proof-manifest.json)
> .claude/worktrees/eager-brown-6ef0f1/HANDOFF.md:671:**6. Handoff milestone node + proof-manifest.** Phase 3 do seal protocol inseriu `session-handoff-20260526-e2e-user-zero-bok-v684` UUID **`8e6462a9-33ed-49f1-9403-780846d1f41f`** (stability 1.0, embedded 768d). Phase 5c material proof audit valida claims acima.
> .claude/worktrees/eager-brown-6ef0f1/HANDOFF.md:682:| Handoff milestone node + proof-manifest.json | ✅ `8e6462a9-33ed-49f1-9403-780846d1f41f` embedded 768d |
> ```

## 🤖 Claude *(03:38:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra && du -sh */ 2>/dev/null | sort -rh | head -15; echo \"---TOTAL-DIRS---\"; ls -1 | wc -l; echo \"---ATIVA---\"; echo \"863fa9e6-3ea7-490f-99e3-99a1876199e3 = sessao ATUAL\"",
  "description": "Rank scratchpad sessions by disk usage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 4.2G	2de725c0-2186-4fa8-9a12-16d4bd8f3128/
> 954M	9b9cb2fa-663b-4f25-98b8-c32877cbffb1/
> 880M	dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/
> 591M	c1b6a7b1-691a-443b-a950-94444ce8065d/
> 36M	5a5e16b5-d937-4510-9eec-a5ca6ca6e209/
> 3.5M	a567ddd1-44e0-49bf-a324-3eb996461c7b/
> 1.3M	101c4987-9d7b-44af-b78d-4b79ff04fbeb/
> 28K	05ed2f1f-54fd-4d9c-99af-2edef14a5803/
> 12K	863fa9e6-3ea7-490f-99e3-99a1876199e3/
> 12K	2dbe54d8-bd64-4ba0-9b8b-d074672381d9/
> 8.0K	fc0a83ba-1b0e-4e5b-b62f-ad0e7c73a938/
> 8.0K	fa3b7745-0e4a-425b-963c-db273cc8b555/
> 8.0K	f6f28380-4586-49c5-8a00-eda7ee0b88a4/
> 8.0K	f249669e-a48c-4352-ba0d-ad9bd6348acc/
> 8.0K	e7678a88-d63a-40f1-a818-4f8d8b7469e5/
> ---TOTAL-DIRS---
> 42
> ---ATIVA---
> 863fa9e6-3ea7-490f-99e3-99a1876199e3 = sessao ATUAL
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:38:26)*

<details>
<summary>💭 Thinking Process</summary>

I need to check four large scratchpads before pruning them, making sure nothing valuable exists only in those files — the largest is 4.2G, followed by 954M from the last session, then 880M and 591M. There's also an alert about an invalid Google API key on tenant 85aaca76 that needs attention, and I should analyze the Higgsfield links.

The key insight here is that using their showcase projects as visual reference material for composition and cinematography is legitimate — it's not about subscribing to their service. My plan is to run the scratchpad inspection in parallel while probing those Higgsfield links, which are JavaScript-heavy SPA pages. I'll use firecrawl or a browser agent to actually see what's on those pages and decompose the visual elements — the camera movements, timing, lighting, and motion. Ideally I'd download and frame-analyze the videos, but first I need to see what the pages expose. Let me start gathering everything in parallel.

</details>


## 🤖 Claude *(03:38:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for d in 2de725c0-2186-4fa8-9a12-16d4bd8f3128 dfd4c8a3-8149-4c5f-8d9c-f6076b019b22 c1b6a7b1-691a-443b-a950-94444ce8065d 9b9cb2fa-663b-4f25-98b8-c32877cbffb1; do\n  p=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/$d/scratchpad\n  echo \"\u2550\u2550\u2550\u2550 $d ($(du -sh $p 2>/dev/null | cut -f1)) mtime=$(stat -c %y $p 2>/dev/null | cut -d. -f1)\"\n  ls -1 $p 2>/dev/null | head -12\n  echo \"  -- extens\u00f5es dominantes:\"\n  find $p -type f 2>/dev/null | sed 's/.*\\.//' | sort | uniq -c | sort -rn | head -6\ndone",
  "description": "Inspect the 4 large scratchpads for harvest-worthy content"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ════ 2de725c0-2186-4fa8-9a12-16d4bd8f3128 (4.2G) mtime=2026-08-07 18:26:18
> 0165a56b.fmd5
> 0165a56b.mp4
> 7b9024cd.fmd5
> 7b9024cd.mp4
> a175.png
> A175.png
> ab.mjs
> ae76522e.fmd5
> ae76522e.mp4
> alpha-ab.png
> alpha-test
> b175.png
>   -- extensões dominantes:
>    7317 jpg
>    1208 png
>      91 ts
>      84 html
>      63 mp4
>      59 mjs
> ════ dfd4c8a3-8149-4c5f-8d9c-f6076b019b22 (880M) mtime=2026-08-08 01:53:59
> audit-35-nos.txt
> ep06-montar
> fixed-c04-pasta.png
> fixed-c10-slider.png
> gen-ep06-c4-c10.ts
> model-2ba98e10.mp4
> model-2ba98e10-sheet.png
> model-2ba98e10-t1.png
> model-2ba98e10-t3.png
> model-2ba98e10-t5.png
> model-2ba98e10-t7.png
> model-fcf91d44.mp4
>   -- extensões dominantes:
>    5162 jpg
>     290 png
>      50 mp4
>      25 mp3
>      17 json
>      15 html
> ════ c1b6a7b1-691a-443b-a950-94444ce8065d (591M) mtime=2026-08-11 12:27:55
> ep07-master
> ep07-pilot
> ep07-render.log
>   -- extensões dominantes:
>     842 png
>       4 mp4
>       3 html
>       1 txt
>       1 log
> ════ 9b9cb2fa-663b-4f25-98b8-c32877cbffb1 (954M) mtime=2026-08-13 21:03:24
> e2e-validation
> ep07-briefs
> ep07-estrutura
> ep07-gauntlet
> ep07-pilot-montar
> f.html
> gimg.html
> gmodels.json
> hf
> km
> or-img.json
> or.json
>   -- extensões dominantes:
>     903 png
>      20 txt
>      14 sample
>      12 json
>       8 md
>       8 html
> ```

## 🤖 Claude *(03:38:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -sI -m 20 -A \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36\" \"https://higgsfield.ai/@higgsfield.studio/projects/oneiric\" | head -12; echo \"=== SEGUNDO ===\"; curl -sI -m 20 -A \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36\" \"https://higgsfield.ai/@higgsfield.studio/projects/cully-hill-boys\" | head -12",
  "description": "Probe Higgsfield project URLs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> HTTP/2 200 
> date: Fri, 14 Aug 2026 03:38:31 GMT
> content-type: text/html; charset=utf-8
> cache-control: private, no-cache
> x-hf-worker: tanstack
> document-policy: js-profiling
> server-timing: i18n;dur=0.0, middleware_total;dur=0.0
> x-clerk-auth-reason: session-token-and-uat-missing
> x-clerk-auth-status: signed-out
> set-cookie: hf-first-visit-at=1786678711634; Max-Age=31104000; Path=/; SameSite=Lax
> set-cookie: $$__device-id=622be54e-13ed-4c05-99ba-820cb409e280; Max-Age=31104000; Path=/; SameSite=Lax
> set-cookie: hf-tier=T2; Max-Age=31104000; Path=/; SameSite=Lax
> === SEGUNDO ===
> HTTP/2 200 
> date: Fri, 14 Aug 2026 03:38:32 GMT
> content-type: text/html; charset=utf-8
> cache-control: private, no-cache
> x-hf-worker: tanstack
> document-policy: js-profiling
> server-timing: i18n;dur=0.0, middleware_total;dur=1.0
> x-clerk-auth-reason: session-token-and-uat-missing
> x-clerk-auth-status: signed-out
> set-cookie: hf-first-visit-at=1786678712828; Max-Age=31104000; Path=/; SameSite=Lax
> set-cookie: $$__device-id=8e720215-945d-4d1f-a9a5-3f8e93ac4743; Max-Age=31104000; Path=/; SameSite=Lax
> set-cookie: hf-tier=T2; Max-Age=31104000; Path=/; SameSite=Lax
> ```

## 🤖 Claude *(03:38:45)*

<details>
<summary>💭 Thinking Process</summary>

Both URLs are accessible without authentication and return 200 responses. Since this is a TanStack SPA with Clerk auth, I need to extract the video assets by fetching the HTML and searching for embedded JSON or video URLs, likely by curling the page and grepping for mp4 or CDN references. I'm also noting a scratchpad directory with motion spike test frames that's mostly regenerable but contains some .mjs files.

I'm seeing several scratchpad directories with different timestamps and sizes. The critical one is `dfd4c8a3` which contains `model-fcf91d44.mp4` — this is the benchmark model referenced in the Record as the approved reference piece, so it needs to be preserved rather than deleted. The other directories contain episode frames and assets that were either already harvested or are regenerable. I need to verify whether the benchmark file is already saved in the repurpose-inbox and check the Higgsfield page content to confirm.

</details>


## 🤖 Claude *(03:38:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad\nfor slug in oneiric cully-hill-boys; do\n  curl -s -m 40 -A \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36\" \\\n    \"https://higgsfield.ai/@higgsfield.studio/projects/$slug\" -o hf-$slug.html\n  echo \"\u2550\u2550\u2550\u2550 $slug: $(wc -c < hf-$slug.html) bytes\"\n  grep -oE 'https://[a-zA-Z0-9._/-]+\\.(mp4|webm|m3u8|jpg|jpeg|png|webp)' hf-$slug.html | sort -u | head -20\ndone",
  "description": "Fetch Higgsfield project pages and extract media URLs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ════ oneiric: 74554 bytes
> ════ cully-hill-boys: 73903 bytes
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:38:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== benchmark fcf91d44 no host (fora do /tmp) ===\"; find /home/gcrUX/htdocs/constellation-orchestra/repurpose-inbox /home/gcrUX/htdocs/constellation-orchestra/scripts -iname \"*fcf91d44*\" 2>/dev/null; echo \"--- no scratchpad 08-08 ---\"; ls -la /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-fcf91d44.mp4 2>/dev/null; echo \"--- mp4/mp3 >1MB nos 4 scratchpads grandes (candidatos a colheita) ---\"; for d in 2de725c0-2186-4fa8-9a12-16d4bd8f3128 dfd4c8a3-8149-4c5f-8d9c-f6076b019b22 c1b6a7b1-691a-443b-a950-94444ce8065d; do find /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/$d/scratchpad -type f \\( -name \"*.mp4\" -o -name \"*.mp3\" -o -name \"*.wav\" \\) -size +1M -printf \"%s\\t%p\\n\" 2>/dev/null; done | sort -rn | head -20",
  "description": "Locate benchmark video and harvest candidates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === benchmark fcf91d44 no host (fora do /tmp) ===
> /home/gcrUX/htdocs/constellation-orchestra/repurpose-inbox/ep06-fe479105/componentes-fcf91d44
> --- no scratchpad 08-08 ---
> -rw-rw-r-- 1 ubuntu ubuntu 3069023 Aug  8 01:00 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-fcf91d44.mp4
> --- mp4/mp3 >1MB nos 4 scratchpads grandes (candidatos a colheita) ---
> 23572524	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/ep06-montar/ep06-master-raw.mp4
> 23572524	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/ep06-montar/ep06-master.mp4
> 9933520	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ep07-master-dataviz.mp4
> 5553085	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/m1/mp_j92.mp4
> 5419080	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-pilot/ep07-adsense-pilot.mp4
> 5249193	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/ep06-montar/clips/veo-p1.mp4
> 5218851	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/ep06-montar/clips/veo-p1-norm.mp4
> 4996643	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ato3-audio/ato3-audio.mp4
> 4937557	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ato2-adsense/ato2-adsense.mp4
> 4693092	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit/src.mp4
> 4619308	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-2ba98e10.mp4
> 4619308	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/w.mp4
> 4619308	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/witness.mp4
> 3916828	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/vidprobe/clip-h264-g1.mp4
> 3766258	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/m1/mp_j100.mp4
> 3601755	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/m1/mp_png.mp4
> 3069023	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-fcf91d44.mp4
> 3069023	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/vw/real_clip.mp4
> 3052604	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/proto-layers/out/spike-montar.mp4
> 3052604	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/critic/repro/out/repro.mp4
> ```

## 🤖 Claude *(03:39:06)*

<details>
<summary>💭 Thinking Process</summary>

The Higgsfield pages are rendering client-side, so I need a real browser to capture the content. I'll use the agent-browser skill since that's the preferred approach, then extract the video files so I can analyze the frames.

Before spinning up a full workflow, let me scout inline first — I'll grab the Higgsfield videos locally, enumerate the harvest candidates in the scratchpads, and check tenant 85aaca76.

</details>


## 🤖 Claude *(03:39:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad\necho \"=== marcadores de estado embutido ===\"\ngrep -oE '(__TSR|dehydrat|streamedValue|routerState|window\\.__)[A-Za-z_]*' hf-oneiric.html | sort | uniq -c | head\necho \"=== ocorr\u00eancias de cdn/storage/video ===\"\ngrep -oiE '[a-z0-9.-]*(cdn|storage|media|video|cloudfront|r2|s3)[a-z0-9.-]*\\.[a-z]{2,}' hf-oneiric.html | sort -u | head -20\necho \"=== title/og ===\"\ngrep -oE '<title>[^<]*</title>|<meta property=\"og:[^>]*>' hf-oneiric.html | head -8",
  "description": "Inspect Higgsfield HTML for embedded state and CDN hosts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === marcadores de estado embutido ===
> === ocorrências de cdn/storage/video ===
> === title/og ===
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:39:11)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:mcp__playwright__browser_navigate,mcp__playwright__browser_network_requests,mcp__playwright__browser_snapshot,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_evaluate,mcp__playwright__browser_wait_for,mcp__playwright__browser_close,mcp__playwright__browser_resize",
  "max_results": 10
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_navigate'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_network_requests'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_snapshot'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_take_screenshot'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_evaluate'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_wait_for'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_close'}, {'type': 'tool_reference', 'tool_name': 'mcp__playwright__browser_resize'}]
> ```

## 🤖 Claude *(03:39:14)*


🛠️ **Tool Call**: `mcp__playwright__browser_navigate`
```json
{
  "url": "https://higgsfield.ai/@higgsfield.studio/projects/oneiric"
}
```

> **Tool Result (mcp__playwright__browser_navigate)** - ❌ Error
>
> ```
> ### Error
> Error: async initializeServer: Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome
> Run "npx playwright install chrome"
> ```

## 🤖 Claude *(03:39:19)*

<details>
<summary>💭 Thinking Process</summary>

I should use the agent-browser skill instead since that's what the project prefers and it's already available from the previous session, rather than trying to set up Playwright with Chrome. Let me load that skill now.

</details>


## 🤖 Claude *(03:39:19)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "agent-browser"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: agent-browser
> ```

## 👤 User *(03:39:19)*

Base directory for this skill: /home/gcrUX/htdocs/constellation-orchestra/.claude/skills/agent-browser

# agent-browser

Fast browser automation CLI for AI agents. Chrome/Chromium via CDP with
accessibility-tree snapshots and compact `@eN` element refs.

Install: `npm i -g agent-browser && agent-browser install`

## Start here

This file is a discovery stub, not the usage guide. Before running any
`agent-browser` command, load the actual workflow content from the CLI:

```bash
agent-browser skills get core             # start here — workflows, common patterns, troubleshooting
agent-browser skills get core --full      # include full command reference and templates
```

The CLI serves skill content that always matches the installed version,
so instructions never go stale. The content in this stub cannot change
between releases, which is why it just points at `skills get core`.

## Specialized skills

Load a specialized skill when the task falls outside browser web pages:

```bash
agent-browser skills get electron          # Electron desktop apps (VS Code, Slack, Discord, Figma, ...)
agent-browser skills get slack             # Slack workspace automation
agent-browser skills get dogfood           # Exploratory testing / QA / bug hunts
agent-browser skills get vercel-sandbox    # agent-browser inside Vercel Sandbox microVMs
agent-browser skills get agentcore         # AWS Bedrock AgentCore cloud browsers
```

Run `agent-browser skills list` to see everything available on the
installed version.

## Why agent-browser

- Fast native Rust CLI, not a Node.js wrapper
- Works with any AI agent (Cursor, Claude Code, Codex, Continue, Windsurf, etc.)
- Chrome/Chromium via CDP with no Playwright or Puppeteer dependency
- Accessibility-tree snapshots with element refs for reliable interaction
- Sessions, authentication vault, state persistence, video recording
- Specialized skills for Electron apps, Slack, exploratory testing, cloud providers

## Observability Dashboard

The dashboard runs independently of browser sessions on port 4848 and can also be opened through a proxied or forwarded URL such as `https://dashboard.agent-browser.localhost`. Agents should stay on the dashboard origin: session tabs, status, and stream traffic are proxied internally, so session ports do not need to be exposed.


## 🤖 Claude *(03:39:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "agent-browser skills get core 2>&1 | head -150",
  "description": "Load agent-browser core skill"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---
> name: core
> description: Core agent-browser usage guide. Read this before running any agent-browser commands. Covers the snapshot-and-ref workflow, navigating pages, interacting with elements (click, fill, type, select), extracting text and data, taking screenshots, managing tabs, handling forms and auth, waiting for content, running multiple browser sessions in parallel, and troubleshooting common failures. Use when the user asks to interact with a website, fill a form, click something, extract data, take a screenshot, log into a site, test a web app, or automate any browser task.
> allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
> ---
> 
> # agent-browser core
> 
> Fast browser automation CLI for AI agents. Chrome/Chromium via CDP, no
> Playwright or Puppeteer dependency. Accessibility-tree snapshots with compact
> `@eN` refs let agents interact with pages in ~200-400 tokens instead of
> parsing raw HTML.
> 
> Most normal web tasks (navigate, read, click, fill, extract, screenshot) are
> covered here. Load a specialized skill when the task falls outside browser
> web pages — see [When to load another skill](#when-to-load-another-skill).
> 
> ## The core loop
> 
> ```bash
> agent-browser open <url>        # 1. Open a page
> agent-browser snapshot -i       # 2. See what's on it (interactive elements only)
> agent-browser click @e3         # 3. Act on refs from the snapshot
> agent-browser snapshot -i       # 4. Re-snapshot after any page change
> ```
> 
> Refs (`@e1`, `@e2`, ...) are assigned fresh on every snapshot. They become
> **stale the moment the page changes** — after clicks that navigate, form
> submits, dynamic re-renders, dialog opens. Always re-snapshot before your
> next ref interaction.
> 
> ## Quickstart
> 
> ```bash
> # Install once
> npm i -g agent-browser && agent-browser install
> 
> # Take a screenshot of a page
> agent-browser open https://example.com
> agent-browser screenshot home.png
> agent-browser close
> 
> # Search, click a result, and capture it
> agent-browser open https://duckduckgo.com
> agent-browser snapshot -i                      # find the search box ref
> agent-browser fill @e1 "agent-browser cli"
> agent-browser press Enter
> agent-browser wait --load networkidle
> agent-browser snapshot -i                      # refs now reflect results
> agent-browser click @e5                        # click a result
> agent-browser screenshot result.png
> ```
> 
> The browser stays running across commands so these feel like a single
> session. Use `agent-browser close` (or `close --all`) when you're done.
> 
> ## Reading a page
> 
> ```bash
> agent-browser snapshot                    # full tree (verbose)
> agent-browser snapshot -i                 # interactive elements only (preferred)
> agent-browser snapshot -i -u              # include href urls on links
> agent-browser snapshot -i -c              # compact (no empty structural nodes)
> agent-browser snapshot -i -d 3            # cap depth at 3 levels
> agent-browser snapshot -s "#main"         # scope to a CSS selector
> agent-browser snapshot -i --json          # machine-readable output
> ```
> 
> Snapshot output looks like:
> 
> ```
> Page: Example - Log in
> URL: https://example.com/login
> 
> @e1 [heading] "Log in"
> @e2 [form]
>   @e3 [input type="email"] placeholder="Email"
>   @e4 [input type="password"] placeholder="Password"
>   @e5 [button type="submit"] "Continue"
>   @e6 [link] "Forgot password?"
> ```
> 
> For unstructured reading (no refs needed):
> 
> ```bash
> agent-browser get text @e1                # visible text of an element
> agent-browser get html @e1                # innerHTML
> agent-browser get attr @e1 href           # any attribute
> agent-browser get value @e1               # input value
> agent-browser get title                   # page title
> agent-browser get url                     # current URL
> agent-browser get count ".item"           # count matching elements
> ```
> 
> ## Interacting
> 
> ```bash
> agent-browser click @e1                   # click
> agent-browser click @e1 --new-tab         # open link in new tab instead of navigating
> agent-browser dblclick @e1                # double-click
> agent-browser hover @e1                   # hover
> agent-browser focus @e1                   # focus (useful before keyboard input)
> agent-browser fill @e2 "hello"            # clear then type
> agent-browser type @e2 " world"           # type without clearing
> agent-browser press Enter                 # press a key at current focus
> agent-browser press Control+a             # key combination
> agent-browser check @e3                   # check checkbox
> agent-browser uncheck @e3                 # uncheck
> agent-browser select @e4 "option-value"   # select dropdown option
> agent-browser select @e4 "a" "b"          # select multiple
> agent-browser upload @e5 file1.pdf        # upload file(s)
> agent-browser scroll down 500             # scroll page (up/down/left/right)
> agent-browser scrollintoview @e1          # scroll element into view
> agent-browser drag @e1 @e2                # drag and drop
> ```
> 
> ### When refs don't work or you don't want to snapshot
> 
> Use semantic locators:
> 
> ```bash
> agent-browser find role button click --name "Submit"
> agent-browser find text "Sign In" click
> agent-browser find text "Sign In" click --exact     # exact match only
> agent-browser find label "Email" fill "user@test.com"
> agent-browser find placeholder "Search" type "query"
> agent-browser find testid "submit-btn" click
> agent-browser find first ".card" click
> agent-browser find nth 2 ".card" hover
> ```
> 
> Or a raw CSS selector:
> 
> ```bash
> agent-browser click "#submit"
> agent-browser fill "input[name=email]" "user@test.com"
> agent-browser click "button.primary"
> ```
> 
> Rule of thumb: snapshot + `@eN` refs are fastest and most reliable for
> AI agents. `find role/text/label` is next best and doesn't require a prior
> snapshot. Raw CSS is a fallback when the others fail.
> 
> ## Waiting (read this)
> 
> Agents fail more often from bad waits than from bad selectors. Pick the
> right wait for the situation:
> 
> ```bash
> agent-browser wait @e1                     # until an element appears
> ```

## 🤖 Claude *(03:39:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "agent-browser skills get core 2>&1 | sed -n '150,300p'",
  "description": "Read rest of agent-browser core skill"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> agent-browser wait @e1                     # until an element appears
> agent-browser wait 2000                    # dumb wait, milliseconds (last resort)
> agent-browser wait --text "Success"        # until the text appears on the page
> agent-browser wait --url "**/dashboard"    # until URL matches pattern (glob)
> agent-browser wait --load networkidle      # until network idle (post-navigation)
> agent-browser wait --load domcontentloaded # until DOMContentLoaded
> agent-browser wait --fn "window.myApp.ready === true"  # until JS condition
> ```
> 
> After any page-changing action, pick one:
> 
> - Wait for a specific element you expect to appear: `wait @ref` or `wait --text "..."`.
> - Wait for URL change: `wait --url "**/new-page"`.
> - Wait for network idle (catch-all for SPA navigation): `wait --load networkidle`.
> 
> Avoid bare `wait 2000` except when debugging — it makes scripts slow and
> flaky. Timeouts default to 25 seconds.
> 
> ## Common workflows
> 
> ### Log in
> 
> ```bash
> agent-browser open https://app.example.com/login
> agent-browser snapshot -i
> 
> # Pick the email/password refs out of the snapshot, then:
> agent-browser fill @e3 "user@example.com"
> agent-browser fill @e4 "hunter2"
> agent-browser click @e5
> agent-browser wait --url "**/dashboard"
> agent-browser snapshot -i
> ```
> 
> Credentials in shell history are a leak. For anything sensitive, use the
> auth vault (see [references/authentication.md](references/authentication.md)):
> 
> ```bash
> agent-browser auth save my-app --url https://app.example.com/login \
>   --username user@example.com --password-stdin
> # (type password, Ctrl+D)
> 
> agent-browser auth login my-app    # fills + clicks, waits for form
> ```
> 
> ### Persist session across runs
> 
> ```bash
> # Log in once, save cookies + localStorage
> agent-browser state save ./auth.json
> 
> # Later runs start already-logged-in
> agent-browser --state ./auth.json open https://app.example.com
> ```
> 
> Or use `--session-name` for auto-save/restore:
> 
> ```bash
> AGENT_BROWSER_SESSION_NAME=my-app agent-browser open https://app.example.com
> # State is auto-saved and restored on subsequent runs with the same name.
> ```
> 
> ### Extract data
> 
> ```bash
> # Structured snapshot (best for AI reasoning over page content)
> agent-browser snapshot -i --json > page.json
> 
> # Targeted extraction with refs
> agent-browser snapshot -i
> agent-browser get text @e5
> agent-browser get attr @e10 href
> 
> # Arbitrary shape via JavaScript
> cat <<'EOF' | agent-browser eval --stdin
> const rows = document.querySelectorAll("table tbody tr");
> Array.from(rows).map(r => ({
>   name: r.cells[0].innerText,
>   price: r.cells[1].innerText,
> }));
> EOF
> ```
> 
> Prefer `eval --stdin` (heredoc) or `eval -b <base64>` for any JS with
> quotes or special characters. Inline `agent-browser eval "..."` works
> only for simple expressions.
> 
> ### Screenshot
> 
> ```bash
> agent-browser screenshot                        # temp path, printed on stdout
> agent-browser screenshot page.png               # specific path
> agent-browser screenshot --full full.png        # full scroll height
> agent-browser screenshot --annotate map.png     # numbered labels + legend keyed to snapshot refs
> ```
> 
> `--annotate` is designed for multimodal models: each label `[N]` maps to ref `@eN`.
> 
> ### Handle multiple pages via tabs
> 
> ```bash
> agent-browser tab                      # list open tabs (with stable tabId)
> agent-browser tab new https://docs...  # open a new tab (and switch to it)
> agent-browser tab 2                    # switch to tab 2
> agent-browser tab close 2              # close tab 2
> ```
> 
> Stable `tabId`s mean `tab 2` points at the same tab across commands even
> when other tabs open or close. After switching, refs from a prior snapshot
> on a different tab no longer apply — re-snapshot.
> 
> ### Run multiple browsers in parallel
> 
> Each `--session <name>` is an isolated browser with its own cookies, tabs,
> and refs. Useful for testing multi-user flows or parallel scraping:
> 
> ```bash
> agent-browser --session a open https://app.example.com
> agent-browser --session b open https://app.example.com
> agent-browser --session a fill @e1 "alice@test.com"
> agent-browser --session b fill @e1 "bob@test.com"
> ```
> 
> `AGENT_BROWSER_SESSION=myapp` sets the default session for the current
> shell.
> 
> ### Mock network requests
> 
> ```bash
> agent-browser network route "**/api/users" --body '{"users":[]}'   # stub a response
> agent-browser network route "**/analytics" --abort                 # block entirely
> agent-browser network requests                                     # inspect what fired
> agent-browser network har start                                    # record all traffic
> # ... perform actions ...
> agent-browser network har stop /tmp/trace.har
> ```
> 
> ### Record a video of the workflow
> 
> ```bash
> agent-browser record start demo.webm
> agent-browser open https://example.com
> agent-browser snapshot -i
> agent-browser click @e3
> agent-browser record stop
> ```
> 
> See [references/video-recording.md](references/video-recording.md) for
> codec options, GIF export, and more.
> 
> ### Iframes
> ```

## 🤖 Claude *(03:39:30)*

<details>
<summary>💭 Thinking Process</summary>

I'm going to use agent-browser to navigate to the Higgsfield project pages, intercept the video URLs from network traffic, and download them. Let me start by opening the page and setting up a task list for this multi-step process.

</details>


## 🤖 Claude *(03:39:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad && mkdir -p hf && cd hf\nagent-browser --session hf open \"https://higgsfield.ai/@higgsfield.studio/projects/oneiric\" 2>&1 | tail -5\nagent-browser --session hf wait --load networkidle 2>&1 | tail -2\nagent-browser --session hf get title 2>&1 | tail -2\nagent-browser --session hf get url 2>&1 | tail -2",
  "description": "Open Higgsfield oneiric project in agent-browser",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ ONEIRIC | Higgsfield Community
>   https://higgsfield.ai/@higgsfield.studio/projects/oneiric
> ✓ Done
> ONEIRIC | Higgsfield Community
> https://higgsfield.ai/@higgsfield.studio/projects/oneiric
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:40:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\ncat <<'EOF' | agent-browser --session hf eval --stdin\nconst vids = Array.from(document.querySelectorAll('video')).map(v => ({\n  src: v.currentSrc || v.src,\n  poster: v.poster,\n  w: v.videoWidth, h: v.videoHeight, dur: v.duration,\n  sources: Array.from(v.querySelectorAll('source')).map(s => s.src)\n}));\nconst imgs = Array.from(document.querySelectorAll('img')).map(i=>i.currentSrc||i.src).filter(Boolean);\nJSON.stringify({ nVideos: vids.length, vids, nImgs: imgs.length, imgs: imgs.slice(0,12), bodyText: document.body.innerText.slice(0,1500) }, null, 1);\nEOF",
  "description": "Extract video and image elements from the page",
  "timeout": 120000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> "{\n \"nVideos\": 3,\n \"vids\": [\n  {\n   \"src\": \"https://cdn.higgsfield.ai/hls/video_input/8e773bcc-7271-41a4-8024-3629f9ea9ca4/index.m3u8\",\n   \"poster\": \"https://cdn.higgsfield.ai/hls/video_input/8e773bcc-7271-41a4-8024-3629f9ea9ca4/thumbnail.webp\",\n   \"w\": 0,\n   \"h\": 0,\n   \"dur\": null,\n   \"sources\": []\n  },\n  {\n   \"src\": \"https://cdn.higgsfield.ai/hls/video_input/22223dcb-7524-4311-9bdc-3ca8444f4183/index.m3u8#t=0.001\",\n   \"poster\": \"\",\n   \"w\": 0,\n   \"h\": 0,\n   \"dur\": null,\n   \"sources\": []\n  },\n  {\n   \"src\": \"https://cdn.higgsfield.ai/hls/video_input/22223dcb-7524-4311-9bdc-3ca8444f4183/index.m3u8\",\n   \"poster\": \"\",\n   \"w\": 0,\n   \"h\": 0,\n   \"dur\": null,\n   \"sources\": []\n  }\n ],\n \"nImgs\": 92,\n \"imgs\": [\n  \"https://d2ol7oe51mr4n9.cloudfront.net/user_3GNcyaSCltezE7ot4WtRdn0jfo0/4203e91f-4612-411f-a567-36265f8ee8b9.png\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd2ol7oe51mr4n9.cloudfront.net%2Fcontent_user_id%2F2576cd81-f6e8-4dcd-afc9-05f9319a463b.png&w=24&q=85\",\n  \"https://d2ol7oe51mr4n9.cloudfront.net/user_3GNcyaSCltezE7ot4WtRdn0jfo0/4203e91f-4612-411f-a567-36265f8ee8b9.png\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd2ol7oe51mr4n9.cloudfront.net%2Fcontent_user_id%2F2576cd81-f6e8-4dcd-afc9-05f9319a463b.png&w=24&q=85\",\n  \"https://higgsfield.ai/cdn-cgi/image/fit=scale-down,format=webp,onerror=redirect,width=1280,quality=85/academy/banners/festival/background.webp\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_3BuCGXDsgbIxK9tn3qHKjEy2sKF%2Fhf_20260715_003709_35aca6ad-a259-4d8d-8279-474e2641d0ad.png&w=256&q=85\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_3BuCGXDsgbIxK9tn3qHKjEy2sKF%2Fhf_20260715_002129_d6e2baf6-ef3c-48c5-9be0-587411df437c.png&w=256&q=85\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_3BuCGXDsgbIxK9tn3qHKjEy2sKF%2Fhf_20260715_001727_99920d97-cda7-418a-8706-54808856c1e4.png&w=256&q=85\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_3BuCGXDsgbIxK9tn3qHKjEy2sKF%2Fhf_20260715_001729_a2cd146e-9c49-4b51-ae24-b3e6226ad21b.png&w=256&q=85\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_3BuCGXDsgbIxK9tn3qHKjEy2sKF%2Fhf_20260715_001317_5ca61464-14ee-4222-b36d-5a309d6b620d.png&w=256&q=85\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_3BuCGXDsgbIxK9tn3qHKjEy2sKF%2Fhf_20260715_004808_9797a78c-4bb8-449e-9ee8-a59bb15a7016.png&w=256&q=85\",\n  \"https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_3BuCGXDsgbIxK9tn3qHKjEy2sKF%2Fhf_20260715_002138_2a18ba4e-46bb-4f5a-87f0-5030fb8d30ba.png&w=256&q=85\"\n ],\n \"bodyText\": \"SIGN UP AND GET ADDITIONAL DISCOUNT ON PREMIUM PLANS\\n\\nEXTRA DISCOUNT\\n\\nExplore\\nImage\\nVideo\\nAudio\\nEdit\\nLayers\\nCinema Studio\\nNew\\nMarketing Studio\\nNew\\nViral Presets\\nMCP & CLI\\nNew\\nSupercomputer\\nAcademy\\nNew\\nCommunity\\nContests\\nNew\\nPlugins\\nCanvas\\nOriginals\\nPricing\\n30% OFF\\nEnterprise\\nLogin\\nSign up\\nCommunity\\n/\\nONEIRIC\\nCommunity\\n/\\nONEIRIC\\nView full project\\n254\\n39\\nShare\\n1×\\n0:00 / 0:00\\nONEIRIC\\n14 774 views\\n·\\n1 day ago\\nHiggsfield Studio\\nView full project\\n254\\n39\\nShare\\n\\nONEIRIC - a short film. Four college students in a dorm discuss the news: Oneiric's technology can plug your brain into any time and place. Each fantasizes about where he'd spend one day: Bob — the Trojan War, to see Helen with his own eyes; Sam — a deep-space future as a galactic pirate; Rudy — a fairy-tale world as a mage on a griffin. Each fantasy plays out as its own genre vignette.\\n\\nAny story. Any genre. One prize pool.\\n\\n$1,000,000\\n\\nJoin the Festival\\n\\nFolders\\n\\nAll assets\\n41118\\nASSETS\\n22960\\nregenerations\\n292\\nSCENE 1 - KITCHEN\\n303\\nSCENE 2 - LIVINGROOM\\n1326\\nSCENE 3 - TROY\\n1665\\nSCENE 3B - LIVINGROOM\\n52\\nSCENE 4 - LIVINGROOM\\n862\\nSCENE 5 - COSMOS\\n5397\\nSCENE 6 - LIVING ROOM\\n912\\nSCENE 7 - FAIRYTALE\\n1819\\nSCENE 8 - LIVINGROOM\\n186\\nSCENE 9 - FAIRY TALE\\n3743\\nSCENE 9A - LIVINGROOM\\n64\\nSCENE 10 - LIVING ROOM\\n747\\nSCENE 11 - LAB\\n116\\nSCENE 12 - TITLE SEQUENCE\\n418\\n\\nAssets\\n\\nProject brief\\n\\nThis is the project breakdown for ONEIRIC, our AI short film: the pipeline, the tools, and the hacks we learned along the way.\\n\\n\\n\\n\\nLogline: Four friends in \"\n}"
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:40:21)*

<details>
<summary>💭 Thinking Process</summary>

I found a detailed project breakdown with pipeline information, tools, and HLS video streams. The data shows ONEIRIC, an AI short film with over 41,000 assets and nearly 23,000 regenerations across 12 scenes, each with specific asset counts like Scene 3 with 1,665 assets and Scene 6 with 912.

Now I'm parsing the structured data more carefully to extract the full project brief text and identify all the HLS video streams so I can download them and analyze the frames. My plan is to pull the complete project documentation and video assets, then run a workflow to decompose the cinema ruler across all dimensions and generate improved next steps.

</details>


## 🤖 Claude *(03:40:21)*

Encontrei o essencial: a página traz o **project breakdown completo** (pipeline, ferramentas, hacks) além dos vídeos. Vou extrair tudo.

## 🤖 Claude *(03:40:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\ncat <<'EOF' | agent-browser --session hf eval --stdin\ndocument.body.innerText\nEOF",
  "description": "Extract full page text for ONEIRIC",
  "timeout": 120000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> "SIGN UP AND GET ADDITIONAL DISCOUNT ON PREMIUM PLANS\n\nEXTRA DISCOUNT\n\nExplore\nImage\nVideo\nAudio\nEdit\nLayers\nCinema Studio\nNew\nMarketing Studio\nNew\nViral Presets\nMCP & CLI\nNew\nSupercomputer\nAcademy\nNew\nCommunity\nContests\nNew\nPlugins\nCanvas\nOriginals\nPricing\n30% OFF\nEnterprise\nLogin\nSign up\nCommunity\n/\nONEIRIC\nCommunity\n/\nONEIRIC\nView full project\n254\n39\nShare\n1×\n0:00 / 0:00\nONEIRIC\n14 774 views\n·\n1 day ago\nHiggsfield Studio\nView full project\n254\n39\nShare\n\nONEIRIC - a short film. Four college students in a dorm discuss the news: Oneiric's technology can plug your brain into any time and place. Each fantasizes about where he'd spend one day: Bob — the Trojan War, to see Helen with his own eyes; Sam — a deep-space future as a galactic pirate; Rudy — a fairy-tale world as a mage on a griffin. Each fantasy plays out as its own genre vignette.\n\nAny story. Any genre. One prize pool.\n\n$1,000,000\n\nJoin the Festival\n\nFolders\n\nAll assets\n41118\nASSETS\n22960\nregenerations\n292\nSCENE 1 - KITCHEN\n303\nSCENE 2 - LIVINGROOM\n1326\nSCENE 3 - TROY\n1665\nSCENE 3B - LIVINGROOM\n52\nSCENE 4 - LIVINGROOM\n862\nSCENE 5 - COSMOS\n5397\nSCENE 6 - LIVING ROOM\n912\nSCENE 7 - FAIRYTALE\n1819\nSCENE 8 - LIVINGROOM\n186\nSCENE 9 - FAIRY TALE\n3743\nSCENE 9A - LIVINGROOM\n64\nSCENE 10 - LIVING ROOM\n747\nSCENE 11 - LAB\n116\nSCENE 12 - TITLE SEQUENCE\n418\n\nAssets\n\nProject brief\n\nThis is the project breakdown for ONEIRIC, our AI short film: the pipeline, the tools, and the hacks we learned along the way.\n\n\n\n\nLogline: Four friends in a dorm common room daydream about a neural net that could drop you into any world — Troy, deep space, a fairy tale. Then the quiet one is asked where he'd go, and his answer changes what the whole afternoon means.\n\n\n\n\n\n\n\nAbout the project\n\nONEIRIC is a ~20-minute photoreal AI short film. Every frame is generated: there is no filmed footage, no sets, no camera crew. The characters exist only as reference assets, and every shot is born from those references plus text.\n\nThe structure of the film defines the whole production. Its spine is one long dialogue scene — four friends in a student dorm common room, discussing a neural engine that could drop a dreamer into any world. Three times the film smash-cuts into those imagined worlds — a battle on the plain of Troy, a chase through a galactic cruiser, a griffin flight over a fairy-tale valley — each a short set piece with its own art direction. The final scene pulls back and reframes everything that came before it.\n\nIn production terms that means two very different jobs. The dream worlds are brief and spectacular — their challenge is design and scale. The common room is the opposite: four characters in one space, held across dozens of shots — same faces, same voices, same seats, same eyelines, for most of the film's runtime. A video model has no memory: it forgets a face between shots, redraws the room when the camera moves, gives a character a new voice in every clip. Keeping that one room stable is the hardest technical task of the film, and most of the pipeline below exists to solve it.\n\n\n\n\nThe tools\nSeedance — every shot, all video and speech. Assets live as named elements on the project.\nClaude + our skills — a skill is a playbook of rules Claude loads and works by. Ours: a scene-drama engine, an acting system, and CINEDANCE, the video-prompt writer.\nThe Diagram Skill — in shots with several characters, text alone doesn't hold the staging.The skill turns any frame into a schematic color-coded diagram, and Seedance reads exact positions, poses and facing directions from it.\nThe anamorphic hack — Seedance doesn't reliably hold anamorphic optics asked for in a video prompt. So the lens character is baked into the location assets themselves: the model reads it straight off the reference image and keeps it. The recipe is in the Assets section.\n\n\n\n\n\n\n\n\n\n\n01 · DEVELOPMENT\n\nThe script goes through a Stress Test\n\nOn an AI film a weak scene costs real money — you find out it doesn't work only after you've generated it. So before anything is generated, every scene runs through the Script Stress Test: a Claude skill that checks it against a five-element engine — Goal, Obstacle, Tactic, Reversal, Value Shift — and returns a verdict per element, the single weakest point, and \"what if\" fixes from minimal to clean rewrite.\n\nThe same stage produces the director's read: for each scene, the one shared event every character lives through, and each character's own physical channel for it. Our laboratory scene: the event is \"the search for self-forgiveness.\" Alfred relives it in the dream; the doctor hides in flawless procedure; the young medic cares for the patient beyond the checklist. The surface — routine rounds — is just the terrain the event moves through. The medic's last line, \"Poor guy. Just can't forgive himself,\" names all three men at once without knowing it.\n\n\n\n\ntig-scene-engine.skill\nSKIL\n\n\n\n\n02 · PRE-PRODUCTION\n\nAssets\n\nAn asset is a pair: text + image. The text descriptor goes into every prompt word for word; the image is the reference the model anchors to. Together they keep for example a hero the same person from shot to shot.\n\n\n\n\nCanvas preview\n\nHiggsfield Canvas\n\n\n\n\nOne naming convention for the whole team\n\nEvery element in the project — locations, characters, extras, props, pose references — is named by a single tag convention the whole team follows. The point is simple: one element, one name. Without it a project this size quickly grows duplicates — the same couch living under three different names — and nobody knows which reference is the real one.\n\n\n\n\nOne tag system everywhere — on the element, in the prompt, in the table:\n@loc_ON_dorm_commonroom_front_s2     location + project + name + scene\n@char_ON_Rudy_s2_v1                                 character + project + scene + version\n@prop_ON_pizza                                          prop + project + name \n\n\n\n\nThe scene suffix ties every asset to where it lives. The version suffix appears when a state changes — a new state is a new asset with a new name, never an overwrite. A character has as many assets as states he goes through: Alfie in the common room and Alfred in the lab bed are different assets of the same man.\n\n\n\n\nCharacter sheets\n\nA character is built in two passes with two models. Soul Cinema makes the face: always generated in close-up, so the model captures identity at maximum detail — that close-up face is the anchor every other asset of the character is checked against. Soul 2.0 then builds the looks: full-figure images with the wardrobe — costume, materials, silhouette — matched to the locked face. \n\nThe two passes are then assembled into the character sheet in Seedream / Nano Banana / ChatGPT — with one hard condition: the original close-up portrait is preserved untouched. It never runs through a model again; the assembly happens in editing tools around it. Every detail that changes between states is integrated point-by-point with masks, without touching the base — a scar, a haircut, a piece of wardrobe, dirt, a wound. The base image stays the same pixels, so the identity (and the skin texture that carries it) survives every new version of the character.\n\n\n\n\n\n\n\nLocations — the anamorphic look\n\nThe film is 2.39:1 with an anamorphic lens character, and here's the problem: ask Seedance for that look in a video prompt and it won't hold it reliably — the optics drift from shot to shot. The fix is to move the lens one step earlier in the pipeline: generate the location image with the anamorphic effect already in it. Seedance reads the optics straight off the asset and keeps them — the plate itself becomes the lens.\n\nThere is no \"anamorphic\" switch in an image model either, so at the asset stage the effect is assembled from words — the geometry of the lens, written out:\n\nBlock for the end of a location image prompt:\n\nSTRONG anamorphic lens character: horizontal squeeze and compression,\noval elliptical bokeh, horizontally stretched highlights, curved barrel\nedge distortion, chromatic aberration toward the edges. NO lens flares, NO light streaks, NO floating bokeh circles. 2.39:1.\n\n\n\n\nDose the strength with subtle / gentle / moderate or strong / maximum, and at this image stage also ban the garbage that tags along: lens flares, light streaks, floating bokeh orbs. In video prompts those words never appear at all — even as bans (see the iron rules: naming them summons them). The video prompt only describes clean glass and contained glows; the anamorphic character comes from the asset.\n\n\n\n\n03 · PRE-PRODUCTION\n\nVoices are written conditions\n\nSeedance generates the speech, but a voice drifts between clips unless it's pinned down. A voice here is a written block — register, timbre, tempo, manner — decided once, stored in the Voice Bible, and pasted into every generation verbatim, never even a synonym changed. \n\nExample AUDIO LOCK (Bob):\nBOB — voice: warm boisterous baritone, big dynamic range, theatrical\ncomedic enthusiasm, a gravelly edge; bursts loud then drops to a\nmock-confidential murmur, punches key words, laughs mid-line. American.\n\n\n\n\n04 · PRODUCTION\n\nVideo prompts — CINEDANCE\n\nEvery shot is written by the CINEDANCE skill in the same blocks, in the same order:\n\nSCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · GAZE / EYELINES ·\nFIRST FRAME AND BLOCKING · SEGMENTS (timed beats) · DIALOGUE · AUDIO ·\nPHYSICS · LIGHTING · STYLE / FORMAT · POSITIVE LOCKS\n\nSeedance sees only the text in front of it, so every prompt is an island: positions, poses, wardrobe, props, optics, light — spelled out from scratch, every time. \"Same as the previous shot\" is an instruction to a model that has no \"before\".\n\nCINEDANCE HIGGSFIELD SKILL.skill\nSKIL\n\n\n\n\n\n\n\nReal fragment — Scene 2\n\nSCENE CONTEXT\nLive-action photoreal feature-film shot, about 11 seconds, continuing Scene 2. Sam, eating pizza, listens to Rudy (off-screen) and cuts him off with a skeptical dismissal; then a hard cut to Bob, who fires back at Sam, all in and trying to win the guys over. It opens on a brief silent wide of the four in their exact positions, then a medium of Sam, then a medium of Bob. The mood is warm and lively.\n\nACTIVE REFERENCES\n@char_ON_Bob_s2_v1: big soft warm guy, early 20s, long curly brown hair, open blue hoodie over a grey UFO tee, baggy jeans. Holding a soda can in his right hand, relaxed in his armchair. 100% matches the reference.\n@char_ON_Sam_s2_v1: slim 18-year-old, short in stature, about 170 cm, ginger hair, rimless glasses, navy-and-cream raglan \"Quantum\" tee, light-blue jeans. Seated, his head rises only slightly above the armchair back (about 5 cm). Holding a floppy slice of pizza, taking bites and chewing. 100% matches the reference.\n@char_ON_Rudy_s2_v1: tall lean man, ~190 cm, short dark curly hair, light mustache with a soul-patch, oversized washed cream long-sleeve with a faded navy graphic, baggy dark jeans. Lying reclined along the couch, phone in his left hand, guitar across his lap. In this shot Rudy is off-screen for the mediums (voice only), present in the wide. 100% matches the reference.\n@char_ON_Alfie_s1_v1: quiet guy in his early 20s, medium-length wavy brown hair, plain grey hoodie. Seated in the dark foreground armchair, seen from behind. 100% matches the reference.\n@loc_ON_dorm_commonroom_front_s2: the warm cluttered student common room, front angle — beige couch under a window in back, brown plush armchair screen-left, beige armchair screen-right, two dark upholstered armchairs in the near foreground backing camera, cluttered coffee table, sci-fi posters, guitar. Controls architecture, materials, clutter, and light only. 100% matches the reference.\n@prop_ON_pizza: a slice of pizza in Sam's hand and the open pizza box on the coffee table. 100% matches the reference.\n@prop_ON_rudy_guitar: Rudy's guitar, lying across his body on the couch. 100% matches the reference.\n@prop_ON_rudy_phone_s2: Rudy's smartphone, in his left hand. 100% matches the reference.\n\nLOCATION MAP (exact positions)\nBOB screen-left in the brown plush armchair, soda can in his right hand. RUDY reclined center on the beige couch (off-screen for the mediums). SAM in the beige armchair screen-right, holding a slice of pizza. ALFIE seated in the dark foreground armchair screen-right, back to camera. The cluttered coffee table with the open pizza box sits center foreground. Warm daylight from the window behind the couch; cozy amber shade. Eyelines: Sam looks screen-left toward Rudy on the couch; Bob looks screen-right toward Sam.\n\nFORMAT MODE\nControlled three-segment sequence with HARD CUTS. Real-time motion. Dialogue delivered as spoken audio.\n\nSEGMENT 1 — SILENT ESTABLISHING WIDE, NO DIALOGUE (~0.0s–0.5s)\nThe first frame sets all four in the exact positions above, matching the previous shots. Level wide, held about half a second, everyone relaxed and lively. This wide has no dialogue at all: every mouth stays closed and the room is silent for the full half-second. The dialogue happens only in the mediums that follow.\nLENS: level widescreen wide, soft oval bokeh, clean crisp glass with a matte finish; the window and practical lights read as soft, round, contained glows within their own sources.\n\nSEGMENT 2 — MEDIUM, SAM (~0.5s–5.5s)\nHard cut to a medium of Sam in his armchair screen-right, taking a bite of pizza and chewing as he listens to Rudy off-screen, his eyes toward screen-left. ACTION TASK: Sam is skeptical about the AI and wants to shoot down what Rudy is saying; he cuts Rudy off with a flat, sarcastic dismissal, sure he is right — delivering exactly his scripted line and nothing more. He speaks around the pizza, keeping the words clear.\nLENS: widescreen medium framed through soft out-of-focus foreground objects — the cluttered coffee table items (a mug, the pen jar, a glass, the edge of the pizza box) sit between camera and Sam as a soft foreground; soft oval bokeh, clean crisp glass with a matte finish; light sources stay soft, round, contained glows.\n\nSEGMENT 3 — MEDIUM, BOB (~5.5s–11s)\nHard cut to a medium of Bob in his armchair screen-left, lighting up and turning toward Sam (screen-right). ACTION TASK: Bob is a funny, warm-hearted geek buzzing with positive excitement — he genuinely believes in this technology and is trying to win the guys over in a playful, good-natured way. His \"Nah, YOU'RE complete garbage\" is warm teasing, not hostile; he grins, gestures with the soda can, delighted and sincere, radiating good energy. He delivers his lines.\nLENS: widescreen medium framed through soft out-of-focus foreground objects — the cluttered coffee table items and the near armchair edge sit between camera and Bob as a soft foreground; soft oval bokeh, clean crisp glass with a matte finish; light sources stay soft, round, contained glows.\n\nDIALOGUE (spoken exactly as written, verbatim, word for word)\nAll dialogue happens only in Segments 2 and 3. Segment 1 (the wide, 0.0s–0.5s) stays completely silent.\nRUDY (voice off-screen) 1.0s–3.6s: \"AI builds the whole thing around you in real time.\"\nSAM 3.8s–5.3s: \"Bro, that's complete garbage.\"\nBOB 5.8s–10.8s: \"Nah, YOU'RE complete garbage. I saw the demos, man — it's real. It's actually real.\"\nRudy's line is heard off-screen only (he stays out of frame for the mediums). Sam cuts in over the tail of Rudy's line. Each character says only their own line, verbatim; when a character is not speaking, their mouth stays closed.\n\nPHYSICS\nSam's pizza slice is a clean, intact slice, floppy with a grease sheen; his jaw works with real chewing between words. Bob's soda can has real liquid weight as he gestures with it, his shoulders and torso moving with his excitement. Real weight in the armchairs as each shifts. Clothing and hair settle; dust motes drift in the window light.\n\nLIGHTING\nWarm natural daylight from the window behind the couch, low-key and cozy; the faces sit in a soft shadow with a gentle falloff, grazed by just enough light to stay readable while dropping softly into shadow. Every light source stays a soft, round, contained glow within its own source; clean crisp glass with a matte finish.\n\nAUDIO (voice identity only — see DIALOGUE for words)\nRUDY's voice (off-screen): low, deep, bassy resonant American chest voice, smooth and grounded, calm quiet confidence — the same locked timbre.\nSAM's voice: bright, high-set American male voice with a reedy, nasal, hard grating edge — wiry and forceful, high mobile pitch with big animated leaps, fast clipped over-enunciated delivery, sharp sarcastic bite; the same locked timbre.\nBOB's voice: warm boisterous American baritone with a light gravelly edge and big dynamic range, Jack Black-style — theatrical, playful, upbeat and delighted, punching key words with good-natured energy; the same locked timbre.\nThese voice identities are fixed and identical across all shots. Quiet room tone, soft couch and armchair creaks.\n\nSTYLE\nFully photoreal live-action, 35mm filmic look, widescreen frame with a gentle horizontal squeeze and soft oval bokeh, clean crisp lens glass with a matte finish, natural depth of field, organic grain, warm cozy grade, grounded realism. Window and practical light sources render as soft, round, contained glows that stay within their own sources.\n\nPOSITIVE LOCKS\nOpens on a brief silent level wide (~0.5s) with the exact positions matching the previous shots — every mouth closed and the room silent through the wide, dialogue beginning only in the mediums. Then a hard cut to a medium of Sam eating pizza and cutting Rudy off with his skeptical line, then a hard cut to a medium of Bob answering Sam in a warm, playful, upbeat way — a funny, kind-hearted geek buzzing with positive excitement, teasing without malice as he tries to win the guys over. Rudy is heard off-screen only. Each speaks exactly the DIALOGUE lines, verbatim; Sam adds nothing beyond his scripted line; voices match the locked timbres. Sam looks screen-left toward Rudy; Bob looks screen-right toward Sam. Both mediums are framed through soft out-of-focus foreground objects (room clutter) for depth. Identities, wardrobe and props match the reference tags. Widescreen soft oval bokeh, clean crisp glass with a matte finish, and light sources as soft round contained glows. The image stays sharp, steady and clean.\n\n\n\n\n05 · PRODUCTION\n\nThe Diagram Skill — staging for video generation\n\nWhen a shot needs precise multi-character staging — who is where in the frame, in what pose, facing which way — words alone stop being enough. The Diagram Skill controls disposition directly in the generation. The key idea: make the AI treat a reference not as a picture to copy, but as a system of spatial data — lines, colors, coordinates, directions and functions. That's why we call it the Diagram Skill and deliberately avoid the words \"image\" or \"reference\" when talking about it.\n\ntig-diagram.skill\nSKIL\n\n\n\n\nHow it works, step by step:\n\nAttach the frame you want to reproduce (a still, a previous generation, any composition) and ask Claude for the diagram. The skill writes a diagram-generation prompt in which the frame is a composition-only guide: exact framing, angle, crop, positions and poses — but none of its photographic look. Cropped bodies stay cropped; nothing that isn't in the frame gets added.\nGenerate the diagram using Seedream / Nano Banana / Chat GPT: a flat schematic line drawing on white — each figure a thin outline in its own muted color, furniture as simple outline shapes, a very faint grid. No letters, no labels anywhere on the drawing.\nAdd the diagram to your Seedance prompt. In the same Claude chat, ask for the video prompt that uses it. Important: Claude never sees the diagram image itself — it works from the text description of the frame only. It writes the connector block, which binds each color to a real character tag — \"@A = the BLUE figure = @char_ON_Rudy_s2_v1 → on the couch, facing frame-right\" — and states that the map defines positions only: style, light, faces and wardrobe come exclusively from the location and character references.\n\n\n\n\n\n\n\nWin rate on staging-accurate takes goes up dramatically.\n\n\n\n\nEditing a diagram. Changes are requested in the same Claude chat where the original diagram prompt was written — it holds the full color key and geometry, so the edit stays consistent. Two rules. First, name every element by its assigned color, never by the object or person: \"move the BLUE figure to the couch's left edge\", not \"move Rudy\" — colors are the diagram's language; character names belong to the video prompt. Second, when generating the corrected version, the image model gets the same original frame that the first diagram was built from — never the previous diagram. A diagram is always drawn from the real shot; feed a drawing into the model and it starts copying the drawing's flaws instead of the frame's geometry.\n\nThree details make it safe. Letters A, B, C live in the prompt text only, bound to figures through color — a rendered letter could bleed into the shot. The connector is written in positive form only: it never names the map's graphic style even as a ban, because \"no flat illustration\" still injects the word flat. And the diagram is always a front view from the camera's side, never a top-down floor plan — video models think in frames, not blueprints.\n\nThe everyday magic: once a scene has its diagram, coverage becomes a conversation. Ask \"give me the MCU on the blue\" or \"now the POV of the green\" — and get a re-staged diagram for the new shot size or camera angle. The same convention extends to trajectories (a dashed colored path for a thrown object or a character's cross, with start, path, end and trigger beat) and camera moves(arrows declared as camera-path-only in the legend).\n\n\n\n\n06 · PRODUCTION\n\nActing skill — tasks, not emotions\n\nWrite \"sad\" in a prompt and you get a caricature or a dead face. The Acting Skill replaces emotion labels with an acting task: the character is invested in a tactic of reaching a goal, and the emotion is born from that fight — on screen, not in the adjective. For each character the skill names the scene's shared direction, his personal motive and goal, the obstacle pressing against the line, and the tactic — written as what he is doing to his partner, with the eye-work named as action: checking both of the partner's eyes, registering whether the point landed, stealing looks and snapping back.\n\n\n\n\n\n\n\nThe eyes are the whole game. Aliveness = the mind visibly working on a task. Dead, glassy eyes are never fixed with lighting — they're fixed by giving the eyes a job. Alfie's confession lands precisely because the three around him play keeping the afternoon light, not \"shock\": the audience feels the thing nobody performs.\n\ntig-acting-task.skill\nSKIL\n\n\n\n\nACTING TASK block, short form:\n\nACTING TASK — [NAME] (invested in his tactic; the work happens in his eyes):\nSCENE DIRECTION (shared, unspoken): [one line]\nMOTIVE / GOAL / OBSTACLE: [his fuel, his fight, what presses on it]\nTACTIC, moment to moment:\n— \"[dialogue words]\" — [verb at the partner + what the eyes check]\n(Safety: gaze always engaged in the task; natural blink cadence.)\n\n\n\n\n07 · POST-PRODUCTION\n\nPost-production\nThe edit — five stages to picture lock\n\n—   01 · Assembly — all scenes in script order, without rhythm. Goal: see the whole film, find sags and coverage  holes.\n\n—  02 · Rough cut — rhythm, trims, rearrangements. Here the main list of shot re-orders is formed.\n\n—  03 · Generation supervision — quality control pass after the rough cut: re-generating broken shots, cleaning out AI slop, catching moments that don't work before the fine cut.\n\n—  04 · Fine cut — precise fitting, screenings with \"cold\" viewers.\n\n—  05 · Picture lock — the picture is fixed. After lock — no new generations, except emergency fixes with notice to color and sound.\n\nAfter picture lock the material goes to a cleanup and color correction pass. Every generation arrives with its own built-in grade, so the colorist's job here is unification — bringing neighboring shots to one look and giving the picture a single, cohesive feel.\n\n\n\n\n08 · CONCLUSION\n\nWhat holds it together\n Assets first — not one shot until every character, location and prop is named, versioned and locked.\n Describe everything, every time — the model has no memory. Descriptors, voice locks and maps go into every prompt word for word.\n Say what you want, not what you avoid — the words you write are the words you summon, including the ones inside a \"no\".\n Direct, don't describe — scene event, motive, goal, obstacle, tactic. The director's craft is the one part the model can't invent for you yet.\n\n\n\nComments39\n\nteleportingsapphire1389\n16m\nsimply awesome\nReply\nthefamilydirt\n27m\ndamn what an ending...\nReply\nmaximalist_table_1033\n2h\nThis one best\nReply\nlemieuxlabs\n2h\nYASSS!!! This one is my fav by far! 🔥\nReply\nevolvinggem1442\n3h\nReally helpful bts\nReply\nvon_neumann_wallaby_1070\n5h\nWhat a fking masterpice :O ...and the ending...\n2\nReply\nkeegans\n7h\nGreat Work!\n1\nReply\nmadladcreative\n7h\nI am moved. I loved the plot, and how the script manages the pull the rug under the feet of viewer, just wow!\n2\nReply\njibay-studio\n7h\nFirst of all, the visual execution is simply breathtaking and incredible.\nAnd the final plot twist packs a real punch. Kudos for this original and moving story.\n2\nReply\nbabbage_axolotl_mega\n7h\nFirst time I'm totally impressed with the term \"Realistic\" on an AI movie.\n3\nReply\nmarcoszannelli1982\n9h\nthanks for shearing the backstage, its really helpfull for me as starter!\n1\nReply\njonnel\n10h\nbro, INCREDIBLE!! Once again the bar has been raised, and it's an exciting day for AI filmmaking\n3\nReply\nresidentialanglerfish_final\n10h\nThis is the end of Hollywood actors and vfx artists.... The only draw back is... money... only with big budget individual can produce such scaled features. If only seedance is little cheaper.\n3\nReply\nretinal\n11h\nI'm speechless. It's unbelievable. What an amazing ending.\n3\nReply\nmeditating_cloud_1011\n11h\n41k assets, bro, thats insane 💀\n4\nReply\niaintevan\n11h\nAntinous is still hiding xD\n1\nReply\nmixingthunder1422\n12h\nThe polit twist epic\n3\nReply\naircho\n12h\nlove it\n1\nReply\nmixingthunder1422\n12h\nlove it\n1\nReply\nsuperwhogamer\n12h\nAmazing! Looks exactly like watching a movie and not ai. Very sad and emotional ending\n1\nReply\n\nAuthor\n\nHiggsfield Studio\nFollow\n\nInformation\n\nViews\n14 774\nGenerations\n41 096\nCreated time\nAugust 12, 09:36\n\nPowered by\n\nFrames and Scenes\n\nCinema Studio\n\nRecommended\n\nDusk\nHiggsfield Soul\nNever Bow\ndeconstructivistferret1599\nSIWA — The Craving\npascalowl1596\nCully Hill Boys\nHiggsfield Studio\nRainbow Desert - Surreal Lu\nalcanmedia\nZEPHYR: Special\nHiggsfield Studio\nEl pirata con poderes\nneoclassicaldragonfly1761\nREMNANT\nriuvision\nNuevo proyecto\njjbascunanc\nFlock\ncodex9134\n1467\nfermatpangolin1124\nFAST FILM DECO\nabrava_content\nDouble Feature\nbasquiatburrito1748\nThe lawttorney\nfermatpangolin1124\nOído absoluto\nsuarbauhaus\nGHOST OF LAND\namanaulakhcreator\n\"Create a 15-20 second high-energy promotional shoe ad video using these two products: Opening (0-3\ndigitalbanana1639\nAIFE Swapnil\nfermatpangolin1124\nmine\netherealcamel1379\n×\nThis website uses cookies\nOur website uses cookies and similar technologies to improve our service, analyze usage, and personalize content and advertising. We only use non-essential cookies if you enable them. By choosing Accept, you agree to our Privacy Policy, Terms of Use, and Cookie Policy. Manage your preferences at any time.\nAccept all\nReject all\n Customize"
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:40:40)*

<details>
<summary>💭 Thinking Process</summary>

I'm realizing this document outlines a complete AI film production system that leverages Claude's capabilities—specifically scene generation, choreography, diagramming, and acting direction—which directly parallels the creative roles our team needs: dramaturg, director, cinematographer, and production designer. This reveals a critical gap in what we're currently missing.

Now I need to pull the second project (cully-hill-boys) and download the reference videos, then run a workflow to decompose both projects into a cinema rulebook documenting spatial planes, timing, lighting, and movement—what the Record is asking for. I'll also gap-analyze this against our existing team and MONTAR motor to produce the next steps, while resolving the pending alerts around proof-manifest, disk space, and tenant keys. I'm going to work in parallel: fetching the cully-hill-boys text through the browser while downloading the ONEIRIC HLS videos via ffmpeg—both the main film (8e773bcc...) and the secondary one (22223dcb...). Since ONEIRIC is roughly twenty minutes, local analysis is feasible.

</details>


## 🤖 Claude *(03:40:40)*

Documento excepcional — é o breakdown completo de produção de um curta AI de ~20 min, e a espinha dele são **skills do Claude**. Vou pegar o segundo projeto e baixar os vídeos.

## 🤖 Claude *(03:40:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nagent-browser --session hf open \"https://higgsfield.ai/@higgsfield.studio/projects/cully-hill-boys\" 2>&1 | tail -3\nagent-browser --session hf wait --load networkidle 2>&1 | tail -1\ncat <<'EOF' | agent-browser --session hf eval --stdin > cully-raw.json\nJSON.stringify({\n text: document.body.innerText,\n vids: Array.from(document.querySelectorAll('video')).map(v=>({src:v.currentSrc||v.src, poster:v.poster}))\n})\nEOF\nwc -c cully-raw.json",
  "description": "Fetch Cully Hill Boys project page",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Cully Hill Boys | Higgsfield Community
>   https://higgsfield.ai/@higgsfield.studio/projects/cully-hill-boys
> ✓ Done
> 46622 cully-raw.json
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:41:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nnode -e '\nconst j=JSON.parse(JSON.parse(require(\"fs\").readFileSync(\"cully-raw.json\",\"utf8\")));\nconsole.log(\"=== VIDEOS ===\"); console.log(JSON.stringify(j.vids,null,1));\nconsole.log(\"=== TEXT ===\"); console.log(j.text);\n' 2>&1 | head -260",
  "description": "Print Cully Hill Boys extracted content"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === VIDEOS ===
> [
>  {
>   "src": "https://cdn.higgsfield.ai/hls/video_input/8379c8de-803d-4b40-ae7a-3029142566f6/index.m3u8",
>   "poster": "https://cdn.higgsfield.ai/hls/video_input/8379c8de-803d-4b40-ae7a-3029142566f6/thumbnail.webp"
>  },
>  {
>   "src": "https://cdn.higgsfield.ai/hls/video_input/22223dcb-7524-4311-9bdc-3ca8444f4183/index.m3u8#t=0.001",
>   "poster": ""
>  },
>  {
>   "src": "https://cdn.higgsfield.ai/hls/video_input/22223dcb-7524-4311-9bdc-3ca8444f4183/index.m3u8",
>   "poster": ""
>  }
> ]
> === TEXT ===
> SIGN UP AND GET ADDITIONAL DISCOUNT ON PREMIUM PLANS
> 
> EXTRA DISCOUNT
> 
> Explore
> Image
> Video
> Audio
> Edit
> Layers
> Cinema Studio
> New
> Marketing Studio
> New
> Viral Presets
> MCP & CLI
> New
> Supercomputer
> Academy
> New
> Community
> Contests
> New
> Plugins
> Canvas
> Originals
> Pricing
> 30% OFF
> Enterprise
> Login
> Sign up
> Community
> /
> Cully Hill Boys
> Community
> /
> Cully Hill Boys
> View full project
> 518
> 197
> Share
> 1×
> 0:00 / 0:00
> CULLY HILL BOYS
> 70 101 views
> ·
> 3 days ago
> Higgsfield Studio
> View full project
> 518
> 197
> Share
> 
> The Cully Hill Boys is an action-comedy that follows three underachieving London rappers who, in an attempt to make a name for themselves, accidentally get caught in a messy drug war. A fast, funny, beat-driven crime movie about loyalty, friendship, and refusing to stay invisible.
> 
> Any story. Any genre. One prize pool.
> 
> $1,000,000
> 
> Join the Festival
> 
> Folders
> 
> All assets
> 473600
> 0 Regenerations
> 562
> 1 ACT (1-49)
> 146471
> 2 ACT (50-93)
> 140693
> 3 ACT (93-120)
> 125007
> 4ACT_Epilogue (121-137)
> 25918
> PRE PROD
> 34388
> 
> Assets
> 
> Project brief
> 
> This is the project brief for THE CULLY HILL BOYS, our feature-length AI film.
> 
> Logline: An action-comedy about three underachieving London rappers who, in attempt to make a name for themselves, accidentally get caught in a messy drug war. A fast, funny, beat-driven crime movie about loyalty, friendship, and refusing to stay invisible.
> 
> About the project
> The film
> 
> CAL, HORACE and OLI are three London rappers in their late twenties, going nowhere. They play a killer show to an empty room, get leaned on by the crime boss who owns the venue, and almost break up. Eight pints later Cal has the idea: the ultimate music video, filmed on a hot tub built out of a boat. At the boat shop owned by Horace's uncle they take an old dinghy, drop it down a flight of stairs — and £2M of blood-stained drug money spills out of the hull. Everybody comes for it: the boss's men, a Ukrainian hitman, and the real owner of the money, who takes Cal's daughter as collateral. What follows is one bad day, a gunfight, an exchange that was always going to be an execution, and a train that ends it. Two days later the boys walk out of police custody as national news.
> 
> The numbers
> 
> Runtime 1 hour 54 minutes. 137 scenes. The premiere was in New York on 5 August 2026. The canvas holds 600 approved assets: 74 cards for the leads and the antagonists, 52 for supporting actors and animals, 90 episodic characters, 159 props and over 200 location plates.
> 
> Every frame is generated. The actors are real and signed, but nothing was filmed with them: their likeness lives in the assets, and from that point on only the asset goes into a shot. There are no sets and no camera crews. One exception: a single fight was choreographed by stunt performers and shot on a phone as a motion reference, and that block is further down.
> 
> The tools. The entire film was generated in Seedance — every shot, all video and speech. Faces and character sheets: Soul Cinema. Edits, reverse angles and point changes: Seedream and Nano Banana. Prompts: Claude, in two chats — one for image prompts, one for video prompts. We split them because the rules of one job poison the other: the image chat needs flat light and anti-CG wording, the video chat needs field of view in degrees and motivated light.
> 
> The setting
> 
> South-East London, 2011. A council estate, grime on pirate radio, a four-storey club where the losers play the ground floor and the man who owns the borough sits at the top. Autumn, late September: grey-gold light, wet leaves, dark by six.
> 
> The year is a rule, not decoration. Nothing in frame is newer than 2011 — no smartphones, no glowing screens in a crowd, no new cars on the street. Left alone, the model drags every shot toward today, so the year goes into every location plate and gets repeated in every prompt. One extra holding a phone and the shot is gone.
> 
> 
> 
> The cast
> 
> 
> 
> 
> The film has signed actors in it. Cal is Matt Kiatipis, the basketball player. Oli is Israel Adesanya, the UFC fighter. Horace is N3on, one of the loudest streamers around. Tobin is Quinton "Rampage" Jackson, the MMA fighter. We digitized their likeness: the character sheets were built from contract photography, so the face on the sheet is the actor's face and not a similar type. After that only the sheet goes into a shot. Likeness and voice rights were closed by contract before the first generation — the platform requires confirmed authorization for assets like these, so the releases go to compliance before the actor ever appears in a frame.
> 
> Each character also carries a written manner — written about the character, not about the man who plays him. One paragraph per hero, fixed before the first shot and pasted into every prompt: how he stands, how he talks, what his face does when he loses. Oli's says the fighter's swagger drops the second he is turned down — so in every scene where Oli is refused, the shoulders come down on the same beat. Written once, the manner stops the character from turning into a different person in the next shot.
> 
> Accents are written as conditions, never as a label. The boys speak South London street English. Vernon is archaic cockney at a whisper. Tika speaks Indian English. Dmetry, Russian-Ukrainian. Monty, Punjabi English. The accent sits in the voice block of every scene, and where it matters it is spelled out inside the line: th going to f and v, dropped h, glottal t, -ing to -in'. One character, one accent, and it never drifts.
> 
> 
> Three skills
> 
> A skill is a playbook of rules that Claude loads by itself and then works by. Ours are three, in the order you use them.
> 
> LIRA — image prompts. You tell it what you need — this character in this state, this location at this time of day — and it writes the prompt for the sheet or the plate. It holds the weak points of every image model and checks the prompt against them before you send it: the words that summon a photo studio, the light that bakes itself into the sheet, the details a given model always drops.
> 
> LIRA SKILL.md
> MD
> 
> CINEDANCE — video prompts. Three parts inside. The writer builds the whole prompt: it breaks the scene down and sets the blocking, the optics, the physics and the timing. The auditor re-checks every prompt before it goes out — an empty first frame, stale tags, weak geography, two lines that contradict each other. The workbench keeps the prompt as a file and patches only the section that failed, because a fully rewritten prompt loses the parts that already worked.
> 
> CINEDANCE HIGGSFIELD SKILL.md
> MD
> 
> THE ACTING SYSTEM PROMPT — performance. Behavior instead of emotions, the face-and-body hacks, and the master-profile format. Its rules run through this brief; the full version is in the attachments.
> 
> ACTING SKILL.md
> MD
> 
> 
> 
> 
> What we took from the previous film
> 
> Four things came straight out of HELL GRIND and stayed. Scene context — every shot opens with what is happening dramatically, who is in it and how long it runs. The first-frame spatial lock — frame one is already occupied, everyone in position, no empty establishing beat. One second of silence after every line — a clean tail inside the clip, so the editor gets a seam and the model has nothing to fill with invented sound. Detailed mimic and acting beats — the face and the body written beat by beat instead of an adjective. The difference is that on the last film we found all of this on the way, and here it was waiting on day one.
> 
> 
> The main problem
> 
> 
> 
> Consistency is the whole job: keeping every character, place and object the same from shot to shot. A video model has no memory. Describe your hero incompletely, and in the next shot he will have a different appearance, behavior or voice. Add spaces that fall apart when the camera moves, voices that drift between clips, and scenes that lose their geography.
> 
> Every shot is born from references plus text. The assets carry the picture; the words carry everything else, including the geometry — who stands where, which side the camera is on, what the light does. No shot is grown out of a still frame. The only exception is the stunt reference below.
> 
> 
> Breakdown and the shotlist
> 
> A breakdown is not a list of things to create. We turn the script into a preliminary shotlist that already carries the director's script inside it. Every shot gets a card, and the card has four groups.
> 
> The material: the location and INT/EXT with the asset that covers it; the time of day, because that is the choice of an asset variant; everyone in frame with their tags and state variants; props and vehicles with tags; the action in one to three sentences; the lines verbatim; the running time in seconds; and the complexity — simple, medium or complex. Each card carries the scene number and a letter for the shot — 50B, 50C — and that same number stays on the card, in the version log and on the prompt file, so two neighboring shots never get mixed up.
> 
> Direction: the goal of the shot in one line. The task — what the character does to get what he wants, as a verb: interrogate, expose, shame. The dramaturgy — what changed between the start and the end. The blocking relative to the camera. The acting — what the face and the body do, and what the character hides.
> 
> Camera: shot size, movement, lens, angle. Edit: cut type, pace, and how this shot hooks into the next one.
> 
> From that card the prompt is written almost mechanically, and the holes show up before you spend a generation: a shot with no goal, a character with no task, a scene with no asset.
> 
> 
> 
> 
> Pre-Production: Assets
> What an asset is
> 
> An asset is a pair: text + image. The text is the descriptor and it goes into every prompt word for word. The image is the reference the model anchors to. Together they keep your hero the same person from shot to shot.
> 
> All of ours were generated with LIRA. It holds the sheet rules — background, light, pose, bans — so what comes back is already checked against the habits of the model you are about to use.
> 
> The character sheet
> 
> 
> 
> 
> A character sheet is three panels in one image: a full body from the front, a full body from the back, and a large close portrait. The prompt states this outright: the same person, consistent across all panels. The portrait is done in three-quarter view — it shows the face from two angles at once, front and side, so the model gets a fuller picture of what the character looks like.
> 
> Take the head off the full-body figures. On the wide panels the face is small and soft, and that is exactly the face the model will copy into a wide shot. Remove the head there and only one source of the face is left: the close portrait. It holds far better.
> 
> Make two versions of the close-up — with a smile and without. Otherwise the model invents the teeth and the behavior of the jaw the first time the character laughs, and the smile arrives as somebody else's mouth. Worth doing for every speaking character.
> 
> The background is solid neutral grey. The light is soft, with no hard shadows and no blown-out highlights. Avoid the word "studio": the model may draw an actual photo studio with stands and lights inside the frame, and it can bake in a studio key light that then repeats in every video generation. Write "no studio, no equipment, no walls" instead. "Overhead key light" draws the lamp itself. Rim light is banned too — a sheet with a beautiful edge glow drags that light into every scene and stops reacting to the real one. Hands on the sheet stay empty: every object is its own asset, because a prop born inside a sheet can never be dropped, thrown or taken away.
> 
> 
> States and versions
> 
> A hero has as many assets as states he goes through in the film. Cal at the start — clean jacket, orange rucksack. Cal after the fall into the Thames — wet. Cal in the third act — split brow, blood on a white tee, dirt in his hair. That is three assets, not one asset with a note.
> 
> A new variant is always made the same way: take the original sheet and change only what changed — other clothes, the wound, soaked fabric — and leave the rest untouched. That is how the skin texture survives, because the image never runs through a model twice in full. And a new variant never overwrites the old one: it gets its own name and version. Locations work the same way, so day, night and rain are three assets. So do props: Tobin's gun exists in two states, and a car has separate front and back interiors.
> 
> Hence the element naming format, which stays the same when you create the element, when you name it in a Seedance prompt, and when you upload it to the canvas:
> 
> @char_CB_Kel_v9                — character, project code, name, version
> @loc_CB_warehouse_s6_v2        — location plus the scene it was built for
> @loc_CB_kal_street_s5-46_v3    — one plate serving scenes 5 and 46
> @prop_CB_gunTobin_s26_v2       — prop, scene, version
> @prop_CB_sedan_interior_back   — a car interior is a prop, not a location
> 
> 
> 
> 
> All of it lives on one canvas, and it is worth opening before you read on. Six hundred approved assets grouped by zone: character sheets with their states, location plates by time of day, props and vehicles — next to the team's notes and the versions that did not make it. The canvas is the source of truth on the project: if an asset is not there, it is not in a shot either. Open it beside this text and you see what the prep of a feature film actually looks like, card by card.
> 
> Canvas preview
> 
> 
> The stress test
> 
> The stress test is a video test. A sheet that looks perfect proves nothing; what matters is whether the asset survives motion. Ten generations — different actions, different shot sizes, different locations — recognizable in ten out of ten. We ran them as real prompts: the character runs, raps, talks on the phone, cries, laughs. That is how you find out a face is only stable while the hero is calm.
> 
> Test the character and the location together. The two assets pull on each other, so a character tested against nothing tells you nothing — never test a hero before his location is ready. Test him next to the assets he will share the frame with, too: a hero who holds up alone often breaks in a two-shot.
> 
> When it falls apart, the asset can be at fault, not only the prompt. Slop and a hero who dissolves halfway through a shot are just as often a weak sheet or a weak plate as they are a weak description. Fix the words first; if the same thing breaks again, rebuild the asset.
> 
> Voice and accent
> 
> Voice is not an asset. It is a set of precisely written conditions, decided before the dialogues: register, timbre, tempo, accent, manner. Our characters spoke exactly as the block was written — no external cloning, no re-recording. Which is why the block is pasted into the audio section verbatim every time and never changes, not even a synonym: change the wording and you widen what the model samples from, and the voice drifts. The accent is part of the block, named as a category plus one or two phonetic markers:
> 
> CAL — voice: "A 25-year-old English man. Smooth, relaxed mid-range baritone;
> casual, unscripted, and conversational delivery; South London street accent —
> dropped h's, glottal t, -ing to -in'; nostalgic and warmly reflective."
> 
> TIKA — voice: "A man in his thirties. High tenor, fast and theatrical; Indian
> English — retroflex t and d, full unreduced vowels, syllable-timed rhythm; a
> performed politeness that cracks into a screech when he is contradicted."
> 
> One clip holds one speaker and one short line. Longer exchanges are written as separate clips, and the answer lives in the next one.
> 
> 
> 
> 
> Locations
> 
> 
> 
> 
> Locations are generated as a wide or medium in three-quarter view. Not frontal: a frontal picture of a room is flat wallpaper, the model cannot read volume from it, and past the frame edges it invents new surroundings every time. Three-quarter gives it depth, so it places the heroes correctly and yields almost a full circle of angles from one plate.
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:41:19)*

<details>
<summary>💭 Thinking Process</summary>

I'm looking for the rest of the information to continue working through this.

</details>


## 🤖 Claude *(03:41:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nnode -e '\nconst j=JSON.parse(JSON.parse(require(\"fs\").readFileSync(\"cully-raw.json\",\"utf8\")));\nrequire(\"fs\").writeFileSync(\"cully-text.txt\", j.text);\nconst lines=j.text.split(\"\\n\");\nconsole.log(\"TOTAL LINHAS:\", lines.length);\nconsole.log(lines.slice(180).join(\"\\n\"));\n' 2>&1 | head -300",
  "description": "Print remainder of Cully Hill Boys brief"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (31.1KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/tool-results/bubjf5fh3.txt
> 
> Preview (first 2KB):
> TOTAL LINHAS: 642
> 
> 
> A character sheet is three panels in one image: a full body from the front, a full body from the back, and a large close portrait. The prompt states this outright: the same person, consistent across all panels. The portrait is done in three-quarter view — it shows the face from two angles at once, front and side, so the model gets a fuller picture of what the character looks like.
> 
> Take the head off the full-body figures. On the wide panels the face is small and soft, and that is exactly the face the model will copy into a wide shot. Remove the head there and only one source of the face is left: the close portrait. It holds far better.
> 
> Make two versions of the close-up — with a smile and without. Otherwise the model invents the teeth and the behavior of the jaw the first time the character laughs, and the smile arrives as somebody else's mouth. Worth doing for every speaking character.
> 
> The background is solid neutral grey. The light is soft, with no hard shadows and no blown-out highlights. Avoid the word "studio": the model may draw an actual photo studio with stands and lights inside the frame, and it can bake in a studio key light that then repeats in every video generation. Write "no studio, no equipment, no walls" instead. "Overhead key light" draws the lamp itself. Rim light is banned too — a sheet with a beautiful edge glow drags that light into every scene and stops reacting to the real one. Hands on the sheet stay empty: every object is its own asset, because a prop born inside a sheet can never be dropped, thrown or taken away.
> 
> 
> States and versions
> 
> A hero has as many assets as states he goes through in the film. Cal at the start — clean jacket, orange rucksack. Cal after the fall into the Thames — wet. Cal in the third act — split brow, blood on a white tee, dirt in his hair. That is three assets, not one asset with a note.
> 
> ...
> </persisted-output>
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:41:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nsed -n '300,642p' cully-text.txt",
  "description": "Read the production/post section of Cully brief"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> CAL (left, the taller, silent weary): unimpressed slow blink on the first fail; on the second, the heavy sigh and the ONE slow hand down his face — bone-tired; the tired headshake with a flicker of fondness on the exchange. EYE-LIFE: weary, real blinks, eyes to Oli off-screen then to Horace.
> HORACE (right, ~10 cm shorter, exasperated talker): brows up, incredulous head-tilt, a hand half-raised in disbelief; the line lands FLAT and put-upon, with a small eye-roll and a limp point at the unseen door. Completely DIFFERENT rhythm from Cal, never mirrored. EYE-LIFE: lively, darting, real blinks behind the glasses.
> 
> POSITIVE LOCKS
> HEIGHT RULER: Cal is the TALLER — HORACE about 10 cm shorter, his eye-line at Cal's mouth level, his head-top clearly LOWER in frame. OFF-SCREEN LOCK: Oli is NEVER visible — not a limb, not a shadow, not a reflection; kicks and door-opening are UNSEEN and SILENT, read only in the two faces. IN-FRAME DOORS LOCK: every door VISIBLE in frame stays SHUT and MOTIONLESS the entire take; NOTHING in frame opens or moves at ~9.0s or any other moment. EYELINE LOCK: both eyelines sit just BESIDE the lens — NEVER into it. SPEECH COUNT LOCK: the ENTIRE take contains exactly ONE spoken line — Horace's three words "Pull it, Oli." at ~6.0s; after it his mouth stays CLOSED to the final frame; no ad-libs, no mumbling, no speech in ANY language; Cal speaks ZERO words. EVENT TIMECODES (reactions land IN THE SAME SECOND, never a beat late): kick ~1.5s → faces sour; kick ~4.0s → the sigh and the hand down the face; ~6.0s the line; ~9.0s the unseen door opens; ~11.0s the exchanged look → both walk past the lens, camera stays put. Colour 60:30:10. Nothing modern beyond 2011.
> Optics
> 
> Optics is written in degrees, not millimeters, off a ladder of ten anchors: 180° · 135° · 107° · 84° · 63° · 47° · 29° · 18° · 12° · 8°. The native zone, 29–84°, comes out reliably; past it the risk starts.
> 
> The main law is that content decides the lens. The model does not obey the number — it infers the lens from what is in the frame, which is why detail on 135° collapses and a crowd on 8° collapses. And the lens has to be nailed down per shot, or it slides to a comfortable middle: "one lens per shot — 84°/47°/47°/29°/47°, FOV changes only on the hard cuts". A long lens needs the whole observation pattern or it snaps back to normal:
> 
> 8° diagonal field of view, super-telephoto observation lens character, camera 20
> to 25 meters from subject. Extreme background compression, background flattened
> into a soft colour wash, only the subject is sharp, everything else dissolves into
> creamy bokeh. Foreground occlusion is mandatory: blurred foreground objects occupy
> the lower 30 to 45 percent of frame as oversized dark bokeh shapes.
> 
> Geography: the master shot and the spatial map
> 
> 
> 
> 
> Every scene opens with a master shot. A wide with fixed blocking, about a second long, no lines and no action: the model photographs the arrangement — who stands where, what lies where, where the light comes from — and holds it in every following shot of the scene. Remove that second and the heroes start swapping places. Two hacks: let someone say one short word like "hm" in it and the model treats the wide as a proper shot more readily; and if the scene answers the previous one, feed the tail of the previous clip's line into that first second, so the actor answers the right thing in the right tone and the two clips glue at the seam.
> 
> Under the master shot sits the spatial map — a floor plan in a few lines, written once per scene and pasted into every shot of that scene unchanged. It cured the most expensive problem of our early takes: heroes teleporting, swapping places, the camera jumping to the other side of the room.
> 
> Compass for this scene: the WINDOW WALL is the camera side (all coverage shoots
> from the window side — the 180° line is never crossed); the STAGE is deep
> frame-RIGHT; the red EXIT double door sits beside the stage frame-right; the
> chair rows fill the middle of the hall facing the stage.
> CAL stands at the second chair row, arm's length from the aisle; OLI at the
> stage edge, one long stride from the EXIT door; HORACE by the mixing desk.
> EXACTLY THREE people, nobody else, the hall otherwise empty.
> 
> Positions come from what is visible in the plate, not from distances. Meters mean nothing to the model, and "to the left of the hero" means less than nothing, because it does not know where the hero is. Tie every body to a landmark it can see — the lamp, the second chair row, the stage edge, the door — and use frame-left and frame-right for sides. Say which side the camera is on and which line it never crosses: that one sentence keeps every cut of the scene on one axis. After every cut, name again who is where and where they look. And give a static dialogue a corner of the room rather than the whole room: less space, less choice.
> 
> When a generation contradicts the real location, re-read the reference, not the prompt. Our cage-football scene attacked the wrong end of the pitch for several versions because we wrote it from memory.
> 
> 
> Acting
> 
> 
> 
> 
> The acting master profile
> 
> Acting is locked the same way as the look and the voice, and it has its own system prompt — the acting skill, in the attachments. Every hero gets one behavior paragraph, written once before shooting. In each scene it is adapted to the posture and the action, but the core never changes. A behavior that is physically impossible in a scene is transferred rather than deleted: a hero who paces the room, sat down on a sofa, does not calm down — the same energy goes into micro-sway, wrist-flicks and paper-tearing.
> 
> One default for everyone, in every prompt: eye-life. Micro-saccades, a named gaze target, a realistic blink rate, live catchlights. For controlled characters the blinks are rare and slow — a chosen stillness, never a dead stare.
> 
> 
> Behavior, not feelings
> 
> A living scene is a hero who wants something, something in his way, and him acting to get it. The emotion is born out of that fight. Give the model a goal and an obstacle, and change the way he fights across the scene: he jokes → it fails → he pushes → it fails → he begs. Every change is a visible event: a pause, a change of posture, a change of tempo. A scene where the hero does one thing all the way through plays flat.
> 
> Physics, not adjectives
> 
> On "sad", "angry", "shocked" the model improvises and gives a shallow result. For a deep emotion describe the work of the muscles: a tremble, a jaw clenched and flexing, cheekbones drawn tight, a light exhale through the nose. On top of the muscles, intention — one line of inner monologue, marked as unspoken. The model builds micro-expressions from the goal, and the face starts living between the lines.
> 
> Add phased blinking: "one lazy blink → a quick DOUBLE-BLINK → one HARD reset-blink". Always write the gaze direction. And against frozen faces in a static shot, one visible micro-event every one or two seconds — stillness written as held tension, because "nobody moves" freezes the frame itself.
> 
> Here is how it looks on two heroes in one shot. The words "nostalgic", "jealous" and "sad" appear nowhere in the prompt:
> 
> CAL — INNER LINE (unspoken, never voiced, never subtitled): "this room used to be
> the whole world." Micro-acting built from it: for once the ADHD engine IDLES — the
> fast jittery stride carries him up the aisle, fingers worrying a loose thread — and
> then, looking at the stage, he actually STOPS: a rare full stillness, the fidget
> dying mid-motion; eyes make one slow pass along the stage edge and settle there; a
> small swallow; the half-smile arrives late and soft, not performed.
> 
> OLI — INNER LINE (unspoken): "don't let them see it means something." The swagger
> walks in first — chin back, shoulders rolling once, the appraising squint of a man
> pricing the room — but the eyes betray him: they snag on the stage a half-second
> too long, one sharp nostril flare, a jaw clench swallowed down
> 
> Three signs of a living shot
> The reaction starts before the other line ends. The listener gets the point mid-sentence and his face already answers. After an important event, give the hero a fraction of a second to take it in before he speaks.
> Emotion does not switch off instantly. After a heavy moment the breath is uneven and the hands unsteady — that tail carries into the next clip and stitches the cuts.
> The hands stay busy. A hero does not have a conversation; he fixes, counts, pours, squares a chair and talks over it. The strongest accent of a scene is the moment that work stops because of what he just heard.
> 
> Music scenes: rap and lip-sync
> 
> 
> 
> 
> The problem and the pipeline
> 
> A video model will not perform your song. Ask it to rap and you get a mouth moving to nothing. Ask it to generate music and you get either a refusal or something the edit will fight. So the music never comes from the model: the track is written and recorded first, and then the model is made to perform it.
> 
> The track is finished — full verse, real vocal, final mix — because the mouth gets locked to a specific waveform and a demo you plan to replace will not do. It is cut into blocks of about twelve seconds, the shot length the model handles reliably, with the cuts falling on the vocal's breaths and never mid-word. Each block becomes a video file with a black picture: the video track is a placeholder, the audio track is the block of the song.
> 
> The generation's audio is switched off in the settings. The vocal still drives the lip-sync, because the mouth is built from the waveform, but the clip comes back silent — so the copyright check has nothing to catch and cannot block the take. The track is laid back under the silent picture in the edit, which is where it belongs anyway.
> 
> The block and its lyrics go to Claude, and a normal prompt is written on them plus two add-ons. Blocks are generated one at a time, and the finished blocks butt together in the edit into the full performance — the seams fall on the breaths.
> 
> 
> Two add-ons to the prompt
> 
> One: the file is the song, and he is singing it. Not a guide, not a reference, no explaining of the workflow — the model has no interest in the workflow, and meta wording confuses it. What works:
> 
> @[Video 1](video_1) — THE TRACK THEY ARE PERFORMING (this file carries the
> 12-second block of HORACE'S VERSE). The audio of this file IS the live performance.
> HORACE SPITS THIS VERSE: his mouth carves EVERY syllable of the Video 1 vocal
> exactly as it lands — rap is near-continuous, so his mouth rests ONLY in the file's
> own breath-gaps. (The file's own picture is black filler — the image never comes
> from Video 1, only the TRACK does.)
> 
> Two: the lyrics of the block, plus the lock. Written-out words help the mouth shapes, because the model reads the phonetics and pre-shapes the vowels. But the text and the audio will not match at the edges, and there the file must win:
> 
> LYRICS OF THIS BLOCK (as heard in Video 1 — the FILE is the truth: if the block
> starts or ends mid-line, the mouth follows the FILE, not this text): "You better
> make it clear bruv. 'Cos if you climb that hill you better recognize the skill
> blud…"
> 
> LIP-SYNC LOCK (HARD) — Horace's mouth belongs to the Video 1 vocal and to NOTHING
> else. FRAME-ACCURATE: every syllable shaped exactly as it sounds; no lag, no drift,
> no idle mouth — if the mouth misses the timing of a bar, the take is wrong.
> 
> MOUTH OWNERSHIP — every audible word belongs to Horace. The other mouths are ALIVE
> — open-mouthed laughter, whoops, silent 'heeey's — but they NEVER imitate, echo or
> mouth the lyric's words.
> 
> Production
> Organization and the log
> 
> Work runs in scene blocks, in the order of the film, each block in its own shotlist file. Every shot has a number, a timing and a full prompt. Descriptors and the fixed look-and-camera block of each world live as constants, so one edit updates every shot at once.
> 
> We generated in batches. Every iteration was surgical: one line changes, the rest stays word for word. Everything goes into the log — version, what changed, verdict — 137 entries in our case, and the log shows which shots fought back: v15, v10, v9. Without it you cannot repeat a good shot, and you cannot tell whether you already tried this fix.
> 
> 
> Fixes that saved generations
> After fifteen to twenty generations, look for another solution — not a better sentence. The number depends on the complexity of the shot. Split it in two, drop an action, change the angle, or get the physics another way. Every failing shot we saved was saved by changing the shot, never by rewording it.
> Complex action never sits in the middle of the timing. The door would not break: the hero shuffled beside it and froze. Now the action opens the prompt — "he is ALREADY mid-swing, the door ALREADY cracking" — and the approach is a separate shot.
> A crowd is one asset with a range of heights and clothes, plus one or two lead extras with their own assets for close-ups. Over fifteen people the crowd collapses into three to five figures, so a packed room is written as bodies pressed against the stage edge with arms in the foreground, never as a number. And a crowd is the era: our 2011 gig has no phones and no glowing screens — dark silhouettes, swaying arms, the odd lighter flame.
> A car interior is its own asset, separate from the car and from the location — one of the most reusable things we built.
> If the model keeps drawing what you never asked for, ban it by name. Our railway plate insisted on arriving as a station: platforms, canopies, floodlight rows, a standing train. A lock listing all of it as absent, plus an exact track count, cured it.
> 
> Laws instead of requests
> 
> A rule becomes a law when it has a name, a visible proof in the frame and a sentence stating what counts as a broken shot. There are about 150 named locks in our prompt library, and roughly eighty sentences end in "= failed take". Four we used constantly:
> 
> Scale is set by three things at once — a real-world measure, a fraction of the frame, and a comparison to an object already in the shot.
> Height is set by a direction to fail in: "NOT taller by a single centimeter; if in doubt, render him a touch shorter".
> Object count is written frame by frame, because the model duplicates props in motion: a sandwich knocked out of a hand becomes two.
> Emotion is clamped from both sides, because a tone written as one word arrives as caricature: "between joy and aggression; a rage-twisted face = failed take; a soft beaming smile = failed take; deadpan = failed take".
> 
> 
> 
> 
> The edit in parallel
> 
> The edit ran alongside generation. The editor assembled scenes as they arrived and ordered what was missing: "need a cutaway to the hands", "need a wider one". A re-shoot costs minutes, so the edit shaped production instead of waiting for it. Generations almost always feel slow in tempo: cut more aggressively than feels right, and plan to trim the first and last half-second of every clip, because the edges drift.
> 
> 
> 
> 
> Post-Production
> 
> After picture lock, a separate polish pass. Some shots needed it — text on a sign, a number plate, a small artifact that only shows on a big screen — and those are retouched frame by frame. A shot that is properly broken is regenerated instead, from the saved final prompt with one line changed, which only works because the prompt library is complete and versioned. First priority: close-ups of faces and hands. All of it before color.
> 
> Generation supervising is its own job, not a hope. Someone watches the assembled cut for shots that technically exist but do not work — a look that lands a beat late, a hand that reads wrong, a face that drifts on the third second — and sends them back with a named fix. Slop that survives to the screen costs reputation; slop found in the assembly costs one prompt.
> 
> Color starts with unification: every generation arrives with its own built-in grade, so the colorist first brings neighboring shots to one look. The look itself was baked into the location assets in pre-production, so the colorist refines rather than invents.
> 
> We did not re-record the voices. The lines were cleaned straight from the generations — noise removal, evening out the timbre between clips, placing the voice in the space — with a studio recording only where a clip came out with no usable voice. Sound design and music were built over continuous ambiences: one shared atmosphere glues generated shots into one space even where the picture drifts. Which is why "SFX only. No music." is mandatory in every prompt.
> 
> 
> 
> 
> Conclusion
> 
> Five rules hold the whole film.
> 
> Assets first. Not one shot until every character, location and prop is locked, named, versioned and stress-tested. This rule saves more money than everything else combined.
> Describe everything, every time. The model has no memory. The descriptor goes into every prompt word for word and is never shortened.
> Change one thing at a time. One line per iteration, everything into the log. Rewrite a prompt fully and you lose the parts that worked.
> Give the model less freedom. A corner instead of a room, a landmark instead of open space, a map instead of guesswork, one lens per shot, one action per beat. Laws with visible proof instead of requests.
> If it will not come together, simplify the shot, not the wording. Split it in two, remove an action, change the angle.
> 
> Every rule here exists because a shot failed without it. Take the attachments and start with one scene: one locked character, one location plate, one prompt skeleton. The pipeline does not need a big team — it needs the rules followed, and it scales down to a team of one.
> 
> 
> 
> 
> What's attached
> 
> The CINEDANCE skill bundle (writer, auditor, workbench and the pre-send self-check), the LIRA image skill, the acting system prompt with the master-profile format, the visual and color bible, the style prefixes for all five worlds, the optics reference with the ten FOV anchors, the voice system with the accents, the music-scene prompts with their lip-sync locks, and the prompt library with the full text and version history of every shot in the film.
> 
> 
> 
> 
> Comments197
> 
> wonkwink
> 9m
> this is AI? wth. looks completely real to me
> Reply
> nancy001
> 42m
> It must be said that with sufficient budget and professional personnel, we can use AI to control AI-generated visuals one hundred percent.
> Reply
> franklinwhale1280
> 1h
> I can't thank you enough for the lesson here. Was that Rampage Jackson?
> Reply
> adaptiveworm1777
> 1h
> increible
> Reply
> hospitalitycamel1500
> 2h
> great
> Reply
> hildeberto
> 2h
> Um dia chegarei nesse nível!
> Reply
> quantumplanet1457
> 2h
> wow good
> Reply
> craftsmanelephant1702
> 2h
> wow
> Reply
> institutionalquokka1832
> 3h
> :=
> Reply
> jxxk
> 3h
> cool 🙂
> Reply
> pointillistchair1568
> 4h
> insanoooooo
> Reply
> meditatingtoucan1357
> 5h
> Incredible
> Reply
> conceptualsun1613
> 6h
> nice
> Reply
> van_goghstar1822
> 6h
> Nice bro!
> Reply
> mehdisixt7
> 6h
> wow
> Reply
> madladcreative
> 8h
> Crazyy
> Reply
> paintingice1252
> 8h
> Hollywood and acting is going down the drain lol, finally
> Reply
> fourierjellyfish1255
> 8h
> Hollywood is cooked
> 1
> Reply
> playfuldonut1555
> 8h
> l
> Reply
> leibnizmoth1651
> 10h
> Good Job guys!
> Reply
> 
> Author
> 
> Higgsfield Studio
> Follow
> 
> Information
> 
> Views
> 70 101
> Generations
> 473 214
> Created time
> August 10, 13:01
> License
> HOL-RO
> 
> Powered by
> 
> Frames and Scenes
> 
> Cinema Studio
> 
> Recommended
> 
> ONEIRIC
> Higgsfield Studio
> Dusk
> Higgsfield Soul
> Never Bow
> deconstructivistferret1599
> SIWA — The Craving
> pascalowl1596
> Rainbow Desert - Surreal Lu
> alcanmedia
> ZEPHYR: Special
> Higgsfield Studio
> El pirata con poderes
> neoclassicaldragonfly1761
> REMNANT
> riuvision
> Nuevo proyecto
> jjbascunanc
> Flock
> codex9134
> 1467
> fermatpangolin1124
> FAST FILM DECO
> abrava_content
> Double Feature
> basquiatburrito1748
> The lawttorney
> fermatpangolin1124
> Oído absoluto
> suarbauhaus
> GHOST OF LAND
> amanaulakhcreator
> "Create a 15-20 second high-energy promotional shoe ad video using these two products: Opening (0-3
> digitalbanana1639
> AIFE Swapnil
> fermatpangolin1124
> mine
> etherealcamel1379
> ×
> This website uses cookies
> Our website uses cookies and similar technologies to improve our service, analyze usage, and personalize content and advertising. We only use non-essential cookies if you enable them. By choosing Accept, you agree to our Privacy Policy, Terms of Use, and Cookie Policy. Manage your preferences at any time.
> Accept all
> Reject all
>  Customize
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:41:40)*

<details>
<summary>💭 Thinking Process</summary>

I've found a complete feature-length AI film with extensive production data and a methodology built on Claude's core skills that aligns perfectly with the existing architecture. Now I'm saving the texts and downloading the videos for frame analysis before running a workflow.

I need to decompose the cinema ruler through actual video frame analysis, compare the Higgsfield method against the MCORCH creative team structure, and produce both the ruler documentation and next steps. I'm also resolving the three alerts in parallel while keeping the analysis tight and actionable—the Sovereign asked for link analysis, so that's the deliverable, but I'll focus on improvement recommendations rather than just documentation.

</details>


## 🤖 Claude *(03:41:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nagent-browser --session hf open \"https://higgsfield.ai/@higgsfield.studio/projects/oneiric\" >/dev/null 2>&1\nagent-browser --session hf wait --load networkidle >/dev/null 2>&1\ncat <<'EOF' | agent-browser --session hf eval --stdin > oneiric-raw.json\nJSON.stringify({text: document.body.innerText})\nEOF\nnode -e 'const j=JSON.parse(JSON.parse(require(\"fs\").readFileSync(\"oneiric-raw.json\",\"utf8\")));require(\"fs\").writeFileSync(\"oneiric-text.txt\",j.text);console.log(\"oneiric-text.txt:\",j.text.length,\"chars\")'\nwc -c oneiric-text.txt cully-text.txt\nagent-browser --session hf close >/dev/null 2>&1; echo \"browser fechado\"",
  "description": "Save ONEIRIC brief text to file",
  "timeout": 180000
}
```

## 🤖 Claude *(03:41:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nfor pair in \"oneiric:8e773bcc-7271-41a4-8024-3629f9ea9ca4\" \"cully:8379c8de-803d-4b40-ae7a-3029142566f6\"; do\n  name=${pair%%:*}; id=${pair##*:}\n  echo \"=== $name ($id) ===\"\n  curl -s -m 30 \"https://cdn.higgsfield.ai/hls/video_input/$id/index.m3u8\" | head -20\ndone",
  "description": "Inspect HLS manifests for both films",
  "timeout": 120000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> oneiric-text.txt: 27482 chars
> 27802 oneiric-text.txt
> 44631 cully-text.txt
> 72433 total
> browser fechado
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === oneiric (8e773bcc-7271-41a4-8024-3629f9ea9ca4) ===
> #EXTM3U
> #EXT-X-VERSION:6
> #EXT-X-STREAM-INF:BANDWIDTH=6763237,AVERAGE-BANDWIDTH=6270757,RESOLUTION=3438x1440,CODECS="avc1.640032,mp4a.40.2"
> index_1440p.m3u8
> 
> #EXT-X-STREAM-INF:BANDWIDTH=3832442,AVERAGE-BANDWIDTH=3608026,RESOLUTION=2578x1080,CODECS="avc1.640032,mp4a.40.2"
> index_1080p.m3u8
> 
> #EXT-X-STREAM-INF:BANDWIDTH=2186816,AVERAGE-BANDWIDTH=2073176,RESOLUTION=1718x720,CODECS="avc1.640020,mp4a.40.2"
> index_720p.m3u8
> 
> #EXT-X-STREAM-INF:BANDWIDTH=912426,AVERAGE-BANDWIDTH=864319,RESOLUTION=1146x480,CODECS="avc1.64001f,mp4a.40.2"
> index_480p.m3u8
> 
> === cully (8379c8de-803d-4b40-ae7a-3029142566f6) ===
> #EXTM3U
> #EXT-X-VERSION:6
> #EXT-X-STREAM-INF:BANDWIDTH=6816880,AVERAGE-BANDWIDTH=6084756,RESOLUTION=3438x1440,CODECS="avc1.640032,mp4a.40.2"
> index_1440p.m3u8
> 
> #EXT-X-STREAM-INF:BANDWIDTH=3875808,AVERAGE-BANDWIDTH=3377534,RESOLUTION=2578x1080,CODECS="avc1.640032,mp4a.40.2"
> index_1080p.m3u8
> 
> #EXT-X-STREAM-INF:BANDWIDTH=2210378,AVERAGE-BANDWIDTH=1892438,RESOLUTION=1718x720,CODECS="avc1.640020,mp4a.40.2"
> index_720p.m3u8
> 
> #EXT-X-STREAM-INF:BANDWIDTH=928720,AVERAGE-BANDWIDTH=772924,RESOLUTION=1146x480,CODECS="avc1.64001f,mp4a.40.2"
> index_480p.m3u8
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:42:20)*

<details>
<summary>💭 Thinking Process</summary>

Both files are 2.39:1 anamorphic, which matches the brief. I'll download the 1080p versions in the background while setting up the workflow — these are the trailers from the community page, with ONEIRIC likely being the full ~20 minute film and cully possibly a trailer or behind-the-scenes content. Let me check the duration first before finalizing the download settings.

</details>


## 🤖 Claude *(03:42:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nnohup bash -c '\nfor pair in \"oneiric:8e773bcc-7271-41a4-8024-3629f9ea9ca4\" \"cully:8379c8de-803d-4b40-ae7a-3029142566f6\"; do\n  name=${pair%%:*}; id=${pair##*:}\n  ffmpeg -y -loglevel error -i \"https://cdn.higgsfield.ai/hls/video_input/$id/index_1080p.m3u8\" -c copy -bsf:a aac_adtstoasc \"$name.mp4\" 2>&1\n  echo \"$name done: $(stat -c %s $name.mp4 2>/dev/null) bytes\"\ndone\n' > dl.log 2>&1 &\necho \"download iniciado em background (PID $!)\"; sleep 20; cat dl.log; ls -la *.mp4 2>/dev/null",
  "description": "Download both reference films via ffmpeg in background"
}
```

## 🤖 Claude *(03:42:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== TRUPE: campos que cada lente j\u00e1 escreve ===\"\nfor a in dramaturgo encenador diretor-fotografia diretor-arte; do printf \"%-22s %s linhas\\n\" \"$a\" \"$(wc -l < .claude/agents/$a.md)\"; done\necho \"=== MOTOR MONTAR v2: kinds e recursos ===\"\ngrep -cE \"^\" scripts/motion/montar-template-v2.mjs\ngrep -oE \"case '[a-z]+'|kind === '[a-z]+'\" scripts/motion/montar-template-v2.mjs | sort -u | head -20\necho \"=== existe alguma skill de 'stress test' / 'diagram' / 'acting task'? ===\"\nls .claude/skills/ | tr '\\n' ' '",
  "description": "Map current trupe and MONTAR engine surface"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> download iniciado em background (PID 799212)
> -rw-rw-r-- 1 ubuntu ubuntu 174325808 Aug 14 00:42 oneiric.mp4
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === TRUPE: campos que cada lente já escreve ===
> dramaturgo             569 linhas
> encenador              675 linhas
> diretor-fotografia     1117 linhas
> diretor-arte           1102 linhas
> === MOTOR MONTAR v2: kinds e recursos ===
> 568
> === existe alguma skill de 'stress test' / 'diagram' / 'acting task'? ===
> agent-browser asset-frame-grouping build-deploy-guardian canvas-studio-cinematic creative-studio-pipeline deepsearch-blueprint diretor-arte diretor-fotografia dramaturgo e2e-user-zero-audit encenador engineer-spaces free-render-dispatch gateway-recovery.md handoff-pruning-gate host-media-masters mcorch-qa-healing motion-montar motion-promo motion-scenes openclaw-dreaming openclaw-gateway-ops open-in-video-deeplink pmo-curator scratchpad-harvest ux-ui-senior-loop webgl-canvas-stabilization
> ```

## 🤖 Claude *(03:43:04)*

<details>
<summary>💭 Thinking Process</summary>

The downloads are progressing while I set up the workflow. I'm mapping out two parallel tracks: one to resolve alerts like committing the manifest, cleaning up disk space, and fixing the tenant API key issue, and another track for analysis that got cut off.

For the analysis track, I'll launch a workflow in the background that can handle multiple agents working in parallel — one doing frame-level forensics on the videos to measure shot lengths and color palettes, while others handle methodology decomposition and gap analysis. This lets me tackle the alert triage inline with my judgment while the workflow runs simultaneously.

Let me wait for the downloads to finish and verify them, then I'll kick off the workflow with the paths to the video files and reference documents it'll need.

</details>


## 🤖 Claude *(03:43:04)*

Baixando as referências. Vou disparar a análise profunda em workflow e resolver os alertas em paralelo.

## 🤖 Claude *(03:43:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf; cat dl.log; ls -la *.mp4 2>/dev/null; for f in oneiric cully; do [ -f $f.mp4 ] && ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_type,width,height,r_frame_rate -of default=nw=1 $f.mp4 2>/dev/null | tr '\\n' ' ' && echo \" <= $f\"; done",
  "description": "Check download progress and probe media",
  "timeout": 240000
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 1
> -rw-rw-r-- 1 ubuntu ubuntu 381157424 Aug 14 00:43 oneiric.mp4
>  <= oneiric
> ```

## 🤖 Claude *(03:43:22)*

<details>
<summary>💭 Thinking Process</summary>

The ffprobe issue is that the file's still being written to, so the moov atom hasn't been created yet. Rather than wait for the full download, I should launch the workflow now with the METHOD decomposition phase since that's text-based and ready, then handle the frame forensics once the videos finish downloading. I could instruct the agents to verify the mp4s exist before proceeding, though that's a bit risky.

Actually, the download is quick enough — 381MB in about a minute — so let me just wait it out and tackle the alerts in the meantime. I need to work through three things: committing the proof-manifest.json, handling the disk space by checking the harvest gate carefully, and dealing with the tenant 85aaca76 key issue. The harvest gate is the tricky one — I need to figure out what's in those four large scratchpads that isn't already preserved elsewhere. Looking at the dfd4c8a3 directory, I see model-fcf91d44.mp4 (the benchmark file) and ep06-master.mp4, and the Record shows ep06 was harvested to repurpose-inbox with what looks like the same file size, so that's likely preserved. But I need to verify whether model-fcf91d44.mp4 itself is actually saved in repurpose-inbox or just the directory structure.

</details>


## 🤖 Claude *(03:43:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== o benchmark fcf91d44 (3.069.023 B) est\u00e1 preservado fora do /tmp? ===\"\nfind repurpose-inbox -type f -size +2M -size -4M -newermt \"2026-08-01\" -printf \"%s %p\\n\" 2>/dev/null | grep -E \"^30[0-9]{5}\" || echo \"  nenhum arquivo de ~3MB\"\nls -la repurpose-inbox/ep06-fe479105/componentes-fcf91d44/ 2>/dev/null | head\necho \"=== invent\u00e1rio do harvest ep06 j\u00e1 preservado ===\"\ndu -sh repurpose-inbox/*/ep06-montar-harvest 2>/dev/null; find repurpose-inbox -name \"ep06-master*.mp4\" -printf \"%s %p\\n\" 2>/dev/null\necho \"=== o master EP07 dataviz (9.9MB, 08-11) est\u00e1 preservado? ===\"\nfind repurpose-inbox -iname \"*ep07*\" -type d 2>/dev/null; find repurpose-inbox -iname \"*dataviz*\" -o -iname \"*adsense*\" 2>/dev/null | head",
  "description": "Harvest gate: verify what is already preserved outside /tmp"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === o benchmark fcf91d44 (3.069.023 B) está preservado fora do /tmp? ===
> 3052604 repurpose-inbox/ada39fae-motion-spike/spike-montar.mp4
> total 1032
> drwxrwsr-x 3 ubuntu gcrUX    4096 Aug  7 13:22 .
> drwxrwsr-x 3 ubuntu gcrUX    4096 Aug  7 13:22 ..
> drwxrwsr-x 2 ubuntu gcrUX    4096 Aug  7 13:22 assets
> -rw-rw-r-- 1 ubuntu gcrUX   24991 Aug  7 13:22 build-scene.mjs.ref
> -rw-rw-r-- 1 ubuntu gcrUX 1013515 Aug  7 13:22 scene.html
> === inventário do harvest ep06 já preservado ===
> 780M	repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep06-montar-harvest
> 23572524 repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep06-montar-harvest/ep06-master-raw.mp4
> 23572524 repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep06-montar-harvest/ep06-master.mp4
> === o master EP07 dataviz (9.9MB, 08-11) está preservado? ===
> repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep07-kit
> repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep07-kit/specs/pilot-adsense.spec.json
> repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep07-kit/cenas/ep07-adsense-montar-pilot.mp4
> ```

## 🤖 Claude *(03:43:37)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking the file preservation status and noticing a discrepancy—the spike video was kept, but the actual benchmark model file with a different size wasn't preserved as expected.

Looking at what's missing from the harvest: the approved benchmark `model-fcf91d44.mp4`, a comparison model, the EP07 dataviz master, the pilot version, and a couple of act renders. I need to verify these by comparing file sizes, then harvest the unique ones before cleaning up, plus I should address the tenant key alert while I'm at it.

</details>


## 🤖 Claude *(03:43:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra\necho \"=== candidatos vs preservados (md5 dos 5 \u00fanicos suspeitos) ===\"\nmd5sum $T/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-fcf91d44.mp4 \\\n       $T/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-2ba98e10.mp4 \\\n       $T/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ep07-master-dataviz.mp4 \\\n       $T/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-pilot/ep07-adsense-pilot.mp4 \\\n       repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep07-kit/cenas/ep07-adsense-montar-pilot.mp4 \\\n       repurpose-inbox/ada39fae-motion-spike/spike-montar.mp4 2>&1\necho \"=== .ts/.mjs/.md/.json em scratchpads N\u00c3O presentes no repo (runners \u00f3rf\u00e3os) ===\"\nfor d in 2de725c0-2186-4fa8-9a12-16d4bd8f3128 dfd4c8a3-8149-4c5f-8d9c-f6076b019b22 c1b6a7b1-691a-443b-a950-94444ce8065d; do\n  find $T/$d/scratchpad -maxdepth 2 -type f \\( -name \"*.ts\" -o -name \"*.mjs\" -o -name \"*.md\" \\) -size +2k -printf \"%s\\t%p\\n\" 2>/dev/null\ndone | sort -rn | head -18",
  "description": "Compare candidates against preserved copies and list orphan runners"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === candidatos vs preservados (md5 dos 5 únicos suspeitos) ===
> 05e85b3fc35097cfe44d167bfab301c1  /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-fcf91d44.mp4
> a51fc16567f4cd314ef89a5fba4757db  /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-2ba98e10.mp4
> 68576c40b30e9883ba7b41e5053d5d04  /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ep07-master-dataviz.mp4
> ed9a08505684a1c9cc4c263d5c04d8bd  /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-pilot/ep07-adsense-pilot.mp4
> fc6e5b7783bb29fada470275eeec88cd  repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep07-kit/cenas/ep07-adsense-montar-pilot.mp4
> 02746dce25144cc38de3b51d9541b93b  repurpose-inbox/ada39fae-motion-spike/spike-montar.mp4
> === .ts/.mjs/.md/.json em scratchpads NÃO presentes no repo (runners órfãos) ===
> 42877	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/v3/seed-ep06-v3.ts
> 23379	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/proto-layers/build-scene.mjs
> 21156	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/proto-layers/build-scene.v2.bak.mjs
> 20310	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/ep06-v31-graph.ts
> 14349	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/motion-promo/SKILL.md
> 9254	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/probe3d/build-variants.mjs
> 6855	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/ep06-hidratar-eleven.ts
> 6688	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/gen-ep06-c4-c10.ts
> 6452	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/vidprobe/mkbench.mjs
> 5941	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/v3/validate-graph.ts
> 5724	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/ep06-hidratar-vozes.ts
> 5718	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit/render-1thread.mjs
> 5663	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/probe/probe.ts
> 5142	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/ep06-narrations.ts
> 4975	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/probe3d/bench2.mjs
> 4861	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/probe3d/arch-showdown.mjs
> 4789	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/ep06-eleven.ts
> 4711	/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/probe3d/bench-ffmpeg.mjs
> ```

## 🤖 Claude *(03:43:58)*

<details>
<summary>💭 Thinking Process</summary>

The benchmark video isn't matching across versions—I need to harvest it. The pilot episode also has a different render, which suggests it's a unique data visualization generation worth preserving separately.

Now I'm checking which of these orphaned files are genuinely unique versus already present in the repo. The build-scene reference file has a different byte count than the proto-layers version, and there's a skill definition that's already installed elsewhere. The EP06 seeder is archived, so I need to determine what's actually worth keeping versus what's redundant before I harvest and clean up.

</details>


## 🤖 Claude *(03:44:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra\necho \"=== build-scene.mjs: scratchpad vs repo vs .ref ===\"\nmd5sum scripts/motion/layered/build-scene.mjs $T/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/proto-layers/build-scene.mjs repurpose-inbox/ep06-fe479105/componentes-fcf91d44/build-scene.mjs.ref 2>&1\necho \"=== motion-promo SKILL.md: scratchpad vs repo ===\"\nmd5sum .claude/skills/motion-promo/SKILL.md $T/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/motion-promo/SKILL.md 2>&1\necho \"=== probe3d (benchmarks de arquitetura 3D) \u2014 existe equivalente no repo? ===\"\nls scripts/motion/ scripts/qa/ 2>/dev/null | grep -iE \"bench|probe|showdown\" || echo \"  nenhum bench de motion no repo\"\necho \"=== download ===\"; cd $T/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf && cat dl.log; ls -la *.mp4",
  "description": "Dedupe orphan runners against repo; check downloads"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === build-scene.mjs: scratchpad vs repo vs .ref ===
> 80090addddc32ee8263f8c612f285050  scripts/motion/layered/build-scene.mjs
> 27660b09e37b904d4f296e4867e300c0  /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/proto-layers/build-scene.mjs
> 80090addddc32ee8263f8c612f285050  repurpose-inbox/ep06-fe479105/componentes-fcf91d44/build-scene.mjs.ref
> === motion-promo SKILL.md: scratchpad vs repo ===
> ddaef0ef8a181c31816a9145b27ba009  .claude/skills/motion-promo/SKILL.md
> ddaef0ef8a181c31816a9145b27ba009  /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/motion-promo/SKILL.md
> === probe3d (benchmarks de arquitetura 3D) — existe equivalente no repo? ===
> apply-host-probe-nginx.sh
> bench-motion-cost.mjs
> firecrawl-ml-probe.ts
> probe-google-key.ts
> probe-vision-mcp-adversarial.ts
> probe-vision-mcp-fatia2-foundation.ts
> probe-vision-mcp-protocol-versions.ts
> === download ===
> oneiric done: 520032509 bytes
> -rw-rw-r-- 1 ubuntu ubuntu 282591280 Aug 14 00:44 cully.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 520032509 Aug 14 00:43 oneiric.mp4
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:44:14)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking which files to preserve based on whether they match the canonical versions in the repo. The build-scene script is identical and should be kept, while the older prototype version can be skipped since the repo has the authoritative copy. The motion promo documentation matches too, and I'm now looking at the benchmark files to see what's available.

The probe3d benchmarks that generated the memory reference data are already documented and the scripts exist in the repo, so those can be skipped as well. That leaves just 4 videos to harvest, totaling about 23 MB. The downloads are progressing—oneiric is complete at 520 MB and cully is nearly there at 282 MB.

My plan is to harvest those 4 videos into the repurpose inbox, prune the large scratchpads, commit the proof manifest, verify the tenant key, and then launch the cinema analysis workflow. I'll do the harvest first since it's quick, check on cully's download status, and then kick off the workflow once cully finishes.

</details>


## 🤖 Claude *(03:44:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra\nDEST=repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/motor-benchmarks\nmkdir -p $DEST\ncp -n $T/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-fcf91d44.mp4 $DEST/benchmark-fcf91d44-APROVADO.mp4\ncp -n $T/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/model-2ba98e10.mp4 $DEST/comparativo-2ba98e10.mp4\ncp -n $T/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ep07-master-dataviz.mp4 $DEST/ep07-master-dataviz-2026-08-11.mp4\ncp -n $T/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-pilot/ep07-adsense-pilot.mp4 $DEST/ep07-adsense-pilot-dataviz-2026-08-11.mp4\necho \"=== COLHIDO ===\"; ls -la $DEST\necho \"=== md5 confere com a origem? ===\"; md5sum $DEST/benchmark-fcf91d44-APROVADO.mp4",
  "description": "Harvest unique benchmark videos before pruning"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> cp: warning: behavior of -n is non-portable and may change in future; use --update=none instead
> cp: warning: behavior of -n is non-portable and may change in future; use --update=none instead
> cp: warning: behavior of -n is non-portable and may change in future; use --update=none instead
> cp: warning: behavior of -n is non-portable and may change in future; use --update=none instead
> === COLHIDO ===
> total 22520
> drwxrwsr-x 2 ubuntu gcrUX    4096 Aug 14 00:44 .
> drwxrwsr-x 6 gcrUX  gcrUX    4096 Aug 14 00:44 ..
> -rw-rw-r-- 1 ubuntu gcrUX 3069023 Aug 14 00:44 benchmark-fcf91d44-APROVADO.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 4619308 Aug 14 00:44 comparativo-2ba98e10.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 5419080 Aug 14 00:44 ep07-adsense-pilot-dataviz-2026-08-11.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 9933520 Aug 14 00:44 ep07-master-dataviz-2026-08-11.mp4
> === md5 confere com a origem? ===
> 05e85b3fc35097cfe44d167bfab301c1  repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/motor-benchmarks/benchmark-fcf91d44-APROVADO.mp4
> ```

## 🤖 Claude *(03:44:25)*

<details>
<summary>💭 Thinking Process</summary>

The checksum validates against the source, so the benchmark is intact. Now I'm going to pull down cully and run through the workflow.

</details>


## 🤖 Claude *(03:44:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf; cat dl.log; ls -la *.mp4; for f in oneiric cully; do echo \"--- $f ---\"; ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration,bit_rate -of default=nw=1 $f.mp4 2>&1 | tr '\\n' ' '; echo; done",
  "description": "Verify both downloads complete and probe",
  "timeout": 300000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> oneiric done: 520032509 bytes
> -rw-rw-r-- 1 ubuntu ubuntu 487587888 Aug 14 00:44 cully.mp4
> -rw-rw-r-- 1 ubuntu ubuntu 520032509 Aug 14 00:43 oneiric.mp4
> --- oneiric ---
> width=2578 height=1080 r_frame_rate=24/1 nb_frames=28535 duration=1188.992000 bit_rate=3498980 
> --- cully ---
> [mov,mp4,m4a,3gp,3g2,mj2 @ 0xaeb215eecb00] moov atom not found cully.mp4: Invalid data found when processing input
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:44:48)*

<details>
<summary>💭 Thinking Process</summary>

I've got the ONEIRIC video specs locked in—a 20-minute short at 2.39:1 aspect ratio. Cully's still downloading, so I'll launch the workflow now with ONEIRIC and the text materials ready, and the video will be available once the agents process it. I'm starting with a "Forense" phase that does frame-level forensics.

The full pipeline runs five phases: forensics on both videos in parallel, decomposing the written briefs into reusable methods, gap analysis across four agent lenses, adversarial verification of those gaps, and finally synthesizing the régua document. That's 12 agents total, well under the limit. I'll use parallelization where possible—the forensics and method phases run concurrently, then merge before the gap analysis, which feeds into verification, then synthesis. I need to provide concrete file paths to the agents and write up the NEXT-STEPS.md myself from their outputs.

The videos are large and memory-intensive, so I can't let agents load them whole or run expensive generation. Instead, I'll pre-generate downscaled 480p proxies and extract scene-change lists and contact sheets myself—that's deterministic and cheap, and gives the agents clean data to reason over rather than raw video. I can run that preprocessing in parallel with the text-based method and gap analysis workflow, which don't need video at all.

</details>


## 🤖 Claude *(03:44:48)*

ONEIRIC confirmado: **2578×1080 (2.39:1), 24 fps, 19min49s**. Vou disparar o workflow de análise e rodar a forense de frames em paralelo.

## 🤖 Claude *(03:46:44)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'regua-de-cinema-higgsfield',\n  description: 'Decomp\u00f5e os 2 breakdowns da Higgsfield Studio em m\u00e9todo reus\u00e1vel e cruza com o que o MCORCH j\u00e1 tem, para virar a r\u00e9gua de cinema do EP07',\n  phases: [\n    { title: 'M\u00e9todo', detail: 'extrai o m\u00e9todo de produ\u00e7\u00e3o dos 2 briefings (ONEIRIC + CULLY HILL BOYS)' },\n    { title: 'Lacuna', detail: '4 lentes cruzam o m\u00e9todo com o c\u00f3digo/agentes reais do MCORCH' },\n    { title: 'Cr\u00edtico', detail: 'verifica\u00e7\u00e3o adversarial de cada lacuna contra o reposit\u00f3rio' },\n    { title: 'Sintese', detail: 'a r\u00e9gua de cinema consolidada' },\n  ],\n}\n\nconst REPO = '/home/gcrUX/htdocs/constellation-orchestra'\nconst HF = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf'\n\nconst CONTEXTO = `\nCONTEXTO OBRIGAT\u00d3RIO \u2014 leia antes de qualquer coisa.\n\nO MCORCH \u00e9 uma plataforma brasileira de produ\u00e7\u00e3o de conte\u00fado com IA. O Sovereign (Gabriel) produz\num canal de videocast document\u00e1rio. O epis\u00f3dio EP07 (\"A economia secreta por tr\u00e1s dos videocasts\nbrasileiros\") est\u00e1 em produ\u00e7\u00e3o com um motor pr\u00f3prio chamado MONTAR \u2014 que MONTA camadas prontas\n(recortes PNG com alpha, screenshots, SVG) num espa\u00e7o 3D com c\u00e2mera \u00fanica e parallax geom\u00e9trico,\nrenderizado por Playwright + FFmpeg a custo ZERO (0 mco / US$ 0), em vez de gerar v\u00eddeo por modelo pago.\n\nEm 2026-08-13 o Sovereign viu o resultado visual e deu o veredito: **\"prova de conceito, ainda amador\"**.\nEle ent\u00e3o mandou dois links da Higgsfield Studio como A R\u00c9GUA \u2014 o padr\u00e3o de qualidade a atingir.\nOs dois breakdowns completos est\u00e3o salvos em:\n  - ${HF}/oneiric-text.txt      (ONEIRIC \u2014 curta de ~20 min, 41.118 assets)\n  - ${HF}/cully-text.txt        (CULLY HILL BOYS \u2014 longa de 1h54, 137 cenas, 473.214 gera\u00e7\u00f5es)\n\nO MCORCH J\u00c1 TEM uma \"trupe criativa\" de 4 agentes-lente que escrevem uma Partitura de Cena v1 com\nvocabul\u00e1rio FECHADO (nunca prosa):\n  ${REPO}/.claude/agents/dramaturgo.md           (intent \u00b7 stakes \u00b7 beats[] com anchorWord/action/onScreen/turn)\n  ${REPO}/.claude/agents/encenador.md            (staging: grid \u00b7 planes fg/mid/bg \u00b7 focal por beat \u00b7 entrances/exits)\n  ${REPO}/.claude/agents/diretor-fotografia.md   (camera[] \u00b7 light \u00b7 lens \u00b7 transitions \u00b7 grade \u2014 tempo em FRAMES, custo por frame MEDIDO)\n  ${REPO}/.claude/agents/diretor-arte.md         (art: type \u00b7 marks[] \u00b7 dataViz \u00b7 figures[] \u2014 proced\u00eancia datada em toda marca)\nE o motor: ${REPO}/scripts/motion/montar-template-v2.mjs (568 linhas)\nE o SSOT da linguagem: ${REPO}/docs/bok/spaces-evolution/43-amendment-motion-montar-camadas.md\n\nDOUTRINA INEGOCI\u00c1VEL DO PROJETO (violar isso invalida a recomenda\u00e7\u00e3o):\n  1. Custo externo em USD = 0 \u00e9 gate de aprova\u00e7\u00e3o. Ferramenta paga s\u00f3 entra com GO expl\u00edcito do Sovereign.\n     O motor MONTAR existe justamente para N\u00c3O pagar por v\u00eddeo gerado.\n  2. Lei 1 \u2014 Materialidade: nenhuma afirma\u00e7\u00e3o sem prova. Se voc\u00ea diz \"o motor n\u00e3o faz X\", PROVE com\n     grep/contagem no arquivo real, citando arquivo:linha. Nunca afirme por intui\u00e7\u00e3o.\n  3. Lei 2 \u2014 Processo Antecipado: automa\u00e7\u00e3o nova exige SOP humano documentado antes do c\u00f3digo.\n  4. Vocabul\u00e1rio FECHADO: a trupe escreve tokens versionados, n\u00e3o prosa. Token novo vira\n     \"Pedido de Vocabul\u00e1rio\" ao engenheiro, jamais improviso.\n  5. O beat cai na PALAVRA falada, n\u00e3o em fra\u00e7\u00e3o aritm\u00e9tica do cron\u00f4metro.\n\nREGRA DE HONESTIDADE: a Higgsfield produz com Seedance (modelo de v\u00eddeo PAGO, US$ caro \u2014 um coment\u00e1rio\nno pr\u00f3prio site diz \"only with big budget\"). O MCORCH N\u00c3O vai comprar Seedance. Portanto sua tarefa\nN\u00c3O \u00e9 dizer \"use Seedance\". \u00c9 separar, com precis\u00e3o cir\u00fargica, o que na r\u00e9gua \u00e9 M\u00c9TODO (transfer\u00edvel\na custo zero para o MONTAR e para a trupe) do que \u00e9 MOTOR (depende do modelo pago). Diga claramente\nqual \u00e9 qual. Um achado do tipo \"eles usam um modelo melhor\" \u00e9 IN\u00daTIL e ser\u00e1 descartado.\n`\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 FASE 1 \u2014 M\u00c9TODO\nconst METODO_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['fonte', 'principios', 'artefatos', 'numeros', 'transferivel_custo_zero', 'preso_ao_motor_pago'],\n  properties: {\n    fonte: { type: 'string' },\n    principios: {\n      type: 'array',\n      description: 'Os princ\u00edpios de produ\u00e7\u00e3o, cada um com a cita\u00e7\u00e3o literal que o sustenta',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['nome', 'regra', 'citacao', 'porque_existe'],\n        properties: {\n          nome: { type: 'string' },\n          regra: { type: 'string', description: 'a regra em uma frase imperativa' },\n          citacao: { type: 'string', description: 'trecho literal do briefing, em ingl\u00eas' },\n          porque_existe: { type: 'string', description: 'qual falha concreta este princ\u00edpio previne' },\n        },\n      },\n    },\n    artefatos: {\n      type: 'array',\n      description: 'Cada artefato/documento/skill que a produ\u00e7\u00e3o mant\u00e9m (character sheet, voice bible, spatial map, shotlist card, prompt library, log...)',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['nome', 'o_que_e', 'quem_escreve', 'formato'],\n        properties: {\n          nome: { type: 'string' },\n          o_que_e: { type: 'string' },\n          quem_escreve: { type: 'string' },\n          formato: { type: 'string', description: 'a estrutura literal do artefato, com os campos' },\n        },\n      },\n    },\n    numeros: {\n      type: 'array',\n      description: 'Todo n\u00famero verific\u00e1vel no briefing (contagem de assets, dura\u00e7\u00e3o, FOV, n\u00ba de locks, etc)',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['valor', 'do_que'],\n        properties: { valor: { type: 'string' }, do_que: { type: 'string' } },\n      },\n    },\n    transferivel_custo_zero: {\n      type: 'array',\n      description: 'O que d\u00e1 para levar para o MCORCH SEM pagar nada \u2014 m\u00e9todo puro',\n      items: { type: 'string' },\n    },\n    preso_ao_motor_pago: {\n      type: 'array',\n      description: 'O que s\u00f3 funciona porque existe um modelo de v\u00eddeo pago no meio',\n      items: { type: 'string' },\n    },\n  },\n}\n\nphase('M\u00e9todo')\nconst metodos = await parallel([\n  () => agent(`${CONTEXTO}\n\nTAREFA: leia INTEGRALMENTE ${HF}/oneiric-text.txt e extraia o m\u00e9todo de produ\u00e7\u00e3o.\nEste \u00e9 o breakdown do curta ONEIRIC. Preste aten\u00e7\u00e3o especial em: o Script Stress Test (motor de\n5 elementos), a conven\u00e7\u00e3o de nomes de asset, os character sheets em duas passadas, o \"anamorphic hack\"\n(a \u00f3tica assada na PLACA de loca\u00e7\u00e3o em vez do prompt de v\u00eddeo), o Voice Bible, os blocos do CINEDANCE,\na Diagram Skill (o diagrama esquem\u00e1tico colorido como sistema de dados espaciais), e o Acting Skill\n(tarefa de atua\u00e7\u00e3o em vez de r\u00f3tulo de emo\u00e7\u00e3o). Cite literalmente. N\u00e3o resuma o que d\u00e1 para citar.`,\n    { label: 'metodo:oneiric', phase: 'M\u00e9todo', schema: METODO_SCHEMA }),\n  () => agent(`${CONTEXTO}\n\nTAREFA: leia INTEGRALMENTE ${HF}/cully-text.txt e extraia o m\u00e9todo de produ\u00e7\u00e3o.\nEste \u00e9 o breakdown do longa CULLY HILL BOYS (1h54). Preste aten\u00e7\u00e3o especial em: a r\u00e9gua de \u00d3TICA em\nGRAUS (os 10 \u00e2ncoras de FOV) e por que graus e n\u00e3o mil\u00edmetros; o master shot de ~1 segundo e o\n\"spatial map\" colado em todo prompt da cena; as \"laws instead of requests\" (~150 locks nomeados,\n~80 frases terminando em \"= failed take\"); o card de shotlist com seus 4 grupos; a regra\n\"change one thing at a time\" e o log de vers\u00f5es; o pipeline de lip-sync musical (a faixa vem primeiro,\no \u00e1udio da gera\u00e7\u00e3o \u00e9 DESLIGADO); as corre\u00e7\u00f5es que salvaram gera\u00e7\u00f5es; e as 5 regras finais.\nCite literalmente. N\u00e3o resuma o que d\u00e1 para citar.`,\n    { label: 'metodo:cully', phase: 'M\u00e9todo', schema: METODO_SCHEMA }),\n])\n\nconst metodoValido = metodos.filter(Boolean)\nlog(`M\u00e9todo extra\u00eddo de ${metodoValido.length}/2 breakdowns \u2014 ${metodoValido.reduce((n, m) => n + m.principios.length, 0)} princ\u00edpios, ${metodoValido.reduce((n, m) => n + m.artefatos.length, 0)} artefatos`)\n\nconst metodoTexto = JSON.stringify(metodoValido, null, 1)\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 FASE 2 \u2014 LACUNA\nconst LACUNA_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['lente', 'lacunas'],\n  properties: {\n    lente: { type: 'string' },\n    lacunas: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['id', 'titulo', 'o_que_a_regua_faz', 'o_que_o_mcorch_faz_hoje', 'prova_material', 'acao', 'custo_usd', 'esforco', 'impacto_no_quadro'],\n        properties: {\n          id: { type: 'string', description: 'slug curto, ex: REGUA-OTICA-GRAUS' },\n          titulo: { type: 'string' },\n          o_que_a_regua_faz: { type: 'string' },\n          o_que_o_mcorch_faz_hoje: { type: 'string' },\n          prova_material: { type: 'string', description: 'OBRIGAT\u00d3RIO: arquivo:linha ou sa\u00edda de grep/contagem que PROVA o estado atual. Sem isso a lacuna \u00e9 descartada.' },\n          acao: { type: 'string', description: 'a mudan\u00e7a concreta a fazer \u2014 em qual arquivo' },\n          custo_usd: { type: 'string', description: 'USD 0 ou o custo real; se n\u00e3o for 0, justifique' },\n          esforco: { type: 'string', enum: ['baixo', 'medio', 'alto'] },\n          impacto_no_quadro: { type: 'string', enum: ['decisivo', 'alto', 'medio', 'baixo'], description: 'quanto isso muda o veredito \"ainda amador\"' },\n        },\n      },\n    },\n  },\n}\n\nphase('Lacuna')\nconst LENTES = [\n  {\n    key: 'trupe',\n    prompt: `Voc\u00ea \u00e9 a lente da TRUPE CRIATIVA. Leia os 4 agentes-lente do MCORCH por inteiro\n(.claude/agents/{dramaturgo,encenador,diretor-fotografia,diretor-arte}.md) e as skills hom\u00f4nimas em\n.claude/skills/. Compare o VOCABUL\u00c1RIO e os CAMPOS que eles escrevem hoje com os artefatos da r\u00e9gua.\nPergunte-se: que campo a r\u00e9gua tem que nossa Partitura de Cena v1 N\u00c3O tem? A r\u00e9gua substitui r\u00f3tulo de\nemo\u00e7\u00e3o por TAREFA de atua\u00e7\u00e3o \u2014 nosso Dramaturgo faz isso? A r\u00e9gua escreve o \"spatial map\" colado em\ntodo prompt \u2014 nosso Encenador faz? A r\u00e9gua trava \u00f3tica em GRAUS com 10 \u00e2ncoras \u2014 nosso DoP usa que\nunidade? A r\u00e9gua tem \"laws instead of requests\" com \"= failed take\" \u2014 temos algo equivalente?\nA r\u00e9gua tem um Script Stress Test ANTES de gastar gera\u00e7\u00e3o \u2014 temos gate equivalente?\nCada lacuna precisa de prova por grep no arquivo real.`,\n  },\n  {\n    key: 'motor',\n    prompt: `Voc\u00ea \u00e9 a lente do MOTOR. Leia scripts/motion/montar-template-v2.mjs por inteiro, mais\nscripts/motion/layered/build-scene.mjs e docs/bok/spaces-evolution/43-amendment-motion-montar-camadas.md.\nCONTE o que o motor executa hoje: quais \"kinds\" de camada, se h\u00e1 dof/blur por profundidade, quantas\nesta\u00e7\u00f5es de c\u00e2mera, se h\u00e1 corte duro entre planos, se h\u00e1 continuidade espacial entre cenas.\nDepois pergunte: dos princ\u00edpios da r\u00e9gua que N\u00c3O dependem do modelo pago (composi\u00e7\u00e3o, \u00f3tica, geografia\ndo espa\u00e7o, ritmo de corte, lei dos 180\u00b0, foreground occlusion, plano-mestre), quais o motor MONTAR\npoderia executar e n\u00e3o executa? Seja cir\u00fargico: \"foreground occlusion obrigat\u00f3ria ocupando 30-45% do\nquadro inferior\" \u00e9 geometria pura \u2014 o MONTAR faz isso? Prove contando no arquivo.`,\n  },\n  {\n    key: 'producao',\n    prompt: `Voc\u00ea \u00e9 a lente de PRODU\u00c7\u00c3O E ORGANIZA\u00c7\u00c3O. A r\u00e9gua descreve uma disciplina industrial:\nconven\u00e7\u00e3o de nome \u00fanica para todo elemento, asset = par (texto + imagem), estados como assets\nseparados nunca sobrescritos, canvas como fonte-da-verdade (\"se o asset n\u00e3o est\u00e1 l\u00e1, n\u00e3o est\u00e1 no\nplano\"), stress test de asset em 10 gera\u00e7\u00f5es, log de vers\u00f5es com veredito, \"change one thing at a\ntime\", biblioteca de prompts versionada, edi\u00e7\u00e3o em paralelo com a gera\u00e7\u00e3o, supervis\u00e3o de gera\u00e7\u00e3o como\nCARGO. Compare com o que o MCORCH tem: leia docs/bok/spaces-evolution/43-amendment-motion-montar-camadas.md,\no kit em repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/ep07-kit/ (liste o conte\u00fado),\nscripts/ep07/*.ts (o gauntlet-piece.ts \u00e9 nosso torneio de pe\u00e7a) e docs/roadmap/ep07-partituras/.\nOnde nossa organiza\u00e7\u00e3o \u00e9 frouxa comparada \u00e0 r\u00e9gua? Prove listando arquivos de verdade.`,\n  },\n  {\n    key: 'linguagem',\n    prompt: `Voc\u00ea \u00e9 a lente da LINGUAGEM VISUAL E DO G\u00caNERO. A r\u00e9gua \u00e9 live-action fotorreal 2.39:1\ncom atores digitalizados. O MCORCH faz motion graphics documental com camadas recortadas em 3D\n(est\u00e9tica de stop-motion com papel recortado, borda branca de contorno como assinatura do canal).\nS\u00e3o g\u00eaneros DIFERENTES. Sua tarefa \u00e9 a mais dif\u00edcil e a mais importante: separar o que na r\u00e9gua \u00e9\nespec\u00edfico de live-action fotorreal (e portanto IRRELEVANTE para n\u00f3s) do que \u00e9 GRAM\u00c1TICA DE CINEMA\nuniversal que vale igual em motion graphics \u2014 profundidade de campo motivada, oclus\u00e3o de primeiro\nplano, eixo de c\u00e2mera, tamanho de plano, ritmo de corte, luz com origem, escala relativa,\n\"content decides the lens\". Leia docs/processes/repertorio-producao-profissional.md e\nsrc/lib/cinematic-grammar.ts para ver o que j\u00e1 codificamos. Depois responda com n\u00fameros:\no que falta na nossa gram\u00e1tica que a r\u00e9gua tem?\nATEN\u00c7\u00c3O: n\u00e3o recomende fotorrealismo. O canal N\u00c3O vai virar live-action. A pergunta \u00e9 como o quadro\nMONTAR deixa de ser \"amador\" mantendo o g\u00eanero dele.`,\n  },\n]\n\nconst lacunas = await parallel(LENTES.map((l) => () =>\n  agent(`${CONTEXTO}\n\nM\u00c9TODO EXTRA\u00cdDO DA R\u00c9GUA (fase anterior, use como insumo):\n${metodoTexto}\n\nSUA LENTE:\n${l.prompt}\n\nTrabalhe a partir de ${REPO}. Use Read/Grep/Bash(read-only) \u00e0 vontade. N\u00c3O edite nada.\nToda lacuna precisa do campo prova_material preenchido com arquivo:linha ou sa\u00edda de comando real.\nPrefira 5 lacunas provadas a 20 palpites.`,\n    { label: `lacuna:${l.key}`, phase: 'Lacuna', schema: LACUNA_SCHEMA })\n))\n\nconst todasLacunas = lacunas.filter(Boolean).flatMap((r) => r.lacunas.map((g) => ({ ...g, lente: r.lente })))\nlog(`${todasLacunas.length} lacunas levantadas por ${lacunas.filter(Boolean).length} lentes`)\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 FASE 3 \u2014 CR\u00cdTICO ADVERSARIAL\nconst VEREDITO_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['id', 'refutada', 'motivo', 'correcao'],\n  properties: {\n    id: { type: 'string' },\n    refutada: { type: 'boolean', description: 'true se a lacuna \u00e9 falsa \u2014 o MCORCH J\u00c1 faz isso, ou a prova n\u00e3o sustenta' },\n    motivo: { type: 'string', description: 'com prova material pr\u00f3pria: arquivo:linha ou sa\u00edda de comando' },\n    correcao: { type: 'string', description: 'se a lacuna \u00e9 real mas mal enunciada, o enunciado correto; sen\u00e3o string vazia' },\n  },\n}\n\nphase('Cr\u00edtico')\n// Verifica\u00e7\u00e3o por 2 lentes distintas: uma tenta provar que J\u00c1 FAZEMOS, outra que a a\u00e7\u00e3o \u00e9 INVI\u00c1VEL/CARA.\nconst veredictos = await parallel(todasLacunas.map((g, i) => () =>\n  parallel([\n    () => agent(`${CONTEXTO}\n\nVoc\u00ea \u00e9 o CR\u00cdTICO DE REDUND\u00c2NCIA. Sua miss\u00e3o \u00e9 REFUTAR a lacuna abaixo provando que o MCORCH J\u00c1 FAZ\nisso em algum lugar do reposit\u00f3rio que a lente n\u00e3o olhou. Default: se voc\u00ea encontrar QUALQUER\nimplementa\u00e7\u00e3o equivalente, refute.\n\nLACUNA #${i + 1}\nid: ${g.id}\ntitulo: ${g.titulo}\na r\u00e9gua faz: ${g.o_que_a_regua_faz}\no mcorch faz hoje (alegado): ${g.o_que_o_mcorch_faz_hoje}\nprova apresentada: ${g.prova_material}\na\u00e7\u00e3o proposta: ${g.acao}\n\nVasculhe ${REPO} \u2014 agentes, skills, docs/processes, src/lib, scripts/motion, docs/bok. Grep agressivo\npor sin\u00f4nimos em portugu\u00eas E ingl\u00eas. Responda com prova material pr\u00f3pria.`,\n      { label: `refuta:${g.id}`, phase: 'Cr\u00edtico', schema: VEREDITO_SCHEMA }),\n    () => agent(`${CONTEXTO}\n\nVoc\u00ea \u00e9 o CR\u00cdTICO DE VIABILIDADE. Sua miss\u00e3o \u00e9 REFUTAR a lacuna abaixo provando que a a\u00e7\u00e3o proposta\n\u00e9 invi\u00e1vel, cara em USD, ou que viola a doutrina do projeto (custo zero, vocabul\u00e1rio fechado,\nLei 2 exigindo SOP antes do c\u00f3digo, o g\u00eanero do canal n\u00e3o ser live-action).\n\nLACUNA #${i + 1}\nid: ${g.id}\ntitulo: ${g.titulo}\na\u00e7\u00e3o proposta: ${g.acao}\ncusto alegado: ${g.custo_usd}\nesfor\u00e7o alegado: ${g.esforco}\nimpacto alegado no quadro: ${g.impacto_no_quadro}\n\nSe a a\u00e7\u00e3o \u00e9 vi\u00e1vel a custo zero e respeita a doutrina, responda refutada=false \u2014 n\u00e3o invente obje\u00e7\u00e3o.\nSe ela exige ferramenta paga, modelo de v\u00eddeo pago, ou mudan\u00e7a de g\u00eanero do canal, refute e diga por qu\u00ea.`,\n      { label: `viab:${g.id}`, phase: 'Cr\u00edtico', schema: VEREDITO_SCHEMA }),\n  ]).then((vs) => {\n    const ok = vs.filter(Boolean)\n    const refutacoes = ok.filter((v) => v.refutada)\n    return { ...g, sobrevive: refutacoes.length === 0, refutacoes: refutacoes.map((v) => v.motivo), correcoes: ok.map((v) => v.correcao).filter(Boolean) }\n  })\n))\n\nconst julgadas = veredictos.filter(Boolean)\nconst sobreviventes = julgadas.filter((g) => g.sobrevive)\nconst mortas = julgadas.filter((g) => !g.sobrevive)\nlog(`Cr\u00edtico: ${sobreviventes.length} lacunas sobreviveram \u00b7 ${mortas.length} refutadas`)\n\n// \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 FASE 4 \u2014 S\u00cdNTESE\nphase('Sintese')\nconst sintese = await agent(`${CONTEXTO}\n\nVoc\u00ea \u00e9 o SINTETIZADOR. Escreva o documento **A R\u00e9gua de Cinema** em PORTUGU\u00caS DO BRASIL, registro\nexecutivo e direto, sem enrola\u00e7\u00e3o. Grave em:\n  ${REPO}/docs/roadmap/regua-de-cinema-higgsfield-2026-08-14.md\n\nINSUMOS:\n\n1) M\u00c9TODO extra\u00eddo dos 2 breakdowns:\n${metodoTexto}\n\n2) LACUNAS QUE SOBREVIVERAM ao cr\u00edtico adversarial (${sobreviventes.length}) \u2014 estas s\u00e3o o miolo do doc:\n${JSON.stringify(sobreviventes, null, 1)}\n\n3) LACUNAS REFUTADAS (${mortas.length}) \u2014 N\u00c3O as inclua como a\u00e7\u00e3o. Inclua no fim, numa se\u00e7\u00e3o curta\n\"O que j\u00e1 fazemos (refutado pelo cr\u00edtico)\", porque saber que j\u00e1 temos \u00e9 t\u00e3o valioso quanto a lacuna:\n${JSON.stringify(mortas.map((m) => ({ id: m.id, titulo: m.titulo, porque_refutada: m.refutacoes })), null, 1)}\n\nESTRUTURA OBRIGAT\u00d3RIA DO DOCUMENTO:\n- Cabe\u00e7alho: o que \u00e9 este doc, de onde veio (os 2 links), a data, e o veredito do Sovereign que o motivou.\n- \u00a71 \"O que a r\u00e9gua realmente \u00e9\" \u2014 em 5 par\u00e1grafos no m\u00e1ximo. A tese central: o que separa o\n  profissional do amador nos dois filmes N\u00c3O \u00e9 o modelo de v\u00eddeo, \u00e9 a DISCIPLINA DE PR\u00c9-PRODU\u00c7\u00c3O.\n  Sustente com os n\u00fameros dos briefings (assets, gera\u00e7\u00f5es, locks, cenas).\n- \u00a72 \"M\u00e9todo \u00d7 Motor\" \u2014 uma tabela separando o que \u00e9 transfer\u00edvel a custo zero do que \u00e9 preso ao\n  modelo pago. Seja honesto: se algo \u00e9 preso ao motor pago, diga.\n- \u00a73 \"As leis que valem para o MONTAR\" \u2014 a tradu\u00e7\u00e3o das leis da r\u00e9gua para a nossa linguagem de\n  camadas em Z. Uma tabela: Lei da r\u00e9gua | Como ela se escreve na Partitura de Cena v1 | Quem \u00e9 o dono\n  (Dramaturgo/Encenador/DoP/Arte/engineer-spaces).\n- \u00a74 \"As lacunas provadas\" \u2014 uma se\u00e7\u00e3o por lacuna sobrevivente, ordenada por impacto_no_quadro\n  (decisivo primeiro). Cada uma com: o que a r\u00e9gua faz, o que fazemos hoje (COM a prova material\n  citada literalmente), a a\u00e7\u00e3o, o custo, o esfor\u00e7o.\n- \u00a75 \"O que N\u00c3O vamos copiar\" \u2014 e por qu\u00ea. Inclua explicitamente: n\u00e3o vamos comprar Seedance,\n  n\u00e3o vamos virar live-action fotorreal, n\u00e3o vamos digitalizar atores.\n- \u00a76 \"O que j\u00e1 fazemos\" \u2014 as refutadas.\n- \u00a77 \"Ordem de ataque\" \u2014 a sequ\u00eancia recomendada, com o crit\u00e9rio de parada de cada passo.\n\nREGRAS DE ESCRITA:\n- Toda afirma\u00e7\u00e3o sobre o estado atual do MCORCH carrega a prova material entre par\u00eanteses.\n- Nenhum n\u00famero inventado. Se um n\u00famero n\u00e3o estava nos insumos, n\u00e3o escreva.\n- Nada de \"revolucion\u00e1rio\", \"poderoso\", \"game-changer\". Engenharia, n\u00e3o poesia.\n- Use tabelas markdown onde couber. O doc deve caber em ~400 linhas.\n\nAo terminar, rode 'wc -l' no arquivo e devolva APENAS: o caminho, o n\u00famero de linhas, e um resumo de\n5 bullets do que o Sovereign precisa decidir.`,\n  { label: 'sintese:regua', phase: 'Sintese' })\n\nreturn {\n  metodos: metodoValido.length,\n  lacunas_levantadas: todasLacunas.length,\n  sobreviventes: sobreviventes.length,\n  refutadas: mortas.length,\n  topo: sobreviventes.filter((g) => g.impacto_no_quadro === 'decisivo').map((g) => `${g.id}: ${g.titulo}`),\n  sintese,\n}\n",
  "description": "Decompose Higgsfield references into cinema ruler"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: w8hhkc7q6
> Summary: Decompõe os 2 breakdowns da Higgsfield Studio em método reusável e cruza com o que o MCORCH já tem, para virar a régua de cinema do EP07
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/subagents/workflows/wf_7c66c36c-893
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/workflows/scripts/regua-de-cinema-higgsfield-wf_7c66c36c-893.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/workflows/scripts/regua-de-cinema-higgsfield-wf_7c66c36c-893.js"} to iterate without resending the script.)
> Run ID: wf_7c66c36c-893
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/workflows/scripts/regua-de-cinema-higgsfield-wf_7c66c36c-893.js", resumeFromRunId: "wf_7c66c36c-893"}) — completed agents return cached results (cached results may themselves be empty — inspect journal.jsonl before assuming there is something to recover).
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(03:46:53)*

<details>
<summary>💭 Thinking Process</summary>

I need to run frame forensics on both videos myself to extract the metrics the workflow can't pull from text—shot lengths via scene detection, color palettes, and plane counts. Since the host can only handle one workflow at a time and I'm working with agents, I'll be careful with CPU usage by limiting ffmpeg threads and starting on ONEIRIC first while cully finishes downloading. I'll kick off the scene detection in the background and tackle the pending alerts in parallel.

For alert 3, there's a QA tenant with an invalid Google API key—I can either clear it so it fails cleanly with a proper error message instead of leaking a 403, or leave it as is. Let me check the probe script to investigate further.

</details>


## 🤖 Claude *(03:46:53)*

Workflow rodando. Agora a forense de frames e os alertas.

## 🤖 Claude *(03:46:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\ncat dl.log; ls -la cully.mp4\nnohup bash -c '\nfor f in oneiric cully; do\n  [ -f $f.mp4 ] || continue\n  # cortes: scene detection com limiar 0.30, timestamps em segundos\n  ffmpeg -threads 2 -hide_banner -loglevel error -i $f.mp4 -vf \"select=gt(scene\\,0.30),showinfo\" -f null - 2>&1 \\\n    | grep -oE \"pts_time:[0-9.]+\" | cut -d: -f2 > $f-cuts.txt\n  echo \"$f cortes: $(wc -l < $f-cuts.txt)\"\ndone\n' > forense.log 2>&1 &\necho \"forense iniciada (PID $!)\"",
  "description": "Run scene-cut detection on both films in background"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> oneiric done: 520032509 bytes
> -rw-rw-r-- 1 ubuntu ubuntu 1787297840 Aug 14 00:46 cully.mp4
> forense iniciada (PID 803353)
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:46:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== o probe de chave existe e o que ele faz ===\"; sed -n '1,40p' scripts/qa/probe-google-key.ts\necho \"=== 85aaca76 aparece onde? ===\"; grep -rn \"85aaca76\" --include=\"*.md\" --include=\"*.ts\" . 2>/dev/null | grep -v node_modules | head -5",
  "description": "Inspect google key probe and the QA tenant reference"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === o probe de chave existe e o que ele faz ===
> /**
>  * Sonda de saúde das chaves Google/Gemini — onde cada uma vive e se está VIVA.
>  *
>  * Nasceu do incidente de 2026-08-12: três chaves Google diferentes espalhadas pelo host, TODAS
>  * devolvendo 403 "reported as leaked", e ninguém sabia quantas eram nem onde moravam. A fonte
>  * provável do vazamento eram notas de memória de agente com a chave em TEXTO PLANO.
>  *
>  * A sonda NUNCA imprime a chave — só os 6 últimos caracteres, que bastam para casar com o
>  * console do AI Studio.
>  *
>  * Uso: bun run scripts/qa/probe-google-key.ts
>  * Exit: 0 = existe ao menos um cofre com chave viva · 1 = nenhuma chave viva · 2 = erro de setup
>  */
> import { readFileSync, existsSync } from "node:fs";
> import { execFileSync } from "node:child_process";
> 
> const USER_ZERO = "ada39fae-67e1-4e53-af1c-5a18e1c108e8";
> const SB_URL = process.env.VITE_SUPABASE_URL;
> const SB_KEY = process.env.SB_SECRET_KEY;
> 
> type Probe = { origem: string; sufixo: string; status: string; vivo: boolean; nota?: string };
> const probes: Probe[] = [];
> const seen = new Map<string, string[]>(); // chave → origens (para achar duplicatas)
> 
> /** O marcador deixado pela redação de 2026-08-12 casa com o padrão AIza… mas NÃO é credencial.
>  *  Contá-lo como achado faz o probe gritar para sempre depois de uma limpeza bem-sucedida —
>  *  e alarme que nunca apaga é alarme que se aprende a ignorar. */
> const REDACTED = /REDACTED|revoked/i;
> 
> async function check(key: string, origem: string, nota?: string) {
>   if (REDACTED.test(key)) return; // já limpo: silêncio é o resultado correto
>   const sufixo = key.slice(-6);
>   const antes = seen.get(key);
>   if (antes) {
>     antes.push(origem);
>     probes.push({ origem, sufixo, status: "= mesma chave acima", vivo: false, nota: "duplicata" });
>     return;
>   }
>   seen.set(key, [origem]);
>   let status = "erro";
> === 85aaca76 aparece onde? ===
> HANDOFF.md:399:**Pendências que a próxima sessão herda:** (1) o **link de cinema** do Sovereign é a régua — decompor ANTES de escrever código (planos, duração, luz, o que se move); (2) re-renderizar a pilha com o leque + as folhas com gráfico; (3) escolher 1 variação por peça; (4) gancho/fecho com Veo dizendo só a frase que precisa de rosto (GO dado); (5) `85aaca76` tem `google_api_key` inválida (tenant de QA).
> ```

## 🤖 Claude *(03:47:16)*

<details>
<summary>💭 Thinking Process</summary>

I'm realizing the cully.mp4 download is massive—nearly 2 GB and still growing—which is counterproductive since I'm trying to free up disk space on a drive that's already at 77% capacity. I should cancel this download and just grab a shorter clip for the régua analysis instead of committing 3 GB to a full 1h54 feature film.

Actually, the forensics script is already running and might be processing the incomplete file, which won't work since ffmpeg needs a valid moov atom. Let me check the state and decide: I have 45 GB free, so letting cully finish is wasteful but feasible, but a smarter approach is to keep just the analysis artifacts (cut lists, contact sheets) and delete the raw video files afterward. I'll proceed with handling the tenant key issue for 85aaca76—it's a QA tenant with an invalid Google API key that should be cleared so it fails cleanly with a 402 instead of confusing 400/403 errors.

</details>


## 🤖 Claude *(03:47:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "timeout 120 bun run scripts/qa/probe-google-key.ts 2>&1 | tail -30; echo \"PROBE_EXIT=$?\"",
  "description": "Probe Google key vaults health",
  "timeout": 150000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> A new version of Supabase CLI is available: v2.114.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> 
> 🔑 CHAVES GOOGLE — onde vivem e se funcionam
> 
>   ✅ COFRE user_api_keys [ada39fae]                                …_EwXDo     HTTP 200
>   ❌ COFRE user_api_keys [85aaca76]                                …called     HTTP 400
>   🔒 COFRE edge functions: GEMINI_API_KEY + MESH_EMBED_GEMINI_KEY  …sha a85b822f valor oculto — só digest  (mesma chave nos dois nomes)
> 
> ✅ 1 cofre(s) com chave VIVA
> 
> PROBE_EXIT=0
> ```

## 🤖 Claude *(03:47:29)*

<details>
<summary>💭 Thinking Process</summary>

So tenant `85aaca76` has an invalid Google API key that's returning a 400 error, and the stored value itself looks suspicious — it ends with "called" which suggests it might be a placeholder or error message fragment rather than an actual key. I need to check the length and prefix pattern to understand what's actually stored there, but I should be careful not to expose the full key value.

The proper solution is to NULL out that column for this tenant so it fails gracefully with a 402 error and the structured `<service>_not_configured` response instead of trying to use a garbage key that breaks mid-render. First I should verify whether tenant `85aaca76` is a QA throwaway account based on the reference to QA smoke users, then write a safe script to handle the fix.

</details>


## 🤖 Claude *(03:47:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/decrypted_user_api_keys?select=user_id,google_api_key&user_id=eq.85aaca76-0000-0000-0000-000000000000\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" 2>/dev/null | head -c 200\necho \"\"\necho \"=== quem \u00e9 85aaca76 (uuid completo + perfil) ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/profiles?select=id,email,created_at&id=like.85aaca76*\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" 2>/dev/null | head -c 400",
  "description": "Identify the QA tenant with the bad key"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> []
> === quem é 85aaca76 (uuid completo + perfil) ===
> {"code":"42703","details":null,"hint":null,"message":"column profiles.email does not exist"}
> ```

## 🤖 Claude *(03:47:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\necho \"=== perfil 85aaca76 ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/profiles?select=*&id=like.85aaca76*\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" 2>/dev/null | head -c 600\necho \"\"\necho \"=== a linha em decrypted_user_api_keys (s\u00f3 o formato da chave, nunca o valor) ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/decrypted_user_api_keys?select=user_id,google_api_key&google_api_key=not.is.null\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" 2>/dev/null \\\n | node -e 'let s=\"\";process.stdin.on(\"data\",d=>s+=d).on(\"end\",()=>{try{const r=JSON.parse(s);console.log(r.map(x=>({user:x.user_id?.slice(0,8),len:x.google_api_key?.length,prefixo:x.google_api_key?.slice(0,4),sufixo:x.google_api_key?.slice(-6),pareceChave:/^AIza[\\w-]{35}$/.test(x.google_api_key||\"\")})))}catch(e){console.log(\"raw:\",s.slice(0,300))}})'",
  "description": "Inspect the malformed key shape without printing it"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === perfil 85aaca76 ===
> {"code":"42883","details":null,"hint":"No operator matches the given name and argument types. You might need to add explicit type casts.","message":"operator does not exist: uuid ~~ unknown"}
> === a linha em decrypted_user_api_keys (só o formato da chave, nunca o valor) ===
> [
>   {
>     user: 'ada39fae',
>     len: 39,
>     prefixo: 'AIza',
>     sufixo: '_EwXDo',
>     pareceChave: true
>   },
>   {
>     user: '85aaca76',
>     len: 22,
>     prefixo: 'AIza',
>     sufixo: 'called',
>     pareceChave: false
>   },
>   {
>     user: '43027d04',
>     len: 0,
>     prefixo: '',
>     sufixo: '',
>     pareceChave: false
>   }
> ]
> ```

## 🤖 Claude *(03:47:52)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking the validity of these API keys. The first one is legitimate at 39 characters, but the second is truncated at just 22 characters and will fail validation, and the third is an empty string which is also invalid.

The core issue is that both the truncated and empty values bypass the fail-closed contract — they should be NULL to trigger the proper `_not_configured` response, but instead they're being treated as configured values that will fail at runtime. I need to verify how the resolution code handles empty strings and whether it's correctly guarding against this, then check the write path in the setup script since the view doesn't support upsert operations.

</details>


## 🤖 Claude *(03:47:52)*

Achado material novo: **não é um tenant, são dois** — e um deles tem string vazia, que passa por "configurada".

## 🤖 Claude *(03:47:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== como o c\u00f3digo resolve google_api_key (guard de vazio?) ===\"\ngrep -rn \"google_api_key\" --include=\"*.ts\" supabase/functions/ scripts/lib/ src/ 2>/dev/null | grep -vE \"types.ts|\\.test\\.\" | head -20\necho \"\"\necho \"=== set-google-key.sh: caminho de escrita correto ===\"\nsed -n '1,60p' scripts/qa/set-google-key.sh",
  "description": "Find key-resolution guards and the correct write path"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === como o código resolve google_api_key (guard de vazio?) ===
> supabase/functions/openrouter-swarm/index.ts:178:    .select("openrouter_api_key, google_api_key, openai_api_key, groq_api_key")
> supabase/functions/openrouter-swarm/index.ts:211:    apiKey = userKeys?.google_api_key;
> supabase/functions/check-video-status/index.ts:207:      const googleKey = userKeys?.google_api_key || Deno.env.get("GOOGLE_API_KEY");
> supabase/functions/tts-speak/index.ts:65:  // User key override: user's google_api_key > vault GEMINI_API_KEY
> supabase/functions/tts-speak/index.ts:72:    .select("google_api_key")
> supabase/functions/tts-speak/index.ts:76:  const geminiKey = userKeys?.google_api_key;
> supabase/functions/orchestrate-step/index.ts:275:    const geminiKey = userKeys?.google_api_key;
> supabase/functions/lead-score/index.ts:95:    const geminiKey = userKeys?.google_api_key;
> supabase/functions/aios-chat/index.ts:62:    .select("google_api_key, openrouter_api_key, pref_ai_model")
> supabase/functions/aios-chat/index.ts:163:  const geminiKey = (forceVault ? null : userKeys?.google_api_key);
> supabase/functions/aios-chat/index.ts:214:      forceVault ? false : !!userKeys?.google_api_key,
> supabase/functions/rescue-video/index.ts:72:    const { data: keys } = await adminClient.from("decrypted_user_api_keys").select("google_api_key").eq("user_id", userId).single();
> supabase/functions/rescue-video/index.ts:73:    const googleKey = keys?.google_api_key || Deno.env.get("GOOGLE_API_KEY");
> supabase/functions/intent-orchestrate/index.ts:42:    const geminiKey = keys?.google_api_key;
> supabase/functions/analyze-node/index.ts:48:    const geminiKey = userKeys?.google_api_key;
> supabase/functions/aios-chat-stream/index.ts:62:    .select("google_api_key, openrouter_api_key, pref_ai_model")
> supabase/functions/aios-chat-stream/index.ts:106:    apiKey = (forceVault ? null : userKeys?.google_api_key) || "";
> supabase/functions/aios-chat-stream/index.ts:204:            isOpenRouter ? !!userKeys?.openrouter_api_key : (forceVault ? false : !!userKeys?.google_api_key)
> supabase/functions/video-render/index.ts:224:    // The canonical Vault column is `google_api_key` (NOT `gemini_api_key` — the BoK 06 §2.5 / CLAUDE.md naming is
> supabase/functions/video-render/index.ts:225:    // stale; canvas-execute + the live decrypted view use google_api_key, verified 2026-06-22 via 42703 on gemini_api_key).
> 
> === set-google-key.sh: caminho de escrita correto ===
> #!/usr/bin/env bash
> # Grava a chave Google/Gemini nos cofres da casa, SEM que ela passe por chat, log ou histórico.
> #
> # Diretiva Sovereign 2026-08-12: "no env não pode ter mais nada, a ideia é guardar tudo no vault".
> # Este script cumpre isso: a chave vai para os DOIS cofres que a plataforma lê de verdade, e o
> # .env fica sem credencial de provedor.
> #
> #   COFRE 1 · user_api_keys.google_api_key  → o rail per-user (BYOK). É de onde a plataforma e os
> #             runners de CLI leem. Cifrado no banco. É o canônico.
> #   COFRE 2 · vault das Edge Functions      → GEMINI_API_KEY + MESH_EMBED_GEMINI_KEY, para os
> #             fluxos de SISTEMA que rodam sem auth.uid() (embeddings da malha, cron).
> #
> # O .env NÃO fica vazio, e isso é de propósito: para abrir um cofre é preciso uma chave, e essa
> # primeira chave não pode morar dentro do cofre que ela abre (paradoxo de bootstrap — mesma razão
> # documentada em docs/processes/bridge-key-freshness.md). O .env guarda só SB_SECRET_KEY + URL.
> #
> # Uso:  bash scripts/qa/set-google-key.sh
> #       (cola a chave quando pedir — a digitação fica OCULTA e não entra no histórico do shell)
> #
> # Opcional: bash scripts/qa/set-google-key.sh --skip-edge   (só o cofre per-user)
> 
> set -euo pipefail
> cd "$(dirname "$0")/../.."
> 
> SKIP_EDGE=0
> [[ "${1:-}" == "--skip-edge" ]] && SKIP_EDGE=1
> 
> USER_ZERO="ada39fae-67e1-4e53-af1c-5a18e1c108e8"
> 
> set -a; source .env 2>/dev/null || true; set +a
> : "${VITE_SUPABASE_URL:?falta VITE_SUPABASE_URL no .env}"
> : "${SB_SECRET_KEY:?falta SB_SECRET_KEY no .env}"
> 
> echo "🔑 Cole a chave do Google AI Studio (a digitação fica oculta) e tecle ENTER:"
> read -rs GKEY
> echo
> 
> [[ -z "${GKEY}" ]] && { echo "❌ nada colado — abortado"; exit 2; }
> [[ "${GKEY}" != AIza* ]] && { echo "❌ não parece uma chave do Google (esperado começar com AIza)"; exit 2; }
> 
> TAIL="…${GKEY: -6}"
> echo "→ chave recebida: ${TAIL}"
> 
> # ── GATE 0: a chave FUNCIONA? Nunca gravar credencial morta num cofre. ────────────────────────
> CODE=$(curl -s -o /dev/null -w '%{http_code}' "https://generativelanguage.googleapis.com/v1beta/models?key=${GKEY}")
> if [[ "${CODE}" != "200" ]]; then
>   echo "❌ GATE 0 falhou: a chave devolve HTTP ${CODE} (403 = vazada/bloqueada · 400 = inválida)."
>   echo "   Nada foi gravado."
>   exit 1
> fi
> echo "✅ GATE 0: chave viva (HTTP 200)"
> 
> # ── GATE 1: ela gera IMAGEM? (o escopo que a diretiva exige, não só listar modelos) ───────────
> IMG_CODE=$(curl -s -o /tmp/.gk-img.json -w '%{http_code}' \
>   "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent?key=${GKEY}" \
>   -H 'Content-Type: application/json' \
>   -d '{"contents":[{"parts":[{"text":"a single plain grey sphere on a flat white background"}]}],"generationConfig":{"responseModalities":["IMAGE"]}}')
> if [[ "${IMG_CODE}" == "200" ]] && grep -q '"inlineData"' /tmp/.gk-img.json 2>/dev/null; then
>   echo "✅ GATE 1: gera imagem em gemini-3.1-flash-image (Nano Banana 2)"
> else
> ```

## 🤖 Claude *(03:48:19)*

<details>
<summary>💭 Thinking Process</summary>

I'm seeing the pattern now—across these different implementations, there's an inconsistency in how the API key fallback logic handles empty strings. Some code paths check for truthiness downstream, while others use the `||` operator which treats empty strings as falsy, creating a gap where an empty string could slip through instead of falling back to the environment variable.

The real issue is with the truncated key for `85aaca76`—it's 22 characters and passes the truthiness check, so all 15 edge functions will attempt to use it as a valid BYOK key and hit HTTP 400 errors. The user gets an opaque failure instead of a clear "configure your credentials" message. The root problem is that truthiness doesn't guarantee validity; I need a shape guard to validate the key format itself.

The fix has two parts: clean the corrupt data by nulling out the truncated key for `85aaca76` and normalizing the empty string for `43027d04` to null, then add a shape guard to prevent this from happening again. But applying that guard across 15 edge functions is too broad for a simple alert resolution, and this is a documented feature bug rather than a new automation requiring a formal SOP.

The pragmatic approach is to clean both rows, add validation to the probe itself so it catches malformed keys, and place the guard at the write path in `set-google-key.sh` where it already validates before storing—that's the single chokepoint that prevents garbage from being written in the first place. The remaining edge function updates can be documented as a follow-up. I need to verify whether NULLing the field through the masked view actually clears the encrypted data, since my notes suggest it doesn't — the RPC disconnect pattern is required instead. Let me check the credential-disconnect-clear SOP to understand the proper cleanup mechanism, then review the forensics progress.

</details>


## 🤖 Claude *(03:48:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== SOP: como LIMPAR credencial numa view mascarada (null n\u00e3o limpa) ===\"\ngrep -nE \"null|NULL|limpa|clear|sentinel|__CLEAR|disconnect\" docs/processes/credential-disconnect-clear.md | head -25",
  "description": "Read the credential clearing SOP"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === SOP: como LIMPAR credencial numa view mascarada (null não limpa) ===
> 8:After credential-encryption, a credential column on the masked view cannot be cleared by a
> 9:client writing `NULL`. The view's INSTEAD OF trigger writes secret columns through
> 10:`COALESCE(NULLIF(NEW.x, '••••••••••••'), base.x)` — a **load-bearing guard** that lets a partial
> 11:save touch only some fields without wiping the others. Its side effect: **`NULL` preserves the old
> 12:value**, so a disconnect that nulls columns from the client silently leaves the secret (and its
> 14:so the client has no privileged path to a true clear.
> 16:A true clear/revoke therefore MUST run server-side with elevated privileges.
> 22:`disconnect_wordpress()` RPC (SECURITY DEFINER, owner `postgres`), scoped to `auth.uid()`.
> 24:Manual equivalent (Sovereign / support, e.g. an LGPD erasure request): run the same clear via the
> 27:## Sequence (per disconnect)
> 29:1. Client calls `supabase.rpc('disconnect_wordpress')` — no parameters (identity comes from the JWT).
> 30:   - **Success criterion:** RPC returns `{ error: null }`.
> 32:3. RPC nulls `wp_site_url`, `wp_username`, `wp_app_password` on the base table (privileged — bypasses the masked view's COALESCE-NULLIF guard).
> 41:-- PASS: all three NULL
> 46:same user are UNCHANGED (the clear must be surgical — never wipe sibling credentials).
> 55:    SET wp_site_url = NULL, wp_username = NULL, wp_app_password = NULL, updated_at = now()
> 60:  deterministic name survived a prior clear. Delete it (query above), then reconnect.
> 64:Decrypted view shows all three WP columns NULL, zero matching `vault.secrets` rows, sibling AI keys
> 83:disconnecting first". (connect → disconnect → reconnect always worked because `disconnect_wordpress()`
> 121:COALESCE defaults, masked sentinels). **Material proof (2026-06-02, rolled back):** BEFORE — attacker
> 128:## Meta / social disconnect — orphaned-secret revocation (closed 2026-06-02)
> 130:**Was:** disconnecting a Meta connection (`useMetaConfig.disconnect`) or a social account
> 131:(`useSocialAccounts.disconnectAccount`) issued a plain `.delete()` through the masked view → the
> 134:**orphaned** (retained plaintext, no owning row) — the same LGPD/retention gap `disconnect_wordpress()`
> 138:`meta_config_pages_*`) — residue of ~6 connect/disconnect cycles.
> ```

## 🤖 Claude *(03:48:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf; cat forense.log 2>/dev/null; ls -la *cuts.txt 2>/dev/null; cat dl.log; ls -la cully.mp4",
  "description": "Check forensics and cully download progress"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu 0 Aug 14 00:46 oneiric-cuts.txt
> oneiric done: 520032509 bytes
> -rw-rw-r-- 1 ubuntu ubuntu 2443444272 Aug 14 00:48 cully.mp4
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:48:32)*

<details>
<summary>💭 Thinking Process</summary>

The INSTEAD OF trigger uses COALESCE to preserve the old value when NULL comes from the client, so clearing that corrupt key requires direct SQL access with elevated privileges rather than going through PostgREST. I should check if the `aios-sql-bridge` tool is available in the project to run the necessary server-side query. Meanwhile, the Cully download is at 2.44GB and still growing—it'll end up around 2.9GB for the full feature.

The scene detection is still processing (20 minutes of footage with 2 threads takes time), and oneiric-cuts.txt is empty until that finishes. I need to find the SQL path for clearing the base table, commit the proof manifest, and clean up the scratchpads now that the harvest is done.

</details>


## 🤖 Claude *(03:48:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== caminho de SQL privilegiado dispon\u00edvel ===\"\nls scripts/ | grep -iE \"sql|bridge|psql\" | head; ls .claude/scripts/ 2>/dev/null | grep -iE \"sql|db\" | head\necho \"--- supabase link + db status ---\"\ngrep -rn \"aios-sql-bridge\\|exec_sql\\|db push\" docs/processes/*.md 2>/dev/null | head -4\necho \"=== tabela base por tr\u00e1s da view ===\"\ngrep -rn \"user_api_keys\" supabase/migrations/*.sql 2>/dev/null | grep -iE \"create table|_base|INSTEAD OF\" | head -6",
  "description": "Locate privileged SQL path and the base table"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === caminho de SQL privilegiado disponível ===
> bridge-mesh-to-openclaw.ts
> crm-media-bridge.ts
> design-bridge.ts
> motion-bridge.ts
> nightly-bridge-refresh.sh
> opencode-bridge.ts
> provenance-bridge.ts
> subtitle-bridge.ts
> video-bridge.ts
> video-repurpose-bridge.ts
> db
> --- supabase link + db status ---
> docs/processes/build-deploy-materiality.md:35:| **DB (migrations)** | `npx supabase db push` (+ `/security-review` antes do commit) | output do push + query material confirmando o schema |
> docs/processes/great-reset-sovereign.md:77:npx supabase db push
> docs/processes/crm-media-ingest.md:138:- [ ] Aplicar a migration (`supabase db push` / bridge) — só depois do review.
> docs/processes/collective-efficiency-ledger.md:56:5. **Aplicar a migration** (`supabase db push` ou bridge). **Gate G5:** `db push` retorna sucesso material (output literal).
> === tabela base por trás da view ===
> supabase/migrations/20260421000000_create_user_api_keys.sql:1:CREATE TABLE IF NOT EXISTS public.user_api_keys (
> supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql:1:-- Migration: fix user_api_keys INSTEAD OF trigger — eliminate encrypt double-fire (23505)
> supabase/migrations/20260601000000_credential_encryption.sql:495:-- 5.3 Instead of trigger for user_api_keys
> supabase/migrations/20260601000000_credential_encryption.sql:534:  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.user_api_keys
> supabase/migrations/20260601000600_secure_definer_views.sql:82:  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.user_api_keys
> supabase/migrations/20260725120100_revoke_anon_credential_view_writes.sql:7:-- INSTEAD OF trigger tenant guard (20260602130000 for user_api_keys; 20260602150000 for
> ```

## 🤖 Claude *(03:48:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== a view mascarada sobre qual tabela base? ===\"\nsed -n '480,540p' supabase/migrations/20260601000000_credential_encryption.sql\necho \"=== h\u00e1 RPC de disconnect para user_api_keys / provider? ===\"\ngrep -rln \"disconnect_provider\\|clear_user_api_key\\|disconnect_api_key\" supabase/migrations/ 2>/dev/null | head",
  "description": "Understand the encrypted view structure for user_api_keys"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === a view mascarada sobre qual tabela base? ===
>       is_active = NEW.is_active,
>       metadata = NEW.metadata,
>       updated_at = now()
>     WHERE id = OLD.id;
>     RETURN NEW;
>   END IF;
>   RETURN NULL;
> END;
> $$ LANGUAGE plpgsql SECURITY DEFINER;
> 
> CREATE TRIGGER trg_instead_of_social_accounts
>   INSTEAD OF INSERT OR UPDATE OR DELETE ON public.social_accounts
>   FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_social_accounts();
> 
> 
> -- 5.3 Instead of trigger for user_api_keys
> CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> RETURNS TRIGGER AS $$
> BEGIN
>   IF TG_OP = 'DELETE' THEN
>     DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
>     RETURN OLD;
>   ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
>     INSERT INTO public.user_api_keys_table (
>       user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret
>     ) VALUES (
>       NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret
>     )
>     ON CONFLICT (user_id) DO UPDATE SET
>       groq_api_key = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
>       openrouter_api_key = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
>       openai_api_key = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
>       pref_audio_provider = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
>       pref_image_provider = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
>       pref_video_provider = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
>       elevenlabs_api_key = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
>       google_api_key = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
>       nanobana_api_key = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
>       seedance_api_key = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
>       wp_site_url = NEW.wp_site_url,
>       wp_username = NEW.wp_username,
>       wp_app_password = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
>       pref_ai_model = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
>       replicate_api_key = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
>       higgsfield_api_key = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
>       higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
>       updated_at = now();
>     RETURN NEW;
>   END IF;
>   RETURN NULL;
> END;
> $$ LANGUAGE plpgsql SECURITY DEFINER;
> 
> CREATE TRIGGER trg_instead_of_user_api_keys
>   INSTEAD OF INSERT OR UPDATE OR DELETE ON public.user_api_keys
>   FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_user_api_keys();
> 
> 
> -- ─────────────────────────────────────────────────────────────────────────────
> -- 6. PRIVATE DECRYPTED VIEWS: Real decrypted keys view for service_role
> -- ─────────────────────────────────────────────────────────────────────────────
> === há RPC de disconnect para user_api_keys / provider? ===
> ```

## 🤖 Claude *(03:48:53)*

<details>
<summary>💭 Thinking Process</summary>

I need to verify whether the base table `public.user_api_keys_table` is directly accessible via PostgREST and whether the service role can write to it, bypassing RLS. The `google_api_key` column is likely encrypted in the base table while the view handles decryption, so writing NULL directly would clear the encrypted value. I'm checking what happens when I interact with the column directly.

This is part of resolving alert #3 from the handoff list—clearing a corrupt credential on a QA tenant is low-risk since the value is garbage anyway. I'll read first to verify the current state, then write the update, then confirm it worked. I'm also batching this with committing the proof manifest and pruning scratchpads in parallel.

</details>


## 🤖 Claude *(03:48:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\necho \"=== a tabela BASE \u00e9 alcan\u00e7\u00e1vel pelo service role? (leitura, sem imprimir segredo) ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/user_api_keys_table?select=user_id,updated_at&limit=5\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" 2>/dev/null \\\n | node -e 'let s=\"\";process.stdin.on(\"data\",d=>s+=d).on(\"end\",()=>{try{const r=JSON.parse(s);console.log(Array.isArray(r)?`OK ${r.length} linhas: `+r.map(x=>x.user_id?.slice(0,8)).join(\" \"):s.slice(0,200))}catch(e){console.log(\"raw:\",s.slice(0,250))}})'",
  "description": "Check service-role access to the base credential table"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === a tabela BASE é alcançável pelo service role? (leitura, sem imprimir segredo) ===
> OK 3 linhas: ada39fae 85aaca76 43027d04
> ```

## 🤖 Claude *(03:48:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git add proof-manifest.json && git commit -q -m \"chore(handoff): fecha o proof-manifest do seal de 2026-08-13\n\nO seal apontou o n\u00f3 69c02e4b no HANDOFF mas o manifesto ficou fora do commit\n6bbe8d8 \u2014 a Fase 5c da auditoria de prova material l\u00ea este arquivo, ent\u00e3o um\nmanifesto sujo no worktree \u00e9 um gate que arranca do estado errado.\" && git log -1 --format=\"%H %s\" && git status --short",
  "description": "Commit the pending proof-manifest"
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
> [90m12:48AM[0m [32mINF[0m 1 commits scanned.
> [90m12:48AM[0m [32mINF[0m scan completed in 6.93ms
> [90m12:48AM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.09 seconds)
> ✔️ e2e-output-tripwire (0.02 seconds)
> ✔️ secret-scan (0.04 seconds)
> ✔️ gitleaks-staged (0.08 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> 3a59c52980b04d581bf5e09f04a7c28006a5f70d chore(handoff): fecha o proof-manifest do seal de 2026-08-13
> ```

## 🤖 Claude *(03:49:11)*

<details>
<summary>💭 Thinking Process</summary>

Alert 1 is resolved with a clean git status. Now I need to clear the corrupt key for 85aaca76 and fix the empty string in 43027d04. I'm being careful here since writing directly to the user_api_keys_table bypasses the INSTEAD OF trigger—which is what the procedure calls for—but I should check if there's a Vault secret that needs revoking, and whether the google_api_key field on the base table contains ciphertext.

Looking at the SOP, there's definitely a Vault secret involved, and for a corrupt 22-character string, that secret is garbage too. Let me verify how google_api_key is actually stored and whether there's an encryption trigger on the base table before I proceed with the write.

</details>


## 🤖 Claude *(03:49:11)*

Alerta 1 resolvido (commit `3a59c529`, worktree limpo). Agora o alerta 3 — que revelou um defeito maior do que o anotado.

## 🤖 Claude *(03:49:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== google_api_key na tabela base: texto cifrado ou refer\u00eancia ao Vault? ===\"\ngrep -nE \"google_api_key\" supabase/migrations/20260601000000_credential_encryption.sql | grep -viE \"COALESCE|VALUES|SELECT|,$\" | head -10\necho \"--- triggers de encripta\u00e7\u00e3o na base ---\"\ngrep -nE \"CREATE TRIGGER.*user_api_keys_table|vault_upsert_secret|encrypt_user_api_keys\" supabase/migrations/*.sql | head -8\necho \"=== forma real do valor na base (sem imprimir) ===\"\nset -a; source .env 2>/dev/null; set +a\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/user_api_keys_table?select=user_id,google_api_key\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" 2>/dev/null \\\n | node -e 'let s=\"\";process.stdin.on(\"data\",d=>s+=d).on(\"end\",()=>{const r=JSON.parse(s);console.log(r.map(x=>({u:x.user_id?.slice(0,8),len:(x.google_api_key||\"\").length,prefixo:(x.google_api_key||\"\").slice(0,10),ehVault:/^[0-9a-f-]{36}$/.test(x.google_api_key||\"\")})))})'",
  "description": "Determine storage form of the credential on the base table"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === google_api_key na tabela base: texto cifrado ou referência ao Vault? ===
> 139:  -- google_api_key
> 140:  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> 141:    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 144:      v_id := vault.create_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');
> 145:      NEW.google_api_key = v_id::text;
> 303:    IF r.google_api_key IS NOT NULL AND r.google_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 304:      v_gg := vault.create_secret(r.google_api_key, 'user_api_keys_google_api_key_' || r.user_id::text, 'Google API Key');
> 504:      user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret
> 506:      NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret
> 611:LEFT JOIN vault.decrypted_secrets s_google ON uak.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_google.id = uak.google_api_key::uuid
> --- triggers de encriptação na base ---
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:20:CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:137:-- (trigger tr_encrypt_user_api_keys already bound to the function — no re-create needed)
> supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql:11:-- encrypt trigger uses the IDEMPOTENT `vault_upsert_secret` (20260602140000); the INSTEAD OF is
> supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql:20:-- ── 2. encrypt trigger (live verbatim + firecrawl block; idempotent vault_upsert_secret) ─────────
> supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql:21:CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql:32:      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key'); NEW.groq_api_key = v_id::text;
> supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql:37:      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key'); NEW.openrouter_api_key = v_id::text;
> supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql:42:      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key'); NEW.openai_api_key = v_id::text;
> === forma real do valor na base (sem imprimir) ===
> [
>   { u: 'ada39fae', len: 36, prefixo: 'd3ade4a2-6', ehVault: true },
>   { u: '85aaca76', len: 36, prefixo: '7a62efec-f', ehVault: true },
>   { u: '43027d04', len: 36, prefixo: 'f2a7cca8-9', ehVault: true }
> ]
> ```

## 🤖 Claude *(03:49:36)*

<details>
<summary>💭 Thinking Process</summary>

The base table stores a Vault secret UUID, and the decrypted view joins against the vault secrets table to retrieve the actual values. To properly clear this data, I need to NULL out the API key column for the specific record—the encrypt trigger only fires on updates when the value is distinct and not null, so setting it to NULL should bypass the trigger. Then I'll need to delete the orphaned vault secret entry itself.

There's a second case with a different user where the vault UUID exists but decrypts to an empty string, which needs the same treatment. The challenge is that I can't delete from the vault schema directly through PostgREST since it's not exposed—I'd need to write SQL. A data-cleanup migration is the right approach here and aligns with the project's rule about turning production hotfixes into migrations in the same session. But the deeper issue is that there's no `disconnect_provider` RPC for the user API keys table, which is exactly the kind of durable safeguard the SOP identified as missing. Building that RPC plus the migration is a larger scope decision that would require security review before committing.

The honest assessment is that resolving the alert requires a privileged clear, and the project currently has no proper path for it—that's the real finding. I should do the clear now using the available privileged access by patching the API key field to null via PostgREST with the service role, then verify it through the decrypted view. The vault secret will become orphaned, which is the LGPD residue problem, but for a QA tenant with garbage data it's low-stakes. I'll flag the orphaned secret as a follow-up item with the exact secret name for tracking. Before I proceed, I need to confirm that this user ID is actually from the QA tenant and not a real customer.

</details>


## 🤖 Claude *(03:49:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\necho \"=== quem s\u00e3o os 3 tenants (antes de tocar em qualquer coisa) ===\"\nfor u in ada39fae-67e1-4e53-af1c-5a18e1c108e8 85aaca76 43027d04; do\n  if [ ${#u} -lt 20 ]; then\n    full=$(curl -s \"$VITE_SUPABASE_URL/rest/v1/user_api_keys_table?select=user_id&user_id=ilike.$u%25\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | node -pe 'JSON.parse(require(\"fs\").readFileSync(0,\"utf8\"))[0]?.user_id||\"\"')\n  else full=$u; fi\n  echo \"--- $full\"\n  curl -s \"$VITE_SUPABASE_URL/rest/v1/profiles?select=id,full_name,plan,mco_balance,created_at&id=eq.$full\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | head -c 300; echo\ndone",
  "description": "Identify the three tenants before modifying credentials"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === quem são os 3 tenants (antes de tocar em qualquer coisa) ===
> --- ada39fae-67e1-4e53-af1c-5a18e1c108e8
> {"code":"42703","details":null,"hint":null,"message":"column profiles.plan does not exist"}
> --- 
> {"code":"42703","details":null,"hint":null,"message":"column profiles.plan does not exist"}
> --- 
> {"code":"42703","details":null,"hint":null,"message":"column profiles.plan does not exist"}
> ```

## 🤖 Claude *(03:49:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nFULL85=$(curl -s \"$VITE_SUPABASE_URL/rest/v1/user_api_keys_table?select=user_id&user_id=ilike.85aaca76%25\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | node -pe 'JSON.parse(require(\"fs\").readFileSync(0,\"utf8\"))[0]?.user_id||\"\"')\nFULL43=$(curl -s \"$VITE_SUPABASE_URL/rest/v1/user_api_keys_table?select=user_id&user_id=ilike.43027d04%25\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | node -pe 'JSON.parse(require(\"fs\").readFileSync(0,\"utf8\"))[0]?.user_id||\"\"')\necho \"85aaca76 \u2192 $FULL85\"; echo \"43027d04 \u2192 $FULL43\"\necho \"=== perfis (colunas reais) ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/profiles?select=*&id=in.($FULL85,$FULL43,ada39fae-67e1-4e53-af1c-5a18e1c108e8)\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" \\\n | node -e 'let s=\"\";process.stdin.on(\"data\",d=>s+=d).on(\"end\",()=>{const r=JSON.parse(s);r.forEach(p=>console.log(JSON.stringify({id:p.id?.slice(0,8),nome:p.full_name,tier:p.subscription_tier||p.plan_tier,saldo:p.mco_balance,criado:p.created_at?.slice(0,10)})))})'\necho \"$FULL85\" > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/u85.txt",
  "description": "Resolve full UUIDs and read profiles"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 85aaca76 → 
> 43027d04 → 
> === perfis (colunas reais) ===
> [eval]:1
> let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const r=JSON.parse(s);r.forEach(p=>console.log(JSON.stringify({id:p.id?.slice(0,8),nome:p.full_name,tier:p.subscription_tier||p.plan_tier,saldo:p.mco_balance,criado:p.created_at?.slice(0,10)})))})
>                                                                                 ^
> 
> TypeError: r.forEach is not a function
>     at Socket.<anonymous> ([eval]:1:81)
>     at Socket.emit (node:events:531:35)
>     at endReadableNT (node:internal/streams/readable:1698:12)
>     at process.processTicksAndRejections (node:internal/process/task_queues:89:21)
> 
> Node.js v22.22.3
> ```

## 🤖 Claude *(03:49:56)*

<details>
<summary>💭 Thinking Process</summary>

I see that `ilike` won't work on UUID columns, so I'll just retrieve all three user IDs directly from the table instead.

</details>


## 🤖 Claude *(03:50:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nIDS=$(curl -s \"$VITE_SUPABASE_URL/rest/v1/user_api_keys_table?select=user_id\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | node -pe 'JSON.parse(require(\"fs\").readFileSync(0,\"utf8\")).map(x=>x.user_id).join(\",\")')\necho \"IDs: $IDS\"\necho \"=== perfis ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/profiles?select=id,full_name,mco_balance,created_at&id=in.($IDS)\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"\necho \"\"\necho \"=== esses tenants t\u00eam conte\u00fado real? (assets criados) ===\"\nfor u in $(echo $IDS | tr ',' ' '); do\n  n=$(curl -s -I \"$VITE_SUPABASE_URL/rest/v1/creative_assets?select=id&user_id=eq.$u\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" -H \"Prefer: count=exact\" -H \"Range: 0-0\" 2>/dev/null | grep -i content-range)\n  echo \"  ${u:0:8} \u2192 assets: $n\"\ndone",
  "description": "Resolve tenant identities and content footprint"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> IDs: ada39fae-67e1-4e53-af1c-5a18e1c108e8,85aaca76-c5e2-42bc-8f32-b51b7a8029e2,43027d04-8239-4dd7-9a70-4496c3b1be7a
> === perfis ===
> [{"id":"85aaca76-c5e2-42bc-8f32-b51b7a8029e2","full_name":"SMOKETEST","mco_balance":1.00,"created_at":"2026-08-05T22:51:01.110259+00:00"}, 
>  {"id":"43027d04-8239-4dd7-9a70-4496c3b1be7a","full_name":"TikTok App Review","mco_balance":1351.00,"created_at":"2026-07-30T13:23:08.744101+00:00"}, 
>  {"id":"ada39fae-67e1-4e53-af1c-5a18e1c108e8","full_name":"Gabriel Rocha","mco_balance":40775.00,"created_at":"2026-04-17T05:57:46.249257+00:00"}]
> === esses tenants têm conteúdo real? (assets criados) ===
>   ada39fae → assets: content-range: 0-261/262
>   85aaca76 → assets: content-range: */0
>   43027d04 → assets: content-range: 0-1/2
> ```

## 🤖 Claude *(03:50:11)*

<details>
<summary>💭 Thinking Process</summary>

I'm reviewing two tenant records to assess what can be safely deleted. The first one, labeled "SMOKETEST," is clearly a QA throwaway with no assets, so its garbage key is safe to clear. The second, "TikTok App Review," is a legitimate demo tenant from an approved project with substantial data—1351 records and 2 assets—but its Google API key appears to be an empty string, which is unusual.

An empty string isn't truly garbage; it's falsy and fails safely in the code, so it's not causing harm. However, since this tenant was used for a platform review, touching it carries more risk than benefit. I'll flag it but leave it alone. My plan is to clear only the SMOKETEST tenant by patching its key to null in the base table, then verify the change through the decrypted view and re-run the probe to confirm. The encryption trigger should handle the null value correctly by skipping the encryption logic.

</details>


## 🤖 Claude *(03:50:11)*

Identificado: `85aaca76` = **"SMOKETEST"** (throwaway de QA, 0 assets). O outro é o tenant do review da TikTok — não toco.

## 🤖 Claude *(03:50:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nU=85aaca76-c5e2-42bc-8f32-b51b7a8029e2\necho \"=== ANTES ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/decrypted_user_api_keys?select=user_id,google_api_key&user_id=eq.$U\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | node -pe 'const r=JSON.parse(require(\"fs\").readFileSync(0,\"utf8\"));JSON.stringify(r.map(x=>({u:x.user_id.slice(0,8),len:(x.google_api_key||\"\").length,nulo:x.google_api_key===null})))'\necho \"=== LIMPANDO (PATCH na tabela BASE \u2014 a view mascarada n\u00e3o limpa com null, SOP credential-disconnect-clear) ===\"\ncurl -s -o /dev/null -w \"HTTP %{http_code}\\n\" -X PATCH \"$VITE_SUPABASE_URL/rest/v1/user_api_keys_table?user_id=eq.$U\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" -H \"Content-Type: application/json\" -H \"Prefer: return=minimal\" \\\n  -d '{\"google_api_key\": null}'\necho \"=== DEPOIS ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/decrypted_user_api_keys?select=user_id,google_api_key&user_id=eq.$U\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | node -pe 'const r=JSON.parse(require(\"fs\").readFileSync(0,\"utf8\"));JSON.stringify(r.map(x=>({u:x.user_id.slice(0,8),len:(x.google_api_key||\"\").length,nulo:x.google_api_key===null})))'\necho \"=== a chave do User 0 continua intacta? (a limpeza tem que ser cir\u00fargica) ===\"\ncurl -s \"$VITE_SUPABASE_URL/rest/v1/decrypted_user_api_keys?select=user_id,google_api_key&user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | node -pe 'const r=JSON.parse(require(\"fs\").readFileSync(0,\"utf8\"));JSON.stringify(r.map(x=>({u:x.user_id.slice(0,8),len:(x.google_api_key||\"\").length,sufixo:(x.google_api_key||\"\").slice(-6)})))'",
  "description": "Clear the corrupt key on the SMOKETEST tenant"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === ANTES ===
> [{"u":"85aaca76","len":22,"nulo":false}]
> === LIMPANDO (PATCH na tabela BASE — a view mascarada não limpa com null, SOP credential-disconnect-clear) ===
> HTTP 204
> === DEPOIS ===
> [{"u":"85aaca76","len":0,"nulo":true}]
> === a chave do User 0 continua intacta? (a limpeza tem que ser cirúrgica) ===
> [{"u":"ada39fae","len":39,"sufixo":"_EwXDo"}]
> ```

## 🤖 Claude *(03:50:29)*

<details>
<summary>💭 Thinking Process</summary>

I've cleared the API key and confirmed user 0's key is still intact. Now I need to re-run the probe to verify the alert disappears, then clean up the scratchpads and review the forensics and workflow. I should also check whether the probe is properly flagging the SHAPE issue in addition to the HTTP 400 response it already caught.

The real vulnerability is on the read side where garbage data passes through validation. I'm going to add a shape guard to the canonical image endpoint in the gemini-image module, but first I'll run the probe again and prune the scratchpads.

</details>


## 🤖 Claude *(03:50:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "timeout 120 bun run scripts/qa/probe-google-key.ts 2>&1 | grep -vE \"Supabase CLI|We recommend\" | tail -12",
  "description": "Re-run probe to confirm alert cleared",
  "timeout": 150000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 🔑 CHAVES GOOGLE — onde vivem e se funcionam
> 
>   ✅ COFRE user_api_keys [ada39fae]                                …_EwXDo     HTTP 200
>   🔒 COFRE edge functions: GEMINI_API_KEY + MESH_EMBED_GEMINI_KEY  …sha a85b822f valor oculto — só digest  (mesma chave nos dois nomes)
> 
> ✅ 1 cofre(s) com chave VIVA
> ```

## 🤖 Claude *(03:50:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf; cat forense.log; wc -l *cuts.txt 2>/dev/null; cat dl.log; ls -la cully.mp4; df -h / | tail -1",
  "description": "Check forensics progress and disk"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 0 oneiric-cuts.txt
> oneiric done: 520032509 bytes
> cully done: 2818862432 bytes
> -rw-rw-r-- 1 ubuntu ubuntu 2818862432 Aug 14 00:49 cully.mp4
> /dev/sda1       193G  151G   42G  79% /
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:50:49)*

<details>
<summary>💭 Thinking Process</summary>

Alert 3 is resolved and the vault is no longer showing as dead. Cully's download finished at 2.82 GB, pushing disk usage to 79%, while the forensics analysis is still processing on oneiric with scene detection running slowly across the footage. I'm pruning the scratchpads now that the harvest is complete and verified, starting with the older files to reclaim disk space.

For the 2de725c0 directory, I'm checking what's actually needed: the build and motion work are already in the repo, benchmarks are cached in memory, and the frame images can be deleted. The video files need careful deduplication — some are already harvested duplicates, others are encoding benchmark outputs where only the findings matter, so the raw files are disposable. I'll preserve any unique videos over 3MB into the benchmarks folder to be safe.

The 9b9cb2fa session is confirmed as fully harvested — the kit and runners are already in their proper locations, leaving only regenerable intermediate frames and scene HTMLs. I'm going to write a script to do a proper md5 sweep across all large media files in the old scratchpads, copy anything unique, then delete everything else.

</details>


## 🤖 Claude *(03:50:49)*

Alerta 3 resolvido — a sonda agora só reporta o cofre vivo. Agora a poda do disco, com o gate de colheita.

## 🤖 Claude *(03:50:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra\nDEST=repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/motor-benchmarks\n# md5 de tudo que J\u00c1 est\u00e1 preservado fora do /tmp\nfind repurpose-inbox -type f \\( -name \"*.mp4\" -o -name \"*.mp3\" -o -name \"*.wav\" \\) -exec md5sum {} + 2>/dev/null | awk '{print $1}' | sort -u > /tmp/preservados.md5\necho \"j\u00e1 preservados fora do /tmp: $(wc -l < /tmp/preservados.md5) arquivos de m\u00eddia (por md5)\"\necho \"=== m\u00eddia >1MB nos scratchpads a podar que N\u00c3O tem c\u00f3pia preservada ===\"\nfor d in 2de725c0-2186-4fa8-9a12-16d4bd8f3128 dfd4c8a3-8149-4c5f-8d9c-f6076b019b22 c1b6a7b1-691a-443b-a950-94444ce8065d 9b9cb2fa-663b-4f25-98b8-c32877cbffb1; do\n  find $T/$d/scratchpad -type f \\( -name \"*.mp4\" -o -name \"*.mp3\" -o -name \"*.wav\" \\) -size +1M -exec md5sum {} + 2>/dev/null\ndone | sort -u -k1,1 | while read h p; do\n  grep -q \"^$h$\" /tmp/preservados.md5 || echo \"\u00d3RF\u00c3O $(stat -c %s \"$p\") $h $p\"\ndone",
  "description": "Harvest gate: find media with no preserved copy"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> já preservados fora do /tmp: 68 arquivos de mídia (por md5)
> === mídia >1MB nos scratchpads a podar que NÃO tem cópia preservada ===
> ÓRFÃO 2310902 05dba34c7892154895092527d41a3bb0 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/7a70b462.mp4
> ÓRFÃO 2012276 07cfe8577d6417e0051fa2867f66e93b /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/vidprobe/clip-h264-g30.mp4
> ÓRFÃO 1314909 25fb8a298fc55a2f3e28054db4a79fdb /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/motion-promo-c01/gancho-8s-16x9.mp4
> ÓRFÃO 2506773 2a7c0d504eb2e9580a38cc4c380a3ba2 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/f9b9b2cc.mp4
> ÓRFÃO 3916828 31202056e728f3f9304ee8de2e85d590 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/vidprobe/clip-h264-g1.mp4
> ÓRFÃO 1487860 329f77886a9ec3a7f12f0d021e5a7673 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/comB.mp4
> ÓRFÃO 1428605 49032f307ba94ffb3fb71f6c9a032c45 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/semB.mp4
> ÓRFÃO 2507790 4f5985c23b9ed4f2c85346c8f8a221a9 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/wA.mp4
> ÓRFÃO 1406713 5bdb2f53c73442040880d57d02a17ec9 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/vidprobe/out-c.mp4
> ÓRFÃO 1285289 5c70ccd766da86f4b57432452c338d42 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/ce1e4558.mp4
> ÓRFÃO 2507790 5e771314968b2f166399bf1fa0a9f965 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/0165a56b.mp4
> ÓRFÃO 2653435 61372d22f399086f693e04a66b57b829 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/vw/e2.mp4
> ÓRFÃO 1319558 630cb12a0b6de2403307def1e1e10978 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/probe3d/ffwork/o.mp4
> ÓRFÃO 2296914 68db2c9452fa036fd9a589a0aa4dc0a8 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/daba7fef.mp4
> ÓRFÃO 2294483 755f72368442675784e947bf8df9b1fa /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/35a10563.mp4
> ÓRFÃO 4996643 7fbfd7165e93a051e9e9bf3ddcf66c48 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ato3-audio/ato3-audio.mp4
> ÓRFÃO 2507790 8415ad9683db0cf8378f5c805f28b8f4 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/7b9024cd.mp4
> ÓRFÃO 2313333 8bceefed6e850dc02232534fdb3aa724 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/b9dc9601.mp4
> ÓRFÃO 4937557 8c0bb5c52349437c6a3692dd4d7e40e9 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ato2-adsense/ato2-adsense.mp4
> ÓRFÃO 2311672 94e40784f13cf2ca3cc1cd2212276749 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/26213870.mp4
> ÓRFÃO 1487860 980e361adfa9f1357d7bcb443933204a /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/comA.mp4
> ÓRFÃO 3601755 9d75e492f89ed5b15ee1b64b89112024 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/m1/mp_png.mp4
> ÓRFÃO 4693092 9dbcac3425edc58695e8ec06db69d22b /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit/src.mp4
> ÓRFÃO 1326504 9e0d255a5240ac1f1d7d5697e3d82d0e /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/probe3d/arch/allcss.mp4
> ÓRFÃO 5553085 a53d90f5c9aed9aee6b73a0a66db0b18 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/m1/mp_j92.mp4
> ÓRFÃO 2310902 a580ffec086dc0298a6a36b8094f638a /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/72c0f938.mp4
> ÓRFÃO 1428605 a76ef71dc3c86fe1796e0177f15b9642 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/semA.mp4
> ÓRFÃO 2322134 e0f0a7ee71ed8cc7225978394f1ca487 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/e2e/motion_e2e.mp4
> ÓRFÃO 2310338 e370bfa20977341765a67a3e1a72aea2 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/02f02c69.mp4
> ÓRFÃO 2353024 e58f30c45f7d22fea637e90813413bb9 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/e2e/rich.mp4
> ÓRFÃO 3766258 ef5601b36105b7fc452e2115545d6753 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/m1/mp_j100.mp4
> ÓRFÃO 1285289 fc0440eefc6d8dc2de98d4949fb297fc /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/2de725c0-2186-4fa8-9a12-16d4bd8f3128/scratchpad/crit2/20502e56.mp4
> ```

## 🤖 Claude *(03:51:15)*

<details>
<summary>💭 Thinking Process</summary>

Looking at the orphaned files, most of them are from that August 7th session with the A/B testing and benchmarking work — the critic reproductions, encoder benchmarks, and the various quality tests that ended up consuming a lot of memory. There are just two stragglers from an earlier commit related to episode 7 rendering.

The real question is whether to keep everything as insurance or be selective. The findings from all those benchmarks are already documented, so the raw files themselves are just taking up space. I'll harvest the three actually useful pieces — the two episode 7 renders and that motion promo clip from the earlier session — and delete the rest of the ephemeral benchmark output.

</details>


## 🤖 Claude *(03:51:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra\nDEST=repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/motor-benchmarks\ncp $T/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ato2-adsense/ato2-adsense.mp4 $DEST/ep07-ato2-adsense-2026-08-11.mp4\ncp $T/c1b6a7b1-691a-443b-a950-94444ce8065d/scratchpad/ep07-master/ato3-audio/ato3-audio.mp4  $DEST/ep07-ato3-audio-2026-08-11.mp4\ncp $T/dfd4c8a3-8149-4c5f-8d9c-f6076b019b22/scratchpad/motion-promo-c01/gancho-8s-16x9.mp4    $DEST/motion-promo-gancho-8s-16x9.mp4\ncat > $DEST/LEIA-ME.md <<'EOF'\n# motor-benchmarks \u2014 o acervo de refer\u00eancia do motor de v\u00eddeo\n\nColhido em 2026-08-14 dos scratchpads de sess\u00e3o ANTES da poda de disco (SOP\n`docs/processes/scratchpad-harvest.md`). Tudo aqui \u00e9 material que existia S\u00d3 em `/tmp` e\nseria perdido no pr\u00f3ximo reboot do host.\n\n| Arquivo | O que \u00e9 | Por que sobreviveu |\n|---|---|---|\n| `benchmark-fcf91d44-APROVADO.mp4` | A pe\u00e7a MONTAR **aprovada pelo Sovereign** (2026-08-06) que virou a refer\u00eancia do motor v2 | \u00c9 citada pelo nome no HANDOFF, no sprint-priorities e na mem\u00f3ria `project_motor_montar`. S\u00f3 existia em `/tmp`. md5 `05e85b3fc35097cfe44d167bfab301c1` |\n| `comparativo-2ba98e10.mp4` | O modelo perdedor do A/B da mesma sess\u00e3o | Prova material do porqu\u00ea da escolha |\n| `ep07-master-dataviz-2026-08-11.mp4` | Master EP07 do pipeline data-viz (motor `scene-template.ts`) | O \"pipeline de produ\u00e7\u00e3o provado\" do seal de 2026-08-11 |\n| `ep07-adsense-pilot-dataviz-2026-08-11.mp4` | Piloto do bloco AdSense, gera\u00e7\u00e3o data-viz | Antecessor do piloto MONTAR \u2014 compara\u00e7\u00e3o de linguagem |\n| `ep07-ato2-adsense-2026-08-11.mp4` | Ato 2 renderizado | idem |\n| `ep07-ato3-audio-2026-08-11.mp4` | Ato 3 renderizado | idem |\n| `motion-promo-gancho-8s-16x9.mp4` | Gancho 8s 16:9 pela skill `motion-promo` | \u00danico output sobrevivente daquela skill |\n\n**Descartado na mesma poda (regener\u00e1vel, achados j\u00e1 em mem\u00f3ria/doc):** ~75 MB de sa\u00eddas de\nbench de encoder (`vidprobe/`, `m1/mp_j*`), reprodu\u00e7\u00f5es de cr\u00edtico (`crit2/`), A/Bs com/sem\nefeito, e ~6,4 GB de frames PNG/JPG intermedi\u00e1rios. Os achados desses benches vivem em\n`reference_motion_render_economics` e em `scripts/qa/bench-motion-cost.mjs`.\nEOF\necho \"=== ACERVO FINAL ===\"; ls -la $DEST; du -sh $DEST",
  "description": "Complete the harvest with a manifest"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === ACERVO FINAL ===
> total 33516
> drwxrwsr-x 2 ubuntu gcrUX    4096 Aug 14 00:51 .
> drwxrwsr-x 6 gcrUX  gcrUX    4096 Aug 14 00:44 ..
> -rw-rw-r-- 1 ubuntu gcrUX 3069023 Aug 14 00:44 benchmark-fcf91d44-APROVADO.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 4619308 Aug 14 00:44 comparativo-2ba98e10.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 5419080 Aug 14 00:44 ep07-adsense-pilot-dataviz-2026-08-11.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 4937557 Aug 14 00:51 ep07-ato2-adsense-2026-08-11.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 4996643 Aug 14 00:51 ep07-ato3-audio-2026-08-11.mp4
> -rw-rw-r-- 1 ubuntu gcrUX 9933520 Aug 14 00:44 ep07-master-dataviz-2026-08-11.mp4
> -rw-rw-r-- 1 ubuntu gcrUX    1664 Aug 14 00:51 LEIA-ME.md
> -rw-rw-r-- 1 ubuntu gcrUX 1314909 Aug 14 00:51 motion-promo-gancho-8s-16x9.mp4
> 33M	repurpose-inbox/ada39fae-67e1-4e53-af1c-5a18e1c108e8/motor-benchmarks
> ```

## 🤖 Claude *(03:51:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra\nANTES=$(du -sh . 2>/dev/null | cut -f1)\nATIVA=863fa9e6-3ea7-490f-99e3-99a1876199e3\n# poda: tudo que n\u00e3o \u00e9 a sess\u00e3o ativa. Colheita feita e verificada por md5.\nN=0; for d in */; do d=${d%/}; [ \"$d\" = \"$ATIVA\" ] && continue; rm -rf \"$d\" && N=$((N+1)); done\nDEPOIS=$(du -sh . 2>/dev/null | cut -f1)\necho \"podadas: $N sess\u00f5es \u00b7 $ANTES \u2192 $DEPOIS\"\nls -1 | wc -l; df -h / | tail -1",
  "description": "Prune all inactive scratchpad sessions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> podadas: 41 sessões · 9.7G → 3.2G
> 1
> /dev/sda1       193G  145G   49G  75% /
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:51:47)*

<details>
<summary>💭 Thinking Process</summary>

I've freed up 6.5 GB of disk space, bringing it from 79% to 75% full with 49GB available now. The remaining 3.2GB is tied up in the active session, mostly from those two Higgsfield video files. Let me verify the workflow and forensics status — the forensics process was running in the active session directory with nohup, so it should have persisted even after I killed the main process.

Now I need to add the anticorpo for the truthy-garbage key and check the overall workflow status before batching everything.

</details>


## 🤖 Claude *(03:51:48)*

Liberados **6,5 GB** (79% → 75%). Agora o anticorpo do defeito que o alerta 3 revelou.

## 🤖 Claude *(03:51:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf; cat forense.log 2>/dev/null; wc -l *cuts.txt 2>/dev/null; ps aux | grep -c \"[f]fmpeg\"",
  "description": "Check forensics progress"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> oneiric cortes: 0
> 0 cully-cuts.txt
> 0 oneiric-cuts.txt
> 0 total
> 2
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:51:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; sed -n '1,70p' scripts/lib/gemini-image.ts",
  "description": "Read the canonical image helper to add the shape guard"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /**
>  * Geração de imagem pela API **Gemini/Google DIRETA** — nunca via OpenRouter.
>  *
>  * Diretiva Sovereign 2026-08-12: *"para imagens sempre usa nanobanana mas na api gemini ou
>  * google que temos disponíveis e não pelo openrouter"*.
>  *
>  * Por que a diretiva existe (e por que ela está certa):
>  *   - o intermediário cobra margem e some com parâmetros nativos (aspect_ratio, image_size);
>  *   - a conta do OpenRouter fechou NEGATIVA em 2026-08-12 (40 comprados / 40,244 usados) —
>  *     estourada pelas 10 imagens do próprio EP07, e a próxima chamada devolve 402;
>  *   - o rail é BYOK per-user, e a coluna canônica da casa é `user_api_keys.google_api_key`
>  *     (NUNCA `gemini_api_key`, que não existe — [[reference_byok_gemini_column]]).
>  *
>  * Contrato: o mesmo `:generateContent` + `responseModalities` já provado em produção pelo
>  * `supabase/functions/tts-speak/index.ts:92-115` (lá com ["AUDIO"], aqui com ["IMAGE"]).
>  * A imagem volta em `candidates[0].content.parts[].inlineData.data` como base64.
>  *
>  * ⚠️ NÃO VERIFICADO nesta sessão: a chave Google que temos (`.env` e `user_api_keys` do User 0
>  * — são a MESMA, terminada em 1Vjw-o) devolve **HTTP 403 "reported as leaked"**. Nenhuma
>  * chamada deste módulo foi executada com sucesso ainda. O contrato abaixo é o padrão
>  * documentado + o molde provado da casa, não uma prova de execução. Rotacionar a chave é
>  * pré-condição — e o primeiro `generate()` que passar É o gate.
>  */
> 
> /** Modelos de imagem do Google. O nome comercial NÃO é ID chamável — "Nano Banana 2" não existe
>  *  como identificador; o ID é o da coluna do meio. */
> export const GEMINI_IMAGE_MODELS = {
>   /** "Nano Banana 2" — recomendado pela decisão de 2026-08-12 (melhor aderência a prompt
>    *  multi-restrição). ⚠️ contrapartida a A/B: foi otimizado para TEXTO legível, o que pode
>    *  trabalhar CONTRA uma peça que deve ficar muda. */
>   nanoBanana2: "gemini-3.1-flash-image",
>   /** "Nano Banana Pro" */
>   nanoBananaPro: "gemini-3-pro-image",
>   /** "Nano Banana" — o que o rail usa hoje em 35 pontos do código. */
>   nanoBanana: "gemini-2.5-flash-image",
> } as const;
> 
> export type GeminiImageModel = (typeof GEMINI_IMAGE_MODELS)[keyof typeof GEMINI_IMAGE_MODELS] | string;
> 
> export type GenerateImageOptions = {
>   prompt: string;
>   model?: GeminiImageModel;
>   apiKey?: string;
>   /** "1K" | "2K" | "4K" — o K é MAIÚSCULO. 2K é o teto útil: a máscara do u2net nasce em grafo
>    *  320×320, então 4K não compra borda melhor, só arquivo maior. */
>   imageSize?: "1K" | "2K" | "4K";
>   aspectRatio?: "1:1" | "16:9" | "9:16" | "4:3" | "3:4";
>   timeoutMs?: number;
> };
> 
> export type GenerateImageResult = {
>   bytes: Uint8Array;
>   mimeType: string;
>   model: string;
>   /** texto que o modelo devolveu junto (às vezes explica recusa) */
>   text?: string;
> };
> 
> /**
>  * Resolve a chave na ordem da doutrina de tenancy (CLAUDE.md · API Tenancy Model):
>  *
>  *   1. argumento explícito (teste pontual);
>  *   2. **`user_api_keys.google_api_key` — o COFRE, cifrado no banco** (caminho canônico);
>  *   3. `.env` — fallback declarado, só para bootstrap.
>  *
>  * Diretiva Sovereign 2026-08-12: *"no env não pode ter mais nada, a ideia é guardar tudo no
>  * vault"*. Este resolvedor cumpre isso: o runner de CLI passa a ler a chave do provedor do
>  * mesmo lugar que a plataforma lê — a view cifrada `decrypted_user_api_keys`, com a
>  * `SB_SECRET_KEY` como única credencial que precisa viver no `.env`.
>  *
> ```

## 🤖 Claude *(03:51:57)*

<details>
<summary>💭 Thinking Process</summary>

I see the issue now — the scene detection returned zero cuts because the showinfo filter output was being suppressed by the error-level logging. I need to switch to info-level logging or use the metadata filter to write directly to a file instead. Let me try a different approach with the select filter to properly capture the frame data.

I'll also add downscaling to speed up the processing, then tackle the guard logic in the image resolution code once I've fixed the forensics issue.

</details>


## 🤖 Claude *(03:52:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\npkill -f \"select=gt.scene\" 2>/dev/null; sleep 1\n# defeito da 1a tentativa: showinfo escreve em n\u00edvel INFO e -loglevel error engolia tudo \u2192 0 cortes.\n# Corre\u00e7\u00e3o: metadata=print grava em arquivo. Downscale antes do select acelera ~10x.\nnohup bash -c '\nfor f in oneiric cully; do\n  ffmpeg -threads 3 -hide_banner -loglevel error -i $f.mp4 \\\n    -vf \"scale=426:-2,select=gt(scene\\,0.30),metadata=print:file=$f-cuts.raw\" -an -f null - 2>&1\n  grep -oE \"pts_time:[0-9.]+\" $f-cuts.raw | cut -d: -f2 > $f-cuts.txt\n  echo \"$f cortes: $(wc -l < $f-cuts.txt)\"\ndone' > forense.log 2>&1 &\necho \"forense v2 iniciada\"",
  "description": "Restart scene detection with corrected ffmpeg invocation"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 144
> ```

## 🤖 Claude *(03:52:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; sed -n '70,130p' scripts/lib/gemini-image.ts",
  "description": "Read the key resolver body"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  *
>  * Por que o `.env` não fica VAZIO: para abrir qualquer cofre é preciso uma chave, e essa
>  * primeira chave não pode estar dentro do cofre que ela abre — é o paradoxo de bootstrap já
>  * registrado na SOP dos 3 cofres. O `.env` guarda só o que abre o cofre (`SB_SECRET_KEY` +
>  * URL); toda credencial de PROVEDOR sai dele.
>  */
> const USER_ZERO = "ada39fae-67e1-4e53-af1c-5a18e1c108e8";
> 
> async function keyFromVault(userId = USER_ZERO): Promise<string | null> {
>   const url = process.env.VITE_SUPABASE_URL;
>   const secret = process.env.SB_SECRET_KEY;
>   if (!url || !secret) return null;
>   try {
>     const res = await fetch(
>       `${url}/rest/v1/decrypted_user_api_keys?user_id=eq.${userId}&select=google_api_key`,
>       { headers: { apikey: secret, Authorization: `Bearer ${secret}` } },
>     );
>     if (!res.ok) return null;
>     const rows = await res.json();
>     const key = Array.isArray(rows) ? rows[0]?.google_api_key : null;
>     return typeof key === "string" && key.length > 10 ? key : null;
>   } catch {
>     return null; // cofre indisponível não pode derrubar o runner — o fallback decide
>   }
> }
> 
> async function resolveKey(explicit?: string): Promise<string> {
>   if (explicit) return explicit;
>   const fromVault = await keyFromVault();
>   if (fromVault) return fromVault;
>   const fromEnv = process.env.GOOGLE_API_KEY ?? process.env.GEMINI_API_KEY;
>   if (fromEnv) {
>     console.warn(
>       "⚠️  chave Google veio do .env, não do cofre — grave-a em user_api_keys.google_api_key " +
>         "(bash scripts/qa/set-google-key.sh) para cumprir a diretiva de 2026-08-12",
>     );
>     return fromEnv;
>   }
>   throw new Error(
>     "sem chave Google no cofre (user_api_keys.google_api_key) nem no .env. " +
>       "Grave com: bash scripts/qa/set-google-key.sh — a diretiva de 2026-08-12 proíbe " +
>       "cair no OpenRouter para imagem",
>   );
> }
> 
> export async function generateImage(opts: GenerateImageOptions): Promise<GenerateImageResult> {
>   const model = opts.model ?? GEMINI_IMAGE_MODELS.nanoBanana2;
>   const key = await resolveKey(opts.apiKey);
>   const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
> 
>   const generationConfig: Record<string, unknown> = { responseModalities: ["IMAGE"] };
>   // imageConfig só existe nos modelos de imagem; enviá-lo a um modelo de texto é 400.
>   const imageConfig: Record<string, unknown> = {};
>   if (opts.aspectRatio) imageConfig.aspectRatio = opts.aspectRatio;
>   if (opts.imageSize) imageConfig.imageSize = opts.imageSize;
>   if (Object.keys(imageConfig).length) generationConfig.imageConfig = imageConfig;
> 
>   const ctl = new AbortController();
>   const timer = setTimeout(() => ctl.abort(), opts.timeoutMs ?? 120_000);
>   let res: Response;
>   try {
> ```

## 🤖 Claude *(03:52:12)*

<details>
<summary>💭 Thinking Process</summary>

The guard `key.length > 10` is way too loose—the corrupt key at 22 characters slips right through, but a real Google API key follows the pattern `AIza` plus 35 alphanumeric characters for 39 total. I need to validate against that specific format with a regex. The exit 144 from the forensics command is puzzling, possibly from pkill terminating something unexpectedly, so I'll apply the proper key validation and recheck the forensics execution.

I'll add the shape validation at the `keyFromVault()` call site to reject malformed keys with a clear warning that names the tenant, and also export a helper function so other parts of the code can reuse the same validation logic.

</details>


## 🤖 Claude *(03:52:12)*

O guard existente é `key.length > 10` — e a chave corrompida tinha **22 caracteres**. Passava. Vou fechar na forma.

## 🤖 Claude *(03:52:21)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/lib/gemini-image.ts",
  "old_string": "const USER_ZERO = \"ada39fae-67e1-4e53-af1c-5a18e1c108e8\";\n\nasync function keyFromVault(userId = USER_ZERO): Promise<string | null> {",
  "new_string": "const USER_ZERO = \"ada39fae-67e1-4e53-af1c-5a18e1c108e8\";\n\n/**\n * A forma de uma chave do Google AI Studio: `AIza` + 35 caracteres do alfabeto base64url.\n * Sempre 39 no total.\n *\n * Por que isto existe (achado material de 2026-08-14): o cofre do tenant `85aaca76`\n * (SMOKETEST) guardava uma string de **22 caracteres** come\u00e7ando em `AIza` e terminando em\n * `called` \u2014 restos de uma mensagem de erro gravada como se fosse credencial. O guard antigo\n * aqui era `key.length > 10`, ent\u00e3o a sucata passava: **truthy n\u00e3o \u00e9 v\u00e1lido**. Cada uma das\n * 15 edge functions que faz `userKeys?.google_api_key` herda o mesmo defeito \u2014 manda a sucata\n * para o Google e recebe um HTTP 400 opaco, em vez do 402 estruturado\n * `google_not_configured` que o contrato de tenancy promete (CLAUDE.md \u00b7 API Tenancy Model).\n *\n * Uma chave malformada \u00e9 PIOR que chave ausente: ausente falha fechado com mensagem \u00fatil;\n * malformada falha aberto, no meio de um render, sem dizer o porqu\u00ea.\n */\nexport function looksLikeGoogleApiKey(key: unknown): key is string {\n  return typeof key === \"string\" && /^AIza[A-Za-z0-9_-]{35}$/.test(key);\n}\n\nasync function keyFromVault(userId = USER_ZERO): Promise<string | null> {"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/lib/gemini-image.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:52:30)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/lib/gemini-image.ts",
  "old_string": "    const rows = await res.json();\n    const key = Array.isArray(rows) ? rows[0]?.google_api_key : null;\n    return typeof key === \"string\" && key.length > 10 ? key : null;",
  "new_string": "    const rows = await res.json();\n    const key = Array.isArray(rows) ? rows[0]?.google_api_key : null;\n    if (looksLikeGoogleApiKey(key)) return key;\n    if (typeof key === \"string\" && key.length > 0) {\n      // Sucata no cofre: diz QUAL tenant e o que fazer. Nunca imprime a chave.\n      console.warn(\n        `\u26a0\ufe0f  o cofre do tenant ${userId.slice(0, 8)} tem um valor em google_api_key que N\u00c3O \u00e9 ` +\n          `uma chave do Google (${key.length} caracteres; o formato \u00e9 AIza + 35). Tratando como ` +\n          `AUSENTE \u2014 falhar fechado \u00e9 melhor que mandar sucata para a API. ` +\n          `Limpe com o caminho da SOP docs/processes/credential-disconnect-clear.md ` +\n          `(PATCH na tabela BASE user_api_keys_table \u2014 a view mascarada N\u00c3O limpa com null) ` +\n          `e regrave com: bash scripts/qa/set-google-key.sh`,\n      );\n    }\n    return null;"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/lib/gemini-image.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:52:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== o guard funciona? (teste direto da fun\u00e7\u00e3o, sem rede) ===\"\ncat > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/guard-test.ts <<'EOF'\nimport { looksLikeGoogleApiKey } from \"./scripts/lib/gemini-image.ts\";\nconst casos: [string, unknown, boolean][] = [\n  [\"chave real (AIza + 35 = 39)\", \"AIza\" + \"A\".repeat(35), true],\n  [\"a sucata do SMOKETEST (22 ch)\", \"AIzaSyMethodNotcalled\", false],\n  [\"string vazia (tenant TikTok)\", \"\", false],\n  [\"null\", null, false],\n  [\"placeholder mascarado\", \"\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\", false],\n  [\"curta mas >10 (o guard antigo passava)\", \"AIzaAAAAAAAAAAA\", false],\n];\nlet ok = 0;\nfor (const [nome, v, esperado] of casos) {\n  const r = looksLikeGoogleApiKey(v);\n  const passou = r === esperado;\n  ok += passou ? 1 : 0;\n  console.log(`${passou ? \"\u2705\" : \"\u274c\"} ${nome} \u2192 ${r} (esperado ${esperado})`);\n}\nconsole.log(`\\n${ok}/${casos.length}`);\nprocess.exit(ok === casos.length ? 0 : 1);\nEOF\nbun run /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/guard-test.ts; echo \"EXIT=$?\"",
  "description": "Verify the shape guard against real failure cases"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === o guard funciona? (teste direto da função, sem rede) ===
> error: Cannot find module './scripts/lib/gemini-image.ts' from '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/guard-test.ts'
> 
> Bun v1.3.12 (Linux arm64)
> EXIT=1
> ```

## 🤖 Claude *(03:52:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nS=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad\nsed -i 's#\"./scripts/lib/gemini-image.ts\"#\"/home/gcrUX/htdocs/constellation-orchestra/scripts/lib/gemini-image.ts\"#' $S/guard-test.ts\nbun run $S/guard-test.ts; echo \"EXIT=$?\"",
  "description": "Run the guard test with absolute import"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ chave real (AIza + 35 = 39) → true (esperado true)
> ✅ a sucata do SMOKETEST (22 ch) → false (esperado false)
> ✅ string vazia (tenant TikTok) → false (esperado false)
> ✅ null → false (esperado false)
> ✅ placeholder mascarado → false (esperado false)
> ✅ curta mas >10 (o guard antigo passava) → false (esperado false)
> 
> 6/6
> EXIT=0
> ```

## 🤖 Claude *(03:52:52)*

<details>
<summary>💭 Thinking Process</summary>

The test passed all checks, so I should move it into the permanent test suite using vitest. I need to figure out where to place it since the module lives in `scripts/lib/` but vitest tests are typically in `src/test/`, and I'm not sure if the vitest config includes the scripts directory.

</details>


## 🤖 Claude *(03:52:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"include|environment|test:\" vite.config.ts vitest.config.* 2>/dev/null | head -10\necho \"--- onde vivem os testes ---\"; ls src/test/ | head -8; find . -name \"*.test.ts\" -not -path \"./node_modules/*\" -not -path \"./src/*\" 2>/dev/null | head -5",
  "description": "Inspect vitest configuration and test layout"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> vitest.config.ts:7:  test: {
> vitest.config.ts:8:    environment: "jsdom",
> vitest.config.ts:11:    include: ["src/**/*.{test,spec}.{ts,tsx}", "supabase/functions/**/*.{test,spec}.ts", "scripts/**/*.{test,spec}.ts"],
> vitest.config.ts:15:      include: ["src/lib/**", "src/store/**", "src/hooks/**"],
> --- onde vivem os testes ---
> agentic-workspace.test.ts
> aios-sql-bridge-smoke.test.ts
> asset-publications.test.ts
> avatar-identity.test.ts
> avatar-voice.test.ts
> billing.test.ts
> canvas-dag.test.ts
> canvas-handles.test.ts
> ./scripts/motion/master-export.test.ts
> ./scripts/hyperframes/split-grid-frame.test.ts
> ./scripts/landing-bundler/ssrf-guard.test.ts
> ./scripts/lib/fetch-public-url.test.ts
> ./canvas-design/open-design/scripts/postinstall.test.ts
> ```

## 🤖 Claude *(03:52:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf; cat forense.log 2>/dev/null; wc -l *cuts.raw *cuts.txt 2>/dev/null; ps aux | grep -c \"[f]fmpeg\"",
  "description": "Check forensics v2 progress"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> oneiric cortes: 0
> 0 cully-cuts.txt
> 0 oneiric-cuts.txt
> 0 total
> 0
> ```

## 🤖 Claude *(03:53:11)*

<details>
<summary>💭 Thinking Process</summary>

I'm placing the test file at `scripts/lib/gemini-image.test.ts` since Vitest picks up tests in that pattern. The forensics output shows zero cuts and no ffmpeg processes running, which means the command completed but produced nothing — the `-cuts.raw` files aren't being generated, and the metadata print filter isn't outputting anything either. The issue seems to be with how the `select` filter is handling the scene detection threshold.

I'm realizing the `scdet` filter sets `lavfi.scd.score`, not `lavfi.scene_score`, so I need to use the right metadata key. The cleanest approach would be using `ffprobe` with the lavfi input to query scene cuts directly, or falling back to `scdet` which logs scene changes at info level. Let me start by writing the test file, then circle back to fix the forensics command itself.

Actually, I should also extract a contact sheet of representative frames so I can visually verify what's happening — the memory notes emphasize looking at the actual frames, not just relying on metrics. So my plan is to run scene detection on a downscaled version for speed, pull out a contact sheet, and then examine the images directly to validate the results.

</details>


## 🤖 Claude *(03:53:21)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/lib/gemini-image.test.ts",
  "content": "import { describe, expect, it } from \"vitest\";\nimport { looksLikeGoogleApiKey } from \"./gemini-image\";\n\n/**\n * Anticorpo do achado de 2026-08-14: **truthy n\u00e3o \u00e9 v\u00e1lido**.\n *\n * O cofre do tenant `85aaca76` (SMOKETEST) guardava 22 caracteres come\u00e7ando em `AIza` e\n * terminando em `called` \u2014 restos de uma mensagem de erro gravada no lugar da credencial.\n * O guard da \u00e9poca era `key.length > 10`, ent\u00e3o a sucata passava e ia para a API do Google,\n * que devolvia um HTTP 400 opaco no meio de um render.\n *\n * Uma chave malformada \u00e9 pior que chave ausente: ausente falha fechado com mensagem \u00fatil;\n * malformada falha aberto e sem explica\u00e7\u00e3o.\n */\ndescribe(\"looksLikeGoogleApiKey\", () => {\n  const CHAVE_VALIDA = `AIza${\"A\".repeat(35)}`; // AIza + 35 = 39 caracteres\n\n  it(\"aceita a forma can\u00f4nica do Google AI Studio (AIza + 35)\", () => {\n    expect(looksLikeGoogleApiKey(CHAVE_VALIDA)).toBe(true);\n    expect(looksLikeGoogleApiKey(\"AIzaSy-Bc_dEfGhIjKlMnOpQrStUvWxYz012345\")).toBe(true);\n  });\n\n  it(\"rejeita a sucata real que estava no cofre do SMOKETEST (22 caracteres)\", () => {\n    expect(looksLikeGoogleApiKey(\"AIzaSyMethodNotcalled\")).toBe(false);\n  });\n\n  it(\"rejeita o que o guard antigo (length > 10) deixava passar\", () => {\n    expect(looksLikeGoogleApiKey(\"AIzaAAAAAAAAAAA\")).toBe(false);\n  });\n\n  it(\"rejeita aus\u00eancia em todas as formas que o banco produz\", () => {\n    expect(looksLikeGoogleApiKey(\"\")).toBe(false); // string vazia \u2014 o que o tenant do review da TikTok tem\n    expect(looksLikeGoogleApiKey(null)).toBe(false);\n    expect(looksLikeGoogleApiKey(undefined)).toBe(false);\n  });\n\n  it(\"rejeita o placeholder da view mascarada\", () => {\n    expect(looksLikeGoogleApiKey(\"\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\")).toBe(false);\n  });\n\n  it(\"rejeita chave do tamanho certo mas com prefixo errado\", () => {\n    expect(looksLikeGoogleApiKey(`sk-o${\"A\".repeat(35)}`)).toBe(false);\n  });\n\n  it(\"rejeita chave com o comprimento certo e caractere fora do alfabeto\", () => {\n    expect(looksLikeGoogleApiKey(`AIza${\"A\".repeat(34)}!`)).toBe(false);\n  });\n\n  it(\"rejeita chave longa demais (colagem com lixo no fim)\", () => {\n    expect(looksLikeGoogleApiKey(`${CHAVE_VALIDA}extra`)).toBe(false);\n  });\n});\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/lib/gemini-image.test.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(03:53:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "timeout 300 npx vitest run scripts/lib/gemini-image.test.ts 2>&1 | tail -15",
  "description": "Run the new anticorpo test",
  "timeout": 330000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  RUN  v3.2.4 /home/gcrUX/htdocs/constellation-orchestra
> 
>  ✓ scripts/lib/gemini-image.test.ts (8 tests) 6ms
> 
>  Test Files  1 passed (1)
>       Tests  8 passed (8)
>    Start at  00:53:27
>    Duration  2.04s (transform 143ms, setup 270ms, collect 46ms, tests 6ms, environment 825ms, prepare 113ms)
> ```

## 🤖 Claude *(03:53:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\n# 3a tentativa: ffprobe via lavfi \u00e9 o caminho determin\u00edstico (metadata=print n\u00e3o carrega scene score)\nnohup bash -c '\nfor f in oneiric cully; do\n  ffprobe -v error -f lavfi -i \"movie=$f.mp4,scale=426:-2,select=gt(scene\\,0.30)\" \\\n    -show_entries frame=pts_time -of csv=p=0 > $f-cuts.txt 2>$f-cuts.err\n  echo \"$f cortes: $(grep -c . $f-cuts.txt)\"\ndone' > forense.log 2>&1 &\nsleep 45; cat forense.log; wc -l *cuts.txt; head -3 oneiric-cuts.txt; head -3 oneiric-cuts.err 2>/dev/null",
  "description": "Scene detection via ffprobe lavfi",
  "timeout": 120000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   0 cully-cuts.txt
>  83 oneiric-cuts.txt
>  83 total
> 12.354333
> 14.396000
> 28.562667
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:54:24)*

<details>
<summary>💭 Thinking Process</summary>

All 8 tests are passing and the scene detection is working well with 83 cuts detected so far on the oneiric footage. While that finishes running, I should extract some representative frames and visually inspect them to make sure the detection is actually working correctly. Let me pull a contact sheet from the oneiric file, check the workflow status, and grab those frames for review.

</details>


## 🤖 Claude *(03:54:24)*

Testes 8/8 e detecção de cortes funcionando. Vou extrair frames para **olhar** a referência.

## 🤖 Claude *(03:54:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nmkdir -p frames\n# 12 frames espa\u00e7ados ao longo do curta, em 640px, num contact sheet 4x3\nffmpeg -y -hide_banner -loglevel error -i oneiric.mp4 -vf \"fps=1/95,scale=640:-2,tile=4x3\" -frames:v 1 frames/oneiric-sheet.jpg 2>&1\nls -la frames/oneiric-sheet.jpg",
  "description": "Build contact sheet from ONEIRIC",
  "timeout": 300000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu 127081 Aug 14 00:57 frames/oneiric-sheet.jpg
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(03:57:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf/frames/oneiric-sheet.jpg"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/jpeg'}}]
> ```

## 👤 User *(03:57:37)*

[Image: original 2560x804, displayed at 2000x628. Multiply coordinates by 1.28 to map to original image.]

## 🤖 Claude *(03:57:51)*

<details>
<summary>💭 Thinking Process</summary>

I'm noticing a consistent pattern across the frames—foreground occlusion is a defining feature of the MONTAR ruler. Whether it's an out-of-focus hand at the edge, posters framing the subject, or a massive gun barrel looming in the foreground, there's always something between the camera and the main focus, creating depth through layered obstruction.

The depth structure is relentless: every shot has at least three distinct planes, from dark foreground walls to mid-ground subjects to lit backgrounds. Light always has intention—a warm window glow, a single source at the end of a corridor, rim light catching a rider against the sunset. The 2.39:1 anamorphic format with its characteristic oval bokeh reinforces this cinematic language, and the composition deliberately uses negative space, leaving subjects off-center in vast, breathing frames. Each world has its own color discipline: warm amber for the dorm, cold cyan for space, golden-teal for the fantasy sequence, desaturated darkness for the lab. I should pull the cully sheet and check the workflow status while the scene detection runs.

</details>


## 🤖 Claude *(03:57:51)*

A referência está clara no quadro. Vou ver o segundo.

## 🤖 Claude *(03:57:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/863fa9e6-3ea7-490f-99e3-99a1876199e3/scratchpad/hf\nffmpeg -y -hide_banner -loglevel error -ss 300 -i cully.mp4 -vf \"fps=1/140,scale=640:-2,tile=4x3\" -frames:v 1 frames/cully-sheet.jpg 2>&1\nls -la frames/cully-sheet.jpg; cat forense.log; wc -l *cuts.txt",
  "description": "Build contact sheet from Cully Hill Boys",
  "timeout": 300000
}
```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-08-12 - agent-aeade303039331f28]]
> * **Próxima Sessão**: [[2026-08-14 - Revisar piloto de vídeo motion e aprovar camadas Z]]
%% --- TIMELINE END --- %%
